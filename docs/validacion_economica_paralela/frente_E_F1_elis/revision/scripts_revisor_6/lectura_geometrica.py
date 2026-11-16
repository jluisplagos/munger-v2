"""Revisión n.º 6 (frente E · F1 · Elis). Lectura propia de cada token del barrido, con geometría y tipografía (geom.py).
No usa pdftotext para decidir ni ninguna función de decisión del autor.

Para cada token de barrido_6.py (documento, página, línea y posición en el texto con maquetación) localiza la misma
fila en la lectura de pdfminer y anota:
  cab      celdas de cabecera alineadas por la derecha con el número (en puntos) y celdas que lo solapan sin alinearse;
  años     ejercicios de cierre y de apertura que nombran las celdas alineadas;
  otras    palabras de las celdas alineadas o que solapan que no son fechas ni calificadores (otra medida, entidad o país);
  edición  «publicada» o «reexpresada» si lo dice una celda alineada;
  unidades fila de la declaración de unidades de la tabla;
  título   título de la tabla (fila corta en seminegra pegada encima de la cabecera) y encabezado de bloque más próximo
           por encima (por tipografía: seminegra o negra de 8,9 puntos o más), en la página o en las anteriores;
  rótulo   rótulo de la fila y de la fila anterior si el rótulo está partido.

Uso: python3 -I lectura_geometrica.py --raiz <munger_v2_r1> --autor <frente C13> --todas <barrido.jsonl.gz>
        --salida <lectura.jsonl.gz> [--solo-grupo] [--procesos 4]
"""
import argparse
import gzip
import json
import re
import sys
from collections import defaultdict
from multiprocessing import Pool
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import geom  # noqa: E402

_F = {}


def norm(t):
    return re.sub(r"[\s  ]+", "", t)


def encabezados(pdf, p):
    """Encabezados de bloque de la página p, de arriba abajo: (índice de fila, texto, tamaño)."""
    fs = geom.filas(geom.palabras(pdf, p))
    return [(k, f["txt"], f["size"]) for k, f in enumerate(fs) if geom.es_encabezado(f)]


def encabezado_encima(pdf, p, k, atras=8):
    """Encabezado de bloque más próximo por encima de la fila k de la página p; si la página no tiene ninguno por encima,
    el último de las páginas anteriores (hasta «atras»). Devuelve (texto, tamaño, páginas hacia atrás) o None."""
    for kk, t, s in reversed(encabezados(pdf, p)):
        if kk < k:
            return t, s, 0
    for d in range(1, atras + 1):
        if p - d < 1:
            break
        e = encabezados(pdf, p - d)
        if e:
            return e[-1][1], e[-1][2], d
    return None


def pagina(arg):
    pdf, fr, doc, p, toks = arg
    fs = geom.filas(geom.palabras(pdf, p))
    compactas = defaultdict(list)
    nums = {}
    for k, f in enumerate(fs):
        compactas[f["txt"]].append(k)
        nums[k] = geom.unir_numeros(f["ws"], fr)
    por_linea = defaultdict(list)
    for t in toks:
        por_linea[t["i"]].append(t)
    out = []
    usados = defaultdict(int)
    for i in sorted(por_linea):
        ts = sorted(por_linea[i], key=lambda t: t["idx"])
        linea = ts[0]["linea"]
        comp = " ".join(linea.replace("’", "'").replace("‘", "'").split())
        k = None
        if comp in compactas:
            ks = compactas[comp]
            k = ks[min(usados[comp], len(ks) - 1)]
            usados[comp] += 1
        else:
            # la fila geométrica puede no partir igual las palabras: se busca por los números de la línea y su primera palabra
            quiero = [norm(x) for x in ts[0]["toks"]]
            prim = comp.split(" ")[0] if comp else ""
            cands = [kk for kk, ns in nums.items() if [norm(x[2]) for x in ns] == quiero and fs[kk]["txt"].split(" ")[0] == prim]
            if len(cands) == 1:
                k = cands[0]
        for t in ts:
            r = {"doc": doc, "p": p, "i": i, "idx": t["idx"], "geo": 0}
            if k is not None:
                ns = nums[k]
                quiero = [norm(x) for x in t["toks"]]
                tengo = [norm(x[2]) for x in ns]
                j = None
                if tengo == quiero:
                    j = t["idx"]
                else:
                    pos = [a for a, x in enumerate(tengo) if x == norm(t["tok"])]
                    rep = [a for a, x in enumerate(quiero) if x == norm(t["tok"])]
                    if len(pos) == len(rep) and t["idx"] in rep:
                        j = pos[rep.index(t["idx"])]
                if j is not None:
                    x0, x1, _ = ns[j]
                    cab = geom.cabecera_del_token(fs, k, x0, x1)
                    cierre, apertura = geom.anios_de(cab["alineadas"])
                    ed = ("publicada" if any(geom.PUBLICADA.search(c) for c in cab["alineadas"]) else
                          "reexpresada" if any(geom.REEXPRESADA.search(c) for c in cab["alineadas"]) else "")
                    j0 = cab["j0"]
                    tit_tabla = ""
                    if cab["zona"]:
                        z0 = cab["zona"][0]
                        # título de la tabla: fila corta, sin cifras, a la izquierda, pegada encima de la cabecera o dentro de ella
                        for jj in list(range(max(0, z0 - 2), z0)) + cab["zona"]:
                            f = fs[jj]
                            if jj != j0 and f["x0"] < 75 and not re.search(r"\d", f["txt"]) and len(f["txt"]) <= 45 \
                                    and re.search(r"-(?:Md|Bold|Demi)", f["font"]) and fs[cab["zona"][0]]["c"] - f["c"] < 30 and not geom.es_encabezado(f):
                                tit_tabla = f["txt"]
                    enc = encabezado_encima(pdf, p, k)
                    ant = fs[k - 1]["txt"] if k > 0 else ""
                    r.update({"geo": 1, "x1": round(x1, 1), "al": cab["alineadas"], "so": cab["solapan"], "cierre": sorted(cierre),
                              "apertura": sorted(apertura), "otras_al": geom.otras_palabras(cab["alineadas"]),
                              "otras_so": geom.otras_palabras(cab["solapan"]), "ed": ed, "un": (cab["unidades"] or "")[:120],
                              "tit": tit_tabla, "enc": list(enc) if enc else None,
                              "rot": " ".join(w["t"] for w in fs[k]["ws"] if w["x1"] < ns[0][0])[:90],
                              "rot_ant": ant[:60] if (not geom.es_fila_de_datos(fs[k - 1]) and len(ant) <= 60 and k > 0) else "",
                              "fuente_fila": fs[k]["font"]})
            out.append(r)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raiz", required=True, type=Path)
    ap.add_argument("--autor", required=True, type=Path)
    ap.add_argument("--todas", required=True, type=Path)
    ap.add_argument("--salida", required=True, type=Path)
    ap.add_argument("--solo-grupo", action="store_true")
    ap.add_argument("--procesos", type=int, default=4)
    a = ap.parse_args()
    fuentes = json.loads((a.autor / "datos" / "fuentes.json").read_text(encoding="utf-8"))["fuentes"]
    sys.path.insert(0, str(a.autor / "scripts"))
    import subprocess
    vistos, por_pag = set(), defaultdict(list)
    lineas_cache = {}

    def lineas(doc, p):
        if (doc, p) not in lineas_cache:
            r = subprocess.run(["pdftotext", "-q", "-layout", "-f", str(p), "-l", str(p), str(a.raiz / fuentes[doc]["archivo"]), "-"],
                               capture_output=True, check=True)
            import unicodedata
            lineas_cache[(doc, p)] = unicodedata.normalize("NFKC", r.stdout.decode("utf-8", errors="replace")).replace("’", "'").replace("‘", "'").splitlines()
        return lineas_cache[(doc, p)]

    toks_linea = defaultdict(dict)
    crudos = []
    with gzip.open(a.todas, "rt", encoding="utf-8") as g:
        for l in g:
            c = json.loads(l)
            if a.solo_grupo and not c["g"]:
                continue
            clave = (c["doc"], c["p"], c["i"], c["idx"])
            if clave in vistos:
                continue
            vistos.add(clave)
            toks_linea[(c["doc"], c["p"], c["i"])][c["idx"]] = c["tok"]
            crudos.append(c)
    # la lista completa de tokens de cada línea (también marcadores y años, que el barrido no declara) se reconstruye con el
    # número de tokens n y los que se conocen; para el cotejo basta con la secuencia de los declarados cuando n coincide
    for c in crudos:
        d = toks_linea[(c["doc"], c["p"], c["i"])]
        toks = [d.get(j) for j in range(c["n"])]
        por_pag[(c["doc"], c["p"])].append({"i": c["i"], "idx": c["idx"], "tok": c["tok"], "toks": [x if x is not None else "§" for x in toks],
                                           "linea": lineas(c["doc"], c["p"])[c["i"]]})
    tareas = [(str(a.raiz / fuentes[doc]["archivo"]), fuentes[doc]["idioma"] == "fr", doc, p, ts) for (doc, p), ts in sorted(por_pag.items())]
    with Pool(a.procesos) as pool:
        res = pool.map(pagina, tareas, chunksize=4)
    n = geo = 0
    a.salida.parent.mkdir(parents=True, exist_ok=True)
    with gzip.open(a.salida, "wt", encoding="utf-8") as g:
        for out in res:
            for r in out:
                n += 1
                geo += r["geo"]
                g.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"tokens: {n}; con lectura geométrica: {geo} ({100 * geo / max(n, 1):.1f} %); páginas: {len(tareas)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
