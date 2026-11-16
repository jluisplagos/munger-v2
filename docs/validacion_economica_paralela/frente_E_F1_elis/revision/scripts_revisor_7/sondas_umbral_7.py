"""Revisión n.º 7 (frente E · F1 · Elis). Sondas de umbral sobre el contraste del autor (C14). No modifica nada del autor.

Qué comprueba, como caja negra: el intervalo «errores_sin_deteccion_entre_paginas» que contraste_f1.py declara desde C14
para cada entrada contrastada entre páginas. Para cada entrada se ejecuta el contraste del autor, como proceso aparte, con
esa sola entrada desplazada, y se mira qué residuos ENTRE PÁGINAS fallan:

  - justo dentro del intervalo (extremo ∓ δ) no debe fallar ninguno;
  - justo fuera (extremo ± δ) debe fallar alguno.

No usa los coeficientes que lleva el autor (q.t): solo el resultado de cada ejecución. El verificador se salta como lo
saltan test_contraste_residuos.py y cobertura_por_mutacion.py (una verificación que declara OK todas las filas y
corresponde al CSV cambiado), porque aquí se mide solo la segunda línea.

Además, para las entradas que nombran los documentos (ventas, crecimiento publicado, FCF antes de impuestos e impuestos
pagados de 2024) prueba errores de una y de dos unidades de la última cifra impresa, en los dos sentidos, y lista todo lo
que falla (entre páginas, misma página y libro). Y recuenta desde cuántas unidades ENTERAS de la última cifra detecta
alguna identidad entre páginas un error de cualquier signo.

Uso: python3 -I sondas_umbral_7.py --autor <frente C14> --libro <xlsx> [--procesos 4] [--delta 0.002]
"""
import argparse
import csv
import hashlib
import json
import subprocess
import sys
import tempfile
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from fractions import Fraction
from pathlib import Path


def decimal(fr):
    """Fracción decimal exacta como texto (para que Fraction(texto) la recupere sin error de coma flotante)."""
    s = f"{float(fr):.9f}".rstrip("0").rstrip(".")
    assert abs(Fraction(s) - fr) < Fraction(1, 10 ** 8), (s, fr)
    return s


class Banco:
    def __init__(self, autor, libro):
        self.autor, self.libro = Path(autor), Path(libro)
        self.base = list(csv.DictReader((self.autor / "datos" / "cifras_fuente.csv").open(encoding="utf-8"), delimiter=";"))
        self.campos = list(self.base[0].keys())
        self.verif = json.loads((self.autor / "resultados" / "verificacion_cifras.json").read_text(encoding="utf-8"))
        for r in self.verif["cifras"]:
            r["estado"] = "OK"
        self.verif["resumen"]["fallos"] = 0
        self.caja = self.autor / "resultados" / "caja_no_nula.json"

    def ejecutar(self, cambios):
        """cambios: {id: desplazamiento (Fraction)}. Devuelve (código, json del contraste o None)."""
        filas = [dict(r) for r in self.base]
        for r in filas:
            if r["id"] in cambios:
                r["valor_publicado"] = decimal(Fraction(r["valor_publicado"]) + cambios[r["id"]])
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            with (d / "c.csv").open("w", encoding="utf-8", newline="") as f:
                w = csv.DictWriter(f, fieldnames=self.campos, delimiter=";")
                w.writeheader()
                w.writerows(filas)
            v = json.loads(json.dumps(self.verif))
            v["huellas"]["datos"] = hashlib.sha256((d / "c.csv").read_bytes()).hexdigest()
            por_id = {r["id"]: r for r in filas}
            for r in v["cifras"]:
                r["literal"], r["valor_publicado"] = por_id[r["id"]]["literal"], por_id[r["id"]]["valor_publicado"]
            (d / "v.json").write_text(json.dumps(v, ensure_ascii=False), encoding="utf-8")
            r = subprocess.run([sys.executable, "-I", str(self.autor / "scripts" / "contraste_f1.py"), "--cifras", str(d / "c.csv"),
                                "--verificacion", str(d / "v.json"), "--libro", str(self.libro), "--caja-no-nula", str(self.caja),
                                "--salida", str(d / "k.json"), "--informe", str(d / "k.md")], capture_output=True, text=True)
            k = json.loads((d / "k.json").read_text(encoding="utf-8")) if (d / "k.json").is_file() else None
        return r.returncode, k


def fallos(k):
    """(residuos entre páginas que fallan, residuos de la misma página que fallan, otras de fuente, del libro)."""
    rc = k["tablas"]["residuos_con_cota"]
    entre, misma, otras, libro = [], [], [], 0
    for c in k["comprobaciones"]:
        if c["ok"]:
            continue
        if c["clase"] == "libro":
            libro += 1
        elif c["clase"] == "fuente" and c["nombre"].startswith("residuo "):
            cod, y = c["nombre"].split(" ")[1:3]
            (entre if rc[y][cod]["contraste"] == "entre páginas" else misma).append(f"{cod} {y}")
        elif c["clase"] == "fuente":
            otras.append(c["nombre"][:40])
    return sorted(entre), sorted(misma), otras, libro


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--autor", required=True)
    ap.add_argument("--libro", required=True)
    ap.add_argument("--procesos", type=int, default=4)
    ap.add_argument("--delta", default="0.002")
    a = ap.parse_args()
    B = Banco(a.autor, a.libro)
    cod0, k0 = B.ejecutar({})
    assert cod0 == 0 and k0 is not None, "el control sin cambios no pasa"
    ent = k0["tablas"]["cobertura_entradas"]["entradas"]
    con = {i: v for i, v in ent.items() if "errores_sin_deteccion_entre_paginas" in v}
    dec = {r["id"]: r["decimales"] for r in B.verif["cifras"] if "decimales" in r}
    delta = Fraction(a.delta)
    print(f"Entradas usadas: {len(ent)}; con intervalo declarado (contrastadas entre páginas): {len(con)}")
    print(f"Control sin cambios: código {cod0}, {k0['resumen']['comprobaciones']} comprobaciones, {k0['resumen']['fallidas']} fallidas\n")

    # 1. los cuatro extremos de cada intervalo
    tareas = []
    for i, v in con.items():
        lo, hi = (Fraction(str(x)) for x in v["errores_sin_deteccion_entre_paginas"])
        for nombre, e in (("dentro, por abajo", lo + delta), ("dentro, por arriba", hi - delta), ("fuera, por abajo", lo - delta),
                          ("fuera, por arriba", hi + delta)):
            tareas.append((i, nombre, e))

    def caso(t):
        i, nombre, e = t
        cod, k = B.ejecutar({i: e})
        return (i, nombre, e) + ((None,) * 4 if k is None else fallos(k))

    with ThreadPoolExecutor(max_workers=a.procesos) as ex:
        res = list(ex.map(caso, tareas))
    mal = []
    for i, nombre, e, entre, misma, otras, libro in res:
        if entre is None:
            mal.append((i, nombre, e, "el contraste no dio salida"))
        elif nombre.startswith("dentro") and entre:
            mal.append((i, nombre, e, f"falla {entre} dentro del intervalo declarado"))
        elif nombre.startswith("fuera") and not entre:
            mal.append((i, nombre, e, "no falla ninguna identidad entre páginas fuera del intervalo declarado"))
    print(f"== 1. Extremos de los intervalos declarados (δ = {a.delta}): {len(tareas)} ejecuciones del contraste ==")
    print(f"   intervalos confirmados en sus dos extremos: {len(con) - len({m[0] for m in mal})} de {len(con)}")
    for m in mal:
        print(f"   DISTINTO: {m[0]} · {m[1]} (error {float(m[2]):+.4f}): {m[3]}")

    # 2. una y dos unidades de la última cifra en las entradas que nombran los documentos
    print("\n== 2. Errores de una y de dos unidades de la última cifra impresa en las entradas que nombran los documentos ==")
    nombradas = [i for i in con if i.startswith(("IS_VENTAS", "VENTAS_SEG", "CREC_PUB_")) or i in ("FCF_ANTES_2024", "CF_IMPPAG_2024")]
    t2 = []
    for i in sorted(nombradas):
        u = Fraction(1, 10 ** dec[i])
        for n in (1, 2, -1, -2):
            t2.append((i, f"{n:+d} u", n * u))
    with ThreadPoolExecutor(max_workers=a.procesos) as ex:
        r2 = list(ex.map(caso, t2))
    por = {}
    for i, nombre, e, entre, misma, otras, libro in r2:
        por.setdefault(i, []).append((nombre, e, entre, misma, otras, libro))
    for i in sorted(por):
        v = con[i]
        print(f"   {i} {v['fuente']} · intervalo declarado {v['errores_sin_deteccion_entre_paginas']} · identidades entre páginas {v['identidades_entre_paginas']}")
        for nombre, e, entre, misma, otras, libro in por[i]:
            print(f"        error {float(e):+.3f} ({nombre}): entre páginas {entre or '—'} · misma página {misma or '—'} · libro {libro}"
                  + (f" · otras {otras}" if otras else ""))

    # 3. desde cuántas unidades enteras se detecta
    print("\n== 3. Menor número ENTERO de unidades de la última cifra que alguna identidad entre páginas detecta en los dos sentidos ==")
    print("   (del intervalo declarado [lo, hi]: n es el menor entero con n·u > hi y n·u > −lo; la comparación del contraste es |residuo| ≤ cota)")
    cuenta, tramo = Counter(), Counter()
    exactos = Counter()
    for i, v in con.items():
        lo, hi = (Fraction(str(x)) for x in v["errores_sin_deteccion_entre_paginas"])
        u = Fraction(1, 10 ** dec[i])
        m = max(hi, -lo) / u
        n = int(m) + 1
        cuenta[n] += 1
        t = "hasta 2" if m <= 2 else "de 2 a 5" if m <= 5 else "de 5 a 10" if m <= 10 else "más de 10"
        tramo[t] += 1
        if m == int(m):
            exactos[(t, int(m))] += 1
    print("   tramos del autor (umbral = max(−lo, hi) en unidades):", dict(tramo))
    print("   detectan desde n unidades enteras:", ", ".join(f"n = {n}: {c}" for n, c in sorted(cuenta.items())))
    print("   entradas cuyo umbral es un número entero exacto de unidades (un error de ese tamaño NO se detecta):",
          ", ".join(f"{t}, umbral {m}: {c}" for (t, m), c in sorted(exactos.items())))
    ej = [i for i, v in con.items() if float(v["umbral_en_unidades_de_la_ultima_cifra"]) == 2.0][:2]
    t3 = [(i, f"{n:+d} u", n * Fraction(1, 10 ** dec[i])) for i in ej for n in (2, 3, -2, -3)]
    with ThreadPoolExecutor(max_workers=a.procesos) as ex:
        r3 = list(ex.map(caso, t3))
    print("   ejemplos con umbral 2,0 (tramo «hasta 2»):")
    for i, nombre, e, entre, misma, otras, libro in r3:
        print(f"        {i} {con[i]['fuente']} intervalo {con[i]['errores_sin_deteccion_entre_paginas']} · error {float(e):+.2f} ({nombre}): entre páginas {entre or '—'}")

    # 4. entradas que mueven la referencia de la especificación y sus identidades entre páginas
    print("\n== 4. Entradas que mueven los valores de referencia de E9 (desplazamiento de +1,0) y sus identidades entre páginas ==")
    usadas = sorted(ent)

    def mueve(i):
        cod, k = B.ejecutar({i: Fraction(1)})
        return i, (k is not None and k.get("referencia_especificacion") != k0.get("referencia_especificacion"))

    with ThreadPoolExecutor(max_workers=a.procesos) as ex:
        r4 = dict(ex.map(mueve, usadas))
    mueven = [i for i in usadas if r4[i]]
    print(f"   mueven la referencia: {len(mueven)} de {len(usadas)} entradas usadas; por clase declarada: "
          f"{dict(Counter(ent[i]['estado'] for i in mueven))}")
    ids = Counter()
    for i in mueven:
        for x in ent[i]["identidades_entre_paginas"]:
            ids[x.split(" ")[0] + (" 2021–22" if x.split(" ")[1] in ("2021", "2022") else " 2023–25")] += 1
    print("   identidades entre páginas en las que intervienen (código y tramo de años: número de entradas):")
    print("      " + ", ".join(f"{k}: {n}" for k, n in sorted(ids.items(), key=lambda x: (x[0].split(' ')[1], int(x[0].split(' ')[0][1:])))))
    rng = [max(Fraction(str(ent[i]["errores_sin_deteccion_entre_paginas"][1])), -Fraction(str(ent[i]["errores_sin_deteccion_entre_paginas"][0]))) for i in mueven]
    print(f"   mayor error sin detectar de esas entradas: de {float(min(rng)):.2f} a {float(max(rng)):.2f}")
    ventas = [i for i in mueven if "VENTAS" in i]
    print(f"   ventas entre las que mueven la referencia: {ventas}")
    print(f"   ¿mueven la referencia las ventas de 2021 y 2022? IS_VENTAS_U22_2021: {r4.get('IS_VENTAS_U22_2021')}, IS_VENTAS_U23_2022: {r4.get('IS_VENTAS_U23_2022')}")
    rc = k0["tablas"]["residuos_con_cota"]
    print("   contraste de R25 y R23 en 2021–22 según el propio contraste: " +
          ", ".join(f"{c} {y}: {rc[y][c]['contraste']} {rc[y][c]['paginas']}" for y in ("2021", "2022") for c in ("R25", "R23") if c in rc[y]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
