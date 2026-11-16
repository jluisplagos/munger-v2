#!/usr/bin/env python3
"""d5 · diferencial ALEATORIO entre 7a6583b (VP) y 876bfc2 (VE) de lo que cambia en la lectura de la cifra (quinta comprobación).
Semilla fija; no usa datos reales ni escribe nada.
A) _signo_en_cita: líneas aleatorias con años, enteros, decimales, guiones (ASCII y tipográficos), prefijos (FY, AF, EJ, Graf, H…),
   paréntesis, monedas y espacios. Para cada cifra de la línea se compara el signo de los dos códigos. Propiedades que se comprueban:
   (1) la única transición admitida es «+ → indeterminado» (la corrección de Q3 no puede crear ni un «+» ni un «−» nuevos);
   (2) lo que sigue en «+» tras un guion pegado a otra cifra cumple la regla declarada, reimplementada aparte por el revisor
       (años de cuatro cifras, 1900 ≤ a ≤ b ≤ 2100, con el primero al principio de una palabra o tras FY/AF/EJ como palabra; o una fecha d-m-aaaa);
   (3) lo que pasa a indeterminado NO la cumple.
B) _cita_cifra con la página: páginas aleatorias de una a tres líneas, citas que son un trozo de la página (cortado en un límite de
   palabra o en medio de una palabra o de un número) y valor_fuente tomado de una cifra de la cita (con su signo o el contrario).
   Transiciones admitidas: el mismo estado; «ok» o «signo_distinto» → «signo_indeterminado» (Q3); «ausente» → «no_localizada» (Q4).
   Nunca un estado distinto de «ok» → «ok».
C) el máximo de apariciones: páginas con la cita repetida N veces (N alrededor de 200): hasta 200, el mismo estado que 7a6583b; más de 200, pendiente.
Uso: python3 -I -B d5_diferencial_aleatorio.py [N_A] [N_B]"""
import collections, os, random, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun5 import VE, VP, ACT, ANT  # noqa: E402

NA = int(sys.argv[1]) if len(sys.argv) > 1 else 300000
NB = int(sys.argv[2]) if len(sys.argv) > 2 else 150000
rnd = random.Random(20261116)
GUI = "-‐‑‒–—−﹣－"
nom = {1: "+", -1: "−", None: "indeterminado"}


def numero():
    r = rnd.random()
    if r < 0.45:
        return str(rnd.choice([rnd.randint(1880, 2120), rnd.randint(1990, 2030), rnd.randint(2019, 2026)]))
    if r < 0.6:
        return str(rnd.randint(0, 99))
    if r < 0.7:
        return str(rnd.randint(100, 9999))
    if r < 0.85:
        return f"{rnd.randint(0, 2100)},{rnd.randint(0, 9)}"
    return f"{rnd.randint(1, 9)}.{rnd.randint(100, 999)}" + rnd.choice(["", f",{rnd.randint(0, 9)}"])


def trozo():
    r = rnd.random()
    if r < 0.50:
        return numero()
    if r < 0.72:
        return rnd.choice(GUI[:3] + "-" * 6 + "–" * 3 + "−" * 2 + GUI)
    if r < 0.84:
        return rnd.choice([" ", " ", "  ", "   "])
    if r < 0.93:
        return rnd.choice(["FY", "AF", "EJ", "fy", "Graf", "H", "Saldo ", "Notas ", "Ejercicio ", "Law ", "L. ", "T", "p.", "nº "])
    return rnd.choice(["(", ")", ":", ";", "/", "€", "$", "%", ".", ",", "[", "|", "=", "+", "EUR ", "x"])


def linea():
    return "".join(trozo() for _ in range(rnd.randint(2, 9)))


def regla_declarada(t, ini, fin):
    """Reimplementación del revisor de la regla de Q3: ¿la cifra t[ini:fin] va tras un guion PEGADO que es un intervalo de años o una fecha?"""
    antes = t[:ini]
    if not antes or antes[-1] not in GUI:
        return False
    previo, tok = antes[:-1], t[ini:fin]
    if not re.fullmatch(r"\d{4}", tok):
        return False
    m = re.search(r"(\d+)$", previo)
    if m is None:
        return False
    a, resto = m.group(1), previo[:m.start()]
    if len(a) == 4 and 1900 <= int(a) <= int(tok) <= 2100:
        if resto == "" or not re.match(r"[\w.,]", resto[-1]):
            return True  # el año al principio de una palabra
        mp = re.search(r"(?:fy|af|ej)$", resto, re.I)
        if mp and (mp.start() == 0 or not re.match(r"[\w.,]", resto[mp.start() - 1])):
            return True  # prefijo FY/AF/EJ como palabra
    # fecha d-m-aaaa (el guion entre el día y el mes es el ASCII, como en el código)
    mf = re.search(r"(\d{1,2})-(\d{1,2})$", previo)
    if mf and (mf.start() == 0 or not re.match(r"[\w.,]", previo[mf.start() - 1])):
        return True
    return False


print(f"VE = {ACT} · VP = {ANT} · semilla 20261116")
print(f"== A · _signo_en_cita sobre {NA} líneas aleatorias")
trans, ej = collections.Counter(), {}
otras, ej_otras = collections.Counter(), {}
viol = collections.Counter()
ejv = {}
ncif = 0
for _ in range(NA):
    t = linea()
    for m in re.finditer(r"(?<![\d.,])\d+(?:[.,]\d+)*(?!\d|[.,]\d)", t):
        ncif += 1
        a, b = VP._signo_en_cita(t, m.start(), m.end()), VE._signo_en_cita(t, m.start(), m.end())
        k = (nom[a], nom[b])
        trans[k] += 1
        ej.setdefault(k, (t, m.group(0)))
        if a != b and not (a == 1 and b is None):
            viol["(1) transición no admitida " + str(k)] += 1
            ejv.setdefault("(1)", (t, m.group(0)))
        # la regla del intervalo solo interviene si hay un guion pegado delante de la cifra y otra cifra pegada delante del guion
        tras_guion_y_cifra = re.search(r"\d[" + re.escape(GUI) + r"]$", t[:m.start()]) is not None
        if tras_guion_y_cifra:
            rd = regla_declarada(t, m.start(), m.end())
            trans[("tras «cifra-»", "regla declarada" if rd else "no la cumple", nom[b])] += 1
            if rd and b is None:
                # la regla del intervalo se cumple pero otra regla anterior deja el signo indeterminado (paréntesis sin abrir, menos detrás…): con 7a6583b tiene que ser igual
                otras[(nom[a], "«)» detrás sin «(»" if re.match(r"\s*\)", t[m.end():]) else "guion detrás no seguido de cifra" if re.match("[" + re.escape(GUI) + r"](?!\d)", t[m.end():]) else
                       "moneda o % entre medias" if re.match(r"\s?(?:[€$£¥%]|EUR)", t[m.end():]) else "otra")] += 1
                ej_otras.setdefault(len(ej_otras), (t, m.group(0))) if len(ej_otras) < 5 else None
            if b == 1 and not rd:
                viol["(2) «+» tras un guion pegado a una cifra que no cumple la regla declarada"] += 1
                ejv.setdefault("(2)", (t, m.group(0)))
            if a == 1 and b is None and rd:
                viol["(3) pasa a indeterminado y cumple la regla declarada"] += 1
                ejv.setdefault("(3)", (t, m.group(0)))
print(f"   {ncif} cifras evaluadas")
for k, v in sorted(trans.items(), key=str):
    if len(k) == 2:
        print(f"   7a6583b {k[0]:14} → 876bfc2 {k[1]:14} {v:8}   ej.: {ej[k]}")
for k, v in sorted(trans.items(), key=str):
    if len(k) == 3:
        print(f"   {k[0]} · {k[1]:16} · 876bfc2 {k[2]:14} {v:8}")
print(f"   «regla declarada» e indeterminado con 876bfc2, por la regla que lo decide (signo con 7a6583b, motivo): {dict(otras)} · ej.: {list(ej_otras.values())}")
print(f"   violaciones de las propiedades: {dict(viol) or 'ninguna'} {ejv or ''}")

print(f"\n== B · _cita_cifra con la página sobre {NB} casos aleatorios")
ADM = {("ok", "signo_indeterminado"), ("signo_distinto", "signo_indeterminado"), ("ausente", "no_localizada")}
tb, ejb, violb = collections.Counter(), {}, []
q4_mal = 0
for _ in range(NB):
    pag = "\n".join(rnd.choice(["", "Total ", "Ventas ", "al cierre del ejercicio.", "p.", "Nota "]) + linea() + rnd.choice(["", " millones", " m", "x"]) for _ in range(rnd.randint(1, 3))) + "\n"
    nums = list(re.finditer(r"(?<![\d.,])\d+(?:[.,]\d+)*(?!\d|[.,]\d)", pag))
    if not nums:
        continue
    m = rnd.choice(nums)
    # la cita: desde un punto antes de la cifra hasta un punto después, o cortada dentro de la cifra
    r = rnd.random()
    if r < 0.5:
        i, j = rnd.randint(max(0, m.start() - 12), m.start()), rnd.randint(m.end(), min(len(pag), m.end() + 10))
    elif r < 0.75:
        i, j = rnd.randint(m.start(), max(m.start(), m.end() - 1)), rnd.randint(m.end(), min(len(pag), m.end() + 6))
    else:
        i, j = rnd.randint(max(0, m.start() - 8), m.start()), rnd.randint(m.start() + 1, m.end())
    cita = pag[i:j].strip()
    if not cita:
        continue
    tok = m.group(0)
    try:
        vf = float(tok.replace(".", "").replace(",", ".")) if "," in tok or re.fullmatch(r"\d\.\d{3}", tok) else float(tok)
    except ValueError:
        continue
    vf = vf if rnd.random() < 0.6 else -vf
    a, b = VP._cita_cifra(cita, vf, pag), VE._cita_cifra(cita, vf, pag)
    k = (a[0], b[0])
    tb[k] += 1
    ejb.setdefault(k, (pag, cita, vf))
    if a[0] != b[0] and k not in ADM:
        violb.append((k, pag, cita, vf))
    if k == ("ausente", "no_localizada"):
        # Q4: tiene que haber un fragmento de la cita precedido por «[.,]» que no sigue a una cifra, y ninguno cortado dentro de un número
        pal = cita.split()
        t_ = re.sub("[   ]", " ", pag)
        fr = list(re.finditer(r"\s+".join(re.escape(w) for w in pal), t_, re.I))
        bien = any(re.search(r"(?:^|[^\d])[.,]$", t_[:x.start()]) for x in fr) and not any(
            (re.match(r"\d", pal[0]) and re.search(r"\d[.,]?$", t_[:x.start()])) or (re.search(r"\d$", pal[-1]) and re.match(r"\d|[.,]\d", t_[x.end():x.end() + 2])) for x in fr)
        q4_mal += not bien
for k, v in sorted(tb.items()):
    marca = "" if k[0] == k[1] else ("   (admitida)" if k in ADM else "   <<< NO ADMITIDA")
    print(f"   7a6583b {k[0]:20} → 876bfc2 {k[1]:20} {v:8}{marca}" + (f"   ej.: {ejb[k]!r}" if k[0] != k[1] else ""))
print(f"   transiciones no admitidas: {len(violb)} {violb[:3]}")
print(f"   «ausente → no_localizada» que no responden a un punto o una coma que no es de un número: {q4_mal}")
print(f"   pasan de un estado distinto de «ok» a «ok»: {sum(v for k, v in tb.items() if k[0] != 'ok' and k[1] == 'ok')}")

print("\n== C · el máximo de apariciones (N alrededor de 200)")
for n in (1, 2, 150, 199, 200, 201, 202, 250, 1000):
    for nombre, linea_, cita, vf in (("todas iguales, positivas", "Total: 849,7", "Total: 849,7", 849.7), ("todas iguales, negativas y valor positivo", "Total: (849,7)", "Total: (849,7)", 849.7),
                                     ("todas iguales, cero", "Saldo 0", "Saldo 0", 0), ("la cita es solo la cifra", "Total: 849,7", "849,7", 849.7)):
        for sep in ("\n", " "):
            pag = sep.join([linea_] * n) + "\n"
            a, b = VP._cita_cifra(cita, vf, pag), VE._cita_cifra(cita, vf, pag)
            esperado = "signo_indeterminado" if n > VE.MAX_APARICIONES_CITA else a[0]
            if b[0] != esperado or n in (200, 201):
                print(f"   N={n:5} sep={'líneas' if sep == chr(10) else 'una línea':10} {nombre:42} 7a6583b {a[0]:20} → 876bfc2 {b[0]:20}" + ("" if b[0] == esperado else "   <<< distinto de lo esperado"))
# una cita con apariciones mezcladas: 150 en positivo y 51 en negativo (201): antes indeterminado por lecturas distintas, ahora por el máximo
pag = "\n".join(["Total: 849,7"] * 150 + ["Total: (849,7)"] * 51) + "\n"
print("   150 positivas + 51 negativas (201), cita «Total:» + cifra recortada «849,7»:", VP._cita_cifra("849,7", 849.7, pag), "→", VE._cita_cifra("849,7", 849.7, pag))
pag = "\n".join(["Total: (849,7)"] * 201) + "\n"
print("   201 apariciones todas NEGATIVAS con valor_fuente positivo (antes discrepancia «signo_distinto»):", VP._cita_cifra("849,7", 849.7, pag)[0], "→", VE._cita_cifra("849,7", 849.7, pag)[0])
pag = "\n".join(["Total: 1849,7"] * 201) + "\n"
print("   201 fragmentos dentro de un número (no son apariciones: el máximo no interviene):", VP._cita_cifra("849,7", 849.7, pag)[0], "→", VE._cita_cifra("849,7", 849.7, pag)[0])
