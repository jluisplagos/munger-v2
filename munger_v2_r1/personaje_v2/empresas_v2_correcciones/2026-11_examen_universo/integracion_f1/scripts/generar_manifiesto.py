#!/usr/bin/env python3
"""Manifiesto SHA-256 de una copia limpia (todos los archivos salvo el propio manifiesto, orden por ruta, formato «huella  ruta»)."""
import hashlib, os, sys
raiz, cabecera, salida = sys.argv[1], sys.argv[2], sys.argv[3]
filas = []
for r, ds, fs in os.walk(raiz):
    ds[:] = [d for d in ds if d != "__pycache__"]
    for f in fs:
        p = os.path.relpath(os.path.join(r, f), raiz)
        if p != "MANIFIESTO_SHA256.txt":
            filas.append((p, hashlib.sha256(open(os.path.join(raiz, p), "rb").read()).hexdigest()))
filas.sort()
with open(salida, "w", encoding="utf-8", newline="\n") as s:
    s.write(cabecera.replace("{N}", str(len(filas))) + "\n")
    for p, h in filas:
        s.write(f"{h}  {p}\n")
print(f"{len(filas)} archivos")
