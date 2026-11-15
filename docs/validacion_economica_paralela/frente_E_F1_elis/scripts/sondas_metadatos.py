"""Sondas de metadatos: ¿comprueba el verificador la unidad y el perímetro declarados? (frente E · F1 · Elis)

Reproduce las dos sondas externas de `revision_chatgpt_1/seguimiento_eb77dea/` (rama auditoria/economica-f1, commit
e57239c), que cambian UN solo campo con el año correcto:
  - CREC_ORG_2025: unidad «%» → «mm EUR»;
  - IS_VENTAS_2025: perímetro «consolidado IFRS, grupo Elis» → «segmento Francia».
y las extiende a TODAS las filas de tabla, un campo cada vez: en una ejecución se cambia solo la unidad de cada fila
(«%» ↔ «mm EUR»); en otra, solo el perímetro (→ «segmento Francia»). El verificador evalúa cada fila por separado,
así que cambiar todas a la vez equivale a una sonda por fila. Una fila no detectada es cobertura que falta.

Se ejecuta con el verificador y los datos de la versión que se quiere probar (--autor), sin modificarlos.

Uso:  python3 -I sondas_metadatos.py --raiz <ruta>/munger_v2_r1 --autor <carpeta frente_E_F1_elis de esa versión> \\
          --etiqueta <commit> --salida <json>
"""
import argparse
import csv
import json
import subprocess
import sys
import tempfile
from pathlib import Path


def ejecutar(verif, raiz, fuentes, filas, d):
    with (d / "c.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0].keys()), delimiter=";")
        w.writeheader()
        w.writerows(filas)
    r = subprocess.run([sys.executable, "-I", str(verif), "--raiz", str(raiz), "--datos", str(d / "c.csv"), "--fuentes", str(fuentes),
                        "--salida", str(d / "v.json")], capture_output=True, text=True)
    v = json.loads((d / "v.json").read_text(encoding="utf-8")) if (d / "v.json").is_file() else None
    return r.returncode, v


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--raiz", required=True, type=Path)
    ap.add_argument("--autor", required=True, type=Path)
    ap.add_argument("--etiqueta", required=True)
    ap.add_argument("--salida", required=True, type=Path)
    a = ap.parse_args()
    verif, fuentes = a.autor / "scripts" / "verificar_cifras.py", a.autor / "datos" / "fuentes.json"
    base = list(csv.DictReader((a.autor / "datos" / "cifras_fuente.csv").open(encoding="utf-8"), delimiter=";"))
    tablas = [r["id"] for r in base if r["tipo"] == "tabla"]
    otra_unidad = {"%": "mm EUR", "mm EUR": "%"}

    def mut(campo, valor_de, ids):
        filas = [dict(r) for r in base]
        for r in filas:
            if r["id"] in ids:
                r[campo] = valor_de(r)
        return filas

    casos = [
        ("base sin cambios", [dict(r) for r in base], None, []),
        ("sonda externa: unidad de CREC_ORG_2025 «%» → «mm EUR»", mut("unidad", lambda r: "mm EUR", {"CREC_ORG_2025"}), "unidad", ["CREC_ORG_2025"]),
        ("sonda externa: perímetro de IS_VENTAS_2025 → «segmento Francia»", mut("perimetro", lambda r: "segmento Francia", {"IS_VENTAS_2025"}),
         "perimetro", ["IS_VENTAS_2025"]),
        ("unidad cambiada en cada fila de tabla («%» ↔ «mm EUR»)", mut("unidad", lambda r: otra_unidad.get(r["unidad"], "%"), set(tablas)), "unidad", tablas),
        ("perímetro cambiado en cada fila de tabla (→ «segmento Francia»)", mut("perimetro", lambda r: "segmento Francia", set(tablas)), "perimetro", tablas),
    ]
    out = {"version": a.etiqueta, "filas": len(base), "filas_de_tabla": len(tablas), "casos": []}
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        for nombre, filas, campo, ids in casos:
            cod, v = ejecutar(verif, a.raiz, fuentes, filas, d)
            res = {"caso": nombre, "codigo_salida": cod, "resumen": v["resumen"] if v else None}
            if v and ids:
                por_id = {r["id"]: r for r in v["cifras"]}
                detectadas = [i for i in ids if por_id[i]["estado"] == "FALLO"]
                en_su_dimension = [i for i in ids if (por_id[i].get("dimensiones") or {}).get(campo, {}).get("estado") == "FALLO"]
                no_detectadas = [i for i in ids if por_id[i]["estado"] != "FALLO"]
                res.update({"filas_mutadas": len(ids), "detectadas": len(detectadas),
                            "detectadas_en_la_dimension_del_campo": len(en_su_dimension),
                            "no_detectadas": no_detectadas[:50], "no_detectadas_total": len(no_detectadas)})
            out["casos"].append(res)
            print(f"{nombre}: código {cod}" + (f" · detectadas {res['detectadas']}/{res['filas_mutadas']}"
                                                 f" (en su dimensión: {res['detectadas_en_la_dimension_del_campo']})" if ids else ""))
    a.salida.parent.mkdir(parents=True, exist_ok=True)
    a.salida.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
