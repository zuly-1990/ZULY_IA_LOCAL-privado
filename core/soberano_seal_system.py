#!/usr/bin/env python3
"""
👑 SOBERANO SEAL SYSTEM - VISTO BUENO Y ARCHIVADO
Sistema de aprobación final del usuario y sellado de patrones
"""

import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional

class SoberanoSealSystem:
    """
    Sistema de Visto Bueno del Soberano (Usuario).
    
    Responsabilidades:
    1. Recibir dictamen de JUES-BOT
    2. Esperar aprobación/rechazo del usuario
    3. Sellar patrón aprobado (mover a mastered/)
    4. Bitacorar rechazos
    5. Limpiar temporales post-sellado
    """
    
    def __init__(self, base_path: str = "./archivo_zuly"):
        self.base_path = Path(base_path)
        self.arena_path = self.base_path / "temp_arena"
        self.mastered_path = self.base_path / "por_estado_aprendizaje" / "mastered"
        self.bitacora_path = self.base_path / "bitacora"
        
        # Asegurar estructura
        self.arena_path.mkdir(parents=True, exist_ok=True)
        self.mastered_path.mkdir(parents=True, exist_ok=True)
        self.bitacora_path.mkdir(parents=True, exist_ok=True)
    
    def presentar_para_visto_bueno(self, 
                                    candidatos_arena: List[Dict],
                                    ganador_recomendado: Dict,
                                    ranking: List[Dict]) -> str:
        """
        Presenta los 3 candidatos de la arena al Soberano para decisión.
        
        Args:
            candidatos_arena: Lista de 3 candidatos con sus reportes JUES
            ganador_recomendado: El candidato que JUES recomienda
            ranking: Ranking ordenado de los 3 candidatos
        
        Returns:
            str: Resumen de presentación
        """
        
        print("\n" + "="*70)
        print("👑 SOBERANO: FASE DE ARENA - 3 CANDIDATOS")
        print("="*70)
        
        # Mostrar ranking completo
        print("\n📊 RANKING JUES-BOT:")
        print("-"*70)
        for i, candidato in enumerate(ranking, 1):
            sp = candidato.get("superpoderes", {})
            dash = candidato.get("dashboard", {})
            
            medalla = "🥇" if i == 1 else "🥈" if i == 2 else "🥉"
            dictamen = candidato.get("dictamen", "PENDIENTE")
            puntos = candidato.get("puntuacion_jues", 0)
            
            print(f"\n{medalla} #{i} - {candidato.get('candidato_id', 'N/A')}")
            print(f"    Puntuación: {puntos}/100")
            print(f"    Dictamen: {dictamen}")
            print(f"    Malla: {dash.get('estado_malla', 'N/A')} {dash.get('estado_malla_icon', '')}")
            print(f"    Color: {dash.get('concordancia_color', 'N/A')} {dash.get('concordancia_icon', '')}")
            print(f"    Peso: {dash.get('peso_patron_kb', 0)} KB")
            print(f"    Hash: {dash.get('hash_corto', 'N/A')}")
        
        # Destacar recomendación
        print("\n" + "="*70)
        print("🤖 RECOMENDACIÓN JUES-BOT:")
        print("="*70)
        print(f"   Candidato recomendado: {ganador_recomendado.get('candidato_id', 'N/A')}")
        print(f"   Puntuación: {ganador_recomendado.get('puntuacion_jues', 0)}/100")
        print(f"   Errores: {ganador_recomendado.get('errores', 0)}")
        print(f"   Advertencias: {ganador_recomendado.get('advertencias', 0)}")
        
        print("\n" + "="*70)
        print("📝 ACCIONES DISPONIBLES PARA EL SOBERANO:")
        print("="*70)
        print("   [1] SELLO #1 → Sellar ganador recomendado por JUES")
        print("   [2] SELLO #2 → Sellar segundo lugar")
        print("   [3] SELLO #3 → Sellar tercer lugar")
        print("   [R] RECHAZO TODOS → Bitacorar y limpiar arena")
        print("   [N] NUEVA GENERACIÓN → Solicitar 3 nuevos candidatos")
        print("="*70)
        
        return "presentado"
    
    def sellar_patron(self, 
                     candidato: Dict,
                     reporte_jues: Dict,
                     decision_soberano: str = "SELLADO") -> Dict:
        """
        Sella el patrón aprobado y lo archiva permanentemente.
        
        Args:
            candidato: Datos del candidato ganador
            reporte_jues: Reporte de validación
            decision_soberano: "SELLADO", "RECHAZADO", "CORREGIR"
        
        Returns:
            Dict: Resultado del sellado
        """
        
        meta = candidato.get("metadata", {})
        pattern_id = meta.get("id", "UNKNOWN")
        timestamp = datetime.now().isoformat()
        
        resultado = {
            "pattern_id": pattern_id,
            "timestamp": timestamp,
            "decision": decision_soberano,
            "archivado": False,
            "ubicacion": None
        }
        
        if decision_soberano == "SELLADO":
            print(f"\n✅ SOBERANO: SELLANDO {pattern_id} → por_estado_aprendizaje/mastered/")
            
            # 1. Crear directorio en mastered/ con estructura organizada
            pattern_dir = self.mastered_path / pattern_id
            subdirs = {
                "blend": pattern_dir / "blend",
                "script": pattern_dir / "script", 
                "json": pattern_dir / "json",
                "render": pattern_dir / "render",
                "certificado": pattern_dir / "certificado"
            }
            
            for d in subdirs.values():
                d.mkdir(parents=True, exist_ok=True)
            
            # 2. Copiar archivos desde arena a subcarpetas organizadas
            src_blend = self.arena_path / f"{pattern_id}.blend"
            src_script = self.arena_path / f"{pattern_id}.py"
            src_json = self.arena_path / f"{pattern_id}.json"
            
            if src_blend.exists():
                shutil.copy2(src_blend, subdirs["blend"] / f"{pattern_id}.blend")
            if src_script.exists():
                shutil.copy2(src_script, subdirs["script"] / f"{pattern_id}.py")
            if src_json.exists():
                shutil.copy2(src_json, subdirs["json"] / f"{pattern_id}.json")
            
            # 3. Crear certificado de sello
            certificado = {
                "pattern_id": pattern_id,
                "nombre_tecnico": meta.get("nombre_tecnico"),
                "sellado_en": timestamp,
                "dictamen_jues": reporte_jues.get("dictamen"),
                "puntuacion_jues": reporte_jues.get("puntuacion_jues"),
                "hash_inmutabilidad": reporte_jues.get("superpoderes", {}).get("sello_inmutabilidad", {}).get("hash"),
                "decision_soberano": decision_soberano,
                "superpoderes_pass": {
                    "vision_rayos_x": reporte_jues.get("superpoderes", {}).get("vision_rayos_x", {}).get("status") == "LIMPIA",
                    "instinto_optimizacion": reporte_jues.get("superpoderes", {}).get("instinto_optimizacion", {}).get("status") == "OPTIMO",
                    "sincronia_cromatica": reporte_jues.get("superpoderes", {}).get("sincronia_cromatica", {}).get("status") == "MATCH",
                    "sello_inmutabilidad": reporte_jues.get("superpoderes", {}).get("sello_inmutabilidad", {}).get("hash") != "ERROR_NO_MESH"
                },
                "ubicacion_archivo": str(pattern_dir)
            }
            
            with open(subdirs["certificado"] / "CERTIFICADO_SELLO.json", 'w') as f:
                json.dump(certificado, f, indent=2)
            
            # 4. Actualizar REGISTRO_MAESTRO.json
            self._actualizar_registro_maestro(pattern_id, candidato, reporte_jues)
            
            resultado["archivado"] = True
            resultado["ubicacion"] = str(pattern_dir)
            resultado["certificado"] = certificado
            
            print(f"   📦 Archivado en mastered/{pattern_id}/")
            print(f"      ├─ blend/{pattern_id}.blend")
            print(f"      ├─ script/{pattern_id}.py")
            print(f"      ├─ json/{pattern_id}.json")
            print(f"      └─ certificado/CERTIFICADO_SELLO.json")
            print(f"   ✓ Estructura organizada lista para uso")
            
            # 5. Limpiar temporales
            self._limpiar_temporales(pattern_id)
            
        elif decision_soberano == "RECHAZADO":
            print(f"\n❌ SOBERANO: RECHAZANDO {pattern_id}")
            
            # Bitacorar rechazo
            self._bitacorar_rechazo(pattern_id, candidato, reporte_jues)
            
            # Limpiar sin archivar
            self._limpiar_temporales(pattern_id)
            
            resultado["archivado"] = False
            resultado["motivo"] = "Rechazo del Soberano"
            
        elif decision_soberano == "CORREGIR":
            print(f"\n🔧 SOBERANO: SOLICITANDO CORRECCIONES {pattern_id}")
            resultado["archivado"] = False
            resultado["accion"] = "devolver_a_generador"
        
        return resultado
    
    def _actualizar_registro_maestro(self, pattern_id: str, candidato: Dict, reporte_jues: Dict):
        """Actualiza el REGISTRO_MAESTRO.json con el nuevo patrón sellado"""
        
        registro_path = self.base_path / "REGISTRO_MAESTRO.json"
        
        # Cargar registro existente
        if registro_path.exists():
            with open(registro_path, 'r', encoding='utf-8') as f:
                registro = json.load(f)
        else:
            registro = {
                "nombre_registro": "REGISTRO_MAESTRO_ZULY",
                "version": "1.0",
                "patrones": [],
                "hashes_registrados": {}
            }
        
        # Obtener hash de inmutabilidad
        hash_geo = reporte_jues.get("superpoderes", {}).get("sello_inmutabilidad", {}).get("hash", "SIN_HASH")
        
        # Crear entrada
        entrada = {
            "pattern_id": pattern_id,
            "timestamp_sellado": datetime.now().isoformat(),
            "dictamen_jues": reporte_jues.get("dictamen"),
            "puntuacion_jues": reporte_jues.get("puntuacion_jues"),
            "hash_inmutabilidad": hash_geo,
            "vertices_count": reporte_jues.get("superpoderes", {}).get("sello_inmutabilidad", {}).get("vertices_count", 0),
            "estado_malla": reporte_jues.get("superpoderes", {}).get("vision_rayos_x", {}).get("status"),
            "concordancia_color": reporte_jues.get("superpoderes", {}).get("sincronia_cromatica", {}).get("status"),
            "peso_kb": reporte_jues.get("superpoderes", {}).get("instinto_optimizacion", {}).get("peso_kb", 0)
        }
        
        # Agregar al registro
        registro["patrones"].append(entrada)
        registro["hashes_registrados"][pattern_id] = hash_geo
        registro["total_patrones"] = len(registro["patrones"])
        registro["ultima_actualizacion"] = datetime.now().isoformat()
        
        # Guardar
        with open(registro_path, 'w', encoding='utf-8') as f:
            json.dump(registro, f, indent=2, ensure_ascii=False)
        
        print(f"   � REGISTRO_MAESTRO.json actualizado")
        print(f"   🔒 Hash registrado: {hash_geo[:16]}..."
    
    def _bitacorar_rechazo(self, pattern_id: str, candidato: Dict, reporte_jues: Dict):
        """Registra el rechazo en la bitácora"""
        
        timestamp = datetime.now().isoformat()
        
        entrada_bitacora = {
            "timestamp": timestamp,
            "pattern_id": pattern_id,
            "tipo": "RECHAZO_Soberano",
            "metadata": candidato.get("metadata", {}),
            "dictamen_jues": reporte_jues.get("dictamen"),
            "puntuacion_jues": reporte_jues.get("puntuacion"),
            "errores_detectados": reporte_jues.get("errores", []),
            "warnings": reporte_jues.get("warnings", []),
            "motivo_rechazo": "Pendiente de especificación del Soberano"
        }
        
        # Guardar en bitácora
        bitacora_file = self.bitacora_path / f"rechazos_{timestamp[:10]}.jsonl"
        
        with open(bitacora_file, 'a') as f:
            f.write(json.dumps(entrada_bitacora) + '\n')
        
        print(f"   📝 Bitacorado en: {bitacora_file}")
    
    def _limpiar_temporales(self, pattern_id: str):
        """Limpia archivos temporales de la arena"""
        
        archivos_temp = [
            self.arena_path / f"{pattern_id}.blend",
            self.arena_path / f"{pattern_id}.py",
            self.arena_path / f"{pattern_id}.json",
            self.arena_path / f"{pattern_id}_jues_report.json"
        ]
        
        eliminados = 0
        for archivo in archivos_temp:
            if archivo.exists():
                archivo.unlink()
                eliminados += 1
        
        print(f"   🧹 {eliminados} archivos temporales eliminados")
    
    def consultar_patron_sellado(self, pattern_id: str) -> Optional[Dict]:
        """Consulta un patrón ya sellado en mastered/"""
        
        cert_path = self.mastered_path / pattern_id / "certificado" / "CERTIFICADO_SELLO.json"
        
        if cert_path.exists():
            with open(cert_path, 'r') as f:
                return json.load(f)
        
        return None
    
    def listar_patrones_sellados(self) -> list:
        """Lista todos los patrones sellados en mastered/"""
        
        if not self.mastered_path.exists():
            return []
        
        patrones = []
        for item in self.mastered_path.iterdir():
            if item.is_dir():
                cert = item / "certificado" / "CERTIFICADO_SELLO.json"
                if cert.exists():
                    with open(cert, 'r') as f:
                        data = json.load(f)
                        data["ubicacion"] = str(item)
                        patrones.append(data)
        
        return sorted(patrones, key=lambda x: x.get("sellado_en", ""))


def ejemplo_flujo_completo():
    """Ejemplo de flujo completo: JUES-BOT → Soberano → Sello"""
    
    print("\n" + "="*70)
    print("🎭 EJEMPLO DE FLUJO COMPLETO")
    print("="*70)
    
    # Simular datos de candidato y reporte JUES
    candidato_ganador = {
        "metadata": {
            "id": "CUB-001",
            "nombre_tecnico": "CUB-001_Modelado_BiselRealista",
            "nombre_simple": "Cubo con bordes suaves",
            "nivel_complejidad": 1,
            "categoria": "Hard Surface"
        }
    }
    
    reporte_jues = {
        "puntuacion": 95,
        "dictamen": "APTO_PARA_SELLO",
        "validaciones": {
            "manifold": {"status": "PASS"},
            "color": {"status": "PASS"},
            "escala": {"status": "PASS"}
        },
        "errores": [],
        "warnings": []
    }
    
    # 1. Presentar
    sistema = SoberanoSealSystem()
    sistema.presentar_para_visto_bueno(candidato_ganador, reporte_jues)
    
    # 2. Simular decisión del Soberano
    print("\n👤 Soberano decide: 'SELLADO'")
    
    # 3. Sellar
    resultado = sistema.sellar_patron(candidato_ganador, reporte_jues, "SELLADO")
    
    print(f"\n✅ RESULTADO:")
    print(f"   Archivado: {resultado['archivado']}")
    print(f"   Ubicación: {resultado['ubicacion']}")
    
    # 4. Consultar
    print(f"\n📚 Consultando patrón sellado...")
    cert = sistema.consultar_patron_sellado("CUB-001")
    if cert:
        print(f"   Sellado en: {cert.get('sellado_en')}")
        print(f"   Puntuación: {cert.get('puntuacion_jues')}")
    
    print("\n" + "="*70)


if __name__ == "__main__":
    ejemplo_flujo_completo()
