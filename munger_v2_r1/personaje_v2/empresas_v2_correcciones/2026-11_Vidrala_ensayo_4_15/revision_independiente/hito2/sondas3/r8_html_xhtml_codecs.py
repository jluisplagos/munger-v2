#!/usr/bin/env python3
"""r8 · N6 (tercera pasada): el modo XHTML y las codificaciones admitidas, candidata anterior (92b2362) frente a la tercera (f3d15e8).
A) ¿Cuándo se decide que un documento es XHTML? La tercera lo decide por el CONTENIDO (empieza por «<?xml» o lleva
   xmlns="http://www.w3.org/1999/xhtml" en sus primeros 4096 caracteres), no por la extensión ni por cómo lo abre un navegador: un archivo
   .html / .htm se analiza SIEMPRE con el analizador de HTML del navegador, aunque lleve ese xmlns (lo llevan los XHTML 1.0 servidos como
   text/html, los HTML exportados por Word y muchos informes): ahí «<div hidden/>» NO se cierra y oculta lo que sigue.
B) Codificaciones que ahora se admiten y que un navegador no reconoce (lista WHATWG): el control leería un texto distinto del que se ve.
Solo usa la parte HTML del código (como html_solo.py).  Uso: python3 -I -B r8_html_xhtml_codecs.py"""
import codecs, encodings.aliases, os, re, sys, tempfile, types, unicodedata
F = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def cargar(arbol):
    p = os.path.join(F, arbol, "munger_v2_r1", "personaje_v2", "scripts", "verificacion_entradas.py")
    src = open(p, encoding="utf-8").read()
    ns = {"re": re, "unicodedata": unicodedata, "os": os}
    exec(compile(src[src.index("HTML_SIN_TEXTO_VISIBLE = "):src.index("def _contiene_texto(")], p + "[HTML]", "exec"), ns)
    return types.SimpleNamespace(**{k: v for k, v in ns.items() if k.startswith("_") and not k.startswith("__")})


VE, VP = cargar(os.environ.get("ARBOL_VE", "copia")), cargar("prev")  # ARBOL_VE=prop: con las propuestas del revisor
TMP = tempfile.mkdtemp(prefix="rev3_html_", dir=os.path.join(F, "tmp"))
CITA = "Partida oculta: 849697.000"
n = [0]


def ver(M, nombre, contenido, ext=".html", binario=None):
    n[0] += 1
    p = os.path.join(TMP, f"c{n[0]}{ext}")
    open(p, "wb").write(binario if binario is not None else contenido.encode("utf-8"))
    e, t = M._texto_html_visible(p)
    return "pendiente" if e != "ok" else ("presente" if M._cmp_txt_espacios(CITA) in M._cmp_txt_espacios(t) else "ausente")


def fila(nombre, navegador, contenido, ext=".html", binario=None):
    a, b = ver(VP, nombre, contenido, ext, binario), ver(VE, nombre, contenido, ext, binario)
    marca = ""
    if navegador == "oculta" and b == "presente":
        marca = "   <<< SE ACEPTA un texto que el navegador no muestra" + (" (REGRESIÓN: la anterior lo rechazaba)" if a != "presente" else "")
    elif navegador == "visible" and b != "presente":
        marca = "   <<< se rechaza un texto que el navegador muestra" + (" (la anterior lo aceptaba)" if a == "presente" else "")
    print(f"   {nombre:112} archivo {ext:6} navegador: {navegador:8} anterior: {a:9} tercera: {b}{marca}")


XN = 'xmlns="http://www.w3.org/1999/xhtml"'
print("== A · modo XHTML decidido por el contenido")
fila("A1 .html con xmlns (XHTML 1.0 servido como HTML): <div hidden/> seguido del texto", "oculta", f"<!DOCTYPE html><html {XN}><body><div hidden/><p>{CITA}</p></body></html>")
fila("A2 .html con xmlns: <div style=\"display:none\"/> seguido del texto", "oculta", f"<html {XN}><body><div style=\"display:none\"/><p>{CITA}</p></body></html>")
fila("A3 .html con xmlns: <script src=x.js/> seguido del texto (en HTML el resto es contenido del script)", "oculta", f"<html {XN}><body><script src=\"x.js\"/><p>{CITA}</p></body></html>")
fila("A4 .html que empieza por <?xml …?> (un navegador lo trata como comentario): <div hidden/>", "oculta", f"<?xml version=\"1.0\" encoding=\"utf-8\"?><html><body><div hidden/><p>{CITA}</p></body></html>")
fila("A5 .html con xmlns: <textarea/> seguido del texto", "oculta", f"<html {XN}><body><textarea/><p>{CITA}</p></body></html>")
fila("A6 control: .html SIN xmlns: <div hidden/> (lo corrigió H7)", "oculta", f"<html><body><div hidden/><p>{CITA}</p></body></html>")
fila("A7 control: .xhtml con declaración XML y xmlns: <div hidden=\"hidden\"/> vacío (en XML se cierra)", "visible", f"<?xml version=\"1.0\"?><html {XN}><body><div hidden=\"hidden\"/><p>{CITA}</p></body></html>", ".xhtml")
fila("A8 .xhtml SIN declaración XML y con el xmlns entre comillas simples: <script src=x.js/>", "visible", f"<html xmlns='http://www.w3.org/1999/xhtml'><body><script src=\"x.js\"/><p>{CITA}</p></body></html>", ".xhtml")
fila("A9 .xhtml sin declaración y con el xmlns tras 5000 caracteres de DOCTYPE/comentario: <script src=x.js/>", "visible", f"<!--{'x' * 5000}--><html {XN}><body><script src=\"x.js\"/><p>{CITA}</p></body></html>", ".xhtml")
fila("A10 .html que menciona el xmlns en un comentario (no es XHTML): <div hidden/>", "oculta", f"<!-- convertido desde {XN} --><html><body><div hidden/><p>{CITA}</p></body></html>")
fila("A11 XHTML verdadero (.xhtml): elemento NO vacío oculto y bien cerrado (control: sigue oculto)", "oculta", f"<?xml version=\"1.0\"?><html {XN}><body><div style=\"display:none\"><p>{CITA}</p></div></body></html>", ".xhtml")

print("\n== B · codificaciones declaradas")
adm = lambda nombre: nombre.startswith(("utf-", "cp125", "cp4", "cp8", "iso8859-", "mac-", "koi8", "euc_", "iso2022_")) or nombre in ("shift_jis", "gb2312", "gbk", "gb18030", "big5", "big5hkscs")  # noqa: E731
ant = lambda nombre: nombre.startswith(("utf-", "cp125", "iso8859-", "mac-", "koi8")) or nombre in ("shift_jis", "euc_jp", "gb2312", "gbk", "gb18030", "big5")  # noqa: E731
def _nombre(x):
    try:
        return codecs.lookup(x).name
    except LookupError:
        return None


nombres = sorted({_nombre(x) for x in set(encodings.aliases.aliases.values())} - {None})
nuevos = [x for x in nombres if adm(x) and not ant(x) and x not in ("latin-1", "iso8859-1", "ascii", "utf-7")]
WHATWG = {"cp866", "cp874", "euc_kr", "euc_jp", "iso2022_jp"}
print(f"   códecs de Python que la tercera admite y la anterior no: {len(nuevos)}")
print("      en la lista WHATWG (los navegadores los leen):", [x for x in nuevos if x in WHATWG])
print("      fuera de la lista WHATWG:", [x for x in nuevos if x not in WHATWG])
def _no_ascii(x):
    try:
        return "A<p>".encode(x) != b"A<p>"
    except Exception:  # noqa: BLE001
        return True


ebc = [x for x in nuevos if _no_ascii(x)]
print("      de ellos, no compatibles con ASCII (EBCDIC: los bytes ASCII del documento no son su texto):", ebc)
# un documento que declara cp875 (EBCDIC): el navegador no reconoce la etiqueta y lo muestra como texto ilegible; el control «lee» la cita
oculto = CITA.encode("cp875")
doc = b'<meta charset="cp875">' + oculto
fila("B1 declara charset=cp875 (EBCDIC; no existe para un navegador) y la cita va codificada en EBCDIC", "oculta", "", ".html", doc)
doc2 = b'<html><head><meta charset="ibm850"></head><body><p>' + CITA.encode("cp850") + b"</p></body></html>"
fila("B2 declara charset=ibm850 (no está en la lista WHATWG; ASCII compatible: el texto se ve igual)", "visible", "", ".html", doc2)
doc3 = b'<html><head><meta charset="iso-2022-kr"></head><body><p>' + CITA.encode("ascii") + b"</p></body></html>"
fila("B3 declara charset=iso-2022-kr (WHATWG: codificación de sustitución: el navegador no muestra el contenido)", "oculta", "", ".html", doc3)
