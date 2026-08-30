from __future__ import annotations

from andocgen.config import ValidationConfig
from andocgen.models.entities import (
    DocBlock,
    EntityContext,
    IssueCategory,
    IssueLevel,
    ValidationIssue,
)
from andocgen.validation.rules.entity_rules import validate_entity_examples
from andocgen.validation.rules.semantic_rules import (
    validate_semantic_consistency,
    validate_text_language,
)
from andocgen.validation.rules.text_quality import mostly_latin


class StructuredValidator:
    def validate(
        self,
        blocks: list[DocBlock],
        contexts: list[EntityContext],
        config: ValidationConfig,
    ) -> list[ValidationIssue]:
        context_map = {(c.module_path, c.entity_type, c.entity_name): c for c in contexts}
        issues: list[ValidationIssue] = []

        for block in blocks:
            ctx = context_map.get((block.module_path, block.entity_type, block.entity_name))
            if ctx is None:
                continue

            if block.entity_type in ("function", "method") and ctx.function:
                issues.extend(self._validate_function(block, ctx, config))
                if config.check_consistency:
                    issues.extend(_rule_warnings(block, validate_semantic_consistency(block, ctx)))

            if config.check_text_quality:
                if not block.summary.strip():
                    issues.append(self._warning(block, "Summary is empty"))
                elif len(block.summary.strip()) < (config.min_summary_length or 10):
                    issues.append(self._warning(block, "Summary appears too short"))
                elif ctx.output_language == "ru" and mostly_latin(block.summary):
                    issues.append(
                        self._warning(
                            block,
                            "Summary appears to be in a different language than configured (ru)",
                        )
                    )
                issues.extend(_rule_warnings(block, validate_text_language(block, ctx)))

            if config.check_representation and block.summary:
                if block.summary not in block.content:
                    issues.append(
                        self._warning(block, "Rendered content does not include summary text")
                    )

        return issues

    def _validate_function(
        self, block: DocBlock, ctx: EntityContext, config: ValidationConfig
    ) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        fn = ctx.function
        if fn is None:
            return issues

        param_names = [p.name for p in fn.parameters if p.name not in ("self", "cls")]
        documented = {p.name for p in (block.parameters or [])}

        if config.check_completeness:
            for param in param_names:
                if param in documented:
                    continue
                clean = param.lstrip("*")
                if param.startswith("*") and _variadic_documented(documented):
                    continue
                if clean and clean not in documented:
                    issues.append(self._warning(block, f"Parameter `{clean}` is not documented"))

            if fn.returns and fn.returns not in ("None", "NoneType"):
                if not block.returns or not (block.returns.type or block.returns.description):
                    issues.append(self._warning(block, "Return value is not described"))

        if config.check_consistency and block.parameters:
            for doc_param in block.parameters:
                if doc_param.name not in param_names and not doc_param.name.startswith("*"):
                    issues.append(
                        ValidationIssue(
                            level=IssueLevel.ERROR,
                            category=IssueCategory.VALIDATION,
                            message=f"Documentation mentions non-existent parameter `{doc_param.name}`",
                            module_path=block.module_path,
                            entity_type=block.entity_type,
                            entity_name=block.entity_name,
                        )
                    )

        if config.check_representation and block.parameters:
            for doc_param in block.parameters:
                if f"`{doc_param.name}`" not in block.content:
                    issues.append(
                        self._warning(block, f"Rendered content missing parameter `{doc_param.name}`")
                    )

        if config.check_text_quality:
            issues.extend(_example_warnings(block, ctx))

        if (
            config.check_text_quality
            and ctx.complexity
            and ctx.complexity >= (config.complexity_warning_threshold or 20)
        ):
            issues.append(
                self._warning(block, f"High cyclomatic complexity ({ctx.complexity})")
            )

        return issues

    @staticmethod
    def _warning(block: DocBlock, message: str) -> ValidationIssue:
        return ValidationIssue(
            level=IssueLevel.WARNING,
            category=IssueCategory.VALIDATION,
            message=message,
            module_path=block.module_path,
            entity_type=block.entity_type,
            entity_name=block.entity_name,
        )


def _variadic_documented(documented: set[str]) -> bool:
    return any(name.startswith("*") or name in ("args", "kwargs") for name in documented)


def _example_warnings(block: DocBlock, ctx: EntityContext) -> list[ValidationIssue]:
    return [
        ValidationIssue(
            level=IssueLevel.WARNING,
            category=IssueCategory.VALIDATION,
            message=issue.message,
            module_path=block.module_path,
            entity_type=block.entity_type,
            entity_name=block.entity_name,
        )
        for issue in validate_entity_examples(block, ctx)
        if issue.code.startswith("examples_")
    ]


def _rule_warnings(block: DocBlock, issues) -> list[ValidationIssue]:
    return [
        ValidationIssue(
            level=IssueLevel.WARNING,
            category=IssueCategory.VALIDATION,
            message=issue.message,
            module_path=block.module_path,
            entity_type=block.entity_type,
            entity_name=block.entity_name,
        )
        for issue in issues
    ]
