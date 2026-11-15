#!/usr/bin/env python3
"""s10 · I19 sobre el expediente REAL del relevo caducado (elis_motor_A/Elis, 4.14; solo lectura, sin ejecutar el pipeline): la condición que
evalúa el paso 13 nuevo (estado «esperando 13:auditoria.md», material fijado ≠ material vigente) y los archivos cambiados que registraría.
Además, en todos los expedientes del árbol que esperan la auditoría: ¿el material fijado sigue siendo el vigente?"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import PV
import cierre_v2 as CIE

raiz = os.path.dirname(PV)
n = 0
for d, _dirs, files in sorted(os.walk(raiz)):
    if "estado_pipeline.json" not in files or "historial_cierres" in d or "antecedentes" in d:
        continue
    try:
        st = json.load(open(os.path.join(d, "estado_pipeline.json"), encoding="utf-8"))
    except Exception:  # noqa: BLE001
        continue
    if not isinstance(st, dict) or st.get("esperando") != "13:auditoria.md":
        continue
    n += 1
    fij = CIE.material_fijado(d)
    vig, huellas = CIE.material(d, os.path.basename(d))
    antes = (fij or {}).get("archivos") or {}
    cambiados = sorted(x for x in set(antes) | set(huellas) if antes.get(x) != huellas.get(x))
    pend = [s for s in st.get("solicitudes_auditoria") or [] if s.get("estado") == "pendiente"]
    print(f"{os.path.relpath(d, raiz)}\n   paso {st.get('paso')} · esperando {st.get('esperando')} · material en el estado {st.get('material_auditoria')} · fijado {(fij or {}).get('id')} · vigente {vig}"
          f"\n   relevo caducado (fijado ≠ vigente): {(fij or {}).get('id') != vig} · archivos cambiados: {cambiados}"
          f"\n   solicitudes pendientes: {[(s['id'], s.get('material')) for s in pend]} · intentos: {st.get('intentos')}")
print(f"expedientes que esperan la auditoría del paso 13: {n}")
