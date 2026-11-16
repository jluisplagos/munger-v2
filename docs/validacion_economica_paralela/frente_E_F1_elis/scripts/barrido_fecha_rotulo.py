"""Barrido del autor sobre la regla de la fecha del rótulo (revisión n.º 8, T2 y T3) en todas las páginas de las fuentes.

Recorre todas las líneas de todas las páginas de los PDF de datos/fuentes.json y lista las líneas en que
`anio_de_saldo_en_rotulo` da un ejercicio, separadas por si la fecha está en la propia línea o en una línea unida de
encima. De estas, señala las que están justo debajo de una fila de datos: si la línea de fecha unida continuara el
rótulo de la fila anterior, la fecha sería de otra fila (límite declarado de T2).

Con --anterior <verificar_cifras.py de otra versión>, compara además, línea a línea, dónde da ejercicio la regla en las
dos versiones y lista las líneas de dos celdas o más en que solo la da una de ellas, con el número de tokens numéricos de
la línea (las líneas de una sola celda son títulos o continuaciones, y la regla nueva las excluye todas). No modifica nada.

Uso:  python3 -I barrido_fecha_rotulo.py --raiz <ruta>/munger_v2_r1 [--fuentes ../datos/fuentes.json] \\
          [--anterior <carpeta de otra versión>/scripts/verificar_cifras.py --etiqueta <nombre>] > ../resultados/barrido_fecha_rotulo.txt
"""
import argparse
import importlib.util
import json
import sys
from collections import Counter
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
import verificar_cifras as V  # noqa: E402


def cargar(ruta):
    spec = importlib.util.spec_from_file_location("verificar_anterior", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raiz", required=True, type=Path)
    ap.add_argument("--fuentes", type=Path, default=AQUI.parent / "datos" / "fuentes.json")
    ap.add_argument("--anterior", type=Path, help="verificar_cifras.py de la versión con la que comparar")
    ap.add_argument("--etiqueta", default="la versión anterior", help="nombre de esa versión en la salida (p. ej., «C16 (66d01b8)»)")
    a = ap.parse_args()
    A = cargar(a.anterior) if a.anterior else None
    fuentes = json.loads(a.fuentes.read_text(encoding="utf-8"))["fuentes"]
    cuenta, por_doc, unidas = Counter(), Counter(), []
    comparacion, solo_anterior, solo_nueva = Counter(), [], []
    for doc, f in fuentes.items():
        pdf, idioma = a.raiz / f["archivo"], f["idioma"]
        for n in range(1, V.num_paginas(pdf) + 1):
            lineas = V.texto_pagina(pdf, n).splitlines()
            for i, linea in enumerate(lineas):
                if not linea.strip():
                    continue
                anio = V.anio_de_saldo_en_rotulo(lineas, i, idioma)
                if A is not None:
                    previo = A.anio_de_saldo_en_rotulo(lineas, i, idioma)
                    celdas, tokens = len(V.trozos(linea)), len(V.tokens_numericos(linea, idioma))
                    if previo is not None and anio is not None:
                        comparacion["las dos, mismo ejercicio" if previo == anio else "las dos, otro ejercicio"] += 1
                    elif previo is not None:
                        comparacion["solo la anterior, línea de una celda" if celdas < 2 else "solo la anterior, dos celdas o más"] += 1
                        if celdas >= 2:
                            solo_anterior.append((doc, n, i, previo, tokens, A.rotulo_multilinea(lineas, i, idioma)))
                    elif anio is not None:
                        comparacion["solo la nueva"] += 1
                        solo_nueva.append((doc, n, i, anio, tokens, V.rotulo_de_saldo(lineas, i, idioma)))
                if anio is None:
                    continue
                por_doc[doc] += 1
                if V.FECHA_DE_SALDO.search(V.rotulo(linea)):
                    cuenta["fecha en la propia línea"] += 1
                    continue
                cuenta["fecha en una línea unida de encima"] += 1
                rotulo = V.rotulo_de_saldo(lineas, i, idioma)
                k = i - 1
                while k >= 0 and lineas[k].strip() and lineas[k].strip() in rotulo and len(V.trozos(lineas[k])) == 1:
                    k -= 1
                encima = lineas[k] if k >= 0 else ""
                bajo_fila = len(V.trozos(encima)) >= 2 and bool(V.tokens_numericos(encima, idioma))
                unidas.append((doc, n, i, anio, rotulo, V.columnas_de_datos(linea, idioma), bajo_fila, encima.strip()[:60]))
    print("Barrido del autor · regla de la fecha del rótulo (anio_de_saldo_en_rotulo), todas las páginas de las fuentes")
    print(f"Líneas en que da un ejercicio: {sum(cuenta.values())} · {dict(cuenta)}")
    print(f"Por fuente: {dict(por_doc)}")
    print()
    print(f"Líneas con la fecha en una línea unida de encima: {len(unidas)}; justo debajo de una fila de datos: "
          f"{sum(u[6] for u in unidas)}")
    for doc, n, i, anio, rotulo, cols, bajo_fila, encima in unidas:
        extra = f" · encima, la fila «{encima}»" if bajo_fila else ""
        print(f"  {doc} p.{n} l.{i} · {anio} · «{rotulo}» · {cols} columnas de datos{extra}")
    if A is not None:
        print()
        print(f"Comparación con {a.etiqueta}: {dict(comparacion)}")
        print(f"Solo la versión nueva: {len(solo_nueva)}")
        for doc, n, i, anio, tokens, rotulo in solo_nueva:
            print(f"  {doc} p.{n} l.{i} · {anio} · {tokens} tokens · «{rotulo}»")
        print(f"Solo la versión anterior, líneas de dos celdas o más: {len(solo_anterior)} "
              f"({sum(1 for x in solo_anterior if x[4] <= 1)} con un token o ninguno)")
        for doc, n, i, anio, tokens, rotulo in solo_anterior:
            print(f"  {doc} p.{n} l.{i} · {anio} · {tokens} tokens · «{rotulo[:110]}»")
    return 0


if __name__ == "__main__":
    sys.exit(main())
