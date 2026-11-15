"""Cuarta pasada (sonda q2 de la tercera, adaptada) · N2/T2/T3 (dato derivado de hipótesis/convención; la fórmula usa todos sus orígenes
y solo ellos; constantes limitadas; cada origen influye; clases de origen; «origenes» lista de textos; no_aplicable contado).
A y B son los contraejemplos literales de la tercera pasada (T2). En C, los casos «mezcla» y «celda hipótesis del universo» se han
reescrito sin constantes no admitidas ni orígenes anulados, para que sigan probando la regla de N2 y no la de T2.
Los contraejemplos NUEVOS de esta pasada están en r2_t2_cifras.py. Arnés fx4.py (vínculo escrito a mano, como las baterías)."""
import copy
import fx4 as fx
from fx4 import VE, con, ent, con_k, resumen, K, REG

inst = fx.inst
vK = inst["celdas"][K]
ORIG = "Historia!F5"  # el año de la columna de K: una celda del universo comprobada que no tiene nada que ver con el importe


def caso(nombre, r, k=K):
    print(f"[{nombre}] {resumen(r, k)}")
    print(f"      datos_como_hipotesis: {r['datos_como_hipotesis'][:3]} | resumen: {r['resumen']}")


print("K =", K, vK, "| ORIG =", ORIG, inst["celdas"][ORIG], "| clase de ORIG en el fixture:", ent(REG, ORIG)["clase"])

print("\n=== A · fórmulas que nombran su origen pero no dependen de él (el control de N2 es sintáctico)")
for formula in (f'o["{ORIG}"] * 0 + {vK!r}', f'o["{ORIG}"] - o["{ORIG}"] + {vK!r}', f'min(o["{ORIG}"], {vK!r})', f'round(o["{ORIG}"] * 0, 3) + {vK!r}',
                f'{vK!r} + 0 * sum([o["{ORIG}"]])', f'{vK!r}'):
    def deriva(g, formula=formula):
        e = ent(g, K); e["fuente"] = {}
        e.update(clase="derivado", derivacion={"origenes": [ORIG], "formula": formula, "conciliacion": "x"})
    r = con(deriva, resellar=True)
    caso(f"A · {K} (ventas, dato de cálculo) como derivado de {ORIG} (el año) con la fórmula {formula}", r)

datos_calc = [e["celda"] for e in REG["entradas"] if e["clase"] == "dato_publicado" and inst["ambito"][e["celda"]] == "calculo"
              and isinstance(e["valor_modelo"], (int, float)) and e["celda"] != ORIG]
datos_juicio = [e["celda"] for e in REG["entradas"] if e["clase"] == "dato_publicado" and inst["ambito"][e["celda"]] == "juicio"
                and isinstance(e["valor_modelo"], (int, float))]


def todos_anulados(g, celdas):
    for k in celdas:
        e = ent(g, k); e["fuente"] = {}
        e.update(clase="derivado", derivacion={"origenes": [ORIG], "formula": f'o["{ORIG}"] * 0 + {inst["celdas"][k]!r}', "conciliacion": "x"})


r = con(lambda g: todos_anulados(g, datos_calc), resellar=True)
print(f"[A · TODOS los datos numéricos publicados del cálculo ({len(datos_calc)}) como derivados de {ORIG} con «o[…] * 0 + valor» (sin fuente; conservan la comprobación del fixture)] {resumen(r)}")
print("      datos_como_hipotesis:", len(r["datos_como_hipotesis"]), "| motivo:", r["motivo"], "| resumen:", r["resumen"])
r = con(lambda g: todos_anulados(g, datos_calc + datos_juicio), resellar=True)
print(f"[A · ídem con los de juicio ({len(datos_calc)} + {len(datos_juicio)})] {resumen(r)}")
print("      datos_como_hipotesis:", len(r["datos_como_hipotesis"]), "| resumen:", r["resumen"])


def sin_revisor(g):
    todos_anulados(g, datos_calc)
    for k in datos_calc:
        ent(g, k)["comprobacion"].update(revisor=None, resultado=None, fuente_examinada=None)


r = con(sin_revisor, resellar=True)
print(f"[A · ídem (cálculo) sin revisor en los derivados] {resumen(r)}")

print("\n=== B · origen auxiliar SIN FUENTE que no es hipótesis ni convención (no_aplicable / dato_ausente con valor_modelo numérico)")
for clase_aux in ("no_aplicable", "dato_ausente", "convencion", "hipotesis"):
    def via_aux(g, clase_aux=clase_aux, just=None):
        aux = {"celda": "aux:sf", "id": "aux:sf", "ambito": "auxiliar", "uso": f"origen de {K}", "material": True, "clase": clase_aux, "valor_modelo": vK,
               "comprobacion": dict(fx.COMPROBADA), "incidencia": None}
        if clase_aux in ("convencion", "hipotesis"):
            aux["hipotesis"] = {"fundamento": "x", "alternativas": ["x"], "limites": ["x"]}
        else:
            aux["justificacion"] = "x"
        g["entradas"].append(aux)
        e = ent(g, K); e["fuente"] = {}
        e.update(clase="derivado", derivacion={"origenes": ["aux:sf"], "formula": 'o["aux:sf"]', "conciliacion": "x"})
    r = con(via_aux, resellar=True)
    caso(f"B · {K} como derivado de un auxiliar «{clase_aux}» con valor_modelo = {vK} y sin fuente (sin justificacion_clase)", r)


def todos_aux_ausente(g):
    for i, k in enumerate(datos_calc):
        a = f"aux:n{i}"
        g["entradas"].append({"celda": a, "id": a, "ambito": "auxiliar", "uso": "x", "material": True, "clase": "dato_ausente", "valor_modelo": inst["celdas"][k],
                              "justificacion": "x", "comprobacion": dict(fx.COMPROBADA), "incidencia": None})
        e = ent(g, k); e["fuente"] = {}
        e.update(clase="derivado", derivacion={"origenes": [a], "formula": f'o["{a}"]', "conciliacion": "x"})


r = con(todos_aux_ausente, resellar=True)
print(f"[B · TODOS los datos numéricos publicados del cálculo ({len(datos_calc)}) como derivados de un auxiliar «dato_ausente» con el número y justificación «x» (sin fuente)] {resumen(r)}")
print("      datos_como_hipotesis:", len(r["datos_como_hipotesis"]), "| auxiliares:", r["auxiliares"], "| resumen:", r["resumen"])

print("\n=== C · cadenas de auxiliares (indirecto) y mezcla con un origen publicado")


def cadena(g, niveles, just=None, mezcla=False):
    g["entradas"].append({"celda": "aux:conv", "id": "aux:conv", "ambito": "auxiliar", "uso": "x", "material": True, "clase": "convencion", "valor_modelo": vK,
                          "hipotesis": {"fundamento": "x", "alternativas": ["x"], "limites": ["x"]}, "comprobacion": dict(fx.COMPROBADA, revisor=None, resultado=None), "incidencia": None})
    previo = "aux:conv"
    for i in range(niveles):
        a = f"aux:d{i}"
        g["entradas"].append({"celda": a, "id": a, "ambito": "auxiliar", "uso": "x", "material": True, "clase": "derivado", "valor_modelo": vK,
                              "derivacion": {"origenes": [previo], "formula": f'o["{previo}"]', "conciliacion": "x"}, "comprobacion": dict(fx.COMPROBADA), "incidencia": None})
        previo = a
    e = ent(g, K); e["fuente"] = {}
    if mezcla:  # 849,697 + 2020 − 2019 − 1: los tres orígenes influyen y el 1 es una constante admitida
        e.update(clase="derivado", derivacion={"origenes": [previo, "Historia!G5", ORIG], "formula": f'o["{previo}"] + o["Historia!G5"] - o["{ORIG}"] - 1', "conciliacion": "x"})
    else:
        e.update(clase="derivado", derivacion={"origenes": [previo], "formula": f'o["{previo}"]', "conciliacion": "x"})
    if just:
        e["justificacion_clase"] = just


for niveles in (1, 2, 4):
    r = con(lambda g: cadena(g, niveles), resellar=True)
    caso(f"C · {K} ← {niveles} auxiliar(es) derivado(s) ← aux «convención», sin justificacion_clase", r)
r = con(lambda g: cadena(g, 2, just="x"), resellar=True)
caso("C · ídem (2 niveles) con justificacion_clase «x»", r)
r = con(lambda g: cadena(g, 1, mezcla=True), resellar=True)
caso("C · mezcla: derivado de [aux derivado de convención, celda publicada], sin justificacion_clase", r)


KH = next(k for k, t in inst["tipos"].items() if t == "hipótesis" and isinstance(inst["celdas"][k], (int, float)) and inst["celdas"][k])
V_DIF = round(vK - inst["celdas"][KH], 6)
CITA_DIF = f"Partida sintética aux:dif: {round(V_DIF * 1000, 6):.3f}"
PAG_DIF = fx.nueva_pagina(CITA_DIF)  # vuelve a sellar el registro base (el mismo objeto REG)
print("KH (celda hipótesis del universo):", KH, inst["celdas"][KH], "| aux:dif =", V_DIF)


def via_hipotesis_del_universo(g, just=None):
    g["entradas"].append({"celda": "aux:dif", "id": "aux:dif", "ambito": "auxiliar", "uso": f"origen de {K}", "material": True, "clase": "dato_publicado", "valor_modelo": V_DIF,
                          "comprobacion": dict(fx.COMPROBADA), "incidencia": None,
                          "fuente": dict(copy.deepcopy(ent(REG, K)["fuente"]), valor_fuente=round(V_DIF * 1000, 6), cita=CITA_DIF, pagina=PAG_DIF)})
    e = ent(g, K); e["fuente"] = {}
    e.update(clase="derivado", derivacion={"origenes": ["aux:dif", KH], "formula": f'o["aux:dif"] + o["{KH}"]', "conciliacion": "x", "unidad": "mm"})
    if just:
        e["justificacion_clase"] = just


r = con(via_hipotesis_del_universo, resellar=True)
caso("C · derivado de [auxiliar publicado, celda HIPÓTESIS del universo] (los dos influyen), sin justificacion_clase", r)
r = con(lambda g: via_hipotesis_del_universo(g, just="x"), resellar=True)
caso("C · ídem con justificacion_clase «x»", r)

print("\n=== D · «origenes» que no es una lista (objeto JSON): ¿sigue el vínculo del derivado a su origen? (hallazgo 9 de la primera pasada)")
AUXP = {"celda": "aux:p", "id": "aux:p", "ambito": "auxiliar", "uso": f"origen de {K}", "material": True, "clase": "dato_publicado", "valor_modelo": vK,
        "comprobacion": dict(fx.COMPROBADA), "incidencia": None, "fuente": dict(copy.deepcopy(ent(REG, K)["fuente"]))}


def derivado_de_aux(g, origenes):
    g["entradas"].append(copy.deepcopy(AUXP))
    e = ent(g, K); e["fuente"] = {}
    e.update(clase="derivado", derivacion={"origenes": origenes, "formula": 'o["aux:p"]', "conciliacion": "x", "unidad": "mm"})


for etiqueta, origenes in (("lista (forma normal)", ["aux:p"]), ("objeto {\"aux:p\": null}", {"aux:p": None})):
    reg = copy.deepcopy(REG)
    derivado_de_aux(reg, origenes)
    fx.sellar_todo(reg)
    fx.escribir(reg)
    r0 = VE.comprobar(fx.c)
    # cambia la evidencia del ORIGEN (otro concepto y ubicación, mismo número) y se vuelve a sellar SOLO el origen
    ea = ent(reg, "aux:p")
    ea["fuente"].update(concepto="OTRO concepto (cambio de evidencia)", ubicacion="otra tabla")
    hs = VE.huellas_registro(fx.c, reg)
    ea["comprobacion"]["vinculo"] = {"huella": hs["aux:p"], "sellado_por": ea["comprobacion"]["revisor"], "fecha": ea["comprobacion"]["fecha"]}
    fx.escribir(reg)
    r1 = VE.comprobar(fx.c)
    print(f"[D · «origenes» como {etiqueta}] antes: {resumen(r0, K, 120)}")
    print(f"      tras cambiar la evidencia del origen y resellar SOLO el origen: {resumen(r1, K, 160)}")

print("\n=== E · casos legítimos que no deben romperse")
a, b = round(vK - 100.25, 3), 100.25
CITA = {v: f"Partida sintética: {round(v * 1000, 6):.3f}" for v in (a, b)}
PAG = {v: fx.nueva_pagina(CITA[v]) for v in (a, b)}  # las páginas se añaden ANTES (nueva_pagina vuelve a sellar el registro base)
REG = fx.REG


def legit(g, formula, origenes, vals):
    for a_, v in vals.items():
        g["entradas"].append(dict(copy.deepcopy(AUXP), celda=a_, id=a_, valor_modelo=v,
                                  fuente=dict(copy.deepcopy(ent(REG, K)["fuente"]), valor_fuente=round(v * 1000, 6), cita=CITA[v], pagina=PAG[v])))
    e = ent(g, K); e["fuente"] = {}
    e.update(clase="derivado", derivacion={"origenes": origenes, "formula": formula, "conciliacion": "x", "unidad": "mm"})


for etiqueta, formula, origenes in (("suma de dos orígenes", 'o["aux:a"] + o["aux:b"]', ["aux:a", "aux:b"]),
                                    ("un origen usado dos veces", '(o["aux:a"] + o["aux:b"]) * o["aux:a"] / o["aux:a"]', ["aux:a", "aux:b"]),
                                    ("sum([...]) y comillas simples", "sum([o['aux:a'], o['aux:b']])", ["aux:a", "aux:b"]),
                                    ("origen repetido en la lista", 'o["aux:a"] + o["aux:b"]', ["aux:a", "aux:b", "aux:a"]),
                                    ("constante de escala legítima", '(o["aux:a"] + o["aux:b"]) * 1000 / 1000', ["aux:a", "aux:b"]),
                                    ("origen declarado y NO usado (documental)", 'o["aux:a"] + 100.25', ["aux:a", "aux:b"])):
    r = con(lambda g: legit(g, formula, origenes, {"aux:a": a, "aux:b": b}), resellar=True)
    caso(f"E · {etiqueta}: {formula}", r)
fx.limpiar()
