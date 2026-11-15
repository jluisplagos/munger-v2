#!/usr/bin/env python3
"""Reproducción del resultado heredado de Viscofan con el código final (encargo 4.12 §8), antes de cualquier ensayo experimental.

Prepara dos expedientes NUEVOS con las entradas de partida del origen (`personaje_v2/empresas_v2/Viscofan`, que no se toca): la etapa 1,
`fase1_v63.json`, `fase1_metadatos.json`, `fase1_fuentes.json` y `fase1_partes/` (las cifras ya extraídas; el origen no trae los textos):
  - `viscofan/reproduccion_v63/Viscofan`: plantilla V6.3 (config_v2.json), como el origen;
  - `viscofan/reproduccion_v64_heredado/Viscofan`: plantilla V6.4 experimental en MODO HEREDADO (sin opciones experimentales).
Recorre el pipeline real y, cuando pide un agente, copia sin cambios la salida del agente del origen (extracto, fases A y B). Se
detiene cuando pide la fase C: la valoración ya está hecha. Compara con el origen, con las cifras completas de sus archivos: V,
probabilidades, ponderado, precio de Sí y zona (tolerancia 1e-9 €). No es un análisis nuevo ni hay auditoría.
Uso (desde munger_v2_r1/): python3 -I …/2026-11_Vidrala_ensayo_4_12/scripts/reproduccion_heredado_viscofan.py
Escribe viscofan/resultados/reproduccion_heredado.json y .md. Código 0 si las dos reproducciones coinciden con el origen.
"""
import json
import os
import shutil
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
EXP = os.path.dirname(AQUI)
PV = os.path.abspath(os.path.join(EXP, "..", ".."))
RAIZ = os.path.dirname(PV)
ORIG = os.path.join(PV, "empresas_v2", "Viscofan")
BASE = os.path.join(EXP, "viscofan")
PIPE = os.path.join(PV, "scripts", "pipeline.py")
ENTRADAS = ["etapa1", "fase1_v63.json", "fase1_metadatos.json", "fase1_fuentes.json", "fase1_partes", "fase1_listas.md"]
ARCHIVOS = {"extraccion_v63": ["extracto_v63.md"], "fase_a": ["fase_a.json", "fase_a.md"], "fase_b": ["fase_b.json", "fase_b.md"]}
HEREDADO = {"tipo": "configuracion_economica_motor_B", "version_formato": 1, "modo": "Heredado",
            "naturaleza": "Reproducción 4.12 del resultado heredado de Viscofan en la plantilla V6.4 experimental en MODO HEREDADO (V6.3 efectiva); no es una adopción ni un ensayo de parámetros.",
            "trazabilidad": {"modo": {"clase": "convención", "confianza": "alta", "fuente_o_condicion": "encargo 4.12 §8: reproducir primero el resultado heredado",
                                      "justificacion": "control antes de atribuir diferencias a la V6.4", "materialidad": "sin efecto: es la V6.3 efectiva"}}}


def preparar(dest, v64):
    if os.path.exists(dest):
        return
    os.makedirs(dest)
    for n in ENTRADAS:
        o = os.path.join(ORIG, n)
        if os.path.isdir(o):
            shutil.copytree(o, os.path.join(dest, n))
        elif os.path.exists(o):
            shutil.copy2(o, os.path.join(dest, n))
    if v64:
        json.dump(HEREDADO, open(os.path.join(dest, "configuracion_economica.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def correr(dest, cfg):
    salidas = []
    for _ in range(25):
        r = subprocess.run([sys.executable, PIPE, dest, "--config", cfg], capture_output=True, text=True)
        salidas.append(r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr[-200:])
        if r.returncode != 10:
            return r.returncode, salidas
        nombre = open(os.path.join(dest, "ESPERANDO.md"), encoding="utf-8").read().split("**")[1]
        if nombre == "fase_c_turno1":
            return 0, salidas + ["el pipeline pide la fase C: valoración hecha; la reproducción termina aquí"]
        if nombre not in ARCHIVOS:
            return 99, salidas + [f"agente no previsto: {nombre}"]
        for f in ARCHIVOS[nombre]:
            shutil.copy(os.path.join(ORIG, f), os.path.join(dest, f))
            os.utime(os.path.join(dest, f), None)
        salidas.append(f"agente simulado {nombre}: {', '.join(ARCHIVOS[nombre])} del origen, sin cambios")
    return 98, salidas + ["demasiadas vueltas"]


def main():
    p0 = json.load(open(os.path.join(ORIG, "precio.json"), encoding="utf-8"))
    r0 = json.load(open(os.path.join(ORIG, "resultados.json"), encoding="utf-8"))
    out = {"origen": os.path.relpath(ORIG, RAIZ), "referencia": {"V": p0.get("V"), "p": p0.get("p"), "ponderado": p0.get("ponderado"), "precio_si": p0.get("precio_si"),
                                                               "zona": p0.get("zona"), "precio": p0.get("precio"), "motor": r0.get("motor")}, "reproducciones": []}
    ok_total = True
    for nombre, cfg, v64 in (("reproduccion_v63", os.path.join(PV, "config_v2.json"), False), ("reproduccion_v64_heredado", os.path.join(PV, "config_v2_v64_experimental.json"), True)):
        dest = os.path.join(BASE, nombre, "Viscofan")
        preparar(dest, v64)
        rc, salidas = correr(dest, cfg)
        rep = {"expediente": os.path.relpath(dest, RAIZ), "config": os.path.basename(cfg), "pipeline_rc": rc, "salidas": salidas}
        if rc == 0:
            p1 = json.load(open(os.path.join(dest, "precio.json"), encoding="utf-8"))
            r1 = json.load(open(os.path.join(dest, "resultados.json"), encoding="utf-8"))
            d = {"V": max(abs(a - b) for a, b in zip(p1["V"], p0["V"])), "ponderado": abs(p1["ponderado"] - p0["ponderado"]), "precio_si": abs(p1["precio_si"] - p0["precio_si"]),
                 "probabilidades_iguales": p1.get("p") == p0.get("p"), "zona_igual": p1.get("zona") == p0.get("zona"), "motor_igual": r1.get("motor") == r0.get("motor")}
            rep.update({"V": p1["V"], "ponderado": p1["ponderado"], "precio_si": p1["precio_si"], "zona": p1["zona"], "diferencias": d,
                        "coincide": d["V"] <= 1e-9 and d["ponderado"] <= 1e-9 and d["precio_si"] <= 1e-9 and d["probabilidades_iguales"] and d["zona_igual"] and d["motor_igual"]})
        else:
            rep["coincide"] = False
        ok_total = ok_total and rep["coincide"]
        out["reproducciones"].append(rep)
    out["resultado"] = "COINCIDE" if ok_total else "NO COINCIDE (ver diferencias)"
    os.makedirs(os.path.join(BASE, "resultados"), exist_ok=True)
    json.dump(out, open(os.path.join(BASE, "resultados", "reproduccion_heredado.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    md = ["# Viscofan · reproducción del resultado heredado con el código final", "", f"**Resultado: {out['resultado']}.**", "",
          f"Referencia del origen (cifras completas): ponderado {p0.get('ponderado')} · precio de Sí {p0.get('precio_si')} · V {p0.get('V')} · probabilidades {p0.get('p')} · zona {p0.get('zona')} · precio {p0.get('precio')} · motor {r0.get('motor')}.", ""]
    for rep in out["reproducciones"]:
        md += [f"## {rep['expediente']} ({rep['config']})", "", f"- código del recorrido: {rep['pipeline_rc']} · coincide: {'sí' if rep['coincide'] else 'NO'}",
               f"- ponderado {rep.get('ponderado')} · precio de Sí {rep.get('precio_si')} · V {rep.get('V')} · zona {rep.get('zona')}",
               f"- |Δ| {rep.get('diferencias')}", ""] + [f"  - {s}" for s in rep["salidas"]] + [""]
    open(os.path.join(BASE, "resultados", "reproduccion_heredado.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
    print(f"{out['resultado']}: " + " · ".join(f"{r['config']}: Sí {r.get('precio_si')} pond {r.get('ponderado')}" for r in out["reproducciones"]))
    return 0 if ok_total else 1


if __name__ == "__main__":
    sys.exit(main())
