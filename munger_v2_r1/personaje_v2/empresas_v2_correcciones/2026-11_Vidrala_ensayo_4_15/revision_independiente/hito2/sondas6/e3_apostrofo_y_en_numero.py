#!/usr/bin/env python3
"""e3 · sexta comprobación · V3 y V7: el borde de en_numero (apóstrofo, decimal sin cero, «\\Z») y los límites de cifra de _lectura_cifra
(«(?<!\\d')» y «[.,']\\d»).
A) casos a nivel de unidad con 876bfc2, 8196522 y la propuesta de la 5.ª: miles con apóstrofo (ASCII y TIPOGRÁFICO), el corte por
   delante y por detrás, el doble corte, y formas en las que «cifra + apóstrofo + cifra» NO es un separador de miles («Q1'24», «H1'24»);
B) tabla EXHAUSTIVA de en_numero según los dos caracteres anteriores a la cita (18 × 18), con la cita cortada dentro de una palabra por
   el final para forzar esa vía: qué pares pasan de pendiente a discrepancia y al revés entre los dos códigos;
C) decimal sin cero y puntos conductores: qué formas vuelven a discrepancia (coste declarado en la quinta comprobación);
D) textos REALES (los 73 textos conservados citados): cuántas veces aparece «cifra + apóstrofo + cifra» (ASCII o tipográfico), un decimal
   sin cero delante y un punto o una coma pegados a una cifra tras un espacio o un signo (las formas que ahora dan discrepancia si la
   cita empieza en la cifra); y cuántas CITAS reales empiezan justo detrás de una de esas formas.
Uso: python3 -I -B e3_apostrofo_y_en_numero.py"""
import collections, itertools, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun6 import VE, VP, VQ, ACT, ANT, PV  # noqa: E402
print(f"VE = {ACT} · VP = {ANT} · VQ = 876bfc2 con las propuestas de la 5.ª")


def caso(nombre, pag, cita, vf, esperado=None):
    a, b, q = VP._cita_cifra(cita, vf, pag)[0], VE._cita_cifra(cita, vf, pag)[0], VQ._cita_cifra(cita, vf, pag)[0]
    marca = "" if esperado is None or b == esperado or (esperado == "no ok" and b != "ok") else f"   <<< el revisor esperaba «{esperado}»"
    print(f"   {nombre}\n      página={pag!r} cita={cita!r} vf={vf!r} · 876bfc2: {a:14} 8196522: {b:14} propuesta 5.ª: {q}{marca}")
    return b


print("\n== A · apóstrofo")
caso("A1 miles con apóstrofo ASCII, cita cortada por delante: «1'849,7» citada «849,7»", "Total 1'849,7\n", "849,7", 849.7, "ausente")
caso("A2 lo mismo con la cita completa y el valor cortado", "Total 1'849,7\n", "Total 1'849,7", 849.7, "ausente")
caso("A3 corte por detrás: «849'697» citada «Total 849» con valor 849", "Total 849'697\n", "Total 849", 849, "ausente")
caso("A4 lo mismo con la cita completa y el valor cortado", "Total 849'697\n", "Total 849'697", 849, "ausente")
caso("A5 control: la cifra entera con apóstrofo y punto decimal «1'849.7» = 1849,7", "Total 1'849.7\n", "Total 1'849.7", 1849.7, "ok")
caso("A6 control: «849'697» = 849697", "Total 849'697\n", "Total 849'697", 849697, "ok")
caso("A7 la cifra entera con apóstrofo y COMA decimal «1'849,7» = 1849,7 (forma que _cifras no genera; ya era así)", "Total 1'849,7\n", "Total 1'849,7", 1849.7, None)
caso("A8 dos apóstrofos «1'234'567» citada «234'567» con valor 234567", "Total 1'234'567\n", "234'567", 234567, "ausente")
caso("A9 «1'234'567» citada entera con valor 1234567", "Total 1'234'567\n", "Total 1'234'567", 1234567, "ok")
caso("A10 «1'234'567» con valor 567 (cita completa)", "Total 1'234'567\n", "Total 1'234'567", 567, "ausente")
caso("A11 «1'234'567» con valor 234 (cifra entre dos apóstrofos)", "Total 1'234'567\n", "Total 1'234'567", 234, "ausente")
caso("A12 doble corte: «1'849,7 millones» citada «849,7 mill» (la única vía que llega al apóstrofo de en_numero)", "Total 1'849,7 millones\n", "849,7 mill", 849.7, "ausente")
print("   -- apóstrofo TIPOGRÁFICO y otros signos parecidos (lo que suelen dar los PDF de informes suizos)")
for nombre, ap in (("U+2019 ’", "’"), ("U+02BC ʼ", "ʼ"), ("U+2032 ′", "′"), ("U+00B4 ´", "´"), ("U+0060 `", "`"), ("U+2018 ‘", "‘")):
    b1 = caso(f"A13 {nombre}: «1{ap}849,7» citada «849,7» con valor 849,7", f"Total 1{ap}849,7\n", "849,7", 849.7, "no ok")
    b2 = caso(f"A14 {nombre}: «849{ap}697» citada «Total 849» con valor 849", f"Total 849{ap}697\n", "Total 849", 849, "no ok")
    caso(f"A15 {nombre}: la cifra entera «1{ap}849.7» = 1849,7", f"Total 1{ap}849.7\n", f"Total 1{ap}849.7", 1849.7, None)
print("   -- «cifra + apóstrofo + cifra» que NO es un separador de miles")
caso("A16 periodo abreviado «Q1'24»: el 24 tras el apóstrofo, valor 24", "Ventas Q1'24 crecen\n", "Ventas Q1'24 crecen", 24, None)
caso("A17 «9M'24 849,7»: la cifra de después no se ve afectada", "Ventas 9M'24 849,7\n", "Ventas 9M'24 849,7", 849.7, "ok")
caso("A18 «H1'24: 24 tiendas» (el 24 aparece además suelto)", "H1'24: 24 tiendas\n", "H1'24: 24 tiendas", 24, "ok")
caso("A19 año abreviado tras letra «FY'24» con valor 24 (no hay cifra delante del apóstrofo)", "Ventas FY'24\n", "Ventas FY'24", 24, "ok")
caso("A20 cita que empieza tras «cifra + apóstrofo»: «24 crecen» en «Q1'24 crecen»", "Ventas Q1'24 crecen\n", "24 crecen", 24, None)
caso("A21 minutos y segundos «5'30» con valor 30", "Tiempo 5'30\n", "Tiempo 5'30", 30, None)
caso("A22 comilla de cierre tras una cifra y otra cifra pegada «'2023'849»", "Plan '2023'849\n", "Plan '2023'849", 849, None)

print("\n== B · en_numero según los dos caracteres anteriores (cita «5 vec» en «…XY5 veces»: cortada dentro de una palabra por el final)")
CH = ["7", "a", " ", ".", ",", "'", "’", "(", ")", "-", "−", "$", "€", "%", ":", "/", "_", "\n"]
nom = lambda ch: {"\n": "⏎", " ": "␠"}.get(ch, ch)  # noqa: E731
camb = collections.defaultdict(list)
n = 0
for x, y in itertools.product(CH, repeat=2):
    pag = "inicio de la línea " + x + y + "5 veces\n"
    a, b, q = VP._cita_cifra("5 vec", 5, pag)[0], VE._cita_cifra("5 vec", 5, pag)[0], VQ._cita_cifra("5 vec", 5, pag)[0]
    n += 1
    if a != b:
        camb[(a, b)].append(nom(x) + nom(y))
    if b != q:
        camb[("frente a la propuesta", q, b)].append(nom(x) + nom(y))
print(f"   {n} pares de caracteres anteriores")
for k, v in camb.items():
    print(f"   {' → '.join(k)}: {len(v)} pares: {' '.join(v)}")
for pre in ("", ".", ",", "'", "7", "7'", "7.", " ."):
    pag = pre + "5 veces\n"
    print(f"   principio de la página + {pre!r:5}: 876bfc2 {VP._cita_cifra('5 vec', 5, pag)[0]:14} 8196522 {VE._cita_cifra('5 vec', 5, pag)[0]:14} propuesta {VQ._cita_cifra('5 vec', 5, pag)[0]}")
print("   -- lo mismo con la cita NO cortada por el final («5 veces»): la vía de en_numero solo se alcanza si el principio va pegado a cifra, punto o coma")
camb2 = collections.defaultdict(list)
for x, y in itertools.product(CH, repeat=2):
    pag = "inicio de la línea " + x + y + "5 veces\n"
    a, b = VP._cita_cifra("5 veces", 5, pag)[0], VE._cita_cifra("5 veces", 5, pag)[0]
    if a != b:
        camb2[(a, b)].append(nom(x) + nom(y))
for k, v in camb2.items():
    print(f"   {' → '.join(k)}: {len(v)} pares: {' '.join(v)}")

print("\n== C · decimal sin cero delante y puntos conductores")
caso("C1 «.5» citada «5 veces» (valor 5)", "Ratio .5 veces\n", "5 veces", 5, "ausente")
caso("C2 «-.5»", "Variación -.5 puntos\n", "5 puntos", 5, "ausente")
caso("C3 «(.5)»", "Resultado (.5)\n", "5)", 5, "ausente")
caso("C4 «$.85»", "Earnings per share $.85 $1.02\n", "85 $1.02", 85, "ausente")
caso("C5 «,5»", "Ratio ,5 veces\n", "5 veces", 5, "ausente")
caso("C6 al principio de la página «.5»", ".5 veces\n", "5 veces", 5, "ausente")
caso("C7 al principio de una línea «⏎.5»", "Ratio\n.5 veces\n", "5 veces", 5, "ausente")
caso("C8 fin de frase pegado «ejercicio.849,7» (sigue pendiente)", "al cierre del ejercicio.849,7 millones\n", "849,7 millones", 849.7, "no_localizada")
caso("C9 puntos conductores seguidos «....130,8» (sigue pendiente)", "Total ............130,8\n", "130,8", 130.8, "no_localizada")
caso("C10 COSTE: puntos conductores con espacios «. . . .130,8» (vuelve a discrepancia)", "Total . . . .130,8\n", "130,8", 130.8, None)
caso("C11 COSTE: punto tras un espacio «ejercicio .849,7» (vuelve a discrepancia)", "al cierre del ejercicio .849,7 millones\n", "849,7 millones", 849.7, None)
caso("C12 COSTE: punto tras paréntesis de nota «(1).849,7» (vuelve a discrepancia)", "Ventas (1).849,7\n", "849,7", 849.7, None)
caso("C13 COSTE: coma tras comillas o paréntesis «),849,7»", "Ventas (netas),849,7\n", "849,7", 849.7, None)
caso("C14 COSTE: puntos suspensivos tras espacio « ...849,7»: el último punto sigue a otro punto (pendiente)", "Ventas ...849,7\n", "849,7", 849.7, "no_localizada")
caso("C15 control: la cita completa con su punto «.5 veces» y valor 0,5 (la forma «.5» no es de _cifras; ya era así)", "Ratio .5 veces\n", ".5 veces", 0.5, None)
caso("C16 el caso «Ajuste .5» de la prueba nueva, cita «.5» y valor 0,5", "Ajuste .5", ".5", 0.5, None)

print("\n== D · textos reales")
E14 = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_14")
EXPS = ["vidrala_decisiones_INVALIDO_perdio_analisis/Vidrala", "elis_decisiones/Elis", "viscofan/Viscofan", "elis_motor_A/Elis", "vidrala_decisiones/Vidrala", "vidrala/Vidrala", "viscofan_decisiones/Viscofan"]
textos = {}
citas = []
for exp in EXPS:
    c = os.path.join(E14, exp)
    reg, err = VE.cargar(c)
    for e in reg["entradas"]:
        f = e.get("fuente") if isinstance(e.get("fuente"), dict) else {}
        if f.get("archivo") and str(f["archivo"]).lower().endswith(".txt"):
            r = VE._ruta_fuente(c, f["archivo"])
            if r:
                textos[os.path.realpath(r)] = None
                if VE._num(f.get("valor_fuente")):
                    citas.append((exp, e.get("celda"), os.path.realpath(r), f.get("pagina"), f.get("cita"), f.get("valor_fuente")))
RX = {"cifra + apóstrofo ASCII + cifra": re.compile(r"\d'\d"), "cifra + apóstrofo tipográfico (’ ʼ ′ ´ ` ‘) + cifra": re.compile(r"\d[’ʼ′´`‘]\d"),
      "decimal sin cero delante (tras principio, espacio, signo, paréntesis o moneda)": re.compile(r"(?:^|[^\w.,])[.,]\d", re.M),
      "apóstrofo (cualquiera) pegado a una cifra por algún lado": re.compile(r"\d['’]|['’]\d")}
tot = collections.Counter()
ej = collections.defaultdict(list)
for p in sorted(textos):
    t = open(p, encoding="utf-8", errors="replace").read()
    for k, rx in RX.items():
        ms = list(rx.finditer(t))
        tot[k] += len(ms)
        for m in ms[:3]:
            if len(ej[k]) < 8:
                ej[k].append((os.path.basename(p)[:28], t[max(0, m.start() - 22):m.end() + 14].replace("\n", "⏎")))
print(f"   {len(textos)} textos conservados citados; {len(citas)} citas numéricas con fuente de texto")
for k in RX:
    print(f"   {k}: {tot[k]}")
    for x in ej[k][:6]:
        print("        ", repr(x))
# citas reales: ¿alguna tiene la cifra pegada a un apóstrofo o empieza tras un punto o coma de «decimal sin cero»? ¿alguna cambia de estado?
c = collections.Counter()
for exp, celda, ruta, pagina, cita, vf in citas:
    est, pag = VE._pagina_examinable(ruta, pagina)
    if est != "ok":
        c["página no examinable"] += 1
        continue
    a, b = VP._cita_cifra(cita, vf, pag), VE._cita_cifra(cita, vf, pag)
    c[f"876bfc2 {a[0]} → 8196522 {b[0]}"] += 1
    if a != b:
        c["CAMBIA (estado o detalle)"] += 1
    if re.search(r"\d['’]\d", str(cita)):
        c["cita con cifra + apóstrofo + cifra"] += 1
    for linea, i, j in VE._apariciones_en_pagina(cita, pag):
        if re.search(r"(?:\d['’]|(?:^|[^\w.,])[.,])$", linea[:i]) and re.match(r"\d", str(cita).strip()):
            c["cita que empieza justo detrás de «cifra + apóstrofo» o de un punto o coma inicial"] += 1
print(f"   citas reales: {dict(c)}")
