#!/usr/bin/env python3
"""Preparación 2 del ensayo 2025 (entrega 4.10.1): reexpresa a 31-dic-2025 los DATOS heredados de la etapa 1 medidos en 2026.

Uso (desde munger_v2_r1/): python3 -I personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_10_1/scripts/reexpresar_base_2025.py

Motivo (configuracion_ensayo_2025.json → datos_heredados_reexpresados_a_2025): siete celdas de datos de Análisis migradas de la etapa 1
(C24, C31, C33, C34, C42, C53, C54) estaban medidas a 30-jun-2026; rellenar_fase1_v63.py no pisa un valor migrado (regla de producción,
que no cambia), así que la reexpresión se hace en la ENTRADA y por la ruta real del pipeline:
  1. archiva en antecedentes/preparacion_1_datos_de_2026/ los productos de la primera preparación (libros, volcados, estado del
     pipeline, prompts y la fase A escrita sobre ese libro), con inventario y huellas;
  2. conserva el original de etapa1/Vidrala_evaluada.xlsx en antecedentes/etapa1_original/ y deja en etapa1/ una COPIA DE ENSAYO en la
     que solo se vacían, a nivel XML, esas siete celdas de dato y las filas de evidencia (Control maestro E:N) que la configuración
     lista; el resto de miembros del ZIP y de celdas queda byte a byte igual (se comprueba), y los juicios de la etapa 1 no se tocan;
  3. añade a fase1_v63.json → analisis los valores de 31-dic-2025 de la configuración (C33 lo deriva rellenar_fase1_v63.py de la
     Historia porque queda vacía);
  4. escribe resultados/reexpresion_2025.json y .md.
No ejecuta el pipeline ni LibreOffice. Se niega a repetirse si antecedentes/etapa1_original/ ya existe."""
import copy
import hashlib
import json
import os
import re
import shutil
import sys
import zipfile

import openpyxl

AQUI = os.path.dirname(os.path.abspath(__file__))
ENS = os.path.dirname(AQUI)
ACT = os.path.join(ENS, "Vidrala")
ANT1 = os.path.join(ENS, "antecedentes", "preparacion_1_datos_de_2026")
ORIG = os.path.join(ENS, "antecedentes", "etapa1_original")
CONF = json.load(open(os.path.join(ENS, "configuracion", "configuracion_ensayo_2025.json"), encoding="utf-8"))
RX = CONF["datos_heredados_reexpresados_a_2025"]
LIBRO_E1 = os.path.join(ACT, "etapa1", "Vidrala_evaluada.xlsx")
# productos de la primera preparación (pasos 0–5 del pipeline y fase A): se archivan; el extracto se conserva (ver reexpresion_2025.md)
PRODUCTOS = ["estado_pipeline.json", "ESPERANDO.md", "prompts_generados", "Vidrala_v63_base.xlsx", "Vidrala_v63_base.xlsx.conciliacion.json",
             "Vidrala_v63_datos.xlsx", "Vidrala_v63_datos.xlsx.fase1.registro.json", "recalc", "datos_v63.json", "datos_v63.md",
             "datos_ausentes.json", "entrada_v63.json", "entrada_v63.md", "fase_a.json", "fase_a.md"]
COLS_EVID = "EFGHIJKLMN"


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def hoja_xml(z, nombre):
    """Ruta del XML de la hoja `nombre` dentro del xlsx."""
    wb = z.read("xl/workbook.xml").decode("utf-8")
    rels = z.read("xl/_rels/workbook.xml.rels").decode("utf-8")
    m = re.search(r'<sheet\b[^>]*\bname="' + re.escape(nombre) + r'"[^>]*\br:id="([^"]+)"', wb) or \
        re.search(r'<sheet\b[^>]*\br:id="([^"]+)"[^>]*\bname="' + re.escape(nombre) + r'"', wb)
    rid = m.group(1)
    t = re.search(r'<Relationship\b[^>]*\bId="' + re.escape(rid) + r'"[^>]*\bTarget="([^"]+)"', rels) or \
        re.search(r'<Relationship\b[^>]*\bTarget="([^"]+)"[^>]*\bId="' + re.escape(rid) + r'"', rels)
    tgt = t.group(1).lstrip("/")
    return tgt if tgt.startswith("xl/") else "xl/" + tgt


def vaciar(xml, refs):
    """Deja vacías (sin valor, sin tipo, conservando el estilo) las celdas `refs`; devuelve (xml, vaciadas)."""
    hechas = []
    for ref in refs:
        pat = re.compile(r'<c\b(?=[^>]*\br="' + ref + r'")([^>]*?)(?:/>|>(.*?)</c>)', re.S)
        m = pat.search(xml)
        if not m or m.group(2) is None or m.group(2) == "":
            continue
        if "<f" in (m.group(2) or ""):
            raise SystemExit(f"{ref} es una fórmula en la etapa 1: no se vacía (revisar la configuración)")
        s = re.search(r'\bs="([^"]+)"', m.group(1))
        nuevo = f'<c r="{ref}"' + (f' s="{s.group(1)}"' if s else "") + "/>"
        xml = xml[:m.start()] + nuevo + xml[m.end():]
        hechas.append(ref)
    return xml, hechas


def main():
    if os.path.exists(ORIG) or os.path.exists(ANT1):
        print("la preparación 2 ya se hizo (existe antecedentes/etapa1_original/ o preparacion_1_datos_de_2026/): no se repite")
        return 2
    # 0. lo que había en la copia de la etapa 1 (para el informe)
    wb_d = openpyxl.load_workbook(LIBRO_E1, data_only=True)
    celdas_an = RX["vaciar_en_la_copia_de_etapa1"]["Análisis"]
    filas_cm = RX["vaciar_en_la_copia_de_etapa1"]["Control maestro (filas de evidencia, columnas E:N)"]
    antes = {"Análisis": {c: wb_d["Análisis"][c].value for c in celdas_an},
             "Control maestro": {r: {c: wb_d["Control maestro"][f"{c}{r}"].value for c in COLS_EVID if wb_d["Control maestro"][f"{c}{r}"].value not in (None, "")}
                                 for r in filas_cm}}
    etiquetas = {r: wb_d["Control maestro"][f"B{r}"].value for r in filas_cm}
    # 1. archivar la primera preparación
    os.makedirs(ANT1)
    inv = []
    for n in PRODUCTOS:
        p = os.path.join(ACT, n)
        if os.path.exists(p):
            shutil.move(p, os.path.join(ANT1, n))
    for r, ds, fs in os.walk(ANT1):
        for f in fs:
            q = os.path.join(r, f)
            inv.append({"archivo": os.path.relpath(q, ANT1), "sha256": sha(q)})
    json.dump({"nota": "Productos de la primera preparación del ensayo 2025 (pasos 0–5 y fase A), hechos con siete datos de Análisis heredados de la "
               "etapa 1 medidos a 30-jun-2026. Se conservan sin cambios; ninguno está en una ruta activa. La fase A se revisa sobre el libro nuevo.",
               "archivos": inv}, open(os.path.join(ANT1, "INVENTARIO.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    # 2. etapa 1: original a antecedentes; copia de ensayo con los datos vaciados a nivel XML
    os.makedirs(ORIG)
    orig = os.path.join(ORIG, "Vidrala_evaluada.xlsx")
    shutil.copy2(LIBRO_E1, orig)
    zin = zipfile.ZipFile(orig)
    x_an, x_cm = hoja_xml(zin, "Análisis"), hoja_xml(zin, "Control maestro")
    cambios = {}
    datos = {i.filename: zin.read(i.filename) for i in zin.infolist()}
    xml, h1 = vaciar(datos[x_an].decode("utf-8"), celdas_an)
    datos[x_an] = xml.encode("utf-8")
    cambios["Análisis"] = h1
    refs_cm = [f"{c}{r}" for r in filas_cm for c in COLS_EVID]
    xml, h2 = vaciar(datos[x_cm].decode("utf-8"), refs_cm)
    datos[x_cm] = xml.encode("utf-8")
    cambios["Control maestro"] = h2
    tmp = LIBRO_E1 + ".tmp"
    with zipfile.ZipFile(tmp, "w") as zout:
        for i in zin.infolist():
            zout.writestr(copy.copy(i), datos[i.filename], compress_type=i.compress_type)  # copia: writestr modifica el ZipInfo
    os.replace(tmp, LIBRO_E1)
    # comprobación: los demás miembros, iguales byte a byte; las celdas vaciadas, vacías; el resto de valores de las dos hojas, iguales
    zn = zipfile.ZipFile(LIBRO_E1)
    distintos = [i.filename for i in zin.infolist() if zn.read(i.filename) != zin.read(i.filename)]
    assert set(distintos) <= {x_an, x_cm}, distintos
    w_o, w_n = openpyxl.load_workbook(orig, data_only=True), openpyxl.load_workbook(LIBRO_E1, data_only=True)
    vaciadas = {("Análisis", c) for c in h1} | {("Control maestro", c) for c in h2}
    otras_cambiadas = []
    for hoja in w_o.sheetnames:
        for fila in w_o[hoja].iter_rows():
            for c in fila:
                v_n = w_n[hoja][c.coordinate].value
                if (hoja, c.coordinate) in vaciadas:
                    assert v_n in (None, ""), (hoja, c.coordinate, v_n)
                elif v_n != c.value:
                    otras_cambiadas.append(f"{hoja}!{c.coordinate}")
    assert not otras_cambiadas, otras_cambiadas[:10]
    # 3. fase1_v63.json → analisis con los valores de 31-dic-2025 (C33 la deriva rellenar_fase1_v63.py)
    f1p = os.path.join(ACT, "fase1_v63.json")
    f1 = json.load(open(f1p, encoding="utf-8"))
    añadidas = {}
    for celda, d in RX["celdas"].items():
        if d.get("derivada"):
            continue
        f1.setdefault("analisis", {})[celda] = {"valor": d["valor"], "fuente": d["fuente"], "pagina": d.get("pagina"), "periodo": d.get("periodo"),
                                                "unidad": "mm" if celda in ("C53", "C54") else None}
        añadidas[celda] = d["valor"]
    f1.setdefault("_notas", []).append("(4.10.1, preparación 2) Datos de Análisis heredados de la etapa 1 medidos a 30-jun-2026 reexpresados a 31-dic-2025: "
                                       + "; ".join(f"{c} {antes['Análisis'].get(c)!r} → {v!r}" for c, v in añadidas.items())
                                       + f"; C33 {antes['Análisis'].get('C33')!r} → la deriva rellenar_fase1_v63.py de la Historia 2025 "
                                       "(configuracion_ensayo_2025.json → datos_heredados_reexpresados_a_2025; la etapa 1 original está en antecedentes/etapa1_original/).")
    json.dump(f1, open(f1p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    # 4. registro
    out = {"motivo": RX["motivo"], "etapa1_original": {"archivo": os.path.relpath(orig, ENS), "sha256": sha(orig)},
           "etapa1_de_ensayo": {"archivo": os.path.relpath(LIBRO_E1, ENS), "sha256": sha(LIBRO_E1), "miembros_cambiados": sorted(distintos)},
           "vaciadas": cambios, "valores_de_la_etapa1": antes, "etiquetas_de_las_filas": etiquetas,
           "anadidas_a_fase1_v63": añadidas, "derivada_por_rellenar": [c for c, d in RX["celdas"].items() if d.get("derivada")],
           "preparacion_1_archivada": {"carpeta": os.path.relpath(ANT1, ENS), "archivos": len(inv)},
           "se_conserva": {"extracto_v63.md": {"sha256": sha(os.path.join(ACT, "extracto_v63.md")),
                                               "por_que": "el extracto de la primera preparación no cita ninguna de las siete cifras ni datos de 2026 de la etapa 1 (comprobado por búsqueda: 409,6; 0,69; 109,4; 7,68; 30-jun-2026; 1S2026); se basa en los textos, que no cambian"}}}
    json.dump(out, open(os.path.join(ENS, "resultados", "reexpresion_2025.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    md = ["# Preparación 2 del ensayo 2025 · reexpresión de los datos heredados a 31-dic-2025", "", RX["motivo"], "",
          "| Celda | Etapa 1 (30-jun-2026) | Ensayo (31-dic-2025) |", "|---|---|---|"]
    md += [f"| Análisis!{c} | {antes['Análisis'].get(c)!r} | {RX['celdas'][c]['valor']!r}{' (derivada de la Historia)' if RX['celdas'][c].get('derivada') else ''} |" for c in celdas_an]
    md += ["", f"Filas de evidencia vaciadas en la copia de ensayo (Control maestro E:N): {', '.join(f'{r} ({etiquetas[r]})' for r in filas_cm)}.", "",
           f"Etapa 1 original: `{out['etapa1_original']['archivo']}` (SHA-256 `{out['etapa1_original']['sha256']}`). Copia de ensayo: SHA-256 `{out['etapa1_de_ensayo']['sha256']}`;"
           f" solo cambian {', '.join(sorted(distintos))}; ninguna otra celda cambia (comprobado).", "",
           f"Primera preparación archivada en `{out['preparacion_1_archivada']['carpeta']}` ({len(inv)} archivos, con INVENTARIO.json).", "",
           f"Se conserva `extracto_v63.md`: {out['se_conserva']['extracto_v63.md']['por_que']}.", "",
           f"No se reexpresa: {json.dumps(RX['no_se_reexpresa'], ensure_ascii=False)}"]
    open(os.path.join(ENS, "resultados", "reexpresion_2025.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
    print("\n".join(md))
    return 0


if __name__ == "__main__":
    sys.exit(main())
