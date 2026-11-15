#!/usr/bin/env python3
"""H3 · Recuento de años con FCF al accionista negativo en Aarsleff (Historia fila 35) y rastreo de la afirmación.

Uso: python3 -I -B h3_aarsleff.py DIR_AARSLEFF LIBRO_RECALCULADO SALIDA_JSON
- Lee la fila 35 de Historia en tres fuentes: valores cacheados del libro evaluado, el mismo libro
  tras recálculo forzado con LibreOffice (copia en el diagnóstico), y un recálculo propio en Python
  a partir de fase1_v63.json (CFO − capex − int. fin. − arrend. − SBC, la fórmula de la fila 35).
- Busca qué fórmulas del libro dependen de Historia!C35:L35.
- Lista los archivos y celdas donde aparece «cuatro años negativos».
"""
import glob
import json
import os
import re
import sys

import openpyxl

carpeta, recalc, salida = sys.argv[1], sys.argv[2], sys.argv[3]
ev = os.path.join(carpeta, "Aarsleff_v63_evaluada.xlsx")
R = {}


def fila(libro, data_only=True):
    wb = openpyxl.load_workbook(libro, data_only=data_only)
    ws = wb["Historia"]
    return [ws.cell(5, c).value for c in range(3, 13)], [ws.cell(35, c).value for c in range(3, 13)], ws.cell(35, 1).value


anios, cache, etiqueta = fila(ev)
_, formulas, _ = fila(ev, data_only=False)
_, recalculado, _ = fila(recalc)
f1 = json.load(open(os.path.join(carpeta, "fase1_v63.json"), encoding="utf-8"))
H = f1["historia"]["partidas"]
propio = []
for i in range(10):
    cfo, capex = H["cfo"]["valores"][i], H["capex"]["valores"][i]
    resto = sum((H[k]["valores"][i] or 0) for k in ("intereses_financiacion", "arrendamientos_principal", "sbc"))
    propio.append(None if cfo is None or capex is None else round(cfo - capex - resto, 3))

neg = lambda serie: [a for a, v in zip(anios, serie) if isinstance(v, (int, float)) and v < 0]
R["etiqueta_fila_35"] = etiqueta
R["formula_C35"] = formulas[0]
R["anios"] = anios
R["fila35_cache"] = cache
R["fila35_recalculo_forzado"] = recalculado
R["fila35_recalculo_python_desde_fase1_v63"] = propio
R["anios_negativos"] = {"cache": neg(cache), "recalculo_forzado": neg(recalculado), "python": neg(propio)}
R["recuento"] = {k: len(v) for k, v in R["anios_negativos"].items()}
R["max_dif_cache_vs_recalculo"] = max(abs(a - b) for a, b in zip(cache, recalculado))
R["max_dif_cache_vs_python"] = max(abs(a - b) for a, b in zip(cache, propio))
R["suma_10_anios"] = round(sum(cache), 3)
R["media_2016_2020"] = round(sum(cache[:5]) / 5, 3)
R["media_2021_2025"] = round(sum(cache[5:]) / 5, 3)

# dependencias: fórmulas fuera de la fila 35 que lean Historia C35:L35
wb = openpyxl.load_workbook(ev)
dep = []
pat_otra = re.compile(r"Historia'?!\$?([C-L])\$?35(?!\d)|Historia'?!\$?[A-L]\$?\d+:\$?[C-L]\$?(3[5-9]|[4-9]\d)(?!\d)")
pat_misma = re.compile(r"(?<![A-Z!$])\$?([C-L])\$?35(?!\d)")
for ws in wb.worksheets:
    for row in ws.iter_rows():
        for c in row:
            v = c.value
            if not (isinstance(v, str) and v.startswith("=")):
                continue
            if ws.title == "Historia":
                if c.row != 35 and pat_misma.search(v):
                    dep.append(f"{ws.title}!{c.coordinate}: {v[:160]}")
            elif pat_otra.search(v):
                dep.append(f"{ws.title}!{c.coordinate}: {v[:160]}")
R["formulas_que_dependen_de_fila35"] = dep
R["nombres_definidos_con_Historia_35"] = [n for n in wb.defined_names if "Historia" in str(wb.defined_names[n].attr_text) and "35" in str(wb.defined_names[n].attr_text)]

# rastreo de la afirmación
frase = re.compile(r"cuatro años negativos", re.I)
apar = []
for f in sorted(glob.glob(os.path.join(carpeta, "**", "*"), recursive=True)):
    if os.path.isdir(f):
        continue
    rel = os.path.relpath(f, carpeta)
    if f.endswith(".xlsx"):
        try:
            w = openpyxl.load_workbook(f)
        except Exception as e:  # noqa: BLE001
            apar.append({"archivo": rel, "error": str(e)})
            continue
        for ws in w.worksheets:
            for row in ws.iter_rows():
                for c in row:
                    if isinstance(c.value, str) and frase.search(c.value):
                        apar.append({"archivo": rel, "celda": f"{ws.title}!{c.coordinate}", "veces": len(frase.findall(c.value))})
    elif f.endswith((".md", ".json", ".txt", ".csv")):
        t = open(f, encoding="utf-8", errors="replace").read()
        for i, l in enumerate(t.splitlines(), 1):
            if frase.search(l):
                apar.append({"archivo": rel, "linea": i, "veces": len(frase.findall(l))})
R["apariciones_cuatro_anios_negativos"] = apar
json.dump(R, open(salida, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: R[k] for k in ("anios", "fila35_cache", "fila35_recalculo_forzado", "fila35_recalculo_python_desde_fase1_v63", "anios_negativos", "recuento",
                                    "max_dif_cache_vs_recalculo", "max_dif_cache_vs_python", "suma_10_anios", "media_2016_2020", "media_2021_2025",
                                    "formulas_que_dependen_de_fila35", "nombres_definidos_con_Historia_35")}, ensure_ascii=False, indent=1))
print("apariciones:")
for a in apar:
    print(" ", a)
