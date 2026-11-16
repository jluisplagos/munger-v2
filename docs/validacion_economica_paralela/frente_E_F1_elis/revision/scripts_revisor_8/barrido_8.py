"""Revisión independiente n.º 8 · barrido propio C14 → C16 (frente E · F1 · Elis). No modifica nada del autor.

Universo: TODOS los tokens numéricos (salvo los marcadores «-») de TODAS las líneas de TODAS las páginas de los cinco
PDF: con rótulo o sin él, del grupo o no, prosa incluida. Los barridos de las revisiones n.º 6 y 7 recorrían, el primero,
solo las líneas con rótulo, y el segundo, solo las páginas del grupo; los dos declaraban cada token solo como cifra del
grupo de dos columnas. Aquí cada token se declara de cuatro maneras:

  G   cifra del grupo, modo «dos_columnas», con el ejercicio de la publicación (E), E−1 y E−2, la unidad que da el literal
      («%» o «mm EUR») y la edición con la que la regla puede dar OK. Se evalúa con `comprobar_tabla` de C14 y de C16;
  M   los demás modos de control del ejercicio (max_cabecera, movimientos, saldo, titulo, crecimiento), con los
      identificadores de sondeo de arnes8.PERFILES_DE_MODO, que fijan también la columna esperada de cada familia.
      Mismos tres ejercicios; «crecimiento», solo en los porcentajes. `comprobar_tabla` de las dos versiones;
  S   el perímetro de cada uno de los siete segmentos: `comprobar_perimetro` de las dos versiones (la dimensión no
      depende del ejercicio ni del modo);
  R   lo que las funciones nuevas de C16 leen en la línea: el ejercicio del saldo del rótulo (regla de S1), los rótulos
      de las líneas contiguas (S2), el rótulo con y sin la pestaña del margen (S3) y la cabecera de países (S4).

Guarda todo en un JSONL comprimido (--todas) y escribe el resumen (--salida). Las clases se analizan con clases_8.py.

Uso: python3 -I -B barrido_8.py --raiz <munger_v2_r1> --c14 <frente C15> --c16 <frente C17> --todas <jsonl.gz> --salida <txt>
"""
import argparse
import gzip
import json
import re
import sys
import time
from collections import Counter
from multiprocessing import Pool
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import arnes8 as H  # noqa: E402

_V = {}
PIE = re.compile(r"Universal Registration Document|enregistrement universel")


def iniciar(raiz, c14, c16):
    _V["a"] = H.Version("C14", c14, raiz)
    _V["n"] = H.Version("C16", c16, raiz)


def detalles(res):
    return {d: res["dimensiones"][d].get("detalle", "") for d in H.DIMS[1:]}


def bloque(tarea):
    doc, pags = tarea
    A, N = _V["a"], _V["n"]
    Va, Vn = A.V, N.V
    idioma, E = N.idioma(doc), N.publicacion(doc)
    out = []
    for pag in pags:
        lineas = N.lineas(doc, pag)
        assert lineas == A.lineas(doc, pag)
        previas = N.lineas(doc, pag - 1) if pag > 1 else []
        grupo = N.es_pagina_del_grupo(lineas)
        for i, l in enumerate(lineas):
            toks = Vn.tokens_numericos(l, idioma)
            sp = Vn.spans_numericos(l, idioma)
            if not toks or sp is None:
                continue
            n = len(toks)
            celdas = Vn.trozos(l)
            a_rot = Vn.anio_de_saldo_en_rotulo(lineas, i, idioma)
            rsr = Vn.rotulos_sin_rotulo(lineas, i, idioma)
            linea = {"doc": doc, "p": pag, "i": i, "g": int(grupo), "n": n, "nceldas": len(celdas), "l": l,
                     "rot14": Va.rotulo(l), "rot16": Vn.rotulo(l), "rml14": Va.rotulo_multilinea(lineas, i, idioma),
                     "rml16": Vn.rotulo_multilinea(lineas, i, idioma), "a_rot": a_rot, "rsr": rsr,
                     "rot_num": int(bool(celdas) and Vn.es_numero(celdas[0].split(" ")[0], idioma)), "pie": int(bool(PIE.search(l))),
                     "ctx": [lineas[j] for j in range(max(0, i - 3), min(len(lineas), i + 2))], "toks": []}
            for k, tok in enumerate(toks):
                if tok in Vn.PLACEHOLDER:
                    continue
                try:
                    val = Vn.valor(tok, idioma)
                except ValueError:
                    continue
                unidad = "%" if "%" in tok else "mm EUR"
                t = {"k": k, "tok": tok, "a0": sp[k][0], "a1": sp[k][1], "G": {}, "M": {}, "S": {}}
                cp = Vn.cabecera_de_paises(lineas, i, k - n, idioma)
                if cp:
                    t["cp"] = [cp[0], cp[1]]
                # G: grupo, dos columnas
                for y in (E, E - 1, E - 2):
                    f = H.fila(doc, pag, lineas, i, k, n, tok, val, y, H.ID_GRUPO, "dos_columnas", unidad, H.GRUPO,
                               N.edicion_que_pasa("dos_columnas", y, doc))
                    ra, rn = A.tabla(f), N.tabla(f)
                    t["G"][str(y)] = {"ed": f["edicion"], "a": H.codigo(ra), "n": H.codigo(rn), "da": detalles(ra), "dn": detalles(rn)}
                # M: los demás modos. La unidad y el perímetro no dependen del modo ni del ejercicio: son los de G (se
                # comprueba que G da los mismos en sus tres ejercicios). El ejercicio, la columna y la edición se piden a
                # las funciones que `comprobar_tabla` usa para ellos, y uno de cada 25 tokens se evalúa además con
                # `comprobar_tabla` entera para comprobar que la composición da lo mismo.
                g0 = t["G"][str(E)]
                if any(g["a"][3:5] != g0["a"][3:5] or g["n"][3:5] != g0["n"][3:5] for g in t["G"].values()):
                    t["incoherente_G"] = 1
                muestra = (i * 7 + k) % 25 == 0
                texto = "\n".join(lineas)
                col = {}
                for idf, modo in H.PERFILES_DE_MODO:
                    if modo == "crecimiento" and "%" not in tok:
                        continue
                    for y in (E, E - 1, E - 2):
                        f = H.fila(doc, pag, lineas, i, k, n, tok, val, y, idf, modo, unidad, H.GRUPO, N.edicion_que_pasa(modo, y, doc))
                        cods, dets = {}, {}
                        for nombre, ver, Vx in (("a", A, Va), ("n", N, Vn)):
                            ej = Vx.comprobar_anio(lineas, i, f, idioma)
                            if (nombre, idf) not in col:
                                col[(nombre, idf)] = Vx.comprobar_columna(lineas, i, f, k - n, idioma)
                            co = col[(nombre, idf)]
                            ed = Vx.comprobar_edicion(texto, f, ver.fuentes[doc], ver.ejercicios)[:2]
                            cods[nombre] = "O" + H.COD[ej[0]] + H.COD[co[0]] + g0[nombre][3:5] + H.COD[ed[0]]
                            dets[nombre] = {"ejercicio": ej[1], "columna": co[1], "edicion": ed[1]}
                            if muestra:
                                c_of = H.codigo(ver.tabla(f))
                                t["mu"] = t.get("mu", 0) + 1
                                if c_of != cods[nombre]:
                                    t["mu_dif"] = t.get("mu_dif", 0) + 1
                        reg = {"a": cods["a"], "n": cods["n"]}
                        if cods["a"] != cods["n"] or H.estado_de_codigo(cods["n"]) == "OK":
                            reg["da"], reg["dn"] = dets["a"], dets["n"]
                        t["M"][idf + "|" + str(y)] = reg
                # S: perímetro de cada segmento
                for s in H.SEGMENTOS:
                    f = {"perimetro": "segmento " + s}
                    ea, da = Va.comprobar_perimetro(lineas, i, f, k - n, idioma, previas)
                    en, dn = Vn.comprobar_perimetro(lineas, i, f, k - n, idioma, previas)
                    if ea != en or en == "OK":
                        t["S"][s] = {"a": H.COD[ea], "n": H.COD[en], "da": da, "dn": dn}
                linea["toks"].append(t)
            if linea["toks"]:
                out.append(linea)
    return doc, pags, out


def equivalencia(ver, salida):
    """Módulo cargado = ejecución oficial guardada, en las filas de tabla reales, y declaración con la línea fijada entera =
    declaración del autor, en las filas cuya etiqueta casa con una sola línea."""
    of = {r["id"]: r for r in json.loads((ver.carpeta / "resultados" / "verificacion_cifras.json").read_text(encoding="utf-8"))["cifras"]}
    n = dif = n2 = dif2 = 0
    for f in H.leer_csv(ver.carpeta / "datos" / "cifras_fuente.csv"):
        if f["tipo"] != "tabla":
            continue
        n += 1
        r = ver.tabla(f)
        if r["dimensiones"] != of[f["id"]]["dimensiones"]:
            dif += 1
        doc, pag, idioma = f["doc"], int(f["pagina"]), ver.idioma(f["doc"])
        lineas = ver.lineas(doc, pag)
        cand = ver.V.lineas_con("\n".join(lineas), f["etiqueta"])
        occ = int(f["ocurrencia"] or 0)
        if occ:
            cand = [cand[occ - 1]]
        if len(cand) != 1:
            continue
        i, l = cand[0]
        toks = ver.V.tokens_numericos(l, idioma)
        k = int(f["pos"]) % len(toks)
        g = H.fila(doc, pag, lineas, i, k, len(toks), f["literal"], f["valor_publicado"], int(f["anio"]), f["id"], f["control_anio"],
                   f["unidad"], f["perimetro"], f["edicion"])
        n2 += 1
        r2 = ver.tabla(g)
        if {d: (v["estado"], v["detalle"]) for d, v in r2["dimensiones"].items()} != {d: (v["estado"], v["detalle"]) for d, v in of[f["id"]]["dimensiones"].items()}:
            dif2 += 1
    salida(f"Equivalencia en {ver.nombre}: `comprobar_tabla` del módulo = ejecución oficial guardada en {n} filas de tabla reales, {dif} con alguna dimensión distinta; "
           f"declaración con la línea fijada entera = declaración del autor en {n2} filas de una sola línea, {dif2} distintas")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raiz", required=True)
    ap.add_argument("--c14", required=True)
    ap.add_argument("--c16", required=True)
    ap.add_argument("--todas", required=True, type=Path)
    ap.add_argument("--salida", required=True, type=Path)
    ap.add_argument("--procesos", type=int, default=4)
    ap.add_argument("--solo", help="DOC:desde-hasta, para pruebas")
    a = ap.parse_args()
    t0 = time.time()
    out = []

    def p(*x):
        s = " ".join(str(v) for v in x)
        out.append(s)
        print(s, flush=True)

    iniciar(a.raiz, a.c14, a.c16)
    A, N = _V["a"], _V["n"]
    p("Barrido propio de la revisión n.º 8 · C14 → C16 · todas las líneas de todas las páginas")
    p()
    equivalencia(N, p)
    equivalencia(A, p)
    tareas = []
    for doc in sorted(N.fuentes):
        np_ = N.paginas(doc)
        rango = range(1, np_ + 1)
        if a.solo:
            d, r = a.solo.split(":")
            if d != doc:
                continue
            x, y = r.split("-")
            rango = range(int(x), int(y) + 1)
        pags = list(rango)
        tareas += [(doc, pags[j:j + 8]) for j in range(0, len(pags), 8)]
    a.todas.parent.mkdir(parents=True, exist_ok=True)
    c = Counter()
    trans = {u: Counter() for u in ("todas", "grupo")}
    por_dim = {u: Counter() for u in ("todas", "grupo")}
    modos = Counter()
    segs = Counter()
    pags_doc, pags_grupo = Counter(), {}
    with gzip.open(a.todas, "wt", encoding="utf-8") as f, Pool(a.procesos, initializer=iniciar, initargs=(a.raiz, a.c14, a.c16)) as pool:
        for doc, pags, lineas in pool.imap_unordered(bloque, tareas):
            pags_doc[doc] += len(pags)
            for ln in lineas:
                f.write(json.dumps(ln, ensure_ascii=False) + "\n")
                pags_grupo.setdefault(doc, set())
                if ln["g"]:
                    pags_grupo[doc].add(ln["p"])
                for t in ln["toks"]:
                    c["tokens"] += 1
                    c["tokens_grupo"] += ln["g"]
                    c["tokens_sin_rotulo"] += ln["rot_num"]
                    c["tokens_sin_rotulo_grupo"] += ln["rot_num"] * ln["g"]
                    for y, g in t["G"].items():
                        ea, en = H.estado_de_codigo(g["a"]), H.estado_de_codigo(g["n"])
                        for u in ("todas",) + (("grupo",) if ln["g"] else ()):
                            c["cand_" + u] += 1
                            trans[u][(ea, en)] += 1
                            for j, d in enumerate(H.DIMS):
                                if g["a"][j] != g["n"][j]:
                                    por_dim[u][(d, g["a"][j], g["n"][j])] += 1
                    c["M_muestra"] += t.get("mu", 0)
                    c["M_muestra_distintas"] += t.get("mu_dif", 0)
                    c["G_incoherente"] += t.get("incoherente_G", 0)
                    for clave, m in t["M"].items():
                        idf = clave.split("|")[0]
                        modos[(idf, "candidatas")] += 1
                        if m["a"] != m["n"]:
                            modos[(idf, "con algún estado distinto")] += 1
                            for j, d in enumerate(H.DIMS):
                                if m["a"][j] != m["n"][j]:
                                    modos[(idf, f"{d}: {m['a'][j]} → {m['n'][j]}")] += 1
                        ea, en = H.estado_de_codigo(m["a"]), H.estado_de_codigo(m["n"])
                        if ea != en:
                            modos[(idf, f"fila: {ea} → {en}")] += 1
                        if en == "OK":
                            modos[(idf, "fila OK en C16")] += 1
                        if ea == "OK":
                            modos[(idf, "fila OK en C14")] += 1
                    for s, m in t["S"].items():
                        segs[(s, f"{m['a']} → {m['n']}")] += 1
    p()
    p("Páginas recorridas y, de ellas, con alguna línea con cifras en una página aceptada como del grupo:")
    for doc in sorted(pags_doc):
        p(f"  {doc}: {pags_doc[doc]} páginas, {len(pags_grupo.get(doc, ()))} del grupo")
    p(f"Tokens: {c['tokens']} ({c['tokens_grupo']} en páginas del grupo); en líneas sin rótulo (primera celda numérica): {c['tokens_sin_rotulo']} "
      f"({c['tokens_sin_rotulo_grupo']} en páginas del grupo)")
    p(f"Candidatas G (token × ejercicio E, E−1, E−2): {c['cand_todas']}; en páginas del grupo: {c['cand_grupo']}")
    for u, nombre in (("todas", "todas las páginas"), ("grupo", "páginas del grupo")):
        p()
        p(f"== G · estado de la fila, {nombre}: C14 → C16 ==")
        for (ea, en), v in sorted(trans[u].items()):
            p(f"  {ea:9} → {en:9} {v:7}" + ("   ← cambia" if ea != en else ""))
        p(f"== G · transiciones por dimensión, {nombre} ==")
        for (d, x, y), v in sorted(por_dim[u].items()):
            p(f"  {d}: {x} → {y}: {v}")
    p()
    p("== M · los demás modos de control del ejercicio (todas las páginas): candidatas y diferencias entre C14 y C16 ==")
    p(f"  composición por dimensiones = `comprobar_tabla` entera: {c['M_muestra']} evaluaciones de muestra, {c['M_muestra_distintas']} distintas; "
      f"tokens cuya unidad o perímetro cambian con el ejercicio declarado en G: {c['G_incoherente']}")
    for idf, modo in H.PERFILES_DE_MODO:
        p(f"  {idf} ({modo}): " + "; ".join(f"{k}: {v}" for (i_, k), v in sorted(modos.items()) if i_ == idf))
    p()
    p("== S · perímetro declarado de cada segmento (todas las páginas): tokens con estado distinto o con OK en C16 ==")
    for s in H.SEGMENTOS:
        p(f"  {s}: " + "; ".join(f"{k}: {v}" for (s_, k), v in sorted(segs.items()) if s_ == s))
    p()
    p(f"Tiempo: {time.time() - t0:.0f} s")
    a.salida.parent.mkdir(parents=True, exist_ok=True)
    a.salida.write_text("\n".join(out) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
