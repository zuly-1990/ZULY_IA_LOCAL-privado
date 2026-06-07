# Consequence Memory

"""Memory layer for ZULY to store and recall action outcomes.

This module manages the historical record of consequences from observed actions.
It provides simple storage, retrieval, and counting of results. No inferences
or decisions are made here.
"""

import json
import os
import datetime
from typing import Dict, List, Any

MEMORY_FILE = "logs/consequence_memory.json"

def _load_memory() -> List[Dict[str, Any]]:
    """Load consequences from JSON file."""
    if not os.path.exists(MEMORY_FILE):
        return []
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

def _save_memory(memory: List[Dict[str, Any]]):
    """Save consequences to JSON file."""
    os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2, ensure_ascii=False)

def store_consequence(observation_report: Dict[str, Any]):
    """Store the consequence of an action based on an observation report.
    
    Fields stored:
    - accion
    - parametros (if available)
    - estado (COHERENTE, etc.)
    - timestamp
    """
    memory = _load_memory()
    
    consequence = {
        "accion": observation_report.get("accion", "unknown"),
        "parametros": observation_report.get("parametros", {}), # Optional
        "estado": observation_report.get("estado", "unknown"),
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    memory.append(consequence)
    _save_memory(memory)

def query_consequences(accion: str) -> Dict[str, Any]:
    """Retrieve historical counts for a specific action.
    
    Returns a summary of how many times each state occurred.
    """
    memory = _load_memory()
    relevant = [c for c in memory if c["accion"] == accion]
    
    # Initialize counts
    counts = {
        "COHERENTE": 0,
        "FALLO_DE_CONTEXTO": 0,
        "INCONSISTENTE": 0
    }
    
    for c in relevant:
        estado = c.get("estado")
        if estado in counts:
            counts[estado] += 1
            
    return {
        "accion": accion,
        "resumen": counts,
        "total_experiencias": len(relevant)
    }

def get_history(accion: str) -> List[Dict[str, Any]]:
    """Retrieve the full raw history for a specific action."""
    memory = _load_memory()
    return [c for c in memory if c["accion"] == accion]
