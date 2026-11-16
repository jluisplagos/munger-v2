#!/usr/bin/env python3
"""d11 · MAX_APARICIONES_CITA con una fuente HTML (quinta comprobación), en el registro completo (fixture de la batería). En una fuente
HTML la cifra se lee también en el texto visible del DOCUMENTO ENTERO (no tiene páginas): el máximo de 200 cuenta las apariciones de
la cita en todo el documento, aunque en la página citada del texto conservado aparezca una vez. Caso: un informe en HTML en el que la
cita («Ejercicio 2019», la de la entrada del año) aparece N veces, siempre igual, y una vez en la página citada del texto conservado.
PV=<prev>/personaje_v2 para la candidata anterior.  Uso: python3 -I -B d11_html_documento_entero.py"""
import hashlib, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sondas"))
import fx5 as X  # noqa: E402
VE = X.VE
print("código:", "quinta (876bfc2)" if "MAX_APARICIONES_CITA" in open(VE.__file__, encoding="utf-8").read() else "anterior (7a6583b, 4.ª comprobación)")
print("control positivo:", X.resumen(X.con())[:80])
KA = "Historia!F5"
e = X.ent(X.REG, KA)
cita = e["fuente"]["cita"]
print(f"{KA}: valor_fuente {e['fuente']['valor_fuente']}, cita {cita!r}")
for n in (1, 150, 200, 201, 400):
    html = "<html><body>" + "".join(f"<p>{cita} · sección {i}</p>" for i in range(n)) + "</body></html>"
    txt = "[PDF PAGE 1]\n" + cita + " · sección 0\n"
    open(os.path.join(X.FS, f"d11_{n}.html"), "w", encoding="utf-8").write(html)
    open(os.path.join(X.FS, f"d11_{n}.txt"), "w", encoding="utf-8").write(txt)
    r = X.con(lambda g, n=n, html=html, txt=txt: X.ent(g, KA)["fuente"].update(archivo=f"fuentes_sinteticas/d11_{n}.html", sha256=hashlib.sha256(html.encode("utf-8")).hexdigest(),
                                                                             archivo_texto=f"fuentes_sinteticas/d11_{n}.txt", sha256_texto=hashlib.sha256(txt.encode("utf-8")).hexdigest(), pagina=1), resellar=True)
    print(f"   la cita aparece {n:4} veces en el documento HTML (1 en la página citada del texto conservado) → "
          + ("COMPROBADA" if KA in r["comprobadas"] else "no comprobada · " + "; ".join(X.con_k(r, KA))[:230]))
print("control positivo al final:", X.resumen(X.con())[:80])
X.limpiar()
