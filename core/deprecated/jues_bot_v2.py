#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 JUES-BOT V2.0 - Sistema de Validación y Sellado Automático
Protocolo de Comunicación ZULY-JUES
"""

import bpy
import bmesh
import sys
import json
import hashlib
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional

# RUTAS DEL SISTEMA
ZULY_BASE = Path("c:/Users/Admin/Desktop/ZULY_IA_LOCAL")
ARCHIVO_ZULY = ZULY_BASE / "archivo_zuly"
TEMP_ARENA = ARCHIVO_ZULY / "temp_arena"
MASTERED = ARCHIVO_ZULY / "por_estado_aprendizaje" / "mastered"
CORE = ZULY_BASE / "core"

# PROTOCOLO DE MENSAJES ZULY-JUES
class ProtocoloZei:
    """
    Lenguaje común entre ZULY y JUES
    """
    MENSAJES = {
        # Estados de validación
        "APTO": "✅ APTO_PARA_SELLO",
        "APTO_ADV": "⚠️ APTO_CON_ADVERTENCIAS", 
        "NO_APTO": "❌ NO_APTO",
        
        # Superpoderes
        "MALLA_OK": "LIMPIA",
        "MALLA_FAIL": "CORRUPTA",
        "PESO_OK": "OPTIMO",
        "PESO_FAIL": "GRASA_DIGITAL",
        "COLOR_OK": "MATCH",
        "COLOR_FAIL": "NO_MATCH",
        
        # Acciones
        "SOLICITAR_SELLO": "🏛️ SOLICITANDO_SELLO_SOBERANO",
        "SELLO_APLICADO": "🏆 SELLO_APLICADO",
        "RECHAZAR": "❌ PATRON_RECHAZADO",
        "CORREGIR": "🔄 SOLICITAR_CORRECCION",
        
        # Comunicación
        "PRESENTAR": "📊 PRESENTANDO_A_SOBERANO",
        "VALIDAR": "🔍 VALIDANDO_TECNICAMENTE",
        "ARCHIVAR": "📁 ARCHIVANDO_EN_MASTERED",
        "REGISTRAR": "🧠 REGISTRANDO_EN_LYZU"
    }
    
    @staticmethod
    def mensaje(codigo: str) -> str:
        return ProtocoloZei.MENSAJES.get(codigo, f"❓ CODIGO_DESCONOCIDO: {codigo}")


class JuesBotV2:
    """
    JUES-BOT V2.0 - Juez Universal de Estándares
    Ahora con capacidad de sellado automático
    """
    
    def __init__(self, blend_path: str, candidato_id: str, target_color_hex: str = "#FF0000"):
        self.blend_path = Path(blend_path)
        self.candidato_id = candidato_id
        self.target_color_hex = target_color_hex.upper()
        self.resultados = {
            "candidato_id": candidato_id,
            "timestamp": datetime.now().isoformat(),
            "protocolo_zei": {},
            "superpoderes": {},
            "dictamen": ProtocoloZei.mensaje("NO_APTO"),
            "sellado": None
        }
        self.MAX_FILE_SIZE_KB = 2000  # Aumentado para permitir materiales complejos
        
    # ========== 4 SUPERPODERES ==========
    
    def vision_rayos_x(self, obj) -> Dict:
        """Superpoder A: Detecta geometría corrupta"""
        if not obj or obj.type != 'MESH':
            return {"status": ProtocoloZei.mensaje("MALLA_FAIL"), "icon": "💀"}
        
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.mesh.select_non_manifold()
        
        bm = bmesh.from_edit_mesh(obj.data)
        no_manifold = sum(1 for e in bm.edges if e.select)
        bpy.ops.object.mode_set(mode='OBJECT')
        
        if no_manifold == 0:
            return {"status": ProtocoloZei.mensaje("MALLA_OK"), "icon": "✨"}
        return {"status": ProtocoloZei.mensaje("MALLA_FAIL"), "icon": "☠️"}
    
    def instinto_optimizacion(self) -> Dict:
        """Superpoder B: Detecta basura digital"""
        if not self.blend_path.exists():
            return {"status": "ERROR", "icon": "❓"}
        
        size_kb = round(self.blend_path.stat().st_size / 1024, 2)
        
        if size_kb > self.MAX_FILE_SIZE_KB:
            return {
                "status": ProtocoloZei.mensaje("PESO_FAIL"),
                "peso_kb": size_kb,
                "icon": "🐷"
            }
        return {
            "status": ProtocoloZei.mensaje("PESO_OK"),
            "peso_kb": size_kb,
            "icon": "⚡"
        }
    
    def sincronia_cromatica(self, obj) -> Dict:
        """Superpoder C: Valida color exacto"""
        if not obj or not obj.data.materials:
            return {"status": ProtocoloZei.mensaje("COLOR_FAIL"), "icon": "🎨❌"}
        
        mat = obj.data.materials[0]
        if not mat.use_nodes:
            return {"status": ProtocoloZei.mensaje("COLOR_FAIL"), "icon": "🎨❌"}
        
        principled = None
        for node in mat.node_tree.nodes:
            if node.type == 'BSDF_PRINCIPLED':
                principled = node
                break
        
        if not principled:
            return {"status": ProtocoloZei.mensaje("COLOR_FAIL"), "icon": "🎨❌"}
        
        color = principled.inputs['Base Color'].default_value
        r, g, b = int(color[0] * 255), int(color[1] * 255), int(color[2] * 255)
        hex_encontrado = f"#{r:02X}{g:02X}{b:02X}"
        
        match = hex_encontrado.upper() == self.target_color_hex.upper()
        
        if match:
            return {
                "status": ProtocoloZei.mensaje("COLOR_OK"),
                "color_encontrado": hex_encontrado,
                "icon": "🎯"
            }
        return {
            "status": ProtocoloZei.mensaje("COLOR_FAIL"),
            "color_encontrado": hex_encontrado,
            "color_esperado": self.target_color_hex,
            "icon": "🎨⚠️"
        }
    
    def sello_inmutabilidad(self, obj) -> Dict:
        """Superpoder D: Genera hash único"""
        if not obj or obj.type != 'MESH':
            return {"hash": "ERROR", "icon": "🔒❌"}
        
        coords_str = ""
        for v in obj.data.vertices:
            coords_str += f"{v.co.x:.3f},{v.co.y:.3f},{v.co.z:.3f};"
        for poly in obj.data.polygons:
            verts_indices = ",".join(str(v) for v in poly.vertices)
            coords_str += f"[{verts_indices}]"
        
        hash_md5 = hashlib.md5(coords_str.encode('utf-8')).hexdigest()
        
        return {
            "hash": hash_md5,
            "vertices_count": len(obj.data.vertices),
            "icon": "🔒"
        }
    
    # ========== FLUJO COMPLETO ==========
    
    def ejecutar_validacion(self) -> Dict:
        """Validación completa con 4 superpoderes"""
        print(f"\n{'='*70}")
        print(ProtocoloZei.mensaje("VALIDAR"))
        print(f"{'='*70}")
        
        # Cargar blend
        bpy.ops.wm.open_mainfile(filepath=str(self.blend_path))
        
        # Obtener objeto
        obj = None
        for o in bpy.context.scene.objects:
            if o.type == 'MESH':
                obj = o
                break
        
        # Ejecutar superpoderes
        sp = self.resultados["superpoderes"]
        sp["vision_rayos_x"] = self.vision_rayos_x(obj)
        sp["instinto_optimizacion"] = self.instinto_optimizacion()
        sp["sincronia_cromatica"] = self.sincronia_cromatica(obj)
        sp["sello_inmutabilidad"] = self.sello_inmutabilidad(obj)
        
        # Dashboard
        print(f"\n📊 DASHBOARD JUES-BOT")
        print(f"{'='*70}")
        print(f"   Malla: {sp['vision_rayos_x']['status']} {sp['vision_rayos_x']['icon']}")
        print(f"   Peso: {sp['instinto_optimizacion'].get('peso_kb', 0)} KB {sp['instinto_optimizacion']['icon']}")
        print(f"   Color: {sp['sincronia_cromatica']['status']} {sp['sincronia_cromatica']['icon']}")
        if 'color_encontrado' in sp['sincronia_cromatica']:
            print(f"      └─ {sp['sincronia_cromatica'].get('color_encontrado', 'N/A')}")
        print(f"   Hash: {sp['sello_inmutabilidad']['hash'][:16]}... {sp['sello_inmutabilidad']['icon']}")
        
        # Calcular dictamen
        errores = 0
        advertencias = 0
        
        if sp["vision_rayos_x"]["status"] == ProtocoloZei.mensaje("MALLA_FAIL"):
            errores += 1
        if sp["instinto_optimizacion"]["status"] == ProtocoloZei.mensaje("PESO_FAIL"):
            advertencias += 1
        if sp["sincronia_cromatica"]["status"] == ProtocoloZei.mensaje("COLOR_FAIL"):
            errores += 1
        
        if errores == 0 and advertencias == 0:
            dictamen = ProtocoloZei.mensaje("APTO")
        elif errores == 0 and advertencias > 0:
            dictamen = ProtocoloZei.mensaje("APTO_ADV")
        else:
            dictamen = ProtocoloZei.mensaje("NO_APTO")
        
        self.resultados["dictamen"] = dictamen
        self.resultados["errores"] = errores
        self.resultados["advertencias"] = advertencias
        
        print(f"\n🏛️ DICTAMEN: {dictamen}")
        print(f"   Errores: {errores} | Advertencias: {advertencias}")
        print(f"{'='*70}\n")
        
        return self.resultados
    
    # ========== SELLO AUTOMÁTICO ==========
    
    def aplicar_sello(self, aprobado_por: str = "Soberano") -> Dict:
        """
        SELLO AUTOMÁTICO - Cuando el Usuario dice OK
        Archiva en mastered/, crea certificado, actualiza registro
        """
        print(f"\n{'='*70}")
        print(ProtocoloZei.mensaje("SOLICITAR_SELLO"))
        print(f"{'='*70}")
        
        # Validar que esté APTO
        if self.resultados["dictamen"] not in [ProtocoloZei.mensaje("APTO"), ProtocoloZei.mensaje("APTO_ADV")]:
            print("❌ No se puede sellar - Dictamen NO_APTO")
            return {"status": "ERROR", "motivo": "NO_APTO"}
        
        # 1. Crear estructura mastered/
        pattern_folder = MASTERED / self.candidato_id
        folders = {
            'blend': pattern_folder / 'blend',
            'script': pattern_folder / 'script',
            'json': pattern_folder / 'json',
            'render': pattern_folder / 'render',
            'certificado': pattern_folder / 'certificado'
        }
        
        for folder in folders.values():
            folder.mkdir(parents=True, exist_ok=True)
        
        # 2. Copiar blend
        dst_blend = folders['blend'] / f"{self.candidato_id}.blend"
        shutil.copy2(self.blend_path, dst_blend)
        
        # 3. Crear certificado
        certificado = {
            "certificado_id": f"CERT-{self.candidato_id}-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "pattern_id": self.candidato_id,
            "fecha_sello": datetime.now().isoformat(),
            "sellado_por": aprobado_por,
            "decision": "SELLADO",
            "dictamen_jues": self.resultados["dictamen"],
            "validacion": {
                "malla": self.resultados["superpoderes"]["vision_rayos_x"]["status"],
                "peso_kb": self.resultados["superpoderes"]["instinto_optimizacion"].get("peso_kb", 0),
                "color": self.resultados["superpoderes"]["sincronia_cromatica"].get("color_encontrado", "N/A"),
                "hash": self.resultados["superpoderes"]["sello_inmutabilidad"]["hash"]
            }
        }
        
        cert_path = folders['certificado'] / "CERTIFICADO_SELLO.json"
        with open(cert_path, 'w', encoding='utf-8') as f:
            json.dump(certificado, f, indent=2, ensure_ascii=False)
        
        # 4. Crear JSON de metadatos
        metadata = {
            "pattern_id": self.candidato_id,
            "nombre_tecnico": self.candidato_id,
            "fecha_sello": datetime.now().isoformat(),
            "estado": "SELLADO",
            "sellado_por": aprobado_por,
            "validacion_jues": self.resultados["superpoderes"]
        }
        
        json_path = folders['json'] / f"{self.candidato_id}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        # 5. Actualizar REGISTRO_MAESTRO
        registro_path = ARCHIVO_ZULY / "REGISTRO_MAESTRO.json"
        if registro_path.exists():
            with open(registro_path, 'r', encoding='utf-8') as f:
                registro = json.load(f)
        else:
            registro = {"sistema": "ZULY", "total_patrones": 0, "patrones": []}
        
        registro["patrones"].append({
            "pattern_id": self.candidato_id,
            "nombre": self.candidato_id,
            "estado": "SELLADO",
            "fecha_sello": datetime.now().isoformat(),
            "ubicacion": f"por_estado_aprendizaje/mastered/{self.candidato_id}/"
        })
        registro["total_patrones"] = len(registro["patrones"])
        
        with open(registro_path, 'w', encoding='utf-8') as f:
            json.dump(registro, f, indent=2, ensure_ascii=False)
        
        # Resultado
        self.resultados["sellado"] = {
            "status": ProtocoloZei.mensaje("SELLO_APLICADO"),
            "ubicacion": str(pattern_folder),
            "certificado": str(cert_path),
            "registro": str(registro_path)
        }
        
        print(f"✅ {ProtocoloZei.mensaje('SELLO_APLICADO')}")
        print(f"   📁 Ubicación: {pattern_folder}")
        print(f"   📜 Certificado: {cert_path.name}")
        print(f"   📚 Registro actualizado: {registro['total_patrones']} patrones")
        print(f"{'='*70}\n")
        
        return self.resultados["sellado"]


def jues_bot_validar_y_sellar(blend_path: str, candidato_id: str, target_color: str, aprobar: bool = False) -> Dict:
    """
    FUNCIÓN PRINCIPAL - Uso desde scripts
    
    Args:
        blend_path: Ruta al archivo .blend
        candidato_id: ID del patrón (ej: "CUB-001")
        target_color: Color objetivo (ej: "#1A4DCC")
        aprobar: Si True, aplica sello automáticamente
    
    Returns:
        Dict con resultados completos
    """
    jues = JuesBotV2(blend_path, candidato_id, target_color)
    
    # Paso 1: Validar
    resultados = jues.ejecutar_validacion()
    
    # Paso 2: Si aprobar=True y está APTO, sellar automáticamente
    if aprobar and resultados["dictamen"] == ProtocoloZei.mensaje("APTO"):
        sello = jues.aplicar_sello("Soberano")
        resultados["sellado"] = sello
    
    return resultados


if __name__ == "__main__":
    # Uso directo: python jues_bot_v2.py <blend> <id> <color> [aprobar]
    if len(sys.argv) >= 4:
        blend = sys.argv[1]
        candidato = sys.argv[2]
        color = sys.argv[3]
        aprobar = len(sys.argv) > 4 and sys.argv[4].lower() in ["true", "ok", "si", "s"]
        
        resultados = jues_bot_validar_y_sellar(blend, candidato, color, aprobar)
        
        # Imprimir resultado para scripts
        print(f"\nRESULTADO_FINAL: {resultados['dictamen']}")
        if resultados.get('sellado'):
            print(f"SELLO: {resultados['sellado']['status']}")
    else:
        print("Uso: python jues_bot_v2.py <blend> <candidato_id> <color_hex> [aprobar]")
        print("Ejemplo: python jues_bot_v2.py cubo.blend CUB-001 #1A4DCC true")
