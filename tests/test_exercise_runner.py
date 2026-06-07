"""
ZULY LAB - Pruebas Unitarias para ExerciseRunner
==================================================
Cubre:
  - Inicialización del runner (creación de directorios)
  - Carga de ejercicios YAML reales del proyecto
  - Ejecución de pasos individuales (handler_map)
  - Ejecución completa de un ejercicio (A1.1, A1.2, A1.3)
  - Sistema de validaciones (object_exists, object_count, object_at_location, object_scale)
  - Guardado de logs JSON
  - Ejecución de fase completa (run_all_phase)

Todos los tests corren SIN Blender real (Agent force_mock=True).
"""

import sys
import json
import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import MagicMock, patch

# Asegurar que el proyecto está en el path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.agent import Agent
from core.lab.exercise_runner import ExerciseRunner


# ──────────────────────────────────────────────────────────────────────────────
# Helpers / Fixtures
# ──────────────────────────────────────────────────────────────────────────────

# Ruta real al ZULY_LAB del proyecto
ZULY_LAB_REAL = Path(__file__).parent.parent / "ZULY_LAB"


@pytest.fixture
def agent_mock():
    """Agent en modo MockAdapter para tests sin Blender."""
    return Agent(force_mock=True)


@pytest.fixture
def tmp_lab_root(tmp_path):
    """
    Crea un lab root temporal que apunta a los ejercicios reales.
    Replica la estructura de ZULY_LAB pero con logs/resultados en tmp.
    """
    # Copiar ejercicios reales al directorio temporal
    for fase in ["A_estructura", "B_automatizacion", "C_render_tecnico", "D_integracion_real"]:
        src = ZULY_LAB_REAL / fase / "ejercicios"
        dst = tmp_path / fase / "ejercicios"
        if src.exists():
            shutil.copytree(src, dst)
        else:
            dst.mkdir(parents=True, exist_ok=True)
    return tmp_path


@pytest.fixture
def runner(agent_mock, tmp_lab_root):
    """ExerciseRunner listo para usar con ejercicios reales y directorios temporales."""
    return ExerciseRunner(agent_mock, lab_root=str(tmp_lab_root))


# ──────────────────────────────────────────────────────────────────────────────
# TestExerciseRunnerInit
# ──────────────────────────────────────────────────────────────────────────────

class TestExerciseRunnerInit:
    """Pruebas de inicialización del ExerciseRunner."""

    def test_crea_directorio_resultados(self, agent_mock, tmp_path):
        """Al instanciar el runner, debe crear la carpeta resultados_zuly/."""
        runner = ExerciseRunner(agent_mock, lab_root=str(tmp_path))
        assert (tmp_path / "resultados_zuly").exists(), \
            "resultados_zuly/ no fue creado"

    def test_crea_directorio_logs(self, agent_mock, tmp_path):
        """Al instanciar el runner, debe crear la carpeta logs_sesiones/."""
        runner = ExerciseRunner(agent_mock, lab_root=str(tmp_path))
        assert (tmp_path / "logs_sesiones").exists(), \
            "logs_sesiones/ no fue creado"

    def test_lab_root_es_path(self, agent_mock, tmp_path):
        """El atributo lab_root debe ser un Path."""
        runner = ExerciseRunner(agent_mock, lab_root=str(tmp_path))
        assert isinstance(runner.lab_root, Path)

    def test_lab_root_configurable(self, agent_mock, tmp_path):
        """El lab_root debe ser el que se pasó en el constructor."""
        runner = ExerciseRunner(agent_mock, lab_root=str(tmp_path))
        assert runner.lab_root == tmp_path

    def test_runner_referencia_agent(self, agent_mock, tmp_path):
        """El runner debe guardar la referencia al agent."""
        runner = ExerciseRunner(agent_mock, lab_root=str(tmp_path))
        assert runner.agent is agent_mock


# ──────────────────────────────────────────────────────────────────────────────
# TestLoadExercise
# ──────────────────────────────────────────────────────────────────────────────

class TestLoadExercise:
    """Pruebas de carga de ejercicios YAML reales del proyecto."""

    def test_carga_A1_1_nombre(self, runner):
        """A1.1 debe tener nombre 'Cubo Básico'."""
        ex = runner.load_exercise("A1.1")
        assert ex["name"] == "Cubo Básico"

    def test_carga_A1_1_fase(self, runner):
        """A1.1 debe pertenecer a la fase A."""
        ex = runner.load_exercise("A1.1")
        assert ex["fase"] == "A"

    def test_carga_A1_1_tiene_steps(self, runner):
        """A1.1 debe tener una lista de pasos no vacía."""
        ex = runner.load_exercise("A1.1")
        assert "steps" in ex
        assert len(ex["steps"]) > 0

    def test_carga_A1_1_tiene_validation(self, runner):
        """A1.1 debe incluir reglas de validación."""
        ex = runner.load_exercise("A1.1")
        assert "validation" in ex
        assert len(ex["validation"]) > 0

    def test_carga_A1_1_tiene_success_criteria(self, runner):
        """A1.1 debe tener criterios de éxito."""
        ex = runner.load_exercise("A1.1")
        assert "success_criteria" in ex

    def test_carga_A1_2_nombre(self, runner):
        """A1.2 debe tener nombre '5 Columnas Alineadas'."""
        ex = runner.load_exercise("A1.2")
        assert ex["name"] == "5 Columnas Alineadas"

    def test_carga_A1_3_tiene_pasos_suficientes(self, runner):
        """A1.3 debe tener al menos 6 pasos."""
        ex = runner.load_exercise("A1.3")
        assert len(ex["steps"]) >= 6

    def test_carga_B1_1_nombre(self, runner):
        """B1.1 debe tener nombre 'Espiral de ADN'."""
        ex = runner.load_exercise("B1.1")
        assert ex["name"] == "Espiral de ADN"

    def test_carga_B1_1_fase_B(self, runner):
        """B1.1 debe pertenecer a la fase B."""
        ex = runner.load_exercise("B1.1")
        assert ex["fase"] == "B"

    def test_carga_A1_4_nombre(self, runner):
        """A1.4 debe tener nombre 'Altar de Zuly'."""
        ex = runner.load_exercise("A1.4")
        assert ex["name"] == "Altar de Zuly"

    def test_ejercicio_inexistente_lanza_error(self, runner):
        """Ejercicio que no existe debe lanzar FileNotFoundError o KeyError.
        
        Si la fase no está mapeada (ej: 'Z') el runner lanza KeyError del dict.
        Si la fase está mapeada pero el YAML no existe, lanza FileNotFoundError.
        Ambos son comportamientos correctos de 'ejercicio no encontrado'.
        """
        with pytest.raises((FileNotFoundError, KeyError)):
            runner.load_exercise("Z9.9")

    def test_ejercicio_con_fase_valida_pero_sin_yaml_lanza_file_not_found(self, runner):
        """Si la fase existe pero el ejercicio no tiene YAML, debe lanzar FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            runner.load_exercise("A9.9")  # Fase A existe pero A9.9 no tiene YAML

    def test_fase_invalida_lanza_error(self, runner):
        """Fase no mapeada debe lanzar KeyError."""
        with pytest.raises(KeyError):
            runner.load_exercise("X1.1")


# ──────────────────────────────────────────────────────────────────────────────
# TestExecuteStep
# ──────────────────────────────────────────────────────────────────────────────

class TestExecuteStep:
    """Pruebas de ejecución de pasos individuales."""

    def _make_step(self, action, params=None):
        return {"action": action, "params": params or {}}

    def test_create_cube_exito(self, runner):
        """Paso create_cube debe retornar exito=True con MockAdapter."""
        step = self._make_step("create_cube", {"location": [0, 0, 0], "name": "TestCubo"})
        result = runner._execute_step(step, 1)
        assert result["exito"] is True, f"Se esperaba éxito pero se obtuvo: {result}"

    def test_create_sphere_exito(self, runner):
        """Paso create_sphere debe retornar exito=True."""
        step = self._make_step("create_sphere", {"location": [1, 0, 0]})
        result = runner._execute_step(step, 1)
        assert result["exito"] is True

    def test_create_cylinder_exito(self, runner):
        """Paso create_cylinder debe retornar exito=True."""
        step = self._make_step("create_cylinder", {"location": [0, 0, 0], "name": "Col1", "scale": [0.3, 0.3, 2.0]})
        result = runner._execute_step(step, 1)
        assert result["exito"] is True

    def test_create_plane_exito(self, runner):
        """Paso create_plane debe retornar exito=True."""
        step = self._make_step("create_plane", {"location": [0, 0, 0], "name": "Suelo"})
        result = runner._execute_step(step, 1)
        assert result["exito"] is True

    def test_move_object_exito(self, runner):
        """Paso move_object debe retornar exito=True."""
        # Primero crear el objeto
        runner._execute_step(self._make_step("create_cube", {"name": "CuboMover"}), 1)
        step = self._make_step("move_object", {"object_name": "CuboMover", "location": [2, 0, 0]})
        result = runner._execute_step(step, 2)
        assert result["exito"] is True

    def test_create_material_exito(self, runner):
        """Paso create_material debe retornar exito=True."""
        step = self._make_step("create_material", {"name": "MatTest", "color": [1.0, 0.0, 0.0, 1.0]})
        result = runner._execute_step(step, 1)
        assert result["exito"] is True

    def test_create_light_exito(self, runner):
        """Paso create_light debe retornar exito=True."""
        step = self._make_step("create_light", {"light_type": "SUN", "name": "Luz1"})
        result = runner._execute_step(step, 1)
        assert result["exito"] is True

    def test_create_camera_exito(self, runner):
        """Paso create_camera debe retornar exito=True."""
        step = self._make_step("create_camera", {"location": [7, -7, 5]})
        result = runner._execute_step(step, 1)
        assert result["exito"] is True

    def test_accion_desconocida_falla(self, runner):
        """Acción no mapeada debe retornar exito=False."""
        step = self._make_step("accion_que_no_existe", {})
        result = runner._execute_step(step, 1)
        assert result["exito"] is False
        assert "error" in result

    def test_paso_registra_numero(self, runner):
        """El resultado del paso debe incluir el número de paso."""
        step = self._make_step("create_cube", {"name": "CuboN"})
        result = runner._execute_step(step, 5)
        assert result["numero"] == 5

    def test_paso_registra_action(self, runner):
        """El resultado del paso debe incluir la acción ejecutada."""
        step = self._make_step("create_cube", {"name": "CuboA"})
        result = runner._execute_step(step, 1)
        assert result["action"] == "create_cube"

    def test_paso_registra_timestamp(self, runner):
        """El resultado del paso debe tener un timestamp."""
        step = self._make_step("create_cube", {"name": "CuboT"})
        result = runner._execute_step(step, 1)
        assert "timestamp" in result
        assert result["timestamp"] is not None


# ──────────────────────────────────────────────────────────────────────────────
# TestExecuteExercise (Ejecución completa)
# ──────────────────────────────────────────────────────────────────────────────

class TestExecuteExercise:
    """Pruebas de ejecución completa de ejercicios."""

    def test_ejecuta_A1_1_retorna_dict(self, runner):
        """Ejecutar A1.1 debe retornar un diccionario."""
        result = runner.execute_exercise("A1.1")
        assert isinstance(result, dict)

    def test_resultado_tiene_campo_ejercicio(self, runner):
        """El resultado debe incluir el campo 'ejercicio'."""
        result = runner.execute_exercise("A1.1")
        assert "ejercicio" in result
        assert result["ejercicio"] == "A1.1"

    def test_resultado_tiene_campo_exito(self, runner):
        """El resultado debe incluir el campo 'exito'."""
        result = runner.execute_exercise("A1.1")
        assert "exito" in result
        assert isinstance(result["exito"], bool)

    def test_resultado_tiene_pasos_ejecutados(self, runner):
        """El resultado debe incluir 'pasos_ejecutados' como lista."""
        result = runner.execute_exercise("A1.1")
        assert "pasos_ejecutados" in result
        assert isinstance(result["pasos_ejecutados"], list)

    def test_resultado_tiene_tiempo_total(self, runner):
        """El resultado debe incluir el tiempo total de ejecución."""
        result = runner.execute_exercise("A1.1")
        assert "tiempo_total_segundos" in result
        assert result["tiempo_total_segundos"] >= 0

    def test_resultado_tiene_errores(self, runner):
        """El resultado debe incluir la lista de errores."""
        result = runner.execute_exercise("A1.1")
        assert "errores" in result
        assert isinstance(result["errores"], list)

    def test_resultado_tiene_validacion(self, runner):
        """El resultado debe incluir el campo de validación."""
        result = runner.execute_exercise("A1.1")
        assert "validacion" in result

    def test_A1_1_exito_con_mock(self, runner):
        """A1.1 ejecutado con MockAdapter debe retornar exito=True."""
        result = runner.execute_exercise("A1.1")
        assert result["exito"] is True, \
            f"A1.1 debería tener éxito con MockAdapter. Errores: {result.get('errores')}"

    def test_A1_2_exito_con_mock(self, runner):
        """A1.2 ejecutado con MockAdapter debe retornar exito=True."""
        result = runner.execute_exercise("A1.2")
        assert result["exito"] is True, \
            f"A1.2 debería tener éxito con MockAdapter. Errores: {result.get('errores')}"

    def test_A1_3_exito_con_mock(self, runner):
        """A1.3 ejecutado con MockAdapter debe retornar exito=True."""
        result = runner.execute_exercise("A1.3")
        assert result["exito"] is True, \
            f"A1.3 debería tener éxito con MockAdapter. Errores: {result.get('errores')}"

    def test_A1_1_pasos_contados_correctamente(self, runner):
        """Los pasos exitosos + fallidos deben sumar el total de pasos."""
        result = runner.execute_exercise("A1.1")
        total = result["pasos_exitosos"] + result["pasos_fallidos"]
        assert total == len(result["pasos_ejecutados"])

    def test_A1_1_genera_log_json(self, runner):
        """Ejecutar A1.1 debe generar al menos un archivo JSON en logs_sesiones/."""
        runner.execute_exercise("A1.1")
        logs = list(runner.logs_dir.glob("A1.1_*.json"))
        assert len(logs) >= 1, "No se encontró log JSON para A1.1"

    def test_log_tiene_estructura_correcta(self, runner):
        """El archivo de log JSON debe tener los campos del estándar ZULY_LAB."""
        runner.execute_exercise("A1.1")
        logs = list(runner.logs_dir.glob("A1.1_*.json"))
        assert logs, "No hay archivos de log"
        with open(logs[0], "r", encoding="utf-8") as f:
            data = json.load(f)
        campos_requeridos = [
            "ejercicio", "nombre", "timestamp",
            "pasos_ejecutados", "pasos_exitosos", "pasos_fallidos",
            "tiempo_total_segundos", "exito", "errores"
        ]
        for campo in campos_requeridos:
            assert campo in data, f"Falta campo '{campo}' en el log JSON"

    def test_log_ejercicio_correcto(self, runner):
        """El log debe registrar el código correcto del ejercicio."""
        runner.execute_exercise("A1.2")
        logs = list(runner.logs_dir.glob("A1.2_*.json"))
        assert logs
        with open(logs[0], "r", encoding="utf-8") as f:
            data = json.load(f)
        assert data["ejercicio"] == "A1.2"

    def test_multiples_ejecuciones_generan_multiples_logs(self, runner):
        """Cada ejecución debe generar un log separado con timestamp único.
        
        El timestamp del filename tiene granularidad de segundos, así que
        esperamos 1.1s entre ejecuciones para garantizar nombres distintos.
        """
        import time
        runner.execute_exercise("A1.1")
        time.sleep(1.1)  # Garantizar timestamp diferente en el nombre del archivo
        runner.execute_exercise("A1.1")
        logs = list(runner.logs_dir.glob("A1.1_*.json"))
        assert len(logs) >= 2, "Se esperan al menos 2 logs para 2 ejecuciones"


# ──────────────────────────────────────────────────────────────────────────────
# TestValidation
# ──────────────────────────────────────────────────────────────────────────────

class TestValidation:
    """Pruebas del sistema de validación del ExerciseRunner."""

    def test_validacion_object_exists_pasa_si_objeto_existe(self, runner):
        """Validación object_exists pasa si el adapter retorna éxito."""
        # Crear el objeto primero
        runner._execute_step({"action": "create_cube", "params": {"name": "ObjPrueba"}}, 1)

        validations = [{"type": "object_exists", "object_name": "ObjPrueba"}]
        result = runner._validate_exercise(validations)
        assert result["pasadas"] == 1

    def test_validacion_object_exists_falla_si_no_existe(self, runner):
        """Validación object_exists falla si el adapter no conoce el objeto."""
        # Forzar que el adapter retorne fallo para cualquier objeto
        runner.agent.engine_adapter.get_object_info = MagicMock(
            return_value={"success": False, "error": "Not found"}
        )
        validations = [{"type": "object_exists", "object_name": "ObjetoFantasma"}]
        result = runner._validate_exercise(validations)
        assert result["fallidas"] == 1

    def test_validacion_object_count_pasa_con_conteo_correcto(self, runner):
        """Validación object_count pasa si el adapter reporta el número correcto."""
        runner.agent.engine_adapter.get_scene_state = MagicMock(
            return_value={"success": True, "object_count": 5}
        )
        validations = [{"type": "object_count", "expected": 5}]
        result = runner._validate_exercise(validations)
        assert result["pasadas"] == 1

    def test_validacion_object_count_falla_con_conteo_incorrecto(self, runner):
        """Validación object_count falla si el conteo no coincide."""
        runner.agent.engine_adapter.get_scene_state = MagicMock(
            return_value={"success": True, "object_count": 2}
        )
        validations = [{"type": "object_count", "expected": 10}]
        result = runner._validate_exercise(validations)
        assert result["fallidas"] == 1

    def test_validacion_object_at_location_pasa_dentro_tolerancia(self, runner):
        """object_at_location pasa si la distancia es menor a la tolerancia."""
        runner.agent.engine_adapter.get_object_info = MagicMock(
            return_value={"success": True, "location": [2.005, 0.001, 0.0], "scale": [1, 1, 1]}
        )
        validations = [{
            "type": "object_at_location",
            "object_name": "CuboA1",
            "expected_location": [2, 0, 0],
            "tolerance": 0.01
        }]
        result = runner._validate_exercise(validations)
        assert result["pasadas"] == 1

    def test_validacion_object_at_location_falla_fuera_tolerancia(self, runner):
        """object_at_location falla si la distancia supera la tolerancia."""
        runner.agent.engine_adapter.get_object_info = MagicMock(
            return_value={"success": True, "location": [5, 5, 5], "scale": [1, 1, 1]}
        )
        validations = [{
            "type": "object_at_location",
            "object_name": "CuboA1",
            "expected_location": [2, 0, 0],
            "tolerance": 0.01
        }]
        result = runner._validate_exercise(validations)
        assert result["fallidas"] == 1

    def test_validacion_object_scale_pasa_dentro_tolerancia(self, runner):
        """object_scale pasa si la escala coincide dentro de tolerancia."""
        runner.agent.engine_adapter.get_object_info = MagicMock(
            return_value={"success": True, "location": [0, 0, 0], "scale": [2.001, 2.001, 2.001]}
        )
        validations = [{
            "type": "object_scale",
            "object_name": "CuboA1",
            "expected_scale": 2.0,
            "tolerance": 0.01
        }]
        result = runner._validate_exercise(validations)
        assert result["pasadas"] == 1

    def test_validacion_material_applied_pasa_si_objeto_existe(self, runner):
        """material_applied pasa si el objeto existe en el adapter."""
        runner.agent.engine_adapter.get_object_info = MagicMock(
            return_value={"success": True, "location": [0, 0, 0], "scale": [1, 1, 1]}
        )
        validations = [{
            "type": "material_applied",
            "object_name": "CuboA1",
            "material_name": "MaterialBasico"
        }]
        result = runner._validate_exercise(validations)
        assert result["pasadas"] == 1

    def test_validacion_total_cuenta_todas_las_reglas(self, runner):
        """El total de validaciones debe coincidir con el número de reglas."""
        runner.agent.engine_adapter.get_object_info = MagicMock(
            return_value={"success": True, "location": [0, 0, 0], "scale": [1, 1, 1]}
        )
        validations = [
            {"type": "object_exists", "object_name": "A"},
            {"type": "object_exists", "object_name": "B"},
        ]
        result = runner._validate_exercise(validations)
        assert result["total"] == 2

    def test_validacion_pasadas_mas_fallidas_igual_total(self, runner):
        """La suma de pasadas y fallidas debe ser el total."""
        runner.agent.engine_adapter.get_object_info = MagicMock(
            return_value={"success": True, "location": [0, 0, 0], "scale": [1, 1, 1]}
        )
        runner.agent.engine_adapter.get_scene_state = MagicMock(
            return_value={"success": True, "object_count": 99}
        )
        validations = [
            {"type": "object_exists", "object_name": "A"},
            {"type": "object_count", "expected": 1},  # Fallará (99 != 1)
        ]
        result = runner._validate_exercise(validations)
        assert result["pasadas"] + result["fallidas"] == result["total"]

    def test_validacion_tipo_desconocido_pasa_por_defecto(self, runner):
        """Validación de tipo desconocido debe pasar por defecto (sin bloquear ejercicio)."""
        validations = [{"type": "TIPO_INEXISTENTE_NEVER_ADDED"}]
        result = runner._validate_exercise(validations)
        assert result["pasadas"] == 1


# ──────────────────────────────────────────────────────────────────────────────
# TestRunAllPhase
# ──────────────────────────────────────────────────────────────────────────────

class TestRunAllPhase:
    """Pruebas de ejecución de fase completa."""

    def test_run_all_A_retorna_lista(self, runner):
        """run_all_phase('A') debe retornar una lista de resultados."""
        results = runner.run_all_phase("A")
        assert isinstance(results, list)

    def test_run_all_A_ejecuta_todos_los_ejercicios(self, runner):
        """run_all_phase('A') debe ejecutar los 4 ejercicios de Fase A."""
        results = runner.run_all_phase("A")
        # Fase A tiene: A1.1, A1.2, A1.3, A1.4
        assert len(results) == 4, \
            f"Se esperaban 4 resultados para Fase A, se obtuvieron {len(results)}"

    def test_run_all_A_cada_resultado_tiene_campo_exito(self, runner):
        """Cada resultado de run_all_phase debe tener el campo 'exito'."""
        results = runner.run_all_phase("A")
        for r in results:
            assert "exito" in r

    def test_run_all_A_con_mock_todos_exitosos(self, runner):
        """Con MockAdapter, todos los ejercicios de Fase A deben tener éxito."""
        results = runner.run_all_phase("A")
        fallidos = [r["ejercicio"] for r in results if not r["exito"]]
        assert not fallidos, f"Ejercicios fallidos con MockAdapter: {fallidos}"

    def test_run_all_B_retorna_lista(self, runner):
        """run_all_phase('B') debe retornar una lista de resultados."""
        results = runner.run_all_phase("B")
        assert isinstance(results, list)

    def test_run_all_B_ejecuta_ejercicios_fase_B(self, runner):
        """run_all_phase('B') debe ejecutar los ejercicios de Fase B."""
        results = runner.run_all_phase("B")
        assert len(results) >= 1, "Fase B no encontró ningún ejercicio"

    def test_run_all_genera_logs_para_cada_ejercicio(self, runner):
        """Cada ejercicio ejecutado debe generar su propio log."""
        runner.run_all_phase("A")
        logs = list(runner.logs_dir.glob("*.json"))
        assert len(logs) >= 4, \
            f"Se esperaban al menos 4 logs para Fase A, hay {len(logs)}"

    def test_run_all_codigos_correctos_en_resultados(self, runner):
        """Los códigos de ejercicio en los resultados deben comenzar con la fase."""
        results = runner.run_all_phase("A")
        for r in results:
            assert r["ejercicio"].startswith("A"), \
                f"Ejercicio '{r['ejercicio']}' no pertenece a Fase A"
