#!/usr/bin/env python3
"""c7 · observación (cuarta comprobación; no es de este diff): T4 quita los caracteres invisibles (guion blando, espacio de ancho cero,
U+200C, U+200D, U+2060, U+FEFF) del texto del documento HTML antes de leer la cifra; el texto conservado y el texto del PDF se leen tal
cual. ¿Qué lee _cita_cifra si entre el signo y la cifra hay un carácter invisible? Candidata anterior (f3d15e8) → cuarta (7a6583b).
Uso: python3 -I -B c7_invisibles_signo.py"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sondas3"))
from comun3 import VE, VP, ACT, ANT  # noqa: E402
print(f"VE = {ACT} · VP = {ANT}")
INV = [("guion blando U+00AD", chr(0xad)), ("espacio de ancho cero U+200B", chr(0x200b)), ("U+200C", chr(0x200c)), ("U+200D", chr(0x200d)), ("U+2060", chr(0x2060)), ("U+FEFF", chr(0xfeff)),
       ("marca de izquierda a derecha U+200E", chr(0x200e)), ("carácter de control U+0096", chr(0x96))]
print("== la página publica la cifra en NEGATIVO con un carácter invisible entre el signo y la cifra; se contrasta con valor_fuente POSITIVO (se espera «signo_distinto» o pendiente)")
n = 0
for nombre, ch in INV:
    for forma, pagina in (("menos", f"Resultado -{ch}849,7\n"), ("paréntesis", f"Resultado ({ch}849,7)\n")):
        a, b = VP._cita_cifra("849,7", 849.7, pagina)[0], VE._cita_cifra("849,7", 849.7, pagina)[0]
        n += b == "ok"
        print(f"   {nombre:38} {forma:11} página={pagina!r:32} anterior: {a:18} cuarta: {b}" + ("   <<< se lee en POSITIVO" if b == "ok" else ""))
print(f"{n} lecturas en positivo de una cifra publicada en negativo")

# B · ¿hay caracteres invisibles o de control en los textos conservados REALES (los que citan los siete registros de la 4.14)?
import collections, glob, re, unicodedata  # noqa: E402
from comun3 import PV  # noqa: E402
E14 = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_14")
textos = sorted(set(os.path.realpath(p) for p in glob.glob(os.path.join(E14, "*", "*", "texto", "*.txt"))))
cuenta, pegados, n_car = collections.Counter(), [], 0
for p in textos:
    t = open(p, encoding="utf-8", errors="replace").read()
    n_car += len(t)
    for ch in set(t):
        if unicodedata.category(ch) in ("Cf", "Cc") and ch not in "\n\r\t\f":
            cuenta[f"U+{ord(ch):04X} ({unicodedata.category(ch)})"] += t.count(ch)
    for m in re.finditer(r"[-‐‑‒–—−(][^\S\n]?[­​-‏⁠-⁤﻿\x00-\x08\x0b\x0e-\x1f\x7f-\x9f]+[^\S\n]?\d", t):
        pegados.append((os.path.basename(p)[:40], t[max(0, m.start() - 20):m.end() + 10]))
print(f"\n== B · textos conservados reales: {len(textos)} archivos distintos, {n_car} caracteres")
print("   caracteres de formato (Cf) o de control (Cc, salvo saltos, tabuladores y salto de página):", dict(cuenta) or "ninguno")
print(f"   apariciones de signo o paréntesis + carácter invisible + cifra: {len(pegados)}", pegados[:5])
