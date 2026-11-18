#!/usr/bin/env python3
"""Traslada las ENTRADAS de un libro V6.3 (o V6.3.1 F1) a una plantilla V6.3 o V6.3.1 F1, sin tocar fórmulas (copia de la de la V6.4.1 en la
carpeta de la V6.3.1 F1: inventario con el perímetro F1; sin hoja de configuración).

Uso: python3 -I trasladar_entradas.py LIBRO_ORIGEN.xlsx PLANTILLA.xlsx SALIDA.xlsx [--entradas celdas.json]

- Copia, celda a celda y con el mismo tipo, todas las celdas del inventario de entradas de la V6.3 (v6/scripts/inventario_entradas.py)
  que tienen contenido en el origen; si una celda de entrada del origen tiene fórmula, se copia la fórmula (la V6.3 lo admite como aviso).
- Con un origen V6.3 las celdas del perímetro F1 (Historia C85:L87, M85:S87) están vacías y no se copian: el destino queda con el perímetro
  vacío (= A0, la V6.3).
- --entradas celdas.json: cambios en otras celdas de ENTRADA (p. ej. {"Historia!C85": "A1_sin_ROU", "Historia!C86": 12.3}), con la lista blanca
  del inventario de la V6.3.1 F1.
- Escribe con v63_xml.LibroV63 (XML; conserva controles, gráficos y estilos) y borra las cachés de fórmula para forzar el recálculo.
Es la herramienta de las pruebas de regresión y de las réplicas (mismas entradas → mismo libro); el pipeline construye los libros
por su ruta normal (migración, fase 1 y fases).
"""
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", "..", ".."))
sys.path.insert(0, os.path.join(RAIZ, "personaje_v2", "scripts"))
from v63_xml import NS, LibroV63  # noqa: E402
from lxml import etree  # noqa: E402

sys.path.insert(0, AQUI)
import inventario_entradas as INV  # noqa: E402  (V6.3.1 F1: V6.3 + perímetro F1)


def escribir_formula(libro, hoja, ref, texto):
    c = libro._celda(hoja, ref, crear=True)
    for hijo in list(c):
        c.remove(hijo)
    for k in list(c.attrib):
        if k not in ("r", "s"):
            del c.attrib[k]
    etree.SubElement(c, f"{{{NS}}}f").text = texto
    libro.marcar_modificada(hoja)


def trasladar(origen, plantilla, salida, otras=None):
    src = LibroV63(origen)
    dst = LibroV63(plantilla)
    entradas = INV.conjunto_entradas()
    hojas = list(entradas)
    n, nf = 0, 0
    for hoja in hojas:
        if hoja not in src.hojas():
            continue
        valores = src.todas_las_celdas(hoja)
        for ref in sorted(entradas[hoja]):
            v = valores.get(ref)
            if v is None:
                continue
            if isinstance(v, tuple) and v and v[0] == "=":
                escribir_formula(dst, hoja, ref, v[1])
                nf += 1
            else:
                if isinstance(v, bool):
                    raise TypeError(f"{hoja}!{ref}: booleano en una celda de entrada")
                dst.escribir(hoja, ref, v, tipo="texto" if isinstance(v, str) else None)
                dst.marcar_modificada(hoja)
            n += 1
    if otras:
        dst.escribir_celdas(otras, entradas)
    dst.borrar_caches()
    dst.guardar(salida)
    return n, nf


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(__doc__)
        sys.exit(2)
    otras = json.load(open(sys.argv[sys.argv.index("--entradas") + 1], encoding="utf-8")) if "--entradas" in sys.argv else None
    n, nf = trasladar(sys.argv[1], sys.argv[2], sys.argv[3], otras)
    print(f"OK: {n} celdas de entrada trasladadas ({nf} con fórmula) → {sys.argv[3]}")
