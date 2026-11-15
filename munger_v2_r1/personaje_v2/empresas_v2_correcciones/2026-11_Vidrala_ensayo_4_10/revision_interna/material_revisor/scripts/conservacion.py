"""Revisión interna 4.10: MANIFIESTO_4_9 frente al árbol (copia de revisión) y frente al MANIFIESTO 4.10; árbol frente a MANIFIESTO 4.10."""
import hashlib, os, sys
arbol, m49, m410 = sys.argv[1:4]
def leer(p):
    d = {}
    for l in open(p, encoding="utf-8"):
        if l.startswith("#") or not l.strip(): continue
        h, r = l.rstrip("\n").split("  ", 1); d[r] = h
    return d
A, B = leer(m49), leer(m410)
def sha(p):
    with open(p, "rb") as f: return hashlib.sha256(f.read()).hexdigest()
mod, aus = [], []
for r, h in A.items():
    p = os.path.join(arbol, r)
    if not os.path.isfile(p): aus.append(r)
    elif sha(p) != h: mod.append(r)
print(f"4.9: {len(A)} entradas · cambiadas en el árbol 4.10: {len(mod)} · ausentes: {len(aus)}")
for r in mod: print("  CAMBIADO", r)
for r in aus: print("  AUSENTE", r)
# árbol frente al manifiesto 4.10
reales = set()
for raiz, ds, fs in os.walk(arbol):
    for f in fs:
        reales.add(os.path.relpath(os.path.join(raiz, f), arbol))
reales.discard("MANIFIESTO_SHA256.txt")
m_mod = [r for r in B if r in reales and sha(os.path.join(arbol, r)) != B[r]]
print(f"4.10: {len(B)} entradas · árbol {len(reales)} archivos · modificados {len(m_mod)} · ausentes {len(set(B) - reales)} · adicionales {len(reales - set(B))}")
for r in m_mod: print("  MOD", r)
for r in sorted(set(B) - reales): print("  AUS", r)
for r in sorted(reales - set(B))[:20]: print("  ADIC", r)
nuevos = sorted(set(B) - set(A))
print(f"nuevos en 4.10 respecto a 4.9: {len(nuevos)}")
fuera = [r for r in nuevos if "2026-11_Vidrala_ensayo_4_10" not in r]
for r in fuera: print("  NUEVO FUERA DEL EXPEDIENTE", r)
