#!/usr/bin/env python3
"""s5 · U2: ¿_importe_libro_exacto es una tolerancia general encubierta? Comparación diferencial con la regla del hito 1 (_igual_libro
sobre el float del exacto) y con la definición «el libro es un redondeo a 3 decimales del exacto (cualquier regla de empate) o es el exacto».
A) fronteras; B) barrido aleatorio (200.000 pares) y recuento de lo que cambia entre el hito 1 y el hito 2; C) en el registro: dato
publicado y derivado con importes, ceros y empates."""
import os, sys, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import VE
from fractions import Fraction as Fr
import decimal

D = decimal.Decimal


def redondeos(ex):
    """Los redondeos a 3 decimales del exacto con todas las reglas de empate (mitad arriba, abajo, par, lejos de cero, hacia cero)."""
    d = D(ex.numerator) / D(ex.denominator) if ex.denominator in (1, 10, 100, 1000, 10 ** 4, 10 ** 5, 10 ** 6, 10 ** 7) else None
    out = set()
    q = ex * 1000
    piso = q.numerator // q.denominator
    resto = q - piso
    if resto == 0:
        out.add(Fr(piso, 1000))
    elif resto < Fr(1, 2):
        out.add(Fr(piso, 1000))
    elif resto > Fr(1, 2):
        out.add(Fr(piso + 1, 1000))
    else:
        out |= {Fr(piso, 1000), Fr(piso + 1, 1000)}
    return out


print("== A · fronteras")
for ex, vm in [(Fr("849.6975"), 849.697), (Fr("849.6975"), 849.698), (Fr("849.69750001"), 849.697), (Fr("849.69749999"), 849.698), (Fr("849.6965"), 849.697),
               (Fr("849.69649999"), 849.697), (Fr("0.0005"), 0.0), (Fr("0.0005"), 0), (Fr("0.00050001"), 0.0), (Fr("-0.0005"), 0.0), (Fr("0.0004"), 0.001),
               (Fr("849.697"), 849.6970000000001), (Fr("849.6970000000001"), 849.697), (Fr(1, 3), 0.333), (Fr(1, 3), 0.3333), (Fr(2, 3), 0.667), (Fr(2, 3), 0.666),
               (Fr("1e15") + Fr("0.0004"), 1e15), (Fr("849.6974"), 849.6972), (Fr("849.0"), 849.697), (Fr("849"), 849), (Fr("849.0004"), 849), (Fr("848.9996"), 849),
               (Fr("0.2511"), 0.25), (Fr("0.2504"), 0.25), (Fr("0.2496"), 0.25), (Fr("-849.6975"), -849.697), (Fr("-849.6975"), -849.698), (Fr("849.6975"), -849.698)]:
    print(f"   exacto={str(ex):>22} libro={vm!r:<22} -> {VE._importe_libro_exacto(ex, vm)}   (hito 1, _igual_libro sobre float: {VE._igual_libro(float(ex), vm)})")

print("\n== B · barrido aleatorio")
rnd = random.Random(20261115)
n = 0
nuevo_acepta, nuevo_rechaza, fuera_def = [], [], []
for _ in range(200000):
    tipo = rnd.random()
    base = Fr(rnd.randint(-2 * 10 ** 6, 2 * 10 ** 6), 1000)  # libro a 3 decimales
    if tipo < 0.25:
        ex = base + Fr(rnd.choice([-1, 1]), 2000)  # empate exacto
    elif tipo < 0.5:
        ex = base + Fr(rnd.randint(-12, 12), 20000)  # cerca del medio milésimo
    elif tipo < 0.75:
        ex = base + Fr(rnd.randint(-10 ** 6, 10 ** 6), 10 ** 9)  # ruido pequeño
    else:
        ex = Fr(rnd.randint(-10 ** 9, 10 ** 9), rnd.randint(1, 10 ** 4))
        base = Fr(round(float(ex), 3)).limit_denominator(1000)
    vm = float(base)
    h2 = VE._importe_libro_exacto(ex, vm)
    h1 = VE._igual_libro(float(ex), vm)
    defin = (Fr(repr(vm)) == ex) or (Fr(repr(vm)) in redondeos(ex))
    n += 1
    if h2 and not h1:
        nuevo_acepta.append((ex, vm))
    if h1 and not h2:
        nuevo_rechaza.append((ex, vm))
    if h2 != defin:
        fuera_def.append((ex, vm, h2, defin))
print(f"   pares: {n}")
print(f"   hito 2 acepta y hito 1 rechazaba: {len(nuevo_acepta)}; de ellos, empates exactos (|exacto − libro| = 0,0005): {sum(abs(e - Fr(repr(v))) == Fr(1, 2000) for e, v in nuevo_acepta)}; "
      f"máxima distancia: {float(max((abs(e - Fr(repr(v))) for e, v in nuevo_acepta), default=0))!r}")
print(f"   hito 1 aceptaba y hito 2 rechaza: {len(nuevo_rechaza)}; ejemplos: {[(str(e), v) for e, v in nuevo_rechaza[:3]]}")
print(f"   hito 2 distinto de la definición «exacto o redondeo a 3 decimales con cualquier regla de empate»: {len(fuera_def)}; ejemplos: {[(str(e), v, a, b) for e, v, a, b in fuera_def[:3]]}")
