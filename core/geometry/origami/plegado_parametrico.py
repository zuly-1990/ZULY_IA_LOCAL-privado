import bpy
import sys
import json
import math

# ==========================================
# ZULY ORIGAMI MODULE
# Creado para la transformacion parametrica de objetos (Ej: Silla -> Mesa)
# ==========================================

def init_origami_scene():
    """Limpia la escena de Blender y prepara el lienzo de Origami"""
    bpy.ops.wm.read_factory_settings(use_empty=True)
    
def generate_folding_pattern(base_geometry_type, output_path):
    """
    Genera un patron de dobleces basado en una forma de entrada.
    Este esqueleto estara destinado a algoritmos de transformacion parametrica.
    """
    init_origami_scene()
    
    # [AQUI IRA EL ALGORITMO PARAMETRICO DEL USUARIO]
    # Ejemplo: Crear un plano, subdividirlo y aplicar riggings/shapekeys de doblez
    
    print(f"[ORIGAMI] Generando patrón base para: {base_geometry_type}")
    
    # Crear un plano base representativo por ahora
    bpy.ops.mesh.primitive_plane_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0))
    obj = bpy.context.active_object
    obj.name = "Origami_Base_Sheet"
    
    # Guardar
    bpy.ops.wm.save_as_mainfile(filepath=output_path)
    print(f"✅ Modelo de Origami guardado en {output_path}")

if __name__ == "__main__":
    # Logica CLI basica
    if len(sys.argv) >= 5 and sys.argv[-3] == "--origami":
        # Argumentos: blender -b -P plegado_parametrico.py -- --origami <tipo> <output_blend>
        tipo = sys.argv[-2]
        output = sys.argv[-1]
        generate_folding_pattern(tipo, output)
    else:
        print("Uso interno de Blender o argumentos incompletos.")
