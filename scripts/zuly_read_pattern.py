import json

files = [
    'knowledge_base/patterns/learned/pattern_casarural_v1.json',
    'knowledge_base/patterns/learned/pattern_edificio2_v1.json',
]

for fp in files:
    try:
        data = json.load(open(fp, encoding='utf-8'))
        objs = data['objects']
        print(f"\n=== {fp.split('/')[-1]} ===")
        print(f"Total mallas: {len(objs)}")
        for i, o in enumerate(objs[:12]):
            mods = ', '.join(m['type'] for m in o['modifiers']) or 'ninguno'
            print(f"  [{i}] {o['name']:35s} scale={[round(x,2) for x in o['scale']]}  mods=[{mods}]")
    except Exception as e:
        print(f"Error leyendo {fp}: {e}")
