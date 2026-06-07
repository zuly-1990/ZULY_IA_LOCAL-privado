#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
💡 SISTEMA DE LUCES INTELIGENTE ZULY (SLIZ) v2.0
Iluminación profesional: 3-Point + Sol direccional
Todas las luces apuntan correctamente al centro del objeto
"""

import bpy
import math
import mathutils
from typing import Dict, Tuple

def look_at(objeto_luz, punto_destino):
    """
    Hace que la luz apunte correctamente al punto_destino
    """
    direccion = punto_destino - objeto_luz.location
    rot_quat = direccion.to_track_quat('-Z', 'Y')
    objeto_luz.rotation_euler = rot_quat.to_euler()

class SistemaLucesInteligente:
    """
    Sistema de iluminación automática que calcula posiciones óptimas
    basándose en el tamaño y posición del objeto objetivo
    """
    
    @staticmethod
    def calcular_iluminacion_completa(objeto) -> Dict[str, Dict]:
        """
        Calcula posiciones de 4 luces: Sol + Key + Fill + Rim
        Todas apuntan al centro del objeto
        """
        centro = objeto.location
        dims = objeto.dimensions
        max_dim = max(dims.x, dims.y, dims.z)
        radio = max_dim * 3
        
        config = {
            "Sol": {
                "type": "SUN",
                "location": (centro.x + 5, centro.y - 5, centro.z + 10),
                "energy": 5,
                "angle": math.radians(11.4),
                "color": (1.0, 0.95, 0.8),
                "name": "ZULY_Sol_Direccional"
            },
            "Key": {
                "type": "AREA",
                "location": (centro.x + radio * 0.7, centro.y - radio * 0.5, centro.z + radio * 0.6),
                "energy": 150,
                "size": max(max_dim * 0.8, 2.0),
                "color": (1.0, 0.98, 0.95),
                "name": "ZULY_Key_Principal"
            },
            "Fill": {
                "type": "AREA",
                "location": (centro.x - radio * 0.5, centro.y + radio * 0.3, centro.z + radio * 0.4),
                "energy": 60,
                "size": max(max_dim * 0.5, 1.5),
                "color": (0.9, 0.95, 1.0),
                "name": "ZULY_Fill_Suave"
            },
            "Rim": {
                "type": "SPOT",
                "location": (centro.x, centro.y - radio, centro.z + radio * 0.5),
                "energy": 180,
                "spot_size": math.radians(60),
                "spot_blend": 0.2,
                "color": (1.0, 1.0, 1.0),
                "name": "ZULY_Rim_Contorno"
            }
        }
        return config
    
    @staticmethod
    def crear_luz_apuntando(tipo: str, config: Dict, centro_objeto) -> bpy.types.Object:
        """Crea luz y la hace apuntar al centro del objeto"""
        bpy.ops.object.light_add(type=config["type"], location=config["location"])
        luz = bpy.context.active_object
        luz.name = config["name"]
        
        # APUNTAR AL CENTRO (función look_at)
        look_at(luz, centro_objeto)
        
        luz.data.energy = config["energy"]
        luz.data.color = config["color"]
        
        if config["type"] == "AREA":
            luz.data.size = config["size"]
        elif config["type"] == "SPOT":
            luz.data.spot_size = config.get("spot_size", math.radians(45))
            luz.data.spot_blend = config.get("spot_blend", 0.3)
        elif config["type"] == "SUN":
            luz.data.angle = config.get("angle", math.radians(11.4))
        
        return luz
    
    @staticmethod
    def iluminar_objeto(objeto) -> Dict[str, bpy.types.Object]:
        """Aplica iluminación Sol + 3-Point, todas apuntan al centro"""
        centro = objeto.location
        config = SistemaLucesInteligente.calcular_iluminacion_completa(objeto)
        
        luces = {}
        for nombre, cfg in config.items():
            luces[nombre] = SistemaLucesInteligente.crear_luz_apuntando(nombre, cfg, centro)
        
        return luces
    
    @staticmethod
    def info_iluminacion():
        return {
            "sistema": "SLIZ v2.0 - Sistema de Luces Inteligente ZULY",
            "version": "2.0",
            "tecnica": "4-Point Lighting (Sol + Key + Fill + Rim)",
            "caracteristica": "Todas las luces apuntan al centro del objeto",
            "luces": {
                "Sol": "Luz direccional SUN - iluminación ambiental",
                "Key": "Luz principal AREA - 45° frontal izquierda",
                "Fill": "Luz de relleno AREA - suaviza sombras",
                "Rim": "Luz de contorno SPOT - separa del fondo"
            }
        }

def aplicar_iluminacion_profesional(objeto):
    luces = SistemaLucesInteligente.iluminar_objeto(objeto)
    return {
        "sol": luces["Sol"].name,
        "key": luces["Key"].name,
        "fill": luces["Fill"].name,
        "rim": luces["Rim"].name
    }

if __name__ == "__main__":
    info = SistemaLucesInteligente.info_iluminacion()
    print(f"💡 {info['sistema']}")
    print(f"   Técnica: {info['tecnica']}")
    print(f"   ✓ {info['caracteristica']}")
