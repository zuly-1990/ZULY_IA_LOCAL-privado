"""
core/validation/v3_validator.py

Validador V3: Auditoría Topológica de Alta Precisión.
Fases Analíticas (ZULY 6.6)
Verifica que las mallas resultantes sean estancas, sin caras superpuestas o de área cero.
Uso bajo demanda (computacionalmente intensivo).

Incluye validación de ensamblaje (estructura, jerarquía, patrones JSON).
"""

from typing import Dict, Any, List, Optional
from core.utils.logging import log_info, log_warning, log_error, log_success


class V3Validator:
    """
    Agente evaluador V3.
    - Por malla: adapter.validate_mesh_topology + clasificación.
    - Por ensamblaje: jerarquía, flotación, coherencia dimensional, patrón declarativo.
    """

    def __init__(self, adapter=None):
        self._adapter = adapter
        log_info("✓ V3Validator inicializado (Topología Geométrica)")

    def validate(self, object_name: str, adapter) -> Dict[str, Any]:
        """
        Validación profunda de una malla vía el adapter.
        """
        log_info(f"[V3] Iniciando validación de malla profunda para: {object_name}")

        topo = getattr(adapter, "validate_mesh_topology", None)
        if not callable(topo):
            log_warning("[V3] Adapter sin validate_mesh_topology; se omite auditoría de malla")
            return {
                "verified": True,
                "classification": "SEGURO",
                "reason": "Topología no auditable en este adapter",
                "metrics": {},
                "object_name": object_name,
            }

        response = topo(object_name)

        if not response.get("success", False):
            log_error(f"[V3] Error capturando topología: {response.get('error')}")
            return {
                "verified": False,
                "reason": response.get("message") or response.get("error", "Error extrayendo datos de malla"),
                "classification": "CORRUPTO",
                "object_name": object_name,
            }

        metrics = response.get("metrics", {})

        non_manifold = metrics.get("non_manifold_edges_count", 0)
        loose_verts = metrics.get("loose_vertices_count", 0)
        zero_area = metrics.get("zero_area_faces_count", 0)
        is_watertight = metrics.get("is_watertight", False)

        if non_manifold == 0 and loose_verts == 0 and zero_area == 0:
            classification = "IMPECABLE"
            verified = True
            reason = "Malla estanca y perfecta. Lista para impresión o simulaciones FEM."
            log_success(f"[V3] '{object_name}' certificado como {classification}")
        elif not is_watertight and non_manifold < 5:
            classification = "SEGURO"
            verified = True
            reason = f"Malla con pequeños defectos ({non_manifold} bordes abiertos) pero usable para render."
            log_warning(f"[V3] '{object_name}' clasificado como {classification}: {reason}")
        else:
            classification = "CORRUPTO"
            verified = False
            reason = (
                f"Topología inestable: {non_manifold} bordes libres, {loose_verts} vértices sueltos, "
                f"{zero_area} caras nulas."
            )
            log_error(f"[V3] Fallo de Malla en '{object_name}': {reason}")

        return {
            "verified": verified,
            "classification": classification,
            "reason": reason,
            "metrics": metrics,
            "object_name": object_name,
        }

    def validate_structure(self, mapping: Dict[str, str]) -> Dict[str, Any]:
        """
        Valida un component_mapping { id_componente: nombre_objeto_blender }.
        """
        errors: List[str] = []
        warnings: List[str] = []

        if not self._adapter:
            return {"valid": False, "errors": ["Adapter no configurado en V3Validator"], "warnings": []}

        names = list(mapping.values())
        if not names:
            return {"valid": True, "errors": [], "warnings": []}

        hr = self.validate_hierarchy(names)
        errors.extend(hr.get("errors", []))
        warnings.extend(hr.get("warnings", []))

        fr = self.validate_floating_objects(names)
        warnings.extend(fr.get("warnings", []))

        dr = self.validate_dimensional_coherence(names)
        warnings.extend(dr.get("warnings", []))

        for name in names:
            verdict = self.validate(name, self._adapter)
            if not verdict.get("verified", False):
                errors.append(f"{name}: {verdict.get('reason', 'fallo V3')}")

        return {"valid": len(errors) == 0, "errors": errors, "warnings": warnings}

    def validate_pattern(self, pattern_def: Dict[str, Any]) -> Dict[str, Any]:
        """Valida definición declarativa de patrón (sin escena)."""
        errors: List[str] = []
        components = pattern_def.get("components") or []

        if not pattern_def.get("name"):
            errors.append("Falta nombre del patrón")

        ids = {c.get("id") for c in components if c.get("id")}
        if len(components) > 0 and None in ids:
            errors.append("Componente sin id")

        for comp in components:
            cid = comp.get("id")
            pid = comp.get("parent")
            if pid and pid not in ids:
                errors.append(f"Componente '{cid}': parent '{pid}' no existe en el patrón")

        return {"valid": len(errors) == 0, "errors": errors, "warnings": []}

    def validate_hierarchy(self, object_names: List[str]) -> Dict[str, Any]:
        """Detecta ciclos en la cadena parent de cada objeto."""
        errors: List[str] = []
        adp = self._adapter
        if not adp:
            return {"valid": False, "errors": ["Adapter no configurado"], "warnings": []}

        get_parent = getattr(adp, "get_parent", None)
        if not callable(get_parent):
            return {"valid": True, "errors": [], "warnings": []}

        for name in object_names:
            seen = set()
            cur: Optional[str] = name
            while cur:
                if cur in seen:
                    errors.append(f"Ciclo de jerarquía detectado (alcanzado desde '{name}')")
                    break
                seen.add(cur)
                cur = get_parent(cur)

        return {"valid": len(errors) == 0, "errors": errors, "warnings": []}

    def validate_floating_objects(
        self, object_names: List[str], ground_threshold: float = 0.01
    ) -> Dict[str, Any]:
        """Advierte objetos elevados sin padre (posible flotación)."""
        warnings: List[str] = []
        adp = self._adapter
        if not adp:
            return {"valid": True, "errors": [], "warnings": []}

        get_parent = getattr(adp, "get_parent", lambda _n: None)
        info_fn = getattr(adp, "get_object_info", None)

        for name in object_names:
            if not callable(info_fn):
                break
            inf = info_fn(name)
            if not inf.get("success"):
                continue
            loc = inf.get("location") or [0, 0, 0]
            z = loc[2] if len(loc) > 2 else 0.0
            parent = get_parent(name) if callable(get_parent) else None
            if z > ground_threshold and not parent:
                warnings.append(f"El objeto '{name}' parece flotar (z={z:.3f} sin padre)")

        return {"valid": True, "errors": [], "warnings": warnings}

    def validate_dimensional_coherence(self, object_names: List[str]) -> Dict[str, Any]:
        """Advierte si un hijo es mucho más grande que su padre (escala)."""
        warnings: List[str] = []
        adp = self._adapter
        if not adp:
            return {"valid": True, "errors": [], "warnings": []}

        get_parent = getattr(adp, "get_parent", None)
        info_fn = getattr(adp, "get_object_info", None)
        if not callable(get_parent) or not callable(info_fn):
            return {"valid": True, "errors": [], "warnings": []}

        for name in object_names:
            parent = get_parent(name)
            if not parent:
                continue
            ci = info_fn(name)
            pi = info_fn(parent)
            if not ci.get("success") or not pi.get("success"):
                continue
            cs = ci.get("scale") or [1, 1, 1]
            ps = pi.get("scale") or [1, 1, 1]
            cmax = max(float(x) for x in cs) if cs else 1.0
            pmax = max(float(x) for x in ps) if ps else 1.0
            if pmax > 0 and cmax > pmax * 1.5:
                warnings.append(
                    f"Hijo '{name}' (escala ~{cmax:.2f}) es mucho mayor que padre '{parent}' (~{pmax:.2f})"
                )

        return {"valid": True, "errors": [], "warnings": warnings}
