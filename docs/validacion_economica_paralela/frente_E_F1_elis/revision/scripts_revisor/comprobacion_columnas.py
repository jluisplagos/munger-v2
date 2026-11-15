"""Contraste independiente del AÑO de cada cifra de datos/cifras_fuente.csv (revisor; solo lectura).

El verificador del autor comprueba página, etiqueta, posición y literal, pero no que la posición corresponda
al ejercicio declarado en la columna «anio». Este script lo contrasta para las tablas de dos columnas de
ejercicio: localiza la línea de la cifra en un texto paginado propio (pdftotext -layout del PDF completo),
busca hacia arriba la cabecera más próxima con dos ejercicios distintos y comprueba que «anio» es el
ejercicio de la columna elegida (pos −2 = primera columna de ejercicio, pos −1 = segunda).
Las filas que no son de dos columnas (movimientos, tablas por segmento, texto) se listan como «no evaluadas»
para revisión visual.

Uso: python3 -I comprobacion_columnas.py <cifras_fuente.csv> <carpeta_txt>
  <carpeta_txt> contiene URD2021.txt, URD2022.txt, URD2023.txt, DEU2024FR.txt y URD2025.txt
"""
import csv
import re
import sys
import unicodedata
from pathlib import Path

ANIO = re.compile(r"(?<![\d.,/])(20[12]\d)(?![\d.,])")
FECHA = re.compile(r"(?:12/31/|31/12/)(20[12]\d)")


def norm(s):
    return unicodedata.normalize("NFKC", s).replace("’", "'").replace("‘", "'")


def anios_cabecera(linea):
    a = FECHA.findall(linea) or ANIO.findall(linea)
    out = []
    for x in a:
        if x not in out:
            out.append(x)
    return out


def main():
    filas = list(csv.DictReader(open(sys.argv[1], encoding="utf-8"), delimiter=";"))
    carpeta = Path(sys.argv[2])
    paginas = {}
    res = {"coincide": 0, "NO_COINCIDE": [], "no_evaluada": [], "sin_cabecera": [], "linea_no_hallada": []}
    for r in filas:
        if r["tipo"] != "tabla":
            res["no_evaluada"].append((r["id"], "texto"))
            continue
        doc = r["doc"]
        if doc not in paginas:
            paginas[doc] = norm((carpeta / f"{doc}.txt").read_text(encoding="utf-8", errors="replace")).split("\f")
        lineas = paginas[doc][int(r["pagina"]) - 1].splitlines()
        et = r["etiqueta"]
        rx = re.compile(et[3:]) if et.startswith("re:") else None
        idx = [i for i, l in enumerate(lineas) if (rx.search(l) if rx else et in l) and r["literal"] in l]
        if not idx:
            res["linea_no_hallada"].append(r["id"])
            continue
        occ = int(r["ocurrencia"] or 0)
        pos = int(r["pos"])
        if occ != 0 or pos not in (-2, -1):
            res["no_evaluada"].append((r["id"], f"occ={occ} pos={pos}"))
            continue
        i = idx[0]
        cab = None
        for j in range(i - 1, max(-1, i - 80), -1):
            a = anios_cabecera(lineas[j])
            if len(a) >= 2:
                cab = a[:2]
                break
            if len(a) == 1 and j > 0:
                # cabecera partida en dos líneas (p. ej. «2024» encima y «2025  restated*» debajo)
                b = anios_cabecera(lineas[j - 1]) + a
                b = [x for k, x in enumerate(b) if x not in b[:k]]
                if len(b) >= 2:
                    cab = sorted(b[:2], reverse=True)
                    break
        if not cab:
            res["sin_cabecera"].append(r["id"])
            continue
        esperado = cab[0] if pos == -2 else cab[1]
        if esperado == r["anio"]:
            res["coincide"] += 1
        else:
            res["NO_COINCIDE"].append((r["id"], r["anio"], cab, pos, lineas[i].strip()[:120]))
    print("filas:", len(filas))
    print("año de la columna coincide con «anio»:", res["coincide"])
    print("NO COINCIDE:", len(res["NO_COINCIDE"]))
    for x in res["NO_COINCIDE"]:
        print("   ", x)
    print("sin cabecera de dos ejercicios localizable:", len(res["sin_cabecera"]), res["sin_cabecera"][:40])
    print("línea no hallada con mi extracción:", len(res["linea_no_hallada"]), res["linea_no_hallada"][:40])
    print("no evaluadas (texto, movimientos u otras posiciones):", len(res["no_evaluada"]))
    cuenta = {}
    for _id, motivo in res["no_evaluada"]:
        cuenta[motivo] = cuenta.get(motivo, 0) + 1
    print("   ", cuenta)


if __name__ == "__main__":
    main()
