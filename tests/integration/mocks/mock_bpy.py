# Mock implementation of the `bpy` module used by ZULY tests.
# This file provides just enough functionality for the state_snapshot module
# to run without a real Blender installation.

class _Collection:
    def __init__(self, name):
        self.name = name

class _Object:
    def __init__(self, name, obj_type="MESH", location=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1), collection_name="Scene Collection", hide_viewport=False):
        self.name = name
        self.type = obj_type
        self.location = location
        self.rotation_euler = rotation
        self.scale = scale
        self.users_collection = [_Collection(collection_name)]
        self.hide_viewport = hide_viewport

class _Data:
    def __init__(self):
        self.objects = []

    def add_object(self, obj):
        self.objects.append(obj)

# The top‑level mock module mimics the structure ``bpy.data.objects``
# that ZULY's ``state_snapshot`` expects.

data = _Data()

# Helper to quickly populate a simple scene for tests.
def populate_scene():
    data.objects.clear()
    # Add a few representative objects.
    data.add_object(_Object(name="Cube", obj_type="MESH", location=(1, 2, 3), rotation=(0.1, 0.2, 0.3), scale=(1, 1, 1)))
    data.add_object(_Object(name="Light", obj_type="LIGHT", location=(5, 5, 5), rotation=(0, 0, 0), scale=(1, 1, 1), collection_name="Lights"))
    data.add_object(_Object(name="Camera", obj_type="CAMERA", location=(0, -10, 5), rotation=(0.5, 0, 0), scale=(1, 1, 1), collection_name="Cameras"))
