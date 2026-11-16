#!/usr/bin/env python3
"""x5g · octava comprobación · coste de `importe_completo` nuevo frente al anterior en textos adversos (una tira larga de cifras y
separadores sin espacios) y en una página real grande. El cambio añade el apóstrofo a una clase que ya existía: ¿cambia el orden del coste?
Uso: python3 -I -B x5g_coste.py"""
import glob, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun8 import FN, FO, CONGELADO  # noqa: E402


def t(f, *a):
    t0 = time.perf_counter()
    r = f(*a)
    return r, time.perf_counter() - t0


for nombre, imp, texto in (("«1,» × 5.000 (tira sin espacios)", "1", "1," * 5000), ("«1,» × 10.000", "1", "1," * 10000), ("«1'» × 10.000", "1", "1'" * 10000),
                           ("«1 » × 200.000 (con espacios)", "1", "1 " * 200000), ("«849,7 » × 100.000 y el importe no está", "849,8", "849,7 " * 100000)):
    (ra, ta), (rn, tn) = t(FO.importe_completo, imp, texto), t(FN.importe_completo, imp, texto)
    print(f"   {nombre:45} anterior: {ra!s:5} {ta * 1000:8.1f} ms · nuevo: {rn!s:5} {tn * 1000:8.1f} ms")
# la página real más larga de un texto conservado
PVC = os.path.join(CONGELADO, "personaje_v2")
mayor = ("", 0, "")
for f in glob.glob(os.path.join(PVC, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_14", "*_decisiones", "*", "texto", "*.txt")):
    for k, v in FN.paginas(f).items():
        if len(v) > len(mayor[2]):
            mayor = (os.path.basename(f), k, v)
P = FN.norm(mayor[2])
for imp in ("1", "0", "2025", "849,7"):
    (ra, ta), (rn, tn) = t(FO.importe_completo, imp, P), t(FN.importe_completo, imp, P)
    print(f"   página real más larga ({mayor[0][:40]} p.{mayor[1]}, {len(P):,} caracteres), impreso {imp!r:8} anterior: {ra!s:5} {ta * 1000:6.2f} ms · nuevo: {rn!s:5} {tn * 1000:6.2f} ms")
