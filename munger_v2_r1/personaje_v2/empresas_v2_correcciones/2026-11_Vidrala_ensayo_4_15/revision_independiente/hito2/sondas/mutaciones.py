#!/usr/bin/env python3
"""Mutaciones del revisor (Fable, hito 2): quita o altera UNA regla del código de la candidata en un árbol aparte y ejecuta las baterías
permitidas (sin LibreOffice) para ver si alguna prueba lo detecta. El árbol mutado es ligero: scripts/ y pruebas/ copiados, el resto son
enlaces simbólicos a la copia propia del árbol congelado (solo lectura). Nunca toca el árbol congelado.
Uso: python3 -I -B mutaciones.py NOMBRE [NOMBRE …]   (sin argumentos: lista las mutaciones)"""
import json, os, re, shutil, subprocess, sys, time
F = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.environ.get("BASE", "hito2")  # BASE=hito1: las mismas mutaciones sobre el código y las pruebas del hito 1 (para comparar)
COPIA = os.path.join(F, "copia" if BASE == "hito2" else "copia_hito1", "munger_v2_r1")
MUT = os.path.join(F, "mut" if BASE == "hito2" else "mut_hito1")
B415, BEE, B414 = "test_verificacion_entradas_415.py", "test_entrada_efectiva_415.py", "test_verificacion_entradas_414.py"
VEP, FHP, FIP, INP, CIP = "scripts/verificacion_entradas.py", "scripts/fase1_historia.py", "scripts/ficha.py", "scripts/informe.py", "scripts/cierre_v2.py"

# nombre: (descripción, [(archivo, texto original, texto nuevo)], [baterías])
M = {
 "m00_control": ("control: sin cambio de regla (solo un comentario); las baterías tienen que pasar enteras en el árbol ligero",
    [(VEP, 'FORMATO = "4.15"', 'FORMATO = "4.15"  # control')], [BEE, B414, B415]),
 "m01_sin_signo": ("R415-SIGNO: _signo_en_cita devuelve siempre +1 (la marca de signo se ignora)",
    [(VEP, '    antes, despues = t[:ini], t[fin:]\n    antes = re.sub("[" + MONEDAS', '    return 1\n    antes, despues = t[:ini], t[fin:]\n    antes = re.sub("[" + MONEDAS')], [B415, BEE]),
 "m02_sin_pasaje_de_pagina": ("R415-SIGNO: contraste_pagina lee el signo en la cita, no en el pasaje de la página",
    [(VEP, 'est, det = _cita_cifra(f.get("cita"), vf, pag)', 'est, det = _cita_cifra(f.get("cita"), vf)')], [B415]),
 "m03_indeterminado_vale": ("R415-SIGNO: un signo indeterminado se da por bueno (ni pendiente ni discrepancia)",
    [(VEP, '        if est == "signo_indeterminado":\n            return "pendiente", (', '        if est == "signo_indeterminado" and False:\n            return "pendiente", (')], [B415]),
 "m04_signo_distinto_pendiente": ("R415-SIGNO: el signo contrario deja la entrada pendiente en vez de discrepancia",
    [(VEP, '        if est == "signo_distinto":\n            return "discrepancia", (', '        if est == "signo_distinto":\n            return "pendiente", (')], [B415]),
 "m05_dos_espacios_negativo": ("R415-SIGNO: el guion a dos o más espacios se lee como signo menos (no como otra columna)",
    [(VEP, '            return 1  # guion aislado de otra columna (un cero), separado de la cifra por dos o más espacios', '            return -1  # MUTACIÓN')], [B415]),
 "m06_un_espacio_negativo": ("R415-SIGNO: el guion a UN espacio se lee como signo menos (no indeterminado)",
    [(VEP, '        if m.group(1) == "" and (previo == "" or re.search(r"[\\s:;=/\\[|]$", previo)):', '        if len(m.group(1)) <= 1 and (previo == "" or re.search(r"[\\s:;=/\\[|]$", previo)):')], [B415]),
 "m07_dos_signos_vale": ("R415-SIGNO: la cifra con los dos signos a la vez vale si alguno coincide",
    [(VEP, '    if s in signos and -s not in signos:', '    if s in signos:')], [B415]),
 "m08_calc_sin_transformacion": ("R415-SIGNO (calcular_entrada): no se exige valor = signo × valor_fuente",
    [(FHP, '    if Fraction(repr(float(v))) != sg * Fraction(repr(float(vf))):', '    if False:')], [BEE]),
 "m09_calc_sin_tratamiento": ("R415-SIGNO (calcular_entrada): no se exige «tratamiento»",
    [(FHP, '    if not str(tr or "").strip():\n        raise ValueError(f"el componente {nombre} de {anio}: la transformación', '    if False:\n        raise ValueError(f"el componente {nombre} de {anio}: la transformación')], [BEE]),
 "m10_calc_cita_sin_signo": ("R415-SIGNO (calcular_entrada): la cita se contrasta con |cifra publicada| en la forma del hito 1 (sin signo)",
    [(FHP, 'est_c, det_c = VE._cita_cifra(cmp.get("cita"), publicado, pag)', 'est_c, det_c = ("ok", "") if (VE._cita_cifra(cmp.get("cita"), abs(publicado), pag)[0] != "ausente") else ("ausente", "")')], [BEE]),
 "m11_tolerancia_0_001": ("U2: tolerancia de importes ampliada a una milésima (0,001)",
    [(VEP, 'abs(exacto - fv) <= fractions.Fraction(1, 2000)', 'abs(exacto - fv) <= fractions.Fraction(1, 1000)')], [B415]),
 "m12_tolerancia_0_00055": ("U2: tolerancia de importes ampliada a 0,00055",
    [(VEP, 'abs(exacto - fv) <= fractions.Fraction(1, 2000)', 'abs(exacto - fv) <= fractions.Fraction(11, 20000)')], [B415]),
 "m13_importe_sin_3_decimales": ("U2: se quita la condición de que el libro tenga 3 decimales como mucho",
    [(VEP, 'return (fv * 1000).denominator == 1 and abs(exacto - fv)', 'return abs(exacto - fv)')], [B415]),
 "m14_empate_en_toda_magnitud": ("U2: el empate vale también sin unidad monetaria en el derivado",
    [(VEP, 'if not (_importe_libro_exacto(r_ex, vm) if importe else _igual_exacto(r, vm)):', 'if not (_importe_libro_exacto(r_ex, vm) if True else _igual_exacto(r, vm)):')], [B415]),
 "m15_publicado_como_hito1": ("U2: el dato publicado vuelve a la comparación del hito 1 (_igual_libro con floats)",
    [(VEP, 'if not (_importe_libro_exacto(sig * _frac(esc) * _frac(vf), vm) if importe else _igual_exacto(sig * esc * vf, vm)):', 'if not (_igual_libro(sig * esc * vf, vm) if importe else _igual_exacto(sig * esc * vf, vm)):')], [B415]),
 "m16_sin_limite_nodos": ("U3: sin límite de nodos de la fórmula",
    [(VEP, 'MAX_NODOS_FORMULA = 400', 'MAX_NODOS_FORMULA = 10 ** 9')], [B415]),
 "m17_sin_limite_longitud": ("U3: sin límite de longitud de la fórmula",
    [(VEP, 'MAX_LONGITUD_FORMULA = 2000  #', 'MAX_LONGITUD_FORMULA = 10 ** 9  #')], [B415]),
 "m18_round_negativo": ("U3: round admite decimales negativos (−12 a 12) en las dos comprobaciones",
    [(VEP, 'DECIMALES_ROUND = range(0, 13)', 'DECIMALES_ROUND = range(-12, 13)')], [B415]),
 "m19_sin_estructural": ("U4: la sensibilidad vuelve a ser solo local (sin puntos genéricos)",
    [(VEP, '    for _ in range(puntos):\n        gen = ', '    for _ in range(0):\n        gen = ')], [B415]),
 "m20_sin_constante_local": ("U4: se quita el error «constante en el punto real» (not locales)",
    [(VEP, '            if not locales:\n                return problema(k, "error", "con los valores comprobados', '            if False:\n                return problema(k, "error", "con los valores comprobados')], [B415]),
 "m21_sin_inertes": ("T2/U4: se quita el error de los orígenes inertes",
    [(VEP, '            if inertes:\n                return problema(k, "error", f"los orígenes {inertes} no influyen', '            if False:\n                return problema(k, "error", f"los orígenes {inertes} no influyen')], [B415]),
 "m22_cero_exento_en_todo": ("U4: el 0 queda exento en cualquier posición de la fórmula, no solo en min/max",
    [(VEP, '            pot10 = v > 0 and any(v == fractions.Fraction(10) ** k for k in range(-12, 13))\n            if not ((v.denominator == 1 and 1 <= v <= 12) or pot10):', '            pot10 = v > 0 and any(v == fractions.Fraction(10) ** k for k in range(-12, 13))\n            if not ((v.denominator == 1 and 0 <= v <= 12) or pot10):')], [B415]),
 "m23_sin_constantes": ("T2: se quita el control de constantes",
    [(VEP, '            if ctes:\n                return problema(k, "error", f"la fórmula escribe cifras', '            if False:\n                return problema(k, "error", f"la fórmula escribe cifras')], [B415]),
 "m24_sin_lista_derivados": ("U1: los derivados comprobados no se listan",
    [(VEP, '            out["derivados_comprobados"].append(k)', '            pass')], [B415]),
 "m25_html_sin_ocultos": ("U5: los elementos ocultos por atributo o estilo se dan por visibles",
    [(VEP, '            return (tag in HTML_SIN_TEXTO_VISIBLE or "hidden" in a or', '            return (tag in HTML_SIN_TEXTO_VISIBLE or False and "hidden" in a or')], [B415]),
 "m26_html_sin_espacios": ("U5: la cita se compara con el HTML sin espacios (como en el hito 1)",
    [(VEP, 'if _cmp_txt_espacios(f.get("cita")) not in _cmp_txt_espacios(plano):', 'if _cmp_txt(f.get("cita")) not in _cmp_txt(plano):')], [B415]),
 "m27_html_sin_charset": ("U5: no se lee el charset declarado (solo BOM o UTF-8)",
    [(VEP, '    if m:\n        cod = m.group(1)', '    if False:\n        cod = m.group(1)')], [B415]),
 "m28_html_adivina_latin1": ("U5: sin declaración y sin UTF-8 válido, se adivina ISO-8859-1",
    [(VEP, '        return None, "el HTML no declara su codificación y no es UTF-8 válido: no puede determinarse (no se adivina)"', '        return "iso-8859-1", crudo.decode("iso-8859-1")')], [B415]),
 "m29_pdf_cabecera_al_principio": ("U5: el tipo PDF vuelve a exigir la cabecera al principio (como en el hito 1)",
    [(VEP, 'if b"%PDF-" in cab[:1024] or ext.endswith(".pdf"):', 'if cab.lstrip().startswith(b"%PDF-") or ext.endswith(".pdf"):')], [B415]),
 "m30_i20_sin_bloque_ficha": ("I20: la ficha no lleva el bloque verificacion_entradas",
    [(FIP, '    ficha["verificacion_entradas"] = verificacion_y_entrada_efectiva(c, pipe)', '    pass')], [BEE, B415]),
 "m31_i20_apto_siempre_no": ("I20: la ficha dice siempre apto_por_entradas = false",
    [(FIP, 'return {"apto_por_entradas": bool(apto_e), "resumen": resumen, "apto_para_dinero_real": False,', 'return {"apto_por_entradas": False, "resumen": resumen, "apto_para_dinero_real": False,')], [BEE, B415, B414]),
 "m32_i20_apto_siempre_si": ("I20: la ficha dice siempre apto_por_entradas = true",
    [(FIP, 'return {"apto_por_entradas": bool(apto_e), "resumen": resumen, "apto_para_dinero_real": False,', 'return {"apto_por_entradas": True, "resumen": resumen, "apto_para_dinero_real": False,')], [BEE, B415, B414]),
 "m33_i20_sin_aviso_no_coincide": ("I20: el informe no avisa de que el modo aplicado no coincide con el declarado",
    [(INP, '+ ("; **el modo aplicado no coincide con el declarado**" if _ee.get("coinciden") is False else "")', '+ ""')], [BEE]),
 "m34_i20_coinciden_siempre": ("I20: la ficha dice siempre que el modo aplicado y el declarado coinciden",
    [(FIP, '"coinciden": (aplicada or {}).get("modo") == declarada.get("modo") if aplicada else None},', '"coinciden": True},')], [BEE]),
 "m35_i20_fuera_del_material": ("I20: entrada_efectiva.json no entra en el material auditado",
    [(CIP, 'MATERIAL_FIJO.append("entrada_efectiva.json")', 'pass')], [BEE]),
 "m36_i20_error_como_registrada": ("I20: una declaración ilegible se muestra como «registrada»",
    [(FIP, '        declarada = {"modo": None, "declarado_en": None, "error": str(ex)}', '        declarada = {"modo": "registrada", "declarado_en": None}')], [BEE]),
 "m37_i20_dinero_real_si": ("I20: el informe dice «Apta para dinero real: sí» si es apta por entradas",
    [(INP, '                  + ". Apta para dinero real: no.")', '                  + (". Apta para dinero real: sí." if vef.get("apto_por_entradas") else ". Apta para dinero real: no."))')], [BEE, B415, B414]),
 "m39_v64_dinero_real_si": ("informe V6.4 (párrafo de aptitud de la 4.14): dice «Apta para dinero real: sí»",
    [(INP, """f"{'sí' if ve.get('apto_por_entradas') else 'no'}. Apta para dinero real: no\"""", """f"{'sí' if ve.get('apto_por_entradas') else 'no'}. Apta para dinero real: sí\"""")], [B414, B415]),
 "m40_v64_apta_siempre_si": ("informe V6.4 (párrafo de aptitud de la 4.14): dice siempre «apta por entradas: sí»",
    [(INP, """f"{'sí' if ve.get('apto_por_entradas') else 'no'}. Apta para dinero real: no\"""", """f"{'sí' if True else 'no'}. Apta para dinero real: no\"""")], [B414, B415]),
 "m47_u1_informe_sin_derivados": ("U1: el informe V6.4 no dice cuántos derivados comprobados hay",
    [(INP, """                      + (f"{ve.get('derivados_comprobados')} derivados comprobados (significado económico: revisión independiente) · " if ve.get("derivados_comprobados") else "") + """, """                      + "" + """)], [B415]),
 "m48_i20_informe_sin_modo_declarado": ("I20: el informe no dice el modo declarado ahora ni su procedencia",
    [(INP, """                  + (f"; declarado ahora: {_de.get('modo')} ({_de.get('declarado_en') or 'sin declaración'})" if not _de.get("error") else f"; declaración actual con error: {str(_de.get('error')).replace('«', '').replace('»', '')}")""", """                  + """"")], [BEE]),
 "m38_cero_guion_sin_pagina": ("R415-SIGNO: el cero impreso como guion se busca en la cita y no en el pasaje de la página (mutación de control)",
    [(VEP, '    t = re.sub(r"[\xa0\u202f\u2009]", " ", str((_pasaje_en_pagina(cita, pagina) if pagina is not None else None) or cita or ""))', '    t = re.sub(r"[\xa0\u202f\u2009]", " ", str(cita or ""))')], [B415]),
}


def preparar(nombre):
    d = os.path.join(MUT, nombre, "munger_v2_r1")
    shutil.rmtree(os.path.join(MUT, nombre), ignore_errors=True)
    os.makedirs(os.path.join(d, "personaje_v2"))
    for x in os.listdir(COPIA):
        if x != "personaje_v2":
            os.symlink(os.path.join(COPIA, x), os.path.join(d, x))
    for x in os.listdir(os.path.join(COPIA, "personaje_v2")):
        o, n = os.path.join(COPIA, "personaje_v2", x), os.path.join(d, "personaje_v2", x)
        if x in ("scripts", "pruebas", "esquema"):
            shutil.copytree(o, n, ignore=shutil.ignore_patterns("__pycache__", "sintetico", "resultados_reparacion", "_v64"))
        elif x != ".lo_perfil":
            os.symlink(o, n)
    return d


def correr(nombre):
    desc, cambios, baterias = M[nombre]
    d = preparar(nombre)
    for arch, viejo, nuevo in cambios:
        p = os.path.join(d, "personaje_v2", arch)
        s = open(p, encoding="utf-8").read()
        if s.count(viejo) != 1:
            return {"mutacion": nombre, "descripcion": desc, "error": f"el texto a mutar aparece {s.count(viejo)} veces en {arch}"}
        open(p, "w", encoding="utf-8").write(s.replace(viejo, nuevo))
    res = {"mutacion": nombre, "descripcion": desc, "baterias": {}}
    env = dict(os.environ, PATH=os.path.join(F, "bin") + os.pathsep + os.environ["PATH"], TMPDIR=os.path.join(F, "tmp"))
    for b in baterias:
        t0 = time.time()
        sal = os.path.join(MUT, nombre, b + ".json")
        try:
            r = subprocess.run([sys.executable, "-B", os.path.join("pruebas", b), "--json", sal], cwd=os.path.join(d, "personaje_v2"), capture_output=True, text=True, env=env, timeout=1500)
            out, rc = r.stdout + r.stderr, r.returncode
        except subprocess.TimeoutExpired as ex:
            out, rc = (ex.stdout or b"").decode("utf-8", "replace") if isinstance(ex.stdout, bytes) else str(ex.stdout or ""), "TIEMPO AGOTADO (1500 s)"
        open(os.path.join(MUT, nombre, b + ".log"), "w", encoding="utf-8").write(out)
        fallan = [l[:230] for l in out.splitlines() if re.match(r"^\[[A-Za-z0-9]+\] FALLA", l)]
        m = re.search(r"(?m)^(\d+)/(\d+) pruebas", out)
        traza = [l for l in out.splitlines() if l.startswith(("Traceback", "AssertionError")) or "Error" in l[:40]][-2:]
        res["baterias"][b] = {"codigo": rc, "pasan": m.group(0) if m else None, "fallan": fallan, "traza": traza, "segundos": round(time.time() - t0)}
    shutil.rmtree(os.path.join(d, "personaje_v2", "scripts"), ignore_errors=True)  # se conserva el registro, no el árbol
    shutil.rmtree(os.path.join(d), ignore_errors=True)
    json.dump(res, open(os.path.join(MUT, nombre, "resultado.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return res


if __name__ == "__main__":
    if len(sys.argv) < 2:
        for k, v in M.items():
            print(k, "·", v[0], "·", v[2])
        sys.exit(0)
    for n in sys.argv[1:]:
        r = correr(n)
        print(json.dumps(r, ensure_ascii=False))
        sys.stdout.flush()
