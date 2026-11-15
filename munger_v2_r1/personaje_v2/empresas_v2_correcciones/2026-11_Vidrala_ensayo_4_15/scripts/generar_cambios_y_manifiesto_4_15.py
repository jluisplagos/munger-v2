#!/usr/bin/env python3
"""Genera CAMBIOS_ARCHIVOS.txt y MANIFIESTO_SHA256.txt de un árbol munger_v2_r1 (entrega 4.15; adaptado del de la 4.14).

Uso: python3 -I generar_cambios_y_manifiesto.py RAIZ_munger_v2_r1 CAMBIOS_ANTERIOR MANIFIESTO_ANTERIOR ETIQUETA [FECHA]
  CAMBIOS_ANTERIOR y MANIFIESTO_ANTERIOR: los de la 4.14 (copias en …_4_15/reproduccion/codigo_4_14/), de los que se reconstruyen las huellas de la
  base original (los modificados con su huella base y los que no cambiaron con la del manifiesto de la 4.14).
CAMBIOS_ARCHIVOS.txt lista, frente a la base original, los modificados (base → nuevo), los nuevos y los eliminados; y además, frente a la
4.14, los cambiados (antes → después), los nuevos y los desaparecidos. MANIFIESTO_SHA256.txt cubre todos los archivos salvo él mismo
(sin __pycache__ ni .lo_perfil/). Se niega a generar si el árbol tiene salidas de pruebas que no van en el paquete (personaje_v2/pruebas/_v64/).
"""
import hashlib
import os
import sys

EXCL_DIRS = {"__pycache__", ".lo_perfil"}
NO_EN_EL_PAQUETE = [os.path.join("personaje_v2", "pruebas", "_v64")]


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


def base_original(cambios, man):
    mod, nuevos, sec, ultimo = {}, set(), None, None
    for l in open(cambios, encoding="utf-8"):
        l = l.rstrip("\n")
        if l.startswith("## MODIFICADOS"):
            sec = "m"
        elif l.startswith("## NUEVOS"):
            sec = "n"
        elif l.startswith("## ELIMINADOS"):
            sec = "e"
        elif l.startswith("## RESPECTO"):
            sec = "r"   # la sección frente a la entrega anterior no describe la base original
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
    for f, h in man.items():
        if f not in mod and f not in nuevos and f not in ("CAMBIOS_ARCHIVOS.txt", "MANIFIESTO_SHA256.txt"):
            base[f] = h
    return base


def main():
    raiz, cambios_ant, man_ant, etiqueta = sys.argv[1:5]
    fecha = sys.argv[5] if len(sys.argv) > 5 else "2026-11-15"
    for d in NO_EN_EL_PAQUETE:
        if os.path.exists(os.path.join(raiz, d)):
            raise SystemExit(f"el árbol tiene {d} (salidas de la batería de la V6.4): bórralo antes de generar el manifiesto")
    m_ant = leer_manifiesto(man_ant)
    base = base_original(cambios_ant, m_ant)
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
    c_ant = sorted(p for p in m_ant if p in act and act[p] != m_ant[p])
    n_ant = sorted(p for p in act if p not in m_ant)
    d_ant = sorted(p for p in m_ant if p not in act and p not in ("CAMBIOS_ARCHIVOS.txt",))
    out = [f"# Archivos cambiados respecto a la base (munger_v2_paquete.zip, SHA-256 61c70800…6af87d). {etiqueta}, generado el {fecha} por "
           "personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_15/scripts/generar_cambios_y_manifiesto_4_15.py.",
           "# No figuran este archivo ni MANIFIESTO_SHA256.txt (se generan al final; el manifiesto cubre todos los archivos, este incluido).",
           f"# Base original reconstruida de los CAMBIOS y el MANIFIESTO de la 4.14: {len(base)} archivos.",
           f"# modificados {len(mod)} · nuevos {len(nue)} · eliminados {len(eli)} · sin cambios {igual}", "", "## MODIFICADOS (SHA-256 base → nuevo)"]
    for p in mod:
        out += [p, f"  {base[p]} → {act[p]}"]
    out += ["", "## NUEVOS (SHA-256)"] + [f"{act[p]}  {p}" for p in nue] + ["", "## ELIMINADOS"] + eli
    out += ["", f"## RESPECTO A LA 4.14 (MANIFIESTO de munger_v2_r1_entrega4.14_cierre_verificacion_entradas.zip, SHA-256 bb51942c…7b93e): "
                f"cambiados {len(c_ant)} · nuevos {len(n_ant)} · desaparecidos {len(d_ant)}",
            "### CAMBIADOS (SHA-256 4.14 → 4.15; CAMBIOS_ARCHIVOS.txt y MANIFIESTO_SHA256.txt se regeneran siempre)"]
    for p in c_ant:
        out += [p, f"  {m_ant[p]} → {act[p]}"]
    out += ["### NUEVOS"] + [f"{act[p]}  {p}" for p in n_ant] + ["### DESAPARECIDOS"] + d_ant
    open(os.path.join(raiz, "CAMBIOS_ARCHIVOS.txt"), "w", encoding="utf-8").write("\n".join(out) + "\n")
    act["CAMBIOS_ARCHIVOS.txt"] = sha(os.path.join(raiz, "CAMBIOS_ARCHIVOS.txt"))
    lineas = [f"# MANIFIESTO SHA-256 · munger_v2_r1 · {etiqueta} · {len(act)} archivos (todos salvo este). Formato: «huella  ruta»."]
    lineas += [f"{act[p]}  {p}" for p in sorted(act)]
    open(os.path.join(raiz, "MANIFIESTO_SHA256.txt"), "w", encoding="utf-8").write("\n".join(lineas) + "\n")
    print(f"base {len(base)} · modificados {len(mod)} · nuevos {len(nue)} · eliminados {len(eli)} · sin cambios {igual} · frente a la 4.14: "
          f"cambiados {len(c_ant)}, nuevos {len(n_ant)}, desaparecidos {len(d_ant)} · manifiesto {len(act)}")


if __name__ == "__main__":
    main()
