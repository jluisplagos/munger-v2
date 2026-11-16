#!/usr/bin/env python3
"""Mutaciones de la TERCERA pasada (Fable, hito 2 de la 4.15, candidata f3d15e8). Como mutaciones2.py de la segunda pasada: quita o altera
UNA regla del código en un árbol ligero aparte (scripts/, pruebas/ y esquema/ copiados de «copia»; el resto, enlaces) y ejecuta las baterías
permitidas (sin LibreOffice) para ver si alguna prueba lo detecta. Nunca toca el árbol congelado.
Grupos: reglas NUEVAS de esta candidata (N1–N6, N9, N10) y las mutaciones de la segunda pasada que el autor dice haber cubierto ahora
(h1g, h9a, h9d, m12, m16, m17, m20, m22, m29 = h7k y H6 ±), más las que la segunda pasada dejó sin detectar y el autor no dice haber cubierto.
Uso: python3 -I -B mutaciones3.py [-j N] NOMBRE [NOMBRE …] | todas | nuevas | cubiertas | resto | lista"""
import concurrent.futures, json, os, re, shutil, subprocess, sys, time
F = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COPIA = os.path.join(F, "copia", "munger_v2_r1")
MUT = os.path.join(F, "mut3")
B415, BEE, B414 = "test_verificacion_entradas_415.py", "test_entrada_efectiva_415.py", "test_verificacion_entradas_414.py"
VEP, FHP, FIP, INP, PLP = "scripts/verificacion_entradas.py", "scripts/fase1_historia.py", "scripts/ficha.py", "scripts/informe.py", "scripts/pipeline.py"
ESQ = "esquema/ficha.esquema.json"
DENTRO = '        return ventana is None or (a >= ventana[0] and b <= ventana[1])'
INTERV = '        if m.group(1) == "" and re.search(r"(?:^|[^\\w.,])\\d{1,4}$", previo) and re.fullmatch(r"\\d{1,4}", t[ini:fin]):'
LIMITES = '    patron = (r"(?<![\\w.,])" if re.match(r"\\w", palabras[0]) else "") + patron + (r"(?!\\w|[.,]\\d)" if re.search(r"\\w$", palabras[-1]) else "")'
OTRAS = '            otras = [x for x in (_cita_cifra(f.get("cita"), vf, tf) for tf in textos_fuente) if x[0] != "no_localizada"]'
PEOR = '            peor = next((x for x in otras if x[0] in ("signo_distinto", "ausente")), None) or next((x for x in otras if x[0] != "ok"), None)'
XHTML = """            self.xhtml = cab.lstrip().startswith("<?xml") or 'xmlns="http://www.w3.org/1999/xhtml"' in cab"""
TRAT = """            if sig == -1 and re.sub(r"[\\s.,;:()¡!¿?«»\\"']+", " ", _norm_txt(f.get("tratamiento"))).strip() in ("", "ninguno", "ninguna", "-", "—", "no", "n/a", "na", "sin tratamiento", "none"):"""
BLOQUE2 = '            or isinstance((pipe or {}).get("entrada_efectiva"), dict) or _declara_modo(c)):'
SUELO = '            if not locales and not (r_ex == 0 and _suelo_cero(d["formula"])):'
OCULTO = '            return (tag in HTML_SIN_TEXTO_VISIBLE or "hidden" in a or "display:none" in st'
TIPO_PDF = '    if cab.lstrip().startswith(b"%PDF-") or ext.endswith(".pdf") or (b"%PDF-" in cab[:1024] and not texto_o_html):'
APTO_FI = '    return {"apto_por_entradas": bool(apto_e) and motivo_modo is None, "resumen": resumen, "apto_para_dinero_real": False,'

# nombre: (grupo, hallazgo, descripción, [(archivo, texto original, texto nuevo)], [baterías])
M = {
 "c00_control": ("control", "—", "control: sin cambio de regla (solo un comentario); las baterías tienen que pasar enteras en el árbol ligero",
    [(VEP, 'FORMATO = "4.15"', 'FORMATO = "4.15"  # control')], [BEE, B414, B415]),
 # ================================================================ reglas NUEVAS de la tercera candidata
 "n4_solapa": ("nuevas", "N4", "la cifra vuelve a valer con que la cita la TOQUE (solapamiento), sin tener que estar dentro",
    [(VEP, DENTRO, '        return ventana is None or (a < ventana[1] and b > ventana[0])')], [B415, BEE]),
 "n5a_intervalo_cualquiera": ("nuevas", "N5", "cualquier guion pegado entre dos cifras vuelve a leerse como intervalo (+1), como antes de la corrección",
    [(VEP, INTERV, '        if m.group(1) == "" and re.search(r"\\d$", previo):')], [B415]),
 "n5b_sin_entero_despues": ("nuevas", "N5", "el intervalo ya no exige que la cifra que sigue al guion sea un entero de 1 a 4 dígitos («2023-849,7» vuelve a ser positivo)",
    [(VEP, INTERV, '        if m.group(1) == "" and re.search(r"(?:^|[^\\w.,])\\d{1,4}$", previo):')], [B415]),
 "n5c_sin_limite_antes": ("nuevas", "N5", "el intervalo ya no exige que el entero anterior al guion sea un número completo («T4-15» o «1.234-567» se leen como intervalo)",
    [(VEP, INTERV, '        if m.group(1) == "" and re.search(r"\\d{1,4}$", previo) and re.fullmatch(r"\\d{1,4}", t[ini:fin]):')], [B415]),
 "n10a_sin_limites": ("nuevas", "N10", "la cita vuelve a buscarse como subcadena (sin límites de fragmento completo ni al principio ni al final)",
    [(VEP, LIMITES, '    patron = patron + ""')], [B415, BEE]),
 "n10a1_sin_limite_inicial": ("nuevas", "N10", "la cita puede empezar dentro de una palabra o de una cifra de la página (sin el límite inicial)",
    [(VEP, LIMITES, '    patron = patron + (r"(?!\\w|[.,]\\d)" if re.search(r"\\w$", palabras[-1]) else "")')], [B415, BEE]),
 "n10a2_sin_limite_final": ("nuevas", "N10", "la cita puede acabar dentro de una palabra o de una cifra de la página (sin el límite final)",
    [(VEP, LIMITES, '    patron = (r"(?<![\\w.,])" if re.match(r"\\w", palabras[0]) else "") + patron')], [B415, BEE]),
 "n10b_cierre_sin_apertura": ("nuevas", "N10", "«cifra)» sin «(» en la línea vuelve a leerse como positivo",
    [(VEP, '    if re.match(r"\\s*\\)", despues) and "(" not in antes:\n        return None  # (hito 2, N10)', '    if False:\n        return None  # (hito 2, N10)')], [B415]),
 "n10c_sin_recorte_400": ("nuevas", "N10", "se quita el recorte del contexto a 400 caracteres (coste con una línea muy larga)",
    [(VEP, '        ini, fin = max(ini, m.start() - 400), min(fin, m.end() + 400)', '        ini, fin = ini, fin')], [B415]),
 "n10d_cortada_no_localizada": ("nuevas", "N10/R3", "una cita que solo está como fragmento de una palabra o de una cifra vuelve a ser «no_localizada» (pendiente), no «ausente» (discrepancia)",
    [(VEP, '            return "ausente", "la cita empieza o acaba dentro de una palabra o de una cifra de la página: no es una cifra completa de la página"',
      '            return "no_localizada", "MUTACIÓN"')], [B415, BEE]),
 "n3a_sin_lectura_documento": ("nuevas", "N3", "la cifra y su signo dejan de leerse en el PDF o el HTML (solo en el texto conservado, como antes)",
    [(VEP, OTRAS, '            otras = []')], [B415]),
 "n3b_html_no_se_lee": ("nuevas", "N3", "la lectura adicional se hace en el PDF pero no en el HTML",
    [(VEP, '        if est_h == "ok":\n            textos_fuente.append(plano)', '        if False:\n            textos_fuente.append(plano)')], [B415]),
 "n3c_solo_signo_distinto": ("nuevas", "N3", "del documento solo cuenta un signo distinto (una cifra ausente o un signo indeterminado en el documento se ignoran)",
    [(VEP, PEOR, '            peor = next((x for x in otras if x[0] in ("signo_distinto",)), None)')], [B415]),
 "n3d_solo_layout": ("nuevas", "N3", "del PDF solo se lee el texto con «-layout» (no el del orden de lectura)",
    [(VEP, '        textos_fuente += [txt_pdf, txt_pdf2]', '        textos_fuente += [txt_pdf]')], [B415]),
 "n3e_solo_sin_layout": ("nuevas", "N3", "del PDF solo se lee el texto sin «-layout»",
    [(VEP, '        textos_fuente += [txt_pdf, txt_pdf2]', '        textos_fuente += [txt_pdf2]')], [B415]),
 "n6a_sin_xhtml": ("nuevas", "N6", "se quita el modo XHTML (un elemento autocerrado no vacío vuelve a ocultar lo que sigue)",
    [(VEP, XHTML, '            self.xhtml = False')], [B415]),
 "n6b_summary_hidden_visible": ("nuevas", "N6", "un <summary hidden> de un <details> cerrado vuelve a darse por visible",
    [(VEP, '            if tag == "summary" and not self._es_oculto(tag, attrs):  # (hito 2, N6)', '            if tag == "summary":  # (hito 2, N6)')], [B415]),
 "n6c_sin_codecs_nuevos": ("nuevas", "N6", "ibm850, cp866, cp874, euc-kr e iso-2022 vuelven a quedar pendientes",
    [(VEP, '"cp125", "cp4", "cp8", "iso8859-", "mac-", "koi8", "euc_", "iso2022_"', '"cp125", "iso8859-", "mac-", "koi8"')], [B415]),
 "n6d_xhtml_siempre": ("nuevas", "N6", "todo documento se trata como XHTML (en HTML, «<div hidden/>» deja de ocultar lo que sigue)",
    [(VEP, XHTML, '            self.xhtml = True')], [B415]),
 "n9a_sin_tipo_cambio": ("nuevas", "N9", "un tipo de cambio («USD por EUR») vuelve a ser una unidad monetaria no reconocida",
    [(VEP, '    tipo_cambio = re.search(r"(por|per|/)\\s*" + MARCAS_MONEDA.pattern, t, re.I) is not None or "tipo de cambio" in t or "exchange rate" in t', '    tipo_cambio = False')], [B415]),
 "n9b_tratamiento_literal": ("nuevas", "N9", "el tratamiento vuelve a compararse literalmente («Ninguno.» pasa)",
    [(VEP, TRAT, '            if sig == -1 and _norm_txt(f.get("tratamiento")) in ("", "ninguno", "ninguna", "-", "—", "no", "n/a", "na", "sin tratamiento", "none"):')], [B415]),
 "n9c_cualquier_mencion_tipo_cambio": ("nuevas", "N9", "control inverso: la exención del tipo de cambio se amplía a cualquier unidad con una barra o «por» («€/MWh», «EUR por tonelada» dejan de quedar pendientes)",
    [(VEP, '    tipo_cambio = re.search(r"(por|per|/)\\s*" + MARCAS_MONEDA.pattern, t, re.I) is not None or "tipo de cambio" in t or "exchange rate" in t',
      '    tipo_cambio = re.search(r"(por|per|/)", t, re.I) is not None or "tipo de cambio" in t or "exchange rate" in t')], [B415]),
 "n1a_sin_senal_estado": ("nuevas", "N1", "el bloque de I20 deja de depender del modo registrado por el paso 2 en estado_pipeline.json",
    [(FIP, BLOQUE2, '            or _declara_modo(c)):')], [BEE]),
 "n1b_sin_declara_modo": ("nuevas", "N1", "el bloque de I20 deja de depender del modo declarado en alcance_v2.json o fase1_metadatos.json",
    [(FIP, BLOQUE2, '            or isinstance((pipe or {}).get("entrada_efectiva"), dict)):')], [BEE]),
 "n1c_ilegible_no_declara": ("nuevas", "N1", "un alcance_v2.json o fase1_metadatos.json ilegible deja de hacer que se muestre el bloque",
    [(FIP, '            except (OSError, ValueError):\n                return True', '            except (OSError, ValueError):\n                continue')], [BEE]),
 "n2a_aptitud_sin_modo": ("nuevas", "N2", "aptitud_de_uso vuelve a ignorar el motivo del modo (el párrafo de la V6.4 dice «sí» con el modo distinto)",
    [(FIP, '    if motivo_modo:\n        # (4.15, hito 2, N2)', '    if False:\n        # (4.15, hito 2, N2)')], [B415, BEE]),
 "n2b_resumen_sin_actualizar": ("nuevas", "N2", "con el modo distinto, el resumen de aptitud_de_uso sigue diciendo apto_por_entradas = true (solo cambia el motivo)",
    [(FIP, """        resumen = dict(resumen, apto_por_entradas=False, motivo=f"{resumen.get('motivo') or ''} {motivo_modo}".strip())""",
      """        resumen = dict(resumen, motivo=f"{resumen.get('motivo') or ''} {motivo_modo}".strip())""")], [B415]),
 "n2c_motivos_sin_modo": ("nuevas", "N2", "con el modo distinto, motivos_no_apto no da el motivo (apto_e no se pone a False; el resumen sí)",
    [(FIP, '        apto_e = False\n        resumen = dict(resumen, apto_por_entradas=False', '        resumen = dict(resumen, apto_por_entradas=False')], [B415]),
 "u6e_umbral_080": ("nuevas", "N9/U6", "el umbral de erratas de la clave vuelve a 0,8 («tasa_efectiva» vuelve a ser un error)",
    [(PLP, '.ratio() >= 0.88]', '.ratio() >= 0.8]')], [BEE]),
 "u6f_umbral_097": ("nuevas", "N9/U6", "el umbral de erratas sube a 0,97 (una errata de una letra, «entrada_efectiba», deja de detectarse)",
    [(PLP, '.ratio() >= 0.88]', '.ratio() >= 0.97]')], [BEE]),
 "u6g_umbral_092": ("nuevas", "N9/U6", "el umbral de erratas sube a 0,92 (dos erratas o una clave con sufijo dejan de detectarse; una letra, todavía)",
    [(PLP, '.ratio() >= 0.88]', '.ratio() >= 0.92]')], [BEE]),
 # ================================================================ mutaciones de la 2.ª pasada que el autor dice haber cubierto (N7)
 "h1g_calc_sin_pagina": ("cubiertas", "H1/N7", "calcular_entrada lee la cifra y el signo del componente en la cita, no en la página",
    [(FHP, 'est_c, det_c = VE._cita_cifra(cmp.get("cita"), publicado, pag)', 'est_c, det_c = VE._cita_cifra(cmp.get("cita"), publicado)')], [BEE]),
 "h9a_modo_distinto_no_impide": ("cubiertas", "H9/N7", "un modo aplicado distinto del declarado (o una declaración con error) deja de impedir «apto por entradas» en el bloque de I20",
    [(FIP, APTO_FI, '    return {"apto_por_entradas": bool(apto_e), "resumen": resumen, "apto_para_dinero_real": False,')], [BEE, B415]),
 "h9d_error_declaracion_no_impide": ("cubiertas", "H9/N7", "una declaración del modo con error deja de impedir «apto por entradas»",
    [(FIP, """tiene un error: {declarada.get('error')}" if declarada.get("error")""", """tiene un error: {declarada.get('error')}" if False""")], [BEE, B415]),
 "m12_tolerancia_0_00055": ("cubiertas", "H11", "(m12) tolerancia de importes ampliada a 0,00055",
    [(VEP, 'abs(exacto - fv) <= fractions.Fraction(1, 2000)', 'abs(exacto - fv) <= fractions.Fraction(11, 20000)')], [B415]),
 "m16_sin_limite_nodos": ("cubiertas", "H11", "(m16) sin límite de nodos de la fórmula",
    [(VEP, 'MAX_NODOS_FORMULA = 400', 'MAX_NODOS_FORMULA = 10 ** 9')], [B415]),
 "m17_sin_limite_longitud": ("cubiertas", "H11", "(m17) sin límite de longitud de la fórmula",
    [(VEP, 'MAX_LONGITUD_FORMULA = 2000  #', 'MAX_LONGITUD_FORMULA = 10 ** 9  #')], [B415]),
 "m20_sin_constante_local": ("cubiertas", "H6/H11", "(m20) se quita el error «constante en el punto real»",
    [(VEP, SUELO, '            if False:')], [B415]),
 "m22_cero_exento_en_todo": ("cubiertas", "H11", "(m22) el 0 queda exento en cualquier posición de la fórmula, no solo en min/max",
    [(VEP, '            if not ((v.denominator == 1 and 1 <= v <= 12) or pot10):', '            if not ((v.denominator == 1 and 0 <= v <= 12) or pot10):')], [B415]),
 "h7k_pdf_cabecera_al_principio": ("cubiertas", "H7/H11", "(m29) el tipo PDF exige la cabecera al principio (un PDF con bytes previos y sin extensión deja de reconocerse)",
    [(VEP, TIPO_PDF, '    if cab.lstrip().startswith(b"%PDF-") or ext.endswith(".pdf"):')], [B415]),
 "h6f_local_solo_arriba": ("cubiertas", "H6", "la perturbación local vuelve a ser solo hacia arriba",
    [(VEP, '        for sg in (1, -1):\n            try:\n                if _eval_formula_exacta(formula, dict(vals, **{o: v_o + sg * delta', '        for sg in (1,):\n            try:\n                if _eval_formula_exacta(formula, dict(vals, **{o: v_o + sg * delta')], [B415]),
 # ================================================================ no detectadas en la 2.ª pasada que el autor no dice haber cubierto
 "h1e_no_localizada_vale": ("resto", "H1", "contraste_pagina da por buena una cita «no_localizada» (ni pendiente ni discrepancia)",
    [(VEP, '        if est in ("signo_indeterminado", "no_localizada"):', '        if est in ("signo_indeterminado",):')], [B415]),
 "h1f_sin_ventana": ("resto", "H1", "se leen todas las cifras de la línea, no solo las de la cita (sin ventana)",
    [(VEP, DENTRO, '        return True')], [B415, BEE]),
 "h6a_semilla_por_formula": ("resto", "H6", "la semilla vuelve a depender del texto de la fórmula",
    [(VEP, '    rnd = _random.Random(semilla)', '    rnd = _random.Random(f"{semilla}|{formula}")')], [B415]),
 "h6b_sin_puntos_extremos": ("resto", "H6", "se quitan los puntos extremos (±10⁹) de cada origen",
    [(VEP, '            pt[o] = fractions.Fraction(g * 10 ** 9)\n            gen_pts.append(pt)', '            pt[o] = fractions.Fraction(g * 10 ** 9)')], [B415]),
 "h6c_sin_suelo_cero": ("resto", "H6", "se quita la excepción del suelo cero (max(a − b, 0) cuando actúa vuelve a ser error)",
    [(VEP, SUELO, '            if not locales:')], [B415]),
 "h6d_suelo_sin_exigir_cero": ("resto", "H6", "la excepción del suelo vale aunque el resultado no sea 0",
    [(VEP, SUELO, '            if not locales and not _suelo_cero(d["formula"]):')], [B415]),
 "h6e_cero_sin_suelo": ("resto", "H6", "una fórmula constante en el punto real vale siempre que el resultado sea 0, tenga o no un suelo en cero",
    [(VEP, SUELO, '            if not locales and not (r_ex == 0):')], [B415]),
 "h7g_ix_no_en_linea": ("resto", "H7", "las etiquetas con espacio de nombres (ix:nonFraction) dejan de tratarse como en línea",
    [(VEP, '            en_linea = tag in HTML_EN_LINEA or ":" in tag  #', '            en_linea = tag in HTML_EN_LINEA  #')], [B415]),
 "h7m_sin_quitar_guion_blando": ("resto", "H7", "el guion blando y el espacio de ancho cero dejan de quitarse al comparar",
    [(VEP, 'unicodedata.normalize("NFKC", "" if s is None else str(s)))\n    return re.sub(r"\\s+", " ", t).strip().lower()',
      'unicodedata.normalize("NFKC", "" if s is None else str(s)))\n    t = unicodedata.normalize("NFKC", "" if s is None else str(s))\n    return re.sub(r"\\s+", " ", t).strip().lower()')], [B415]),
 "h7n_sin_etiquetas_en_linea_nuevas": ("resto", "H7", "<ins>, <del>, <label>, <big> y <tt> dejan de ser en línea",
    [(VEP, '"wbr", "nobr", "ins", "del", "label", "big", "tt"}', '"wbr", "nobr"}')], [B415]),
 "h14b_esquema_dinero_real": ("resto", "H14", "el esquema deja de fijar aptitud_de_uso.apto_para_dinero_real en false",
    [(ESQ, '    "apto_para_dinero_real": {\n     "const": false,\n     "description": "(4.15, hito 2, H14)', '    "apto_para_dinero_real": {\n     "type": "boolean",\n     "description": "(4.15, hito 2, H14)')], [BEE, B415, B414]),
 "i20b_bloque_sin_declaracion": ("resto", "I20", "la ficha no lleva el bloque con solo entrada_efectiva.json (sin registro ni señales del estado o del alcance)",
    [(FIP, '    if (any(os.path.isfile(os.path.join(c, n)) for n in ("verificacion_entradas.json", "entrada_efectiva.json"))',
      '    if (any(os.path.isfile(os.path.join(c, n)) for n in ("verificacion_entradas.json",))')], [BEE]),
 "m47_u1_informe_sin_derivados": ("resto", "H11", "(m47) el informe V6.4 no dice cuántos derivados comprobados hay",
    [(INP, """                      + (f"{ve.get('derivados_comprobados')} derivados comprobados (significado económico: revisión independiente) · " if ve.get("derivados_comprobados") else "") + """, """                      + "" + """)], [B415]),
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
    tmp = os.path.join(F, "tmp", "mut3_" + nombre)
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
    elif len(args) == 1 and args[0] in ("nuevas", "cubiertas", "resto", "control"):
        nombres = [k for k, v in M.items() if v[0] == args[0]]
    else:
        nombres = args
    with concurrent.futures.ThreadPoolExecutor(max_workers=j) as ex:
        for r in ex.map(correr, nombres):
            print(json.dumps(r, ensure_ascii=False))
            sys.stdout.flush()
