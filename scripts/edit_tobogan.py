import bpy
import math

filepath = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\ZULY_PROJECTS\pruebas\rube_goldberg_zuly_real.blend"

try:
    bpy.ops.wm.open_mainfile(filepath=filepath)
    
    # Asegurar Object Mode
    if bpy.context.object and bpy.context.object.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

    # 1. Eliminar rampa vieja
    old_ramp = bpy.data.objects.get('Ramp')
    if old_ramp:
        bpy.data.objects.remove(old_ramp, do_unlink=True)

    # 2. Material de rampa
    mat_ramp = bpy.data.materials.get('Ramp_Mat')

    # 3. Crear Nueva Rampa Larga
    bpy.ops.mesh.primitive_cube_add(location=(0, 15, 10), scale=(3, 20, 0.5))
    ramp_base = bpy.context.active_object
    ramp_base.name = 'Long_Ramp_Base'

    # 4. Crear Barandas Laterales (Bordes)
    bpy.ops.mesh.primitive_cube_add(location=(-2.75, 15, 11), scale=(0.25, 20, 1.5))
    rail_L = bpy.context.active_object
    rail_L.name = 'Ramp_Rail_Left'
    
    bpy.ops.mesh.primitive_cube_add(location=(2.75, 15, 11), scale=(0.25, 20, 1.5))
    rail_R = bpy.context.active_object
    rail_R.name = 'Ramp_Rail_Right'

    # Rotar el conjunto e integrar físicas
    ramp_parts = [ramp_base, rail_L, rail_R]
    # Emparentar rieles a la base para rotarlos juntos fácilmente
    rail_L.parent = ramp_base
    rail_R.parent = ramp_base
    
    # Inclinacion de Tobogán
    ramp_base.rotation_euler = (math.radians(30), 0, 0)
    # Re-ajustar altura
    ramp_base.location = (0, 12, 10)

    # Aplicar escalas, físicas y material
    for p in ramp_parts:
        # Desemparentar manteniendo la transformacion para las fisicas
        bpy.context.view_layer.objects.active = p
        bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
        
        if mat_ramp:
            p.data.materials.append(mat_ramp)
            
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        
        bpy.ops.rigidbody.object_add()
        p.rigid_body.type = 'PASSIVE'
        p.rigid_body.collision_shape = 'MESH'
        p.rigid_body.restitution = 0.4
        p.rigid_body.friction = 0.5

    # 5. DADOS: Clonar hasta tener 5 (o reposicionar los existentes)
    # Buscar dados existentes
    existing_dice = []
    for obj in bpy.data.objects:
        if "RoundDie" in obj.name:
            existing_dice.append(obj)
            
    # Clonacion inteligente
    target_count = 5
    current_count = len(existing_dice)
    
    if current_count > 0:
        source_die = existing_dice[0]
        while current_count < target_count:
            # Duplicar
            bpy.context.view_layer.objects.active = source_die
            source_die.select_set(True)
            bpy.ops.object.duplicate_move()
            new_die = bpy.context.active_object
            current_count += 1
            new_die.name = f"RoundDie_{current_count}"
            existing_dice.append(new_die)
            source_die.select_set(False)

    # Reposicionar todos los dados en la cima de la rampa
    # La parte superior de la rampa está cerca de Y=28, Z=19
    start_y = 26
    start_z = 21
    
    for i, die in enumerate(existing_dice):
        die.location = (0, start_y - (i * 2.5), start_z + (i * 2.0))
        # Asegurar físicas
        if not die.rigid_body:
            bpy.context.view_layer.objects.active = die
            bpy.ops.rigidbody.object_add()
            die.rigid_body.type = 'ACTIVE'
            die.rigid_body.collision_shape = 'SPHERE'
            die.rigid_body.mass = 1.0
            die.rigid_body.restitution = 0.6
            
    # Ajustar Cajón Inferior 
    cajon = bpy.data.objects.get('SinglePiece_Box')
    if cajon:
        # Mover un poco hacia adelante para cachar la rampa más larga
        cajon.location = (0, -10, -1)

    bpy.ops.wm.save_mainfile()
    print("EXITO: Tobogan y Clones creados.")
    
except Exception as e:
    print(f"ERROR: {e}")
