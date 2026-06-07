"""
Knowledge Intake Package

Sistema de ingesta de conocimiento crudo.
"""

from extensions.knowledge_intake.intake_v1 import IntakeV1
from extensions.knowledge_intake.schema import KnowledgeSchema

__all__ = ['IntakeV1', 'KnowledgeSchema']
