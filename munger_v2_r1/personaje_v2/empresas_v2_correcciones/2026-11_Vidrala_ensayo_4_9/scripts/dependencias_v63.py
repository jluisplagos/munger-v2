#!/usr/bin/env python3
"""Rastreo de dependencias de un libro V6.3 (entrega 4.9, N4). Solo lectura.

Uso: python3 -I dependencias_v63.py LIBRO.xlsx CELDA [CELDA …] [--salidas Hoja!A1,…]

Construye el grafo de fórmulas de todas las hojas (referencias con o sin hoja, rangos y nombres de hoja entre comillas) y lista,
para cada celda semilla, las celdas con fórmula que dependen de ella (directa o indirectamente) y cuáles de las salidas indicadas
alcanza. Los valores escritos por scripts (no fórmulas) no son dependencias del libro: los rastrea n4_investigacion.py aparte.
Límite declarado: no evalúa INDIRECT ni OFFSET (si aparecen, se señalan) y expande cada rango hasta 5.000 celdas.
"""
import json
import re
import sys
from collections import defaultdict, deque

import openpyxl
from openpyxl.formula import Tokenizer
from openpyxl.utils import column_index_from_string, get_column_letter, range_boundaries

LIMITE_RANGO = 5000


def _norm(hoja, ref):
    return f"{hoja}!{ref.replace('$', '').upper()}"


def _expandir(hoja, ref):
    ref = ref.replace("$", "")
    if ":" not in ref:
        return [_norm(hoja, ref)]
    try:
        c1, f1, c2, f2 = range_boundaries(ref)
    except ValueError:
        return []
    if None in (c1, f1, c2, f2) or (c2 - c1 + 1) * (f2 - f1 + 1) > LIMITE_RANGO:
        return []
    return [f"{hoja}!{get_column_letter(c)}{f}" for c in range(c1, c2 + 1) for f in range(f1, f2 + 1)]


def referencias(formula, hoja):
    """Celdas referidas por una fórmula (lista de «Hoja!A1»)."""
    out, avisos = [], []
    try:
        tok = Tokenizer(formula)
    except Exception:  # noqa
        return out, ["fórmula no analizable"]
    for t in tok.items:
        if t.type == "OPERAND" and t.subtype == "RANGE":
            v = t.value
            if "!" in v:
                h, r = v.rsplit("!", 1)
                h = h.strip("'").replace("''", "'")
            else:
                h, r = hoja, v
            if re.fullmatch(r"\$?[A-Z]{1,3}\$?\d+(:\$?[A-Z]{1,3}\$?\d+)?", r.upper()):
                out += _expandir(h, r)
        if t.type == "FUNC" and t.value.upper().startswith(("INDIRECT", "OFFSET")):
            avisos.append(t.value.rstrip("("))
    return out, avisos


def grafo(libro):
    wb = openpyxl.load_workbook(libro, data_only=False)
    dependientes = defaultdict(set)
    avisos = defaultdict(list)
    formulas = {}
    for ws in wb:
        for fila in ws.iter_rows():
            for c in fila:
                v = c.value
                if isinstance(v, str) and v.startswith("="):
                    clave = f"{ws.title}!{c.coordinate}"
                    formulas[clave] = v
                    refs, av = referencias(v, ws.title)
                    for r in refs:
                        dependientes[r].add(clave)
                    if av:
                        avisos[clave] += av
    return dependientes, formulas, avisos


def alcanzadas(dependientes, semillas):
    vistos, cola = set(), deque(semillas)
    while cola:
        x = cola.popleft()
        for d in dependientes.get(x, ()):
            if d not in vistos:
                vistos.add(d)
                cola.append(d)
    return vistos


def main():
    args = sys.argv[1:]
    salidas = []
    if "--salidas" in args:
        i = args.index("--salidas")
        salidas = args[i + 1].split(",")
        args = args[:i] + args[i + 2:]
    libro, semillas = args[0], args[1:]
    dep, formulas, avisos = grafo(libro)
    res = {}
    for s in semillas:
        a = alcanzadas(dep, _expandir(*s.split("!", 1)))
        res[s] = {"n_dependientes": len(a), "salidas_alcanzadas": [x for x in salidas if x in a], "por_hoja": {h: sum(1 for x in a if x.startswith(h + "!")) for h in sorted({x.split("!")[0] for x in a})}}
    print(json.dumps({"libro": libro, "n_formulas": len(formulas), "avisos_indirect_offset": len(avisos), "semillas": res}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
