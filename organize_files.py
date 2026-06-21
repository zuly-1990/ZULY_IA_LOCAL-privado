import os
import shutil
import glob

# Rutas de carpetas nuevas
DIRS = {
    "scripts_descarga": [
        "download_*.js", "download_*.py", "extract_*.js", "extract_*.py", 
        "upload_*.js", "upload_*.ps1", "upload_all.ps1"
    ],
    "experimentos_zuly": [
        "zuly_iter*.py", "zuly_auto*.py", "zuly_qa_v9*.py", "zuly_strict*.py",
        "generado_bogota.py", "run_autonomous_bogota.py", "run_remote_test_zuly.py", "run_test_massive.py",
        "train_massive_c3.py", "train_zuly_from_youtube.py", "test_*.py", "test_safe.txt"
    ],
    "herramientas_utiles": [
        "check_*.py", "inspect_*.py", "find_*.py", "debug_*.py", "fix_*.py", "search_*.py"
    ],
    "scripts_remotos": [
        "audit_remote.py", "compile_blend*.py", "compare_blends.py", "deploy_to_remote.py",
        "kill_v8_remote.py", "launch_v8_remote.py", "launch_v9_remote.py", "remote_*.py"
    ],
    "scripts_varios": [
        "*.ps1", "*.bat" # Los que queden sueltos
    ]
}

ROOT = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL"

# Crear carpetas si no existen
for folder in DIRS.keys():
    os.makedirs(os.path.join(ROOT, "archive", folder), exist_ok=True)

# Mover archivos
for folder, patterns in DIRS.items():
    for pattern in patterns:
        for file in glob.glob(os.path.join(ROOT, pattern)):
            if os.path.isfile(file):
                # Avoid moving standard files if matched
                filename = os.path.basename(file)
                if filename in ["README.md", "zuly_cli.py", "dashboard.py"]:
                    continue
                shutil.move(file, os.path.join(ROOT, "archive", folder, filename))
                print(f"Moved {filename} -> archive/{folder}/")

print("Organización completada.")
