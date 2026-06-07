import os
import shutil
from pathlib import Path
from glob import glob

os.chdir(r'c:\Users\Admin\Desktop\ZULY_IA_LOCAL')
base = Path('.')
archive = base / 'archive'

# Crear estructura
dirs = ['debug_logs', 'historical_reports', 'legacy_consolidators', 'old_demos', 'legacy_validators', 'bitacora_historica']
for d in dirs:
    (archive / d).mkdir(parents=True, exist_ok=True)

# Mover debug_*.txt
for f in glob('debug_*.txt'):
    shutil.move(f, str(archive / 'debug_logs' / f))
for f in glob('debug_*.py'):
    shutil.move(f, str(archive / 'debug_logs' / f))
for f in glob('debug_*.log'):
    shutil.move(f, str(archive / 'debug_logs' / f))
for f in glob('lab_*.log'):
    shutil.move(f, str(archive / 'debug_logs' / f))

# Mover reportes
for f in glob('REPORTE_*.md'):
    shutil.move(f, str(archive / 'historical_reports' / f))
for f in glob('RESUMEN_*.md'):
    shutil.move(f, str(archive / 'historical_reports' / f))

# Mover consolidadores
for f in glob('consolidate_*.py'):
    shutil.move(f, str(archive / 'legacy_consolidators' / f))
for f in glob('run_youtube_*.py'):
    shutil.move(f, str(archive / 'legacy_consolidators' / f))

# Mover demos
demos = ['demo_agent.py', 'demo_c1_evaluador.py', 'demo_c2_memory.py', 'demo_c3_objectives.py', 'demo_c4_auto_tuning.py', 'demo_fase2.py', 'demo_learning_freedom.py', 'demo_lyzu_interactive.py', 'demo_mejoras_blender.py', 'demo_sculpted_building.py', 'demo_zuly_cmd.py']
for f in demos:
    if Path(f).exists():
        shutil.move(f, str(archive / 'old_demos' / f))

# Mover validators
vals = ['core/validation/v0_validator.py', 'core/validation/v1_validator.py', 'core/validation/v2_validator.py']
for f in vals:
    if Path(f).exists():
        shutil.move(f, str(archive / 'legacy_validators' / f.split('/')[-1]))

# Mover bitácoras
if Path('bitacora').exists():
    shutil.move('bitacora', str(archive / 'bitacora_historica' / 'bitacora'))
if Path('BITACORA_DE_AVANCE').exists():
    shutil.move('BITACORA_DE_AVANCE', str(archive / 'bitacora_historica' / 'BITACORA_DE_AVANCE'))

# Resumen
print('✅ Archivado completado')
for d in dirs:
    path = archive / d
    count = len(list(path.rglob('*')))
    print(f'  {d}: {count} items')
