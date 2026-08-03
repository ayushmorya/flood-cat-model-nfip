"""
Run this once your environment is set up:
    python src/check_setup.py

It just confirms every package you'll need for Phases 2-9 is installed
and importable. If this prints all OK, you're ready for Phase 2.
"""

import importlib

packages = ["pandas", "numpy", "matplotlib", "plotly", "scipy"]

print("Checking environment for flood-cat-model-nfip...\n")

all_ok = True
for pkg in packages:
    try:
        module = importlib.import_module(pkg)
        version = getattr(module, "__version__", "unknown version")
        print(f"  [OK] {pkg:<12} {version}")
    except ImportError:
        print(f"  [MISSING] {pkg:<12} -> run: pip install {pkg}")
        all_ok = False

print()
if all_ok:
    print("Environment ready. You can move on to Phase 2 (data collection).")
else:
    print("Some packages are missing. Run: pip install -r requirements.txt")
