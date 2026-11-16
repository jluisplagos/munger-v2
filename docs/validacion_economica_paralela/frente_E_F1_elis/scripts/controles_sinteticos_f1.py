"""Controles sintéticos de correspondencia de caja · propuesta F1 (P1–P4 y correcciones V1–V11).

Son ejemplos de política con importes ficticios. No usan datos de Elis, no ejecutan el producto y no adoptan ninguna
definición. Cada caso compara dos cosas, calculadas por separado:
  · los flujos del motor A sintético: las ecuaciones de `motor_a`, la función con que `contraste_f1.py` replica el
    libro (crecimiento g15 en los años 1–5 y lineal hasta g∞ en los años 6–10; margen lineal de m0 a m_obj en cinco
    años; flujo_t = V_t·[m_t(1−τ) − f] − ΔV_t/S2C; terminal = V_10·(1+g∞)·[m_obj(1−τ)(1 − g∞/ROIC) − f]), más los
    términos explícitos X_t que declare el caso (E3). Sin términos explícitos coincide exactamente con `motor_a`, con
    cualquier senda de crecimiento y de margen y con impuestos (`comprobar_motor`);
  · la caja del escenario, partida a partida: EBITDA − capex de mantenimiento − pagos de arrendamiento − compras de
    cartera necesarias para mantener las ventas − inversión de transición − inversión de crecimiento.
Así se comprueba que cada desembolso se cobra una sola vez en la calibración, en los años proyectados y en el
terminal, también a crecimiento cero.

Bloques:
  · reproducción de los nueve casos de `sondas_economicas.py` de la revisión externa (1a07188);
  · P1–P4 de la respuesta (13f864f), con el ancla dada;
  · V2 y V9 (revisión dirigida, 8fcc7fd): ventana con crecimiento y ancla de S2C calculada con la fórmula de E4, en
    su versión anterior (sin excluir lo que se cobra como término explícito) y en la corregida; transición y compras
    de reposición con crecimiento; caso fiscal sintético de N1 con caja conocida; fórmula del terminal del libro
    (Convenciones V6.3 §3); guardas V-F1c que deben saltar y que no.

Convenciones del escenario, todas ficticias: sin impuestos (salvo el caso fiscal), sin circulante ni intereses de
deuda; ventas del año base 100; los costes que escalan con las ventas lo hacen en proporción constante.

Uso: python3 -I controles_sinteticos_f1.py --salida ../resultados/controles_sinteticos_f1.json
Termina con 1 si algún caso no da el resultado esperado o si el motor sintético no coincide con `motor_a`.
"""
import argparse
import importlib.util
import json
import sys
from fractions import Fraction as Fr
from pathlib import Path

_spec = importlib.util.spec_from_file_location("contraste_f1", Path(__file__).with_name("contraste_f1.py"))
_C = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_C)
motor_a = _C.motor_a

N = 10                      # años proyectados, como el motor A
V0 = Fr(100)                # ventas del año base (última de la ventana)
REVISOR = {                 # comprobaciones_sinteticas.json del revisor externo (1a07188): flujo modelizado y caja
    "arrendamiento_una_vez": (68, 68),
    "A0_doble_arrendamiento": (58, 68),
    "transicion_excluida_de_R_y_sin_linea_de_caja": (68, 61),
    "transicion_incluida_en_R": (61, 61),
    "transicion_separada_con_cargo_explicito": (61, 61),
    "adquisicion_de_reposicion_tratada_solo_como_crecimiento": (68, 59),
    "adquisicion_de_reposicion_incluida_en_R": (59, 59),
    "gasto_comercial_ya_en_EBIT_y_cargado_otro_vez_en_R": (63, 68),
    "PPA_no_monetaria_con_costes_de_reposicion_ya_cubiertos": (68, 68),
}


def num(x):
    return float(x) if x.denominator != 1 else int(x)


def senda_g(g15, g_inf):
    """Crecimiento de cada año, como motor_a: g15 en los años 1–5; de 6 a 10, lineal hasta g∞."""
    return [g15 if t <= 5 else g15 - (g15 - g_inf) * Fr(t - 5, 5) for t in range(1, N + 1)]


class Escenario:
    """Escenario ficticio. Importes por cada 100 de ventas del año base; los «por ventas» escalan con V_t."""

    def __init__(self, **k):
        self.ebitda = Fr(k.get("ebitda", 100))          # por ventas; ya descuenta el gasto comercial corriente
        self.d_propia = Fr(k.get("d_propia", 20))       # por ventas; amortización propia (= capex de mantenimiento)
        self.rou = Fr(k.get("rou", 10))                 # por ventas; amortización de derechos de uso
        self.pagos_arr = Fr(k.get("pagos_arr", 12))     # por ventas; pagos de arrendamiento (principal + interés)
        self.mant = Fr(k.get("mant", 20))               # por ventas; capex propio de mantenimiento
        self.rep_adq = Fr(k.get("rep_adq", 0))          # por ventas; compras de cartera necesarias para mantener ventas
        self.ppa_v = Fr(k.get("ppa", 0))                # PPA de la ventana (no monetaria)
        self.trans = k.get("trans", lambda t, Vt: Fr(0))  # transición del año t (t = 1..N; N+1 = terminal)
        self.trans_v = Fr(k.get("trans_v", 0))          # inversión de transición dentro del capex de la ventana
        self.s2c_real = Fr(k.get("s2c_real", 1))        # ventas adicionales por euro de inversión de crecimiento
        self.dV_v = Fr(k.get("dV_v", 0))                # aumento de ventas en la ventana (para el ancla de E4)

    # ventana de calibración. El FCF base excluye las compras de sociedades, como en la plantilla
    def inv_crec_v(self):
        return self.dV_v / self.s2c_real                # inversión de crecimiento de la ventana (propia y compras)

    def capex_ventana(self):
        return self.mant + self.trans_v + self.inv_crec_v()

    def fcf_base(self):
        return self.ebitda - self.capex_ventana() - self.pagos_arr

    def ebit_ventana(self):
        return self.ebitda - self.d_propia - self.rou - self.ppa_v

    def f(self, R):
        """f = [EBIT − (capex − R) − FCF base] ÷ ventas, con τ = 0 y sin circulante (Convenciones V6.3 §10)."""
        return (self.ebit_ventana() - (self.capex_ventana() - R) - self.fcf_base()) / V0

    def ancla_E4(self, R, fuera_del_ancla=Fr(0)):
        """C53 = ΔV ÷ Σ(capex − D_X + circulante + adquisiciones − lo que se cobra como término explícito) (E4).
        En la ventana, las compras de reposición están fuera del capex y dentro de «adquisiciones»."""
        return self.dV_v / (self.capex_ventana() - R + self.rep_adq - fuera_del_ancla)

    # caja del escenario, partida a partida
    def caja(self, t, Vt, Vprev):
        e = Vt / V0
        dV = Vt - Vprev
        return (self.ebitda * e - self.mant * e - self.pagos_arr * e - self.rep_adq * e - self.trans(t, Vt)
                - dV / self.s2c_real)


def motor_sintetico(m, f, g, s2c, roic, g_inf, extra=lambda t, Vt: Fr(0), tau=Fr(0), m_obj=None, g15=None):
    """Ecuaciones de motor_a con términos explícitos X_t (E3). g: crecimiento de los años 1–5 (o g15); de 6 a 10, lineal
    hasta g∞. m: número (con m_obj, senda lineal de cinco años, como motor_a) o función de (t, V_t)."""
    g15 = g if g15 is None else g15
    if callable(m):
        mt = m
    else:
        mo = m if m_obj is None else m_obj
        mt = lambda t, Vt: m + (mo - m) * Fr(min(t, 5), 5)   # noqa: E731
    V, prev, flujos = [], V0, []
    for t, gt in enumerate(senda_g(g15, g_inf), start=1):
        Vt = prev * (1 + gt)
        flujos.append(Vt * (mt(t, Vt) * (1 - tau) - f) - (Vt - prev) / s2c - extra(t, Vt))
        V.append(Vt)
        prev = Vt
    V11 = V[-1] * (1 + g_inf)
    term = V11 * (mt(N + 1, V11) * (1 - tau) * (1 - g_inf / roic) - f) - extra(N + 1, V11)
    return flujos, term, V


def caja_sintetica(esc, g15, g_inf):
    V, prev, cajas = [], V0, []
    for t, gt in enumerate(senda_g(g15, g_inf), start=1):
        Vt = prev * (1 + gt)
        cajas.append(esc.caja(t, Vt, prev))
        V.append(Vt)
        prev = Vt
    return cajas, esc.caja(N + 1, V[-1] * (1 + g_inf), V[-1])


def comprobar_motor():
    """Sin términos explícitos, el motor sintético coincide exactamente con motor_a, también con g15 ≠ g∞, m0 ≠ m_obj
    e impuestos (revisión dirigida, V9 y V10: antes solo se comprobaba con crecimiento y margen constantes)."""
    difs = []
    juegos = [(Fr("0.7"), Fr("0.7"), Fr("0.02"), Fr(0), Fr(0), Fr(1), Fr("0.714"), Fr(0)),
              (Fr("0.7"), Fr("0.7"), Fr("0.02"), Fr("0.05"), Fr("0.05"), Fr("0.5"), Fr("0.3"), Fr(0)),
              (Fr("0.13"), Fr("0.125"), Fr("0.04"), Fr("0.045"), Fr("0.02"), Fr("1.2"), Fr("0.1"), Fr("0.2882")),
              (Fr("0.10"), Fr("0.135"), Fr("-0.01"), Fr("0.055"), Fr("0.025"), Fr("1.5"), Fr("0.12"), Fr("0.25"))]
    for (m0, mo, f, g15, gi, s2c, roic, tau) in juegos:
        fl, term, _ = motor_sintetico(m0, f, g15, s2c, roic, gi, tau=tau, m_obj=mo)
        ref = motor_a(V0, m0, tau, f, g15, mo, s2c, gi, roic)
        difs += [abs(a - b) for a, b in zip(fl, ref["flujos"])] + [abs(term - ref["flujo_11"])]
    return max(difs) == 0, len(juegos)


def caso_fiscal():
    """N1 con impuestos y caja conocida (revisión dirigida, V9 y su sonda S3). Ventana de tres años con ventas 100,
    EBITDA 100, D&A 30 = capex, tipo legal del 25 %; en el año 2, un cargo de 9 no monetario y no deducible (como una
    revaluación de earnout). Caja sostenible: 70·(1 − 0,25) = 52,5. Se compara el flujo sin crecimiento del motor con
    cuatro tratamientos y tres convenciones del tipo de proyección."""
    t, E, EB0, D, S = Fr("0.25"), Fr(9), Fr(70), Fr(30), Fr(100)
    gasto = t * EB0                                   # no deducible: el gasto no baja por el cargo
    caja = EB0 * (1 - t)
    bai = {1: EB0, 2: EB0 - E, 3: EB0}
    fcf = Fr(100) - D - gasto                         # caja de cada año: el cargo no es monetario
    res = {}
    for trat in ("sin_normalizar", "N1_no_deducible", "N1_tipo_fijo", "deducir_la_partida_entera"):
        ebit = dict(bai)
        tau = {y: gasto / bai[y] for y in bai}        # tipo efectivo de cada año (fila 10)
        if trat in ("N1_no_deducible", "N1_tipo_fijo"):
            ebit[2] = EB0
            if trat == "N1_no_deducible":
                tau[2] = gasto / (bai[2] + E)         # gasto sin cambios, BAI sin el cargo
        nopat = sum(ebit[y] * (1 - tau[y]) for y in bai) / 3
        f = (nopat - (D - D) - fcf) / S
        if trat == "deducir_la_partida_entera":
            f += E / 3 / S                            # restar la partida antes de impuestos, como el diagnóstico
        for conv, extra in (("media_de_la_ventana", []), ("cinco_años_con_los_dos_anteriores_al_tipo_legal", [t, t]),
                            ("cinco_años_con_los_dos_anteriores_al_31", [Fr("0.31"), Fr("0.31")])):
            taus = [tau[y] for y in bai] + extra
            tp = sum(taus) / len(taus)
            res.setdefault(conv, {})[trat] = V0 * (EB0 / V0 * (1 - tp) - f)
    esperado = {"media_de_la_ventana": {"N1_no_deducible": True, "N1_tipo_fijo": True, "sin_normalizar": False, "deducir_la_partida_entera": False},
                "cinco_años_con_los_dos_anteriores_al_tipo_legal": {"N1_no_deducible": True, "N1_tipo_fijo": False, "sin_normalizar": False, "deducir_la_partida_entera": False},
                "cinco_años_con_los_dos_anteriores_al_31": {"N1_no_deducible": False, "N1_tipo_fijo": False, "sin_normalizar": False, "deducir_la_partida_entera": False}}
    ok = all((res[c][k] == caja) == esperado[c][k] for c in res for k in res[c])
    return {"caja_sostenible": num(caja),
            "flujo_sin_crecimiento": {c: {k: num(v) for k, v in d.items()} for c, d in res.items()},
            "coincide_con_la_caja_esperado": esperado, "ok": ok,
            "lectura": "Con tipos homogéneos, N1 sin efecto fiscal da la caja; con el tipo fijo solo la da si el tipo de "
                       "proyección es la media de la ventana; deducir la partida entera no la da nunca. La tercera fila es "
                       "la convención del tipo de proyección (E8.1), no un defecto de N1"}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--salida", required=True, type=Path)
    a = ap.parse_args()
    casos, errores = [], []

    def caso(ident, cuestion, descripcion, esc, R, esperado, g=Fr(0), g_inf=Fr(0), s2c=None, roic=Fr(1), m=None,
             extra=lambda t, Vt: Fr(0), m_obj=None, ancla=None):
        """esperado: «coherente» (motor = caja en todos los años y en el terminal) o «incoherencia_ilustrada».
        ancla: descripción del ancla de S2C cuando se calcula con la fórmula de E4."""
        f = esc.f(Fr(R))
        mm = m if m is not None else esc.ebit_ventana() / V0
        s2c_m = s2c if s2c is not None else esc.s2c_real
        fl, term, V = motor_sintetico(mm, f, g, s2c_m, roic, g_inf, extra, m_obj=m_obj)
        cj, cterm = caja_sintetica(esc, g, g_inf)
        dif = [x - y for x, y in zip(fl, cj)] + [term - cterm]
        situacion = "coherente" if all(d == 0 for d in dif) else "incoherencia_ilustrada"
        ok = situacion == esperado
        if not ok:
            errores.append(ident)
        anios = [1, 5, 6, 10]
        casos.append({
            "caso": ident, "cuestion": cuestion, "descripcion": descripcion,
            "parametros": {"R_que_calibra_f": num(Fr(R)), "f": num(f), "margen_inicial": num(mm if not callable(mm) else mm(1, V[0])),
                           "g_anios_1_5": num(g), "g_terminal": num(g_inf), "S2C_del_motor": num(s2c_m),
                           "ancla_de_S2C": ancla or "dada", "S2C_real": num(esc.s2c_real), "ROIC_del_terminal": num(roic),
                           "fcf_base_ventana": num(esc.fcf_base())},
            "motor": {f"año_{t}": num(fl[t - 1]) for t in anios} | {"año_11_terminal": num(term)},
            "caja_del_escenario": {f"año_{t}": num(cj[t - 1]) for t in anios} | {"año_11_terminal": num(cterm)},
            "diferencia_maxima": num(max(dif, key=abs)),
            "años_con_diferencia": [t for t in range(1, N + 1) if dif[t - 1] != 0] + (["año_11"] if dif[-1] != 0 else []),
            "esperado": esperado, "obtenido": situacion, "ok": ok})

    base = dict(ebitda=100, d_propia=20, rou=10, pagos_arr=12, mant=20)
    temporal = lambda t, Vt: Fr(7) if t <= 5 else Fr(0)     # noqa: E731  plan de transición de cinco años
    perpetua = lambda t, Vt: Fr(7)                          # noqa: E731
    proporcional = lambda t, Vt: Fr(7) * Vt / V0            # noqa: E731  permanente y proporcional a las ventas

    # ---------------------------------------------------------------- reproducción de los nueve casos del revisor externo
    rep = []
    for ident, esc, R in [
        ("arrendamiento_una_vez", Escenario(**base), 20),
        ("A0_doble_arrendamiento", Escenario(**base), 30),
        ("transicion_excluida_de_R_y_sin_linea_de_caja", Escenario(**base, trans_v=7, trans=perpetua), 20),
        ("transicion_incluida_en_R", Escenario(**base, trans_v=7, trans=perpetua), 27),
        ("transicion_separada_con_cargo_explicito", Escenario(**base, trans_v=7, trans=perpetua), 20),
        ("adquisicion_de_reposicion_tratada_solo_como_crecimiento", Escenario(**base, rep_adq=9), 20),
        ("adquisicion_de_reposicion_incluida_en_R", Escenario(**base, rep_adq=9), 29),
        ("gasto_comercial_ya_en_EBIT_y_cargado_otro_vez_en_R", Escenario(**base), 25),
        ("PPA_no_monetaria_con_costes_de_reposicion_ya_cubiertos", Escenario(**base, ppa=5), 20),
    ]:
        f = esc.f(Fr(R))
        flujo0 = V0 * (esc.ebit_ventana() / V0 - f) - (Fr(7) if ident == "transicion_separada_con_cargo_explicito" else 0)
        caja0 = esc.caja(1, V0, V0)
        esp = REVISOR[ident]
        ok = (flujo0, caja0) == (Fr(esp[0]), Fr(esp[1]))
        if not ok:
            errores.append("reproduccion:" + ident)
        rep.append({"caso": ident, "flujo_modelizado": num(flujo0), "caja_del_escenario": num(caja0),
                    "revisor": {"flujo_modelizado": esp[0], "caja_del_escenario": esp[1]}, "ok": ok})

    # ---------------------------------------------------------------- P1 · inversión de transición (clima), ancla dada
    c27 = dict(base, trans_v=7)
    caso("P1a_transicion_temporal_cargada_en_R", "P1",
         "Plan de transición de 7 al año durante 5 años, dentro del capex de la ventana, cargado en R (perpetuo en f). "
         "Cobra bien los años 1–5, pero sigue cobrando los 7 en los años 6–10 y en el año 11: el nombre «inversión» "
         "no la hace perpetua.", Escenario(**c27, trans=temporal), 27, "incoherencia_ilustrada")
    caso("P1b_transicion_temporal_con_termino_explicito", "P1",
         "El mismo plan, con R = 20 (solo mantenimiento) y un término explícito de 7 en los años 1–5, a crecimiento cero: "
         "exige importe y horizonte documentados.", Escenario(**c27, trans=temporal), 20, "coherente",
         extra=lambda t, Vt: Fr(7) if t <= 5 else Fr(0))
    caso("P1c_transicion_permanente_con_termino_temporal", "P1",
         "Si la inversión es en realidad permanente y el término explícito se limita a cinco años, los años 6–10 y el "
         "año 11 la omiten.", Escenario(**c27, trans=perpetua), 20, "incoherencia_ilustrada",
         extra=lambda t, Vt: Fr(7) if t <= 5 else Fr(0))
    caso("P1d_transicion_en_R_y_en_termino_explicito", "P1",
         "Cargarla en R y además como término explícito la cobra dos veces (54 frente a 61).",
         Escenario(**c27, trans=perpetua), 27, "incoherencia_ilustrada", extra=lambda t, Vt: Fr(7))
    caso("P1e_transicion_clasificada_como_crecimiento", "P1",
         "Clasificarla como crecimiento (solo por ΔV/S2C) la elimina a crecimiento cero: 68 frente a 61, como si se "
         "excluyera de todo.", Escenario(**c27, trans=perpetua), 20, "incoherencia_ilustrada")

    # ---------------------------------------------------------------- V2 y V9 · ventana con crecimiento y ancla de E4
    # Ventana: ventas 100, ΔV 5 con inversión de crecimiento 5 (S2C real 1), mantenimiento 20 y, si la hay, transición 7.
    g5, g2 = Fr("0.05"), Fr("0.02")
    roic_c = (1 + g2) * Fr("0.7")                    # ROIC que iguala la inversión del año 11 con ΔV/S2C (S2C = 1, m = 0,7)
    e_tr = dict(base, trans_v=7, dV_v=5)
    esc = Escenario(**e_tr, trans=temporal)
    caso("V2a_transicion_temporal_termino_explicito_ancla_E4_anterior", "P1/V2",
         "Ventana con crecimiento; transición temporal de 7 como término explícito en los años 1–5, y ancla de S2C con la "
         "fórmula de E4 anterior, sin sacar la transición del denominador: 5 ÷ (32 − 20) = 5/12. Con crecimiento la cobra "
         "dos veces, y por el ancla se vuelve perpetua. Es el caso P1b del autor con el ancla calculada.",
         esc, 20, "incoherencia_ilustrada", g=g5, g_inf=g2, s2c=esc.ancla_E4(Fr(20)), roic=roic_c,
         extra=lambda t, Vt: Fr(7) if t <= 5 else Fr(0), ancla="E4 anterior: 5/12")
    caso("V2b_transicion_temporal_termino_explicito_ancla_E4_corregida", "P1/V2",
         "Lo mismo con la regla corregida de E4: lo que se cobra como término explícito sale del denominador del ancla: "
         "5 ÷ (32 − 20 − 7) = 1. Coherente en los años 1–10 y en el año 11.",
         esc, 20, "coherente", g=g5, g_inf=g2, s2c=esc.ancla_E4(Fr(20), Fr(7)), roic=roic_c,
         extra=lambda t, Vt: Fr(7) if t <= 5 else Fr(0), ancla="E4 corregida: 1")
    esc = Escenario(**e_tr, trans=proporcional)
    caso("V2c_transicion_permanente_proporcional_en_R_ancla_E4", "P1/V2",
         "Transición permanente y proporcional a las ventas, dentro de R (R = 27): el ancla de E4 la excluye sola, porque "
         "está en D_X (5 ÷ (32 − 27) = 1). Coherente con crecimiento.",
         esc, 27, "coherente", g=g5, g_inf=g2, s2c=esc.ancla_E4(Fr(27)), roic=roic_c, ancla="E4: 1")
    esc = Escenario(**e_tr, trans=perpetua)
    caso("V2d_transicion_fija_en_euros_en_R_ancla_E4", "P1/V10",
         "Si la transición es fija en euros (7 al año) y se carga en R, f la hace crecer con las ventas: con crecimiento "
         "la cobra de más (revisión dirigida, S1d). «En R» supone proporcionalidad a las ventas.",
         esc, 27, "incoherencia_ilustrada", g=g5, g_inf=g2, s2c=esc.ancla_E4(Fr(27)), roic=roic_c, ancla="E4: 1")
    esc = Escenario(**dict(base, dV_v=5), s2c_real=Fr(5, 12))     # inversión de crecimiento 12 = 5 propia + 7 de transición
    caso("V2e_transicion_de_crecimiento_ancla_E4", "P1/V2",
         "Transición que amplía capacidad: en la ventana, 7 de los 12 de inversión de crecimiento para ΔV 5. El ancla de E4 "
         "la lleva en el denominador y es lo correcto: 5 ÷ (32 − 20) = 5/12 = S2C real. Coherente, también en el año 11 "
         "con el ROIC coherente.",
         esc, 20, "coherente", g=g5, g_inf=g2, s2c=esc.ancla_E4(Fr(20)), roic=(1 + g2) * Fr("0.7") * Fr(5, 12), ancla="E4: 5/12")
    e_rep = dict(base, rep_adq=9, dV_v=5)
    esc = Escenario(**e_rep)
    caso("V2f_compras_de_reposicion_termino_explicito_ancla_E4_anterior", "P2/V2",
         "Compras de reposición del 9 % de las ventas como término explícito (R = 20) y ancla con todas las compras en el "
         "denominador: 5 ÷ (25 − 20 + 9) = 5/14. Con crecimiento se cobran dos veces (revisión dirigida, S2a).",
         esc, 20, "incoherencia_ilustrada", g=g5, g_inf=g2, s2c=esc.ancla_E4(Fr(20)), roic=(1 + g2) * Fr("0.7") * Fr(5, 14),
         extra=lambda t, Vt: Fr(9) * Vt / V0, ancla="E4 anterior: 5/14")
    caso("V2g_compras_de_reposicion_termino_explicito_ancla_E4_corregida", "P2/V2",
         "Lo mismo con la regla corregida de E4: 5 ÷ (25 − 20 + 9 − 9) = 1. Coherente.",
         esc, 20, "coherente", g=g5, g_inf=g2, s2c=esc.ancla_E4(Fr(20), Fr(9)), roic=roic_c,
         extra=lambda t, Vt: Fr(9) * Vt / V0, ancla="E4 corregida: 1")
    caso("V2h_compras_de_reposicion_en_R_ancla_E4", "P2/V2",
         "Las compras de reposición dentro de R (R = 29, perímetro A3_estimado): el ancla de E4 las excluye sola, "
         "5 ÷ (25 − 29 + 9) = 1. Coherente (revisión dirigida, S2c).",
         esc, 29, "coherente", g=g5, g_inf=g2, s2c=esc.ancla_E4(Fr(29)), roic=roic_c, ancla="E4: 1")

    # ---------------------------------------------------------------- P2 · reposición de clientes y adquisiciones
    ancla_con_reposicion = Fr(5) / (Fr(5) + Fr(9))
    for gg, sufijo in [(Fr(0), "crecimiento_0"), (g5, "crecimiento_5_historico"), (Fr("0.10"), "crecimiento_10")]:
        caso(f"P2a_compras_de_reposicion_solo_como_crecimiento_{sufijo}", "P2",
             "Compras de cartera de 9 % de las ventas necesarias para mantenerlas, tratadas solo como crecimiento, con el "
             "ancla de S2C calculada con todas las compras (5 ÷ 14). A crecimiento cero faltan 9; a la tasa histórica casi "
             "se compensan por coincidencia; por encima, se cobran de más. Compensación no es correspondencia.",
             Escenario(**base, rep_adq=9), 20, "incoherencia_ilustrada", g=gg, g_inf=gg, s2c=ancla_con_reposicion,
             roic=(1 + gg) * Fr("0.7") * ancla_con_reposicion if gg else Fr(1))
        caso(f"P2b_compras_de_reposicion_en_R_y_ancla_sin_ellas_{sufijo}", "P2",
             "Las mismas compras dentro de R (R = 29 = 20 propio + 9 de cartera) y el ancla de S2C sin ellas (S2C real 1): "
             "coherente con cualquier crecimiento y en el año 11 (ROIC = (1+g)·m·S2C).",
             Escenario(**base, rep_adq=9), 29, "coherente", g=gg, g_inf=gg, s2c=Fr(1),
             roic=(1 + gg) * Fr("0.7") if gg else Fr(1))
    caso("P2c_compras_de_reposicion_en_R_y_tambien_en_el_ancla", "P2",
         "R = 29 y además el ancla de S2C con las compras de reposición en el denominador: a crecimiento cero es "
         "coherente (59), pero con crecimiento las cobra dos veces. La prueba a crecimiento cero no basta.",
         Escenario(**base, rep_adq=9), 29, "incoherencia_ilustrada", g=g5, g_inf=g5, s2c=ancla_con_reposicion,
         roic=(1 + g5) * Fr("0.7") * ancla_con_reposicion)
    caso("P2d_compras_de_reposicion_como_termino_explicito", "P2",
         "R = 20 y las compras de reposición como término explícito proporcional a las ventas (9 % de V_t), con el ancla "
         "dada sin ellas: coherente. Con el ancla calculada, véanse V2f y V2g.", Escenario(**base, rep_adq=9), 20, "coherente",
         g=g5, g_inf=g5, s2c=Fr(1), roic=(1 + g5) * Fr("0.7"), extra=lambda t, Vt: Fr(9) * Vt / V0)
    caso("P2e_compras_solo_de_crecimiento", "P2",
         "Si las compras solo amplían ventas (no hay compras de reposición), tratarlas como crecimiento es coherente, "
         "también a crecimiento cero (68). Es la hipótesis que exige la decisión (4b).",
         Escenario(**base), 20, "coherente", g=g5, g_inf=g5, s2c=Fr(1), roic=(1 + g5) * Fr("0.7"))
    caso("P2f_gasto_comercial_en_EBIT_y_en_R_con_crecimiento", "P2",
         "El gasto comercial de 5 ya está en el EBITDA; añadirlo a R lo cobra dos veces en todos los años.",
         Escenario(**base), 25, "incoherencia_ilustrada", g=g5, g_inf=g5, s2c=Fr(1), roic=(1 + g5) * Fr("0.7"))
    m_ppa = (Fr(100) - 20 - 10 - 5) / V0
    caso("P2g_PPA_constante_como_proporcion_de_las_ventas", "P2",
         "PPA del 5 % de las ventas en el margen y la misma proporción devuelta por f (perímetro A2): se anula cada año, "
         "con cualquier crecimiento. Es lo que significa «PPA constante».",
         Escenario(**base, ppa=5), 20, "coherente", g=g5, g_inf=g5, s2c=Fr(1), roic=(1 + g5) * m_ppa, m=m_ppa)
    m_euros = lambda t, Vt: (Fr(70) * Vt / V0 - Fr(5)) / Vt        # noqa: E731  PPA fija de 5 € en el margen
    caso("P2h_PPA_constante_en_euros_frente_a_f_proporcional", "P2",
         "Si el margen lleva la PPA constante en euros (5) y f devuelve el 5 % de las ventas, con crecimiento el flujo se "
         "sobrestima en 0,05·V_t − 5, cada vez más (año 11 con g∞ = 0 para aislar el efecto).",
         Escenario(**base, ppa=5), 20, "incoherencia_ilustrada", g=g5, g_inf=Fr(0), s2c=Fr(1), m=m_euros)
    m_agota = lambda t, Vt: (Fr(70) * Vt / V0 - max(Fr(0), Fr(5) * (1 - Fr(t, 4)))) / Vt     # noqa: E731
    caso("P2i_PPA_que_se_agota_frente_a_f_proporcional", "P2",
         "Si la PPA del margen se agota (cartera adquirida sin compras nuevas) y f sigue devolviendo el 5 %, el flujo se "
         "sobrestima hasta en 5 a crecimiento cero: por eso `EBIT_NIIF16_PPA_decreciente` con A2 no es admisible.",
         Escenario(**base, ppa=5), 20, "incoherencia_ilustrada", m=m_agota)

    # ---------------------------------------------------------------- P4 · terminal (g/ROIC) y crecimiento cero
    caso("P4a_terminal_con_ROIC_coherente_con_S2C", "P4",
         "Todos los costes recurrentes en el margen o en f; ROIC = (1+g∞)·m(1−τ)·S2C: el año 11 cobra la misma "
         "inversión de crecimiento que ΔV/S2C.", Escenario(**base), 20, "coherente",
         g=g2, g_inf=g2, s2c=Fr(1), roic=(1 + g2) * Fr("0.7"))
    caso("P4b_terminal_con_ROIC_de_otro_perimetro", "P4",
         "La inversión de crecimiento real es mitad capex propio y mitad compras (S2C real 1, ancla con compras = 1), "
         "pero el ROIC se mide solo sobre el capital propio (S2C propio 2): el año 11 cobra la mitad de la inversión "
         "de crecimiento.", Escenario(**base), 20, "incoherencia_ilustrada",
         g=g2, g_inf=g2, s2c=Fr(1), roic=(1 + g2) * Fr("0.7") * 2)
    caso("P4c_terminal_a_crecimiento_cero_con_reposicion_solo_como_crecimiento", "P4",
         "Con g∞ = 0 el año 11 es V·[m(1−τ) − f]: un coste recurrente cobrado solo como crecimiento desaparece "
         "también del terminal (68 frente a 59).", Escenario(**base, rep_adq=9), 20, "incoherencia_ilustrada")
    caso("P4d_arrendamiento_A0_en_el_terminal", "P4",
         "A0 (R = D&A total) cobra el arrendamiento dos veces en todos los años y en el año 11.",
         Escenario(**base), 30, "incoherencia_ilustrada", g=g2, g_inf=g2, s2c=Fr(1), roic=(1 + g2) * Fr("0.7"))
    caso("P4e_terminal_con_ROIC_igual_a_la_rentabilidad_marginal_del_libro", "P4/V6",
         "Si el ROIC es igual a la rentabilidad marginal de los años 1–10 del libro, S2C·m_obj·(1−τ) (Convenciones V6.3 §3: "
         "«salto» nulo), el año 11 cobra (1+g∞) veces ΔV/S2C: una diferencia de g∞·ΔV/S2C. Las dos fórmulas difieren solo "
         "en ese factor.", Escenario(**base), 20, "incoherencia_ilustrada", g=g2, g_inf=g2, s2c=Fr(1), roic=Fr("0.7"))
    caso("P4f_senda_de_motor_a_con_ancla_y_ROIC_coherentes", "P4/V9",
         "Senda de motor_a (g = 5 % en los años 1–5, lineal hasta g∞ = 2 %) con margen constante, ancla y ROIC coherentes: "
         "coherente en todos los años.", Escenario(**base), 20, "coherente", g=g5, g_inf=g2, s2c=Fr(1), roic=roic_c)

    # ---------------------------------------------------------------- guardas V-F1c: cada parte frente a su caja
    def guarda(R_propia, R_compras, capex_propio, compras):
        return {"R_propia": num(R_propia), "R_compras": num(R_compras), "capex_propio": num(capex_propio), "compras": num(compras),
                "guarda_anterior_R_total_mayor_que_capex_propio": (R_propia + R_compras) > capex_propio,
                "guarda_propuesta_salta": (R_propia > capex_propio) or (R_compras > compras)}
    guardas = {"no_salta_con_compras_de_cartera (R = 20 + 9)": (guarda(Fr(20), Fr(9), Fr(20), Fr(14)), False),
               "salta_si_R_propia_supera_el_capex_propio (25 frente a 20)": (guarda(Fr(25), Fr(0), Fr(20), Fr(14)), True),
               "salta_si_R_compras_supera_las_compras (9 frente a 5)": (guarda(Fr(20), Fr(9), Fr(20), Fr(5)), True)}
    for k, (g_, esperado) in guardas.items():
        g_["esperado_que_salte"] = esperado
        g_["ok"] = g_["guarda_propuesta_salta"] == esperado
        if not g_["ok"]:
            errores.append("guarda:" + k)
    if not guardas["no_salta_con_compras_de_cartera (R = 20 + 9)"][0]["guarda_anterior_R_total_mayor_que_capex_propio"]:
        errores.append("guarda anterior")

    fiscal = caso_fiscal()
    if not fiscal["ok"]:
        errores.append("caso_fiscal_N1")
    motor_ok, juegos = comprobar_motor()
    if not motor_ok:
        errores.append("motor_sintetico_distinto_de_motor_a")
    res = {
        "naturaleza": "ilustraciones sintéticas de definiciones de política; importes ficticios; no son datos de Elis ni una "
                      "ejecución del producto; no adoptan ninguna política",
        "procedencia": "amplía sondas_economicas.py de la revisión de la propuesta (1a071881c65a) y las sondas S1–S5 de la revisión "
                       "dirigida a P1–P4 (8fcc7fd792f0), con código propio",
        "motor_sintetico_coincide_con_motor_a": {"ok": motor_ok, "juegos": juegos,
                                                 "alcance": "sin términos explícitos; con g15 ≠ g∞, m0 ≠ m_obj e impuestos"},
        "reproduccion_casos_del_revisor": rep,
        "casos": casos,
        "guardas_V_F1c": {k: v[0] for k, v in guardas.items()},
        "caso_fiscal_N1": fiscal,
        "resumen": {"casos": len(casos), "coherentes": sum(c["obtenido"] == "coherente" for c in casos),
                    "incoherencias_ilustradas": sum(c["obtenido"] != "coherente" for c in casos),
                    "con_crecimiento": sum(c["parametros"]["g_anios_1_5"] != 0 for c in casos),
                    "con_ancla_calculada_E4": sum(c["parametros"]["ancla_de_S2C"] != "dada" for c in casos),
                    "reproducidos_del_revisor": sum(r["ok"] for r in rep), "guardas": len(guardas),
                    "caso_fiscal_ok": fiscal["ok"], "errores": errores},
    }
    a.salida.write_text(json.dumps(res, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(res["resumen"], ensure_ascii=False))
    for c in casos:
        print(f"{c['caso']}: {c['obtenido']} (esperado {c['esperado']}); diferencia máxima {c['diferencia_maxima']}; "
              f"años con diferencia {c['años_con_diferencia'] or 'ninguno'}")
    for k, v in res["guardas_V_F1c"].items():
        print(f"guarda {k}: salta {v['guarda_propuesta_salta']} (esperado {v['esperado_que_salte']})")
    print("caso fiscal N1:", json.dumps(fiscal["flujo_sin_crecimiento"], ensure_ascii=False), "caja", fiscal["caja_sostenible"])
    return 1 if errores else 0


if __name__ == "__main__":
    sys.exit(main())
