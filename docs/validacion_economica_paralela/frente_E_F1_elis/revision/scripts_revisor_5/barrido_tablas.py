"""Revisión n.º 5 (frente E · F1 · Elis). Barrido diferencial de las tablas de los cinco informes con el verificador de dos
versiones del autor. No modifica nada del autor.

Qué hace
  1. Comprueba que llamar a las funciones del verificador cargado como módulo da lo mismo que su ejecución oficial: para
     cada fila de tabla del CSV real, las seis dimensiones deben coincidir con resultados/verificacion_cifras.json.
  2. Recorre todas las páginas cuya cabecera el verificador acepta como del grupo (las demás nunca dan OK en perímetro).
     Por cada token numérico de cada línea con rótulo construye una fila candidata declarada como lo haría una cifra del
     grupo: «mm EUR» (o «%» si el literal lo lleva), «consolidado IFRS, grupo Elis», modo «dos_columnas», el ejercicio de
     la publicación (E) y el anterior (E−1), y la edición que la regla exige para cada uno.
  3. Evalúa cada candidata con el verificador de la versión nueva y con el de la anterior (ejercicio, columna, unidad,
     perímetro y edición; el literal es el impreso por construcción).
  4. Anota cada candidata con una lectura PROPIA de la tabla, que no usa las funciones de decisión del autor:
       - cabecera sobre el token por alineación del borde derecho (el autor usa la distancia entre centros);
       - declaración de unidades más próxima por encima, leída como cualquier paréntesis «(In …)» / «(en …)»;
       - título más próximo por encima de la tabla y rótulo de la fila, cotejados con una lista amplia de países.
  5. Escribe un resumen, las transiciones de estado entre versiones y las listas de candidatas a falso negativo (OK en la
     versión nueva con una señal propia en contra) y a falso positivo (OK en la anterior, no OK en la nueva, sin señal).

Las listas son candidatas: cada clase se comprueba después en el PDF (contraejemplos_5.py y el informe).

Uso: python3 -I barrido_tablas.py --raiz <munger_v2_r1> --nueva <frente C11> --anterior <frente C8> --salida <carpeta>
        [--todas <archivo.tsv.gz>] [--procesos 4]
"""
import argparse
import gzip
import json
import re
import sys
from collections import Counter, defaultdict
from multiprocessing import Pool
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from arnes import DIMS, GRUPO, Modulo, fila, leer_csv  # noqa: E402

DIM5 = ("ejercicio", "columna", "unidad", "perimetro", "edicion")
# lista amplia de países y gentilicios geográficos (inglés | francés), mayor que la del verificador
PAISES_AMPLIA = re.compile(
    r"(?i)\b(?:France|Germany|Allemagne|United Kingdom|Royaume-Uni|Great Britain|Grande-Bretagne|Britain|UK|Spain|Espagne|Andorra|Andorre|"
    r"Brazil|Brésil|Netherlands|Nether-|Pays-Bas|Denmark|Danemark|Sweden|Suède|Switzerland|Suisse|Mexico|Mexique|Ireland|Irlande|Russia|"
    r"Russie|Norway|Norvège|Italy|Italie|Portugal|Belgium|Belgique|Poland|Pologne|Chile|Chili|Colombia|Colombie|Finland|Finlande|Austria|"
    r"Autriche|Luxembourg|Czech|Tchèque|Slovakia|Slovaquie|Hungary|Hongrie|Estonia|Estonie|Latvia|Lettonie|Lithuania|Lituanie|Malaysia|"
    r"Malaisie|Singapore|Singapour|Peru|Pérou|Argentina|Argentine|Uruguay|Europe|Latin America|Amérique latine|Scandinavia|Scandinavie|"
    r"Other countries|Autres pays)\b")
OTRO_PERIMETRO = re.compile(r"(?i)\b(?:parent company|société mère|Elis SA\b|Elis S\.A\.|subsidiar(?:y|ies) (?:of|acquired)|acquired compan|"
                            r"sociétés acquises|joint venture|coentreprise|associates?\b|entreprises associées|discontinued|abandonnées|"
                            r"by country|par pays|by region|par région|by geographic|par zone|per segment|by segment|par secteur)\b")
UNIDAD_PROPIA = re.compile(r"\(\s*(?:[Ii]n|[Ee]n)\s+[^()]{2,60}\)")
MILLONES = re.compile(r"(?i)millions?\s+(?:of\s+euros|d['’]euros)")
ANIO_O_FECHA = re.compile(r"20\d\d")
_M = {}


def modulos(a):
    if not _M:
        _M["n"] = Modulo(a["nueva"], a["raiz"], "verificador_nuevo")
        _M["a"] = Modulo(a["anterior"], a["raiz"], "verificador_anterior")
    return _M["n"], _M["a"]


def es_dato(linea):
    """Línea con algún número con decimales que no es una fecha."""
    return bool(re.search(r"(?<![\d/])\d[\d  ,.]*[.,]\d(?![\d/])", linea))


def zona_propia(lineas, i):
    """Líneas de cabecera de la tabla de la línea i, por un criterio propio: la línea más próxima por encima que lleva una
    declaración de unidades entre paréntesis o dos fechas o años sin datos, las líneas sin datos pegadas encima (hasta
    seis) y las líneas sin datos que la siguen hasta la primera de datos."""
    j0 = None
    for j in range(i - 1, max(-1, i - 80), -1):
        l = lineas[j]
        if UNIDAD_PROPIA.search(l) or (len(ANIO_O_FECHA.findall(l)) >= 2 and not es_dato(re.sub(r"\d{1,2}/\d{1,2}/20\d\d", "", l))):
            j0 = j
            break
    if j0 is None:
        return None, []
    zona = [j0]
    k = j0
    while k - 1 >= 0 and lineas[k - 1].strip() and not es_dato(lineas[k - 1]) and j0 - (k - 1) <= 6:
        k -= 1
        zona.insert(0, k)
    k = j0 + 1
    while k < i and not es_dato(lineas[k]):
        if lineas[k].strip():
            zona.append(k)
        k += 1
    return j0, zona


def palabras_sobre(lineas, zona, b, margen=4):
    """Palabras de la zona de cabecera cuyo borde derecho está a «margen» caracteres o menos del borde derecho del token,
    de arriba abajo; y la palabra más próxima por el borde derecho, con su distancia."""
    cerca, mejor = [], None
    for k in zona:
        for m in re.finditer(r"\S+", lineas[k]):
            d = abs(m.end() - b)
            if d <= margen:
                cerca.append(m.group())
            if mejor is None or d < mejor[0]:
                mejor = (d, m.group())
    return cerca, mejor


def unidad_propia(lineas, i):
    """Texto del paréntesis «(In …)» / «(en …)» más próximo por encima de la línea, o «» si no lo hay en 70 líneas."""
    for j in range(i - 1, max(-1, i - 70), -1):
        m = UNIDAD_PROPIA.search(lineas[j])
        if m:
            return m.group(), j
    return "", None


def titulos_encima(lineas, j0, n=6):
    """Hasta n líneas no vacías y sin datos por encima de la cabecera de la tabla (títulos y subtítulos)."""
    out = []
    j = (j0 if j0 is not None else 0) - 1
    while j >= 0 and len(out) < n:
        t = lineas[j].strip()
        if t and not es_dato(t):
            out.append(re.sub(r"\s{2,}", "  ", t)[:90])
        elif es_dato(t):
            break
        j -= 1
    return out


def pagina(arg):
    a, doc, p = arg
    Mn, Ma = modulos(a)
    m = Mn.m
    idioma = Mn.fuentes[doc]["idioma"]
    E = Mn.fuentes[doc]["ejercicio"]
    texto = Mn.texto(doc, p)
    lineas = texto.splitlines()
    if not any(m.GRUPO_RX.search(l) for l in [x for x in lineas if x.strip()][:8]):
        return doc, p, None
    out = []
    for i, l in enumerate(lineas):
        toks = m.tokens_numericos(l, idioma)
        sp = m.spans_numericos(l, idioma)
        if not toks or sp is None:
            continue
        rot = m.rotulo(l)
        if not rot or m.es_numero(rot, idioma) or all(re.fullmatch(r"20\d\d", t) or t in m.PLACEHOLDER for t in toks):
            continue
        j0, zona = zona_propia(lineas, i)
        u_txt, _ = unidad_propia(lineas, i)
        tit = titulos_encima(lineas, zona[0] if zona else j0)
        for idx, tok in enumerate(toks):
            if tok in m.PLACEHOLDER or re.fullmatch(r"20\d\d", tok):
                continue
            try:
                val = m.valor(tok, idioma)
            except ValueError:
                continue
            cerca, mejor = palabras_sobre(lineas, zona, sp[idx][1]) if zona else ([], None)
            for anio in (E, E - 1):
                f = fila("B5", doc=doc, pagina=p, anio=anio, etiqueta="-", pos=idx - len(toks), literal=tok, valor_publicado=str(val),
                         unidad="%" if "%" in tok else "mm EUR",
                         edicion="vigente" if (anio == E - 1 or (E + 1) not in Mn.ejercicios) else "anterior")
                dn = Mn.dimensiones(doc, lineas, texto, i, f)
                da = Ma.dimensiones(doc, lineas, texto, i, f)
                out.append({"doc": doc, "p": p, "i": i + 1, "idx": idx, "n": len(toks), "tok": tok, "anio": anio, "rot": rot[:70],
                            "n_e": [dn[k][0] for k in DIM5], "a_e": [da[k][0] for k in DIM5],
                            "n_d": {k: dn[k][1] for k in ("ejercicio", "unidad", "perimetro")},
                            "a_d": {k: da[k][1] for k in ("ejercicio", "unidad", "perimetro")},
                            "sobre": cerca, "mejor": list(mejor) if mejor else None, "u": u_txt, "tit": tit[:3],
                            "linea": re.sub(r"\s{2,}", "  ", l.strip())[:150]})
    return doc, p, out


def equivalencia(carpeta, raiz, nombre):
    """Módulo frente a ejecución oficial, sobre las filas de tabla del CSV de esa versión."""
    M = Modulo(carpeta, raiz, nombre)
    of = {r["id"]: r for r in json.loads((Path(carpeta) / "resultados" / "verificacion_cifras.json").read_text(encoding="utf-8"))["cifras"]}
    n = dif = 0
    for f in leer_csv(carpeta):
        if f["tipo"] != "tabla":
            continue
        n += 1
        r = M.tabla(f)
        for k in DIMS:
            if (r["dimensiones"][k]["estado"], r["dimensiones"][k]["detalle"]) != (of[f["id"]]["dimensiones"][k]["estado"], of[f["id"]]["dimensiones"][k]["detalle"]):
                dif += 1
                break
    return n, dif


def plantilla(motivo):
    """Motivo sin sus partes variables, para agrupar."""
    t = re.sub(r"«[^»]*»", "«…»", motivo)
    t = re.sub(r"\(línea \d+\)|línea \d+", "línea N", t)
    t = re.sub(r"\b20\d\d\b", "AAAA", t)
    return re.sub(r"\([^)]*…\)", "(…)", t)[:110]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raiz", required=True)
    ap.add_argument("--nueva", required=True)
    ap.add_argument("--anterior", required=True)
    ap.add_argument("--salida", required=True, type=Path)
    ap.add_argument("--todas", type=Path, help="si se da, guarda todas las candidatas (TSV comprimido; grande)")
    ap.add_argument("--procesos", type=int, default=4)
    ap.add_argument("--nombres", default="C11,C8", help="nombres de las dos versiones para los textos")
    a = ap.parse_args()
    nom_n, nom_a = a.nombres.split(",")
    cfg = {"raiz": a.raiz, "nueva": a.nueva, "anterior": a.anterior}
    S = []
    w = S.append
    w(f"Barrido diferencial de tablas · versión nueva {nom_n} · versión anterior {nom_a}\n")
    for nom, carpeta in ((nom_n, a.nueva), (nom_a, a.anterior)):
        n, dif = equivalencia(carpeta, a.raiz, "equiv_" + nom)
        w(f"Equivalencia módulo = ejecución oficial en {nom}: {n} filas de tabla del CSV real, {dif} con alguna dimensión distinta")
    Mn, _ = modulos(cfg)
    tareas = [(cfg, doc, p) for doc in sorted(Mn.fuentes) for p in range(1, Mn.paginas(doc) + 1)]
    with Pool(a.procesos) as pool:
        res = pool.map(pagina, tareas, chunksize=8)
    cand = []
    pags = defaultdict(list)
    for doc, p, out in res:
        if out is None:
            continue
        pags[doc].append(p)
        cand.extend(out)
    w("\nPáginas con cabecera aceptada como del grupo (las únicas que pueden dar OK en perímetro):")
    for doc in sorted(pags):
        w(f"  {doc}: {len(pags[doc])} páginas")
    w(f"Candidatas evaluadas (token × ejercicio): {len(cand)}")
    if a.todas:
        with gzip.open(a.todas, "wt", encoding="utf-8") as g:
            for c in cand:
                g.write(json.dumps(c, ensure_ascii=False) + "\n")

    ok5 = lambda e: all(x in ("OK", "NO_APLICA") for x in e)  # noqa: E731
    w(f"\nOK en las cinco dimensiones: {nom_a} {sum(ok5(c['a_e']) for c in cand)} · {nom_n} {sum(ok5(c['n_e']) for c in cand)}")

    # ---------------------------------------------------------------- transiciones
    w(f"\n== Transiciones de estado {nom_a} → {nom_n}, por dimensión ==")
    trans = Counter()
    grupos = defaultdict(list)
    for c in cand:
        for k, ea, en in zip(DIM5, c["a_e"], c["n_e"]):
            if ea != en:
                trans[(k, ea, en)] += 1
                grupos[(k, ea, en, plantilla(c["n_d"].get(k, "")))].append(c)
    for (k, ea, en), n in sorted(trans.items()):
        w(f"  {k}: {ea} → {en}: {n}")
    if not trans:
        w("  ninguna")
    w("\n== Las mismas transiciones, por motivo de la versión nueva (páginas y un ejemplo) ==")
    for (k, ea, en, pl), cs in sorted(grupos.items(), key=lambda x: (-len(x[1]), x[0])):
        pp = Counter(f"{c['doc']} p.{c['p']}" for c in cs)
        w(f"\n  {k}: {ea} → {en} · {len(cs)} · {pl}")
        w("     páginas: " + ", ".join(f"{q} ({n})" for q, n in pp.most_common(14)) + (" …" if len(pp) > 14 else ""))
        c = cs[0]
        w(f"     ejemplo: {c['doc']} p.{c['p']} l.{c['i']} token {c['idx'] + 1}/{c['n']} «{c['tok']}» declarado {c['anio']} · {c['linea'][:100]}")

    # ---------------------------------------------------------------- candidatas a falso positivo
    def con_anio(c):
        return any(str(c["anio"]) in x for x in c["sobre"])

    w(f"\n\n== Candidatas a FALSO POSITIVO: OK en {nom_a}, no OK en {nom_n}, y el token está bajo una cabecera del ejercicio declarado ==")
    fp = [c for c in cand if ok5(c["a_e"]) and not ok5(c["n_e"]) and con_anio(c)]
    w(f"  total: {len(fp)}")
    por = defaultdict(list)
    for c in fp:
        k = next(k for k, e in zip(DIM5, c["n_e"]) if e not in ("OK", "NO_APLICA"))
        por[(k, plantilla(c["n_d"].get(k, "")))].append(c)
    for (k, pl), cs in sorted(por.items(), key=lambda x: -len(x[1])):
        w(f"\n  {k} · {len(cs)} · {pl}")
        for c in cs[:40]:
            w(f"     {c['doc']} p.{c['p']} l.{c['i']} tok {c['idx'] + 1}/{c['n']} «{c['tok']}» {c['anio']} · sobre: {' | '.join(c['sobre'])} · {c['n_d'].get(k, '')[:90]} · {c['linea'][:80]}")

    # ---------------------------------------------------------------- candidatas a falso negativo
    okn = [c for c in cand if ok5(c["n_e"])]
    w(f"\n\n== Candidatas a FALSO NEGATIVO entre las {len(okn)} que quedan OK en las cinco dimensiones en {nom_n} ==")

    def lista(titulo, cs, extra=lambda c: "", tope=40):
        pp = Counter(f"{c['doc']} p.{c['p']}" for c in cs)
        w(f"\n-- {titulo}: {len(cs)} en {len(pp)} páginas")
        w("   páginas: " + ", ".join(f"{q} ({n})" for q, n in sorted(pp.items())))
        for c in cs[:tope]:
            w(f"     {c['doc']} p.{c['p']} l.{c['i']} tok {c['idx'] + 1}/{c['n']} «{c['tok']}» {c['anio']} · {extra(c)} · {c['linea'][:90]}")
        if len(cs) > tope:
            w(f"     … y {len(cs) - tope} más (lista completa con --todas)")

    # (a) columna: ninguna cabecera alineada por la derecha lleva el ejercicio declarado
    a1 = [c for c in okn if not con_anio(c)]
    lista("(a) ninguna palabra de cabecera alineada por la derecha con el token lleva el ejercicio declarado", a1,
          lambda c: f"sobre: {' | '.join(c['sobre']) or '—'}; más próxima: {c['mejor']}; {c['n_d']['ejercicio'][:45]}")
    # (b) columna: sobre el token hay una palabra que no es fecha ni año
    califica = re.compile(r"(?i)^(?:\(?\*+\)?|\([a-z0-9]\)|restated[*()a-z]*|retrait[ée]e?s?[*()a-z0-9]*|notes?|\d+|\(?\d+\)?)$")
    b1 = [c for c in okn if con_anio(c) and any(not ANIO_O_FECHA.search(x) and not califica.match(x) for x in c["sobre"])]
    lista("(b) el ejercicio está sobre el token, pero también otra palabra que no es fecha, año, «restated» ni llamada", b1,
          lambda c: f"sobre: {' | '.join(c['sobre'])}")
    # (c) unidad: la declaración más próxima, leída por mí, no dice millones de euros
    c1 = [c for c in okn if "%" not in c["tok"] and not MILLONES.search(c["u"])]
    lista("(c) unidad OK, pero el paréntesis de unidades más próximo por encima no dice millones de euros", c1, lambda c: f"unidad leída: «{c['u']}»")
    # (d) unidad: literal entero (sin decimales), declarado en millones de euros
    def sin_decimales(c):
        return not re.search(r",\d" if Mn.fuentes[c["doc"]]["idioma"] == "fr" else r"\.\d", c["tok"])

    d1 = [c for c in okn if "%" not in c["tok"] and sin_decimales(c)]
    lista("(d) unidad OK con un literal entero, sin decimales", d1, lambda c: f"rótulo: {c['rot'][:40]}")
    # (e) perímetro: un título por encima o el rótulo nombra un país, una región u otro perímetro
    e1 = [c for c in okn if any(PAISES_AMPLIA.search(t) or OTRO_PERIMETRO.search(t) for t in c["tit"][:2])]
    lista("(e) perímetro OK, pero uno de los dos títulos más próximos por encima nombra un país, una región u otro perímetro", e1,
          lambda c: f"títulos: {' ‖ '.join(c['tit'][:2])}")
    e2 = [c for c in okn if PAISES_AMPLIA.search(c["rot"]) or OTRO_PERIMETRO.search(c["rot"])]
    lista("(f) perímetro OK, pero el rótulo de la fila nombra un país, una región u otro perímetro", e2, lambda c: f"rótulo: {c['rot'][:50]}")

    a.salida.mkdir(parents=True, exist_ok=True)
    (a.salida / "barrido_tablas.txt").write_text("\n".join(S) + "\n", encoding="utf-8")
    print("\n".join(S[:40]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
