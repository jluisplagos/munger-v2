"""Sondas sintéticas de correspondencia de caja · revisión dirigida a P1–P4 · propuesta de decisiones F1.

Script de revisión. Importes ficticios: no son datos de Elis, no ejecutan el producto y no adoptan nada.
Implementación propia (no importa código del autor). Cada sonda compara, calculados por separado:
  · el motor A (Convenciones V6.3 §1–§3) con la f calibrada como en §10 y, cuando se indica, con el ancla de S2C
    calculada con la fórmula de la especificación, E4: ΔV de la ventana ÷ (capex − D_X + circulante + adquisiciones);
  · la caja del escenario, partida a partida.
A diferencia de los controles del autor, la ventana tiene crecimiento, para que el ancla salga de sus datos y no se
escriba a mano. Así se prueba la cadena completa ventana → f y ancla → años 1–10 → año 11.

Bloques:
  S1  transición como término explícito y ancla de E4 (P1);
  S2  compras de reposición como término explícito o dentro de R, y ancla de E4 (P2);
  S3  regla N1 con impuestos: cargo no monetario y no deducible en un año de la ventana (P3);
  S4  ROIC del año 11: condición de la propuesta y fórmula de Convenciones §3 (P4);
  S5  peso del arrendamiento: pagos y amortización ROU devuelta por f (P4, decisión 1b).

Uso: python3 -I sondas_caja.py --salida ../resultados_revisor_p1_p4/sondas_caja.json --informe ../resultados_revisor_p1_p4/sondas_caja.txt
Termina con 1 si una sonda no da el resultado que el informe del revisor declara.
"""
import argparse
import json
import sys
from fractions import Fraction as Fr
from pathlib import Path

N = 10
V0 = Fr(100)


def num(x):
    x = Fr(x)
    return int(x) if x.denominator == 1 else round(float(x), 6)


class Mundo:
    """Escenario ficticio. Sin impuestos, sin circulante y sin intereses, salvo en S3.
    Por euro de ventas: EBITDA, capex de mantenimiento (= amortización propia), amortización ROU, pagos de
    arrendamiento y compras de cartera necesarias para mantener las ventas. En euros por año: transición.
    Cada euro de inversión de crecimiento da `s_real` euros de ventas nuevas."""

    def __init__(self, ebitda=100, mant=20, rou=10, pagos=12, rep=0, trans=lambda t: Fr(0), trans_ventana=0,
                 s_real=1, dv_ventana=5, crec_propio_ventana=5, crec_compras_ventana=0):
        self.ebitda, self.mant, self.rou, self.pagos, self.rep = map(Fr, (ebitda, mant, rou, pagos, rep))
        self.trans, self.trans_v, self.s_real = trans, Fr(trans_ventana), Fr(s_real)
        self.dv, self.g_propio, self.g_compras = Fr(dv_ventana), Fr(crec_propio_ventana), Fr(crec_compras_ventana)

    # --- ventana (un año representativo con ventas 100 y ΔV = dv)
    def capex(self):
        return self.mant + self.g_propio + self.trans_v

    def adquisiciones(self):
        return self.g_compras + self.rep

    def fcf_base(self):                       # como la plantilla: sin las compras de sociedades
        return self.ebitda - self.capex() - self.pagos

    def ebit(self):
        return self.ebitda - self.mant - self.rou

    def f(self, dx):                          # Convenciones §10, con τ = 0 y sin circulante
        return (self.ebit() - (self.capex() - Fr(dx)) - self.fcf_base()) / V0

    def ancla_e4(self, dx, fuera=0):          # especificación, E4; `fuera`: importe que se saca del denominador
        return self.dv / (self.capex() - Fr(dx) + self.adquisiciones() - Fr(fuera))

    # --- caja del escenario, partida a partida
    def caja(self, t, v, ant):
        e = v / V0
        return (self.ebitda - self.mant - self.pagos - self.rep) * e - self.trans(t) - (v - ant) / self.s_real


def motor(m, f, g, s2c, g_inf, roic, extra=lambda t, v: Fr(0), tau=Fr(0)):
    """Motor A con g y margen constantes. Año 11: V_10·(1+g∞)·[m(1−τ)(1 − g∞/ROIC) − f] − término explícito."""
    ant, fl, V = V0, [], []
    for t in range(1, N + 1):
        v = ant * (1 + g)
        fl.append(v * (m * (1 - tau) - f) - (v - ant) / s2c - extra(t, v))
        V.append(v)
        ant = v
    v11 = V[-1] * (1 + g_inf)
    a11 = v11 * (m * (1 - tau) * (1 - (g_inf / roic if g_inf else 0)) - f) - extra(N + 1, v11)
    return fl, a11, V


def caja_del_mundo(w, g, g_inf):
    ant, cj, V = V0, [], []
    for t in range(1, N + 1):
        v = ant * (1 + g)
        cj.append(w.caja(t, v, ant))
        V.append(v)
        ant = v
    return cj, w.caja(N + 1, V[-1] * (1 + g_inf), V[-1])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--salida", required=True, type=Path)
    ap.add_argument("--informe", required=True, type=Path)
    a = ap.parse_args()
    sondas, lineas, errores = [], [], []

    def p(s=""):
        lineas.append(s)

    def sonda(ident, bloque, texto, w, dx, esperado, g, s2c, extra=lambda t, v: Fr(0)):
        """esperado: «coherente», «cobra de más» (motor < caja) o «cobra de menos» (motor > caja). El ROIC del año 11 sale del ancla: (1+g)·m·S2C."""
        m = w.ebit() / V0
        f = w.f(dx)
        roic = (1 + g) * m * s2c if g else Fr(1)
        fl, a11, _ = motor(m, f, g, s2c, g, roic, extra)
        cj, c11 = caja_del_mundo(w, g, g)
        dif = [x - y for x, y in zip(fl, cj)] + [a11 - c11]
        if all(d == 0 for d in dif):
            obtenido = "coherente"
        elif all(d <= 0 for d in dif):
            obtenido = "cobra de más"
        elif all(d >= 0 for d in dif):
            obtenido = "cobra de menos"
        else:
            obtenido = "mixto"
        ok = obtenido == esperado
        if not ok:
            errores.append(ident)
        sondas.append({"sonda": ident, "bloque": bloque, "descripcion": texto,
                       "D_X_que_calibra_f": num(dx), "f": num(f), "ancla_S2C": num(s2c), "g": num(g),
                       "motor": {"año_1": num(fl[0]), "año_5": num(fl[4]), "año_6": num(fl[5]), "año_10": num(fl[9]), "año_11": num(a11)},
                       "caja": {"año_1": num(cj[0]), "año_5": num(cj[4]), "año_6": num(cj[5]), "año_10": num(cj[9]), "año_11": num(c11)},
                       "motor_menos_caja": {"año_1": num(dif[0]), "año_5": num(dif[4]), "año_6": num(dif[5]), "año_10": num(dif[9]), "año_11": num(dif[10])},
                       "esperado": esperado, "obtenido": obtenido, "ok": ok})
        p(f"  {ident}: {obtenido} (esperado: {esperado}) · f {num(f)} · ancla {num(s2c)} · g {num(g)}")
        p(f"      motor − caja: año 1 {num(dif[0])}; año 5 {num(dif[4])}; año 6 {num(dif[5])}; año 10 {num(dif[9])}; año 11 {num(dif[10])}")

    g5, g0 = Fr("0.05"), Fr(0)
    plan = lambda t: Fr(7) if t <= 5 else Fr(0)                      # noqa: E731  plan de transición de cinco años
    cobro_plan = lambda t, v: Fr(7) if t <= 5 else Fr(0)             # noqa: E731

    # ------------------------------------------------------------------ S1 · transición (P1)
    p("S1 · TRANSICIÓN COMO TÉRMINO EXPLÍCITO Y ANCLA DE E4 (P1)")
    p("  Ventana: ventas 100, ΔV 5; capex 32 = 20 de mantenimiento + 5 de crecimiento + 7 de transición; pagos de arrendamiento 12.")
    w = Mundo(trans=plan, trans_ventana=7)
    sonda("S1a_termino_explicito_y_ancla_de_E4", "S1",
          "`tratamiento_transicion = termino_explicito`: R = 20, término de 7 en los años 1–5. El ancla de E4 con D_X = R lleva los 7 "
          "de transición de la ventana en el denominador: 5 ÷ (32 − 20) = 5/12. Con crecimiento, ΔV/S2C vuelve a cobrarla.",
          w, 20, "cobra de más", g5, w.ancla_e4(20), cobro_plan)
    sonda("S1b_termino_explicito_y_ancla_sin_la_transicion", "S1",
          "Lo mismo, sacando la transición del denominador del ancla: 5 ÷ (32 − 20 − 7) = 1.",
          w, 20, "coherente", g5, w.ancla_e4(20, fuera=7), cobro_plan)
    sonda("S1c_como_S1a_a_crecimiento_cero", "S1",
          "S1a a crecimiento cero: coherente. La prueba a crecimiento cero no detecta el doble cargo.",
          w, 20, "coherente", g0, w.ancla_e4(20), cobro_plan)
    wp = Mundo(trans=lambda t: Fr(7), trans_ventana=7)
    sonda("S1d_permanente_en_R_y_ancla_de_E4", "S1",
          "`en_R` con una transición permanente que no crece con las ventas (7 al año): D_X = 27 y el ancla de E4 la excluye sola "
          "(5 ÷ (32 − 27) = 1). f la escala con las ventas: con crecimiento cobra de más 7·(V_t/100 − 1).",
          wp, 27, "cobra de más", g5, wp.ancla_e4(27))
    sonda("S1e_permanente_en_R_a_crecimiento_cero", "S1", "S1d a crecimiento cero: coherente.", wp, 27, "coherente", g0, wp.ancla_e4(27))
    wc = Mundo(trans=lambda t: Fr(0), trans_ventana=2, s_real=Fr(5, 7))
    sonda("S1f_crecimiento_cuando_amplia_capacidad", "S1",
          "`crecimiento` cuando de verdad amplía capacidad: cada euro de ventas nuevas pide 1 de inversión propia y 0,4 de transición. "
          "Ventana: capex 27 = 20 + 5 + 2. El ancla de E4 (5 ÷ 7) la cobra una vez.",
          wc, 20, "coherente", g5, wc.ancla_e4(20))

    # ------------------------------------------------------------------ S2 · compras de reposición (P2)
    p()
    p("S2 · COMPRAS DE REPOSICIÓN Y ANCLA DE E4 (P2)")
    p("  Ventana: ventas 100, ΔV 5; capex 25 = 20 + 5; compras de sociedades 9, todas necesarias para mantener las ventas (9 % de las ventas).")
    w2 = Mundo(rep=9)
    cobro_rep = lambda t, v: Fr(9) * v / V0                          # noqa: E731
    sonda("S2a_termino_explicito_y_ancla_de_E4", "S2",
          "`reposicion_con_importe` como término explícito: R = 20. El ancla de E4 con D_X = R lleva las 9 de la ventana en el "
          "denominador: 5 ÷ (25 − 20 + 9) = 5/14. Con crecimiento se cobran dos veces. V-F1j solo nombra «en R y en el ancla».",
          w2, 20, "cobra de más", g5, w2.ancla_e4(20), cobro_rep)
    sonda("S2b_termino_explicito_y_ancla_sin_ellas", "S2", "Lo mismo, con el ancla sin ellas: 5 ÷ (25 − 20 + 9 − 9) = 1.",
          w2, 20, "coherente", g5, w2.ancla_e4(20, fuera=9), cobro_rep)
    sonda("S2c_en_R_y_ancla_de_E4", "S2",
          "R = 29 (R_propia 20 + R_compras 9): la fórmula de E4 con D_X = R las excluye sola, 5 ÷ (25 − 29 + 9) = 1.",
          w2, 29, "coherente", g5, w2.ancla_e4(29))
    sonda("S2d_hipotesis_4b_con_compras_pequeñas_necesarias", "S2",
          "Hipótesis (4b) cuando hacen falta compras pequeñas del 3 % de las ventas para mantenerlas. Con la definición publicada "
          "esas compras cuentan dentro del crecimiento «orgánico», que saldría 0 % y no −3 %. Tratadas como crecimiento, a "
          "crecimiento cero el motor no las cobra.",
          Mundo(rep=3), 20, "cobra de menos", g0, Fr(1))

    # ------------------------------------------------------------------ S3 · N1 con impuestos (P3)
    p()
    p("S3 · REGLA N1 CON IMPUESTOS (P3)")
    p("  Ventana de tres años, ventas 100 y sin crecimiento: EBITDA 100; amortización = capex = 20; gasto financiero 10, pagado; tipo legal 25 %.")
    p("  En el año 1, cargo de 9 no monetario y no deducible dentro del EBIT. Impuesto pagado = devengado = 25 % × (80 − 10) = 17,5 cada año.")
    t_legal, fin, X = Fr(1, 4), Fr(10), Fr(9)
    ebit_limpio = Fr(80)
    imp = t_legal * (ebit_limpio - fin)
    fcf = Fr(100) - imp - 20 - fin                       # 52,5 cada año: es el flujo sostenible del escenario
    ebit_pub = [ebit_limpio - X, ebit_limpio, ebit_limpio]
    bai_pub = [e - fin for e in ebit_pub]

    def plantilla(ebit, bai, tau_fijos=None, horizonte_extra=()):
        tau = tau_fijos or [imp / b for b in bai]
        nopat = sum(e * (1 - tt) for e, tt in zip(ebit, tau)) / 3
        f = (nopat - 0 - fcf) / V0                       # reinversión = capex − amortización = 0
        taus_proy = list(tau) + list(horizonte_extra)
        tau_p = sum(taus_proy) / len(taus_proy)
        return V0 * ((ebit[2] / V0) * (1 - tau_p) - f), f, tau, tau_p

    tau_pub = [imp / b for b in bai_pub]
    ebit_n1 = [ebit_limpio] * 3
    bai_n1 = [e - fin for e in ebit_n1]
    s3 = {}
    for nombre, extra_h in (("τ de proyección = media de la ventana", ()),
                            ("τ de proyección = media de cinco años (dos años anteriores al 25 %)", (t_legal, t_legal)),
                            ("τ de proyección = media de cinco años (dos años anteriores al 31 %)", (Fr(31, 100), Fr(31, 100)))):
        sin, _, _, _ = plantilla(ebit_pub, bai_pub, horizonte_extra=extra_h)
        nd, _, _, _ = plantilla(ebit_n1, bai_n1, horizonte_extra=extra_h)
        fijo, _, _, _ = plantilla(ebit_n1, bai_n1, tau_fijos=tau_pub, horizonte_extra=extra_h)
        diag = sin - X                                   # deducir el diagnóstico: la partida entera, antes de impuestos
        s3[nombre] = {"flujo sostenible del escenario": num(fcf), "sin normalizar": num(sin),
                      "N1, no deducible (gasto sin cambios, tipo recalculado)": num(nd),
                      "N1, tipo fijo (fila 10 sin cambios)": num(fijo), "deducir la partida entera": num(diag),
                      "errores (motor − caja)": {"sin normalizar": num(sin - fcf), "no deducible": num(nd - fcf),
                                                 "tipo fijo": num(fijo - fcf), "deducir la partida": num(diag - fcf)}}
        p(f"  {nombre}: caja {num(fcf)}; sin normalizar {num(sin)}; N1 no deducible {num(nd)}; N1 tipo fijo {num(fijo)}; deducir la partida {num(diag)}")
    v = s3["τ de proyección = media de la ventana"]["errores (motor − caja)"]
    if not (v["no deducible"] == 0 and v["tipo fijo"] == 0 and v["sin normalizar"] != 0):
        errores.append("S3: con el τ de la ventana las dos reglas de N1 deben dar la caja y la base sin normalizar no")
    v5 = s3["τ de proyección = media de cinco años (dos años anteriores al 31 %)"]["errores (motor − caja)"]
    if not (v5["no deducible"] != 0 and v5["tipo fijo"] != 0 and v5["no deducible"] != v5["tipo fijo"]):
        errores.append("S3: con un τ de cinco años distinto, las dos reglas deben desviarse y diferir entre sí")

    # ------------------------------------------------------------------ S4 · ROIC del año 11 (P4)
    p()
    p("S4 · ROIC DEL AÑO 11 (P4)")
    g2, m4, s4c = Fr("0.02"), Fr("0.7"), Fr(1)
    w4 = Mundo()
    f4 = w4.f(20)
    cj, c11 = caja_del_mundo(w4, g2, g2)
    s4 = {}
    for nombre, roic in (("(1+g∞)·m·(1−τ)·S2C (condición de la propuesta)", (1 + g2) * m4 * s4c),
                         ("m·(1−τ)·S2C (Convenciones §3 y Diagnóstico V6, bloque 10)", m4 * s4c)):
        fl, a11, V = motor(m4, f4, g2, s4c, g2, roic)
        v11 = V[-1] * (1 + g2)
        inv = v11 * m4 * g2 / roic
        s4[nombre] = {"ROIC": num(roic), "inversión del año 11": num(inv), "ΔV_11/S2C": num((v11 - V[-1]) / s4c),
                      "cociente": num(inv / ((v11 - V[-1]) / s4c)), "año 11 del motor − caja": num(a11 - c11)}
        p(f"  {nombre}: {s4[nombre]}")
    if s4["(1+g∞)·m·(1−τ)·S2C (condición de la propuesta)"]["año 11 del motor − caja"] != 0:
        errores.append("S4: la condición de la propuesta debe igualar el año 11")
    if s4["m·(1−τ)·S2C (Convenciones §3 y Diagnóstico V6, bloque 10)"]["cociente"] != num(1 + g2):
        errores.append("S4: con la fórmula de Convenciones la inversión debe ser (1+g) veces ΔV/S2C")

    # ------------------------------------------------------------------ S5 · peso del arrendamiento (P4, 1b)
    p()
    p("S5 · PESO DEL ARRENDAMIENTO: PAGOS Y AMORTIZACIÓN ROU (P4, decisión 1b)")
    p("  Ventana de tres años con ventas 100: pagos 10 / 11 / 12 y amortización ROU 8 / 9 / 10; EBITDA 100; mantenimiento 20. Sin crecimiento.")
    pag, rou = [Fr(10), Fr(11), Fr(12)], [Fr(8), Fr(9), Fr(10)]
    m0 = (Fr(100) - 20 - rou[2]) / V0                    # el margen de partida lleva la amortización ROU del último año
    fcf5 = Fr(100) - 20 - sum(pag) / 3
    ebit5 = Fr(100) - 20 - sum(rou) / 3
    s5 = {}
    for per, dx in (("A0 (D_X = amortización total)", 20 + sum(rou) / 3), ("A1/A2 (D_X sin la ROU)", Fr(20))):
        f5 = (ebit5 - (20 - dx) - fcf5) / V0
        F0 = V0 * (m0 - f5)
        f_pagos = f5 + (pag[2] - sum(pag) / 3) / V0
        f_ambos = f_pagos - ((rou[2] - sum(rou) / 3) / V0 if "sin la ROU" in per else 0)
        s5[per] = {"f": num(f5), "flujo sin crecimiento": num(F0),
                   "con el peso del último año en los pagos": num(V0 * (m0 - f_pagos) - F0),
                   "con el peso del último año en los pagos y en la ROU que devuelve f": num(V0 * (m0 - f_ambos) - F0),
                   "caja con los pagos del último año": num(Fr(100) - 20 - pag[2])}
        p(f"  {per}: {s5[per]}")
    if s5["A1/A2 (D_X sin la ROU)"]["con el peso del último año en los pagos y en la ROU que devuelve f"] != 0:
        errores.append("S5: en A1/A2 los dos efectos de escala del ejemplo deben compensarse")

    res = {"naturaleza": "sondas sintéticas del revisor; importes ficticios; no son datos de Elis ni una ejecución del producto",
           "sondas": sondas, "S3_regla_N1_con_impuestos": s3, "S4_ROIC_del_año_11": s4, "S5_peso_del_arrendamiento": s5,
           "resumen": {"sondas_de_flujo": len(sondas), "errores": errores}}
    p()
    p(f"RESUMEN: {len(sondas)} sondas de flujo y tres bloques de cálculo; errores {len(errores)}")
    for e in errores:
        p("  ERROR " + e)
    a.salida.write_text(json.dumps(res, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    a.informe.write_text("\n".join(lineas) + "\n", encoding="utf-8")
    print("\n".join(lineas))
    return 1 if errores else 0


if __name__ == "__main__":
    sys.exit(main())
