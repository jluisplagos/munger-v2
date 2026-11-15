#!/usr/bin/env python3
"""Comparación del expediente de continuación (4.5) con el original (empresas_v2/Vidrala/). Solo lectura de ambos.

Uso: python3 -I comparar_con_original.py [--salida resultados/comparacion_con_original.md]

Compara: entradas (fase1_v63.json, valores de Historia), las 68 celdas de juicio (libros evaluados), las celdas numéricas de
Historia (libros recalculados), estados (pipeline, libro, ficha) y resultados mecánicos (precio.json, resultados.json).
El original es la ejecución anterior (motor A, P1 sin corregir): se compara para documentar diferencias, no se reutiliza.
"""
import argparse
import json
import os
import sys

sys.dont_write_bytecode = True
AQUI = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PV2 = os.path.abspath(os.path.join(AQUI, "..", ".."))
sys.path.insert(0, os.path.join(PV2, "scripts"))
import celdas_v2 as C  # noqa: E402
import openpyxl  # noqa: E402

E = os.path.join(AQUI, "Vidrala")
O = os.path.join(PV2, "empresas_v2", "Vidrala")


def j(d, f):
    return json.load(open(os.path.join(d, f), encoding="utf-8"))


def fmt(x):
    if x is None:
        return "(vacía)"
    if isinstance(x, float):
        return f"{x:.6g}"
    s = str(x).replace("\n", " ").replace("|", "/")
    return s if len(s) <= 90 else s[:87] + "…"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--salida", default=os.path.join(AQUI, "resultados", "comparacion_con_original.md"))
    a = ap.parse_args()
    L = ["# Comparación con el expediente original · Vidrala (entrega 4.5)", "",
         "Original: `personaje_v2/empresas_v2/Vidrala/` (ejecución anterior, motor A, circulante de 2024 sin P1). Ensayo: `2026-11_Vidrala_ensayo_4_5/Vidrala/`. "
         "Generado por `scripts/comparar_con_original.py`. Los resultados son **mecánicos**; ninguna de las dos columnas es una valoración comparable con el precio.", ""]

    # 1. entradas
    fo, fn = j(O, "fase1_v63.json"), j(E, "fase1_v63.json")
    anios = fo["historia"]["anios"]
    L += ["## 1. Entradas (Historia de fase1_v63.json)", "", "| Partida | Año | Original | Ensayo |", "|---|---|---|---|"]
    n = 0
    for k, v in fo["historia"]["partidas"].items():
        for i, (x, y) in enumerate(zip(v["valores"], fn["historia"]["partidas"][k]["valores"])):
            if x != y:
                L.append(f"| {k} | {anios[i]} | {fmt(x)} | {fmt(y)} |")
                n += 1
    meta = [k for k in ("precio", "acciones_diluidas", "capitalizacion", "fecha_analisis", "tasa_sin_riesgo") if fo.get(k) != fn.get(k)]
    L += ["", f"Diferencias de valor: {n}. Metadatos distintos: {meta or 'ninguno'}. Ceros pendientes de verificación en el ensayo: {len(fn.get('pendientes_verificacion', []))} (el original no los marcaba: se construyó antes de la reparación H1).", ""]

    # 2. celdas de juicio
    wo = openpyxl.load_workbook(os.path.join(O, "Vidrala_v63_evaluada.xlsx"))
    wn = openpyxl.load_workbook(os.path.join(E, "Vidrala_v63_evaluada.xlsx"))
    L += ["## 2. Celdas de juicio (68) en el libro evaluado", "", "| Celda | Fase | Original | Ensayo |", "|---|---|---|---|"]
    iguales = dist = 0
    for hoja, celdas in C.CELDAS.items():
        for ref, meta_c in celdas.items():
            x, y = wo[hoja][ref].value, wn[hoja][ref].value
            if x == y:
                iguales += 1
                continue
            dist += 1
            L.append(f"| {hoja}!{ref} | {meta_c.get('fase')} | {fmt(x)} | {fmt(y)} |")
    L += ["", f"Iguales: {iguales}. Distintas: {dist}. (Las iguales no prueban que se heredaran: las fases del ensayo las decidieron de nuevo; ver sus Observaciones.)", ""]

    # 3. Historia recalculada (numérica)
    ho = openpyxl.load_workbook(os.path.join(O, "Vidrala_v63_evaluada.xlsx"), data_only=True)["Historia"]
    hn = openpyxl.load_workbook(os.path.join(E, "recalc", "Vidrala_v63_evaluada.xlsx"), data_only=True)["Historia"]
    L += ["## 3. Historia: celdas numéricas distintas (libros evaluados recalculados)", "", "| Celda | Original | Ensayo |", "|---|---|---|"]
    for row in ho.iter_rows():
        for c in row:
            x, y = c.value, hn[c.coordinate].value
            if isinstance(x, (int, float)) and isinstance(y, (int, float)) and abs(x - y) > 1e-9:
                L.append(f"| {c.coordinate} | {x:.6g} | {y:.6g} |")
    L.append("")

    # 4. estados y resultados
    so, sn = j(O, "estado_pipeline.json"), j(E, "estado_pipeline.json")
    po, pn = j(O, "precio.json"), j(E, "precio.json")
    ro, rn = j(O, "resultados.json"), j(E, "resultados.json")
    ficho, fichn = j(O, "ficha.json"), j(E, "ficha.json")
    filas = [
        ("Estado del análisis", so.get("estado_analisis"), sn.get("estado_analisis")),
        ("Auditoría", so.get("auditoria"), sn.get("auditoria")),
        ("Motor (C62)", ro.get("motor"), rn.get("motor")),
        ("f (Historia C58)", ro.get("f"), rn.get("f")),
        ("Tasa de descuento del motor", ro["valores"].get("C56") if ro.get("motor") == "A" else ro.get("r_operativa_C15"), rn["valores"].get("C56") if rn.get("motor") == "A" else rn.get("r_operativa_C15")),
        ("r (C56)", ro["valores"].get("C56"), rn["valores"].get("C56")),
        ("Pasivos netos del puente (C16, motor B)", ro.get("pasivos_netos_B_C16"), rn.get("pasivos_netos_B_C16")),
        ("Valor por acción MALO", po["V"][0], pn["V"][0]),
        ("Valor por acción NORMAL", po["V"][1], pn["V"][1]),
        ("Valor por acción BUENO", po["V"][2], pn["V"][2]),
        ("Probabilidades", po["p"], pn["p"]),
        ("Ponderado (mecánico)", po["ponderado"], pn["ponderado"]),
        ("Precio de Sí (mecánico)", po["precio_si"], pn["precio_si"]),
        ("Zona (mecánica)", po["zona"], pn["zona"]),
        ("Precio de la hoja (C37)", po["precio"], pn["precio"]),
        ("Cubo", ficho.get("cubo"), fichn.get("cubo")),
        ("Estado del libro", ficho.get("estado_libro"), fichn.get("estado_libro")),
        ("Estado de las evidencias", ficho.get("estado_evidencias"), fichn.get("estado_evidencias")),
        ("Análisis!C104", wo["Análisis"]["C104"].value, wn["Análisis"]["C104"].value),
    ]
    L += ["## 4. Estados y resultados mecánicos", "", "| Concepto | Original | Ensayo |", "|---|---|---|"] + [f"| {a_} | {fmt(b)} | {fmt(c)} |" for a_, b, c in filas]
    L += ["", "Los valores del original y del ensayo no son comparables entre sí como valoraciones: cambian el dato de 2024 (P1), el motor, las palancas decididas de nuevo y la fecha de referencia del valor (motor B: 31-dic-2025, con derecho al dividendo a cuenta)."]
    os.makedirs(os.path.dirname(a.salida), exist_ok=True)
    open(a.salida, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print(f"OK: {a.salida} · {n} diferencias de entrada · {dist} celdas de juicio distintas de 68")


if __name__ == "__main__":
    main()
