"""Sondas complementarias (árbol CONGELADO): residuos de los hallazgos 1, 2, 5 y 12."""
import copy, hashlib, json, os, shutil, sys
import fx3 as fx
from fx3 import VE, con, ent, con_k, resumen, K, REG, c, FS, nueva_pagina


def caso(nombre, r, k=K):
    print(f"[{nombre}] {resumen(r, k)}")


# h12: «PDF» de bytes ajenos + archivo_texto con su huella VIGENTE
open(os.path.join(FS, "otro.pdf"), "wb").write(b"%PDF-1.4 contenido que no tiene nada que ver\n")
sha_pdf = hashlib.sha256(open(os.path.join(FS, "otro.pdf"), "rb").read()).hexdigest()
sha_txt = hashlib.sha256(open(os.path.join(FS, "fuente.txt"), "rb").read()).hexdigest()
r = con(lambda g: ent(g, K)["fuente"].update(archivo="fuentes_sinteticas/otro.pdf", sha256=sha_pdf, archivo_texto="fuentes_sinteticas/fuente.txt", sha256_texto=sha_txt), resellar=True)
caso("h12 «PDF» de bytes ajenos + archivo_texto sintético con su huella vigente (nada vincula el texto con el PDF)", r)

# h2: variantes del reetiquetado
k0 = next(e["celda"] for e in REG["entradas"] if e["clase"] == "cero_comprobado" and fx.inst["ambito"][e["celda"]] == "calculo")
ceros_calc = [e["celda"] for e in REG["entradas"] if e["clase"] == "cero_comprobado" and fx.inst["ambito"][e["celda"]] == "calculo"]
print("ceros del universo de cálculo:", len(ceros_calc), ceros_calc[:6])
def ceros_no_aplicables(g):
    for k in ceros_calc:
        e = ent(g, k); e["fuente"] = {}; e.update(clase="no_aplicable", justificacion="x")
r = con(ceros_no_aplicables, resellar=True); print(f"[h2 TODOS los ceros del cálculo ({len(ceros_calc)}) como «no_aplicable» con justificación «x» (sin fuente; comprobación completa del fixture)] {resumen(r)}")
def ceros_no_aplicables_sin_revisor(g):
    ceros_no_aplicables(g)
    for k in ceros_calc:
        ent(g, k)["comprobacion"].update(revisor=None, resultado=None, fuente_examinada=None)
r = con(ceros_no_aplicables_sin_revisor, resellar=True); print(f"[h2 ídem sin revisor] {resumen(r)}")

datos_calc = [e["celda"] for e in REG["entradas"] if e["clase"] == "dato_publicado" and fx.inst["ambito"][e["celda"]] == "calculo" and isinstance(e["valor_modelo"], (int, float))]
print("datos publicados numéricos del universo de cálculo:", len(datos_calc))
def derivados_de_aux_convencion(g, sin_revisor_derivado=False):
    for i, k in enumerate(datos_calc):
        e = ent(g, k); e["fuente"] = {}
        a = f"aux:c{i}"
        g["entradas"].append({"celda": a, "id": a, "ambito": "auxiliar", "uso": "x", "material": True, "clase": "convencion", "valor_modelo": fx.inst["celdas"][k],
                              "hipotesis": {"fundamento": "x", "alternativas": ["x"], "limites": ["x"]}, "comprobacion": {"extractor": "e", "revisor": None, "fecha": None, "resultado": None, "fuente_examinada": None}})
        e.update(clase="derivado", derivacion={"origenes": [a], "formula": f'o["{a}"]', "conciliacion": "x"})
        if sin_revisor_derivado:
            e["comprobacion"].update(revisor=None, resultado=None, fuente_examinada=None)
r = con(derivados_de_aux_convencion, resellar=True)
print(f"[h2 TODOS los datos numéricos del cálculo ({len(datos_calc)}) como DERIVADOS de un auxiliar «convención» sin fuente, sin justificacion_clase y sin revisor en el auxiliar (el derivado conserva la comprobación del fixture)] {resumen(r)}")
print("   datos_como_hipotesis:", len(r["datos_como_hipotesis"]), "| auxiliares:", r["auxiliares"], "| motivo:", r["motivo"])
r = con(lambda g: derivados_de_aux_convencion(g, True), resellar=True); print(f"[h2 ídem sin revisor tampoco en el derivado] {resumen(r)}")
# derivado con fórmula constante (sin usar el origen)
def derivado_constante(g):
    e = ent(g, K); e["fuente"] = {}
    k2 = "Historia!C5"
    e.update(clase="derivado", derivacion={"origenes": [k2], "formula": f'{fx.inst["celdas"][K]!r}', "conciliacion": "x"})
r = con(derivado_constante, resellar=True); caso("h2 dato de cálculo como DERIVADO con fórmula CONSTANTE (no usa su origen)", r)

# h5: derivado de tasa con redondeo no declarado, y de importe
k_t = "Análisis!C57"; vm_t = fx.inst["celdas"][k_t]
print("C57 libro:", vm_t)
def tasa_derivada(g, aux_v, formula):
    e = ent(g, k_t); e["fuente"] = {}
    pg = ent(REG, K)["fuente"]
    g["entradas"].append({"celda": "aux:tasa", "id": "aux:tasa", "ambito": "auxiliar", "uso": "x", "material": True, "clase": "convencion", "valor_modelo": aux_v,
                          "hipotesis": {"fundamento": "x", "alternativas": ["x"], "limites": ["x"]}, "comprobacion": {"extractor": "e"}})
    e.update(clase="derivado", derivacion={"origenes": ["aux:tasa"], "formula": formula, "conciliacion": "x"})
for aux_v in (3.354, 3.346, 3.31, 3.36):
    r = con(lambda g: tasa_derivada(g, aux_v, 'o["aux:tasa"] / 100'), resellar=True)
    caso(f"h5 DERIVADO: tasa del libro {vm_t} = o[aux]/100 con aux = {aux_v} % (sin round declarado)", r, k_t)
fx.limpiar()
