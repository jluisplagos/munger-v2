"""Batería de la corrección de la verificación de las entradas (4.15; encargo correctivo tras la revisión externa de la 4.14, §2 y §4).

Mismo fixture que test_verificacion_entradas_414.py (copia del expediente cerrado de Viscofan de la 4.13 y registro SINTÉTICO completo,
con su fuente sintética conservada con huella y cada comprobación sellada por el revisor sintético), que es el control positivo; cada
caso negativo cambia una sola cosa. No ejecuta el pipeline ni LibreOffice.

Grupos:
  R1 · página inexistente (el contraejemplo de la revisión externa: Historia!F6 → «999999»), página no inequívoca, fuente no textual sin
       texto con marcas de página; positivos: PDF con «archivo_texto» y su huella, folio impreso distinto de la página del PDF.
  R2 · fuente local ausente (el contraejemplo: «fuentes_sinteticas/NO_EXISTE.txt», sha256 = None), fuente local sin huella, lectura
       externa incompleta, lectura externa completa (material: no apta; no material: apta), revisor que declara haberla examinado.
  R3 · redondeo aceptado como cifra exacta (el contraejemplo: 45479.209 con una cita que solo contiene 45479 y la huella del texto
       actualizada; y _cita_contiene(«Amortización: 150», 149.5), («Partida: 0», 0.49)); positivos con formatos legítimos.
  V  · vigencia del fundamento (I13): fundamento, conciliación o evidencia del libro cambiados con el mismo número → desactualizada;
       sin vínculo o registro 4.14 → pendiente; `sellar` no legitima revisiones antiguas.
  J  · cobertura del juicio (I8): las cifras financieras que usan las fases de juicio entran en el universo con dependencias distintas.
  E  · entrada efectiva (C48 de Elis): una entrada del FCF base que fase1_v63.json no reproduce no se acredita.
  N  · recuentos (I9): el informe dice «N de M» con N ≤ M y separa cálculo y juicio.
  U  · (4.15, hito 2) límites de la cuarta revisión: U2 empates del redondeo de importes (sin tolerancia general), U3 coste acotado de
       round y de las fórmulas, U4 rechazos falsos del control de sensibilidad y un caso que solo detecta el de constantes, U1 derivados
       contados y listados, U5 texto visible y codificación de las fuentes HTML, U7 unidad monetaria no reconocida.
  RV · (4.15, hito 2) hallazgos de la revisión independiente: cita recortada o cortada dentro de un número (H1), «−» como cero y moneda,
       porcentaje, fechas (H4, H5), sensibilidad independiente de la escritura (H6), HTML (H7) y signo −1 sin tratamiento (H14); y, en N,
       los dos bloques de aptitud del informe por separado (H2).
  SG · (4.15, hito 2, R415-SIGNO) signo de la cifra publicada: contraejemplos completos en los dos sentidos, paréntesis contables, menos
       ASCII y Unicode, guiones de cero y signos indeterminados; positivos con la transformación justificada (signo −1).
Uso: python3 -B test_verificacion_entradas_415.py [--json salida.json]
"""
import argparse, copy, datetime, hashlib, json, os, re, shutil, subprocess, sys, tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
PV = os.path.dirname(AQUI)
sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
sys.path.insert(0, os.path.join(PV, "scripts"))
import verificacion_entradas as VE  # noqa: E402
import entradas_economicas as EE  # noqa: E402
from v63_xml import LibroV63  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--json")
ARGS = ap.parse_args()
E413 = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_13")
CFG = os.path.join(PV, "config_v2_v641_experimental.json")
TMP = tempfile.mkdtemp(prefix="verificacion_entradas_415_")
RES = []


def paso(grupo, nombre, ok, detalle=""):
    RES.append({"grupo": grupo, "prueba": nombre, "resultado": "PASA" if ok else "FALLA", "detalle": str(detalle)[:400]})
    print(f"[{grupo}] {'PASA ' if ok else 'FALLA'} {nombre}" + (f" · {str(detalle)[:240]}" if detalle else ""))


IGN = shutil.ignore_patterns(".lo_perfil", "variantes_v64", "recalc", "prompts_generados", "__pycache__")
c = os.path.join(TMP, "viscofan", "Viscofan")
shutil.copytree(os.path.join(E413, "viscofan", "Viscofan"), c, ignore=IGN)

# (4.15) la copia de Viscofan de la 4.13 tiene C47–C50 de la etapa 1 distintos de las medias de su fase1_v63.json (el mismo defecto que C48
# de Elis: entrada efectiva sostenida solo por el valor migrado). El fixture declara en SU COPIA de fase1_v63.json el valor efectivo del
# libro, para que el control positivo sea un expediente reproducible; el caso negativo está en test_verificacion_entradas_415.py.
_f1p = os.path.join(c, "fase1_v63.json")
_f1 = json.load(open(_f1p, encoding="utf-8"))
for _k, (_vl, _vf, _m) in VE.entradas_no_reproducibles(c, VE.universo(c)).items():
    _d = _f1.setdefault("analisis", {}).get(_k.split("!")[1])
    _f1["analisis"][_k.split("!")[1]] = dict(_d, valor=_vl) if isinstance(_d, dict) else {"valor": _vl, "fuente": "(fixture sintético) valor efectivo del libro"}
json.dump(_f1, open(_f1p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
inst = VE.universo(c)
anios = [inst["celdas"].get(f"Historia!{x}5") for x in "CDEFGHIJKL"]
FS = os.path.join(c, "fuentes_sinteticas")
os.makedirs(FS)
paginas = []


def escribir_fuente():
    open(os.path.join(FS, "fuente.txt"), "w", encoding="utf-8").write("".join(f"[PDF PAGE {i + 1}]\n{p}\n" for i, p in enumerate(paginas)))


def fuente_para(k, v):
    n = len(paginas) + 1
    m = re.match(r"^Historia!([C-L])(\d+)$", k)
    periodo = f"ejercicio {int(anios['CDEFGHIJKL'.index(m.group(1))])}" if m else "31-dic-2025"
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        if m and int(m.group(2)) == 5:
            vf, unidad, escala, cita = v, "año", 1.0, f"Ejercicio {int(v)}"
        else:
            vf, unidad, escala = round(v * 1000, 6), "miles de euros", 0.001
            cita = f"Partida sintética de {k}: {vf:.3f}"
    else:
        vf, unidad, escala, cita = v, "texto", 1.0, f"Dato sintético de {k}: {v}"
    paginas.append(cita)
    return {"documento": "Fuente sintética de la prueba (no es un documento de la empresa)", "archivo": "fuentes_sinteticas/fuente.txt", "sha256": "__actual__",
            "version": "sintética 1", "pagina": str(n), "ubicacion": "tabla sintética", "concepto": f"concepto de {k}", "columna": periodo, "periodo": periodo,
            "unidad": unidad, "escala": escala, "signo": 1, "tratamiento": "ninguno", "perimetro": "consolidado", "reexpresado": "no aplica",
            "valor_fuente": vf, "cita": cita}


COMPROBADA = {"extractor": "extractor sintético", "revisor": "revisor sintético", "fecha": "2026-11-15", "resultado": "verificado",
              "fuente_examinada": "fuentes_sinteticas/fuente.txt (página citada)", "nota": None}
ents = []
for k, v in inst["celdas"].items():
    t = inst["tipos"].get(k)
    e = {"celda": k, "id": inst["ids"].get(k), "ambito": inst["ambito"].get(k), "uso": "prueba", "material": True, "valor_modelo": v,
         "comprobacion": dict(COMPROBADA), "incidencia": None}
    if t in ("hipótesis", "configuracion"):
        e.update(clase="hipotesis" if t == "hipótesis" else "convencion", hipotesis={"fundamento": "(prueba)", "alternativas": ["(prueba)"], "limites": ["(prueba)"]})
    elif v is None or v == "":
        e.update(clase="no_aplicable", justificacion="(prueba) celda vacía del libro: no aplica a este expediente")
    elif isinstance(v, (int, float)) and v == 0:
        e.update(clase="cero_comprobado", fuente=fuente_para(k, v))
    else:
        e.update(clase="dato_publicado", fuente=fuente_para(k, v))
    ents.append(e)
escribir_fuente()
EVID = VE.evidencia_libro(c)
REG = {"formato": VE.FORMATO, "empresa": "Viscofan", "nota": "REGISTRO SINTÉTICO DE PRUEBA (no verifica ningún dato real)", "perimetro_del_expediente": "consolidado",
       "huella_entradas_economicas": inst["huella"], "entradas": ents}


def sellar_todo(reg, carpeta=None):
    carpeta = carpeta or c
    evid = VE.evidencia_libro(carpeta)
    sha = hashlib.sha256(open(os.path.join(carpeta, "fuentes_sinteticas", "fuente.txt"), "rb").read()).hexdigest()
    for e in reg["entradas"]:
        f = e.get("fuente") or {}
        if f.get("archivo") == "fuentes_sinteticas/fuente.txt" and f.get("sha256") == "__actual__":
            f["sha256"] = sha
    hs = VE.huellas_registro(carpeta, reg)
    for e in reg["entradas"]:
        cmp_ = e.setdefault("comprobacion", {})
        cmp_["vinculo"] = {"huella": hs[e["celda"]], "sellado_por": cmp_.get("revisor"), "fecha": cmp_.get("fecha")}
    return reg


def pdf_minimo(paginas):
    """PDF mínimo (sin dependencias): una página por texto, Helvetica WinAnsi, una línea por renglón."""
    objs = []
    def esc(t):
        b = t.encode("cp1252", errors="replace")
        return b.replace(b"\\", b"\\\\").replace(b"(", b"\\(").replace(b")", b"\\)")
    n = len(paginas)
    kids = " ".join(f"{4 + 2 * i} 0 R" for i in range(n))
    objs.append(b"<< /Type /Catalog /Pages 2 0 R >>")
    objs.append(f"<< /Type /Pages /Kids [{kids}] /Count {n} >>".encode())
    objs.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>")
    for i, t in enumerate(paginas):
        lineas = str(t).split("\n")
        cont = b"BT /F1 9 Tf 40 800 Td 11 TL " + b" ".join(b"(" + esc(l) + b") Tj T*" for l in lineas) + b" ET"
        objs.append(f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 3 0 R >> >> /Contents {5 + 2 * i} 0 R >>".encode())
        objs.append(b"<< /Length " + str(len(cont)).encode() + b" >>\nstream\n" + cont + b"\nendstream")
    out = b"%PDF-1.4\n"
    offs = []
    for j, o in enumerate(objs, 1):
        offs.append(len(out))
        out += f"{j} 0 obj\n".encode() + o + b"\nendobj\n"
    xref = len(out)
    out += f"xref\n0 {len(objs) + 1}\n0000000000 65535 f \n".encode() + b"".join(f"{x:010d} 00000 n \n".encode() for x in offs)
    out += f"trailer\n<< /Size {len(objs) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode()
    return out


def nueva_pagina(texto):
    """Añade una página a la fuente sintética, registra su huella nueva en el registro base y vuelve a sellar."""
    paginas.append(texto)
    escribir_fuente()
    for e in REG["entradas"]:
        if (e.get("fuente") or {}).get("archivo") == "fuentes_sinteticas/fuente.txt":
            e["fuente"]["sha256"] = "__actual__"
    sellar_todo(REG)
    return str(len(paginas))


sellar_todo(REG)


def con(cambio=None, resellar=False, carpeta=None):
    carpeta = carpeta or c
    reg = copy.deepcopy(REG)
    if cambio:
        cambio(reg)
    if resellar:
        sellar_todo(reg, carpeta)
    json.dump(reg, open(os.path.join(carpeta, VE.REGISTRO), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    return VE.comprobar(carpeta)


def ent(reg, k):
    return next(e for e in reg["entradas"] if e["celda"] == k)


def con_k(r, k, cats=("errores", "discrepancias", "pendientes", "desactualizadas")):
    return [f"{cat}: {x}" for cat in cats for x in r[cat] if x.startswith(k + ":")]


def bloques_aptitud(inf):
    """(4.15, hito 2, H2) Los dos bloques del informe que hablan de la aptitud, por separado: el párrafo de aptitud de la V6.4 (desde
    «Verificación de las entradas financieras:») y la línea de las entradas financieras de todas las plantillas (I20)."""
    import re as _re
    v64 = _re.search(r"\*\*Verificación de las entradas financieras:\*\*[^\n]*", inf)
    i20 = _re.search(r"\*\*Entradas financieras:\*\*[^\n]*", inf)
    return (v64.group(0) if v64 else None), (i20.group(0) if i20 else None)


def aptitud_en_informe(inf, apta_entradas):
    """Cada bloque presente dice «apta por entradas: sí|no» según el registro y «Apta para dinero real: no»; ninguna parte del informe
    dice «Apta para dinero real: sí»; hay una frase «Apta para dinero real: no» por bloque."""
    b = [x for x in bloques_aptitud(inf) if x is not None]
    esp = "apta por entradas: " + ("sí" if apta_entradas else "no")
    return (bool(b) and all(esp in x and "Apta para dinero real: no" in x for x in b) and "Apta para dinero real: sí" not in inf
            and "apta por entradas: " + ("no" if apta_entradas else "sí") not in " ".join(b) and inf.count("Apta para dinero real: no") == len(b))


K = "Historia!F6"  # la entrada del contraejemplo de la revisión externa
assert ent(REG, K)["clase"] == "dato_publicado"
r = con()
paso("P", f"control positivo: {r['comprobadas_universo']} de {r['universo']} celdas comprobadas ({r['comprobadas_calculo']} de {r['universo_calculo']} de cálculo, "
          f"{r['comprobadas_juicio']} de {r['universo_juicio']} de juicio), apta por entradas", r["apto_por_entradas"] and r["comprobadas_universo"] == r["universo"], (r["errores"] + r["discrepancias"] + r["pendientes"])[:3])

# ------------------------------------------------------------------ R1 · página
r = con(lambda g: ent(g, K)["fuente"].update(pagina="999999"))
paso("R1", "página inexistente «999999» (contraejemplo de la revisión externa): discrepancia, no apta (antes: apta, sin errores ni discrepancias)",
     not r["apto_por_entradas"] and any("no existe" in x for x in con_k(r, K, ("discrepancias",))), con_k(r, K))
r = con(lambda g: ent(g, K)["fuente"].update(pagina=999999))
paso("R1", "página inexistente como entero: discrepancia", not r["apto_por_entradas"] and con_k(r, K, ("discrepancias",)), con_k(r, K))
r = con(lambda g: ent(g, K)["fuente"].update(pagina="22-23"))
paso("R1", "página no inequívoca («22-23»): pendiente (no puede examinarse), no apta", not r["apto_por_entradas"] and con_k(r, K, ("pendientes",)), con_k(r, K))
r = con(lambda g: ent(g, K)["fuente"].update(pagina="folio 76"))
paso("R1", "un folio impreso en lugar de la página del PDF («folio 76»): pendiente", not r["apto_por_entradas"] and con_k(r, K, ("pendientes",)), con_k(r, K))
pag_k = ent(REG, K)["fuente"]["pagina"]
r = con(lambda g: ent(g, K)["fuente"].update(pagina=f"PDF {pag_k}", folio="76"), resellar=True)
paso("R1", "página del PDF «PDF n» con un folio impreso distinto declarado aparte: aceptada", r["apto_por_entradas"], con_k(r, K))
# (4.15, segunda revisión, hallazgo 12) el «PDF» conservado es un PDF de verdad con las mismas páginas que su texto extraído
open(os.path.join(FS, "fuente_original.pdf"), "wb").write(pdf_minimo(paginas))
sha_pdf = hashlib.sha256(open(os.path.join(FS, "fuente_original.pdf"), "rb").read()).hexdigest()
sha_txt = hashlib.sha256(open(os.path.join(FS, "fuente.txt"), "rb").read()).hexdigest()
r = con(lambda g: ent(g, K)["fuente"].update(archivo="fuentes_sinteticas/fuente_original.pdf", sha256=sha_pdf), resellar=True)
paso("R1", "fuente conservada no textual (PDF) sin «archivo_texto»: la página no puede examinarse → pendiente", not r["apto_por_entradas"] and any("archivo_texto" in x for x in con_k(r, K, ("pendientes",))), con_k(r, K))
r = con(lambda g: ent(g, K)["fuente"].update(archivo="fuentes_sinteticas/fuente_original.pdf", sha256=sha_pdf, archivo_texto="fuentes_sinteticas/fuente.txt", sha256_texto=sha_txt), resellar=True)
paso("R1", "PDF con «archivo_texto» y «sha256_texto» vigentes: contraste de página hecho, aceptada", r["apto_por_entradas"], con_k(r, K))
shutil.copy(os.path.join(FS, "fuente.txt"), os.path.join(FS, "ajeno.pdf"))  # bytes ajenos con extensión .pdf
sha_aj = hashlib.sha256(open(os.path.join(FS, "ajeno.pdf"), "rb").read()).hexdigest()
r = con(lambda g: ent(g, K)["fuente"].update(archivo="fuentes_sinteticas/ajeno.pdf", sha256=sha_aj, archivo_texto="fuentes_sinteticas/fuente.txt", sha256_texto=sha_txt), resellar=True)
paso("R1", "(segunda revisión, h12) un «PDF» de bytes ajenos con «archivo_texto» y su huella: discrepancia, no apta (antes: comprobada)",
     not r["apto_por_entradas"] and any("no es un PDF" in x for x in con_k(r, K, ("discrepancias",))), con_k(r, K))
open(os.path.join(FS, "otro.pdf"), "wb").write(pdf_minimo([f"Otro documento, página {i + 1}" for i in range(len(paginas))]))
sha_ot = hashlib.sha256(open(os.path.join(FS, "otro.pdf"), "rb").read()).hexdigest()
r = con(lambda g: ent(g, K)["fuente"].update(archivo="fuentes_sinteticas/otro.pdf", sha256=sha_ot, archivo_texto="fuentes_sinteticas/fuente.txt", sha256_texto=sha_txt), resellar=True)
paso("R1", "(segunda revisión, h12) un PDF verdadero cuyo texto no es el conservado: discrepancia (la cita tiene que estar en esa página del PDF)",
     not r["apto_por_entradas"] and any("no es el de ese documento" in x for x in con_k(r, K, ("discrepancias",))), con_k(r, K))
assert not VE._contiene_texto("Divisa: NEURROS", "EUR") and VE._contiene_texto("Divisa: EUR (millones)", "eur")
paso("R1", "(segunda revisión, h12) un valor de texto se busca como palabra completa: «EUR» no está en «NEURROS»", True)
r = con(lambda g: ent(g, K)["fuente"].update(archivo="fuentes_sinteticas/fuente_original.pdf", sha256=sha_pdf, archivo_texto="fuentes_sinteticas/fuente.txt"), resellar=True)
paso("R1", "PDF con «archivo_texto» sin su huella: pendiente", not r["apto_por_entradas"] and con_k(r, K, ("pendientes",)), con_k(r, K))
r = con(lambda g: ent(g, K)["fuente"].update(archivo="fuentes_sinteticas/fuente_original.pdf", sha256=sha_pdf, archivo_texto="fuentes_sinteticas/fuente.txt", sha256_texto=sha_txt, pagina="999999"), resellar=True)
paso("R1", "PDF con texto examinable y página inexistente: discrepancia", not r["apto_por_entradas"] and con_k(r, K, ("discrepancias",)), con_k(r, K))
k_txt = next(e["celda"] for e in REG["entradas"] if e["clase"] == "dato_publicado" and not isinstance(e["valor_modelo"], (int, float)))
r = con(lambda g: ent(g, k_txt)["fuente"].update(pagina="999999"))
paso("R1", f"dato publicado de TEXTO ({k_txt}) con página inexistente: discrepancia (la vía de texto tampoco omite el contraste)",
     not r["apto_por_entradas"] and con_k(r, k_txt, ("discrepancias",)), con_k(r, k_txt))
assert VE._numero_pagina(12) == 12 and VE._numero_pagina("12") == 12 and VE._numero_pagina("PDF 12") == 12 and VE._numero_pagina("pdf p. 12") == 12
assert VE._numero_pagina("12-13") is None and VE._numero_pagina("") is None and VE._numero_pagina(0) is None and VE._numero_pagina("folio 76") is None and VE._numero_pagina(True) is None
paso("R1", "lectura de la página: entero, «12», «PDF 12» y «pdf p. 12» valen; «12-13», vacío, 0, «folio 76» y booleanos no", True)

# ------------------------------------------------------------------ R2 · conservación
r = con(lambda g: ent(g, K)["fuente"].update(archivo="fuentes_sinteticas/NO_EXISTE.txt", sha256=None))
paso("R2", "fuente local ausente con sha256 = None (contraejemplo de la revisión externa): pendiente, no apta (antes: apta)",
     not r["apto_por_entradas"] and any("no está" in x for x in con_k(r, K, ("pendientes",))), con_k(r, K))
r = con(lambda g: ent(g, K)["fuente"].update(archivo="fuentes_sinteticas/NO_EXISTE.txt"))
paso("R2", "fuente local ausente con la huella registrada: pendiente", not r["apto_por_entradas"] and con_k(r, K, ("pendientes",)), con_k(r, K))
r = con(lambda g: (ent(g, K)["fuente"].update(archivo="fuentes_sinteticas/NO_EXISTE.txt", sha256=None),
                   ent(g, K)["comprobacion"].update(fuente_examinada="fuentes_sinteticas/NO_EXISTE.txt, página 22: cifra vista por el revisor", nota="examinada")))
paso("R2", "la declaración del revisor de haber examinado la fuente no sustituye su existencia: pendiente", not r["apto_por_entradas"] and con_k(r, K, ("pendientes",)), con_k(r, K))
r = con(lambda g: ent(g, K)["fuente"].update(sha256=None), resellar=True)
paso("R2", "fuente local que existe pero sin sha256: pendiente (no se puede comprobar que es la examinada)", not r["apto_por_entradas"] and any("sha256" in x for x in con_k(r, K, ("pendientes",))), con_k(r, K))
r = con(lambda g: ent(g, K)["fuente"].update(conservacion="ninguna"))
paso("R2", "conservación no declarada como local ni externa: pendiente", not r["apto_por_entradas"] and con_k(r, K, ("pendientes",)), con_k(r, K))
LE = {"referencia": "https://ejemplo.invalid/serie (página leída en pantalla)", "fecha": "2026-11-15 10:00 CET",
      "evidencia": "transcripción de la fila leída; captura no conservada", "limitaciones": "sin bytes conservados: no es reproducible; la página puede cambiar"}


def externa(g, k=K, le=LE, material=True):
    f = ent(g, k)["fuente"]
    for x in ("archivo", "sha256"):
        f.pop(x, None)
    f.update(conservacion="externa", lectura_externa=dict(le))
    ent(g, k)["material"] = material


r = con(lambda g: externa(g, le={**LE, "limitaciones": ""}), resellar=True)
paso("R2", "lectura externa sin limitaciones explícitas: pendiente", not r["apto_por_entradas"] and con_k(r, K, ("pendientes",)), con_k(r, K))
r = con(lambda g: externa(g, le={**LE, "fecha": None}), resellar=True)
paso("R2", "lectura externa sin fecha: pendiente", not r["apto_por_entradas"] and con_k(r, K, ("pendientes",)), con_k(r, K))
r = con(lambda g: externa(g), resellar=True)
paso("R2", "lectura externa completa de una entrada MATERIAL: listada aparte, no cuenta como comprobada y la entrada no es apta",
     not r["apto_por_entradas"] and K not in r["comprobadas"] and any(x.startswith(K) for x in r["lecturas_externas"]) and K in r["materiales_no_comprobadas"],
     (r["lecturas_externas"][:1], r["motivo"]))
KJ = next(e["celda"] for e in REG["entradas"] if e["ambito"] == "juicio" and e["clase"] == "dato_publicado" and isinstance(e["valor_modelo"], (int, float)))


def externa_juicio(g):
    externa(g, k=KJ, material=False)
    ent(g, KJ)["justificacion_materialidad"] = "(prueba) cifra de contexto que el juicio no usa para concluir"


r = con(externa_juicio, resellar=True)
paso("R2", "lectura externa completa de una entrada de juicio NO material (con su justificación): apta, pero sigue listada como lectura externa y como no material (no se equipara en silencio)",
     r["apto_por_entradas"] and KJ not in r["comprobadas"] and any(x.startswith(KJ) for x in r["lecturas_externas"]) and KJ in r["no_materiales"], r["motivo"])

# ------------------------------------------------------------------ R3 · redondeo
assert not VE._cita_contiene("Amortización: 150", 149.5) and not VE._cita_contiene("Partida: 0", 0.49) and not VE._cita_contiene("Acciones: 45479", 45479.209)
assert not VE._cita_contiene("Acciones: 45.479", 45479.209) and not VE._cita_contiene("1,23", 1.234) and not VE._cita_contiene("Precio 54,70", 54.7001)
paso("R3", "_cita_contiene: «150» no es 149,5; «0» no es 0,49; «45479» y «45.479» no son 45.479,209; «1,23» no es 1,234 (antes: True)", True)
assert VE._cita_contiene("Amortización: 149,5", 149.5) and VE._cita_contiene("Amortización: 149.5", 149.5) and VE._cita_contiene("Acciones: 45.479,209", 45479.209)
assert VE._cita_contiene("Shares 45,479.209", 45479.209) and VE._cita_contiene("Acciones 45479,2090", 45479.209) and VE._cita_contiene("Total 1.234,50", 1234.5)
assert VE._cita_contiene("VISCOFAN 54,7000", 54.7) and VE._cita_contiene("Total 4 573,7", 4573.7) and VE._cita_contiene("Saldo 0", 0) and VE._cita_contiene("Saldo 0,0", 0)
# (4.15, hito 2, R415-SIGNO) la versión del hito 1 daba por buena «(149,5)» para 149,5 (la revisión externa lo señala): un pago entre paréntesis
# es la cifra publicada −149,5; su magnitud positiva se obtiene con la transformación declarada (signo −1), no se confunde con la cifra
assert VE._cita_contiene("Revenue 912.160 849.697", 849697) and VE._cita_contiene("Acquisitions  -   (12.3)", 0) and VE._cita_contiene("(149,5)", -149.5)
assert not VE._cita_contiene("(149,5)", 149.5)
paso("R3", "formatos legítimos aceptados: separadores de miles y decimales, ceros finales, miles con espacio, paréntesis (con su signo: «(149,5)» es −149,5), cero impreso «-»", True)
pr3 = nueva_pagina("Número de acciones (miles): 45479")
AUX = {"celda": "aux:acciones_miles", "id": "aux:acciones_miles", "ambito": "auxiliar", "uso": "origen sintético", "material": True, "clase": "dato_publicado",
       "valor_modelo": 45.479209, "comprobacion": dict(COMPROBADA), "incidencia": None,
       "fuente": {"documento": "Fuente sintética de la prueba", "archivo": "fuentes_sinteticas/fuente.txt", "sha256": "__actual__", "version": "sintética 1", "pagina": pr3,
                  "ubicacion": "tabla sintética", "concepto": "acciones emitidas", "columna": "31-dic-2025", "periodo": "31-dic-2025", "unidad": "miles de acciones",
                  "escala": 0.001, "signo": 1, "tratamiento": "miles de acciones → millones", "perimetro": "consolidado", "reexpresado": "no aplica",
                  "valor_fuente": 45479.209, "cita": "Número de acciones (miles): 45479"}}
r = con(lambda g: g["entradas"].append(copy.deepcopy(AUX)), resellar=True)
paso("R3", "valor de la fuente 45479.209 con una cita real que solo contiene 45479 y la huella del texto actualizada (contraejemplo; restantes entradas iguales): discrepancia, no apta",
     not r["apto_por_entradas"] and any("cifra completa" in x for x in con_k(r, "aux:acciones_miles", ("discrepancias",))), con_k(r, "aux:acciones_miles"))
pr3a = nueva_pagina("Número de acciones (miles): 45.479,209")
r = con(lambda g: g["entradas"].append(dict(copy.deepcopy(AUX), fuente=dict(AUX["fuente"], pagina=pr3a, cita="Número de acciones (miles): 45.479,209"))), resellar=True)
paso("R3", "la misma entrada con la cifra publicada completa («45.479,209»): aceptada", r["apto_por_entradas"], con_k(r, "aux:acciones_miles"))
pr3d = nueva_pagina("Número de acciones (miles): 45479")


def menor_precision(g):
    g["entradas"].append(dict(copy.deepcopy(AUX), clase="derivado", fuente={}, valor_modelo=45.479,
                              derivacion={"origenes": ["aux:acciones_publicadas"], "formula": 'o["aux:acciones_publicadas"] / 1000',
                                          "conciliacion": "la fuente publica 45.479 miles (sin decimales); el modelo usa 45,479 millones, sin inventar precisión"}))
    g["entradas"].append(dict(copy.deepcopy(AUX), celda="aux:acciones_publicadas", id="aux:acciones_publicadas", valor_modelo=45479,
                              fuente=dict(AUX["fuente"], pagina=pr3d, unidad="acciones (miles, tal como se publican)", escala=1, valor_fuente=45479,
                                          tratamiento="valor publicado, sin redondear ni completar")))


r = con(menor_precision, resellar=True)
paso("R3", "menor precisión publicada: se registra el valor publicado (45479) y la transformación explícita (derivado): aceptada", r["apto_por_entradas"], con_k(r, "aux:acciones_miles") + con_k(r, "aux:acciones_publicadas"))
vf0 = ent(REG, K)["fuente"]["valor_fuente"]
pr3b = nueva_pagina(f"Partida sintética de {K}: {vf0:,.4f}".replace(",", "X").replace(".", ",").replace("X", "."))
r = con(lambda g: ent(g, K)["fuente"].update(pagina=pr3b, cita=f"Partida sintética de {K}: {vf0:,.4f}".replace(",", "X").replace(".", ",").replace("X", ".")), resellar=True)
paso("R3", "el mismo número con separador de miles «.», coma decimal y cuatro decimales (cero final): aceptado", r["apto_por_entradas"], con_k(r, K))
pr3c = nueva_pagina(f"Partida sintética de {K}: {round(vf0):,}".replace(",", "."))
r = con(lambda g: ent(g, K)["fuente"].update(pagina=pr3c, cita=f"Partida sintética de {K}: {round(vf0):,}".replace(",", "."), valor_fuente=vf0 + 0.4), resellar=True)
paso("R3", "un valor con decimales frente a la cifra entera publicada (0,4 de diferencia): discrepancia", not r["apto_por_entradas"] and con_k(r, K, ("discrepancias",)), con_k(r, K))

# ------------------------------------------------------------------ V · vigencia del fundamento (I13)
k_hip = next(e["celda"] for e in REG["entradas"] if e["clase"] == "hipotesis")
k_der = next(e["celda"] for e in REG["entradas"] if e["clase"] == "dato_publicado" and e["celda"].startswith("Historia!") and isinstance(e["valor_modelo"], (int, float)) and e["valor_modelo"] > 0 and e["celda"] != K)
r = con(lambda g: ent(g, k_hip)["hipotesis"].update(fundamento="(prueba) fundamento del expediente anterior: cita 259,08"))
paso("V", "hipótesis con su fundamento cambiado y el mismo valor, sin nueva revisión: desactualizada (antes: comprobada)", not r["apto_por_entradas"] and con_k(r, k_hip, ("desactualizadas",)), con_k(r, k_hip))
r = con(lambda g: ent(g, K)["fuente"].update(tratamiento="(prueba) cifra reexpresada con otra transformación"))
paso("V", "dato con la transformación declarada cambiada y el mismo número: desactualizada", not r["apto_por_entradas"] and con_k(r, K, ("desactualizadas",)), con_k(r, K))
r = con(lambda g: ent(g, K)["fuente"].update(documento="(prueba) otro documento"))
paso("V", "dato con la evidencia (documento) cambiada y el mismo número: desactualizada", not r["apto_por_entradas"] and con_k(r, K, ("desactualizadas",)), con_k(r, K))
r = con(lambda g: ent(g, k_hip)["hipotesis"].update(fundamento="(prueba) fundamento nuevo"), resellar=True)
paso("V", "el mismo cambio con una revisión nueva sellada: comprobada", r["apto_por_entradas"], con_k(r, k_hip))
r = con(lambda g: ent(g, K)["comprobacion"].pop("vinculo"))
paso("V", "comprobación sin vínculo: pendiente (hay que revisarla de nuevo)", not r["apto_por_entradas"] and any("vinculada" in x for x in con_k(r, K, ("pendientes",))), con_k(r, K))
r = con(lambda g: (g.update(formato="4.14"), [e["comprobacion"].pop("vinculo", None) for e in g["entradas"]]))
paso("V", "registro de formato 4.14 (sin vínculos): todas las comprobaciones pendientes, no apto", not r["apto_por_entradas"] and r["comprobadas_universo"] == 0, r["motivo"])
r = con(lambda g: g.update(formato="4.9"))
paso("V", "registro de un formato no admitido: no se lee (no verificado)", not r["apto_por_entradas"] and "formato" in str(r["motivo"]), r["motivo"])
# evidencia del libro (Control maestro) cambiada en una copia, con el mismo número
cev = os.path.join(TMP, "viscofan_evid", "Viscofan")
shutil.copytree(c, cev)
k_ev = next(k for k, v in EVID.items() if k in inst["celdas"] and ent(REG, k)["clase"] == "hipotesis" and v.get("N"))
lb = LibroV63(VE.libro_de(cev))
lb.escribir_celdas({f"Control maestro!N{EVID[k_ev]['fila']}": "(prueba) texto de evidencia del expediente anterior"})
lb.guardar(VE.libro_de(cev))
r = con(carpeta=cev)
paso("V", f"evidencia del libro (Control maestro!N{EVID[k_ev]['fila']}, de {k_ev}) cambiada con el mismo valor: desactualizada; el universo de cálculo no cambia",
     not r["apto_por_entradas"] and con_k(r, k_ev, ("desactualizadas",)) and VE.universo(cev)["huella"] == inst["huella"], con_k(r, k_ev))
# sellar: solo el revisor, entrada por entrada, con su revisión de HOY y solo entradas que pasan los controles (revisión independiente, hallazgo 3)
HOY = datetime.datetime.now().astimezone().date().isoformat()
cs = os.path.join(TMP, "viscofan_sellar", "Viscofan")
shutil.copytree(c, cs)
reg_s = copy.deepcopy(REG)
for e in reg_s["entradas"]:
    e["comprobacion"].pop("vinculo", None)
    e["comprobacion"]["fecha"] = HOY
ent(reg_s, k_der)["comprobacion"].update(revisor="extractor sintético")
ent(reg_s, k_hip)["comprobacion"].update(resultado="pendiente")
k_mal = next(e["celda"] for e in reg_s["entradas"] if e["clase"] == "dato_publicado" and e["celda"] not in (K, k_der))
ent(reg_s, k_mal)["fuente"]["pagina"] = "999999"
ent(reg_s, KJ)["comprobacion"]["fecha"] = "2026-11-14"
json.dump(reg_s, open(os.path.join(cs, VE.REGISTRO), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)


def sale(f):
    try:
        return f(), None
    except SystemExit as ex:
        return None, str(ex)


_, e_vacio = sale(lambda: VE.sellar(cs, [], "revisor sintético", HOY))
_, e_fecha = sale(lambda: VE.sellar(cs, [K], "revisor sintético", "2026-11-14"))
sha_antes = hashlib.sha256(open(os.path.join(cs, VE.REGISTRO), "rb").read()).hexdigest()
ok_o, mal_o = VE.sellar(cs, [K], "otro revisor", HOY)
sin_cambio = hashlib.sha256(open(os.path.join(cs, VE.REGISTRO), "rb").read()).hexdigest() == sha_antes
ok_s, mal_s = VE.sellar(cs, [K, k_der, k_hip, k_mal, KJ], "revisor sintético", HOY)
r = VE.comprobar(cs)
paso("V", "sellar: exige la lista de celdas y la fecha de hoy (una fecha anterior no se sella: SystemExit); un sello rechazado no reescribe el registro",
     bool(e_vacio) and bool(e_fecha) and "hoy" in e_fecha and not ok_o and sin_cambio, (e_vacio, e_fecha, mal_o))
paso("V", "sellar: sella solo la comprobada hoy por ese revisor y que pasa los controles; rechaza revisor = extractor, resultado pendiente, página inexistente y comprobación de otro día",
     ok_s == [K] and len(mal_s) == 4 and any(k_mal in x and "controles" in x for x in mal_s) and K in r["comprobadas"] and not r["apto_por_entradas"], (ok_s, [x[:80] for x in mal_s]))
reg_s2 = json.load(open(os.path.join(cs, VE.REGISTRO), encoding="utf-8"))
v_k = ent(reg_s2, K)["comprobacion"]["vinculo"]
ent(reg_s2, K)["comprobacion"]["revisor"] = "otro revisor (cambiado después del sello)"
json.dump(reg_s2, open(os.path.join(cs, VE.REGISTRO), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
r = VE.comprobar(cs)
paso("V", "el vínculo registra sellado_en y cubre la propia comprobación: cambiar el revisor después del sello la deja desactualizada",
     bool(v_k.get("sellado_en")) and v_k.get("sellado_por") == "revisor sintético" and any(x.startswith(K + ":") for x in r["desactualizadas"]), r["desactualizadas"][:1])

# ------------------------------------------------------------------ J · cobertura del juicio (I8)
import volcar_datos_v63 as VD  # noqa: E402
import leer_v63 as L  # noqa: E402
fuera = {r for r in VD.DATOS_ANALISIS if f"Análisis!{r}" not in inst["celdas"]}
paso("J", "(hallazgo 6) de lo que datos_v63.md da a las fases solo quedan fuera la identificación y la fórmula del FCF base ({B3, D3, B4, D4, C52}); filas de la Historia sin el año; geografía, sector y fechas de Palancas dentro",
     fuera == {"B3", "D3", "B4", "D4", "C52"} and set(VE.FILAS_HISTORIA_JUICIO) == set(L.FILAS_HISTORIA) - {5}
     and all(inst["ambito"].get(f"Palancas!{x}") == "juicio" for x in ("C7", "C45", "C46", "A28", "B28")), sorted(fuera))
ee = EE.instantanea(VE.libro_de(c))
paso("J", f"universo = cálculo ({inst['n_calculo']}, la instantánea de entradas_economicas, misma huella) + juicio ({inst['n_juicio']}); C42 (EV/EBITDA) está en el juicio",
     inst["n_calculo"] == ee["n"] and inst["huella"] == ee["huella"] and inst["ambito"].get("Análisis!C42") == "juicio" and inst["n"] == inst["n_calculo"] + inst["n_juicio"])
r = con(lambda g: g["entradas"].remove(ent(g, "Análisis!C42")))
paso("J", "sin la entrada de C42 (cifra usada por el juicio): no apta, con C42 sin entrada", not r["apto_por_entradas"] and "Análisis!C42" in r["sin_entrada"], r["motivo"])
r = con(lambda g: ent(g, "Análisis!C42").update(valor_modelo=(ent(g, "Análisis!C42")["valor_modelo"] or 0) + 1))
paso("J", "C42 registrado con otro valor (p. ej. con la capitalización anterior): desactualizada, no apta", not r["apto_por_entradas"] and con_k(r, "Análisis!C42", ("desactualizadas",)), con_k(r, "Análisis!C42"))
k_hj = next(k for k, a in inst["ambito"].items() if a == "juicio" and k.startswith("Historia!") and ent(REG, k)["clase"] == "dato_publicado")
r = con(lambda g: ent(g, k_hj)["comprobacion"].update(resultado="pendiente"))
paso("J", f"fila de la Historia usada solo por el juicio ({k_hj}) pendiente: no apta (no queda fuera por ser «descriptiva»)", not r["apto_por_entradas"] and k_hj in r["materiales_no_comprobadas"], con_k(r, k_hj))

# ------------------------------------------------------------------ RI · contraejemplos de la revisión independiente del hito 1 (Fable)
r = con(lambda g: (ent(g, K)["fuente"].update(archivo="fuentes_sinteticas/NO_EXISTE.txt", sha256=None), ent(g, K).update(material=False)))
paso("RI", "(h1) el contraejemplo R2 con «material: false» en una entrada de CÁLCULO: error, no apta (antes: apta sin revisor)", not r["apto_por_entradas"] and any(x.startswith(K + ":") and "material" in x for x in r["errores"]), con_k(r, K))
r = con(lambda g: ent(g, KJ).update(material=False), resellar=True)
paso("RI", "(h1) «material: false» en una entrada de juicio sin «justificacion_materialidad»: error", not r["apto_por_entradas"] and any(x.startswith(KJ + ":") for x in r["errores"]), con_k(r, KJ))
r = con(lambda g: (ent(g, K).update(clase="convencion", fuente={}, hipotesis={"fundamento": "(prueba)", "alternativas": ["x"], "limites": ["x"]})), resellar=True)
paso("RI", "(h2) un dato del cálculo reetiquetado como convención sin «justificacion_clase»: error (antes: comprobado sin fuente)", not r["apto_por_entradas"] and any(x.startswith(K + ":") and "justificacion_clase" in x for x in r["errores"]), con_k(r, K))
r = con(lambda g: (ent(g, K).update(clase="convencion", fuente={}, justificacion_clase="(prueba) la cifra es una convención del modelo",
                                    hipotesis={"fundamento": "(prueba)", "alternativas": ["x"], "limites": ["x"]}), ent(g, K)["comprobacion"].update(revisor=None)), resellar=True)
paso("RI", "(h2) con justificación pero sin revisor independiente: no se acredita", not r["apto_por_entradas"] and K not in r["comprobadas"], con_k(r, K))
r = con(lambda g: ent(g, K).update(clase="convencion", fuente={}, justificacion_clase="(prueba) la cifra es una convención del modelo",
                                   hipotesis={"fundamento": "(prueba)", "alternativas": ["x"], "limites": ["x"]}), resellar=True)
paso("RI", "(h2) con justificación y revisión completa: se acredita, pero se lista aparte como dato tratado como convención", K in r["comprobadas"] and K in r["datos_como_hipotesis"], r["datos_como_hipotesis"][:2])
r = con(lambda g: ent(g, K).update(clase="no_aplicable", fuente={}, justificacion="(prueba)"), resellar=True)
paso("RI", "(h2) «no aplicable» con un valor distinto de cero en el libro: error", not r["apto_por_entradas"] and any(x.startswith(K + ":") and "no aplicable" in x for x in r["errores"]), con_k(r, K))
k_tasa = next((e["celda"] for e in REG["entradas"] if e["clase"] == "dato_publicado" and isinstance(e["valor_modelo"], float) and 0 < abs(e["valor_modelo"]) < 1), None)
if k_tasa:
    vt = inst["celdas"][k_tasa]
    pt = nueva_pagina(f"Tasa sintética: {(vt - 0.001) * 100:.6f} %")
    r = con(lambda g: ent(g, k_tasa)["fuente"].update(pagina=pt, cita=f"Tasa sintética: {(vt - 0.001) * 100:.6f} %", valor_fuente=round((vt - 0.001) * 100, 6), unidad="porcentaje", escala=0.01), resellar=True)
    paso("RI", f"(h5) una tasa ({k_tasa} = {vt}) contrastada con una fuente que publica 0,1 puntos menos: discrepancia (antes: comprobada por la tolerancia de importes)",
         not r["apto_por_entradas"] and any(x.startswith(k_tasa + ":") for x in r["discrepancias"]), con_k(r, k_tasa))
    r = con(lambda g: ent(g, k_tasa).update(valor_modelo=vt + 0.001))
    paso("RI", "(h5) vigencia exacta: el registro con el valor + 0,001 queda desactualizado", any(x.startswith(k_tasa + ":") for x in r["desactualizadas"]), con_k(r, k_tasa))
r = con(lambda g: ent(g, K)["fuente"].update(unidad="euros"), resellar=True)
paso("RI", "(h5) la misma cifra en miles declarada en «euros» con escala 0,001: error de escala", any(x.startswith(K + ":") and "escala" in x for x in r["errores"]), con_k(r, K))
paso("RI", "(h10) «10.000.000» no es 10.000.000,01 ni «1.234.567.890» es 1.234.567.890,45; «149,5000000», «849 697.0» y «45'479.209» sí son 149,5, 849.697 y 45.479,209",
     not VE._cita_contiene("Ingresos: 10.000.000", 10000000.01) and not VE._cita_contiene("Ingresos: 1.234.567.890", 1234567890.45)
     and VE._cita_contiene("x 149,5000000", 149.5) and VE._cita_contiene("x 849 697.0", 849697) and VE._cita_contiene("x 45'479.209", 45479.209))
r = con(lambda g: ent(g, K)["fuente"].update(archivo=os.path.join(FS, "fuente.txt")), resellar=True)
paso("RI", "(h11) una fuente «local» con ruta absoluta (fuera de lo conservado con el expediente): pendiente", not r["apto_por_entradas"] and con_k(r, K, ("pendientes",)), con_k(r, K))
r = con(lambda g: ent(g, k_txt)["fuente"].update(cita=" "), resellar=True)
paso("RI", "(h12) un dato de texto con la cita vacía: pendiente", not r["apto_por_entradas"] and con_k(r, k_txt), con_k(r, k_txt))
pt2 = nueva_pagina("Texto sintético sin el valor")
r = con(lambda g: ent(g, k_txt)["fuente"].update(pagina=pt2, cita="Texto sintético sin el valor"), resellar=True)
paso("RI", "(h12) un dato de texto con una cita que no contiene el valor: discrepancia", not r["apto_por_entradas"] and con_k(r, k_txt, ("discrepancias",)), con_k(r, k_txt))
r = con(lambda g: ent(g, K)["fuente"].update(sha256=ent(g, K)["fuente"]["sha256"].upper()), resellar=True)
paso("RI", "(h18) un sha256 en mayúsculas es la misma huella", r["apto_por_entradas"], con_k(r, K))
e0 = copy.deepcopy(ent(REG, K)); e0["fuente"]["valor_fuente"] = 849697; e0["valor_modelo"] = 849.697
e1 = copy.deepcopy(e0); e1["fuente"]["valor_fuente"] = 849697.0  # (tercera revisión, T7) entero frente a float de verdad
e2 = copy.deepcopy(e1); e2["fuente"]["cita"] = e2["fuente"]["cita"] + " "; e2["fuente"]["concepto"] = "  " + e2["fuente"]["concepto"]
e3 = copy.deepcopy(e1); e3["fuente"]["cita"] = e3["fuente"]["cita"] + " (otra)"
paso("RI", "(h17; segunda revisión) la huella no distingue 849697 de 849697.0 ni espacios de más, y sí un texto distinto",
     VE.huella_fundamento(e0) == VE.huella_fundamento(e1) == VE.huella_fundamento(e2) and VE.huella_fundamento(e3) != VE.huella_fundamento(e0))


vd = inst["celdas"][k_der]
va = round(vd / 2, 3)
vb = round(vd - va, 3)
pa_ = nueva_pagina(f"Partida sintética de aux:p1: {round(va * 1000):d}")
pb_ = nueva_pagina(f"Partida sintética de aux:p2: {round(vb * 1000):d}")


def montar_derivado(g):
    base_f = dict(ent(g, K)["fuente"])
    for nom, v, pg in (("aux:p1", va, pa_), ("aux:p2", vb, pb_)):
        g["entradas"].append({"celda": nom, "id": nom, "ambito": "auxiliar", "uso": f"origen de {k_der}", "material": True, "clase": "dato_publicado", "valor_modelo": v,
                              "fuente": dict(base_f, pagina=pg, valor_fuente=round(v * 1000), cita=f"Partida sintética de {nom}: {round(v * 1000):d}",
                                             periodo=ent(g, k_der)["fuente"]["periodo"], columna=ent(g, k_der)["fuente"]["columna"]),
                              "comprobacion": dict(COMPROBADA), "incidencia": None})
    ent(g, k_der).update(clase="derivado", fuente={}, derivacion={"origenes": ["aux:p1", "aux:p2"], "formula": 'o["aux:p1"] + o["aux:p2"]', "conciliacion": "(prueba) suma"})


def origen_cambia(g):
    montar_derivado(g)
    sellar_todo(g)  # todo revisado y sellado
    ent(g, "aux:p1")["fuente"].update(documento="(prueba) otro documento", concepto="(prueba) otro concepto")
    ent(g, "aux:p1")["comprobacion"]["vinculo"]["huella"] = VE.huellas_registro(c, g)["aux:p1"]  # se revisa y se sella SOLO el origen


r0 = con(montar_derivado, resellar=True)
r = con(origen_cambia)
paso("RI", "(h9) el origen de un derivado cambia de evidencia y se vuelve a sellar SOLO el origen: el derivado queda desactualizado (su huella incluye la de sus orígenes)",
     k_der in r0["comprobadas"] and r0["apto_por_entradas"] and "aux:p1" in r["comprobadas"] and any(x.startswith(k_der + ":") for x in r["desactualizadas"]), (con_k(r0, k_der), con_k(r, k_der)))
r = con(lambda g: ent(g, k_der).update(clase="derivado", fuente={}, derivacion={"origenes": [k_der], "formula": f'o["{k_der}"]', "conciliacion": "(prueba) circular"}), resellar=True)
paso("RI", "(o21) una derivación circular es un error del contrato, no una excepción", not r["apto_por_entradas"] and any(x.startswith(k_der + ":") for x in r["errores"]), con_k(r, k_der))
r = con(lambda g: ent(g, K).update(clase=["dato_publicado"]))
paso("RI", "(o21) una clase que no es un texto es un error del contrato, no una excepción", not r["apto_por_entradas"] and any(x.startswith(K + ":") for x in r["errores"]), con_k(r, K))
cc = os.path.join(TMP, "viscofan_config", "Viscofan")
shutil.copytree(c, cc)
CEm = VE.EE.CE
k_cfg = next(k for k in inst["celdas"] if k.startswith(CEm.HOJA + "!") and (EVID.get(k) or {}).get("trazabilidad"))
meta_ref = next(iter(EVID[k_cfg]["trazabilidad"]))
lbc = LibroV63(VE.libro_de(cc))
lbc.escribir_celdas({f"{CEm.HOJA}!{meta_ref}": "(prueba) otra fuente de la configuración"})
lbc.guardar(VE.libro_de(cc))
r = con(carpeta=cc)
paso("RI", f"(h14) la trazabilidad de una celda de «Configuración V6.4» ({k_cfg}: {meta_ref}) cambia con el mismo valor: desactualizada", any(x.startswith(k_cfg + ":") for x in r["desactualizadas"]), con_k(r, k_cfg))

# ------------------------------------------------------------------ S · segunda revisión independiente del hito 1 (N1–N4, N8)
JUST_M = "(prueba) cifra de contexto del sector que ninguna fase usa para concluir; revisado por el revisor independiente"
r = con(lambda g: (ent(g, KJ).update(material=False, justificacion_materialidad="x"), ent(g, KJ)["fuente"].update(archivo="fuentes_sinteticas/NO_EXISTE.txt", sha256=None),
                   ent(g, KJ)["comprobacion"].update(revisor=None, resultado="pendiente")), resellar=True)
paso("S", "(N1) juicio declarado no material con justificación «x», fuente ausente y sin revisor: no apta (antes: apta, motivo None)",
     not r["apto_por_entradas"] and any(x.startswith(KJ + ":") for x in r["no_materiales_sin_revisar"]) and r["resumen"], (r["no_materiales_sin_revisar"][:1], r["motivo"]))


def todas_juicio_no_materiales(g):
    for e in g["entradas"]:
        if e.get("ambito") == "juicio":
            e.update(material=False, justificacion_materialidad="x")
            e["comprobacion"].update(revisor=None, resultado="pendiente")


r = con(todas_juicio_no_materiales, resellar=True)
paso("S", f"(N1) el contraejemplo: TODAS las entradas de juicio ({inst['n_juicio']}) no materiales con «x» y sin revisor: no apta, todas listadas",
     not r["apto_por_entradas"] and len(r["no_materiales_sin_revisar"]) == inst["n_juicio"], r["motivo"])
r = con(lambda g: (ent(g, KJ).update(material=False, justificacion_materialidad=JUST_M), ent(g, KJ)["fuente"].update(archivo="fuentes_sinteticas/NO_EXISTE.txt", sha256=None)), resellar=True)
paso("S", "(N1) no material con su justificación revisada y sellada por un revisor independiente (contenido sin contrastar): apta, contada en el resumen",
     r["apto_por_entradas"] and KJ in r["no_materiales_revisados"] and KJ not in r["comprobadas"] and "1 entradas declaradas no materiales (de juicio o auxiliares) (1 con el juicio de materialidad revisado" in str(r["resumen"]), r["resumen"])
r = con(lambda g: (ent(g, KJ).update(material=False, justificacion_materialidad=JUST_M), ent(g, KJ)["fuente"].update(archivo="fuentes_sinteticas/NO_EXISTE.txt", sha256=None),
                   ent(g, KJ)["comprobacion"].update(extractor="revisor sintético")), resellar=True)
paso("S", "(N1) el juicio de materialidad revisado por el propio extractor: no apta", not r["apto_por_entradas"] and any(x.startswith(KJ + ":") for x in r["no_materiales_sin_revisar"]), r["no_materiales_sin_revisar"][:1])


def no_mat_sin_resellar(g):
    ent(g, KJ).update(material=False, justificacion_materialidad=JUST_M)
    ent(g, KJ)["fuente"].update(archivo="fuentes_sinteticas/NO_EXISTE.txt", sha256=None)


r = con(no_mat_sin_resellar)
paso("S", "(N1) la justificación de materialidad escrita después del sello (vínculo de otra versión): no apta", not r["apto_por_entradas"] and any(x.startswith(KJ + ":") for x in r["no_materiales_sin_revisar"]), r["no_materiales_sin_revisar"][:1])
vK = inst["celdas"][K]
AUXC = {"celda": "aux:conv", "id": "aux:conv", "ambito": "auxiliar", "uso": f"origen de {K}", "material": True, "clase": "convencion", "valor_modelo": vK,
        "hipotesis": {"fundamento": "(prueba) convención", "alternativas": ["x"], "limites": ["x"]}, "comprobacion": dict(COMPROBADA, revisor=None, resultado=None), "incidencia": None}


def via_convencion(g, just=None):
    g["entradas"].append(copy.deepcopy(AUXC))
    ent(g, K).update(clase="derivado", fuente={}, derivacion={"origenes": ["aux:conv"], "formula": 'o["aux:conv"]', "conciliacion": "(prueba) igual a la convención", "unidad": "mm"})
    if just:
        ent(g, K)["justificacion_clase"] = just


r = con(via_convencion, resellar=True)
paso("S", "(N2) un dato de cálculo como derivado de un auxiliar «convención» sin fuente y sin «justificacion_clase»: error, no apta (antes: apta, no listado)",
     not r["apto_por_entradas"] and any(x.startswith(K + ":") and "justificacion_clase" in x for x in r["errores"]), con_k(r, K))
r = con(lambda g: via_convencion(g, "(prueba) la cifra es una convención del modelo"), resellar=True)
paso("S", "(N2) el mismo con su justificación y la revisión del derivado: se acredita, pero se lista como dato tratado como hipótesis o convención",
     K in r["comprobadas"] and K in r["datos_como_hipotesis"], r["datos_como_hipotesis"][:2])
r = con(lambda g: (montar_derivado(g), ent(g, k_der)["derivacion"].update(formula=repr(float(vd)))), resellar=True)
paso("S", "(N2) un derivado con una fórmula constante que no usa sus orígenes: error (desde la tercera revisión, por la cifra escrita en la fórmula)", not r["apto_por_entradas"] and any(x.startswith(k_der + ":") and ("orígenes" in x or "cifras" in x) for x in r["errores"]), con_k(r, k_der))
r = con(lambda g: (montar_derivado(g), ent(g, k_der)["derivacion"].update(formula='o["aux:p1"] * 2')), resellar=True)
paso("S", "(N2) un derivado cuya fórmula no usa todos sus orígenes: error", not r["apto_por_entradas"] and any(x.startswith(k_der + ":") and "orígenes" in x for x in r["errores"]), con_k(r, k_der))
r = con()
paso("S", "(N2) los «no aplicable» se cuentan aparte, también con el registro apto", r["apto_por_entradas"] and r["no_aplicables"] and f"{len(r['no_aplicables'])} no aplicables" in str(r["resumen"]), r["resumen"])
k_r = next((k for k, v in inst["celdas"].items() if inst["ambito"].get(k) == "calculo" and isinstance(v, float) and not v.is_integer() and VE._decimales_exactos(v) is not None
            and VE._decimales_exactos(v) <= 3 and ent(REG, k)["clase"] == "dato_publicado" and k != K), None)
if k_r:
    vr = inst["celdas"][k_r]
    va4 = round(vr + 0.0004, 6)
    pr4 = nueva_pagina(f"Magnitud sintética: {va4}")
    AUX4 = {"celda": "aux:r4", "id": "aux:r4", "ambito": "auxiliar", "uso": f"origen de {k_r}", "material": True, "clase": "dato_publicado", "valor_modelo": va4,
            "comprobacion": dict(COMPROBADA), "incidencia": None,
            "fuente": dict(ent(REG, k_r)["fuente"], pagina=pr4, unidad="unidades sintéticas", escala=1, valor_fuente=va4, cita=f"Magnitud sintética: {va4}")}

    def deriva4(g, formula='o["aux:r4"]', unidad=None):
        g["entradas"].append(copy.deepcopy(AUX4))
        ent(g, k_r).update(clase="derivado", fuente={}, derivacion=dict({"origenes": ["aux:r4"], "formula": formula, "conciliacion": "(prueba)"}, **({"unidad": unidad} if unidad else {})))

    r = con(deriva4, resellar=True)
    paso("S", f"(N4) un derivado que no es un importe ({k_r} = {vr} frente a {va4}) sin el redondeo declarado: discrepancia (antes: comprobado por el redondeo a 3 decimales)",
         not r["apto_por_entradas"] and any(x.startswith(k_r + ":") for x in r["discrepancias"]), con_k(r, k_r))
    r = con(lambda g: deriva4(g, formula='round(o["aux:r4"], 3)'), resellar=True)
    paso("S", "(N4) el mismo con el redondeo declarado en la fórmula (round(…, 3)): comprobado", k_r in r["comprobadas"] and r["apto_por_entradas"], con_k(r, k_r))
    r = con(lambda g: deriva4(g, unidad="mm"), resellar=True)
    paso("S", "(N4) el mismo declarado como importe («derivacion.unidad» = «mm»): el redondeo del libro a 3 decimales vale", k_r in r["comprobadas"], con_k(r, k_r))
import inspect  # noqa: E402
paso("S", "(N3) sellar no admite otra fecha del día que la del sistema (sin parámetro «hoy»)", "hoy" not in inspect.signature(VE.sellar).parameters, str(inspect.signature(VE.sellar)))
cs8 = os.path.join(TMP, "viscofan_sellar8", "Viscofan")
shutil.copytree(c, cs8)
reg8 = copy.deepcopy(REG)
reg8["entradas"].append(dict(copy.deepcopy(AUX), celda="aux:ext", id="aux:ext", fuente={k_: v_ for k_, v_ in AUX["fuente"].items() if k_ not in ("archivo", "sha256")}))
ent(reg8, "aux:ext")["fuente"].update(conservacion="externa", lectura_externa=dict(LE))
ent(reg8, KJ).update(material=False, justificacion_materialidad=JUST_M)
ent(reg8, KJ)["fuente"].update(archivo="fuentes_sinteticas/NO_EXISTE.txt", sha256=None)
sellar_todo(reg8, cs8)
for k_ in ("aux:ext", KJ):
    ent(reg8, k_)["comprobacion"].pop("vinculo", None)
    ent(reg8, k_)["comprobacion"]["fecha"] = HOY
json.dump(reg8, open(os.path.join(cs8, VE.REGISTRO), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
ok8, mal8 = VE.sellar(cs8, ["aux:ext", KJ], "revisor sintético", HOY)
paso("S", "(N8; N1) sellar sella la lectura externa de un auxiliar y el juicio de materialidad de una entrada no material (antes: rechazada con «estado True»)",
     sorted(ok8) == sorted(["aux:ext", KJ]) and not mal8, (ok8, mal8))

# ------------------------------------------------------------------ T · tercera revisión independiente del hito 1 (T1–T4)
GR = {"aux:n": 887000000.0, "aux:d": 1000000000.0}
pT = [nueva_pagina(f"Magnitud sintética {n}: {int(v)}") for n, v in GR.items()]


def deriva_grande(g, k_, formula, vm_aux=None, clase_aux="dato_publicado"):
    for (n, v), pg in zip(GR.items(), pT):
        g["entradas"].append({"celda": n, "id": n, "ambito": "auxiliar", "uso": f"origen de {k_}", "material": True, "clase": clase_aux, "valor_modelo": v,
                              "comprobacion": dict(COMPROBADA), "incidencia": None,
                              "fuente": dict(ent(REG, K)["fuente"], pagina=pg, unidad="unidades", escala=1, valor_fuente=int(v), cita=f"Magnitud sintética {n}: {int(v)}")})
    ent(g, k_).update(clase="derivado", fuente={}, derivacion={"origenes": ["aux:n", "aux:d"], "formula": formula, "conciliacion": "(prueba)"})


k_rat = k_r if k_r else K
v_rat = inst["celdas"][k_rat]
GR["aux:n"] = float(round(v_rat * 1e9))  # el ratio exacto n/d con d = 1e9 es el valor del libro
pT = [nueva_pagina(f"Magnitud sintética {n}: {int(v)}") for n, v in GR.items()]
r = con(lambda g: deriva_grande(g, k_rat, 'o["aux:n"] / o["aux:d"]'), resellar=True)
paso("T", f"(T1, control) un ratio de orígenes grandes (≈1e9) que da exactamente el valor del libro ({k_rat}): comprobado", k_rat in r["comprobadas"], con_k(r, k_rat))
r = con(lambda g: deriva_grande(g, k_rat, 'o["aux:n"] / o["aux:d"] / 2'), resellar=True)
paso("T", "(T1) el mismo ratio con orígenes ≈1e9 que da la mitad del valor del libro: discrepancia (antes: comprobado por una tolerancia relativa a los orígenes)",
     not r["apto_por_entradas"] and any(x.startswith(k_rat + ":") for x in r["discrepancias"]), con_k(r, k_rat))
assert VE._eval_formula_exacta('o["a"] - o["b"]', {"a": 120.4, "b": 120.4}) == 0 and float(VE._eval_formula_exacta('o["a"] + o["b"]', {"a": 0.1, "b": 0.2})) == 0.3
assert VE._round_frac(VE._frac(0.12345), 4) == VE._frac(0.1235) and VE._round_frac(VE._frac(-2.5)) == -3
paso("T", "(T1) aritmética exacta: 120,4 − 120,4 = 0 y 0,1 + 0,2 = 0,3 sin tolerancia; round de la hoja (mitad lejos de cero)", True)
for nombre, fml in (("o[x] * 0 + cifra", f'o["aux:p1"] * 0 + {vd!r}'), ("o[x] − o[x] + o[y]", 'o["aux:p1"] - o["aux:p1"] + o["aux:p2"]'),
                    ("min(o[x], cifra) con la cifra como límite", f'min(o["aux:p1"] * 1000, 1) * {vd!r}')):
    r = con(lambda g: (montar_derivado(g), ent(g, k_der)["derivacion"].update(formula=fml)), resellar=True)
    paso("T", f"(T2) fórmula que anula un origen o escribe la cifra ({nombre}): error, no apta (antes: apta y sin listar)",
         not r["apto_por_entradas"] and any(x.startswith(k_der + ":") for x in r["errores"]), con_k(r, k_der)[:1])


def origen_sin_dato(g, clase_o):
    g["entradas"].append({"celda": "aux:sd", "id": "aux:sd", "ambito": "auxiliar", "uso": f"origen de {k_der}", "material": True, "clase": clase_o, "valor_modelo": vd,
                          "justificacion": "(prueba) x", "comprobacion": dict(COMPROBADA), "incidencia": None})
    ent(g, k_der).update(clase="derivado", fuente={}, derivacion={"origenes": ["aux:sd"], "formula": 'o["aux:sd"]', "conciliacion": "(prueba)"})


for clase_o in ("dato_ausente", "no_aplicable"):
    r = con(lambda g: origen_sin_dato(g, clase_o), resellar=True)
    paso("T", f"(T2) un dato derivado de un auxiliar «{clase_o}» que lleva el número: error, no apta (antes: apta y sin listar)",
         not r["apto_por_entradas"] and (any(x.startswith(k_der + ":") for x in r["errores"]) or any(x.startswith("aux:sd:") for x in r["errores"])), (con_k(r, k_der) + con_k(r, "aux:sd"))[:2])
r = con(lambda g: (montar_derivado(g), ent(g, k_der)["derivacion"].update(origenes={"aux:p1": None, "aux:p2": None})), resellar=True)
paso("T", "(T3) «origenes» que no es una lista: error del contrato", not r["apto_por_entradas"] and any(x.startswith(k_der + ":") for x in r["errores"]), con_k(r, k_der)[:1])
r = con(lambda g: ent(g, K)["fuente"].update(unidad="unidades", escala=ent(g, K)["fuente"]["valor_fuente"] and inst["celdas"][K] / ent(g, K)["fuente"]["valor_fuente"] * 7, valor_fuente=ent(g, K)["fuente"]["valor_fuente"] / 7), resellar=True)
paso("T", "(T2, escala libre) con una unidad no monetaria, una escala que no es potencia de diez: error", not r["apto_por_entradas"] and any(x.startswith(K + ":") and "potencia de diez" in x for x in r["errores"]), con_k(r, K)[:1])
sha_txt = hashlib.sha256(open(os.path.join(FS, "fuente.txt"), "rb").read()).hexdigest()  # el texto conservado tras las páginas añadidas
for nombre_aj in ("ajeno.bin", "ajeno.pdf.bak", "ajeno.html"):
    if nombre_aj.endswith(".html"):  # un HTML de otro documento (sin la cita)
        open(os.path.join(FS, nombre_aj), "w", encoding="utf-8").write("<html><body><p>Otro documento sin la cifra citada</p></body></html>")
    else:
        shutil.copy(os.path.join(FS, "fuente.txt"), os.path.join(FS, nombre_aj))
    sha_x = hashlib.sha256(open(os.path.join(FS, nombre_aj), "rb").read()).hexdigest()
    r = con(lambda g: ent(g, K)["fuente"].update(archivo=f"fuentes_sinteticas/{nombre_aj}", sha256=sha_x, archivo_texto="fuentes_sinteticas/fuente.txt", sha256_texto=sha_txt), resellar=True)
    paso("T", f"(T4) bytes ajenos con otro nombre ({nombre_aj}) y un texto conservado: no se acredita (pendiente o discrepancia; antes: comprobada)",
         not r["apto_por_entradas"] and K not in r["comprobadas"], con_k(r, K)[:1])
open(os.path.join(FS, "fuente_html.html"), "w", encoding="utf-8").write("<!DOCTYPE html><html><body>" + "".join(f"<p>{x}</p>" for x in paginas) + "</body></html>")
sha_h = hashlib.sha256(open(os.path.join(FS, "fuente_html.html"), "rb").read()).hexdigest()
r = con(lambda g: ent(g, K)["fuente"].update(archivo="fuentes_sinteticas/fuente_html.html", sha256=sha_h, archivo_texto="fuentes_sinteticas/fuente.txt", sha256_texto=sha_txt), resellar=True)
paso("T", "(T4, control) una fuente HTML que contiene la cita, con su texto conservado: aceptada", r["apto_por_entradas"], con_k(r, K))
open(os.path.join(FS, "escaneado.pdf"), "wb").write(pdf_minimo([p_ if i != int(ent(REG, K)["fuente"]["pagina"]) - 1 else "" for i, p_ in enumerate(paginas)]))
sha_e = hashlib.sha256(open(os.path.join(FS, "escaneado.pdf"), "rb").read()).hexdigest()
r = con(lambda g: ent(g, K)["fuente"].update(archivo="fuentes_sinteticas/escaneado.pdf", sha256=sha_e, archivo_texto="fuentes_sinteticas/fuente.txt", sha256_texto=sha_txt), resellar=True)
paso("T", "(T4) una página del PDF sin capa de texto: pendiente (no se afirma que el texto conservado sea otro)",
     not r["apto_por_entradas"] and any("capa de texto" in x for x in con_k(r, K, ("pendientes",))), con_k(r, K)[:1])

# ------------------------------------------------------------------ E · entrada efectiva reproducible (C48 de Elis)
cE = os.path.join(TMP, "viscofan_efectiva", "Viscofan")
shutil.copytree(c, cE)
shutil.copy2(os.path.join(E413, "viscofan", "Viscofan", "fase1_v63.json"), os.path.join(cE, "fase1_v63.json"))  # la declaración original de la 4.13
nr = VE.entradas_no_reproducibles(cE, VE.universo(cE))
r = con(carpeta=cE)
paso("E", f"entradas del FCF base que la vía generativa no reproduce (libro ≠ fase1_v63.json: {sorted(nr)}): discrepancia, no apta, aunque su registro esté comprobado",
     bool(nr) and not r["apto_por_entradas"] and all(any(x.startswith(k + ":") and "reproducible" in x for x in r["entradas_no_reproducibles"]) for k in nr) and len(r["entradas_no_reproducibles"]) == len(nr)
     and all(k not in r["comprobadas"] for k in nr),
     r["entradas_no_reproducibles"][:1])
paso("E", "con la declaración alineada con el libro (fixture), ninguna entrada no reproducible", not VE.entradas_no_reproducibles(c, inst) and not con()["entradas_no_reproducibles"])
cE2 = os.path.join(TMP, "viscofan_efectiva2", "Viscofan")
shutil.copytree(c, cE2)
os.remove(os.path.join(cE2, "fase1_v63.json"))
r = con(carpeta=cE2)
paso("E", "(h4) sin fase1_v63.json: no se puede determinar la entrada efectiva y no es apta (antes: apta)", not r["apto_por_entradas"] and r["entradas_no_reproducibles"], r["entradas_no_reproducibles"][:1])
json.dump([], open(os.path.join(cE2, "fase1_v63.json"), "w"))
try:
    r = con(carpeta=cE2); sin_excepcion = True
except Exception:  # noqa: BLE001
    sin_excepcion = False
paso("E", "(h4) fase1_v63.json que no es un objeto (una lista): sin excepción y no apta", sin_excepcion and not r["apto_por_entradas"])
f1x = json.load(open(os.path.join(c, "fase1_v63.json"), encoding="utf-8"))
f1x["analisis"].pop("C50", None)
json.dump(f1x, open(os.path.join(cE2, "fase1_v63.json"), "w", encoding="utf-8"), ensure_ascii=False)
r = con(carpeta=cE2)
paso("E", "(h4) una entrada del FCF base con valor en el libro que fase1_v63.json NO declara (el caso real de Vidrala C50): no reproducible, no apta",
     not r["apto_por_entradas"] and any(x.startswith("Análisis!C50:") for x in r["entradas_no_reproducibles"]), r["entradas_no_reproducibles"][:1])
shutil.copy2(os.path.join(c, "fase1_v63.json"), os.path.join(cE2, "fase1_v63.json"))
f1y = json.load(open(os.path.join(cE2, "fase1_v63.json"), encoding="utf-8"))
f1y["analisis"]["C47"] = dict(f1y["analisis"]["C47"], fuente="(prueba) fuente cambiada después del sello")
json.dump(f1y, open(os.path.join(cE2, "fase1_v63.json"), "w", encoding="utf-8"), ensure_ascii=False)
r = con(carpeta=cE2)
paso("E", "(h4) editar la declaración de fase1_v63.json después del sello (mismo número) deja la entrada desactualizada: el vínculo incluye la declaración",
     any(x.startswith("Análisis!C47:") for x in r["desactualizadas"]), con_k(r, "Análisis!C47"))

# ------------------------------------------------------------------ SG · signo de la cifra publicada (4.15, hito 2, R415-SIGNO)
# «valor_fuente» es la cifra publicada con su signo; «signo» y «escala» la transforman después hacia el modelo. Contraejemplos completos
# (registro positivo, página conservada y cita cambiadas, huella y vínculos rehechos) en los dos sentidos y positivos con paréntesis.
VF_K = ent(REG, K)["fuente"]["valor_fuente"]
VM_K = ent(REG, K)["valor_modelo"]
assert VF_K > 0 and ent(REG, K)["fuente"]["signo"] == 1


def con_signo(texto_pagina, cita=None, vf=VF_K, signo=1, tratamiento=None, extra=None):
    pg = nueva_pagina(texto_pagina)
    def cambio(g):
        f = ent(g, K)["fuente"]
        f.update(pagina=pg, cita=cita if cita is not None else texto_pagina, valor_fuente=vf, signo=signo)
        if tratamiento:
            f["tratamiento"] = tratamiento
        if extra:
            extra(g)
    return con(cambio, resellar=True)


TRAT = "pago publicado en negativo; el modelo usa su magnitud positiva (signo −1)"
r = con_signo(f"Partida sintética de {K}: -{VF_K:.3f}")
paso("SG", "contraejemplo de la revisión externa: página y cita «-849697.000» con valor_fuente positivo, signo 1 y tratamiento «ninguno»: discrepancia, no apta (antes: apta y comprobada)",
     not r["apto_por_entradas"] and K not in r["comprobadas"] and any("R415-SIGNO" in x for x in con_k(r, K, ("discrepancias",))), con_k(r, K))
r = con_signo(f"Partida sintética de {K}: {VF_K:.3f}", vf=-VF_K, signo=-1, tratamiento=TRAT)
paso("SG", "sentido inverso: la página publica la cifra en positivo y valor_fuente es negativo (con signo −1, el modelo cuadra): discrepancia, no apta",
     not r["apto_por_entradas"] and any("R415-SIGNO" in x for x in con_k(r, K, ("discrepancias",))), con_k(r, K))
r = con_signo(f"Partida sintética de {K}: ({VF_K:,.3f})")
paso("SG", "cantidad positiva frente a un pago publicado entre paréntesis «(849,697.000)»: discrepancia", not r["apto_por_entradas"] and con_k(r, K, ("discrepancias",)), con_k(r, K))
r = con_signo(f"Partida sintética de {K}: ({VF_K:,.3f})", vf=-VF_K, signo=-1, tratamiento=TRAT)
paso("SG", "positivo: pago publicado entre paréntesis, valor_fuente negativo y transformación justificada (signo −1) hacia la magnitud del modelo: apta",
     r["apto_por_entradas"] and K in r["comprobadas"], con_k(r, K))
r = con_signo(f"Partida sintética de {K}: \u2212{VF_K:,.3f}".replace(",", " ").replace(".", ","), vf=-VF_K, signo=-1, tratamiento=TRAT)
paso("SG", "positivo: signo menos Unicode «−849 697,000» con valor_fuente negativo: apta", r["apto_por_entradas"] and K in r["comprobadas"], con_k(r, K))
r = con_signo(f"Partida sintética de {K}: \u2013{VF_K:.3f}", vf=-VF_K, signo=-1, tratamiento=TRAT)
paso("SG", "positivo: guion tipográfico pegado «–849697.000» (signo menos) con valor_fuente negativo: apta", r["apto_por_entradas"] and K in r["comprobadas"], con_k(r, K))
r = con_signo(f"Partida sintética de {K}: -{VF_K:.3f}", vf=-VF_K, signo=1)
paso("SG", "la cifra y su signo coinciden, pero la transformación no lleva al modelo (valor_fuente negativo con signo +1): discrepancia de signo × escala",
     not r["apto_por_entradas"] and any("signo × escala" in x for x in con_k(r, K, ("discrepancias",))), con_k(r, K))
r = con_signo(f"Partida sintética de {K} - {VF_K:.3f}")
paso("SG", "guion a un espacio de la cifra («… - 849697.000»: cero de otra columna o signo menos): pendiente, no apta aunque el revisor la declare verificada",
     not r["apto_por_entradas"] and any("no puede determinarse" in x for x in con_k(r, K, ("pendientes",))), con_k(r, K))
r = con_signo(f"Partida sintética de {K}        -          {VF_K:,.3f}", cita=f"Partida sintética de {K} - {VF_K:,.3f}")
paso("SG", "positivo: el guion está en otra columna de la página conservada (dos o más espacios), aunque la cita normalice los espacios: apta",
     r["apto_por_entradas"] and K in r["comprobadas"], con_k(r, K))
r = con_signo(f"Partida sintética de {K}: {VF_K:.3f} ({VF_K:.3f})")
paso("SG", "la cita publica la misma cifra con los dos signos: pendiente (el signo no puede determinarse)", not r["apto_por_entradas"] and con_k(r, K, ("pendientes",)), con_k(r, K))
r = con_signo(f"Partida sintética de {K}: -({VF_K:.3f})", vf=-VF_K, signo=-1, tratamiento=TRAT)
paso("SG", "dos marcas pegadas «-(849697.000)»: pendiente", not r["apto_por_entradas"] and con_k(r, K, ("pendientes",)), con_k(r, K))
r = con_signo(f"Partida sintética de {K}: {VF_K:.3f}-", vf=VF_K)
paso("SG", "menos detrás de la cifra «849697.000-»: pendiente", not r["apto_por_entradas"] and con_k(r, K, ("pendientes",)), con_k(r, K))
casos_ok = [("Importe: (149.5)", -149.5), ("Importe: \u2212149,5", -149.5), ("Importe: -149,5", -149.5),
            ("Importe: \u2014149,5", -149.5), ("(\u20ac149,5)", -149.5), ("(149,5 \u20ac)", -149.5), ("-\u20ac149,5", -149.5), ("+149,5", 149.5),
            ("Importe: 149,5", 149.5), ("Saldo 0", 0), ("Saldo (0)", 0), ("Saldo -0", 0), ("Acquisitions  -   (12.3)", 0), ("Acquisitions  -   (12.3)", -12.3),
            ("Payments -55.320 -62.755", -62755), ("Interest paid (7,230) (9,776)", -9776), ("2019-2020", 2019),
            ("2019-2020", 2020)]  # (hito 2, H5) un guion pegado a otra cifra es un intervalo o una fecha, no un signo
casos_no = [("Importe: -149.5", 149.5, "signo_distinto"), ("Importe: 149.5", -149.5, "signo_distinto"), ("Importe: (149.5)", 149.5, "signo_distinto"),
            ("Importe: \u2212149,5", 149.5, "signo_distinto"), ("Importe - 149,5", 149.5, "signo_indeterminado"), ("Importe - 149,5", -149.5, "signo_indeterminado"),
            ("x 149,5 (149,5)", 149.5, "signo_indeterminado"), ("-(149,5)", -149.5, "signo_indeterminado"), ("(149,5", -149.5, "signo_indeterminado"),
            # (hito 2, H4) «−» a un espacio: una fuente real (Elis 2017) usa «−» para imprimir un cero, así que es tan ambiguo como el guion
            ("Importe: \u2212 149,5", -149.5, "signo_indeterminado"),
            ("149,5-", 149.5, "signo_indeterminado"), ("EBITDA-149,5", -149.5, "signo_indeterminado"),
            ("Importe: 150", 149.5, "ausente"), ("Importe: -150", -149.5, "ausente")]
mal = [(c_, v_, VE._cita_cifra(c_, v_)) for c_, v_ in casos_ok if VE._cita_cifra(c_, v_)[0] != "ok"]
mal += [(c_, v_, VE._cita_cifra(c_, v_)) for c_, v_, esp in casos_no if VE._cita_cifra(c_, v_)[0] != esp]
paso("SG", f"_cita_cifra: {len(casos_ok)} formas con el signo publicado correcto aceptadas y {len(casos_no)} rechazadas con su categoría "
           "(signo contrario, indeterminado o ausente; menos ASCII y Unicode, guiones, paréntesis, moneda, cero sin signo)", not mal, mal[:3])
try:
    mal_formadas = [VE._cita_cifra(None, 5), VE._cita_cifra("x 5", None), VE._cita_cifra("x 5", float("nan")), VE._cita_cifra("x 5", "5"), VE._cita_cifra(12345, 12345)]
    ok_mf = [x[0] for x in mal_formadas] == ["ausente", "ausente", "ausente", "ausente", "ok"]
except Exception as ex:  # noqa: BLE001
    ok_mf, mal_formadas = False, repr(ex)
paso("SG", "entradas mal formadas (cita None o no textual, valor None, NaN o texto): diagnóstico controlado, sin excepción", ok_mf, mal_formadas)
r = con(lambda g: ent(g, K)["fuente"].update(valor_fuente=float("nan")), resellar=True)
paso("SG", "valor_fuente NaN en el registro: error del contrato, sin excepción", not r["apto_por_entradas"] and con_k(r, K, ("errores",)), con_k(r, K))
r = con()
paso("SG", "el control positivo sigue apto después de los casos de signo", r["apto_por_entradas"], (r["errores"] + r["discrepancias"] + r["pendientes"])[:2])

# ------------------------------------------------------------------ U · límites U1–U5 de la cuarta revisión (4.15, hito 2)
import time as _time  # noqa: E402


def montar_media(g, a, b, unidad="mm", formula='(o["aux:m1"] + o["aux:m2"]) / 2'):
    base_f = dict(ent(g, K)["fuente"])
    for nom, v in (("aux:m1", a), ("aux:m2", b)):
        g["entradas"].append({"celda": nom, "id": nom, "ambito": "auxiliar", "uso": f"origen de {k_der}", "material": True, "clase": "dato_publicado", "valor_modelo": v,
                              "fuente": dict(base_f, pagina=PG_M[nom], valor_fuente=round(v * 1000), cita=f"Partida sintética de {nom}: {round(v * 1000):d}",
                                             periodo=ent(g, k_der)["fuente"]["periodo"], columna=ent(g, k_der)["fuente"]["columna"]),
                              "comprobacion": dict(COMPROBADA), "incidencia": None})
    ent(g, k_der).update(clase="derivado", fuente={}, derivacion=dict({"origenes": ["aux:m1", "aux:m2"], "formula": formula, "conciliacion": "(prueba) media de dos"},
                                                                        **({"unidad": unidad} if unidad else {})))


def casos_media(a, b):
    PG_M["aux:m1"] = nueva_pagina(f"Partida sintética de aux:m1: {round(a * 1000):d}")
    PG_M["aux:m2"] = nueva_pagina(f"Partida sintética de aux:m2: {round(b * 1000):d}")


PG_M = {}
v3 = round(vd, 3)
assert abs(v3 - vd) < 1e-12
casos_media(v3, round(v3 + 0.001, 3))  # media exacta = libro + 0,0005: empate
r = con(lambda g: montar_media(g, v3, round(v3 + 0.001, 3)), resellar=True)
paso("U", "(U2) importe: la media de dos valores con empate x,xxx5 (exacto = libro + 0,0005) se acepta con el valor del libro (antes: discrepancia en ~11 % de las medias pares)",
     k_der in r["comprobadas"], con_k(r, k_der))
casos_media(v3, round(v3 - 0.001, 3))
r = con(lambda g: montar_media(g, v3, round(v3 - 0.001, 3)), resellar=True)
paso("U", "(U2) el empate en el otro sentido (exacto = libro − 0,0005): también", k_der in r["comprobadas"], con_k(r, k_der))
casos_media(v3, round(v3 + 0.003, 3))
r = con(lambda g: montar_media(g, v3, round(v3 + 0.003, 3)), resellar=True)
paso("U", "(U2) sin tolerancia general: la media exacta libro + 0,0015 no es el libro: discrepancia", not r["apto_por_entradas"] and any(x.startswith(k_der + ":") for x in r["discrepancias"]), con_k(r, k_der))
casos_media(v3, round(v3 + 0.001, 3))
r = con(lambda g: montar_media(g, v3, round(v3 + 0.001, 3), unidad=None), resellar=True)
paso("U", "(U2) el empate solo vale en un importe: sin «derivacion.unidad» monetaria la media de empate es una discrepancia (exacta o round declarado)",
     not r["apto_por_entradas"] and any(x.startswith(k_der + ":") for x in r["discrepancias"]), con_k(r, k_der))
F_ = VE.fractions.Fraction
paso("U", "(U2) _importe_libro_exacto: 849,0 no es 849,697; 849,6976 no es 849,697; 0,2511 no es 0,25; 849,6974 sí es 849,697; un libro con 4 decimales no se redondea",
     not VE._importe_libro_exacto(F_(849), 849.697) and not VE._importe_libro_exacto(F_("849.6976"), 849.697) and not VE._importe_libro_exacto(F_("0.2511"), 0.25)
     and VE._importe_libro_exacto(F_("849.6974"), 849.697) and not VE._importe_libro_exacto(F_("849.6974"), 849.6972) and VE._importe_libro_exacto(F_("849.6975"), 849.698))
for nombre_u3, fml in (("round con 999999999999 decimales", 'round(o["aux:p1"], 999999999999) + o["aux:p2"]'), ("round con decimales negativos", 'round(o["aux:p1"], -9) + o["aux:p2"]'),
                       ("round con decimales no literales", 'round(o["aux:p1"], o["aux:p2"]) + o["aux:p2"]'),
                       ("fórmula de más de 2000 caracteres", "(" + " + ".join(['o["aux:p1"] * 1'] * 200) + ') / 200 + o["aux:p2"]')):
    t0 = _time.time()
    r = con(lambda g: (montar_derivado(g), ent(g, k_der)["derivacion"].update(formula=fml)), resellar=True)
    paso("U", f"(U3) {nombre_u3}: error del contrato en un tiempo acotado (antes, con decimales enormes, comprobar no terminaba)",
         not r["apto_por_entradas"] and any(x.startswith(k_der + ":") for x in r["errores"]) and _time.time() - t0 < 60, (round(_time.time() - t0, 1), con_k(r, k_der)[:1]))
cli = subprocess.run([sys.executable, "-B", os.path.join(PV, "scripts", "verificacion_entradas.py"), "comprobar", c], capture_output=True, text=True, timeout=300)
paso("U", "(U3) la orden «comprobar» termina con el registro anterior (código 1, no apto)", cli.returncode == 1, cli.stdout[-160:])
sens = {"origen −1": ('o["a"] + o["b"]', {"a": 850.697, "b": -1.0}), "producto con un cero": ('o["a"] * o["b"]', {"a": 0.25, "b": 0.0}),
        "0 / d": ('o["a"] / o["b"]', {"a": 0.0, "b": 190.537}), "max de dos partidas": ('max(o["a"], o["b"])', {"a": 849.697, "b": 100.25}),
        "max(a − b, 0)": ('max(o["a"] - o["b"], 0)', {"a": 5.0, "b": 2.0})}
mal_s = {n_: VE._sensibilidad(f_, v_, list(v_)) for n_, (f_, v_) in sens.items()}
mal_s = {n_: x for n_, x in mal_s.items() if x[0] or not x[1]} | {n_: VE._constantes_no_admitidas(f_) for n_, (f_, v_) in sens.items() if VE._constantes_no_admitidas(f_)}
paso("U", "(U4) derivaciones legítimas en casos límite (origen −1, producto con cero, 0 / d, max de dos partidas, max(a − b, 0)): ningún origen inerte (antes: error)", not mal_s, mal_s)
siguen = {"o[x] * 0 + 12": ('o["a"] * 0 + 12', {"a": 2019}), "o[x] − o[x] + o[y]": ('o["a"] - o["a"] + o["b"]', {"a": 2019, "b": 849.697}),
          "min(o[x], 12) como límite": ('min(o["a"], 12)', {"a": 2019})}
no_rech = []
for n_, (f_, v_) in siguen.items():
    try:
        ine, loc = VE._sensibilidad(f_, v_, list(v_))
        if not (ine or not loc or VE._constantes_no_admitidas(f_)):
            no_rech.append(n_)
    except ValueError:
        pass
paso("U", "(U4) siguen rechazadas las formas triviales: o[x] * 0 + c (constante 0 fuera de min/max), o[x] − o[x] + o[y] y min(o[x], c) como límite (constante en el punto real)", not no_rech, no_rech)
PG_X = {"aux:p1": pa_, "aux:p2": pb_}
r = con(lambda g: (montar_derivado(g), ent(g, k_der)["derivacion"].update(formula='max(o["aux:p1"] + o["aux:p2"], o["aux:p2"])')), resellar=True)
paso("U", "(U4) en el registro: un max cuyo segundo argumento no es el mayor deriva el valor (antes: «no influye»)", k_der in r["comprobadas"], con_k(r, k_der))
r = con(lambda g: (montar_derivado(g), ent(g, k_der)["derivacion"].update(formula='o["aux:p1"] + o["aux:p2"] + 13 - 13')), resellar=True)
paso("U", "(U4/U8) un caso que solo detecta el control de constantes («+ 13 − 13» con el valor exacto): error «escribe cifras»",
     not r["apto_por_entradas"] and any(x.startswith(k_der + ":") and "escribe cifras" in x for x in r["errores"]), con_k(r, k_der)[:1])
r = con(lambda g: (montar_derivado(g)), resellar=True)
paso("U", "(U1) los derivados comprobados se cuentan y se listan en el resumen (el control no acredita su significado económico: lo hace la revisión independiente)",
     k_der in r["derivados_comprobados"] and "derivados comprobados" in str(r["resumen"]) and "revisión independiente" in str(r["resumen"]), r["resumen"][-200:])
sha_txt2 = hashlib.sha256(open(os.path.join(FS, "fuente.txt"), "rb").read()).hexdigest()
CITA_K = ent(REG, K)["fuente"]["cita"]


def con_html(nombre, contenido_bytes):
    open(os.path.join(FS, nombre), "wb").write(contenido_bytes)
    sha_x = hashlib.sha256(contenido_bytes).hexdigest()
    return con(lambda g: ent(g, K)["fuente"].update(archivo=f"fuentes_sinteticas/{nombre}", sha256=sha_x, archivo_texto="fuentes_sinteticas/fuente.txt", sha256_texto=sha_txt2), resellar=True)


html_malos = {"en un comentario con «>»": f"<html><body><!-- nota > {CITA_K} --><p>otro texto</p></body></html>",
              "en un atributo con «>»": f'<html><head><meta name="d" content="resumen > {CITA_K}"></head><body><p>otro</p></body></html>',
              "en un <script> cerrado con «</script >»": f"<html><body><script>var a = '{CITA_K}';</script ><p>otro</p></body></html>",
              "en un <script> sin cerrar": f"<html><body><p>otro</p><script>var a = '{CITA_K}';",
              "en el <title>": f"<html><head><title>{CITA_K}</title></head><body><p>otro</p></body></html>",
              "en un elemento oculto": f'<html><body><div style="display:none">{CITA_K}</div><p>otro</p></body></html>',
              "en un <template>": f"<html><body><template><p>{CITA_K}</p></template><p>otro</p></body></html>",
              "partida en dos celdas contiguas": "<html><body><table><tr><td>" + CITA_K[:-7] + "</td><td>" + CITA_K[-7:] + "</td></tr></table></body></html>"}
mal_h = {}
for i_, (n_, h_) in enumerate(html_malos.items()):
    r = con_html(f"u5_{i_}.html", h_.encode("utf-8"))
    if r["apto_por_entradas"] or K in r["comprobadas"]:
        mal_h[n_] = con_k(r, K)[:1]
paso("U", f"(U5) la cita que solo está {', '.join(html_malos)}: no se acredita (antes: aceptada en varios de estos casos)", not mal_h, mal_h)
r = con_html("u5_latin1.html", f'<html><head><meta charset="iso-8859-1"></head><body><p>Página: {CITA_K}</p></body></html>'.encode("iso-8859-1"))
paso("U", "(U5) un HTML legítimo en ISO-8859-1 con su charset declarado: aceptado (antes: discrepancia en falso)", r["apto_por_entradas"], con_k(r, K))
r = con_html("u5_utf16.html", f"<html><body><p>{CITA_K}</p></body></html>".encode("utf-16"))
paso("U", "(U5) un HTML legítimo en UTF-16 con BOM: aceptado", r["apto_por_entradas"], con_k(r, K))
r = con_html("u5_sin_decl.html", f"<html><body><p>Página: {CITA_K}</p></body></html>".encode("iso-8859-1"))
paso("U", "(U5) un HTML que no es UTF-8 y no declara su codificación: pendiente (no se adivina)", not r["apto_por_entradas"] and any("codificación" in x for x in con_k(r, K, ("pendientes",))), con_k(r, K)[:1])
mal_u7 = {}
for u7 in ("miles de €", "en miles de euros", "MM€", "USD (millones)"):
    r = con(lambda g, u7=u7: ent(g, K)["fuente"].update(unidad=u7, escala=1, valor_fuente=VM_K), resellar=True)
    if r["apto_por_entradas"] or not any("unidad monetaria no reconocida" in x for x in con_k(r, K, ("pendientes",))):
        mal_u7[u7] = con_k(r, K)[:1]
paso("U", "(U7) una unidad monetaria que el vocabulario no reconoce («miles de €», «en miles de euros», «MM€», «USD (millones)») con escala 1: pendiente (antes: comprobada)",
     not mal_u7, mal_u7)
paso("U", "(U7) un precio por acción («EUR por acción», «euros por acción», «EUR per share») no es una unidad monetaria sin reconocer",
     not any(VE._unidad_monetaria_no_reconocida(x) for x in ("EUR por acción", "euros por acción", "EUR per share")) and VE._unidad_monetaria_no_reconocida("euro"))
r = con()
paso("U", "el control positivo sigue apto después de los casos U", r["apto_por_entradas"], (r["errores"] + r["discrepancias"] + r["pendientes"])[:2])

# ------------------------------------------------------------------ RV · hallazgos de la revisión independiente del hito 2 (H1, H4–H7, H14)
r = con_signo(f"Partida sintética de {K}: -{VF_K:.3f}", cita=f"{VF_K:.3f}")
paso("RV", "(H1) la variante de la sonda externa: la página publica «-849697.000» y la cita se recorta a «849697.000»: discrepancia (antes: apta y comprobada)",
     not r["apto_por_entradas"] and K not in r["comprobadas"] and any("R415-SIGNO" in x for x in con_k(r, K, ("discrepancias",))), con_k(r, K))
r = con_signo(f"Partida sintética de {K}: ({VF_K:,.3f})", cita=f"{VF_K:,.3f}")
paso("RV", "(H1) página con paréntesis contables y cita recortada a la cifra: discrepancia", not r["apto_por_entradas"] and con_k(r, K, ("discrepancias",)), con_k(r, K))
r = con_signo(f"Partida sintética de {K}: \u2212{VF_K:.3f}", cita=f"{VF_K:.3f}")
paso("RV", "(H1) página con menos Unicode pegado y cita recortada: discrepancia", not r["apto_por_entradas"] and con_k(r, K, ("discrepancias",)), con_k(r, K))
r = con_signo(f"Partida sintética de {K}: {VF_K * 10:.0f}", cita=f"Partida sintética de {K}: {VF_K:.0f}")
paso("RV", "(H1/R3) cita cortada dentro de un número (la página publica 8496970 y la cita «…: 849697»): discrepancia (la cifra completa es la de la página)",
     not r["apto_por_entradas"] and any("cifra completa de la página" in x for x in con_k(r, K, ("discrepancias",))), con_k(r, K))
r = con_signo(f"Partida sintética de {K}: 1{VF_K:.3f}", cita=f"{VF_K:.3f}")
paso("RV", "(H1/R3) cita que empieza dentro de un número (página 1849697.000, cita «849697.000»): discrepancia", not r["apto_por_entradas"] and con_k(r, K, ("discrepancias",)), con_k(r, K))
r = con_signo(f"Partida sintética de {K}: {VF_K:.3f} y otra línea\nPartida sintética de {K}: -{VF_K:.3f}", cita=f"{VF_K:.3f}")
paso("RV", "(H1) la cita aparece dos veces en la página con lecturas distintas (positiva y con signo menos): pendiente", not r["apto_por_entradas"] and con_k(r, K, ("pendientes",)), con_k(r, K))
r = con_signo(f"Partida sintética de {K}: ({VF_K:,.3f})", cita=f"{VF_K:,.3f}", vf=-VF_K, signo=-1, tratamiento=TRAT)
paso("RV", "(H1, positivo) cita recortada a la cifra con valor_fuente negativo y la transformación declarada: apta (la cifra y su signo son los de la página)",
     r["apto_por_entradas"] and K in r["comprobadas"], con_k(r, K))
r = con(lambda g: ent(g, K)["fuente"].update(signo=-1, valor_fuente=-ent(g, K)["fuente"]["valor_fuente"], tratamiento="ninguno"), resellar=True)
paso("RV", "(H14) signo −1 con el tratamiento «ninguno»: error (un cambio de signo declara su tratamiento)", not r["apto_por_entradas"] and any("tratamiento" in x for x in con_k(r, K, ("errores",))), con_k(r, K))
casos_rv = {("Acquisitions \u2212", 0): "ok", ("Acquisitions  \u2212   (12.3)", 0): "ok", ("Dividends \u2212 42.2", 42.2): "signo_indeterminado",
            ("Dividends \u2212 42.2", -42.2): "signo_indeterminado", ("Importe (EUR 149,5)", -149.5): "ok", ("Importe (EUR 149,5)", 149.5): "signo_distinto",
            ("Margen (3,2 %)", -3.2): "ok", ("Importe $-149,5", -149.5): "ok", ("Importe $-149,5", 149.5): "signo_distinto", ("Cierre 31-12-2024", 2024): "ok",
            ("Ejercicio 2019-2020", 2020): "ok"}
mal_rv = {k_: VE._cita_cifra(*k_) for k_, e_ in casos_rv.items() if VE._cita_cifra(*k_)[0] != e_}
paso("RV", "(H4, H5) «−» aislado como cero; «− x» a un espacio, indeterminado como con el guion; moneda con código y porcentaje dentro de los paréntesis; «$-x»; fechas e intervalos",
     not mal_rv, mal_rv)
pag_rv = "Partida A: 849697.000\nPartida A: -849697.000"
paso("RV", "(H1) _cita_cifra con la página: no localizada → «no_localizada»; dos apariciones con lecturas distintas → indeterminado; cifra recortada → la de la página",
     VE._cita_cifra("Partida Z: 1", 1, pag_rv)[0] == "no_localizada" and VE._cita_cifra("849697.000", 849697, pag_rv)[0] == "signo_indeterminado"
     and VE._cita_cifra("849697.000", 849697, "Total -849697.000")[0] == "signo_distinto" and VE._cita_cifra("Partida: 0", 0, "Partida: 0.49")[0] == "ausente")
esc_max = ['max(o["a"], o["b"])', 'max( o["a"] ,o["b"] )', 'max(o["b"], o["a"])', '(max(o["a"], o["b"]))', 'max(o["a"],\n o["b"])']
vers = {f_: VE._sensibilidad(f_, {"a": 849.697, "b": 100.25}, ["a", "b"])[0] for f_ in esc_max}
paso("RV", "(H6) escrituras equivalentes de max(a, b) con b el menor: el mismo veredicto (ningún origen inerte) en todas", all(v_ == [] for v_ in vers.values()), vers)
ine_s, loc_s = VE._sensibilidad('max(o["a"] - o["b"], 0)', {"a": 2.0, "b": 5.0}, ["a", "b"])
paso("RV", "(H6) max(a − b, 0) cuando actúa el suelo: sin orígenes inertes, constante en el punto real pero con suelo cero declarado (se acepta como la regla de la fórmula)",
     ine_s == [] and not loc_s and VE._suelo_cero('max(o["a"] - o["b"], 0)') and not VE._suelo_cero('min(o["a"], 12)'), (ine_s, loc_s))
h7 = {"details cerrado": (f"<html><body><details><summary>Resumen</summary><p>{CITA_K}</p></details><p>otro</p></body></html>", False),
      "summary de un details cerrado": (f"<html><body><details><summary>{CITA_K}</summary><p>x</p></details></body></html>", True),
      "dialog sin open": (f"<html><body><dialog><p>{CITA_K}</p></dialog><p>otro</p></body></html>", False),
      "<div hidden/> (la barra no cierra)": (f"<html><body><div hidden/><p>{CITA_K}</p></div><p>otro</p></body></html>", False),
      "aria-hidden (visible en pantalla)": (f'<html><body><p aria-hidden="true">{CITA_K}</p></body></html>', True),
      "sin </head>": (f"<html><head><title>t</title><body><p>{CITA_K}</p></body></html>", True),
      "iXBRL en línea": ("<html><body><p>" + CITA_K.replace(f"{VF_K:.3f}", f"<ix:nonFraction name='x'>{VF_K:.3f}</ix:nonFraction>") + "</p></body></html>", True)}
mal_h7 = {}
for i_, (n_, (h_, visible)) in enumerate(h7.items()):
    open(os.path.join(FS, f"h7_{i_}.html"), "w", encoding="utf-8").write(h_)
    est_, t_ = VE._texto_html_visible(os.path.join(FS, f"h7_{i_}.html"))
    if est_ != "ok" or (VE._cmp_txt_espacios(CITA_K) in VE._cmp_txt_espacios(t_)) != visible:
        mal_h7[n_] = (est_, t_[:80])
open(os.path.join(FS, "h7_cp1252.html"), "wb").write(f'<html><head><meta charset="iso-8859-1"></head><body><p>\u20ac 5 \u2013 {CITA_K}</p></body></html>'.encode("cp1252"))
est_, t_ = VE._texto_html_visible(os.path.join(FS, "h7_cp1252.html"))
if not (est_ == "ok" and "\u20ac" in t_ and "\u2013" in t_):
    mal_h7["ISO-8859-1 con bytes de windows-1252"] = (est_, t_[:80])
open(os.path.join(FS, "h7_utf7.html"), "wb").write(b'<html><head><meta charset="utf-7"></head><body><p>x</p></body></html>')
if VE._texto_html_visible(os.path.join(FS, "h7_utf7.html"))[0] != "pendiente":
    mal_h7["charset=utf-7"] = "no pendiente"
open(os.path.join(FS, "h7_menciona.html"), "w", encoding="utf-8").write(f"<html><body><p>El formato %PDF-1.4</p><p>{CITA_K}</p></body></html>")
if VE._tipo_fuente(os.path.join(FS, "h7_menciona.html")) != "html":
    mal_h7["HTML que menciona %PDF-"] = VE._tipo_fuente(os.path.join(FS, "h7_menciona.html"))
paso("RV", f"(H7) HTML: {', '.join(list(h7) + ['ISO-8859-1 con bytes de windows-1252', 'charset=utf-7 (pendiente)', 'HTML que menciona %PDF-'])}", not mal_h7, mal_h7)
r = con()
paso("RV", "el control positivo sigue apto después de los casos RV", r["apto_por_entradas"], (r["errores"] + r["discrepancias"] + r["pendientes"])[:2])

# ------------------------------------------------------------------ N · recuentos (I9) en la ficha y el informe
env = dict(os.environ, MUNGER_CONFIG=CFG)
con()
subprocess.run([sys.executable, "-B", os.path.join(PV, "scripts", "ficha.py"), c, "--provisional"], capture_output=True, text=True, env=env)
subprocess.run([sys.executable, "-B", os.path.join(PV, "scripts", "informe.py"), c, "--provisional"], capture_output=True, text=True, env=env)
inf = open(os.path.join(c, "informe_provisional.md"), encoding="utf-8").read() if os.path.exists(os.path.join(c, "informe_provisional.md")) else ""
m = re.search(r"(\d+) de (\d+) celdas del universo comprobadas \((\d+) de (\d+) de cálculo y (\d+) de (\d+) usadas por el juicio\)", inf)
paso("N", "el informe dice «N de M celdas» con N ≤ M y separa cálculo y juicio (antes: «330 de 232»)",
     bool(m) and int(m.group(1)) <= int(m.group(2)) and int(m.group(3)) + int(m.group(5)) == int(m.group(1)) and int(m.group(4)) + int(m.group(6)) == int(m.group(2)), m.group(0) if m else (re.findall(r"Verificación de las entradas financieras:.{0,260}", inf) or [inf[:200]])[0])
r = con(lambda g: g["entradas"].remove(ent(g, K)))
subprocess.run([sys.executable, "-B", os.path.join(PV, "scripts", "informe.py"), c, "--provisional"], capture_output=True, text=True, env=env)
subprocess.run([sys.executable, "-B", os.path.join(PV, "scripts", "ficha.py"), c, "--provisional"], capture_output=True, text=True, env=env)
subprocess.run([sys.executable, "-B", os.path.join(PV, "scripts", "informe.py"), c, "--provisional"], capture_output=True, text=True, env=env)
inf = open(os.path.join(c, "informe_provisional.md"), encoding="utf-8").read()
m = re.search(r"(\d+) de (\d+) celdas del universo comprobadas", inf)
paso("N", "con una entrada menos, el informe baja el recuento (N < M) y dice «apta por entradas: no»", bool(m) and int(m.group(1)) < int(m.group(2)) and "apta por entradas: no" in inf, m.group(0) if m else "")
paso("N", "(hito 2, H2) con una entrada menos: cada bloque de aptitud del informe (el de la V6.4 y la línea de las entradas) dice «apta por entradas: no» y «Apta para dinero real: no»; ninguno dice «sí»",
     aptitud_en_informe(inf, False) and bloques_aptitud(inf)[0] is not None and bloques_aptitud(inf)[1] is not None, bloques_aptitud(inf))
con()
subprocess.run([sys.executable, "-B", os.path.join(PV, "scripts", "ficha.py"), c, "--provisional"], capture_output=True, text=True, env=env)
subprocess.run([sys.executable, "-B", os.path.join(PV, "scripts", "informe.py"), c, "--provisional"], capture_output=True, text=True, env=env)
inf = open(os.path.join(c, "informe_provisional.md"), encoding="utf-8").read()
paso("N", "(hito 2, H2) con el registro apto: cada bloque de aptitud dice «apta por entradas: sí» y «Apta para dinero real: no»; ninguno dice «Apta para dinero real: sí»",
     aptitud_en_informe(inf, True) and bloques_aptitud(inf)[0] is not None and bloques_aptitud(inf)[1] is not None, bloques_aptitud(inf))
paso("N", "(N1/N2; tercera revisión, T7) con el registro apto, el informe da igualmente los «no aplicables»", "apta por entradas: sí" in inf and re.search(r"\d+ no aplicables", inf) is not None,
     (re.findall(r"Verificación de las entradas financieras:.{0,400}", inf) or [""])[0][:300])

n_ok = sum(x["resultado"] == "PASA" for x in RES)
print(f"{n_ok}/{len(RES)} pruebas de la corrección de la verificación de las entradas (4.15) PASAN")
print("RESULTADO verificación de las entradas 4.15: " + ("PASA" if n_ok == len(RES) else "FALLA"))
if ARGS.json:
    json.dump(RES, open(ARGS.json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
shutil.rmtree(TMP, ignore_errors=True)
sys.exit(0 if n_ok == len(RES) else 1)
