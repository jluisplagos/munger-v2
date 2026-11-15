#!/usr/bin/env python3
"""Extremos del rango de λ del piloto 4.11, calculados en el libro (revisión interna H11; encargo §9: «no cambia la zona» solo de variantes
calculadas). La configuración de demostración declara en su trazabilidad «λ 1,15; rango 1,10–1,25», pero no traía el campo PM1.lambda_rango
(se añadió después a configuracion_economica.py). Este script NO toca el expediente: copia el libro evaluado final y la configuración a un
temporal, añade lambda_rango = [1,10; 1,25] a la copia de la configuración y ejecuta variantes_configuracion_v64.py (el mismo código que el
paso 10, LibreOffice en secuencia). Escribe …/2026-11_Vidrala_ensayo_4_11/resultados/rango_lambda_4_11.json y .md.
Uso (desde munger_v2_r1/): python3 -I …/2026-11_Vidrala_ensayo_4_11/scripts/rango_parametro_4_11.py
Código 0 si se calcularon los dos extremos y la variante «activa» reproduce el precio.json del expediente.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
ENS = os.path.dirname(AQUI)
RAIZ = os.path.abspath(os.path.join(ENS, "..", "..", ".."))
PV = os.path.join(RAIZ, "personaje_v2")
PIL = os.path.join(ENS, "piloto", "Vidrala")
RANGO = [1.10, 1.25]


def main():
    tmp = os.path.join(tempfile.mkdtemp(prefix="rango_lambda_4_11_"), "Vidrala")
    os.makedirs(tmp)
    libro = os.path.join(PIL, "Vidrala_v63_evaluada.xlsx")
    shutil.copy(libro, os.path.join(tmp, "Vidrala_v63_evaluada.xlsx"))
    conf = json.load(open(os.path.join(PIL, "configuracion_economica.json"), encoding="utf-8"))
    conf["PM1"]["lambda_rango"] = RANGO
    json.dump(conf, open(os.path.join(tmp, "configuracion_economica.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    r = subprocess.run([sys.executable, os.path.join(PV, "scripts", "variantes_configuracion_v64.py"), tmp, os.path.join(tmp, "Vidrala_v63_evaluada.xlsx"),
                        "--config", os.path.join(PV, "config_v2_v64_experimental.json")], capture_output=True, text=True, timeout=3600)
    print(r.stdout[-3000:] + r.stderr[-1000:])
    var = json.load(open(os.path.join(tmp, "configuracion_v64_variantes.json"), encoding="utf-8"))
    pr = json.load(open(os.path.join(PIL, "precio.json"), encoding="utf-8"))
    filas = {v["clave"]: v for v in var["variantes"]}
    act = filas["activa"]
    ok = r.returncode == 0 and all(k in filas and filas[k].get("zona") for k in ("parametro_minimo", "parametro_maximo")) \
        and abs(act["ponderado"] - pr["ponderado"]) < 1e-9 and abs(act["precio_si"] - pr["precio_si"]) < 1e-9
    sel = [filas[k] for k in ("parametro_minimo", "activa", "parametro_maximo") if k in filas]
    out = {"expediente": os.path.relpath(PIL, RAIZ), "libro_sha256": hashlib.sha256(open(libro, "rb").read()).hexdigest(), "rango_lambda": RANGO,
           "precio": pr.get("precio"), "variantes": [{k: v.get(k) for k in ("clave", "descripcion", "V", "ponderado", "precio_si", "zona", "conciliacion",
                                                                              "delta_ponderado_frente_a_activa", "delta_precio_si_frente_a_activa")} for v in sel],
           "control_activa_reproduce_el_expediente": ok,
           "nota": "Variantes calculadas en el libro con el código del paso 10. λ es una hipótesis (no una medición); el rango es el que declara la trazabilidad de la configuración de demostración. Nada se adopta."}
    os.makedirs(os.path.join(ENS, "resultados"), exist_ok=True)
    json.dump(out, open(os.path.join(ENS, "resultados", "rango_lambda_4_11.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    f6 = lambda x: f"{x:.6f}" if isinstance(x, (int, float)) else "—"  # noqa: E731
    md = ["# Rango de λ del piloto 4.11, calculado en el libro", "",
          f"Libro evaluado final del piloto (SHA-256 `{out['libro_sha256'][:16]}…`), copia en un temporal; λ = {RANGO[0]} y {RANGO[1]} con la estructura, la familia y las "
          "convenciones de la configuración de demostración (SR1 · Λ · años planos · terminal proporcional · P0). El expediente no se modifica.", "",
          "| Variante | λ | MALO | NORMAL | BUENO | Ponderado | Δ | Precio de Sí | Δ | Zona (90,10 €) | Conciliación |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for v, lam in zip(out["variantes"], (RANGO[0], conf["PM1"]["lambda"], RANGO[1])):
        md.append(f"| {v['clave']} | {lam} | " + " | ".join(f6(x) for x in v["V"]) + f" | {f6(v['ponderado'])} | {f6(v['delta_ponderado_frente_a_activa'])} | {f6(v['precio_si'])} | "
                  f"{f6(v['delta_precio_si_frente_a_activa'])} | {v['zona']} | {', '.join(sorted(set(str(x)[:8] for x in (v.get('conciliacion') or {}).values())))} |")
    md += ["", f"Control: la variante «activa» {'reproduce' if ok else 'NO reproduce'} el precio.json del expediente (ponderado {f6(pr.get('ponderado'))}, precio de Sí {f6(pr.get('precio_si'))}).",
           "", "**Lectura.** " + out["nota"]]
    open(os.path.join(ENS, "resultados", "rango_lambda_4_11.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
    print("\n".join(md))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
