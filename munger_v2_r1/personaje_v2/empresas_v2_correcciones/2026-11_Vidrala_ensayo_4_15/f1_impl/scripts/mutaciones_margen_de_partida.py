#!/usr/bin/env python3
"""Mutaciones de la corrección del margen de partida de motor_a_f1.py (19-nov-2026: m0 según Palancas C8, «Media del ciclo» → Historia C49) frente a
las baterías pruebas/test_motor_a_f1.py y pruebas/test_motor_a_f1_usgaap.py: cada mutación (una línea de la capa cambiada a propósito) tiene que
hacer que deje de pasar alguna prueba que pasa sin ella.

Uso (desde cualquier carpeta): python3 -I mutaciones_margen_de_partida.py [SALIDA.txt]
Trabaja sobre copias temporales de personaje_v2/scripts, esquema, prompts y las dos baterías: no toca el árbol. Sin LibreOffice. En esas copias no
están los binarios (el libro de Elis): las pruebas que lo necesitan fallan también sin mutar, así que se compara con la ejecución sin mutar.
"""
import os
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor

PV = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
SALIDA = sys.argv[1] if len(sys.argv) > 1 else None
BATERIAS = ("test_motor_a_f1.py", "test_motor_a_f1_usgaap.py")
M = [
    ("z01 · la base del margen no se lee (m0 siempre del último año)", "    ciclo = base_m0 == BASE_CICLO\n", "    ciclo = False\n"),
    ("z02 · la réplica solo contrasta la celda de la Historia", 'for ref in (celda, "Diagnóstico V6!C10", "Motor!D6", "Motor!D7", "Motor!D8"):', "for ref in (celda,):"),
    ("z03 · la réplica no contrasta m0", "    rep.extend(_replica_m0(L, m0_rep, base_m0, celda_m0))\n", "\n"),
    ("z04 · un valor de Palancas C8 fuera de la lista se acepta", '    if base not in (None, "") and base not in BASES_MARGEN:', "    if False:"),
    ("z05 · la celda de la Historia vacía no es diferencia", "        if v is None and ref != celda:", "        if v is None:"),
    ("z06 · la tolerancia de m0 se relaja a 10⁻²", "TOL_M0 = Fr(1, 10 ** 12)", "TOL_M0 = Fr(1, 10 ** 2)"),
    ("z07 · la partida K3 vuelve a ser el EBIT del año base", '                   (m0 * V0 - Eb) * (1 - tau5), "explicada"),',
     '                   (ebit[anios[-1]] - Eb) * (1 - tau5), "explicada"),'),
    ("z08 · con «Media del ciclo» y C49 incalculable no se para", '    if ciclo and margen_de_partida(anios, H["V"], H["EBIT"], V0, True) is None:', "    if False:"),
    ("z09 · la media del ciclo sobre la ventana y no sobre todos los años con ventas", "    con_ventas = [y for y in anios if V.get(y) is not None]",
     "    con_ventas = [y for y in anios[-3:] if V.get(y) is not None]"),
    ("z10 · N1 con «Media del ciclo» y un ajuste fuera de la ventana sin aviso en F1-PARAM", "        if ciclo and fuera:", "        if False:"),
    ("z11 · V-F1f: lo que lleva m0, siempre del año base", "        if not ciclo:\n            return serie[yL] / V0", "        if True:\n            return serie[yL] / V0"),
    ("z12 · el m0 del perímetro declarado sin N1 (la Historia en lugar del EBIT normalizado)", '        m0 = margen_de_partida(anios, H["V"], ebit, V0, ciclo)',
     '        m0 = margen_de_partida(anios, H["V"], H["EBIT"], V0, ciclo)'),
]
SRC = open(os.path.join(PV, "scripts", "motor_a_f1.py"), encoding="utf-8").read()


def correr(codigo):
    """(pasan, fallan): nombres de las pruebas de las dos baterías con la capa `codigo`, en una copia temporal."""
    tmp = tempfile.mkdtemp(prefix="mut_m0_")
    try:
        pv = os.path.join(tmp, "personaje_v2")
        for d in ("scripts", "esquema", "prompts"):
            shutil.copytree(os.path.join(PV, d), os.path.join(pv, d), ignore=shutil.ignore_patterns("__pycache__"))
        os.makedirs(os.path.join(pv, "pruebas"))
        for b in BATERIAS:
            shutil.copy(os.path.join(PV, "pruebas", b), os.path.join(pv, "pruebas"))
        open(os.path.join(pv, "scripts", "motor_a_f1.py"), "w", encoding="utf-8").write(codigo)
        td = os.path.join(tmp, "tmp")
        os.makedirs(td)
        pasan, fallan = set(), set()
        for b in BATERIAS:
            r = subprocess.run([sys.executable, "-B", os.path.join("pruebas", b)], cwd=pv, capture_output=True, text=True,
                               env=dict(os.environ, TMPDIR=td, PYTHONDONTWRITEBYTECODE="1"))
            for ln in r.stdout.splitlines():
                if ln.startswith("PASA "):
                    pasan.add((b, ln[8:160]))
                elif ln.startswith("FALLA"):
                    fallan.add((b, ln[8:160]))
            if r.returncode != 0 and "Traceback" in r.stderr:
                fallan.add((b, "la batería se interrumpe: " + r.stderr.strip().splitlines()[-1][:120]))
        return pasan, fallan
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


BASE_P, BASE_F = correr(SRC)


def una(m):
    nombre, viejo, nuevo = m
    n = SRC.count(viejo)
    if n != 1:
        return False, f"ERROR        · {nombre}: el texto a mutar aparece {n} veces"
    pasan, _ = correr(SRC.replace(viejo, nuevo))
    dejan = sorted(BASE_P - pasan)
    return bool(dejan), (("DETECTADA    " if dejan else "NO DETECTADA ") + f"· {nombre} · {len(dejan)} pruebas dejan de pasar"
                         + (f" (p. ej. «{dejan[0][1][:100]}»)" if dejan else ""))


with ThreadPoolExecutor(max_workers=int(os.environ.get("MUT_TRABAJADORES", "3"))) as ex:
    res = list(ex.map(una, M))
out = [f"sin mutar: {len(BASE_P)} pruebas pasan y {len(BASE_F)} fallan en la copia sin binarios (las del libro de Elis)"] + [x for _, x in res]
det = sum(ok for ok, _ in res)
out.append(f"\n{det} de {len(M)} mutaciones detectadas")
if SALIDA:
    open(SALIDA, "w", encoding="utf-8").write("\n".join(out) + "\n")
print("\n".join(out))
sys.exit(0 if det == len(M) else 1)
