"""Mutantes del revisor (revisión n.º 3) contra verificar_cifras.py y contraste_f1.py del autor (commit congelado).

No modifica nada del autor: escribe copias mutadas de datos/cifras_fuente.csv en una carpeta temporal y ejecuta sobre
ellas los scripts del autor con «python3 -I». Para cada mutante muestra el estado de las cinco dimensiones de la fila
mutada y, si el verificador no la rechaza (ningún FALLO en esa fila), el resultado de contraste_f1.py.

Uso: python3 -I prueba_mutantes_3.py --raiz <ruta>/munger_v2_r1 --autor <carpeta frente_E_F1_elis del autor> --libro <xlsx>
"""
import argparse
import csv
import json
import subprocess
import sys
import tempfile
from pathlib import Path

GRUPO = "consolidado IFRS, grupo Elis"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raiz", required=True, type=Path)
    ap.add_argument("--autor", required=True, type=Path)
    ap.add_argument("--libro", required=True, type=Path)
    a = ap.parse_args()
    verif, contr = a.autor / "scripts" / "verificar_cifras.py", a.autor / "scripts" / "contraste_f1.py"
    base = list(csv.DictReader((a.autor / "datos" / "cifras_fuente.csv").open(encoding="utf-8"), delimiter=";"))
    campos = list(base[0].keys())
    ref = json.loads((a.autor / "resultados" / "contraste_f1.json").read_text(encoding="utf-8"))

    def cambia(rid, **c):
        filas = [dict(r) for r in base]
        hit = [r for r in filas if r["id"] == rid]
        assert len(hit) == 1, rid
        hit[0].update(c)
        return rid, filas

    def nueva(rid, **c):
        fila = {k: "" for k in campos}
        fila.update(id=rid, tipo="tabla", ocurrencia="0", perimetro=GRUPO, edicion="vigente", unidad="mm EUR",
                    control_anio="dos_columnas", concepto="mutante del revisor")
        fila.update(c)
        return rid, [dict(r) for r in base] + [fila]

    casos = [
        ("K0 control: M1 de la revisión n.º 1 (DA_ROU_2025 toma «(132.2)» de 2024, modo por defecto)",
         cambia("DA_ROU_2025", pos="-1", literal="(132.2)", valor_publicado="-132.2")),
        ("A1 M1 con el modo declarado «crecimiento»",
         cambia("DA_ROU_2025", pos="-1", literal="(132.2)", valor_publicado="-132.2", control_anio="crecimiento")),
        ("A2 M1 con el modo declarado «max_cabecera»",
         cambia("DA_ROU_2025", pos="-1", literal="(132.2)", valor_publicado="-132.2", control_anio="max_cabecera")),
        ("A5 control: edición anterior declarada vigente (IS_EBIT_FR_2024, DEU 2024, 596,4)",
         cambia("IS_EBIT_FR_2024", edicion="vigente")),
        ("A4 edición anterior declarada vigente con el modo declarado «crecimiento»",
         cambia("IS_EBIT_FR_2024", edicion="vigente", control_anio="crecimiento")),
        ("B1 unidad: número de acciones (millones de acciones) bajo cabecera «In millions of euros» (URD 2025 p.313)",
         nueva("MUT_ACCIONES", anio="2025", doc="URD2025", pagina="313", etiqueta="Number of shares, basic (C)", pos="-2",
               literal="234.0", valor_publicado="234.0")),
        ("B2 unidad: euros por acción bajo la misma cabecera (URD 2025 p.313)",
         nueva("MUT_BPA", anio="2025", doc="URD2025", pagina="313", etiqueta="re:basic, attributable to owners of the parent = A/C",
               pos="-2", literal="2.00", valor_publicado="2.00")),
        ("C1 perímetro: margen de EBITDA de Francia («As a % of revenue», URD 2025 p.308) declarado del grupo",
         nueva("MUT_MARGEN_FR", anio="2025", doc="URD2025", pagina="308", etiqueta="As a % of revenue", ocurrencia="1", pos="-2",
               literal="41.9%", valor_publicado="41.9", unidad="%")),
        ("D1 concepto de columna: TAXDIF_INT_2025 toma «(0.9)» (combinaciones) en vez de «17.5» (resultado)",
         cambia("TAXDIF_INT_2025", pos="-5", literal="(0.9)", valor_publicado="-0.9")),
        ("D2 concepto de columna: CREC_ORG_2025 toma «+1.8%» (crecimiento externo) en vez de «+3.8%» (orgánico)",
         cambia("CREC_ORG_2025", pos="-3", literal="+1.8%", valor_publicado="1.8")),
        ("E1 control: tabla de 2024 de la p.348 declarada 2025 (modo titulo)",
         cambia("VENTAS_LINO_PLANO_2025", pagina="348", literal="2,104.3", valor_publicado="2104.3")),
        # Tabla con una tercera columna «Change» (URD 2025 p.308, EBITDA por región: «TOTAL 1,700.1 1,609.8 +5.6%»).
        # El modo por defecto supone que los dos últimos tokens son los dos ejercicios.
        ("F1 modo por defecto: el total de 2024 «1,609.8» (pos −2 por la columna «Change») declarado 2025",
         nueva("MUT_EBITDA_2025", anio="2025", doc="URD2025", pagina="308", etiqueta="re:^\\s*TOTAL\\s{2,}", pos="-2",
               literal="1,609.8", valor_publicado="1609.8")),
        ("F2 falso positivo: el total correcto de 2025 «1,700.1» (pos −3) declarado 2025 en el modo por defecto",
         nueva("MUT_EBITDA_2025_OK", anio="2025", doc="URD2025", pagina="308", etiqueta="re:^\\s*TOTAL\\s{2,}", pos="-3",
               literal="1,700.1", valor_publicado="1700.1")),
        ("F3 falso positivo: el total correcto de 2024 «1,609.8» (pos −2) declarado 2024 en el modo por defecto",
         nueva("MUT_EBITDA_2024_OK", anio="2024", doc="URD2025", pagina="308", etiqueta="re:^\\s*TOTAL\\s{2,}", pos="-2",
               literal="1,609.8", valor_publicado="1609.8")),
    ]
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        for nombre, (rid, filas) in casos:
            with (d / "c.csv").open("w", encoding="utf-8", newline="") as f:
                w = csv.DictWriter(f, fieldnames=campos, delimiter=";")
                w.writeheader()
                w.writerows(filas)
            r1 = subprocess.run([sys.executable, "-I", str(verif), "--raiz", str(a.raiz), "--datos", str(d / "c.csv"),
                                 "--fuentes", str(a.autor / "datos" / "fuentes.json"), "--salida", str(d / "v.json")],
                                capture_output=True, text=True)
            print(f"\n{nombre}")
            try:
                v = json.loads((d / "v.json").read_text(encoding="utf-8"))
            except Exception as e:  # noqa: BLE001
                print(f"  verificar_cifras.py: código {r1.returncode}, sin salida legible ({e})")
                continue
            e = [c for c in v["cifras"] if c["id"] == rid][0]
            dims = {k: x["estado"] for k, x in e["dimensiones"].items()}
            print(f"  verificar_cifras.py: código {r1.returncode} · fila {rid}: {e['estado']} · {dims}")
            for k, x in e["dimensiones"].items():
                if x["estado"] not in ("OK", "NO_APLICA"):
                    print(f"    {k}: {x.get('detalle', '')[:150]}")
            if e["estado"] == "FALLO":
                continue
            if not all(c["estado"] != "FALLO" for c in v["cifras"]):
                continue
            r2 = subprocess.run([sys.executable, "-I", str(contr), "--cifras", str(d / "c.csv"), "--verificacion", str(d / "v.json"),
                                 "--libro", str(a.libro), "--caja-no-nula", str(a.autor / "resultados" / "caja_no_nula.json"),
                                 "--salida", str(d / "k.json"), "--informe", str(d / "k.md")], capture_output=True, text=True)
            primera = (r2.stdout.strip().splitlines() or [r2.stderr.strip()[-200:]])[0]
            print(f"  contraste_f1.py: código {r2.returncode} · {primera[:230]}")
            try:
                k = json.loads((d / "k.json").read_text(encoding="utf-8"))
            except Exception:  # noqa: BLE001
                continue
            malas = [c["nombre"] for c in k["comprobaciones"] if not c["ok"]]
            print(f"    comprobaciones fallidas: {len(malas)} {malas[:4]}")
            if rid == "TAXDIF_INT_2025":
                print("    tabla de impuestos 2025, diferido de intangibles:",
                      {x: y for x, y in k["tablas"]["impuestos"]["2025"].items() if "intang" in x.lower()},
                      "| original:", {x: y for x, y in ref["tablas"]["impuestos"]["2025"].items() if "intang" in x.lower()})
            if rid == "CREC_ORG_2025":
                o = ref["tablas"]["alternativas"]; m = k["tablas"]["alternativas"]
                for n in o:
                    for kk in o[n]:
                        if "organico" in kk and o[n][kk] != m[n][kk]:
                            print(f"    {n.split(':')[0]} · {kk[:22]}: {o[n][kk]} → {m[n][kk]}")


if __name__ == "__main__":
    main()
