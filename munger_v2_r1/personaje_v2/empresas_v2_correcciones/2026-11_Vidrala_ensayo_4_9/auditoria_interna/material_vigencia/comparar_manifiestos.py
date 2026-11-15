# Compara el árbol de la copia con MANIFIESTO_SHA256.txt y con MANIFIESTO_4_8_1.txt
import os, sys, hashlib
R = "/home/claude/vigencia_4_9/munger_v2_r1"
E = "personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_9"
def leer(p):
    d = {}
    for l in open(p, encoding="utf-8"):
        if l.startswith("#") or not l.strip(): continue
        h, r = l.rstrip("\n").split("  ", 1); d[r] = h
    return d
def h(p):
    return hashlib.sha256(open(os.path.join(R, p), "rb").read()).hexdigest()
arbol = {}
for dp, dn, fn in os.walk(R):
    dn[:] = [x for x in dn if x != "__pycache__"]
    for f in fn:
        p = os.path.relpath(os.path.join(dp, f), R); arbol[p] = h(p)
m = leer(os.path.join(R, "MANIFIESTO_SHA256.txt"))
print("árbol (sin __pycache__):", len(arbol), "· manifiesto:", len(m))
a = set(arbol) - {"MANIFIESTO_SHA256.txt"}
print("en árbol y no en manifiesto:", sorted(a - set(m)))
print("en manifiesto y no en árbol:", sorted(set(m) - a))
print("huella distinta:", sorted(p for p in a & set(m) if arbol[p] != m[p]))
m481 = leer(os.path.join(R, E, "reproduccion/MANIFIESTO_4_8_1.txt"))
print("\nmanifiesto 4.8.1:", len(m481))
mod = sorted(p for p in set(m481) & set(arbol) if arbol[p] != m481[p])
aus = sorted(set(m481) - set(arbol))
nue = sorted(set(arbol) - set(m481))
print("MODIFICADOS frente a 4.8.1:", len(mod)); [print("  ", p) for p in mod]
print("AUSENTES frente a 4.8.1:", aus)
print("NUEVOS frente a 4.8.1:", len(nue))
print("  nuevos fuera del expediente 4.9:", [p for p in nue if not p.startswith(E + "/")])
