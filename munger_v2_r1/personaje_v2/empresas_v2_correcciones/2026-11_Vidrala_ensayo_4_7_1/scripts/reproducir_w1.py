#!/usr/bin/env python3
"""Reproducción de W-1 (revisión independiente de la 4.7, §1) con el código de un árbol dado. Solo escribe en un temporal.

Uso: python3 -I reproducir_w1.py --raiz <munger_v2_r1 cuyo código se prueba>

Secuencia de la revisión: copia del expediente aprobado de la 4.6.1 con su resumen_v2.csv predeterminado (fila de Vidrala
«concluido / APROBADO» publicada antes del registro de destinos); marcador en fase_c.json → celdas.B101; resumen.py COPIA
OTRO_DESTINO.csv. Se comprueba, sin ninguna llamada posterior, el código, el archivo de las salidas y la fila del predeterminado.
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
a = ap.parse_args()
raiz = os.path.abspath(a.raiz)
exp = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "2026-11_Vidrala_ensayo_4_6_1", "Vidrala")
tmp = tempfile.mkdtemp(prefix="w1_")
try:
    base = os.path.join(tmp, "exp")
    d = os.path.join(base, "Vidrala")
    shutil.copytree(exp, d, ignore=shutil.ignore_patterns(".lo_perfil"))
    for f in ("resumen_v2.csv", "resumen_v2_historial.csv"):
        shutil.copy(os.path.join(os.path.dirname(exp), f), os.path.join(base, f))
    pred = os.path.join(base, "resumen_v2.csv")
    otro = os.path.join(tmp, "OTRO_DESTINO.csv")
    fila = lambda: [r for r in csv.DictReader(open(pred, encoding="utf-8")) if r["empresa"] == "Vidrala, S.A."]
    print(f"código de {raiz}")
    print(f"1. predeterminado antes: {[(r['estado_analisis'], r['verificacion']) for r in fila()]} · registro de destinos: {os.path.exists(os.path.join(d, 'publicaciones_resumen.json'))}")
    fc = json.load(open(os.path.join(d, "fase_c.json"), encoding="utf-8"))
    fc["celdas"]["B101"] += " [MARCADOR W-1]"
    json.dump(fc, open(os.path.join(d, "fase_c.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("2. marcador añadido en fase_c.json → celdas.B101")
    r = subprocess.run([sys.executable, "-B", os.path.join(raiz, "personaje_v2", "scripts", "resumen.py"), d, otro], capture_output=True, text=True,
                       env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
    print(f"3. resumen.py COPIA OTRO_DESTINO.csv → código {r.returncode}")
    print(f"4. archivados: ficha.json {'no' if os.path.exists(os.path.join(d, 'ficha.json')) else 'sí'}, informe.md {'no' if os.path.exists(os.path.join(d, 'informe.md')) else 'sí'}, "
          f"cierre_vigente.json {'no' if os.path.exists(os.path.join(d, 'cierre_vigente.json')) else 'sí'}")
    f = fila()
    print(f"5. predeterminado después (sin ninguna otra llamada): {[(r['estado_analisis'], r['verificacion'][:40]) for r in f]}")
    sigue = any(r["estado_analisis"] == "concluido" and r["verificacion"] == "APROBADO" for r in f)
    print("REPRODUCIDO: la aprobación caducada permanece en el resumen predeterminado" if sigue else "NO SE REPRODUCE: la fila pierde la aprobación en la misma llamada")
finally:
    shutil.rmtree(tmp, ignore_errors=True)
