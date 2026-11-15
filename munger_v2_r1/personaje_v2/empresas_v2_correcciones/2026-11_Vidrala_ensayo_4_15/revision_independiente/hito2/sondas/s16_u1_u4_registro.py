#!/usr/bin/env python3
"""s16 · U1 y U4 en el registro sintético completo (arnés fx5): derivados con orígenes auxiliares publicados y comprobados.
1) max(a − b, 0) con el suelo activo (resultado 0, el caso para el que existe la fórmula);  2) origen «decorativo» multiplicado por un cero comprobado;
3) U1: un dato de cálculo sin fuente escrito con cifras admitidas a partir del año;  4) U1 con un origen anulado por round;
5) U1 en bloque: TODOS los datos numéricos de cálculo publicados, sin fuente, como «año − cifra compuesta»: ¿apto? ¿se cuentan y se listan?"""
import os, re, sys
from fractions import Fraction as Fr
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fx5 as X
VE, K = X.VE, X.K
print("control positivo:", X.resumen(X.con(), K)[:70])
ANIO = "Historia!F5"
v_anio = X.ent(X.REG, ANIO)["valor_modelo"]
k_der = next(e["celda"] for e in X.REG["entradas"] if e["clase"] == "dato_publicado" and e["celda"].startswith("Historia!") and isinstance(e["valor_modelo"], float) and e["valor_modelo"] > 0 and e["celda"] != K and not e["celda"].endswith("5"))
vd = X.ent(X.REG, k_der)["valor_modelo"]
KZ = next(e["celda"] for e in X.REG["entradas"] if e["clase"] == "cero_comprobado" and e["celda"].startswith("Historia!"))
PGS = {}


def aux(g, nombre, v, destino):
    base_f = dict(X.ent(g, K)["fuente"])
    vf = round(v * 1000)
    g["entradas"].append({"celda": nombre, "id": nombre, "ambito": "auxiliar", "uso": f"origen de {destino}", "material": True, "clase": "cero_comprobado" if v == 0 else "dato_publicado", "valor_modelo": v,
                          "fuente": dict(base_f, pagina=PGS[nombre], valor_fuente=vf, cita=f"Partida sintética de {nombre}: {vf:d}", periodo=X.ent(X.REG, destino)["fuente"]["periodo"], columna=X.ent(X.REG, destino)["fuente"]["columna"]),
                          "comprobacion": dict(X.COMPROBADA), "incidencia": None})


def probar(nombre, destino, origenes, formula, unidad="mm"):
    for n_, v in origenes.items():
        if n_.startswith("aux:"):
            PGS[n_] = X.nueva_pagina(f"Partida sintética de {n_}: {round(v * 1000):d}")

    def cambio(g):
        for n_, v in origenes.items():
            if n_.startswith("aux:"):
                aux(g, n_, v, destino)
        X.ent(g, destino).update(clase="derivado", fuente={}, derivacion=dict({"origenes": list(origenes), "formula": formula, "conciliacion": "(prueba)"}, **({"unidad": unidad} if unidad else {})))
    r = X.con(cambio, resellar=True)
    print(f"   {nombre}\n      {destino} (libro {X.inst['celdas'][destino]!r}) = {formula}  con {origenes}\n      -> apto={r['apto_por_entradas']} · {'comprobada' if destino in r['comprobadas'] else 'NO comprobada'} · derivados_comprobados={r.get('derivados_comprobados')} {'; '.join(x[:200] for x in X.con_k(r, destino))}")
    return r


def compuesta(x):
    """x (Fraction ≥ 0, con 6 decimales como mucho) escrita con dígitos y potencias de diez: «8*100 + 4*10 + 9 + 6/10 + …»."""
    ent_, dec = divmod(x, 1)
    partes = [f"{c}*{10 ** (len(str(ent_)) - i - 1)}" if len(str(ent_)) - i - 1 else c for i, c in enumerate(str(ent_)) if c != "0"]
    d = str(int(dec * 10 ** 6)).rjust(6, "0").rstrip("0")
    partes += [f"{c}/{10 ** (i + 1)}" for i, c in enumerate(d) if c != "0"]
    return "(" + " + ".join(partes or ["1 - 1"]) + ")"


probar("1 · max(a − b, 0) con el suelo ACTIVO", KZ, {"aux:a": 2.0, "aux:b": 5.0}, 'max(o["aux:a"] - o["aux:b"], 0)')
probar("1b · control: max(a − b, 0) con el suelo inactivo", k_der, {"aux:a": round(vd + 2.0, 3), "aux:b": 2.0}, 'max(o["aux:a"] - o["aux:b"], 0)')
probar("2 · origen decorativo: b + a × z con z = 0 comprobado", k_der, {"aux:b": vd, "aux:a": 2019.0, "aux:z": 0.0}, 'o["aux:b"] + o["aux:a"] * o["aux:z"]')
dif = Fr(repr(float(v_anio))) - Fr(repr(float(vd)))
r = probar("3 · U1: dato de cálculo sin fuente = año − cifra compuesta", k_der, {ANIO: v_anio}, f'o["{ANIO}"] - {compuesta(dif)}')
print("      resumen:", r["resumen"][-190:])
probar("4 · U1 con el origen anulado por round (sin decimales negativos)", k_der, {ANIO: v_anio}, f'{compuesta(Fr(repr(float(vd))))} + round(o["{ANIO}"] / 1000000000000)')

print("\n   5 · U1 en bloque: todos los datos numéricos de cálculo publicados (dato_publicado), sin fuente, como «año − cifra compuesta»")
objetivos = [e["celda"] for e in X.REG["entradas"] if e["clase"] == "dato_publicado" and e["ambito"] == "calculo" and isinstance(e["valor_modelo"], (int, float)) and not isinstance(e["valor_modelo"], bool)
             and e["celda"] != ANIO and not re.match(r"^Historia![C-L]5$", e["celda"])]


def bloque(g):
    for k in objetivos:
        v = X.ent(g, k)["valor_modelo"]
        d = Fr(repr(float(v_anio))) - Fr(repr(float(v)))
        f = f'o["{ANIO}"] - {compuesta(d)}' if d >= 0 else f'o["{ANIO}"] + {compuesta(-d)}'
        X.ent(g, k).update(clase="derivado", fuente={}, derivacion={"origenes": [ANIO], "formula": f, "conciliacion": "(prueba) sin fuente"})


r = X.con(bloque, resellar=True)
print(f"      {len(objetivos)} datos de cálculo convertidos en derivados sin fuente -> apto={r['apto_por_entradas']} · comprobadas {r['comprobadas_universo']}/{r['universo']} · errores {len(r['errores'])} · discrepancias {len(r['discrepancias'])} · "
      f"derivados_comprobados {len(r.get('derivados_comprobados') or [])} · datos_como_hipotesis {len(r['datos_como_hipotesis'])}")
print("      errores (primeros):", [x[:140] for x in r["errores"][:2]], "discrepancias (primeras):", [x[:140] for x in r["discrepancias"][:2]])
print("      resumen:", r["resumen"])
X.limpiar()
