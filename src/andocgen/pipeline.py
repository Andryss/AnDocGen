from __future__ import annotations

import time
from dataclasses import dataclass
from pathlib import Path

from andocgen.call_graph.base import CallGraphBuilder
from andocgen.call_graph.factory import create_call_graph_builder
from andocgen.config import AppConfig
from andocgen.config_values import config_bool, config_int, config_str
from andocgen.context.doc_brief_registry import DocBriefRegistry
from andocgen.context.factory import ContextComponents, create_context_components
from andocgen.context.previous_doc_registry import seed_registry_from_previous_docs
from andocgen.generation_plan import CacheSnapshot, build_generation_plan, changed_doc_modules
from andocgen.generator.factory import GeneratorComponents, create_generator_components
from andocgen.llm.factory import create_llm_provider, create_llm_provider_factory
from andocgen.models.entities import (
    CallGraph,
    DocBlock,
    EntityContext,
    GenerationError,
    IssueCategory,
    IssueLevel,
    ModuleModel,
    ParseError,
    PipelineResult,
    ProjectModel,
    ValidationIssue,
)
from andocgen.output.factory import OutputComponents, create_output_components
from andocgen.parser.base import SourceParser
from andocgen.parser.factory import create_parser
from andocgen.reporting.base import Reporter, TraceLogger
from andocgen.reporting.factory import create_reporter
from andocgen.reporting.implementations.null_progress import NullProgressReporter
from andocgen.reporting.progress import ProgressReporter
from andocgen.reporting.timing import StageTimer
from andocgen.scanner.base import ProjectScanner
from andocgen.scanner.factory import create_scanner
from andocgen.validator.base import DocumentationValidator
from andocgen.validator.factory import create_validator


@dataclass
class _ParsedProject:
    all_module_paths: list[str]
    all_modules: list[ModuleModel]
    changed_modules: list[ModuleModel]


@dataclass
class _PipelineComponents:
    scanner: ProjectScanner
    parser: SourceParser
    call_graph_builder: CallGraphBuilder
    context_components: ContextComponents
    output_components: OutputComponents
    validator: DocumentationValidator
    reporter: Reporter


@dataclass
class _GenerationWork:
    contexts: list[EntityContext]
    ordered: list[EntityContext]
    changed_modules: list[ModuleModel]


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
    components = _create_pipeline_components(config, write_reports)
    trace = components.reporter.create_trace_logger(config)

    project_path = project_path.resolve()
    out_dir = config.resolve_output_dir()
    cache_dir = config.resolve_cache_dir()
    incremental = bool(config.generation.incremental)
    cache_snapshot = (
        components.output_components.cache_store.load_snapshot(cache_dir)
        if incremental
        else CacheSnapshot()
    )

    progress.on_stage(f"AnDocGen — {project_path.name}")
    mode_label = "dry-run" if dry_run else str(config.generation.provider or "mock")
    progress.on_stage(f"Mode: {mode_label} | workers: {config_int(config.generation.workers, 1)}")

    trace.info(
        f"AnDocGen run: project={project_path} "
        f"provider={config.generation.provider or 'mock'} dry_run={dry_run}"
    )
    trace.info(f"Output directory: {out_dir}")

    parsed = _scan_and_parse(project_path, config, components, trace, progress, result)
    project = _build_project_model(project_path, config, components, parsed.all_modules)

    if not parsed.all_modules:
        result.elapsed_seconds = time.perf_counter() - start
        return components.reporter.write_reports(result, config)

    with StageTimer(trace, "call_graph"):
        graph = components.call_graph_builder.build(project)
    trace.debug(
        f"Call graph: {len(graph.nodes)} nodes, {len(graph.edges)} edges"
    )

    work = _prepare_generation_work(
        project_path,
        project,
        graph,
        parsed,
        config,
        components,
        cache_snapshot,
        out_dir,
        trace,
        result,
    )
    if not work.ordered:
        result.elapsed_seconds = time.perf_counter() - start
        trace.info("Incremental run: no affected entities, generation skipped")
        return components.reporter.write_reports(result, config)

    progress.on_stage(f"{'Would generate' if dry_run else 'Generating'} {len(work.ordered)} entities...")
    trace.info(f"{'Dry-run' if dry_run else 'Generating'} documentation for {len(work.ordered)} entities")

    if dry_run:
        result.dry_run_entities = len(work.ordered)
        result.elapsed_seconds = time.perf_counter() - start
        trace.info(f"Dry-run finished: {len(work.ordered)} entities, {len(graph.edges)} call-graph edges")
        return components.reporter.write_reports(result, config)

    try:
        blocks, gen_errors = _generate_blocks(
            work,
            graph,
            parsed.all_module_paths,
            config,
            components,
            out_dir,
            trace,
            progress,
            result,
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
        return components.reporter.write_reports(result, config)

    result.generation_errors.extend(gen_errors)
    result.doc_blocks = blocks
    for err in gen_errors:
        trace.error(f"Generation error {err.module_path} {err.entity_name}: {err.message}")

    _validate_blocks(blocks, work.contexts, config, components.validator, trace, result)
    _write_outputs_and_cache(
        project,
        blocks,
        work.changed_modules,
        parsed,
        config,
        components,
        out_dir,
        cache_dir,
        cache_snapshot,
        graph,
        trace,
        result,
    )

    result.elapsed_seconds = time.perf_counter() - start
    trace.info(f"Pipeline finished in {result.elapsed_seconds:.2f}s")
    return components.reporter.write_reports(result, config)


def _create_pipeline_components(config: AppConfig, write_reports: bool) -> _PipelineComponents:
    return _PipelineComponents(
        scanner=create_scanner(config.discovery),
        parser=create_parser(config.extraction),
        call_graph_builder=create_call_graph_builder(config.call_graph),
        context_components=create_context_components(config.context),
        output_components=create_output_components(config.output),
        validator=create_validator(config.validation),
        reporter=create_reporter(config.reporting) if write_reports else _NullReporter(),
    )


def _scan_and_parse(
    project_path: Path,
    config: AppConfig,
    components: _PipelineComponents,
    trace: TraceLogger,
    progress: ProgressReporter,
    result: PipelineResult,
) -> _ParsedProject:
    with StageTimer(trace, "scan"):
        files = components.scanner.scan(project_path, config.discovery)
    progress.on_stage(f"Scanning {len(files)} files...")
    trace.info(f"Found {len(files)} files")

    with StageTimer(trace, "parse", f"{len(files)} files"):
        return _scan_and_parse_project(
            files,
            project_path,
            config,
            components.scanner,
            components.parser,
            trace,
            result,
        )


def _build_project_model(
    project_path: Path,
    config: AppConfig,
    components: _PipelineComponents,
    modules: list[ModuleModel],
) -> ProjectModel:
    metadata = components.context_components.metadata_loader
    return ProjectModel(
        project_path=str(project_path),
        modules=modules,
        project_name=config.project.name or project_path.name,
        project_description=metadata.load_project_description(
            project_path,
            config_str(config.project.description),
        ),
    )


def _prepare_generation_work(
    project_path: Path,
    project: ProjectModel,
    graph: CallGraph,
    parsed: _ParsedProject,
    config: AppConfig,
    components: _PipelineComponents,
    cache_snapshot: CacheSnapshot,
    out_dir: Path,
    trace: TraceLogger,
    result: PipelineResult,
) -> _GenerationWork:
    readme = components.context_components.metadata_loader.load_readme_excerpt(
        project_path,
        config_int(config.context.readme_limit, 2000),
        config_str(config.project.readme_path),
    )
    contexts = _build_contexts(project, config, components, readme, {})
    ordered = components.call_graph_builder.order_entities(contexts, graph)
    changed_modules = parsed.changed_modules

    if not config_bool(config.generation.incremental, True):
        return _GenerationWork(contexts=contexts, ordered=ordered, changed_modules=changed_modules)

    plan = build_generation_plan(project, graph, cache_snapshot)
    affected_paths = plan.affected_module_paths
    result.processed_files = sorted(affected_paths)
    result.skipped_files = sorted(path for path in parsed.all_module_paths if path not in affected_paths)
    ordered = [ctx for ctx in ordered if ctx.module_path in affected_paths]
    changed_modules = [module for module in parsed.all_modules if module.path in affected_paths]

    if affected_paths:
        previous_docs = components.output_components.previous_doc_loader.extract(
            out_dir,
            sorted(affected_paths),
            language=config_str(config.generation.language, "ru"),
        )
        if previous_docs:
            trace.debug(f"Loaded {len(previous_docs)} previous doc fragments for affected modules")
        contexts = _build_contexts(project, config, components, readme, previous_docs)
        context_by_id = {ctx.entity_id: ctx for ctx in contexts}
        ordered = [context_by_id[ctx.entity_id] for ctx in ordered if ctx.entity_id in context_by_id]

    for entity_id in plan.generated_entity_ids:
        trace.debug(f"Incremental reason {entity_id}: {plan.reasons[entity_id]}")

    return _GenerationWork(contexts=contexts, ordered=ordered, changed_modules=changed_modules)


def _build_contexts(
    project: ProjectModel,
    config: AppConfig,
    components: _PipelineComponents,
    readme: str | None,
    previous_docs: dict[str, str],
) -> list[EntityContext]:
    return components.context_components.context_builder.build(
        project,
        config.context,
        output_language=config_str(config.generation.language, "ru"),
        readme_excerpt=readme,
        previous_docs=previous_docs,
    )


def _generate_blocks(
    work: _GenerationWork,
    graph: CallGraph,
    all_module_paths: list[str],
    config: AppConfig,
    components: _PipelineComponents,
    out_dir: Path,
    trace: TraceLogger,
    progress: ProgressReporter,
    result: PipelineResult,
) -> tuple[list[DocBlock], list[GenerationError]]:
    seed_registry = _seed_brief_registry(
        work.contexts,
        all_module_paths,
        config,
        components,
        out_dir,
        trace,
        result,
    )
    generator_components = create_generator_components(config.generation, config.output)
    return _run_document_generator(
        generator_components,
        work,
        graph,
        config,
        components,
        seed_registry,
        trace,
        progress,
    )


def _seed_brief_registry(
    contexts: list[EntityContext],
    all_module_paths: list[str],
    config: AppConfig,
    components: _PipelineComponents,
    out_dir: Path,
    trace: TraceLogger,
    result: PipelineResult,
) -> DocBriefRegistry:
    seed_registry = DocBriefRegistry()
    if not config_bool(config.generation.incremental, True):
        return seed_registry
    unchanged_paths = [path for path in all_module_paths if path not in result.processed_files]
    if not unchanged_paths:
        return seed_registry
    brief_docs = components.output_components.previous_doc_loader.extract(
        out_dir,
        unchanged_paths,
        language=config_str(config.generation.language, "ru"),
    )
    seed_registry_from_previous_docs(seed_registry, brief_docs, contexts)
    if brief_docs:
        trace.debug(f"Seeded brief registry from {len(brief_docs)} previous doc fragments")
    return seed_registry


def _run_document_generator(
    generator_components: GeneratorComponents,
    work: _GenerationWork,
    graph: CallGraph,
    config: AppConfig,
    components: _PipelineComponents,
    seed_registry: DocBriefRegistry,
    trace: TraceLogger,
    progress: ProgressReporter,
) -> tuple[list[DocBlock], list[GenerationError]]:
    llm = create_llm_provider(config.generation)
    llm_factory = (
        create_llm_provider_factory(config.generation)
        if config_int(config.generation.workers, 1) > 1
        else None
    )
    with StageTimer(trace, "generate", f"{len(work.ordered)} entities"):
        return generator_components.document_generator.generate(
            work.ordered,
            llm,
            config.generation,
            config.context,
            graph,
            components.call_graph_builder,
            components.context_components.context_builder,
            components.context_components.prompt_builder,
            trace=trace,
            progress=progress,
            llm_factory=llm_factory,
            validation_config=config.validation,
            seed_registry=seed_registry,
        )


def _validate_blocks(
    blocks: list[DocBlock],
    contexts: list[EntityContext],
    config: AppConfig,
    validator: DocumentationValidator,
    trace: TraceLogger,
    result: PipelineResult,
) -> None:
    with StageTimer(trace, "validate"):
        result.issues = validator.validate(blocks, contexts, config.validation)
        result.issues.extend(_fallback_issues(blocks))
    trace.info(f"Validation: {len(result.warnings)} warnings, {len(result.errors)} errors")


def _write_outputs_and_cache(
    project: ProjectModel,
    blocks: list[DocBlock],
    changed_modules: list[ModuleModel],
    parsed: _ParsedProject,
    config: AppConfig,
    components: _PipelineComponents,
    out_dir: Path,
    cache_dir: Path,
    cache_snapshot: CacheSnapshot,
    graph: CallGraph,
    trace: TraceLogger,
    result: PipelineResult,
) -> None:
    if not changed_modules:
        return

    write_blocks = blocks
    if config_bool(config.generation.incremental, True):
        changed_doc_paths = changed_doc_modules(blocks, cache_snapshot)
        write_blocks = [block for block in blocks if block.module_path in changed_doc_paths]
        if not write_blocks:
            trace.info("Generated doc hashes unchanged; markdown rewrite skipped")

    if write_blocks:
        with StageTimer(trace, "write"):
            output_files = components.output_components.writer.write(
                project,
                write_blocks,
                config.output,
                out_dir,
                all_module_paths=parsed.all_module_paths,
                language=config_str(config.generation.language, "ru"),
            )
        result.output_files = output_files
        trace.info(f"Wrote {len(output_files)} output files")
        for path in output_files:
            trace.debug(f"  output: {path}")

    cache_modules = (
        [module for module in parsed.all_modules if module.path in set(result.processed_files)]
        if config_bool(config.generation.incremental, True)
        else changed_modules
    )
    components.output_components.cache_store.update(cache_dir, cache_modules, blocks, graph)


def _scan_and_parse_project(
    files: list[Path],
    project_path: Path,
    config: AppConfig,
    scanner: ProjectScanner,
    parser: SourceParser,
    trace: TraceLogger,
    result: PipelineResult,
) -> _ParsedProject:
    all_module_paths: list[str] = []
    all_modules: list[ModuleModel] = []
    changed_modules: list[ModuleModel] = []
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
