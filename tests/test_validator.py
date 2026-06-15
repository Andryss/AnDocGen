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
