from __future__ import annotations

from andocgen.generator.formatter import is_empty_section
from andocgen.models.entities import (
    DocBlock,
    EntityContext,
    ExportDoc,
    ParameterDoc,
    ReturnDoc,
)

_NOISE_BASES = {"object", "Generic", "TypedDict", "NamedTuple", "Protocol"}


class BlockEnricher:
    def enrich(self, block: DocBlock, ctx: EntityContext) -> None:
        if ctx.entity_type in ("function", "method"):
            self.enrich_parameters(block, ctx)
        elif ctx.entity_type == "class":
            self.enrich_class_fields(block, ctx)
            block.inheritance = self.enrich_inheritance(block.inheritance or "", ctx)
            block.methods_overview = self.enrich_methods_overview(block.methods_overview or "", ctx)
        elif ctx.entity_type == "module":
            self.enrich_exports(block, ctx)

    def enrich_exports(self, block: DocBlock, ctx: EntityContext) -> None:
        llm_exports = {export.name: export for export in (block.exports or [])}
        if not ctx.module or not ctx.module.exports:
            block.exports = []
            return
        block.exports = [
            ExportDoc(
                name=name,
                type=llm_exports[name].type if name in llm_exports else "",
                description=llm_exports[name].description if name in llm_exports else "",
            )
            for name in ctx.module.exports
        ]

    def enrich_parameters(self, block: DocBlock, ctx: EntityContext) -> None:
        if not ctx.function:
            return
        fn = ctx.function
        documented = {p.name for p in (block.parameters or [])}

        if not block.parameters:
            block.parameters = []

        for param in fn.parameters:
            if param.name in ("self", "cls"):
                continue
            if param.name not in documented:
                block.parameters.append(
                    ParameterDoc(
                        name=param.name,
                        type=param.type_annotation or "",
                        description="",
                    )
                )
                documented.add(param.name)

        if not block.returns and fn.returns and fn.returns not in ("None", "NoneType"):
            block.returns = ReturnDoc(type=fn.returns, description="")

        allowed = {p.name for p in fn.parameters if p.name not in ("self", "cls")}
        block.parameters = [p for p in block.parameters if p.name in allowed]

    def enrich_class_fields(self, block: DocBlock, ctx: EntityContext) -> None:
        if not ctx.class_model:
            block.fields = []
            return
        cls = ctx.class_model
        structured = cls.is_dataclass or cls.is_namedtuple
        if structured and cls.field_defs:
            llm_fields = {field.name: field for field in (block.fields or [])}
            block.fields = [
                ParameterDoc(
                    name=field.name,
                    type=field.type_annotation or "",
                    description=llm_fields.get(field.name, ParameterDoc("", "", "")).description,
                )
                for field in cls.field_defs
            ]
        elif cls.field_defs:
            block.fields = [
                ParameterDoc(
                    name=field.name,
                    type=field.type_annotation or "",
                    description="",
                )
                for field in cls.field_defs
            ]
        else:
            block.fields = []

    def enrich_inheritance(self, section: str, ctx: EntityContext) -> str:
        if not is_empty_section(section):
            normalized = self.normalize_inheritance(section)
            if normalized != "N/A":
                return normalized
        if not ctx.class_model or not ctx.class_model.bases:
            return "N/A"
        bases = [
            base
            for base in ctx.class_model.bases
            if base.split("[", 1)[0].strip() not in _NOISE_BASES
        ]
        if not bases:
            return "N/A"
        return "\n".join(f"- `{base}`" for base in bases)

    def enrich_methods_overview(self, section: str, ctx: EntityContext) -> str:
        if not is_empty_section(section):
            return section
        if ctx.class_member_docs:
            return "\n".join(doc.content for doc in ctx.class_member_docs)
        if not ctx.class_model:
            return "N/A"
        lines = [f"- `{method.name}`" for method in ctx.class_model.methods]
        return "\n".join(lines) if lines else "N/A"

    @staticmethod
    def normalize_inheritance(section: str) -> str:
        text = section.strip()
        if is_empty_section(text):
            return "N/A"
        stripped = text.strip().strip("`- ")
        if stripped.lower() in ("object", "object —", "- object"):
            return "N/A"
        if stripped.startswith("object") and len(stripped.split()) <= 2:
            return "N/A"
        return text
