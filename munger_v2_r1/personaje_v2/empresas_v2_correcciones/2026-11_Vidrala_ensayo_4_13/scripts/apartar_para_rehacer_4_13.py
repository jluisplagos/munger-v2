#!/usr/bin/env python3
"""Aparta a antecedentes/<etiqueta>/ (copia con su SHA-256 y después retirada) las salidas de un expediente que hay que rehacer tras la
revisión interna de la 4.13, sin borrar nada: la fase C y la auditoría (contrato R4 de la materialidad para el objetivo) y, si se pide,
las variantes calculadas (agrupación de avisos de dominio corregida en R17: `en_la_activa` cuenta las lecturas de la activa).
Uso (desde munger_v2_r1/): python3 -I …/apartar_para_rehacer_4_13.py CARPETA_EMPRESA ETIQUETA [--variantes] [--motivo TEXTO]
Escribe CARPETA_EMPRESA/../resultados/apartado_<etiqueta>.json."""
import datetime as dt
import hashlib
import json
import os
import shutil
import sys


def main():
    c = os.path.abspath(sys.argv[1])
    etiqueta = sys.argv[2]
    motivo = sys.argv[sys.argv.index("--motivo") + 1] if "--motivo" in sys.argv else ""
    nombres = ["fase_c.json", "fase_c.md", "auditoria.md"]
    if "--variantes" in sys.argv:
        nombres += ["configuracion_v64_variantes.json", "configuracion_v64_variantes.md"]
    ant = os.path.join(os.path.dirname(c), "antecedentes", etiqueta)
    os.makedirs(ant, exist_ok=True)
    reg = {"fecha": dt.datetime.now().isoformat(timespec="seconds"), "expediente": c, "motivo": motivo, "apartados": {}}
    for n in nombres:
        p = os.path.join(c, n)
        if os.path.exists(p):
            reg["apartados"][n] = hashlib.sha256(open(p, "rb").read()).hexdigest()
            shutil.copy2(p, os.path.join(ant, n))
            os.remove(p)
    res = os.path.join(os.path.dirname(c), "resultados")
    os.makedirs(res, exist_ok=True)
    json.dump(reg, open(os.path.join(res, f"apartado_{etiqueta}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps(reg, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
