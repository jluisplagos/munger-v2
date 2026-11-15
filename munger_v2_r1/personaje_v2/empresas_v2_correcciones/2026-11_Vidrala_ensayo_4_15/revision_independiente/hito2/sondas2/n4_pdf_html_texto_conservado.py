#!/usr/bin/env python3
"""n4 · H1 (segunda pasada), vía PDF y HTML: cuando la fuente conservada es un PDF o un HTML con su «archivo_texto», ¿dónde se leen la
cifra y su signo? Registro sintético completo (arnés fx5 de la primera pasada). La fuente (PDF o HTML) publica la cifra en negativo o
con un dígito más; el texto conservado (archivo_texto) no lleva la marca (p. ej. un OCR o un extractor que pierde los paréntesis) y la cita
es la del texto conservado, recortada a la cifra o al rótulo. pdftotext sí se usa (no es LibreOffice).
Uso: python3 -I -B n4_pdf_html_texto_conservado.py   (PV=<cand>/personaje_v2 para la candidata de la primera pasada)"""
import hashlib, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sondas"))
import fx5 as X
from pdfmin import pdf_minimo
VE, K, FS = X.VE, X.K, X.FS
print("código:", "estable" if hasattr(VE, "_apariciones_en_pagina") else "candidata (1.ª pasada)")
VF = X.ent(X.REG, K)["fuente"]["valor_fuente"]
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()  # noqa: E731
r0 = X.con()
print("control positivo:", X.resumen(r0, K)[:80])
N = [0]


def caso(nombre, texto_fuente, texto_conservado, cita, tipo, vf=VF, signo=1, tratamiento="ninguno", espera="rechazo"):
    N[0] += 1
    pg = X.nueva_pagina(texto_conservado)  # página nueva del texto conservado (fuente.txt), con su sha y vínculos
    n = int(pg)
    if tipo == "pdf":
        pags = list(X.paginas)
        pags[n - 1] = texto_fuente
        nombre_f = f"n4_{N[0]}.pdf"
        open(os.path.join(FS, nombre_f), "wb").write(pdf_minimo(pags))
    else:
        nombre_f = f"n4_{N[0]}.html"
        open(os.path.join(FS, nombre_f), "w", encoding="utf-8").write(f"<!doctype html><html><head><meta charset='utf-8'><title>t</title></head><body><table><tr><td>{texto_fuente}</td></tr></table></body></html>")
    cambio = dict(archivo=f"fuentes_sinteticas/{nombre_f}", sha256=sha(os.path.join(FS, nombre_f)), archivo_texto="fuentes_sinteticas/fuente.txt",
                  sha256_texto=sha(os.path.join(FS, "fuente.txt")), pagina=pg, cita=cita, valor_fuente=vf, signo=signo, tratamiento=tratamiento)
    r = X.con(lambda g: X.ent(g, K)["fuente"].update(cambio), resellar=True)
    ok = K in r["comprobadas"]
    marca = "" if (ok and espera == "ok") or (not ok and espera == "rechazo") else ("   <<< ACEPTADA: la fuente no publica eso" if ok else "   <<< rechazo falso")
    print(f"   {nombre}\n      fuente ({tipo}): {texto_fuente!r}\n      texto conservado: {texto_conservado!r} · cita: {cita!r} · valor_fuente {vf} signo {signo}\n"
          f"      -> {'comprobada' if ok else 'NO comprobada'} {'; '.join(x[:150] for x in X.con_k(r, K))}{marca}")


L = f"Partida sintética de {K}"
caso("1 control: PDF y texto conservado iguales (negativo declarado)", f"{L}: ({VF:,.3f})", f"{L}: ({VF:,.3f})", f"{L}: ({VF:,.3f})", "pdf", vf=-VF, signo=-1, tratamiento="pago publicado entre paréntesis", espera="ok")
caso("2 PDF «(849,697.000)»; el texto conservado perdió los paréntesis; cita = la cifra", f"{L}: ({VF:,.3f})", f"{L}: {VF:,.3f}", f"{VF:,.3f}", "pdf")
caso("3 PDF «-849697.000»; texto conservado sin el menos; cita = la cifra", f"{L}: -{VF:.3f}", f"{L}: {VF:.3f}", f"{VF:.3f}", "pdf")
caso("4 PDF «8496970»; el texto conservado dice «849697»; cita = rótulo y cifra del texto conservado", f"{L}: {VF * 10:.0f}", f"{L}: {VF:.0f}", f"{L}: {VF:.0f}", "pdf")
caso("5 control: lo mismo que 2 con la cita completa del texto conservado (no está en el PDF)", f"{L}: ({VF:,.3f})", f"{L}: {VF:,.3f}", f"{L}: {VF:,.3f}", "pdf")
caso("6 HTML «(849,697.000)» visible; texto conservado sin paréntesis; cita = la cifra", f"{L}: ({VF:,.3f})", f"{L}: {VF:,.3f}", f"{VF:,.3f}", "html")
caso("7 HTML «-849697.000»; texto conservado sin el menos; cita = la cifra", f"{L}: -{VF:.3f}", f"{L}: {VF:.3f}", f"{VF:.3f}", "html")
caso("8 HTML «1849697.000»; texto conservado «849697.000»; cita = la cifra", f"{L}: 1{VF:.3f}", f"{L}: {VF:.3f}", f"{VF:.3f}", "html")
r = X.con()
print("control positivo al final:", X.resumen(r, K)[:80])
X.limpiar()
