#!/usr/bin/env python3
"""Productor del ZIP portable del paquete (entrega 4.10, encargo §3.1) y sus partes.

Uso: python3 -I empaquetar_zip.py RAIZ_PADRE ZIP_SALIDA [--partes MiB] [--comprobar DIR_TEMPORAL]
  RAIZ_PADRE: carpeta que contiene munger_v2_r1/ (se empaqueta munger_v2_r1/ completo, sin __pycache__ ni .lo_perfil/).

Incidencia que corrige: el ZIP de la 4.9 guardaba el nombre «n4_paginas_reales_engaños.txt» con bytes UTF-8 pero SIN el indicador
UTF-8 (bit 11 de los indicadores generales) ni un campo Unicode alternativo (0x7075). unzip lo recupera bien; Python zipfile
predeterminado lo interpreta como cp437 y extrae «enga├▒os.txt» (un ausente y un adicional en el manifiesto). Este productor usa
zipfile, que marca con el bit 11 todo nombre que no es ASCII y lo guarda en UTF-8; los bytes de los archivos no cambian (ningún archivo
histórico se renombra). Orden alfabético y fechas de modificación conservadas.

Con --comprobar, extrae el ZIP con Python predeterminado y con unzip en dos carpetas nuevas, comprueba en las dos extracciones el
manifiesto (cero modificados, ausentes y adicionales) y que los dos árboles son idénticos byte a byte, y comprueba en el propio ZIP que
cada nombre no ASCII lleva el indicador. Es la extracción real, no solo el encabezado.
Con --partes N, escribe partes de hasta N MiB (.parte00, .parte01…), su .PARTES.txt con huellas e instrucciones, y el .sha256 del ZIP.
"""
import argparse
import hashlib
import os
import shutil
import subprocess
import sys
import zipfile

EXCLUIR_DIRS = {"__pycache__", ".lo_perfil"}


def sha_archivo(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def construir(padre, salida):
    raiz = os.path.join(padre, "munger_v2_r1")
    entradas = []
    for r, ds, fs in os.walk(raiz):
        ds[:] = sorted(d for d in ds if d not in EXCLUIR_DIRS)
        rel = os.path.relpath(r, padre)
        entradas.append((rel + "/", None))
        for f in sorted(fs):
            entradas.append((os.path.join(rel, f), os.path.join(r, f)))
    with zipfile.ZipFile(salida, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for nombre, ruta in entradas:
            if ruta is None:
                zi = zipfile.ZipInfo.from_file(os.path.join(padre, nombre), nombre)
                z.writestr(zi, b"")
            else:
                z.write(ruta, nombre)
    return len([e for e in entradas if e[1]])


def manifiesto(raiz):
    esp = {}
    for l in open(os.path.join(raiz, "MANIFIESTO_SHA256.txt"), encoding="utf-8"):
        if l.strip() and not l.startswith("#"):
            h, p = l.rstrip("\n").split("  ", 1)
            esp[p] = h
    act = {}
    for r, ds, fs in os.walk(raiz):
        ds[:] = [d for d in ds if d != "__pycache__"]
        for f in fs:
            p = os.path.relpath(os.path.join(r, f), raiz)
            if p != "MANIFIESTO_SHA256.txt":
                act[p] = sha_archivo(os.path.join(raiz, p))
    mod = [p for p in esp if p in act and act[p] != esp[p]]
    falt = [p for p in esp if p not in act]
    extra = [p for p in act if p not in esp]
    return len(esp), mod, falt, extra


def arbol(raiz):
    out = {}
    for r, ds, fs in os.walk(raiz):
        for f in fs:
            p = os.path.join(r, f)
            out[os.path.relpath(p, raiz)] = sha_archivo(p)
    return out


def comprobar(zip_path, tmp):
    res, ok = [], True
    with zipfile.ZipFile(zip_path) as z:
        sin_marca = [i.filename for i in z.infolist() if not i.filename.isascii() and not i.flag_bits & 0x800]
        no_ascii = [i.filename for i in z.infolist() if not i.filename.isascii()]
        malos = z.testzip()
    res.append(f"nombres no ASCII: {len(no_ascii)} · sin indicador UTF-8: {len(sin_marca)} · CRC: {'correcto' if malos is None else 'ERROR en ' + malos}")
    ok &= not sin_marca and malos is None
    dirs = {}
    for lector in ("python", "unzip"):
        d = os.path.join(tmp, f"extraccion_{lector}")
        if os.path.exists(d):
            shutil.rmtree(d)
        os.makedirs(d)
        if lector == "python":
            zipfile.ZipFile(zip_path).extractall(d)
        else:
            subprocess.run(["unzip", "-q", zip_path, "-d", d], check=True)
        n, mod, falt, extra = manifiesto(os.path.join(d, "munger_v2_r1"))
        res.append(f"extracción con {lector}: {n} en el manifiesto · modificados {len(mod)} · ausentes {len(falt)} · adicionales {len(extra)}"
                   + "".join(f"\n    {e}: {p}" for e, l in (("MODIFICADO", mod), ("AUSENTE", falt), ("ADICIONAL", extra)) for p in l[:10]))
        ok &= not (mod or falt or extra)
        dirs[lector] = arbol(d)
    iguales = dirs["python"] == dirs["unzip"]
    res.append(f"árboles extraídos con python y con unzip idénticos byte a byte: {iguales} ({len(dirs['python'])} archivos)")
    ok &= iguales
    nombres = [p for p in dirs["python"] if not p.isascii()]
    res.append("archivos con nombre no ASCII recuperados: " + "; ".join(nombres))
    return ok, res


def partes(zip_path, mib):
    tam = mib * 1024 * 1024
    base = os.path.basename(zip_path)
    lista = []
    with open(zip_path, "rb") as fh:
        i = 0
        while True:
            b = fh.read(tam)
            if not b:
                break
            nombre = f"{zip_path}.parte{i:02d}"
            open(nombre, "wb").write(b)
            lista.append((os.path.basename(nombre), hashlib.sha256(b).hexdigest(), len(b)))
            i += 1
    total = sha_archivo(zip_path)
    open(zip_path + ".sha256", "w", encoding="utf-8").write(f"{total}  {base}\n")
    txt = [f"Partes de {base} (hasta {mib} MiB cada una). SHA-256 del ZIP completo: {total} ({os.path.getsize(zip_path)} bytes).", "",
           "Huellas de las partes:"] + [f"{h}  {n}  ({b} bytes)" for n, h, b in lista] + [
           "", "Reconstrucción (en este orden, sin saltarse ninguna):",
           f"  Linux/macOS:  cat {' '.join(n for n, _, _ in lista)} > {base}",
           f"  Windows (cmd): copy /b {'+'.join(n for n, _, _ in lista)} {base}",
           f"Comprobación: sha256sum {base}  →  {total}"]
    open(zip_path + ".PARTES.txt", "w", encoding="utf-8").write("\n".join(txt) + "\n")
    return lista, total


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("padre")
    ap.add_argument("salida")
    ap.add_argument("--partes", type=int)
    ap.add_argument("--comprobar")
    a = ap.parse_args()
    n = construir(a.padre, a.salida)
    print(f"ZIP {a.salida}: {n} archivos · {os.path.getsize(a.salida)} bytes · SHA-256 {sha_archivo(a.salida)}")
    ok = True
    if a.comprobar:
        ok, res = comprobar(a.salida, a.comprobar)
        print("\n".join(res))
        print("RESULTADO extracción doble:", "PASA" if ok else "FALLA")
    if a.partes:
        lista, total = partes(a.salida, a.partes)
        print(f"{len(lista)} partes de hasta {a.partes} MiB · .PARTES.txt y .sha256 escritos")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
