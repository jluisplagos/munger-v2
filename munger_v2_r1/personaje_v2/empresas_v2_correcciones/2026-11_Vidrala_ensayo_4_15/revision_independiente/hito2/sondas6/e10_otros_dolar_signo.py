#!/usr/bin/env python3
"""e10 · sexta comprobación · los «$» de _signo_en_cita que el diff NO cambia (:466 la moneda delante de la cifra, :469 y :471 el paréntesis,
:478 el guion, :490 lo que precede al guion) y el salto de línea: ¿queda alguna lectura a través de un salto de línea?
A) casos a nivel de unidad con 876bfc2 y 8196522 (la cita abarca las dos líneas);
B) textos reales: cuántas veces una línea acaba en un guion (con o sin moneda detrás) y la siguiente empieza por una cifra.
Uso: python3 -I -B e10_otros_dolar_signo.py"""
import collections, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun6 import VE, VP, ACT, ANT, PV  # noqa: E402
print(f"VE = {ACT} · VP = {ANT}")
print("== A · unidad")
for nombre, pag, cita, vf in (
        ("A1 la moneda al final de la línea anterior, sin guion: «Total €⏎849,7»", "Total €\n849,7", "Total € 849,7", 849.7),
        ("A2 guion y moneda al final de la línea anterior: «Total -€⏎849,7» (valor +)", "Total -€\n849,7", "Total -€ 849,7", 849.7),
        ("A3 lo mismo con el valor en negativo", "Total -€\n849,7", "Total -€ 849,7", -849.7),
        ("A4 guion, moneda y espacio al final de la línea: «Total -€ ⏎849,7» (valor +)", "Total -€ \n849,7", "Total -€ 849,7", 849.7),
        ("A5 guion solo al final de la línea anterior: «Total -⏎849,7» (valor +)", "Total -\n849,7", "Total - 849,7", 849.7),
        ("A6 año, guion y moneda al final de la línea y un año al principio de la siguiente: «Saldo 2023-€⏎2024» (valor +)", "Saldo 2023-€\n2024", "Saldo 2023-€ 2024", 2024),
        ("A7 lo mismo en una línea: «Saldo 2023-€2024» (valor +)", "Saldo 2023-€2024", "Saldo 2023-€2024", 2024),
        ("A8 intervalo partido tras el guion: «Periodo 2023-⏎2024» (valor +)", "Periodo 2023-\n2024", "Periodo 2023- 2024", 2024),
        ("A9 paréntesis abierto al final de la línea anterior: «Resultado (⏎849,7)» (valor −)", "Resultado (\n849,7)", "Resultado ( 849,7)", -849.7),
        ("A10 guion al final de la línea y paréntesis en la siguiente: «Total -⏎(849,7)» (valor −)", "Total -\n(849,7)", "Total - (849,7)", -849.7),
        ("A11 guion pegado a la moneda tras un salto: «31-12⏎-€1900» (valor +)", "Cierre 31-12\n-€1900", "Cierre 31-12 -€1900", 1900),
        ("A12 guion pegado a la moneda tras un salto: «2023⏎-EUR 2024» (valor +)", "Ejercicio 2023\n-EUR 2024", "Ejercicio 2023 -EUR 2024", 2024)):
    a, b = VP._cita_cifra(cita, vf, pag)[0], VE._cita_cifra(cita, vf, pag)[0]
    print(f"   {nombre}\n      876bfc2: {a:20} 8196522: {b}")
print("== B · textos reales (los 73 textos conservados citados)")
E14 = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_14")
textos = set()
for exp in ["vidrala_decisiones_INVALIDO_perdio_analisis/Vidrala", "elis_decisiones/Elis", "viscofan/Viscofan", "elis_motor_A/Elis", "vidrala_decisiones/Vidrala", "vidrala/Vidrala", "viscofan_decisiones/Viscofan"]:
    c = os.path.join(E14, exp)
    reg, err = VE.cargar(c)
    for e in reg["entradas"]:
        f = e.get("fuente") if isinstance(e.get("fuente"), dict) else {}
        if f.get("archivo") and str(f["archivo"]).lower().endswith(".txt"):
            r = VE._ruta_fuente(c, f["archivo"])
            if r:
                textos.add(os.path.realpath(r))
GUI = "-‐‑‒–—−"
MON = r"(?:[€$£¥]|\b(?:EUR|USD|GBP|CHF|JPY|DKK|SEK|NOK|BRL)\b)"
RX = {"línea que acaba en «guion + moneda» y la siguiente empieza por una cifra": re.compile(r"[" + GUI + r"]" + MON + r"\s?\n\d", re.I),
      "línea que acaba en «año + guion + moneda» y la siguiente empieza por un año": re.compile(r"\d{4}[" + GUI + r"]" + MON + r"\s?\n\d{4}(?!\d)", re.I),
      "línea que acaba en una moneda (sin guion) y la siguiente empieza por una cifra": re.compile(MON + r"\s?\n\d", re.I)}
tot = collections.Counter()
for p in sorted(textos):
    t = open(p, encoding="utf-8", errors="replace").read()
    for k, rx in RX.items():
        tot[k] += len(rx.findall(t))
print(f"   {len(textos)} textos: {dict(tot)}")
