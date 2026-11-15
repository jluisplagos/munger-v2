#!/usr/bin/env python3
"""s7 · U5: texto visible de una fuente HTML (_texto_html_visible) y su codificación (_decodificar_html). Nivel de unidad, sin importar
el resto del verificador (se ejecutan solo esas funciones desde el código fuente, para poder usar también python3.11 y python3.12, que
aquí no tienen lxml). Para cada caso: ¿la cita se da por presente en el texto visible? (misma comparación que contraste_pagina:
_cmp_txt_espacios(cita) in _cmp_txt_espacios(texto visible)). «navegador» = lo que mostraría un navegador (HTML5), a juicio del revisor.
Uso: pythonX -I -B s7_u5_html.py [ruta de verificacion_entradas.py]"""
import os, re, sys, tempfile, unicodedata
F = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(F, "copia", "munger_v2_r1", "personaje_v2", "scripts", "verificacion_entradas.py")
src = open(SRC, encoding="utf-8").read()
ini = src.index("HTML_SIN_TEXTO_VISIBLE = ")
fin = src.index("def _tipo_fuente(ruta):")
ns = {"re": re, "unicodedata": unicodedata}
exec(compile(src[ini:fin], "verificacion_entradas.py[HTML]", "exec"), ns)
visible, cmp_e, decod = ns["_texto_html_visible"], ns["_cmp_txt_espacios"], ns["_decodificar_html"]
TMP = tempfile.mkdtemp(prefix="rev_fable_s7_", dir=os.path.join(F, "tmp"))
CITA = "Ventas netas del grupo: 849.697"
print("python", sys.version.split()[0])


def caso(nombre, html, navegador, cita=CITA):
    p = os.path.join(TMP, "f.html")
    open(p, "wb").write(html if isinstance(html, bytes) else html.encode("utf-8"))
    try:
        est, txt = visible(p)
    except Exception as ex:  # noqa: BLE001
        est, txt = "EXCEPCIÓN", f"{type(ex).__name__}: {ex}"
    if est == "ok":
        res = "presente" if cmp_e(cita) in cmp_e(txt) else "ausente"
    else:
        res = f"{est} ({str(txt)[:90]})"
    marca = ""
    if navegador == "oculta" and res == "presente":
        marca = "   <<< SE ACEPTA un texto que el navegador no muestra"
    elif navegador == "visible" and res != "presente":
        marca = "   <<< se rechaza un texto que el navegador muestra"
    print(f"   {nombre:78} navegador: {navegador:8} control: {res}{marca}")


B = "<p>otro texto</p>"
print("== A · no visible en el navegador")
caso("A1 comentario sin cerrar hasta el final", f"<html><body>{B}<!-- nota {CITA}", "oculta")
caso("A2 comentario cerrado con --!>", f"<html><body>{B}<!-- nota {CITA} --!><p>fin</p></body></html>", "oculta")
caso("A3 CDATA en HTML (comentario espurio)", f"<html><body>{B}<![CDATA[ {CITA} ]]></body></html>", "oculta")
caso("A4 comentario condicional de IE", f"<html><body>{B}<!--[if IE]><p>{CITA}</p><![endif]--></body></html>", "oculta")
caso("A5 instrucción de proceso <? … >", f"<html><body>{B}<? {CITA} ></body></html>", "oculta")
caso("A6 etiqueta de cierre espuria </ … >", f"<html><body>{B}</ {CITA}></body></html>", "oculta")
caso("A7 declaración espuria <! … >", f"<html><body>{B}<! {CITA} ></body></html>", "oculta")
caso("A8 style con display:none y comentario CSS", f'<html><body>{B}<div style="display:/**/none">{CITA}</div></body></html>', "oculta")
caso("A9 clase CSS que oculta (hoja de estilo en <style>)", f'<html><head><style>.x{{display:none}}</style></head><body>{B}<div class="x">{CITA}</div></body></html>', "oculta")
caso("A10 font-size:0", f'<html><body>{B}<span style="font-size:0">{CITA}</span></body></html>', "oculta")
caso("A11 opacity:0", f'<html><body>{B}<span style="opacity:0">{CITA}</span></body></html>', "oculta")
caso("A12 fuera de pantalla (left:-9999px)", f'<html><body>{B}<div style="position:absolute;left:-9999px">{CITA}</div></body></html>', "oculta")
caso("A13 <details> cerrado", f"<html><body>{B}<details><summary>más</summary><p>{CITA}</p></details></body></html>", "oculta")
caso("A14 <dialog> sin abrir", f"<html><body>{B}<dialog><p>{CITA}</p></dialog></body></html>", "oculta")
caso("A15 contenido alternativo de <canvas>", f"<html><body>{B}<canvas>{CITA}</canvas></body></html>", "oculta")
caso("A16 contenido alternativo de <video>/<audio>", f"<html><body>{B}<video>{CITA}</video></body></html>", "oculta")
caso("A17 <noembed> / <noframes>", f"<html><body>{B}<noembed>{CITA}</noembed><noframes>{CITA}</noframes></body></html>", "oculta")
caso("A18 <datalist><option>", f"<html><body>{B}<datalist><option>{CITA}</option></datalist></body></html>", "oculta")
caso("A19 <div hidden/> (en HTML la barra se ignora: sigue abierto)", f"<html><body>{B}<div hidden/>{CITA}</div></body></html>", "oculta")
caso("A20 <script/> (en HTML la barra se ignora: todo lo que sigue es script)", f"<html><body>{B}<script/>{CITA}", "oculta")
caso("A21 <title/> en el body", f"<html><body>{B}<title/>{CITA}", "oculta")
caso("A22 </div> dentro de una celda no cierra el div oculto exterior", f'<html><body>{B}<div style="display:none"><table><tr><td>x</div>{CITA}</td></tr></table></div></body></html>', "oculta")
caso("A23 atributo title / alt / value", f'<html><body>{B}<a title="{CITA}">x</a><img alt="{CITA}"><input type="hidden" value="{CITA}"></body></html>', "oculta")
caso("A24 <xmp> (texto literal) con la cita dentro de una etiqueta oculta", f"<html><body>{B}<xmp><div hidden>{CITA}</div></xmp></body></html>", "visible")
caso("A25 JSON en <script type=application/ld+json>", f'<html><body>{B}<script type="application/ld+json">{{"v": "{CITA}"}}</script></body></html>', "oculta")
caso("A26 texto solo para lectores de pantalla (clase sr-only)", f'<html><body>{B}<span class="sr-only">{CITA}</span></body></html>', "oculta")
caso("A27 <rp> (paréntesis de ruby) y <rt>", f"<html><body>{B}<ruby>x<rp>{CITA}</rp></ruby></body></html>", "oculta")
caso("A28 comentario <!--> … (en HTML5 «<!-->» es un comentario vacío)", f"<html><body>{B}<!--> {CITA} <!-- fin --></body></html>", "visible")
print("== B · visible en el navegador")
caso("B1 párrafo normal", f"<html><body><p>{CITA}</p></body></html>", "visible")
caso("B2 sin </head> (cierre opcional en HTML5)", f"<!doctype html><html><head><title>T</title><body><p>{CITA}</p></body></html>", "visible")
caso("B3 sin <html>, <head> ni <body> (opcionales)", f"<!doctype html><title>T</title><p>{CITA}", "visible")
caso("B4 <meta> y <link> en el head y body implícito", f"<!doctype html><head><meta charset=utf-8><link rel=x></head><p>{CITA}", "visible")
caso("B5 <p hidden> seguido de otro <p> (cierre implícito)", f"<html><body><p hidden>oculto<p>{CITA}</body></html>", "visible")
caso("B6 <li hidden> seguido de otro <li>", f"<html><body><ul><li hidden>x<li>{CITA}</ul></body></html>", "visible")
caso("B7 aria-hidden=true (visible en pantalla)", f'<html><body><span aria-hidden="true">{CITA}</span></body></html>', "visible")
caso("B8 iXBRL: (<ix:nonFraction>849.697</ix:nonFraction>) con paréntesis fuera", f'<html><body><table><tr><td>Ventas netas del grupo:</td><td>(<ix:nonFraction name="x" sign="-">849.697</ix:nonFraction>)</td></tr></table></body></html>', "visible", cita="Ventas netas del grupo: (849.697)")
caso("B9 iXBRL: <ix:nonFraction> dentro de un párrafo", f'<html><body><p>Ventas netas del grupo: <ix:nonFraction name="x">849.697</ix:nonFraction></p></body></html>', "visible")
caso("B10 etiquetas en línea no listadas (<ins>, <label>, <big>, <tt>)", f"<html><body><p>Ventas netas del grupo: <ins>849</ins>.697</p></body></html>", "visible")
caso("B11 <input type=text value=…> (el valor se ve)", f'<html><body><p>Ventas netas del grupo: <input type="text" value="849.697"></p></body></html>', "visible")
caso("B12 <textarea> (se ve)", f"<html><body><textarea>{CITA}</textarea></body></html>", "visible")
caso("B13 <svg><text> (se ve)", f"<html><body><svg><text>{CITA}</text></svg></body></html>", "visible")
caso("B14 <select><option selected>", f"<html><body><select><option selected>{CITA}</option></select></body></html>", "visible")
caso("B15 guion blando dentro de una palabra (&shy;)", "<html><body><p>Ven&shy;tas netas del grupo: 849.697</p></body></html>", "visible")
caso("B16 espacio de ancho cero en la cifra", "<html><body><p>Ventas netas del grupo: 849.&#8203;697</p></body></html>", "visible")
caso("B17 entidades numéricas en la cifra", "<html><body><p>Ventas netas del grupo: 8&#52;9.&#x36;97</p></body></html>", "visible")
caso("B18 <br> entre rótulo y cifra", "<html><body><p>Ventas netas del grupo:<br>849.697</p></body></html>", "visible")
caso("B19 celdas contiguas (rótulo | cifra)", "<html><body><table><tr><td>Ventas netas del grupo:</td><td>849.697</td></tr></table></body></html>", "visible")
caso("B20 comentario condicional revelado <![if !IE]>", f"<html><body><![if !IE]><p>{CITA}</p><![endif]></body></html>", "visible")
caso("B21 <noscript> (se ve sin JavaScript)", f"<html><body><noscript><p>{CITA}</p></noscript></body></html>", "visible")
caso("B22 nombre de etiqueta en mayúsculas y atributos sin comillas", f"<HTML><BODY><P CLASS=x>{CITA}</P></BODY></HTML>", "visible")
print("== C · codificación")
caso("C1 ISO-8859-1 declarado, con bytes de windows-1252 (€, –: el navegador lo lee como cp1252)", '<html><head><meta charset="iso-8859-1"></head><body><p>Resultado – 849.697 €</p></body></html>'.encode("cp1252"), "visible", cita="Resultado – 849.697 €")
caso("C2 windows-1252 declarado", '<html><head><meta charset="windows-1252"></head><body><p>Resultado – 849.697 €</p></body></html>'.encode("cp1252"), "visible", cita="Resultado – 849.697 €")
caso("C3 UTF-16 LE sin BOM y sin declaración (bytes válidos como UTF-8)", f"<html><body><p>{CITA}</p></body></html>".encode("utf-16-le"), "visible")
caso("C4 charset=rot13 (códec de Python que no es de texto)", f'<html><head><meta charset="rot13"></head><body><p>{CITA}</p></body></html>', "visible")
caso("C5 charset=unicode_escape con la cifra escapada", '<html><head><meta charset="unicode_escape"></head><body><p>Ventas netas del grupo: \\u0038\\u0034\\u0039.697</p></body></html>', "oculta")
caso("C6 charset=utf-7 con la cifra codificada", '<html><head><meta charset="utf-7"></head><body><p>Ventas netas del grupo: +ADgANAA5-.697</p></body></html>', "oculta")
caso("C7 <meta charset> dentro de un comentario (no cuenta) y página en UTF-8", f'<html><head><!-- <meta charset="utf-16"> --></head><body><p>{CITA} — año</p></body></html>', "visible")
caso("C8 UTF-8 declarado con un byte inválido suelto", f'<html><head><meta charset="utf-8"></head><body><p>{CITA}</p><p>caf'.encode() + b"\xe9" + "</p></body></html>".encode(), "visible")
caso("C9 BOM UTF-8 y meta ISO-8859-1 (manda el BOM)", b"\xef\xbb\xbf" + '<html><head><meta charset="iso-8859-1"></head><body><p>Resultado – 849.697 €</p></body></html>'.encode("utf-8"), "visible", cita="Resultado – 849.697 €")
caso("C10 declaración XML de XHTML", f'<?xml version="1.0" encoding="ISO-8859-1"?><html xmlns="http://www.w3.org/1999/xhtml"><body><p>Año: {CITA}</p></body></html>'.encode("iso-8859-1"), "visible")
caso("C11 «charset=» en el contenido de otra meta antes de la buena", f'<html><head><meta name="description" content="sobre charset=foo"><meta charset="utf-8"></head><body><p>{CITA}</p></body></html>', "visible")
import shutil
shutil.rmtree(TMP, ignore_errors=True)
