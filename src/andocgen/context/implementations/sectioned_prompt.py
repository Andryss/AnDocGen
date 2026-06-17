from __future__ import annotations

from andocgen.models.entities import EntityContext

_FUNCTION_SECTIONS = (
    "Summary",
    "Parameters",
    "Returns",
    "Raises",
    "Edge cases",
    "Side effects",
    "Examples",
    "See also",
)
_CLASS_SECTIONS = ("Summary", "Fields", "Inheritance", "Methods overview")
_MODULE_SECTIONS = ("Summary", "Exports")

_FUNCTION_EXAMPLE = """## Summary

Складывает два числа и возвращает результат.

## Parameters

- `a` (`float`) — первое слагаемое
- `b` (`float`) — второе слагаемое

## Returns

- `float` — сумма a и b

## Raises

N/A

## Edge cases

N/A

## Side effects

N/A

## Examples

N/A

## See also

N/A"""

_CLASS_EXAMPLE = """## Summary

Класс для базовых арифметических операций.

## Fields

- `precision` (`int`) — количество знаков после запятой

## Inheritance

N/A

## Methods overview

N/A"""

_MODULE_EXAMPLE = """## Summary

Модуль калькулятора с базовыми операциями.

## Exports

N/A"""


class SectionedPromptBuilder:
    def build_system_message(self, output_language: str, entity_type: str) -> str:
        lang_label = "Russian" if output_language == "ru" else output_language
        sections, example = self._sections_and_example(entity_type)
        section_headers = "\n".join(f"## {s}" for s in sections)

        return f"""You are a technical documentation generator.

<task>
Document the entity from the user message. Write all section body text in {lang_label}.
</task>

<output_contract>
Return Markdown with EXACTLY these section headers in this order — no more, no less:

{section_headers}

Rules (mandatory):
1. Output ONLY the sections above. No preamble, no postscript, no commentary outside sections.
2. Do not wrap the response in code fences.
3. All section body text MUST be in {lang_label}. Do not mix languages.
4. If a section is not relevant, write exactly N/A as the entire section body on a single line.
   Do NOT add explanations, bullet points, markdown, or any other text to N/A sections.
   Wrong: "N/A — no exceptions raised". Wrong: "**N/A**". Correct: N/A
5. Parameters section: one line per parameter, exact format:
   - `name` (`type`) — description
   If there are no parameters, write N/A.
   For variadic signatures use `*args` and/or `**kwargs` as parameter names.
6. Returns section: exactly one line in format:
   - `type` — description
   If there is no return value, write N/A.
7. Fields and Exports sections use the same list format as Parameters when applicable.
   For Exports, describe only names listed in `__all__` when provided; descriptions in {lang_label}.
8. Base documentation only on the provided source code. Do not invent parameters, types, or behavior.
9. Examples must use valid calls matching the signature (required arguments must be present).
</output_contract>

<example>
{example}
</example>

Your response must follow the example structure exactly and nothing else."""

    def build_user_message(self, ctx: EntityContext, max_chars: int) -> str:
        sections: list[tuple[str, str]] = []

        entity_lines = [
            f"Type: {ctx.entity_type}",
            f"Name: {ctx.entity_name}",
            f"Module: {ctx.module_path}",
        ]
        if ctx.signature:
            entity_lines.append(f"Signature: {ctx.signature}")
        if ctx.complexity is not None:
            entity_lines.append(f"Cyclomatic complexity: {ctx.complexity}")
        sections.append(("Entity", "\n".join(entity_lines)))

        source_parts = []
        if ctx.source_docstring:
            source_parts.append(f"Docstring:\n{ctx.source_docstring}")
        if ctx.source_body:
            source_parts.append(f"Source body:\n```python\n{ctx.source_body}\n```")
        sections.append(("Source", "\n".join(source_parts) or "(none)"))

        if ctx.previous_output_doc:
            sections.append(("Previous output", ctx.previous_output_doc))

        if ctx.imports:
            sections.append(("Dependencies", "\n".join(ctx.imports)))

        if ctx.called_entities_docs:
            called = "\n\n".join(f"### {d.name}\n{d.content}" for d in ctx.called_entities_docs)
            sections.append(("Called entities", called))

        if ctx.readme_excerpt:
            sections.append(("Project", f"Name: {ctx.project_name}\nREADME excerpt:\n{ctx.readme_excerpt}"))

        return _truncate_sections(sections, max_chars)

    @staticmethod
    def _sections_and_example(entity_type: str) -> tuple[tuple[str, ...], str]:
        if entity_type in ("function", "method"):
            return _FUNCTION_SECTIONS, _FUNCTION_EXAMPLE
        if entity_type == "class":
            return _CLASS_SECTIONS, _CLASS_EXAMPLE
        return _MODULE_SECTIONS, _MODULE_EXAMPLE


def _truncate_sections(sections: list[tuple[str, str]], max_chars: int) -> str:
    protected = {"Entity", "Source"}
    rendered = [f"## {title}\n\n{body}" for title, body in sections]
    full = "\n\n".join(rendered)
    if len(full) <= max_chars:
        return full

    result_sections = list(sections)
    for idx in range(len(result_sections) - 1, -1, -1):
        title, _ = result_sections[idx]
        if title in protected:
            continue
        result_sections[idx] = (title, "(truncated)")
        rendered = [f"## {t}\n\n{b}" for t, b in result_sections]
        full = "\n\n".join(rendered)
        if len(full) <= max_chars:
            return full

    return full[:max_chars]
