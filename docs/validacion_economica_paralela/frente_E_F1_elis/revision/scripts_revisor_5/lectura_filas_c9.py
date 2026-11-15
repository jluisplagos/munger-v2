"""Revisión n.º 5 (frente E · F1 · Elis). Lectura independiente de las siete filas nuevas de C9 y de la afirmación [P] sobre
las adquisiciones de 2021. No modifica nada del autor.

No usa pdftotext, que es la herramienta del autor. Lee cada página con dos motores distintos:

  pdfminer (pdfplumber)  palabras con su caja; las filas se reconstruyen por la coordenada vertical y la columna de cada
                         número se identifica por la cabecera cuyo borde derecho está más cerca del suyo;
  PDFium (pypdfium2)     texto en orden de lectura: el rótulo debe ir seguido de los mismos números, en el mismo orden.

Para cada fila compara con datos/cifras_fuente.csv del autor: literal, valor con signo, posición del token, cabecera de la
columna (ejercicio), declaración de unidades de la tabla, cabecera de la página (perímetro) y pie (edición). Después
recalcula las tres identidades de C9 con fracciones exactas y su cota de redondeo.

Uso: python3 -I lectura_filas_c9.py --raiz <ruta>/munger_v2_r1 --autor <carpeta frente_E_F1_elis del commit congelado>
"""
import argparse
import csv
import json
import re
import sys
from fractions import Fraction
from pathlib import Path

import pdfplumber
import pypdfium2 as pdfium

NUM = re.compile(r"^\(?[+\-–−]?\d{1,3}(?:,\d{3})*(?:\.\d+)?\)?%?$")
GUION = {"-", "–", "—", "−"}


def valor(tok):
    neg = tok.startswith("(") or tok[:1] in "-–−"
    v = Fraction(re.sub(r"[^\d.]", "", tok))
    return -v if neg else v


def lineas_pdfminer(pdf, pagina):
    """Filas de la página: lista de listas de palabras (x0, x1, top, texto), de arriba abajo y de izquierda a derecha."""
    with pdfplumber.open(pdf) as doc:
        pg = doc.pages[pagina - 1]
        palabras = pg.extract_words(x_tolerance=1.5, y_tolerance=2, keep_blank_chars=False)
    filas = []
    for w in sorted(palabras, key=lambda w: (w["bottom"], w["x0"])):
        # la línea se identifica por el borde inferior: los superíndices («(a)») tienen otro borde superior
        if filas and abs(filas[-1][0]["bottom"] - w["bottom"]) <= 2.5:
            filas[-1].append(w)
        else:
            filas.append([w])
    return [sorted(f, key=lambda w: w["x0"]) for f in filas]


def texto(fila):
    return " ".join(w["text"] for w in fila)


def texto_pdfium(pdf, pagina):
    doc = pdfium.PdfDocument(str(pdf))
    tp = doc[pagina - 1].get_textpage()
    return tp.get_text_range()


def leer(pdf, pagina, rotulo, ocurrencia=1):
    """Fila cuyo texto empieza por el rótulo: números en orden, cada uno con la cabecera que tiene encima."""
    filas = lineas_pdfminer(pdf, pagina)
    cand = [k for k, f in enumerate(filas) if texto(f).startswith(rotulo) and any(NUM.match(w["text"]) or w["text"] in GUION for w in f)]
    if len(cand) < ocurrencia:
        return None
    k = cand[ocurrencia - 1]
    fila = filas[k]
    # declaración de unidades más próxima por encima
    ku = next((j for j in range(k - 1, -1, -1) if re.search(r"\((?:[Ii]n|en) millions?", texto(filas[j]))), None)
    nums = [w for w in fila if NUM.match(w["text"]) or w["text"] in GUION]
    cab = []
    if ku is not None:
        # Zona de cabecera: la línea de unidades, las líneas pegadas encima (cabeceras partidas: «12/31/2021» sobre
        # «restated») y las que hay debajo hasta la primera fila con un número con decimales (cabeceras bajo la línea de
        # unidades, como en la tabla de reexpresión). Cada grupo de palabras contiguas de una línea es una celda.
        arriba = [j for j in range(max(0, ku - 3), ku) if filas[ku][0]["bottom"] - filas[j][0]["bottom"] <= 16]
        abajo = []
        for j in range(ku + 1, k):
            if any(re.search(r"\d\.\d", w["text"]) for w in filas[j]):
                break
            abajo.append(j)
        celdas = []
        for j in arriba + [ku] + abajo:
            for w in filas[j]:
                if celdas and celdas[-1]["j"] == j and w["x0"] - celdas[-1]["x1"] < 3.5:
                    celdas[-1]["x1"], celdas[-1]["text"] = w["x1"], celdas[-1]["text"] + " " + w["text"]
                else:
                    celdas.append({"j": j, "x0": w["x0"], "x1": w["x1"], "top": w["top"], "text": w["text"]})
        celdas = [c for c in celdas if not re.match(r"\((?:[Ii]n|en) millions?", c["text"])]
        for n in nums:
            centro = (n["x0"] + n["x1"]) / 2
            sobre = [c for c in celdas if abs(c["x1"] - n["x1"]) <= 16 or c["x0"] - 3 <= centro <= c["x1"] + 3]
            sobre.sort(key=lambda c: (c["top"], c["x0"]))
            cab.append(" ".join(c["text"] for c in sobre) or "?")
    else:
        cab = ["?"] * len(nums)
    no_vacias = [f for f in filas if texto(f).strip()]
    pie = next((texto(f) for f in reversed(no_vacias) if re.search(r"Universal Registration Document|Document d'enregistrement", texto(f))), "?")
    # título más próximo por encima de la tabla (línea corta sin números)
    tit = "?"
    if ku is not None:
        for j in range(ku - 1, max(-1, ku - 8), -1):
            t = texto(filas[j])
            if t.strip() and not re.search(r"\d", t) and len(t) < 70 and filas[ku][0]["top"] - filas[j][0]["top"] > 12:
                tit = t
                break
    return {"rotulo": texto([w for w in fila if w not in nums]), "numeros": [n["text"] for n in nums], "cabeceras": cab,
            "unidad": texto(filas[ku]) if ku is not None else "?", "titulo": tit,
            "cabecera_pagina": " / ".join(texto(f) for f in no_vacias[:2]), "pie": pie}


def secuencia_pdfium(pdf, pagina, rotulo, numeros):
    """¿Aparece en el texto de PDFium el rótulo seguido de esos números, en ese orden, sin otro número en medio?"""
    t = re.sub(r"\s+", " ", texto_pdfium(pdf, pagina))
    # entre el rótulo y los importes puede ir una referencia a notas con barras («3.1/4.1/4.2»), que no es un importe
    patron = (re.escape(rotulo) + r"[^\d(]{0,80}?(?:\d+(?:\.\d+)?(?:/\d+(?:\.\d+)?)+\s*)?"
              + r"\s*".join(re.escape(n) + r"(?!\d)" for n in numeros))
    return bool(re.search(patron, t))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raiz", required=True, type=Path)
    ap.add_argument("--autor", required=True, type=Path)
    a = ap.parse_args()
    fuentes = json.loads((a.autor / "datos" / "fuentes.json").read_text(encoding="utf-8"))["fuentes"]
    csvf = {r["id"]: r for r in csv.DictReader((a.autor / "datos" / "cifras_fuente.csv").open(encoding="utf-8"), delimiter=";")}
    pdf = {k: a.raiz / v["archivo"] for k, v in fuentes.items()}
    fallos = 0

    def caso(titulo, doc, pagina, rotulo, esperado, col, anio_cab, idf=None, ocurrencia=1, notas=0):
        """esperado: literal; col: índice del número en la fila (sin contar las «notas» iniciales); anio_cab: texto que
        debe llevar la cabecera de esa columna."""
        nonlocal fallos
        r = leer(pdf[doc], pagina, rotulo, ocurrencia)
        print(f"\n{titulo}\n   {doc} p.{pagina} · rótulo «{rotulo}»")
        if r is None:
            print("   NO ENCONTRADA")
            fallos += 1
            return None
        nums, cabs = r["numeros"][notas:], r["cabeceras"][notas:]
        print(f"   números (pdfminer): {nums}")
        print(f"   cabeceras:          {cabs}")
        print(f"   unidad: «{r['unidad'][:70]}» · título: «{r['titulo'][:60]}»")
        print(f"   página: «{r['cabecera_pagina'][:110]}» · pie: «{r['pie'][-50:]}»")
        ok_lit = nums[col] == esperado
        ok_cab = anio_cab in cabs[col]
        ok_pdfium = secuencia_pdfium(pdf[doc], pagina, rotulo, r["numeros"])
        ok_unidad = bool(re.search(r"\((?:[Ii]n|en) millions? of euros\)|\(en millions d'euros\)", r["unidad"]))
        ok_grupo = bool(re.search(r"Consolidated financial statements|Group results", r["cabecera_pagina"]))
        linea = [f"literal {'OK' if ok_lit else 'DISTINTO'} («{nums[col]}»)", f"columna {'OK' if ok_cab else 'DISTINTA'} («{cabs[col]}»)",
                 f"PDFium {'OK' if ok_pdfium else 'NO COINCIDE'}", f"unidad {'OK' if ok_unidad else '?'}", f"página del grupo {'OK' if ok_grupo else '?'}"]
        if idf:
            f = csvf[idf]
            pos = int(f["pos"])
            n_tot = len(r["numeros"])
            # el autor cuenta todos los tokens numéricos de la línea, incluidas las referencias a notas
            idx_autor = pos if pos >= 0 else n_tot + pos
            ok_csv = (f["literal"] == esperado and Fraction(f["valor_publicado"]) == valor(esperado) and int(f["pagina"]) == pagina
                      and f["doc"] == doc and idx_autor == col + notas)
            linea.append(f"CSV del autor {'OK' if ok_csv else 'DISTINTO'} (pos {pos} de {n_tot}; {f['anio']}; {f['unidad']}; {f['perimetro']}; {f['edicion']})")
            if not ok_csv:
                fallos += 1
        if not (ok_lit and ok_cab and ok_pdfium and ok_unidad and ok_grupo):
            fallos += 1
        print("   → " + " · ".join(linea))
        return valor(nums[col])

    print("A. Las siete filas nuevas de C9, leídas con pdfminer y PDFium")
    tc21 = caso("A1 TAX_CORR_U22_2021 · impuesto corriente de 2021 (nota 9)", "URD2022", 326, "Current taxes", "81.4", 1, "12/31/2021", "TAX_CORR_U22_2021")
    td21 = caso("A2 TAX_DIF_U22_2021 · impuesto diferido de 2021 (nota 9)", "URD2022", 326, "Deferred taxes", "(24.8)", 1, "12/31/2021", "TAX_DIF_U22_2021")
    an21 = caso("A3 CF_ADQ_NOTA_U22_2021 · flujo neto de las adquisiciones de 2021 (nota 2.4, columna del total)", "URD2022", 277, "Net cash flow", "(86.8)", 0, "12/31/2021", "CF_ADQ_NOTA_U22_2021")
    tc22 = caso("A4 TAX_CORR_U23_2022 · impuesto corriente de 2022 reexpresado (nota 9)", "URD2023", 345, "Current taxes", "92.6", 1, "2022", "TAX_CORR_U23_2022")
    td22 = caso("A5 TAX_DIF_U23_2022 · impuesto diferido de 2022 reexpresado (nota 9)", "URD2023", 345, "Deferred taxes", "(12.9)", 1, "2022", "TAX_DIF_U23_2022")
    an22 = caso("A6 CF_ADQ_NOTA_U23_2022 · flujo neto de las adquisiciones de 2022 (nota 2.4, columna del total)", "URD2023", 294, "NET CASH FLOW", "(221.7)", 0, "2022", "CF_ADQ_NOTA_U23_2022")
    v20m = caso("A7 IS_VENTAS_MR_U21_2020 · ventas de 2020 en el informe de gestión", "URD2021", 213, "Revenue", "2,806.3", 1, "2020", "IS_VENTAS_MR_U21_2020")

    print("\n\nB. Las entradas que esas filas contrastan")
    i21 = caso("B1 IS_IMP_U22_2021 · gasto por impuesto de 2021 (cuenta de resultados)", "URD2022", 258, "Tax", "(56.6)", 1, "12/31/2021", "IS_IMP_U22_2021", notas=1)
    i22 = caso("B2 IS_IMP_U23_2022 · gasto por impuesto de 2022 reexpresado (cuenta de resultados)", "URD2023", 276, "Tax", "(79.7)", 1, "2022", "IS_IMP_U23_2022", notas=1)
    a21 = caso("B3 CF_ADQ_U22_2021 · adquisiciones de 2021 (EFE)", "URD2022", 261, "Acquisition of subsidiaries, net of cash acquired", "(86.8)", 1, "12/31/2021", "CF_ADQ_U22_2021", notas=1)
    a22 = caso("B4 CF_ADQ_U23_2022 · adquisiciones de 2022 reexpresadas (EFE)", "URD2023", 279, "Acquisition of subsidiaries, net of cash acquired", "(221.7)", 1, "2022", "CF_ADQ_U23_2022", notas=1)
    v20 = caso("B5 IS_VENTAS_U21_2020 · ventas de 2020 (cuenta de resultados)", "URD2021", 226, "Revenue", "2,806.3", 1, "12/31/2020", "IS_VENTAS_U21_2020")

    print("\n\nC. La afirmación [P] sobre las adquisiciones de 2021 en el URD 2022")
    g = caso("C1 informe de gestión, p.247, flujos de inversión: columna «2021 restated»", "URD2022", 247, "Acquisition of subsidiaries, net of cash acquired", "(86.9)", 1, "2021")
    caso("C2 informe de gestión, p.247: total de los flujos de inversión, columna «2021 restated»", "URD2022", 247, "NET CASH FROM INVESTING ACTIVITIES", "(655.4)", 1, "2021")
    pub = caso("C3 tabla de reexpresión, p.271: columna «12/31/2021 published»", "URD2022", 271, "Acquisition of subsidiaries, net of cash acquired", "(86.9)", 0, "published")
    aj = caso("C4 tabla de reexpresión, p.271: columna «IFRS 3»", "URD2022", 271, "Acquisition of subsidiaries, net of cash acquired", "0.1", 1, "IFRS")
    rex = caso("C5 tabla de reexpresión, p.271: columna «12/31/2021 restated»", "URD2022", 271, "Acquisition of subsidiaries, net of cash acquired", "(86.8)", 2, "restated")
    caso("C6 tabla de reexpresión, p.271: total de inversión publicado", "URD2022", 271, "NET CASH FLOWS FROM INVESTING ACTIVITIES", "(655.4)", 0, "published")
    caso("C7 EFE, p.261: total de inversión reexpresado", "URD2022", 261, "NET CASH FLOWS FROM INVESTING ACTIVITIES", "(655.3)", 1, "12/31/2021")
    caso("C8 EFE del URD 2021, p.229: adquisiciones de 2021 tal como se publicaron", "URD2021", 229, "Acquisition of subsidiaries, net of cash acquired", "(86.9)", 0, "12/31/2021", notas=1)
    caso("C9 nota 2.4 del URD 2021, p.242: flujo neto de las adquisiciones de 2021 tal como se publicó", "URD2021", 242, "NET CASH FLOW", "(86.9)", 0, "12/31/2021")
    caso("C10 nota 2.4 del URD 2021, p.242: columna de Irlanda tal como se publicó", "URD2021", 242, "NET CASH FLOW", "(13.5)", 8, "Ireland")
    caso("C11 nota 2.4 del URD 2022, p.277: columna de Irlanda reexpresada", "URD2022", 277, "Net cash flow", "(13.4)", 8, "Ireland")

    print("\n\nD. Identidades de C9, con fracciones exactas (cota = media unidad de la última cifra de cada cifra que interviene)")
    m = Fraction(1, 20)

    def identidad(nombre, residuo, n_cifras, esperado=Fraction(0)):
        nonlocal fallos
        cota = n_cifras * m
        ok = abs(residuo - esperado) <= cota
        fallos += 0 if ok else 1
        print(f"   {nombre}: residuo {float(residuo):+.1f} · cota {float(cota):.2f} · {'dentro' if ok else 'FUERA'}")

    if None not in (tc21, td21, i21, tc22, td22, i22, an21, a21, an22, a22, v20, v20m, g, pub, aj, rex):
        identidad("R17 2021  corriente + diferido − gasto            81,4 + (−24,8) − 56,6", tc21 + td21 - (-i21), 3)
        identidad("R17 2022  corriente + diferido − gasto            92,6 + (−12,9) − 79,7", tc22 + td22 - (-i22), 3)
        identidad("R39 2021  EFE − nota 2.4                          86,8 − 86,8", (-a21) - (-an21), 2)
        identidad("R39 2022  EFE − nota 2.4                          221,7 − 221,7", (-a22) - (-an22), 2)
        identidad("R40       ventas 2020: cuenta − informe de gestión 2.806,3 − 2.806,3", v20 - v20m, 2)
        print("\n   Afirmación [P]: publicado + ajuste IFRS 3 = reexpresado")
        identidad("   (86,9) + 0,1 − (86,8)", pub + aj - rex, 3)
        print(f"   informe de gestión p.247, «2021 restated»: {float(g):.1f} = publicado {float(pub):.1f} ≠ reexpresado {float(rex):.1f}")
        print("\n   Límite de R39: con la cifra publicada (86,9) en lugar de la reexpresada (86,8) en el EFE de 2021")
        r = Fraction("86.9") - (-an21)
        print(f"   residuo {float(r):+.1f} · cota 0,10 · {'dentro: R39 no lo distingue' if abs(r) <= 2 * m else 'fuera: R39 lo detecta'}")
    print(f"\nCasos con alguna diferencia: {fallos}")
    return 1 if fallos else 0


if __name__ == "__main__":
    sys.exit(main())
