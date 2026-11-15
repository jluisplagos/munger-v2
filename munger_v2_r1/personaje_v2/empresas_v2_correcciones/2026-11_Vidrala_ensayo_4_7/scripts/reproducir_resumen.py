#!/usr/bin/env python3
"""Reproduce el fallo del resumen configurado (encargo 4.7, bloque A) con el código de un paquete dado. Solo en temporales.

Uso: python3 -I reproducir_resumen.py --raiz <munger_v2_r1 a probar> [--expediente <Vidrala aprobado de la 4.6.1>]

Secuencia: (1) configuración válida con las rutas del paquete resueltas y resumen_csv = «cartera/resumen_global.csv» (relativa a la
configuración); (2) pipeline --config --desde 14; (3) marcador en fase_c.json → celdas.B101, sin tocar la auditoría; (4) informe.py
directo, sin --config; (5) pipeline --config --desde 14. En cada paso se muestran el código, las salidas oficiales y las filas de
la empresa en el CSV personalizado y en el predeterminado.
"""
import argparse
import csv
import json
import os
import shutil
import subprocess
import sys
import tempfile

ap = argparse.ArgumentParser()
ap.add_argument("--raiz", required=True)
ap.add_argument("--expediente")
a = ap.parse_args()
R = os.path.abspath(a.raiz)
SCR = os.path.join(R, "personaje_v2", "scripts")
EXP = os.path.abspath(a.expediente or os.path.join(R, "personaje_v2", "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_6_1", "Vidrala"))
PY = sys.executable
tmp = tempfile.mkdtemp(prefix="resumen47_")
d = os.path.join(tmp, "expediente", "Vidrala")
shutil.copytree(EXP, d, ignore=shutil.ignore_patterns(".lo_perfil"))
for f in ("resumen_v2.csv", "resumen_v2_historial.csv"):
    if os.path.exists(os.path.join(os.path.dirname(EXP), f)):
        shutil.copy(os.path.join(os.path.dirname(EXP), f), os.path.join(tmp, "expediente", f))
sys.path.insert(0, SCR)
sys.dont_write_bytecode = True
import config_v2  # noqa: E402
cfg = config_v2.cargar(os.path.join(R, "personaje_v2", "config_v2.json"))
cfg_dir = os.path.join(tmp, "cfg")
os.makedirs(os.path.join(cfg_dir, "cartera"))
cfg = {k: v for k, v in cfg.items() if not k.startswith("_")}
cfg["resumen_csv"] = "cartera/resumen_global.csv"
CONF = os.path.join(cfg_dir, "config.json")
json.dump(cfg, open(CONF, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
PERS, PRED = os.path.join(cfg_dir, "cartera", "resumen_global.csv"), os.path.join(tmp, "expediente", "resumen_v2.csv")


def filas(p):
    if not os.path.exists(p):
        return "no existe"
    return [(r.get("estado_analisis"), r.get("verificacion")[:60], r.get("precio_si"), r.get("accion")) for r in csv.DictReader(open(p, encoding="utf-8")) if r.get("empresa") == "Vidrala, S.A."]


def corre(etiqueta, cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    out = (r.stdout + r.stderr).strip()
    print(f"\n$ {etiqueta} → código {r.returncode}\n   {out.splitlines()[-1][:200] if out else ''}")
    print(f"   ficha.json {os.path.exists(os.path.join(d, 'ficha.json'))} · informe.md {os.path.exists(os.path.join(d, 'informe.md'))} · cierre_vigente.json {os.path.exists(os.path.join(d, 'cierre_vigente.json'))}")
    print(f"   CSV personalizado (cartera/resumen_global.csv): {filas(PERS)}")
    print(f"   CSV predeterminado (resumen_v2.csv junto al expediente): {filas(PRED)}")
    return r.returncode, filas(PERS)


print(f"REPRODUCCIÓN DEL FALLO DEL RESUMEN CONFIGURADO · código de {R}")
try:
    rc1, p1 = corre("pipeline.py COPIA --config CONFIG --desde 14", [PY, "-B", os.path.join(SCR, "pipeline.py"), d, "--config", CONF, "--desde", "14"])
    fc = json.load(open(os.path.join(d, "fase_c.json"), encoding="utf-8"))
    fc["celdas"]["B101"] += " [MARCADOR 4.7]"
    json.dump(fc, open(os.path.join(d, "fase_c.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("\nmodificación: fase_c.json → celdas.B101 += « [MARCADOR 4.7]» (auditoría sin tocar)")
    rc2, p2 = corre("informe.py COPIA (directo, sin --config)", [PY, "-B", os.path.join(SCR, "informe.py"), d])
    rc3, p3 = corre("pipeline.py COPIA --config CONFIG --desde 14", [PY, "-B", os.path.join(SCR, "pipeline.py"), d, "--config", CONF, "--desde", "14"])
    aprobado = lambda p: isinstance(p, list) and any(x[0] == "concluido" and x[1] == "APROBADO" for x in p)  # noqa: E731
    print("\nVEREDICTO")
    print(f"  paso 2 (publicación configurada): código {rc1} · fila {'concluido / APROBADO' if aprobado(p1) else p1}")
    print("  tras informe.py directo: " + ("REPRODUCIDO: el CSV personalizado sigue en concluido / APROBADO" if aprobado(p2) else "NO SE REPRODUCE: el CSV personalizado ya no presenta la aprobación"))
    print("  tras el relanzamiento configurado: " + ("REPRODUCIDO: el CSV personalizado sigue en concluido / APROBADO" if aprobado(p3) else "NO SE REPRODUCE: el CSV personalizado ya no presenta la aprobación"))
finally:
    shutil.rmtree(tmp, ignore_errors=True)
