#!/usr/bin/env python3
"""Compara los VALORES calculados de dos libros recalculados, celda a celda, en las once hojas de la V6.3 (copia de la de la V6.3.1 F1 para la
V6.3.2 F1: todas las columnas; se excluyen las etiquetas de versión y las filas de la Historia que no existen en el libro con el que se compara).

Uso: python3 -I comparar_libros.py A_recalculado.xlsx B_recalculado.xlsx [--tol 1e-12] [--hojas H1,H2] [--excluir Hoja!A1,…] [--json salida.json]
Números: |a − b| ≤ tol × max(1, |a|) (con --tol 0, igualdad exacta); texto, booleanos y vacíos: iguales. Código 0 si no hay diferencias; 1 si las hay.
Por defecto excluye SOLO las cuatro etiquetas de versión (Análisis!A1, Panel!A1, Guía V6!A1, Control maestro!A3) y la sección nueva de la
V6.3.2 F1 (Historia A91:S98, que no existe en la V6.3.1 F1). comparar(…, filas_nuevas=range(84, 99)) excluye además la de la V6.3.1 F1 (A84:S90),
para comparar con la V6.3.
"""
import json
import sys

from openpyxl import load_workbook

HOJAS_V63 = ["Panel", "Análisis", "Palancas", "Diagnóstico V6", "Historia", "Sector", "Riesgo país", "Guía V6", "Opciones", "Control maestro", "Motor"]
ETIQUETAS = {"Análisis!A1", "Panel!A1", "Guía V6!A1", "Control maestro!A3"}
FILAS_V632 = range(91, 99)    # sección de la V6.3.2 F1 (normalización del circulante)
FILAS_V631 = range(84, 99)    # además, la de la V6.3.1 F1 (perímetro F1): para comparar con la V6.3


def _excluidas(filas):
    return ETIQUETAS | {f"Historia!{c}{r}" for r in filas for c in "ABCDEFGHIJKLMNOPQRS"}


EXCLUIR = _excluidas(FILAS_V632)


def valores(path, hojas):
    wb = load_workbook(path, data_only=True)
    out = {}
    for h in hojas:
        ws = wb[h]
        for row in ws.iter_rows():
            for c in row:
                out[f"{h}!{c.coordinate}"] = c.value
    return out


def igual(a, b, tol):
    if isinstance(a, bool) or isinstance(b, bool):
        return a == b
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return abs(a - b) <= tol * max(1.0, abs(a))
    na = a in (None, "")
    nb = b in (None, "")
    if na or nb:
        return na and nb
    return a == b


def comparar(a, b, tol=1e-12, hojas=None, excluir=None, filas_nuevas=FILAS_V632):
    hojas = hojas or HOJAS_V63
    excluir = _excluidas(filas_nuevas) | set(excluir or ())
    va, vb = valores(a, hojas), valores(b, hojas)
    dif = []
    for k in sorted(set(va) | set(vb)):
        if k in excluir:
            continue
        x, y = va.get(k), vb.get(k)
        if not igual(x, y, tol):
            dif.append((k, x, y))
    return dif, len(set(va) | set(vb))


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(2)
    tol = float(sys.argv[sys.argv.index("--tol") + 1]) if "--tol" in sys.argv else 1e-12
    hojas = sys.argv[sys.argv.index("--hojas") + 1].split(",") if "--hojas" in sys.argv else None
    exc = sys.argv[sys.argv.index("--excluir") + 1].split(",") if "--excluir" in sys.argv else None
    dif, n = comparar(sys.argv[1], sys.argv[2], tol, hojas, exc)
    print(f"{n} celdas comparadas · {len(dif)} diferencias (tolerancia {tol:g})")
    for k, x, y in dif[:40]:
        print(f"  {k}: {x!r} ≠ {y!r}")
    if "--json" in sys.argv:
        json.dump({"celdas": n, "diferencias": [[k, str(x), str(y)] for k, x, y in dif]}, open(sys.argv[sys.argv.index("--json") + 1], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    sys.exit(0 if not dif else 1)
