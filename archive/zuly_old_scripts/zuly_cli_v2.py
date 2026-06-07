#!/usr/bin/env python3
"""
zuly_cli.py

CLI interactivo para ZULY. 

USO:
    python zuly_cli.py
    
    zuly> crear un cubo
    zuly> mover objeto
    zuly> rotar
    zuly> salir
"""

import sys
import os

# FIX: UTF-8 encoding para Windows PowerShell
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

sys.path.insert(0, 'c:\\Users\\Admin\\Desktop\\ZULY_IA_LOCAL')

from core.agent import Agent
from decision_engine import get_decision_engine
from core.utils.logging import log_info, log_success
from core.cognition.c3_task_decomposer import TaskDecomposer
from core.cognition.c3_dependency_graph import DependencyGraph
from core.cognition.c3_scheduler import TaskScheduler
from pathlib import Path


class ZulyCLI:
    """CLI interactivo para Zuly."""
    
    def __init__(self, mock_mode: bool = True):
        """
        Inicializa la CLI.
        
        Args:
            mock_mode: Si True, ejecuta sin Blender (simulado)
        """
        print("\n" + "="*70)
        print("🤖 ZULY CLI - Sistema de Agente Inteligente para Blender")
        print("="*70)
        print("\n⏳ Inicializando agente (versión optimizada)...\n")
        
        # FIX: Lazy loading - solo inicializar si es necesario
        self.agent = None
        self.engine = None
        self.mock_mode = mock_mode
        self._initialized = False
        
        # C3 Decomposer (inicializado siempre, es ligero)
        self.decomposer = TaskDecomposer()
        
        # Mostrar hint rápido
        mode_str = "MOCK MODE (simulado)" if mock_mode else "BLENDER REAL"
        print(f"✓ CLI listo | Modo: {mode_str}\n")
        
        # Ayuda
        self._print_help()
    
    def _ensure_initialized(self):
        """Inicializa el agente solo cuando se necesita (lazy loading)."""
        if self._initialized:
            return
        
        print("\n⏳ Cargando agente inteligente...\n")
        try:
            self.agent = Agent(force_mock=self.mock_mode)
            self.engine = get_decision_engine()
            self._initialized = True
            print("✅ Agente listo\n")
        except Exception as e:
            print(f"❌ Error al inicializar: {e}")
            raise
    
    def _print_help(self):
        """Imprime ayuda de comandos."""
        help_text = """
📋 COMANDOS DISPONIBLES:

  CREAR:
    • crear un cubo / crear cubo / haz un cubo
    • crear una esfera / crear esfera
    • crear cilindro / crear plano / crear cono
    
  TRANSFORMAR:
    • mover objeto / mover cubo
    • rotar objeto / rotar
    • escalar objeto / escalar / cambiar tamaño
    
  ESCENA:
    • limpiar escena / borrar todo
    • eliminar / borrar objeto
    • duplicar / copiar objeto
    
  RENDER:
    • renderizar / renderizar escena / render
    • guardar / save / guardar proyecto
    
  SISTEMA:
    • ayuda / help / ? → muestra esta ayuda
    • estado / info → estado del sistema
    • patrones → lista patrones conocidos
    • salir / exit / quit → cierra CLI

"""
        print(help_text)
    
    def _print_status(self):
        """Imprime estado del sistema."""
        self._ensure_initialized()
        patterns = self.engine.index.patterns
        
        print("\n" + "="*70)
        print("📊 ESTADO DEL SISTEMA ZULY")
        print("="*70)
        print(f"\nPatrones conocidos: {len(patterns)}")
        print(f"Modo: {'MOCK (simulado)' if self.mock_mode else 'BLENDER REAL'}")
        print(f"Decisiones tomadas: {len(self.engine.decision_history)}")
        print(f"Patrones en cache: {len(self.engine.index.patterns)}")
        
        print("\n" + "="*70 + "\n")
    
    def _list_patterns(self):
        """Lista patrones disponibles."""
        self._ensure_initialized()
        patterns = self.engine.index.patterns
        
        print("\n" + "="*70)
        print("📚 PATRONES CONOCIDOS")
        print("="*70 + "\n")
        
        for i, (name, data) in enumerate(patterns.items(), 1):
            handler = data.get("handler", "?")
            tags = ", ".join(data.get("tags", [])[:3])
            print(f"{i:2d}. {name:20s} | {handler:25s} | tags: {tags}")
        
        print("\n" + "="*70 + "\n")
    
    def _is_complex_objective(self, command: str) -> bool:
        """
        Detecta si el comando es un objetivo complejo que requiere descomposición.
        
        Args:
            command: Comando del usuario
            
        Returns:
            True si es objetivo complejo, False si es comando simple
        """
        cmd_lower = command.lower()
        
        # Palabras clave que indican objetivo complejo
        complex_keywords = [
            'completa', 'escena completa', 'proyecto', 
            'arquitect', 'edificio', 'casa', 'interior',
            'visualiz', 'render', 'producto',
            'personaje', 'character', 'laberinto',
            'create scene', 'crea escena'
        ]
        
        return any(kw in cmd_lower for kw in complex_keywords)
    
    def _handle_complex_objective(self, command: str) -> bool:
        """
        Maneja objetivos complejos usando C3 Task Decomposition.
        
        Args:
            command: Objetivo complejo
            
        Returns:
            True para continuar
        """
        print(f"\n📋 OBJETIVO COMPLEJO DETECTADO")
        print("="*70)
        print(f"\nAnalizando: '{command}'")
        print("\n⏳ Generando plan de tareas...\n")
        
        try:
            # Descomponer objetivo
            plan = self.decomposer.decompose(command)
            
            # Mostrar plan
            print(f"✓ Plan generado: {plan.plan_id}")
            print(f"  • Tareas: {len(plan.tasks)}")
            print(f"  • Complejidad: {plan.complexity_score:.0%}")
            print(f"  • Duración estimada: {plan.total_estimated_time_sec/60:.1f} min")
            print(f"  • Grupos parallelizables: {len(plan.parallelizable_groups)}")
            
            # Listar tareas
            print("\n📋 PLAN DE TAREAS:")
            for i, task in enumerate(plan.tasks, 1):
                indent = "  "
                if task.depends_on:
                    indent = "    ↳ "
                print(f"{indent}{i}. {task.name}")
            
            # Construir y validar grafo de dependencias
            graph = DependencyGraph()
            for task in plan.tasks:
                graph.add_task(
                    task_id=task.id,
                    task_name=task.name,
                    duration=task.estimated_time_sec,
                    dependencies=task.depends_on
                )
            
            is_valid, cycle = graph.validate()
            
            if not is_valid:
                print(f"\n❌ ERROR: Ciclo detectado: {' → '.join(cycle)}")
                return True
            
            # Análisis
            critical_path, critical_duration = graph.calculate_critical_path()
            print(f"\n✓ Análisis de dependencias:")
            print(f"  • Duración crítica: {critical_duration/60:.1f} min")
            print(f"  • Tareas críticas: {len(critical_path)}")
            
            # Ejecutar plan
            print(f"\n⏳ Ejecutando plan (dry-run simulado)...")
            scheduler = TaskScheduler()
            report = scheduler.execute_plan(plan, dry_run=True)
            
            print(f"\n✅ PLAN VALIDADO")
            print(f"  • Tareas: {len(plan.tasks)}")
            print(f"  • Estado: {report.overall_status.value}")
            print(f"  • Listo para ejecutar cuando Blender real esté disponible")
            
        except Exception as e:
            print(f"❌ Error al procesar objetivo complejo: {e}")
            import traceback
            traceback.print_exc()
        
        return True
    
    def process_command(self, command: str) -> bool:
        """
        Procesa un comando del usuario.
        
        Args:
            command: Comando ingresado
            
        Returns:
            False si debe salir, True si continuar
        """
        command = command.strip()
        
        if not command:
            return True
        
        # Comandos especiales
        if command.lower() in ['salir', 'exit', 'quit', 'q']:
            return False
        
        if command.lower() in ['ayuda', 'help', '?']:
            self._print_help()
            return True
        
        if command.lower() in ['estado', 'info', 'status']:
            self._print_status()
            return True
        
        if command.lower() in ['patrones', 'patterns', 'list']:
            self._list_patterns()
            return True
        
        # NEW: Detectar objektivos complejos y usar C3
        if self._is_complex_objective(command):
            return self._handle_complex_objective(command)
        
        # Procesar como petición al agente
        self._ensure_initialized()
        print(f"\n⏳ Procesando: '{command}'\n")
        
        try:
            result = self.agent.process_natural_request(command)
            
            # Mostrar resultado
            if result.get('success'):
                print(f"\n✅ ÉXITO")
                print(f"  └─ Comando: {result.get('command_executed')}")
                print(f"  └─ Confianza: {result.get('confidence', 0):.0%}")
            else:
                print(f"\n❌ ERROR")
                print(f"  └─ {result.get('feedback', result.get('error', 'Unknown error'))}")
            
            # Diagnóstico de Validadores para Pruebas
            last_res = result.get('results', [{}])[-1] if result.get('results') else {}
            v0 = last_res.get('validation_v0', {})
            v1 = last_res.get('validation_v1', {})
            

            if v0:
                status = "✓" if v0.get('verified') else "✗"
                print(f"  └─ Validación V0 (Física): {status} {v0.get('details', '')}")
            if v1:
                status = "✓" if v1.get('verified') else "✗"
                print(f"  └─ Validación V1 (Estructural): {status} {v1.get('details', '')}")


            if 'operational_state' in result:
                print(f"  └─ Estado Operativo: {result['operational_state']}")

            feedback = result.get('feedback', '')
            if feedback and feedback != result.get('error'):
                print(f"\n📝 Feedback: {feedback}")
            
        except Exception as e:
            print(f"❌ Excepción: {e}")
            import traceback
            traceback.print_exc()
        
        return True
    
    def run_interactive(self):
        """Ejecuta loop interactivo."""
        print("🔹 Ingresa comandos o 'ayuda' para ver opciones\n")
        
        while True:
            try:
                prompt = "🤖 zuly> "
                command = input(prompt).strip()
                
                if not self.process_command(command):
                    break
                
                print()  # Separador
            
            except KeyboardInterrupt:
                print("\n\n👋 Adiós!\n")
                break
            except EOFError:
                print("\n\n👋 Adiós!\n")
                break
    
    def run_command(self, command: str):
        """Ejecuta un comando único."""
        self.process_command(command)


def main():
    """Punto de entrada."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='ZULY CLI - Agente Inteligente para Blender'
    )
    parser.add_argument(
        '--real',
        action='store_true',
        help='Usar Blender real (por defecto: MOCK mode)'
    )
    parser.add_argument(
        '--command',
        '-c',
        type=str,
        help='Ejecutar comando único y salir'
    )
    
    args = parser.parse_args()
    
    # Crear CLI
    cli = ZulyCLI(mock_mode=not args.real)
    
    # Ejecutar
    if args.command:
        cli.run_command(args.command)
    else:
        cli.run_interactive()


if __name__ == '__main__':
    main()
