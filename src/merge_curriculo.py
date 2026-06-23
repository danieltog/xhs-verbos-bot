#!/usr/bin/env python3
"""
Merge all curriculum files into one and generate all scripts.
Run this once to populate the full A1 curriculum.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.contenido_a1 import A1_CURRICULO
from src.contenido_a1_extra import EXTRA_MODULOS
from src.contenido_a1_extra2 import EXTRA2
from src.contenido_a1_extra3 import EXTRA3
from src.contenido_a1_extra4 import EXTRA4
from src.contenido_a1_extra5 import EXTRA5

# Merge all modules
A1_CURRICULO["modulos"].extend(EXTRA_MODULOS)
A1_CURRICULO["modulos"].extend(EXTRA2)
A1_CURRICULO["modulos"].extend(EXTRA3)
A1_CURRICULO["modulos"].extend(EXTRA4)
A1_CURRICULO["modulos"].extend(EXTRA5)

# Update calendar
import yaml
cal_path = Path(__file__).resolve().parent.parent / "scripts" / "calendario.yaml"

cal = {"orden": [], "dia_actual": 0}
for mod in A1_CURRICULO["modulos"]:
    entry = {
        "nivel": "A1",
        "modulo": mod["slug"],
        "lecciones": [l["slug"] for l in mod["lecciones"]],
    }
    cal["orden"].append(entry)

with open(cal_path, "w") as f:
    yaml.dump(cal, f, allow_unicode=True, sort_keys=False)

print(f"📅 Calendario actualizado: {sum(len(m['lecciones']) for m in A1_CURRICULO['modulos'])} lecciones en {len(A1_CURRICULO['modulos'])} módulos")

# Generate all scripts
from src.content_factory import build_all
paths = build_all(force=True)

total_scripts = len(paths)
total_slides = 0
for p in paths:
    with open(p) as f:
        d = yaml.safe_load(f)
        total_slides += len(d.get("slides", []))

print(f"\n✅ {total_scripts} scripts generados ({total_slides} slides en total)")
print(f"   Módulos: {len(A1_CURRICULO['modulos'])}")
print(f"   Listo para usar en el dashboard!")
