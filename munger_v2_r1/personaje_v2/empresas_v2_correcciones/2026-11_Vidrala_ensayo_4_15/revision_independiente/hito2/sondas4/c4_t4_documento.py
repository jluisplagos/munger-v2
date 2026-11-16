#!/usr/bin/env python3
"""c4 · T4 (cuarta comprobación): la lectura de la cifra en el documento (PDF o HTML) cuando la cita no se localiza en él con sus palabras.
Registro completo (fixture de la batería, como r4b). Además de los casos de r4b (palabra partida, guion blando), diferencias tipográficas
LEGÍTIMAS entre el texto conservado y el documento: ¿cuáles dejan ahora pendiente una entrada cuyo documento publica la cifra tal como se
cita? ¿Y alguna sigue dejando pasar un signo contrario?
PV=<prev>/personaje_v2 para la candidata anterior.  Uso: python3 -I -B c4_t4_documento.py"""
import hashlib, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sondas"))
import fx5 as X
from pdfmin import pdf_minimo
VE, K = X.VE, X.K
print("código:", "cuarta (7a6583b)" if "CODECS_TEXTO_HTML" in open(VE.__file__, encoding="utf-8").read() else "anterior (f3d15e8, 3.ª comprobación)")
print("control positivo:", X.resumen(X.con())[:80])
VF = X.ent(X.REG, K)["fuente"]["valor_fuente"]
FS, N = X.FS, [0]
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()  # noqa: E731
RES = []


def caso(nombre, tipo, doc, linea_txt, cita, vf, espera, ext=None):
    """doc: el contenido del documento (una página de PDF o el cuerpo del HTML); linea_txt: la línea del texto conservado; espera: «comprobada» o «NO comprobada»."""
    N[0] += 1
    n = X.nueva_pagina(linea_txt)
    nombre_f = f"c4_{N[0]}." + (ext or tipo)
    if tipo == "pdf":
        open(os.path.join(FS, nombre_f), "wb").write(pdf_minimo(["relleno"] * (int(n) - 1) + [doc]))
    else:
        open(os.path.join(FS, nombre_f), "w", encoding="utf-8").write(f"<html><head><meta charset='utf-8'></head><body>{doc}</body></html>")
    s, st = sha(os.path.join(FS, nombre_f)), sha(os.path.join(FS, "fuente.txt"))
    r = X.con(lambda g: X.ent(g, K)["fuente"].update(archivo=f"fuentes_sinteticas/{nombre_f}", sha256=s, archivo_texto="fuentes_sinteticas/fuente.txt", sha256_texto=st, pagina=n, cita=cita,
                                                    valor_fuente=vf), resellar=True)
    ok = K in r["comprobadas"]
    real = "comprobada" if ok else "NO comprobada"
    cat = next((c for c in ("discrepancias", "pendientes", "errores", "desactualizadas") if any(x.startswith(K) or K in x for x in r.get(c, []))), "")
    marca = "" if real == espera else ("   <<< COMPROBADA y no debería" if ok else "   <<< no se comprueba una entrada cuyo documento publica la cifra como se cita")
    if tipo == "pdf":
        vis = [VE._texto_pdf(os.path.join(FS, nombre_f), int(n), layout=lay)[1].strip() for lay in (True, False)]
    else:
        vis = [VE._texto_html_visible(os.path.join(FS, nombre_f))[1].strip()]
    lect = [VE._cita_cifra(cita, vf, t)[0] for t in vis]
    RES.append((nombre.split(" ")[0], real, cat))
    print(f"   {nombre}\n      documento ({tipo}): {doc!r}\n      texto conservado: {linea_txt!r} · cita: {cita!r} · valor_fuente {vf!r}\n      lectura de la cita en el texto del documento: {lect}"
          f"\n      -> {real}" + (f" ({cat})" if cat else "") + " " + "; ".join(X.con_k(r, K))[:230] + marca)


R, c = f"Partida sintetica de {K}", f"{VF:.3f}"
P = lambda x: f"<p>{x}</p>"  # noqa: E731
print("== A · el documento publica la cifra EN POSITIVO, como la cita (se espera «comprobada»)")
caso("A1 control: HTML idéntico al texto conservado", "html", P(f"{R}: {c} total"), f"{R}: {c} total", f"{c} total", VF, "comprobada")
caso("A2 HTML con espacio de no separación entre las palabras de la cita", "html", P(f"{R}: {c}&nbsp;total"), f"{R}: {c} total", f"{c} total", VF, "comprobada")
caso("A3 HTML con un espacio largo (&emsp;)", "html", P(f"{R}: {c}&emsp;total"), f"{R}: {c} total", f"{c} total", VF, "comprobada")
caso("A4 HTML con una etiqueta en línea dentro de una palabra de la cita (<b>to</b>tal)", "html", P(f"{R}: {c} <b>to</b>tal"), f"{R}: {c} total", f"{c} total", VF, "comprobada")
caso("A5 HTML con <br> entre las palabras de la cita", "html", P(f"{R}: {c}<br>total"), f"{R}: {c} total", f"{c} total", VF, "comprobada")
caso("A6 HTML con la cifra y el rótulo en celdas contiguas", "html", f"<table><tr><td>{R}:</td><td>{c}</td><td>total</td></tr></table>", f"{R}: {c} total", f"{c} total", VF, "comprobada")
caso("A7 HTML con una ligadura tipográfica en una palabra de la cita («beneﬁcio»); el texto conservado dice «beneficio»", "html", P(f"{R}: {c} beneﬁcio"), f"{R}: {c} beneficio", f"{c} beneficio", VF, "comprobada")
caso("A8 HTML con un guion blando en una palabra de la cita (to&shy;tal), cifra positiva", "html", P(f"{R}: {c} to&shy;tal"), f"{R}: {c} total", f"{c} total", VF, "comprobada")
caso("A9 HTML con un guion blando DENTRO de la cifra", "html", P(f"{R}: {c[:3]}&shy;{c[3:]} total"), f"{R}: {c} total", f"{c} total", VF, "comprobada")
caso("A10 PDF con las palabras de la cita en dos líneas", "pdf", f"{R}: {c}\ntotal del ejercicio", f"{R}: {c} total del ejercicio", f"{c} total del", VF, "comprobada")
caso("A11 PDF con una palabra de la cita partida («to tal»): r4b 6", "pdf", f"{R}: {c} to tal", f"{R}: {c} total", f"{c} total", VF, "comprobada")
caso("A12 PDF con los miles de la cifra separados por un espacio y el texto conservado sin él", "pdf", f"{R}: {c[:3]} {c[3:]} total", f"{R}: {c} total", f"{c} total", VF, "comprobada")
caso("A13 la cita es solo la cifra y el PDF la lleva pegada al rótulo («…F6:849697.000»)", "pdf", f"{R}:{c} total", f"{R}: {c} total", f"{c}", VF, "comprobada")
print("== B · el documento publica la cifra EN NEGATIVO y el texto conservado perdió el signo (se espera «NO comprobada»)")
caso("B1 HTML con ligadura en una palabra de la cita y la cifra con menos", "html", P(f"{R}: -{c} beneﬁcio"), f"{R}: {c} beneficio", f"{c} beneficio", VF, "NO comprobada")
caso("B2 HTML con &minus; y espacio de no separación", "html", P(f"{R}: &minus;{c}&nbsp;total"), f"{R}: {c} total", f"{c} total", VF, "NO comprobada")
caso("B3 HTML con el paréntesis en celdas aparte", "html", f"<table><tr><td>{R}:</td><td>(</td><td>{c}</td><td>)</td><td>total</td></tr></table>", f"{R}: {c} total", f"{c} total", VF, "NO comprobada")
caso("B4 HTML con un guion blando dentro de la cifra y menos delante", "html", P(f"{R}: -{c[:3]}&shy;{c[3:]} total"), f"{R}: {c} total", f"{c} total", VF, "NO comprobada")
caso("B5 PDF con los miles separados por un espacio y menos delante", "pdf", f"{R}: -{c[:3]} {c[3:]} total", f"{R}: {c} total", f"{c} total", VF, "NO comprobada")
caso("B6 la cita es solo la cifra; el PDF la lleva pegada al rótulo con menos («…F6:-849697.000»)", "pdf", f"{R}:-{c} total", f"{R}: {c} total", f"{c}", VF, "NO comprobada")
caso("B7 HTML con la cifra negativa en una palabra de la cita cortada («Subtotal» citado «total»)", "html", P(f"Subtotal -{c}") , f"total {c}", f"total {c}", VF, "NO comprobada")
print("control positivo al final:", X.resumen(X.con())[:80])
print("RESUMEN:", " · ".join(f"{a}: {b}" + (f" ({c_})" if c_ else "") for a, b, c_ in RES))
X.limpiar()
