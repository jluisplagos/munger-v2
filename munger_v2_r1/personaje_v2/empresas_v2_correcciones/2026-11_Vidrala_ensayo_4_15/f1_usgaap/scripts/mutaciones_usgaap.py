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
 ("m01 · la lógica de US GAAP desactivada (us = False)", 'us = norma == "US_GAAP"   # (F1', 'us = False and norma == "US_GAAP"   # (F1'),
 ("m02 · norma del libro buscando «ifrs» dentro del texto (H13)", 'return NORMA_DEL_LIBRO.get(t.casefold()) if t else None',
  'return ("NIIF" if "ifrs" in t.casefold() else NORMA_DEL_LIBRO.get(t.casefold())) if t else None'),
 ("m03 · la amortización operativa dentro de la fila 8 no sale de D_X (rou8 = solo financieros)", 'rou, rou8 = U["rou_fin"], U["rou8"]', 'rou, rou8 = U["rou_fin"], U["rou_fin"]'),
 ("m04 · el circulante no retira la partida del arrendamiento operativo", '        return w - U["ajuste"][y] if y in U["ajuste"] else None\n\n    def calcular', '        return w if y in U["ajuste"] else None\n\n    def calcular'),
 ("m05 · F1-US-C49 no ve el exceso de C49", 'exceso_c49, defecto_c49 = dif > TOL_US_C49, dif < -TOL_US_C49', 'exceso_c49, defecto_c49 = False, dif < -TOL_US_C49'),
 ("m06 · F1-US-C49 no ve el defecto (principal financiero omitido)", 'exceso_c49, defecto_c49 = dif > TOL_US_C49, dif < -TOL_US_C49', 'exceso_c49, defecto_c49 = dif > TOL_US_C49, False'),
 ("m07 · F1-US-DA no salta con A0", '    da1 = per == "A0_total" and a8_pos\n', '    da1 = False\n'),
 ("m08 · F1-US-SIM no ve la variación del pasivo sola en el circulante", '    pas14_solo_sin = sin_ajuste and en14 == ["variacion_pasivo"]', '    pas14_solo_sin = False'),
 ("m09 · F1-LIBRO no salta por el ajuste del circulante", 'hay_ajuste = bool(us and U["tramos_en_fila_14"] and any(', 'hay_ajuste = bool(False and U["tramos_en_fila_14"] and any('),
 ("m10 · el puente con el motor B solo informa", '    elif op23 > TOL_E7 and motor == "B":', '    elif op23 > TOL_E7 and motor == "Z":'),
 ("m11 · «no_publicada» sin marcar la hipótesis D-US1", '            hip.append(clave)\n', '            pass\n'),
 ("m12 · ajuste derivado con el signo cambiado (coste − pagos)", 'aj[y] = S["pagos_arr_operativo"][y] - S["coste_arr_operativo"][y]', 'aj[y] = S["coste_arr_operativo"][y] - S["pagos_arr_operativo"][y]'),
 ("m13 · K3b de los operativos sin el exceso de C49", '(1 if f["pagos_op_pos"] else 0) + (1 if f["exceso_c49"] else 0) +', '(1 if f["pagos_op_pos"] else 0) + 0 +'),
 ("m14 · declaración NIIF con claves de US GAAP sin F1-US-MEZCLA", 'elif norma == "NIIF" and (decl.get("arrendamientos_us_gaap") is not None', 'elif norma == "NADA" and (decl.get("arrendamientos_us_gaap") is not None'),
 ("m15 · US GAAP con C48 > 0 sin F1-US-MEZCLA", 'if (c48 is not None and c48 > TOL_E7) else []) + ([f"Historia fila 16', 'if (c48 is not None and c48 > 10 ** 9) else []) + ([f"Historia fila 16'),
 ("m16 · «no_publicada» sin contrastar la página citada", '            if lineas:\n                inval.append(f"{et}: «no_publicada»', '            if lineas and False:\n                inval.append(f"{et}: «no_publicada»'),
 ("m17 · la cita de una clasificación no se busca en la página", '            elif cita not in VE._norm_txt(pag):', '            elif False:'),
 ("m18 · la réplica del libro con el ajuste del circulante", '        r0 = calcular("A0_total", aplicar_n1=False, con_ajuste=False)', '        r0 = calcular("A0_total", aplicar_n1=False, con_ajuste=True)'),
 ("m19 · un libro US GAAP sin arrendamientos a la vista no exige F1", 'return arrendamientos_en_el_libro(L) or norma_del_libro(L) == "US_GAAP"', 'return arrendamientos_en_el_libro(L)'),
 ("m20 · vigencia: el motor B con US GAAP no exige F1", 'puente_b = motor == "B" and not out["exento"] and us_gaap_del_expediente(carpeta)', 'puente_b = False'),
 ("m21 · el motor B con US GAAP no se evalúa", 'if motor_ == "B" and "US_GAAP" in (', 'if motor_ == "Z" and "US_GAAP" in ('),
 ("m22 · F1-ROU-HISTORIA trata la fila 23 con US GAAP como con NIIF", '        fila23 = fila23 if (U["op"] is False and U["fin"] is False) else []\n', '        pass\n'),
 ("m23 · una ubicación sin declarar vale cero (a8 = 0)", '        U["a8"] = dict(cero) if conocida else {}', '        U["a8"] = dict(cero)'),
 ("m24 · existencia de una clase sin evidencia", '        if not _evidencia_ok(d):\n            faltas.append(f"arrendamientos_us_gaap.{nombre}: sin documento', '        if False:\n            faltas.append(f"arrendamientos_us_gaap.{nombre}: sin documento'),
 ("m25 · el importe retirado solo se exige en la ventana", 'j_w = [y for y in sorted(set(ventana) | set(horiz)) if y not in U["ajuste"]]', 'j_w = [y for y in sorted(set(ventana)) if y not in U["ajuste"]]'),
 ("m26 · K3b afirma «una vez» sin el desglose", 'k3["K3b_alquiler_contado"], k3["K3b_por_clase"] = "no evaluable (falta declarar si hay arrendamientos operativos y financieros)", None', 'k3["K3b_alquiler_contado"], k3["K3b_por_clase"] = "una vez", None'),
 ("m27 · la cota D-US1 con el signo cambiado", 'dfs["si la variación del pasivo estuviera sola dentro de la fila 14 (el alquiler se omitiría): como máximo, los pagos"] = p_m / S_w', 'dfs["si la variación del pasivo estuviera sola dentro de la fila 14 (el alquiler se omitiría): como máximo, los pagos"] = -p_m / S_w'),
 ("m28 · una conclusión con hipótesis no se rotula condicionada", '        res["condicionada"] = {"hipotesis": "D-US1"', '        res["condicionada_x"] = {"hipotesis": "D-US1"'),
 ("m29 · el coste lineal no se exige", '        if l_w:\n            faltas.append(', '        if False:\n            faltas.append('),
 ("m30 · F1-SERIES no examina las series de US GAAP", '("da_rou", "da_ppa") + (SERIES_US if us is not None else ())', '("da_rou", "da_ppa") + (() if us is not None else ())'),
 ("m31 · la fila 86 del libro solo con los financieros", '    if _valor(decl, "norma_contable")[0] == "US_GAAP":\n        return leer_us(decl, anios)["rou8"]', '    if _valor(decl, "norma_contable")[0] == "US_GAAP":\n        return leer_us(decl, anios)["rou_fin"]'),
 ("m32 · F1-US-DA no ve la amortización sola en el circulante", '    am14_solo_sin = sin_ajuste and en14 == ["amortizacion_rou"]', '    am14_solo_sin = False'),
 ("m33 · F1-US-SIM no ve la amortización excluida sin pagos", '    s1 = per in ("A1_sin_ROU", "A2_propio", "A3_estimado") and a8_pos and not pagos_op_pos', '    s1 = False'),
 ("m34 · el pasivo operativo mayor que la fila 23 no se rechaza", '    elif l23 is not None and op23 > l23 + TOL_E7:', '    elif l23 is not None and op23 > l23 + 10 ** 9:'),
 ("m35 · F1-US-FILAS no contrasta la fila 14 con fase1_partes", '    if hall["circulante_lineas"] and not U["tramos_en_fila_14"]:', '    if False and hall["circulante_lineas"] and not U["tramos_en_fila_14"]:'),
 ("m36 · F1-US-FILAS no contrasta la fila 8 con fase1_partes", '    if hall["da"] and not (U["op"] is True', '    if False and hall["da"] and not (U["op"] is True'),
 ("m37 · con el motor B y US GAAP el gancho no se exige (exigido_puente)", '    return not exencion(carpeta) and us_gaap_del_expediente(carpeta, libro=libro, L=L)', '    return False'),
 ("m38 · el dato del puente bloquea al motor A", '    if op23 is None and motor != "B" and U["op"] is True:', '    if op23 is None and motor == "Z" and U["op"] is True:'),
]
src = open(os.path.join(PV, "scripts", "motor_a_f1.py"), encoding="utf-8").read()
out, det = [], 0
for nombre, viejo, nuevo in M:
    n = src.count(viejo)
    if n != 1:
        out.append(f"ERROR  · {nombre}: el texto a mutar aparece {n} veces")
        continue
    tmp = tempfile.mkdtemp(prefix="mut_us_")
    try:
        pv = os.path.join(tmp, "personaje_v2")
        for d in ("scripts", "esquema"):
            shutil.copytree(os.path.join(PV, d), os.path.join(pv, d), ignore=shutil.ignore_patterns("__pycache__"))
        os.makedirs(os.path.join(pv, "pruebas"))
        shutil.copy(os.path.join(PV, "pruebas", "test_motor_a_f1_usgaap.py"), os.path.join(pv, "pruebas"))
        open(os.path.join(pv, "scripts", "motor_a_f1.py"), "w", encoding="utf-8").write(src.replace(viejo, nuevo))
        r = subprocess.run([sys.executable, "-B", os.path.join("pruebas", "test_motor_a_f1_usgaap.py")], cwd=pv, capture_output=True, text=True)
        fallan = [l[8:90] for l in r.stdout.splitlines() if l.startswith("FALLA")]
        ok = r.returncode != 0
        det += ok
        out.append(("DETECTADA   " if ok else "NO DETECTADA") + f" · {nombre}" + (f" · {len(fallan)} pruebas fallan (p. ej. «{fallan[0]}»)" if fallan else
                                                                                 (" · la batería se interrumpe: " + r.stderr.strip().splitlines()[-1][:120] if ok else "")))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
out.append(f"\n{det} de {len(M)} mutaciones detectadas")
if SALIDA:
    open(SALIDA, "w", encoding="utf-8").write("\n".join(out) + "\n")
print("\n".join(out))
sys.exit(0 if det == len(M) else 1)
