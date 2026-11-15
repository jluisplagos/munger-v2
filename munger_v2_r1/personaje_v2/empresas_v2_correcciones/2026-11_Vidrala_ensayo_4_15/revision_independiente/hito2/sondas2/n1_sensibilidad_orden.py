#!/usr/bin/env python3
"""n1 · H6 (segunda pasada): con la semilla FIJA, ¿el veredicto de _sensibilidad depende del ORDEN de la lista de orígenes, de cuántos
son o de sus valores reales? Para fórmulas legítimas (cada origen influye de verdad en alguna región: se comprueba por fuerza bruta con
4000 puntos), se prueban todas las permutaciones de la lista de orígenes y varios puntos reales. Un «inerte» ahí es un rechazo falso
determinista. Después, fórmulas con un origen de verdad inerte (control: tienen que rechazarse siempre).
Uso: python3 -I -B n1_sensibilidad_orden.py"""
import itertools, os, random, sys
from fractions import Fraction as Fr
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun2 import VE, ETIQUETA

print("código:", ETIQUETA)
LEGITIMAS = [
    'max(o["a"], o["b"])', 'min(o["a"], o["b"])', 'max(o["a"], o["b"], o["c"])', 'min(o["a"], o["b"], o["c"])',
    'max(o["a"] - o["b"], o["c"] - o["d"])', 'min(max(o["a"], o["b"]), o["c"])', 'max(min(o["a"], o["b"]), o["c"])',
    'min(max(o["a"], o["b"]), max(o["c"], o["d"]))', 'max(min(o["a"], o["b"]), min(o["c"], o["d"]))',
    'min(max(o["a"], o["b"]), max(o["c"], o["d"]), o["e"])', 'max(o["a"], o["b"]) - min(o["c"], o["d"])',
    'max(o["a"] - o["b"], 0)', 'min(o["a"] - o["b"], 0)', 'max(o["a"], 0) + min(o["b"], 0)',
    'abs(o["a"] - o["b"]) - max(o["c"], o["d"])', 'max(o["a"] / o["b"], o["c"])', 'min(o["a"] * o["b"], o["c"] * o["d"])',
    'max(min(o["a"], o["b"]), min(o["c"], o["d"]), min(o["e"], o["f"]))', 'min(max(o["a"], o["b"]), max(o["c"], o["d"]), max(o["e"], o["f"]))',
    'max(o["a"] - 100, 0) + o["b"]', 'max(o["a"] - 1000000, 0) + o["b"]', 'min(max(o["a"] - o["b"], 0), o["c"])',
    'max(min(max(o["a"], o["b"]), o["c"]), o["d"])', 'min(max(min(o["a"], o["b"]), o["c"]), o["d"])',
    'sum([max(o["a"], o["b"]), min(o["c"], o["d"])])', 'max(o["a"], o["b"]) / max(o["c"], o["d"])',
]
INERTES = [  # el primer origen (a) NO influye nunca
    ('o["a"] - o["a"] + o["b"]', "a"), ('min(max(o["a"], 0), 0) + o["b"]', "a"), ('abs(o["a"]) - max(o["a"], -o["a"]) + o["b"]', "a"),
    ('max(o["a"], o["a"] + 1) - o["a"] + o["b"]', "a"), ('o["b"] + (o["a"] - o["a"]) / o["c"]', "a"),
    ('o["b"] + max(o["a"] - 1000000000000, 0) * (o["a"] - o["a"])', "a"),
]


def claves(f):
    return sorted(x for x in VE._claves_formula(f))


def influye_de_verdad(f, ks, n=4000):
    """origen → True si en alguno de n puntos aleatorios (semilla propia, distinta de la del control) cambiar el origen cambia el resultado"""
    rnd = random.Random(20261115)
    vivos = set()
    for _ in range(n):
        esc = rnd.choice([1, 10, 1000, 10 ** 6])
        pt = {k: Fr(rnd.randint(-10 ** 4, 10 ** 4), rnd.randint(1, 50)) * esc for k in ks}
        try:
            b = VE._eval_formula_exacta(f, pt, sin_redondeo=True)
        except ZeroDivisionError:
            continue
        for k in ks:
            if k in vivos:
                continue
            for d in (Fr(1, 7), -Fr(1, 7), Fr(10 ** 7), -Fr(10 ** 7)):
                try:
                    if VE._eval_formula_exacta(f, dict(pt, **{k: pt[k] + d}), sin_redondeo=True) != b:
                        vivos.add(k)
                        break
                except ZeroDivisionError:
                    pass
    return vivos


rnd_v = random.Random(7)
print("\n== A · fórmulas legítimas: todas las permutaciones de la lista de orígenes × 25 puntos reales")
tot_falsos = 0
for f in LEGITIMAS:
    ks = claves(f)
    verdad = influye_de_verdad(f, ks)
    if set(ks) != verdad:
        print(f"   (aviso del revisor) {f}: por fuerza bruta no influyen {sorted(set(ks) - verdad)}")
    malos, n = [], 0
    perms = list(itertools.permutations(ks)) if len(ks) <= 5 else [tuple(rnd_v.sample(ks, len(ks))) for _ in range(120)]
    for perm in perms:
        for _ in range(25):
            vals = {k: float(Fr(rnd_v.randint(-5000, 5000), rnd_v.choice([1, 2, 4, 5, 10]))) for k in ks}
            n += 1
            try:
                inertes, locales = VE._sensibilidad(f, vals, list(perm))
            except ZeroDivisionError:
                continue
            falsos = [x for x in inertes if x in verdad]
            if falsos:
                malos.append((perm, falsos))
    ordenes = sorted({p for p, _ in malos})
    tot_falsos += len(malos)
    print(f"   {f:68} rechazos falsos: {len(malos):4} de {n:5}" + (f" · en {len(ordenes)} de {len(perms)} órdenes, p. ej. orígenes {list(ordenes[0])} → inertes {malos[0][1]}" if malos else ""))
print(f"   total de rechazos falsos (origen que sí influye, declarado inerte): {tot_falsos}")

print("\n== B · control: un origen de verdad inerte tiene que declararse inerte en cualquier orden")
for f, inerte in INERTES:
    ks = claves(f)
    no_detectado = 0
    perms = list(itertools.permutations(ks))
    for perm in perms:
        vals = {k: float(Fr(rnd_v.randint(1, 5000), rnd_v.choice([1, 2, 4, 5, 10]))) for k in ks}
        try:
            inertes, locales = VE._sensibilidad(f, vals, list(perm))
        except ZeroDivisionError:
            inertes = ["(división por cero en el punto real)"]
        if inerte not in inertes and "(división por cero en el punto real)" not in inertes:
            no_detectado += 1
    print(f"   {f:68} inerte «{inerte}» no detectado en {no_detectado} de {len(perms)} órdenes")

print("\n== C · origen decorativo que pasa por los puntos extremos (±10⁹) o por una división por cero en el punto perturbado")
for f, vals in [('o["b"] + max(o["a"] - 100000000, 0)', {"a": 849.697, "b": 12.5}),
                ('o["b"] + max(o["a"] - 1000000000000, 0)', {"a": 849.697, "b": 12.5}),
                ('o["b"] + (o["a"] - o["a"]) / (o["a"] - 1000000000 - 1000000 - 1/1000)', {"a": 849.697, "b": 12.5}),
                ('min(o["b"], o["a"])', {"a": 849.697, "b": 12.5})]:
    ks = claves(f)
    try:
        ctes = VE._constantes_no_admitidas(f)
        inertes, locales = VE._sensibilidad(f, vals, ks)
        r = VE._eval_formula_exacta(f, vals)
        print(f"   {f:75} constantes no admitidas {ctes} · inertes {inertes} · locales {sorted(locales)} · resultado {float(r)} (= b: {float(r) == vals['b']})")
    except Exception as ex:  # noqa: BLE001
        print(f"   {f:75} {type(ex).__name__}: {ex}")
