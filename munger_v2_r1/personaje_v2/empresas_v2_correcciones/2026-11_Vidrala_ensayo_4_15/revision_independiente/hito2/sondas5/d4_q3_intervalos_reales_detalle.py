#!/usr/bin/env python3
"""d4 · Q3 (quinta comprobación) sobre los TEXTOS REALES, detalle de c10: los pares «dddd-dddd» de los 73 textos conservados citados por
los siete registros. Para cada uno, el signo que _signo_en_cita da al segundo entero con 7a6583b y con 876bfc2, y la clase del par según
el revisor (años crecientes 1900–2100, años decrecientes, otro). También: los pares con prefijo FY/AF/EJ y los que tienen una letra
pegada delante del primer año. Solo lee.  Uso: python3 -I -B d4_q3_intervalos_reales_detalle.py"""
import collections, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun5 import VE, VP, PV, ACT, ANT  # noqa: E402
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
nom = {1: "+", -1: "−", None: "indeterminado"}
GUI = "-‐‑‒–—−"
c = collections.Counter()
ej = collections.defaultdict(collections.Counter)
for p in sorted(textos):
    for linea in open(p, encoding="utf-8", errors="replace").read().split("\n"):
        for m in re.finditer(r"(\d{4})[" + GUI + r"](\d{4})(?![\d]|[.,]\d)", linea):
            if m.start() > 0 and re.match(r"[\d.,]", linea[m.start() - 1]):
                continue
            a, b = int(m.group(1)), int(m.group(2))
            clase = ("años crecientes (1900–2100)" if 1900 <= a <= b <= 2100 else "años DECRECIENTES (1900–2100)" if 1900 <= b < a <= 2100 else "otro (no son dos años plausibles)")
            pegado = m.start() > 0 and re.match(r"\w", linea[m.start() - 1]) is not None
            pref = re.search(r"(?:FY|AF|EJ)$", linea[:m.start()], re.I) is not None
            sa, sb = VP._signo_en_cita(linea, m.start(2), m.end(2)), VE._signo_en_cita(linea, m.start(2), m.end(2))
            k = (clase, "letra pegada delante" if pegado else "sin letra delante", "prefijo FY/AF/EJ" if pref else "", nom[sa], nom[sb])
            c[k] += 1
            ej[k][linea[max(0, m.start() - 22):m.end() + 10].strip()] += 1
print(f"VE = {ACT} · VP = {ANT} · textos: {len(textos)}")
for k, n in sorted(c.items()):
    print(f"   {k[0]:34} {k[1]:22} {k[2]:17} 7a6583b {k[3]:13} → 876bfc2 {k[4]:13} {n:5}")
    if k[3] != k[4] or k[0] != "años crecientes (1900–2100)" or k[1] != "sin letra delante":
        for x, v in ej[k].most_common(6):
            print(f"         {v:3} × «{x}»")
