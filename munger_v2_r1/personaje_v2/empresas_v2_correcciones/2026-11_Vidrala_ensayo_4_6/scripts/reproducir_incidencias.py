#!/usr/bin/env python3
"""Reproduce las cuatro incidencias del cierre (encargo 4.6, §7) con el código de un paquete dado. Solo trabaja en copias temporales.

Uso: python3 -I reproducir_incidencias.py --raiz <munger_v2_r1 de la versión a probar> [--expediente <carpeta Vidrala de la 4.5>]

Con el código de la 4.5 las cuatro se reproducen («REPRODUCIDA»); con el reparado, no («NO SE REPRODUCE»). No cambia el expediente.
  I1 · `concluido` publicado antes de la auditoría: --desde 11 --hasta 11 sin auditoria.md (¿ficha.json oficial dice concluido?) y
       --desde 14 sin auditoría (¿cierra?).
  I2 · marca «con datos de etapa 1 incompletos»: ¿falta en ficha.json e informe.md con necesarios_para_listo_provisional no vacío?
  I3 · C104 «fundamento …»: ¿coherencia_fase_c acepta una etiqueta fuera de las cuatro y una etiqueta contradictoria con el JSON?
  I4 · aviso de alcance exploratorio: ¿faltan en las secciones 6 y 7 del informe junto al DCF inverso, la escalera y la zona?
"""
import argparse
import json
import os
import re
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
EXP = os.path.abspath(a.expediente or os.path.join(R, "personaje_v2", "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_5", "Vidrala"))
PY = sys.executable
MARCA = "con datos de etapa 1 incompletos"
tmp = tempfile.mkdtemp(prefix="repro46_")


def copia(nombre, sin=()):
    d = os.path.join(tmp, nombre, "Vidrala")
    shutil.copytree(EXP, d, ignore=shutil.ignore_patterns(".lo_perfil"))
    for f in sin:
        if os.path.exists(os.path.join(d, f)):
            os.remove(os.path.join(d, f))
    return d


def corre(*args):
    r = subprocess.run([PY, "-B", os.path.join(SCR, "pipeline.py"), *args], capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr).strip()


def ficha_oficial(d):
    p = os.path.join(d, "ficha.json")
    return json.load(open(p, encoding="utf-8")).get("estado_analisis") if os.path.exists(p) else None


def seccion(md, n):
    m = re.search(rf"^## {n}\..*?(?=^## \d+\.|\Z)", md, flags=re.M | re.S)
    return m.group(0) if m else ""


print(f"REPRODUCCIÓN DE LAS CUATRO INCIDENCIAS · código de {R}")
print(f"expediente de partida: {os.path.relpath(EXP, R) if EXP.startswith(R) else EXP}")
try:
    # I1
    d = copia("i1a", sin=("ficha.json", "informe.md", "auditoria.md"))
    rc, out = corre(d, "--desde", "11", "--hasta", "11")
    e = ficha_oficial(d)
    print(f"\nI1a · paso 11 sin auditoría: código {rc}; ficha.json oficial = {e!r}; ficha_provisional.json = {os.path.exists(os.path.join(d, 'ficha_provisional.json'))}")
    print("     " + ("REPRODUCIDA: la salida oficial confirma «concluido» antes de la auditoría" if e == "concluido" else "NO SE REPRODUCE: ninguna salida oficial confirma «concluido» antes de la auditoría"))
    d = copia("i1b", sin=("ficha.json", "informe.md", "auditoria.md"))
    st = json.load(open(os.path.join(d, "estado_pipeline.json"), encoding="utf-8"))
    st["auditoria"] = None
    json.dump(st, open(os.path.join(d, "estado_pipeline.json"), "w", encoding="utf-8"))
    rc, out = corre(d, "--desde", "14")
    e = ficha_oficial(d)
    print(f"I1b · --desde 14 sin auditoría: código {rc}; ficha.json oficial = {e!r}; última línea: {out.splitlines()[-1] if out else ''}")
    print("     " + ("REPRODUCIDA: cierra sin aprobación" if e == "concluido" else "NO SE REPRODUCE: el cierre se rechaza sin aprobación"))
    # I2
    ent = json.load(open(os.path.join(EXP, "entrada_v63.json"), encoding="utf-8"))
    nec = [x["dato"] for x in ent.get("necesarios_para_listo_provisional") or []]
    d = copia("i2")
    # se regeneran ficha e informe con el código a probar: con --provisional si lo admite (código reparado), si no sin él (4.5)
    r = subprocess.run([PY, "-B", os.path.join(SCR, "ficha.py"), d, "--provisional"], capture_output=True, text=True)
    prov = r.returncode == 0
    if not prov:
        subprocess.run([PY, "-B", os.path.join(SCR, "ficha.py"), d], capture_output=True, text=True)
    subprocess.run([PY, "-B", os.path.join(SCR, "informe.py"), d] + (["--provisional"] if prov else []), capture_output=True, text=True)
    fi = json.load(open(os.path.join(d, "ficha_provisional.json" if prov else "ficha.json"), encoding="utf-8"))
    inf2 = open(os.path.join(d, "informe_provisional.md" if prov else "informe.md"), encoding="utf-8").read()
    en_ficha = MARCA in json.dumps(fi, ensure_ascii=False)
    en_s1 = MARCA in seccion(inf2, 1)
    print(f"\nI2 · necesarios_para_listo_provisional: {len(nec)} ({'; '.join(nec)})")
    print(f"     marca en la ficha regenerada con este código: {en_ficha}; en la sección 1 del informe regenerado: {en_s1}")
    print("     " + ("REPRODUCIDA: falta la marca obligatoria" if nec and not (en_ficha and en_s1) else "NO SE REPRODUCE"))
    # I3
    sys.path.insert(0, SCR)
    sys.dont_write_bytecode = True
    import config_v2
    import pipeline
    cfg = config_v2.cargar(os.path.join(R, "personaje_v2", "config_v2.json"))
    d = copia("i3")
    P = pipeline.Pipeline(d, cfg)
    fc = json.load(open(os.path.join(d, "fase_c.json"), encoding="utf-8"))
    c104 = fc["celdas"]["C104"]
    m = re.search(r"fundamento ([^·]+)", c104)
    print(f"\nI3 · resultado {fc['fundamento_material']['resultado']!r}; etiqueta de C104: «fundamento {m.group(1).strip() if m else '?'}»")
    print(f"     coherencia_fase_c (fase C real): {P.coherencia_fase_c(fc)!r}")
    raras = 0
    for etiqueta in ("XYZ inventada", "lista vacía"):
        f2 = json.loads(json.dumps(fc))
        f2["celdas"]["C104"] = re.sub(r"fundamento [^·]+", f"fundamento {etiqueta} ", c104)
        r = P.coherencia_fase_c(f2)
        raras += r is None
        print(f"     coherencia_fase_c con «fundamento {etiqueta}» y resultado no_procede: {r!r}")
    print("     " + ("REPRODUCIDA: no hay correspondencia: acepta etiquetas desconocidas o contradictorias con el JSON" if raras else "NO SE REPRODUCE: rechaza etiquetas desconocidas y contradictorias"))
    # I4
    s6, s7 = seccion(inf2, 6), seccion(inf2, 7)
    print(f"\nI4 · alcance_v2.json en el expediente: {os.path.exists(os.path.join(EXP, 'alcance_v2.json'))} (sin ese metadato explícito ningún código añade avisos)")
    pat = re.compile(r"ruta A|ensayo exploratorio|no comparable", re.I)
    print(f"     sección 6 (DCF inverso) con aviso de alcance: {bool(pat.search(s6))}; sección 7 (escalera y zona) con aviso: {bool(pat.search(s7))}")
    print("     " + ("REPRODUCIDA: las secciones 6 y 7 comparan con el precio sin aviso local" if not (pat.search(s6) and pat.search(s7)) else "NO SE REPRODUCE"))
finally:
    shutil.rmtree(tmp, ignore_errors=True)
