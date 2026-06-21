import argparse
import base64
import json
import os
import re
import shutil
import subprocess
import sys
import time
import traceback
from datetime import datetime
from urllib import error, parse, request
from typing import Dict, List, Optional, Any

# Asegurar que la raíz del proyecto esté en sys.path cuando se ejecuta directamente.
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# Importar core de Zuly
try:
    from core.agent import Agent, ExecutionContext
    from core.learning.pattern_memory import PatternMemory
    from core.validation.v0_validator import V0Validator
    from core.environment.blender_observer import BlenderObserver
    CORE_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Advertencia: Core de Zuly no disponible: {e}")
    CORE_AVAILABLE = False
    Agent = None
    PatternMemory = None
    V0Validator = None
    BlenderObserver = None


def llamar_a_gemini(tarea_o_codigo):
    try:
        from tools.ai_agents.gemini_revisor import llamar_a_gemini as _llamar_a_gemini
        return _llamar_a_gemini(tarea_o_codigo)
    except Exception as exc:
        mensaje = f"Error al cargar Gemini: {str(exc)}"
        log_weekend_event(mensaje)
        return mensaje

try:
    from core.external.multi_api_orchestrator import enviar_alerta_telegram, responder_telegram
    TELEGRAM_AVAILABLE = True
except ImportError:
    TELEGRAM_AVAILABLE = False
    def enviar_alerta_telegram(msg): pass
    def responder_telegram(msg): pass


MEMORY_FILE = "/opt/zuly/memory/tutor_memory.json"
WEEKEND_LOG = "/opt/zuly/bitacora/weekend_autorepair.log"
BACKUP_DIR = "/opt/zuly/backups"
MANUAL_OPERATIVO = "/opt/zuly/MANUAL_OPERATIVO.md"
PID_FILE = "/opt/zuly/zuly_tutor.pid"
# Modo simulacro controlable por variable de entorno
MODO_SIMULACRO = os.getenv("ZULY_SIMULACRO", "false").lower() in {"true", "1", "yes"}
AUTO_CYCLE_DELAY = int(os.getenv("ZULY_CYCLE_DELAY", "300"))
PLAN_DE_PRUEBAS = {
    "calibracion": 15,
    "media": 100,
    "masiva": 500,
}

# Variable global para cache de tareas
TASK_DEFINITIONS = {}


def load_task_definitions_dynamic():
    """Carga TASK_DEFINITIONS dinámicamente desde core/commands/ y fallback a tareas básicas."""
    global TASK_DEFINITIONS
    
    # Tareas básicas de fallback
    basic_tasks = {
        "compilar_tutor": {
            "description": "Validar sintaxis de zuly_tutor.py",
            "command": ["python3", "-m", "py_compile", "/opt/zuly/tools/ai_agents/zuly_tutor.py"],
            "target_file": "/opt/zuly/tools/ai_agents/zuly_tutor.py",
        },
        "compilar_revisor": {
            "description": "Validar sintaxis de gemini_revisor.py",
            "command": ["python3", "-m", "py_compile", "/opt/zuly/tools/ai_agents/gemini_revisor.py"],
            "target_file": "/opt/zuly/tools/ai_agents/gemini_revisor.py",
        },
    }
    
    # Intenta cargar del core
    if CORE_AVAILABLE and Agent:
        try:
            agent = Agent()
            if hasattr(agent, 'get_available_commands'):
                core_commands = agent.get_available_commands()
                TASK_DEFINITIONS.update(core_commands)
                print(f"✅ Cargadas {len(core_commands)} tareas del core")
            else:
                print("⚠️  Agent no tiene get_available_commands, usando fallback")
                TASK_DEFINITIONS.update(basic_tasks)
        except Exception as e:
            print(f"⚠️  Error cargando tareas del core: {e}, usando fallback")
            TASK_DEFINITIONS.update(basic_tasks)
    else:
        TASK_DEFINITIONS.update(basic_tasks)
    
    return TASK_DEFINITIONS


def ensure_directory(path):
    if path:
        os.makedirs(path, exist_ok=True)


def load_memory():
    """Carga memoria usando PatternMemory del core si está disponible, sino JSON fallback."""
    ensure_directory(os.path.dirname(MEMORY_FILE))
    
    if CORE_AVAILABLE and PatternMemory:
        try:
            pattern_memory = PatternMemory()
            memoria = pattern_memory.load_all()
            print(f"✅ Memoria cargada desde PatternMemory del core ({len(memoria)} patrones)")
            return memoria
        except Exception as e:
            print(f"⚠️  Error cargando PatternMemory: {e}, usando JSON fallback")
    
    # Fallback a JSON
    if not os.path.exists(MEMORY_FILE):
        return {}
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}


def save_memory(memoria):
    """Guarda memoria usando PatternMemory del core si está disponible, sino JSON fallback."""
    if CORE_AVAILABLE and PatternMemory:
        try:
            pattern_memory = PatternMemory()
            pattern_memory.save_all(memoria)
            print(f"✅ Memoria guardada en PatternMemory del core")
            return
        except Exception as e:
            print(f"⚠️  Error guardando en PatternMemory: {e}, usando JSON fallback")
    
    # Fallback a JSON
    ensure_directory(os.path.dirname(MEMORY_FILE))
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memoria, f, indent=4, ensure_ascii=False)


def log_weekend_event(message):
    ensure_directory(os.path.dirname(WEEKEND_LOG))
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(WEEKEND_LOG, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")


def write_pid_file():
    ensure_directory(os.path.dirname(PID_FILE))
    with open(PID_FILE, "w", encoding="utf-8") as f:
        f.write(str(os.getpid()))
    log_weekend_event(f"PID de Zuly Tutor guardado: {os.getpid()}")


def send_whatsapp(message):
    """Fallback to Telegram due to Twilio removal"""
    if TELEGRAM_AVAILABLE:
        enviar_alerta_telegram(message)
        log_weekend_event(f"Telegram enviado: {message[:50]}...")
        return True
    return False


def actualizar_manual(task_name, issue, solucion, memory):
    header = "# MANUAL OPERATIVO\n\n"
    section_registro = "## Registro de Cambios\n"
    section_memoria = "## Memoria de Patrones\n"
    section_estado = "## Estado del Sistema\n"
    section_emergencia = "## Instrucciones de Emergencia\n"

    ensure_directory(os.path.dirname(MANUAL_OPERATIVO))
    if not os.path.exists(MANUAL_OPERATIVO):
        with open(MANUAL_OPERATIVO, "w", encoding="utf-8") as f:
            f.write(f"{header}{section_registro}\n{section_memoria}\n{section_estado}\n{section_emergencia}\n")

    with open(MANUAL_OPERATIVO, "r", encoding="utf-8") as f:
        content = f.read()

    parts = re.split(r"(?m)^## ", content)
    registro_actual = ""
    if len(parts) >= 2 and parts[1].startswith("Registro de Cambios"):
        registro_actual = parts[1].split("## ", 1)[0].strip()
        registro_actual = registro_actual.replace("Registro de Cambios\n", "")

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    issue_sanitizado = issue.strip().replace("\n", " ")
    solucion_sanitizada = solucion.strip().replace("\n", " ")
    nueva_entrada = (
        f"- **{timestamp}** | Tarea: {task_name} | Qué falló: {issue_sanitizado} | "
        f"Cómo se reparó: {solucion_sanitizada}\n"
    )
    registro_actual = f"{registro_actual}\n{nueva_entrada}".strip()

    memoria_items = []
    for count, key in enumerate(memory.keys()):
        if count >= 10:
            break
        memoria_items.append(f"- {key}")
    memoria_texto = "\n".join(memoria_items) if memoria_items else "- Ningún patrón registrado."

    estado_texto = f"- MODO_SIMULACRO: {'ACTIVO' if MODO_SIMULACRO else 'DESACTIVADO'}\n"

    emergencia_texto = (
        "1. Revisar backups en /opt/zuly/backups/\n"
        "2. Restaurar el archivo original desde el backup correspondiente.\n"
        "3. Volver a ejecutar la tarea fallida.\n"
        "4. Si el problema persiste, restaurar el último backup completo y analizar fuera de línea.\n"
    )

    with open(MANUAL_OPERATIVO, "w", encoding="utf-8") as f:
        f.write(header)
        f.write(section_registro)
        f.write(registro_actual + "\n\n")
        f.write(section_memoria)
        f.write(memoria_texto + "\n\n")
        f.write(section_estado)
        f.write(estado_texto + "\n")
        f.write(section_emergencia)
        f.write(emergencia_texto)


def actualizar_manual_fase(nombre_fase, total_pruebas, fallos, reparadas, memory):
    issue = f"Fase {nombre_fase} ejecutada."
    solucion = f"Resumen: {total_pruebas} pruebas, {fallos} fallos, {reparadas} reparaciones automáticas."
    actualizar_manual(f"Fase {nombre_fase}", issue, solucion, memory)


def get_stack_trace():
    return traceback.format_exc()


def summarize_memory(memory, limit=5):
    if not memory:
        return "Memoria vacía."

    summary = {}
    for count, (key, value) in enumerate(memory.items()):
        if count >= limit:
            break
        summary[key] = value
    return json.dumps(summary, indent=2, ensure_ascii=False)


def extract_json_object(text):
    start_indexes = [m.start() for m in re.finditer(r"\{", text)]
    for start in start_indexes:
        depth = 0
        for idx in range(start, len(text)):
            if text[idx] == "{":
                depth += 1
            elif text[idx] == "}":
                depth -= 1
                if depth == 0:
                    candidate = text[start:idx + 1]
                    try:
                        return json.loads(candidate)
                    except json.JSONDecodeError:
                        continue
    return None


def propose_correction(task_name, target_file, stack_trace, memory):
    memory_summary = summarize_memory(memory)
    prompt = (
        "Eres un revisor experto en arquitectura BIM, modelado 3D y corrección de código. "
        "Tienes acceso a una memoria de patrones y debes generar un parche inmediato para un fallo detectado.\n\n"
        f"Tarea fallida: {task_name}\n"
        f"Archivo objetivo: {target_file}\n\n"
        "Traza de error:\n"
        f"{stack_trace}\n\n"
        "Contexto de memoria relevante (solo los primeros patrones):\n"
        f"{memory_summary}\n\n"
        "Devuelve SOLO un objeto JSON válido con estas claves:"
        " file_path, replacement_code, explanation. "
        "El campo replacement_code debe contener el código completo corregido para el archivo objetivo."
    )

    response = llamar_a_gemini(prompt)
    patch = extract_json_object(response)
    if patch and patch.get("file_path") and patch.get("replacement_code"):
        return patch
    return None


def preparar_backup(ruta_archivo):
    ruta_archivo = os.path.abspath(ruta_archivo)
    if not os.path.exists(ruta_archivo):
        return None

    ensure_directory(BACKUP_DIR)
    nombre = os.path.basename(ruta_archivo)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(BACKUP_DIR, f"{nombre}.{timestamp}.bak")
    shutil.copy2(ruta_archivo, backup_path)
    return backup_path


def apply_patch(patch, modo_simulacro=None):
    file_path = patch.get("file_path")
    replacement_code = patch.get("replacement_code") or patch.get("corrected_code")
    if not file_path or not replacement_code:
        return False

    file_path = os.path.abspath(file_path)
    ensure_directory(os.path.dirname(file_path))

    if modo_simulacro is None:
        modo_simulacro = MODO_SIMULACRO

    if modo_simulacro:
        log_weekend_event(
            f"Modo simulacro activo. Parche propuesto para {file_path}:\n{replacement_code}"
        )
        print("Modo simulacro activo: no se aplicó el parche. Consulta weekend_autorepair.log para ver la propuesta.")
        return False

    backup_path = preparar_backup(file_path)
    if backup_path:
        log_weekend_event(f"Backup creado: {backup_path}")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(replacement_code)

    log_weekend_event(f"Parche aplicado a {file_path}")
    return True


def run_command(command):
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip())
    return result


def execute_task(task_name, memory, modo_simulacro=None):
    task = TASK_DEFINITIONS.get(task_name)
    if not task:
        print(f"Tarea desconocida: {task_name}. Usa 'tasks' para ver las disponibles.")
        return {"success": False, "repaired": False}

    print(f"Ejecutando tarea: {task_name} - {task['description']}")
    try:
        run_command(task["command"])
        print("Tarea completada sin errores.")
        return {"success": True, "repaired": False}
    except Exception:
        stack_trace = get_stack_trace()
        print("Error detectado durante la ejecución de la tarea. Iniciando autorreparación...")
        patch = propose_correction(task_name, task["target_file"], stack_trace, memory)

        if patch:
            if modo_simulacro is None:
                modo_simulacro = MODO_SIMULACRO
            if modo_simulacro:
                log_weekend_event("Corrección simulada: se generó una propuesta pero no se aplicó.")
                print("Corrección simulada. No se aplica parche en modo simulacro.")
                return {"success": False, "repaired": False, "simulated": True}

            if apply_patch(patch, modo_simulacro=modo_simulacro):
                print("Parche aplicado. Re-ejecutando la tarea una sola vez...")
                try:
                    run_command(task["command"])
                    log_weekend_event("Corrección exitosa")
                    actualizar_manual(task_name, stack_trace, patch.get("explanation", "Corrección aplicada automáticamente."), memory)
                    print("Corrección exitosa.")
                    return {"success": True, "repaired": True}
                except Exception:
                    log_weekend_event("Error crítico persistente")
                    send_whatsapp(f"ALERTA: Zuly no pudo reparar automáticamente la tarea {task_name}.")
                    print("Error crítico persistente después de la re-ejecución.")
                    return {"success": False, "repaired": False}

        log_weekend_event("Error crítico persistente")
        send_whatsapp(f"ALERTA: Zuly no pudo corregir automáticamente la tarea {task_name}.")
        print("No fue posible generar o aplicar la corrección automática.")
        return {"success": False, "repaired": False}


def sesion_de_estudio(memory):
    temas = ["Cálculo de cargas en columnas", "Normativa de escaleras", "Optimización de malla BIM"]
    for tema in temas:
        print(f"Zuly estudiando: {tema}...")
        leccion = llamar_a_gemini(f"Explícale a un agente de modelado BIM cómo aplicar {tema} de forma eficiente.")
        memory[f"aprendizaje_{tema}"] = leccion

    save_memory(memory)
    print("¡Sesión de estudio finalizada! Zuly ha guardado los nuevos conocimientos.")
    return memory


def ejecutar_fase(nombre_fase, memory, modo_simulacro_override=None):
    fase = nombre_fase.lower()
    cantidad = PLAN_DE_PRUEBAS.get(fase)
    if cantidad is None:
        print(f"Fase desconocida: {nombre_fase}. Usa calibracion, media o masiva.")
        return

    if modo_simulacro_override is None:
        modo_simulacro_fase = fase == "calibracion"
    else:
        modo_simulacro_fase = modo_simulacro_override

    print(f"Iniciando fase '{fase}' con {cantidad} pruebas. Modo simulacro: {'ACTIVO' if modo_simulacro_fase else 'DESACTIVADO'}.")

    total_pruebas = 0
    fallos = 0
    reparadas = 0

    for i in range(1, cantidad + 1):
        print(f"\n[Prueba {i}/{cantidad}] Ejecutando prueba base...")
        result = execute_task("compilar_tutor", memory, modo_simulacro=modo_simulacro_fase)
        total_pruebas += 1
        if not result.get("success"):
            fallos += 1
        if result.get("repaired"):
            reparadas += 1

    resumen = (
        f"Fase '{fase}' completada. Total: {total_pruebas}, Fallos: {fallos}, Reparadas: {reparadas}."
    )
    print(resumen)
    actualizar_manual_fase(fase, total_pruebas, fallos, reparadas, memory)


def run_autonomous_cycle(memory, delay_seconds=AUTO_CYCLE_DELAY, max_iterations=None):
    print("Iniciando modo autónomo de Zuly. El agente trabajará en ciclos continuos.")
    print(f"⏱️  Delay entre ciclos: {delay_seconds}s | Max iteraciones: {max_iterations if max_iterations else 'infinito'}")
    print("💡 Presiona Enter para siguiente ciclo, o escribe 'exit' para salir.\n")
    log_weekend_event("Modo autónomo activado.")
    cycle = 0
    try:
        while True:
            cycle += 1
            log_weekend_event(f"Ciclo autónomo #{cycle} iniciado.")
            print(f"\n[Ciclo {cycle}] Estudiando y validando sistema...")

            if cycle % 2 == 1:
                memory = sesion_de_estudio(memory)
            else:
                ejecutar_fase("calibracion", memory, modo_simulacro_override=False)

            if max_iterations and cycle >= max_iterations:
                print(f"\n✅ Se alcanzó el límite de {max_iterations} ciclos autónomos.")
                break

            print(f"\n⏳ Esperando {delay_seconds} segundos...")
            try:
                # Intenta leer entrada con timeout usando input no bloqueante
                # En Python puro, input() siempre bloquea, pero mostramos la opción
                user_input = input(f"[Ciclo {cycle}] Presiona Enter para continuar o escribe 'exit': ").strip().lower()
                if user_input in {"exit", "q", "salir", "quit"}:
                    print("\n👋 Ciclo autónomo detenido por el usuario.")
                    break
            except EOFError:
                # Si no hay entrada interactiva (en cron/systemd), solo espera
                print(f"⏳ Esperando {delay_seconds}s (modo no-interactivo)...")
                time.sleep(delay_seconds)
                continue
    except KeyboardInterrupt:
        print("\n⚠️  Modo autónomo detenido por Ctrl+C.")
        log_weekend_event("Modo autónomo detenido por Ctrl+C.")
    return memory


def interactive_loop(memory):
    print("Modo interactivo de Zuly iniciado. Usa 'tasks' para ver tareas, 'run <tarea>' para ejecutarlas, 'fase <calibracion|media|masiva>' para ejecutar fases, 'notificar <texto>' para WhatsApp, 'study' para estudiar y 'exit' para salir.")
    while True:
        try:
            comando = input("Zuly > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nSaliendo de la sesión interactiva de Zuly.")
            break

        if not comando:
            continue
        comando_lower = comando.lower()
        if comando_lower in {"exit", "salir", "quit", "q"}:
            print("Saliendo de la sesión interactiva de Zuly.")
            break
        if comando_lower == "tasks":
            print("Tareas disponibles:")
            for name, info in TASK_DEFINITIONS.items():
                print(f"  - {name}: {info['description']}")
            continue
        if comando_lower.startswith("run "):
            _, task_name = comando.split(" ", 1)
            execute_task(task_name.strip(), memory)
            continue
        if comando_lower.startswith("ejecutar_fase ") or comando_lower.startswith("fase "):
            _, fase = comando.split(" ", 1)
            ejecutar_fase(fase.strip(), memory)
            continue
        if comando_lower in {"calibracion", "media", "masiva"}:
            ejecutar_fase(comando_lower, memory)
            continue
        if comando_lower.startswith("notificar ") or comando_lower.startswith("whatsapp "):
            _, texto = comando.split(" ", 1)
            if send_whatsapp(texto.strip()):
                print("Nota enviada por WhatsApp.")
            else:
                print("No se pudo enviar la nota por WhatsApp. Revisa el log.")
            continue
        if comando_lower == "study":
            memory = sesion_de_estudio(memory)
            continue
        print("Comando no reconocido. Usa 'tasks', 'run <tarea>', 'fase <calibracion|media|masiva>', 'notificar <texto>', 'study' o 'exit'.")


def main():
    parser = argparse.ArgumentParser(description="Zuly Tutor con autorreparación basada en revisor.")
    parser.add_argument("--reparar-y-tutelar", action="store_true", help="Activar modo de reparación y tutoría interactiva.")
    parser.add_argument("--auto-cycle", action="store_true", help="Activar modo autónomo de ciclos continuos.")
    parser.add_argument("--auto-delay", type=int, default=AUTO_CYCLE_DELAY, help="Segundos de espera entre ciclos autónomos.")
    parser.add_argument("--max-iterations", type=int, default=None, help="Número máximo de ciclos autónomos.")
    parser.add_argument("--fase", choices=["calibracion", "media", "masiva"], help="Ejecutar directamente una fase de pruebas sin interacción adicional.")
    parser.add_argument("--study", action="store_true", help="Forzar ejecución de sesión de estudio antes de continuar.")
    parser.add_argument("--test-whatsapp", action="store_true", help="Enviar un mensaje de prueba por WhatsApp y salir.")
    parser.add_argument("--simulacro", dest="modo_simulacro", action="store_true", help="Forzar modo simulacro para la ejecución de fase.")
    parser.add_argument("--no-simulacro", dest="modo_simulacro", action="store_false", help="Forzar desactivación de modo simulacro para la ejecución de fase.")
    parser.set_defaults(modo_simulacro=None)
    args = parser.parse_args()

    memoria = load_memory()
    write_pid_file()
    log_weekend_event(f"Inicio de Zuly Tutor con argumentos: {sys.argv[1:]}")

    if args.test_whatsapp:
        if send_whatsapp("Prueba de WhatsApp: este es el primer mensaje de Zuly."):
            print("Mensaje de prueba enviado.")
        else:
            print("No se pudo enviar el mensaje de prueba. Revisa el log de Twilio.")
        return

    send_whatsapp(f"Zuly Tutor ha iniciado en la VM con argumentos: {sys.argv[1:]}")

    if args.study:
        memoria = sesion_de_estudio(memoria)

    if args.fase:
        ejecutar_fase(args.fase, memoria, modo_simulacro_override=args.modo_simulacro)
    elif args.auto_cycle:
        memoria = run_autonomous_cycle(memoria, delay_seconds=args.auto_delay, max_iterations=args.max_iterations)
    elif args.reparar_y_tutelar:
        interactive_loop(memoria)
    elif args.study:
        print("Sesión de estudio completada. No se seleccionó fase ni modo interactivo.")
    else:
        print("No se seleccionó modo de ejecución. Usa --reparar-y-tutelar, --auto-cycle o --fase <calibracion|media|masiva>.")

    log_weekend_event("Finalización de Zuly Tutor: el proceso ha terminado.")
    send_whatsapp("Zuly Tutor ha finalizado. Revisa la bitácora en la VM para más detalles.")
    print("Zuly Tutor ha finalizado. Revisa bitacora/weekend_autorepair.log para confirmación.")


if __name__ == "__main__":
    main()
