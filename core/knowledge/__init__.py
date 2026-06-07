"""
core/knowledge/__init__.py

Módulo de Knowledge Graph para LYZU
"""

from .knowledge_graph import (
    KnowledgeGraph,
    Node,
    Relation,
    NodeType,
    RelationType
)

__all__ = [
    'KnowledgeGraph',
    'Node',
    'Relation',
    'NodeType',
    'RelationType'
]
