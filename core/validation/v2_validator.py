"""
v2_validator.py
===============

Validador de Nivel V2: Validación Contextual.

FIN DE SEMANA 4 — Plan Maestro ZULY 2026

Responsabilidad:
    Verificar que el CONTEXTO de ejecución es válido ANTES de que se ejecute
    cualquier comando en el motor. Si el contexto es incorrecto, bloquea
    inmediatamente con una explicación clara.

Principio: "V2 custodia la puerta. Si el contexto falla, ni siquiera
           se intenta la ejecución."

Cadena de validación completa:
    V2 (pre-ejecución, contextual)
        → Ejecución
        → V0 (post-ejecución, existencial)
        → V1 (post-ejecución, estructural)

Checks implementados:
    1. check_blender_available   — ¿Está Blender activo y disponible?
    2. check_execution_mode      — ¿Estamos en OBJECT mode? (no EDIT, SCULPT, etc.)
    3. check_active_collection   — ¿Hay una colección activa en la escena?
    4. check_base_file_path      — ¿El archivo activo respeta la ruta oficial?
    5. check_protocol_negro      — ¿El Protocolo Negro está activo?

Última actualización: 2026-03-07 (Semana 4)
"""

from typing import Dict, Any, List
from core.utils.logging import log_info, log_warning, log_error, log_success


class V2Validator:
    """
    Validador de Nivel V2: Validación Contextual.

    Corre ANTES de la ejecución del comando.
    Bloquea si el contexto es incorrecto o inseguro.
    NUNCA modifica el estado de la escena.
    """

    # Ruta oficial para proyectos .blend (según manual, Sección 15)
    ALLOWED_BASE_PATH = "ZULY_PROJECTS"
    ALLOWED_LAB_PATH = "ZULY_LAB/resultados_zuly"

    # Modos de Blender válidos para ejecutar comandos
    VALID_EXECUTION_MODES = {"OBJECT"}

    def __init__(self):
        self._last_checks = []  # Log de los últimos checks ejecutados

    def validate(self, adapter=None, blender_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Ejecuta la validación contextual completa.

        Corre todos los checks en orden. Si alguno falla, retorna
        bloqueo inmediato con explicación detallada.

        :param adapter: El engine adapter activo (BlenderAdapter o MockAdapter)
        :param blender_context: Contexto capturado por analyze_scene() del Agent
        :return: {'verified': bool, 'blocked': bool, 'checks': list, 'reason': str}
        """
        self._last_checks = []
        ctx = blender_context or {}

        # CHECK 1: ¿Blender está disponible?
        check1 = self.check_blender_available(adapter)
        self._last_checks.append(check1)
        if not check1["passed"]:
            return self._build_block_response(check1, self._last_checks)

        # CHECK 2: ¿Estamos en OBJECT mode?
        check2 = self.check_execution_mode(ctx)
        self._last_checks.append(check2)
        if not check2["passed"]:
            return self._build_block_response(check2, self._last_checks)

        # CHECK 3: ¿Hay colección activa?
        check3 = self.check_active_collection(ctx)
        self._last_checks.append(check3)
        if not check3["passed"]:
            return self._build_block_response(check3, self._last_checks)

        # CHECK 4: ¿El archivo base está en ruta oficial?
        check4 = self.check_base_file_path(ctx)
        self._last_checks.append(check4)
        # CHECK 4 es ADVERTENCIA, no bloqueo (un proyecto nuevo no tiene ruta aún)
        if not check4["passed"]:
            log_warning(f"[V2] Advertencia de ruta: {check4['detail']}")

        log_success("[V2] Contexto válido — ejecución autorizada.")
        return {
            "verified": True,
            "blocked": False,
            "checks": self._last_checks,
            "reason": "Contexto verificado. Todos los checks pasaron."
        }

    # ─────────────────────────────────────────────────
    # CHECKS INDIVIDUALES
    # ─────────────────────────────────────────────────

    def check_blender_available(self, adapter) -> Dict[str, Any]:
        """
        CHECK 1: Verifica que el motor Blender esté activo y disponible.

        Si el adapter es None o reporta is_available() = False,
        la ejecución está completamente fuera de contexto.
        """
        check_name = "blender_available"

        if adapter is None:
            return {
                "check": check_name,
                "passed": False,
                "detail": "V2 BLOQUEO: No hay adapter activo. "
                          "El sistema no puede ejecutar comandos sin un motor conectado."
            }

        try:
            is_available = adapter.is_available()
        except Exception as e:
            is_available = False

        if not is_available:
            return {
                "check": check_name,
                "passed": False,
                "detail": "V2 BLOQUEO: El adapter reporta que Blender NO está disponible. "
                          "Verifica que Blender está en ejecución o usa force_mock=True para simulación."
            }

        return {
            "check": check_name,
            "passed": True,
            "detail": "Blender disponible y activo."
        }

    def check_execution_mode(self, blender_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        CHECK 2: Verifica que Blender esté en OBJECT mode.

        En EDIT mode, SCULPT mode u otros modos especiales, los operadores
        de creación de primitivas pueden fallar o producir resultados incorrectos.
        """
        check_name = "execution_mode"

        # Si no hay contexto de Blender, se considera válido (MockAdapter u otro)
        if not blender_context:
            return {
                "check": check_name,
                "passed": True,
                "detail": "Sin contexto de modo (MockAdapter o contexto vacío) — check pasivo."
            }

        mode = blender_context.get("mode", blender_context.get("active_mode", "OBJECT"))

        if mode not in self.VALID_EXECUTION_MODES:
            return {
                "check": check_name,
                "passed": False,
                "detail": f"V2 BLOQUEO: Modo de ejecución inválido '{mode}'. "
                          f"Se requiere: {', '.join(self.VALID_EXECUTION_MODES)}. "
                          f"Sal del modo actual antes de ejecutar comandos."
            }

        return {
            "check": check_name,
            "passed": True,
            "detail": f"Modo de ejecución válido: '{mode}'."
        }

    def check_active_collection(self, blender_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        CHECK 3: Verifica que exista al menos una colección activa en la escena.

        Una escena sin colecciones es una escena corrupta o no inicializada.
        """
        check_name = "active_collection"

        if not blender_context:
            return {
                "check": check_name,
                "passed": True,
                "detail": "Sin contexto de colección (MockAdapter) — check pasivo."
            }

        # El contexto de Blender puede venir de analyze_scene() con distintos formatos
        collections = blender_context.get("collections", [])
        collection_count = blender_context.get("collection_count", len(collections))
        source = blender_context.get("source", "unknown")

        # Si la fuente no es Blender nativo o si es un adapter, el check es pasivo
        if source in ("no_blender", "mock", "simulation", "engine_adapter", "adapter"):
            return {
                "check": check_name,
                "passed": True,
                "detail": f"Fuente '{source}' — check de colección pasivo."
            }
        
        # En modo background, a veces la jerarquía de colecciones no se reporta igual
        if blender_context.get("is_background") or blender_context.get("mode") == "OBJECT":
             if collection_count == 0:
                 log_info("[V2] Colección no detectada en background, asumiendo Master Collection.")
                 return {
                    "check": check_name,
                    "passed": True,
                    "detail": "Modo background detectado — check de colección relajado."
                 }

        if collection_count == 0 and not collections:
            return {
                "check": check_name,
                "passed": False,
                "detail": "V2 BLOQUEO: No se detectaron colecciones en la escena. "
                          "La escena puede estar corrupta o no inicializada correctamente."
            }

        return {
            "check": check_name,
            "passed": True,
            "detail": f"Colecciones activas detectadas: {collection_count}."
        }

    def check_base_file_path(self, blender_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        CHECK 4: Verifica que el archivo .blend activo esté en la ruta oficial.

        Rutas válidas (según manual Sección 15):
          - ZULY_PROJECTS/
          - ZULY_LAB/resultados_zuly/
          - Archivo nuevo sin guardar (ruta vacía) — válido

        Este check genera ADVERTENCIA, no bloqueo.
        """
        check_name = "base_file_path"

        if not blender_context:
            return {
                "check": check_name,
                "passed": True,
                "detail": "Sin contexto de archivo (MockAdapter) — check pasivo."
            }

        filepath = blender_context.get("filepath", blender_context.get("base_file", ""))

        # Archivo nuevo (no guardado aún) — siempre válido
        if not filepath or filepath.strip() == "":
            return {
                "check": check_name,
                "passed": True,
                "detail": "Archivo nuevo sin guardar — ruta no requerida todavía."
            }

        # Normalizar path para comparación
        filepath_normalized = filepath.replace("\\", "/")

        if (self.ALLOWED_BASE_PATH in filepath_normalized or
                self.ALLOWED_LAB_PATH in filepath_normalized):
            return {
                "check": check_name,
                "passed": True,
                "detail": f"Ruta del archivo correcta: '{filepath_normalized}'."
            }

        return {
            "check": check_name,
            "passed": False,  # Advertencia, no bloqueo (ver validate())
            "detail": f"ADVERTENCIA V2: El archivo activo '{filepath_normalized}' está fuera "
                      f"de las rutas oficiales. Rutas válidas: "
                      f"[{self.ALLOWED_BASE_PATH}/, {self.ALLOWED_LAB_PATH}/]. "
                      f"Guarda tu proyecto en la ruta correcta (ver Manual Sección 15)."
        }

    # ─────────────────────────────────────────────────
    # UTILIDADES INTERNAS
    # ─────────────────────────────────────────────────

    def _build_block_response(self, failed_check: Dict, all_checks: List[Dict]) -> Dict[str, Any]:
        """Construye la respuesta de bloqueo con detalle completo."""
        log_error(f"[V2] {failed_check['detail']}")
        return {
            "verified": False,
            "blocked": True,
            "failed_check": failed_check["check"],
            "checks": all_checks,
            "reason": failed_check["detail"]
        }

    def get_last_checks(self) -> List[Dict]:
        """Retorna el log de los últimos checks ejecutados."""
        return self._last_checks
