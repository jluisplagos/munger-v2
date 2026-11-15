#!/usr/bin/env python3
"""n13 · U6 (segunda pasada): pipeline.modo_entrada_efectiva sobre TODAS las carpetas del árbol que tienen alcance_v2.json,
entrada_efectiva.json o fase1_metadatos.json (solo lectura). ¿Algún expediente existente pasa a dar error con la estable?
Uso: python3 -I -B n13_u6_expedientes_reales.py > salida.json   (PV=<cand>/personaje_v2 para la candidata)"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun2 import PV, F
import pipeline as PL  # noqa: E402
raiz = os.path.join(F, "copia", "munger_v2_r1")  # los mismos expedientes para los dos códigos
out = {}
for d, ds, fs in os.walk(raiz):
    ds[:] = [x for x in ds if x not in ("__pycache__", ".lo_perfil")]
    if any(n in fs for n in ("alcance_v2.json", "entrada_efectiva.json", "fase1_metadatos.json")):
        try:
            r = list(PL.modo_entrada_efectiva(d))
        except ValueError as ex:
            r = ["ERROR", str(ex)[:160]]
        out[os.path.relpath(d, raiz)] = r
json.dump(out, sys.stdout, ensure_ascii=False, indent=0, sort_keys=True)
