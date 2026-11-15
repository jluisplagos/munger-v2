#!/usr/bin/env python3
"""Alcance H1 sin textos fuente · mide, solo dentro de los AR_*.json, rasgos que la reparación tendría que cubrir.

Uso: python3 -I -B alcance_lineas.py DIR_EMPRESAS SALIDA_JSON
Para cada componente {concepto, impreso, pagina, linea}:
  - impreso_en_linea_como_token: el número aparece en la línea como número completo (no como trozo de otro);
  - impreso_solo_como_subcadena: aparece en la línea, pero solo dentro de otro número (lo aceptaría la prueba actual);
  - concepto_en_linea: el texto del concepto aparece en la línea declarada;
  - linea_con_varios_numeros: la línea tiene ≥ 2 importes (riesgo de columna equivocada).
No dice nada sobre las páginas reales: texto/ no está en el paquete.
"""
import glob
import json
import os
import re
import sys

empresas, salida = sys.argv[1], sys.argv[2]
norm = lambda s: re.sub(r"\s+", " ", str(s).replace("−", "-").replace("–", "-").replace("—", "-")).strip()
NUMTOK = re.compile(r"\(?-?\d[\d.,]*\)?")
R = {}
for c in sorted(glob.glob(os.path.join(empresas, "*", ""))):
    e = os.path.basename(os.path.dirname(c))
    n = tok = sub = noen = conc = varios = sin_linea = 0
    ejemplos_sub = []
    for f in sorted(glob.glob(os.path.join(c, "fase1_partes", "AR_*.json"))):
        d = json.load(open(f, encoding="utf-8"))
        for k, p in (d.get("partidas") or {}).items():
            if not isinstance(p, dict):
                continue
            for cual in ("actual", "anterior"):
                x = p.get(cual)
                if isinstance(x, dict):
                    x = x.get("componentes") or ([x] if "impreso" in x else [])
                for y in (x or []):
                    if not isinstance(y, dict) or "impreso" not in y:
                        continue
                    n += 1
                    imp, lin = norm(y.get("impreso")), norm(y.get("linea") or "")
                    if not lin:
                        sin_linea += 1
                        continue
                    if re.search(r"(?<![\d.,])" + re.escape(imp) + r"(?![\d.,]*\d)", lin):
                        tok += 1
                    elif imp in lin:
                        sub += 1
                        if len(ejemplos_sub) < 5:
                            ejemplos_sub.append(f"{os.path.basename(f)} {k} {cual}: impreso {imp!r} · línea {lin[:120]!r}")
                    else:
                        noen += 1
                    if y.get("concepto") and norm(y["concepto"]).lower() in lin.lower():
                        conc += 1
                    nums = [t for t in NUMTOK.findall(lin) if re.search(r"\d", t) and not re.fullmatch(r"\(?(19|20)\d\d\)?", t) and len(re.sub(r"\D", "", t)) >= 1]
                    if len(nums) >= 2:
                        varios += 1
    R[e] = {"componentes": n, "sin_linea": sin_linea, "impreso_en_linea_como_token": tok, "impreso_solo_como_subcadena": sub,
            "impreso_no_esta_en_linea": noen, "concepto_en_linea": conc, "linea_con_varios_numeros": varios, "ejemplos_subcadena": ejemplos_sub}
json.dump(R, open(salida, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
tot = {k: sum(v[k] for v in R.values()) for k in ("componentes", "sin_linea", "impreso_en_linea_como_token", "impreso_solo_como_subcadena", "impreso_no_esta_en_linea", "concepto_en_linea", "linea_con_varios_numeros")}
for e, v in R.items():
    print(e, {k: v[k] for k in tot}, v["ejemplos_subcadena"][:2])
print("TOTAL", tot)
