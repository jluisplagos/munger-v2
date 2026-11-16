"""Lectura geométrica propia de la revisión n.º 7 (frente E · F1 · Elis). No modifica nada del autor.

Motor: MuPDF (PyMuPDF), distinto de poppler/pdftotext (el del verificador) y de pdfminer y PDFium (los de la revisión
n.º 6). Lee cada página carácter a carácter (posición, cuerpo, negrita y color de cada glifo), forma palabras y filas por
la línea base y decide, para un número de una fila:

  - la PILA DE CABECERA de su columna: las palabras que no son datos y que están encima del número, en su misma banda
    horizontal, subiendo fila a fila hasta que se acaba la tabla. De ahí salen los ejercicios de la columna y las
    palabras que no son fechas ni calificadores (una marca, una sociedad, un país, una medida);
  - los TÍTULOS por tipografía que hay encima de la tabla (negrita o cuerpo mayor que el de la fila, en línea propia).

No usa la rejilla de caracteres de pdftotext, ni la declaración de unidades, ni las mayúsculas: es otra vía para lo mismo.
Es un filtro, no una verdad: cada clase que se lleva al informe se mira en la página y se pasa por el verificador oficial.
"""
import re
import unicodedata

NUM = re.compile(r"^[+\-–−]?\(?[+\-–−]?\d[\d.,  ]*\)?%?\)?$")
HUECO = {"-", "–", "—", "−", "n/a", "N/A", "na", "NA", "ns", "n.s.", "n.a.", "nm", "n.m."}
FECHA = re.compile(r"(?:\d{1,2}/\d{1,2}/)?(20\d\d)")
CALIF = re.compile(r"(?i)^(?:\(?\*+\)?|\(\d+\)|\([a-z]\)|restated\*?|retrait[ée]e?s?\*?|adjusted\*?|ajust[ée]e?s?\*?|net|nets?|nette?s?|"
                   r"at|as|au|aux|le|de|du|of|in|en|december|décembre|january|janvier|31|1er|1,|31,)$")


def normalizar(s):
    s = unicodedata.normalize("NFKC", s)
    return s.replace("’", "'").replace("‘", "'")


class Palabra:
    __slots__ = ("t", "x0", "x1", "y0", "y1", "base", "cuerpo", "negrita", "color")

    def __init__(self, t, x0, x1, y0, y1, base, cuerpo, negrita, color):
        self.t, self.x0, self.x1, self.y0, self.y1, self.base = t, x0, x1, y0, y1, base
        self.cuerpo, self.negrita, self.color = cuerpo, negrita, color

    def __repr__(self):
        return f"«{self.t}»[{self.x0:.0f}-{self.x1:.0f}]"


def palabras_de_pagina(page):
    """Palabras de la página a partir de los glifos (rawdict): se corta en los espacios y en los huecos entre glifos."""
    out = []
    d = page.get_text("rawdict")
    for b in d.get("blocks", []):
        for ln in b.get("lines", []):
            if abs(ln.get("dir", (1, 0))[1]) > 0.2:      # texto girado (márgenes): fuera
                continue
            for sp in ln.get("spans", []):
                negrita = bool(sp.get("flags", 0) & 16) or bool(re.search(r"(?i)bold|black|heavy|semibold|demi", sp.get("font", "")))
                act = None
                for ch in sp.get("chars", []):
                    c = ch["c"]
                    x0, y0, x1, y1 = ch["bbox"]
                    if c.isspace() or c == " ":
                        act = None
                        continue
                    if act is not None and x0 - act.x1 > 0.28 * sp["size"]:
                        act = None
                    if act is None:
                        act = Palabra(c, x0, x1, y0, y1, ch["origin"][1], sp["size"], negrita, sp.get("color", 0))
                        out.append(act)
                    else:
                        act.t += c
                        act.x1, act.y0, act.y1 = max(act.x1, x1), min(act.y0, y0), max(act.y1, y1)
    for w in out:
        w.t = normalizar(w.t)
    return out


def filas_de_pagina(palabras, tol=2.2):
    """Filas por línea base: palabras cuya línea base difiere en menos de tol puntos; ordenadas de arriba abajo."""
    filas = []
    for w in sorted(palabras, key=lambda w: (w.base, w.x0)):
        if filas and abs(filas[-1]["base"] - w.base) <= tol:
            filas[-1]["w"].append(w)
            filas[-1]["base"] = sum(x.base for x in filas[-1]["w"]) / len(filas[-1]["w"])
        else:
            filas.append({"base": w.base, "w": [w]})
    for f in filas:
        f["w"].sort(key=lambda w: w.x0)
        f["clave"] = "".join(w.t for w in f["w"])
        f["cuerpo"] = max(w.cuerpo for w in f["w"])
    return filas


def sin_espacios(s):
    return re.sub(r"\s+", "", s)


def casar_lineas(lineas, filas):
    """Empareja cada línea de pdftotext con una fila geométrica por su texto sin espacios, en orden de aparición (la k-ésima
    línea con un texto ↔ la k-ésima fila con ese texto). Devuelve {índice de línea: índice de fila}."""
    por_clave = {}
    for n, f in enumerate(filas):
        por_clave.setdefault(f["clave"], []).append(n)
    usados, mapa = {}, {}
    for i, l in enumerate(lineas):
        k = sin_espacios(l)
        if not k:
            continue
        cand = por_clave.get(k)
        if cand:
            j = usados.get(k, 0)
            if j < len(cand):
                mapa[i] = cand[j]
                usados[k] = j + 1
    return mapa


def caja_de_token(linea, a, b, fila):
    """Caja (x0, x1) del token que ocupa [a, b) en la línea de pdftotext, dentro de la fila geométrica emparejada."""
    antes = len(sin_espacios(linea[:a]))
    largo = len(sin_espacios(linea[a:b]))
    pos, cubren = 0, []
    for w in fila["w"]:
        ini, fin = pos, pos + len(w.t)
        if ini < antes + largo and antes < fin:
            cubren.append(w)
        pos = fin
    if not cubren:
        return None
    # si la palabra geométrica es más larga que el token (rótulo pegado), se reparte en proporción a los caracteres
    w0, w1 = cubren[0], cubren[-1]
    pos = 0
    for w in fila["w"]:
        if w is w0:
            break
        pos += len(w.t)
    x0 = w0.x0 + (w0.x1 - w0.x0) * (antes - pos) / max(1, len(w0.t))
    pos1 = 0
    for w in fila["w"]:
        if w is w1:
            break
        pos1 += len(w.t)
    x1 = w1.x0 + (w1.x1 - w1.x0) * (antes + largo - pos1) / max(1, len(w1.t))
    return x0, x1


def es_dato(w):
    return bool(NUM.match(w.t)) and not re.fullmatch(r"20\d\d", w.t) or w.t in HUECO


def celda(fila, w, hueco=None):
    """Texto de la celda de la fila a la que pertenece la palabra w: las palabras contiguas separadas por menos de un
    hueco (por defecto, 0,55 veces el cuerpo)."""
    ws = fila["w"]
    k = ws.index(w)
    h = hueco if hueco is not None else 0.55 * w.cuerpo
    a = k
    while a > 0 and ws[a].x0 - ws[a - 1].x1 <= h:
        a -= 1
    b = k
    while b + 1 < len(ws) and ws[b + 1].x0 - ws[b].x1 <= h:
        b += 1
    return ws[a:b + 1]


def pila_de_cabecera(filas, n, x0, x1, margen=3.0, salto=2.6, alto=9):
    """Pila de cabecera del número que ocupa [x0, x1] en la fila n: subiendo desde la fila, las palabras que solapan la
    banda [x0 − margen, x1 + margen] y que no son datos. Las celdas de datos de la banda se saltan mientras no se haya
    recogido cabecera; una vez recogida, un dato o un salto vertical grande terminan la pila. Devuelve la lista de celdas
    (de abajo arriba), cada una {texto, fila, x0, x1, negrita, cuerpo}, y la fila más alta de la pila."""
    pila, ultima, cima = [], filas[n]["base"], n
    cuerpo = filas[n]["cuerpo"]
    datos_saltados = 0
    for m in range(n - 1, -1, -1):
        f = filas[m]
        if ultima - f["base"] > salto * max(cuerpo, f["cuerpo"]) and pila:
            break
        en_banda = [w for w in f["w"] if w.x1 >= x0 - margen and w.x0 <= x1 + margen]
        if not en_banda:
            # fila sin nada en la banda: si ya hay cabecera y la fila es de datos, se acabó la tabla
            if pila and sum(1 for w in f["w"] if es_dato(w)) >= 2:
                break
            if not pila and ultima - f["base"] > 14 * cuerpo:
                break
            continue
        if all(es_dato(w) for w in en_banda):
            if pila:
                break
            datos_saltados += 1
            ultima = f["base"]
            continue
        # palabras de cabecera en la banda: se toma la celda entera de cada una
        vistos = []
        for w in en_banda:
            if es_dato(w):
                continue
            c = celda(f, w)
            if c[0] in [v[0] for v in vistos]:
                continue
            vistos.append(c)
        for c in vistos:
            pila.append({"texto": " ".join(w.t for w in c), "fila": m, "x0": c[0].x0, "x1": c[-1].x1,
                         "negrita": all(w.negrita for w in c), "cuerpo": max(w.cuerpo for w in c)})
        ultima, cima = f["base"], m
        if len({p["fila"] for p in pila}) >= alto:
            break
    return pila, cima


def ejercicios_de_pila(pila):
    """Ejercicios que nombran las celdas de la pila (apertura «01/01/AAAA», «January 1, AAAA» y «1er janvier AAAA» → AAAA − 1)."""
    out = []
    for p in pila:
        t = p["texto"]
        for m in re.finditer(r"(?:(\d{1,2})/(\d{1,2})/)?(20\d\d)", t):
            a = int(m.group(3))
            if (m.group(1) and int(m.group(1)) == 1 and int(m.group(2)) == 1) or re.search(r"(?i)(?:January 1,|1er janvier)\s*$", t[:m.start(3)]):
                a -= 1
            out.append(a)
    return out


def ajenas_de_pila(pila):
    """Palabras de la pila que no son fechas, ni calificadores, ni la declaración de unidades."""
    out = []
    for p in pila:
        t = re.sub(r"\((?:In|in|en|En) [^)]*\)", " ", p["texto"])
        t = re.sub(r"\d{1,2}/\d{1,2}/20\d\d|20\d\d", " ", t)
        ws = [w for w in t.split() if not CALIF.match(w) and re.search(r"[^\W\d_]{2,}", w)]
        if ws:
            out.append(" ".join(ws))
    return out


def titulos_encima(filas, cima, cuerpo_fila, x_izq, max_titulos=3, alto=40):
    """Títulos por tipografía por encima de la fila `cima` (la más alta de la pila de cabecera): filas en línea propia cuyas
    palabras van todas en negrita o con cuerpo mayor que el de la fila de datos (más de 0,6 puntos), sin dos o más datos.
    Devuelve hasta max_titulos, del más próximo al más lejano: (texto, cuerpo, negrita, fila)."""
    out = []
    for m in range(cima - 1, max(-1, cima - alto), -1):
        f = filas[m]
        ws = f["w"]
        if sum(1 for w in ws if es_dato(w)) >= 2:
            continue
        mayor = min(w.cuerpo for w in ws) > cuerpo_fila + 0.6
        negr = all(w.negrita for w in ws)
        if not (mayor or negr):
            continue
        txt = " ".join(w.t for w in ws)
        if len(txt) < 3:
            continue
        out.append((txt, round(max(w.cuerpo for w in ws), 1), negr, m))
        if len(out) >= max_titulos:
            break
    return out
