class CognitiveRiskExplainer:
    def __init__(self, evaluation_report: dict = None):
        self.report = evaluation_report or {}

    def explain(self, report: dict = None) -> list:
        # Permite pasar el reporte directamente como pide el script del usuario
        target_report = report if report else self.report
        messages = []

        # R-01 Lenguaje ambiguo
        if self.report.get("ambiguous_language_detected", False):
            messages.append(
                "Se detecta lenguaje ambiguo que puede dificultar la interpretación de algunos pasos."
            )

        # R-02 Vacíos técnicos
        if self.report.get("technical_gaps_detected", False):
            messages.append(
                "Se detectan elementos sin parámetros técnicos completos, lo que puede generar confusión durante la ejecución."
            )

        # R-03 Nivel de confianza global
        confidence_level = self.report.get("confidence_level")

        if confidence_level == "ALTO":
            messages.append(
                "El tutorial presenta un nivel de claridad y consistencia general alto."
            )
        elif confidence_level == "MEDIO":
            messages.append(
                "El tutorial presenta un nivel de claridad general medio, con algunos puntos que podrían requerir aclaración."
            )
        elif confidence_level == "BAJO":
            messages.append(
                "El tutorial presenta un nivel de claridad general bajo, con múltiples aspectos poco definidos."
            )

        return messages
