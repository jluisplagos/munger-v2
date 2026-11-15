"""Revisión interna 4.10: quién lee Historia!L26 (directa o por rango) y quién lee el puente Historia!C65."""
import re, sys, openpyxl
from openpyxl.utils import column_index_from_string as ci
wb = openpyxl.load_workbook(sys.argv[1], data_only=False)
ref = re.compile(r"(?:'([^']+)'|([A-Za-zÁÉÍÓÚáéíóúñÑ0-9_ ]+?))?!?\$?([A-Z]{1,3})\$?(\d+)(?::\$?([A-Z]{1,3})\$?(\d+))?")
tok = re.compile(r"(?:(?:'([^']+)'|([A-Za-z][A-Za-z0-9_]*))!)?\$?([A-Z]{1,3})\$?([0-9]+)(?::\$?([A-Z]{1,3})\$?([0-9]+))?")
def cubre(ws_title, f, hoja, col, fila):
    for m in tok.finditer(f):
        h = m.group(1) or m.group(2) or ws_title
        if h != hoja: continue
        c1, r1 = ci(m.group(3)), int(m.group(4))
        c2, r2 = (ci(m.group(5)), int(m.group(6))) if m.group(5) else (c1, r1)
        if min(c1,c2) <= col <= max(c1,c2) and min(r1,r2) <= fila <= max(r1,r2):
            return True
    return False
for hoja, celda in (("Historia", "L26"), ("Historia", "C65")):
    col, fila = ci(re.match(r"[A-Z]+", celda).group()), int(re.search(r"\d+", celda).group())
    print(f"--- lectores de {hoja}!{celda}")
    for ws in wb.worksheets:
        for row in ws.iter_rows():
            for c in row:
                v = c.value
                if isinstance(v, str) and v.startswith("=") and cubre(ws.title, v, hoja, col, fila):
                    print(f"  {ws.title}!{c.coordinate}: {v[:170]}")
print("Historia C65 =", wb["Historia"]["C65"].value, "· A65 =", wb["Historia"]["A65"].value)
