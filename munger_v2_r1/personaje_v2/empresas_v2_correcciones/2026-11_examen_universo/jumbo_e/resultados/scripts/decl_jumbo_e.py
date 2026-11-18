"""Construye la declaración F1 de jumbo_e desde la de jumbo_d (entrada → salida). Uso: decl_jumbo_e.py ENTRADA SALIDA"""
import json, sys, collections
from fractions import Fraction as Fr
O = collections.OrderedDict
d = json.load(open(sys.argv[1], encoding="utf-8"), object_pairs_hook=O)
F = d["fuentes_series"]
def mm(lit):
    from decimal import Decimal
    n = int(lit.strip("()").replace(".", ""))
    return float(Decimal(n) / Decimal(10**6))
# 1) da_rou: escala «unidades» (valor_fuente en millones = literal / 1.000.000, exacto)
for y, e in d["series"]["da_rou"].items():
    v = mm(e["literal"]); assert v is not None and abs(v) == abs(e["valor_fuente"]), (y, e["literal"], e["valor_fuente"])
    e["escala"] = "unidades"
    e["tratamiento"] = "cargo publicado entre paréntesis y EN EUROS enteros; magnitud positiva en el modelo (signo −1); «valor_fuente» en millones = literal ÷ 1.000.000 (escala «unidades», F1-SERIES con escala)"
    e["nota"] = e["nota"].split(" La columna")[0] + " La columna es una clase de activo, no un ejercicio (F1-SERIES deja la columna pendiente). La D&A total de la Historia (fila 8) incluye esta amortización. Página con «(amounts in Euro)»."
# 2) da_ppa: cero_comprobado 2021–2025 (sin «literal»; valor_fuente 0); pendiente de revisor
FRASE_TABLA = "The Group’s fixed assets movements for the year were as follows:"
FRASE_PPA = ("The final fair values of the Statement of Financial Position of the acquired company, the total purchase consideration, "
             "and the result arising for the Group at the acquisition date are presented as follows:")
ppa = O()
for y, doc, pg in ((2021, "AR2022", 97), (2022, "AR2023", 100), (2023, "AR2024", 183), (2024, "AR2025", 185)):
    ppa[str(y)] = O([("valor_fuente", 0), ("signo", 1), ("tratamiento", "ninguno"), ("documento", doc), ("archivo", F[doc]["archivo"]), ("pagina", pg),
        ("cero_comprobado", O([("motivo", f"PPA de {y} = 0 por LECTURA, pendiente de revisor: en el cuadro de movimientos del inmovilizado, intangibles y derechos de uso del grupo (nota 5.8) que introduce la frase citada, el único intangible es «Software» (licencias a coste menos amortización, política 4.5); no hay ninguna clase de intangibles de combinaciones de negocios ni fondo de comercio. La frase solo sitúa el cuadro: no prueba por sí sola la inexistencia. No se usa para {y} la frase de AR2025 p. 189, que es de la combinación HERALD 2 de octubre de 2025 (revisión R2 de f1/series-escala, §3; README_V6.3.1_F1.md §10)"),
                                ("cita", FRASE_TABLA)])),
        ("nota", "cero declarado con cero_comprobado (F1-SERIES-CERO: PENDIENTE de revisor; la aptitud por entradas sigue en «no»). Sin cifra impresa: el cuadro no tiene columna de intangibles de combinaciones")])
ppa["2025"] = O([("valor_fuente", 0), ("signo", 1), ("tratamiento", "ninguno"), ("documento", "AR2025"), ("archivo", F["AR2025"]["archivo"]), ("pagina", 189),
    ("cero_comprobado", O([("motivo", "PPA de 2025 = 0 por LECTURA, pendiente de revisor: la única combinación del ejercicio, HERALD 2 (24-oct-2025, nota 5.10.1), no reconoce ningún intangible en la asignación del precio que introduce la frase citada (inmovilizado propio, inversión inmobiliaria, derechos de uso, cuentas a cobrar y caja; ganancia por compra ventajosa); el cuadro de la nota 5.8 de 2025 (AR2025 PDF p. 185) solo tiene «Software» como intangible. La frase no prueba por sí sola la inexistencia; tampoco confirma que la revalorización del inmueble no cuente (nota de la revisión R2 de f1/series-escala, §3)"),
                            ("cita", FRASE_PPA)])),
    ("nota", "cero declarado con cero_comprobado (F1-SERIES-CERO: PENDIENTE de revisor; la aptitud por entradas sigue en «no»)")])
d["series"]["da_ppa"] = ppa
# 3) la nota de texto que estaba dentro de «series» pasa a «nota» (R2-4 de la revisión R2 de f1/usgaap)
nota_pagos = d["series"].pop("pagos_arrendamiento_sin_declarar")
# AR2021 (nota 5.5 del propio ejercicio: su columna de 2021 está alineada con el encabezado; en AR2022 p. 92 no)
import hashlib, os
_t = os.path.join(os.path.dirname(os.path.abspath(sys.argv[1])), "texto", "jumbo-annual-report-fy2021.txt")
F["AR2021"] = O([("archivo", "texto/jumbo-annual-report-fy2021.txt"), ("sha256", hashlib.sha256(open(_t, "rb").read()).hexdigest())])
d["fuentes_series"] = O(sorted(F.items()))
F = d["fuentes_series"]
# 4) intereses de arrendamiento (vara del foso P-FOSO (a)): nota de costes financieros 5.5, «Interest expense on lease liabilities», columna del GRUPO
INT = ((2021, "AR2021", 87, "3.056.657"), (2022, "AR2022", 92, "2.628.373"), (2023, "AR2023", 95, "2.664.523"),
       (2024, "AR2024", 178, "2.526.806"), (2025, "AR2025", 179, "2.390.655"))
s = O()
for y, doc, pg, lit in INT:
    s[str(y)] = O([("valor_fuente", mm(lit)), ("signo", 1), ("tratamiento", "ninguno"), ("escala", "unidades"), ("documento", doc), ("archivo", F[doc]["archivo"]),
        ("pagina", pg), ("literal", lit), ("fila", "Interest expense on lease liabilities"), ("columna", str(y)),
        ("cuadro", f"nota 5.5 «Finance income / expenses and other financial results», «Finance costs», columna THE GROUP del ejercicio {y} (amounts in €)"),
        ("nota", f"intereses del pasivo por arrendamiento (gasto financiero NIIF 16) del grupo en {y}: {lit} € = {mm(lit)} mm; solo para la vara del foso de P-FOSO (a). "
                 "Se toma la NOTA DE COSTES FINANCIEROS y no el estado de flujos: el emisor cruzó en los flujos de 2020–2025 las etiquetas «Lease repayments» e "
                 "«Interest paid for leases» (decisión J3; jumbo_c/resultados/cambio_de_base.json); la cifra de la nota coincide con la línea de flujos rotulada "
                 "«Lease repayments».")])
d["series"]["intereses_arrendamiento"] = s
d["nota"] = ("Declaración F1 de Jumbo S.A. (examen, expediente jumbo_e, 18-nov-2026; desde la de jumbo_d). Aplica literalmente las decisiones registradas del "
    "17-nov (F1 (1a)–(5b), E8.1) y del 18-nov (Examen · F1-A y F1-B; P-FOSO (a)). Preparada por un agente de la orquestación; no acredita aptitud. Respeta "
    "J-T bis (2019, fuera del horizonte 2021–2025 de las series) y J3 (Historia de arrendamientos corregida). CAMBIOS frente a jumbo_d: (1) formato nuevo de "
    "F1-SERIES con escala: Jumbo publica en euros enteros; cada año lleva «escala»: «unidades» y «valor_fuente» en millones = literal ÷ 1.000.000; (2) PPA "
    "2021–2025 declarada con «cero_comprobado» (motivo y cita en su página), PENDIENTE DE REVISOR (F1-SERIES-CERO): es un cero por lectura, sin cifra impresa; "
    "(3) serie de intereses de arrendamiento 2021–2025 de la nota de costes financieros (5.5) para la vara del foso de P-FOSO (a); (4) la nota de texto que "
    "estaba dentro de «series» («pagos_arrendamiento_sin_declarar», R2-4 de la revisión R2 de f1/usgaap) pasa aquí: " + nota_pagos + ". LÍMITE: sin "
    "pagos_arrendamiento (solo la sensibilidad (1b)).")
json.dump(d, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("escrita", sys.argv[2])
