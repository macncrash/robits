"""Build every AM drawing: /Applications/FreeCAD.app/Contents/Resources/bin/python build_all.py
Writes ../AM-<nn>-<name>.pdf (and _png/ previews) and prints layout warnings and sheet/model disagreements."""
import glob
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
for script in sorted(glob.glob(os.path.join(HERE, "am[0-9][0-9]_*.py"))):
    r = subprocess.run([sys.executable, script], capture_output=True, text=True, cwd=HERE)
    lines = [ln for ln in (r.stdout + r.stderr).splitlines() if ln.strip()]
    status = "ok" if r.returncode == 0 else "FAILED"
    print(f"{os.path.basename(script)}: {status}")
    for ln in lines:
        print("   ", ln)
