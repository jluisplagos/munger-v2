#!/usr/bin/env python3
"""Mutaciones de la normalización declarada del circulante (V-CIRC, 19-nov-2026) frente a las baterías sin LibreOffice: cada mutación (una línea del
producto cambiada a propósito en motor_a_f1.py, f1_libro_v631.py, entradas_economicas.py, seleccion_plantilla.py, cierre_v2.py o
volcar_datos_v63.py) tiene que hacer que deje de pasar alguna prueba que pasa sin ella (o que una batería se interrumpa).

Uso (desde cualquier carpeta): python3 -I mutaciones_circulante.py [SALIDA.txt]
Trabaja sobre copias temporales de personaje_v2 (scripts, esquema, prompts, configuraciones y las baterías): no toca el árbol. Las plantillas y su
carpeta v6/ se enlazan (solo se leen). Sin LibreOffice. Baterías: test_circulante_f1.py (la de este cambio), test_motor_a_f1.py y test_v631_f1.py
(las de F1 y de la V6.3.1, que no pueden cambiar). Se detecta por el recuento de pruebas que pasan (como mutaciones_margen_de_partida.py).
c34–c51 (revisión C1, 19-nov-2026): la demostración de la exclusión del circulante en C46 con el cálculo declarado del expediente.
"""
import os
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor

PV = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
RAIZ = os.path.dirname(PV)
SALIDA = sys.argv[1] if len(sys.argv) > 1 else None
BATERIAS = ("test_circulante_f1.py", "test_motor_a_f1.py", "test_v631_f1.py")
MF, LV, EE, SE, CI, VD = ("scripts/motor_a_f1.py", "scripts/f1_libro_v631.py", "scripts/entradas_economicas.py", "scripts/seleccion_plantilla.py",
                          "scripts/cierre_v2.py", "scripts/volcar_datos_v63.py")
M = [
    ("c01 · la capa no aplica la normalización declarada", MF, "        if circ_aplica and normalizar:\n            return _wc_normalizado(y, circ_anios)\n",
     "        if False:\n            return _wc_normalizado(y, circ_anios)\n"),
    ("c02 · un año que usa la reinversión y no está normalizado entra con la fila 14 (se mezclan las dos definiciones)", MF,
     "        return None if y in usados else w\n", "        return w\n"),
    ("c03 · la reinversión de f con la fila 14 tal cual", MF,
     '        reinv = media(H["capex"][y] - DX_de(p, y) + WC_de(y, con_ajuste, normalizar) for y in ventana)\n',
     '        reinv = media(H["capex"][y] - DX_de(p, y) + H["dwc"][y] for y in ventana)\n'),
    ("c04 · el ancla de S2C con la fila 14 tal cual (la normalización no entra en el ancla)", MF,
     '(WC_de(y, con_ajuste, normalizar) or Fr(0)) + (H["adq"][y] or Fr(0)) for y in horiz) - xv', '(H["dwc"][y] or Fr(0)) + (H["adq"][y] or Fr(0)) for y in horiz) - xv'),
    ("c05 · K3c mide la reinversión sin normalizar", MF, '        neg = decl_r["reinv"] < 0 and H["V"][ventana[-1]] >= H["V"][ventana[0]]\n',
     '        neg = (calcular(per, normalizar=False) or decl_r)["reinv"] < 0 and H["V"][ventana[-1]] >= H["V"][ventana[0]]\n'),
    ("c06 · el puente K3 sin la partida del circulante excluido", MF,
     '                elif (circ_aplica and normalizar) if con_ajuste else nl_activa:\n', "                elif False:\n"),
    ("c07 · F1-CIRC no exige los años H–L del ancla", MF, "        if falta_h:\n", "        if False:\n"),
    ("c08 · F1-CIRC no exige los años de la ventana", MF, "        if falta_w:\n", "        if False:\n"),
    ("c09 · F1-CIRC no comprueba que la caja base excluya el circulante", MF, "    elif media_w != 0 and not coinc:\n", "    elif False:\n"),
    ("c10 · la coherencia con la caja base con una tolerancia de 100 mm", MF, '    coinc = [e for e in partidas if media_w is not None and abs(Q(e["importe"]) - media_w) <= TOL_E7]\n',
     '    coinc = [e for e in partidas if media_w is not None and abs(Q(e["importe"]) - media_w) <= 100]\n'),
    ("c11 · la coherencia con cualquier componente (no solo C46)", MF, '                if isinstance(e, dict) and e.get("componente") == "C46" and Q(e.get("importe")) is not None',
     '                if isinstance(e, dict) and Q(e.get("importe")) is not None'),
    ("c12 · la normalización también con US GAAP", MF, '            "aplicable": not forma and norma == "NIIF", "norma": norma}', '            "aplicable": not forma, "norma": norma}'),
    ("c13 · claves desconocidas aceptadas en silencio", MF, "    desc = sorted(set(n) - CLAVES_CIRCULANTE)\n", "    desc = []\n"),
    ("c14 · un año repetido se acepta", MF, "            elif a in ok:\n", "            elif False:\n"),
    ("c15 · otra regla se acepta", MF, "    elif regla != REGLA_CIRCULANTE:\n", "    elif False:\n"),
    ("c16 · sin registro no bloquea", MF, '    if not _registro_ok(C["registro"]):\n', "    if False:\n"),
    ("c17 · sin fundamento no bloquea", MF, '    if not str(C["fundamento"] or "").strip():\n', "    if False:\n"),
    ("c18 · la réplica de un libro V6.3 o V6.3.1 con la normalización declarada usa el circulante declarado, no el del libro", MF,
     '    if (us and U["retira_de_14"]) or circ_aplica or nl_activa:\n', '    if (us and U["retira_de_14"]) or nl_activa:\n'),
    ("c19 · la réplica de un libro V6.3.2 ignora su normalización", MF,
     '                return _wc_normalizado(y, set(nl["anios"])) if nl["efectiva"] == REGLA_CIRCULANTE else None\n', "                return H[\"dwc\"][y]\n"),
    ("c20 · la réplica no contrasta las filas 95–97 del libro V6.3.2", MF, "    rep.extend(V631m.replica_circulante(L, anios, col))", "    pass"),
    ("c21 · F1-LIBRO con un libro V6.3 no mira la normalización", MF, "or dif_motor or hay_ajuste or hay_circ):", "or dif_motor or hay_ajuste):"),
    ("c22 · f vacía en un libro V6.3.2 con la normalización activa se trata como libro ilegible", MF,
     ' or (nl is not None and nl["efectiva"] in V631.EFECTIVAS_ACTIVAS)\n', "\n"),
    ("c23 · el oráculo no contrasta los años normalizados del libro V6.3.2", LV, '    elif circ is not None and nl["anios"] != sorted(circ):\n', "    elif False:\n"),
    ("c24 · el oráculo no ve un libro V6.3.2 normalizado sin la declaración", LV, '    elif circ is None and nl["efectiva"] != "ninguna":\n', "    elif False:\n"),
    ("c25 · el oráculo no dice que un libro V6.3.1 no normaliza el circulante", LV, "        if circ is not None and circ_efecto:\n", "        if False:\n"),
    ("c26 · aplicar escribe una normalización no aplicable", LV, '        ap = bool(C and C["aplicable"])\n', "        ap = bool(C)\n"),
    ("c27 · aplicar escribe la normalización en un libro V6.3.1", LV, "    if circulante:\n", "    if True:\n"),
    ("c28 · replica_circulante no contrasta el circulante excluido", LV, "        if v95 is None or abs(v95 - e95) > TOL:\n", "        if False:\n"),
    ("c29 · la réplica de las filas 95–97 da por buena cualquier marca con la regla (la efectiva sería «circulante_a_cero» con una marca 2)", LV,
     '    elif nl["regla"] == REGLA_CIRC and all(_num(v) == 1 for v in marcas):\n', '    elif nl["regla"] == REGLA_CIRC:\n'),
    ("c30 · la huella de entradas no lleva la normalización (V6.3.2)", EE, '    if "Historia" in hojas and "NORMALIZACIÓN DEL CIRCULANTE" in str(lec.leer("Historia", "A92") or ""):',
     "    if False:"),
    ("c31 · la V6.3.2 no es de la familia V6.3.1 (el paso 2 no le aplicaría la declaración)", SE, "    return version(cfg) in FAMILIA_V631\n", "    return version(cfg) == V631\n"),
    ("c32 · la V6.3.2 sin resumen propio", CI, '            else RESUMEN_V632 if v == "V6.3.2 F1" else "resumen_v2.csv")', '            else "resumen_v2.csv")'),
    ("c33 · el volcado a las fases dice la normalización aunque no esté activa", VD,
     '    if "NORMALIZACIÓN DEL CIRCULANTE" not in str(ws["A92"].value or "") or ws["C97"].value != "circulante_a_cero":',
     '    if "NORMALIZACIÓN DEL CIRCULANTE" not in str(ws["A92"].value or ""):'),
    # (revisión C1, 19-nov-2026) la exclusión del circulante en C46, demostrada con el cálculo declarado del expediente
    ("c34 · F1-CIRC no exige la demostración con el cálculo declarado de C46 (vuelve a bastar la partida)", MF, '    if C["aplicable"] and media_w:\n', "    if False:\n"),
    ("c35 · sin la carpeta del expediente la partida basta", MF, '        prob.append(("INCOMPLETO", "sin la carpeta del expediente no se puede demostrar',
     '        return [], info\n        prob.append(("INCOMPLETO", "sin la carpeta del expediente no se puede demostrar'),
    ("c36 · sin fase1_v63.json la partida basta", MF, '        prob.append(("INCOMPLETO", f"el expediente no tiene {F1_V63} legible',
     '        return [], info\n        prob.append(("INCOMPLETO", f"el expediente no tiene {F1_V63} legible'),
    ("c37 · con C46 sin cálculo declarado la partida basta", MF, '        prob.append(("INCOMPLETO", f"C46 no tiene cálculo declarado',
     '        return [], info\n        prob.append(("INCOMPLETO", f"C46 no tiene cálculo declarado'),
    ("c38 · el cálculo de C46 no se contrasta con sus fuentes (calcular_entrada sin la carpeta)", MF,
     '        out = FH.calcular_entrada("C46", d, partidas, anios_h, carpeta)\n', '        out = FH.calcular_entrada("C46", d, partidas, anios_h)\n'),
    ("c39 · el cálculo de C46 puede ser una suma", MF, '    if cal.get("operacion") != "media":\n', "    if False:\n"),
    ("c40 · el cálculo de C46 puede usar otros años que la ventana de f", MF, "    if sel != sorted(ventana):\n", "    if False:\n"),
    ("c41 · el cálculo de C46 puede no llevar el CFO", MF, '    if neto.get("cfo", 0) != 1:\n', "    if False:\n"),
    ("c42 · el cálculo de C46 puede no sumar la fila 14 (o sumarla con otro signo o dos veces)", MF, '    if neto.get("circulante", 0) != 1:\n', "    if False:\n"),
    ("c43 · el cálculo de C46 no se ata al C46 del libro", MF,
     "    elif bruto is None or abs(c46 - bruto) > max(TOL_E7, _unidad_de_redondeo(c46) / 2) + Fr(1, 10 ** 9):\n", "    elif False:\n"),
    ("c44 · el C46 del libro frente al cálculo sin la unidad con que lo escribe (±0,0005 siempre)", MF,
     "abs(c46 - bruto) > max(TOL_E7, _unidad_de_redondeo(c46) / 2) + Fr(1, 10 ** 9):", "abs(c46 - bruto) > TOL_E7:"),
    ("c45 · el C46 del libro frente al cálculo con una tolerancia de 100 mm", MF,
     "abs(c46 - bruto) > max(TOL_E7, _unidad_de_redondeo(c46) / 2) + Fr(1, 10 ** 9):", "abs(c46 - bruto) > 100:"),
    ("c46 · las filas 11 y 14 del libro no se atan a la Historia del cálculo", MF, "            if vh is None or vl is None or abs(vh - vl) > TOL_E7:\n",
     "            if False:\n"),
    ("c47 · no se buscan términos que compensen la fila 14", MF, "    if not prob and media_w:\n", "    if False:\n"),
    ("c48 · solo compensaciones de un término (no combinaciones)", MF, "            for k in range(1, len(serie) + 1):\n", "            for k in range(1, 2):\n"),
    ("c49 · la compensación se busca con el signo cambiado", MF, "                    if abs(m + media_w) <= TOL_E7:\n", "                    if abs(m - media_w) <= TOL_E7:\n"),
    ("c50 · el informe no dice el cálculo de C46", MF, '               _md_calculo_c46(nc.get("calculo_C46")),\n', ""),
    ("c51 · el resultado no enseña el cálculo de C46", MF, '            "calculo_C46": (circ_info or {}).get("calculo_C46"),\n', '            "calculo_C46": None,\n'),
]
SRC = {f: open(os.path.join(PV, f), encoding="utf-8").read() for f in {m[1] for m in M}}


def correr(cambios):
    """Las baterías con los archivos `cambios` ({ruta relativa a personaje_v2: contenido}), en una copia temporal: {"n_pasa", "n_falla", "pasan",
    "interrumpidas"}."""
    tmp = tempfile.mkdtemp(prefix="mut_circ_")
    try:
        raiz = os.path.join(tmp, "munger_v2_r1")
        pv = os.path.join(raiz, "personaje_v2")
        for d in ("scripts", "esquema", "prompts"):
            shutil.copytree(os.path.join(PV, d), os.path.join(pv, d), ignore=shutil.ignore_patterns("__pycache__"))
        for f in os.listdir(PV):
            if f.startswith("config_v2") and f.endswith(".json"):
                shutil.copy(os.path.join(PV, f), pv)
        os.makedirs(os.path.join(pv, "pruebas"))
        for b in BATERIAS:
            shutil.copy(os.path.join(PV, "pruebas", b), os.path.join(pv, "pruebas"))
        shutil.copytree(os.path.join(PV, "pruebas", "datos_circulante"), os.path.join(pv, "pruebas", "datos_circulante"))
        os.symlink(os.path.join(RAIZ, "v6"), os.path.join(raiz, "v6"))   # plantillas, referencias y guiones: solo lectura
        for rel in ("empresas_v2_correcciones",):   # el libro de Elis y sus datos (test_motor_a_f1.py): solo lectura
            os.symlink(os.path.join(PV, rel), os.path.join(pv, rel))
        for f, contenido in cambios.items():
            open(os.path.join(pv, f), "w", encoding="utf-8").write(contenido)
        td = os.path.join(tmp, "tmp")
        os.makedirs(td)
        out = {"pasan": set(), "n_pasa": 0, "n_falla": 0, "interrumpidas": []}
        for b in BATERIAS:
            r = subprocess.run([sys.executable, "-B", os.path.join("pruebas", b)], cwd=pv, capture_output=True, text=True,
                               env=dict(os.environ, TMPDIR=td, PYTHONDONTWRITEBYTECODE="1"))
            for ln in r.stdout.splitlines():
                if ln.startswith("PASA "):
                    out["pasan"].add((b, ln[8:68]))
                    out["n_pasa"] += 1
                elif ln.startswith("FALLA"):
                    out["n_falla"] += 1
            if r.returncode != 0 and "Traceback" in r.stderr:
                out["interrumpidas"].append(f"{b} ({r.stderr.strip().splitlines()[-1][:100]})")
        return out
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


BASE = correr({})
if BASE["interrumpidas"] or BASE["n_falla"]:
    sys.exit(f"sin mutar no pasan todas ({BASE['n_falla']} fallan; {BASE['interrumpidas']}): no hay con qué comparar")


def una(m):
    nombre, f, viejo, nuevo = m
    n = SRC[f].count(viejo)
    if n != 1:
        return False, f"ERROR        · {nombre}: el texto a mutar aparece {n} veces en {f}"
    r = correr({f: SRC[f].replace(viejo, nuevo)})
    dejan = BASE["n_pasa"] - r["n_pasa"]
    ok = dejan > 0 or bool(r["interrumpidas"])
    ej = sorted(BASE["pasan"] - r["pasan"])
    return ok, (("DETECTADA    " if ok else "NO DETECTADA ") + f"· {nombre} ({f}) · pasan {r['n_pasa']} de {BASE['n_pasa']} ({dejan} dejan de pasar)"
                + (f" · se interrumpe {r['interrumpidas'][0]}" if r["interrumpidas"] else "") + (f" (p. ej. «{ej[0][0]}: {ej[0][1]}…»)" if ej else ""))


with ThreadPoolExecutor(max_workers=int(os.environ.get("MUT_TRABAJADORES", "3"))) as ex:
    res = list(ex.map(una, M))
out = [f"sin mutar: {BASE['n_pasa']} pruebas pasan y {BASE['n_falla']} fallan ({', '.join(BATERIAS)})"] + [x for _, x in res]
det = sum(ok for ok, _ in res)
out.append(f"\n{det} de {len(M)} mutaciones detectadas")
if SALIDA:
    open(SALIDA, "w", encoding="utf-8").write("\n".join(out) + "\n")
print("\n".join(out))
sys.exit(0 if det == len(M) else 1)
