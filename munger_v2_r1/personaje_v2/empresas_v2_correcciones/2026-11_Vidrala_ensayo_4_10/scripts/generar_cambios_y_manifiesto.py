#!/usr/bin/env python3
"""Genera CAMBIOS_ARCHIVOS.txt y MANIFIESTO_SHA256.txt de un árbol munger_v2_r1 (entrega 4.10).

Uso: python3 -I generar_cambios_y_manifiesto.py RAIZ_munger_v2_r1 CAMBIOS_4_9 MANIFIESTO_4_9 ETIQUETA
  CAMBIOS_4_9 y MANIFIESTO_4_9: los de la 4.9 (reproduccion/), de los que se reconstruyen las huellas de la base original
  (676 archivos: los modificados con su huella base y los que no cambiaron con la del manifiesto de la 4.9).
CAMBIOS_ARCHIVOS.txt lista, frente a la base original, los modificados (base → nuevo), los nuevos y los eliminados; y además, frente a la
4.9, los cambiados (antes → después) y los nuevos. MANIFIESTO_SHA256.txt cubre todos los archivos salvo él mismo (sin __pycache__).
"""
import hashlib
import os
import sys

EXCL_DIRS = {"__pycache__", ".lo_perfil"}


def sha(p):
    with open(p, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def leer_manifiesto(p):
    d = {}
    for l in open(p, encoding="utf-8"):
        if l.strip() and not l.startswith("#"):
            h, f = l.rstrip("\n").split("  ", 1)
            d[f] = h
    return d


def base_original(cambios49, m49):
    mod, nuevos, sec, ultimo = {}, set(), None, None
    for l in open(cambios49, encoding="utf-8"):
        l = l.rstrip("\n")
        if l.startswith("## MODIFICADOS"):
            sec = "m"
        elif l.startswith("## NUEVOS"):
            sec = "n"
        elif l.startswith("## ELIMINADOS"):
            sec = "e"
        elif l.startswith("#") or not l.strip():
            continue
        elif sec == "m":
            if l.startswith("  ") and "→" in l:
                mod[ultimo] = l.strip().split(" → ")[0]
            else:
                ultimo = l
        elif sec == "n":
            nuevos.add(l.split("  ", 1)[1] if "  " in l else l)
    base = dict(mod)
    for f, h in m49.items():
        if f not in mod and f not in nuevos and f not in ("CAMBIOS_ARCHIVOS.txt", "MANIFIESTO_SHA256.txt"):
            base[f] = h
    return base


def main():
    raiz, cambios49, man49, etiqueta = sys.argv[1:5]
    m49 = leer_manifiesto(man49)
    base = base_original(cambios49, m49)
    act = {}
    for r, ds, fs in os.walk(raiz):
        ds[:] = [d for d in ds if d not in EXCL_DIRS]
        for f in fs:
            p = os.path.relpath(os.path.join(r, f), raiz)
            if p not in ("MANIFIESTO_SHA256.txt", "CAMBIOS_ARCHIVOS.txt"):
                act[p] = sha(os.path.join(raiz, p))
    mod = sorted(p for p in base if p in act and act[p] != base[p])
    nue = sorted(p for p in act if p not in base)
    eli = sorted(p for p in base if p not in act)
    igual = len([p for p in base if p in act and act[p] == base[p]])
    c49 = sorted(p for p in m49 if p in act and act[p] != m49[p])
    n49 = sorted(p for p in act if p not in m49)
    out = [f"# Archivos cambiados respecto a la base (munger_v2_paquete.zip, SHA-256 61c70800…6af87d). {etiqueta}, generado el 2026-11-11 por "
           "personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_10/scripts/generar_cambios_y_manifiesto.py.",
           "# No figuran este archivo ni MANIFIESTO_SHA256.txt (se generan al final; el manifiesto cubre todos los archivos, este incluido).",
           f"# Base original reconstruida de los CAMBIOS y el MANIFIESTO de la 4.9: {len(base)} archivos.",
           f"# modificados {len(mod)} · nuevos {len(nue)} · eliminados {len(eli)} · sin cambios {igual}", "", "## MODIFICADOS (SHA-256 base → nuevo)"]
    for p in mod:
        out += [p, f"  {base[p]} → {act[p]}"]
    out += ["", "## NUEVOS (SHA-256)"] + [f"{act[p]}  {p}" for p in nue] + ["", "## ELIMINADOS"] + eli
    out += ["", f"## RESPECTO A LA 4.9 (MANIFIESTO de munger_v2_r1_entrega4.9_integridad_auditoria_y_N4.zip, SHA-256 8a481589…2ea5): "
                f"cambiados {len(c49)} · nuevos {len(n49)} · desaparecidos {len([p for p in m49 if p not in act and p not in ('CAMBIOS_ARCHIVOS.txt',)])}",
            "### CAMBIADOS (SHA-256 4.9 → 4.10; CAMBIOS_ARCHIVOS.txt y MANIFIESTO_SHA256.txt se regeneran siempre)"]
    for p in c49:
        out += [p, f"  {m49[p]} → {act[p]}"]
    out += ["### NUEVOS"] + [f"{act[p]}  {p}" for p in n49]
    open(os.path.join(raiz, "CAMBIOS_ARCHIVOS.txt"), "w", encoding="utf-8").write("\n".join(out) + "\n")
    act["CAMBIOS_ARCHIVOS.txt"] = sha(os.path.join(raiz, "CAMBIOS_ARCHIVOS.txt"))
    lineas = [f"# MANIFIESTO SHA-256 · munger_v2_r1 · {etiqueta} · {len(act)} archivos (todos salvo este). Formato: «huella  ruta»."]
    lineas += [f"{act[p]}  {p}" for p in sorted(act)]
    open(os.path.join(raiz, "MANIFIESTO_SHA256.txt"), "w", encoding="utf-8").write("\n".join(lineas) + "\n")
    print(f"base {len(base)} · modificados {len(mod)} · nuevos {len(nue)} · eliminados {len(eli)} · sin cambios {igual} · frente a la 4.9: cambiados {len(c49)}, nuevos {len(n49)} · manifiesto {len(act)}")


if __name__ == "__main__":
    main()
