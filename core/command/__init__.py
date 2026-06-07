"""
Core Command Module - Puerta de Comandos

Este módulo define la única vía legítima para recibir órdenes externas.
"""

from core.command.command_gate import CommandGate

__all__ = ['CommandGate']
