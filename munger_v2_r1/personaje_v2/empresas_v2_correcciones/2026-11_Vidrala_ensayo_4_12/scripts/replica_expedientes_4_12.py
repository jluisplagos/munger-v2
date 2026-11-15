#!/usr/bin/env python3
"""Réplica independiente de la 4.11 sobre los libros FINALES de un expediente real de la 4.12 (encargo 4.12 §9, entregable 2: «variantes,
conciliaciones y réplicas»). No usa LibreOffice: lee los libros ya recalculados por el pipeline.

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
R411 = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_11", "scripts")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    c = os.path.abspath(sys.argv[1])
    emp = os.path.basename(c)
    sys.path.insert(0, os.path.join(PV, "scripts"))
    sys.path.insert(0, R411)
    import configuracion_economica as CE
    import replica_independiente_v64 as R
    import variantes_configuracion_v64 as VC
    conf = json.load(open(os.path.join(c, "configuracion_economica.json"), encoding="utf-8"))
    # configuración que DECLARA cada caso (la del expediente y la de cada variante, regenerada con la función pura del paso 10):
    # el grupo 0 de la réplica comprueba que las celdas de entrada del libro son esas
    confs = {k: cv for k, _, cv in VC.variantes(conf)}
    confs["activa_expediente"] = conf
    d = tempfile.mkdtemp(prefix="replica412_")
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
        cel = CE.celdas(confs[k])
        cfg = {f"{CE.HOJA}!{x}": cel.get(f"{CE.HOJA}!{x}") for x in R.CELDAS_CFG}
        casos.append({"id": k, "base": emp, "config": cfg, "entradas": {}, "referencia": ref, "nota": nota, "libro": f"{k}.xlsx", "recalculado": f"rc/{k}.xlsx",
                      "recalculo_ok": True, "motivo_esperado": None})
    json.dump({"plantilla": "V6.4 experimental", "plantilla_sha256": None, "casos": casos}, open(os.path.join(d, "manifiesto_casos.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    R.cargar_definiciones = lambda: (None, "casos de un expediente real de la 4.12: no están en casos_v64.py (el contraste con los 117 casos no aplica)")  # noqa: E731
    res_dir = os.path.join(os.path.dirname(c), "resultados")
    os.makedirs(res_dir, exist_ok=True)
    rc = R.main([d, "--json", os.path.join(res_dir, "replica_independiente.json"), "--txt", os.path.join(res_dir, "replica_independiente.txt")])
    shutil.rmtree(d, ignore_errors=True)
    return rc


if __name__ == "__main__":
    sys.exit(main())
