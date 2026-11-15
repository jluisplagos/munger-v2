#!/usr/bin/env python3
"""Efecto separado de la decisión E6 de Elis (base coherente a 31-dic-2025) sobre el libro evaluado del expediente ANTERIOR
(elis_motor_A, motor A, V6.3), en copias: fases A, B y C del anterior fijas; LibreOffice en secuencia. Exigencia de la persona responsable
(14-nov-2026): «Recalcular, mostrar los efectos separados». Cada grupo se mide solo y después todos juntos; el caso «todo» se compara con
el precio de Sí del expediente nuevo (elis_decisiones), que rehízo las fases con agentes reales. Aparte, la dilución potencial (NO
incorporada) sobre el caso «todo»: conversión de la OCEANE (acciones + 23,355764 M y sin su cupón en C48) y acciones de rendimiento (cota: el coste de esas acciones ya resta en C50 como SBC, así que sumar las acciones puede contarlo dos veces en parte; aviso de la auditoría
SA-d58921ca0d0cf0fa, condición e).
Fechas distintas: acciones a 31-dic-2025 y precio del 4-nov-2026; no es una actualización a 2026. Advertencia de alcance: motor A con
arrendamientos NIIF 16 (hallazgo F1): el precio de Sí no es una conclusión utilizable.
Uso (desde munger_v2_r1/): python3 -I …/scripts/efecto_decisiones_E6_elis.py"""
import json
import os
import shutil
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import efecto_correcciones_entradas_4_14 as EF  # noqa: E402

E414 = EF.E414
PRECIO = 24.18
N = 232.47681
N_OCEANE = 23.355764
N_RENDIMIENTO, N_RENDIMIENTO_MAX = 2.613905, 3.136686
CUPON_OCEANE = 8.55  # 2,25 % × 380,0 (URD 2025, PDF p. 380)
ACCIONES = {"Análisis!C55": N, "Análisis!C41": round(PRECIO * N, 7)}
PENSIONES = {"Historia!I25": 47.4, "Historia!J25": 74.9, "Historia!K25": 91.6, "Historia!L25": 67.1}
MEDIAS = {"Análisis!C46": 1429.433, "Análisis!C47": 857.167, "Análisis!C50": 28.233}
REEXPRESADAS = {"Análisis!C24": 0.097, "Análisis!C31": "Sí", "Análisis!C33": 2.22, "Análisis!C34": "No", "Análisis!C40": 323.9,
                "Análisis!C42": 5.53, "Análisis!C53": 398.1, "Análisis!C54": 4121.5}
TODO = {**ACCIONES, **PENSIONES, **MEDIAS, **REEXPRESADAS}
CASOS = [
    ("expediente anterior elis_motor_A (reproducción)", {}),
    ("E6 · solo el denominador C55 = 232,47681 (E fijo)", {"Análisis!C55": N}),
    ("E6 · solo la capitalización C41 = 24,18 × 232,47681", {"Análisis!C41": ACCIONES["Análisis!C41"]}),
    ("E6 · acciones y capitalización", ACCIONES),
    ("E6 · pensiones I25:L25 (déficit de prestación definida)", PENSIONES),
    ("supuesto de la orquestación (precedente E1) · medias exactas C46, C47, C50", MEDIAS),
    ("E6 · entradas reexpresadas a 2025 (C24, C31, C33, C34, C40, C42, C53, C54)", REEXPRESADAS),
    ("E6 · todo", TODO),
    ("dilución potencial (NO incorporada) · conversión de la OCEANE: + 23,355764 M acciones y C48 sin el cupón",
     {**TODO, "Análisis!C55": N + N_OCEANE, "Análisis!C41": round(PRECIO * (N + N_OCEANE), 7), "Análisis!C48": round(108.0 - CUPON_OCEANE, 3)}),
    ("dilución potencial (NO incorporada) · acciones de rendimiento vivas (+ 2,613905 M) · COTA: C50 (SBC) sigue restando su coste, posible doble cómputo parcial",
     {**TODO, "Análisis!C55": N + N_RENDIMIENTO, "Análisis!C41": round(PRECIO * (N + N_RENDIMIENTO), 7)}),
    ("dilución potencial (NO incorporada) · acciones de rendimiento al 120 % (+ 3,136686 M) · COTA: C50 (SBC) sigue restando su coste, posible doble cómputo parcial",
     {**TODO, "Análisis!C55": N + N_RENDIMIENTO_MAX, "Análisis!C41": round(PRECIO * (N + N_RENDIMIENTO_MAX), 7)}),
]


def main():
    ant = os.path.join(E414, "elis_motor_A", "Elis")
    nuevo = os.path.join(E414, "elis_decisiones", "Elis")
    libro = os.path.join(ant, "Elis_v63_evaluada.xlsx")
    pr_ant = json.load(open(os.path.join(ant, "precio.json"), encoding="utf-8"))
    pr_nuevo = json.load(open(os.path.join(nuevo, "precio.json"), encoding="utf-8"))
    tmp = tempfile.mkdtemp(prefix="e6_elis_")
    os.makedirs(os.path.join(tmp, "recalc"))
    filas = []
    try:
        for i, (nombre, cs) in enumerate(CASOS):
            r = EF.recalcular(libro, cs, f"c{i}", tmp, os.path.join(tmp, ".lo_perfil"))
            filas.append({"caso": nombre, "celdas": cs, **r})
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    p0 = filas[0]["precio_si"]
    p_todo = next(f["precio_si"] for f in filas if f["caso"] == "E6 · todo")
    for f in filas:
        f["delta_frente_al_anterior"] = f["precio_si"] - p0
        f["delta_frente_a_todo"] = (f["precio_si"] - p_todo) if f["caso"].startswith("dilución") else None
    out = {"empresa": "Elis", "libro": os.path.relpath(libro, EF.PV), "precio_si_anterior": pr_ant["precio_si"],
           "reproduce_el_anterior": abs(p0 - pr_ant["precio_si"]) <= 1e-9, "precio_si_expediente_nuevo": pr_nuevo["precio_si"],
           "todo_frente_al_expediente_nuevo": p_todo - pr_nuevo["precio_si"],
           "naturaleza": "efecto mecánico con las fases del expediente anterior fijas; el expediente nuevo rehízo las fases con agentes reales",
           "fechas": "acciones a 31-dic-2025 (cuentas de 2025); precio del 4-nov-2026: fechas distintas, no es una actualización a 2026",
           "alcance": "motor A con arrendamientos NIIF 16 (hallazgo F1, supuesto (a)): el precio de Sí no es una conclusión utilizable",
           "casos": filas}
    res = os.path.join(E414, "resultados")
    os.makedirs(res, exist_ok=True)
    json.dump(out, open(os.path.join(res, "efecto_decisiones_elis_E6.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    g = lambda x: f"{x:.5f}".replace(".", ",") if isinstance(x, (int, float)) else "—"  # noqa: E731
    md = ["# Elis · efecto separado de la decisión E6 (base 31-dic-2025)", "",
          f"Copias del libro evaluado del expediente anterior (`elis_motor_A`), con sus fases fijas, recalculadas con LibreOffice. {out['naturaleza']}. {out['fechas']}. **{out['alcance']}.**", "",
          f"Reproducción del anterior: {'sí' if out['reproduce_el_anterior'] else 'NO'} ({g(p0)} frente a {g(pr_ant['precio_si'])}). Caso «todo» frente al expediente nuevo: {g(p_todo)} frente a {g(pr_nuevo['precio_si'])} (diferencia {g(out['todo_frente_al_expediente_nuevo'])}).", "",
          "| Caso | Precio de Sí | Δ frente al anterior | Δ frente a «todo» | Ponderado | Zona |", "|---|---|---|---|---|---|"]
    for f in filas:
        md.append(f"| {f['caso']} | {g(f['precio_si'])} | {g(f['delta_frente_al_anterior'])} | {g(f['delta_frente_a_todo'])} | {g(f['ponderado'])} | {f['zona']} |")
    open(os.path.join(res, "efecto_decisiones_elis_E6.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main()
