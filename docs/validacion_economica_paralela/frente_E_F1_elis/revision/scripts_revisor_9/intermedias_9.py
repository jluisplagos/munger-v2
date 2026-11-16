"""Revisión independiente n.º 9 · las versiones intermedias de C18 (frente E · F1 · Elis). No modifica nada del autor.

La octava parte de las respuestas dice dos cosas de la primera parte del código de C18 (d3c0f1b) que el commit final
corrige:
  (1) en d3c0f1b el rótulo unido absorbía la cabecera de columna o la línea de unidades de encima y dejaban de reconocerse
      los saldos de apertura de las cinco tablas de la reserva de coberturas y dos de las cuentas de la sociedad dominante;
  (2) el año de la fecha de cuatro rótulos de saldo volvía a la regla de las columnas y quedaba OK en las seis dimensiones
      («AU 31 DÉCEMBRE 2024», DEU 2024 p.295; «As at December 31, 2021», URD 2022 p.323; «NET CARRYING AMOUNT AS AT
      DECEMBER 31, 2023», URD 2023 p.317 y p.319), como ya ocurría en C14.
Este script lo comprueba con el verificador de cada versión cargado como módulo: C14 (opcional), C16, d3c0f1b, 485de8d y C18.

Uso: python3 -I -B intermedias_9.py --raiz <munger_v2_r1> --c18 <frente C19> --version C16=<frente C17> \
         --version d3c0f1b=<verificar_cifras.py> --version 485de8d=<verificar_cifras.py> [--version C14=<verificar_cifras.py>]
"""
import argparse
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import arnes9 as H  # noqa: E402

ANIOS = [("DEU2024FR", 295, r"^\s*AU 31 DÉCEMBRE 2024\s", "2024"), ("URD2022", 323, r"^\s*As at December 31, 2021\s", "2021"),
         ("URD2023", 317, r"^\s*NET CARRYING AMOUNT AS AT DECEMBER 31, 2023\s", "2023"), ("URD2023", 319, r"^\s*NET CARRYING AMOUNT AS AT DECEMBER 31, 2023\s", "2023")]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raiz", required=True, type=Path)
    ap.add_argument("--c18", required=True, type=Path)
    ap.add_argument("--version", action="append", default=[])
    a = ap.parse_args()
    N = H.Version("C18", a.c18, a.raiz)
    vers = [H.Version(v.split("=", 1)[0], v.split("=", 1)[1], a.raiz, datos=a.c18) for v in a.version] + [N]
    nombres = [v.nombre for v in vers]
    print("Versiones intermedias de C18 · " + " · ".join(nombres))
    print()
    print("== 1. Líneas en que `anio_de_saldo_en_rotulo` da un ejercicio, por versión (todas las páginas) ==")
    da = {v.nombre: {} for v in vers}
    textos = {}
    for doc in sorted(N.fuentes):
        idioma = N.idioma(doc)
        for pag in range(1, N.paginas(doc) + 1):
            L = N.lineas(doc, pag)
            for i, l in enumerate(L):
                if not l.strip():
                    continue
                for v in vers:
                    f = getattr(v.V, "anio_de_saldo_en_rotulo", None)   # C14 no tiene la regla
                    x = f(L, i, idioma) if f else None
                    if x is not None:
                        da[v.nombre][(doc, pag, i)] = x
                        textos[(doc, pag, i)] = l
    for n in nombres:
        print(f"  {n}: {len(da[n])} líneas")
    for x, y in zip(nombres, nombres[1:]):
        solo_x, solo_y = sorted(set(da[x]) - set(da[y])), sorted(set(da[y]) - set(da[x]))
        otro = [k for k in set(da[x]) & set(da[y]) if da[x][k] != da[y][k]]
        print(f"  {x} → {y}: dejan de tenerlo {len(solo_x)}; pasan a tenerlo {len(solo_y)}; con otro ejercicio {len(otro)}")
        if len(solo_y) <= 40:
            for k in solo_y:
                print(f"      + {k[0]} p.{k[1]} l.{k[2] + 1} · {da[y][k]} · «{re.sub(chr(92) + 's{2,}', '  ', textos[k].strip())[:100]}»")
        if len(solo_x) <= 12:
            for k in solo_x:
                print(f"      − {k[0]} p.{k[1]} l.{k[2] + 1} · {da[x][k]} · «{re.sub(chr(92) + 's{2,}', '  ', textos[k].strip())[:100]}»")
    print()
    print("== 2. El año de la fecha de cuatro rótulos de saldo, declarado como cifra del grupo con cada ejercicio (seis dimensiones) ==")
    for doc, pag, rx, lit in ANIOS:
        L = N.lineas(doc, pag)
        cand = [i for i, l in enumerate(L) if re.search(rx, l)]
        idioma, E = N.idioma(doc), N.publicacion(doc)
        for i in cand:
            toks = N.V.tokens_numericos(L[i], idioma)
            k = toks.index(lit)
            print(f"  {doc} p.{pag} l.{i + 1} · «{re.sub(chr(92) + 's{2,}', '  ', L[i].strip())[:90]}» · token «{lit}»")
            for y in (E, E - 1):
                f = H.declarar(doc, pag, L, i, k, len(toks), lit, N.V.valor(lit, idioma), y, H.ID_GENERICO, "dos_columnas", "mm EUR", H.GRUPO,
                               N.edicion_posible("dos_columnas", y, doc))
                partes = []
                for v in vers:
                    r = v.tabla(f)
                    c = H.codigo(r)
                    partes.append(f"{v.nombre} {c} ({H.estado(c)})")
                print(f"      declarado {y}: " + " · ".join(partes))
                print(f"          ejercicio en {vers[-1].nombre}: {vers[-1].tabla(f)['dimensiones']['ejercicio'].get('detalle', '')[:110]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
