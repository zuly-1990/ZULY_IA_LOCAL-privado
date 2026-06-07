
import bpy
import os
import sys

BASE_DIR = r'C:\Users\Admin\Desktop\ZULY_IA_LOCAL'
sys.path.append(BASE_DIR)

from core.adapters.blender_adapter import BlenderAdapter

def sculpted_building_v2():
    """
    DEMO V2: Edificio Esculpido con orientacion de caras corregida.
    Usa extrude/inset/bevel/boolean con vectores de normal correctos.
    """
    adapter = BlenderAdapter(bpy)
    pruebas_dir = os.path.join(BASE_DIR, 'ZULY_PROJECTS', 'pruebas')
    output_path = os.path.join(pruebas_dir, 'sculpted_building_v2.blend')

    adapter.clear_scene()
    print("=== ZULY EDIT MODE V2: ORIENTACION CORREGIDA ===")

    # ---------------------------------------------------------------
    # 1. MURO PRINCIPAL (8m ancho x 6m alto x 0.4m grosor)
    # ---------------------------------------------------------------
    print("[1/7] Creando muro principal...")
    adapter.create_primitive('cube', name="Muro_Principal", location=[0, 0, 3])
    muro = bpy.data.objects["Muro_Principal"]
    muro.dimensions = [8, 0.4, 6]

    # ---------------------------------------------------------------
    # 2. PERFORAR VENTANAS con Boolean Cut (huecos reales)
    # ---------------------------------------------------------------
    print("[2/7] Perforando 3 ventanas con Boolean Cut...")
    for i in range(3):
        win_name = f"Hueco_{i}"
        x_pos = -2.5 + (i * 2.5)
        adapter.create_primitive('cube', name=win_name, location=[x_pos, 0, 3.5])
        hueco = bpy.data.objects[win_name]
        hueco.dimensions = [1.5, 0.8, 2.0]
        adapter.boolean_cut("Muro_Principal", win_name, operation='DIFFERENCE')

    # ---------------------------------------------------------------
    # 3. PERFORAR PUERTA con Boolean Cut
    # ---------------------------------------------------------------
    print("[3/7] Perforando puerta...")
    adapter.create_primitive('cube', name="Hueco_Puerta", location=[0, 0, 1.3])
    puerta = bpy.data.objects["Hueco_Puerta"]
    puerta.dimensions = [1.2, 0.8, 2.6]
    adapter.boolean_cut("Muro_Principal", "Hueco_Puerta", operation='DIFFERENCE')

    # ---------------------------------------------------------------
    # 4. INSET en cara frontal (crear relieve de fachada)
    # ---------------------------------------------------------------
    print("[4/7] Inset frontal para moldura de fachada...")
    adapter.inset_faces("Muro_Principal", thickness=0.12, depth=0.03, face_select='FRONT')

    # ---------------------------------------------------------------
    # 5. BEVEL en las aristas (esquinas suavizadas)
    # ---------------------------------------------------------------
    print("[5/7] Biselando aristas del muro...")
    adapter.bevel_edges("Muro_Principal", width=0.02, segments=2)

    # ---------------------------------------------------------------
    # 6. TECHO con extrusion lateral (cornisa)
    # ---------------------------------------------------------------
    print("[6/7] Creando techo con cornisa extruida...")
    adapter.create_primitive('cube', name="Techo", location=[0, 0, 6.2])
    techo = bpy.data.objects["Techo"]
    techo.dimensions = [9, 1.0, 0.3]
    # Extruir cara FRONTAL hacia afuera (cornisa frontal)
    adapter.extrude_faces("Techo", offset=0.3, face_select='FRONT')
    # Extruir cara superior ligeramente (relieve de techo)
    adapter.extrude_faces("Techo", offset=0.08, face_select='TOP')

    # ---------------------------------------------------------------
    # 7. SUELO + MATERIALES
    # ---------------------------------------------------------------
    print("[7/7] Suelo y materiales...")
    adapter.create_primitive('plane', name="Suelo", location=[0, 0, 0])
    suelo = bpy.data.objects["Suelo"]
    suelo.dimensions = [14, 14, 0]

    # Materiales
    adapter.create_material("Mat_Concreto", color=(0.72, 0.69, 0.66), roughness=0.85)
    adapter.apply_material("Muro_Principal", "Mat_Concreto")
    
    adapter.create_material("Mat_Techo", color=(0.12, 0.12, 0.15), roughness=0.3, metallic=0.4)
    adapter.apply_material("Techo", "Mat_Techo")
    
    adapter.create_material("Mat_Suelo", color=(0.45, 0.42, 0.38), roughness=0.95)
    adapter.apply_material("Suelo", "Mat_Suelo")

    # Luz
    adapter.create_light('SUN', name="Sol", location=[5, -5, 10], energy=3.0)

    # ---------------------------------------------------------------
    # EXPORTAR
    # ---------------------------------------------------------------
    bpy.ops.wm.save_as_mainfile(filepath=output_path)
    
    if os.path.exists(output_path):
        size = os.path.getsize(output_path)
        print(f"=== EXITO! sculpted_building_v2.blend ({size} bytes) ===")
        
        # Conteo de vertices para demostrar complejidad
        obj = bpy.data.objects.get("Muro_Principal")
        if obj and obj.type == 'MESH':
            verts = len(obj.data.vertices)
            faces = len(obj.data.polygons)
            print(f"Muro: {verts} vertices, {faces} caras (vs. 8 vertices de un cubo original)")
    else:
        print("ERROR: Archivo no guardado")

if __name__ == "__main__":
    sculpted_building_v2()
