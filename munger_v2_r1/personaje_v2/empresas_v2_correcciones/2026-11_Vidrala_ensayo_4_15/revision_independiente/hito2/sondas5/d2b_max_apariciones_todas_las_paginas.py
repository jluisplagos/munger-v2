#!/usr/bin/env python3
"""d2b · MAX_APARICIONES_CITA = 200 sobre TODAS las páginas de los textos conservados que citan los siete registros reales (no solo las
páginas citadas): la cifra que más se repite como aparición completa en cada página (lo que contaría la cita más corta posible, una sola
cifra) y el número de guiones. ¿En cuántas páginas una cita de una sola cifra superaría el máximo? Solo lee.
Uso: python3 -I -B d2b_max_apariciones_todas_las_paginas.py"""
import collections, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun5 import VE, PV, ACT  # noqa: E402
E14 = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_14")
EXPS = ["vidrala_decisiones_INVALIDO_perdio_analisis/Vidrala", "elis_decisiones/Elis", "viscofan/Viscofan", "elis_motor_A/Elis", "vidrala_decisiones/Vidrala", "vidrala/Vidrala", "viscofan_decisiones/Viscofan"]
textos = set()
for exp in EXPS:
    c = os.path.join(E14, exp)
    reg, err = VE.cargar(c)
    for e in reg["entradas"]:
        f = e.get("fuente") if isinstance(e.get("fuente"), dict) else {}
        if f.get("archivo") and str(f["archivo"]).lower().endswith(".txt"):
            r = VE._ruta_fuente(c, f["archivo"])
            if r:
                textos.add(os.path.realpath(r))
MAX = VE.MAX_APARICIONES_CITA
RX = re.compile(r"(?<![\d.,])\d+(?:[.,]\d+)*(?!\d|[.,]\d)")
n_pag, peor, peor_g, sobre, sobre_g, largas = 0, [], [], 0, 0, []
for p in sorted(textos):
    t = open(p, encoding="utf-8", errors="replace").read()
    partes = re.split(r"\[PDF PAGE (\d+)\]", t)
    for i in range(1, len(partes) - 1, 2):
        pag = re.sub("[   ]", " ", partes[i + 1])
        n_pag += 1
        cnt = collections.Counter(m.group(0) for m in RX.finditer(pag))
        if cnt:
            tok, k = cnt.most_common(1)[0]
            peor.append((k, tok, os.path.basename(p)[:40], int(partes[i])))
            sobre += k > MAX
        g = sum(pag.count(x) for x in "-‐‑‒–—−")
        peor_g.append((g, os.path.basename(p)[:40], int(partes[i])))
        sobre_g += g > MAX
        largas.append((len(pag), os.path.basename(p)[:40], int(partes[i])))
peor.sort(reverse=True)
peor_g.sort(reverse=True)
largas.sort(reverse=True)
print(f"código: {ACT} · {len(textos)} textos · {n_pag} páginas")
print(f"   páginas en las que alguna cifra aparece más de {MAX} veces: {sobre} · las cinco cifras más repetidas en una página: {peor[:5]}")
print(f"   páginas con más de {MAX} guiones: {sobre_g} · las cinco con más: {peor_g[:5]}")
print(f"   las tres páginas más largas (caracteres): {largas[:3]}")
