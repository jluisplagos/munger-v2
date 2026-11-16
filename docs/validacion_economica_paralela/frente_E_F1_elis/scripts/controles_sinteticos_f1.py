"""Controles sintéticos de correspondencia de caja · propuesta F1 (respuesta a la revisión de la propuesta, P1–P4).

Son ejemplos de política con importes ficticios. No usan datos de Elis, no ejecutan el producto y no adoptan ninguna
definición. Cada caso compara dos cosas, calculadas por separado:
  · los flujos del motor A sintético: la misma función `motor_a` con la que `contraste_f1.py` replica el libro
    (flujo_t = V_t·[m_t(1−τ) − f] − ΔV_t/S2C; terminal = V_10·(1+g∞)·[m(1−τ)(1 − g∞/ROIC) − f]), más los términos
    explícitos que declare el caso;
  · la caja del escenario, partida a partida: EBITDA − capex de mantenimiento − pagos de arrendamiento − compras de
    cartera necesarias para mantener las ventas − inversión de transición − inversión de crecimiento.
Así se comprueba que cada desembolso se cobra una sola vez en la calibración, en los años proyectados y en el
terminal, también a crecimiento cero.

Amplía `sondas_economicas.py` de la revisión externa de la propuesta (rama auditoria/revision-propuesta-f1, commit
1a071881c65a191056ca3c6b41a20a965825cf12): reproduce sus nueve casos y añade años con crecimiento, términos
explícitos con horizonte, el ancla de S2C, el terminal con g/ROIC, el significado de «PPA constante» y la guarda que
compara R con el capex.

Convenciones del escenario, todas ficticias: sin impuestos, sin circulante ni intereses de deuda; ventas de la
ventana 100, ventana estacionaria; los costes que escalan con las ventas lo hacen en proporción constante.

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
V0 = Fr(100)                # ventas de la ventana y del año base
REVISOR = {                 # comprobaciones_sinteticas.json del revisor (1a07188): flujo modelizado y caja del escenario
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


class Escenario:
    """Escenario ficticio. Importes de la ventana (ventas 100); los marcados «por ventas» escalan con V_t."""

    def __init__(self, **k):
        self.ebitda = Fr(k.get("ebitda", 100))          # por ventas; ya descuenta el gasto comercial corriente
        self.d_propia = Fr(k.get("d_propia", 20))       # por ventas; amortización propia (= capex de mantenimiento)
        self.rou = Fr(k.get("rou", 10))                 # por ventas; amortización de derechos de uso
        self.pagos_arr = Fr(k.get("pagos_arr", 12))     # por ventas; pagos de arrendamiento (principal + interés)
        self.mant = Fr(k.get("mant", 20))               # por ventas; capex propio de mantenimiento
        self.rep_adq = Fr(k.get("rep_adq", 0))          # por ventas; compras de cartera necesarias para mantener ventas
        self.ppa_v = Fr(k.get("ppa", 0))                # PPA de la ventana (no monetaria)
        self.trans = k.get("trans", lambda t: Fr(0))     # euros por año t (t = 1..N; N+1 = terminal); inversión de transición
        self.trans_v = Fr(k.get("trans_v", 0))          # inversión de transición dentro del capex de la ventana
        self.s2c_real = Fr(k.get("s2c_real", 1))        # ventas adicionales por euro de inversión de crecimiento

    # ventana de calibración (estacionaria): el FCF base excluye las compras de sociedades, como en la plantilla
    def capex_ventana(self):
        return self.mant + self.trans_v

    def fcf_base(self):
        return self.ebitda - self.capex_ventana() - self.pagos_arr

    def ebit_ventana(self):
        return self.ebitda - self.d_propia - self.rou - self.ppa_v

    def f(self, R):
        """f = [EBIT − (capex − R) − FCF base] ÷ ventas, con τ = 0 y sin circulante (Convenciones V6.3 §10)."""
        return (self.ebit_ventana() - (self.capex_ventana() - R) - self.fcf_base()) / V0

    # caja del escenario, partida a partida
    def caja(self, t, Vt, Vprev):
        e = Vt / V0
        return (self.ebitda * e - self.mant * e - self.pagos_arr * e - self.rep_adq * e - self.trans(t)
                - (Vt - Vprev) / self.s2c_real)


def motor_sintetico(m, f, g, s2c, roic, g_inf, extra=lambda t, Vt: Fr(0), tau=Fr(0)):
    """Mismas ecuaciones que motor_a, con margen m_t (número o función de t y V_t) y términos explícitos X_t.
    t = N+1 es el terminal: V_N·(1+g∞)·[m(1−τ)(1 − g∞/ROIC) − f] − X_{N+1}."""
    mt = m if callable(m) else (lambda t, Vt: m)
    V, prev, flujos = [], V0, []
    for t in range(1, N + 1):
        Vt = prev * (1 + g)
        flujos.append(Vt * (mt(t, Vt) * (1 - tau) - f) - (Vt - prev) / s2c - extra(t, Vt))
        V.append(Vt)
        prev = Vt
    V11 = V[-1] * (1 + g_inf)
    term = V11 * (mt(N + 1, V11) * (1 - tau) * (1 - g_inf / roic) - f) - extra(N + 1, V11)
    return flujos, term, V


def caja_sintetica(esc, g, g_inf):
    V, prev, cajas = [], V0, []
    for t in range(1, N + 1):
        Vt = prev * (1 + g)
        cajas.append(esc.caja(t, Vt, prev))
        V.append(Vt)
        prev = Vt
    return cajas, esc.caja(N + 1, V[-1] * (1 + g_inf), V[-1])


def comprobar_motor():
    """El motor sintético sin términos explícitos y con m y g constantes coincide exactamente con motor_a."""
    difs = []
    for (m, f, g, s2c, roic, gi) in [(Fr("0.7"), Fr("0.02"), Fr(0), Fr(1), Fr("0.714"), Fr(0)),
                                     (Fr("0.7"), Fr("0.02"), Fr("0.05"), Fr("0.5"), Fr("0.3"), Fr("0.05")),
                                     (Fr("0.13"), Fr("0.04"), Fr("0.02"), Fr("1.2"), Fr("0.1"), Fr("0.02"))]:
        fl, term, _ = motor_sintetico(m, f, g, s2c, roic, gi)
        ref = motor_a(V0, m, Fr(0), f, g, m, s2c, gi, roic)
        difs += [abs(a - b) for a, b in zip(fl, ref["flujos"])] + [abs(term - ref["flujo_11"])]
    return max(difs) == 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--salida", required=True, type=Path)
    a = ap.parse_args()
    casos, errores = [], []

    def caso(ident, cuestion, descripcion, esc, R, esperado, g=Fr(0), g_inf=Fr(0), s2c=None, roic=Fr(1), m=None,
             extra=lambda t, Vt: Fr(0), muestra=None):
        """esperado: «coherente» (motor = caja en todos los años y en el terminal) o «incoherencia_ilustrada»."""
        f = esc.f(Fr(R))
        mm = m if m is not None else esc.ebit_ventana() / V0
        fl, term, V = motor_sintetico(mm, f, g, s2c if s2c is not None else esc.s2c_real, roic, g_inf, extra)
        cj, cterm = caja_sintetica(esc, g, g_inf)
        dif = [x - y for x, y in zip(fl, cj)] + [term - cterm]
        situacion = "coherente" if all(d == 0 for d in dif) else "incoherencia_ilustrada"
        ok = situacion == esperado
        if not ok:
            errores.append(ident)
        anios = sorted(set([1, 5, 6, 10] + (muestra or [])))
        casos.append({
            "caso": ident, "cuestion": cuestion, "descripcion": descripcion,
            "parametros": {"R_que_calibra_f": num(Fr(R)), "f": num(f), "margen_inicial": num(mm if not callable(mm) else mm(1, V[0])),
                           "g_anios_1_10": num(g), "g_terminal": num(g_inf), "S2C_del_motor": num(s2c if s2c is not None else esc.s2c_real),
                           "S2C_real": num(esc.s2c_real), "ROIC_del_terminal": num(roic), "fcf_base_ventana": num(esc.fcf_base())},
            "motor": {f"año_{t}": num(fl[t - 1]) for t in anios} | {"terminal": num(term)},
            "caja_del_escenario": {f"año_{t}": num(cj[t - 1]) for t in anios} | {"terminal": num(cterm)},
            "diferencia_maxima": num(max(dif, key=abs)),
            "años_con_diferencia": [t for t in range(1, N + 1) if dif[t - 1] != 0] + (["terminal"] if dif[-1] != 0 else []),
            "esperado": esperado, "obtenido": situacion, "ok": ok})
        return fl, term, cj, cterm

    base = dict(ebitda=100, d_propia=20, rou=10, pagos_arr=12, mant=20)
    temporal = lambda t: Fr(7) if t <= 5 else Fr(0)     # noqa: E731  plan de transición de cinco años
    perpetua = lambda t: Fr(7)                          # noqa: E731

    # ---------------------------------------------------------------- reproducción de los nueve casos del revisor
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

    # ---------------------------------------------------------------- P1 · inversión de transición (clima)
    c27 = dict(base, trans_v=7)
    caso("P1a_transicion_temporal_cargada_en_R", "P1",
         "Plan de transición de 7 al año durante 5 años, dentro del capex de la ventana, cargado en R (perpetuo en f). "
         "Cobra bien los años 1–5, pero sigue cobrando los 7 en los años 6–10 y en el terminal: el nombre «inversión» "
         "no la hace perpetua.", Escenario(**c27, trans=temporal), 27, "incoherencia_ilustrada")
    caso("P1b_transicion_temporal_con_termino_explicito", "P1",
         "El mismo plan, con R = 20 (solo mantenimiento) y un término explícito de 7 en los años 1–5: exige importe y "
         "horizonte documentados.", Escenario(**c27, trans=temporal), 20, "coherente",
         extra=lambda t, Vt: Fr(7) if t <= 5 else Fr(0))
    caso("P1c_transicion_permanente_con_termino_temporal", "P1",
         "Si la inversión es en realidad permanente y el término explícito se limita a cinco años, los años 6–10 y el "
         "terminal la omiten.", Escenario(**c27, trans=perpetua), 20, "incoherencia_ilustrada",
         extra=lambda t, Vt: Fr(7) if t <= 5 else Fr(0))
    caso("P1d_transicion_en_R_y_en_termino_explicito", "P1",
         "Cargarla en R y además como término explícito la cobra dos veces (54 frente a 61).",
         Escenario(**c27, trans=perpetua), 27, "incoherencia_ilustrada", extra=lambda t, Vt: Fr(7))
    caso("P1e_transicion_clasificada_como_crecimiento", "P1",
         "Clasificarla como crecimiento (solo por ΔV/S2C) la elimina a crecimiento cero: 68 frente a 61, como si se "
         "excluyera de todo.", Escenario(**c27, trans=perpetua), 20, "incoherencia_ilustrada")

    # ---------------------------------------------------------------- P2 · reposición de clientes y adquisiciones
    g5 = Fr("0.05")
    # Ancla histórica de S2C con ΔV = 5: inversión de crecimiento 5 (propia y compras de crecimiento, S2C real = 1)
    # más las compras de reposición 9 si se cuentan en el denominador.
    ancla_con_reposicion = Fr(5) / (Fr(5) + Fr(9))
    for g, sufijo in [(Fr(0), "crecimiento_0"), (g5, "crecimiento_5_historico"), (Fr("0.10"), "crecimiento_10")]:
        caso(f"P2a_compras_de_reposicion_solo_como_crecimiento_{sufijo}", "P2",
             "Compras de cartera de 9 % de las ventas necesarias para mantenerlas, tratadas solo como crecimiento, con el "
             "ancla de S2C calculada con todas las compras (5 ÷ 14). A crecimiento cero faltan 9; a la tasa histórica casi "
             "se compensan por coincidencia; por encima, se cobran de más. Compensación no es correspondencia.",
             Escenario(**base, rep_adq=9), 20, "incoherencia_ilustrada", g=g, g_inf=g, s2c=ancla_con_reposicion,
             roic=(1 + g) * Fr("0.7") * ancla_con_reposicion if g else Fr(1))
        caso(f"P2b_compras_de_reposicion_en_R_y_ancla_sin_ellas_{sufijo}", "P2",
             "Las mismas compras dentro de R (R = 29 = 20 propio + 9 de cartera) y el ancla de S2C sin ellas (S2C real 1): "
             "coherente con cualquier crecimiento y en el terminal (ROIC = (1+g)·m·S2C).",
             Escenario(**base, rep_adq=9), 29, "coherente", g=g, g_inf=g, s2c=Fr(1),
             roic=(1 + g) * Fr("0.7") * 1 if g else Fr(1))
    caso("P2c_compras_de_reposicion_en_R_y_tambien_en_el_ancla", "P2",
         "R = 29 y además el ancla de S2C con las compras de reposición en el denominador: a crecimiento cero es "
         "coherente (59), pero con crecimiento las cobra dos veces. La prueba a crecimiento cero no basta.",
         Escenario(**base, rep_adq=9), 29, "incoherencia_ilustrada", g=g5, g_inf=g5, s2c=ancla_con_reposicion,
         roic=(1 + g5) * Fr("0.7") * ancla_con_reposicion)
    caso("P2d_compras_de_reposicion_como_termino_explicito", "P2",
         "R = 20 y las compras de reposición como término explícito proporcional a las ventas (9 % de V_t), con el ancla "
         "sin ellas: coherente, alternativa a meterlas en R.", Escenario(**base, rep_adq=9), 20, "coherente",
         g=g5, g_inf=g5, s2c=Fr(1), roic=(1 + g5) * Fr("0.7"), extra=lambda t, Vt: Fr(9) * Vt / V0)
    caso("P2e_compras_solo_de_crecimiento", "P2",
         "Si las compras solo amplían ventas (no hay compras de reposición), tratarlas como crecimiento es coherente, "
         "también a crecimiento cero (68). Es la hipótesis que exige la decisión (4b).",
         Escenario(**base), 20, "coherente", g=g5, g_inf=g5, s2c=Fr(1), roic=(1 + g5) * Fr("0.7"))
    caso("P2f_gasto_comercial_en_EBIT_y_en_R_con_crecimiento", "P2",
         "El gasto comercial de 5 ya está en el EBITDA; añadirlo a R lo cobra dos veces en todos los años.",
         Escenario(**base), 25, "incoherencia_ilustrada", g=g5, g_inf=g5, s2c=Fr(1), roic=(1 + g5) * Fr("0.7"))
    # «PPA constante»: proporción de las ventas frente a euros
    ppa_share = Fr(5) / V0
    m_ppa = (Fr(100) - 20 - 10 - 5) / V0
    caso("P2g_PPA_constante_como_proporcion_de_las_ventas", "P2",
         "PPA del 5 % de las ventas en el margen y la misma proporción devuelta por f (perímetro A2): se anula cada año, "
         "con cualquier crecimiento. Es lo que significa «PPA constante».",
         Escenario(**base, ppa=5), 20, "coherente", g=g5, g_inf=g5, s2c=Fr(1), roic=(1 + g5) * m_ppa, m=m_ppa)
    m_euros = lambda t, Vt: (Fr(70) * Vt / V0 - Fr(5)) / Vt        # noqa: E731  PPA fija de 5 € en el margen
    caso("P2h_PPA_constante_en_euros_frente_a_f_proporcional", "P2",
         "Si el margen lleva la PPA constante en euros (5) y f devuelve el 5 % de las ventas, con crecimiento el flujo se "
         "sobrestima en 0,05·V_t − 5, cada vez más (terminal con g∞ = 0 para aislar el efecto).",
         Escenario(**base, ppa=5), 20, "incoherencia_ilustrada", g=g5, g_inf=Fr(0), s2c=Fr(1), m=m_euros)
    m_agota = lambda t, Vt: (Fr(70) * Vt / V0 - max(Fr(0), Fr(5) * (1 - Fr(t, 4)))) / Vt     # noqa: E731
    caso("P2i_PPA_que_se_agota_frente_a_f_proporcional", "P2",
         "Si la PPA del margen se agota (cartera adquirida sin compras nuevas) y f sigue devolviendo el 5 %, el flujo se "
         "sobrestima hasta en 5 a crecimiento cero: por eso `EBIT_NIIF16_PPA_decreciente` con A2 no es admisible.",
         Escenario(**base, ppa=5), 20, "incoherencia_ilustrada", m=m_agota)

    # ---------------------------------------------------------------- P4 · terminal (g/ROIC) y crecimiento cero
    g2 = Fr("0.02")
    caso("P4a_terminal_con_ROIC_coherente_con_S2C", "P4",
         "Todos los costes recurrentes en el margen o en f; ROIC = (1+g∞)·m(1−τ)·S2C: el terminal cobra la misma "
         "inversión de crecimiento que ΔV/S2C.", Escenario(**base), 20, "coherente",
         g=g2, g_inf=g2, s2c=Fr(1), roic=(1 + g2) * Fr("0.7"))
    caso("P4b_terminal_con_ROIC_de_otro_perimetro", "P4",
         "La inversión de crecimiento real es mitad capex propio y mitad compras (S2C real 1, ancla con compras = 1), "
         "pero el ROIC se mide solo sobre el capital propio (S2C propio 2): el terminal cobra la mitad de la inversión "
         "de crecimiento.", Escenario(**base), 20, "incoherencia_ilustrada",
         g=g2, g_inf=g2, s2c=Fr(1), roic=(1 + g2) * Fr("0.7") * 2)
    caso("P4c_terminal_a_crecimiento_cero_con_reposicion_solo_como_crecimiento", "P4",
         "Con g∞ = 0 el terminal es V·[m(1−τ) − f]: un coste recurrente cobrado solo como crecimiento desaparece "
         "también del terminal (68 frente a 59).", Escenario(**base, rep_adq=9), 20, "incoherencia_ilustrada")
    caso("P4d_arrendamiento_A0_en_el_terminal", "P4",
         "A0 (R = D&A total) cobra el arrendamiento dos veces en todos los años y en el terminal.",
         Escenario(**base), 30, "incoherencia_ilustrada", g=g2, g_inf=g2, s2c=Fr(1), roic=(1 + g2) * Fr("0.7"))

    # ---------------------------------------------------------------- guarda V-F1c: R frente a capex
    # Con R = 29 (20 propio + 9 de compras de cartera) y capex propio 20, comparar R total con el capex propio
    # dispararía la alarma de infrainversión sin que la haya. La guarda debe comparar cada parte con su caja.
    R_propio, R_compras, capex_propio, compras = Fr(20), Fr(9), Fr(20), Fr(9) + Fr(5)
    guarda = {"R_total": num(R_propio + R_compras), "capex_propio": num(capex_propio), "compras_de_sociedades": num(compras),
              "guarda_anterior_R_total_mayor_que_capex_propio": (R_propio + R_compras) > capex_propio,
              "guarda_propuesta_R_propio_mayor_que_capex_propio": R_propio > capex_propio,
              "guarda_propuesta_R_compras_mayor_que_compras": R_compras > compras}
    if not (guarda["guarda_anterior_R_total_mayor_que_capex_propio"] and not guarda["guarda_propuesta_R_propio_mayor_que_capex_propio"]
            and not guarda["guarda_propuesta_R_compras_mayor_que_compras"]):
        errores.append("guarda")

    motor_ok = comprobar_motor()
    if not motor_ok:
        errores.append("motor_sintetico_distinto_de_motor_a")
    res = {
        "naturaleza": "ilustraciones sintéticas de definiciones de política; importes ficticios; no son datos de Elis ni una "
                      "ejecución del producto; no adoptan ninguna política",
        "procedencia": "amplía sondas_economicas.py de la revisión de la propuesta (auditoria/revision-propuesta-f1, 1a071881c65a)",
        "motor_sintetico_coincide_con_motor_a": motor_ok,
        "reproduccion_casos_del_revisor": rep,
        "casos": casos,
        "guarda_R_frente_a_capex": guarda,
        "resumen": {"casos": len(casos), "coherentes": sum(c["obtenido"] == "coherente" for c in casos),
                    "incoherencias_ilustradas": sum(c["obtenido"] != "coherente" for c in casos),
                    "reproducidos_del_revisor": sum(r["ok"] for r in rep), "errores": errores},
    }
    a.salida.write_text(json.dumps(res, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(res["resumen"], ensure_ascii=False))
    for c in casos:
        print(f"{c['caso']}: {c['obtenido']} (esperado {c['esperado']}); diferencia máxima {c['diferencia_maxima']}; "
              f"años con diferencia {c['años_con_diferencia'] or 'ninguno'}")
    return 1 if errores else 0


if __name__ == "__main__":
    sys.exit(main())
