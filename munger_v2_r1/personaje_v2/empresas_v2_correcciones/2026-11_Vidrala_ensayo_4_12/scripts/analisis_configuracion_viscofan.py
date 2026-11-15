#!/usr/bin/env python3
"""Análisis propio de las entradas de la configuración experimental de Viscofan (encargo 4.12 §8). Solo lee; no transfiere nada de Vidrala.

1. Cifras de las publicaciones recuperadas (viscofan/fuentes/texto/*.txt, con marcas [PDF PAGE n]): cada cifra impresa se busca en la
   página citada y el script se detiene si no está (una cifra que no se puede comprobar no entra).
2. N1 · tipo: efectivo por año (Historia, fila del tipo) y conciliación con el tipo de Navarra (28 %) de 2021–2025; lecturas con las
   activaciones de bases imponibles negativas fuera (lo que la empresa da como causa del 10,1 % de 2025) y, además, sin los ajustes de
   ejercicios anteriores. Período y perímetro: los de la regla heredada (2021–2025, actividades continuadas).
3. N2 · margen de partida: margen EBIT de la Historia por año; regla heredada (Palancas C8 «Último año»), ciclo 2021–2025 y serie de
   diez años; perímetro (adquisiciones de 2024–2025) y partidas no recurrentes identificadas.
4. N3 · circulante comercial de 2025 (balance) conciliado con las notas 9 y 14, y la misma razón en 2024.
5. Capex, amortización y adquisiciones 2021–2025 (estado de flujos y cuenta de resultados), con la amortización de derechos de uso
   separada (se repone con arrendamientos, no con capex).
6. Bases históricas de la hoja «Configuración V6.4» (B54:B63) calculadas con las fórmulas de la plantilla sobre la Historia H–L, y los
   factores f, f_fija y el nivel de cada familia en función de su parámetro (θ en [0, 1]; λ ≥ 1), con los límites de dominio:
   λ a partir del cual SRF o f dejan de estar definidos y el S2C a partir del cual la inversión fija para crecer sería negativa.
Uso (desde munger_v2_r1/): python3 -I …/scripts/analisis_configuracion_viscofan.py
Escribe viscofan/configuracion/analisis_configuracion_viscofan.json y .md. Código 0 si todas las cifras están en su página.
"""
import json
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
EXP = os.path.dirname(AQUI)
PV = os.path.abspath(os.path.join(EXP, "..", ".."))
RAIZ = os.path.dirname(PV)
TXT = os.path.join(EXP, "viscofan", "fuentes", "texto")
ORIG = os.path.join(PV, "empresas_v2", "Viscofan")
OUT = os.path.join(EXP, "viscofan", "configuracion")

# (id, concepto, ejercicio, cifra impresa, archivo, página PDF). Miles de euros salvo que se diga otra cosa.
CIFRAS = [
    # --- impuesto: conciliación con el tipo de Navarra
    ("T25_bai", "resultado antes de impuestos de continuadas", 2025, "176,254", "AR_2025.txt", 109),
    ("T25_gasto", "gasto por impuesto", 2025, "17,784", "AR_2025.txt", 109),
    ("T25_bin", "activación de bases imponibles negativas", 2025, "-18,009", "AR_2025.txt", 109),
    ("T25_ant", "ajustes de ejercicios anteriores y otros", 2025, "-2,122", "AR_2025.txt", 109),
    ("T24_bai", "resultado antes de impuestos de continuadas", 2024, "206,438", "AR_2025.txt", 109),
    ("T24_gasto", "gasto por impuesto", 2024, "49,105", "AR_2025.txt", 109),
    ("T24_bin", "activación de bases imponibles negativas", 2024, "-2,493", "AR_2025.txt", 109),
    ("T24_ant", "ajustes de ejercicios anteriores y otros", 2024, "6,905", "AR_2025.txt", 109),
    ("T25_tipo_navarra", "tipo de Navarra de la conciliación", 2025, "Tax rate at 28%", "AR_2025.txt", 109),
    ("T25_causa", "causa del 10,1 % según la empresa", 2025, "tax bases in the US worth €18.0 million", "AR_2025.txt", 142),
    ("T25_10_1", "tipo efectivo de 2025 según la empresa", 2025, "effective tax rate of 10.1%", "AR_2025.txt", 142),
    ("T25_impacto", "impacto de la activación en resultados", 2025, "18,009 thousand euros (2,493 thousand euros in 2024)", "AR_2025.txt", 108),
    ("T25_activo_bin", "activo por impuesto diferido por bases imponibles negativas", 2025, "€26,731 thousand", "AR_2025.txt", 105),
    ("T23_bai", "resultado antes de impuestos de continuadas", 2023, "168,906", "CF_2024.txt", 85),
    ("T23_gasto", "gasto por impuesto", 2023, "27,944", "CF_2024.txt", 85),
    ("T23_ded", "deducciones generadas o aplicadas", 2023, "-12,259", "CF_2024.txt", 85),
    ("T23_ant", "ajustes de ejercicios anteriores y otros", 2023, "-6,602", "CF_2024.txt", 85),
    ("T24_ant_cf24", "ajustes de ejercicios anteriores y otros (edición 2024, sin separar las bases negativas)", 2024, "4,412", "CF_2024.txt", 85),
    ("T23_icms", "deducción de subvenciones de ICMS en Brasil (2023)", 2023, "subvenciones de ICMS", "CA_2023_es.txt", 122),
    ("T22_bai", "resultado antes de impuestos de continuadas", 2022, "183,789", "CF_2022_compilacion.txt", 74),
    ("T22_gasto", "gasto por impuesto", 2022, "44,359", "CF_2022_compilacion.txt", 74),
    ("T22_ant", "ajustes de ejercicios anteriores y otros", 2022, "-1,700", "CF_2022_compilacion.txt", 74),
    ("T21_bai", "resultado antes de impuestos de continuadas", 2021, "176,420", "CF_2022_compilacion.txt", 74),
    ("T21_gasto", "gasto por impuesto", 2021, "43,423", "CF_2022_compilacion.txt", 74),
    ("T21_ant", "ajustes de ejercicios anteriores y otros", 2021, "-11", "CF_2022_compilacion.txt", 74),
    # --- perímetro y continuidad
    ("P25_continuadas", "resultado de continuadas = resultado del ejercicio", 2025, "Profit for the year from continuing operations 158,470 157,333", "AR_2025.txt", 23),
    ("P23_continuadas", "resultado de continuadas = resultado del ejercicio (2024 y 2023)", 2024, "157,333 140,962", "CF_2024.txt", 4),
    ("P25_perimetro", "cambios de perímetro sin efecto material en el EBITDA según la empresa", 2025, "changes having no material impact (0.0", "AR_2025.txt", 142),
    ("P25_deterioro", "deterioro y resultado por enajenación de inmovilizado", 2025, "Impairment and gain/loss on disposal of fixed assets 648", "AR_2025.txt", 23),
    # --- circulante comercial
    ("C25_ventas", "ventas y prestación de servicios", 2025, "1,251,983", "AR_2025.txt", 23),
    ("C24_ventas", "ventas y prestación de servicios", 2024, "1,203,994", "AR_2025.txt", 23),
    ("C25_exist", "existencias (balance)", 2025, "386,859", "AR_2025.txt", 21),
    ("C24_exist", "existencias (balance)", 2024, "398,954", "AR_2025.txt", 21),
    ("C25_deud", "deudores comerciales y otras cuentas a cobrar (balance)", 2025, "321,044", "AR_2025.txt", 21),
    ("C24_deud", "deudores comerciales y otras cuentas a cobrar (balance)", 2024, "305,643", "AR_2025.txt", 21),
    ("C25_acre", "acreedores comerciales y otras cuentas a pagar (balance)", 2025, "103,388", "AR_2025.txt", 22),
    ("C24_acre", "acreedores comerciales y otras cuentas a pagar (balance)", 2024, "126,164", "AR_2025.txt", 22),
    ("C25_deud_com", "total deudores comerciales (nota 9)", 2025, "Total trade debtors 289,733 279,146", "AR_2025.txt", 70),
    ("C25_deud_aapp", "administraciones públicas deudoras (nota 9)", 2025, "Public authorities receivable 24,783 20,886", "AR_2025.txt", 70),
    ("C25_deud_perio", "periodificaciones (nota 9)", 2025, "Accruals 6,528 5,611", "AR_2025.txt", 70),
    ("C25_acre_com", "acreedores comerciales (nota 14)", 2025, "Trade creditors 90,766 113,091", "AR_2025.txt", 95),
    ("C25_acre_aapp", "administraciones públicas acreedoras (nota 14)", 2025, "Payables to public authorities 12,622 13,073", "AR_2025.txt", 95),
    # --- amortización, capex, adquisiciones y arrendamientos
    ("A25_intang", "amortización de intangibles", 2025, "-5,737 -4,587", "AR_2025.txt", 23),
    ("A25_mat", "amortización del inmovilizado material", 2025, "-73,956 -73,364", "AR_2025.txt", 23),
    ("A25_rou", "amortización de derechos de uso", 2025, "-5,503 -5,843", "AR_2025.txt", 23),
    ("A25_total", "amortización total (flujos)", 2025, "85,196 83,794", "AR_2025.txt", 27),
    ("K25_capex", "pagos por inmovilizado material e intangible", 2025, "-80,447 -75,027", "AR_2025.txt", 27),
    ("K25_adq", "adquisición de dependientes neta de caja", 2025, "-8,948 -7,213", "AR_2025.txt", 27),
    ("L25_arr", "pagos por arrendamientos (derechos de uso)", 2025, "-5,503 -5,843", "AR_2025.txt", 28),
    ("A23_intang", "amortización de intangibles (2024 y 2023)", 2023, "-4,587 -4,792", "CF_2024.txt", 4),
    ("A23_mat", "amortización del inmovilizado material (2024 y 2023)", 2023, "-73,364 -73,628", "CF_2024.txt", 4),
    ("A23_rou", "amortización de derechos de uso (2024 y 2023)", 2023, "-5,843 -5,293", "CF_2024.txt", 4),
    ("K23_capex", "pagos por inmovilizado (2024 y 2023)", 2023, "-75,027 -77,126", "CF_2024.txt", 9),
    ("L23_arr", "pagos por arrendamientos (2024 y 2023)", 2023, "-5,843 -5,296", "CF_2024.txt", 9),
    ("A22_intang", "amortización de intangibles (2022 y 2021)", 2022, "−4.782 −4.345", "CF_2022_compilacion.txt", 21),
    ("A22_mat", "amortización del inmovilizado material (2022 y 2021)", 2022, "−68.076 −62.813", "CF_2022_compilacion.txt", 21),
    ("A22_rou", "amortización de derechos de uso (2022 y 2021)", 2022, "−5.289 −5.123", "CF_2022_compilacion.txt", 21),
    ("K22_capex", "pagos por inmovilizado (2022 y 2021)", 2022, "−115.566 −95.779", "CF_2022_compilacion.txt", 25),
    ("L22_arr", "pagos por arrendamientos (2022 y 2021)", 2022, "−5.289 −5.123", "CF_2022_compilacion.txt", 25),
    # --- cartera de clientes
    ("Q25_cartera", "altas de cartera de clientes de la combinación de negocios", 2025, "customer portfolio (1,294 thousand euros)", "AR_2025.txt", 33),
    ("Q25_vida", "vidas útiles de cartera, marca y know-how", 2025, "useful lives of 12, 8 and 10 years", "AR_2025.txt", 33),
]


def paginas(arch):
    t = open(os.path.join(TXT, arch), encoding="utf-8").read()
    p = re.split(r"\[PDF PAGE (\d+)\]", t)
    return {int(p[i]): re.sub(r"\s+", " ", p[i + 1]) for i in range(1, len(p), 2)}


def num(s):
    """«-18,009» → -18.009 (miles → M€) y «−4.782» (formato español) → -4.782."""
    s = s.replace("−", "-").strip()
    neg = s.startswith("-")
    d = re.sub(r"[^\d]", "", s)
    return (-1 if neg else 1) * int(d) / 1000.0


def main():
    cache, comprobadas, faltan = {}, {}, []
    for cid, conc, anio, imp, arch, pag in CIFRAS:
        P = cache.setdefault(arch, paginas(arch))
        ok = imp in (P.get(pag) or "")
        comprobadas[cid] = {"concepto": conc, "ejercicio": anio, "impreso": imp, "archivo": arch, "pagina": pag, "en_la_pagina": ok}
        if not ok:
            faltan.append(f"{cid}: «{imp}» no está en {arch} p. {pag}")
    if faltan:
        print("FALLO: cifras que no están en su página:\n" + "\n".join(faltan))
        return 1
    f1 = json.load(open(os.path.join(ORIG, "fase1_v63.json"), encoding="utf-8"))
    H = f1["historia"]["partidas"]
    anios = f1["historia"]["anios"]
    s = lambda k: dict(zip(anios, H[k]["valores"] if isinstance(H[k], dict) and "valores" in H[k] else H[k]))  # noqa: E731
    ventas, ebit, da, capex, adq, circ, tipo = s("ventas"), s("ebit"), s("da"), s("capex"), s("adquisiciones"), s("circulante"), s("tipo_impositivo")
    HL = [2021, 2022, 2023, 2024, 2025]
    # ---------------------------------------------------------------- N1
    imp = {2025: (176.254, 17.784, -18.009, -2.122), 2024: (206.438, 49.105, -2.493, 6.905), 2023: (168.906, 27.944, 0.0, -6.602),
           2022: (183.789, 44.359, 0.0, -1.700), 2021: (176.420, 43.423, 0.0, -0.011)}
    efectivo = {a: imp[a][1] / imp[a][0] for a in HL}
    sin_bin = {a: (imp[a][1] - imp[a][2]) / imp[a][0] for a in HL}
    sin_bin_ni_ant = {a: (imp[a][1] - imp[a][2] - imp[a][3]) / imp[a][0] for a in HL}
    media = lambda d: sum(d[a] for a in HL) / len(HL)  # noqa: E731
    agregado = lambda f: sum(f(a) for a in HL) / sum(imp[a][0] for a in HL)  # noqa: E731
    n1 = {"historia_fila_del_tipo": {a: tipo[a] for a in HL}, "regla_heredada_C52": media({a: tipo[a] for a in HL}),
          "efectivo_de_la_conciliacion": efectivo, "sin_activaciones_de_bases_negativas": sin_bin, "sin_activaciones_ni_ajustes_de_anteriores": sin_bin_ni_ant,
          "medias": {"heredada_C52": media({a: tipo[a] for a in HL}), "efectivo": media(efectivo), "sin_activaciones": media(sin_bin), "sin_activaciones_ni_ajustes": media(sin_bin_ni_ant),
                     "agregado_sin_activaciones": agregado(lambda a: imp[a][1] - imp[a][2]), "agregado_sin_activaciones_ni_ajustes": agregado(lambda a: imp[a][1] - imp[a][2] - imp[a][3])},
          "activo_por_bases_negativas_2025_mm": 26.731,
          "nota": ("La fila del tipo de la Historia (fase 1) va redondeada a 4 decimales; C52 es su media 2021–2025. Las activaciones de bases imponibles negativas (Estados Unidos: "
                   "18,009 en 2025 y 2,493 en 2024) son la causa que da la empresa del 10,1 % de 2025; los ajustes de ejercicios anteriores mezclan signos (−0,011; −1,700; −6,602; +6,905; −2,122) "
                   "y su media es pequeña. La deducción de 2023 por las subvenciones de ICMS en Brasil no está cuantificada por separado: no se ajusta.")}
    # ---------------------------------------------------------------- N2
    margen = {a: ebit[a] / ventas[a] for a in anios}
    n2 = {"margen_ebit_historia": margen, "ultimo_anio_regla_heredada": margen[2025], "media_2021_2025": sum(margen[a] for a in HL) / 5,
          "media_10_anios_C49": sum(margen.values()) / len(margen), "minimo": min(margen.values()), "maximo": max(margen.values()),
          "adquisiciones_historia": {a: adq[a] for a in anios},
          "nota": ("La regla heredada (Palancas C8 «Último año») da el margen de 2025; el ciclo 2021–2025 da prácticamente lo mismo. En 2025 no hay partidas no recurrentes identificadas "
                   "de importe material en el resultado de explotación (deterioro y enajenaciones +0,648) y la empresa dice que los cambios de perímetro no tuvieron efecto material en el "
                   "EBITDA (0,0 p.p.). Las adquisiciones de 2024 y 2025 (Brasil) son 7,213 y 8,948.")}
    # ---------------------------------------------------------------- N3
    c25 = {"existencias": 386.859, "deudores": 321.044, "acreedores": 103.388}
    c24 = {"existencias": 398.954, "deudores": 305.643, "acreedores": 126.164}
    com25 = {"existencias": 386.859, "deudores": 289.733, "acreedores": 90.766}
    nwc = lambda c, v: (c["existencias"] + c["deudores"] - c["acreedores"]) / v  # noqa: E731
    n3 = {"balance_2025": c25, "nwc_balance_2025": nwc(c25, 1251.983), "balance_2024": c24, "nwc_balance_2024": nwc(c24, 1203.994),
          "solo_comercial_2025": com25, "nwc_solo_comercial_2025": nwc(com25, 1251.983),
          "conciliacion_2025": {"deudores": "321,044 = deudores comerciales 289,733 + administraciones públicas 24,783 + periodificaciones 6,528 (nota 9, p. 70)",
                                "acreedores": "103,388 = acreedores comerciales 90,766 + administraciones públicas 12,622 (nota 14, p. 95)"},
          "ventas_del_ultimo_anio_C44": ventas[2025],
          "nota": "Se usan las líneas del balance (como la definición B29:B31 de la plantilla); la lectura solo comercial de las notas baja la razón en 1,5 puntos."}
    # ---------------------------------------------------------------- capex y amortización
    rou = {2021: 5.123, 2022: 5.289, 2023: 5.293, 2024: 5.843, 2025: 5.503}
    intang = {2021: 4.345, 2022: 4.782, 2023: 4.792, 2024: 4.587, 2025: 5.737}
    mat = {2021: 62.813, 2022: 68.076, 2023: 73.628, 2024: 73.364, 2025: 73.956}
    k = {"capex_historia": {a: capex[a] for a in HL}, "da_historia": {a: da[a] for a in HL}, "da_suma_de_componentes": {a: round(intang[a] + mat[a] + rou[a], 3) for a in HL},
         "da_sin_derechos_de_uso": {a: round(intang[a] + mat[a], 3) for a in HL}, "amortizacion_derechos_de_uso": rou,
         "capex_menos_da": {a: round(capex[a] - da[a], 3) for a in HL}, "capex_menos_da_sin_derechos_de_uso": {a: round(capex[a] - da[a] + rou[a], 3) for a in HL},
         "capex_sobre_da": {a: capex[a] / da[a] for a in HL},
         "capex_sobre_da_10_anios": sum(capex[a] for a in anios) / sum(da[a] for a in anios),
         "ventas_crecimiento_2021_2025": ventas[2025] / ventas[2021] - 1,
         "nota": ("La D&A de la Historia incluye la amortización de los derechos de uso (5,1–5,8 al año), que se repone con arrendamientos (financiación) y no con capex: la plantilla no la "
                  "separa, así que el «exceso histórico» de la familia Θ (Σ capex − D&A) queda 27,1 por debajo del exceso sobre la amortización que se repone con capex, y la base de la "
                  "familia Λ (D&A₀) incluye 5,5 que no se reponen con capex. Es un límite de definición de la plantilla, no se corrige en la configuración.")}
    # ---------------------------------------------------------------- bases históricas (fórmulas de la plantilla, legado)
    s31 = sum(capex[a] - da[a] + (adq[a] or 0) + circ[a] for a in HL)
    B = {"B54_DA0": da[2025], "B55_reinversion_neta": s31, "B56_cartera": 0.0, "B57_D_hist": s31, "B58_capex_menos_da": sum(capex[a] for a in HL) - sum(da[a] for a in HL),
         "B59_adquisiciones": sum((adq[a] or 0) for a in HL)}
    B["B60_exceso"] = B["B58_capex_menos_da"] + B["B56_cartera"]
    B["B61_exceso_medio"] = B["B60_exceso"] / 5
    B["B62_F_hist"] = B["B60_exceso"] + B["B59_adquisiciones"]
    B["B63_amortizacion_que_se_repone"] = sum(da[a] for a in HL) - B["B56_cartera"]
    s2c_hist = (ventas[2025] - ventas[2020]) / s31

    def theta(t):
        rh = t * B["B60_exceso"]
        return {"theta": t, "Rh": rh, "f": B["B57_D_hist"] / (B["B57_D_hist"] - rh), "f_fija": 1 - rh / B["B62_F_hist"], "nivel_anual": t * B["B61_exceso_medio"]}

    def lam(x):
        rh = (x - 1) * B["B63_amortizacion_que_se_repone"]
        dh = B["B57_D_hist"] - rh
        return {"lambda": x, "Rh": rh, "f": (B["B57_D_hist"] / dh) if dh > 0 else None, "f_fija": 1 - rh / B["B62_F_hist"], "requisito_anual": (x - 1) * B["B54_DA0"]}
    dominio = {"lambda_max_SRF_definida": 1 + B["B62_F_hist"] / B["B63_amortizacion_que_se_repone"],
               "lambda_max_f_definida": 1 + B["B57_D_hist"] / B["B63_amortizacion_que_se_repone"],
               "theta_SRF_definida_en_todo_0_1": theta(1.0)["f_fija"] >= 0,
               "S2C_por_f_umbral_inversion_fija_negativa": 1 / n3["nwc_balance_2025"],
               "S2C_umbral_con_f_theta_0_5": 1 / (n3["nwc_balance_2025"] * theta(0.5)["f"]), "S2C_umbral_con_f_theta_1": 1 / (n3["nwc_balance_2025"] * theta(1.0)["f"])}
    out = {"empresa": "Viscofan", "base_economica": "2025-12-31", "fuentes": "viscofan/fuentes/inventario_fuentes_viscofan.md", "cifras_comprobadas": comprobadas,
           "N1": n1, "N2": n2, "N3": n3, "capex_y_amortizacion": k, "bases_historicas": B, "s2c_historico_C53": s2c_hist,
           "familia_theta": [theta(t) for t in (0.0, 0.25, 0.5, 0.75, 1.0)], "familia_lambda": [lam(x) for x in (1.0, 1.05, 1.10, 1.14, 1.15, 1.25, 1.5)],
           "dominios": dominio, "cartera": {"altas_2025_mm": 1.294, "vida_util_anios": 12, "amortizacion_anual_aprox_mm": 1.294 / 12,
                                             "nota": "cartera de clientes de la combinación de negocios de Brasil: inmaterial (≈0,11 al año); sin cartera identificada en 2021–2024 en esta revisión, la ausencia no confirma ceros: no se usa P0"}}
    os.makedirs(OUT, exist_ok=True)
    json.dump(out, open(os.path.join(OUT, "analisis_configuracion_viscofan.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    pc = lambda x: f"{100 * x:.2f} %"  # noqa: E731
    f3 = lambda x: f"{x:.3f}" if isinstance(x, (int, float)) else "—"  # noqa: E731
    md = ["# Viscofan · análisis propio de las entradas de la configuración experimental (encargo 4.12 §8)", "",
          f"Base económica 31-dic-2025. Todas las cifras se han buscado en su página ({len(CIFRAS)} de {len(CIFRAS)} encontradas; tabla al final). Millones de euros salvo que se diga otra cosa. "
          "Nada de esto viene de Vidrala; nada se adopta.", "",
          "## N1 · tipo impositivo (perímetro: actividades continuadas, consolidado; período: 2021–2025, el de la regla heredada)", "",
          "| Año | Fila del tipo (Historia) | Efectivo (conciliación) | Sin activaciones de bases negativas | Además sin ajustes de años anteriores |", "|---|---|---|---|---|"]
    md += [f"| {a} | {pc(tipo[a])} | {pc(efectivo[a])} | {pc(sin_bin[a])} | {pc(sin_bin_ni_ant[a])} |" for a in HL]
    m = n1["medias"]
    md += [f"| **Media** | **{pc(m['heredada_C52'])}** (C52, regla heredada) | {pc(m['efectivo'])} | **{pc(m['sin_activaciones'])}** | {pc(m['sin_activaciones_ni_ajustes'])} |", "",
           n1["nota"], f"Agregado 2021–2025 (Σ impuesto ÷ Σ resultado antes de impuestos): sin activaciones {pc(m['agregado_sin_activaciones'])}; además sin ajustes {pc(m['agregado_sin_activaciones_ni_ajustes'])}. "
           "El activo por impuesto diferido de las bases negativas (26,731 a 31-dic-2025) no entra en el motor B.", "",
           "## N2 · margen de partida", "", "| Año | " + " | ".join(str(a) for a in anios) + " |", "|---|" + "---|" * len(anios),
           "| Margen EBIT | " + " | ".join(pc(margen[a]) for a in anios) + " |", "",
           f"Regla heredada (Palancas C8 «Último año»): {pc(n2['ultimo_anio_regla_heredada'])}. Media 2021–2025: {pc(n2['media_2021_2025'])}. Diez años (C49): {pc(n2['media_10_anios_C49'])}; "
           f"mínimo {pc(n2['minimo'])}, máximo {pc(n2['maximo'])}. {n2['nota']}", "",
           "## N3 · circulante comercial", "",
           f"- 2025 (balance, p. 21–22): existencias 386,859 + deudores 321,044 − acreedores 103,388 = {f3(386.859 + 321.044 - 103.388)} sobre ventas {f3(ventas[2025])} → **{pc(n3['nwc_balance_2025'])}**.",
           f"- 2024 (mismas líneas): {pc(n3['nwc_balance_2024'])}. Solo comercial (notas 9 y 14): {pc(n3['nwc_solo_comercial_2025'])}.",
           f"- Conciliación: {n3['conciliacion_2025']['deudores']}; {n3['conciliacion_2025']['acreedores']}. {n3['nota']}", "",
           "## Capex, amortización y adquisiciones (2021–2025)", "", "| Año | Capex | D&A | de ella, derechos de uso | Capex − D&A | Capex − D&A sin derechos de uso | Capex ÷ D&A | Adquisiciones |", "|---|---|---|---|---|---|---|---|"]
    md += [f"| {a} | {f3(capex[a])} | {f3(da[a])} | {f3(rou[a])} | {f3(capex[a] - da[a])} | {f3(capex[a] - da[a] + rou[a])} | {capex[a] / da[a]:.2f} | {f3(adq[a] or 0)} |" for a in HL]
    md += ["", f"Capex ÷ D&A en diez años: {k['capex_sobre_da_10_anios']:.2f}; ventas 2021→2025: +{pc(k['ventas_crecimiento_2021_2025'])}. {k['nota']}", "",
           "## Bases históricas de «Configuración V6.4» (fórmulas de la plantilla; cartera legado)", "",
           "; ".join(f"{kk} {f3(vv)}" for kk, vv in B.items()) + f". S2C histórico (C53) {s2c_hist:.4f}.", "",
           "| θ | Rh | f (SR1, SR2) | f_fija (SRF) | nivel anual |", "|---|---|---|---|---|"]
    md += [f"| {x['theta']} | {f3(x['Rh'])} | {x['f']:.4f} | {x['f_fija']:.4f} | {f3(x['nivel_anual'])} |" for x in out["familia_theta"]]
    md += ["", "| λ | Rh | f (SR1, SR2) | f_fija (SRF) | requisito anual |", "|---|---|---|---|---|"]
    md += [f"| {x['lambda']} | {f3(x['Rh'])} | {('%.4f' % x['f']) if x['f'] else 'no definido'} | {x['f_fija']:.4f}{' (fuera de [0, 1]: SRF no definida)' if x['f_fija'] < 0 else ''} | {f3(x['requisito_anual'])} |" for x in out["familia_lambda"]]
    md += ["", f"**Dominios.** Con Λ, SRF deja de estar definida por encima de λ = {dominio['lambda_max_SRF_definida']:.4f} y f por encima de λ = {dominio['lambda_max_f_definida']:.4f}. "
           f"Con Θ, todo θ en [0, 1] está definido. La inversión fija para crecer de R1 sería negativa si S2C × f > 1 ÷ NWC = {dominio['S2C_por_f_umbral_inversion_fija_negativa']:.3f} "
           f"(S2C > {dominio['S2C_umbral_con_f_theta_0_5']:.3f} con θ = 0,5; > {dominio['S2C_umbral_con_f_theta_1']:.3f} con θ = 1).", "",
           f"**Cartera.** {out['cartera']['nota']}.", "", "## Cifras comprobadas", "", "| Id | Concepto | Ejercicio | Cifra | Fuente |", "|---|---|---|---|---|"]
    md += [f"| {cid} | {x['concepto']} | {x['ejercicio']} | «{x['impreso']}» | {x['archivo']}, PDF p. {x['pagina']} |" for cid, x in comprobadas.items()]
    open(os.path.join(OUT, "analisis_configuracion_viscofan.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
    print(f"OK: {len(CIFRAS)} cifras en su página · N1 heredada {pc(m['heredada_C52'])} → sin activaciones {pc(m['sin_activaciones'])} · NWC {pc(n3['nwc_balance_2025'])} · "
          f"D_hist {f3(B['B57_D_hist'])} · exceso {f3(B['B60_exceso'])} · λ máx. SRF {dominio['lambda_max_SRF_definida']:.4f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
