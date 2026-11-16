"""Revisión n.º 6 (frente E · F1 · Elis). Contraejemplos sobre filas reales de los PDF, con el verificador oficial de cada
versión como proceso aparte. No modifica nada del autor.

Cada caso fija una línea real de una página (por un patrón que solo casa esa línea, o por su número de orden entre las
que casan), una posición y un ejercicio, y la declara como lo haría una cifra del grupo: «consolidado IFRS, grupo Elis»,
«mm EUR» (o «%»), modo «dos_columnas» y la edición que la regla exige. Se imprime la línea, el token y el veredicto de
cada versión en las seis dimensiones.

Bloques:
  F  falsos negativos nuevos de C12: el mismo año repetido en la cabecera (una vez por medida o por entidad);
  G  falsos positivos nuevos de C12: cifras legítimas que pasan a PENDIENTE o a FALLO;
  H  perímetro: tablas bajo un título de tabla en caja normal, o con columnas por país sin columna de fecha;
  I  controles de las correcciones de Q1–Q5 con filas elegidas por el revisor.

Uso: python3 -I contraejemplos_6.py --raiz <munger_v2_r1> --version C11=<frente C11> --version C13=<frente C13>
"""
import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from arnes6 import DIMS, Modulo, edicion_que_exige_la_regla, etiqueta_de_linea, fila, oficial  # noqa: E402

# (id, bloque, doc, página, patrón de la línea, n.º de orden entre las que casan (0 = primera), posición del token, ejercicio,
#  lectura del revisor en la página [P])
CASOS = [
    # ---------------- F: mismo año repetido por medida o por entidad
    ("F1", "URD2025", 393, r"^\s*› of which Ireland\s", 0, 1, 2025, "impuesto reconocido en IRLANDA en 2025 (1,8); la fila es un desglose por jurisdicción fiscal, no el grupo"),
    ("F2", "URD2025", 393, r"^\s*› of which Ireland\s", 0, 0, 2025, "resultado antes de impuestos de IRLANDA en 2025 (13,4)"),
    ("F3", "DEU2024FR", 338, r"^\s*dont Irlande\s", 0, 3, 2023, "resultado antes de impuestos de IRLANDA en 2023 (10,1)"),
    ("F4", "DEU2024FR", 338, r"^\s*dont Irlande\s", 0, 0, 2024, "resultado antes de impuestos de IRLANDA en 2024 (8,2)"),
    ("F5", "DEU2024FR", 338, r"^\s*Hors Union européenne\s", 0, 4, 2023, "impuesto reconocido FUERA DE LA UNIÓN EUROPEA en 2023 (27,2)"),
    ("F6", "URD2023", 346, r"^\s*of which Ireland\s", 0, 1, 2023, "impuesto reconocido en IRLANDA en 2023 (1,3)"),
    ("F7", "URD2025", 393, r"^\s*TOTAL\s+492\.9", 0, 1, 2025, "control: total del grupo, impuesto reconocido en 2025 (126,2)"),
    ("F8", "URD2025", 393, r"^\s*France\s+141\.4", 0, 1, 2025, "control: fila «France» de la misma tabla"),
    ("F9", "URD2025", 371, r"^\s*Discount rate\s+9\.1%\s+9\.3%\s+9\.1%", 0, 4, 2025, "tasa de descuento de la marca KENNEDY HYGIENE (10,3 %); columna de una sociedad"),
    ("F10", "URD2025", 371, r"^\s*Royalty rate\s", 0, 2, 2025, "tasa de regalía de la marca LE JACQUARD FRANÇAIS (4,0 %)"),
    ("F11", "DEU2024FR", 317, r"^\s*Taux d'actualisation\s+9,3%", 0, 4, 2024, "tasa de descuento de la marca KENNEDY HYGIENE (10,3 %)"),
    ("F12", "DEU2024FR", 317, r"^\s*Taux d'actualisation\s+9,3%", 0, 0, 2024, "misma línea, marca ELIS (9,3 %)"),
    ("F13", "URD2022", 302, r"^\s*Lease liabilities\s+485\.5", 0, 5, 2022, "TOTAL DE FLUJOS FUTUROS SIN DESCONTAR a 31-12-2022 (612,1); no es el pasivo por arrendamientos"),
    ("F14", "URD2022", 302, r"^\s*Lease liabilities\s+485\.5", 0, 0, 2022, "valor en libros del pasivo por arrendamientos a 31-12-2022 (485,5): la cifra legítima"),
    ("F15", "URD2025", 366, r"^\s*Lease liabilities\s+703\.2", 0, 5, 2025, "control en otra edición: total de flujos sin descontar a 31-12-2025 (856,9)"),
    ("F16", "URD2025", 366, r"^\s*Lease liabilities\s+703\.2", 0, 0, 2025, "control en otra edición: valor en libros a 31-12-2025 (703,2)"),
    ("F17", "URD2025", 402, r"^\s*TOTAL\s+0\.8\s+0\.8\s+0\.6\s+0\.6", 0, 2, 2025, "honorarios de 2025 de UNA de las dos firmas auditoras (0,6), no el total del grupo"),
    ("F18", "URD2025", 402, r"^\s*TOTAL\s+0\.8\s+0\.8\s+0\.6\s+0\.6", 0, 0, 2025, "honorarios de 2025 de la otra firma (0,8)"),
    ("F19", "URD2023", 261, r"Net income from ordinary operations at €433\.4 million, up 23\.4%", 0, 0, 2022, "línea de prosa: variación de 2023 frente a 2022, declarada 2022"),
    # ---------------- G: cifras legítimas que pasan a PENDIENTE o a FALLO
    ("G1", "URD2021", 298, r"^\s*TOTAL\s+\d", 0, 0, 2021, "total de honorarios de auditores de 2021 (nota 13): cifra del grupo. Encima, en la página, termina la lista de sociedades"),
    ("G2", "URD2022", 336, r"^\s*TOTAL\s+\d", 0, 0, 2022, "total de honorarios de auditores de 2022 (nota 13)"),
    ("G3", "URD2023", 355, r"^\s*TOTAL\s+\d", 0, 0, 2023, "total de honorarios de auditores de 2023 (nota 13)"),
    ("G4", "DEU2024FR", 347, r"^\s*TOTAL\s+\d", 0, 0, 2024, "total de honorarios de auditores de 2024 (nota 13)"),
    ("G5", "URD2025", 402, r"^\s*Fees relating to the independent audit\*", 0, 0, 2025, "control: en el URD 2025 el encabezado de la nota 13 ocupa dos líneas"),
    ("G6", "DEU2024FR", 323, r"^\s*convertibles\s+354,6", 0, 0, 2024, "valor en libros (coste amortizado) de las obligaciones convertibles a 31-12-2024 (354,6)"),
    ("G7", "DEU2024FR", 323, r"^\s*USPP\s+705,8", 0, 0, 2024, "valor en libros del USPP a 31-12-2024 (705,8)"),
    ("G8", "URD2025", 377, r"^\s*Convertible bonds\s+364\.4", 0, 0, 2025, "control en otra edición: valor en libros de los convertibles a 31-12-2025 (364,4)"),
    ("G9", "URD2025", 360, r"^\s*Number of rights originally granted", 0, 3, 2024, "plan de acciones de rendimiento n.º 21 (nota 5.4, del grupo); encima termina el bloque «SWITZERLAND – DETAILS» de pensiones"),
    # ---------------- H: perímetro
    ("H1", "URD2025", 371, r"^\s*WACC\s+9\.9%\s+226\.2", 0, 1, 2025, "tabla de sensibilidad del deterioro de la UGE MÉXICO (título de tabla «Mexico»)"),
    ("H2", "URD2022", 274, r"^\s*Intangible assets\s+23\.8\s+16\.9", 0, 1, 2022, "combinaciones de negocio de 2022: columna ALEMANIA (16,9)"),
    ("H3", "URD2022", 274, r"^\s*Intangible assets\s+23\.8\s+16\.9", 0, 0, 2022, "control: primera columna, valor razonable total (23,8)"),
    ("H4", "URD2021", 288, r"^\s*Fixed rate\s", 1, 0, 2021, "tabla «Interest rate swap – Chile»: tipo fijo del swap de la filial chilena"),
    ("H5", "URD2023", 323, r"^\s*WACC\s+\d", 0, 1, 2023, "tabla de sensibilidad del deterioro de la UGE FRANCIA (título de tabla «France»)"),
    # ---------------- I: controles de Q1–Q5 con filas del revisor
    ("I1", "URD2021", 228, r"^\s*TOTAL ASSETS\s", 0, 0, 2021, "balance del URD 2021: total activo a 31-12-2021 (8.039,5)"),
    ("I2", "URD2021", 228, r"^\s*TOTAL ASSETS\s", 0, 1, 2020, "ídem a 31-12-2020 reexpresado (7.862,4)"),
    ("I3", "URD2021", 228, r"^\s*TOTAL ASSETS\s", 0, 2, 2020, "ídem, saldo de apertura 01-01-2020 (8.198,0) declarado 2020: debe fallar"),
    ("I4", "URD2021", 228, r"^\s*TOTAL ASSETS\s", 0, 1, 2021, "ídem, columna de 2020 declarada 2021: debe fallar"),
    ("I5", "URD2022", 271, r"^\s*Acquisition of subsidiaries, net of cash acquired\s", 0, 0, 2021, "tabla de reexpresión: adquisiciones de 2021, columna «published» (86,9): debe fallar en edición"),
    ("I6", "URD2022", 271, r"^\s*Acquisition of subsidiaries, net of cash acquired\s", 0, -1, 2021, "ídem, columna «restated» (86,8): la vigente"),
    ("I7", "URD2023", 309, r"^\s*Discount rate: -0\.5% impact\s", 0, 0, 2023, "sensibilidad de las pensiones de Irlanda a 31-12-2023 (+8,8 %); su cabecera propia es «12/31/2023»"),
    ("I8", "URD2023", 309, r"^\s*Discount rate: -0\.5% impact\s", 0, 0, 2022, "ídem, declarada 2022: debe fallar (C11 la aceptaba)"),
    ("I9", "URD2023", 308, r"^\s*Total value of defined benefit plan obligations \(1\)\s", 0, -1, 2022, "obligaciones de FRANCIA de 2022 (40,1), bloque «FRANCE – DETAILS» (caso de Q4)"),
    ("I10", "URD2022", 243, r"^\s*and Ireland\s", 0, 0, 2022, "tabla de crecimiento: rótulo partido «United Kingdom / and Ireland» (caso de Q5)"),
    ("I11", "URD2025", 363, r"^\s*CGU France\s", 0, 0, 2025, "fondo de comercio de la UGE FRANCIA (caso E15 de Q5): debe fallar"),
    ("I12", "URD2025", 363, r"^\s*CGU Denmark\s", 0, 0, 2025, "misma tabla: fondo de comercio de la UGE DINAMARCA (412,2), declarado del grupo"),
    ("I13", "URD2025", 363, r"^\s*CGU Sweden & Finland\s", 0, 0, 2025, "misma tabla: fondo de comercio de la UGE SUECIA Y FINLANDIA (538,5)"),
    ("I14", "DEU2024FR", 309, r"^\s*UGT Irlande\s", 0, 1, 2023, "DEU 2024: fondo de comercio de la UGE IRLANDA de 2023 (76,1)"),
    ("I15", "URD2021", 265, r"^\s*CGU United Kingdom\s", 0, 0, 2021, "URD 2021: fondo de comercio de la UGE REINO UNIDO (101,4)"),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raiz", required=True)
    ap.add_argument("--version", action="append", required=True, help="NOMBRE=carpeta (se puede repetir)")
    a = ap.parse_args()
    versiones = [v.split("=", 1) for v in a.version]
    M = Modulo(versiones[-1][1], a.raiz, "v_ultima")
    filas, meta = [], {}
    for idc, doc, p, patron, orden, pos, anio, lectura in CASOS:
        idioma, E = M.fuentes[doc]["idioma"], M.fuentes[doc]["ejercicio"]
        lineas = M.texto(doc, p).splitlines()
        casan = [i for i, l in enumerate(lineas) if re.search(patron, l)]
        if len(casan) <= orden:
            print(f"{idc}: la línea no se localiza en {doc} p.{p} ({patron})")
            continue
        i = casan[orden]
        toks = M.m.tokens_numericos(lineas[i], idioma)
        tok = toks[pos]
        etq, occ = etiqueta_de_linea(lineas, i)
        f = fila(idc, doc=doc, pagina=p, anio=anio, etiqueta=etq, ocurrencia=occ, pos=pos if pos < 0 else pos - len(toks), literal=tok,
                 valor_publicado=str(M.m.valor(tok, idioma)), unidad="%" if "%" in tok else "mm EUR",
                 edicion=edicion_que_exige_la_regla(anio, E, M.ejercicios))
        filas.append(f)
        meta[idc] = (doc, p, i, lineas[i], tok, anio, f["unidad"], f["edicion"], lectura, len(casan))
    res = {nom: oficial(carpeta, a.raiz, filas)[1] for nom, carpeta in versiones}
    titulos = {"F": "F. Falsos negativos nuevos de C12: el mismo año repetido en la cabecera, una vez por medida o por entidad",
               "G": "G. Falsos positivos nuevos de C12: cifras legítimas que pasan a PENDIENTE o a FALLO",
               "H": "H. Perímetro: título de tabla en caja normal y columnas por país sin columna de fecha",
               "I": "I. Controles de las correcciones de Q1–Q5 con filas elegidas por el revisor"}
    bloque = None
    for idc, *_ in CASOS:
        if idc not in meta:
            continue
        if idc[0] != bloque:
            bloque = idc[0]
            print(f"\n\n{titulos[bloque]}\n" + "-" * 100)
        doc, p, i, linea, tok, anio, unidad, edicion, lectura, n = meta[idc]
        print(f"\n{idc} · {lectura}")
        print(f"    {doc} p.{p} l.{i + 1} · «{re.sub(r'  +', '  ', linea.strip())[:118]}» · token «{tok}» · declarado {anio}, {unidad}, grupo, edición {edicion}")
        for nom, _ in versiones:
            r = res[nom][idc]
            partes = [f"{k} {r['dimensiones'][k]['estado']}: {r['dimensiones'][k].get('detalle', '')[:150]}" for k in DIMS
                      if r["dimensiones"][k]["estado"] not in ("OK", "NO_APLICA")]
            print(f"    {nom}: {r['estado']}" + (" · " + " · ".join(partes) if partes else " en las seis dimensiones"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
