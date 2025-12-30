from pathlib import Path
import os

BASE_DIR = Path(__file__).parent.absolute()
print(f"Current Script Dir: {BASE_DIR}")

# Simulating server/main.py location logic
# If this script is in Root, and server is in Root/server...
# Wait, I'll put this script in ROOT. So BASE_DIR is ROOT.
# main.py says BASE_DIR = Path(__file__).parent.parent (since it's in server/)
# So effectively BASE_DIR in main.py is ROOT.

ROOT = BASE_DIR
DATOS_DIR = ROOT / "datos"
TARGET_FILE = DATOS_DIR / "DATA PARA EL CONTEO ANUAL.xlsx"

print(f"Checking Path: {TARGET_FILE}")
print(f"Exists? {TARGET_FILE.exists()}")

if DATOS_DIR.exists():
    print(f"Contents of {DATOS_DIR}:")
    for f in DATOS_DIR.iterdir():
        print(f" - '{f.name}'")
else:
    print("Directory 'datos' does not exist!")
