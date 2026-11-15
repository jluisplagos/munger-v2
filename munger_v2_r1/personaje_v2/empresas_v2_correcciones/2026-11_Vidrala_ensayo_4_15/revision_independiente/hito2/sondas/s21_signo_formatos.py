#!/usr/bin/env python3
"""s21 · R415-SIGNO: tabla sistemática. Para cada forma de imprimir un número con signo conocido (26 formas × 4 escrituras del número
× 3 contextos), lo que dice _cita_cifra con el valor_fuente verdadero y con el de signo contrario. Página = cita (espacios originales).
  «bien» = acepta el verdadero y rechaza el contrario · «rechazo falso» = no acepta el verdadero · «ACEPTA EL CONTRARIO» = acepta el signo que no se publica."""
import collections, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import VE

NUM = {"1,234.5": 1234.5, "1.234,5": 1234.5, "1 234,5": 1234.5, "1234.5": 1234.5}
FORMAS = [  # (nombre, plantilla con {n}, signo verdadero)
    ("sin marca", "{n}", 1), ("+n", "+{n}", 1), ("n €", "{n} €", 1), ("€n", "€{n}", 1), ("EUR n", "EUR {n}", 1), ("n %", "{n} %", 1), ("n%", "{n}%", 1),
    ("-n", "-{n}", -1), ("−n (U+2212)", "−{n}", -1), ("–n (U+2013)", "–{n}", -1), ("(n)", "({n})", -1), ("( n )", "( {n} )", -1), ("(n €)", "({n} €)", -1), ("(€n)", "(€{n})", -1),
    ("-€n", "-€{n}", -1), ("€-n", "€-{n}", -1), ("-n €", "-{n} €", -1), ("(n)%", "({n})%", -1), ("(n%)", "({n}%)", -1), ("(n %)", "({n} %)", -1), ("−n %", "−{n} %", -1),
    ("− n (un espacio)", "− {n}", -1), ("(n m)", "({n} m)", -1), ("(EUR n)", "(EUR {n})", -1), ("n- (final)", "{n}-", -1), ("-     n (contabilidad, menos a la izquierda)", "-     {n}", -1),
    ("−     n (contabilidad, U+2212)", "−     {n}", -1), ("-€    n (contabilidad)", "-€    {n}", -1),
]
CONTEXTOS = {"rótulo + cifra": "Partida de ejemplo  {x}", "tras otra cifra": "Partida de ejemplo  987.6   {x}", "antes de otra cifra": "Partida de ejemplo  {x}   987.6"}
res = collections.defaultdict(collections.Counter)
for nombre, plantilla, signo in FORMAS:
    for ntxt, nval in NUM.items():
        for cn, ctx in CONTEXTOS.items():
            cita = ctx.format(x=plantilla.format(n=ntxt))
            v = signo * nval
            a = VE._cita_cifra(cita, v, cita)[0]
            b = VE._cita_cifra(cita, -v, cita)[0]
            if b == "ok":
                res[nombre]["ACEPTA EL CONTRARIO"] += 1
            elif a == "ok":
                res[nombre]["bien"] += 1
            else:
                res[nombre][f"rechazo falso ({'pendiente' if a == 'signo_indeterminado' else 'discrepancia'})"] += 1
print(f"{'forma':48} {'signo':>5}   resultado en 12 combinaciones (4 escrituras × 3 contextos)")
for nombre, plantilla, signo in FORMAS:
    print(f"{nombre:48} {'+' if signo > 0 else '−':>5}   {dict(res[nombre])}")
tot = collections.Counter()
for c in res.values():
    tot.update(c)
print("\ntotal:", dict(tot))
