"""Revisión independiente n.º 8 · el recuento nuevo `detecta_desde_unidades` del contraste, como caja negra.

Para cada entrada que el contraste declara «contrastada entre páginas», el autor da en C16 `detecta_desde_unidades`: el
menor número entero n de unidades de la última cifra impresa con el que un error, en los DOS sentidos, hace fallar alguna
identidad entre páginas. Aquí no se usan sus coeficientes ni sus intervalos: se ejecuta su `contraste_f1.py`, sin cambios,
con esa sola entrada desplazada +n, −n, +(n−1) y −(n−1) unidades, y se mira qué residuos «entre páginas» fallan:

  - con ±n deben fallar los dos sentidos;
  - con n−1 (si n ≥ 2), al menos un sentido no debe hacer fallar ninguno (si no, n no sería el menor);
  - además, para comprobar que n es de verdad el MENOR, se prueban todos los enteros de 1 a n−1.

El verificador se salta como en `cobertura_por_mutacion.py` del autor: la verificación falsa declara OK todas las filas y
se hace corresponder con cada CSV mutado. Trabaja sobre copias temporales; no modifica nada del autor.

También comprueba las frases de S6 c: un error de 0,1 exacto en las ventas no hace fallar R23 ni R40 y uno de 0,2 sí.

Uso: python3 -I -B sondas_8.py --autor <frente C17> --libro <xlsx> [--procesos 4]
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--autor", required=True, type=Path)
    ap.add_argument("--libro", required=True, type=Path)
    ap.add_argument("--procesos", type=int, default=4)
    a = ap.parse_args()
    contraste = a.autor / "scripts" / "contraste_f1.py"
    caja = a.autor / "resultados" / "caja_no_nula.json"
    with (a.autor / "datos" / "cifras_fuente.csv").open(encoding="utf-8", newline="") as f:
        base = list(csv.DictReader(f, delimiter=";"))
    campos = list(base[0].keys())
    verif = json.loads((a.autor / "resultados" / "verificacion_cifras.json").read_text(encoding="utf-8"))
    decimales = {r["id"]: r.get("decimales") for r in verif["cifras"]}
    for r in verif["cifras"]:
        r["estado"] = "OK"
    verif["resumen"]["fallos"] = 0
    guardado = json.loads((a.autor / "resultados" / "contraste_f1.json").read_text(encoding="utf-8"))
    ent = guardado["tablas"]["cobertura_entradas"]["entradas"]

    def ejecutar(cambios, referencia=False):
        """cambios: {id: desplazamiento (Fraction)}. Devuelve (código, residuos entre páginas que fallan, todos los que fallan);
        con referencia=True, el tercer valor es `referencia_especificacion`."""
        filas = [dict(r) for r in base]
        for r in filas:
            if r["id"] in cambios:
                r["valor_publicado"] = str(float(Fraction(r["valor_publicado"]) + cambios[r["id"]]))
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
            r = subprocess.run([sys.executable, "-I", "-B", str(contraste), "--cifras", str(d / "c.csv"), "--verificacion", str(d / "v.json"),
                                "--libro", str(a.libro), "--caja-no-nula", str(caja), "--salida", str(d / "k.json"), "--informe", str(d / "k.md")],
                               capture_output=True, text=True)
            if not (d / "k.json").is_file():
                return r.returncode, None, None
            k = json.loads((d / "k.json").read_text(encoding="utf-8"))
        rc = k["tablas"]["residuos_con_cota"]
        entre = sorted(f"{c} {y}" for y, dd in rc.items() for c, x in dd.items() if x["contraste"] == "entre páginas" and not x["ok"])
        todos = sorted(f"{c} {y}" for y, dd in rc.items() for c, x in dd.items() if not x["ok"])
        if referencia:
            return r.returncode, entre, k.get("referencia_especificacion")
        return r.returncode, entre, todos

    cod0, e0, t0 = ejecutar({})
    print(f"Control sin cambios: código {cod0}; residuos que fallan: {t0}")
    objetivos = sorted(i for i, v in ent.items() if "detecta_desde_unidades" in v)
    print(f"Entradas con `detecta_desde_unidades`: {len(objetivos)} (de {len(ent)} usadas)")
    print(f"Recuento declarado: {dict(sorted(Counter(ent[i]['detecta_desde_unidades'] for i in objetivos).items()))}")
    print(f"Recuento en umbrales_entre_paginas: {guardado['tablas']['cobertura_entradas']['umbrales_entre_paginas'].get('detecta_desde_unidades')}")

    def sonda(i):
        n = ent[i]["detecta_desde_unidades"]
        u = Fraction(1, 10 ** decimales[i])
        res = {}
        for m in range(1, n + 1):
            for s in (1, -1):
                cod, entre, _ = ejecutar({i: s * m * u})
                res[(m, s)] = None if entre is None else bool(entre)
        return i, n, res

    with ThreadPoolExecutor(max_workers=a.procesos) as ex:
        resultados = list(ex.map(sonda, objetivos))
    ejec = sum(len(r) for _, _, r in resultados)
    malos, propio = [], Counter()
    for i, n, res in resultados:
        if any(v is None for v in res.values()):
            malos.append((i, n, "el contraste aborta con alguna sonda"))
            continue
        menor = next((m for m in range(1, n + 1) if res[(m, 1)] and res[(m, -1)]), None)
        propio[menor] += 1
        if menor != n:
            malos.append((i, n, f"menor número de unidades con detección en los dos sentidos según la sonda: {menor}"))
    print()
    print(f"== 1. `detecta_desde_unidades` frente a la sonda: {ejec} ejecuciones del contraste ==")
    print(f"   entradas en las que el valor declarado es el menor entero con detección en los dos sentidos: {len(resultados) - len(malos)} de {len(resultados)}")
    print(f"   recuento propio: {dict(sorted((k, v) for k, v in propio.items() if k is not None))}")
    for i, n, m in malos:
        print(f"   DISTINTA: {i} · declarado {n} · {m}")
    solo_uno = [(i, n) for i, n, res in resultados if n >= 2 and (res[(n - 1, 1)] != res[(n - 1, -1)])]
    print(f"   entradas en las que n−1 unidades se detectan en un sentido y no en el otro: {len(solo_uno)}")
    print()
    print("== 2. Frases de S6 c: ventas contrastadas entre páginas «por encima de ±0,1» ==")
    for i in sorted((i for i in ent if i.startswith(("IS_VENTAS_", "VENTAS_SEG_")) and "errores_sin_deteccion_entre_paginas" in ent[i]),
                    key=lambda x: (ent[x]["usos"][0][-4:], x)):
        fila = []
        for d in ("0.1", "-0.1", "0.2", "-0.2"):
            cod, entre, _ = ejecutar({i: Fraction(d)})
            fila.append(f"{d}: {', '.join(entre) if entre else 'ningún residuo entre páginas falla'}")
        print(f"   {i} ({', '.join(ent[i]['usos'])}) · intervalo declarado {ent[i].get('errores_sin_deteccion_entre_paginas')} · " + " | ".join(fila))


    print()
    print("== 3. Entradas que mueven la referencia de E9 y sus identidades entre páginas (S6 e) ==")
    ref0 = guardado["referencia_especificacion"]
    usadas = sorted(ent)

    def mueve(i):
        cod, entre, ref = ejecutar({i: Fraction(1)}, referencia=True)
        return i, (ref is not None and ref != ref0), cod

    with ThreadPoolExecutor(max_workers=a.procesos) as ex:
        mov = list(ex.map(mueve, usadas))
    movedoras = [i for i, m, _ in mov if m]
    print(f"   entradas usadas: {len(usadas)}; con +1,0 cambian `referencia_especificacion`: {len(movedoras)}; abortan: {sum(1 for _, _, c in mov if c not in (0, 1, 2))}")
    print(f"   por clase declarada: {dict(Counter(ent[i]['estado'] for i in movedoras))}")
    ids = Counter()
    for i in movedoras:
        for x in ent[i]["identidades_entre_paginas"]:
            c, y = x.split(" ")
            ids[(c, "2021–22" if y in ("2021", "2022") else "2023–25")] += 1
    for periodo in ("2021–22", "2023–25"):
        print(f"   identidades entre páginas en las que interviene alguna de ellas, {periodo}: "
              + ", ".join(f"{c} ({n})" for (c, pp), n in sorted(ids.items(), key=lambda kv: (int(kv[0][0][1:]), kv[0][1])) if pp == periodo))
    umb = [float(ent[i]["umbral_en_unidades_de_la_ultima_cifra"]) * 10 ** (-decimales[i]) for i in movedoras]
    print(f"   mayor error sin detección de esas entradas: de {min(umb):.3f} a {max(umb):.3f}")
    rc0 = guardado["tablas"]["residuos_con_cota"]
    for c in ("R23", "R25", "R35", "R36"):
        print(f"   {c} en 2021 y 2022: " + "; ".join(f"{y}: {rc0[y][c]['contraste']}, intervienen {sum(1 for i in movedoras if f'{c} {y}' in ent[i]['identidades_entre_paginas'] + ent[i]['identidades_misma_pagina'])} de las que mueven la referencia"
                                                       for y in ("2021", "2022") if c in rc0[y]))


if __name__ == "__main__":
    main()
