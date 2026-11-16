#!/usr/bin/env python3
"""r4b · N3 (tercera pasada), residuo: la lectura en el documento solo se hace si la cita se LOCALIZA en el texto del documento con sus
palabras separadas igual (_apariciones_en_pagina); si no se localiza («no_localizada»), se ignora y manda el texto conservado. Pero el
control que exige que la cita esté en el documento compara SIN espacios (PDF: _cmp_txt) o sin guiones blandos ni caracteres de ancho cero
(HTML: _cmp_txt_espacios). Una diferencia tipográfica entre el texto conservado y el del documento en una palabra de la cita (una palabra
partida, un guion blando) deja pasar la cita y, a la vez, impide la lectura del signo en el documento.
Registro completo (fixture de la batería). PV=<prev>/personaje_v2 para la candidata anterior.  Uso: python3 -I -B r4b_n3_no_localizada.py"""
import hashlib, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sondas"))
import fx5 as X
from pdfmin import pdf_minimo
VE, K = X.VE, X.K
print("código:", "tercera (f3d15e8)" if "textos_fuente" in open(VE.__file__, encoding="utf-8").read() else "anterior (92b2362, 2.ª pasada)")
print("control positivo:", X.resumen(X.con())[:80])
VF = X.ent(X.REG, K)["fuente"]["valor_fuente"]
FS, N = X.FS, [0]
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()  # noqa: E731


def caso(nombre, tipo, doc, linea_txt, cita, vf, espera):
    N[0] += 1
    n = X.nueva_pagina(linea_txt)
    nombre_f = f"r4b_{N[0]}." + tipo
    if tipo == "pdf":
        open(os.path.join(FS, nombre_f), "wb").write(pdf_minimo(["relleno"] * (int(n) - 1) + [doc]))
    else:
        open(os.path.join(FS, nombre_f), "w", encoding="utf-8").write(f"<html><head><meta charset='utf-8'></head><body><p>{doc}</p></body></html>")
    s, st = sha(os.path.join(FS, nombre_f)), sha(os.path.join(FS, "fuente.txt"))
    r = X.con(lambda g: X.ent(g, K)["fuente"].update(archivo=f"fuentes_sinteticas/{nombre_f}", sha256=s, archivo_texto="fuentes_sinteticas/fuente.txt", sha256_texto=st, pagina=n, cita=cita,
                                                    valor_fuente=vf), resellar=True)
    ok = K in r["comprobadas"]
    real = "comprobada" if ok else "NO comprobada"
    marca = "" if real == espera else ("   <<< COMPROBADA: el documento publica la cifra en negativo" if ok else "   <<< rechazo")
    if tipo == "pdf":
        vis = [VE._texto_pdf(os.path.join(FS, nombre_f), int(n), layout=lay)[1].strip() for lay in (True, False)]
    else:
        vis = [VE._texto_html_visible(os.path.join(FS, nombre_f))[1].strip()]
    lect = [VE._cita_cifra(cita, vf, t)[0] for t in vis]
    print(f"   {nombre}\n      documento ({tipo}): {doc!r}\n      texto conservado: {linea_txt!r} · cita: {cita!r} · valor_fuente {vf!r}\n      texto del documento: {vis} · lectura de la cita en él: {lect}"
          f"\n      -> {real} " + "; ".join(X.con_k(r, K))[:260] + marca)


R, c = f"Partida sintetica de {K}", f"{VF:.3f}"
caso("1 control: PDF «-c total»; texto conservado sin el menos; cita «c total» (se localiza: lo detecta N3)", "pdf", f"{R}: -{c} total", f"{R}: {c} total", f"{c} total", VF, "NO comprobada")
caso("2 PDF con una palabra de la cita PARTIDA en el texto del PDF («to tal»); texto conservado «total» sin el menos", "pdf", f"{R}: -{c} to tal", f"{R}: {c} total", f"{c} total", VF, "NO comprobada")
caso("3 PDF con dos palabras de la cita JUNTAS en el texto del PDF («totaldel ejercicio»)", "pdf", f"{R}: -{c} totaldel ejercicio", f"{R}: {c} total del ejercicio", f"{c} total del", VF, "NO comprobada")
caso("4 HTML con un guion blando en una palabra de la cita («to&shy;tal»); texto conservado sin el menos", "html", f"{R}: -{c} to&shy;tal", f"{R}: {c} total", f"{c} total", VF, "NO comprobada")
caso("5 HTML con un espacio de ancho cero en una palabra de la cita", "html", f"{R}: -{c} to&#8203;tal", f"{R}: {c} total", f"{c} total", VF, "NO comprobada")
caso("6 control: lo mismo que 2 con el PDF en positivo (legítimo: la palabra partida no debería impedir la comprobación)", "pdf", f"{R}: {c} to tal", f"{R}: {c} total", f"{c} total", VF, "comprobada")
print("control positivo al final:", X.resumen(X.con())[:80])
X.limpiar()
