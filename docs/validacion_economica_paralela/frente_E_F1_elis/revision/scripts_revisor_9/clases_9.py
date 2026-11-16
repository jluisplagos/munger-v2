"""Revisión independiente n.º 9 · clases del barrido propio C16 → C18 (frente E · F1 · Elis). No modifica nada del autor.

Lee el JSONL de barrido_9.py y escribe por la salida estándar, por secciones:

  A  universo, controles y transiciones del estado de la fila, con la causa de cada cambio;
  B  T1: líneas en que la regla de la fecha del rótulo da un ejercicio en C18, sus columnas de datos, y las candidatas
     que quedan OK en las seis dimensiones con el ejercicio dado por esa regla;
  C  T2: dónde da ejercicio la regla en C16 y en C18; clasificación PROPIA de todas las líneas con una fecha completa en
     el rótulo (expresión propia, unión propia de las líneas de encima), por las palabras que acompañan a la fecha;
  D  T3: líneas en que la unión con `fecha` añade líneas, y las que toman la fecha de una línea de encima;
  E  regla nueva de f12f8ea (`token_del_rotulo`): todos los tokens que retira, por forma del rótulo;
  F  T4: tokens en que `cabecera_de_paises` cambia;
  G  T5: líneas en que `rotulos_sin_rotulo` cambia, por causa, y lo que se deja de detectar;
  H  T6: líneas en que `es_encabezado_numerado` cambia (con y sin la línea de debajo) y sus efectos;
  I  la pestaña del margen derecho y otras comprobaciones puntuales.

Uso: python3 -I -B clases_9.py --todas <jsonl.gz> --raiz <munger_v2_r1> --c16 <frente C17> --c18 <frente C19>
"""
import argparse
import gzip
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import arnes9 as H  # noqa: E402

# expresión propia de una fecha completa de apertura o de cierre (no es la del autor): día/mes/año con barras, mes y día
# en inglés en cualquier orden y con o sin coma, y día y mes en francés
FECHA9 = re.compile(r"(?i)\b\d{1,2}/\d{1,2}/20\d\d\b|\b(?:january|december)\s*,?\s*\d{1,2}\s*,?\s*20\d\d|"
                    r"\b\d{1,2}(?:er)?\s+(?:janvier|d[ée]cembre)\s+20\d\d")
ANIO9 = re.compile(r"^\(?20\d\d[,)]?$")
PIE9 = re.compile(r"Universal Registration Document|enregistrement universel")


def p(*x):
    print(" ".join(str(v) for v in x))


def corta(s, n=150):
    s = re.sub(r"\s{2,}", "  ", s.strip())
    return s if len(s) <= n else s[:n - 1] + "…"


def donde(r):
    return f"{r['doc']} p.{r['p']} l.{r['i'] + 1}"


def firma(rotulo_unido):
    """Palabras del rótulo que acompañan a la fecha, en minúsculas y sin puntuación, con las llamadas quitadas."""
    t = FECHA9.sub(" ", rotulo_unido)
    t = re.sub(r"\(\w\)|\*+|[(),:;›–—−-]", " ", t)
    return " ".join(w.lower() for w in t.split()) or "(solo la fecha)"


def union_propia(lineas, i, rot):
    """Rótulo de la línea i unido, a mi manera, con hasta tres líneas de encima de una sola celda (60 caracteres o menos),
    sin exigir la misma sangría: más ancho que el del autor."""
    partes, k = [rot], i - 1
    while k >= 0 and len(partes) <= 3:
        l = lineas[k]
        if not l.strip() or len(re.split(r"\s{2,}", l.strip())) != 1 or len(l.strip()) > 60:
            break
        partes.insert(0, l.strip())
        k -= 1
    return partes


def causa(x, g, r):
    """Causa del cambio de una candidata entre C16 y C18, por la dimensión que cambia y el motivo de cada versión."""
    da, dn = g.get("da", {}), g.get("dn", {})
    cambios = [d for d, ca, cn in zip(H.DIMS, g["a"], g["n"]) if ca != cn]
    out = []
    for d in cambios:
        ea, en = da.get(d, ""), dn.get(d, "")
        if d == "columna":
            out.append("T1 columna PENDIENTE con la fecha en el rótulo" if "fecha del rótulo" in en else
                       ("T2/T1 la regla ya no da el ejercicio (columna vuelve a NO_APLICA)" if "fecha del rótulo" not in en and r["ar_a"] is not None
                        else "columna: otra"))
        elif d == "ejercicio":
            if "no una cifra" in en:
                out.append("f12f8ea token del rótulo (año o día)")
            elif "fecha en" in ea and "fecha en" not in en:
                out.append("T2 la regla deja de dar el ejercicio")
            elif "fecha en" in en and "fecha en" not in ea:
                out.append("T3 la regla da el ejercicio por primera vez")
            elif "fecha en" in ea and "fecha en" in en:
                out.append("ejercicio: la regla da otro año")
            else:
                out.append("ejercicio: otra (zona de cabecera)")
        elif d == "perimetro":
            if "columna por país" in en and "columna por país" not in ea:
                out.append("T4 cabecera por países")
            elif r["rsr_a"] != r["rsr_n"]:
                out.append("T5 rótulos contiguos")
            else:
                out.append("perímetro: otra (T6, título o encabezado)")
        elif d == "edicion":
            out.append("edición: otra (zona de cabecera)")
        else:
            out.append(d + ": otra")
    return " + ".join(sorted(set(out)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--todas", required=True, type=Path)
    ap.add_argument("--raiz", required=True, type=Path)
    ap.add_argument("--c16", required=True, type=Path)
    ap.add_argument("--c18", required=True, type=Path)
    a = ap.parse_args()
    A, N = H.Version("C16", a.c16, a.raiz), H.Version("C18", a.c18, a.raiz)
    V = N.V
    with gzip.open(a.todas, "rt", encoding="utf-8") as f:
        R = [json.loads(l) for l in f]
    pag = {}

    def lineas(doc, n):
        if (doc, n) not in pag:
            pag[(doc, n)] = N.lineas(doc, n)
        return pag[(doc, n)]

    p("Clases del barrido propio de la revisión n.º 9 · C16 → C18")
    p()
    # ------------------------------------------------------------------ A
    p("== A. Universo, controles y transiciones ==")
    con = [r for r in R if r["toks"]]
    ntok = sum(len(r["toks"]) for r in con)
    p(f"  registros: {len(R)}; líneas con cifras: {len(con)}; tokens: {ntok} ({sum(len(r['toks']) for r in con if r['g'])} en páginas del grupo); "
      f"candidatas: {ntok * 3}")
    for k, nombre in enumerate(("es_titulo", "rotulo_multilinea sin fecha", "rotulo", "tokens_numericos")):
        p(f"  control «{nombre}»: distinto en {sum(1 for r in R if not r['ctl'][k])} de {len(R)} líneas")
    trans, por_causa, ej_trans = Counter(), defaultdict(Counter), Counter()
    ejemplos = defaultdict(list)
    for r in con:
        for x in r["toks"]:
            for y, g in x["G"].items():
                ea, en = H.estado(g["a"]), H.estado(g["n"])
                trans[(ea, en)] += 1
                if g["a"] != g["n"]:
                    c = causa(x, g, r)
                    por_causa[(ea, en)][c] += 1
                    if len(ejemplos[(ea, en, c)]) < 3:
                        ejemplos[(ea, en, c)].append(f"{donde(r)} «{x['tok']}» {y}: {g['a']}→{g['n']} · «{corta(r['l'], 90)}»")
                    if g["a"][1] != g["n"][1]:
                        ej_trans[(g["a"][1], g["n"][1])] += 1
    for (ea, en), c in sorted(trans.items()):
        p(f"  {ea:9} → {en:9} {c:7}")
        for causa_, cc in sorted(por_causa[(ea, en)].items(), key=lambda z: -z[1]):
            p(f"       {cc:6}  {causa_}")
            if ea != en:
                for e in ejemplos[(ea, en, causa_)][:2]:
                    p(f"               p. ej. {e}")
    p(f"  OK en las seis dimensiones: C16 {sum(c for (ea, _), c in trans.items() if ea == 'OK')} · C18 {sum(c for (_, en), c in trans.items() if en == 'OK')}")
    p(f"  cambios de la dimensión «ejercicio» (C16 → C18): {dict(sorted(ej_trans.items()))}")
    p()
    # ------------------------------------------------------------------ B
    p("== B. T1 · la regla de la fecha del rótulo en C18 y la dimensión «columna» ==")
    regla = [r for r in R if r["ar_n"] is not None]
    p(f"  líneas en que la regla da un ejercicio en C18: {len(regla)} ({sum(1 for r in regla if r['g'])} en páginas del grupo); por publicación: "
      f"{dict(sorted(Counter(r['doc'] for r in regla).items()))}")
    p(f"  por columnas de datos de la fila: {dict(sorted(Counter(r['ncol'] for r in regla).items()))}")
    p(f"  por unidad declarada por encima: {dict(Counter(str((r.get('ud') or [None])[0]) for r in regla))}")
    ok_regla, ok_otros_a = [], 0
    for r in con:
        for x in r["toks"]:
            for y, g in x["G"].items():
                if H.estado(g["n"]) == "OK" and "fecha en el rótulo" in g.get("dn", {}).get("ejercicio", ""):
                    ok_regla.append((r, x, y, g))
                if H.estado(g["a"]) == "OK" and "fecha en el rótulo" in g.get("da", {}).get("ejercicio", ""):
                    ok_otros_a += 1
    p(f"  candidatas OK en las seis dimensiones con el ejercicio dado por la regla: C16 {ok_otros_a} · C18 {len(ok_regla)}")
    p(f"    en C18, por estado de «columna»: {dict(Counter(g['n'][2] for _, _, _, g in ok_regla))}; por columnas de datos de la fila: "
      f"{dict(Counter(r['ncol'] for r, _, _, _ in ok_regla))}")
    for r, x, y, g in ok_regla:
        p(f"    {donde(r)} · «{x['tok']}» declarado {y} ({g['n']}) · «{corta(r['l'], 100)}»")
    p("  clasificación propia de esas líneas (por la unidad declarada, las cifras a la derecha y la línea de rótulo que queda encima sin unir):")
    PLAN9 = re.compile(r"(?i)number of|nombre de|rights|droits|of which|dont")

    def clase_regla(r):
        ud = (r.get("ud") or [None])[0]
        encima = r["pf"][:-1] if r["rds"] == r["rot"] and len(r["pf"]) > 1 else []
        if r["ncol"] == 0:
            return "línea sin cifras a la derecha del rótulo (cabeceras con fecha; una fila con todas las cifras con llamada)"
        if encima and PLAN9.search(" ".join(encima)):
            return "recuento de un plan de acciones con el rótulo partido antes de «as at» o «au»"
        if ud and ud.startswith("otra unidad"):
            return "tabla del capital social (número de acciones, nominal y capital en euros), fuera de las páginas del grupo"
        if ud == "miles EUR":
            return "saldo en miles de euros (cuentas de la sociedad dominante)"
        if ud == "mm EUR":
            return "saldo en millones de euros, página del grupo" if r["g"] else "saldo en millones de euros, cuentas de la sociedad dominante"
        datos = [x["tok"] for x in r["toks"] if x["arp"] is not None]
        if r["ncol"] == 1 and len(datos) == 1 and re.fullmatch(r"\d{3}", datos[0]):
            return "entrada de sumario: la cifra es el número de página"
        return "saldo en una página en la que no se localiza la declaración de unidades"
    cl = defaultdict(list)
    for r in regla:
        cl[clase_regla(r)].append(r)
    for k, v in sorted(cl.items(), key=lambda z: -len(z[1])):
        cols = Counter(r["ncol"] for r in v)
        p(f"    {len(v):4}  {k} · columnas de datos: {dict(sorted(cols.items()))}")
        if not k.startswith("saldo en millones de euros, página del grupo") and not k.startswith("línea sin cifras"):
            for r in v:
                encima = r["pf"][:-1] if r["rds"] == r["rot"] and len(r["pf"]) > 1 else []
                p(f"            {donde(r)} · «{corta(r['l'], 85)}»" + (f" · encima, sin unir: {encima}" if encima else ""))
    p("  líneas con la regla y UNA sola columna de datos (la columna queda NO_APLICA), con las líneas de su tabla:")
    for r in regla:
        if r["ncol"] != 1:
            continue
        L = lineas(r["doc"], r["p"])
        # tabla: de la declaración de unidades de encima (o diez líneas) a la primera línea en blanco tras la fila
        j = (r.get("ud") or [None, None])[1]
        ini = j if j is not None and r["i"] - j <= 25 else max(0, r["i"] - 10)
        fin = r["i"]
        while fin + 1 < len(L) and L[fin + 1].strip():
            fin += 1
        maxcol = max((V.columnas_de_datos(L[k], N.idioma(r["doc"])) for k in range(ini, fin + 1)), default=0)
        cab = corta(L[ini], 110) if j is not None else "(sin declaración de unidades)"
        p(f"    {donde(r)} g={r['g']} · {r['ar_n']} · «{corta(r['l'], 80)}» · máx. de columnas de datos en las líneas {ini + 1}–{fin + 1}: {maxcol} · cabecera: «{cab}»")
    p()
    # ------------------------------------------------------------------ C
    p("== C. T2 · dónde da ejercicio la regla, en C16 y en C18, y clasificación propia de las líneas con fecha ==")
    cmp_ = Counter()
    for r in R:
        if r["ar_a"] is None and r["ar_n"] is None:
            continue
        if r["ar_a"] is not None and r["ar_n"] is not None:
            cmp_["las dos, mismo ejercicio" if r["ar_a"] == r["ar_n"] else "las dos, otro ejercicio"] += 1
        elif r["ar_a"] is not None:
            cmp_["solo C16, una celda" if r["nc"] < 2 else ("solo C16, dos celdas o más, 0–1 tokens" if r["nt"] <= 1 else "solo C16, dos celdas o más, 2+ tokens")] += 1
        else:
            cmp_["solo C18"] += 1
    p(f"  {dict(sorted(cmp_.items()))}")
    p("  solo C18:")
    for r in R:
        if r["ar_a"] is None and r["ar_n"] is not None:
            p(f"    {donde(r)} · {r['ar_n']} · {r['ncol']} columnas · «{r['rds']}»")
    p("  solo C16, dos celdas o más y 2+ tokens (lo que C18 deja fuera con cifras a la derecha):")
    for r in R:
        if r["ar_a"] is not None and r["ar_n"] is None and r["nc"] >= 2 and r["nt"] >= 2:
            p(f"    {donde(r)} g={r['g']} · {r['ar_a']} · unidad {(r.get('ud') or [None])[0]} · «{corta(r['l'], 120)}»")
    # clasificación propia
    p("  -- clasificación propia: líneas cuyo rótulo (unido a mi manera) lleva una fecha completa y que tienen alguna cifra a su derecha --")
    cls = defaultdict(lambda: {"n": 0, "regla": 0, "tok": 0, "ud": Counter(), "ej": [], "grupo": 0})
    una_celda = []
    for r in con:
        L = lineas(r["doc"], r["p"])
        rot = r["rot"]
        fin_rot = r["l"].find(rot) + len(rot) if rot else 0
        datos = [x for x in r["toks"] if x["a0"] >= fin_rot and not ANIO9.match(x["tok"])]
        partes = union_propia(L, r["i"], rot)
        # la unión más corta, de abajo arriba, que lleva la fecha
        unido = None
        for n_ in range(1, len(partes) + 1):
            t = " ".join(partes[-n_:])
            if FECHA9.search(t):
                unido = t
                break
        if unido is None:
            continue
        if not datos:
            dentro = [x for x in r["toks"] if x["a0"] < fin_rot and not ANIO9.match(x["tok"]) and not re.fullmatch(r"\d{1,2},?", x["tok"])]
            if r["nc"] == 1 and dentro and FECHA9.search(rot):
                una_celda.append((r, dentro))
            continue
        f_ = firma(unido)
        c = cls[f_]
        c["n"] += 1
        c["regla"] += r["ar_n"] is not None
        c["tok"] += len(datos)
        c["grupo"] += r["g"]
        c["ud"][str((r.get("ud") or [None])[0])] += 1
        if len(c["ej"]) < 2:
            c["ej"].append(f"{donde(r)} «{corta(r['l'], 70)}»")
    tot = sum(c["n"] for c in cls.values())
    p(f"  líneas: {tot}; con la regla de C18: {sum(c['regla'] for c in cls.values())}; sin ella: {tot - sum(c['regla'] for c in cls.values())}; firmas distintas: {len(cls)}")
    p("  firma (palabras que acompañan a la fecha) · líneas · con la regla · en páginas del grupo · unidad declarada · ejemplos")
    for f_, c in sorted(cls.items(), key=lambda z: (-(z[1]["regla"] > 0), -z[1]["n"], z[0])):
        p(f"    [{'regla' if c['regla'] == c['n'] else ('NO' if c['regla'] == 0 else 'MIXTA ' + str(c['regla']))}] «{f_}» · {c['n']} · {c['regla']} · g {c['grupo']} · "
          f"{dict(c['ud'])} · {' | '.join(c['ej'])}")
    p("  las de firma «(solo la fecha)» con la regla (mi unión se queda en la línea de la fecha; la del autor sube hasta la fórmula del saldo):")
    for r in con:
        if r["ar_n"] is not None and r["toks"] and not V.SALDO_EN_ROTULO.search(r["rot"]) and FECHA9.search(r["rot"]):
            p(f"    {donde(r)} · {r['ar_n']} · rótulo del autor «{r['rds']}» · «{corta(r['l'], 80)}»")
    p(f"  líneas de UNA sola celda con fecha en el rótulo y alguna cifra pegada a él que no es el día ni el año: {len(una_celda)}")
    for r, dentro in una_celda[:40]:
        p(f"    {donde(r)} g={r['g']} · {[x['tok'] for x in dentro]} · «{corta(r['l'], 120)}»")
    p()
    # ------------------------------------------------------------------ D
    p("== D. T3 · la unión con `fecha` ==")
    dif = [r for r in R if r["pf"] != r["pnf"]]
    p(f"  líneas en que partes_de_rotulo con `fecha` difiere de la versión sin `fecha`: {len(dif)}; con la regla: {sum(1 for r in dif if r['ar_n'] is not None)}")
    p(f"    con `fecha` se unen MÁS líneas: {sum(1 for r in dif if len(r['pf']) > len(r['pnf']))}; MENOS (la línea en minúscula bajo una fila de datos): "
      f"{sum(1 for r in dif if len(r['pf']) < len(r['pnf']))}")
    p("  las que tienen la regla:")
    for r in dif:
        if r["ar_n"] is not None:
            p(f"    {donde(r)} · {r['ar_n']} · con fecha {r['pf']} · sin fecha {r['pnf']}")
    p("  las que unen MENOS líneas (regla de la línea en minúscula) y tienen cifras:")
    for r in dif:
        if len(r["pf"]) < len(r["pnf"]) and r["toks"]:
            p(f"    {donde(r)} g={r['g']} · C16 daba {r['ar_a']} · sin fecha {r['pnf']} · con fecha {r['pf']} · «{corta(r['l'], 90)}»")
    p("  las que unen MÁS líneas y NO tienen la regla, por lo que se une (primeras 25 de cada clase):")
    clases_d = defaultdict(list)
    for r in dif:
        if len(r["pf"]) > len(r["pnf"]) and r["ar_n"] is None:
            extra = r["pf"][:len(r["pf"]) - len(r["pnf"])]
            clases_d["la línea unida lleva una fecha completa" if FECHA9.search(" ".join(r["pf"])) else "sin fecha completa"].append((r, extra))
    for k, v in clases_d.items():
        p(f"    {k}: {len(v)}")
        for r, extra in v[:25]:
            p(f"      {donde(r)} g={r['g']} nt={r['nt']} · unidas de más {extra} · rótulo «{corta(r['rot'], 60)}»")
    unidas = [r for r in regla if not V.FECHA_DE_SALDO.search(r["rot"])]
    p(f"  líneas con la regla cuya fecha NO está entera en su propio rótulo: {len(unidas)}")
    for r in unidas:
        L = lineas(r["doc"], r["p"])
        k = r["i"] - (len(r["rds"].split()) and 1)
        # la línea no vacía que queda por encima de las partes unidas
        n_unidas = 0
        for n_ in range(1, len(r["pf"]) + 1):
            if " ".join(r["pf"][-n_:]) == r["rds"]:
                n_unidas = n_ - 1
                break
        enc = L[r["i"] - n_unidas - 1] if r["i"] - n_unidas - 1 >= 0 else ""
        p(f"    {donde(r)} · {r['ar_n']} · «{r['rds']}» · {r['ncol']} columnas · línea de encima de lo unido: «{corta(enc, 70)}»")
    p()
    # ------------------------------------------------------------------ E
    p("== E. Regla de f12f8ea · tokens que `token_del_rotulo` retira (todas las páginas) ==")
    tdr = [(r, x) for r in con for x in r["toks"] if x["tdr"]]
    p(f"  tokens: {len(tdr)} en {len({(r['doc'], r['p'], r['i']) for r, _ in tdr})} líneas; por motivo: {dict(Counter(x['tdr'] for _, x in tdr))}")
    forma = Counter()
    raros = []
    perdidas = Counter()
    for r, x in tdr:
        rot, tok = r["rot"], x["tok"]
        ini = r["l"].find(rot)
        antes, despues = r["l"][ini:x["a0"]], r["l"][x["a1"]:ini + len(rot)]
        if "día" in x["tdr"]:
            f_ = "día: «" + corta(re.sub(r"20\d\d", "AAAA", rot), 60) + "»"
        elif PIE9.search(rot):
            f_ = "año del pie de página"
        elif FECHA9.search(rot) or re.search(r"(?i)(?:january|february|march|april|may|june|july|august|september|october|november|december|janvier|février|mars|avril|mai|juin|"
                                             r"juillet|août|septembre|octobre|novembre|décembre)\s*,?\s*(?:\d{1,2},?\s*)?$", antes):
            f_ = "año de una fecha del rótulo"
        elif despues.strip():
            f_ = "año en medio del rótulo (le siguen palabras)"
        else:
            f_ = "año al final del rótulo, sin fecha"
            raros.append((r, x))
        forma[f_] += 1
        for y, g in x["G"].items():
            if H.estado(g["a"]) == "OK":
                perdidas[f_] += 1
    for f_, c in sorted(forma.items(), key=lambda z: -z[1]):
        p(f"    {c:5}  {f_}  (candidatas que eran OK en C16: {perdidas[f_]})")
    p(f"  «año al final del rótulo, sin fecha»: rótulos distintos (con el año como AAAA) y recuento; son los que podrían ser una cifra pegada al rótulo")
    for rot_, c in sorted(Counter(corta(re.sub(r"20\d\d", "AAAA", r["rot"]), 70) for r, _ in raros).items(), key=lambda z: -z[1])[:80]:
        p(f"    {c:4}  «{rot_}»")
    # ¿hay tokens en el rótulo con forma de año cuyo valor NO es un año plausible de estas publicaciones?
    fuera = [(r, x) for r, x in tdr if re.fullmatch(r"20\d\d,?", x["tok"]) and not 2010 <= int(x["tok"][:4]) <= 2035]
    p(f"  tokens retirados con forma de año fuera de 2010–2035: {len(fuera)}")
    for r, x in fuera[:30]:
        p(f"    {donde(r)} «{x['tok']}» · «{corta(r['l'], 110)}»")
    p()
    # ------------------------------------------------------------------ F
    p("== F. T4 · `cabecera_de_paises` de C16 y de C18 ==")
    cpd = [(r, x) for r in con for x in r["toks"] if x.get("cp") and x["cp"][0] != x["cp"][1]]
    por_l = Counter((r["doc"], r["p"], r["i"]) for r, _ in cpd)
    p(f"  tokens en que cambia: {len(cpd)}, en {len(por_l)} líneas; tokens con cabecera de países: C16 {sum(1 for r in con for x in r['toks'] if x.get('cp') and x['cp'][0])} · "
      f"C18 {sum(1 for r in con for x in r['toks'] if x.get('cp') and x['cp'][1])}")
    vistos = set()
    for r, x in cpd:
        if (r["doc"], r["p"], r["i"]) in vistos:
            continue
        vistos.add((r["doc"], r["p"], r["i"]))
        p(f"    {donde(r)} g={r['g']} · {por_l[(r['doc'], r['p'], r['i'])]} tokens · C16 {x['cp'][0]} → C18 {x['cp'][1]} · «{corta(r['l'], 90)}»")
    p()
    # ------------------------------------------------------------------ G
    p("== G. T5 · `rotulos_sin_rotulo` de C16 y de C18 ==")
    con_a = [r for r in R if r["rsr_a"]]
    con_n = [r for r in R if r["rsr_n"]]
    p(f"  líneas con algún rótulo contiguo: C16 {len(con_a)} ({sum(1 for r in con_a if r['g'])} en páginas del grupo) · C18 {len(con_n)} ({sum(1 for r in con_n if r['g'])})")
    p(f"  de ellas, líneas con algún token numérico: C16 {sum(1 for r in con_a if r['toks'])} ({sum(1 for r in con_a if r['toks'] and r['g'])} en páginas del grupo) · "
      f"C18 {sum(1 for r in con_n if r['toks'])} ({sum(1 for r in con_n if r['toks'] and r['g'])})")
    seg_cambios = Counter()
    seg_lineas = set()
    for r in con:
        for x in r["toks"]:
            for seg_, v in (x.get("S") or {}).items():
                if v[0] != v[1]:
                    seg_cambios[(seg_, v[0], v[1])] += 1
                    seg_lineas.add(donde(r) + " «" + corta(r["l"], 60) + "»")
    p(f"  perímetro declarado de un segmento: tokens cuyo estado cambia entre C16 y C18: {dict(seg_cambios)} · líneas: {sorted(seg_lineas)}")
    per_grupo = Counter()
    for r in con:
        if r["rsr_a"] != r["rsr_n"]:
            for x in r["toks"]:
                for g in x["G"].values():
                    if g["a"][4] != g["n"][4]:
                        per_grupo[(donde(r), g["a"][4], g["n"][4])] += 1
    p(f"  perímetro del grupo: candidatas que cambian en las líneas en que cambia la función: {dict(per_grupo)}")
    cambia = [r for r in R if r["rsr_a"] != r["rsr_n"]]
    motivos = Counter()
    perdidos = []
    for r in cambia:
        L, idi = lineas(r["doc"], r["p"]), N.idioma(r["doc"])
        t = V.trozos(r["l"])
        if re.fullmatch(r"\d", t[0]):
            m = "la línea empieza por un dígito suelto (pestaña)"
        elif t[0].split(" ")[0] in V.PLACEHOLDER and len(t[0].split(" ")) > 1:
            m = "rótulo con viñeta"
        else:
            largo = sang = False
            for paso in (-1, 1):
                k, n_ = r["i"] + paso, 0
                while 0 <= k < len(L) and n_ < 3:
                    l = L[k]
                    if not l.strip() or V.tokens_numericos(l, idi) or len(V.trozos(l)) != 1:
                        break
                    largo |= len(l.strip()) > 45
                    sang |= H.sangria(l) > 12
                    if len(l.strip()) > 45 or H.sangria(l) > 12:
                        break
                    k += paso
                    n_ += 1
            m = "línea contigua de más de 45 caracteres" if largo and not sang else ("línea contigua con más de 12 de sangría" if sang and not largo else "las dos (larga y sangrada)")
        motivos[(m, r["g"])] += 1
        nombra = [x for x in r["rsr_a"] if x not in r["rsr_n"] and (V.ROTULOS_SEGMENTO_NORM.get(V.normalizar_rotulo(x)) or V.PAISES.match(V.sin_prefijo_uge(x))
                                                                    or V.JURISDICCION.search(x) or V.DESGLOSE_PAIS.search(x))]
        if nombra:
            perdidos.append((r, m, nombra))
    p(f"  líneas en que cambia: {len(cambia)}; por causa y tipo de página (1 = grupo):")
    for (m, g), c in sorted(motivos.items(), key=lambda z: -z[1]):
        p(f"    {c:5}  g={g}  {m}")
    p(f"  rótulos contiguos que C16 daba, C18 no, y que nombran un segmento, un país o una jurisdicción: {len(perdidos)} líneas")
    for r, m, nombra in perdidos:
        seg = {s: v[:2] for x in r["toks"] for s, v in (x.get("S") or {}).items()}
        gper = Counter((g["a"][4], g["n"][4]) for x in r["toks"] for g in x["G"].values())
        p(f"    {donde(r)} g={r['g']} nt={r['nt']} · {m} · {nombra[:2]} · perímetro del grupo C16→C18 {dict(gper)} · segmentos que cambian {seg} · «{corta(r['l'], 70)}»")
    solo_n = [r for r in R if r["rsr_n"] and r["rsr_a"] != r["rsr_n"]]
    p(f"  líneas con rótulos contiguos en C18 distintos de los de C16: {len(solo_n)}")
    p("  líneas con rótulos contiguos en C18, en páginas del grupo:")
    for r in con_n:
        if r["g"]:
            p(f"    {donde(r)} nt={r['nt']} · {r['rsr_n'][:3]} · «{corta(r['l'], 80)}»")
    # líneas cuya primera celda es un dígito suelto: ¿la pestaña del capítulo o la primera cifra de una fila sin rótulo?
    digito = [r for r in con if re.fullmatch(r"\d", V.trozos(r["l"])[0]) and V.es_numero(V.trozos(r["l"])[0], N.idioma(r["doc"]))]
    solo_cifras, con_texto = [], []
    for r in digito:
        t, idi = V.trozos(r["l"]), N.idioma(r["doc"])
        if len(t) < 2 or not V.es_numero(t[1].split(" ")[0], idi):
            continue
        (solo_cifras if all(V.es_numero(c, idi) or re.fullmatch(r"\(\w\)", c) for c in t[1:]) else con_texto).append(r)
    p(f"  líneas cuyo primer trozo es un dígito suelto: {len(digito)}; de ellas, con rótulos contiguos en C16: {sum(1 for r in digito if r['rsr_a'])}")
    p(f"  de ellas, con una segunda celda que empieza por un número: {len(solo_cifras) + len(con_texto)}: {len(con_texto)} llevan texto en esa celda o en otra (la pestaña ante una "
      f"dirección, un título numerado o prosa) y {len(solo_cifras)} están hechas solo de cifras y llamadas ({sum(r['g'] for r in solo_cifras)} en páginas del grupo; "
      f"{sum(1 for r in solo_cifras if r['rsr_a'])} con rótulos contiguos en C16):")
    for r in solo_cifras:
        p(f"    {donde(r)} g={r['g']} · «{corta(r['l'], 60)}» · rótulos contiguos en C16: {r['rsr_a'][:2]}")
    p()
    # ------------------------------------------------------------------ H
    p("== H. T6 · `es_encabezado_numerado`: C16, C18 con la línea de debajo y C18 sin ella ==")
    tot = Counter()
    for r in R:
        for k, nombre in enumerate(("C16", "C18 con la línea de debajo", "C18 sin ella")):
            tot[(nombre, r["g"])] += r["enc"][k]
    for nombre in ("C16", "C18 con la línea de debajo", "C18 sin ella"):
        p(f"  {nombre}: {tot[(nombre, 1)]} en páginas del grupo y {tot[(nombre, 0)]} en las demás")
    for titulo, sel in (("dejan de ser encabezado (C16 sí, C18 con la línea de debajo no)", lambda e: e[0] and not e[1]),
                        ("pasan a ser encabezado (C16 no, C18 con la línea de debajo sí)", lambda e: not e[0] and e[1]),
                        ("solo con la línea de debajo (C18 sin ella no, con ella sí)", lambda e: e[1] and not e[2]),
                        ("solo sin la línea de debajo (C18 sin ella sí, con ella no)", lambda e: e[2] and not e[1])):
        sel_ = [r for r in R if sel(r["enc"])]
        p(f"  {titulo}: {len(sel_)}")
        for r in sel_:
            L = lineas(r["doc"], r["p"])
            deb = L[r["i"] + 1] if r["i"] + 1 < len(L) else ""
            p(f"    {donde(r)} g={r['g']} · «{corta(r['l'], 95)}» / debajo «{corta(deb, 50)}»")
    zonas = [r for r in con if "zona" in r]
    tpes = [r for r in con if "tpe" in r]
    p(f"  líneas con cifras cuya zona de cabecera cambia: {len(zonas)} ({sum(1 for r in zonas if r['g'])} en páginas del grupo); cuyo título de país encima cambia: {len(tpes)}")
    for r in zonas:
        cam = Counter((g["a"], g["n"]) for x in r["toks"] for g in x["G"].values() if g["a"] != g["n"])
        p(f"    zona · {donde(r)} g={r['g']} nt={r['nt']} · C16 {r['zona'][0]} → C18 {r['zona'][1]} · candidatas que cambian: {dict(cam)} · «{corta(r['l'], 70)}»")
    for r in tpes:
        cam = Counter((g["a"][4], g["n"][4]) for x in r["toks"] for g in x["G"].values())
        p(f"    título · {donde(r)} g={r['g']} nt={r['nt']} · C16 {r['tpe'][0]!r} → C18 {r['tpe'][1]!r} · perímetro {dict(cam)} · «{corta(r['l'], 70)}»")
    p()
    # ------------------------------------------------------------------ I
    p("== I. Comprobaciones puntuales ==")
    # pestaña del margen derecho: último token de un dígito suelto, muy separado, en una línea con la regla
    der = []
    for r in regla:
        if not r["toks"]:
            continue
        x = r["toks"][-1]
        if re.fullmatch(r"\d", x["tok"]) and x["arp"] is not None:
            der.append((r, x))
    p(f"  líneas con la regla cuyo último token es un dígito suelto que toma el ejercicio (posible pestaña del margen derecho): {len(der)}")
    for r, x in der:
        p(f"    {donde(r)} · {r['ncol']} columnas · «{corta(r['l'], 120)}»")
    # tokens a la derecha del rótulo que toman el ejercicio y son años
    anios_der = [(r, x) for r in regla for x in r["toks"] if x["arp"] is not None and ANIO9.match(x["tok"])]
    p(f"  tokens con forma de año a la derecha del rótulo que toman el ejercicio de la regla: {len(anios_der)}")
    for r, x in anios_der[:20]:
        p(f"    {donde(r)} «{x['tok']}» · «{corta(r['l'], 110)}»")
    # la fecha del rótulo frente a una columna de ejercicio reconocida en C16 para tokens a la derecha (¿conflicto fila/columna?)
    conf = Counter()
    ej_conf = []
    for r in regla:
        for x in r["toks"]:
            if x["arp"] is None:
                continue
            for y, g in x["G"].items():
                dn = g.get("dn", {}).get("ejercicio") or (g.get("ej") or ["", ""])[1]
                if "fecha en" in dn:
                    conf[(g["n"][1], g["n"][2])] += 1
    p(f"  candidatas a la derecha del rótulo con el ejercicio decidido por la regla, por (ejercicio, columna) en C18: {dict(conf)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
