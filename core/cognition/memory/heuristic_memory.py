"""
heuristic_memory.py

Sistema de persistencia de experiencias técnicas exitosas.
Permite a ZULY "recordar" qué parámetros funcionaron mejor para cada comando.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional


class HeuristicMemory:
    """Gestiona la base de conocimientos empíricos de ZULY"""
    
    def __init__(self, memory_file: str = "core/cognition/memory/experiences.json"):
        self.memory_file = Path(memory_file)
        self.memory_file.parent.mkdir(parents=True, exist_ok=True)
        self.experiences = self._load_memory()
    
    def _load_memory(self) -> Dict[str, Any]:
        """Carga la memoria desde el disco"""
        if self.memory_file.exists():
            try:
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}
    
    def _save_memory(self):
        """Guarda la memoria en el disco"""
        try:
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump(self.experiences, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Error guardando memoria heurística: {e}")

    def store_experience(self, command: str, parameters: Dict[str, Any], score: float, diagnosis: Dict[str, Any]):
        """
        Almacena una nueva experiencia si el score es suficientemente alto.
        
        Args:
            command: Nombre del handler ejecutado
            parameters: Parámetros utilizados
            score: Puntuación de calidad (0.0 a 1.0)
            diagnosis: Diagnóstico completo del evaluador
        """
        # Solo guardamos experiencias con score mayor a 0.7 (calidad técnica alta)
        if score < 0.7:
            return

        timestamp = datetime.now().isoformat()
        
        experience = {
            'timestamp': timestamp,
            'parameters': parameters,
            'score': score,
            'findings': diagnosis.get('findings', [])
        }
        
        if command not in self.experiences:
            self.experiences[command] = []
            
        # Mantener solo las 5 mejores experiencias por comando
        self.experiences[command].append(experience)
        self.experiences[command] = sorted(
            self.experiences[command], 
            key=lambda x: x['score'], 
            reverse=True
        )[:5]
        
        self._save_memory()

    def get_best_parameters(self, command: str) -> Optional[Dict[str, Any]]:
        """Recupera los mejores parámetros conocidos para un comando"""
        if command in self.experiences and self.experiences[command]:
            # Retornar los parámetros de la experiencia con mejor score
            return self.experiences[command][0]['parameters']
        return None

    def get_stats(self) -> Dict[str, int]:
        """Retorna estadísticas simples de la memoria"""
        return {cmd: len(exps) for cmd, exps in self.experiences.items()}
