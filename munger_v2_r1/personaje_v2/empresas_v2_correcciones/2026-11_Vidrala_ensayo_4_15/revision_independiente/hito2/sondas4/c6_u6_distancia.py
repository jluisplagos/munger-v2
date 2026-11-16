#!/usr/bin/env python3
"""c6 · T6 (cuarta comprobación): la errata de la clave «entrada_efectiva» en alcance_v2.json se detecta ahora por parecido (≥ 0,88) O por
distancia de edición (≤ 3, sobre la clave en minúsculas y sin lo que no sea a–z). Se llama a pipeline._alcance_modo de las dos candidatas.
A) erratas de una y de dos ediciones (las mismas muestras que r6 de la tercera comprobación, misma semilla), y de tres: ¿cuántas dejan el
   modo en «registrada» en silencio?   B) claves legítimas parecidas: ¿cuáles vuelven a dar error?   C) las claves de los alcances reales.
Uso: python3 -I -B c6_u6_distancia.py"""
import glob, importlib.util, json, os, random, re, sys, tempfile
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sondas3"))
from comun3 import VE, PV, PVP, ACT, ANT, F  # noqa: E402
import pipeline as PL  # noqa: E402


def cargar_prev_pipeline():
    p = os.path.join(PVP, "scripts", "pipeline.py")
    spec = importlib.util.spec_from_file_location("pipeline_anterior", p)
    m = importlib.util.module_from_spec(spec)
    ruta = list(sys.path)
    spec.loader.exec_module(m)
    sys.path[:] = ruta
    return m


PLP = cargar_prev_pipeline()
assert "_ediciones" in open(PL.__file__, encoding="utf-8").read() and "_ediciones" not in open(PLP.__file__, encoding="utf-8").read()
print(f"pipeline: {ACT} frente a {ANT}")
OBJ = "entradaefectiva"
LETRAS = "abcdefghijklmnopqrstuvwxyz"
TMP = tempfile.mkdtemp(prefix="rev4_c6_", dir=os.path.join(F, "tmp"))
d0 = os.path.join(TMP, "X")
os.makedirs(d0)


def que_hace(M, clave):
    json.dump({"tipo": "x", "aviso": "y", clave: "estricta"}, open(os.path.join(d0, "alcance_v2.json"), "w", encoding="utf-8"))
    try:
        return "silencio (" + repr(M._alcance_modo(d0)) + ")"
    except ValueError as ex:
        return "ERROR (errata)" if "errata" in str(ex) else "ERROR: " + str(ex)[:50]


def ediciones(s):
    out = set()
    for i in range(len(s)):
        out.add(s[:i] + s[i + 1:])
        out |= {s[:i] + c + s[i + 1:] for c in LETRAS if c != s[i]}
        if i + 1 < len(s) and s[i] != s[i + 1]:
            out.add(s[:i] + s[i + 1] + s[i] + s[i + 2:])
    for i in range(len(s) + 1):
        out |= {s[:i] + c + s[i:] for c in LETRAS}
    out.discard(s)
    return out


e1 = ediciones(OBJ)
rnd = random.Random(20261115)
e2 = set()
for x in rnd.sample(sorted(e1), 400):
    e2 |= set(rnd.sample(sorted(ediciones(x) - e1 - {OBJ}), 60))
rnd3 = random.Random(20261116)
e3 = set()
for x in rnd3.sample(sorted(e2), 300):
    e3 |= set(rnd3.sample(sorted(ediciones(x) - e2 - e1 - {OBJ}), 20))
print("== A · erratas de «entradaefectiva» (clave ya normalizada) que NO dan error (el modo queda en «registrada» en silencio)")
for nombre, conj in (("una edición", e1), ("dos ediciones (muestra, semilla de r6)", e2), ("tres operaciones de edición (muestra)", e3)):
    na = sorted(x for x in conj if que_hace(PLP, x).startswith("silencio"))
    nb = sorted(x for x in conj if que_hace(PL, x).startswith("silencio"))
    print(f"   {nombre:42} {len(conj):6} claves · anterior: {len(na):5} sin detectar ({100 * len(na) / len(conj):.1f} %) · cuarta: {len(nb):5} ({100 * len(nb) / len(conj):.1f} %)" + (f" · p. ej. {nb[:5]}" if nb else ""))

print("\n== B · claves concretas: anterior → cuarta")
CASOS = [("erratas", ["entrada_efectiba", "Entrada-Efectiva", "entrada efectiva", "emtrada_efectiba", "entrada_efectibo", "entrara_efectiba", "entrda_efectva", "emtrda_efctiva", "entrada_efec", "ent_efectiva",
                      "entrada_efect", "entrada_ef", "entrada_efectiva_", "entrada_efectiva2", "3ntrada_3f3ctiva", "entrada.efectiva", "entradaEfectiva", "ENTRADA_EFECTIVA", " entrada_efectiva"]),
         ("variantes de quien quiere declarar el modo (ni error ni «estricta»: silencio)", ["modo_entrada_efectiva", "entrada_efectiva_modo", "entrada_estricta", "modo", "efectiva", "entrada_efectiva_estricta", "effective_input"]),
         ("claves legítimas que se parecen (un error aquí es un rechazo en falso)", ["tasa_efectiva", "entrega_efectiva", "entrada_de_efectivo", "entradas_efectivo", "fecha_efectiva", "salida_efectiva", "entrada_en_vigor",
                                                                                   "entrada_efectiva_motivo", "nota_entrada_efectiva", "fecha_entrada_efectiva", "entrada_efectiva_nota", "entrada_selectiva",
                                                                                   "entrada_afectada", "entidad_efectiva", "estrada_efectiva", "entrada_colectiva", "entrada_defectiva", "entrada_electiva", "gerencia_efectiva"])]
for titulo, claves in CASOS:
    print(f"   -- {titulo}")
    for k in claves:
        a, b = que_hace(PLP, k), que_hace(PL, k)
        nk = re.sub(r"[^a-z]", "", k.lower())
        marca = "   <<< cambia" if a.split(" ")[0] != b.split(" ")[0] else ""
        print(f"      {k!r:30} distancia {PL._ediciones(nk, OBJ)} · anterior: {a:28} cuarta: {b}{marca}")

print("\n== C · alcance_v2.json reales del árbol: claves y su distancia a «entradaefectiva»")
claves, n, errores = {}, 0, []
for p in sorted(glob.glob(os.path.join(PV, "empresas_v2*", "**", "alcance_v2.json"), recursive=True)):
    n += 1
    try:
        a = json.load(open(p, encoding="utf-8"))
    except (OSError, ValueError):
        continue
    for k in (a if isinstance(a, dict) else {}):
        claves[k] = min(claves.get(k, 99), PL._ediciones(re.sub(r"[^a-z]", "", str(k).lower()), OBJ))
    try:
        ra = PLP._alcance_modo(os.path.dirname(p))
    except ValueError as ex:
        ra = "ERROR " + str(ex)[:40]
    try:
        rb = PL._alcance_modo(os.path.dirname(p))
    except ValueError as ex:
        rb = "ERROR " + str(ex)[:40]
    if ra != rb or str(rb).startswith("ERROR"):
        errores.append((os.path.relpath(p, PV), ra, rb))
print(f"   {n} alcances · {len(claves)} claves distintas · las más cercanas: {sorted(claves.items(), key=lambda x: x[1])[:6]}")
print(f"   alcances en los que _alcance_modo cambia o da error: {len(errores)} {errores[:3]}")
