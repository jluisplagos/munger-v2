#!/usr/bin/env python3
"""n17 · N1 (propuesta): ¿qué expedientes del árbol cambiarían de ficha si el bloque de I20 dependiera, además de los dos archivos, de
las claves que el pipeline deja en estado_pipeline.json (entrada_efectiva: paso 2 desde la 4.15; verificacion_entradas: paso 12 desde la
4.14), del modo declarado en alcance_v2.json o del registrado en fase1_metadatos.json? Solo lee.
Uso: python3 -I -B n17_discriminante_i20.py"""
import collections, json, os, sys
F = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
raiz = os.path.join(F, "copia", "munger_v2_r1")


def j(p):
    try:
        return json.load(open(p, encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return None


c = collections.Counter()
cambian = []
for d, ds, fs in os.walk(raiz):
    ds[:] = [x for x in ds if x not in ("__pycache__", ".lo_perfil")]
    if "estado_pipeline.json" not in fs:
        continue
    st = j(os.path.join(d, "estado_pipeline.json"))
    if not isinstance(st, dict):
        continue
    archivos = any(os.path.isfile(os.path.join(d, n)) for n in ("verificacion_entradas.json", "entrada_efectiva.json"))
    alc = j(os.path.join(d, "alcance_v2.json")) if "alcance_v2.json" in fs else None
    meta = j(os.path.join(d, "fase1_metadatos.json")) if "fase1_metadatos.json" in fs else None
    senales = {"estado.entrada_efectiva": "entrada_efectiva" in st, "estado.verificacion_entradas": "verificacion_entradas" in st,
               "alcance.entrada_efectiva": isinstance(alc, dict) and "entrada_efectiva" in alc, "metadatos.entrada_efectiva": isinstance(meta, dict) and "entrada_efectiva" in meta}
    cerrado = os.path.lexists(os.path.join(d, "cierre_vigente.json"))
    historial = "historial_cierres" in d or "antecedentes" in d
    clave = ("con registro o declaración" if archivos else "sin ninguno de los dos archivos") + " · " + ("con alguna señal" if any(senales.values()) else "sin señales")
    c[clave] += 1
    if not archivos and any(senales.values()):
        cambian.append((os.path.relpath(d, raiz), [k for k, v in senales.items() if v], "cierre vigente" if cerrado else "sin cierre vigente", "en historial" if historial else ""))
print("carpetas con estado_pipeline.json:", sum(c.values()))
for k, v in sorted(c.items()):
    print(f"   {v:4}  {k}")
print("expedientes SIN los archivos cuya ficha cambiaría con la propuesta (tienen alguna señal):", len(cambian))
for x in cambian[:25]:
    print("   ", x)
