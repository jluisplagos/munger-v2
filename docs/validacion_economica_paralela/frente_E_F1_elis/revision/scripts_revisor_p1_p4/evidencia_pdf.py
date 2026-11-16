"""Evidencia de los PDF · revisión dirigida a P1–P4 · propuesta de decisiones F1 · Elis.

Script de revisión, de solo lectura. Para cada pasaje en que se apoya la revisión:
  · comprueba la huella del PDF contra `datos/fuentes.json` del autor;
  · extrae esa página con `pdftotext -layout` y exige que estén en ella todos los fragmentos declarados;
  · si `pypdf` está instalado, busca los mismos fragmentos con ese segundo extractor y anota el resultado;
  · guarda las líneas donde aparecen.
Además suma los ingresos anuales publicados de las «otras adquisiciones» (las que no son «importantes») de 2024 y
de 2025, y comprueba los literales de las cifras que `recalculo_independiente.py` usa con el rótulo [LECTURA].

Las páginas son páginas del PDF (1 = la primera del archivo), como en el material del autor.

Uso:
  python3 -I evidencia_pdf.py --base <árbol materializado>/munger_v2_r1 --fuentes <frente>/datos/fuentes.json \
      --salida ../resultados_revisor_p1_p4/evidencia_pdf.json --informe ../resultados_revisor_p1_p4/evidencia_pdf.txt
Termina con 1 si falta un fragmento o una huella no coincide.
"""
import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

# (clave, documento, página PDF, fragmentos que deben estar en la página, para qué se usa)
PASAJES = [
    ("def_organico_2025", "URD2025", 313,
     ["changes in the scope of consolidation of “major acquisitions” and",
      "revenue of more than €5.0 million in France and €3.0 million in"],
     "P2/4b: el crecimiento orgánico publicado solo excluye las adquisiciones «importantes»"),
    ("def_organico_2024", "DEU2024FR", 259,
     ["consolidation des « acquisitions importantes » et des « cessions"],
     "P2/4b: la misma definición en la edición de 2024"),
    ("def_organico_2023", "URD2023", 267,
     ["the impacts of changes in the scope of consolidation of “major"],
     "P2/4b: la misma definición en la edición de 2023"),
    ("def_organico_2022", "URD2022", 249,
     ["the impacts of changes in the scope of consolidation of “major"],
     "P2/4b: la misma definición en la edición de 2022"),
    ("def_organico_2021", "URD2021", 217,
     ["the impacts of changes in the scope of consolidation of “major"],
     "P2/4b: la misma definición en la edición de 2021"),
    ("gastos_de_transaccion_2025_24", "URD2025", 350,
     ["Major acquisition-related transaction expenses", "(2.4)", "(5.2)"],
     "P2: los gastos de transacción de las compras están en otros gastos operativos (EBIT y caja)"),
    ("gastos_de_transaccion_2024_23", "DEU2024FR", 296,
     ["Coûts connexes aux acquisitions importantes", "(5,2)", "(1,5)"],
     "P2: ídem, 2024 y 2023"),
    ("actualizacion_2025", "URD2025", 313,
     ["Accretion expense for the earnout pertaining to the acquisition in Mexico", "0.7", "5.6"],
     "P3: la actualización del earnout de 2025 sí está publicada por separado"),
    ("actualizacion_2023_24", "DEU2024FR", 259,
     ["Charge de désactualisation du complément de prix de l’acquisition réalisée au Mexique", "5,6", "12,4"],
     "P3: actualización del earnout de 2023 y 2024"),
    ("flujos_adquisiciones_2025", "URD2025", 341,
     ["CASH FLOWS FROM ACQUISITIONS", "Earnouts and deferred", "(23.3)", "(19.7)", "(117.6)", "(37.3)"],
     "P3: los earnouts pagados están en la línea de adquisiciones (inversión), fuera del FCF base"),
    ("flujos_adquisiciones_2024", "URD2025", 342,
     ["CASH FLOWS FROM ACQUISITIONS", "Earnouts and deferred consideration", "(93.9)", "(83.2)", "(10.7)", "(183.3)", "(22.0)"],
     "P3: ídem, 2024; Lavartex es la compra de México de 2022"),
    ("flujos_adquisiciones_2023", "DEU2024FR", 288,
     ["FLUX DE TRÉSORERIE LIÉS AUX ACQUISITIONS", "Compléments de prix et paiements différés", "(34,4)", "(31,4)", "(82,1)", "(35,3)"],
     "P3: ídem, 2023"),
    ("liquidacion_earnout_mexico", "URD2025", 352,
     ["settlement of the second installment and the balance of the Mexican earnout in 2024 and"],
     "P3: el earnout de México se liquidó en 2024 y 2025"),
    ("linea_fiscal_2023_24", "DEU2024FR", 337,
     ["Ajustements et désactualisation de compléments de prix non déductibles", "0,8", "(15,8)"],
     "P3: los ajustes y la actualización del earnout no son deducibles"),
    ("linea_fiscal_2024_25", "URD2025", 392,
     ["Adjustments and accretion of non-deductible earnouts", "(0.2)", "0.8"],
     "P3: ídem, 2024 y 2025"),
    ("linea_fiscal_2022", "URD2023", 345,
     ["Adjustments and accretion of non-deductible earnouts", "(15.8)", "0.5"],
     "P3: en 2022 también hubo ajuste de earnout, fuera de la ventana y dentro del τ de 5 años"),
    ("nota46_2023_2022", "URD2023", 302,
     ["Earnout adjustments", "(48.9)", "2.4", "mainly to the revaluation of the earnout pertaining to the"],
     "P3: ajuste de 2022 (+2,4) y motivo del de 2023"),
    ("nota46_2022_2021", "URD2022", 285,
     ["Earnout adjustments", "2.1", "(3.0)"],
     "P3: ajuste de 2021 (−3,0)"),
    ("ooie_2025", "URD2025", 309,
     ["acquisition earnout compared to 2024 (including that in Mexico),", "offset by a high level of insurance benefits in 2025.",
      "structures in particular, in line with the growth in revenue and"],
     "P3 (N2) y P2: indemnizaciones de seguros dentro de otros ingresos operativos; gasto comercial en el resultado"),
    ("plan_climatico_capex", "URD2025", 122,
     ["capex contained despite new workwear contracts and expenditure", "under the Climate plan", "and a volume effect"],
     "P1 y 4b: gasto del plan climático dentro del capex; efecto volumen de 2025"),
    ("plan_climatico_deterioro", "URD2025", 369,
     ["climate plan, with a level of investment greater than"],
     "P1: los planes de deterioro suponen una inversión superior a la amortización histórica"),
    ("deterioro_arrendamientos", "URD2025", 368,
     ["capital expenditure (including lease"],
     "1a: la renovación de arrendamientos dentro de la inversión en las pruebas de deterioro"),
    ("lino_crecimiento", "URD2025", 312,
     ["Growth investments thus make up a"],
     "P2: dotación inicial a clientes nuevos dentro del capex"),
    ("otras_adquisiciones_2025", "URD2025", 339,
     ["Other acquisitions", "These bolt-on acquisitions help to consolidate the Group’s position"],
     "P2/4b: lista de las adquisiciones de 2025 que no son «importantes»"),
    ("otras_adquisiciones_2024", "URD2025", 341,
     ["Other acquisitions", "These bolt-on acquisitions have helped to consolidate the Group’s"],
     "P2/4b: lista de las adquisiciones de 2024 que no son «importantes»"),
]
LISTAS = {"otras_adquisiciones_2025": ("URD2025", 339), "otras_adquisiciones_2024": ("URD2025", 341)}


def pagina_pdftotext(pdf, n):
    return subprocess.run(["pdftotext", "-layout", "-f", str(n), "-l", str(n), str(pdf), "-"], check=True,
                          capture_output=True).stdout.decode("utf-8", errors="replace")


def normal(s):
    return re.sub(r"\s+", " ", s.replace("ﬁ", "fi").replace("ﬂ", "fl").replace("’", "'").replace(" ", " ")).strip()


def ingresos_de_la_lista(texto):
    """Ingresos anuales de las viñetas bajo «Other acquisitions» (columna derecha de la página)."""
    lineas = texto.splitlines()
    ini = next(i for i, l in enumerate(lineas) if "Other acquisitions" in l)
    col = lineas[ini].index("Other acquisitions")
    fin = next((i for i in range(ini, len(lineas)) if "These bolt-on acquisitions" in lineas[i]), len(lineas))
    bloque = normal(" ".join(l[max(0, col - 3):] for l in lineas[ini + 1:fin]))
    vinetas = [v.strip() for v in bloque.split("›") if v.strip()]
    filas = []
    for v in vinetas:
        m = re.search(r"revenue of (?:around )?€([0-9]+\.[0-9]) million", v)
        filas.append({"viñeta": v[:150], "ingresos_anuales": float(m.group(1)) if m else None})
    return filas


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--base", required=True, type=Path, help="raíz munger_v2_r1 del árbol materializado")
    ap.add_argument("--fuentes", required=True, type=Path)
    ap.add_argument("--salida", required=True, type=Path)
    ap.add_argument("--informe", required=True, type=Path)
    a = ap.parse_args()
    fuentes = json.loads(a.fuentes.read_text(encoding="utf-8"))["fuentes"]
    try:
        import pypdf
    except Exception:                                   # noqa: BLE001
        pypdf = None
    res, lineas, fallos, lectores = {"huellas": {}, "pasajes": {}}, [], [], {}
    for doc, f in fuentes.items():
        ruta = a.base / f["archivo"]
        h = hashlib.sha256(ruta.read_bytes()).hexdigest()
        ok = h == f["sha256"]
        res["huellas"][doc] = {"sha256": h, "coincide_con_fuentes_json": ok}
        if not ok:
            fallos.append("huella " + doc)
        lineas.append(f"{doc}: huella {'coincide' if ok else 'DISTINTA'} ({h[:12]}…)")
    textos = {}
    for clave, doc, pag, fragmentos, uso in PASAJES:
        ruta = a.base / fuentes[doc]["archivo"]
        t = textos.setdefault((doc, pag), pagina_pdftotext(ruta, pag))
        tn = normal(t)
        halladas, faltan = [], []
        for fr in fragmentos:
            if normal(fr) in tn:
                halladas += [normal(l)[:230] for l in t.splitlines() if normal(fr) in normal(l)][:2]
            else:
                faltan.append(fr)
        segundo = None
        if pypdf is not None:
            if doc not in lectores:
                lectores[doc] = pypdf.PdfReader(str(ruta))
            t2 = normal(lectores[doc].pages[pag - 1].extract_text() or "")
            segundo = {fr: (normal(fr) in t2) for fr in fragmentos}
        if faltan:
            fallos.append(f"{clave}: faltan {faltan}")
        res["pasajes"][clave] = {"doc": doc, "pagina_pdf": pag, "uso": uso, "fragmentos": fragmentos,
                                 "todos_en_la_pagina (pdftotext)": not faltan, "segundo_extractor (pypdf)": segundo,
                                 "lineas": sorted(set(halladas))}
        lineas.append("")
        lineas.append(f"[{clave}] {doc} p.{pag} · {uso} · {'OK' if not faltan else 'FALTA ' + str(faltan)}")
        for h_ in sorted(set(halladas)):
            lineas.append("    " + h_)
        if segundo is not None and not all(segundo.values()):
            lineas.append("    (pypdf no encuentra: " + "; ".join(k for k, v in segundo.items() if not v) + ")")
    res["otras_adquisiciones"] = {}
    for clave, (doc, pag) in LISTAS.items():
        filas = ingresos_de_la_lista(textos[(doc, pag)])
        suma = round(sum(f["ingresos_anuales"] for f in filas if f["ingresos_anuales"] is not None), 1)
        sin = [f["viñeta"] for f in filas if f["ingresos_anuales"] is None]
        res["otras_adquisiciones"][clave] = {"doc": doc, "pagina_pdf": pag, "viñetas": len(filas), "sin_cifra_de_ingresos": sin,
                                             "suma_de_ingresos_anuales": suma, "detalle": filas}
        lineas.append("")
        lineas.append(f"[{clave}] {doc} p.{pag}: {len(filas)} viñetas; suma de ingresos anuales publicados = {suma}; sin cifra: {len(sin)}")
        for f in filas:
            lineas.append(f"    {f['ingresos_anuales']}  ·  {f['viñeta'][:110]}")
    res["resumen"] = {"pasajes": len(PASAJES), "fallos": fallos, "segundo_extractor": "pypdf" if pypdf is not None else None}
    lineas.append("")
    lineas.append(f"RESUMEN: {len(PASAJES)} pasajes; fallos {len(fallos)}; segundo extractor: {'pypdf' if pypdf is not None else 'no disponible'}")
    for f in fallos:
        lineas.append("  FALLO " + f)
    a.salida.write_text(json.dumps(res, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    a.informe.write_text("\n".join(lineas) + "\n", encoding="utf-8")
    print("\n".join(lineas))
    return 1 if fallos else 0


if __name__ == "__main__":
    sys.exit(main())
