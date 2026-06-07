#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 JUES-BOT V3.0 - AUDITORÍA AVANZADA
Fortalecido con 10 superpoderes para modelos complejos
"""

import bpy
import bmesh
import sys
import json
import hashlib
import shutil
import math
import mathutils  # <-- CORREGIDO: Añadido mathutils
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional

# RUTAS DEL SISTEMA
ZULY_BASE = Path("c:/Users/Admin/Desktop/ZULY_IA_LOCAL")
ARCHIVO_ZULY = ZULY_BASE / "archivo_zuly"
TEMP_ARENA = ARCHIVO_ZULY / "temp_arena"
MASTERED = ARCHIVO_ZULY / "por_estado_aprendizaje" / "mastered"
CORE = ZULY_BASE / "core"

# PROTOCOLO ZEI EXTENDIDO
class ProtocoloZeiV3:
    """Lenguaje ZULY-JUES V3 con más estados"""
    MENSAJES = {
        # Estados base
        "APTO": "✅ APTO_PARA_SELLO",
        "APTO_ADV": "⚠️ APTO_CON_ADVERTENCIAS", 
        "NO_APTO": "❌ NO_APTO",
        
        # Superpoderes originales
        "MALLA_OK": "LIMPIA",
        "MALLA_FAIL": "CORRUPTA",
        "PESO_OK": "OPTIMO",
        "PESO_FAIL": "GRASA_DIGITAL",
        "COLOR_OK": "MATCH",
        "COLOR_FAIL": "NO_MATCH",
        
        # NUEVOS - Superpoderes V3
        "ESTRUCTURA_OK": "JERARQUIA_SANA",
        "ESTRUCTURA_FAIL": "JERARQUIA_ROTA",
        "MATERIAL_OK": "MATERIALES_VALIDOS",
        "MATERIAL_FAIL": "MATERIALES_CORRUPTOS",
        "METROLOGIA_OK": "DIMENSIONES_CORRECTAS",
        "METROLOGIA_FAIL": "DIMENSIONES_ERRONEAS",
        "LUZ_OK": "ILUMINACION_ADECUADA",
        "LUZ_FAIL": "ILUMINACION_DEFICIENTE",
        "COMPLEJIDAD_OK": "GEOMETRIA_BALANCEADA",
        "COMPLEJIDAD_FAIL": "GEOMETRIA_EXTREMA",
        
        # Acciones
        "SOLICITAR_SELLO": "🏛️ SOLICITANDO_SELLO_SOBERANO",
        "SELLO_APLICADO": "🏆 SELLO_APLICADO",
        "AUDITORIA_INICIO": "🔍 INICIANDO_AUDITORIA_COMPLETA",
        "AUDITORIA_FIN": "📊 AUDITORIA_COMPLETADA",
        
        # Niveles de severidad
        "CRITICO": "🚨 CRITICO",
        "MAYOR": "⚠️ MAYOR",
        "MENOR": "💡 MENOR",
        "INFO": "ℹ️ INFO"
    }
    
    @staticmethod
    def mensaje(codigo: str) -> str:
        return ProtocoloZeiV3.MENSAJES.get(codigo, f"❓ CODIGO_DESCONOCIDO: {codigo}")


class JuesBotV3:
    """
    JUES-BOT V3.0 - Auditoría Profesional
    10 Superpoderes para validación exhaustiva
    """
    
    def __init__(self, blend_path: str, candidato_id: str, target_color_hex: str = "#FF0000"):
        self.blend_path = Path(blend_path)
        self.candidato_id = candidato_id
        self.target_color_hex = target_color_hex.upper()
        self.resultados = {
            "candidato_id": candidato_id,
            "timestamp": datetime.now().isoformat(),
            "version_jues": "3.0",
            "protocolo_zei": {},
            "superpoderes": {},
            "hallazgos": [],
            "dictamen": ProtocoloZeiV3.mensaje("NO_APTO"),
            "puntuacion": 0,
            "sellado": None
        }
        self.MAX_FILE_SIZE_KB = 5000  # Aumentado para modelos complejos
        self.MAX_VERTICES = 100000    # Límite geometría pesada
        self.MIN_VERTICES = 10       # Mínimo para ser válido
        
    # ========== 10 SUPERPODERES ==========
    
    def superpoder_a_vision_rayos_x(self, obj) -> Dict:
        """A: Detecta geometría corrupta (non-manifold)"""
        if not obj or obj.type != 'MESH':
            return {"status": ProtocoloZeiV3.mensaje("MALLA_FAIL"), "icon": "💀", "severidad": "CRITICO"}
        
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.mesh.select_non_manifold()
        
        bm = bmesh.from_edit_mesh(obj.data)
        no_manifold = sum(1 for e in bm.edges if e.select)
        bpy.ops.object.mode_set(mode='OBJECT')
        
        if no_manifold == 0:
            return {"status": ProtocoloZeiV3.mensaje("MALLA_OK"), "icon": "✨", "severidad": "INFO", "no_manifold": 0}
        return {"status": ProtocoloZeiV3.mensaje("MALLA_FAIL"), "icon": "☠️", "severidad": "CRITICO", "no_manifold": no_manifold}
    
    def superpoder_b_instinto_optimizacion(self) -> Dict:
        """B: Detecta basura digital (tamaño archivo)"""
        if not self.blend_path.exists():
            return {"status": "ERROR", "icon": "❓", "severidad": "CRITICO"}
        
        size_kb = round(self.blend_path.stat().st_size / 1024, 2)
        
        if size_kb > self.MAX_FILE_SIZE_KB:
            return {
                "status": ProtocoloZeiV3.mensaje("PESO_FAIL"),
                "peso_kb": size_kb,
                "icon": "🐷",
                "severidad": "MAYOR",
                "ratio": round(size_kb / self.MAX_FILE_SIZE_KB, 2)
            }
        return {
            "status": ProtocoloZeiV3.mensaje("PESO_OK"),
            "peso_kb": size_kb,
            "icon": "⚡",
            "severidad": "INFO",
            "ratio": round(size_kb / self.MAX_FILE_SIZE_KB, 2)
        }
    
    def superpoder_c_sincronia_cromatica(self, obj) -> Dict:
        """C: Valida color exacto del material"""
        if not obj or not obj.data.materials:
            return {"status": ProtocoloZeiV3.mensaje("COLOR_FAIL"), "icon": "🎨❌", "severidad": "CRITICO"}
        
        mat = obj.data.materials[0]
        if not mat.use_nodes:
            return {"status": ProtocoloZeiV3.mensaje("COLOR_FAIL"), "icon": "🎨❌", "severidad": "MAYOR"}
        
        principled = None
        for node in mat.node_tree.nodes:
            if node.type == 'BSDF_PRINCIPLED':
                principled = node
                break
        
        if not principled:
            return {"status": ProtocoloZeiV3.mensaje("COLOR_FAIL"), "icon": "🎨❌", "severidad": "MAYOR"}
        
        color = principled.inputs['Base Color'].default_value
        r, g, b = int(color[0] * 255), int(color[1] * 255), int(color[2] * 255)
        hex_encontrado = f"#{r:02X}{g:02X}{b:02X}"
        
        match = hex_encontrado.upper() == self.target_color_hex.upper()
        
        if match:
            return {
                "status": ProtocoloZeiV3.mensaje("COLOR_OK"),
                "color_encontrado": hex_encontrado,
                "icon": "🎯",
                "severidad": "INFO"
            }
        return {
            "status": ProtocoloZeiV3.mensaje("COLOR_FAIL"),
            "color_encontrado": hex_encontrado,
            "color_esperado": self.target_color_hex,
            "icon": "🎨⚠️",
            "severidad": "MAYOR"
        }
    
    def superpoder_d_sello_inmutabilidad(self, obj) -> Dict:
        """D: Genera hash único de geometría"""
        if not obj or obj.type != 'MESH':
            return {"hash": "ERROR", "icon": "🔒❌", "severidad": "CRITICO"}
        
        coords_str = ""
        for v in obj.data.vertices:
            coords_str += f"{v.co.x:.4f},{v.co.y:.4f},{v.co.z:.4f};"
        for poly in obj.data.polygons:
            verts_indices = ",".join(str(v) for v in poly.vertices)
            coords_str += f"[{verts_indices}]"
        
        hash_md5 = hashlib.md5(coords_str.encode('utf-8')).hexdigest()
        hash_sha256 = hashlib.sha256(coords_str.encode('utf-8')).hexdigest()
        
        return {
            "hash_md5": hash_md5,
            "hash_sha256": hash_sha256[:32] + "...",
            "vertices_count": len(obj.data.vertices),
            "polygons_count": len(obj.data.polygons),
            "icon": "🔒",
            "severidad": "INFO"
        }
    
    # ===== NUEVOS SUPERPODERES V3 =====
    
    def superpoder_e_auditoria_estructura(self) -> Dict:
        """E: Analiza jerarquía y estructura de la escena"""
        objetos_mesh = [o for o in bpy.context.scene.objects if o.type == 'MESH']
        objetos_luz = [o for o in bpy.context.scene.objects if o.type == 'LIGHT']
        objetos_camara = [o for o in bpy.context.scene.objects if o.type == 'CAMERA']
        
        # Detectar objetos huérfanos (sin padre)
        huerfanos = [o for o in objetos_mesh if o.parent is None]
        
        # Detectar objetos con hijos (raíces)
        raices = [o for o in objetos_mesh if len(o.children) > 0]
        
        estructura_sana = len(objetos_mesh) > 0 and len(objetos_camara) > 0
        
        return {
            "status": ProtocoloZeiV3.mensaje("ESTRUCTURA_OK") if estructura_sana else ProtocoloZeiV3.mensaje("ESTRUCTURA_FAIL"),
            "icon": "🏗️" if estructura_sana else "🏗️❌",
            "severidad": "INFO" if estructura_sana else "MAYOR",
            "total_mesh": len(objetos_mesh),
            "total_luces": len(objetos_luz),
            "total_camaras": len(objetos_camara),
            "huerfanos": len(huerfanos),
            "raices_jerarquia": len(raices)
        }
    
    def superpoder_f_escaneo_materiales(self, obj) -> Dict:
        """F: Analiza materiales en profundidad"""
        if not obj or obj.type != 'MESH':
            return {"status": ProtocoloZeiV3.mensaje("MATERIAL_FAIL"), "icon": "🧪❌", "severidad": "CRITICO"}
        
        mats = obj.data.materials
        if not mats:
            return {"status": ProtocoloZeiV3.mensaje("MATERIAL_FAIL"), "icon": "🧪❌", "severidad": "MAYOR", "razon": "Sin materiales"}
        
        mat = mats[0]
        if not mat.use_nodes:
            return {"status": ProtocoloZeiV3.mensaje("MATERIAL_FAIL"), "icon": "🧪❌", "severidad": "MENOR", "razon": "Sin nodos"}
        
        # Contar nodos
        total_nodos = len(mat.node_tree.nodes)
        nodos_principales = sum(1 for n in mat.node_tree.nodes if n.type in ['BSDF_PRINCIPLED', 'OUTPUT_MATERIAL'])
        
        # Detectar texturas
        tiene_texturas = any(n.type == 'TEX_IMAGE' for n in mat.node_tree.nodes)
        
        return {
            "status": ProtocoloZeiV3.mensaje("MATERIAL_OK"),
            "icon": "🧪",
            "severidad": "INFO",
            "total_nodos": total_nodos,
            "nodos_principales": nodos_principales,
            "usa_texturas": tiene_texturas,
            "material_name": mat.name
        }
    
    def superpoder_g_metrologia_exacta(self, obj) -> Dict:
        """G: Mide dimensiones reales del objeto"""
        if not obj or obj.type != 'MESH':
            return {"status": ProtocoloZeiV3.mensaje("METROLOGIA_FAIL"), "icon": "📏❌", "severidad": "CRITICO"}
        
        # Calcular bounding box en world space
        bbox_corners = [obj.matrix_world @ mathutils.Vector(corner) for corner in obj.bound_box]
        
        # Dimensiones
        min_x = min(v.x for v in bbox_corners)
        max_x = max(v.x for v in bbox_corners)
        min_y = min(v.y for v in bbox_corners)
        max_y = max(v.y for v in bbox_corners)
        min_z = min(v.z for v in bbox_corners)
        max_z = max(v.z for v in bbox_corners)
        
        ancho = round(max_x - min_x, 3)
        profundidad = round(max_y - min_y, 3)
        alto = round(max_z - min_z, 3)
        
        volumen_aprox = round(ancho * profundidad * alto, 3)
        
        return {
            "status": ProtocoloZeiV3.mensaje("METROLOGIA_OK"),
            "icon": "📏",
            "severidad": "INFO",
            "dimensiones": {"ancho": ancho, "profundidad": profundidad, "alto": alto},
            "volumen_m3": volumen_aprox,
            "unidades": "metros"
        }
    
    def superpoder_h_analisis_iluminacion(self) -> Dict:
        """H: Evalúa iluminación de la escena"""
        luces = [o for o in bpy.context.scene.objects if o.type == 'LIGHT']
        
        if not luces:
            return {
                "status": ProtocoloZeiV3.mensaje("LUZ_FAIL"),
                "icon": "💡❌",
                "severidad": "MAYOR",
                "total_luces": 0,
                "tipo_iluminacion": "AUSENTE"
            }
        
        # Analizar tipos de luces
        tipos = {}
        energia_total = 0
        for luz in luces:
            tipo = luz.data.type
            tipos[tipo] = tipos.get(tipo, 0) + 1
            energia_total += luz.data.energy
        
        iluminacion_ok = len(luces) >= 1 and energia_total > 0
        
        return {
            "status": ProtocoloZeiV3.mensaje("LUZ_OK") if iluminacion_ok else ProtocoloZeiV3.mensaje("LUZ_FAIL"),
            "icon": "💡" if iluminacion_ok else "💡⚠️",
            "severidad": "INFO" if iluminacion_ok else "MENOR",
            "total_luces": len(luces),
            "tipos": tipos,
            "energia_total": round(energia_total, 2),
            "tipo_iluminacion": "PROFESIONAL" if len(luces) >= 3 else "BASICA"
        }
    
    def superpoder_i_criptografia_escena(self) -> Dict:
        """I: Hash completo de toda la escena"""
        scene_data = ""
        
        # Hash de todos los objetos mesh
        for obj in sorted(bpy.context.scene.objects, key=lambda x: x.name):
            if obj.type == 'MESH':
                scene_data += f"OBJ:{obj.name};"
                for v in obj.data.vertices:
                    scene_data += f"v{v.co.x:.3f},{v.co.y:.3f},{v.co.z:.3f};"
        
        hash_completo = hashlib.sha256(scene_data.encode('utf-8')).hexdigest()
        
        return {
            "hash_escena": hash_completo[:16] + "..." + hash_completo[-16:],
            "icon": "🔐",
            "severidad": "INFO",
            "objetos_hasheados": sum(1 for o in bpy.context.scene.objects if o.type == 'MESH')
        }
    
    def superpoder_j_analisis_complejidad(self, obj) -> Dict:
        """J: Evalúa complejidad geométrica"""
        if not obj or obj.type != 'MESH':
            return {"status": ProtocoloZeiV3.mensaje("COMPLEJIDAD_FAIL"), "icon": "📊❌", "severidad": "CRITICO"}
        
        vertices = len(obj.data.vertices)
        aristas = len(obj.data.edges)
        poligonos = len(obj.data.polygons)
        
        # Calcular ratio polígonos/vértices (ideal: ~0.5 para quads)
        ratio = round(poligonos / vertices, 3) if vertices > 0 else 0
        
        # Clasificar complejidad
        if vertices < self.MIN_VERTICES:
            nivel = "DEMasiado_SIMPLE"
            status = ProtocoloZeiV3.mensaje("COMPLEJIDAD_FAIL")
            severidad = "MAYOR"
        elif vertices > self.MAX_VERTICES:
            nivel = "EXTREMA"
            status = ProtocoloZeiV3.mensaje("COMPLEJIDAD_FAIL")
            severidad = "MAYOR"
        elif vertices > 50000:
            nivel = "ALTA"
            status = ProtocoloZeiV3.mensaje("COMPLEJIDAD_OK")
            severidad = "INFO"
        elif vertices > 10000:
            nivel = "MEDIA"
            status = ProtocoloZeiV3.mensaje("COMPLEJIDAD_OK")
            severidad = "INFO"
        else:
            nivel = "OPTIMIZADA"
            status = ProtocoloZeiV3.mensaje("COMPLEJIDAD_OK")
            severidad = "INFO"
        
        return {
            "status": status,
            "icon": "📊",
            "severidad": severidad,
            "vertices": vertices,
            "aristas": aristas,
            "poligonos": poligonos,
            "ratio_polig_vertices": ratio,
            "nivel_complejidad": nivel
        }
    
    # ========== FLUJO COMPLETO V3 ==========
    
    def ejecutar_auditoria_completa(self) -> Dict:
        """Auditoría completa con 10 superpoderes"""
        print(f"\n{'='*70}")
        print(ProtocoloZeiV3.mensaje("AUDITORIA_INICIO"))
        print(f"{'='*70}")
        print(f"🤖 JUES-BOT V3.0 - 10 Superpoderes Activados")
        print(f"🎯 Candidato: {self.candidato_id}")
        print(f"{'='*70}\n")
        
        # Cargar blend
        bpy.ops.wm.open_mainfile(filepath=str(self.blend_path))
        
        # Obtener objeto principal (primer mesh)
        obj = None
        for o in bpy.context.scene.objects:
            if o.type == 'MESH':
                obj = o
                break
        
        # Ejecutar los 10 superpoderes
        sp = self.resultados["superpoderes"]
        sp["A_vision_rayos_x"] = self.superpoder_a_vision_rayos_x(obj)
        sp["B_instinto_optimizacion"] = self.superpoder_b_instinto_optimizacion()
        sp["C_sincronia_cromatica"] = self.superpoder_c_sincronia_cromatica(obj)
        sp["D_sello_inmutabilidad"] = self.superpoder_d_sello_inmutabilidad(obj)
        sp["E_auditoria_estructura"] = self.superpoder_e_auditoria_estructura()
        sp["F_escaneo_materiales"] = self.superpoder_f_escaneo_materiales(obj)
        sp["G_metrologia_exacta"] = self.superpoder_g_metrologia_exacta(obj)
        sp["H_analisis_iluminacion"] = self.superpoder_h_analisis_iluminacion()
        sp["I_criptografia_escena"] = self.superpoder_i_criptografia_escena()
        sp["J_analisis_complejidad"] = self.superpoder_j_analisis_complejidad(obj)
        
        # Dashboard extendido
        print(f"\n📊 DASHBOARD JUES-BOT V3.0")
        print(f"{'='*70}")
        
        for letra, nombre in [("A", "Rayos X"), ("B", "Optimización"), ("C", "Sincronía"),
                               ("D", "Inmutabilidad"), ("E", "Estructura"), ("F", "Materiales"),
                               ("G", "Metrología"), ("H", "Iluminación"), ("I", "Criptografía"),
                               ("J", "Complejidad")]:
            key = f"{letra}_{[k for k in sp.keys() if k.startswith(letra)][0].split('_', 1)[1]}"
            data = sp[key]
            print(f"   {letra}. {nombre}: {data['status']} {data['icon']}")
        
        # Calcular puntuación
        puntuacion = 100
        hallazgos = []
        
        for key, data in sp.items():
            if data.get("severidad") == "CRITICO":
                puntuacion -= 30
                hallazgos.append(f"🚨 {key}: {data['status']}")
            elif data.get("severidad") == "MAYOR":
                puntuacion -= 15
                hallazgos.append(f"⚠️ {key}: {data['status']}")
            elif data.get("severidad") == "MENOR":
                puntuacion -= 5
                hallazgos.append(f"💡 {key}: {data['status']}")
        
        puntuacion = max(0, min(100, puntuacion))
        self.resultados["puntuacion"] = puntuacion
        self.resultados["hallazgos"] = hallazgos
        
        # Dictamen basado en puntuación
        if puntuacion >= 90:
            dictamen = ProtocoloZeiV3.mensaje("APTO")
        elif puntuacion >= 70:
            dictamen = ProtocoloZeiV3.mensaje("APTO_ADV")
        else:
            dictamen = ProtocoloZeiV3.mensaje("NO_APTO")
        
        self.resultados["dictamen"] = dictamen
        
        # Resumen
        print(f"\n{'='*70}")
        print(f"🏛️ DICTAMEN: {dictamen}")
        print(f"⭐ PUNTUACIÓN: {puntuacion}/100")
        print(f"{'='*70}")
        
        if hallazgos:
            print(f"\n📋 HALLAZGOS ({len(hallazgos)}):")
            for h in hallazgos[:5]:  # Mostrar primeros 5
                print(f"   {h}")
            if len(hallazgos) > 5:
                print(f"   ... y {len(hallazgos)-5} más")
        
        print(f"{'='*70}\n")
        
        return self.resultados
    
    def aplicar_sello_v3(self, aprobado_por: str = "Soberano") -> Dict:
        """SELLO AUTOMÁTICO V3 - Más completo"""
        print(f"\n{'='*70}")
        print(ProtocoloZeiV3.mensaje("SOLICITAR_SELLO"))
        print(f"{'='*70}")
        
        if self.resultados["puntuacion"] < 70:
            print("❌ No se puede sellar - Puntuación insuficiente (< 70)")
            return {"status": "ERROR", "motivo": "PUNTUACION_BAJA"}
        
        # Crear estructura mastered/
        pattern_folder = MASTERED / self.candidato_id
        folders = {
            'blend': pattern_folder / 'blend',
            'script': pattern_folder / 'script',
            'json': pattern_folder / 'json',
            'render': pattern_folder / 'render',
            'certificado': pattern_folder / 'certificado',
            'auditoria': pattern_folder / 'auditoria'  # NUEVO: carpeta auditoría
        }
        
        for folder in folders.values():
            folder.mkdir(parents=True, exist_ok=True)
        
        # Copiar blend
        dst_blend = folders['blend'] / f"{self.candidato_id}.blend"
        shutil.copy2(self.blend_path, dst_blend)
        
        # Crear certificado V3 más completo
        certificado = {
            "certificado_id": f"CERT-V3-{self.candidato_id}-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "pattern_id": self.candidato_id,
            "fecha_sello": datetime.now().isoformat(),
            "version_jues": "3.0",
            "sellado_por": aprobado_por,
            "decision": "SELLADO",
            "dictamen_jues": self.resultados["dictamen"],
            "puntuacion": self.resultados["puntuacion"],
            "auditoria_completa": self.resultados["superpoderes"],
            "hallazgos": self.resultados["hallazgos"]
        }
        
        cert_path = folders['certificado'] / "CERTIFICADO_SELLO_V3.json"
        with open(cert_path, 'w', encoding='utf-8') as f:
            json.dump(certificado, f, indent=2, ensure_ascii=False)
        
        # Guardar reporte de auditoría detallado
        audit_path = folders['auditoria'] / "REPORTE_AUDITORIA.json"
        with open(audit_path, 'w', encoding='utf-8') as f:
            json.dump(self.resultados, f, indent=2, ensure_ascii=False)
        
        # Actualizar REGISTRO_MAESTRO
        registro_path = ARCHIVO_ZULY / "REGISTRO_MAESTRO.json"
        if registro_path.exists():
            with open(registro_path, 'r', encoding='utf-8') as f:
                registro = json.load(f)
        else:
            registro = {"sistema": "ZULY", "version_jues": "3.0", "total_patrones": 0, "patrones": []}
        
        registro["patrones"].append({
            "pattern_id": self.candidato_id,
            "nombre": self.candidato_id,
            "estado": "SELLADO",
            "version_jues": "3.0",
            "puntuacion": self.resultados["puntuacion"],
            "fecha_sello": datetime.now().isoformat(),
            "ubicacion": f"por_estado_aprendizaje/mastered/{self.candidato_id}/"
        })
        registro["total_patrones"] = len(registro["patrones"])
        registro["version_jues"] = "3.0"
        
        with open(registro_path, 'w', encoding='utf-8') as f:
            json.dump(registro, f, indent=2, ensure_ascii=False)
        
        self.resultados["sellado"] = {
            "status": ProtocoloZeiV3.mensaje("SELLO_APLICADO"),
            "ubicacion": str(pattern_folder),
            "certificado": str(cert_path),
            "reporte_auditoria": str(audit_path),
            "puntuacion": self.resultados["puntuacion"]
        }
        
        print(f"✅ {ProtocoloZeiV3.mensaje('SELLO_APLICADO')}")
        print(f"   📁 Ubicación: {pattern_folder}")
        print(f"   📜 Certificado V3: {cert_path.name}")
        print(f"   📊 Reporte Auditoría: {audit_path.name}")
        print(f"   ⭐ Puntuación: {self.resultados['puntuacion']}/100")
        print(f"   📚 Total patrones en registro: {registro['total_patrones']}")
        print(f"{'='*70}\n")
        
        return self.resultados["sellado"]


def jues_bot_v3_validar_y_sellar(blend_path: str, candidato_id: str, target_color: str, aprobar: bool = False) -> Dict:
    """FUNCIÓN PRINCIPAL V3"""
    jues = JuesBotV3(blend_path, candidato_id, target_color)
    
    # Auditoría completa
    resultados = jues.ejecutar_auditoria_completa()
    
    # Sellar si aprobado y puntuación >= 70
    if aprobar and resultados["puntuacion"] >= 70:
        sello = jues.aplicar_sello_v3("Soberano")
        resultados["sellado"] = sello
    
    return resultados


if __name__ == "__main__":
    if len(sys.argv) >= 4:
        blend = sys.argv[1]
        candidato = sys.argv[2]
        color = sys.argv[3]
        aprobar = len(sys.argv) > 4 and sys.argv[4].lower() in ["true", "ok", "si", "s"]
        
        resultados = jues_bot_v3_validar_y_sellar(blend, candidato, color, aprobar)
        
        print(f"\nRESULTADO_FINAL: {resultados['dictamen']}")
        print(f"PUNTUACION: {resultados['puntuacion']}/100")
        if resultados.get('sellado'):
            print(f"SELLO: {resultados['sellado']['status']}")
    else:
        print("Uso: python jues_bot_v3.py <blend> <candidato_id> <color_hex> [aprobar]")
        print("Ejemplo: python jues_bot_v3.py modelo.blend ARC-PAV-001 #CCCCCC true")
