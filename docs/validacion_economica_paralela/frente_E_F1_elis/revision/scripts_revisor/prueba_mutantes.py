"""Contraejemplos del revisor contra los scripts del autor (no modifica nada del autor).

Crea copias mutadas de datos/cifras_fuente.csv y datos/fuentes.json en una carpeta temporal y ejecuta sobre
ellas scripts/verificar_cifras.py y scripts/contraste_f1.py del autor con «python3 -I». Muestra qué mutaciones
pasan sin fallo.

Uso: python3 -I prueba_mutantes.py --raiz <ruta>/munger_v2_r1 --autor <carpeta frente_E_F1_elis> --libro <xlsx>
"""
import argparse
import csv
import json
import subprocess
import sys
import tempfile
from pathlib import Path


def escribir(filas, ruta):
    with ruta.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0].keys()), delimiter=";")
        w.writeheader()
        w.writerows(filas)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raiz", required=True, type=Path)
    ap.add_argument("--autor", required=True, type=Path)
    ap.add_argument("--libro", required=True, type=Path)
    a = ap.parse_args()
    verif, contr = a.autor / "scripts" / "verificar_cifras.py", a.autor / "scripts" / "contraste_f1.py"
    base = list(csv.DictReader((a.autor / "datos" / "cifras_fuente.csv").open(encoding="utf-8"), delimiter=";"))
    fuentes = json.loads((a.autor / "datos" / "fuentes.json").read_text(encoding="utf-8"))
    ref = json.loads((a.autor / "resultados" / "contraste_f1.json").read_text(encoding="utf-8"))

    def mut(cambios):
        filas = [dict(r) for r in base]
        for rid, c in cambios.items():
            hit = [r for r in filas if r["id"] == rid]
            assert len(hit) == 1, rid
            hit[0].update(c)
        return filas

    casos = [
        ("M1 columna de otro ejercicio con su literal: DA_ROU_2025 toma «(132.2)» (2024) y se declara 2025",
         mut({"DA_ROU_2025": {"pos": "-1", "literal": "(132.2)", "valor_publicado": "-132.2"}}), fuentes),
        ("M4 metadatos falsos: año 2031, unidad «mm EUR» para un porcentaje y perímetro «segmento Francia»",
         mut({"CREC_ORG_2025": {"anio": "2031", "unidad": "mm EUR"}, "IS_VENTAS_2025": {"perimetro": "segmento Francia"}}), fuentes),
    ]
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        for nombre, filas, fu in casos:
            escribir(filas, d / "c.csv")
            (d / "f.json").write_text(json.dumps(fu, ensure_ascii=False), encoding="utf-8")
            r1 = subprocess.run([sys.executable, "-I", str(verif), "--raiz", str(a.raiz), "--datos", str(d / "c.csv"),
                                 "--fuentes", str(d / "f.json"), "--salida", str(d / "v.json")], capture_output=True, text=True)
            print(f"\n{nombre}\n  verificar_cifras.py: código {r1.returncode} · {r1.stdout.strip().splitlines()[0] if r1.stdout.strip() else r1.stderr.strip()[-200:]}")
            if r1.returncode != 0:
                continue
            r2 = subprocess.run([sys.executable, "-I", str(contr), "--cifras", str(d / "c.csv"), "--verificacion", str(d / "v.json"),
                                 "--libro", str(a.libro), "--salida", str(d / "k.json"), "--informe", str(d / "k.md")],
                                capture_output=True, text=True)
            print(f"  contraste_f1.py: código {r2.returncode} · {r2.stdout.strip().splitlines()[0] if r2.stdout.strip() else r2.stderr.strip()[-200:]}")
            if r2.returncode == 0:
                k = json.loads((d / "k.json").read_text(encoding="utf-8"))
                for nom in ("R6 D&A en EBIT − suma de componentes", "R16 amortización ROU (nota 4.5) − amortización del movimiento de ROU"):
                    print(f"  residuo 2025 · {nom}: original {ref['tablas']['conciliaciones_residuos']['2025'][nom]} → mutado {k['tablas']['conciliaciones_residuos']['2025'][nom]}")
                for p in ("A1", "A2"):
                    o, m = ref["referencia_especificacion"]["perimetros"][p], k["referencia_especificacion"]["perimetros"][p]
                    print(f"  referencia {p}: f {o['f']:.9f} → {m['f']:.9f} · flujo sin crecimiento {o['flujo_sin_crecimiento']:.3f} → {m['flujo_sin_crecimiento']:.3f}")
        # M2/M3: fuente sin huella declarada o con huella vacía
        dos = base[:2]
        escribir(dos, d / "c2.csv")
        for nombre, edit in (("M2 fuente sin campo sha256", lambda f: f["fuentes"]["URD2025"].pop("sha256")),
                             ("M3 fuente con sha256 vacío", lambda f: f["fuentes"]["URD2025"].__setitem__("sha256", ""))):
            fu = json.loads(json.dumps(fuentes))
            edit(fu)
            (d / "f2.json").write_text(json.dumps(fu, ensure_ascii=False), encoding="utf-8")
            r = subprocess.run([sys.executable, "-I", str(verif), "--raiz", str(a.raiz), "--datos", str(d / "c2.csv"),
                                "--fuentes", str(d / "f2.json"), "--salida", str(d / "v2.json")], capture_output=True, text=True)
            ult = (r.stdout.strip().splitlines() or r.stderr.strip().splitlines() or [""])[0 if r.stdout.strip() else -1]
            print(f"\n{nombre}\n  verificar_cifras.py: código {r.returncode} · {ult[:160]}")


if __name__ == "__main__":
    main()
