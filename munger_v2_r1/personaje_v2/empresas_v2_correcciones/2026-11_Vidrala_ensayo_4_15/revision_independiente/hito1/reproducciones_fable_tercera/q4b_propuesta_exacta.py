"""Tercera pasada · apoyo de la [Propuesta] de T1: evaluar la fórmula de un derivado con aritmética decimal EXACTA (fractions.Fraction a
partir de repr) y comparar con la tolerancia relativa al RESULTADO (1e-9), en lugar de «1e-9 × el mayor origen».
Se comprueba (solo lectura) sobre los derivados de los tres registros reales de la 4.14 que la regla propuesta acepta exactamente lo que
hoy se acepta como «exacto» en ellos, y sobre los contraejemplos de q4 que los rechaza. No modifica el árbol."""
import ast, json, os, sys
from decimal import Decimal
from fractions import Fraction

PV = os.environ.get("PV", "/tmp/rev_fable3/congelado3/personaje_v2")
sys.path.insert(0, os.path.join(PV, "scripts"))
sys.dont_write_bytecode = True
import verificacion_entradas as VE  # noqa: E402


def fr(x):
    return Fraction(Decimal(repr(x)))


class _Exacto(ast.NodeTransformer):
    def visit_Constant(self, n):
        if isinstance(n.value, (int, float)) and not isinstance(n.value, bool):
            return ast.copy_location(ast.Call(func=ast.Name(id="_fr", ctx=ast.Load()), args=[ast.Constant(value=repr(n.value))], keywords=[]), n)
        return n

    def visit_Subscript(self, n):  # las claves de o["…"] no se tocan
        return n

    def visit_Call(self, n):  # round(x, n): el número de decimales sigue siendo un entero
        if isinstance(n.func, ast.Name) and n.func.id == "round" and len(n.args) == 2:
            n.args[0] = self.visit(n.args[0])
            return n
        return self.generic_visit(n)


def eval_exacto(formula, o):
    VE._claves_formula(formula)
    arbol = ast.fix_missing_locations(_Exacto().visit(ast.parse(formula, mode="eval")))
    return eval(compile(arbol, "<formula>", "eval"), {"__builtins__": {}},
                {"o": {k: fr(v) for k, v in o.items()}, "abs": abs, "min": min, "max": max, "sum": sum, "round": round, "_fr": lambda s: Fraction(Decimal(s))})


def propuesto(formula, vals, vm):
    r = eval_exacto(formula, vals)
    v = fr(vm)
    return abs(r - v) <= Fraction(1, 10 ** 9) * max(abs(r), abs(v)), r


def actual(formula, vals, vm):
    r = VE._eval_formula(formula, vals)
    esc_o = max([abs(x) for x in vals.values()] + [abs(r), abs(vm), 1e-300])
    return abs(r - vm) <= 1e-9 * esc_o or VE._igual_exacto(r, vm), r


E414 = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_14")
tot = dif = 0
for exp in ("viscofan_decisiones/Viscofan", "vidrala_decisiones/Vidrala", "elis_decisiones/Elis"):
    reg = json.load(open(os.path.join(E414, exp, "verificacion_entradas.json"), encoding="utf-8"))
    por = {e["celda"]: e for e in reg["entradas"]}
    n = a_ok = p_ok = 0
    for e in reg["entradas"]:
        d = e.get("derivacion") or {}
        if e.get("clase") != "derivado":
            continue
        vals = {o: por[o]["valor_modelo"] for o in d["origenes"]}
        vm = e["valor_modelo"]
        a, ra = actual(d["formula"], vals, vm)
        p, rp = propuesto(d["formula"], vals, vm)
        n += 1; a_ok += a; p_ok += p
        if a != p:
            dif += 1
            print(f"   DISTINTO {exp} {e['celda']}: actual {a} ({ra!r}) · propuesto {p} ({float(rp)!r}) · modelo {vm!r} · {d['formula'][:80]}")
    tot += n
    print(f"{exp}: {n} derivados · «exacto» con la regla actual: {a_ok} · con la aritmética exacta propuesta: {p_ok}")
print(f"total {tot} derivados reales · decisiones distintas: {dif}")
print("\ncontraejemplos de q4 (deben rechazarse) y controles (deben aceptarse):")
for rot, formula, vals, vm in (("ratio 0,887 con orígenes ≈1e9 que dan 0,25", 'o["n"] / o["d"]', {"n": 250000000.0, "d": 1000000000.0}, 0.887),
                               ("ratio 0,887 con orígenes en miles que dan 0,8874", 'o["n"] / o["d"]', {"n": 887400.0, "d": 1000000.0}, 0.887),
                               ("importe 849,697 con origen en unidades que da 849,0", 'o["e"] / 1000000', {"e": 849000000.0}, 849.697),
                               ("C55 con 40.000 acciones de menos", '(o["a"] - o["b"]) / 1000000', {"a": 46500000.0, "b": 980791.0}, 45.479209),
                               ("control: C55 con las cifras exactas", '(o["a"] - o["b"]) / 1000000', {"a": 46500000.0, "b": 1020791.0}, 45.479209),
                               ("control: 120,4 − 120,4 = 0 (el ruido que motivó la tolerancia)", 'o["a"] - o["b"]', {"a": 120.4, "b": 120.4}, 0),
                               ("control: 0,1 + 0,2 = 0,3", 'o["a"] + o["b"]', {"a": 0.1, "b": 0.2}, 0.3),
                               ("control: 1e9 + 0,4 − (1e9 + 0,1) = 0,3", 'o["a"] - o["b"]', {"a": 1000000000.4, "b": 1000000000.1}, 0.3),
                               ("control: round(n/d, 4) = 0,1948", 'round(o["n"] / o["d"], 4)', {"n": 37.117, "d": 190.537}, 0.1948),
                               ("control: n/d sin redondear, modelo con todos los decimales", 'o["n"] / o["d"]', {"n": 37.117, "d": 190.537}, 37.117 / 190.537)):
    a, ra = actual(formula, vals, vm)
    p, rp = propuesto(formula, vals, vm)
    print(f"   [{rot}] regla actual: {'ACEPTA' if a else 'rechaza'} · aritmética exacta propuesta: {'ACEPTA' if p else 'rechaza'}")
