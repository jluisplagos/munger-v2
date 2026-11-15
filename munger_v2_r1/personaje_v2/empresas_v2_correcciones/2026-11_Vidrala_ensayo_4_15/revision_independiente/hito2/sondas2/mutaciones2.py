#!/usr/bin/env python3
"""Mutaciones de la SEGUNDA pasada (Fable, hito 2 de la 4.15, candidata estable 92b2362). Como mutaciones.py de la primera pasada: quita o
altera UNA regla del código en un árbol ligero aparte (scripts/, pruebas/ y esquema/ copiados; el resto, enlaces a la copia propia del árbol
congelado) y ejecuta las baterías permitidas (sin LibreOffice) para ver si alguna prueba lo detecta. Nunca toca el árbol congelado.
Uso: python3 -I -B mutaciones2.py [-j N] NOMBRE [NOMBRE …] | todas | lista"""
import concurrent.futures, json, os, re, shutil, subprocess, sys, time
F = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COPIA = os.path.join(F, "copia", "munger_v2_r1")
MUT = os.path.join(F, "mut2")
B415, BEE, B414 = "test_verificacion_entradas_415.py", "test_entrada_efectiva_415.py", "test_verificacion_entradas_414.py"
VEP, FHP, FIP, INP, PLP = "scripts/verificacion_entradas.py", "scripts/fase1_historia.py", "scripts/ficha.py", "scripts/informe.py", "scripts/pipeline.py"
ESQ = "esquema/ficha.esquema.json"
V64 = """f"{'sí' if ve.get('apto_por_entradas') else 'no'}. Apta para dinero real: no\""""
I20_FIN = '                  + ". Apta para dinero real: no.")'
SUELO = '            if not locales and not (r_ex == 0 and _suelo_cero(d["formula"])):'
OCULTO = '            return (tag in HTML_SIN_TEXTO_VISIBLE or "hidden" in a or "display:none" in st'
TIPO_PDF = '    if cab.lstrip().startswith(b"%PDF-") or ext.endswith(".pdf") or (b"%PDF-" in cab[:1024] and not texto_o_html):'
BLOQUE = '    if any(os.path.isfile(os.path.join(c, n)) for n in ("verificacion_entradas.json", "entrada_efectiva.json")):'

# nombre: (hallazgo, descripción, [(archivo, texto original, texto nuevo)], [baterías])
M = {
 "c00_control": ("—", "control: sin cambio de regla (solo un comentario); las baterías tienen que pasar enteras en el árbol ligero",
    [(VEP, 'FORMATO = "4.15"', 'FORMATO = "4.15"  # control')], [BEE, B414, B415]),
 # ---------------------------------------------------------------- H1
 "h1a_cita_no_pagina": ("H1", "contraste_pagina lee la cifra y el signo en la CITA, no en la página (como antes de la corrección)",
    [(VEP, 'est, det = _cita_cifra(f.get("cita"), vf, pag)', 'est, det = _cita_cifra(f.get("cita"), vf)')], [B415]),
 "h1b_solo_pasaje": ("H1", "_apariciones_en_pagina devuelve solo el pasaje que casa con la cita (no la línea completa): la marca de signo o el resto del número que quedan fuera de la cita no se ven",
    [(VEP, '        out.append((t[ini:fin], m.start() - ini, m.end() - ini))', '        out.append((t[m.start():m.end()], 0, m.end() - m.start()))')], [B415, BEE]),
 "h1c_primera_aparicion": ("H1", "solo se lee la PRIMERA aparición de la cita en la página",
    [(VEP, '    lect = [_lectura_cifra(linea, vf, (a, b)) for linea, a, b in apar]', '    lect = [_lectura_cifra(linea, vf, (a, b)) for linea, a, b in apar[:1]]')], [B415]),
 "h1d_no_localizada_en_cita": ("H1", "si el pasaje no se localiza en la página, la cifra se lee en la cita",
    [(VEP, '    if not apar:\n        return "no_localizada", ', '    if not apar:\n        return _lectura_cifra(cita, vf)\n        return "no_localizada", ')], [B415]),
 "h1e_no_localizada_vale": ("H1", "contraste_pagina da por buena una cita «no_localizada» (ni pendiente ni discrepancia)",
    [(VEP, '        if est in ("signo_indeterminado", "no_localizada"):', '        if est in ("signo_indeterminado",):')], [B415]),
 "h1f_sin_ventana": ("H1", "se leen todas las cifras de la línea, no solo las que toca la cita (sin ventana)",
    [(VEP, '        return ventana is None or (a < ventana[1] and b > ventana[0])', '        return True')], [B415, BEE]),
 "h1g_calc_sin_pagina": ("H1", "calcular_entrada lee la cifra y el signo del componente en la cita, no en la página",
    [(FHP, 'est_c, det_c = VE._cita_cifra(cmp.get("cita"), publicado, pag)', 'est_c, det_c = VE._cita_cifra(cmp.get("cita"), publicado)')], [BEE]),
 "h1h_lecturas_distintas_vale": ("H1", "si la cita aparece varias veces con lecturas distintas, vale con que una sea «ok»",
    [(VEP, '    if len(estados) == 1:\n        return lect[0]\n', '    if len(estados) == 1:\n        return lect[0]\n    if "ok" in estados:\n        return "ok", "MUTACIÓN"\n')], [B415]),
 "h1i_limites_en_la_cita": ("H1", "los límites de «cifra completa» se evalúan dentro de la cita (la línea se recorta a la ventana antes de buscar la cifra)",
    [(VEP, '    lect = [_lectura_cifra(linea, vf, (a, b)) for linea, a, b in apar]',
      '    lect = [(lambda e: e if e[0] != "ausente" or _lectura_cifra(linea[a:b], vf)[0] == "ausente" else ("ok", "MUTACIÓN"))(_lectura_cifra(linea, vf, (a, b))) for linea, a, b in apar]')], [B415]),
 "p1_cifra_dentro_de_la_cita": ("N1 (propuesta)", "PROPUESTA del revisor, no una regla quitada: la cifra de la página tiene que quedar DENTRO de la cita (no basta que la toque). Si las baterías pasan, la propuesta es compatible con ellas",
    [(VEP, '        return ventana is None or (a < ventana[1] and b > ventana[0])', '        return ventana is None or (a >= ventana[0] and b <= ventana[1])')], [B415, BEE]),
 # ---------------------------------------------------------------- H2
 "h2a_i20_dinero_real_si": ("H2", "(m37 de la 1.ª pasada) la línea de I20 dice «Apta para dinero real: sí» si es apta por entradas",
    [(INP, I20_FIN, '                  + (". Apta para dinero real: sí." if vef.get("apto_por_entradas") else ". Apta para dinero real: no."))')], [BEE, B415, B414]),
 "h2b_v64_dinero_real_si": ("H2", "(m39) el párrafo de aptitud de la V6.4 dice «Apta para dinero real: sí»",
    [(INP, V64, V64.replace("real: no", "real: sí"))], [B414, B415]),
 "h2c_v64_apta_siempre_si": ("H2", "(m40) el párrafo de aptitud de la V6.4 dice siempre «apta por entradas: sí»",
    [(INP, V64, V64.replace("ve.get('apto_por_entradas')", "True"))], [B414, B415]),
 "h2d_i20_apta_siempre_si": ("H2", "la línea de I20 dice siempre «apta por entradas: sí»",
    [(INP, """apta por entradas: {'sí' if vef.get('apto_por_entradas') else 'no'}\"""", """apta por entradas: {'sí' if True else 'no'}\"""")], [BEE, B415, B414]),
 "h2e_i20_sin_dinero_real": ("H2", "la línea de I20 no dice «Apta para dinero real: no»",
    [(INP, I20_FIN, '                  + ".")')], [BEE, B415, B414]),
 "h2f_v64_sin_dinero_real_si_apta": ("H2", "el párrafo de la V6.4 omite «Apta para dinero real: no» cuando el registro es apto por entradas",
    [(INP, V64, """f"{'sí. Conclusión' if ve.get('apto_por_entradas') else 'no. Apta para dinero real: no'}\"""")], [B414, B415]),
 "h2g_v64_dinero_real_si_solo_si_apta": ("H2", "el párrafo de la V6.4 dice «Apta para dinero real: sí» solo cuando el registro es apto por entradas",
    [(INP, V64, """f"{'sí. Apta para dinero real: sí' if ve.get('apto_por_entradas') else 'no. Apta para dinero real: no'}\"""")], [B414, B415]),
 # ---------------------------------------------------------------- H4, H5
 "h4a_menos_unicode_un_espacio": ("H4", "«− x» (menos Unicode a un espacio) vuelve a leerse como negativo seguro",
    [(VEP, '    m = re.search("[" + marcas + r"](\\s*)$", antes)\n    if m:', '    if re.search(MENOS_UNICODE + r"\\s?$", antes):\n        return -1\n    m = re.search("[" + marcas + r"](\\s*)$", antes)\n    if m:')], [B415]),
 "h4b_cero_sin_menos_unicode": ("H4", "el «−» (U+2212) aislado deja de valer como cero impreso",
    [(VEP, '[-–—−](?![\\w.,]| ?[\\d(])", r"(?<=[\\d)] )[-–—−](?= [\\d(])"', '[-–—](?![\\w.,]| ?[\\d(])", r"(?<=[\\d)] )[-–—](?= [\\d(])"')], [B415]),
 "h5a_sin_codigo_moneda": ("H5", "el código de moneda (EUR, USD…) deja de admitirse entre el paréntesis y la cifra",
    [(VEP, 'MONEDA_RE = r"(?:[€$£¥]|\\b(?:EUR|USD|GBP|CHF|JPY|DKK|SEK|NOK|BRL)\\b)"', 'MONEDA_RE = r"(?:[€$£¥])"')], [B415]),
 "h5b_sin_porcentaje": ("H5", "el «%» deja de admitirse entre la cifra y el paréntesis de cierre",
    [(VEP, '    despues = re.sub(r"^\\s?(?:" + MONEDA_RE + r"|%)", "", despues, flags=re.I)', '    despues = re.sub(r"^\\s?(?:" + MONEDA_RE + r")", "", despues, flags=re.I)')], [B415]),
 "h5c_sin_dolar_menos": ("H5", "«$-x» deja de leerse como negativo",
    [(VEP, 're.search(r"[\\s:;=/\\[|€$£¥]$", previo)):', 're.search(r"[\\s:;=/\\[|]$", previo)):')], [B415]),
 "h5d_sin_intervalo": ("H5", "el guion pegado entre dos cifras deja de leerse como intervalo o fecha",
    [(VEP, '        if m.group(1) == "" and re.search(r"\\d$", previo):\n            return 1  # intervalo', '        if False:\n            return 1  # intervalo')], [B415]),
 # ---------------------------------------------------------------- H6
 "h6a_semilla_por_formula": ("H6", "la semilla vuelve a depender del texto de la fórmula",
    [(VEP, '    rnd = _random.Random(semilla)', '    rnd = _random.Random(f"{semilla}|{formula}")')], [B415]),
 "h6b_sin_puntos_extremos": ("H6", "se quitan los puntos extremos (±10⁹) de cada origen",
    [(VEP, '            pt[o] = fractions.Fraction(g * 10 ** 9)\n            gen_pts.append(pt)', '            pt[o] = fractions.Fraction(g * 10 ** 9)')], [B415]),
 "h6c_sin_suelo_cero": ("H6", "se quita la excepción del suelo cero (max(a − b, 0) cuando actúa vuelve a ser error)",
    [(VEP, SUELO, '            if not locales:')], [B415]),
 "h6d_suelo_sin_exigir_cero": ("H6", "la excepción del suelo vale aunque el resultado no sea 0",
    [(VEP, SUELO, '            if not locales and not _suelo_cero(d["formula"]):')], [B415]),
 "h6e_cero_sin_suelo": ("H6", "una fórmula constante en el punto real vale siempre que el resultado sea 0, tenga o no un suelo en cero",
    [(VEP, SUELO, '            if not locales and not (r_ex == 0):')], [B415]),
 "h6f_local_solo_arriba": ("H6", "la perturbación local vuelve a ser solo hacia arriba",
    [(VEP, '        for sg in (1, -1):\n            try:\n                if _eval_formula_exacta(formula, dict(vals, **{o: v_o + sg * delta', '        for sg in (1,):\n            try:\n                if _eval_formula_exacta(formula, dict(vals, **{o: v_o + sg * delta')], [B415]),
 "m20_sin_constante_local": ("H6/H11", "(m20 de la 1.ª pasada) se quita el error «constante en el punto real»",
    [(VEP, SUELO, '            if False:')], [B415]),
 # ---------------------------------------------------------------- H7
 "h7a_details_visible": ("H7", "el contenido de un <details> cerrado vuelve a darse por visible",
    [(VEP, '(tag in ("dialog", "details") and "open" not in a)', '(tag in ("dialog",) and "open" not in a)')], [B415]),
 "h7b_dialog_visible": ("H7", "un <dialog> sin «open» vuelve a darse por visible",
    [(VEP, '(tag in ("dialog", "details") and "open" not in a)', '(tag in ("details",) and "open" not in a)')], [B415]),
 "h7c_summary_oculto": ("H7", "el <summary> de un <details> cerrado se oculta con el resto",
    [(VEP, '                if det:  # el <summary>', '                if det and False:  # el <summary>')], [B415]),
 "h7d_barra_cierra": ("H7", "«<div hidden/>» vuelve a cerrarse con la barra (lo que sigue se da por visible)",
    [(VEP, '            if tag.lower() in HTML_VACIOS:\n                if tag.lower() not in HTML_EN_LINEA:\n                    self.trozos.append(" ")\n            else:\n                self.handle_starttag(tag, attrs)',
      '            if tag.lower() not in HTML_EN_LINEA:\n                self.trozos.append(" ")')], [B415]),
 "h7e_aria_hidden_oculta": ("H7", "aria-hidden=\"true\" vuelve a ocultar el texto",
    [(VEP, OCULTO, '            return (tag in HTML_SIN_TEXTO_VISIBLE or "hidden" in a or a.get("aria-hidden", "").strip().lower() == "true" or "display:none" in st')], [B415]),
 "h7f_sin_cierre_de_head": ("H7", "un elemento del cuerpo deja de cerrar la cabecera cuando falta </head>",
    [(VEP, '            if any(t == "head" for t, _ in self.pila) and tag not in HTML_EN_CABECERA:', '            if False:')], [B415]),
 "h7g_ix_no_en_linea": ("H7", "las etiquetas con espacio de nombres (ix:nonFraction) dejan de tratarse como en línea",
    [(VEP, '            en_linea = tag in HTML_EN_LINEA or ":" in tag  #', '            en_linea = tag in HTML_EN_LINEA  #')], [B415]),
 "h7h_sin_cp1252": ("H7", "ISO-8859-1 declarado deja de leerse como windows-1252",
    [(VEP, '        if nombre in ("latin-1", "iso8859-1", "ascii"):\n            cod = "cp1252"', '        if False:\n            cod = "cp1252"')], [B415]),
 "h7i_utf7_admitido": ("H7", "charset=utf-7 vuelve a admitirse",
    [(VEP, '        elif nombre == "utf-7" or not (', '        elif not (')], [B415]),
 "h7j_pdf_por_mencion": ("H7", "un HTML o un texto que mencionan «%PDF-» en su primer kilobyte vuelven a tratarse como PDF",
    [(VEP, TIPO_PDF, '    if b"%PDF-" in cab[:1024] or ext.endswith(".pdf"):')], [B415]),
 "h7k_pdf_cabecera_al_principio": ("H7/H11", "(m29) el tipo PDF exige la cabecera al principio (un PDF con bytes previos y sin extensión deja de reconocerse)",
    [(VEP, TIPO_PDF, '    if cab.lstrip().startswith(b"%PDF-") or ext.endswith(".pdf"):')], [B415]),
 "h7l_hidden_no_oculta": ("H7/H11", "(m25) el atributo hidden deja de ocultar el elemento",
    [(VEP, OCULTO, '            return (tag in HTML_SIN_TEXTO_VISIBLE or "display:none" in st')], [B415]),
 "h7m_sin_quitar_guion_blando": ("H7", "el guion blando y el espacio de ancho cero dejan de quitarse al comparar",
    [(VEP, 'unicodedata.normalize("NFKC", "" if s is None else str(s)))\n    return re.sub(r"\\s+", " ", t).strip().lower()',
      'unicodedata.normalize("NFKC", "" if s is None else str(s)))\n    t = unicodedata.normalize("NFKC", "" if s is None else str(s))\n    return re.sub(r"\\s+", " ", t).strip().lower()')], [B415]),
 "h7n_sin_etiquetas_en_linea_nuevas": ("H7", "<ins>, <del>, <label>, <big> y <tt> dejan de ser en línea",
    [(VEP, '"wbr", "nobr", "ins", "del", "label", "big", "tt"}', '"wbr", "nobr"}')], [B415]),
 # ---------------------------------------------------------------- H8, H9, H10
 "h8a_i20_sin_resumen": ("H8", "la línea de I20 del informe no da el resumen de lo que no se contrastó",
    [(INP, """                  + (f"; {str(_rs.get('resumen')).replace('«', '').replace('»', '')}" if _rs.get("resumen") else "")\n""", '                  + ""\n')], [BEE, B415]),
 "h8b_motivo_cortado": ("H8", "el motivo de la línea de I20 vuelve a cortarse a 300 caracteres",
    [(INP, """(f"; motivo: {str(_rs.get('motivo')).replace('«', '').replace('»', '')}" if not vef""", """(f"; motivo: {str(_rs.get('motivo')).replace('«', '').replace('»', '')[:300]}" if not vef""")], [BEE]),
 "h9a_modo_distinto_no_impide": ("H9", "un modo aplicado distinto del declarado (o una declaración con error) deja de impedir «apto por entradas»",
    [(FIP, '    return {"apto_por_entradas": bool(apto_e) and motivo_modo is None, "resumen": resumen,', '    return {"apto_por_entradas": bool(apto_e), "resumen": resumen,')], [BEE]),
 "h9b_sin_motivo_modo": ("H9", "la ficha no da el motivo del modo (motivo_modo siempre vacío en la salida)",
    [(FIP, '            "motivo_modo": motivo_modo,', '            "motivo_modo": None,')], [BEE]),
 "h9c_informe_sin_aviso": ("H9/H11", "(m33) el informe no avisa de que el modo aplicado no coincide con el declarado",
    [(INP, '                  + ("; **el modo aplicado no coincide con el declarado**" if _ee.get("coinciden") is False else "")\n', '                  + ""\n')], [BEE]),
 "h9d_error_declaracion_no_impide": ("H9", "una declaración del modo con error deja de impedir «apto por entradas»",
    [(FIP, """tiene un error: {declarada.get('error')}" if declarada.get("error")""", """tiene un error: {declarada.get('error')}" if False""")], [BEE]),
 "h10_fuente_recortada": ("H10", "el texto de fuente del cálculo de C48 vuelve a cortarse a 1500 caracteres",
    [(FHP, '+ "; ".join(fuentes))  # (4.15, hito 2, H10)', '+ "; ".join(fuentes))[:1500]  # (4.15, hito 2, H10)')], [BEE]),
 # ---------------------------------------------------------------- H14, U7, U6, I20
 "h14a_sin_tratamiento": ("H14", "signo −1 con el tratamiento «ninguno» vuelve a aceptarse",
    [(VEP, '            if sig == -1 and _norm_txt(f.get("tratamiento")) in (', '            if False and _norm_txt(f.get("tratamiento")) in (')], [B415]),
 "h14b_esquema_dinero_real": ("H14", "el esquema deja de fijar aptitud_de_uso.apto_para_dinero_real en false",
    [(ESQ, '    "apto_para_dinero_real": {\n     "const": false,\n     "description": "(4.15, hito 2, H14)', '    "apto_para_dinero_real": {\n     "type": "boolean",\n     "description": "(4.15, hito 2, H14)')], [BEE, B415, B414]),
 "u7a_sin_control": ("U7", "una unidad monetaria no reconocida vuelve a quedar como «no monetaria»",
    [(VEP, '            if u is None and _unidad_monetaria_no_reconocida(f.get("unidad")):', '            if False:')], [B415]),
 "u7b_por_accion": ("U7", "un precio por acción («EUR por acción») se trata como unidad monetaria no reconocida",
    [(VEP, 'MARCAS_MONEDA.search(t) is not None and POR_UNIDAD.search(t) is None', 'MARCAS_MONEDA.search(t) is not None')], [B415]),
 "u6a_sin_erratas": ("U6", "una errata de la clave «entrada_efectiva» en alcance_v2.json deja el modo en «registrada» en silencio",
    [(PLP, '    if parecidas:\n        raise ValueError(', '    if False:\n        raise ValueError(')], [BEE]),
 "u6b_sin_contradiccion": ("U6", "«registrada» en entrada_efectiva.json frente a «estricta» en alcance_v2.json deja de ser un error",
    [(PLP, '        if d["modo"] == "registrada" and _alcance_modo(carpeta) == "estricta":', '        if False:')], [BEE]),
 "u6c_alcance_ilegible": ("U6", "un alcance_v2.json ilegible deja el modo en «registrada» en silencio",
    [(PLP, '    except (OSError, ValueError) as ex:\n        raise ValueError(f"alcance_v2.json no se puede leer', '    except (OSError, ValueError) as ex:\n        return None\n        raise ValueError(f"alcance_v2.json no se puede leer')], [BEE]),
 "u6d_alcance_no_objeto": ("U6", "un alcance_v2.json que no es un objeto deja el modo en «registrada» en silencio",
    [(PLP, '    if not isinstance(a, dict):\n        raise ValueError("alcance_v2.json no es un objeto', '    if not isinstance(a, dict):\n        return None\n        raise ValueError("alcance_v2.json no es un objeto')], [BEE]),
 "i20a_bloque_siempre": ("I20", "la ficha lleva el bloque también sin registro ni declaración (como en la candidata de la 1.ª pasada)",
    [(FIP, BLOQUE, '    if True:')], [BEE, B414]),
 "i20b_bloque_solo_con_registro": ("I20", "la ficha solo lleva el bloque si hay verificacion_entradas.json (con solo la declaración del modo, no)",
    [(FIP, BLOQUE, '    if os.path.isfile(os.path.join(c, "verificacion_entradas.json")):')], [BEE]),
 "i20c_bloque_solo_con_declaracion": ("I20", "la ficha solo lleva el bloque si hay entrada_efectiva.json (con solo el registro, no)",
    [(FIP, BLOQUE, '    if os.path.isfile(os.path.join(c, "entrada_efectiva.json")):')], [BEE, B415]),
 "m31_i20_apto_siempre_no": ("H11", "(m31) la ficha dice siempre apto_por_entradas = false en el bloque de I20",
    [(FIP, '    return {"apto_por_entradas": bool(apto_e) and motivo_modo is None, "resumen": resumen,', '    return {"apto_por_entradas": False, "resumen": resumen,')], [BEE, B415, B414]),
 # ---------------------------------------------------------------- H11: no detectadas en la 1.ª pasada
 "m12_tolerancia_0_00055": ("H11", "(m12) tolerancia de importes ampliada a 0,00055",
    [(VEP, 'abs(exacto - fv) <= fractions.Fraction(1, 2000)', 'abs(exacto - fv) <= fractions.Fraction(11, 20000)')], [B415]),
 "m16_sin_limite_nodos": ("H11", "(m16) sin límite de nodos de la fórmula",
    [(VEP, 'MAX_NODOS_FORMULA = 400', 'MAX_NODOS_FORMULA = 10 ** 9')], [B415]),
 "m17_sin_limite_longitud": ("H11", "(m17) sin límite de longitud de la fórmula",
    [(VEP, 'MAX_LONGITUD_FORMULA = 2000  #', 'MAX_LONGITUD_FORMULA = 10 ** 9  #')], [B415]),
 "m22_cero_exento_en_todo": ("H11", "(m22) el 0 queda exento en cualquier posición de la fórmula, no solo en min/max",
    [(VEP, '            if not ((v.denominator == 1 and 1 <= v <= 12) or pot10):', '            if not ((v.denominator == 1 and 0 <= v <= 12) or pot10):')], [B415]),
 "m47_u1_informe_sin_derivados": ("H11", "(m47) el informe V6.4 no dice cuántos derivados comprobados hay",
    [(INP, """                      + (f"{ve.get('derivados_comprobados')} derivados comprobados (significado económico: revisión independiente) · " if ve.get("derivados_comprobados") else "") + """, """                      + "" + """)], [B415]),
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


def comprobar_textos():
    """Cada texto a mutar aparece exactamente una vez en la copia (sin ejecutar nada)."""
    mal = []
    for nombre, (_h, _desc, cambios, _b) in M.items():
        for arch, viejo, nuevo in cambios:
            s = open(os.path.join(COPIA, "personaje_v2", arch), encoding="utf-8").read()
            if s.count(viejo) != 1 or viejo == nuevo:
                mal.append((nombre, arch, s.count(viejo)))
    return mal


def correr(nombre):
    hall, desc, cambios, baterias = M[nombre]
    d = preparar(nombre)
    for arch, viejo, nuevo in cambios:
        p = os.path.join(d, "personaje_v2", arch)
        s = open(p, encoding="utf-8").read()
        if s.count(viejo) != 1:
            return {"mutacion": nombre, "hallazgo": hall, "descripcion": desc, "error": f"el texto a mutar aparece {s.count(viejo)} veces en {arch}"}
        open(p, "w", encoding="utf-8").write(s.replace(viejo, nuevo))
    res = {"mutacion": nombre, "hallazgo": hall, "descripcion": desc, "baterias": {}}
    env = dict(os.environ, PATH=os.path.join(F, "bin") + os.pathsep + os.environ["PATH"], TMPDIR=os.path.join(F, "tmp"))
    for b in baterias:
        t0 = time.time()
        sal = os.path.join(MUT, nombre, b + ".json")
        try:
            r = subprocess.run([sys.executable, "-B", os.path.join("pruebas", b), "--json", sal], cwd=os.path.join(d, "personaje_v2"), capture_output=True, text=True, env=env, timeout=2400)
            out, rc = r.stdout + r.stderr, r.returncode
        except subprocess.TimeoutExpired as ex:
            out, rc = (ex.stdout or b"").decode("utf-8", "replace") if isinstance(ex.stdout, bytes) else str(ex.stdout or ""), "TIEMPO AGOTADO (2400 s)"
        open(os.path.join(MUT, nombre, b + ".log"), "w", encoding="utf-8").write(out)
        fallan = [l[:260] for l in out.splitlines() if re.match(r"^\[[A-Za-z0-9]+\] FALLA", l)]
        m = re.search(r"(?m)^(\d+)/(\d+) pruebas", out)
        traza = [l[:200] for l in out.splitlines() if l.startswith(("Traceback", "AssertionError")) or "Error" in l[:40]][-2:]
        res["baterias"][b] = {"codigo": rc, "pasan": m.group(0) if m else None, "fallan": fallan, "traza": traza, "segundos": round(time.time() - t0)}
    shutil.rmtree(d, ignore_errors=True)  # se conserva el registro, no el árbol
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
            print(k, "·", v[0], "·", v[1], "·", v[3])
        print(len(M), "mutaciones; textos comprobados")
        sys.exit(0)
    nombres = list(M) if args == ["todas"] else args
    with concurrent.futures.ThreadPoolExecutor(max_workers=j) as ex:
        for r in ex.map(correr, nombres):
            print(json.dumps(r, ensure_ascii=False))
            sys.stdout.flush()
