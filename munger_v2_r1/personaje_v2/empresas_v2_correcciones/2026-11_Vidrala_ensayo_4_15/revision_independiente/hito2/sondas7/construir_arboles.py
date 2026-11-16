#!/usr/bin/env python3
"""Séptima comprobación (Fable) · árboles ligeros. NUNCA toca el árbol congelado (rev7/munger_v2_r1) ni /home/user/munger-v2 (solo «git archive»/«git show»).
  copia/  = candidata 45ff57c: scripts/, pruebas/ y esquema/ copiados del árbol congelado; el resto, enlaces simbólicos al árbol congelado.
  prev/   = candidata de la sexta comprobación (8196522): scripts/, pruebas/ y esquema/ sacados con «git archive»; el resto, enlaces.
  c876/   = solo scripts/verificacion_entradas.py de 876bfc2 (candidata de la quinta), con «git show».
Uso: python3 -I -B construir_arboles.py"""
import io, os, shutil, subprocess, tarfile
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
    ligero("copia", del_congelado)
    ligero("prev", de_git("8196522"))
    os.makedirs(os.path.join(F, "c876", "scripts"))
    open(os.path.join(F, "c876", "scripts", "verificacion_entradas.py"), "wb").write(
        subprocess.run(["git", "-C", REPO, "show", "876bfc2:munger_v2_r1/personaje_v2/scripts/verificacion_entradas.py"], capture_output=True, check=True).stdout)
    print("hecho")
