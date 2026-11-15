"""Verificación de cada cifra citada contra los BYTES del PDF original (frente E · F1 · Elis).

Cada fila de datos/cifras_fuente.csv se comprueba en cinco dimensiones. Cada una queda en OK, PENDIENTE (no se puede
acreditar automáticamente; el motivo queda escrito) o FALLO:

  literal    el PDF está en la ruta declarada y su SHA-256 es el de datos/fuentes.json (una fuente sin huella declarada
             es FALLO con motivo); la página PDF existe (1 = primera del archivo, no el folio impreso); hay una línea con
             la etiqueta y el token de la posición declarada es EXACTAMENTE el literal impreso, con su signo; el valor
             con signo coincide con «valor_publicado». Si la etiqueta aparece en varias líneas y no se fija
             «ocurrencia», todas deben dar el mismo literal. Prosa («texto»): el literal está en la página.
  ejercicio  la columna, el bloque o el saldo corresponden al ejercicio declarado («anio»), según «control_anio»:
               dos_columnas  cabecera más próxima con dos ejercicios, en orden descendente: pos −2 = el más reciente, pos −1 = el anterior;
               crecimiento   tabla de variación: el ejercicio es el más reciente de la cabecera;
               max_cabecera  tabla de movimiento con apertura y cierre en la cabecera: el ejercicio es el de cierre;
               movimientos   el bloque empieza en el saldo anterior más próximo («AS AT JANUARY 1, Y» → Y; «AS AT 12/31/Y» → Y+1);
               saldo         la fecha está en la propia línea («12/31/Y» → Y; «JANUARY 1, Y» → Y−1);
               titulo        tabla de un solo ejercicio: el año aislado en una línea por encima de la tabla;
               manual        sin comprobación automática: PENDIENTE con la justificación de «nota» (sin ella, FALLO).
             Prosa: el ejercicio declarado debe ser el de la edición (pie de página).
  unidad     «mm EUR»: el literal no es un porcentaje y la declaración de unidades más próxima por encima de la línea
             dice millones de euros (otra unidad: FALLO; ninguna: PENDIENTE). «%»: el literal lleva «%». Cualquier otra
             unidad declarada es FALLO. Prosa: no aplica.
  perimetro  «consolidado IFRS, grupo Elis»: la cabecera de la página es de estados consolidados o de resultados del
             grupo (si no, PENDIENTE); en una matriz por segmentos solo vale la columna «Total»; una línea cuyo rótulo
             es un segmento es FALLO. «segmento X»: X debe ser el rótulo de la línea. Otro perímetro: FALLO.
             Prosa: no aplica.
  edicion    el pie de página («Elis | Universal Registration Document AAAA» o «Elis | Document d'enregistrement
             universel AAAA») da el ejercicio de la publicación, que debe ser el declarado en datos/fuentes.json
             (sin pie: PENDIENTE). En tablas, «edicion» es «vigente» si la fuente es la que exige la regla de la Historia
             (la publicación más reciente que presenta el ejercicio: la del ejercicio siguiente si está entre las
             fuentes; en tablas de crecimiento y de movimiento de un solo ejercicio, la del propio ejercicio; en saldos,
             la del bloque de movimientos al que pertenecen), o «anterior» si es una publicación previa. Las filas
             «anterior» sirven para comparar ediciones; contraste_f1.py no las usa en sus cálculos.

Estado de la fila: FALLO si alguna dimensión falla; PENDIENTE si alguna queda pendiente; OK si todas lo están.
Código de salida: 1 con algún FALLO o alguna fuente sin verificar; 2 con pendientes y sin fallos; 0 si todo es OK.
No hay tolerancias: un redondeo, un signo cambiado, una columna de otro ejercicio o una página inexistente son FALLO.
Solo biblioteca estándar y los binarios pdftotext/pdfinfo (poppler). Uso:

  python3 -I verificar_cifras.py --raiz <ruta>/munger_v2_r1 --datos ../datos/cifras_fuente.csv \
      --fuentes ../datos/fuentes.json --salida ../resultados/verificacion_cifras.json \
      [--exportar-paginas ../evidencias/paginas]
"""
import argparse
import csv
import hashlib
import json
import re
import subprocess
import sys
import unicodedata
from fractions import Fraction
from pathlib import Path

NUM_EN = re.compile(r"^(?P<pre>[+\-–−]\s?)?(?P<par>\()?(?P<sig>[+\-–−])?(?P<num>\d{1,3}(?:,\d{3})*(?:\.\d+)?|\d+(?:\.\d+)?)(?P<cpar>\))?(?P<pct>\s?%)?(?P<cpar2>\))?$")
NUM_FR = re.compile(r"^(?P<pre>[+\-–−]\s?)?(?P<par>\()?(?P<sig>[+\-–−])?(?P<num>\d{1,3}(?: \d{3})*(?:,\d+)?|\d+(?:,\d+)?)(?P<cpar>\))?(?P<pct>\s?%)?(?P<cpar2>\))?$")
PLACEHOLDER = {"-", "–", "—", "−"}
MODOS = {"dos_columnas", "crecimiento", "max_cabecera", "movimientos", "saldo", "titulo", "manual"}
# tablas que solo presentan un ejercicio: la edición vigente es la del propio ejercicio
MODOS_UN_EJERCICIO = {"crecimiento", "max_cabecera"}
PERIMETRO_GRUPO = "consolidado IFRS, grupo Elis"
UNIDADES = {"mm EUR", "%"}
EDICIONES = {"vigente", "anterior"}
UNIDAD_RX = [
    (re.compile(r"(?:\bin|\ben)\s+millions?\s+(?:of\s+euros|d'euros)", re.I), "mm EUR"),
    (re.compile(r"(?:\bin|\ben)\s+(?:thousands?\s+of\s+euros|milliers\s+d'euros)", re.I), "miles EUR"),
    (re.compile(r"(?:\bin|\ben)\s+(?:billions?\s+of\s+euros|milliards\s+d'euros)", re.I), "miles de millones EUR"),
]
GRUPO_RX = re.compile(r"Consolidated financial statements|Group results|Comptes consolidés|Résultats du Groupe", re.I)
EDICION_RX = re.compile(r"Elis\s*\|\s*(?:Universal Registration Document|Document d'enregistrement universel)\s+(20\d\d)")
# segmentos de Elis: nombre en español → rótulos en los URD (inglés) y el DEU (francés)
SEGMENTOS = {
    "Francia": ["France"],
    "Europa central": ["Central Europe", "Europe centrale"],
    "Escandinavia y Europa del Este": ["Scandinavia & Eastern Europe", "Scandinavie & Europe de l'Est"],
    "Reino Unido e Irlanda": ["UK & Ireland", "Royaume-Uni & Irlande"],
    "Latinoamérica": ["Latin America", "Amérique latine"],
    "Europa del Sur": ["Southern Europe", "Europe du Sud"],
    "Otros segmentos": ["Other segments", "Autres segments"],
}
ROTULOS_SEGMENTO = {r: es for es, rs in SEGMENTOS.items() for r in rs + [es]}
PALABRA_SEGMENTO = re.compile(r"\b(France|Central|Scandinavia|Ireland|Latin|Southern|segments|centrale|Scandinavie|Irlande|latine|Sud)\b")

ANIO = re.compile(r"(?<![\d.,/])(20\d\d)(?![\d.,])")
FECHA_CIERRE = re.compile(r"(?:12/31/|31/12/)(20\d\d)")
# saldos: (patrón, desplazamiento del ejercicio respecto del año de la fecha)
SALDO_APERTURA = re.compile(r"(?:JANUARY 1,|January 1,|1ER JANVIER|1er JANVIER|1er janvier)\s*(20\d\d)")
SALDO_CIERRE = re.compile(r"(?:12/31/|31/12/|DECEMBER 31,\s*|December 31,\s*|31 DÉCEMBRE\s*|31 décembre\s*)(20\d\d)")
MARCA_SALDO = re.compile(r"(AS AT|As at|NET CARRYING AMOUNT|VALEUR NETTE COMPTABLE|^\s*AU\s)")


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def normalizar(s):
    s = unicodedata.normalize("NFKC", s)
    return s.replace("’", "'").replace("‘", "'")


_cache = {}


def texto_pagina(pdf, n, layout=True):
    clave = (str(pdf), n, layout)
    if clave not in _cache:
        args = ["pdftotext", "-q", "-f", str(n), "-l", str(n)] + (["-layout"] if layout else []) + [str(pdf), "-"]
        r = subprocess.run(args, capture_output=True, check=True)
        _cache[clave] = normalizar(r.stdout.decode("utf-8", errors="replace"))
    return _cache[clave]


def num_paginas(pdf):
    r = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, check=True, text=True)
    m = re.search(r"^Pages:\s+(\d+)", r.stdout, re.M)
    return int(m.group(1))


def trozos(linea):
    return [t.strip() for t in re.split(r"\s{2,}", linea.strip()) if t.strip()]


def es_numero(tok, idioma):
    rx = NUM_FR if idioma == "fr" else NUM_EN
    return tok in PLACEHOLDER or bool(rx.match(tok))


def tokens_numericos(linea, idioma):
    """Tokens numéricos de una línea en orden (los marcadores «-» cuentan como posición, sin valor)."""
    out = []
    for t in trozos(linea):
        if es_numero(t, idioma):
            out.append(t)
            continue
        partes = t.split(" ")
        cola = []
        while partes:
            cand = partes[-1]
            if idioma == "fr" and len(partes) >= 2 and re.fullmatch(r"\(?\d{1,3}", partes[-2]) and re.fullmatch(r"\d{3}(?:,\d+)?\)?%?", cand):
                unido = partes[-2] + " " + cand
                if es_numero(unido, idioma):
                    cola.insert(0, unido)
                    partes = partes[:-2]
                    continue
            if es_numero(cand, idioma) and cand not in PLACEHOLDER:
                cola.insert(0, cand)
                partes = partes[:-1]
            else:
                break
        out.extend(cola)
    return out


def valor(tok, idioma):
    """Fraction con signo del literal impreso; None para marcadores. Los porcentajes se devuelven en puntos (3.8 por «+3.8%»)."""
    if tok in PLACEHOLDER:
        return None
    rx = NUM_FR if idioma == "fr" else NUM_EN
    m = rx.match(tok)
    if not m:
        raise ValueError(f"no numérico: {tok!r}")
    num = m.group("num")
    num = num.replace(" ", "").replace(",", ".") if idioma == "fr" else num.replace(",", "")
    v = Fraction(num)
    neg = bool(m.group("par")) or (m.group("pre") or "").strip() in {"-", "–", "−"} or (m.group("sig") or "") in {"-", "–", "−"}
    return -v if neg else v


def lineas_con(texto, etiqueta):
    """Lista de (índice de línea, línea) que contienen la etiqueta (o casan con «re:…»)."""
    lineas = texto.splitlines()
    if etiqueta.startswith("re:"):
        rx = re.compile(etiqueta[3:])
        return [(i, l) for i, l in enumerate(lineas) if rx.search(l)]
    return [(i, l) for i, l in enumerate(lineas) if etiqueta in l]


# ------------------------------------------------------------------ ejercicio de la columna
def anios_linea(linea):
    a = FECHA_CIERRE.findall(linea) or ANIO.findall(linea)
    vistos = []
    for x in a:
        if x not in vistos:
            vistos.append(x)
    return [int(x) for x in vistos]


def cabecera(lineas, i, limite=80):
    """Ejercicios de la cabecera más próxima por encima de la línea i, en orden descendente (las tablas de Elis
    presentan el ejercicio corriente primero). Admite cabeceras partidas en dos líneas («2024» encima de «2025 restated*»)."""
    for j in range(i - 1, max(-1, i - limite), -1):
        a = anios_linea(lineas[j])
        if len(a) >= 2:
            return sorted(set(a), reverse=True)
        if len(a) == 1 and j > 0:
            b = set(a) | set(anios_linea(lineas[j - 1]))
            if len(b) >= 2:
                return sorted(b, reverse=True)
    return None


def anios_bloque_cabecera(lineas, i, limite=60, alto=12):
    """Ejercicios del bloque de cabecera de una tabla de movimientos: las líneas situadas encima de la línea de
    unidades («(In millions of euros)» / «(en millions d'euros)») más próxima por encima de i. Sirve para cabeceras
    con la fecha de apertura y la de cierre en líneas distintas."""
    for j in range(i - 1, max(-1, i - limite), -1):
        if re.search(r"\((?:In|in|en) millions", lineas[j]):
            a = set()
            for k in range(max(0, j - alto), j + 1):
                a |= set(anios_linea(lineas[k]))
            return sorted(a, reverse=True) or None
    return None


def anio_de_saldo(linea):
    m = SALDO_APERTURA.search(linea)
    if m:
        return int(m.group(1)) - 1
    m = SALDO_CIERRE.search(linea)
    if m:
        return int(m.group(1))
    return None


def anio_de_bloque(lineas, i, limite=80):
    """Ejercicio del bloque de movimientos al que pertenece la línea i: el que sigue al saldo más próximo por encima."""
    for j in range(i - 1, max(-1, i - limite), -1):
        if MARCA_SALDO.search(lineas[j]):
            a = anio_de_saldo(lineas[j])
            if a is not None:
                return a + 1
    return None


def anio_titulo(lineas, i, limite=25):
    """Año aislado en una línea por encima de la tabla (tablas de un solo ejercicio, como el desglose de ingresos)."""
    for j in range(i - 1, max(-1, i - limite), -1):
        m = re.fullmatch(r"\s*(20\d\d)\s*", lineas[j])
        if m:
            return int(m.group(1))
    return None


def comprobar_anio(lineas, i, fila):
    modo = (fila.get("control_anio") or "dos_columnas").strip()
    if modo not in MODOS:
        return "FALLO", f"modo de control del ejercicio desconocido: {modo!r}"
    if modo == "manual":
        if not (fila.get("nota") or "").strip():
            return "FALLO", "control manual del ejercicio sin justificación en «nota»"
        return "PENDIENTE", "ejercicio sin comprobación automática; la justificación de «nota» requiere comprobación independiente"
    try:
        anio = int(fila["anio"])
    except ValueError:
        return "FALLO", f"ejercicio no numérico: {fila['anio']!r}"
    pos = int(fila["pos"])
    if modo == "saldo":
        a = anio_de_saldo(lineas[i])
        return ("OK", f"saldo de {a}") if a == anio else ("FALLO", f"la línea es un saldo de {a}, no de {anio}")
    if modo == "movimientos":
        a = anio_de_bloque(lineas, i)
        return ("OK", f"bloque de {a}") if a == anio else ("FALLO", f"la línea está en el bloque de {a}, no de {anio}")
    if modo == "titulo":
        a = anio_titulo(lineas, i)
        if a is None:
            return "FALLO", "no hay un año aislado por encima de la tabla"
        return ("OK", f"tabla de {a}") if a == anio else ("FALLO", f"la tabla es de {a}, no de {anio}")
    if modo == "max_cabecera":
        bloque = anios_bloque_cabecera(lineas, i)
        if not bloque or len(bloque) < 2:
            return "FALLO", "no se localiza la cabecera de apertura y cierre"
        return ("OK", f"cabecera {bloque}") if bloque[0] == anio else ("FALLO", f"el cierre de la tabla es {bloque[0]}, no {anio}")
    cab = cabecera(lineas, i)
    if not cab:
        return "FALLO", "no se localiza la cabecera de ejercicios"
    if modo == "crecimiento":
        return ("OK", f"cabecera {cab}") if cab[0] == anio else ("FALLO", f"la tabla es de {cab[0]}, no de {anio}")
    if pos not in (-2, -1) or len(cab) < 2:
        return "FALLO", f"dos_columnas exige pos −2/−1 y dos ejercicios en la cabecera (pos {pos}, cabecera {cab})"
    esperado = cab[0] if pos == -2 else cab[1]
    return ("OK", f"columna de {esperado}") if esperado == anio else ("FALLO", f"la columna es de {esperado}, no de {anio}")


# ------------------------------------------------------------------ unidad, perímetro y edición
def rotulo(linea):
    t = trozos(linea)
    return t[0] if t else ""


def unidad_declarada(lineas, i, limite=70):
    """Unidad de la declaración más próxima por encima de la línea i, y su línea. Admite la declaración partida en dos
    líneas dentro del rótulo de la primera columna («… concerned (In» / «thousands of euros)»)."""
    for j in range(i - 1, max(-1, i - limite), -1):
        textos = [lineas[j]]
        if j + 1 < i:
            textos.append(rotulo(lineas[j]) + " " + rotulo(lineas[j + 1]))
        for tx in textos:
            for rx, u in UNIDAD_RX:
                if rx.search(tx):
                    return u, j
    return None, None


def comprobar_unidad(lineas, i, fila):
    u = (fila.get("unidad") or "").strip()
    lit = fila["literal"]
    if u not in UNIDADES:
        return "FALLO", f"unidad no reconocida: {u!r}"
    if u == "%":
        return ("OK", "porcentaje impreso") if "%" in lit else ("FALLO", "unidad «%» para un literal sin «%»")
    if "%" in lit:
        return "FALLO", "unidad «mm EUR» para un literal en porcentaje"
    dec, j = unidad_declarada(lineas, i)
    if dec is None:
        return "PENDIENTE", "la página no declara la unidad por encima de la línea"
    if dec != u:
        return "FALLO", f"la tabla declara {dec} (línea {j + 1}), no {u}"
    return "OK", f"tabla en millones de euros (línea {j + 1})"


def matriz_segmentos(lineas, j_unidad, alto=6):
    """¿La cabecera de la tabla (la línea de unidades y las que tiene encima) nombra tres segmentos o más?"""
    if j_unidad is None:
        return False, ""
    zona = " ".join(lineas[max(0, j_unidad - alto): j_unidad + 1])
    return len(set(PALABRA_SEGMENTO.findall(zona))) >= 3, zona


def comprobar_perimetro(lineas, i, fila, pos):
    p = (fila.get("perimetro") or "").strip()
    seg_linea = ROTULOS_SEGMENTO.get(rotulo(lineas[i]))
    _, j = unidad_declarada(lineas, i)
    es_matriz, zona = matriz_segmentos(lineas, j)
    if p == PERIMETRO_GRUPO:
        if not any(GRUPO_RX.search(l) for l in [x for x in lineas if x.strip()][:8]):
            return "PENDIENTE", "la cabecera de la página no la identifica como estados consolidados ni como resultados del grupo"
        if seg_linea:
            return "FALLO", f"la línea es del segmento {seg_linea}, no del grupo"
        if es_matriz:
            if pos == -1 and lineas[j].split() and lineas[j].split()[-1] == "Total":
                return "OK", "columna «Total» de una matriz por segmentos"
            return "FALLO", "columna de un segmento en una matriz por segmentos, no el total del grupo"
        return "OK", "página de estados consolidados o de resultados del grupo"
    if p.startswith("segmento "):
        es = ROTULOS_SEGMENTO.get(p[len("segmento "):].strip())
        if es is None:
            return "FALLO", f"segmento no reconocido: {p!r}"
        if seg_linea == es:
            return "OK", f"línea del segmento {es}"
        if es_matriz and any(r in zona for r in SEGMENTOS[es]):
            return "PENDIENTE", f"columna del segmento {es} en una matriz: no se acredita automáticamente"
        return "FALLO", f"el segmento declarado ({es}) no figura en la línea ni en la cabecera"
    return "FALLO", f"perímetro no reconocido: {p!r}"


def ejercicio_publicacion(texto):
    """Ejercicio de la publicación según el pie de página; None si no hay pie, −1 si hay pies de años distintos."""
    a = {int(x) for x in EDICION_RX.findall(texto)}
    return a.pop() if len(a) == 1 else (None if not a else -1)


def regla_edicion(ey, modo, ejercicios):
    """Ejercicio de la publicación que exige la regla de la Historia para el ejercicio ey."""
    if modo in MODOS_UN_EJERCICIO:
        return ey
    return ey + 1 if (ey + 1) in ejercicios else ey


def comprobar_edicion(texto, fila, fuente, ejercicios):
    e_decl = fuente.get("ejercicio")
    if not isinstance(e_decl, int):
        return "FALLO", "la fuente no declara su ejercicio en datos/fuentes.json", None
    e = ejercicio_publicacion(texto)
    if e is None:
        return "PENDIENTE", "la página no lleva pie con el nombre y el ejercicio de la publicación", None
    if e == -1:
        return "FALLO", "la página lleva pies de publicaciones de años distintos", None
    if e != e_decl:
        return "FALLO", f"el pie de página es de la publicación {e}, no de la {e_decl} declarada", None
    if fila["tipo"] == "texto":
        return "OK", f"publicación {e}", None
    rol = (fila.get("edicion") or "").strip()
    if rol not in EDICIONES:
        return "FALLO", f"edición no declarada o no reconocida: {rol!r}", None
    modo = (fila.get("control_anio") or "").strip()
    anio = int(fila["anio"])
    ey = max(anio, e - 1) if modo == "saldo" else anio
    regla = regla_edicion(ey, modo, ejercicios)
    info = {"publicacion": e, "ejercicio_de_edicion": ey, "publicacion_de_la_regla": regla, "rol": rol}
    if rol == "vigente":
        if e == regla:
            return "OK", f"edición vigente ({e}) para {ey}", info
        return "FALLO", f"declarada vigente, pero la regla exige la publicación {regla} para {ey} y esta es la {e}", info
    if e < regla:
        return "OK", f"edición anterior ({e}); la vigente para {ey} es la {regla}", info
    if e == regla:
        return "FALLO", f"declarada anterior, pero es la publicación {e} que exige la regla para {ey}", info
    return "FALLO", f"publicación {e} posterior a la que exige la regla ({regla}) para {ey}", info


def comprobar_anio_texto(texto, fila):
    e = ejercicio_publicacion(texto)
    if e is None or e == -1:
        return "PENDIENTE", "sin pie de página con el que comparar el ejercicio"
    try:
        anio = int(fila["anio"])
    except ValueError:
        return "FALLO", f"ejercicio no numérico: {fila['anio']!r}"
    return ("OK", f"publicación {e}") if anio == e else ("FALLO", f"el ejercicio declarado {anio} no es el de la publicación ({e})")


def decimales(tok, idioma):
    nucleo = re.sub(r"[^\d.,]", "", tok)
    sep = "," if idioma == "fr" else "."
    return len(nucleo.split(sep)[1]) if sep in nucleo else 0


ORDEN = {"OK": 0, "NO_APLICA": 0, "PENDIENTE": 1, "FALLO": 2, "NO_EVALUADO": 2}


def combinar(estados):
    """Peor estado de una lista de (estado, detalle), con los detalles de ese estado."""
    peor = max((e for e, _ in estados), key=lambda e: ORDEN[e])
    return {"estado": peor, "detalle": "; ".join(sorted({d for e, d in estados if e == peor}))}


DIMENSIONES = ("literal", "ejercicio", "unidad", "perimetro", "edicion")


def sin_evaluar(dims):
    for k in DIMENSIONES:
        dims.setdefault(k, {"estado": "NO_EVALUADO", "detalle": "falla el literal"})
    return dims


def comprobar_tabla(pdf, fila, idioma, fuente, ejercicios):
    pag = int(fila["pagina"])
    texto = texto_pagina(pdf, pag)
    lineas = texto.splitlines()
    cand = lineas_con(texto, fila["etiqueta"])
    if not cand:
        return {"dimensiones": sin_evaluar({"literal": {"estado": "FALLO", "detalle": "etiqueta no encontrada en la página"}})}
    occ = int(fila["ocurrencia"] or 0)
    if occ:
        if occ > len(cand):
            return {"dimensiones": sin_evaluar({"literal": {"estado": "FALLO", "detalle": f"solo hay {len(cand)} líneas con la etiqueta"}})}
        cand = [cand[occ - 1]]
    pos = int(fila["pos"])
    vistos = []
    for i, l in cand:
        toks = tokens_numericos(l, idioma)
        try:
            tok = toks[pos]
        except IndexError:
            vistos.append({"i": i, "linea": l.strip(), "token": None})
            continue
        vistos.append({"i": i, "linea": re.sub(r"\s{2,}", "  ", l.strip()), "token": tok})
    literales = {v["token"] for v in vistos}
    if len(literales) != 1 or None in literales:
        return {"dimensiones": sin_evaluar({"literal": {"estado": "FALLO", "detalle": "etiqueta ambigua o sin token en la posición"}}), "lineas": vistos}
    tok = literales.pop()
    if tok != fila["literal"]:
        return {"dimensiones": sin_evaluar({"literal": {"estado": "FALLO", "detalle": f"literal impreso {tok!r} ≠ declarado {fila['literal']!r}"}}), "lineas": vistos}
    v = valor(tok, idioma)
    if v != Fraction(fila["valor_publicado"]):
        return {"dimensiones": sin_evaluar({"literal": {"estado": "FALLO", "detalle": f"valor con signo {float(v)} ≠ valor_publicado {fila['valor_publicado']}"}}), "lineas": vistos}
    dims = {"literal": {"estado": "OK", "detalle": f"«{tok}» en la línea {vistos[0]['i'] + 1}"}}
    dims["ejercicio"] = combinar([comprobar_anio(lineas, x["i"], fila) for x in vistos])
    dims["unidad"] = combinar([comprobar_unidad(lineas, x["i"], fila) for x in vistos])
    dims["perimetro"] = combinar([comprobar_perimetro(lineas, x["i"], fila, pos) for x in vistos])
    e, d, info = comprobar_edicion(texto, fila, fuente, ejercicios)
    dims["edicion"] = {"estado": e, "detalle": d}
    if info:
        dims["edicion"]["regla"] = info
    return {"dimensiones": dims, "linea": vistos[0]["linea"], "token": tok, "decimales": decimales(tok, idioma)}


def comprobar_texto(pdf, fila, fuente=None, ejercicios=()):
    t_bruto = texto_pagina(pdf, int(fila["pagina"]), layout=False)
    texto = re.sub(r"\s+", " ", t_bruto)
    lit = re.sub(r"\s+", " ", normalizar(fila["literal"]))
    if lit not in texto:
        return {"dimensiones": sin_evaluar({"literal": {"estado": "FALLO", "detalle": "literal no encontrado en la página (modo texto)"}}),
                "estado": "FALLO"}
    dims = {"literal": {"estado": "OK", "detalle": "prosa encontrada en la página"}}
    if fuente is None:
        return {"dimensiones": dims, "estado": "OK"}
    t_layout = texto_pagina(pdf, int(fila["pagina"]))
    e, d = comprobar_anio_texto(t_layout, fila)
    dims["ejercicio"] = {"estado": e, "detalle": d}
    dims["unidad"] = {"estado": "NO_APLICA", "detalle": "prosa"}
    dims["perimetro"] = {"estado": "NO_APLICA", "detalle": "prosa"}
    e, d, _ = comprobar_edicion(t_layout, fila, fuente, ejercicios)
    dims["edicion"] = {"estado": e, "detalle": d}
    return {"dimensiones": dims}


def estado_fila(dims):
    peor = max((v["estado"] for v in dims.values()), key=lambda e: ORDEN[e])
    return "FALLO" if ORDEN[peor] == 2 else ("PENDIENTE" if peor == "PENDIENTE" else "OK")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--raiz", required=True, type=Path, help="carpeta munger_v2_r1 materializada (con binarios)")
    ap.add_argument("--datos", required=True, type=Path)
    ap.add_argument("--fuentes", required=True, type=Path)
    ap.add_argument("--salida", required=True, type=Path)
    ap.add_argument("--exportar-paginas", type=Path, help="escribe el texto de cada página citada, con cabecera de huella")
    a = ap.parse_args()
    fuentes = json.loads(a.fuentes.read_text(encoding="utf-8"))["fuentes"]
    ejercicios = {f["ejercicio"] for f in fuentes.values() if isinstance(f.get("ejercicio"), int)}
    res = {"fuentes": {}, "cifras": [], "resumen": {}}
    pdfs = {}
    for slug, f in fuentes.items():
        p = a.raiz / f.get("archivo", "")
        info = {"archivo": f.get("archivo"), "existe": p.is_file(), "ejercicio_declarado": f.get("ejercicio")}
        esperado = (f.get("sha256") or "").strip().lower()
        if not esperado:
            info["motivo"] = "la fuente no declara SHA-256: no se acepta"
        if p.is_file():
            info["sha256"] = sha256_file(p)
            info["sha256_coincide"] = bool(esperado) and info["sha256"] == esperado
            info["paginas"] = num_paginas(p)
            if info["sha256_coincide"]:
                pdfs[slug] = p
        res["fuentes"][slug] = info
    filas = list(csv.DictReader(a.datos.open(encoding="utf-8"), delimiter=";"))
    citadas = set()
    for fila in filas:
        slug = fila["doc"]
        r = {"id": fila["id"], "doc": slug, "pagina": int(fila["pagina"]), "anio": fila["anio"], "literal": fila["literal"]}
        if slug not in pdfs:
            motivo = res["fuentes"].get(slug, {}).get("motivo") or "fuente ausente o con huella distinta"
            r["dimensiones"] = sin_evaluar({"literal": {"estado": "FALLO", "detalle": motivo}})
        elif not (1 <= int(fila["pagina"]) <= res["fuentes"][slug]["paginas"]):
            r["dimensiones"] = sin_evaluar({"literal": {"estado": "FALLO", "detalle": "página inexistente en el PDF"}})
        else:
            idioma = fuentes[slug]["idioma"]
            if fila["tipo"] == "texto":
                r.update(comprobar_texto(pdfs[slug], fila, fuentes[slug], ejercicios))
            else:
                r.update(comprobar_tabla(pdfs[slug], fila, idioma, fuentes[slug], ejercicios))
            citadas.add((slug, int(fila["pagina"])))
        r["estado"] = estado_fila(r["dimensiones"])
        no_ok = [f"{k}: {v['detalle']}" for k, v in r["dimensiones"].items() if v["estado"] in ("FALLO", "PENDIENTE")]
        if no_ok:
            r["motivo"] = " | ".join(no_ok)
        res["cifras"].append(r)
    cuenta = {e: sum(1 for r in res["cifras"] if r["estado"] == e) for e in ("OK", "PENDIENTE", "FALLO")}
    por_dim = {k: {} for k in DIMENSIONES}
    for r in res["cifras"]:
        for k in DIMENSIONES:
            e = r["dimensiones"][k]["estado"]
            por_dim[k][e] = por_dim[k].get(e, 0) + 1
    res["resumen"] = {"filas": len(filas), "ok": cuenta["OK"], "pendientes": cuenta["PENDIENTE"], "fallos": cuenta["FALLO"],
                      "por_dimension": por_dim,
                      "fuentes_verificadas": sum(1 for v in res["fuentes"].values() if v.get("sha256_coincide")),
                      "fuentes_declaradas": len(fuentes)}
    if a.exportar_paginas:
        a.exportar_paginas.mkdir(parents=True, exist_ok=True)
        for slug, n in sorted(citadas):
            cab = (f"# Fuente: {fuentes[slug]['archivo']}\n# SHA-256: {res['fuentes'][slug]['sha256']}\n"
                   f"# Página PDF: {n} (texto extraído con pdftotext -layout; la evidencia primaria es el PDF)\n\n")
            (a.exportar_paginas / f"{slug}_p{n:03d}.txt").write_text(cab + texto_pagina(pdfs[slug], n), encoding="utf-8")
    a.salida.parent.mkdir(parents=True, exist_ok=True)
    a.salida.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(res["resumen"], ensure_ascii=False))
    for r in res["cifras"]:
        if r["estado"] != "OK":
            print(r["estado"], r["id"], r.get("motivo"), json.dumps(r.get("lineas", ""), ensure_ascii=False)[:300])
    if res["resumen"]["fallos"] or res["resumen"]["fuentes_verificadas"] != len(fuentes):
        return 1
    return 2 if res["resumen"]["pendientes"] else 0


if __name__ == "__main__":
    sys.exit(main())
