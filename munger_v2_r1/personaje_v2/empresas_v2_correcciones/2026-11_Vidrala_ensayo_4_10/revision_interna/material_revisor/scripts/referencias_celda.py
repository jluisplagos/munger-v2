"""Revisión interna 4.10: etiquetas de Historia filas 5-26 y fórmulas que leen Historia!L25/L26 y Diagnóstico V6!C15 (openpyxl, sin recalcular)."""
import re, sys, openpyxl
wb = openpyxl.load_workbook(sys.argv[1], data_only=False)
h = wb["Historia"]
for r in (10, 24, 25, 26, 27):
    print("Historia fila", r, [h.cell(r, c).value for c in range(1, 4)], "L =", h.cell(r, 12).value)
objetivos = [("Historia", "L26"), ("Historia", "L25"), ("Diagnóstico V6", "C15"), ("Historia", "L10")]
pat = {o: re.compile(r"(?:'?%s'?!)?\$?%s\$?%s(?![0-9])" % (re.escape(o[0]), o[1][0], o[1][1:])) for o in objetivos}
rango26 = re.compile(r"Historia'?!\$?[A-L]\$?\d+:\$?[A-L]\$?26\b|Historia'?!\$?L\$?2[0-6]:")
for ws in wb.worksheets:
    for row in ws.iter_rows():
        for c in row:
            v = c.value
            if isinstance(v, str) and v.startswith("="):
                for o, p in pat.items():
                    mism = ws.title == o[0]
                    if (o[0] in v and p.search(v)) or (mism and re.search(r"(?<![A-Z!])\$?%s\$?%s(?![0-9])" % (o[1][0], o[1][1:]), v)):
                        print(f"{o[0]}!{o[1]} ← {ws.title}!{c.coordinate}: {v[:160]}")
                if rango26.search(v):
                    print(f"RANGO hasta fila 26 ← {ws.title}!{c.coordinate}: {v[:160]}")
d = wb["Diagnóstico V6"]
print("Diagnóstico V6!C15 =", d["C15"].value, "· B15 =", d["B15"].value, "· A15 =", d["A15"].value)
