#!/usr/bin/env python3
"""g6 · séptima comprobación · las propuestas del revisor (propuestas7.py; NO es código entregado), a nivel de unidad.
El bloque de pruebas CON los cuatro casos de la cita completa y los dos controles (fix7t) se ejecuta contra:
 (a) la candidata 45ff57c → la prueba «(V3, V7)» tiene que FALLAR (es la demostración de X1 dentro de la batería);
 (b) 8196522 y la propuesta de la sexta (prop6);
 (c) la candidata con la corrección de la línea :542 (fix7) → tiene que pasar entero;
 (d) cada mutación sobre el código CORREGIDO (fix7): las de mutantes7.py que no tocan la línea :542, tal cual, y las seis de esa línea
     reescritas sobre la línea corregida. ¿Queda alguna sin detectar?
Uso: python3 -I -B g6_propuestas7_unidad.py"""
import os, sys, time, types
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun7 import VE, VP, VQ, F, ACT, ANT, PROP, cargar  # noqa: E402
import mutantes7 as MU  # noqa: E402
P7 = os.path.join(F, "fix7", "munger_v2_r1", "personaje_v2")
VF7 = cargar(os.path.join(P7, "scripts", "verificacion_entradas.py"), "verificacion_entradas_fix7")
SRC7 = open(VF7.__file__, encoding="utf-8").read()
assert """(?<![\\d.,])(?<!\\d['’])" + re.escape(c)""" in SRC7 and "(hito 2, W5)" in SRC7  # la candidata con la línea :542 corregida
T = open(os.path.join(F, "fix7t", "munger_v2_r1", "personaje_v2", "pruebas", "test_verificacion_entradas_415.py"), encoding="utf-8").read()
assert T == open(os.path.join(P7, "pruebas", "test_verificacion_entradas_415.py"), encoding="utf-8").read()  # fix7 y fix7t llevan las mismas pruebas
ini = T.index("# (hito 2, quinta comprobación, V1–V7 y pruebas de V4)")
fin = T.index("r = con()\npaso(\"RW\", \"el control positivo sigue apto después de los casos RW\"", ini)
BLOQUE = T[ini:fin]
print(f"bloque de pruebas propuesto (fix7t): {len(BLOQUE.splitlines())} líneas, {BLOQUE.count('paso(')} pruebas")


def bloque(mod):
    res = []
    exec(compile(BLOQUE, "bloque_propuesto7", "exec"), {"VE": mod, "paso": lambda b, n, ok, det=None: res.append((n, bool(ok), det)), "_time": time})
    return res


def desde_texto(s, nombre):
    m = types.ModuleType(nombre)
    m.__file__ = VF7.__file__
    ruta = list(sys.path)
    exec(compile(s, nombre + ".py", "exec"), m.__dict__)
    sys.path[:] = ruta
    return m


for etiqueta, mod, debe in ((f"(a) candidata {ACT}", VE, "FALLAR en «(V3, V7)»"), (f"(b) {ANT}", VP, "fallar (no tiene W3)"), (f"(b) {PROP}", VQ, "pasar"),
                            ("(c) candidata con la corrección de :542 (fix7)", VF7, "pasar")):
    r = bloque(mod)
    print(f"\n== {etiqueta}: {sum(ok for _n, ok, _d in r)} de {len(r)} pasan (debe {debe})")
    for n, ok, d in r:
        if not ok:
            print(f"   FALLA {n[:70]} · {str(d)[:330]}")

print("\n== (d) mutaciones sobre el código corregido (fix7)")
L7 = next(l for l in SRC7.split("\n") if "re.escape(c)" in l and "for m in re.finditer" in l)
INI7, FIN7 = r"""(?<![\d.,])(?<!\d['’])" + re.escape(c)""", r"""(?!\d|[.,'’]\d)", t)"""
assert L7.count(INI7) == 1 and L7.count(FIN7) == 1
LINEA = {
    "L1_inicio_sin_apostrofos (= x1a)": L7.replace(INI7, r"""(?<![\d.,])" + re.escape(c)"""),
    "L2_inicio_solo_ascii (= 8196522, x1b)": L7.replace(INI7, r"""(?<![\d.,])(?<!\d')" + re.escape(c)"""),
    "L3_inicio_solo_tipografico (= la candidata 45ff57c)": L7.replace(INI7, r"""(?<![\d.,])(?<!\d[’])" + re.escape(c)"""),
    "L4_final_sin_apostrofos (= v7c)": L7.replace(FIN7, r"""(?!\d|[.,]\d)", t)"""),
    "L5_final_solo_ascii (= w3b)": L7.replace(FIN7, r"""(?!\d|[.,']\d)", t)"""),
    "L6_final_solo_tipografico (= w3c)": L7.replace(FIN7, r"""(?!\d|[.,’]\d)", t)"""),
}
sin = []
for nombre, linea in LINEA.items():
    assert linea != L7 and SRC7.count(L7) == 1
    r = bloque(desde_texto(SRC7.replace(L7, linea), "m_" + nombre[:2]))
    fallan = [(n, d) for n, ok, d in r if not ok]
    print(f"   {nombre:52} {'DETECTADA' if fallan else '<<< NO detectada'}" + (f" · {str(fallan[0][1])[:150]}" if fallan else ""))
    if not fallan:
        sin.append(nombre)
for nombre, (grupo, hall, desc, cambios, bats) in MU.M.items():
    if grupo == "control" or any(a != MU.VEP for a, _v, _n in cambios) or any(v == MU.LECT for _a, v, _n in cambios):
        continue
    s = SRC7
    for _a, viejo, nuevo in cambios:
        assert s.count(viejo) == 1, (nombre, s.count(viejo))
        s = s.replace(viejo, nuevo)
    r = bloque(desde_texto(s, "m_" + nombre))
    fallan = [(n, d) for n, ok, d in r if not ok]
    print(f"   {nombre:52} {'DETECTADA' if fallan else '<<< NO detectada'}" + (f" · {str(fallan[0][1])[:150]}" if fallan else ""))
    if not fallan:
        sin.append(nombre)
print(f"\n   sin detectar con las pruebas propuestas y el código corregido: {sin}")
