"""Inventario de las celdas que el usuario (o un script de relleno) puede escribir en la V6.4 EXPERIMENTAL.

Es el de la V6.3 (v6/scripts/inventario_entradas.py, sin cambios) más las entradas de la hoja nueva «Configuración V6.4».
Todo lo que NO esté aquí es parte fija de la plantilla: fórmulas, etiquetas, tablas y parámetros de diseño. El verificador
(verificar_v64.py) compara esas celdas con la referencia aprobada de la V6.4 de forma exacta.

Este módulo tiene el MISMO nombre que el de la V6.3 a propósito: los scripts del personaje lo importan desde
config → plantilla.scripts_v63, así que con la configuración experimental (config_v2_v64_experimental.json) reciben
este inventario y con la heredada (config_v2.json), el de la V6.3.
"""
from openpyxl.utils import range_boundaries

HOJA_CONFIG = "Configuración V6.4"
HOJA_CONCILIACION = "Conciliación B"

ENTRADAS = {
    "Análisis": ["B3", "D3", "B4", "D4", "C11:C14", "C17:C20", "C24:C28", "C31:C34", "C37", "C38",
                 "C40:C42", "C46:C51", "C53:C57", "C60:C62", "B65:D66", "B68:D69", "C76", "C88",
                 "C93", "C96:C98", "B101", "B102", "C103", "C104"],
    "Historia": ["C5:L26", "C57", "M5:S26"],   # M:S = notas de fuente por fila
    "Palancas": ["C5:C10", "B14:D16", "B18:D18", "C22:C24", "A28:B33", "A38:C40", "C43:C48"],
    "Control maestro": ["H4", "J4", "L4", "N4", "B5", "D5", "F5", "J5", "L5", "N5",
                        "E17:N82", "C86:E102", "E107:N175"],
    "Panel": ["C6", "F6", "E20:E25"],
    "Diagnóstico V6": ["C91:C94", "C158", "C179", "B222:C223"],
    # V6.4 experimental: modo, N1, N2, N3, P-M1 y trazabilidad de los parámetros (columnas C:G de la tabla)
    HOJA_CONFIG: ["B4", "B11:B16", "B21:B23", "B28:B32", "B36:B51", "C129:G141"],
}

# Parámetros de diseño editables que, si cambian, no son una manipulación pero sí deben verse.
PARAMETROS = {"Diagnóstico V6!C91", "Diagnóstico V6!C92", "Diagnóstico V6!C93", "Diagnóstico V6!C94",
              "Diagnóstico V6!C158", "Diagnóstico V6!C179", "Historia!C57"}


def _celdas(rango):
    c0, r0, c1, r1 = range_boundaries(rango)
    from openpyxl.utils import get_column_letter as L
    return {f"{L(c)}{r}" for r in range(r0, r1 + 1) for c in range(c0, c1 + 1)}


def conjunto_entradas():
    """{hoja: set(coordenadas)}"""
    return {h: set().union(*(_celdas(r) for r in rangos)) for h, rangos in ENTRADAS.items()}


def es_entrada(hoja, coord, _cache={}):
    if not _cache:
        _cache.update(conjunto_entradas())
    return coord in _cache.get(hoja, set())
