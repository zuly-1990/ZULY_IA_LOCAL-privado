import json

# Código inyectado para prueba
class CognitiveRiskExplainer:
    def __init__(self, evaluation_report: dict):
        self.report = evaluation_report

    def explain(self) -> list:
        messages = []

        ambiguous = self.report.get("ambiguous_language_detected", False)
        if ambiguous:
            messages.append(
                "Se detecta lenguaje ambiguo que puede dificultar la interpretación de algunos pasos."
            )

        technical_gaps = self.report.get("technical_gaps_detected", False)
        if technical_gaps:
            messages.append(
                "Se detectan elementos sin parámetros técnicos completos, lo que puede generar confusión durante la ejecución."
            )

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

def test_final_fase_5_7():
    # Reporte de ejemplo extremo
    mock_report = {
        "ambiguous_language_detected": True,
        "technical_gaps_detected": True,
        "confidence_level": "BAJO"
    }
    
    explainer = CognitiveRiskExplainer(mock_report)
    messages = explainer.explain()
    
    print("\n--- TEST FINAL FASE 5.7 ---")
    for msg in messages:
        print(f"ZULY dice: {msg}")
    
    assert len(messages) == 3
    assert messages[0] == "Se detecta lenguaje ambiguo que puede dificultar la interpretación de algunos pasos."
    assert messages[1] == "Se detectan elementos sin parámetros técnicos completos, lo que puede generar confusión durante la ejecución."
    assert messages[2] == "El tutorial presenta un nivel de claridad general bajo, con múltiples aspectos poco definidos."
    print("------------------------\n")

if __name__ == "__main__":
    test_final_fase_5_7()
