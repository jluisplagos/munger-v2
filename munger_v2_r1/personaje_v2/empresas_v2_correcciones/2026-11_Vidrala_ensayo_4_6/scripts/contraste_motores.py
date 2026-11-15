#!/usr/bin/env python3
"""Contraste controlado del motor B (ensayo principal) con el motor A y T3 (entrega 4.5, §7 del encargo).

Uso: python3 -I contraste_motores.py [--salida DIR]   (por defecto: ../contraste_motores)

Parte del libro evaluado final del ensayo (Vidrala/Vidrala_v63_evaluada.xlsx), que NO se modifica, y construye copias separadas
en DIR/<variante>/. En cada copia escribe solo las celdas de la variante (escribir_v63.py --lista-blanca cualquiera
--copia-de-prueba), recalcula con LibreOffice (recalc.sh, perfil propio de DIR) y lee resultados y escalera (leer_resultados.py,
precio_de_si.py). Las palancas de la fase B (crecimiento, margen, S2C, ROIC, g, probabilidades) son comunes a todas las variantes.

Variantes (cada una cambia una cosa respecto a la anterior, para separar efectos):
  B0     ensayo principal sin cambios (motor B): comprueba que la copia reproduce el resultado del ensayo.
  A1     motor A (C62 = «Sí»; C76 = 0, referencia mecánica del exceso de caja) con los datos publicados: f = −0,0276 (T1).
         Efecto «motor» con los mismos datos: tasa (r en lugar de r_op), f del FCF en lugar de f = 0, y puente.
  A2     A1 + T3 (perímetro de continuadas, condicionado): Análisis C46 = 322,650; Historia J14 = 85,978; K14 = 36,487
         (circulantes derivados, no publicados; δ = 0 como hipótesis). Efecto «definición de f» (A2 − A1).
  A2a    A2 con C49 = 6,8 (sensibilidad de los arrendamientos; no es un intervalo demostrado).
  A2b    A2 con C49 = 0 (ídem).
Ningún resultado de este contraste es una valoración comparable con el precio ni un argumento para elegir motor.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys

sys.dont_write_bytecode = True
AQUI = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PV2 = os.path.abspath(os.path.join(AQUI, "..", ".."))
SCR = os.path.join(PV2, "scripts")
E = os.path.join(AQUI, "Vidrala")
LIBRO = os.path.join(E, "Vidrala_v63_evaluada.xlsx")

VARIANTES = [
    ("B0", "Motor B · ensayo principal (sin cambios)", {}),
    ("A1", "Motor A · datos publicados (T1: f del libro)", {"Análisis!C62": "Sí", "Análisis!C76": 0}),
    ("A2", "Motor A · T3 (continuadas; δ = 0; circulante derivado)", {"Análisis!C62": "Sí", "Análisis!C76": 0, "Análisis!C46": 322.65, "Historia!J14": 85.978, "Historia!K14": 36.487}),
    ("A2a", "Motor A · T3 con C49 = 6,8", {"Análisis!C62": "Sí", "Análisis!C76": 0, "Análisis!C46": 322.65, "Historia!J14": 85.978, "Historia!K14": 36.487, "Análisis!C49": 6.8}),
    ("A2b", "Motor A · T3 con C49 = 0", {"Análisis!C62": "Sí", "Análisis!C76": 0, "Análisis!C46": 322.65, "Historia!J14": 85.978, "Historia!K14": 36.487, "Análisis!C49": 0}),
]


def corre(cmd, cwd=None):
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)
    return r.returncode, (r.stdout + r.stderr).strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--salida", default=os.path.join(AQUI, "contraste_motores"))
    a = ap.parse_args()
    S = os.path.abspath(a.salida)
    os.makedirs(S, exist_ok=True)
    perfil = os.path.join(S, ".lo_perfil")
    filas = []
    for clave, nombre, celdas in VARIANTES:
        d = os.path.join(S, clave)
        if os.path.exists(d):
            shutil.rmtree(d)
        os.makedirs(d)
        libro = os.path.join(d, "Vidrala_v63_evaluada.xlsx")
        if celdas:
            cj = os.path.join(d, "celdas_variante.json")
            json.dump(celdas, open(cj, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            rc, out = corre([sys.executable, "-B", os.path.join(SCR, "escribir_v63.py"), LIBRO, libro, "--celdas", cj, "--lista-blanca", "cualquiera", "--copia-de-prueba"])
            if rc != 0:
                sys.exit(f"{clave}: escribir_v63.py código {rc}: {out[-400:]}")
        else:
            shutil.copy(LIBRO, libro)
        rc, out = corre(["bash", os.path.join(SCR, "recalc.sh"), libro, os.path.join(d, "recalc"), perfil])
        if rc != 0:
            sys.exit(f"{clave}: recalc.sh código {rc}: {out[-400:]}")
        rec = os.path.join(d, "recalc", os.path.basename(libro))
        rc, out = corre([sys.executable, "-B", os.path.join(SCR, "leer_resultados.py"), rec, os.path.join(d, "resultados.json"), "--exigir-recalculo-forzado"])
        if rc != 0:
            sys.exit(f"{clave}: leer_resultados.py código {rc}: {out[-400:]}")
        rc, out = corre([sys.executable, "-B", os.path.join(SCR, "precio_de_si.py"), os.path.join(d, "resultados.json"), os.path.join(d, "precio.json"), "--k", "3"])
        if rc not in (0, 5):
            sys.exit(f"{clave}: precio_de_si.py código {rc}: {out[-400:]}")
        r = json.load(open(os.path.join(d, "resultados.json"), encoding="utf-8"))
        p = json.load(open(os.path.join(d, "precio.json"), encoding="utf-8"))
        pe = r.get("por_escenario", {})
        filas.append({
            "variante": clave, "descripcion": nombre, "celdas_cambiadas": celdas,
            "motor": r.get("motor"), "f": r.get("f"), "r_operativa_C15": r.get("r_operativa_C15"),
            "pasivos_netos_B_C16": r.get("pasivos_netos_B_C16"), 
            "valor_por_accion": pe.get("valor_por_accion"), "valor_final": pe.get("valor_final"),
            "peso_terminal": pe.get("peso_terminal"), "ponderado": p.get("ponderado"), "precio_si": p.get("precio_si"),
            "precio_escenario_malo": p.get("precio_escenario_malo"), "zona": p.get("zona"),
            "estado_tecnico": (r.get("estados") or {}).get("estado_tecnico_B255"),
            "reglas_motor_no_ok": [f"{x.get('id')} {x.get('resultado')} (nivel {x.get('nivel')})" for x in (r.get("reglas_motor") or []) if x.get("aplica") and x.get("resultado") not in ("OK", "N/A")],
            "r_C56": (r.get("valores") or {}).get("C56"),
            "sha256_libro": __import__("hashlib").sha256(open(libro, "rb").read()).hexdigest(),
        })
    shutil.rmtree(perfil, ignore_errors=True)
    json.dump({"libro_de_partida": os.path.relpath(LIBRO, AQUI), "sha256_libro_de_partida": __import__("hashlib").sha256(open(LIBRO, "rb").read()).hexdigest(),
               "variantes": filas}, open(os.path.join(S, "contraste_resultados.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    def n(x, k=4):
        return "—" if x is None else (f"{x:.{k}f}" if isinstance(x, (int, float)) else str(x))
    lin = ["# Contraste de motores · resultados mecánicos (entrega 4.5)", "",
           "Resultados mecánicos de copias separadas del libro evaluado del ensayo. **No son valoraciones comparables con el precio ni argumentos para elegir motor.** Valores por acción en euros, referidos a la fecha de cada motor (B: 31-dic-2025, con derecho al dividendo a cuenta).", "",
           "| Variante | Motor | f | Tasa de descuento | Pasivos netos B (C16) | V MALO | V NORMAL | V BUENO | Ponderado | Precio de Sí (mecánico) |", "|---|---|---|---|---|---|---|---|---|---|"]
    for f in filas:
        v = f["valor_por_accion"] or [None, None, None]
        lin.append(f"| {f['variante']} · {f['descripcion']} | {f['motor']} | {n(f['f'], 6)} | {n(f['r_operativa_C15'] if f['motor'] == 'B' else f['r_C56'])} | {n(f['pasivos_netos_B_C16'], 3)} | {n(v[0], 2)} | {n(v[1], 2)} | {n(v[2], 2)} | {n(f['ponderado'], 2)} | {n(f['precio_si'], 2)} |")
    lin += ["", "Tasa de descuento: `r_op` (Motor!C15) en el motor B; r = C56 en el motor A. Reglas del motor distintas de OK en cada variante: " + "; ".join(f"{f['variante']}: " + (", ".join(f["reglas_motor_no_ok"]) or "ninguna") for f in filas) + "."]
    open(os.path.join(S, "contraste_resultados.md"), "w", encoding="utf-8").write("\n".join(lin) + "\n")
    print("\n".join(lin))


if __name__ == "__main__":
    main()
