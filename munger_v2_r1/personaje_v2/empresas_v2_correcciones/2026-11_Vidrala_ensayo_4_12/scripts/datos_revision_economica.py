#!/usr/bin/env python3
"""Datos para la revisión económica de un expediente V6.4 experimental (encargo 4.12 §7 y §8). Solo lee.

Del libro evaluado RECALCULADO (recalc/<E>_v63_evaluada.xlsx) toma la hoja «Conciliación B» (tres bloques, MALO, NORMAL y BUENO, que
empiezan en las filas 5, 35 y 65; columnas B:K años 1–10 y L terminal) y las bases y derivados de «Configuración V6.4» (B54:B89); de
precio.json, V y probabilidades; de configuracion_v64_variantes.json, las variantes calculadas. Con eso escribe, por escenario:
  - reposición frente a crecimiento: reposición contable, requisito adicional, crédito, inversión fija para crecer, Δcirculante e
    inversión total por año y en el terminal, y las sumas de los años 1–10;
  - S2C y ROIC: S2C efectivo de los años, ROIC efectivo del terminal y rentabilidad marginal implícita de los años
    (S2C efectivo × margen × (1 − t));
  - terminal: peso en el valor y salto del año 10 al terminal (requisito, FCF y ventas);
  - capacidad conservada: años con ventas por debajo del máximo, inversión fija para crecer en esos años y en el terminal, y
    circulante liberado;
y la tabla de variantes con la diferencia frente a la activa. No juzga: los números van a la revisión económica, que los interpreta.
Uso (desde munger_v2_r1/): python3 -I …/scripts/datos_revision_economica.py CARPETA_EMPRESA
Escribe CARPETA_EMPRESA/../resultados/datos_revision_economica.json y .md.
"""
import json
import os
import sys

FILAS = {1: "anio", 2: "ventas", 3: "maximo_conservado", 4: "margen", 5: "nopat", 6: "da", 7: "cartera_p0", 8: "reposicion_contable", 9: "requisito",
         10: "fija_para_crecer", 11: "credito", 12: "adicional_pagada", 13: "delta_circulante", 14: "fija_bruta", 15: "inversion_total", 16: "fcf_identidad",
         17: "fcf_motor", 18: "diferencia", 19: "factor_descuento", 20: "vp"}
INICIO = {"MALO": 5, "NORMAL": 35, "BUENO": 65}


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    import openpyxl
    c = os.path.abspath(sys.argv[1])
    emp = os.path.basename(c)
    libro = os.path.join(c, "recalc", f"{emp}_v63_evaluada.xlsx")
    w = openpyxl.load_workbook(libro, data_only=True, read_only=True)
    cb, cf = w["Conciliación B"], w["Configuración V6.4"]
    pr = json.load(open(os.path.join(c, "precio.json"), encoding="utf-8"))
    var = json.load(open(os.path.join(c, "configuracion_v64_variantes.json"), encoding="utf-8"))
    conf = json.load(open(os.path.join(c, "configuracion_economica.json"), encoding="utf-8"))
    v = lambda ws, ref: ws[ref].value  # noqa: E731
    bases = {f"B{r}": v(cf, f"B{r}") for r in list(range(54, 64)) + list(range(66, 74)) + list(range(76, 90))}
    etiquetas = {f"B{r}": v(cf, f"A{r}") for r in bases and [int(k[1:]) for k in bases]}
    esc = {}
    for nombre, r0 in INICIO.items():
        filas = {}
        for off, k in FILAS.items():
            filas[k] = [v(cb, f"{col}{r0 + off}") for col in "BCDEFGHIJKL"]
        anios, term = {k: x[:10] for k, x in filas.items()}, {k: x[10] for k, x in filas.items()}
        num = lambda xs: [x for x in xs if isinstance(x, (int, float))]  # noqa: E731
        bajo_max = [i + 1 for i, (vt, mx) in enumerate(zip(anios["ventas"], anios["maximo_conservado"])) if isinstance(vt, (int, float)) and isinstance(mx, (int, float)) and vt < mx]
        s2c_roic = [v(cb, f"{col}{r0 + 24}") for col in "BC"]
        salto = [v(cb, f"{col}{r0 + 23}") for col in "BCD"]
        t_nopat = bases.get("B18") if isinstance(bases.get("B18"), (int, float)) else None
        esc[nombre] = {"estado": v(cb, f"B{r0}"), "anios": anios, "terminal": term,
                       "sumas_1_10": {k: sum(num(anios[k])) for k in ("nopat", "da", "reposicion_contable", "requisito", "fija_para_crecer", "credito", "adicional_pagada", "delta_circulante", "fija_bruta", "inversion_total", "fcf_motor", "vp")},
                       "vp_terminal": term.get("vp"), "peso_terminal": v(cb, f"B{r0 + 22}"),
                       "salto_anio_10_a_terminal": {"requisito": salto[0], "fcf": salto[1], "ventas": salto[2]},
                       "s2c_efectivo_anios": s2c_roic[0], "roic_efectivo_terminal": s2c_roic[1],
                       "anios_bajo_el_maximo": bajo_max, "fija_para_crecer_en_anios_bajo_el_maximo": sum(anios["fija_para_crecer"][i - 1] or 0 for i in bajo_max),
                       "circulante_liberado_1_10": -sum(x for x in num(anios["delta_circulante"]) if x < 0),
                       "comprobacion": v(cb, f"B{r0 + 25}")}
    t = None
    try:
        t = w["Configuración V6.4"]["B18"].value
    except KeyError:
        pass
    for nombre, e in esc.items():
        m = e["anios"]["margen"][-1]
        e["rentabilidad_marginal_implicita_anios"] = (e["s2c_efectivo_anios"] * m * (1 - t)) if all(isinstance(x, (int, float)) for x in (e["s2c_efectivo_anios"], m, t)) else None
    act = next(x for x in var["variantes"] if x["clave"] == "activa")
    tabla = [{"clave": x["clave"], "descripcion": x.get("descripcion"), "parametros_variados": x.get("parametros_variados"), "V": x.get("V"), "ponderado": x.get("ponderado"),
              "precio_si": x.get("precio_si"), "zona": x.get("zona"), "delta_precio_si_frente_a_activa": (x["precio_si"] - act["precio_si"]) if isinstance(x.get("precio_si"), (int, float)) else None}
             for x in var["variantes"]]
    out = {"expediente": c, "libro": libro, "configuracion": conf.get("naturaleza", "")[:300], "precio": pr.get("precio"), "V": pr.get("V"), "p": pr.get("p"),
           "ponderado": pr.get("ponderado"), "precio_si": pr.get("precio_si"), "zona": pr.get("zona"), "t_nopat": t,
           "bases_y_derivados": {k: {"etiqueta": etiquetas.get(k), "valor": x} for k, x in bases.items()}, "escenarios": esc, "variantes": tabla,
           "avisos_de_dominio": var.get("avisos_de_dominio")}
    res = os.path.join(os.path.dirname(c), "resultados")
    os.makedirs(res, exist_ok=True)
    json.dump(out, open(os.path.join(res, "datos_revision_economica.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    f = lambda x, d=2: (f"{x:,.{d}f}" if isinstance(x, (int, float)) else "—")  # noqa: E731
    md = [f"# Datos para la revisión económica · {emp}", "",
          f"Libro `{os.path.relpath(libro, os.path.dirname(c))}` (recalculado). Precio {pr.get('precio')} · V {[round(x, 2) for x in pr.get('V') or []]} · p {pr.get('p')} · ponderado {f(pr.get('ponderado'))} · "
          f"precio de Sí {f(pr.get('precio_si'))} · zona {pr.get('zona')} · t NOPAT {f(t, 4)}.", "",
          "## Bases y derivados de «Configuración V6.4»", "", "| Celda | Concepto | Valor |", "|---|---|---|"]
    md += [f"| {k} | {etiquetas.get(k) or ''} | {f(x, 4) if isinstance(x, (int, float)) else x} |" for k, x in bases.items() if x is not None]
    for nombre, e in esc.items():
        md += ["", f"## {nombre} · {e['estado']} · comprobación: {e['comprobacion']}", "",
               "| Partida | " + " | ".join(str(i) for i in range(1, 11)) + " | Terminal | Σ 1–10 |", "|---|" + "---|" * 12]
        for k in ("ventas", "maximo_conservado", "margen", "nopat", "da", "reposicion_contable", "requisito", "fija_para_crecer", "credito", "delta_circulante", "fija_bruta", "inversion_total", "fcf_motor", "vp"):
            d = 4 if k == "margen" else 1
            md.append(f"| {k} | " + " | ".join(f(x, d) for x in e["anios"][k]) + f" | {f(e['terminal'][k], d)} | {f(e['sumas_1_10'].get(k), 1) if k in e['sumas_1_10'] else ''} |")
        md += ["", f"- S2C efectivo de los años {f(e['s2c_efectivo_anios'], 4)} · ROIC efectivo del terminal {f(e['roic_efectivo_terminal'], 4)} · rentabilidad marginal implícita de los años "
               f"(S2C × margen del año 10 × (1 − t)) {f(e['rentabilidad_marginal_implicita_anios'], 4)}.",
               f"- Peso del terminal {f(e['peso_terminal'], 3)} · salto año 10 → terminal: requisito {f(e['salto_anio_10_a_terminal']['requisito'], 3)}, FCF {f(e['salto_anio_10_a_terminal']['fcf'], 3)}, ventas {f(e['salto_anio_10_a_terminal']['ventas'], 3)}.",
               f"- Años con ventas bajo el máximo conservado: {e['anios_bajo_el_maximo'] or 'ninguno'} · inversión fija para crecer en esos años {f(e['fija_para_crecer_en_anios_bajo_el_maximo'], 2)} · "
               f"en el terminal {f(e['terminal']['fija_para_crecer'], 2)} · circulante liberado en los años 1–10 {f(e['circulante_liberado_1_10'], 2)}."]
    md += ["", "## Variantes calculadas (diferencia del precio de Sí frente a la activa)", "", "| Variante | Parámetros que varía | Ponderado | Precio de Sí | Zona | Δ Sí |", "|---|---|---|---|---|---|"]
    md += [f"| {x['clave']} | {', '.join(x['parametros_variados'] or []) or '—'} | {f(x['ponderado'])} | {f(x['precio_si'])} | {x['zona']} | {f(x['delta_precio_si_frente_a_activa'])} |" for x in tabla]
    if out["avisos_de_dominio"]:
        md += ["", "## Avisos de dominio de las variantes", "", "```", json.dumps(out["avisos_de_dominio"], ensure_ascii=False, indent=1, default=str)[:6000], "```"]
    open(os.path.join(res, "datos_revision_economica.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
    print(f"OK: {emp} · {len(esc)} escenarios · {len(tabla)} variantes → resultados/datos_revision_economica.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
