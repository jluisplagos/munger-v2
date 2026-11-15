#!/usr/bin/env python3
"""s7b · U5: texto visible literal que devuelve _texto_html_visible en algunos casos (para ver diferencias entre intérpretes)."""
import os, re, sys, tempfile, unicodedata
F = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(F, "copia", "munger_v2_r1", "personaje_v2", "scripts", "verificacion_entradas.py")
src = open(SRC, encoding="utf-8").read()
ns = {"re": re, "unicodedata": unicodedata}
exec(compile(src[src.index("HTML_SIN_TEXTO_VISIBLE = "):src.index("def _tipo_fuente(ruta):")], "ve_html", "exec"), ns)
TMP = tempfile.mkdtemp(prefix="rev_fable_s7b_", dir=os.path.join(F, "tmp"))
print("python", sys.version.split()[0])
for nombre, h in [("comentario sin cerrar", "<p>a</p><!-- nota CITA"), ("comentario sin cerrar con > dentro", "<p>a</p><!-- nota > CITA"),
                  ("comentario sin cerrar con etiqueta dentro", "<p>a</p><!-- <p>CITA</p>"), ("declaración sin cerrar", "<p>a</p><!DOCTYPE CITA"),
                  ("etiqueta sin cerrar al final", '<p>a</p><div title="CITA'), ("etiqueta sin cerrar con > en atributo", '<p>a</p><div title="x > CITA'),
                  ("script sin cerrar", "<p>a</p><script>var x = 'CITA'"), ("style sin cerrar", "<p>a</p><style>.x{content:'CITA'}"),
                  ("textarea sin cerrar", "<p>a</p><textarea>CITA"), ("title sin cerrar", "<p>a</p><title>CITA"),
                  ("script con </script dentro de cadena", "<p>a</p><script>var x = '</script>CITA';</script>"),
                  ("script con comentario <!-- <script> --> (doble escape)", "<p>a</p><script><!-- <script> </script> CITA --></script><p>b</p>"),
                  ("CDATA", "<p>a</p><![CDATA[ CITA ]]><p>b</p>"), ("CDATA en svg", "<p>a</p><svg><![CDATA[ CITA ]]></svg>"),
                  ("plaintext", "<p>a</p><plaintext><div hidden>CITA</div>"), ("iframe con marcado", "<p>a</p><iframe><p>CITA</p></iframe><p>b</p>"),
                  ("noscript con marcado", "<p>a</p><noscript><p>CITA</p></noscript><p>b</p>"), ("entidad sin punto y coma", "<p>CITA &euro 5 &amp 6 &nbsp7</p>"),
                  ("</p > con espacio", "<p hidden>x</p >CITA"), ("</script\t>", "<script>x</script\t>CITA"), ("etiqueta con salto de línea", "<p\nhidden\n>x</p>CITA")]:
    p = os.path.join(TMP, "f.html")
    open(p, "w", encoding="utf-8").write(h)
    print(f"   {nombre:55} {h!r:62} -> {ns['_texto_html_visible'](p)!r}")
import shutil
shutil.rmtree(TMP, ignore_errors=True)
