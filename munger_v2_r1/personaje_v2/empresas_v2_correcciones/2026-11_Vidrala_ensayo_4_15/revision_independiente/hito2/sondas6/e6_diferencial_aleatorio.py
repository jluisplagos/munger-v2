#!/usr/bin/env python3
"""e6 · sexta comprobación · diferencial ALEATORIO de _cita_cifra (con la página) entre 876bfc2 (VP), 8196522 (VE) y la propuesta de la
5.ª (VQ). Semilla fija; no usa datos reales ni escribe nada. Páginas de una a tres líneas hechas con cifras (enteros, años, decimales,
miles con punto, coma, espacio, apóstrofo ASCII y tipográfico, decimales sin cero delante), palabras, guiones, paréntesis, monedas,
puntos conductores y saltos de línea; la cita es un trozo de la página (cortado entre palabras o en un carácter cualquiera) y el valor,
una cifra de la página, un trozo de una cifra («849,7» de «1'849,7») o su contrario.
Se comprueba:
 (1) toda diferencia de ESTADO entre 876bfc2 y 8196522 aparece en una página que tiene alguno de los rasgos que la candidata cambia
     (apóstrofo ASCII pegado a cifras; salto de línea justo antes de un guion pegado a una cifra; punto o coma inicial pegado a una cifra;
     línea que empieza por una cifra tras otra que acaba en cifra); las que no, se listan;
 (2) las transiciones HACIA «ok» (aceptaciones nuevas), una a una por clase, con ejemplos;
 (3) entre 8196522 y la propuesta de la 5.ª solo hay diferencias con un apóstrofo ASCII pegado a cifras.
Uso: python3 -I -B e6_diferencial_aleatorio.py [N]"""
import collections, os, random, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun6 import VE, VP, VQ, ACT, ANT  # noqa: E402
N = int(sys.argv[1]) if len(sys.argv) > 1 else 200000
rnd = random.Random(20261116 + 6)
GUI = "-‐‑‒–—−"
print(f"VE = {ACT} · VP = {ANT} · VQ = 876bfc2 con las propuestas de la 5.ª · {N} casos")


def numero():
    """(texto, [valores candidatos])"""
    r = rnd.random()
    if r < 0.18:
        a = rnd.choice([rnd.randint(1880, 2120), rnd.randint(2019, 2026)])
        return str(a), [a]
    if r < 0.30:
        a = rnd.randint(0, 999)
        return str(a), [a]
    if r < 0.45:
        a, d = rnd.randint(0, 999), rnd.randint(0, 9)
        s = rnd.choice([",", "."])
        return f"{a}{s}{d}", [a + d / 10, a, d]
    if r < 0.80:
        m, c, d = rnd.randint(1, 9), rnd.randint(100, 999), rnd.randint(0, 9)
        sep = rnd.choice(["'", "'", "'", "’", ".", ",", " ", "ʼ"])
        dec = rnd.choice(["", "", ",", "."])
        if dec and dec == sep:
            dec = "," if sep == "." else "."
        t = f"{m}{sep}{c}" + (f"{dec}{d}" if dec else "")
        v = m * 1000 + c + (d / 10 if dec else 0)
        return t, [v, c + (d / 10 if dec else 0), c, m]
    if r < 0.92:
        d = rnd.randint(1, 99)
        s = rnd.choice([".", ","])
        return f"{s}{d}", [d, d / (10 if d < 10 else 100)]
    a, b = rnd.randint(1, 9), rnd.randint(100, 999)
    return f"{a}'{b}'{rnd.randint(100, 999)}", [b, a]


def trozo(vals):
    r = rnd.random()
    if r < 0.42:
        t, v = numero()
        vals.extend(v)
        return t
    if r < 0.55:
        return rnd.choice(GUI[:1] * 5 + "–−" + GUI)
    if r < 0.72:
        return rnd.choice([" ", " ", " ", "  ", "   "])
    if r < 0.80:
        return "\n"
    if r < 0.90:
        return rnd.choice(["Total ", "Saldo", "Ejercicio ", "FY", "Q1'", "H1'", "p.", "Nota ", "(1)", "ejercicio", "millones", "veces", "Ratio ", "CHF", "EUR "])
    return rnd.choice(["(", ")", ":", ";", "/", "€", "$", "%", ".", "..", "....", ". . . .", ",", "'", "’", "+", "="])


RASGOS = {"apóstrofo ASCII pegado a cifras": re.compile(r"\d'\d"),
          "salto de línea justo antes de un guion pegado a una cifra": re.compile(r"\n[" + re.escape(GUI) + r"](?:[€$£¥]|(?:EUR|USD|GBP|CHF|JPY|DKK|SEK|NOK|BRL)\b)?\s?\d", re.I),
          "punto o coma inicial pegado a una cifra": re.compile(r"(?:^|[^\w.,])[.,]\d", re.M),
          "línea que empieza por cifra tras otra que acaba en cifra o en cifra y separador": re.compile(r"\d[.,']?\n\d")}
tr = collections.Counter()
ej = {}
sin_rasgo = []
hacia_ok = collections.Counter()
ej_ok = collections.defaultdict(list)
frente_q = collections.Counter()
ej_q = collections.defaultdict(list)
for _ in range(N):
    vals = []
    pag = "".join(trozo(vals) for _i in range(rnd.randint(3, 12)))
    if not vals or not pag.strip():
        continue
    # la cita: un trozo de la página
    if rnd.random() < 0.6:
        cortes = [0] + [m.start() for m in re.finditer(r"(?<=\s)\S", pag)]
        fines = [m.end() for m in re.finditer(r"\S(?=\s|$)", pag)]
        i = rnd.choice(cortes)
        fs = [f for f in fines if f > i]
        j = rnd.choice(fs) if fs else len(pag)
    else:
        i = rnd.randrange(len(pag))
        j = rnd.randint(i + 1, len(pag))
    cita = pag[i:j]
    if not cita.strip():
        continue
    vf = rnd.choice(vals) * rnd.choice([1, 1, -1])
    a, b, q = VP._cita_cifra(cita, vf, pag)[0], VE._cita_cifra(cita, vf, pag)[0], VQ._cita_cifra(cita, vf, pag)[0]
    if a != b:
        rs = [k for k, rx in RASGOS.items() if rx.search(pag)]
        tr[(a, b)] += 1
        ej.setdefault((a, b), (pag, cita, vf))
        if not rs:
            sin_rasgo.append((pag, cita, vf, a, b))
        if b == "ok":
            k = " + ".join(rs) or "NINGUNO"
            hacia_ok[(a, k)] += 1
            if len(ej_ok[(a, k)]) < 3:
                ej_ok[(a, k)].append((pag, cita, vf))
    else:
        tr[("igual", a)] += 1
    if b != q:
        k = "con apóstrofo ASCII pegado a cifras" if RASGOS["apóstrofo ASCII pegado a cifras"].search(pag) else "SIN él"
        frente_q[(q, b, k)] += 1
        if len(ej_q[(q, b, k)]) < 2:
            ej_q[(q, b, k)].append((pag, cita, vf))
print("== transiciones 876bfc2 → 8196522")
for k, v in sorted(tr.items(), key=lambda kv: (kv[0][0] == "igual", -kv[1])):
    if k[0] == "igual":
        print(f"   igual ({k[1]}): {v}")
    else:
        print(f"   {k[0]:20} → {k[1]:20}: {v:6}   ej.: {ej[k]!r}")
print(f"== (1) diferencias de estado en páginas SIN ninguno de los rasgos cambiados: {len(sin_rasgo)}")
for x in sin_rasgo[:8]:
    print("     ", repr(x))
print("== (2) transiciones HACIA «ok» (aceptaciones nuevas), por estado anterior y rasgos de la página")
for k, v in sorted(hacia_ok.items(), key=lambda kv: -kv[1]):
    print(f"   {k[0]:20} → ok · rasgos: {k[1]}: {v}")
    for x in ej_ok[k]:
        print("        ", repr(x))
print("== (3) 8196522 frente a la propuesta de la 5.ª")
for k, v in sorted(frente_q.items(), key=lambda kv: -kv[1]):
    print(f"   propuesta {k[0]:20} · 8196522 {k[1]:20} ({k[2]}): {v}   ej.: {ej_q[k][:1]!r}")
print(f"   diferencias SIN apóstrofo ASCII pegado a cifras: {sum(v for k, v in frente_q.items() if k[2] == 'SIN él')}")
