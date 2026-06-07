#!/usr/bin/env python3
"""
🧪 PRUEBAS EXTRA PARA ZULY
Estructura basada en el manual: guardando .blend en ./export/
"""

import os
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

class PruebasExtraZuly:
    def __init__(self):
        self.script_dir = Path(__file__).parent
        self.blender_exe = self.script_dir / "blender/v3/blender-3.6.0-zuly/blender.exe"
        self.export_dir = self.script_dir / "export"
        self.export_dir.mkdir(exist_ok=True)
        self.pruebas_resultados = []
        self.fecha = datetime.now().isoformat()
        
    def generar_script_blender(self, numero_prueba: int) -> str:
        scripts = {
            11: self._prueba_sistema_solar(),
            12: self._prueba_guardar_blend()
        }
        return scripts.get(numero_prueba, "")

    def _prueba_sistema_solar(self) -> str:
        return """
import bpy
import json
from datetime import datetime

results = {
    'prueba_num': 11,
    'nombre': 'Crear Sistema Solar',
    'timestamp': datetime.now().isoformat(),
    'status': 'iniciada'
}

try:
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
    # Sol
    bpy.ops.mesh.primitive_uv_sphere_add(radius=3, location=(0, 0, 0))
    sol = bpy.context.active_object
    sol.name = "Sol"
    
    # Planeta 1
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(8, 0, 0))
    p1 = bpy.context.active_object
    p1.name = "Planeta_1"
    
    # Planeta 2
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1.5, location=(15, 0, 0))
    p2 = bpy.context.active_object
    p2.name = "Planeta_2"
    
    # Luces
    bpy.ops.object.light_add(type='SUN', location=(0, 0, 10))
    
    results['status'] = 'éxito'
    results['detalle'] = {
        'total_planetas': 2,
        'sol_creado': True,
        'luz_creada': True
    }
except Exception as e:
    results['status'] = 'excepción'
    results['error'] = str(e)

import os
resultado_path = os.path.join("C:/Users/Admin/Desktop/ZULY_IA_LOCAL", "prueba_11_resultado.json")
with open(resultado_path, 'w') as f:
    json.dump(results, f, indent=2)
print(json.dumps(results))
"""

    def _prueba_guardar_blend(self) -> str:
        return """
import bpy
import json
import os
from datetime import datetime

results = {
    'prueba_num': 12,
    'nombre': 'Guardar en Export como indica el Manual',
    'timestamp': datetime.now().isoformat(),
    'status': 'iniciada'
}

try:
    # Asegurarnos de usar ruta absoluta a export
    export_path = os.path.abspath(os.path.join(".", "export", "zuly_extra_pruebas.blend"))
    
    # Guardar archivo
    bpy.ops.wm.save_as_mainfile(filepath=export_path)
    
    results['status'] = 'éxito'
    results['detalle'] = {
        'archivo_guardado': export_path,
        'existe': os.path.exists(export_path)
    }
except Exception as e:
    results['status'] = 'excepción'
    results['error'] = str(e)

resultado_path = os.path.join("C:/Users/Admin/Desktop/ZULY_IA_LOCAL", "prueba_12_resultado.json")
with open(resultado_path, 'w') as f:
    json.dump(results, f, indent=2)
print(json.dumps(results))
"""

    def ejecutar_todas_pruebas(self):
        print("\\n" + "=" * 80)
        print("  => EJECUTANDO PRUEBAS EXTRA (ZULY WORKING)")
        print("=" * 80 + "\\n")
        
        for prueba_num in [11, 12]:
            self._ejecutar_prueba(prueba_num)
        
        self._guardar_resultados()

    def _ejecutar_prueba(self, prueba_num: int):
        print(f"\\n-- PRUEBA EXTRA {prueba_num}")
        print(f"   {'-' * 75}")
        
        script = self.generar_script_blender(prueba_num)
        script_path = self.script_dir / f"temp_extra_prueba_{prueba_num}.py"
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script)
            
        cmd = [str(self.blender_exe), "--background", "--python", str(script_path)]
        
        try:
            print("   ->  Ejecutando Blender con Zuly...")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30, cwd=self.script_dir)
            if result.stdout or result.stderr:
                with open(f"blender_out_{prueba_num}.txt", "w", encoding="utf-8") as outf:
                    outf.write(result.stdout)
                with open(f"blender_err_{prueba_num}.txt", "w", encoding="utf-8") as errf:
                    errf.write(result.stderr)
                
            resultado_file = self.script_dir / f"prueba_{prueba_num}_resultado.json"
            if resultado_file.exists():
                with open(resultado_file) as f:
                    resultado = json.load(f)
                
                status = resultado.get('status', 'desconocido')
                if status == 'éxito':
                    print("   [OK] EXITO")
                    for k, v in resultado.get('detalle', {}).items():
                        print(f"      - {k}: {v}")
                else:
                    print(f"   [FAIL] {status}")
                self.pruebas_resultados.append(resultado)
            else:
                print("   [WARN]  Archivo de resultado no creado")
                
        except Exception as e:
            print(f"   [FAIL] EXCEPCION: {e}")
            
        finally:
            if script_path.exists():
                script_path.unlink()

    def _guardar_resultados(self):
        zuly_lab = self.script_dir / "ZULY_LAB"
        zuly_lab.mkdir(exist_ok=True)
        resumen = {
            "fecha": self.fecha,
            "total_pruebas_extra": len(self.pruebas_resultados),
            "resultados": self.pruebas_resultados
        }
        res_file = zuly_lab / "extra_pruebas_resultados.json"
        with open(res_file, "w") as f:
            json.dump(resumen, f, indent=2)
        print(f"\\n[OK] Resumen guardado en {res_file}")

if __name__ == "__main__":
    suite = PruebasExtraZuly()
    suite.ejecutar_todas_pruebas()
