"""
core/observability/system_state.py

Fase 18.1 — State Snapshot Humano

Captura el estado completo de ZULY de forma legible y robusta.
Principio: El snapshot NUNCA debe fallar, incluso si el sistema está roto.
"""

from typing import Dict, Any, Optional
from datetime import datetime
import json


class SystemStateSnapshot:
    """
    Snapshot del estado completo del sistema ZULY.
    
    Diseño:
    - Separación datos/representación
    - Fail-safe (nunca falla)
    - Encadenable (capture() retorna self)
    - Múltiples formatos (JSON, texto humano)
    """
    
    def __init__(self, agent):
        """
        Inicializa el snapshot con referencia al agent.
        
        Args:
            agent: Instancia de Agent
        """
        self.agent = agent
        self.state: Dict[str, Any] = {}
        self.timestamp = datetime.now()
    
    def capture(self) -> "SystemStateSnapshot":
        """
        Captura el estado completo del sistema.
        
        FAIL-SAFE: Nunca falla. Si un módulo no responde, marca como "unavailable".
        
        Returns:
            self (para encadenamiento)
        """
        # Timestamp en ISO
        self.state["timestamp"] = self.timestamp.isoformat()
        self.state["timestamp_local"] = self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        
        # Capturar cada componente con manejo de errores
        self.state["agent"] = self._capture_agent()
        self.state["adapter"] = self._capture_adapter()
        self.state["black_protocol"] = self._capture_black_protocol()
        self.state["modules"] = self._capture_modules()
        self.state["last_action"] = self._capture_last_action()
        
        # FASE 18.3: Trace (si existe)
        if hasattr(self.agent, "trace_core"):
            self.state["trace"] = {
                "total_events": len(self.agent.trace_core.traces),
                "last_event": (
                    self.agent.trace_core.traces[-1]
                    if self.agent.trace_core.traces else None
                )
            }
        
        return self
    
    def _capture_agent(self) -> Dict[str, Any]:
        """Captura estado del Agent (fail-safe)."""
        try:
            return {
                "operational_state": getattr(self.agent, "operational_state", "unknown"),
                "authorized": getattr(self.agent, "authorized", False),
                "commands_loaded": len(getattr(self.agent, "commands", {})),
                "session_start": getattr(self.agent.context, "session_start", datetime.now()).isoformat() if hasattr(self.agent, "context") else "unknown",
                "execution_history_count": len(getattr(self.agent.context, "execution_history", [])) if hasattr(self.agent, "context") else 0,
                "success_count": getattr(self.agent.context, "success_count", 0) if hasattr(self.agent, "context") else 0,
                "failure_count": getattr(self.agent.context, "failure_count", 0) if hasattr(self.agent, "context") else 0
            }
        except Exception as e:
            return {"status": "unavailable", "error": str(e)}
    
    def _capture_adapter(self) -> Dict[str, Any]:
        """Captura estado del Adapter (fail-safe)."""
        try:
            adapter = getattr(self.agent, "engine_adapter", None)
            if not adapter:
                return {"status": "not_initialized"}
            
            adapter_type = type(adapter).__name__
            available = adapter.is_available() if hasattr(adapter, "is_available") else False
            
            result = {
                "type": adapter_type,
                "available": available
            }
            
            # Intentar obtener info del motor
            if available:
                try:
                    engine_info = adapter.get_engine_info()
                    if engine_info.get("success"):
                        result["engine_name"] = engine_info.get("name", "unknown")
                        result["engine_version"] = engine_info.get("version", "unknown")
                except:
                    result["engine_name"] = "unavailable"
                    result["engine_version"] = "unavailable"
            
            return result
        except Exception as e:
            return {"status": "unavailable", "error": str(e)}
    
    def _capture_black_protocol(self) -> Dict[str, Any]:
        """Captura estado del Protocolo Negro (fail-safe)."""
        try:
            from core.security.black_protocol import BlackProtocol
            
            return {
                "active": BlackProtocol.is_active(),
                "mode": "MODO_NEGRO" if BlackProtocol.is_active() else "NORMAL",
                "last_check": datetime.now().isoformat()
            }
        except Exception as e:
            return {"status": "unavailable", "error": str(e)}
    
    def _capture_modules(self) -> Dict[str, str]:
        """Captura estado de módulos clave (fail-safe)."""
        modules = {}
        
        # SceneMonitor
        try:
            if hasattr(self.agent, "scene_monitor"):
                modules["scene_monitor"] = "active"
            else:
                modules["scene_monitor"] = "not_loaded"
        except:
            modules["scene_monitor"] = "unavailable"
        
        # BlenderObserver
        try:
            if hasattr(self.agent, "blender_observer"):
                modules["blender_observer"] = "active"
            else:
                modules["blender_observer"] = "not_loaded"
        except:
            modules["blender_observer"] = "unavailable"
        
        # PatternMemory
        try:
            if hasattr(self.agent, "pattern_memory"):
                stats = self.agent.pattern_memory.get_stats()
                pattern_count = stats.get("total_patterns", 0)
                modules["pattern_memory"] = f"active ({pattern_count} patterns)"
            else:
                modules["pattern_memory"] = "not_loaded"
        except:
            modules["pattern_memory"] = "unavailable"
        
        # TraceCore
        try:
            if hasattr(self.agent, "trace_core"):
                modules["trace_core"] = "active"
            else:
                modules["trace_core"] = "not_loaded"
        except:
            modules["trace_core"] = "unavailable"
        
        return modules
    
    def _capture_last_action(self) -> Dict[str, Any]:
        """Captura última acción ejecutada (fail-safe)."""
        try:
            if not hasattr(self.agent, "context"):
                return {"status": "no_context"}
            
            history = getattr(self.agent.context, "execution_history", [])
            if not history:
                return {"status": "no_actions"}
            
            last = history[-1]
            return {
                "command": last.get("command", "unknown"),
                "success": last.get("success", False),
                "timestamp": last.get("timestamp", "unknown")
            }
        except Exception as e:
            return {"status": "unavailable", "error": str(e)}
    
    def to_json(self, indent: int = 2) -> str:
        """
        Exporta snapshot a JSON.
        
        Args:
            indent: Nivel de indentación
            
        Returns:
            String JSON
        """
        return json.dumps(self.state, indent=indent, ensure_ascii=False)
    
    def to_human_readable(self) -> str:
        """
        Exporta snapshot a formato legible por humanos.
        
        Returns:
            String formateado con cajas ASCII
        """
        lines = []
        
        # Header
        lines.append("═" * 65)
        lines.append("🧠 ZULY - ESTADO DEL SISTEMA")
        lines.append("═" * 65)
        lines.append(f"Timestamp: {self.state.get('timestamp_local', 'unknown')}")
        lines.append("")
        
        # Agent
        agent = self.state.get("agent", {})
        lines.append("┌─ AGENT " + "─" * 56 + "┐")
        if agent.get("status") == "unavailable":
            lines.append(f"│ Estado: ❌ NO DISPONIBLE                                    │")
        else:
            lines.append(f"│ Estado Operacional: {agent.get('operational_state', 'unknown'):<33} │")
            auth = "✓ SÍ" if agent.get("authorized") else "✗ NO"
            lines.append(f"│ Autorizado: {auth:<48} │")
            lines.append(f"│ Comandos Cargados: {agent.get('commands_loaded', 0):<41} │")
            lines.append(f"│ Acciones Ejecutadas: {agent.get('execution_history_count', 0):<39} │")
            lines.append(f"│ Éxitos: {agent.get('success_count', 0):<52} │")
            lines.append(f"│ Fallos: {agent.get('failure_count', 0):<52} │")
        lines.append("└" + "─" * 63 + "┘")
        lines.append("")
        
        # Adapter
        adapter = self.state.get("adapter", {})
        lines.append("┌─ ADAPTER " + "─" * 53 + "┐")
        if adapter.get("status") == "unavailable":
            lines.append(f"│ Estado: ❌ NO DISPONIBLE                                    │")
        else:
            lines.append(f"│ Tipo: {adapter.get('type', 'unknown'):<56} │")
            avail = "✓ SÍ" if adapter.get("available") else "✗ NO"
            lines.append(f"│ Disponible: {avail:<50} │")
            if adapter.get("available"):
                engine = f"{adapter.get('engine_name', 'unknown')} {adapter.get('engine_version', '')}"
                lines.append(f"│ Motor: {engine:<55} │")
        lines.append("└" + "─" * 63 + "┘")
        lines.append("")
        
        # Protocolo Negro
        bp = self.state.get("black_protocol", {})
        lines.append("┌─ PROTOCOLO NEGRO " + "─" * 45 + "┐")
        if bp.get("status") == "unavailable":
            lines.append(f"│ Estado: ❌ NO DISPONIBLE                                    │")
        else:
            if bp.get("active"):
                lines.append(f"│ Estado: ❌ ACTIVO (MODO NEGRO)                              │")
            else:
                lines.append(f"│ Estado: ✓ NORMAL (no activo)                               │")
            lines.append(f"│ Modo: {bp.get('mode', 'unknown'):<56} │")
        lines.append("└" + "─" * 63 + "┘")
        lines.append("")
        
        # Módulos
        modules = self.state.get("modules", {})
        lines.append("┌─ MÓDULOS " + "─" * 53 + "┐")
        for name, status in modules.items():
            icon = "✓" if "active" in status else "✗"
            lines.append(f"│ {name}: {icon} {status:<48} │")
        lines.append("└" + "─" * 63 + "┘")
        lines.append("")
        
        # Última acción
        last = self.state.get("last_action", {})
        lines.append("┌─ ÚLTIMA ACCIÓN " + "─" * 47 + "┐")
        if last.get("status") in ["no_actions", "no_context", "unavailable"]:
            lines.append(f"│ Sin acciones registradas                                    │")
        else:
            lines.append(f"│ Comando: {last.get('command', 'unknown'):<51} │")
            result = "✓ ÉXITO" if last.get("success") else "✗ FALLO"
            lines.append(f"│ Resultado: {result:<51} │")
        lines.append("└" + "─" * 63 + "┘")
        lines.append("")
        
        # FASE 18.3: Traza (si existe)
        if "trace" in self.state:
            trace = self.state["trace"]
            lines.append("┌─ TRAZA " + "─" * 56 + "┐")
            lines.append(f"│ Eventos registrados: {trace['total_events']:<43} │")
            
            if trace["last_event"]:
                last_evt = trace["last_event"]
                data = last_evt.get("data", {})
                intention = data.get("intention", "unknown")
                success = data.get("execution_success", False)
                status = "✓" if success else "✗"
                lines.append(f"│ Último evento: {status} {intention:<46} │")
            
            lines.append("└" + "─" * 63 + "┘")
        
        # Footer
        lines.append("═" * 65)
        
        return "\n".join(lines)
    
    def save(self, filepath: str, format: str = "human"):
        """
        Guarda snapshot a archivo.
        
        Args:
            filepath: Ruta del archivo
            format: "human" o "json"
        """
        content = self.to_human_readable() if format == "human" else self.to_json()
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
    
    def print(self):
        """Imprime snapshot en formato humano."""
        print(self.to_human_readable())
