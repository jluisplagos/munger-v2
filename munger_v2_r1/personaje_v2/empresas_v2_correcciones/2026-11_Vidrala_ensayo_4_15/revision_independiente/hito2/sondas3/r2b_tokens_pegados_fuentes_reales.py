#!/usr/bin/env python3
"""r2b · N10 (tercera pasada): ¿con qué frecuencia aparecen en los textos conservados REALES (los 34 de los tres expedientes finales de la
4.14) las formas que la regla del «fragmento completo» rechaza si la cita acaba o empieza justo en la cifra? (a) cifra con una letra o un
superíndice pegado detrás («849.7m», «12,5x», «1.2bn», «849,7¹»); (b) cifra con una letra pegada delante («EUR849,7», «FY2024»);
(c) palabra tras un punto o una coma pegados («2.3.Deuda», «ejercicio.Total»). Solo lee.  Uso: python3 -I -B r2b_tokens_pegados_fuentes_reales.py"""
import collections, glob, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun3 import PV
E14 = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_14")
PAT = {"(a) cifra con decimales o miles + letra o superíndice pegado detrás": r"(?<![\w.,])\d{1,3}(?:[.,]\d{3})*[.,]\d+(?=[^\W\d_])",
       "(a2) entero + letra pegada detrás (150MW, 12x, 2024E)": r"(?<![\w.,])\d+(?=[^\W\d_])",
       "(b) letra pegada delante de una cifra con decimales o miles": r"(?<=[^\W\d_])\d{1,3}(?:[.,]\d{3})*[.,]\d+(?![\w.,]|[.,]\d)",
       "(b2) letra pegada delante de un entero (FY2024, T4, Q1)": r"(?<=[^\W\d_])\d+(?![\w]|[.,]\d)",
       "(c) palabra de 3+ letras tras «.» o «,» pegados a otra palabra o cifra": r"(?<=\w[.,])[^\W\d_]{3,}"}
tot = collections.Counter()
ej = collections.defaultdict(collections.Counter)
n_txt = 0
for exp in ("vidrala_decisiones/Vidrala", "elis_decisiones/Elis", "viscofan_decisiones/Viscofan"):
    for p in sorted(glob.glob(os.path.join(E14, exp, "texto", "*.txt"))):
        n_txt += 1
        t = open(p, encoding="utf-8", errors="replace").read()
        for k, rx in PAT.items():
            for m in re.finditer(rx, t):
                tot[(exp.split("/")[0], k)] += 1
                ej[k][t[max(0, m.start() - 12):m.end() + 6].replace("\n", "⏎")] += 1
print("textos conservados:", n_txt)
for k in PAT:
    print(f"\n{k}")
    for exp in ("vidrala_decisiones", "elis_decisiones", "viscofan_decisiones"):
        print(f"   {exp:22} {tot[(exp, k)]}")
    print("   ejemplos más frecuentes:", [f"{x!r}×{n}" for x, n in ej[k].most_common(8)])
