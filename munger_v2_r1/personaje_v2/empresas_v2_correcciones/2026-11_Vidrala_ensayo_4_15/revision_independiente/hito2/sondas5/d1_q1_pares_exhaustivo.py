#!/usr/bin/env python3
"""d1 · Q1 (quinta comprobación): la exención del tipo de cambio de U7 exige ahora dos monedas DISTINTAS (_moneda_de).
A) las trece unidades de la sonda c8 de la cuarta comprobación y otras de la misma moneda, con cinco códigos:
   92b2362 (estable de la 2.ª pasada), f3d15e8, 7a6583b (4.ª), 876bfc2 (esta) y la propuesta del revisor de la 4.ª (no es código entregado).
B) EXHAUSTIVO: todas las unidades «a SEP b» con a y b tomadas de todas las formas que MARCAS_MONEDA reconoce y varios separadores,
   prefijos y envoltorios. Para cada una se clasifica el par por la moneda REAL de cada forma (tabla del revisor, independiente de
   _moneda_de) y se cuenta: misma moneda → ¿pendiente?; monedas distintas → ¿exenta?
C) MONOTONÍA: ninguna unidad pendiente con 7a6583b deja de estarlo con 876bfc2 (la corrección solo puede añadir pendientes); se comprueba
   sobre B y sobre un corpus de unidades con calificativos y escalas.
D) _moneda_de forma a forma.
Uso: python3 -I -B d1_q1_pares_exhaustivo.py"""
import collections, itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun5 import VE, VP, V92, VF3, VPR, ACT, ANT  # noqa: E402

est = lambda x: "PENDIENTE" if x else "no pendiente"  # noqa: E731
f = lambda M, u: M._unidad_monetaria_no_reconocida(u)  # noqa: E731

print(f"VE = {ACT} · VP = {ANT}")
print("== A · unidad a unidad")
print(f"   {'unidad':40} {'92b2362':13} {'f3d15e8':13} {'7a6583b':13} {'876bfc2':13} propuesta 4.ª")
GRUPOS = (
    ("las trece de c8 (misma moneda)", ["euros/EUR", "EUR/€", "€/EUR", "Euros / Euro", "euro/euros", "EUR/EUR", "USD/$", "$/USD", "libras/GBP", "GBP/£", "eur por eur", "(€/EUR)", "coronas/DKK"]),
    ("otras de la MISMA moneda", ["JPY/¥", "¥/JPY", "dólar/USD", "USD/dólar", "dolar/$", "libra/libras", "£/libras", "tipo de cambio EUR/EUR", "exchange rate: € per EUR",
                                 "francos/CHF", "CHF/francos", "franco/francos", "reales/BRL", "BRL/reales", "real/reales", "DKK/coronas", "corona/coronas", "coronas/coronas",
                                 "coronas/SEK", "NOK/coronas", "CHF/CHF", "DKK/DKK"]),
    ("monedas distintas (tipos de cambio: se esperan exentas)", ["USD por EUR", "EUR/USD", "tipo de cambio EUR/GBP", "exchange rate USD per EUR", "$/€", "dólar por euro", "euros por dólar",
                                                                "coronas/euros", "DKK/SEK", "CHF/EUR", "francos/euro", "reales por euro", "BRL/USD", "¥/€", "JPY per USD", "libras por dólar"]),
)
restos = []
for titulo, us in GRUPOS:
    print(f"-- {titulo}")
    for u in us:
        r = [f(M, u) for M in (V92, VF3, VP, VE, VPR)]
        marca = ""
        if "misma" in titulo.lower() and not r[3]:
            marca = "   <<< misma moneda y sigue EXENTA con 876bfc2"
            restos.append(u)
        if "distintas" in titulo and r[3]:
            marca = "   <<< tipo de cambio que queda pendiente"
        print(f"   {u!r:40} {est(r[0]):13} {est(r[1]):13} {est(r[2]):13} {est(r[3]):13} {est(r[4])}{marca}")
print(f"   pares de la misma moneda que siguen exentos con 876bfc2: {len(restos)} · {restos}")

print("\n== B · exhaustivo: todas las formas de MARCAS_MONEDA, por pares")
# moneda real de cada forma (tabla del revisor). «corona(s)» es DKK, SEK o NOK (y otras): se trata como «corona» y se considera la misma
# moneda que cualquiera de los tres códigos; «franco(s)» = CHF; «real(es)» = BRL. Las marcas con escala (mm€, meur, keur, k€) llevan escala.
FORMAS = {"€": "eur", "eur": "eur", "euro": "eur", "euros": "eur", "$": "usd", "usd": "usd", "dólar": "usd", "dolar": "usd", "£": "gbp", "gbp": "gbp", "libra": "gbp",
          "libras": "gbp", "¥": "jpy", "jpy": "jpy", "chf": "chf", "franco": "chf", "francos": "chf", "dkk": "dkk", "sek": "sek", "nok": "nok", "corona": "corona",
          "coronas": "corona", "brl": "brl", "reales": "brl"}  # «real» (singular) NO es una marca: MARCAS_MONEDA dice «reales?» = «reale(s)» (ya era así; no es de este diff)
CON_ESCALA = ["mm€", "meur", "keur", "k€"]
for forma in list(FORMAS) + CON_ESCALA:
    assert VE.MARCAS_MONEDA.fullmatch(forma), forma


def misma(a, b):
    ca, cb = FORMAS[a], FORMAS[b]
    return ca == cb or ("corona" in (ca, cb) and {ca, cb} <= {"corona", "dkk", "sek", "nok"})


SEPS = ["/", " / ", " por ", " per "]
ENV = ["{}", "({})", "tipo de cambio {}", "tipo de cambio: {}", "exchange rate {}", " {} "]
c = collections.Counter()
ej = collections.defaultdict(list)
no_monotona = []
n = 0
for a, b in itertools.product(FORMAS, repeat=2):
    for sep in SEPS:
        for env in ENV:
            for mayus in (str, str.upper, str.capitalize):
                u = env.format(mayus(a) + sep + mayus(b))
                n += 1
                rp, re_, rpr = f(VP, u), f(VE, u), f(VPR, u)
                clave = ("misma" if misma(a, b) else "distintas", est(rp), est(re_))
                c[clave] += 1
                if len(ej[clave]) < 6 and env == "{}" and sep == "/" and mayus is str:
                    ej[clave].append(u)
                if rp and not re_:
                    no_monotona.append(u)
                c[("frente a la propuesta 4.ª", est(rpr), est(re_))] += 1
print(f"   «real» ¿es una marca de moneda? {VE.MARCAS_MONEDA.fullmatch('real') is not None} · «reale»: {VE.MARCAS_MONEDA.fullmatch('reale') is not None} · «reales»: {VE.MARCAS_MONEDA.fullmatch('reales') is not None}")
print(f"   {n} unidades ({len(FORMAS)} formas × {len(FORMAS)} × {len(SEPS)} separadores × {len(ENV)} envoltorios × 3 mayúsculas)")
for k_, v in sorted(c.items()):
    if k_[0] in ("misma", "distintas"):
        print(f"   par de monedas {k_[0]:9} · 7a6583b {k_[1]:13} → 876bfc2 {k_[2]:13}: {v:6}   ej.: {ej.get(k_, [])}")
for k_, v in sorted(c.items()):
    if k_[0].startswith("frente"):
        print(f"   propuesta 4.ª {k_[1]:13} · 876bfc2 {k_[2]:13}: {v}")
exentas_misma = sorted({(a, b) for a, b in itertools.product(FORMAS, repeat=2) if misma(a, b) and not f(VE, a + "/" + b)})
print(f"   pares (a, b) de la MISMA moneda que siguen EXENTOS con 876bfc2 (separador «/»): {len(exentas_misma)}")
for a, b in exentas_misma:
    print(f"      {a + '/' + b:20} _moneda_de → {VE._moneda_de(a)!r}, {VE._moneda_de(b)!r}")
pend_dist = sorted({(a, b) for a, b in itertools.product(FORMAS, repeat=2) if not misma(a, b) and f(VE, a + "/" + b)})
print(f"   pares (a, b) de monedas DISTINTAS que quedan PENDIENTES con 876bfc2 (separador «/»): {len(pend_dist)} · {pend_dist[:12]}")
pend_dist_prev = sorted({(a, b) for a, b in itertools.product(FORMAS, repeat=2) if not misma(a, b) and f(VP, a + "/" + b)})
print(f"      de ellos, ya pendientes con 7a6583b: {len(set(pend_dist) & set(pend_dist_prev))}")
# marcas con escala
esc = collections.Counter()
for a, b in itertools.product(list(FORMAS) + CON_ESCALA, repeat=2):
    if a in CON_ESCALA or b in CON_ESCALA:
        for sep in SEPS:
            esc[(est(f(VP, a + sep + b)), est(f(VE, a + sep + b)))] += 1
print(f"   pares con una marca de escala (mm€, meur, keur, k€): 7a6583b → 876bfc2: {dict(esc)}")

print("\n== C · monotonía (pendiente con 7a6583b ⇒ pendiente con 876bfc2)")
CAL = ["", " medio", " (cierre)", " a 31-12", " constante", " miles", " millones", " thousand", " m", " bn", " mm"]
PRE = ["", "importe en ", "saldo en ", "miles de ", "millones de ", "tipo de cambio medio ", "cambio "]
n2 = 0
for a, b in itertools.product(FORMAS, repeat=2):
    for sep in ("/", " por "):
        for cal in CAL:
            for pre in PRE:
                u = pre + a + sep + b + cal
                n2 += 1
                rp, re_ = f(VP, u), f(VE, u)
                if rp and not re_:
                    no_monotona.append(u)
                c[("C", est(rp), est(re_))] += 1
print(f"   {n2} unidades con prefijos y calificativos: " + str({f"{k_[1]} → {k_[2]}": v for k_, v in sorted(c.items()) if k_[0] == "C"}))
print(f"   unidades pendientes con 7a6583b y NO pendientes con 876bfc2 (B y C): {len(no_monotona)} {no_monotona[:10]}")

print("\n== D · _moneda_de, forma a forma")
for forma in list(FORMAS) + CON_ESCALA + ["DÓLAR", "Euros", "EUR", " eur ", "dólares", "euroz"]:
    print(f"   {forma!r:12} → {VE._moneda_de(forma)!r}" + ("" if forma not in FORMAS or VE._moneda_de(forma) == FORMAS[forma] or FORMAS[forma] == "corona" else f"   (moneda real: {FORMAS[forma]})"))
