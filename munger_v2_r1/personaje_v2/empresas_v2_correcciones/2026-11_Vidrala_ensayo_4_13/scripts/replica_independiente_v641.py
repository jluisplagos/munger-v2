#!/usr/bin/env python3
"""Réplica independiente de la valoración del motor B de las plantillas V6.4 y V6.4.1 experimentales (encargo 4.11 §8; 4.13 §7).

(4.13) Copia de `…_4_11/scripts/replica_independiente_v64.py`, que no cambia. Lo único que añade es el perímetro de la inversión de la
V6.4.1, partiendo de su definición económica (NIIF 16 completo: capex de caja + altas de derechos de uso frente a toda la D&A), no de
las fórmulas de la plantilla:
  - lee además las celdas de entrada B146 (perímetro) y B147:B152 (altas H–L y su fuente);
  - con «NIIF 16», en modo experimental y con las cinco altas, suma Σ altas a la reinversión histórica (D_hist) y al exceso histórico
    (y con él a F_hist, Rh con Θ, f y f_fija);
  - rechaza, como la comprobación 29 del libro, un perímetro no reconocido o NIIF 16 sin las cinco altas (≥ 0) o sin su fuente.
Con B146 vacío o «Caja» calcula exactamente lo mismo que la réplica de la 4.11.

Uso:
    python3 -I replica_independiente_v64.py DIR_CASOS [--json salida.json] [--txt salida.txt]

DIR_CASOS contiene `manifiesto_casos.json` y los libros recalculados `rc/<id>.xlsx`.
Código de salida: 0 si todos los casos coinciden; 1 si alguno no coincide o no puede compararse (libro ausente, recálculo
fallido según el manifiesto, o caso definido en `casos_v64.py` que el manifiesto no trae); 2 si el uso es incorrecto.
Dependencias: biblioteca estándar y openpyxl. No ejecuta LibreOffice y no escribe nada salvo los dos archivos de salida que se
le pidan (la salida legible va siempre también a la salida estándar).

QUÉ REPLICA
    La valoración por acción del motor B («operativo con deuda») en sus dos modos:
    - Heredado (V6.3): proyección a diez años con reinversión simétrica ΔV ÷ S2C y terminal NOPAT₁₁ × (1 − g ÷ ROIC).
    - Experimental (V6.4): N1 (tipo normalizado y escudo de la deuda), N2 (margen de partida manual), N3 (regla de reinversión
      R0 o R1) y P-M1 (cartera P0; estructuras H, S, SR1, SR2 y SRF; familias Λ y Θ; convenciones de los años y del terminal).
    Además calcula el valor ponderado y el precio de Sí (escalera con k = 3, acotada en el valor NORMAL).

DE QUÉ FUENTES SALE (definiciones económicas, no fórmulas de la hoja nueva)
    - `…_4_11/replica/ESPECIFICACION_REPLICA_INDEPENDIENTE.md` (entradas, modelo, validez y comparaciones).
    - 4.7.1 `analisis_n1_n3.py`: `r_op`, `proyeccion` (regla «circulante» = R1), `valor`, `escalera`.
    - 4.8.1 `analisis_reinversion_4_8_1.py`: `req_lambda`, `req_nivel`, `valorar`, `f_desc`, `kw_estructura`.
    - 4.8 `analisis_pm1.py`: agotamiento de la cartera de clientes (P0).
    - `personaje_v2/scripts/precio_de_si.py`: convención del precio de Sí (mínimo entre P* y el valor NORMAL).
    - `v6/scripts/` (V6.3 heredada): disposición de la hoja Motor y dominio de validez heredado.
    - `casos_v64.py`: definición de los casos (entradas). Solo se usa para contrastar el manifiesto.

QUÉ NO LEE (para conservar la independencia)
    - `v6/v64_experimental/scripts/` (en particular `construir_v64_experimental.py`) ni `v6/v64_experimental/referencia/*.json`.
    - Ninguna fórmula de ningún libro: todos se abren con `openpyxl.load_workbook(..., data_only=True)`.
    - De «Configuración V6.4» solo las celdas de entrada B4, B11:B16, B21:B23, B28:B32 y B36:B51; B8 (el motivo) solo se lee
      cuando hay un rechazo que comprobar.
    - De la hoja Motor, las columnas BU:DY no se leen en ningún caso (ni siquiera como valores).
    Ningún valor intermedio del libro entra en el cálculo de las filas 6–8: la réplica parte de Historia, Palancas, Análisis y de
    las celdas de entrada de «Configuración V6.4». En las filas 9–136, como pide la especificación, los parámetros C..P de cada
    fila se toman del libro y el resto se recalcula.

QUÉ COMPARA, CASO A CASO (especificación §4)
    0. entradas      las celdas de entrada del libro son las del manifiesto (y el manifiesto, el de `casos_v64.py`, si está).
    1. validez       la réplica rechaza ⇔ el libro no calcula (Análisis B78:D78 sin números y Motor D237 = «INCOMPLETO»);
                     en los casos de rechazo, «Configuración V6.4»!B8 contiene `motivo_esperado`.
    2. valores       V MALO / NORMAL / BUENO frente a Análisis B78:D78 (y Motor BK6:BK8) y ponderado frente a C83
                     (1e-9 €/acción). El precio de Sí no tiene celda en el libro: se compara con la referencia.
       parámetros    (añadido) m0, t, r operativa, puente y palancas de las filas 6–8 del Motor frente a los derivados.
       referencia    V, ponderado y precio de Sí frente a `referencia` del caso, con su tolerancia (`tol`, `tol_V`).
    3. flujos        FCF de los años 1–10 y del año 11 frente a Motor AU6:BD8 y BF6:BF8 (1e-9 relativo a las ventas).
    4. conciliación  nueve partidas de «Conciliación B» (tres bloques, años 1–10 y terminal).
    5. sensibilidad  filas 9–136 del Motor con valor en AU: valor por acción (BK, 1e-9) con los parámetros C..P de la fila.
                     Añadidos: los flujos de la fila (AU:BD y BF) y que sus parámetros comunes (V0, m0, t, puente, quiebra,
                     acciones) y la base de su tasa sean los del modelo activo derivado por la réplica.
    6. identidades   crédito nulo fuera de H; 0 ≤ crédito ≤ min(req, max(0, fija)) en H; Δcirculante de SRF = el de S;
                     Rh = 0 ⇒ SRF = S; θ = 0 ⇒ f = 1. Se comprueban en los valores del libro, en la réplica y, cuando el
                     directorio trae el caso homólogo, libro contra libro.
    Un caso «coincide» si pasan todos los grupos que le aplican. La réplica no corrige nada: informa de cada discrepancia con
    el caso, la celda, el valor del libro y el suyo.
"""
import argparse
import hashlib
import importlib.util
import json
import math
import os
import sys

sys.dont_write_bytecode = True  # no dejar .pyc en el paquete al contrastar con casos_v64.py

import openpyxl  # noqa: E402
from openpyxl.utils import get_column_letter  # noqa: E402

# ---------------------------------------------------------------------------------------------------------------- constantes
HOJA_HIS, HOJA_PAL, HOJA_ANA, HOJA_MOT = "Historia", "Palancas", "Análisis", "Motor"
HOJA_CFG, HOJA_CON = "Configuración V6.4", "Conciliación B"
CELDAS_CFG = (["B4"] + [f"B{i}" for i in range(11, 17)] + [f"B{i}" for i in range(21, 24)]
              + [f"B{i}" for i in range(28, 33)] + [f"B{i}" for i in range(36, 52)] + [f"B{i}" for i in range(146, 153)])
# (4.13) perímetros de la inversión de la V6.4.1 (texto de la lista del libro)
PER_CAJA = "Caja · capex de caja frente a toda la D&A (V6.4)"
PER_NIIF16 = "NIIF 16 · capex de caja + altas de derechos de uso frente a toda la D&A"
FILAS_HIS = (5, 6, 7, 8, 10, 12, 13, 14, 15, 22, 23, 24, 25, 26)  # Historia, columnas C..L (años 1..10)
ESCENARIOS = ("MALO", "NORMAL", "BUENO")
COLS_ESC = "BCD"
K_SI = 3.0

# textos de las opciones (especificación §3; comparación exacta, con mayúsculas y minúsculas)
MODO_HER, MODO_EXP = "Heredado", "Experimental"
MOTOR_B = "No · financiación cambia mucho"
BASE_MEDIA = "Media del ciclo"
CLASES_N1 = ("dato publicado", "derivado de datos publicados", "convención", "hipótesis")
ESCUDO_VINCULADO, ESCUDO_HISTORIA = "Vinculado al tipo aplicado a NOPAT", "Tipo de la Historia (separado)"
REGLAS = {"R0 · simétrica (heredada)": "R0", "R1 · solo circulante; capacidad conservada": "R1"}
ESTRUCTURAS = {"Sin requisito adicional": "SIN", "H · hueco (crédito de la inversión para crecer)": "H",
               "S · suma sin reestimar": "S", "SR1 · suma con S2C reestimado": "SR1",
               "SR2 · suma con S2C y ROIC reestimados": "SR2", "SRF · suma con inversión fija reestimada": "SRF"}
FAMILIAS = {"Λ · (λ − 1) × amortización que se repone": "Λ", "Θ · θ × exceso histórico medio": "Θ"}
CONV_ANIOS = {"Plana": "plana", "Proporcional a las ventas": "ventas"}
CONV_TERMINAL = {"Proporcional a las ventas": "ventas", "Crece con g": "g"}
ROIC_SR2, ROIC_SIN_CAMBIO = "ROIC × f (SR2)", "ROIC de la fase B sin cambio"
CARTERAS = {"Legado · se repone con la amortización": "legado", "P0 · no se repone (explícito)": "P0"}

# tolerancias (especificación §4)
TOL_VALOR = 1e-9      # €/acción: valores, ponderado y BK de las filas 9–136
TOL_REL_FLUJO = 1e-9  # relativa a la escala de las ventas (V0): flujos y partidas de la conciliación
TOL_PARAM = 1e-12     # parámetros de las filas 6–8 (relativa a max(1, |x|))

# disposición de la hoja Motor (V6.3 heredada: v6/scripts/V6.1/build_v6.py)
FILAS_ESC = (6, 7, 8)
FILAS_SENS = range(9, 137)
COL_C, COL_P = 3, 16
COL_AU, COL_BD, COL_BF, COL_BK = 47, 56, 58, 63
FILA_V35 = 237
# disposición de «Conciliación B» (especificación §4.4)
BLOQUES_CON = (5, 35, 65)
PARTIDAS_CON = ((2, "ventas"), (3, "pico"), (5, "nopat"), (7, "cartera"), (9, "requisito"), (10, "fija"), (11, "credito"),
                (13, "dcirc"), (17, "fcf"))
NOMBRE_PARTIDA = {"ventas": "ventas", "pico": "máximo conservado", "nopat": "NOPAT", "cartera": "cartera", "requisito": "requisito",
                  "fija": "fija para crecer", "credito": "crédito", "dcirc": "Δcirculante", "fcf": "FCF del motor"}
MAX_DISCREPANCIAS_POR_GRUPO = 12
LADOS = ("libro", "réplica")   # nombres por defecto de los dos valores de una comparación (claves «libro» y «replica» del JSON)


# ------------------------------------------------------------------------------------------------------------------ utilidades
def es_num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)


def vacio(x):
    return x is None or (isinstance(x, str) and x == "")


def hay_texto(x):
    """Documentación obligatoria «no vacía»: algo distinto de vacío o de solo espacios."""
    return x is not None and str(x).strip() != ""


def n0(x):
    """Vacío o texto cuenta como 0 (convención heredada de la hoja: N())."""
    return float(x) if es_num(x) else 0.0


def abrir(ruta):
    """Único punto de apertura de libros: SIEMPRE valores (data_only=True), nunca fórmulas."""
    return openpyxl.load_workbook(ruta, data_only=True)


def celda(col, fila):
    return f"{get_column_letter(col)}{fila}"


# -------------------------------------------------------------------------------------------------------- lectura de entradas
def leer_entradas(wb):
    """Entradas del caso (especificación §2): valores de Historia, Palancas, Análisis y celdas de entrada de la configuración."""
    H, P, A, K = wb[HOJA_HIS], wb[HOJA_PAL], wb[HOJA_ANA], wb[HOJA_CFG]
    his = {f: [H.cell(f, c).value for c in range(3, 13)] for f in FILAS_HIS}
    pal = {"C8": P["C8"].value,
           "g1": [P[f"{c}14"].value for c in COLS_ESC], "m_obj": [P[f"{c}15"].value for c in COLS_ESC],
           "s2c": [P[f"{c}16"].value for c in COLS_ESC], "roic": [P[f"{c}18"].value for c in COLS_ESC],
           "C22": P["C22"].value, "C23": P["C23"].value}
    ana = {"g": [A[f"{c}68"].value for c in COLS_ESC], "prob": [A[f"{c}69"].value for c in COLS_ESC],
           "C41": A["C41"].value, "C55": A["C55"].value, "C56": A["C56"].value, "C62": A["C62"].value}
    cfg = {c: K[c].value for c in CELDAS_CFG}
    return {"his": his, "pal": pal, "ana": ana, "cfg": cfg}


def leer_entradas_del_caso(wb, caso):
    """Valor que tiene en el libro cada celda de `entradas` del caso (solo Historia, Palancas y Análisis: celdas de datos)."""
    out = {}
    for clave in caso.get("entradas", {}):
        hoja, _, cel = clave.partition("!")
        out[clave] = wb[hoja][cel].value if hoja in (HOJA_HIS, HOJA_PAL, HOJA_ANA) else "(hoja que la réplica no lee como entrada)"
    return out


def huella(ent, sin_celdas=()):
    """Tupla canónica de las entradas leídas, sin las celdas de configuración indicadas (para emparejar casos homólogos)."""
    def f(x):
        return float(x) if es_num(x) else x
    his = tuple((k, tuple(f(v) for v in ent["his"][k])) for k in FILAS_HIS)
    pal = tuple((k, tuple(f(x) for x in v) if isinstance(v, list) else f(v)) for k, v in sorted(ent["pal"].items()))
    ana = tuple((k, tuple(f(x) for x in v) if isinstance(v, list) else f(v)) for k, v in sorted(ent["ana"].items()))
    cfg = tuple((c, f(ent["cfg"][c])) for c in CELDAS_CFG if c not in sin_celdas)
    return (his, pal, ana, cfg)


# ----------------------------------------------------------------------------------------------- derivados de la Historia (§2)
def derivar(ent):
    """Derivados heredados: V0, m0, t de la Historia, deuda, coste de la deuda, puente y bases de los años H..L.
    Devuelve (dict, lista de faltas). Las faltas son datos heredados sin los que el motor B no puede calcular."""
    his, pal, ana = ent["his"], ent["pal"], ent["ana"]
    faltas = []
    ventas, ebit = his[6], his[7]
    V0 = ventas[9]
    if not es_num(V0):
        faltas.append("Historia L6 (ventas del último año) no es un número")
    margenes = [e / v for v, e in zip(ventas, ebit) if es_num(v) and es_num(e) and v != 0]
    m_ultimo = (ebit[9] / ventas[9]) if es_num(ventas[9]) and es_num(ebit[9]) and ventas[9] != 0 else None
    m_medio = (sum(margenes) / len(margenes)) if margenes else None
    m0 = m_medio if pal["C8"] == BASE_MEDIA else m_ultimo   # vacío u otro texto: como «Último año»
    if m0 is None:
        faltas.append("no hay margen de partida heredado (Historia filas 6 y 7)")
    tipos = [x for x in his[10][5:10] if es_num(x)]
    t_hist = (sum(tipos) / len(tipos)) if tipos else None
    if t_hist is None:
        faltas.append("no hay tipo impositivo en Historia H10:L10")
    K22, K23, L22, L23, L24, L25, L26, L15 = his[22][8], his[23][8], his[22][9], his[23][9], his[24][9], his[25][9], his[26][9], his[15][9]
    if not (es_num(L22) or es_num(L23)):
        faltas.append("falta la deuda del último año (Historia L22:L23)")
    D = n0(L22) + n0(L23)
    deuda_media = (n0(K22) + n0(K23) + n0(L22) + n0(L23)) / 2
    i_deuda = (L15 / deuda_media) if es_num(L15) and deuda_media > 0 else None
    if not (es_num(L25) and es_num(L26)):
        faltas.append("faltan pensiones o minoritarios del último año (Historia L25, L26)")
        puente = None
    else:
        puente = D + (max(0.0, L25) + L26) - n0(L24)
    r, E, N = ana["C56"], ana["C41"], ana["C55"]
    for nombre, x in (("Análisis C56 (r)", r), ("Análisis C55 (acciones)", N)):
        if not es_num(x):
            faltas.append(f"{nombre} no es un número")
    if D != 0 and not (es_num(E) and E > 0 and i_deuda is not None):
        faltas.append("no se puede calcular la r operativa (Análisis C41, Historia L15, L22, L23)")
    p_q, rec = pal["C22"], pal["C23"]
    if not vacio(p_q) and not (es_num(p_q) and 0 <= p_q <= 1):
        faltas.append("probabilidad de quiebra fuera de [0, 1] (Palancas C22)")
    if not vacio(rec) and not (es_num(rec) and rec >= 0):
        faltas.append("recuperación si quiebra no válida (Palancas C23)")
    # bases históricas de los cinco últimos años (H..L)
    idx = range(5, 10)
    capex, da, adq, circ = his[12], his[8], his[13], his[14]
    completas = all(es_num(capex[k]) and es_num(da[k]) for k in idx)
    bases = {"completas": completas, "da0": da[9] if es_num(da[9]) else None}
    if completas:
        bases.update({"sum_reinv": sum(capex[k] - da[k] + n0(circ[k]) + n0(adq[k]) for k in idx),
                      "sum_exceso": sum(capex[k] - da[k] for k in idx),
                      "sum_adq": sum(n0(adq[k]) for k in idx),
                      "sum_da": sum(da[k] for k in idx)})
    return ({"V0": V0, "m0": m0, "m_ultimo": m_ultimo, "m_medio": m_medio, "t_hist": t_hist, "D": D, "i": i_deuda,
             "puente": puente, "r": r, "E": E, "N": N, "p": n0(p_q), "rec": n0(rec), "bases": bases}, faltas)


def r_operativa(r, E, i_deuda, tau_escudo, D):
    """r_op = (r·E + i·(1 − τ_escudo)·D) ÷ (E + D); sin deuda, r."""
    if D == 0:
        return r
    return (r * E + i_deuda * (1 - tau_escudo) * D) / (E + D)


# ------------------------------------------------------------------------------------------- modo, validez y modelo (§3.2–3.3)
def construir_modelo(ent):
    """Devuelve (modelo, motivos, fuera_de_alcance). Con motivos no vacíos la réplica RECHAZA el caso (no calcula)."""
    cfg, ana = ent["cfg"], ent["ana"]
    motivos = []

    def rechazar(clave, texto):
        motivos.append({"clave": clave, "texto": texto})

    b4 = cfg["B4"]
    if vacio(b4) or b4 == MODO_HER:
        modo = MODO_HER
    elif b4 == MODO_EXP:
        modo = MODO_EXP
    else:
        rechazar("modo", f"B4 = {b4!r}: modo no reconocido (solo «Heredado», «Experimental» o vacío)")
        return None, motivos, None
    es_motor_b = ana["C62"] == MOTOR_B
    if modo == MODO_HER and not es_motor_b:
        return None, [], f"modo heredado con un motor distinto de B (Análisis C62 = {ana['C62']!r}): fuera del alcance de la réplica"
    if modo == MODO_EXP and not es_motor_b:
        rechazar("motor", f"el modo experimental solo es aplicable al motor B (Análisis C62 = {ana['C62']!r})")
        return None, motivos, None
    der, faltas = derivar(ent)
    for f in faltas:
        rechazar("heredado", f)
    if motivos:
        return None, motivos, None
    V0, bases = der["V0"], der["bases"]
    mod = {"modo": modo, "t": der["t_hist"], "tau_escudo": der["t_hist"], "m0": der["m0"], "origen_t": "Historia", "origen_m0": "Palancas C8",
           "regla": "R0", "nwc": 0.0, "estructura": "SIN", "familia": None, "lam": None, "theta": None, "conv_anios": None,
           "conv_terminal": None, "cartera": "legado", "cl": [0.0] * 10, "da0": bases["da0"], "exceso_medio": None, "rh": 0.0,
           "f": 1.0, "f_fija": 1.0, "d_hist": None, "f_hist": None, "exceso_acumulado": None, "sum_amort_repone": None}
    if modo == MODO_EXP:
        # --- N1 · tipo normalizado y escudo de la deuda
        b11 = cfg["B11"]
        if not vacio(b11):
            if not (es_num(b11) and 0 <= b11 < 1):
                rechazar("N1", f"B11 = {b11!r}: el tipo normalizado debe ser un número en [0, 1)")
            else:
                mod["t"], mod["origen_t"] = float(b11), "B11"
            if not all(hay_texto(cfg[c]) for c in ("B12", "B13", "B14")):
                rechazar("N1", "faltan la fuente, el período o el perímetro del tipo normalizado (B12:B14)")
            if cfg["B15"] not in CLASES_N1:
                rechazar("N1", f"B15 = {cfg['B15']!r}: falta la clase del tipo normalizado o no es una de las cuatro admitidas")
            if cfg["B16"] == ESCUDO_VINCULADO:
                mod["tau_escudo"] = mod["t"]
            elif cfg["B16"] == ESCUDO_HISTORIA:
                mod["tau_escudo"] = der["t_hist"]
            else:
                rechazar("N1", f"B16 = {cfg['B16']!r}: falta el tratamiento del escudo de la deuda (vinculado o tipo de la Historia)")
        # --- N2 · margen de partida manual
        b21 = cfg["B21"]
        if not vacio(b21):
            if not (es_num(b21) and -1 < b21 < 1):
                rechazar("N2", f"B21 = {b21!r}: el margen de partida debe ser un número en (−1, 1)")
            else:
                mod["m0"], mod["origen_m0"] = float(b21), "B21"
            if not (hay_texto(cfg["B22"]) and hay_texto(cfg["B23"])):
                rechazar("N2", "faltan el perímetro o la fuente del margen de partida (B22, B23)")
        # --- N3 · regla de reinversión y circulante
        regla = REGLAS.get(cfg["B28"]) if isinstance(cfg["B28"], str) else None
        trio = [cfg["B29"], cfg["B30"], cfg["B31"]]
        if regla is None:
            rechazar("N3", f"B28 = {cfg['B28']!r}: falta la regla de reinversión (R0 o R1)")
        else:
            mod["regla"] = regla
            if regla == "R1":
                if not all(es_num(x) and x >= 0 for x in trio):
                    rechazar("N3", "R1 exige existencias, deudores y acreedores comerciales (B29:B31) numéricos y ≥ 0")
                else:
                    mod["nwc"] = (trio[0] + trio[1] - trio[2]) / V0
            elif all(es_num(x) for x in trio):   # R0: solo presentación; sin los tres datos, NWC = 0
                mod["nwc"] = (trio[0] + trio[1] - trio[2]) / V0
        # --- P-M1 · estructura y cartera
        est = ESTRUCTURAS.get(cfg["B36"]) if isinstance(cfg["B36"], str) else None
        cart = CARTERAS.get(cfg["B43"]) if isinstance(cfg["B43"], str) else None
        if est is None:
            rechazar("P-M1", f"B36 = {cfg['B36']!r}: falta la estructura (o «Sin requisito adicional»)")
        if cart is None:
            rechazar("P-M1", f"B43 = {cfg['B43']!r}: falta el tratamiento de la cartera de clientes (legado o P0)")
        if regla == "R0" and ((est is not None and est != "SIN") or cart == "P0"):
            rechazar("P-M1", "R0 + P-M1 no está especificado: las estructuras de reposición y la cartera P0 exigen R1")
        elif est is not None and cart is not None and regla is not None:
            mod["estructura"], mod["cartera"] = est, cart
            cla = vnc = None
            sum_cart = 0.0
            if cart == "P0":
                cla, vnc, hist_cart = cfg["B44"], cfg["B45"], [cfg[f"B{i}"] for i in range(46, 51)]
                if not (all(es_num(x) and x >= 0 for x in (cla, vnc)) and all(es_num(x) and x >= 0 for x in hist_cart)):
                    rechazar("P0", "faltan la amortización anual (B44), el valor neto (B45) o la amortización histórica de la cartera "
                                   "(B46:B50, cinco años con 0 explícito), o alguno es negativo")
                    cla = vnc = None
                elif vnc > 10 * cla:
                    rechazar("P0", f"el valor neto de la cartera ({vnc}) supera diez años de su amortización anual ({cla})")
                    cla = vnc = None
                else:
                    mod["cl"] = [min(cla, max(0.0, vnc - cla * (k - 1))) for k in range(1, 11)]
                    sum_cart = float(sum(hist_cart))
            if est != "SIN":
                fam = FAMILIAS.get(cfg["B37"]) if isinstance(cfg["B37"], str) else None
                parametro_ok = False
                if fam is None:
                    rechazar("P-M1", f"B37 = {cfg['B37']!r}: falta la familia del requisito (Λ o Θ)")
                elif fam == "Λ":
                    if not (es_num(cfg["B38"]) and cfg["B38"] >= 1):
                        rechazar("P-M1", f"B38 = {cfg['B38']!r}: λ debe ser un número ≥ 1")
                    else:
                        mod["lam"], parametro_ok = float(cfg["B38"]), True
                else:
                    if not (es_num(cfg["B39"]) and 0 <= cfg["B39"] <= 1):
                        rechazar("P-M1", f"B39 = {cfg['B39']!r}: θ debe ser un número entre 0 y 1")
                    else:
                        mod["theta"], parametro_ok = float(cfg["B39"]), True
                mod["familia"] = fam
                ca = CONV_ANIOS.get(cfg["B40"]) if isinstance(cfg["B40"], str) else None
                ct = CONV_TERMINAL.get(cfg["B41"]) if isinstance(cfg["B41"], str) else None
                if ca is None:
                    rechazar("P-M1", f"B40 = {cfg['B40']!r}: falta la convención del requisito en los años 1–10")
                if ct is None:
                    rechazar("P-M1", f"B41 = {cfg['B41']!r}: falta la convención del requisito en el terminal")
                mod["conv_anios"], mod["conv_terminal"] = ca, ct
                if cfg["B42"] != (ROIC_SR2 if est == "SR2" else ROIC_SIN_CAMBIO):
                    rechazar("P-M1", f"B42 = {cfg['B42']!r}: el ROIC del terminal debe ser «× f» en SR2 y «sin cambio» en las demás")
                # (4.13) perímetro de la inversión de la V6.4.1
                per = cfg.get("B146")
                altas = [cfg.get(f"B{i}") for i in range(147, 152)]
                sum_altas = 0.0
                if not vacio(per) and per not in (PER_CAJA, PER_NIIF16):
                    rechazar("perímetro", f"B146 = {per!r}: perímetro de la inversión no reconocido")
                elif per == PER_NIIF16:
                    if not (all(es_num(x) and x >= 0 for x in altas) and hay_texto(cfg.get("B152"))):
                        rechazar("perímetro", "NIIF 16 sin las cinco altas de derechos de uso (≥ 0) o sin su fuente (B147:B152)")
                    else:
                        sum_altas = float(sum(altas))
                if not bases["completas"] or bases["da0"] is None:
                    rechazar("P-M1", "bases históricas incompletas en los cinco años H..L (Historia filas 12 y 8, y con ellas la 31)")
                elif fam is not None and parametro_ok and not (cart == "P0" and cla is None):
                    da0 = bases["da0"]
                    d_hist = bases["sum_reinv"] + sum_cart + sum_altas  # (4.13) + altas con NIIF 16
                    exc_acum = bases["sum_exceso"] + sum_cart + sum_altas
                    exc_medio = exc_acum / 5
                    f_hist = exc_acum + bases["sum_adq"]
                    sum_rep = bases["sum_da"] - sum_cart
                    if fam == "Λ":
                        rh, req_cte = (mod["lam"] - 1) * sum_rep, (mod["lam"] - 1) * da0
                    else:
                        rh, req_cte = mod["theta"] * exc_acum, mod["theta"] * exc_medio
                    mod.update({"d_hist": d_hist, "exceso_acumulado": exc_acum, "exceso_medio": exc_medio, "f_hist": f_hist,
                                "sum_amort_repone": sum_rep, "rh": rh})
                    if req_cte < 0:
                        rechazar("P-M1", f"el requisito a ventas constantes es negativo ({req_cte})")
                    if fam == "Λ" and cart == "P0" and cla > da0:
                        rechazar("P-M1", "Λ con P0: la amortización anual de la cartera (B44) supera la amortización del último año")
                    if est in ("SR1", "SR2"):
                        if not (d_hist > 0 and d_hist - rh > 0):
                            rechazar("P-M1", f"f no está definido: D_hist = {d_hist}, D_hist − Rh = {d_hist - rh} (deben ser > 0)")
                        else:
                            mod["f"] = d_hist / (d_hist - rh)
                    if est == "SRF":
                        if not (f_hist > 0 and 1 - rh / f_hist >= 0):
                            rechazar("P-M1", f"f_fija no está definido: F_hist = {f_hist}, Rh = {rh} (F_hist > 0 y f_fija ≥ 0)")
                        else:
                            mod["f_fija"] = 1 - rh / f_hist
    if not all(es_num(x) and x >= 0 for x in ana["prob"]):
        rechazar("heredado", "probabilidades de los escenarios no numéricas o negativas (Análisis B69:D69)")
    if motivos:
        return None, motivos, None
    mod["r_op"] = r_operativa(der["r"], der["E"], der["i"], mod["tau_escudo"], der["D"])
    mod["der"] = der
    # dominio heredado del motor (V6.3): r_op > g, ROIC > 0, ROIC > g, V0 > 0, S2C > 0, acciones > 0
    pal = ent["pal"]
    for j, esc in enumerate(ESCENARIOS):
        g1, mo, s2c, ro, g = pal["g1"][j], pal["m_obj"][j], pal["s2c"][j], pal["roic"][j], ana["g"][j]
        if not all(es_num(x) for x in (g1, mo, s2c, ro, g)):
            rechazar("heredado", f"{esc}: faltan palancas (Palancas filas 14–18) o g para siempre (Análisis fila 68)")
        elif not (mod["r_op"] > g and ro > 0 and ro > g and V0 > 0 and s2c > 0 and der["N"] > 0):
            rechazar("heredado", f"{esc}: fuera del dominio heredado (r_op > g, ROIC > max(0, g), V0 > 0, S2C > 0, acciones > 0)")
    if motivos:
        return None, motivos, None
    return mod, [], None


def describir(mod):
    if mod["modo"] == MODO_HER:
        return "Heredado"
    partes = ["Exp", f"t={mod['t']:.4f}" + ("" if mod["origen_t"] == "Historia" else (" vinc." if mod["tau_escudo"] == mod["t"] else " escudo Hist.")),
              f"m0={mod['m0']:.4f}", mod["regla"]]
    if mod["estructura"] != "SIN":
        par = f"λ={mod['lam']:g}" if mod["familia"] == "Λ" else f"θ={mod['theta']:g}"
        partes.append(f"{mod['estructura']} {par} años {'planos' if mod['conv_anios'] == 'plana' else '∝ventas'} term. {'∝ventas' if mod['conv_terminal'] == 'ventas' else '×(1+g)'}")
    if mod["cartera"] == "P0":
        partes.append("P0")
    return " · ".join(partes)


# --------------------------------------------------------------------------------------------------------- proyección (§3.1, 3.3)
def proyectar(par, mod):
    """Proyección de una fila del motor B. par: V0, m0, g1, m_obj, s2c, g, roic, r_op, t, ajuste (= −puente), p, rec, N.
    Devuelve las series de los años 1–10 y del terminal (posición 10 de cada lista) y el valor por acción."""
    V0, m0, g1, m_obj, s2c, g, roic = par["V0"], par["m0"], par["g1"], par["m_obj"], par["s2c"], par["g"], par["roic"]
    r_op, t = par["r_op"], par["t"]
    regla, nwc, est = mod["regla"], mod["nwc"], mod["estructura"]
    f = mod["f"] if est in ("SR1", "SR2") else 1.0
    f_fija = mod["f_fija"] if est == "SRF" else 1.0
    s2c_ef = s2c * f
    roic_ef = roic * (f if est == "SR2" else 1.0)
    V = [V0]
    for k in range(1, 11):
        gk = g1 if k <= 5 else g1 - (g1 - g) * (k - 5) / 5
        V.append(V[-1] * (1 + gk))
    s = {x: [] for x in ("ventas", "pico", "margen", "nopat", "cartera", "requisito", "fija", "credito", "dcirc", "fcf")}
    for k in range(1, 11):
        mk = m0 + (m_obj - m0) * min(k, 5) / 5
        nopat = V[k] * mk * (1 - t)
        dv = V[k] - V[k - 1]
        pico = max(V[:k])
        dcirc = dv * nwc
        cl = req = cred = 0.0
        if regla == "R0":                                   # simétrica (heredada): reinversión = ΔV ÷ S2C en las dos direcciones
            reinversion = dv / s2c
            fija = reinversion - dcirc                      # presentación: el resto de la reinversión es inversión fija neta
            fcf = nopat - reinversion
        else:                                               # R1: solo circulante; la capacidad se conserva hasta el máximo de ventas
            fija = max(0.0, V[k] - pico) * (1 / s2c_ef - nwc) * f_fija
            cl = mod["cl"][k - 1]
            if est != "SIN":
                a = 1.0 if mod["conv_anios"] == "plana" else V[k] / V0
                req = (mod["lam"] - 1) * (mod["da0"] * a - cl) if mod["familia"] == "Λ" else mod["theta"] * mod["exceso_medio"] * a
                if est == "H":
                    cred = min(req, max(0.0, fija))
            fcf = nopat + cl - fija - dcirc - req + cred
        for nombre, x in (("ventas", V[k]), ("pico", pico), ("margen", mk), ("nopat", nopat), ("cartera", cl), ("requisito", req),
                          ("fija", fija), ("credito", cred), ("dcirc", dcirc), ("fcf", fcf)):
            s[nombre].append(x)
    # terminal (año 11)
    v11 = V[10] * (1 + g)
    nopat11 = v11 * m_obj * (1 - t)
    dcirc11 = V[10] * g * nwc
    req11 = cred11 = 0.0
    if regla == "R0":
        fcf11 = nopat11 * (1 - g / roic)
        fija11 = nopat11 * g / roic - dcirc11
    else:
        fija11 = (nopat11 * g / roic_ef - dcirc11) * f_fija
        if est != "SIN":
            b = V[10] * (1 + g) / V0 if mod["conv_terminal"] == "ventas" else (1 + g)
            req11 = (mod["lam"] - 1) * mod["da0"] * b if mod["familia"] == "Λ" else mod["theta"] * mod["exceso_medio"] * b
            if est == "H":
                cred11 = min(req11, max(0.0, fija11))
        fcf11 = nopat11 - fija11 - dcirc11 - req11 + cred11
    for nombre, x in (("ventas", v11), ("pico", max(V)), ("margen", m_obj), ("nopat", nopat11), ("cartera", 0.0), ("requisito", req11),
                      ("fija", fija11), ("credito", cred11), ("dcirc", dcirc11), ("fcf", fcf11)):
        s[nombre].append(x)
    vp_anios = sum(s["fcf"][k - 1] / (1 + r_op) ** k for k in range(1, 11))
    vp_terminal = fcf11 / (r_op - g) / (1 + r_op) ** 10
    total = vp_anios + vp_terminal + par["ajuste"]
    s["valor"] = ((1 - par["p"]) * total + par["p"] * par["rec"]) / par["N"]
    s["vp_anios"], s["vp_terminal"] = vp_anios, vp_terminal
    return s


def parametros_escenario(ent, mod, j):
    der, pal, ana = mod["der"], ent["pal"], ent["ana"]
    return {"V0": der["V0"], "m0": mod["m0"], "g1": pal["g1"][j], "m_obj": pal["m_obj"][j], "s2c": pal["s2c"][j], "g": ana["g"][j],
            "roic": pal["roic"][j], "r_op": mod["r_op"], "t": mod["t"], "ajuste": -der["puente"], "p": der["p"], "rec": der["rec"],
            "N": der["N"]}


# ----------------------------------------------------------------------------------------------------- precio de Sí (§3.1)
def p_estrella(V, p, k=K_SI):
    """Mayor precio P con G(P) ≥ k·L(P), donde G(P) = Σ p·max(V − P, 0) y L(P) = Σ p·max(P − V, 0).
    h(P) = G(P) − k·L(P) es continua, lineal a tramos y no creciente, con h(mín V) ≥ 0 ≥ h(máx V): se localiza el último
    tramo entre valores consecutivos en el que h pasa de ≥ 0 a < 0 y se resuelve en él exactamente (interpolación lineal)."""
    pares = sorted(zip(V, p))
    nodos = [v for v, _ in pares]

    def h(P):
        return sum(q * max(v - P, 0.0) for v, q in pares) - k * sum(q * max(P - v, 0.0) for v, q in pares)

    mejor = nodos[0]
    for a, b in zip(nodos, nodos[1:]):
        ha, hb = h(a), h(b)
        if ha >= 0 and hb >= 0:
            mejor = b
        elif ha >= 0 > hb:
            mejor = a + (b - a) * ha / (ha - hb)
    return mejor


def precio_de_si(V, p, k=K_SI):
    """Convención de `precio_de_si.py` y de la escalera de la 4.7.1: precio de Sí = min(P*, valor NORMAL)."""
    pe = p_estrella(V, p, k)
    G = sum(q * max(v - pe, 0.0) for v, q in zip(V, p))
    L = sum(q * max(pe - v, 0.0) for v, q in zip(V, p))
    return {"P_estrella": pe, "precio_si": min(pe, V[1]), "tope_normal_aplicado": pe > V[1], "G": G, "L": L,
            "valores_ordenados": V[0] <= V[1] <= V[2]}


# --------------------------------------------------------------------------------------------------------- cálculo de un caso
def calcular(ent):
    """Réplica completa de un caso a partir de sus entradas. No usa ningún valor calculado del libro."""
    mod, motivos, fuera = construir_modelo(ent)
    if mod is None:
        return {"modelo": None, "motivos": motivos, "fuera_de_alcance": fuera}
    esc = [proyectar(parametros_escenario(ent, mod, j), mod) for j in range(3)]
    V = [e["valor"] for e in esc]
    prob = ent["ana"]["prob"]
    res = {"modelo": mod, "motivos": [], "fuera_de_alcance": None, "escenarios": esc, "V": V,
           "parametros": [parametros_escenario(ent, mod, j) for j in range(3)]}
    res["ponderado"] = sum(q * v for q, v in zip(prob, V))
    res.update(precio_de_si(V, prob))
    return res


# ----------------------------------------------------------------------------------------------------------- comparaciones
class Grupo:
    """Acumula las comparaciones de un grupo: cuántas, la diferencia máxima, dónde, y las que superan la tolerancia."""

    def __init__(self):
        self.n, self.dif_max, self.donde, self.n_fallos, self.fallos, self.notas, self.aplica = 0, None, None, 0, [], [], True
        self.extra = {}

    def comparar(self, donde, libro, replica, tol, lados=LADOS):
        """Comparación numérica |libro − réplica| ≤ tol. Un valor no numérico en cualquiera de los dos lados es una discrepancia.
        `lados` nombra los dos valores cuando no son «libro» y «réplica» (referencia frente a réplica, libro frente a libro…)."""
        self.n += 1
        if not (es_num(libro) and es_num(replica)):
            self._fallo(donde, libro, replica, None, tol, None, lados)
            return False
        d = abs(libro - replica)
        if self.dif_max is None or d > self.dif_max:
            self.dif_max, self.donde = d, donde
        if d > tol:
            self._fallo(donde, libro, replica, d, tol, None, lados)
            return False
        return True

    def exigir(self, condicion, donde, libro=None, replica=None, nota=None, lados=LADOS):
        """Comprobación lógica (sin diferencia numérica): cuenta como comparación y, si no se cumple, como discrepancia."""
        self.n += 1
        if not condicion:
            self._fallo(donde, libro, replica, None, None, nota, lados)
        return bool(condicion)

    def _fallo(self, donde, libro, replica, d, tol, nota=None, lados=LADOS):
        self.n_fallos += 1
        if len(self.fallos) < MAX_DISCREPANCIAS_POR_GRUPO:
            self.fallos.append({"celda": donde, "lados": list(lados), "libro": libro, "replica": replica, "diferencia": d, "tolerancia": tol, "nota": nota})

    def no_aplica(self, nota):
        self.aplica = False
        self.notas.append(nota)

    @property
    def pasa(self):
        return self.n_fallos == 0

    def a_dict(self):
        d = {"aplica": self.aplica, "pasa": self.pasa if self.aplica else None, "comparaciones": self.n, "dif_max": self.dif_max,
             "donde_dif_max": self.donde, "n_discrepancias": self.n_fallos, "discrepancias": self.fallos, "notas": self.notas}
        d.update(self.extra)
        return d


def leer_salidas(wb, con_motivo):
    """Valores calculados del libro que se comparan. Nunca fórmulas; del Motor no se leen las columnas BU:DY."""
    A, M, C = wb[HOJA_ANA], wb[HOJA_MOT], wb[HOJA_CON]
    sal = {"V": [A[f"{c}78"].value for c in COLS_ESC], "C83": A["C83"].value, "A237": M.cell(FILA_V35, 1).value, "D237": M.cell(FILA_V35, 4).value}
    filas = {}
    for r in list(FILAS_ESC) + list(FILAS_SENS):
        filas[r] = {"etiqueta": M.cell(r, 1).value, "motor": M.cell(r, 2).value,
                    "par": [M.cell(r, c).value for c in range(COL_C, COL_P + 1)],            # C..P
                    "fcf": [M.cell(r, c).value for c in range(COL_AU, COL_BD + 1)] + [M.cell(r, COL_BF).value],
                    "bk": M.cell(r, COL_BK).value}
    sal["filas"] = filas
    sal["con"] = {b: {nombre: [C.cell(b + d, c).value for c in range(2, 13)] for d, nombre in PARTIDAS_CON} for b in BLOQUES_CON}
    sal["B8"] = wb[HOJA_CFG]["B8"].value if con_motivo else None
    return sal


def par_de_fila(fila):
    """Parámetros C..P de una fila del Motor: C V0, D m0, E g1, F m_obj, G S2C, H g, I ROIC, J r, K t, (L f), M ajuste, N p, O rec, P N."""
    c = fila["par"]
    return {"V0": c[0], "m0": c[1], "g1": c[2], "m_obj": c[3], "s2c": c[4], "g": c[5], "roic": c[6], "r_op": c[7], "t": c[8],
            "f": c[9], "ajuste": c[10], "p": c[11], "rec": c[12], "N": c[13]}


ORDEN_PAR = ("V0", "m0", "g1", "m_obj", "s2c", "g", "roic", "r_op", "t", "f", "ajuste", "p", "rec", "N")
PAR_COMUNES = ("V0", "m0", "t", "ajuste", "p", "rec", "N")   # iguales en todas las filas del Motor (diseño heredado V6.3)
PASO_TASA = 0.0025                                            # paso del deslizador de la tasa en la fila ESTUDIO (heredado)
DESPLAZAMIENTOS_TASA = (-8, -4, 0, 4, 8)                      # filas 12–136: la tasa se desplaza 0, ±0,01 o ±0,02 (heredado)


def comparar_caso(caso, ent, rep, sal, definicion, entradas_libro):
    """Aplica las comparaciones 0–5 de un caso (las identidades cruzadas se añaden después). Devuelve dict de Grupo."""
    g = {k: Grupo() for k in ("entradas", "validez", "valores", "parametros", "referencia", "flujos", "conciliacion", "sensibilidad", "identidades")}
    # 0 · entradas: libro = manifiesto (= casos_v64.py)
    man = {k.split("!", 1)[1]: v for k, v in caso.get("config", {}).items() if k.startswith(HOJA_CFG + "!")}
    for c in CELDAS_CFG:
        a, b = ent["cfg"][c], man.get(c)
        igual = (a == b) or (es_num(a) and es_num(b) and abs(a - b) <= 1e-15 * max(1.0, abs(b)))
        g["entradas"].exigir(igual, f"{HOJA_CFG}!{c}", a, b, "celda de entrada distinta de la del manifiesto", ("libro", "manifiesto"))
    for k in man:
        g["entradas"].exigir(k in CELDAS_CFG, f"{HOJA_CFG}!{k}", None, man[k], "el manifiesto escribe una celda que no es de entrada", ("libro", "manifiesto"))
    for k, v in caso.get("entradas", {}).items():
        leido = entradas_libro.get(k)
        g["entradas"].exigir(leido == v or (es_num(leido) and es_num(v) and abs(leido - v) <= 1e-15 * max(1.0, abs(v))), k, leido, v,
                             "entrada del caso distinta en el libro", ("libro", "manifiesto"))
    if definicion is not None:
        for campo in ("base", "config", "entradas", "referencia", "motivo_esperado"):
            a, b = caso.get(campo), definicion.get(campo)
            if isinstance(a, dict) and isinstance(b, dict):   # se nombra la clave que difiere, no el diccionario entero
                for k in sorted(set(a) | set(b)):
                    g["entradas"].exigir(a.get(k) == b.get(k), f"casos_v64.py · {campo} · {k}", a.get(k), b.get(k),
                                         "el manifiesto no coincide con la definición del caso", ("manifiesto", "casos_v64.py"))
            else:
                g["entradas"].exigir(a == b, f"casos_v64.py · {campo}", a, b, "el manifiesto no coincide con la definición del caso", ("manifiesto", "casos_v64.py"))
    # 1 · validez
    v = g["validez"]
    libro_calcula = all(es_num(x) for x in sal["V"])
    rechaza = rep["modelo"] is None
    v.extra.update({"replica_rechaza": rechaza, "libro_calcula": libro_calcula, "motivos_replica": [m["texto"] for m in rep["motivos"]],
                    "motivo_libro": sal["B8"], "motivo_esperado": caso.get("motivo_esperado")})
    v.exigir(sal["A237"] == "V35", f"{HOJA_MOT}!A{FILA_V35}", sal["A237"], "V35", "la fila 237 del Motor no es la regla V35")
    if rep["fuera_de_alcance"]:
        v.exigir(False, "alcance", None, None, rep["fuera_de_alcance"])
    elif rechaza:
        for c, x in zip(COLS_ESC, sal["V"]):
            v.exigir(not es_num(x), f"{HOJA_ANA}!{c}78", x, "(rechazado)", "la réplica rechaza el caso y el libro calcula un valor")
        v.exigir(not es_num(sal["C83"]), f"{HOJA_ANA}!C83", sal["C83"], "(rechazado)", "la réplica rechaza el caso y el libro da un ponderado")
        v.exigir(sal["D237"] == "INCOMPLETO", f"{HOJA_MOT}!D{FILA_V35}", sal["D237"], "INCOMPLETO", "la réplica rechaza el caso y V35 no dice INCOMPLETO")
        con_numero = [r for r, f in sal["filas"].items() if any(es_num(x) for x in f["fcf"]) or es_num(f["bk"])]
        v.exigir(not con_numero, f"{HOJA_MOT}!AU:BK", f"filas con números: {con_numero[:6]}", "(sin números)", "la réplica rechaza el caso y el Motor tiene flujos o valores")
    else:
        for c, x in zip(COLS_ESC, sal["V"]):
            v.exigir(es_num(x), f"{HOJA_ANA}!{c}78", x, "(valor)", "la réplica calcula y el libro no")
        v.exigir(es_num(sal["C83"]), f"{HOJA_ANA}!C83", sal["C83"], "(valor)", "la réplica calcula y el libro no da ponderado")
        v.exigir(sal["D237"] != "INCOMPLETO", f"{HOJA_MOT}!D{FILA_V35}", sal["D237"], "≠ INCOMPLETO", "la réplica calcula y V35 dice INCOMPLETO")
    if caso.get("motivo_esperado") is not None:
        v.exigir(rechaza, "réplica", None, None, "caso de rechazo que la réplica no rechaza")
        v.exigir(isinstance(sal["B8"], str) and caso["motivo_esperado"] in sal["B8"], f"{HOJA_CFG}!B8", sal["B8"], caso["motivo_esperado"],
                 "el motivo del libro no contiene el motivo esperado")
    resto = ("valores", "parametros", "referencia", "flujos", "conciliacion", "sensibilidad", "identidades")
    if rechaza or not libro_calcula:
        for k in resto:
            g[k].no_aplica("caso rechazado: no hay valores que comparar" if rechaza and not libro_calcula else "validez discordante: no se compara")
        return g
    mod, esc = rep["modelo"], rep["escenarios"]
    V0 = mod["der"]["V0"]
    tol_f = TOL_REL_FLUJO * max(1.0, abs(V0))
    # 2 · valores
    for j, c in enumerate(COLS_ESC):
        g["valores"].comparar(f"{HOJA_ANA}!{c}78 (V {ESCENARIOS[j]})", sal["V"][j], rep["V"][j], TOL_VALOR)
    g["valores"].comparar(f"{HOJA_ANA}!C83 (ponderado)", sal["C83"], rep["ponderado"], TOL_VALOR)
    for j, r in enumerate(FILAS_ESC):
        g["valores"].comparar(f"{HOJA_MOT}!BK{r} (V {ESCENARIOS[j]})", sal["filas"][r]["bk"], rep["V"][j], TOL_VALOR)
    # 2b · parámetros de las filas 6–8 (añadido)
    for j, r in enumerate(FILAS_ESC):
        fila, mio = par_de_fila(sal["filas"][r]), dict(rep["parametros"][j], f=0.0)
        g["parametros"].exigir(sal["filas"][r]["motor"] == "B", f"{HOJA_MOT}!B{r}", sal["filas"][r]["motor"], "B", "la fila no es del motor B")
        for i, nombre in enumerate(ORDEN_PAR):
            g["parametros"].comparar(f"{HOJA_MOT}!{celda(COL_C + i, r)} ({nombre})", fila[nombre], mio[nombre], TOL_PARAM * max(1.0, abs(mio[nombre])))
    # 2c · referencia de una réplica anterior
    ref = caso.get("referencia")
    if not ref:
        g["referencia"].no_aplica("el caso no trae referencia")
    else:
        tol, tol_v = ref.get("tol", TOL_VALOR), ref.get("tol_V", ref.get("tol", TOL_VALOR))
        g["referencia"].extra.update({"fuente": ref.get("fuente"), "tol": tol, "tol_V": tol_v})
        if ref.get("V") is not None:
            for j in range(3):
                g["referencia"].comparar(f"referencia V {ESCENARIOS[j]} frente a la réplica", ref["V"][j], rep["V"][j], tol_v, ("referencia", "réplica"))
                g["referencia"].comparar(f"referencia V {ESCENARIOS[j]} frente a {HOJA_ANA}!{COLS_ESC[j]}78", ref["V"][j], sal["V"][j], tol_v, ("referencia", "libro"))
        if ref.get("ponderado") is not None:
            g["referencia"].comparar("referencia ponderado frente a la réplica", ref["ponderado"], rep["ponderado"], tol, ("referencia", "réplica"))
            g["referencia"].comparar(f"referencia ponderado frente a {HOJA_ANA}!C83", ref["ponderado"], sal["C83"], tol, ("referencia", "libro"))
        if ref.get("precio_si") is not None:
            g["referencia"].comparar("referencia precio de Sí frente a la réplica", ref["precio_si"], rep.get("precio_si"), tol, ("referencia", "réplica"))
            g["referencia"].extra["precio_si"] = {"referencia": ref["precio_si"], "replica": rep.get("precio_si"),
                                                  "diferencia": abs(ref["precio_si"] - rep["precio_si"]) if es_num(rep.get("precio_si")) else None}
    # 3 · flujos de las filas 6–8
    for j, r in enumerate(FILAS_ESC):
        for k in range(11):
            col = COL_AU + k if k < 10 else COL_BF
            g["flujos"].comparar(f"{HOJA_MOT}!{celda(col, r)} (FCF {ESCENARIOS[j]} año {k + 1})", sal["filas"][r]["fcf"][k], esc[j]["fcf"][k], tol_f)
    g["flujos"].extra["tolerancia_absoluta"] = tol_f
    # 4 · conciliación
    for j, b in enumerate(BLOQUES_CON):
        for d, nombre in PARTIDAS_CON:
            for k in range(11):
                g["conciliacion"].comparar(f"{HOJA_CON}!{celda(2 + k, b + d)} ({NOMBRE_PARTIDA[nombre]} {ESCENARIOS[j]} {'año ' + str(k + 1) if k < 10 else 'terminal'})",
                                           sal["con"][b][nombre][k], esc[j][nombre][k], tol_f)
    g["conciliacion"].extra["tolerancia_absoluta"] = tol_f
    # 5 · filas de sensibilidad, tornado y DCF inverso (9–136 con valor en AU)
    s = g["sensibilidad"]
    n_filas, dif_fcf, donde_fcf, sin_valor = 0, 0.0, None, []
    comunes = rep["parametros"][0]   # V0, m0, t, ajuste, quiebra y acciones son los mismos en los tres escenarios
    for r in FILAS_SENS:
        fila = sal["filas"][r]
        if not es_num(fila["fcf"][0]):
            if fila["etiqueta"] is not None:
                sin_valor.append(r)
            continue
        n_filas += 1
        par = par_de_fila(fila)
        if not all(es_num(par[x]) for x in ORDEN_PAR if x != "f") or fila["motor"] != "B" or n0(par["f"]) != 0:
            s.exigir(False, f"{HOJA_MOT}!B{r}:P{r}", fila["par"], None, "parámetros de la fila no numéricos o fila que no es del motor B")
            continue
        # (añadido) los parámetros comunes de la fila son los del modelo activo —m0 (N2), t (N1), puente— y su tasa es la
        # r operativa activa (N1, escudo) más el desplazamiento heredado de la fila; así un m0, un t o una r_op heredados
        # en la tabla del DCF inverso o en el tornado no pasan inadvertidos aunque el resto de la fila se tome del libro
        for nombre in PAR_COMUNES:
            s.exigir(abs(par[nombre] - comunes[nombre]) <= TOL_PARAM * max(1.0, abs(comunes[nombre])),
                     f"{HOJA_MOT}!{celda(COL_C + ORDEN_PAR.index(nombre), r)} ({nombre}, {fila['etiqueta']})", par[nombre], comunes[nombre],
                     "parámetro común de la fila distinto del modelo activo")
        pasos = (par["r_op"] - mod["r_op"]) / PASO_TASA
        s.exigir(abs(pasos - round(pasos)) * PASO_TASA <= TOL_PARAM and (r < 12 or round(pasos) in DESPLAZAMIENTOS_TASA),
                 f"{HOJA_MOT}!J{r} (tasa, {fila['etiqueta']})", par["r_op"], mod["r_op"],
                 "la tasa de la fila no es la r operativa activa más un desplazamiento heredado (0, ±0,01, ±0,02; ESTUDIO: múltiplos de 0,0025)")
        mia = proyectar(par, mod)
        s.comparar(f"{HOJA_MOT}!BK{r} ({fila['etiqueta']})", fila["bk"], mia["valor"], TOL_VALOR)
        tol_r = TOL_REL_FLUJO * max(1.0, abs(par["V0"]))
        for k in range(11):
            col = COL_AU + k if k < 10 else COL_BF
            x, y = fila["fcf"][k], mia["fcf"][k]
            if not es_num(x) or abs(x - y) > tol_r:
                s.exigir(False, f"{HOJA_MOT}!{celda(col, r)} (FCF año {k + 1}, {fila['etiqueta']})", x, y, f"flujo de la fila fuera de tolerancia ({tol_r:.3g})")
            elif abs(x - y) > dif_fcf:
                dif_fcf, donde_fcf = abs(x - y), f"{HOJA_MOT}!{celda(col, r)}"
    s.extra.update({"filas_comparadas": n_filas, "filas_con_etiqueta_sin_valor": sin_valor, "dif_max_flujos": dif_fcf, "donde_dif_max_flujos": donde_fcf})
    s.exigir(n_filas > 0, f"{HOJA_MOT}!AU9:AU136", n_filas, "> 0", "no hay ninguna fila 9–136 con valor en AU")
    s.exigir(not sin_valor, f"{HOJA_MOT}!AU9:AU136", sin_valor[:8], "[]", "filas con etiqueta y sin valor en AU en un caso que calcula")
    # 6 · identidades propias del caso (sobre los valores del libro y sobre la réplica)
    idn = g["identidades"]
    est = mod["estructura"]
    cred_lib = [(b, k, sal["con"][b]["credito"][k]) for b in BLOQUES_CON for k in range(11)]
    if est != "H":
        idn.extra["credito_nulo_fuera_de_H"] = True
        for b, k, x in cred_lib:
            idn.exigir(es_num(x) and x == 0, f"{HOJA_CON}!{celda(2 + k, b + 11)}", x, 0.0, "crédito distinto de cero fuera de H (libro)")
        for j in range(3):
            idn.exigir(all(x == 0 for x in esc[j]["credito"]), f"réplica · crédito {ESCENARIOS[j]}", None, esc[j]["credito"], "crédito distinto de cero fuera de H (réplica)")
    else:
        idn.extra["credito_acotado_en_H"] = True
        for j, b in enumerate(BLOQUES_CON):
            for k in range(11):
                cr, rq, fj = (sal["con"][b][x][k] for x in ("credito", "requisito", "fija"))
                ok = all(es_num(x) for x in (cr, rq, fj)) and -tol_f <= cr <= min(rq, max(0.0, fj)) + tol_f
                idn.exigir(ok, f"{HOJA_CON}!{celda(2 + k, b + 11)}", cr, f"0 ≤ crédito ≤ min({rq}, max(0, {fj}))", "crédito fuera de [0, min(req, max(0, fija))] en H (libro)")
                cr, rq, fj = (esc[j][x][k] for x in ("credito", "requisito", "fija"))
                idn.exigir(0 <= cr <= min(rq, max(0.0, fj)), f"réplica · crédito {ESCENARIOS[j]} {k + 1}", None, cr, "crédito fuera de [0, min(req, max(0, fija))] en H (réplica)")
    if est != "SIN" and mod["familia"] == "Θ" and mod["theta"] == 0 and est in ("SR1", "SR2"):
        idn.extra["theta_cero_f_uno"] = mod["f"]
        idn.exigir(mod["f"] == 1.0, "réplica · f con θ = 0", None, mod["f"], "con θ = 0, f debe ser 1")
    if est == "SRF" and mod["rh"] == 0:
        idn.extra["rh_cero_f_fija_uno"] = mod["f_fija"]
        idn.exigir(mod["f_fija"] == 1.0, "réplica · f_fija con Rh = 0", None, mod["f_fija"], "con Rh = 0, f_fija debe ser 1")
    return g


def comparar_libros(nombre, id_a, sal_a, id_b, sal_b, V0, grupo, partidas=None, valores=True):
    """Identidad cruzada libro ↔ libro: mismas cifras en dos casos homólogos (valores, flujos o partidas de la conciliación)."""
    tol_f = TOL_REL_FLUJO * max(1.0, abs(V0))
    lados = (f"libro {id_a}", f"libro {id_b}")
    if valores:
        for j, c in enumerate(COLS_ESC):
            grupo.comparar(f"{nombre} · {HOJA_ANA}!{c}78", sal_a["V"][j], sal_b["V"][j], TOL_VALOR, lados)
        grupo.comparar(f"{nombre} · {HOJA_ANA}!C83", sal_a["C83"], sal_b["C83"], TOL_VALOR, lados)
        for r in FILAS_ESC:
            for k in range(11):
                col = COL_AU + k if k < 10 else COL_BF
                grupo.comparar(f"{nombre} · {HOJA_MOT}!{celda(col, r)}", sal_a["filas"][r]["fcf"][k], sal_b["filas"][r]["fcf"][k], tol_f, lados)
    for p in partidas or ():
        d = {nom: dd for dd, nom in PARTIDAS_CON}[p]
        for b in BLOQUES_CON:
            for k in range(11):
                grupo.comparar(f"{nombre} · {HOJA_CON}!{celda(2 + k, b + d)} ({NOMBRE_PARTIDA[p]})", sal_a["con"][b][p][k], sal_b["con"][b][p][k], tol_f, lados)


def variante(ent, cambios):
    """Las mismas entradas con otras celdas de configuración (para las identidades calculadas con la propia réplica)."""
    e2 = dict(ent)
    e2["cfg"] = dict(ent["cfg"])
    e2["cfg"].update(cambios)
    return e2


TEXTO_EST = {v: k for k, v in ESTRUCTURAS.items()}


def identidades_cruzadas(datos):
    """Identidades entre casos (especificación §4.6): SRF frente a S, Rh = 0 ⇒ SRF = S, θ = 0 ⇒ f = 1."""
    calculados = {i: d for i, d in datos.items() if d.get("rep") and d["rep"]["modelo"] is not None and d["grupos"]["identidades"].aplica}
    por_huella_sin_b36 = {}
    por_huella_sin_req = {}
    for i, d in calculados.items():
        por_huella_sin_b36.setdefault(huella(d["ent"], ("B36",)), []).append(i)
        por_huella_sin_req.setdefault(huella(d["ent"], tuple(f"B{k}" for k in range(36, 43))), []).append(i)
    for i, d in calculados.items():
        mod, idn, ent, rep, sal = d["rep"]["modelo"], d["grupos"]["identidades"], d["ent"], d["rep"], d["sal"]
        V0 = mod["der"]["V0"]
        tol_f = TOL_REL_FLUJO * max(1.0, abs(V0))
        if mod["estructura"] == "SRF":
            # (a) con la réplica: la variante S de las mismas entradas tiene el mismo Δcirculante, fila a fila
            rep_s = calcular(variante(ent, {"B36": TEXTO_EST["S"]}))
            ok_var = rep_s["modelo"] is not None
            idn.exigir(ok_var, "réplica · variante S", None, None, "la variante S de un caso SRF no es calculable")
            if ok_var:
                for j, b in enumerate(BLOQUES_CON):
                    for k in range(11):
                        idn.exigir(rep["escenarios"][j]["dcirc"][k] == rep_s["escenarios"][j]["dcirc"][k], f"réplica · Δcirculante SRF = S ({ESCENARIOS[j]} {k + 1})",
                                   None, rep["escenarios"][j]["dcirc"][k], "Δcirculante de SRF distinto del de S (réplica)")
                        idn.comparar(f"{HOJA_CON}!{celda(2 + k, b + 13)} (Δcirculante SRF del libro frente al de S de la réplica)", sal["con"][b]["dcirc"][k],
                                     rep_s["escenarios"][j]["dcirc"][k], tol_f, ("libro SRF", "réplica de la variante S"))
                if mod["rh"] == 0:   # Rh = 0 ⇒ SRF = S (valores y flujos)
                    for j in range(3):
                        idn.comparar(f"réplica · V {ESCENARIOS[j]} SRF = S con Rh = 0", rep["V"][j], rep_s["V"][j], 0.0, ("réplica SRF", "réplica de la variante S"))
            # (b) con los libros: el libro S homólogo, si existe
            homologos = [x for x in por_huella_sin_b36.get(huella(ent, ("B36",)), []) if calculados[x]["rep"]["modelo"]["estructura"] == "S"]
            idn.extra["libro_S_homologo"] = homologos[0] if homologos else None
            if homologos:
                otro = calculados[homologos[0]]
                comparar_libros("SRF = S", i, sal, homologos[0], otro["sal"], V0, idn, partidas=("dcirc",), valores=(mod["rh"] == 0))
                if mod["rh"] == 0:
                    idn.extra["rh_cero_SRF_igual_S"] = homologos[0]
                    comparar_libros("Rh = 0 · SRF = S", i, sal, homologos[0], otro["sal"], V0, idn, partidas=("fija", "requisito", "fcf"), valores=False)
            else:
                idn.notas.append("SRF sin libro S homólogo en el directorio: la identidad del Δcirculante se comprueba solo con la variante S de la réplica")
        if mod["estructura"] in ("SR1", "SR2") and mod["familia"] == "Θ" and mod["theta"] == 0:
            # θ = 0 ⇒ f = 1 y requisito nulo: el caso coincide con el homólogo sin requisito adicional
            rep_n = calcular(variante(ent, {"B36": TEXTO_EST["SIN"]}))
            if rep_n["modelo"] is not None:
                for j in range(3):
                    idn.comparar(f"réplica · V {ESCENARIOS[j]} con θ = 0 = sin requisito", rep["V"][j], rep_n["V"][j], 0.0, ("réplica", "réplica de la variante sin requisito"))
            homologos = [x for x in por_huella_sin_req.get(huella(ent, tuple(f"B{k}" for k in range(36, 43))), [])
                         if calculados[x]["rep"]["modelo"]["estructura"] == "SIN"]
            idn.extra["libro_sin_requisito_homologo"] = homologos[0] if homologos else None
            if homologos:
                comparar_libros("θ = 0 ⇒ f = 1 · igual que sin requisito", i, sal, homologos[0], calculados[homologos[0]]["sal"], V0, idn, partidas=("fija", "fcf"), valores=True)
            else:
                idn.notas.append("θ = 0 sin libro homólogo sin requisito: la consecuencia de f = 1 se comprueba solo con la réplica")


# --------------------------------------------------------------------------------------------------------------- definiciones
def cargar_definiciones():
    """Definición de los casos en `casos_v64.py` (junto a este guion), para contrastar el manifiesto. Opcional."""
    ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "casos_v64.py")
    if not os.path.isfile(ruta):
        return None, "casos_v64.py no está junto al guion: el manifiesto no se contrasta con la definición de los casos"
    try:
        spec = importlib.util.spec_from_file_location("casos_v64_definicion", ruta)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        casos = list(m.CASOS) + list(m.casos_rechazo())
        return {c["id"]: json.loads(json.dumps(c)) for c in casos}, None
    except Exception as e:  # noqa: BLE001  (la comprobación es auxiliar: se informa y se sigue)
        return None, f"casos_v64.py no se pudo cargar ({type(e).__name__}: {e}): el manifiesto no se contrasta"


# --------------------------------------------------------------------------------------------------------------------- informe
GRUPOS = ("entradas", "validez", "valores", "parametros", "referencia", "flujos", "conciliacion", "sensibilidad", "identidades")
TITULO = {"entradas": "0 · entradas (libro = manifiesto = casos_v64.py)", "validez": "1 · validez", "valores": "2 · valores (Análisis B78:D78, C83; Motor BK6:BK8)",
          "parametros": "2b · parámetros de las filas 6–8 (añadido)", "referencia": "2c · referencia de réplicas anteriores (V, ponderado, precio de Sí)",
          "flujos": "3 · flujos (Motor AU6:BD8 y BF6:BF8)", "conciliacion": "4 · conciliación («Conciliación B»)",
          "sensibilidad": "5 · sensibilidad, tornado y DCF inverso (Motor 9–136)", "identidades": "6 · identidades"}


def marca(gr):
    if not gr["aplica"]:
        return "—"
    return "ok" if gr["pasa"] else "FALLA"


def cifra(x, fmt="{:.1e}"):
    return "—" if x is None else fmt.format(x)


def informe_txt(res):
    L = []
    a = L.append
    global_txt = (f"RESULTADO GLOBAL: {res['n_pasan']} de {res['n_casos']} casos coinciden"
                  + (f" · {len(res['casos_definidos_sin_libro'])} casos definidos sin libro" if res["casos_definidos_sin_libro"] else "")
                  + " → " + ("TODOS COINCIDEN (código 0)" if res["todo_coincide"] else "HAY CASOS QUE NO COINCIDEN O NO SE HAN PODIDO COMPARAR (código 1)"))
    a("RÉPLICA INDEPENDIENTE · V6.4 experimental del motor B (encargo 4.11 §8)")
    a(global_txt)
    a(f"directorio de casos: {res['directorio']}")
    a(f"manifiesto: sha256 {res['manifiesto_sha256']} · plantilla {res['plantilla']} (sha256 {res['plantilla_sha256']})")
    a(f"casos: {res['n_casos']} · rechazados por la réplica: {res['n_rechazados']} · calculados: {res['n_calculados']} · con referencia: {res['n_con_referencia']}")
    a(f"tolerancias: valores y BK {TOL_VALOR:g} €/acción · flujos y conciliación {TOL_REL_FLUJO:g} × ventas de partida · parámetros {TOL_PARAM:g} · referencia: la de cada caso")
    a("libros abiertos solo con data_only=True (valores); la réplica no lee fórmulas ni las columnas BU:DY del Motor")
    for n in res["avisos"]:
        a(f"AVISO: {n}")
    a("")
    a("RESUMEN POR GRUPO (casos que pasan de los evaluados; «no aplican»: rechazos sin valores o casos sin referencia)")
    for k in GRUPOS:
        r = res["resumen"][k]
        linea = f"  {TITULO[k]}: pasan {r['pasan']} de {r['evaluados']} ({r['no_aplica']} no aplican) · comparaciones {r['comparaciones']}"
        if r["dif_max"] is not None:
            linea += f" · dif. máx. {r['dif_max']:.3e} ({r['caso_dif_max']} · {r['donde_dif_max']})"
        a(linea)
        if r["fallan"]:
            a(f"      NO PASAN: {', '.join(r['fallan'])}")
    a(f"  flujos de las filas 9–136 (añadido al grupo 5): dif. máx. {cifra(res['dif_max_flujos_sens'], '{:.3e}')} · filas comparadas {res['filas_sens_comparadas']}")
    a("")
    a("CASOS  (ent = entradas · val = validez · V = valores · par = parámetros · ref = referencia · fcf = flujos · con = conciliación · sens = filas 9–136 · id = identidades;")
    a("        «—» = no aplica; dif = diferencia máxima libro − réplica: V y BK en €/acción, fcf y con en millones)")
    a(f"  {'caso':36s} {'ent':5s} {'val':5s} {'V':5s} {'par':5s} {'ref':5s} {'fcf':5s} {'con':5s} {'sens':5s} {'id':5s} {'dif V':>8s} {'dif fcf':>8s} {'dif con':>8s} {'dif BK':>8s}  resultado")
    for c in res["casos"]:
        gr = c["grupos"]
        a(f"  {c['id']:36s} " + " ".join(f"{marca(gr[k]):5s}" for k in GRUPOS)
          + f" {cifra(gr['valores']['dif_max']):>8s} {cifra(gr['flujos']['dif_max']):>8s} {cifra(gr['conciliacion']['dif_max']):>8s} {cifra(gr['sensibilidad']['dif_max']):>8s}"
          + f"  {'COINCIDE' if c['pasa'] else 'NO COINCIDE'}")
    a("")
    a("MODELO ACTIVO DE CADA CASO (según la réplica, a partir de las celdas de entrada)")
    for c in res["casos"]:
        a(f"  {c['id']:36s} {c['modelo']}")
    a("")
    a("VALORES DE LA RÉPLICA (€/acción)")
    a(f"  {'caso':36s} {'V MALO':>12s} {'V NORMAL':>12s} {'V BUENO':>12s} {'ponderado':>12s} {'precio de Sí':>13s} {'P*':>12s} tope NORMAL")
    for c in res["casos"]:
        if c["replica"]:
            r = c["replica"]
            a(f"  {c['id']:36s} {r['V'][0]:12.6f} {r['V'][1]:12.6f} {r['V'][2]:12.6f} {r['ponderado']:12.6f} {r['precio_si']:13.6f} {r['P_estrella']:12.6f} "
              + ("sí" if r["tope_normal_aplicado"] else "no") + ("" if r["valores_ordenados"] else "  (valores desordenados: precio_de_si.py no daría escalera, error G19)"))
    a("")
    a("PRECIO DE SÍ FRENTE A LA REFERENCIA (k = 3; convención: min(P*, V NORMAL))")
    for c in res["casos"]:
        ps = c["grupos"]["referencia"].get("precio_si")
        if ps:
            a(f"  {c['id']:38s} réplica {ps['replica']:.12f} · referencia {ps['referencia']:.12f} · dif. {ps['diferencia']:.2e} · tol {c['grupos']['referencia']['tol']:g} · {c['grupos']['referencia']['fuente']}")
    a("")
    a("RECHAZOS (motivos de la réplica · motivo del libro en «Configuración V6.4»!B8 · motivo esperado)")
    for c in res["casos"]:
        v = c["grupos"]["validez"]
        if v["replica_rechaza"] or v["motivo_esperado"] is not None or not v["libro_calcula"]:
            a(f"  {c['id']}: réplica {'RECHAZA' if v['replica_rechaza'] else 'calcula'} · libro {'calcula' if v['libro_calcula'] else 'no calcula'}")
            for m in v["motivos_replica"]:
                a(f"      réplica: {m}")
            a(f"      libro B8: {v['motivo_libro']}")
            if v["motivo_esperado"] is not None:
                a(f"      esperado: «{v['motivo_esperado']}» → {'contenido en B8' if isinstance(v['motivo_libro'], str) and v['motivo_esperado'] in v['motivo_libro'] else 'NO contenido en B8'}")
    a("")
    a("IDENTIDADES")
    r = res["identidades"]
    a(f"  crédito = 0 fuera de H (años y terminal; libro y réplica): {r['credito_nulo_fuera_de_H']} casos")
    a(f"  0 ≤ crédito ≤ min(req, max(0, fija)) en H (libro y réplica): {r['credito_acotado_en_H']} casos")
    a(f"  Δcirculante de SRF = el de S, fila a fila: {r['srf_total']} casos SRF · con libro S homólogo {r['srf_con_libro_S']} · solo con la variante S de la réplica {r['srf_total'] - r['srf_con_libro_S']}")
    a(f"  Rh = 0 ⇒ SRF = S: {', '.join(f'{x} = {y}' for x, y in r['rh_cero']) or '(ningún caso)'}")
    a(f"  θ = 0 ⇒ f = 1: {', '.join(f'{x} (f = {f:g}; libro homólogo sin requisito: {y})' for x, f, y in r['theta_cero']) or '(ningún caso)'}")
    a("")
    a("DISCREPANCIAS")
    hay = False
    for c in res["casos"]:
        for k in GRUPOS:
            for d in c["grupos"][k]["discrepancias"]:
                hay = True
                a(f"  {c['id']} · {TITULO[k]} · {d['celda']}: {d['lados'][0]} {d['libro']!r} · {d['lados'][1]} {d['replica']!r}"
                  + (f" · dif. {d['diferencia']:.3e} > tol {d['tolerancia']:.3e}" if d["diferencia"] is not None else "") + (f" · {d['nota']}" if d.get("nota") else ""))
            extra = c["grupos"][k]["n_discrepancias"] - len(c["grupos"][k]["discrepancias"])
            if extra > 0:
                a(f"  {c['id']} · {TITULO[k]}: … y {extra} discrepancias más (no listadas)")
        if c.get("error"):
            hay = True
            a(f"  {c['id']} · ERROR: {c['error']}")
    if res["casos_definidos_sin_libro"]:
        hay = True
        a(f"  {len(res['casos_definidos_sin_libro'])} casos definidos en casos_v64.py y ausentes del manifiesto: sin libro, no comparados (lista en el AVISO de la cabecera)")
    if not hay:
        a("  (ninguna)")
    a("")
    a(global_txt)
    return "\n".join(L) + "\n"


def resumen_replica(rep):
    if rep is None or rep["modelo"] is None:
        return None
    mod = rep["modelo"]
    return {"V": rep["V"], "ponderado": rep["ponderado"], "precio_si": rep.get("precio_si"), "P_estrella": rep.get("P_estrella"),
            "tope_normal_aplicado": rep.get("tope_normal_aplicado"), "valores_ordenados": rep.get("valores_ordenados"), "G": rep.get("G"), "L": rep.get("L"),
            "fcf": [e["fcf"] for e in rep["escenarios"]], "vp_anios": [e["vp_anios"] for e in rep["escenarios"]], "vp_terminal": [e["vp_terminal"] for e in rep["escenarios"]],
            "modelo": {k: mod[k] for k in ("modo", "t", "tau_escudo", "m0", "origen_t", "origen_m0", "r_op", "regla", "nwc", "estructura", "familia", "lam", "theta",
                                           "conv_anios", "conv_terminal", "cartera", "cl", "da0", "d_hist", "exceso_acumulado", "exceso_medio", "f_hist",
                                           "sum_amort_repone", "rh", "f", "f_fija")},
            "derivados": {k: mod["der"][k] for k in ("V0", "m_ultimo", "m_medio", "t_hist", "D", "i", "puente", "r", "E", "N", "p", "rec")}}


# ------------------------------------------------------------------------------------------------------------------ principal
def main(argv=None):
    ap = argparse.ArgumentParser(description="Réplica independiente de la valoración del motor B de la V6.4 experimental (encargo 4.11 §8).")
    ap.add_argument("dir_casos", help="directorio con manifiesto_casos.json y rc/<id>.xlsx")
    ap.add_argument("--json", dest="json", help="archivo de resultados (JSON)")
    ap.add_argument("--txt", dest="txt", help="archivo de salida legible (texto)")
    args = ap.parse_args(argv)
    d = os.path.abspath(args.dir_casos)
    ruta_man = os.path.join(d, "manifiesto_casos.json")
    if not os.path.isfile(ruta_man):
        print(f"no existe {ruta_man}", file=sys.stderr)
        return 2
    man = json.load(open(ruta_man, encoding="utf-8"))
    definiciones, aviso = cargar_definiciones()
    avisos = [aviso] if aviso else []
    ids_man = [c["id"] for c in man["casos"]]
    if len(set(ids_man)) != len(ids_man):
        avisos.append("el manifiesto tiene identificadores de caso repetidos")
    sin_libro = []
    if definiciones is not None:
        sin_libro = [i for i in definiciones if i not in set(ids_man)]
        if sin_libro:
            avisos.append(f"casos definidos en casos_v64.py que no están en el manifiesto (sin libro, no comparados; cuentan como no coincidentes): {', '.join(sin_libro)}")
    datos = {}
    for caso in man["casos"]:
        i = caso["id"]
        dato = {"caso": caso, "ent": None, "rep": None, "sal": None, "grupos": None, "error": None, "sha256": None}
        datos[i] = dato
        ruta = os.path.join(d, caso.get("recalculado") or os.path.join("rc", f"{i}.xlsx"))
        try:
            if not caso.get("recalculo_ok", False):
                raise RuntimeError("el manifiesto indica que el recálculo del libro no fue correcto")
            with open(ruta, "rb") as fh:
                dato["sha256"] = hashlib.sha256(fh.read()).hexdigest()
            wb = abrir(ruta)
            dato["ent"] = leer_entradas(wb)
            entradas_libro = leer_entradas_del_caso(wb, caso)
            dato["rep"] = calcular(dato["ent"])
            con_motivo = dato["rep"]["modelo"] is None or caso.get("motivo_esperado") is not None
            dato["sal"] = leer_salidas(wb, con_motivo)
            if not con_motivo and not all(es_num(x) for x in dato["sal"]["V"]):   # el libro no calcula y la réplica sí: se informa su motivo
                dato["sal"]["B8"] = wb[HOJA_CFG]["B8"].value
            wb.close()
            definicion = None
            if definiciones is not None:
                definicion = definiciones.get(i)
                if definicion is None:
                    avisos.append(f"el caso {i} del manifiesto no está definido en casos_v64.py")
            dato["grupos"] = comparar_caso(caso, dato["ent"], dato["rep"], dato["sal"], definicion, entradas_libro)
        except Exception as e:  # noqa: BLE001  (un caso que no puede compararse cuenta como no coincidente)
            dato["error"] = f"{type(e).__name__}: {e}"
    identidades_cruzadas({i: x for i, x in datos.items() if x["grupos"] is not None})
    # ---- resultados
    casos_out, resumen = [], {k: {"evaluados": 0, "pasan": 0, "no_aplica": 0, "comparaciones": 0, "dif_max": None, "caso_dif_max": None,
                                  "donde_dif_max": None, "fallan": []} for k in GRUPOS}
    ident = {"credito_nulo_fuera_de_H": 0, "credito_acotado_en_H": 0, "srf_total": 0, "srf_con_libro_S": 0, "rh_cero": [], "theta_cero": []}
    dif_fcf_sens, filas_sens = None, 0
    for i, x in datos.items():
        caso, rep = x["caso"], x["rep"]
        if x["grupos"] is None:
            vacio_gr = Grupo()
            vacio_gr.no_aplica("caso no comparado por un error")
            grupos = {k: dict(vacio_gr.a_dict(), replica_rechaza=None, libro_calcula=None, motivos_replica=[], motivo_libro=None,
                              motivo_esperado=caso.get("motivo_esperado")) for k in GRUPOS}
            pasa = False
        else:
            grupos = {k: x["grupos"][k].a_dict() for k in GRUPOS}
            pasa = all(gr["pasa"] for gr in grupos.values() if gr["aplica"])
        for k in GRUPOS:
            gr, r = grupos[k], resumen[k]
            if not gr["aplica"]:
                r["no_aplica"] += 1
                continue
            r["evaluados"] += 1
            r["comparaciones"] += gr["comparaciones"]
            if gr["pasa"]:
                r["pasan"] += 1
            else:
                r["fallan"].append(i)
            if gr["dif_max"] is not None and (r["dif_max"] is None or gr["dif_max"] > r["dif_max"]):
                r["dif_max"], r["caso_dif_max"], r["donde_dif_max"] = gr["dif_max"], i, gr["donde_dif_max"]
        idn = grupos["identidades"]
        if idn["aplica"]:
            ident["credito_nulo_fuera_de_H"] += 1 if idn.get("credito_nulo_fuera_de_H") else 0
            ident["credito_acotado_en_H"] += 1 if idn.get("credito_acotado_en_H") else 0
            if rep["modelo"]["estructura"] == "SRF":
                ident["srf_total"] += 1
                ident["srf_con_libro_S"] += 1 if idn.get("libro_S_homologo") else 0
            if idn.get("rh_cero_SRF_igual_S"):
                ident["rh_cero"].append((i, idn["rh_cero_SRF_igual_S"]))
            if "theta_cero_f_uno" in idn:
                ident["theta_cero"].append((i, idn["theta_cero_f_uno"], idn.get("libro_sin_requisito_homologo")))
        s = grupos["sensibilidad"]
        if s["aplica"]:
            filas_sens += s.get("filas_comparadas", 0)
            if s.get("dif_max_flujos") is not None and (dif_fcf_sens is None or s["dif_max_flujos"] > dif_fcf_sens):
                dif_fcf_sens = s["dif_max_flujos"]
        casos_out.append({"id": i, "base": caso.get("base"), "libro": caso.get("recalculado"), "libro_sha256": x["sha256"], "nota": caso.get("nota"),
                          "rechazado": None if rep is None else rep["modelo"] is None,
                          "fuera_de_alcance": None if rep is None else rep["fuera_de_alcance"],
                          "modelo": "(error)" if rep is None else ("RECHAZADO" if rep["modelo"] is None else describir(rep["modelo"])),
                          "replica": resumen_replica(rep), "grupos": grupos, "pasa": pasa and x["error"] is None, "error": x["error"]})
    n_pasan = sum(1 for c in casos_out if c["pasa"])
    with open(ruta_man, "rb") as fh:
        sha_man = hashlib.sha256(fh.read()).hexdigest()
    res = {"directorio": d, "manifiesto_sha256": sha_man, "plantilla": man.get("plantilla"), "plantilla_sha256": man.get("plantilla_sha256"),
           "n_casos": len(casos_out), "casos_definidos_sin_libro": sin_libro,
           "n_rechazados": sum(1 for c in casos_out if c["rechazado"]), "n_calculados": sum(1 for c in casos_out if c["rechazado"] is False),
           "n_con_referencia": sum(1 for c in man["casos"] if c.get("referencia")), "n_pasan": n_pasan,
           "todo_coincide": n_pasan == len(casos_out) and len(casos_out) > 0 and not sin_libro,
           "tolerancias": {"valor_eur_por_accion": TOL_VALOR, "flujos_relativa_a_ventas": TOL_REL_FLUJO, "parametros": TOL_PARAM},
           "avisos": avisos, "resumen": resumen, "identidades": ident, "dif_max_flujos_sens": dif_fcf_sens, "filas_sens_comparadas": filas_sens, "casos": casos_out}
    texto = informe_txt(res)
    sys.stdout.write(texto)
    if args.txt:
        with open(args.txt, "w", encoding="utf-8") as fh:
            fh.write(texto)
    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(res, fh, ensure_ascii=False, indent=1)
            fh.write("\n")
    return 0 if res["todo_coincide"] else 1


if __name__ == "__main__":
    sys.exit(main())
