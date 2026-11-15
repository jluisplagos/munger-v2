#!/usr/bin/env python3
"""Reproduce los tres fallos R1–R3 de la revisión externa de la 4.14 (encargo correctivo §2) con el registro sintético completo de
test_verificacion_entradas_414.py, con el código de la 4.14 (reproduccion/codigo_4_14/) o con el vigente.

  R1 · Historia!F6 con la página «999999»;  R2 · su archivo cambiado a fuentes_sinteticas/NO_EXISTE.txt con sha256 = None;
  R3 · _cita_contiene(«Amortización: 150», 149.5), («Partida: 0», 0.49) y («Acciones: 45479», 45479.209).
Con el código 4.14 (y su batería) el control positivo es apto y los tres casos siguen aptos (o True): es el defecto. Con el vigente
(y la batería 4.14 con el fixture adaptado a la 4.15: fuente sintética con huella y comprobaciones selladas), el control positivo es apto
y los tres casos dejan de serlo: R1 discrepancia, R2 pendiente, R3 False. Los casos completos están en test_verificacion_entradas_415.py.
Uso (desde munger_v2_r1/): python3 -I -B …/reproducir_r1_r3.py --codigo 4.14|vigente SALIDA.json"""
import argparse, importlib.machinery, importlib.util, json, os, shutil, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
PV = os.path.abspath(os.path.join(AQUI, "..", "..", ".."))
ap = argparse.ArgumentParser()
ap.add_argument("--codigo", choices=("4.14", "vigente"), required=True)
ap.add_argument("salida")
a = ap.parse_args()
sys.path.insert(0, os.path.join(PV, "scripts"))
if a.codigo == "4.14":
    R = os.path.join(AQUI, "..", "reproduccion", "codigo_4_14")
    spec = importlib.util.spec_from_file_location("verificacion_entradas", os.path.join(R, "verificacion_entradas.py.txt"),
                                                  loader=importlib.machinery.SourceFileLoader("verificacion_entradas", os.path.join(R, "verificacion_entradas.py.txt")))
    VE = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(VE)
    sys.modules["verificacion_entradas"] = VE
    src = open(os.path.join(R, "test_verificacion_entradas_414.py.txt"), encoding="utf-8").read()
else:
    import verificacion_entradas as VE  # noqa: E402
    src = open(os.path.join(PV, "pruebas", "test_verificacion_entradas_414.py"), encoding="utf-8").read()
corte = src.index('r = con()\npaso("P"')
ns = {"__file__": os.path.join(PV, "pruebas", "test_verificacion_entradas_414.py"), "__name__": "reproduccion"}
sys.argv = [ns["__file__"]]
exec(compile(src[:corte], ns["__file__"], "exec"), ns)
con, ent = ns["con"], ns["ent"]
K = "Historia!F6"
out = {"codigo": a.codigo, "entrada": K}
r = con(); out["control_positivo_apto"] = r["apto_por_entradas"]
r = con(lambda g: ent(g, K)["fuente"].update(pagina="999999"))
out["R1_pagina_999999"] = {"apto": r["apto_por_entradas"], "problemas_de_la_entrada": [x for x in r["errores"] + r["discrepancias"] + r["pendientes"] + r["desactualizadas"] if x.startswith(K)]}
r = con(lambda g: ent(g, K)["fuente"].update(archivo="fuentes_sinteticas/NO_EXISTE.txt", sha256=None))
out["R2_fuente_ausente"] = {"apto": r["apto_por_entradas"], "problemas_de_la_entrada": [x for x in r["errores"] + r["discrepancias"] + r["pendientes"] + r["desactualizadas"] if x.startswith(K)]}
out["R3"] = {"«Amortización: 150» contiene 149.5": VE._cita_contiene("Amortización: 150", 149.5), "«Partida: 0» contiene 0.49": VE._cita_contiene("Partida: 0", 0.49),
             "«Acciones: 45479» contiene 45479.209": VE._cita_contiene("Acciones: 45479", 45479.209)}
json.dump(out, open(a.salida, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(out, ensure_ascii=False, indent=1)[:1500])
shutil.rmtree(ns["TMP"], ignore_errors=True)
