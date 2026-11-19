#!/usr/bin/env python3
"""Pruebas de las acciones exactas de los metadatos (Análisis!C55; examen, zoetis_t1c; rama producto/minoritarios-acciones).

Zoetis: el 10-K 2025 (p. 68) da 424.927.535 acciones en circulación y los metadatos guardaban 424,928 millones (redondeo a 3 decimales,
que solo vale para importes: verificacion_entradas, N4). Ningún script redondeaba: la cifra llegaba redondeada y nada lo detectaba.
Ahora los metadatos pueden traer la cifra impresa («impreso» y «unidad») y construir se detiene si «valor» no es exactamente esa cifra
en millones; sin «impreso» (metadatos anteriores) todo sigue igual. El libro escribe el valor por su repr (v63_xml), sin redondear.
No escribe en el repositorio: trabaja sobre copias temporales.
Uso: python3 -B pruebas/test_acciones_metadatos_exactas.py      (código 0 si todo pasa)
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
PV = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(PV, "scripts"))
import fase1_historia as F  # noqa: E402
import v63_xml  # noqa: E402

ZOETIS = os.path.join(PV, "empresas_v2_correcciones", "2026-11_examen_universo", "zoetis_t1c", "Zoetis")
PARTES = ("texto", "fase1_partes", "fase1_metadatos.json", "fase1_fuentes.json", "fase1_decisiones.json")
fallos, total = [], 0


def paso(nombre, ok, detalle=""):
    global total
    total += 1
    print(("PASA " if ok else "FALLA") + f" · {nombre}" + (f" · {detalle}" if detalle else ""))
    if not ok:
        fallos.append(nombre)


def defectos(ac):
    try:
        return F.defecto_acciones_meta(ac)
    except AttributeError as ex:  # antes del cambio no existe la comprobación: la prueba falla, no se interrumpe
        return [f"AttributeError: {ex}"]


# 1 · la comprobación
paso("424.927.535 acciones con valor 424,928: defecto (redondeado)", len(d := defectos({"valor": 424.928, "impreso": "424.927.535"})) == 1
     and "424.927535" in d[0] and "no se redondea" in d[0], "; ".join(d))
paso("424.927.535 con valor 424,927535: sin defecto", defectos({"valor": 424.927535, "impreso": "424.927.535"}) == [])
paso("unidad «millones» («905» → 905)", defectos({"valor": 905, "impreso": "905", "unidad": "millones"}) == [])
paso("unidad «miles» («1.500» → 1,5)", defectos({"valor": 1.5, "impreso": "1.500", "unidad": "miles"}) == [])
paso("cifra en unidades tomada como millones (424.927,535): defecto", len(defectos({"valor": 424927.535, "impreso": "424.927.535"})) == 1)
paso("unidad que no es de la lista: defecto", any("unidad" in x for x in defectos({"valor": 1, "impreso": "1", "unidad": "docenas"})))
paso("impreso que no es texto: defecto", len(defectos({"valor": 424.927535, "impreso": 424927535})) == 1)
paso("impreso no numérico: defecto", len(defectos({"valor": 1, "impreso": "12a"})) == 1)
paso("valor booleano o ausente: defecto", len(defectos({"valor": True, "impreso": "1"})) == 1 and len(defectos({"impreso": "1"})) == 1)
paso("impreso cero o guion: defecto (no es un número positivo de acciones)", len(defectos({"valor": 0, "impreso": "-"})) == 1)
paso("metadatos sin «impreso» (anteriores a la regla): sin cambio", defectos({"valor": 424.928}) == [] and defectos(None) == [])

# 2 · el libro escribe el valor exacto (repr), sin redondear
paso("v63_xml escribe 424.927535 tal cual", v63_xml._texto_numero(424.927535) == "424.927535", v63_xml._texto_numero(424.927535))
cap = F.exacto(73.08) * F.exacto(424.927535)
paso("y C41 = 73,08 × 424,927535 = 31.053,7042578 se escribe exacto (sin heredar el redondeo de C55: no 31.053,73824)",
     F.Fraction(v63_xml._texto_numero(float(cap))) == cap and cap == F.Fraction("31053.7042578"), v63_xml._texto_numero(float(cap)))

# 3 · la instrucción del agente de metadatos
prm = open(os.path.join(PV, "prompts", "metadatos_fase1.md"), encoding="utf-8").read()
paso("el prompt de metadatos pide «impreso», «unidad» y el valor con todos sus decimales", "`impreso`" in prm and "TODOS sus decimales" in prm
     and "nunca redondeada" in prm)


# 4 · construir sobre copias de zoetis_t1c
def copiar(dest):
    os.makedirs(dest)
    for n in PARTES:
        s = os.path.join(ZOETIS, n)
        if os.path.isdir(s):
            shutil.copytree(s, os.path.join(dest, n))
        elif os.path.exists(s):
            shutil.copy2(s, os.path.join(dest, n))
    return dest


def construir_con(c, cambio):
    mp = os.path.join(c, "fase1_metadatos.json")
    m = json.load(open(mp, encoding="utf-8"))
    cambio(m["acciones_diluidas"])
    json.dump(m, open(mp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    r = subprocess.run([sys.executable, "-B", os.path.join(PV, "scripts", "fase1_historia.py"), "construir", c], capture_output=True, text=True)
    f = os.path.join(c, "fase1_v63.json")
    return r.returncode, (r.stdout + r.stderr).strip(), (json.load(open(f, encoding="utf-8")) if os.path.exists(f) else None)


t = tempfile.mkdtemp(prefix="acciones_meta_")
try:
    if os.path.isdir(os.path.join(ZOETIS, "fase1_partes")) and os.path.isdir(os.path.join(ZOETIS, "texto")):
        rc, out, f1 = construir_con(copiar(os.path.join(t, "redondeada", "Zoetis")), lambda a: a.update(impreso="424.927.535", unidad="unidades"))
        paso("zoetis_t1c con «impreso» 424.927.535 y valor 424,928: construir se detiene sin escribir fase1_v63.json",
             rc == 1 and f1 is None and "no se redondea" in out, out[-220:])
        rc, out, f1 = construir_con(copiar(os.path.join(t, "exacta", "Zoetis")), lambda a: a.update(valor=424.927535, impreso="424.927.535", unidad="unidades"))
        v = f1 and f1["acciones_diluidas"]["valor"]
        paso("zoetis_t1c con la cifra exacta: construye y fase1_v63.json lleva C55 = 424,927535", rc == 0 and v == 424.927535 and repr(v) == "424.927535",
             repr(v) if rc == 0 else out[-200:])
        rc, out, f1 = construir_con(copiar(os.path.join(t, "anterior", "Zoetis")), lambda a: None)
        v = f1 and f1["acciones_diluidas"]["valor"]
        ref = json.load(open(os.path.join(ZOETIS, "fase1_v63.json"), encoding="utf-8"))["acciones_diluidas"]["valor"]
        paso("zoetis_t1c con sus metadatos de hoy (sin «impreso»): construye igual que antes (424,928)", rc == 0 and v == ref == 424.928,
             repr(v) if rc == 0 else out[-200:])
    else:  # el expediente del examen no forma parte de todos los paquetes: sin él, la prueba real se omite y lo dice
        print(f"OMITIDA · construir sobre zoetis_t1c: no está el expediente {ZOETIS}")
finally:
    shutil.rmtree(t, ignore_errors=True)

print(f"\n{total - len(fallos)}/{total} comprobaciones PASAN")
sys.exit(1 if fallos else 0)
