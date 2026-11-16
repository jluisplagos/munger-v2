"""Revisión independiente n.º 9 · barrido propio C16 → C18 (frente E · F1 · Elis). No modifica nada del autor.

Universo: TODAS las líneas no vacías de TODAS las páginas de los cinco PDF de datos/fuentes.json, leídas con la misma
entrada que usa el verificador (`texto_pagina`, pdftotext -layout). Dos niveles:

  FUNCIONES  Cada función que C18 cambia o añade se llama directamente sobre cada línea (o cada token) con el código de C16
             y con el de C18, y se guarda lo que devuelve cada uno:
               - anio_de_saldo_en_rotulo (C16; C18 sin posición y con la posición de cada token), rotulo_de_saldo,
                 partes_de_rotulo con y sin `fecha`, columnas_de_datos                                   (T1, T2, T3)
               - token_del_rotulo, por token                                                    (regla nueva de f12f8ea)
               - cabecera_de_paises, por token                                                                    (T4)
               - rotulos_sin_rotulo                                                                               (T5)
               - es_encabezado_numerado: C16; C18 con la línea de debajo, como la llama el verificador; C18 sin ella (T6)
               - zona_de_cabecera y titulo_de_pais_encima_v2, que dependen de la anterior
               - es_titulo y rotulo_multilinea sin `fecha`, que C18 reescribe y no deberían cambiar (control)
  FILAS      Cada token numérico (salvo los marcadores «-») se declara como cifra del grupo en el modo «dos_columnas», con
             un identificador genérico, la unidad que da el literal («%» o «mm EUR») y la edición con la que la regla puede
             dar OK, para el ejercicio de la publicación (E), E−1 y E−2. Cada declaración se evalúa con `comprobar_tabla`
             de C16 y de C18. Además, el perímetro de cada uno de los siete segmentos con `comprobar_perimetro` de las dos
             versiones. Los demás modos de control se evalúan aparte, solo donde el código puede dar un resultado distinto
             (modos_9.py).

Escribe todo en un JSONL comprimido (--todas) y un resumen (--salida). Las clases se analizan con clases_9.py.

Uso: python3 -I -B barrido_9.py --raiz <munger_v2_r1> --c16 <frente C17> --c18 <frente C19> --todas <jsonl.gz> --salida <txt>
"""
import argparse
import csv
import gzip
import json
import sys
import time
from collections import Counter
from multiprocessing import Pool
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import arnes9 as H  # noqa: E402

_V = {}


def iniciar(raiz, c16, c18):
    _V["a"] = H.Version("C16", c16, raiz)
    _V["n"] = H.Version("C18", c18, raiz)


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
        grupo = N.pagina_del_grupo(lineas)
        for i, l in enumerate(lineas):
            if not l.strip():
                continue
            t = l.strip()
            debajo = lineas[i + 1] if i + 1 < len(lineas) else ""
            ar_a = Va.anio_de_saldo_en_rotulo(lineas, i, idioma)
            ar_n = Vn.anio_de_saldo_en_rotulo(lineas, i, idioma)
            enc = [int(Va.es_encabezado_numerado(t, idioma)), int(Vn.es_encabezado_numerado(t, idioma, debajo)),
                   int(Vn.es_encabezado_numerado(t, idioma))]
            rsr_a, rsr_n = Va.rotulos_sin_rotulo(lineas, i, idioma), Vn.rotulos_sin_rotulo(lineas, i, idioma)
            pf = Vn.partes_de_rotulo(lineas, i, idioma, alto=3, fecha=True)
            pnf = Vn.partes_de_rotulo(lineas, i, idioma, alto=3)
            toks = Vn.tokens_numericos(l, idioma)
            sp = Vn.spans_numericos(l, idioma)
            reg = {"doc": doc, "p": pag, "i": i, "g": int(grupo), "l": l, "nc": len(Vn.trozos(l)), "nt": len(toks),
                   "ar_a": ar_a, "ar_n": ar_n, "enc": enc, "rsr_a": rsr_a, "rsr_n": rsr_n, "rds": Vn.rotulo_de_saldo(lineas, i, idioma),
                   "pf": pf, "pnf": pnf, "ncol": Vn.columnas_de_datos(l, idioma), "rot": Vn.rotulo(l),
                   "ctl": [int(Va.es_titulo(t) == Vn.es_titulo(t)), int(Va.rotulo_multilinea(lineas, i, idioma) == Vn.rotulo_multilinea(lineas, i, idioma)),
                           int(Va.rotulo(l) == Vn.rotulo(l)), int(Va.tokens_numericos(l, idioma) == toks)],
                   "ctx": [lineas[j] for j in range(max(0, i - 4), min(len(lineas), i + 3))], "ci": i - max(0, i - 4), "toks": []}
            if toks and sp is not None:
                n = len(toks)
                za, zn = Va.zona_de_cabecera(lineas, i, idioma), Vn.zona_de_cabecera(lineas, i, idioma)
                if za != zn:
                    reg["zona"] = [za, zn]
                _, j = Vn.unidad_declarada(lineas, i)
                reg["ud"] = [Vn.unidad_declarada(lineas, i)[0], j]
                ta, tn = Va.titulo_de_pais_encima_v2(lineas, i, j, previas, idioma), Vn.titulo_de_pais_encima_v2(lineas, i, j, previas, idioma)
                if ta != tn:
                    reg["tpe"] = [ta, tn]
                for k, tok in enumerate(toks):
                    if tok in Vn.PLACEHOLDER:
                        continue
                    try:
                        val = Vn.valor(tok, idioma)
                    except ValueError:
                        continue
                    pos = k - n
                    unidad = "%" if "%" in tok else "mm EUR"
                    x = {"k": k, "tok": tok, "a0": sp[k][0], "a1": sp[k][1], "tdr": Vn.token_del_rotulo(lineas, i, pos, idioma),
                         "arp": Vn.anio_de_saldo_en_rotulo(lineas, i, idioma, pos), "G": {}}
                    ca, cn = Va.cabecera_de_paises(lineas, i, pos, idioma), Vn.cabecera_de_paises(lineas, i, pos, idioma)
                    if ca or cn:
                        x["cp"] = [list(ca) if ca else None, list(cn) if cn else None]
                    for y in (E, E - 1, E - 2):
                        f = H.declarar(doc, pag, lineas, i, k, n, tok, val, y, H.ID_GENERICO, "dos_columnas", unidad, H.GRUPO,
                                       N.edicion_posible("dos_columnas", y, doc))
                        ra, rn = A.tabla(f), N.tabla(f)
                        ca_, cn_ = H.codigo(ra), H.codigo(rn)
                        g = {"a": ca_, "n": cn_}
                        if ca_ != cn_ or H.estado(cn_) == "OK" or H.estado(ca_) == "OK":
                            g["da"], g["dn"] = H.detalles(ra), H.detalles(rn)
                        else:
                            g["ej"] = [ra["dimensiones"]["ejercicio"].get("detalle", ""), rn["dimensiones"]["ejercicio"].get("detalle", "")]
                        x["G"][str(y)] = g
                    seg = {}
                    for s in H.SEGMENTOS:
                        f = {"perimetro": "segmento " + s}
                        ea, da = Va.comprobar_perimetro(lineas, i, f, pos, idioma, previas)
                        en, dn = Vn.comprobar_perimetro(lineas, i, f, pos, idioma, previas)
                        if ea != en or da != dn:
                            seg[s] = [H.LETRA[ea], H.LETRA[en], da, dn]
                    if seg:
                        x["S"] = seg
                    reg["toks"].append(x)
            interesa = (reg["toks"] or ar_a is not None or ar_n is not None or any(enc) or rsr_a or rsr_n or pf != pnf or 0 in reg["ctl"])
            if interesa:
                out.append(reg)
    return doc, pags, out


def equivalencia(ver, p):
    """(1) El módulo cargado da, para las filas de tabla reales, lo mismo que la ejecución oficial guardada. (2) Declarar la
    fila con la línea fijada entera (como hace este barrido) da los mismos estados que la declaración del autor, en las
    filas cuya etiqueta casa con una sola línea."""
    of = {r["id"]: r for r in json.loads((ver.carpeta / "resultados" / "verificacion_cifras.json").read_text(encoding="utf-8"))["cifras"]}
    with open(ver.carpeta / "datos" / "cifras_fuente.csv", encoding="utf-8", newline="") as f:
        filas = [x for x in csv.DictReader(f, delimiter=";") if x["tipo"] == "tabla"]
    iguales = exactas = exactas_ok = 0
    for fila in filas:
        res = ver.tabla(fila)
        mismas = all(res["dimensiones"][d]["estado"] == of[fila["id"]]["dimensiones"][d]["estado"]
                     and res["dimensiones"][d].get("detalle") == of[fila["id"]]["dimensiones"][d].get("detalle") for d in H.DIMS)
        iguales += mismas
        doc, pag, idioma = fila["doc"], int(fila["pagina"]), ver.idioma(fila["doc"])
        lineas = ver.lineas(doc, pag)
        cand = ver.V.lineas_con("\n".join(lineas), fila["etiqueta"])
        occ = int(fila["ocurrencia"] or 0)
        if occ:
            cand = [cand[occ - 1]]
        if len(cand) != 1:
            continue
        i = cand[0][0]
        toks = ver.V.tokens_numericos(lineas[i], idioma)
        k = int(fila["pos"]) % len(toks)
        f2 = dict(fila, etiqueta=H.declarar(doc, pag, lineas, i, k, len(toks), toks[k], 0, 0, "", "", "", "", "")["etiqueta"],
                  ocurrencia=str(1 + sum(1 for x in lineas[:i] if x == lineas[i])), pos=str(k - len(toks)))
        exactas += 1
        exactas_ok += H.codigo(ver.tabla(f2)) == H.codigo(res)
    p(f"  {ver.nombre}: {iguales} de {len(filas)} filas de tabla reales con los mismos estados y detalles que la salida oficial guardada; "
      f"{exactas_ok} de {exactas} con los mismos estados al declararlas con la línea fijada entera")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raiz", required=True, type=Path)
    ap.add_argument("--c16", required=True, type=Path)
    ap.add_argument("--c18", required=True, type=Path)
    ap.add_argument("--todas", required=True, type=Path)
    ap.add_argument("--salida", required=True, type=Path)
    ap.add_argument("--procesos", type=int, default=4)
    ap.add_argument("--solo", help="doc:pagina, para pruebas")
    a = ap.parse_args()
    t0 = time.time()
    iniciar(a.raiz, a.c16, a.c18)
    N = _V["n"]
    out = []

    def p(*x):
        s = " ".join(str(v) for v in x)
        out.append(s)
        print(s, flush=True)

    tareas = []
    for doc in sorted(N.fuentes):
        np_ = N.paginas(doc)
        for ini in range(1, np_ + 1, 6):
            tareas.append((doc, list(range(ini, min(np_, ini + 5) + 1))))
    if a.solo:
        d, n = a.solo.split(":")
        tareas = [(d, [int(n)])]
    p("# Barrido n.º 9 · C16 (worktree de C17) → C18 (worktree de C19) · todas las líneas de todas las páginas")
    p("Equivalencia del arnés con la ejecución oficial:")
    equivalencia(_V["a"], p)
    equivalencia(N, p)
    paginas = lineas_n = tokens = 0
    trans, trans_dim, ctl = Counter(), Counter(), Counter()
    with gzip.open(a.todas, "wt", encoding="utf-8") as g, Pool(a.procesos, initializer=iniciar, initargs=(a.raiz, a.c16, a.c18)) as pool:
        for doc, pags, regs in pool.imap(bloque, tareas, chunksize=1):
            paginas += len(pags)
            for r in regs:
                g.write(json.dumps(r, ensure_ascii=False) + "\n")
                if r["toks"]:
                    lineas_n += 1
                for k, v in zip(("es_titulo", "rotulo_multilinea sin fecha", "rotulo", "tokens_numericos"), r["ctl"]):
                    ctl[(k, v)] += 1
                for x in r["toks"]:
                    tokens += 1
                    for y, gg in x["G"].items():
                        ea, en = H.estado(gg["a"]), H.estado(gg["n"])
                        trans[(ea, en)] += 1
                        for d, ca, cn in zip(H.DIMS, gg["a"], gg["n"]):
                            if ca != cn:
                                trans_dim[(d, ca, cn)] += 1
    p(f"Páginas: {paginas}; líneas con algún token numérico: {lineas_n}; tokens: {tokens}; candidatas (token × 3 ejercicios): {sum(trans.values())}")
    p("Controles (funciones que C18 reescribe y no deberían cambiar; 1 = igual en las dos versiones):")
    for (k, v), c in sorted(ctl.items()):
        p(f"  {k}: {'igual' if v else 'DISTINTO'} en {c} líneas")
    p("Transiciones del estado de la fila (C16 → C18), candidatas del grupo en «dos_columnas»:")
    for (ea, en), c in sorted(trans.items()):
        p(f"  {ea:9} → {en:9} {c:7}")
    p(f"  OK en C16: {sum(c for (ea, _), c in trans.items() if ea == 'OK')}; OK en C18: {sum(c for (_, en), c in trans.items() if en == 'OK')}")
    p("Cambios por dimensión (O = OK, N = NO_APLICA, P = PENDIENTE, F = FALLO):")
    for (d, ca, cn), c in sorted(trans_dim.items()):
        p(f"  {d:10} {ca} → {cn} {c:7}")
    p(f"Tiempo: {time.time() - t0:.0f} s")
    a.salida.write_text("\n".join(out) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
