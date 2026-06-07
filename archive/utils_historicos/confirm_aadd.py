#!/usr/bin/env python3
from core.cognition.c2_experience_memory import C2ExperienceMemory
import json

def confirm_extraction():
    memory = C2ExperienceMemory()
    all_exp = memory.storage.get_all_experiences()
    
    aadd_exp = [e for e in all_exp if "AADD" in str(e.recommendations) or "profesional" in e.objective]
    
    print(f"=== CONFIRMACIÓN DE EXTRACCIÓN AADD ===")
    print(f"Total experiencias en memoria: {len(all_exp)}")
    print(f"Experiencias AADD detectadas: {len(aadd_exp)}")
    print("\nDetalle de patrones extraídos:")
    
    for exp in aadd_exp[:5]:
        print(f"  - Objetivo: {exp.objective}")
        print(f"    Status: {exp.evaluation_status}")
        print(f"    Score: {exp.evaluation_score}")
        print(f"    Parámetros: {exp.parameters}")
        print(f"    Recomendaciones: {exp.recommendations}")
        print("-" * 30)

    insights = memory.get_insights()
    if insights.get('top_patterns'):
        print("\nTop Patrones Identificados por el Motor:")
        for p in insights['top_patterns']:
            if "profesional" in p['objective']:
                print(f"  ⭐ {p['objective']} (Score: {p['score']})")

if __name__ == "__main__":
    confirm_extraction()
