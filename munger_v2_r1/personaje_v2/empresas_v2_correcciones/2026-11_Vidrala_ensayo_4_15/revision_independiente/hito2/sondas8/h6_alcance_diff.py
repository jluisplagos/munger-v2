#!/usr/bin/env python3
"""h6 · octava comprobación · ALCANCE del cambio de código entre 45ff57c y 0a0020b (git, solo lectura; y el árbol congelado).
 1. archivos que cambian en todo el repositorio, clasificados; ninguno de código fuera de los cinco esperados;
 2. por archivo de código: líneas quitadas y puestas, y comparación por árbol sintáctico (qué funciones o sentencias cambian);
 3. verificar_paquete.sh: solo «61» → «62» en tres líneas.
Uso: python3 -I -B h6_alcance_diff.py"""
import ast, difflib, hashlib, os, re, subprocess, sys
REPO = "/home/user/munger-v2"
F = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONG = os.path.join(os.path.dirname(F), "munger_v2_r1")
A, B = "45ff57c", "0a0020b"
ok_todo = True


def dicho(ok, t):
    global ok_todo
    ok_todo = ok_todo and bool(ok)
    print(("   CONFORME     " if ok else "   NO CONFORME  ") + t)


def git(*a):
    return subprocess.run(["git", "-C", REPO, *a], capture_output=True, check=True).stdout.decode("utf-8")


print("1 · archivos que cambian entre", A, "y", B)
ns = [l.split("\t") for l in git("diff", "--name-status", A, B).strip().split("\n")]
ESPERADOS = {"munger_v2_r1/personaje_v2/scripts/verificacion_entradas.py", "munger_v2_r1/personaje_v2/scripts/fase1_historia.py",
             "munger_v2_r1/personaje_v2/pruebas/test_verificacion_entradas_415.py", "munger_v2_r1/personaje_v2/pruebas/test_entrada_efectiva_415.py",
             "munger_v2_r1/verificar_paquete.sh"}
clases = {}
for est, ruta in ns:
    if ruta in ESPERADOS:
        c = "código esperado"
    elif "/revision_independiente/hito2/" in ruta:
        c = "informe, sondas y salidas de la séptima comprobación"
    elif "/hito2/resultados/" in ruta:
        c = "resultados (regresión de 45ff57c y reconstrucción de C48)"
    elif ruta.endswith((".md", "VERSION", "MANIFIESTO_SHA256.txt", "CAMBIOS_ARCHIVOS.txt")):
        c = "registro y empaquetado"
    else:
        c = "OTRO"
    clases.setdefault(c, []).append((est, ruta))
for c, l in sorted(clases.items()):
    print(f"   {c}: {len(l)}" + ("" if len(l) > 12 else " · " + ", ".join(f"{e} {os.path.basename(r)}" for e, r in l)))
cod = [r for e, r in ns if re.search(r"\.(py|sh|json|xlsx|xml|txt)$", r) and "/revision_independiente/" not in r and "/resultados/" not in r
       and not r.endswith(("MANIFIESTO_SHA256.txt", "CAMBIOS_ARCHIVOS.txt"))]
dicho(set(cod) == ESPERADOS and "OTRO" not in clases, f"archivos de código, esquema, configuración o datos que cambian fuera de revisión/resultados: {len(cod)} (los cinco esperados: {set(cod) == ESPERADOS})")
dicho(not [r for e, r in ns if e != "M" and r in ESPERADOS] and not [r for e, r in ns if e == "D"], "ningún archivo borrado; los cinco de código, modificados (no añadidos)")
for d in ("munger_v2_r1/personaje_v2/esquema", "munger_v2_r1/v6", "munger_v2_r1/kit_pipeline_munger", "munger_v2_r1/contrastes", "munger_v2_r1/personaje_v2/empresas_v2",
          "munger_v2_r1/personaje_v2/prompts", "munger_v2_r1/personaje_v2/corpus", "tools", "docs"):
    n = len([1 for e, r in ns if r.startswith(d + "/")])
    if n:
        dicho(False, f"cambia {d}/: {n} archivos")
print("   (sin cambios en esquema/, v6/, kit_pipeline_munger/, contrastes/, empresas_v2/, prompts/, corpus/, tools/ ni docs/)")

print("\n2 · por archivo")
for ruta in sorted(ESPERADOS):
    a, b = git("show", f"{A}:{ruta}"), git("show", f"{B}:{ruta}")
    cong = open(os.path.join(CONG, ruta.split("/", 1)[1]), encoding="utf-8").read()
    la, lb = a.split("\n"), b.split("\n")
    ops = [o for o in difflib.SequenceMatcher(None, la, lb, autojunk=False).get_opcodes() if o[0] != "equal"]
    quita, pone = sum(o[2] - o[1] for o in ops), sum(o[4] - o[3] for o in ops)
    print(f"   {ruta.split('/', 1)[1]}: −{quita} +{pone} líneas en {len(ops)} tramos (líneas nuevas {[f'{o[3] + 1}-{o[4]}' for o in ops]}) · árbol congelado == {B}: {cong == b} · sha256 {hashlib.sha256(b.encode()).hexdigest()[:16]}…")
    if ruta.endswith(".py"):
        ta, tb = ast.parse(a), ast.parse(b)
        da = {getattr(n, "name", None) or f"sentencia@{i}": ast.dump(n) for i, n in enumerate(ta.body)}
        # sentencias de primer nivel que difieren (por posición), con su nombre o su primera línea
        dif = []
        if len(ta.body) != len(tb.body):
            # alinear por contenido: sentencias de b que no están en a, y viceversa
            sa, sb = [ast.dump(n) for n in ta.body], [ast.dump(n) for n in tb.body]
            dif = [f"+ línea {n.lineno}: {b.split(chr(10))[n.lineno - 1].strip()[:60]}" for n, s in zip(tb.body, sb) if s not in sa] + \
                  [f"− línea {n.lineno}: {a.split(chr(10))[n.lineno - 1].strip()[:60]}" for n, s in zip(ta.body, sa) if s not in sb]
        else:
            for x, y in zip(ta.body, tb.body):
                if ast.dump(x) != ast.dump(y):
                    dif.append(f"línea {y.lineno}: {getattr(y, 'name', None) or b.split(chr(10))[y.lineno - 1].strip()[:70]}")
        print(f"      sentencias de primer nivel distintas (árbol sintáctico): {len(dif)}")
        for d in dif:
            print("        ", d)
print("\n3 · verificar_paquete.sh")
a, b = git("show", f"{A}:munger_v2_r1/verificar_paquete.sh").split("\n"), git("show", f"{B}:munger_v2_r1/verificar_paquete.sh").split("\n")
dif = [(i + 1, x, y) for i, (x, y) in enumerate(zip(a, b)) if x != y]
dicho(len(a) == len(b) and len(dif) == 3 and all(x.replace("61", "62") == y and x.count("61") == 1 for _i, x, y in dif), f"cambian {len(dif)} líneas ({[d[0] for d in dif]}), y en cada una solo «61» → «62»")
for i, x, y in dif:
    print(f"      {i}: …{y.strip()[:150]}")
print("\nRESULTADO:", "CONFORME" if ok_todo else "NO CONFORME")
sys.exit(0 if ok_todo else 1)
