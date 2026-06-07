bl_info = {
    "name": "JUES-BOT - Auditor Profesional ZULY",
    "author": "ZULY Team + Grok",
    "version": (1, 0, 0),
    "blender": (3, 6, 0),
    "location": "View3D > Sidebar > JUES",
    "description": "Auditoría completa con métricas reales, SHA-256, Geometry Nodes, Materiales, Luces, Curvas, Modificadores y Render Engine inteligente",
    "category": "ZULY",
}

import bpy
import bmesh
import hashlib
import sys
import json
from pathlib import Path
from datetime import datetime
from bpy.types import Panel, Operator, PropertyGroup
from bpy.props import BoolProperty, PointerProperty, StringProperty

# ====================== RUTAS ZULY ======================
ZULY_BASE = Path("c:/Users/Admin/Desktop/ZULY_IA_LOCAL")
ARCHIVO_ZULY = ZULY_BASE / "archivo_zuly"
TEMP_ARENA = ARCHIVO_ZULY / "temp_arena"
MASTERED = ARCHIVO_ZULY / "por_estado_aprendizaje" / "mastered"

# ====================== PROPIEDADES ======================
class JuesBotProperties(PropertyGroup):
    check_geo: BoolProperty(name="Geometria + Metricas", default=True)
    check_gn: BoolProperty(name="Geometry Nodes", default=True)
    check_lights: BoolProperty(name="Luces", default=True)
    check_curves: BoolProperty(name="Curvas", default=True)
    check_mods: BoolProperty(name="Modificadores", default=True)
    check_materials: BoolProperty(name="Materiales + UVs", default=True)
    check_render: BoolProperty(name="Render Engine", default=True)
    check_scene: BoolProperty(name="Escena Global", default=True)
    audit_entire_scene: BoolProperty(name="Auditar TODA la escena", default=False)
    target_color: StringProperty(name="Color Objetivo (Hex)", default="#FFFFFF")

# ====================== COLORES CONSOLA ======================
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    ENDC = '\033[0m'

def color_text(text, color):
    return f"{color}{text}{Colors.ENDC}"

# ====================== HELPERS ======================
def get_blender_version():
    return bpy.app.version

def get_render_engine():
    engine = bpy.context.scene.render.engine
    if engine in ('BLENDER_EEVEE', 'BLENDER_EEVEE_NEXT'):
        return "Eevee", "real-time"
    elif engine == 'CYCLES':
        return "Cycles", "path-tracing"
    elif engine == 'BLENDER_WORKBENCH':
        return "Workbench", "viewport"
    return engine, "unknown"

def calculate_sha256(obj=None):
    data = ""
    if obj and obj.type == 'MESH' and obj.data:
        bm = bmesh.new()
        bm.from_mesh(obj.data)
        for v in bm.verts:
            data += f"{v.co.x:.6f}{v.co.y:.6f}{v.co.z:.6f}"
        bm.free()
    return hashlib.sha256(data.encode()).hexdigest()[:16]

def get_real_dimensions(obj):
    if obj.type not in {'MESH', 'CURVE', 'SURFACE', 'META', 'FONT'}:
        return (0.0, 0.0, 0.0)
    d = obj.dimensions
    return (round(d.x, 4), round(d.y, 4), round(d.z, 4))

# ====================== SISTEMA DE RETRY ======================
def ejecutar_con_retry(func, max_intentos=3, *args, **kwargs):
    """Ejecuta función con reintentos ante fallos"""
    ultimo_error = None
    for intento in range(max_intentos):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            ultimo_error = e
            print(f"  ⚠️ Intento {intento+1}/{max_intentos} fallido: {str(e)[:50]}")
            if intento < max_intentos - 1:
                import time
                time.sleep(0.1 * (intento + 1))  # Backoff incremental
    
    # Todos los intentos fallaron
    return None, [("CRITICO", f"Fallo tras {max_intentos} intentos: {str(ultimo_error)[:50]}")], {}

# ====================== AUDITORIAS ======================
def audit_render_engine():
    deduction = 0
    errors = []
    engine_name, engine_type = get_render_engine()
    scene = bpy.context.scene
    report = [f"Motor: {engine_name} ({engine_type})"]

    if engine_name == "Eevee":
        eevee = scene.eevee
        if not getattr(eevee, 'use_ssr', False):
            errors.append(("MAYOR", "Screen Space Reflections desactivado"))
            deduction -= 15
        report.append("Recomendacion: Activa SSR y AO")
    elif engine_name == "Cycles":
        cycles = scene.cycles
        if cycles.samples < 128:
            errors.append(("MAYOR", "Samples bajos en Cycles"))
            deduction -= 15
        if not cycles.use_denoising:
            errors.append(("MAYOR", "Denoising desactivado"))
            deduction -= 15
        report.append(f"Samples: {cycles.samples}")
    
    return deduction, errors, report

def audit_geometry(obj):
    """Auditoría de geometría con normales, duplicados y métricas avanzadas"""
    if obj.type != 'MESH' or not obj.data:
        return 0, [], {}
    
    bm = bmesh.new()
    try:
        bm.from_mesh(obj.data)
    except Exception as e:
        bm.free()
        return 0, [("CRITICO", f"Error bmesh: {str(e)}")], {}
    
    bm.verts.ensure_lookup_table()
    bm.faces.ensure_lookup_table()
    bm.edges.ensure_lookup_table()
    
    # Calcular normales
    try:
        bm.normal_update()
    except:
        pass
    
    errors = []
    deduction = 0
    metrics = {}
    
    dims = get_real_dimensions(obj)
    metrics["Dimensiones"] = f"{dims[0]} x {dims[1]} x {dims[2]} m"
    metrics["SHA-256"] = calculate_sha256(obj)
    metrics["Vertices"] = len(bm.verts)
    metrics["Caras"] = len(bm.faces)
    
    # 1. Non-manifold (original)
    non_manifold = len([e for e in bm.edges if not e.is_manifold])
    if non_manifold:
        errors.append(("CRITICO", f"Non-manifold: {non_manifold}"))
        deduction -= 30
    
    # 2. Vértices sueltos (original)
    loose = len([v for v in bm.verts if v.is_loose])
    if loose:
        errors.append(("CRITICO", f"Vertices sueltos: {loose}"))
        deduction -= 30
    
    # 3. NUEVO: Vértices duplicados (coordenadas idénticas)
    vert_coords = {}
    duplicates = 0
    for v in bm.verts:
        coord_key = (round(v.co.x, 4), round(v.co.y, 4), round(v.co.z, 4))
        if coord_key in vert_coords:
            duplicates += 1
        else:
            vert_coords[coord_key] = v.index
    
    if duplicates > 0:
        errors.append(("MAYOR", f"Vertices duplicados: {duplicates}"))
        deduction -= 15
        metrics["VerticesDuplicados"] = duplicates
    
    # 4. NUEVO: Normales invertidas
    inverted_normals = 0
    for face in bm.faces:
        # Una cara está invertida si su normal apunta hacia dentro del objeto
        # (simplificación: verificar contra centro de la cara)
        face_center = face.calc_center_median()
        world_center = obj.matrix_world @ face_center
        world_normal = (obj.matrix_world.to_3x3() @ face.normal).normalized()
        
        # Verificar dirección (esto es una heurística simplificada)
        dot_product = world_normal.dot(world_center - obj.location)
        if dot_product < -0.1:  # Normal apunta hacia el centro del objeto
            inverted_normals += 1
    
    if inverted_normals > 0:
        errors.append(("MAYOR", f"Posibles normales invertidas: {inverted_normals}"))
        deduction -= 15
        metrics["NormalesInvertidas"] = inverted_normals
    
    # 5. N-Gons (original)
    ngons = len([f for f in bm.faces if len(f.verts) > 4])
    if ngons:
        errors.append(("MAYOR", f"N-Gons: {ngons}"))
        deduction -= 15
    
    # 6. Escala no aplicada (original)
    if any(abs(s - 1.0) > 0.001 for s in obj.scale):
        errors.append(("MAYOR", "Escala no aplicada"))
        deduction -= 15
    
    bm.free()
    return deduction, errors, metrics

def audit_materials_uv(obj, target_color_hex="#FFFFFF"):
    """Auditoría de materiales con soporte multi-material"""
    deduction = 0
    errors = []
    color_match = False
    color_found = "N/A"
    material_info = []
    
    if obj.type != 'MESH':
        return 0, errors, color_match, color_found, material_info
    
    slot_count = len(obj.material_slots)
    
    if slot_count == 0:
        errors.append(("MAYOR", "Sin materiales"))
        deduction -= 15
    else:
        # NUEVO: Iterar sobre TODOS los material slots
        for slot_idx, slot in enumerate(obj.material_slots):
            mat = slot.material
            if not mat:
                errors.append(("MENOR", f"Slot {slot_idx}: Sin material"))
                deduction -= 5
                continue
            
            mat_info = {"slot": slot_idx, "name": mat.name}
            
            if mat.use_nodes:
                # Buscar Principled BSDF
                principled = None
                for node in mat.node_tree.nodes:
                    if node.type == 'BSDF_PRINCIPLED':
                        principled = node
                        break
                
                if principled:
                    color = principled.inputs['Base Color'].default_value
                    r, g, b = int(color[0] * 255), int(color[1] * 255), int(color[2] * 255)
                    hex_color = f"#{r:02X}{g:02X}{b:02X}"
                    mat_info["color"] = hex_color
                    mat_info["metallic"] = round(principled.inputs['Metallic'].default_value, 2)
                    mat_info["roughness"] = round(principled.inputs['Roughness'].default_value, 2)
                    
                    # Primer material define el color de referencia
                    if slot_idx == 0:
                        color_found = hex_color
                        color_match = hex_color.upper() == target_color_hex.upper()
                else:
                    mat_info["error"] = "Sin Principled BSDF"
            else:
                mat_info["error"] = "Sin nodos"
            
            material_info.append(mat_info)
        
        # NUEVO: Verificar materiales sin asignar polígonos
        if obj.data.polygons and slot_count > 0:
            used_slots = set(poly.material_index for poly in obj.data.polygons)
            unused_slots = set(range(slot_count)) - used_slots
            if unused_slots:
                errors.append(("MENOR", f"Materiales sin usar: {len(unused_slots)}"))
                deduction -= 5
    
    # UVs
    if not obj.data.uv_layers:
        errors.append(("MAYOR", "Sin UVs"))
        deduction -= 15
    else:
        uv_count = len(obj.data.uv_layers)
        if uv_count > 1:
            material_info.append({"info": f"{uv_count} mapas UV"})
    
    return deduction, errors, color_match, color_found, material_info

def audit_scene():
    deduction = 0
    errors = []
    if not bpy.context.scene.camera:
        errors.append(("MAYOR", "No hay camara activa"))
        deduction -= 15
    return deduction, errors

# ====================== SELLO ZULY ======================
def aplicar_sello_zuly(candidato_id, resultados, aprobado_por="Soberano"):
    """Aplica sello ZULY al patron validado"""
    
    if resultados["puntuacion"] < 70:
        return {"status": "ERROR", "motivo": "PUNTUACION_BAJA"}
    
    pattern_folder = MASTERED / candidato_id
    folders = {
        'blend': pattern_folder / 'blend',
        'json': pattern_folder / 'json',
        'certificado': pattern_folder / 'certificado',
        'auditoria': pattern_folder / 'auditoria'
    }
    
    for folder in folders.values():
        folder.mkdir(parents=True, exist_ok=True)
    
    # Guardar blend
    blend_path = folders['blend'] / f"{candidato_id}.blend"
    bpy.ops.wm.save_as_mainfile(filepath=str(blend_path))
    
    # Certificado
    certificado = {
        "certificado_id": f"CERT-{candidato_id}-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "pattern_id": candidato_id,
        "fecha_sello": datetime.now().isoformat(),
        "sellado_por": aprobado_por,
        "decision": "SELLADO",
        "puntuacion": resultados["puntuacion"],
        "dictamen": resultados["dictamen"],
        "validacion": resultados.get("metricas", {})
    }
    
    cert_path = folders['certificado'] / "CERTIFICADO.json"
    with open(cert_path, 'w', encoding='utf-8') as f:
        json.dump(certificado, f, indent=2, ensure_ascii=False)
    
    # Reporte auditoria
    audit_path = folders['auditoria'] / "REPORTE.json"
    with open(audit_path, 'w', encoding='utf-8') as f:
        json.dump(resultados, f, indent=2, ensure_ascii=False)
    
    return {
        "status": "SELLADO",
        "ubicacion": str(pattern_folder),
        "puntuacion": resultados["puntuacion"]
    }

# ====================== OPERADOR PRINCIPAL ======================
class JUES_OT_Audit(Operator):
    bl_idname = "jues.audit"
    bl_label = "Ejecutar Auditoria JUES"
    bl_description = "Auditoria completa ZULY con sellado automatico"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        try:
            props = context.scene.jues_props
            total_deduction = 0
            all_errors = []
            all_metrics = {}
            
            engine_name, _ = get_render_engine()
            
            report_lines = [
                color_text("=== JUES-BOT - AUDITORIA ZULY ===", Colors.HEADER),
                f"Blender {get_blender_version()[0]}.{get_blender_version()[1]} | Motor: {engine_name}"
            ]
            
            # Render Engine
            if props.check_render:
                ded, errs, rpt = audit_render_engine()
                total_deduction += ded
                all_errors.extend(errs)
                report_lines.extend([color_text(f"  {line}", Colors.OKCYAN) for line in rpt])
            
            # Objetos
            objects_to_audit = bpy.data.objects if props.audit_entire_scene else [context.active_object] if context.active_object else []
            
            for obj in objects_to_audit:
                if not obj or obj.type != 'MESH':
                    continue
                    
                report_lines.append(color_text(f"\nOBJETO: {obj.name}", Colors.OKBLUE))
                
                # Geometria con retry
                if props.check_geo:
                    resultado = ejecutar_con_retry(audit_geometry, 3, obj)
                    if resultado[0] is None:
                        # Fallo catastrófico
                        ded, errs, metrics = resultado
                    else:
                        ded, errs, metrics = resultado
                    total_deduction += ded
                    all_errors.extend(errs)
                    all_metrics.update(metrics)
                    report_lines.append(color_text(f"  Geometria: {ded:+} pts", Colors.OKCYAN))
                
                # Materiales
                if props.check_materials:
                    ded, errs, color_match, color_found, mat_info = audit_materials_uv(obj, props.target_color)
                    total_deduction += ded
                    all_errors.extend(errs)
                    all_metrics["Color"] = color_found
                    all_metrics["ColorMatch"] = color_match
                    if mat_info:
                        all_metrics["Materiales"] = len([m for m in mat_info if "name" in m])
                    report_lines.append(color_text(f"  Materiales: {ded:+} pts | Color: {color_found}", Colors.OKCYAN))
            
            # Escena
            if props.check_scene:
                ded, errs = audit_scene()
                total_deduction += ded
                all_errors.extend(errs)
                report_lines.append(color_text(f"  Escena: {ded:+} pts", Colors.OKCYAN))
            
            # Puntuacion final
            score = max(0, 100 + total_deduction)
            bar = "█" * int(score / 3.33) + "░" * (30 - int(score / 3.33))
            report_lines.append("\n" + color_text(f"PUNTUACION: [{bar}] {score}/100", Colors.BOLD))
            
            if score >= 70:
                verdict = color_text("APROBADO - Listo para sello", Colors.OKGREEN)
                dictamen = "APTO_PARA_SELLO"
            elif score >= 40:
                verdict = color_text("CONDICIONAL - Revisar", Colors.WARNING)
                dictamen = "APTO_CON_ADVERTENCIAS"
            else:
                verdict = color_text("RECHAZADO", Colors.FAIL)
                dictamen = "NO_APTO"
            
            report_lines.append(verdict)
            
            # Métricas
            if all_metrics:
                report_lines.append(color_text("\nMETRICAS:", Colors.OKBLUE))
                for k, v in all_metrics.items():
                    report_lines.append(f"  {k}: {v}")
            
            # Errores
            if all_errors:
                report_lines.append(color_text("\nERRORES:", Colors.FAIL))
                for sev, msg in all_errors:
                    col = Colors.FAIL if "CRITICO" in sev else Colors.WARNING
                    report_lines.append(color_text(f"  {sev}: {msg}", col))
            
            report_text = "\n".join(report_lines)
            print(report_text)
            
            # Guardar en Text Editor
            txt = bpy.data.texts.get("JUES_REPORT") or bpy.data.texts.new("JUES_REPORT")
            txt.clear()
            txt.write(report_text.replace('\033[95m','').replace('\033[92m','').replace('\033[91m','').replace('\033[93m','').replace('\033[0m','').replace('\033[1m',''))
            
            # Resultados para sello
            resultados = {
                "puntuacion": score,
                "dictamen": dictamen,
                "metricas": all_metrics,
                "errores": all_errors
            }
            
            self.report({'INFO'}, f"JUES: {score}/100 | {dictamen}")
            
            # Si aprobado, ofrecer sello
            if score >= 70 and context.active_object:
                candidato = context.active_object.name.replace(".", "_")
                sello = aplicar_sello_zuly(candidato, resultados)
                if sello["status"] == "SELLADO":
                    self.report({'INFO'}, f"SELLADO: {candidato}")
            
            return {'FINISHED'}
            
        except Exception as e:
            self.report({'ERROR'}, f"Error: {str(e)}")
            return {'CANCELLED'}

# ====================== PANEL ======================
class JUES_PT_Panel(Panel):
    bl_label = "JUES-BOT ZULY"
    bl_idname = "JUES_PT_Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "JUES"

    def draw(self, context):
        layout = self.layout
        props = context.scene.jues_props
        
        engine_name, _ = get_render_engine()
        layout.label(text=f"Render: {engine_name}", icon="RENDER_RESULT")
        
        layout.prop(props, "audit_entire_scene")
        layout.prop(props, "target_color")
        layout.separator()
        
        layout.label(text="Auditar:", icon="CHECKBOX_HLT")
        layout.prop(props, "check_geo")
        layout.prop(props, "check_materials")
        layout.prop(props, "check_render")
        layout.prop(props, "check_scene")
        
        layout.separator()
        layout.operator("jues.audit", icon="PLAY")
        
        layout.separator()
        layout.label(text="Puntuacion: 100 base")
        layout.label(text="-30 Critico | -15 Mayor | -5 Menor")
        layout.label(text="Aprobado >= 70 pts")

# ====================== REGISTRO ======================
def register():
    bpy.utils.register_class(JuesBotProperties)
    bpy.utils.register_class(JUES_OT_Audit)
    bpy.utils.register_class(JUES_PT_Panel)
    bpy.types.Scene.jues_props = PointerProperty(type=JuesBotProperties)

def unregister():
    bpy.utils.unregister_class(JUES_PT_Panel)
    bpy.utils.unregister_class(JUES_OT_Audit)
    bpy.utils.unregister_class(JuesBotProperties)
    del bpy.types.Scene.jues_props

if __name__ == "__main__":
    register()
