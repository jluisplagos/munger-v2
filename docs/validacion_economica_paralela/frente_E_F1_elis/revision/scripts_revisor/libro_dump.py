"""Vuelca celdas del libro (solo lectura): fórmula y valor en caché.
Uso: python3 -I libro_dump.py <xlsx> <Hoja!A1:B2> [...]
"""
import sys
import openpyxl

def main():
    path = sys.argv[1]
    wf = openpyxl.load_workbook(path, data_only=False, read_only=False)
    wv = openpyxl.load_workbook(path, data_only=True, read_only=False)
    if len(sys.argv) == 2:
        for ws in wf.worksheets:
            print(ws.title, ws.dimensions)
        return
    for ref in sys.argv[2:]:
        sheet, rng = ref.split("!")
        wsf, wsv = wf[sheet], wv[sheet]
        cells = wsf[rng]
        if not isinstance(cells, tuple):
            cells = ((cells,),)
        for row in cells:
            for c in row:
                v = wsv[c.coordinate].value
                if c.value is None and v is None:
                    continue
                f = c.value
                fs = (str(f)[:200] + "…") if isinstance(f, str) and len(str(f)) > 200 else f
                print(f"{sheet}!{c.coordinate}\t{fs!r}\t=> {v!r}")

if __name__ == "__main__":
    main()
