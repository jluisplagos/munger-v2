#!/usr/bin/env python3
"""Propuestas del revisor para T1–T4 (tercera pasada), aplicadas JUNTAS sobre una copia ligera del código de la candidata f3d15e8
(fable/prop/: scripts, pruebas y esquema copiados; el resto, enlaces). NO es código entregado ni revisado: sirve para ver si las propuestas
son compatibles con las baterías permitidas y con los registros reales. Nunca toca el árbol congelado.
Uso: python3 -I -B propuestas3.py preparar   (después se ejecutan las baterías y las sondas con PV=<fable>/prop/munger_v2_r1/personaje_v2)"""
import os, shutil, sys
F = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COPIA = os.path.join(F, "copia", "munger_v2_r1")
PROP = os.path.join(F, "prop", "munger_v2_r1")
VEP = "scripts/verificacion_entradas.py"

CAMBIOS = [
 # ---- T1: la exención del tipo de cambio, solo si la unidad ENTERA es un par de monedas y no lleva palabra de escala
 ("T1", VEP,
  '    tipo_cambio = re.search(r"(por|per|/)\\s*" + MARCAS_MONEDA.pattern, t, re.I) is not None or "tipo de cambio" in t or "exchange rate" in t\n',
  '    _m = MARCAS_MONEDA.pattern  # (PROPUESTA T1) solo un par de monedas, con «tipo de cambio» delante o sin él, y sin palabra de escala\n'
  '    tipo_cambio = (re.fullmatch(r"(?:(?:tipo de cambio|exchange rate)\\b)?[\\s:(]*" + _m + r"\\s*(?:por|per|/)\\s*" + _m + r"[\\s)]*", t, re.I) is not None\n'
  '                   and re.search(r"miles|millones|millares|thousand|million|billion|\\bmm\\b|\\bbn\\b|mm€|meur|keur|k€|m€|€m|€000", t, re.I) is None)\n'),
 # ---- T2: límites de la cita según la clase del carácter (cifra: no pegada a otra cifra; letra: no pegada a otra letra)
 ("T2", VEP,
  '    patron = (r"(?<![\\w.,])" if re.match(r"\\w", palabras[0]) else "") + patron + (r"(?!\\w|[.,]\\d)" if re.search(r"\\w$", palabras[-1]) else "")\n',
  '    # (PROPUESTA T2) si la cita empieza o acaba en una cifra, no va pegada a otra cifra ni a un separador con cifra; si empieza o acaba en\n'
  '    # una letra, no va pegada a otra letra («849.7» cuenta en «849.7m»; «Total 5» no cuenta en «Subtotal 5,01»)\n'
  '    patron = ((r"(?<![\\d.,])" if re.match(r"\\d", palabras[0]) else r"(?<![^\\W\\d_])" if re.match(r"[^\\W\\d_]", palabras[0]) else "") + patron\n'
  '              + (r"(?!\\d|[.,]\\d)" if re.search(r"\\d$", palabras[-1]) else r"(?![^\\W\\d_])" if re.search(r"[^\\W\\d_]$", palabras[-1]) else ""))\n'),
 ("T2", VEP,
  '        if palabras and re.search(r"\\s+".join(re.escape(w) for w in palabras), t_, re.I):\n'
  '            # (hito 2, N10 y R3) la cita solo está como fragmento de una palabra o de una cifra de la página: la cifra citada no es la publicada\n'
  '            return "ausente", "la cita empieza o acaba dentro de una palabra o de una cifra de la página: no es una cifra completa de la página"\n',
  '        sucias = list(re.finditer(r"\\s+".join(re.escape(w) for w in palabras), t_, re.I)) if palabras else []\n'
  '        if sucias:\n'
  '            # (PROPUESTA T2) «ausente» (discrepancia) solo si el corte cae dentro de un NÚMERO; dentro de una palabra, pendiente\n'
  '            def _en_numero(m):\n'
  '                return ((re.match(r"\\d", palabras[0]) is not None and re.search(r"[\\d.,]$", t_[:m.start()]) is not None)\n'
  '                        or (re.search(r"\\d$", palabras[-1]) is not None and re.match(r"\\d|[.,]\\d", t_[m.end():m.end() + 2]) is not None))\n'
  '            if any(_en_numero(m) for m in sucias):\n'
  '                return "ausente", "la cita empieza o acaba dentro de una cifra de la página: no es una cifra completa de la página"\n'
  '            return "no_localizada", "la cita empieza o acaba dentro de una palabra de la página: se cita el fragmento completo"\n'),
 # ---- T3: modo XML por la extensión del archivo; codificaciones enumeradas
 ("T3", VEP,
  """            self.xhtml = cab.lstrip().startswith("<?xml") or 'xmlns="http://www.w3.org/1999/xhtml"' in cab\n""",
  '            self.xhtml = str(ruta).lower().endswith((".xhtml", ".xht"))  # (PROPUESTA T3) como abre el archivo un navegador\n'),
 ("T3", VEP,
  'nombre.startswith(("utf-", "cp125", "cp4", "cp8", "iso8859-", "mac-", "koi8", "euc_", "iso2022_")) or nombre in ("shift_jis", "gb2312", "gbk", "gb18030", "big5", "big5hkscs")',
  'nombre.startswith(("utf-", "cp125", "iso8859-", "mac-", "koi8")) or nombre in ("shift_jis", "euc_jp", "euc_kr", "iso2022_jp", "gb2312", "gbk", "gb18030", "big5", "big5hkscs", "cp866", "cp874", "cp437", "cp850", "cp852", "cp858")'),
 # ---- T4: la lectura en el documento, sin los caracteres invisibles del HTML, y pendiente si la cita no se localiza en ningún texto del documento
 ("T4", VEP,
  '        if est_h == "ok":\n            textos_fuente.append(plano)\n',
  '        if est_h == "ok":\n            textos_fuente.append(re.sub("[\\u00ad\\u200b\\u200c\\u200d\\u2060\\ufeff]", "", plano))  # (PROPUESTA T4) como _cmp_txt_espacios\n'),
 ("T4", VEP,
  '            otras = [x for x in (_cita_cifra(f.get("cita"), vf, tf) for tf in textos_fuente) if x[0] != "no_localizada"]\n'
  '            peor = next((x for x in otras if x[0] in ("signo_distinto", "ausente")), None) or next((x for x in otras if x[0] != "ok"), None)\n'
  '            if peor:\n'
  '                est, det = peor[0], peor[1] + " (en el documento de la fuente, no en el texto conservado)"\n',
  '            lect = [_cita_cifra(f.get("cita"), vf, tf) for tf in textos_fuente]\n'
  '            otras = [x for x in lect if x[0] != "no_localizada"]\n'
  '            peor = next((x for x in otras if x[0] in ("signo_distinto", "ausente")), None) or next((x for x in otras if x[0] != "ok"), None)\n'
  '            if peor:\n'
  '                est, det = peor[0], peor[1] + " (en el documento de la fuente, no en el texto conservado)"\n'
  '            elif lect and not otras:  # (PROPUESTA T4) la cita está en el documento, pero no con sus palabras: no se puede leer el signo en él\n'
  '                est, det = "no_localizada", "la cita está en el documento de la fuente, pero no con sus palabras separadas igual: la cifra y su signo no pueden leerse en él"\n'),
]


def preparar(solo=None):
    if os.path.lexists(os.path.dirname(PROP)):
        shutil.rmtree(os.path.dirname(PROP))
    os.makedirs(os.path.join(PROP, "personaje_v2"))
    for x in os.listdir(COPIA):
        if x != "personaje_v2":
            os.symlink(os.path.realpath(os.path.join(COPIA, x)), os.path.join(PROP, x))
    for x in os.listdir(os.path.join(COPIA, "personaje_v2")):
        o, n = os.path.join(COPIA, "personaje_v2", x), os.path.join(PROP, "personaje_v2", x)
        if x in ("scripts", "pruebas", "esquema"):
            shutil.copytree(o, n, ignore=shutil.ignore_patterns("__pycache__", "sintetico", "resultados_reparacion", "_v64"))
        else:
            os.symlink(os.path.realpath(o), n)
    for etq, arch, viejo, nuevo in CAMBIOS:
        if solo and etq not in solo:
            continue
        p = os.path.join(PROP, "personaje_v2", arch)
        s = open(p, encoding="utf-8").read()
        assert s.count(viejo) == 1, (etq, s.count(viejo), viejo[:80])
        open(p, "w", encoding="utf-8").write(s.replace(viejo, nuevo))
    print("propuestas aplicadas:", sorted({c[0] for c in CAMBIOS if not solo or c[0] in solo}), "en", PROP)


if __name__ == "__main__":
    preparar(sys.argv[2:] or None)
