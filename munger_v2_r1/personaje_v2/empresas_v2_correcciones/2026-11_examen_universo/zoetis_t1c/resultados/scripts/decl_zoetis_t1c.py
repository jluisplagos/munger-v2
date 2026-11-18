#!/usr/bin/env python3
"""zoetis_t1c · declaración F1 del motor A con US GAAP (motor_a_f1.json). Uso: python3 -I decl_zoetis_t1c.py CARPETA_EMPRESA SALIDA.json
Aplica las decisiones registradas (F1 (1a)–(5b) y E8.1 del 17-nov; Examen F1-A y F1-B; D-US1, D-US2, D-US2 bis y D-WM del 18-nov-2026). Cifras
publicadas con su página del texto del expediente; nada estimado. Preparada por un agente de la orquestación; no acredita aptitud."""
import hashlib, json, os, sys
from collections import OrderedDict as O

C, SAL = sys.argv[1], sys.argv[2]
h = lambda p: hashlib.sha256(open(os.path.join(C, p), "rb").read()).hexdigest()  # noqa: E731
D25, D22, D21 = "Zoetis · Form 10-K FY2025", "Zoetis · Form 10-K FY2022", "Zoetis · Form 10-K FY2021"
ARCH = {D25: "texto/zoetis-10k-fy2025.txt", D22: "texto/zoetis-10k-fy2022.txt", D21: "texto/zoetis-10k-fy2021.txt"}
DEC = "munger-v2-evidencias-mistral, coordinacion/cierre_v2/DECISIONES_PARA_EL_USUARIO.md"
REG = lambda fecha, motivo: O([("fecha", fecha), ("persona", "persona responsable del proyecto (decisión registrada; no se firma aquí)"), ("motivo", motivo)])  # noqa: E731


def cifra(doc, pagina, fila, lit, nota=None, columna=None):
    v = 0 if lit in ("—", "-") else float(lit.replace(",", ""))
    e = O([("valor_fuente", v), ("signo", 1), ("tratamiento", "ninguno"), ("documento", doc), ("archivo", ARCH[doc]), ("pagina", pagina), ("literal", lit), ("fila", fila)])
    if columna:
        e["columna"] = columna
    if nota:
        e["nota"] = nota
    return e


def cero(doc, pagina, motivo, cita, nota=None):
    e = O([("valor_fuente", 0), ("signo", 1), ("tratamiento", "ninguno"), ("documento", doc), ("archivo", ARCH[doc]), ("pagina", pagina),
           ("cero_comprobado", O([("motivo", motivo), ("cita", cita)]))])
    if nota:
        e["nota"] = nota
    return e


SOLO_OP = "Our current portfolio includes only operating leases which are recorded as a right of use"
F_ROU = "Amortization of right-of-use assets"
F_PPA = "Amortization and depreciation"
NOTA_PPA = ("«Purchase accounting adjustments: Amortization and depreciation» de la conciliación del beneficio ajustado: amortización del mayor valor razonable de "
            "los intangibles de vida definida adquiridos y amortización por la revalorización de los activos fijos adquiridos, en combinaciones de negocios y "
            "compras de activos netos (10-K 2025 PDF p. 52: «These impacts, primarily associated with certain acquisitions, include amortization related to the "
            "increase in fair value of the acquired finite-lived intangible assets and depreciation related to the increase/decrease to fair value of the "
            "acquired fixed assets»). Es la PPA más cercana que publica Zoetis y se declara como COTA SUPERIOR de la PPA: incluye la depreciación de la "
            "revalorización de los activos fijos adquiridos y la amortización de compras de activos netos (p. ej. derechos de producto comprados, que pueden "
            "ser reinversión recurrente). Efecto en A2 (D_X = D&A − ROU − PPA): si parte de esta cifra fuera reposición, D_X y f están subestimadas y el valor "
            "sobrestimado: sesgo OPTIMISTA de hasta ≈ 1,35 % de las ventas (128 ÷ 9.467 en 2025; 1,54 % de media en la ventana, V-F1f). Comparación con A1 "
            "(sin restar la PPA; diagnóstico de la capa F1 en el paso 7, 18-nov-2026): f 0,0255 frente a 0,0101 en A2, flujo sin crecimiento 2.624,9 frente a "
            "2.771,1 mm (−146,2 mm, −5,3 %). Cuadra 325 + 34 + 128 = 487 = D&A de la fila 8 (10-K 2025 PDF p. 54 y 70), así que la amortización del derecho "
            "de uso operativo no está en la fila 8 (refuerza D-US1). Lectura de la orquestación, PENDIENTE DE REVISOR. Está dentro de la D&A de la fila 8.")
d = O()
d["formato"] = "motor_a_f1 v1"
d["nota"] = ("Declaración F1 de Zoetis (examen, primer tiempo, expediente zoetis_t1c, 18-nov-2026), la primera del expediente. Aplica literalmente las "
             "decisiones registradas del 17-nov (F1 (1a)–(5b), E8.1) y del 18-nov (Examen F1-A y F1-B; D-US1, D-US2, D-US2 bis y D-WM). US GAAP (ASC 842): "
             "arrendamientos OPERATIVOS (coste lineal en el EBIT y pago en el CFO; Zoetis no publica en qué líneas del estado de flujos van la amortización del "
             "derecho de uso ni la variación del pasivo: hipótesis D-US1, conclusión CONDICIONADA) y un arrendamiento FINANCIERO desde 2023 (desglosado: "
             "amortización 1/1/1 y principal 2/1/—, 10-K 2025 PDF p. 89; D-WM no aplica). La fila 23 de la Historia lleva solo el pasivo financiero (corrección "
             "registrada en resultados/correccion_fase1_partes.json). La reinversión A2 es una HIPÓTESIS DECLARADA (F1-A), no un dato. La PPA es la línea "
             "«Amortization and depreciation» de los ajustes de contabilidad de adquisiciones (lectura pendiente de revisor). P-FOSO (a): con US GAAP la "
             "medida no tiene fórmula (perimetro_f1.py, C3): no se declara la serie de intereses de arrendamiento. N1 no se usa. Preparada por un agente de "
             "la orquestación; no acredita aptitud.")
d["norma_contable"] = O([("valor", "US_GAAP"), ("registro", REG("2026-11-18", "Los estados financieros consolidados se preparan con US GAAP: «The consolidated financial statements were prepared in accordance with accounting principles generally accepted in the United States of America (U.S. GAAP)» (10-K 2025, texto/zoetis-10k-fy2025.txt PDF p. 71); el libro dice «US GAAP» (Control maestro L4). Arrendamientos con ASC 842."))])
d["perimetro_reinversion"] = O([("valor", "A2_propio"), ("registro", REG("2026-11-18", f"{DEC} · Examen F1-A: reinversión necesaria = amortización propia sin derechos de uso ni PPA (A2_propio), como hipótesis declarada, no como dato; se presenta condicionada y con su sensibilidad. Zoetis no publica el reparto entre mantenimiento y crecimiento."))])
d["perimetro_margen"] = O([("valor", "EBIT_NIIF16_PPA_constante"), ("registro", REG("2026-11-17", f"{DEC} · F1 (2)(v): la PPA y la ROU como proporción constante de las ventas (la que devuelve f); con US GAAP el identificador designa el EBIT publicado (F1_USGAAP.md §4)"))])
d["perimetro_palancas_s2c"] = O([("valor", "A2_propio"), ("registro", REG("2026-11-17", f"{DEC} · F1 (4a): un solo perímetro para f, el ancla de S2C, el margen y el ROIC del terminal (A2_propio por F1-A)"))])
d["perimetro_roic"] = O([("valor", "A2_propio"), ("registro", REG("2026-11-17", f"{DEC} · F1 (4a): un solo perímetro (A2_propio por F1-A)"))])
d["clasificacion_compras"] = O([("valor", "crecimiento_por_hipotesis"), ("registro", REG("2026-11-18", f"{DEC} · Examen F1-B: compras de empresas como crecimiento, hipótesis declarada y revisable (equivale a (4b) opción B)")),
    ("importes", None), ("proporcion_ventas", None), ("ancla_s2c_excluye_terminos", None),
    ("fundamento", "regla general F1-B del 18-nov-2026: las compras de sociedades de la Historia (fila 13: 14 en 2021, 312 en 2022, 251 en 2023, −285 en 2024 por ventas de negocios netas, 28 en 2025) se tratan como crecimiento. El 10-K no publica un reparto entre compras de mantenimiento y de crecimiento. Si una compra pareciera necesaria para mantener las ventas, lo señala el personaje; aquí no se juzga")])
d["transicion"] = O([("conocida", False), ("tratamiento", None), ("registro", REG("2026-11-18", f"{DEC} · F1 (5b) por finalidad documentada; regla del encargo del coordinador (18-nov): sin inversión de transición documentada con importe → «sin transición conocida» con su motivo")),
    ("importes", None), ("horizonte", None), ("naturaleza", None), ("finalidad_documentada", None), ("ancla_s2c_excluye_terminos", None),
    ("motivo_sin_transicion", "El 10-K 2025 no documenta una inversión de transición con importe propio: la carta habla de «more than 30 carbon reduction projects at key sites» para «long-term climate goals» (PDF p. 6), sin importe, y los riesgos dicen que «it is not possible to accurately estimate the timing for the emergence of new regulation, their scope or our future costs relating to implementation and compliance» (PDF p. 31). Límite: «sin transición conocida» significa sin importe documentado, no que no haya inversión climática")])
d["reinversion_estimada"] = None
d["arrendamientos_us_gaap"] = O([
    ("registro", REG("2026-11-18", f"{DEC} · D-US1 (hipótesis general declarada si la empresa no publica en qué líneas del estado de flujos van los dos tramos del arrendamiento operativo), D-US2 (se cuentan los pagos), D-WM (no aplica: financieros desglosados)")),
    ("operativos", O([("existen", True), ("documento", D25), ("pagina", 88), ("cita", "We have facilities and vehicles under various non-cancellable operating leases with third parties"),
        ("amortizacion_rou", O([("ubicacion", "no_publicada"), ("documento", D25), ("pagina", 70)])),
        ("variacion_pasivo", O([("ubicacion", "no_publicada"), ("documento", D25), ("pagina", 70)]))])),
    ("financieros", O([("existen", True), ("documento", D25), ("pagina", 88), ("cita", "an equipment finance lease with a third party"), ("desglose", "publicado")]))])
S = O()
S["da_rou"] = O([
    ("2021", cero(D21, 78, "Sin arrendamientos financieros en 2021: «Our current portfolio includes only operating leases»; la amortización del derecho de uso de los operativos no está dentro de la fila 8 (D-US1). Cero por lectura, PENDIENTE DE REVISOR", SOLO_OP)),
    ("2022", cero(D22, 70, "Sin arrendamientos financieros en 2022: «Our current portfolio includes only operating leases»; la amortización del derecho de uso de los operativos no está dentro de la fila 8 (D-US1). Cero por lectura, PENDIENTE DE REVISOR", SOLO_OP)),
    ("2023", cifra(D25, 89, F_ROU, "1", "amortización del derecho de uso del arrendamiento FINANCIERO (Supplemental Income Statement information for finance leases); dentro de la D&A de la fila 8 por omisión (F1_USGAAP.md regla 2)", "2023")),
    ("2024", cifra(D25, 89, F_ROU, "1", "ídem 2024", "2024")),
    ("2025", cifra(D25, 89, F_ROU, "1", "ídem 2025", "2025"))])
S["da_ppa"] = O([
    ("2021", cifra(D22, 52, F_PPA, "175", NOTA_PPA, "2021")), ("2022", cifra(D22, 52, F_PPA, "160", NOTA_PPA, "2022")),
    ("2023", cifra(D25, 54, F_PPA, "153", NOTA_PPA, "2023")), ("2024", cifra(D25, 54, F_PPA, "140", NOTA_PPA, "2024")), ("2025", cifra(D25, 54, F_PPA, "128", NOTA_PPA, "2025"))])
S["pagos_arr_operativo"] = O([(str(y), cifra(D25, 89, "Operating cash flows – operating leases", v, "caja pagada por arrendamientos operativos (dentro del CFO)", str(y))) for y, v in ((2023, "57"), (2024, "61"), (2025, "67"))])
S["coste_arr_operativo"] = O([(str(y), cifra(D25, 89, "Operating lease expense", v, "coste lineal de los arrendamientos operativos capitalizados; el variable y el de corto plazo se publican aparte (mismo perímetro que los pagos)", str(y))) for y, v in ((2023, "56"), (2024, "59"), (2025, "68"))])
S["pasivo_arr_operativo"] = O([("2025", cero(D25, 89, "Pasivo por arrendamiento OPERATIVO dentro de la fila 23 de la Historia en 2025 = 0: la fila 23 lleva solo el pasivo por arrendamientos financieros (1 + 6 = 7, PDF p. 89) por la corrección registrada de fase1_partes (resultados/correccion_fase1_partes.json); el pasivo operativo publicado (52 + 196 = 248, misma página) no está en ella. La capa lo contrasta con las líneas que la fase 1 sumó en la fila 23. PENDIENTE DE REVISOR", "Supplemental information for our lease portfolio is as follows:"))])
S["pagos_arr_financiero_principal"] = O([("2023", cifra(D25, 89, "Financing cash flows – finance leases", "—", "cero impreso «—» en la columna de 2023", "2023")),
    ("2024", cifra(D25, 89, "Financing cash flows – finance leases", "1", "principal pagado del arrendamiento financiero (nota de arrendamientos, información complementaria; la línea del estado de flujos donde va no está publicada: en 2024 «Other financing activities» es «—» y el pago es 1, PDF p. 70)", "2024")),
    ("2025", cifra(D25, 89, "Financing cash flows – finance leases", "2", "principal pagado del arrendamiento financiero (nota de arrendamientos, información complementaria; la línea del estado de flujos donde va no está publicada: en 2024 «Other financing activities» es «—» y el pago es 1, PDF p. 70)", "2025"))])
d["series"] = S
d["normalizacion"] = O([("ajustes", []), ("bai", {}), ("gasto_impuesto", {}), ("margen_objetivo_sin_ajustes", None), ("deducir_diagnostico_partidas_puntuales", False),
                        ("nota", "N1 no se usa: Zoetis no tiene partidas N1 (no hay ajustes de earnout como en Elis); N2 sigue pendiente y no se aplica")])
d["umbral_v_f1a"] = None
d["fuentes_series"] = O([(doc, O([("archivo", a), ("sha256", h(a))])) for doc, a in ARCH.items()])
json.dump(d, open(SAL, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("escrita", SAL)
