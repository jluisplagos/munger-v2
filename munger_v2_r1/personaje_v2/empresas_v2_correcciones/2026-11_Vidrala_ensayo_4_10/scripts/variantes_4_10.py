#!/usr/bin/env python3
"""Variantes financieras de Vidrala (entrega 4.10, encargo §4.3, §5 y §6): efectos aislados y combinados sobre copias identificadas.

Uso: python3 -I variantes_4_10.py [--salida DIR] [--copia-combinada DIR]   (usa LibreOffice: no ejecutar en paralelo con otras pruebas)

Parte del libro evaluado de referencia (…/2026-11_Vidrala_ensayo_4_6_1/Vidrala/Vidrala_v63_evaluada.xlsx), que no se modifica. Para
cada variante escribe una COPIA identificada (escribir_v63.py --copia-de-prueba), la recalcula con recalc.sh (recálculo forzado) y
lee la valoración. Ninguna variante cambia r (0,09), probabilidades (0,2/0,6/0,2), k (3), escenarios ni palancas, salvo la variante
N10 de historia adversa, que se declara como tal. Las copias no heredan la aprobación de la referencia ni son resultados oficiales.

Cada identidad se comprueba con un cálculo INDEPENDIENTE del libro (aritmética de este script):
  N6: r_op del libro (Diagnóstico V6!C15) = (r·E + i·(1−τ)·D)/(E+D) con E, D, i y τ leídos de sus celdas;
  N7: con E fija, V(N') = V(N)·N/N' (motor B sin probabilidad de quiebra);
  N8: V_sin_derecho = V_con_derecho − 43,338/N en los tres escenarios, el ponderado y el precio de Sí;
  N5: ΔV = −ΔL25/N;  P3: (C48 = I, C49 = P) y (C48 = 0, C49 = P+I) dan el mismo FCF y la misma valoración.
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

import openpyxl

AQUI = os.path.dirname(os.path.abspath(__file__))
EXP = os.path.dirname(AQUI)
RAIZ = os.path.abspath(os.path.join(EXP, "..", "..", ".."))
SCR = os.path.join(RAIZ, "personaje_v2", "scripts")
sys.path.insert(0, SCR)
import precio_de_si as PS  # noqa: E402

REF = os.path.join(RAIZ, "personaje_v2", "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_6_1", "Vidrala", "Vidrala_v63_evaluada.xlsx")
PROB, K = [0.2, 0.6, 0.2], 3

# ---------- datos con fuente (miles de euros en la fuente; mm aquí). ES 2025 = 2308_es-informacion_financiera_consolidada_2025.pdf ----------
PRECIO_CIERRE_2025 = 90.10          # ES 2025, Informe de gestión «Evolución bursátil», pág. PDF 97 (impresa 10): «cerró 2025 en 90,10 euros … 3.172 millones»
EMITIDAS = 35.206258                # ES 2025, nota 14(k), pág. PDF 67 (impresa 59): 35.206.258 acciones a 31-dic-2025
AUTOCARTERA = 0.023400              # ídem: 23.400 acciones propias a 31-dic-2025 (coste 2.097 miles)
CIRCULACION = round(EMITIDAS - AUTOCARTERA, 6)   # 35,182858 (derivado); lo confirma el dividendo a cuenta: 43.338.244,48 € ÷ 1,2318 €
DIVIDENDO_A_CUENTA = 43.338         # ES 2025, nota 14(n), pág. PDF 70 (impresa 62) y nota 17 «Accionistas por dividendos» 43.338 (pasivo al cierre)
CAJA, PUENTE = 108.352, 160.784
PENSIONES = 6.223                   # ES 2025, nota 19, pág. PDF 77 (impresa 69): provisión «Personal» a 31-dic-2025
TAU_UK = 0.25                       # hipótesis: tipo general del impuesto de sociedades británico (el plan de prestación definida es de Encirc)
TAU_2025 = 0.2433                   # Historia!L10: tipo efectivo 2025 (alternativa de τ solo en r_op)
I_ARR = (2.131 + 2.179 + 2.452) / 3     # devengo de intereses de arrendamientos 2023–2025 (nota 8; 4.2): 2,254 · HIPÓTESIS de pago, no acreditado
P_MAS_I = (5.861 + 6.117 + 8.314) / 3   # pagos totales del pasivo por arrendamiento 2023–2025 (nota 8, movimiento): 6,764
P_ARR = P_MAS_I - I_ARR                 # principal, si el interés pagado = devengado: 4,510 (≈ C49 = 4,5 de la referencia)

SALIDAS = {"MALO": ("Análisis", "B78"), "NORMAL": ("Análisis", "C78"), "BUENO": ("Análisis", "D78"), "ponderado": ("Análisis", "C83"),
           "r_op": ("Diagnóstico V6", "C15"), "puente": ("Diagnóstico V6", "C16"), "FCF_base": ("Análisis", "C52"), "f": ("Diagnóstico V6", "C12"),
           "control_f": ("Diagnóstico V6", "C50"), "estado_tecnico": ("Motor", "B255"), "E_capitalizacion": ("Análisis", "C41"), "N": ("Análisis", "C55"),
           "C48": ("Análisis", "C48"), "C49": ("Análisis", "C49"), "L25": ("Historia", "L25"), "caja_C66": ("Historia", "C66"), "L26": ("Historia", "L26"),
           "i_C63": ("Historia", "C63"), "D_C64": ("Historia", "C64"), "tau_C11": ("Diagnóstico V6", "C11"), "r_C56": ("Análisis", "C56"),
           "g_MALO": ("Análisis", "B68"), "g_NORMAL": ("Análisis", "C68"), "g_BUENO": ("Análisis", "D68"), "veredicto": ("Análisis", "A6")}


def r_op(E, D, i, tau, r=0.09):
    return (r * E + i * (1 - tau) * D) / (E + D)


def variantes():
    E25 = round(PRECIO_CIERRE_2025 * EMITIDAS, 6)
    E25c = round(PRECIO_CIERRE_2025 * CIRCULACION, 6)
    i, D = 0.0633928911577584, 262.913
    v = [
        ("base", "control", "sin cambios: debe reproducir la referencia mecánica heredada", {}),
        ("N6_E_2025", "aislada", f"E = precio de cierre de 2025 × acciones emitidas = {PRECIO_CIERRE_2025} × {EMITIDAS} = {E25} (el resto heredado: N 35,206, D, i, τ)",
         {"Análisis!C41": E25}),
        ("N6_E_2025_tau_2025", "alternativa (estructural)", f"como N6_E_2025 y τ del escudo de la deuda = tipo efectivo 2025 ({TAU_2025}) solo en r_op. La plantilla usa el mismo τ "
         "(C11) en el motor y en r_op: no es representable con celdas de valor; se sustituye la FÓRMULA de Diagnóstico V6!C15 por su valor en esta copia (copia estructural, "
         "no íntegra; el τ del motor no cambia)", {"Análisis!C41": E25}, {"Diagnóstico V6!C15": round(r_op(E25, D, i, TAU_2025), 12)}),
        ("N7_N_puro", "aislada", f"N = acciones en circulación a 31-dic-2025 = {CIRCULACION} con E fija (heredada 3.094,6): efecto puro del denominador",
         {"Análisis!C55": CIRCULACION}),
        ("N7_conjunto", "aislada", f"N = {CIRCULACION} y E = {PRECIO_CIERRE_2025} × {CIRCULACION} = {E25c}: efecto conjunto coherente por E y r_op",
         {"Análisis!C55": CIRCULACION, "Análisis!C41": E25c}),
        ("N5_neto_impuestos", "hipótesis", f"HIPÓTESIS: pensiones netas de un impuesto del {TAU_UK:.0%}: L25 = {PENSIONES} × (1 − {TAU_UK}) = {round(PENSIONES * (1 - TAU_UK), 6)}",
         {"Historia!L25": round(PENSIONES * (1 - TAU_UK), 6)}),
        ("N8_sin_derecho", "aislada", f"sin derecho al dividendo a cuenta: la obligación «Accionistas por dividendos» ({DIVIDENDO_A_CUENTA}) se resta UNA vez en el puente; "
                                      "vehículo: Historia!L26 (celda de valor que en la VALORACIÓN solo entra por el puente; mueve además los múltiplos informativos EV/ventas y "
                                      "EV/EBITDA de Diagnóstico V6, que no intervienen en los valores; NO son minoritarios, que siguen en 0); caja 108,352 sin tocar; "
                                      "fijos: valoración operativa, E, r_op, escenarios y N", {"Historia!L26": DIVIDENDO_A_CUENTA}),
        ("P3_B1", "condicionada", f"intereses de arrendamientos pagados en FINANCIACIÓN (no acreditado): C48 = I = {I_ARR:.6f} y C49 = P = 4,5 (referencia)",
         {"Análisis!C48": round(I_ARR, 6)}),
        ("P3_B2", "condicionada", f"la misma localización con la otra representación: C48 = 0 y C49 = 4,5 + I = {4.5 + I_ARR:.6f} (equivalente a P3_B1; "
                                  f"P + I con P = {P_ARR:.3f} sería {P_MAS_I:.3f}: la diferencia de 0,010 es el redondeo de C49 = 4,5)", {"Análisis!C49": round(4.5 + I_ARR, 6)}),
        ("N10_MALO_historia_adversa", "hipótesis", "HISTORIA ADVERSA del MALO (no un cambio de pesos): crecimiento −2 % (Palancas!B14) y margen 12 %, el mínimo de la serie "
                                                  "2016–2025 (Palancas!B15); NORMAL, BUENO, probabilidades y r sin cambios",
         {"Palancas!B14": -0.02, "Palancas!B15": 0.12}),
        ("C1_31dic2025_con_derecho", "combinada", f"N6 + N7: E = {E25c} (cierre de 2025 × acciones en circulación) y N = {CIRCULACION}; con derecho al dividendo a cuenta; "
                                                  "P3 en la representación de la referencia (C48 = 0, C49 = 4,5); L25 = 6,223", {"Análisis!C55": CIRCULACION, "Análisis!C41": E25c}),
        ("C2_31dic2025_sin_derecho", "combinada", f"C1 sin derecho al dividendo a cuenta (obligación de {DIVIDENDO_A_CUENTA} en el puente, vehículo Historia!L26); E se mantiene con el precio CON derecho "
                                                  "(otro contraste, no la identidad pura)", {"Análisis!C55": CIRCULACION, "Análisis!C41": E25c, "Historia!L26": DIVIDENDO_A_CUENTA}),
    ]
    return v


def leer(libro):
    wb = openpyxl.load_workbook(libro, data_only=True)
    out = {k: wb[h][c].value for k, (h, c) in SALIDAS.items()}
    if isinstance(out.get("veredicto"), str):
        out["veredicto"] = out["veredicto"][:90]
    if isinstance(out.get("control_f"), str):
        out["control_f"] = out["control_f"][:70]
    return out


def precio_si(vals, prob=PROB):
    V = [vals["MALO"], vals["NORMAL"], vals["BUENO"]]
    return PS.p_estrella(V, prob, K) if all(isinstance(x, (int, float)) for x in V) else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--salida", default=os.path.join(EXP, "variantes"))
    ap.add_argument("--copia-combinada", default=os.path.join(EXP, "copia_combinada"))
    a = ap.parse_args()
    out = os.path.abspath(a.salida)
    copias = os.path.join(out, "copias")
    os.makedirs(copias, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix="variantes410_")
    perfil, recalc = os.path.join(tmp, "perfil_lo"), os.path.join(tmp, "recalc")
    filas = []
    for var in variantes():
        nombre, tipo, desc, celdas = var[:4]
        estructural = var[4] if len(var) > 4 else {}
        cj = os.path.join(copias, f"{nombre}.celdas.json")
        json.dump(celdas, open(cj, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        copia = os.path.join(copias, f"COPIA_EXPLORATORIA_{nombre}.xlsx")
        r = subprocess.run([sys.executable, "-I", "-B", os.path.join(SCR, "escribir_v63.py"), REF, copia, "--celdas", cj, "--lista-blanca", "cualquiera", "--copia-de-prueba"],
                           capture_output=True, text=True)
        if r.returncode != 0:
            print(f"FALLO al escribir {nombre}: {r.stdout}{r.stderr}")
            return 1
        if estructural:
            wbx = openpyxl.load_workbook(copia)
            for ref_c, val in estructural.items():
                h, c = ref_c.split("!")
                wbx[h][c] = val
            wbx.save(copia)
            json.dump({"celdas": celdas, "sustituciones_estructurales_de_formulas": estructural}, open(cj, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        r = subprocess.run(["bash", os.path.join(SCR, "recalc.sh"), copia, recalc, perfil], capture_output=True, text=True)
        if r.returncode != 0:
            print(f"FALLO al recalcular {nombre}: {r.stdout}{r.stderr}")
            return 1
        rec = os.path.join(recalc, os.path.basename(copia))
        vals = leer(rec)
        vals["precio_de_si"] = precio_si(vals)
        fila = {"variante": nombre, "tipo": tipo, "descripcion": desc, "celdas": celdas, "sustituciones_estructurales": estructural, "valores": vals,
                "aviso": ("copia estructural NO íntegra (una fórmula sustituida por su valor): el estado técnico lo calcula la hoja y no refleja la sustitución"
                          if estructural else None),
                "copia": os.path.relpath(copia, RAIZ), "copia_sha256": hashlib.sha256(open(copia, "rb").read()).hexdigest(),
                "g_menor_que_r_op": all(isinstance(vals.get(g), (int, float)) and isinstance(vals.get("r_op"), (int, float)) and vals[g] < vals["r_op"] for g in ("g_MALO", "g_NORMAL", "g_BUENO"))}
        if nombre.startswith("C1"):
            # copia exploratoria combinada ENTREGABLE: con sus cachés (add_cached_values, como el paso 12) y su comprobante externo
            dest = os.path.abspath(a.copia_combinada)
            os.makedirs(dest, exist_ok=True)
            final = os.path.join(dest, "Vidrala_v63_evaluada.xlsx")
            kit = subprocess.run([sys.executable, os.path.join(SCR, "config_v2.py"), "kit_v1.scripts", os.path.join(RAIZ, "personaje_v2", "config_v2.json")], capture_output=True, text=True).stdout.strip()
            ref_v = subprocess.run([sys.executable, os.path.join(SCR, "config_v2.py"), "plantilla.referencia", os.path.join(RAIZ, "personaje_v2", "config_v2.json")], capture_output=True, text=True).stdout.strip()
            ver = subprocess.run([sys.executable, os.path.join(SCR, "config_v2.py"), "plantilla.verificador", os.path.join(RAIZ, "personaje_v2", "config_v2.json")], capture_output=True, text=True).stdout.strip()
            rr = subprocess.run([sys.executable, "-I", "-B", os.path.join(kit, "add_cached_values.py"), copia, rec, final], capture_output=True, text=True)
            ri = subprocess.run([sys.executable, "-I", "-B", ver, copia, ref_v], capture_output=True, text=True)
            # verificación ANTES de las cachés, tal cual (nombra la copia sin cachés); el archivo final lo acredita acreditar_libro.py (P-N2)
            open(os.path.join(dest, "verificacion_integridad.txt"), "w", encoding="utf-8").write(ri.stdout + ri.stderr)
            # (revisión interna R-2) libro de ENTRADA coherente con C1: el de datos de la referencia con las mismas celdas de C1 (C41 y C55)
            rd = subprocess.run([sys.executable, "-I", "-B", os.path.join(SCR, "escribir_v63.py"), os.path.join(os.path.dirname(REF), "Vidrala_v63_datos.xlsx"),
                                 os.path.join(dest, "Vidrala_v63_datos.xlsx"), "--celdas", cj, "--lista-blanca", "cualquiera"], capture_output=True, text=True)
            if rd.returncode != 0:
                print(f"FALLO al escribir el libro de entrada de C1: {rd.stdout}{rd.stderr}")
                return 1
            ra = subprocess.run([sys.executable, "-I", "-B", os.path.join(SCR, "acreditar_libro.py"), dest, final, os.path.join(dest, "Vidrala_v63_datos.xlsx"), ref_v, ver,
                                 "incorporadas" if rr.returncode == 0 else "fallidas"], capture_output=True, text=True)
            fila["copia_combinada"] = {"libro": os.path.relpath(final, RAIZ), "sha256": hashlib.sha256(open(final, "rb").read()).hexdigest(),
                                       "add_cached_values": rr.returncode, "acreditar_libro": ra.returncode, "salida": ra.stdout.strip()[-300:]}
        filas.append(fila)
        print(f"{nombre:28s} · MALO {vals['MALO']:.4f} · NORMAL {vals['NORMAL']:.4f} · BUENO {vals['BUENO']:.4f} · pond {vals['ponderado']:.4f} · Sí {vals['precio_de_si']:.4f} "
              f"· r_op {vals['r_op']:.6f} · puente {vals['puente']:.3f} · FCF {vals['FCF_base']:.3f} · f {vals['f']:.6f}", flush=True)
    base = filas[0]["valores"]
    V = {f["variante"]: f["valores"] for f in filas}
    claves = ("MALO", "NORMAL", "BUENO", "ponderado", "precio_de_si")
    for f in filas:
        f["delta_frente_a_base"] = {k: round(f["valores"][k] - base[k], 6) for k in claves + ("r_op", "puente", "FCF_base", "f")
                                    if isinstance(f["valores"].get(k), (int, float)) and isinstance(base.get(k), (int, float))}
    ESP = {"MALO": 53.670420, "NORMAL": 70.772197, "BUENO": 86.488762, "ponderado": 70.495154, "precio_de_si": 65.688087, "puente": 160.784}
    ident = {}
    ident["base_reproduce_la_referencia"] = all(abs(base[k] - v) < 5e-7 for k, v in ESP.items())
    for n in ("base", "N6_E_2025", "N7_conjunto", "C1_31dic2025_con_derecho"):
        x = V[n]
        calc = r_op(x["E_capitalizacion"], x["D_C64"], x["i_C63"], x["tau_C11"], x["r_C56"])
        ident[f"N6_r_op_libro_igual_a_formula_{n}"] = abs(calc - x["r_op"]) < 1e-12
    n0, n1 = base["N"], V["N7_N_puro"]["N"]
    ident["N7_puro_V_por_N"] = all(abs(V["N7_N_puro"][k] - base[k] * n0 / n1) < 1e-9 for k in claves)
    ident["N8_sin_derecho_igual_V_menos_dividendo_por_N"] = all(abs(V["N8_sin_derecho"][k] - (base[k] - DIVIDENDO_A_CUENTA / base["N"])) < 1e-9 for k in claves)
    ident["N8_puente_sube_el_dividendo"] = abs(V["N8_sin_derecho"]["puente"] - (base["puente"] + DIVIDENDO_A_CUENTA)) < 1e-9
    ident["N8_resto_fijo"] = all(V["N8_sin_derecho"][k] == base[k] for k in ("r_op", "FCF_base", "f", "E_capitalizacion", "N", "caja_C66"))
    ident["N5_delta_igual_menos_dL25_por_N"] = all(abs(V["N5_neto_impuestos"][k] - (base[k] + (PENSIONES - PENSIONES * (1 - TAU_UK)) / base["N"])) < 1e-9 for k in claves)
    ident["P3_B1_igual_B2"] = all(abs(V["P3_B1"][k] - V["P3_B2"][k]) < 1e-9 for k in claves + ("FCF_base", "f"))
    ident["P3_FCF_baja_I"] = abs(V["P3_B1"]["FCF_base"] - (base["FCF_base"] - I_ARR)) < 1e-6
    ident["C2_igual_C1_menos_dividendo_por_N"] = all(abs(V["C2_31dic2025_sin_derecho"][k] - (V["C1_31dic2025_con_derecho"][k] - DIVIDENDO_A_CUENTA / CIRCULACION)) < 1e-9 for k in claves)
    ident["g_menor_que_r_op_en_todas"] = all(f["g_menor_que_r_op"] for f in filas)
    # N10: sensibilidad de PESOS (sin recálculo: los mismos tres valores) frente a la historia adversa (recalculada)
    pesos = {"referencia 0,2/0,6/0,2": [0.2, 0.6, 0.2], "cola adversa 0,3/0,5/0,2": [0.3, 0.5, 0.2], "cola adversa 0,4/0,5/0,1": [0.4, 0.5, 0.1],
             "colas simétricas 0,25/0,5/0,25": [0.25, 0.5, 0.25], "equiprobable 1/3": [1 / 3, 1 / 3, 1 / 3], "cola favorable 0,1/0,6/0,3": [0.1, 0.6, 0.3]}
    sens = {}
    for nv in ("base", "C1_31dic2025_con_derecho", "N10_MALO_historia_adversa"):
        x = V[nv]
        sens[nv] = {etq: {"ponderado": round(sum(p * x[e] for p, e in zip(w, ("MALO", "NORMAL", "BUENO"))), 6), "precio_de_si": round(precio_si(x, w), 6)} for etq, w in pesos.items()}
    res = {"generado_por": "scripts/variantes_4_10.py", "referencia": os.path.relpath(REF, RAIZ), "referencia_sha256": hashlib.sha256(open(REF, "rb").read()).hexdigest(),
           "aviso": "Cálculos exploratorios sobre copias identificadas: no heredan la aprobación de la referencia ni son resultados oficiales ni comparables con el precio de "
                    "noviembre de 2026 (fuera del encargo). «hipótesis» y «condicionada» no son cotas ni convenciones adoptadas.",
           "datos": {"precio_cierre_2025": PRECIO_CIERRE_2025, "acciones_emitidas_mm": EMITIDAS, "autocartera_mm": AUTOCARTERA, "acciones_en_circulacion_mm": CIRCULACION,
                     "dividendo_a_cuenta_mm": DIVIDENDO_A_CUENTA, "pensiones_L25_mm": PENSIONES, "I_arrendamientos_media_mm": round(I_ARR, 6),
                     "P_mas_I_media_mm": round(P_MAS_I, 6), "P_media_si_I_pagado_igual_devengado_mm": round(P_ARR, 6)},
           "probabilidades": PROB, "k": K, "identidades": ident, "sensibilidad_de_pesos_N10": sens, "variantes": filas}
    json.dump(res, open(os.path.join(out, "variantes_4_10.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    import csv
    with open(os.path.join(out, "variantes_4_10.csv"), "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        cols = ["MALO", "NORMAL", "BUENO", "ponderado", "precio_de_si", "r_op", "puente", "FCF_base", "f", "E_capitalizacion", "N", "C48", "C49", "L25", "caja_C66", "estado_tecnico"]
        w.writerow(["variante", "tipo"] + cols + ["delta_ponderado", "delta_precio_de_si", "celdas"])
        for f in filas:
            w.writerow([f["variante"], f["tipo"]] + [f["valores"].get(c) for c in cols] + [f["delta_frente_a_base"].get("ponderado"), f["delta_frente_a_base"].get("precio_de_si"),
                                                                                          json.dumps(f["celdas"], ensure_ascii=False)])
    for k, ok in ident.items():
        print(f"{'CUMPLE' if ok else 'NO CUMPLE'} · {k}")
    shutil.rmtree(tmp, ignore_errors=True)
    return 0 if all(ident.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
