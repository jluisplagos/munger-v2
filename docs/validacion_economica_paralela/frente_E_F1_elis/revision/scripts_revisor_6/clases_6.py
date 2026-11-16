"""Revisión n.º 6 (frente E · F1 · Elis). Clases de las transiciones del barrido C11 → C13, cruzadas con la lectura propia
(geometría y tipografía). No modifica nada del autor.

Entradas: el barrido de barrido_6.py (todas las candidatas) y la lectura de lectura_geometrica.py (tokens de las páginas
del grupo). Para cada dimensión que cambia entre versiones se cuenta cuántas transiciones coinciden con la lectura propia
y cuántas no, y se listan las páginas. La lectura propia es un filtro para encontrar clases, no una verdad: cada clase que
se lleva al informe está comprobada en la página y con el verificador oficial (contraejemplos_6.py).

Uso: python3 -I clases_6.py --todas <barrido.jsonl.gz> --lectura <lectura.jsonl.gz> [--anterior C11 --nueva C13]
"""
import argparse
import gzip
import json
import re
import sys
from collections import Counter, defaultdict

DIMS = ("literal", "ejercicio", "columna", "unidad", "perimetro", "edicion")
E = {"URD2021": 2021, "URD2022": 2022, "URD2023": 2023, "DEU2024FR": 2024, "URD2025": 2025}
# lista propia de países, regiones y segmentos (más amplia que la del verificador)
PA = re.compile(r"(?i)\b(?:France|French|Germany|Allemagne|United Kingdom|Royaume-Uni|Great Britain|Grande-Bretagne|UK|Spain|Espagne|Andorra|"
                r"Brazil|Brésil|Netherlands|Pays-Bas|Denmark|Danemark|Sweden|Suède|Switzerland|Suisse|Mexico|Mexique|Ireland|Irlande|Eire|Russia|"
                r"Russie|Norway|Norvège|Italy|Italie|Portugal|Belgium|Belgique|Poland|Pologne|Chile|Chili|Colombia|Colombie|Finland|Finlande|"
                r"Austria|Autriche|Luxembourg|Czech|Tchèque|Slovakia|Hungary|Hongrie|Estonia|Latvia|Lettonie|Lithuania|Lituanie|Malaysia|Malaisie|"
                r"Singapore|Central Europe|Europe centrale|Scandinavia|Scandinavie|Eastern Europe|Europe de l'Est|Latin America|Amérique latine|"
                r"Southern Europe|Europe du Sud|Other countries|Autres pays)\b")
SOCIEDADES = re.compile(r"(?i)Subsidiaries and consolidated companies|Filiales et entreprises consolidées")
SUBPERIMETRO = re.compile(r"(?i)\b(?:of which|dont|excluding|hors|European Union|Union européenne|jurisdictions|juridictions|non coopératifs)\b")


def est(e):
    return "FALLO" if any(x in ("FALLO", "NO_EVALUADO") for x in e) else "PENDIENTE" if "PENDIENTE" in e else "OK"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--todas", required=True)
    ap.add_argument("--lectura", required=True)
    ap.add_argument("--anterior", default="C11")
    ap.add_argument("--nueva", default="C13")
    a = ap.parse_args()
    na, nn = a.anterior, a.nueva
    L = {}
    with gzip.open(a.lectura, "rt", encoding="utf-8") as g:
        for l in g:
            r = json.loads(l)
            L[(r["doc"], r["p"], r["i"], r["idx"])] = r
    C = []
    with gzip.open(a.todas, "rt", encoding="utf-8") as g:
        for l in g:
            c = json.loads(l)
            if c["g"]:
                C.append(c)
    K = lambda c: (c["doc"], c["p"], c["i"], c["idx"])  # noqa: E731
    R = lambda c: L[K(c)]  # noqa: E731
    BT = defaultdict(dict)
    for c in C:
        BT[K(c)][c["anio"]] = c
    w = print

    def paginas(cs, n=14):
        pp = Counter(f"{c['doc']} p.{c['p']}" for c in cs)
        return ", ".join(f"{q} ({m})" for q, m in sorted(pp.items(), key=lambda x: (-x[1], x[0]))[:n]) + (" …" if len(pp) > n else "")

    def ntok(cs):
        return len({K(c) for c in cs})

    w(f"Clases de las transiciones {na} → {nn} en las páginas del grupo, cruzadas con la lectura propia\n")
    geo = sum(1 for k in BT if L[k]["geo"])
    w(f"Tokens en páginas del grupo: {len(BT)}; con lectura geométrica propia: {geo} ({100 * geo / len(BT):.1f} %)")
    w(f"Candidatas (token × ejercicio E, E−1, E−2): {len(C)}; OK en las seis dimensiones: {na} {sum(est(c['a_e']) == 'OK' for c in C)} · {nn} {sum(est(c['n_e']) == 'OK' for c in C)}")

    # ------------------------------------------------------------------ A. ejercicio
    def verdad_anio(c):
        r = R(c)
        if not r["geo"]:
            return "sin lectura"
        if c["anio"] in r["cierre"] or (c["anio"] + 1) in r["apertura"]:
            return "la cabecera alineada es del ejercicio declarado"
        if r["cierre"] or r["apertura"]:
            return "la cabecera alineada es de otro ejercicio"
        return "ninguna fecha alineada (otra medida, otra entidad o sin cabecera)"

    w("\n\n== A. Dimensión «ejercicio»: transición × lectura propia de la cabecera alineada por la derecha (candidatas) ==")
    tr = defaultdict(Counter)
    gr = defaultdict(list)
    for c in C:
        if c["a_e"][1] != c["n_e"][1]:
            v = verdad_anio(c)
            tr[(c["a_e"][1], c["n_e"][1])][v] += 1
            gr[(c["a_e"][1], c["n_e"][1], v)].append(c)
    for k in sorted(tr):
        w(f"  {k[0]} → {k[1]}: {sum(tr[k].values())}")
        for v, n in sorted(tr[k].items(), key=lambda x: -x[1]):
            w(f"      {n:6d}  {v} · páginas: {paginas(gr[(k[0], k[1], v)], 8)}")

    # ------------------------------------------------------------------ B. edición
    w("\n\n== B. Dimensión «edición»: transición × lectura propia de la columna (candidatas) ==")
    tr = defaultdict(Counter)
    gr = defaultdict(list)
    for c in C:
        if c["a_e"][5] != c["n_e"][5]:
            r = R(c)
            v = "sin lectura" if not r["geo"] else ("columna «published», «reported» o «publié»" if r["ed"] == "publicada" else
                                                    "columna «restated» o «retraité»" if r["ed"] == "reexpresada" else
                                                    "columna sin marca de edición (ajuste «IFRS 3» u otra): " + " ".join(r["al"])[:30])
            tr[(c["a_e"][5], c["n_e"][5])][re.sub(r": .*", "", v)] += 1
            gr[(c["a_e"][5], c["n_e"][5], re.sub(r": .*", "", v))].append(c)
    for k in sorted(tr):
        w(f"  {k[0]} → {k[1]}: {sum(tr[k].values())}")
        for v, n in sorted(tr[k].items(), key=lambda x: -x[1]):
            w(f"      {n:6d}  {v} · páginas: {paginas(gr[(k[0], k[1], v)], 8)}")
    pub = [c for c in C if R(c)["geo"] and R(c)["ed"] == "publicada" and c["anio"] == E[c["doc"]] - 1]
    rex = [c for c in C if R(c)["geo"] and R(c)["ed"] == "reexpresada" and c["anio"] == E[c["doc"]] - 1]
    reexp_pag = {(c["doc"], c["p"]) for c in pub if re.search(r"(?i)published|publi|reported", " ".join(R(c)["al"])) and not re.search(r"(?i)growth|croissance", " ".join(R(c)["al"]))}
    pub_t = [c for c in pub if (c["doc"], c["p"]) in reexp_pag and not re.search(r"(?i)growth|croissance", " ".join(R(c)["al"]))]
    w(f"\n  Columna publicada de las tablas de reexpresión según la lectura propia, declarada del ejercicio anterior y «vigente»: {len(pub_t)} tokens en {len(reexp_pag)} páginas")
    w(f"      estado de la fila: {na} {dict(Counter(est(c['a_e']) for c in pub_t))} · {nn} {dict(Counter(est(c['n_e']) for c in pub_t))}")
    w(f"      dimensión edición en {nn}: {dict(Counter(c['n_e'][5] for c in pub_t))}")
    queda = [c for c in pub_t if est(c["n_e"]) == "OK"]
    w(f"      quedan OK en las seis dimensiones en {nn}: {len(queda)} " + "; ".join(f"{c['doc']} p.{c['p']} l.{c['i'] + 1} «{c['tok']}» ({c['rot'][:25]})" for c in queda))
    rex_t = [c for c in rex if (c["doc"], c["p"]) in reexp_pag]
    w(f"  Columna reexpresada en esas mismas páginas: {len(rex_t)} tokens · fila {na} → {nn}: {dict(Counter((est(c['a_e']), est(c['n_e'])) for c in rex_t))}")

    # ------------------------------------------------------------------ C. perímetro
    def nombra(r):
        out = []
        if r.get("enc") and PA.search(r["enc"][0]):
            out.append("encabezado «" + r["enc"][0][:40] + "»")
        if r.get("tit") and PA.search(r["tit"]):
            out.append("título de tabla «" + r["tit"][:30] + "»")
        un = re.sub(r"\((?:[Ii]n|en) [^)]*\)", "", r.get("un") or "")
        if PA.search(un):
            out.append("columnas «" + un.strip()[:40] + "»")
        return out

    def titulo_autor(c):
        m = re.findall(r"«([^»]*)»", c["n_d"].get("perimetro", "") if c["n_e"][4] != "OK" else c["a_d"].get("perimetro", ""))
        return re.sub(r"\s+", " ", m[0])[:40] if m else "—"

    w("\n\n== C. Dimensión «perímetro»: transición × lectura propia del bloque (tokens; el estado del perímetro no depende del ejercicio declarado) ==")
    grupos = defaultdict(list)
    for k, d in BT.items():
        c = next(iter(d.values()))
        r = L[k]
        t = (c["a_e"][4], c["n_e"][4])
        if t[0] == t[1]:
            continue
        if not r["geo"]:
            cl = "sin lectura"
        elif nombra(r):
            cl = "la lectura propia nombra un país o un segmento (encabezado, título de tabla o columnas)"
        elif r.get("enc") and SOCIEDADES.search(r["enc"][0]):
            cl = "lista de sociedades consolidadas por país (subtítulos de país en negrita de 7 puntos)"
        else:
            cl = "la lectura propia NO nombra ningún país ni segmento"
        grupos[(t, cl)].append((k, c, r))
    for t in sorted({t for t, _ in grupos}):
        w(f"  {t[0]} → {t[1]}: {sum(len(v) for (tt, _), v in grupos.items() if tt == t)} tokens")
        for (tt, cl), v in sorted(grupos.items(), key=lambda x: -len(x[1])):
            if tt != t:
                continue
            w(f"      {len(v):6d}  {cl}")
            bp = defaultdict(list)
            for k, c, r in v:
                bp[k[:2]].append((k, c, r))
            if cl.startswith("lista de sociedades") or cl == "sin lectura":
                w("              páginas: " + ", ".join(f"{d} p.{p} ({len(x)})" for (d, p), x in sorted(bp.items())))
                continue
            for (doc, p), x in sorted(bp.items()):
                ta = Counter(titulo_autor(y[1]) for y in x).most_common(2)
                mio = Counter(("; ".join(nombra(y[2])) or ((y[2]["enc"][0][:44] + (f" [página −{y[2]['enc'][2]}]" if y[2]["enc"][2] else "")) if y[2].get("enc") else "—")) for y in x).most_common(2)
                okf = sum(1 for y in x if any(est(z["n_e"]) == "OK" for z in BT[y[0]].values()))
                k0, c0, r0 = x[0]
                w(f"              {doc} p.{p}: {len(x)} tokens (con alguna declaración OK en las seis dimensiones en {nn}: {okf}) · título que ve el verificador: "
                  f"{', '.join(f'«{q}» ({m})' for q, m in ta)} · lectura propia: {', '.join(f'{q} ({m})' for q, m in mio)} · ej. l.{k0[2] + 1} «{c0['tok']}» ({c0['rot'][:30]})")

    # ------------------------------------------------------------------ D. filas que pasan a OK
    w(f"\n\n== D. Candidatas que no eran OK en {na} y son OK en las seis dimensiones en {nn} ==")
    nuevas = [c for c in C if est(c["n_e"]) == "OK" and est(c["a_e"]) != "OK"]
    w(f"  total: {len(nuevas)} candidatas, {ntok(nuevas)} tokens")
    rest = [c for c in nuevas if (c["doc"], c["p"]) in reexp_pag and R(c)["geo"] and R(c)["ed"] == "reexpresada"]
    w(f"  columna reexpresada de las tablas de reexpresión: {len(rest)} · por publicación: {dict(Counter(c['doc'] for c in rest))}")
    otras = [c for c in nuevas if c not in rest]
    w(f"  otras: {len(otras)}")
    bp = defaultdict(list)
    for c in otras:
        bp[(c["doc"], c["p"])].append(c)
    for (doc, p), v in sorted(bp.items()):
        r = R(v[0])
        cab = Counter()
        for c in v:
            rr = R(c)
            cab[(" / ".join(rr["al"])[:50] + (" ‖ solapa: " + " / ".join(rr["so"])[:40] if rr.get("so") else "")) if rr["geo"] else "sin lectura"] += 1
        rots = Counter(c["rot"][:38] for c in v)
        w(f"      {doc} p.{p}: {len(v)} · rótulos: {', '.join(f'«{q}» ({m})' for q, m in rots.most_common(5))}")
        w(f"            cabecera propia: {'; '.join(f'{q} ({m})' for q, m in cab.most_common(4))}")

    # ------------------------------------------------------------------ D2. OK bajo una cabecera que no es solo una fecha
    w(f"\n\n== D2. Candidatas OK en las seis dimensiones en {nn}, según la cabecera propia de su columna ==")
    okn = [c for c in C if est(c["n_e"]) == "OK"]

    def clase_cab(c):
        r = R(c)
        if not r["geo"]:
            return "sin lectura"
        otras = geom_otras(r)
        if c["anio"] in r["cierre"] or (c["anio"] + 1) in r["apertura"]:
            return "fecha del ejercicio declarado y nada más" if not otras else "fecha del ejercicio declarado y, además, otra medida o entidad"
        if r["cierre"] or r["apertura"]:
            return "fecha de otro ejercicio"
        return "ninguna fecha: solo una medida, una entidad o nada"

    def geom_otras(r):
        return [x for x in (r.get("otras_al") or []) + (r.get("otras_so") or []) if not re.fullmatch(r"(?i)consolidated|statement|of|financial|position|comprehensive|income|cash|flows|the|for|year|years|january|er|janvier|net", x)]

    cl = defaultdict(list)
    for c in okn:
        cl[clase_cab(c)].append(c)
    for k, v in sorted(cl.items(), key=lambda x: -len(x[1])):
        nuevas_k = [c for c in v if est(c["a_e"]) != "OK"]
        w(f"  {len(v):6d}  {k} · de ellas, no eran OK en {na}: {len(nuevas_k)}")
        if k.startswith("fecha del ejercicio declarado y nada"):
            continue
        cab = Counter()
        for c in v:
            r = R(c)
            cab[(" ".join(r["al"])[:34] + (" ‖ " + " ".join(r["so"])[:30] if r.get("so") else "")) if r["geo"] else "—"] += 1
        w("          cabeceras más frecuentes: " + "; ".join(f"«{q}» ({m})" for q, m in cab.most_common(9)))
        w(f"          páginas: {paginas(v, 16)}")

    # ------------------------------------------------------------------ E. subperímetros por rótulo
    w(f"\n\n== E. Filas cuyo rótulo nombra un país, una región, una UGE o una jurisdicción y quedan OK en las seis dimensiones como del grupo ==")
    JUR = re.compile(r"(?i)European Union|Union européenne|jurisdictions|juridictions|non coopératifs|Non-cooperative")

    def rotulo_sub(c):
        r = R(c)
        ant = (r.get("rot_ant") or "") if r["geo"] else ""
        junto = (ant + " " + c["rot"]) if ant and not re.search(r"\d", ant) else c["rot"]
        return PA.search(c["rot"]) or JUR.search(junto) or (junto != c["rot"] and PA.search(ant) and re.search(r"(?i)excluding|hors|\(", ant))

    sub = [c for c in C if rotulo_sub(c) and not re.search(r"(?i)universal registration|enregistrement", c["rot"])]
    for nom, idx in ((na, "a_e"), (nn, "n_e")):
        okc = [c for c in sub if est(c[idx]) == "OK"]
        w(f"  {nom}: {len(okc)} candidatas, {ntok(okc)} tokens · páginas: {paginas(okc, 24)}")
    okn = [c for c in sub if est(c["n_e"]) == "OK"]
    bl = defaultdict(list)
    for c in okn:
        bl[(c["doc"], c["p"])].append(c)
    for (doc, p), v in sorted(bl.items()):
        antes = sum(est(c["a_e"]) == "OK" for c in v)
        rots = []
        for c in v:
            r = R(c)
            t = ((r.get("rot_ant") or "") + " / " if r["geo"] and r.get("rot_ant") and not re.search(r"\d", r.get("rot_ant") or "") else "") + c["rot"][:34]
            if t not in rots:
                rots.append(t)
        w(f"      {doc} p.{p}: OK en {nn} {len(v)} (en {na}: {antes}) · rótulos: {'; '.join('«' + t + '»' for t in rots[:14])}")

    # ------------------------------------------------------------------ F. cifras del ejercicio que pasan a FALLO en los tres años
    w(f"\n\n== F. Tokens cuyo ejercicio falla con los tres ejercicios declarados en {nn} y no fallaba con los tres en {na} ==")
    f3 = [k for k, d in BT.items() if all(c["n_e"][1] == "FALLO" for c in d.values()) and not all(c["a_e"][1] == "FALLO" for c in d.values())]
    w(f"  total: {len(f3)} tokens")
    libros = [k for k in f3 if L[k]["geo"] and re.search(r"(?i)carrying|comptable|amorti[sz]ed|amorti\b", " ".join(L[k]["al"])) and not L[k]["cierre"]]
    w(f"  de ellos, bajo una cabecera alineada de valor en libros o coste amortizado sin fecha (cifras del cierre de la publicación): {len(libros)}")
    for k in sorted(libros):
        c = BT[k][E[k[0]]]
        w(f"      {k[0]} p.{k[1]} l.{k[2] + 1} «{c['tok']}» ({c['rot'][:30]}) · cabecera propia: {' / '.join(L[k]['al'])[:50]} · declarado {c['anio']}: "
          f"{na} {c['a_e'][1]} → {nn} {c['n_e'][1]} · {c['n_d'].get('ejercicio', '')[:95]}")

    # ------------------------------------------------------------------ G. las cuatro clases del encargo
    w("\n\n== G. Las cuatro clases que nombra el encargo ==")

    def tabla(titulo, sel_tok):
        ks = [k for k in BT if sel_tok(k)]
        cs = [c for k in ks for c in BT[k].values()]
        w(f"\n  {titulo}: {len(ks)} tokens en {len({k[:2] for k in ks})} páginas")
        w(f"      estado de la fila (candidatas) {na} → {nn}: " + ", ".join(f"{x}→{y} {n}" for (x, y), n in sorted(Counter((est(c['a_e']), est(c['n_e'])) for c in cs).items())))
        w(f"      perímetro (tokens) {na} → {nn}: " + ", ".join(f"{x}→{y} {n}" for (x, y), n in sorted(Counter((BT[k][E[k[0]]]['a_e'][4], BT[k][E[k[0]]]['n_e'][4]) for k in ks).items())))
        okn = [c for c in cs if est(c["n_e"]) == "OK"]
        w(f"      candidatas OK en las seis dimensiones en {nn}: {len(okn)} · páginas: {paginas(okn, 12)}")
        return ks, cs

    def enc(k):
        r = L[k]
        return (r["enc"][0] if r["geo"] and r.get("enc") else "")

    tabla("Bloques de la nota de pensiones por país (encabezado «X – DETAILS» / «DÉTAIL POUR X»)", lambda k: re.search(r"DETAILS|DÉTAIL POUR", enc(k)) is not None)
    TOT_BAL = re.compile(r"(?i)^TOTAL (?:ASSETS|EQUITY AND LIABILITIES)\b|^TOTAL (?:DE L')?ACTIFS?\b|^TOTAL (?:DES )?(?:PASSIFS? ET CAPITAUX PROPRES|CAPITAUX PROPRES ET PASSIFS?)\b")
    pag_bal = {(c["doc"], c["p"]) for c in C if TOT_BAL.search(c["rot"])}
    ks, cs = tabla("Balances (páginas con las filas «TOTAL ASSETS» / «TOTAL EQUITY AND LIABILITIES» o sus equivalentes en francés; filas con cabecera propia)",
                   lambda k: k[:2] in pag_bal and L[k]["geo"] and len(L[k]["al"]) > 0)
    por_pag = defaultdict(set)
    for k in ks:
        por_pag[k[:2]] |= {t for t in L[k]["al"] if re.search(r"20\d\d", t)}
    for (doc, p), al in sorted(por_pag.items()):
        cc = [c for k in ks if k[:2] == (doc, p) for c in BT[k].values()]
        bien = [c for c in cc if verdad_anio(c).startswith("la cabecera alineada es del ejercicio declarado")]
        mal = [c for c in cc if verdad_anio(c).startswith("la cabecera alineada es de otro")]
        w(f"      {doc} p.{p}: fechas de cabecera {sorted(al)[:5]} · declaración con el ejercicio de su cabecera: {nn} {dict(Counter(c['n_e'][1] for c in bien))}"
          f" ({na} {dict(Counter(c['a_e'][1] for c in bien))}) · con otro ejercicio: {nn} {dict(Counter(c['n_e'][1] for c in mal))} ({na} {dict(Counter(c['a_e'][1] for c in mal))})")
    tabla("Tablas de sensibilidad del deterioro por país o UGE (título de tabla que nombra un país, o encabezado «Sensitivity» / «Sensibilité»)",
          lambda k: L[k]["geo"] and (re.search(r"(?i)sensitivity|sensibilité", enc(k)) is not None or (PA.search(L[k].get("tit", "")) is not None and "WACC" in " ".join(c["rot"] for c in BT[k].values()))))
    tabla("Listas de sociedades consolidadas por país", lambda k: SOCIEDADES.search(enc(k)) is not None)
    return 0


if __name__ == "__main__":
    sys.exit(main())
