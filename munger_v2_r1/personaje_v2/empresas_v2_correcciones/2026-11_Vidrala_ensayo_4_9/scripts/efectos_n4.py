#!/usr/bin/env python3
"""Efectos de los ceros pendientes de Vidrala sobre la valoración (entrega 4.9, N4). Copias identificadas, recálculo forzado.

Uso: python3 -I efectos_n4.py [--salida DIR]   (desde munger_v2_r1/; usa LibreOffice: no ejecutar en paralelo con otras pruebas)

Parte del libro evaluado del expediente de referencia (…/2026-11_Vidrala_ensayo_4_6_1/Vidrala/Vidrala_v63_evaluada.xlsx), que no
se modifica. Para cada variante escribe una COPIA identificada (escribir_v63.py --copia-de-prueba, que borra las cachés de fórmula),
la recalcula con recalc.sh (recálculo forzado) y lee las salidas de la valoración. Las copias no heredan la aprobación de la
referencia ni son resultados oficiales: son cálculos exploratorios con su aviso. Ninguna variante cambia criterios, probabilidades,
rentabilidad exigida ni escenarios.

Variantes:
  - base: la copia sin cambios (debe reproducir los valores del expediente: control de que el recálculo es fiel);
  - unitarias (+1 mm en la celda o la fila): miden la dependencia NUMÉRICA de cada grupo de ceros (el grafo de fórmulas solo da la
    dependencia formal, que pasa por las puertas de validación del libro);
  - hipótesis (etiquetadas como tales, no como cotas): C48 con los intereses de arrendamientos devengados (media 2023–2025 de la
    nota 8: 2,131, 2,179 y 2,452) por si se pagaran dentro de financiación; C48 con los intereses pagados de explotación (media
    2023–2025: 12,320, 32,100 y 20,800), que muestra el efecto de un DOBLE CÓMPUTO (esos intereses ya están restados en el CFO).
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile

import openpyxl

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "scripts")))
import precio_de_si as PS  # noqa: E402

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", "..", "..", ".."))
SCR = os.path.join(RAIZ, "personaje_v2", "scripts")
REF = os.path.join(RAIZ, "personaje_v2", "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_6_1", "Vidrala", "Vidrala_v63_evaluada.xlsx")
SALIDAS = {"MALO (Análisis!B78)": ("Análisis", "B78"), "NORMAL (Análisis!C78)": ("Análisis", "C78"), "BUENO (Análisis!D78)": ("Análisis", "D78"),
           "ponderado (Análisis!C83)": ("Análisis", "C83"), "puente (Diagnóstico V6!C16)": ("Diagnóstico V6", "C16"),
           "FCF simplificado (Análisis!C52)": ("Análisis", "C52"), "f (Diagnóstico V6!C12)": ("Diagnóstico V6", "C12"),
           "control de rango de f (Diagnóstico V6!C50)": ("Diagnóstico V6", "C50"), "estado técnico (Motor!B255)": ("Motor", "B255")}
ESPERADO_BASE = {"MALO (Análisis!B78)": 53.6704195834156, "NORMAL (Análisis!C78)": 70.7721966823599, "BUENO (Análisis!D78)": 86.4887624455832,
                 "ponderado (Análisis!C83)": 70.4951544152157, "puente (Diagnóstico V6!C16)": 160.784, "precio de Sí (precio_de_si.p_estrella, k = 3)": 65.68808732041568}

INT_ARR = (2.131, 2.179, 2.452)        # nota 8, gasto devengado por intereses de arrendamientos 2023–2025 (contraste 4.2)
INT_PAG = (12.320, 32.100, 20.800)     # «Interest paid» / «Pagos de intereses», explotación, 2023–2025 (CF p.7; ES 2025 p.14)

LEEME_COPIAS = 'COPIAS EXPLORATORIAS (entrega 4.9, N4). No son libros oficiales ni heredan la aprobación del expediente de referencia\n(…/2026-11_Vidrala_ensayo_4_6_1/Vidrala/). Cada COPIA_EXPLORATORIA_<variante>.xlsx es el libro evaluado de la referencia con las\nceldas de <variante>.celdas.json escritas por escribir_v63.py --copia-de-prueba (cachés de fórmula borradas). Las regenera\nscripts/efectos_n4.py, que las recalcula con recalc.sh y deja los valores en ../efectos_n4.json. Las variantes «unitaria» miden la\nsensibilidad (+1 mm); las «hipótesis» no son cotas; el «contraejemplo» muestra un doble cómputo y no es una alternativa.\n'


def media(x):
    return round(sum(x) / len(x), 6)


def variantes(valores_base):
    h = valores_base
    v = [("base", "sin cambios", {}, "control")]
    v.append(("L26_mas_1", "Historia!L26 + 1 mm (minoritarios 2025)", {"Historia!L26": h["Historia!L26"] + 1}, "unitaria"))
    v.append(("C26_K26_mas_1", "Historia!C26:K26 + 1 mm (minoritarios 2016–2024)", {f"Historia!{c}26": h[f"Historia!{c}26"] + 1 for c in "CDEFGHIJK"}, "unitaria"))
    v.append(("C48_mas_1", "Análisis!C48 + 1 mm (intereses pagados en financiación, media 2023–2025)", {"Análisis!C48": h["Análisis!C48"] + 1}, "unitaria"))
    v.append(("fila16_mas_1", "Historia!C16:L16 + 1 mm (sin tocar C48, que es un valor escrito por la fase 1)", {f"Historia!{c}16": h[f"Historia!{c}16"] + 1 for c in "CDEFGHIJKL"}, "unitaria"))
    v.append(("E13_I13_mas_1", "Historia!E13:I13 + 1 mm (adquisiciones 2018–2022)", {f"Historia!{c}13": h[f"Historia!{c}13"] + 1 for c in "EFGHI"}, "unitaria"))
    v.append(("C17_E17_mas_1", "Historia!C17 y E17 + 1 mm (principal de arrendamientos 2016 y 2018)", {"Historia!C17": h["Historia!C17"] + 1, "Historia!E17": h["Historia!E17"] + 1}, "unitaria"))
    v.append(("C23_mas_1", "Historia!C23 + 1 mm (pasivo por arrendamientos 2016)", {"Historia!C23": h["Historia!C23"] + 1}, "unitaria"))
    v.append(("H_C48_int_arrend", f"HIPÓTESIS: Análisis!C48 = {media(INT_ARR)} (intereses de arrendamientos devengados, si se pagaran en financiación y C49 = 4,5 no los incluyera)",
              {"Análisis!C48": media(INT_ARR)}, "hipótesis"))
    v.append(("H_C48_doble_computo", f"DOBLE CÓMPUTO (no es una alternativa): Análisis!C48 = {media(INT_PAG)} (intereses pagados que el CFO ya resta)",
              {"Análisis!C48": media(INT_PAG)}, "contraejemplo"))
    return v


def leer(libro, celdas):
    wb = openpyxl.load_workbook(libro, data_only=True)
    return {k: wb[h][c].value for k, (h, c) in celdas.items()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--salida", default=os.path.join(AQUI, "..", "n4", "efectos"))
    a = ap.parse_args()
    out = os.path.abspath(a.salida)
    os.makedirs(out, exist_ok=True)
    wb = openpyxl.load_workbook(REF, data_only=False)
    base_vals = {f"Historia!{c}{r}": (wb["Historia"][f"{c}{r}"].value or 0) for r in (13, 16, 17, 23, 26) for c in "CDEFGHIJKL"}
    base_vals["Análisis!C48"] = wb["Análisis"]["C48"].value or 0
    tmp = tempfile.mkdtemp(prefix="efectos_n4_")  # perfil de LibreOffice y libros recalculados: fuera del paquete
    perfil, recalc = os.path.join(tmp, "perfil_lo"), os.path.join(tmp, "recalc")
    copias = os.path.join(out, "copias")
    os.makedirs(copias, exist_ok=True)
    with open(os.path.join(copias, "LEEME.txt"), "w", encoding="utf-8") as fh:
        fh.write(LEEME_COPIAS)
    filas = []
    for nombre, desc, celdas, tipo in variantes(base_vals):
        cj = os.path.join(copias, f"{nombre}.celdas.json")
        json.dump(celdas, open(cj, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        copia = os.path.join(copias, f"COPIA_EXPLORATORIA_{nombre}.xlsx")
        r = subprocess.run([sys.executable, "-I", os.path.join(SCR, "escribir_v63.py"), REF, copia, "--celdas", cj, "--lista-blanca", "cualquiera", "--copia-de-prueba"], capture_output=True, text=True)
        if r.returncode != 0:
            print(f"FALLO al escribir {nombre}: {r.stdout}{r.stderr}")
            sys.exit(1)
        r = subprocess.run(["bash", os.path.join(SCR, "recalc.sh"), copia, recalc, perfil], capture_output=True, text=True)
        if r.returncode != 0:
            print(f"FALLO al recalcular {nombre}: {r.stdout}{r.stderr}")
            sys.exit(1)
        vals = leer(os.path.join(recalc, os.path.basename(copia)), SALIDAS)
        # (auditoría interna de la 4.9, Z-6) precio de Sí (k = 3, probabilidades 0,2 / 0,6 / 0,2) desde los tres valores recalculados
        V = [vals["MALO (Análisis!B78)"], vals["NORMAL (Análisis!C78)"], vals["BUENO (Análisis!D78)"]]
        vals["precio de Sí (precio_de_si.p_estrella, k = 3)"] = PS.p_estrella(V, [0.2, 0.6, 0.2], 3) if all(isinstance(x, (int, float)) for x in V) else None
        if isinstance(vals.get("control de rango de f (Diagnóstico V6!C50)"), str):
            vals["control de rango de f (Diagnóstico V6!C50)"] = vals["control de rango de f (Diagnóstico V6!C50)"][:60]
        filas.append({"variante": nombre, "tipo": tipo, "descripcion": desc, "celdas": celdas, "valores": vals,
                      "copia": os.path.relpath(copia, RAIZ), "copia_sha256": hashlib.sha256(open(copia, "rb").read()).hexdigest()})
        print(f"{nombre:22s} · " + " · ".join(f"{k.split(' (')[0]} {v:.4f}" if isinstance(v, float) else f"{k.split(' (')[0]} {v}" for k, v in vals.items()), flush=True)
    base = filas[0]["valores"]
    fiel = all(abs((base.get(k) or 0) - v) < 1e-9 for k, v in ESPERADO_BASE.items())
    for f in filas:
        f["delta"] = {k: (round(v - base[k], 6) if isinstance(v, (int, float)) and isinstance(base[k], (int, float)) else None) for k, v in f["valores"].items()}
    res = {"referencia": os.path.relpath(REF, RAIZ), "referencia_sha256": hashlib.sha256(open(REF, "rb").read()).hexdigest(),
           "aviso": "Cálculos exploratorios sobre copias identificadas: no heredan la aprobación de la referencia ni son resultados oficiales. "
                    "Las variantes «unitaria» miden la sensibilidad (+1 mm), las «hipótesis» no son cotas y el «contraejemplo» muestra un doble cómputo.",
           "recalculo_base_reproduce_referencia": fiel, "variantes": filas}
    json.dump(res, open(os.path.join(out, "efectos_n4.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"recálculo de la base fiel a la referencia: {fiel}")
    for f in filas[1:]:
        print(f"Δ {f['variante']:22s} · " + " · ".join(f"{k.split(' (')[0]} {d:+.4f}" for k, d in f["delta"].items() if d is not None))
    import shutil
    shutil.rmtree(tmp, ignore_errors=True)
    sys.exit(0 if fiel else 1)


if __name__ == "__main__":
    main()
