"""
Fase 6 - Simulador de Intenciones
Motor de razonamiento puro que cruza "lo que el usuario quiere" con "lo que la realidad es".
NO EJECUTA NADA. Solo simula y valida.
"""

from typing import Dict, Any, List

class IntentionSimulator:
    """
    Analiza la viabilidad de una intención en el contexto actual.
    """

    def simulate(self, intent: Any, scene_context: Dict) -> Dict[str, Any]:
        """
        Simula la ejecución de una intención.
        
        Args:
            intent: Objeto CommandIntent o dict con 'command_name' y 'parameters'.
            scene_context: Dict completo retornado por agent.analyze_scene().
            
        Returns:
            Dict con formato estricto de Fase 6.
        """
        # Normalizar entrada de intención
        command_name = getattr(intent, 'command_name', str(intent)).lower()
        params = getattr(intent, 'parameters', {}) if hasattr(intent, 'parameters') else {}
        
        # Extraer datos clave del contexto
        objects_in_scene = [obj['name'] for obj in scene_context.get('visual_snapshot', {}).get('objects', [])]
        
        # Estructura base de respuesta
        simulation_result = {
            "intencion": f"{command_name} {params}",
            "estado_detectado": "Desconocido",
            "contradiccion": False,
            "razon": "Análisis completado",
            "opciones_sugeridas": [],
            "accion_ejecutada": False  # GARANTÍA DE SEGURIDAD
        }

        # Lógica de simulación específica por tipo de comando
        
        # CASO 1: BORRAR / ELIMINAR
        if 'borrar' in command_name or 'eliminar' in command_name:
            target_name = params.get('name') or params.get('nombre')
            
            # Si no se especifica nombre, buscar en parámetros posicionales o asumir "cubo" si intencion textual lo dice
            # (Simplificación para NLU básico, idealmente NLU ya entrega el parametro 'name')
            if not target_name: 
                 # Heurística simple para "borrar cubo" sin params explícitos en intent crudo
                 if 'cubo' in str(intent).lower(): target_name = 'Cube'
            
            if not target_name:
                 simulation_result["contradiccion"] = True
                 simulation_result["razon"] = "Intención incompleta: No se especificó qué borrar."
                 simulation_result["opciones_sugeridas"] = ["Especificar el nombre del objeto", "Seleccionar objeto"]
                 simulation_result["estado_detectado"] = "Intención vaga"
                 return simulation_result

            # Verificación de Existencia
            exists = False
            for obj_name in objects_in_scene:
                if target_name.lower() in obj_name.lower(): # Match laxo
                    exists = True
                    simulation_result["estado_detectado"] = f"Objeto '{obj_name}' encontrado"
                    break
            
            if not exists:
                simulation_result["estado_detectado"] = f"Objeto '{target_name}' NO existe en escena"
                simulation_result["contradiccion"] = True
                simulation_result["razon"] = f"No se puede borrar '{target_name}' porque no existe."
                simulation_result["opciones_sugeridas"] = [
                    f"Crear '{target_name}' antes de borrarlo",
                    "Listar objetos existentes",
                    "Cancelar operación"
                ]
            else:
                simulation_result["estado_detectado"] = f"Objeto '{target_name}' existe y está listo"
                simulation_result["razon"] = "Acción viable (pero simulada)"
                simulation_result["opciones_sugeridas"] = ["Confirmar borrado (Real)", "Mantener objeto"]

        # CASO 2: CREAR (Validación básica)
        elif 'crear' in command_name:
             target_name = params.get('name', 'NuevoObjeto')
             # Chequear si ya existe para evitar duplicados molestos (opcional, pero buena práctica)
             # ...
             simulation_result["estado_detectado"] = "Intención de creación"
             simulation_result["opciones_sugeridas"] = ["Proceder con creación"]

        else:
             simulation_result["estado_detectado"] = "Comando genérico"
             simulation_result["razon"] = "Simulación genérica aprobada"

        return simulation_result
