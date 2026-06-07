#!/usr/bin/env python3
import sys
import subprocess

result = subprocess.run([sys.executable, r'c:\Users\Admin\Desktop\ZULY_IA_LOCAL\fase2_cleanup.py'], 
                       cwd=r'c:\Users\Admin\Desktop\ZULY_IA_LOCAL')
sys.exit(result.returncode)
