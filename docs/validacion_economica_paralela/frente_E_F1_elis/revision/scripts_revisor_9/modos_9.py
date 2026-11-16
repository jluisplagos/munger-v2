"""Revisión independiente n.º 9 · los demás modos de control del ejercicio (frente E · F1 · Elis). No modifica nada del autor.

Entre C16 y C18, fuera del modo «dos_columnas», el resultado de una fila solo puede cambiar por dos caminos del código:
`token_del_rotulo` (se aplica en todos los modos) y `zona_de_cabecera` (cambia `es_encabezado_numerado`); el perímetro y la
unidad no dependen del modo y ya están en barrido_9.py. Este script toma del barrido los tokens por los que pasa alguno de
los dos caminos (el token tiene motivo en `token_del_rotulo`, o la zona de cabecera de su línea cambia) y los evalúa con
`comprobar_tabla` de C16 y de C18 con los 15 identificadores de sondeo de arnes9.PERFILES y los tres ejercicios.

Uso: python3 -I -B modos_9.py --todas <jsonl.gz> --raiz <munger_v2_r1> --c16 <frente C17> --c18 <frente C19>
"""
import argparse
import gzip
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import arnes9 as H  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--todas", required=True, type=Path)
    ap.add_argument("--raiz", required=True, type=Path)
    ap.add_argument("--c16", required=True, type=Path)
    ap.add_argument("--c18", required=True, type=Path)
    a = ap.parse_args()
    A, N = H.Version("C16", a.c16, a.raiz), H.Version("C18", a.c18, a.raiz)
    sel = []
    with gzip.open(a.todas, "rt", encoding="utf-8") as f:
        for l in f:
            r = json.loads(l)
            for x in r["toks"]:
                if x["tdr"] or "zona" in r:
                    sel.append((r["doc"], r["p"], r["i"], x["k"], x["tok"], bool(x["tdr"]), "zona" in r, r["rot"]))
    print("Los demás modos de control del ejercicio · C16 → C18 · tokens por los que pasa `token_del_rotulo` o un cambio de zona de cabecera")
    print(f"Tokens: {len(sel)} ({sum(1 for s in sel if s[5])} con motivo de `token_del_rotulo`; {sum(1 for s in sel if s[6])} en líneas cuya zona cambia)")
    por_modo, dejan, ej = {}, [], Counter()
    for doc, pag, i, k, tok, con_tdr, con_zona, rot in sel:
        idioma, E = N.idioma(doc), N.publicacion(doc)
        L = N.lineas(doc, pag)
        n = len(N.V.tokens_numericos(L[i], idioma))
        val = N.V.valor(tok, idioma)
        unidad = "%" if "%" in tok else "mm EUR"
        for idf, modo in H.PERFILES:
            if modo == "crecimiento" and "%" not in tok:
                continue
            for y in (E, E - 1, E - 2):
                f = H.declarar(doc, pag, L, i, k, n, tok, val, y, idf, modo, unidad, H.GRUPO, N.edicion_posible(modo, y, doc))
                ca, cn = H.codigo(A.tabla(f)), H.codigo(N.tabla(f))
                c = por_modo.setdefault(idf, Counter())
                c[(H.estado(ca), H.estado(cn))] += 1
                if ca[1] != cn[1]:
                    ej[(modo, ca[1], cn[1])] += 1
                if H.estado(ca) == "OK" and H.estado(cn) != "OK":
                    dejan.append((idf, doc, pag, i, tok, y, ca, cn, rot))
                if H.estado(cn) == "OK" and H.estado(ca) != "OK":
                    print(f"  PASA A OK: {idf} {doc} p.{pag} l.{i + 1} «{tok}» {y}: {ca} → {cn}")
    print("Estado de la fila por identificador de sondeo (C16 → C18):")
    for idf, c in por_modo.items():
        print(f"  {idf}: {dict(sorted(c.items()))}")
    print(f"Cambios de la dimensión «ejercicio» por modo: {dict(sorted(ej.items()))}")
    print(f"Candidatas que dejan de ser OK: {len(dejan)}; ninguna pasa a OK: {not any(1 for c in por_modo.values() for (ea, en), v in c.items() if en == 'OK' and ea != 'OK')}")
    for idf, doc, pag, i, tok, y, ca, cn, rot in dejan:
        print(f"  {idf} · {doc} p.{pag} l.{i + 1} · «{tok}» declarado {y}: {ca} → {cn} · rótulo «{re.sub(chr(92) + 's{2,}', '  ', rot)[:80]}»")
    return 0


if __name__ == "__main__":
    sys.exit(main())
