from __future__ import annotations

from andocgen.models.entities import DocBlock, EntityContext, ExportDoc, ParameterDoc, ReturnDoc


def build_fallback_block(ctx: EntityContext, raw_response: str = "", reason: str = "exhausted retries") -> DocBlock:
    block = DocBlock(
        entity_type=ctx.entity_type,
        entity_name=ctx.entity_name,
        module_path=ctx.module_path,
        signature=ctx.signature,
        raw_response=raw_response.strip(),
        summary=_summary(ctx),
        fallback=True,
        fallback_reason=reason,
    )

    if ctx.entity_type in ("function", "method") and ctx.function:
        block.parameters = [
            ParameterDoc(
                name=param.name,
                type=param.type_annotation or "",
                description="",
                default=param.default,
                optional=param.default is not None,
            )
            for param in ctx.function.parameters
            if param.name not in ("self", "cls")
        ]
        if ctx.function.returns and ctx.function.returns not in ("None", "NoneType"):
            block.returns = ReturnDoc(type=ctx.function.returns, description="")
        block.raises = "N/A"
        block.edge_cases = "N/A"
        block.side_effects = "N/A"
        block.examples = []
        block.see_also = "N/A"
    elif ctx.entity_type == "class" and ctx.class_model:
        block.purpose = f"Класс `{ctx.entity_name}` описан по структуре исходного кода."
        block.usage_notes = "Используйте публичные методы и поля класса согласно их сигнатурам."
        block.fields = [
            ParameterDoc(
                name=field.name,
                type=field.type_annotation or "",
                description="",
                default=field.default,
                optional=field.default is not None,
            )
            for field in ctx.class_model.field_defs
        ]
        bases = [
            base
            for base in ctx.class_model.bases
            if base.split("[", 1)[0].strip() not in {"object", "Generic", "TypedDict", "NamedTuple", "Protocol"}
        ]
        block.inheritance = "\n".join(f"- `{base}`" for base in bases) if bases else "N/A"
        block.methods_overview = (
            "\n".join(f"- `{method.name}`" for method in ctx.class_model.methods)
            if ctx.class_model.methods
            else "N/A"
        )
    elif ctx.entity_type == "module" and ctx.module:
        export_names = ctx.module.exports or [fn.name for fn in ctx.module.functions] + [
            cls.name for cls in ctx.module.classes
        ]
        block.exports = [
            ExportDoc(name=name, type=None, description="")
            for name in export_names
        ]

    return block


def _summary(ctx: EntityContext) -> str:
    if ctx.source_docstring and ctx.source_docstring.strip():
        return ctx.source_docstring.strip()
    if ctx.entity_type == "module":
        return f"Модуль `{ctx.entity_name}`."
    if ctx.entity_type == "class":
        return f"Класс `{ctx.entity_name}`."
    return f"Сущность `{ctx.entity_name}` описана по сигнатуре и структуре исходного кода."
