from __future__ import annotations

import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from andocgen.call_graph.factory import create_call_graph_builder
from andocgen.config import AppConfig
from andocgen.context.doc_brief_registry import DocBriefRegistry
from andocgen.context.factory import create_context_components
from andocgen.context.previous_doc_registry import seed_registry_from_previous_docs
from andocgen.generation_plan import CacheSnapshot, build_generation_plan, changed_doc_modules
from andocgen.generator.factory import create_generator_components
from andocgen.llm.factory import create_llm_provider, create_llm_provider_factory
from andocgen.models.entities import (
    DocBlock,
    GenerationError,
    IssueCategory,
    IssueLevel,
    ParseError,
    PipelineResult,
    ProjectModel,
    ValidationIssue,
)
from andocgen.output.factory import create_output_components
from andocgen.parser.factory import create_parser
from andocgen.reporting.factory import create_reporter
from andocgen.reporting.implementations.file_reporter import StageTimer
from andocgen.reporting.implementations.null_progress import NullProgressReporter
from andocgen.reporting.progress import ProgressReporter
from andocgen.scanner.factory import create_scanner
from andocgen.validator.factory import create_validator


@dataclass
class _ParsedProject:
    all_module_paths: list[str]
    all_modules: list
    changed_modules: list


def run_pipeline(
    project_path: Path,
    config: AppConfig,
    progress: ProgressReporter | None = None,
    *,
    dry_run: bool = False,
    write_reports: bool = True,
) -> PipelineResult:
    start = time.perf_counter()
    result = PipelineResult()
    progress = progress or NullProgressReporter()

    scanner = create_scanner(config.discovery)
    parser = create_parser(config.extraction)
    call_graph_builder = create_call_graph_builder(config.call_graph)
    context_components = create_context_components(config.context)
    output_components = create_output_components(config.output)
    validator = create_validator(config.validation)
    reporter = create_reporter(config.reporting) if write_reports else _NullReporter()

    trace = reporter.create_trace_logger(config)

    project_path = project_path.resolve()
    out_dir = config.resolve_output_dir()
    cache_dir = config.resolve_cache_dir()
    cache_snapshot = (
        output_components.cache_store.load_snapshot(cache_dir)
        if config.generation.incremental
        else CacheSnapshot()
    )

    progress.on_stage(f"AnDocGen — {project_path.name}")
    mode_label = "dry-run" if dry_run else str(config.generation.provider)
    progress.on_stage(f"Mode: {mode_label} | workers: {config.generation.workers}")

    trace.info(f"AnDocGen run: project={project_path} provider={config.generation.provider} dry_run={dry_run}")
    trace.info(f"Output directory: {out_dir}")

    with StageTimer(trace, "scan"):
        files = scanner.scan(project_path, config.discovery)
    progress.on_stage(f"Scanning {len(files)} files...")
    trace.info(f"Found {len(files)} files")

    with StageTimer(trace, "parse", f"{len(files)} files"):
        parsed = _scan_and_parse_project(files, project_path, config, scanner, parser, trace, result)
    all_module_paths = parsed.all_module_paths
    all_modules = parsed.all_modules
    changed_modules = parsed.changed_modules

    project = ProjectModel(
        project_path=str(project_path),
        modules=all_modules,
        project_name=config.project.name or project_path.name,
        project_description=context_components.metadata_loader.load_project_description(
            project_path, config.project.description
        ),
    )

    if not all_modules:
        result.elapsed_seconds = time.perf_counter() - start
        return reporter.write_reports(result, config)

    with StageTimer(trace, "call_graph"):
        graph = call_graph_builder.build(project)
    trace.debug(
        f"Call graph: {len(graph.nodes)} nodes, {len(graph.edges)} edges"
    )

    readme = context_components.metadata_loader.load_readme_excerpt(
        project_path, config.context.readme_limit, config.project.readme_path
    )
    previous_docs: dict[str, str] = {}

    contexts = context_components.context_builder.build(
        project,
        config.context,
        output_language=config.generation.language,
        readme_excerpt=readme,
        previous_docs=previous_docs,
    )
    ordered = call_graph_builder.order_entities(contexts, graph)
    if config.generation.incremental:
        plan = build_generation_plan(project, graph, cache_snapshot)
        affected_paths = plan.affected_module_paths
        result.processed_files = sorted(affected_paths)
        result.skipped_files = sorted(path for path in all_module_paths if path not in affected_paths)
        ordered = [ctx for ctx in ordered if ctx.module_path in affected_paths]
        changed_modules = [module for module in all_modules if module.path in affected_paths]
        if affected_paths:
            previous_docs = output_components.previous_doc_loader.extract(
                out_dir,
                sorted(affected_paths),
                language=config.generation.language,
            )
            if previous_docs:
                trace.debug(f"Loaded {len(previous_docs)} previous doc fragments for affected modules")
            contexts = context_components.context_builder.build(
                project,
                config.context,
                output_language=config.generation.language,
                readme_excerpt=readme,
                previous_docs=previous_docs,
            )
            context_by_id = {ctx.entity_id: ctx for ctx in contexts}
            ordered = [context_by_id[ctx.entity_id] for ctx in ordered if ctx.entity_id in context_by_id]
        for entity_id in plan.generated_entity_ids:
            trace.debug(f"Incremental reason {entity_id}: {plan.reasons[entity_id]}")
        if not ordered:
            result.elapsed_seconds = time.perf_counter() - start
            trace.info("Incremental run: no affected entities, generation skipped")
            return reporter.write_reports(result, config)

    progress.on_stage(f"{'Would generate' if dry_run else 'Generating'} {len(ordered)} entities...")
    trace.info(f"{'Dry-run' if dry_run else 'Generating'} documentation for {len(ordered)} entities")

    if dry_run:
        result.dry_run_entities = len(ordered)
        result.elapsed_seconds = time.perf_counter() - start
        trace.info(f"Dry-run finished: {len(ordered)} entities, {len(graph.edges)} call-graph edges")
        return reporter.write_reports(result, config)

    seed_registry = DocBriefRegistry()
    if config.generation.incremental:
        unchanged_paths = [path for path in all_module_paths if path not in result.processed_files]
        if unchanged_paths:
            brief_docs = output_components.previous_doc_loader.extract(
                out_dir,
                unchanged_paths,
                language=config.generation.language,
            )
            seed_registry_from_previous_docs(seed_registry, brief_docs, contexts)
            if brief_docs:
                trace.debug(f"Seeded brief registry from {len(brief_docs)} previous doc fragments")

    generator_components = create_generator_components(config.generation, config.output)
    llm = create_llm_provider(config.generation)
    llm_factory = (
        create_llm_provider_factory(config.generation)
        if config.generation.workers > 1
        else None
    )
    try:
        with StageTimer(trace, "generate", f"{len(ordered)} entities"):
            blocks, gen_errors = generator_components.document_generator.generate(
                ordered,
                llm,
                config.generation,
                config.context,
                graph,
                call_graph_builder,
                context_components.context_builder,
                context_components.prompt_builder,
                trace=trace,
                progress=progress,
                llm_factory=llm_factory,
                validation_config=config.validation,
                seed_registry=seed_registry,
            )
    except RuntimeError as exc:
        result.generation_errors.append(
            GenerationError(
                module_path="",
                entity_type=None,
                entity_name=None,
                message=str(exc),
            )
        )
        trace.error(str(exc))
        result.elapsed_seconds = time.perf_counter() - start
        return reporter.write_reports(result, config)

    result.generation_errors.extend(gen_errors)
    result.doc_blocks = blocks
    for err in gen_errors:
        trace.error(f"Generation error {err.module_path} {err.entity_name}: {err.message}")

    with StageTimer(trace, "validate"):
        result.issues = validator.validate(blocks, contexts, config.validation)
        result.issues.extend(_fallback_issues(blocks))
    trace.info(
        f"Validation: {len(result.warnings)} warnings, {len(result.errors)} errors"
    )

    if changed_modules:
        write_blocks = blocks
        if config.generation.incremental:
            changed_doc_paths = changed_doc_modules(blocks, cache_snapshot)
            write_blocks = [block for block in blocks if block.module_path in changed_doc_paths]
            if not write_blocks:
                trace.info("Generated doc hashes unchanged; markdown rewrite skipped")

        if write_blocks:
            with StageTimer(trace, "write"):
                output_files = output_components.writer.write(
                    project,
                    write_blocks,
                    config.output,
                    out_dir,
                    all_module_paths=all_module_paths,
                    language=config.generation.language,
                )
            result.output_files = output_files
            trace.info(f"Wrote {len(output_files)} output files")
            for path in output_files:
                trace.debug(f"  output: {path}")

        cache_modules = (
            [module for module in all_modules if module.path in set(result.processed_files)]
            if config.generation.incremental
            else changed_modules
        )
        output_components.cache_store.update(cache_dir, cache_modules, blocks, graph)

    result.elapsed_seconds = time.perf_counter() - start
    trace.info(f"Pipeline finished in {result.elapsed_seconds:.2f}s")
    return reporter.write_reports(result, config)


def _scan_and_parse_project(
    files: list[Path],
    project_path: Path,
    config: AppConfig,
    scanner: Any,
    parser: Any,
    trace: Any,
    result: PipelineResult,
) -> _ParsedProject:
    all_module_paths: list[str] = []
    all_modules = []
    changed_modules = []
    for file_path in files:
        rel = str(file_path.relative_to(project_path))
        all_module_paths.append(rel)
        file_hash = scanner.file_hash(file_path)

        trace.debug(f"Parsing: {rel}")
        parse_result = parser.parse(file_path, project_path, content_hash=file_hash)
        if parse_result.error:
            result.parse_errors.append(ParseError(module_path=rel, message=parse_result.error))
            trace.error(f"Parse error in {rel}: {parse_result.error}")
            continue

        assert parse_result.module is not None
        all_modules.append(parse_result.module)

        if not config.generation.incremental:
            changed_modules.append(parse_result.module)
            result.processed_files.append(rel)
        trace.debug(
            f"  parsed {rel}: "
            f"{len(parse_result.module.functions)} functions, "
            f"{len(parse_result.module.classes)} classes"
        )

    return _ParsedProject(
        all_module_paths=all_module_paths,
        all_modules=all_modules,
        changed_modules=changed_modules,
    )


class _NullTraceLogger:
    def info(self, message: str) -> None:
        pass

    def debug(self, message: str) -> None:
        pass

    def error(self, message: str) -> None:
        pass

    def log_stage(self, stage: str, detail: str = "", duration_ms: float | None = None) -> None:
        pass

    def log_llm_request(self, entity_id: str, system: str, user: str) -> None:
        pass

    def log_llm_response(self, entity_id: str, response: str, duration_ms: float, parsed: bool) -> None:
        pass

    def log_llm_attempt(
        self,
        *,
        entity_id: str,
        entity_type: str,
        entity_name: str,
        module_path: str,
        provider: str,
        model: str,
        attempt: int,
        duration_ms: float,
        system: str,
        user: str,
        raw_response: str,
        parse_ok: bool,
        validation_ok: bool,
        retry_reason: str | None = None,
        fallback_reason: str | None = None,
        structured_format: str | None = None,
    ) -> None:
        pass


class _NullReporter:
    def write_reports(self, result: PipelineResult, config: AppConfig) -> PipelineResult:
        return result

    def create_trace_logger(self, config: AppConfig) -> _NullTraceLogger:
        return _NullTraceLogger()


def _fallback_issues(blocks: list[DocBlock]) -> list[ValidationIssue]:
    return [
        ValidationIssue(
            level=IssueLevel.WARNING,
            category=IssueCategory.GENERATION,
            message="fallback_generated",
            module_path=block.module_path,
            entity_type=block.entity_type,
            entity_name=block.entity_name,
            detail=block.fallback_reason,
        )
        for block in blocks
        if block.fallback
    ]
