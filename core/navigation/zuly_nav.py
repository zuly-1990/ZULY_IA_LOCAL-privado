"""
core/navigation/zuly_nav.py
============================
MÓDULO DE NAVEGACIÓN COGNITIVA - ZULY v1.1
==========================================

Propósito:
  Módulo EXCLUSIVO de navegación espacial para Zuly.
  Centraliza TODAS las coordenadas, dimensiones y relaciones
  espaciales registradas históricamente (Ancestral Memory).

Funciones:
  1. NAV_SCAN    — Escaneo profundo de toda la bitácora histórica
  2. NAV_QUERY   — Consulta inteligente de coordenadas por nombre/contexto
  3. NAV_DISPATCH — Despacha contexto espacial completo a agentes (API)
  4. NAV_REGISTER — Registra nuevas coordenadas en tiempo real
  5. NAV_ANCESTRAL — Búsqueda profunda en memoria ancestral Zuly

Activación:  from core.navigation.zuly_nav import ZulyNav
"""

import os
import json
import glob
import sqlite3
import time
import math
from typing import Dict, List, Any, Optional
from datetime import datetime

# ─── Paths del sistema ────────────────────────────────────────
ZULY_ROOT       = os.environ.get("PYTHONPATH", "/opt/zuly").split(":")[0]
NAV_DB_PATH     = os.path.join(ZULY_ROOT, "bitacora", "nav_memory.db")
KNOWLEDGE_BASE  = os.path.join(ZULY_ROOT, "knowledge_base")
BITACORA_PATH   = os.path.join(ZULY_ROOT, "bitacora")
BLEND_REF       = os.path.join(ZULY_ROOT, "planos_temp", "Planos y premodelado", "Villa Saboye v05 Pre Modelado.blend")
BLEND_FINAL     = os.path.join(ZULY_ROOT, "ZULY_VILLA_SAVOYE_FINAL.blend")
PATTERNS_DB     = os.path.join(ZULY_ROOT, "bitacora", "patterns_signed.db")
MEMORY_DB       = os.path.join(ZULY_ROOT, "bitacora", "memory.db")


# ─── ADN Ancestral: coordenadas históricas grabadas en código ─
ANCESTRAL_COORDS = {
    # ── VILLA SAVOYE (Le Corbusier, 1929) ─────────────────────
    "villa_savoye": {
        "proyecto": "Villa Savoye",
        "autor": "Le Corbusier",
        "año": 1929,
        "ubicacion_real": "Poissy, Francia",
        "sistema_coordenadas": "Blender (metros reales)",
        "elementos": {
            "Losa_PlantaBaja":   {"loc": [0, 0, 0],       "dim": [19.6, 21.6, 0.3], "coleccion": "Primer Nivel"},
            "Losa_PrimerNivel":  {"loc": [0, 0, 3.5],     "dim": [19.6, 21.6, 0.3], "coleccion": "Segundo Nivel"},
            "Losa_SegundoNivel": {"loc": [0, 0, 6.7],     "dim": [19.6, 21.6, 0.3], "coleccion": "Tercer Nivel"},
            "Muro_Norte":        {"loc": [0, 10.65, 5.1], "dim": [19.6, 0.3, 3.2]},
            "Muro_Sur":          {"loc": [0, -10.65, 5.1],"dim": [19.6, 0.3, 3.2]},
            "Muro_Este":         {"loc": [9.65, 0, 5.1],  "dim": [0.3, 21.6, 3.2]},
            "Muro_Oeste":        {"loc": [-9.65, 0, 5.1], "dim": [0.3, 21.6, 3.2]},
            "Solarium_Norte":    {"loc": [0, 5.75, 8.2],  "dim": [11.0, 0.3, 2.0]},
            "Solarium_Oeste":    {"loc": [-5.5, 0, 8.2],  "dim": [0.3, 11.5, 2.0]},
            "Solarium_Sur":      {"loc": [0, -5.75, 8.2], "dim": [11.0, 0.3, 2.0]},
            "Terreno":           {"loc": [0, 0, 0],        "dim": [50, 50, 0]},
        },
        "pilotes": {
            "cuadricula": "4x4",
            "paso_x": 4.9,
            "paso_y": 5.4,
            "origen": [-7.35, -8.1],
            "radio": 0.15,
            "altura": 3.5,
            "z_centro": 1.75,
        },
        "ventanas": {
            "tipo": "fenetre_en_longueur",
            "ancho_tramo": 5.5,
            "alto": 1.2,
            "z": 4.9,
            "fachadas": ["Norte", "Sur"],
        },
        "escalera": {
            "tipo": "helicoidal",
            "peldanos_total": 35,
            "h_peldano": 0.194,
            "huella": 0.28,
            "radio": 1.8,
            "giro_por_peldano_deg": 10,
            "centro_n0": [2.5, -2.5],
            "centro_n1": [-2.5, 2.5],
        },
        "fachadas_referencia": {
            "Fachada_principal": {"loc": [12.69, 0.0, 5.75], "dim": [19.6, 9.6, 0.0], "rot": [1.5708, 0, 0]},
            "Fachada_derecha":   {"loc": [19.6, 10.8, 4.8],  "dim": [21.6, 9.6, 0.0], "rot": [-4.7124, 0, 1.5708]},
            "Fachada_izquierda": {"loc": [0.0, 10.8, 4.8],   "dim": [21.6, 9.6, 0.0], "rot": [1.5708, 0, 4.7124]},
            "Fachada_opuesta":   {"loc": [9.07, 21.6, 3.70], "dim": [19.6, 9.6, 0.0]},
        },
        "cortes_seccion": {
            "Corte_01": {"loc": [5.15, 9.88, 0.3],   "dim": [19.6, 9.6, 0.0]},
            "Corte_02": {"loc": [10.79, 11.91, 2.66], "dim": [21.6, 9.6, 0.0]},
            "Corte_03": {"loc": [11.74, 8.81, 4.61],  "dim": [21.6, 9.6, 0.0]},
        },
        "archivo_referencia": "Villa Saboye v05 Pre Modelado.blend",
        "archivo_final": "ZULY_VILLA_SAVOYE_FINAL.blend",
        "sesion_registro": "2026-06-21",
    },

    # ── ADN RURAL (de knowledge_base/adn_rural.json) ──────────
    "adn_rural": {
        "proyecto": "ADN Rural",
        "descripcion": "Patrones de construcción vernacular colombiana",
        "fuente": "knowledge_base/adn_rural.json",
        "tipo": "ancestral",
    },
}


class ZulyNav:
    """
    Módulo de Navegación Cognitiva de Zuly.
    Gestiona el espacio, las coordenadas y la memoria ancestral.
    """

    def __init__(self):
        self._init_db()
        self._load_ancestral()

    # ═══════════════════════════════════════════════════════════
    # INICIALIZACIÓN
    # ═══════════════════════════════════════════════════════════

    def _init_db(self):
        """Inicializa la base de datos de navegación."""
        os.makedirs(os.path.dirname(NAV_DB_PATH), exist_ok=True)
        conn = sqlite3.connect(NAV_DB_PATH)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS nav_coords (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                proyecto    TEXT NOT NULL,
                elemento    TEXT NOT NULL,
                loc_x       REAL, loc_y REAL, loc_z REAL,
                dim_x       REAL, dim_y REAL, dim_z REAL,
                rot_x       REAL, rot_y REAL, rot_z REAL,
                coleccion   TEXT,
                contexto    TEXT,
                fuente      TEXT,
                timestamp   TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS nav_ancestral (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                clave       TEXT UNIQUE,
                tipo        TEXT,
                datos_json  TEXT,
                descripcion TEXT,
                timestamp   TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS nav_dispatch_log (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                agente      TEXT,
                contexto    TEXT,
                payload_json TEXT,
                respuesta   TEXT,
                timestamp   TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()

    def _load_ancestral(self):
        """Carga la memoria ancestral hardcoded al inicio."""
        conn = sqlite3.connect(NAV_DB_PATH)
        for clave, datos in ANCESTRAL_COORDS.items():
            conn.execute("""
                INSERT OR REPLACE INTO nav_ancestral (clave, tipo, datos_json, descripcion)
                VALUES (?, 'ANCESTRAL', ?, ?)
            """, (clave, json.dumps(datos, ensure_ascii=False), datos.get("proyecto", clave)))
        conn.commit()
        conn.close()

    # ═══════════════════════════════════════════════════════════
    # 1. NAV_SCAN — Escaneo profundo histórico
    # ═══════════════════════════════════════════════════════════

    def nav_scan(self, deep: bool = True) -> Dict[str, Any]:
        """
        Escanea TODA la bitácora y archivos JSON del servidor
        buscando coordenadas y datos espaciales registrados.

        Args:
            deep: Si True, escanea subdirectorios recursivamente

        Returns:
            Dict con todos los datos encontrados y count total
        """
        found = []
        scan_paths = [
            BITACORA_PATH,
            KNOWLEDGE_BASE,
            os.path.join(ZULY_ROOT, "ZULY_LAB", "dataset_patrones"),
            os.path.join(ZULY_ROOT, "archivo_zuly"),
        ]

        coord_keys = {"location", "loc", "position", "pos",
                      "dimension", "dim", "dimensions",
                      "rotation", "scale", "coordinates"}

        for base_path in scan_paths:
            if not os.path.exists(base_path):
                continue
            pattern = os.path.join(base_path, "**/*.json") if deep else os.path.join(base_path, "*.json")
            for json_file in glob.glob(pattern, recursive=deep):
                try:
                    with open(json_file, 'r', encoding='utf-8', errors='ignore') as f:
                        data = json.load(f)
                    # Buscar claves espaciales en el JSON
                    hits = self._extract_coords_from_json(data, json_file)
                    if hits:
                        found.extend(hits)
                        # Registrar en la DB
                        self._register_batch(hits, fuente=json_file)
                except Exception:
                    continue

        # También escanear patterns_signed.db
        patterns = self._scan_patterns_db()
        found.extend(patterns)

        return {
            "success": True,
            "total_encontrados": len(found),
            "fuentes_escaneadas": len(scan_paths),
            "elementos": found[:50],  # Primeros 50 para no saturar
            "timestamp": datetime.now().isoformat(),
        }

    def _extract_coords_from_json(self, data: Any, fuente: str) -> List[Dict]:
        """Extrae entradas con coordenadas de un JSON arbitrario."""
        results = []
        if isinstance(data, dict):
            # Si tiene objetos con location/dim
            objects = data.get("objects") or data.get("elements") or data.get("pattern", {}).get("objects", [])
            if isinstance(objects, list):
                for obj in objects:
                    if isinstance(obj, dict) and ("location" in obj or "loc" in obj or "dimensions" in obj):
                        results.append({
                            "proyecto":  os.path.basename(fuente).replace(".json", ""),
                            "elemento":  obj.get("name", "unknown"),
                            "loc":       obj.get("location", obj.get("loc", [0,0,0])),
                            "dim":       obj.get("dimensions", obj.get("dim", [0,0,0])),
                            "rot":       obj.get("rotation", [0,0,0]),
                            "fuente":    fuente,
                        })
        return results

    def _scan_patterns_db(self) -> List[Dict]:
        """Extrae coordenadas de patterns_signed.db."""
        results = []
        if not os.path.exists(PATTERNS_DB):
            return results
        try:
            conn = sqlite3.connect(PATTERNS_DB)
            rows = conn.execute("SELECT * FROM patterns_signed LIMIT 50").fetchall()
            for row in rows:
                results.append({
                    "proyecto": "patterns_signed",
                    "elemento": str(row[0]) if row else "pattern",
                    "fuente": PATTERNS_DB,
                })
            conn.close()
        except Exception:
            pass
        return results

    def _register_batch(self, hits: List[Dict], fuente: str):
        """Registra un lote de coordenadas en la DB."""
        conn = sqlite3.connect(NAV_DB_PATH)
        for h in hits:
            loc = h.get("loc", [0, 0, 0]) or [0, 0, 0]
            dim = h.get("dim", [0, 0, 0]) or [0, 0, 0]
            rot = h.get("rot", [0, 0, 0]) or [0, 0, 0]
            conn.execute("""
                INSERT OR IGNORE INTO nav_coords
                (proyecto, elemento, loc_x, loc_y, loc_z, dim_x, dim_y, dim_z, rot_x, rot_y, rot_z, fuente)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                h.get("proyecto", ""),
                h.get("elemento", ""),
                loc[0] if len(loc) > 0 else 0,
                loc[1] if len(loc) > 1 else 0,
                loc[2] if len(loc) > 2 else 0,
                dim[0] if len(dim) > 0 else 0,
                dim[1] if len(dim) > 1 else 0,
                dim[2] if len(dim) > 2 else 0,
                rot[0] if len(rot) > 0 else 0,
                rot[1] if len(rot) > 1 else 0,
                rot[2] if len(rot) > 2 else 0,
                fuente,
            ))
        conn.commit()
        conn.close()

    # ═══════════════════════════════════════════════════════════
    # 2. NAV_QUERY — Consulta de coordenadas
    # ═══════════════════════════════════════════════════════════

    def nav_query(self, query: str, proyecto: str = None) -> Dict[str, Any]:
        """
        Busca coordenadas por nombre de elemento o proyecto.

        Args:
            query:    Nombre parcial del elemento o proyecto
            proyecto: Filtrar por proyecto específico

        Returns:
            Lista de coincidencias con coordenadas completas
        """
        # Primero buscar en ancestral (memoria hard)
        ancestral_hits = []
        for clave, datos in ANCESTRAL_COORDS.items():
            if query.lower() in clave.lower() or query.lower() in datos.get("proyecto","").lower():
                ancestral_hits.append({"fuente": "ANCESTRAL", "clave": clave, "datos": datos})
            elementos = datos.get("elementos", {})
            for nombre, coords in elementos.items():
                if query.lower() in nombre.lower():
                    ancestral_hits.append({"fuente": "ANCESTRAL", "elemento": nombre, "coords": coords})

        # Luego buscar en DB
        conn = sqlite3.connect(NAV_DB_PATH)
        sql = "SELECT * FROM nav_coords WHERE elemento LIKE ?"
        params = [f"%{query}%"]
        if proyecto:
            sql += " AND proyecto LIKE ?"
            params.append(f"%{proyecto}%")
        rows = conn.execute(sql, params).fetchall()
        conn.close()

        db_hits = [
            {
                "proyecto": r[1], "elemento": r[2],
                "loc": [r[3], r[4], r[5]],
                "dim": [r[6], r[7], r[8]],
                "rot": [r[9], r[10], r[11]],
                "fuente": r[13],
            }
            for r in rows
        ]

        return {
            "success": True,
            "query": query,
            "ancestral": ancestral_hits,
            "db_results": db_hits,
            "total": len(ancestral_hits) + len(db_hits),
        }

    # ═══════════════════════════════════════════════════════════
    # 3. NAV_REGISTER — Registrar coordenadas nuevas
    # ═══════════════════════════════════════════════════════════

    def nav_register(self, proyecto: str, elemento: str,
                     loc: List[float], dim: List[float] = None,
                     rot: List[float] = None, coleccion: str = None,
                     contexto: str = None) -> Dict[str, Any]:
        """
        Registra coordenadas nuevas en la memoria de navegación.

        Returns:
            Confirmación del registro
        """
        dim = dim or [0, 0, 0]
        rot = rot or [0, 0, 0]

        conn = sqlite3.connect(NAV_DB_PATH)
        conn.execute("""
            INSERT INTO nav_coords
            (proyecto, elemento, loc_x, loc_y, loc_z, dim_x, dim_y, dim_z,
             rot_x, rot_y, rot_z, coleccion, contexto)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            proyecto, elemento,
            loc[0], loc[1], loc[2],
            dim[0], dim[1], dim[2],
            rot[0], rot[1], rot[2],
            coleccion, contexto,
        ))
        conn.commit()
        conn.close()

        return {
            "success": True,
            "registrado": elemento,
            "proyecto": proyecto,
            "loc": loc,
            "dim": dim,
        }

    # ═══════════════════════════════════════════════════════════
    # 4. NAV_DISPATCH — Despachar a agentes vía API
    # ═══════════════════════════════════════════════════════════

    def nav_dispatch(self,
                     agente: str,
                     contexto: str = "villa_savoye",
                     api_key: str = None,
                     modo: str = "completo") -> Dict[str, Any]:
        """
        Despacha el contexto espacial completo a un agente IA externo.

        Args:
            agente:   "deepseek" | "gemini" | "groq" | "openrouter"
            contexto: Proyecto a enviar (default: villa_savoye)
            api_key:  Clave de API del agente
            modo:     "completo" | "resumen" | "ancestral"

        Returns:
            Respuesta del agente con análisis espacial
        """
        # Construir payload espacial
        payload = self._build_spatial_payload(contexto, modo)

        prompt = self._build_nav_prompt(payload, contexto)

        # Despachar al agente seleccionado
        respuesta = None
        if agente == "deepseek":
            respuesta = self._dispatch_deepseek(prompt, api_key)
        elif agente == "gemini":
            respuesta = self._dispatch_gemini(prompt, api_key)
        elif agente == "groq":
            respuesta = self._dispatch_groq(prompt, api_key)
        else:
            respuesta = {"error": f"Agente '{agente}' no soportado. Usa: deepseek, gemini, groq"}

        # Guardar en log
        conn = sqlite3.connect(NAV_DB_PATH)
        conn.execute("""
            INSERT INTO nav_dispatch_log (agente, contexto, payload_json, respuesta)
            VALUES (?,?,?,?)
        """, (agente, contexto, json.dumps(payload, ensure_ascii=False),
              json.dumps(respuesta, ensure_ascii=False)))
        conn.commit()
        conn.close()

        return {
            "success": True,
            "agente": agente,
            "contexto": contexto,
            "elementos_enviados": len(payload.get("elementos", {})),
            "respuesta": respuesta,
        }

    def _build_spatial_payload(self, contexto: str, modo: str) -> Dict[str, Any]:
        """Construye el payload espacial completo para el agente."""
        base = ANCESTRAL_COORDS.get(contexto, {})

        if modo == "resumen":
            return {
                "proyecto": base.get("proyecto"),
                "año": base.get("año"),
                "total_elementos": len(base.get("elementos", {})),
                "niveles": ["Planta Baja", "Primer Nivel", "Segundo Nivel"],
                "footprint": "19.6m x 21.6m",
            }
        elif modo == "ancestral":
            return {
                "tipo": "ANCESTRAL",
                "todos_los_proyectos": list(ANCESTRAL_COORDS.keys()),
                "villa_savoye": base,
            }
        else:  # completo
            return {
                **base,
                "contexto_adicional": {
                    "archivo_referencia": BLEND_REF,
                    "archivo_final": BLEND_FINAL,
                    "nav_db": NAV_DB_PATH,
                    "timestamp_consulta": datetime.now().isoformat(),
                },
            }

    def _build_nav_prompt(self, payload: Dict, contexto: str) -> str:
        """Construye el prompt de navegación para el agente IA."""
        return f"""Eres el Agente de Navegación Espacial de Zuly.

Recibes el contexto espacial COMPLETO del proyecto '{contexto}'.
Tu tarea es:
1. Analizar todas las coordenadas y dimensiones
2. Identificar inconsistencias geométricas
3. Sugerir mejoras estructurales si las hay
4. Calcular el centro de masa del edificio
5. Verificar que la escalera helicoidal cumple la norma (h=0.19m, huella=0.28m)

DATOS ESPACIALES:
{json.dumps(payload, indent=2, ensure_ascii=False)}

Responde en JSON con este formato:
{{
  "analisis": "...",
  "inconsistencias": [],
  "centro_masa": [x, y, z],
  "escalera_ok": true/false,
  "sugerencias": [],
  "score_precision": 0-100
}}"""

    def _dispatch_deepseek(self, prompt: str, api_key: str = None) -> Dict:
        """Envía el prompt a DeepSeek."""
        try:
            import requests
            key = api_key or os.environ.get("DEEPSEEK_API_KEY", "")
            if not key:
                return {"error": "No hay API key de DeepSeek"}
            resp = requests.post(
                "https://api.deepseek.com/chat/completions",
                headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
                json={"model": "deepseek-chat", "messages": [{"role": "user", "content": prompt}],
                      "temperature": 0.1, "max_tokens": 1500},
                timeout=60
            )
            data = resp.json()
            content = data["choices"][0]["message"]["content"]
            try:
                return json.loads(content)
            except:
                return {"raw": content}
        except Exception as e:
            return {"error": str(e)}

    def _dispatch_gemini(self, prompt: str, api_key: str = None) -> Dict:
        """Envía el prompt a Gemini."""
        try:
            import google.genai as genai
            key = api_key or os.environ.get("GEMINI_API_KEY", "")
            if not key:
                return {"error": "No hay API key de Gemini"}
            client = genai.Client(api_key=key)
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )
            raw = response.text
            try:
                start = raw.find('{')
                end = raw.rfind('}') + 1
                return json.loads(raw[start:end])
            except:
                return {"raw": raw}
        except Exception as e:
            return {"error": str(e)}

    def _dispatch_groq(self, prompt: str, api_key: str = None) -> Dict:
        """Envía el prompt a Groq (ultra rápido)."""
        try:
            from groq import Groq
            key = api_key or os.environ.get("GROQ_API_KEY", "")
            if not key:
                return {"error": "No hay API key de Groq"}
            client = Groq(api_key=key)
            resp = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.1-8b-instant",
                temperature=0.1,
                max_tokens=1500,
            )
            raw = resp.choices[0].message.content
            try:
                start = raw.find('{')
                end = raw.rfind('}') + 1
                return json.loads(raw[start:end])
            except:
                return {"raw": raw}
        except Exception as e:
            return {"error": str(e)}

    # ═══════════════════════════════════════════════════════════
    # 5. NAV_ANCESTRAL — Búsqueda profunda ancestral
    # ═══════════════════════════════════════════════════════════

    def nav_ancestral(self, query: str = None) -> Dict[str, Any]:
        """
        Búsqueda profunda en toda la memoria ancestral de Zuly.
        Incluye: knowledge_base, patrones C2/C3, sesiones históricas,
                 modelos V8/V9, datasets de YouTube, bitácora completa.

        Args:
            query: Búsqueda opcional por clave (None = todo)

        Returns:
            Mapa completo de la memoria ancestral
        """
        resultado = {
            "tipo": "BUSQUEDA_ANCESTRAL",
            "timestamp": datetime.now().isoformat(),
            "memorias": {},
        }

        # ── 1. Memoria hardcoded (prioridad máxima) ────────────
        resultado["memorias"]["ancestral_hardcoded"] = {
            "proyectos": list(ANCESTRAL_COORDS.keys()),
            "datos": ANCESTRAL_COORDS if not query else {
                k: v for k, v in ANCESTRAL_COORDS.items()
                if query.lower() in k.lower() or query.lower() in str(v).lower()
            }
        }

        # ── 2. Knowledge base (adn_*.json) ────────────────────
        kb_files = glob.glob(os.path.join(KNOWLEDGE_BASE, "*.json"))
        kb_data = {}
        for f in kb_files:
            try:
                with open(f, 'r', encoding='utf-8', errors='ignore') as fp:
                    data = json.load(fp)
                key = os.path.basename(f).replace(".json", "")
                if not query or query.lower() in key.lower() or query.lower() in str(data).lower()[:500]:
                    kb_data[key] = data
            except:
                pass
        resultado["memorias"]["knowledge_base"] = kb_data

        # ── 3. Patrones C2 (patterns_signed.db) ──────────────
        try:
            conn = sqlite3.connect(PATTERNS_DB)
            tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
            patrones = {}
            for (table,) in tables:
                try:
                    rows = conn.execute(f"SELECT * FROM {table} LIMIT 20").fetchall()
                    patrones[table] = [str(r) for r in rows[:5]]
                except:
                    pass
            conn.close()
            resultado["memorias"]["patterns_c2"] = {"tablas": list(patrones.keys()), "muestra": patrones}
        except Exception as e:
            resultado["memorias"]["patterns_c2"] = {"error": str(e)}

        # ── 4. Modelos V8/V9 registrados ──────────────────────
        v_models = []
        for pattern in ["resultados_masivos_v*"]:
            for d in glob.glob(os.path.join(ZULY_ROOT, pattern)):
                for f in glob.glob(os.path.join(d, "*.blend")):
                    v_models.append(f.replace(ZULY_ROOT, ""))
        resultado["memorias"]["modelos_historicos"] = v_models

        # ── 5. Sesiones de bitácora ────────────────────────────
        sesiones = [
            f.replace(ZULY_ROOT, "")
            for f in glob.glob(os.path.join(BITACORA_PATH, "SESION_*.md"))
        ]
        resultado["memorias"]["sesiones_historicas"] = {
            "total": len(sesiones),
            "lista": sesiones[-10:],  # Últimas 10
        }

        # ── 6. Nav DB (coordenadas registradas en tiempo real) ─
        try:
            conn = sqlite3.connect(NAV_DB_PATH)
            count = conn.execute("SELECT COUNT(*) FROM nav_coords").fetchone()[0]
            proyectos = conn.execute("SELECT DISTINCT proyecto FROM nav_coords").fetchall()
            conn.close()
            resultado["memorias"]["nav_db"] = {
                "total_coordenadas": count,
                "proyectos": [r[0] for r in proyectos],
            }
        except:
            resultado["memorias"]["nav_db"] = {"total_coordenadas": 0}

        total = sum(
            len(v) if isinstance(v, (list, dict)) else 1
            for v in resultado["memorias"].values()
        )
        resultado["total_memorias_encontradas"] = total
        resultado["resumen"] = (
            f"Ancestral: {len(ANCESTRAL_COORDS)} proyectos | "
            f"KB: {len(kb_data)} archivos | "
            f"Modelos: {len(v_models)} .blend | "
            f"Sesiones: {len(sesiones)}"
        )

        return resultado

    # ═══════════════════════════════════════════════════════════
    # ESTADO Y REPORTE
    # ═══════════════════════════════════════════════════════════

    def status(self) -> Dict[str, Any]:
        """Retorna el estado del módulo de navegación."""
        try:
            conn = sqlite3.connect(NAV_DB_PATH)
            coords_total = conn.execute("SELECT COUNT(*) FROM nav_coords").fetchone()[0]
            ancestral_total = conn.execute("SELECT COUNT(*) FROM nav_ancestral").fetchone()[0]
            dispatch_total = conn.execute("SELECT COUNT(*) FROM nav_dispatch_log").fetchone()[0]
            conn.close()
        except:
            coords_total = ancestral_total = dispatch_total = 0

        return {
            "modulo": "ZulyNav v1.0",
            "estado": "ACTIVO",
            "db_path": NAV_DB_PATH,
            "coords_registradas": coords_total,
            "memorias_ancestrales": ancestral_total,
            "dispatches_realizados": dispatch_total,
            "proyectos_ancestrales": list(ANCESTRAL_COORDS.keys()),
        }
