#!/usr/bin/env python3
"""e5 · sexta comprobación · ¿detectan las pruebas NUEVAS lo que dicen? Evaluación A NIVEL DE UNIDAD (rápida; la batería entera, en
mutaciones6.py): se extrae de test_verificacion_entradas_415.py el bloque de las pruebas nuevas (son llamadas puras a VE) y se ejecuta
tal cual contra (a) la candidata 8196522, (b) el código de 876bfc2 (sin NINGUNA de las correcciones) y (c) cada mutación de mutantes6.py
cargada en memoria. Para T6 (pipeline.py) se repite el bucle de las «erratas dobles» de test_entrada_efectiva_415.py.
Una prueba «detecta» una mutación si pasa con la candidata y FALLA con el código mutado.
Uso: python3 -I -B e5_pruebas_nuevas_unidad.py"""
import importlib.util, json, os, shutil, sys, tempfile, time, types
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun6 import VE, VP, F, PV, ACT, ANT  # noqa: E402
import mutantes6 as MU  # noqa: E402

T415 = open(os.path.join(PV, "pruebas", "test_verificacion_entradas_415.py"), encoding="utf-8").read()
ini = T415.index("# (hito 2, quinta comprobación, V1–V7 y pruebas de V4)")
fin = T415.index("r = con()\npaso(\"RW\", \"el control positivo sigue apto después de los casos RW\"", ini)
BLOQUE = T415[ini:fin]
print(f"bloque de pruebas nuevas: {len(BLOQUE.splitlines())} líneas, {BLOQUE.count('paso(')} pruebas")


def cargar_texto(src, nombre):
    """Carga un módulo desde su texto (el código mutado no se escribe en ningún árbol)."""
    m = types.ModuleType(nombre)
    m.__file__ = VE.__file__
    ruta = list(sys.path)
    exec(compile(src, nombre + ".py", "exec"), m.__dict__)
    sys.path[:] = ruta
    return m


def ejecutar_bloque(mod):
    res = []

    def paso(bloque, nombre, ok, det=None):
        res.append((nombre, bool(ok), det))
    exec(compile(BLOQUE, "bloque_pruebas_nuevas", "exec"), {"VE": mod, "paso": paso, "_time": time})
    return res


SRC_VE = open(VE.__file__, encoding="utf-8").read()
base = ejecutar_bloque(VE)
print(f"\n== (a) candidata {ACT}: " + ", ".join(f"{'PASA' if ok else 'FALLA'}" for _n, ok, _d in base))
for n, ok, d in base:
    print(f"   {'PASA ' if ok else 'FALLA'} {n[:150]}" + (f" · {d}" if d else ""))
prev = ejecutar_bloque(VP)
print(f"\n== (b) con el código de {ANT} (ninguna corrección de esta candidata): ¿qué pruebas nuevas FALLAN?")
for n, ok, d in prev:
    print(f"   {'pasa TAMBIÉN sin las correcciones' if ok else 'FALLA (detecta)':34} {n[:130]}" + (f" · {str(d)[:160]}" if d else ""))

print("\n== (c) mutaciones de verificacion_entradas.py, una cada vez")
res_mut = {}
for nombre, (grupo, hall, desc, cambios, bats) in MU.M.items():
    if any(a != MU.VEP for a, _v, _n in cambios) or grupo == "control":
        continue
    s = SRC_VE
    for _a, viejo, nuevo in cambios:
        assert s.count(viejo) == 1 and viejo != nuevo, (nombre, s.count(viejo))
        s = s.replace(viejo, nuevo)
    r = ejecutar_bloque(cargar_texto(s, "ve_mut_" + nombre))
    fallan = [(n, d) for n, ok, d in r if not ok]
    res_mut[nombre] = fallan
    print(f"   {nombre:34} {hall:3} {'DETECTADA por ' + str(len(fallan)) + ' prueba(s) nueva(s)' if fallan else 'NO detectada por las pruebas nuevas'}")
    print(f"      {desc}")
    for n, d in fallan:
        print(f"      FALLA: {n[:110]} · {str(d)[:170]}")

print("\n== (d) T6 (pipeline.py): el bucle de las «erratas dobles» de test_entrada_efectiva_415.py, con el código y con las mutaciones")
SRC_PL = open(os.path.join(PV, "scripts", "pipeline.py"), encoding="utf-8").read()
tmp = tempfile.mkdtemp(prefix="e5_", dir=os.path.join(F, "tmp"))
ERRATAS = ("entrdaefectivaa", "Entrada_Efectiv", "entrada_efectvia", "emtrada_efectiba", "ehtrada_efectiwa")
ERRATAS_ANTES = ERRATAS[:3]


def erratas(PL):
    out = {}
    for e in ERRATAS:
        json.dump({"tipo": "x", e: "estricta"}, open(os.path.join(tmp, "alcance_v2.json"), "w"))
        try:
            out[e] = "sin error: " + repr(PL.modo_entrada_efectiva(tmp))
        except SystemExit as ex:
            out[e] = "ERROR (SystemExit)"
        except Exception as ex:  # noqa: BLE001
            out[e] = "ERROR (" + type(ex).__name__ + ")"
    return out


import difflib, re
for e in ERRATAS:
    k = re.sub(r"[^a-z]", "", e.lower())
    print(f"   «{e}»: proporción de parecido {difflib.SequenceMatcher(None, k, 'entradaefectiva').ratio():.3f}")
try:
    for nombre in ("(candidata)", "t6a_sin_distancia_de_edicion", "t6b_distancia_1", "t6c_distancia_2"):
        s = SRC_PL
        if nombre in MU.M:
            for _a, viejo, nuevo in MU.M[nombre][3]:
                assert s.count(viejo) == 1, nombre
                s = s.replace(viejo, nuevo)
        PL = cargar_texto(s, "pl_" + re.sub(r"\W", "_", nombre))
        r = erratas(PL)
        sin_error = [e for e, v in r.items() if not v.startswith("ERROR")]
        sin_error_antes = [e for e in sin_error if e in ERRATAS_ANTES]
        print(f"   {nombre:32} " + ("todas dan error (la prueba PASA)" if not sin_error else f"SIN error: {sin_error} → la prueba nueva FALLA (detecta)")
              + ("" if nombre == "(candidata)" else f" · con las tres claves de la quinta: {'detectaría' if sin_error_antes else 'no detectaba'}"))
finally:
    shutil.rmtree(tmp, ignore_errors=True)
