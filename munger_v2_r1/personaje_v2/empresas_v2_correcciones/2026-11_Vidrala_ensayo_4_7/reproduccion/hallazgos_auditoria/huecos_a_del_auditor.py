#!/usr/bin/env python3
"""Pruebas propias del auditor sobre la copia (no forman parte del paquete)."""
import json, os, shutil, sys
COPIA = "/tmp/claude-0/-home-claude/e1d9fd2f-7a4e-5443-8b0f-fae3b340b4cf/scratchpad/aud47/munger_v2_r1/personaje_v2"
sys.path.insert(0, os.path.join(COPIA, "pruebas"))
os.chdir(COPIA)
import test_resumen_v2 as T  # noqa

EXP = os.path.join(COPIA, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_6_1", "Vidrala")


def estado(rows):
    return [(r["estado_analisis"], r["verificacion"][:28]) for r in rows]


def reg(d):
    return [(e["csv"][-30:], e["expediente"][-25:], e["estado"]) for e in (T.j(d, T.REG) or {}).get("publicaciones", [])]

# A. expediente movido (renombrado) tras publicar en el CSV configurado
d, conf, pers, pred = T.caso(EXP)
rc, _ = T.run("pipeline.py", d, "--config", conf, "--desde", "14")
nuevo = os.path.join(os.path.dirname(os.path.dirname(d)), "exp_movido", "Vidrala")
shutil.move(os.path.dirname(d), os.path.dirname(nuevo))
T.marca(nuevo)
rc2, out2 = T.run("informe.py", nuevo)
print("A movido:", rc, rc2, "pers", estado(T.de(pers)), "reg", reg(nuevo))

# B. registro borrado antes de la invalidación por informe.py directo
d, conf, pers, pred = T.caso(EXP)
T.run("pipeline.py", d, "--config", conf, "--desde", "14")
os.remove(os.path.join(d, T.REG))
T.marca(d)
rc, out = T.run("informe.py", d)
print("B registro borrado:", rc, "pers", estado(T.de(pers)), "pred", estado(T.de(pred)))

# C. registro corrupto
d, conf, pers, pred = T.caso(EXP)
T.run("pipeline.py", d, "--config", conf, "--desde", "14")
open(os.path.join(d, T.REG), "w").write("{corrupto")
T.marca(d)
rc, out = T.run("informe.py", d)
print("C registro corrupto:", rc, out[-160:].replace("\n", " | "), "pers", estado(T.de(pers)))
rc, out = T.run("pipeline.py", d, "--config", conf, "--desde", "14")
print("C' pipeline con registro corrupto:", rc, out[-120:].replace("\n", " | "))

# D. copia del expediente invalidada por el pipeline CONFIGURADO (misma configuración que el original)
d0, conf0, pers0, pred0 = T.caso(EXP)
T.run("pipeline.py", d0, "--config", conf0, "--desde", "14")
dc = os.path.join(os.path.dirname(os.path.dirname(d0)), "copia2", "Vidrala")
shutil.copytree(d0, dc)
T.marca(dc)
rc, _ = T.run("pipeline.py", dc, "--config", conf0, "--desde", "14")
print("D copia invalidada con la config compartida:", rc, "pers0 (original)", estado(T.de(pers0)))

# E. dos expedientes publican en el mismo CSV; el primero se invalida después de que el segundo publique
d1, conf1, pers1, _ = T.caso(EXP)
T.run("pipeline.py", d1, "--config", conf1, "--desde", "14")
d2 = os.path.join(os.path.dirname(os.path.dirname(d1)), "segundo", "Vidrala")
shutil.copytree(d1, d2)
os.remove(os.path.join(d2, T.REG))
rc_b, _ = T.run("resumen.py", d2, pers1)  # el segundo publica (vigente) en el mismo CSV
T.marca(d1)
rc, _ = T.run("informe.py", d1)
print("E segundo publica", rc_b, "; primero invalidado", rc, "-> CSV compartido", estado(T.de(pers1)), "| motivo vigencia segundo:",
      T.CIE.motivo_vigencia(d2, __import__("pipeline").Pipeline.veredicto_auditoria))

# F. resumen.py tras salidas archivadas con retirada pendiente
d, conf, pers, pred = T.caso(EXP)
T.run("pipeline.py", d, "--config", conf, "--desde", "14")
copia = open(pers, encoding="utf-8").read(); os.remove(pers); os.makedirs(pers)
T.marca(d)
rc, _ = T.run("informe.py", d)
rcr, outr = T.run("resumen.py", d, pred)
print("F informe", rc, "; resumen.py tras archivo:", rcr, outr[-140:].replace("\n", " | "))

# G. destino ausente (renombrado / desmontado) en la invalidación: ¿pendiente o «retirada»?
d, conf, pers, pred = T.caso(EXP)
T.run("pipeline.py", d, "--config", conf, "--desde", "14")
os.rename(os.path.dirname(pers), os.path.dirname(pers) + "_desmontado")
T.marca(d)
rc, _ = T.run("informe.py", d)
print("G destino ausente:", rc, reg(d))
os.rename(os.path.dirname(pers) + "_desmontado", os.path.dirname(pers))
rc, _ = T.run("pipeline.py", d, "--config", conf, "--desde", "14")
print("G' destino vuelve:", rc, "pers", estado(T.de(pers)))

# H. CSV de solo lectura (permiso) como root: ¿se detecta?
print("uid", os.getuid())
shutil.rmtree(T.TMP, ignore_errors=True)
