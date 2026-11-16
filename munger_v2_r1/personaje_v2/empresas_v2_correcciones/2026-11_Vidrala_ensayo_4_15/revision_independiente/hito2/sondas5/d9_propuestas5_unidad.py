#!/usr/bin/env python3
"""d9 · las propuestas del revisor para V1, V2 y V3 (fable/prop5; NO es código entregado), a nivel de unidad frente a 876bfc2:
A) V1: todos los pares de marcas de moneda frente a la tabla del revisor (misma moneda → pendiente; distintas → exenta);
B) V2: los casos del salto de línea de d8 y un diferencial aleatorio de _signo_en_cita en líneas con y sin salto de línea;
C) V3: los casos del punto delante de la cifra de d7 y un diferencial aleatorio de _cita_cifra.
Uso: python3 -I -B d9_propuestas5_unidad.py"""
import collections, itertools, os, random, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun5 import VE, VP, F, cargar, ACT  # noqa: E402
VQ = cargar(os.path.join(F, "prop5", "munger_v2_r1", "personaje_v2", "scripts", "verificacion_entradas.py"), "verificacion_entradas_prop5")
assert "propuesta del revisor, V2" in open(VQ.__file__, encoding="utf-8").read()
print(f"VE = {ACT} · VQ = 876bfc2 con las propuestas V1, V2 y V3 del revisor")

print("== A · V1: pares de marcas de moneda")
FORMAS = {"€": "eur", "eur": "eur", "euro": "eur", "euros": "eur", "$": "usd", "usd": "usd", "dólar": "usd", "dolar": "usd", "£": "gbp", "gbp": "gbp", "libra": "gbp",
          "libras": "gbp", "¥": "jpy", "jpy": "jpy", "chf": "chf", "franco": "chf", "francos": "chf", "dkk": "dkk", "sek": "sek", "nok": "nok", "corona": "corona",
          "coronas": "corona", "brl": "brl", "reales": "brl"}


def misma(a, b):
    ca, cb = FORMAS[a], FORMAS[b]
    return ca == cb or ("corona" in (ca, cb) and {ca, cb} <= {"corona", "dkk", "sek", "nok"})


c = collections.Counter()
mal = []
for a, b in itertools.product(FORMAS, repeat=2):
    for sep in ("/", " / ", " por ", " per "):
        for env in ("{}", "({})", "tipo de cambio {}", "exchange rate {}"):
            u = env.format(a + sep + b)
            e, q = VE._unidad_monetaria_no_reconocida(u), VQ._unidad_monetaria_no_reconocida(u)
            c[("misma" if misma(a, b) else "distintas", "PENDIENTE" if e else "exenta", "PENDIENTE" if q else "exenta")] += 1
            if q != misma(a, b):
                mal.append(u)
            if e and not q:
                mal.append("(deja de estar pendiente) " + u)
for k, v in sorted(c.items()):
    print(f"   monedas {k[0]:9} · 876bfc2 {k[1]:9} → propuesta {k[2]:9}: {v}")
print(f"   unidades en las que la propuesta no coincide con la tabla del revisor o deja de dar pendiente: {len(mal)} {mal[:5]}")
for u in ("coronas/DKK", "francos/CHF", "reales/BRL", "corona/coronas", "DKK/SEK", "coronas/euros", "USD por EUR", "euros/EUR", "miles de euros", "EUR por acción", "millones de coronas"):
    print(f"      {u!r:24} 876bfc2 {'PENDIENTE' if VE._unidad_monetaria_no_reconocida(u) else 'no pendiente':13} propuesta {'PENDIENTE' if VQ._unidad_monetaria_no_reconocida(u) else 'no pendiente'}")

print("\n== B · V2: el salto de línea")
for pag, cita, vf, real in (("Gastos financieros\n-1980\n-2050\n", "Gastos financieros -1980 -2050", 2050, "−"), ("Gastos financieros\n-1980\n-2050\n", "Gastos financieros -1980 -2050", -2050, "−"),
                            ("Ejercicio 2023\n-2024\n", "Ejercicio 2023 -2024", 2024, "−"), ("Notas 5-6\n-2024\n", "Notas 5-6 -2024", 2024, "−"),
                            ("Ejercicio 2023-2024\n", "Ejercicio 2023-2024", 2024, "+"), ("Cierre 31-12-2024\n", "Cierre 31-12-2024", 2024, "+"), ("FY2023-2024\n", "FY2023-2024", 2024, "+"),
                            ("Periodo 2019-\n2020\n", "Periodo 2019- 2020", 2020, "+")):
    print(f"   página={pag!r} vf={vf} (publicada en {real}) · 876bfc2: {VE._cita_cifra(cita, vf, pag)[0]:20} propuesta: {VQ._cita_cifra(cita, vf, pag)[0]}")
rnd = random.Random(5)
GUI = "-‐‑‒–—−"
tr = collections.Counter()
ej = {}
for _ in range(200000):
    partes = []
    for _i in range(rnd.randint(2, 7)):
        r = rnd.random()
        partes.append(str(rnd.randint(1890, 2110)) if r < 0.45 else rnd.choice(GUI + "---") if r < 0.7 else "\n" if r < 0.82 else rnd.choice([" ", "  ", "FY", "(", ")", "5-6", "Nota ", "€", "12"]))
    t = "".join(partes)
    for m in re.finditer(r"(?<![\d.,])\d+(?!\d|[.,]\d)", t):
        a, b = VE._signo_en_cita(t, m.start(), m.end()), VQ._signo_en_cita(t, m.start(), m.end())
        k = (a, b, "con salto de línea justo antes del guion" if re.search(r"\n[" + GUI + r"]\s*$", t[:m.start()]) else "sin él")
        tr[k] += 1
        ej.setdefault(k, (t, m.group(0)))
for k, v in sorted(tr.items(), key=str):
    if k[0] != k[1]:
        print(f"   _signo_en_cita 876bfc2 {k[0]} → propuesta {k[1]} ({k[2]}): {v}   ej.: {ej[k]!r}")
print(f"   _signo_en_cita: {sum(tr.values())} cifras; distintas entre 876bfc2 y la propuesta: {sum(v for k, v in tr.items() if k[0] != k[1])}; de ellas, sin salto de línea antes del guion: "
      f"{sum(v for k, v in tr.items() if k[0] != k[1] and k[2] == 'sin él')}")

print("\n== C · V3: punto o coma delante de la cifra citada")
for nombre, pag, cita, vf in (("fin de frase «ejercicio.849,7»", "al cierre del ejercicio.849,7 millones\n", "849,7 millones", 849.7), ("abreviatura «p.12»", "véase p.12 del informe\n", "12 del informe", 12),
                              ("puntos conductores", "Total ............130,8\n", "130,8", 130.8), ("dentro de un número «1.849,7»", "total 1.849,7\n", "849,7", 849.7),
                              ("decimal sin cero « .5»", "Ratio .5 veces\n", "5 veces", 5), ("«-.5»", "Variación -.5 puntos\n", "5 puntos", 5), ("«(.5)»", "Resultado (.5)\n", "5)", 5),
                              ("«$.85»", "Earnings per share $.85 $1.02\n", "85 $1.02", 85), ("«,5»", "Ratio ,5 veces\n", "5 veces", 5), ("al principio de la página «.5»", ".5 veces\n", "5 veces", 5),
                              ("palabra cortada tras una línea que acaba en cifra (D1 de d7)", "Ventas 2023\n849,7 millones\n", "849,7 mill", 849.7),
                              ("«(1).849,7»", "Ventas (1).849,7\n", "849,7", 849.7)):
    print(f"   {nombre:62} 7a6583b: {VP._cita_cifra(cita, vf, pag)[0]:14} 876bfc2: {VE._cita_cifra(cita, vf, pag)[0]:14} propuesta: {VQ._cita_cifra(cita, vf, pag)[0]}")
