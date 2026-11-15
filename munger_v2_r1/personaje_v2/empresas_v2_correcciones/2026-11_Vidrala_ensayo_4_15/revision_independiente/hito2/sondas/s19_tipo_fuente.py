#!/usr/bin/env python3
"""s19 · U5 (tipo de la fuente por su contenido): «%PDF-» en los primeros 1024 bytes ya basta para tratar el archivo como PDF.
A) PDF con bytes previos, con y sin extensión (lo que se quería aceptar);  B) archivos que NO son PDF y contienen «%PDF-» en su primer
kilobyte: un HTML legítimo que menciona «%PDF-», y un texto conservado .txt cuya primera página lo menciona (¿rechazo falso?).
Arnés fx5; pdf_minimo es el de la cuarta pasada (pdfmin.py). pdftotext sí se usa (no es LibreOffice)."""
import hashlib, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fx5 as X
from pdfmin import pdf_minimo
VE, K, FS = X.VE, X.K, X.FS
f_k = X.ent(X.REG, K)["fuente"]
CITA = f_k["cita"]
paginas = list(X.paginas)
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()  # noqa: E731
SHA_TXT = sha(os.path.join(FS, "fuente.txt"))
print("código:", "hito 2" if hasattr(VE, "_cita_cifra") else "hito 1")


def probar(nombre, contenido, rotulo, como_texto=False):
    p = os.path.join(FS, nombre)
    open(p, "wb").write(contenido if isinstance(contenido, bytes) else contenido.encode("utf-8"))
    cambio = dict(archivo=f"fuentes_sinteticas/{nombre}", sha256=sha(p))
    if not como_texto:
        cambio.update(archivo_texto="fuentes_sinteticas/fuente.txt", sha256_texto=SHA_TXT)
    r = X.con(lambda g: X.ent(g, K)["fuente"].update(cambio), resellar=True)
    print(f"   {rotulo} ({nombre}; tipo: {VE._tipo_fuente(p)})\n      -> {'comprobada' if K in r['comprobadas'] else 'NO comprobada'} {'; '.join(x[:210] for x in X.con_k(r, K))}")


PDF = pdf_minimo(paginas)
BASURA = b"\x00\x01cabecera de un gestor documental\r\n" * 5
probar("a1.pdf", PDF, "A1 control: PDF fiel")
probar("a2_basura.bin", BASURA + PDF, "A2 PDF con bytes previos y extensión .bin")
probar("a3_basura", BASURA + PDF, "A3 PDF con bytes previos, sin extensión")
probar("a4_basura_larga.bin", b"x" * 1100 + PDF, "A4 PDF con 1100 bytes previos (la cabecera queda fuera del primer kilobyte), extensión .bin")
probar("b1_menciona.html", f"<!doctype html><html><head><title>Descarga del informe (%PDF-1.7, 3 MB)</title></head><body><p>{CITA}</p></body></html>", "B1 HTML legítimo con la cita visible que menciona «%PDF-» en su cabecera")
probar("b1_control.html", f"<!doctype html><html><head><title>Descarga del informe</title></head><body><p>{CITA}</p></body></html>", "B1' control: el mismo HTML sin «%PDF-»")
txt = open(os.path.join(FS, "fuente.txt"), encoding="utf-8").read()
probar("b2_fuente_con_mencion.txt", "[PDF PAGE 0]\nÍndice del documento. Formato original: %PDF-1.7\n" + txt, "B2 texto conservado .txt cuya primera página menciona «%PDF-» (la fuente citada es el propio .txt)", como_texto=True)
probar("b2_control.txt", "[PDF PAGE 0]\nÍndice del documento.\n" + txt, "B2' control: el mismo .txt sin la mención", como_texto=True)
X.limpiar()
