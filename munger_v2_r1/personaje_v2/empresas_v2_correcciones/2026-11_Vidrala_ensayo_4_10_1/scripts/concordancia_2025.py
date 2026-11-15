#!/usr/bin/env python3
"""Concordancia de las entradas del ensayo 2025 (entrega 4.10.1, encargo §4.2): configuración ↔ fase1_metadatos.json ↔ fase1_v63.json ↔
libro de datos ↔ datos volcados (datos_v63.json) y, si existe, libro evaluado. Además busca residuos de la base anterior (87,9 €,
3.094,6, 35,206 como N, 3-nov-2026, rf 0,0329) como DATOS del caso y comprueba que ningún valor migrado prevaleció sin declararse.
Uso: python3 -I concordancia_2025.py [--libro] [--salida DIR]   Escribe (por defecto en) ../resultados/concordancia_2025[_evaluada].json y .md."""
import json
import os
import sys

import openpyxl

AQUI = os.path.dirname(os.path.abspath(__file__))
ENS = os.path.dirname(AQUI)
ACT = os.path.join(ENS, "Vidrala")
C = json.load(open(os.path.join(ENS, "configuracion", "configuracion_ensayo_2025.json"), encoding="utf-8"))
e = C["entradas"]
EVAL = "--libro" in sys.argv
SALIDA = sys.argv[sys.argv.index("--salida") + 1] if "--salida" in sys.argv else os.path.join(ENS, "resultados")   # (control de la entrega: a un temporal)
RX = C.get("datos_heredados_reexpresados_a_2025", {})
ESP = {"Análisis!C37": e["precio"]["valor"], "Análisis!C41": e["E_capitalizacion"]["valor"], "Análisis!C55": e["N_millones"]["valor"],
       "Análisis!C57": e["tasa_sin_riesgo"]["valor"], "Análisis!D4": C["fechas"]["ejecucion"],
       **{f"Análisis!{k}": v["valor"] for k, v in C["caso_principal_analisis"].items()},
       **{f"Análisis!{k}": v["valor"] for k, v in RX.get("celdas", {}).items()}}   # (preparación 2) datos reexpresados a 31-dic-2025
DERIVADAS = {f"Análisis!{k}" for k, v in RX.get("celdas", {}).items() if v.get("derivada")}
RESIDUOS = {"precio 87,9": 87.9, "E 3.094,6": 3094.6, "N 35,206": 35.206, "rf 0,0329": 0.0329}
# (preparación 2) valores de la etapa 1 medidos a 30-jun-2026 en las celdas reexpresadas: no pueden quedar como datos del caso
RESIDUOS_CELDA = {"Análisis!C24": 0.13, "Análisis!C33": 0.69, "Análisis!C34": "No", "Análisis!C42": 7.68, "Análisis!C53": 109.4, "Análisis!C54": 409.6}


def j(p):
    return json.load(open(p, encoding="utf-8"))


def num_eq(a, b):
    try:
        return abs(float(a) - float(b)) < 1e-9
    except (TypeError, ValueError):
        return str(a)[:10] == str(b)[:10]


meta, f1 = j(os.path.join(ACT, "fase1_metadatos.json")), j(os.path.join(ACT, "fase1_v63.json"))
libro = os.path.join(ACT, "Vidrala_v63_evaluada.xlsx" if EVAL else "Vidrala_v63_datos.xlsx")
wb = openpyxl.load_workbook(libro, data_only=False)
val = lambda ref: wb[ref.split("!")[0]][ref.split("!")[1]].value  # noqa: E731
datos = j(os.path.join(ACT, "datos_v63.json")) if os.path.exists(os.path.join(ACT, "datos_v63.json")) else {}
an = (datos.get("analisis") or {}) if isinstance(datos, dict) else {}
filas, ok = [], True
fuente_f1 = {"Análisis!C37": f1.get("precio", {}).get("valor"), "Análisis!C41": f1.get("capitalizacion", {}).get("valor"),
             "Análisis!C55": f1.get("acciones_diluidas", {}).get("valor"), "Análisis!C57": f1.get("tasa_sin_riesgo", {}).get("valor"),
             "Análisis!D4": f1.get("fecha_analisis"), **{f"Análisis!{k}": (f1.get("analisis", {}).get(k) or {}).get("valor") for k in C["caso_principal_analisis"]},
             **{f"Análisis!{k}": ("(derivada)" if v.get("derivada") else (f1.get("analisis", {}).get(k) or {}).get("valor")) for k, v in RX.get("celdas", {}).items()}}
fuente_meta = {"Análisis!C37": meta.get("precio", {}).get("valor"), "Análisis!C41": meta.get("capitalizacion", {}).get("valor"),
               "Análisis!C55": meta.get("acciones_diluidas", {}).get("valor"), "Análisis!C57": meta.get("tasa_sin_riesgo", {}).get("valor"), "Análisis!D4": meta.get("fecha_analisis")}
for ref, esp in ESP.items():
    v_meta = fuente_meta.get(ref, "(no aplica)")
    v_f1, v_lib = fuente_f1.get(ref), val(ref)
    v_dat = an.get(ref.split("!")[1], {}).get("valor") if isinstance(an.get(ref.split("!")[1]), dict) else an.get(ref.split("!")[1])
    bien = (v_f1 == "(derivada)" or num_eq(v_f1, esp)) and num_eq(v_lib, esp) and (v_meta == "(no aplica)" or num_eq(v_meta, esp)) and (v_dat is None or num_eq(v_dat, esp))
    ok &= bien
    filas.append({"celda": ref, "configuracion": esp, "fase1_metadatos": v_meta, "fase1_v63": v_f1, "libro": v_lib, "datos_v63": v_dat, "concuerda": bien})
# residuos: en las celdas de datos del libro (Análisis C37/C41/C55/C57/D4 y Palancas C45/C46) y en los JSON activos
res = []
for ref in ("Análisis!C37", "Análisis!C41", "Análisis!C55", "Análisis!C57", "Análisis!D4", "Palancas!C45", "Palancas!C46"):
    v = val(ref)
    for et, x in RESIDUOS.items():
        if isinstance(v, (int, float)) and abs(v - x) < 1e-9:
            res.append(f"{ref} = {v} ({et})")
    if isinstance(v, str) and "2026-11-03" in v:
        res.append(f"{ref} = {v} (fecha de noviembre de 2026)")
for ref, x in RESIDUOS_CELDA.items():
    if num_eq(val(ref), x) and not num_eq(ESP.get(ref), x):
        res.append(f"{ref} = {val(ref)} (valor de la etapa 1 a 30-jun-2026)")
# (preparación 2) evidencia de Control maestro de las celdas de datos: ningún periodo o fuente de 2026 en las filas reexpresadas ni en D4/C37/C57
cm = wb["Control maestro"]
filas_rx = set(RX.get("vaciar_en_la_copia_de_etapa1", {}).get("Control maestro (filas de evidencia, columnas E:N)", []))
evid = []
for r in range(17, 176):
    b = cm[f"B{r}"].value
    if r in filas_rx:
        for col in "GJLN":
            t = str(cm[f"{col}{r}"].value or "")
            if any(m in t for m in ("30/06/2026", "LTM 30/06", "1S2026", "IPP CNMV 1S2026", "09/10/2026", "10/10/2026")):
                res.append(f"Control maestro!{col}{r} ({b}): «{t[:80]}»")
        evid.append({"fila": r, "celda": b, "periodo_G": cm[f"G{r}"].value, "fuente_J": str(cm[f"J{r}"].value or "")[:160]})
for fic in ("fase1_metadatos.json", "fase1_v63.json", "alcance_v2.json"):
    s = open(os.path.join(ACT, fic), encoding="utf-8").read()
    for marca in ('"valor": 87.9', '"valor": 3094.6', '"valor": 35.206,', '"valor": 0.0329', '"fecha": "2026-11-03"', '"fecha_analisis": "2026-11-03"'):
        if marca in s:
            res.append(f"{fic}: {marca}")
ok &= not res
# (revisión interna 4.10.1, H-1 y H-2) TEXTOS heredados con cifras o fechas de la base anterior en la evidencia de Control maestro de las
# celdas de datos de Análisis (columnas G a N) y en las notas (_notas) de los JSON activos. No son datos del caso (los valores concuerdan
# arriba) y no bloquean, pero se IDENTIFICAN aquí uno a uno: el libro cerrado no se reescribe sin una auditoría nueva (D-EVIDENCIA-2026).
MARCAS_TEXTO = ("88,70", "88,7 ", "34,185", "3.032", "87,9", "3.094", "35,206 −", "35,206 M", "30/06/2026", "LTM 30/06", "1S2026", "1S26", "09/10/2026",
                "10/10/2026", "25/09", "23/06", "3.029", "liberada 2026", "Trading Economics", "autocartera ignorada")
textos = []
for r in range(17, 176):
    b = cm[f"B{r}"].value
    if not (isinstance(b, str) and b.startswith("Análisis!")):
        continue
    for col in "GHIJKLMN":
        t = str(cm[f"{col}{r}"].value or "")
        hits = [m for m in MARCAS_TEXTO if m in t]
        if hits:
            textos.append({"celda": f"Control maestro!{col}{r}", "de": b, "marcas": hits, "texto": t[:160]})
for fic in ("fase1_metadatos.json", "fase1_v63.json"):
    for i, n in enumerate(j(os.path.join(ACT, fic)).get("_notas") or []):
        hits = [m for m in MARCAS_TEXTO if m in str(n)]
        if hits and "4.10.1" not in str(n):
            textos.append({"celda": f"{fic} → _notas[{i}]", "de": "nota heredada de los metadatos de la 4.6.1", "marcas": hits, "texto": str(n)[:160]})
reg_p = os.path.join(ACT, "Vidrala_v63_datos.xlsx.fase1.registro.json")
no_pis = j(reg_p).get("no_pisadas", []) if os.path.exists(reg_p) else []
declaradas = {f"Análisis!{k}" for k in C["caso_principal_analisis"]}
silenciosas = [x for x in no_pis if isinstance(x, dict) and isinstance(x.get("actual"), (int, float)) and x.get("celda") not in declaradas
               and not num_eq(x.get("actual"), x.get("nuevo"))]
ok &= not silenciosas
fechas = {"Palancas!C45 (fecha del precio)": val("Palancas!C45"), "Palancas!C46 (fecha de las acciones)": val("Palancas!C46")}
out = {"libro": os.path.basename(libro), "concordancia": filas, "residuos_de_la_base_anterior": res, "migrados_que_prevalecen_sin_declarar": silenciosas,
       "no_pisadas_registradas": no_pis, "fechas_en_el_libro": fechas, "evidencia_de_las_filas_reexpresadas": evid,
       "textos_heredados_identificados": textos, "resultado": "CONCUERDA" if ok else "NO CONCUERDA"}
suf = "_evaluada" if EVAL else ""
json.dump(out, open(os.path.join(SALIDA, f"concordancia_2025{suf}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
md = [f"# Concordancia de las entradas del ensayo 2025 ({os.path.basename(libro)})", "", "| Celda | Configuración | fase1_metadatos | fase1_v63 | Libro | datos_v63 | ¿Concuerda? |", "|---|---|---|---|---|---|---|"]
md += [f"| {f['celda']} | {f['configuracion']} | {f['fase1_metadatos']} | {f['fase1_v63']} | {f['libro']} | {f['datos_v63']} | {'sí' if f['concuerda'] else 'NO'} |" for f in filas]
md += ["", f"**Residuos de la base anterior como datos del caso:** {res or 'ninguno'}", "", f"**Valores migrados que prevalecen sin declararse:** {silenciosas or 'ninguno'}",
       "", f"**Fechas en el libro:** {fechas}", "",
       f"**Textos heredados con cifras o fechas de la base anterior (identificados; no son datos del caso ni bloquean):** {len(textos)}. "
       "Los valores de esas celdas concuerdan con la configuración (tabla de arriba); lo que queda es la explicación de la etapa 1 o de los metadatos de la "
       "4.6.1 en la evidencia de Control maestro o en las notas. El libro cerrado no se reescribe sin una auditoría nueva (D-EVIDENCIA-2026).", ""]
md += [f"- `{x['celda']}` ({x['de']}; {', '.join(x['marcas'])}): «{x['texto'][:120]}»" for x in textos]
md += ["", f"**Resultado:** {out['resultado']}"]
open(os.path.join(SALIDA, f"concordancia_2025{suf}.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
print("\n".join(md))
sys.exit(0 if ok else 1)
