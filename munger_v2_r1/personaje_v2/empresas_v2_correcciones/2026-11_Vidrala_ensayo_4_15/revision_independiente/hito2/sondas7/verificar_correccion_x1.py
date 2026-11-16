#!/usr/bin/env python3
"""Séptima comprobación · VERIFICACIÓN MECÁNICA de la corrección de X1 y X2 sobre un árbol dado (segundos; solo lee el árbol; no lanza nada).
Uso: python3 -I -B verificar_correccion_x1.py <ruta a …/munger_v2_r1 de la candidata corregida>
Comprueba, y termina con código 0 solo si todo es conforme:
 1. CÓDIGO · `personaje_v2/scripts/verificacion_entradas.py` es EL MISMO PROGRAMA que el que esta comprobación ha probado (la candidata
    45ff57c con un carácter más en la línea :542): mismo árbol sintáctico (los comentarios no cuentan). Informa además de si la huella del
    archivo es exactamente la esperada (4b00aa2a…a98c86cd), que solo coincide si tampoco se ha tocado ningún comentario.
 2. X1 · los casos de la cita localizada cuyo valor es un trozo de un número con apóstrofo (ASCII o «’») dan «ausente» y los controles
    de la cifra entera dan «ok».
 3. PRUEBAS (X2) · el bloque «(hito 2, quinta comprobación, V1–V7 …)» de `pruebas/test_verificacion_entradas_415.py` del árbol:
    (a) pasa entero con el código del árbol; (b) FALLA con el código de 45ff57c (es decir, vería X1); (c) detecta las seis variantes de
    la línea :542 (sin apóstrofo, solo ASCII o solo «’», por delante y por detrás) aplicadas al código del árbol.
No sustituye a las tres baterías ni a la regresión completa."""
import ast, hashlib, os, subprocess, sys, time, types
AQUI = os.path.dirname(os.path.abspath(__file__))
F = os.path.dirname(AQUI)
ARBOL = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.join(F, "fix7", "munger_v2_r1")
REL_VE, REL_T = "personaje_v2/scripts/verificacion_entradas.py", "personaje_v2/pruebas/test_verificacion_entradas_415.py"
H_ESPERADA = "4b00aa2a42ae45743ef4f31669faad36a7effb81affe828fd4975a2ca98c86cd"
sys.dont_write_bytecode = True
os.environ["PATH"] = os.path.join(F, "bin") + os.pathsep + os.environ.get("PATH", "")
ok_todo = True


def dicho(ok, texto):
    global ok_todo
    ok_todo = ok_todo and bool(ok)
    print(("   CONFORME     " if ok else "   NO CONFORME  ") + texto)


def modulo(src, nombre, ruta_scripts):
    m = types.ModuleType(nombre)
    m.__file__ = os.path.join(ruta_scripts, "verificacion_entradas.py")
    antes = list(sys.path)
    sys.path.insert(0, ruta_scripts)
    exec(compile(src, nombre + ".py", "exec"), m.__dict__)
    sys.path[:] = antes
    return m


S_ARBOL = open(os.path.join(ARBOL, REL_VE), encoding="utf-8").read()
P_CAND = os.path.join(F, "copia", "munger_v2_r1", REL_VE)   # 45ff57c (copia del árbol congelado); si no está, se saca de git (solo lectura)
if os.path.exists(P_CAND):
    S_CAND = open(P_CAND, encoding="utf-8").read()
else:
    S_CAND = subprocess.run(["git", "-C", os.environ.get("REPO", "/home/user/munger-v2"), "show", "45ff57c:munger_v2_r1/" + REL_VE], capture_output=True, check=True).stdout.decode("utf-8")
assert hashlib.sha256(S_CAND.encode("utf-8")).hexdigest().startswith("7abbb081"), "la copia de 45ff57c no es la esperada"
L_CAND = next(l for l in S_CAND.split("\n") if "re.escape(c)" in l and "for m in re.finditer" in l)
INI_C, INI_OK = r"""(?<![\d.,])(?<!\d[’])" + re.escape(c)""", r"""(?<![\d.,])(?<!\d['’])" + re.escape(c)"""
assert L_CAND.count(INI_C) == 1
S_REF = S_CAND.replace(L_CAND, L_CAND.replace(INI_C, INI_OK))   # 45ff57c con el carácter repuesto: lo que esta comprobación ha probado
assert hashlib.sha256(S_REF.encode("utf-8")).hexdigest() == H_ESPERADA
print(f"árbol: {ARBOL}")

print("\n1 · código")
h = hashlib.sha256(S_ARBOL.encode("utf-8")).hexdigest()
mismo = ast.dump(ast.parse(S_ARBOL)) == ast.dump(ast.parse(S_REF))
dicho(mismo, "verificacion_entradas.py es el mismo programa (árbol sintáctico) que 45ff57c con el carácter repuesto en :542")
print(f"   (informativo) SHA-256 del archivo: {h} · {'ES la huella esperada: ni un comentario de más' if h == H_ESPERADA else 'no es 4b00aa2a…a98c86cd: cambia algún comentario o algo más (véase la línea anterior)'}")
if not mismo:
    ta, tb = ast.parse(S_ARBOL), ast.parse(S_REF)
    dif = sorted({x.lineno for x, y in zip(ast.walk(ta), ast.walk(tb)) if isinstance(x, ast.Constant) and isinstance(y, ast.Constant) and x.value != y.value})
    print(f"   constantes distintas en las líneas {dif or '(la estructura difiere)'} del archivo del árbol · ¿es 45ff57c sin corregir?: {ast.dump(ast.parse(S_ARBOL)) == ast.dump(ast.parse(S_CAND))}")

RS = os.path.join(ARBOL, "personaje_v2", "scripts")
VA = modulo(S_ARBOL, "ve_arbol", RS)
VC = modulo(S_CAND, "ve_45ff57c", RS)   # sus importaciones internas, de los scripts del árbol (entre 45ff57c y la corrección solo cambia este archivo)

print("\n2 · X1: la cifra de detrás de un apóstrofo ASCII, con la cita localizada")
CASOS = [("Total 1'849,7", "Total 1'849,7", 849.7), ("Total 1'849,7", "1'849,7", 849.7), ("Total 1'234'567", "Total 1'234'567", 567), ("Total 1'234'567", "Total 1'234'567", 234567),
         ("Total 1'234'567", "Total 1'234'567", 234), ("Total 1'849.7", "Total 1'849.7", 849.7), ("Empleados 12'345", "Empleados 12'345", 345),
         ("Resultado -1'849,7", "Resultado -1'849,7", 849.7), ("Resultado -1'849,7", "Resultado -1'849,7", -849.7), ("Resultado (1'849,7)", "Resultado (1'849,7)", 849.7),
         ("Resultado (1'849,7)", "Resultado (1'849,7)", -849.7), ("Ventas CHF 1'849,7 millones", "Ventas CHF 1'849,7 millones", 849.7),
         ("Ventas 1'849,7 1'702,3", "Ventas 1'849,7 1'702,3", 702.3), ("Total de 1'849,7 millones", "de 1'849,7", 849.7),
         ("Total 1’849,7", "Total 1’849,7", 849.7), ("Total 849’697", "Total 849’697", 849), ("Total 849'697", "Total 849'697", 849)]
r = {(p, c, v): VA._cita_cifra(c, v, p + "\n")[0] for p, c, v in CASOS}
mal = {k: e for k, e in r.items() if e != "ausente"}
dicho(not mal, f"los {len(CASOS)} casos del trozo de un número con apóstrofo dan «ausente»" + (f" · NO: {mal}" if mal else ""))
rc = {(p, c, v): VC._cita_cifra(c, v, p + "\n")[0] for p, c, v in CASOS}
print(f"   (informativo) con el código de 45ff57c dan «ok» {sum(e == 'ok' for e in rc.values())} de esos {len(CASOS)}")
CTRL = [("Total 1'849.7", 1849.7), ("Total 849'697", 849697), ("Total 1'234'567", 1234567), ("Total 849,7", 849.7), ("Otros 849,7\nTotal 1'849,7", 849.7)]
rk = {(p, v): VA._cita_cifra(p.split("\n")[0], v, p + "\n")[0] for p, v in CTRL}
dicho(all(e == "ok" for e in rk.values()), f"los {len(CTRL)} controles de la cifra entera dan «ok»" + ("" if all(e == "ok" for e in rk.values()) else f" · NO: {rk}"))

print("\n3 · pruebas (X2): el bloque de test_verificacion_entradas_415.py del árbol")
T = open(os.path.join(ARBOL, REL_T), encoding="utf-8").read()
ini = T.index("# (hito 2, quinta comprobación, V1–V7 y pruebas de V4)")
fin = T.index("r = con()\npaso(\"RW\", \"el control positivo sigue apto después de los casos RW\"", ini)
BLOQUE = T[ini:fin]


def bloque(mod):
    res = []
    exec(compile(BLOQUE, "bloque_del_arbol", "exec"), {"VE": mod, "paso": lambda b, n, ok, det=None: res.append((n, bool(ok), det)), "_time": time})
    return res


ra = bloque(VA)
dicho(all(ok for _n, ok, _d in ra), f"(a) con el código del árbol pasan {sum(ok for _n, ok, _d in ra)} de {len(ra)} pruebas del bloque" + "".join(f" · FALLA {n[:40]}: {str(d)[:120]}" for n, ok, d in ra if not ok))
rcn = bloque(VC)
fallan = [(n, d) for n, ok, d in rcn if not ok]
dicho(bool(fallan), "(b) con el código de 45ff57c (X1 sin corregir) el bloque FALLA" + (f": {fallan[0][0][:9]} · {str(fallan[0][1])[:110]}" if fallan else " — NO: las pruebas del árbol no ven X1"))
L_A = next((l for l in S_ARBOL.split("\n") if "re.escape(c)" in l and "for m in re.finditer" in l), None)
FIN_OK = r"""(?!\d|[.,'’]\d)", t)"""
if L_A and L_A.count(INI_OK) == 1 and L_A.count(FIN_OK) == 1:
    VAR = {"sin apóstrofo por delante": L_A.replace(INI_OK, r"""(?<![\d.,])" + re.escape(c)"""), "solo ASCII por delante": L_A.replace(INI_OK, r"""(?<![\d.,])(?<!\d')" + re.escape(c)"""),
           "solo «’» por delante (= 45ff57c)": L_A.replace(INI_OK, INI_C), "sin apóstrofo por detrás": L_A.replace(FIN_OK, r"""(?!\d|[.,]\d)", t)"""),
           "solo ASCII por detrás": L_A.replace(FIN_OK, r"""(?!\d|[.,']\d)", t)"""), "solo «’» por detrás": L_A.replace(FIN_OK, r"""(?!\d|[.,’]\d)", t)""")}
    sin = [n for n, l in VAR.items() if all(ok for _n, ok, _d in bloque(modulo(S_ARBOL.replace(L_A, l), "ve_var", RS)))]
    dicho(not sin, f"(c) las seis variantes de la línea :542 se detectan" + (f" — NO se detectan: {sin}" if sin else ""))
else:
    dicho(False, "(c) la línea :542 del árbol no tiene la forma corregida: no se pueden aplicar las variantes")

print("\nRESULTADO:", "CONFORME (código y pruebas de X1/X2; faltan las tres baterías y la regresión completa)" if ok_todo else "NO CONFORME")
sys.exit(0 if ok_todo else 1)
