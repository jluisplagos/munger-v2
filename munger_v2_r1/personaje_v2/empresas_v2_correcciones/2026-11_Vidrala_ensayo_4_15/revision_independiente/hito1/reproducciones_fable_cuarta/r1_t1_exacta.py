"""Cuarta pasada · T1 (fórmulas de los derivados con aritmética decimal exacta; comparación relativa al resultado; round de la hoja).
A · controles de la aritmética exacta y del round de la hoja (VE._eval_formula_exacta, VE._round_frac).
B · efecto lateral: la MEDIA de un número PAR de valores con 3 decimales que termina exactamente en x,xxx5. El generador del paquete
    (fase1_historia.calcular_entrada y la media de anios_fcf_base: round(sum / n, 3) con floats) y el comprobador (round de Python sobre
    el float del resultado exacto, o el round de la hoja si se declara en la fórmula) resuelven el empate de forma distinta.
    B1 estadística con el generador real del paquete; B2 un caso en una celda del universo del fixture (Historia!D6 = 778,136).
Arnés fx4.py. PV=<copia de arbol_congelado3>/personaje_v2 para comparar con el código de la tercera pasada (allí solo se ejecuta B2)."""
import copy, random, sys
import fx4 as fx
from fx4 import VE, con, ent, resumen, K, REG

inst = fx.inst
print("árbol:", fx.PV)
EXACTA = hasattr(VE, "_eval_formula_exacta")

if EXACTA:
    print("\n=== A · aritmética exacta y round de la hoja")
    for rot, formula, vals in (("120,4 − 120,4", 'o["a"] - o["b"]', {"a": 120.4, "b": 120.4}), ("0,1 + 0,2", 'o["a"] + o["b"]', {"a": 0.1, "b": 0.2}),
                               ("1e9 + 0,4 − (1e9 + 0,1)", 'o["a"] - o["b"]', {"a": 1000000000.4, "b": 1000000000.1}),
                               ("round(2,5) · round(−2,5) · round(0,125; 2) · round(2,675; 2)", 'round(o["a"]) * 1000000 + round(o["b"]) * 1000 + round(o["c"], 2) * 100 + round(o["d"], 2) / 1000',
                                {"a": 2.5, "b": -2.5, "c": 0.125, "d": 2.675}),
                               ("round(x, 1.0) (decimales como float entero)", 'round(o["a"], 1.0)', {"a": 0.25}),
                               ("round(x, 1.5) (decimales no enteros)", 'round(o["a"], 1.5)', {"a": 0.25}),
                               ("sum(a, b) (sin lista; Python lo rechazaría)", 'sum(o["a"], o["b"])', {"a": 1.5, "b": 2.5}),
                               ("abs(a, b) (el segundo argumento se ignora)", 'abs(o["a"], o["b"])', {"a": -1.5, "b": 2.5}),
                               ("x[\"b\"] sobre algo que no es o: (o[\"a\"],)[\"b\"] se evalúa como o[\"b\"]", '(o["a"],)["b"]', {"a": 1.5, "b": 2.5})):
        try:
            r = VE._eval_formula_exacta(formula, vals)
            print(f"   {rot}: {formula} → {r} = {float(r)!r} | claves según _claves_formula: {sorted(map(str, VE._claves_formula(formula)))}")
        except Exception as ex:  # noqa: BLE001
            print(f"   {rot}: {formula} → {type(ex).__name__}: {ex}")

    print("\n=== B1 · medias con el generador real (fase1_historia.calcular_entrada, operación «media», redondeo 3) frente al comprobador")
    import fase1_historia as FH  # noqa: E402
    random.seed(415)
    for n_anios in (2, 3, 4, 5, 6):
        tot = empates = rech_importe = rech_round = 0
        ejemplos = []
        for _ in range(20000):
            vals = [round(random.uniform(1, 2000), 3) for _ in range(n_anios)]
            anios = list(range(2026 - n_anios, 2026))
            cal = {"operacion": "media", "anios": anios, "terminos": [{"partida": "cfo", "signo": 1}], "redondeo": 3}
            gen = FH.calcular_entrada("C46", {"calculo": cal}, {"cfo": vals}, anios)["valor"]
            o = {f"v{i}": v for i, v in enumerate(vals)}
            formula = "(" + " + ".join(f'o["v{i}"]' for i in range(n_anios)) + f") / {n_anios}"
            ex = VE._eval_formula_exacta(formula, o)
            tot += 1
            empates += (ex * 10000) % 10 == 5
            ok_importe = VE._igual_libro(float(ex), gen)  # derivado con derivacion.unidad = «mm»
            ok_round = VE._igual_exacto(float(VE._eval_formula_exacta(f"round({formula}, 3)", o)), gen)  # round declarado en la fórmula, sin unidad
            rech_importe += not ok_importe
            rech_round += not ok_round
            if not ok_importe and len(ejemplos) < 2:
                ejemplos.append((vals, gen, float(ex), round(float(ex), 3)))
        print(f"   media de {n_anios} valores: {tot} casos · empates exactos (x,xxx5) {empates} · el valor que escribe el generador, RECHAZADO con unidad «mm»: {rech_importe} "
              f"({100 * rech_importe / tot:.1f} %) · con round(…, 3) en la fórmula: {rech_round} ({100 * rech_round / tot:.1f} %)")
        for e in ejemplos:
            print(f"      p. ej. valores {e[0]} → generador {e[1]!r} · exacto {e[2]!r} · round(float(exacto), 3) = {e[3]!r}")

print("\n=== B2 · en el registro: Historia!D6 = 778,136 como media de dos orígenes (678,210 y 878,061), con derivacion.unidad = «mm»")
KD = "Historia!D6"
VALS = {"aux:m1": 678.21, "aux:m2": 878.061}
print("   libro:", inst["celdas"][KD], "| media con floats (como el generador): (678.21 + 878.061) / 2 =", repr((678.21 + 878.061) / 2), "→ round(…, 3) =", round((678.21 + 878.061) / 2, 3))
CITA = {n: f"Partida sintética {n}: {round(v * 1000, 6):.3f}" for n, v in VALS.items()}
PAG = {n: fx.nueva_pagina(CITA[n]) for n in VALS}
REG = fx.REG
BASE_F = copy.deepcopy(ent(REG, KD)["fuente"])


def media(g, formula, unidad):
    for n, v in VALS.items():
        g["entradas"].append({"celda": n, "id": n, "ambito": "auxiliar", "uso": "origen", "material": True, "clase": "dato_publicado", "valor_modelo": v,
                              "comprobacion": dict(fx.COMPROBADA), "incidencia": None,
                              "fuente": dict(copy.deepcopy(BASE_F), pagina=PAG[n], valor_fuente=round(v * 1000, 6), cita=CITA[n])})
    e = ent(g, KD); e["fuente"] = {}
    e.update(clase="derivado", derivacion=dict({"origenes": list(VALS), "formula": formula, "conciliacion": "x"}, **({"unidad": unidad} if unidad else {})))


for formula, unidad in (('(o["aux:m1"] + o["aux:m2"]) / 2', "mm"), ('round((o["aux:m1"] + o["aux:m2"]) / 2, 3)', None), ('round((o["aux:m1"] + o["aux:m2"]) / 2, 3)', "mm"),
                        ('round(sum(o["aux:m1"], o["aux:m2"]) / 2, 3)', None)):  # sum(a, b) sin lista: Python lo rechaza; el evaluador exacto lo admite
    r = con(lambda g: media(g, formula, unidad), resellar=True)
    print(f"[{KD} = {formula} · unidad {unidad!r}]\n      {resumen(r, KD, 300)}")
fx.limpiar()
