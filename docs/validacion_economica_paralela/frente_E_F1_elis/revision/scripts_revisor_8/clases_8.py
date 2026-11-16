"""Revisión independiente n.º 8 · clases del barrido propio C14 → C16 (frente E · F1 · Elis). No modifica nada del autor.

Lee el JSONL de barrido_8.py y escribe, por la salida estándar:

  A  universo y cruce con los barridos de las revisiones n.º 6 y 7 (mismo recuento con otro arnés);
  B  aceptaciones nuevas de C16 (candidatas G que no eran OK en C14 y lo son en las seis dimensiones en C16), por clase
     de token y de línea, y por página;
  C  la regla de S1 (fecha del saldo en el rótulo): todas las líneas en que se dispara, clasificadas; las que no son
     filas de saldo se listan;
  D  la regla de S1 y la dimensión «columna»;
  E  los saldos de apertura y de cierre de los diez estados de cambios en el patrimonio: cuáles reconoce la regla;
  F  líneas en las que la fecha viene entera de las líneas de rótulo de encima (rótulo de la fila anterior);
  G  transiciones C14 → C16 por dimensión y motivo; cifras que eran OK y dejan de serlo;
  H  S2: líneas sin rótulo y rótulos contiguos; I  S3: pestaña del margen; J  S4: cabecera de países y tablas con países
     en la cabecera que conservan el perímetro OK; K  S5: líneas que dejan de ser encabezado numerado, por tipografía
     (MuPDF, si se da --pylibs);
  L  la decisión (b) de C14 (honorarios por firma auditora) y S7 d (título corto que retiene las tablas de las marcas);
  M  la zona de cabecera de C14 y de C16 en todas las líneas; N  los demás modos de control del ejercicio.

Uso: python3 -I -B clases_8.py --todas <jsonl.gz> --raiz <munger_v2_r1> --c14 <frente C15> --c16 <frente C17> [--pylibs <carpeta con pymupdf>]
"""
import argparse
import gzip
import json
import re
import sys
import unicodedata
from collections import Counter, OrderedDict, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import arnes8 as H  # noqa: E402

PUB = {}
FECHA = (r"(?:(?:DECEMBER|December),? ?\d{0,2},? ?20\d\d|JANUARY 1, 20\d\d|January 1, 20\d\d|\d\d/\d\d/20\d\d|\d\d? D[ÉE]CEMBRE 20\d\d|"
         r"\d\d? décembre 20\d\d|1(?:ER|er) (?:JANVIER|janvier) 20\d\d)")
SALDO = re.compile(r"^(?:Cash flow hedges |Couvertures de flux de trésorerie |\(In thousands of euros\) )?(?:NET CARRYING AMOUNT AS AT|VALEUR NETTE COMPTABLE AU|"
                   r"BALANCE AS AT|Balance as at|Ajusted balance as at|SOLDE AU|Solde au|AS AT|As at|AU|Au) " + FECHA +
                   r"(?:,? ?(?:restated ?\*?|RESTATED\*?|retraité\*?|published|adjusted|\(a\)|restated ?\(a\)))*$")
RECUENTO = re.compile(r"(?i)^(?:›\s*)?(?:of which\s+)?(?:Number of|Nombre d|Rights vested|rights vested outperform|NUMBER OF SHARES|NOMBRE D'ACTIONS|"
                      r"Percentage of treasury|Pourcentage de capital|Par value|Valeur nominale|Market value|Valeur du marché|Treasury shares held|Capital auto-détenu)|"
                      r"(?i:number of rights|of which (?:members|rights))")
PAISES_PROPIO = re.compile(r"\b(?:France|Germany|Allemagne|United Kingdom|Royaume-Uni|Spain|Espagne|Brazil|Brésil|Netherlands|Pays-Bas|Denmark|Danemark|Sweden|Suède|"
                           r"Switzerland|Suisse|Mexico|Mexique|Ireland|Irlande|Norway|Norvège|Italy|Italie|Portugal|Belgium|Belgique|Poland|Pologne|Chile|Chili|"
                           r"Colombia|Colombie|Finland|Finlande|Great Britain|Grande-Bretagne|Bretagne|Latvia|Austria|Luxembourg)\b")


def est(c):
    return H.estado_de_codigo(c)


def es_anio(tok):
    return bool(re.fullmatch(r"\(?20\d\d\)?[.,;:]?", tok))


def corta(l, n=120):
    return re.sub(r" {2,}", " · ", l.strip())[:n]


def clase_linea(ln):
    r = re.sub(r"\s+", " ", ln["rml16"]).strip()
    if SALDO.match(r):
        return "fila de saldo"
    if RECUENTO.search(r):
        return "recuento o dato con fecha (planes de acciones, capital, autocartera)"
    return "otra (prosa, título, sumario o cabecera)"


def plantilla(m):
    m = re.sub(r"«[^»]*»", "«…»", m)
    m = re.sub(r"\b20\d\d\b", "AAAA", m)
    m = re.sub(r"\(\d+(?:\.\d+)? caracteres\)", "(N caracteres)", m)
    m = re.sub(r"a \d+(?:\.\d+)? caracteres", "a N caracteres", m)
    m = re.sub(r"\(línea \d+\)", "(línea N)", m)
    m = re.sub(r"\([^()]*, [^()]*\)", "(…)", m)
    return m[:105]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--todas", required=True)
    ap.add_argument("--raiz", required=True)
    ap.add_argument("--c14", required=True)
    ap.add_argument("--c16", required=True)
    ap.add_argument("--pylibs")
    a = ap.parse_args()
    A, N = H.Version("C14", a.c14, a.raiz), H.Version("C16", a.c16, a.raiz)
    V = N.V
    for d in N.fuentes:
        PUB[d] = N.publicacion(d)
    L = []
    with gzip.open(a.todas, "rt", encoding="utf-8") as f:
        for l in f:
            L.append(json.loads(l))
    L.sort(key=lambda x: (x["doc"], x["p"], x["i"]))
    p = print
    DIM = {d: j for j, d in enumerate(H.DIMS)}

    def cands():
        for ln in L:
            for t in ln["toks"]:
                for y, g in t["G"].items():
                    yield ln, t, y, g

    # ------------------------------------------------------------------ A
    p("Clases del barrido propio de la revisión n.º 8 · C14 → C16")
    p()
    p("== A. Universo y cruce con los barridos anteriores ==")
    ntok = sum(len(ln["toks"]) for ln in L)
    p(f"  líneas con cifras: {len(L)}; tokens: {ntok} ({sum(len(ln['toks']) for ln in L if ln['g'])} en páginas del grupo); candidatas G: {3 * ntok}")
    # universo de la revisión n.º 6: líneas cuyo rótulo (el de C16) no es numérico, que no son el pie y no tienen solo años; tokens que no son un año suelto
    u6 = Counter()
    u6g = Counter()
    n6 = n6g = t6 = t6g = 0
    for ln in L:
        idi = N.idioma(ln["doc"])
        rot = ln["rot16"]
        if not rot or V.es_numero(rot, idi) or ln["pie"] or all(re.fullmatch(r"20\d\d", t) or t in V.PLACEHOLDER for t in V.tokens_numericos(ln["l"], idi)):
            continue
        for t in ln["toks"]:
            if re.fullmatch(r"20\d\d", t["tok"]):
                continue
            t6 += 1
            t6g += ln["g"]
            for y, g in t["G"].items():
                n6 += 1
                u6[(est(g["a"]), est(g["n"]))] += 1
                if ln["g"]:
                    n6g += 1
                    u6g[(est(g["a"]), est(g["n"]))] += 1
    p(f"  restringido al universo del barrido de la revisión n.º 6 (líneas con rótulo, sin años sueltos ni pies): {t6} tokens, {n6} candidatas; "
      f"en páginas del grupo, {t6g} tokens y {n6g} candidatas")
    p("    transiciones del estado de la fila, todas las páginas: " + "; ".join(f"{x} → {y}: {v}" for (x, y), v in sorted(u6.items()) if x != y))
    p("    transiciones del estado de la fila, páginas del grupo: " + "; ".join(f"{x} → {y}: {v}" for (x, y), v in sorted(u6g.items()) if x != y))
    p("    (el barrido de la revisión n.º 6 sobre C16, que guarda el autor, da 124887 candidatas y 41629 tokens; 72036 y 24012 en páginas del grupo; "
      "FALLO → OK 6, FALLO → PENDIENTE 247 [178 en el grupo], OK → FALLO 3, OK → PENDIENTE 37, PENDIENTE → FALLO 811 [688], PENDIENTE → OK 340)")

    # ------------------------------------------------------------------ B
    p()
    p("== B. Aceptaciones nuevas de C16: candidatas G que no eran OK en C14 y son OK en las seis dimensiones en C16 ==")
    nuevas = [(ln, t, y, g) for ln, t, y, g in cands() if est(g["n"]) == "OK" and est(g["a"]) != "OK"]
    p(f"  total: {len(nuevas)} (en páginas del grupo: {sum(1 for x in nuevas if x[0]['g'])}); desde PENDIENTE: {sum(1 for x in nuevas if est(x[3]['a']) == 'PENDIENTE')}; "
      f"desde FALLO: {sum(1 for x in nuevas if est(x[3]['a']) == 'FALLO')}")
    p(f"  dimensión que cambia: {dict(Counter(''.join(d for d in H.DIMS if g['a'][DIM[d]] != g['n'][DIM[d]]) for _, _, _, g in nuevas))}; "
      f"motivo del ejercicio en C16: {dict(Counter(plantilla(g['dn']['ejercicio']) for _, _, _, g in nuevas))}")

    def clase_token(ln, t):
        tok = t["tok"]
        cl = clase_linea(ln)
        if not cl.startswith("fila de saldo"):
            return "año de la fecha en una línea que no es una fila de saldo" if es_anio(tok) else "otra cifra en una línea que no es una fila de saldo"
        if es_anio(tok):
            return "año de la fecha del propio rótulo, en una fila de saldo"
        if t["k"] == 0 and re.fullmatch(r"\d", tok) and ln["rot14"] != ln["rot16"]:
            return "pestaña del capítulo («6») en una fila de saldo"
        if re.fullmatch(r"\d\d?", tok) and re.search(r"(?i)december,? ?" + tok + r"\b|" + tok + r" d[ée]cembre", ln["l"][:t["a1"] + 12]) and t["a0"] < len(ln["rot16"]) + (len(ln["l"]) - len(ln["l"].lstrip())) + 2:
            return "día de la fecha del propio rótulo («31»), en una fila de saldo"
        return "cifra de una fila de saldo"
    cb = Counter(clase_token(ln, t) for ln, t, y, g in nuevas)
    for k, v in sorted(cb.items(), key=lambda kv: -kv[1]):
        p(f"  {v:4} · {k}")
    en6 = sum(1 for ln, t, y, g in nuevas if not re.fullmatch(r"20\d\d", t["tok"]))
    p(f"  de ellas, en el universo de la revisión n.º 6 (sin años sueltos): {en6} (el autor declara 346)")
    p("  por página (cifras de filas de saldo · otros tokens):")
    pp = OrderedDict()
    for ln, t, y, g in nuevas:
        c = clase_token(ln, t)
        k = (ln["doc"], ln["p"])
        pp.setdefault(k, [0, 0, set()])
        pp[k][0 if c == "cifra de una fila de saldo" else 1] += 1
        pp[k][2].add(re.sub(r"\d", "9", H.sin_anios(re.sub(r"\s+", " ", ln["rml16"])))[:60])
    for (doc, pag), (n1, n2, rots) in pp.items():
        p(f"    {doc} p.{pag}: {n1} · {n2} · rótulos: " + "; ".join(f"«{r}»" for r in sorted(rots)))
    p("  tokens aceptados que no son cifras de un saldo:")
    for ln, t, y, g in nuevas:
        c = clase_token(ln, t)
        if c != "cifra de una fila de saldo" and not c.startswith("año de la fecha del propio rótulo"):
            p(f"    {ln['doc']} p.{ln['p']} l.{ln['i'] + 1} · «{t['tok']}» declarado {y} · {c} · «{corta(ln['l'], 110)}»")

    # ------------------------------------------------------------------ C
    p()
    p("== C. Regla de S1: líneas en las que `anio_de_saldo_en_rotulo` da un ejercicio (todas las páginas) ==")
    S1 = [ln for ln in L if ln["a_rot"] is not None]
    p(f"  líneas: {len(S1)} (en páginas del grupo: {sum(ln['g'] for ln in S1)}); tokens: {sum(len(ln['toks']) for ln in S1)}")
    cc = Counter()
    for ln in S1:
        cc[(clase_linea(ln), "en páginas del grupo" if ln["g"] else "fuera de las páginas del grupo")] += 1
    for k, v in sorted(cc.items()):
        p(f"  {v:4} líneas · {k[0]} · {k[1]}")
    otras = [ln for ln in S1 if clase_linea(ln).startswith("otra")]
    tk_no_anio = [(ln, t) for ln in otras for t in ln["toks"] if not es_anio(t["tok"])]
    p(f"  en las {len(otras)} líneas que no son filas de saldo ni recuentos con fecha: {sum(len(ln['toks']) for ln in otras)} tokens; "
      f"{sum(1 for ln in otras for t in ln['toks'] if es_anio(t['tok']))} son el año de la propia fecha; {len(tk_no_anio)} no lo son:")
    for ln, t in tk_no_anio:
        y = str(ln["a_rot"])
        g = t["G"].get(y)
        p(f"    {ln['doc']} p.{ln['p']} l.{ln['i'] + 1} · «{t['tok']}» · con el ejercicio del rótulo ({y}): "
          + (f"C14 {g['a']} → C16 {g['n']} ({est(g['n'])}; unidad: {g['dn']['unidad'][:48]})" if g else "fuera de E, E−1, E−2") + f" · «{corta(ln['l'], 95)}»")
    ok6 = [(ln, t, y) for ln in otras for t in ln["toks"] for y, g in t["G"].items() if est(g["n"]) == "OK"]
    p(f"  candidatas OK en las seis dimensiones en esas líneas: {len(ok6)}: " + "; ".join(f"{ln['doc']} p.{ln['p']} l.{ln['i'] + 1} «{t['tok']}» ({y})" for ln, t, y in ok6))
    p("  las líneas que no son filas de saldo ni recuentos con fecha (página · línea · texto):")
    for ln in otras:
        p(f"    {ln['doc']} p.{ln['p']} l.{ln['i'] + 1} g={ln['g']} · {ln['a_rot']} · «{corta(ln['l'], 125)}»")

    # ------------------------------------------------------------------ D
    p()
    p("== D. Regla de S1 y dimensión «columna» ==")
    cifras = [(ln, t, y, g) for ln, t, y, g in nuevas if clase_token(ln, t) == "cifra de una fila de saldo"]
    p(f"  cifras de filas de saldo aceptadas: {len(cifras)}; estado de «columna»: {dict(Counter(g['n'][DIM['columna']] for _, _, _, g in cifras))} "
      f"(N = NO_APLICA); motivo: {dict(Counter(g['dn']['columna'] for _, _, _, g in cifras))}")
    ncol = Counter()
    for ln, t, y, g in cifras:
        ncol[sum(1 for x in ln["toks"] if not es_anio(x["tok"]) and not (x["k"] == 0 and re.fullmatch(r"\d\d?", x["tok"])))] += 1
    p(f"  por número de cifras de la fila (columnas de datos de la tabla): {dict(sorted(ncol.items()))}; en filas de dos columnas o más: {sum(v for k, v in ncol.items() if k >= 2)}")
    p("  (con un identificador de concepto de saldo, el modo «saldo» sí comprueba la columna: contraejemplos_8.py, T1a–T1c)")

    # ------------------------------------------------------------------ E
    p()
    p("== E. Estado de cambios en el patrimonio: saldos de apertura y de cierre, y lo que da la regla de S1 ==")
    ESTADOS = {"URD2021": (230, 231), "URD2022": (262, 263), "URD2023": (280, 281), "DEU2024FR": (274, 275), "URD2025": (328, 329)}
    for doc, pags in ESTADOS.items():
        for pag in pags:
            lineas = N.lineas(doc, pag)
            idi = N.idioma(doc)
            for i, l in enumerate(lineas):
                if not re.search(r"(?i)balance as at|solde au|^\s*(?:DECEMBER|DÉCEMBRE|31, 20|20\d\d\b|\(?RESTATED|RETRAITÉ|December 31|January 1)", l):
                    continue
                toks = [t for t in V.tokens_numericos(l, idi) if t not in V.PLACEHOLDER]
                if len(toks) < 10:
                    continue
                arriba = " / ".join(x.strip() for x in lineas[max(0, i - 2):i] if x.strip() and len(V.trozos(x)) == 1 and len(V.tokens_numericos(x, idi)) <= 1
                                    and not re.search(r"(?i)income|global|r[ée]sultat", x))
                ar = V.anio_de_saldo_en_rotulo(lineas, i, idi)
                p(f"  {doc} p.{pag} l.{i + 1} · rótulo «{arriba} / {V.rotulo(l)}» · {len(toks)} tokens · regla de S1: "
                  + (f"saldo de {ar}" if ar is not None else "NO lo reconoce (ejercicio por columna: PENDIENTE)"))

    # ------------------------------------------------------------------ F
    p()
    p("== F. Regla de S1: líneas cuyo propio rótulo no lleva ningún año y reciben la fecha de las líneas de encima ==")
    for ln in S1:
        if not re.search(r"20\d\d", ln["rot16"]):
            p(f"  {ln['doc']} p.{ln['p']} l.{ln['i'] + 1} g={ln['g']} · ejercicio {ln['a_rot']} · rótulo propio «{ln['rot16'][:60]}» · rótulo unido «{ln['rml16'][:90]}»")
            for c in ln["ctx"]:
                p("        |" + c[:150])

    # ------------------------------------------------------------------ G
    p()
    p("== G. Transiciones C14 → C16 por dimensión y motivo (candidatas G, todas las páginas) ==")
    tr = Counter()
    pg = defaultdict(Counter)
    for ln, t, y, g in cands():
        for d in H.DIMS:
            j = DIM[d]
            if g["a"][j] != g["n"][j]:
                k = (d, g["a"][j] + " → " + g["n"][j], plantilla(g["da"][d]), plantilla(g["dn"][d]))
                tr[k] += 1
                pg[k][(ln["doc"], ln["p"])] += 1
    for k, v in sorted(tr.items(), key=lambda kv: (kv[0][0], -kv[1])):
        p(f"  {k[0]}: {k[1]} · {v} candidatas en {len(pg[k])} páginas")
        p(f"      C14: {k[2]}")
        p(f"      C16: {k[3]}")
        p("      " + ", ".join(f"{d} p.{pag} ({n})" for (d, pag), n in pg[k].most_common(10)) + (" …" if len(pg[k]) > 10 else ""))
    p()
    p("  Candidatas OK en las seis dimensiones en C14 que dejan de serlo en C16:")
    for ln, t, y, g in cands():
        if est(g["a"]) == "OK" and est(g["n"]) != "OK":
            d = next(d for d in H.DIMS if g["a"][DIM[d]] != g["n"][DIM[d]])
            p(f"    {ln['doc']} p.{ln['p']} l.{ln['i'] + 1} · «{t['tok']}» declarado {y} · {est(g['n'])} · {d}: {g['dn'][d][:105]} · «{corta(ln['l'], 60)}»")

    # ------------------------------------------------------------------ H
    p()
    p("== H. S2: líneas de cifras sin rótulo y rótulos de las líneas contiguas (`rotulos_sin_rotulo`) ==")
    sr = [ln for ln in L if ln["rsr"]]
    p(f"  líneas en las que la función devuelve algún rótulo: {len(sr)} (en páginas del grupo: {sum(ln['g'] for ln in sr)}); "
      f"de ellas, líneas con solo la pestaña del capítulo o un número suelto: {sum(1 for ln in sr if ln['n'] == 1 and ln['nceldas'] == 1)}")
    largo = Counter()
    for ln in sr:
        largo["algún rótulo contiguo de más de 45 caracteres" if any(len(r) > 45 for r in ln["rsr"]) else "todos de 45 caracteres o menos"] += 1
    p(f"  longitud de los rótulos tomados: {dict(largo)} (`rotulo_multilinea` corta en 45; `rotulos_sin_rotulo` no tiene límite)")
    p("  líneas en las que el perímetro del grupo pasa de OK a FALLO por el rótulo de las líneas contiguas o por la pestaña (S2 y S3):")
    vistos = set()
    for ln, t, y, g in cands():
        j = DIM["perimetro"]
        if g["a"][j] == "O" and g["n"][j] == "F" and (ln["doc"], ln["p"], ln["i"]) not in vistos:
            vistos.add((ln["doc"], ln["p"], ln["i"]))
            p(f"    {ln['doc']} p.{ln['p']} l.{ln['i'] + 1} · «{corta(ln['l'], 70)}» · {g['dn']['perimetro'][:150]}")
    p("  perímetro declarado de un segmento que pasa de FALLO a OK (perfil S):")
    for ln in L:
        for t in ln["toks"]:
            for s, m in t["S"].items():
                if m["a"] != m["n"]:
                    p(f"    {ln['doc']} p.{ln['p']} l.{ln['i'] + 1} g={ln['g']} · «{t['tok']}» · segmento {s}: {m['a']} → {m['n']} · rótulos contiguos {ln['rsr'][:3]} · «{corta(ln['l'], 60)}»")

    # ------------------------------------------------------------------ I
    p()
    p("== I. S3: líneas cuyo rótulo cambia por la pestaña del margen (`rotulo` de C14 ≠ `rotulo` de C16) ==")
    dif = [ln for ln in L if ln["rot14"] != ln["rot16"]]
    ci = Counter()
    for ln in dif:
        cambia = any(g["a"] != g["n"] for t in ln["toks"] for g in t["G"].values())
        con = any(not (t["k"] == 0 and re.fullmatch(r"\d", t["tok"])) for t in ln["toks"])
        ci[("grupo" if ln["g"] else "no grupo", "con cifras además de la pestaña" if con else "solo la pestaña", "cambia algún estado" if cambia else "sin cambios")] += 1
    p(f"  líneas: {len(dif)} (en páginas del grupo: {sum(ln['g'] for ln in dif)})")
    for k, v in sorted(ci.items()):
        p(f"    {v:4} · {' · '.join(k)}")
    for ln in dif:
        if ln["g"] and any(not (t["k"] == 0 and re.fullmatch(r"\d", t["tok"])) for t in ln["toks"]) and any(g["a"] != g["n"] for t in ln["toks"] for g in t["G"].values()):
            p(f"    cambia: {ln['doc']} p.{ln['p']} l.{ln['i'] + 1} · «{corta(ln['l'], 90)}»")

    # ------------------------------------------------------------------ J
    p()
    p("== J. S4: cabecera con una columna por país (`cabecera_de_paises`) ==")
    cp = Counter()
    for ln in L:
        for t in ln["toks"]:
            if "cp" in t:
                g = t["G"][str(PUB[ln["doc"]])]
                cp[(ln["doc"], ln["p"], ln["g"], g["a"][DIM["perimetro"]] + "→" + g["n"][DIM["perimetro"]])] += 1
    for k, v in sorted(cp.items()):
        p(f"  {k[0]} p.{k[1]} (grupo: {k[2]}): {v} tokens bajo una cabecera de países · perímetro {k[3]}")
    p("  Lectura propia: líneas de cabecera de las páginas del grupo con dos países o más en celdas cortas, y tokens de las 25 líneas siguientes con el perímetro OK en C16")
    porlinea = {(ln["doc"], ln["p"], ln["i"]): ln for ln in L}
    for doc in sorted(N.fuentes):
        idi = N.idioma(doc)
        for pag in range(1, N.paginas(doc) + 1):
            lineas = N.lineas(doc, pag)
            if not N.es_pagina_del_grupo(lineas):
                continue
            for i, l in enumerate(lineas):
                celdas = [c for c in re.split(r"\s{2,}", l.strip()) if c]
                cpais = [c for c in celdas if PAISES_PROPIO.search(c) and len(c.split()) <= 4 and not re.search(r"\d", c)]
                if len(celdas) >= 3 and len(cpais) >= 2 and len(set(PAISES_PROPIO.findall(l))) >= 2 and not V.tokens_numericos(l, idi) \
                        and not any(rx.search(l) for rx, _ in V.UNIDAD_RX) and not V.PALABRA_SEGMENTO.search(re.sub(r"France", "", l)):
                    ok = tot = 0
                    ej = []
                    for k in range(i + 1, min(len(lineas), i + 26)):
                        ln = porlinea.get((doc, pag, k))
                        if not ln:
                            continue
                        for t in ln["toks"]:
                            tot += 1
                            if t["G"][str(PUB[doc])]["n"][DIM["perimetro"]] == "O":
                                ok += 1
                                if k + 1 not in [e[0] for e in ej]:
                                    ej.append((k + 1, corta(lineas[k], 60)))
                    p(f"    {doc} p.{pag} l.{i + 1} «{corta(l, 85)}» · {tot} tokens debajo, {ok} con el perímetro OK" + ("" if not ok else " · en: " + "; ".join(f"l.{e[0]} «{e[1]}»" for e in ej[:4])))

    # ------------------------------------------------------------------ K
    p()
    p("== K. S5: líneas que C14 toma por encabezado numerado y C16 no ==")
    difh = []
    tot = Counter()
    for doc in sorted(N.fuentes):
        idi = N.idioma(doc)
        for pag in range(1, N.paginas(doc) + 1):
            lineas = N.lineas(doc, pag)
            g = N.es_pagina_del_grupo(lineas)
            for i, l in enumerate(lineas):
                t = l.strip()
                x, y = A.V.es_encabezado_numerado(t, idi), V.es_encabezado_numerado(t, idi)
                tot[("C14", g)] += x
                tot[("C16", g)] += y
                if x != y:
                    difh.append((doc, pag, i + 1, g, x, y, t))
    p(f"  encabezados numerados en páginas del grupo: C14 {tot[('C14', True)]}, C16 {tot[('C16', True)]}; en las demás: C14 {tot[('C14', False)]}, C16 {tot[('C16', False)]}; "
      f"líneas distintas: {len(difh)} (ninguna pasa a serlo: {not any(d[5] for d in difh)})")
    tipo = {}
    if a.pylibs:
        sys.path.insert(0, a.pylibs)
        import warnings
        warnings.filterwarnings("ignore")
        import pymupdf
        docs = {}

        def norm(s):
            return re.sub(r"\s+", "", unicodedata.normalize("NFKC", s).replace("’", "'").replace("‘", "'"))
        for doc, pag, i, g, x, y, t in difh:
            d = docs.setdefault(doc, pymupdf.open(str(N.pdf(doc))))
            sp = [s for b in d[pag - 1].get_text("dict")["blocks"] for ln_ in b.get("lines", []) for s in ln_["spans"] if s["text"].strip()]
            cuerpo = Counter(round(s["size"], 1) for s in sp).most_common(1)[0][0]
            m = V.ENCABEZADO_NUMERADO.match(t)
            cola = norm(t[m.end():])[:12]
            num = norm(t[:m.end()])      # el número del encabezado («3.2», «NOTE6», «Note6.1»)
            c = [s for s in sp if cola and cola in norm(s["text"])]

            def con_numero(s):
                """El tramo lleva el número del encabezado o lo tiene en su misma línea (solape vertical): así no se toma
                por la línea el titulillo de la página, que repite el texto del título sin su número."""
                if num in norm(s["text"]):
                    return True
                y0, y1 = s["bbox"][1], s["bbox"][3]
                return any(norm(o["text"]).startswith(num) and min(y1, o["bbox"][3]) - max(y0, o["bbox"][1]) > 0.3 * min(y1 - y0, o["bbox"][3] - o["bbox"][1])
                           for o in sp)
            c = [s for s in c if con_numero(s)] or c
            if not c:
                tipo[(doc, pag, i)] = "sin lectura"
            else:
                s = c[0]
                negrita = bool(s["flags"] & 16) or any(w in s["font"] for w in ("Bold", "Black", "Semi"))
                tipo[(doc, pag, i)] = (f"TÍTULO por tipografía ({s['size']:.0f} pt, {s['font'].split('-')[-1]}; cuerpo {cuerpo:.0f})"
                                       if (s["size"] > cuerpo + 0.9 or (negrita and s["size"] >= cuerpo)) else f"texto ({s['size']:.1f} pt; cuerpo {cuerpo:.1f})")
        p(f"  por tipografía (MuPDF): {dict(Counter((re.sub(r' *[(].*', '', v), 'grupo' if any(dd[3] for dd in difh if (dd[0], dd[1], dd[2]) == k) else 'no grupo') for k, v in tipo.items()))}")
    for doc, pag, i, g, x, y, t in difh:
        p(f"    {doc} p.{pag} l.{i} g={int(g)} · {tipo.get((doc, pag, i), '')} · «{t[:110]}»")

    # ------------------------------------------------------------------ L
    p()
    p("== L. Decisión (b) de C14 y S7 d ==")
    cg = Counter()
    for ln, t, y, g in cands():
        if "la cabecera repite los ejercicios" in g["dn"]["perimetro"]:
            solo = all(x in "ON" for j, x in enumerate(g["n"]) if j != DIM["perimetro"])
            cg[(ln["doc"], ln["p"], "solo el perímetro impide el OK" if solo else "otras dimensiones también", corta(ln["l"], 40) if False else "")] += 1
    p("  Regla de grupos de columnas en C16: candidatas retenidas, por página")
    for k, v in sorted(cg.items()):
        p(f"    {k[0]} p.{k[1]} · {k[2]}: {v}")
    p(f"    total en las que solo el perímetro impide el OK: {sum(v for k, v in cg.items() if k[2].startswith('solo'))}")
    p("  Título corto de tabla que retiene las tablas siguientes (S7 d): tokens bajo el epígrafe de las marcas con el motivo del título de otro país")
    for doc, pag in (("URD2021", 272), ("URD2022", 305), ("URD2023", 324)):
        lineas = N.lineas(doc, pag)
        ini = next((i for i, l in enumerate(lineas) if re.search(r"unamortized brands", l)), None)
        if ini is None:
            continue
        res = Counter()
        for k in range(ini, len(lineas)):
            if re.match(r"\s*NOTE \d", lineas[k]):
                break
            ln = porlinea.get((doc, pag, k))
            if not ln or ln["pie"]:
                continue
            for t in ln["toks"]:
                g = t["G"][str(PUB[doc])]
                m = re.search(r"el título «([^»]*)»", g["dn"]["perimetro"])
                res[(f"perímetro {est('O' * 4 + g['n'][DIM['perimetro']] + 'O')}" + (f" por el título «{m.group(1)}»" if m else ""), )] += 1
        p(f"    {doc} p.{pag}, desde «Sensitivity of tests for unamortized brands»: " + "; ".join(f"{k[0]}: {v} tokens" for k, v in sorted(res.items())))

    # ------------------------------------------------------------------ M
    p()
    p("== M. Zona de cabecera (`zona_de_cabecera`) de C14 y de C16 en todas las líneas con cifras ==")
    cont, quitadas, anadidas = Counter(), Counter(), Counter()
    ndif = ndifg = 0
    for ln in L:
        doc, pag, i = ln["doc"], ln["p"], ln["i"]
        lineas, idi = N.lineas(doc, pag), N.idioma(doc)
        za, zn = A.V.zona_de_cabecera(lineas, i, idi), V.zona_de_cabecera(lineas, i, idi)
        if za == zn:
            continue
        ndif += 1
        ndifg += ln["g"]
        for z in set(za) - set(zn):
            if any(k >= 0 and V.es_encabezado_numerado(lineas[k].strip(), idi) and V.es_continuacion_de_encabezado(lineas, k, z) for k in (z - 1, z - 2)):
                cont[(doc, pag, z + 1, lineas[z].strip()[:60])] += 1
            else:
                quitadas[(doc, pag)] += 1
        for z in set(zn) - set(za):
            anadidas[(doc, pag)] += 1
    p(f"  líneas con la zona distinta: {ndif} de {len(L)} (en páginas del grupo: {ndifg})")
    p(f"  continuaciones de un encabezado numerado que salen de la zona: {len(cont)} líneas distintas")
    for k in sorted(cont):
        p(f"    {k[0]} p.{k[1]} l.{k[2]} · «{k[3]}»")
    p(f"  otras líneas que salen (las de encima del encabezado): {sum(quitadas.values())} en {len(quitadas)} páginas")
    p(f"  líneas que entran (regla del rótulo partido de S4): {sum(anadidas.values())} en {len(anadidas)} páginas: "
      + ", ".join(f"{d} p.{pg_} ({n})" for (d, pg_), n in sorted(anadidas.items())))

    # ------------------------------------------------------------------ N
    p()
    p("== N. Los demás modos de control del ejercicio (perfil M): líneas con alguna diferencia de ejercicio o de columna entre C14 y C16 ==")
    lm = OrderedDict()
    okm = Counter()
    for ln in L:
        for t in ln["toks"]:
            for clave, m in t["M"].items():
                idf = clave.split("|")[0]
                ea, en = est(m["a"]), est(m["n"])
                if ea == "OK":
                    okm[(idf, "C14")] += 1
                if en == "OK":
                    okm[(idf, "C16")] += 1
                if ea != en and "OK" in (ea, en):
                    okm[(idf, f"fila {ea} → {en}")] += 1
                if m["a"][1:3] != m["n"][1:3]:
                    lm.setdefault((ln["doc"], ln["p"], ln["i"]), [ln, set()])[1].add(idf.split("_B8")[0])
    p("  filas OK en las seis dimensiones por identificador de sondeo: "
      + "; ".join(f"{idf}: C14 {okm[(idf, 'C14')]}, C16 {okm[(idf, 'C16')]}" + "".join(f", {k[1]}: {v}" for k, v in sorted(okm.items()) if k[0] == idf and k[1].startswith("fila"))
                  for idf, _ in H.PERFILES_DE_MODO))
    p(f"  líneas con alguna diferencia de ejercicio o de columna: {len(lm)}")
    for (doc, pag, i), (ln, ids) in lm.items():
        p(f"    {doc} p.{pag} l.{i + 1} g={ln['g']} · «{corta(ln['l'], 90)}» · {', '.join(sorted(ids))}")


if __name__ == "__main__":
    main()
