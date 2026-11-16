#!/usr/bin/env python3
"""e2 · sexta comprobación · V2: «\\Z» en el intervalo de años y en la fecha, y la lectura de una línea que empieza por «-2024».
A) los DOS casos de la prueba nueva de la batería («(V2) …»), tal cual, con 876bfc2 (sin la corrección) y con 8196522; el contexto que
   _apariciones_en_pagina entrega a la lectura con la cita «2024» (¿incluye la línea anterior?);
B) los casos que SÍ distinguen la corrección (la cita abarca las dos líneas), con los dos códigos;
C) formas del salto: «\\n», «\\r\\n», «\\r», salto de página «\\f», líneas en blanco, espacios al final o al principio, separadores Unicode,
   con guion ASCII, raya y menos Unicode; se espera que NINGUNA lea +2024 como «ok» con 8196522;
D) la lectura SIN página (solo la cita, _cita_contiene) y con la cita de una sola línea que empieza por el guion;
E) diferencial aleatorio de _signo_en_cita y de _cita_cifra entre 876bfc2, 8196522 y la propuesta de la 5.ª en textos con saltos de línea:
   toda diferencia entre 876bfc2 y 8196522 debe tener el salto justo delante del guion; entre 8196522 y la propuesta no debe haber ninguna.
Uso: python3 -I -B e2_v2_salto_de_linea.py"""
import collections, os, random, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun6 import VE, VP, VQ, ACT, ANT  # noqa: E402
print(f"VE = {ACT} · VP = {ANT} · VQ = 876bfc2 con las propuestas de la 5.ª")

print("\n== A · los dos casos de la prueba nueva «(V2)» de la batería, tal cual")
for cita, vf, pag in (("2024", 2024, "Ejercicio 2023\n-2024"), ("2024", 2024, "Cierre 31-12\n-2024")):
    ap = VE._apariciones_en_pagina(cita, pag)
    print(f"   _cita_cifra({cita!r}, {vf}, {pag!r}): 876bfc2 → {VP._cita_cifra(cita, vf, pag)[0]} · 8196522 → {VE._cita_cifra(cita, vf, pag)[0]} (la prueba espera «signo_distinto»)")
    print(f"      contexto que se lee (línea o líneas de la página que contienen la cita): {[a[0] for a in ap]!r}  ← no incluye la línea anterior")
print("   → la prueba pasa igual sin la corrección: con la cita «2024» solo se lee la línea «-2024», donde el guion ya era un signo menos")

print("\n== B · casos que distinguen la corrección (la cita abarca las dos líneas)")
for cita, vf, pag in (("Ejercicio 2023 -2024", 2024, "Ejercicio 2023\n-2024"), ("Cierre 31-12 -2024", 2024, "Cierre 31-12\n-2024"),
                      ("Ejercicio 2023 -2024", -2024, "Ejercicio 2023\n-2024"), ("FY2023 -2024", 2024, "FY2023\n-2024"), ("Notas 5-6 -2024", 2024, "Notas 5-6\n-2024"),
                      ("2023 -2024", 2024, "2023\n-2024"), ("Ejercicio 2023-2024", 2024, "Ejercicio 2023-2024"), ("Cierre 31-12-2024", 2024, "Cierre 31-12-2024")):
    print(f"   _cita_cifra({cita!r}, {vf}, {pag!r}): 876bfc2 → {VP._cita_cifra(cita, vf, pag)[0]:16} 8196522 → {VE._cita_cifra(cita, vf, pag)[0]}")

print("\n== C · formas del salto entre «…2023» y «-2024» (cita «Ejercicio 2023 G2024»; valor +2024; la página publica −2024 salvo donde se dice)")
SALTOS = {"\\n": "\n", "\\r\\n": "\r\n", "\\r": "\r", "\\f (salto de página)": "\f", "\\n\\n": "\n\n", "espacio + \\n": " \n", "\\n + espacio": "\n ", "tab + \\n": "\t\n", "\\n + tab": "\n\t",
          "\\v": "\v", "U+2028": " ", "U+2029": " ", "U+0085": "\x85", "U+00A0 + \\n": "\xa0\n", "\\n + U+00A0": "\n\xa0", "U+200B (invisible) + \\n": "​\n",
          "\\n + U+200B": "\n​", "un espacio (misma línea)": " ", "dos espacios (misma línea)": "  ", "nada (intervalo de verdad: +)": ""}
aceptan = []
for nombre, s in SALTOS.items():
    fila = []
    for g in "-–−":
        pag = f"Ejercicio 2023{s}{g}2024\n"
        cita = f"Ejercicio 2023 {g}2024" if s else f"Ejercicio 2023{g}2024"
        a, b = VP._cita_cifra(cita, 2024, pag)[0], VE._cita_cifra(cita, 2024, pag)[0]
        fila.append(f"«{g}» {a} → {b}")
        if b == "ok" and s:
            aceptan.append((nombre, g))
    print(f"   {nombre:30} " + " | ".join(fila))
print(f"   formas con salto o separador en las que 8196522 lee +2024 como «ok»: {aceptan}")

print("\n== D · sin página (solo la cita) y cita de una línea que empieza por el guion")
for cita, vf in (("Ejercicio 2023\n-2024", 2024), ("-2024", 2024), ("-2024", -2024), ("Ejercicio 2023 -2024", 2024), ("2023\n-2024", 2024), ("31-12\n-2024", 2024)):
    print(f"   _cita_cifra({cita!r}, {vf}) sin página: 876bfc2 → {VP._cita_cifra(cita, vf)[0]:16} 8196522 → {VE._cita_cifra(cita, vf)[0]}")
for cita, vf, pag in (("-2024", 2024, "Ejercicio 2023\n-2024"), ("-2024", -2024, "Ejercicio 2023\n-2024"), ("2023", 2023, "Ejercicio 2023\n-2024"), ("Ejercicio 2023", 2023, "Ejercicio 2023\n-2024")):
    print(f"   _cita_cifra({cita!r}, {vf}, {pag!r}): 876bfc2 → {VP._cita_cifra(cita, vf, pag)[0]:16} 8196522 → {VE._cita_cifra(cita, vf, pag)[0]}")

print("\n== E · diferencial aleatorio con saltos de línea")
rnd = random.Random(62)
GUI = "-‐‑‒–—−"
tr, trq = collections.Counter(), collections.Counter()
ej = {}
n_c = 0
for _ in range(250000):
    partes = []
    for _i in range(rnd.randint(2, 8)):
        r = rnd.random()
        partes.append(str(rnd.randint(1890, 2110)) if r < 0.4 else rnd.choice(GUI + "---") if r < 0.66 else rnd.choice(["\n", "\n", "\r\n", "\f", "\n\n", " \n", "\n "]) if r < 0.8
                      else rnd.choice([" ", "  ", "FY", "AF", "(", ")", "5-6", "31-12", "Nota ", "€", "12", "1.5", ".", ","]))
    t = "".join(partes)
    for m in re.finditer(r"(?<![\d.,])\d+(?!\d|[.,]\d)", t):
        n_c += 1
        a, b, q = VP._signo_en_cita(t, m.start(), m.end()), VE._signo_en_cita(t, m.start(), m.end()), VQ._signo_en_cita(t, m.start(), m.end())
        if a != b:
            k = (a, b, "con «\\n» justo antes del guion pegado" if re.search(r"\n[" + GUI + r"]$", t[:m.start()]) else "SIN él")
            tr[k] += 1
            ej.setdefault(k, (t, m.group(0)))
        if b != q:
            trq[(b, q)] += 1
            ej.setdefault(("q", b, q), (t, m.group(0)))
print(f"   _signo_en_cita: {n_c} cifras en 250.000 textos")
for k, v in sorted(tr.items(), key=str):
    print(f"      876bfc2 {k[0]} → 8196522 {k[1]} ({k[2]}): {v}   ej.: {ej[k]!r}")
print(f"      diferencias 876bfc2/8196522 SIN el salto justo antes del guion: {sum(v for k, v in tr.items() if k[2] == 'SIN él')}")
print(f"      diferencias entre 8196522 y la propuesta de la 5.ª: {sum(trq.values())} {dict(trq)}")
