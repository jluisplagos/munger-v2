#!/usr/bin/env python3
"""c3 · T3 (cuarta comprobación): el modo XHTML por la extensión y la lista explícita de codificaciones, candidata anterior (f3d15e8) →
cuarta (7a6583b).
A) el modo XHTML: extensiones (.xhtml, .XHTML, .xht, .htm, sin extensión) y qué tipo de fuente da _tipo_fuente; un .xhtml mal formado.
B) codificaciones: para TODOS los nombres y alias de códecs de Python, qué hace _decodificar_html con un documento que declara ese charset
   (admitido o pendiente) con los dos códigos; lo admitido se compara con la lista WHATWG (lo que lee un navegador).
C) ISO-8859-9 e ISO-8859-11: un navegador los lee como windows-1254 y windows-874 (WHATWG); Python, no: un guion de la zona 0x80–0x9F.
Uso: python3 -I -B c3_xhtml_codecs.py"""
import codecs, encodings.aliases, os, pkgutil, sys, tempfile
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sondas3"))
import importlib.util, types  # noqa: E402
if importlib.util.find_spec("lxml") is None:
    # Python 3.11 y 3.12 de esta máquina no tienen lxml (lo usa v63_xml, que aquí no hace falta): se sustituye entradas_economicas por un módulo vacío
    sys.modules["entradas_economicas"] = types.ModuleType("entradas_economicas")
from comun3 import VE, VP, ACT, ANT, F  # noqa: E402

print(f"VE = {ACT} · VP = {ANT} · Python {sys.version.split()[0]}")
TMP = tempfile.mkdtemp(prefix="rev4_c3_", dir=os.path.join(F, "tmp"))
CITA = "Partida oculta: 849697.000"
n = [0]


def ver(M, contenido, ext, binario=None):
    """Lo que hace el control con la fuente: «pendiente» si _tipo_fuente no la da por HTML o no se puede leer; si no, si el texto está en lo visible."""
    n[0] += 1
    p = os.path.join(TMP, f"c{n[0]}{ext}")
    open(p, "wb").write(binario if binario is not None else contenido.encode("utf-8"))
    tipo = M._tipo_fuente(p)
    e, t = M._texto_html_visible(p)
    r = "pendiente" if e != "ok" else ("presente" if M._cmp_txt_espacios(CITA) in M._cmp_txt_espacios(t) else "ausente")
    return (r if tipo == "html" else f"pendiente (tipo «{tipo}»; visible: {r})"), tipo


def fila(nombre, navegador, contenido, ext=".html", binario=None):
    (a, _), (b, tipo) = ver(VP, contenido, ext, binario), ver(VE, contenido, ext, binario)
    marca = ""
    if navegador == "oculta" and b == "presente":
        marca = "   <<< SE ACEPTA un texto que el navegador no muestra" + (" (la anterior lo rechazaba)" if a != "presente" else " (igual que la anterior)")
    elif navegador == "visible" and b != "presente":
        marca = "   <<< no se acepta un texto que el navegador muestra" + (" (la anterior lo aceptaba)" if a == "presente" else " (igual que la anterior)")
    print(f"   {nombre:108} {ext or '(sin ext.)':10} navegador: {navegador:8} anterior: {a:9} cuarta: {b}{marca}")


XN = 'xmlns="http://www.w3.org/1999/xhtml"'
X1 = '<?xml version="1.0" encoding="utf-8"?>'
print("== A · modo XHTML por la extensión (si _tipo_fuente no da «html», contraste_pagina deja la entrada pendiente)")
fila("A1 .xhtml con <div hidden=\"hidden\"/> vacío (en XML se cierra): lo que sigue se ve", "visible", f"{X1}<html {XN}><body><div hidden=\"hidden\"/><p>{CITA}</p></body></html>", ".xhtml")
fila("A2 .XHTML (mayúsculas), lo mismo", "visible", f"{X1}<html {XN}><body><div hidden=\"hidden\"/><p>{CITA}</p></body></html>", ".XHTML")
fila("A3 .xht que empieza por <?xml …?> (lo habitual): ¿es una fuente HTML?", "visible", f"{X1}<html {XN}><body><div hidden=\"hidden\"/><p>{CITA}</p></body></html>", ".xht")
fila("A4 .xht que empieza por <html …>", "visible", f"<html {XN}><body><div hidden=\"hidden\"/><p>{CITA}</p></body></html>", ".xht")
fila("A5 .htm con el xmlns y <div hidden/>: es HTML, oculta lo que sigue", "oculta", f"<html {XN}><body><div hidden/><p>{CITA}</p></body></html>", ".htm")
fila("A6 sin extensión, empieza por <html y lleva el xmlns: <div hidden/>", "oculta", f"<html {XN}><body><div hidden/><p>{CITA}</p></body></html>", "")
fila("A7 .xhtml: elemento NO vacío oculto y bien cerrado (sigue oculto)", "oculta", f"{X1}<html {XN}><body><div hidden=\"hidden\"><p>{CITA}</p></div></body></html>", ".xhtml")
fila("A8 .xhtml: <script>…</script> con el texto dentro (sigue oculto)", "oculta", f"{X1}<html {XN}><body><script>var x = \"{CITA}\";</script><p>otro</p></body></html>", ".xhtml")
fila("A9 .xhtml: <head/> y <title/> autocerrados y el texto en el cuerpo", "visible", f"{X1}<html {XN}><head/><body><p>{CITA}</p></body></html>", ".xhtml")
fila("A10 .xhtml con una etiqueta con prefijo del espacio de nombres XHTML y hidden: <h:div hidden=\"hidden\">texto</h:div>", "oculta",
     f"{X1}<h:html xmlns:h=\"http://www.w3.org/1999/xhtml\"><h:body><h:div hidden=\"hidden\"><h:p>{CITA}</h:p></h:div></h:body></h:html>", ".xhtml")
fila("A11 .xhtml MAL FORMADO (un <br> sin cerrar antes del texto): un navegador da error de XML y no muestra lo que sigue", "oculta",
     f"{X1}<html {XN}><body><p>visible</p><br><p>{CITA}</p></body></html>", ".xhtml")
fila("A12 .xhtml con el texto en una sección CDATA (en XML es texto visible)", "visible", f"{X1}<html {XN}><body><p><![CDATA[{CITA}]]></p></body></html>", ".xhtml")
fila("A13 .html con una sección CDATA (en HTML es un comentario: no se ve)", "oculta", f"<html><body><p><![CDATA[{CITA}]]></p></body></html>", ".html")

print("\n== B · codificaciones declaradas (<meta charset=…> y contenido ASCII): admitidas por _decodificar_html")
# lista WHATWG (Encoding Standard): nombre canónico de Python de cada codificación que un navegador decodifica
WHATWG = {"utf-8", "cp866", "iso8859-2", "iso8859-3", "iso8859-4", "iso8859-5", "iso8859-6", "iso8859-7", "iso8859-8", "iso8859-10", "iso8859-13", "iso8859-14",
          "iso8859-15", "iso8859-16", "koi8-r", "koi8-u", "mac-roman", "cp874", "cp1250", "cp1251", "cp1252", "cp1253", "cp1254", "cp1255", "cp1256", "cp1257", "cp1258",
          "mac-cyrillic", "gbk", "gb18030", "big5", "euc_jp", "iso2022_jp", "shift_jis", "euc_kr", "utf-16-be", "utf-16-le", "utf-16"}
# etiquetas que WHATWG asigna a OTRA codificación que la de Python con ese nombre
WHATWG_OTRA = {"latin-1": "windows-1252", "iso8859-1": "windows-1252", "ascii": "windows-1252", "iso8859-9": "windows-1254", "iso8859-11": "windows-874", "tis-620": "windows-874",
               "gb2312": "GBK", "big5hkscs": "Big5", "cp949": "EUC-KR"}
etiquetas = set(encodings.aliases.aliases) | set(encodings.aliases.aliases.values()) | {m.name for m in pkgutil.iter_modules(encodings.__path__)}
canon = {}
for e in sorted(etiquetas):
    try:
        canon.setdefault(codecs.lookup(e).name, e)
    except LookupError:
        pass


def admite(M, etiqueta):
    doc = f'<html><head><meta charset="{etiqueta}"></head><body><p>{CITA}</p></body></html>'.encode("ascii")
    cod, txt = M._decodificar_html(doc)
    return cod is not None, (cod if cod is not None else txt)


res = {c: (admite(VP, e)[0], admite(VE, e)[0], admite(VE, e)[1]) for c, e in sorted(canon.items())}
adm_ve = sorted(c for c, (a, b, _) in res.items() if b)
adm_vp = sorted(c for c, (a, b, _) in res.items() if a)
print(f"   códecs de Python (nombres canónicos): {len(res)} · admitidos por la anterior: {len(adm_vp)} · por la cuarta: {len(adm_ve)}")
print("   dejan de admitirse con la cuarta:", sorted(set(adm_vp) - set(adm_ve)))
print("   se admiten con la cuarta y no con la anterior:", sorted(set(adm_ve) - set(adm_vp)))
print("   admitidos por la cuarta:", adm_ve)
fuera = [c for c in adm_ve if c not in WHATWG and c not in WHATWG_OTRA]
print("   de ellos, fuera de la lista WHATWG (un navegador no conoce la etiqueta y usa su codificación por defecto):", fuera)
print("   de ellos, que WHATWG lee como OTRA codificación:", {c: WHATWG_OTRA[c] for c in adm_ve if c in WHATWG_OTRA}, "(latin-1 y ascii ya se leen como cp1252: H7)")


def ascii_compatible(c):
    try:
        return bytes(range(0x20, 0x7F)).decode(c) == bytes(range(0x20, 0x7F)).decode("ascii")
    except Exception:  # noqa: BLE001
        return False


print("   admitidos por la cuarta que NO son compatibles con ASCII (los bytes ASCII del documento no son su texto):", [c for c in adm_ve if not ascii_compatible(c)])
print("   WHATWG que la cuarta NO admite (quedan pendientes: conservador):", sorted(c for c in WHATWG if c in res and not res[c][1]), "· no existen en Python:", sorted(c for c in WHATWG if c not in res))
for et in ("cp875", "iso-2022-kr", "hz", "utf-7", "cp037", "ibm850", "euc-kr", "windows-874", "x-mac-cyrillic", "macintosh", "ibm866", "koi8-t", "utf-32", "shift_jis_2004", "iso-2022-jp-2", "cp1125", "mac-greek"):
    a, b = admite(VP, et), admite(VE, et)
    print(f"      charset={et:16} anterior: {'admitida' if a[0] else 'pendiente'}  cuarta: {'admitida' if b[0] else 'pendiente'} · {str(b[1])[:90]}")

print("\n== C · ISO-8859-9 / ISO-8859-11: el byte 0x96 es «–» en windows-1254 y windows-874 (lo que muestra un navegador) y un carácter de control en la tabla ISO")
for et in ("iso-8859-9", "iso-8859-11", "iso-8859-1", "iso-8859-15", "windows-1254"):
    doc = f'<html><head><meta charset="{et}"></head><body><p>Resultado '.encode("ascii") + b"\x96849697.000</p></body></html>"
    p = os.path.join(TMP, f"c_{et}.html")
    open(p, "wb").write(doc)
    for M, etq in ((VP, "anterior"), (VE, "cuarta")):
        e, t = M._texto_html_visible(p)
        t = t.strip() if e == "ok" else t
        lect = M._cita_cifra("849697.000", 849697.0, t) if e == "ok" else ("—", "")
        print(f"      charset={et:13} {etq:8}: {e:9} texto {t[:40]!r:44} lectura de «849697.000» con valor_fuente +849697: {lect[0]}")
