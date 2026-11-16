"""Revisión independiente n.º 8 · consultas al barrido propio que desglosan lo que `clases_8.py` no imprime.

Cada bloque da un recuento que el informe cita y que no sale tal cual de `barrido_8.txt` ni de `clases_8.txt`. Usa las
mismas clases de línea que `clases_8.py` (se importan de él). No modifica nada del autor.

  Q1  las aceptaciones nuevas: líneas y páginas de las cifras de saldos y de los demás tokens;
  Q2  las transiciones del estado de la fila, por la dimensión que las causa;
  Q3  los cambios de «ejercicio» que no vienen de la regla de la fila con fecha (S1);
  Q4  la regla de la fila con fecha frente a una cabecera con columnas de ejercicio reconocidas por C14;
  Q5  las líneas en que la regla se dispara y que no son filas de saldo ni recuentos con fecha, por tipo;
  Q6  S2: líneas de las páginas del grupo con rótulos contiguos y dos tokens o más;
  Q7  S3: los cambios de «unidad» (la pestaña ante una línea de prosa);
  Q8  S7 d: el epígrafe de las marcas en las cinco publicaciones, línea a línea, con el estado del perímetro en C16;
  Q9  decisión (b): candidatas en las que solo el perímetro impide el OK por la regla de grupos de columnas;
  Q10 los recuentos de la séptima parte de las respuestas sobre el «ejercicio», en el universo de la revisión n.º 6.

Uso: python3 -I -B consultas_8.py --todas <jsonl.gz de barrido_8.py> --raiz <munger_v2_r1> --c14 <frente C15> --c16 <frente C17>
"""
import argparse
import gzip
import json
import re
import sys
from collections import Counter, OrderedDict, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import arnes8 as H  # noqa: E402
from clases_8 import clase_linea, corta, es_anio, est, plantilla  # noqa: E402

REGLA_FILA = ("saldo de ", "la fila es el saldo de ")
ESTADOS_PATRIMONIO = {("URD2021", 230), ("URD2021", 231), ("URD2022", 262), ("URD2022", 263), ("URD2023", 280), ("URD2023", 281),
                      ("DEU2024FR", 274), ("DEU2024FR", 275), ("URD2025", 328), ("URD2025", 329)}


def por_regla_de_fila(motivo):
    return motivo.startswith(REGLA_FILA) and "fecha en" in motivo


def clase_token(ln, t):
    """La misma clase de token que la sección B de clases_8.py."""
    tok = t["tok"]
    if not clase_linea(ln).startswith("fila de saldo"):
        return "año de la fecha en una línea que no es una fila de saldo" if es_anio(tok) else "otra cifra en una línea que no es una fila de saldo"
    if es_anio(tok):
        return "año de la fecha del propio rótulo, en una fila de saldo"
    if t["k"] == 0 and re.fullmatch(r"\d", tok) and ln["rot14"] != ln["rot16"]:
        return "pestaña del capítulo («6») en una fila de saldo"
    if (re.fullmatch(r"\d\d?", tok) and re.search(r"(?i)december,? ?" + tok + r"\b|" + tok + r" d[ée]cembre", ln["l"][:t["a1"] + 12])
            and t["a0"] < len(ln["rot16"]) + (len(ln["l"]) - len(ln["l"].lstrip())) + 2):
        return "día de la fecha del propio rótulo («31»), en una fila de saldo"
    return "cifra de una fila de saldo"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--todas", required=True)
    ap.add_argument("--raiz", required=True)
    ap.add_argument("--c14", required=True)
    ap.add_argument("--c16", required=True)
    a = ap.parse_args()
    N = H.Version("C16", a.c16, a.raiz)
    V = N.V
    L = []
    with gzip.open(a.todas, "rt", encoding="utf-8") as f:
        for l in f:
            L.append(json.loads(l))
    L.sort(key=lambda x: (x["doc"], x["p"], x["i"]))
    porlinea = {(ln["doc"], ln["p"], ln["i"]): ln for ln in L}
    DIM = {d: j for j, d in enumerate(H.DIMS)}
    p = print

    def cands():
        for ln in L:
            for t in ln["toks"]:
                for y, g in t["G"].items():
                    yield ln, t, y, g

    def donde(ln):
        return f"{ln['doc']} p.{ln['p']} l.{ln['i'] + 1}"

    def paginas(items, n=12):
        c = Counter((ln["doc"], ln["p"]) for ln in items)
        return ", ".join(f"{d} p.{pg} ({v})" for (d, pg), v in sorted(c.items(), key=lambda kv: (-kv[1], kv[0]))[:n]) + (" …" if len(c) > n else "")

    p("Consultas de la revisión n.º 8 al barrido propio · C14 → C16")

    # ------------------------------------------------------------------ Q1
    p()
    p("== Q1. Aceptaciones nuevas (no OK en C14, OK en las seis dimensiones en C16): líneas y páginas ==")
    nuevas = [(ln, t, y, g) for ln, t, y, g in cands() if est(g["n"]) == "OK" and est(g["a"]) != "OK"]
    porclase = defaultdict(list)
    for ln, t, y, g in nuevas:
        porclase[clase_token(ln, t)].append((ln, t, y, g))
    p(f"  todas: {len(nuevas)} candidatas en {len({donde(x[0]) for x in nuevas})} líneas de {len({(x[0]['doc'], x[0]['p']) for x in nuevas})} páginas")
    for k, v in sorted(porclase.items(), key=lambda kv: -len(kv[1])):
        p(f"  {len(v):4} · {k}: {len({donde(x[0]) for x in v})} líneas de {len({(x[0]['doc'], x[0]['p']) for x in v})} páginas")
    cif = porclase["cifra de una fila de saldo"]
    p("  cifras de filas de saldo, por publicación (candidatas · líneas · páginas): " + "; ".join(
        f"{d}: {sum(1 for x in cif if x[0]['doc'] == d)} · {len({donde(x[0]) for x in cif if x[0]['doc'] == d})} · {len({x[0]['p'] for x in cif if x[0]['doc'] == d})}"
        for d in sorted({x[0]["doc"] for x in cif})))
    p("  cifras de filas de saldo: una candidata por token (cada cifra se acepta con un solo ejercicio): "
      f"{len({(donde(x[0]), x[1]['k']) for x in cif}) == len(cif)}")
    p("  ejercicio aceptado frente al de la publicación (E): " + str(dict(sorted(Counter(
        f"E{int(y) - N.publicacion(ln['doc']):+d}".replace("E+0", "E") for ln, t, y, g in cif).items()))))
    an = porclase["año de la fecha del propio rótulo, en una fila de saldo"]
    p(f"  años de la fecha en una fila de saldo: en líneas que además llevan cifras del saldo aceptadas: {sum(1 for x in an if donde(x[0]) in {donde(z[0]) for z in cif})}; "
      f"en líneas sin ninguna cifra aceptada: {sum(1 for x in an if donde(x[0]) not in {donde(z[0]) for z in cif})}")
    for ln, t, y, g in an:
        if donde(ln) not in {donde(z[0]) for z in cif}:
            p(f"    {donde(ln)} · «{t['tok']}» declarado {y} · «{corta(ln['l'], 110)}»")

    # ------------------------------------------------------------------ Q2
    p()
    p("== Q2. Transiciones del estado de la fila (candidatas G, todas las páginas), por la dimensión que las causa ==")
    tr = defaultdict(list)
    for ln, t, y, g in cands():
        ea, en = est(g["a"]), est(g["n"])
        if ea != en:
            tr[(ea, en)].append((ln, t, y, g))
    for (ea, en), v in sorted(tr.items()):
        p(f"  {ea} → {en}: {len(v)} (en páginas del grupo: {sum(1 for x in v if x[0]['g'])})")
        c = Counter()
        ej = defaultdict(list)
        for ln, t, y, g in v:
            dif = [d for d in H.DIMS if g["a"][DIM[d]] != g["n"][DIM[d]]]
            clave = " + ".join(f"{d} {g['a'][DIM[d]]}→{g['n'][DIM[d]]}" for d in dif)
            if "ejercicio" in dif:
                clave += " · " + ("regla de la fila con fecha" if por_regla_de_fila(g["dn"]["ejercicio"]) else "sin la regla de la fila")
            c[clave] += 1
            ej[clave].append(ln)
        for k, n in sorted(c.items(), key=lambda kv: -kv[1]):
            ep = sum(1 for ln in ej[k] if (ln["doc"], ln["p"]) in ESTADOS_PATRIMONIO)
            p(f"    {n:5} · {k} · en las diez páginas del estado de cambios en el patrimonio: {ep} · {paginas(ej[k], 6)}")

    # ------------------------------------------------------------------ Q3
    p()
    p("== Q3. Cambios de «ejercicio» que no vienen de la regla de la fila con fecha ==")
    ce = [(ln, t, y, g) for ln, t, y, g in cands() if g["a"][DIM["ejercicio"]] != g["n"][DIM["ejercicio"]]]
    regla = [x for x in ce if por_regla_de_fila(x[3]["dn"]["ejercicio"])]
    resto = [x for x in ce if not por_regla_de_fila(x[3]["dn"]["ejercicio"])]
    p(f"  cambios de «ejercicio»: {len(ce)}; por la regla de la fila con fecha: {len(regla)}; los demás: {len(resto)}")
    enp = [x for x in resto if (x[0]["doc"], x[0]["p"]) in ESTADOS_PATRIMONIO]
    fuera = [x for x in resto if (x[0]["doc"], x[0]["p"]) not in ESTADOS_PATRIMONIO]
    p(f"  de los demás, en las diez páginas del estado de cambios en el patrimonio: {len(enp)}; "
      f"transiciones: {dict(Counter(x[3]['a'][DIM['ejercicio']] + '→' + x[3]['n'][DIM['ejercicio']] for x in enp))}; "
      f"fila OK en C16: {sum(1 for x in enp if est(x[3]['n']) == 'OK')}")
    p(f"  en otras páginas: {len(fuera)} (en páginas del grupo: {sum(1 for x in fuera if x[0]['g'])}); fila OK en C16: {sum(1 for x in fuera if est(x[3]['n']) == 'OK')}; "
      f"fila OK en C14: {sum(1 for x in fuera if est(x[3]['a']) == 'OK')}")
    vistos = OrderedDict()
    for ln, t, y, g in fuera:
        vistos.setdefault(donde(ln), [ln, Counter()])[1][g["a"][DIM["ejercicio"]] + "→" + g["n"][DIM["ejercicio"]]] += 1
    for k, (ln, c) in vistos.items():
        p(f"    {k} g={ln['g']} · {dict(c)} · «{corta(ln['l'], 100)}»")

    # ------------------------------------------------------------------ Q4
    p()
    p("== Q4. La regla de la fila con fecha frente a una cabecera con columnas de ejercicio que C14 reconocía ==")
    p("  (líneas en las que la regla da el ejercicio y C14 decidía el «ejercicio» por una columna reconocida: OK o FALLO en C14)")
    q4 = OrderedDict()
    for ln in L:
        if ln["a_rot"] is None:
            continue
        for t in ln["toks"]:
            for y, g in t["G"].items():
                ea = g["a"][DIM["ejercicio"]]
                if ea in "OF" and por_regla_de_fila(g["dn"]["ejercicio"]):
                    r = q4.setdefault(donde(ln), [ln, Counter(), set()])
                    r[1][ea + "→" + g["n"][DIM["ejercicio"]]] += 1
                    r[2].add(plantilla(g["da"]["ejercicio"])[:60])
    cl = Counter(clase_linea(r[0]) for r in q4.values())
    p(f"  líneas: {len(q4)} (en páginas del grupo: {sum(1 for r in q4.values() if r[0]['g'])}); por clase: {dict(cl)}")
    p(f"  candidatas: {dict(sum((r[1] for r in q4.values()), Counter()))}")
    for k, (ln, c, m) in q4.items():
        p(f"    {k} g={ln['g']} · {clase_linea(ln).split(' (')[0]} · {dict(c)} · «{corta(ln['l'], 105)}»")

    # ------------------------------------------------------------------ Q5
    p()
    p("== Q5. Líneas en que la regla se dispara y que no son filas de saldo ni recuentos con fecha, por tipo ==")
    otras = [ln for ln in L if ln["a_rot"] is not None and clase_linea(ln).startswith("otra")]
    tipos = Counter()
    for ln in otras:
        s = re.sub(r"\s+", " ", ln["l"]).strip()
        toks_no_anio = [t["tok"] for t in ln["toks"] if not es_anio(t["tok"])]
        if re.match(r"(?:Main offices and positions held as at|Principaux mandats et fonctions au) ", s):
            k = "epígrafe «Main offices and positions held as at…» / «Principaux mandats et fonctions au…»"
        elif re.fullmatch(r"(?:as at December 31, 20\d\d|au 31 décembre 20\d\d)", s) and (ln["doc"], ln["p"]) in ESTADOS_PATRIMONIO:
            k = "continuación del título del estado de cambios en el patrimonio"
        elif re.fullmatch(r"as at December 31, 20\d\d \d{3}", s):
            k = "entrada de sumario («as at December 31, AAAA · página»)"
        elif re.match(r"(?:Status as at|Situation au) ", s):
            k = "título «Status as at…» / «Situation au…»"
        else:
            k = "otra línea de prosa, de título o de cabecera"
        tipos[(k, "grupo" if ln["g"] else "no grupo")] += 1
    p(f"  líneas: {len(otras)} (en páginas del grupo: {sum(ln['g'] for ln in otras)})")
    for (k, gr), v in sorted(tipos.items(), key=lambda kv: (kv[0][0], kv[0][1])):
        p(f"  {v:4} · {k} · {gr}")

    # ------------------------------------------------------------------ Q6
    p()
    p("== Q6. S2: líneas de las páginas del grupo en las que `rotulos_sin_rotulo` devuelve algún rótulo y hay dos tokens o más ==")
    q6 = [ln for ln in L if ln["g"] and ln["rsr"] and len(ln["toks"]) >= 2]
    p(f"  líneas con rótulos contiguos en páginas del grupo: {sum(1 for ln in L if ln['g'] and ln['rsr'])}; con un solo token: "
      f"{sum(1 for ln in L if ln['g'] and ln['rsr'] and len(ln['toks']) == 1)}; con dos o más: {len(q6)}")
    cambia = [ln for ln in q6 if any(g["a"] != g["n"] for t in ln["toks"] for g in t["G"].values())]
    p(f"  de las de dos o más, con algún estado distinto entre C14 y C16 (candidatas G): {len(cambia)}: " + "; ".join(f"{donde(ln)} «{corta(ln['l'], 50)}»" for ln in cambia))
    for ln in q6:
        p(f"    {donde(ln)} · «{corta(ln['l'], 70)}» · rótulos contiguos: {[r[:40] for r in ln['rsr']]}")

    # ------------------------------------------------------------------ Q7
    p()
    p("== Q7. S3: cambios de «unidad» entre C14 y C16 ==")
    cu = [(ln, t, y, g) for ln, t, y, g in cands() if g["a"][DIM["unidad"]] != g["n"][DIM["unidad"]]]
    p(f"  candidatas: {len(cu)} en {len({donde(x[0]) for x in cu})} líneas (en páginas del grupo: {sum(1 for x in cu if x[0]['g'])}); "
      f"transición de la fila: {dict(Counter(est(x[3]['a']) + ' → ' + est(x[3]['n']) for x in cu))}")
    vistos = OrderedDict()
    for ln, t, y, g in cu:
        vistos.setdefault((donde(ln), t["tok"]), (ln, g["dn"]["unidad"]))
    for (k, tok), (ln, m) in vistos.items():
        p(f"    {k} · token «{tok}» · «{corta(ln['l'], 80)}» · {m[:110]}")

    # ------------------------------------------------------------------ Q8
    p()
    p("== Q8. S7 d: el epígrafe de las marcas en las cinco publicaciones (perímetro en C16 de cada línea con cifras, declarada del grupo) ==")
    RX = re.compile(r"(?i)unamortized brands|marques non amorti")
    for doc in sorted(N.fuentes):
        halladas = []
        for pag in range(1, N.paginas(doc) + 1):
            lineas = N.lineas(doc, pag)
            ini = next((i for i, l in enumerate(lineas) if RX.search(l) and re.search(r"(?i)sensitivity|sensibilité", l)), None)
            if ini is not None and any((doc, pag, k) in porlinea and porlinea[(doc, pag, k)]["g"] for k in range(ini, len(lineas))):
                halladas.append((pag, ini, lineas))
        for pag, ini, lineas in halladas:
            p(f"  {doc} p.{pag}, desde la línea {ini + 1} «{corta(lineas[ini], 80)}»")
            for k in range(ini, len(lineas)):
                if k > ini and re.match(r"\s*(?:\d\s+)?NOTE \d", lineas[k]):
                    break
                ln = porlinea.get((doc, pag, k))
                if not ln or ln["pie"]:
                    if lineas[k].strip():
                        p(f"      l.{k + 1} · (sin cifras) · «{corta(lineas[k], 100)}»")
                    continue
                per = Counter()
                mot = set()
                for t in ln["toks"]:
                    for y, g in t["G"].items():
                        per[g["n"][DIM["perimetro"]]] += 1
                        if g["n"][DIM["perimetro"]] != "O":
                            mot.add(plantilla(g["dn"]["perimetro"])[:70] + (" «" + (re.findall(r"«([^»]*)»", g["dn"]["perimetro"]) or [""])[0][:30] + "»"))
                filas = Counter(est(g["n"]) for t in ln["toks"] for g in t["G"].values())
                p(f"      l.{k + 1} · {len(ln['toks'])} tokens · perímetro {dict(per)} · fila {dict(filas)} · «{corta(ln['l'], 70)}»" + (" · " + "; ".join(sorted(mot)) if mot else ""))

    # ------------------------------------------------------------------ Q9
    p()
    p("== Q9. Decisión (b): candidatas en las que solo el perímetro impide el OK por la regla de grupos de columnas (C16) ==")
    q9 = [(ln, t, y, g) for ln, t, y, g in cands() if "la cabecera repite los ejercicios" in g["dn"]["perimetro"]
          and all(x in "ON" for j, x in enumerate(g["n"]) if j != DIM["perimetro"])]
    p(f"  candidatas: {len(q9)}; estado de la fila en C14: {dict(Counter(est(x[3]['a']) for x in q9))}; perímetro en C14: {dict(Counter(x[3]['a'][DIM['perimetro']] for x in q9))}")
    pp = OrderedDict()
    for ln, t, y, g in q9:
        pp.setdefault((ln["doc"], ln["p"]), []).append((ln, t, y, g))
    for (doc, pag), v in pp.items():
        lin = sorted({x[0]["i"] for x in v})
        p(f"    {doc} p.{pag}: {len(v)} candidatas en {len(lin)} líneas · primera: «{corta(porlinea[(doc, pag, lin[0])]['l'], 70)}»"
          + (f" · token «{v[0][1]['tok']}» declarado {v[0][2]}" if len(v) <= 2 else ""))

    # ------------------------------------------------------------------ Q10
    p()
    p("== Q10. «Ejercicio» en el universo de la revisión n.º 6 (líneas con rótulo, sin años sueltos ni pies) ==")
    u6 = []
    for ln in L:
        idi = N.idioma(ln["doc"])
        rot = ln["rot16"]
        if not rot or V.es_numero(rot, idi) or ln["pie"] or all(re.fullmatch(r"20\d\d", t) or t in V.PLACEHOLDER for t in V.tokens_numericos(ln["l"], idi)):
            continue
        for t in ln["toks"]:
            if re.fullmatch(r"20\d\d", t["tok"]):
                continue
            for y, g in t["G"].items():
                u6.append((ln, t, y, g))
    ej = Counter()
    for ln, t, y, g in u6:
        x, z = g["a"][DIM["ejercicio"]], g["n"][DIM["ejercicio"]]
        if x != z:
            ej[(x + "→" + z, "fila OK en C16" if est(g["n"]) == "OK" else "fila no OK en C16", "regla de la fila" if por_regla_de_fila(g["dn"]["ejercicio"]) else "sin la regla")] += 1
    for k, v in sorted(ej.items()):
        p(f"  {v:5} · ejercicio {k[0]} · {k[1]} · {k[2]}")
    fo = [(ln, t, y, g) for ln, t, y, g in u6 if g["a"][DIM["ejercicio"]] == "F" and g["n"][DIM["ejercicio"]] == "O"]
    c = Counter((plantilla(g["da"]["ejercicio"])[:58], clase_linea(ln).split(" (")[0]) for ln, t, y, g in fo)
    p(f"  ejercicio F→O: {len(fo)}; por motivo de C14 y clase de línea:")
    for k, v in sorted(c.items(), key=lambda kv: -kv[1]):
        p(f"    {v:4} · {k[0]} · {k[1]}")
    p("  ejercicio F→O, por página: " + paginas([x[0] for x in fo], 40))


if __name__ == "__main__":
    main()
