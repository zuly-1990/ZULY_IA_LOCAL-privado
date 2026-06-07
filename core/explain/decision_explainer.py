"""
DecisionExplainer - El Corazón de la Explicabilidad de ZULY
Fase 13: "Si no puedo explicarlo, no debo hacerlo."
"""

import datetime

class DecisionExplainer:
    """
    Genera resúmenes humanos y logs técnicos sobre el porqué de una decisión.
    """

    @staticmethod
    def explain(decision_data: dict) -> dict:
        """
        Analiza los datos de decisión y genera una narrativa coherente.
        
        Args:
            decision_data (dict): {
                "intention": str,
                "guard_result": dict,       # { status, reason }
                "simulation_result": dict,  # Opcional { status, prediction }
                "execution_result": dict    # Opcional { success, message, details }
            }
            
        Returns:
            dict: {
                "human_summary": str,
                "technical_log": dict,
                "timestamp": str
            }
        """
        intention = decision_data.get("intention", "Desconocida").upper()
        guard = decision_data.get("guard_result", {})
        simulation = decision_data.get("simulation_result", {})
        execution = decision_data.get("execution_result", {})
        
        status = guard.get("status", "BLOQUEADO")
        reason = guard.get("reason", "Sin motivo especificado")
        
        human_summary = ""
        
        # Escenario: Bloqueado por Context Guard
        if status == "BLOQUEADO":
            human_summary = f"No ejecuté '{intention}' porque {reason.lower()}"
        
        # Escenario: Permitido
        else:
            if execution:
                success = execution.get("success", False)
                exec_msg = execution.get("message", "")
                
                if success:
                    human_summary = f"La acción '{intention}' fue realizada con éxito. {exec_msg}"
                else:
                    human_summary = f"Intenté ejecutar '{intention}' pero ocurrió un error técnico: {exec_msg}"
            
            elif simulation:
                # Caso donde solo hubo simulación
                sim_status = simulation.get("status", "OK")
                human_summary = f"La acción '{intention}' es válida según el contexto. Simulación: {sim_status}."
            
            else:
                human_summary = f"La acción '{intention}' ha sido validada y está lista para ejecutarse."

        # Construcción del registro técnico
        technical_log = {
            "intention": intention,
            "guard_status": status,
            "guard_reason": reason,
            "simulation": simulation,
            "execution": execution,
            "phase": "FASE_13_EXPLAINABILITY"
        }

        return {
            "human_summary": human_summary,
            "technical_log": technical_log,
            "timestamp": datetime.datetime.now().isoformat()
        }
