#!/usr/bin/env python3
"""s3d · Registros reales (solo lectura): combinaciones de signo de valor_fuente, «signo» y «tratamiento» en los datos publicados numéricos.
¿Hay entradas con signo −1 y un «tratamiento» que no explica la transformación («ninguno», vacío…)? ¿Y valor_fuente negativo con signo +1?"""
import collections, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import VE, PV

E414 = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_14")
for exp in ["elis_decisiones/Elis", "vidrala_decisiones/Vidrala", "viscofan_decisiones/Viscofan"]:
    reg, _ = VE.cargar(os.path.join(E414, exp))
    c = collections.Counter()
    trat = collections.Counter()
    ej = []
    for e in reg["entradas"]:
        f = e.get("fuente") if isinstance(e.get("fuente"), dict) else {}
        vf, sg = f.get("valor_fuente"), f.get("signo")
        if not VE._num(vf) or e.get("clase") != "dato_publicado":
            continue
        t = VE._norm_txt(f.get("tratamiento"))
        clave = f"valor_fuente {'negativo' if vf < 0 else 'positivo' if vf > 0 else 'cero'} · signo {sg!r} · modelo {'negativo' if (e.get('valor_modelo') or 0) < 0 else 'positivo o cero'}"
        c[clave] += 1
        if str(sg) in ("-1",):
            trat[t[:70]] += 1
            if t in ("ninguno", "", "no aplica", "n/a", "ninguna") and len(ej) < 5:
                ej.append((e["celda"], vf, sg, f.get("tratamiento"), str(f.get("cita"))[:80]))
    print(f"\n=== {exp}")
    for k, v in sorted(c.items()):
        print(f"   {v:4d}  {k}")
    print("   tratamientos de las entradas con signo −1:")
    for k, v in trat.most_common(8):
        print(f"      {v:4d}  {k!r}")
    for x in ej:
        print("      ejemplo con tratamiento que no explica:", x)
