#!/usr/bin/env python3
"""
ZULY CLI - Interfaz de línea de comandos interactiva
Opción 2: CLI No-Code para LYZU

Permite interactuar con LYZU usando lenguaje natural:
  zuly "crear un cubo"
  zuly "crear una esfera y rotarla 45 grados"
  zuly "crear arquitectura"
"""

import os
import sys
import json
import click
import subprocess
from typing import Tuple, List, Dict, Any
from pathlib import Path
from datetime import datetime
from core.agent import Agent

# Configuración de paths
SCRIPT_DIR = Path(__file__).parent
ZULY_LAB = SCRIPT_DIR / "ZULY_LAB"
BLENDER_EXE = Path(r"blender\v3\blender-3.6.0-zuly\blender.exe")

class ZULYCommandParser:
    """Parser de comandos de lenguaje natural a acciones LYZU"""
    
    # Mapa de palabras clave en español a acciones LYZU
    ACTION_MAP = {
        # Primitivas básicas
        "cubo": {"action": "create_cube", "args": {}},
        "cubos": {"action": "create_cube", "args": {}},
        "caja": {"action": "create_cube", "args": {}},
        "cajas": {"action": "create_cube", "args": {}},
        "esfera": {"action": "create_sphere", "args": {}},
        "esferas": {"action": "create_sphere", "args": {}},
        "bola": {"action": "create_sphere", "args": {}},
        "bolas": {"action": "create_sphere", "args": {}},
        "cilindro": {"action": "create_cylinder", "args": {}},
        "cilindros": {"action": "create_cylinder", "args": {}},
        "tubo": {"action": "create_cylinder", "args": {}},
        "tubos": {"action": "create_cylinder", "args": {}},
        "plano": {"action": "create_plane", "args": {}},
        "planos": {"action": "create_plane", "args": {}},
        "cono": {"action": "create_cone", "args": {}},
        "conos": {"action": "create_cone", "args": {}},
        "piramide": {"action": "create_cone", "args": {}},
        "piramides": {"action": "create_cone", "args": {}},
        "torus": {"action": "create_torus", "args": {}},
        "toroides": {"action": "create_torus", "args": {}},
        "dona": {"action": "create_torus", "args": {}},
        "suzanne": {"action": "create_monkey", "args": {}},
        "mona": {"action": "create_monkey", "args": {}},
        "mono": {"action": "create_monkey", "args": {}},
        
        # Agujeros y perforaciones
        "agujero": {"action": "create_hollow_primitive", "args": {}},
        "agujeros": {"action": "create_hollow_primitive", "args": {}},
        "hueco": {"action": "create_hollow_primitive", "args": {}},
        "huecos": {"action": "create_hollow_primitive", "args": {}},
        "perforado": {"action": "create_hollow_primitive", "args": {}},
        "perforar": {"action": "create_hollow_primitive", "args": {}},
        "perfora": {"action": "create_hollow_primitive", "args": {}},
        "tallar": {"action": "create_hollow_primitive", "args": {}},
        "cavar": {"action": "create_hollow_primitive", "args": {}},
        "excavar": {"action": "create_hollow_primitive", "args": {}},
        "hacer agujero": {"action": "create_hollow_primitive", "args": {}},
        "haz agujero": {"action": "create_hollow_primitive", "args": {}},
        "crea agujero": {"action": "create_hollow_primitive", "args": {}},
        
        # Transformaciones
        "mover": {"action": "move_object", "args": {"offset": [5, 0, 0]}},
        "mueve": {"action": "move_object", "args": {"offset": [5, 0, 0]}},
        "desplazar": {"action": "move_object", "args": {"offset": [5, 0, 0]}},
        "desplaza": {"action": "move_object", "args": {"offset": [5, 0, 0]}},
        "trasladar": {"action": "move_object", "args": {"offset": [5, 0, 0]}},
        "traslada": {"action": "move_object", "args": {"offset": [5, 0, 0]}},
        "rotar": {"action": "rotate_object", "args": {"rotation": [0, 0, 45]}},
        "rota": {"action": "rotate_object", "args": {"rotation": [0, 0, 45]}},
        "girar": {"action": "rotate_object", "args": {"rotation": [0, 0, 45]}},
        "gira": {"action": "rotate_object", "args": {"rotation": [0, 0, 45]}},
        "voltear": {"action": "rotate_object", "args": {"rotation": [0, 0, 45]}},
        "escalar": {"action": "scale_object", "args": {"scale": 1.5}},
        "escala": {"action": "scale_object", "args": {"scale": 1.5}},
        "tamaño": {"action": "scale_object", "args": {"scale": 1.5}},
        "grande": {"action": "scale_object", "args": {"scale": 2.0}},
        "pequeño": {"action": "scale_object", "args": {"scale": 0.5}},
        "redimensionar": {"action": "scale_object", "args": {"scale": 1.5}},
        
        # Sistema
        "renderizar": {"action": "render", "args": {}},
        "render": {"action": "render", "args": {}},
        "dibujar": {"action": "render", "args": {}},
        "obtener": {"action": "get_info", "args": {}},
        "info": {"action": "get_info", "args": {}},
        "información": {"action": "get_info", "args": {}},
        "guardar": {"action": "save", "args": {}},
        "salvar": {"action": "save", "args": {}},
        "exportar": {"action": "export", "args": {}},
        "limpiar": {"action": "clear_scene", "args": {}},
        "borrar": {"action": "clear_scene", "args": {}},
        "nuevo": {"action": "clear_scene", "args": {}},
        
        # Ejes específicos
        "eje x": {"action": "axis_x", "args": {}},
        "eje y": {"action": "axis_y", "args": {}},
        "eje z": {"action": "axis_z", "args": {}},
        "horizontal": {"action": "axis_x", "args": {}},
        "vertical": {"action": "axis_y", "args": {}},
        "profundidad": {"action": "axis_z", "args": {}},
    }
    
    # Colores reconocidos
    COLOR_MAP = {
        "rojo": [1.0, 0.0, 0.0],
        "roja": [1.0, 0.0, 0.0],
        "azul": [0.0, 0.0, 1.0],
        "verde": [0.0, 1.0, 0.0],
        "amarillo": [1.0, 1.0, 0.0],
        "naranja": [1.0, 0.5, 0.0],
        "naranja": [1.0, 0.5, 0.0],
        "morado": [0.5, 0.0, 1.0],
        "morada": [0.5, 0.0, 1.0],
        "rosa": [1.0, 0.0, 1.0],
        "blanco": [1.0, 1.0, 1.0],
        "blanca": [1.0, 1.0, 1.0],
        "negro": [0.0, 0.0, 0.0],
        "negra": [0.0, 0.0, 0.0],
        "gris": [0.5, 0.5, 0.5],
        "cyan": [0.0, 1.0, 1.0],
        "cian": [0.0, 1.0, 1.0],
        "magenta": [1.0, 0.0, 1.0],
        "dorado": [1.0, 0.84, 0.0],
        "plateado": [0.75, 0.75, 0.75],
        "marron": [0.6, 0.3, 0.0],
        "café": [0.6, 0.3, 0.0],
        "marrón": [0.6, 0.3, 0.0],
    }
    
    # Palabras auxiliares y numéricos
    NUMERIC_WORDS = {
        "uno": 1, "dos": 2, "tres": 3, "cuatro": 4, "cinco": 5,
        "seis": 6, "siete": 7, "ocho": 8, "nueve": 9, "diez": 10,
        "45": 45, "90": 90, "180": 180, "360": 360,
    }
    
    @staticmethod
    def parse_command(instruction: str) -> Tuple[List[Dict], float]:
        """
        Convierte instrucción en lenguaje natural a lista de acciones LYZU
        
        Args:
            instruction: Ej: "crear un cubo y rotarlo 45 grados"
        
        Returns:
            (acciones_lista, confianza_score)
        """
        instruction_lower = instruction.lower().strip()
        actions = []
        confidence = 1.0
        
        # Palabras clave para split
        separators = [" y ", " luego ", " después "]
        commands = [instruction_lower]
        for sep in separators:
            temp = []
            for cmd in commands:
                if sep in cmd:
                    temp.extend(cmd.split(sep))
                else:
                    temp.append(cmd)
            commands = temp
        
        # Procesar cada comando
        for cmd in commands:
            cmd = cmd.strip()
            if not cmd:
                continue
            
            action_found = False
            
            # Buscar acciones en el mapa
            for keyword, action_info in ZULYCommandParser.ACTION_MAP.items():
                if keyword in cmd:
                    action = {
                        "action": action_info["action"],
                        "parameters": ZULYCommandParser._extract_parameters(cmd, action_info, keyword),
                        "intent": cmd,
                        "original": cmd
                    }
                    actions.append(action)
                    action_found = True
                    confidence *= 0.95  # Reducir confianza por cada acción
                    break
            
            if not action_found:
                # Si no encuentra acción exacta, podría ser parámetro
                if "arquitectura" in cmd or "villa" in cmd or "savoye" in cmd:
                    # Comando especial para arquitectura
                    actions.append({
                        "action": "create_architectural_scene",
                        "parameters": {"style": "villa_savoye"},
                        "intent": cmd,
                        "original": cmd
                    })
                    confidence *= 0.85
                else:
                    confidence *= 0.5  # Muy baja confianza si no reconoce
        
        # Validar mínimo de confianza
        confidence = max(0.0, min(1.0, confidence))
        
        return actions, confidence
    
    @staticmethod
    def _extract_parameters(cmd: str, action_info: Dict, keyword: str) -> Dict:
        """Extrae parámetros de la instrucción"""
        params = action_info["args"].copy()
        
        # Buscar números/ángulos
        tokens = cmd.split()
        for i, token in enumerate(tokens):
            token_clean = token.rstrip("º°grados.")
            
            if token_clean.isdigit():
                num = int(token_clean)
                if "rotar" in keyword or "rotación" in cmd:
                    params["rotation"] = [0, 0, num]
                elif "escala" in keyword or "escalar" in cmd:
                    params["scale"] = num / 10.0 if num > 10 else num
                elif "mover" in keyword:
                    params["offset"] = [num, 0, 0]
            
            # Buscar palabras numéricas
            if token_clean in ZULYCommandParser.NUMERIC_WORDS:
                num = ZULYCommandParser.NUMERIC_WORDS[token_clean]
                if "rotar" in keyword or "rotación" in cmd:
                    params["rotation"] = [0, 0, num]
                elif "escala" in keyword or "escalar" in cmd:
                    params["scale"] = num / 10.0 if num > 10 else num
        
        return params


class ZULYCLIExecutor:
    """Ejecutor de comandos parseados en Blender"""
    
    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.history = []
        self.blender_exe = BLENDER_EXE
        self.results = {"commands_executed": 0, "successful": 0, "failed": 0}
        
        # Detector de tiempo real
        from core.adapters.blender_adapter import BlenderAdapter
        self.adapter = BlenderAdapter()
        if hasattr(self.adapter, '_live_active') and self.adapter._live_active:
            self.log("📡 MODO LIVE ACTIVO: El puente con Blender está abierto.", "success")
    
    def execute_actions(self, actions: List[Dict]) -> Dict[str, Any]:
        """Ejecuta lista de acciones en Blender, priorizando Live-Link"""
        
        if not actions:
            self.log("[WARNING] No hay acciones para ejecutar", "error")
            return {"status": "error", "message": "Sin acciones"}
            
        # --- BIFURCACIÓN TIEMPO REAL ---
        if hasattr(self, 'adapter') and hasattr(self.adapter, '_live_active') and self.adapter._live_active:
            live_results = {"status": "success", "objects_created": 0, "commands": []}
            all_live = True
            for action in actions:
                action_name = action.get("action")
                params = action.get("parameters", {})
                
                # Acciones soportadas por el puente
                supported = ["create_cube", "create_sphere", "create_cylinder", "create_cone", "create_plane", "create_hollow_primitive"]
                if action_name in supported:
                    # Enrutamiento especial para perforaciones
                    p_type = action_name.replace("create_", "")
                    if p_type == "hollow_primitive":
                        # Enviar directamente al cliente de tiempo real
                        res = self.adapter._live_client.send_command("create_hollow_primitive", params)
                        if res:
                            self.log("⚡ Live-Link: Perforación enviada.", "success")
                            live_results["objects_created"] += 1
                            live_results["commands"].append({"action": action_name, "status": "success"})
                            continue
                    else:
                        res = self.adapter.create_primitive(p_type, **params)
                        if res.get("status") == "success":
                            live_results["objects_created"] += 1
                            live_results["commands"].append({"action": action_name, "status": "success"})
                            continue
                
                # Si llegamos aquí, hay un comando no soportado por Live v1
                all_live = False
                break
            
            if all_live:
                self.results["successful"] += 1
                self.results["commands_executed"] += len(actions)
                return live_results

        self.log(f"[EXECUTE] Ejecutando {len(actions)} acciones vía Script...", "info")
        
        # Generar script de Blender
        script = self._generate_blender_script(actions)
        
        # Ejecutar en Blender
        return self._run_blender_script(script)
    
    def _generate_blender_script(self, actions: List[Dict]) -> str:
        """Genera script Python para Blender"""
        
        script_lines = [
            "import bpy",
            "import json",
            "from datetime import datetime",
            "",
            "results = {"
            "    'status': 'success',",
            "    'commands': [],",
            "    'validation_v0': 'PENDING',",
            "    'objects_created': 0,",
            "    'timestamp': datetime.now().isoformat()",
            "}",
            "",
            "cursor_x = 0.0",
            "",
            "# Limpieza de escena (Garantía de visibilidad)",
            "bpy.ops.object.select_all(action='SELECT')",
            "bpy.ops.object.delete()",
            "",
        ]
        
        for i, action in enumerate(actions):
            action_name = action.get("action", "")
            params = action.get("parameters", {})
            
            # Crear acciones específicas
            if action_name == "create_cube":
                script_lines.extend([
                    f"try:",
                    f"    bpy.ops.mesh.primitive_cube_add(size=2, location=(cursor_x, 0, 0))",
                    f"    cursor_x += 3.0",
                    f"    results['commands'].append({{'action': 'create_cube', 'status': 'success'}})",
                    f"    results['objects_created'] += 1",
                    f"except Exception as e:",
                    f"    results['commands'].append({{'action': 'create_cube', 'status': 'error', 'error': str(e)}})",
                    "",
                ])
            
            elif action_name == "create_sphere":
                script_lines.extend([
                    f"try:",
                    f"    bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(cursor_x, 0, 0))",
                    f"    cursor_x += 3.0",
                    f"    results['commands'].append({{'action': 'create_sphere', 'status': 'success'}})",
                    f"    results['objects_created'] += 1",
                    f"except Exception as e:",
                    f"    results['commands'].append({{'action': 'create_sphere', 'status': 'error', 'error': str(e)}})",
                    "",
                ])
                
            elif action_name == "create_cylinder":
                script_lines.extend([
                    f"try:",
                    f"    bpy.ops.mesh.primitive_cylinder_add(radius=1, depth=2, location=(cursor_x, 0, 0))",
                    f"    cursor_x += 3.0",
                    f"    results['commands'].append({{'action': 'create_cylinder', 'status': 'success'}})",
                    f"    results['objects_created'] += 1",
                    f"except Exception as e:",
                    f"    results['commands'].append({{'action': 'create_cylinder', 'status': 'error', 'error': str(e)}})",
                    "",
                ])

            elif action_name == "create_plane":
                script_lines.extend([
                    f"try:",
                    f"    bpy.ops.mesh.primitive_plane_add(size=2, location=(cursor_x, 0, 0))",
                    f"    cursor_x += 3.0",
                    f"    results['commands'].append({{'action': 'create_plane', 'status': 'success'}})",
                    f"    results['objects_created'] += 1",
                    f"except Exception as e:",
                    f"    results['commands'].append({{'action': 'create_plane', 'status': 'error', 'error': str(e)}})",
                    "",
                ])

            elif action_name == "create_cone":
                script_lines.extend([
                    f"try:",
                    f"    bpy.ops.mesh.primitive_cone_add(radius1=1, depth=2, location=(cursor_x, 0, 0))",
                    f"    cursor_x += 3.0",
                    f"    results['commands'].append({{'action': 'create_cone', 'status': 'success'}})",
                    f"    results['objects_created'] += 1",
                    f"except Exception as e:",
                    f"    results['commands'].append({{'action': 'create_cone', 'status': 'error', 'error': str(e)}})",
                    "",
                ])

            elif action_name == "create_monkey":
                script_lines.extend([
                    f"try:",
                    f"    bpy.ops.mesh.primitive_monkey_add(size=2, location=(cursor_x, 0, 0))",
                    f"    cursor_x += 3.0",
                    f"    results['commands'].append({{'action': 'create_monkey', 'status': 'success'}})",
                    f"    results['objects_created'] += 1",
                    f"except Exception as e:",
                    f"    results['commands'].append({{'action': 'create_monkey', 'status': 'error', 'error': str(e)}})",
                    "",
                ])
            
            elif action_name == "create_hollow_primitive":
                type_prim = params.get("type", "cube")
                script_lines.extend([
                    f"try:",
                    f"    import math",
                    f"    # 1. Limpieza y Creación Base",
                    f"    bpy.ops.object.select_all(action='SELECT')",
                    f"    bpy.ops.object.delete()",
                    f"    if '{type_prim}' == 'cube': bpy.ops.mesh.primitive_cube_add(size=2, location=(0,0,0))",
                    f"    elif '{type_prim}' == 'sphere': bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, location=(0,0,0))",
                    f"    elif '{type_prim}' == 'monkey' or '{type_prim}' == 'suzanne': bpy.ops.mesh.primitive_monkey_add(size=2, location=(0,0,0))",
                    f"    else: bpy.ops.mesh.primitive_cube_add(size=2, location=(0,0,0))",
                    f"    ",
                    f"    obj = bpy.context.active_object",
                    f"    obj.name = 'ZULY_HUECO'",
                    f"    ",
                    f"    # 2. Perforación con Taladros Axiales",
                    f"    cutters = []",
                    f"    # X",
                    f"    bpy.ops.mesh.primitive_cylinder_add(radius=0.25, depth=10, location=(0,0,0), rotation=(0, math.pi/2, 0))",
                    f"    cutters.append(bpy.context.active_object)",
                    f"    # Y",
                    f"    bpy.ops.mesh.primitive_cylinder_add(radius=0.25, depth=10, location=(0,0,0), rotation=(math.pi/2, 0, 0))",
                    f"    cutters.append(bpy.context.active_object)",
                    f"    # Z",
                    f"    bpy.ops.mesh.primitive_cylinder_add(radius=0.25, depth=10, location=(0,0,0))",
                    f"    cutters.append(bpy.context.active_object)",
                    f"    ",
                    f"    # 3. Fusión Booleana con Garantía de Contexto",
                    f"    for i, cut in enumerate(cutters):",
                    f"        bpy.ops.object.select_all(action='DESELECT')",
                    f"        obj.select_set(True)",
                    f"        bpy.context.view_layer.objects.active = obj",
                    f"        mod = obj.modifiers.new(name=f'Hole_{{i}}', type='BOOLEAN')",
                    f"        mod.operation = 'DIFFERENCE'",
                    f"        mod.object = cut",
                    f"        mod.solver = 'EXACT'",
                    f"        bpy.ops.object.modifier_apply(modifier=mod.name)",
                    f"        bpy.data.objects.remove(cut, do_unlink=True)",
                    f"    ",
                    f"    results['objects_created'] += 1",
                    f"    results['commands'].append({{'action': 'create_hollow_primitive', 'status': 'success'}})",
                    f"except Exception as e:",
                    f"    import traceback",
                    f"    results['commands'].append({{'action': 'create_hollow_primitive', 'status': 'error', 'error': str(e) + ': ' + traceback.format_exc()}})",
                    "",
                ])
            
            elif action_name == "create_hollow_primitives":
                script_lines.extend([
                    f"try:",
                    f"    import math",
                    f"    bpy.ops.object.select_all(action='SELECT')",
                    f"    bpy.ops.object.delete()",
                    f"    cursor_x = 0.0",
                    f"    prims = ['cube', 'sphere', 'monkey', 'cylinder', 'cone']",
                    f"    for p_type in prims:",
                    f"        loc = (cursor_x, 0, 0)",
                    f"        if p_type == 'cube': bpy.ops.mesh.primitive_cube_add(size=2, location=loc)",
                    f"        elif p_type == 'sphere': bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, location=loc)",
                    f"        elif p_type == 'monkey': bpy.ops.mesh.primitive_monkey_add(size=2, location=loc)",
                    f"        elif p_type == 'cylinder': bpy.ops.mesh.primitive_cylinder_add(radius=1.0, depth=2.0, location=loc)",
                    f"        elif p_type == 'cone': bpy.ops.mesh.primitive_cone_add(radius1=1.0, radius2=0.0, depth=2.0, location=loc)",
                    f"        ",
                    f"        obj = bpy.context.active_object",
                    f"        obj.name = f'ZULY_{{p_type.upper()}}'",
                    f"        ",
                    f"        cutters = []",
                    f"        bpy.ops.mesh.primitive_cylinder_add(radius=0.25, depth=10, location=loc, rotation=(0, math.pi/2, 0))",
                    f"        cutters.append(bpy.context.active_object)",
                    f"        bpy.ops.mesh.primitive_cylinder_add(radius=0.25, depth=10, location=loc, rotation=(math.pi/2, 0, 0))",
                    f"        cutters.append(bpy.context.active_object)",
                    f"        bpy.ops.mesh.primitive_cylinder_add(radius=0.25, depth=10, location=loc)",
                    f"        cutters.append(bpy.context.active_object)",
                    f"        ",
                    f"        for i, cut in enumerate(cutters):",
                    f"            bpy.ops.object.select_all(action='DESELECT')",
                    f"            obj.select_set(True)",
                    f"            bpy.context.view_layer.objects.active = obj",
                    f"            mod = obj.modifiers.new(name=f'Hole_{{i}}', type='BOOLEAN')",
                    f"            mod.operation = 'DIFFERENCE'",
                    f"            mod.object = cut",
                    f"            mod.solver = 'EXACT'",
                    f"            bpy.ops.object.modifier_apply(modifier=mod.name)",
                    f"            bpy.data.objects.remove(cut, do_unlink=True)",
                    f"        ",
                    f"        cursor_x += 6.0",
                    f"        results['objects_created'] += 1",
                    f"    results['commands'].append({{'action': 'create_hollow_primitives', 'status': 'success'}})",
                    f"except Exception as e:",
                    f"    import traceback",
                    f"    results['commands'].append({{'action': 'create_hollow_primitives', 'status': 'error', 'error': str(e) + ': ' + traceback.format_exc()}})",
                    "",
                ])
            
            elif action_name == "rotate_object":
                rotation = params.get("rotation", [0, 0, 45])
                script_lines.extend([
                    f"try:",
                    f"    obj = bpy.context.active_object",
                    f"    if obj:",
                    f"        import math",
                    f"        rx, ry, rz = {rotation[0]} * math.pi/180, {rotation[1]} * math.pi/180, {rotation[2]} * math.pi/180",
                    f"        obj.rotation_euler = (rx, ry, rz)",
                    f"        results['commands'].append({{'action': 'rotate_object', 'rotation': {rotation}, 'status': 'success'}})",
                    f"except Exception as e:",
                    f"    results['commands'].append({{'action': 'rotate_object', 'status': 'error', 'error': str(e)}})",
                    "",
                ])
            
            elif action_name == "scale_object":
                scale = params.get("scale", 1.5)
                script_lines.extend([
                    f"try:",
                    f"    obj = bpy.context.active_object",
                    f"    if obj:",
                    f"        obj.scale = ({scale}, {scale}, {scale})",
                    f"        results['commands'].append({{'action': 'scale_object', 'scale': {scale}, 'status': 'success'}})",
                    f"except Exception as e:",
                    f"    results['commands'].append({{'action': 'scale_object', 'status': 'error', 'error': str(e)}})",
                    "",
                ])
            
            elif action_name == "create_architectural_scene":
                script_lines.extend([
                    f"try:",
                    f"    # Villa Savoye inspirada",
                    f"    bpy.ops.mesh.primitive_cube_add(size=8, location=(0, 0, 0))",
                    f"    bpy.ops.mesh.primitive_cube_add(size=1, location=(3, 3, 0))",
                    f"    results['commands'].append({{'action': 'create_architectural_scene', 'status': 'success'}})",
                    f"    results['objects_created'] += 2",
                    f"except Exception as e:",
                    f"    results['commands'].append({{'action': 'create_architectural_scene', 'status': 'error', 'error': str(e)}})",
                    "",
                ])
        
        # Guardar resultados
        script_lines.extend([
            "try:",
            "    # Validación V0 rápida: verificar si realmente hay mallas nuevas",
            "    mesh_count = len([o for o in bpy.data.objects if o.type == 'MESH'])",
            "    if mesh_count >= results['objects_created']:",
            "        results['validation_v0'] = 'OK'",
            "    else:",
            "        results['validation_v0'] = 'FAILED'",
            "",
            "    import os",
            "    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ZULY_LAB', 'resultados_zuly')",
            "    os.makedirs(out_dir, exist_ok=True)",
            "    blend_path = os.path.join(out_dir, 'zuly_cli_resultado_primitivas.blend')",
            "    bpy.ops.wm.save_as_mainfile(filepath=blend_path)",
            "    results['blend_file'] = blend_path",
            "except Exception as e:",
            "    pass",
            "",
            "with open('zuly_cli_results.json', 'w') as f:",
            "    json.dump(results, f, indent=2)",
            "print(json.dumps(results))",
        ])
        
        return "\n".join(script_lines)
    
    def _run_blender_script(self, script: str) -> Dict[str, Any]:
        """Ejecuta script en Blender"""
        
        # Guardar script
        script_path = SCRIPT_DIR / "temp_cli_script.py"
        with open(script_path, "w") as f:
            f.write(script)
        
        try:
            # Ejecutar Blender
            cmd = [
                str(self.blender_exe),
                "--background",
                "--python", str(script_path)
            ]
            
            self.log(f"[BLENDER] Ejecutando: {' '.join(cmd)}", "debug")
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # Parsear resultado
            try:
                if Path("zuly_cli_results.json").exists():
                    with open("zuly_cli_results.json") as f:
                        results = json.load(f)
                    self.results["successful"] += 1
                    self.results["commands_executed"] += 1
                    self.log(f"[SUCCESS] {results['objects_created']} objetos creados", "success")
                    return results
            except:
                pass
            
            self.results["failed"] += 1
            return {"status": "error", "output": result.stdout}
            
        except subprocess.TimeoutExpired:
            self.log("[ERROR] Timeout ejecutando Blender", "error")
            self.results["failed"] += 1
            return {"status": "error", "message": "Timeout"}
        except Exception as e:
            self.log(f"[ERROR] {e}", "error")
            self.results["failed"] += 1
            return {"status": "error", "message": str(e)}
        finally:
            # Limpiar
            if script_path.exists():
                script_path.unlink()
    
    def log(self, message: str, level: str = "info"):
        """Log con colores"""
        if not self.verbose:
            return
        
        colors = {
            "info": "\033[94m",      # Azul
            "success": "\033[92m",   # Verde
            "error": "\033[91m",     # Rojo
            "debug": "\033[90m",     # Gris
            "reset": "\033[0m"
        }
        
        color = colors.get(level, colors["info"])
        click.echo(f"{color}{message}{colors['reset']}")


# ============================================================================
# CLICK CLI
# ============================================================================

@click.group()
def cli():
    """ZULY CLI - Interfaz interactiva para LYZU en Blender"""
    pass


@cli.command()
@click.argument("instruction", nargs=-1)
@click.option("--verbose", is_flag=True, help="Modo verbose")
@click.option("--dry-run", is_flag=True, help="Solo parsear, no ejecutar")
def execute(instruction, verbose, dry_run):
    """Ejecuta instrucción en lenguaje natural
    
    Ejemplos:
      zuly execute "crear un cubo"
      zuly execute "crear esfera y rotar 45 grados"
      zuly execute "crear arquitectura"
    """
    
    if not instruction:
        click.echo("❌ Debe proporcionar una instrucción")
        return
    
    full_instruction = " ".join(instruction)
    
    # Banner
    click.secho("\n" + "=" * 70, fg="cyan")
    click.secho("  ZULY CLI - EJECUTOR DE COMANDOS", fg="cyan", bold=True)
    click.secho("=" * 70 + "\n", fg="cyan")
    
    # Parsear
    click.echo(f"📝 Instrucción: {full_instruction}\n")
    
    # Usar el Agente real para procesar la petición
    agent = Agent(auto_monitor=True)
    result = agent.process_natural_request(full_instruction)
    
    confidence = result.get('confidence', 0.0)
    click.secho(f"🔍 Confianza del Agente: {confidence:.1%}", fg="yellow")

    if confidence < 0.5:
        click.secho("\n⚠️  Confianza muy baja, cancelando", fg="red")
        return

    # Mostrar resultados
    click.secho("\n" + "=" * 70, fg="cyan")
    click.secho("  RESULTADOS", fg="cyan", bold=True)
    click.secho("=" * 70 + "\n", fg="cyan")
    
    if result.get("success"):
        click.secho(f"✅ {result.get('feedback')}", fg="green")
    else:
        click.secho(f"❌ Error: {result.get('error', 'Fallo en la ejecución')}", fg="red")
    
    click.echo()


@cli.command()
@click.option("--limit", default=10, help="Últimos N comandos")
def history(limit):
    """Muestra historial de comandos"""
    
    history_file = ZULY_LAB / "cli_history.json"
    
    if not history_file.exists():
        click.echo("📋 Historial vacío")
        return
    
    with open(history_file) as f:
        history = json.load(f)
    
    click.secho("\n📜 HISTORIAL DE COMANDOS\n", fg="cyan", bold=True)
    
    for i, cmd in enumerate(history[-limit:], 1):
        click.echo(f"{i}. {cmd.get('instruction')}")
        click.echo(f"   Resultado: {cmd.get('status')}")
        click.echo()


@cli.command()
def interactive():
    """Modo interactivo - REPL"""
    
    click.secho("\n" + "=" * 70, fg="cyan")
    click.secho("  ZULY INTERACTIVE MODE - Escribe 'exit' para salir", fg="cyan", bold=True)
    click.secho("=" * 70 + "\n", fg="cyan")
    
    executor = ZULYCLIExecutor(verbose=False)
    
    while True:
        try:
            instruction = click.prompt("zuly> ", type=str)
            
            if instruction.lower() in ["exit", "quit", "salir"]:
                click.secho("\n👋 Hasta luego!", fg="cyan")
                break
            
            if not instruction.strip():
                continue
            
            # Parsear y ejecutar
            parser = ZULYCommandParser()
            actions, confidence = parser.parse_command(instruction)
            
            if confidence < 0.3:
                click.secho("⚠️  No entendí bien eso (confianza baja)", fg="yellow")
                continue
            
            click.echo(f"🔍 {len(actions)} acciones | Confianza: {confidence:.1%}")
            
            results = executor.execute_actions(actions)
            
            if results.get("status") == "success":
                click.secho(f"✅ {results.get('objects_created', 0)} creado(s)", fg="green")
            else:
                click.secho("❌ Error ejecutando", fg="red")
            
        except KeyboardInterrupt:
            click.echo("\n👋 Hasta luego!")
            break
        except Exception as e:
            click.secho(f"❌ Error: {e}", fg="red")


@cli.command()
def status():
    """Muestra estado del sistema"""
    
    click.secho("\n" + "=" * 70, fg="cyan")
    click.secho("  ZULY SYSTEM STATUS", fg="cyan", bold=True)
    click.secho("=" * 70 + "\n", fg="cyan")
    
    # Verificar Blender
    if BLENDER_EXE and BLENDER_EXE.exists():
        click.secho(f"✅ Blender: {BLENDER_EXE}", fg="green")
    else:
        click.secho(f"❌ Blender no encontrado: {BLENDER_EXE}", fg="red")
    
    # Verificar ZULY_LAB
    if ZULY_LAB.exists():
        click.secho(f"✅ ZULY_LAB: {ZULY_LAB}", fg="green")
    else:
        click.secho(f"❌ ZULY_LAB no encontrado", fg="red")
    
    # Verificar C2 Memory
    c2_db = ZULY_LAB / "c2_memory.db"
    if c2_db.exists():
        click.secho(f"✅ C2 Memory: {c2_db.stat().st_size} bytes", fg="green")
    else:
        click.secho("⚠️  C2 Memory aún no creada", fg="yellow")
    
    click.echo()


@cli.command()
def review():
    """Revisa los patrones que esperan 'Visto Bueno'"""
    
    agent = Agent()
    pending = agent.get_pending_patterns()
    
    if not pending:
        click.secho("\n📋 No hay patrones esperando revisión.", fg="green")
        return
    
    click.secho("\n🔍 REVISIÓN DE PATRONES PENDIENTES\n", fg="cyan", bold=True)
    
    for i, p in enumerate(pending, 1):
        click.echo(f"{i}. ID: {p['pattern_id'][:8]}")
        click.echo(f"   Instrucción: '{p['user_request']}'")
        click.echo(f"   Comando: {p['intent']['command_name']}")
        click.echo(f"   Confianza: {p['intent']['confidence']:.1%}")
        click.echo("-" * 40)
        
    click.echo("\nUsa 'zuly approve <id>' para dar el visto bueno.")

@cli.command()
@click.argument("pattern_id")
def approve(pattern_id):
    """Da el visto bueno (aprobación) a un patrón pendiente"""
    
    agent = Agent()
    # Buscar ID corto
    pending = agent.get_pending_patterns()
    full_id = None
    for p in pending:
        if p['pattern_id'].startswith(pattern_id):
            full_id = p['pattern_id']
            break
            
    if not full_id:
        click.secho(f"❌ No se encontró patrón pendiente con ID {pattern_id}", fg="red")
        return
        
    if agent.approve_pattern(full_id):
        click.secho(f"✅ ¡VISTO BUENO CONCEDIDO! El patrón {pattern_id} ya es parte del conocimiento de Zuly.", fg="green")
    else:
        click.secho("❌ Falló la aprobación.", fg="red")

@cli.command()
@click.argument("pattern_id")
def reject(pattern_id):
    """Rechaza y elimina un patrón pendiente"""
    
    agent = Agent()
    # Buscar ID corto
    pending = agent.get_pending_patterns()
    full_id = None
    for p in pending:
        if p['pattern_id'].startswith(pattern_id):
            full_id = p['pattern_id']
            break
            
    if not full_id:
        click.secho(f"❌ No se encontró patrón pendiente con ID {pattern_id}", fg="red")
        return
        
    if agent.reject_pattern(full_id):
        click.secho(f"🗑️ Patrón {pattern_id} rechazado y purgado con éxito.", fg="yellow")
    else:
        click.secho("❌ Falló el rechazo.", fg="red")

if __name__ == "__main__":
    cli()
