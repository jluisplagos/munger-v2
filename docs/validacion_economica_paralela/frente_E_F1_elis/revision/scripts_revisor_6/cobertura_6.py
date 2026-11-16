"""Revisión n.º 6 (frente E · F1 · Elis). Cobertura de las entradas por SENSIBILIDAD y por TABLA. No modifica nada del autor.

El autor clasifica cada entrada por pertenencia: «contrastada entre páginas» si interviene, con cualquier coeficiente, en
una identidad cuyas cifras están en dos páginas o más. La revisión n.º 5 derivó la misma clase por comportamiento con una
mutación de +3,0. Aquí se mide otra cosa:

  1. el coeficiente de cada entrada en cada identidad afirmada (una ejecución del contraste del autor por entrada, con la
     entrada aumentada en 1 y el verificador saltado, como en cobertura_por_mutacion.py);
  2. con el residuo y la cota de cada identidad, el menor error de cada signo que la hace fallar (umbral de detección);
     para una entrada, el umbral garantizado entre páginas es el mayor de los dos signos del mejor conjunto de identidades
     entre páginas. Se expresa también en unidades de la última cifra impresa;
  3. qué entradas mueven los valores de referencia de la especificación, y con qué umbral están contrastadas entre páginas;
  4. el anclaje por tabla, no por página: la tabla de una entrada es la declaración de unidades más próxima por encima de
     su línea. Una entrada con solo identidad de su página puede estar en una página «anclada» y en una tabla que no lo está.

Uso: python3 -I cobertura_6.py --raiz <munger_v2_r1> --autor <frente C13> --libro <xlsx> [--procesos 4]
"""
import argparse
import csv
import hashlib
import json
import re
import subprocess
import sys
import tempfile
import unicodedata
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from fractions import Fraction
from pathlib import Path

UNIDADES = re.compile(r"\((?:[Ii]n|[Ee]n)\s+(?:millions?|thousands?|milliers|milliards|billions?|euros|%|number|nombre)\b")


def ejecutar(autor, filas, campos, verif, libro):
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        with (d / "c.csv").open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=campos, delimiter=";")
            w.writeheader()
            w.writerows(filas)
        v = json.loads(json.dumps(verif))
        v["huellas"]["datos"] = hashlib.sha256((d / "c.csv").read_bytes()).hexdigest()
        por_id = {r["id"]: r for r in filas}
        for r in v["cifras"]:
            r["literal"], r["valor_publicado"] = por_id[r["id"]]["literal"], por_id[r["id"]]["valor_publicado"]
        (d / "v.json").write_text(json.dumps(v, ensure_ascii=False), encoding="utf-8")
        r = subprocess.run([sys.executable, "-I", str(autor / "scripts" / "contraste_f1.py"), "--cifras", str(d / "c.csv"), "--verificacion",
                            str(d / "v.json"), "--libro", str(libro), "--caja-no-nula", str(autor / "resultados" / "caja_no_nula.json"),
                            "--salida", str(d / "k.json"), "--informe", str(d / "k.md")], capture_output=True, text=True)
        return json.loads((d / "k.json").read_text(encoding="utf-8")) if (d / "k.json").is_file() else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raiz", required=True, type=Path)
    ap.add_argument("--autor", required=True, type=Path)
    ap.add_argument("--libro", required=True, type=Path)
    ap.add_argument("--procesos", type=int, default=4)
    a = ap.parse_args()
    base = list(csv.DictReader((a.autor / "datos" / "cifras_fuente.csv").open(encoding="utf-8"), delimiter=";"))
    campos = list(base[0].keys())
    meta = {r["id"]: r for r in base}
    fuentes = json.loads((a.autor / "datos" / "fuentes.json").read_text(encoding="utf-8"))["fuentes"]
    verif = json.loads((a.autor / "resultados" / "verificacion_cifras.json").read_text(encoding="utf-8"))
    dec = {r["id"]: r.get("decimales", 1) for r in verif["cifras"]}
    for r in verif["cifras"]:
        r["estado"] = "OK"
    verif["resumen"]["fallos"] = 0
    k0 = ejecutar(a.autor, base, campos, verif, a.libro)
    assert k0 is not None and k0["resumen"]["fallidas"] == 0
    decl = k0["tablas"]["cobertura_entradas"]["entradas"]
    usadas = sorted(decl)
    tipo = {}
    for y, d in k0["tablas"]["residuos_con_cota"].items():
        for cod, x in d.items():
            tipo[f"residuo {cod} {y}"] = (x["contraste"], x["paginas"])
    fuente0 = {c["nombre"]: c for c in k0["comprobaciones"] if c["clase"] == "fuente"}

    def clave(nombre):
        return nombre.split(" dentro")[0]

    def caso(i):
        filas = [dict(r) for r in base]
        hit = next(r for r in filas if r["id"] == i)
        hit["valor_publicado"] = str(float(Fraction(hit["valor_publicado"]) + 1))
        k = ejecutar(a.autor, filas, campos, verif, a.libro)
        if k is None:
            return i, None
        coef = {}
        for c in k["comprobaciones"]:
            if c["clase"] == "fuente":
                d = c["diferencia"] - fuente0[c["nombre"]]["diferencia"]
                if abs(d) > 5e-7:
                    coef[c["nombre"]] = d
        libro = sum(1 for c in k["comprobaciones"] if c["clase"] == "libro" and not c["ok"])
        ref = k.get("referencia_especificacion") != k0.get("referencia_especificacion")
        return i, {"coef": coef, "libro": libro, "ref": ref}

    with ThreadPoolExecutor(max_workers=a.procesos) as ex:
        res = dict(ex.map(caso, usadas))
    assert all(v is not None for v in res.values()), "alguna ejecución no terminó"

    def umbrales(i, solo):
        """(menor error positivo, menor error negativo en valor absoluto) que hace fallar alguna identidad del conjunto «solo»."""
        mas, menos, quien = float("inf"), float("inf"), (None, None)
        for nombre, c in res[i]["coef"].items():
            t = tipo.get(clave(nombre), ("doble vía del FCF base", []))[0]
            if t not in solo:
                continue
            r0, T = fuente0[nombre]["diferencia"], fuente0[nombre]["tolerancia"]
            s = 1 if c > 0 else -1
            up, dn = (T - s * r0) / abs(c), (T + s * r0) / abs(c)
            if up < mas:
                mas, quien = up, (clave(nombre).replace("residuo ", ""), quien[1])
            if dn < menos:
                menos, quien = dn, (quien[0], clave(nombre).replace("residuo ", ""))
        return max(mas, 0.0), max(menos, 0.0), quien

    w = print
    w(f"Entradas que el contraste declara usadas: {len(usadas)} · declarado: {k0['tablas']['cobertura_entradas']['resumen']}")
    w(f"Comprobaciones de fuente: {len(fuente0)} ({sum(1 for n in fuente0 if clave(n) in tipo)} residuos: "
      f"{sum(1 for v in tipo.values() if v[0] == 'entre páginas')} entre páginas y {sum(1 for v in tipo.values() if v[0] == 'misma página')} de la misma página)")

    # ------------------------------------------------------------------ 1. clase por pertenencia, reproducida
    w("\n== 1. Clase por pertenencia, derivada de los coeficientes (una entrada interviene en una identidad si su coeficiente no es cero) ==")
    propia = {}
    for i in usadas:
        ts = {tipo.get(clave(n), ("doble vía",))[0] for n in res[i]["coef"]}
        propia[i] = ("contrastada entre páginas" if "entre páginas" in ts else "solo identidad de la misma página" if "misma página" in ts
                     else "contrastada con la Historia del libro" if res[i]["libro"] else "sin comprobación de segunda línea")
    w(f"   {dict(Counter(propia.values()))}")
    dif = [i for i in usadas if propia[i] != decl[i]["estado"]]
    w(f"   distintas de la clase declarada por el autor: {len(dif)} {[(i, decl[i]['estado'], propia[i]) for i in dif][:8]}")

    # ------------------------------------------------------------------ 2. umbral de detección entre páginas
    w("\n== 2. Umbral de detección de las entradas «contrastadas entre páginas» (menor error que alguna identidad entre páginas detecta) ==")
    w("   Para cada entrada: umbral con error positivo y con error negativo; el umbral garantizado es el mayor de los dos.")
    filas_u = []
    for i in usadas:
        if decl[i]["estado"] != "contrastada entre páginas":
            continue
        mas, menos, quien = umbrales(i, {"entre páginas"})
        ult = 10.0 ** (-int(dec.get(i, 1)))
        filas_u.append((max(mas, menos), i, mas, menos, quien, ult))
    tramos = Counter()
    for g, i, mas, menos, quien, ult in filas_u:
        n = g / ult
        tramos["hasta 2 unidades de la última cifra" if n <= 2.0000001 else "de 2 a 5 unidades" if n <= 5.0000001 else
               "de 5 a 10 unidades" if n <= 10.0000001 else "más de 10 unidades"] += 1
    for t in ("hasta 2 unidades de la última cifra", "de 2 a 5 unidades", "de 5 a 10 unidades", "más de 10 unidades"):
        w(f"   {tramos[t]:4d}  {t}")
    w("   Entradas con umbral garantizado de más de 5 unidades de la última cifra impresa (umbral +, umbral −, identidades que lo dan):")
    for g, i, mas, menos, quien, ult in sorted(filas_u, reverse=True):
        if g / ult > 5.0000001:
            w(f"      {i:<24} {meta[i]['doc']} p.{meta[i]['pagina']} «{meta[i]['literal']}» · +{mas:.2f} ({quien[0]}) / −{menos:.2f} ({quien[1]}) · "
              f"entre páginas: {decl[i]['identidades_entre_paginas']} · misma página: {decl[i]['identidades_misma_pagina']} · Historia: {'sí' if decl[i]['historia_del_libro'] else 'no'}"
              f" · mueve la referencia: {'sí' if res[i]['ref'] else 'no'}")

    # ------------------------------------------------------------------ 3. entradas que mueven la referencia
    w("\n== 3. Entradas que mueven los valores de referencia de la especificación (mutación de +1,0) ==")
    mueven = [i for i in usadas if res[i]["ref"]]
    w(f"   total: {len(mueven)} · por clase declarada: {dict(Counter(decl[i]['estado'] for i in mueven))}")
    w(f"   entradas que NO están contrastadas entre páginas y mueven la referencia: {[i for i in mueven if decl[i]['estado'] != 'contrastada entre páginas']}")
    um = {i: umbrales(i, {"entre páginas"}) for i in mueven}
    tr = Counter()
    for i in mueven:
        n = max(um[i][0], um[i][1]) / 10.0 ** (-int(dec.get(i, 1)))
        tr["hasta 2 unidades de la última cifra" if n <= 2.0000001 else "de 2 a 5 unidades" if n <= 5.0000001 else
           "de 5 a 10 unidades" if n <= 10.0000001 else "más de 10 unidades"] += 1
    w(f"   umbral garantizado entre páginas de esas {len(mueven)}: {dict(tr)}")
    for i in sorted(mueven, key=lambda i: -max(um[i][0], um[i][1])):
        if max(um[i][0], um[i][1]) / 10.0 ** (-int(dec.get(i, 1))) > 2.0000001:
            w(f"      {i:<24} «{meta[i]['literal']}» · +{um[i][0]:.2f} / −{um[i][1]:.2f} · entre páginas: {decl[i]['identidades_entre_paginas']} · Historia: {'sí' if decl[i]['historia_del_libro'] else 'no'}")
    solo_r42 = [i for i in usadas if decl[i]["identidades_entre_paginas"] and all(x.startswith("R42 ") for x in decl[i]["identidades_entre_paginas"])]
    w(f"   entradas cuya única identidad entre páginas es R42: {len(solo_r42)}")
    for i in solo_r42:
        mas, menos, quien = umbrales(i, {"entre páginas"})
        w(f"      {i:<24} «{meta[i]['literal']}» · umbral +{mas:.3f} / −{menos:.3f} · misma página: {decl[i]['identidades_misma_pagina']} · Historia: {'sí' if decl[i]['historia_del_libro'] else 'no'}"
          f" · mueve la referencia: {'sí' if res[i]['ref'] else 'no'}")

    # ------------------------------------------------------------------ 4. anclaje por tabla
    w("\n== 4. Anclaje por tabla (la tabla de una entrada: la declaración de unidades más próxima por encima de su línea) ==")
    cache = {}

    def lineas(doc, p):
        if (doc, p) not in cache:
            r = subprocess.run(["pdftotext", "-q", "-layout", "-f", str(p), "-l", str(p), str(a.raiz / fuentes[doc]["archivo"]), "-"], capture_output=True, check=True)
            cache[(doc, p)] = unicodedata.normalize("NFKC", r.stdout.decode("utf-8", errors="replace")).replace("’", "'").replace("‘", "'").splitlines()
        return cache[(doc, p)]

    tabla_de, sin_linea = {}, []
    for i in usadas:
        m = meta[i]
        ls = lineas(m["doc"], int(m["pagina"]))
        etq = m["etiqueta"]
        cand = [n for n, l in enumerate(ls) if (re.search(etq[3:], l) if etq.startswith("re:") else etq in l)]
        occ = int(m["ocurrencia"] or 0)
        if not cand or (occ and occ > len(cand)):
            sin_linea.append(i)
            continue
        n = cand[occ - 1] if occ else cand[0]
        j = next((q for q in range(n - 1, max(-1, n - 90), -1) if UNIDADES.search(ls[q])), None)
        tabla_de[i] = (m["doc"], int(m["pagina"]), j)
    w(f"   entradas con su línea localizada: {len(tabla_de)} de {len(usadas)}; sin localizar: {sin_linea}")
    tablas = defaultdict(list)
    for i, t in tabla_de.items():
        tablas[t].append(i)
    ancladas = {t for t, ids in tablas.items() if any(decl[i]["estado"] == "contrastada entre páginas" for i in ids)}
    paginas = defaultdict(list)
    for i in usadas:
        paginas[(meta[i]["doc"], int(meta[i]["pagina"]))].append(i)
    pag_ancladas = {p for p, ids in paginas.items() if any(decl[i]["estado"] == "contrastada entre páginas" for i in ids)}
    w(f"   páginas con entradas: {len(paginas)}; sin ninguna entrada contrastada entre páginas: {len(paginas) - len(pag_ancladas)} "
      f"(con {sum(len(v) for p, v in paginas.items() if p not in pag_ancladas)} entradas)  ← lo que declara el autor")
    w(f"   tablas con entradas: {len(tablas)}; sin ninguna entrada contrastada entre páginas: {len(tablas) - len(ancladas)} "
      f"(con {sum(len(v) for t, v in tablas.items() if t not in ancladas)} entradas)")
    w("   Tablas sin ninguna entrada contrastada entre páginas que están en una página que el autor cuenta como anclada:")
    extra = 0
    for t, ids in sorted(tablas.items(), key=lambda x: (x[0][0], x[0][1], x[0][2] or -1)):
        if t in ancladas or (t[0], t[1]) not in pag_ancladas:
            continue
        extra += len(ids)
        ls = lineas(t[0], t[1])
        cab = re.sub(r"\s{2,}", "  ", ls[t[2]].strip())[:70] if t[2] is not None else "(sin declaración de unidades por encima)"
        w(f"      {t[0]} p.{t[1]} l.{(t[2] or 0) + 1} «{cab}»: {len(ids)} entradas · {dict(Counter(decl[i]['estado'] for i in ids))}")
        for i in ids:
            w(f"            {i:<24} «{meta[i]['literal']}» · {decl[i]['estado']} · misma página: {decl[i]['identidades_misma_pagina']} · mueve la referencia: {'sí' if res[i]['ref'] else 'no'}")
    w(f"   entradas en esas tablas: {extra}")
    misma = [i for i in usadas if decl[i]["estado"] == "solo identidad de la misma página"]
    w(f"   de las {len(misma)} entradas con solo identidad de su página: en una página sin ancla {sum(1 for i in misma if (meta[i]['doc'], int(meta[i]['pagina'])) not in pag_ancladas)}"
      f" (autor) · en una tabla sin ancla {sum(1 for i in misma if i in tabla_de and tabla_de[i] not in ancladas)} (por tabla)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
