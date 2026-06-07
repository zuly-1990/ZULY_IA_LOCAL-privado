import os
from pathlib import Path

def setup_assets():
    base = Path("assets_3d")
    dirs = [
        "blends/escenas_base",
        "blends/pruebas",
        "blends/produccion",
        "textures/madera",
        "textures/metal",
        "textures/concreto",
        "textures/misc",
        "hdri/interior",
        "hdri/exterior",
        "models/low_poly",
        "models/mid_poly",
        "models/high_poly",
        "references/imagenes",
        "references/planos"
    ]
    
    for d in dirs:
        p = base / d
        p.mkdir(parents=True, exist_ok=True)
        print(f"Created/Verified: {p}")

    # Temp cache
    (Path("temp/cache_blender")).mkdir(parents=True, exist_ok=True)
    print("Created/Verified: temp/cache_blender")

if __name__ == "__main__":
    setup_assets()
