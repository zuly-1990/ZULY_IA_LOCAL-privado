class ClarificationQuestionGenerator:
    def __init__(self, evaluation_report: dict = None):
        self.report = evaluation_report or {}

    def generate(self) -> list:
        # Mantenemos compatibilidad con el DialogManager original
        questions = []
        if self.report.get("ambiguous_language_detected", False):
            questions.append("Hay pasos poco precisos. ¿Podrías aclarar los puntos ambiguos?")
        if self.report.get("technical_gaps_detected", False):
            questions.append("Faltan parámetros técnicos. ¿Podrías especificarlos?")
        return questions

    def generate_question(self, step: dict) -> str:
        """Genera una pregunta específica para un paso ambiguo o incompleto."""
        text = step.get("original_segment", "este paso")
        gaps = step.get("technical_gaps", [])
        clarity = step.get("clarity_score", 1.0)
        
        if gaps:
            return f"En el paso '{text}', detecto vacíos: {', '.join(gaps)}. ¿Podrías dar más detalles técnicos?"
        if clarity < 1.0:
            return f"El paso '{text}' usa lenguaje ambiguo. ¿Podrías ser más específico con las instrucciones?"
        
        return f"¿Podrías dar más detalles sobre el paso: '{text}'?"
