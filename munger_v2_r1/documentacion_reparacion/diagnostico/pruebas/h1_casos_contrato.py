#!/usr/bin/env python3
"""H1 · línea de base, con el código ACTUAL, de los casos que añade el contrato de reparación (3b, 7b, 12, 13).

Uso: python3 -I -B h1_casos_contrato.py RUTA_SCRIPTS DIR_TRABAJO SALIDA_JSON
Mismo método que h1_comprobar_anio.py. El campo `cita` todavía no existe en el código actual (lo ignora).
"""
import json
import os
import shutil
import sys

scripts, trabajo, salida = sys.argv[1], sys.argv[2], sys.argv[3]
sys.path.insert(0, scripts)
import fase1_historia as F  # noqa: E402


def caso(nombre, pagina, extra, que):
    c = os.path.join(trabajo, "h1_contrato", nombre)
    shutil.rmtree(c, ignore_errors=True)
    os.makedirs(os.path.join(c, "texto"))
    os.makedirs(os.path.join(c, "fase1_partes"))
    open(os.path.join(c, "texto", "AR.txt"), "w", encoding="utf-8").write("[PDF PAGE 1]\n" + pagina + "\n")
    p = {k: {} for k in F.PARTIDAS}
    p.update(extra)
    json.dump({"anio": 2025, "archivo": "AR.txt", "unidad": "millones", "partidas": p},
              open(os.path.join(c, "fase1_partes", "AR_2025.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    e = F.comprobar_anio(c, 2025)
    return {"caso": nombre, "que_prueba": que, "pagina": pagina, "partidas_declaradas": extra, "errores": e,
            "resultado_actual": "ACEPTADO" if not e else "RECHAZADO"}


R = [
    caso("3b_subcadena_con_linea_real", "Capital expenditure 91234",
         {"capex": {"actual": [{"concepto": "Capital expenditure", "impreso": "123", "pagina": 1, "linea": "Capital expenditure 91234"}]}},
         "La línea existe en la página; '123' solo aparece dentro de 91234 (aísla la regla del importe completo)."),
    caso("7b_cero_cita_no_en_pagina", "Revenue 123",
         {"sbc": {"cero": {"motivo": "no hay plan de pagos en acciones", "pagina": 1, "cita": "The Group has no share-based payment programmes"}}},
         "Cero con cita que no está en la página."),
    caso("12_cero_bien_respaldado", "The Group has no share-based payment programmes.",
         {"sbc": {"cero": {"motivo": "no hay plan de pagos en acciones", "pagina": 1, "cita": "The Group has no share-based payment programmes"}}},
         "Cero de SBC con cita literal de la página que lo respalda."),
    caso("13_cero_cita_de_otra_partida", "The Group has no defined benefit pension obligations.",
         {"sbc": {"cero": {"motivo": "no hay plan de pagos en acciones", "pagina": 1, "cita": "The Group has no defined benefit pension obligations"}}},
         "Cero de SBC con cita literal auténtica que habla de pensiones (otra partida)."),
]
json.dump(R, open(salida, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for r in R:
    print(f"{r['caso']:32s} {r['resultado_actual']:10s} {'; '.join(r['errores'])}")
