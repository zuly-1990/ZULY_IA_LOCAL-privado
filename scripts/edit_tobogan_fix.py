import bpy
import math

filepath = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\ZULY_PROJECTS\pruebas\rube_goldberg_zuly_real.blend"

try:
    bpy.ops.wm.open_mainfile(filepath=filepath)
    if bpy.context.object and bpy.context.object.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

    # 1. Eliminar pista vieja y barandas si existen
    for n in ['Long_Ramp_Base', 'Ramp_Rail_Left', 'Ramp_Rail_Right']:
        obj = bpy.data.objects.get(n)
        if obj:
            bpy.data.objects.remove(obj, do_unlink=True)

    # 2. Material de rampa
    mat_ramp = bpy.data.materials.get('Ramp_Mat')

    # 3. CREAR TOBOGÁN DE UNA SOLA PIEZA (Forma de U)
    # Cubo base (4x25x2 en scale = ancho total 8, largo 50, alto 4)
    bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0), scale=(3, 20, 1.5))
    tobogan = bpy.context.active_object
    tobogan.name = 'Solid_Tobogan'
    
    # Cubo cortador para hacer el ahuecado de la pista
    # Lo subimos un poco (Z=0.5) para que no corte el fondo
    bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0.5), scale=(2.5, 21, 1.5))
    cutter = bpy.context.active_object
    cutter.name = 'Tobogan_Hollow_Cutter'
    
    # Aplicar booleano
    bpy.context.view_layer.objects.active = tobogan
    mod = tobogan.modifiers.new(name="Tobogan_U", type='BOOLEAN')
    mod.operation = 'DIFFERENCE'
    mod.object = cutter
    bpy.ops.object.modifier_apply(modifier=mod.name)
    bpy.data.objects.remove(cutter, do_unlink=True)
    
    # Rotar y posicionar tobogán
    tobogan.rotation_euler = (math.radians(20), 0, 0)
    tobogan.location = (0, 10, 12)
    
    if mat_ramp:
        tobogan.data.materials.append(mat_ramp)
        
    # Aplicar escala rotada
    bpy.context.view_layer.objects.active = tobogan
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    # Físicas del tobogán
    bpy.ops.rigidbody.object_add()
    tobogan.rigid_body.type = 'PASSIVE'
    tobogan.rigid_body.collision_shape = 'MESH'
    tobogan.rigid_body.restitution = 0.2
    tobogan.rigid_body.friction = 0.5

    # 4. REPOSICIONAR DADOS CON PRECISIÓN MATEMÁTICA
    # Buscar todos los dados (esperamos 5)
    dados = [obj for obj in bpy.data.objects if "RoundDie" in obj.name]
    
    # Para ubicarlos perfectamente SOBRE la rampa girada, 
    # los emparentamos sin "keep transform", seteamos local cords, y desemparentamos.
    for i, die in enumerate(dados):
        # Mover al centro del objeto tobogan localmente
        # Local Z debe ser suficiente para que el radio 1.0 toque el suelo del U-shape.
        # En el cubo base (scale Z 1.5 -> height 3), bottom is -1.5. El ahuecado estaba en Z_scale=1.5 con offset = 0.5 local...
        # Un valor empírico seguro es z=0.5 a 1.0 local, intentemos local_Y espaciado, y local_X = 0
        die.parent = tobogan
        die.matrix_parent_inverse = tobogan.matrix_world.inverted()
        
        local_y = 15 - (i * 2.5) # De Y=15 a Y=5
        local_z = 0.5 # Apenas sobre la madera
        die.location = (0, local_y, local_z)
        
        # limpiar fuerzas residuales físicas para que no salgan volando
        if die.rigid_body:
            die.rigid_body.restitution = 0.3 # Bajar rebote un poco
            die.rigid_body.mass = 2.0

    # Ahora que están en su sitio, desemparentar manteniendo la forma global
    for die in dados:
        die.select_set(True)
        bpy.context.view_layer.objects.active = die
    bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
    # Deseleccionar
    bpy.ops.object.select_all(action='DESELECT')

    # Guardar silenciosamente
    bpy.ops.wm.save_mainfile()
    print("EXITO: Tobogan de una pieza reconstruido y dados alineados milimetricamente.")

except Exception as e:
    print(f"ERROR: {e}")
