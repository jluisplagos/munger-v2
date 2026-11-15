#!/usr/bin/env python3
"""n7 · H4/H5 (segunda pasada): las reglas nuevas de signo de _signo_en_cita (moneda con código, porcentaje, «$-x», fechas e intervalos,
«−» a un espacio o como cero). Cada caso es una LÍNEA de página con el signo que publica de verdad (a juicio del revisor: −, + o «?» si es
ambiguo y debería quedar pendiente) y se prueba con valor_fuente negativo y positivo. Clasificación: «bien», «rechazo falso» (pendiente o
discrepancia con el signo publicado) y «ACEPTA EL CONTRARIO». Estable frente a candidata.  Uso: python3 -I -B n7_signo_reglas_nuevas.py"""
import collections, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dos_codigos import VE, VC


def clasifica(mod, linea, n, real):
    """real: -1, +1 o None (ambiguo). Devuelve la clase del peor resultado entre declarar +n y −n."""
    ok_pos = mod._cita_cifra(linea, n, linea)[0] == "ok"
    ok_neg = mod._cita_cifra(linea, -n, linea)[0] == "ok"
    if real is None:
        return "ACEPTA (era ambiguo)" if ok_pos or ok_neg else "bien (pendiente)"
    acierta, contrario = (ok_neg, ok_pos) if real == -1 else (ok_pos, ok_neg)
    if contrario:
        return "ACEPTA EL CONTRARIO"
    return "bien" if acierta else "rechazo falso"


CASOS = [
    # (rótulo, línea, cifra, signo real)
    ("intervalo de años", "Ejercicios 2019-2020", 2020, 1),
    ("fecha dd-mm-aaaa", "Cierre a 31-12-2024", 2024, 1),
    ("fecha aaaa-mm-dd", "Fecha 2024-12-31", 31, 1),
    ("intervalo con raya", "Rango 2–3 %", 3, 1),
    ("intervalo de importes", "Entre 100-150 millones", 150, 1),
    ("rótulo que acaba en cifra, pegado a un negativo: «T4-15,2» (trimestre 4: −15,2)", "Variación T4-15,2", 15.2, -1),
    ("nota al pie pegada a un negativo: «Resultado financiero1-149,5»", "Resultado financiero1-149,5", 149.5, -1),
    ("columnas pegadas: «2023-849,7» (año de la columna y −849,7)", "Saldo 2023-849,7", 849.7, -1),
    ("dos importes pegados: «1.234,5-567,8» (segunda columna negativa)", "Flujo 1.234,5-567,8", 567.8, -1),
    ("resta escrita: «1.234,5-567,8» (la segunda cifra se resta)", "Neto = 1.234,5-567,8", 567.8, None),
    ("código de norma: «NIIF-16» ", "Aplicación de NIIF-16", 16, 1),
    ("«COVID-19»", "Efecto del COVID-19", 19, 1),
    ("teléfono o referencia «75-49-98-30»", "Ref. 75-49-98-30", 30, 1),
    ("porcentaje negativo entre paréntesis", "Variación (3,2 %)", 3.2, -1),
    ("porcentaje negativo con signo", "Variación -3,2 %", 3.2, -1),
    ("inciso positivo con porcentaje", "un margen (12,5 % de las ventas) estable", 12.5, 1),
    ("inciso positivo con porcentaje y cierre inmediato: «(12,5 %)» en una frase", "crece al mismo ritmo (12,5 %) que el año anterior", 12.5, None),
    ("código de moneda dentro del paréntesis", "Pago (EUR 149,5)", 149.5, -1),
    ("código de moneda detrás, dentro del paréntesis", "Pago (149,5 EUR)", 149.5, -1),
    ("código de moneda en minúsculas", "Pago (eur 149,5)", 149.5, -1),
    ("moneda entre guion y cifra con un espacio: «- EUR 149,5»", "Pago - EUR 149,5", 149.5, None),
    ("moneda pegada al guion: «-EUR 149,5»", "Pago -EUR 149,5", 149.5, -1),
    ("«$-149.5»", "Amount $-149.5", 149.5, -1),
    ("«€-149,5»", "Importe €-149,5", 149.5, -1),
    ("«USD-149.5» (código pegado y menos)", "Amount USD-149.5", 149.5, -1),
    ("«EUR/USD-1.08» (par de divisas, positivo)", "Tipo EUR/USD-1.08", 1.08, None),
    ("palabra que acaba en código de moneda en minúsculas: «…sek 149,5» (sueco)", "Omsättning i sek 149,5", 149.5, 1),
    ("palabra «nok» (noruego: bastante) antes de la cifra entre paréntesis", "(nok 149,5)", 149.5, None),
    ("«−» Unicode pegado", "Resultado −149,5", 149.5, -1),
    ("«−» Unicode a un espacio (menos tipográfico habitual en informes: «− 149,5»)", "Resultado − 149,5", 149.5, -1),
    ("«−» Unicode a un espacio en una tabla estrecha (cero de la columna anterior)", "Dividendos − 42,2", 42.2, 1),
    ("«−» a dos espacios (otra columna)", "Dividendos −  42,2", 42.2, 1),
    ("menos Unicode dentro de paréntesis «(−149,5)»", "variación (−149,5)", 149.5, -1),
    ("guion ASCII dentro de paréntesis «(-149,5)»", "variación (-149,5)", 149.5, -1),
    ("cierre de paréntesis sin apertura en la línea: «149,5)»", "149,5) 12,0", 149.5, None),
    ("apertura sin cierre: «(149,5»", "Pago (149,5", 149.5, None),
    ("corchetes contables «[149,5]»", "Saldo [149,5]", 149.5, None),
    ("«149,5 CR» / «149,5 DR»", "Saldo 149,5 CR", 149.5, None),
    ("«149,5-» (menos detrás)", "Saldo 149,5-", 149.5, -1),
    ("«(149,5)%»", "Variación (149,5)%", 149.5, -1),
    ("«-149,5%»", "Variación -149,5%", 149.5, -1),
    ("«+149,5»", "Variación +149,5", 149.5, 1),
    ("«±149,5»", "Margen ±149,5", 149.5, None),
    ("cifra tras dos puntos y guion: «: -149,5»", "Importe: -149,5", 149.5, -1),
    ("cifra tras barra: «/-149,5»", "n/a/-149,5", 149.5, -1),
]
tot = {"estable": collections.Counter(), "candidata": collections.Counter()}
print(f"{'caso':86} {'publica':7} {'candidata':24} estable")
for rot, linea, n, real in CASOS:
    c2, c1 = clasifica(VE, linea, n, real), clasifica(VC, linea, n, real)
    tot["estable"][c2.split(" (")[0]] += 1
    tot["candidata"][c1.split(" (")[0]] += 1
    marca = "   <<<" if c2.startswith("ACEPTA") else ""
    print(f"   {rot[:83]:83} {'−' if real == -1 else '+' if real == 1 else '?':7} {c1:24} {c2}{marca}")
print("total candidata:", dict(tot["candidata"]))
print("total estable:  ", dict(tot["estable"]))
