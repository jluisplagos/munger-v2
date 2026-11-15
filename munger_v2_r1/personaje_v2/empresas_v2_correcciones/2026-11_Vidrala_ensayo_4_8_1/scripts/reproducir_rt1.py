#!/usr/bin/env python3
"""Reproducción del hallazgo externo R-T1 (entrega 4.8.1) con el código de un árbol dado; solo escribe en temporales.

Uso (desde munger_v2_r1/):
  python3 -I personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_8_1/scripts/reproducir_rt1.py --raiz <munger_v2_r1 del código> [--etiqueta 4.8]

El guion hace lo mismo que la revisión externa, con el código de `--raiz` y el expediente aprobado de la 4.6.1 de este árbol:
1. Provoca X-c: la ficha falla su esquema al cerrar, porque el esquema exige un campo inexistente, y se lanza `--desde 14`.
2. Restaura el esquema y relanza `--desde 13`.
3. Repite los pasos 1 y 2 en los tres modos de fechas de la descompresión:
   - cet: las fechas del ZIP leídas en CET;
   - utc: las fechas DOS leídas en UTC, una hora después;
   - renovadas: todas las fechas, ahora.
   Los fija sobre la copia, sin depender de la zona horaria de la máquina; el procedimiento es el mismo que en
   pruebas/test_auditorias_v2.py.

Resultado correcto: en los tres modos se pide una auditoría nueva, con código 10, y no se cierra nada.
Los identificadores de solicitud, aleatorios, se escriben como «SA-<id>» para que la salida sea reproducible.
Código del guion: 0 si los tres modos piden auditoría nueva; 1 si alguno reutiliza la auditoría antigua.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time

sys.dont_write_bytecode = True
AQUI = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
EXP = os.path.join(os.path.dirname(AQUI), "2026-11_Vidrala_ensayo_4_6_1", "Vidrala")
ap = argparse.ArgumentParser()
ap.add_argument("--raiz", required=True)
ap.add_argument("--etiqueta", default="")
a = ap.parse_args()
RAIZ = os.path.join(os.path.abspath(a.raiz), "personaje_v2")
TMP = tempfile.mkdtemp(prefix="rt1_")


def j(p):
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}


def corre(pipe, d, *extra):
    r = subprocess.run([sys.executable, "-B", pipe, d, *extra], capture_output=True, text=True, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
    out = (r.stdout + r.stderr).strip()
    return r.returncode, (out.splitlines() or [""])[-1]


try:
    roto = os.path.join(TMP, "codigo_roto")
    shutil.copytree(RAIZ, os.path.join(roto, "personaje_v2"), ignore=shutil.ignore_patterns("empresas_v2", "empresas_v2_correcciones", "pruebas", ".lo_perfil", "__pycache__"))
    for x in ("v6", "kit_pipeline_munger"):
        os.symlink(os.path.join(os.path.dirname(RAIZ), x), os.path.join(roto, x))
    esq = os.path.join(roto, "personaje_v2", "esquema", "ficha.esquema.json")
    e = json.load(open(esq, encoding="utf-8"))
    e["required"] = list(e["required"]) + ["campo_inexistente_xc"]
    json.dump(e, open(esq, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    pipe_roto, pipe = os.path.join(roto, "personaje_v2", "scripts", "pipeline.py"), os.path.join(RAIZ, "scripts", "pipeline.py")
    reutiliza = []
    print(f"R-T1 · código de {a.etiqueta or a.raiz}")
    for modo in ("cet", "utc", "renovadas"):
        base = os.path.join(TMP, modo, "exp")
        d = os.path.join(base, "Vidrala")
        shutil.copytree(EXP, d, ignore=shutil.ignore_patterns(".lo_perfil"))
        for f in ("resumen_v2.csv", "resumen_v2_historial.csv"):
            shutil.copy2(os.path.join(os.path.dirname(EXP), f), os.path.join(base, f))
        todos = [os.path.join(r, f) for r, _, fs in os.walk(base) for f in fs]
        if modo == "renovadas":
            t = time.time()
            for p in todos:
                os.utime(p, (t, t))
        else:
            c = j(os.path.join(d, "estado_pipeline.json"))["consumidos"]["auditoria.md"]
            delta = (int(c) // 2) * 2 + (3600 if modo == "utc" else 0) - os.path.getmtime(os.path.join(d, "auditoria.md"))
            for p in todos:
                os.utime(p, (os.path.getmtime(p) + delta,) * 2)
        rc1, u1 = corre(pipe_roto, d, "--desde", "14")
        rc2, u2 = corre(pipe, d, "--desde", "13")
        st, fi = j(os.path.join(d, "estado_pipeline.json")), j(os.path.join(d, "ficha.json"))
        nueva = rc2 == 10 and st.get("auditoria") != "APROBADO" and not fi.get("cierre")
        if not nueva:
            reutiliza.append(modo)
        print(f"  {modo:9s} X-c: código {rc1} ({u1[:60]}) · esquema restaurado, --desde 13: código {rc2} · estado {st.get('estado_analisis')!r} · auditoría {st.get('auditoria')!r} · "
              f"ficha con cierre {bool(fi.get('cierre'))} · {'pide una auditoría nueva' if nueva else 'REUTILIZA la auditoría antigua'} · {re.sub(r'SA-[0-9a-f]{16}', 'SA-<id>', u2)[:90]}")
    print("RESULTADO: " + ("en los tres modos se pide una auditoría nueva" if not reutiliza else f"la auditoría antigua se reutiliza en: {', '.join(reutiliza)}"))
finally:
    shutil.rmtree(TMP, ignore_errors=True)
sys.exit(0 if not reutiliza else 1)
