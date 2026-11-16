#!/usr/bin/env python3
"""Rellena en REVISION_FABLE_HITO2_SEXTA.md lo que depende de resultados que tardan (tabla de mutaciones, baterías de las propuestas e
integridad del árbol congelado), leyéndolo de los archivos de resultados; falla si algo no cuadra con lo que el informe afirma.
Uso: python3 -I -B finalizar_informe6.py"""
import json, os, re, subprocess, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
F = os.path.dirname(AQUI)
sys.path.insert(0, AQUI)
import mutantes6 as MU  # noqa: E402
INF = os.path.join(F, "REVISION_FABLE_HITO2_SEXTA.md")
s = open(INF, encoding="utf-8").read()
NOM = {"test_verificacion_entradas_415.py": "entradas 4.15", "test_entrada_efectiva_415.py": "entrada efectiva", "test_verificacion_entradas_414.py": "entradas 4.14"}


def leer(dir_mut, k):
    p = os.path.join(F, dir_mut, k, "resultado.json")
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else None


def fila(r):
    bats, detect = [], False
    for b, x in r["baterias"].items():
        falla = x["codigo"] != 0 or bool(x["fallan"])
        detect = detect or falla
        bats.append(f"{NOM[b]}: {x['pasan'].replace(' pruebas', '') if x['pasan'] else 'sin recuento'}" + (f", fallan {len(x['fallan'])} («{re.sub(r'^.[A-Za-z0-9]+. FALLA +', '', x['fallan'][0])[:95]}…»)" if x["fallan"] else ""))
    return detect, "; ".join(bats)


# ---------------------------------------------------------------- unidad (e5)
e5 = open(os.path.join(F, "salidas", "e5_pruebas_nuevas_unidad.log"), encoding="utf-8").read()
unidad = {}
for m in re.finditer(r"(?m)^   (\S+)\s+\S+\s+(DETECTADA por|NO detectada por)", e5):
    unidad[m.group(1)] = m.group(2).startswith("DETECTADA")
for k in ("t6a_sin_distancia_de_edicion", "t6b_distancia_1", "t6c_distancia_2"):
    unidad[k] = bool(re.search(r"(?m)^   " + k + r"\s+SIN error", e5))
# ---------------------------------------------------------------- batería entera
filas, n_ej, det, nodet, codigos, incoh = [], 0, [], [], set(), []
for k, v in MU.M.items():
    r = leer("mut6", k)
    if r is None:
        filas.append(f"| `{k}` | {v[1]} | {v[2]} | {'detectada' if unidad.get(k) else '**NO detectada**'} (solo a nivel de unidad, `e5`) | no ejecutada con la batería entera |")
        (det if unidad.get(k) else nodet).append(k)
        continue
    assert "error" not in r, r
    d, bats = fila(r)
    for x in r["baterias"].values():
        codigos.add(x["codigo"])
    n_ej += 1
    if v[0] == "control":
        assert not d, "el control no pasa entero"
        filas.append(f"| `{k}` | {v[1]} | {v[2]} | pasa entera | {bats} |")
        continue
    (det if d else nodet).append(k)
    if k in unidad and unidad[k] != d:
        incoh.append(k)
    filas.append(f"| `{k}` | {v[1]} | {v[2]} | {'detectada' if d else '**NO detectada**'} | {bats} |")
assert not incoh, ("unidad y batería no coinciden", incoh)
assert codigos <= {0, 1}, codigos
total = len(MU.M) - 1
sin_bateria = [k for k in MU.M if leer("mut6", k) is None]
mut = (f"**[Hecho]** {len(MU.M)} definiciones (el control y {total} mutaciones). Con la batería entera se han ejecutado {n_ej} (el control y {n_ej - 1} mutaciones); todas terminan con código 0 o 1, "
       f"cada detección lleva su línea FALLA y, en todas, el resultado coincide con el de la evaluación a nivel de unidad. El control sin cambio de regla pasa entero (61/61, 33/33 y 190/190). "
       + (f"Las otras {len(sin_bateria)} (" + ", ".join(f"`{k.split('_')[0]}`" for k in sin_bateria) + ") solo se han evaluado a nivel de unidad: las detecta la misma prueba «(V1, V4)» o «(Q3, V4)» que detecta a sus vecinas con la batería entera.\n\n" if sin_bateria else "\n\n")
       + f"- **De las {total} mutaciones, {len(det)} se detectan y {len(nodet)} no.** Sin detectar: " + ", ".join(f"`{k.split('_')[0]}`" for k in nodet) + ".\n"
       + "- **Lo corregido en esta candidata (17: V1, V2, V3, V5 y V7, una pieza cada vez):** " + f"{sum(1 for k in det if MU.M[k][0] == 'v')} detectadas y {sum(1 for k in nodet if MU.M[k][0] == 'v')} no. "
       + "V1, 6 de 6; V2, 0 de 3; V3 y V7, 2 de 6; V5, 1 de 2.\n"
       + "- **Las que la quinta comprobación dejó sin detectar y sus vecinas (9: Q1, Q3, T6 y T8):** " + f"{sum(1 for k in det if MU.M[k][0] == 'v4')} detectadas y {sum(1 for k in nodet if MU.M[k][0] == 'v4')} no (`t6c`, que es nueva, y `t8d`, para la que el autor no declara prueba).\n\n"
       + "| Mutación | Hallazgo | Qué se quita o altera | Resultado | Baterías |\n|---|---|---|---|---|\n" + "\n".join(filas))
assert sum(1 for k in det if MU.M[k][0] == 'v') + sum(1 for k in nodet if MU.M[k][0] == 'v') == 17
esperado_nodet = {"v2a", "v2b", "v2c", "v3b", "v7a", "v7c", "v7d", "v5a", "t6c", "t8d"}
assert {k.split("_")[0] for k in nodet} == esperado_nodet, sorted(nodet)
assert {k.split("_")[0] for k in det if MU.M[k][1] == "V1"} == {"v1a", "v1b", "v1c", "v1d", "v1e", "v1f"}
# ---------------------------------------------------------------- propuestas
def bat(nombre):
    t = open(os.path.join(F, "salidas", "propuestas6", nombre), encoding="utf-8").read()
    m = re.search(r"(?m)^(\d+)/(\d+) pruebas", t)
    rc = re.search(r"### rc=(\d+)", t).group(1)
    assert m and m.group(1) == m.group(2) and rc == "0" and not re.search(r"(?m)^\[[A-Za-z0-9]+\] FALLA", t), nombre
    return f"{m.group(1)}/{m.group(2)}"


t_ee, t_415 = bat("prop6t_bateria_entrada_efectiva_415.log"), bat("prop6t_bateria_entradas_415.log")
c_ee, c_414, c_415 = bat("prop6_bateria_test_entrada_efectiva_415.log"), bat("prop6_bateria_test_verificacion_entradas_414.log"), bat("prop6_bateria_test_verificacion_entradas_415.log")
assert (t_ee, t_415, c_ee, c_414, c_415) == ("61/61", "190/190", "61/61", "33/33", "190/190")
CONG = os.path.join(os.path.dirname(F), "munger_v2_r1", "personaje_v2", "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_15", "hito2", "resultados")
for a, b in (("prop6_diagnostico_finales.json", "diagnostico_registros_4_14_con_reglas_hito2.json"), ("prop6_inventario_signo.json", "inventario_signo_registros_reales.json")):
    assert open(os.path.join(F, "salidas", "propuestas6", a), "rb").read() == open(os.path.join(CONG, b), "rb").read(), a
q12 = open(os.path.join(F, "salidas", "propuestas6", "prop6_q12_pdf_parteB.log"), encoding="utf-8").read()
assert "pasan citando el .txt: 244; pasan citando el PDF + archivo_texto: 244; rechazadas SOLO por el control del PDF: 0" in q12 and "pasan citando el .txt: 225; pasan citando el PDF + archivo_texto: 225; rechazadas SOLO por el control del PDF: 0" in q12
mp = {}
for k in ("v2c_los_dos_con_dolar", "v5a_sin_corte", "v7c_lectura_sin_apostrofo_detras", "t8d_fecha_cualquier_cifra", "t6c_distancia_2", "v7d_real_solo_plural"):
    r = leer("mut6p", k)
    assert r is not None and "error" not in r, k
    d, bats = fila(r)
    assert d, ("la mutación no se detecta con las pruebas propuestas", k)
    mp[k] = bats
prop = (f"- **[Hecho] Solo las pruebas (`prop6t`), con el código de la candidata sin tocar:** entradas 4.15 {t_415} y entrada efectiva {t_ee}, código 0, ninguna línea FALLA; el número de pruebas no cambia.\n"
        "- **[Hecho] Las mutaciones que hoy sobreviven, repetidas con la batería entera sobre `prop6t`** (`mutaciones6p.py`, resultados en `mut6p/`): las seis ejecutadas se detectan. "
        + "; ".join(f"`{k.split('_')[0]}` ({v})" for k, v in mp.items()) + ". Las demás (`v2a`, `v2b`, `v3b`, `v7a`), a nivel de unidad (`e9` A): detectadas.\n"
        f"- **[Hecho] Pruebas y código (`prop6`):** entrada efectiva {c_ee}, entradas 4.14 {c_414} y entradas 4.15 {c_415}, código 0. Registros reales con ese código: el diagnóstico de los tres registros finales y el inventario de signo, "
        "idénticos byte a byte a los entregados; `q12_pdf` B, 244 y 225, 0 rechazadas. A nivel de unidad (`e9` B y C): el apóstrofo tipográfico entre cifras deja de aceptar el trozo, los dos casos de W4 vuelven a «ok» y a «signo_distinto», "
        "el mensaje dice «más de 200 veces», toda diferencia con la candidata está en una página con un apóstrofo entre cifras (120.000 citas aleatorias) y las 1.645 citas reales no cambian ni en el estado ni en el detalle.\n"
        "- No se han probado con la regresión completa ni con LibreOffice.")
# ---------------------------------------------------------------- integridad
ini, fin = os.path.join(F, "huellas_arbol_congelado_inicio.txt"), os.path.join(F, "huellas_arbol_congelado_fin.txt")
assert os.path.exists(fin), "falta el listado final de huellas"
import hashlib
h_ini, h_fin = hashlib.sha256(open(ini, "rb").read()).hexdigest(), hashlib.sha256(open(fin, "rb").read()).hexdigest()
assert h_ini == h_fin, "el árbol congelado ha cambiado"
n = sum(1 for _ in open(ini, encoding="utf-8", errors="replace"))
integ = open(os.path.join(F, "salidas", "integridad_final.txt"), encoding="utf-8").read()
assert "INTEGRIDAD CONFORME" in integ, "la comprobación final de integridad no es conforme"
horas = re.search(r"inicio: (.+)\nfin: (.+)\n", integ)
integridad = (f"- **[Hecho]** Listado de huellas SHA-256 de los {n} archivos del árbol congelado al empezar ({horas.group(1)}; `fable/huellas_arbol_congelado_inicio.txt`) y al terminar ({horas.group(2)}; "
              f"`fable/huellas_arbol_congelado_fin.txt`): idénticos (SHA-256 de los listados: `{h_ini[:8]}…{h_ini[-8:]}`). Ningún archivo ni carpeta del árbol tiene fecha posterior al inicio de la comprobación, y el manifiesto sigue conforme al terminar (7486 «OK»).\n"
              "- **[Hecho]** La copia ligera (`fable/copia/`) tiene al terminar sus `scripts/`, `pruebas/` y `esquema/` idénticos a los del árbol congelado (`diff -rq`) y sin `__pycache__`: todas las sondas se ejecutaron contra el código congelado tal cual. "
              "Huellas de los otros códigos (primeros y últimos 8 caracteres de `verificacion_entradas.py`): `prev/` (876bfc2) `dfe76013…7b40215a`, la que anotó la quinta comprobación; `c7a/` (7a6583b) `7e5acd82…d44a422d`; `f3d/` (f3d15e8) `c52017d6…d5ed0de0`; "
              "`estable92/` (92b2362) `99de635e…404ae6aa`; `prop5/` `54bcb09a…12fda342`; " + re.search(r"(`prop6t/`.*)", integ).group(1) + "\n"
              "- **[Hecho]** `/home/user/munger-v2` solo se ha leído (`git diff`, `git archive`, `git show`, `git log`, `git status`, `git rev-parse`). " + re.search(r"(Al terminar, .*)", integ).group(1) + "\n"
              "- **[Hecho]** `fable/salidas/INTENTOS_SOFFICE.log` no existe: ninguna sonda ni batería intentó lanzar LibreOffice.\n"
              "- **[Hecho]** Huellas de referencia de lo revisado (primeros y últimos 8 caracteres): `verificacion_entradas.py` `96c2572c…c0fa9d8d`; `test_verificacion_entradas_415.py` `95b29454…ccc7be1b`; `test_entrada_efectiva_415.py` `6888f7e6…2221a0aa`; "
              "`verificar_paquete.sh` `8158d256…4160beb3`; `ficha.py` `c3ba3d86…ae65f7af`, `pipeline.py` `3999a95a…1e1459ef`, `informe.py` `eabe0546…c083a43d`, `cierre_v2.py` `6d89a81a…b379c813`, `fase1_historia.py` `b74494db…f67e90b2`, "
              "`ficha.esquema.json` `eefed485…b81cc165`, `test_verificacion_entradas_414.py` `e14147d0…ca07724f`, `test_relevo_i19_415.py` `663a9225…8b58dea4` y `test_cierre_v2.py` `970cc094…8f389c87` (los nueve, sin cambio desde 876bfc2); "
              "`MANIFIESTO_SHA256.txt` `d9030060…cc8f2599`; `CAMBIOS_ARCHIVOS.txt` `85dc966b…ba7a4872` (36 modificados y 6809 nuevos, todas las huellas iguales a las del manifiesto); `DIFF_QUINTA_A_SEXTA.diff` `59a04889…b8f0e26b`.")
for marca, texto in (("<<MUTACIONES>>", mut), ("<<PROPUESTAS>>", prop), ("<<INTEGRIDAD>>", integridad)):
    assert s.count(marca) == 1, marca
    s = s.replace(marca, texto)
linea = "**ESTADO DEL INFORME: EN CURSO (faltan por cerrar la tabla de mutaciones de §5, las baterías de las propuestas de §3 y §8; lo demás está comprobado).**\n\n"
assert s.count(linea) == 1
s = s.replace(linea, "")
assert "<<" not in s
open(INF, "w", encoding="utf-8").write(s)
print(f"informe finalizado: {len(s.splitlines())} líneas · mutaciones detectadas {len(det)}, no detectadas {len(nodet)}, con la batería entera {n_ej}")
