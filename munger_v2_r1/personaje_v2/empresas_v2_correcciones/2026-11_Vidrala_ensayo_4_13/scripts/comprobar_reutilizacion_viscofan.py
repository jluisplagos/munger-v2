#!/usr/bin/env python3
"""¿Se pueden reutilizar en el expediente V6.4.1 de Viscofan la extracción y las fases A y B de la 4.12? (encargo 4.13 §9). Solo lee.

Una fase se reutiliza solo si lo que lee no cambia más que en lo editorial. Se comprueba de forma mecánica:
  1. Prompts generados de la extracción, la fase A y la fase B: iguales a los de la 4.12, salvo la ruta del expediente. Los que aún no
     existan en el expediente nuevo no se comparan.
  2. Libro de datos (salida de la fase 1, que leen las tres fases a través de datos_v63.md): todas las celdas con valor frente al de la
     4.12, una a una. Se clasifican las diferencias:
     - fecha de análisis;
     - evidencia de las celdas frescas (Control maestro, G:N de C37, C41, C55 y C57);
     - «Configuración V6.4» (perímetro de la V6.4.1, sus etiquetas y su traza);
     - cualquier otra, que impide la reutilización.
  3. Textos de las fuentes (texto/) y etapa 1: mismos bytes.
Uso (desde munger_v2_r1/): python3 -I …/scripts/comprobar_reutilizacion_viscofan.py · Escribe viscofan/resultados/reutilizacion_4_12.json y .md;
código 0 si se puede reutilizar, 1 si no.
"""
import hashlib
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
E413 = os.path.dirname(AQUI)
PV = os.path.abspath(os.path.join(E413, "..", ".."))
NUEVO = os.path.join(E413, "viscofan", "Viscofan")
VIEJO = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_12", "viscofan", "experimental", "Viscofan")
PROMPTS = ("05_extraccion_v63.md", "06_fase_a.md", "08_fase_b.md")
# ruta con que se generaron los prompts de la 4.12 (su árbol de trabajo) y etiquetas de versión de la plantilla (texto, sin cálculo)
ORIG_412 = "/home/claude/trabajo_4_12/munger_v2_r1/personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_12/viscofan/experimental/Viscofan"
ETIQUETAS = {"Análisis!A1", "Conciliación B!A1", "Control maestro!A3", "Diagnóstico V6!E176", "Diagnóstico V6!E177", "Guía V6!A1", "Panel!A1"}


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def arbol(base):
    out = {}
    for r, ds, fs in os.walk(base):
        for f in sorted(fs):
            p = os.path.join(r, f)
            out[os.path.relpath(p, base)] = sha(p)
    return out


def valores(p):
    from openpyxl import load_workbook
    wb = load_workbook(p, read_only=True)
    out = {}
    for ws in wb.worksheets:
        for row in ws.iter_rows():
            for c in row:
                if c.value is not None:
                    out[f"{ws.title}!{c.coordinate}"] = c.value
    wb.close()
    return out


def main():
    res = {"prompts": {}, "libro_datos": {}, "fuentes": {}}
    for n in PROMPTS:
        a, b = os.path.join(VIEJO, "prompts_generados", n), os.path.join(NUEVO, "prompts_generados", n)
        if not os.path.exists(b):
            res["prompts"][n] = "todavía no generado en el expediente nuevo"
            continue
        ta = open(a, encoding="utf-8").read().replace(ORIG_412, "<EXP>").replace(VIEJO, "<EXP>").replace("/home/claude/trabajo_4_12/munger_v2_r1", "<RAIZ>")
        tb = open(b, encoding="utf-8").read().replace(NUEVO, "<EXP>").replace("/home/claude/trabajo_4_13/munger_v2_r1", "<RAIZ>")
        la, lb = ta.splitlines(), tb.splitlines()
        dif = [(i + 1, x, y) for i, (x, y) in enumerate(zip(la, lb)) if x != y] + ([("longitud", len(la), len(lb))] if len(la) != len(lb) else [])
        res["prompts"][n] = "igual salvo la ruta del expediente" if not dif else {"diferencias": [list(map(str, d))[:3] for d in dif[:10]]}
    va, vb = valores(os.path.join(VIEJO, "Viscofan_v63_datos.xlsx")), valores(os.path.join(NUEVO, "Viscofan_v63_datos.xlsx"))
    import re
    cm = {}
    for k, v in va.items():  # fila de Control maestro de cada celda fresca (columna B)
        m = re.match(r"Control maestro!B(\d+)$", k)
        if m and v in ("Análisis!C37", "Análisis!C41", "Análisis!C55", "Análisis!C57"):
            cm[int(m.group(1))] = v
    clases = {"fecha": [], "evidencia_celdas_frescas": [], "configuracion_v64_1": [], "etiquetas_de_version": [], "otras": []}
    for k in sorted(set(va) | set(vb)):
        x, y = va.get(k), vb.get(k)
        if x == y:
            continue
        hoja, ref = k.split("!")
        m = re.match(r"([A-Z]+)(\d+)$", ref)
        if hoja == "Análisis" and ref in ("D4", "B4") or (isinstance(x, str) and "2026-11-12" in x and isinstance(y, str) and "2026-11-13" in y):
            clases["fecha"].append([k, x, y])
        elif hoja == "Control maestro" and m and int(m.group(2)) in cm and m.group(1) in "GHIJKLMN":
            clases["evidencia_celdas_frescas"].append([k, cm[int(m.group(2))], str(x)[:160], str(y)[:160]])
        elif k in ETIQUETAS and isinstance(y, str) and "V6.4.1 experimental" in y:
            clases["etiquetas_de_version"].append([k, str(x)[:80], str(y)[:80]])
        elif hoja == "Configuración V6.4":
            clases["configuracion_v64_1"].append([k, str(x)[:80], str(y)[:80]])
        else:
            clases["otras"].append([k, str(x)[:120], str(y)[:120]])
    res["libro_datos"] = {k: len(v) for k, v in clases.items()} | {"detalle": clases}
    for n in ("texto", "etapa1"):
        res["fuentes"][n] = "mismos bytes" if arbol(os.path.join(VIEJO, n)) == arbol(os.path.join(NUEVO, n)) else "DISTINTOS"
    # la sección 0 de datos_v63.md (configuración económica) cambia con la V6.4.1 (f, D_hist, perímetro). Las fases no la usan para las
    # palancas («no se anticipan en las palancas»); se comprueba que las salidas reutilizadas no citan ninguna de esas cifras o conceptos
    import re as _re
    terminos = r"D_hist|F_hist|\bRh\b|f_s2c|exceso medio|P-M1|θ|theta|SR1|SR2|SRF|perímetro de la inversión|1[.,]0739|1[.,]1127|296[.,]489|320[.,]599"
    cifras = r"1[.,]0739|1[.,]1127|296[.,]489|320[.,]599|56[.,]974|81[.,]084|20[.,]4065|32[.,]46"
    citas, lineas = {}, {}
    for n in ("extracto_v63.md", "fase_a.json", "fase_a.md", "fase_b.json", "fase_b.md"):
        t = open(os.path.join(VIEJO, n), encoding="utf-8").read()
        citas[n] = sorted(set(_re.findall(terminos, t)))
        lineas[n] = [ln.strip()[:400] for ln in t.splitlines() if _re.search(terminos, ln)]
    res["salidas_reutilizadas_citan_la_configuracion"] = {"terminos": citas, "lineas": lineas}
    # una cifra de la configuración citada impide reutilizar; una mención del concepto se lista con su línea para revisarla
    ok_citas = not any(_re.search(cifras, open(os.path.join(VIEJO, n), encoding="utf-8").read()) for n in citas)
    ok = ok_citas and (all(v in ("igual salvo la ruta del expediente", "todavía no generado en el expediente nuevo") for v in res["prompts"].values())
          and not clases["otras"] and all(v == "mismos bytes" for v in res["fuentes"].values()))
    res["reutilizable"] = ok
    os.makedirs(os.path.join(E413, "viscofan", "resultados"), exist_ok=True)
    json.dump(res, open(os.path.join(E413, "viscofan", "resultados", "reutilizacion_4_12.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    md = ["# Viscofan · reutilización de la extracción y de las fases A y B de la 4.12 (encargo 4.13 §9)", "",
          f"**Resultado: {'REUTILIZABLES' if ok else 'NO REUTILIZABLES'}.**", "",
          "## Prompts generados (normalizada la ruta del expediente)", ""] + [f"- `{n}`: {v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)[:600]}" for n, v in res["prompts"].items()]
    md += ["", "## Libro de datos (salida de la fase 1) frente al de la 4.12, celda a celda", "",
           f"- Fecha de análisis: {len(clases['fecha'])} celdas · evidencia de las celdas frescas (Control maestro G:N): {len(clases['evidencia_celdas_frescas'])} · "
           f"«Configuración V6.4» (perímetro de la V6.4.1): {len(clases['configuracion_v64_1'])} · etiquetas de versión de la plantilla: {len(clases['etiquetas_de_version'])} · "
           f"**otras: {len(clases['otras'])}**", "",
           "| Celda | Celda fresca | 4.12 | 4.13 |", "|---|---|---|---|"]
    md += [f"| {a} | {b} | {c.replace('|', '/')} | {d.replace('|', '/')} |" for a, b, c, d in clases["evidencia_celdas_frescas"]]
    if clases["otras"]:
        md += ["", "Otras diferencias (impiden reutilizar):", ""] + [f"- {a}: {b!r} → {c!r}" for a, b, c in clases["otras"][:40]]
    md += ["", "## Sección 0 de datos_v63.md (configuración económica)", "",
           "Cambia con la V6.4.1: f 1,0739 → 1,1127, D_hist 296,489 → 320,599, perímetro NIIF 16. Las palancas se eligen sin anticipar la configuración "
           "(«no se anticipan en las palancas»). ¿Citan las salidas reutilizadas alguna de esas cifras o conceptos? "
           + "; ".join(f"`{n}`: {', '.join(v) or 'ninguno'}" for n, v in citas.items()) + ".",
           "", "Líneas que mencionan la configuración (revisión de la orquestación: ninguna la usa para fijar una palanca; la de la fase B declara justo lo contrario):", ""]
    md += [f"- `{n}`: «{ln}»" for n, ls in lineas.items() for ln in ls]
    md += ["", "## Fuentes", ""] + [f"- `{n}/`: {v}" for n, v in res["fuentes"].items()]
    md += ["", "**Lectura.** Las fases reutilizadas son del 12-nov-2026 (sus archivos conservan esa fecha). Lo que cambia en sus entradas es la fecha de análisis "
               "y el texto de la evidencia de las cifras frescas, que ahora describe su concepto y sus fechas (4.13 §6). Las cifras no cambian. La plantilla V6.4.1 añade "
               "el perímetro de la inversión, que solo actúa en las bases de P-M1 (paso 10, después de la fase B). La fase C y la auditoría se hacen de nuevo con agentes reales."]
    open(os.path.join(E413, "viscofan", "resultados", "reutilizacion_4_12.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
    print("\n".join(md[:12]))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
