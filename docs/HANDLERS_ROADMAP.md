# Roadmap: 25 Handlers Arquitectónicos Prioritarios

Esta lista contiene los primeros 25 handlers seleccionados para implementar en ZULY, cubriendo principalmente selección, gestión de escena y modelado de precisión.

## Selección y Gestión de Escena
- blender.select_object_by_name
- blender.select_all_by_type
- blender.deselect_all
- blender.delete_object
- blender.rename_object
- blender.duplicate_object
- blender.hide_object
- blender.unhide_all
- blender.join_objects
- blender.group_in_collection

## Creación Avanzada de Objetos
- blender.create_text
- blender.create_curve_bezier
- blender.create_grid
- blender.convert_to_mesh
- blender.import_svg

## Modelado de Precisión (Modo Edición)
- blender.enter_edit_mode
- blender.exit_edit_mode
- blender.select_faces_by_index
- blender.select_edges_by_condition
- blender.select_vertices_by_position
- blender.extrude_faces
- blender.inset_faces
- blender.create_loop_cut
- blender.merge_vertices
- blender.delete_faces

---

Cada handler será implementado en `core/commands/` siguiendo la plantilla estándar y registrado en el sistema de comandos.
