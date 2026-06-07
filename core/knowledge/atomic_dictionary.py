# core/knowledge/atomic_dictionary.py

ATOMIC_DICTIONARY = {
    "primitives": {
        "cube": {
            "keywords": ["cubo", "cubos", "box", "cube", "bloque"],
            "mandatory_params": ["location"],
            "optional_params": ["size", "rotation", "scale"],
            "description": "Primitiva cúbica estándar"
        },
        "sphere": {
            "keywords": ["esfera", "esferas", "sphere", "bola", "bolas"],
            "mandatory_params": ["location"],
            "optional_params": ["radius", "rotation", "scale"],
            "description": "Primitiva esférica estándar"
        },
        "cylinder": {
            "keywords": ["cilindro", "cilindros", "cylinder"],
            "mandatory_params": ["location"],
            "optional_params": ["radius", "depth", "rotation", "scale"],
            "description": "Primitiva cilíndrica"
        },
        "plane": {
            "keywords": ["plano", "planos", "plane", "suelo", "piso"],
            "mandatory_params": ["location"],
            "optional_params": ["size", "rotation", "scale"],
            "description": "Primitiva de plano 2D"
        },
        "cone": {
            "keywords": ["cono", "conos", "cone"],
            "mandatory_params": ["location"],
            "optional_params": ["radius1", "depth", "rotation", "scale"],
            "description": "Primitiva cónica"
        },
        "torus": {
            "keywords": ["toroide", "torus", "dona", "aro"],
            "mandatory_params": ["location"],
            "optional_params": ["major_radius", "minor_radius", "rotation", "scale"],
            "description": "Primitiva de tipo dona"
        }
    },
    "roles": {
        "base": ["base", "suelo", "cimiento", "plataforma", "soporte inferior"],
        "support": ["soporte", "pilar", "columna", "poste", "brazo"],
        "fill": ["relleno", "volumen", "interno"],
        "detail": ["detalle", "adorno", "decoración", "pieza pequeña"],
        "connector": ["conector", "unión", "bisagra", "enlace"]
    },
    "transformations": {
        "location": ["posicion", "posición", "ubicación", "lugar", "en"],
        "rotation": ["rotación", "rotacion", "giro", "orientación"],
        "scale": ["escala", "tamaño", "tamano", "dimensiones"],
        "size": ["tamaño", "medida", "largo", "ancho"],
        "radius": ["radio"]
    },
    "spatial_relations": {
        "encima_de": ["encima de", "sobre", "arriba de", "superior a"],
        "debajo_de": ["debajo de", "bajo", "inferior a"],
        "alineado_con": ["alineado con", "junto a", "a un lado de", "paralelo a"]
    },
    "procedural_descriptors": {
        "GEOMETRY_NODES_CONCEPTO": {
            "id": "GEOMETRY_NODES_CONCEPTO",
            "type": "DESCRIPTOR",
            "executable": "NO",
            "description": "Sistema procedural basado en nodos para modificar geometría de forma no destructiva.",
            "keywords": ["geometry nodes", "procedural", "instancias", "nodos", "fields", "distribuir"],
            "characteristics": [
                "Opera sobre geometría existente",
                "Usa flujos de datos (geometry, value, vector)",
                "No define resultados sin contexto"
            ],
            "risks": [
                "Ambigüedad de escala",
                "Densidad excesiva",
                "Falta de geometría base"
            ],
            "requires": [
                "Objeto base definido",
                "Objetivo del sistema procedural"
            ]
        }
    },
    "paradigms": {
        "PARADIGM_IMPERATIVE": {
            "id": "PARADIGM_IMPERATIVE",
            "description": "Operaciones directas y secuenciales sobre objetos.",
            "status": "LEGACY",
            "keywords": ["add cube", "mover", "escalar", "rotar", "create", "apply"],
            "executable": "YES"
        },
        "PARADIGM_MODULAR": {
            "id": "PARADIGM_MODULAR",
            "description": "Sistemas basados en modificadores y nodos iniciales.",
            "status": "SUPPORTED",
            "keywords": ["modifier", "modificador", "stack", "subdivision", "mirror", "array"],
            "executable": "YES"
        },
        "PARADIGM_DECLARATIVE": {
            "id": "PARADIGM_DECLARATIVE",
            "description": "Sistemas basados en campos, flujos de datos y evaluación contextual.",
            "status": "REQUIERE_ADAPTACION",
            "keywords": ["geometry nodes", "fields", "attribute", "atributo", "instances", "instancias", "nodes"],
            "executable": "NO"
        },
        "PARADIGM_PROCEDURAL_EVALUATED": {
            "id": "PARADIGM_PROCEDURAL_EVALUATED",
            "description": "Sistemas evaluados dinámicamente, GPU-driven o declarativos avanzados.",
            "status": "NO_EJECUTABLE",
            "keywords": ["simulation", "zone", "physics nodes", "realtime", "gpu"],
            "executable": "NO"
        }
    }
}
