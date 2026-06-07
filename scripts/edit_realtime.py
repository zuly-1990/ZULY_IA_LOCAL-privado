import bpy
import os

filepath = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\ZULY_PROJECTS\pruebas\rube_goldberg_zuly_real.blend"

try:
    bpy.ops.wm.open_mainfile(filepath=filepath)
    
    cajon = bpy.data.objects.get('SinglePiece_Box')
    if cajon:
        # Modo objeto
        if bpy.context.object and bpy.context.object.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')

        # El cajon tiene location Y=-8, scale_Y=9 -> su pared frontal esta entre Y=0 y Y=2.
        # Haremos un cortador en Y=1 ancho suficiente para que pasen las esferas.
        # Sphere radius is 1.0 -> diameter 2.0. Ramp is at X=0. 
        # So we need a hole at X=0, Y=1, Z=1 of at least width 4.
        bpy.ops.mesh.primitive_cube_add(location=(0, 1.0, 1.0), scale=(3.5, 3.0, 5.0))
        hole_cutter = bpy.context.active_object
        hole_cutter.name = 'Entrance_Hole_Cutter'

        bpy.context.view_layer.objects.active = cajon
        mod = cajon.modifiers.new(name="Entrance_Hole", type='BOOLEAN')
        mod.operation = 'DIFFERENCE'
        mod.object = hole_cutter
        
        # Aplicamos el Booleano
        bpy.ops.object.modifier_apply(modifier=mod.name)
        
        # Limpiamos
        bpy.data.objects.remove(hole_cutter, do_unlink=True)
        
        # Guardar cambios silenciosamente para el "tiempo real"
        bpy.ops.wm.save_mainfile()
        print("EXITO: Agujero creado en "+filepath)
    else:
        print("ERROR: Objeto SinglePiece_Box no encontrado.")
        
except Exception as e:
    print(f"ERROR: {e}")
