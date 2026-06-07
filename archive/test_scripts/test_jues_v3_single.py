#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, 'c:/Users/Admin/Desktop/ZULY_IA_LOCAL/core')
from jues_bot_v3 import jues_bot_v3_validar_y_sellar

resultado = jues_bot_v3_validar_y_sellar(
    './archivo_zuly/temp_arena/MOD-001_Pabellon_Minimalista.blend',
    'MOD-001_Pabellon_Minimalista',
    '#C0C0C0',
    aprobar=True
)

print(f"Puntuacion: {resultado.get('puntuacion', 0)}")
print(f"Dictamen: {resultado.get('dictamen', 'N/A')}")
if resultado.get('sellado'):
    print(f"SELLO: {resultado['sellado'].get('status', 'N/A')}")
else:
    print("Sin sello")
