#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎮 CONTROLADOR ZULY-JUES - Sistema Automático de Sellado
Un comando del Soberano = Validación + Sellado + Archivado
"""

import subprocess
import sys
import json
from pathlib import Path
from datetime import datetime

# RUTAS
ZULY_BASE = Path("c:/Users/Admin/Desktop/ZULY_IA_LOCAL")
CORE = ZULY_BASE / "core"
TEMP_ARENA = ZULY_BASE / "archivo_zuly" / "temp_arena"

sys.path.insert(0, str(CORE))


class ControladorZulyJues:
    """
    Controlador maestro que coordina ZULY y JUES
    Cuando el Soberano dice "OK", todo fluye automáticamente
    """
    
    def __init__(self):
        self.zuly_base = ZULY_BASE
        self.temp_arena = TEMP_ARENA
        self.resultado = {}
        
    def procesar_orden_soberano(self, blend_file: str, candidato_id: str, target_color: str, orden: str) -> dict:
        """
        Procesa la orden del Soberano
        
        Args:
            blend_file: Nombre del archivo .blend (sin ruta)
            candidato_id: ID del patrón (ej: "CUB-001")
            target_color: Color objetivo (ej: "#1A4DCC")
            orden: "OK", "S", "SELLAR", "APROBAR" → Sella automáticamente
                   "R", "RECHAZAR" → Rechaza
                   "C", "CORREGIR" → Pide corrección
        
        Returns:
            dict con resultado completo
        """
        blend_path = self.temp_arena / blend_file
        
        print("="*70)
        print("🎮 CONTROLADOR ZULY-JUES - Procesando Orden del Soberano")
        print("="*70)
        print(f"📦 Patrón: {candidato_id}")
        print(f"🎨 Color objetivo: {target_color}")
        print(f"🏛️ Orden recibida: {orden.upper()}")
        print("="*70)
        
        # Interpretar orden
        orden = orden.upper().strip()
        aprobar = orden in ["OK", "S", "SI", "SELLAR", "APROBAR", "SELO", "GO"]
        rechazar = orden in ["R", "NO", "RECHAZAR", "N", "MAL"]
        corregir = orden in ["C", "CORREGIR", "ARREGLAR", "FIX"]
        
        if aprobar:
            print("\n✅ SOBERANO APRUEBA - Ejecutando sellado automático")
            return self._ejecutar_sellado(blend_path, candidato_id, target_color)
        elif rechazar:
            print("\n❌ SOBERANO RECHAZA - Archivando en bitácora")
            return self._ejecutar_rechazo(blend_path, candidato_id)
        elif corregir:
            print("\n🔄 SOLICITANDO CORRECCIÓN - Devolviendo a ZULY")
            return {"status": "CORRECCION_SOLICITADA", "candidato": candidato_id}
        else:
            print(f"\n❓ ORDEN NO RECONOCIDA: {orden}")
            return {"status": "ORDEN_INVALIDA", "orden_recibida": orden}
    
    def _ejecutar_sellado(self, blend_path: Path, candidato_id: str, target_color: str) -> dict:
        """Ejecuta validación + sellado automático"""
        
        # Llamar a JUES-BOT V2 para validar y sellar
        blender_exe = self.zuly_base / "blender" / "v3" / "blender-3.6.0-zuly" / "blender.exe"
        
        script_ejecucion = f'''
import sys
sys.path.insert(0, '{CORE}')
from jues_bot_v2 import jues_bot_validar_y_sellar, ProtocoloZei

resultado = jues_bot_validar_y_sellar(
    "{blend_path}",
    "{candidato_id}",
    "{target_color}",
    aprobar=True
)

# Imprimir resultado parseable
print(f"DICTAMEN: {{resultado['dictamen']}}")
print(f"ERRORES: {{resultado.get('errores', 0)}}")
print(f"ADVERTENCIAS: {{resultado.get('advertencias', 0)}}")
if resultado.get('sellado'):
    print(f"SELLO_STATUS: {{resultado['sellado']['status']}}")
    print(f"UBICACION: {{resultado['sellado']['ubicacion']}}")
'''
        
        # Guardar script temporal
        temp_script = self.temp_arena / "temp_controlador_jues.py"
        with open(temp_script, 'w', encoding='utf-8') as f:
            f.write(script_ejecucion)
        
        print(f"\n🔍 PASO 1: JUES-BOT validando {candidato_id}...")
        
        # Ejecutar en Blender
        result = subprocess.run(
            [str(blender_exe), '--background', '--python', str(temp_script)],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore',
            cwd=str(self.zuly_base)
        )
        
        output = result.stdout if result.stdout else ""
        
        # Parsear resultado
        dictamen = "DESCONOCIDO"
        errores = 0
        advertencias = 0
        sello_status = "NO_APLICADO"
        ubicacion = "N/A"
        
        for line in output.split('\n'):
            if line.startswith("DICTAMEN:"):
                dictamen = line.replace("DICTAMEN:", "").strip()
            elif line.startswith("ERRORES:"):
                errores = int(line.replace("ERRORES:", "").strip())
            elif line.startswith("ADVERTENCIAS:"):
                advertencias = int(line.replace("ADVERTENCIAS:", "").strip())
            elif line.startswith("SELLO_STATUS:"):
                sello_status = line.replace("SELLO_STATUS:", "").strip()
            elif line.startswith("UBICACION:"):
                ubicacion = line.replace("UBICACION:", "").strip()
        
        temp_script.unlink()
        
        # Resultado final
        self.resultado = {
            "candidato_id": candidato_id,
            "timestamp": datetime.now().isoformat(),
            "orden": "SELLAR",
            "dictamen": dictamen,
            "errores": errores,
            "advertencias": advertencias,
            "sello": sello_status,
            "ubicacion": ubicacion,
            "output_completo": output[-1500:] if len(output) > 1500 else output
        }
        
        # Imprimir resumen
        print(f"\n{'='*70}")
        print("📊 RESULTADO FINAL - SELLO AUTOMÁTICO")
        print(f"{'='*70}")
        print(f"🎯 Patrón: {candidato_id}")
        print(f"🏛️ Dictamen: {dictamen}")
        print(f"⚠️  Errores: {errores} | Advertencias: {advertencias}")
        print(f"🏆 Sello: {sello_status}")
        print(f"📁 Ubicación: {ubicacion}")
        print(f"{'='*70}")
        
        return self.resultado
    
    def _ejecutar_rechazo(self, blend_path: Path, candidato_id: str) -> dict:
        """Archiva el patrón rechazado en bitácora"""
        
        bitacora_path = self.zuly_base / "archivo_zuly" / "bitacora"
        bitacora_path.mkdir(exist_ok=True)
        
        # Mover a bitácora
        import shutil
        rechazo_path = bitacora_path / f"{candidato_id}_RECHAZADO_{datetime.now().strftime('%Y%m%d_%H%M%S')}.blend"
        
        if blend_path.exists():
            shutil.move(str(blend_path), str(rechazo_path))
        
        resultado = {
            "candidato_id": candidato_id,
            "timestamp": datetime.now().isoformat(),
            "orden": "RECHAZAR",
            "status": "RECHAZADO",
            "ubicacion": str(rechazo_path)
        }
        
        print(f"\n📦 Patrón rechazado movido a: {rechazo_path}")
        
        return resultado


def main():
    """
    Uso desde línea de comandos:
    python controlador_zuly_jues.py <blend> <id> <color> <orden>
    
    Ejemplos:
    python controlador_zuly_jues.py CUB-001.blend CUB-001 #1A4DCC OK
    python controlador_zuly_jues.py CUB-001.blend CUB-001 #1A4DCC S
    python controlador_zuly_jues.py CUB-001.blend CUB-001 #1A4DCC R
    """
    if len(sys.argv) >= 5:
        blend_file = sys.argv[1]
        candidato_id = sys.argv[2]
        target_color = sys.argv[3]
        orden = sys.argv[4]
        
        ctrl = ControladorZulyJues()
        resultado = ctrl.procesar_orden_soberano(blend_file, candidato_id, target_color, orden)
        
        # Guardar resultado
        result_path = ZULY_BASE / "ultima_orden_resultado.json"
        with open(result_path, 'w', encoding='utf-8') as f:
            json.dump(resultado, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Resultado guardado en: {result_path}")
        
    else:
        print("="*70)
        print("🎮 CONTROLADOR ZULY-JUES - Ayuda")
        print("="*70)
        print("\nUso:")
        print("  python controlador_zuly_jues.py <blend> <id> <color> <orden>")
        print("\nOrdenes válidas:")
        print("  OK, S, SI, SELLAR, APROBAR → Sella automáticamente")
        print("  R, NO, RECHAZAR, N, MAL   → Rechaza el patrón")
        print("  C, CORREGIR, ARREGLAR     → Solicita corrección")
        print("\nEjemplo (Sellar CUB-001):")
        print("  python controlador_zuly_jues.py CUB-001.blend CUB-001 #1A4DCC OK")
        print("="*70)


if __name__ == "__main__":
    main()
