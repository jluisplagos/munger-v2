#!/usr/bin/env python3
"""Reinversión de Vidrala: reposición, crecimiento y circulante (entrega 4.8.1, encargo §3 R-F1 y §4 R-F2).
Solo lectura del árbol: el modelo auxiliar de la 4.8 se ejecuta SIN CAMBIOS, y sus salidas se escriben en un temporal.

Uso (desde munger_v2_r1/): python3 -I personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_8_1/scripts/analisis_reinversion_4_8_1.py [--salida DIR]
Escribe ../financiero/rf_* o DIR. Código 1 si la réplica de la 4.8 no es idéntica, si el motor de este guion no reproduce
las alternativas de la 4.8, si no se reproducen las referencias externas de R-F2 o si falla una identidad.

0. RÉPLICA. Ejecuta `…_4_8/scripts/analisis_pm1.py --salida <temporal>`, sin modificarlo. Exige:
   - código 0;
   - sus siete salidas idénticas byte a byte a las conservadas en `…_4_8/financiero/`.
   Esa ejecución reproduce a su vez la 4.7.1 sin cambios.
1. MOTOR. Una única función `valorar` reproduce las alternativas de la 4.8 que intervienen: REF, X41, P5x0, P1, P1s, P5, P6m y P0.
   La diferencia admitida es menor de 1e-9 en V, ponderado y precio de Sí.
   - Separa, en cada año y en el terminal, cuatro piezas:
     1. reposición contable (la amortización que se repone);
     2. requisito de reposición adicional (por encima de esa amortización);
     3. inversión fija para crecer (ΔV ÷ S2C − Δcirculante, o g ÷ ROIC − Δcirculante en el terminal);
     4. circulante.
   - Separa también el CRÉDITO: la parte del requisito que la estructura del hueco da por cubierta con la inversión fija para crecer.
     Es decir, la misma inversión cumpliendo las dos funciones.
2. R-F2. Aísla el crédito del cambio de convención terminal entre X41 y P5x0, sin P0 en ninguna rama. Se mantienen iguales el
   requisito de los años 1–10, los impuestos, el descuento y las demás entradas.
   - Diseño 2 × 2:
     - convención del requisito terminal: 55,555 × (1 + g), la de X41, o 55,555 × ventas₁₁ ÷ ventas₀, la de P5x0;
     - crédito: no o sí.
   - Efectos: el crédito con cada convención, la convención con y sin crédito, la interacción y el reparto de Shapley.
   - Referencias externas del encargo, a 7 decimales:
     - REF 69,2446731 / 64,2621768;
     - X41 48,6081961 / 44,0094136;
     - X41 con el mismo requisito y crédito 61,0825280 / 53,6729333;
     - P5x0 59,0350469 / 52,3123793.
3. R-F1. Estructuras para cada requisito de reposición adicional, ninguna seleccionada:
   - H: la regla del hueco de la 4.8. El crédito de toda la inversión fija neta se aplica contra el requisito. Supone que la
     inversión para crecer también repone; por ejemplo, reconstrucciones de hornos con ampliación de capacidad.
   - S: suma sin reestimar. Requisito completo más la inversión para crecer con el S2C y el ROIC de la fase B. Si el S2C de
     referencia ya contiene el exceso histórico, lo cuenta dos veces.
   - SR1: suma con el S2C reestimado. El S2C de los diez años se multiplica por f = den ÷ (den − Rh), donde:
     - den es la reinversión neta de la Historia 2021–2025 (H31:L31), el denominador de C53;
     - Rh es la parte de esa reinversión que la misma hipótesis atribuye a la reposición.
     El ROIC del terminal no cambia; el requisito sigue también en el terminal, sin crédito.
   - SR2: como SR1, pero el ROIC del terminal también se multiplica por f. La reinversión para crecer se descontamina igual en los
     diez años (ΔV ÷ S2C) y en el terminal (g ÷ ROIC).
   - SRF (auditoría interna, Y-c): la descontaminación se aplica solo a la inversión FIJA para crecer, multiplicada por 1 − Rh ÷ F,
     donde F es la inversión fija neta histórica frente a la amortización que se repone, con las adquisiciones (251,21). El circulante
     no se toca; el requisito va completo; vale en los años y en el terminal. Hace falta porque den es en un 53,6 % circulante y f
     reparte Rh también sobre él.
   - Corrección de f (Y-c): den se mide, como Rh, frente a la amortización que se repone. Es den + Σ cartera (530,01), no 520,60.
   - Variante de convención (Y-d): el requisito proporcional a las ventas también en los años 1–10, continuo con el terminal. Se da
     su efecto («Δ conv.») en cada celda.
   - Requisitos:
     - familia Λ: (λ − 1) × (amortización − cartera), con λ = 1,10 / 1,15 / 1,25. Su Rh histórico es Σ 2021–2025 de
       (λ − 1) × (amortización − cartera);
     - familia Θ: θ × el exceso medio 2021–2025 de la inversión sobre la amortización que se repone (47,76 M€/año), con
       θ = 0,25 / 0,50 / 0,75 / 1. θ es la fracción de ese exceso que fue reposición o competitividad y no crecimiento. No es un
       dato publicado (Q-E1). Su Rh es θ × 238,79.
   - P0 (cartera no repuesta) se aplica en toda la familia R-F1, como en P1 y P5 de la 4.8.
   - Convenciones del terminal, las de la 4.8:
     - familia Λ: amortización proporcional a las ventas;
     - familia Θ: requisito proporcional a las ventas.
     El efecto de la convención se cuantifica en R-F2.
4. P1s. La 4.8 lo calculó con los diez años en SR1 y el terminal en H, una combinación incoherente. Aquí se reproduce tal cual
   («P1s_4_8») y se sustituye por SR1, SR2 y SRF con λ = 1,15. Son coherentes en cuanto al crédito: no lo hay ni en los diez años ni
   en el terminal. Conservan la convención de la amortización plana en los años 1–10, como todas las estructuras; su efecto es Δ conv.
Ningún valor es una previsión, una cota, una medición del mantenimiento real ni una comparación con la cotización.
"""
import contextlib
import csv
import hashlib
import importlib.util
import io
import json
import os
import shutil
import sys
import tempfile

sys.dont_write_bytecode = True
AQUI = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CORR = os.path.dirname(AQUI)
E48 = os.path.join(CORR, "2026-11_Vidrala_ensayo_4_8")
SAL = os.path.join(AQUI, "financiero")
if "--salida" in sys.argv:
    SAL = os.path.abspath(sys.argv[sys.argv.index("--salida") + 1])
os.makedirs(SAL, exist_ok=True)
LOG = []
CONTROLES = {}


def log(s=""):
    LOG.append(s)
    print(s)


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


# ------------------------------------------------------------------ 0. réplica de la 4.8 sin cambios
SALIDAS_48 = ("pm1_alternativas.csv", "pm1_anio_a_anio.csv", "pm1_conciliacion_anual.csv", "pm1_evidencia.json", "pm1_resultados.json", "pm1_salida.txt", "pm1_segmentos.csv")
TMP = tempfile.mkdtemp(prefix="rf481_")
argv0 = sys.argv
try:
    P48 = os.path.join(E48, "scripts", "analisis_pm1.py")
    sys.argv = [P48, "--salida", TMP]
    spec = importlib.util.spec_from_file_location("pm1_48", P48)
    M = importlib.util.module_from_spec(spec)
    codigo_48 = None
    with contextlib.redirect_stdout(io.StringIO()):
        try:
            spec.loader.exec_module(M)
        except SystemExit as e:  # el guion de la 4.8 termina con sys.exit(0 si sus controles cumplen)
            codigo_48 = e.code
    IGUALES_48 = {f: sha(os.path.join(TMP, f)) == sha(os.path.join(E48, "financiero", f)) for f in SALIDAS_48}
finally:
    sys.argv = argv0
    shutil.rmtree(TMP, ignore_errors=True)
CONTROLES["replica_4_8"] = codigo_48 == 0 and all(IGUALES_48.values())
A = M.A
T1, M1, R_OP, DA25, NWC, V0, ACC, PUENTE, PROB, ESC, CL = M.T1, M.M1, M.R_OP, M.DA25, M.NWC, M.V0, M.ACC, M.PUENTE, M.PROB, M.ESC, M.CL
NOMBRES = M.NOMBRES
CART_Y = {2023: 0.0, 2024: M.CL24 / 1000.0, 2025: M.CL25 / 1000.0}

# datos de la Historia (publicados o derivados de la plantilla; clase en ORIGEN)
DV_HIST = A.VENTAS[2025] - A.VENTAS[2020]
DEN_HIST = sum(A.H.cell(31, 3 + (y - 2016)).value for y in range(2021, 2026))  # Historia!H31:L31, denominador de C53
C53 = DV_HIST / DEN_HIST
EXC_PROPIO = {y: A.CAPEX_H[y] - (A.DA_H[y] - CART_Y.get(y, 0.0)) for y in range(2021, 2026)}
EXC_PROPIO_SUMA = sum(EXC_PROPIO.values())
EXC_PROPIO_MEDIO = EXC_PROPIO_SUMA / 5
LEVEL_X41 = A.X_2025 * DA25  # 55,555: exceso de 2025 sobre la amortización total (X41 y P5x0)
# (auditoría interna de la 4.8.1, Y-c) composición del denominador de C53 y base de la inversión fija neta histórica
FILA = {"capex": 12, "da": 8, "adquisiciones": 13, "circulante": 14}
DEN_COMP = {k: sum(A.H.cell(r, 3 + (y - 2016)).value or 0.0 for y in range(2021, 2026)) for k, r in FILA.items()}
DEN_COMP["capex_menos_da"] = DEN_COMP["capex"] - DEN_COMP["da"]
CART_SUMA = sum(CART_Y.get(y, 0.0) for y in range(2021, 2026))
DEN_PROPIO = DEN_HIST + CART_SUMA  # el mismo denominador medido frente a la amortización que se repone (sin la cartera), como Rh
F_HIST = EXC_PROPIO_SUMA + DEN_COMP["adquisiciones"]  # inversión fija neta histórica frente a la amortización que se repone, con adquisiciones
ORIGEN = {
    "amortizacion_2025": "dato publicado (CF_2025; Historia fila 8)",
    "reposicion_contable": "dato publicado (amortización de 2025) llevado PLANO a los años 1–10 por convención del motor, y proporcional a las ventas en el terminal (convención); la variante «años ∝ ventas» mide el efecto de esa convención (Y-d)",
    "inversion_historica": "dato publicado (Historia fila 8, 2016–2025)",
    "den_C53": "cálculo de la plantilla con datos publicados (Historia!H31:L31; incluye adquisiciones y desinversiones)",
    "cartera_no_repuesta": "dato publicado (nota de intangibles 2024–2025) y cálculo de su agotamiento",
    "inversion_fija_para_crecer": "cálculo del modelo (ΔV ÷ S2C − Δcirculante; g ÷ ROIC − Δcirculante en el terminal) con S2C y ROIC de la fase B",
    "circulante": "cálculo del modelo (ΔV × circulante ÷ ventas de 2025, regla R1)",
    "requisito_reposicion_adicional": "hipótesis (λ o θ): no es un dato publicado",
    "credito": "consecuencia de la estructura H (hipótesis): no es una medición",
    "fcf": "cálculo: NOPAT + amortización − inversión fija bruta − Δcirculante",
}


# ------------------------------------------------------------------ 1. motor
def req_lambda(lmb, anios="plano"):
    """anios='plano': la amortización de 2025 en los diez años (convención de la 4.8); 'ventas': proporcional a las ventas de cada año,
    continua con el terminal (variante de convención, Y-d de la auditoría interna)."""
    anual = (lambda i, k, f, cl: (lmb - 1) * (DA25 - cl)) if anios == "plano" else (lambda i, k, f, cl: (lmb - 1) * (DA25 * f["ventas"] / V0 - cl))
    return {"anual": anual, "terminal": lambda i, V10, g: (lmb - 1) * DA25 * V10 * (1 + g) / V0,
            "historico": sum((lmb - 1) * (A.DA_H[y] - CART_Y.get(y, 0.0)) for y in range(2021, 2026)),
            "texto": f"(λ − 1) × (amortización − cartera), λ = {lmb:.2f}; terminal con la amortización proporcional a las ventas"}


def req_nivel(nivel, convencion, historico=None, anios="plano"):
    """convencion 'ventas': nivel × ventas₁₁ ÷ ventas₀ (P5, P5x0); 'crecimiento': nivel × (1 + g) (X41). anios='ventas': el nivel también
    proporcional a las ventas en los años 1–10 (variante de convención, Y-d)."""
    term = (lambda i, V10, g: nivel * V10 * (1 + g) / V0) if convencion == "ventas" else (lambda i, V10, g: nivel * (1 + g))
    anual = (lambda i, k, f, cl: nivel) if anios == "plano" else (lambda i, k, f, cl: nivel * f["ventas"] / V0)
    return {"anual": anual, "terminal": term, "historico": historico,
            "texto": f"nivel {nivel:.3f} M€/año; terminal × " + ("ventas₁₁ ÷ ventas₀" if convencion == "ventas" else "(1 + g)")}


def valorar(clave, req=None, estructura="H", cartera=True, f_s2c=1.0, f_roic=1.0, credito_terminal=None, x_plano_471=False, f_fija=1.0):
    """Valor por escenario con la estructura y el requisito dados. estructura:
       'H' crédito de la inversión fija para crecer contra el requisito (regla del hueco); 'S' suma (sin crédito);
       credito_terminal=None usa la misma estructura en el terminal; True/False la fuerza (solo para reproducir P1s de la 4.8).
       x_plano_471: X41 tal como la calculó la 4.7.1 (el adicional se cobra entero cada año y en el terminal).
       f_fija: multiplicador de la inversión FIJA para crecer (en los años y en el terminal), sin tocar el circulante (estructura SRF)."""
    res = {"clave": clave, "V": [], "peso_terminal": [], "filas": [], "terminal": [], "pv_anios": [], "pv_terminal": []}
    for i, (g1, m5, s2c, g, roic) in enumerate(ESC):
        e2 = (g1, m5, s2c * f_s2c, g, roic)
        V, fil = A.proyeccion(T1, M1, "circulante", e2)
        pv, filas = 0.0, []
        v_prev = V0
        for k, f in enumerate(fil):
            cl = CL[k] if cartera else 0.0
            requisito = req["anual"](i, k, f, cl) if req else 0.0
            fija = f["inversion_fija_neta"] * f_fija
            credito = min(requisito, max(0.0, fija)) if estructura == "H" else 0.0
            pagado = requisito - credito
            bruta = (DA25 - cl) + fija + pagado
            fcf = f["nopat"] + DA25 - bruta - f["delta_circulante"]
            pv += fcf / (1 + R_OP) ** f["anio"]
            filas.append({"alternativa": clave, "escenario": NOMBRES[i], "anio": f["anio"], "ventas": f["ventas"], "nopat": f["nopat"],
                          "reposicion_contable": DA25 - cl, "cartera_no_repuesta": cl, "requisito_reposicion_adicional": requisito,
                          "inversion_fija_para_crecer": fija, "credito_misma_inversion": credito, "reposicion_adicional_pagada": pagado,
                          "inversion_fija_bruta": bruta, "delta_circulante": f["delta_circulante"], "inversion_total": bruta + f["delta_circulante"],
                          "fcf": fcf, "varias_funciones": credito > 1e-12,
                          "s2c_efectivo": (f["ventas"] - v_prev) / (fija + f["delta_circulante"]) if f["ventas"] > v_prev and (fija + f["delta_circulante"]) > 0 else None})
            v_prev = f["ventas"]
        n11 = V[10] * (1 + g) * m5 * (1 - T1)
        dwc11 = V[10] * g * NWC
        fija11 = (n11 * g / (roic * f_roic) - dwc11) * f_fija
        reinv11 = fija11 + dwc11
        req11 = req["terminal"](i, V[10], g) if req else 0.0
        h_term = (estructura == "H") if credito_terminal is None else credito_terminal
        cred11 = min(req11, max(0.0, fija11)) if h_term else 0.0
        if h_term and not x_plano_471:
            pag11 = max(0.0, req11 - fija11)  # forma literal de la 4.8; coincide con req11 − min(req11, max(0, fija11)) si fija11 ≥ 0
        else:
            pag11 = req11 - cred11
        fcf11 = n11 - reinv11 - pag11
        tv = fcf11 / (R_OP - g)
        pvt = tv / (1 + R_OP) ** 10
        res["V"].append((pv + pvt - PUENTE) / ACC)
        res["peso_terminal"].append(pvt / (pv + pvt))
        res["pv_anios"].append(pv)
        res["pv_terminal"].append(pvt)
        res["filas"] += filas
        da11 = DA25 * V[10] * (1 + g) / V0
        res["terminal"].append({"alternativa": clave, "escenario": NOMBRES[i], "anio": 11, "ventas": V[10] * (1 + g), "nopat": n11,
                                "reposicion_contable": da11, "cartera_no_repuesta": 0.0, "requisito_reposicion_adicional": req11,
                                "inversion_fija_para_crecer": fija11, "credito_misma_inversion": req11 - pag11, "reposicion_adicional_pagada": pag11,
                                "inversion_fija_bruta": da11 + fija11 + pag11, "delta_circulante": dwc11, "inversion_total": da11 + fija11 + pag11 + dwc11,
                                "fcf": fcf11, "varias_funciones": (req11 - pag11) > 1e-12, "roic_terminal": roic * f_roic, "s2c_anios": s2c * f_s2c,
                                "roic_efectivo": n11 * g / reinv11 if reinv11 > 0 else None})
    res["precio_si"], res["ponderado"] = A.escalera(res["V"], PROB)
    return res


def igual(a, b):
    return all(abs(x - y) < 1e-9 for x, y in zip(a["V"], b["V"])) and abs(a["ponderado"] - b["ponderado"]) < 1e-9 and abs(a["precio_si"] - b["precio_si"]) < 1e-9


F115 = M.s2c_factor(M.LAM_C)[0]
CRUCE = {
    "REF": valorar("REF", None, "S", cartera=False),
    "P0": valorar("P0", None, "S"),
    "X41": valorar("X41", req_nivel(LEVEL_X41, "crecimiento"), "S", cartera=False, x_plano_471=True),
    "P5x0": valorar("P5x0", req_nivel(M.EXCESO_2025, "ventas"), "H", cartera=False),
    "P1": valorar("P1", req_lambda(M.LAM_C), "H"),
    "P5": valorar("P5", req_nivel(M.EXCESO_MEDIO_PROPIO, "ventas"), "H"),
    "P1s": valorar("P1s", req_lambda(M.LAM_C), "S", f_s2c=F115, credito_terminal=True),
}
CRUCE_OK = {k: igual(v, M.R[k]) for k, v in CRUCE.items()}
CONTROLES["motor_reproduce_4_8"] = all(CRUCE_OK.values())

# ------------------------------------------------------------------ 2. R-F2
X41c = valorar("X41c", req_nivel(LEVEL_X41, "crecimiento"), "H", cartera=False)
X41t = valorar("X41t", req_nivel(LEVEL_X41, "ventas"), "S", cartera=False)
RF2 = {"REF": CRUCE["REF"], "X41": CRUCE["X41"], "X41c": X41c, "X41t": X41t, "P5x0": CRUCE["P5x0"]}
REFS_EXT = {"REF": (69.2446731, 64.2621768), "X41": (48.6081961, 44.0094136), "X41c": (61.0825280, 53.6729333), "P5x0": (59.0350469, 52.3123793)}
CONTROLES["referencias_externas_RF2"] = all(round(RF2[k]["ponderado"], 7) == v[0] and round(RF2[k]["precio_si"], 7) == v[1] for k, v in REFS_EXT.items())


def efectos(campo):
    x, xc, xt, p = (RF2[k][campo] for k in ("X41", "X41c", "X41t", "P5x0"))
    ref = RF2["REF"][campo]
    cred_g, cred_v = xc - x, p - xt
    conv_sin, conv_con = xt - x, p - xc
    return {"caida_X41": x - ref, "credito_con_convencion_X41": cred_g, "credito_con_convencion_P5x0": cred_v,
            "convencion_sin_credito": conv_sin, "convencion_con_credito": conv_con, "interaccion": cred_v - cred_g,
            "shapley_credito": (cred_g + cred_v) / 2, "shapley_convencion": (conv_sin + conv_con) / 2, "P5x0_menos_X41": p - x,
            "fraccion_caida_X41_atribuida_al_credito": cred_g / (ref - x), "fraccion_4_8_retirada": 1 - (p - ref) / (x - ref)}


EF = {c: efectos(c) for c in ("ponderado", "precio_si")}
EF_ESC = {NOMBRES[i]: {k: RF2[k]["V"][i] for k in RF2} for i in range(3)}
CONTROLES["descomposicion_cierra"] = all(abs(e["shapley_credito"] + e["shapley_convencion"] - e["P5x0_menos_X41"]) < 1e-12 for e in EF.values())

# ------------------------------------------------------------------ 3. R-F1
def f_desc(rh):
    """Factor del S2C (y del ROIC en SR2). (Y-c) den se mide frente a la amortización que se repone, como Rh: den + Σ cartera."""
    return DEN_PROPIO / (DEN_PROPIO - rh)


def f_desc_primera_version(rh):
    return DEN_HIST / (DEN_HIST - rh)


REQS, REQS_V = {}, {}
for l in (1.10, 1.15, 1.25):
    REQS[f"L{l:.2f}"] = req_lambda(l)
    REQS_V[f"L{l:.2f}"] = req_lambda(l, anios="ventas")
for th in (0.25, 0.50, 0.75, 1.00):
    REQS[f"T{th:.2f}"] = req_nivel(th * EXC_PROPIO_MEDIO, "ventas", historico=th * EXC_PROPIO_SUMA)
    REQS[f"T{th:.2f}"]["texto"] = f"θ = {th:.2f} × {EXC_PROPIO_MEDIO:.2f} M€/año (exceso medio 2021–2025 sobre la amortización que se repone); terminal × ventas₁₁ ÷ ventas₀"
    REQS_V[f"T{th:.2f}"] = req_nivel(th * EXC_PROPIO_MEDIO, "ventas", historico=th * EXC_PROPIO_SUMA, anios="ventas")
ESTRUCTURAS = ("H", "S", "SR1", "SR2", "SRF")


def kw_estructura(est, rh):
    f = f_desc(rh)
    return {"H": {"estructura": "H"}, "S": {"estructura": "S"}, "SR1": {"estructura": "S", "f_s2c": f}, "SR2": {"estructura": "S", "f_s2c": f, "f_roic": f},
            "SRF": {"estructura": "S", "f_fija": 1 - rh / F_HIST}}[est]
RF1 = {"REF": CRUCE["REF"], "P0": CRUCE["P0"]}
META = {}
CONV = {}
for rk, rq in REQS.items():
    for est in ESTRUCTURAS:
        clave = f"{est}·{rk}"
        kw = kw_estructura(est, rq["historico"])
        RF1[clave] = valorar(clave, rq, **kw)
        META[clave] = {"estructura": est, "requisito": rk, "texto_requisito": rq["texto"], "Rh": rq["historico"],
                       "f": kw.get("f_s2c", 1.0), "f_fija": kw.get("f_fija", 1.0),
                       "f_primera_version": f_desc_primera_version(rq["historico"]) if est in ("SR1", "SR2") else None}
        v = valorar(clave + "·años∝ventas", REQS_V[rk], **kw)
        CONV[clave] = {"ponderado": v["ponderado"], "precio_si": v["precio_si"], "d_ponderado": v["ponderado"] - RF1[clave]["ponderado"], "d_precio_si": v["precio_si"] - RF1[clave]["precio_si"]}
RF1["P1s_4_8"] = valorar("P1s_4_8", req_lambda(M.LAM_C), "S", f_s2c=F115, credito_terminal=True)  # = P1s de la 4.8 (CRUCE["P1s"])
META["P1s_4_8"] = {"estructura": "SR1 en los años 1–10 y H en el terminal (incoherente)", "requisito": "L1.15", "texto_requisito": REQS["L1.15"]["texto"], "Rh": REQS["L1.15"]["historico"], "f": F115}
# equivalencias de nombre con la 4.8 (para leer las tablas)
EQUIV = {"H·L1.15": "P1", "H·L1.10": "P1b", "H·L1.25": "P1a", "H·T1.00": "P5", "SR1·L1.15": "P1s coherente (terminal sin crédito; ROIC sin cambio)", "SR2·L1.15": "P1s coherente (terminal sin crédito; ROIC × f)"}
for k, nombre48 in (("H·L1.15", "P1"), ("H·L1.10", "P1b"), ("H·L1.25", "P1a"), ("H·T1.00", "P5")):
    CRUCE_OK[f"{k}={nombre48}"] = igual(RF1[k], M.R[nombre48])
CONTROLES["motor_reproduce_4_8"] = all(CRUCE_OK.values())
TODAS = list(RF1.values()) + [X41c, X41t]
CONTROLES["identidad_fcf"] = all(abs(f["fcf"] - (f["nopat"] + f["reposicion_contable"] + f["cartera_no_repuesta"] - f["inversion_fija_bruta"] - f["delta_circulante"])) < 1e-9
                                 for r in TODAS for f in r["filas"]) and all(abs(t["fcf"] - (t["nopat"] - (t["inversion_fija_para_crecer"] + t["delta_circulante"]) - t["reposicion_adicional_pagada"])) < 1e-9
                                                                              for r in TODAS for t in r["terminal"])
CONTROLES["credito_solo_en_H"] = all((f["credito_misma_inversion"] == 0.0) for k, r in RF1.items() if META.get(k, {}).get("estructura") in ("S", "SR1", "SR2", "SRF") for f in r["filas"] + r["terminal"])
# (control de vigencia, V-4) SRF con Rh = 0 por la misma vía que SRF reproduce S, y la inversión fija de SRF es la de S × (1 − Rh ÷ F) fila a fila
CONTROLES["srf_con_rho_cero_es_S"] = igual(valorar("control", REQS["L1.15"], **kw_estructura("SRF", 0.0)), RF1["S·L1.15"])
CONTROLES["srf_fila_a_fila"] = all(abs(a["inversion_fija_para_crecer"] - b["inversion_fija_para_crecer"] * META[f"SRF·{rk}"]["f_fija"]) < 1e-9
                                   for rk in REQS for a, b in zip(RF1[f"SRF·{rk}"]["filas"] + RF1[f"SRF·{rk}"]["terminal"], RF1[f"S·{rk}"]["filas"] + RF1[f"S·{rk}"]["terminal"]))
# rango de cada requisito entre estructuras (sin elegir ninguna)
RANGO = {}
for rk in REQS:
    vals = {est: RF1[f"{est}·{rk}"]["ponderado"] for est in ESTRUCTURAS}
    RANGO[rk] = {"min": min(vals.values()), "max": max(vals.values()), "por_estructura": vals}

# ------------------------------------------------------------------ salidas
REFV = RF1["REF"]
log("REINVERSIÓN DE VIDRALA · reposición, crecimiento y circulante · entrega 4.8.1 (resultados condicionados de un ensayo; no comparables con el precio)")
log(f"réplica de la 4.8 sin cambios: código {codigo_48} · salidas idénticas byte a byte: {all(IGUALES_48.values())} ({sum(IGUALES_48.values())}/{len(IGUALES_48)})")
log("motor de este guion frente a la 4.8 (V, ponderado y precio de Sí, < 1e-9): " + " · ".join(f"{k} {'sí' if v else 'NO'}" for k, v in CRUCE_OK.items()))
log(f"Historia 2021–2025: ΔV 2020–2025 {DV_HIST:.3f} · reinversión neta (H31:L31) {DEN_HIST:.3f} · C53 {C53:.4f} · exceso sobre la amortización que se repone {EXC_PROPIO_SUMA:.3f} (media {EXC_PROPIO_MEDIO:.3f})")
log(f"  composición de H31:L31 2021–2025: inversión − amortización {DEN_COMP['capex_menos_da']:.3f} · adquisiciones netas {DEN_COMP['adquisiciones']:.3f} · circulante {DEN_COMP['circulante']:.3f} ({DEN_COMP['circulante'] / DEN_HIST:.1%}) · "
    f"Σ cartera {CART_SUMA:.3f} · den frente a la amortización que se repone {DEN_PROPIO:.3f} · inversión fija neta histórica (sin cartera, con adquisiciones) {F_HIST:.3f}")
log("\nR-F2 · CRÉDITO FRENTE A CONVENCIÓN TERMINAL (sin P0 en ninguna rama; requisito de los años 1–10 = 55,555 en todos)")
log(f"  {'caso':6s} {'requisito terminal':28s} {'crédito':8s} {'V MALO':>8s} {'V NORMAL':>9s} {'V BUENO':>8s} {'ponderado':>11s} {'Sí':>11s}")
DESC = {"REF": ("—", "—"), "X41": ("55,555 × (1 + g)", "no"), "X41c": ("55,555 × (1 + g)", "sí"), "X41t": ("55,555 × ventas₁₁ ÷ ventas₀", "no"), "P5x0": ("55,555 × ventas₁₁ ÷ ventas₀", "sí")}
for k, r in RF2.items():
    log(f"  {k:6s} {DESC[k][0]:28s} {DESC[k][1]:8s} {r['V'][0]:8.4f} {r['V'][1]:9.4f} {r['V'][2]:8.4f} {r['ponderado']:11.7f} {r['precio_si']:11.7f}")
log("  requisito terminal por escenario (M€): " + " · ".join(f"{NOMBRES[i]} X41 {RF2['X41']['terminal'][i]['requisito_reposicion_adicional']:.3f} / P5x0 {RF2['P5x0']['terminal'][i]['requisito_reposicion_adicional']:.3f}" for i in range(3)))
log(f"  referencias externas del encargo reproducidas a 7 decimales: {CONTROLES['referencias_externas_RF2']}")
for c, e in EF.items():
    log(f"  {c}: caída de X41 {e['caida_X41']:+.4f} · crédito con la convención de X41 {e['credito_con_convencion_X41']:+.4f} ({e['fraccion_caida_X41_atribuida_al_credito']:.2%} de la caída) · "
        f"crédito con la de P5x0 {e['credito_con_convencion_P5x0']:+.4f} · convención sin crédito {e['convencion_sin_credito']:+.4f} · con crédito {e['convencion_con_credito']:+.4f} · "
        f"interacción {e['interaccion']:+.4f} · Shapley: crédito {e['shapley_credito']:+.4f}, convención {e['shapley_convencion']:+.4f} (suman {e['P5x0_menos_X41']:+.4f}) · "
        f"cifra de la 4.8 que mezclaba las dos cosas: {e['fraccion_4_8_retirada']:.2%}")
log("\nR-F1 · CONCILIACIÓN: valor por estructura y requisito (con P0; r, probabilidades, k, caja, puente y acciones sin cambios)")
P0V = RF1["P0"]
log(f"  {'clave':12s} {'f':>6s} {'f_fija':>6s} {'V MALO':>8s} {'V NORMAL':>9s} {'V BUENO':>8s} {'ponderado':>10s} {'Δ REF':>7s} {'Δ P0':>7s} {'Sí':>7s} {'Δ REF':>7s} {'Δ conv.':>8s} {'crédito NORMAL':>15s} {'peso terminal':>20s}")
for k, r in RF1.items():
    cred = sum(f["credito_misma_inversion"] for f in r["filas"] if f["escenario"] == "NORMAL")
    mt = META.get(k, {})
    cv = CONV.get(k, {}).get("d_ponderado")
    log(f"  {k:12s} {mt.get('f', 1.0):6.3f} {mt.get('f_fija', 1.0):6.3f} {r['V'][0]:8.2f} {r['V'][1]:9.2f} {r['V'][2]:8.2f} {r['ponderado']:10.2f} {r['ponderado'] - REFV['ponderado']:+7.2f} {r['ponderado'] - P0V['ponderado']:+7.2f} "
        f"{r['precio_si']:7.2f} {r['precio_si'] - REFV['precio_si']:+7.2f} {('%+8.2f' % cv) if cv is not None else '       —'} {cred:15.1f}   " + "/".join(f"{p:.3f}" for p in r["peso_terminal"]))
log("  ROIC efectivo del terminal (g × NOPAT ÷ reinversión para crecer) en SRF, NORMAL: " + " · ".join(f"{rk} {RF1[f'SRF·{rk}']['terminal'][1]['roic_efectivo']:.3f}" for rk in REQS)
    + " (fase B: 0,110); con θ = 1 el crecimiento casi no necesita inversión fija, también a perpetuidad")
log("  Δ conv.: efecto en el ponderado de llevar el requisito proporcional a las ventas también en los años 1–10 (continuo con el terminal), en lugar de plano")
log("  rango por requisito entre las cinco estructuras (ponderado): " + " · ".join(f"{rk} {v['min']:.2f}–{v['max']:.2f}" for rk, v in RANGO.items()))
for k in ("H·L1.15", "S·L1.15", "SR1·L1.15", "SR2·L1.15", "SRF·L1.15", "P1s_4_8"):
    t = RF1[k]["terminal"][1]
    log(f"  terminal NORMAL {k}: NOPAT {t['nopat']:.2f} · fija para crecer {t['inversion_fija_para_crecer']:.2f} (ROIC de la fase B {t['roic_terminal']:.4f}; efectivo {t['roic_efectivo']:.4f}) · requisito {t['requisito_reposicion_adicional']:.2f} · crédito {t['credito_misma_inversion']:.2f} · pagado {t['reposicion_adicional_pagada']:.2f} · FCF {t['fcf']:.2f}")
log("\ncontroles: " + " · ".join(f"{k} {v}" for k, v in CONTROLES.items()))

CAMPOS = ["alternativa", "escenario", "anio", "ventas", "nopat", "reposicion_contable", "cartera_no_repuesta", "requisito_reposicion_adicional", "inversion_fija_para_crecer",
          "credito_misma_inversion", "reposicion_adicional_pagada", "inversion_fija_bruta", "delta_circulante", "inversion_total", "fcf", "varias_funciones", "roic_terminal", "s2c_anios",
          "s2c_efectivo", "roic_efectivo"]
with open(os.path.join(SAL, "rf_conciliacion_anual_y_terminal.csv"), "w", encoding="utf-8", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=CAMPOS)
    w.writeheader()
    for r in list(RF1.values()) + [X41c, X41t, CRUCE["X41"], CRUCE["P5x0"]]:
        for f in r["filas"] + r["terminal"]:
            w.writerow({c: (round(f[c], 6) if isinstance(f.get(c), float) else f.get(c)) for c in CAMPOS})
with open(os.path.join(SAL, "rf1_alternativas.csv"), "w", encoding="utf-8", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["clave", "estructura", "requisito", "f", "f_fija", "V_malo", "V_normal", "V_bueno", "ponderado", "d_ponderado", "d_ponderado_frente_a_P0", "precio_si", "d_precio_si", "d_precio_si_frente_a_P0",
                "d_ponderado_convencion_anios_ventas", "d_precio_si_convencion_anios_ventas", "peso_terminal_malo", "peso_terminal_normal", "peso_terminal_bueno", "equivalente_4_8", "requisito_texto"])
    for k, r in RF1.items():
        mt = META.get(k, {})
        cv = CONV.get(k, {})
        w.writerow([k, mt.get("estructura", "—"), mt.get("requisito", "—"), round(mt.get("f", 1.0), 6), round(mt.get("f_fija", 1.0), 6), *[round(v, 4) for v in r["V"]], round(r["ponderado"], 4), round(r["ponderado"] - REFV["ponderado"], 4),
                    round(r["ponderado"] - P0V["ponderado"], 4), round(r["precio_si"], 4), round(r["precio_si"] - REFV["precio_si"], 4), round(r["precio_si"] - P0V["precio_si"], 4),
                    round(cv["d_ponderado"], 4) if cv else "", round(cv["d_precio_si"], 4) if cv else "", *[round(p, 4) for p in r["peso_terminal"]], EQUIV.get(k, ""), mt.get("texto_requisito", "")])
with open(os.path.join(SAL, "rf2_credito_y_convencion.csv"), "w", encoding="utf-8", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["caso", "requisito_terminal", "credito", "V_malo", "V_normal", "V_bueno", "ponderado", "precio_si", "pv_anios_malo", "pv_anios_normal", "pv_anios_bueno", "pv_terminal_malo", "pv_terminal_normal", "pv_terminal_bueno"])
    for k, r in RF2.items():
        w.writerow([k, *DESC[k], *[round(v, 7) for v in r["V"]], round(r["ponderado"], 7), round(r["precio_si"], 7), *[round(v, 4) for v in r["pv_anios"]], *[round(v, 4) for v in r["pv_terminal"]]])
json.dump({"origen_de_cada_pieza": ORIGEN, "historia": {"dv_2020_2025": DV_HIST, "den_C53": DEN_HIST, "composicion_den": DEN_COMP, "suma_cartera": CART_SUMA, "den_propio": DEN_PROPIO, "inversion_fija_neta_historica": F_HIST, "C53": C53, "exceso_propio_2021_2025": EXC_PROPIO, "exceso_propio_suma": EXC_PROPIO_SUMA, "exceso_propio_medio": EXC_PROPIO_MEDIO},
           "rf2": {"casos": {k: {"V": r["V"], "ponderado": r["ponderado"], "precio_si": r["precio_si"], "pv_anios": r["pv_anios"], "pv_terminal": r["pv_terminal"]} for k, r in RF2.items()},
                   "efectos": EF, "por_escenario": EF_ESC, "referencias_externas": REFS_EXT},
           "rf1": {"alternativas": {k: {"V": r["V"], "ponderado": r["ponderado"], "precio_si": r["precio_si"], "peso_terminal": r["peso_terminal"], **META.get(k, {})} for k, r in RF1.items()},
                   "rango_por_requisito": RANGO, "equivalencias_4_8": EQUIV, "convencion_anios_ventas": CONV},
           "controles": CONTROLES, "cruce_con_la_4_8": CRUCE_OK, "replica_4_8": IGUALES_48},
          open(os.path.join(SAL, "rf_resultados.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
TODO = all(CONTROLES.values())
log(f"\nRESULTADO: {'todos los controles cumplen' if TODO else 'ALGÚN CONTROL FALLA'}")
open(os.path.join(SAL, "rf_salida.txt"), "w", encoding="utf-8").write("\n".join(LOG) + "\n")
sys.exit(0 if TODO else 1)
