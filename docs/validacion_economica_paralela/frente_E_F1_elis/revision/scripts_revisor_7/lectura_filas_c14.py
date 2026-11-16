"""Revisión n.º 7 (frente E · F1 · Elis). Lectura de las dos filas nuevas de C14 y de sus contrapartes de R23 con tres
motores que no son pdftotext: MuPDF (PyMuPDF), pdfminer (pdfplumber) y PDFium (pypdfium2). No modifica nada del autor.

Cada motor da palabras con su posición. Con ellas, sin la rejilla de caracteres de pdftotext:
  - se localiza la fila por su rótulo y su número de ocurrencia en la página;
  - se toma el número de la posición declarada (por la derecha);
  - se lee la cabecera que queda encima de ese número (misma banda horizontal), el año aislado que encabeza el bloque, la
    declaración de unidades de la tabla, la cabecera de la página y el pie.
Después recalcula R23 de 2021 y 2022 con fracciones exactas.

Uso: python3 -I lectura_filas_c14.py --raiz <munger_v2_r1> --autor <frente C14> --pylibs <carpeta con pymupdf>
"""
import argparse
import csv
import json
import re
import sys
import warnings
from fractions import Fraction
from pathlib import Path

NUM = re.compile(r"^\(?-?\d[\d,.]*\)?%?$")
FILAS = ["VENTAS_SEG_U22_2021", "VENTAS_SEG_U23_2022", "IS_VENTAS_U22_2021", "IS_VENTAS_U23_2022"]
# rótulo con el que se busca la fila en cada motor (la etiqueta del CSV, en palabras)
ROTULO = {"VENTAS_SEG_U22_2021": ["SEGMENT", "REVENUE"], "VENTAS_SEG_U23_2022": ["SEGMENT", "REVENUE"],
          "IS_VENTAS_U22_2021": ["Revenue"], "IS_VENTAS_U23_2022": ["Revenue"]}


def palabras_mupdf(pdf, n, fitz):
    pg = fitz.open(str(pdf))[n - 1]
    return [(w[4], w[0], w[2], (w[1] + w[3]) / 2) for w in pg.get_text("words")], pg.rect.height


def palabras_pdfminer(pdf, n):
    import pdfplumber
    with pdfplumber.open(str(pdf)) as d:
        pg = d.pages[n - 1]
        ws = pg.extract_words(x_tolerance=1.5, y_tolerance=2, keep_blank_chars=False)
        return [(w["text"], w["x0"], w["x1"], (w["top"] + w["bottom"]) / 2) for w in ws], float(pg.height)


def palabras_pdfium(pdf, n):
    import pypdfium2 as pdfium
    d = pdfium.PdfDocument(str(pdf))
    pg = d[n - 1]
    alto = pg.get_height()
    tp = pg.get_textpage()
    out = []
    for k in range(tp.count_rects()):
        l, b, r, t = tp.get_rect(k)
        txt = tp.get_text_bounded(l, b, r, t).strip()
        x = l
        # un rectángulo de PDFium puede traer varias palabras: se reparten por su longitud
        partes = txt.split()
        total = sum(len(p) for p in partes) + max(0, len(partes) - 1)
        for p in partes:
            w = (r - l) * len(p) / max(1, total)
            out.append((p, x, x + w, alto - (t + b) / 2))
            x += w + (r - l) / max(1, total)
    return out, alto


def filas(ws, tol=2.5):
    out = []
    for w in sorted(ws, key=lambda w: (w[3], w[1])):
        if out and abs(out[-1][0] - w[3]) <= tol:
            out[-1][1].append(w)
        else:
            out.append([w[3], [w]])
    for f in out:
        f[1].sort(key=lambda w: w[1])
    return out


def leer(ws, alto, rotulo, ocurrencia, pos):
    fs = filas(ws)
    cand = [k for k, f in enumerate(fs) if [w[0] for w in f[1]][:len(rotulo)] == rotulo and any(NUM.match(w[0]) for w in f[1])]
    if not cand:
        return {"error": "fila no encontrada"}
    k = cand[(ocurrencia or 1) - 1]
    f = fs[k]
    nums = [w for w in f[1] if NUM.match(w[0])]
    tok = nums[pos]
    r = {"fila": " ".join(w[0] for w in f[1]), "filas_que_casan": len(cand), "numero": tok[0], "x": (round(tok[1], 1), round(tok[2], 1))}
    # cabecera encima del número: palabras no numéricas que solapan su banda, subiendo hasta la declaración de unidades
    cab, unidades, anio_bloque = [], None, None
    for j in range(k - 1, -1, -1):
        txt = " ".join(w[0] for w in fs[j][1])
        if re.fullmatch(r"20\d\d", txt.strip()):
            anio_bloque = txt.strip()
            break
        if re.search(r"(?i)\(in millions? of euros\)", txt) and unidades is None:
            unidades = txt
        en_banda = [w[0] for w in fs[j][1] if w[2] >= tok[1] - 3 and w[1] <= tok[2] + 3 and not NUM.match(w[0])]
        if unidades is None or re.search(r"(?i)\(in millions? of euros\)", txt) or len(cab) < 3:
            cab += [w for w in en_banda if w not in cab]
        if unidades is not None and fs[k][0] - fs[j][0] > 160:
            break
    r["cabecera_encima"] = cab[:6]
    r["unidades"] = unidades
    r["anio_del_bloque"] = anio_bloque
    cabeza = " | ".join(" ".join(w[0] for w in f2[1]) for f2 in fs if f2[0] < 0.12 * alto)
    pie = " | ".join(" ".join(w[0] for w in f2[1]) for f2 in fs if f2[0] > 0.93 * alto)
    r["cabecera_de_pagina"] = cabeza[:120]
    r["pie"] = pie[:80]
    return r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raiz", required=True, type=Path)
    ap.add_argument("--autor", required=True, type=Path)
    ap.add_argument("--pylibs", required=True)
    a = ap.parse_args()
    sys.path.insert(0, a.pylibs)
    warnings.simplefilter("ignore")
    import pymupdf
    fuentes = json.loads((a.autor / "datos" / "fuentes.json").read_text(encoding="utf-8"))["fuentes"]
    csvf = {r["id"]: r for r in csv.DictReader((a.autor / "datos" / "cifras_fuente.csv").open(encoding="utf-8"), delimiter=";")}
    motores = [("MuPDF", lambda p, n: palabras_mupdf(p, n, pymupdf)), ("pdfminer", palabras_pdfminer), ("PDFium", palabras_pdfium)]
    leidos, difs = {}, 0
    for i in FILAS:
        f = csvf[i]
        pdf = a.raiz / fuentes[f["doc"]]["archivo"]
        print(f"\n{i} · {f['doc']} p.{f['pagina']} · declarado: ejercicio {f['anio']}, etiqueta «{f['etiqueta']}», ocurrencia {f['ocurrencia']}, "
              f"pos {f['pos']}, literal «{f['literal']}», {f['unidad']}, {f['perimetro']}, edición {f['edicion']}, modo {f['control_anio']}")
        for nom, fn in motores:
            ws, alto = fn(pdf, int(f["pagina"]))
            # en la cuenta de resultados la fila «Revenue» es la primera que empieza por esa palabra y lleva cifras
            r = leer(ws, alto, ROTULO[i], int(f["ocurrencia"] or 0), int(f["pos"]))
            if "error" in r:
                print(f"   {nom}: {r['error']}")
                difs += 1
                continue
            igual = r["numero"] == f["literal"]
            difs += 0 if igual else 1
            leidos.setdefault(i, []).append(r["numero"])
            print(f"   {nom:8s}: fila «{r['fila'][:110]}» (filas que casan: {r['filas_que_casan']})")
            print(f"             número «{r['numero']}» {'= literal declarado' if igual else '≠ LITERAL DECLARADO'} · cabecera encima: {r['cabecera_encima']} · "
                  f"año del bloque: {r['anio_del_bloque']}")
            print(f"             unidades: «{(r['unidades'] or '')[:90]}»")
            print(f"             cabecera de página: «{r['cabecera_de_pagina']}» · pie: «{r['pie']}»")
    print(f"\nLecturas: {sum(len(v) for v in leidos.values())}; distintas del literal declarado o sin localizar: {difs}")

    def val(s):
        return Fraction(s.replace(",", ""))

    print("\n== R23 de 2021 y 2022 con las cifras leídas con MuPDF (fracciones exactas) ==")
    for y, a_, b_ in ((2021, "IS_VENTAS_U22_2021", "VENTAS_SEG_U22_2021"), (2022, "IS_VENTAS_U23_2022", "VENTAS_SEG_U23_2022")):
        va, vb = val(leidos[a_][0]), val(leidos[b_][0])
        cota = Fraction(5, 100) * 2
        print(f"   R23 {y}: {leidos[a_][0]} ({csvf[a_]['doc']} p.{csvf[a_]['pagina']}) − {leidos[b_][0]} ({csvf[b_]['doc']} p.{csvf[b_]['pagina']}) = "
              f"{float(va - vb):.1f} · cota de redondeo de dos cifras con un decimal: {float(cota):.2f} · "
              f"{'dentro' if abs(va - vb) <= cota else 'FUERA'}; un error de ±0,1 en una de las dos deja el residuo en ±0,1 = cota: no falla; ±0,2, sí")
    return 0


if __name__ == "__main__":
    sys.exit(main())
