#!/usr/bin/env python3
"""Inventario de las fuentes de Viscofan para el §8 del encargo 4.12 (solo lee el origen; escribe en viscofan/fuentes/).

1. Fuentes que cita el origen (`personaje_v2/empresas_v2/Viscofan/fase1_fuentes.json` y `fase1_partes/AR_*.json`): ninguna está en el
   paquete (ni PDF ni texto AR_2016.txt … AR_2025.txt).
2. Publicaciones recuperadas (copias de los archivos que la persona responsable dejó en una carpeta de su ordenador, conectada el
   12-nov-2026): por cada una, archivo, SHA-256, bytes, páginas, identificación por su contenido, edición y texto con marcas de página.
3. Edición y paginación: cada cifra citada por la fase 1 (`fase1_partes/AR_<año>.json`: cifra impresa y página) se busca en la página
   citada del texto recuperado. Solo una coincidencia completa permite asociar la publicación a las citas anteriores; si no, es OTRA
   edición y sirve para contrastar cifras, no como «original recuperado».
Uso (desde munger_v2_r1/): python3 -I personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_12/scripts/inventario_fuentes_viscofan.py
"""
import hashlib
import json
import os
import re
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
EXP = os.path.dirname(AQUI)
PV = os.path.abspath(os.path.join(EXP, "..", ".."))
RAIZ = os.path.dirname(PV)
ORIG = os.path.join(PV, "empresas_v2", "Viscofan")
F = os.path.join(EXP, "viscofan", "fuentes")
URL_2025 = "https://public.viscofan.com/investor-relations/financialinformation/en/Viscofan%20Group%202025%20Annual%20Report%20PDF%20version.pdf"
URL_IR = "https://www.viscofan.com/investor-relations/financial-information-and-annual-report/2025"
# archivo recuperado → (ejercicio, nombre en la carpeta de la persona responsable, identificación por el contenido)
RECUPERADOS = {
    "AR_2025.pdf": (2025, "Viscofan Group 2025 Annual Report PDF version.pdf", "Informe anual consolidado del Grupo Viscofan 2025 (inglés; título del PDF «Informe consolidado Grupo Viscofan 2025_EN_def», creado el 25-mar-2026)", URL_2025),
    "CF_2024.pdf": (2024, "consolidated-financial-statements-24.pdf", "Cuentas consolidadas 2024 (inglés), estados a 31-dic-2024", None),
    "CA_2023_es.pdf": (2023, "viscofan-ccaa-2023-en.pdf", "Cuentas anuales consolidadas 2023 en ESPAÑOL (miles de euros), pese al nombre del archivo", None),
    "CF_2022_compilacion.pdf": (2022, "ia_en.pdf", "Compilación hecha con iLovePDF: informes de verificación y auditoría de 2021 (español) y estados financieros consolidados 2022 (inglés)", None),
    "CF_2021.pdf": (2021, "ingles.pdf", "Cuentas anuales consolidadas 2021 (inglés)", None),
    # (4.12, segunda entrega de la persona responsable, 12-nov 21:59) ediciones con la paginación de la fase 1 para 2017, 2019 y 2020, y otras
    # ediciones de 2016 y 2018 (en español) que contienen las cifras; sustituyen a la edición de 2020 de la primera entrega
    "AR_2020.pdf": (2020, "2020/2020_Annual_Report_EN.pdf", "Informe anual 2020 del Grupo Viscofan (inglés, con las cuentas consolidadas)", None),
    "AR_2019.pdf": (2019, "2019/2019_Annual_Report_EN.pdf", "Informe anual 2019 del Grupo Viscofan (inglés, con las cuentas consolidadas)", None),
    "IA_2018_es.pdf": (2018, "2018/2018_Informe_Anual_Integrado.pdf", "Informe anual integrado 2018 del Grupo Viscofan (español)", None),
    "AR_2017.pdf": (2017, "2017/2017_Annual_Accounts_Management_Report_EN.pdf", "Cuentas anuales e informe de gestión consolidados 2017 (inglés)", None),
    "IA_2016_es.pdf": (2016, "2016/2016_Informe_Anual_Integrado.pdf", "Informe anual integrado 2016 del Grupo Viscofan (español)", None),
    # informes anuales en español de 2021 y 2023, con el informe de gestión (mercado, ventas, precios) que las cuentas recuperadas no traen
    "IA_2021_es.pdf": (2021, "2021/2021_Informe_Anual.pdf", "Informe anual 2021 del Grupo Viscofan (español, con el informe de gestión)", None),
    "IA_2023_es.pdf": (2023, "2023/2023_Informe_Anual.pdf", "Informe anual 2023 del Grupo Viscofan (español, con el informe de gestión)", None),
}
# consultadas y no conservadas en el paquete (huella registrada): no se usan en ningún resultado final
SUSTITUIDAS = [{"archivo": "AR_2020_otra_edicion.pdf", "nombre_en_la_carpeta": "annual-report-2020.pdf", "ejercicio": 2020, "bytes": 19899592,
                "sha256": "efbe9e1d1c7362e7a669ab471552fd5e318fc7b48be24f50aac53f73130c39f3",
                "motivo": "otra edición del informe de 2020 (0 de 63 cifras en la página citada); sustituida por AR_2020.pdf, que tiene la paginación de la fase 1"}]
NO_USADOS = ("En la carpeta hay además, y no se copian: los documentos de 2026 (posteriores a la base); los informes trimestrales y sus anexos; "
             "las versiones en el otro idioma de 2016–2020 (2016 y 2018 en inglés, 2017, 2019 y 2020 en español) y los informes anuales en español de "
             "2022, 2024 y 2025, que no tienen la paginación de la fase 1 (sus cifras ya están en las ediciones conservadas); los paquetes ESEF/FEUE "
             "(.zip, .xhtml, .xbri); ARR-24 y CGAR-24 (remuneraciones y gobierno corporativo 2024); tabla.xls (cifras clave de 2019).")


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def paginas_texto(p):
    t = open(p, encoding="utf-8").read()
    partes = re.split(r"\[PDF PAGE (\d+)\]", t)
    return {int(partes[i]): partes[i + 1] for i in range(1, len(partes), 2)}


def n_paginas(pdf):
    r = subprocess.run(["pdfinfo", pdf], capture_output=True, text=True)
    m = re.search(r"Pages:\s+(\d+)", r.stdout)
    return int(m.group(1)) if m else None


def main():
    citadas = json.load(open(os.path.join(ORIG, "fase1_fuentes.json"), encoding="utf-8"))
    en_paquete = {a: any(os.path.exists(os.path.join(ORIG, d, n)) for d in ("", "texto", "pdf") for n in (f, f.replace(".txt", ".pdf")))
                  for a, f in citadas.items()}
    out = {"origen": os.path.relpath(ORIG, RAIZ), "fuentes_citadas_por_el_origen": citadas, "presentes_en_el_paquete": en_paquete,
           "localizadores_oficiales": [URL_IR, URL_2025], "recuperadas": [], "faltan": [], "fecha_de_consulta": "2026-11-12",
           "procedencia": ("copias de los archivos que la persona responsable dejó en una carpeta de su ordenador, conectada a esta sesión el 12-nov-2026 "
                           "(primera entrega hacia las 20:38; segunda, con una subcarpeta por año, a las 21:59); la consola no puede descargar de "
                           "viscofan.com: no se descargaron de la web desde aquí"),
           "sustituidas_no_conservadas": SUSTITUIDAS, "no_usados": NO_USADOS}
    for nombre, (anio, original, ident, url) in RECUPERADOS.items():
        pdf = os.path.join(F, "pdf", nombre)
        txt = os.path.join(F, "texto", nombre.replace(".pdf", ".txt"))
        reg = {"archivo": os.path.relpath(pdf, RAIZ), "nombre_en_la_carpeta": original, "ejercicio": anio, "identificacion": ident, "url_oficial": url,
               "sha256": sha(pdf), "bytes": os.path.getsize(pdf), "paginas": n_paginas(pdf), "texto_con_marcas_de_pagina": os.path.relpath(txt, RAIZ)}
        pj = os.path.join(ORIG, "fase1_partes", f"AR_{anio}.json")
        if os.path.exists(pj) and os.path.exists(txt):
            pg = paginas_texto(txt)
            partes = json.load(open(pj, encoding="utf-8"))["partidas"]
            tot = misma = otra = 0
            for v in partes.values():
                if not isinstance(v, dict):
                    continue
                for lado in ("actual", "anterior"):
                    for x in v.get(lado) or []:
                        if isinstance(x, dict) and x.get("impreso"):
                            tot += 1
                            if x.get("pagina") in pg and x["impreso"] in pg[x["pagina"]]:
                                misma += 1
                            elif any(x["impreso"] in t for t in pg.values()):
                                otra += 1
            reg["contraste_con_las_citas_de_la_fase_1"] = {"citas": tot, "en_la_misma_pagina": misma, "en_otra_pagina": otra, "no_encontradas": tot - misma - otra}
            if tot and misma == tot:
                reg["edicion"] = (f"MISMA PAGINACIÓN que la fuente AR_{anio}.txt de la fase 1: las {tot} cifras citadas están en la página citada. Se asocia a esas citas; "
                                  "como no hay huella del original, se dice «misma paginación y cifras», no «mismo archivo»")
            else:
                reg["edicion"] = (f"OTRA EDICIÓN que la fuente AR_{anio}.txt de la fase 1 ({misma} de {tot} cifras en la página citada): sirve para contrastar cifras; "
                                  "no es el original recuperado")
        out["recuperadas"].append(reg)
    tiene = {r["ejercicio"] for r in out["recuperadas"]}
    for a in sorted(citadas):
        if int(a) not in tiene:
            out["faltan"].append({"ejercicio": int(a), "fuente_citada": citadas[a], "efecto": "sus cifras de la Historia se reutilizan sin contraste con el documento (extracción antigua; no equivale a verificar el PDF)"})
    misma = {r["ejercicio"] for r in out["recuperadas"] if (r.get("edicion") or "").startswith("MISMA")}
    vistos = set()
    for r in out["recuperadas"]:
        if (r.get("edicion") or "").startswith("OTRA EDICIÓN") and r["ejercicio"] not in misma and r["ejercicio"] not in vistos:
            vistos.add(r["ejercicio"])
            out["faltan"].append({"ejercicio": r["ejercicio"], "fuente_citada": citadas.get(str(r["ejercicio"])),
                                  "efecto": "la edición que citan las páginas de la fase 1 no se ha recuperado; sus cifras se contrastan en otra edición ("
                                            + ", ".join(f"`{os.path.basename(x['archivo'])}`" for x in out["recuperadas"] if x["ejercicio"] == r["ejercicio"]) + "), por su contenido"})
    out["faltan"].append({"fuente": "Bundesbank, rendbund-data.pdf (rf de Vidrala)", "efecto": "no se ha podido conservar desde aquí; la rf del ensayo de Vidrala sigue con la cita de fase1_metadatos.json"})
    json.dump(out, open(os.path.join(F, "inventario_fuentes_viscofan.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    md = ["# Fuentes de Viscofan · inventario (encargo 4.12 §8)", "",
          f"**Origen:** `{out['origen']}`. Cita {len(citadas)} fuentes (`fase1_fuentes.json`: {', '.join(citadas.values())}); **ninguna está en el paquete**: ni los PDF ni los textos.", "",
          f"**Procedencia de las recuperadas:** {out['procedencia']}. Fecha de consulta: {out['fecha_de_consulta']}. Localizadores oficiales: {URL_IR} · {URL_2025}.", "",
          "| Ejercicio | Archivo | Identificación | SHA-256 | Págs. | Edición frente a la fase 1 |", "|---|---|---|---|---|---|"]
    for r in sorted(out["recuperadas"], key=lambda x: -x["ejercicio"]):
        c = r.get("contraste_con_las_citas_de_la_fase_1") or {}
        md.append(f"| {r['ejercicio']} | `{os.path.basename(r['archivo'])}` (en la carpeta: `{r['nombre_en_la_carpeta']}`) | {r['identificacion']} | `{r['sha256'][:16]}…` | {r['paginas']} | "
                  f"{r.get('edicion', '—')} ({c.get('en_la_misma_pagina')} de {c.get('citas')} en la misma página; {c.get('en_otra_pagina')} en otra; {c.get('no_encontradas')} no encontradas) |")
    md += ["", "**Faltan:**"] + [f"- {x.get('ejercicio', '')} {x.get('fuente_citada') or x.get('fuente')}: {x['efecto']}." for x in out["faltan"]]
    md += ["", "**Consultadas y no conservadas** (huella registrada; no se usan en ningún resultado final):"]
    md += [f"- {x['ejercicio']} `{x['archivo']}` (en la carpeta: `{x['nombre_en_la_carpeta']}`, {x['bytes']} bytes, SHA-256 `{x['sha256'][:16]}…`): {x['motivo']}." for x in SUSTITUIDAS]
    md += ["", NO_USADOS]
    open(os.path.join(F, "inventario_fuentes_viscofan.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
    print(f"OK: {len(out['recuperadas'])} recuperadas · {len(out['faltan'])} faltas → viscofan/fuentes/inventario_fuentes_viscofan.json/.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
