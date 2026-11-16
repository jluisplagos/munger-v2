#!/usr/bin/env python3
"""x5d · octava comprobación · la prueba NUEVA de X5 (el bloque «x5 = {…}» … «paso("C", "(séptima comprobación, X5) …")» de
pruebas/test_entrada_efectiva_415.py del árbol), ejecutada tal cual a nivel de unidad contra: el código del árbol (tiene que pasar),
el de 45ff57c (tiene que fallar) y cada mutación de mutantes8.py aplicada al código del árbol.
Uso: python3 -I -B x5d_prueba_x5_mutaciones_unidad.py"""
import os, sys, types
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun8 import FN, FO, P_FN, PV  # noqa: E402
from mutantes8 import LINEA, MUT  # noqa: E402

T = open(os.path.join(PV, "pruebas", "test_entrada_efectiva_415.py"), encoding="utf-8").read()
ini = T.index("x5 = {(")
fin = T.index("\n", T.index('paso("C", "(séptima comprobación, X5)', ini)) + 1
BLOQUE = T[ini:fin]
print("bloque de la prueba (del árbol):")
for l in BLOQUE.rstrip("\n").split("\n"):
    print("   | " + l[:200])
S = open(P_FN, encoding="utf-8").read()
assert S.count(LINEA) == 1, "la línea del return no es la esperada"


def bloque(mod):
    res = []
    exec(compile(BLOQUE, "bloque_x5", "exec"), {"FH": mod, "paso": lambda g, n, ok, det=None: res.append((n, bool(ok), det))})
    assert len(res) == 1
    return res[0]


def mutado(linea):
    m = types.ModuleType("fase1_mut")
    m.__file__ = P_FN
    exec(compile(S.replace(LINEA, linea), "fase1_mut.py", "exec"), m.__dict__)
    return m


ok_todo = True
n, ok, det = bloque(FN)
print(f"\ncódigo del árbol (0a0020b): {'PASA' if ok else 'FALLA'} {det if det else ''}")
ok_todo &= ok
n, ok, det = bloque(FO)
print(f"código de 45ff57c:          {'PASA  <<< la prueba no vería X5' if ok else 'FALLA'} {det if det else ''}")
ok_todo &= not ok
print("\nmutaciones sobre el código del árbol:")
no_det_acepta = []
for nombre, (linea, sentido, que) in MUT.items():
    n, ok, det = bloque(mutado(linea))
    print(f"   {nombre:34} [{sentido:8}] {'NO detectada' if ok else 'detectada   '} · {que}" + (f"\n{'':52}→ {det}" if not ok else ""))
    if ok and sentido == "acepta":
        no_det_acepta.append(nombre)
print(f"\nno detectadas en el sentido de aceptar: {no_det_acepta or 'ninguna'}")
# ¿cambian de verdad el comportamiento las no detectadas? un caso que las distingue
DIST = {"m9_detras_un_solo_separador": [("7", "Total 7,,6"), ("7", "Total 7.'6"), ("849", "Total 849''697")],
        "s1_delante_apostrofo_sin_cifra": [("1,5", "taux d’1,5 %"), ("849", "'849")],
        "s2_detras_apostrofo_sin_cifra": [("120", "SBF 120’s"), ("849", "849' 697")],
        "s3_apostrofo_en_cualquier_sitio": [("849,7", "849,7 l’exercice")]}
for nombre, casos in DIST.items():
    m = mutado(MUT[nombre][0])
    print(f"   {nombre}: " + " · ".join(f"{i!r} en {t!r}: árbol={FN.importe_completo(i, t)}, mutación={m.importe_completo(i, t)}" for i, t in casos))
print("\nRESULTADO:", "CONFORME" if ok_todo and not [x for x in no_det_acepta if x != "m9_detras_un_solo_separador"] else "NO CONFORME")
