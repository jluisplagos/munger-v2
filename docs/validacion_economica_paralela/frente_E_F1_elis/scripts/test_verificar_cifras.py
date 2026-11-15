"""Contraejemplos del verificador de cifras (frente E). Deben FALLAR todos los casos manipulados.

Cubre los huecos señalados por la revisión externa: página inexistente, fuente ausente o con otra huella,
redondeo presentado como cifra exacta y signo publicado invertido (R415-SIGNO). Uso:

  python3 -I test_verificar_cifras.py --raiz <ruta>/munger_v2_r1
"""
import argparse
import csv
import json
import subprocess
import sys
import tempfile
from pathlib import Path

AQUI = Path(__file__).resolve().parent
DATOS = AQUI.parent / "datos"


def ejecutar(raiz, filas, fuentes):
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        (d / "f.json").write_text(json.dumps(fuentes, ensure_ascii=False), encoding="utf-8")
        with (d / "c.csv").open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(filas[0].keys()), delimiter=";")
            w.writeheader()
            w.writerows(filas)
        r = subprocess.run([sys.executable, "-I", str(AQUI / "verificar_cifras.py"), "--raiz", str(raiz), "--datos", str(d / "c.csv"),
                            "--fuentes", str(d / "f.json"), "--salida", str(d / "s.json")], capture_output=True, text=True)
        return r.returncode, json.loads((d / "s.json").read_text(encoding="utf-8"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raiz", required=True, type=Path)
    a = ap.parse_args()
    fuentes = json.loads((DATOS / "fuentes.json").read_text(encoding="utf-8"))
    base = {r["id"]: r for r in csv.DictReader((DATOS / "cifras_fuente.csv").open(encoding="utf-8"), delimiter=";")}
    lease, rou = dict(base["CF_LEASE_2025"]), dict(base["DA_ROU_2025"])
    casos = []
    # 0. control positivo: las dos filas originales pasan
    casos.append(("control positivo", [lease, rou], fuentes, True))
    # 1. signo invertido: magnitud positiva frente a «(177.9)» publicado
    c = dict(lease); c["literal"] = "177.9"; c["valor_publicado"] = "177.9"
    casos.append(("signo invertido en el literal", [c], fuentes, False))
    c = dict(lease); c["valor_publicado"] = "177.9"
    casos.append(("signo invertido solo en el valor", [c], fuentes, False))
    # 2. redondeo presentado como exacto: 150 frente a (149.5)
    c = dict(rou); c["literal"] = "(150)"; c["valor_publicado"] = "-150"
    casos.append(("redondeo 150 frente a 149,5", [c], fuentes, False))
    c = dict(rou); c["valor_publicado"] = "-150"
    casos.append(("valor redondeado con literal correcto", [c], fuentes, False))
    # 3. página inexistente
    c = dict(lease); c["pagina"] = "999999"
    casos.append(("página inexistente", [c], fuentes, False))
    # 4. página existente pero distinta (la cifra no está allí)
    c = dict(lease); c["pagina"] = "326"
    casos.append(("página equivocada", [c], fuentes, False))
    # 5. fuente con otra huella
    f2 = json.loads(json.dumps(fuentes)); f2["fuentes"]["URD2025"]["sha256"] = "0" * 64
    casos.append(("fuente con huella distinta", [lease], f2, False))
    # 6. fuente ausente (ruta inexistente)
    f3 = json.loads(json.dumps(fuentes)); f3["fuentes"]["URD2025"]["archivo"] += ".no_existe"
    casos.append(("fuente ausente", [lease], f3, False))
    # 7. columna de otro año
    c = dict(lease); c["pos"] = "-1"
    casos.append(("columna de otro ejercicio", [c], fuentes, False))
    fallos = 0
    for nombre, filas, fu, debe_pasar in casos:
        cod, res = ejecutar(a.raiz, filas, fu)
        paso = cod == 0 and res["resumen"]["fallos"] == 0
        bien = paso == debe_pasar
        fallos += not bien
        print(("OK " if bien else "MAL"), nombre, "→", "pasa" if paso else "rechazado")
    print(f"{len(casos) - fallos}/{len(casos)} casos con el resultado esperado")
    return 1 if fallos else 0


if __name__ == "__main__":
    sys.exit(main())
