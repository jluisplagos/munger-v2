#!/usr/bin/env python3
"""n6 · H7 (segunda pasada): lo cambiado en _texto_html_visible (cabecera implícita, summary/details/dialog, startendtag, espacio de
nombres, aria-hidden) y en _decodificar_html / _tipo_fuente. Cada caso dice si un navegador muestra la cita (criterio del revisor) y qué
hace el control en la estable y en la candidata de la primera pasada. Para XHTML (sintaxis XML: .xhtml, declaración <?xml …?>) «<x/>» sí
cierra el elemento. Uso: pythonX -I -B n6_html_segunda.py"""
import os, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from html_solo import VE, VC
print("python", sys.version.split()[0])
CITA = "Importe neto 849.697"
TMP = tempfile.mkdtemp(prefix="rev2_n6_")
N = [0]


def ver(mod, nombre, contenido):
    p = os.path.join(TMP, nombre)
    open(p, "wb").write(contenido if isinstance(contenido, bytes) else contenido.encode("utf-8"))
    try:
        est, t = mod._texto_html_visible(p)
    except Exception as ex:  # noqa: BLE001
        return f"EXCEPCIÓN {type(ex).__name__}"
    if est != "ok":
        return "pendiente"
    return "presente" if mod._cmp_txt_espacios(CITA) in mod._cmp_txt_espacios(t) else "ausente"


def caso(rotulo, html, navegador, ext=".html"):
    N[0] += 1
    e2, e1 = ver(VE, f"c{N[0]}{ext}", html), ver(VC, f"c{N[0]}{ext}", html)
    marca = ""
    if navegador == "visible" and e2 != "presente":
        marca = "   <<< se rechaza un texto que el navegador muestra" + (" (REGRESIÓN: la candidata lo aceptaba)" if e1 == "presente" else "")
    if navegador == "oculta" and e2 == "presente":
        marca = "   <<< SE ACEPTA un texto que el navegador no muestra" + (" (REGRESIÓN: la candidata lo rechazaba)" if e1 != "presente" else "")
    print(f"   {rotulo:92} navegador: {navegador:8} candidata: {e1:9} estable: {e2}{marca}")


X = '<?xml version="1.0" encoding="UTF-8"?>\n<html xmlns="http://www.w3.org/1999/xhtml" xmlns:ix="http://www.xbrl.org/2013/inlineXBRL">'
print("== A · XHTML / iXBRL (sintaxis XML: «<x/>» cierra el elemento)")
caso("A1 XHTML: <script src=…/> autocerrado en el cuerpo", f'{X}<head><title>t</title></head><body><script type="text/javascript" src="a.js"/><p>{CITA}</p></body></html>', "visible", ".xhtml")
caso("A2 XHTML: <div style=\"display:none\"/> vacío y autocerrado antes del contenido", f'{X}<head><title>t</title></head><body><div style="display:none"/><p>{CITA}</p></body></html>', "visible", ".xhtml")
caso("A3 XHTML: <title/> vacío en la cabecera y contenido en el cuerpo", f'{X}<head><title/><meta charset="utf-8"/></head><body><p>{CITA}</p></body></html>', "visible", ".xhtml")
caso("A4 XHTML: <span hidden=\"hidden\"/> autocerrado dentro de un párrafo", f'{X}<head><title>t</title></head><body><p><span hidden="hidden"/>{CITA}</p></body></html>', "visible", ".xhtml")
caso("A5 XHTML: <style/> vacío en el cuerpo", f'{X}<head><title>t</title></head><body><style type="text/css"/><p>{CITA}</p></body></html>', "visible", ".xhtml")
caso("A6 XHTML: <textarea/> autocerrado", f'{X}<head><title>t</title></head><body><textarea name="x"/><p>{CITA}</p></body></html>', "visible", ".xhtml")
caso("A7 iXBRL habitual: cabecera ix:header dentro de <div style=\"display:none\"> cerrado y hecho en línea",
     f'{X}<head><title>t</title></head><body><div style="display:none"><ix:header><ix:hidden><ix:nonNumeric name="a">oculto 111</ix:nonNumeric></ix:hidden></ix:header></div>'
     f'<p>Importe neto <ix:nonFraction name="b" unitRef="u" decimals="3">849.697</ix:nonFraction></p></body></html>', "visible", ".xhtml")
caso("A8 iXBRL: el hecho citado está SOLO en ix:hidden (dentro del div oculto)",
     f'{X}<head><title>t</title></head><body><div style="display:none"><ix:header><ix:hidden><ix:nonNumeric name="a">{CITA}</ix:nonNumeric></ix:hidden></ix:header></div><p>otro</p></body></html>', "oculta", ".xhtml")
caso("A9 iXBRL: ix:header SIN el div oculto que lo envuelve (el texto de ix:hidden se vería)",
     f'{X}<head><title>t</title></head><body><ix:header><ix:hidden><ix:nonNumeric name="a">{CITA}</ix:nonNumeric></ix:hidden></ix:header><p>otro</p></body></html>', "visible", ".xhtml")
caso("A10 etiqueta con espacio de nombres y style=display:none: <ix:nonNumeric style=\"display:none\">", f'<html><body><p><ix:nonNumeric style="display:none">{CITA}</ix:nonNumeric></p><p>otro</p></body></html>', "oculta")
caso("A11 etiqueta con espacio de nombres y atributo hidden: <x:div hidden>", f'<html><body><x:div hidden>{CITA}</x:div><p>otro</p></body></html>', "oculta")
caso("A12 <svg:svg><svg:text> (SVG con prefijo en XHTML: el texto se ve)", f'{X}<head><title>t</title></head><body><svg:svg xmlns:svg="http://www.w3.org/2000/svg"><svg:text>{CITA}</svg:text></svg:svg></body></html>', "visible", ".xhtml")

print("== B · details / summary / dialog")
caso("B1 <details> cerrado con el texto en un <p>", f"<html><body><details><summary>Resumen</summary><p>{CITA}</p></details></body></html>", "oculta")
caso("B2 <summary> de un <details> cerrado", f"<html><body><details><summary>{CITA}</summary><p>x</p></details></body></html>", "visible")
caso("B3 <details open>", f"<html><body><details open><summary>Resumen</summary><p>{CITA}</p></details></body></html>", "visible")
caso("B4 <summary hidden> de un <details> cerrado", f"<html><body><details><summary hidden>{CITA}</summary><p>x</p></details><p>otro</p></body></html>", "oculta")
caso("B5 <summary style=display:none> de un <details> cerrado", f'<html><body><details><summary style="display:none">{CITA}</summary><p>x</p></details><p>otro</p></body></html>', "oculta")
caso("B6 <summary> que no es hijo directo del <details> cerrado (<details><div><summary>…)", f"<html><body><details><div><summary>{CITA}</summary></div></details><p>otro</p></body></html>", "oculta")
caso("B7 segundo <summary> de un <details> cerrado (solo el primero hace de resumen)", f"<html><body><details><summary>Uno</summary><summary>{CITA}</summary></details><p>otro</p></body></html>", "oculta")
caso("B8 <details> cerrado dentro de un <div hidden>, texto en el summary", f"<html><body><div hidden><details><summary>{CITA}</summary></details></div><p>otro</p></body></html>", "oculta")
caso("B9 <details open> dentro de un <details> cerrado, texto en el summary interior", f"<html><body><details><summary>Fuera</summary><details open><summary>{CITA}</summary></details></details><p>otro</p></body></html>", "oculta")
caso("B10 <details> sin cerrar seguido de contenido normal fuera (</details> omitido por error)", f"<html><body><div><details><summary>R</summary><p>x</p></div><p>{CITA}</p></body></html>", "visible")
caso("B11 <dialog open>", f"<html><body><dialog open><p>{CITA}</p></dialog></body></html>", "visible")
caso("B12 <dialog> sin open", f"<html><body><dialog><p>{CITA}</p></dialog><p>otro</p></body></html>", "oculta")
caso("B13 <summary> fuera de un details (sin efecto)", f"<html><body><summary>{CITA}</summary></body></html>", "visible")

print("== C · cabecera implícita y elementos de cabecera")
caso("C1 sin </head>: <head><title>t</title><body>…", f"<html><head><title>t</title><body><p>{CITA}</p></body></html>", "visible")
caso("C2 sin </head> ni <body>: <head><title>t</title><p>…", f"<html><head><title>t</title><p>{CITA}</p></html>", "visible")
caso("C3 texto suelto tras <head> sin ningún elemento del cuerpo", f"<html><head><title>t</title>{CITA}</html>", "visible")
caso("C4 <head> con <noscript><img/></noscript> y luego </head><body>", f'<html><head><noscript><img src="x"/></noscript><title>t</title></head><body><p>{CITA}</p></body></html>', "visible")
caso("C5 la cita en el <title> (no se muestra en la página)", f"<html><head><title>{CITA}</title></head><body><p>otro</p></body></html>", "oculta")
caso("C6 la cita en <title> tras un <div> dentro de <head> sin cerrar", f"<html><head><div></div><title>{CITA}</title><body><p>otro</p></body></html>", "oculta")
caso("C7 la cita en un <style> que sigue a un elemento del cuerpo dentro de <head>", f"<html><head><p>x</p><style>.a{{content:'{CITA}'}}</style><body><p>otro</p></body></html>", "oculta")
caso("C8 <header> (no es <head>)", f"<html><body><header><p>{CITA}</p></header></body></html>", "visible")
caso("C9 dos documentos concatenados (segundo <head> a mitad)", f"<html><head><title>a</title></head><body><p>uno</p></body></html><html><head><title>b</title></head><body><p>{CITA}</p></body></html>", "visible")
caso("C10 <head> dentro del cuerpo con un <p> detrás sin cerrar el head", f"<html><body><p>uno</p><head><meta name='x'><p>{CITA}</p></body></html>", "visible")

print("== D · startendtag en HTML (la barra se ignora) y aria-hidden")
caso("D1 <div hidden/> seguido del texto", f"<html><body><div hidden/><p>{CITA}</p></div><p>otro</p></body></html>", "oculta")
caso("D2 <p/> y <span/> sin atributos (inocuos)", f"<html><body><p/><span/>{CITA}</body></html>", "visible")
caso("D3 <br/> y <img/> (vacíos)", f"<html><body><p>Importe<br/>neto <img src='x'/>849.697</p></body></html>", "visible")
caso("D4 aria-hidden=\"true\" (se ve en pantalla)", f'<html><body><p aria-hidden="true">{CITA}</p></body></html>', "visible")
caso("D5 <a/> autocerrado antes del texto (ancla XHTML servida como HTML: el resto queda dentro del enlace, visible)", f'<html><body><a name="x"/>{CITA}</body></html>', "visible")
caso("D6 <iframe/> autocerrado (en HTML abre un iframe: lo que sigue no se muestra)", f"<html><body><iframe src='x'/><p>{CITA}</p></body></html>", "oculta")

print("== E · codificación y tipo")
caso("E1 ISO-8859-1 declarado con «–» de windows-1252", f'<html><head><meta charset="iso-8859-1"></head><body><p>2024 – {CITA}</p></body></html>'.encode("cp1252"), "visible")
caso("E2 us-ascii declarado con bytes altos de windows-1252", f'<html><head><meta charset="us-ascii"></head><body><p>€ {CITA}</p></body></html>'.encode("cp1252"), "visible")
caso("E3 ISO-8859-15 declarado (el € es 0xA4)", f'<html><head><meta charset="iso-8859-15"></head><body><p>€ {CITA}</p></body></html>'.encode("iso-8859-15"), "visible")
caso("E4 windows-1250 declarado", f'<html><head><meta charset="windows-1250"></head><body><p>ř {CITA}</p></body></html>'.encode("cp1250"), "visible")
caso("E5 x-mac-roman declarado", f'<html><head><meta charset="x-mac-roman"></head><body><p>é {CITA}</p></body></html>'.encode("mac-roman"), "visible")
caso("E6 macintosh declarado", f'<html><head><meta charset="macintosh"></head><body><p>é {CITA}</p></body></html>'.encode("mac-roman"), "visible")
caso("E7 IBM850 declarado (página de códigos DOS)", f'<html><head><meta charset="ibm850"></head><body><p>é {CITA}</p></body></html>'.encode("cp850"), "visible")
caso("E8 Shift_JIS / EUC-KR declarados", f'<html><head><meta charset="euc-kr"></head><body><p>{CITA}</p></body></html>'.encode("euc-kr"), "visible")
caso("E9 utf-16 declarado en meta con el archivo en UTF-8 (los navegadores lo leen como UTF-8)", f'<html><head><meta charset="utf-16"></head><body><p>{CITA}</p></body></html>', "visible")
caso("E10 latin1 declarado como «l1» / «cp819»", f'<html><head><meta charset="cp819"></head><body><p>é {CITA}</p></body></html>'.encode("latin-1"), "visible")
for nombre, cont in (("e_menciona.html", f"<html><body><p>El formato %PDF-1.4</p><p>{CITA}</p></body></html>"), ("e_menciona.txt", "[PDF PAGE 1]\nFormato %PDF-1.7\n" + CITA),
                     ("e_sin_ext", "\x00\x01cabecera\r\n%PDF-1.4\n…"), ("e_xml.xml", "<?xml version='1.0'?><nota>El formato %PDF-1.4</nota>"), ("e_json.json", '{"nota": "%PDF-1.4 mencionado"}'),
                     ("e_md.md", "# Informe\nDescarga en %PDF-1.7\n"), ("e_pdf_tras_blanco.dat", "\n\n   %PDF-1.4\n…"), ("e_lt.dat", "<binario> %PDF-1.4 …")):
    p = os.path.join(TMP, nombre)
    open(p, "wb").write(cont.encode("utf-8"))
    print(f"   tipo de {nombre:22} candidata: {VC._tipo_fuente(p):6} estable: {VE._tipo_fuente(p)}")
import shutil
shutil.rmtree(TMP, ignore_errors=True)
