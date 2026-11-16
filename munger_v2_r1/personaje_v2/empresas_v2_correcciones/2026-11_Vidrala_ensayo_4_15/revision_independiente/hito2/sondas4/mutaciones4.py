#!/usr/bin/env python3
"""Mutaciones de la CUARTA comprobación (Fable, hito 2 de la 4.15, candidata 7a6583b). Mismo arnés que mutaciones3.py: quita o altera UNA
regla del código en un árbol ligero aparte (scripts/, pruebas/ y esquema/ copiados de «copia»; el resto, enlaces) y ejecuta las baterías
permitidas (sin LibreOffice) para ver si alguna prueba lo detecta. Nunca toca el árbol congelado. Cada resultado se guarda en
mut4/<nombre>/resultado.json al terminar (un reinicio no pierde lo ya hecho; «pendientes» repite solo lo que falta).
Grupos: «t» = reglas que entran con esta candidata (T1–T4, T6–T9); «t5» = mutaciones de la tercera pasada que quedaron sin detectar y cuyas
pruebas el autor dice haber añadido ahora (N1, N3, N10, T1, T2, T4), adaptadas al código actual; «resto3» = otras de la tercera pasada sin detectar.
Uso: python3 -I -B mutaciones4.py [-j N] NOMBRE [NOMBRE …] | todas | t | t5 | resto3 | control | pendientes | lista"""
import concurrent.futures, json, os, re, shutil, subprocess, sys, time
F = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COPIA = os.path.join(F, "copia", "munger_v2_r1")
MUT = os.path.join(F, "mut4")
B415, BEE, B414 = "test_verificacion_entradas_415.py", "test_entrada_efectiva_415.py", "test_verificacion_entradas_414.py"
VEP, FHP, FIP, INP, PLP = "scripts/verificacion_entradas.py", "scripts/fase1_historia.py", "scripts/ficha.py", "scripts/informe.py", "scripts/pipeline.py"
DENTRO = '        return ventana is None or (a >= ventana[0] and b <= ventana[1])'
TC1 = r"""    tipo_cambio = (re.fullmatch(r"(?:(?:tipo de cambio|exchange rate)\b)?[\s:(]*" + m_ + r"\s*(?:por|per|/)\s*" + m_ + r"[\s)]*", t, re.I) is not None"""
TC2 = r"""                   and re.search(r"miles|millones|millares|thousand|million|billion|\bmm\b|\bbn\b|mm€|meur|keur|k€|m€|€m|€000", t, re.I) is None)"""
LIM1 = r"""    patron = ((r"(?<![\d.,])" if re.match(r"\d", palabras[0]) else r"(?<![^\W\d_])" if re.match(r"[^\W\d_]", palabras[0]) else "") + patron"""
LIM2 = r"""              + (r"(?!\d|[.,]\d)" if re.search(r"\d$", palabras[-1]) else r"(?![^\W\d_])" if re.search(r"[^\W\d_]$", palabras[-1]) else ""))"""
ENNUM1 = r"""                return ((re.match(r"\d", palabras[0]) is not None and re.search(r"[\d.,]$", t_[:m.start()]) is not None)"""
ENNUM2 = r"""                        or (re.search(r"\d$", palabras[-1]) is not None and re.match(r"\d|[.,]\d", t_[m.end():m.end() + 2]) is not None))"""
AUS_NUM = '                return "ausente", "la cita empieza o acaba dentro de una cifra de la página: no es una cifra completa de la página"'
NOLOC_PAL = '            return "no_localizada", "la cita empieza o acaba dentro de una palabra de la página: hay que citar el fragmento completo"'
MPREV = r"""        m_prev = re.search(r"(?:^|[^\w.,])(\d{1,4})$", previo) or re.search(r"(?:FY|AF|EJ)(\d{4})$", previo, re.I)"""
FECHA = r"""        fecha = re.search(r"(?:^|[^\w.,])\d{1,2}-\d{1,2}$", previo) is not None and re.fullmatch(r"\d{4}", t[ini:fin]) is not None  # «31-12-2024»"""
INTERV = r"""        if m.group(1) == "" and (fecha or (m_prev and re.fullmatch(r"\d{1,4}", t[ini:fin]) and len(m_prev.group(1)) == len(t[ini:fin]))):"""
XHTML = '            self.xhtml = str(ruta).lower().endswith((".xhtml", ".xht"))'
CODECS = """        elif nombre in ("utf-7",) or not (nombre.startswith(("utf-", "cp125", "iso8859-", "koi8")) or nombre in CODECS_TEXTO_HTML):  # (hito 2, T3) lista explícita"""
HTMLTF = '            textos_fuente.append(re.sub("[' + "".join(chr(92) + "u" + x for x in ("00ad", "200b", "200c", "200d", "2060", "feff")) + ']", "", plano))  # (T4) sin caracteres invisibles'
LECT = '            lect = [_cita_cifra(f.get("cita"), vf, tf) for tf in textos_fuente]'
OTRAS = '            otras = [x for x in lect if x[0] != "no_localizada"]'
PEOR = '            peor = next((x for x in otras if x[0] in ("signo_distinto", "ausente")), None) or next((x for x in otras if x[0] != "ok"), None)'
T4ELIF = '            elif lect and not otras:'
EDIC = r"""                                                              or _ediciones(re.sub(r"[^a-z]", "", str(k).lower()), "entradaefectiva") <= 3)]"""
T7 = '    if motivo_modo and isinstance(resumen, dict):\n        resumen = dict(resumen, apto_por_entradas=False)  # (hito 2, T7) el resumen no contradice al bloque\n'
BLOQUE2 = '            or isinstance((pipe or {}).get("entrada_efectiva"), dict) or _declara_modo(c)):'

# nombre: (grupo, hallazgo, descripción, [(archivo, texto original, texto nuevo)], [baterías])
M = {
 "c00_control": ("control", "—", "control: sin cambio de regla (solo un comentario); las baterías tienen que pasar enteras en el árbol ligero",
    [(VEP, 'FORMATO = "4.15"', 'FORMATO = "4.15"  # control')], [BEE, B414, B415]),
 # ================================================================ T1 · exención del tipo de cambio (U7)
 "t1a_exencion_antigua": ("t", "T1", "la exención vuelve a decidirse por subcadenas («tipo de cambio», «exchange rate» o una moneda tras «por», «per» o «/»), como en f3d15e8",
    [(VEP, TC1 + "\n" + TC2, '    tipo_cambio = re.search(r"(por|per|/)\\s*" + m_, t, re.I) is not None or "tipo de cambio" in t or "exchange rate" in t')], [B415]),
 "t1b_search_en_vez_de_fullmatch": ("t", "T1", "el par de monedas ya no tiene que ser la unidad ENTERA (search en vez de fullmatch): «importe en USD por EUR al cierre» queda exento",
    [(VEP, TC1, TC1.replace("re.fullmatch(", "re.search("))], [B415]),
 "t1c_sin_palabra_de_escala": ("t", "T1", "se quita la condición «sin palabra de escala» («meur/keur», «k€/usd» quedan exentos)",
    [(VEP, TC2, "                   and True)")], [B415]),
 "t1d_sin_exencion": ("t", "T1/N9", "sin exención: un tipo de cambio («USD por EUR») vuelve a ser una unidad monetaria no reconocida",
    [(VEP, TC1 + "\n" + TC2, "    tipo_cambio = False")], [B415]),
 # ================================================================ T2 · límites del fragmento de la cita y clasificación de la cita cortada
 "t2a_limites_antiguos": ("t", "T2", "los límites de la cita vuelven a ser los de f3d15e8 (\\w a los dos lados: «849.7» no cuenta en «849.7m»)",
    [(VEP, LIM1 + "\n" + LIM2, '    patron = (r"(?<![\\w.,])" if re.match(r"\\w", palabras[0]) else "") + patron + (r"(?!\\w|[.,]\\d)" if re.search(r"\\w$", palabras[-1]) else "")')], [B415, BEE]),
 "t2b_sin_limite_inicial_cifra": ("t", "T2", "una cita que empieza por una cifra puede empezar dentro de un número de la página (sin el límite inicial de cifra)",
    [(VEP, LIM1, LIM1.replace('(r"(?<![\\d.,])" if re.match(r"\\d", palabras[0]) else ', '("" if re.match(r"\\d", palabras[0]) else '))], [B415, BEE]),
 "t2c_sin_limite_inicial_letra": ("t", "T2", "una cita que empieza por una letra puede empezar dentro de una palabra de la página («otal 5» en «Total 5»)",
    [(VEP, LIM1, LIM1.replace('r"(?<![^\\W\\d_])" if re.match(r"[^\\W\\d_]", palabras[0]) else ""', '""'))], [B415, BEE]),
 "t2d_sin_limite_final_cifra": ("t", "T2", "una cita que acaba en una cifra puede acabar dentro de un número de la página (sin el límite final de cifra)",
    [(VEP, LIM2, LIM2.replace('(r"(?!\\d|[.,]\\d)" if re.search(r"\\d$", palabras[-1]) else ', '("" if re.search(r"\\d$", palabras[-1]) else '))], [B415, BEE]),
 "t2e_sin_limite_final_letra": ("t", "T2", "una cita que acaba en una letra puede acabar dentro de una palabra de la página («849,7 mill» en «849,7 millones»)",
    [(VEP, LIM2, LIM2.replace('r"(?![^\\W\\d_])" if re.search(r"[^\\W\\d_]$", palabras[-1]) else ""', '""'))], [B415, BEE]),
 "t2f_palabra_cortada_ausente": ("t", "T2", "una cita cortada dentro de una PALABRA vuelve a ser «ausente» (discrepancia) en vez de pendiente",
    [(VEP, NOLOC_PAL, '            return "ausente", "MUTACIÓN"')], [B415]),
 "t2g_numero_cortado_pendiente": ("t", "T2/R3", "una cita cortada dentro de un NÚMERO deja de ser «ausente» (discrepancia): queda «no_localizada» (pendiente)",
    [(VEP, AUS_NUM, '                return "no_localizada", "MUTACIÓN"')], [B415, BEE]),
 "t2h_en_numero_sin_inicio": ("t", "T2", "el corte dentro de un número solo se mira al FINAL de la cita (una cita que empieza dentro de un número queda pendiente, no discrepancia)",
    [(VEP, ENNUM1 + "\n" + ENNUM2, "                return (False\n" + ENNUM2)], [B415]),
 "t2i_en_numero_sin_final": ("t", "T2", "el corte dentro de un número solo se mira al PRINCIPIO de la cita (una cita que acaba dentro de un número queda pendiente, no discrepancia)",
    [(VEP, ENNUM1 + "\n" + ENNUM2, ENNUM1 + ")")], [B415]),
 # ================================================================ T3 · XHTML por extensión y lista de códecs
 "t3a_xhtml_por_contenido": ("t", "T3", "el modo XHTML vuelve a decidirse por el contenido (<?xml o el xmlns en los primeros 4.096 caracteres), como en f3d15e8",
    [(VEP, XHTML, """            cab = texto[:4096].lower()\n            self.xhtml = cab.lstrip().startswith("<?xml") or 'xmlns="http://www.w3.org/1999/xhtml"' in cab""")], [B415]),
 "t3b_xhtml_nunca": ("t", "T3/N6", "se quita el modo XHTML (un elemento autocerrado no vacío de un .xhtml vuelve a ocultar lo que sigue)",
    [(VEP, XHTML, "            self.xhtml = False")], [B415]),
 "t3c_xhtml_siempre": ("t", "T3/N6", "todo documento se trata como XHTML (en un .html, «<div hidden/>» deja de ocultar lo que sigue)",
    [(VEP, XHTML, "            self.xhtml = True")], [B415]),
 "t3d_codecs_por_prefijos": ("t", "T3", "la lista de codificaciones vuelve a ser por prefijos («cp4», «cp8», «euc_», «iso2022_», «mac-»), como en f3d15e8 (cp875 e iso-2022-kr vuelven a leerse)",
    [(VEP, CODECS, """        elif nombre == "utf-7" or not (nombre.startswith(("utf-", "cp125", "cp4", "cp8", "iso8859-", "mac-", "koi8", "euc_", "iso2022_")) or nombre in ("shift_jis", "gb2312", "gbk", "gb18030", "big5", "big5hkscs")):""")], [B415]),
 "t3e_sin_lista_de_codecs": ("t", "T3/N6", "solo se admiten utf-*, cp125*, iso8859-* y koi8 (ibm850 y euc-kr vuelven a quedar pendientes)",
    [(VEP, CODECS, CODECS.replace(" or nombre in CODECS_TEXTO_HTML", ""))], [B415]),
 # ================================================================ T4 · la cita no se localiza con sus palabras en el documento
 "t4a_sin_pendiente": ("t", "T4", "si la cita no se localiza con sus palabras en ningún texto del documento, la lectura vuelve a omitirse en silencio",
    [(VEP, T4ELIF, "            elif False:")], [B415]),
 "t4b_html_con_invisibles": ("t", "T4", "el texto del HTML se lee sin quitar los guiones blandos ni los caracteres de ancho cero",
    [(VEP, HTMLTF, "            textos_fuente.append(plano)")], [B415]),
 "t4c_pendiente_aunque_un_texto_lea": ("t", "T4", "control inverso: basta que UN texto del documento no localice la cita para dejarla pendiente (aunque el otro la lea «ok»)",
    [(VEP, T4ELIF, "            elif lect and len(otras) < len(lect):")], [B415]),
 # ================================================================ T8 · intervalos y fechas
 "t8a_intervalo_sin_misma_longitud": ("t", "T8", "el intervalo ya no exige que los dos enteros tengan la misma longitud («2023-849» vuelve a leerse como intervalo: positivo)",
    [(VEP, INTERV, INTERV.replace(" and len(m_prev.group(1)) == len(t[ini:fin])", ""))], [B415]),
 "t8b_sin_prefijo_fy": ("t", "T8", "sin el prefijo FY/AF/EJ: «FY2023-2024» vuelve a quedar pendiente",
    [(VEP, MPREV, MPREV.replace(""" or re.search(r"(?:FY|AF|EJ)(\\d{4})$", previo, re.I)""", ""))], [B415]),
 "t8c_sin_fecha": ("t", "T8", "sin la regla de la fecha: «31-12-2024» deja de leerse como fecha",
    [(VEP, FECHA, "        fecha = False")], [B415]),
 "t8d_fecha_cualquier_cifra": ("t", "T8", "la regla de la fecha vale para cualquier cifra que siga a «d-m-» (no solo un año de cuatro cifras): «5-6-849,7» se lee en positivo",
    [(VEP, FECHA, FECHA.replace(""" and re.fullmatch(r"\\d{4}", t[ini:fin]) is not None""", ""))], [B415]),
 # ================================================================ T6 · umbral de erratas por distancia de edición (pipeline.py)
 "t6a_sin_distancia_de_edicion": ("t", "T6", "se quita la distancia de edición: las erratas dobles («emtrada_efectiba») vuelven a dejar el modo en «registrada» en silencio",
    [(PLP, " >= 0.88\n" + EDIC, " >= 0.88)]")], [BEE]),
 "t6b_distancia_1": ("t", "T6", "la distancia de edición admitida baja a 1 (las erratas dobles que no llegan a 0,88 dejan de detectarse)",
    [(PLP, EDIC, EDIC.replace("<= 3)]", "<= 1)]"))], [BEE]),
 "t6c_distancia_5": ("t", "T6", "control inverso: la distancia sube a 5 («tasa_efectiva», a 4, vuelve a ser una errata)",
    [(PLP, EDIC, EDIC.replace("<= 3)]", "<= 5)]"))], [BEE]),
 # ================================================================ T7 · resumen del bloque de I20 (ficha.py)
 "t7a_resumen_sin_actualizar": ("t", "T7", "con el modo distinto, el resumen del bloque de I20 vuelve a decir apto_por_entradas = true",
    [(FIP, T7, "")], [BEE, B415]),
 # ================================================================ T9 · relevo (pipeline.py) — ninguna de las tres baterías permitidas ejecuta el paso 13
 "t9a_refijar_sin_bandera": ("t", "T9", "material_refijado vuelve a anotarse en el último relevo sin él, sin mirar la bandera «relevo_por_refijar»",
    [(PLP, '                            and st.pop("relevo_por_refijar", False)):', "                            and True):")], [BEE]),
 "t9b_archivos_sin_convertir": ("t", "T9", "los archivos cambiados del relevo dejan de convertirse a texto (una lista con algo que no es texto vuelve a dar TypeError)",
    [(PLP, "            _arch = [str(x) for x in _arch] if isinstance(_arch, list) else [str(_arch)]  # (hito 2, T9) un registro mal formado no detiene nada", "            _arch = _arch or []")], [BEE]),
 # ================================================================ T5 · mutaciones de la 3.ª pasada sin detectar cuyas pruebas el autor dice haber añadido (N1, N3, N10, T1, T2, T4)
 "n1b_sin_declara_modo": ("t5", "N1", "el bloque de I20 deja de depender del modo declarado en alcance_v2.json o fase1_metadatos.json",
    [(FIP, BLOQUE2, '            or isinstance((pipe or {}).get("entrada_efectiva"), dict)):')], [BEE]),
 "n1c_ilegible_no_declara": ("t5", "N1", "un alcance_v2.json o fase1_metadatos.json ilegible deja de hacer que se muestre el bloque",
    [(FIP, '            except (OSError, ValueError):\n                return True', '            except (OSError, ValueError):\n                continue')], [BEE]),
 "n3b_html_no_se_lee": ("t5", "N3", "la lectura adicional se hace en el PDF pero no en el HTML",
    [(VEP, '        if est_h == "ok":\n' + HTMLTF, '        if False:\n' + HTMLTF)], [B415]),
 "n3c_solo_signo_distinto": ("t5", "N3", "del documento solo cuenta un signo distinto (una cifra ausente o un signo indeterminado en el documento se ignoran)",
    [(VEP, PEOR, '            peor = next((x for x in otras if x[0] in ("signo_distinto",)), None)')], [B415]),
 "n3d_solo_layout": ("t5", "N3", "del PDF solo se lee el texto con «-layout» (no el del orden de lectura)",
    [(VEP, '        textos_fuente += [txt_pdf, txt_pdf2]', '        textos_fuente += [txt_pdf]')], [B415]),
 "n3e_solo_sin_layout": ("t5", "N3", "del PDF solo se lee el texto sin «-layout»",
    [(VEP, '        textos_fuente += [txt_pdf, txt_pdf2]', '        textos_fuente += [txt_pdf2]')], [B415]),
 "n10c_sin_recorte_400": ("t5", "N10", "se quita el recorte del contexto a 400 caracteres (coste con una línea muy larga)",
    [(VEP, '        ini, fin = max(ini, m.start() - 400), min(fin, m.end() + 400)', '        ini, fin = ini, fin')], [B415]),
 "n9c_cualquier_barra_o_por": ("t5", "T1/N9", "control inverso de la 3.ª pasada: la exención del tipo de cambio se amplía a cualquier unidad con una barra o «por» («€/MWh», «EUR por tonelada»)",
    [(VEP, TC1 + "\n" + TC2, '    tipo_cambio = re.search(r"(por|per|/)", t, re.I) is not None or "tipo de cambio" in t or "exchange rate" in t')], [B415]),
 "n4_solapa": ("t5", "N4", "la cifra vuelve a valer con que la cita la TOQUE (solapamiento), sin tener que estar dentro",
    [(VEP, DENTRO, '        return ventana is None or (a < ventana[1] and b > ventana[0])')], [B415, BEE]),
 # ================================================================ otras de la 3.ª pasada que quedaron sin detectar (el autor no dice haberlas cubierto)
 "n5c_sin_limite_antes": ("resto3", "N5", "el intervalo ya no exige que el entero anterior al guion sea un número completo («T4-15» o «1.234-567» se leen como intervalo)",
    [(VEP, MPREV, MPREV.replace('re.search(r"(?:^|[^\\w.,])(\\d{1,4})$", previo)', 're.search(r"(\\d{1,4})$", previo)'))], [B415]),
 "n2c_motivos_sin_modo": ("resto3", "N2", "con el modo distinto, motivos_no_apto no da el motivo (apto_e no se pone a False; el resumen sí)",
    [(FIP, '        apto_e = False\n        resumen = dict(resumen, apto_por_entradas=False', '        resumen = dict(resumen, apto_por_entradas=False')], [B415]),
 "h9d_error_declaracion_no_impide": ("resto3", "H9/N7", "una declaración del modo con error deja de impedir «apto por entradas»",
    [(FIP, """tiene un error: {declarada.get('error')}" if declarada.get("error")""", """tiene un error: {declarada.get('error')}" if False""")], [BEE, B415]),
 "u6g_umbral_092": ("resto3", "N9/U6", "el umbral de parecido sube a 0,92 (con la distancia de edición ≤ 3 que entra ahora)",
    [(PLP, '.ratio() >= 0.88', '.ratio() >= 0.92')], [BEE]),
}


def preparar(nombre):
    d = os.path.join(MUT, nombre, "munger_v2_r1")
    if os.path.lexists(os.path.join(MUT, nombre)):
        shutil.rmtree(os.path.join(MUT, nombre))
    os.makedirs(os.path.join(d, "personaje_v2"))
    for x in os.listdir(COPIA):
        if x != "personaje_v2":
            os.symlink(os.path.realpath(os.path.join(COPIA, x)), os.path.join(d, x))
    for x in os.listdir(os.path.join(COPIA, "personaje_v2")):
        o, n = os.path.join(COPIA, "personaje_v2", x), os.path.join(d, "personaje_v2", x)
        if x in ("scripts", "pruebas", "esquema"):
            shutil.copytree(o, n, ignore=shutil.ignore_patterns("__pycache__", "sintetico", "resultados_reparacion", "_v64"))
        elif x != ".lo_perfil":
            os.symlink(os.path.realpath(o), n)
    return d


def comprobar_textos():
    """Cada texto a mutar aparece exactamente una vez en la copia (sin ejecutar nada)."""
    mal = []
    for nombre, (_g, _h, _desc, cambios, _b) in M.items():
        for arch, viejo, nuevo in cambios:
            s = open(os.path.join(COPIA, "personaje_v2", arch), encoding="utf-8").read()
            if s.count(viejo) != 1 or viejo == nuevo:
                mal.append((nombre, arch, s.count(viejo)))
    return mal


def correr(nombre):
    grupo, hall, desc, cambios, baterias = M[nombre]
    d = preparar(nombre)
    for arch, viejo, nuevo in cambios:
        p = os.path.join(d, "personaje_v2", arch)
        s = open(p, encoding="utf-8").read()
        if s.count(viejo) != 1:
            return {"mutacion": nombre, "hallazgo": hall, "descripcion": desc, "error": f"el texto a mutar aparece {s.count(viejo)} veces en {arch}"}
        open(p, "w", encoding="utf-8").write(s.replace(viejo, nuevo))
    res = {"mutacion": nombre, "grupo": grupo, "hallazgo": hall, "descripcion": desc, "baterias": {}}
    tmp = os.path.join(F, "tmp", "mut4_" + nombre)
    os.makedirs(tmp, exist_ok=True)
    env = dict(os.environ, PATH=os.path.join(F, "bin") + os.pathsep + os.environ["PATH"], TMPDIR=tmp, PYTHONDONTWRITEBYTECODE="1")
    for b in baterias:
        t0 = time.time()
        sal = os.path.join(MUT, nombre, b + ".json")
        try:
            r = subprocess.run(["nice", "-n", "15", sys.executable, "-B", os.path.join("pruebas", b), "--json", sal], cwd=os.path.join(d, "personaje_v2"), capture_output=True, text=True, env=env, timeout=3600)
            out, rc = r.stdout + r.stderr, r.returncode
        except subprocess.TimeoutExpired as ex:
            out, rc = (ex.stdout or b"").decode("utf-8", "replace") if isinstance(ex.stdout, bytes) else str(ex.stdout or ""), "TIEMPO AGOTADO (3600 s)"
        open(os.path.join(MUT, nombre, b + ".log"), "w", encoding="utf-8").write(out)
        fallan = [l[:300] for l in out.splitlines() if re.match(r"^\[[A-Za-z0-9]+\] FALLA", l)]
        m = re.search(r"(?m)^(\d+)/(\d+) pruebas", out)
        traza = [l[:200] for l in out.splitlines() if l.startswith(("Traceback", "AssertionError")) or "Error" in l[:40]][-2:]
        res["baterias"][b] = {"codigo": rc, "pasan": m.group(0) if m else None, "fallan": fallan, "traza": traza, "segundos": round(time.time() - t0)}
    shutil.rmtree(d, ignore_errors=True)  # se conserva el registro, no el árbol
    shutil.rmtree(tmp, ignore_errors=True)
    json.dump(res, open(os.path.join(MUT, nombre, "resultado.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return res


if __name__ == "__main__":
    args = sys.argv[1:]
    j = 1
    if args[:1] == ["-j"]:
        j, args = int(args[1]), args[2:]
    mal = comprobar_textos()
    if mal:
        print("TEXTOS QUE NO APARECEN EXACTAMENTE UNA VEZ:", mal)
        sys.exit(2)
    if not args or args == ["lista"]:
        for k, v in M.items():
            print(k, "·", v[0], "·", v[1], "·", v[2], "·", v[4])
        print(len(M), "mutaciones; textos comprobados")
        sys.exit(0)
    if args == ["todas"]:
        nombres = list(M)
    elif len(args) == 1 and args[0] in ("t", "t5", "resto3", "control"):
        nombres = [k for k, v in M.items() if v[0] == args[0]]
    elif args == ["pendientes"]:
        nombres = [k for k in M if not os.path.exists(os.path.join(MUT, k, "resultado.json"))]
    else:
        nombres = args
    with concurrent.futures.ThreadPoolExecutor(max_workers=j) as ex:
        for r in ex.map(correr, nombres):
            print(json.dumps(r, ensure_ascii=False))
            sys.stdout.flush()
