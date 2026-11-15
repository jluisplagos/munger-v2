"""Revisión n.º 5 (frente E · F1 · Elis). Recuento por clases, con la ejecución oficial del verificador de dos versiones.
No modifica nada del autor.

contraejemplos_5.py da un ejemplo de cada clase. Aquí se mide cuántas filas reales hay en cada una. Las filas se eligen
con criterios propios del revisor (no con las funciones de decisión del autor) y se entregan a verificar_cifras.py de
cada versión como proceso aparte.

  R  tablas de reexpresión (nota 1.4) de las cinco publicaciones: columna publicada, ajustes y columna reexpresada;
  P  bloques por país de la nota de pensiones («X – DETAILS», «DÉTAIL POUR X») de las cinco publicaciones;
  G  filas de segmento de las cinco tablas de crecimiento del informe de gestión;
  S  columna de 2020 de los estados principales del URD 2021 (cuenta de resultados, resultado global y EFE);
  N  enteros de seis cifras o más en todas las páginas del grupo.

Cada token se declara como una cifra del grupo en millones de euros (o «%»), de dos columnas (en G, también como
crecimiento orgánico), con el ejercicio que le corresponde y la edición que exige la regla.

Uso: python3 -I clases_5.py --raiz <munger_v2_r1> --anterior C8=<frente C8> --nueva C11=<frente C11>
"""
import argparse
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from arnes import DIMS, Modulo, estados, fila, oficial  # noqa: E402
from barrido_tablas import palabras_sobre, zona_propia  # noqa: E402

PUB = re.compile(r"(?i)^(?:published|publié|reported)$")
REX = re.compile(r"(?i)^(?:restated|retraité)\*?$")
TITULO_BLOQUE = re.compile(r"^\s*(?:\d\s+)?((?:[A-ZÉÈ' ]+ – DETAILS)|(?:DÉTAIL POUR [A-ZÉÈ' -]+))\s*\d?\s*$")
FIN_BLOQUE = re.compile(r"^\s*(?:\d\s+)?(?:\d\.\d\s+[A-Z]|NOTE \d|INFORMATION BY REGION|INFORMATIONS? PAR)")
SEGMENTO = re.compile(r"(?i)france|europ|scandinav|ireland|irlande|royaume|kingdom|\buk\b|latin|amérique|\bl'est\b|other|autres")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raiz", required=True)
    ap.add_argument("--anterior", required=True)
    ap.add_argument("--nueva", required=True)
    a = ap.parse_args()
    (na, ca), (nn, cn) = a.anterior.split("=", 1), a.nueva.split("=", 1)
    M = Modulo(cn, a.raiz, "verificador_revisado")
    filas, meta = [], {}

    def anadir(clase, doc, p, lineas, i, idx, anio, **extra):
        idioma = M.fuentes[doc]["idioma"]
        toks = M.m.tokens_numericos(lineas[i], idioma)
        tok = toks[idx]
        E = M.fuentes[doc]["ejercicio"]
        modo = extra.get("control_anio", "dos_columnas")
        vig = (anio == E) if modo == "crecimiento" else (anio == E - 1 or (anio == E and (E + 1) not in M.ejercicios))
        iguales = [k for k, l in enumerate(lineas) if l == lineas[i]]
        idf = extra.pop("idf", "R5") + f"_{len(filas)}"
        filas.append(fila(idf, doc=doc, pagina=p, anio=anio, etiqueta="re:^" + re.escape(lineas[i]) + "$", ocurrencia=iguales.index(i) + 1,
                          pos=idx - len(toks), literal=tok, valor_publicado=str(M.m.valor(tok, idioma)), unidad="%" if "%" in tok else "mm EUR",
                          edicion="vigente" if vig else "anterior", **extra))
        meta[idf] = {"clase": clase, "doc": doc, "p": p, "i": i + 1, "tok": tok, "anio": anio, "linea": re.sub(r"  +", "  ", lineas[i].strip())[:90]}
        return idf

    def datos(doc, p):
        lineas = M.texto(doc, p).splitlines()
        idioma = M.fuentes[doc]["idioma"]
        out = []
        for i, l in enumerate(lineas):
            toks = M.m.tokens_numericos(l, idioma)
            sp = M.m.spans_numericos(l, idioma)
            rot = M.m.rotulo(l)
            if toks and sp and rot and not M.m.es_numero(rot, idioma) and not re.search(r"Universal Registration|enregistrement universel", l):
                out.append((i, toks, sp))
        return lineas, out

    # ------------------------------------------------------------------ R: tablas de reexpresión
    REEX = {"URD2021": (236, 237, 238, 239), "URD2022": (268, 269, 270, 271), "URD2023": (286, 287, 288, 289),
            "DEU2024FR": (280, 281, 282, 283), "URD2025": (334, 335, 336, 337)}
    for doc, pags in REEX.items():
        E = M.fuentes[doc]["ejercicio"]
        for p in pags:
            lineas, dd = datos(doc, p)
            for i, toks, sp in dd:
                _, zona = zona_propia(lineas, i)
                if not zona or not any(PUB.match(w) for k in zona for w in lineas[k].split()):
                    continue
                for idx, tok in enumerate(toks):
                    if tok in M.m.PLACEHOLDER or "€" in tok or not re.search(r"\d[.,]\d", tok):
                        continue
                    cerca, _ = palabras_sobre(lineas, zona, sp[idx][1])
                    col = "publicada" if any(PUB.match(w) for w in cerca) else "reexpresada" if any(REX.match(w) for w in cerca) else "ajuste u otra"
                    meta[anadir("R", doc, p, lineas, i, idx, E - 1)]["col"] = col

    # ------------------------------------------------------------------ P: bloques por país de la nota de pensiones
    PENS = {"URD2021": (257, 261), "URD2022": (289, 294), "URD2023": (307, 312), "DEU2024FR": (301, 306), "URD2025": (355, 360)}
    for doc, (p0, p1) in PENS.items():
        E = M.fuentes[doc]["ejercicio"]
        bloque = None
        for p in range(p0, p1 + 1):
            lineas, dd = datos(doc, p)
            de_linea = {}
            for i, l in enumerate(lineas):
                m = TITULO_BLOQUE.match(l)
                if m:
                    bloque = m.group(1).strip()
                elif FIN_BLOQUE.match(l):
                    bloque = None
                de_linea[i] = bloque
            for i, toks, sp in dd:
                if not de_linea.get(i):
                    continue
                for idx, tok in enumerate(toks):
                    if tok in M.m.PLACEHOLDER or re.fullmatch(r"\(?\d\)?", tok):
                        continue
                    for anio in (E, E - 1):
                        x = meta[anadir("P", doc, p, lineas, i, idx, anio)]
                        x["bloque"], x["token"] = de_linea[i], (doc, p, i, idx)

    # ------------------------------------------------------------------ G: tablas de crecimiento
    CREC = {"URD2021": 211, "URD2022": 243, "URD2023": 261, "DEU2024FR": 253, "URD2025": 307}
    for doc, p in CREC.items():
        E = M.fuentes[doc]["ejercicio"]
        lineas, dd = datos(doc, p)
        j_total = next(i for i, l in enumerate(lineas) if re.match(r"^\s*TOTAL\s{2,}", l))
        j_cab = next(i for i in range(j_total, -1, -1) if re.search(r"\((?:[Ii]n|en) millions", lineas[i]))
        for i, toks, sp in dd:
            if not (j_cab < i < j_total) or len(toks) < 4:
                continue
            x = meta[anadir("G", doc, p, lineas, i, 0, E)]                      # ventas del ejercicio de la publicación
            x["que"] = "ventas"
            # crecimiento orgánico: última columna en 2021 (publicado | orgánico); tercera en las demás (orgánico | externo | divisa | publicado)
            idx = len(toks) - 1 if doc == "URD2021" else 2
            if "%" in toks[idx]:
                x = meta[anadir("G", doc, p, lineas, i, idx, E, idf="CREC_ORG_R5", control_anio="crecimiento")]
                x["que"] = "crecimiento orgánico"

    # ------------------------------------------------------------------ S: estados principales del URD 2021, columna de 2020
    for p in (226, 227, 229):
        lineas, dd = datos("URD2021", p)
        for i, toks, sp in dd:
            if len(toks) < 2 or toks[-1] in M.m.PLACEHOLDER or re.search(r"per share|\(in euros\)", lineas[i]) or not re.search(r"\d\.\d$|\d\.\d\)$", toks[-1]):
                continue
            for anio in (2020, 2021):
                meta[anadir("S", "URD2021", p, lineas, i, len(toks) - 1, anio)]["ancho"] = len(toks[-1])

    # ------------------------------------------------------------------ N: enteros de seis cifras o más
    for doc in sorted(M.fuentes):
        E = M.fuentes[doc]["ejercicio"]
        dec = r",\d" if M.fuentes[doc]["idioma"] == "fr" else r"\.\d"
        for p in range(1, M.paginas(doc) + 1):
            lineas = M.texto(doc, p).splitlines()
            if not any(M.m.GRUPO_RX.search(l) for l in [x for x in lineas if x.strip()][:8]):
                continue
            _, dd = datos(doc, p)
            for i, toks, sp in dd:
                for idx, tok in enumerate(toks):
                    if "%" in tok or "€" in tok or re.search(dec, tok) or len(re.sub(r"\D", "", tok)) < 6:
                        continue
                    meta[anadir("N", doc, p, lineas, i, idx, E)]["rot"] = M.m.rotulo(lineas[i])[:60]

    ra, rn = oficial(ca, a.raiz, filas)[1], oficial(cn, a.raiz, filas)[1]
    print(f"Filas entregadas al verificador oficial de {na} y de {nn}: {len(filas)}\n")

    def est(r):
        return r["estado"]

    def tabla(titulo, grupos):
        print(titulo)
        for g, ids in grupos:
            ca_, cn_ = Counter(est(ra[i]) for i in ids), Counter(est(rn[i]) for i in ids)
            f = lambda c: " · ".join(f"{k} {c[k]}" for k in ("OK", "PENDIENTE", "FALLO") if c[k]) or "—"  # noqa: E731
            print(f"   {g:<58} {len(ids):5d}   {na}: {f(ca_):<34} {nn}: {f(cn_)}")
        print()

    R = [i for i in meta if meta[i]["clase"] == "R"]
    tabla("R. Tablas de reexpresión: tokens declarados del ejercicio anterior al de la publicación, edición «vigente»",
          [(f"columna {c}", [i for i in R if meta[i]["col"] == c]) for c in ("publicada", "ajuste u otra", "reexpresada")])
    for doc in REEX:
        ids = [i for i in R if meta[i]["doc"] == doc and meta[i]["col"] == "publicada"]
        dif = [i for i in ids if est(rn[i]) == "OK"]
        print(f"   {doc}: columna publicada, {len(ids)} tokens, {len(dif)} OK en las seis dimensiones en {nn}")
    print()

    P = [i for i in meta if meta[i]["clase"] == "P"]
    toks_p = sorted({meta[i]["token"] for i in P})

    def mejor(res, t):
        e = [est(res[i]) for i in P if meta[i]["token"] == t]
        return "OK" if "OK" in e else "PENDIENTE" if "PENDIENTE" in e else "FALLO"

    print("P. Bloques por país de la nota de pensiones: tokens de las tablas del bloque (mejor estado con el ejercicio E o E−1)")
    for nombre, filtro in (("en millones de euros", lambda t: "%" not in next(meta[i]["tok"] for i in P if meta[i]["token"] == t)),
                           ("en porcentaje", lambda t: "%" in next(meta[i]["tok"] for i in P if meta[i]["token"] == t))):
        ts = [t for t in toks_p if filtro(t)]
        ca_, cn_ = Counter(mejor(ra, t) for t in ts), Counter(mejor(rn, t) for t in ts)
        print(f"   {nombre:<24} {len(ts):5d} tokens   {na}: {dict(ca_)}   {nn}: {dict(cn_)}")
    por_doc = Counter()
    for t in toks_p:
        if mejor(rn, t) == "OK" and "%" not in next(meta[i]["tok"] for i in P if meta[i]["token"] == t):
            por_doc[t[0]] += 1
    print(f"   en millones de euros y OK en {nn}, por publicación: {dict(por_doc)}")
    per = Counter()
    for i in P:
        if est(rn[i]) != "OK" and est(ra[i]) == "OK":
            per[estados(rn[i])["perimetro"]] += 1
    print(f"   filas (token × ejercicio) OK en {na} y no en {nn}: perímetro en {nn}: {dict(per)}")
    print(f"   tokens en millones de euros que quedan OK en {nn}, por página y bloque (líneas):")
    donde = {}
    for t in toks_p:
        if mejor(rn, t) == "OK" and "%" not in next(meta[i]["tok"] for i in P if meta[i]["token"] == t):
            b = next(meta[i]["bloque"] for i in P if meta[i]["token"] == t)
            donde.setdefault((t[0], t[1], b), []).append(t[2] + 1)
    for (d, p, b), ls in sorted(donde.items()):
        print(f"      {d} p.{p} · {b} · {len(ls)} tokens · líneas {min(ls)}–{max(ls)}")
    print()

    G = [i for i in meta if meta[i]["clase"] == "G"]
    print(f"G. Tablas de crecimiento: filas entre la cabecera y TOTAL (segmentos), declaradas del grupo; estado en {nn}")
    for doc, p in CREC.items():
        for que in ("ventas", "crecimiento orgánico"):
            ids = [i for i in G if meta[i]["doc"] == doc and meta[i]["que"] == que]
            pasan = [meta[i]["linea"].split("  ")[0] for i in ids if est(rn[i]) == "OK"]
            print(f"   {doc} p.{p} · {que:<21} {len(ids)} filas · OK en las seis dimensiones: {len(pasan)} {pasan}")
    print()

    S = [i for i in meta if meta[i]["clase"] == "S"]
    print("S. Estados principales del URD 2021 (p.226, 227 y 229), columna «12/31/2020 restated (a)»")
    bien, mal = [i for i in S if meta[i]["anio"] == 2020], [i for i in S if meta[i]["anio"] == 2021]
    tabla("", [("token de 2020 declarado 2020 (legítimo)", bien), ("el mismo token declarado 2021 (ejercicio equivocado)", mal)])
    anchos = Counter((meta[i]["ancho"], est(rn[i])) for i in bien)
    print("   legítimos, por anchura del literal en caracteres → estado en " + nn + ": " +
          ", ".join(f"{w} car.: {dict((e, n) for (ww, e), n in anchos.items() if ww == w)}" for w in sorted({w for w, _ in anchos})) + "\n")

    N = [i for i in meta if meta[i]["clase"] == "N"]
    print("N. Enteros de seis cifras o más en las páginas del grupo, declarados en millones de euros: dimensión «unidad»")
    tr = Counter((estados(ra[i])["unidad"], estados(rn[i])["unidad"]) for i in N)
    for (x, y), n in sorted(tr.items()):
        print(f"   {na} {x} → {nn} {y}: {n}")
    nuevos = sorted({(meta[i]["doc"], meta[i]["p"], meta[i]["rot"]) for i in N if estados(ra[i])["unidad"] == "OK" and estados(rn[i])["unidad"] == "PENDIENTE"})
    print(f"   líneas que pasan de OK a PENDIENTE ({len(nuevos)}):")
    for d, p, r in nuevos:
        print(f"      {d} p.{p} · {r}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
