"""Revisión independiente n.º 9 · consultas al barrido propio (frente E · F1 · Elis). No modifica nada del autor.

Desgloses que el informe cita y que clases_9.py no imprime:
  Q1  transiciones del estado de la fila por el motivo de la regla nueva de f12f8ea (año del rótulo, día de la fecha, otro);
  Q2  los tokens con el motivo «día de la fecha», uno a uno;
  Q3  tokens que están dentro de la celda del rótulo de texto y que la regla no retira: años con paréntesis y candidatas
      que quedan OK en las seis dimensiones en C18 (folios del pie de página, «As at January 1»);
  Q4  años sueltos, en cualquier posición: estado en C16 y en C18;
  Q5  filas reales del CSV cuyo token está dentro de la celda del rótulo de texto;
  Q6  recuentos con fecha de los planes de acciones y de las tablas de acciones: cuáles toman la regla en C18 y cuáles no.

Uso: python3 -I -B consultas_9.py --todas <jsonl.gz> --raiz <munger_v2_r1> --c18 <frente C19>
"""
import argparse
import csv
import gzip
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import arnes9 as H  # noqa: E402

PIE9 = re.compile(r"Universal Registration Document|enregistrement universel")
RECUENTO9 = re.compile(r"(?i)number of|nombre d|rights|droits|shares|actions|beneficiar|bénéficiaires|of which|dont")
FECHA9 = re.compile(r"(?i)\b\d{1,2}/\d{1,2}/20\d\d\b|\b(?:january|december)\s*,?\s*\d{1,2}\s*,?\s*20\d\d|\b\d{1,2}(?:er)?\s+(?:janvier|d[ée]cembre)\s+20\d\d")


def corta(s, n=110):
    s = re.sub(r"\s{2,}", "  ", s.strip())
    return s if len(s) <= n else s[:n - 1] + "…"


def dentro_del_rotulo(r, x):
    rot = r["rot"]
    ini = r["l"].find(rot) if rot else -1
    return ini >= 0 and ini <= x["a0"] and x["a1"] <= ini + len(rot) and bool(re.search(r"[^\W\d_]", rot))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--todas", required=True, type=Path)
    ap.add_argument("--raiz", required=True, type=Path)
    ap.add_argument("--c18", required=True, type=Path)
    a = ap.parse_args()
    with gzip.open(a.todas, "rt", encoding="utf-8") as f:
        R = [json.loads(l) for l in f]
    p = print
    p("Consultas de la revisión n.º 9 al barrido propio · C16 → C18")
    p()
    p("== Q1. Transiciones del estado de la fila por el motivo del ejercicio en C18 ==")
    c, cg = Counter(), Counter()
    for r in R:
        for x in r["toks"]:
            for y, g in x["G"].items():
                ea, en = H.estado(g["a"]), H.estado(g["n"])
                if ea != en:
                    dn = g.get("dn", {}).get("ejercicio", "")
                    m = "año del rótulo" if "es un año del rótulo" in dn else ("día de la fecha" if "es el día" in dn else "otro motivo")
                    c[(ea, en, m)] += 1
                    cg[(ea, en, m)] += r["g"]
    for k in sorted(c):
        p(f"  {k[0]:9} → {k[1]:9} · {k[2]:16} · {c[k]:5} ({cg[k]} en páginas del grupo)")
    p()
    p("== Q2. Tokens con el motivo «el token es el día de la fecha del rótulo de la fila» ==")
    for r in R:
        for x in r["toks"]:
            if x["tdr"] and "día" in x["tdr"]:
                rot = r["rot"]
                ini = r["l"].find(rot)
                p(f"  {r['doc']} p.{r['p']} l.{r['i'] + 1} g={r['g']} · «{x['tok']}» en las posiciones {x['a0']}–{x['a1']}: «{r['l'][max(0, x['a0'] - 10):x['a1'] + 10].strip()}» · "
                  f"rótulo «{rot}» en {ini}–{ini + len(rot)} · estados C16 → C18: {', '.join(y + ' ' + g['a'] + '→' + g['n'] for y, g in x['G'].items())}")
                p(f"       «{corta(r['l'], 130)}»")
    p()
    p("== Q3. Tokens dentro de la celda del rótulo de texto que la regla no retira ==")
    no_ret = [(r, x) for r in R for x in r["toks"] if dentro_del_rotulo(r, x) and not x["tdr"]]
    p(f"  tokens: {len(no_ret)}")
    par = [(r, x) for r, x in no_ret if re.fullmatch(r"\(?20\d\d\)?%?", x["tok"])]
    p(f"  con forma de año y algún paréntesis («2023)», «(2023», «(2023)»): {len(par)} · {dict(Counter(re.sub(chr(92) + 'd', '9', x['tok']) for _, x in par))}; "
      f"candidatas OK en las seis dimensiones en C18: {sum(1 for _, x in par for g in x['G'].values() if H.estado(g['n']) == 'OK')}; "
      f"ejercicio C16 → C18: {dict(Counter((g['a'][1], g['n'][1]) for _, x in par for g in x['G'].values()))}")
    ok = [(r, x, y, g) for r, x in no_ret for y, g in x["G"].items() if H.estado(g["n"]) == "OK"]
    clases = Counter()
    for r, x, y, g in ok:
        clases["folio del pie de página" if PIE9.search(r["rot"]) else ("«" + corta(r["rot"], 40) + "»")] += 1
    p(f"  candidatas OK en las seis dimensiones en C18: {len(ok)} (OK también en C16: {sum(1 for _, _, _, g in ok if H.estado(g['a']) == 'OK')}) · {dict(clases)}")
    for r, x, y, g in ok:
        if not PIE9.search(r["rot"]):
            p(f"      {r['doc']} p.{r['p']} l.{r['i'] + 1} · «{x['tok']}» declarado {y} · {g['n']} · {g.get('dn', {}).get('ejercicio', '')[:60]} · «{corta(r['l'], 70)}»")
    pies = [(r, x, y, g) for r, x, y, g in ok if PIE9.search(r["rot"])]
    p(f"      folios: {len(pies)} en {len({(r['doc'], r['p']) for r, _, _, _ in pies})} páginas; por publicación {dict(Counter(r['doc'] for r, _, _, _ in pies))}; "
      f"p. ej. {pies[0][0]['doc']} p.{pies[0][0]['p']} «{corta(pies[0][0]['l'], 70)}» · «{pies[0][1]['tok']}» declarado {pies[0][2]}" if pies else "      folios: 0")
    p()
    p("== Q4. Años sueltos (token «20AA», con o sin paréntesis), en cualquier posición: estado de la fila C16 → C18 ==")
    c = Counter()
    primera = []
    for r in R:
        for x in r["toks"]:
            if re.fullmatch(r"\(?20\d\d\)?", x["tok"]):
                for y, g in x["G"].items():
                    c[(H.estado(g["a"]), H.estado(g["n"]))] += 1
                    if H.estado(g["n"]) == "OK":
                        primera.append((r, x, y))
    p(f"  {dict(sorted(c.items()))}")
    p(f"  los que siguen OK en C18: {len(primera)}; en una línea que solo lleva el año: {sum(1 for r, _, _ in primera if r['l'].strip() == r['toks'][0]['tok'])}; "
      f"por número de celdas de la línea: {dict(Counter(r['nc'] for r, _, _ in primera))}")
    for r, x, y in primera[:8]:
        p(f"      {r['doc']} p.{r['p']} l.{r['i'] + 1} · «{x['tok']}» declarado {y} · «{corta(r['l'], 90)}»")
    p()
    p("== Q5. Filas reales del CSV cuyo token está dentro de la celda del rótulo de texto ==")
    N = H.Version("C18", a.c18, a.raiz)
    V = N.V
    with open(N.carpeta / "datos" / "cifras_fuente.csv", encoding="utf-8", newline="") as f:
        filas = [x for x in csv.DictReader(f, delimiter=";") if x["tipo"] == "tabla"]
    n = 0
    for fila in filas:
        doc, pag, idi = fila["doc"], int(fila["pagina"]), N.idioma(fila["doc"])
        L = N.lineas(doc, pag)
        cand = V.lineas_con("\n".join(L), fila["etiqueta"])
        occ = int(fila["ocurrencia"] or 0)
        if occ:
            cand = [cand[occ - 1]]
        for i, l in cand:
            sp = V.spans_numericos(l, idi)
            k = int(fila["pos"]) % len(sp)
            rot = V.rotulo(l)
            ini = l.find(rot)
            if ini <= sp[k][0] and sp[k][1] <= ini + len(rot) and re.search(r"[^\W\d_]", rot):
                n += 1
                p(f"  {fila['id']} · {doc} p.{pag} l.{i + 1} · «{fila['literal']}»")
    p(f"  {n} de {len(filas)} filas de tabla")
    p()
    p("== Q6. Recuentos con fecha: líneas con una fecha completa en su rótulo, o en la línea de rótulo de encima, cuyo rótulo unido habla de")
    p("       acciones, derechos o beneficiarios y que tienen alguna cifra a la derecha ==")
    con, sin = [], []
    for r in R:
        if not r["toks"]:
            continue
        unido = " ".join(r["pnf"]) if FECHA9.search(" ".join(r["pnf"])) else (" ".join(r["pf"]) if FECHA9.search(" ".join(r["pf"])) else None)
        if unido is None or not RECUENTO9.search(unido) or r["nt"] < 1:
            continue
        rot = r["rot"]
        fin = r["l"].find(rot) + len(rot)
        if not any(x["a0"] >= fin for x in r["toks"]):
            continue
        (con if r["ar_n"] is not None else sin).append((r, unido))
    p(f"  con la regla de la fecha del rótulo en C18: {len(con)} · sin ella: {len(sin)}")
    p("  con la regla (el rótulo que la regla ve es solo la última línea):")
    for r, unido in con:
        p(f"      {r['doc']} p.{r['p']} l.{r['i'] + 1} g={r['g']} · rótulo unido «{corta(unido, 70)}» · rótulo de la regla «{r['rds']}»")
    p("  sin la regla:")
    for r, unido in sin:
        p(f"      {r['doc']} p.{r['p']} l.{r['i'] + 1} g={r['g']} · C16 daba {r['ar_a']} · rótulo unido «{corta(unido, 90)}»")
    return 0


if __name__ == "__main__":
    sys.exit(main())
