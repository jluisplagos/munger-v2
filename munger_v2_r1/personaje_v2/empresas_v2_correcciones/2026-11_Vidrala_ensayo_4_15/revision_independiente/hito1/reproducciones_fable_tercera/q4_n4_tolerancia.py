"""Tercera pasada · N4 (derivados: redondeo a 3 decimales solo con derivacion.unidad monetaria; si no, «exacto» con tolerancia 1e-9
relativa a la MAGNITUD DE LOS ORÍGENES). Sondas: la tolerancia de «exacto» cuando los orígenes son grandes (unidades, miles, acciones)
y el resultado es pequeño (ratio, tasa) o es un importe. Arnés fx3.py. Para comparar con el árbol de la segunda pasada:
PV=<copia del árbol de la segunda pasada>/personaje_v2 python3 -B q4_n4_tolerancia.py"""
import copy
import fx3 as fx
from fx3 import VE, con, ent, con_k, resumen, K, REG

inst = fx.inst
print("árbol:", fx.PV)
K_RATIO, K_TASA = "Historia!H15", "Análisis!C57"
print("celdas:", K_RATIO, inst["celdas"][K_RATIO], inst["ambito"][K_RATIO], "|", K_TASA, inst["celdas"][K_TASA], inst["ambito"][K_TASA], "|", K, inst["celdas"][K], inst["ambito"][K])
BASE_F = copy.deepcopy(ent(REG, K)["fuente"])
PAGS = {}


def pagina_de(v):
    if v not in PAGS:
        PAGS[v] = fx.nueva_pagina(f"Magnitud sintética: {v:.1f}")
    return PAGS[v]


def aux(nombre, v, unidad="unidades"):
    return {"celda": nombre, "id": nombre, "ambito": "auxiliar", "uso": "origen", "material": True, "clase": "dato_publicado", "valor_modelo": v,
            "comprobacion": dict(fx.COMPROBADA), "incidencia": None,
            "fuente": dict(copy.deepcopy(BASE_F), pagina=PAGS[v], unidad=unidad, escala=1, valor_fuente=v, cita=f"Magnitud sintética: {v:.1f}")}


CASOS = [
    # (rótulo, celda, {aux: valor}, fórmula, unidad del derivado)
    ("ratio 0,887 = n/d con n y d en UNIDADES (≈1e9): la fórmula da 0,25", K_RATIO, {"aux:n": 250000000.0, "aux:d": 1000000000.0}, 'o["aux:n"] / o["aux:d"]', None),
    ("ratio 0,887 = n/d con n y d en unidades: la fórmula da 0,5", K_RATIO, {"aux:n": 500000000.0, "aux:d": 1000000000.0}, 'o["aux:n"] / o["aux:d"]', None),
    ("tasa 0,0335 = n/d con n y d en unidades (≈1e9): la fórmula da 0,9", K_TASA, {"aux:n": 900000000.0, "aux:d": 1000000000.0}, 'o["aux:n"] / o["aux:d"]', None),
    ("ratio 0,887 = n/d con n y d en MILES (≈1e6): la fórmula da 0,8874 (el caso de N4, sin round)", K_RATIO, {"aux:n": 887400.0, "aux:d": 1000000.0}, 'o["aux:n"] / o["aux:d"]', None),
    ("ratio 0,887 = n/d con n y d en miles: la fórmula da 0,8879", K_RATIO, {"aux:n": 887900.0, "aux:d": 1000000.0}, 'o["aux:n"] / o["aux:d"]', None),
    ("ratio 0,887 = n/d con n y d en MILLONES (≈1e3): la fórmula da 0,8874 (control: debe ser discrepancia)", K_RATIO, {"aux:n": 887.4, "aux:d": 1000.0}, 'o["aux:n"] / o["aux:d"]', None),
    ("importe 849,697 mm = origen en unidades / 1e6, con unidad «mm»: la fórmula da 849,0 (0,697 mm menos)", K, {"aux:e": 849000000.0}, 'o["aux:e"] / 1000000', "mm"),
    ("importe 849,697 mm = origen en unidades / 1e6, SIN unidad: la fórmula da 850,5 (0,803 mm más)", K, {"aux:e": 850500000.0}, 'o["aux:e"] / 1000000', None),
    ("importe 849,697 mm = origen en unidades / 1e6: la fórmula da 851,0 (control: fuera de 1e-9 × origen)", K, {"aux:e": 851000000.0}, 'o["aux:e"] / 1000000', "mm"),
]
# Caso realista: Análisis!C55 (acciones, en millones) = emitidas − propias, como en los tres registros reales de la 4.14 (allí los
# auxiliares llevan escala 1e-06); aquí los mismos auxiliares en ACCIONES (escala 1) y la división en la fórmula
K_ACC = "Análisis!C55"
vC55 = inst["celdas"][K_ACC]
EMI = 46500000.0
PRO = round(EMI - vC55 * 1e6, 0)
print("C55 del libro:", vC55, "| emitidas", EMI, "| propias (exactas)", PRO)
CASOS += [
    ("C55 = (emitidas − propias) / 1e6 con los auxiliares en acciones: cifras EXACTAS (control positivo)", K_ACC, {"aux:emi": EMI, "aux:pro": PRO}, '(o["aux:emi"] - o["aux:pro"]) / 1000000', None),
    ("C55 ídem con 40.000 acciones propias de MENOS en el origen (la fórmula da 0,04 M más)", K_ACC, {"aux:emi": EMI, "aux:pro": PRO - 40000.0}, '(o["aux:emi"] - o["aux:pro"]) / 1000000', None),
    ("C55 ídem con 60.000 acciones de menos (control: fuera de 1e-9 × origen)", K_ACC, {"aux:emi": EMI, "aux:pro": PRO - 60000.0}, '(o["aux:emi"] - o["aux:pro"]) / 1000000', None),
]
for _, _, vals, _, _ in CASOS:
    for v in vals.values():
        pagina_de(v)
REG = fx.REG
BASE_F = copy.deepcopy(ent(REG, K)["fuente"])

for rotulo, celda, vals, formula, unidad in CASOS:
    def cambio(g, celda=celda, vals=vals, formula=formula, unidad=unidad):
        for n, v in vals.items():
            g["entradas"].append(aux(n, v))
        e = ent(g, celda); e["fuente"] = {}
        e.update(clase="derivado", derivacion=dict({"origenes": list(vals), "formula": formula, "conciliacion": "x"}, **({"unidad": unidad} if unidad else {})))
    r = con(cambio, resellar=True)
    o = {n: v for n, v in vals.items()}
    res = VE._eval_formula(formula, o)
    print(f"[{rotulo}] modelo {inst['celdas'][celda]!r} · fórmula {res!r} · |dif| {abs(res - inst['celdas'][celda]):.6g} · 1e-9 × mayor origen = {1e-9 * max(abs(x) for x in vals.values()):.6g}")
    print(f"      {resumen(r, celda, 330)}")
fx.limpiar()
