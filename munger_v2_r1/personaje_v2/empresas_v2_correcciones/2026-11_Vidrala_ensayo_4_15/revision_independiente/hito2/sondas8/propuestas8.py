#!/usr/bin/env python3
"""Propuesta OPCIONAL del revisor de la OCTAVA comprobación (Y3; sentido prudente; NO hace falta para cerrar). NO es código entregado ni revisado.
  fix8t · SOLO PRUEBAS: dos controles más en el diccionario «x5» de pruebas/test_entrada_efectiva_415.py, para que una corrección futura no
          se pase de estricta: un apóstrofo que no está entre dos cifras no bloquea («120’s» con impreso 120; «d’1,5» con impreso 1,5).
Escribe el árbol ligero fable/fix8t (código de 0a0020b + la prueba cambiada), el diff en salidas8/ y evalúa el bloque a nivel de unidad
contra el código del árbol y contra las mutaciones de mutantes8.py.   Uso: python3 -I -B propuestas8.py"""
import os, shutil, subprocess, sys, types
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun8 import FN, FO, P_FN, CONGELADO  # noqa: E402
from mutantes8 import LINEA, MUT  # noqa: E402
F = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COPIA = os.path.join(F, "copia", "munger_v2_r1")
TEE = "pruebas/test_entrada_efectiva_415.py"
VIEJO = '''      ("849'697", "Total 849'697"): True, ("849,7", "Ventas SBF 120\\u2019s 849,7"): True}'''
NUEVO = '''      ("849'697", "Total 849'697"): True, ("849,7", "Ventas SBF 120\\u2019s 849,7"): True,
      # (octava, propuesta del revisor, Y3) un apóstrofo que no está entre dos cifras no bloquea: posesivo tras la cifra y elisión antes de ella
      ("120", "Ventas SBF 120\\u2019s 849,7"): True, ("1,5", "taux d\\u20191,5 %"): True}'''
base = os.path.join(F, "fix8t")
if os.path.lexists(base):
    shutil.rmtree(base)
dst = os.path.join(base, "munger_v2_r1")
os.makedirs(os.path.join(dst, "personaje_v2"))
for x in os.listdir(CONGELADO):
    if x != "personaje_v2":
        os.symlink(os.path.join(CONGELADO, x), os.path.join(dst, x))
for x in os.listdir(os.path.join(CONGELADO, "personaje_v2")):
    n = os.path.join(dst, "personaje_v2", x)
    if x in ("scripts", "esquema", "pruebas"):
        shutil.copytree(os.path.join(CONGELADO, "personaje_v2", x), n, ignore=shutil.ignore_patterns("__pycache__"), symlinks=True)
    elif x != ".lo_perfil":
        os.symlink(os.path.join(CONGELADO, "personaje_v2", x), n)
p = os.path.join(dst, "personaje_v2", TEE)
s = open(p, encoding="utf-8").read()
assert s.count(VIEJO) == 1
open(p, "w", encoding="utf-8").write(s.replace(VIEJO, NUEVO))
d = subprocess.run(["diff", "-u", os.path.join(CONGELADO, "personaje_v2", TEE), p, "--label", "a/munger_v2_r1/personaje_v2/" + TEE, "--label", "b/munger_v2_r1/personaje_v2/" + TEE],
                   capture_output=True, text=True).stdout
open(os.path.join(F, "salidas8", "propuestas8_fix8t.diff"), "w", encoding="utf-8").write(d)
print(d)
T = open(p, encoding="utf-8").read()
ini = T.index("x5 = {(")
fin = T.index("\n", T.index('paso("C", "(séptima comprobación, X5)', ini)) + 1
BLOQUE = T[ini:fin]
S = open(P_FN, encoding="utf-8").read()


def bloque(mod):
    res = []
    exec(compile(BLOQUE, "bloque_x5_propuesto", "exec"), {"FH": mod, "paso": lambda g, n, ok, det=None: res.append((n, bool(ok), det))})
    return res[0]


def mutado(linea):
    m = types.ModuleType("fase1_mut")
    m.__file__ = P_FN
    exec(compile(S.replace(LINEA, linea), "fase1_mut.py", "exec"), m.__dict__)
    return m


print("bloque propuesto, a nivel de unidad:")
print("   código del árbol (0a0020b):", "PASA" if bloque(FN)[1] else f"FALLA {bloque(FN)[2]}")
print("   código de 45ff57c:         ", "PASA (mal)" if bloque(FO)[1] else "FALLA (como debe)")
for nombre, (linea, sentido, que) in MUT.items():
    n, ok, det = bloque(mutado(linea))
    print(f"   {nombre:34} [{sentido:8}] {'NO detectada' if ok else 'detectada   '}" + (f" → {det}" if not ok else ""))
