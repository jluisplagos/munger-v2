"""Revisión independiente n.º 9 · sondas sobre líneas SINTÉTICAS (frente E · F1 · Elis). No modifica nada del autor.

Como las dos comprobaciones de la excepción «Total» del test del autor, estas sondas llaman a las funciones del verificador
sobre páginas inventadas, de pocas líneas, para fijar el comportamiento de las reglas de C18 en sus bordes. NO son filas de
los PDF: lo que muestran es hipotético [H] mientras no se encuentre en una publicación; el informe dice, para cada una,
cuántas líneas reales tienen esa forma según barrido_9.py y spans_9.py.

Cada token se evalúa con las funciones que `comprobar_tabla` usa para cuatro dimensiones (`comprobar_anio`,
`comprobar_columna`, `comprobar_unidad`, `comprobar_perimetro`), con un identificador genérico (modo «dos_columnas») y el
perímetro del grupo, en C16 y en C18. El literal y la edición no se evalúan: no dependen de la forma de la tabla.

Uso: python3 -I -B sondas_sinteticas_9.py --raiz <munger_v2_r1> --c16 <frente C17> --c18 <frente C19>
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import arnes9 as H  # noqa: E402

CAB = ["    Financial statements for the year ended December 31, 2022", "    Consolidated financial statements", ""]


def evaluar(V, lineas, i, literal, n, anio, idioma="en"):
    toks = V.tokens_numericos(lineas[i], idioma)
    k = [j for j, t in enumerate(toks) if t == literal][n]
    pos = k - len(toks)
    fila = {"id": H.ID_GENERICO, "anio": str(anio), "control_anio": "dos_columnas", "pos": str(pos), "literal": literal,
            "unidad": "%" if "%" in literal else "mm EUR", "perimetro": H.GRUPO, "nota": ""}
    res = [V.comprobar_anio(lineas, i, fila, idioma), V.comprobar_columna(lineas, i, fila, pos, idioma), V.comprobar_unidad(lineas, i, fila, idioma),
           V.comprobar_perimetro(lineas, i, fila, pos, idioma, [])]
    cod = "".join(H.LETRA[e] for e, _ in res)
    return cod, res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raiz", required=True, type=Path)
    ap.add_argument("--c16", required=True, type=Path)
    ap.add_argument("--c18", required=True, type=Path)
    a = ap.parse_args()
    versiones = (H.Version("C16", a.c16, a.raiz), H.Version("C18", a.c18, a.raiz))

    def sonda(clave, titulo, cuerpo, casos, idioma="en"):
        lineas = CAB + cuerpo
        print()
        print(f"{clave} · {titulo}")
        for j, l in enumerate(cuerpo):
            print(f"      {j + len(CAB):2}| {l}")
        for i_rel, literal, n, anio, nota in casos:
            i = len(CAB) + i_rel
            for ver in versiones:
                cod, res = evaluar(ver.V, lineas, i, literal, n, anio, idioma)
                est = "FALLO" if "F" in cod else ("PENDIENTE" if "P" in cod else "OK")
                print(f"    {ver.nombre} · «{literal}»{' (' + str(n + 1) + 'º)' if n else ''} declarado {anio} · ejercicio {res[0][0]} · columna {res[1][0]} · "
                      f"unidad {res[2][0]} · perímetro {res[3][0]} → {est} en las cuatro{' · ' + nota if nota and ver.nombre == 'C18' else ''}")
                if ver.nombre == "C18":
                    for nombre, (e, d) in zip(("ejercicio", "columna", "unidad", "perímetro"), res):
                        if nombre in ("ejercicio", "columna") or e != "OK":
                            print(f"          {nombre}: {d[:170]}")

    print("Sondas sintéticas de la revisión n.º 9 · C16 y C18 · cuatro dimensiones (ejercicio, columna, unidad, perímetro); literal y edición no se evalúan")

    sonda("H1", "T1 · «una sola columna de datos» se mide en los tokens de la fila, no en las columnas de la tabla: celdas con llamada",
          ["    (In millions of euros)                          Land      Vehicles         Total",
           "    As at December 31, 2021                      12.0(a)       33.6(a)          45.6",
           "    Increases                                        1.0           2.0           3.0"],
          [(1, "45.6", 0, 2021, "las celdas «12.0(a)» y «33.6(a)» no son tokens: la fila cuenta una columna")])
    sonda("H2", "T1 · lo mismo con celdas vacías: una sola cifra bajo «Vehicles» en una tabla de tres columnas",
          ["    (In millions of euros)                          Land      Vehicles         Total",
           "    As at December 31, 2021                                       33.6",
           "    Increases                                        1.0           2.0           3.0"],
          [(1, "33.6", 0, 2021, "")])
    sonda("H3", "posición de los tokens · la primera cifra es un entero que está en la fecha del rótulo: la fila de dos columnas cuenta una",
          ["    (In millions of euros)                      Vehicles         Total",
           "    As at 12/31/2021                                  12          45.6",
           "    Increases                                        1.0           3.0"],
          [(1, "12", 0, 2021, "«12» se localiza en «12/31/2021»"), (1, "45.6", 0, 2021, "")])
    sonda("H4", "posición de los tokens · desplazamiento de una columna con cifras distintas (tabla de dos ejercicios)",
          ["    (In millions of euros)                              2022          2021",
           "    Impact of a 0.5 point decrease                       0.5             5",
           "    Other                                                1.0           2.0"],
          [(1, "5", 0, 2022, "«5» es la cifra de 2021: se localiza dentro de «0.5», bajo 2022"), (1, "5", 0, 2021, "su ejercicio verdadero"),
           (1, "0.5", 0, 2022, "«0.5» es la cifra de 2022: se localiza en el rótulo")])
    sonda("H5", "T2 · límite declarado: fila «Balance» bajo una línea de fecha, en mayúscula inicial, que continúa la fila anterior",
          ["    (In millions of euros)                              2022          2021",
           "    Provisions for litigation                           10.0          20.0",
           "    As at 12/31/2021",
           "    Balance                                             30.0          40.0"],
          [(3, "30.0", 0, 2021, "toma la fecha de la línea de encima, que es de la fila anterior"), (3, "30.0", 0, 2022, "")])
    sonda("H6", "T2 · el mismo límite con otros rótulos que la regla admite: «Restated», «Net», «Published»",
          ["    (In millions of euros)                              2022          2021",
           "    Provisions for litigation                           10.0          20.0",
           "    As at 12/31/2021",
           "    Restated                                            30.0          40.0",
           "    Other                                                1.0           2.0",
           "    As at 12/31/2021",
           "    Net                                                 31.0          42.0",
           "    Other                                                1.0           2.0",
           "    As at 12/31/2021",
           "    Published                                           29.0          39.0"],
          [(3, "30.0", 0, 2021, ""), (6, "31.0", 0, 2021, ""), (9, "29.0", 0, 2021, "")])
    sonda("H7", "T2 · control: la misma forma con la línea de fecha en minúscula no se une",
          ["    (In millions of euros)                              2022          2021",
           "    Provisions for litigation                           10.0          20.0",
           "    as at 12/31/2021",
           "    Balance                                             30.0          40.0"],
          [(3, "30.0", 0, 2021, ""), (3, "30.0", 0, 2022, "")])
    sonda("H8", "T2 · «published» en el rótulo de un saldo de una sola columna: toma el ejercicio; nada mira que sea la cifra anterior a la reexpresión",
          ["    (In millions of euros)                                   Impairment loss",
           "    As at December 31, 2021, published                               (57.9)",
           "    As at December 31, 2021, restated                                (58.4)"],
          [(1, "(57.9)", 0, 2021, "edicion_de_columna: " + str(versiones[1].V.edicion_de_columna(
              CAB + ["    (In millions of euros)                                   Impairment loss",
                     "    As at December 31, 2021, published                               (57.9)"], len(CAB) + 1, -1, "en"))),
           (2, "(58.4)", 0, 2021, "")])
    sonda("H9", "T5 · una fila de cifras sin rótulo que empieza por un dígito suelto se toma por la pestaña del capítulo",
          ["    (In number of sites)                                2022          2021",
           "    France                                                12            11",
           "    Scandinavia and Eastern",
           "                                                           5             3",
           "    Europe",
           "    Central Europe                                         9             8",
           "    Latin America                                          7             6"],
          [(3, "5", 0, 2022, "primera celda «5»: `rotulos_sin_rotulo` devuelve la lista vacía")])
    sonda("H10", "T5 · control: la misma fila con «15» y «13»",
          ["    (In number of sites)                                2022          2021",
           "    France                                                12            11",
           "    Scandinavia and Eastern",
           "                                                          15            13",
           "    Europe",
           "    Central Europe                                         9             8",
           "    Latin America                                          7             6"],
          [(3, "15", 0, 2022, "")])
    sonda("H11", "T4 · un título en mayúsculas justo encima de la primera fila de una tabla del grupo, tras una tabla con una columna por país",
          ["    Country                      France       Germany        Brazil",
           "    WACC                           8.3%          7.5%         11.4%",
           "    GROUP MARGINS",
           "    EBITDA margin                 35.1%         34.2%"],
          [(3, "35.1%", 0, 2022, "el título no corta la búsqueda: lo toma por la primera línea del rótulo de la fila")])
    sonda("H12", "S4 · la excepción «Total» con `comprobar_perimetro` (las dos líneas del test del autor, en una página del grupo)",
          ["    Country             France      Germany      Brazil       Total",
           "    WACC 2024             8.3%         7.5%       11.4%        9.0%"],
          [(1, "9.0%", 0, 2024, "columna bajo «Total»"), (1, "8.3%", 0, 2024, "columna de Francia"), (1, "2024", 0, 2024, "el año del rótulo")])
    sonda("H13", "regla de f12f8ea · un año entre paréntesis dentro del rótulo no casa con la expresión del año",
          ["    (In millions of euros)                              2022          2021",
           "    Provision used (2021)                               10.0          20.0",
           "    Provision used 2021                                 10.0          20.0"],
          [(1, "(2021)", 0, 2021, ""), (2, "2021", 0, 2021, "control: el año suelto sí se retira")])
    sonda("H14", "T2 · el límite declarado de H5 en una tabla de una sola columna: no hay columna de ejercicio que lo contradiga",
          ["    (In millions of euros)                                   Impairment loss",
           "    Provisions for litigation                                        10.0",
           "    As at 12/31/2021",
           "    Balance                                                          30.0"],
          [(3, "30.0", 0, 2021, "toma la fecha de la línea de encima, que es de la fila anterior"), (3, "30.0", 0, 2022, "")])
    return 0


if __name__ == "__main__":
    sys.exit(main())
