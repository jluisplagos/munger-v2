#!/usr/bin/env python3
"""Rellena en REVISION_FABLE_HITO2.md la tabla de mutaciones y los datos que dependen de ellas (lee fable/mut*/…/resultado.json)."""
import json, os, re, sys
F = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INF = os.path.join(F, "REVISION_FABLE_HITO2.md")
CORTO = {"test_verificacion_entradas_415.py": "entradas 4.15", "test_entrada_efectiva_415.py": "entrada efectiva", "test_verificacion_entradas_414.py": "entradas 4.14"}


def leer(base):
    out = {}
    d0 = os.path.join(F, base)
    for n in sorted(os.listdir(d0)) if os.path.isdir(d0) else []:
        p = os.path.join(d0, n, "resultado.json")
        if os.path.exists(p):
            out[n] = json.load(open(p, encoding="utf-8"))
    return out


def detectada(r):
    return not all(v["codigo"] == 0 and not v["fallan"] for v in r["baterias"].values())


def celda(r):
    partes = []
    for b, v in r["baterias"].items():
        if v["codigo"] == 0 and not v["fallan"]:
            partes.append(f"{CORTO[b]}: {v['pasan'].replace(' pruebas', '')}")
        elif v["fallan"]:
            partes.append(f"{CORTO[b]}: {(v['pasan'] or 'abortada').replace(' pruebas', '')}, fallan {len(v['fallan'])}")
        else:
            partes.append(f"{CORTO[b]}: abortada ({(v['traza'] or ['sin traza'])[-1][:60]}…)")
    return "; ".join(partes)


EQUIV = {"m18_round_negativo"}
h2, h1 = leer("mut"), leer("mut_hito1")
if "m25_html_sin_ocultos" in h2:  # la mutación solo anuló el atributo «hidden» (precedencia de «and»): se describe lo que hizo de verdad
    h2["m25_html_sin_ocultos"]["descripcion"] = "U5: el atributo `hidden` deja de ocultar el elemento (display:none, visibility:hidden y aria-hidden siguen ocultando)"
falta = [n for n in os.listdir(os.path.join(F, "mut")) if n not in h2]
filas = ["| Mutación | Qué se quita o altera | Resultado | Baterías |", "|---|---|---|---|"]
for n, r in h2.items():
    if n == "m00_control":
        continue
    res = "detectada" if detectada(r) else ("equivalente (no cuenta): «-9» no es un literal, es un menos aplicado a 9, y `_validar_formula` lo rechaza antes de mirar el rango" if n in EQUIV else "**NO detectada**")
    filas.append(f"| `{n.split('_')[0]}` | {r['descripcion']} | {res} | {celda(r)} |")
n_det = sum(detectada(r) for n, r in h2.items() if n != "m00_control")
n_tot = len(h2) - 1 - sum(1 for n in h2 if n in EQUIV and not detectada(h2[n]))
tabla = "\n".join(filas) + f"\n\n**[Hecho]** {n_det} de {n_tot} mutaciones detectadas; {n_tot - n_det} no detectadas (aparte, una mutación equivalente)."
if h1:
    tabla += "\n\nLas mismas mutaciones del párrafo de aptitud de la V6.4 sobre el **código y las pruebas del hito 1** (`fable/mut_hito1/`):\n\n| Mutación | Resultado | Baterías |\n|---|---|---|\n"
    tabla += "\n".join(f"| `{n.split('_')[0]}` | {'detectada' if detectada(r) else '**NO detectada**'} | {celda(r)} |" for n, r in h1.items())
no_det = [f"`{n.split('_')[0]}` ({r['descripcion'].split(': ', 1)[-1]})" for n, r in h2.items() if n != "m00_control" and not detectada(r) and n.split("_")[0] not in ("m37", "m39", "m40") and n not in EQUIV]
m3940 = "; ".join(f"`{n.split('_')[0]}` {'detectada' if detectada(r) else 'NO detectada'} ({celda(r)})" for n, r in h1.items()) or "(sin resultado)"
r37 = h2.get("m37_i20_dinero_real_si")
m37 = ("**no detectada** (" + celda(r37) + "). Ninguna prueba comprueba la frase de la línea nueva con un registro apto" if r37 and not detectada(r37) else ("detectada (" + celda(r37) + ")" if r37 else "(sin resultado)"))
s = open(INF, encoding="utf-8").read()
s = s.replace("<<TABLA_MUTACIONES>>", tabla).replace("<<NO_DETECTADAS>>", "; ".join(no_det) or "ninguna").replace("<<M39_M40_HITO1>>", m3940).replace("<<M37>>", m37)
if len(sys.argv) > 1 and sys.argv[1] == "--escribir":
    open(INF, "w", encoding="utf-8").write(s)
print("mutaciones con resultado:", n_tot, "· detectadas:", n_det, "· sin resultado todavía:", falta)
print("no detectadas:", [n for n, r in h2.items() if n != "m00_control" and not detectada(r) and n not in EQUIV])
print("hito 1:", m3940)
print("marcadores que quedan:", re.findall(r"<<[A-Z0-9_]+>>", s))
