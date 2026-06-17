from __future__ import annotations

from andocgen.config import ContextConfig
from andocgen.context.doc_brief_registry import DocBriefRegistry
from andocgen.models.entities import (
    CalledEntityDoc,
    CallGraph,
    EntityContext,
    ProjectModel,
    make_entity_id,
)


class DefaultContextBuilder:
    def build(
        self,
        project: ProjectModel,
        config: ContextConfig,
        output_language: str = "ru",
        readme_excerpt: str | None = None,
        previous_docs: dict[str, str] | None = None,
    ) -> list[EntityContext]:
        previous_docs = previous_docs or {}
        contexts: list[EntityContext] = []

        for module in project.modules:
            import_lines = [imp.display() for imp in module.imports] if config.include_imports else []
            module_source = _module_light_body(module) if config.include_source_body else ""

            module_id = make_entity_id(module.path, "module", "module")
            contexts.append(
                EntityContext(
                    entity_type="module",
                    entity_name=module.path,
                    entity_id=module_id,
                    module_path=module.path,
                    project_name=project.name,
                    signature="",
                    source_docstring=module.docstring,
                    source_body=module_source,
                    imports=import_lines,
                    readme_excerpt=readme_excerpt,
                    previous_output_doc=previous_docs.get(module_id),
                    output_language=output_language,
                    module=module,
                )
            )

            for cls in module.classes:
                class_id = make_entity_id(module.path, "class", cls.name)
                contexts.append(
                    EntityContext(
                        entity_type="class",
                        entity_name=cls.name,
                        entity_id=class_id,
                        module_path=module.path,
                        project_name=project.name,
                        signature=_class_signature(cls),
                        source_docstring=cls.docstring,
                        source_body="",
                        imports=import_lines,
                        readme_excerpt=readme_excerpt,
                        previous_output_doc=previous_docs.get(class_id),
                        output_language=output_language,
                        class_model=cls,
                        module=module,
                    )
                )
                for method in cls.methods:
                    method_id = make_entity_id(module.path, "method", method.qualified_name())
                    contexts.append(
                        EntityContext(
                            entity_type="method",
                            entity_name=method.qualified_name(),
                            entity_id=method_id,
                            module_path=module.path,
                            project_name=project.name,
                            signature=method.signature(),
                            source_docstring=method.docstring,
                            source_body=method.source_body if config.include_source_body else method.source_snippet,
                            imports=import_lines,
                            readme_excerpt=readme_excerpt,
                            previous_output_doc=previous_docs.get(method_id),
                            output_language=output_language,
                            complexity=method.complexity,
                            function=method,
                            class_model=cls,
                            module=module,
                        )
                    )

            for fn in module.functions:
                fn_id = make_entity_id(module.path, "function", fn.name)
                contexts.append(
                    EntityContext(
                        entity_type="function",
                        entity_name=fn.name,
                        entity_id=fn_id,
                        module_path=module.path,
                        project_name=project.name,
                        signature=fn.signature(),
                        source_docstring=fn.docstring,
                        source_body=fn.source_body if config.include_source_body else fn.source_snippet,
                        imports=import_lines,
                        readme_excerpt=readme_excerpt,
                        previous_output_doc=previous_docs.get(fn_id),
                        output_language=output_language,
                        complexity=fn.complexity,
                        function=fn,
                        module=module,
                    )
                )

        return contexts

    def attach_callee_docs(
        self,
        ctx: EntityContext,
        docs_by_id: dict[str, str],
        callee_ids: list[str],
        unresolved: list[str],
    ) -> None:
        del docs_by_id
        self.attach_callee_briefs(ctx, DocBriefRegistry(), callee_ids, unresolved)

    def attach_callee_briefs(
        self,
        ctx: EntityContext,
        registry: DocBriefRegistry,
        callee_ids: list[str],
        unresolved: list[str],
    ) -> None:
        ctx.called_entities_docs = [
            CalledEntityDoc(
                name=cid.split("::")[-1],
                content=registry.brief_line(cid),
            )
            for cid in callee_ids
            if registry.has(cid)
        ]
        ctx.unresolved_calls = unresolved

    def attach_class_method_briefs(
        self,
        ctx: EntityContext,
        registry: DocBriefRegistry,
    ) -> None:
        if ctx.entity_type != "class" or not ctx.class_model:
            return
        ctx.class_member_docs = []
        for method in ctx.class_model.methods:
            method_id = make_entity_id(ctx.module_path, "method", method.qualified_name())
            ctx.class_member_docs.append(
                CalledEntityDoc(
                    name=method.name,
                    content=registry.brief_line(method_id, method.signature()),
                )
            )

    def attach_module_dependency_briefs(
        self,
        ctx: EntityContext,
        registry: DocBriefRegistry,
        call_graph: CallGraph,
    ) -> None:
        if ctx.entity_type != "module" or not ctx.module:
            return
        deps = call_graph.module_dependencies.get(ctx.module.path, [])
        ctx.module_dependency_docs = [
            CalledEntityDoc(
                name=dep_path,
                content=registry.brief_line(
                    make_entity_id(dep_path, "module", "module"),
                    dep_path,
                ),
            )
            for dep_path in deps
        ]
        ctx.module_export_docs = []
        export_names = ctx.module.exports or [
            fn.name for fn in ctx.module.functions
        ] + [cls.name for cls in ctx.module.classes]
        seen: set[str] = set()
        for name in export_names:
            if name in seen:
                continue
            seen.add(name)
            for entity_type in ("class", "function"):
                entity_id = make_entity_id(ctx.module.path, entity_type, name)
                if registry.has(entity_id):
                    ctx.module_export_docs.append(
                        CalledEntityDoc(name=name, content=registry.brief_line(entity_id))
                    )
                    break

    def attach_base_class_briefs(
        self,
        ctx: EntityContext,
        registry: DocBriefRegistry,
    ) -> None:
        if ctx.entity_type != "method" or not ctx.class_model:
            return
        ctx.base_class_docs = []
        module = ctx.module
        if module is None:
            return
        for base in ctx.class_model.bases:
            base_name = base.split("[", 1)[0].strip()
            if base_name in ("object", "Generic", "TypedDict", "NamedTuple", "Protocol"):
                continue
            for cls in module.classes:
                if cls.name == base_name:
                    class_id = make_entity_id(ctx.module_path, "class", cls.name)
                    ctx.base_class_docs.append(
                        CalledEntityDoc(
                            name=base_name,
                            content=registry.brief_line(class_id, _class_signature(cls)),
                        )
                    )
                    break

    def attach_related_briefs(
        self,
        ctx: EntityContext,
        registry: DocBriefRegistry,
        callee_ids: list[str],
        unresolved: list[str],
        call_graph: CallGraph,
    ) -> None:
        self.attach_callee_briefs(ctx, registry, callee_ids, unresolved)
        self.attach_class_method_briefs(ctx, registry)
        self.attach_module_dependency_briefs(ctx, registry, call_graph)
        self.attach_base_class_briefs(ctx, registry)


def _class_signature(cls) -> str:
    if cls.bases:
        return f"class {cls.name}({', '.join(cls.bases)})"
    return f"class {cls.name}"


def _module_light_body(module) -> str:
    lines: list[str] = []
    if module.exports:
        lines.append(f"__all__ = {module.exports!r}")
    top_level = [fn.name for fn in module.functions] + [cls.name for cls in module.classes]
    if top_level:
        lines.append("Top-level names: " + ", ".join(top_level))
    return "\n".join(lines)
