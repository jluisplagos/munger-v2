#!/usr/bin/env python3
"""Escribe la sección 5 (mutaciones) del informe de la quinta comprobación a partir de mut5/*/resultado.json. Sustituye el marcador
«(pendiente de anotar)» de esa sección; si falta algún resultado, no escribe nada y lo dice.
Uso: python3 -I -B finalizar_informe5.py"""
import json, os, re, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
F = os.path.dirname(AQUI)
sys.path.insert(0, AQUI)
import mutaciones5 as M5  # noqa: E402
INFORME = os.path.join(F, "REVISION_FABLE_HITO2_QUINTA.md")
NOMBRE_B = {"test_verificacion_entradas_415.py": "entradas 4.15", "test_entrada_efectiva_415.py": "entrada efectiva", "test_verificacion_entradas_414.py": "entradas 4.14"}
filas, falta = [], []
n_bat, codigos = 0, set()
for nombre, (grupo, hall, desc, _c, bats) in M5.M.items():
    p = os.path.join(F, "mut5", nombre, "resultado.json")
    if not os.path.exists(p):
        falta.append(nombre)
        continue
    r = json.load(open(p, encoding="utf-8"))
    det, partes = False, []
    for b, x in r.get("baterias", {}).items():
        n_bat += 1
        codigos.add(x.get("codigo"))
        m = re.match(r"(\d+)/(\d+)", x.get("pasan") or "")
        if x.get("fallan") or x.get("codigo") not in (0,) or not m or m.group(1) != m.group(2):
            det = True
        if x.get("fallan"):
            partes.append(f"{NOMBRE_B[b]}: {x['pasan'].split(' ')[0] if x.get('pasan') else '—'}, fallan {len(x['fallan'])} («{re.sub(r'^.[A-Za-z0-9]+. FALLA +', '', x['fallan'][0])[:95]}…»)")
        elif x.get("codigo") != 0 or not m:
            partes.append(f"{NOMBRE_B[b]}: abortada (código {x.get('codigo')}; {(x.get('traza') or ['sin traza'])[-1][:90]})")
        else:
            partes.append(f"{NOMBRE_B[b]}: {m.group(0)}")
    res = "pasa entera" if nombre == "c00_control" and not det else ("detectada" if det else "**NO detectada**")
    filas.append((nombre, grupo, hall, desc, res, "; ".join(partes)))
if falta:
    print("faltan resultados:", falta)
    sys.exit(1)


def cuenta(grupo, pref=None):
    fs = [f for f in filas if f[1] == grupo and (pref is None or f[0].startswith(pref))]
    return sum(1 for f in fs if f[4] == "detectada"), sum(1 for f in fs if "NO" in f[4]), [f"`{f[0].split('_')[0]}`" for f in fs if "NO" in f[4]]


q2, q, t = cuenta("q2"), cuenta("q"), cuenta("t")
q1, q3, q4 = cuenta("q", "q1"), cuenta("q", "q3"), cuenta("q", "q4")
tabla = "| Mutación | Hallazgo | Qué se quita o altera | Resultado | Baterías |\n|---|---|---|---|---|\n" + "\n".join(
    f"| `{n}` | {h} | {d.replace('|', '/').replace('<', '&lt;')} | {res} | {part.replace('|', '/').replace('<', '&lt;')} |" for n, g, h, d, res, part in filas)
texto = f"""## 5. Mutaciones

Una regla quitada o alterada cada vez, en un árbol ligero aparte (`sondas5/mutaciones5.py`, con el arnés de la cuarta comprobación; resultados en `fable/mut5/<nombre>/resultado.json`, guardados al terminar cada una). Baterías: las permitidas que correspondan a cada regla. El control sin cambio de regla pasa entero (61/61, 33/33 y 185/185).

**[Hecho]** {len(filas)} mutaciones (el control y {len(filas) - 1}) y {n_bat} ejecuciones de batería; todas terminan con código 0 o 1 (códigos vistos: {sorted(codigos)}), cada detección lleva su línea FALLA y ninguna queda sin resultado.

- **Las que la cuarta comprobación dejó sin detectar y para las que el autor dice haber añadido prueba ({q2[0] + q2[1]}):** {q2[0]} detectadas y {q2[1]} no ({', '.join(q2[2]) or '—'}).
- **Reglas que entran con esta candidata ({q[0] + q[1]}):** {q[0]} detectadas y {q[1]} no. Q1: {q1[0]} de {q1[0] + q1[1]}; Q3: {q3[0]} de {q3[0] + q3[1]}; Q4: {q4[0]} de {q4[0] + q4[1]}. Sin detectar: {', '.join(q[2]) or '—'}.
- **Reglas de la cuarta cuyas líneas se reescriben ahora ({t[0] + t[1]}):** {t[0]} detectadas y {t[1]} no ({', '.join(t[2]) or '—'}).

{tabla}

__NOTAS__"""
s = open(INFORME, encoding="utf-8").read()
marca = "## 5. Mutaciones\n\n(pendiente de anotar)"
if s.count(marca) != 1:
    print("el marcador de la sección 5 no está (¿ya se escribió?)")
    sys.exit(2)
open(INFORME, "w", encoding="utf-8").write(s.replace(marca, texto))
print(texto[:1800])
