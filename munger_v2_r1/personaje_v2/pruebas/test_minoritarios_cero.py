#!/usr/bin/env python3
"""Pruebas de los minoritarios impresos en negativo (fase1_historia.py; decisión Z-MIN de la persona responsable, 19-nov-2026; examen,
zoetis_t1c; rama producto/minoritarios-cero).

Zoetis imprime «Equity attributable to noncontrolling interests» (2) en 2022 y (6) en 2023 (10-K). ajustar tomaba el valor absoluto y la
Historia guardaba +2 y +6. Decisión Z-MIN: minoritarios deficitarios → 0 con aviso, conservando la cifra impresa. Solo cambia
«minoritarios»: pensiones (posición neta) y las demás partidas siguen igual, y la plantilla no cambia (fila 26 ≥ 0).
No escribe en el repositorio: trabaja sobre copias temporales.
Uso: python3 -B pruebas/test_minoritarios_cero.py      (código 0 si todo pasa)
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
PV = os.path.dirname(AQUI)
ZOETIS = os.path.join(PV, "empresas_v2_correcciones", "2026-11_examen_universo", "zoetis_t1c", "Zoetis")
PARTES = ("texto", "fase1_partes", "fase1_metadatos.json", "fase1_fuentes.json", "fase1_decisiones.json")
fallos, total = [], 0


def paso(nombre, ok, detalle=""):
    global total
    total += 1
    print(("PASA " if ok else "FALLA") + f" · {nombre}" + (f" · {detalle}" if detalle else ""))
    if not ok:
        fallos.append(nombre)


def copiar(dest):
    os.makedirs(dest)
    for n in PARTES:
        s = os.path.join(ZOETIS, n)
        if os.path.isdir(s):
            shutil.copytree(s, os.path.join(dest, n))
        elif os.path.exists(s):
            shutil.copy2(s, os.path.join(dest, n))
    return dest


def construir(c):
    r = subprocess.run([sys.executable, "-B", os.path.join(PV, "scripts", "fase1_historia.py"), "construir", c], capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr).strip()


t = tempfile.mkdtemp(prefix="minoritarios_cero_")
try:
    if os.path.isdir(os.path.join(ZOETIS, "fase1_partes")) and os.path.isdir(os.path.join(ZOETIS, "texto")):
        c = copiar(os.path.join(t, "z", "Zoetis"))
        rc, out = construir(c)
        paso("zoetis_t1c: construye", rc == 0, out[-160:])
        if rc == 0:
            h = json.load(open(os.path.join(c, "fase1_v63.json"), encoding="utf-8"))["historia"]
            ref = json.load(open(os.path.join(ZOETIS, "fase1_v63.json"), encoding="utf-8"))["historia"]  # construido antes de Z-MIN
            rev = open(os.path.join(c, "historia_revision.md"), encoding="utf-8").read()
            anios, mi = h["anios"], h["partidas"]["minoritarios"]

            def val(hh, k, a):
                return hh["partidas"][k]["valores"][hh["anios"].index(a)]
            # 1 · minoritarios impresos en negativo → 0 (antes el valor absoluto)
            paso("minoritarios 2022, impreso (2) → 0 (antes +2)", val(h, "minoritarios", 2022) == 0.0 and val(ref, "minoritarios", 2022) == 2.0,
                 f"{val(h, 'minoritarios', 2022)!r} (antes {val(ref, 'minoritarios', 2022)!r})")
            paso("minoritarios 2023, impreso (6) → 0 (antes +6)", val(h, "minoritarios", 2023) == 0.0 and val(ref, "minoritarios", 2023) == 6.0,
                 f"{val(h, 'minoritarios', 2023)!r} (antes {val(ref, 'minoritarios', 2023)!r})")
            paso("el 0 es un cero, no un desconocido ni un cero negativo", all(str(val(h, "minoritarios", a)) == "0.0" for a in (2022, 2023)))
            # 2 · nada más cambia: minoritarios positivos, pensiones y el resto de la Historia
            otros = [a for a in anios if a not in (2022, 2023)]
            paso("minoritarios de los demás años sin cambio (12, 16, —, 0, 4, 1, 0, 0)",
                 [val(h, "minoritarios", a) for a in otros] == [val(ref, "minoritarios", a) for a in otros], str([val(h, "minoritarios", a) for a in otros]))
            dif = [f"{k} {a}" for k, p in ref["partidas"].items() if k != "minoritarios" for a in ref["anios"] if val(ref, k, a) != val(h, k, a)]
            paso("toda la Historia salvo minoritarios 2022–2023 igual que antes (también pensiones, impresa en negativo)", h["anios"] == ref["anios"] and not dif,
                 "; ".join(dif[:6]))
            paso("pensiones sigue en valor absoluto (posición neta: déficit impreso en negativo, 42 en 2025)", val(h, "pensiones", 2025) == 42.0)
            # 3 · el aviso, con la cifra impresa, el año y la página
            lin = {a: next((x for x in rev.splitlines() if x.startswith(f"- **minoritarios {a}**")), "") for a in (2022, 2023)}
            paso("historia_revision.md avisa de minoritarios 2022: cifra impresa −2, página 67 del 10-K 2023, guarda 0, decisión Z-MIN",
                 all(x in lin[2022] for x in ("-2.0", "zoetis-10k-fy2023.txt p.67", "guarda 0", "Z-MIN")), lin[2022][:200])
            paso("y de minoritarios 2023: cifra impresa −6, página 66 del 10-K 2024",
                 all(x in lin[2023] for x in ("-6.0", "zoetis-10k-fy2024.txt p.66", "guarda 0", "Z-MIN")), lin[2023][:200])
            paso("la fuente de la fila conserva la cifra impresa", "impreso -2.0" in mi["fuente"][anios.index(2022)] and "impreso -6.0" in mi["fuente"][anios.index(2023)]
                 if isinstance(mi.get("fuente"), list) else ("impreso -2.0" in str(mi) and "impreso -6.0" in str(mi)), str(mi.get("fuente"))[:200])
            paso("pensiones no se avisa (no es una fila ≥ 0 de la plantilla)", "**pensiones" not in rev)
    else:  # el expediente del examen no forma parte de todos los paquetes: sin él, la prueba se omite y lo dice
        print(f"OMITIDA · construir sobre zoetis_t1c: no está el expediente {ZOETIS}")
finally:
    shutil.rmtree(t, ignore_errors=True)

print(f"\n{total - len(fallos)}/{total} comprobaciones PASAN")
sys.exit(1 if fallos else 0)
