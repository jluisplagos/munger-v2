#!/usr/bin/env python3
"""s6 · U3 (coste acotado) y U4 (sensibilidad y constantes), nivel de unidad, con el código del hito 2 y (PV=…hito1) con el del hito 1.
A) coste: fórmulas dentro de los límites (2000 caracteres, 400 nodos) con el peor coste que el revisor sabe construir; anidamientos.
B) sensibilidad: derivaciones legítimas en casos límite y formas triviales; se imprime (constantes no admitidas, inertes, locales).
C) el 0 exento en min/max y el «origen anulado» con round."""
import os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import VE
from fractions import Fraction as Fr

H2 = hasattr(VE, "_sensibilidad")


def estado(formula, vals, origenes=None):
    """Lo que haría comprobar con esta fórmula: error de constantes, error de evaluación, inertes, constante local; si no, el valor."""
    origenes = list(vals) if origenes is None else origenes
    try:
        ctes = VE._constantes_no_admitidas(formula)
    except Exception as ex:  # noqa: BLE001
        return f"ERROR fórmula no evaluable ({type(ex).__name__}: {str(ex)[:70]})"
    if ctes:
        return f"ERROR escribe cifras {ctes!r}"
    try:
        usadas = VE._claves_formula(formula)
        if usadas != set(origenes):
            return f"ERROR usa {sorted(map(str, usadas))} y declara {sorted(origenes)}"
        r = VE._eval_formula_exacta(formula, vals)
        if H2:
            inertes, locales = VE._sensibilidad(formula, vals, origenes)
        else:  # regla del hito 1 (copiada de su comprobar)
            base = VE._eval_formula_exacta(formula, vals, sin_redondeo=True)
            inertes = []
            for o in origenes:
                v_o = VE._frac(vals[o])
                pert = dict(vals, **{o: v_o * (1 + Fr(1, 10 ** 7)) + Fr(1, 10 ** 7)})
                if VE._eval_formula_exacta(formula, pert, sin_redondeo=True) == base:
                    inertes.append(o)
            locales = {"(hito 1: sin esta regla)"}
    except Exception as ex:  # noqa: BLE001
        return f"ERROR fórmula no evaluable ({type(ex).__name__}: {str(ex)[:70]})"
    if inertes:
        return f"ERROR orígenes inertes {inertes}"
    if not locales:
        return "ERROR constante en el punto real (ningún origen influye localmente)"
    try:
        return f"ACEPTADA valor={float(r)!r}"
    except OverflowError:
        return f"ACEPTADA por estas reglas; float(resultado) desborda (en comprobar: «fórmula no evaluable (OverflowError)»); bits del numerador: {r.numerator.bit_length()}"


import ast


def max_terminos(op, termino='o["a"]'):
    n = 1
    while sum(1 for _ in ast.walk(ast.parse(op.join([termino] * (n + 1)), mode="eval"))) <= 400 and len(op.join([termino] * (n + 1))) <= 2000:
        n += 1
    return n


print(f"código: {'hito 2' if H2 else 'hito 1'}")
print("== A · coste")
casos_a = {
    "1999 signos menos": "-" * 1990 + 'o["a"]',
    "999 paréntesis anidados": "(" * 990 + 'o["a"]' + ")" * 990,
    "190 paréntesis anidados": "(" * 190 + 'o["a"]' + ")" * 190,
    "abs anidado 150 veces": "abs(" * 150 + 'o["a"]' + ")" * 150,
    "producto del máximo de orígenes enormes que cabe en 400 nodos": " * ".join(['o["a"]'] * max_terminos(" * ")),
    "cociente encadenado (máximo en 400 nodos)": " / ".join(['o["a"]'] * max_terminos(" / ")),
    "suma de productos (máximo en 400 nodos)": " + ".join(['o["a"] * o["b"]'] * max_terminos(" + ", 'o["a"] * o["b"]')),
    "round 12 anidado (máximo en 400 nodos)": "round(" * 60 + 'o["a"] / o["b"]' + ", 12)" * 60,
    "round 12 anidado 40 veces sobre un cociente periódico": "round(" * 40 + 'o["a"] / o["b"]' + ", 12)" * 40,
    "cociente de sumas de fracciones periódicas (denominadores grandes)": " + ".join(['o["a"] / (o["b"] + %d)' % k for k in range(1, 13)] * 3),
    "literal de 1990 cifras": 'o["a"] * ' + "9" * 1985,
    "literal 1e400 (inf)": 'o["a"] * 1e400',
    "literal 1e-400 (0.0)": 'o["a"] + 1e-400',
    "subíndices encadenados": 'o["a"]' + '["a"]' * 150,
    "lista enorme en sum": "sum([" + ", ".join(['o["a"]'] * 90) + "])",
    "comparación (no permitida)": 'o["a"] if o["a"] > 0 else 0',
    "potencia (no permitida)": 'o["a"] ** 9999999',
    "desplazamiento": 'o["a"] << 999999',
    "cadena * entero": '"x" * 1000000000 + o["a"]',
    "lambda": '(lambda: o["a"])()',
    "atributo": 'o.__class__',
}
for n_, f_ in casos_a.items():
    t0 = time.time()
    r = estado(f_, {"a": 1e300, "b": 3e-300} if "o[\"b\"]" in f_ else {"a": 1e300})
    print(f"   {n_:35} ({len(f_)} caracteres) -> {r[:110]}   [{time.time() - t0:.2f} s]")

print("\n== B · sensibilidad: casos límite legítimos y formas triviales")
casos_b = [
    ("max(a − b, 0) con el suelo ACTIVO (a < b): partida que no puede ser negativa", 'max(o["a"] - o["b"], 0)', {"a": 2.0, "b": 5.0}),
    ("max(a − b, 0) con el suelo inactivo", 'max(o["a"] - o["b"], 0)', {"a": 5.0, "b": 2.0}),
    ("min(a, 0) con a positivo (techo activo)", 'min(o["a"], 0)', {"a": 5.0}),
    ("producto de dos ceros comprobados", 'o["a"] * o["b"]', {"a": 0.0, "b": 0.0}),
    ("producto con un cero", 'o["a"] * o["b"]', {"a": 0.25, "b": 0.0}),
    ("0 / d", 'o["a"] / o["b"]', {"a": 0.0, "b": 190.537}),
    ("origen −1", 'o["a"] + o["b"]', {"a": 850.697, "b": -1.0}),
    ("max de dos partidas (argumento menor)", 'max(o["a"], o["b"])', {"a": 849.697, "b": 100.25}),
    ("abs de una diferencia nula", 'abs(o["a"] - o["b"])', {"a": 5.0, "b": 5.0}),
    ("media con round", 'round((o["a"] + o["b"]) / 2, 3)', {"a": 1120.148, "b": 1528.871}),
    ("max(a, b) − min(a, b) con a = b", 'max(o["a"], o["b"]) - min(o["a"], o["b"])', {"a": 5.0, "b": 5.0}),
    ("TRIVIAL o[x] * 0 + 12", 'o["a"] * 0 + 12', {"a": 2019}),
    ("TRIVIAL o[x] − o[x] + o[y]", 'o["a"] - o["a"] + o["b"]', {"a": 2019, "b": 849.697}),
    ("TRIVIAL min(o[x], 12)", 'min(o["a"], 12)', {"a": 2019}),
    ("TRIVIAL o[x] * max(0, 0) + o[y]", 'o["a"] * max(0, 0) + o["b"]', {"a": 2019, "b": 849.697}),
    ("TRIVIAL o[x] * min(0) + o[y]", 'o["a"] * min(0) + o["b"]', {"a": 2019, "b": 849.697}),
    ("TRIVIAL max(o[x], 0) * 0", 'max(o["a"], 0) * 0 + o["b"]', {"a": 2019, "b": 849.697}),
    ("DECORADO o[y] + max(o[x] − 1000000, 0)  (x no influye en el punto real)", 'o["b"] + max(o["a"] - 1000000, 0)', {"a": 2019, "b": 849.697}),
    ("DECORADO o[y] + o[x] * o[z] con z = 0 comprobado", 'o["b"] + o["a"] * o["z"]', {"a": 2019, "b": 849.697, "z": 0.0}),
    ("DECORADO min(o[y], o[x]) con x mayor", 'min(o["b"], o["a"])', {"a": 2019, "b": 849.697}),
]
for n_, f_, v_ in casos_b:
    print(f"   {n_}\n        {f_}  {v_} -> {estado(f_, v_)}")

print("\n== C · cifra escrita con constantes admitidas y un origen anulado (U1)")
CIFRA = "(8*100 + 4*10 + 9 + 6/10 + 9/100 + 7/1000)"
casos_c = [
    ("año − cifra compuesta (U1, fila 1 de la cuarta pasada)", 'o["a"] - (1*1000 + 1*100 + 6*10 + 9 + 3/10 + 3/1000)', {"a": 2019}),
    ("round con decimales negativos (U1, fila 4; el hito 2 lo prohíbe)", CIFRA + ' + round(o["a"], -9)', {"a": 2019}),
    ("round de o[x] / 10^12 (el origen queda anulado igual, sin decimales negativos)", CIFRA + ' + round(o["a"] / 1000000000000)', {"a": 2019}),
    ("round de o[x] * 10^-12 con 0 decimales", CIFRA + ' + round(o["a"] * 0.000000000001, 0)', {"a": 2019}),
    ("round de o[x] / 10^5 con 2 decimales, x = 0,25", CIFRA + ' + round(o["a"] / 100000, 2)', {"a": 0.25}),
    ("abs (U1, fila 3)", CIFRA + ' + abs(o["a"] - (2*1000 + 1*10 + 9))', {"a": 2019}),
    ("max con 0 exento: cifra + max(o[x] − 10^12, 0)", CIFRA + ' + max(o["a"] - 1000000000000, 0)', {"a": 2019}),
    ("max con 0 exento: cifra + max(o[x] − 10^5, 0)", CIFRA + ' + max(o["a"] - 100000, 0)', {"a": 2019}),
    ("producto (U1, fila 5)", 'o["a"] * (8*100000 + 4*10000 + 9*1000 + 6*100 + 9*10 + 7) / (2*1000 + 1*10 + 9) / 1000', {"a": 2019}),
]
for n_, f_, v_ in casos_c:
    print(f"   {n_}\n        {f_} -> {estado(f_, v_)}")
