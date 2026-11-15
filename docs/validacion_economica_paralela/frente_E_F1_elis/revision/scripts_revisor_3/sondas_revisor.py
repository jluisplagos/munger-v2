"""Sondas del revisor sobre la unidad y el perímetro (adenda de la revisión n.º 3). No modifica nada del autor.

Para cada versión del autor que se indique (--version etiqueta=carpeta frente_E_F1_elis de esa versión) ejecuta SU
verificar_cifras.py sobre copias mutadas de SU datos/cifras_fuente.csv:

  1. Las dos sondas externas de un solo campo, con el año correcto:
       CREC_ORG_2025: unidad «%» → «mm EUR»;   IS_VENTAS_2025: perímetro → «segmento Francia».
  2. La extensión a todas las filas de tabla (un campo cada vez) y su equivalencia con una sonda por fila:
       a) todas las filas a la vez;  b) solo una mitad y solo la otra;  c) una muestra de filas, cada una sola en su CSV.
     Si el verificador evalúa cada fila por separado, el estado de cada fila mutada es el mismo en a, b y c.
  3. Contraejemplos de las heurísticas (solo en versiones con las cinco dimensiones): filas nuevas cuya cifra es de otra
     unidad o de otro perímetro, declaradas como millones de euros del grupo o con un segmento equivocado.

  2b. (con --libro) contraste_f1.py ante una sola etiqueta cambiada, con el verificador saltado.

Uso: python3 -I sondas_revisor.py --raiz <ruta>/munger_v2_r1 [--libro <xlsx>] --version eb77dea=<carpeta> --version 1864c4e=<carpeta> ...
"""
import argparse
import csv
import json
import random
import subprocess
import sys
import tempfile
from pathlib import Path

GRUPO = "consolidado IFRS, grupo Elis"
LIBRO = None
OTRA = {"%": "mm EUR", "mm EUR": "%"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raiz", required=True, type=Path)
    ap.add_argument("--version", action="append", required=True, help="etiqueta=carpeta")
    ap.add_argument("--muestra", type=int, default=40)
    ap.add_argument("--libro", type=Path, help="libro de Elis, para probar la barrera de contraste_f1.py")
    a = ap.parse_args()
    global LIBRO
    LIBRO = a.libro
    for v in a.version:
        etiqueta, carpeta = v.split("=", 1)
        probar(etiqueta, Path(carpeta), a.raiz, a.muestra)


def probar(etiqueta, autor, raiz, muestra):
    verif, fuentes = autor / "scripts" / "verificar_cifras.py", autor / "datos" / "fuentes.json"
    base = list(csv.DictReader((autor / "datos" / "cifras_fuente.csv").open(encoding="utf-8"), delimiter=";"))
    campos = list(base[0].keys())
    tablas = [r["id"] for r in base if r["tipo"] == "tabla"]
    print(f"\n================ versión {etiqueta}: {len(base)} filas, {len(tablas)} de tabla ================")

    def correr(filas):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            with (d / "c.csv").open("w", encoding="utf-8", newline="") as f:
                w = csv.DictWriter(f, fieldnames=campos, delimiter=";")
                w.writeheader()
                w.writerows(filas)
            r = subprocess.run([sys.executable, "-I", str(verif), "--raiz", str(raiz), "--datos", str(d / "c.csv"), "--fuentes",
                                str(fuentes), "--salida", str(d / "v.json")], capture_output=True, text=True)
            v = json.loads((d / "v.json").read_text(encoding="utf-8"))
            return r.returncode, v["resumen"], {x["id"]: x for x in v["cifras"]}

    def estado(x, campo):
        dims = x.get("dimensiones")
        return (x["estado"], dims[campo]["estado"] if dims else "(sin dimensiones)")

    def mutar(campo, ids):
        filas = [dict(r) for r in base]
        for r in filas:
            if r["id"] in ids:
                r[campo] = OTRA.get(r["unidad"], "%") if campo == "unidad" else "segmento Francia"
        return filas

    # 1. sondas externas
    print("1. Sondas externas de un solo campo")
    for rid, campo in (("CREC_ORG_2025", "unidad"), ("IS_VENTAS_2025", "perimetro")):
        cod, res, por_id = correr(mutar(campo, {rid}))
        x = por_id[rid]
        det = (x.get("dimensiones") or {}).get(campo, {}).get("detalle", x.get("motivo", ""))
        ok_n = res.get("ok")
        print(f"   {rid}, solo {campo}: código {cod} · {ok_n}/{res['filas']} OK · fila: {estado(x, campo)} · {str(det)[:110]}")

    # 2. extensión a todas las filas y equivalencia con una sonda por fila
    print("2. Un campo cambiado en cada fila de tabla")
    rnd = random.Random(20261115)
    for campo in ("unidad", "perimetro"):
        _, _, todas = correr(mutar(campo, set(tablas)))
        e_todas = {i: estado(todas[i], campo) for i in tablas}
        det = sum(1 for i in tablas if e_todas[i][0] == "FALLO")
        en_dim = sum(1 for i in tablas if e_todas[i][1] == "FALLO")
        no_det = [i for i in tablas if e_todas[i][0] != "FALLO"]
        print(f"   {campo}: detectadas {det}/{len(tablas)} (en la dimensión del campo: {en_dim}) · sin detectar: "
              f"{[(i, e_todas[i]) for i in no_det[:6]]}{' …' if len(no_det) > 6 else ''}")
        orden = list(tablas)
        rnd.shuffle(orden)
        mitades = (set(orden[: len(orden) // 2]), set(orden[len(orden) // 2:]))
        distintas = 0
        for m in mitades:
            _, _, parte = correr(mutar(campo, m))
            distintas += sum(1 for i in m if estado(parte[i], campo) != e_todas[i])
        sola = 0
        ids = orden[:muestra]
        for i in ids:
            _, _, una = correr([r for r in mutar(campo, {i}) if r["id"] == i])
            sola += estado(una[i], campo) != e_todas[i]
        print(f"      equivalencia: filas con estado distinto al mutar solo media tabla: {distintas} de {len(tablas)}; "
              f"filas con estado distinto al evaluarlas solas en su CSV: {sola} de {len(ids)}")

    # 2b. barrera de contraste_f1.py ante una etiqueta declarada que no es la que pide el cálculo (verificador saltado)
    contr, libro = autor / "scripts" / "contraste_f1.py", LIBRO
    if libro is not None and (autor / "resultados" / "caja_no_nula.json").is_file():
        print("2b. contraste_f1.py con una sola etiqueta cambiada y una verificación que declara OK todas las filas")
        ver = json.loads((autor / "resultados" / "verificacion_cifras.json").read_text(encoding="utf-8"))
        for x in ver["cifras"]:
            x["estado"] = "OK"
        ver["resumen"]["fallos"] = 0
        for rid, campo in (("CREC_ORG_2025", "unidad"), ("IS_VENTAS_2025", "perimetro")):
            with tempfile.TemporaryDirectory() as d:
                d = Path(d)
                with (d / "c.csv").open("w", encoding="utf-8", newline="") as f:
                    w = csv.DictWriter(f, fieldnames=campos, delimiter=";")
                    w.writeheader()
                    w.writerows(mutar(campo, {rid}))
                (d / "v.json").write_text(json.dumps(ver, ensure_ascii=False), encoding="utf-8")
                r = subprocess.run([sys.executable, "-I", str(contr), "--cifras", str(d / "c.csv"), "--verificacion", str(d / "v.json"), "--libro",
                                    str(libro), "--caja-no-nula", str(autor / "resultados" / "caja_no_nula.json"), "--salida", str(d / "k.json"),
                                    "--informe", str(d / "k.md")], capture_output=True, text=True)
                print(f"   {rid}, solo {campo}: código {r.returncode} · informe escrito: {(d / 'k.json').is_file()} · "
                      f"{(r.stderr.strip().splitlines() or [''])[-1][:150]}")

    # 3. contraejemplos de las heurísticas
    if "edicion" not in campos:
        print("3. Contraejemplos: no aplican (esta versión no comprueba la unidad ni el perímetro)")
        return

    def nueva(rid, **c):
        fila = {k: "" for k in campos}
        fila.update(id=rid, tipo="tabla", doc="URD2025", anio="2025", ocurrencia="0", perimetro=GRUPO, edicion="vigente", unidad="mm EUR",
                    control_anio="dos_columnas", concepto="contraejemplo del revisor")
        fila.update(c)
        return fila

    casos = [
        ("P1 ventas de Alemania («Germany 621.2», tabla por países, URD 2025 p.346) declaradas del grupo",
         nueva("CE_ALEMANIA", pagina="346", etiqueta="re:^\\s*Germany\\s{2,}", ocurrencia="1", pos="-2", literal="621.2", valor_publicado="621.2")),
        ("P2a ventas del segmento «Other» (URD 2025 p.307, «Other 35.6 30.7 …») declaradas del grupo",
         nueva("CE_OTROS_GRUPO", pagina="307", etiqueta="re:^\\s*Other\\s{2,}", pos="-6", literal="35.6", valor_publicado="35.6",
               control_anio="crecimiento")),
        ("P2b la misma cifra con su perímetro CORRECTO, «segmento Otros segmentos»",
         nueva("CE_OTROS_SEGMENTO", pagina="307", etiqueta="re:^\\s*Other\\s{2,}", pos="-6", literal="35.6", valor_publicado="35.6",
               control_anio="crecimiento", perimetro="segmento Otros segmentos")),
        ("U1 número medio de acciones («233,954,020», URD 2025 p.395) declarado en millones de euros",
         nueva("CE_ACCIONES_MEDIA", pagina="395", etiqueta="re:^\\s*Weighted average number of shares\\s{2,}", pos="-2", literal="233,954,020",
               valor_publicado="233954020")),
        ("U2 número de acciones suscritas («889,250», URD 2025 p.362; la línea anterior dice «(in millions of euros)») declarado en millones de euros",
         nueva("CE_ACCIONES_SUSCRITAS", pagina="362", etiqueta="re:^\\s*Number of shares subscribed\\s{2,}", pos="-2", literal="889,250",
               valor_publicado="889250")),
        ("X1 matriz por segmentos con una celda vacía (URD 2025 p.344, «Adjusted EBITDA margin»): el margen de FRANCIA, 41,9 %, declarado «segmento Europa central»",
         nueva("CE_MARGEN_FR_COMO_EC", pagina="344", etiqueta="re:^\\s*Adjusted EBITDA margin\\s{2,}", pos="-7", literal="41.9%", valor_publicado="41.9",
               unidad="%", control_anio="titulo", perimetro="segmento Europa central")),
        ("X2 la misma cifra con su perímetro CORRECTO, «segmento Francia»",
         nueva("CE_MARGEN_FR_COMO_FR", pagina="344", etiqueta="re:^\\s*Adjusted EBITDA margin\\s{2,}", pos="-7", literal="41.9%", valor_publicado="41.9",
               unidad="%", control_anio="titulo", perimetro="segmento Francia")),
        ("X3 matriz con orden de cabeceras NO canónico (URD 2021 p.247: France, UK & Ireland, Central Europe…): las ventas de Reino Unido e Irlanda, 364,2, declaradas «segmento Europa central»",
         nueva("CE_ORDEN_UK_COMO_EC", doc="URD2021", anio="2021", edicion="anterior", pagina="247", etiqueta="re:^\\s*External customers\\s{2,}", ocurrencia="1",
               pos="-7", literal="364.2", valor_publicado="364.2", control_anio="titulo", perimetro="segmento Europa central")),
        ("X4 la misma cifra con su perímetro CORRECTO, «segmento Reino Unido e Irlanda»",
         nueva("CE_ORDEN_UK_COMO_UK", doc="URD2021", anio="2021", edicion="anterior", pagina="247", etiqueta="re:^\\s*External customers\\s{2,}", ocurrencia="1",
               pos="-7", literal="364.2", valor_publicado="364.2", control_anio="titulo", perimetro="segmento Reino Unido e Irlanda")),
        ("X5 el total del grupo de esa matriz, 3.048,3, declarado del grupo",
         nueva("CE_ORDEN_TOTAL", doc="URD2021", anio="2021", edicion="anterior", pagina="247", etiqueta="re:^\\s*External customers\\s{2,}", ocurrencia="1",
               pos="-1", literal="3,048.3", valor_publicado="3048.3", control_anio="titulo")),
    ]
    print("3. Contraejemplos de las heurísticas (filas nuevas)")
    for nombre, fila in casos:
        _, _, por_id = correr([fila])
        x = por_id[fila["id"]]
        dims = {k: v["estado"] for k, v in x["dimensiones"].items()}
        print(f"   {nombre}\n      → {x['estado']} · {dims}")
        for k, v in x["dimensiones"].items():
            if v["estado"] not in ("OK", "NO_APLICA") or k == "perimetro":
                print(f"        {k}: {v.get('detalle', '')[:140]}")


if __name__ == "__main__":
    main()
