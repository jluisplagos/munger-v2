#!/usr/bin/env python3
"""Alcance · qué expedientes podrían compartir los problemas H1–H3 (solo lectura).

Uso: python3 -I -B alcance.py DIR_EMPRESAS SALIDA_JSON
Por empresa:
  - si existe texto/ (fuentes en texto para volver a pasar comprobar_anio) y cuántos componentes y ceros hay en fase1_partes;
  - cuántos ceros declarados hay (H1: el cero solo exige motivo + página existente);
  - años con FCF al accionista negativo en Historia fila 35 (valores cacheados del libro evaluado) y toda frase del tipo
    «N años negativos» en fase_a.md, fase_c.json e informe.md, con el número que dice (H3 generalizado, solo esa forma de frase);
  - qué constructor de la Historia consta en estado_pipeline.json.
"""
import glob
import json
import os
import re
import sys

import openpyxl

empresas, salida = sys.argv[1], sys.argv[2]
NUM = {"un": 1, "uno": 1, "dos": 2, "tres": 3, "cuatro": 4, "cinco": 5, "seis": 6, "siete": 7, "ocho": 8, "nueve": 9, "diez": 10}
FRASE = re.compile(r"\b(\w+) (?:de (?:los )?(?:diez|\w+) )?(?:años|ejercicios) (?:con (?:FCF|flujo)[^.,;]{0,30} )?negativos(?: de (\w+))?", re.I)
R = []
for c in sorted(glob.glob(os.path.join(empresas, "*", ""))):
    e = os.path.basename(os.path.dirname(c))
    r = {"empresa": e, "texto_presente": os.path.isdir(os.path.join(c, "texto"))}
    comps = ceros = 0
    ceros_lista = []
    for f in sorted(glob.glob(os.path.join(c, "fase1_partes", "AR_*.json"))):
        d = json.load(open(f, encoding="utf-8"))
        for k, p in (d.get("partidas") or {}).items():
            if not isinstance(p, dict):
                continue
            for cual in ("actual", "anterior"):
                x = p.get(cual)
                if isinstance(x, dict):
                    x = x.get("componentes") or ([x] if "impreso" in x else [])
                comps += len([y for y in (x or []) if isinstance(y, dict)])
            if p.get("cero"):
                ceros += 1
                ceros_lista.append(f"{os.path.basename(f)}:{k}")
    r["componentes_extraidos"] = comps
    r["ceros_declarados"] = ceros
    r["ceros"] = ceros_lista
    est = os.path.join(c, "estado_pipeline.json")
    hist = json.load(open(est, encoding="utf-8")).get("historial", []) if os.path.exists(est) else []
    r["constructor_historia"] = sorted({m.group(0) for h in hist for m in re.finditer(r"fase1_historia\.py (preparar|construir)", h)}) or ["no consta fase1_historia.py en el historial"]
    ev = glob.glob(os.path.join(c, "*_v63_evaluada.xlsx"))
    if ev:
        ws = openpyxl.load_workbook(ev[0], data_only=True)["Historia"]
        anios = [ws.cell(5, k).value for k in range(3, 13)]
        v = [ws.cell(35, k).value for k in range(3, 13)]
        r["fila35"] = dict(zip(map(str, anios), v))
        r["anios_negativos_fila35"] = [a for a, x in zip(anios, v) if isinstance(x, (int, float)) and x < 0]
    afirm = []
    for nombre in ("fase_a.md", "fase_c.json", "informe.md", "fase_b.md"):
        p = os.path.join(c, nombre)
        if not os.path.exists(p):
            continue
        for i, l in enumerate(open(p, encoding="utf-8").read().splitlines(), 1):
            for m in FRASE.finditer(l):
                w = m.group(1).lower()
                if w in NUM:
                    ctx = l[max(0, m.start() - 120): m.end() + 40]
                    afirm.append({"archivo": nombre, "linea": i, "dice": NUM[w], "frase": m.group(0), "contexto": ctx,
                                  "menciona_FCF": bool(re.search(r"FCF|flujo", ctx, re.I))})
    r["afirmaciones_n_anios_negativos"] = afirm
    R.append(r)
json.dump(R, open(salida, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for r in R:
    print(f"== {r['empresa']}: texto/={r['texto_presente']} componentes={r['componentes_extraidos']} ceros={r['ceros_declarados']} constructor={r['constructor_historia']}")
    print(f"   fila35 negativos: {r.get('anios_negativos_fila35')} ({len(r.get('anios_negativos_fila35') or [])})")
    for a in r["afirmaciones_n_anios_negativos"]:
        print(f"   {a['archivo']}:{a['linea']} dice {a['dice']} · FCF={a['menciona_FCF']} · «{a['frase']}» · …{a['contexto'][-160:]}")
