#!/usr/bin/env python3
"""g5 · séptima comprobación · ¿detectan las pruebas del bloque (V1–V7, W1, W3, W4) lo que dicen? Evaluación A NIVEL DE UNIDAD (segundos;
la batería entera, en mutaciones7.py). Se extrae de test_verificacion_entradas_415.py de la CANDIDATA el bloque de pruebas
(«# (hito 2, quinta comprobación, V1–V7 y pruebas de V4)» … hasta el control positivo final; son llamadas puras a VE) y se ejecuta tal cual contra:
 (a) la candidata 45ff57c; (b) el código de 8196522 (sin W3–W5); (c) el de 876bfc2 (sin V1–V7); (d) 8196522 con las propuestas de la sexta
 (prop6); (e) cada definición de mutantes7.py cargada en memoria. Para T6 (pipeline.py) se repite el bucle de las «erratas dobles».
Una prueba «detecta» una mutación si pasa con la candidata y FALLA con el código mutado.
Uso: python3 -I -B g5_pruebas_unidad_y_mutaciones.py [archivo de pruebas alternativo]   (p. ej. el de fix7t, con los casos que propone el revisor)"""
import difflib, json, os, re, shutil, sys, tempfile, time, types
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun7 import VE, VP, VQ, V876, F, PV, ACT, ANT, PROP  # noqa: E402
import mutantes7 as MU  # noqa: E402

ARCH = sys.argv[1] if len(sys.argv) > 1 else os.path.join(PV, "pruebas", "test_verificacion_entradas_415.py")
T415 = open(ARCH, encoding="utf-8").read()
ini = T415.index("# (hito 2, quinta comprobación, V1–V7 y pruebas de V4)")
fin = T415.index("r = con()\npaso(\"RW\", \"el control positivo sigue apto después de los casos RW\"", ini)
BLOQUE = T415[ini:fin]
print(f"archivo de pruebas: {os.path.relpath(ARCH, F)}\nbloque de pruebas: {len(BLOQUE.splitlines())} líneas, {BLOQUE.count('paso(')} pruebas")


def cargar_texto(src, nombre):
    m = types.ModuleType(nombre)
    m.__file__ = VE.__file__
    ruta = list(sys.path)
    exec(compile(src, nombre + ".py", "exec"), m.__dict__)
    sys.path[:] = ruta
    return m


def ejecutar_bloque(mod):
    res = []
    exec(compile(BLOQUE, "bloque_pruebas", "exec"), {"VE": mod, "paso": lambda b, n, ok, det=None: res.append((n, bool(ok), det)), "_time": time})
    return res


SRC_VE = open(VE.__file__, encoding="utf-8").read()
base = ejecutar_bloque(VE)
print(f"\n== (a) candidata {ACT}")
for n, ok, d in base:
    print(f"   {'PASA ' if ok else 'FALLA'} {n[:150]}" + (f" · {d}" if d and not ok else ""))
for etiqueta, mod in ((f"(b) {ANT}: sin W3, W4 ni W5", VP), ("(c) 876bfc2: sin V1–V7", V876), (f"(d) {PROP}", VQ)):
    r = ejecutar_bloque(mod)
    print(f"\n== {etiqueta}: {sum(ok for _n, ok, _d in r)} de {len(r)} pasan")
    for n, ok, d in r:
        if not ok:
            print(f"   FALLA (detecta) {n[:100]} · {str(d)[:230]}")

print("\n== (e) definiciones de mutantes7.py sobre verificacion_entradas.py, una cada vez")
res = {}
for nombre, (grupo, hall, desc, cambios, bats) in MU.M.items():
    if any(a != MU.VEP for a, _v, _n in cambios) or grupo == "control":
        continue
    s = SRC_VE
    for _a, viejo, nuevo in cambios:
        assert s.count(viejo) == 1 and viejo != nuevo, (nombre, s.count(viejo))
        s = s.replace(viejo, nuevo)
    r = ejecutar_bloque(cargar_texto(s, "ve_mut_" + nombre))
    fallan = [(n, d) for n, ok, d in r if not ok]
    res[nombre] = fallan
    if nombre == "x1_correccion_propuesta":
        est = "PASA entero (compatible)" if not fallan else "<<< FALLA con la corrección propuesta"
    else:
        est = f"DETECTADA por {len(fallan)} prueba(s)" if fallan else "<<< NO detectada"
    print(f"   {nombre:40} {grupo:3} {hall:6} {est}")
    for n, d in fallan:
        print(f"        FALLA: {n[:60]} · {str(d)[:200]}")
print("\n   resumen: " + json.dumps({g: {"detectadas": sorted(k for k, v in res.items() if v and MU.M[k][0] == g), "NO detectadas": sorted(k for k, v in res.items() if not v and MU.M[k][0] == g)}
                                    for g in ("w1", "x1", "w", "v")}, ensure_ascii=False))

print("\n== (f) T6 (pipeline.py): el bucle de las «erratas dobles» de test_entrada_efectiva_415.py de la candidata, con el código y con t6c")
TEE = open(os.path.join(PV, "pruebas", "test_entrada_efectiva_415.py"), encoding="utf-8").read()
m = re.search(r"for errata_doble in \(([^)]*)\):", TEE)
ERRATAS = tuple(json.loads("[" + m.group(1) + "]"))
SRC_PL = open(os.path.join(PV, "scripts", "pipeline.py"), encoding="utf-8").read()
tmp = tempfile.mkdtemp(prefix="g5_", dir=os.path.join(F, "tmp"))


def ediciones(a, b):
    ant = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        act = [i]
        for j, cb in enumerate(b, 1):
            act.append(min(ant[j] + 1, act[j - 1] + 1, ant[j - 1] + (ca != cb)))
        ant = act
    return ant[-1]


def erratas(PL):
    out = {}
    for e in ERRATAS:
        json.dump({"tipo": "x", e: "estricta"}, open(os.path.join(tmp, "alcance_v2.json"), "w"))
        try:
            out[e] = "sin error: " + repr(PL.modo_entrada_efectiva(tmp))
        except SystemExit:
            out[e] = "ERROR (SystemExit)"
        except Exception as ex:  # noqa: BLE001
            out[e] = "ERROR (" + type(ex).__name__ + ")"
    return out


for e in ERRATAS:
    k = re.sub(r"[^a-z]", "", e.lower())
    print(f"   «{e}»: proporción de parecido {difflib.SequenceMatcher(None, k, 'entradaefectiva').ratio():.3f} · distancia de edición {ediciones(k, 'entradaefectiva')}")
try:
    for nombre in ("(candidata)", "t6c_distancia_2"):
        s = SRC_PL
        if nombre in MU.M:
            for _a, viejo, nuevo in MU.M[nombre][3]:
                assert s.count(viejo) == 1, nombre
                s = s.replace(viejo, nuevo)
        PL = cargar_texto(s, "pl_" + re.sub(r"\W", "_", nombre))
        r = erratas(PL)
        sin_error = [e for e, v in r.items() if not v.startswith("ERROR")]
        print(f"   {nombre:20} " + ("todas dan error (la prueba PASA)" if not sin_error else f"SIN error: {sin_error} → la prueba FALLA (DETECTADA)"))
finally:
    shutil.rmtree(tmp, ignore_errors=True)
