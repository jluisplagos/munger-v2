#!/usr/bin/env python3
"""r1 · N1 (tercera pasada): ¿la condición nueva del bloque de I20 en ficha.py cambia la ficha de alguna carpeta del árbol? Para CADA carpeta
del árbol congelado (solo lectura) con estado_pipeline.json, ficha.json, ficha_provisional.json, cierre_vigente.json, alcance_v2.json o
fase1_metadatos.json se evalúan la condición de la candidata anterior (existe verificacion_entradas.json o entrada_efectiva.json) y la de la
tercera (además: estado_pipeline.json → entrada_efectiva es un objeto, o ficha._declara_modo(c): alcance_v2.json o fase1_metadatos.json
llevan la clave o NO SE PUEDEN LEER). Se usa la función real ficha._declara_modo.  Uso: python3 -I -B r1_bloque_fichas_historicas.py"""
import collections, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun3 import CONGELADO, PV
import ficha as FI  # noqa: E402


def j(p):
    try:
        return json.load(open(p, encoding="utf-8")), None
    except Exception as ex:  # noqa: BLE001
        return None, type(ex).__name__


NOMBRES = ("estado_pipeline.json", "ficha.json", "ficha_provisional.json", "cierre_vigente.json", "alcance_v2.json", "fase1_metadatos.json")
c = collections.Counter()
cambian, ilegibles = [], []
n = 0
for d, ds, fs in os.walk(CONGELADO):
    ds[:] = [x for x in ds if x not in ("__pycache__", ".lo_perfil")]
    if not any(x in fs for x in NOMBRES):
        continue
    n += 1
    pipe, err = j(os.path.join(d, "estado_pipeline.json")) if "estado_pipeline.json" in fs else (None, None)
    vieja = any(os.path.isfile(os.path.join(d, x)) for x in ("verificacion_entradas.json", "entrada_efectiva.json"))
    s_estado = isinstance((pipe or {}).get("entrada_efectiva") if isinstance(pipe, dict) else None, dict)
    s_decl = FI._declara_modo(d)
    nueva = vieja or s_estado or s_decl
    for x in ("alcance_v2.json", "fase1_metadatos.json"):
        if x in fs and j(os.path.join(d, x))[1]:
            ilegibles.append(os.path.relpath(os.path.join(d, x), CONGELADO))
    c[(vieja, nueva)] += 1
    if vieja != nueva:
        cambian.append((os.path.relpath(d, CONGELADO), {"estado.entrada_efectiva": s_estado, "_declara_modo": s_decl},
                        "con cierre_vigente.json" if os.path.lexists(os.path.join(d, "cierre_vigente.json")) else "sin cierre vigente",
                        "con ficha.json" if "ficha.json" in fs else "sin ficha.json"))
print("carpetas examinadas (con estado, ficha, cierre, alcance o metadatos):", n)
print("(condición anterior, condición nueva) → nº de carpetas:", {str(k): v for k, v in sorted(c.items())})
print("alcance_v2.json o fase1_metadatos.json que no se pueden leer:", len(ilegibles), ilegibles[:10])
print("carpetas cuya ficha llevaría ahora el bloque y antes no:", len(cambian))
for x in cambian:
    print("   ", x)
