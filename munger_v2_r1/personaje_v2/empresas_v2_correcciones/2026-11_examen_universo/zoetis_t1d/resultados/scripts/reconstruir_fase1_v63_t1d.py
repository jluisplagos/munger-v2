#!/usr/bin/env python3
"""zoetis_t1d · reconstruye fase1_v63.json con fase1_historia.py construir tras la corrección registrada de fase1_partes/AR_2018.json (Historia E26).
Guarda antes la versión de cambiar_base.py y su historia_revision.md en antecedentes/, comprueba que solo cambian los minoritarios de 2018 (y sus textos de
fuente y nota) y vuelve a añadir la nota del cambio de base que `construir` no reproduce. Uso: python3 -I reconstruir_fase1_v63_t1d.py CARPETA_EMPRESA CARPETA_ANTECEDENTES REGISTRO.json"""
import hashlib, json, os, shutil, subprocess, sys
C, ANT, REG = sys.argv[1:4]
h = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()  # noqa: E731
f1p, hr = os.path.join(C, "fase1_v63.json"), os.path.join(C, "historia_revision.md")
a_f1, a_hr = os.path.join(ANT, "fase1_v63_antes_de_corregir_AR_2018.json"), os.path.join(ANT, "historia_revision_antes_de_corregir_AR_2018.md")
assert not os.path.exists(a_f1) and not os.path.exists(a_hr)
shutil.copy2(f1p, a_f1)
shutil.copy2(hr, a_hr)
os.remove(f1p)
SCRIPTS = os.path.abspath(os.path.join(C, *[".."] * 4, "scripts"))
r = subprocess.run([sys.executable, "-B", os.path.join(SCRIPTS, "fase1_historia.py"), "construir", C], capture_output=True, text=True)
if r.returncode != 0:
    shutil.copy2(a_f1, f1p)
    sys.exit("construir falló (se restaura la versión anterior): " + (r.stdout + r.stderr)[-600:])
a, b = json.load(open(a_f1, encoding="utf-8")), json.load(open(f1p, encoding="utf-8"))
dif = []


def diff(x, y, p=""):
    if isinstance(x, dict) and isinstance(y, dict):
        for k in sorted(set(x) | set(y)):
            diff(x.get(k), y.get(k), f"{p}.{k}")
    elif isinstance(x, list) and isinstance(y, list) and len(x) == len(y) and p != "._notas":
        for i, (u, v) in enumerate(zip(x, y)):
            diff(u, v, f"{p}[{i}]")
    elif x != y:
        dif.append({"ruta": p, "antes": x, "despues": y})


diff(a, b)
rutas = sorted(d["ruta"] for d in dif)
assert rutas == ["._notas", ".historia.partidas.minoritarios.fuente", ".historia.partidas.minoritarios.nota", ".historia.partidas.minoritarios.valores[2]"], rutas
assert [d for d in dif if d["ruta"].endswith("valores[2]")][0]["despues"] == 0.0
perdidas = [n for n in a["_notas"] if n not in b["_notas"]]
assert len(perdidas) == 1 and perdidas[0].startswith("(cambio de base"), perdidas
b["_notas"] += perdidas + ["(zoetis_t1d, 19-nov-2026) fase1_v63.json reconstruido con fase1_historia.py construir tras la corrección registrada de fase1_partes/AR_2018.json "
                           "(minoritarios 2018 = «—» impreso → 0; resultados/correccion_fase1_partes_t1d.json); se conserva la nota del cambio de base; la versión de "
                           "cambiar_base.py está en antecedentes/fase1_v63_antes_de_corregir_AR_2018.json."]
json.dump(b, open(f1p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump({"fecha": "2026-11-19", "guion": "resultados/scripts/reconstruir_fase1_v63_t1d.py", "salida_construir": r.stdout[-1000:], "diferencias": dif,
           "antes_sha256": h(a_f1), "despues_sha256": h(f1p), "historia_revision_antes_sha256": h(a_hr), "historia_revision_despues_sha256": h(hr)},
          open(REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
print("OK", rutas)
