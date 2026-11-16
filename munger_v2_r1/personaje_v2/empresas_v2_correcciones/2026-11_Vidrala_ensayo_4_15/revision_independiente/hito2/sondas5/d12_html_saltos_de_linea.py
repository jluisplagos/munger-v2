#!/usr/bin/env python3
"""d12 · V2 (quinta comprobación) con una fuente HTML: ¿puede el texto visible de un HTML tener la forma de riesgo «…1980⏎-2050»
(un número al final de una línea y, al principio de la siguiente, un guion pegado a otro)? Se extrae el texto visible con
_texto_html_visible y se lee +2050 en él (la fuente publica −2050). Solo usa archivos temporales propios.
Uso: python3 -I -B d12_html_saltos_de_linea.py"""
import os, shutil, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun5 import VE, F, ACT  # noqa: E402
d = tempfile.mkdtemp(prefix="d12_", dir=os.path.join(F, "tmp"))
print("código:", ACT)
casos = {"<br> entre las celdas": "<html><body><p>Gastos financieros<br>-1980<br>-2050</p></body></html>",
         "tabla escrita en líneas": "<html><body><table>\n<tr>\n<td>Gastos financieros</td>\n<td>-1980</td>\n<td>-2050</td>\n</tr>\n</table></body></html>",
         "tabla sin saltos": "<html><body><table><tr><td>Gastos financieros</td><td>-1980</td><td>-2050</td></tr></table></body></html>",
         "bloques <div>": "<html><body><div>Gastos financieros</div><div>-1980</div><div>-2050</div></body></html>",
         "<pre> con saltos de línea": "<html><body><pre>Gastos financieros\n-1980\n-2050</pre></body></html>",
         "párrafo con saltos de línea literales": "<html><body><p>Gastos financieros\n-1980\n-2050</p></body></html>"}
try:
    for n, h in casos.items():
        p = os.path.join(d, "caso.html")
        open(p, "w", encoding="utf-8").write(h)
        est, t = VE._texto_html_visible(p)
        r = VE._cita_cifra("Gastos financieros -1980 -2050", 2050, t)
        print(f"   {n:40} texto visible={t.strip()!r:44} → lectura de +2050: {r[0]}" + ("   <<< acepta +2050 (la fuente publica −2050)" if r[0] == "ok" else ""))
finally:
    shutil.rmtree(d, ignore_errors=True)
