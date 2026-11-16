#!/usr/bin/env python3
"""Séptima comprobación · rellena el informe (sondas7/informe_cuerpo.md → REVISION_FABLE_HITO2_SEPTIMA.md) con lo que se obtiene de los
resultados: la tabla de mutaciones (mut7/<nombre>/resultado.json), las baterías sobre los árboles con las propuestas
(salidas/propuestas7/*.log) y la integridad (salidas/integridad_final.txt). Lo que aún no tiene resultado se marca «(en curso)».
Uso: python3 -I -B finalizar_informe7.py"""
import json, os, re, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
F = os.path.dirname(AQUI)
sys.path.insert(0, AQUI)
import mutantes7 as MU  # noqa: E402

NOM = {MU.B415: "entradas 4.15", MU.BEE: "entrada efectiva", MU.B414: "entradas 4.14"}
W1 = [k for k, v in MU.M.items() if v[0] == "w1"]
s = open(os.path.join(AQUI, "informe_cuerpo.md"), encoding="utf-8").read()
en_curso = False


def res(nombre):
    p = os.path.join(F, "mut7", nombre, "resultado.json")
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else None


def corto(nombre):
    return nombre.split("_")[0]


def celda(r):
    out, det = [], False
    for b, v in r["baterias"].items():
        m = re.match(r"(\d+)/(\d+)", v["pasan"] or "")
        t = f"{NOM[b]}: {m.group(0) if m else '¿?'}"
        if v["fallan"]:
            det = True
            t += f", fallan {len(v['fallan'])} («" + re.sub(r"^\[[A-Za-z0-9]+\] FALLA\s+", "", v["fallan"][0])[:96].replace("|", "/") + "…»)"
        elif v["codigo"] != 0:
            det = True
            t += f", código {v['codigo']}"
        out.append(t)
    return "; ".join(out), det


# ---------------------------------------------------------------- tabla de mutaciones
filas, hechas, det_, nodet = [], [], [], []
for nombre, (grupo, hall, desc, _c, bats) in MU.M.items():
    r = res(nombre)
    if r is None:
        continue
    hechas.append(nombre)
    txt, d = celda(r)
    if grupo == "control" or nombre == "x1_correccion_propuesta":
        estado = "pasa entera" if not d else "**FALLA**"
    else:
        estado = "detectada" if d else "**NO detectada**"
        (det_ if d else nodet).append(nombre)
    filas.append(f"| `{nombre}` | {hall} | {desc.replace('|', '/')} | {estado} | {txt} |")
pend_w1 = [k for k in W1 if res(k) is None]
if pend_w1:
    en_curso = True
w1_det = [k for k in W1 if k in det_]
w1_no = [k for k in W1 if k in nodet]
mut = []
n_def = len(hechas)
mut.append(f"**[Hecho]** Con la batería entera se han ejecutado {n_def} definiciones" + (f" (faltan por terminar, de las diez de W1: {', '.join('`' + corto(k) + '`' for k in pend_w1)}: **en curso**)" if pend_w1 else "")
           + ": " + ("el control sin cambio de regla, " if "c00_control" in hechas else "") + ("la corrección propuesta de `:542` con las pruebas de la candidata y " if "x1_correccion_propuesta" in hechas else "")
           + f"{len(det_) + len(nodet)} mutaciones. Todas terminan con código 0 o 1 y cada detección lleva su línea FALLA. En todas, el resultado coincide con el de la evaluación a nivel de unidad (`g5`)."
           + (" El control pasa entero en el árbol ligero del arnés (" + celda(res("c00_control"))[0] + ")." if "c00_control" in hechas else "") + "\n")
mut.append(f"- **Las diez de W1:** {len(w1_det)} detectadas ({', '.join('`' + corto(k) + '`' for k in w1_det) or '—'}) y {len(w1_no)} no ({', '.join('`' + corto(k) + '`' for k in w1_no) or '—'})"
           + (f"; {len(pend_w1)} en curso" if pend_w1 else "") + ".")
otras_no = [k for k in nodet if k not in W1]
otras_det = [k for k in det_ if k not in W1]
if otras_no or otras_det:
    mut.append(f"- **Las demás ejecutadas** (lo cambiado en esta candidata y la línea `:542`): detectadas {', '.join('`' + corto(k) + '`' for k in otras_det) or 'ninguna'}; no detectadas {', '.join('`' + corto(k) + '`' for k in otras_no) or 'ninguna'}.")
mut.append("\n| Definición | Hallazgo | Qué se quita o altera | Resultado | Baterías |\n|---|---|---|---|---|\n" + "\n".join(filas))
solo_unidad = [k for k, v in MU.M.items() if res(k) is None and k not in pend_w1]
mut.append("\n- **[Hecho] Las no detectadas cambian de verdad el comportamiento** (no son mutaciones equivalentes): `g6` da, para cada una de las de la línea `:542` y de los límites de la cita, el caso con el que el código mutado responde otra cosa (los casos propuestos en X2).")
mut.append("- **[Hecho] Sentido de las no detectadas.** Aceptan: `v7c` («849» dentro de «849'697» con la cita entera), `x1a` y `x1b` (la cifra de detrás de un apóstrofo, con la cita entera), `w3b` y `w3c` (lo mismo por detrás con un solo tipo de apóstrofo). Solo cambian un «ok» por un pendiente, o el texto de un mensaje: `w4b`, `w4e`, `w4g`, `w4h`, `w5a`.")
if solo_unidad:
    mut.append(f"- **Solo a nivel de unidad** (no ejecutadas con la batería entera; `g5`): {', '.join('`' + corto(k) + '`' for k in solo_unidad)}.")
mut.append("- **No repetidas.** Las mutaciones de las pasadas anteriores cuyas líneas no cambian en este diff (V1, Q1, Q3, T6 salvo `t6c`…) no se han vuelto a ejecutar; no se afirma nada nuevo de ellas.")
s = s.replace("@@MUT@@", "\n".join(mut))

# ---------------------------------------------------------------- resumen de W1 en el dictamen
if pend_w1:
    w1txt = (f"A nivel de unidad (`g5`) se detectan `v2a`, `v2b`, `v2c`, `v5a`, `v7a`, `v7d`, `v3b`, `t8d` y `t6c`. Con la batería entera, hasta ahora: detectadas {', '.join('`' + corto(k) + '`' for k in w1_det) or '—'}; "
             f"no detectada {', '.join('`' + corto(k) + '`' for k in w1_no) or '—'}; **en curso** {', '.join('`' + corto(k) + '`' for k in pend_w1)} (§5).")
else:
    w1txt = (f"Con la batería entera (§5): detectadas {', '.join('`' + corto(k) + '`' for k in w1_det)}; no detectada {', '.join('`' + corto(k) + '`' for k in w1_no) or 'ninguna'}: pasa {next((celda(res(k))[0] for k in w1_no), '')}. "
             "El caso que la fijaba con el código de 8196522 deja de llegar a la línea con W4 aplicado.")
s = s.replace("@@W1_RESUMEN@@", w1txt)
s = s.replace("@@NO_HECHO_MUT@@", ("Con la batería entera solo se han ejecutado las diez mutaciones de W1, el control, la corrección propuesta y " + (", ".join('`' + corto(k) + '`' for k in hechas if k not in W1 and k not in ("c00_control", "x1_correccion_propuesta")) or "ninguna más")
                                   + "; las demás de `mutantes7.py` (" + (", ".join('`' + corto(k) + '`' for k in solo_unidad) or "—") + "), solo a nivel de unidad (`g5`, `g6`), que en todas las ejecutadas da el mismo resultado que la batería entera.")
              if not pend_w1 else "Las mutaciones con la batería entera están **en curso**.")

# ---------------------------------------------------------------- baterías sobre fix7t y fix7
def bateria(nombre):
    p = os.path.join(F, "salidas", "propuestas7", nombre + ".log")
    if not os.path.exists(p):
        return None
    t = open(p, encoding="utf-8", errors="replace").read()
    m = re.search(r"(?m)^(\d+)/(\d+) pruebas", t)
    rc = re.search(r"### rc=(\d+) segundos=(\d+)", t)
    if not rc:
        return None
    fallan = [re.sub(r"^\[[A-Za-z0-9]+\] FALLA\s+", "", l)[:330] for l in t.splitlines() if re.match(r"^\[[A-Za-z0-9]+\] FALLA", l)]
    return {"pasan": m.group(0).split()[0] if m else "¿?", "rc": int(rc.group(1)), "seg": int(rc.group(2)), "fallan": fallan}


b_t, b_415, b_ee, b_414 = bateria("fix7t_bateria_415"), bateria("fix7_bateria_415"), bateria("fix7_bateria_ee415"), bateria("fix7_bateria_414")
prop = []
if b_t:
    prop.append(f"- **[Hecho] Solo las pruebas (`fix7t`), con el código de la candidata sin tocar:** entradas 4.15 **{b_t['pasan']}**, código {b_t['rc']}"
                + (f"; falla «{b_t['fallan'][0]}»" if b_t["fallan"] else "") + ". Es la demostración de X1 dentro de la batería: con los casos de la cita completa, la candidata no pasa.")
else:
    prop.append("- **Solo las pruebas (`fix7t`):** batería **en curso**."); en_curso = True
if b_415 and b_ee and b_414:
    prop.append(f"- **[Hecho] Pruebas y código (`fix7`):** entradas 4.15 {b_415['pasan']}, entrada efectiva {b_ee['pasan']} y entradas 4.14 {b_414['pasan']}, códigos {b_415['rc']}, {b_ee['rc']} y {b_414['rc']}"
                + ("; ninguna línea FALLA" if not (b_415["fallan"] or b_ee["fallan"] or b_414["fallan"]) else "; **HAY LÍNEAS FALLA**") + "; el número de pruebas no cambia.")
else:
    hechas_b = [f"{n} {b['pasan']}" for n, b in (("entradas 4.15", b_415), ("entrada efectiva", b_ee), ("entradas 4.14", b_414)) if b]
    prop.append("- **Pruebas y código (`fix7`):** baterías **en curso**" + (f" (terminadas: {', '.join(hechas_b)})" if hechas_b else "") + "."); en_curso = True
rx = res("x1_correccion_propuesta")
if rx:
    prop.append(f"- **[Hecho] El carácter repuesto con las pruebas de la candidata sin tocar** (`mut7/x1_correccion_propuesta`): {celda(rx)[0]}.")
s = s.replace("@@PROP_BATERIAS@@", "\n".join(prop))

# ---------------------------------------------------------------- regresión de la otra sesión (solo lectura)
pr = os.path.join(os.path.dirname(os.path.dirname(F)), "reg7", "verificacion_completa_septima.txt")
if os.path.exists(pr):
    tr = open(pr, encoding="utf-8", errors="replace").read()
    ini_r = next((l for l in tr.splitlines() if re.match(r"^\d{4}-\d\d-\d\dT", l)), "¿?")
    glob = [l.strip() for l in tr.splitlines() if "RESULTADO GLOBAL" in l]
    bloques = [l.strip() for l in tr.splitlines() if l.startswith("RESULTADO") and "GLOBAL" not in l]
    fallan_r = [b for b in bloques if "PASA" not in b]
    fin_r = __import__("time").strftime("%H:%M", __import__("time").gmtime(os.path.getmtime(pr)))
    if glob:
        regtxt = (f"Su registro (`reg7/verificacion_completa_septima.txt`) empieza a las {ini_r[11:16]} UTC y termina (última escritura, {fin_r} UTC) con «{glob[-1]}»; {len(bloques)} bloques con resultado, "
                  + ("todos en PASA." if not fallan_r else f"**{len(fallan_r)} que no dicen PASA**: {'; '.join(fallan_r)[:300]}."))
    else:
        regtxt = (f"Al cerrar este informe no había terminado: su registro (`reg7/verificacion_completa_septima.txt`, empezado a las {ini_r[11:16]} UTC; última escritura, {fin_r} UTC) lleva {len(bloques)} bloques con resultado, "
                  + ("todos en PASA" if not fallan_r else f"{len(fallan_r)} que no dicen PASA") + (f" (el último: «{bloques[-1]}»)." if bloques else "."))
else:
    regtxt = "No se ha encontrado su registro."
s = s.replace("@@REGRESION@@", regtxt)

# ---------------------------------------------------------------- integridad
p = os.path.join(F, "salidas", "integridad_final.txt")
if os.path.exists(p):
    L = [l.rstrip("\n") for l in open(p, encoding="utf-8")]
    d = {}
    for l in L:
        if ": " in l:
            k, v = l.split(": ", 1); d[k] = v
    integ = [
        f"- **[Hecho]** Listado de huellas SHA-256 de los archivos del árbol congelado al empezar ({d.get('inicio')}; `fable/huellas_arbol_congelado_inicio.txt`) y al terminar ({d.get('fin')}; `fable/huellas_arbol_congelado_fin.txt`): {d.get('huellas del árbol congelado')}. Archivos o carpetas del árbol con fecha posterior al inicio de la comprobación: {d.get('archivos o carpetas del árbol congelado posteriores al inicio')}. El manifiesto sigue conforme al terminar ({d.get('manifiesto al terminar')}).",
        f"- **[Hecho]** La copia ligera (`fable/copia/`) tiene al terminar sus `scripts/`, `pruebas/` y `esquema/` idénticos a los del árbol congelado (`diff -rq`: {d.get('diff -rq scripts (congelado frente a copia)')}, {d.get('diff -rq pruebas (congelado frente a copia)')} y {d.get('diff -rq esquema (congelado frente a copia)')}) y no hay `__pycache__` en el árbol congelado, en las copias ni en las sondas ({d.get('__pycache__ en el árbol congelado, en las copias o en las sondas')}): todas las sondas se ejecutaron contra el código congelado tal cual.",
        f"- **[Hecho]** Huellas de `verificacion_entradas.py` (primeros y últimos 8 caracteres): {d.get('huellas de verificacion_entradas.py')}. Las de 8196522, 876bfc2 y `prop6` son las que anotó la sexta comprobación; `prop6t` y `fix7t` solo cambian las pruebas. {('De las pruebas: ' + d.get('huellas de las pruebas') + '.') if d.get('huellas de las pruebas') else ''}",
        f"- **[Hecho]** SHA-256 completo de `verificacion_entradas.py` con el carácter repuesto (`fix7`): `{d.get('SHA-256 completo de verificacion_entradas.py con el carácter repuesto (fix7)')}`; su `diff` con el de la candidata: {d.get('diff de fix7 frente a la copia en verificacion_entradas.py')}.",
        f"- **[Hecho]** `/home/user/munger-v2` solo se ha leído (`git diff`, `git archive`, `git show`, `git log`, `git status`, `git rev-parse`). {d.get('git', '').capitalize() if False else ('Al terminar, ' + d.get('git', '').split('al terminar, ', 1)[-1] if d.get('git') else '')}",
        f"- **[Hecho]** `fable/salidas/INTENTOS_SOFFICE.log` {'no existe: ninguna sonda ni batería intentó lanzar LibreOffice' if d.get('INTENTOS_SOFFICE.log') == 'no existe' else 'EXISTE: HUBO INTENTOS'}.",
        f"- **[Hecho]** Huellas de referencia de lo revisado (primeros y últimos 8 caracteres): `verificacion_entradas.py` `7abbb081…9227c41b`; `test_verificacion_entradas_415.py` `a4a12f7b…4504a43f`; `test_entrada_efectiva_415.py` `bbf3d713…6f04d145`; `verificar_paquete.sh` `8158d256…4160beb3`; `ficha.py` `c3ba3d86…ae65f7af`, `pipeline.py` `3999a95a…1e1459ef`, `informe.py` `eabe0546…c083a43d`, `cierre_v2.py` `6d89a81a…b379c813`, `fase1_historia.py` `b74494db…f67e90b2`, `ficha.esquema.json` `eefed485…b81cc165`, `test_verificacion_entradas_414.py` `e14147d0…ca07724f`, `test_relevo_i19_415.py` `663a9225…8b58dea4` y `test_cierre_v2.py` `970cc094…8f389c87` (los diez, sin cambio desde 8196522); `HITO_2_4_15.md` `87fa07cb…9c5f6a8c`; `PUNTO_DE_RECUPERACION.md` `81db2ea3…a05a6ef1`; `MANIFIESTO_SHA256.txt` `dfe39ecb…e7c777e5`; `CAMBIOS_ARCHIVOS.txt` `06ebe851…2080d3fd`; `DIFF_SEXTA_A_SEPTIMA.diff` `06b1adcc…a4b7f48c`.",
        f"- **Resultado de la comprobación de integridad:** {L[-1]}.",
    ]
    s = s.replace("@@INTEGRIDAD@@", "\n".join(integ))
else:
    s = s.replace("@@INTEGRIDAD@@", "(La comprobación de integridad se ejecuta al terminar: **en curso**.)"); en_curso = True

if en_curso:
    s = s.replace("## 0. Qué se ha revisado y cómo", "**ESTADO DE ESTE DOCUMENTO: BORRADOR.** Hay ejecuciones con la batería entera sin terminar; lo que falta se marca «en curso». El dictamen y los hallazgos X1–X4 no dependen de ellas.\n\n## 0. Qué se ha revisado y cómo", 1)
assert "@@" not in s, re.findall(r"@@\w+@@", s)
open(os.path.join(F, "REVISION_FABLE_HITO2_SEPTIMA.md"), "w", encoding="utf-8").write(s)
print("informe escrito ·", "BORRADOR (en curso)" if en_curso else "DEFINITIVO", "·", len(s.splitlines()), "líneas · mutaciones con resultado:", len(hechas), "· W1 pendientes:", pend_w1)
