#!/usr/bin/env python3
"""
train_zuly_aadd.py

Integra el sistema AADD (Architecture-Augmented Data-Driven) en la memoria C2
para acelerar el aprendizaje de patrones arquitectónicos profesionales.
"""

import sys
from pathlib import Path

# Agregar ruta del proyecto
sys.path.insert(0, str(Path(__file__).parent))

from core.cognition.c2_experience_memory import C2ExperienceMemory

def train_aadd():
    print("=== ACELERACIÓN DE APRENDIZAJE AADD (Fase 5) ===")
    print("Inyectando patrones arquitectónicos de alta fidelidad en C2...")
    
    memory = C2ExperienceMemory()
    
    # Patrones de Ventanas Inteligentes
    aadd_patterns = [
        {
            "objective": "crear ventana profesional 1.2x1.5",
            "evaluation": {
                "status": "success",
                "score": 95.0,
                "parameters": {"width": 1.2, "height": 1.5, "sill_height": 0.9},
                "metrics_passed": 5,
                "metrics_total": 5,
                "recommendations": ["Usar AADD para corte booleano automático"]
            }
        },
        {
            "objective": "crear muro perimetral 10m",
            "evaluation": {
                "status": "success",
                "score": 98.0,
                "parameters": {"length": 10.0, "thickness": 0.3, "height": 2.5},
                "metrics_passed": 3,
                "metrics_total": 3,
                "recommendations": ["Optimizado para inserción de componentes AADD"]
            }
        },
        {
            "objective": "crear puerta profesional 0.9x2.1",
            "evaluation": {
                "status": "success",
                "score": 92.0,
                "parameters": {"width": 0.9, "height": 2.1},
                "metrics_passed": 4,
                "metrics_total": 4,
                "recommendations": ["Marco en U invertida detectado correctamente"]
            }
        }
    ]
    
    count = 0
    for pattern in aadd_patterns:
        memory.record_experience(pattern["objective"], pattern["evaluation"])
        print(f"✅ Patrón inyectado: {pattern['objective']}")
        count += 1
        
    print(f"\n[SUCCESS] {count} patrones AADD integrados en C2 Memory.")
    print("ZULY ahora priorizará estos componentes profesionales en tareas arquitectónicas.")

if __name__ == "__main__":
    train_aadd()
