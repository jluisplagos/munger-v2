"""Contraejemplos y controles del revisor para la revisión n.º 4 (frente E, F1 de Elis). No modifica nada del autor.

Ejecuta verificar_cifras.py y contraste_f1.py del commit congelado del autor sobre copias mutadas de su CSV. Cada caso usa
su propia carpeta temporal (así un contraste que se niega a calcular no deja leer la salida de un caso anterior).

  A. Unidad: filas reales que no son importes en millones de euros y cuyo rótulo no está en la lista del verificador.
  B. Perímetro: filas reales de otro perímetro en una página consolidada, sin rótulo de segmento ni de país.
  C. Concepto de la línea en entradas sin segunda línea de comprobación (verificador regenerado y contraste).
  D. Límite de la diferencia fijada R13 de 2025, con la verificación falsa ligada al CSV mutado (corrige H3a–H3c y H4 de
     prueba_mutantes_3b.py de la revisión n.º 3, que sobre este commit leían la salida de un caso anterior).
  E. Matriz por segmentos con una celda vacía, con identificadores de la lista cerrada de modos.

Uso: python3 -I contraejemplos_4.py --raiz <ruta>/munger_v2_r1 --autor <carpeta frente_E_F1_elis del autor> --libro <xlsx>
"""
import argparse
import csv
import hashlib
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
    fuentes, caja = a.autor / "datos" / "fuentes.json", a.autor / "resultados" / "caja_no_nula.json"
    base = list(csv.DictReader((a.autor / "datos" / "cifras_fuente.csv").open(encoding="utf-8"), delimiter=";"))
    campos = list(base[0].keys())
    v0 = json.loads((a.autor / "resultados" / "verificacion_cifras.json").read_text(encoding="utf-8"))
    k0 = json.loads((a.autor / "resultados" / "contraste_f1.json").read_text(encoding="utf-8"))

    def escribir(d, filas):
        with (d / "c.csv").open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=campos, delimiter=";")
            w.writeheader()
            w.writerows(filas)

    def verificar(filas):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            escribir(d, filas)
            r = subprocess.run([sys.executable, "-I", str(verif), "--raiz", str(a.raiz), "--datos", str(d / "c.csv"), "--fuentes",
                                str(fuentes), "--salida", str(d / "v.json")], capture_output=True, text=True)
            return r.returncode, json.loads((d / "v.json").read_text(encoding="utf-8"))

    def contrastar(filas, v):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            escribir(d, filas)
            (d / "v.json").write_text(json.dumps(v, ensure_ascii=False), encoding="utf-8")
            r = subprocess.run([sys.executable, "-I", str(contr), "--cifras", str(d / "c.csv"), "--verificacion", str(d / "v.json"),
                                "--libro", str(a.libro), "--caja-no-nula", str(caja), "--salida", str(d / "k.json"), "--informe",
                                str(d / "k.md")], capture_output=True, text=True)
            k = json.loads((d / "k.json").read_text(encoding="utf-8")) if (d / "k.json").is_file() else None
            return r.returncode, k, (r.stderr.strip().splitlines() or [""])[-1][:160]

    def verificacion_falsa(filas):
        """Declara OK todas las filas y corresponde al CSV dado (huella, literal y valor): salta la primera línea."""
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            escribir(d, filas)
            h = hashlib.sha256((d / "c.csv").read_bytes()).hexdigest()
        v = json.loads(json.dumps(v0))
        v["huellas"]["datos"] = h
        por_id = {r["id"]: r for r in filas}
        for r in v["cifras"]:
            r["estado"] = "OK"
            r["literal"], r["valor_publicado"] = por_id[r["id"]]["literal"], por_id[r["id"]]["valor_publicado"]
        v["resumen"]["fallos"] = 0
        return v

    def nueva(rid, **c):
        fila = {k: "" for k in campos}
        fila.update(id=rid, tipo="tabla", doc="URD2025", anio="2025", ocurrencia="0", perimetro=GRUPO, edicion="vigente", unidad="mm EUR",
                    control_anio="dos_columnas", concepto="contraejemplo del revisor", pos="-2")
        fila.update(c)
        return fila

    def mut(cambios):
        filas = [dict(r) for r in base]
        for i, c in cambios.items():
            hit = [r for r in filas if r["id"] == i]
            assert len(hit) == 1, i
            hit[0].update(c)
        return filas

    def fila_sola(nombre, fila):
        _, v = verificar([fila])
        x = [c for c in v["cifras"] if c["id"] == fila["id"]][0]
        dims = {k: d["estado"] for k, d in x["dimensiones"].items()}
        print(f"   {nombre}\n      → {x['estado']} · {dims}")
        for k in ("ejercicio", "unidad", "perimetro"):
            print(f"        {k}: {x['dimensiones'][k].get('detalle', '')[:120]}")

    print("A. Unidad: líneas reales de la tabla del beneficio por acción (URD 2025 p.395), bajo «(In millions of euros)»")
    fila_sola("A1 «Effect of conversion of convertible bonds 23,355,764» (acciones) declarado en millones de euros",
              nueva("CE4_ACC_CONVERSION", pagina="395", etiqueta="re:^\\s*Effect of conversion of convertible bonds\\s{2,}", literal="23,355,764",
                    valor_publicado="23355764"))
    fila_sola("A2 «Effect of contingently issuable shares 1,767,869» (acciones) declarado en millones de euros",
              nueva("CE4_ACC_CONTINGENTES", pagina="395", etiqueta="re:^\\s*Effect of contingently issuable shares\\s{2,}", literal="1,767,869",
                    valor_publicado="1767869"))
    fila_sola("A3 control: «Weighted average number of shares 233,954,020» (U1 de la adenda)",
              nueva("CE4_ACC_MEDIA", pagina="395", etiqueta="re:^\\s*Weighted average number of shares\\s{2,}", literal="233,954,020",
                    valor_publicado="233954020"))

    print("\nB. Perímetro: nota de pensiones «Information by region» (URD 2025 p.356)")
    fila_sola("B1 obligaciones de los planes de FRANCIA, 45,2 («TOTAL VALUE OF DEFINED BENEFIT PLAN OBLIGATIONS (1)» del bloque de Francia), declaradas del grupo (el grupo son 414,4, p.355)",
              nueva("CE4_PENSIONES_FR", pagina="356", etiqueta="TOTAL VALUE OF DEFINED BENEFIT PLAN OBLIGATIONS (1)", ocurrencia="1", literal="45.2",
                    valor_publicado="45.2"))
    fila_sola("B2 control: fila «United Kingdom (9.2)» de la tabla por países de esa página, declarada del grupo",
              nueva("CE4_PENSIONES_UK", pagina="356", etiqueta="re:^\\s*United Kingdom\\s{2,}", ocurrencia="1", literal="(9.2)", valor_publicado="-9.2"))
    fila_sola("B3 control: ventas de Alemania (P1 de la adenda)",
              nueva("CE4_ALEMANIA", pagina="346", etiqueta="re:^\\s*Germany\\s{2,}", ocurrencia="1", literal="621.2", valor_publicado="621.2"))

    print("\nC. Otra línea de la misma tabla en entradas SIN segunda línea (verificador regenerado y contraste)")
    for nombre, rid, cambios, tabla in [
        ("C1 TAXDIF_INT_2025 toma «(17.5)» de la línea «Right-of-use assets» (misma columna de resultado)", "TAXDIF_INT_2025",
         {"etiqueta": "re:^\\s*Right-of-use assets\\s{2,}\\(", "literal": "(17.5)", "valor_publicado": "-17.5"}, "impuestos"),
        ("C2 OOIE_PLUSV_2025 toma «(0.4)» de la línea «Expenses relating to site disposal» (misma tabla, p.350)", "OOIE_PLUSV_2025",
         {"etiqueta": "Expenses relating to site disposal", "literal": "(0.4)", "valor_publicado": "-0.4"}, "partidas_puntuales_en_flujo_sin_crecimiento"),
    ]:
        filas = mut({rid: cambios})
        cod_v, v = verificar(filas)
        x = [c for c in v["cifras"] if c["id"] == rid][0]
        print(f"   {nombre}\n      verificador: código {cod_v} · {x['estado']} · { {k: d['estado'] for k, d in x['dimensiones'].items()} }")
        cod_k, k, err = contrastar(filas, v)
        if k is None:
            print(f"      contraste: código {cod_k}, sin informe ({err})")
            continue
        malas = [c["nombre"] for c in k["comprobaciones"] if not c["ok"]]
        print(f"      contraste: código {cod_k} · fallidas: {len(malas)} {malas[:2]}")
        if tabla == "impuestos":
            for y in ("2025",):
                a_, b_ = k0["tablas"]["impuestos"][y], k["tablas"]["impuestos"][y]
                for kk in a_:
                    if a_[kk] != b_[kk]:
                        print(f"        impuestos {y} · {kk[:60]}: {a_[kk]} → {b_[kk]}")
        else:
            print(f"        {tabla}: {list(k0['tablas'][tabla].values())} → {list(k['tablas'][tabla].values())}")
        print(f"        ¿cambia referencia_especificacion?: {k['referencia_especificacion'] != k0['referencia_especificacion']}")

    print("\nD. Diferencia fijada R13 de 2025 (+0,4 ± 0,15), verificador saltado con una verificación ligada al CSV mutado")
    for nombre, cambios in [
        ("D1 (H3a) gasto devengado 29,3 en lugar de 29,2", {"FIN_INTLS_2025": {"valor_publicado": "-29.3"}}),
        ("D2 (H3b) gasto devengado 29,1", {"FIN_INTLS_2025": {"valor_publicado": "-29.1"}}),
        ("D3 (H3c) pagos de arrendamientos 178,0 en lugar de 177,9", {"CF_LEASE_2025": {"valor_publicado": "-178.0"}}),
        ("D4 (H4) control: gasto devengado 29,5", {"FIN_INTLS_2025": {"valor_publicado": "-29.5"}}),
    ]:
        filas = mut(cambios)
        cod_k, k, err = contrastar(filas, verificacion_falsa(filas))
        if k is None:
            print(f"   {nombre}: código {cod_k}, sin informe ({err})")
            continue
        fall = [c for c in k["comprobaciones"] if not c["ok"]]
        x = k["tablas"]["residuos_con_cota"]["2025"]["R13"]
        print(f"   {nombre}: código {cod_k} · R13 residuo {x['residuo']} ok={x['ok']} · fallidas: {len(fall)} "
              f"(de fuente: {sum(1 for c in fall if c['clase'] == 'fuente')}, del libro: {sum(1 for c in fall if c['clase'] == 'libro')})")

    print("\nE. Matriz por segmentos con una celda vacía (URD 2025 p.344), identificadores con el modo «titulo» admitido")
    for nombre, rid, etq, pos, lit, per in [
        ("E1 margen de EBITDA de Francia, 41,9 %, declarado «segmento Europa central»", "VENTAS_SEG_CE4_E1", "Adjusted EBITDA margin", "-7", "41.9%", "segmento Europa central"),
        ("E2 el mismo, declarado «segmento Francia» (correcto)", "VENTAS_SEG_CE4_E2", "Adjusted EBITDA margin", "-7", "41.9%", "segmento Francia"),
        ("E3 margen de EBIT de Europa del Sur, 15,6 %, declarado «segmento Otros segmentos» (la columna que le correspondería contando desde la derecha)",
         "VENTAS_SEG_CE4_E3", "Adjusted EBIT margin", "-2", "15.6%", "segmento Otros segmentos"),
        ("E4 el mismo, declarado «segmento Europa del Sur» (correcto)", "VENTAS_SEG_CE4_E4", "Adjusted EBIT margin", "-2", "15.6%", "segmento Europa del Sur"),
    ]:
        fila_sola(nombre, nueva(rid, pagina="344", etiqueta="re:^\\s*" + etq + "\\s{2,}", pos=pos, literal=lit, valor_publicado=lit.rstrip("%"),
                                unidad="%", control_anio="titulo", perimetro=per))


if __name__ == "__main__":
    main()
