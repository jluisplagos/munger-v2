"""Segundo lote de mutantes del revisor (revisión n.º 3): entradas sin identidad, verificación caducada y límite de la
excepción fijada R13. No modifica nada del autor: trabaja con copias en una carpeta temporal.

  H1  Truco del modo sobre una entrada que no cubre ninguna identidad: OOIE_PLUSV_2025 toma «(1.5)» de la columna de 2024
      y declara el modo «crecimiento». Pasa por el verificador regenerado y por el contraste.
  H2  Verificación caducada: se cambia el CSV DESPUÉS de verificar (DA_ROU_U23_2022: −103,7 → −93,7) y se entrega a
      contraste_f1.py la verificación original del autor, sin regenerar.
  H5  Fila equivocada (concepto) en una entrada que ninguna identidad cubre: DA_ROU_U23_2022 toma la cifra de la línea
      «Other leased items» de la misma tabla (URD 2023 p.301). Verificador regenerado y contraste.
  H3  Límite de la excepción fijada R13 de 2025 (+0,4 ± 0,15): errores nuevos de 0,1 en el gasto devengado o en los pagos.
      Como en test_contraste_residuos.py del autor, con el verificador saltado.
  H4  Control: error nuevo de 0,3 en el gasto devengado (debe fallar R13).

Uso: python3 -I prueba_mutantes_3b.py --raiz <ruta>/munger_v2_r1 --autor <carpeta frente_E_F1_elis del autor> --libro <xlsx>
"""
import argparse
import csv
import json
import subprocess
import sys
import tempfile
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raiz", required=True, type=Path)
    ap.add_argument("--autor", required=True, type=Path)
    ap.add_argument("--libro", required=True, type=Path)
    a = ap.parse_args()
    verif, contr = a.autor / "scripts" / "verificar_cifras.py", a.autor / "scripts" / "contraste_f1.py"
    base = list(csv.DictReader((a.autor / "datos" / "cifras_fuente.csv").open(encoding="utf-8"), delimiter=";"))
    campos = list(base[0].keys())
    v_autor = json.loads((a.autor / "resultados" / "verificacion_cifras.json").read_text(encoding="utf-8"))
    k0 = json.loads((a.autor / "resultados" / "contraste_f1.json").read_text(encoding="utf-8"))
    v_ok = json.loads(json.dumps(v_autor))
    for r in v_ok["cifras"]:
        r["estado"] = "OK"
    v_ok["resumen"]["fallos"] = 0

    def mut(cambios):
        filas = [dict(r) for r in base]
        for i, c in cambios.items():
            hit = [r for r in filas if r["id"] == i]
            assert len(hit) == 1, i
            hit[0].update(c)
        return filas

    def corre(d, filas, verificacion=None):
        """verificacion None → se regenera con verificar_cifras.py del autor; si no, se entrega la indicada."""
        with (d / "c.csv").open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=campos, delimiter=";")
            w.writeheader()
            w.writerows(filas)
        cod_v = None
        if verificacion is None:
            r1 = subprocess.run([sys.executable, "-I", str(verif), "--raiz", str(a.raiz), "--datos", str(d / "c.csv"), "--fuentes",
                                 str(a.autor / "datos" / "fuentes.json"), "--salida", str(d / "v.json")], capture_output=True, text=True)
            cod_v = r1.returncode
        else:
            (d / "v.json").write_text(json.dumps(verificacion, ensure_ascii=False), encoding="utf-8")
        r2 = subprocess.run([sys.executable, "-I", str(contr), "--cifras", str(d / "c.csv"), "--verificacion", str(d / "v.json"),
                             "--libro", str(a.libro), "--caja-no-nula", str(a.autor / "resultados" / "caja_no_nula.json"),
                             "--salida", str(d / "k.json"), "--informe", str(d / "k.md")], capture_output=True, text=True)
        k = json.loads((d / "k.json").read_text(encoding="utf-8")) if (d / "k.json").is_file() else None
        v = json.loads((d / "v.json").read_text(encoding="utf-8"))
        return cod_v, v, r2.returncode, k, (r2.stderr.strip().splitlines() or [""])[-1][:200]

    def informe(nombre, rid, cod_v, v, cod_k, k, err):
        print(f"\n{nombre}")
        if cod_v is not None:
            e = [c for c in v["cifras"] if c["id"] == rid][0]
            print(f"  verificar_cifras.py (regenerado): código {cod_v} · fila {rid}: {e['estado']} · "
                  f"{ {x: y['estado'] for x, y in e['dimensiones'].items()} }")
        if k is None:
            print(f"  contraste_f1.py: código {cod_k}, sin informe ({err})")
            return None
        malas = [c["nombre"] for c in k["comprobaciones"] if not c["ok"]]
        print(f"  contraste_f1.py: código {cod_k} · comprobaciones fallidas: {len(malas)} {malas[:3]}")
        cambian = sorted(t for t in k0["tablas"] if k["tablas"].get(t) != k0["tablas"][t])
        if k.get("referencia_especificacion") != k0.get("referencia_especificacion"):
            cambian.append("referencia_especificacion")
        print(f"  tablas que cambian respecto al resultado del autor: {cambian}")
        return k

    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        k = informe("H1 truco del modo en una entrada sin identidad (OOIE_PLUSV_2025 ← «(1.5)» de 2024, modo «crecimiento»)", "OOIE_PLUSV_2025",
                    *corre(d, mut({"OOIE_PLUSV_2025": {"pos": "-1", "literal": "(1.5)", "valor_publicado": "-1.5", "control_anio": "crecimiento"}})))
        if k:
            print("  partidas puntuales (O9):", k["tablas"]["partidas_puntuales_en_flujo_sin_crecimiento"])
            print("  original del autor:    ", k0["tablas"]["partidas_puntuales_en_flujo_sin_crecimiento"])
        k = informe("H2 verificación caducada (CSV cambiado después de verificar: DA_ROU_U23_2022 −103,7 → −93,7; se entrega la verificación original)",
                    "DA_ROU_U23_2022", *corre(d, mut({"DA_ROU_U23_2022": {"valor_publicado": "-93.7"}}), verificacion=v_autor))
        if k:
            for p in ("A1", "A2"):
                print(f"  referencia de la especificación, C53 de {p}: {k0['referencia_especificacion']['perimetros'][p]['S2C_C53']} → "
                      f"{k['referencia_especificacion']['perimetros'][p]['S2C_C53']}")
        k = informe("H5 fila equivocada en una entrada sin identidad (DA_ROU_U23_2022 toma «(30.3)» de la línea «Other leased items» de la misma tabla)",
                    "DA_ROU_U23_2022", *corre(d, mut({"DA_ROU_U23_2022": {"etiqueta": "Other leased items", "literal": "(30.3)", "valor_publicado": "-30.3"}})))
        if k:
            for p in ("A1", "A2"):
                print(f"  referencia de la especificación, C53 de {p}: {k0['referencia_especificacion']['perimetros'][p]['S2C_C53']} → "
                      f"{k['referencia_especificacion']['perimetros'][p]['S2C_C53']}")
        for nombre, cambios in [
            ("H3a gasto devengado de arrendamientos 2025: 29,3 en lugar de 29,2 (verificador saltado)", {"FIN_INTLS_2025": {"valor_publicado": "-29.3"}}),
            ("H3b gasto devengado de arrendamientos 2025: 29,1 en lugar de 29,2 (verificador saltado)", {"FIN_INTLS_2025": {"valor_publicado": "-29.1"}}),
            ("H3c pagos de arrendamientos 2025: 178,0 en lugar de 177,9 (verificador saltado)", {"CF_LEASE_2025": {"valor_publicado": "-178.0"}}),
            ("H4 control: gasto devengado 2025 29,5 en lugar de 29,2 (verificador saltado)", {"FIN_INTLS_2025": {"valor_publicado": "-29.5"}}),
        ]:
            rid = next(iter(cambios))
            k = informe(nombre, rid, *corre(d, mut(cambios), verificacion=v_ok))
            if k:
                x = k["tablas"]["residuos_con_cota"]["2025"]["R13"]
                print(f"  R13 2025: residuo {x['residuo']}, valor fijado {x['valor_fijado']}, cota {x['cota_de_redondeo']}, ok={x['ok']}")


if __name__ == "__main__":
    main()
