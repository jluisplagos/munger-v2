"""Cuarta pasada · T2 (constantes de fórmula limitadas a enteros 1–12, potencias de diez y decimales de round; control de sensibilidad de
cada origen sin round; clases de origen admitidas; escala potencia de diez con unidad no monetaria).
A · una cifra escrita en la fórmula con dígitos × potencias de diez (todas las constantes admitidas) y un origen cualquiera que «influye»;
    round con decimales negativos (anula el origen en la evaluación real y no en el control de sensibilidad); cifra compuesta sin ningún
    literal salvo potencias de diez (diferencias entre los años de la Historia).
B · en bloque: todos los datos numéricos publicados del cálculo (y de juicio) así, sin fuente.
C · rechazos falsos del control de sensibilidad y de constantes en derivaciones legítimas.
D · escala (q5 de la tercera pasada, adaptada).
Arnés fx4.py (vínculo escrito a mano, como las baterías). PV=<otro árbol>/personaje_v2 para comparar con el de la tercera pasada."""
import copy
from decimal import Decimal
import fx4 as fx
from fx4 import VE, con, ent, con_k, resumen, K, REG

inst = fx.inst
vK = inst["celdas"][K]
ORIG = "Historia!F5"  # el año de la columna de K (2019): celda del universo, dato publicado y comprobado, ajena al importe
vO = inst["celdas"][ORIG]
print("árbol:", fx.PV)
print("K =", K, vK, "| ORIG =", ORIG, vO, "| años C5:L5 =", [int(a) for a in fx.anios])


def digitos(x):
    """x ≥ 0 escrito solo con enteros de 1 a 9 y potencias de diez (10^0 … 10^12): las constantes que T2 admite."""
    s = format(Decimal(repr(x)) if isinstance(x, float) else Decimal(x), "f")
    ent_, _, dec = s.partition(".")
    t = []
    for i, ch in enumerate(ent_):
        p = len(ent_) - 1 - i
        if ch != "0":
            t.append(f"{ch}*{10 ** p}" if p else ch)
    for i, ch in enumerate(dec):
        if ch != "0":
            p = i + 1
            t.append(f"{ch}" + "".join(f"/{10 ** min(12, p - j)}" for j in range(0, p, 12)))
    return "(" + " + ".join(t) + ")" if t else None


def desde(origen, v_origen, v):
    """Fórmula que da v a partir de un origen cualquiera más (o menos) una cifra compuesta con dígitos y potencias de diez."""
    dif = Decimal(repr(v)) - Decimal(repr(v_origen))
    if dif == 0:
        return f'o["{origen}"]'
    return f'o["{origen}"] {"+" if dif > 0 else "-"} {digitos(abs(dif))}'


def caso(nombre, r, k=K, ancho=300):
    print(f"[{nombre}]\n      {resumen(r, k, ancho)}")


def deriva(g, k, formula, origenes, unidad=None, just=None):
    e = ent(g, k); e["fuente"] = {}
    e.update(clase="derivado", derivacion=dict({"origenes": origenes, "formula": formula, "conciliacion": "x"}, **({"unidad": unidad} if unidad else {})))
    if just:
        e["justificacion_clase"] = just


print("\n=== A · una cifra escrita en la fórmula con constantes admitidas (dígitos × potencias de diez) y un origen que «influye»")
A5 = {c: f"Historia!{c}5" for c in "CDEFHL"}
SIN_LITERALES = (f'(o["{A5["L"]}"] - o["{A5["D"]}"]) * 100 + (o["{A5["L"]}"] - o["{A5["H"]}"]) * 10 + (o["{A5["L"]}"] - o["{A5["C"]}"]) '
                 f'+ (o["{A5["L"]}"] - o["{A5["F"]}"]) / 10 + (o["{A5["L"]}"] - o["{A5["C"]}"]) / 100 + (o["{A5["L"]}"] - o["{A5["E"]}"]) / 1000')
FORMULAS = [
    ("año − cifra compuesta", desde(ORIG, vO, vK), [ORIG]),
    ("cifra compuesta + año − año compuesto", f'{digitos(vK)} + o["{ORIG}"] - {digitos(vO)}', [ORIG]),
    ("cifra compuesta + max(año, año compuesto) − año compuesto (codo de max)", f'{digitos(vK)} + max(o["{ORIG}"], {digitos(vO)}) - {digitos(vO)}', [ORIG]),
    ("cifra compuesta + abs(año − año compuesto)", f'{digitos(vK)} + abs(o["{ORIG}"] - {digitos(vO)})', [ORIG]),
    ("cifra compuesta + round(año, -9) (el round real da 0; el control de sensibilidad lo trata como identidad)", f'{digitos(vK)} + round(o["{ORIG}"], -9)', [ORIG]),
    ("año × cifra compuesta ÷ año compuesto ÷ 1000", f'o["{ORIG}"] * {digitos(round(vK * 1000))} / {digitos(vO)} / 1000', [ORIG]),
    ("sin ningún literal salvo potencias de diez: dígitos = diferencias entre los años de la Historia", SIN_LITERALES, [A5[c] for c in "LDHCFE"]),
]
for nombre, formula, origenes in FORMULAS:
    print("   constantes no admitidas según VE._constantes_no_admitidas:", VE._constantes_no_admitidas(formula) if hasattr(VE, "_constantes_no_admitidas") else "(no existe en este árbol)")
    r = con(lambda g: deriva(g, K, formula, origenes), resellar=True)
    caso(f"A · {K} (ventas 2019, dato de cálculo) sin fuente, como derivado de {origenes} · {nombre}: {formula}", r)
    print("      datos_como_hipotesis:", r["datos_como_hipotesis"], "| por_clase:", r["por_clase"])

print("\n=== A' · formas de escribir una constante (VE._constantes_no_admitidas y VE._eval_formula_exacta con o[\"x\"] = 2)")
if hasattr(VE, "_eval_formula_exacta"):
    for f in ('o["x"] * 10**3', 'o["x"] * 1e3', 'o["x"] * 1_000', 'o["x"] * 0x3E8', 'o["x"] * 10 * 10 * 10', 'o["x"] * 1e400', 'o["x"] * 1e-400', 'o["x"] * 1j', 'o["x"] * True',
              'o["x"] + "849.697"', 'o["x"] + sum([])', 'max(o["x"] - 3, sum([]))', 'o["x"] * 10000000000000', 'o["x"] * 1000000000000 * 10', 'o["x"] + 13', 'o["x"] + 12 + 1',
              'o["x"] + 849697 / 1000', 'o["x"] + (8*100 + 4*10 + 9 + 6/10 + 9/100 + 7/1000)'):
        try:
            malas = VE._constantes_no_admitidas(f)
        except Exception as ex:  # noqa: BLE001
            malas = f"{type(ex).__name__}: {str(ex)[:60]}"
        try:
            val = float(VE._eval_formula_exacta(f, {"x": 2.0}))
        except Exception as ex:  # noqa: BLE001
            val = f"{type(ex).__name__}: {str(ex)[:60]}"
        print(f"   {f} → constantes no admitidas: {malas} · valor: {val}")

print("\n=== B · en bloque")
datos_calc = [e["celda"] for e in REG["entradas"] if e["clase"] == "dato_publicado" and inst["ambito"][e["celda"]] == "calculo"
              and isinstance(e["valor_modelo"], (int, float)) and e["celda"] != ORIG]
datos_juicio = [e["celda"] for e in REG["entradas"] if e["clase"] == "dato_publicado" and inst["ambito"][e["celda"]] == "juicio" and isinstance(e["valor_modelo"], (int, float))]


def todos(g, celdas):
    for k in celdas:
        deriva(g, k, desde(ORIG, vO, inst["celdas"][k]), [ORIG])


r = con(lambda g: todos(g, datos_calc), resellar=True)
print(f"[B · TODOS los datos numéricos publicados del cálculo ({len(datos_calc)}) sin fuente, como derivados de {ORIG} con «año ± cifra compuesta» (conservan la comprobación del fixture)]\n      {resumen(r)}")
print("      datos_como_hipotesis:", len(r["datos_como_hipotesis"]), "| por_clase:", r["por_clase"], "| motivo:", r["motivo"])
print("      resumen:", r["resumen"])
print("      ejemplos:", [(k, ent(copy.deepcopy(REG), k)["valor_modelo"], desde(ORIG, vO, inst["celdas"][k])) for k in datos_calc[:3] + datos_calc[-2:]])
r = con(lambda g: todos(g, datos_calc + datos_juicio), resellar=True)
print(f"[B · ídem con los de juicio ({len(datos_calc)} + {len(datos_juicio)})]\n      {resumen(r)}")
print("      datos_como_hipotesis:", len(r["datos_como_hipotesis"]), "| por_clase:", r["por_clase"])


def sin_revisor(g):
    todos(g, datos_calc)
    for k in datos_calc:
        ent(g, k)["comprobacion"].update(revisor=None, resultado=None, fuente_examinada=None)


r = con(sin_revisor, resellar=True)
print(f"[B · ídem (cálculo) sin revisor en los derivados (control: la firma del revisor sigue siendo necesaria)]\n      {resumen(r)}")

print("\n=== C · derivaciones legítimas que el control de sensibilidad o el de constantes rechazan")
BASE_F = copy.deepcopy(ent(REG, K)["fuente"])
KZ = next(e["celda"] for e in REG["entradas"] if e["clase"] == "cero_comprobado" and inst["ambito"][e["celda"]] == "calculo")
print("KZ (celda de cálculo con cero comprobado en el fixture):", KZ, inst["celdas"][KZ], "| id:", inst["ids"][KZ])
VALS = {"aux:a1": round(vK + 1, 3), "aux:m1": -1.0, "aux:t": 0.25, "aux:z": 0.0, "aux:d": 190.537, "aux:kv": vK, "aux:b": 100.25, "aux:x": round(vK + 100.25, 3)}
CITA = {n: f"Partida sintética {n}: {round(v * 1000, 6):.3f}" for n, v in VALS.items()}
PAG = {n: fx.nueva_pagina(CITA[n]) for n in VALS}  # las páginas se añaden antes (nueva_pagina vuelve a sellar el registro base)
REG = fx.REG
BASE_F = copy.deepcopy(ent(REG, K)["fuente"])


def aux(n):
    v = VALS[n]
    return {"celda": n, "id": n, "ambito": "auxiliar", "uso": "origen", "material": True, "clase": "cero_comprobado" if v == 0 else "dato_publicado", "valor_modelo": v,
            "comprobacion": dict(fx.COMPROBADA), "incidencia": None,
            "fuente": dict(copy.deepcopy(BASE_F), pagina=PAG[n], valor_fuente=round(v * 1000, 6), cita=CITA[n])}


LEGIT = [
    ("un origen que vale exactamente −1 (punto fijo de la perturbación v·(1+1e-7)+1e-7)", K, 'o["aux:a1"] + o["aux:m1"]', ["aux:a1", "aux:m1"], "mm"),
    ("producto con un cero comprobado (p. ej. tipo × base, con base 0): el resultado 0 no cambia al perturbar el otro factor", KZ, 'o["aux:t"] * o["aux:z"]', ["aux:t", "aux:z"], "mm"),
    ("cociente 0 / d (p. ej. dividendos ÷ beneficio, sin dividendos)", KZ, 'o["aux:z"] / o["aux:d"]', ["aux:z", "aux:d"], None),
    ("max(a, b) con b menor (el mayor de dos partidas)", K, 'max(o["aux:kv"], o["aux:b"])', ["aux:kv", "aux:b"], "mm"),
    ("max(x − b, 0) (suelo en cero): el 0 no es una constante admitida", K, 'max(o["aux:x"] - o["aux:b"], 0)', ["aux:x", "aux:b"], "mm"),
    ("control: resta de dos orígenes corrientes", K, 'o["aux:x"] - o["aux:b"]', ["aux:x", "aux:b"], "mm"),
]
for nombre, celda, formula, origenes, unidad in LEGIT:
    def cambio(g, celda=celda, formula=formula, origenes=origenes, unidad=unidad):
        for n in origenes:
            g["entradas"].append(aux(n))
        deriva(g, celda, formula, origenes, unidad)
    r = con(cambio, resellar=True)
    caso(f"C · {celda} = {formula} · {nombre}", r, celda, 260)
if hasattr(VE, "_eval_formula_exacta"):
    from fractions import Fraction
    v = Fraction(-1)
    print("   perturbación de un origen de valor −1:", v * (1 + Fraction(1, 10 ** 7)) + Fraction(1, 10 ** 7), "(no cambia)")
    for lit, uso in ((0, "max(x, 0)"), (0.5, "× 0,5 (media de dos)"), (2, "÷ 2"), (12, "meses"), (52, "semanas"), (360, "días"), (365, "días"), (100, "porcentaje"), (1e-3, "miles"), (0.21, "un tipo escrito"), (-1, "cambio de signo")):
        print(f"   literal {lit!r} ({uso}):", "no admitido" if VE._constantes_no_admitidas(f'o["a"] * {lit!r}') else "admitido")

print("\n=== D · escala con una unidad no monetaria (q5 de la tercera pasada) y nuevas variantes")
pag = fx.nueva_pagina("Véase la nota 1 de la memoria consolidada")
pag0 = fx.nueva_pagina("Tipo de cambio aplicado: 1,0842 · importe 783,7087253")
pag1 = fx.nueva_pagina("Importe neto de la cifra de negocios (en miles de euros): 849,697")
vf_fx = 783.7087253
for rot, k, cambio in (
        ("valor_fuente 1 («nota 1») × escala 849,697, unidad «unidades» (el contraejemplo de la tercera pasada)", K, dict(unidad="unidades", escala=vK, valor_fuente=1, cita="Véase la nota 1 de la memoria consolidada", pagina=pag)),
        ("lo mismo con «miles de €» (no reconocida)", K, dict(unidad="miles de €", escala=vK, valor_fuente=1, cita="Véase la nota 1 de la memoria consolidada", pagina=pag)),
        ("control: unidad «miles de €» (no reconocida) con escala 0,001 y la cifra en la cita", K, dict(unidad="miles de €")),
        ("conversión de divisa: unidad «USD (millones)», escala 1,0842 (tipo de cambio) × 783,7087253 → rechazada por no ser potencia de diez", K,
         dict(unidad="USD (millones)", escala=vK / vf_fx, valor_fuente=vf_fx, cita="Tipo de cambio aplicado: 1,0842 · importe 783,7087253", pagina=pag0)),
        ("unidad monetaria con una grafía NO reconocida («miles de €») y escala 1: la fuente dice 849,697 miles (0,85 millones) y el modelo 849,697 millones", K,
         dict(unidad="miles de €", escala=1, valor_fuente=vK, cita="Importe neto de la cifra de negocios (en miles de euros): 849,697", pagina=pag1)),
        ("control: lo mismo con la grafía reconocida «miles de euros» (la escala obligada es 0,001)", K,
         dict(unidad="miles de euros", escala=1, valor_fuente=vK, cita="Importe neto de la cifra de negocios (en miles de euros): 849,697", pagina=pag1)),
        ("cero comprobado con unidad «unidades» y escala 0 (cualquier cifra × 0)", KZ, dict(unidad="unidades", escala=0, valor_fuente=1, cita="Véase la nota 1 de la memoria consolidada", pagina=pag))):
    r = con(lambda g: ent(g, k)["fuente"].update(cambio), resellar=True)
    caso(f"D · {k} como dato publicado: {rot}", r, k, 230)
fx.limpiar()
