#!/usr/bin/env python3
"""Testigos, en el registro completo (fixture de la batería), de dos mutaciones NO detectadas que viven dentro de contraste_pagina:
t4b (el texto del HTML se lee sin quitar los caracteres invisibles) y n3c (del documento solo cuenta un signo distinto). El módulo mutado
se carga en memoria (mismo cambio de texto que mutaciones4.py) y su contraste_pagina sustituye al de la candidata solo durante el caso.
Uso: python3 -I -B mutaciones4_testigos_registro.py"""
import hashlib, importlib.util, os, sys, types
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sondas"))
import fx5 as X
from pdfmin import pdf_minimo
VE, K = X.VE, X.K
spec = importlib.util.spec_from_file_location("mutaciones4", os.path.join(os.path.dirname(os.path.abspath(__file__)), "mutaciones4.py"))
M4 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M4)
SRC = open(VE.__file__, encoding="utf-8").read()
ORIG = VE.contraste_pagina


def mutado(nombre):
    s = SRC
    for arch, viejo, nuevo in M4.M[nombre][3]:
        assert s.count(viejo) == 1
        s = s.replace(viejo, nuevo)
    m = types.ModuleType("ve_" + nombre)
    m.__file__ = VE.__file__
    exec(compile(s, VE.__file__ + "[" + nombre + "]", "exec"), m.__dict__)
    return m


VF = X.ent(X.REG, K)["fuente"]["valor_fuente"]
c, R = f"{VF:.3f}", f"Partida sintetica de {K}"
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()  # noqa: E731
print("control positivo:", X.resumen(X.con())[:70])


def caso(mut, nombre, tipo, doc, linea_txt, cita):
    n = X.nueva_pagina(linea_txt)
    nf = f"tr_{mut}.{tipo}"
    if tipo == "pdf":
        open(os.path.join(X.FS, nf), "wb").write(pdf_minimo(["relleno"] * (int(n) - 1) + [doc]))
    else:
        open(os.path.join(X.FS, nf), "w", encoding="utf-8").write(f"<html><head><meta charset='utf-8'></head><body><p>{doc}</p></body></html>")
    s, st = sha(os.path.join(X.FS, nf)), sha(os.path.join(X.FS, "fuente.txt"))
    out = []
    for etq, f in (("candidata", ORIG), ("mutada", mutado(mut).contraste_pagina)):
        VE.contraste_pagina = f
        r = X.con(lambda g: X.ent(g, K)["fuente"].update(archivo=f"fuentes_sinteticas/{nf}", sha256=s, archivo_texto="fuentes_sinteticas/fuente.txt", sha256_texto=st, pagina=n, cita=cita), resellar=True)
        cat = "comprobada" if K in r["comprobadas"] else next((x for x in ("discrepancias", "pendientes", "errores") if any(K in y for y in r.get(x, []))), "?")
        out.append(f"{etq}: {cat}")
    VE.contraste_pagina = ORIG
    print(f"{mut}: {nombre}\n   documento: {doc!r} · texto conservado: {linea_txt!r} · cita: {cita!r}\n   " + " · ".join(out) + ("   TESTIGO" if out[0].split(": ")[1] != out[1].split(": ")[1] else "   sin diferencia"))


caso("t4b_html_con_invisibles", "HTML con un guion blando en una palabra de la cita y la cifra en negativo; texto conservado sin el menos", "html", f"{R}: -{c} to&shy;tal", f"{R}: {c} total", f"{c} total")
caso("n3c_solo_signo_distinto", "el PDF publica la cifra con un dígito más («…0001») y el texto conservado no", "pdf", f"{R}: {c}1 total", f"{R}: {c} total", f"{c}")
print("control positivo al final:", X.resumen(X.con())[:70])
X.limpiar()
