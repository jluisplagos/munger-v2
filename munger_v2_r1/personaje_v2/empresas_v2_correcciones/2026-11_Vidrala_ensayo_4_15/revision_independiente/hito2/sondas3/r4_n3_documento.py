#!/usr/bin/env python3
"""r4 · N3 (tercera pasada): la lectura adicional de la cifra y su signo en el PDF o el HTML, en el registro completo (fixture de la batería).
¿Qué pasa cuando el texto conservado y el texto del documento difieren de forma LEGÍTIMA (columnas, celdas, llamadas de nota)?
A) PDF: guion de cero de la columna anterior («…   -   849697.000»): el texto conservado y «pdftotext -layout» conservan las columnas;
   «pdftotext» sin layout las junta con un espacio.  B) HTML: celdas contiguas (el texto visible las separa con UN espacio).
C) residuo de N3: el documento publica el negativo y el texto conservado no, con citas de varias palabras.
D) el mensaje cuando la discrepancia está en el documento.
PV=<prev>/personaje_v2 para la candidata anterior.  Uso: python3 -I -B r4_n3_documento.py"""
import hashlib, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sondas"))
import fx5 as X
from pdfmin import pdf_minimo
VE, K = X.VE, X.K
print("código:", "tercera (f3d15e8)" if "textos_fuente" in open(VE.__file__, encoding="utf-8").read() else "anterior (92b2362, 2.ª pasada)")
print("control positivo:", X.resumen(X.con())[:80])
VF = X.ent(X.REG, K)["fuente"]["valor_fuente"]
FS = X.FS
N = [0]


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def caso(nombre, tipo, linea_doc, linea_txt, cita, vf, signo=1, espera="comprobada", html=None):
    """La fuente es un PDF (una página con linea_doc) o un HTML; el texto conservado es linea_txt en una página nueva del .txt sintético."""
    N[0] += 1
    n = X.nueva_pagina(linea_txt)
    if tipo == "pdf":
        nombre_f = f"r4_{N[0]}.pdf"
        open(os.path.join(FS, nombre_f), "wb").write(pdf_minimo(["relleno"] * (int(n) - 1) + [linea_doc]))
    else:
        nombre_f = f"r4_{N[0]}.html"
        open(os.path.join(FS, nombre_f), "w", encoding="utf-8").write(html or f"<html><head><meta charset='utf-8'></head><body>{linea_doc}</body></html>")
    s, st = sha(os.path.join(FS, nombre_f)), sha(os.path.join(FS, "fuente.txt"))

    def cambio(g):
        e = X.ent(g, K)
        e["fuente"].update(archivo=f"fuentes_sinteticas/{nombre_f}", sha256=s, archivo_texto="fuentes_sinteticas/fuente.txt", sha256_texto=st, pagina=n, cita=cita, valor_fuente=vf,
                           signo=signo, tratamiento="ninguno" if signo == 1 else "pago publicado entre paréntesis")
    r = X.con(cambio, resellar=True)
    ok = K in r["comprobadas"]
    real = "comprobada" if ok else "NO comprobada"
    marca = "" if (real == espera) else ("   <<< COMPROBADA: el documento no publica eso" if ok else "   <<< rechazo de una entrada legítima")
    print(f"   {nombre}\n      documento ({tipo}): {linea_doc!r}\n      texto conservado: {linea_txt!r}\n      cita: {cita!r} · valor_fuente {vf!r} signo {signo}")
    if tipo == "pdf":
        for lay in (True, False):
            t = VE._texto_pdf(os.path.join(FS, nombre_f), int(n), layout=lay)[1]
            print(f"      pdftotext {'-layout' if lay else 'sin layout'}: {t.strip()!r}")
    else:
        print(f"      texto visible del HTML: {VE._texto_html_visible(os.path.join(FS, nombre_f))[1].strip()!r}")
    print(f"      -> {real} " + "; ".join(X.con_k(r, K))[:300] + marca)


R = f"Partida sintetica de {K}"
c = f"{VF:.3f}"
print("\n== A · PDF: columnas")
caso("A1 control: PDF y texto conservado iguales, sin guion", "pdf", f"{R}: {c}", f"{R}: {c}", f"{R}: {c}", VF)
caso("A2 guion de cero en la columna anterior (2+ espacios en el PDF y en el texto conservado); cita con los espacios normalizados",
     "pdf", f"{R}        -        {c}", f"{R}        -        {c}", f"{R} - {c}", VF)
caso("A3 lo mismo, la cita es solo la cifra", "pdf", f"{R}        -        {c}", f"{R}        -        {c}", c, VF)
caso("A4 dos columnas de cifras: la segunda tras un negativo entre paréntesis", "pdf", f"{R}     (12.5)     {c}", f"{R}     (12.5)     {c}", f"{R} (12.5) {c}", VF)
caso("A5 negativo publicado entre paréntesis en una tabla con guion delante", "pdf", f"{R}        -        ({c})", f"{R}        -        ({c})", f"{R} - ({c})", -VF, signo=-1)

for esp in (2, 3, 4, 5):
    hueco = " " * esp
    caso(f"A6.{esp} guion de cero separado por {esp} espacios en el PDF (el texto conservado es el de «pdftotext -layout»: columnas estrechas)", "pdf",
         f"{R}{hueco}-{hueco}{c}", VE._texto_pdf_de_linea(f"{R}{hueco}-{hueco}{c}") if hasattr(VE, "_texto_pdf_de_linea") else f"{R}{hueco}-{hueco}{c}", f"{R} - {c}", VF)
print("\n== B · HTML: celdas contiguas (el texto visible separa las celdas con un solo espacio)")
tabla = lambda celdas: "<table><tr>" + "".join(f"<td>{x}</td>" for x in celdas) + "</tr></table>"  # noqa: E731
caso("B1 control: HTML con la cifra en una celda, sin guion", "html", tabla([R, c]), f"{R}        {c}", f"{R} {c}", VF)
caso("B2 celda con el guion del cero antes de la celda de la cifra", "html", tabla([R, "-", c]), f"{R}        -        {c}", f"{R} - {c}", VF)
caso("B3 lo mismo, la cita es solo la cifra", "html", tabla([R, "-", c]), f"{R}        -        {c}", c, VF)
caso("B4 negativo con los paréntesis en celdas aparte (frecuente en HTML de informes): «(», cifra, «)»", "html", tabla([R, "(", c, ")"]), f"{R}        ({c})", f"({c})", -VF, signo=-1)
caso("B5 celda con «—» (raya) antes de la cifra", "html", tabla([R, "—", c]), f"{R}        —        {c}", f"{R} — {c}", VF)
caso("B6 símbolo de moneda en su celda y guion antes", "html", tabla([R, "-", "€", c]), f"{R}     -     € {c}", f"{R} - € {c}", VF)

print("\n== C · residuo de N3: el documento publica el negativo, el texto conservado no, y la cita no es solo la cifra")
caso("C1 PDF «(c) 100.0»; texto conservado sin paréntesis; cita «cifra 100.0» (la cifra y la columna siguiente)", "pdf", f"{R}: ({c}) 100.0", f"{R}: {c} 100.0", f"{c} 100.0", VF, espera="NO comprobada")
caso("C2 PDF «-c»; texto conservado sin el menos; cita de varias palabras que empieza en la cifra", "pdf", f"{R}: -{c} total del ejercicio", f"{R}: {c} total del ejercicio", f"{c} total del ejercicio", VF, espera="NO comprobada")
caso("C3 HTML «-c» en una celda; texto conservado sin el menos; cita = la cifra y la celda siguiente", "html", tabla([R, "-" + c, "100.0"]), f"{R} {c} 100.0", f"{c} 100.0", VF, espera="NO comprobada")
caso("C4 PDF con una raya corta como signo menos («–c», U+2013); texto conservado sin ella; cita = la cifra", "pdf", f"{R}: {chr(0x2013)}{c}", f"{R}: {c}", c, VF, espera="NO comprobada")
caso("C5 PDF «c-» (menos detrás, estilo SAP); texto conservado sin él; cita = la cifra", "pdf", f"{R}: {c}-", f"{R}: {c}", c, VF, espera="NO comprobada")
caso("C6 PDF en el que la cifra es otra (un dígito más: «…0001»); texto conservado y cita con la cifra corta", "pdf", f"{R}: {c}1", f"{R}: {c}", f"{R}: {c}", VF, espera="NO comprobada")

print("\ncontrol positivo al final:", X.resumen(X.con())[:80])
X.limpiar()
