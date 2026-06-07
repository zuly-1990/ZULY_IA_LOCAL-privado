#!/usr/bin/env python3
"""
Validación rápida de WO-002
============================

Script de demostración que valida cada punto del checklist sin complications de cleanup.
"""

import os
import sys
import json
import tempfile
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.cognition.c2_pattern_storage import PatternStorageV2, AuthorSignature

print("="*80)
print("🔬 VALIDACIÓN WO-002 - Firma del Autor en C2")
print("="*80)

# Setup temporal
temp_dir = tempfile.mkdtemp()
test_author_id = "17a08a21-8eef-41b5-ac6b-bbd620a45fa4"

# Crear identidad temporal
identity_file = os.path.join(temp_dir, '.zuly_identity.key')
with open(identity_file, 'w') as f:
    f.write(test_author_id)

# Cambiar a directorio temporal
orig_cwd = os.getcwd()
os.chdir(temp_dir)

try:
    print("\n[1️⃣  ] Validación de firma correcta vs incorrecta")
    print("-" * 80)
    
    # Test 1: Firma válida
    sig_valid = AuthorSignature(
        autor_id=test_author_id,
        autor_aprueba=True,
        autor_nota="Patrón aprobado"
    )
    assert sig_valid.is_valid(), "❌ Firma válida debería pasar"
    print("✅ Firma válida pasa validación")
    
    # Test 2: Firma con nota vacía
    sig_empty_nota = AuthorSignature(
        autor_id=test_author_id,
        autor_aprueba=True,
        autor_nota=""
    )
    assert not sig_empty_nota.is_valid(), "❌ Firma con nota vacía debería fallar"
    print("✅ Firma con nota vacía rechazada")
    
    print("\n[2️⃣  ] Validación de identidad del autor")
    print("-" * 80)
    
    storage = PatternStorageV2(
        db_path=os.path.join(temp_dir, 'test.db'),
        diagnostics_log_path=os.path.join(temp_dir, 'diagnósticos.jsonl')
    )
    
    assert storage.stored_author_id == test_author_id, "❌ Identidad no cargada correctamente"
    print(f"✅ Identidad cargada: {storage.stored_author_id[:8]}...")
    
    print("\n[3️⃣  ] Test: save() sin firma → excepción")
    print("-" * 80)
    
    pattern_sin_firma = {
        "pattern_name": "test1",
        "pattern_type": "primitive",
        "origin": "real_execution",
        "intent": "test",
        "handlers": [],
        "scene_before": {},
        "scene_after": {},
        "validation_v0": "OK",
        "score_c1": 80.0,
        # Falta: autor_id, autor_aprueba, autor_nota
    }
    
    try:
        storage.save(pattern_sin_firma)
        print("❌ Debería haber lanzado excepción")
        sys.exit(1)
    except ValueError as e:
        if "BLOCKED" in str(e) and "autor_id" in str(e):
            print("✅ Excepción correcta: " + str(e)[:60])
        else:
            print(f"❌ Excepción incorrecta: {e}")
            sys.exit(1)
    
    print("\n[4️⃣  ] Test: save() con autor_id incorrecto → SECURITY exception")
    print("-" * 80)
    
    pattern_wrong_id = {
        "pattern_name": "test2",
        "pattern_type": "primitive",
        "origin": "real_execution",
        "intent": "test",
        "handlers": [],
        "scene_before": {},
        "scene_after": {},
        "validation_v0": "OK",
        "score_c1": 80.0,
        "autor_id": "WRONG_ID_FROM_OTHER_MACHINE",
        "autor_aprueba": True,
        "autor_nota": "Valid"
    }
    
    try:
        storage.save(pattern_wrong_id)
        print("❌ Debería haber lanzado SECURITY exception")
        sys.exit(1)
    except ValueError as e:
        if "SECURITY" in str(e) and "coincide" in str(e):
            print("✅ SECURITY exception correcta: " + str(e)[:70])
        else:
            print(f"❌ Excepción incorrecta: {e}")
            sys.exit(1)
    
    print("\n[5️⃣  ] Test: Rechazo del autor → guardado en DISCO, NO en C2")
    print("-" * 80)
    
    pattern_rechazado = {
        "pattern_name": "pattern_rechazado",
        "pattern_type": "primitive",
        "origin": "real_execution",
        "intent": "test",
        "handlers": [],
        "scene_before": {},
        "scene_after": {},
        "validation_v0": "OK",
        "score_c1": 80.0,
        "autor_id": test_author_id,
        "autor_aprueba": False,
        "autor_nota": "Rechazado por baja calidad"
    }
    
    ok, msg = storage.save(pattern_rechazado)
    assert not ok, "❌ Debería retornar False (no guardado)"
    assert "rechazado" in msg.lower(), "❌ Mensaje debe indicar rechazo"
    print(f"✅ Rechazo retorna False: {msg}")
    
    # Verificar que NO está en C2
    retrieved = storage.get_pattern_by_name("pattern_rechazado")
    assert retrieved is None, "❌ Patrón rechazado NO debería estar en C2"
    print("✅ Patrón rechazado NOT en C2")
    
    # Verificar que ESTÁ en diagnósticos
    diag_file = Path(temp_dir) / 'diagnósticos.jsonl'
    assert diag_file.exists(), "❌ Archivo diagnósticos no existe"
    with open(diag_file, 'r') as f:
        event = json.loads(f.read().strip())
        assert event['pattern_name'] == 'pattern_rechazado', "❌ Evento no registrado"
    print("✅ Evento de rechazo guardado en DISCO")
    
    print("\n[6️⃣  ] Test: Patrón aprobado → C2 con score_final y confianza")
    print("-" * 80)
    
    pattern_aprobado = {
        "pattern_name": "pattern_aprobado",
        "pattern_type": "primitive",
        "origin": "real_execution",
        "intent": "Create cube",
        "handlers": ["create_cube"],
        "scene_before": {"objects": 0},
        "scene_after": {"objects": 1},
        "validation_v0": "OK",
        "score_c1": 87.0,
        "autor_id": test_author_id,
        "autor_aprueba": True,
        "autor_nota": "Perfecto, listo para reusar"
    }
    
    ok, msg = storage.save(pattern_aprobado)
    assert ok, f"❌ Debería retornar True: {msg}"
    print(f"✅ Guardado exitosamente: {msg}")
    
    # Verificar que ESTÁ en C2
    retrieved = storage.get_pattern_by_name("pattern_aprobado")
    assert retrieved is not None, "❌ Patrón aprobado debería estar en C2"
    print("✅ Patrón aprobado está en C2")
    
    # Verificar score_final y confianza
    expected_score = min(87.0 * 1.15, 100.0)
    assert retrieved['score_final'] == expected_score, f"❌ score_final incorrecto: {retrieved['score_final']} vs {expected_score}"
    print(f"✅ score_final correcto: 87 * 1.15 = {expected_score}")
    
    assert retrieved['confianza'] == 95, f"❌ confianza incorrecto: {retrieved['confianza']}"
    print(f"✅ confianza correcta: 95 (máxima)")
    
    print("\n[7️⃣  ] Test: score_final capeado en 100")
    print("-" * 80)
    
    pattern_alto_score = {
        "pattern_name": "pattern_alto_score",
        "pattern_type": "primitive",
        "origin": "real_execution",
        "intent": "Test",
        "handlers": [],
        "scene_before": {},
        "scene_after": {},
        "validation_v0": "OK",
        "score_c1": 95.0,  # 95 * 1.15 = 109.25 → debe capar a 100
        "autor_id": test_author_id,
        "autor_aprueba": True,
        "autor_nota": "Excelente"
    }
    
    ok, msg = storage.save(pattern_alto_score)
    retrieved = storage.get_pattern_by_name("pattern_alto_score")
    assert retrieved['score_final'] == 100.0, f"❌ score_final debería estar capeado: {retrieved['score_final']}"
    print(f"✅ score_final capeado en 100.0 (95 * 1.15 = 109.25 → 100.0)")
    
    print("\n[8️⃣  ] Test: Consultas filtradas por confianza")
    print("-" * 80)
    
    patterns = storage.get_patterns_by_confianza(min_confianza=90)
    assert len(patterns) == 2, f"❌ Debería haber 2 patrones con confianza >= 90: {len(patterns)}"
    print(f"✅ Patrones con confianza >= 90: {len(patterns)}")
    for p in patterns:
        print(f"   - {p['pattern_name']}: confianza={p['confianza']}, score={p['score_final']}")
    
    print("\n[9️⃣  ] Test: Estadísticas de decisiones del autor")
    print("-" * 80)
    
    stats = storage.get_author_decisions()
    print(f"✅ Estadísticas:")
    print(f"   Patrones aprobados: {stats['total_patterns_approved']}")
    print(f"   Patrones rechazados: {stats['total_patterns_rejected']}")
    print(f"   Tasa de rechazo: {stats['rejection_rate']:.1%}")
    
    assert stats['total_patterns_approved'] == 2, "❌ Debería haber 2 aprobados"
    assert stats['total_patterns_rejected'] == 1, "❌ Debería haber 1 rechazado"
    
    print("\n[🔟] Verificación: __persist() es privado")
    print("-" * 80)
    
    # __persist debería ser inaccesible directamente
    assert not hasattr(storage, '__persist'), "❌ __persist debería ser privado"
    assert hasattr(storage, f'_PatternStorageV2__persist'), "❌ name mangling no funciona"
    print("✅ __persist() es privado (name mangling funciona)")
    print(f"✅ Métodos públicos disponibles: save(), get_pattern_by_name(), get_patterns_by_confianza(), get_all_patterns(), get_author_decisions()")
    
    print("\n" + "="*80)
    print("✅✅✅ VALIDACIÓN WO-002 COMPLETADA EXITOSAMENTE ✅✅✅")
    print("="*80)
    print("\nRESUMEN:")
    print("  ✓ Firma del autor validada")
    print("  ✓ Identidad del autor verificada contra .zuly_identity.key")
    print("  ✓ save() lanza excepción sin firma")
    print("  ✓ save() lanza SECURITY exception si autor_id no coincide")
    print("  ✓ Rechazo del autor se persiste en DISCO (no en C2)")
    print("  ✓ Patrón aprobado entra a C2 con score_final y confianza correctos")
    print("  ✓ score_final = C1_score * 1.15 (capped en 100)")
    print("  ✓ confianza = 95 (máxima) si autor aprobó")
    print("  ✓ Consultas filtradas por confianza funcionan")
    print("  ✓ Estadísticas de decisiones disponibles")
    print("  ✓ __persist() es privado (name mangling)")
    print("\nWO-002 está LISTO PARA PRODUCCIÓN")
    print("="*80)

except Exception as e:
    print(f"\n❌❌❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

finally:
    os.chdir(orig_cwd)
    # Cleanup
    import shutil
    try:
        shutil.rmtree(temp_dir, ignore_errors=True)
    except:
        pass
