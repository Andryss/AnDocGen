from __future__ import annotations

from andocgen.models.entities import DocBlock, EntityContext, FunctionModel, ParameterDoc, ParameterModel
from andocgen.validator.factory import create_validator
from andocgen.config import ValidationConfig


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
        examples="```python\norder = OrderService().create_order('John')\n```",
    )
    validator = create_validator(ValidationConfig())
    issues = validator.validate([block], [ctx], ValidationConfig())
    assert any("constructor arguments" in i.message for i in issues)


def test_class_signature_without_object() -> None:
    from andocgen.context.implementations.default_context import _class_signature
    from andocgen.models.entities import ClassModel

    assert _class_signature(ClassModel(name="Item", bases=[])) == "class Item"
    assert _class_signature(ClassModel(name="Child", bases=["Parent"])) == "class Child(Parent)"
