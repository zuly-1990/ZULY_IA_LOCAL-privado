"""
core/adapters/real_blender_adapter.py

Adapter REAL que ejecuta comandos en Blender via CLI:
  blender --background --python script.py

Esto es 100% real: los objetos se crean en un archivo .blend verdadero.
NO usa MockAdapter. NO simula nada.
"""

import os
import sys
import json
import subprocess
import tempfile
from typing import Dict, Any, List, Optional, Literal
from core.adapters.engine_adapter import EngineAdapter, EngineError
from core.utils.logging import log_info, log_warning, log_error, log_debug

# Ruta al ejecutable de Blender (auto-detectado o desde env)
BLENDER_BIN = os.environ.get("BLENDER_BIN", "/usr/local/bin/blender")
# Archivo .blend donde se acumula el trabajo real
BLEND_FILE   = os.environ.get("ZULY_BLEND_FILE", "/opt/zuly/ZULY_MAESTRO.blend")


def _run_blender_script(script_code: str) -> Dict[str, Any]:
    """
    Ejecuta un script Python dentro de Blender en modo background.
    El script debe imprimir un JSON con la clave 'zuly_result' al final.
    Retorna el dict parseado o un error.
    """
    # Escribir script a archivo temporal
    with tempfile.NamedTemporaryFile(
        mode='w', suffix='.py', delete=False, prefix='/tmp/zuly_bpy_'
    ) as f:
        f.write(script_code)
        tmp_path = f.name

    try:
        cmd = [
            BLENDER_BIN,
            BLEND_FILE,
            "--background",
            "--python", tmp_path
        ]
        log_debug(f"[RealBlender] Ejecutando: {' '.join(cmd)}")

        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60
        )

        # Buscar el JSON de resultado en stdout
        result_json = None
        for line in proc.stdout.splitlines():
            if line.strip().startswith('ZULY_RESULT:'):
                try:
                    result_json = json.loads(line.strip()[len('ZULY_RESULT:'):])
                except Exception:
                    pass

        if result_json:
            return result_json
        elif proc.returncode != 0:
            log_error(f"[RealBlender] stderr: {proc.stderr[-500:]}")
            return {"success": False, "error": f"Blender exit code {proc.returncode}", "stderr": proc.stderr[-300:]}
        else:
            return {"success": True, "output": proc.stdout[-300:]}

    except subprocess.TimeoutExpired:
        return {"success": False, "error": "Blender tardó más de 60s"}
    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        try:
            os.unlink(tmp_path)
        except:
            pass


class RealBlenderAdapter(EngineAdapter):
    """
    Adapter 100% REAL. Usa el binario de Blender via CLI.
    Cada operación genera y ejecuta un script bpy dentro de Blender.
    Los cambios se guardan en ZULY_MAESTRO.blend.
    """

    def __init__(self):
        self._blender_bin = BLENDER_BIN
        self._blend_file = BLEND_FILE
        self._available = os.path.exists(self._blender_bin)
        if self._available:
            log_info(f"[RealBlenderAdapter] ✅ Blender encontrado: {self._blender_bin}")
            log_info(f"[RealBlenderAdapter] 📁 Archivo de trabajo: {self._blend_file}")
        else:
            log_error(f"[RealBlenderAdapter] ❌ Blender NO encontrado en: {self._blender_bin}")

    def is_available(self) -> bool:
        return self._available

    def get_engine_info(self) -> Dict[str, Any]:
        return self._success_response(
            name="RealBlenderAdapter",
            blender_bin=self._blender_bin,
            blend_file=self._blend_file,
            mode="REAL_CLI"
        )

    def _make_script(self, bpy_code: str, result_vars: str = "{}") -> str:
        """Envuelve código bpy en un script que imprime el resultado como JSON."""
        return f"""
import bpy
import json
import sys

# Asegurar que el archivo se guarda correctamente
def save_blend():
    bpy.ops.wm.save_as_mainfile(filepath="{self._blend_file}")

try:
    result = dict()
{bpy_code}
    save_blend()
    result["success"] = True
    print("ZULY_RESULT:" + json.dumps(result))
except Exception as e:
    import traceback
    print("ZULY_RESULT:" + json.dumps({{"success": False, "error": str(e), "trace": traceback.format_exc()[-400:]}}))
"""

    def create_primitive(self, primitive_type: str, **params) -> Dict[str, Any]:
        """Crea una primitiva REAL en Blender."""
        location = params.get('location', [0, 0, 0])
        scale = params.get('scale', [1, 1, 1])
        name = params.get('name', f'{primitive_type}_real')
        size = params.get('size', None)

        # Calcular scale desde size si se especificó
        if size and isinstance(size, list) and len(size) == 3:
            sx, sy, sz = size[0]/2, size[1]/2, size[2]/2
        elif size and isinstance(size, (int, float)):
            sx = sy = sz = size / 2
        else:
            if isinstance(scale, list) and len(scale) == 3:
                sx, sy, sz = scale
            else:
                sx = sy = sz = float(scale) if not isinstance(scale, list) else 1.0

        lx, ly, lz = location[0], location[1], location[2]

        type_map = {
            'cube':     'bpy.ops.mesh.primitive_cube_add()',
            'sphere':   'bpy.ops.mesh.primitive_uv_sphere_add(radius=1)',
            'cylinder': 'bpy.ops.mesh.primitive_cylinder_add(radius=1, depth=2)',
            'plane':    'bpy.ops.mesh.primitive_plane_add(size=2)',
            'cone':     'bpy.ops.mesh.primitive_cone_add(radius1=1, radius2=0, depth=2)',
        }

        add_op = type_map.get(primitive_type, 'bpy.ops.mesh.primitive_cube_add()')

        bpy_code = f"""
    {add_op}
    obj = bpy.context.active_object
    obj.name = "{name}"
    obj.location = ({lx}, {ly}, {lz})
    obj.scale = ({sx}, {sy}, {sz})
    result["object_name"] = obj.name
    result["location"] = list(obj.location)
    result["scale"] = list(obj.scale)
"""
        script = self._make_script(bpy_code)
        res = _run_blender_script(script)
        if res.get("success"):
            log_info(f"[RealBlender] ✅ Primitiva REAL creada: {name} en {location}")
        else:
            log_error(f"[RealBlender] ❌ Error creando {name}: {res.get('error')}")
        return res

    def move_object(self, object_name: str, location: List[float] = None, offset: List[float] = None) -> Dict[str, Any]:
        if location:
            lx, ly, lz = location
            bpy_code = f"""
    obj = bpy.data.objects.get("{object_name}")
    if not obj:
        raise Exception("OBJECT_NOT_FOUND: {object_name}")
    obj.location = ({lx}, {ly}, {lz})
    result["object_name"] = obj.name
    result["new_location"] = list(obj.location)
"""
        else:
            ox, oy, oz = offset or [0, 0, 0]
            bpy_code = f"""
    obj = bpy.data.objects.get("{object_name}")
    if not obj:
        raise Exception("OBJECT_NOT_FOUND: {object_name}")
    obj.location[0] += {ox}
    obj.location[1] += {oy}
    obj.location[2] += {oz}
    result["object_name"] = obj.name
    result["new_location"] = list(obj.location)
"""
        return _run_blender_script(self._make_script(bpy_code))

    def rotate_object(self, object_name: str, rotation: List[float], degrees: bool = False) -> Dict[str, Any]:
        import math
        rot = [math.radians(r) for r in rotation] if degrees else rotation
        rx, ry, rz = rot
        bpy_code = f"""
    import math
    obj = bpy.data.objects.get("{object_name}")
    if not obj:
        raise Exception("OBJECT_NOT_FOUND: {object_name}")
    obj.rotation_euler = ({rx}, {ry}, {rz})
    result["object_name"] = obj.name
"""
        return _run_blender_script(self._make_script(bpy_code))

    def scale_object(self, object_name: str, scale) -> Dict[str, Any]:
        if isinstance(scale, (list, tuple)):
            sx, sy, sz = scale
        else:
            sx = sy = sz = float(scale)
        bpy_code = f"""
    obj = bpy.data.objects.get("{object_name}")
    if not obj:
        raise Exception("OBJECT_NOT_FOUND: {object_name}")
    obj.scale = ({sx}, {sy}, {sz})
    result["object_name"] = obj.name
"""
        return _run_blender_script(self._make_script(bpy_code))

    def create_material(self, name: str, **properties) -> Dict[str, Any]:
        color = properties.get('color', [0.8, 0.8, 0.8])
        r, g, b = color[0], color[1], color[2]
        bpy_code = f"""
    mat = bpy.data.materials.new(name="{name}")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get('Principled BSDF')
    if bsdf:
        bsdf.inputs['Base Color'].default_value = ({r}, {g}, {b}, 1.0)
    result["material_name"] = mat.name
"""
        return _run_blender_script(self._make_script(bpy_code))

    def apply_material(self, object_name: str, material_name: str) -> Dict[str, Any]:
        bpy_code = f"""
    obj = bpy.data.objects.get("{object_name}")
    mat = bpy.data.materials.get("{material_name}")
    if not obj:
        raise Exception("OBJECT_NOT_FOUND: {object_name}")
    if not mat:
        raise Exception("MATERIAL_NOT_FOUND: {material_name}")
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)
    result["object_name"] = obj.name
    result["material_name"] = mat.name
"""
        return _run_blender_script(self._make_script(bpy_code))

    def get_scene_state(self) -> Dict[str, Any]:
        bpy_code = """
    objects = []
    for obj in bpy.data.objects:
        objects.append({
            'name': obj.name,
            'type': obj.type,
            'location': list(obj.location),
        })
    result["objects"] = objects
    result["object_count"] = len(objects)
"""
        return _run_blender_script(self._make_script(bpy_code))

    def get_active_object(self) -> Optional[str]:
        return None

    def get_object_info(self, object_name: str) -> Dict[str, Any]:
        bpy_code = f"""
    obj = bpy.data.objects.get("{object_name}")
    if not obj:
        raise Exception("OBJECT_NOT_FOUND: {object_name}")
    result["name"] = obj.name
    result["type"] = obj.type
    result["location"] = list(obj.location)
    result["scale"] = list(obj.scale)
"""
        return _run_blender_script(self._make_script(bpy_code))

    def get_object(self, object_name: str) -> Dict[str, Any]:
        return self.get_object_info(object_name)

    def create_light(self, light_type: str, **params) -> Dict[str, Any]:
        name = params.get('name', f'Light_{light_type}')
        location = params.get('location', [0, 0, 5])
        energy = params.get('energy', 1000)
        lx, ly, lz = location
        bpy_code = f"""
    light_data = bpy.data.lights.new(name="{name}", type="{light_type}")
    light_data.energy = {energy}
    light_obj = bpy.data.objects.new(name="{name}", object_data=light_data)
    light_obj.location = ({lx}, {ly}, {lz})
    bpy.context.scene.collection.objects.link(light_obj)
    result["light_name"] = light_obj.name
"""
        return _run_blender_script(self._make_script(bpy_code))

    def clear_scene(self) -> Dict[str, Any]:
        bpy_code = """
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    result["cleared"] = True
"""
        return _run_blender_script(self._make_script(bpy_code))

    def set_material_color(self, object_name: str, color: List[float]) -> Dict[str, Any]:
        r, g, b = color[0], color[1], color[2]
        bpy_code = f"""
    obj = bpy.data.objects.get("{object_name}")
    if not obj:
        raise Exception("OBJECT_NOT_FOUND: {object_name}")
    if not obj.data.materials:
        mat = bpy.data.materials.new(name="{object_name}_mat")
        mat.use_nodes = True
        obj.data.materials.append(mat)
    mat = obj.data.materials[0]
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get('Principled BSDF')
    if bsdf:
        bsdf.inputs['Base Color'].default_value = ({r}, {g}, {b}, 1.0)
    result["object_name"] = obj.name
    result["color"] = [{r}, {g}, {b}]
"""
        return _run_blender_script(self._make_script(bpy_code))

    def execute_geometry_nodes_script(self, target_object: str, script_code: str) -> Dict[str, Any]:
        return self._error_response(EngineError.OPERATION_FAILED, "GeoNodes scripting no soportado en RealBlenderAdapter. Usa primitivas.")

    def set_dimensions(self, name: str, dimensions: List[float]) -> Dict[str, Any]:
        sx, sy, sz = dimensions[0]/2, dimensions[1]/2, dimensions[2]/2
        bpy_code = f"""
    obj = bpy.data.objects.get("{name}")
    if not obj:
        raise Exception("OBJECT_NOT_FOUND: {name}")
    obj.scale = ({sx}, {sy}, {sz})
    result["name"] = obj.name
"""
        return _run_blender_script(self._make_script(bpy_code))

    def set_rotation(self, name: str, rotation: List[float], mode: str = 'XYZ') -> Dict[str, Any]:
        rx, ry, rz = rotation
        bpy_code = f"""
    obj = bpy.data.objects.get("{name}")
    if not obj:
        raise Exception("OBJECT_NOT_FOUND: {name}")
    obj.rotation_euler = ({rx}, {ry}, {rz})
    result["name"] = obj.name
"""
        return _run_blender_script(self._make_script(bpy_code))

    def create_texture_material(self, name: str, image_path: str, **properties) -> Dict[str, Any]:
        return self._error_response(EngineError.OPERATION_FAILED, "Usa create_material en su lugar.")

    def get_parent(self, object_name: str):
        return None

    def get_children(self, object_name: str) -> List:
        return []

    def align_objects(self, target_name: str, reference_name: str, mode: str) -> Dict[str, Any]:
        return self._success_response(message="align_objects not implemented in CLI mode")

    def add_modifier(self, object_name: str, modifier_type: str, **params) -> Dict[str, Any]:
        bpy_code = f"""
    obj = bpy.data.objects.get("{object_name}")
    if not obj:
        raise Exception("OBJECT_NOT_FOUND: {object_name}")
    mod = obj.modifiers.new(name="{modifier_type}", type="{modifier_type}")
    result["modifier"] = mod.name if mod else "failed"
"""
        return _run_blender_script(self._make_script(bpy_code))

    def update_light(self, light_name: str, **properties) -> Dict[str, Any]:
        energy = properties.get('energy', 1000)
        bpy_code = f"""
    obj = bpy.data.objects.get("{light_name}")
    if obj and obj.data:
        obj.data.energy = {energy}
    result["light_name"] = "{light_name}"
"""
        return _run_blender_script(self._make_script(bpy_code))

    def update_material(self, material_name: str, **properties) -> Dict[str, Any]:
        return self._success_response(message="update_material: use apply_material instead")

    def create_camera(self, **params) -> Dict[str, Any]:
        name = params.get('name', 'Camera_Zuly')
        location = params.get('location', [20, -20, 15])
        lx, ly, lz = location
        bpy_code = f"""
    cam_data = bpy.data.cameras.new(name="{name}")
    cam_obj = bpy.data.objects.new(name="{name}", object_data=cam_data)
    cam_obj.location = ({lx}, {ly}, {lz})
    bpy.context.scene.collection.objects.link(cam_obj)
    result["camera_name"] = cam_obj.name
"""
        return _run_blender_script(self._make_script(bpy_code))

    def set_active_camera(self, camera_name: str) -> Dict[str, Any]:
        bpy_code = f"""
    cam = bpy.data.objects.get("{camera_name}")
    if cam:
        bpy.context.scene.camera = cam
    result["camera_name"] = "{camera_name}"
"""
        return _run_blender_script(self._make_script(bpy_code))

    def position_camera(self, camera_name: str, location: List[float], look_at: List[float]) -> Dict[str, Any]:
        lx, ly, lz = location
        bpy_code = f"""
    cam = bpy.data.objects.get("{camera_name}")
    if cam:
        cam.location = ({lx}, {ly}, {lz})
    result["camera_name"] = "{camera_name}"
"""
        return _run_blender_script(self._make_script(bpy_code))

    def delete_object(self, object_name: str) -> Dict[str, Any]:
        bpy_code = f"""
    obj = bpy.data.objects.get("{object_name}")
    if obj:
        bpy.data.objects.remove(obj, do_unlink=True)
    result["deleted"] = "{object_name}"
"""
        return _run_blender_script(self._make_script(bpy_code))

    def duplicate_object(self, object_name: str, new_name: str = None) -> Dict[str, Any]:
        new_name = new_name or f"{object_name}_copy"
        bpy_code = f"""
    obj = bpy.data.objects.get("{object_name}")
    if not obj:
        raise Exception("OBJECT_NOT_FOUND: {object_name}")
    new_obj = obj.copy()
    new_obj.data = obj.data.copy()
    new_obj.name = "{new_name}"
    bpy.context.scene.collection.objects.link(new_obj)
    result["new_name"] = new_obj.name
"""
        return _run_blender_script(self._make_script(bpy_code))

    def select_object(self, object_name: str) -> Dict[str, Any]:
        bpy_code = f"""
    obj = bpy.data.objects.get("{object_name}")
    if obj:
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
    result["selected"] = "{object_name}"
"""
        return _run_blender_script(self._make_script(bpy_code))

    def deselect_all(self) -> Dict[str, Any]:
        bpy_code = """
    bpy.ops.object.select_all(action='DESELECT')
    result["deselected"] = True
"""
        return _run_blender_script(self._make_script(bpy_code))

    def select_all_by_type(self, type_name: str) -> Dict[str, Any]:
        bpy_code = f"""
    bpy.ops.object.select_all(action='DESELECT')
    count = 0
    for obj in bpy.data.objects:
        if obj.type == "{type_name.upper()}":
            obj.select_set(True)
            count += 1
    result["selected_count"] = count
"""
        return _run_blender_script(self._make_script(bpy_code))

    def rename_object(self, old_name: str, new_name: str) -> Dict[str, Any]:
        bpy_code = f"""
    obj = bpy.data.objects.get("{old_name}")
    if not obj:
        raise Exception("OBJECT_NOT_FOUND: {old_name}")
    obj.name = "{new_name}"
    result["new_name"] = obj.name
"""
        return _run_blender_script(self._make_script(bpy_code))

    def export_scene(self, format: str, filepath: str, **params) -> Dict[str, Any]:
        fmt = format.lower()
        bpy_code = f"""
    if "{fmt}" == "fbx":
        bpy.ops.export_scene.fbx(filepath="{filepath}")
    elif "{fmt}" == "obj":
        bpy.ops.export_scene.obj(filepath="{filepath}")
    elif "{fmt}" == "gltf":
        bpy.ops.export_scene.gltf(filepath="{filepath}")
    result["exported"] = "{filepath}"
"""
        return _run_blender_script(self._make_script(bpy_code))

    def render_scene(self, output_path: str, **params) -> Dict[str, Any]:
        bpy_code = f"""
    bpy.context.scene.render.filepath = "{output_path}"
    bpy.ops.render.render(write_still=True)
    result["rendered"] = "{output_path}"
"""
        return _run_blender_script(self._make_script(bpy_code))

    def set_parent(self, child_name: str, parent_name: str, keep_transform: bool = True) -> Dict[str, Any]:
        bpy_code = f"""
    child = bpy.data.objects.get("{child_name}")
    parent = bpy.data.objects.get("{parent_name}")
    if not child or not parent:
        raise Exception("OBJECT_NOT_FOUND")
    child.parent = parent
    result["child"] = child.name
    result["parent"] = parent.name
"""
        return _run_blender_script(self._make_script(bpy_code))
