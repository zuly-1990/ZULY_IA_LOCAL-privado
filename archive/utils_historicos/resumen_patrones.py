#!/usr/bin/env python3
"""
Resumen de patrones en PENDING
"""

import json

with open('memory/patterns_pending.json', 'r') as f:
    patrones = json.load(f)

# Agrupar por tipo de comando
comandos = {}
for p in patrones:
    cmd = p['intent']['command_name']
    req = p['user_request']
    if cmd not in comandos:
        comandos[cmd] = {'count': 0, 'ejemplos': []}
    comandos[cmd]['count'] += 1
    if len(comandos[cmd]['ejemplos']) < 2:
        comandos[cmd]['ejemplos'].append(req)

print("="*60)
print("PATRONES EN PENDING (23 total):")
print("="*60)

for cmd, info in sorted(comandos.items(), key=lambda x: -x[1]['count']):
    print(f"\n{cmd}")
    print(f"  Cantidad: {info['count']} patrones")
    ejemplos = ', '.join(info['ejemplos'])
    print(f"  Ejemplos: {ejemplos}")

print('\n' + '='*60)
print(f"Resumen:")
print(f"  Comandos diferentes: {len(comandos)}")
print(f"  Total patrones: {len(patrones)}")
print('='*60)
