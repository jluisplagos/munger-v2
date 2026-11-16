"""Lectura geométrica de una página con pdfminer (pdfplumber): palabras con su caja en puntos, agrupadas en filas y celdas.
Revisión n.º 6 (frente E · F1 · Elis). No usa pdftotext ni ninguna función del autor.

La columna de un número se decide por la posición real de las palabras en la página (puntos) y los títulos, por la
fuente tipográfica (tamaño y peso), no por las mayúsculas ni por la rejilla de caracteres del texto con maquetación. Es
una lectura independiente de la del verificador y de la del barrido de la revisión n.º 5, que trabajaban sobre
`pdftotext -layout`.

En las tablas de Elis la cabecera y las cifras de una columna se alinean por la derecha: la cabecera de un número es la
celda de cabecera cuyo borde derecho coincide con el suyo (tolerancia de 6 puntos). Las cabeceras de segundo nivel (una
entidad o una medida que abarca varias columnas) no coinciden por la derecha, pero solapan en horizontal.
"""
import re
import unicodedata
from functools import lru_cache

import pdfplumber

NUM = re.compile(r"^[+\-–−]?\(?[+\-–−]?\d[\d.,  ]*\)?%?\)?$")
UNIDAD = re.compile(r"\((?:[Ii]n|[Ee]n)\s+(?:millions?|thousands?|milliers|milliards|billions?|euros|%|number|nombre)\b")
FECHA_O_ANIO = re.compile(r"(?<![\d.,])(?:\d{1,2}/\d{1,2}/)?(20\d\d)(?![\d.,])")
APERTURA = re.compile(r"(?i)\b0?1/0?1/20\d\d|January 1,? 20\d\d|1er janvier 20\d\d")
PUBLICADA = re.compile(r"(?i)\b(?:published|reported|publi[ée]e?s?)\b")
REEXPRESADA = re.compile(r"(?i)\b(?:restated|retrait[ée]e?s?)\b")
# palabras que califican una fecha sin ser otra columna (llamadas, «restated», «Notes»…)
CALIFICA = re.compile(r"(?i)^(?:\(?\*+\)?|\(?[a-z0-9]\)|restated\*?|retrait[ée]e?s?\*?|adjusted\*?|ajust[ée]e?s?\*?|published|reported|publi[ée]e?s?\*?|"
                      r"notes?|\(unaudited\)|\(non|audité\)|as|at|au|le|-|–)$")


@lru_cache(maxsize=16)
def _abrir(ruta):
    return pdfplumber.open(ruta)


@lru_cache(maxsize=8192)
def palabras(ruta, n):
    """Palabras de la página n (1 = primera): x0, x1, top, bottom, texto, tamaño y fuente del primer carácter."""
    pg = _abrir(str(ruta)).pages[n - 1]
    ws = pg.extract_words(x_tolerance=1.5, y_tolerance=2, keep_blank_chars=False, use_text_flow=False, extra_attrs=["size", "fontname"])
    return tuple({"x0": float(w["x0"]), "x1": float(w["x1"]), "top": float(w["top"]), "bottom": float(w["bottom"]),
                  "t": unicodedata.normalize("NFKC", w["text"]).replace("’", "'").replace("‘", "'"), "size": round(float(w["size"]), 1), "font": w["fontname"].split("+")[-1]}
                 for w in ws)


def filas(ws, tol=3.2):
    """Filas: palabras cuyo centro vertical dista menos de tol puntos; cada fila ordenada de izquierda a derecha."""
    orden = sorted(ws, key=lambda w: ((w["top"] + w["bottom"]) / 2, w["x0"]))
    out = []
    for w in orden:
        c = (w["top"] + w["bottom"]) / 2
        if out and abs(out[-1]["c"] - c) <= tol:
            out[-1]["ws"].append(w)
            out[-1]["c"] = (out[-1]["c"] * (len(out[-1]["ws"]) - 1) + c) / len(out[-1]["ws"])
        else:
            out.append({"c": c, "ws": [w]})
    for f in out:
        f["ws"].sort(key=lambda w: w["x0"])
        f["txt"] = " ".join(w["t"] for w in f["ws"])
        fu = {}
        for w in f["ws"]:
            fu[(w["font"], w["size"])] = fu.get((w["font"], w["size"]), 0) + len(w["t"])
        f["font"], f["size"] = max(fu, key=fu.get)
        f["x0"] = f["ws"][0]["x0"]
    return out


def es_num(t):
    return bool(NUM.match(t)) and bool(re.search(r"\d", t))


def unir_numeros(ws, frances=False):
    """Tokens numéricos de una fila como (x0, x1, texto). En francés une los grupos de millares separados por un espacio
    («1 234,5»); en los dos idiomas une el «%» suelto y el signo suelto («+ 6,1%»)."""
    out, k = [], 0
    while k < len(ws):
        w = ws[k]
        if w["t"] in ("+", "-", "–", "−") and k + 1 < len(ws) and es_num(ws[k + 1]["t"]) and ws[k + 1]["x0"] - w["x1"] < 5:
            x0, x1, t = w["x0"], ws[k + 1]["x1"], w["t"] + " " + ws[k + 1]["t"]
            k += 1
        elif es_num(w["t"]):
            x0, x1, t = w["x0"], w["x1"], w["t"]
        else:
            k += 1
            continue
        while frances and k + 1 < len(ws) and re.fullmatch(r"[+\-–−]?\(?[+\-–−]?\d{1,3}", t.split(" ")[-1]) \
                and re.fullmatch(r"\d{3}(?:,\d+)?\)?%?", ws[k + 1]["t"]) and ws[k + 1]["x0"] - x1 < 4.5:
            k += 1
            x1, t = ws[k]["x1"], t + " " + ws[k]["t"]
        if k + 1 < len(ws) and ws[k + 1]["t"] in ("%", "%)") and ws[k + 1]["x0"] - x1 < 5:
            k += 1
            x1, t = ws[k]["x1"], t + " " + ws[k]["t"]
        out.append((x0, x1, t))
        k += 1
    return out


def celdas(f, hueco=4.6):
    """Celdas de una fila: palabras consecutivas separadas por menos de «hueco» puntos (un espacio normal a 7 puntos mide
    unos 2). Devuelve (x0, x1, texto, n_palabras)."""
    out = []
    for w in f["ws"]:
        if out and w["x0"] - out[-1][1] < hueco:
            out[-1] = (out[-1][0], w["x1"], out[-1][2] + " " + w["t"], out[-1][3] + 1)
        else:
            out.append((w["x0"], w["x1"], w["t"], 1))
    return out


def es_fila_de_datos(f):
    """Dos números o más con decimales, o porcentajes, que no son fechas ni años."""
    n = 0
    for w in f["ws"]:
        if es_num(w["t"]) and not re.fullmatch(r"\(?20\d\d\)?", w["t"]) and (re.search(r"\d[.,]\d", w["t"]) or "%" in w["t"]):
            n += 1
    return n >= 2


SOLO_FECHA = re.compile(r"(?i)^(?:(?:as at|au|at|le)\s+)?(?:\d{1,2}/\d{1,2}/20\d\d|20\d\d|(?:December|January) \d{1,2}, 20\d\d|(?:31 décembre|1er janvier) 20\d\d)"
                        r"(?:\s+(?:restated|retrait[ée]e?s?|adjusted|ajust[ée]e?s?|published|reported|publi[ée]e?s?|pro forma))?\s*(?:\(?\*+\)?|\([a-z0-9]\))?$")


def es_fila_de_fechas(f):
    """Fila de cabecera sin declaración de unidades: sin datos, y con alguna celda que es solo una fecha o un año (con su
    calificador). Caso: la tabla de sensibilidad de las pensiones, que solo lleva «12/31/2023» sobre su única columna."""
    if es_fila_de_datos(f):
        return False
    cs = celdas(f)
    return any(SOLO_FECHA.match(c[2]) for c in cs) and all(c[3] <= 5 for c in cs)


def zona_de_cabecera(fs, k, max_filas=140):
    """Filas de la cabecera de la tabla de la fila k: la fila de cabecera más próxima por encima (la declaración de
    unidades o una fila de fechas sin datos) y las filas sin datos pegadas encima de ella (hueco vertical de 13 puntos
    como máximo, seis filas como máximo). Devuelve (índices, índice de la fila de cabecera más próxima)."""
    j0 = None
    for j in range(k - 1, max(-1, k - max_filas), -1):
        f = fs[j]
        if UNIDAD.search(f["txt"]) or es_fila_de_fechas(f):
            j0 = j
            break
    if j0 is None:
        return [], None
    zona = [j0]
    j = j0
    while j - 1 >= 0 and len(zona) < 7 and fs[j]["ws"][0]["top"] - max(w["bottom"] for w in fs[j - 1]["ws"]) <= 13 and not es_fila_de_datos(fs[j - 1]):
        j -= 1
        zona.insert(0, j)
    return zona, j0


def cabecera_del_token(fs, k, x0, x1, tol=6.0):
    """Lectura de la cabecera de la columna del token [x0, x1] de la fila k. Devuelve un dict:
      alineadas   celdas de cabecera cuyo borde derecho dista menos de tol puntos del borde derecho del token;
      solapan     celdas de cabecera que solapan el token en horizontal sin estar alineadas por la derecha;
      unidades    texto de la fila de la declaración de unidades; zona: índices de las filas de cabecera."""
    zona, j0 = zona_de_cabecera(fs, k)
    al, so = [], []
    for j in zona:
        for (c0, c1, t, n) in celdas(fs[j]):
            if n > 7 or UNIDAD.search(t) and c0 < x0 - 40:        # prosa o la propia declaración de unidades, a la izquierda
                # la declaración puede llevar pegada una cabecera («(In millions of euros) France»): se trata aparte
                continue
            if abs(c1 - x1) <= tol:
                al.append(t)
            elif c0 <= x1 and c1 >= x0:
                so.append(t)
    return {"alineadas": al, "solapan": so, "unidades": fs[j0]["txt"] if j0 is not None else None, "zona": zona, "j0": j0}


def anios_de(celdas_txt):
    """(años de cierre, años de apertura) que nombran unas celdas de cabecera. Una fecha de apertura («01/01/2020») es el
    cierre del ejercicio anterior: se devuelve aparte."""
    cierre, apertura = set(), set()
    for t in celdas_txt:
        for m in APERTURA.finditer(t):
            apertura.add(int(re.search(r"20\d\d", m.group()).group()))
        resto = APERTURA.sub(" ", t)
        cierre |= {int(a) for a in FECHA_O_ANIO.findall(resto)}
    return cierre, apertura


def otras_palabras(celdas_txt):
    """Palabras de unas celdas de cabecera que no son fechas, años ni calificadores: otra medida, otra entidad, un país."""
    out = []
    for t in celdas_txt:
        for w in t.split():
            if FECHA_O_ANIO.fullmatch(w) or re.fullmatch(r"\d{1,2}/\d{1,2}/20\d\d|20\d\d[*)]*|\(?20\d\d\)?", w) or CALIFICA.match(w) or es_num(w):
                continue
            out.append(w)
    return out


def es_encabezado(f):
    """Encabezado de bloque por su tipografía: fuente seminegra o negra de 8,9 puntos o más, fuera de la cabecera y del pie
    de la página, y que no sea el número de capítulo del margen."""
    return (f["size"] >= 8.9 and re.search(r"-(?:Md|Bold|Demi)", f["font"]) is not None and 60 < f["c"] < 790
            and not re.fullmatch(r"\d{1,2}", f["txt"].strip()) and f["size"] < 16)
