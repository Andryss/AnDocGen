from __future__ import annotations

import ast
from pathlib import Path

from andocgen.models.entities import (
    ClassModel,
    FunctionModel,
    ImportModel,
    ModuleModel,
    ParameterModel,
)
from andocgen.parser.base import ParseResult
from andocgen.scanner.implementations.filesystem import FilesystemScanner


class PythonAstParser:
    def __init__(self) -> None:
        self._hasher = FilesystemScanner()

    def parse(self, file_path: Path, project_root: Path) -> ParseResult:
        rel_path = str(file_path.relative_to(project_root))
        try:
            source = file_path.read_text(encoding="utf-8")
            tree = ast.parse(source, filename=str(file_path))
        except SyntaxError as exc:
            return ParseResult(error=f"Syntax error at line {exc.lineno}: {exc.msg}")

        visitor = _ModuleVisitor(source, rel_path)
        visitor.visit(tree)
        return ParseResult(
            module=ModuleModel(
                path=rel_path,
                docstring=ast.get_docstring(tree),
                imports=visitor.imports,
                functions=visitor.functions,
                classes=visitor.classes,
                exports=visitor.exports,
                source=source,
                content_hash=self._hasher.file_hash(file_path),
            )
        )


class _ModuleVisitor(ast.NodeVisitor):
    def __init__(self, source: str, rel_path: str) -> None:
        self._lines = source.splitlines()
        self._rel_path = rel_path
        self.imports: list[ImportModel] = []
        self.functions: list[FunctionModel] = []
        self.classes: list[ClassModel] = []
        self.exports: list[str] = []

    def visit_Module(self, node: ast.Module) -> None:
        for item in node.body:
            if isinstance(item, (ast.Import, ast.ImportFrom)):
                self.visit(item)
            elif isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                self.functions.append(self._parse_function(item))
            elif isinstance(item, ast.ClassDef):
                self._parse_class(item)
            elif isinstance(item, ast.Assign):
                self._maybe_collect_all(item)

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            self.imports.append(
                ImportModel(module=alias.name, names=[alias.asname or alias.name])
            )

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        module = node.module or ""
        names = [a.name for a in node.names]
        self.imports.append(ImportModel(module=module, names=names, level=node.level))

    def _maybe_collect_all(self, node: ast.Assign) -> None:
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == "__all__":
                if isinstance(node.value, (ast.List, ast.Tuple)):
                    for elt in node.value.elts:
                        if isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                            self.exports.append(elt.value)

    def _parse_class(self, node: ast.ClassDef) -> None:
        methods: list[FunctionModel] = []
        fields: list[str] = []
        field_defs: list[ParameterModel] = []
        is_dataclass = _is_dataclass(node)
        is_namedtuple = _is_namedtuple(node)
        for item in node.body:
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                method = self._parse_function(item, is_method=True, owner_class=node.name)
                methods.append(method)
            elif isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                name = item.target.id
                fields.append(name)
                default = self._expr_to_str(item.value) if item.value else None
                field_defs.append(
                    ParameterModel(
                        name=name,
                        type_annotation=(
                            self._expr_to_str(item.annotation) if item.annotation else None
                        ),
                        default=default,
                    )
                )
            elif isinstance(item, ast.Assign):
                for target in item.targets:
                    if isinstance(target, ast.Name):
                        fields.append(target.id)

        end = node.end_lineno or node.lineno
        self.classes.append(
            ClassModel(
                name=node.name,
                bases=[self._expr_to_str(b) for b in node.bases],
                docstring=ast.get_docstring(node),
                fields=fields,
                field_defs=field_defs,
                is_dataclass=is_dataclass,
                is_namedtuple=is_namedtuple,
                methods=methods,
                line_start=node.lineno,
                line_end=end,
                source_body=self._body(node),
                source_snippet=self._snippet(node.lineno, end),
            )
        )

    def _parse_function(
        self,
        node: ast.FunctionDef | ast.AsyncFunctionDef,
        is_method: bool = False,
        owner_class: str | None = None,
    ) -> FunctionModel:
        params = self._parse_args(node.args)
        calls = _extract_calls(node)
        end = node.end_lineno or node.lineno
        decorators = _extract_decorators(node)
        return FunctionModel(
            name=node.name,
            parameters=params,
            returns=self._expr_to_str(node.returns) if node.returns else None,
            docstring=ast.get_docstring(node),
            calls=calls,
            line_start=node.lineno,
            line_end=end,
            is_method=is_method,
            owner_class=owner_class,
            source_body=self._body(node),
            source_snippet=self._snippet(node.lineno, end),
            complexity=_cyclomatic_complexity(node),
            decorators=decorators,
        )

    def _parse_args(self, args: ast.arguments) -> list[ParameterModel]:
        params: list[ParameterModel] = []
        defaults_offset = len(args.args) - len(args.defaults)

        for i, arg in enumerate(args.args):
            default = None
            if i >= defaults_offset:
                default_node = args.defaults[i - defaults_offset]
                default = self._expr_to_str(default_node)
            ann = self._expr_to_str(arg.annotation) if arg.annotation else None
            params.append(ParameterModel(name=arg.arg, type_annotation=ann, default=default))

        if args.vararg:
            params.append(
                ParameterModel(
                    name=f"*{args.vararg.arg}",
                    type_annotation=(
                        self._expr_to_str(args.vararg.annotation)
                        if args.vararg.annotation
                        else None
                    ),
                )
            )
        if args.kwarg:
            params.append(
                ParameterModel(
                    name=f"**{args.kwarg.arg}",
                    type_annotation=(
                        self._expr_to_str(args.kwarg.annotation)
                        if args.kwarg.annotation
                        else None
                    ),
                )
            )
        return params

    def _snippet(self, start: int, end: int) -> str:
        return "\n".join(self._lines[start - 1 : end])

    def _body(self, node: ast.AST) -> str:
        if not hasattr(node, "body"):
            return self._snippet(getattr(node, "lineno", 1), getattr(node, "end_lineno", 1))
        if not node.body:
            return ""
        start = node.body[0].lineno
        end = node.body[-1].end_lineno or node.body[-1].lineno
        return self._snippet(start, end)

    @staticmethod
    def _expr_to_str(node: ast.expr | None) -> str:
        if node is None:
            return ""
        try:
            return ast.unparse(node)
        except Exception:
            return type(node).__name__


def _extract_decorators(node: ast.FunctionDef | ast.AsyncFunctionDef) -> list[str]:
    decorators: list[str] = []
    for dec in node.decorator_list:
        if isinstance(dec, ast.Name):
            decorators.append(dec.id)
        elif isinstance(dec, ast.Attribute):
            decorators.append(dec.attr)
        else:
            try:
                decorators.append(ast.unparse(dec))
            except Exception:
                decorators.append("unknown")
    return decorators


def _is_namedtuple(node: ast.ClassDef) -> bool:
    for base in node.bases:
        name = _base_name(base)
        if name == "NamedTuple":
            return True
    return False


def _base_name(node: ast.expr) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    if isinstance(node, ast.Subscript):
        return _base_name(node.value)
    return ""


def _is_dataclass(node: ast.ClassDef) -> bool:
    for decorator in node.decorator_list:
        if isinstance(decorator, ast.Name) and decorator.id == "dataclass":
            return True
        if isinstance(decorator, ast.Attribute) and decorator.attr == "dataclass":
            return True
        if isinstance(decorator, ast.Call):
            func = decorator.func
            if isinstance(func, ast.Name) and func.id == "dataclass":
                return True
            if isinstance(func, ast.Attribute) and func.attr == "dataclass":
                return True
    return False


def _cyclomatic_complexity(node: ast.AST) -> int:
    complexity = 1
    for child in ast.walk(node):
        if isinstance(child, (ast.If, ast.For, ast.AsyncFor, ast.While, ast.ExceptHandler)):
            complexity += 1
        elif isinstance(child, ast.BoolOp):
            complexity += max(0, len(child.values) - 1)
        elif isinstance(child, (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)):
            complexity += 1
    return complexity


def _extract_calls(node: ast.AST) -> list[str]:
    calls: list[str] = []
    for child in ast.walk(node):
        if isinstance(child, ast.Call):
            name = _call_name(child.func)
            if name:
                calls.append(name)
    return sorted(set(calls))


def _call_name(node: ast.expr) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        value = _call_name(node.value) if not isinstance(node.value, ast.Name) else node.value.id
        if value:
            return f"{value}.{node.attr}"
        return node.attr
    return ""
