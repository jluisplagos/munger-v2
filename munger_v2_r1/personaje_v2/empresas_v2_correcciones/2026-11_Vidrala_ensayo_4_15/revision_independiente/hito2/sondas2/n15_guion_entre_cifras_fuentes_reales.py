#!/usr/bin/env python3
"""n15 · H5 (segunda pasada): la regla nueva «un guion pegado entre dos cifras es un intervalo o una fecha → la segunda cifra es positiva».
¿Con qué frecuencia aparece «cifra-guion-cifra» en los textos conservados REALES (carpetas texto/ de los expedientes de la 4.14) y de qué
tipo es? Se clasifica cada aparición por su forma: año-año, fecha, otra con importes (la cifra de la derecha lleva separador decimal o de
miles, o la de la izquierda no es un año). Solo lee.   Uso: python3 -I -B n15_guion_entre_cifras_fuentes_reales.py"""
import collections, glob, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun2 import VE, PV

E14 = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_14")
rx = re.compile(r"(?<![\d.,])(\d[\d.,]*\d|\d)([-‐‑‒–—﹣－−])(\d[\d.,]*\d|\d)(?![\d])")
tot = collections.Counter()
ej = collections.defaultdict(list)
n_arch = 0
vistos = set()
for exp in ("elis_decisiones/Elis", "vidrala_decisiones/Vidrala", "viscofan_decisiones/Viscofan"):
    for p in sorted(glob.glob(os.path.join(E14, exp, "texto", "*.txt"))):
        h = VE._sha(p)
        if h in vistos:
            continue
        vistos.add(h)
        n_arch += 1
        t = open(p, encoding="utf-8", errors="replace").read()
        for linea in t.splitlines():
            for m in rx.finditer(linea):
                izq, g, der = m.group(1), m.group(2), m.group(3)
                anio = lambda s: re.fullmatch(r"(19|20)\d\d", s) is not None  # noqa: E731
                if anio(izq) and (anio(der) or re.fullmatch(r"\d\d", der)):
                    clase = "año-año (2019-2020, 2019-20)"
                elif re.fullmatch(r"\d{1,2}", izq) and re.fullmatch(r"\d{1,2}", der) and re.match(r"[-‐‑‒–—﹣－−]\d{2,4}\b", linea[m.end():m.end() + 6]):
                    clase = "fecha dd-mm-aaaa"
                elif re.fullmatch(r"\d{1,2}", der) and re.search(r"\d{4}[-‐‑‒–—﹣－−]\d{1,2}[-‐‑‒–—﹣－−]$", linea[:m.start(3)]):
                    clase = "fecha aaaa-mm-dd"
                elif re.search(r"[.,]\d", der) or re.search(r"[.,]\d", izq):
                    clase = "con separador decimal o de miles en algún lado (importes, porcentajes)"
                else:
                    clase = "enteros sin separador (páginas, notas, teléfonos, códigos, rangos)"
                tot[clase] += 1
                if len(ej[clase]) < (20 if clase.startswith("con separador") else 6):
                    ej[clase].append(linea.strip()[max(0, m.start() - 45 - (len(linea) - len(linea.lstrip()))):][:110])
print(f"textos conservados distintos examinados: {n_arch}")
for k, v in tot.most_common():
    print(f"   {v:6}  {k}")
    for x in ej[k][:20 if k.startswith("con separador") else 5]:
        print("            ", x)
