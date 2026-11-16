"""Definición de las MUTACIONES de la sexta comprobación (Fable, hito 2 de la 4.15, candidata 8196522): una regla quitada o alterada cada
vez. Las usa e5 (evaluación a nivel de unidad de las pruebas nuevas, cargando el código mutado en memoria) y mutaciones6.py (batería
entera en un árbol ligero aparte, con el arnés de mutaciones4.py).
Grupos: «v» = lo corregido en esta candidata (V1, V2, V3, V5, V7), una pieza cada vez; «v4» = mutaciones que la quinta comprobación dejó
SIN detectar y para las que el autor añade prueba ahora (Q1, Q3, T6) y la de T8 que quedó sin prueba; «control»."""
VEP, PLP = "scripts/verificacion_entradas.py", "scripts/pipeline.py"
B415, BEE, B414 = "test_verificacion_entradas_415.py", "test_entrada_efectiva_415.py", "test_verificacion_entradas_414.py"
MARCAS = r"""                           r"\bcoronas?\b|\breal(?:es)?\b|\bfrancos?\b|\bmm€|\bmeur|\bkeur|\bk€)", re.I)  # (hito 2, V7) también «real»"""
MON1 = """    for cod, formas in (("eur", ("€", "eur", "euro", "euros")), ("usd", ("$", "usd", "dólar", "dolar", "dólares", "dolares")),"""
MON2 = """                        ("gbp", ("£", "gbp", "libra", "libras")), ("jpy", ("¥", "jpy")), ("chf", ("chf", "franco", "francos")),"""
MON3 = """                        ("brl", ("brl", "real", "reales")), ("corona", ("corona", "coronas", "dkk", "sek", "nok"))):"""
ESPECIAL = """    if {_a, _b} <= {"corona"} and par is not None and _norm_txt(par.group("a")) in ("dkk", "sek", "nok") and _norm_txt(par.group("b")) in ("dkk", "sek", "nok"):"""
MPREV = r"""        m_prev = re.search(r"(?:^|[^\w.,])(\d{4})\Z", previo) or re.search(r"(?:^|[^\w.,])(?:FY|AF|EJ)(\d{4})\Z", previo, re.I)"""
ANIOS = r"""        anios = (m_prev is not None and re.fullmatch(r"\d{4}", tok) is not None and 1900 <= int(m_prev.group(1)) <= int(tok) <= 2100)"""
RANGO = "1900 <= int(m_prev.group(1)) <= int(tok) <= 2100"
FECHA = r"""        fecha = re.search(r"(?:^|[^\w.,])\d{1,2}-\d{1,2}\Z", previo) is not None and re.fullmatch(r"\d{4}", tok) is not None  # «31-12-2024»"""
CORTE = """        if len(out) > MAX_APARICIONES_CITA:  # (hito 2, V5) basta saber que pasa del máximo: el coste queda acotado\n            break\n"""
LECT = r"""        for m in re.finditer(r"(?<![\d.,])(?<!\d')" + re.escape(c) + r"(?!\d|[.,']\d)", t):  # (hito 2, V7) «1'849,7» no contiene 849,7"""
ENNUM1 = r"""                return ((re.match(r"\d", palabras[0]) is not None and re.search(r"(?:\d|\d[.,']|(?:^|[^\w.,])[.,])\Z", antes2) is not None)"""
EDIC = r"""                                                              or _ediciones(re.sub(r"[^a-z]", "", str(k).lower()), "entradaefectiva") <= 3)]"""

# nombre: (grupo, hallazgo, descripción, [(archivo, texto original, texto nuevo)], [baterías])
M = {
 "c00_control": ("control", "—", "control: sin cambio de regla (solo un comentario); las baterías tienen que pasar enteras en el árbol ligero",
    [(VEP, 'FORMATO = "4.15"', 'FORMATO = "4.15"  # control')], [BEE, B414, B415]),
 # ================================================================ V1 · _moneda_de: franco, real y coronas
 "v1a_sin_franco": ("v", "V1", "_moneda_de no normaliza el franco («francos/CHF» vuelve a quedar exenta de U7)",
    [(VEP, MON2, MON2.replace(""", ("chf", ("chf", "franco", "francos")),""", ","))], [B415]),
 "v1b_sin_real": ("v", "V1", "_moneda_de no normaliza el real («reales/BRL» vuelve a quedar exenta)",
    [(VEP, MON3, MON3.replace("""("brl", ("brl", "real", "reales")), """, ""))], [B415]),
 "v1c_sin_corona": ("v", "V1", "_moneda_de no normaliza las coronas («coronas/DKK» y «corona/coronas» vuelven a quedar exentas)",
    [(VEP, MON3, MON3.replace(""", ("corona", ("corona", "coronas", "dkk", "sek", "nok"))):""", "):"))], [B415]),
 "v1d_corona_sin_codigos": ("v", "V1", "la familia de la corona no incluye los códigos DKK, SEK y NOK («coronas/DKK» vuelve a ser un «tipo de cambio»; «corona/coronas» sigue pendiente)",
    [(VEP, MON3, MON3.replace("""("corona", "coronas", "dkk", "sek", "nok")""", """("corona", "coronas")"""))], [B415]),
 "v1e_sin_excepcion_dos_codigos": ("v", "V1", "se quita la excepción de los dos códigos: «DKK/SEK» (un tipo de cambio de verdad) pasa a pendiente",
    [(VEP, ESPECIAL, "    if False:")], [B415]),
 "v1f_excepcion_un_solo_codigo": ("v", "V1", "la excepción vale con que UNO de los dos sea un código («coronas/DKK» vuelve a ser un «tipo de cambio»)",
    [(VEP, ESPECIAL, ESPECIAL.replace("""and _norm_txt(par.group("a")) in ("dkk", "sek", "nok") and _norm_txt(par.group("b")) in ("dkk", "sek", "nok"):""",
                                      """and (_norm_txt(par.group("a")) in ("dkk", "sek", "nok") or _norm_txt(par.group("b")) in ("dkk", "sek", "nok")):"""))], [B415]),
 # ================================================================ V2 · \Z en el intervalo y en la fecha
 "v2a_anio_anterior_con_dolar": ("v", "V2", "el año anterior del intervalo vuelve a anclarse con «$» (el año al final de la línea anterior vuelve a hacer de «⏎-2024» un intervalo)",
    [(VEP, MPREV, MPREV.replace(r"(\d{4})\Z", r"(\d{4})$"))], [B415]),
 "v2b_fecha_con_dolar": ("v", "V2", "la fecha vuelve a anclarse con «$» («Notas 5-6⏎-2024» vuelve a leerse como fecha)",
    [(VEP, FECHA, FECHA.replace(r"\d{1,2}-\d{1,2}\Z", r"\d{1,2}-\d{1,2}$"))], [B415]),
 "v2c_los_dos_con_dolar": ("v", "V2", "las dos anclas vuelven a «$» (la regla de 876bfc2)",
    [(VEP, MPREV, MPREV.replace(r"(\d{4})\Z", r"(\d{4})$")), (VEP, FECHA, FECHA.replace(r"\d{1,2}-\d{1,2}\Z", r"\d{1,2}-\d{1,2}$"))], [B415]),
 # ================================================================ V3 y V7 · en_numero
 "v3a_sin_decimal_sin_cero": ("v", "V3", "en_numero deja de contar el punto o la coma que empiezan una «palabra» («(.5)» citada «5» vuelve a quedar pendiente)",
    [(VEP, ENNUM1, ENNUM1.replace(r"(?:\d|\d[.,']|(?:^|[^\w.,])[.,])\Z", r"(?:\d|\d[.,'])\Z"))], [B415]),
 "v3b_en_numero_con_dolar": ("v", "V7", "en_numero vuelve a anclarse con «$» (una palabra cortada al principio de una línea, tras una línea que acaba en cifra, vuelve a discrepancia)",
    [(VEP, ENNUM1, ENNUM1.replace(r"[.,])\Z", r"[.,])$"))], [B415]),
 "v7a_en_numero_sin_apostrofo": ("v", "V7", "en_numero deja de contar «cifra + apóstrofo» delante de la cita",
    [(VEP, ENNUM1, ENNUM1.replace(r"\d[.,']", r"\d[.,]"))], [B415]),
 # ================================================================ V7 · apóstrofo en _lectura_cifra y «real» en MARCAS_MONEDA
 "v7b_lectura_sin_apostrofo_delante": ("v", "V7", "_lectura_cifra sin «(?<!\\d')»: «849,7» vuelve a leerse dentro de «1'849,7»",
    [(VEP, LECT, LECT.replace(r"""(?<![\d.,])(?<!\d')" + re.escape(c)""", r"""(?<![\d.,])" + re.escape(c)"""))], [B415]),
 "v7c_lectura_sin_apostrofo_detras": ("v", "V7", "_lectura_cifra sin el apóstrofo en el límite final: «849» vuelve a leerse dentro de «849'697»",
    [(VEP, LECT, LECT.replace(r"""(?!\d|[.,']\d)", t)""", r"""(?!\d|[.,]\d)", t)"""))], [B415]),
 "v7d_real_solo_plural": ("v", "V7", "MARCAS_MONEDA vuelve a «reales?» («real», en singular, deja de ser una marca: «miles de real» no queda pendiente)",
    [(VEP, MARCAS, MARCAS.replace(r"\breal(?:es)?\b", r"\breales?\b"))], [B415]),
 # ================================================================ V5 · corte del recuento
 "v5a_sin_corte": ("v", "V5", "se quita el corte del recuento de apariciones (se recogen todas; el coste vuelve a crecer con el cuadrado en una línea)",
    [(VEP, CORTE, "")], [B415]),
 "v5b_corte_en_el_maximo": ("v", "V5", "el corte salta al LLEGAR al máximo (≥ en vez de >): se devuelven 200 apariciones y la cita con miles de apariciones se lee como si tuviera 200",
    [(VEP, CORTE, CORTE.replace("len(out) > MAX_APARICIONES_CITA", "len(out) >= MAX_APARICIONES_CITA"))], [B415]),
 # ================================================================ V4 · sin detectar en la quinta comprobación; el autor añade prueba ahora
 "q1c_moneda_sin_gbp_jpy": ("v4", "Q1", "_moneda_de no normaliza la libra ni el yen («libras/GBP», «GBP/£» y «JPY/¥» vuelven a quedar exentas) (adaptada a la línea nueva)",
    [(VEP, MON2, MON2.replace("""("gbp", ("£", "gbp", "libra", "libras")), ("jpy", ("¥", "jpy")), """, ""))], [B415]),
 "q3b_prefijo_sin_anclar": ("v4", "Q3", "el prefijo FY/AF/EJ deja de anclarse al principio de la palabra («Graf2023-2024» vuelve a leerse como intervalo)",
    [(VEP, MPREV, MPREV.replace(r""" or re.search(r"(?:^|[^\w.,])(?:FY|AF|EJ)""", r""" or re.search(r"(?:FY|AF|EJ)"""))], [B415]),
 "q3c_sin_rango_1900_2100": ("v4", "Q3", "se quita el rango 1900–2100 (basta que el segundo entero de cuatro cifras no sea menor: «1850-1860» se lee en positivo)",
    [(VEP, ANIOS, ANIOS.replace(RANGO, "int(m_prev.group(1)) <= int(tok)"))], [B415]),
 "q3d_sin_creciente": ("v4", "Q3", "se quita la condición de años crecientes (dos años plausibles en cualquier orden: «2024-2023» se lee en positivo)",
    [(VEP, ANIOS, ANIOS.replace(RANGO, "1900 <= int(m_prev.group(1)) <= 2100 and 1900 <= int(tok) <= 2100"))], [B415]),
 "q3e_rango_hasta_2099": ("v4", "Q3", "el rango acaba en 2099 («2099-2100» queda pendiente)",
    [(VEP, ANIOS, ANIOS.replace(RANGO, "1900 <= int(m_prev.group(1)) <= int(tok) <= 2099"))], [B415]),
 "t6a_sin_distancia_de_edicion": ("v4", "T6", "se quita la distancia de edición: las erratas dobles («emtrada_efectiba») vuelven a dejar el modo en «registrada» en silencio",
    [(PLP, " >= 0.88\n" + EDIC, " >= 0.88)]")], [BEE]),
 "t6b_distancia_1": ("v4", "T6", "la distancia de edición admitida baja a 1 (las erratas dobles que no llegan a 0,88 dejan de detectarse)",
    [(PLP, EDIC, EDIC.replace("<= 3)]", "<= 1)]"))], [BEE]),
 "t6c_distancia_2": ("v4", "T6", "la distancia de edición admitida baja a 2",
    [(PLP, EDIC, EDIC.replace("<= 3)]", "<= 2)]"))], [BEE]),
 "t8d_fecha_cualquier_cifra": ("v4", "T8", "la regla de la fecha vale para cualquier cifra que siga a «d-m-» (no solo un año de cuatro cifras): «5-6-849,7» se lee en positivo (sin detectar en la cuarta y en la quinta; el autor no declara prueba)",
    [(VEP, FECHA, FECHA.replace(r""" and re.fullmatch(r"\d{4}", tok) is not None""", ""))], [B415]),
}
