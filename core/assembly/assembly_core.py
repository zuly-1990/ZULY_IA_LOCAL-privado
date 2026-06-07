"""
assembly_core.py

FASE 19: Orquestador de ensamblaje de estructuras compuestas.

Construye estructuras a partir de múltiples primitivas relacionadas
jerárquicamente y posicionadas relativamente.
"""

from typing import Dict, Any, List, Optional
from core.adapters import get_engine_adapter
from core.utils.logging import log_info, log_debug, log_warning, log_error


class AssemblyCore:
    """
    Orquestador de ensamblaje de estructuras compuestas.
    
    Responsabilidades:
    - Crear múltiples primitivas
    - Establecer relaciones parent/child
    - Aplicar alineaciones relativas
    - Validar coherencia estructural
    """
    
    def __init__(self, adapter=None):
        """
        Inicializa el AssemblyCore.
        
        Args:
            adapter: EngineAdapter a usar (si None, usa get_engine_adapter())
        """
        self.adapter = adapter or get_engine_adapter()
        log_debug("AssemblyCore inicializado")
    
    def create_structure(self, structure_def: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crea una estructura compuesta desde definición.
        
        Args:
            structure_def: {
                'name': str,
                'components': [
                    {
                        'id': str,  # Identificador único dentro de la estructura
                        'type': 'cube'|'sphere'|'cylinder'|...,
                        'location': [x, y, z],
                        'scale': float | [x, y, z],
                        'parent': str (id de otro componente) | None,
                        'align_to': str (id de otro componente) | None,
                        'align_mode': 'top'|'bottom'|... (si align_to está presente)
                    }
                ]
            }
        
        Returns:
            {
                'success': bool,
                'structure_name': str,
                'created_objects': [str],  # Nombres reales en escena
                'component_mapping': {id: object_name},
                'error': str (opcional)
            }
        """
        log_info(f"🏗️ Construyendo estructura: {structure_def.get('name', 'sin_nombre')}")
        
        components = structure_def.get('components', [])
        if not components:
            return {
                'success': False,
                'error': 'No se proporcionaron componentes'
            }
        
        created_objects = []
        component_mapping = {}  # {id: object_name}
        errors = []
        
        # FASE 1: Crear todas las primitivas
        log_debug(f"📦 Fase 1: Creando {len(components)} primitivas")
        for component in components:
            comp_id = component.get('id')
            comp_type = component.get('type', 'cube')
            location = component.get('location', [0, 0, 0])
            scale = component.get('scale', 1.0)
            
            # Crear primitiva
            result = self.adapter.create_primitive(
                comp_type,
                location=location,
                scale=scale
            )
            
            if not result.get('success', False):
                error_msg = f"Error creando {comp_type} (id: {comp_id}): {result.get('error', 'unknown')}"
                log_warning(error_msg)
                errors.append(error_msg)
                continue
            
            object_name = result.get('object_name')
            created_objects.append(object_name)
            component_mapping[comp_id] = object_name
            log_debug(f"  ✓ {comp_id} → {object_name}")
        
        if not created_objects:
            return {
                'success': False,
                'error': 'No se pudo crear ninguna primitiva',
                'details': errors
            }
        
        # FASE 2: Establecer jerarquías (parent/child)
        log_debug("🔗 Fase 2: Estableciendo jerarquías")
        hierarchy_count = 0
        for component in components:
            comp_id = component.get('id')
            parent_id = component.get('parent')
            
            if not parent_id:
                continue
            
            # Verificar que tanto hijo como padre fueron creados
            if comp_id not in component_mapping or parent_id not in component_mapping:
                log_warning(f"  ⚠️ Relación {comp_id} → {parent_id} omitida (uno no existe)")
                continue
            
            child_name = component_mapping[comp_id]
            parent_name = component_mapping[parent_id]
            
            result = self.adapter.set_parent(child_name, parent_name, keep_transform=True)
            
            if result.get('success', False):
                log_debug(f"  ✓ {comp_id} → {parent_id}")
                hierarchy_count += 1
            else:
                log_warning(f"  ⚠️ Error en jerarquía {comp_id} → {parent_id}: {result.get('error')}")
        
        log_debug(f"  Jerarquías establecidas: {hierarchy_count}")
        
        # FASE 3: Aplicar alineaciones
        log_debug("📐 Fase 3: Aplicando alineaciones")
        alignment_count = 0
        for component in components:
            comp_id = component.get('id')
            align_to = component.get('align_to')
            align_mode = component.get('align_mode', 'center')
            
            if not align_to:
                continue
            
            # Verificar que tanto target como reference existen
            if comp_id not in component_mapping or align_to not in component_mapping:
                log_warning(f"  ⚠️ Alineación {comp_id} → {align_to} omitida (uno no existe)")
                continue
            
            target_name = component_mapping[comp_id]
            reference_name = component_mapping[align_to]
            
            result = self.adapter.align_objects(target_name, reference_name, align_mode)
            
            if result.get('success', False):
                log_debug(f"  ✓ {comp_id} alineado {align_mode} con {align_to}")
                alignment_count += 1
            else:
                log_warning(f"  ⚠️ Error alineando {comp_id}: {result.get('error')}")
        
        log_debug(f"  Alineaciones aplicadas: {alignment_count}")
        
        # RESULTADO FINAL
        log_info(f"✅ Estructura completada: {len(created_objects)} objetos, {hierarchy_count} relaciones, {alignment_count} alineaciones")
        
        return {
            'success': True,
            'structure_name': structure_def.get('name', 'estructura'),
            'created_objects': created_objects,
            'component_mapping': component_mapping,
            'stats': {
                'total_objects': len(created_objects),
                'hierarchies': hierarchy_count,
                'alignments': alignment_count,
                'errors': len(errors)
            },
            'errors': errors if errors else None
        }
    
    def get_structure_hierarchy(self, root_object: str) -> Dict[str, Any]:
        """
        Obtiene la jerarquía completa de una estructura.
        
        Args:
            root_object: Nombre del objeto raíz
        
        Returns:
            {
                'root': str,
                'hierarchy': Dict (árbol de objetos)
            }
        """
        def build_tree(obj_name):
            children_names = self.adapter.get_children(obj_name)
            children = [build_tree(child) for child in children_names]
            
            return {
                'name': obj_name,
                'children': children if children else None
            }
        
        return {
            'root': root_object,
            'hierarchy': build_tree(root_object)
        }
