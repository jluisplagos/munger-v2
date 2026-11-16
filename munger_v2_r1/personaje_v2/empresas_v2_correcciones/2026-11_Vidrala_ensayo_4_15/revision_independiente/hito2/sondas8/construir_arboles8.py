#!/usr/bin/env python3
"""Octava comprobación (Fable) · árboles ligeros. NUNCA toca el árbol congelado (rev8/munger_v2_r1) ni /home/user/munger-v2 (solo «git archive»/«git show»).
  copia/  = candidata 0a0020b: scripts/, pruebas/ y esquema/ copiados del árbol congelado; el resto, enlaces simbólicos al árbol congelado.
  prev/   = candidata de la séptima comprobación (45ff57c): scripts/, pruebas/ y esquema/ sacados con «git archive»; el resto, enlaces.
Uso: python3 -I -B construir_arboles8.py [nombre ...]   (sin argumentos: copia y prev)"""
import io, os, shutil, subprocess, sys, tarfile
F = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONG = os.path.join(os.path.dirname(F), "munger_v2_r1")
REPO = "/home/user/munger-v2"


def ligero(nombre, fuente_codigo):
    dst = os.path.join(F, nombre, "munger_v2_r1")
    if os.path.lexists(os.path.join(F, nombre)):
        raise SystemExit(f"{nombre} ya existe")
    os.makedirs(os.path.join(dst, "personaje_v2"))
    for x in os.listdir(CONG):
        if x != "personaje_v2":
            os.symlink(os.path.join(CONG, x), os.path.join(dst, x))
    for x in os.listdir(os.path.join(CONG, "personaje_v2")):
        o, n = os.path.join(CONG, "personaje_v2", x), os.path.join(dst, "personaje_v2", x)
        if x in ("scripts", "pruebas", "esquema"):
            fuente_codigo(x, n)
        elif x != ".lo_perfil":
            os.symlink(o, n)
    return dst


def del_congelado(x, n):
    shutil.copytree(os.path.join(CONG, "personaje_v2", x), n, ignore=shutil.ignore_patterns("__pycache__"), symlinks=True)


def de_git(commit):
    def f(x, n):
        pref = f"munger_v2_r1/personaje_v2/{x}"
        tar = subprocess.run(["git", "-C", REPO, "archive", commit, pref], capture_output=True, check=True).stdout
        with tarfile.open(fileobj=io.BytesIO(tar)) as t:
            for m in t.getmembers():
                rel = os.path.relpath(m.name, pref)
                if m.isdir():
                    os.makedirs(os.path.join(n, rel), exist_ok=True)
                elif m.isfile():
                    os.makedirs(os.path.dirname(os.path.join(n, rel)), exist_ok=True)
                    open(os.path.join(n, rel), "wb").write(t.extractfile(m).read())
    return f


if __name__ == "__main__":
    que = sys.argv[1:] or ["copia", "prev"]
    for q in que:
        if q == "prev":
            ligero("prev", de_git("45ff57c"))
        else:
            ligero(q, del_congelado)   # copia, o cualquier otro nombre: código de la candidata, para mutarlo después
    print("hecho:", que)
