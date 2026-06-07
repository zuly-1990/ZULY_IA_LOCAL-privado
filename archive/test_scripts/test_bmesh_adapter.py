import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.absolute()))
from core.adapters.blender_adapter import BlenderAdapter
import bpy

def run_test():
    adapter = BlenderAdapter(bpy_module=bpy)
    print("Iniciando pruebas bmesh en adaptador...")
    
    # Limpiar escena
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
    # Cubos
    res1 = adapter.create_cube(location=[0, 0, 0], scale=1.0)
    print("✅ Cube:", res1.get('payload', res1))
    
    # Esfera
    res2 = adapter.create_sphere(location=[3, 0, 0], radius=1.5)
    print("✅ Sphere:", res2.get('payload', res2))
    
    # Plane
    res3 = adapter.create_plane(location=[-3, 0, 0], scale=[2,2,2])
    print("✅ Plane:", res3.get('payload', res3))
    
    # Cylinder
    res4 = adapter.create_cylinder(location=[0, 3, 0], radius=0.5)
    print("✅ Cylinder:", res4.get('payload', res4))
    
    # Cone
    res5 = adapter.create_cone(location=[0, -3, 0], radius=1.5)
    print("✅ Cone:", res5.get('payload', res5))
    
    # Guardar para inspeccion visual
    out_path = Path("ZULY_LAB/resultados_zuly/test_bmesh.blend").absolute()
    bpy.ops.wm.save_as_mainfile(filepath=str(out_path))
    print(f"✓ Guardado en {out_path}")

if __name__ == "__main__":
    run_test()
