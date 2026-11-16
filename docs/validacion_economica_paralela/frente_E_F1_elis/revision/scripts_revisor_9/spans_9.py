"""Revisión independiente n.º 9 · posición de cada token numérico en su línea (frente E · F1 · Elis). No modifica nada del autor.

`spans_numericos` del verificador localiza cada token con `linea.find(token, desde)`: la primera aparición de su TEXTO a
partir del final del token anterior. Si ese texto aparece antes dentro de otra celda (el «0» de «12/31/2025», el «2» de
«Level 2»), la posición que devuelve no es la del token. De esa posición dependen la columna del token (ejercicio, concepto,
país, grupo de columnas, matriz por segmentos, edición) y, desde C18, `token_del_rotulo`, la condición «a la derecha del
rótulo» de la regla de la fecha y `columnas_de_datos`.

Este script calcula la posición verdadera de cada token con un tokenizador propio que sigue celda a celda la misma regla
que `tokens_numericos` (se comprueba que da los mismos tokens en todas las líneas) y la compara con la del verificador:

  1. tokens mal localizados en todas las páginas, por dónde cae la posición devuelta;
  2. filas reales del CSV cuyo token está mal localizado;
  3. efecto: cada token de las líneas afectadas se declara como en barrido_9.py (grupo, «dos_columnas», tres ejercicios) y,
     además, con los identificadores de sondeo de los demás modos, y se evalúa con `comprobar_tabla` tal como es y con
     `spans_numericos` sustituido en memoria por la posición verdadera, en C16 y en C18. Nada se escribe en el verificador.

Uso: python3 -I -B spans_9.py --raiz <munger_v2_r1> --c16 <frente C17> --c18 <frente C19>
"""
import argparse
import csv
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import arnes9 as H  # noqa: E402


def tokens_con_posicion(V, linea, idioma):
    """[(inicio, fin, token)] con la misma regla que `tokens_numericos`, siguiendo la posición de cada celda y de cada
    palabra de la celda."""
    out = []
    for c in re.finditer(r"\S+(?:\s\S+)*", linea):
        t = c.group()
        if V.es_numero(t, idioma):
            out.append((c.start(), c.end(), t))
            continue
        partes = [(c.start() + m.start(), c.start() + m.end(), m.group()) for m in re.finditer(r"[^ ]+", t)]
        cola = []
        while partes:
            a, b, cand = partes[-1]
            if idioma == "fr" and len(partes) >= 2 and re.fullmatch(r"\(?\d{1,3}", partes[-2][2]) and re.fullmatch(r"\d{3}(?:,\d+)?\)?%?", cand):
                unido = partes[-2][2] + " " + cand
                if V.es_numero(unido, idioma) and b - partes[-2][0] == len(unido):
                    cola.insert(0, (partes[-2][0], b, unido))
                    partes = partes[:-2]
                    continue
            if V.es_numero(cand, idioma) and cand not in V.PLACEHOLDER:
                cola.insert(0, (a, b, cand))
                partes = partes[:-1]
            else:
                break
        out.extend(cola)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raiz", required=True, type=Path)
    ap.add_argument("--c16", required=True, type=Path)
    ap.add_argument("--c18", required=True, type=Path)
    a = ap.parse_args()
    A, N = H.Version("C16", a.c16, a.raiz), H.Version("C18", a.c18, a.raiz)
    V = N.V

    def p(*x):
        print(" ".join(str(v) for v in x), flush=True)

    p("Posición de los tokens numéricos: `spans_numericos` del verificador frente a la posición verdadera")
    p()
    lineas_tot = tokens_tot = distintos_tok = 0
    mal = []      # (doc, pag, i, k, token, dado, verdadero, clase, grupo)
    for doc in sorted(N.fuentes):
        idioma = N.idioma(doc)
        for pag in range(1, N.paginas(doc) + 1):
            L = N.lineas(doc, pag)
            g = N.pagina_del_grupo(L)
            for i, l in enumerate(L):
                toks = V.tokens_numericos(l, idioma)
                if not toks:
                    continue
                mios = tokens_con_posicion(V, l, idioma)
                lineas_tot += 1
                tokens_tot += len(toks)
                if [t for _, _, t in mios] != toks:
                    distintos_tok += 1
                    continue
                sp = V.spans_numericos(l, idioma)
                if sp is None:
                    continue
                rot = V.rotulo(l)
                ini = l.find(rot)
                for k, ((a0, a1, t), (b0, b1)) in enumerate(zip(mios, sp)):
                    if (a0, a1) != (b0, b1):
                        if ini <= b0 < ini + len(rot) and not (ini <= a0 < ini + len(rot)):
                            clase = "cae dentro del rótulo; el token está a su derecha"
                        elif any(x0 <= b0 < x1 for x0, x1, _ in mios[:k]):
                            clase = "cae dentro de un token anterior"
                        elif any(x0 <= b0 and b1 <= x1 and (x0, x1) != (a0, a1) for x0, x1, _ in mios):
                            clase = "cae sobre otro token de la línea"
                        else:
                            clase = "cae dentro de otra celda de texto"
                        mal.append((doc, pag, i, k, t, (b0, b1), (a0, a1), clase, int(g)))
    p("== 1. Tokens mal localizados ==")
    p(f"  líneas con cifras: {lineas_tot}; tokens: {tokens_tot}; líneas en que mi tokenizador no da los mismos tokens que el verificador: {distintos_tok}")
    lin_mal = {(m[0], m[1], m[2]) for m in mal}
    p(f"  tokens cuya posición no es la verdadera: {len(mal)} en {len(lin_mal)} líneas ({sum(1 for m in mal if m[8])} tokens en páginas del grupo)")
    for c, n in Counter(m[7] for m in mal).most_common():
        p(f"    {n:5}  {c}")
    p(f"  por publicación: {dict(sorted(Counter(m[0] for m in mal).items()))}")
    p(f"  por texto del token (los 15 más frecuentes): {Counter(m[4] for m in mal).most_common(15)}")
    rx_dec, rx_ent, rx_esp = re.compile(r"[.,]\d|\d \d"), re.compile(r"\(?\d+\)?"), re.compile(r"\s{2,}")
    p(f"  marcadores «-»: {sum(1 for m in mal if m[4] in V.PLACEHOLDER)}; con decimales o separador de miles: {sum(1 for m in mal if rx_dec.search(m[4]))}; "
      f"porcentajes: {sum(1 for m in mal if '%' in m[4])}; enteros sin separador: {sum(1 for m in mal if rx_ent.fullmatch(m[4]))}")
    p("  en páginas del grupo, sin los marcadores «-» (todas):")
    for doc, pag, i, k, t, dado, verd, clase, g in mal:
        if g and t not in V.PLACEHOLDER:
            l = N.lineas(doc, pag)[i]
            p(f"    {doc} p.{pag} l.{i + 1} · token {k} «{t}» · dado {dado} «{l[max(0, dado[0] - 8):dado[1] + 8].strip()}» · verdadero {verd} · {clase} · "
              f"«{rx_esp.sub('  ', l.strip())[:95]}»")
    p()
    # ------------------------------------------------------------------ 2
    p("== 2. Filas reales del CSV ==")
    with open(N.carpeta / "datos" / "cifras_fuente.csv", encoding="utf-8", newline="") as f:
        filas = [x for x in csv.DictReader(f, delimiter=";") if x["tipo"] == "tabla"]
    afectadas = lineas_afect = 0
    for fila in filas:
        doc, pag, idioma = fila["doc"], int(fila["pagina"]), N.idioma(fila["doc"])
        L = N.lineas(doc, pag)
        cand = V.lineas_con("\n".join(L), fila["etiqueta"])
        occ = int(fila["ocurrencia"] or 0)
        if occ:
            cand = [cand[occ - 1]]
        fila_mal = linea_mal = False
        for i, l in cand:
            n = len(V.tokens_numericos(l, idioma))
            k = int(fila["pos"]) % n
            if any(m[:4] == (doc, pag, i, k) for m in mal):
                fila_mal = True
                p(f"    {fila['id']} · {doc} p.{pag} l.{i + 1} · token {k} «{fila['literal']}» mal localizado")
            if (doc, pag, i) in lin_mal:
                linea_mal = True
        afectadas += fila_mal
        lineas_afect += linea_mal
    p(f"  filas de tabla reales: {len(filas)}; con su token mal localizado: {afectadas}; en una línea con algún otro token mal localizado: {lineas_afect - afectadas}")
    p()
    # ------------------------------------------------------------------ 3
    p("== 3. Efecto: `comprobar_tabla` tal como es y con la posición verdadera, en las líneas afectadas ==")
    for ver in (A, N):
        Vx = ver.V
        original = Vx.spans_numericos

        def corregida(linea, idioma, Vx=Vx):
            m = tokens_con_posicion(Vx, linea, idioma)
            return [(x0, x1) for x0, x1, _ in m] if [t for _, _, t in m] == Vx.tokens_numericos(linea, idioma) else original(linea, idioma)
        trans, trans_m, ejemplos = Counter(), Counter(), {}
        por_dim = Counter()
        retirados, falso_ok = {}, []
        for doc, pag, i in sorted(lin_mal):
            idioma, E = ver.idioma(doc), ver.publicacion(doc)
            L = ver.lineas(doc, pag)
            toks = Vx.tokens_numericos(L[i], idioma)
            n = len(toks)
            for k, tok in enumerate(toks):
                if tok in Vx.PLACEHOLDER:
                    continue
                try:
                    val = Vx.valor(tok, idioma)
                except ValueError:
                    continue
                unidad = "%" if "%" in tok else "mm EUR"
                perfiles = [(H.ID_GENERICO, "dos_columnas")] + [x for x in H.PERFILES if x[1] != "crecimiento" or "%" in tok]
                for idf, modo in perfiles:
                    for y in (E, E - 1, E - 2):
                        f = H.declarar(doc, pag, L, i, k, n, tok, val, y, idf, modo, unidad, H.GRUPO, ver.edicion_posible(modo, y, doc))
                        Vx.spans_numericos = original
                        r0 = ver.tabla(f)
                        c0 = H.codigo(r0)
                        Vx.spans_numericos = corregida
                        r1 = ver.tabla(f)
                        c1 = H.codigo(r1)
                        Vx.spans_numericos = original
                        destino = trans if modo == "dos_columnas" else trans_m
                        destino[(H.estado(c0), H.estado(c1))] += 1
                        d0 = r0["dimensiones"]["ejercicio"].get("detalle", "")
                        if "no una cifra" in d0 and "no una cifra" not in r1["dimensiones"]["ejercicio"].get("detalle", ""):
                            retirados.setdefault((doc, pag, i, k, tok), set()).add((modo, c0[1], c1[1]))
                        if modo == "dos_columnas" and c0[1] == "O" and c1[1] != "O":
                            falso_ok.append(f"{doc} p.{pag} l.{i + 1} token {k} «{tok}» declarado {y}: {c0} → {c1} · tal como es: «{d0[:60]}» · "
                                            f"con la posición verdadera: «{r1['dimensiones']['ejercicio'].get('detalle', '')[:80]}»")
                        if c0 != c1:
                            for d, x0, x1 in zip(H.DIMS, c0, c1):
                                if x0 != x1:
                                    por_dim[(modo == "dos_columnas", d, x0, x1)] += 1
                            clave = (modo == "dos_columnas", H.estado(c0), H.estado(c1))
                            if H.estado(c0) != H.estado(c1) and len(ejemplos.setdefault(clave, [])) < 6:
                                ejemplos[clave].append(f"{doc} p.{pag} l.{i + 1} «{tok}» {idf} {y}: {c0} → {c1} · "
                                                       f"{'; '.join(d + ': ' + r1['dimensiones'][d].get('detalle', '')[:70] for d, x0, x1 in zip(H.DIMS, c0, c1) if x0 != x1)}")
        p(f"  -- {ver.nombre} --")
        p(f"  modo «dos_columnas» (estado tal como es → estado con la posición verdadera): {dict(sorted(trans.items()))}")
        p(f"  demás modos (15 identificadores de sondeo): {dict(sorted(trans_m.items()))}")
        p(f"  dimensiones que cambian («dos_columnas»): {dict(sorted((k[1:], v) for k, v in por_dim.items() if k[0]))}")
        p(f"  dimensiones que cambian (demás modos): {dict(sorted((k[1:], v) for k, v in por_dim.items() if not k[0]))}")
        for (dc, e0, e1), ej in sorted(ejemplos.items()):
            p(f"    {'dos_columnas' if dc else 'otros modos'} · {e0} → {e1}:")
            for e in ej:
                p("      " + e)
        p(f"  «dos_columnas»: candidatas con el ejercicio OK tal como es y no OK con la posición verdadera: {len(falso_ok)}")
        for e in falso_ok:
            p("      " + e)
        p(f"  tokens que `token_del_rotulo` da por «año o día del rótulo» y que con la posición verdadera no lo son: {len(retirados)}")
        for (doc, pag, i, k, tok), usos in sorted(retirados.items()):
            l = ver.lineas(doc, pag)[i]
            cambios = Counter((x0, x1) for _, x0, x1 in usos)
            p(f"      {doc} p.{pag} l.{i + 1} token {k} «{tok}» · ejercicio tal como es → con la posición verdadera, por declaración: {dict(cambios)} · "
              f"«{re.sub(chr(92) + 's{2,}', '  ', l.strip())[:110]}»")
    return 0


if __name__ == "__main__":
    sys.exit(main())
