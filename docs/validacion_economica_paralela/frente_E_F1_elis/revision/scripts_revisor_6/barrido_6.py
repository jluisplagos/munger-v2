"""Revisión n.º 6 (frente E · F1 · Elis). Barrido diferencial propio del verificador: C11 (congelado de la revisión n.º 5)
frente a C13 (congelado de esta revisión). No modifica nada del autor.

Diferencias con el barrido de la revisión n.º 5 (barrido_tablas.py):
  - compara C11 con C13 (el anterior comparaba C8 con la versión nueva), así que las transiciones son las de C12;
  - recorre TODAS las páginas de los cinco PDF, no solo las que el verificador acepta como del grupo (se marca cuáles lo son);
  - declara cada token con tres ejercicios: el de la publicación (E), el anterior (E−1) y E−2 (columnas de apertura);
  - llama a comprobar_tabla, la función que usa la ejecución oficial para cada fila (con la página anterior y la edición
    de la columna), no a las funciones por dimensión;
  - guarda todas las candidatas (JSONL comprimido) para que las clases se cuenten después con lecturas propias
    (lectura_geometrica.py, clases_6.py).

Cada candidata es un token numérico de una línea con rótulo, declarado como lo haría una cifra del grupo: «mm EUR» (o «%»
si el literal lo lleva), «consolidado IFRS, grupo Elis», modo «dos_columnas» y la edición que la regla exige para ese
ejercicio en esa publicación.

Uso: python3 -I barrido_6.py --raiz <munger_v2_r1> --anterior C11=<frente C11> --nueva C13=<frente C13>
        --todas <archivo.jsonl.gz> --salida <resumen.txt> [--procesos 4]
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
from arnes6 import DIM5, DIMS, Modulo, edicion_que_exige_la_regla, etiqueta_de_linea, fila, leer_csv  # noqa: E402

_M = {}


def modulos(cfg):
    if not _M:
        _M["n"] = Modulo(cfg["nueva"], cfg["raiz"], "verificador_nuevo")
        _M["a"] = Modulo(cfg["anterior"], cfg["raiz"], "verificador_anterior")
    return _M["n"], _M["a"]


def pagina(arg):
    cfg, doc, p = arg
    Mn, Ma = modulos(cfg)
    m = Mn.m
    idioma, E = Mn.fuentes[doc]["idioma"], Mn.fuentes[doc]["ejercicio"]
    lineas = Mn.texto(doc, p).splitlines()
    grupo = any(m.GRUPO_RX.search(l) for l in [x for x in lineas if x.strip()][:8])
    out = []
    for i, l in enumerate(lineas):
        toks = m.tokens_numericos(l, idioma)
        sp = m.spans_numericos(l, idioma)
        if not toks or sp is None:
            continue
        rot = m.rotulo(l)
        if not rot or m.es_numero(rot, idioma) or all(re.fullmatch(r"20\d\d", t) or t in m.PLACEHOLDER for t in toks):
            continue
        if re.search(r"Universal Registration Document|enregistrement universel", l):
            continue
        etq, occ = etiqueta_de_linea(lineas, i)
        for idx, tok in enumerate(toks):
            if tok in m.PLACEHOLDER or re.fullmatch(r"20\d\d", tok):
                continue
            try:
                val = m.valor(tok, idioma)
            except ValueError:
                continue
            for anio in (E, E - 1, E - 2):
                f = fila("B6", doc=doc, pagina=p, anio=anio, etiqueta=etq, ocurrencia=occ, pos=idx - len(toks), literal=tok,
                         valor_publicado=str(val), unidad="%" if "%" in tok else "mm EUR",
                         edicion=edicion_que_exige_la_regla(anio, E, Mn.ejercicios))
                rn, ra = Mn.tabla(f), Ma.tabla(f)
                out.append({"doc": doc, "p": p, "g": int(grupo), "i": i, "idx": idx, "n": len(toks), "tok": tok, "anio": anio,
                            "a0": sp[idx][0], "a1": sp[idx][1], "rot": rot[:80], "ed": f["edicion"],
                            "n_e": [rn["dimensiones"][k]["estado"] for k in DIMS], "a_e": [ra["dimensiones"][k]["estado"] for k in DIMS],
                            "n_d": {k: rn["dimensiones"][k].get("detalle", "") for k in ("ejercicio", "unidad", "perimetro", "edicion")
                                    if rn["dimensiones"][k]["estado"] not in ("NO_APLICA",)},
                            "a_d": {k: ra["dimensiones"][k].get("detalle", "") for k in ("ejercicio", "unidad", "perimetro", "edicion")
                                    if ra["dimensiones"][k]["estado"] not in ("OK", "NO_APLICA")}})
    return doc, p, grupo, out


def equivalencia(carpeta, raiz, nombre):
    """Módulo frente a ejecución oficial, sobre las filas de tabla del CSV de esa versión: estado y detalle de cada dimensión."""
    M = Modulo(carpeta, raiz, nombre)
    of = {r["id"]: r for r in json.loads((Path(carpeta) / "resultados" / "verificacion_cifras.json").read_text(encoding="utf-8"))["cifras"]}
    n = dif = 0
    for f in leer_csv(carpeta):
        if f["tipo"] != "tabla":
            continue
        n += 1
        r = M.tabla(f)
        if any((r["dimensiones"][k]["estado"], r["dimensiones"][k]["detalle"]) !=
               (of[f["id"]]["dimensiones"][k]["estado"], of[f["id"]]["dimensiones"][k]["detalle"]) for k in DIMS):
            dif += 1
    return n, dif


def plantilla(motivo):
    """Motivo sin sus partes variables, para agrupar."""
    t = re.sub(r"«[^»]*»", "«…»", motivo)
    t = re.sub(r"\(línea \d+\)|línea \d+", "línea N", t)
    t = re.sub(r"\b20\d\d\b", "AAAA", t)
    return re.sub(r"\([^)]*…\)", "(…)", t)[:120]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raiz", required=True)
    ap.add_argument("--anterior", required=True, help="NOMBRE=carpeta")
    ap.add_argument("--nueva", required=True, help="NOMBRE=carpeta")
    ap.add_argument("--todas", required=True, type=Path)
    ap.add_argument("--salida", required=True, type=Path)
    ap.add_argument("--procesos", type=int, default=4)
    a = ap.parse_args()
    (na, ca), (nn, cn) = a.anterior.split("=", 1), a.nueva.split("=", 1)
    cfg = {"raiz": a.raiz, "nueva": cn, "anterior": ca}
    S = []
    w = S.append
    w(f"Barrido diferencial propio · versión anterior {na} · versión nueva {nn}\n")
    for nom, carpeta in ((nn, cn), (na, ca)):
        n, dif = equivalencia(carpeta, a.raiz, "equiv_" + nom)
        w(f"Equivalencia comprobar_tabla (módulo) = ejecución oficial en {nom}: {n} filas de tabla del CSV real, {dif} con algún estado o detalle distinto")
    Mn, _ = modulos(cfg)
    tareas = [(cfg, doc, p) for doc in sorted(Mn.fuentes) for p in range(1, Mn.paginas(doc) + 1)]
    with Pool(a.procesos) as pool:
        res = pool.map(pagina, tareas, chunksize=6)
    cand, pags, pags_g = [], Counter(), Counter()
    for doc, p, grupo, out in res:
        pags[doc] += 1
        pags_g[doc] += int(grupo)
        cand.extend(out)
    a.todas.parent.mkdir(parents=True, exist_ok=True)
    with gzip.open(a.todas, "wt", encoding="utf-8") as g:
        for c in cand:
            g.write(json.dumps(c, ensure_ascii=False) + "\n")
    w("\nPáginas recorridas (todas) y, de ellas, con cabecera aceptada como del grupo:")
    for doc in sorted(pags):
        w(f"  {doc}: {pags[doc]} páginas, {pags_g[doc]} del grupo")
    ng = sum(c["g"] for c in cand)
    w(f"Candidatas evaluadas (token × ejercicio E, E−1, E−2): {len(cand)}; en páginas del grupo: {ng}")
    tokens = {(c["doc"], c["p"], c["i"], c["idx"]) for c in cand}
    w(f"Tokens distintos: {len(tokens)}; en páginas del grupo: {len({(c['doc'], c['p'], c['i'], c['idx']) for c in cand if c['g']})}")

    def est_fila(e):
        return "FALLO" if any(x in ("FALLO", "NO_EVALUADO") for x in e) else "PENDIENTE" if "PENDIENTE" in e else "OK"

    for titulo, sel in (("todas las páginas", cand), ("páginas del grupo", [c for c in cand if c["g"]])):
        w(f"\n== Estado de la fila, {titulo}: {na} → {nn} ==")
        tr = Counter((est_fila(c["a_e"]), est_fila(c["n_e"])) for c in sel)
        for (x, y), n in sorted(tr.items()):
            w(f"  {x:<9} → {y:<9} {n:7d}" + ("" if x == y else "   ← cambia"))
        w(f"\n== Transiciones por dimensión, {titulo}: {na} → {nn} ==")
        trd = Counter()
        for c in sel:
            for k, ea, en in zip(DIMS, c["a_e"], c["n_e"]):
                if ea != en:
                    trd[(k, ea, en)] += 1
        for (k, ea, en), n in sorted(trd.items()):
            w(f"  {k}: {ea} → {en}: {n}")
        if not trd:
            w("  ninguna")

    w(f"\n== Transiciones por dimensión y motivo de {nn} (todas las páginas): recuento, páginas y un ejemplo ==")
    grupos = defaultdict(list)
    for c in cand:
        for j, k in enumerate(DIMS):
            if c["a_e"][j] != c["n_e"][j]:
                mot = c["n_d"].get(k, "") if c["n_e"][j] != "OK" else "(queda OK) antes: " + c["a_d"].get(k, "")
                grupos[(k, c["a_e"][j], c["n_e"][j], plantilla(mot))].append(c)
    for (k, ea, en, pl), cs in sorted(grupos.items(), key=lambda x: (x[0][0], -len(x[1]))):
        pp = Counter(f"{c['doc']} p.{c['p']}" for c in cs)
        w(f"\n  {k}: {ea} → {en} · {len(cs)} candidatas · {len({(c['doc'], c['p'], c['i'], c['idx']) for c in cs})} tokens · {len(pp)} páginas · {pl}")
        w("     páginas: " + ", ".join(f"{q} ({n})" for q, n in pp.most_common(12)) + (" …" if len(pp) > 12 else ""))
        c = cs[0]
        w(f"     ejemplo: {c['doc']} p.{c['p']} l.{c['i'] + 1} token {c['idx'] + 1}/{c['n']} «{c['tok']}» declarado {c['anio']} · rótulo «{c['rot'][:60]}»")
    a.salida.parent.mkdir(parents=True, exist_ok=True)
    a.salida.write_text("\n".join(S) + "\n", encoding="utf-8")
    print("\n".join(S[:70]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
