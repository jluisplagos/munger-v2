"""Sondas R1–R3 de extremo a extremo sobre el árbol CONGELADO (arnés fx2.py). Hallazgos 1, 2, 5, 10, 11, 12, 18 y observación 20."""
import copy, hashlib, json, os, shutil, sys
import fx2 as fx
from fx2 import VE, con, ent, con_k, resumen, K, REG, c, FS, nueva_pagina


def caso(nombre, r, k=K):
    print(f"[{nombre}] {resumen(r, k)}")


r = con(); caso("control positivo", r)
k_txt = next(e["celda"] for e in REG["entradas"] if e["clase"] == "dato_publicado" and not isinstance(e["valor_modelo"], (int, float)))
KJ = next(e["celda"] for e in REG["entradas"] if e["ambito"] == "juicio" and e["clase"] == "dato_publicado" and isinstance(e["valor_modelo"], (int, float)))
vf0 = ent(REG, K)["fuente"]["valor_fuente"]; vm0 = fx.inst["celdas"][K]
print("K:", K, "vm", vm0, "vf", vf0, "| KJ:", KJ, fx.inst["celdas"][KJ], "| k_txt:", k_txt, fx.inst["celdas"][k_txt])

print("\n=== HALLAZGO 1 · material:false")
r = con(lambda g: (ent(g, K)["fuente"].update(archivo="fuentes_sinteticas/NO_EXISTE.txt", sha256=None), ent(g, K).update(material=False)))
caso("h1 R2 fuente local AUSENTE + material:false en CÁLCULO (sin revisor ni sello)", r)
r = con(lambda g: (ent(g, K)["fuente"].update(pagina="22-23"), ent(g, K).update(material=False)))
caso("h1 R1 página no inequívoca + material:false en CÁLCULO", r)
n_mf = [0]
def todo_no_material(g):
    for e in g["entradas"]:
        if e["clase"] in ("dato_publicado", "cero_comprobado"):
            e["material"] = False; e["fuente"].update(archivo="fuentes_sinteticas/NO_EXISTE.txt", sha256=None); n_mf[0] += 1
r = con(todo_no_material); print(f"[h1 TODOS los datos publicados ({n_mf[0]}) con fuente ausente y material:false] {resumen(r)}")
# juicio: material:false con justificación, fuente ausente, sin revisor ni sello
def juicio_no_material(g, k=KJ, just="cifra de contexto"):
    e = ent(g, k); e["material"] = False; e["justificacion_materialidad"] = just
    e["fuente"].update(archivo="fuentes_sinteticas/NO_EXISTE.txt", sha256=None)
    e["comprobacion"] = {"extractor": "extractor sintético", "revisor": None, "fecha": None, "resultado": "pendiente", "fuente_examinada": None}
r = con(juicio_no_material); caso("h1 JUICIO: material:false con una justificación de dos palabras, fuente ausente, comprobación pendiente, sin revisor ni sello", r, KJ)
n_j = [0]
def todo_juicio_no_material(g):
    for e in g["entradas"]:
        if e.get("ambito") == "juicio" and e["clase"] in ("dato_publicado", "cero_comprobado"):
            juicio_no_material(g, e["celda"], "x"); n_j[0] += 1
r = con(todo_juicio_no_material); print(f"[h1 TODAS las entradas de juicio con dato ({n_j[0]}) como no materiales («x»), fuente ausente, sin revisor] {resumen(r)}")
print("   motivo:", r["motivo"]); print("   no_materiales listadas:", len(r["no_materiales"]))
# aux: material false
print("\n=== HALLAZGO 2 · reetiquetado")
def a_convencion(g, k=K, just=None, revisor=True):
    e = ent(g, k); e["fuente"] = {}
    e.update(clase="convencion", hipotesis={"fundamento": "tratamiento del inversor", "alternativas": ["otra"], "limites": ["ninguno"]})
    if just:
        e["justificacion_clase"] = just
    if not revisor:
        e["comprobacion"].update(extractor="extractor", revisor=None, resultado=None, fuente_examinada=None)
r = con(a_convencion, resellar=True); caso("h2 dato de cálculo (ventas 2019) como CONVENCIÓN, sin fuente ni justificacion_clase", r)
r = con(lambda g: a_convencion(g, just="x", revisor=False), resellar=True); caso("h2 ídem con justificacion_clase «x» pero sin revisor ni resultado", r)
r = con(lambda g: a_convencion(g, just="x"), resellar=True); caso("h2 ídem con justificacion_clase «x» y la comprobación completa del fixture (revisor ≠ extractor, verificado, fuente examinada)", r)
n_c = [0]
def todo_convencion(g):
    for e in g["entradas"]:
        if e["clase"] in ("dato_publicado", "cero_comprobado"):
            a_convencion(g, e["celda"], just="x"); n_c[0] += 1
r = con(todo_convencion, resellar=True); print(f"[h2 TODOS los datos publicados ({n_c[0]}) como convención con justificacion_clase «x» y comprobación completa, sin fuente] {resumen(r)}")
print("   motivo:", r["motivo"])
def a_no_aplicable(g, k=K):
    e = ent(g, k); e["fuente"] = {}; e.update(clase="no_aplicable", justificacion="no aplica")
r = con(a_no_aplicable, resellar=True); caso("h2 dato de cálculo con valor como NO_APLICABLE", r)
k0 = next(e["celda"] for e in REG["entradas"] if e["clase"] == "cero_comprobado")
r = con(lambda g: a_no_aplicable(g, k0), resellar=True); caso(f"h2 un CERO del libro ({k0}) como NO_APLICABLE (sin fuente)", r, k0)
def a_dato_ausente(g, k=K):
    e = ent(g, k); e["fuente"] = {}; e.update(clase="dato_ausente", justificacion="no se publica")
r = con(a_dato_ausente, resellar=True); caso("h2 dato de cálculo con valor como DATO_AUSENTE", r)
r = con(lambda g: a_no_aplicable(g, k_txt), resellar=True); caso(f"h2 dato de TEXTO ({k_txt}) como NO_APLICABLE", r, k_txt)
def a_derivado_const(g, k=K):
    e = ent(g, k); e["fuente"] = {}
    e.update(clase="derivado", derivacion={"origenes": [k], "formula": str(fx.inst["celdas"][k]), "conciliacion": "x"})
# derivado con fórmula constante y origen ficticio aux: hipótesis
def a_derivado_aux(g, k=K):
    e = ent(g, k); e["fuente"] = {}
    g["entradas"].append({"celda": "aux:const", "id": "aux:const", "ambito": "auxiliar", "uso": "x", "material": True, "clase": "convencion", "valor_modelo": fx.inst["celdas"][k],
                          "hipotesis": {"fundamento": "x", "alternativas": ["x"], "limites": ["x"]}, "comprobacion": {"extractor": "e", "revisor": None, "fecha": None, "resultado": None, "fuente_examinada": None}})
    e.update(clase="derivado", derivacion={"origenes": ["aux:const"], "formula": 'o["aux:const"]', "conciliacion": "x"})
r = con(a_derivado_aux, resellar=True); caso("h2 (variante) dato de cálculo como DERIVADO de un auxiliar «convención» sin fuente ni revisor", r)

print("\n=== HALLAZGO 5 · tolerancias")
print("VE._igual_exacto(0.25, 0.2511)", VE._igual_exacto(0.25, 0.2511), "| _igual_libro(0.2511, 0.25)", VE._igual_libro(0.2511, 0.25), "| _igual_libro(0.2504, 0.25)", VE._igual_libro(0.2504, 0.25),
      "| _igual_libro(0.0334, 0.033)", VE._igual_libro(0.0334, 0.033), "| _igual_libro(0.001, 0)", VE._igual_libro(0.001, 0), "| _igual_libro(0.0004, 0)", VE._igual_libro(0.0004, 0))
k_t = "Análisis!C57"; vm_t = fx.inst["celdas"][k_t]; print("tasa sin riesgo del libro:", vm_t, "| clase", ent(REG, k_t)["clase"], "| ámbito", fx.inst["ambito"][k_t])
vf_t = round(vm_t - 0.001, 6)
pt = nueva_pagina(f"Rentabilidad del bono a 10 años: {vf_t*100:.2f} %".replace(".", ","))
def tasa(g, unidad="%"):
    ent(g, k_t)["fuente"].update(pagina=pt, unidad=unidad, escala=0.01, valor_fuente=round(vf_t * 100, 4), cita=f"Rentabilidad del bono a 10 años: {vf_t*100:.2f} %".replace(".", ","))
r = con(tasa, resellar=True); caso(f"h5 tasa del libro {vm_t} contrastada con una fuente que publica {vf_t*100:.2f} % (0,10 pp menos)", r, k_t)
k_g = "Análisis!C68"; print("g NORMAL del libro:", fx.inst["celdas"].get(k_g), "| clase", ent(REG, k_g)["clase"])
r = con(lambda g: ent(g, k_g).update(valor_modelo=round(fx.inst["celdas"][k_g] - 0.001, 6)), resellar=True); caso(f"h5 vigencia: registro con g = {round(fx.inst['celdas'][k_g] - 0.001, 6)} y libro con {fx.inst['celdas'][k_g]}", r, k_g)
r = con(lambda g: ent(g, K)["fuente"].update(unidad="euros"), resellar=True); caso("h5 unidades: la misma cifra (miles) declarada en «euros» con escala 0,001", r)
# tasa con 4 decimales: el libro la tiene redondeada a 3 → ¿se acepta sin transformación? (dato publicado, unidad no monetaria)
k_t2 = next((e["celda"] for e in REG["entradas"] if e["clase"] == "dato_publicado" and isinstance(e["valor_modelo"], float) and 0 < abs(e["valor_modelo"]) < 1 and round(e["valor_modelo"], 3) == e["valor_modelo"]), None)
print("tasa/ratio del libro con ≤ 3 decimales:", k_t2, fx.inst["celdas"].get(k_t2) if k_t2 else None)
if k_t2:
    v2 = fx.inst["celdas"][k_t2]
    vfp = round(v2 * 100 + 0.04, 4)   # la fuente publica 0,04 pp más (se redondea al mismo valor a 3 decimales)
    p2 = nueva_pagina(f"Tipo sintético: {vfp:.2f} %")
    r = con(lambda g: ent(g, k_t2)["fuente"].update(pagina=p2, unidad="porcentaje", escala=0.01, valor_fuente=vfp, cita=f"Tipo sintético: {vfp:.2f} %"), resellar=True)
    caso(f"h5 DATO PUBLICADO: ratio del libro {v2} con una fuente que publica {vfp:.2f} % (unidad «porcentaje»: no es importe)", r, k_t2)
    r = con(lambda g: ent(g, k_t2)["fuente"].update(pagina=p2, unidad="mm", escala=0.01, valor_fuente=vfp, cita=f"Tipo sintético: {vfp:.2f} %"), resellar=True)
    caso(f"h5 ídem declarando la unidad «mm» (monetaria) con escala 0,01", r, k_t2)
    r = con(lambda g: ent(g, k_t2)["fuente"].update(pagina=p2, unidad="millones", escala=1.0, valor_fuente=round(vfp / 100, 6), cita=f"Tipo sintético: {vfp:.2f} %"), resellar=True)
    caso(f"h5 ídem con unidad «millones», escala 1 y valor_fuente {round(vfp / 100, 6)} (la cita no lo contiene: solo interesa el producto)", r, k_t2)
    # DERIVADO: ratio derivado de un auxiliar con más decimales, sin round declarado
    def ratio_derivado(g):
        e = ent(g, k_t2); e["fuente"] = {}
        pa = None
        g["entradas"].append({"celda": "aux:ratio", "id": "aux:ratio", "ambito": "auxiliar", "uso": "x", "material": True, "clase": "dato_publicado", "valor_modelo": round(vfp / 100, 6),
                              "fuente": dict(ent(REG, K)["fuente"], pagina=p2, unidad="porcentaje", escala=0.01, valor_fuente=vfp, cita=f"Tipo sintético: {vfp:.2f} %", periodo="31-dic-2025", columna="31-dic-2025"),
                              "comprobacion": dict(fx.COMPROBADA), "incidencia": None})
        e.update(clase="derivado", derivacion={"origenes": ["aux:ratio"], "formula": 'o["aux:ratio"]', "conciliacion": "el mismo tipo"})
    r = con(ratio_derivado, resellar=True)
    caso(f"h5 DERIVADO: ratio del libro {v2} = o[aux] con aux = {round(vfp / 100, 6)} (0,04 pp más), SIN round declarado en la fórmula", r, k_t2)

print("\n=== HALLAZGO 10 · decimales")
for cita, v in [("Ingresos: 1.234.567.890", 1234567890.45), ("Ingresos: 100.000.000", 100000000.1), ("Ingresos: 10.000.000", 10000000.01), ("Tasa: 54,7", 54.70000001), ("Partida: 0", 4.9e-10),
                ("x 0,12345678901", 0.12345678901), ("x 0,12345679", 0.12345678901), ("x 0,1234567890", 0.123456789), ("x 1e-07", 1e-07), ("x 0,0000001", 1e-07), ("x 123456789012345680", 1.2345678901234568e17),
                ("x 0,30000000000000004", 0.1 + 0.2), ("x 0,3", 0.1 + 0.2)]:
    print(f"   _cita_contiene({cita!r}, {v!r}) = {VE._cita_contiene(cita, v)}")
vf_e = round(vm0 * 1e6 + 0.45, 2)
pe = nueva_pagina(f"Importe neto de la cifra de negocios: {round(vf_e):,}".replace(",", "."))
r = con(lambda g: ent(g, K)["fuente"].update(pagina=pe, unidad="euros", escala=1e-6, valor_fuente=vf_e, cita=f"Importe neto de la cifra de negocios: {round(vf_e):,}".replace(",", ".")), resellar=True)
caso(f"h10 valor_fuente {vf_e!r} € con una cita que solo trae {round(vf_e):,} (céntimos redondeados)", r)
pe2 = nueva_pagina(f"Importe neto de la cifra de negocios: {vf_e:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
r = con(lambda g: ent(g, K)["fuente"].update(pagina=pe2, unidad="euros", escala=1e-6, valor_fuente=vf_e, cita=f"Importe neto de la cifra de negocios: {vf_e:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")), resellar=True)
caso(f"h10/h5 positivo: valor_fuente {vf_e!r} € con la cita completa y el libro en mm con 3 decimales ({vm0})", r)

print("\n=== HALLAZGO 11 · rutas")
fuera = "/tmp/rev_fable2/fuera_del_paquete"; os.makedirs(fuera, exist_ok=True)
shutil.copy(os.path.join(FS, "fuente.txt"), os.path.join(fuera, "fuente_ajena.txt"))
r = con(lambda g: ent(g, K)["fuente"].update(archivo=os.path.join(fuera, "fuente_ajena.txt")), resellar=True); caso("h11 fuente «local» con ruta ABSOLUTA fuera del expediente y del paquete", r)
rel = os.path.relpath(os.path.join(fuera, "fuente_ajena.txt"), c)
r = con(lambda g: ent(g, K)["fuente"].update(archivo=rel), resellar=True); caso(f"h11 ruta relativa que sale del expediente ({rel[:40]}…)", r)
rel_pv = os.path.relpath(os.path.join(fuera, "fuente_ajena.txt"), fx.PV)
r = con(lambda g: ent(g, K)["fuente"].update(archivo=rel_pv), resellar=True); caso(f"h11 ruta relativa a personaje_v2/ que sale del paquete ({rel_pv[:40]}…)", r)
os.symlink(os.path.join(fuera, "fuente_ajena.txt"), os.path.join(FS, "enlace.txt"))
r = con(lambda g: ent(g, K)["fuente"].update(archivo="fuentes_sinteticas/enlace.txt"), resellar=True); caso("h11 enlace simbólico dentro del expediente que apunta fuera", r)
os.remove(os.path.join(FS, "enlace.txt"))
r = con(lambda g: ent(g, K)["fuente"].update(archivo="fuentes_sinteticas/../fuentes_sinteticas/fuente.txt"), resellar=True); caso("h11 positivo: ruta con «..» que queda dentro del expediente", r)
sha_txt = hashlib.sha256(open(os.path.join(FS, "fuente.txt"), "rb").read()).hexdigest()
open(os.path.join(FS, "otro.pdf"), "wb").write(b"%PDF-1.4 contenido que no tiene nada que ver\n")
sha_pdf = hashlib.sha256(open(os.path.join(FS, "otro.pdf"), "rb").read()).hexdigest()
r = con(lambda g: ent(g, K)["fuente"].update(archivo="fuentes_sinteticas/otro.pdf", sha256=sha_pdf, archivo_texto=os.path.join(fuera, "fuente_ajena.txt"), sha256_texto=sha_txt), resellar=True)
caso("h11 «archivo_texto» con ruta absoluta fuera del paquete", r)

print("\n=== HALLAZGO 12 · texto y fuentes no textuales")
print("dato de texto:", k_txt, ent(REG, k_txt)["valor_modelo"], "| cita:", ent(REG, k_txt)["fuente"]["cita"])
pg = nueva_pagina("Texto cualquiera de otra cosa, sin el dato")
r = con(lambda g: ent(g, k_txt)["fuente"].update(pagina=pg, cita="Texto cualquiera de otra cosa"), resellar=True); caso("h12 dato de TEXTO con cita que NO contiene el valor", r, k_txt)
r = con(lambda g: ent(g, k_txt)["fuente"].update(cita=" "), resellar=True); caso("h12 dato de TEXTO con cita de un espacio", r, k_txt)
r = con(lambda g: ent(g, K)["fuente"].update(cita=" "), resellar=True); caso("h12 dato NUMÉRICO con cita de un espacio", r)
vtxt = str(ent(REG, k_txt)["valor_modelo"])
pg2 = nueva_pagina(f"Informe en N{vtxt}ROS y otras cosas")
r = con(lambda g: ent(g, k_txt)["fuente"].update(pagina=pg2, cita=f"Informe en N{vtxt}ROS"), resellar=True); caso(f"h12 dato de TEXTO «{vtxt}» contenido como subcadena de otra palabra («N{vtxt}ROS»)", r, k_txt)
pg3 = nueva_pagina("Moneda: dólares")
r = con(lambda g: ent(g, k_txt)["fuente"].update(pagina=pg3, cita="Moneda: dólares", equivalencia="dólares"), resellar=True); caso(f"h12 dato de TEXTO «{vtxt}» con cita «Moneda: dólares» y equivalencia declarada «dólares» (la equivalencia es texto libre del extractor)", r, k_txt)
r = con(lambda g: ent(g, K)["fuente"].update(archivo="fuentes_sinteticas/otro.pdf", sha256=sha_pdf, archivo_texto="fuentes_sinteticas/fuente.txt", sha256_texto=sha_txt), resellar=True)
caso("h12 «PDF» de bytes ajenos + archivo_texto sintético con su huella (nada los vincula)", r)

print("\n=== HALLAZGO 18 · formatos legítimos")
for cita, v in [("x 849 697.0", 849697), ("x 1 234 567.89", 1234567.89), ("x 45'479.209", 45479.209), ("x 149,5000000", 149.5), ("x 849.697,0", 849697), ("x 1’234.5", 1234.5), ("x 1.234.567", 1234567), ("x 1 234 567", 1234567),
                ("x 12,5%", 12.5), ("x €1,234.5", 1234.5), ("x 1,234.5m", 1234.5), ("x (1.234,5)", 1234.5), ("x -1.234,5", 1234.5), ("x 1.234,5-", 1234.5)]:
    print(f"   _cita_contiene({cita!r}, {v!r}) = {VE._cita_contiene(cita, v)}")
r = con(lambda g: ent(g, K)["fuente"].update(sha256=ent(g, K)["fuente"]["sha256"].upper()), resellar=True); caso("h18 sha256 en MAYÚSCULAS (mismo valor)", r)
for p in ["p. 22", "pág. 22", "22.0", "PDF22", "pdf pág. 22", "PDF page 22", " 22 ", "022", 22.0, "２２"]:
    print(f"   _numero_pagina({p!r}) = {VE._numero_pagina(p)}")
r = con(lambda g: ent(g, K)["fuente"].update(pagina="p. " + ent(g, K)["fuente"]["pagina"]), resellar=True); caso("h18 página «p. n»: mensaje", r)
open(os.path.join(FS, "sin_marcas.txt"), "w", encoding="utf-8").write(ent(REG, K)["fuente"]["cita"] + "\n")
sha_sm = hashlib.sha256(open(os.path.join(FS, "sin_marcas.txt"), "rb").read()).hexdigest()
r = con(lambda g: ent(g, K)["fuente"].update(archivo="fuentes_sinteticas/sin_marcas.txt", sha256=sha_sm, pagina=1), resellar=True); caso("h18 .txt SIN marcas de página, página 1", r)

print("\n=== OBSERVACIÓN 20 (no declarada como corregida) · estado actual")
for cita, v in [("Deuda neta - total: 12,3", 0), ("12,3 - 4,5", 0), ("x 1.234", 1.234), ("x 1.234", 1234), ("(149,5)", 149.5), ("(149,5)", -149.5)]:
    print(f"   _cita_contiene({cita!r}, {v!r}) = {VE._cita_contiene(cita, v)}")
fx.limpiar()
