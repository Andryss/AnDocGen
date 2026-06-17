from __future__ import annotations

from andocgen.generator.entity_validator import validate_entity
from andocgen.models.entities import (
    ClassModel,
    DocBlock,
    EntityContext,
    FunctionModel,
    ModuleModel,
    ParameterDoc,
    ParameterModel,
)


def test_no_false_positive_on_namedtuple_empty_ctor() -> None:
    point_cls = ClassModel(
        name="Point",
        is_namedtuple=True,
        field_defs=[
            ParameterModel(name="x", type_annotation="int"),
            ParameterModel(name="y", type_annotation="int"),
        ],
    )
    fn = FunctionModel(
        name="show",
        parameters=[ParameterModel(name="self"), ParameterModel(name="p")],
        is_method=True,
        owner_class="Viewer",
    )
    ctx = EntityContext(
        entity_type="method",
        entity_name="Viewer.show",
        entity_id="main.py::Viewer.show",
        module_path="main.py",
        project_name="demo",
        function=fn,
        module=ModuleModel(path="main.py", classes=[point_cls]),
    )
    block = DocBlock(
        entity_type="method",
        entity_name="Viewer.show",
        module_path="main.py",
        summary="Shows point.",
        examples="```python\nPoint()\n```",
    )
    issues = validate_entity(block, ctx)
    assert any(issue.code == "examples_invalid_ctor" for issue in issues)


def test_no_false_positive_on_inmemory_storage_ctor() -> None:
    init_fn = FunctionModel(
        name="__init__",
        parameters=[ParameterModel(name="self")],
        is_method=True,
        owner_class="InMemoryStorage",
    )
    create_fn = FunctionModel(
        name="create",
        parameters=[
            ParameterModel(name="self"),
            ParameterModel(name="customer"),
        ],
        returns="Order",
        is_method=True,
        owner_class="InMemoryStorage",
    )
    storage_cls = ClassModel(name="InMemoryStorage", methods=[init_fn, create_fn])
    ctx = EntityContext(
        entity_type="method",
        entity_name="InMemoryStorage.create",
        entity_id="storage.py::InMemoryStorage.create",
        module_path="storage.py",
        project_name="demo",
        function=create_fn,
        class_model=storage_cls,
        module=ModuleModel(path="storage.py", classes=[storage_cls]),
    )
    block = DocBlock(
        entity_type="method",
        entity_name="InMemoryStorage.create",
        module_path="storage.py",
        summary="Creates order.",
        examples="```python\nstorage = InMemoryStorage()\nstorage.create('Alice')\n```",
    )
    issues = validate_entity(block, ctx)
    assert not any(issue.code == "examples_invalid_ctor" for issue in issues)


def test_blocking_on_order_service_ctor_without_args() -> None:
    init_fn = FunctionModel(
        name="__init__",
        parameters=[
            ParameterModel(name="self"),
            ParameterModel(name="storage"),
            ParameterModel(name="settings", default="None"),
        ],
        is_method=True,
        owner_class="OrderService",
    )
    create_fn = FunctionModel(
        name="create_order",
        parameters=[
            ParameterModel(name="self"),
            ParameterModel(name="customer"),
        ],
        returns="Order",
        is_method=True,
        owner_class="OrderService",
    )
    service_cls = ClassModel(name="OrderService", methods=[init_fn, create_fn])
    ctx = EntityContext(
        entity_type="method",
        entity_name="OrderService.create_order",
        entity_id="services.py::OrderService.create_order",
        module_path="services.py",
        project_name="demo",
        function=create_fn,
        class_model=service_cls,
        module=ModuleModel(path="services.py", classes=[service_cls]),
    )
    block = DocBlock(
        entity_type="method",
        entity_name="OrderService.create_order",
        module_path="services.py",
        summary="Creates order.",
        examples="```python\nOrderService().create_order('John')\n```",
    )
    issues = validate_entity(block, ctx)
    assert any(issue.code == "examples_invalid_ctor" for issue in issues)


def test_phantom_param_blocking() -> None:
    fn = FunctionModel(
        name="add",
        parameters=[ParameterModel(name="a"), ParameterModel(name="b")],
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
        summary="Adds.",
        parameters=[ParameterDoc(name="phantom", type="int", description="bad")],
    )
    issues = validate_entity(block, ctx)
    assert any(issue.code == "phantom_param" for issue in issues)
