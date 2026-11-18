#!/usr/bin/env python3
"""Mutaciones de la parte de US GAAP de motor_a_f1.py frente a la batería pruebas/test_motor_a_f1_usgaap.py: cada mutación (una línea de la
capa cambiada a propósito) tiene que hacer fallar alguna prueba. Sirve para comprobar que la batería protege las guardas nuevas.

Uso (desde cualquier carpeta): python3 -I mutaciones_usgaap.py [SALIDA.txt]
Trabaja sobre copias temporales de personaje_v2/scripts, esquema y la batería: no toca el árbol. Sin LibreOffice.
"""
import os
import shutil
import subprocess
import sys
import tempfile

PV = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
SALIDA = sys.argv[1] if len(sys.argv) > 1 else None
M = [
 # ---------------------------------------------------------------- ronda 1 (actualizadas al código de la ronda 2)
 ("m01 · la lógica de US GAAP desactivada (us = False)", 'us = norma == "US_GAAP"   # (F1', 'us = False and norma == "US_GAAP"   # (F1'),
 ("m02 · norma del libro buscando «ifrs» dentro del texto (H13)", 'return NORMA_DEL_LIBRO.get(t.casefold()) if t else None',
  'return ("NIIF" if "ifrs" in t.casefold() else NORMA_DEL_LIBRO.get(t.casefold())) if t else None'),
 ("m03 · la amortización operativa dentro de la fila 8 no sale de D_X (rou8 = solo financieros)", 'rou, rou8 = U["rou_fin"], U["rou8"]', 'rou, rou8 = U["rou_fin"], U["rou_fin"]'),
 ("m04 · el circulante no retira la partida del arrendamiento operativo", '        return w - U["ajuste"][y] if y in U["ajuste"] else None\n\n    def calcular', '        return w if y in U["ajuste"] else None\n\n    def calcular'),
 ("m05 · F1-US-C49 no ve el exceso de C49", 'exceso_c49, defecto_c49 = resto > tol, resto < -tol', 'exceso_c49, defecto_c49 = False, resto < -tol'),
 ("m06 · F1-US-C49 no ve el defecto (principal financiero omitido)", 'exceso_c49, defecto_c49 = resto > tol, resto < -tol', 'exceso_c49, defecto_c49 = resto > tol, False'),
 ("m07 · F1-US-DA no salta con A0", '    da1 = per == "A0_total" and a8_pos\n', '    da1 = False\n'),
 ("m08 · F1-US-SIM no ve la variación del pasivo sola en el circulante", '    pas14_solo_sin = sin_ajuste and en14 == ["variacion_pasivo"]', '    pas14_solo_sin = False'),
 ("m09 · F1-LIBRO no salta por el ajuste del circulante", 'hay_ajuste = bool(us and U["retira_de_14"] and any(', 'hay_ajuste = bool(False and U["retira_de_14"] and any('),
 ("m10 · el puente con el motor B solo informa", '    elif op23 > TOL_E7 and motor == "B":', '    elif op23 > TOL_E7 and motor == "Z":'),
 ("m11 · «no_publicada» sin marcar la hipótesis D-US1", '            hip.append(clave)\n', '            pass\n'),
 ("m12 · D-US2 bis: el neto dentro de la fila 14 con el signo cambiado (coste − pagos)", 'neto[y] = S["pagos_arr_operativo"][y] - S["coste_arr_operativo"][y]',
  'neto[y] = S["coste_arr_operativo"][y] - S["pagos_arr_operativo"][y]'),
 ("m13 · K3b de los operativos sin el exceso de C49", '(1 if f["pagos_op_pos"] else 0) + (1 if f["exceso_c49"] else 0) +', '(1 if f["pagos_op_pos"] else 0) + 0 +'),
 ("m14 · declaración NIIF con claves de US GAAP sin F1-US-MEZCLA", 'elif norma == "NIIF" and (decl.get("arrendamientos_us_gaap") is not None', 'elif norma == "NADA" and (decl.get("arrendamientos_us_gaap") is not None'),
 ("m15 · US GAAP con C48 > 0 sin F1-US-MEZCLA", 'if (c48 is not None and c48 > TOL_E7) else []) + ([f"Historia fila 16', 'if (c48 is not None and c48 > 10 ** 9) else []) + ([f"Historia fila 16'),
 ("m16 · «no_publicada» sin contrastar la página citada", '        elif lineas:\n            C["invalidas"].append(f"{et}: «no_publicada»', '        elif lineas and False:\n            C["invalidas"].append(f"{et}: «no_publicada»'),
 ("m17 · la cita de una clasificación no se busca en la página", '        elif cita not in _nlin(pag):\n            C["invalidas"]', '        elif False:\n            C["invalidas"]'),
 ("m18 · la réplica del libro con el ajuste del circulante", '        r0 = calcular("A0_total", aplicar_n1=False, con_ajuste=False)', '        r0 = calcular("A0_total", aplicar_n1=False, con_ajuste=True)'),
 ("m19 · un libro US GAAP sin arrendamientos a la vista no exige F1", 'return arrendamientos_en_el_libro(L) or norma_del_libro(L) == "US_GAAP"', 'return arrendamientos_en_el_libro(L)'),
 ("m20 · vigencia: el motor B con US GAAP no exige F1", 'puente_b = motor == "B" and exigido_puente(carpeta)', 'puente_b = False'),
 ("m21 · el motor B con US GAAP no se evalúa", '        if nd == "US_GAAP" or nl == "US_GAAP" or (nl is None and (carpeta is None or _expediente_415(carpeta))):', '        if False:'),
 ("m22 · F1-ROU-HISTORIA trata la fila 23 con US GAAP como con NIIF", '        fila23 = fila23 if (U["op"] is False and U["fin"] is False) else []\n', '        pass\n'),
 ("m23 · una ubicación sin declarar vale cero (a8 = 0)", '        U["a8"] = dict(cero) if conocida else {}', '        U["a8"] = dict(cero)'),
 ("m24 · existencia de una clase sin evidencia", '        if not _evidencia_ok(d):\n            faltas.append(f"arrendamientos_us_gaap.{nombre}: sin documento', '        if False:\n            faltas.append(f"arrendamientos_us_gaap.{nombre}: sin documento'),
 ("m25 · el importe retirado solo se exige en la ventana", 'j_w = [y for y in sorted(set(ventana) | set(horiz)) if y not in U["ajuste"]]', 'j_w = [y for y in sorted(set(ventana)) if y not in U["ajuste"]]'),
 ("m26 · K3b afirma «una vez» sin el desglose", 'k3["K3b_alquiler_contado"], k3["K3b_por_clase"] = "no evaluable (falta declarar si hay arrendamientos operativos y financieros)", None', 'k3["K3b_alquiler_contado"], k3["K3b_por_clase"] = "una vez", None'),
 ("m27 · la cota D-US1 con el signo cambiado", 'entradas["si la variación del pasivo estuviera sola dentro de la fila 14 (el alquiler se omitiría): como máximo, los pagos"] = efecto(p_m / S_w)',
  'entradas["si la variación del pasivo estuviera sola dentro de la fila 14 (el alquiler se omitiría): como máximo, los pagos"] = efecto(-p_m / S_w)'),
 ("m28 · una conclusión con hipótesis no se rotula condicionada", '    cond = res.get("condicionada")\n    bis = ', '    cond = None\n    bis = '),
 ("m29 · el coste lineal no se exige", '        if l_w:\n            faltas.append(', '        if False:\n            faltas.append('),
 ("m30 · F1-SERIES no examina las series de US GAAP", '("da_rou", "da_ppa") + (SERIES_US if us is not None else ())', '("da_rou", "da_ppa") + (() if us is not None else ())'),
 ("m31 · la fila 86 del libro solo con los financieros", '    if _valor(decl, "norma_contable")[0] == "US_GAAP":\n        return leer_us(decl, anios)["rou8"]', '    if _valor(decl, "norma_contable")[0] == "US_GAAP":\n        return leer_us(decl, anios)["rou_fin"]'),
 ("m32 · F1-US-DA no ve la amortización sola en el circulante", '    am14_solo_sin = sin_ajuste and en14 == ["amortizacion_rou"]', '    am14_solo_sin = False'),
 ("m33 · F1-US-SIM no ve la amortización excluida sin pagos", '    s1 = per in ("A1_sin_ROU", "A2_propio", "A3_estimado") and a8_pos and not pagos_op_pos', '    s1 = False'),
 ("m34 · el pasivo operativo mayor que la fila 23 no se rechaza", '    elif l23 is not None and op23 > l23 + TOL_E7:', '    elif l23 is not None and op23 > l23 + 10 ** 9:'),
 ("m35 · F1-US-FILAS no contradice una línea de la fila 14 que nombra un tramo declarado en otro sitio", '                    mal_k = [k for k in fuera14 if _LADO_TRAMO[k] in c["lados"]]', '                    mal_k = []'),
 ("m36 · F1-US-FILAS no contradice una línea de la fila 8 que nombra el derecho de uso", '                elif en8 or (fin8 and not c["es_op"]):', '                elif True:'),
 ("m37 · exigido_puente falla en abierto con la norma sin determinar", '    if n is not None:\n        return n == "US_GAAP"\n    return _expediente_415(carpeta)', '    return n == "US_GAAP"'),
 ("m38 · el dato del puente bloquea al motor A", '    elif op23 is None and motor != "B" and U["op"] is True:', '    elif op23 is None and motor == "Z" and U["op"] is True:'),
 # ---------------------------------------------------------------- ronda 2 · R1-1: motor B
 ("n01 · (R1-1) L4 leído con el lector ligero, que devuelve el índice del texto compartido", '            L = {"Control maestro!L4": _l4_del_libro(libro)}',
  '            L = {"Control maestro!L4": __import__("v63_xml").LibroV63(libro).leer("Control maestro", "L4")}'),
 ("n02 · (R1-1) con la norma sin determinar el motor B pide el desglose de US GAAP en vez de pararse en F1-NORMA", '    if norma != "US_GAAP" and norma_del_libro(L) != "US_GAAP":\n        res["alcance"]',
  '    if False:\n        res["alcance"]'),
 # ---------------------------------------------------------------- ronda 2 · R1-3 y R1-6: contraste de ubicaciones
 ("n03 · (R1-3) sin fase1_partes una ubicación declarada se da por contrastada", '                marcar(clave, "sin_contrastar", "sin fase1_partes en el expediente: la ubicación declarada no se ha contrastado con las líneas que la fase 1 sumó en las filas 8 y 14")',
  '                marcar(clave, "contrastada", "x")'),
 ("n04 · (R1-3) «fuera» aunque la línea citada esté entre las sumadas", '                if enl:\n                    contradice.append(f"{nom} está declarada fuera de las filas 8 y 14, pero la línea citada',
  '                if enl and False:\n                    contradice.append(f"{nom} está declarada fuera de las filas 8 y 14, pero la línea citada'),
 ("n05 · (R1-3) la cita no tiene que nombrar el arrendamiento", '            if not ls or _LINEA_SUPL.search(cn):', '            if False:'),
 ("n06 · (R1-3) la cita de un tramo puede ser la línea del otro", '            if lado not in ls:\n                insuf.append', '            if False:\n                insuf.append'),
 ("n07 · (R1-3) «fuera» sin que la página citada sea la del estado de flujos", '                if not es_estado(pag):\n                    insuf.append(f"{et}: «fuera de las filas» se prueba',
  '                if False:\n                    insuf.append(f"{et}: «fuera de las filas» se prueba'),
 ("n08 · (R1-3) la cita vale aunque solo esté dentro de una línea de información complementaria",
  '            if not [t for t in _lineas_con_cita(explotacion(pag), cn) if not _LINEA_SUPL.search(t) and not (_ES_FIN.search(t) and not _ES_OP.search(t))]:', '            if False:'),
 ("n09 · (R1-3) «fila_8» o «fila_14» con una línea del estado de flujos que la fase 1 no sumó ahí", '            if es_estado(pag) and not enl and not con:', '            if False:'),
 ("n10 · (R1-3) las líneas de la fase 1 se toman solo del lado «actual»", '            sig, pro = comps(a + 1, k, "anterior"), comps(a, k, "actual")', '            sig, pro = None, comps(a, k, "actual")'),
 ("n11 · (R1-3) un año fijado a mano en fase1_decisiones.json se da por examinado", '            if str(a) in dk:\n                usados[a][k], sin_ex[(a, k)] = None,', '            if False:\n                usados[a][k], sin_ex[(a, k)] = None,'),
 ("n12 · (R1-3) sin reconstruir la etiqueta entera de las líneas partidas", '                comp = _etiqueta_completa(pagina(arch, c.get("pagina")), lin)', '                comp = None'),
 ("n13 · (R1-3) «fuera» contrastada con una página que no es de los años del modelo", '                if not del_modelo(pag):', '                if False:'),
 ("n14 · (R1-3) «fuera» contrastada sin haber examinado todos los años del modelo", '                elif falta:\n                    marcar(clave, "sin_contrastar", "la línea citada no está entre las sumadas en el informe citado',
  '                elif False:\n                    marcar(clave, "sin_contrastar", "la línea citada no está entre las sumadas en el informe citado'),
 ("n15 · (R1-3) la cota de «fila_8» sin contrastar con el signo cambiado", '"la habría excluido sin llevarla): el importe declarado"] = efecto(a8_m / S_w)', '"la habría excluido sin llevarla): el importe declarado"] = efecto(-a8_m / S_w)'),
 ("n16 · (R1-3) una ubicación sin contrastar no condiciona la conclusión", '    sc = dict(C.get("sin_contrastar") or {})', '    sc = {}'),
 ("n17 · (R1-6) «no_publicada»: cualquier cita de la declaración anula el contraste con la página",
  '        otras = [_nlin(U["ev"][k].get("cita")) for k in _LADO_TRAMO if k != clave and U["ub_decl"].get(k) not in (None, "no_publicada")]', '        otras = [_nlin(e_.get("cita")) for _, e_ in U["evidencias"]]'),
 ("n18 · (R1-6) «no_publicada» con una página que no es la del estado de flujos", '        if P is not None and not es_estado(pag):\n            C["incompletas"].append(f"{et}: «no_publicada»',
  '        if False:\n            C["incompletas"].append(f"{et}: «no_publicada»'),
 ("n19 · (R1-6) una línea que mezcla operativos y financieros se descarta por decir «financ»", 'if not _LINEA_ARR.search(t) or _LINEA_SUPL.search(t) or (_ES_FIN.search(t) and not _ES_OP.search(t)):',
  'if not _LINEA_ARR.search(t) or _LINEA_SUPL.search(t) or _ES_FIN.search(t):'),
 # ---------------------------------------------------------------- ronda 2 · D-US2 bis y D-WM
 ("n20 · (D-US2 bis) los dos tramos en la fila 14 se retiran del circulante (lectura estricta anterior)", '"retira_de_14": len(en14) == 1,', '"retira_de_14": len(en14) >= 1,'),
 ("n21 · (D-US2 bis) se publica el valor de la hoja sin comprobar las dos líneas", '        if pend:\n            insuf.append("D-US2 bis:', '        if False:\n            insuf.append("D-US2 bis:'),
 ("n22 · (D-US2 bis) cuánto cambiaría contando los pagos, con el signo cambiado", '            ef = efecto(n_m / S_w)                    # contar los pagos', '            ef = efecto(-n_m / S_w)                    # contar los pagos'),
 ("n23 · (D-US2 bis) el rótulo no dice que el valor es el de la hoja", '    bis = ((res.get("us_gaap") or {}).get("D_US2_bis") or {}).get("texto")', '    bis = None'),
 ("n24 · (D-WM) «no_publicado» no se aplica (se siguen pidiendo amortización y principal)", '        elif dg == "no_publicado":\n            U["fin_como_deuda"] = True', '        elif dg == "no_publicado":\n            U["fin_como_deuda"] = False'),
 ("n25 · (D-WM) C49 positivo con los financieros tratados como deuda", '        exceso_c49 = C49 > TOL_US_C49\n', '        exceso_c49 = False\n'),
 ("n26 · (D-WM) la diferencia estimada con el signo cambiado", '            ef = efecto(d_m / S_w)   # tratados como arrendamientos', '            ef = efecto(-d_m / S_w)   # tratados como arrendamientos'),
 ("n27 · (D-WM) no se exigen la caja pagada ni el gasto total", '            x_w = [y for y in ventana if y not in S[s_]]', '            x_w = []'),
 ("n28 · (D-WM) la hipótesis no condiciona la conclusión", '        conds.append({"id": "D-WM", "tipo": "hipótesis declarada", "tramos": ["financieros"],', '        ({}).update({"id": "D-WM", "tipo": "hipótesis declarada", "tramos": ["financieros"],'),
 # ---------------------------------------------------------------- ronda 2 · R1-7 a R1-16
 ("n29 · (R1-7) el coste «no comparable» se trata como comparable", '    comparable = U["coste_comparable"]', '    comparable = True'),
 ("n30 · (R1-8) el resumen de la cota no suma las variaciones del mismo signo", 'return [round(sum(x for x in xs if x < 0), 6), round(sum(x for x in xs if x > 0), 6)] if xs else None',
  'return [round(min(xs + [0]), 6), round(max(xs + [0]), 6)] if xs else None'),
 ("n31 · (R1-9) el motor B no avisa del ancla de S2C", '    if U["op"] is not False:\n        # (R1-9)', '    if False:\n        # (R1-9)'),
 ("n32 · (R1-9) el puente no se contrasta con las líneas de la fila 23", '    if op23 is not None and op23 <= TOL_E7 and lin23:', '    if False:'),
 ("n33 · (R1-9) motor B sin arrendamientos declarados y con pasivo en la fila 23", '    elif motor == "B" and U["op"] is False and U["fin"] is False and l23 is not None and l23 > TOL_E7:', '    elif False:'),
 ("n34 · (R1-11) la norma de la fase 1 no se comprueba", '    if not t or t.casefold() in NORMA_DEL_LIBRO or t.casefold() == "otro":', '    if True:'),
 ("n35 · (R1-13) tolerancia fija de C49 (no la del redondeo con que se registró)", '        tol = TOL_US_C49 if C49 == 0 else max(TOL_US_C49, _unidad_de_redondeo(C49) / 2)', '        tol = TOL_US_C49'),
 ("n36 · (R1-13) un cero en C49 se toma como redondeo a la unidad", '        tol = TOL_US_C49 if C49 == 0 else max(TOL_US_C49, _unidad_de_redondeo(C49) / 2)', '        tol = max(TOL_US_C49, _unidad_de_redondeo(C49) / 2)'),
 ("n37 · (R1-13) la diferencia explicada en conciliacion_fcf_base no se admite", '        expl = _conciliacion_explicada(decl).get("C49", Fr(0))', '        expl = Fr(0)'),
 ("n38 · (R1-14) la declaración mal formada no se normaliza", '    decl, mal_formadas = _declaracion_bien_formada(decl)', '    decl, mal_formadas = decl, []'),
 ("n39 · (R1-15) K3 se presenta como conforme sin contraste con líneas", '    if us and k3["conforme"] is True and k3.get("K3b_contrastado") is False:', '    if False:'),
 ("n40 · (R1-15) K3b siempre «contrastado»", '    fund = (U.get("contraste") or {}).get("fundamento") or "declarado"', '    fund = "contrastado"'),
 ("n41 · (R1-16) F1-ROU-HISTORIA bloquea la amortización financiera declarada fuera de la fila 8 (y D-WM)", '        if U["fin"] is True and (U["fin_como_deuda"] or U["fin_am_ub"] == "fuera_de_la_fila_8"):\n            fila17 = []',
  '        if False:\n            fila17 = []'),
 ("n42 · (R1-16) V-F1m bloquea A0 con la amortización financiera declarada fuera de la fila 8", ' and not (us and U["fin"] is True and U["fin_am_ub"] == "fuera_de_la_fila_8" and c49_pos and not rou_pos)', ''),
 ("n43 · (R1-16) «fuera_de_la_fila_8» sin la cifra publicada", '        x_w = [y for y in ventana if y not in S["da_rou_financiero_fuera"]]', '        x_w = []'),
 ("n44 · (R1-3 y R1-6) las líneas de arrendamiento posteriores al total del flujo de explotación cuentan como tramos del operativo", '            if t and any(x in t for x in cfo):', '            if False:'),
 ("n45 · (R1-3) una carpeta fase1_partes sin líneas se toma como contraste hecho", '        if not P["todos"]:\n            P = None', '        if False:\n            P = None'),
 ("n46 · (R1-3) la línea citada no se reconoce por los renglones de la página en que está la cita",
  ' or any(c["nlin"] in t for t in de_la_cita))]', ')]'),
]
src = open(os.path.join(PV, "scripts", "motor_a_f1.py"), encoding="utf-8").read()


def una(m):
    nombre, viejo, nuevo = m
    n = src.count(viejo)
    if n != 1:
        return False, f"ERROR  · {nombre}: el texto a mutar aparece {n} veces"
    tmp = tempfile.mkdtemp(prefix="mut_us_")
    try:
        pv = os.path.join(tmp, "personaje_v2")
        for d in ("scripts", "esquema", "prompts"):
            shutil.copytree(os.path.join(PV, d), os.path.join(pv, d), ignore=shutil.ignore_patterns("__pycache__"))
        os.makedirs(os.path.join(pv, "pruebas"))
        shutil.copy(os.path.join(PV, "pruebas", "test_motor_a_f1_usgaap.py"), os.path.join(pv, "pruebas"))
        open(os.path.join(pv, "scripts", "motor_a_f1.py"), "w", encoding="utf-8").write(src.replace(viejo, nuevo))
        r = subprocess.run([sys.executable, "-B", os.path.join("pruebas", "test_motor_a_f1_usgaap.py")], cwd=pv, capture_output=True, text=True)
        fallan = [l[8:90] for l in r.stdout.splitlines() if l.startswith("FALLA")]
        ok = r.returncode != 0
        return ok, (("DETECTADA   " if ok else "NO DETECTADA") + f" · {nombre}" + (f" · {len(fallan)} pruebas fallan (p. ej. «{fallan[0]}»)" if fallan else
                                                                                  (" · la batería se interrumpe: " + r.stderr.strip().splitlines()[-1][:120] if ok else "")))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


from concurrent.futures import ThreadPoolExecutor  # noqa: E402
with ThreadPoolExecutor(max_workers=int(os.environ.get("MUT_TRABAJADORES", "3"))) as ex:
    res = list(ex.map(una, M))
out = [x for _, x in res]
det = sum(ok for ok, _ in res)
out.append(f"\n{det} de {len(M)} mutaciones detectadas")
if SALIDA:
    open(SALIDA, "w", encoding="utf-8").write("\n".join(out) + "\n")
print("\n".join(out))
sys.exit(0 if det == len(M) else 1)
