from __future__ import annotations

from andocgen.config import ContextConfig
from andocgen.models.entities import (
    CalledEntityDoc,
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
            source_body = module.source if config.include_source_body else ""

            module_id = make_entity_id(module.path, "module", module.path)
            contexts.append(
                EntityContext(
                    entity_type="module",
                    entity_name=module.path,
                    entity_id=module_id,
                    module_path=module.path,
                    project_name=project.name,
                    signature="",
                    source_docstring=module.docstring,
                    source_body=source_body,
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
                        signature=f"class {cls.name}({', '.join(cls.bases) or 'object'})",
                        source_docstring=cls.docstring,
                        source_body=cls.source_body if config.include_source_body else cls.source_snippet,
                        imports=import_lines,
                        readme_excerpt=readme_excerpt,
                        previous_output_doc=previous_docs.get(class_id),
                        output_language=output_language,
                        class_model=cls,
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
        ctx.called_entities_docs = [
            CalledEntityDoc(name=cid.split("::")[-1], content=docs_by_id[cid])
            for cid in callee_ids
            if cid in docs_by_id
        ]
        ctx.unresolved_calls = unresolved
