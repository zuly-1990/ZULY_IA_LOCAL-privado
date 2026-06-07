import bpy
import os
import sys
import math

BASE_DIR = r'C:\Users\Admin\Desktop\ZULY_IA_LOCAL'
sys.path.append(BASE_DIR)

from core.adapters.blender_adapter import BlenderAdapter
from core.validation.common_sense_auditor import CommonSenseAuditor

def build_smart_rural_house_v2():
    adapter = BlenderAdapter(bpy)
    auditor = CommonSenseAuditor()
    adapter.clear_scene()
    
    output_path = os.path.join(BASE_DIR, 'ZULY_PROJECTS', 'zuly_rural_inteligente_v2.blend')
    
    print("=== ZULY: MODELADO CON SENTIDO COMÚN Y GEOMETRÍA AVANZADA ===")
    
    # 1. Auditoría
    building_data = {
        "levels": [
            {
                "name": "Planta Baja - Casa Rural",
                "is_habitable": True,
                "rooms": [{"type": "living_space", "doors": 1, "windows": 2}],
                "slabs": [{"overhang_length": 1.0}]
            }
        ],
        "vertical_circulation": []
    }
    
    report = auditor.audit_building(building_data)
    if not report["passed"]:
        print("🚨 ERROR: Lógica fallida.")
        return
        
    # 2. Construcción
    adapter.create_material("Ladrillo_Rustico", color=(0.8, 0.4, 0.3), roughness=0.9)
    adapter.create_material("Teja_Arcilla", color=(0.6, 0.2, 0.1), roughness=0.8)
    adapter.create_material("Madera_Puerta", color=(0.3, 0.2, 0.1), roughness=0.7)
    adapter.create_material("Cristal", color=(0.7, 0.8, 0.9), roughness=0.1, alpha=0.5, transmission=1.0)
    
    ancho = 6.0
    largo = 8.0
    alto = 3.0
    
    # Muros
    adapter.create_primitive('cube', name="Cuerpo_Casa", location=[0, 0, alto/2])
    adapter.set_dimensions("Cuerpo_Casa", [ancho, largo, alto])
    adapter.apply_material("Cuerpo_Casa", "Ladrillo_Rustico")
    
    adapter.create_primitive('cube', name="Vaciador", location=[0, 0, alto/2])
    adapter.set_dimensions("Vaciador", [ancho-0.6, largo-0.6, alto-0.2])
    adapter.boolean_cut("Cuerpo_Casa", "Vaciador", operation='DIFFERENCE')
    adapter.fix_mesh("Cuerpo_Casa", remove_doubles=True, recalculate_normals=True)
    
    # 3. EL TECHO (Geometría Booleana Avanzada)
    print("Esculpiendo un techo a dos aguas perfecto usando Booleanos cruzados...")
    alto_techo = 2.5
    voladizo = 0.8
    # Bloque macizo para el techo
    adapter.create_primitive('cube', name="Techo_Macizo", location=[0, 0, alto + (alto_techo/2)])
    adapter.set_dimensions("Techo_Macizo", [ancho + (voladizo*2), largo + (voladizo*2), alto_techo])
    
    # Vaciadores angulares para esculpir la pendiente (Pitch)
    # Cortador Derecho
    adapter.create_primitive('cube', name="Corte_Derecho", location=[ancho/2 + 1.0, 0, alto + alto_techo])
    adapter.set_dimensions("Corte_Derecho", [ancho, largo + 4, alto_techo * 2])
    obj_cd = bpy.data.objects.get("Corte_Derecho")
    obj_cd.rotation_euler = (0, math.radians(35), 0)
    
    # Cortador Izquierdo
    adapter.create_primitive('cube', name="Corte_Izquierdo", location=[-(ancho/2 + 1.0), 0, alto + alto_techo])
    adapter.set_dimensions("Corte_Izquierdo", [ancho, largo + 4, alto_techo * 2])
    obj_ci = bpy.data.objects.get("Corte_Izquierdo")
    obj_ci.rotation_euler = (0, math.radians(-35), 0)
    
    adapter.boolean_cut("Techo_Macizo", "Corte_Derecho", operation='DIFFERENCE')
    adapter.boolean_cut("Techo_Macizo", "Corte_Izquierdo", operation='DIFFERENCE')
    adapter.apply_material("Techo_Macizo", "Teja_Arcilla")
    adapter.fix_mesh("Techo_Macizo", remove_doubles=True, recalculate_normals=True)
    
    # Vaciado del interior del techo para no aplastar el interior
    adapter.create_primitive('cube', name="Vaciador_Techo", location=[0, 0, alto + (alto_techo/2) - 0.5])
    adapter.set_dimensions("Vaciador_Techo", [ancho-0.4, largo-0.4, alto_techo])
    adapter.boolean_cut("Techo_Macizo", "Vaciador_Techo", operation='DIFFERENCE')
    adapter.fix_mesh("Techo_Macizo", remove_doubles=True, recalculate_normals=True)

    # 4. Puerta y Ventanas
    adapter.create_primitive('cube', name="Hueco_Puerta", location=[0, -(largo/2), 1.05])
    adapter.set_dimensions("Hueco_Puerta", [1.2, 1.0, 2.1])
    adapter.boolean_cut("Cuerpo_Casa", "Hueco_Puerta", operation='DIFFERENCE')
    
    adapter.create_primitive('cube', name="Puerta_Madera", location=[0, -(largo/2), 1.05])
    adapter.set_dimensions("Puerta_Madera", [1.1, 0.2, 2.05])
    adapter.apply_material("Puerta_Madera", "Madera_Puerta")
    
    for x_pos in [-ancho/4, ancho/4]:
        name_h = f"Hueco_Ven_{x_pos}"
        adapter.create_primitive('cube', name=name_h, location=[x_pos, (largo/2), 1.5])
        adapter.set_dimensions(name_h, [1.5, 1.0, 1.2])
        adapter.boolean_cut("Cuerpo_Casa", name_h, operation='DIFFERENCE')
        
        name_v = f"Cristal_Ven_{x_pos}"
        adapter.create_primitive('cube', name=name_v, location=[x_pos, (largo/2), 1.5])
        adapter.set_dimensions(name_v, [1.4, 0.1, 1.1])
        adapter.apply_material(name_v, "Cristal")

    adapter.fix_mesh("Cuerpo_Casa", remove_doubles=True, recalculate_normals=True)

    print("[3/3] Guardando y Finalizando...")
    bpy.ops.wm.save_as_mainfile(filepath=output_path)
    print(f"=== ZULY EXITO: Casa Rural v2 guardada en {output_path} ===")

if __name__ == "__main__":
    build_smart_rural_house_v2()
