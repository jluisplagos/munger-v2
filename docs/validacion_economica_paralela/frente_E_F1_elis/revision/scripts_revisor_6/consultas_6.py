"""Revisión n.º 6 (frente E · F1 · Elis). Consultas que sostienen datos del informe y no salen de los demás scripts.
No modifica nada del autor.

  1. Motivos de las transiciones de fila OK → FALLO y OK → PENDIENTE del barrido (páginas del grupo), con sus páginas.
  2. Las transiciones por ejercicio que no son del balance del URD 2021, una a una, con su línea.
  3. Columnas que el verificador reconoce en la cabecera de las tablas de R1 y de R4, en cada versión, frente al número
     de cifras de la línea (si coinciden, la fila se asigna por orden).
  4. Valor en libros de las tablas de vencimientos de la deuda y de los arrendamientos, declarado del ejercicio de la
     publicación: estado en cada versión.
  5. Sublíneas «As a % of revenue» de las tablas de EBITDA por segmento: estado en la versión nueva.

Uso: python3 -I consultas_6.py --raiz <munger_v2_r1> --todas <barrido.jsonl.gz> --anterior C11=<carpeta> --nueva C13=<carpeta>
"""
import argparse
import gzip
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from arnes6 import DIMS, Modulo  # noqa: E402

E = {"URD2021": 2021, "URD2022": 2022, "URD2023": 2023, "DEU2024FR": 2024, "URD2025": 2025}
CLAVES = ("ejercicio", "variacion", "notas")


def est(e):
    return "FALLO" if any(x in ("FALLO", "NO_EVALUADO") for x in e) else "PENDIENTE" if "PENDIENTE" in e else "OK"


def plantilla(m):
    return re.sub(r"«[^»]*»", "«…»", re.sub(r"\b(19|20)\d\d\b", "AAAA", m or ""))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raiz", required=True)
    ap.add_argument("--todas", required=True)
    ap.add_argument("--anterior", required=True, help="NOMBRE=carpeta")
    ap.add_argument("--nueva", required=True, help="NOMBRE=carpeta")
    a = ap.parse_args()
    na, ca = a.anterior.split("=", 1)
    nn, cn = a.nueva.split("=", 1)
    Ma, Mn = Modulo(ca, a.raiz, "v_anterior"), Modulo(cn, a.raiz, "v_nueva")
    cache = {}

    def lineas(doc, p):
        if (doc, p) not in cache:
            cache[(doc, p)] = Mn.texto(doc, p).splitlines()
        return cache[(doc, p)]

    def linea(doc, p, i):
        return " ".join(lineas(doc, p)[i].split())

    with gzip.open(a.todas, "rt", encoding="utf-8") as g:
        T = [json.loads(l) for l in g]
    G = [r for r in T if r["g"]]
    print(f"Consultas sobre el barrido {na} → {nn}: {len(T)} candidatas, {len(G)} en páginas del grupo\n")

    # ---------------------------------------------------------------- 1
    for desde, hasta in (("OK", "FALLO"), ("OK", "PENDIENTE")):
        S = [r for r in G if est(r["a_e"]) == desde and est(r["n_e"]) == hasta]
        print(f"== 1. Fila {desde} → {hasta} (páginas del grupo): {len(S)} candidatas, por dimensión y motivo de {nn} ==")
        c, pp = Counter(), defaultdict(Counter)
        for r in S:
            k = " + ".join(f"{d}: {plantilla(r['n_d'].get(d))[:120]}" for d, e in zip(DIMS, r["n_e"]) if e == hasta)
            c[k] += 1
            pp[k][f"{r['doc']} p.{r['p']}"] += 1
        for k, n in c.most_common():
            print(f"  {n:4d} · {k}")
            print("         páginas: " + ", ".join(f"{p} ({m})" for p, m in pp[k].most_common(40)))
        print()

    # ---------------------------------------------------------------- 2
    print(f"== 2. Fila OK → FALLO por ejercicio fuera del balance del URD 2021 p.228 ==")
    for r in G:
        if est(r["a_e"]) == "OK" and est(r["n_e"]) == "FALLO" and r["n_e"][1] == "FALLO" and (r["doc"], r["p"]) != ("URD2021", 228):
            print(f"  {r['doc']} p.{r['p']} l.{r['i']+1} tok {r['idx']+1}/{r['n']} «{r['tok']}» declarado {r['anio']} · «{linea(r['doc'], r['p'], r['i'])[:80]}»"
                  f" · {nn}: {r['n_d'].get('ejercicio')}")
    print(f"\n== 2b. Fila OK → PENDIENTE por ejercicio ==")
    for r in G:
        if est(r["a_e"]) == "OK" and est(r["n_e"]) == "PENDIENTE" and r["n_e"][1] == "PENDIENTE":
            print(f"  {r['doc']} p.{r['p']} l.{r['i']+1} tok {r['idx']+1}/{r['n']} «{r['tok']}» declarado {r['anio']} · «{linea(r['doc'], r['p'], r['i'])[:80]}»")
    print()

    # ---------------------------------------------------------------- 3
    print("== 3. Columnas reconocidas en la cabecera frente a las cifras de la línea (iguales → asignación por orden) ==")
    CASOS = [("URD2022", 302, r"^\s*Lease liabilities\s", "vencimientos de arrendamientos (R1)"),
             ("URD2025", 366, r"^\s*Lease liabilities\s", "vencimientos de arrendamientos, caso B17/B18 de Q2"),
             ("URD2021", 269, r"^\s*Lease liabilities\s", "vencimientos de arrendamientos"),
             ("URD2025", 393, r"^\s*› of which Ireland", "impuesto por jurisdicción (R1)"),
             ("DEU2024FR", 338, r"^\s*dont Irlande", "impuesto por jurisdicción (R1)"),
             ("URD2023", 346, r"^\s*of which Ireland", "impuesto por jurisdicción (R1)"),
             ("URD2025", 371, r"^\s*Discount rate\s+9\.1%", "columnas por marca (R1)"),
             ("DEU2024FR", 317, r"^\s*Taux d'actualisation\s+9,3%", "columnas por marca (R1)"),
             ("URD2025", 402, r"^\s*TOTAL\s", "honorarios por firma auditora"),
             ("URD2022", 274, r"^\s*Intangible assets\s", "combinaciones de negocio, columnas por país (R4)")]
    for doc, p, rx, que in CASOS:
        L = lineas(doc, p)
        ii = [k for k, l in enumerate(L) if re.search(rx, l)]
        if not ii:
            print(f"  {doc} p.{p}: línea no encontrada ({rx})")
            continue
        i = ii[-1]
        idi = Mn.fuentes[doc]["idioma"]
        print(f"  {doc} p.{p} l.{i+1} · {que} · «{linea(doc, p, i)[:90]}»")
        for nom, M in ((na, Ma), (nn, Mn)):
            m = M.m
            zona = m.zona_de_cabecera(L, i, idi)
            cols = m.columnas_de_cabecera(L, zona, CLAVES) if zona else []
            n = len(m.spans_numericos(L[i], idi))
            metodo = "por orden" if cols and len(cols) == n else "por alineación" if cols else "sin columnas reconocidas"
            print(f"      {nom}: {n} cifras · {len(cols)} columnas reconocidas {[t for _, _, t in cols]} → {metodo}")
        if doc == "URD2022" and p == 274:
            m = Mn.m
            print(f"      {nn}: pais_de_columna para la columna de Alemania (posición 1): {m.pais_de_columna(L, i, 1, idi)!r}")
    print()

    # ---------------------------------------------------------------- 4
    print("== 4. Valor en libros (primera cifra) en las tablas de vencimientos, declarado del ejercicio de la publicación ==")
    for doc, p in (("URD2021", 279), ("URD2022", 312), ("URD2023", 331), ("DEU2024FR", 323), ("URD2025", 377)):
        S = [r for r in T if (r["doc"], r["p"]) == (doc, p) and r["idx"] == 0 and r["n"] >= 8 and r["anio"] == E[doc]]
        c = Counter(f"{est(r['a_e'])} → {est(r['n_e'])}" for r in S)
        ej = next((r for r in S if est(r["n_e"]) == "FALLO"), S[0] if S else None)
        print(f"  deuda · {doc} p.{p}: {len(S)} filas · {dict(c)}" + (f" · ej. «{ej['tok']}»: {ej['n_d'].get('ejercicio')}" if ej else ""))
    for doc, p in (("URD2021", 269), ("URD2022", 302), ("URD2023", 321), ("DEU2024FR", 312), ("URD2025", 366)):
        for r in T:
            if (r["doc"], r["p"]) == (doc, p) and r["n"] == 6 and r["idx"] in (0, 5) and r["anio"] == E[doc] and re.match(r"(?i)Lease liabilities|Passifs locatifs", r["rot"]):
                cual = "valor en libros" if r["idx"] == 0 else "total sin descontar"
                print(f"  arrendamientos · {doc} p.{p} l.{r['i']+1} · {cual} «{r['tok']}»: {est(r['a_e'])} → {est(r['n_e'])} · {r['n_d'].get('ejercicio')}")
    print()

    # ---------------------------------------------------------------- 5
    print(f"== 5. Sublíneas de margen de las tablas de EBITDA por segmento: estado en {nn} (candidatas por sublínea) ==")
    for doc, p in (("URD2021", 212), ("URD2022", 244), ("URD2023", 262), ("DEU2024FR", 254), ("URD2025", 308)):
        L = lineas(doc, p)
        por = defaultdict(Counter)
        for r in T:
            if (r["doc"], r["p"]) == (doc, p) and re.match(r"(?i)As a % of|En % d", r["rot"]):
                por[r["i"]][est(r["n_e"])] += 1
        for i in sorted(por):
            k = i - 1
            while k >= 0 and not L[k].strip():
                k -= 1
            print(f"  {doc} p.{p} l.{i+1} bajo «{' '.join(L[k].split())[:50]}»: {dict(por[i])}")


if __name__ == "__main__":
    main()
