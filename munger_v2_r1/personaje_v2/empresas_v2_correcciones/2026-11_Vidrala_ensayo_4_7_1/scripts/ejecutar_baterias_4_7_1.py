#!/usr/bin/env python3
"""Ejecuta las baterías de la 4.7.1 en copias temporales del árbol y guarda sus salidas, con las huellas del código de cada copia.

Uso: python3 -I ejecutar_baterias_4_7_1.py [--todas] [--solo-comprobar]

- `test_resumen_v2.py` con el código actual, con el de la 4.7 (`reproduccion/codigo_4_7/`) y con el que vio la auditoría interna
  (`reproduccion/codigo_auditado_4_7_1/`, con `pipeline.py` de la 4.7, que entonces no había cambiado). Siempre la batería actual.
- Con `--todas`, además `test_cierre_v2.py` y `test_pipeline_sintetico.py` con el código actual (unos 6 minutos).
- Con `--solo-comprobar` no escribe nada: devuelve 0 si las salidas obtenidas coinciden con las conservadas (estado de cada prueba,
  resumen final y huellas del código), lo que usa `comprobar_entrega_4_7_1.py`.

Nunca se ejecuta en el árbol real: las baterías escriben (perfiles de LibreOffice, temporales) y aquí solo se escribe en copias.
"""
import argparse
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile

AQUI = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", "..", ".."))
REP = os.path.join(AQUI, "reproduccion")
CODIGO = ["personaje_v2/scripts/cierre_v2.py", "personaje_v2/scripts/ficha.py", "personaje_v2/scripts/informe.py", "personaje_v2/scripts/pipeline.py",
          "personaje_v2/scripts/resumen.py", "verificar_paquete.sh", "personaje_v2/pruebas/test_resumen_v2.py"]
ENV = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def huellas(raiz):
    return "# código: " + " · ".join(f"{os.path.basename(p)} {sha(os.path.join(raiz, p))[:16]}" for p in CODIGO)


def copia(sustituir=None):
    tmp = tempfile.mkdtemp(prefix="bat471_")
    dst = os.path.join(tmp, "munger_v2_r1")
    shutil.copytree(RAIZ, dst, symlinks=True, ignore=shutil.ignore_patterns("__pycache__", ".lo_perfil"))
    for nombre, origen in (sustituir or {}).items():
        shutil.copy(origen, os.path.join(dst, "personaje_v2", "scripts", nombre))
    return tmp, dst


def ejecutar(prueba, sustituir=None):
    tmp, dst = copia(sustituir)
    try:
        r = subprocess.run([sys.executable, "-B", os.path.join("pruebas", prueba)], cwd=os.path.join(dst, "personaje_v2"), capture_output=True, text=True, env=ENV)
        return huellas(dst) + "\n" + (r.stdout + r.stderr).strip() + "\n", r.returncode
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def firma(txt):
    """Lo que debe coincidir entre dos ejecuciones: las huellas, el estado de cada prueba (en orden), el principio de las que fallan y la línea final."""
    lineas = txt.splitlines()
    estados = [l[:5] for l in lineas if l.startswith(("PASA ", "FALLA"))]
    fallos = [l[:90] for l in lineas if l.startswith("FALLA")]
    final = [l for l in lineas if re.match(r"^\d+/\d+ pruebas", l)]
    return lineas[0], estados, fallos, final[-1:] if final else []


CASOS = {
    "resultados/test_resumen_v2_salida.txt": ("test_resumen_v2.py", None),
    "reproduccion/pruebas_resumen_con_codigo_4_7.txt": ("test_resumen_v2.py", {f"{n}.py": os.path.join(REP, "codigo_4_7", f"{n}.py.txt") for n in ("cierre_v2", "ficha", "resumen", "pipeline")}),
    "reproduccion/pruebas_resumen_con_codigo_auditado.txt": ("test_resumen_v2.py", {**{f"{n}.py": os.path.join(REP, "codigo_auditado_4_7_1", f"{n}.py.txt") for n in ("cierre_v2", "ficha", "resumen")},
                                                                                   "pipeline.py": os.path.join(REP, "codigo_4_7", "pipeline.py.txt")}),
}
LARGAS = {"resultados/test_cierre_v2_salida.txt": ("test_cierre_v2.py", None), "resultados/test_pipeline_sintetico_salida.txt": ("test_pipeline_sintetico.py", None)}

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--todas", action="store_true")
    ap.add_argument("--solo-comprobar", action="store_true")
    a = ap.parse_args()
    casos = {**CASOS, **(LARGAS if a.todas else {})}
    distintos = 0
    for destino, (prueba, sust) in casos.items():
        txt, rc = ejecutar(prueba, sust)
        f = firma(txt)
        print(f"{destino}: {prueba} · código {rc} · {f[3][0] if f[3] else 'sin línea final'} · {len(f[2])} en FALLA")
        if a.solo_comprobar:
            ok = os.path.exists(os.path.join(AQUI, destino)) and firma(open(os.path.join(AQUI, destino), encoding="utf-8").read()) == f
            distintos += not ok
            print(f"  {'coincide con la conservada' if ok else 'NO COINCIDE con la conservada'}")
        else:
            open(os.path.join(AQUI, destino), "w", encoding="utf-8").write(txt)
    sys.exit(1 if distintos else 0)
