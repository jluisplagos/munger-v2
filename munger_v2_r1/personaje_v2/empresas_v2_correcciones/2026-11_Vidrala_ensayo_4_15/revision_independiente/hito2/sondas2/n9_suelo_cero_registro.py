#!/usr/bin/env python3
"""n9 · H6 (segunda pasada), _suelo_cero en el registro completo (arnés fx5): ¿la excepción «constante en el punto real, pero con un 0 de
min/max y resultado 0» permite dar por comprobado un CERO sin fuente? Se convierten los ceros comprobados (con su fuente) del fixture en
derivados sin fuente con min(o[año], 0) o max(o[a] − o[b], 0), y se compara con las formas que ya se aceptaban (U1).
Uso: python3 -I -B n9_suelo_cero_registro.py   (PV=<cand>/personaje_v2 para la candidata)"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sondas"))
import fx5 as X
VE = X.VE
print("código:", "estable" if hasattr(VE, "_apariciones_en_pagina") else "candidata (1.ª pasada)")
r0 = X.con()
print("control positivo:", X.resumen(r0)[:75])
ceros = [e["celda"] for e in X.REG["entradas"] if e["clase"] == "cero_comprobado" and e.get("ambito") == "calculo"]
ANIO, OTRO = "Historia!F5", "Historia!G5"
print(f"ceros comprobados de cálculo en el fixture: {len(ceros)} (p. ej. {ceros[:4]}) · {ANIO} = {X.inst['celdas'][ANIO]} · {OTRO} = {X.inst['celdas'][OTRO]}")


def probar(nombre, formula, origenes, n=None):
    ks = ceros[:n] if n else ceros

    def cambio(g):
        for k in ks:
            e = X.ent(g, k)
            e.update(clase="derivado", derivacion={"origenes": origenes, "formula": formula, "conciliacion": "(prueba) sin fuente", "unidad": "mm"})
            e.pop("fuente", None)
    r = X.con(cambio, resellar=True)
    ok = sum(k in r["comprobadas"] for k in ks)
    ej = [x[:170] for x in X.con_k(r, ks[0])][:1]
    print(f"   {nombre}\n      {formula}\n      -> apto={r['apto_por_entradas']} · {ok} de {len(ks)} ceros SIN FUENTE quedan comprobados · derivados_comprobados={len(r.get('derivados_comprobados') or [])} {ej}")


probar("1 min(año, 0): el año es positivo, el resultado es el 0 literal", f'min(o["{ANIO}"], 0)', [ANIO])
probar("2 max(año − año siguiente, 0): el suelo actúa siempre", f'max(o["{ANIO}"] - o["{OTRO}"], 0)', [ANIO, OTRO])
probar("3 max(−año, 0)", f'max(-o["{ANIO}"], 0)', [ANIO])
probar("4 control (ya se aceptaba, U1): año − año compuesto con literales admitidos", f'o["{ANIO}"] - (2*1000 + 1*10 + 9)' if X.inst["celdas"][ANIO] == 2019 else f'o["{ANIO}"] - o["{ANIO}"]', [ANIO])
probar("5 control (tiene que rechazarse): año − año", f'o["{ANIO}"] - o["{ANIO}"]', [ANIO])
probar("6 control (tiene que rechazarse): min(max(año, 0), 0), constante en todo punto", f'min(max(o["{ANIO}"], 0), 0)', [ANIO])
r = X.con()
print("control positivo al final:", X.resumen(r)[:75])
X.limpiar()
