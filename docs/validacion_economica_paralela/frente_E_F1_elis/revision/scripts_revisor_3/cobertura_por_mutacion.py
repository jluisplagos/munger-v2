"""Cobertura por mutación de las entradas de contraste_f1.py del autor (revisión n.º 3; solo lectura del material del autor).

Para cada fila de tabla de la edición vigente de datos/cifras_fuente.csv se altera «valor_publicado» en +delta (por
defecto 3,0: mayor que el doble de cualquier cota de redondeo) y se ejecuta contraste_f1.py del autor con una verificación
que declara OK todas las filas (igual que hace su test_contraste_residuos.py: se salta la primera línea de defensa para
medir la segunda). Cada entrada queda en una de estas clases:

  no usada             ninguna salida cambia;
  identidad de fuente  falla al menos un residuo afirmado (R1–R24) o la doble vía de C52;
  solo libro           no falla ninguna identidad de fuente, pero sí alguna comprobación contra el libro;
  aborta               contraste_f1.py termina sin informe (se anota el motivo);
  SIN DETECTAR         cambia alguna tabla o valor de referencia y no falla ninguna comprobación.

Uso: python3 -I cobertura_por_mutacion.py --autor <carpeta frente_E_F1_elis del autor> --libro <xlsx> [--delta 3] [--procesos 4]
"""
import argparse
import csv
import json
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from fractions import Fraction
from pathlib import Path


def ejecutar(contr, filas, campos, verif_txt, libro, caja):
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        with (d / "c.csv").open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=campos, delimiter=";")
            w.writeheader()
            w.writerows(filas)
        (d / "v.json").write_text(verif_txt, encoding="utf-8")
        r = subprocess.run([sys.executable, "-I", str(contr), "--cifras", str(d / "c.csv"), "--verificacion", str(d / "v.json"),
                            "--libro", str(libro), "--caja-no-nula", str(caja), "--salida", str(d / "k.json"),
                            "--informe", str(d / "k.md")], capture_output=True, text=True)
        k = json.loads((d / "k.json").read_text(encoding="utf-8")) if (d / "k.json").is_file() else None
        return r.returncode, k, (r.stderr.strip().splitlines() or [""])[-1][:160]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--autor", required=True, type=Path)
    ap.add_argument("--libro", required=True, type=Path)
    ap.add_argument("--delta", default="3")
    ap.add_argument("--procesos", type=int, default=4)
    a = ap.parse_args()
    contr = a.autor / "scripts" / "contraste_f1.py"
    caja = a.autor / "resultados" / "caja_no_nula.json"
    base = list(csv.DictReader((a.autor / "datos" / "cifras_fuente.csv").open(encoding="utf-8"), delimiter=";"))
    campos = list(base[0].keys())
    verif = json.loads((a.autor / "resultados" / "verificacion_cifras.json").read_text(encoding="utf-8"))
    for r in verif["cifras"]:
        r["estado"] = "OK"
    verif["resumen"]["fallos"] = 0
    verif_txt = json.dumps(verif, ensure_ascii=False)
    cod0, k0, _ = ejecutar(contr, base, campos, verif_txt, a.libro, caja)
    assert cod0 == 0 and k0 is not None, "el control sin mutar no pasa"
    delta = Fraction(a.delta)
    objetivos = [r["id"] for r in base if r["tipo"] == "tabla" and r["edicion"] == "vigente"]

    def caso(rid):
        filas = [dict(r) for r in base]
        hit = [r for r in filas if r["id"] == rid][0]
        hit["valor_publicado"] = str(float(Fraction(hit["valor_publicado"]) + delta))
        cod, k, err = ejecutar(contr, filas, campos, verif_txt, a.libro, caja)
        if k is None:
            return rid, "aborta", err, []
        fall = [c for c in k["comprobaciones"] if not c["ok"]]
        fuente = sorted({c["nombre"].split(" dentro")[0].replace("residuo ", "") for c in fall if c["clase"] == "fuente"})
        libro = [c["nombre"] for c in fall if c["clase"] == "libro"]
        cambian = sorted(t for t in k0["tablas"] if k["tablas"].get(t) != k0["tablas"][t])
        if k.get("referencia_especificacion") != k0.get("referencia_especificacion"):
            cambian.append("referencia_especificacion")
        if fuente:
            return rid, "identidad de fuente", ", ".join(fuente) + (f" (+{len(libro)} del libro)" if libro else ""), cambian
        if libro:
            return rid, "solo libro", f"{len(libro)} comprobaciones del libro; p. ej. {libro[0][:60]}", cambian
        if fall:
            return rid, "solo algebraica", fall[0]["nombre"][:80], cambian
        if cambian:
            return rid, "SIN DETECTAR", "", cambian
        return rid, "no usada", "", cambian

    with ThreadPoolExecutor(max_workers=a.procesos) as ex:
        res = list(ex.map(caso, objetivos))
    meta = {r["id"]: r for r in base}
    clases = {}
    for rid, clase, det, cambian in res:
        clases.setdefault(clase, []).append((rid, det, cambian))
    print(f"Filas de tabla de la edición vigente mutadas (+{a.delta}): {len(objetivos)}")
    for c in ("identidad de fuente", "solo libro", "solo algebraica", "aborta", "SIN DETECTAR", "no usada"):
        print(f"  {c}: {len(clases.get(c, []))}")
    usadas = len(objetivos) - len(clases.get("no usada", []))
    print(f"  usadas (alguna salida cambia o alguna comprobación falla): {usadas}; el autor declara {k0['resumen']['entradas_usadas']}")
    for c in ("SIN DETECTAR", "solo libro", "solo algebraica", "aborta"):
        print(f"\n== {c} ==")
        for rid, det, cambian in clases.get(c, []):
            m = meta[rid]
            print(f"{rid} · {m['doc']} p.{m['pagina']} «{m['literal']}» · {det} · tablas que cambian: {', '.join(cambian)[:230]}")
    print("\n== identidad de fuente (resumen por entrada) ==")
    for rid, det, cambian in clases.get("identidad de fuente", []):
        print(f"{rid} · {det}")


if __name__ == "__main__":
    main()
