#!/usr/bin/env python3
"""Copia limpia: git archive de un árbol + los binarios del manifiesto que no están en Git, copiados de wt_examen con su huella."""
import hashlib, os, shutil, subprocess, sys
repo, arbol, destino, manifiestos = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:]
ORIGEN = "/home/user/e_work/wt_examen/munger_v2_r1"
os.makedirs(destino, exist_ok=False)
p1 = subprocess.Popen(["git", "-C", repo, "archive", arbol, "munger_v2_r1/"], stdout=subprocess.PIPE)
subprocess.run(["tar", "-x", "-C", destino], stdin=p1.stdout, check=True); p1.wait()
assert p1.returncode == 0
raiz = os.path.join(destino, "munger_v2_r1")
en_git = set(subprocess.run(["git", "-C", repo, "ls-tree", "-r", "-z", "--name-only", arbol, "munger_v2_r1/"],
                            capture_output=True, check=True).stdout.decode().split("\0")) - {""}
en_git = {p[len("munger_v2_r1/"):] for p in en_git}
huellas = None
for m in manifiestos:
    d = {}
    texto = subprocess.run(["git", "-C", repo, "show", f"{m}:munger_v2_r1/MANIFIESTO_SHA256.txt"], capture_output=True, check=True).stdout.decode()
    for l in texto.splitlines():
        if l.strip() and not l.startswith("#"):
            h, p = l.split("  ", 1)
            if p not in en_git:
                d[p] = h
    # solo los binarios (rutas que .gitignore excluye de Git); un texto que el manifiesto antiguo listaba y Git ya borró no se copia
    ign = subprocess.run(["git", "-C", repo, "check-ignore", "--no-index", "-z", "--stdin"],
                         input="".join("munger_v2_r1/" + p + "\0" for p in d).encode(), capture_output=True).stdout.decode().split("\0")
    ign = {x[len("munger_v2_r1/"):] for x in ign if x}
    fuera = sorted(set(d) - ign)
    if fuera: print(f"{m}: {len(fuera)} rutas del manifiesto fuera de Git que no son binarios ignorados (no se copian): {fuera}")
    d = {p: h for p, h in d.items() if p in ign}
    if huellas is None: huellas = d
    elif d != huellas: sys.exit(f"los binarios del manifiesto de {m} no coinciden con los de {manifiestos[0]}")
n = 0
for p, h in sorted(huellas.items()):
    o = os.path.join(ORIGEN, p); t = os.path.join(raiz, p)
    if os.path.exists(t): sys.exit(f"ya existe en la copia: {p}")
    os.makedirs(os.path.dirname(t), exist_ok=True)
    shutil.copy2(o, t)
    hh = hashlib.sha256(open(t, "rb").read()).hexdigest()
    if hh != h: sys.exit(f"huella distinta: {p}")
    n += 1
print(f"copia limpia de {arbol} en {raiz}: {len(en_git)} archivos de Git + {n} binarios copiados con su huella (manifiestos {' '.join(manifiestos)})")
