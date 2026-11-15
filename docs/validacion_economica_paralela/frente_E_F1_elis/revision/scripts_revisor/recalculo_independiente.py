"""Recálculo independiente del revisor (paso A de la revisión del frente E, F1 de Elis).

Las cifras se transcribieron a mano de los PDF (pdftotext -layout) ANTES de leer el informe del autor.
Cada cifra lleva documento y página PDF. Millones de euros. Solo biblioteca estándar.

Uso: python3 -I recalculo_independiente.py [ruta_libro.xlsx]
Si se pasa el libro (y hay openpyxl), se comparan los resultados con sus valores en caché (solo lectura).
"""
import json
import sys

# --- Cifras transcritas (documento · página PDF) -------------------------------------------------
# URD2025 = «Elis - 2025 Universal Registration Document.pdf»; DEU2024 = «Elis_Document d'enregistrement
# universel_2024_FR.pdf». 2023 = comparativo «retraité» de DEU2024; 2024 = comparativo «restated» de URD2025.
A = [2023, 2024, 2025]
ventas = {2023: 4309.4, 2024: 4573.7, 2025: 4796.8}            # DEU2024 p.270 ; URD2025 p.324
ebit = {2023: 496.8, 2024: 596.3, 2025: 629.9}                  # DEU2024 p.270 ; URD2025 p.324 (impreso 629,9)
ebit_libro = {2023: 496.8, 2024: 596.3, 2025: 630.0}            # Historia J7:L7 (630,0 = 492,9 + 137,1)
rn = {2023: 261.9, 2024: 337.7, 2025: 366.6}                    # DEU2024 p.273 ; URD2025 p.327
imp_gasto = {2023: 110.3, 2024: 128.3, 2025: 126.2}
fin_neto = {2023: 124.6, 2024: 130.4, 2025: 137.1}
sbc = {2023: 22.9, 2024: 27.1, 2025: 34.7}
da_prov_cf = {2023: 886.0, 2024: 963.4, 2025: 1020.8}           # línea del estado de flujos
subv = {2023: -0.5, 2024: -0.9, 2025: -1.0}
plusv = {2023: 4.3, 2024: 7.3, 2025: -23.1}
earnout = {2023: 48.4, 2024: -9.3, 2025: -0.1}
caf = {2023: 1457.9, 2024: 1584.0, 2025: 1661.3}                # cash flow before finance costs and tax
wc5 = {2023: (12.3, -66.6, -1.4, 1.7, 52.5), 2024: (-14.0, -15.8, -3.5, 10.6, 21.3),
       2025: (-5.3, -63.6, -2.4, 11.4, 59.9)}
otros_wc = {2023: -0.9, 2024: -3.2, 2025: -1.2}
personal = {2023: -3.5, 2024: -2.3, 2025: -2.8}
imp_pagado = {2023: 126.4, 2024: 124.9, 2025: 146.7}
cfo = {2023: 1325.6, 2024: 1452.1, 2025: 1510.6}
capex_intang = {2023: 26.8, 2024: 26.6, 2025: 26.2}
capex_ppe = {2023: 797.1, 2024: 860.8, 2025: 864.0}
cobros_intang = {2023: 0.1, 2024: 0.0, 2025: 0.0}
cobros_ppe = {2023: 2.8, 2024: 7.3, 2025: 15.3}
subv_inv = {2023: 0.3, 2024: 4.1, 2025: 0.2}
adquis = {2023: 82.1, 2024: 183.3, 2025: 117.6}
pagos_lease = {2023: 130.8, 2024: 150.8, 2025: 177.9}
int_fin = {2023: 70.5, 2024: 78.9, 2025: 99.4}
net_capex_pub = {2023: 820.8, 2024: 876.0, 2025: 874.7}         # DEU2024 p.259 ; URD2025 p.314
fcf_pub = {2023: 303.6, 2024: 346.3, 2025: 358.6}               # DEU2024 p.259 (2024 original 346,4) ; URD2025 p.314
principal = {2023: 111.0, 2024: 125.0, 2025: 148.3}             # DEU2024 p.312 ; URD2025 p.366
int_lease_devengo = {2023: 19.8, 2024: 25.8, 2025: 29.2}        # DEU2024 p.324 ; URD2025 p.379
# Nota 4.5 (DEU2024 p.296 para 2023; URD2025 p.350 para 2024 reexpresado y 2025)
da_textil = {2023: 482.1, 2024: 537.6, 2025: 565.1}
da_otros_art = {2023: 32.7, 2024: 35.3, 2025: 36.3}
da_otros = {2023: 161.6, 2024: 172.5, 2025: 183.6}
da_rou = {2023: 115.8, 2024: 132.2, 2025: 149.5}
da_subv = {2023: 0.5, 2024: 0.9, 2025: 1.0}                     # resta
da_deterioro = {2023: 0.0, 2024: 3.3, 2025: 0.1}
da_ppa = {2023: 85.7, 2024: 85.0, 2025: 85.7}
da_total = {2023: 877.4, 2024: 965.1, 2025: 1019.4}             # total impreso (neto de subvenciones)
tipo = {2023: 0.2963, 2024: 0.2754, 2025: 0.2560}               # Historia J10:L10 (gasto ÷ BAI)
tipo5 = 0.2882                                                  # Historia C52 (media 2021–25 del libro)
bai = {2023: 372.2, 2024: 465.9, 2025: 492.9}
imp_corriente = {2023: 120.3, 2024: 127.7, 2025: 147.2}         # nota 9
imp_diferido = {2023: -10.1, 2024: 0.6, 2025: -21.0}


def media(d):
    return sum(d[a] for a in A) / len(A)


def main():
    r = {}
    # 1. Sumas de control de los estados de flujos (residuos de redondeo)
    for a in A:
        s_caf = rn[a] + imp_gasto[a] + fin_neto[a] + sbc[a] + da_prov_cf[a] + subv[a] + plusv[a] + earnout[a]
        s_cfo = caf[a] + sum(wc5[a]) + otros_wc[a] + personal[a] - imp_pagado[a]
        capex_bruto = capex_intang[a] + capex_ppe[a]
        capex_neto_lineas = capex_bruto - cobros_intang[a] - cobros_ppe[a] - subv_inv[a]
        wc = -(sum(wc5[a]) + otros_wc[a] + personal[a])
        fcf_lineas = caf[a] - net_capex_pub[a] - wc - int_fin[a] - imp_pagado[a] - pagos_lease[a]
        da_suma = (da_textil[a] + da_otros_art[a] + da_otros[a] + da_rou[a] - da_subv[a]
                   + da_deterioro[a] + da_ppa[a])
        r[a] = {
            "residuo_CAF": round(caf[a] - s_caf, 3), "residuo_CFO": round(cfo[a] - s_cfo, 3),
            "capex_bruto": round(capex_bruto, 3), "capex_neto_por_lineas": round(capex_neto_lineas, 3),
            "residuo_capex_neto_publicado": round(net_capex_pub[a] - capex_neto_lineas, 3),
            "aumento_circulante": round(wc, 3),
            "FCF_por_lineas": round(fcf_lineas, 3), "residuo_FCF_publicado": round(fcf_pub[a] - fcf_lineas, 3),
            "interes_lease_implicito": round(pagos_lease[a] - principal[a], 3),
            "interes_lease_devengado": int_lease_devengo[a],
            "DA_suma_componentes": round(da_suma, 3), "residuo_DA_total": round(da_total[a] - da_suma, 3),
            "tipo_efectivo_recalculado": round(imp_gasto[a] / bai[a], 5),
            "EBIT_por_RN+imp+fin": round(rn[a] + imp_gasto[a] + fin_neto[a], 3),
        }
    # 2. C46–C52
    c46 = media(cfo); c47 = media(net_capex_pub)
    c48 = media(int_fin) + sum(pagos_lease[a] - principal[a] for a in A) / 3
    c49 = media(principal); c50 = media(sbc)
    c52 = c46 - c47 - c48 - c49 - c50
    # 3. f (convención 10) con las entradas del libro (EBIT 630,0 en 2025, capex bruto, D&A total)
    vm = media(ventas)
    nopat = sum(ebit_libro[a] * (1 - tipo[a]) for a in A) / 3
    capex_b = {a: capex_intang[a] + capex_ppe[a] for a in A}
    wc_a = {a: -(sum(wc5[a]) + otros_wc[a] + personal[a]) for a in A}
    reinv = sum(capex_b[a] - da_total[a] + wc_a[a] for a in A) / 3
    f = (nopat - reinv - c52) / vm
    v0 = ventas[2025]; m0 = ebit_libro[2025] / v0
    flujo0 = v0 * (m0 * (1 - tipo5) - f)
    esc = v0 / vm
    # 4. Composición de f·Vmedia (derivación propia)
    otros_no_caja = {a: cfo[a] - (ebit_libro[a] + da_total[a] - wc_a[a] - imp_pagado[a]) for a in A}
    comp = {
        "pagos_lease_medios": media(pagos_lease),
        "interes_financiero_neto_medio": media(int_fin),
        "SBC_restada_en_FCF_base": media(sbc),
        "SBC_sumada_en_CFO(-)": -media(sbc),
        "impuesto_pagado_menos_tipo_x_EBIT": media(imp_pagado) - sum(ebit_libro[a] * tipo[a] for a in A) / 3,
        "capex_bruto_menos_neto(-)": -(media(capex_b) - c47),
        "otros_no_monetarios_del_CFO_sin_SBC(-)": -(media(otros_no_caja) - media(sbc)),
    }
    comp_total = sum(comp.values())
    # 5. Descomposición de la reinversión media
    da_propios = {a: da_textil[a] + da_otros_art[a] + da_otros[a] - da_subv[a] for a in A}
    desc = {
        "capex_bruto_medio": media(capex_b), "DA_activos_propios_media": media(da_propios),
        "capex_menos_DA_propios": media(capex_b) - media(da_propios),
        "ROU(-)": -media(da_rou), "PPA(-)": -media(da_ppa), "deterioro(-)": -media(da_deterioro),
        "redondeo_DA(-)": -(media(da_total) - media(da_propios) - media(da_rou) - media(da_ppa) - media(da_deterioro)),
        "circulante": media(wc_a),
    }
    desc_total = (desc["capex_menos_DA_propios"] + desc["ROU(-)"] + desc["PPA(-)"] + desc["deterioro(-)"]
                  + desc["redondeo_DA(-)"] + desc["circulante"])
    # 6. Puente FCF base -> flujo sin crecimiento
    puente = {
        "FCF_base": c52, "efecto_escala_V0/Vmedia": c52 * (esc - 1),
        "efecto_margen_y_tipo": v0 * m0 * (1 - tipo5) - esc * nopat,
        "reinversion_media_escalada": esc * reinv,
    }
    puente_total = sum(puente.values())
    # 7. Variantes ilustrativas (NO son propuestas): quitar del perímetro ROU, o ROU y PPA
    def variante(quita_rou, quita_ppa):
        e = {a: ebit_libro[a] + (da_rou[a] - pagos_lease[a] if quita_rou else 0) + (da_ppa[a] if quita_ppa else 0)
             for a in A}
        d = {a: da_total[a] - (da_rou[a] if quita_rou else 0) - (da_ppa[a] if quita_ppa else 0) for a in A}
        n = sum(e[a] * (1 - tipo[a]) for a in A) / 3
        rv = sum(capex_b[a] - d[a] + wc_a[a] for a in A) / 3
        fv = (n - rv - c52) / vm
        return {"NOPAT_medio": n, "reinversion_media": rv, "f": fv,
                "flujo_sin_crecimiento": v0 * (e[2025] / v0 * (1 - tipo5) - fv)}
    out = {
        "controles_por_ano": r,
        "C46": c46, "C47": c47, "C48": c48, "C49": c49, "C50": c50, "C52": c52,
        "ventas_medias": vm, "NOPAT_medio": nopat, "reinversion_media": reinv, "f": f, "f_x_Vmedia": f * vm,
        "V0": v0, "m0": m0, "flujo_sin_crecimiento": flujo0, "f_x_V0": f * v0,
        "NOPAT_medio_menos_fVm": nopat - f * vm, "FCF_base_mas_reinversion": c52 + reinv,
        "composicion_f_x_Vmedia": comp, "composicion_total": comp_total,
        "descomposicion_reinversion": desc, "descomposicion_total": desc_total,
        "puente_FCFbase_a_flujo0": puente, "puente_total": puente_total,
        "variante_sin_ROU_cash": variante(True, False), "variante_sin_ROU_ni_PPA": variante(True, True),
        "FCF_2025_con_SBC": cfo[2025] - net_capex_pub[2025] - int_fin[2025] - pagos_lease[2025] - sbc[2025],
    }
    print(json.dumps(out, ensure_ascii=False, indent=1))
    if len(sys.argv) > 1:
        import openpyxl
        wb = openpyxl.load_workbook(sys.argv[1], data_only=True, read_only=True)
        an, hi, mo = wb["Análisis"], wb["Historia"], wb["Motor"]
        pares = [("Análisis!C46", an["C46"].value, c46), ("Análisis!C47", an["C47"].value, c47),
                 ("Análisis!C48", an["C48"].value, c48), ("Análisis!C49", an["C49"].value, c49),
                 ("Análisis!C50", an["C50"].value, c50), ("Análisis!C52", an["C52"].value, c52),
                 ("Historia!C74", hi["C74"].value, vm), ("Historia!C75", hi["C75"].value, nopat),
                 ("Historia!C76", hi["C76"].value, reinv), ("Historia!C58", hi["C58"].value, f),
                 ("Motor!D6", mo["D6"].value, m0), ("Motor!L6", mo["L6"].value, f)]
        print("\nComparación con el libro (caché):")
        for nombre, libro, mio in pares:
            print(f"  {nombre:14s} libro={libro!r:22} revisor={mio:.9f} dif={mio - libro:+.6f}")


if __name__ == "__main__":
    main()
