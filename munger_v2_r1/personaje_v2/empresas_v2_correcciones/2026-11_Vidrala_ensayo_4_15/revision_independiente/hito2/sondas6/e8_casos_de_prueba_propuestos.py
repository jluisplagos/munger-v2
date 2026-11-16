#!/usr/bin/env python3
"""e8 · sexta comprobación · casos de prueba PROPUESTOS por el revisor para las mutaciones que las pruebas nuevas no detectan (e5 y
mutaciones6). No es código entregado: se evalúa cada caso, a nivel de unidad, contra la candidata (tiene que dar lo esperado) y contra
cada mutación que hoy sobrevive (tiene que dar OTRA cosa: entonces el caso la detectaría).
Uso: python3 -I -B e8_casos_de_prueba_propuestos.py"""
import json, os, re, shutil, sys, tempfile, time, types
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun6 import VE, F, PV, ACT  # noqa: E402
import mutantes6 as MU  # noqa: E402
SRC_VE = open(VE.__file__, encoding="utf-8").read()
SRC_PL = open(os.path.join(PV, "scripts", "pipeline.py"), encoding="utf-8").read()


def mutante(nombre, src):
    s = src
    for _a, viejo, nuevo in MU.M[nombre][3]:
        assert s.count(viejo) == 1, nombre
        s = s.replace(viejo, nuevo)
    m = types.ModuleType("mut_" + nombre)
    m.__file__ = VE.__file__
    ruta = list(sys.path)
    exec(compile(s, nombre + ".py", "exec"), m.__dict__)
    sys.path[:] = ruta
    return m


# (mutación que hoy sobrevive, descripción del caso propuesto, función que devuelve el resultado, valor esperado con la candidata)
CASOS = [
    ("v2a_anio_anterior_con_dolar", "V2 · _cita_cifra('Ejercicio 2023 -2024', 2024, 'Ejercicio 2023\\n-2024') == 'signo_distinto' (la cita abarca las dos líneas)",
     lambda M: M._cita_cifra("Ejercicio 2023 -2024", 2024, "Ejercicio 2023\n-2024")[0], "signo_distinto"),
    ("v2b_fecha_con_dolar", "V2 · _cita_cifra('Cierre 31-12 -2024', 2024, 'Cierre 31-12\\n-2024') == 'signo_distinto'",
     lambda M: M._cita_cifra("Cierre 31-12 -2024", 2024, "Cierre 31-12\n-2024")[0], "signo_distinto"),
    ("v2c_los_dos_con_dolar", "V2 · los dos casos anteriores",
     lambda M: (M._cita_cifra("Ejercicio 2023 -2024", 2024, "Ejercicio 2023\n-2024")[0], M._cita_cifra("Cierre 31-12 -2024", 2024, "Cierre 31-12\n-2024")[0]), ("signo_distinto", "signo_distinto")),
    ("v5a_sin_corte", "V5 · len(_apariciones_en_pagina('Total: 5.5', 1000 apariciones en una línea)) == MAX_APARICIONES_CITA + 1 (estructura, no reloj)",
     lambda M: len(M._apariciones_en_pagina("Total: 5.5", " ".join(["Total: 5.5"] * 1000))), VE.MAX_APARICIONES_CITA + 1),
    ("v7c_lectura_sin_apostrofo_detras", "V7 · _cita_cifra('Total 849', 849, \"Total 849'697\") == 'ausente'",
     lambda M: M._cita_cifra("Total 849", 849, "Total 849'697")[0], "ausente"),
    ("v7d_real_solo_plural", "V7 · _unidad_monetaria_no_reconocida('miles de real') is True",
     lambda M: M._unidad_monetaria_no_reconocida("miles de real"), True),
    ("v7a_en_numero_sin_apostrofo", "V7 · _cita_cifra('849,7 mill', 849.7, \"Total 1'849,7 millones\") == 'ausente' (doble corte)",
     lambda M: M._cita_cifra("849,7 mill", 849.7, "Total 1'849,7 millones")[0], "ausente"),
    ("v3b_en_numero_con_dolar", "V7 · _cita_cifra('849,7 mill', 849.7, 'Ventas 2023\\n849,7 millones') == 'no_localizada'",
     lambda M: M._cita_cifra("849,7 mill", 849.7, "Ventas 2023\n849,7 millones")[0], "no_localizada"),
    ("t8d_fecha_cualquier_cifra", "T8 · _cita_cifra('Notas 5-6-849,7', 849.7) == 'signo_indeterminado'",
     lambda M: M._cita_cifra("Notas 5-6-849,7", 849.7)[0], "signo_indeterminado"),
]
print(f"candidata: {ACT}")
for nombre, desc, fn, esperado in CASOS:
    c = fn(VE)
    m = fn(mutante(nombre, SRC_VE))
    print(f"   {nombre:34} {desc}\n      candidata: {c!r} ({'lo esperado' if c == esperado else '<<< NO es lo esperado'}) · mutación: {m!r} → {'la DETECTARÍA' if m != esperado and c == esperado else '<<< no la detectaría'}")
# el caso vacío de la prueba nueva de V3: da «ausente» con cualquier código
print("\n   caso de la prueba nueva «(V3, V7)» que no distingue nada: _cita_cifra('.5', 0.5, 'Ajuste .5') → candidata",
      VE._cita_cifra(".5", 0.5, "Ajuste .5")[0], "· sin el decimal sin cero (v3a):", mutante("v3a_sin_decimal_sin_cero", SRC_VE)._cita_cifra(".5", 0.5, "Ajuste .5")[0],
      "· (la cita «.5» se localiza entera y la forma «.5» no es una de las de _cifras: límite que ya existía)")

print("\n   T6 · una clave a TRES ediciones con proporción < 0,88 (fijaría el umbral ≤ 3 de la distancia de edición; hoy t6c, distancia 2, sobrevive)")
import difflib
tmp = tempfile.mkdtemp(prefix="e8_", dir=os.path.join(F, "tmp"))
try:
    def modo(PL, clave):
        json.dump({"tipo": "x", clave: "estricta"}, open(os.path.join(tmp, "alcance_v2.json"), "w"))
        try:
            return "sin error: " + repr(PL.modo_entrada_efectiva(tmp))
        except SystemExit:
            return "ERROR"
        except Exception as ex:  # noqa: BLE001
            return "ERROR (" + type(ex).__name__ + ")"
    PLC = types.ModuleType("pl_c"); PLC.__file__ = os.path.join(PV, "scripts", "pipeline.py")
    ruta = list(sys.path); exec(compile(SRC_PL, "pipeline.py", "exec"), PLC.__dict__); sys.path[:] = ruta
    PL2 = mutante("t6c_distancia_2", SRC_PL)
    for clave in ("emtrada_efextiba", "emtrada_efectiba", "tasa_efectiva", "entradas_otras", "emtrada_efextibas"):
        k = re.sub(r"[^a-z]", "", clave.lower())
        print(f"      «{clave}»: proporción {difflib.SequenceMatcher(None, k, 'entradaefectiva').ratio():.3f}, ediciones {PLC._ediciones(k, 'entradaefectiva')} · candidata: {modo(PLC, clave)[:40]} · con distancia ≤ 2: {modo(PL2, clave)[:40]}")
finally:
    shutil.rmtree(tmp, ignore_errors=True)
