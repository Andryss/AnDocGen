from __future__ import annotations

import time
from pathlib import Path

from andocgen.call_graph.factory import create_call_graph_builder
from andocgen.config import AppConfig
from andocgen.context.doc_brief_registry import DocBriefRegistry
from andocgen.context.factory import create_context_components
from andocgen.context.previous_doc_registry import seed_registry_from_previous_docs
from andocgen.generator.factory import create_generator_components
from andocgen.llm.factory import create_llm_provider, create_llm_provider_factory
from andocgen.models.entities import GenerationError, ParseError, PipelineResult, ProjectModel
from andocgen.output.factory import create_output_components
from andocgen.parser.factory import create_parser
from andocgen.reporting.factory import create_reporter
from andocgen.reporting.implementations.file_reporter import StageTimer
from andocgen.reporting.implementations.null_progress import NullProgressReporter
from andocgen.reporting.progress import ProgressReporter
from andocgen.scanner.factory import create_scanner
from andocgen.validator.factory import create_validator


def run_pipeline(
    project_path: Path,
    config: AppConfig,
    progress: ProgressReporter | None = None,
    *,
    dry_run: bool = False,
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
    reporter = create_reporter(config.reporting)

    trace = reporter.create_trace_logger(config)

    project_path = project_path.resolve()
    out_dir = config.resolve_output_dir()
    cache_dir = config.resolve_cache_dir()
    cache = output_components.cache_store.load(cache_dir) if config.generation.incremental else {}

    progress.on_stage(f"AnDocGen — {project_path.name}")
    mode_label = "dry-run" if dry_run else str(config.generation.provider)
    progress.on_stage(f"Mode: {mode_label} | workers: {config.generation.workers}")

    trace.info(f"AnDocGen run: project={project_path} provider={config.generation.provider} dry_run={dry_run}")
    trace.info(f"Output directory: {out_dir}")

    with StageTimer(trace, "scan"):
        files = scanner.scan(project_path, config.discovery)
    progress.on_stage(f"Scanning {len(files)} files...")
    trace.info(f"Found {len(files)} files")

    all_module_paths: list[str] = []
    all_modules = []
    changed_modules = []
    changed_paths: set[str] = set()

    with StageTimer(trace, "parse", f"{len(files)} files"):
        for file_path in files:
            rel = str(file_path.relative_to(project_path))
            all_module_paths.append(rel)
            file_hash = scanner.file_hash(file_path)
            unchanged = (
                config.generation.incremental
                and cache.get(rel) == file_hash
            )

            trace.debug(f"Parsing: {rel}")
            parse_result = parser.parse(file_path, project_path, content_hash=file_hash)
            if parse_result.error:
                result.parse_errors.append(ParseError(module_path=rel, message=parse_result.error))
                trace.error(f"Parse error in {rel}: {parse_result.error}")
                continue

            assert parse_result.module is not None
            all_modules.append(parse_result.module)

            if unchanged:
                result.skipped_files.append(rel)
                trace.debug(f"Unchanged file (skip LLM): {rel}")
            else:
                changed_modules.append(parse_result.module)
                changed_paths.add(rel)
                result.processed_files.append(rel)
                trace.debug(
                    f"  parsed {rel}: "
                    f"{len(parse_result.module.functions)} functions, "
                    f"{len(parse_result.module.classes)} classes"
                )

    project = ProjectModel(
        project_path=str(project_path),
        modules=all_modules,
        project_name=config.project.name or project_path.name,
        project_description=context_components.metadata_loader.load_project_description(
            project_path, config.project.description
        ),
    )

    if config.generation.incremental and not changed_modules:
        if all_module_paths:
            readme_project = ProjectModel(
                project_path=str(project_path),
                modules=all_modules,
                project_name=project.project_name,
                project_description=project.project_description,
            )
            readme_path = out_dir / "README.md"
            out_dir.mkdir(parents=True, exist_ok=True)
            readme_path.write_text(
                output_components.writer.render_project_readme(
                    readme_project, all_module_paths, language=config.generation.language
                ),
                encoding="utf-8",
            )
            result.output_files.append(str(readme_path))
        result.elapsed_seconds = time.perf_counter() - start
        trace.info("Incremental run: no changed files, generation skipped")
        return reporter.write_reports(result, config)

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
    if config.generation.incremental and changed_paths:
        previous_docs = output_components.previous_doc_loader.extract(
            out_dir,
            [m.path for m in changed_modules],
            language=config.generation.language,
        )
        if previous_docs:
            trace.debug(f"Loaded {len(previous_docs)} previous doc fragments for changed modules")

    contexts = context_components.context_builder.build(
        project,
        config.context,
        output_language=config.generation.language,
        readme_excerpt=readme,
        previous_docs=previous_docs,
    )
    ordered = call_graph_builder.order_entities(contexts, graph)
    if config.generation.incremental:
        ordered = [ctx for ctx in ordered if ctx.module_path in changed_paths]

    progress.on_stage(f"{'Would generate' if dry_run else 'Generating'} {len(ordered)} entities...")
    trace.info(f"{'Dry-run' if dry_run else 'Generating'} documentation for {len(ordered)} entities")

    if dry_run:
        result.dry_run_entities = len(ordered)
        result.elapsed_seconds = time.perf_counter() - start
        trace.info(f"Dry-run finished: {len(ordered)} entities, {len(graph.edges)} call-graph edges")
        return reporter.write_reports(result, config)

    seed_registry = DocBriefRegistry()
    if config.generation.incremental:
        unchanged_paths = [path for path in all_module_paths if path not in changed_paths]
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
    for err in gen_errors:
        trace.error(f"Generation error {err.module_path} {err.entity_name}: {err.message}")

    with StageTimer(trace, "validate"):
        result.issues = validator.validate(blocks, contexts, config.validation)
    trace.info(
        f"Validation: {len(result.warnings)} warnings, {len(result.errors)} errors"
    )

    if changed_modules:
        with StageTimer(trace, "write"):
            output_files = output_components.writer.write(
                project,
                blocks,
                config.output,
                out_dir,
                all_module_paths=all_module_paths,
                language=config.generation.language,
            )
        result.output_files = output_files
        output_components.cache_store.update(cache_dir, changed_modules)
        trace.info(f"Wrote {len(output_files)} output files")
        for path in output_files:
            trace.debug(f"  output: {path}")

    result.elapsed_seconds = time.perf_counter() - start
    trace.info(f"Pipeline finished in {result.elapsed_seconds:.2f}s")
    return reporter.write_reports(result, config)
