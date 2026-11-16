#!/usr/bin/env python3
"""x5a · octava comprobación · X5: `fase1_historia.importe_completo` de 0a0020b frente al de 45ff57c, a nivel de unidad.
 A. las dos expresiones, leídas del código;
 B. los casos de g11 (séptima) y más: qué cierra;
 C. MONOTONÍA, exhaustiva: sobre todos los textos de hasta 6 caracteres de un alfabeto de 9 símbolos y 10 importes, el código nuevo
    nunca dice True donde el anterior decía False (no abre nada); y donde difieren, el texto lleva un apóstrofo pegado a una cifra;
    sin apóstrofo en el texto, los dos códigos coinciden siempre;
 D. cierre: en números bien formados con miles con apóstrofo (ASCII o «’»), ningún trozo numérico propio vale como importe completo
    y el número entero sí;
 E. costes prudentes: «cifra + apóstrofo + cifra» que no es un separador de miles.
Uso: python3 -I -B x5a_importe_completo_unidad.py"""
import itertools, os, random, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # con -I el directorio de la sonda no entra solo en sys.path
from comun8 import FN, FO, ACT, ANT, P_FN, P_FO  # noqa: E402

ok_todo = True


def dicho(ok, t):
    global ok_todo
    ok_todo = ok_todo and bool(ok)
    print(("   CONFORME     " if ok else "   NO CONFORME  ") + t)


print("A · las expresiones")
for et, p in ((ANT, P_FO), (ACT, P_FN)):
    src = open(p, encoding="utf-8").read().split("\n")
    l = next(x for x in src if "re.search(" in x and "re.escape(imp)" in x)
    print(f"   {et:20} {l.strip()}")
print("   usos (0a0020b):", [f":{i + 1}" for i, x in enumerate(open(P_FN, encoding='utf-8').read().split(chr(10))) if "importe_completo(" in x and not x.startswith("def ")])

print("\nB · casos (importe, texto) → anterior / nuevo; «esperado» = lo que debe dar un control de importe completo")
T = "’"
CASOS = [  # (imp, texto, esperado, nota)
    ("849,7", "Total 1.849,7", False, "trozo con punto (ya rechazado)"), ("849,7", "Total 1,849,7", False, "trozo con coma (ya rechazado)"),
    ("7", "Total 7,608", False, "trozo por delante (ya rechazado)"), ("849,7", "Total 849,7", True, "control"),
    ("849,7", "Total 1'849,7", False, "X5: detrás de apóstrofo ASCII"), ("849,7", f"Total 1{T}849,7", False, "X5: detrás de «’»"),
    ("849", "Total 849'697", False, "X5: delante de apóstrofo ASCII"), ("849", f"Total 849{T}697", False, "X5: delante de «’»"),
    ("234", "Total 1'234'567", False, "X5: entre dos apóstrofos"), ("567", "Total 1'234'567", False, "X5: último grupo"),
    ("1", "Total 1'234'567", False, "X5: primer grupo"), ("234'567", "Total 1'234'567", False, "X5: cola con apóstrofo"),
    ("1'234", "Total 1'234'567", False, "X5: cabeza con apóstrofo"), ("849,7", "Total 1'849,7 1'702,3", False, "X5: dos columnas"),
    ("702,3", "Total 1'849,7 1'702,3", False, "X5: segunda columna"), ("849,7", "Total (1'849,7)", False, "X5: entre paréntesis"),
    ("849,7", "Total -1'849,7", False, "X5: negativo"), ("849", "Total 849'697.50", False, "X5: con decimales detrás"),
    ("697", f"Total 849{T}697", False, "X5: cola con «’»"), ("849,7", f"Total 12{T}849,7 y 849,7", True, "el trozo y además suelto: vale el suelto"),
    ("1'849,7", "Total 1'849,7", True, "control: el número entero con apóstrofo"), ("849'697", "Total 849'697", True, "control: entero"),
    (f"1{T}849,7", f"Total 1{T}849,7", True, "control: entero con «’»"), ("1'234'567", "Total 1'234'567", True, "control: entero, dos apóstrofos"),
    ("849,7", f"Ventas SBF 120{T}s 849,7", True, "control: posesivo en la línea"), ("120", f"Ventas SBF 120{T}s 849,7", True, "control: cifra + ’ + letra"),
    ("1,5", f"taux d{T}1,5 %", True, "control: letra + ’ + cifra"), ("2023", f"l{T}exercice 2023", True, "control: francés"),
    ("849,7", "Total 1 849,7", None, "miles con espacio: límite conocido, sin cambio (acepta)"),
    ("849,7", "Total 1 849,7", None, "miles con espacio duro: lo mismo tras norm() (acepta)"),
    ("849,7", "Total 1ʼ849,7", None, "«ʼ» U+02BC: no cuenta (acepta; resto de W3)"), ("849,7", "Total 1′849,7", None, "«′» U+2032: no cuenta (acepta)"),
    ("849,7", "Total 1´849,7", None, "«´» U+00B4: no cuenta (acepta)"), ("849,7", "Total 1`849,7", None, "«`»: no cuenta (acepta)"),
    ("849,7", "Total 1‘849,7", None, "«‘» U+2018: no cuenta (acepta)"),
]
cierra = abre = 0
for imp, texto, esp, nota in CASOS:
    a, n = FO.importe_completo(FO.norm(imp), FO.norm(texto)), FN.importe_completo(FN.norm(imp), FN.norm(texto))
    marca = ""
    if esp is not None and n != esp:
        marca = "   <<< NO es lo esperado"
        dicho(False, f"{imp!r} en {texto!r}: nuevo {n}, esperado {esp}")
    if a and not n:
        cierra += 1
    if n and not a:
        abre += 1
    print(f"   {imp!r:12} en {texto!r:30} anterior={a!s:5} nuevo={n!s:5} {'CAMBIA' if a != n else '      '} · {nota}{marca}")
dicho(abre == 0, f"ningún caso pasa de False a True · pasan de True a False (lo que cierra): {cierra}")

print("\nC · monotonía, exhaustiva")
ALF = ["1", "8", ",", ".", "'", T, " ", "a", "("]
IMPS = ["8", "18", "1", "8,1", "1.8", "81", "1'8", f"8{T}1", "8'", "'8"]
ro = {i: re.compile(r"(?<![\d.,])" + re.escape(i) + r"(?![\d.,]*\d)") for i in IMPS}
rn = {i: re.compile(r"(?<![\d.,])(?<!\d['’])" + re.escape(i) + r"(?![\d.,'’]*\d)") for i in IMPS}
# las expresiones precompiladas son las del código: se comprueba con una muestra contra las funciones
rnd = random.Random(8)
for _ in range(20000):
    t = "".join(rnd.choice(ALF) for _ in range(rnd.randint(0, 9)))
    i = rnd.choice(IMPS)
    assert (ro[i].search(t) is not None) == FO.importe_completo(i, t) and (rn[i].search(t) is not None) == FN.importe_completo(i, t)
n_tot = n_dif = n_abre = n_dif_sin_apo = n_sin_explicar = 0
ejemplos = []
adj = re.compile(r"\d['’]|['’][\d.,'’]*\d")
for L in range(0, 7):
    for tup in itertools.product(ALF, repeat=L):
        t = "".join(tup)
        apo = ("'" in t) or (T in t)
        for i in IMPS:
            if i not in t:
                continue
            n_tot += 1
            a, n = ro[i].search(t) is not None, rn[i].search(t) is not None
            if a != n:
                n_dif += 1
                if n and not a:
                    n_abre += 1
                if not apo:
                    n_dif_sin_apo += 1
                if not adj.search(t):
                    n_sin_explicar += 1
                if len(ejemplos) < 6 and L >= 5:
                    ejemplos.append((i, t))
print(f"   pares (importe presente en el texto) examinados: {n_tot:,} · difieren: {n_dif:,}")
dicho(n_abre == 0, f"el código nuevo NUNCA acepta lo que el anterior rechazaba: {n_abre} casos de False→True")
dicho(n_dif_sin_apo == 0, f"sin apóstrofo en el texto los dos códigos coinciden siempre: {n_dif_sin_apo} diferencias")
dicho(n_sin_explicar == 0, f"toda diferencia tiene un apóstrofo pegado a una cifra («cifra+apóstrofo» o «apóstrofo+…cifra»): {n_sin_explicar} sin explicar")
print("   ejemplos de True→False:", ejemplos)

print("\nD · cierre en números bien formados con miles con apóstrofo")
rnd = random.Random(15)
n_num = n_frag = n_frag_acept_ant = n_frag_acept_nue = n_entero_mal = 0
malos = []
for _ in range(4000):
    ap = rnd.choice(["'", T])
    grupos = [str(rnd.randint(1, 999))] + [f"{rnd.randint(0, 999):03d}" for _ in range(rnd.randint(1, 3))]
    dec = rnd.choice(["", "", f",{rnd.randint(0, 99):02d}", f".{rnd.randint(0, 9)}"])
    num = ap.join(grupos) + dec
    texto = rnd.choice(["Total ", "Ventas CHF ", "Revenue (", "Capex -", ""]) + num + rnd.choice(["", " millones", ")", " 12", " CHF"])
    texto = FN.norm(texto)
    n_num += 1
    if not FN.importe_completo(num, texto):
        n_entero_mal += 1
    # trozos propios que empiezan y acaban en cifra y son un número para numero() (lo que un extractor podría dar como «impreso»)
    vistos = set()
    for i in range(len(num)):
        for j in range(i + 1, len(num) + 1):
            fr = num[i:j]
            if fr == num or fr in vistos or not (fr[0].isdigit() and fr[-1].isdigit()):
                continue
            vistos.add(fr)
            # ¿aparece el trozo además como número suelto en el texto (p. ej. el « 12» añadido)? entonces no es el caso
            resto = texto.replace(num, "#")
            if re.search(r"(?<![\d.,'’])" + re.escape(fr) + r"(?![\d.,'’])", resto):
                continue
            n_frag += 1
            n_frag_acept_ant += FO.importe_completo(fr, texto)
            if FN.importe_completo(fr, texto):
                n_frag_acept_nue += 1
                if len(malos) < 8:
                    malos.append((fr, texto))
print(f"   números generados: {n_num:,} · trozos propios (empiezan y acaban en cifra, no sueltos en la línea): {n_frag:,}")
print(f"   trozos que el código ANTERIOR aceptaba como importe completo: {n_frag_acept_ant:,}")
dicho(n_frag_acept_nue == 0, f"trozos que el código NUEVO acepta: {n_frag_acept_nue}" + (f" · {malos}" if malos else ""))
dicho(n_entero_mal == 0, f"el número entero se reconoce siempre como importe completo (fallos: {n_entero_mal})")

print("\nE · costes prudentes: «cifra + apóstrofo + cifra» que NO es un separador de miles (anterior → nuevo)")
COSTES = [("24", "Ventas Q1'24 crecen"), ("24", f"Ventas Q1{T}24 crecen"), ("30", "Tiempo 5'30"), ("5", "sube 2'5 puntos"), ("2", "sube 2'5 puntos"),
          ("2030", f"the ‘Vision 2030{T}1 plan"), ("849", "Nota '2023'849"), ("24", f"9M{T}24 849,7"), ("849,7", f"9M{T}24 849,7"),
          ("24", f"H1{T}24: 24 tiendas"), ("24", f"FY{T}24"), ("120", f"SBF 120{T}s"), ("1,5", f"d{T}1,5 %"), ("2023", f"l{T}exercice 2023"),
          ("849", "849' 697"), ("849", "849'a"), ("849", "'849"), ("849", f"{T}849{T}"), ("849", "1' 849"), ("849", "849,'5"), ("849", "849'.5")]
for imp, texto in COSTES:
    a, n = FO.importe_completo(FO.norm(imp), FO.norm(texto)), FN.importe_completo(FN.norm(imp), FN.norm(texto))
    print(f"   {imp!r:8} en {texto!r:30} anterior={a!s:5} nuevo={n!s:5} {'RECHAZO NUEVO (prudente)' if a and not n else ''}")
print("\nRESULTADO:", "CONFORME" if ok_todo else "NO CONFORME")
sys.exit(0 if ok_todo else 1)
