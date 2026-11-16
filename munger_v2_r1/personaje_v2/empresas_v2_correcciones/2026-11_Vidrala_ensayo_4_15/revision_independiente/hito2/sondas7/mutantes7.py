"""Definición de las MUTACIONES de la séptima comprobación (Fable, hito 2 de la 4.15, candidata 45ff57c): una regla quitada o alterada cada
vez. Las usan g5 (evaluación a nivel de unidad de las pruebas del bloque, cargando el código mutado en memoria) y mutaciones7.py (batería
ENTERA en un árbol ligero aparte, con el arnés de mutaciones4.py).
Grupos: «w1» = las diez mutaciones que la sexta comprobación dejó SIN detectar y para las que el autor añade ahora los casos de prueba
propuestos (v2a–v2c, v5a, v7a, v7c, v7d, v3b, t8d, t6c), adaptadas a las líneas de esta candidata; «w» = lo cambiado en esta candidata
(W3, W4 y W5), una pieza cada vez; «x1» = la línea :542 (límite inicial de la cifra en _lectura_cifra): la corrección que propone el
revisor (NO es una mutación: la batería tiene que pasar entera) y sus vecinas; «v» = vecinas de la sexta que siguen aplicando; «control»."""
VEP, PLP = "scripts/verificacion_entradas.py", "scripts/pipeline.py"
B415, BEE, B414 = "test_verificacion_entradas_415.py", "test_entrada_efectiva_415.py", "test_verificacion_entradas_414.py"
MARCAS = r"""                           r"\bcoronas?\b|\breal(?:es)?\b|\bfrancos?\b|\bmm€|\bmeur|\bkeur|\bk€)", re.I)  # (hito 2, V7) también «real»"""
MPREV = r"""        m_prev = re.search(r"(?:^|[^\w.,])(\d{4})\Z", previo) or re.search(r"(?:^|[^\w.,])(?:FY|AF|EJ)(\d{4})\Z", previo, re.I)"""
FECHA = r"""        fecha = re.search(r"(?:^|[^\w.,])\d{1,2}-\d{1,2}\Z", previo) is not None and re.fullmatch(r"\d{4}", tok) is not None  # «31-12-2024»"""
CORTE = """        if len(out) > MAX_APARICIONES_CITA:  # (hito 2, V5) basta saber que pasa del máximo: el coste queda acotado\n            break\n"""
# --- líneas que cambian en esta candidata
LIM1 = r"""    patron = ((r"(?<![\d.,])(?<!\d['’])" if re.match(r"\d", palabras[0]) else r"(?<![^\W\d_])" if re.match(r"[^\W\d_]", palabras[0]) else "") + patron  # (W4) apóstrofo"""
LIM2 = r"""              + (r"(?!\d|[.,'’]\d)" if re.search(r"\d$", palabras[-1]) else r"(?![^\W\d_])" if re.search(r"[^\W\d_]$", palabras[-1]) else ""))"""
LECT = r"""        for m in re.finditer(r"(?<![\d.,])(?<!\d[’])" + re.escape(c) + r"(?!\d|[.,'’]\d)", t):  # (hito 2, V7 y W3) «1'849,7» ni «1’849,7» contienen 849,7"""
ENNUM1 = r"""                return ((re.match(r"\d", palabras[0]) is not None and re.search(r"(?:\d|\d[.,'’]|(?:^|[^\w.,])[.,])\Z", antes2) is not None)"""
ENNUM2 = r"""                        or (re.search(r"\d$", palabras[-1]) is not None and re.match(r"\d|[.,'’]\d", t_[m.end():m.end() + 2]) is not None))  # (W4)"""
MENS = '''        return "signo_indeterminado", f"la cita aparece más de {MAX_APARICIONES_CITA} veces en la página: no identifica un pasaje; hay que citar un fragmento distintivo"  # (hito 2, W5)'''
EDIC = r"""                                                              or _ediciones(re.sub(r"[^a-z]", "", str(k).lower()), "entradaefectiva") <= 3)]"""
LECT_INI = r"""(?<![\d.,])(?<!\d[’])" + re.escape(c)"""
LECT_FIN = r"""(?!\d|[.,'’]\d)", t)"""

# nombre: (grupo, hallazgo, descripción, [(archivo, texto original, texto nuevo)], [baterías])
M = {
 "c00_control": ("control", "—", "control: sin cambio de regla (solo un comentario); las baterías tienen que pasar enteras en el árbol ligero",
    [(VEP, 'FORMATO = "4.15"', 'FORMATO = "4.15"  # control')], [BEE, B414, B415]),
 # ================================================================ W1 · las diez que la sexta dejó sin detectar
 "v2a_anio_anterior_con_dolar": ("w1", "V2", "el año anterior del intervalo vuelve a anclarse con «$» (el año al final de la línea anterior vuelve a hacer de «⏎-2024» un intervalo)",
    [(VEP, MPREV, MPREV.replace(r"(\d{4})\Z", r"(\d{4})$"))], [B415]),
 "v2b_fecha_con_dolar": ("w1", "V2", "la fecha vuelve a anclarse con «$» («Notas 5-6⏎-2024» vuelve a leerse como fecha)",
    [(VEP, FECHA, FECHA.replace(r"\d{1,2}-\d{1,2}\Z", r"\d{1,2}-\d{1,2}$"))], [B415]),
 "v2c_los_dos_con_dolar": ("w1", "V2", "las dos anclas vuelven a «$» (la regla de 876bfc2)",
    [(VEP, MPREV, MPREV.replace(r"(\d{4})\Z", r"(\d{4})$")), (VEP, FECHA, FECHA.replace(r"\d{1,2}-\d{1,2}\Z", r"\d{1,2}-\d{1,2}$"))], [B415]),
 "v5a_sin_corte": ("w1", "V5", "se quita el corte del recuento de apariciones (se recogen todas; el coste vuelve a crecer con el cuadrado en una línea)",
    [(VEP, CORTE, "")], [B415]),
 "v7a_en_numero_sin_apostrofo": ("w1", "V7", "en_numero deja de contar «cifra + apóstrofo» (ASCII y tipográfico) delante de la cita",
    [(VEP, ENNUM1, ENNUM1.replace(r"\d[.,'’]", r"\d[.,]"))], [B415]),
 "v7c_lectura_sin_apostrofo_detras": ("w1", "V7", "_lectura_cifra sin apóstrofo (ASCII ni tipográfico) en el límite final: «849» vuelve a leerse dentro de «849'697»",
    [(VEP, LECT, LECT.replace(LECT_FIN, r"""(?!\d|[.,]\d)", t)"""))], [B415]),
 "v7d_real_solo_plural": ("w1", "V7", "MARCAS_MONEDA vuelve a «reales?» («real», en singular, deja de ser una marca: «miles de real» no queda pendiente)",
    [(VEP, MARCAS, MARCAS.replace(r"\breal(?:es)?\b", r"\breales?\b"))], [B415]),
 "v3b_en_numero_con_dolar": ("w1", "V7", "en_numero vuelve a anclarse con «$» (una palabra cortada al principio de una línea, tras una línea que acaba en cifra, vuelve a discrepancia)",
    [(VEP, ENNUM1, ENNUM1.replace(r"[.,])\Z", r"[.,])$"))], [B415]),
 "t8d_fecha_cualquier_cifra": ("w1", "T8", "la regla de la fecha vale para cualquier cifra que siga a «d-m-» (no solo un año de cuatro cifras): «5-6-849,7» se lee en positivo",
    [(VEP, FECHA, FECHA.replace(r""" and re.fullmatch(r"\d{4}", tok) is not None""", ""))], [B415]),
 "t6c_distancia_2": ("w1", "T6", "la distancia de edición admitida baja a 2",
    [(PLP, EDIC, EDIC.replace("<= 3)]", "<= 2)]"))], [BEE]),
 # ================================================================ X1 · la línea :542 (límite inicial de la cifra en _lectura_cifra)
 "x1_correccion_propuesta": ("x1", "X1", "NO es una mutación: la corrección que propone el revisor («(?<!\\d['’])», ASCII y tipográfico, como proponía la sexta); la batería tiene que pasar ENTERA",
    [(VEP, LECT, LECT.replace(LECT_INI, r"""(?<![\d.,])(?<!\d['’])" + re.escape(c)""") + "  (séptima, propuesta del revisor)")], [B415, BEE, B414]),
 "x1a_lectura_sin_limite_apostrofo_delante": ("x1", "X1/W3", "_lectura_cifra sin NINGÚN apóstrofo en el límite inicial (se quita «(?<!\\d[’])»): «849,7» vuelve a leerse dentro de «1’849,7» (y de «1'849,7», que la candidata ya lee)",
    [(VEP, LECT, LECT.replace(LECT_INI, r"""(?<![\d.,])" + re.escape(c)"""))], [B415]),
 "x1b_lectura_solo_ascii_delante": ("x1", "W3", "el límite inicial de _lectura_cifra vuelve a ser el de 8196522 («(?<!\\d')», solo ASCII): se pierde W3 por delante",
    [(VEP, LECT, LECT.replace(LECT_INI, r"""(?<![\d.,])(?<!\d')" + re.escape(c)"""))], [B415]),
 # ================================================================ W3 · apóstrofo tipográfico en el límite final de _lectura_cifra
 "w3b_lectura_sin_tipografico_detras": ("w", "W3", "_lectura_cifra sin «’» en el límite final (queda el ASCII): «849» vuelve a leerse dentro de «849’697»",
    [(VEP, LECT, LECT.replace(LECT_FIN, r"""(?!\d|[.,']\d)", t)"""))], [B415]),
 "w3c_lectura_sin_ascii_detras": ("w", "V7", "_lectura_cifra sin el apóstrofo ASCII en el límite final (queda «’»): «849» vuelve a leerse dentro de «849'697»",
    [(VEP, LECT, LECT.replace(LECT_FIN, r"""(?!\d|[.,’]\d)", t)"""))], [B415]),
 # ================================================================ W4 · límites de la cita y final de en_numero
 "w4a_cita_sin_apostrofo_delante": ("w", "W4", "_apariciones_en_pagina sin el límite «cifra + apóstrofo» por delante (los límites de la cita de 8196522): «849,7» vuelve a contar como aparición en «1'849,7»",
    [(VEP, LIM1, LIM1.replace(r"""(?<![\d.,])(?<!\d['’])""", r"""(?<![\d.,])"""))], [B415]),
 "w4b_cita_sin_apostrofo_detras": ("w", "W4", "_apariciones_en_pagina sin apóstrofo en el límite final: «Total 849» vuelve a contar como aparición en «Total 849'697»",
    [(VEP, LIM2, LIM2.replace(r"""(?!\d|[.,'’]\d)""", r"""(?!\d|[.,]\d)"""))], [B415]),
 "w4c_en_numero_final_sin_apostrofo": ("w", "W4", "el final de en_numero sin apóstrofo («otal 849» ante «'697» vuelve a quedar pendiente en vez de discrepancia)",
    [(VEP, ENNUM2, ENNUM2.replace(r"""\d|[.,'’]\d""", r"""\d|[.,]\d"""))], [B415]),
 "w4d_en_numero_inicio_sin_tipografico": ("w", "W4", "el principio de en_numero sin «’» (queda el ASCII)",
    [(VEP, ENNUM1, ENNUM1.replace(r"\d[.,'’]", r"\d[.,']"))], [B415]),
 "w4e_cita_delante_solo_ascii": ("w", "W4", "el límite inicial de la cita solo con el apóstrofo ASCII («849,7» vuelve a contar como aparición en «1’849,7»)",
    [(VEP, LIM1, LIM1.replace(r"""(?<!\d['’])""", r"""(?<!\d['])"""))], [B415]),
 "w4f_cita_delante_solo_tipografico": ("w", "W4", "el límite inicial de la cita solo con «’» («849,7» vuelve a contar como aparición en «1'849,7»: con la :542 de la candidata, vuelve a leerse)",
    [(VEP, LIM1, LIM1.replace(r"""(?<!\d['’])""", r"""(?<!\d[’])"""))], [B415]),
 "w4g_cita_detras_solo_ascii": ("w", "W4", "el límite final de la cita solo con el apóstrofo ASCII",
    [(VEP, LIM2, LIM2.replace(r"""(?!\d|[.,'’]\d)""", r"""(?!\d|[.,']\d)"""))], [B415]),
 "w4h_cita_detras_solo_tipografico": ("w", "W4", "el límite final de la cita solo con «’»",
    [(VEP, LIM2, LIM2.replace(r"""(?!\d|[.,'’]\d)""", r"""(?!\d|[.,’]\d)"""))], [B415]),
 # ================================================================ W5 · mensaje del máximo
 "w5a_mensaje_antiguo": ("w", "W5", "el mensaje del máximo vuelve a decir «aparece {len(apar)} veces» (201, sea cual sea el número)",
    [(VEP, MENS, MENS.replace("más de {MAX_APARICIONES_CITA} veces", "{len(apar)} veces"))], [B415]),
 # ================================================================ vecinas de la sexta que siguen aplicando (detectadas entonces)
 "v3a_sin_decimal_sin_cero": ("v", "V3", "en_numero deja de contar el punto o la coma que empiezan una «palabra» («(.5)» citada «5» vuelve a quedar pendiente)",
    [(VEP, ENNUM1, ENNUM1.replace(r"(?:\d|\d[.,'’]|(?:^|[^\w.,])[.,])\Z", r"(?:\d|\d[.,'’])\Z"))], [B415]),
 "v5b_corte_en_el_maximo": ("v", "V5", "el corte salta al LLEGAR al máximo (≥ en vez de >): se devuelven 200 apariciones",
    [(VEP, CORTE, CORTE.replace("len(out) > MAX_APARICIONES_CITA", "len(out) >= MAX_APARICIONES_CITA"))], [B415]),
}
