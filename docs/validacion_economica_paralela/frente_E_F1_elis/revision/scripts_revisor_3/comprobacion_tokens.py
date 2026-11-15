"""¿Alguna fila real del modo por defecto («dos_columnas») procede de una tabla con una tercera columna a la derecha?

El control del ejercicio de verificar_cifras.py del autor es posicional: supone que los dos últimos números de la línea son
los dos ejercicios de la cabecera (objeción N1 de la revisión n.º 3). Este script cuenta, en la línea que el verificador
del autor encontró para cada fila, los números que siguen al rótulo. Con dos, la hipótesis se cumple. Con tres, solo se
cumple si el primero es la referencia de una nota («4.5», «9», «8.2»).

Uso: python3 -I comprobacion_tokens.py --autor <carpeta frente_E_F1_elis del autor>
"""
import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path

NUM_EN = re.compile(r"^[+\-–−]?\(?[+\-–−]?(\d{1,3}(,\d{3})*(\.\d+)?|\d+(\.\d+)?)\)?\s?%?\)?$")
NUM_FR = re.compile(r"^[+\-–−]?\s?\(?[+\-–−]?(\d{1,3}( \d{3})*(,\d+)?|\d+(,\d+)?)\)?\s?%?\)?$")
NOTA = re.compile(r"^\d{1,2}([.,]\d{1,2})?$")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--autor", required=True, type=Path)
    a = ap.parse_args()
    filas = list(csv.DictReader((a.autor / "datos" / "cifras_fuente.csv").open(encoding="utf-8"), delimiter=";"))
    ver = {r["id"]: r for r in json.loads((a.autor / "resultados" / "verificacion_cifras.json").read_text(encoding="utf-8"))["cifras"]}
    c, sin_nota = Counter(), []
    for r in filas:
        if r["tipo"] != "tabla" or r["control_anio"] != "dos_columnas":
            continue
        linea = ver[r["id"]].get("linea") or ""
        rx = NUM_FR if r["doc"].startswith("DEU") else NUM_EN
        trozos = [t.strip() for t in re.split(r"\s{2,}", linea.strip()) if t.strip()]
        nums = [t for t in trozos[1:] if rx.match(t) or t in ("-", "–", "—", "−")]
        c[len(nums)] += 1
        if len(nums) != 2 and not (len(nums) == 3 and NOTA.match(nums[0]) and "%" not in nums[2]):
            sin_nota.append((r["id"], r["doc"], r["pagina"], linea[:110]))
    print(f"Filas del modo por defecto: {sum(c.values())}")
    for n in sorted(c):
        print(f"  con {n} números tras el rótulo: {c[n]}")
    print(f"Filas con un número de más que no es una referencia de nota a la izquierda: {len(sin_nota)}")
    for x in sin_nota:
        print("  ", x)


if __name__ == "__main__":
    main()
