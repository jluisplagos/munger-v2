"""Pruebas de la segunda línea de defensa de contraste_f1.py: los residuos de conciliación (frente E · F1 · Elis).

verificar_cifras.py es la primera línea: rechaza una cifra de otro ejercicio, unidad, perímetro o edición. Aquí se le
SALTA a propósito: cada caso muta datos/cifras_fuente.csv y entrega a contraste_f1.py una verificación que declara OK
todas las filas. Así se comprueba que los residuos, por sí solos, hacen fallar el cálculo cuando una cifra está mal, y
que la diferencia de concepto fijada (R13 de 2025, +0,4) no absorbe un error nuevo en sus cifras.

Cada residuo se afirma con su cota de redondeo (media unidad de la última cifra impresa de cada cifra que interviene).
Por debajo de esa cota ninguna identidad puede detectar un error: el último caso lo documenta.

Uso:  python3 -I test_contraste_residuos.py --libro <ruta>/Elis_v63_evaluada.xlsx
"""
import argparse
import csv
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ_F = AQUI.parent


def ejecutar(filas, verif, libro, caducada=False):
    """caducada=False: la verificación falsa se hace corresponder con el CSV mutado (huella y valores), como haría un
    verificador defectuoso que lo declarase todo OK. caducada=True: se entrega la verificación original sin tocar."""
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        with (d / "c.csv").open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(filas[0].keys()), delimiter=";")
            w.writeheader()
            w.writerows(filas)
        v = json.loads(json.dumps(verif))
        if not caducada:
            v["huellas"]["datos"] = hashlib.sha256((d / "c.csv").read_bytes()).hexdigest()
            por_id = {r["id"]: r for r in filas}
            for r in v["cifras"]:
                r["literal"], r["valor_publicado"] = por_id[r["id"]]["literal"], por_id[r["id"]]["valor_publicado"]
        (d / "v.json").write_text(json.dumps(v, ensure_ascii=False), encoding="utf-8")
        r = subprocess.run([sys.executable, "-I", str(AQUI / "contraste_f1.py"), "--cifras", str(d / "c.csv"), "--verificacion",
                            str(d / "v.json"), "--libro", str(libro), "--salida", str(d / "k.json"), "--informe", str(d / "k.md")],
                           capture_output=True, text=True)
        k = json.loads((d / "k.json").read_text(encoding="utf-8")) if (d / "k.json").is_file() else None
        return r.returncode, k, r.stderr.strip()[-300:]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--libro", required=True, type=Path)
    a = ap.parse_args()
    base = list(csv.DictReader((RAIZ_F / "datos" / "cifras_fuente.csv").open(encoding="utf-8"), delimiter=";"))
    verif = json.loads((RAIZ_F / "resultados" / "verificacion_cifras.json").read_text(encoding="utf-8"))
    # verificación que declara OK todas las filas: se salta el verificador para probar solo los residuos
    for r in verif["cifras"]:
        r["estado"] = "OK"
    verif["resumen"]["fallos"] = 0

    def mut(cambios):
        filas = [dict(r) for r in base]
        for i, c in cambios.items():
            hit = [r for r in filas if r["id"] == i]
            assert len(hit) == 1, i
            hit[0].update(c)
        return filas

    casos = [
        ("control: datos sin mutar", mut({}), 0, set()),
        ("M1 (contraste externo): DA_ROU_2025 toma 132,2 de 2024", mut({"DA_ROU_2025": {"literal": "(132.2)", "valor_publicado": "-132.2"}}),
         1, {"residuo R6 2025", "residuo R16 2025"}),
        ("error nuevo en una cifra de la diferencia fijada: principal 2025 148,0 en lugar de 148,3",
         mut({"LS_PRINC_PAS_2025": {"valor_publicado": "-148.0"}}), 1, {"residuo R13 2025"}),
        ("error nuevo en el gasto devengado de 2025: 29,5 en lugar de 29,2", mut({"FIN_INTLS_2025": {"valor_publicado": "-29.5"}}),
         1, {"residuo R13 2025"}),
        ("error nuevo en el FCF publicado de 2024: 346,0 en lugar de 346,3", mut({"FCF_FCF_2024": {"valor_publicado": "346.0"}}),
         1, {"residuo R11 2024"}),
        ("ventas 2025 de otra página con un dígito cambiado (4.769,8)", mut({"IS_VENTAS_2025": {"valor_publicado": "4769.8"}}),
         1, {"residuo R23 2025"}),
        ("límite de detección: 0,05 en la amortización ROU de 2025, dentro de la cota de redondeo",
         mut({"DA_ROU_2025": {"valor_publicado": "-149.55"}}), None, set()),
        # revisión n.º 3
        ("H5: la amortización ROU de 2022 toma «(30.3)», la línea de otros artículos arrendados",
         mut({"DA_ROU_U23_2022": {"literal": "(30.3)", "valor_publicado": "-30.3"}}), 1, {"residuo R25 2022", "residuo R16 2022"}),
        ("límite de detección de la diferencia fijada (N6, H3a): gasto devengado de 2025 en 29,3",
         mut({"FIN_INTLS_2025": {"valor_publicado": "-29.3"}}), None, set()),
        ("límite de detección de la diferencia fijada (H3b): gasto devengado de 2025 en 29,1",
         mut({"FIN_INTLS_2025": {"valor_publicado": "-29.1"}}), None, set()),
        ("límite de detección de la diferencia fijada (H3c): pagos de arrendamientos de 2025 en 178,0",
         mut({"CF_LEASE_2025": {"valor_publicado": "-178.0"}}), None, set()),
        ("D2 con el verificador saltado: crecimiento externo de 2025 como orgánico", mut({"CREC_ORG_2025": {"literal": "+1.8%", "valor_publicado": "1.8"}}),
         1, {"residuo R32 2025"}),
        # cobertura por mutación sobre C7: el circulante de 2021–22 entra en el C53 de referencia y tenía solo la Historia del libro
        ("circulante de 2021 que entra en el ancla de S2C: clientes 77,8 en lugar de 76,8", mut({"CF_CLI_U22_2021": {"valor_publicado": "-77.8"}}),
         1, {"residuo R5 2021"}),
        # C9: segundas presentaciones del impuesto, las adquisiciones y las ventas de 2020 del ancla de S2C
        ("impuesto de 2022 con la cifra original del URD 2022 (80,5) en lugar de la reexpresada (79,7)",
         mut({"IS_IMP_U23_2022": {"valor_publicado": "-80.5"}}), 1, {"residuo R17 2022"}),
        ("ventas de 2020 con dos dígitos permutados (2.860,3)", mut({"IS_VENTAS_U21_2020": {"valor_publicado": "2860.3"}}),
         1, {"residuo R40 2021"}),
        ("adquisiciones de 2022 de la columna de otra sociedad (146,2)", mut({"CF_ADQ_U23_2022": {"valor_publicado": "-146.2"}}),
         1, {"residuo R39 2022"}),
        ("límite: adquisiciones de 2021 con la cifra publicada antes de la reexpresión (86,9) en lugar de la reexpresada (86,8)",
         mut({"CF_ADQ_U22_2021": {"valor_publicado": "-86.9"}}), None, set()),
    ]
    malos = 0
    # H2 (revisión n.º 3, N3): CSV cambiado después de verificar y verificación original → el contraste no calcula
    filas_h2 = mut({"DA_ROU_U23_2022": {"valor_publicado": "-93.7"}})
    cod, k, err = ejecutar(filas_h2, json.loads((RAIZ_F / "resultados" / "verificacion_cifras.json").read_text(encoding="utf-8")),
                           a.libro, caducada=True)
    bien = cod == 1 and "no corresponde a este CSV" in err
    malos += not bien
    print("OK " if bien else "MAL", "H2: verificación de otro CSV (cambiado después de verificar)", "" if bien else f"→ código {cod}: {err}")
    for nombre, filas, cod_esp, deben_fallar in casos:
        cod, k, err = ejecutar(filas, verif, a.libro)
        problemas = []
        if k is None:
            problemas.append(f"sin salida ({err})")
        else:
            fallidas = {c["nombre"] for c in k["comprobaciones"] if not c["ok"]}
            residuos_fallidos = {n.split(" dentro")[0] for n in fallidas if n.startswith("residuo ")}
            if cod_esp is not None and cod != cod_esp:
                problemas.append(f"código {cod}, se esperaba {cod_esp}")
            faltan = deben_fallar - residuos_fallidos
            if faltan:
                problemas.append(f"no fallan {sorted(faltan)}")
            if not deben_fallar and residuos_fallidos:
                problemas.append(f"fallan residuos inesperados {sorted(residuos_fallidos)}")
            if cod_esp is None:
                otros = sorted(n for n in fallidas if not n.startswith("residuo "))
                nombre += f" → ningún residuo lo detecta; comprobaciones contra el libro que sí: {len(otros)}"
        malos += bool(problemas)
        print("OK " if not problemas else "MAL", nombre, "" if not problemas else "→ " + "; ".join(problemas))
    print(f"{len(casos) + 1 - malos}/{len(casos) + 1} casos con el resultado esperado")
    return 1 if malos else 0


if __name__ == "__main__":
    sys.exit(main())
