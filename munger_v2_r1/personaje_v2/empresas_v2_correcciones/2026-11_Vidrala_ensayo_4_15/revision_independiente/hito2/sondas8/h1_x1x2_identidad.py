#!/usr/bin/env python3
"""Octava comprobación · X1/X2: lo aplicado es EXACTAMENTE lo que propuso la séptima.
 1. huella de verificacion_entradas.py del árbol congelado = 4b00aa2a…a98c86cd;
 2. los archivos del árbol congelado (verificacion_entradas.py y test_verificacion_entradas_415.py) son byte a byte los del árbol de la
    corrección propuesta por la séptima (rev7/fable/fix7), que solo se lee;
 3. independiente del estado de rev7/fable: se aplican las sustituciones de sondas7/propuestas7.py (PRUEBAS y CODIGO, tal como están en el
    árbol congelado; se cargan sin ejecutar su «main») a los dos archivos de 45ff57c sacados de git («git show», solo lectura) y el
    resultado es byte a byte el del árbol congelado;
 4. entre 45ff57c y el árbol, en verificacion_entradas.py cambia UN carácter de UNA línea.
Uso: python3 -I -B h1_x1x2_identidad.py"""
import ast, difflib, hashlib, os, subprocess, sys
sys.dont_write_bytecode = True
AQUI = os.path.dirname(os.path.abspath(__file__))
F = os.path.dirname(AQUI)
S = os.path.dirname(os.path.dirname(F))
CONG = os.path.join(os.path.dirname(F), "munger_v2_r1")
FIX7 = os.path.join(S, "rev7", "fable", "fix7", "munger_v2_r1")
PROP = os.path.join(CONG, "personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_15/revision_independiente/hito2/sondas7/propuestas7.py")
REPO = "/home/user/munger-v2"
ok_todo = True


def dicho(ok, t):
    global ok_todo
    ok_todo = ok_todo and bool(ok)
    print(("   CONFORME     " if ok else "   NO CONFORME  ") + t)


def h(b):
    return hashlib.sha256(b).hexdigest()


def git(commit, rel):
    return subprocess.run(["git", "-C", REPO, "show", f"{commit}:munger_v2_r1/personaje_v2/{rel}"], capture_output=True, check=True).stdout


VEP, T415 = "scripts/verificacion_entradas.py", "pruebas/test_verificacion_entradas_415.py"
cong = {r: open(os.path.join(CONG, "personaje_v2", r), "rb").read() for r in (VEP, T415)}
print("1 · huella")
dicho(h(cong[VEP]) == "4b00aa2a42ae45743ef4f31669faad36a7effb81affe828fd4975a2ca98c86cd", f"verificacion_entradas.py del árbol: {h(cong[VEP])}")
print(f"   (informativo) test_verificacion_entradas_415.py del árbol: {h(cong[T415])}")

print("2 · frente al árbol de la corrección propuesta por la séptima (rev7/fable/fix7, solo lectura)")
for r in (VEP, T415):
    p = os.path.join(FIX7, "personaje_v2", r)
    if os.path.exists(p):
        b = open(p, "rb").read()
        dicho(b == cong[r], f"{r}: {'idéntico byte a byte' if b == cong[r] else 'DISTINTO'} (fix7 {h(b)[:16]}…)")
    else:
        dicho(False, f"{r}: no está en fix7")

print("3 · las sustituciones de sondas7/propuestas7.py aplicadas a 45ff57c (git show) dan el archivo del árbol")
src = open(PROP, encoding="utf-8").read()
# solo las asignaciones de constantes del módulo (PRUEBAS, CODIGO, T415, VEP): se evalúan sin ejecutar el «main» ni «construir»
arbol = ast.parse(src)
ns = {}
for nodo in arbol.body:
    if isinstance(nodo, ast.Assign) and all(isinstance(t, (ast.Name, ast.Tuple)) for t in nodo.targets):
        nombres = [n.id for t in nodo.targets for n in ast.walk(t) if isinstance(n, ast.Name)]
        if set(nombres) & {"PRUEBAS", "CODIGO", "T415", "VEP"}:
            exec(compile(ast.Module([nodo], []), "propuestas7", "exec"), ns)
    elif isinstance(nodo, ast.Expr) and isinstance(nodo.value, ast.Call) and getattr(getattr(nodo.value.func, "value", None), "id", "") == "PRUEBAS":
        exec(compile(ast.Module([nodo], []), "propuestas7", "exec"), ns)   # PRUEBAS.append(...)
print(f"   propuestas7.py: {len(ns['PRUEBAS'])} sustituciones de pruebas y {len(ns['CODIGO'])} de código")
base = {r: git("45ff57c", r).decode("utf-8") for r in (VEP, T415)}
assert h(base[VEP].encode()).startswith("7abbb081")
res = dict(base)
for arch, viejo, nuevo in ns["PRUEBAS"] + ns["CODIGO"]:
    assert res[arch].count(viejo) == 1, (arch, viejo[:60], res[arch].count(viejo))
    res[arch] = res[arch].replace(viejo, nuevo)
for r in (VEP, T415):
    dicho(res[r].encode("utf-8") == cong[r], f"{r}: 45ff57c + propuestas7 {'=' if res[r].encode('utf-8') == cong[r] else '≠'} árbol congelado")

print("4 · qué cambia en verificacion_entradas.py entre 45ff57c y el árbol")
a, b = base[VEP].split("\n"), cong[VEP].decode("utf-8").split("\n")
dif = [(i + 1, x, y) for i, (x, y) in enumerate(zip(a, b)) if x != y]
dicho(len(a) == len(b) and len(dif) == 1, f"líneas distintas: {[d[0] for d in dif]} (mismo número de líneas: {len(a) == len(b)})")
for n, x, y in dif:
    ops = [(t, x[i1:i2], y[j1:j2]) for t, i1, i2, j1, j2 in difflib.SequenceMatcher(None, x, y, autojunk=False).get_opcodes() if t != "equal"]
    dicho(ops == [("insert", "", "'")], f"línea {n}: operaciones {ops} (se espera una sola inserción del apóstrofo ASCII)")
    print("     antes:  ", x.strip()[:110])
    print("     después:", y.strip()[:110])
print("\nRESULTADO:", "CONFORME" if ok_todo else "NO CONFORME")
sys.exit(0 if ok_todo else 1)
