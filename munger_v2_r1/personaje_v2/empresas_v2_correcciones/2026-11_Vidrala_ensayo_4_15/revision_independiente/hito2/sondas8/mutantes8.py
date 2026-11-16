"""Octava comprobación · definiciones de las mutaciones de `fase1_historia.importe_completo` (X5). Cada una sustituye la línea del «return».
SENTIDO: «acepta» = la mutación deja pasar algo que la candidata rechaza (la prueba debe verla); «prudente» = rechaza de más."""
T = "’"
LINEA = r'''    return re.search(r"(?<![\d.,])(?<!\d['’])" + re.escape(imp) + r"(?![\d.,'’]*\d)", texto) is not None'''


def _l(delante, detras):
    return '    return re.search(r"' + delante + '" + re.escape(imp) + r"' + detras + '", texto) is not None'


D_OK, T_OK = r"(?<![\d.,])(?<!\d['’])", r"(?![\d.,'’]*\d)"
D_ANT, T_ANT = r"(?<![\d.,])", r"(?![\d.,]*\d)"
MUT = {  # nombre: (línea nueva, sentido, qué es)
    "m0_sin_el_cambio": (_l(D_ANT, T_ANT), "acepta", "se quita el cambio entero (la línea de 45ff57c)"),
    "m1_solo_delante": (_l(D_OK, T_ANT), "acepta", "el apóstrofo solo cuenta por delante: «849» vuelve a valer dentro de «849'697»"),
    "m2_solo_detras": (_l(D_ANT, T_OK), "acepta", "el apóstrofo solo cuenta por detrás: «849,7» vuelve a valer dentro de «1'849,7»"),
    "m3_solo_ascii": (_l(r"(?<![\d.,])(?<!\d['])", r"(?![\d.,']*\d)"), "acepta", "solo el apóstrofo ASCII, en los dos lados (se pierde «’»)"),
    "m4_solo_tipografico": (_l(r"(?<![\d.,])(?<!\d[’])", r"(?![\d.,’]*\d)"), "acepta", "solo «’», en los dos lados (se pierde el ASCII)"),
    "m5_delante_solo_ascii": (_l(r"(?<![\d.,])(?<!\d['])", T_OK), "acepta", "por delante solo ASCII; por detrás, los dos"),
    "m6_delante_solo_tipografico": (_l(r"(?<![\d.,])(?<!\d[’])", T_OK), "acepta", "por delante solo «’»; por detrás, los dos (el descuido de X1, aquí)"),
    "m7_detras_solo_ascii": (_l(D_OK, r"(?![\d.,']*\d)"), "acepta", "por detrás solo ASCII; por delante, los dos"),
    "m8_detras_solo_tipografico": (_l(D_OK, r"(?![\d.,’]*\d)"), "acepta", "por detrás solo «’»; por delante, los dos"),
    "m9_detras_un_solo_separador": (_l(D_OK, r"(?!\d|[.,'’]\d)"), "acepta", "por detrás, la forma de verificacion_entradas (un solo separador y una cifra): «7» valdría en «7,,6» o «7.'6»"),
    "s1_delante_apostrofo_sin_cifra": (_l(r"(?<![\d.,'’])", T_OK), "prudente", "cualquier apóstrofo delante bloquea, aunque no haya cifra antes («d’1,5»)"),
    "s2_detras_apostrofo_sin_cifra": (_l(D_OK, r"(?![\d.,'’]*\d|['’])"), "prudente", "cualquier apóstrofo detrás bloquea, aunque no siga cifra («120’s»)"),
    "s3_apostrofo_en_cualquier_sitio": (_l(D_OK, r"(?![\d.,'’]*\d)(?![^'’]*['’])"), "prudente", "un apóstrofo en cualquier punto posterior de la línea bloquea"),
}
assert all(v[0] != LINEA for v in MUT.values()) and len({v[0] for v in MUT.values()}) == len(MUT)
