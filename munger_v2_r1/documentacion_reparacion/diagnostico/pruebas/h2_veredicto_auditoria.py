#!/usr/bin/env python3
"""H2 · Prueba de Pipeline.veredicto_auditoria con entradas mínimas y con las auditorías reales.

Uso: python3 -I -B h2_veredicto_auditoria.py RUTA_SCRIPTS DIR_EMPRESAS SALIDA_JSON
Importa pipeline.py de la COPIA (no lo modifica) y llama al método estático con cada texto.
Además, para cada auditoria.md real, mide lo que el formato documentado exige (Anexo D §D.9 y
prompts/verificacion.md): 16 puntos numerados 1–16, cada uno con PASA o FALLA como primera palabra.
"""
import glob
import json
import os
import re
import sys

scripts, empresas, salida = sys.argv[1], sys.argv[2], sys.argv[3]
sys.path.insert(0, scripts)
import pipeline  # noqa: E402

V = pipeline.Pipeline.veredicto_auditoria


def formato(txt):
    """Comprobación del formato DOCUMENTADO (no del código): puntos 1–16 presentes, una vez, con PASA/FALLA."""
    puntos = {}
    for l in txt.splitlines():
        m = re.match(r"^\s*(\d{1,2})\.\s+\**\s*(PASA|FALLA)\b", l)
        if m:
            puntos.setdefault(int(m.group(1)), []).append(m.group(2))
    faltan = [n for n in range(1, 17) if n not in puntos]
    repetidos = [n for n, v in puntos.items() if len(v) > 1]
    fallas = sorted(n for n, v in puntos.items() if "FALLA" in v)
    return {"puntos_presentes": len([n for n in puntos if 1 <= n <= 16]), "faltan": faltan, "repetidos": repetidos,
            "puntos_con_FALLA": fallas, "cumple_formato_16": not faltan and not repetidos}


SINT = {
    "1_solo_veredicto": "Veredicto: APROBADO\n",
    "2_falla_8_y_aprobado": "8. FALLA · hecho material inventado\nVeredicto: APROBADO\n",
    "3a_falla_bloqueante_1": "1. FALLA · verificar_v63.py no íntegro\nVeredicto: APROBADO\n",
    "3b_falla_bloqueante_11": "11. FALLA · rango sin hecho propio\nVeredicto: APROBADO\n",
    "3c_falla_bloqueante_16": "16. FALLA · faltan datos ausentes por revisar\nVeredicto: APROBADO\n",
    "4_vacio": "",
    "5_veredicto_con_coletilla": "Veredicto: APROBADO con reservas\n",
    "6_dos_veredictos": "Veredicto: APROBADO\nVeredicto: REPETIR\n",
}
# 16 puntos completos con FALLA en un punto no bloqueante (2, 3, 5–10, 13–15) y APROBADO
completo = "\n".join(f"{n}. PASA · prueba {n}" for n in range(1, 17))
SINT["7_dieciseis_puntos_falla_8_aprobado"] = completo.replace("8. PASA · prueba 8", "8. FALLA · hecho material inventado") + "\nVeredicto: APROBADO\n"
SINT["8_dieciseis_puntos_todos_falla_no_bloqueantes"] = "\n".join(
    f"{n}. {'PASA' if n in (1, 4, 11, 12, 16) else 'FALLA'} · prueba {n}" for n in range(1, 17)) + "\nVeredicto: APROBADO\n"
SINT["9_dieciseis_puntos_todo_pasa"] = completo + "\nVeredicto: APROBADO\n"

R = {"sinteticos": [], "reales": []}
for k, t in SINT.items():
    R["sinteticos"].append({"caso": k, "texto": t, "codigo_devuelve": V(t), "formato_documentado": formato(t)})
for f in sorted(glob.glob(os.path.join(empresas, "*", "auditoria*.md"))):
    t = open(f, encoding="utf-8").read()
    R["reales"].append({"archivo": os.path.relpath(f, empresas), "codigo_devuelve": V(t), "formato_documentado": formato(t)})

json.dump(R, open(salida, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for r in R["sinteticos"]:
    fd = r["formato_documentado"]
    print(f"SINT {r['caso']:45s} código={r['codigo_devuelve']:9s} formato16={fd['cumple_formato_16']!s:5s} FALLA en {fd['puntos_con_FALLA']}")
for r in R["reales"]:
    fd = r["formato_documentado"]
    print(f"REAL {r['archivo']:45s} código={r['codigo_devuelve']:9s} formato16={fd['cumple_formato_16']!s:5s} presentes={fd['puntos_presentes']} FALLA en {fd['puntos_con_FALLA']}")
