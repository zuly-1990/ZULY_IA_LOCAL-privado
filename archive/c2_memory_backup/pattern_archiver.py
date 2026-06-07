#!/usr/bin/env python3
"""
ZULY - SISTEMA DE VALIDACIÓN, CLASIFICACIÓN Y ARCHIVO PERMANENTE
Arquitectura completa para gestión de patrones

FLUJO COMPLETO:
1. ZULY genera patrón
2. Validador Técnico revisa .blend (automático)
3. Si pasa → Presenta a usuario
4. Usuario dice "OK" o "ERROR"
5. Si "OK" → Clasificador organiza y archiva PERMANENTEMENTE
"""

import json
import os
import shutil
from datetime import datetime
from pathlib import Path

class ZulyPatternArchiver:
    """
    Sistema de archivo permanente de patrones ZULY.
    NUNCA borra patrones aprobados - son estudio permanente.
    """
    
    def __init__(self, base_path="./archivo_zuly"):
        self.base_path = Path(base_path)
        self._ensure_structure()
    
    def _ensure_structure(self):
        """Crea estructura de archivo permanente"""
        
        # Estructura jerárquica de clasificación
        structure = {
            "por_tipo": {
                "primitivas": ["cubo", "esfera", "cilindro", "cono", "plano", "torus"],
                "modificadores": ["bevel", "array", "boolean", "mirror", "solidify"],
                "materiales": ["metal", "vidrio", "emisivo", "plastico", "madera"],
                "iluminacion": ["3point", "hdri", "ambient", "spot"],
                "transformaciones": ["pivot", "escala", "rotacion", "posicion"],
                "composicion": ["colecciones", "parenting", "constraints"]
            },
            "por_categoria": {
                "hard_surface": [],
                "organico": [],
                "arquitectura": [],
                "producto": [],
                "abstracto": []
            },
            "por_complejidad": {
                "nivel_1_simple": [],      # 1 primitiva, 1 material
                "nivel_2_basico": [],      # 1 primitiva + modificador
                "nivel_3_intermedio": [], # Combinación de 2-3 elementos
                "nivel_4_avanzado": [],    # Composición compleja
                "nivel_5_pro": []          # Sistema completo
            },
            "por_estado_aprendizaje": {
                "mastered": [],            # ZULY lo domina perfectamente
                "practicing": [],          # En entrenamiento
                "experimental": [],        # Nuevo, probando
                "deprecated": []           # Viejo pero guardado por historia
            }
        }
        
        # Crear directorios
        for main_cat, subcats in structure.items():
            main_path = self.base_path / main_cat
            main_path.mkdir(parents=True, exist_ok=True)
            
            for subcat in subcats.keys() if isinstance(subcats, dict) else subcats:
                (main_path / subcat).mkdir(exist_ok=True)
        
        # Registro maestro indestructible
        self.registry_path = self.base_path / "REGISTRO_MAESTRO.json"
        if not self.registry_path.exists():
            self._init_registry()
    
    def _init_registry(self):
        """Inicializa registro maestro con metadatos de sistema"""
        registry = {
            "sistema": "ZULY Pattern Archive",
            "version": "1.0",
            "creado": datetime.now().isoformat(),
            "reglas": [
                "NUNCA borrar patrones aprobados",
                "Cada patrón tiene hash único",
                "Múltiples clasificaciones permitidas",
                "Historial completo de versiones"
            ],
            "patrones": {},
            "estadisticas": {
                "total_aprobados": 0,
                "por_tipo": {},
                "por_categoria": {},
                "por_complejidad": {}
            }
        }
        self._save_registry(registry)
    
    def _save_registry(self, registry):
        """Guarda registro maestro con backup automático"""
        # Backup del anterior si existe
        if self.registry_path.exists():
            backup_path = self.base_path / f"REGISTRO_MAESTRO_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            shutil.copy(self.registry_path, backup_path)
        
        # Guardar nuevo
        with open(self.registry_path, 'w') as f:
            json.dump(registry, f, indent=2)
    
    def clasificar_y_archivar(self, pattern_data, archivos_generados):
        """
        Clasifica y archiva un patrón aprobado permanentemente.
        
        Args:
            pattern_data: Dict con datos del patrón (JSON estructura)
            archivos_generados: Dict con rutas a .blend, render, etc.
        """
        
        pattern_id = pattern_data["id"]
        timestamp = datetime.now().isoformat()
        
        print(f"\n{'='*60}")
        print(f"📦 ARCHIVANDO: {pattern_id}")
        print(f"{'='*60}")
        
        # 1. Calcular hash único del patrón
        import hashlib
        pattern_hash = hashlib.sha256(
            json.dumps(pattern_data, sort_keys=True).encode()
        ).hexdigest()[:16]
        
        print(f"🔐 Hash único: {pattern_hash}")
        
        # 2. Determinar clasificaciones
        clasificaciones = self._determinar_clasificaciones(pattern_data)
        
        print(f"\n🏷️  Clasificaciones detectadas:")
        for cat, vals in clasificaciones.items():
            print(f"   • {cat}: {vals}")
        
        # 3. Copiar archivos a ubicaciones clasificadas
        archivos_archivados = {}
        
        for categoria_principal, subcategorias in clasificaciones.items():
            for subcat in subcategorias:
                dest_dir = self.base_path / "por_tipo" / subcat
                dest_dir.mkdir(parents=True, exist_ok=True)
                
                # Guardar JSON del patrón
                json_dest = dest_dir / f"{pattern_id}_{pattern_hash}.json"
                with open(json_dest, 'w') as f:
                    json.dump(pattern_data, f, indent=2)
                
                archivos_archivados[f"{categoria_principal}/{subcat}"] = str(json_dest)
                
                # Copiar .blend si existe
                if "blend" in archivos_generados:
                    blend_src = Path(archivos_generados["blend"])
                    if blend_src.exists():
                        blend_dest = dest_dir / f"{pattern_id}_{pattern_hash}.blend"
                        shutil.copy2(blend_src, blend_dest)
        
        # 4. Guardar en complejidad
        nivel = self._calcular_nivel_complejidad(pattern_data)
        comp_dir = self.base_path / "por_complejidad" / f"nivel_{nivel}"
        comp_dir.mkdir(parents=True, exist_ok=True)
        
        comp_json = comp_dir / f"{pattern_id}_{pattern_hash}.json"
        with open(comp_json, 'w') as f:
            json.dump(pattern_data, f, indent=2)
        
        print(f"\n📊 Nivel de complejidad: {nivel}")
        
        # 5. Actualizar registro maestro
        registry = self._load_registry()
        
        registry["patrones"][pattern_id] = {
            "hash": pattern_hash,
            "aprobado_en": timestamp,
            "clasificaciones": clasificaciones,
            "nivel_complejidad": nivel,
            "archivos": archivos_archivados,
            "datos": pattern_data
        }
        
        registry["estadisticas"]["total_aprobados"] += 1
        
        # Actualizar contadores por tipo
        for tipo in clasificaciones.get("por_tipo", []):
            registry["estadisticas"]["por_tipo"][tipo] = \
                registry["estadisticas"]["por_tipo"].get(tipo, 0) + 1
        
        self._save_registry(registry)
        
        print(f"\n✅ Patrón {pattern_id} archivado permanentemente")
        print(f"   Ubicaciones: {len(archivos_archivados)}")
        print(f"   Registro maestro actualizado")
        print(f"{'='*60}\n")
        
        return {
            "pattern_id": pattern_id,
            "hash": pattern_hash,
            "clasificaciones": clasificaciones,
            "archivado_en": timestamp
        }
    
    def _determinar_clasificaciones(self, pattern_data):
        """Determina todas las clasificaciones aplicables"""
        
        tags = pattern_data.get("tags", [])
        nombre = pattern_data.get("nombre_tecnico", "").lower()
        descripcion = pattern_data.get("descripcion_tecnica", "").lower()
        
        clasificaciones = {
            "por_tipo": [],
            "por_categoria": [],
            "por_estado_aprendizaje": ["mastered"]  # Por defecto, aprobado = mastered
        }
        
        # Detectar tipo
        tipo_map = {
            "cubo": "primitivas",
            "esfera": "primitivas",
            "cilindro": "primitivas",
            "cono": "primitivas",
            "plano": "primitivas",
            "bevel": "modificadores",
            "array": "modificadores",
            "boolean": "modificadores",
            "mirror": "modificadores",
            "metal": "materiales",
            "vidrio": "materiales",
            "emisivo": "materiales",
            "transform": "transformaciones",
            "pivot": "transformaciones",
            "3point": "iluminacion",
            "hdri": "iluminacion"
        }
        
        for tag in tags:
            tag_lower = tag.lower()
            for key, categoria in tipo_map.items():
                if key in tag_lower:
                    if categoria not in clasificaciones["por_tipo"]:
                        clasificaciones["por_tipo"].append(categoria)
                    break
        
        # Detectar categoría de uso
        uso = pattern_data.get("uso", "").lower()
        if "arquitectura" in uso or "muro" in nombre:
            clasificaciones["por_categoria"].append("arquitectura")
        if "hard" in uso or "surface" in uso:
            clasificaciones["por_categoria"].append("hard_surface")
        if "organico" in uso:
            clasificaciones["por_categoria"].append("organico")
        if "producto" in uso:
            clasificaciones["por_categoria"].append("producto")
        
        # Si no se detectó categoría, usar "hard_surface" por defecto
        if not clasificaciones["por_categoria"]:
            clasificaciones["por_categoria"].append("hard_surface")
        
        return clasificaciones
    
    def _calcular_nivel_complejidad(self, pattern_data):
        """Calcula nivel de complejidad 1-5"""
        
        score = 0
        
        # Por modificadores
        props = pattern_data.get("propiedades", {})
        params = props.get("parametros_editables", {})
        score += len(params) * 0.5
        
        # Por tags
        tags = pattern_data.get("tags", [])
        score += len(tags) * 0.3
        
        # Por descripción técnica
        desc = pattern_data.get("descripcion_tecnica", "")
        if "modificador" in desc:
            score += 1
        if "material" in desc:
            score += 0.5
        if "iluminación" in desc or "iluminacion" in desc:
            score += 0.5
        
        # Determinar nivel
        if score <= 1:
            return "1_simple"
        elif score <= 2:
            return "2_basico"
        elif score <= 3.5:
            return "3_intermedio"
        elif score <= 5:
            return "4_avanzado"
        else:
            return "5_pro"
    
    def _load_registry(self):
        """Carga registro maestro"""
        with open(self.registry_path, 'r') as f:
            return json.load(f)
    
    def consultar_patron(self, pattern_id):
        """Consulta un patrón archivado"""
        registry = self._load_registry()
        return registry["patrones"].get(pattern_id)
    
    def listar_por_clasificacion(self, clasificacion_principal, subcategoria=None):
        """Lista patrones por clasificación"""
        registry = self._load_registry()
        
        resultados = []
        for pid, pdata in registry["patrones"].items():
            clasifs = pdata.get("clasificaciones", {})
            
            if clasificacion_principal in clasifs:
                if subcategoria:
                    if subcategoria in clasifs[clasificacion_principal]:
                        resultados.append(pid)
                else:
                    resultados.append(pid)
        
        return resultados
    
    def generar_reporte(self):
        """Genera reporte completo del archivo"""
        registry = self._load_registry()
        stats = registry["estadisticas"]
        
        reporte = {
            "fecha_reporte": datetime.now().isoformat(),
            "total_patrones": stats["total_aprobados"],
            "distribucion": {
                "por_tipo": stats["por_tipo"],
                "por_categoria": stats["por_categoria"],
                "por_complejidad": stats["por_complejidad"]
            },
            "patrones_recientes": list(registry["patrones"].keys())[-10:]
        }
        
        return reporte


# ============================================================================
# VALIDADOR TÉCNICO
# ============================================================================

class ZulyTechnicalValidator:
    """
    Valida técnicamente un patrón antes de presentarlo al usuario.
    Revisa el .blend generado contra la especificación.
    """
    
    def __init__(self):
        self.checks = []
        self.auto_fixes = []
    
    def validar_blend(self, blend_path, pattern_spec):
        """
        Valida un archivo .blend contra la especificación.
        
        Returns:
            dict: Resultado de validación con status y detalles
        """
        print(f"\n🔍 VALIDANDO TÉCNICAMENTE: {pattern_spec['id']}")
        print(f"   Archivo: {blend_path}")
        
        resultado = {
            "pattern_id": pattern_spec["id"],
            "status": "PENDING",
            "checks": {},
            "errores": [],
            "warnings": [],
            "auto_fixed": []
        }
        
        # Aquí iría la lógica real de validación con bpy
        # Por ahora, estructura de checks:
        
        checks_requeridos = [
            ("objeto_existe", "El objeto con nombre técnico existe en escena"),
            ("escala_aplicada", "Escala es (1,1,1)"),
            ("modificadores", "Tiene los modificadores especificados"),
            ("materiales", "Tiene material asignado"),
            ("nombres_correctos", "Nombres coinciden con especificación"),
            ("sin_duplicados", "No hay objetos duplicados"),
            ("iluminacion", "Iluminación configurada"),
            ("camara", "Cámara posicionada")
        ]
        
        for check_id, descripcion in checks_requeridos:
            # Simulación - en implementación real, abriría el .blend con bpy
            resultado["checks"][check_id] = {
                "descripcion": descripcion,
                "status": "PASS",  # o "FAIL"
                "auto_fixable": check_id in ["escala_aplicada", "sin_duplicados"]
            }
        
        # Determinar status global
        all_pass = all(c["status"] == "PASS" for c in resultado["checks"].values())
        resultado["status"] = "PASS" if all_pass else "FAIL"
        
        print(f"   Status: {resultado['status']}")
        for check_id, data in resultado["checks"].items():
            icon = "✅" if data["status"] == "PASS" else "❌"
            print(f"   {icon} {check_id}")
        
        return resultado


# ============================================================================
# FLUJO COMPLETO DE EJEMPLO
# ============================================================================

def ejemplo_flujo_completo():
    """Ejemplo de cómo funciona el flujo completo"""
    
    print("="*70)
    print("🔄 EJEMPLO DE FLUJO COMPLETO ZULY")
    print("="*70)
    
    # 1. ZULY genera patrón CUB-001
    pattern_cub001 = {
        "id": "CUB-001",
        "nombre_tecnico": "CUB-001_Modelado_BiselRealista",
        "nombre_simple": "Cubo con bordes suaves",
        "descripcion_simple": "Crea un cubo con bordes redondeados.",
        "descripcion_tecnica": "Aplica modificador Bevel con 3 segmentos.",
        "uso": "Arquitectura, hard surface",
        "tags": ["cubo", "modelado", "modificador", "bevel", "hard_surface"],
        "propiedades": {
            "parametros_editables": {
                "bevel_width": "Ancho del bisel",
                "bevel_segments": "Cantidad de segmentos"
            },
            "valores_default": {
                "bevel_width": 0.05,
                "bevel_segments": 3
            }
        },
        "reglas_aplicadas": {
            "reset": True,
            "escala": True,
            "nombres_tecnicos": True,
            "sin_errores": True
        }
    }
    
    archivos = {
        "blend": "./ZULY_PROJECTS/CUB001_Modelado_BiselRealista.blend",
        "render": "./ZULY_PROJECTS/CUB001_render.png",
        "script": "./CUB001_ejecutar.py"
    }
    
    # 2. Validador Técnico revisa
    print("\n📋 PASO 1: Generación completada")
    print("📋 PASO 2: Validación técnica...")
    
    validator = ZulyTechnicalValidator()
    validacion = validator.validar_blend(archivos["blend"], pattern_cub001)
    
    if validacion["status"] == "PASS":
        print("\n✅ PASA validación técnica")
        print("\n📋 PASO 3: Presentando a usuario para aprobación...")
        print("   (Aquí el usuario diría 'OK' o 'ERROR')")
        
        # Simulación: Usuario dice "OK"
        usuario_aprueba = True
        
        if usuario_aprueba:
            print("\n👤 Usuario: 'OK'")
            print("\n📋 PASO 4: Clasificando y archivando...")
            
            # 4. Archivador clasifica y guarda PERMANENTEMENTE
            archiver = ZulyPatternArchiver()
            resultado = archiver.clasificar_y_archivar(pattern_cub001, archivos)
            
            print(f"\n🎉 FLUJO COMPLETADO")
            print(f"   Patrón {resultado['pattern_id']} archivado")
            print(f"   Hash: {resultado['hash']}")
            print(f"   Clasificaciones: {len(resultado['clasificaciones'])}")
        else:
            print("\n👤 Usuario: 'ERROR' → Corregir o descartar")
    else:
        print("\n❌ NO PASA validación técnica")
        print("   Auto-corregir o rechazar")
    
    print("\n" + "="*70)


if __name__ == "__main__":
    ejemplo_flujo_completo()
