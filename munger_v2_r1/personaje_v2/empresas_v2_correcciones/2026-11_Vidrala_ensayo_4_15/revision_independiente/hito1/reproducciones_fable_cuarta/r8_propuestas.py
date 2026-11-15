"""Cuarta pasada · apoyo de las [Propuestas] (no modifica el árbol; solo lectura de los registros reales de la 4.14).
P1 · constantes por su PAPEL, no solo por su valor: un literal (entero 1–12 o potencia de diez) solo como factor o divisor de una
     expresión que contiene un origen, o como decimales de round (0…12); nunca sumado, ni operado con otro literal, ni como argumento.
P2 · dependencia ESTRUCTURAL de cada origen: se evalúa (sin round) en tres puntos genéricos, no en los valores reales; un origen es
     inerte si no cambia el resultado en ninguno. Evita los rechazos falsos por un −1, un cero o el codo de max/min.
P3 · importes: el valor del libro es un redondeo a 3 decimales del resultado EXACTO en cualquiera de los dos sentidos del empate:
     |exacto − libro| ≤ 0,0005 y libro con 3 decimales como mucho.
Se comprueba que las tres aceptan los 148 derivados reales igual que el código vigente y los casos legítimos, y que rechazan los
contraejemplos de r1 y r2 (salvo el que no puede detectarse con una regla sintáctica: cifra compuesta con diferencias de orígenes)."""
import ast, fractions, json, os, random, sys
from fractions import Fraction

PV = os.environ.get("PV", "/tmp/rev_fable4/congelado4/personaje_v2")
sys.path.insert(0, os.path.join(PV, "scripts"))
sys.dont_write_bytecode = True
import verificacion_entradas as VE  # noqa: E402
import fase1_historia as FH  # noqa: E402


# ------------------------------------------------------------------ P1
def _es_o(n):
    return isinstance(n, ast.Subscript) and isinstance(n.value, ast.Name) and n.value.id == "o"


def _tiene_origen(n):
    return any(_es_o(x) for x in ast.walk(n))


def literales_fuera_de_sitio(formula):
    arbol = ast.parse(formula, mode="eval")
    padre = {}
    for n in ast.walk(arbol):
        for h in ast.iter_child_nodes(n):
            padre[id(h)] = n
    mal = []
    for n in ast.walk(arbol):
        if not (isinstance(n, ast.Constant) and isinstance(n.value, (int, float)) and not isinstance(n.value, bool)):
            continue
        v = Fraction(repr(n.value)) if isinstance(n.value, float) else Fraction(n.value)
        nodo, p = n, padre.get(id(n))
        while isinstance(p, ast.UnaryOp):  # el signo forma parte del literal
            nodo, p = p, padre.get(id(p))
        if isinstance(p, ast.Call) and isinstance(p.func, ast.Name) and p.func.id == "round" and len(p.args) == 2 and p.args[1] is nodo:
            if not (nodo is n and v.denominator == 1 and 0 <= v <= 12):
                mal.append((n.value, "decimales de round fuera de 0…12"))
            continue
        valor_ok = (v.denominator == 1 and 1 <= v <= 12) or (v > 0 and any(v == Fraction(10) ** k for k in range(-12, 13)))
        if not valor_ok:
            mal.append((n.value, "valor no admitido"))
        elif isinstance(p, ast.BinOp) and isinstance(p.op, ast.Mult) and _tiene_origen(p.right if p.left is nodo else p.left):
            pass
        elif isinstance(p, ast.BinOp) and isinstance(p.op, ast.Div) and p.right is nodo and _tiene_origen(p.left):
            pass
        else:
            mal.append((n.value, "no es factor ni divisor de una expresión con un origen"))
    return mal


# ------------------------------------------------------------------ P2
def inertes_estructurales(formula, origenes, semilla=415, puntos=3):
    rnd = random.Random(semilla)

    def generico():
        return Fraction(rnd.randint(-10 ** 9, 10 ** 9), rnd.randint(1, 10 ** 6))
    vivos = set()
    for _ in range(puntos):
        vals = {o: generico() for o in origenes}
        try:
            base = VE._eval_formula_exacta(formula, vals, sin_redondeo=True)
        except ZeroDivisionError:
            continue
        for o in origenes:
            try:
                if VE._eval_formula_exacta(formula, dict(vals, **{o: generico()}), sin_redondeo=True) != base:
                    vivos.add(o)
            except ZeroDivisionError:
                vivos.add(o)
    return [o for o in dict.fromkeys(origenes) if o not in vivos]


def inertes_vigente(formula, vals):
    base = VE._eval_formula_exacta(formula, vals, sin_redondeo=True)
    out = []
    for o in vals:
        v_o = VE._frac(vals[o])
        pert = dict(vals, **{o: v_o * (1 + Fraction(1, 10 ** 7)) + Fraction(1, 10 ** 7)})
        if VE._eval_formula_exacta(formula, pert, sin_redondeo=True) == base:
            out.append(o)
    return out


# ------------------------------------------------------------------ P3
def importe_exacto(r_ex, vm):
    fv = VE._frac(vm)
    return (fv * 1000).denominator == 1 and abs(r_ex - fv) <= Fraction(1, 2000) or VE._igual_exacto(float(r_ex), vm)


print("árbol:", PV)
print("\n=== 1 · los 148 derivados reales de la 4.14 con las tres propuestas")
E414 = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_14")
tot = p1 = p2 = 0
for exp in ("viscofan_decisiones/Viscofan", "vidrala_decisiones/Vidrala", "elis_decisiones/Elis"):
    reg = json.load(open(os.path.join(E414, exp, "verificacion_entradas.json"), encoding="utf-8"))
    por = {e["celda"]: e for e in reg["entradas"]}
    for e in reg["entradas"]:
        if e.get("clase") != "derivado":
            continue
        d = e["derivacion"]
        tot += 1
        m1 = literales_fuera_de_sitio(d["formula"]); m2 = inertes_estructurales(d["formula"], d["origenes"])
        p1 += bool(m1); p2 += bool(m2)
        if m1 or m2:
            print("   ", exp, e["celda"], d["formula"][:70], m1, m2)
print(f"   {tot} derivados reales · con literales fuera de sitio (P1): {p1} · con orígenes estructuralmente inertes (P2): {p2}")

print("\n=== 2 · P1 y P2 sobre fórmulas legítimas y sobre los contraejemplos")
Y = {c: f"Historia!{c}5" for c in "CDEFHL"}
CASOS = [
    ("legítima: media de tres", '(o["a"] + o["b"] + o["c"]) / 3', {"a": 1.5, "b": 2.5, "c": 3.5}),
    ("legítima: cambio de unidad", '(o["a"] - o["b"]) / 1000000', {"a": 46500000.0, "b": 1020791.0}),
    ("legítima: ratio redondeado", 'round(o["a"] / o["b"], 4)', {"a": 17.784, "b": 176.254}),
    ("legítima: cambio de signo", '-(o["a"] + o["b"]) * -1 * 100 / 100', {"a": 1.5, "b": 2.5}),
    ("legítima con un origen −1", 'o["a"] + o["b"]', {"a": 850.697, "b": -1.0}),
    ("legítima: producto con un cero", 'o["a"] * o["b"]', {"a": 0.25, "b": 0.0}),
    ("legítima: 0 / d", 'o["a"] / o["b"]', {"a": 0.0, "b": 190.537}),
    ("legítima: max de dos partidas", 'max(o["a"], o["b"])', {"a": 849.697, "b": 100.25}),
    ("T2 de la tercera: o[x] * 0 + cifra", 'o["a"] * 0 + 849.697', {"a": 2019}),
    ("T2 de la tercera: o[x] − o[x] + o[y]", 'o["a"] - o["a"] + o["b"]', {"a": 2019, "b": 849.697}),
    ("nuevo: año − cifra compuesta", 'o["a"] - (1*1000 + 1*100 + 6*10 + 9 + 3/10 + 3/1000)', {"a": 2019}),
    ("nuevo: cifra compuesta + max(año, año compuesto) − año compuesto (codo de max)", '(8*100 + 4*10 + 9 + 6/10 + 9/100 + 7/1000) + max(o["a"], (2*1000 + 1*10 + 9)) - (2*1000 + 1*10 + 9)', {"a": 2019}),
    ("nuevo: cifra compuesta + abs(año − año compuesto)", '(8*100 + 4*10 + 9 + 6/10 + 9/100 + 7/1000) + abs(o["a"] - (2*1000 + 1*10 + 9))', {"a": 2019}),
    ("nuevo: cifra compuesta + round(año, -9)", '(8*100 + 4*10 + 9 + 6/10 + 9/100 + 7/1000) + round(o["a"], -9)', {"a": 2019}),
    ("nuevo: año × cifra compuesta ÷ año compuesto ÷ 1000", 'o["a"] * (8*100000 + 4*10000 + 9*1000 + 6*100 + 9*10 + 7) / (2*1000 + 1*10 + 9) / 1000', {"a": 2019}),
    ("nuevo: abs(a, b) (segundo argumento ignorado)", 'abs(o["a"], o["b"])', {"a": -1.5, "b": 2.5}),
    ("nuevo: round(x, 999999999999)", 'round(o["a"], 999999999999)', {"a": 849.697}),
    ("LÍMITE (no detectable): dígitos = diferencias entre años de la Historia", f'(o["{Y["L"]}"] - o["{Y["D"]}"]) * 100 + (o["{Y["L"]}"] - o["{Y["H"]}"]) * 10 + (o["{Y["L"]}"] - o["{Y["C"]}"]) '
     f'+ (o["{Y["L"]}"] - o["{Y["F"]}"]) / 10 + (o["{Y["L"]}"] - o["{Y["C"]}"]) / 100 + (o["{Y["L"]}"] - o["{Y["E"]}"]) / 1000', {Y[c]: 2016 + "CDEFGHIJKL".index(c) for c in "CDEFHL"}),
]
for rot, formula, vals in CASOS:
    try:
        vig_c = VE._constantes_no_admitidas(formula)
        vig_i = inertes_vigente(formula, vals) if "999999999999" not in formula else "(no se evalúa: no termina)"
    except Exception as ex:  # noqa: BLE001
        vig_c, vig_i = f"{type(ex).__name__}", "—"
    m1 = literales_fuera_de_sitio(formula)
    m2 = inertes_estructurales(formula, list(vals)) if "999999999999" not in formula else "(no se evalúa)"
    print(f"   [{rot}] vigente: {'RECHAZA' if (vig_c or (vig_i and not isinstance(vig_i, str))) else 'acepta'} (constantes {vig_c}; inertes {vig_i}) · "
          f"propuesta: {'RECHAZA' if (m1 or (m2 and not isinstance(m2, str))) else 'acepta'} (P1 {[x[0] for x in m1]}; P2 {m2})")

print("\n=== 3 · P3 (importes): el valor del generador del paquete para medias de n valores con 3 decimales, y los contraejemplos de T1")
random.seed(415)
for n_anios in (2, 3, 4, 6):
    rech_v = rech_p = 0
    for _ in range(20000):
        vals = [round(random.uniform(1, 2000), 3) for _ in range(n_anios)]
        anios = list(range(2026 - n_anios, 2026))
        gen = FH.calcular_entrada("C46", {"calculo": {"operacion": "media", "anios": anios, "terminos": [{"partida": "cfo", "signo": 1}], "redondeo": 3}}, {"cfo": vals}, anios)["valor"]
        ex = sum(VE._frac(v) for v in vals) / n_anios
        rech_v += not VE._igual_libro(float(ex), gen)
        rech_p += not importe_exacto(ex, gen)
    print(f"   media de {n_anios}: rechazados con la regla vigente (_igual_libro sobre el float del exacto) {rech_v} de 20000 · con P3 {rech_p}")
for rot, ex, vm in (("849,0 frente a 849,697", Fraction(849), 849.697), ("849,6974 frente a 849,697 (redondeo legítimo)", Fraction("849.6974"), 849.697), ("849,6976 frente a 849,697", Fraction("849.6976"), 849.697),
                    ("849,6975 (empate) frente a 849,697", Fraction("849.6975"), 849.697), ("849,6975 (empate) frente a 849,698", Fraction("849.6975"), 849.698),
                    ("849,6974 frente a 849,6972 (el libro no tiene 3 decimales)", Fraction("849.6974"), 849.6972), ("0,2511 frente a 0,25", Fraction("0.2511"), 0.25)):
    print(f"   [{rot}] vigente: {'acepta' if VE._igual_libro(float(ex), vm) else 'rechaza'} · P3: {'acepta' if importe_exacto(ex, vm) else 'rechaza'}")
