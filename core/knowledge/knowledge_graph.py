"""
knowledge_graph.py
==================

GRAFO DE CONOCIMIENTO SEMÁNTICO

LYZU entiende relaciones entre objetos 3D:
- "Luz ilumina cubo"
- "Material está en cubo"  
- "Cámara enfoca esfera"
- "Cubo está cerca de cilindro"

Capacidades:
- Almacenar nodos (objetos 3D)
- Almacenar relaciones (cómo se conectan)
- Consultar (¿qué objetos hay?)
- Inferir (¿qué está iluminado?)
- Razonar (si usuario quiere X, entonces Y)

Base de datos: SQLite persistente
"""

import sqlite3
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass
from pathlib import Path
from enum import Enum


class NodeType(Enum):
    """Tipos de nodos en el grafo"""
    OBJECT = "object"           # Objetos 3D (cubos, esferas, etc)
    LIGHT = "light"             # Luces
    MATERIAL = "material"       # Materiales
    CAMERA = "camera"           # Cámaras
    MODIFIER = "modifier"       # Modificadores
    TEXTURE = "texture"         # Texturas
    ANIMATION = "animation"     # Animaciones


class RelationType(Enum):
    """Tipos de relaciones entre nodos"""
    HAS_MATERIAL = "has_material"      # Objeto tiene material
    ILLUMINATES = "illuminates"        # Luz ilumina objeto
    IS_NEAR = "is_near"                # Está cerca de
    CONTAINS = "contains"              # Contiene
    IS_MODIFIED_BY = "is_modified_by"  # Modificado por
    LOOKS_AT = "looks_at"              # Cámara enfoca


@dataclass
class Node:
    """Un nodo en el grafo (representa un objeto 3D)"""
    id: str
    name: str
    node_type: NodeType
    properties: Dict = None
    created_at: str = None
    
    def __post_init__(self):
        if self.properties is None:
            self.properties = {}
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()


@dataclass
class Relation:
    """Una relación entre dos nodos"""
    source_id: str
    target_id: str
    relation_type: RelationType
    attributes: Dict = None
    created_at: str = None
    
    def __post_init__(self):
        if self.attributes is None:
            self.attributes = {}
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()


class KnowledgeGraph:
    """
    Base de conocimiento para LYZU.
    
    Mantiene un modelo semántico de la escena 3D actual.
    LYZU usa esto para razonar qué hacer.
    """
    
    def __init__(self, db_path: str = 'bitacora/knowledge_graph.db'):
        """Inicializa el grafo de conocimiento"""
        if db_path != ':memory:':
            db_path_obj = Path(db_path)
            db_path_obj.parent.mkdir(parents=True, exist_ok=True)
        self.db_path = db_path
        
        # Caché en memoria
        self.nodes: Dict[str, Node] = {}
        self.relations: List[Relation] = []
        
        # Inicializar BD
        self._init_database()
        
        print(f"[KG] Knowledge Graph inicializado en {db_path}")
    
    def _init_database(self):
        """Crea las tablas necesarias"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Tabla de nodos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS nodes (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    node_type TEXT NOT NULL,
                    properties JSON,
                    created_at TEXT
                )
            ''')
            
            # Tabla de relaciones
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS relations (
                    source_id TEXT NOT NULL,
                    target_id TEXT NOT NULL,
                    relation_type TEXT NOT NULL,
                    attributes JSON,
                    created_at TEXT,
                    PRIMARY KEY (source_id, target_id, relation_type)
                )
            ''')
            
            # Tabla de inferencias (decisiones tomadas)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS inferences (
                    id TEXT PRIMARY KEY,
                    condition TEXT,
                    action TEXT,
                    reasoning TEXT,
                    created_at TEXT
                )
            ''')
            
            conn.commit()
    
    # ========== OPERACIONES DE NODOS ==========
    
    def add_object(self, obj_id: str, name: str, obj_type: str, properties: Dict = None) -> Node:
        """Agrega un objeto 3D al grafo"""
        if properties is None:
            properties = {}
        
        node = Node(
            id=obj_id,
            name=name,
            node_type=NodeType.OBJECT,
            properties={'type': obj_type, **properties}
        )
        
        self.nodes[obj_id] = node
        self._persist_node(node)
        
        print(f"  ✓ Objeto agregado: {name} ({obj_type})")
        return node
    
    def add_light(self, light_id: str, name: str, light_type: str, energy: float = 1000) -> Node:
        """Agrega una luz al grafo"""
        node = Node(
            id=light_id,
            name=name,
            node_type=NodeType.LIGHT,
            properties={'type': light_type, 'energy': energy}
        )
        
        self.nodes[light_id] = node
        self._persist_node(node)
        
        print(f"  ✓ Luz agregada: {name} ({light_type}, energía={energy})")
        return node
    
    def add_material(self, material_id: str, name: str, color: Tuple = None) -> Node:
        """Agrega un material al grafo"""
        node = Node(
            id=material_id,
            name=name,
            node_type=NodeType.MATERIAL,
            properties={'color': color or (1, 1, 1)}
        )
        
        self.nodes[material_id] = node
        self._persist_node(node)
        
        print(f"  ✓ Material agregado: {name}")
        return node
    
    def add_camera(self, camera_id: str, name: str, focal_length: float = 50) -> Node:
        """Agrega una cámara al grafo"""
        node = Node(
            id=camera_id,
            name=name,
            node_type=NodeType.CAMERA,
            properties={'focal_length': focal_length}
        )
        
        self.nodes[camera_id] = node
        self._persist_node(node)
        
        print(f"  ✓ Cámara agregada: {name}")
        return node
    
    def _persist_node(self, node: Node):
        """Guarda nodo en BD"""
        # Solo persistir si no es memory DB (que ya tiene los datos en caché)
        if self.db_path == ':memory:':
            return
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO nodes (id, name, node_type, properties, created_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                node.id,
                node.name,
                node.node_type.value,
                json.dumps(node.properties),
                node.created_at
            ))
            conn.commit()
    
    # ========== OPERACIONES DE RELACIONES ==========
    
    def relate(self, source_id: str, relation_type: RelationType, target_id: str, attributes: Dict = None) -> Relation:
        """Crea una relación entre dos nodos"""
        relation = Relation(
            source_id=source_id,
            target_id=target_id,
            relation_type=relation_type,
            attributes=attributes or {}
        )
        
        self.relations.append(relation)
        self._persist_relation(relation)
        
        source_node = self.nodes.get(source_id)
        target_node = self.nodes.get(target_id)
        source_name = source_node.name if source_node else source_id
        target_name = target_node.name if target_node else target_id
        print(f"  ✓ Relación: {source_name} --{relation_type.value}--> {target_name}")
        
        return relation
    
    def has_material(self, obj_id: str, material_id: str):
        """Objeto tiene material"""
        return self.relate(obj_id, RelationType.HAS_MATERIAL, material_id)
    
    def illuminates(self, light_id: str, obj_id: str):
        """Luz ilumina objeto"""
        return self.relate(light_id, RelationType.ILLUMINATES, obj_id)
    
    def is_near(self, obj1_id: str, obj2_id: str, distance: float = 5.0):
        """Objeto está cerca de otro"""
        return self.relate(obj1_id, RelationType.IS_NEAR, obj2_id, {'distance': distance})
    
    def looks_at(self, camera_id: str, obj_id: str):
        """Cámara enfoca objeto"""
        return self.relate(camera_id, RelationType.LOOKS_AT, obj_id)
    
    def _persist_relation(self, relation: Relation):
        """Guarda relación en BD"""
        # Solo persistir si no es memory DB
        if self.db_path == ':memory:':
            return
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO relations (source_id, target_id, relation_type, attributes, created_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                relation.source_id,
                relation.target_id,
                relation.relation_type.value,
                json.dumps(relation.attributes),
                relation.created_at
            ))
            conn.commit()
    
    # ========== CONSULTAS ==========
    
    def query_objects(self) -> List[Node]:
        """¿Qué objetos hay en la escena?"""
        return [n for n in self.nodes.values() if n.node_type == NodeType.OBJECT]
    
    def query_lights(self) -> List[Node]:
        """¿Qué luces hay?"""
        return [n for n in self.nodes.values() if n.node_type == NodeType.LIGHT]
    
    def query_materials(self) -> List[Node]:
        """¿Qué materiales hay?"""
        return [n for n in self.nodes.values() if n.node_type == NodeType.MATERIAL]
    
    def query_illuminated_objects(self) -> List[Tuple[str, str]]:
        """¿Qué objetos están iluminados?"""
        return [
            (r.source_id, r.target_id) for r in self.relations
            if r.relation_type == RelationType.ILLUMINATES
        ]
    
    def query_objects_with_material(self) -> List[Tuple[str, str]]:
        """¿Qué objetos tienen material?"""
        return [
            (r.source_id, r.target_id) for r in self.relations
            if r.relation_type == RelationType.HAS_MATERIAL
        ]
    
    def query_nearby_objects(self, obj_id: str, max_distance: float = 10.0) -> List[str]:
        """¿Qué objetos están cerca de este?"""
        nearby = []
        for relation in self.relations:
            if (relation.source_id == obj_id and 
                relation.relation_type == RelationType.IS_NEAR and
                relation.attributes.get('distance', 0) <= max_distance):
                nearby.append(relation.target_id)
        return nearby
    
    # ========== INFERENCIAS (RAZONAMIENTO) ==========
    
    def infer_improvements(self, user_request: str) -> List[str]:
        """
        LYZU infiere mejoras basadas en la escena actual.
        
        Ejemplo:
          Usuario: "Que se vea mejor"
          LYZU analiza: "No hay luces" → "Agregar iluminación"
          LYZU analiza: "Cubo solo" → "Agregar más objetos o materiales"
        """
        suggestions = []
        
        objects = self.query_objects()
        lights = self.query_lights()
        illuminated = self.query_illuminated_objects()
        
        # Inferencia 1: Si no hay luces, agregar
        if not lights:
            suggestions.append("Agregar iluminación para mejorar visibilidad")
        
        # Inferencia 2: Si hay objetos pero no están iluminados
        if objects and not illuminated:
            suggestions.append("Iluminar objetos para mejor presentación")
        
        # Inferencia 3: Si solo hay un objeto, agregar composición
        if len(objects) == 1:
            suggestions.append("Agregar más objetos para composición interesante")
        
        # Inferencia 4: Si no hay materiales
        materials = self.query_materials()
        if not materials and objects:
            suggestions.append("Aplicar materiales para mayor realismo")
        
        # Inferencia 5: Si hay muchos objetos sin iluminar bien
        if len(objects) > 3 and len(illuminated) < len(objects):
            suggestions.append("Mejorar iluminación general para escena compleja")
        
        # Si no hay sugerencias, retornar sugerencia default
        if not suggestions:
            suggestions.append("Escena básica lista, considerar mejorar composición visual")
        
        return suggestions
    
    def infer_actions(self, situation: str) -> List[Dict[str, str]]:
        """
        LYZU infiere acciones recomendadas para una situación.
        """
        actions = []
        
        if "oscuro" in situation.lower():
            actions.append({
                'action': 'agregar_luz',
                'reasoning': 'La escena está oscura, necesita más iluminación'
            })
        
        if "pequeño" in situation.lower() or "minimalista" in situation.lower():
            actions.append({
                'action': 'agregar_objetos',
                'reasoning': 'Escena pequeña, agregar elementos para composición'
            })
        
        if "aburrido" in situation.lower() or "plano" in situation.lower():
            actions.append({
                'action': 'aplicar_materiales',
                'reasoning': 'Agregar materiales y texturas para interés visual'
            })
            actions.append({
                'action': 'mejorar_composicion',
                'reasoning': 'Ajustar posiciones y cámara para mejor composición'
            })
        
        return actions
    
    # ========== ESTADÍSTICAS ==========
    
    def get_scene_summary(self) -> Dict:
        """Resumen de la escena actual"""
        return {
            'total_objects': len(self.query_objects()),
            'total_lights': len(self.query_lights()),
            'total_materials': len(self.query_materials()),
            'total_cameras': len([n for n in self.nodes.values() if n.node_type == NodeType.CAMERA]),
            'illuminated_objects': len(self.query_illuminated_objects()),
            'objects_with_material': len(self.query_objects_with_material()),
            'total_relations': len(self.relations)
        }
    
    def clear_scene(self):
        """Limpia la escena (para nueva sesión)"""
        self.nodes.clear()
        self.relations.clear()
        print("  🗑️  Escena limpiada")
    
    def export_as_json(self) -> str:
        """Exporta el grafo como JSON"""
        data = {
            'nodes': {
                nid: {
                    'name': n.name,
                    'type': n.node_type.value,
                    'properties': n.properties
                }
                for nid, n in self.nodes.items()
            },
            'relations': [
                {
                    'source': r.source_id,
                    'target': r.target_id,
                    'type': r.relation_type.value,
                    'attributes': r.attributes
                }
                for r in self.relations
            ]
        }
        return json.dumps(data, indent=2)
