#!/usr/bin/env python3
"""Una pasada del pipeline real sobre un expediente del encargo 4.12, con registro (§7 y §8).

Uso (desde munger_v2_r1/): python3 -I …/scripts/paso_pipeline.py CARPETA_EMPRESA [--config config.json] [--hasta N] [--desde N]
Ejecuta pipeline.py una vez (por defecto con config_v2_v64_experimental.json), guarda la salida completa en
CARPETA_EMPRESA/../resultados/pipeline_NN_<paso>.txt y escribe en la consola el código, las últimas líneas y, si el pipeline espera a
un agente (código 10), su nombre, el archivo que tiene que escribir y el prompt generado. `--desde 13` es la vía documentada del pipeline
tras corregir el código que escribe el material provisional (ficha.py, informe.py): regenera el material, lo fija de nuevo y pide
una auditoría nueva; una aprobación del material anterior no vale para el nuevo. Cada código 10 es un relevo a un agente
real: se resuelve lanzando el agente y volviendo a ejecutar este script; nunca se entrega un expediente en espera.
"""
import json
import os
import re
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
PV = os.path.abspath(os.path.join(AQUI, "..", "..", ".."))
PIPE = os.path.join(PV, "scripts", "pipeline.py")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    c = os.path.abspath(sys.argv[1])
    cfg = sys.argv[sys.argv.index("--config") + 1] if "--config" in sys.argv else os.path.join(PV, "config_v2_v64_experimental.json")
    extra = ["--hasta", sys.argv[sys.argv.index("--hasta") + 1]] if "--hasta" in sys.argv else []
    extra += ["--desde", sys.argv[sys.argv.index("--desde") + 1]] if "--desde" in sys.argv else []
    res = os.path.join(os.path.dirname(c), "resultados")
    os.makedirs(res, exist_ok=True)
    n = 1 + max([int(m.group(1)) for f in os.listdir(res) for m in [re.match(r"pipeline_(\d+)_", f)] if m] or [0])
    st0 = {}
    try:
        st0 = json.load(open(os.path.join(c, "estado_pipeline.json"), encoding="utf-8"))
    except (OSError, ValueError):
        pass
    r = subprocess.run([sys.executable, PIPE, c, "--config", cfg] + extra, capture_output=True, text=True)
    salida = r.stdout + r.stderr
    st = {}
    try:
        st = json.load(open(os.path.join(c, "estado_pipeline.json"), encoding="utf-8"))
    except (OSError, ValueError):
        pass
    nombre = f"pipeline_{n:02d}_pasos_{st0.get('paso', 0)}_{st.get('paso', '?')}.txt"
    open(os.path.join(res, nombre), "w", encoding="utf-8").write(f"$ pipeline.py {c} --config {os.path.basename(cfg)} {' '.join(extra)}\ncódigo {r.returncode}\n\n{salida}")
    print(f"código {r.returncode} · paso {st0.get('paso', 0)} → {st.get('paso')} · estado {st.get('estado_analisis')} · auditoría {st.get('auditoria')} · registro {nombre}")
    print("\n".join(salida.strip().splitlines()[-6:]))
    esp = os.path.join(c, "ESPERANDO.md")
    if r.returncode == 10 and os.path.exists(esp):
        t = open(esp, encoding="utf-8").read()
        ag = t.split("**")[1] if "**" in t else "?"
        sal = t.split("Escribe **")[1].split("**")[0] if "Escribe **" in t else "?"
        prompts = sorted(f for f in os.listdir(os.path.join(c, "prompts_generados")) if ag in f) if os.path.isdir(os.path.join(c, "prompts_generados")) else []
        print(f"ESPERA al agente {ag} → escribir {sal} · prompt: {os.path.join(c, 'prompts_generados', prompts[-1]) if prompts else '—'}")
        if "CORRECCIÓN" in t:
            print("CORRECCIÓN: " + t.split("CORRECCIÓN:")[1].split("Entradas:")[0].strip()[:1500])
    return r.returncode


if __name__ == "__main__":
    sys.exit(main())
