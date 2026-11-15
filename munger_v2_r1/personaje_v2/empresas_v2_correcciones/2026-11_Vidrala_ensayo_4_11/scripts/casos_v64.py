#!/usr/bin/env python3
"""Casos de prueba de la V6.4 experimental (encargo 4.11 §8): entradas, no fórmulas.

Cada caso es {id, base, config, entradas, referencia, nota}:
  - base: "4.6.1" (libro de referencia histórica, el de las réplicas 4.7.1 y 4.8.1) o "4.10.1" (piloto con base 2025);
  - config: {celda de «Configuración V6.4»: valor} (vacío = modo heredado);
  - entradas: cambios en otras celdas de entrada (p. ej. palancas de un caso sintético);
  - referencia: valores esperados de una réplica anterior identificada (archivo fuente), o None.
Lo usan la batería (personaje_v2/pruebas/test_integracion_v64.py), el generador de libros (generar_libros_casos.py) y la réplica
independiente (replica_independiente_v64.py). Los valores numéricos de entrada son los completos de los archivos fuente:
T1 y M1 de …_4_7_1/financiero/matriz.json (t_rec, m_rec); circulante comercial del balance de 2025 (CF_2025, pág. 2–3); cartera de
clientes de la nota de intangibles 2024–2025 (…_4_8/scripts/analisis_pm1.py: CL25 4,492; VNC 21,858; CL24 4,921; 2021–2023 = 0).
"""
H = "Configuración V6.4!"
CORR = "personaje_v2/empresas_v2_correcciones"
BASES = {"4.6.1": f"{CORR}/2026-11_Vidrala_ensayo_4_6_1/Vidrala/Vidrala_v63_evaluada.xlsx",
         "4.10.1": f"{CORR}/2026-11_Vidrala_ensayo_4_10_1/Vidrala/Vidrala_v63_evaluada.xlsx"}
T1 = 0.220541332769837        # 4.7.1 matriz.json t_rec
M1 = 0.18546672136199518      # 4.7.1 matriz.json m_rec
T2 = 67.320 / 276.661         # 4.7.1 «T2 adversa»: tipo efectivo de 2025 (gasto 67,320 ÷ resultado antes de impuestos 276,661, CF_2025)
EST = {"H": "H · hueco (crédito de la inversión para crecer)", "S": "S · suma sin reestimar", "SR1": "SR1 · suma con S2C reestimado",
       "SR2": "SR2 · suma con S2C y ROIC reestimados", "SRF": "SRF · suma con inversión fija reestimada"}
LAM, THE = "Λ · (λ − 1) × amortización que se repone", "Θ · θ × exceso histórico medio"
R0, R1 = "R0 · simétrica (heredada)", "R1 · solo circulante; capacidad conservada"
LEGADO, P0 = "Legado · se repone con la amortización", "P0 · no se repone (explícito)"


def exp(n1=None, n2=None, regla=R1, escudo="Vinculado al tipo aplicado a NOPAT"):
    c = {"B4": "Experimental", "B28": regla, "B29": 252.454, "B30": 315.821, "B31": 352.841,
         "B32": "CF_2025 (cuentas consolidadas 2025, inglés), balance a 31-dic-2025, págs. 2–3: existencias, deudores y acreedores comerciales",
         "B36": "Sin requisito adicional", "B43": LEGADO}
    if n1 is not None:
        c.update({"B11": n1, "B12": "…_4_7_1/financiero/matriz.json (t_rec)", "B13": "2023–2025", "B14": "continuadas", "B15": "derivado de datos publicados", "B16": escudo})
    if n2 is not None:
        c.update({"B21": n2, "B22": "continuadas", "B23": "…_4_7_1/financiero/matriz.json (m_rec, media del ciclo 2020–2025)"})
    return c


def pm1(c, est, fam="L", par=1.15, anios="Plana", term="Proporcional a las ventas", cartera=True):
    c = dict(c)
    c.update({"B36": EST[est], "B37": LAM if fam == "L" else THE, "B40": anios, "B41": term,
              "B42": "ROIC × f (SR2)" if est == "SR2" else "ROIC de la fase B sin cambio"})
    c["B38" if fam == "L" else "B39"] = par
    if cartera:
        c.update(con_p0({}))
    return c


def con_p0(c):
    c = dict(c)
    c.update({"B43": P0, "B44": 4.492, "B45": 21.858, "B46": 0, "B47": 0, "B48": 0, "B49": 4.921, "B50": 4.492,
              "B51": "Nota de intangibles 2024–2025 (cartera de clientes de Vidroporto); 2021–2023 = 0 (2023: dos meses, no publicada por separado)"})
    return c


def caso(id_, base, config=None, entradas=None, referencia=None, nota=""):
    return {"id": id_, "base": base, "config": {H + k: v for k, v in (config or {}).items()}, "entradas": entradas or {}, "referencia": referencia, "nota": nota}


F471 = "…_4_7_1/financiero/matriz.json"
F481 = "…_4_8_1/financiero/rf_resultados.json"
import json as _json  # noqa: E402
import os as _os  # noqa: E402
_RAIZ = _os.path.abspath(_os.path.join(_os.path.dirname(__file__), "..", "..", "..", ".."))
_MATRIZ = {f["combinacion"]: f for f in _json.load(open(_os.path.join(_RAIZ, CORR, "2026-11_Vidrala_ensayo_4_7_1", "financiero", "matriz.json"), encoding="utf-8"))["matriz"]}
_RF = _json.load(open(_os.path.join(_RAIZ, CORR, "2026-11_Vidrala_ensayo_4_8_1", "financiero", "rf_resultados.json"), encoding="utf-8"))["rf1"]
REF_461 = {"V": [53.670420, 70.772197, 86.488762], "ponderado": 70.495154, "precio_si": 65.688087, "fuente": "4.6.1 (encargo 4.11 §8.1, seis decimales)", "tol": 1e-6}
REF_4101 = {"V": [53.659650, 72.740491, 86.443849], "ponderado": 71.664994, "precio_si": 66.520610, "fuente": "4.10.1 (encargo 4.11 §8.3, seis decimales)", "tol": 1e-6}


def r471(comb):
    """Valores COMPLETOS de la matriz de la 4.7.1 (sin redondeos)."""
    f = _MATRIZ[comb]
    return {"V": [f["V_malo"], f["V_normal"], f["V_bueno"]], "ponderado": f["ponderado"], "precio_si": f["precio_si"], "fuente": f"{F471} · {comb}", "tol": 1e-9}


def r481(clave):
    """Valores COMPLETOS de rf_resultados.json de la 4.8.1 (sin redondeos)."""
    a = _RF["alternativas"][clave]
    return {"V": list(a["V"]), "ponderado": a["ponderado"], "precio_si": a["precio_si"], "fuente": f"{F481} · rf1.alternativas[{clave}]", "tol": 1e-9}


# senda sintética del MALO para R1 con caída, recuperación por debajo del máximo y NUEVO máximo (años 8–10)
SENDA_NUEVO_MAXIMO = {"Palancas!B14": -0.005, "Análisis!B68": 0.03}

CASOS = [
    caso("her_461", "4.6.1", None, referencia=REF_461, nota="modo heredado sobre el libro 4.6.1"),
    caso("her_4101", "4.10.1", None, referencia=REF_4101, nota="modo heredado sobre el libro 4.10.1 (piloto)"),
    caso("her_461_explicito", "4.6.1", {"B4": "Heredado"}, referencia=REF_461, nota="«Heredado» escrito"),
    # N1–N3 aislados y combinados (matriz de la 4.7.1; T0 = vacío = tipo de la Historia, M0 = vacío = Palancas C8)
    caso("T1_M0_R0", "4.6.1", exp(T1, None, R0)),
    caso("T0_M1_R0", "4.6.1", exp(None, M1, R0)),
    caso("T0_M0_R1", "4.6.1", exp(None, None, R1), referencia=r471("T0·M0·R1")),
    caso("T0_M0_R0_exp", "4.6.1", exp(None, None, R0), referencia=r471("T0·M0·R0"),
         nota="experimental sin cambios efectivos (vacíos y R0): reproduce el heredado"),
    caso("T1_M1_R0", "4.6.1", exp(T1, M1, R0), referencia=r471("T1·M1·R0")),
    caso("T1_M1_R1", "4.6.1", exp(T1, M1, R1), referencia=r471("T1·M1·R1")),
    caso("T2_M1_R1", "4.6.1", exp(T2, M1, R1)),
    caso("T1_M1_R1_escudo_separado", "4.6.1", exp(T1, M1, R1, escudo="Tipo de la Historia (separado)"), nota="N1 con el escudo de la deuda al tipo de la Historia"),
    caso("N2_cero", "4.6.1", exp(T1, 0.0, R1), nota="cero válido en N2: m0 = 0, no el respaldo"),
    caso("N1_cero", "4.6.1", exp(0.0, M1, R1), nota="cero válido en N1: t = 0, no el respaldo"),
    caso("P0_solo", "4.6.1", con_p0(exp(T1, M1, R1)), referencia=r481("P0"), nota="cartera no repuesta sin requisito adicional"),
]
for e in EST:
    for fam, par, tag in (("L", 1.15, "L1.15"), ("L", 1.10, "L1.10"), ("L", 1.25, "L1.25"), ("T", 0.25, "T0.25"), ("T", 0.50, "T0.50"), ("T", 0.75, "T0.75"), ("T", 1.00, "T1.00")):
        k = f"{e}·{tag}"
        CASOS.append(caso(f"{e}_{tag}", "4.6.1", pm1(exp(T1, M1, R1), e, fam, par), referencia=r481(k),
                          nota="4.8.1 R-F1: años planos, terminal proporcional a las ventas, con P0"))
    CASOS.append(caso(f"{e}_L1.15_anios_ventas", "4.6.1", pm1(exp(T1, M1, R1), e, "L", 1.15, anios="Proporcional a las ventas"),
                      nota="convención continua: requisito ∝ ventas también en los años 1–10 (4.8.1 «Δ conv.»)"))
    CASOS.append(caso(f"{e}_L1.15_terminal_g", "4.6.1", pm1(exp(T1, M1, R1), e, "L", 1.15, term="Crece con g"), nota="terminal del requisito × (1 + g)"))
    CASOS.append(caso(f"{e}_T0.50_terminal_g_anios_ventas", "4.6.1", pm1(exp(T1, M1, R1), e, "T", 0.50, anios="Proporcional a las ventas", term="Crece con g")))
    CASOS.append(caso(f"{e}_L1.15_legado", "4.6.1", pm1(exp(T1, M1, R1), e, "L", 1.15, cartera=False), nota="sin P0 (cartera legado): Rh, D_hist y F_hist sin la cartera"))
    CASOS.append(caso(f"{e}_L1.15_nuevo_maximo", "4.6.1", pm1(exp(T1, M1, R1), e, "L", 1.15), SENDA_NUEVO_MAXIMO,
                      nota="MALO con caída (años 1–5), recuperación por debajo del máximo y nuevo máximo"))
# referencias de la «Δ conv.» de la 4.8.1 (convencion_anios_ventas)
for e in EST:
    for tag, fam, par in (("L1.15", "L", 1.15), ("T0.50", "T", 0.50)):
        cv = _RF["convencion_anios_ventas"][f"{e}·{tag}"]
        CASOS.append(caso(f"{e}_{tag}_anios_ventas_ref", "4.6.1", pm1(exp(T1, M1, R1), e, fam, par, anios="Proporcional a las ventas"),
                          referencia={"V": None, "ponderado": cv["ponderado"], "precio_si": cv["precio_si"], "fuente": f"{F481} · rf1.convencion_anios_ventas[{e}·{tag}]", "tol": 1e-9},
                          nota="4.8.1 «Δ conv.»: requisito ∝ ventas también en los años 1–10"))
CASOS += [
    caso("R1_nuevo_maximo", "4.6.1", exp(T1, M1, R1), SENDA_NUEVO_MAXIMO, nota="R1 sola con caída, recuperación y nuevo máximo"),
    caso("R0_nuevo_maximo", "4.6.1", exp(T1, M1, R0), SENDA_NUEVO_MAXIMO, nota="R0 con la misma senda (contraste)"),
    caso("SRF_L1.00", "4.6.1", pm1(exp(T1, M1, R1), "SRF", "L", 1.00), nota="Rh = 0: SRF = S"),
    caso("S_L1.00", "4.6.1", pm1(exp(T1, M1, R1), "S", "L", 1.00), nota="Rh = 0: requisito nulo"),
    caso("SR1_T0.00", "4.6.1", pm1(exp(T1, M1, R1), "SR1", "T", 0.0), nota="θ = 0: f = 1"),
    # piloto 4.10.1 (base 2025)
    caso("piloto_T1_M1_R1", "4.10.1", exp(T1, M1, R1)),
    caso("piloto_SR1_L1.15", "4.10.1", pm1(exp(T1, M1, R1), "SR1", "L", 1.15)),
    caso("piloto_H_T0.50", "4.10.1", pm1(exp(T1, M1, R1), "H", "T", 0.50)),
    caso("piloto_SRF_L1.15_legado", "4.10.1", pm1(exp(T1, M1, R1), "SRF", "L", 1.15, cartera=False)),
    # (ampliación tras la réplica independiente) R0 sin desglose del circulante: mismo valor que con desglose (R0 no lo usa para valorar)
    caso("T1_M1_R0_sin_circulante", "4.6.1", {k: v for k, v in exp(T1, M1, R0).items() if k not in ("B29", "B30", "B31", "B32")},
         nota="R0 sin existencias, deudores ni acreedores: la conciliación no separa el circulante; el valor es el de T1_M1_R0"),
]
# rechazos (configuración incompleta o incompatible): no deben calcular
RECHAZOS = [
    ("sin_N3", {"B28": None}, "N3: elige la regla"),
    ("lambda_vacio", {"B38": None}, "λ debe ser"),
    ("lambda_menor_1", {"B38": 0.95}, "λ debe ser"),
    ("theta_fuera", {"B37": THE, "B39": 1.2}, "θ debe ser"),
    ("R0_mas_PM1", {"B28": R0}, "R0 + P-M1"),
    ("modo_mal_escrito", {"B4": "experimental"}, "Modo no reconocido"),
    ("roic_incoherente", {"B42": "ROIC × f (SR2)"}, "ROIC del terminal"),
    ("N1_sin_escudo", {"B16": None}, "escudo de la deuda"),
    ("N1_sin_fuente", {"B12": None}, "faltan la fuente"),
    ("P0_sin_historia", {"B48": None}, "P0: faltan"),
    ("estructura_vacia", {"B36": None}, "P-M1: elige la estructura"),
    ("cartera_vacia", {"B43": None}, "cartera de clientes"),
    ("convencion_vacia", {"B40": None}, "convención del requisito en los años"),
    # (ampliación tras la réplica independiente) rechazos por dominio, sin recortes: bases del libro 4.6.1 (Configuración B54 = 132,948;
    # B57 D_hist = 530,009; B62 F_hist = 251,212; B63 Σ amortización que se repone = 500,209)
    ("N1_fuera_de_rango", {"B11": 1.2}, "N1: el tipo normalizado debe ser"),
    ("N2_fuera_de_rango", {"B21": 1.5}, "N2: el margen de partida debe ser"),
    ("N2_sin_procedencia", {"B23": None}, "N2: faltan el perímetro o la procedencia"),
    ("circulante_negativo", {"B29": -1.0}, "circulante comercial no pueden ser negativos"),
    ("P0_negativo", {"B44": -1.0}, "P0: los importes de la cartera no pueden ser negativos"),
    ("P0_no_se_agota", {"B45": 100.0}, "la cartera no se agota en diez años"),
    ("f_no_definido", {"B36": EST["SR1"], "B38": 3.0}, "el factor f no está definido"),           # Rh = 2 × 500,209 > D_hist
    ("f_fija_fuera", {"B36": EST["SRF"], "B38": 1.6}, "el factor de la inversión fija queda fuera"),  # Rh = 0,6 × 500,209 > F_hist
    ("cartera_supera_amortizacion", {"B44": 200.0}, "la amortización de la cartera supera la amortización total"),  # 200 > D&A₀
]
BASE_RECHAZO = pm1(exp(T1, M1, R1), "S", "L", 1.15)


def casos_rechazo():
    out = []
    for nombre, cambios, motivo in RECHAZOS:
        c = dict(BASE_RECHAZO)
        for k, v in cambios.items():
            if v is None:
                c.pop(k, None)
            else:
                c[k] = v
        out.append(caso(f"rechazo_{nombre}", "4.6.1", c, nota=f"rechazo esperado: «{motivo}»") | {"motivo_esperado": motivo})
    out.append(caso("rechazo_motor_A", "4.6.1", BASE_RECHAZO, {"Análisis!C62": "Sí"}, nota="motor A con parámetros experimentales activos") | {"motivo_esperado": "solo es aplicable al motor B"})
    return out


if __name__ == "__main__":
    print(len(CASOS), "casos ·", len(casos_rechazo()), "rechazos ·", sum(1 for c in CASOS if c["referencia"]), "con referencia")
