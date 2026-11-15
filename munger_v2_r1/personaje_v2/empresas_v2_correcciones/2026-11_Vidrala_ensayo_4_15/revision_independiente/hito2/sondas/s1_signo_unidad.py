#!/usr/bin/env python3
"""s1 · R415-SIGNO, nivel de unidad: _cita_cifra(cita, vf) y _cita_cifra(cita, vf, pagina) con formatos reales de informes.
Columna «esperado» = juicio del revisor: ok / no (cualquier rechazo) ; se marca con «<<<» lo que no coincide."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # con -I el directorio del script no entra en sys.path
from comun import VE

def ver(cita, vf, pagina=None):
    return VE._cita_cifra(cita, vf, pagina)

casos = [
    # (descripción, cita, vf, esperado: "ok" o "no")
    ("A1 negativo entre paréntesis con % dentro", "Variación (3,2 %)", -3.2, "ok"),
    ("A2 negativo entre paréntesis con % pegado dentro", "Change (3.2%)", -3.2, "ok"),
    ("A3 negativo con paréntesis y % fuera", "Change (3.2)%", -3.2, "ok"),
    ("A4 positivo en inciso de prosa", "un margen (12,5 % de las ventas) estable", 12.5, "ok"),
    ("A5 positivo en inciso: (2024: 150,8)", "pagos (2024: 150,8) y otros", 150.8, "ok"),
    ("A6 negativo «(-149,5)»", "variación (-149,5)", -149.5, "ok"),
    ("A7 negativo «(−149,5)» Unicode", "variación (−149,5)", -149.5, "ok"),
    ("A8 menos Unicode a dos espacios (columna alineada)", "Resultado −  149,5", -149.5, "ok"),
    ("A8b lo mismo frente a +149,5", "Resultado −  149,5", 149.5, "no"),
    ("A9 formato contable de Excel «-£   1,234.00»", "Charge -£   1,234.00", -1234.0, "ok"),
    ("A9b lo mismo frente a +1234", "Charge -£   1,234.00", 1234.0, "no"),
    ("A10 guion ASCII a 2 espacios (¿cero de otra columna o menos alineado a la izquierda?)", "Resultado  -  149,5", 149.5, "no"),
    ("A10b lo mismo frente a −149,5", "Resultado  -  149,5", -149.5, "no"),
    ("A11 menos pegado tras paréntesis de nota «(1)-149,5»", "Resultado (1)-149,5", -149.5, "ok"),
    ("A12 menos tras coma «a,-149,5»", "x, -149,5", -149.5, "ok"),
    ("A13 «EUR -149,5»", "EUR -149,5", -149.5, "ok"),
    ("A14 «(EUR 149,5)» contable con código de moneda", "Pago (EUR 149,5)", -149.5, "ok"),
    ("A14b lo mismo frente a +149,5", "Pago (EUR 149,5)", 149.5, "no"),
    ("A15 «(149,5 millones)» inciso", "deuda (149,5 millones)", 149.5, "ok"),
    ("A16 fecha «31-12-2024» frente a 2024", "a 31-12-2024", 2024, "ok"),
    ("A17 fecha «31-dic-2024» frente a 2024", "a 31-dic-2024", 2024, "ok"),
    ("A18 «FY 2023-2024» frente a 2024", "FY 2023-2024", 2024, "ok"),
    ("A19 «149,5 CR» / «149,5 DR»", "Saldo 149,5 CR", 149.5, "ok"),
    ("A20 menos final con espacio «149,5 -»", "Saldo 149,5 -", 149.5, "ok"),
    ("A21 menos final pegado SAP «149,5-» frente a −149,5", "Saldo 149,5-", -149.5, "ok"),
    ("A22 corchetes «[149,5]» como negativo", "Saldo [149,5]", -149.5, "no"),
    ("A22b «[149,5]» frente a +149,5", "Saldo [149,5]", 149.5, "no"),
    ("A23 «<149,5>» negativo", "Saldo <149,5>", 149.5, "no"),
    ("A24 punto decimal y miles europeos «(1.234,5)»", "Pagos (1.234,5)", -1234.5, "ok"),
    ("A25 miles con espacio «(4 573,7)»", "Paiements (4 573,7)", -4573.7, "ok"),
    ("A25b miles con espacio fino U+202F «−4 573,7»", "Paiements −4 573,7", -4573.7, "ok"),
    ("A26 «(4 573,7)» frente a 573,7 positivo (límite declarado de «4 573,7»)", "Paiements (4 573,7)", 573.7, "no"),
    ("A27 «-4 573,7» frente a 573,7 positivo", "Paiements -4 573,7", 573.7, "no"),
    ("A28 nota al pie «(1) 150,8»", "Pagos (1) 150,8", 150.8, "ok"),
    ("A29 nota al pie como cifra «(3)» frente a −3", "Ventas (3) 849.697", -3, "no"),
    ("A30 dos columnas «(177.9) (150.8)»", "Lease payments (177.9) (150.8)", -150.8, "ok"),
    ("A31 salto de línea entre paréntesis y cifra", "Lease payments (\n150.8)", -150.8, "ok"),
    ("A32 tabulador «\t-149,5»", "Importe\t-149,5", -149.5, "ok"),
    ("A33 «+/-149,5»", "variación +/-149,5", 149.5, "no"),
    ("A34 «±149,5»", "variación ±149,5", 149.5, "no"),
    ("A35 «~149,5» / «≈ 149,5»", "aprox. ≈ 149,5", 149.5, "ok"),
    ("A36 «−149,5» con U+2212 y NBSP", "Importe − 149,5", -149.5, "ok"),
    ("A37 guion no separable U+2011 pegado", "Importe ‑149,5", -149.5, "ok"),
    ("A38 raya horizontal U+2015 pegada", "Importe ―149,5", -149.5, "no"),
    ("A38b raya horizontal U+2015 pegada frente a +149,5", "Importe ―149,5", 149.5, "no"),
    ("A39 figure dash/soft hyphen U+00AD pegado", "Importe ­149,5", 149.5, "no"),
    ("A40 «–» pegado a letra «EBITDA–149,5»", "EBITDA–149,5", 149.5, "no"),
    ("A41 negativo en rojo (sin marca) no es detectable: positivo", "Importe 149,5", 149.5, "ok"),
    ("A42 «149,5)» paréntesis solo de cierre (cita recortada tras «(»)", "149,5)", 149.5, "no"),
    ("A42b «149,5)» frente a −149,5", "149,5)", -149.5, "no"),
    ("A43 «(149,5» cita recortada antes de «)»", "(149,5", -149.5, "no"),
    ("A44 porcentaje negativo «-3,2 %»", "tasa -3,2 %", -3.2, "ok"),
    ("A45 porcentaje «−3,2%» frente a +3,2", "tasa −3,2%", 3.2, "no"),
    ("A46 intervalo «entre 2 y 3 %»", "entre 2 y 3 %", 3, "ok"),
    ("A47 intervalo «2-3 %» frente a 3", "rango 2-3 %", 3, "ok"),
    ("A48 intervalo «2–3 %» frente a 3", "rango 2–3 %", 3, "ok"),
    ("A49 moneda detrás «149,5€» / «-149,5 €»", "Importe -149,5 €", -149.5, "ok"),
    ("A50 «€ (149,5)»", "Importe € (149,5)", -149.5, "ok"),
    ("A51 «(€ 149,5)»", "Importe (€ 149,5)", -149.5, "ok"),
    ("A52 «$(149.5)»", "Amount $(149.5)", -149.5, "ok"),
    ("A53 «-$149.5»", "Amount -$149.5", -149.5, "ok"),
    ("A54 «$-149.5»", "Amount $-149.5", -149.5, "ok"),
    ("A54b «$-149.5» frente a +149.5", "Amount $-149.5", 149.5, "no"),
    ("A55 «US$ (149.5)»", "Amount US$ (149.5)", -149.5, "ok"),
    ("A56 «(149.5)m»", "Amount (149.5)m", -149.5, "ok"),
    ("A57 «(149.5m)»", "Amount (149.5m)", -149.5, "ok"),
    ("A57b «(149.5m)» frente a +149.5", "Amount (149.5m)", 149.5, "no"),
    ("A58 «(149.5)» con nota pegada «(149.5)(a)»", "Amount (149.5)(a)", -149.5, "ok"),
    ("A59 «(149.5 (a))»", "Amount (149.5 (a))", -149.5, "ok"),
    ("A60 «minus 149.5» / «menos 149,5» (palabra)", "resultado de menos 149,5", 149.5, "no"),
]
mal = 0
for d, c, v, esp in casos:
    est, det = ver(c, v)
    got = "ok" if est == "ok" else "no"
    m = "" if got == esp else "   <<< distinto de lo esperado"
    mal += bool(m)
    print(f"{d}\n      cita={c!r} vf={v!r} -> {est} ({det}){m}")
print(f"\n{mal} casos distintos de lo esperado por el revisor, de {len(casos)}")
