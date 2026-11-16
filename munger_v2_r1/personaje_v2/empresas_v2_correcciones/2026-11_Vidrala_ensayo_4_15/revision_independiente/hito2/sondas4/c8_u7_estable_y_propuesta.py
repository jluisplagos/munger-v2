#!/usr/bin/env python3
"""c8 · resto de T1 (cuarta comprobación): (A) qué hacía con los pares de la misma moneda la candidata ESTABLE de la segunda pasada
(92b2362, anterior a la exención del tipo de cambio; su verificacion_entradas.py se saca con «git show», solo lectura) y qué hacen f3d15e8
y 7a6583b; (B) la propuesta del revisor (no es código entregado): la exención solo vale si las DOS monedas del par son distintas.
Uso: python3 -I -B c8_u7_estable_y_propuesta.py"""
import importlib.util, os, re, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sondas3"))
from comun3 import VE, VP, ACT, ANT, F  # noqa: E402


def cargar(p, nombre):
    spec = importlib.util.spec_from_file_location(nombre, p)
    m = importlib.util.module_from_spec(spec)
    ruta = list(sys.path)
    spec.loader.exec_module(m)
    sys.path[:] = ruta
    return m


V92 = cargar(os.path.join(F, "estable92", "scripts", "verificacion_entradas.py"), "verificacion_entradas_92b2362")
assert "tipo_cambio" not in open(V92.__file__, encoding="utf-8").read()
CANON = {"€": "eur", "euro": "eur", "euros": "eur", "$": "usd", "dólar": "usd", "dolar": "usd", "£": "gbp", "libra": "gbp", "libras": "gbp", "¥": "jpy",
         "franco": "chf", "francos": "chf", "real": "brl", "reales": "brl"}
CORONAS = {"corona", "coronas", "dkk", "sek", "nok"}


def propuesta(unidad):
    """_unidad_monetaria_no_reconocida de la cuarta con un cambio: el par tiene que ser de dos monedas DISTINTAS."""
    t = VE._norm_txt(unidad)
    m_ = VE.MARCAS_MONEDA.pattern
    m = re.fullmatch(r"(?:(?:tipo de cambio|exchange rate)\b)?[\s:(]*" + m_ + r"\s*(?:por|per|/)\s*" + m_ + r"[\s)]*", t, re.I)
    a, b = (CANON.get(m.group(1), m.group(1)), CANON.get(m.group(2), m.group(2))) if m else (None, None)
    misma = a == b or (bool({a, b} & {"corona", "coronas"}) and {a, b} <= CORONAS)  # «coronas/DKK»: el nombre y un código de corona pueden ser la misma
    distintas = m is not None and not misma
    tipo_cambio = distintas and re.search(r"miles|millones|millares|thousand|million|billion|\bmm\b|\bbn\b|mm€|meur|keur|k€|m€|€m|€000", t, re.I) is None
    return bool(t) and t not in VE.UNIDADES and VE.MARCAS_MONEDA.search(t) is not None and VE.POR_UNIDAD.search(t) is None and not tipo_cambio


est = lambda x: "PENDIENTE" if x else "no pendiente"  # noqa: E731
print(f"{'unidad':44} {'92b2362 (estable)':18} {'f3d15e8':14} {'7a6583b':14} propuesta")
for titulo, us in (("pares de la MISMA moneda", ["euros/EUR", "EUR/€", "€/EUR", "Euros / Euro", "euro/euros", "EUR/EUR", "USD/$", "$/USD", "libras/GBP", "GBP/£", "eur por eur", "(€/EUR)", "coronas/DKK"]),
                   ("pares de monedas distintas (tipos de cambio)", ["USD por EUR", "EUR/USD", "tipo de cambio EUR/GBP", "exchange rate USD per EUR", "$/€", "dólar por euro", "euros por dólar", "coronas/euros", "DKK/SEK"]),
                   ("importes", ["miles de euros a tipo de cambio constante", "millones de euros/EUR million", "Miles de € / € thousand", "meur/keur", "miles de €", "MM€"]),
                   ("reconocidas o por acción", ["euros", "miles de euros", "EUR por acción"])):
    print(f"-- {titulo}")
    for u in us:
        print(f"   {u!r:42} {est(V92._unidad_monetaria_no_reconocida(u)):18} {est(VP._unidad_monetaria_no_reconocida(u)):14} {est(VE._unidad_monetaria_no_reconocida(u)):14} {est(propuesta(u))}")
