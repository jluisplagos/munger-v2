#!/usr/bin/env python3
"""Pruebas de la unidad declarada de las acciones diluidas en la Historia (examen del personaje, caso Ahold; commit f5a3381 y su
corrección tras la revisión independiente: hallazgos 1, 3 y 4). No escribe en el repositorio: trabaja sobre copias temporales.
Uso: python3 -B pruebas/test_acciones_unidad_examen.py      (código 0 si todo pasa)
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

AHOLD = os.path.join(PV, "empresas_v2_correcciones", "2026-11_examen_universo", "ahold_4_15", "Ahold")
ELIS = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_14", "elis_motor_A", "Elis")
ANIOS = list(range(2016, 2026))
SERIE_AHOLD = [1031, 1281, 1203, 1112, 1072, 1034, 1001, 966, 933, 905]
fallos, total = [], 0


def paso(nombre, ok, detalle=""):
    global total
    total += 1
    print(("PASA " if ok else "FALLA") + f" · {nombre}" + (f" · {detalle}" if detalle else ""))
    if not ok:
        fallos.append(nombre)


def copiar(origen, dest, partes=("texto", "fase1_partes", "fase1_metadatos.json", "fase1_fuentes.json")):
    os.makedirs(dest)
    for n in partes:
        s = os.path.join(origen, n)
        if os.path.isdir(s):
            shutil.copytree(s, os.path.join(dest, n))
        elif os.path.exists(s):
            shutil.copy2(s, os.path.join(dest, n))
    return dest


def construir(c):
    r = subprocess.run([sys.executable, "-B", os.path.join(PV, "scripts", "fase1_historia.py"), "construir", c], capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def serie(c):
    d = json.load(open(os.path.join(c, "fase1_v63.json"), encoding="utf-8"))
    return [None if v is None else round(v, 3) for v in d["historia"]["partidas"]["acciones_diluidas"]["valores"]]


# 1 · función de coherencia
paso("serie de Ahold coherente", F.incoherencias_acciones(ANIOS, SERIE_AHOLD, {"valor": 905}) == [])
mal = list(SERIE_AHOLD); mal[4] = 1.072
inc = F.incoherencias_acciones(ANIOS, mal, {"valor": 905})
paso("un año dividido por mil se detiene (dos saltos)", len(inc) == 2 and all("salto" in x for x in inc), "; ".join(inc)[:160])
paso("último año frente a los metadatos (C55)", any("metadatos" in x for x in F.incoherencias_acciones(ANIOS, SERIE_AHOLD, {"valor": 905000})))
paso("años sin dato no rompen la comprobación", F.incoherencias_acciones(ANIOS, [None] * 3 + SERIE_AHOLD[3:], {"valor": 905}) == [])
paso("metadatos sin valor numérico no rompen", F.incoherencias_acciones(ANIOS, SERIE_AHOLD, {"valor": "n/d"}) == [])

t = tempfile.mkdtemp(prefix="acciones_unidad_")
try:
    if os.path.isdir(os.path.join(AHOLD, "fase1_partes")):
        # 2 · Ahold real con las unidades declaradas
        c = copiar(AHOLD, os.path.join(t, "ahold_ok", "Ahold"))
        rc, out = construir(c)
        paso("Ahold con unidad declarada: construye", rc == 0, out.strip()[-160:])
        paso("Ahold: 1.031 … 905 millones", rc == 0 and serie(c) == [float(x) for x in SERIE_AHOLD], str(serie(c)) if rc == 0 else "")
        # 3 · un año sin unidad: antes 1,072 en silencio; ahora se detiene
        c2 = copiar(AHOLD, os.path.join(t, "ahold_sin_unidad", "Ahold"))
        p = os.path.join(c2, "fase1_partes", "AR_2020.json")
        d = json.load(open(p, encoding="utf-8")); d["partidas"]["acciones_diluidas"].pop("unidad", None)
        json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        rc, out = construir(c2)
        paso("Ahold con un año sin unidad: se detiene", rc == 1 and "acciones diluidas incoherentes" in out, out.strip()[-200:])
        # 4 · unidad mal formada: mensaje, no TypeError
        p3 = os.path.join(c2, "fase1_partes", "AR_2021.json")
        d = json.load(open(p3, encoding="utf-8")); d["partidas"]["acciones_diluidas"]["unidad"] = []
        json.dump(d, open(p3, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        try:
            e = F.comprobar_anio(c2, 2021)
            paso("unidad [] da un mensaje de error", any("acciones_diluidas: unidad" in x for x in e), "; ".join(e)[:160])
        except Exception as ex:  # noqa: BLE001
            paso("unidad [] da un mensaje de error", False, f"{type(ex).__name__}: {ex}")
    else:
        paso("expediente de Ahold disponible", False, AHOLD)
    # 5 · regresión: Elis sin unidad declarada construye igual que antes del parche
    if os.path.isdir(os.path.join(ELIS, "fase1_partes")):
        c4 = copiar(ELIS, os.path.join(t, "elis", "Elis"))
        rc, out = construir(c4)
        ref = json.load(open(os.path.join(ELIS, "fase1_v63.json"), encoding="utf-8"))["historia"]["partidas"]["acciones_diluidas"]["valores"]
        paso("Elis sin unidad: construye y conserva su serie de acciones", rc == 0 and serie(c4) == [None if v is None else round(v, 3) for v in ref], out.strip()[-160:])
    else:
        paso("expediente de Elis disponible", False, ELIS)
finally:
    shutil.rmtree(t, ignore_errors=True)

print(f"\n{total - len(fallos)}/{total} comprobaciones PASAN")
sys.exit(1 if fallos else 0)
