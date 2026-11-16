"""Verificación de cada cifra citada contra los BYTES del PDF original (frente E · F1 · Elis).

Cada fila de datos/cifras_fuente.csv se comprueba en seis dimensiones. Cada una queda en OK, PENDIENTE (no se puede
acreditar automáticamente; el motivo queda escrito) o FALLO:

  literal    el PDF está en la ruta declarada y su SHA-256 es el de datos/fuentes.json (una fuente sin huella declarada
             es FALLO con motivo); la página PDF existe (1 = primera del archivo, no el folio impreso); hay una línea con
             la etiqueta y el token de la posición declarada es EXACTAMENTE el literal impreso, con su signo; el valor
             con signo coincide con «valor_publicado». Si la etiqueta aparece en varias líneas y no se fija
             «ocurrencia», todas deben dar el mismo literal. Prosa («texto»): el literal está en la página.
  ejercicio  la columna, el bloque o el saldo corresponden al ejercicio declarado («anio»), según «control_anio»:
               dos_columnas  la columna de ejercicio de la cabecera de la tabla bajo la que está el token: por orden si hay tantas
                             columnas reconocidas como números y cada número está alineado con la suya; si no, la más
                             próxima. Bajo una palabra de cabecera ajena, PENDIENTE, salvo que la columna de otro ejercicio
                             esté alineada con el token (FALLO);
               crecimiento   tabla de variación: el ejercicio es el más reciente de la cabecera;
               max_cabecera  tabla de movimiento con apertura y cierre en la cabecera: el ejercicio es el de cierre;
               movimientos   el bloque empieza en el saldo anterior más próximo («AS AT JANUARY 1, Y» → Y; «AS AT 12/31/Y» → Y+1);
               saldo         la fecha está en la propia línea («12/31/Y» → Y; «JANUARY 1, Y» → Y−1);
               titulo        tabla de un solo ejercicio: el año aislado en una línea por encima de la tabla;
               manual        sin comprobación automática: PENDIENTE con la justificación de «nota» (sin ella, FALLO).
             Prosa: el ejercicio declarado debe ser el de la edición (pie de página).
  columna    en las tablas de varias columnas que no son ejercicios (crecimiento, impuestos diferidos, movimientos de
             arrendamientos, intangibles e inmovilizado, matrices por segmentos), la cabecera de la columna del token debe
             ser la del concepto declarado.
  unidad     «mm EUR»: el literal no es un porcentaje y la declaración de unidades más próxima por encima de la línea
             dice millones de euros (otra unidad: FALLO; ninguna: PENDIENTE). «%»: el literal lleva «%». Cualquier otra
             unidad declarada es FALLO. Prosa: no aplica.
  perimetro  «consolidado IFRS, grupo Elis»: la cabecera de la página es de estados consolidados o de resultados del
             grupo (si no, PENDIENTE); en una matriz por segmentos solo vale la columna «Total»; una línea cuyo rótulo
             es un segmento, un país de una tabla por países (también con el prefijo «CGU»/«UGT»), una jurisdicción o el
             desglose de un país («of which Ireland», «Hors Union européenne») es FALLO; un título de bloque o de tabla
             que nombra un país o un segmento, una cabecera con países sin columna reconocida o una columna de un grupo
             de columnas por entidad (la cabecera repite los ejercicios por marca o por firma) dejan PENDIENTE. «segmento X»: X debe ser el rótulo de la línea o, en una matriz por segmentos, la
             columna del token, identificada por el orden horizontal de las ocho cabeceras (la columna «Total» es FALLO;
             si el orden no se puede acreditar, PENDIENTE). Otro perímetro: FALLO. Prosa: no aplica.
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
    "Reino Unido e Irlanda": ["UK & Ireland", "Royaume-Uni & Irlande", "United Kingdom & Ireland"],
    "Latinoamérica": ["Latin America", "Amérique latine"],
    "Europa del Sur": ["Southern Europe", "Europe du Sud"],
    "Otros segmentos": ["Other segments", "Autres segments"],
}
ROTULOS_SEGMENTO = {r: es for es, rs in SEGMENTOS.items() for r in rs + [es]}
# columnas de las matrices por segmentos de Elis, de izquierda a derecha, con la palabra de cabecera que las identifica
# (inglés | francés). La última es el total del grupo.
COLUMNAS_MATRIZ = [("Francia", r"France"), ("Europa central", r"Central|centrale"), ("Escandinavia y Europa del Este", r"Scandinavia|Scandinavie"),
                   ("Reino Unido e Irlanda", r"UK\b|Royaume"), ("Latinoamérica", r"Latin|Amérique"), ("Europa del Sur", r"Southern|du Sud"),
                   ("Otros segmentos", r"(?i:\bother\b|[ée]liminations|autres secteurs)"), ("Total", r"\bTotal\b")]
# Columnas de las tablas: frase de cabecera (inglés | francés) que identifica cada una. La columna de un token es la de la
# frase cuyo centro horizontal está más cerca del centro del token, dentro del bloque de cabecera de su tabla.
FRASES_COLUMNA = {
    "ejercicio": r"20\d\d",
    "variacion": r"\bChange\b|Variation|\bbp\b",
    "notas": r"\bNotes?\b",
    "organico": r"Organic|organique",
    "externo": r"External|externe",
    "divisa": r"exchange|Effet|Currency",
    "publicado": r"Reported|publiée|\bChange\b",
    "resultado": r"\(loss\)|Résultat\b",
    "combinaciones": r"combinations|regroupements|d'entreprises",
    "global": r"comprehensive|global",
    "otros_mov": r"Translation|conversion",
    "fecha": r"\d{1,2}/\d{1,2}/20\d\d|1er janvier 20\d\d|January 1, 20\d\d",
    "total": r"\bTotal\b",
    "pasivo_arr": r"liabilit|locatifs",
    "terrenos": r"Land|Terrains|buildings|constructions",
    "vehiculos": r"Vehicles|Véhicules",
    "equipos": r"equipment|matériels|Installations|Facilities",
    "relaciones": r"relationships|clientèle",
    "marcas": r"Trademarks|Marques|competition|concurrence",
    "otros": r"\bOther\b|\bAutres\b",
    "alquiler": r"Rental|items",
}
# familias de columnas por tipo de tabla, y columna esperada de cada concepto (prefijo del identificador)
FAMILIAS = {
    "crecimiento": ("ejercicio", "organico", "externo", "divisa", "publicado"),
    "diferidos": ("fecha", "combinaciones", "resultado", "global", "otros_mov"),
    "arrendamientos": ("terrenos", "vehiculos", "equipos", "total", "pasivo_arr"),
    "intangibles": ("marcas", "relaciones", "otros", "total"),
    "inmovilizado": ("terrenos", "vehiculos", "equipos", "alquiler", "total"),
}
COLUMNA_POR_CONCEPTO = [
    (r"^CREC_ORG_", "crecimiento", "organico"), (r"^CREC_EXT_", "crecimiento", "externo"),
    (r"^CREC_FX_", "crecimiento", "divisa"), (r"^CREC_PUB_", "crecimiento", "publicado"),
    (r"^TAXDIF_", "diferidos", "resultado"),
    (r"^LS_\w+_ROU_", "arrendamientos", "total"), (r"^LS_\w+_PAS_", "arrendamientos", "pasivo_arr"),
    (r"^INT_RC_", "intangibles", "relaciones"), (r"^INT_MARCA_", "intangibles", "marcas"),
    (r"^PPE_\w+_RM_", "inmovilizado", "alquiler"), (r"^PPE_\w+_TOT_", "inmovilizado", "total"),
]
# líneas que no son importes en millones de euros aunque su tabla lo sea (recuentos, importes por acción, márgenes)
NO_MONETARIA = re.compile(r"(?i)number of|nombre d|per share|par action|= ?\(?A|\bA ?/ ?C\b|headcount|effectifs? moyens?|employees|salariés|"
                          r"\bdays\b|\bjours\b|as a % of|en % d|basis points|\(in years\)|\(en années\)")
# declaraciones de otras unidades que cortan la búsqueda de la de millones de euros
UNIDAD_OTRA_RX = re.compile(r"(?i)\((?:in|en)\s+(?:euros|number|nombre|%|thousands? of shares|milliers d'actions|days|jours)")
# países donde Elis informa ventas o activos por país (inglés | francés): una tabla con tres o más filas de países es una
# tabla por países; sus filas no son del grupo (salvo el total)
PAISES = re.compile(r"^(?:France|Germany|Allemagne|United Kingdom|Royaume-Uni|Spain|Espagne|Brazil|Brésil|Netherlands|Pays-Bas|"
                    r"Denmark|Danemark|Sweden|Suède|Switzerland|Suisse|Mexico|Mexique|Republic of Ireland|Irlande|Ireland|Russia|Russie|"
                    r"Norway|Norvège|Italy|Italie|Portugal|Belgium|Belgique|Poland|Pologne|Chile|Chili|Colombia|Colombie|Finland|Finlande|"
                    r"République d'Irlande|Eire|Great Britain|Grande-Bretagne|Latvia|Lettonie|"
                    r"Austria|Autriche|Luxembourg|Czech|Tchèque|Other countries|Autres pays)\b")
# rótulos de sublíneas que dependen de la línea anterior (márgenes, desgloses)
SUBLINEA = re.compile(r"^(?:As a % of|En % d|of which|dont|›|o/w)", re.I)
# países y segmentos en un título por encima de una tabla, en cualquier caja («FRANCE – DETAILS»)
PAIS_O_SEGMENTO_TITULO = re.compile(r"\b(?:" + PAISES.pattern[4:].rstrip(")\\b") + "|" +
                                    "|".join(re.escape(r) for r in sorted(ROTULOS_SEGMENTO, key=len, reverse=True)) + r")\b", re.I)
# los mismos países como palabras de una cabecera de columnas (tabla con una columna por país)
PAIS_EN_CABECERA = re.compile(r"\b" + PAISES.pattern[1:])
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


SALDO_EN_ROTULO = re.compile(r"(?i)\b(?:balance|solde|as at|au)\b")


def anio_de_saldo_en_rotulo(lineas, i, idioma):
    """(Revisión n.º 7, S1) Ejercicio del saldo cuya fecha lleva el rótulo de la fila, aunque esté partido en varias líneas
    («Balance as at December» / «31, 2021 restated(a)»; «DECEMBER, 31 2022»; «Solde au 31 décembre» / «2023, retraité*»).
    None si el rótulo no es el de un saldo con fecha."""
    r = rotulo_multilinea(lineas, i, idioma)
    if not SALDO_EN_ROTULO.search(r):
        return None
    r = re.sub(r"(?i)\bdecember,\s*31\b,?", "December 31,", r)
    return anio_de_saldo(r)


def anio_de_bloque(lineas, i, limite=80):
    """Ejercicio del bloque de movimientos al que pertenece la línea i: el que sigue al saldo más próximo por encima."""
    for j in range(i - 1, max(-1, i - limite), -1):
        if MARCA_SALDO.search(lineas[j]):
            a = anio_de_saldo(lineas[j])
            if a is not None:
                return a + 1
    return None


def modo_admitido(idf):
    """Modo de control del ejercicio que admite cada concepto. Es una lista cerrada: la fila no puede declarar otro (salvo
    «manual», que nunca da OK). Así un modo declarado no puede saltarse el control de la columna o de la edición."""
    if idf == "VENTAS_LINO_PLANO_2025" or idf.startswith("VENTAS_SEG_"):
        return "titulo"
    if idf.startswith("CREC_"):
        return "crecimiento"
    if idf.startswith("TAXDIF_"):
        return "max_cabecera"
    if "_SALDO_" in idf or idf.startswith("INT_RC_VNC"):
        return "saldo"
    if idf.startswith(("LS_", "PPE_", "INT_")):
        return "movimientos"
    return "dos_columnas"


def spans_numericos(linea, idioma):
    """Posición (inicio, fin) en la línea de cada token numérico, en el mismo orden que tokens_numericos."""
    out, desde = [], 0
    for t in tokens_numericos(linea, idioma):
        k = linea.find(t, desde)
        if k < 0:
            return None
        out.append((k, k + len(t)))
        desde = k + len(t)
    return out


def es_linea_de_datos(linea, idioma):
    """Línea con dos o más números que no son años: una fila de datos, no de cabecera."""
    return len([t for t in tokens_numericos(linea, idioma) if not re.fullmatch(r"20\d\d", t)]) >= 2


def linea_cabecera_anios(lineas, i, limite=80):
    for j in range(i - 1, max(-1, i - limite), -1):
        if len(anios_linea(lineas[j])) >= 2 or (len(anios_linea(lineas[j])) == 1 and j > 0 and anios_linea(lineas[j - 1])):
            return j
    return None


def es_fragmento_de_cabecera(linea):
    """Fragmento de cabecera en columnas: muy sangrado o con huecos de varias posiciones; la prosa no lo es."""
    return bool(re.match(r"^\s{10,}\S", linea) or re.search(r"\S {3,}\S", linea))


def cabecera_de_otra_tabla(lineas, j, i, idioma):
    """Línea de la cabecera de ejercicios de la tabla de la fila i si esa tabla empieza después de la declaración de
    unidades de la línea j, sin declaración propia: la última línea con dos ejercicios o más (y ninguna otra cifra) que
    aparece tras filas de datos entre j e i. None si la tabla de la fila es la de la declaración."""
    vistos_datos, h = False, None
    for k in range(j + 1, i):
        l = lineas[k]
        if es_linea_de_datos(l, idioma):
            vistos_datos = True
        elif vistos_datos and len(anios_linea(l)) >= 2 and not tokens_numericos(re.sub(r"20\d\d", "", l), idioma):
            h = k
    return h


def zona_de_cabecera(lineas, i, idioma):
    """Líneas de la cabecera de la tabla de la línea i: el bloque contiguo, sin líneas de datos, que termina en la
    declaración de unidades más próxima por encima (o, si no la hay, en la cabecera de ejercicios), y las líneas sin
    datos entre esa declaración y la fila. (Revisión n.º 6, R1) Si entre la declaración y la fila empieza otra tabla
    (cabecera_de_otra_tabla), la cabecera es la de esa tabla: su línea de ejercicios, los fragmentos de cabecera que tiene
    encima y las líneas sin datos que hay entre ella y la fila. Antes se tomaba la de la tabla anterior, con su prosa."""
    _, j = unidad_declarada(lineas, i)
    if j is None:
        j = linea_cabecera_anios(lineas, i)
        # (revisión n.º 7, S4) la primera línea de un rótulo partido, de una sola celda, justo encima de la fila («Pre-tax
        # discount rate 2021» / «(approximation)  9.1% …») no es la cabecera de ejercicios: se busca por encima
        k0 = i
        while j is not None and j == k0 - 1 and len(trozos(lineas[j])) == 1:
            k0, j = j, linea_cabecera_anios(lineas, j)
        if j is None:
            return []
    h = cabecera_de_otra_tabla(lineas, j, i, idioma)
    base = j if h is None else h
    zona, k = [base], base
    while k - 1 > (-1 if h is None else j) and lineas[k - 1].strip() and len(zona) < 9 and not es_linea_de_datos(lineas[k - 1], idioma):
        k -= 1
        # (revisión n.º 7, S1) el título numerado de la tabla («6.1.5 Consolidated statement of changes in equity») y su
        # continuación sangrada («as at December 31, 2022») no son cabecera de columnas: su año no es una columna
        if es_encabezado_numerado(lineas[k].strip(), idioma):
            zona = [z for z in zona if not es_continuacion_de_encabezado(lineas, k, z)]
            break
        # solo fragmentos de cabecera en columnas (muy sangrados o con huecos de varias posiciones), no prosa
        if es_fragmento_de_cabecera(lineas[k]):
            zona.insert(0, k)
    zona += [m for m in range(base + 1, i) if lineas[m].strip() and not es_linea_de_datos(lineas[m], idioma)]
    return zona


def es_continuacion_de_encabezado(lineas, k, z):
    """(Revisión n.º 7, S1) ¿Es la línea z (una de las dos siguientes al encabezado numerado de la línea k) la continuación
    de su título? Una sola celda que empieza en la columna en la que empieza el texto del encabezado."""
    if not k < z <= k + 2 or not lineas[z].strip() or len(trozos(lineas[z])) != 1:
        return False
    if z == k + 2 and not es_continuacion_de_encabezado(lineas, k, k + 1):
        return False
    t = lineas[k].lstrip()
    m = ENCABEZADO_NUMERADO.match(t)
    col_texto = len(lineas[k]) - len(t) + (m.end() if m else 0)
    return abs((len(lineas[z]) - len(lineas[z].lstrip())) - col_texto) <= 2


def columnas_de_cabecera(lineas, zona, claves):
    """Columnas reconocidas en la cabecera, ordenadas de izquierda a derecha: (centro, clave, texto). Cada año o fecha
    distinto es una columna; cada otra clave cuenta una vez, en su aparición más a la izquierda."""
    vistas, fechas = {}, []
    for clave in claves:
        # de la línea más cercana a la fila hacia arriba: si dos cabeceras de ejercicio ocupan el mismo sitio, manda la más
        # próxima (la zona puede incluir la línea de unidades de una tabla anterior con su propia fecha)
        for k in sorted(zona, reverse=True):
            for m in re.finditer(FRASES_COLUMNA[clave], lineas[k]):
                c = (m.start() + m.end()) / 2
                if clave in ("ejercicio", "fecha"):
                    txt = m.group()
                    # (revisión n.º 5, Q2) una columna de apertura («01/01/2020», «January 1, 2020», «1er janvier 2020») es
                    # el cierre del ejercicio anterior: su ejercicio es 2019, no 2020
                    if clave == "ejercicio" and APERTURA_RX.search(lineas[k][max(0, m.start() - 14):m.start()]):
                        txt = str(int(txt) - 1)
                    # (revisión n.º 5, Q1 y Q2) dos apariciones del mismo año en posiciones distintas son columnas
                    # distintas: «12/31/2021 published» y «12/31/2021 restated», o «12/31/2020» y «01/01/2020». Solo se
                    # funden las que están una encima de otra, en el mismo sitio (a menos de 6 caracteres).
                    if not any(abs(c - c2) <= 6 for c2, _, _ in fechas):
                        fechas.append((c, clave, txt))
                elif clave not in vistas or c < vistas[clave][0]:
                    vistas[clave] = (c, clave, m.group())
    return sorted(fechas + list(vistas.values()))


def asignar_columna(sp, cols, idx, maxdist=14, orden_alineado=False):
    """Columna del token idx de la línea (sp: posiciones de sus números) entre las columnas reconocidas de la cabecera.
    Por orden («orden») si la cabecera tiene tantas columnas reconocidas como números la línea; con orden_alineado
    (columnas de ejercicio; revisión n.º 6, R1), además, si cada número está alineado con la columna que le toca, a maxdist
    caracteres o menos: una cuenta que coincide por accidente desplazaría todas las cifras. En las columnas de concepto
    (familias) no se exige: sus cabeceras son frases alineadas a la izquierda («Reported growth») y las cifras, a la
    derecha. Si no, la columna cuyo centro está más cerca del centro del token («alineación», dentro de maxdist).
    Devuelve (clave, texto, método, centro de la columna, distancia), o (None, None, motivo, None, distancia) si el token
    no está bajo ninguna columna reconocida."""
    centros = [(a + b) / 2 for a, b in sp]
    if len(cols) == len(sp) and (not orden_alineado or all(abs(c - k[0]) <= maxdist for c, k in zip(centros, cols))):
        c, clave, txt = cols[idx]
        return clave, txt, "orden", c, abs(centros[idx] - c)
    d, clave, txt, c = min((abs(c - centros[idx]), clave, txt, c) for c, clave, txt in cols)
    if d > maxdist:
        return None, None, "el token no está bajo ninguna columna reconocida", None, d
    return clave, txt, "alineación", c, d


def columna_de_token(lineas, i, pos, idioma, claves, maxdist=14, cabeceras_ajenas=False, orden_alineado=False):
    """Columna del token de la posición pos en la línea i (asignar_columna). Devuelve (clave, texto, método) o
    (None, None, motivo). Con cabeceras_ajenas, el método «ajena:D:palabra» dice que el token está más cerca de una palabra
    de la cabecera que no es de ninguna columna reconocida que de la columna asignada, que está a D caracteres."""
    sp = spans_numericos(lineas[i], idioma)
    if not sp or not -len(sp) <= pos < len(sp):
        return None, None, "sin token en la posición"
    zona = zona_de_cabecera(lineas, i, idioma)
    if not zona:
        return None, None, "no se localiza la cabecera de la tabla"
    cols = columnas_de_cabecera(lineas, zona, claves)
    if not cols:
        return None, None, "la cabecera no tiene columnas reconocibles"
    idx = pos % len(sp)
    clave, txt, metodo, _, d = asignar_columna(sp, cols, idx, maxdist, orden_alineado)
    # Por orden, cada número de la línea tiene su propia columna reconocida y está alineado con ella: una palabra ajena
    # más próxima es parte de la misma celda apilada («Income (loss) / before tax 2025», «Montant (HT)»), no otra columna.
    if clave is None or metodo == "orden":
        return clave, txt, metodo
    a, b = sp[idx]
    c_tok = (a + b) / 2
    # La columna reconocida más cercana no basta si el token está aún más cerca de otra palabra de la cabecera que no es
    # de ninguna columna reconocida (un país, una sociedad, un ajuste). Caso: tabla de flujos de adquisiciones con la
    # columna «12/31/2021» (total) seguida de «Belgium», «Brazil»…: la cifra de Bélgica quedaba asignada a 2021.
    # Solo para las columnas de ejercicio: en las de concepto (familias) la cabecera es una frase de varias palabras y
    # solo una casa con la clave, así que las demás no son columnas ajenas.
    ajena = palabra_de_cabecera_mas_cercana(lineas, zona, claves, c_tok) if cabeceras_ajenas else None
    if ajena is not None and ajena[0] < d:
        # (revisión n.º 5, Q3) no se devuelve None: quien llama decide, con la distancia a la columna reconocida
        # (revisión n.º 6, R3)
        return clave, txt, f"ajena:{d:g}:{ajena[1]}"
    return clave, txt, "alineación"


APERTURA_RX = re.compile(r"(?i)(?:\b0?1/0?1/|January 1,\s*|1er janvier\s*)$")
# (revisión n.º 6, R3) distancia máxima, en caracteres, entre el centro de un token y el de una columna de ejercicio para
# tenerlos por alineados cuando el token está además bajo una cabecera ajena: la mitad de una fecha «12/31/2025» sobre una
# cifra de un carácter alineada a la derecha (4,5) más un carácter de holgura de la maquetación de pdftotext. Con el valor
# de 3 que proponía el revisor, 131 cifras de una columna de otro ejercicio alineada (según su propia lectura por la
# posición de las palabras) quedaban PENDIENTE a 3,5 caracteres; las cifras del cierre bajo «Valeur comptable» del DEU
# 2024 p.323 están a 13,5
ALINEADA = 5.5
# palabras de cabecera que califican una columna reconocida (no son columnas propias)
CALIFICADOR = re.compile(r"(?i)^(?:\(?\*+\)?|\(\d+\)|\([a-z]\)|restated\*?|published|reported|retrait[ée]e?s?\*?|publi[ée]e?s?|réel|actual|"
                         r"pro|forma|\(unaudited\)|\(non|audité\)|adjusted\*?|ajust[ée]e?s?\*?)$")
# (revisión n.º 5, Q1) palabras de la cabecera que dicen si la columna es la publicada antes de la reexpresión o la reexpresada
EDICION_COLUMNA = re.compile(r"(?i)\b(published|reported|publi[ée]e?s?|restated|retrait[ée]e?s?)\b")


def palabra_de_cabecera_mas_cercana(lineas, zona, claves, c_tok):
    """(distancia, palabra) de la palabra de la cabecera más cercana al centro del token que no forma parte de ninguna
    columna reconocida ni la califica. Solo cuenta lo que está a la derecha del inicio de la primera columna reconocida:
    a la izquierda están los rótulos de fila y la declaración de unidades."""
    reconocidos, inicio = [], None
    for clave in claves:
        for k in zona:
            for m in re.finditer(FRASES_COLUMNA[clave], lineas[k]):
                reconocidos.append((k, m.start(), m.end()))
                inicio = m.start() if inicio is None else min(inicio, m.start())
    if inicio is None:
        return None
    # (revisión n.º 5, Q3) celdas: en su línea, el trozo de texto (separado por dos espacios o más) que contiene una columna
    # reconocida es la celda de esa columna; sus otras palabras («restated (a)», «Adjusted») la califican, no son ajenas
    celdas = []
    for kk, s0, e0 in reconocidos:
        for t in re.finditer(r"\S+(?: \S+)*", lineas[kk]):
            if t.start() <= s0 and e0 <= t.end():
                celdas.append((kk, t.start(), t.end()))
    mejor = None
    for k in zona:
        for m in re.finditer(r"\S+", lineas[k]):
            if m.start() < inicio - 2 or CALIFICADOR.match(m.group()):
                continue
            if any(k == kk and m.start() < e and s < m.end() for kk, s, e in reconocidos + celdas):
                continue
            dist = abs((m.start() + m.end()) / 2 - c_tok)
            if mejor is None or dist < mejor[0]:
                mejor = (dist, m.group())
    return mejor


def edicion_de_columna(lineas, i, pos, idioma, maxdist=14):
    """(Revisión n.º 5, Q1) «publicada» o «reexpresada» si la columna de ejercicio del token lleva en su cabecera, a menos
    de 10 caracteres de su centro, «published», «reported», «publié(e)» o «restated», «retraité(e)»; None si no lleva
    ninguna de esas marcas. La columna se asigna como en columna_de_token, con la misma regla de cabecera ajena: si el
    token está bajo una palabra de la cabecera que no es de ninguna columna reconocida (la columna de ajuste «IFRS 3» de una
    tabla de reexpresión), no está bajo la columna publicada ni bajo la reexpresada, y no se marca (revisión n.º 6, R8 b)."""
    claves = ("ejercicio", "variacion", "notas")
    clave, _, metodo = columna_de_token(lineas, i, pos, idioma, claves, maxdist, cabeceras_ajenas=True, orden_alineado=True)
    if clave != "ejercicio" or metodo.startswith("ajena:"):
        return None
    sp = spans_numericos(lineas[i], idioma)
    zona = zona_de_cabecera(lineas, i, idioma)
    _, _, _, centro, _ = asignar_columna(sp, columnas_de_cabecera(lineas, zona, claves), pos % len(sp), maxdist, orden_alineado=True)
    mejor = None
    for k in zona:
        for m in EDICION_COLUMNA.finditer(lineas[k]):
            d = abs((m.start() + m.end()) / 2 - centro)
            if d <= 10 and (mejor is None or d < mejor[0]):
                mejor = (d, m.group(1).lower())
    if mejor is None:
        return None
    return "reexpresada" if mejor[1].startswith(("restated", "retrait")) else "publicada"


def token_y_zona(lineas, i, pos, idioma):
    sp = spans_numericos(lineas[i], idioma)
    if not sp or not -len(sp) <= pos < len(sp):
        return None, []
    return sp[pos], zona_de_cabecera(lineas, i, idioma)


def anio_titulo(lineas, i, limite=25):
    """Año aislado en una línea por encima de la tabla (tablas de un solo ejercicio, como el desglose de ingresos)."""
    for j in range(i - 1, max(-1, i - limite), -1):
        m = re.fullmatch(r"\s*(20\d\d)\s*", lineas[j])
        if m:
            return int(m.group(1))
    return None


def comprobar_anio(lineas, i, fila, idioma="en"):
    modo = (fila.get("control_anio") or "dos_columnas").strip()
    if modo not in MODOS:
        return "FALLO", f"modo de control del ejercicio desconocido: {modo!r}"
    if modo == "manual":
        if not (fila.get("nota") or "").strip():
            return "FALLO", "control manual del ejercicio sin justificación en «nota»"
        return "PENDIENTE", "ejercicio sin comprobación automática; la justificación de «nota» requiere comprobación independiente"
    if modo != modo_admitido(fila["id"]):
        return "FALLO", f"el modo «{modo}» no es el que admite este concepto («{modo_admitido(fila['id'])}»)"
    try:
        anio = int(fila["anio"])
    except ValueError:
        return "FALLO", f"ejercicio no numérico: {fila['anio']!r}"
    pos = int(fila["pos"])
    if modo == "crecimiento" and "%" not in fila["literal"]:
        return "FALLO", "una tabla de crecimiento solo admite porcentajes"
    if modo == "dos_columnas":
        # (revisión n.º 7, S1) una fila que lleva en su rótulo la fecha de un saldo («Balance as at December / 31, 2021
        # restated(a)», «Solde au 31 décembre / 2023, retraité*») es de ese ejercicio, sea cual sea su columna
        a_rot = anio_de_saldo_en_rotulo(lineas, i, idioma)
        if a_rot is not None:
            return ("OK", f"saldo de {a_rot} (fecha en el rótulo de la fila)") if a_rot == anio else (
                "FALLO", f"la fila es el saldo de {a_rot} (fecha en su rótulo), no de {anio}")
        col, txt, metodo = columna_de_token(lineas, i, pos, idioma, ("ejercicio", "variacion", "notas"), cabeceras_ajenas=True,
                                            orden_alineado=True)
        if col is None:
            return "PENDIENTE", f"columna del ejercicio no acreditada: {metodo}"
        if metodo.startswith("ajena:"):
            _, dist, palabra = metodo.split(":", 2)
            # (revisión n.º 6, R3) el FALLO solo si la columna de otro ejercicio está alineada con el token (ALINEADA): si está
            # más lejos, el token está bajo su propia cabecera ajena («Valeur comptable» junto a columnas de vencimientos
            # futuros) y la columna reconocida más próxima es la vecina, no la suya
            if col == "ejercicio" and int(txt) != anio and float(dist) <= ALINEADA:
                return "FALLO", f"la columna reconocida más próxima, alineada con el token ({dist} caracteres), es de {txt}, no de {anio} (el token está además bajo «{palabra}»)"
            if col == "ejercicio" and int(txt) != anio:
                return "PENDIENTE", (f"columna del ejercicio no acreditada: el token está bajo la cabecera «{palabra}», que no es una columna "
                                     f"reconocida; la columna reconocida más próxima ({txt}) está a {dist} caracteres, no alineada con él")
            return "PENDIENTE", f"columna del ejercicio no acreditada: el token está bajo la cabecera «{palabra}», que no es una columna reconocida"
        if col != "ejercicio":
            return "FALLO", f"la columna es «{txt}», no un ejercicio"
        a = int(txt)
        return ("OK", f"columna de {a} ({metodo} con la cabecera)") if a == anio else ("FALLO", f"la columna es de {a}, no de {anio}")
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
        _, zona = token_y_zona(lineas, i, pos, idioma)
        if not any(re.search(r"\d{1,2}/\d{1,2}/20\d\d", lineas[k]) for k in zona):
            return "FALLO", "la cabecera no tiene fechas de apertura y cierre: no es una tabla de movimiento"
        return ("OK", f"cabecera {bloque}") if bloque[0] == anio else ("FALLO", f"el cierre de la tabla es {bloque[0]}, no {anio}")
    cab = cabecera(lineas, i)
    if not cab:
        return "FALLO", "no se localiza la cabecera de ejercicios"
    # modo «crecimiento»: tabla de variación del ejercicio más reciente de su cabecera
    return ("OK", f"cabecera {cab}") if cab[0] == anio else ("FALLO", f"la tabla es de {cab[0]}, no de {anio}")


def comprobar_columna(lineas, i, fila, pos, idioma):
    """Concepto de la columna en las tablas de varias columnas que no son ejercicios (crecimiento, impuestos diferidos,
    movimientos de arrendamientos, intangibles e inmovilizado, matrices por segmentos)."""
    modo = (fila.get("control_anio") or "").strip()
    if modo == "dos_columnas":
        return "NO_APLICA", "la columna es el ejercicio: se comprueba en «ejercicio»"
    if modo == "titulo":
        if (fila.get("perimetro") or "").startswith("segmento "):
            return "NO_APLICA", "la columna del segmento declarado se comprueba en «perimetro»"
        _, j = unidad_declarada(lineas, i)
        col = columna_de_matriz(lineas, j, lineas[i], pos, idioma) if j is not None else None
        if col is None:
            return "PENDIENTE", "no se puede acreditar la columna de la matriz"
        return ("OK", "columna «Total»") if col == "Total" else ("FALLO", f"la columna es del segmento {col}, no el total")
    regla = next(((fam, esp) for rx, fam, esp in COLUMNA_POR_CONCEPTO if re.search(rx, fila["id"])), None)
    if regla is None:
        return "PENDIENTE", "concepto sin columna esperada declarada en el verificador"
    fam, esperada = regla
    col, txt, metodo = columna_de_token(lineas, i, pos, idioma, FAMILIAS[fam])
    if col is None:
        return "PENDIENTE", f"columna no acreditada: {metodo}"
    if col != esperada:
        return "FALLO", f"la columna es «{txt}» ({col}), no la de {esperada}"
    return "OK", f"columna «{txt}» ({metodo})"


# ------------------------------------------------------------------ unidad, perímetro y edición
def rotulo(linea):
    t = trozos(linea)
    # (revisión n.º 7, S3) la pestaña del capítulo en el margen («6») no es el rótulo: si la línea empieza por un dígito
    # suelto y le sigue una celda de texto, el rótulo es esa celda («6 · CGU France · 1,418.1» → «CGU France»)
    if len(t) >= 2 and re.fullmatch(r"\d", t[0]) and re.search(r"[^\W\d_]", t[1]):
        return t[1]
    return t[0] if t else ""


def unidad_declarada(lineas, i, limite=70):
    """Unidad de la declaración más próxima por encima de la línea i, y su línea. Admite la declaración partida en dos
    líneas dentro del rótulo de la primera columna («… concerned (In» / «thousands of euros)»). Una declaración de otra
    unidad («(In euros)», «(In number…», «(In %)») también corta la búsqueda."""
    for j in range(i - 1, max(-1, i - limite), -1):
        textos = [lineas[j]]
        if j + 1 < i:
            textos.append(rotulo(lineas[j]) + " " + rotulo(lineas[j + 1]))
        for tx in textos:
            for rx, u in UNIDAD_RX:
                if rx.search(tx):
                    return u, j
            if UNIDAD_OTRA_RX.search(tx):
                return "otra unidad (" + UNIDAD_OTRA_RX.search(tx).group(0) + "…)", j
    return None, None


def otra_tabla_entre(lineas, j, i, idioma):
    """¿Empieza otra tabla entre la declaración de unidades (j) y la línea (i)? Una cabecera de ejercicios que aparece
    después de filas de datos, sin declaración propia, es de otra tabla (cabecera_de_otra_tabla)."""
    return cabecera_de_otra_tabla(lineas, j, i, idioma) is not None


def entero_de_recuento(lit, idioma):
    """Literal sin parte decimal y con seis cifras o más («23,355,764», «233 954 020»)."""
    decimal = r",\d" if idioma == "fr" else r"\.\d"
    return not re.search(decimal, lit) and len(re.sub(r"\D", "", lit)) >= 6


def comprobar_unidad(lineas, i, fila, idioma="en"):
    u = (fila.get("unidad") or "").strip()
    lit = fila["literal"]
    if u not in UNIDADES:
        return "FALLO", f"unidad no reconocida: {u!r}"
    if u == "%":
        return ("OK", "porcentaje impreso") if "%" in lit else ("FALLO", "unidad «%» para un literal sin «%»")
    if "%" in lit:
        return "FALLO", "unidad «mm EUR» para un literal en porcentaje"
    if "€" in lit:
        return "FALLO", "unidad «mm EUR» para un importe en euros"
    if NO_MONETARIA.search(rotulo(lineas[i])):
        return "FALLO", f"la línea «{rotulo(lineas[i])}» es un recuento, un importe por acción o un margen, no millones de euros"
    # (revisión n.º 4, P1) criterio de formato, que no depende del rótulo: un entero de seis cifras o más no es una cifra en
    # millones de euros con decimales; es un recuento (acciones, efectos de dilución) aunque su rótulo no lo diga
    if entero_de_recuento(lit, idioma):
        return "PENDIENTE", f"el literal «{lit}» es un entero de seis cifras o más: formato de recuento, no de millones de euros"
    dec, j = unidad_declarada(lineas, i)
    if dec is None:
        return "PENDIENTE", "la página no declara la unidad por encima de la línea"
    if dec != u:
        return "FALLO", f"la tabla declara {dec} (línea {j + 1}), no {u}"
    if otra_tabla_entre(lineas, j, i, idioma):
        return "PENDIENTE", f"la declaración de la línea {j + 1} es de otra tabla; esta no declara su unidad"
    return "OK", f"tabla en millones de euros (línea {j + 1})"


def matriz_segmentos(lineas, j_unidad, alto=6):
    """¿La cabecera de la tabla (la línea de unidades y las que tiene encima) nombra tres segmentos o más?"""
    if j_unidad is None:
        return False, ""
    zona = " ".join(lineas[max(0, j_unidad - alto): j_unidad + 1])
    return len(set(PALABRA_SEGMENTO.findall(zona))) >= 3, zona


def columna_de_matriz(lineas, j_unidad, linea, pos, idioma, alto=6):
    """Columna (nombre en español) del token en una matriz por segmentos, si la cabecera tiene las ocho columnas en el
    orden de Elis (comprobado por la posición horizontal de cada palabra de cabecera); None si no se puede acreditar."""
    zona = lineas[max(0, j_unidad - alto): j_unidad + 1]
    posiciones = []
    for _, patron in COLUMNAS_MATRIZ:
        rx = re.compile(patron)
        cols = [m.start() for l in zona for m in rx.finditer(l)]
        if not cols:
            return None
        posiciones.append(min(cols))
    if posiciones != sorted(posiciones) or len(set(posiciones)) != len(posiciones):
        return None
    # (revisión n.º 3, N9) la columna se asigna por la posición horizontal del token respecto a las ocho cabeceras, no
    # contando desde la derecha: una celda vacía desplazaría la cuenta. Con ocho números, la cuenta debe coincidir.
    centros = []
    for _, patron in COLUMNAS_MATRIZ:
        rx = re.compile(patron)
        ms = [m for l in zona for m in rx.finditer(l)]
        m0 = min(ms, key=lambda m: m.start())
        centros.append((m0.start() + m0.end()) / 2)
    sp = spans_numericos(linea, idioma)
    if not sp or not -len(sp) <= pos < len(sp):
        return None
    a_, b_ = sp[pos % len(sp)]
    c_tok = (a_ + b_) / 2
    d, k = min((abs(c - c_tok), k) for k, c in enumerate(centros))
    if d > 12:
        return None
    col = COLUMNAS_MATRIZ[k][0]
    desde_la_derecha = len(sp) - (pos % len(sp))
    if len(sp) in (len(COLUMNAS_MATRIZ), len(COLUMNAS_MATRIZ) + 1) and desde_la_derecha <= len(COLUMNAS_MATRIZ):
        if COLUMNAS_MATRIZ[len(COLUMNAS_MATRIZ) - desde_la_derecha][0] != col:
            return None
    return col


def sin_prefijo_uge(r):
    """Rótulo sin el prefijo de unidad generadora de efectivo («CGU Denmark» → «Denmark», «UGT Irlande» → «Irlande»)."""
    return re.sub(r"^(?:CGU|UGT)\s+", "", r.strip(), flags=re.I)


def tabla_por_paises(lineas, i, j, idioma):
    """País de la fila i si está en una tabla por países (tres o más filas de datos con rótulo de país); None si no.
    (Revisión n.º 6, R5) El rótulo se compara sin el prefijo «CGU»/«UGT»: la tabla del fondo de comercio por UGE es una
    tabla por países, y antes solo fallaba la fila «CGU France» (por ser Francia un segmento)."""
    if j is None:
        return None
    datos = [k for k in range(j + 1, min(len(lineas), i + 40)) if es_linea_de_datos(lineas[k], idioma)]
    if sum(1 for k in datos if PAISES.match(sin_prefijo_uge(rotulo(lineas[k])))) < 3:
        return None
    for r in [rotulo(lineas[i])] + rotulos_sin_rotulo(lineas, i, idioma):
        m = PAISES.match(sin_prefijo_uge(r))
        if m:
            return m.group(0)
    return None


# (revisión n.º 6, R1) filas de jurisdicciones fiscales o de regiones, y desgloses de un país («of which Ireland»,
# «dont Irlande», «European Union (excluding France)», «Hors Union européenne»): no son el grupo
JURISDICCION = re.compile(r"(?i)\b(?:European Union|Union européenne|Non-cooperative jurisdictions?|(?:Pays|juridictions?) non[- ]coopérati\w*|"
                          r"Rest of the world|Reste du monde)\b")
DESGLOSE_PAIS = re.compile(r"(?i)(?:^|[›(\s])(?:of which|o/w|dont|including|excluding|excl\.?|hors)\s+(?:the\s+|l'|la\s+|le\s+|les\s+)?"
                           + PAIS_O_SEGMENTO_TITULO.pattern)


def rotulo_multilinea(lineas, i, idioma, alto=4):
    """Rótulo de la fila i con las líneas de rótulo que tiene encima: sin cifras, de una sola celda, con la misma sangría
    y sin línea en blanco por medio («Non-cooperative» / «jurisdictions for tax» / «purposes (European Union» / «list)»)."""
    r = rotulo(lineas[i])
    if not r:
        return r
    sangria = len(lineas[i]) - len(lineas[i].lstrip())
    partes, k = [r], i - 1
    while k >= 0 and len(partes) <= alto:
        l = lineas[k]
        if not l.strip() or tokens_numericos(l, idioma) or len(trozos(l)) != 1 or len(l.strip()) > 45:
            break
        if abs((len(l) - len(l.lstrip())) - sangria) > 3:
            break
        partes.insert(0, l.strip())
        k -= 1
    return " ".join(partes)


def jurisdiccion_de_fila(lineas, i, idioma):
    """(Revisión n.º 6, R1) El rótulo completo de la fila si es una jurisdicción, una región o el desglose de un país o de
    un segmento («› of which Ireland», «dont Irlande», «Excluding the European Union»); None si no."""
    for r in [rotulo_multilinea(lineas, i, idioma)] + rotulos_sin_rotulo(lineas, i, idioma):
        if JURISDICCION.search(r) or DESGLOSE_PAIS.search(r):
            return r
    return None


def es_titulo(t):
    """Línea propia de título: corta, sin cifras, con tres letras o más y casi toda en mayúsculas («FRANCE – DETAILS»,
    «DÉTAIL POUR LE ROYAUME-UNI»). La prosa y las cabeceras de columna en minúsculas no lo son."""
    letras = [c for c in t if c.isalpha()]
    return (bool(t) and not re.search(r"\d", t) and len(t) <= 60 and len(letras) >= 3
            and sum(c.isupper() for c in letras) >= 0.8 * len(letras))


# (revisión n.º 6, R2) encabezado numerado de nota o de apartado: «NOTE 13 STATUTORY AUDITORS' FEES», «5.4 Share-based
# payments», «NOTE 2.4 …»; no las filas con cifras ni el número de capítulo del margen («6   On January 9…»)
ENCABEZADO_NUMERADO = re.compile(r"^(?:(?:NOTE|Note|NOTA|Nota)\s+\d+(?:\.\d+)*|\d+(?:\.\d+)+\.?)\s+(?=\S)")


def es_encabezado_numerado(t, idioma):
    m = ENCABEZADO_NUMERADO.match(t)
    if not m:
        return False
    resto = t[m.end():].strip()
    # (revisión n.º 7, S5) no es prosa: sin comillas tras la numeración («Note 5.2 “Expenses related…”») ni puntuación final
    if re.search(r"[“”\"«»]", resto) or re.search(r"[.;:,]$", resto):
        return False
    return len(t) <= 80 and not tokens_numericos(resto, idioma) and bool(re.search(r"[^\W\d_]{3}", resto))


def titulo_de_pais_encima_v2(lineas, i, j, lineas_previas=None, idioma="en"):
    """(Revisión n.º 5, Q4) Título del bloque de la fila, si nombra un país o un segmento. Primero, lo que queda en la línea
    de unidades de su tabla después de la declaración, si es una cabecera de columna («(In millions of euros) France»).
    Después, hacia arriba desde la fila hasta el principio de la página, la primera línea de título (es_titulo) o
    (revisión n.º 6, R2) el primer encabezado numerado de nota o de apartado; si la página no tiene ninguno por encima de la
    fila, el último de la página anterior. None si ese título no nombra ninguno."""
    if j is not None and j < i:
        resto = lineas[j]
        for rx, _ in UNIDAD_RX:
            resto = rx.sub("", resto)
        # solo si lo que queda es un único país o segmento: la tabla tiene una sola columna, la de ese país. Si quedan
        # varias cabeceras («Acquisition date Belgium Brazil…»), decide la regla de las columnas por país (pais_de_columna)
        resto = re.sub(r"[()]", "", resto).strip()
        if resto and not re.search(r"\d", resto) and PAIS_O_SEGMENTO_TITULO.fullmatch(resto):
            return resto
    for t in [lineas[k].strip() for k in range(i - 1, -1, -1)] + list(reversed([x.strip() for x in (lineas_previas or [])])):
        if es_titulo(t) or es_encabezado_numerado(t, idioma):
            return t if PAIS_O_SEGMENTO_TITULO.search(t) else None
    return None


def titulo_corto_de_tabla(lineas, i, j, idioma, alto=8):
    """(Revisión n.º 6, R4: criterio de C10, acotado) Título corto de la tabla de la fila i si nombra un país o un segmento
    («Mexico», «France», «Interest rate swap – Chile»). Desde la cabecera de la tabla (la línea de unidades j o, si la
    tabla empieza después, su línea de ejercicios) hacia arriba, hasta `alto` líneas no vacías: las líneas de cabecera en
    columnas (dos celdas o más) se saltan; una línea de datos, con cifras, de más de 40 caracteres o con puntuación de
    frase corta la búsqueda; la primera línea de una sola celda decide: es el título si nombra un país o un segmento con
    cuatro palabras más como mucho. Así no cuenta la prosa que menciona un país por encima de una tabla del grupo."""
    if j is None:
        return None
    h = cabecera_de_otra_tabla(lineas, j, i, idioma)
    vistas = 0
    for k in range((j if h is None else h) - 1, -1, -1):
        l = lineas[k]
        t = l.strip()
        if not t:
            continue
        vistas += 1
        if vistas > alto or es_linea_de_datos(l, idioma) or re.search(r"\d", t):
            return None
        if len(trozos(l)) >= 2:
            continue
        if len(t) > 40 or re.search(r"[,;.:!?]", t):
            return None
        m = PAIS_O_SEGMENTO_TITULO.search(t)
        if not m:
            return None
        otras = re.findall(r"[^\W\d_][\w'-]*", (t[:m.start()] + " " + t[m.end():]))
        return t if len(otras) <= 4 else None
    return None


def pais_de_columna(lineas, i, pos, idioma):
    """En una tabla con columnas por país (tres países o más en la cabecera), palabra de cabecera bajo la que está el token
    si no es la columna del ejercicio o del total: la columna de un país o de una sociedad, no del grupo. Devuelve
    («columna», cabecera) o, si la cabecera nombra tres países o más y no tiene ninguna columna reconocida (ni ejercicio
    ni total), («sin_columnas», países) (revisión n.º 6, R4); None si no."""
    sp = spans_numericos(lineas[i], idioma)
    if not sp or not -len(sp) <= pos < len(sp):
        return None
    zona = zona_de_cabecera(lineas, i, idioma)
    paises = sorted(set(PAIS_EN_CABECERA.findall(" ".join(lineas[k] for k in zona)))) if zona else []
    if len(paises) < 3:
        return None
    a, b = sp[pos % len(sp)]
    c_tok = (a + b) / 2
    claves = ("ejercicio", "variacion", "notas", "total")
    cols = columnas_de_cabecera(lineas, zona, claves)
    if not cols:
        return "sin_columnas", ", ".join(paises)
    d_rec = min(abs(c - c_tok) for c, _, _ in cols)
    ajena = palabra_de_cabecera_mas_cercana(lineas, zona, claves, c_tok)
    if ajena is None or ajena[0] >= d_rec:
        return None
    # (revisión n.º 5, Q7 f; revisión n.º 6, R8 c) la cabecera completa de la columna: las palabras sin cifras apiladas en el
    # mismo sitio, en el orden de la página, línea a línea («Great» / «Britain», «Germany &» / «Luxembourg»). La prosa de la
    # tabla anterior ya no entra: la zona de cabecera es la de la propia tabla
    # (revisión n.º 7, S7 e) solo las líneas de cabecera, de celdas cortas: no la prosa a dos columnas que precede a la tabla
    cab = [k for k in zona if all(len(c.split()) <= 4 for c in trozos(lineas[k]))]
    pal = [(k, m.start(), m.group()) for k in cab for m in re.finditer(r"\S+", lineas[k])
           if not re.search(r"\d", m.group()) and abs((m.start() + m.end()) / 2 - c_tok) <= ajena[0] + 5]
    return "columna", " ".join(w for _, _, w in sorted(pal)) or ajena[1]


def cabecera_de_paises(lineas, i, pos, idioma, alto=30):
    """(Revisión n.º 7, S4) Cabecera con una columna por país de una tabla sin declaración de unidades ni línea de
    ejercicios (hipótesis del WACC por UGE: «Country · France · Germany · Brazil…»): la primera línea, hacia arriba desde la
    fila, de tres celdas o más, cortas y sin cifras, que nombra tres países o más. Una declaración de unidades, un título o un
    encabezado numerado cortan la búsqueda: la cabecera es la de otra tabla. Devuelve (línea, países), o None si no la hay o
    si el token está bajo una celda «Total» o «Group» de esa línea."""
    sp = spans_numericos(lineas[i], idioma)
    if not sp or not -len(sp) <= pos < len(sp):
        return None
    a, b = sp[pos % len(sp)]
    c_tok = (a + b) / 2
    for k in range(i - 1, max(-1, i - alto), -1):
        l, t = lineas[k], lineas[k].strip()
        if not t:
            continue
        if any(rx.search(l) for rx, _ in UNIDAD_RX) or UNIDAD_OTRA_RX.search(l) or es_titulo(t) or es_encabezado_numerado(t, idioma):
            return None
        celdas = list(re.finditer(r"\S+(?: \S+)*", l))
        if len(celdas) >= 3 and all(len(c.group().split()) <= 3 and not re.search(r"\d", c.group()) for c in celdas):
            paises = sorted(set(PAIS_EN_CABECERA.findall(l)))
            if len(paises) >= 3:
                if any(re.search(r"(?i)\b(?:total|group|groupe)\b", c.group()) and c.start() - 3 <= c_tok <= c.end() + 3 for c in celdas):
                    return None
                return k, paises
    return None


def periodo_de_ejercicios(anios):
    """(Revisión n.º 6, R1) Menor periodo p ≥ 2 con el que los ejercicios de las columnas, de izquierda a derecha, repiten
    dos veces o más un mismo bloque de ejercicios distintos («2025 2024 2025 2024 2025 2024» → 2: un grupo de columnas por
    entidad o por medida, con una columna por ejercicio). None si no («2025 2025 2025 2024 2024 2024»: una columna por
    medida dentro de cada ejercicio; o ejercicios sin repetir)."""
    n = len(anios)
    for p in range(2, n // 2 + 1):
        if n % p == 0 and len(set(anios[:p])) == p and all(anios[k] == anios[k % p] for k in range(n)):
            return p
    return None


def grupo_de_columnas(lineas, i, pos, idioma, alto=4):
    """(Revisión n.º 6, R1) En una tabla cuya cabecera repite los mismos ejercicios una vez por grupo de columnas
    (periodo_de_ejercicios: «Elis · Le Jacquard Français · Kennedy Hygiene», cada una con «12/31/2025 · 12/31/2024»; las
    firmas auditoras con sus importes y porcentajes), el rótulo del grupo de la columna del token: en cada línea de la
    cabecera por encima de la línea de fechas (y en las `alto` líneas de cabecera en columnas que tiene encima), la celda
    más próxima al centro del grupo. None si la tabla no es de esa forma, si no se sabe la columna del token o si el grupo
    es el total o el grupo consolidado."""
    sp = spans_numericos(lineas[i], idioma)
    if not sp or not -len(sp) <= pos < len(sp):
        return None
    zona = zona_de_cabecera(lineas, i, idioma)
    cols = columnas_de_cabecera(lineas, zona, ("ejercicio",)) if zona else []
    p = periodo_de_ejercicios([txt for _, _, txt in cols])
    if p is None:
        return None
    clave, _, _, centro, _ = asignar_columna(sp, cols, pos % len(sp), orden_alineado=True)
    if clave is None:
        return None
    g = [c for c, _, _ in cols].index(centro) // p
    grupo = cols[g * p:(g + 1) * p]
    c_g = sum(c for c, _, _ in grupo) / p
    ini, fin = cols[0][0] - 6, cols[-1][0] + 6
    fechas = [k for k in zona if len(re.findall(FRASES_COLUMNA["ejercicio"], lineas[k])) >= 2]
    k_fechas = max(fechas) if fechas else min(zona)
    # la línea de fechas debe ser una cabecera, no prosa: además de las fechas, una declaración de unidades o pocas palabras
    resto = re.sub(r"\d{1,2}/\d{1,2}/20\d\d|20\d\d", " ", lineas[k_fechas])
    for rx, _ in UNIDAD_RX:
        resto = rx.sub(" ", resto)
    if len(re.findall(r"[^\W\d_]{2,}", resto)) > 4:
        return None
    encima = [k for k in zona if k < k_fechas]
    k, extra = min(zona) - 1, 0
    while k >= 0 and extra < alto:
        if lineas[k].strip():
            if es_linea_de_datos(lineas[k], idioma) or not es_fragmento_de_cabecera(lineas[k]):
                break
            encima.insert(0, k)
            extra += 1
        k -= 1
    rotulos = []
    for k in sorted(set(encima)):
        celdas = [(abs((m.start() + m.end()) / 2 - c_g), m.group()) for m in re.finditer(r"\S+(?: \S+)*", lineas[k])
                  if ini <= (m.start() + m.end()) / 2 <= fin and not re.search(r"\d", m.group())]
        if celdas:
            rotulos.append(min(celdas)[1])
    nombre = " / ".join(rotulos) or f"grupo {g + 1} de {len(cols) // p}"
    if re.search(r"(?i)\b(?:total|group|groupe|consolid)", nombre):
        return None
    return nombre


def normalizar_rotulo(r):
    """«United Kingdom and Ireland» → «united kingdom & ireland»; quita «CGU», «UGT» y espacios repetidos."""
    r = re.sub(r"^(?:CGU|UGT)\s+", "", r.strip(), flags=re.I)
    r = re.sub(r"\s+(?:and|et)\s+", " & ", r, flags=re.I)
    return re.sub(r"\s+", " ", r).strip().lower()


ROTULOS_SEGMENTO_NORM = {normalizar_rotulo(r): es for r, es in ROTULOS_SEGMENTO.items()}


def rotulo_completo(lineas, i, idioma):
    """Rótulo de la línea i, unido al de la línea anterior si el rótulo está partido en dos líneas: la anterior no tiene
    cifras y es corta, y la segunda parte empieza en minúscula («and Ireland») o la primera termina en «and», «et» o «&»."""
    r = rotulo(lineas[i])
    k = i - 1
    while k >= 0 and not lineas[k].strip():
        k -= 1
    if k >= 0 and not tokens_numericos(lineas[k], idioma):
        prev = lineas[k].strip()
        if len(prev) <= 40 and (r[:1].islower() or re.search(r"(?:\band|\bet|&)$", prev)):
            return prev + " " + r
    return r


def rotulos_sin_rotulo(lineas, i, idioma, alto=3):
    """(Revisión n.º 7, S2) Rótulos posibles de una línea de cifras que no tiene rótulo (su primera celda es un número): las
    líneas de rótulo contiguas de arriba y de abajo, de una sola celda y sin cifras, en todas sus combinaciones
    («Scandinavia and Eastern» / «599.2  580.7 …» / «Europe» → «Scandinavia and Eastern Europe»). Lista vacía si la línea
    tiene rótulo."""
    t = trozos(lineas[i])
    if not t or not es_numero(t[0].split(" ")[0], idioma):
        return []
    def contiguas(paso):
        out, k = [], i + paso
        while 0 <= k < len(lineas) and len(out) < alto:
            l = lineas[k]
            if not l.strip() or tokens_numericos(l, idioma) or len(trozos(l)) != 1:
                break
            out.append(l.strip())
            k += paso
        return out
    arriba, abajo = list(reversed(contiguas(-1))), contiguas(1)
    return [" ".join(arriba[len(arriba) - a:] + abajo[:b]) for a in range(len(arriba) + 1) for b in range(len(abajo) + 1) if a or b]


def segmento_de_rotulo(lineas, i, idioma):
    """(Revisión n.º 5, Q5) Segmento de la fila por su rótulo normalizado y, si está partido, unido. (Revisión n.º 7, S2) Si
    la línea de la cifra no tiene rótulo, el de las líneas de rótulo contiguas."""
    for r in (rotulo_completo(lineas, i, idioma), rotulo(lineas[i])) + tuple(rotulos_sin_rotulo(lineas, i, idioma)):
        es = ROTULOS_SEGMENTO_NORM.get(normalizar_rotulo(r))
        if es:
            return es
    return None


def segmento_de_sublinea(lineas, i, j, idioma):
    """En una tabla por segmentos (tres o más filas con rótulo de segmento), segmento del que depende la línea i: una
    sublínea («As a % of revenue», «of which»…) bajo un rótulo de segmento, o la fila «Other»/«Autres» de esa tabla."""
    if j is None:
        return None
    datos = [k for k in range(j + 1, min(len(lineas), i + 40)) if es_linea_de_datos(lineas[k], idioma)]
    if sum(1 for k in datos if segmento_de_rotulo(lineas, k, idioma)) < 3:
        return None
    r = rotulo(lineas[i])
    if r in ("Other", "Autres"):
        return "Otros"
    if not SUBLINEA.match(r):
        return None
    for k in sorted((k for k in datos if k < i), reverse=True):
        rk = rotulo(lineas[k])
        if SUBLINEA.match(rk):
            continue
        # (revisión n.º 6, R8 d) la fila de la que depende se atribuye con el mismo criterio con el que se cuentan las
        # filas de segmento: rótulo normalizado y, si está partido, unido
        return segmento_de_rotulo(lineas, k, idioma)
    return None


def comprobar_perimetro(lineas, i, fila, pos, idioma="en", lineas_previas=None):
    p = (fila.get("perimetro") or "").strip()
    seg_linea = segmento_de_rotulo(lineas, i, idioma)
    _, j = unidad_declarada(lineas, i)
    es_matriz, zona = matriz_segmentos(lineas, j)
    if p == PERIMETRO_GRUPO:
        if not any(GRUPO_RX.search(l) for l in [x for x in lineas if x.strip()][:8]):
            return "PENDIENTE", "la cabecera de la página no la identifica como estados consolidados ni como resultados del grupo"
        if seg_linea:
            return "FALLO", f"la línea es del segmento {seg_linea}, no del grupo"
        jur = jurisdiccion_de_fila(lineas, i, idioma)
        if jur:
            return "FALLO", f"la línea «{jur}» es de una jurisdicción, una región o el desglose de un país, no del grupo"
        seg_padre = segmento_de_sublinea(lineas, i, j, idioma)
        if seg_padre:
            return "FALLO", f"la línea depende del rótulo del segmento {seg_padre}, no del grupo"
        pais = tabla_por_paises(lineas, i, j, idioma)
        if pais:
            return "FALLO", f"la línea es de un país ({pais}) en una tabla por países, no del grupo"
        if es_matriz:
            col = columna_de_matriz(lineas, j, lineas[i], pos, idioma)
            if col == "Total" or (col is None and pos == -1 and lineas[j].split() and lineas[j].split()[-1] == "Total"):
                return "OK", "columna «Total» de una matriz por segmentos"
            return "FALLO", f"columna {'del segmento ' + col if col else 'de un segmento'} en una matriz por segmentos, no el total del grupo"
        tit = titulo_de_pais_encima_v2(lineas, i, j, lineas_previas, idioma) or titulo_corto_de_tabla(lineas, i, j, idioma)
        if tit:
            return "PENDIENTE", f"el título «{tit}» encima de la tabla nombra un país o un segmento: el perímetro del grupo no se puede acreditar"
        pc = pais_de_columna(lineas, i, pos, idioma)
        if pc and pc[0] == "columna":
            return "FALLO", f"la columna es la de «{pc[1]}» en una tabla con columnas por país, no la del grupo"
        if pc:
            return "PENDIENTE", (f"la cabecera nombra países ({pc[1]}) y no tiene ninguna columna reconocida (ejercicio o total): "
                                 "no se puede acreditar que la columna sea la del grupo")
        cp = cabecera_de_paises(lineas, i, pos, idioma)
        if cp:
            return "PENDIENTE", (f"la cabecera de la tabla (línea {cp[0] + 1}) tiene una columna por país ({', '.join(cp[1])}): "
                                 "no se puede acreditar que la columna sea la del grupo")
        ent = grupo_de_columnas(lineas, i, pos, idioma)
        if ent:
            return "PENDIENTE", (f"la cabecera repite los ejercicios una vez por grupo de columnas (entidad o medida) y la columna es la de "
                                 f"«{ent}»: el perímetro del grupo no se puede acreditar")
        return "OK", "página de estados consolidados o de resultados del grupo"
    if p.startswith("segmento "):
        es = ROTULOS_SEGMENTO.get(p[len("segmento "):].strip())
        if es is None:
            return "FALLO", f"segmento no reconocido: {p!r}"
        if seg_linea == es or segmento_de_sublinea(lineas, i, j, idioma) == es or (
                es == "Otros segmentos" and segmento_de_sublinea(lineas, i, j, idioma) == "Otros"):
            return "OK", f"línea del segmento {es}"
        if es_matriz:
            col = columna_de_matriz(lineas, j, lineas[i], pos, idioma)
            if col is None:
                if pos == -1 and lineas[j].split() and lineas[j].split()[-1] == "Total":
                    return "FALLO", f"declarado segmento {es}, pero la columna es el total del grupo"
                return "PENDIENTE", f"columna de una matriz por segmentos sin orden de cabecera acreditable (declarado {es})"
            if col == es:
                return "OK", f"columna del segmento {es} en una matriz por segmentos"
            return "FALLO", f"declarado segmento {es}, pero la columna es {'el total del grupo' if col == 'Total' else 'del segmento ' + col}"
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


DIMENSIONES = ("literal", "ejercicio", "columna", "unidad", "perimetro", "edicion")


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
    dims["ejercicio"] = combinar([comprobar_anio(lineas, x["i"], fila, idioma) for x in vistos])
    dims["columna"] = combinar([comprobar_columna(lineas, x["i"], fila, pos, idioma) for x in vistos])
    dims["unidad"] = combinar([comprobar_unidad(lineas, x["i"], fila, idioma) for x in vistos])
    previas = texto_pagina(pdf, pag - 1).splitlines() if pag > 1 else []
    dims["perimetro"] = combinar([comprobar_perimetro(lineas, x["i"], fila, pos, idioma, previas) for x in vistos])
    e, d, info = comprobar_edicion(texto, fila, fuente, ejercicios)
    # (revisión n.º 5, Q1) en una tabla de reexpresión, la columna «published» es la cifra de la edición anterior aunque
    # esté impresa en la publicación vigente: no puede declararse vigente
    if e == "OK" and (fila.get("control_anio") or "").strip() == "dos_columnas" and (fila.get("edicion") or "").strip() == "vigente":
        if any(edicion_de_columna(lineas, x["i"], pos, idioma) == "publicada" for x in vistos):
            e, d = "FALLO", "la columna es la publicada antes de la reexpresión («published», «reported» o «publié»): cifra de la edición anterior, no la vigente"
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
    dims["columna"] = {"estado": "NO_APLICA", "detalle": "prosa"}
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
    res = {"huellas": {"datos": sha256_file(a.datos), "fuentes": sha256_file(a.fuentes)}, "fuentes": {}, "cifras": [], "resumen": {}}
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
        r = {"id": fila["id"], "doc": slug, "pagina": int(fila["pagina"]), "anio": fila["anio"], "literal": fila["literal"],
             "valor_publicado": fila["valor_publicado"]}
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
