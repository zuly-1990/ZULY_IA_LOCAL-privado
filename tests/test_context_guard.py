import pytest
import sys
import os

# Añadir el path raíz para importar core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.guard.context_guard import ContextGuard

def test_render_blocked_when_dirty():
    context = {"is_dirty": True}
    result = ContextGuard.evaluate("RENDER", context)
    assert result["status"] == ContextGuard.BLOQUEADO
    assert "sin guardar" in result["reason"]

def test_render_allowed_when_not_dirty():
    context = {"is_dirty": False}
    result = ContextGuard.evaluate("RENDER", context)
    assert result["status"] == ContextGuard.PERMITIDO

def test_delete_blocked_when_no_selection():
    context = {"selected_objects_count": 0}
    result = ContextGuard.evaluate("DELETE", context)
    assert result["status"] == ContextGuard.BLOQUEADO
    assert "No hay objetos seleccionados" in result["reason"]

def test_delete_allowed_with_selection():
    context = {"selected_objects_count": 1}
    result = ContextGuard.evaluate("DELETE", context)
    assert result["status"] == ContextGuard.PERMITIDO

def test_create_blocked_in_edit_mode():
    context = {"mode": "EDIT"}
    result = ContextGuard.evaluate("CREATE", context)
    assert result["status"] == ContextGuard.BLOQUEADO
    assert "modo EDIT" in result["reason"]

def test_create_allowed_in_object_mode():
    context = {"mode": "OBJECT"}
    result = ContextGuard.evaluate("CREATE", context)
    assert result["status"] == ContextGuard.PERMITIDO

def test_edit_mode_blocked_without_active_object():
    context = {"active_object": None}
    result = ContextGuard.evaluate("EDIT_MODE", context)
    assert result["status"] == ContextGuard.BLOQUEADO
    assert "No hay un objeto activo" in result["reason"]

def test_edit_mode_allowed_with_active_object():
    context = {"active_object": "Cube"}
    result = ContextGuard.evaluate("EDIT_MODE", context)
    assert result["status"] == ContextGuard.PERMITIDO
