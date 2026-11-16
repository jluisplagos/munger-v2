#!/usr/bin/env python3
"""r2c · N10 (tercera pasada), con PÁGINAS REALES: en los textos conservados de los tres expedientes finales de la 4.14 se buscan cifras
con decimales que llevan pegado un código de moneda delante («CHF7.3») o una letra detrás («3.75x») y, para cada una, se contrasta con los
dos códigos la cita que un extractor escribiría cortando justo en la cifra (sin el código o sin la letra) y la que incluye el trozo pegado.
No son entradas de ningún registro: son páginas reales con citas construidas por el revisor.  Uso: python3 -I -B r2c_tokens_pegados_pagina_real.py"""
import collections, glob, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun3 import VE, VP, PV
E14 = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_14")
c = collections.Counter()
ej = collections.defaultdict(list)
for exp in ("vidrala_decisiones/Vidrala", "elis_decisiones/Elis", "viscofan_decisiones/Viscofan"):
    for p in sorted(glob.glob(os.path.join(E14, exp, "texto", "*.txt"))):
        t = open(p, encoding="utf-8", errors="replace").read()
        partes = re.split(r"\[PDF PAGE (\d+)\]", t)
        for i in range(1, len(partes) - 1, 2):
            pag = partes[i + 1]
            for tipo, rx in (("código de moneda pegado delante", r"(?<![\w.,])(?:EUR|USD|GBP|CHF|DKK|SEK|NOK|BRL|JPY)(\d{1,3}(?:[.,]\d{3})*[.,]\d+)(?![\w]|[.,]\d)(\s+\w+)?"),
                             ("letra pegada detrás (x, m, bn, pp, k)", r"(?<![\w.,])(\w+\s+)?(\d{1,3}(?:[.,]\d{3})*[.,]\d+)(?:x|m|bn|pp|k|M)\b")):
                for m in re.finditer(rx, pag):
                    if tipo.startswith("código"):
                        num, corta, larga = m.group(1), (m.group(1) + (m.group(2) or "")), m.group(0)
                    else:
                        num, corta, larga = m.group(2), ((m.group(1) or "") + m.group(2)), m.group(0)
                    try:
                        vf = float(num.replace(",", "")) if re.fullmatch(r"\d{1,3}(,\d{3})*\.\d+", num) else float(num.replace(".", "").replace(",", "."))
                    except ValueError:
                        continue
                    for etq, cita in (("cita cortada en la cifra", corta), ("cita con el trozo pegado", larga)):
                        r1, r2 = VP._cita_cifra(cita, vf, pag)[0], VE._cita_cifra(cita, vf, pag)[0]
                        c[(tipo, etq, r1, r2)] += 1
                        if len(ej[(tipo, etq, r1, r2)]) < 3:
                            ej[(tipo, etq, r1, r2)].append((os.path.basename(p)[:40], int(partes[i]), cita, vf, pag[max(0, m.start() - 25):m.end() + 12].replace("\n", "⏎")))
print("(forma, cita, anterior → tercera): nº de apariciones en páginas reales")
for k in sorted(c):
    print(f"   {k[0]:40} {k[1]:26} {k[2]:20} → {k[3]:20} {c[k]}")
    for x in ej[k]:
        print("        ", x)
