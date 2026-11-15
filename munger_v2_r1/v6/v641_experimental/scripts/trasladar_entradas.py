#!/usr/bin/env python3
"""Traslada las ENTRADAS de un libro V6.3 (o V6.4) a una plantilla V6.4 o V6.4.1 experimental, sin tocar fórmulas (copia en la carpeta de la V6.4.1: inventario con el perímetro).

Uso: python3 -I trasladar_entradas.py LIBRO_ORIGEN.xlsx PLANTILLA_V6.4.xlsx SALIDA.xlsx [--config celdas.json] [--entradas celdas.json] [--sin-config-origen]

- Copia, celda a celda y con el mismo tipo, todas las celdas del inventario de entradas de la V6.3 (v6/scripts/inventario_entradas.py)
  que tienen contenido en el origen; si una celda de entrada del origen tiene fórmula, se copia la fórmula (la V6.3 lo admite como aviso).
- Si el origen ya es V6.4 (tiene la hoja «Configuración V6.4») y no se pide --sin-config-origen, copia también sus entradas de configuración.
- --config celdas.json: {"Configuración V6.4!B4": "Experimental", …} se escribe después (solo celdas de entrada de la V6.4).
- --entradas celdas.json: cambios en otras celdas de ENTRADA (p. ej. palancas de un caso de prueba), con la lista blanca del inventario.
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
import inventario_entradas as INV64  # noqa: E402  (V6.4: V6.3 + Configuración V6.4)


def escribir_formula(libro, hoja, ref, texto):
    c = libro._celda(hoja, ref, crear=True)
    for hijo in list(c):
        c.remove(hijo)
    for k in list(c.attrib):
        if k not in ("r", "s"):
            del c.attrib[k]
    etree.SubElement(c, f"{{{NS}}}f").text = texto
    libro.marcar_modificada(hoja)


def trasladar(origen, plantilla, salida, config=None, con_config_origen=True, otras=None):
    src = LibroV63(origen)
    dst = LibroV63(plantilla)
    entradas = INV64.conjunto_entradas()
    hojas = [h for h in entradas if h != INV64.HOJA_CONFIG or (con_config_origen and h in src.hojas())]
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
    if config:
        permitidas = {INV64.HOJA_CONFIG: entradas[INV64.HOJA_CONFIG]}
        dst.escribir_celdas(config, permitidas)
    if otras:
        dst.escribir_celdas(otras, entradas)
    dst.borrar_caches()
    dst.guardar(salida)
    return n, nf


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(__doc__)
        sys.exit(2)
    cfg = None
    if "--config" in sys.argv:
        cfg = json.load(open(sys.argv[sys.argv.index("--config") + 1], encoding="utf-8"))
    otras = json.load(open(sys.argv[sys.argv.index("--entradas") + 1], encoding="utf-8")) if "--entradas" in sys.argv else None
    n, nf = trasladar(sys.argv[1], sys.argv[2], sys.argv[3], cfg, "--sin-config-origen" not in sys.argv, otras)
    print(f"OK: {n} celdas de entrada trasladadas ({nf} con fórmula) → {sys.argv[3]}")
