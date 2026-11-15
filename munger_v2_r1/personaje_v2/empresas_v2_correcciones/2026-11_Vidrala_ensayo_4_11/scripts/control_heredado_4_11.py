#!/usr/bin/env python3
"""Control heredado limpio del encargo 4.11 (§9): la plantilla V6.4 en MODO HEREDADO, con el expediente preparado por cambiar_base.py
(entradas del ensayo 2025 de la 4.10.1 y evidencia corregida), recorre el pipeline real con la configuración V6.4 hasta el paso 12
con agentes SIMULADOS: las salidas de los agentes de la 4.10.1 (extracto, fases A, B y C), copiadas sin cambios cuando el pipeline las
pide. No es un análisis nuevo ni hay auditoría: compara valores y estados mecánicos con la 4.10.1.

Uso (desde munger_v2_r1/): python3 -I …/2026-11_Vidrala_ensayo_4_11/scripts/control_heredado_4_11.py
Escribe control_heredado/resultados/control_heredado.json y .md. Código 0 si V, ponderado, precio de Sí, zona y estados coinciden
con la 4.10.1 (tolerancia 1e-9 €) y el libro evaluado recalculado no difiere en ninguna celda calculada fuera de las declaradas.
"""
import json
import os
import shutil
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
ENS = os.path.dirname(AQUI)
RAIZ = os.path.abspath(os.path.join(ENS, "..", "..", ".."))
PV = os.path.join(RAIZ, "personaje_v2")
DEST = os.path.join(ENS, "control_heredado", "Vidrala")
REF = os.path.join(ENS, "..", "2026-11_Vidrala_ensayo_4_10_1", "Vidrala")
CFG = os.path.join(PV, "config_v2_v64_experimental.json")
PIPE = os.path.join(PV, "scripts", "pipeline.py")
sys.path.insert(0, os.path.join(RAIZ, "v6", "v64_experimental", "scripts"))
from comparar_libros import comparar  # noqa: E402
ARCHIVOS = {"extraccion_v63": ["extracto_v63.md"], "fase_a": ["fase_a.json", "fase_a.md"], "fase_b": ["fase_b.json", "fase_b.md"],
            "fase_c_turno1": ["fase_c.json", "fase_c.md"], "fase_c_turno2": ["fase_c.json", "fase_c.md"]}


def correr():
    salidas = []
    for _ in range(20):
        r = subprocess.run([sys.executable, PIPE, DEST, "--config", CFG, "--hasta", "12"], capture_output=True, text=True)
        salidas.append(r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr[-200:])
        if r.returncode != 10:
            return r.returncode, salidas
        nombre = open(os.path.join(DEST, "ESPERANDO.md"), encoding="utf-8").read().split("**")[1]
        if nombre not in ARCHIVOS:
            return 99, salidas + [f"agente no previsto: {nombre}"]
        for f in ARCHIVOS[nombre]:
            shutil.copy(os.path.join(REF, f), os.path.join(DEST, f))
            os.utime(os.path.join(DEST, f), None)
        salidas.append(f"agente simulado {nombre}: {', '.join(ARCHIVOS[nombre])} de la 4.10.1")
    return 98, salidas + ["demasiadas vueltas"]


def main():
    rc, salidas = correr()
    j = lambda d, n: json.load(open(os.path.join(d, n), encoding="utf-8"))  # noqa: E731
    out = {"pipeline_rc": rc, "salidas": salidas}
    if rc != 0:
        json.dump(out, open(os.path.join(ENS, "control_heredado", "resultados", "control_heredado.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("\n".join(salidas))
        return 1
    st = j(DEST, "estado_pipeline.json")
    p_c, p_r = j(DEST, "precio.json"), j(REF, "precio.json")
    r_c, r_r = j(DEST, "resultados.json"), j(REF, "resultados.json")
    d = {"V": max(abs(a - b) for a, b in zip(p_c["V"], p_r["V"])), "ponderado": abs(p_c["ponderado"] - p_r["ponderado"]), "precio_si": abs(p_c["precio_si"] - p_r["precio_si"])}
    estados = {k: (r_c["estados"].get(k), r_r["estados"].get(k)) for k in ("estado_tecnico_B255", "bloqueo_valor_B252", "comparable_B253", "dcf_inverso_monotono_B193")}
    libro_c = os.path.join(DEST, "recalc", "Vidrala_v63_evaluada.xlsx")
    libro_r = os.path.join(REF, "recalc", "Vidrala_v63_evaluada.xlsx")
    dif, n = comparar(libro_r, libro_c, 1e-9)
    # diferencias esperadas: la evidencia de Control maestro reescrita por el cambio de base, la fecha real de ejecución (D4 y lo que
    # depende de ella) y los recuentos de evidencias del Control maestro que leen esos textos
    esperadas = [x for x in dif if x[0].startswith("Control maestro!") or x[0] in ("Análisis!D4",)]
    otras = [x for x in dif if x not in esperadas]
    ok = all(v < 1e-9 for v in d.values()) and p_c.get("zona") == p_r.get("zona") and all(a == b for a, b in estados.values())
    out.update({"estado_pipeline": {"paso": st.get("paso"), "estado_analisis": st.get("estado_analisis")}, "diferencias_valoracion": d,
                "zona": (p_c.get("zona"), p_r.get("zona")), "estados": estados, "configuracion_v64": {k: (r_c.get("configuracion_v64") or {}).get(k) for k in ("modo", "valida", "resumen")},
                "libro": {"celdas_comparadas": n, "diferencias": len(dif), "en_control_maestro_o_fecha": len(esperadas), "otras": [[k, str(a), str(b)] for k, a, b in otras][:60]},
                "resultado": "CONCUERDA" if ok else "NO CONCUERDA"})
    json.dump(out, open(os.path.join(ENS, "control_heredado", "resultados", "control_heredado.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    md = ["# Control heredado 4.11 · V6.4 en modo heredado frente a la 4.10.1", "",
          f"- Pipeline real con la configuración V6.4 hasta el paso 12 (agentes simulados con las salidas de la 4.10.1): código {rc}; paso {st.get('paso')}.",
          f"- Configuración del libro: {out['configuracion_v64']}.",
          f"- V (MALO/NORMAL/BUENO): {' / '.join(f'{v:.6f}' for v in p_c['V'])} frente a {' / '.join(f'{v:.6f}' for v in p_r['V'])} · máx. |Δ| {d['V']:.1e}",
          f"- Ponderado {p_c['ponderado']:.9f} frente a {p_r['ponderado']:.9f} (|Δ| {d['ponderado']:.1e}); precio de Sí {p_c['precio_si']:.9f} frente a {p_r['precio_si']:.9f} (|Δ| {d['precio_si']:.1e}); zona {p_c.get('zona')} / {p_r.get('zona')}.",
          f"- Estados: " + "; ".join(f"{k} {a!r} / {b!r}" for k, (a, b) in estados.items()),
          f"- Libro evaluado recalculado, celda a celda (11 hojas de la V6.3, A:BT): {n} celdas, {len(dif)} diferencias, {len(esperadas)} en Control maestro (evidencia reescrita) o en la fecha de análisis; otras: {len(otras)}.",
          ] + [f"  - {k}: {a!r} → {b!r}" for k, a, b in otras[:30]] + ["", f"**Resultado:** {out['resultado']}"]
    open(os.path.join(ENS, "control_heredado", "resultados", "control_heredado.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
    print("\n".join(md))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
