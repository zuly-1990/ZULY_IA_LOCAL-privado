import os
from pathlib import Path

def setup():
    base = Path("ZULY_PROJECTS/proyecto_prueba_estandar")
    folders = ["blend", "textures", "hdri", "references", "exports"]
    
    for f in folders:
        path = base / f
        path.mkdir(parents=True, exist_ok=True)
        print(f"Created: {path}")
        
    # Create dummy blend
    blend_file = base / "blend" / "proyecto.blend"
    with open(blend_file, "w") as f:
        f.write("DUMMY BLEND CONTENT")
    print(f"Created: {blend_file}")

if __name__ == "__main__":
    setup()
