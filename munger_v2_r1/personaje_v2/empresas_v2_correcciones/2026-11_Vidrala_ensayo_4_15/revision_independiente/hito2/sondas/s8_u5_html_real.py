#!/usr/bin/env python3
"""s8 · U5 con las dos fuentes HTML REALES del árbol (Elis, fuentes_2026): solo lectura.
A) las tres citas de la cuarta pasada (r4, A') contra contraste_pagina, con un texto conservado sintético de una página;
B) referencia independiente con BeautifulSoup + lxml: cada bloque de texto visible (p, li, td, th, h1–h6, dd, dt) con alguna cifra se busca
   en el texto visible del control (misma comparación que contraste_pagina). Se cuentan los bloques que el control no encuentra
   (rechazos falsos) con el código del hito 2 y con la regla del hito 1 (etiquetas quitadas con una expresión regular, sin espacios)."""
import hashlib, html as _html, os, re, shutil, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import VE, PV, F
from bs4 import BeautifulSoup

FUENTES = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_14", "elis_decisiones", "Elis", "fuentes_2026")
TMP = tempfile.mkdtemp(prefix="rev_fable_s8_", dir=os.path.join(F, "tmp"))


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


print("== A · citas de la cuarta pasada sobre Elis_OCEANE_2029_resultados_conversion.html")
h = os.path.join(TMP, "elis_oceane.html")
shutil.copy(os.path.join(FUENTES, "Elis_OCEANE_2029_resultados_conversion.html"), h)
for cita_e, vf in (("representing an aggregate redemption amount of €3,304,271.85", 3304271.85), ("at a price of €100,129.45 per Bond", 100129.45),
                   ("representing an aggregate redemption amount of €3,304,271.99", 3304271.99)):
    t = os.path.join(TMP, "elis_oceane.txt")
    open(t, "w", encoding="utf-8").write(f"[PDF PAGE 1]\n… {cita_e} …\n")
    f = {"archivo": "elis_oceane.html", "archivo_texto": "elis_oceane.txt", "sha256_texto": sha(t), "pagina": 1, "cita": cita_e}
    print(f"   cita {cita_e!r} → {VE.contraste_pagina(TMP, 'aux:elis', f, h, vf) or 'pasa el contraste'}")

print("\n== B · bloques de texto con cifras (referencia: BeautifulSoup + lxml) frente al texto visible del control")
for nombre in ("Elis_OCEANE_2029_resultados_conversion.html", "Elis_comunicados_Euronext.html"):
    ruta = os.path.join(FUENTES, nombre)
    crudo = open(ruta, "rb").read()
    est, plano = VE._texto_html_visible(ruta)
    plano2 = VE._cmp_txt_espacios(plano) if est == "ok" else ""
    crudo_txt = crudo.decode("utf-8", errors="replace")
    plano1 = VE._cmp_txt(_html.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", crudo_txt))))  # regla del hito 1
    sopa = BeautifulSoup(crudo, "lxml")
    for x in sopa(["script", "style", "template", "head", "noscript"]):
        x.decompose()
    bloques, vistos = [], set()
    for el in sopa.find_all(["p", "li", "td", "th", "h1", "h2", "h3", "h4", "h5", "h6", "dd", "dt"]):
        if el.find(["p", "li", "td", "th", "table", "ul", "ol", "div"]):
            continue  # solo bloques hoja
        t = re.sub(r"\s+", " ", el.get_text()).strip()
        if len(t) >= 25 and re.search(r"\d", t) and t not in vistos:
            vistos.add(t)
            bloques.append((el, t))
    no2 = [(el, t) for el, t in bloques if VE._cmp_txt_espacios(t) not in plano2]
    no1 = [(el, t) for el, t in bloques if VE._cmp_txt(t) not in plano1]
    print(f"   {nombre}: estado {est}; {len(bloques)} bloques con cifras; no encontrados por el control del hito 2: {len(no2)}; por la regla del hito 1: {len(no1)}")
    for el, t in no2[:8]:
        print(f"        hito 2 no encuentra: {t[:110]!r}\n            marcado: {str(el)[:230]!r}")
    etiquetas = {}
    for el, t in no2:
        for d in el.find_all(True):
            etiquetas[d.name] = etiquetas.get(d.name, 0) + 1
    print("        etiquetas dentro de los bloques no encontrados:", dict(sorted(etiquetas.items(), key=lambda kv: -kv[1])[:12]))
shutil.rmtree(TMP, ignore_errors=True)
