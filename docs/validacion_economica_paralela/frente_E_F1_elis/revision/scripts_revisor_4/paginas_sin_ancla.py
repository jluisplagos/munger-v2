"""Páginas de fuente sin ninguna entrada contrastada entre páginas (revisión n.º 4, objeción P3). Solo lectura.

Lee la tabla «cobertura_entradas» de resultados/contraste_f1.json del autor y agrupa las entradas usadas por documento y
página. Una identidad de la misma página acredita la coherencia interna de una tabla, no su unidad ni su perímetro: en las
páginas sin ninguna entrada contrastada entre páginas, esos dos campos descansan en las reglas del verificador y en la
lectura.

Uso: python3 -I paginas_sin_ancla.py --contraste <ruta>/resultados/contraste_f1.json
"""
import argparse
import collections
import json
import re


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--contraste", required=True)
    a = ap.parse_args()
    k = json.load(open(a.contraste, encoding="utf-8"))
    ce = k["tablas"]["cobertura_entradas"]
    print("Clases declaradas por el contraste:", ce["resumen"])
    pag = collections.defaultdict(collections.Counter)
    ids = collections.defaultdict(list)
    for i, e in ce["entradas"].items():
        m = re.match(r"(\S+) p\.(\d+)", e["fuente"])
        clave = (m.group(1), int(m.group(2)))
        pag[clave][e["estado"]] += 1
        ids[clave].append(i)
    entre = "contrastada entre páginas"
    sin = {p: c for p, c in pag.items() if c[entre] == 0}
    print(f"Páginas con entradas usadas: {len(pag)} · sin ninguna entrada contrastada entre páginas: {len(sin)}")
    tot = collections.Counter()
    for p, c in sorted(sin.items()):
        tot.update(c)
        print(f"  {p[0]} p.{p[1]}: {dict(c)} · {', '.join(sorted(ids[p]))[:150]}")
    print("Entradas en esas páginas, por clase:", dict(tot), "· total:", sum(tot.values()))
    misma = "solo identidad de la misma página"
    print(f"Entradas «{misma}» en páginas que sí tienen alguna entrada contrastada entre páginas: "
          f"{sum(c[misma] for p, c in pag.items() if c[entre])} de {ce['resumen'][misma]}")


if __name__ == "__main__":
    main()
