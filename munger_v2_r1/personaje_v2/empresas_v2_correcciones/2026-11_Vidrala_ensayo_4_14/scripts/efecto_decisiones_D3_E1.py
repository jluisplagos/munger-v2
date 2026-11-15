#!/usr/bin/env python3
"""Efecto separado de las decisiones D3 (acciones de Viscofan) y E1 (medias exactas) sobre el libro evaluado de la RAMA 4.14, en copias
(fases A, B y C de la rama fijas; LibreOffice en secuencia). Exigencia de la persona responsable (14-nov-2026): conciliar el efecto del
denominador solo y separar el de la capitalización (que mueve el peso del patrimonio en la r operativa) y el de cualquier otra entrada.
Fechas distintas: acciones a 31-dic-2025 y precio del 3-nov-2026; no es una actualización a 2026.
Uso (desde munger_v2_r1/): python3 -I …/scripts/efecto_decisiones_D3_E1.py [viscofan|vidrala]"""
import json, os, shutil, sys, tempfile
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import efecto_correcciones_entradas_4_14 as EF  # noqa: E402
E414 = EF.E414
PRECIO, N_NUEVO = 54.70, 45.993399
CASOS = {"viscofan": ("viscofan", "Viscofan", [
    ("rama 4.14 (reproducción)", {}),
    ("D3 · solo el denominador C55 = 45,993399 (E fijo)", {"Análisis!C55": N_NUEVO}),
    ("D3 · solo la capitalización C41 = 54,70 × 45,993399 (denominador sin cambiar)", {"Análisis!C41": round(PRECIO * N_NUEVO, 6)}),
    ("D3 · denominador y capitalización (E recalculado)", {"Análisis!C55": N_NUEVO, "Análisis!C41": round(PRECIO * N_NUEVO, 6)}),
    ("E1 · medias exactas C47–C50", {"Análisis!C47": 77.533, "Análisis!C48": 8.294, "Análisis!C49": 5.547, "Análisis!C50": 3.707}),
    ("D3 + E1 · todo", {"Análisis!C55": N_NUEVO, "Análisis!C41": round(PRECIO * N_NUEVO, 6), "Análisis!C47": 77.533, "Análisis!C48": 8.294, "Análisis!C49": 5.547, "Análisis!C50": 3.707})]),
    "vidrala": ("vidrala", "Vidrala", [("rama 4.14 (reproducción)", {}), ("E1 · medias exactas C46 y C47", {"Análisis!C46": 335.413, "Análisis!C47": 169.668})])}


def main():
    clave = (sys.argv[1] if len(sys.argv) > 1 else "viscofan").lower()
    carp, E, casos = CASOS[clave]
    rama = os.path.join(E414, carp, E)
    libro = os.path.join(rama, f"{E}_v63_evaluada.xlsx")
    pr0 = json.load(open(os.path.join(rama, "precio.json"), encoding="utf-8"))
    tmp = tempfile.mkdtemp(prefix=f"d3e1_{clave}_")
    os.makedirs(os.path.join(tmp, "recalc"))
    filas = []
    try:
        for i, (nombre, cs) in enumerate(casos):
            r = EF.recalcular(libro, cs, f"c{i}", tmp, os.path.join(tmp, ".lo_perfil"))
            rj = json.load(open(os.path.join(tmp, f"c{i}.resultados.json"), encoding="utf-8"))
            r["r_operativa"] = rj.get("r_operativa_C15")
            filas.append({"caso": nombre, "celdas": cs, **r})
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    p0 = filas[0]["precio_si"]
    for f in filas:
        f["delta_frente_a_la_rama"] = f["precio_si"] - p0
    out = {"empresa": E, "libro": os.path.relpath(libro, EF.PV), "precio_si_rama": pr0["precio_si"], "reproduce": abs(p0 - pr0["precio_si"]) <= 1e-9,
           "fechas": "acciones a 31-dic-2025 (cuentas de 2025); precio del 3-nov-2026: fechas distintas, no es una actualización a 2026", "casos": filas}
    os.makedirs(os.path.join(E414, "resultados"), exist_ok=True)
    json.dump(out, open(os.path.join(E414, "resultados", f"efecto_decisiones_{clave}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    for f in filas:
        print(f"{f['caso']:85s} precio de Sí {f['precio_si']:.5f} · Δ rama {f['delta_frente_a_la_rama']:+.5f} · r_op {f['r_operativa']} · {f['zona']}")
    print("reproduce la rama:", out["reproduce"])


if __name__ == "__main__":
    main()
