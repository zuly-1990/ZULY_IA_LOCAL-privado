#!/usr/bin/env python3
"""
🤖 JUES-BOT V1.0 - SISTEMA DE VALIDACIÓN TÉCNICA ZULY
Juez Universal de Estándares para Blender

4 SUPERPODERES:
A. Visión de Rayos X (Manifold/Topología)
B. Instinto de Optimización (Grasa Digital)
C. Sincronía Cromática (ADN de Color)
D. Sello de Inmutabilidad (Hash de Vértices)
"""

import bpy
import bmesh
import sys
import json
import hashlib
import os
import math
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional

# Importar Sistema de Luces Inteligente
sys.path.insert(0, str(Path(__file__).parent))
from sistema_luces_inteligente import aplicar_iluminacion_profesional

# RUTA DEL EJECUTABLE BLENDER
BLENDER_EXE = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe"

class JuesBotValidator:
    """
    JUES-BOT: El juez técnico indestructible.
    Valida geometría, eficiencia, color y genera hashes únicos.
    """
    
    def __init__(self, blend_path: str, candidato_id: str, target_color_hex: str = "#FF0000"):
        self.blend_path = Path(blend_path)
        self.candidato_id = candidato_id
        self.target_color_hex = target_color_hex.upper()
        
        # Resultados de validación
        self.resultados = {
            "candidato_id": candidato_id,
            "timestamp": datetime.now().isoformat(),
            "superpoderes": {},
            "dashboard": {},
            "dictamen": "PENDIENTE"
        }
        
        # Umbrales
        self.MAX_FILE_SIZE_KB = 500  # Para primitivas simples
    
    # =====================================================================
    # SUPERPODER A: VISIÓN DE RAYOS X (Topología/Manifold)
    # =====================================================================
    def check_manifold(self, obj) -> Dict:
        """
        Superpoder A: Visión de Rayos X
        Detecta bordes abiertos, caras internas, geometría corrupta.
        """
        if not obj or obj.type != 'MESH':
            return {
                "status": "CORRUPTA",
                "detalle": "No hay objeto mesh",
                "vertices_no_manifold": -1,
                "icon": "💀"
            }
        
        # Entrar modo edit
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='DESELECT')
        
        # Seleccionar no-manifold
        bpy.ops.mesh.select_non_manifold()
        
        # Contar - usar from_edit_mesh que funciona en modo edit
        bm = bmesh.from_edit_mesh(obj.data)
        no_manifold_edges = sum(1 for e in bm.edges if e.select)
        no_manifold_verts = sum(1 for v in bm.verts if v.select)
        # No hacer bm.free() con from_edit_mesh, se maneja automáticamente
        
        bpy.ops.object.mode_set(mode='OBJECT')
        
        if no_manifold_edges == 0 and no_manifold_verts == 0:
            return {
                "status": "LIMPIA",
                "detalle": "Geometría completamente cerrada y válida",
                "vertices_no_manifold": 0,
                "edges_no_manifold": 0,
                "icon": "✨"
            }
        else:
            return {
                "status": "CORRUPTA",
                "detalle": f"Detectados {no_manifold_verts} vértices y {no_manifold_edges} bordes no-manifold",
                "vertices_no_manifold": no_manifold_verts,
                "edges_no_manifold": no_manifold_edges,
                "icon": "☠️"
            }
    
    # =====================================================================
    # SUPERPODER B: INSTINTO DE OPTIMIZACIÓN (Grasa Digital)
    # =====================================================================
    def check_efficiency(self, file_path: str) -> Dict:
        """
        Superpoder B: Instinto de Optimización
        Detecta archivos .blend con peso excesivo (basura digital).
        """
        path = Path(file_path)
        
        if not path.exists():
            return {
                "status": "ERROR",
                "peso_kb": 0,
                "alerta": "Archivo no encontrado",
                "icon": "❓"
            }
        
        size_bytes = path.stat().st_size
        size_kb = round(size_bytes / 1024, 2)
        
        if size_kb > self.MAX_FILE_SIZE_KB:
            return {
                "status": "GRASA_DIGITAL",
                "peso_kb": size_kb,
                "limite_kb": self.MAX_FILE_SIZE_KB,
                "alerta": f"⚠️ BASURA DIGITAL DETECTADA: {size_kb}KB > {self.MAX_FILE_SIZE_KB}KB",
                "icon": "🐷"
            }
        else:
            return {
                "status": "OPTIMO",
                "peso_kb": size_kb,
                "limite_kb": self.MAX_FILE_SIZE_KB,
                "alerta": None,
                "icon": "⚡"
            }
    
    # =====================================================================
    # SUPERPODER C: SINCRONÍA CROMÁTICA (ADN de Color)
    # =====================================================================
    def validate_materials(self, obj, target_hex: str = None) -> Dict:
        """
        Superpoder C: Sincronía Cromática
        Verifica que el material coincida exactamente con el color objetivo.
        """
        if target_hex is None:
            target_hex = self.target_color_hex
        
        # DEBUG - Mostrar info del objeto
        print(f"      DEBUG: Objeto = {obj.name if obj else 'None'}")
        print(f"      DEBUG: Materiales = {len(obj.data.materials) if obj and obj.data.materials else 0}")
        
        if not obj or not obj.data.materials:
            return {
                "status": "NO_MATCH",
                "color_encontrado": None,
                "color_esperado": target_hex,
                "diferencia": "No hay material",
                "icon": "🎨❌"
            }
        
        mat = obj.data.materials[0]
        print(f"      DEBUG: Material[0] = {mat.name if mat else 'None'}")
        
        if not mat.use_nodes:
            return {
                "status": "NO_MATCH",
                "color_encontrado": None,
                "color_esperado": target_hex,
                "diferencia": "Material sin nodos",
                "icon": "🎨❌"
            }
        
        # Obtener Principled BSDF
        principled = None
        for node in mat.node_tree.nodes:
            if node.type == 'BSDF_PRINCIPLED':
                principled = node
                break
        
        if not principled:
            return {
                "status": "NO_MATCH",
                "color_encontrado": None,
                "color_esperado": target_hex,
                "diferencia": "No hay Principled BSDF",
                "icon": "🎨❌"
            }
        
        # Extraer color
        color = principled.inputs['Base Color'].default_value
        r, g, b = int(color[0] * 255), int(color[1] * 255), int(color[2] * 255)
        hex_encontrado = f"#{r:02X}{g:02X}{b:02X}"
        
        print(f"      DEBUG: Color leído = {hex_encontrado} (RGB: {r},{g},{b})")
        
        # Comparar
        match = hex_encontrado.upper() == target_hex.upper()
        
        if match:
            return {
                "status": "MATCH",
                "color_encontrado": hex_encontrado,
                "color_esperado": target_hex,
                "rgb": (r, g, b),
                "diferencia": "0%",
                "icon": "🎯"
            }
        else:
            # Calcular diferencia
            target_rgb = tuple(int(target_hex.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
            diff = sum(abs(a - b) for a, b in zip((r, g, b), target_rgb)) / 3
            diff_pct = min(100, round((diff / 255) * 100, 1))
            
            return {
                "status": "NO_MATCH",
                "color_encontrado": hex_encontrado,
                "color_esperado": target_hex,
                "rgb": (r, g, b),
                "diferencia": f"{diff_pct}%",
                "icon": "🎨⚠️"
            }
    
    # =====================================================================
    # SUPERPODER D: SELLO DE INMUTABILIDAD (Hash MD5 de Vértices)
    # =====================================================================
    def generate_geometry_hash(self, obj) -> Dict:
        """
        Superpoder D: Sello de Inmutabilidad
        Genera hash MD5 único de la posición de cada vértice.
        Este hash se guarda en REGISTRO_MAESTRO.json
        """
        if not obj or obj.type != 'MESH':
            return {
                "hash": "ERROR_NO_MESH",
                "vertices_count": 0,
                "icon": "🔒❌"
            }
        
        # Crear string de coordenadas
        coords_str = ""
        for v in obj.data.vertices:
            # 3 decimales de precisión
            coords_str += f"{v.co.x:.3f},{v.co.y:.3f},{v.co.z:.3f};"
        
        # Agregar información de caras (índices de vértices por cara)
        for poly in obj.data.polygons:
            verts_indices = ",".join(str(v) for v in poly.vertices)
            coords_str += f"[{verts_indices}]"
        
        # Generar MD5
        hash_md5 = hashlib.md5(coords_str.encode('utf-8')).hexdigest()
        
        return {
            "hash": hash_md5,
            "vertices_count": len(obj.data.vertices),
            "faces_count": len(obj.data.polygons),
            "icon": "🔒"
        }
    
    # =====================================================================
    # EJECUCIÓN COMPLETA Y DASHBOARD
    # =====================================================================
    def ejecutar_inspeccion_completa(self) -> Dict:
        """
        Ejecuta los 4 superpoderes y genera el dashboard protocolar.
        """
        print(f"\n{'='*70}")
        print(f"🤖 JUES-BOT INICIANDO INSPECCIÓN: {self.candidato_id}")
        print(f"{'='*70}")
        
        # Obtener objeto principal (asume que es el primero de tipo MESH)
        obj = None
        for o in bpy.context.scene.objects:
            if o.type == 'MESH':
                obj = o
                break
        
        # GUARDAR REFERENCIA AL OBJETO ORIGINAL
        objeto_original = obj
        print(f"   Objeto detectado: {objeto_original.name if objeto_original else 'None'}")
        
        # APLICAR SISTEMA DE LUCES INTELIGENTE ANTES DE VALIDAR
        if obj:
            print("\n💡 Aplicando Sistema de Luces Inteligente v2.0 (SLIZ)...")
            luces = aplicar_iluminacion_profesional(obj)
            print(f"   ☀️  Sol:   {luces['sol']}   (Luz direccional ambiental)")
            print(f"   ✨ Key:   {luces['key']}   (Luz principal)")
            print(f"   💫 Fill:  {luces['fill']}  (Luz de relleno)")
            print(f"   🌟 Rim:   {luces['rim']}    (Luz de contorno)")
            print(f"   ✓ Todas las luces apuntan al centro del objeto")
        
        # Ejecutar 4 superpoderes - USAR objeto_original
        print("\n🔍 Aplicando superpoderes...")
        
        # A. Visión de Rayos X
        manifold_result = self.check_manifold(objeto_original)
        self.resultados["superpoderes"]["vision_rayos_x"] = manifold_result
        print(f"   {manifold_result['icon']} Visión Rayos X: {manifold_result['status']}")
        
        # B. Instinto de Optimización
        efficiency_result = self.check_efficiency(str(self.blend_path))
        self.resultados["superpoderes"]["instinto_optimizacion"] = efficiency_result
        print(f"   {efficiency_result['icon']} Instinto Optimización: {efficiency_result['peso_kb']}KB")
        if efficiency_result['alerta']:
            print(f"      ⚠️ {efficiency_result['alerta']}")
        
        # C. Sincronía Cromática - USAR objeto_original
        color_result = self.validate_materials(objeto_original)
        self.resultados["superpoderes"]["sincronia_cromatica"] = color_result
        print(f"   {color_result['icon']} Sincronía Cromática: {color_result['status']}")
        if color_result['status'] == 'NO_MATCH':
            print(f"      Esperado: {color_result['color_esperado']}")
            print(f"      Encontrado: {color_result['color_encontrado']}")
        
        # D. Sello de Inmutabilidad - USAR objeto_original
        hash_result = self.generate_geometry_hash(objeto_original)
        self.resultados["superpoderes"]["sello_inmutabilidad"] = hash_result
        print(f"   {hash_result['icon']} Sello Inmutabilidad: {hash_result['hash'][:16]}...")
        print(f"      Vértices: {hash_result['vertices_count']}, Caras: {hash_result['faces_count']}")
        
        # Generar Dashboard
        self._generar_dashboard()
        
        # Calcular dictamen
        self._calcular_dictamen()
        
        return self.resultados
    
    def _generar_dashboard(self):
        """
        Genera el Dashboard Protocolar para el Soberano.
        """
        sp = self.resultados["superpoderes"]
        
        dashboard = {
            "estado_malla": sp["vision_rayos_x"]["status"],
            "estado_malla_icon": sp["vision_rayos_x"]["icon"],
            
            "concordancia_color": sp["sincronia_cromatica"]["status"],
            "color_encontrado": sp["sincronia_cromatica"].get("color_encontrado", "N/A"),
            "concordancia_icon": sp["sincronia_cromatica"]["icon"],
            
            "peso_patron_kb": sp["instinto_optimizacion"]["peso_kb"],
            "peso_alerta": sp["instinto_optimizacion"].get("alerta"),
            
            "hash_inmutabilidad": sp["sello_inmutabilidad"]["hash"],
            "hash_corto": sp["sello_inmutabilidad"]["hash"][:16] + "...",
            "vertices_count": sp["sello_inmutabilidad"]["vertices_count"]
        }
        
        self.resultados["dashboard"] = dashboard
        
        # Imprimir Dashboard
        print(f"\n{'='*70}")
        print(f"📊 DASHBOARD JUES-BOT - {self.candidato_id}")
        print(f"{'='*70}")
        print(f"   ESTADO DE MALLA:          [{dashboard['estado_malla']}] {dashboard['estado_malla_icon']}")
        print(f"   CONCORDANCIA DE COLOR:    [{dashboard['concordancia_color']}] {dashboard['concordancia_icon']}")
        print(f"      └─ Color detectado: {dashboard['color_encontrado']}")
        print(f"   PESO DE PATRÓN:           [{dashboard['peso_patron_kb']} KB]")
        if dashboard['peso_alerta']:
            print(f"      ⚠️ {dashboard['peso_alerta']}")
        print(f"   HASH DE INMUTABILIDAD:    [{dashboard['hash_corto']}]")
        print(f"      └─ Vértices: {dashboard['vertices_count']}")
        print(f"{'='*70}")
    
    def _calcular_dictamen(self):
        """
        Calcula el dictamen final basado en los 4 superpoderes.
        """
        sp = self.resultados["superpoderes"]
        
        errores = 0
        advertencias = 0
        
        # Verificar manifold
        if sp["vision_rayos_x"]["status"] == "CORRUPTA":
            errores += 1
        
        # Verificar eficiencia
        if sp["instinto_optimizacion"]["status"] == "GRASA_DIGITAL":
            advertencias += 1
        
        # Verificar color
        if sp["sincronia_cromatica"]["status"] == "NO_MATCH":
            errores += 1
        
        # Hash siempre pasa (es solo registro)
        
        # Dictamen
        if errores == 0 and advertencias == 0:
            dictamen = "✅ APTO_PARA_SELLO"
        elif errores == 0 and advertencias > 0:
            dictamen = "⚠️ APTO_CON_ADVERTENCIAS"
        else:
            dictamen = "❌ NO_APTO"
        
        self.resultados["dictamen"] = dictamen
        self.resultados["errores"] = errores
        self.resultados["advertencias"] = advertencias
        
        print(f"\n🏛️  DICTAMEN FINAL: {dictamen}")
        print(f"   Errores: {errores} | Advertencias: {advertencias}")
        print(f"{'='*70}\n")
    
    def guardar_reporte(self, output_path: str = None) -> str:
        """
        Guarda el reporte completo en JSON.
        """
        if output_path is None:
            output_path = str(self.blend_path).replace(".blend", "_JUES_REPORT.json")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.resultados, f, indent=2, ensure_ascii=False)
        
        return output_path


# =============================================================================
# FUNCIÓN: COMPARAR MÚLTIPLES CANDIDATOS (FASE DE ARENA)
# =============================================================================

def jues_bot_comparar_arena(candidatos: List[Tuple[str, str, str]]) -> Dict:
    """
    Compara múltiples candidatos en la arena y recomienda el mejor.
    
    Args:
        candidatos: Lista de (blend_path, candidato_id, target_color_hex)
    
    Returns:
        Dict con ranking y recomendación
    """
    print("\n" + "="*70)
    print("⚔️  FASE DE ARENA - JUES-BOT EVALUANDO CANDIDATOS")
    print("="*70)
    
    resultados_arena = []
    
    for blend_path, candidato_id, target_color in candidatos:
        print(f"\n{'─'*70}")
        print(f"🥊 CANDIDATO: {candidato_id}")
        print(f"{'─'*70}")
        
        # Abrir archivo
        bpy.ops.wm.open_mainfile(filepath=blend_path)
        
        # Ejecutar JUES-BOT
        jues = JuesBotValidator(blend_path, candidato_id, target_color)
        resultado = jues.ejecutar_inspeccion_completa()
        
        # Calcular puntuación
        puntos = 0
        if resultado["superpoderes"]["vision_rayos_x"]["status"] == "LIMPIA":
            puntos += 25
        if resultado["superpoderes"]["instinto_optimizacion"]["status"] == "OPTIMO":
            puntos += 25
        if resultado["superpoderes"]["sincronia_cromatica"]["status"] == "MATCH":
            puntos += 25
        if resultado["superpoderes"]["sello_inmutabilidad"]["hash"] != "ERROR_NO_MESH":
            puntos += 25
        
        resultado["puntuacion_jues"] = puntos
        resultados_arena.append(resultado)
        
        # Guardar reporte individual
        report_path = jues.guardar_reporte()
        print(f"📄 Reporte guardado: {report_path}")
    
    # Ranking
    print(f"\n{'='*70}")
    print("🏆 RANKING FASE DE ARENA")
    print("="*70)
    
    ranking = sorted(resultados_arena, key=lambda x: x["puntuacion_jues"], reverse=True)
    
    for i, r in enumerate(ranking, 1):
        medalla = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
        print(f"   {medalla} {r['candidato_id']}: {r['puntuacion_jues']}/100 pts | {r['dictamen']}")
    
    ganador = ranking[0] if ranking else None
    
    print(f"\n🎯 RECOMENDACIÓN JUES-BOT: {ganador['candidato_id']}")
    print(f"   Puntuación: {ganador['puntuacion_jues']}/100")
    print("="*70)
    
    return {
        "ranking": ranking,
        "ganador_recomendado": ganador,
        "total_evaluados": len(candidatos)
    }


# =============================================================================
# USO DIRECTO DESDE LÍNEA DE COMANDOS
# =============================================================================

if __name__ == "__main__":
    if len(sys.argv) >= 3:
        blend_file = sys.argv[1]
        candidato = sys.argv[2]
        color_hex = sys.argv[3] if len(sys.argv) > 3 else "#FF0000"
        
        # Ejecutar
        jues = JuesBotValidator(blend_file, candidato, color_hex)
        resultado = jues.ejecutar_inspeccion_completa()
        
        # Guardar
        report_path = jues.guardar_reporte()
        
        # Exit code
        sys.exit(0 if resultado["errores"] == 0 else 1)
    else:
        print("Uso: python jues_bot_validator.py <blend_file> <candidato_id> [color_hex]")
        print("Ejemplo: python jues_bot_validator.py ./cubo.blend Candidato_A #FF0000")
