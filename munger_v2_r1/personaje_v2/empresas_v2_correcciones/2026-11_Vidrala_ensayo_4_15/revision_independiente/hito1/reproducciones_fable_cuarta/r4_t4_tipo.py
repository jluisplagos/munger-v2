"""Cuarta pasada · T4 (tipo de la fuente por su contenido: PDF por cabecera o extensión; HTML con la cita en su texto sin etiquetas; otro →
pendiente; página de PDF sin texto → pendiente).
A · HTML: la cita solo en un comentario, en un atributo, en un <script>, en el <title> o en un elemento oculto; HTML legítimo en
    ISO-8859-1 o UTF-16; cifra partida entre dos celdas; el HTML real de Elis (OCEANE 2029).
B · PDF: cabecera precedida de basura (con y sin extensión .pdf); página con un encabezado como única capa de texto.
C · VE._tipo_fuente sobre nombres y contenidos.
Arnés fx4.py (vínculo escrito a mano). El texto conservado es siempre fuentes_sinteticas/fuente.txt con su huella."""
import hashlib, os, shutil, sys
import fx4 as fx
from fx4 import VE, con, ent, resumen, K, REG, FS
from pdfmin import pdf_minimo

print("árbol:", fx.PV)
paginas = list(fx.paginas)
f_k = ent(REG, K)["fuente"]
CITA, PAG_K = f_k["cita"], int(f_k["pagina"])
print("K:", K, "| página", PAG_K, "| cita:", repr(CITA))


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


SHA_TXT = sha(os.path.join(FS, "fuente.txt"))


def probar(nombre, contenido, rotulo, cita=None):
    p = os.path.join(FS, nombre)
    open(p, "wb").write(contenido if isinstance(contenido, bytes) else contenido.encode("utf-8"))
    s = sha(p)
    cambio = dict(archivo=f"fuentes_sinteticas/{nombre}", sha256=s, archivo_texto="fuentes_sinteticas/fuente.txt", sha256_texto=SHA_TXT)
    r = con(lambda g: ent(g, K)["fuente"].update(cambio), resellar=True)
    print(f"[{rotulo}] ({nombre}; tipo según VE._tipo_fuente: {VE._tipo_fuente(p) if hasattr(VE, '_tipo_fuente') else '—'})\n      {resumen(r, K, 270)}")
    return r


OTRO = "<p>Otro documento, sin la partida citada. Ventas del grupo: 1.234,5</p>"
print("\n=== A · fuente HTML (la cita está en el texto conservado; ¿está en el TEXTO del HTML?)")
probar("a0_fiel.html", f"<!DOCTYPE html><html><head><meta charset='utf-8'><title>Informe</title></head><body><p>{CITA}</p></body></html>", "A0 · control positivo: HTML en UTF-8 con la cita en un párrafo")
probar("a1_ajeno.html", f"<!DOCTYPE html><html><body>{OTRO}</body></html>", "A1 · control negativo: HTML de otro documento, sin la cita")
probar("a2_comentario.html", f"<!DOCTYPE html><html><body>{OTRO}<!-- {CITA} --></body></html>", "A2 · la cita SOLO en un comentario HTML")
probar("a3_comentario_mayor.html", f"<!DOCTYPE html><html><body>{OTRO}<!-- nota del maquetador > {CITA} --></body></html>", "A3 · la cita SOLO en un comentario que contiene un «>» antes de la cita")
probar("a4_atributo.html", f'<!DOCTYPE html><html><body>{OTRO}<img src="x.png" alt="{CITA}"></body></html>', "A4 · la cita SOLO en un atributo (alt)")
probar("a5_atributo_mayor.html", f'<!DOCTYPE html><html><head><meta name="description" content="resumen > {CITA}"></head><body>{OTRO}</body></html>',
       "A5 · la cita SOLO en un atributo (meta description) que contiene un «>» antes de la cita")
probar("a6_script.html", f'<!DOCTYPE html><html><body>{OTRO}<script>var datos = "{CITA}";</script></body></html>', "A6 · la cita SOLO en un <script> bien cerrado")
probar("a7_script_espacio.html", f'<!DOCTYPE html><html><body>{OTRO}<script>var datos = "{CITA}";</script ></body></html>', "A7 · la cita SOLO en un <script> cerrado con «</script >» (cierre válido en HTML)")
probar("a8_script_abierto.html", f'<!DOCTYPE html><html><body>{OTRO}<script>var datos = "{CITA}";', "A8 · la cita SOLO en un <script> sin cerrar")
probar("a9_title.html", f"<!DOCTYPE html><html><head><title>{CITA}</title></head><body>{OTRO}</body></html>", "A9 · la cita SOLO en el <title>")
probar("a10_oculto.html", f'<!DOCTYPE html><html><body>{OTRO}<div style="display:none">{CITA}</div><template>{CITA}</template></body></html>', "A10 · la cita SOLO en un elemento oculto (display:none)")
num = CITA.rsplit(" ", 1)[-1]
probar("a11_partida.html", f"<!DOCTYPE html><html><body><table><tr><td>{CITA[:-len(num)]}{num[:3]}</td><td>{num[3:]} (otra columna)</td></tr></table></body></html>",
       f"A11 · el HTML no contiene la cifra {num}: tiene «{num[:3]}» y «{num[3:]}» en dos celdas contiguas")
fiel = f"<!DOCTYPE html><html><head><meta http-equiv='Content-Type' content='text/html; charset=ISO-8859-1'></head><body><p>{CITA}</p></body></html>"
probar("a12_latin1.html", fiel.encode("latin-1"), "A12 · HTML LEGÍTIMO con la cita, codificado en ISO-8859-1 (declarado en su meta)")
probar("a13_utf16.html", fiel.replace("ISO-8859-1", "UTF-16").encode("utf-16"), "A13 · HTML legítimo con la cita, en UTF-16 con BOM")
probar("a14_entidades.html", "<!DOCTYPE html><html><body><p>" + CITA.replace("é", "&eacute;").replace(" ", "&nbsp;") + "</p></body></html>", "A14 · control: la cita con entidades (&eacute;, &nbsp;)")

print("\n=== A' · HTML real del árbol (Elis, OCEANE 2029), con un texto conservado sintético de una página")
ELIS_HTML = os.path.join(fx.PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_14", "elis_decisiones", "Elis", "fuentes_2026", "Elis_OCEANE_2029_resultados_conversion.html")
if os.path.isfile(ELIS_HTML) and hasattr(VE, "_tipo_fuente"):
    shutil.copy(ELIS_HTML, os.path.join(FS, "elis_oceane.html"))
    for cita_e, vf in (("representing an aggregate redemption amount of €3,304,271.85", 3304271.85), ("at a price of €100,129.45 per Bond", 100129.45),
                       ("representing an aggregate redemption amount of €3,304,271.99", 3304271.99)):
        open(os.path.join(FS, "elis_oceane.txt"), "w", encoding="utf-8").write(f"[PDF PAGE 1]\n… {cita_e} …\n")
        f = {"archivo": "fuentes_sinteticas/elis_oceane.html", "archivo_texto": "fuentes_sinteticas/elis_oceane.txt", "sha256_texto": sha(os.path.join(FS, "elis_oceane.txt")), "pagina": 1, "cita": cita_e}
        print(f"   cita {cita_e!r} → {VE.contraste_pagina(fx.c, 'aux:elis', f, os.path.join(FS, 'elis_oceane.html'), vf) or 'pasa el contraste'}")

print("\n=== B · fuente PDF")
PDF = pdf_minimo(paginas)
probar("b0_fiel.pdf", PDF, "B0 · control positivo: PDF fiel a su texto conservado")
BASURA = b"\x00\x01cabecera de un gestor documental (basura antes del PDF)\r\n" * 5
probar("b1_basura.pdf", BASURA + PDF, f"B1 · el mismo PDF con {len(BASURA)} bytes de basura antes de «%PDF-» y extensión .pdf")
probar("b2_basura.bin", BASURA + PDF, "B2 · los mismos bytes con extensión .bin")
probar("b3_basura_sin_extension", BASURA + PDF, "B3 · los mismos bytes sin extensión")
probar("b4_pdf_sin_extension", PDF, "B4 · control: el PDF fiel (cabecera al principio) sin extensión")
probar("b5_espacios.PDF", b"\r\n  \t" + PDF, "B5 · el PDF fiel con espacios y saltos antes de la cabecera, extensión .PDF")
con_encabezado = list(paginas)
con_encabezado[PAG_K - 1] = "Informe anual 2019 · Grupo sintético · página 3"
probar("b6_escaneado_con_encabezado.pdf", pdf_minimo(con_encabezado),
       "B6 · página escaneada cuya única capa de texto es el encabezado (el texto conservado sería un OCR del resto)")
sin_texto = list(paginas)
sin_texto[PAG_K - 1] = ""
probar("b7_escaneado.pdf", pdf_minimo(sin_texto), "B7 · control de T4: página sin ninguna capa de texto")
probar("b8_falso.pdf", b"%PDF-1.7\nbytes que no son un PDF\n", "B8 · bytes ajenos con cabecera %PDF- y extensión .pdf")
probar("b9_falso.txt", ("%PDF-1.7\n" + "".join(f"[PDF PAGE {i + 1}]\n{p}\n" for i, p in enumerate(paginas))).encode("utf-8"),
       "B9 · el texto conservado con una primera línea «%PDF-1.7» y extensión .txt (pasa a tratarse como PDF)")

print("\n=== C · VE._tipo_fuente (nombre · primeros bytes)")
if hasattr(VE, "_tipo_fuente"):
    d = os.path.join(fx.TMP, "tipos"); os.makedirs(d)
    for nombre, cont in (("informe.pdf", b"%PDF-1.4\n"), ("informe.pdf", b"no es un pdf"), ("informe", b"%PDF-1.4\n"), ("informe.bin", b"\xef\xbb\xbf%PDF-1.4\n"), ("informe.txt", b"[PDF PAGE 1]\nx"),
                         ("informe.TXT", b"<html><body>x</body></html>"), ("informe.md", b"[PDF PAGE 1]\nx"), ("pagina.htm", b"x"), ("pagina", b"<!DOCTYPE html><html>"), ("pagina", b"\xef\xbb\xbf<!DOCTYPE html><html>"),
                         ("pagina", b"<?xml version='1.0'?><html xmlns='http://www.w3.org/1999/xhtml'>"), ("pagina", b"<!-- saved from url=(0014)about:internet -->\n<html>"),
                         ("pagina.aspx", b"<HTML><BODY>"), ("datos.csv", b"a;b"), ("datos.xlsx", b"PK\x03\x04"), ("informe.docx", b"PK\x03\x04"), ("nota.json", b"{}")):
        p = os.path.join(d, nombre)
        open(p, "wb").write(cont)
        print(f"   {nombre!r} · {cont[:40]!r} → {VE._tipo_fuente(p)}")
fx.limpiar()
