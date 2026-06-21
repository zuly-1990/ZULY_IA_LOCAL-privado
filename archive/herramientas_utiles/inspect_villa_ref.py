import subprocess, json, tempfile, os, sys

BLEND_REF = '/opt/zuly/planos_temp/Planos y premodelado/Villa Saboye v05 Pre Modelado.blend'
BLENDER   = '/usr/local/bin/blender'

script = '''
import bpy, json

objects = []
for obj in bpy.data.objects:
    objects.append({
        "name": obj.name,
        "type": obj.type,
        "location": [round(v,4) for v in obj.location],
        "scale": [round(v,4) for v in obj.scale],
        "dimensions": [round(v,4) for v in obj.dimensions],
        "collection": obj.users_collection[0].name if obj.users_collection else "Scene",
        "parent": obj.parent.name if obj.parent else None,
    })

meshes_count = len([o for o in objects if o["type"]=="MESH"])
data = {"success": True, "total": len(objects), "meshes": meshes_count, "objects": objects}
print("ZULY_RESULT:" + json.dumps(data))
'''

with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, prefix='/tmp/inspect_') as f:
    f.write(script)
    tmp = f.name

result = subprocess.run(
    [BLENDER, BLEND_REF, '--background', '--python', tmp],
    capture_output=True, text=True, timeout=90
)

for line in result.stdout.splitlines():
    if line.startswith('ZULY_RESULT:'):
        data = json.loads(line[12:])
        print(json.dumps(data, indent=2, ensure_ascii=False))
        break
else:
    print("ERROR - no ZULY_RESULT found")
    print("STDOUT:", result.stdout[-500:])
    print("STDERR:", result.stderr[-300:])

try:
    os.unlink(tmp)
except:
    pass
