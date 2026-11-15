#!/usr/bin/env python3
"""Ejecuta, uno detrás de otro, los controles de las entregas anteriores sobre el árbol actual (encargo 4.12 §9: «los controles
históricos afectados, distinguiendo diferencias esperadas documentadas de regresiones nuevas»). Va DESPUÉS de
`bash verificar_paquete.sh completa`, sobre una descompresión limpia, nunca a la vez que otra tarea con LibreOffice.

Uso (desde munger_v2_r1/): python3 -I -B …/scripts/controles_historicos_4_12.py CARPETA_SALIDA
Escribe en CARPETA_SALIDA una salida por control (`<nombre>.txt`, con el código al final) y `resumen.json`/`resumen.md`: código,
última línea y, si el control tiene salida de referencia en su entrega, si la salida es idéntica a ella. No decide si una diferencia es
esperada: eso lo explica `resultados/LEEME_CONTROLES_HISTORICOS_4_12.md`, con las salidas de referencia del árbol 4.12.
"""
import json
import os
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
EXP = os.path.dirname(AQUI)
RAIZ = os.path.abspath(os.path.join(EXP, "..", "..", ".."))
C = "personaje_v2/empresas_v2_correcciones/"
R411 = C + "2026-11_Vidrala_ensayo_4_11/resultados/"
# salida del mismo control sobre el árbol 4.11 (LEEME de la 4.11): sirve para ver qué cambia de la 4.11 a la 4.12
EN_4_11 = {"4_6_comprobar_cierre_ensayo": "comprobar_cierre_ensayo_4_6_en_arbol_4_11.txt", "4_8_1_comparar_baterias_4_7_1_en_4_8_1": "comparar_baterias_4_7_1_en_4_8_1_en_arbol_4_11.txt",
           "4_7_comprobar_entrega": "comprobar_entrega_4_7_en_arbol_4_11.txt", "4_7_1_comprobar_entrega": "comprobar_entrega_4_7_1_en_arbol_4_11.txt",
           "4_8_comprobar_entrega": "comprobar_entrega_4_8_en_arbol_4_11.txt", "4_8_comparar_baterias_4_7_1": "comparar_baterias_4_7_1_de_4_8_en_arbol_4_11.txt",
           "4_8_1_comprobar_entrega": "comprobar_entrega_4_8_1_en_arbol_4_11.txt", "4_9_comprobar_entrega": "comprobar_entrega_4_9_en_arbol_4_11.txt",
           "4_10_comprobar_entrega": "comprobar_entrega_4_10_en_arbol_4_11.txt", "4_10_1_comprobar_entrega": "comprobar_entrega_4_10_1_en_arbol_4_11.txt",
           "4_11_comprobar_entrega": "comprobar_entrega_4_11_salida.txt"}
# (nombre, script, salida de referencia en su propia entrega o None)
CONTROLES = [
    ("4_2_contraste_2023_arrendamientos", "contrastes/vidrala_2023_arrendamientos/scripts/contraste_2023_arrendamientos.py", "contrastes/vidrala_2023_arrendamientos/resultados/contraste_salida.txt"),
    ("4_3_revision_financiera", "contrastes/vidrala_revision_financiera/scripts/revision_financiera_vidrala.py", "contrastes/vidrala_revision_financiera/resultados/revision_salida.txt"),
    ("4_3_1_subsanacion", "contrastes/vidrala_revision_financiera/scripts/subsanacion_entradas_fechas.py", "contrastes/vidrala_revision_financiera/resultados/subsanacion_salida.txt"),
    ("4_4_comprobar_ensayo", C + "2026-11_Vidrala_ensayo/scripts/comprobar_ensayo.py", C + "2026-11_Vidrala_ensayo/resultados/comprobar_ensayo_salida.txt"),
    ("4_5_comprobar_continuacion", C + "2026-11_Vidrala_ensayo_4_5/scripts/comprobar_continuacion.py", C + "2026-11_Vidrala_ensayo_4_5/resultados/comprobar_continuacion_salida.txt"),
    ("4_6_1_comprobar_vigencia_ensayo", C + "2026-11_Vidrala_ensayo_4_6_1/scripts/comprobar_vigencia_ensayo.py", C + "2026-11_Vidrala_ensayo_4_6_1/resultados/comprobar_vigencia_ensayo_salida.txt"),
    ("4_6_comprobar_cierre_ensayo", C + "2026-11_Vidrala_ensayo_4_6/scripts/comprobar_cierre_ensayo.py", None),
    ("4_8_1_comparar_baterias_4_7_1_en_4_8_1", C + "2026-11_Vidrala_ensayo_4_8_1/scripts/comparar_baterias_4_7_1_en_4_8_1.py", None),
    ("4_7_comprobar_entrega", C + "2026-11_Vidrala_ensayo_4_7/scripts/comprobar_entrega_4_7.py", None),
    ("4_7_1_comprobar_entrega", C + "2026-11_Vidrala_ensayo_4_7_1/scripts/comprobar_entrega_4_7_1.py", None),
    ("4_8_comprobar_entrega", C + "2026-11_Vidrala_ensayo_4_8/scripts/comprobar_entrega_4_8.py", None),
    ("4_8_comparar_baterias_4_7_1", C + "2026-11_Vidrala_ensayo_4_8/scripts/comparar_baterias_4_7_1.py", None),
    ("4_8_1_comprobar_entrega", C + "2026-11_Vidrala_ensayo_4_8_1/scripts/comprobar_entrega_4_8_1.py", None),
    ("4_9_comprobar_entrega", C + "2026-11_Vidrala_ensayo_4_9/scripts/comprobar_entrega_4_9.py", None),
    ("4_10_comprobar_entrega", C + "2026-11_Vidrala_ensayo_4_10/scripts/comprobar_entrega_4_10.py", None),
    ("4_10_1_comprobar_entrega", C + "2026-11_Vidrala_ensayo_4_10_1/scripts/comprobar_entrega_4_10_1.py", None),
    ("4_11_comprobar_entrega", C + "2026-11_Vidrala_ensayo_4_11/scripts/comprobar_entrega_4_11.py", C + "2026-11_Vidrala_ensayo_4_11/resultados/comprobar_entrega_4_11_salida.txt"),
    ("4_12_comprobar_entrega", C + "2026-11_Vidrala_ensayo_4_12/scripts/comprobar_entrega_4_12.py", None),
]


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    out = os.path.abspath(sys.argv[1])
    os.makedirs(out, exist_ok=True)
    filas = []
    for nombre, script, ref in CONTROLES:
        r = subprocess.run([sys.executable, "-I", "-B", script], cwd=RAIZ, capture_output=True, text=True)
        salida = r.stdout + r.stderr
        open(os.path.join(out, f"{nombre}.txt"), "w", encoding="utf-8").write(salida)
        ultima = (salida.strip().splitlines() or [""])[-1]
        identica = igual_4_11 = None
        if ref and os.path.exists(os.path.join(RAIZ, ref)):
            identica = open(os.path.join(RAIZ, ref), encoding="utf-8").read() == r.stdout
        r411 = os.path.join(RAIZ, R411 + EN_4_11[nombre]) if nombre in EN_4_11 else None
        if r411 and os.path.exists(r411):
            igual_4_11 = open(r411, encoding="utf-8").read() == r.stdout
        filas.append({"control": nombre, "script": script, "codigo": r.returncode, "ultima_linea": ultima[:300], "referencia": ref, "identica_a_su_referencia": identica,
                      "salida_en_el_arbol_4_11": (R411 + EN_4_11[nombre]) if nombre in EN_4_11 else None, "igual_que_en_el_arbol_4_11": igual_4_11})
        print(f"{nombre:42s} código {r.returncode} · {ultima[:150]}" + ("" if identica is None else f" · idéntica a su referencia: {identica}")
              + ("" if igual_4_11 is None else f" · igual que en el árbol 4.11: {igual_4_11}"), flush=True)
    json.dump(filas, open(os.path.join(out, "resumen.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    sn = lambda x: "—" if x is None else ("sí" if x else "no")  # noqa: E731
    md = ["# Controles históricos sobre el árbol actual", "", "| Control | Código | Última línea | ¿Idéntica a su referencia? | ¿Igual que en el árbol 4.11? |", "|---|---|---|---|---|"]
    md += [f"| {f['control']} | {f['codigo']} | {f['ultima_linea']} | {sn(f['identica_a_su_referencia'])} | {sn(f['igual_que_en_el_arbol_4_11'])} |" for f in filas]
    open(os.path.join(out, "resumen.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
