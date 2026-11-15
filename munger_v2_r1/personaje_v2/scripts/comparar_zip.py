#!/usr/bin/env python3
"""Comparación de dos paquetes ZIP (xlsx, docx o zip) miembro a miembro (encargo 4.12 §6).

Para un artefacto ENTREGADO se exige la huella estricta del archivo (SHA-256 de todos sus bytes). Para una RECONSTRUCCIÓN en otro
entorno, la huella del archivo no sirve: la misma lista de miembros con el mismo contenido puede comprimirse con otros bytes (otra
versión de zlib, otro nivel o el orden de los metadatos del contenedor). Esta comparación exige lo que importa: los mismos nombres
de miembro, en el mismo orden, con el mismo contenido descomprimido (SHA-256 de cada miembro). No compara fechas ni compresión.
Uso: comparar_zip.py A.zip B.zip   → código 0 si el contenido coincide miembro a miembro; 1 con las diferencias.
"""
import hashlib
import sys
import zipfile


def miembros(p):
    with zipfile.ZipFile(p) as z:
        return [(i.filename, hashlib.sha256(z.read(i.filename)).hexdigest()) for i in z.infolist()]


def comparar(a, b):
    """(iguales, detalle): mismos nombres de miembro, en el mismo orden, con el mismo contenido descomprimido."""
    ma, mb = miembros(a), miembros(b)
    na, nb = [x[0] for x in ma], [x[0] for x in mb]
    if na != nb:
        solo_a, solo_b = sorted(set(na) - set(nb)), sorted(set(nb) - set(na))
        return False, f"miembros distintos: solo en A {solo_a[:5]}, solo en B {solo_b[:5]}" + ("" if solo_a or solo_b else " (mismo conjunto, otro orden)")
    dif = [n for (n, ha), (_, hb) in zip(ma, mb) if ha != hb]
    if dif:
        return False, f"{len(dif)} miembros con contenido distinto: {dif[:8]}"
    return True, f"{len(ma)} miembros con el mismo contenido descomprimido"


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)
    ok, det = comparar(sys.argv[1], sys.argv[2])
    print(("IGUAL MIEMBRO A MIEMBRO · " if ok else "DISTINTO · ") + det)
    sys.exit(0 if ok else 1)
