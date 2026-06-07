#!/usr/bin/env python3
"""
ZULY CLI INTERACTIVO - Opción 2
Interfaz de línea de comandos para LYZU con lenguaje natural

Uso:
  python zuly_cli_interactive.py
  > crear un cubo
  > crear esfera y rotarla 45 grados
  > crear arquitectura
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Tuple


class ZULYNLParser:
    """Parser de lenguaje natural español a acciones LYZU"""
    
    ACTION_MAP = {
        "cubo": {"action": "create_cube", "params": {}},
        "esfera": {"action": "create_sphere", "params": {}},
        "cilindro": {"action": "create_cylinder", "params": {}},
        "cono": {"action": "create_cone", "params": {}},
        "mover": {"action": "move_object", "params": {"location": [5, 0, 0]}},
        "rotar": {"action": "rotate_object", "params": {"rotation": [0, 0, 45]}},
        "escalar": {"action": "scale_object", "params": {"scale": 1.5}},
        "renderiza": {"action": "render_scene", "params": {}},
        "información": {"action": "get_info", "params": {}},
    }
    
    @staticmethod
    def parse(instruction: str) -> Tuple[List[Dict], float]:
        """
        Convierte instrucción en lenguaje natural a acciones LYZU
        
        Returns:
            (lista_de_acciones, confianza_float)
        """
        instruction = instruction.lower().strip()
        actions = []
        confidence = 1.0
        
        # Separar por conectores
        commands = instruction.replace(" y ", "|").replace(" luego ", "|").split("|")
        
        for cmd in commands:
            cmd = cmd.strip()
            if not cmd:
                continue
            
            action_found = False
            
            # Buscar en ACTION_MAP
            for keyword, info in ZULYNLParser.ACTION_MAP.items():
                if keyword in cmd:
                    params = ZULYNLParser._extract_params(cmd, info)
                    actions.append({
                        "action": info["action"],
                        "parameters": params,
                        "intent": cmd
                    })
                    action_found = True
                    confidence *= 0.95
                    break
            
            if not action_found:
                # Casos especiales
                if "arquitectura" in cmd or "villa" in cmd or "savoye" in cmd:
                    actions.append({
                        "action": "create_scene_villa_savoye",
                        "parameters": {"style": "villa_savoye"},
                        "intent": cmd
                    })
                    confidence *= 0.80
                else:
                    confidence *= 0.5
        
        confidence = max(0.0, min(1.0, confidence))
        return actions, confidence
    
    @staticmethod
    def _extract_params(cmd: str, action_info: Dict) -> Dict:
        """Extrae parámetros numéricos"""
        params = action_info["params"].copy()
        
        # Números
        tokens = cmd.split()
        for token in tokens:
            clean = token.rstrip("º°grados.").replace("grados", "")
            
            if clean.isdigit():
                num = int(clean)
                if "rotar" in cmd or "rotación" in cmd:
                    params["rotation"] = [0, 0, num]
                elif "escala" in cmd:
                    params["scale"] = num / 10.0 if num > 10 else (num * 0.1)
                elif "mover" in cmd:
                    params["location"] = [num, 0, 0]
        
        return params


class ZULYExecutor:
    """Ejecuta acciones en Blender"""
    
    def __init__(self):
        self.script_dir = Path(__file__).parent
        self.blender_exe = self.script_dir / "blender/v3/blender-3.6.0-zuly/blender.exe"
        self.executed = 0
        self.successful = 0
    
    def execute(self, actions: List[Dict]) -> Dict[str, Any]:
        """Ejecuta lista de acciones"""
        
        if not actions:
            return {"status": "error", "message": "Sin acciones", "objects": 0}
        
        # Generar script
        script = self._generate_script(actions)
        
        # Ejecutar
        return self._run_blender(script)
    
    def _generate_script(self, actions: List[Dict]) -> str:
        """Genera script Python para Blender"""
        
        code = [
            "import bpy",
            "import json",
            "import math",
            "",
            "results = {'status': 'success', 'commands': [], 'objects': 0}",
            "",
        ]
        
        for action in actions:
            name = action.get("action", "")
            params = action.get("parameters", {})
            
            if name == "create_cube":
                code.extend([
                    "try:",
                    "    bpy.ops.mesh.primitive_cube_add(size=2)",
                    "    results['objects'] += 1",
                    "    results['commands'].append({'action': 'create_cube', 'status': 'ok'})",
                    "except Exception as e:",
                    "    results['commands'].append({'action': 'create_cube', 'status': 'error'})",
                    "",
                ])
            
            elif name == "create_sphere":
                code.extend([
                    "try:",
                    "    bpy.ops.mesh.primitive_uv_sphere_add(radius=1)",
                    "    results['objects'] += 1",
                    "    results['commands'].append({'action': 'create_sphere', 'status': 'ok'})",
                    "except Exception as e:",
                    "    results['commands'].append({'action': 'create_sphere', 'status': 'error'})",
                    "",
                ])
            
            elif name == "rotate_object":
                rot = params.get("rotation", [0, 0, 45])
                code.extend([
                    "try:",
                    "    obj = bpy.context.active_object",
                    "    if obj:",
                    f"        obj.rotation_euler = ({rot[0]*3.14159/180}, {rot[1]*3.14159/180}, {rot[2]*3.14159/180})",
                    "    results['commands'].append({'action': 'rotate_object', 'status': 'ok'})",
                    "except Exception as e:",
                    "    results['commands'].append({'action': 'rotate_object', 'status': 'error'})",
                    "",
                ])
            
            elif name == "scale_object":
                scale = params.get("scale", 1.5)
                code.extend([
                    "try:",
                    "    obj = bpy.context.active_object",
                    "    if obj:",
                    f"        obj.scale = ({scale}, {scale}, {scale})",
                    "    results['commands'].append({'action': 'scale_object', 'status': 'ok'})",
                    "except Exception as e:",
                    "    results['commands'].append({'action': 'scale_object', 'status': 'error'})",
                    "",
                ])
            
            elif name == "create_scene_villa_savoye":
                code.extend([
                    "try:",
                    "    # Base",
                    "    bpy.ops.mesh.primitive_cube_add(size=8, location=(0,0,0))",
                    "    bpy.ops.mesh.primitive_cube_add(size=6, location=(2,2,4))",
                    "    results['objects'] += 2",
                    "    results['commands'].append({'action': 'villa_savoye', 'status': 'ok'})",
                    "except Exception as e:",
                    "    results['commands'].append({'action': 'villa_savoye', 'status': 'error'})",
                    "",
                ])
        
        # Guardar resultado
        code.extend([
            "with open('zuly_result.json', 'w') as f:",
            "    json.dump(results, f)",
            "print('ZULY_RESULT:' + json.dumps(results))",
        ])
        
        return "\n".join(code)
    
    def _run_blender(self, script: str) -> Dict[str, Any]:
        """Ejecuta Blender con script"""
        
        script_file = self.script_dir / "temp_zuly_script.py"
        
        try:
            # Guardar script
            with open(script_file, "w") as f:
                f.write(script)
            
            # Ejecutar Blender
            cmd = [
                str(self.blender_exe),
                "--background",
                "--python", str(script_file)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            # Parsear resultado
            try:
                if Path("zuly_result.json").exists():
                    with open("zuly_result.json") as f:
                        data = json.load(f)
                    self.executed += 1
                    if data.get("status") == "success":
                        self.successful += 1
                    return data
            except:
                pass
            
            return {"status": "error", "message": "No se procesó", "objects": 0}
        
        except Exception as e:
            return {"status": "error", "message": str(e), "objects": 0}
        
        finally:
            if script_file.exists():
                script_file.unlink()


def main():
    """Modo interactivo"""
    
    print("\n" + "=" * 70)
    print("  ZULY CLI INTERACTIVO v2.0")
    print("  Escribe comandos en español natural")
    print("=" * 70)
    print("\nEjemplos:")
    print("  > crear un cubo")
    print("  > crear esfera y rotar 45 grados")
    print("  > crear arquitectura")
    print("  > exit para salir")
    print("\n" + "=" * 70 + "\n")
    
    parser = ZULYNLParser()
    executor = ZULYExecutor()
    
    while True:
        try:
            instruction = input("zuly> ").strip()
            
            if not instruction:
                continue
            
            if instruction.lower() in ["exit", "quit", "salir"]:
                print("\n👋 Hasta luego!")
                break
            
            # Parsear
            actions, confidence = parser.parse(instruction)
            
            if not actions:
                print("❌ No entendí el comando")
                continue
            
            print(f"\n📋 Acciones: {len(actions)} | Confianza: {confidence:.1%}")
            for action in actions:
                print(f"   • {action['action']}")
            
            if confidence < 0.3:
                print("⚠️  Confianza muy baja, cancelando")
                continue
            
            # Ejecutar
            print("\n⚙️  Ejecutando...")
            result = executor.execute(actions)
            
            if result.get("status") == "success":
                print(f"✅ Completado: {result.get('objects', 0)} objetos creados")
            else:
                print(f"❌ Error: {result.get('message', 'Desconocido')}")
            
            print(f"   [Estadísticas] Ejecutados: {executor.executed}, Exitosos: {executor.successful}\n")
        
        except KeyboardInterrupt:
            print("\n👋 Hasta luego!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            print()


if __name__ == "__main__":
    main()
