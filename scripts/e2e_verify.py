
from core.adapters.mock_adapter import MockAdapter
from core.commands.blender_handlers.primitives import create_cube_handler
from core.commands.blender_handlers.transforms import move_object_handler
from core.commands.blender_handlers.selection import delete_object_handler
from core.utils.logging import log_info

def run_e2e_test():
    adapter = MockAdapter()
    log_info("--- INICIO TEST E2E ---")
    
    # 1. Crear
    r1 = create_cube_handler({'name': 'TestCube', 'location': [0,0,0], 'color': 'red'}, adapter=adapter)
    print(f"CREAR: {r1.get('success')} | Obj: {r1.get('object_name')}")
    
    # 2. Mover
    r2 = move_object_handler({'name': 'TestCube', 'location': [5,0,0]}, adapter=adapter)
    print(f"MOVER: {r2.get('success')} | Loc: {r2.get('new_location')}")
    
    # 3. Borrar
    r3 = delete_object_handler({'name': 'TestCube'}, adapter=adapter)
    print(f"BORRAR: {r3.get('success')} | Effect: {r3.get('effect')}")
    
    # 4. Verificar
    scene = adapter.get_scene_state()
    count = len(scene.get('objects', []))
    print(f"OBJETOS FINALES: {count}")
    
    if r1.get('success') and r2.get('success') and r3.get('success') and count == 0:
        print("🟢 E2E PIPELINE OK")
        return True
    else:
        print("🔴 E2E PIPELINE FAIL")
        return False

if __name__ == "__main__":
    run_e2e_test()
