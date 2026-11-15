#!/usr/bin/env python3
"""H2 · línea de base, con el código ACTUAL, de los casos que añade el contrato de reparación (10–14).

Uso: python3 -I -B h2_casos_contrato.py RUTA_SCRIPTS SALIDA_JSON
"""
import json
import sys

scripts, salida = sys.argv[1], sys.argv[2]
sys.path.insert(0, scripts)
import pipeline  # noqa: E402

V = pipeline.Pipeline.veredicto_auditoria
pts = {n: f"{n}. PASA · prueba {n}" for n in range(1, 17)}


def txt(lineas, veredicto="APROBADO"):
    return "\n".join(lineas) + f"\nVeredicto: {veredicto}\n"


C = {
    "10_punto_5_duplicado": txt([pts[n] for n in range(1, 17)] + ["5. PASA · prueba 5 repetida"]),
    "11_falta_el_punto_12": txt([pts[n] for n in range(1, 17) if n != 12]),
    "12_todo_pasa_veredicto_repetir": txt([pts[n] for n in range(1, 17)], "REPETIR"),
    "13_aviso_en_punto_que_pasa": txt([pts[n] if n != 7 else "7. PASA · tesis con hechos. Aviso: una cifra sin página" for n in range(1, 17)]),
    "14_palabra_FALLA_en_texto_de_punto_que_pasa": txt([pts[n] if n != 6 else "6. PASA · ninguna cita FALLA en el corpus" for n in range(1, 17)]),
}
R = [{"caso": k, "texto": t, "codigo_actual": V(t)} for k, t in C.items()]
json.dump(R, open(salida, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for r in R:
    print(f"{r['caso']:46s} {r['codigo_actual']}")
