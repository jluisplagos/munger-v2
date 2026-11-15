#!/usr/bin/env python3
"""Comparación del resultado del ensayo 2025 con C1 de la 4.10 y variante de precisión de C46/C47 (entrega 4.10.1, encargo §4.2 y §6).

Uso (desde munger_v2_r1/, con el libro final del ensayo ya acreditado; usa LibreOffice: NO ejecutar en paralelo con otras pruebas ni
con el pipeline): python3 -I personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_10_1/scripts/comparar_con_C1.py

Variantes, cada una sobre una COPIA identificada (escribir_v63.py --copia-de-prueba) recalculada con recalc.sh (recálculo forzado):
  C1_control              libro evaluado de la referencia 4.6.1 + C41/C55 de C1 → debe reproducir C1 (70,4665 / 65,6645): control mecánico;
  ensayo_control          libro final del ensayo sin cambios → debe reproducir sus propios resultados (resultados.json del ensayo);
  ensayo_palancas_C1      libro final del ensayo con las PALANCAS de la referencia (celdas de valor de su fase B, celdas_B.json) → separa
                          entrada (C1 → esta variante) de juicio (esta variante → ensayo);
  ensayo_C46_C47_precisos libro final del ensayo con C46 = 335,413 y C47 = 169,668 (los que construye fase1_historia.py) → efecto de la
                          precisión, separado del caso principal (335,4 / 169,7).
Además lista las celdas de ENTRADA (inventario de la V6.3) cuyo valor difiere entre C1_control y ensayo_palancas_C1, para atribuir la
diferencia de entrada. Ninguna variante cambia r, probabilidades, k ni escenarios. Las copias no son resultados oficiales ni heredan
aprobaciones. Escribe ../resultados/comparacion_C1.json y .md (o en el directorio de --salida DIR)."""
import hashlib
import json
import os
import subprocess
import sys
import tempfile

import openpyxl

AQUI = os.path.dirname(os.path.abspath(__file__))
ENS = os.path.dirname(AQUI)
RAIZ = os.path.abspath(os.path.join(ENS, "..", "..", ".."))
PV = os.path.join(RAIZ, "personaje_v2")
SCR = os.path.join(PV, "scripts")
sys.path.insert(0, SCR)
import config_v2  # noqa: E402
import precio_de_si as PS  # noqa: E402

REF_DIR = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_6_1", "Vidrala")
REF = os.path.join(REF_DIR, "Vidrala_v63_evaluada.xlsx")
FIN = os.path.join(ENS, "Vidrala", "Vidrala_v63_evaluada.xlsx")
CONF = json.load(open(os.path.join(ENS, "configuracion", "configuracion_ensayo_2025.json"), encoding="utf-8"))
PROB, K = [0.2, 0.6, 0.2], 3
C1_ESP = {"ponderado": 70.4665, "precio_de_si": 65.6645}   # INFORME_FINANCIERO_4_10.md (4 decimales)
SALIDAS = {"MALO": ("Análisis", "B78"), "NORMAL": ("Análisis", "C78"), "BUENO": ("Análisis", "D78"), "ponderado": ("Análisis", "C83"),
           "r_op": ("Diagnóstico V6", "C15"), "puente": ("Diagnóstico V6", "C16"), "FCF_base": ("Análisis", "C52"), "f": ("Diagnóstico V6", "C12"),
           "estado_tecnico": ("Motor", "B255"), "E": ("Análisis", "C41"), "N": ("Análisis", "C55"), "C46": ("Análisis", "C46"), "C47": ("Análisis", "C47")}


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def leer(libro):
    wb = openpyxl.load_workbook(libro, data_only=True)
    out = {k: wb[h][c].value for k, (h, c) in SALIDAS.items()}
    V = [out["MALO"], out["NORMAL"], out["BUENO"]]
    out["precio_de_si"] = PS.p_estrella(V, PROB, K) if all(isinstance(x, (int, float)) for x in V) else None
    return out


def main():
    cfg = config_v2.cargar(os.path.join(PV, "config_v2.json"))
    sys.path.insert(0, cfg["plantilla"]["scripts_v63"])
    import inventario_entradas  # noqa
    entradas = inventario_entradas.conjunto_entradas()
    tmp = tempfile.mkdtemp(prefix="comparar_C1_")
    salida = sys.argv[sys.argv.index("--salida") + 1] if "--salida" in sys.argv else os.path.join(ENS, "resultados")   # (control de la entrega: a un temporal)
    copias = os.path.join(salida, "comparacion_C1_copias")
    os.makedirs(copias, exist_ok=True)
    perfil, recalc = os.path.join(tmp, "perfil_lo"), os.path.join(tmp, "recalc")
    e = CONF["entradas"]
    palancas_ref = {k: v for k, v in json.load(open(os.path.join(REF_DIR, "celdas_B.json"), encoding="utf-8")).items() if not k.startswith("Control maestro!")}
    variantes = [
        ("C1_control", REF, {"Análisis!C41": e["E_capitalizacion"]["valor"], "Análisis!C55": e["N_millones"]["valor"]}),
        ("ensayo_control", FIN, {}),
        ("ensayo_palancas_C1", FIN, palancas_ref),
        ("ensayo_C46_C47_precisos", FIN, {"Análisis!C46": 335.413, "Análisis!C47": 169.668}),
    ]
    filas, recs = [], {}
    for nombre, origen, celdas in variantes:
        cj = os.path.join(copias, f"{nombre}.celdas.json")
        json.dump(celdas, open(cj, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        copia = os.path.join(copias, f"COPIA_EXPLORATORIA_{nombre}.xlsx")
        r = subprocess.run([sys.executable, "-I", "-B", os.path.join(SCR, "escribir_v63.py"), origen, copia, "--celdas", cj, "--lista-blanca", "cualquiera", "--copia-de-prueba"],
                           capture_output=True, text=True)
        if r.returncode != 0:
            print(f"FALLO al escribir {nombre}: {r.stdout}{r.stderr}")
            return 1
        r = subprocess.run(["bash", os.path.join(SCR, "recalc.sh"), copia, recalc, perfil], capture_output=True, text=True)
        if r.returncode != 0:
            print(f"FALLO al recalcular {nombre}: {r.stdout}{r.stderr}")
            return 1
        rec = os.path.join(recalc, os.path.basename(copia))
        recs[nombre] = rec
        v = leer(rec)
        filas.append({"variante": nombre, "origen": os.path.relpath(origen, RAIZ), "origen_sha256": sha(origen), "celdas": celdas, "valores": v,
                      "copia": os.path.relpath(copia, RAIZ), "copia_sha256": sha(copia)})
        print(f"{nombre:26s} · MALO {v['MALO']:.4f} · NORMAL {v['NORMAL']:.4f} · BUENO {v['BUENO']:.4f} · pond {v['ponderado']:.4f} · Sí {v['precio_de_si']:.4f} "
              f"· r_op {v['r_op']:.6f} · puente {v['puente']:.3f} · FCF {v['FCF_base']:.3f} · {str(v['estado_tecnico'])[:40]}", flush=True)
    V = {f["variante"]: f["valores"] for f in filas}
    res = json.load(open(os.path.join(ENS, "Vidrala", "resultados.json"), encoding="utf-8")) if os.path.exists(os.path.join(ENS, "Vidrala", "resultados.json")) else {}
    # diferencias de ENTRADA entre C1 y el ensayo con las mismas palancas (celdas del inventario de entradas, sin textos de Control maestro)
    w1, w2 = openpyxl.load_workbook(recs["C1_control"], data_only=True), openpyxl.load_workbook(recs["ensayo_palancas_C1"], data_only=True)
    dif = []
    for hoja, refs in entradas.items():
        if hoja == "Control maestro" or hoja not in w1.sheetnames:
            continue
        for ref in sorted(refs):
            a, b = w1[hoja][ref].value, w2[hoja][ref].value
            if a != b and not (isinstance(a, (int, float)) and isinstance(b, (int, float)) and abs(a - b) < 1e-12):
                dif.append({"celda": f"{hoja}!{ref}", "C1": a if not isinstance(a, str) else a[:80], "ensayo": b if not isinstance(b, str) else b[:80]})
    claves = ("MALO", "NORMAL", "BUENO", "ponderado", "precio_de_si")
    d = lambda x, y: {k: round(V[x][k] - V[y][k], 6) for k in claves}  # noqa: E731
    out = {"generado_por": os.path.relpath(__file__, RAIZ), "referencia": os.path.relpath(REF, RAIZ), "referencia_sha256": sha(REF),
           "libro_final_del_ensayo": os.path.relpath(FIN, RAIZ), "libro_final_sha256": sha(FIN), "variantes": filas,
           "controles": {"C1_control_reproduce_C1": all(abs(V["C1_control"][k] - x) < 5e-5 for k, x in C1_ESP.items()),
                         "ensayo_control_reproduce_resultados_json": (all(abs(V["ensayo_control"][k] - res["valores"][c]) < 1e-6 for k, c in
                                                                          (("MALO", "B78"), ("NORMAL", "C78"), ("BUENO", "D78"), ("ponderado", "C83")))
                                                                      if isinstance(res.get("valores"), dict) and all(c in res["valores"] for c in ("B78", "C78", "D78", "C83"))
                                                                      else "resultados.json sin valores comparables")},
           "atribucion": {"entrada_y_convencion (C1 → ensayo con palancas de C1)": d("ensayo_palancas_C1", "C1_control"),
                          "juicio (palancas nuevas: ensayo con palancas de C1 → ensayo)": d("ensayo_control", "ensayo_palancas_C1"),
                          "total (C1 → ensayo)": d("ensayo_control", "C1_control"),
                          "precision_C46_C47 (ensayo → ensayo con 335,413 / 169,668)": d("ensayo_C46_C47_precisos", "ensayo_control")},
           "entradas_distintas_C1_vs_ensayo": dif}
    json.dump(out, open(os.path.join(salida, "comparacion_C1.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    md = ["# Comparación con C1 de la 4.10 y variante de precisión de C46/C47", "",
          "| Variante | MALO | NORMAL | BUENO | Ponderado | Precio de Sí | r_op | Puente | FCF base |", "|---|---|---|---|---|---|---|---|---|"]
    md += [f"| {f['variante']} | {f['valores']['MALO']:.4f} | {f['valores']['NORMAL']:.4f} | {f['valores']['BUENO']:.4f} | {f['valores']['ponderado']:.4f} | "
           f"{f['valores']['precio_de_si']:.4f} | {f['valores']['r_op']:.6f} | {f['valores']['puente']:.3f} | {f['valores']['FCF_base']:.3f} |" for f in filas]
    md += ["", f"**Controles:** {json.dumps(out['controles'], ensure_ascii=False)}", "", "**Atribución (diferencias en €/acción):**", ""]
    md += [f"- {k}: {json.dumps(v, ensure_ascii=False)}" for k, v in out["atribucion"].items()]
    num = [x for x in dif if not isinstance(x["C1"], str) and not isinstance(x["ensayo"], str)]
    txt = [x for x in dif if x not in num]
    md += ["", f"**Celdas de entrada distintas entre C1 y el ensayo con las mismas palancas:** {len(dif)} ({len(num)} numéricas o fechas; {len(txt)} de texto)", "",
           "Numéricas o fechas (datos y fechas). Ninguna entra en el valor del motor B con E dada (C41): C37 (precio) solo entra en la escalera, "
           "y C24, C33, C42, C53, C54 y C57 son datos informativos o de reglas que no mueven B78:D78 (la variante con las palancas de C1 reproduce C1):", ""]
    md += [f"- `{x['celda']}`: C1 {x['C1']!r} → ensayo {x['ensayo']!r}" for x in num[:80]]
    md += ["", "De texto: datos escritos como texto (C34 «No» → «Sí»; D4, fecha de análisis 2026-11-03 → 2026-11-11) y juicios, nombres de escenarios, "
           "predicciones y notas de la fase C; no entran en el cálculo del motor:", ""]
    md += [f"- `{x['celda']}`" + (f": C1 {x['C1']!r} → ensayo {x['ensayo']!r}" if x["celda"] in ("Análisis!C34", "Análisis!D4") else "") for x in txt[:80]]
    open(os.path.join(salida, "comparacion_C1.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
    print("\n".join(md))
    return 0 if out["controles"]["C1_control_reproduce_C1"] else 1


if __name__ == "__main__":
    sys.exit(main())
