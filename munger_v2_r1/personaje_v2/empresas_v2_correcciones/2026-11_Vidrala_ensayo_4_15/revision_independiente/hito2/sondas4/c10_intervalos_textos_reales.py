#!/usr/bin/env python3
"""c10 · T8 (cuarta comprobación) sobre los TEXTOS REALES: para cada entero de 1 a 4 cifras que sigue pegado a un guion a otro entero
(«2019-2020», «2019-20», «63-93», «L. 225-129-5»…) en los textos conservados que citan los siete registros de la 4.14, el signo que le da
_signo_en_cita con la candidata anterior (f3d15e8) y con la cuarta (7a6583b). Dice cuántas formas reales pasan de «intervalo» (+) a
«indeterminado» (pendiente si alguien las citara como valor) y si alguna pasa a leerse como signo. Solo lee.
Uso: python3 -I -B c10_intervalos_textos_reales.py"""
import collections, glob, os, re, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sondas3"))
from comun3 import VE, VP, PV, ACT, ANT  # noqa: E402
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
trans, ej = collections.Counter(), collections.defaultdict(list)
GUI = "-‐‑‒–—−"
for p in sorted(textos):
    for linea in open(p, encoding="utf-8", errors="replace").read().split("\n"):
        for m in re.finditer(r"(\d{1,4})[" + GUI + r"](\d{1,4})(?![\d]|[.,]\d)", linea):
            if m.start() > 0 and re.match(r"[\d.,]", linea[m.start() - 1]):
                continue
            a, b = VP._signo_en_cita(linea, m.start(2), m.end(2)), VE._signo_en_cita(linea, m.start(2), m.end(2))
            forma = f"{len(m.group(1))} cifras-{len(m.group(2))} cifras" + (" (misma longitud)" if len(m.group(1)) == len(m.group(2)) else "")
            trans[(nom[a], nom[b], forma)] += 1
            if a != b and len(ej[(nom[a], nom[b], forma)]) < 4:
                ej[(nom[a], nom[b], forma)].append(linea[max(0, m.start() - 25):m.end() + 12].strip())
print(f"VE = {ACT} · VP = {ANT} · textos conservados citados por los registros: {len(textos)}")
tot = collections.Counter()
for (a, b, forma), n in sorted(trans.items()):
    tot[(a, b)] += n
    print(f"   {a:14} → {b:14} {forma:32} {n:6}" + ("".join(f"\n         «{x}»" for x in ej[(a, b, forma)]) if a != b else ""))
print("totales (anterior → cuarta):", {f"{a} → {b}": n for (a, b), n in sorted(tot.items())})
