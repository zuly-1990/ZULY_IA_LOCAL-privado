import sys
from pathlib import Path

# Add root
sys.path.insert(0, str(Path(__file__).parent))

try:
    from core.knowledge.atomic_dictionary import ATOMIC_DICTIONARY
    print("KEYS:", ATOMIC_DICTIONARY.keys())
    if "procedural_descriptors" in ATOMIC_DICTIONARY:
        print("PROCEDURAL:", ATOMIC_DICTIONARY["procedural_descriptors"])
    else:
        print("MISSING 'procedural_descriptors' key.")
except Exception as e:
    print(f"ERROR: {e}")
