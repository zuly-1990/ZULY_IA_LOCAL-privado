"""Cobertura mínima: apply_modifier, boolean con material_mode, weighted normal (MockAdapter)."""
import pytest
from core.adapters.mock_adapter import MockAdapter
from core.commands.blender_handlers.advanced.modifiers import (
    apply_modifier_handler,
    add_boolean_modifier_handler,
    add_weighted_normal_handler,
)


@pytest.fixture
def adapter():
    a = MockAdapter()
    a.create_primitive("cube", name="Die", location=[0, 0, 0])
    a.create_primitive("sphere", name="Cutter", location=[1, 0, 0])
    return a


def test_apply_modifier_apply_last(adapter):
    adapter.add_modifier("Die", "BEVEL", width=0.1, segments=2)
    r = apply_modifier_handler({"object_name": "Die", "apply_last": True}, adapter=adapter)
    assert r["success"] is True
    assert r.get("modifier_applied")


def test_boolean_then_apply_last(adapter):
    r1 = add_boolean_modifier_handler(
        {
            "object_name": "Die",
            "operand_object": "Cutter",
            "operation": "DIFFERENCE",
            "hide_operand": False,
            "material_mode": "TRANSFER",
        },
        adapter=adapter,
    )
    assert r1["success"] is True
    r2 = apply_modifier_handler({"object_name": "Die", "apply_last": True}, adapter=adapter)
    assert r2["success"] is True


def test_weighted_normal_then_apply(adapter):
    r1 = add_weighted_normal_handler({"object_name": "Die", "keep_sharp": True}, adapter=adapter)
    assert r1["success"] is True
    r2 = apply_modifier_handler({"object_name": "Die", "apply_last": True}, adapter=adapter)
    assert r2["success"] is True
