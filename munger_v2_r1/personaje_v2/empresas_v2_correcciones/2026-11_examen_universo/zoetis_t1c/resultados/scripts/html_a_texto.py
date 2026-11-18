#!/usr/bin/env python3
"""zoetis_t1c · texto con marca de página de una página HTML de la Release (comunicado de resultados del T2 2026 de Zoetis).
Extrae el texto visible (sin <script>, <style> ni <noscript>), con saltos de línea en los bloques y tabuladores en las celdas, y lo escribe
como UNA página «[PDF PAGE 1]» (formato de texto/ de los expedientes; el HTML no tiene páginas). No quita ni reordena nada más: la navegación del
sitio y el aviso de cookies quedan en el texto, sin efecto. Uso: python3 -I html_a_texto.py ENTRADA.html SALIDA.txt"""
import html.parser, re, sys


class P(html.parser.HTMLParser):
    def __init__(s):
        super().__init__(); s.out = []; s.skip = 0

    def handle_starttag(s, t, a):
        if t in ("script", "style", "noscript"):
            s.skip += 1
        if t in ("p", "div", "br", "tr", "li", "h1", "h2", "h3", "h4", "table"):
            s.out.append("\n")
        if t in ("td", "th"):
            s.out.append("\t")

    def handle_endtag(s, t):
        if t in ("script", "style", "noscript"):
            s.skip -= 1

    def handle_data(s, d):
        if not s.skip:
            s.out.append(d)


p = P()
p.feed(open(sys.argv[1], encoding="utf-8", errors="replace").read())
t = "".join(p.out)
t = re.sub(r"[ \t\xa0]+", " ", t)
t = re.sub(r"\n\s*\n+", "\n\n", t).strip()
open(sys.argv[2], "w", encoding="utf-8").write("[PDF PAGE 1]\n" + t + "\n\n")
