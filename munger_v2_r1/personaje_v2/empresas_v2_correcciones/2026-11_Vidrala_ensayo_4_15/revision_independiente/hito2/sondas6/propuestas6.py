#!/usr/bin/env python3
"""Propuestas del revisor de la SEXTA comprobación, aplicadas sobre copias ligeras del código de 8196522. NO es código entregado ni
revisado: sirve para comprobar que lo que se propone es compatible con las baterías y con los registros reales. Nunca toca el árbol congelado.
  prop6t · SOLO PRUEBAS (lo mínimo que se recomienda antes de cerrar): W1 — los casos de V2 con la cita que abarca las dos líneas; V5 con
           una aserción de estructura (apariciones devueltas), no solo de reloj; y, de paso, los casos que fijan el apóstrofo por detrás,
           el doble corte, «\\Z» de en_numero, «real» en singular, la fecha con una cifra que no es un año (t8d) y una clave a tres ediciones (T6).
           El número de pruebas no cambia (190 y 61).
  prop6  · prop6t + CÓDIGO: W3 y W4 — el apóstrofo tipográfico «’» junto al ASCII en los límites de la cifra (_lectura_cifra), de la cita
           (_apariciones_en_pagina) y de en_numero (principio y final); W5 — el mensaje del máximo dice «más de N veces».
Uso: python3 -I -B propuestas6.py   (escribe fable/prop6t y fable/prop6, y los diff en salidas/)"""
import os, shutil, subprocess
F = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COPIA = os.path.join(F, "copia", "munger_v2_r1")
T415, TEE, VEP = "pruebas/test_verificacion_entradas_415.py", "pruebas/test_entrada_efectiva_415.py", "scripts/verificacion_entradas.py"

PRUEBAS = [
    (T415, '''v1 = {"coronas/DKK": True, "francos/CHF": True, "reales/BRL": True, "corona/coronas": True, "libras/GBP": True, "JPY/¥": True, "DKK/SEK": False, "CHF/EUR": False}''',
           '''v1 = {"coronas/DKK": True, "francos/CHF": True, "reales/BRL": True, "corona/coronas": True, "libras/GBP": True, "JPY/¥": True, "DKK/SEK": False, "CHF/EUR": False,
      "miles de real": True}  # (propuesta del revisor, W1) «real» en singular'''),
    (T415, '''v2 = {("2024", 2024, "Ejercicio 2023\\n-2024"): "signo_distinto", ("2024", 2024, "Cierre 31-12\\n-2024"): "signo_distinto"}''',
           '''v2 = {("Ejercicio 2023 -2024", 2024, "Ejercicio 2023\\n-2024"): "signo_distinto", ("Cierre 31-12 -2024", 2024, "Cierre 31-12\\n-2024"): "signo_distinto",
      ("2024", 2024, "Ejercicio 2023\\n-2024"): "signo_distinto"}  # (propuesta del revisor, W1) la cita abarca las dos líneas: es lo que distingue «\\Z» de «$»'''),
    (T415, '''       ("2099-2100", 2100): "ok", ("AF2023-2024", 2024): "ok"}''',
           '''       ("2099-2100", 2100): "ok", ("AF2023-2024", 2024): "ok", ("Notas 5-6-849,7", 849.7): "signo_indeterminado"}  # (propuesta del revisor, W1) la fecha exige un año'''),
    (T415, '''v3 = {(".5", 0.5, "Ajuste .5"): "ausente", ("5", 5, "Ajuste (.5)"): "ausente", ("849,7", 849.7, "Total 1'849,7"): "ausente"}''',
           '''v3 = {(".5", 0.5, "Ajuste .5"): "ausente", ("5", 5, "Ajuste (.5)"): "ausente", ("849,7", 849.7, "Total 1'849,7"): "ausente",
      # (propuesta del revisor, W1) el decimal sin cero citado desde la cifra, el apóstrofo por detrás, el doble corte y «\\Z» en en_numero
      ("5 veces", 5, "Ratio .5 veces"): "ausente", ("Total 849", 849, "Total 849'697"): "ausente", ("849,7 mill", 849.7, "Total 1'849,7 millones"): "ausente",
      ("849,7 mill", 849.7, "Ventas 2023\\n849,7 millones"): "no_localizada"}'''),
    (T415, '''paso("RW", "(V5) 100.000 apariciones de una cita en una línea: se deja de contar al pasar del máximo (tiempo acotado) y queda pendiente", r_v5[0] == "signo_indeterminado" and _time.time() - t0 < 5,''',
           '''n_v5 = len(VE._apariciones_en_pagina("Total: 5.5", " ".join(["Total: 5.5"] * 1000)))  # (propuesta del revisor, W1) estructura, no reloj
paso("RW", "(V5) 100.000 apariciones de una cita en una línea: se deja de contar al pasar del máximo (tiempo acotado) y queda pendiente", r_v5[0] == "signo_indeterminado" and n_v5 == VE.MAX_APARICIONES_CITA + 1 and _time.time() - t0 < 5,'''),
    (TEE, '''for errata_doble in ("entrdaefectivaa", "Entrada_Efectiv", "entrada_efectvia", "emtrada_efectiba", "ehtrada_efectiwa"):''',
          '''for errata_doble in ("entrdaefectivaa", "Entrada_Efectiv", "entrada_efectvia", "emtrada_efectiba", "ehtrada_efectiwa", "emtrada_efextiba"):  # (propuesta del revisor, W1) la última, a tres ediciones'''),
]
CODIGO = [
    # W3 y W4: el apóstrofo tipográfico junto al ASCII, y también en los límites de la cita y en el final de en_numero
    (VEP, r"""        for m in re.finditer(r"(?<![\d.,])(?<!\d')" + re.escape(c) + r"(?!\d|[.,']\d)", t):  # (hito 2, V7) «1'849,7» no contiene 849,7""",
          r"""        for m in re.finditer(r"(?<![\d.,])(?<!\d['’])" + re.escape(c) + r"(?!\d|[.,'’]\d)", t):  # (hito 2, V7) «1'849,7» no contiene 849,7 (propuesta del revisor, W3: también «’»)"""),
    (VEP, r"""    patron = ((r"(?<![\d.,])" if re.match(r"\d", palabras[0]) else r"(?<![^\W\d_])" if re.match(r"[^\W\d_]", palabras[0]) else "") + patron""",
          r"""    patron = ((r"(?<![\d.,])(?<!\d['’])" if re.match(r"\d", palabras[0]) else r"(?<![^\W\d_])" if re.match(r"[^\W\d_]", palabras[0]) else "") + patron  # (propuesta del revisor, W4)"""),
    (VEP, r"""              + (r"(?!\d|[.,]\d)" if re.search(r"\d$", palabras[-1]) else r"(?![^\W\d_])" if re.search(r"[^\W\d_]$", palabras[-1]) else ""))""",
          r"""              + (r"(?!\d|[.,'’]\d)" if re.search(r"\d$", palabras[-1]) else r"(?![^\W\d_])" if re.search(r"[^\W\d_]$", palabras[-1]) else ""))"""),
    (VEP, r"""                return ((re.match(r"\d", palabras[0]) is not None and re.search(r"(?:\d|\d[.,']|(?:^|[^\w.,])[.,])\Z", antes2) is not None)""",
          r"""                return ((re.match(r"\d", palabras[0]) is not None and re.search(r"(?:\d|\d[.,'’]|(?:^|[^\w.,])[.,])\Z", antes2) is not None)"""),
    (VEP, r"""                        or (re.search(r"\d$", palabras[-1]) is not None and re.match(r"\d|[.,]\d", t_[m.end():m.end() + 2]) is not None))""",
          r"""                        or (re.search(r"\d$", palabras[-1]) is not None and re.match(r"\d|[.,'’]\d", t_[m.end():m.end() + 2]) is not None))  # (propuesta del revisor, W4)"""),
    # W5: el mensaje no afirma un recuento que ya no se hace
    (VEP, '''        return "signo_indeterminado", f"la cita aparece {len(apar)} veces en la página: no identifica un pasaje; hay que citar un fragmento distintivo"''',
          '''        return "signo_indeterminado", f"la cita aparece más de {MAX_APARICIONES_CITA} veces en la página: no identifica un pasaje; hay que citar un fragmento distintivo"  # (propuesta del revisor, W5)'''),
]


def construir(nombre, cambios):
    dst = os.path.join(F, nombre, "munger_v2_r1")
    if os.path.lexists(os.path.join(F, nombre)):
        raise SystemExit(f"{nombre} ya existe: bórrese a mano si se quiere rehacer")
    os.makedirs(os.path.join(dst, "personaje_v2"))
    for x in os.listdir(COPIA):
        if x != "personaje_v2":
            os.symlink(os.path.realpath(os.path.join(COPIA, x)), os.path.join(dst, x))
    for x in os.listdir(os.path.join(COPIA, "personaje_v2")):
        o, n = os.path.join(COPIA, "personaje_v2", x), os.path.join(dst, "personaje_v2", x)
        if x in ("scripts", "pruebas", "esquema"):
            shutil.copytree(o, n, ignore=shutil.ignore_patterns("__pycache__"), symlinks=True)
        else:
            os.symlink(os.path.realpath(o), n)
    for arch, viejo, nuevo in cambios:
        p = os.path.join(dst, "personaje_v2", arch)
        s = open(p, encoding="utf-8").read()
        assert s.count(viejo) == 1, (nombre, arch, viejo[:70], s.count(viejo))
        open(p, "w", encoding="utf-8").write(s.replace(viejo, nuevo))
    d = subprocess.run(["diff", "-ru", os.path.join("copia", "munger_v2_r1", "personaje_v2"), os.path.join(nombre, "munger_v2_r1", "personaje_v2"), "-x", "__pycache__",
                        "-x", "empresas_v2*", "-x", "corpus", "-x", "prompts"], cwd=F, capture_output=True, text=True).stdout
    open(os.path.join(F, "salidas", f"propuestas6_{nombre}.diff"), "w", encoding="utf-8").write(d)
    print(f"{nombre}: {len(cambios)} cambios · {len(d.splitlines())} líneas de diff")


if __name__ == "__main__":
    construir("prop6t", PRUEBAS)
    construir("prop6", PRUEBAS + CODIGO)
