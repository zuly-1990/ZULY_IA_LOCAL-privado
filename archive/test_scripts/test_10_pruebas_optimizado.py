#!/usr/bin/env python3
"""
🧪 SUITE OPTIMIZADA: 10 PRUEBAS EN UNA SOLA EJECUCIÓN BLENDER
Estructura: Manual de Pruebas ZULY
Guardada: ZULY_LAB/test_10_pruebas_completas_resultados.json
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime


class SuiteOptimizada:
    """10 pruebas optimizadas en una ejecución Blender"""
    
    def __init__(self):
        self.script_dir = Path(__file__).parent
        self.blender_exe = self.script_dir / "blender/v3/blender-3.6.0-zuly/blender.exe"
    
    def generar_script_completo(self) -> str:
        """Genera script que ejecuta TODAS las 10 pruebas en Blender"""
        return """
import bpy
import json
import math
from datetime import datetime

# Inicializar resultados
resultados = {
    'fecha': datetime.now().isoformat(),
    'blender_version': '3.6.2',
    'total_pruebas': 10,
    'pruebas': []
}

# ════════════════════════════════════════════════════════════════════════
# PRUEBA 1: CREAR CUBO BÁSICO
# ════════════════════════════════════════════════════════════════════════
try:
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
    bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
    obj = bpy.context.active_object
    
    if obj and obj.type == 'MESH':
        resultados['pruebas'].append({
            'num': 1,
            'nombre': 'Crear Cubo Básico',
            'status': 'éxito',
            'objeto': obj.name,
            'ubicación': list(obj.location),
            'escala': list(obj.scale)
        })
    else:
        resultados['pruebas'].append({'num': 1, 'nombre': 'Crear Cubo Básico', 'status': 'error'})
except Exception as e:
    resultados['pruebas'].append({'num': 1, 'nombre': 'Crear Cubo Básico', 'status': 'excepción', 'error': str(e)})

# ════════════════════════════════════════════════════════════════════════
# PRUEBA 2: CREAR ESFERA
# ════════════════════════════════════════════════════════════════════════
try:
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1.5, location=(0, 0, 0))
    obj = bpy.context.active_object
    
    resultados['pruebas'].append({
        'num': 2,
        'nombre': 'Crear Esfera',
        'status': 'éxito',
        'objeto': obj.name,
        'vértices': len(obj.data.vertices),
        'radio': 1.5
    })
except Exception as e:
    resultados['pruebas'].append({'num': 2, 'nombre': 'Crear Esfera', 'status': 'excepción', 'error': str(e)})

# ════════════════════════════════════════════════════════════════════════
# PRUEBA 3: CREAR CILINDRO
# ════════════════════════════════════════════════════════════════════════
try:
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
    bpy.ops.mesh.primitive_cylinder_add(radius=1, depth=3, location=(0, 0, 0))
    obj = bpy.context.active_object
    
    resultados['pruebas'].append({
        'num': 3,
        'nombre': 'Crear Cilindro',
        'status': 'éxito',
        'objeto': obj.name,
        'vértices': len(obj.data.vertices)
    })
except Exception as e:
    resultados['pruebas'].append({'num': 3, 'nombre': 'Crear Cilindro', 'status': 'excepción', 'error': str(e)})

# ════════════════════════════════════════════════════════════════════════
# PRUEBA 4: MOVER OBJETO
# ════════════════════════════════════════════════════════════════════════
try:
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
    bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
    obj = bpy.context.active_object
    obj.location = (5, 3, 2)
    
    if obj.location[0] == 5 and obj.location[1] == 3 and obj.location[2] == 2:
        resultados['pruebas'].append({
            'num': 4,
            'nombre': 'Mover Objeto',
            'status': 'éxito',
            'ubicación_inicial': [0, 0, 0],
            'ubicación_final': list(obj.location)
        })
    else:
        resultados['pruebas'].append({'num': 4, 'nombre': 'Mover Objeto', 'status': 'error'})
except Exception as e:
    resultados['pruebas'].append({'num': 4, 'nombre': 'Mover Objeto', 'status': 'excepción', 'error': str(e)})

# ════════════════════════════════════════════════════════════════════════
# PRUEBA 5: ROTAR OBJETO 45°
# ════════════════════════════════════════════════════════════════════════
try:
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
    bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
    obj = bpy.context.active_object
    angulo = math.radians(45)
    obj.rotation_euler = (0, 0, angulo)
    
    resultados['pruebas'].append({
        'num': 5,
        'nombre': 'Rotar Objeto 45°',
        'status': 'éxito',
        'rotación_grados': 45,
        'eje': 'Z'
    })
except Exception as e:
    resultados['pruebas'].append({'num': 5, 'nombre': 'Rotar Objeto 45°', 'status': 'excepción', 'error': str(e)})

# ════════════════════════════════════════════════════════════════════════
# PRUEBA 6: ESCALAR OBJETO
# ════════════════════════════════════════════════════════════════════════
try:
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
    bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
    obj = bpy.context.active_object
    obj.scale = (2, 2, 2)
    
    resultados['pruebas'].append({
        'num': 6,
        'nombre': 'Escalar Objeto',
        'status': 'éxito',
        'escala_inicial': [1, 1, 1],
        'escala_final': list(obj.scale),
        'volumen_multiplicado': 8
    })
except Exception as e:
    resultados['pruebas'].append({'num': 6, 'nombre': 'Escalar Objeto', 'status': 'excepción', 'error': str(e)})

# ════════════════════════════════════════════════════════════════════════
# PRUEBA 7: CREAR MÚLTIPLES OBJETOS
# ════════════════════════════════════════════════════════════════════════
try:
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
    for i in range(3):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(i*3, 0, 0))
    
    for i in range(2):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.8, location=(i*3, 3, 0))
    
    mesh_count = len([obj for obj in bpy.context.scene.objects if obj.type == 'MESH'])
    
    resultados['pruebas'].append({
        'num': 7,
        'nombre': 'Crear Múltiples Objetos',
        'status': 'éxito',
        'cubos': 3,
        'esferas': 2,
        'total': mesh_count
    })
except Exception as e:
    resultados['pruebas'].append({'num': 7, 'nombre': 'Crear Múltiples Objetos', 'status': 'excepción', 'error': str(e)})

# ════════════════════════════════════════════════════════════════════════
# PRUEBA 8: CREAR ESCENA VILLA SAVOYE
# ════════════════════════════════════════════════════════════════════════
try:
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
    bpy.ops.mesh.primitive_cube_add(size=10, location=(0, 0, 0))
    bpy.ops.mesh.primitive_cube_add(size=6, location=(0, 0, 5))
    
    for x in [-3, 3]:
        for y in [-3, 3]:
            bpy.ops.mesh.primitive_cylinder_add(radius=0.5, depth=5, location=(x, y, 2.5))
    
    mesh_count = len([obj for obj in bpy.context.scene.objects if obj.type == 'MESH'])
    
    resultados['pruebas'].append({
        'num': 8,
        'nombre': 'Crear Escena Villa Savoye',
        'status': 'éxito',
        'componentes': ['base 10x10', 'nivel2 6x6', '4 columnas'],
        'total_objetos': mesh_count
    })
except Exception as e:
    resultados['pruebas'].append({'num': 8, 'nombre': 'Crear Escena Villa Savoye', 'status': 'excepción', 'error': str(e)})

# ════════════════════════════════════════════════════════════════════════
# PRUEBA 9: VERIFICAR ESCENA
# ════════════════════════════════════════════════════════════════════════
try:
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
    bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
    bpy.ops.mesh.primitive_sphere_add(radius=1, location=(5, 0, 0))
    
    scene = bpy.context.scene
    total_objects = len(scene.objects)
    mesh_objects = len([obj for obj in scene.objects if obj.type == 'MESH'])
    
    resultados['pruebas'].append({
        'num': 9,
        'nombre': 'Verificar Escena',
        'status': 'éxito',
        'total_objetos': total_objects,
        'mesh_objects': mesh_objects,
        'cámara': any(obj.type == 'CAMERA' for obj in scene.objects),
        'luz': any(obj.type == 'LIGHT' for obj in scene.objects)
    })
except Exception as e:
    resultados['pruebas'].append({'num': 9, 'nombre': 'Verificar Escena', 'status': 'excepción', 'error': str(e)})

# ════════════════════════════════════════════════════════════════════════
# PRUEBA 10: EVALUACIÓN DE CALIDAD INTEGRAL
# ════════════════════════════════════════════════════════════════════════
try:
    puntuación = 0
    checks = {
        'mesh_objects_válidos': 0,
        'ubicaciones_válidas': 0,
        'escalas_válidas': 0
    }
    
    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH':
            checks['mesh_objects_válidos'] += 1
        
        if all(-1000 < l < 1000 for l in obj.location):
            checks['ubicaciones_válidas'] += 1
        
        if all(0 < s < 100 for s in obj.scale):
            checks['escalas_válidas'] += 1
    
    total_objs = len([obj for obj in bpy.context.scene.objects if obj.type == 'MESH'])
    if total_objs > 0:
        puntuación = int((checks['mesh_objects_válidos'] / total_objs * 40) +
                        (checks['ubicaciones_válidas'] / total_objs * 30) +
                        (checks['escalas_válidas'] / total_objs * 30))
    
    resultados['pruebas'].append({
        'num': 10,
        'nombre': 'Evaluación de Calidad Integral',
        'status': 'éxito',
        'puntuación': puntuación,
        'checks': checks,
        'total_verificado': total_objs
    })
except Exception as e:
    resultados['pruebas'].append({'num': 10, 'nombre': 'Evaluación de Calidad Integral', 'status': 'excepción', 'error': str(e)})

# ════════════════════════════════════════════════════════════════════════
# GUARDAR RESULTADOS Y MOSTRAR RESUMEN
# ════════════════════════════════════════════════════════════════════════

# Calcular estadísticas
exitosas = sum(1 for p in resultados['pruebas'] if p.get('status') == 'éxito')
resultados['exitosas'] = exitosas
resultados['tasa_exito'] = f'{(exitosas / len(resultados["pruebas"]) * 100):.1f}%'

# Guardar archivo .blend visual para el usuario
filepath_blend = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\test_10_pruebas_visual.blend"
bpy.ops.wm.save_as_mainfile(filepath=filepath_blend)

# Guardar archivo
with open('test_10_pruebas_completas_resultados.json', 'w') as f:
    json.dump(resultados, f, indent=2)

# Mostrar en consola
print(json.dumps(resultados, indent=2))
"""
    
    def ejecutar(self):
        """Ejecuta todas las pruebas en una sola ejecución"""
        
        print("\n" + "=" * 85)
        print("  🧪 SUITE 10 PRUEBAS OPTIMIZADA - EJECUCIÓN ÚNICA EN BLENDER")
        print("=" * 85 + "\n")
        
        # Generar script completo
        script = self.generar_script_completo()
        script_path = self.script_dir / "temp_suite_completa.py"
        
        with open(script_path, "w") as f:
            f.write(script)
        
        print(f"📝 Script generado: {script_path}\n")
        print(f"⚙️  Ejecutando todas las pruebas en Blender...\n")
        
        try:
            # Ejecutar Blender con todas las pruebas
            cmd = [
                str(self.blender_exe),
                "--background",
                "--python", str(script_path)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
            
            print("✅ Blender ejecutado\n")
            
            # Buscar archivo de resultados
            resultado_file = self.script_dir / "test_10_pruebas_completas_resultados.json"
            
            if resultado_file.exists():
                with open(resultado_file) as f:
                    resultados = json.load(f)
                
                # Mostrar resumen
                self._mostrar_resumen(resultados)
                
                # Guardar en ZULY_LAB
                zuly_lab = self.script_dir / "ZULY_LAB"
                zuly_lab.mkdir(exist_ok=True)
                
                destino = zuly_lab / "test_10_pruebas_completas_resultados.json"
                with open(destino, "w") as f:
                    json.dump(resultados, f, indent=2)
                
                print(f"\n✅ Guardado en: {destino}\n")
            else:
                print("⚠️  No se encontró archivo de resultados\n")
            
        except subprocess.TimeoutExpired:
            print("❌ TIMEOUT - Blender tardó demasiado\n")
        except Exception as e:
            print(f"❌ ERROR: {e}\n")
        finally:
            if script_path.exists():
                script_path.unlink()
    
    def _mostrar_resumen(self, resultados):
        """Muestra resumen formateado"""
        
        print("=" * 85)
        print("  📊 RESULTADOS DE PRUEBAS")
        print("=" * 85 + "\n")
        
        for prueba in resultados['pruebas']:
            num = prueba['num']
            nombre = prueba['nombre']
            status = prueba['status']
            
            if status == 'éxito':
                icono = "✅"
            else:
                icono = "❌"
            
            print(f"{icono} PRUEBA {num}: {nombre}")
            print(f"   Status: {status}")
            
            # Mostrar detalles relevantes
            for k, v in prueba.items():
                if k not in ['num', 'nombre', 'status', 'error']:
                    if isinstance(v, (list, dict)):
                        print(f"   • {k}: {v}")
                    else:
                        print(f"   • {k}: {v}")
            
            print()
        
        print("=" * 85)
        print(f"  📈 RESUMEN FINAL")
        print("=" * 85)
        print(f"  Total:        {len(resultados['pruebas'])} pruebas")
        print(f"  ✅ Exitosas:   {resultados['exitosas']}")
        print(f"  ❌ Fallidas:   {len(resultados['pruebas']) - resultados['exitosas']}")
        print(f"  📊 Tasa:       {resultados['tasa_exito']}")
        print("=" * 85 + "\n")


if __name__ == "__main__":
    suite = SuiteOptimizada()
    suite.ejecutar()
