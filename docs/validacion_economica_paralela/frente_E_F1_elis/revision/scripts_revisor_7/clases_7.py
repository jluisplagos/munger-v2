"""Revisión n.º 7 (frente E · F1 · Elis). Clases del barrido propio (barrido_7.py), cruzadas con la lectura propia por
MuPDF (geo7.py) y con las variantes del verificador de C14 (arnes7.py). No modifica nada del autor.

Secciones:
  A  candidatas OK en las seis dimensiones en C14 según la cabecera inmediata de su columna (lectura propia);
  B  transiciones de la fila C13 → C14 a FALLO o a PENDIENTE, por motivo y lectura propia;
  C  decisión (a): la regla de cabecera ajena no se aplica al asignar por orden — lo que la propuesta retendría;
     cabeceras que repiten ejercicios, con y sin periodo; asignaciones por orden desplazadas;
  D  decisión (b): lo que retiene la regla de grupos de columnas, por tabla y por grupo;
  E  decisión (c): umbral de 5,5 frente a 3 — qué FALLO pasaría a PENDIENTE y qué dice la lectura propia; saldos con la
     fecha en el rótulo que fallan con su propio ejercicio;
  F  R2: líneas que cortan la búsqueda del título como «encabezado numerado» y cuántas no lo son por tipografía;
  G  R4: títulos cortos que retienen, y tablas con columnas por país que conservan el perímetro OK;
  H  R5 y R1: filas con prefijo de UGE y filas de jurisdicción;
  I  líneas sin rótulo (fuera del universo del barrido de la revisión n.º 6): candidatas OK y líneas con el número de
     capítulo del margen en lugar del rótulo;
  J  «la cabecera es la de la propia tabla»: líneas tomadas por cabecera de otra tabla.

Uso: python3 -I clases_7.py --todas <barrido.jsonl.gz> --raiz <munger_v2_r1> --autor <frente C14> --pylibs <carpeta con pymupdf>
"""
import argparse
import collections
import gzip
import json
import re
import sys
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import arnes7  # noqa: E402
import geo7  # noqa: E402

DIMS = arnes7.DIMS
CAL = re.compile(r"(?i)^(?:\(?\*+\)?|\(\d+\)|\([a-z]\)|restated\*{0,2}|retrait[ée]e?s?\*{0,2}|adjusted\*?|ajust[ée]e?s?\*?|published|reported|"
                 r"publi[ée]e?s?|net|nets?|nette?s?)$")
# lista propia de países y segmentos, más amplia que la del autor
PAISES7 = ["France", "Germany", "Allemagne", "Austria", "Autriche", "Belgium", "Belgique", "Luxembourg", "Netherlands", "Pays-Bas", "Poland",
           "Pologne", "Czech Republic", "République tchèque", "Hungary", "Hongrie", "Slovakia", "Slovaquie", "Switzerland", "Suisse", "Denmark",
           "Danemark", "Finland", "Finlande", "Norway", "Norvège", "Sweden", "Suède", "Estonia", "Estonie", "Latvia", "Lettonie", "Lithuania",
           "Lituanie", "Russia", "Russie", "United Kingdom", "Royaume-Uni", "Great Britain", "Grande-Bretagne", "Ireland", "Irlande", "Brazil",
           "Brésil", "Chile", "Chili", "Colombia", "Colombie", "Mexico", "Mexique", "Spain", "Espagne", "Andorra", "Andorre", "Italy", "Italie",
           "Portugal", "Malaysia", "Malaisie", "Singapore", "Singapour", "Cyprus", "Chypre", "Central Europe", "Europe centrale", "Scandinavia",
           "Scandinavie", "Eastern Europe", "Europe de l'Est", "UK & Ireland", "Latin America", "Amérique latine", "Southern Europe",
           "Europe du Sud", "European Union", "Union européenne"]
RXP7 = re.compile(r"(?i)\b(?:" + "|".join(re.escape(x) for x in sorted(PAISES7, key=len, reverse=True)) + r")\b")
RX_CIERRE = re.compile(r"(?i)(?:12/31/|31/12/|december\s+31,\s*|31\s+décembre\s+|^31,\s*)(20\d\d)")
RX_APERT = re.compile(r"(?i)(?:january\s+1,\s*|1er\s+janvier\s+|01/01/|1/1/)(20\d\d)")


def ok6(e):
    return all(x in "ON" for x in e)


def fila(e):
    return "FALLO" if ("F" in e or "E" in e) else "PENDIENTE" if "P" in e else "OK"


def pg(t):
    return f"{t['doc']} p.{t['p']}"


def ej(t, c=None):
    s = f"{t['doc']} p.{t['p']} l.{t['i'] + 1} token {t['idx'] + 1}/{t['n']} «{t['tok']}» · «{t['rot'][:44]}»"
    return s + (f" declarado {c['anio']}" if c else "")


def tipo_celda(txt):
    resto = [w for w in re.sub(r"\d{1,2}/\d{1,2}/20\d\d|\b20\d\d\b", " ", txt).split() if not CAL.match(w)]
    if re.search(r"20\d\d", txt) and not resto:
        return "fecha"
    if len(txt.split()) <= 6 and not re.search(r"[.;:]$|, ", txt) and len(txt) <= 45:
        return "corta"
    return "prosa"


def lectura(t):
    """(ejercicios, palabras ajenas) de las celdas de cabecera inmediatas de la columna: la pila, desde abajo, hasta la
    primera celda de prosa."""
    g = t.get("g")
    if not g:
        return None
    anios, ajenas = [], []
    for txt in g["pila"]:
        k = tipo_celda(txt)
        if k == "prosa":
            break
        for m in re.finditer(r"(?:(\d{1,2})/(\d{1,2})/)?(20\d\d)", txt):
            a = int(m.group(3))
            if m.group(1) and int(m.group(1)) == 1 and int(m.group(2)) == 1:
                a -= 1
            anios.append(a)
        if k == "corta":
            r = " ".join(w for w in re.sub(r"\d{1,2}/\d{1,2}/20\d\d|\b20\d\d\b", " ", txt).split() if not CAL.match(w))
            if re.search(r"[^\W\d_]{2,}", r):
                ajenas.append(r)
    return anios, ajenas


def clase(t, c):
    r = lectura(t)
    if r is None:
        return "sin lectura"
    anios, ajenas = r
    if anios and c["anio"] in anios:
        return "fecha del ejercicio declarado" + (" y, además, otra cabecera" if ajenas else "")
    if anios:
        return "fecha de OTRO ejercicio" + (" y, además, otra cabecera" if ajenas else "")
    return "ninguna fecha" + (" (cabecera propia sin fecha)" if ajenas else " (sin cabecera inmediata)")


def anio_de_fila(t):
    m = RX_APERT.search(t["rot"])
    if m:
        return int(m.group(1)) - 1
    m = RX_CIERRE.search(t["rot"])
    return int(m.group(1)) if m else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--todas", required=True)
    ap.add_argument("--raiz", required=True)
    ap.add_argument("--autor", required=True)
    ap.add_argument("--pylibs", required=True)
    a = ap.parse_args()
    T = [json.loads(l) for l in gzip.open(a.todas, "rt", encoding="utf-8")]
    C = [(t, c) for t in T for c in t["c"]]
    p = print
    p("Clases del barrido propio de la revisión n.º 7 · páginas del grupo · C13 → C14 y variantes de C14\n")
    p(f"Tokens: {len(T)} ({sum(t['cr'] for t in T)} en líneas con rótulo, {sum(1 for t in T if not t['cr'])} en líneas sin rótulo); "
      f"candidatas: {len(C)}; con lectura propia: {sum(1 for t in T if 'g' in t)} tokens")
    p(f"OK en las seis dimensiones: C13 {sum(1 for t, c in C if ok6(c['c13']))} · C14 {sum(1 for t, c in C if ok6(c['c14']))}; "
      f"candidatas que no eran OK en C13 y lo son en C14: {sum(1 for t, c in C if ok6(c['c14']) and not ok6(c['c13']))}")

    # ---------------------------------------------------------------- A
    p("\n\n== A. Candidatas OK en las seis dimensiones en C14, según la cabecera inmediata de su columna (lectura propia) ==")
    cnt = collections.Counter(clase(t, c) for t, c in C if ok6(c["c14"]))
    for k, v in cnt.most_common():
        p(f"   {v:5d}  {k}")
    p("   (cabecera inmediata: las celdas cortas que el número tiene encima en su misma banda, hasta la primera línea de prosa)")
    sin = collections.Counter()
    for t, c in C:
        if ok6(c["c14"]) and clase(t, c).startswith("ninguna fecha"):
            sin[(pg(t), " ‖ ".join(t["g"]["pila"][:2])[:50])] += 1
    p("   sin fecha en la cabecera inmediata, por página y cabecera (las 14 mayores): " +
      "; ".join(f"{k[0]} «{k[1]}» ({n})" for k, n in sin.most_common(14)))

    # ---------------------------------------------------------------- B
    p("\n\n== B. Estado de la fila C13 → C14: transiciones a FALLO o a PENDIENTE, por dimensión, motivo y lectura propia ==")
    for x, y in (("OK", "FALLO"), ("OK", "PENDIENTE"), ("PENDIENTE", "FALLO"), ("FALLO", "PENDIENTE")):
        sel = [(t, c) for t, c in C if fila(c["c13"]) == x and fila(c["c14"]) == y]
        p(f"\n  {x} → {y}: {len(sel)} candidatas ({sum(1 for t, c in sel if t['cr'])} en líneas con rótulo)")
        grp = collections.defaultdict(list)
        for t, c in sel:
            dims = [k for k, u, v in zip(DIMS, c["c13"], c["c14"]) if u != v]
            mot = " | ".join(re.sub(r"\d+(?:\.\d+)? caracteres", "N caracteres", re.sub(r"«[^»]*»", "«…»", re.sub(r"\(línea \d+\)", "", re.sub(
                r"20\d\d", "AAAA", re.sub(r"\([A-ZÉa-zé]+\) en una", "(…) en una", c["d14"].get(k, ""))))))[:86] for k in dims)
            grp[(",".join(dims), mot, clase(t, c) if "ejercicio" in dims else "—")].append((t, c))
        for (dims, mot, lec), v in sorted(grp.items(), key=lambda z: -len(z[1]))[:12]:
            pp = collections.Counter(pg(t) for t, c in v)
            p(f"    {len(v):5d} · {dims} · {mot}" + (f" · lectura propia: {lec}" if lec != "—" else ""))
            p("            páginas: " + ", ".join(f"{q} ({n})" for q, n in pp.most_common(7)) + (" …" if len(pp) > 7 else ""))
        if len(grp) > 12:
            p(f"    … y otros {len(grp) - 12} motivos con {sum(len(v) for k, v in sorted(grp.items(), key=lambda z: -len(z[1]))[12:])} candidatas")
    sel = [(t, c) for t, c in C if c["c13"][1] == "F" and c["c14"][1] == "P" and t["cr"]]
    p(f"\n  Dimensión «ejercicio», FALLO → PENDIENTE en líneas con rótulo: {len(sel)} · lectura propia:")
    for k, v in collections.Counter(clase(t, c) for t, c in sel).most_common():
        p(f"    {v:5d}  {k}")
    otro = [(t, c) for t, c in sel if clase(t, c).startswith("fecha de OTRO")]
    p("    con fecha de otro ejercicio en la cabecera inmediata, por página: " +
      ", ".join(f"{q} ({n})" for q, n in collections.Counter(pg(t) for t, c in otro).most_common()))

    # ---------------------------------------------------------------- C
    p("\n\n== C. Decisión (a): la regla de cabecera ajena no se aplica cuando la columna se asigna por orden ==")
    V = "ajena_en_orden"
    sel = [(t, c) for t, c in C if V in c and c["c14"][1] == "O" and c[V][1] == "P"]
    p(f"  Con la propuesta de la revisión n.º 6 (variante «{V}»), el ejercicio pasaría de OK a PENDIENTE en {len(sel)} candidatas "
      f"y de FALLO a PENDIENTE en {sum(1 for t, c in C if V in c and c['c14'][1] == 'F' and c[V][1] == 'P')}.")
    ok = [(t, c) for t, c in sel if ok6(c["c14"])]
    p(f"  De ellas, son OK en las seis dimensiones en C14: {len(ok)}. Por tabla y palabra ajena que dispararía la regla:")
    grp = collections.defaultdict(list)
    for t, c in ok:
        m = re.search(r"«([^»]*)»", c["d_" + V].get("ejercicio", ""))
        grp[(pg(t), m.group(1) if m else "?")].append((t, c))
    for (q, w), v in sorted(grp.items(), key=lambda z: -len(z[1])):
        t, c = v[0]
        p(f"    {len(v):3d} · {q} · bajo «{w}» · p. ej. l.{t['i'] + 1} «{t['tok']}» «{t['rot'][:40]}» declarado {c['anio']} · "
          f"cabecera inmediata: {t['g']['pila'][:2]} · lectura propia: {clase(t, c)}")
    p("  Las demás no son OK en C14 por otra dimensión. Por página (las 12 mayores): " +
      ", ".join(f"{q} ({n})" for q, n in collections.Counter(pg(t) for t, c in sel if not ok6(c["c14"])).most_common(12)))

    tabs = collections.defaultdict(list)
    for t in T:
        an = [x[1] for x in t["ej"]]
        if len(an) > len(set(an)):
            tabs[(pg(t), tuple(an), t["per"])].append(t)
    con = sorted(k for k in tabs if k[2])
    sinp = sorted(k for k in tabs if not k[2])
    p(f"\n  Cabeceras en las que el verificador reconoce algún ejercicio repetido: {len(tabs)} · con periodo (regla de grupos): {len(con)} · sin periodo: {len(sinp)}")
    p("  Con periodo:")
    for k in con:
        ts = tabs[k]
        per = collections.Counter(c["c14"][4] for t in ts for c in t["c"])
        pil = collections.Counter(" / ".join(t.get("g", {}).get("pila", [])[:2])[:40] for t in ts).most_common(2)
        p(f"    {k[0]} · ejercicios {list(k[1])} · {len(ts)} tokens · perímetro {dict(per)} · OK en seis dimensiones "
          f"{sum(1 for t in ts for c in t['c'] if ok6(c['c14']))} · cabeceras propias: {[x[0] for x in pil]}")
    p("  Sin periodo y con alguna candidata OK en las seis dimensiones (ejercicios · tokens · OK · cabeceras propias más frecuentes):")
    for k in sinp:
        ts = tabs[k]
        nok = sum(1 for t in ts for c in t["c"] if ok6(c["c14"]))
        if nok:
            pil = collections.Counter(" / ".join(t.get("g", {}).get("pila", [])[:2])[:34] for t in ts for c in t["c"] if ok6(c["c14"])).most_common(3)
            p(f"    {k[0]} · {list(k[1])} · {len(ts)} · {nok} · {[x[0] for x in pil]}")

    n_orden, despl, dist = 0, 0, collections.Counter()
    for t in T:
        s = t.get("asig")
        if not s or s[2] != "orden":
            continue
        n_orden += 1
        c_tok = (t["a0"] + t["a1"]) / 2
        dist["0–4" if s[4] < 5 else "5–9" if s[4] < 10 else "10–14"] += 1
        otras = [abs(c - c_tok) for c, y in t["ej"] if abs(c - s[3]) > 0.01]
        if otras and min(otras) < s[4] - 0.01:
            despl += 1
    p(f"\n  Tokens asignados por orden en C14: {n_orden} · distancia a su columna en caracteres: {dict(dist)} · "
      f"más cerca de otra columna de ejercicio que de la asignada (orden desplazado): {despl}")

    # ---------------------------------------------------------------- D
    p("\n\n== D. Decisión (b): lo que retiene la regla de grupos de columnas ==")
    V = "sin_grupos"
    sel = [(t, c) for t, c in C if V in c]
    p(f"  Sin la regla (variante «{V}») el perímetro pasaría de PENDIENTE a OK en {len(sel)} candidatas "
      f"({len({(t['doc'], t['p'], t['i'], t['idx']) for t, c in sel})} tokens); {sum(1 for t, c in sel if ok6(c[V]))} quedarían OK en las seis dimensiones.")
    grp = collections.defaultdict(list)
    for t, c in sel:
        m = re.search(r"la de «([^»]*)»", c["d14"]["perimetro"])
        grp[(pg(t), m.group(1) if m else "?")].append((t, c))
    for k, v in sorted(grp.items()):
        p(f"    {k[0]} · grupo «{k[1]}» · {len({(t['i'], t['idx']) for t, c in v})} tokens · quedarían OK en seis dimensiones: "
          f"{sum(1 for t, c in v if ok6(c[V]))} · eran OK en C13: {sum(1 for t, c in v if ok6(c['c13']))}")
    marca = sum(1 for t, c in sel if ok6(c[V]) and t["p"] in (317, 371))
    p(f"  Por clase de tabla: columnas por marca {marca} · honorarios por firma auditora {sum(1 for t, c in sel if ok6(c[V])) - marca} "
      f"(de estas, OK en C13: {sum(1 for t, c in sel if ok6(c[V]) and ok6(c['c13']) and t['p'] not in (317, 371))})")

    # ---------------------------------------------------------------- E
    p("\n\n== E. Decisión (c): umbral de alineación de 5,5 caracteres frente a 3 ==")
    V = "al3"
    sel = [(t, c) for t, c in C if V in c and c["c14"][1] == "F" and c[V][1] == "P"]
    p(f"  Con 3 (variante «{V}») pasarían de FALLO a PENDIENTE {len(sel)} candidatas ({len({(t['doc'], t['p'], t['i'], t['idx']) for t, c in sel})} tokens). "
      "Lectura propia de la cabecera inmediata y distancia que da el verificador:")
    for k, v in collections.Counter(clase(t, c) for t, c in sel).most_common():
        p(f"    {v:5d}  {k}")
    d = collections.Counter()
    for t, c in sel:
        m = re.search(r"\(([\d.]+) caracteres\)", c["d14"]["ejercicio"])
        d[(m.group(1) if m else "?", "otro ejercicio" if clase(t, c).startswith("fecha de OTRO") else "resto")] += 1
    p("    por distancia: " + ", ".join(f"{k[0]} → {k[1]}: {v}" for k, v in sorted(d.items())))
    otro = [(t, c) for t, c in sel if clase(t, c).startswith("fecha de OTRO")]
    p(f"    con la fecha de otro ejercicio encima ({len(otro)}), por página: " +
      ", ".join(f"{q} ({n})" for q, n in collections.Counter(pg(t) for t, c in otro).most_common()))
    al = [(t, c) for t, c in C if c["c14"][1] == "F" and "alineada con el token" in c["d14"]["ejercicio"]]
    p(f"\n  FALLO de ejercicio en C14 por la rama «columna de otro ejercicio alineada»: {len(al)} candidatas · lectura propia:")
    for k, v in collections.Counter(clase(t, c) for t, c in al).most_common():
        p(f"    {v:5d}  {k}")
    # distancia que mide el verificador cuando el número tiene encima solo una fecha «dd/mm/aaaa» y se le asigna esa columna
    import statistics
    med = collections.defaultdict(list)
    for t in T:
        s_, g = t.get("asig"), t.get("g")
        if not s_ or s_[0] != "ejercicio" or not g or not g["pila"] or not re.fullmatch(r"\d{1,2}/\d{1,2}/20\d\d", g["pila"][0]):
            continue
        r = lectura(t)
        if r and r[0] and not r[1] and str(r[0][0]) == s_[1]:
            med[t["a1"] - t["a0"]].append(s_[4])
    todas = sorted(d_ for v in med.values() for d_ in v)
    p(f"\n  Distancia que calcula el verificador (centro del número ↔ centro del año de su columna) en los {len(todas)} tokens que tienen encima solo")
    p(f"  una fecha «dd/mm/aaaa»: mediana {statistics.median(todas)} · percentil 99 {todas[int(0.99 * len(todas))]} · máximo {todas[-1]} · "
      f"a más de 3: {sum(1 for d_ in todas if d_ > 3)} · a más de 5,5: {sum(1 for d_ in todas if d_ > 5.5)}")
    p("  por ancho del número en caracteres (casos, mediana, máximo): " +
      ", ".join(f"{w}: {len(v)}, {statistics.median(v)}, {max(v)}" for w, v in sorted(med.items())))

    p("\n  Filas que llevan la fecha del saldo en su rótulo, declaradas con el ejercicio de esa fecha («January 1, Y» → Y − 1):")
    fs = [(t, c) for t, c in C if anio_de_fila(t) is not None and c["anio"] == anio_de_fila(t)]
    p(f"    {len(fs)} candidatas · ejercicio en C14: {dict(collections.Counter(c['c14'][1] for t, c in fs))} · en C13: {dict(collections.Counter(c['c13'][1] for t, c in fs))}")
    fal = [(t, c) for t, c in fs if c["c14"][1] == "F"]
    p(f"    en FALLO de ejercicio en C14: {len(fal)} · por página: " + ", ".join(f"{q} ({n})" for q, n in collections.Counter(pg(t) for t, c in fal).most_common()))
    p("    de ellas, en el estado de cambios en el patrimonio (rótulo con «31, AAAA» o «December 31, AAAA» y cifras en millones):")
    for t, c in fal:
        if re.search(r"(?i)^(?:31, 20\d\d|december 31, 20\d\d|january 1, 20\d\d)", t["rot"]) and t["c"][0]["c14"][3] == "O":
            m = re.search(r"\(([\d.]+) caracteres\)", c["d14"]["ejercicio"])
            p(f"      {ej(t, c)} · {c['d14']['ejercicio'][:70]}… · con umbral 3: {'PENDIENTE' if c.get(V, '')[1:2] == 'P' else 'FALLO'}")

    # ---------------------------------------------------------------- F
    p("\n\n== F. R2: el encabezado numerado ==")
    V = "sin_numerado"
    sel = [(t, c) for t, c in C if V in c and c["c14"][4] != c[V][4]]
    p(f"  Sin la regla (variante «{V}») el perímetro cambiaría en {len(sel)} candidatas: {dict(collections.Counter(c['c14'][4] + '→' + c[V][4] for t, c in sel))}")
    grp = collections.defaultdict(set)
    for t, c in sel:
        m = re.search(r"«([^»]*)»", c["d_" + V].get("perimetro", "") or c["d14"].get("perimetro", ""))
        grp[(pg(t), (t["tit"][1] or "")[:66], "página anterior" if (t["tit"][2] or 0) < 0 else "misma página", (m.group(1) if m else "?")[:28],
             c["c14"][4] + "→" + c[V][4])].add((t["i"], t["idx"]))
    for k, v in sorted(grp.items()):
        p(f"    {k[0]} · {len(v)} tokens · corta la línea «{k[1]}» ({k[2]}) · sin la regla, el título sería «{k[3]}» · {k[4]}")
    v14 = arnes7.Version(a.autor, a.raiz, "C14")
    m14 = v14.m
    sys.path.insert(0, a.pylibs)
    warnings.simplefilter("ignore")
    import pymupdf
    tot, falsos = collections.Counter(), []
    for doc in sorted(v14.fuentes):
        d_ = pymupdf.open(str(v14.pdf(doc)))
        idi = v14.fuentes[doc]["idioma"]
        for n in range(1, v14.paginas(doc) + 1):
            lineas = v14.lineas(doc, n)
            if not any(m14.GRUPO_RX.search(l) for l in [x for x in lineas if x.strip()][:8]):
                continue
            cand = [i for i, l in enumerate(lineas) if m14.es_encabezado_numerado(l.strip(), idi)]
            if not cand:
                continue
            filas = geo7.filas_de_pagina(geo7.palabras_de_pagina(d_[n - 1]))
            mapa = geo7.casar_lineas(lineas, filas)
            base = collections.Counter(round(w.cuerpo, 1) for f in filas for w in f["w"]).most_common(1)[0][0]
            for i in cand:
                if i not in mapa:
                    tot["sin lectura"] += 1
                    continue
                ws = filas[mapa[i]]["w"]
                if all(w.negrita for w in ws) or min(w.cuerpo for w in ws) > base + 0.6:
                    tot["título por tipografía"] += 1
                else:
                    tot["no es título por tipografía"] += 1
                    falsos.append(f"{doc} p.{n} l.{i + 1} «{re.sub(chr(32) + '{2,}', '  ', lineas[i].strip())[:74]}»")
    p(f"\n  Líneas de las páginas del grupo que es_encabezado_numerado toma por encabezado: {sum(tot.values())} · {dict(tot)}")
    p("  Las que no son título por tipografía (ni negrita ni cuerpo mayor que el del texto):")
    for x in falsos:
        p("    " + x)

    # ---------------------------------------------------------------- G
    p("\n\n== G. R4: título corto de tabla y columnas por país ==")
    V = "sin_corto"
    sel = [(t, c) for t, c in C if V in c and c["c14"][4] != c[V][4]]
    p(f"  Sin la regla del título corto (variante «{V}») el perímetro pasaría de PENDIENTE a OK en {len(sel)} candidatas "
      f"({len({(t['doc'], t['p'], t['i'], t['idx']) for t, c in sel})} tokens); quedarían OK en las seis dimensiones: {sum(1 for t, c in sel if ok6(c[V]))}")
    tit = collections.Counter(t["corto"] for t, c in sel)
    p("  Títulos que retienen (candidatas): " + ", ".join(f"«{k}» ({v})" for k, v in tit.most_common()))
    p("  No nombran un país ni un segmento según la lista propia: " + (", ".join(f"«{k}»" for k in tit if not RXP7.search(k or "")) or "ninguno"))
    paises = collections.defaultdict(list)
    for t in T:
        if t["c"][0]["c14"][4] != "O" or "g" not in t:
            continue
        cab = [x for x in t["g"]["pila"][:2] if tipo_celda(x) == "corta" and RXP7.fullmatch(x.strip())]
        if cab:
            paises[pg(t)].append((t, cab[0]))
    p(f"\n  Tokens con perímetro OK en C14 cuya cabecera inmediata es el nombre de un país (columna de un país): {sum(len(v) for v in paises.values())}")
    for q, v in sorted(paises.items()):
        t, cab = v[0]
        p(f"    {q}: {len(v)} tokens · países {sorted({c for _, c in v})[:10]} · OK en seis dimensiones "
          f"{sum(1 for t2, _ in v for c in t2['c'] if ok6(c['c14']))} · p. ej. l.{t['i'] + 1} «{t['tok']}» «{t['rot'][:30]}» · "
          f"ejercicio: {t['c'][0]['d14']['ejercicio'][:58]}")

    # ---------------------------------------------------------------- H
    p("\n\n== H. R5 y R1: filas con prefijo de UGE y filas de jurisdicción ==")
    uge = [t for t in T if re.match(r"(?i)^(?:CGU|UGT)\b", t["rot"])]
    p(f"  Tokens en filas cuyo rótulo empieza por «CGU» o «UGT»: {len(uge)} · perímetro en C14: {dict(collections.Counter(t['c'][0]['c14'][4] for t in uge))}")
    jur = [t for t in T if "jurisdicción" in t["c"][0]["d14"].get("perimetro", "")]
    p(f"  Tokens con FALLO de perímetro por la regla de jurisdicción: {len(jur)} · rótulos (unidos): " +
      "; ".join(sorted({f"{pg(t)} «{(t['rm'] or t['rot'])[:46]}»" for t in jur})))

    # ---------------------------------------------------------------- I
    p("\n\n== I. Líneas sin rótulo (la línea empieza por un número): fuera del universo del barrido de la revisión n.º 6 ==")
    sr = [t for t in T if not t["cr"]]
    p(f"  Tokens: {len(sr)} · candidatas OK en las seis dimensiones en C14: {sum(1 for t in sr for c in t['c'] if ok6(c['c14']))}")
    p("  Líneas sin rótulo con dos números o más y alguna candidata OK en las seis dimensiones, con la línea de arriba y la de abajo:")
    vistos = {}
    for t in sr:
        if t["n"] >= 2 and any(ok6(c["c14"]) for c in t["c"]):
            vistos.setdefault((t["doc"], t["p"], t["i"]), []).append(t)

    def corto(s):
        return re.sub(r"\s{2,}", "  ", s.strip())[:62]

    for (doc, n, i), ts in sorted(vistos.items()):
        L = v14.lineas(doc, n)
        oks = [f"«{t['tok']}» declarado {c['anio']}" for t in ts for c in t["c"] if ok6(c["c14"])]
        p(f"    {doc} p.{n} l.{i + 1}: «{corto(L[i])}» · arriba «{corto(L[i - 1]) if i else ''}» · abajo «{corto(L[i + 1]) if i + 1 < len(L) else ''}» · OK: {', '.join(oks)}")
    p("  Líneas de las páginas del grupo que empiezan por un solo dígito seguido de un rótulo (el número de capítulo del margen):")
    marg = collections.defaultdict(list)
    for t in sr:
        if re.fullmatch(r"\d", t["rot"]) and t["a0"] > 3:
            marg[(t["doc"], t["p"], t["i"])].append(t)
    n_seg = 0
    for (doc, n, i), ts in sorted(marg.items()):
        L = v14.lineas(doc, n)
        tr = m14.trozos(L[i])
        if len(tr) < 2 or re.fullmatch(r"[\d.,()% -]+", tr[1]):
            continue
        es_sub = bool(RXP7.search(tr[1]) or re.match(r"(?i)^(?:CGU|UGT)\b", tr[1]))
        n_seg += es_sub
        p(f"    {doc} p.{n} l.{i + 1}: «{corto(L[i])}» · perímetro C14 {ts[0]['c'][0]['c14'][4]} · OK en seis dimensiones: "
          f"{sum(1 for t in ts for c in t['c'] if ok6(c['c14']))}" + (" · ← rótulo de país, segmento o UGE" if es_sub else ""))
    p(f"  de ellas, con rótulo de país, segmento o UGE: {n_seg}")

    # ---------------------------------------------------------------- J
    p("\n\n== J. «La cabecera es la de la propia tabla»: líneas que C14 toma por cabecera de una tabla que empieza después ==")
    hs = collections.defaultdict(list)
    for t in T:
        if t["h"] is not None:
            hs[(t["doc"], t["p"], t["h"], t["lh"])].append(t)
    p(f"  Líneas: {len(hs)} · tokens bajo ellas: {sum(len(v) for v in hs.values())} · estado de la fila C13 → C14 de esos tokens: "
      f"{dict(collections.Counter(fila(c['c13']) + '→' + fila(c['c14']) for v in hs.values() for t in v for c in t['c']))}")
    for (doc, n, h, lh), v in sorted(hs.items()):
        resto = re.sub(r"\d{1,2}/\d{1,2}/20\d\d|20\d\d|(?i:\((?:in|en) millions? (?:of euros|d'euros)\))", " ", lh)
        pal = [w for w in re.findall(r"[^\W\d_]{2,}", resto) if not CAL.match(w)]
        p(f"    {doc} p.{n} l.{h + 1} «{re.sub(chr(32) + '{2,}', '  ', lh)[:70]}» · {len(v)} tokens · {'PROSA' if len(pal) >= 3 else 'cabecera de fechas'} · "
          f"OK en seis dimensiones C13 {sum(1 for t in v for c in t['c'] if ok6(c['c13']))} → C14 {sum(1 for t in v for c in t['c'] if ok6(c['c14']))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
