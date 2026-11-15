"""Cobertura por mutación de las entradas de contraste_f1.py (frente E · F1 · Elis).

Adaptación del autor de revision/scripts_revisor_3/cobertura_por_mutacion.py (revisión n.º 3, commit 034301c de la rama
del revisor), que se conserva sin cambios. Solo cambia una cosa: desde C7, contraste_f1.py no calcula con una
verificación de otro CSV (N3). El script del revisor entregaba a cada CSV mutado la verificación del CSV original, así que
sobre C7 todas sus mutaciones terminarían en «aborta». Aquí la verificación falsa, que declara OK todas las filas, se hace
corresponder con cada CSV mutado: su huella y el literal y el valor de cada fila. Es lo mismo que hace
test_contraste_residuos.py. Se salta así la primera línea de defensa, el verificador, para medir solo la segunda.

Para cada fila de tabla de la edición vigente de datos/cifras_fuente.csv se suma «delta» a «valor_publicado». Por
defecto, delta = 3,0, más del doble de cualquier cota de redondeo. Cada entrada queda en una de estas clases, las mismas
del revisor:

  no usada             ninguna salida cambia;
  identidad de fuente  falla al menos un residuo afirmado o la doble vía de C52;
  solo libro           no falla ninguna identidad de fuente, pero sí alguna comprobación contra el libro;
  solo algebraica      solo falla una identidad algebraica;
  aborta               contraste_f1.py termina sin informe (se anota el motivo);
  SIN DETECTAR         cambia alguna tabla o valor de referencia y no falla ninguna comprobación.

Al final compara cada clase con la cobertura que declara el propio contraste («cobertura_entradas»). Señala dos casos:
- una entrada declarada «contrastada» que la mutación no detecta en ninguna identidad de fuente;
- una entrada usada que el contraste no declara.
Lista aparte, sin contarlas como incoherencia, las entradas que el contraste lee pero cuya mutación no cambia ninguna
salida, y las no detectadas que cambian la referencia de la especificación. Termina con código 1 si hay incoherencias.

Uso: python3 -I cobertura_por_mutacion.py --libro <xlsx> [--delta 3] [--procesos 4]
"""
import argparse
import csv
import hashlib
import json
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from fractions import Fraction
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ_F = AQUI.parent


def ejecutar(filas, campos, verif, libro, caja):
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        with (d / "c.csv").open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=campos, delimiter=";")
            w.writeheader()
            w.writerows(filas)
        # única diferencia con el script del revisor: la verificación falsa corresponde al CSV mutado
        v = json.loads(json.dumps(verif))
        v["huellas"]["datos"] = hashlib.sha256((d / "c.csv").read_bytes()).hexdigest()
        por_id = {r["id"]: r for r in filas}
        for r in v["cifras"]:
            r["literal"], r["valor_publicado"] = por_id[r["id"]]["literal"], por_id[r["id"]]["valor_publicado"]
        (d / "v.json").write_text(json.dumps(v, ensure_ascii=False), encoding="utf-8")
        r = subprocess.run([sys.executable, "-I", str(AQUI / "contraste_f1.py"), "--cifras", str(d / "c.csv"), "--verificacion",
                            str(d / "v.json"), "--libro", str(libro), "--caja-no-nula", str(caja), "--salida", str(d / "k.json"),
                            "--informe", str(d / "k.md")], capture_output=True, text=True)
        k = json.loads((d / "k.json").read_text(encoding="utf-8")) if (d / "k.json").is_file() else None
        return r.returncode, k, (r.stderr.strip().splitlines() or [""])[-1][:160]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--libro", required=True, type=Path)
    ap.add_argument("--delta", default="3")
    ap.add_argument("--procesos", type=int, default=4)
    a = ap.parse_args()
    caja = RAIZ_F / "resultados" / "caja_no_nula.json"
    base = list(csv.DictReader((RAIZ_F / "datos" / "cifras_fuente.csv").open(encoding="utf-8"), delimiter=";"))
    campos = list(base[0].keys())
    verif = json.loads((RAIZ_F / "resultados" / "verificacion_cifras.json").read_text(encoding="utf-8"))
    for r in verif["cifras"]:
        r["estado"] = "OK"
    verif["resumen"]["fallos"] = 0
    cod0, k0, err0 = ejecutar(base, campos, verif, a.libro, caja)
    assert cod0 == 0 and k0 is not None, f"el control sin mutar no pasa: {cod0} {err0}"
    delta = Fraction(a.delta)
    objetivos = [r["id"] for r in base if r["tipo"] == "tabla" and r["edicion"] == "vigente"]

    def caso(rid):
        filas = [dict(r) for r in base]
        hit = [r for r in filas if r["id"] == rid][0]
        hit["valor_publicado"] = str(float(Fraction(hit["valor_publicado"]) + delta))
        cod, k, err = ejecutar(filas, campos, verif, a.libro, caja)
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
    print(f"  usadas (alguna salida cambia o alguna comprobación falla): {usadas}; el contraste declara {k0['resumen']['entradas_usadas']} "
          f"en todas las ediciones")

    # comparación con la cobertura que declara el contraste (cobertura_entradas)
    estado_decl = {i: e["estado"] for i, e in k0["tablas"]["cobertura_entradas"]["entradas"].items()}
    por_clase = {rid: clase for rid, clase, _, _ in res}
    print("\n== comparación con cobertura_entradas del contraste (solo filas de la edición vigente, las mutadas) ==")
    esperado = {"contrastada entre páginas": {"identidad de fuente"}, "solo identidad de la misma página": {"identidad de fuente"},
                "contrastada con la Historia del libro": {"identidad de fuente", "solo libro"},
                "sin comprobación de segunda línea": {"identidad de fuente", "solo libro", "solo algebraica", "SIN DETECTAR", "no usada"}}
    tabla_cruce = {}
    for rid in objetivos:
        tabla_cruce.setdefault((estado_decl.get(rid, "no declarada"), por_clase[rid]), []).append(rid)
    for (dec, mutc), ids in sorted(tabla_cruce.items()):
        print(f"  declarada «{dec}» · mutación «{mutc}»: {len(ids)}")
    incoherentes = sorted(rid for rid in objetivos if rid in estado_decl and por_clase[rid] not in esperado[estado_decl[rid]])
    print(f"  declaradas con una comprobación que la mutación no hace fallar: {len(incoherentes)} {incoherentes}")
    sin_decl = sorted(rid for rid in objetivos if rid not in estado_decl and por_clase[rid] != "no usada")
    print(f"  usadas según la mutación y no declaradas por el contraste: {len(sin_decl)} {sin_decl}")
    decl_no_usadas = sorted(rid for rid in objetivos if rid in estado_decl and por_clase[rid] == "no usada")
    print(f"  declaradas por el contraste en las que la mutación no cambia nada (se leen sin efecto en ninguna salida): "
          f"{len(decl_no_usadas)} {decl_no_usadas}")
    sin_det_ref = sorted(rid for rid, clase, _, cambian in res if clase == "SIN DETECTAR" and "referencia_especificacion" in cambian)
    print(f"  sin detectar y con efecto en la referencia de la especificación: {len(sin_det_ref)} {sin_det_ref}")
    libro_ref = sorted(rid for rid, clase, _, cambian in res if clase == "solo libro" and "referencia_especificacion" in cambian)
    print(f"  solo contrastadas con el libro y con efecto en la referencia de la especificación: {len(libro_ref)} {libro_ref}")

    for c in ("SIN DETECTAR", "solo libro", "solo algebraica", "aborta"):
        print(f"\n== {c} ==")
        for rid, det, cambian in clases.get(c, []):
            m = meta[rid]
            print(f"{rid} · {m['doc']} p.{m['pagina']} «{m['literal']}» · declarada: {estado_decl.get(rid, 'no declarada')} · {det} · "
                  f"tablas que cambian: {', '.join(cambian)[:200]}")
    print("\n== identidad de fuente (resumen por entrada) ==")
    for rid, det, cambian in clases.get("identidad de fuente", []):
        print(f"{rid} · {det}")
    return 1 if (incoherentes or sin_decl) else 0


if __name__ == "__main__":
    sys.exit(main())
