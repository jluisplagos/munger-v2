"""Réplica independiente (revisor) de los flujos del motor A a partir de Convenciones_financieras_V6_3.md §1–§3.
Lee del libro solo entradas y valores en caché (solo lectura) y compara flujos de los años 1–10 y del año 11.
No calcula valores por acción ni precios.

Uso: python3 -I replica_motor_A.py <Elis_v63_evaluada.xlsx>
"""
import sys
import openpyxl


def main():
    wb = openpyxl.load_workbook(sys.argv[1], data_only=True, read_only=True)
    hi, pa, an, mo = wb["Historia"], wb["Palancas"], wb["Análisis"], wb["Motor"]
    v0 = hi["L6"].value
    m0 = hi["L7"].value / hi["L6"].value
    tau = sum(hi[c + "10"].value for c in "HIJKL") / 5
    f = hi["C58"].value
    cols = ["AU", "AV", "AW", "AX", "AY", "AZ", "BA", "BB", "BC", "BD"]
    peor = 0.0
    for fila, col in ((6, "B"), (7, "C"), (8, "D")):
        g15, mobj, s2c, roic = (pa[f"{col}{n}"].value for n in (14, 15, 16, 18))
        ginf = an[f"{col}68"].value
        vprev = v0
        for t in range(1, 11):
            g = g15 if t <= 5 else g15 - (g15 - ginf) * (t - 5) / 5
            v = vprev * (1 + g)
            m = m0 + (mobj - m0) * min(t, 5) / 5
            flujo = v * (m * (1 - tau) - f) - (v - vprev) / s2c
            libro = mo[f"{cols[t - 1]}{fila}"].value
            peor = max(peor, abs(flujo - libro))
            vprev = v
        term = vprev * (1 + ginf) * (mobj * (1 - tau) * (1 - ginf / roic) - f)
        peor = max(peor, abs(term - mo[f"BF{fila}"].value))
        print(f"fila {fila}: g15={g15} m_obj={mobj} S2C={s2c} ROIC={roic} g_inf={ginf} · flujo año 11 réplica={term:.6f} libro={mo[f'BF{fila}'].value:.6f}")
    print(f"V0={v0} m0={m0:.12f} tau5={tau:.6f} f={f:.15f}")
    print(f"flujo sin crecimiento V0·[m0(1−τ)−f] = {v0 * (m0 * (1 - tau) - f):.6f}")
    print(f"máxima diferencia absoluta réplica − libro en 33 flujos: {peor:.3e}")


if __name__ == "__main__":
    main()
