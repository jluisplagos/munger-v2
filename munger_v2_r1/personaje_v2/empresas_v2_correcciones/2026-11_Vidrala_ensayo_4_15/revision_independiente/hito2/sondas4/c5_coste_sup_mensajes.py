#!/usr/bin/env python3
"""c5 · varios (cuarta comprobación), candidata anterior (f3d15e8) → cuarta (7a6583b).
A) coste de la clasificación de la cita cortada (T2): la función en_numero recorre el texto anterior a CADA fragmento; página de una sola
   línea con miles de fragmentos de la cita (la cita empieza por una cifra y acaba dentro de una palabra).
B) categoría y mensaje en el registro completo (fixture de la batería): cita cortada dentro de una palabra (pendiente) y dentro de un número
   (discrepancia).
C) llamada de nota en <sup> pegada a la cifra en una fuente HTML («849697.000<sup>1</sup>»): <sup> es un elemento en línea y el texto
   visible queda «849697.0001» (no es de este diff: viene de U5/N3; se anota porque la lectura en el documento es de N3/T4).
Uso: python3 -I -B c5_coste_sup_mensajes.py"""
import hashlib, os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sondas3"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sondas"))
from comun3 import VE, VP, ACT, ANT  # noqa: E402

print(f"VE = {ACT} · VP = {ANT}")
print("== A · coste de _cita_cifra con una cita que solo aparece como fragmento, N veces en una página de una sola línea")
for n in (1000, 5000, 20000):
    for nombre, pagina, cita, vf in (("empieza por cifra, acaba dentro de una palabra", " ".join(["5 total"] * n) + "\n", "5 tot", 5),
                                     ("empieza dentro de una palabra, acaba en cifra", " ".join(["Total 5"] * n) + "\n", "otal 5", 5),
                                     ("cortada dentro de un número (corta al primero)", " ".join(["Total 51"] * n) + "\n", "Total 5", 5)):
        fila = f"   N={n:6} ({len(pagina) // 1000:4} kB) {nombre:48}"
        for M, etq in ((VP, "anterior"), (VE, "cuarta")):
            t0 = time.time()
            r = M._cita_cifra(cita, vf, pagina)[0]
            fila += f" · {etq}: {r:14} {time.time() - t0:6.2f} s"
        print(fila)

import fx5 as X  # noqa: E402
K = X.K
print("\n== B · registro completo: categoría y mensaje · código:", ACT if X.VE.__file__ == VE.__file__ else X.VE.__file__)
print("   control positivo:", X.resumen(X.con())[:80])
VF = X.ent(X.REG, K)["fuente"]["valor_fuente"]
c = f"{VF:.3f}"
for nombre, linea, cita in (("B1 cita cortada dentro de una PALABRA («Subpartida…» citada «partida…»)", f"Subpartida sintética de {K}: {c}", f"partida sintética de {K}: {c}"),
                            ("B2 cita cortada dentro de un NÚMERO", f"Partida sintética de {K}: {c}0", f"Partida sintética de {K}: {c}"),
                            ("B3 cita que acaba dentro de una palabra", f"Partida sintética de {K}: {c} millones", f"Partida sintética de {K}: {c} mill"),
                            ("B4 punto pegado delante de la cifra («{K}.{c}»): no es de un número", f"Partida sintética de {K}.{c}", c),
                            ("B5 control: unidad pegada detrás", f"Partida sintética de {K}: {c}m", f"Partida sintética de {K}: {c}")):
    n = X.nueva_pagina(linea)
    r = X.con(lambda g: X.ent(g, K)["fuente"].update(cita=cita, pagina=n), resellar=True)
    print(f"   {nombre}\n      página={linea!r}\n      cita={cita!r}\n      -> " + ("comprobada" if K in r["comprobadas"] else "NO comprobada · " + "; ".join(X.con_k(r, K))[:330]))

print("\n== C · fuente HTML con una llamada de nota en <sup> pegada a la cifra")
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
