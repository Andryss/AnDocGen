from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Literal


class IssueLevel(str, Enum):
    WARNING = "warning"
    ERROR = "error"


class IssueCategory(str, Enum):
    PARSE = "parse"
    GENERATION = "generation"
    VALIDATION = "validation"


@dataclass
class ParameterModel:
    name: str
    type_annotation: str | None = None
    default: str | None = None


@dataclass
class FunctionModel:
    name: str
    parameters: list[ParameterModel] = field(default_factory=list)
    returns: str | None = None
    docstring: str | None = None
    calls: list[str] = field(default_factory=list)
    line_start: int = 0
    line_end: int = 0
    is_method: bool = False
    owner_class: str | None = None
    source_body: str = ""
    source_snippet: str = ""
    complexity: int = 1
    decorators: list[str] = field(default_factory=list)

    def signature(self) -> str:
        prefix = "def "
        if "staticmethod" in self.decorators:
            prefix = "@staticmethod\n" + prefix
        elif "classmethod" in self.decorators:
            prefix = "@classmethod\n" + prefix
        params = ", ".join(
            self._format_param(p) for p in self.parameters if p.name not in ("self", "cls")
        )
        ret = f" -> {self.returns}" if self.returns else ""
        return f"{prefix}{self.name}({params}){ret}"

    def qualified_name(self) -> str:
        if self.owner_class:
            return f"{self.owner_class}.{self.name}"
        return self.name

    @staticmethod
    def _format_param(p: ParameterModel) -> str:
        parts = [p.name]
        if p.type_annotation:
            parts[0] = f"{p.name}: {p.type_annotation}"
        if p.default is not None:
            parts.append(f" = {p.default}")
        return "".join(parts)


@dataclass
class ClassModel:
    name: str
    bases: list[str] = field(default_factory=list)
    docstring: str | None = None
    fields: list[str] = field(default_factory=list)
    methods: list[FunctionModel] = field(default_factory=list)
    line_start: int = 0
    line_end: int = 0
    source_body: str = ""
    source_snippet: str = ""


@dataclass
class ImportModel:
    module: str
    names: list[str] = field(default_factory=list)
    level: int = 0

    def display(self) -> str:
        prefix = "." * self.level
        if self.names:
            return f"from {prefix}{self.module} import {', '.join(self.names)}"
        return f"import {prefix}{self.module}"


@dataclass
class ModuleModel:
    path: str
    docstring: str | None = None
    imports: list[ImportModel] = field(default_factory=list)
    functions: list[FunctionModel] = field(default_factory=list)
    classes: list[ClassModel] = field(default_factory=list)
    source: str = ""
    content_hash: str = ""


@dataclass
class CallGraphNode:
    id: str
    module: str
    name: str
    kind: Literal["function", "method"]
    class_name: str | None = None


@dataclass
class CallGraphEdge:
    caller_id: str
    callee_name: str
    callee_id: str | None = None


@dataclass
class CallGraph:
    nodes: list[CallGraphNode] = field(default_factory=list)
    edges: list[CallGraphEdge] = field(default_factory=list)
    module_dependencies: dict[str, list[str]] = field(default_factory=dict)


@dataclass
class ProjectModel:
    project_path: str
    modules: list[ModuleModel] = field(default_factory=list)
    call_graph: CallGraph = field(default_factory=CallGraph)
    project_name: str = ""
    project_description: str = ""

    @property
    def name(self) -> str:
        if self.project_name:
            return self.project_name
        from pathlib import Path

        return Path(self.project_path).name


EntityType = Literal["function", "class", "module", "method"]


@dataclass
class CalledEntityDoc:
    name: str
    content: str


@dataclass
class EntityContext:
    entity_type: EntityType
    entity_name: str
    module_path: str
    project_name: str
    entity_id: str = ""
    signature: str = ""
    source_docstring: str | None = None
    source_body: str = ""
    imports: list[str] = field(default_factory=list)
    called_entities_docs: list[CalledEntityDoc] = field(default_factory=list)
    base_class_docs: list[CalledEntityDoc] = field(default_factory=list)
    readme_excerpt: str | None = None
    previous_output_doc: str | None = None
    output_language: str = "ru"
    complexity: int | None = None
    unresolved_calls: list[str] = field(default_factory=list)
    function: FunctionModel | None = None
    class_model: ClassModel | None = None
    module: ModuleModel | None = None


@dataclass
class ParameterDoc:
    name: str
    type: str
    description: str
    optional: bool = False
    default: str | None = None


@dataclass
class ReturnDoc:
    type: str
    description: str


@dataclass
class ExportDoc:
    name: str
    type: str | None = None
    description: str = ""


@dataclass
class DocBlock:
    entity_type: EntityType
    entity_name: str
    module_path: str
    signature: str = ""
    raw_response: str = ""
    summary: str = ""
    content: str = ""
    parameters: list[ParameterDoc] | None = None
    returns: ReturnDoc | None = None
    raises: str | None = None
    edge_cases: str | None = None
    side_effects: str | None = None
    examples: str | None = None
    see_also: str | None = None
    fields: list[ParameterDoc] | None = None
    inheritance: str | None = None
    methods_overview: str | None = None
    exports: list[ExportDoc] | None = None


@dataclass
class ParseError:
    module_path: str
    message: str


@dataclass
class GenerationError:
    module_path: str
    entity_type: EntityType | None
    entity_name: str | None
    message: str


@dataclass
class ValidationIssue:
    level: IssueLevel
    category: IssueCategory
    message: str
    module_path: str
    entity_type: EntityType | None = None
    entity_name: str | None = None


@dataclass
class PipelineResult:
    processed_files: list[str] = field(default_factory=list)
    skipped_files: list[str] = field(default_factory=list)
    output_files: list[str] = field(default_factory=list)
    parse_errors: list[ParseError] = field(default_factory=list)
    generation_errors: list[GenerationError] = field(default_factory=list)
    issues: list[ValidationIssue] = field(default_factory=list)
    elapsed_seconds: float = 0.0
    summary_log_path: str | None = None
    detail_log_path: str | None = None
    trace_log_path: str | None = None

    @property
    def warnings(self) -> list[ValidationIssue]:
        return [i for i in self.issues if i.level == IssueLevel.WARNING]

    @property
    def errors(self) -> list[ValidationIssue]:
        return [i for i in self.issues if i.level == IssueLevel.ERROR]

    @property
    def has_fatal_errors(self) -> bool:
        return bool(self.parse_errors or self.generation_errors)


def make_entity_id(module_path: str, entity_type: EntityType, entity_name: str) -> str:
    return f"{module_path}::{entity_name}"
