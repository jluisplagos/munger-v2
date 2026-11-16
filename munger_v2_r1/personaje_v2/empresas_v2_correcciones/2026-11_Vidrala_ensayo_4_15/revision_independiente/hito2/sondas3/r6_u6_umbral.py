#!/usr/bin/env python3
"""r6 · N9/U6 (tercera pasada): el umbral de «errata de la clave entrada_efectiva» en alcance_v2.json pasa de 0,8 a 0,88
(difflib.SequenceMatcher sobre la clave en minúsculas y sin lo que no sea a–z, frente a «entradaefectiva»).
A) todas las erratas de UNA edición (borrar, cambiar, insertar una letra, trasponer dos contiguas) y una muestra de las de DOS ediciones:
   ¿cuántas dejan de detectarse (el modo queda en «registrada» en silencio) con cada umbral?
B) claves legítimas parecidas y formas habituales de escribir la clave: ¿error o silencio?  C) pipeline.modo_entrada_efectiva real.
Uso: python3 -I -B r6_u6_umbral.py"""
import difflib, itertools, json, os, random, re, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun3 import VE, PV
import pipeline as PL  # noqa: E402

OBJ = "entradaefectiva"
LETRAS = "abcdefghijklmnopqrstuvwxyz"


def ratio(k):
    return difflib.SequenceMatcher(None, re.sub(r"[^a-z]", "", str(k).lower()), OBJ).ratio()


def ediciones(s):
    out = set()
    for i in range(len(s)):
        out.add(s[:i] + s[i + 1:])                                  # borrar
        out |= {s[:i] + c + s[i + 1:] for c in LETRAS if c != s[i]}  # cambiar
        if i + 1 < len(s) and s[i] != s[i + 1]:
            out.add(s[:i] + s[i + 1] + s[i] + s[i + 2:])            # trasponer
    for i in range(len(s) + 1):
        out |= {s[:i] + c + s[i:] for c in LETRAS}                  # insertar
    out.discard(s)
    return out


e1 = ediciones(OBJ)
print(f"== A · erratas de una edición de «{OBJ}» (sobre la clave ya normalizada): {len(e1)}")
for u in (0.8, 0.88):
    no = sorted(x for x in e1 if ratio(x) < u)
    print(f"   umbral {u}: no detectadas {len(no)} de {len(e1)}" + (f" · p. ej. {no[:6]}" if no else ""))
rnd = random.Random(20261115)
e2 = set()
for x in rnd.sample(sorted(e1), 400):
    e2 |= set(rnd.sample(sorted(ediciones(x) - e1 - {OBJ}), 60))
print(f"   erratas de dos ediciones (muestra aleatoria con semilla fija): {len(e2)}")
for u in (0.8, 0.88):
    no = sorted(x for x in e2 if ratio(x) < u)
    print(f"   umbral {u}: no detectadas {len(no)} de {len(e2)} ({100 * len(no) / len(e2):.1f} %)" + (f" · p. ej. {no[:8]}" if no else ""))

print("\n== B · claves concretas: proporción y qué hace el control (umbral 0,8 de la candidata anterior → 0,88 de la tercera)")
CASOS = [("erratas de una letra", ["entrada_efectiba", "entrda_efectiva", "entrada_efectva", "entrada_efectivo", "entradas_efectiva", "Entrada-Efectiva", "entrada efectiva", "ENTRADA_EFECTIVA",
                                    "entradaEfectiva", "entrada_efcetiva", "entarda_efectiva"]),
         ("erratas de dos letras", ["emtrada_efectiba", "entrda_efectva", "entrada_efectibo", "entradas_efectivas", "emtrada_efectiva_", "entrada_afectiba", "entrara_efectiba"]),
         ("abreviaturas y variantes de quien quiere declarar el modo", ["entrada_efect", "entrada_efec", "ent_efectiva", "entrada_ef", "efectiva", "modo_entrada_efectiva", "entrada_efectiva_modo",
                                                                        "entrada_estricta", "modo", "modo_efectiva", "entrada_efectiva_estricta", "entradaefectivaestricta", "effective_input"]),
         ("claves legítimas que se parecen", ["tasa_efectiva", "entrada_efectiva_motivo", "nota_entrada_efectiva", "fecha_entrada_efectiva", "entrega_efectiva", "entrada_de_efectivo",
                                               "fecha_efectiva", "salida_efectiva", "entrada_en_vigor", "entradas", "entrada_efectiva_nota", "entrada_efectiva_fecha"])]
tmp = tempfile.mkdtemp(prefix="rev3_u6_")
for titulo, claves in CASOS:
    print(f"   -- {titulo}")
    for k in claves:
        d = os.path.join(tmp, re.sub(r"\W", "_", k) + "_" + str(len(os.listdir(tmp))))
        os.makedirs(d)
        json.dump({"tipo": "x", "aviso": "y", k: "estricta"}, open(os.path.join(d, "alcance_v2.json"), "w", encoding="utf-8"))
        try:
            r = repr(PL.modo_entrada_efectiva(d))
        except ValueError as ex:
            r = "ERROR (errata)" if "errata" in str(ex) else "ERROR: " + str(ex)[:60]
        rt = ratio(k)
        print(f"      {k!r:32} proporción {rt:.3f} · con 0,8: {'error' if rt >= 0.8 else 'silencio'} · tercera: {r}")
