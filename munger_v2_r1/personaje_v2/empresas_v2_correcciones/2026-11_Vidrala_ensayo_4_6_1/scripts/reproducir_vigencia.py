#!/usr/bin/env python3
"""Reproduce el caso de la revisión independiente (encargo 4.6.1, §2–§3): salida oficial obsoleta que sigue apareciendo como aprobada.

Uso: python3 -I reproducir_vigencia.py --raiz <munger_v2_r1 de la versión a probar> [--expediente <carpeta Vidrala aprobada de la 4.6>]

Trabaja en una copia temporal del expediente aprobado (con su resumen_v2.csv); el expediente original no se modifica.
Pasos: estado inicial · modificación de fase_c.json → celdas.B101 · pipeline --desde 14 · estado después del rechazo (pipeline,
ficha, informe, fila del resumen) · informe.py directo · ficha.py directo. Con el código 4.6 el caso se REPRODUCE; con el reparado, no.
"""
import argparse
import csv
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

ap = argparse.ArgumentParser()
ap.add_argument("--raiz", required=True)
ap.add_argument("--expediente")
a = ap.parse_args()
R = os.path.abspath(a.raiz)
SCR = os.path.join(R, "personaje_v2", "scripts")
EXP = os.path.abspath(a.expediente or os.path.join(R, "personaje_v2", "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_6", "Vidrala"))
PY = sys.executable
MARCA = " [TESIS DE PRUEBA AÑADIDA DESPUÉS DE LA AUDITORÍA]"
tmp = tempfile.mkdtemp(prefix="vigencia461_")
d = os.path.join(tmp, "expediente", "Vidrala")
shutil.copytree(EXP, d, ignore=shutil.ignore_patterns(".lo_perfil"))
shutil.copy(os.path.join(os.path.dirname(EXP), "resumen_v2.csv"), os.path.join(tmp, "expediente", "resumen_v2.csv"))
CSV = os.path.join(tmp, "expediente", "resumen_v2.csv")


def j(f):
    p = os.path.join(d, f)
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else None


def fila():
    return next(({k: r[k] for k in ("empresa", "estado_analisis", "verificacion")} for r in csv.DictReader(open(CSV, encoding="utf-8")) if r.get("empresa") == "Vidrala, S.A."), None) if os.path.exists(CSV) else None


def estado(titulo):
    st, fi = j("estado_pipeline.json"), j("ficha.json")
    inf = open(os.path.join(d, "informe.md"), encoding="utf-8").read() if os.path.exists(os.path.join(d, "informe.md")) else None
    print(f"\n-- {titulo}")
    print(f"   pipeline: paso {st['paso']} · estado {st.get('estado_analisis')!r} · auditoría {st.get('auditoria')!r}")
    print(f"   ficha.json: {'ausente' if fi is None else 'estado ' + repr(fi.get('estado_analisis')) + ' · cierre ' + repr(fi.get('cierre'))}")
    print(f"   informe.md: {'ausente' if inf is None else 'presente · ' + inf.splitlines()[0][:60] + ' · «Estado `concluido`» ' + str('Estado `concluido`' in inf) + ' · tesis de prueba ' + str(MARCA.strip() in inf)}")
    print(f"   fila del resumen: {fila()}")
    hist = os.path.join(d, "historial_cierres")
    print(f"   historial_cierres/: {sorted(os.listdir(hist)) if os.path.isdir(hist) else 'no existe'}")
    return st, fi, inf


def corre(etiqueta, cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    out = (r.stdout + r.stderr).strip()
    print(f"\n$ {etiqueta} → código {r.returncode}")
    print("   " + (out.splitlines()[-1][:220] if out else ""))
    return r.returncode


print(f"REPRODUCCIÓN DEL CASO DE VIGENCIA · código de {R}")
try:
    estado("estado inicial (expediente aprobado, copia temporal)")
    fc = j("fase_c.json")
    antes = hashlib.sha256(open(os.path.join(d, "fase_c.json"), "rb").read()).hexdigest()
    fc["celdas"]["B101"] = fc["celdas"]["B101"] + MARCA
    json.dump(fc, open(os.path.join(d, "fase_c.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"\nmodificación: fase_c.json → celdas.B101 += «{MARCA.strip()}» (SHA-256 {antes[:12]}… → {hashlib.sha256(open(os.path.join(d, 'fase_c.json'), 'rb').read()).hexdigest()[:12]}…)")
    rc14 = corre("pipeline.py <copia> --desde 14", [PY, "-B", os.path.join(SCR, "pipeline.py"), d, "--desde", "14"])
    st, fi, inf = estado("después del rechazo")
    obsoleta = (fi or {}).get("estado_analisis") == "concluido" or (inf is not None and "Estado `concluido`" in inf) or (fila() or {}).get("verificacion") == "APROBADO"
    rci = corre("informe.py <copia> (directo)", [PY, "-B", os.path.join(SCR, "informe.py"), d])
    st, fi, inf = estado("después de informe.py directo")
    publicada = rci == 0 and inf is not None and MARCA.strip() in inf and "Estado `concluido`" in inf
    rcf = corre("ficha.py <copia> --estado concluido (directo)", [PY, "-B", os.path.join(SCR, "ficha.py"), d, "--estado", "concluido"])
    st, fi, inf = estado("después de ficha.py directo")
    ficha_vigente = (fi or {}).get("estado_analisis") == "concluido"
    print("\nVEREDICTO")
    print("  --desde 14: " + ("REPRODUCIDO: rechaza (código 4) pero ficha, informe o resumen siguen presentando concluido / APROBADO" if rc14 == 4 and obsoleta else
                              f"NO SE REPRODUCE: código {rc14} y ninguna salida ni fila presenta la versión modificada como concluida y aprobada"))
    print("  informe.py directo: " + ("REPRODUCIDO: publica la tesis modificada bajo el cierre anterior (código 0)" if publicada else
                                     f"NO SE REPRODUCE: código {rci}; no publica el contenido nuevo como aprobado"))
    print("  ficha.py directo: " + ("REPRODUCIDO: la ficha oficial anterior sigue presentando concluido" if ficha_vigente else
                                   f"NO SE REPRODUCE: código {rcf}; ninguna ficha oficial presenta concluido"))
finally:
    shutil.rmtree(tmp, ignore_errors=True)
