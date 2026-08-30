from __future__ import annotations

from andocgen.config import ValidationConfig
from andocgen.models.entities import (
    DocBlock,
    EntityContext,
    ExampleDoc,
    FunctionModel,
    ParameterDoc,
    ParameterModel,
)
from andocgen.validator.factory import create_validator


def test_phantom_parameter_error() -> None:
    fn = FunctionModel(
        name="add",
        parameters=[ParameterModel(name="a"), ParameterModel(name="b")],
        returns="float",
    )
    ctx = EntityContext(
        entity_type="function",
        entity_name="add",
        entity_id="calc.py::add",
        module_path="calc.py",
        project_name="demo",
        function=fn,
    )
    block = DocBlock(
        entity_type="function",
        entity_name="add",
        module_path="calc.py",
        summary="Adds numbers.",
        content="Adds numbers.",
        parameters=[
            ParameterDoc(name="phantom", type="int", description="bad")
        ],
    )
    validator = create_validator(ValidationConfig())
    issues = validator.validate([block], [ctx], ValidationConfig())
    assert any("phantom" in i.message for i in issues)


def test_example_missing_required_args_warning() -> None:
    init_fn = FunctionModel(
        name="__init__",
        parameters=[
            ParameterModel(name="self"),
            ParameterModel(name="storage"),
        ],
        is_method=True,
        owner_class="OrderService",
    )
    fn = FunctionModel(
        name="create_order",
        parameters=[
            ParameterModel(name="self"),
            ParameterModel(name="customer"),
        ],
        returns="Order",
        is_method=True,
        owner_class="OrderService",
    )
    from andocgen.models.entities import ClassModel, ModuleModel

    service_cls = ClassModel(name="OrderService", methods=[init_fn, fn])
    ctx = EntityContext(
        entity_type="method",
        entity_name="OrderService.create_order",
        entity_id="services.py::OrderService.create_order",
        module_path="services.py",
        project_name="demo",
        function=fn,
        class_model=service_cls,
        module=ModuleModel(path="services.py", classes=[service_cls]),
        output_language="ru",
    )
    block = DocBlock(
        entity_type="method",
        entity_name="OrderService.create_order",
        module_path="services.py",
        summary="Creates order.",
        content="Creates order.",
        examples=[
            ExampleDoc(
                description="Create order.",
                language="python",
                code="order = OrderService().create_order('John')",
            )
        ],
    )
    validator = create_validator(ValidationConfig())
    issues = validator.validate([block], [ctx], ValidationConfig())
    assert any("constructor arguments" in i.message for i in issues)


def test_undocumented_raised_exception_warning() -> None:
    fn = FunctionModel(
        name="load",
        parameters=[],
        returns="str",
        source_body='raise ValueError("missing")',
    )
    ctx = EntityContext(
        entity_type="function",
        entity_name="load",
        entity_id="loader.py::load",
        module_path="loader.py",
        project_name="demo",
        function=fn,
    )
    block = DocBlock(
        entity_type="function",
        entity_name="load",
        module_path="loader.py",
        summary="Загружает значение.",
        raises="N/A",
        content="Загружает значение.",
    )

    issues = create_validator(ValidationConfig()).validate([block], [ctx], ValidationConfig())

    assert any("ValueError" in issue.message for issue in issues)


def test_invalid_python_example_warning() -> None:
    fn = FunctionModel(name="load", parameters=[], returns="str")
    ctx = EntityContext(
        entity_type="function",
        entity_name="load",
        entity_id="loader.py::load",
        module_path="loader.py",
        project_name="demo",
        function=fn,
    )
    block = DocBlock(
        entity_type="function",
        entity_name="load",
        module_path="loader.py",
        summary="Загружает значение.",
        content="Загружает значение.",
        examples=[ExampleDoc(description="Bad.", language="python", code="load(")],
    )

    issues = create_validator(ValidationConfig()).validate([block], [ctx], ValidationConfig())

    assert any("valid Python" in issue.message for issue in issues)


def test_return_type_mismatch_warning() -> None:
    fn = FunctionModel(name="load", parameters=[], returns="int")
    ctx = EntityContext(
        entity_type="function",
        entity_name="load",
        entity_id="loader.py::load",
        module_path="loader.py",
        project_name="demo",
        function=fn,
    )
    block = DocBlock(
        entity_type="function",
        entity_name="load",
        module_path="loader.py",
        summary="Загружает значение.",
        content="Загружает значение.",
        returns=None,
    )

    issues = create_validator(ValidationConfig()).validate([block], [ctx], ValidationConfig())

    assert any("Return type `int`" in issue.message for issue in issues)


def test_russian_language_check_covers_class_fields() -> None:
    ctx = EntityContext(
        entity_type="class",
        entity_name="Loader",
        entity_id="loader.py::Loader",
        module_path="loader.py",
        project_name="demo",
        output_language="ru",
    )
    block = DocBlock(
        entity_type="class",
        entity_name="Loader",
        module_path="loader.py",
        summary="Загрузчик данных.",
        purpose="Loads records from external storage and maps them into application objects.",
        usage_notes="Create it once and reuse it in endpoint handlers.",
        content="Загрузчик данных.",
    )

    issues = create_validator(ValidationConfig()).validate([block], [ctx], ValidationConfig())

    assert any("different language" in issue.message for issue in issues)


def test_class_signature_without_object() -> None:
    from andocgen.context.implementations.default_context import _class_signature
    from andocgen.models.entities import ClassModel

    assert _class_signature(ClassModel(name="Item", bases=[])) == "class Item"
    assert _class_signature(ClassModel(name="Child", bases=["Parent"])) == "class Child(Parent)"
