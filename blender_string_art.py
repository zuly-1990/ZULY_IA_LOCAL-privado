import bpy
import json
import math
import os

# Configuracion
NUM_CLAVOS = 288
RADIO_TABLERO = 5.0 # Metros
GROSOR_HILO = 0.005 # Metros
ALTURA_CLAVO = 0.1 # Metros
RADIO_CLAVO = 0.02 # Metros

# Ruta al JSON (Asegurate de que sea la ruta correcta donde se genero el json)
JSON_PATH = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\secuencia_clavos.json"

def limpiar_escena():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

def crear_clavos():
    clavos_coords = []
    
    # Crear un clavo base
    bpy.ops.mesh.primitive_cylinder_add(radius=RADIO_CLAVO, depth=ALTURA_CLAVO, location=(0, 0, ALTURA_CLAVO/2))
    clavo_base = bpy.context.active_object
    clavo_base.name = "Clavo_Base"
    
    # Crear un material metalico para los clavos
    mat_metal = bpy.data.materials.new(name="Material_Clavo")
    mat_metal.use_nodes = True
    bsdf = mat_metal.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Metallic'].default_value = 1.0
        bsdf.inputs['Roughness'].default_value = 0.2
    clavo_base.data.materials.append(mat_metal)
    
    # Generar los 288 clavos en circulo
    for i in range(NUM_CLAVOS):
        angulo = 2.0 * math.pi * i / NUM_CLAVOS - math.pi / 2.0
        x = RADIO_TABLERO * math.cos(angulo)
        y = RADIO_TABLERO * math.sin(angulo)
        clavos_coords.append((x, y, ALTURA_CLAVO)) # El hilo ira en la punta del clavo
        
        # Instanciar clavo
        nuevo_clavo = clavo_base.copy()
        nuevo_clavo.data = clavo_base.data.copy()
        nuevo_clavo.location = (x, y, ALTURA_CLAVO/2)
        bpy.context.collection.objects.link(nuevo_clavo)
        
    # Ocultar el original
    bpy.data.objects.remove(clavo_base)
    
    return clavos_coords

def crear_hilo(clavos_coords, secuencia):
    # Crear una curva
    curve_data = bpy.data.curves.new(name="Hilo_StringArt", type='CURVE')
    curve_data.dimensions = '3D'
    
    # Añadir un spline poligonal
    spline = curve_data.splines.new(type='POLY')
    spline.points.add(len(secuencia) - 1)
    
    # Asignar coordenadas
    for idx, clavo_id in enumerate(secuencia):
        # Para que el hilo no atraviese los clavos magicamente, le damos una altura aleatoria minima
        # simulando como se apilan los hilos
        altura_hilo = ALTURA_CLAVO - (idx * 0.00002) 
        
        x, y, _ = clavos_coords[clavo_id]
        spline.points[idx].co = (x, y, altura_hilo, 1.0)
        
    # Crear el objeto curva
    curve_obj = bpy.data.objects.new("Hilo_StringArt_Obj", curve_data)
    bpy.context.collection.objects.link(curve_obj)
    
    # Darle grosor 3D al hilo
    curve_data.bevel_depth = GROSOR_HILO
    curve_data.bevel_resolution = 2
    
    # Material del hilo
    mat_hilo = bpy.data.materials.new(name="Material_Hilo")
    mat_hilo.use_nodes = True
    bsdf = mat_hilo.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (0.01, 0.01, 0.01, 1) # Negro muy oscuro
        bsdf.inputs['Roughness'].default_value = 0.9 # Hilo mate
    curve_obj.data.materials.append(mat_hilo)

def main():
    if not os.path.exists(JSON_PATH):
        print(f"ERROR: No se encontro el archivo JSON en {JSON_PATH}")
        return
        
    print("Limpiando escena...")
    limpiar_escena()
    
    print("Creando 288 clavos...")
    clavos_coords = crear_clavos()
    
    print("Cargando secuencia de hilos...")
    with open(JSON_PATH, 'r') as f:
        secuencia = json.load(f)
        
    print(f"Tejiendo {len(secuencia)} pasos de hilo...")
    crear_hilo(clavos_coords, secuencia)
    
    print("¡String Art 3D completado!")

if __name__ == "__main__":
    main()
