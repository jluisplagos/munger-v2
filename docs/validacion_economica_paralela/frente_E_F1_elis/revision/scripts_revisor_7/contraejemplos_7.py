"""Revisión n.º 7 (frente E · F1 · Elis). Contraejemplos sobre filas reales de los PDF, con el verificador OFICIAL de cada
versión ejecutado como proceso aparte (scripts/verificar_cifras.py sobre un CSV temporal, igual que lo ejecuta el autor).
No modifica nada del autor.

Cada caso fija una línea entera de la página (etiqueta «re:^…$» y ocurrencia) y un token de esa línea, y lo declara como
se indica. Se muestra el resultado de cada versión: estado de la fila y motivo de cada dimensión que no queda OK.

Uso: python3 -I contraejemplos_7.py --raiz <munger_v2_r1> --version C11=<frente C11> --version C13=<frente C13> --version C14=<frente C14>
"""
import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import arnes7  # noqa: E402

# (id, título, doc, página, patrón de la línea, token, ejercicio declarado, opciones)
#   opciones: idf (identificador de la fila: decide el modo que admite el verificador), modo, unidad
CASOS = [
    ("A", "Estado de cambios en el patrimonio: el año del TÍTULO de la tabla («as at December 31, AAAA») cuenta como columna de "
          "ejercicio. La fila es el saldo de apertura (cierre del ejercicio anterior); la cifra, el capital social"),
    ("A1", "capital a 31-12-2021 (224,1) declarado 2021, su ejercicio: cifra legítima", "URD2022", 262, r"^\s*31, 2021 restated\(a\)\s", "224.1", 2021, {}),
    ("A2", "la misma cifra declarada 2022, el año del título: ejercicio equivocado", "URD2022", 262, r"^\s*31, 2021 restated\(a\)\s", "224.1", 2022, {}),
    ("A3", "capital a 31-12-2024 (236,7) declarado 2024, su ejercicio", "URD2025", 328, r"^\s*31, 2024, restated\*\s", "236.7", 2024, {}),
    ("A4", "la misma cifra declarada 2025, el año del título", "URD2025", 328, r"^\s*31, 2024, restated\*\s", "236.7", 2025, {}),
    ("A5", "capital a 31-12-2022 (230,1) declarado 2022, su ejercicio; el año del título queda a 4,5 caracteres", "URD2023", 280,
     r"^\s*31, 2022, restated\*\s", "230.1", 2022, {}),
    ("A6", "capital a 31-12-2020 (221,8) declarado 2020, su ejercicio", "URD2021", 230, r"^\s*31, 2020 restated \(a\)\s", "221.8", 2020, {}),
    ("A7", "DEU 2024: capital a 31-12-2023 (234,0) declarado 2023, su ejercicio", "DEU2024FR", 274, r"^\s*2023, retraité\*\s", "234,0", 2023, {}),
    ("A8", "la misma cifra declarada 2024, el año del título: ejercicio equivocado", "DEU2024FR", 274, r"^\s*2023, retraité\*\s", "234,0", 2024, {}),
    ("A9", "DEU 2024, estado del ejercicio anterior: capital a 31-12-2022 (230,1) declarado 2023, el año del título: ejercicio equivocado",
     "DEU2024FR", 275, r"^\s*2022\s+230,1\s", "230,1", 2023, {}),
    ("A10", "control: saldo de cierre a 31-12-2022 (230,1) declarado 2022, su ejercicio", "URD2022", 262, r"^\s*DECEMBER, 31 2022\s", "230.1", 2022, {}),
    ("A11", "control: el mismo saldo de cierre declarado 2021", "URD2022", 262, r"^\s*DECEMBER, 31 2022\s", "230.1", 2021, {}),
    ("A12", "URD 2021: prima de emisión a 31-12-2020 (2.575,6) declarada 2020, su ejercicio; el año del título queda a 5,5 caracteres",
     "URD2021", 230, r"^\s*31, 2020 restated \(a\)\s", "2,575.6", 2020, {}),
    ("A13", "URD 2021, estado del ejercicio anterior: capital a 31-12-2019 (221,3) declarado 2019, su ejercicio", "URD2021", 231,
     r"^\s*December 31, 2019\s", "221.3", 2019, {}),
    ("A14", "URD 2022, estado del ejercicio anterior: capital a 31-12-2020 (221,8) declarado 2020, su ejercicio", "URD2022", 263,
     r"^\s*31, 2020\s", "221.8", 2020, {}),
    ("A15", "URD 2025, estado del ejercicio anterior: capital a 31-12-2023 (234,0) declarado 2023, su ejercicio", "URD2025", 329,
     r"^\s*31, 2023\s", "234.0", 2023, {}),
    ("A16", "URD 2023: capital a 31-12-2022 (230,1) declarado 2023, el año del título", "URD2023", 280, r"^\s*31, 2022, restated\*\s", "230.1", 2023, {}),
    ("A17", "URD 2021: capital a 31-12-2020 (221,8) declarado 2021, el año del título", "URD2021", 230, r"^\s*31, 2020 restated \(a\)\s", "221.8", 2021, {}),
    ("A18", "DEU 2024, estado del ejercicio anterior: capital a 31-12-2022 (230,1) declarado 2022, su ejercicio", "DEU2024FR", 275,
     r"^\s*2022\s+230,1\s", "230,1", 2022, {}),

    ("B", "Fila de un segmento cuya cifra cae en una línea SIN rótulo (el rótulo «Scandinavia and Eastern / Europe» ocupa la línea "
          "de arriba y la de abajo). Tabla de crecimiento del informe de gestión, URD 2023 p.261"),
    ("B1", "ventas de 2022 del segmento Escandinavia y Europa del Este (580,7), declaradas del grupo", "URD2023", 261,
     r"^\s+599\.2\s+580\.7\s", "580.7", 2022, {}),
    ("B2", "ventas de 2023 del mismo segmento (599,2), declaradas del grupo", "URD2023", 261, r"^\s+599\.2\s+580\.7\s", "599.2", 2023, {}),
    ("B3", "crecimiento publicado de 2023 del segmento (3,2 %), declarado como el del grupo (modo «crecimiento»)", "URD2023", 261,
     r"^\s+599\.2\s+580\.7\s", "3.2%", 2023, {"idf": "CREC_PUB_R7B3", "modo": "crecimiento", "edicion": "vigente"}),
    ("B4", "crecimiento orgánico de 2023 del segmento (8,5 %), declarado como el del grupo (modo «crecimiento»)", "URD2023", 261,
     r"^\s+599\.2\s+580\.7\s", "8.5%", 2023, {"idf": "CREC_ORG_R7B4", "modo": "crecimiento", "edicion": "vigente"}),
    ("B5", "control: fila «France» de la misma tabla (1.311,6)", "URD2023", 261, r"^\s*France\s+1,311\.6", "1,311.6", 2023, {}),
    ("B6", "control: rótulo partido «United Kingdom and / Ireland» (534,9), con la cifra en la segunda línea del rótulo", "URD2023", 261,
     r"^\s*Ireland\s+534\.9", "534.9", 2023, {}),
    ("B7", "control: fila TOTAL, crecimiento publicado del grupo de 2023 (12,8 %)", "URD2023", 261, r"^\s*TOTAL\s+4,309\.4", "12.8%", 2023,
     {"idf": "CREC_PUB_R7B7", "modo": "crecimiento", "edicion": "vigente"}),

    ("C", "Fila «CGU France» del fondo de comercio por UGE: el número de capítulo del margen («6») cae al principio de su línea "
          "y ocupa el lugar del rótulo. URD 2022 p.298"),
    ("C1", "fondo de comercio de la UGE Francia a 31-12-2021 (1.415,1), declarado del grupo", "URD2022", 298, r"^6\s+CGU France\s", "1,415.1", 2021, {}),
    ("C2", "ídem a 31-12-2022 (1.418,1)", "URD2022", 298, r"^6\s+CGU France\s", "1,418.1", 2022, {}),
    ("C3", "control: la fila siguiente, «CGU Sweden & Finland» (568,5)", "URD2022", 298, r"^\s*CGU Sweden & Finland\s", "568.5", 2021, {}),
    ("C4", "control: «CGU France» en el URD 2025 p.363 (1.442,9), sin el número del margen en su línea", "URD2025", 363, r"^\s*CGU France\s", "1,442.9", 2025, {}),

    ("D", "Tabla con una columna por país y SIN declaración de unidades ni fechas (hipótesis del WACC por UGE): la regla de «cabecera "
          "con países sin columna reconocida» no llega a actuar"),
    ("D1", "tipo sin riesgo de la UGE FRANCIA (3,7 %), URD 2025 p.369", "URD2025", 369, r"^\s*Risk-free rate\s+3\.7%", "3.7%", 2025, {"tok_occ": 1}),
    ("D2", "tipo sin riesgo de la UGE ALEMANIA (2,8 %), misma fila", "URD2025", 369, r"^\s*Risk-free rate\s+3\.7%", "2.8%", 2025, {}),
    ("D3", "DEU 2024 p.315: tipo sin riesgo de la UGE Francia (3,4 %)", "DEU2024FR", 315, r"^\s*Taux sans risque\s+3,4%", "3,4%", 2024, {"tok_occ": 1}),
    ("D4", "control (H2 de la revisión n.º 6): combinaciones de negocio de 2022, columna de Alemania (16,9), con declaración de unidades",
     "URD2022", 274, r"^\s*Intangible assets\s+23\.8\s+16\.9", "16.9", 2022, {}),
    ("D5", "URD 2021 p.270, la misma tabla tras un texto: última fila, «PRE-TAX DISCOUNT RATE 2021 / (APPROXIMATION)», columna de Francia (9,1 %)",
     "URD2021", 270, r"^\s*\(APPROXIMATION\)\s+9\.1%", "9.1%", 2021, {"tok_occ": 1}),
    ("D6", "control: en esa misma tabla, la fila «Risk-free rate», columna de Francia (0,7 %): la regla de columnas por país sí actúa",
     "URD2021", 270, r"^\s*Risk-free rate\s+0\.7%", "0.7%", 2021, {"tok_occ": 1}),

    ("E", "Decisiones de C14 que no siguen la propuesta de la revisión n.º 6: casos de control"),
    ("E1", "R2 (G5): honorarios de 2025 de una firma auditora (0,6): cifra del grupo; OK en C13", "URD2025", 402,
     r"^\s*Fees relating to the independent audit\*\s", "0.6", 2025, {"tok_occ": 1}),
    ("E2", "R3: capital a 31-12-2021 de la página del ejercicio anterior (224,1) declarado 2021; el año del título queda a 3,5 caracteres",
     "URD2023", 281, r"^\s*December 31, 2021\s", "224.1", 2021, {}),
    ("E3", "R2 (G9): plan de acciones n.º 21 (990.040) del URD 2025 p.360: el perímetro queda OK", "URD2025", 360,
     r"^\s*Number of rights originally granted", "990,040", 2024, {}),
    ("E4", "R1, límite de la regla de grupos: tabla con una columna por marca y SIN ejercicios (URD 2022 p.305); tasa de descuento de la "
           "marca ELIS (8,4 %)", "URD2022", 305, r"^\s*Discount rate\s+8\.4%\s+8\.4%\s+8\.8%", "8.4%", 2022, {"tok_occ": 1}),
    ("E5", "misma fila, marca KENNEDY (8,8 %)", "URD2022", 305, r"^\s*Discount rate\s+8\.4%\s+8\.4%\s+8\.8%", "8.8%", 2022, {}),
]


def construir(v, caso):
    cid, titulo, doc, pag, patron, tok, anio, op = caso
    m = v.m
    idioma, E = v.fuentes[doc]["idioma"], v.fuentes[doc]["ejercicio"]
    lineas = v.lineas(doc, pag)
    idxs = [i for i, l in enumerate(lineas) if re.search(patron, l)]
    if len(idxs) != 1:
        raise SystemExit(f"{cid}: el patrón casa {len(idxs)} líneas en {doc} p.{pag}")
    i = idxs[0]
    toks = m.tokens_numericos(lineas[i], idioma)
    pos = [k for k, t in enumerate(toks) if t == tok]
    if not pos:
        raise SystemExit(f"{cid}: el token {tok!r} no está en la línea: {toks}")
    k = pos[op.get("tok_occ", 1) - 1] if "tok_occ" in op else pos[0]
    etq, occ = arnes7.etiqueta_de_linea(lineas, i)
    f = arnes7.fila(op.get("idf", "R7_" + cid), doc=doc, pagina=pag, anio=anio, etiqueta=etq, ocurrencia=occ, pos=k - len(toks), literal=tok,
                    valor_publicado=str(m.valor(tok, idioma)), unidad="%" if "%" in tok else "mm EUR",
                    edicion=op.get("edicion", arnes7.edicion_de_la_regla(anio, E, v.ejercicios)), control_anio=op.get("modo", "dos_columnas"))
    return f, i, lineas[i]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raiz", required=True)
    ap.add_argument("--version", action="append", required=True, help="NOMBRE=carpeta (se puede repetir); la última es la de referencia")
    a = ap.parse_args()
    versiones = [x.split("=", 1) for x in a.version]
    ref = arnes7.Version(versiones[-1][1], a.raiz, versiones[-1][0])
    filas, meta = [], {}
    for caso in CASOS:
        if len(caso) == 2:
            continue
        f, i, linea = construir(ref, caso)
        filas.append(f)
        meta[caso[0]] = (f, i, linea)
    res = {nom: arnes7.oficial(carpeta, a.raiz, filas)[1] for nom, carpeta in versiones}
    for caso in CASOS:
        if len(caso) == 2:
            print(f"\n\n{caso[0]}. {caso[1]}\n" + "-" * 100)
            continue
        cid, titulo, doc, pag = caso[:4]
        f, i, linea = meta[cid]
        print(f"\n{cid} · {titulo}")
        print(f"    {doc} p.{pag} l.{i + 1} · «{re.sub(r'\\s{2,}', '  ', linea.strip())[:150]}» · token «{f['literal']}» · declarado {f['anio']}, "
              f"{f['unidad']}, grupo, edición {f['edicion']}, modo {f['control_anio']}")
        for nom, _ in versiones:
            print(f"    {nom}: {arnes7.resumen(res[nom][f['id']])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
