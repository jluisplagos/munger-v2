"""Sondas R1–R3 de extremo a extremo (arnés fx.py; copia en /tmp)."""
import copy, hashlib, json, os, shutil, sys
import fx
from fx import VE, con, ent, con_k, resumen, K, REG, c, FS, nueva_pagina

def caso(nombre, r, k=K):
    print(f"[{nombre}] {resumen(r, k)}")

r = con(); caso("control positivo", r)

# ---------- R1
print("\n=== R1")
for p in ["p. 22", "pág. 22", "22.0", "PDF22", "２２", " 22 ", "022"]:
    r = con(lambda g: ent(g, K)["fuente"].update(pagina=p), resellar=True); caso(f"R1 página {p!r} (resellada)", r)
# marcas duplicadas: la primera gana
txt = open(os.path.join(FS, "fuente.txt"), encoding="utf-8").read()
# dato de TEXTO cuya cita no contiene el valor
k_txt = next(e["celda"] for e in REG["entradas"] if e["clase"] == "dato_publicado" and not isinstance(e["valor_modelo"], (int, float)))
print("dato de texto:", k_txt, ent(REG, k_txt)["valor_modelo"], "| cita:", ent(REG, k_txt)["fuente"]["cita"])
pg = nueva_pagina("Texto cualquiera de otra cosa, sin el dato")
r = con(lambda g: ent(g, k_txt)["fuente"].update(pagina=pg, cita="Texto cualquiera de otra cosa"), resellar=True); caso("R1 dato de TEXTO con cita que NO contiene el valor", r, k_txt)
r = con(lambda g: ent(g, k_txt)["fuente"].update(cita=" "), resellar=True); caso("R1 dato de TEXTO con cita de un espacio", r, k_txt)
# PDF con archivo_texto que no procede del PDF
open(os.path.join(FS, "otro.pdf"), "wb").write(b"%PDF-1.4 contenido que no tiene nada que ver\n")
sha_pdf = hashlib.sha256(open(os.path.join(FS, "otro.pdf"), "rb").read()).hexdigest()
sha_txt = hashlib.sha256(open(os.path.join(FS, "fuente.txt"), "rb").read()).hexdigest()
r = con(lambda g: ent(g, K)["fuente"].update(archivo="fuentes_sinteticas/otro.pdf", sha256=sha_pdf, archivo_texto="fuentes_sinteticas/fuente.txt", sha256_texto=sha_txt), resellar=True)
caso("R1 «PDF» de bytes ajenos + archivo_texto sintético (nada los vincula)", r)
# archivo_texto sin marcas / txt sin marcas
open(os.path.join(FS, "sin_marcas.txt"), "w", encoding="utf-8").write(ent(REG, K)["fuente"]["cita"] + "\n")
sha_sm = hashlib.sha256(open(os.path.join(FS, "sin_marcas.txt"), "rb").read()).hexdigest()
r = con(lambda g: ent(g, K)["fuente"].update(archivo="fuentes_sinteticas/sin_marcas.txt", sha256=sha_sm, pagina=1), resellar=True); caso("R1 .txt legítimo SIN marcas de página (p. ej. boletín de mercado), página 1", r)

# ---------- R2
print("\n=== R2")
# ruta absoluta fuera del expediente y del paquete
fuera = "/tmp/rev_fable/fuera_del_paquete"; os.makedirs(fuera, exist_ok=True)
shutil.copy(os.path.join(FS, "fuente.txt"), os.path.join(fuera, "fuente_ajena.txt"))
r = con(lambda g: ent(g, K)["fuente"].update(archivo=os.path.join(fuera, "fuente_ajena.txt")), resellar=True); caso("R2 fuente «local» con ruta ABSOLUTA fuera del expediente y del paquete", r)
rel = os.path.relpath(os.path.join(fuera, "fuente_ajena.txt"), c)
r = con(lambda g: ent(g, K)["fuente"].update(archivo=rel), resellar=True); caso(f"R2 fuente «local» con ruta relativa que sale del paquete ({rel[:40]}…)", r)
# material: false + fuente ausente (sin resellar: nadie revisa)
r = con(lambda g: (ent(g, K)["fuente"].update(archivo="fuentes_sinteticas/NO_EXISTE.txt", sha256=None), ent(g, K).update(material=False)))
caso("R2 fuente local AUSENTE + material:false (sin revisor ni sello)", r)
r = con(lambda g: (ent(g, K)["fuente"].update(pagina="22-23"), ent(g, K).update(material=False)))
caso("R1 página no inequívoca + material:false (sin revisor ni sello)", r)
n_mf = [0]
def todo_no_material(g):
    for e in g["entradas"]:
        if e["clase"] in ("dato_publicado", "cero_comprobado"):
            e["material"] = False; e["fuente"].update(archivo="fuentes_sinteticas/NO_EXISTE.txt", sha256=None); n_mf[0] += 1
r = con(todo_no_material); print(f"[R2 TODOS los datos publicados ({n_mf[0]}) con fuente ausente y material:false] {resumen(r)}")
# clase reetiquetada: dato → convención / hipótesis / no_aplicable
def a_convencion(g, k=K):
    e = ent(g, k); e.pop("fuente", None)
    e.update(clase="convencion", hipotesis={"fundamento": "tratamiento del inversor", "alternativas": ["otra"], "limites": ["ninguno"]})
r = con(a_convencion, resellar=True); caso("dato de cálculo (ventas 2019) reetiquetado como CONVENCIÓN, sin fuente", r)
def a_convencion_sin_revisor(g, k=K):
    a_convencion(g, k); ent(g, k)["comprobacion"].update(extractor="extractor", revisor=None, resultado=None, fuente_examinada=None)
r = con(a_convencion_sin_revisor, resellar=True); caso("ídem sin revisor ni resultado (vínculo calculado a mano)", r)
def a_no_aplicable(g, k=K):
    e = ent(g, k); e.pop("fuente", None); e.update(clase="no_aplicable", justificacion="no aplica")
r = con(a_no_aplicable, resellar=True); caso("dato de cálculo con valor reetiquetado como NO_APLICABLE", r)
n_c = [0]
def todo_convencion(g):
    for e in g["entradas"]:
        if e["clase"] in ("dato_publicado", "cero_comprobado"):
            a_convencion_sin_revisor(g, e["celda"]); n_c[0] += 1
r = con(todo_convencion, resellar=True); print(f"[TODOS los datos publicados ({n_c[0]}) reetiquetados como convención sin fuente ni revisor] {resumen(r)}")
# sha256 en mayúsculas
r = con(lambda g: ent(g, K)["fuente"].update(sha256=ent(g, K)["fuente"]["sha256"].upper()), resellar=True); caso("R2 sha256 en MAYÚSCULAS (mismo valor)", r)
# lectura externa con campos sin sentido
def externa(g, k=K, le=None, material=True):
    f = ent(g, k)["fuente"]
    for x in ("archivo", "sha256"):
        f.pop(x, None)
    f.update(conservacion="externa", lectura_externa=le or {"referencia": "x", "fecha": "ayer", "evidencia": "x", "limitaciones": "ninguna"})
    ent(g, k)["material"] = material
r = con(lambda g: externa(g, material=False), resellar=True); caso("R2 lectura externa NO material con campos vacíos de contenido («x», «ayer», «ninguna»)", r)
n_e = [0]
def todo_externo(g):
    for e in g["entradas"]:
        if e["clase"] in ("dato_publicado", "cero_comprobado"):
            externa(g, e["celda"], material=False); n_e[0] += 1
r = con(todo_externo, resellar=True); print(f"[R2 TODOS los datos publicados ({n_e[0]}) como lectura externa no material] {resumen(r)}")

# ---------- R3
print("\n=== R3")
vf0 = ent(REG, K)["fuente"]["valor_fuente"]; vm0 = fx.inst["celdas"][K]
print("K:", K, "vm", vm0, "vf", vf0)
# (a) tolerancia relativa de _decimales_exactos en magnitudes grandes: fuente en euros
vf_e = round(vm0 * 1e6 + 0.45, 2)   # euros con céntimos
pe = nueva_pagina(f"Importe neto de la cifra de negocios: {round(vf_e):,}".replace(",", "."))
r = con(lambda g: ent(g, K)["fuente"].update(pagina=pe, unidad="euros", escala=1e-6, valor_fuente=vf_e, cita=f"Importe neto de la cifra de negocios: {round(vf_e):,}".replace(",", ".")), resellar=True)
caso(f"R3 valor_fuente {vf_e!r} € con una cita que solo trae {round(vf_e):,} (céntimos redondeados)", r)
# (b) tolerancia absoluta 0,0011 en cifras pequeñas: tasa/ratio
k_t = "Análisis!C57"; vm_t = fx.inst["celdas"][k_t]; print("tasa sin riesgo del libro:", vm_t, "| clase", ent(REG, k_t)["clase"])
vf_t = round(vm_t - 0.001, 6)
pt = nueva_pagina(f"Rentabilidad del bono a 10 años: {vf_t*100:.2f} %".replace(".", ","))
def tasa(g):
    ent(g, k_t)["fuente"].update(pagina=pt, unidad="%", escala=0.01, valor_fuente=round(vf_t * 100, 4), cita=f"Rentabilidad del bono a 10 años: {vf_t*100:.2f} %".replace(".", ","))
r = con(tasa, resellar=True); caso(f"R3 tasa del libro {vm_t} contrastada con una fuente que publica {vf_t*100:.2f} % (0,10 pp menos)", r, k_t)
# (c) vigencia: valor registrado distinto del libro dentro de 0,0011
k_g = "Análisis!C68"; print("g NORMAL del libro:", fx.inst["celdas"].get(k_g), "| clase", ent(REG, k_g)["clase"])
r = con(lambda g: ent(g, k_g).update(valor_modelo=round(fx.inst["celdas"][k_g] - 0.001, 6)), resellar=True); caso(f"vigencia: registro con g = {round(fx.inst['celdas'][k_g] - 0.001, 6)} y libro con {fx.inst['celdas'][k_g]}", r, k_g)
# (d) coherencia de escala vacía por debajo de 0,0021
r = con(lambda g: ent(g, K)["fuente"].update(unidad="euros"), resellar=True); caso("R3/unidades: la misma cifra (miles) declarada en «euros» con escala 0,001", r)
r = con(lambda g: ent(g, K)["fuente"].update(unidad="euros", escala=0.002, valor_fuente=vf0 / 2, cita=f"x {vf0/2:.3f}"), resellar=True); caso("unidades: «euros» con escala 0,002 (cita no está en la página: solo interesa el control de escala)", r)
# (e) separadores ambiguos: 849,697 (mm con decimales) frente a «849.697» miles
pa = nueva_pagina("Importe neto de la cifra de negocios 849.697 912.160")
r = con(lambda g: ent(g, K)["fuente"].update(pagina=pa, unidad="millones de euros", escala=1.0, valor_fuente=849.697, cita="Importe neto de la cifra de negocios 849.697 912.160"), resellar=True)
caso("R3 separador ambiguo: «849.697» (miles, formato español) leído como 849,697 millones", r)
# (f) cero con guion de puntuación
k0 = next(e["celda"] for e in REG["entradas"] if e["clase"] == "cero_comprobado")
p0 = nueva_pagina("Arrendamientos - total de la nota: 12,3")
r = con(lambda g: ent(g, k0)["fuente"].update(pagina=p0, cita="Arrendamientos - total de la nota: 12,3"), resellar=True); caso(f"cero comprobado ({k0}) con un guion de puntuación en la cita", r, k0)
# (g) formato legítimo rechazado: miles con espacio y punto decimal
pf = nueva_pagina(f"Revenue {vf0:,.1f}".replace(",", " "))
r = con(lambda g: ent(g, K)["fuente"].update(pagina=pf, cita=f"Revenue {vf0:,.1f}".replace(",", " ")), resellar=True); caso(f"formato legítimo «{vf0:,.1f}» con miles separados por espacio y punto decimal", r)
fx.limpiar()
