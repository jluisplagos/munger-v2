#!/usr/bin/env python3
"""Tabla antes/después de R-V1 (entrega 4.9) a partir de las dos salidas de la batería de integridad conservadas.

Uso: python3 -I tabla_antes_despues_rv1.py   → escribe reproduccion/tabla_antes_despues_rv1.md

Antes: pruebas/test_integridad_auditoria_v2.py --codigo reproduccion/codigo_4_8_1 --json reproduccion/test_integridad_con_codigo_4_8_1.json.
Después: la misma batería con el código del árbol (--json resultados/test_integridad_auditoria_v2.json).
Para cada prueba muestra el resultado y lo observado (código, estado, auditoría, filas del resumen) con cada código.
"""
import json
import os

AQUI = os.path.dirname(os.path.abspath(__file__))
EXP = os.path.dirname(AQUI)


def leer(p):
    d = json.load(open(p, encoding="utf-8"))
    return {(x["grupo"], x["prueba"]): ("PASA" if x["pasa"] else "FALLA", (x["detalle"] or "")[:150]) for x in d["pruebas"]}


def main():
    antes = leer(os.path.join(EXP, "reproduccion", "test_integridad_con_codigo_4_8_1.json"))
    despues = leer(os.path.join(EXP, "resultados", "test_integridad_auditoria_v2.json"))
    lin = ["# R-V1 · antes (código 4.8.1) y después (código 4.9)", "",
           "Generada por `scripts/tabla_antes_despues_rv1.py` desde las dos salidas conservadas de `pruebas/test_integridad_auditoria_v2.py`.",
           "«Antes» ejecuta la batería con `--codigo reproduccion/codigo_4_8_1` (cierre_v2.py, pipeline.py, ficha.py, resumen.py e informe.py de la 4.8.1: todos los archivos de código que cambia la 4.9; el resto es idéntico).",
           "Las pruebas que solo existen con el código 4.9 (unidades de `huella_fiel`) figuran como «—» antes.", "",
           "| Grupo | Prueba | Antes (4.8.1) | Lo observado antes | Después (4.9) |", "|---|---|---|---|---|"]
    for k, (r, obs) in despues.items():
        ra, oa = antes.get(k, ("—", ""))
        lin.append(f"| {k[0].split(' ')[0]} | {k[1].replace('|', '/')} | {ra} | {oa.replace('|', '/') if ra == 'FALLA' else ''} | {r} |")
    na = sum(1 for v in antes.values() if v[0] == "PASA")
    nd = sum(1 for v in despues.values() if v[0] == "PASA")
    lin += ["", f"Antes: {na}/{len(antes)} PASAN. Después: {nd}/{len(despues)} PASAN."]
    open(os.path.join(EXP, "reproduccion", "tabla_antes_despues_rv1.md"), "w", encoding="utf-8").write("\n".join(lin) + "\n")
    print(f"antes {na}/{len(antes)} · después {nd}/{len(despues)}")


if __name__ == "__main__":
    main()
