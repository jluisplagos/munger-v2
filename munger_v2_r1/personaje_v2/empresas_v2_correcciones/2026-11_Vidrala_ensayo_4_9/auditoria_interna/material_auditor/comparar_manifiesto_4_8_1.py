#!/usr/bin/env python3
"""Compara el árbol auditado con reproduccion/MANIFIESTO_4_8_1.txt (modificados, ausentes y de más). Solo lectura."""
import hashlib, os
R = "/home/claude/auditoria_4_9/munger_v2_r1"
os.chdir(R)
man = "personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_9/reproduccion/MANIFIESTO_4_8_1.txt"
esp = dict(reversed(l.rstrip("\n").split("  ", 1)) for l in open(man, encoding="utf-8") if l.strip() and not l.startswith("#"))
act = {}
for r, ds, fs in os.walk("."):
    ds[:] = [d for d in ds if d != "__pycache__"]
    for f in fs:
        p = os.path.relpath(os.path.join(r, f), ".")
        act[p] = hashlib.sha256(open(p, "rb").read()).hexdigest()
print("MODIFICADOS:", sorted(p for p in esp if p in act and act[p] != esp[p]))
print("AUSENTES:", sorted(p for p in esp if p not in act))
extra = sorted(p for p in act if p not in esp)
print("DE MÁS fuera de .lo_perfil y del expediente 4.9:", [p for p in extra if "/.lo_perfil/" not in "/" + p and not p.startswith("personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_9/")])
