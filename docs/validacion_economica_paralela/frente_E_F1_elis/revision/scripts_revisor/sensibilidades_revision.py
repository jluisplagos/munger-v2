"""Cálculos de apoyo de las objeciones del revisor (frente E, F1 de Elis). Solo biblioteca estándar.
Cifras transcritas por el revisor de los PDF (documento y página en REVISION_INDEPENDIENTE_1.md).
No son propuestas ni valoraciones: ilustran matices de alcance.

Uso: python3 -I sensibilidades_revision.py
"""
A = [2023, 2024, 2025]
ventas = {2020: 2806.3, 2021: 3048.3, 2022: 3820.9, 2023: 4309.4, 2024: 4573.7, 2025: 4796.8}
ebit = {2023: 496.8, 2024: 596.3, 2025: 630.0}
tipo = {2021: 0.331, 2022: 0.2823, 2023: 0.2963, 2024: 0.2754, 2025: 0.256}
capex = {2021: 573.9, 2022: 699.8, 2023: 823.9, 2024: 887.4, 2025: 890.2}
da = {2021: 744.8, 2022: 799.0, 2023: 877.4, 2024: 965.1, 2025: 1019.4}
rou = {2021: 92.6, 2022: 103.7, 2023: 115.8, 2024: 132.2, 2025: 149.5}
ppa = {2021: 81.1, 2022: 82.9, 2023: 85.7, 2024: 85.0, 2025: 85.7}
wc = {2021: -10.2, 2022: 52.6, 2023: 5.9, 2024: 6.9, 2025: 4.0}
adq = {2021: 86.8, 2022: 221.7, 2023: 82.1, 2024: 183.3, 2025: 117.6}
pagos = {2023: 130.8, 2024: 150.8, 2025: 177.9}
pasivo = {2022: 485.4, 2023: 538.3, 2024: 606.2, 2025: 703.2}
C52 = 307.933
tau5 = sum(tipo.values()) / 5
vm = sum(ventas[a] for a in A) / 3
nopat = sum(ebit[a] * (1 - tipo[a]) for a in A) / 3
v0, m0 = ventas[2025], ebit[2025] / ventas[2025]


def f_per(dx):
    reinv = sum(capex[a] - dx(a) + wc[a] for a in A) / 3
    return (nopat - reinv - C52) / vm


def s2c_total(dx):
    return (ventas[2025] - ventas[2020]) / sum(capex[a] - dx(a) + wc[a] + adq[a] for a in range(2021, 2026))


per = {"A0 (D&A total)": lambda a: da[a], "A1 (sin ROU)": lambda a: da[a] - rou[a],
       "A2 (propia)": lambda a: da[a] - rou[a] - ppa[a]}
print("1. Flujo del año 1 del escenario NORMAL (g=4,5 %, m_obj=12,5 %) con el ancla S2C propia de cada perímetro")
g, mobj = 0.045, 0.125
v1 = v0 * (1 + g); m1 = m0 + (mobj - m0) / 5
base = {}
for n, dx in per.items():
    f, s = f_per(dx), s2c_total(dx)
    f0 = v0 * (m0 * (1 - tau5) - f)
    fl1 = v1 * (m1 * (1 - tau5) - f) - (v1 - v0) / s
    base[n] = (f, s, f0)
    print(f"   {n:16s} f={f:.6f} S2C_ancla={s:.4f} F0={f0:8.3f} flujo_año1={fl1:8.3f}")
f_a0, s_a0, f0_a0 = base["A0 (D&A total)"]
for n in ("A1 (sin ROU)", "A2 (propia)"):
    f_x, s_x, f0_x = base[n]
    por_dv = (f_x + 1 / s_x) - (f_a0 + 1 / s_a0)
    dv = (f0_x - f0_a0) / por_dv
    print(f"   brecha {n} − A0: {f0_x - f0_a0:.2f} a crecimiento cero; se anula con ΔV={dv:.1f} ({100 * dv / v0:.1f} % de V0)")
cagr5 = (ventas[2025] / ventas[2020]) ** 0.2 - 1
print(f"   crecimiento medio 2020→2025 de las ventas: {100 * cagr5:.1f} % anual (ΔV medio {(ventas[2025] - ventas[2020]) / 5:.1f})")

print("\n2. Partidas puntuales dentro de F0 (cifras del propio informe del autor, §4.2)")
earn = (48.4 - 9.3 - 0.1) / 3
plus = -(4.3 + 7.3 - 23.1) / 3
print(f"   earnout y otros no monetarios en f: {-earn:.3f} mm ({-100 * earn / vm:.3f} % de ventas) -> F0 mayor en {earn / vm * v0:.2f}")
print(f"   plusvalías netas en f: {plus:+.3f} mm ({100 * plus / vm:.3f} % de ventas) -> F0 menor en {plus / vm * v0:.2f}")
print(f"   plusvalía de 25,7 dentro de m0: {100 * 25.7 / v0:.3f} puntos de margen -> F0 mayor en {25.7 * (1 - tau5):.2f}")
print(f"   efecto neto en F0 de cualquier perímetro: {earn / vm * v0 - plus / vm * v0 + 25.7 * (1 - tau5):+.2f}")
n23 = (ebit[2023] + 48.9) * (1 - 110.3 / (372.2 + 48.9))
print(f"   (si además se cuenta el efecto del earnout no deducible en el tipo de 2023: NOPAT 2023 {ebit[2023] * (1 - tipo[2023]):.1f} -> {n23:.1f};"
      f" F0 mayor en {(n23 - ebit[2023] * (1 - tipo[2023])) / 3 / vm * v0:.2f} por el earnout)")

print("\n3. Pagos de arrendamiento sobre ventas y pasivo")
for a in A:
    print(f"   {a}: pagos/ventas {100 * pagos[a] / ventas[a]:.2f} %  ROU/ventas {100 * rou[a] / ventas[a]:.2f} %  pasivo {pasivo[a]} ({100 * (pasivo[a] / pasivo[a - 1] - 1):+.1f} %)  ventas {100 * (ventas[a] / ventas[a - 1] - 1):+.1f} %")
print(f"   media 2023–25 de pagos/ventas medias: {100 * sum(pagos.values()) / 3 / vm:.3f} % ; 2025: {100 * pagos[2025] / v0:.3f} %"
      f" ; diferencia a ventas 2025: {pagos[2025] - sum(pagos.values()) / 3 / vm * v0:.1f} mm")

print("\n4. Relaciones con clientes y diferido de intangibles")
print(f"   valor neto 275,1 ÷ amortización 83,5 = {275.1 / 83.5:.2f} años")
for a, d, am in ((2023, 15.5, 84.6), (2024, 20.3, 83.9), (2025, 17.5, 83.5)):
    print(f"   {a}: ingreso por diferido de intangibles {d} ÷ amortización de relaciones con clientes {am} = {100 * d / am:.1f} %")
print(f"   lino plano sobre ventas 2025: {100 * 2217.4 / 4796.8:.1f} %")
