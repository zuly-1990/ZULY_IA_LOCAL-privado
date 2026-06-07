import sys
import os
from pathlib import Path

# Simulate stress test path logic
zuly_path = Path(__file__).parent.parent
sys.path.insert(0, str(zuly_path))

import core.adapters.blender_adapter as ba
import core.agent as agent

print(f"--- PATH DIAGNOSTIC ---")
print(f"Sys Path: {sys.path[:3]}")
print(f"BlenderAdapter file: {ba.__file__}")
print(f"Agent file: {agent.__file__}")
print(f"CWD: {os.getcwd()}")
print(f"--- END ---")
