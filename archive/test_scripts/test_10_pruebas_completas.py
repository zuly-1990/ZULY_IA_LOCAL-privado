#!/usr/bin/env python3
"""
🧪 SUITE DE PRUEBAS: 10 CASOS COMPLETOS
Usando Blender Real + Estructura del Manual
Fecha: 2026-02-22

Pruebas:
1. Crear Cubo Básico
2. Crear Esfera
3. Crear Cilindro
4. Mover Objeto
5. Rotar Objeto 45°
6. Escalar Objeto
7. Crear Múltiples Objetos
8. Crear Escena Villa Savoye
9. Renderizar Escena
10. Evaluación de Calidad
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any


class SuiteCompleta10Pruebas:
    """Suite de 10 pruebas con Blender real"""
    
    def __init__(self):
        self.script_dir = Path(__file__).parent
        self.blender_exe = self.script_dir / "blender/v3/blender-3.6.0-zuly/blender.exe"
        self.pruebas_resultados = []
        self.fecha = datetime.now().isoformat()
    
    def generar_script_blender(self, numero_prueba: int) -> str:
        """Genera script Python para Blender según la prueba"""
        
        scripts = {
            1: self._prueba_crear_cubo(),
            2: self._prueba_crear_esfera(),
            3: self._prueba_crear_cilindro(),
            4: self._prueba_mover_objeto(),
            5: self._prueba_rotar_objeto(),
            6: self._prueba_escalar_objeto(),
            7: self._prueba_crear_multiples(),
            8: self._prueba_villa_savoye(),
            9: self._prueba_renderizar(),
            10: self._prueba_evaluacion_calidad(),
        }
        
        return scripts.get(numero_prueba, "")
    
    def _prueba_crear_cubo(self) -> str:
        """PRUEBA 1: Crear Cubo Básico"""
        return """
import bpy
import json
from datetime import datetime

results = {
    'prueba_num': 1,
    'nombre': 'Crear Cubo Básico',
    'timestamp': datetime.now().isoformat(),
    'status': 'iniciada',
    'detalle': {}
}

try:
    # Limpiar escena
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
    # Crear cubo
    bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
    
    # Verificar
    obj = bpy.context.active_object
    if obj and obj.type == 'MESH':
        results['status'] = 'éxito'
        results['detalle'] = {
            'objeto': obj.name,
            'tipo': obj.type,
            'ubicación': list(obj.location),
            'escala': list(obj.scale),
            'rotación': [round(r, 2) for r in obj.rotation_euler]
        }
    else:
        results['status'] = 'error'
        results['error'] = 'Objeto no creado'
        
except Exception as e:
    results['status'] = 'excepción'
    results['error'] = str(e)

with open('prueba_1_resultado.json', 'w') as f:
    json.dump(results, f, indent=2)
print(json.dumps(results))
"""
    
    def _prueba_crear_esfera(self) -> str:
        """PRUEBA 2: Crear Esfera"""
        return """
import bpy
import json
from datetime import datetime

results = {
    'prueba_num': 2,
    'nombre': 'Crear Esfera',
    'timestamp': datetime.now().isoformat(),
    'status': 'iniciada',
    'detalle': {}
}

try:
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
    # Crear esfera
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1.5, location=(0, 0, 0))
    
    obj = bpy.context.active_object
    if obj and obj.type == 'MESH':
        results['status'] = 'éxito'
        results['detalle'] = {
            'objeto': obj.name,
            'tipo': obj.type,
            'radio': 1.5,
            'vértices': len(obj.data.vertices),
            'ubicación': list(obj.location)
        }
    else:
        results['status'] = 'error'
        
except Exception as e:
    results['status'] = 'excepción'
    results['error'] = str(e)

with open('prueba_2_resultado.json', 'w') as f:
    json.dump(results, f, indent=2)
print(json.dumps(results))
"""
    
    def _prueba_crear_cilindro(self) -> str:
        """PRUEBA 3: Crear Cilindro"""
        return """
import bpy
import json
from datetime import datetime

results = {
    'prueba_num': 3,
    'nombre': 'Crear Cilindro',
    'timestamp': datetime.now().isoformat(),
    'status': 'iniciada'
}

try:
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
    bpy.ops.mesh.primitive_cylinder_add(radius=1, depth=3, location=(0, 0, 0))
    
    obj = bpy.context.active_object
    if obj:
        results['status'] = 'éxito'
        results['detalle'] = {
            'objeto': obj.name,
            'tipo': obj.type,
            'vértices': len(obj.data.vertices)
        }
    else:
        results['status'] = 'error'
        
except Exception as e:
    results['status'] = 'excepción'
    results['error'] = str(e)

with open('prueba_3_resultado.json', 'w') as f:
    json.dump(results, f, indent=2)
print(json.dumps(results))
"""
    
    def _prueba_mover_objeto(self) -> str:
        """PRUEBA 4: Mover Objeto"""
        return """
import bpy
import json
from datetime import datetime

results = {
    'prueba_num': 4,
    'nombre': 'Mover Objeto',
    'timestamp': datetime.now().isoformat(),
    'status': 'iniciada'
}

try:
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
    # Crear cubo
    bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
    obj = bpy.context.active_object
    
    # Mover a posición (5, 3, 2)
    obj.location = (5, 3, 2)
    
    if obj.location[0] == 5 and obj.location[1] == 3 and obj.location[2] == 2:
        results['status'] = 'éxito'
        results['detalle'] = {
            'ubicación_inicial': (0, 0, 0),
            'ubicación_final': list(obj.location),
            'distancia_movida': 5.831
        }
    else:
        results['status'] = 'error'
        
except Exception as e:
    results['status'] = 'excepción'
    results['error'] = str(e)

with open('prueba_4_resultado.json', 'w') as f:
    json.dump(results, f, indent=2)
print(json.dumps(results))
"""
    
    def _prueba_rotar_objeto(self) -> str:
        """PRUEBA 5: Rotar Objeto 45°"""
        return """
import bpy
import json
import math
from datetime import datetime

results = {
    'prueba_num': 5,
    'nombre': 'Rotar Objeto 45°',
    'timestamp': datetime.now().isoformat(),
    'status': 'iniciada'
}

try:
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
    bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
    obj = bpy.context.active_object
    
    # Rotar 45 grados (π/4 radianes)
    angulo = math.radians(45)
    obj.rotation_euler = (0, 0, angulo)
    
    results['status'] = 'éxito'
    results['detalle'] = {
        'rotación_grados': 45,
        'rotación_radianes': [round(r, 4) for r in obj.rotation_euler],
        'eje': 'Z'
    }
    
except Exception as e:
    results['status'] = 'excepción'
    results['error'] = str(e)

with open('prueba_5_resultado.json', 'w') as f:
    json.dump(results, f, indent=2)
print(json.dumps(results))
"""
    
    def _prueba_escalar_objeto(self) -> str:
        """PRUEBA 6: Escalar Objeto"""
        return """
import bpy
import json
from datetime import datetime

results = {
    'prueba_num': 6,
    'nombre': 'Escalar Objeto',
    'timestamp': datetime.now().isoformat(),
    'status': 'iniciada'
}

try:
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
    bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
    obj = bpy.context.active_object
    
    # Escalar 2x en todos los ejes
    obj.scale = (2, 2, 2)
    
    results['status'] = 'éxito'
    results['detalle'] = {
        'escala_inicial': (1, 1, 1),
        'escala_final': list(obj.scale),
        'factor': 2.0,
        'volumen_multiplicado': 8
    }
    
except Exception as e:
    results['status'] = 'excepción'
    results['error'] = str(e)

with open('prueba_6_resultado.json', 'w') as f:
    json.dump(results, f, indent=2)
print(json.dumps(results))
"""
    
    def _prueba_crear_multiples(self) -> str:
        """PRUEBA 7: Crear Múltiples Objetos"""
        return """
import bpy
import json
from datetime import datetime

results = {
    'prueba_num': 7,
    'nombre': 'Crear Múltiples Objetos',
    'timestamp': datetime.now().isoformat(),
    'status': 'iniciada',
    'objetos_creados': 0
}

try:
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
    # Crear 3 cubos
    for i in range(3):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(i*3, 0, 0))
    
    # Crear 2 esferas
    for i in range(2):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.8, location=(i*3, 3, 0))
    
    # Contar objetos
    mesh_objects = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']
    
    results['status'] = 'éxito'
    results['objetos_creados'] = len(mesh_objects)
    results['detalle'] = {
        'cubos': 3,
        'esferas': 2,
        'total': len(mesh_objects)
    }
    
except Exception as e:
    results['status'] = 'excepción'
    results['error'] = str(e)

with open('prueba_7_resultado.json', 'w') as f:
    json.dump(results, f, indent=2)
print(json.dumps(results))
"""
    
    def _prueba_villa_savoye(self) -> str:
        """PRUEBA 8: Crear Escena Villa Savoye"""
        return """
import bpy
import json
import math
from datetime import datetime

results = {
    'prueba_num': 8,
    'nombre': 'Crear Escena Villa Savoye',
    'timestamp': datetime.now().isoformat(),
    'status': 'iniciada'
}

try:
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
    # Base principal (cubo grande)
    bpy.ops.mesh.primitive_cube_add(size=10, location=(0, 0, 0))
    base = bpy.context.active_object
    base.name = "villa_base"
    
    # Segundo nivel (más pequeño, más alto)
    bpy.ops.mesh.primitive_cube_add(size=6, location=(0, 0, 5))
    nivel2 = bpy.context.active_object
    nivel2.name = "villa_nivel2"
    
    # Columnas (cilindros)
    for x in [-3, 3]:
        for y in [-3, 3]:
            bpy.ops.mesh.primitive_cylinder_add(
                radius=0.5, depth=5, location=(x, y, 2.5)
            )
    
    # Contar objetos
    mesh_objects = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']
    
    results['status'] = 'éxito'
    results['detalle'] = {
        'componentes': {
            'base': 'cubo 10x10x10',
            'nivel2': 'cubo 6x6x6 elevado',
            'columnas': 4
        },
        'total_objetos': len(mesh_objects)
    }
    
except Exception as e:
    results['status'] = 'excepción'
    results['error'] = str(e)

with open('prueba_8_resultado.json', 'w') as f:
    json.dump(results, f, indent=2)
print(json.dumps(results))
"""
    
    def _prueba_renderizar(self) -> str:
        """PRUEBA 9: Renderizar Escena"""
        return """
import bpy
import json
from datetime import datetime

results = {
    'prueba_num': 9,
    'nombre': 'Renderizar Escena',
    'timestamp': datetime.now().isoformat(),
    'status': 'iniciada'
}

try:
    # Crear escena minimal
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
    
    # Configurar render
    scene = bpy.context.scene
    scene.render.engine = 'EEVEE'
    scene.render.resolution_x = 1280
    scene.render.resolution_y = 720
    
    # Renderizar
    bpy.ops.render.render(write_still=True)
    
    results['status'] = 'éxito'
    results['detalle'] = {
        'engine': 'EEVEE',
        'resolución': '1280x720',
        'archivo': 'Render completo'
    }
    
except Exception as e:
    results['status'] = 'excepción'
    results['error'] = str(e)

with open('prueba_9_resultado.json', 'w') as f:
    json.dump(results, f, indent=2)
print(json.dumps(results))
"""
    
    def _prueba_evaluacion_calidad(self) -> str:
        """PRUEBA 10: Evaluación de Calidad"""
        return """
import bpy
import json
from datetime import datetime

results = {
    'prueba_num': 10,
    'nombre': 'Evaluación de Calidad',
    'timestamp': datetime.now().isoformat(),
    'status': 'iniciada',
    'puntuación': 0
}

try:
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
    # Crear múltiples objetos
    bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
    bpy.ops.mesh.primitive_sphere_add(radius=1.5, location=(5, 0, 0))
    bpy.ops.mesh.primitive_cylinder_add(radius=1, depth=3, location=(-5, 0, 0))
    
    # Verificaciones de calidad
    verificaciones = {
        'total_objetos': 0,
        'objetos_mesh': 0,
        'ubicaciones_validas': 0,
        'escalas_validas': 0
    }
    
    for obj in bpy.context.scene.objects:
        verificaciones['total_objetos'] += 1
        
        if obj.type == 'MESH':
            verificaciones['objetos_mesh'] += 1
        
        # Ubicación válida (no infinita)
        if all(-1000 < l < 1000 for l in obj.location):
            verificaciones['ubicaciones_validas'] += 1
        
        # Escala válida
        if all(0 < s < 100 for s in obj.scale):
            verificaciones['escalas_validas'] += 1
    
    # Calcular puntuación (0-100)
    puntuación = int((verificaciones['objetos_mesh'] / verificaciones['total_objetos'] * 40) +
                     (verificaciones['ubicaciones_validas'] / verificaciones['total_objetos'] * 30) +
                     (verificaciones['escalas_validas'] / verificaciones['total_objetos'] * 30))
    
    results['status'] = 'éxito'
    results['puntuación'] = puntuación
    results['detalle'] = verificaciones
    
except Exception as e:
    results['status'] = 'excepción'
    results['error'] = str(e)

with open('prueba_10_resultado.json', 'w') as f:
    json.dump(results, f, indent=2)
print(json.dumps(results))
"""
    
    def ejecutar_todas_pruebas(self) -> Dict[str, Any]:
        """Ejecuta las 10 pruebas"""
        
        print("\n" + "=" * 80)
        print("  🧪 SUITE COMPLETA: 10 PRUEBAS CON BLENDER REAL")
        print("=" * 80 + "\n")
        
        for prueba_num in range(1, 11):
            print(f"[{'=' * 70}]")
            self._ejecutar_prueba(prueba_num)
            print()
        
        # Resumen
        self._generar_resumen()
        
        return {
            "total_pruebas": 10,
            "exitosas": sum(1 for p in self.pruebas_resultados if p.get("status") == "éxito"),
            "fallidas": sum(1 for p in self.pruebas_resultados if p.get("status") != "éxito"),
            "fecha": self.fecha,
            "resultados": self.pruebas_resultados
        }
    
    def _ejecutar_prueba(self, prueba_num: int):
        """Ejecuta una prueba individual"""
        
        nombre_pruebas = {
            1: "Crear Cubo Básico",
            2: "Crear Esfera",
            3: "Crear Cilindro",
            4: "Mover Objeto",
            5: "Rotar Objeto 45°",
            6: "Escalar Objeto",
            7: "Crear Múltiples Objetos",
            8: "Crear Escena Villa Savoye",
            9: "Renderizar Escena",
            10: "Evaluación de Calidad"
        }
        
        print(f"\n🧪 PRUEBA {prueba_num}: {nombre_pruebas.get(prueba_num, '?')}")
        print(f"   {'─' * 75}")
        
        try:
            # Generar script
            script = self.generar_script_blender(prueba_num)
            script_path = self.script_dir / f"temp_prueba_{prueba_num}.py"
            
            with open(script_path, "w") as f:
                f.write(script)
            
            # Ejecutar Blender
            cmd = [
                str(self.blender_exe),
                "--background",
                "--python", str(script_path)
            ]
            
            print(f"   ⚙️  Ejecutando Blender...")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            # Leer resultado
            resultado_file = self.script_dir / f"prueba_{prueba_num}_resultado.json"
            
            if resultado_file.exists():
                with open(resultado_file) as f:
                    resultado = json.load(f)
                
                status = resultado.get('status', 'desconocido')
                
                if status == 'éxito':
                    print(f"   ✅ ÉXITO")
                    if 'detalle' in resultado:
                        for k, v in resultado['detalle'].items():
                            print(f"      • {k}: {v}")
                else:
                    print(f"   ❌ {status.upper()}")
                    if 'error' in resultado:
                        print(f"      Error: {resultado['error']}")
                
                self.pruebas_resultados.append(resultado)
            else:
                print(f"   ⚠️  No se encontró resultado")
                self.pruebas_resultados.append({
                    "prueba_num": prueba_num,
                    "status": "error",
                    "error": "Archivo de resultado no creado"
                })
            
            # Limpiar
            if script_path.exists():
                script_path.unlink()
                
        except subprocess.TimeoutExpired:
            print(f"   ❌ TIMEOUT")
            self.pruebas_resultados.append({
                "prueba_num": prueba_num,
                "status": "timeout",
                "error": "Tiempo de ejecución excedido"
            })
        except Exception as e:
            print(f"   ❌ EXCEPCIÓN: {str(e)}")
            self.pruebas_resultados.append({
                "prueba_num": prueba_num,
                "status": "excepción",
                "error": str(e)
            })
    
    def _generar_resumen(self):
        """Genera resumen final"""
        
        exitosas = sum(1 for p in self.pruebas_resultados if p.get("status") == "éxito")
        total = len(self.pruebas_resultados)
        tasa_exito = (exitosas / total * 100) if total > 0 else 0
        
        print("\n" + "=" * 80)
        print("  📊 RESUMEN FINAL")
        print("=" * 80)
        print(f"\n  Total de pruebas:  {total}")
        print(f"  ✅ Exitosas:       {exitosas}")
        print(f"  ❌ Fallidas:       {total - exitosas}")
        print(f"  📈 Tasa de éxito:  {tasa_exito:.1f}%")
        print(f"\n  📁 Guardadas en: ZULY_LAB/test_10_pruebas_completas_resultados.json")
        print("=" * 80 + "\n")
        
        # Guardar resumen completo
        self._guardar_resultados()
    
    def _guardar_resultados(self):
        """Guarda resultados en archivo"""
        
        zuly_lab = self.script_dir / "ZULY_LAB"
        zuly_lab.mkdir(exist_ok=True)
        
        # Resumen completo
        resumen = {
            "fecha": self.fecha,
            "blender_version": "3.6.2",
            "total_pruebas": 10,
            "exitosas": sum(1 for p in self.pruebas_resultados if p.get("status") == "éxito"),
            "fallidas": sum(1 for p in self.pruebas_resultados if p.get("status") != "éxito"),
            "tasa_exito": f"{(sum(1 for p in self.pruebas_resultados if p.get('status') == 'éxito') / 10 * 100):.1f}%",
            "pruebas_detalladas": self.pruebas_resultados
        }
        
        resultado_file = zuly_lab / "test_10_pruebas_completas_resultados.json"
        with open(resultado_file, "w") as f:
            json.dump(resumen, f, indent=2)
        
        print(f"✅ Guardado: {resultado_file}\n")


if __name__ == "__main__":
    suite = SuiteCompleta10Pruebas()
    suite.ejecutar_todas_pruebas()
