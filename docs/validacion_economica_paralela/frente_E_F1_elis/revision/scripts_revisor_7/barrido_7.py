"""Revisión n.º 7 (frente E · F1 · Elis). Barrido propio del verificador de C14. No modifica nada del autor.

Qué recorre: las páginas que el verificador de C14 acepta como del grupo (cabecera de estados consolidados o de resultados
del grupo) en los cinco PDF. En las demás el perímetro queda siempre PENDIENTE y ninguna candidata puede quedar OK; sus
transiciones las da el barrido de la revisión n.º 6, que se ha vuelto a ejecutar aparte.

Candidatas: cada token numérico (que no sea un año ni un marcador) de cada línea, declarado como lo haría una cifra del
grupo: «mm EUR» (o «%» si el literal lo lleva), «consolidado IFRS, grupo Elis», modo «dos_columnas», con el ejercicio de la
publicación (E), E−1 y E−2, y con la edición que la regla exige. A diferencia del barrido de la revisión n.º 6, entran
también las líneas SIN rótulo (las que empiezan por un número: la cifra de una fila cuyo rótulo está en otra línea).

Qué anota de cada token:
  - el resultado de comprobar_tabla en C14, en C13 y en cinco variantes de C14 cambiadas en memoria (arnes7.VARIANTES);
  - el diagnóstico del propio verificador de C14: columnas de ejercicio que reconoce en la cabecera, método de asignación,
    distancia, periodo de los ejercicios repetidos, línea de cabecera de «otra tabla», rótulo unido y título que decide;
  - una lectura propia con otro motor (MuPDF, geo7.py): pila de cabecera de la columna del número, ejercicios y palabras
    ajenas que nombra, y títulos por tipografía por encima de la tabla.

Uso: python3 -I barrido_7.py --raiz <munger_v2_r1> --c13 <frente C13> --c14 <frente C14> --pylibs <carpeta con pymupdf>
        --todas <archivo.jsonl.gz> --salida <resumen.txt> [--procesos 4]
"""
import argparse
import gzip
import json
import re
import sys
import warnings
from collections import Counter
from multiprocessing import Pool
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import arnes7  # noqa: E402
import geo7  # noqa: E402

_V, _DOCS = {}, {}
INICIAL = {"OK": "O", "PENDIENTE": "P", "FALLO": "F", "NO_APLICA": "N", "NO_EVALUADO": "E"}
DETALLES = ("ejercicio", "unidad", "perimetro", "edicion")


def versiones(cfg):
    if not _V:
        _V["c14"] = arnes7.Version(cfg["c14"], cfg["raiz"], "C14")
        _V["c13"] = arnes7.Version(cfg["c13"], cfg["raiz"], "C13")
        for v in arnes7.VARIANTES:
            _V[v] = arnes7.Version(cfg["c14"], cfg["raiz"], "C14", v)
        sys.path.insert(0, cfg["pylibs"])
        warnings.simplefilter("ignore")
        import pymupdf
        _V["fitz"] = pymupdf
    return _V


def geometria(cfg, doc, p, lineas):
    V = versiones(cfg)
    if doc not in _DOCS:
        _DOCS[doc] = V["fitz"].open(str(V["c14"].pdf(doc)))
    filas = geo7.filas_de_pagina(geo7.palabras_de_pagina(_DOCS[doc][p - 1]))
    mapa = geo7.casar_lineas(lineas, filas)
    # segunda vuelta: una línea de pdftotext que reúne dos o tres filas geométricas contiguas (líneas base algo distintas)
    usadas = set(mapa.values())
    virtuales = {}
    for i, l in enumerate(lineas):
        if i in mapa or not l.strip():
            continue
        k = geo7.sin_espacios(l)
        hecho = False
        for ancho in (2, 3):
            for n in range(len(filas) - ancho + 1):
                grupo = list(range(n, n + ancho))
                if any(g in usadas for g in grupo) or filas[n + ancho - 1]["base"] - filas[n]["base"] > 7:
                    continue
                ws = sorted([w for g in grupo for w in filas[g]["w"]], key=lambda w: w.x0)
                if "".join(w.t for w in ws) == k:
                    virtuales[i] = ({"base": filas[n]["base"], "w": ws, "cuerpo": max(w.cuerpo for w in ws)}, n)
                    usadas.update(grupo)
                    hecho = True
                    break
            if hecho:
                break
    return filas, mapa, virtuales


def titulo_que_decide(m, lineas, i, j, previas, idioma):
    """Réplica, solo para anotar, del recorrido de titulo_de_pais_encima_v2 de C14: qué línea corta la búsqueda del título
    del bloque y por qué criterio («unidades», «titulo» en mayúsculas o «numerado»), y si está en la página anterior."""
    if j is not None and j < i:
        resto = lineas[j]
        for rx, _ in m.UNIDAD_RX:
            resto = rx.sub("", resto)
        resto = re.sub(r"[()]", "", resto).strip()
        if resto and not re.search(r"\d", resto) and m.PAIS_O_SEGMENTO_TITULO.fullmatch(resto):
            return ["unidades", resto, j]
    for k in range(i - 1, -1, -1):
        t = lineas[k].strip()
        if m.es_titulo(t):
            return ["titulo", t, k]
        if m.es_encabezado_numerado(t, idioma):
            return ["numerado", t, k]
    for n, t in enumerate(reversed([x.strip() for x in previas])):
        if m.es_titulo(t):
            return ["titulo", t, -1 - n]
        if m.es_encabezado_numerado(t, idioma):
            return ["numerado", t, -1 - n]
    return [None, None, None]


def pagina(arg):
    cfg, doc, p = arg
    V = versiones(cfg)
    v14 = V["c14"]
    m = v14.m
    idioma, E = v14.fuentes[doc]["idioma"], v14.fuentes[doc]["ejercicio"]
    lineas = v14.lineas(doc, p)
    grupo = any(m.GRUPO_RX.search(l) for l in [x for x in lineas if x.strip()][:8])
    if not grupo:
        return doc, p, False, []
    previas = v14.lineas(doc, p - 1) if p > 1 else []
    filas, mapa, virtuales = geometria(cfg, doc, p, lineas)
    out = []
    for i, l in enumerate(lineas):
        toks = m.tokens_numericos(l, idioma)
        sp = m.spans_numericos(l, idioma)
        if not toks or sp is None:
            continue
        if all(re.fullmatch(r"20\d\d", t) or t in m.PLACEHOLDER for t in toks):
            continue
        if re.search(r"Universal Registration Document|enregistrement universel", l):
            continue
        rot = m.rotulo(l)
        con_rotulo = bool(rot) and not m.es_numero(rot, idioma)
        etq, occ = arnes7.etiqueta_de_linea(lineas, i)
        # diagnóstico de la línea con las funciones del propio verificador de C14
        _, j = m.unidad_declarada(lineas, i)
        zona = m.zona_de_cabecera(lineas, i, idioma)
        h = m.cabecera_de_otra_tabla(lineas, j, i, idioma) if j is not None else None
        cols_ej = m.columnas_de_cabecera(lineas, zona, ("ejercicio",)) if zona else []
        cols3 = m.columnas_de_cabecera(lineas, zona, ("ejercicio", "variacion", "notas")) if zona else []
        periodo = m.periodo_de_ejercicios([t for _, _, t in cols_ej])
        tit = titulo_que_decide(m, lineas, i, j, previas, idioma)
        corto = m.titulo_corto_de_tabla(lineas, i, j, idioma)
        rot_multi = m.rotulo_multilinea(lineas, i, idioma)
        # geometría de la fila
        if i in mapa:
            gfila, n_desde = filas[mapa[i]], mapa[i]
        elif i in virtuales:
            gfila, n_desde = virtuales[i]
        else:
            gfila, n_desde = None, None
        for idx, tok in enumerate(toks):
            if tok in m.PLACEHOLDER or re.fullmatch(r"20\d\d", tok):
                continue
            try:
                val = m.valor(tok, idioma)
            except ValueError:
                continue
            rec = {"doc": doc, "p": p, "i": i, "idx": idx, "n": len(toks), "tok": tok, "rot": rot[:90], "cr": int(con_rotulo),
                   "a0": sp[idx][0], "a1": sp[idx][1], "j": j, "h": h, "lh": lineas[h].strip()[:140] if h is not None else None,
                   "nz": len(zona), "ej": [[c, t] for c, _, t in cols_ej], "nc3": len(cols3), "per": periodo, "tit": tit,
                   "corto": corto, "rm": rot_multi[:160] if rot_multi != rot else None}
            if cols3:
                clave, txt, metodo, centro, d = m.asignar_columna(sp, cols3, idx, 14, True)
                rec["asig"] = [clave, txt, metodo, centro, d]
                if len(cols3) == len(sp):
                    cen = [(a + b) / 2 for a, b in sp]
                    rec["orden_max"] = max(abs(c - k[0]) for c, k in zip(cen, cols3))
                    rec["orden_bruto"] = [cols3[idx][1], cols3[idx][2]]
            # lectura propia
            if gfila is not None:
                caja = geo7.caja_de_token(l, sp[idx][0], sp[idx][1], gfila)
                if caja:
                    pila, cima = geo7.pila_de_cabecera(filas, n_desde, caja[0], caja[1])
                    rec["g"] = {"x": [round(caja[0], 1), round(caja[1], 1)], "pila": [x["texto"][:60] for x in pila],
                                "anios": geo7.ejercicios_de_pila(pila), "ajenas": geo7.ajenas_de_pila(pila),
                                "tit": [[t[0][:70], t[1], int(t[2])] for t in geo7.titulos_encima(filas, cima, gfila["cuerpo"], 0)],
                                "negrita": int(all(w.negrita for w in gfila["w"]))}
            cands = []
            for anio in (E, E - 1, E - 2):
                f = arnes7.fila("B7", doc=doc, pagina=p, anio=anio, etiqueta=etq, ocurrencia=occ, pos=idx - len(toks), literal=tok,
                                valor_publicado=str(val), unidad="%" if "%" in tok else "mm EUR",
                                edicion=arnes7.edicion_de_la_regla(anio, E, v14.ejercicios))
                c = {"anio": anio, "ed": f["edicion"]}
                r14 = v14.tabla(f)
                d14 = r14["dimensiones"]
                c["c14"] = "".join(INICIAL[d14[k]["estado"]] for k in arnes7.DIMS)
                c["d14"] = {k: d14[k].get("detalle", "") for k in DETALLES if d14[k]["estado"] != "NO_APLICA"}
                r13 = V["c13"].tabla(f)
                d13 = r13["dimensiones"]
                c["c13"] = "".join(INICIAL[d13[k]["estado"]] for k in arnes7.DIMS)
                c["d13"] = {k: d13[k].get("detalle", "") for k in DETALLES if d13[k]["estado"] != d14[k]["estado"]}
                for v in arnes7.VARIANTES:
                    dv = V[v].tabla(f)["dimensiones"]
                    e = "".join(INICIAL[dv[k]["estado"]] for k in arnes7.DIMS)
                    if e != c["c14"]:
                        c[v] = e
                        c["d_" + v] = {k: dv[k].get("detalle", "") for k in DETALLES if dv[k]["estado"] != d14[k]["estado"]}
                cands.append(c)
            rec["c"] = cands
            out.append(rec)
    return doc, p, True, out


def estado_fila(e):
    return "FALLO" if ("F" in e or "E" in e) else "PENDIENTE" if "P" in e else "OK"


def equivalencia(carpeta, raiz, nombre):
    """comprobar_tabla (módulo) frente a la ejecución oficial guardada por el autor, sobre las filas de tabla reales."""
    v = arnes7.Version(carpeta, raiz, nombre)
    of = {r["id"]: r for r in json.loads((Path(carpeta) / "resultados" / "verificacion_cifras.json").read_text(encoding="utf-8"))["cifras"]}
    n = dif = 0
    for f in arnes7.leer_csv(carpeta):
        if f["tipo"] != "tabla":
            continue
        n += 1
        r = v.tabla(f)
        if any((r["dimensiones"][k]["estado"], r["dimensiones"][k]["detalle"]) !=
               (of[f["id"]]["dimensiones"][k]["estado"], of[f["id"]]["dimensiones"][k]["detalle"]) for k in arnes7.DIMS):
            dif += 1
    return n, dif


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raiz", required=True)
    ap.add_argument("--c13", required=True)
    ap.add_argument("--c14", required=True)
    ap.add_argument("--pylibs", required=True)
    ap.add_argument("--todas", required=True, type=Path)
    ap.add_argument("--salida", required=True, type=Path)
    ap.add_argument("--procesos", type=int, default=4)
    a = ap.parse_args()
    cfg = {"raiz": a.raiz, "c13": a.c13, "c14": a.c14, "pylibs": a.pylibs}
    S = []
    w = S.append
    w("Barrido propio de la revisión n.º 7 · C13 → C14 y variantes de C14 · páginas del grupo\n")
    for nom, carpeta in (("C14", a.c14), ("C13", a.c13)):
        n, dif = equivalencia(carpeta, a.raiz, "equiv" + nom)
        w(f"Equivalencia comprobar_tabla (módulo) = ejecución oficial guardada en {nom}: {n} filas de tabla reales, {dif} con algún estado o detalle distinto")
    v14 = arnes7.Version(a.c14, a.raiz, "C14")
    tareas = [(cfg, doc, p) for doc in sorted(v14.fuentes) for p in range(1, v14.paginas(doc) + 1)]
    with Pool(a.procesos) as pool:
        res = pool.map(pagina, tareas, chunksize=4)
    toks, pags, pags_g = [], Counter(), Counter()
    for doc, p, grupo, out in res:
        pags[doc] += 1
        pags_g[doc] += int(grupo)
        toks.extend(out)
    a.todas.parent.mkdir(parents=True, exist_ok=True)
    with gzip.open(a.todas, "wt", encoding="utf-8") as g:
        for t in toks:
            g.write(json.dumps(t, ensure_ascii=False) + "\n")
    w("\nPáginas recorridas y, de ellas, aceptadas como del grupo por el verificador de C14:")
    for doc in sorted(pags):
        w(f"  {doc}: {pags[doc]} páginas, {pags_g[doc]} del grupo")
    con = [t for t in toks if t["cr"]]
    w(f"\nTokens: {len(toks)} ({len(con)} en líneas con rótulo y {len(toks) - len(con)} en líneas sin rótulo); candidatas (token × E, E−1, E−2): {3 * len(toks)}")
    w(f"Con lectura propia (MuPDF): {sum(1 for t in toks if 'g' in t)} de {len(toks)} ({100 * sum(1 for t in toks if 'g' in t) / len(toks):.1f} %)")
    for titulo, sel in (("líneas con rótulo (el universo del barrido de la revisión n.º 6)", con), ("líneas sin rótulo", [t for t in toks if not t["cr"]])):
        w(f"\n== Estado de la fila, {titulo}: C13 → C14 ==")
        tr = Counter((estado_fila(c["c13"]), estado_fila(c["c14"])) for t in sel for c in t["c"])
        for (x, y), n in sorted(tr.items()):
            w(f"  {x:<9} → {y:<9} {n:7d}" + ("" if x == y else "   ← cambia"))
        w(f"== Transiciones por dimensión, {titulo}: C13 → C14 ==")
        trd = Counter()
        for t in sel:
            for c in t["c"]:
                for k, x, y in zip(arnes7.DIMS, c["c13"], c["c14"]):
                    if x != y:
                        trd[(k, x, y)] += 1
        for (k, x, y), n in sorted(trd.items()):
            w(f"  {k}: {x} → {y}: {n}")
        if not trd:
            w("  ninguna")
    w("\n== Variantes de C14 frente a C14 (todas las líneas): candidatas cuyo estado cambia, por dimensión ==")
    for v in arnes7.VARIANTES:
        trd = Counter()
        for t in toks:
            for c in t["c"]:
                if v in c:
                    for k, x, y in zip(arnes7.DIMS, c["c14"], c[v]):
                        if x != y:
                            trd[(k, x, y)] += 1
        w(f"  {v}: " + (", ".join(f"{k} {x}→{y}: {n}" for (k, x, y), n in sorted(trd.items())) or "ningún cambio"))
    a.salida.parent.mkdir(parents=True, exist_ok=True)
    a.salida.write_text("\n".join(S) + "\n", encoding="utf-8")
    print("\n".join(S))
    return 0


if __name__ == "__main__":
    sys.exit(main())
