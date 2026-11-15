"""Recálculo independiente del revisor para la revisión n.º 3 (frente E, F1 de Elis). Solo biblioteca estándar.

Usa las cifras que el revisor transcribió de los PDF en la revisión n.º 1 (scripts_revisor/recalculo_independiente.py y
sensibilidades_revision.py), no el CSV ni el código del autor, y una réplica propia del motor A escrita desde la convención.
Aritmética exacta (fracciones). Compara con resultados/contraste_f1.json del autor (commit congelado) solo al final.

Uso: python3 -I recalculo_3.py --autor-json <ruta>/resultados/contraste_f1.json
"""
import argparse
import json
from fractions import Fraction as F

V = (2023, 2024, 2025)          # ventana de f
H = (2021, 2022, 2023, 2024, 2025)


def d(**k):
    return {int(a[1:]): F(v) for a, v in k.items()}


ventas = d(a2020="2806.3", a2021="3048.3", a2022="3820.9", a2023="4309.4", a2024="4573.7", a2025="4796.8")
ebit = d(a2023="496.8", a2024="596.3", a2025="630.0")                 # Historia fila 7 (BAI + financiero)
tipo = d(a2021="0.331", a2022="0.2823", a2023="0.2963", a2024="0.2754", a2025="0.256")
capex = d(a2021="573.9", a2022="699.8", a2023="823.9", a2024="887.4", a2025="890.2")
da = d(a2021="744.8", a2022="799.0", a2023="877.4", a2024="965.1", a2025="1019.4")
rou = d(a2021="92.6", a2022="103.7", a2023="115.8", a2024="132.2", a2025="149.5")
ppa = d(a2021="81.1", a2022="82.9", a2023="85.7", a2024="85.0", a2025="85.7")
wc = d(a2021="-10.2", a2022="52.6", a2023="5.9", a2024="6.9", a2025="4.0")
adq = d(a2021="86.8", a2022="221.7", a2023="82.1", a2024="183.3", a2025="117.6")
pagos = d(a2023="130.8", a2024="150.8", a2025="177.9")
C52 = F("1429.433") - F("857.167") - F("108") - F("128.1") - F("28.233")   # entradas registradas (3 decimales)
PAL = {  # Palancas B14:D18 y Análisis B68:D68, leídas del libro en la revisión n.º 1
    "MALO": dict(g15=F("0.02"), m_obj=F("0.105"), s2c=F("1"), roic=F("0.07"), g_inf=F("0.01")),
    "NORMAL": dict(g15=F("0.045"), m_obj=F("0.125"), s2c=F("1.2"), roic=F("0.10"), g_inf=F("0.02")),
    "BUENO": dict(g15=F("0.055"), m_obj=F("0.135"), s2c=F("1.5"), roic=F("0.12"), g_inf=F("0.025")),
}


def media(x, anios=V):
    return sum(x[a] for a in anios) / len(anios)


vm = media(ventas)
nopat = sum(ebit[a] * (1 - tipo[a]) for a in V) / 3
tau5 = sum(tipo[a] for a in H) / 5
v0, m0 = ventas[2025], ebit[2025] / ventas[2025]


def f_de(dx):
    """f con la reinversión necesaria D_X (dict por año)."""
    return (nopat - sum(capex[a] - dx[a] + wc[a] for a in V) / 3 - C52) / vm


def c53_de(dx):
    return (ventas[2025] - ventas[2020]) / sum(capex[a] - dx[a] + wc[a] + adq[a] for a in H)


def motor(f_anios, f_terminal, p):
    """Flujos de los años 1–10 y del año 11 (terminal), con una f para los años y otra para el terminal."""
    vp, fl = v0, []
    for t in range(1, 11):
        g = p["g15"] if t <= 5 else p["g15"] - (p["g15"] - p["g_inf"]) * F(t - 5, 5)
        vt = vp * (1 + g)
        mt = m0 + (p["m_obj"] - m0) * F(min(t, 5), 5)
        fl.append(vt * (mt * (1 - tau5) - f_anios) - (vt - vp) / p["s2c"])
        vp = vt
    f11 = vp * (1 + p["g_inf"]) * (p["m_obj"] * (1 - tau5) * (1 - p["g_inf"] / p["roic"]) - f_terminal)
    return fl, f11, vp


DX = {"A0": dict(da), "A1": {a: da[a] - rou[a] for a in H}, "A2": {a: da[a] - rou[a] - ppa[a] for a in H},
      "B": dict(capex)}
f_ = {k: f_de(x) for k, x in DX.items()}
F0 = {k: v0 * (m0 * (1 - tau5) - f_[k]) for k in DX}
C53 = {k: c53_de(x) for k, x in DX.items()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--autor-json", required=True)
    a = ap.parse_args()
    K = json.load(open(a.autor_json, encoding="utf-8"))
    ref = K["referencia_especificacion"]
    malos = 0

    def cmp(nombre, mio, suyo, tol=1e-9):
        nonlocal malos
        ok = abs(float(mio) - float(suyo)) <= tol
        malos += not ok
        print(f"   {'OK ' if ok else 'DIF'} {nombre}: revisor {float(mio):.12f} · autor {float(suyo):.12f}")

    print("1. f, flujo sin crecimiento y C53 por perímetro (T1–T3 y cota B)")
    for k in ("A0", "A1", "A2", "B"):
        r = ref["perimetros"][k]
        cmp(f"{k} f", f_[k], r["f"], 1e-13)
        cmp(f"{k} flujo sin crecimiento", F0[k], r["flujo_sin_crecimiento"])
        cmp(f"{k} C53", C53[k], r["S2C_C53"])

    print("\n2. Flujos de A1 y A2 con las palancas actuales (T2 y T3): años 1–10 y año 11")
    for k in ("A1", "A2"):
        for n, p in PAL.items():
            fl, f11, v10 = motor(f_[k], f_[k], p)
            det = ref["A1_A2_flujos_detalle"][k][n]
            dmax = max(abs(float(x) - y) for x, y in zip(fl, det["anios_1_10"]))
            ok = dmax <= 1e-9 and abs(float(f11) - det["anio_11_terminal"]) <= 1e-9
            malos += not ok
            print(f"   {'OK ' if ok else 'DIF'} {k} {n}: año 1 {float(fl[0]):.6f} · año 10 {float(fl[9]):.6f} · año 11 {float(f11):.12f}"
                  f" (autor {det['anio_11_terminal']:.12f}; dif. máx. años 1–10 {dmax:.1e})")

    print("\n3. Controles negativos de implementación parcial (¿qué referencia la detecta y por cuánto?)")
    for k in ("A1", "A2"):
        for n, p in PAL.items():
            fl, f11, v10 = motor(f_[k], f_[k], p)
            fl_b, f11_b, _ = motor(f_[k], f_["A0"], p)        # f nueva en los años, f de A0 en el terminal
            fl_c, f11_c, _ = motor(f_["A0"], f_[k], p)        # f de A0 en los años, f nueva en el terminal
            esperado = v10 * (1 + p["g_inf"]) * (f_["A0"] - f_[k])
            assert f11 - f11_b == esperado and fl == fl_b and f11 == f11_c
            print(f"   {k} {n}: terminal con f de A0 → año 11 {float(f11_b):.3f} frente a {float(f11):.3f} (desvío {float(f11 - f11_b):.3f} = V10·(1+g)·Δf);"
                  f" años con f de A0 → año 1 {float(fl_c[0]):.3f} frente a {float(fl[0]):.3f} (desvío {float(fl[0] - fl_c[0]):.3f})")
    print("   (ninguno de los desvíos es cero: la referencia del año 11 detecta el primero y las de los años 1–10 el segundo)")

    print("\n4. A3_estimado con valores sintéticos (T3b)")
    a3 = ref["A3_estimado_sintetico"]
    casos = {"D_X = capex propio (reproduce B)": dict(capex),
             "D_X = D&A propia (reproduce A2)": DX["A2"],
             "D_X = (capex + D&A propia)/2 (sintético)": {y: (capex[y] + DX["A2"][y]) / 2 for y in H}}
    for n, dx in casos.items():
        fx = f_de(dx)
        cmp(f"{n} f", fx, a3[n]["f"], 1e-13)
        cmp(f"{n} flujo sin crecimiento", v0 * (m0 * (1 - tau5) - fx), a3[n]["flujo_sin_crecimiento"])
    fm = f_de(casos["D_X = (capex + D&A propia)/2 (sintético)"])
    assert fm == (f_["B"] + f_["A2"]) / 2
    print("   punto medio exacto de A2 y B en f:", fm == (f_["B"] + f_["A2"]) / 2)
    # forma cerrada: f es lineal en la media de D_X de la ventana
    libre = {2021: F(600), 2022: F(650), 2023: F(700), 2024: F(820), 2025: F(905)}
    cerrada = f_["A0"] - (media(da) - media(libre)) / vm
    print(f"   D_X sintética no uniforme (700/820/905 en la ventana): f = {float(f_de(libre)):.15f}; forma cerrada f_A0 − (D&A total media − D_X media)/ventas medias: {f_de(libre) == cerrada}")
    solo25 = {y: libre[2025] for y in H}
    print(f"   una implementación que tomara solo la D_X de 2025 daría f = {float(f_de(solo25)):.6f} (≠ {float(f_de(libre)):.6f}): la referencia de f la detectaría si T3b incluyera un caso no uniforme")
    print("   C53 que correspondería a cada caso sintético (la especificación E4 exige la misma D_X en el ancla; T3b NO da esta referencia):")
    for n, dx in casos.items():
        print(f"      {n}: C53 = {float(c53_de(dx)):.12f}")

    print("\n5. O4 · palanca S2C anclada en el C53 de cada perímetro, escenario NORMAL")
    p = PAL["NORMAL"]
    v1 = v0 * (1 + p["g15"]); m1 = m0 + (p["m_obj"] - m0) / 5
    t = K["tablas"]["S2C_anclada_en_C53"]
    fl1 = {k: v1 * (m1 * (1 - tau5) - f_[k]) - (v1 - v0) / C53[k] for k in ("A0", "A1", "A2")}
    for k in ("A0", "A1", "A2"):
        cmp(f"{k} flujo del año 1 con S2C = C53", fl1[k], t[k]["flujo_año_1_NORMAL_con_S2C_ancla"], 1e-4)
    for k in ("A1", "A2"):
        dv = (F0[k] - F0["A0"]) / ((f_[k] + 1 / C53[k]) - (f_["A0"] + 1 / C53["A0"]))
        cmp(f"{k} brecha en el año 1", fl1[k] - fl1["A0"], t[k]["brecha_frente_a_A0_año_1"], 1e-4)
        cmp(f"{k} aumento de ventas que anula la brecha", dv, t[k]["aumento_de_ventas_que_anula_la_brecha"], 1e-4)
    print(f"   crecimiento compuesto de las ventas 2020→2025: {100 * ((float(ventas[2025]) / float(ventas[2020])) ** 0.2 - 1):.1f} %")

    print("\n6. O9 · partidas puntuales en el flujo sin crecimiento")
    earn = (F("48.4") - F("9.3") - F("0.1")) / 3
    plus = -(F("4.3") + F("7.3") - F("23.1")) / 3
    e1, e2, e3 = earn / vm * v0, -plus / vm * v0, F("25.7") * (1 - tau5)
    t = K["tablas"]["partidas_puntuales_en_flujo_sin_crecimiento"]
    for (n, x), y in zip((("earnout en f", e1), ("plusvalías en f", e2), ("plusvalía en m0", e3), ("neto", e1 + e2 + e3)), t.values()):
        cmp(n, x, y, 1e-3)

    print("\n7. O10 · tendencia de los arrendamientos")
    t = K["tablas"]["arrendamientos_tendencia"]
    esc = media(pagos) / vm * v0
    cmp("pagos medios escalados a 2025", esc, t["pagos_medios_escalados_a_2025 (f)"], 1e-3)
    cmp("pagos 2025 − escalados", pagos[2025] - esc, t["diferencia_pagos_2025_menos_escalados"], 1e-3)
    cmp("ROU 2025 no devuelta en A1/A2", rou[2025] - media(rou) / vm * v0, t["ROU_2025_no_devuelta_en_A1_A2"], 1e-3)

    print("\n8. O7 · ingreso por diferido de intangibles ÷ amortización de relaciones con clientes")
    t = K["tablas"]["impuestos"]
    for y, dif, am in ((2023, "15.5", "84.6"), (2024, "20.3", "83.9"), (2025, "17.5", "83.5")):   # URD23 p.346; DEU24 p.338 y p.310; URD25 p.393 y p.364
        cmp(f"{y}: {dif} ÷ {am} = {100 * float(F(dif) / F(am)):.1f} %", F(dif) / F(am), t[str(y)]["diferido_intangibles_÷_amortizacion_relaciones_con_clientes"], 1e-4)
    cmp("agotamiento 275,1 ÷ 83,5 (años)", F("275.1") / F("83.5"), t["2025"]["anios_de_agotamiento_relaciones_con_clientes_(VNC ÷ amortización 2025)"], 1e-4)
    print(f"   variante con la amortización de 2024 de la edición original (DEU 2024 p.310, 83,8): {100 * 20.3 / 83.8:.1f} %")

    print("\n9. E2 de la especificación · interés de arrendamiento que A1′ deja dentro de f")
    int_arr = (F("19.8") + F("25.8") + F("29.6")) / 3
    print(f"   interés de caja medio {float(int_arr):.3f} = {100 * float(int_arr / vm):.3f} % de las ventas medias; en la base 2025: {float(int_arr / vm * v0):.1f}")
    print(f"\n{'TODO COINCIDE con las referencias del autor' if not malos else str(malos) + ' DIFERENCIAS'}")
    return 1 if malos else 0


if __name__ == "__main__":
    raise SystemExit(main())
