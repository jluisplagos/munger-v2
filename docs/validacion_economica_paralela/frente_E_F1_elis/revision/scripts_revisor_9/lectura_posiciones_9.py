"""Revisión independiente n.º 9 · lectura con otro motor de las filas de U1 (frente E · F1 · Elis). No modifica nada del autor.

Lee con pdfminer (pdfplumber), no con pdftotext, las palabras de las filas que cita la objeción U1, con la coordenada
horizontal de cada una en puntos: sirve para comprobar, con un motor distinto del que usa el verificador, que el «0» que
`token_del_rotulo` da por «el día de la fecha» es la primera cifra de la fila, a la derecha del rótulo, y que en «Number of
fatal accidents · 0(a) · 0 · 0» el primer «0» sin llamada está bajo «Group 2020».

Uso: python3 -I -B lectura_posiciones_9.py --raiz <munger_v2_r1> --c18 <frente C19>
"""
import argparse
import json
import re
import sys
from pathlib import Path

CASOS = [("URD2025", 360, r"as at 12/31/2025", 1, "filas «as at 12/31/2025», con la línea de rótulo de encima"),
         ("DEU2024FR", 306, r"au 31/12/2024", 1, "filas «au 31/12/2024», con la línea de rótulo de encima"),
         ("URD2021", 176, r"Number of fatal accidents|Group 2021", 0, "cabecera «Group 2021 · Group 2020 · Group 2019» y fila «Number of fatal accidents»")]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raiz", required=True, type=Path)
    ap.add_argument("--c18", required=True, type=Path)
    a = ap.parse_args()
    import pdfplumber
    fuentes = json.loads((a.c18 / "datos" / "fuentes.json").read_text(encoding="utf-8"))["fuentes"]
    print(f"Lectura con pdfminer (pdfplumber {pdfplumber.__version__}): palabra@x0 en puntos, por fila")
    for doc, pag, rx, antes, txt in CASOS:
        print()
        print(f"{doc} p.{pag} · {txt}")
        with pdfplumber.open(str(a.raiz / fuentes[doc]["archivo"])) as d:
            w = d.pages[pag - 1].extract_words(keep_blank_chars=False, x_tolerance=1.5, y_tolerance=2)
        filas = {}
        for x in w:
            filas.setdefault(round(x["top"] / 2.5), []).append(x)
        claves = sorted(filas)
        for n, k in enumerate(claves):
            if re.search(rx, " ".join(x["text"] for x in sorted(filas[k], key=lambda x: x["x0"]))):
                for kk in claves[max(0, n - antes): n + 1]:
                    r = sorted(filas[kk], key=lambda x: x["x0"])
                    print(f"   y={r[0]['top']:6.1f} | " + "  ".join(f"{x['text']}@{x['x0']:.0f}" for x in r))
                print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
