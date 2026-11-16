#!/usr/bin/env python3
"""g11 · séptima comprobación · FUERA DEL DIFF (no cambia desde antes del hito 2): `fase1_historia.importe_completo` (`:93`), el control
de la fase 1 que exige que el importe impreso de un componente esté en su línea y en su página «como importe completo», no trata el
apóstrofo (ASCII ni tipográfico) como parte de un número: el mismo límite que V7 y W3 señalaron en `verificacion_entradas.py`.
Uso: python3 -I -B g11_importe_completo_fase1.py"""
import hashlib, os, subprocess, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
F = os.path.dirname(AQUI)
sys.dont_write_bytecode = True
os.environ["PATH"] = os.path.join(F, "bin") + os.pathsep + os.environ.get("PATH", "")
sys.path.insert(0, os.path.join(F, "copia", "munger_v2_r1", "personaje_v2", "scripts"))
import fase1_historia as FH  # noqa: E402
src = open(FH.__file__, encoding="utf-8").read().split("\n")
print("fase1_historia.py:", hashlib.sha256("\n".join(src).encode("utf-8")).hexdigest()[:8] + "…", "· línea 93:", src[92].strip())
for imp, texto, esperado in (("849,7", "Total 1.849,7", False), ("849,7", "Total 1,849,7", False), ("7", "Total 7,608", False), ("849,7", "Total 849,7", True),
                             ("849,7", "Total 1'849,7", False), ("849,7", "Total 1’849,7", False), ("849", "Total 849'697", False), ("849", "Total 849’697", False),
                             ("849,7", "Total 1 849,7", None)):
    r = FH.importe_completo(FH.norm(imp), FH.norm(texto))
    print(f"   importe_completo({imp!r:8}, {texto!r:18}) = {r!s:5}" + ("" if esperado is None or r == esperado else "   <<< el revisor esperaba " + str(esperado)) + ("   (miles con espacio: límite conocido)" if esperado is None else ""))
print("   usos:", [f":{i + 1}" for i, l in enumerate(src) if "importe_completo(" in l and not l.startswith("def ")])
try:
    r = subprocess.run(["git", "-C", "/home/user/munger-v2", "log", "--format=%h %s", "-L", "90,93:munger_v2_r1/personaje_v2/scripts/fase1_historia.py", "-s"], capture_output=True, text=True, timeout=60)
    print("   commits que tocan esas líneas (git log -L, solo lectura):", [l[:70] for l in r.stdout.strip().split("\n") if l][:4])
except Exception as e:  # noqa: BLE001
    print("   (git log no disponible:", e, ")")
