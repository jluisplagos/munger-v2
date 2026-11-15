#!/usr/bin/env python3
"""Réplica independiente sobre los libros FINALES de un expediente real de la 4.13 (copia de `…_4_12/scripts/replica_expedientes_4_12.py`).
No usa LibreOffice: lee los libros ya recalculados por el pipeline. (4.13) Usa `replica_independiente_v641.py` (esta carpeta): la réplica de
la 4.11 con el perímetro de la inversión de la V6.4.1 añadido desde su definición económica; con «Caja» o sin perímetro es la de la 4.11.

Por cada libro recalculado del expediente —el evaluado (`recalc/<E>_v63_evaluada.xlsx`) y cada variante del paso 10
(`variantes_v64/recalc/<clave>.xlsx`)— arma un caso con la referencia de su `precio.json` (V, ponderado y precio de Sí; tolerancia
1e-9 €/acción) y ejecuta la réplica de la 4.11 (`…_4_11/scripts/replica_independiente_v64.py`, sin cambios), que recalcula la valoración
del motor B desde las entradas del libro sin leer ninguna fórmula de la hoja nueva ni las columnas BU:DY del Motor. Como estos casos
no están en `casos_v64.py` (son libros de expedientes reales), la réplica se llama sin esa definición: el contraste del manifiesto
con los 117 casos no aplica aquí.
Uso (desde munger_v2_r1/): python3 -I …/scripts/replica_expedientes_4_12.py CARPETA_EMPRESA
Escribe CARPETA_EMPRESA/../resultados/replica_independiente.json y .txt. Código 0 si todos los casos coinciden.
"""
import json
import os
import shutil
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
EXP = os.path.dirname(AQUI)
PV = os.path.abspath(os.path.join(EXP, "..", ".."))
R411 = AQUI  # (4.13) replica_independiente_v641.py


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    c = os.path.abspath(sys.argv[1])
    emp = os.path.basename(c)
    sys.path.insert(0, os.path.join(PV, "scripts"))
    sys.path.insert(0, R411)
    import configuracion_economica as CE
    import replica_independiente_v641 as R
    import variantes_configuracion_v64 as VC
    conf = json.load(open(os.path.join(c, "configuracion_economica.json"), encoding="utf-8"))
    # configuración que DECLARA cada caso (la del expediente y la de cada variante, regenerada con la función pura del paso 10):
    # el grupo 0 de la réplica comprueba que las celdas de entrada del libro son esas
    confs = {k: cv for k, _, cv in VC.variantes(conf)}
    confs["activa_expediente"] = conf
    d = tempfile.mkdtemp(prefix="replica413_")
    os.makedirs(os.path.join(d, "rc"))
    casos = []
    libros = [("activa_expediente", os.path.join(c, "recalc", f"{emp}_v63_evaluada.xlsx"), os.path.join(c, "precio.json"), "libro evaluado del expediente")]
    vdir = os.path.join(c, "variantes_v64")
    for f in sorted(os.listdir(os.path.join(vdir, "recalc"))):
        if f.endswith(".xlsx"):
            k = f[:-5]
            libros.append((k, os.path.join(vdir, "recalc", f), os.path.join(vdir, f"{k}.precio.json"), f"variante {k} del paso 10"))
    for k, libro, pj, nota in libros:
        if not (os.path.exists(libro) and os.path.exists(pj)):
            continue
        pr = json.load(open(pj, encoding="utf-8"))
        shutil.copy2(libro, os.path.join(d, "rc", f"{k}.xlsx"))
        ref = None
        if all(isinstance(x, (int, float)) for x in (pr.get("V") or [None])) and isinstance(pr.get("ponderado"), (int, float)):
            ref = {"V": pr["V"], "ponderado": pr["ponderado"], "precio_si": pr.get("precio_si"), "fuente": os.path.relpath(pj, os.path.dirname(c)), "tol": 1e-9, "tol_V": 1e-9}
        cel = CE.celdas(confs[k], v641=CE.declara_perimetro(conf))  # (4.13) en un libro V6.4.1 las celdas del perímetro no declarado van vacías
        cfg = {f"{CE.HOJA}!{x}": cel.get(f"{CE.HOJA}!{x}") for x in R.CELDAS_CFG}
        casos.append({"id": k, "base": emp, "config": cfg, "entradas": {}, "referencia": ref, "nota": nota, "libro": f"{k}.xlsx", "recalculado": f"rc/{k}.xlsx",
                      "recalculo_ok": True, "motivo_esperado": None})
    json.dump({"plantilla": json.load(open(os.path.join(c, "plantilla_activa.json"), encoding="utf-8")).get("version"), "plantilla_sha256": None, "casos": casos}, open(os.path.join(d, "manifiesto_casos.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    R.cargar_definiciones = lambda: (None, "casos de un expediente real de la 4.13: no están en casos_v64.py (el contraste con los 117 casos no aplica)")  # noqa: E731
    res_dir = os.path.join(os.path.dirname(c), "resultados")
    os.makedirs(res_dir, exist_ok=True)
    rc = R.main([d, "--json", os.path.join(res_dir, "replica_independiente.json"), "--txt", os.path.join(res_dir, "replica_independiente.txt")])
    shutil.rmtree(d, ignore_errors=True)
    return rc


if __name__ == "__main__":
    sys.exit(main())
