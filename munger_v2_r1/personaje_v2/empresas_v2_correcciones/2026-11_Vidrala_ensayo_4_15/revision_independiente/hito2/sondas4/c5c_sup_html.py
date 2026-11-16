#!/usr/bin/env python3
"""c5c · la parte C de c5 (llamada de nota en <sup> pegada a la cifra en una fuente HTML), ejecutable con otro código:
PV=<prev>/personaje_v2 para la candidata anterior (f3d15e8).  Uso: python3 -I -B c5c_sup_html.py"""
import hashlib, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sondas"))
import fx5 as X
VE, K = X.VE, X.K
print("código:", "cuarta (7a6583b)" if "CODECS_TEXTO_HTML" in open(VE.__file__, encoding="utf-8").read() else "anterior (f3d15e8, 3.ª comprobación)")
VF = X.ent(X.REG, K)["fuente"]["valor_fuente"]
c = f"{VF:.3f}"
print("== C · fuente HTML con una llamada de nota en <sup> pegada a la cifra")
FS = X.FS
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()  # noqa: E731
R = f"Partida sintetica de {K}"
for i, (nombre, cuerpo) in enumerate((("C1 control: sin llamada de nota", f"<p>{R}: {c}</p>"), ("C2 llamada <sup>1</sup> pegada a la cifra", f"<p>{R}: {c}<sup>1</sup></p>"),
                                      ("C3 llamada <sup>(1)</sup>", f"<p>{R}: {c}<sup>(1)</sup></p>"), ("C4 llamada <sup>a</sup>", f"<p>{R}: {c}<sup>a</sup></p>"),
                                      ("C5 llamada con <a>: <a href='#n1'><sup>1</sup></a>", f"<p>{R}: {c}<a href='#n1'><sup>1</sup></a></p>"))):
    n = X.nueva_pagina(f"{R}: {c}")
    nf = f"c5_{i}.html"
    open(os.path.join(FS, nf), "w", encoding="utf-8").write(f"<html><head><meta charset='utf-8'></head><body>{cuerpo}</body></html>")
    s, st = sha(os.path.join(FS, nf)), sha(os.path.join(FS, "fuente.txt"))
    r = X.con(lambda g: X.ent(g, K)["fuente"].update(archivo=f"fuentes_sinteticas/{nf}", sha256=s, archivo_texto="fuentes_sinteticas/fuente.txt", sha256_texto=st, pagina=n, cita=f"{R}: {c}"), resellar=True)
    vis = VE._texto_html_visible(os.path.join(FS, nf))[1].strip()
    print(f"   {nombre}\n      texto visible: {vis!r}\n      -> " + ("comprobada" if K in r["comprobadas"] else "NO comprobada · " + "; ".join(X.con_k(r, K))[:260]))
print("   control positivo al final:", X.resumen(X.con())[:80])
X.limpiar()

