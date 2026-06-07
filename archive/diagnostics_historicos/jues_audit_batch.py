#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 AUDITORÍA JUES-BOT - Script independiente para batch auditing
"""

import bpy
import bmesh
import json
from datetime import datetime
from pathlib import Path

def audit_model_complete(blend_path, target_color="#FFFFFF"):
    """
    Auditoría completa de un modelo .blend
    Retorna dict con score, dictamen y métricas
    """
    # Cargar archivo
    bpy.ops.wm.open_mainfile(filepath=str(blend_path))
    
    scene = bpy.context.scene
    total_deduction = 0
    all_errors = []
    all_metrics = {}
    superpoderes = {}
    
    # 1. AUDITORÍA RENDER ENGINE
    engine = scene.render.engine
    if engine == 'BLENDER_EEVEE':
        if not scene.eevee.use_ssr:
            all_errors.append(("MAYOR", "SSR desactivado"))
            total_deduction -= 15
    
    superpoderes["render_engine"] = {
        "status": f"Motor: {engine}",
        "icon": "🎨"
    }
    
    # 2. AUDITORÍA GEOMETRÍA - Todos los objetos mesh
    mesh_objects = [obj for obj in scene.objects if obj.type == 'MESH']
    
    for obj in mesh_objects:
        bm = bmesh.new()
        try:
            bm.from_mesh(obj.data)
            bm.verts.ensure_lookup_table()
            bm.edges.ensure_lookup_table()
            bm.faces.ensure_lookup_table()
            
            # Métricas
            dims = obj.dimensions
            all_metrics[f"{obj.name}_dims"] = f"{dims.x:.2f}x{dims.y:.2f}x{dims.z:.2f}m"
            all_metrics[f"{obj.name}_verts"] = len(bm.verts)
            all_metrics[f"{obj.name}_faces"] = len(bm.faces)
            
            # Non-manifold
            non_manifold = len([e for e in bm.edges if not e.is_manifold])
            if non_manifold:
                all_errors.append(("CRITICO", f"{obj.name}: {non_manifold} non-manifold"))
                total_deduction -= 30
            
            # Vértices sueltos (sin caras conectadas)
            loose = len([v for v in bm.verts if not v.link_faces])
            if loose:
                all_errors.append(("CRITICO", f"{obj.name}: {loose} vértices sueltos"))
                total_deduction -= 30
            
            # Vértices duplicados
            vert_coords = {}
            duplicates = 0
            for v in bm.verts:
                key = (round(v.co.x, 4), round(v.co.y, 4), round(v.co.z, 4))
                if key in vert_coords:
                    duplicates += 1
                else:
                    vert_coords[key] = True
            if duplicates:
                all_errors.append(("MAYOR", f"{obj.name}: {duplicates} duplicados"))
                total_deduction -= 15
            
            # N-Gons
            ngons = len([f for f in bm.faces if len(f.verts) > 4])
            if ngons:
                all_errors.append(("MAYOR", f"{obj.name}: {ngons} N-Gons"))
                total_deduction -= 15
            
            # Escala no aplicada
            if any(abs(s - 1.0) > 0.001 for s in obj.scale):
                all_errors.append(("MAYOR", f"{obj.name}: Escala no aplicada"))
                total_deduction -= 15
                
        finally:
            bm.free()
    
    superpoderes["geometria"] = {
        "status": f"{len(mesh_objects)} objetos mesh auditados",
        "icon": "🔷"
    }
    
    # 3. AUDITORÍA MATERIALES
    color_match = False
    color_found = "N/A"
    
    for obj in mesh_objects:
        if obj.data.materials:
            mat = obj.data.materials[0]
            if mat and mat.use_nodes:
                for node in mat.node_tree.nodes:
                    if node.type == 'BSDF_PRINCIPLED':
                        color = node.inputs['Base Color'].default_value
                        r, g, b = int(color[0]*255), int(color[1]*255), int(color[2]*255)
                        hex_color = f"#{r:02X}{g:02X}{b:02X}"
                        color_found = hex_color
                        color_match = hex_color.upper() == target_color.upper()
                        break
    
    if not color_match and color_found != "N/A":
        all_errors.append(("MAYOR", f"Color no coincide: {color_found} vs {target_color}"))
        total_deduction -= 15
    
    superpoderes["materiales"] = {
        "status": f"Color: {color_found} (Match: {color_match})",
        "icon": "🎨" if color_match else "🎨⚠️"
    }
    
    # 4. AUDITORÍA ESCENA
    if not scene.camera:
        all_errors.append(("MAYOR", "Sin cámara"))
        total_deduction -= 15
    
    superpoderes["escena"] = {
        "status": "OK" if scene.camera else "Sin cámara",
        "icon": "📷" if scene.camera else "📷❌"
    }
    
    # CÁLCULO FINAL
    score = max(0, 100 + total_deduction)
    
    if score >= 80:
        dictamen = "APTO"
    elif score >= 60:
        dictamen = "APTO_CON_ADVERTENCIAS"
    else:
        dictamen = "NO_APTO"
    
    return {
        "candidato_id": Path(blend_path).stem,
        "score": score,
        "dictamen": dictamen,
        "timestamp": datetime.now().isoformat(),
        "superpoderes": superpoderes,
        "metricas": all_metrics,
        "errores": all_errors,
        "total_objetos": len(mesh_objects)
    }

if __name__ == "__main__":
    import sys
    
    # Leer argumentos después de --
    try:
        dash_index = sys.argv.index('--')
        args = sys.argv[dash_index + 1:]
    except ValueError:
        # Si no hay --, buscar argumentos que parezcan rutas
        args = [a for a in sys.argv if a.endswith('.blend') or a.startswith('#')]
    
    if len(args) >= 2:
        blend_path = args[0]
        target_color = args[1]
        
        resultado = audit_model_complete(blend_path, target_color)
        
        print("\n" + "="*70)
        print("📊 RESULTADO AUDITORÍA JUES-BOT")
        print("="*70)
        print(f"Modelo: {resultado['candidato_id']}")
        print(f"Score: {resultado['score']}/100")
        print(f"Dictamen: {resultado['dictamen']}")
        print(f"Objetos: {resultado['total_objetos']}")
        
        print("\n🔍 Superpoderes:")
        for sp_name, sp_data in resultado['superpoderes'].items():
            print(f"  {sp_data['icon']} {sp_name}: {sp_data['status']}")
        
        if resultado['errores']:
            print("\n🚨 Errores:")
            for sev, msg in resultado['errores'][:5]:  # Mostrar solo primeros 5
                print(f"  [{sev}] {msg}")
        
        print("\n" + "="*70)
        
        # Guardar JSON
        report_path = Path(blend_path).parent / f"{resultado['candidato_id']}_AUDIT.json"
        with open(report_path, 'w') as f:
            json.dump(resultado, f, indent=2)
        print(f"💾 Reporte guardado: {report_path}")
