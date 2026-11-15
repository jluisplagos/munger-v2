#!/usr/bin/env python3
"""Paquete pequeño de cambios para la revisión externa (4.15; encargo correctivo §7): solo los archivos cambiados y nuevos frente a la base
4.14, con sus rutas y huellas, y un manifiesto ligado a la base. Aplicado sobre una descompresión limpia de la 4.14, reproduce el árbol
de la entrega (se comprueba con --comprobar contra su MANIFIESTO_SHA256.txt completo).

Uso: python3 -I empaquetar_cambios_4_15.py RAIZ_munger_v2_r1 MANIFIESTO_4_14 ZIP_SALIDA ETIQUETA [--comprobar ZIP_BASE_4_14 DIR_TEMPORAL]
Contenido del ZIP: munger_v2_r1/<rutas> de los archivos cambiados y nuevos (también CAMBIOS_ARCHIVOS.txt y MANIFIESTO_SHA256.txt) y, en la
raíz, MANIFIESTO_CAMBIOS.txt: base (ZIP 4.14 y su SHA-256), cada archivo con su estado (cambiado/nuevo), su huella 4.14 y la nueva, y
la lista de desaparecidos (debe estar vacía). Nombres UTF-8 marcados (zipfile); orden alfabético.
(4.15, hito 2; revisión externa del hito 1, discrepancia del empaquetado) MANIFIESTO_SHA256.txt no se lista a sí mismo: no es ni
«cambiado» ni «nuevo» frente a las entradas del manifiesto 4.14, sino el manifiesto SUSTITUIDO, y va en su propia sección (con la huella
del manifiesto 4.14 de partida). En el hito 1 se contaba en los dos grupos (13 cambiados y 207 nuevos, por 12 y 206).
"""
import argparse
import hashlib
import os
import shutil
import subprocess
import sys
import zipfile

BASE_ZIP = "munger_v2_r1_entrega4.14_cierre_verificacion_entradas.zip"
BASE_SHA = "bb51942cefb848e409a4828e3faeb70f94aa4d29af39cda6d90cd0a97cb7b93e"
EXCL = {"__pycache__", ".lo_perfil"}


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def leer_manifiesto(p):
    d = {}
    for l in open(p, encoding="utf-8"):
        if l.strip() and not l.startswith("#"):
            h, f = l.rstrip("\n").split("  ", 1)
            d[f] = h
    return d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("raiz"); ap.add_argument("manifiesto_base"); ap.add_argument("zip"); ap.add_argument("etiqueta")
    ap.add_argument("--comprobar", nargs=2, metavar=("ZIP_BASE", "TMP"))
    a = ap.parse_args()
    base = leer_manifiesto(a.manifiesto_base)
    act = {}
    for r, ds, fs in os.walk(a.raiz):
        ds[:] = [d for d in ds if d not in EXCL]
        for f in fs:
            p = os.path.relpath(os.path.join(r, f), a.raiz)
            act[p] = sha(os.path.join(a.raiz, p))
    base_sin = {k: v for k, v in base.items()}
    MAN = "MANIFIESTO_SHA256.txt"
    cambiados = sorted(p for p in act if p in base_sin and act[p] != base_sin[p] and p != MAN)
    nuevos = sorted(p for p in act if p not in base_sin and p != MAN)
    desap = sorted(p for p in base_sin if p not in act and p != MAN)
    sustituido = MAN in act
    lineas = [f"# MANIFIESTO DE CAMBIOS · munger_v2_r1 · {a.etiqueta}",
              f"# Base: {BASE_ZIP} · SHA-256 {BASE_SHA}",
              "# Aplicación: descomprimir la base en una carpeta nueva y vacía; descomprimir este ZIP encima (sobrescribe los cambiados y añade",
              "# los nuevos); desde munger_v2_r1/: `sha256sum -c` de MANIFIESTO_SHA256.txt (sin su primera línea) → todos OK y ningún archivo de más.",
              f"# cambiados {len(cambiados)} · nuevos {len(nuevos)} · desaparecidos {len(desap)} (entradas del manifiesto 4.14)"
              + (" · y el propio MANIFIESTO_SHA256.txt, sustituido (no figura en ningún otro grupo)" if sustituido else ""), "",
              "## CAMBIADOS (SHA-256 4.14 → nuevo · ruta)"]
    lineas += [f"{base_sin.get(p, '—')} → {act[p]}  {p}" for p in sorted(cambiados)]
    lineas += ["", "## NUEVOS (SHA-256 · ruta)"] + [f"{act[p]}  {p}" for p in nuevos]
    lineas += ["", "## DESAPARECIDOS"] + desap
    lineas += ["", "## MANIFIESTO SUSTITUIDO (SHA-256 del manifiesto 4.14 de partida → nuevo)"] + ([f"{sha(a.manifiesto_base)} → {act[MAN]}  {MAN}"] if sustituido else [])
    texto = "\n".join(lineas) + "\n"
    with zipfile.ZipFile(a.zip, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("MANIFIESTO_CAMBIOS.txt", texto)
        for p in sorted(set(cambiados) | set(nuevos) | ({MAN} if sustituido else set())):
            z.write(os.path.join(a.raiz, p), os.path.join("munger_v2_r1", p))
    print(f"{a.zip}: cambiados {len(cambiados)} · nuevos {len(nuevos)} · desaparecidos {len(desap)}" + (" · manifiesto sustituido" if sustituido else "")
          + f" · SHA-256 {sha(a.zip)}")
    if desap:
        print("AVISO: hay archivos desaparecidos frente a la base")
    if a.comprobar:
        zb, tmp = a.comprobar
        if os.path.exists(tmp):
            raise SystemExit(f"{tmp} ya existe: hace falta una carpeta nueva")
        os.makedirs(tmp)
        try:
            if sha(zb) != BASE_SHA:
                raise SystemExit("el ZIP base no es el de la 4.14")
            subprocess.run(["unzip", "-q", zb, "-d", tmp], check=True)
            with zipfile.ZipFile(a.zip) as z:
                for n in z.namelist():
                    if n.startswith("munger_v2_r1/"):
                        z.extract(n, tmp)
            r = os.path.join(tmp, "munger_v2_r1")
            man = leer_manifiesto(os.path.join(r, "MANIFIESTO_SHA256.txt"))
            todos = {}
            for rr, ds, fs in os.walk(r):
                ds[:] = [d for d in ds if d not in EXCL]
                for f in fs:
                    p = os.path.relpath(os.path.join(rr, f), r)
                    if p != "MANIFIESTO_SHA256.txt":
                        todos[p] = sha(os.path.join(r, p))
            mod = [p for p in man if p in todos and todos[p] != man[p]]
            aus = [p for p in man if p not in todos]
            mas = [p for p in todos if p not in man]
            print(f"comprobación (base 4.14 + cambios): manifiesto {len(man)} · modificados {len(mod)} · ausentes {len(aus)} · de más {len(mas)}")
            if mod or aus or mas:
                print(mod[:5], aus[:5], mas[:5])
                sys.exit(1)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
