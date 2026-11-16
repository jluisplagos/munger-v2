#!/usr/bin/env python3
"""Mutaciones de la QUINTA comprobación (Fable, hito 2 de la 4.15, candidata 876bfc2). Usa el arnés de mutaciones4.py (preparar y correr:
un árbol ligero aparte por mutación, con scripts/, pruebas/ y esquema/ copiados de «copia» y el resto enlaces; baterías permitidas, sin
LibreOffice). Solo las mutaciones relevantes para esta comprobación:
  «q2» = las que la cuarta comprobación dejó SIN detectar y para las que el autor dice haber añadido prueba ahora (T3, T6, T7, N3, N10);
  «q»  = las reglas que entran con esta candidata (Q1, Q3, Q4), una condición cada vez;
  «t»  = reglas de la cuarta cuyas líneas se han reescrito ahora (prefijo FY, fecha, en_numero), adaptadas al código actual.
Resultados en mut5/<nombre>/resultado.json (se guardan al terminar cada una; «pendientes» repite solo lo que falta).
Uso: python3 -I -B mutaciones5.py [-j N] NOMBRE [NOMBRE …] | todas | q2 | q | t | control | pendientes | lista"""
import concurrent.futures, json, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
F = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(F, "sondas4"))
import mutaciones4 as m4  # noqa: E402
assert m4.F == F and m4.COPIA == os.path.join(F, "copia", "munger_v2_r1")
m4.MUT = os.path.join(F, "mut5")
B415, BEE, B414, VEP, FIP, PLP = m4.B415, m4.BEE, m4.B414, m4.VEP, m4.FIP, m4.PLP

PAR = r"""    tipo_cambio = (par is not None and _moneda_de(par.group("a")) != _moneda_de(par.group("b"))  # (hito 2, Q1) dos monedas DISTINTAS: «euros/EUR» no es un tipo de cambio"""
MON1 = """    for cod, formas in (("eur", ("€", "eur", "euro", "euros")), ("usd", ("$", "usd", "dólar", "dolar", "dólares", "dolares")),"""
MON2 = """                        ("gbp", ("£", "gbp", "libra", "libras")), ("jpy", ("¥", "jpy"))):"""
MPREV = r"""        m_prev = re.search(r"(?:^|[^\w.,])(\d{4})$", previo) or re.search(r"(?:^|[^\w.,])(?:FY|AF|EJ)(\d{4})$", previo, re.I)"""
ANIOS = r"""        anios = (m_prev is not None and re.fullmatch(r"\d{4}", tok) is not None and 1900 <= int(m_prev.group(1)) <= int(tok) <= 2100)"""
RANGO = "1900 <= int(m_prev.group(1)) <= int(tok) <= 2100"
FECHA = r"""        fecha = re.search(r"(?:^|[^\w.,])\d{1,2}-\d{1,2}$", previo) is not None and re.fullmatch(r"\d{4}", tok) is not None  # «31-12-2024»"""
ENNUM1 = r"""                return ((re.match(r"\d", palabras[0]) is not None and re.search(r"(?:\d|\d[.,])$", antes2) is not None)"""
ENNUM2 = m4.ENNUM2
MAXCHK = "    if len(apar) > MAX_APARICIONES_CITA:"
MAXDEF = "MAX_APARICIONES_CITA = 200  # (hito 2, Q4)"
RECORTE = "        ini, fin = max(ini, m.start() - 400), min(fin, m.end() + 400)"

M = {
 "c00_control": m4.M["c00_control"],
 # ================================================================ q2 · sin detectar en la cuarta comprobación; el autor añade prueba ahora
 "t3a_xhtml_por_contenido": ("q2",) + m4.M["t3a_xhtml_por_contenido"][1:],
 "t3d_codecs_por_prefijos": ("q2",) + m4.M["t3d_codecs_por_prefijos"][1:],
 "n3c_solo_signo_distinto": ("q2",) + m4.M["n3c_solo_signo_distinto"][1:],
 "n10c_sin_recorte_400": ("q2",) + m4.M["n10c_sin_recorte_400"][1:],
 "t6a_sin_distancia_de_edicion": ("q2",) + m4.M["t6a_sin_distancia_de_edicion"][1:],
 "t6b_distancia_1": ("q2",) + m4.M["t6b_distancia_1"][1:],
 "t7a_resumen_sin_actualizar": ("q2",) + m4.M["t7a_resumen_sin_actualizar"][1:],
 # ================================================================ Q1 · el par tiene que ser de dos monedas distintas
 "q1a_sin_monedas_distintas": ("q", "Q1", "se quita la condición de que las dos monedas del par sean distintas (la regla de 7a6583b: «euros/EUR» vuelve a quedar exenta)",
    [(VEP, PAR, PAR.replace(""" and _moneda_de(par.group("a")) != _moneda_de(par.group("b"))""", ""))], [B415]),
 "q1b_moneda_solo_eur": ("q", "Q1", "_moneda_de solo normaliza el euro (sin USD, GBP ni JPY: «USD/$», «libras/GBP» y «JPY/¥» vuelven a quedar exentas)",
    [(VEP, MON1 + "\n" + MON2, """    for cod, formas in (("eur", ("€", "eur", "euro", "euros")),):""")], [B415]),
 "q1c_moneda_sin_gbp_jpy": ("q", "Q1", "_moneda_de no normaliza la libra ni el yen («libras/GBP», «GBP/£» y «JPY/¥» vuelven a quedar exentas)",
    [(VEP, MON1 + "\n" + MON2, MON1[:-1] + "):")], [B415]),
 # ================================================================ Q3 · intervalo solo entre años crecientes y plausibles; prefijo anclado
 "q3a_intervalo_regla_anterior": ("q", "Q3", "el intervalo vuelve a la regla de 7a6583b (dos enteros de la misma longitud; prefijo FY/AF/EJ sin anclar)",
    [(VEP, MPREV, r"""        m_prev = re.search(r"(?:^|[^\w.,])(\d{1,4})$", previo) or re.search(r"(?:FY|AF|EJ)(\d{4})$", previo, re.I)"""),
     (VEP, ANIOS, r"""        anios = bool(m_prev and re.fullmatch(r"\d{1,4}", tok) and len(m_prev.group(1)) == len(tok))""")], [B415]),
 "q3b_prefijo_sin_anclar": ("q", "Q3", "el prefijo FY/AF/EJ deja de anclarse al principio de la palabra («Graf2023-2024» vuelve a leerse como intervalo)",
    [(VEP, MPREV, MPREV.replace(r""" or re.search(r"(?:^|[^\w.,])(?:FY|AF|EJ)""", r""" or re.search(r"(?:FY|AF|EJ)"""))], [B415]),
 "q3c_sin_rango_1900_2100": ("q", "Q3", "se quita el rango 1900–2100 (basta que el segundo entero de cuatro cifras no sea menor: «Saldo 2023-2849» se lee en positivo)",
    [(VEP, ANIOS, ANIOS.replace(RANGO, "int(m_prev.group(1)) <= int(tok)"))], [B415]),
 "q3d_sin_creciente": ("q", "Q3", "se quita la condición de años crecientes (dos años plausibles en cualquier orden: «Saldo 2023-1950» se lee en positivo)",
    [(VEP, ANIOS, ANIOS.replace(RANGO, "1900 <= int(m_prev.group(1)) <= 2100 and 1900 <= int(tok) <= 2100"))], [B415]),
 # ================================================================ Q4 · en_numero con los caracteres vecinos y máximo de apariciones
 "q4a_en_numero_regla_anterior": ("q", "Q4", "en_numero vuelve a la regla de 7a6583b (cualquier punto, coma o cifra delante, mirando todo el texto anterior)",
    [(VEP, ENNUM1, r"""                return ((re.match(r"\d", palabras[0]) is not None and re.search(r"[\d.,]$", t_[:m.start()]) is not None)""")], [B415]),
 "q4b_sin_maximo_de_apariciones": ("q", "Q4", "se quita el máximo de apariciones de la cita (se leen todas, por muchas que sean)",
    [(VEP, MAXCHK, "    if False:")], [B415]),
 "q4c_en_numero_solo_cifra_pegada": ("q", "Q4", "en_numero solo mira si hay una cifra pegada delante (un separador de miles o decimal delante deja de contar: «1.849,7» citada «849,7» queda pendiente, no discrepancia)",
    [(VEP, ENNUM1, ENNUM1.replace(r"(?:\d|\d[.,])$", r"\d$"))], [B415]),
 "q4d_maximo_100": ("q", "Q4", "el máximo de apariciones baja a 100 (una cita legítima con 150 apariciones iguales en una línea queda pendiente)",
    [(VEP, MAXDEF, "MAX_APARICIONES_CITA = 100  # (hito 2, Q4)")], [B415]),
 # ================================================================ reglas de la cuarta cuyas líneas se reescriben ahora
 "t8b_sin_prefijo_fy": ("t", "T8", "sin el prefijo FY/AF/EJ: «FY2023-2024» vuelve a quedar pendiente (adaptada a la línea nueva)",
    [(VEP, MPREV, MPREV.replace(r""" or re.search(r"(?:^|[^\w.,])(?:FY|AF|EJ)(\d{4})$", previo, re.I)""", ""))], [B415]),
 "t8c_sin_fecha": ("t", "T8", "sin la regla de la fecha: «31-12-2024» deja de leerse como fecha (adaptada)",
    [(VEP, FECHA, "        fecha = False")], [B415]),
 "t8d_fecha_cualquier_cifra": ("t", "T8", "la regla de la fecha vale para cualquier cifra que siga a «d-m-» (no solo un año de cuatro cifras): «5-6-849,7» se lee en positivo (adaptada; sin detectar en la cuarta)",
    [(VEP, FECHA, FECHA.replace(r""" and re.fullmatch(r"\d{4}", tok) is not None""", ""))], [B415]),
 "t2h_en_numero_sin_inicio": ("t", "T2", "el corte dentro de un número solo se mira al FINAL de la cita (adaptada a la línea nueva de en_numero)",
    [(VEP, ENNUM1 + "\n" + ENNUM2, "                return (False\n" + ENNUM2)], [B415]),
}
m4.M = M

if __name__ == "__main__":
    args = sys.argv[1:]
    j = 1
    if args[:1] == ["-j"]:
        j, args = int(args[1]), args[2:]
    mal = m4.comprobar_textos()
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
    elif len(args) == 1 and args[0] in ("q2", "q", "t", "control"):
        nombres = [k for k, v in M.items() if v[0] == args[0]]
    elif args == ["pendientes"]:
        nombres = [k for k in M if not os.path.exists(os.path.join(m4.MUT, k, "resultado.json"))]
    else:
        nombres = args
    with concurrent.futures.ThreadPoolExecutor(max_workers=j) as ex:
        for r in ex.map(m4.correr, nombres):
            print(json.dumps(r, ensure_ascii=False))
            sys.stdout.flush()
