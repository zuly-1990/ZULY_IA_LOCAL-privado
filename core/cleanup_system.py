#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧹 ZULY CLEANUP SYSTEM - Borrado Inteligente 24h
Automatiza la limpieza de archivos temporales en temp_arena/
"""

import os
import json
import shutil
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict

class ZulyCleanupSystem:
    """
    Sistema de limpieza inteligente para archivos temporales.
    
    Reglas:
    - Archivos en temp_arena/ con >24h de antigüedad: ELIMINAR
    - Archivos .blend en temp_arena/ aprobados: MOVER a mastered/
    - Resultados JUES con >48h: ARCHIVAR en bitacora/
    """
    
    def __init__(self, base_path: str = "./archivo_zuly"):
        self.base_path = Path(base_path)
        self.arena_path = self.base_path / "temp_arena"
        self.bitacora_path = self.base_path / "bitacora"
        self.limite_horas = 24
        
    def limpiar_temp_arena(self, dry_run: bool = False) -> Dict:
        """
        Limpia archivos temporales antiguos de temp_arena/
        
        Args:
            dry_run: Si True, solo muestra lo que haría sin eliminar
            
        Returns:
            Dict con estadísticas de limpieza
        """
        resultado = {
            "timestamp": datetime.now().isoformat(),
            "dry_run": dry_run,
            "eliminados": [],
            "archivados": [],
            "conservados": [],
            "errores": []
        }
        
        if not self.arena_path.exists():
            resultado["errores"].append("temp_arena/ no existe")
            return resultado
            
        ahora = datetime.now()
        limite = timedelta(hours=self.limite_horas)
        
        print(f"\n🧹 ZULY CLEANUP - Analizando {self.arena_path}")
        print(f"   Límite: {self.limite_horas} horas")
        print(f"   Modo dry-run: {dry_run}")
        print("="*60)
        
        for archivo in self.arena_path.iterdir():
            if archivo.is_file():
                stat = archivo.stat()
                mtime = datetime.fromtimestamp(stat.st_mtime)
                edad = ahora - mtime
                
                info = {
                    "archivo": archivo.name,
                    "tamano_kb": round(stat.st_size / 1024, 2),
                    "modificado": mtime.isoformat(),
                    "edad_horas": round(edad.total_seconds() / 3600, 1)
                }
                
                # Decidir acción
                if edad > limite:
                    # Archivo viejo - eliminar o archivar
                    if archivo.suffix == '.json' and 'RESULTADO' in archivo.name:
                        # Archivar resultados JUES en bitácora
                        destino = self.bitacora_path / f"{archivo.stem}_{mtime.strftime('%Y%m%d')}.json"
                        if not dry_run:
                            self.bitacora_path.mkdir(parents=True, exist_ok=True)
                            shutil.move(str(archivo), str(destino))
                        resultado["archivados"].append({**info, "destino": str(destino)})
                        accion = "ARCHIVADO → bitacora/"
                        
                    elif archivo.suffix in ['.blend', '.py', '.json']:
                        # Archivo temporal viejo - eliminar
                        if not dry_run:
                            archivo.unlink()
                        resultado["eliminados"].append(info)
                        accion = "ELIMINADO (>24h)"
                    else:
                        resultado["conservados"].append({**info, "razon": "tipo_desconocido"})
                        accion = "CONSERVADO (tipo no reconocido)"
                else:
                    # Archivo reciente - conservar
                    resultado["conservados"].append(info)
                    accion = "CONSERVADO (<24h)"
                
                print(f"   {archivo.name[:40]:40} | {info['edad_horas']:>6.1f}h | {accion}")
        
        # Guardar log
        log_path = self.bitacora_path / f"cleanup_log_{ahora.strftime('%Y%m%d_%H%M%S')}.json"
        if not dry_run:
            self.bitacora_path.mkdir(parents=True, exist_ok=True)
            with open(log_path, 'w') as f:
                json.dump(resultado, f, indent=2)
        
        print("="*60)
        print(f"📊 RESUMEN:")
        print(f"   Eliminados: {len(resultado['eliminados'])}")
        print(f"   Archivados: {len(resultado['archivados'])}")
        print(f"   Conservados: {len(resultado['conservados'])}")
        print(f"   Errores: {len(resultado['errores'])}")
        if not dry_run:
            print(f"   Log guardado: {log_path}")
        
        return resultado
    
    def programar_limpieza_automatica(self):
        """
        Configura limpieza automática (para integrar con scheduler)
        """
        return {
            "frecuencia": "cada_24h",
            "hora_ejecucion": "03:00",
            "accion": "self.limpiar_temp_arena()",
            "path": str(self.arena_path)
        }

def ejecutar_limpieza(dry_run: bool = True):
    """Función de conveniencia para ejecutar limpieza"""
    cleaner = ZulyCleanupSystem()
    return cleaner.limpiar_temp_arena(dry_run=dry_run)

if __name__ == "__main__":
    import sys
    
    # Si se pasa --exec, ejecuta realmente. Si no, modo dry-run.
    dry_run = "--exec" not in sys.argv
    
    if dry_run:
        print("\n⚠️  MODO SIMULACIÓN (dry-run)")
        print("   Usa --exec para ejecutar limpieza real\n")
    
    resultado = ejecutar_limpieza(dry_run=dry_run)
