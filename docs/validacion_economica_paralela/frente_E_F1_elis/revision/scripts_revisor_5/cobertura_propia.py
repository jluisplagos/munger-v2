"""Revisión n.º 5 (frente E · F1 · Elis). Recuento propio de la cobertura de las entradas que usa contraste_f1.py.
No modifica nada del autor.

El autor declara en `cobertura_entradas` la clase de cada entrada (identidad entre páginas, solo de su página, solo la
Historia del libro, sin segunda línea) con la contabilidad interna de contraste_f1.py. Su prueba de mutación no distingue
las dos primeras clases: en las dos «falla una identidad de fuente». Aquí la clase de cada entrada se deriva de su
comportamiento, sin leer esa contabilidad:

  1. se suma 3,0 a «valor_publicado» de una entrada (una cada vez), con una verificación que declara OK todas las filas y
     corresponde al CSV mutado (se salta la primera línea de defensa, como en las pruebas del autor);
  2. se anotan las comprobaciones que fallan. El tipo de cada residuo se deriva aquí: es «entre páginas» si las entradas
     cuya mutación lo hace fallar están en dos páginas o más del CSV, y «misma página» si están en una. Se compara con el
     tipo y las páginas que declara el autor para ese residuo;
  3. clase derivada: entre páginas, si falla algún residuo entre páginas; solo misma página, si solo fallan residuos de
     una página; solo libro, si solo fallan comprobaciones contra el libro; sin detectar, si cambia alguna salida y no
     falla nada; sin efecto, si no cambia nada;
  4. se compara con la clase declarada, se recuentan las páginas sin ninguna entrada contrastada entre páginas y se mira
     si la mutación mueve `referencia_especificacion`.

Además lista, para las identidades entre páginas, las que tienen una contraparte PENDIENTE en el verificador.

Uso: python3 -I cobertura_propia.py --autor <frente C11> --libro <xlsx> [--procesos 4]
"""
import argparse
import csv
import hashlib
import json
import subprocess
import sys
import tempfile
from collections import Counter, defaultdict
from multiprocessing import Pool
from pathlib import Path

DECL = {"contrastada entre páginas": "entre páginas", "solo identidad de la misma página": "solo misma página",
        "contrastada con la Historia del libro": "solo libro", "sin comprobación de segunda línea": "sin segunda línea"}
_G = {}


def preparar(autor, libro):
    autor = Path(autor)
    with (autor / "datos" / "cifras_fuente.csv").open(encoding="utf-8") as f:
        base = list(csv.DictReader(f, delimiter=";"))
    _G.update(autor=autor, libro=str(libro), base=base, campos=list(base[0].keys()),
              v0=json.loads((autor / "resultados" / "verificacion_cifras.json").read_text(encoding="utf-8")),
              k0=json.loads((autor / "resultados" / "contraste_f1.json").read_text(encoding="utf-8")))


def contraste(filas):
    """(código, salida JSON o None) de contraste_f1.py con una verificación que declara OK todo y corresponde a filas."""
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        with (d / "c.csv").open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=_G["campos"], delimiter=";")
            w.writeheader()
            w.writerows(filas)
        v = json.loads(json.dumps(_G["v0"]))
        v["huellas"]["datos"] = hashlib.sha256((d / "c.csv").read_bytes()).hexdigest()
        por_id = {r["id"]: r for r in filas}
        for r in v["cifras"]:
            r["estado"] = "OK"
            r["literal"], r["valor_publicado"] = por_id[r["id"]]["literal"], por_id[r["id"]]["valor_publicado"]
        v["resumen"]["fallos"] = 0
        (d / "v.json").write_text(json.dumps(v, ensure_ascii=False), encoding="utf-8")
        a = _G["autor"]
        r = subprocess.run([sys.executable, "-I", str(a / "scripts" / "contraste_f1.py"), "--cifras", str(d / "c.csv"), "--verificacion",
                            str(d / "v.json"), "--libro", _G["libro"], "--caja-no-nula", str(a / "resultados" / "caja_no_nula.json"),
                            "--salida", str(d / "k.json"), "--informe", str(d / "k.md")], capture_output=True, text=True)
        k = json.loads((d / "k.json").read_text(encoding="utf-8")) if (d / "k.json").is_file() else None
        return r.returncode, k


def mutar(idf):
    from fractions import Fraction
    filas = [dict(r) for r in _G["base"]]
    hit = [r for r in filas if r["id"] == idf]
    hit[0]["valor_publicado"] = str(float(Fraction(hit[0]["valor_publicado"]) + 3))
    cod, k = contraste(filas)
    if k is None:
        return idf, {"aborta": True}
    k0 = _G["k0"]
    fallan = [c for c in k["comprobaciones"] if not c["ok"]]
    tipos = []
    for c in fallan:
        if c["nombre"].startswith("residuo "):
            _, cod_r, anio = c["nombre"].split(" ")[:3]
            tipos.append(k["tablas"]["residuos_con_cota"][anio][cod_r]["contraste"])
    # no cuentan las tablas que describen la cobertura o las pendientes: cambian por la verificación que declara OK todo
    aparte = ("cobertura_entradas", "contrapartes_de_identidad_pendientes", "entradas_usadas_pendientes")
    cambia = [t for t in k["tablas"] if t not in aparte and k["tablas"][t] != k0["tablas"][t]]
    return idf, {"aborta": False, "residuos": sorted({c["nombre"] for c in fallan if c["nombre"].startswith("residuo ")}),
                 "tipos": sorted(set(tipos)), "otras_fuente": sum(1 for c in fallan if c["clase"] == "fuente" and not c["nombre"].startswith("residuo ")),
                 "libro": sum(1 for c in fallan if c["clase"] == "libro"), "tablas": cambia,
                 "referencia": k["referencia_especificacion"] != k0["referencia_especificacion"]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--autor", required=True)
    ap.add_argument("--libro", required=True)
    ap.add_argument("--procesos", type=int, default=4)
    a = ap.parse_args()
    preparar(a.autor, a.libro)
    k0 = _G["k0"]
    cod, kb = contraste(_G["base"])
    assert kb is not None and kb["referencia_especificacion"] == k0["referencia_especificacion"] and all(c["ok"] for c in kb["comprobaciones"]), "base"
    ce = k0["tablas"]["cobertura_entradas"]
    decl = {i: DECL[v["estado"]] for i, v in ce["entradas"].items()}
    por_id = {r["id"]: r for r in _G["base"]}
    vigentes = [r["id"] for r in _G["base"] if r["tipo"] == "tabla" and r["edicion"] == "vigente"]
    print(f"Entradas que el contraste declara usadas: {len(decl)} · filas de tabla de la edición vigente (mutadas): {len(vigentes)}")
    print("Declarado por el autor: " + " · ".join(f"{k} {n}" for k, n in Counter(decl.values()).most_common()))
    with Pool(a.procesos, initializer=preparar, initargs=(a.autor, a.libro)) as pool:
        res = dict(pool.map(mutar, vigentes, chunksize=4))

    # Tipo de cada residuo, derivado aquí: las entradas cuya mutación lo hace fallar y las páginas del CSV de esas entradas.
    # No se usa el campo «contraste» del autor; se compara con él.
    pag_csv = {r["id"]: f"{r['doc']} p.{r['pagina']}" for r in _G["base"]}
    ent_de = defaultdict(set)
    for i, m in res.items():
        for r in m.get("residuos", []):
            ent_de[r].add(i)
    tipo = {r: ("entre páginas" if len({pag_csv[i] for i in e}) >= 2 else "misma página") for r, e in ent_de.items()}
    distintos = []
    for r, e in sorted(ent_de.items()):
        _, cod_r, anio = r.split(" ")[:3]
        d = k0["tablas"]["residuos_con_cota"][anio][cod_r]
        if d["contraste"] != tipo[r] or sorted(d["paginas"]) != sorted({pag_csv[i] for i in e}):
            distintos.append((r, d["contraste"], tipo[r]))
    print(f"\nResiduos que alguna mutación hace fallar: {len(tipo)} de {sum(len(v) for v in k0['tablas']['residuos_con_cota'].values())} · "
          f"entre páginas {sum(1 for t in tipo.values() if t == 'entre páginas')}, de una página {sum(1 for t in tipo.values() if t == 'misma página')} · "
          f"tipo o páginas distintos de los que declara el autor: {len(distintos)} {distintos[:6]}")
    for m in res.values():
        if not m["aborta"]:
            m["tipos"] = sorted({tipo[r] for r in m["residuos"]})

    def clase(m):
        if m["aborta"]:
            return "aborta"
        if "entre páginas" in m["tipos"]:
            return "entre páginas"
        if "misma página" in m["tipos"]:
            return "solo misma página"
        if m["otras_fuente"]:
            return "solo otra comprobación de fuente"
        if m["libro"]:
            return "solo libro"
        return "sin detectar" if (m["tablas"] or m["referencia"]) else "sin efecto"

    der = {i: clase(m) for i, m in res.items()}
    print("\n== Clase derivada por mutación frente a clase declarada (entradas usadas) ==")
    cruz = Counter((decl[i], der[i]) for i in decl)
    for (d, r), n in sorted(cruz.items()):
        print(f"   declarada «{d}» · derivada «{r}»: {n}")
    equivalentes = {("sin segunda línea", "sin detectar"), ("sin segunda línea", "sin efecto")}
    dif = [(i, decl[i], der[i]) for i in decl if decl[i] != der[i] and (decl[i], der[i]) not in equivalentes]
    print(f"   discrepancias: {len(dif)} {dif[:12]}")
    fuera = sorted(i for i in vigentes if i not in decl and der[i] != "sin efecto")
    print(f"   filas de la edición vigente que el contraste no declara usadas: {sum(1 for i in vigentes if i not in decl)}; su mutación cambia algo en: {len(fuera)} {fuera[:8]}")

    print("\n== Recuento propio ==")
    n = Counter(der[i] for i in decl)
    print(f"   entre páginas {n['entre páginas']} · solo misma página {n['solo misma página']} · solo libro {n['solo libro']} · "
          f"sin segunda línea {n['sin detectar'] + n['sin efecto']} (sin detectar {n['sin detectar']}, leídas sin efecto {n['sin efecto']})")

    pag = {i: f"{por_id[i]['doc']} p.{por_id[i]['pagina']}" for i in decl}
    con_ancla = {pag[i] for i in decl if der[i] == "entre páginas"}
    sin = defaultdict(list)
    for i in sorted(decl):
        if pag[i] not in con_ancla:
            sin[pag[i]].append(i)
    n_ent = sum(len(v) for v in sin.values())
    print(f"\n== Páginas con entradas usadas: {len(set(pag.values()))} · sin ninguna entrada contrastada entre páginas: {len(sin)}, con {n_ent} entradas ==")
    for p, ids in sorted(sin.items()):
        cl = Counter(der[i] for i in ids)
        print(f"   {p}: {len(ids)} · {dict(cl)} · {', '.join(ids)}")
    print(f"   de ellas, con solo identidad de su página: {sum(1 for v in sin.values() for i in v if der[i] == 'solo misma página')}")
    igual = sorted(sin) == sorted(ce["paginas_sin_identidad_entre_paginas"]) and all(sorted(sin[p]) == sorted(ce["paginas_sin_identidad_entre_paginas"][p]) for p in sin)
    print(f"   coincide con `paginas_sin_identidad_entre_paginas` del autor: {'sí' if igual else 'NO'}")

    print("\n== ¿Mueve la mutación los valores de referencia de la especificación? ==")
    for nombre, ids in (("entradas de las páginas sin identidad entre páginas", [i for v in sin.values() for i in v]),
                        ("entradas con solo identidad de su página", [i for i in decl if der[i] == "solo misma página"]),
                        ("entradas con solo el libro", [i for i in decl if der[i] == "solo libro"]),
                        ("entradas sin segunda línea", [i for i in decl if der[i] in ("sin detectar", "sin efecto")]),
                        ("entradas contrastadas entre páginas", [i for i in decl if der[i] == "entre páginas"])):
        mueven = sorted(i for i in ids if res[i]["referencia"])
        print(f"   {nombre}: {len(ids)} · mueven la referencia: {len(mueven)} {mueven[:10]}{' …' if len(mueven) > 10 else ''}")
    ref = sorted(i for i in decl if res[i]["referencia"])
    print(f"   entradas que mueven la referencia: {len(ref)} · por clase derivada: {dict(Counter(der[i] for i in ref))}")
    solo_misma_ref = sorted(i for i in ref if der[i] != "entre páginas")
    print(f"   de ellas, sin identidad entre páginas: {len(solo_misma_ref)} {solo_misma_ref}")

    print("\n== Identidades entre páginas con una contraparte PENDIENTE en el verificador ==")
    pend = {r["id"] for r in _G["v0"]["cifras"] if r["estado"] == "PENDIENTE"}
    usadas_pend = sorted(pend & set(decl))
    print(f"   entradas usadas en estado PENDIENTE: {usadas_pend}")
    for i in usadas_pend:
        afect = sorted(j for j in decl if j != i and set(res[j]["residuos"]) & set(res[i]["residuos"]))
        for j in afect:
            otros = [r for r in res[j]["residuos"] if r not in res[i]["residuos"]]
            print(f"   {j}: comparte {sorted(set(res[j]['residuos']) & set(res[i]['residuos']))} con {i}; otros residuos entre páginas que la detectan: "
                  f"{[r for r in otros if k0['tablas']['residuos_con_cota'][r.split(' ')[2]][r.split(' ')[1]]['contraste'] == 'entre páginas']}; clase derivada: {der[j]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
