#!/usr/bin/env python3
"""Contraste selectivo y conciliación de inversión, amortización y arrendamientos de Viscofan 2021–2025 (encargo 4.13 §6 y §7).

No basta con encontrar dígitos en una página: cada cifra se toma de una LÍNEA concreta cuya etiqueta dice el concepto, en la COLUMNA
que dice la cabecera de su tabla (el año), con su SIGNO tal como se publica y su UNIDAD (miles de euros → millones). Para las altas de
derechos de uso, que se publican en una frase, se lee la frase. Cada cifra se contrasta con su comparativo del informe siguiente
cuando existe (la edición más reciente manda, como en la fase 1) y con el valor de la Historia del expediente cuando lo hay.

Después concilia, año a año: activo por derecho de uso (saldo inicial + altas − amortización ± otros = saldo final), pasivo por
arrendamientos (inicial + altas − pagos ± otros = final) y las bases de inversión de P-M1 con tres perímetros:
  - «caja» (la plantilla V6.4): capex de caja frente a toda la D&A (incluida la de los derechos de uso);
  - «NIIF 16 completo»: capex de caja + altas de derechos de uso frente a toda la D&A; coherente con el motor B, que trata los
    arrendamientos como capital (Historia fila 32) y como deuda (puente, Diagnóstico V6 C16) y no resta sus pagos del flujo;
  - «solo activos propios»: capex de caja frente a la D&A sin los derechos de uso; solo sería coherente si además se reexpresaran el
    NOPAT (EBIT sin NIIF 16), el capital y el puente (sin el pasivo por arrendamientos): no se construye.
Solo lee. Uso (desde munger_v2_r1/): python3 -I …/scripts/conciliacion_arrendamientos_viscofan.py
Escribe resultados/conciliacion_arrendamientos_viscofan.json y .md en la carpeta del ensayo 4.13.
"""
import json
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
E413 = os.path.dirname(AQUI)
PV = os.path.abspath(os.path.join(E413, "..", ".."))
VIS = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_12", "viscofan")
TXT = os.path.join(VIS, "fuentes", "texto")
LIBRO = os.path.join(VIS, "experimental", "Viscofan", "Viscofan_v63_evaluada.xlsx")
ANIOS = [2021, 2022, 2023, 2024, 2025]

# (concepto, archivo, etiqueta (regex de la línea), signo publicado esperado, años de la cabecera en orden) → valores por año
TABLAS = [
    ("amortizacion_derechos_de_uso", "CF_2021.txt", r"Depreciation expenses on right of use", -1, (2021, 2020)),
    ("amortizacion_derechos_de_uso", "CF_2022_compilacion.txt", r"Right-of-use asset depreciation expense", -1, (2022, 2021)),
    ("amortizacion_derechos_de_uso", "CA_2023_es.txt", r"Gastos por amortización de activos por derecho de uso", -1, (2023, 2022)),
    ("amortizacion_derechos_de_uso", "CF_2024.txt", r"Right-of-use asset depreciation expense", -1, (2024, 2023)),
    ("amortizacion_derechos_de_uso", "AR_2025.txt", r"Depreciation of right-of-use assets", -1, (2025, 2024)),
    ("pagos_arrendamientos", "CF_2021.txt", r"Payments of Right-of-use assets", -1, (2021, 2020)),
    ("pagos_arrendamientos", "CF_2022_compilacion.txt", r"Payments for right-of-use assets", -1, (2022, 2021)),
    ("pagos_arrendamientos", "CF_2024.txt", r"Payments for right-of-use assets", -1, (2024, 2023)),
    ("pagos_arrendamientos", "AR_2025.txt", r"Lease payments for right-of-use assets", -1, (2025, 2024)),
    ("activo_derechos_de_uso", "CF_2022_compilacion.txt", r"^Right-of-use assets\s+7\.1", 1, (2022, 2021)),
    ("activo_derechos_de_uso", "CA_2023_es.txt", r"Activos por derecho de uso\s+7\.1", 1, (2023, 2022)),
    ("activo_derechos_de_uso", "CF_2024.txt", r"Right-of-use assets\s+7\.1", 1, (2024, 2023)),
    ("activo_derechos_de_uso", "AR_2025.txt", r"Right-of-use assets\s+7\.1", 1, (2025, 2024)),
    ("pasivo_largo_plazo", "AR_2025.txt", r"Long-term debts for right-of-use assets\s+7\.2", 1, (2025, 2024)),
    ("pasivo_corto_plazo", "AR_2025.txt", r"Short-term debts for right-of-use assets\s+7\.2", 1, (2025, 2024)),
]
# altas: frase «Additions to right-of-use assets in AAAA amounted to X thousand euros; Y thousand euros in AAAA-1»
FRASES_ALTAS = ["CF_2021.txt", "CF_2022_compilacion.txt", "CA_2023_es.txt", "CF_2024.txt", "AR_2025.txt"]
NUM = re.compile(r"[−\-–]?\d{1,3}(?:[.,]\d{3})+|[−\-–]?\d+")


def num(t):
    neg = t[0] in "−-–"
    t = t.lstrip("−-–").replace(".", "").replace(",", "")
    return -int(t) if neg else int(t)


def pagina(lineas, i):
    for j in range(i, -1, -1):
        m = re.search(r"\[PDF PAGE (\d+)\]", lineas[j])
        if m:
            return int(m.group(1))
    return None


def cabecera(lineas, i, anios):
    """Línea de cabecera de la tabla (hasta 60 líneas arriba) con los años en el orden esperado."""
    pat = re.compile(r"\b" + r"\D+".join(str(a) for a in anios) + r"\b")
    for j in range(i - 1, max(-1, i - 60), -1):
        if pat.search(lineas[j]) and ("Thousands" in lineas[j] or "Miles" in lineas[j] or "Notes" in lineas[j] or "Notas" in lineas[j] or re.search(r"\s{3,}\d{4}\s{3,}\d{4}", lineas[j])):
            return j
    return None


def leer_tabla(concepto, archivo, etiqueta, signo, anios):
    lineas = open(os.path.join(TXT, archivo), encoding="utf-8", errors="replace").read().split("\n")
    for i, l in enumerate(lineas):
        if re.search(etiqueta, l.strip() if etiqueta.startswith("^") else l):
            resto = re.sub(etiqueta, "", l.strip() if etiqueta.startswith("^") else l, count=1)
            resto = re.sub(r"\b\d+\.\d\b", "", resto, count=1)  # la nota (7.1, 12.1) no es una cifra
            vals = [num(x) for x in NUM.findall(resto)]
            h = cabecera(lineas, i, anios)
            if len(vals) < 2 or h is None:
                continue
            return [{"concepto": concepto, "anio": a, "valor_publicado": vals[k], "signo_publicado": "negativo" if vals[k] < 0 else "positivo",
                     "signo_esperado_ok": (vals[k] < 0) == (signo < 0), "unidad_publicada": "miles de euros", "valor_mm": abs(vals[k]) / 1000,
                     "archivo": archivo, "linea": i + 1, "pagina_pdf": pagina(lineas, i), "etiqueta": l.strip()[:110],
                     "cabecera": {"linea": h + 1, "texto": lineas[h].strip()[:110]}, "columna": k + 1} for k, a in enumerate(anios)]
    return [{"concepto": concepto, "anio": a, "error": f"no se encontró la línea «{etiqueta}» con su cabecera en {archivo}", "archivo": archivo} for a in anios]


def leer_altas(archivo):
    lineas = open(os.path.join(TXT, archivo), encoding="utf-8", errors="replace").read().split("\n")
    for i, l in enumerate(lineas):
        m = re.search(r"Additions to right-of-use assets (?:during|in) (\d{4}) amounted to €?([\d,.]+) thousand(?: euros)?; €?([\d,.]+) thousand(?: euros)? in (\d{4})", l + " " + (lineas[i + 1] if i + 1 < len(lineas) else ""))
        if m:
            a1, v1, v2, a2 = int(m.group(1)), num(m.group(2)), num(m.group(3)), int(m.group(4))
            # (4.13, revisión interna R11) la búsqueda une cada línea con la siguiente para frases partidas: la línea citada es la
            # del comienzo de la frase, que puede ser la siguiente
            j = i if m.start() < len(l) else i + 1
            base = {"concepto": "altas_derechos_de_uso", "signo_publicado": "positivo", "signo_esperado_ok": True, "unidad_publicada": "miles de euros",
                    "archivo": archivo, "linea": j + 1, "pagina_pdf": pagina(lineas, j), "etiqueta": lineas[j].strip()[:140], "cabecera": None, "columna": "frase"}
            return [dict(base, anio=a1, valor_publicado=v1, valor_mm=v1 / 1000), dict(base, anio=a2, valor_publicado=v2, valor_mm=v2 / 1000)]
    return [{"concepto": "altas_derechos_de_uso", "error": f"no se encontró la frase de altas en {archivo}", "archivo": archivo}]


def main():
    obs = []
    for t in TABLAS:
        obs += leer_tabla(*t)
    for a in FRASES_ALTAS:
        obs += leer_altas(a)
    errores = [o for o in obs if "error" in o]
    # la edición más reciente manda; las demás contrastan
    orden = {"CF_2021.txt": 1, "CF_2022_compilacion.txt": 2, "CA_2023_es.txt": 3, "CF_2024.txt": 4, "AR_2025.txt": 5}
    serie, contrastes = {}, []
    for o in sorted([o for o in obs if "error" not in o], key=lambda o: orden[o["archivo"]]):
        k = (o["concepto"], o["anio"])
        if k in serie and abs(serie[k]["valor_mm"] - o["valor_mm"]) > 1e-9:
            contrastes.append({"concepto": k[0], "anio": k[1], "antes": serie[k]["valor_mm"], "despues": o["valor_mm"], "archivos": [serie[k]["archivo"], o["archivo"]]})
        elif k in serie:
            contrastes.append({"concepto": k[0], "anio": k[1], "coincide": True, "archivos": [serie[k]["archivo"], o["archivo"]]})
        serie[k] = o
    s = lambda c, a: (serie.get((c, a)) or {}).get("valor_mm")  # noqa: E731
    # Historia del expediente (capex, D&A, pasivo por arrendamientos, principal de arrendamientos)
    from openpyxl import load_workbook
    wv = load_workbook(LIBRO, read_only=True, data_only=True)["Historia"]
    col = dict(zip(ANIOS, "HIJKL"))
    hist = {k: {a: wv[f"{col[a]}{f}"].value for a in ANIOS} for k, f in (("capex", 12), ("da", 8), ("adquisiciones", 13), ("pasivo_arrendamientos", 23),
                                                                         ("principal_arrendamientos", 17), ("reinversion_neta_total", 31), ("ventas", 6))}
    # conciliaciones anuales
    rec = []
    for a in ANIOS:
        ini_a, fin_a = s("activo_derechos_de_uso", a - 1), s("activo_derechos_de_uso", a)
        altas, dep, pag = s("altas_derechos_de_uso", a), s("amortizacion_derechos_de_uso", a), s("pagos_arrendamientos", a)
        if pag is None and a == 2023:
            pag = hist["principal_arrendamientos"][a]
        fila = {"anio": a, "altas": altas, "amortizacion_derechos_de_uso": dep, "pagos": pag, "capex_caja": hist["capex"][a], "da_total": hist["da"][a],
                "pasivo_final_historia": hist["pasivo_arrendamientos"][a], "pasivo_inicial_historia": hist["pasivo_arrendamientos"].get(a - 1)}
        if None not in (ini_a, fin_a, altas, dep):
            fila["activo"] = {"inicial": ini_a, "final": fin_a, "otros_residuo": round(fin_a - ini_a - altas + dep, 3)}
        if None not in (fila["pasivo_inicial_historia"], altas, pag):
            fila["pasivo"] = {"inicial": fila["pasivo_inicial_historia"], "final": fila["pasivo_final_historia"],
                              "otros_residuo": round(fila["pasivo_final_historia"] - fila["pasivo_inicial_historia"] - altas + pag, 3)}
        fila["capex_mas_altas"] = round(hist["capex"][a] + altas, 3) if altas is not None else None
        fila["da_sin_derechos_de_uso"] = round(hist["da"][a] - dep, 3) if dep is not None else None
        rec.append(fila)
    sum_ = lambda k: round(sum(f[k] for f in rec if f[k] is not None), 3)  # noqa: E731
    S_capex, S_da, S_altas, S_dep = sum_("capex_caja"), sum_("da_total"), sum_("altas"), sum_("amortizacion_derechos_de_uso")
    D_hist_caja = round(sum(hist["reinversion_neta_total"][a] for a in ANIOS), 3)
    S_adq = round(sum(hist["adquisiciones"][a] for a in ANIOS), 3)
    perimetros = {
        "caja (V6.4)": {"exceso_B60": round(S_capex - S_da, 3), "D_hist_B57": D_hist_caja, "F_hist_B62": round(S_capex - S_da + S_adq, 3),
                        "amortizacion_que_se_repone_B63": S_da, "coherencia": "infravalora la inversión que repone los arrendamientos: su amortización está en la D&A pero sus altas no están en el capex"},
        "NIIF 16 completo": {"exceso_B60": round(S_capex + S_altas - S_da, 3), "D_hist_B57": round(D_hist_caja + S_altas, 3), "F_hist_B62": round(S_capex + S_altas - S_da + S_adq, 3),
                             "amortizacion_que_se_repone_B63": S_da,
                             "coherencia": "coherente con el motor B: los arrendamientos son capital (Historia fila 32) y deuda (puente), el EBIT ya descuenta su amortización y los pagos no se restan del flujo; las altas son inversión financiada con deuda"},
        "solo activos propios": {"exceso_B60": round(S_capex - (S_da - S_dep), 3), "D_hist_B57": round(D_hist_caja + S_dep, 3), "F_hist_B62": round(S_capex - (S_da - S_dep) + S_adq, 3),
                                 "amortizacion_que_se_repone_B63": round(S_da - S_dep, 3),
                                 "coherencia": "no coherente sin reexpresar el NOPAT (EBIT antes de NIIF 16, con el pago como gasto), el capital invertido y el puente (sin el pasivo por arrendamientos): no se construye; restar la amortización de los derechos de uso de dos bases no basta"},
    }
    ventas = hist["ventas"]
    for p in perimetros.values():
        p["ventas_2021_2025"] = (ventas[2021], ventas[2025])
    out = {"naturaleza": "contraste selectivo y conciliación (solo lectura); ninguna cifra cambia el expediente", "fuentes_texto": TXT,
           "observaciones": obs, "errores": errores, "contrastes_entre_ediciones": contrastes,
           "serie": {f"{c}:{a}": v["valor_mm"] for (c, a), v in sorted(serie.items())}, "conciliacion_anual": rec,
           "sumas_2021_2025": {"capex_caja": S_capex, "da_total": S_da, "altas_derechos_de_uso": S_altas, "amortizacion_derechos_de_uso": S_dep, "adquisiciones": S_adq},
           "perimetros": perimetros,
           "dobles_computos": [
               "Flujo del motor B: NOPAT − reinversión (ΔV ÷ S2C) − requisito de P-M1; no resta pagos por arrendamientos. Puente: resta el pasivo por arrendamientos (Diagnóstico V6 C16). Sin doble cómputo: el pasivo cubre los contratos vigentes y la reposición futura (altas) es inversión.",
               "Restar además los pagos por arrendamientos del flujo del motor B sería un doble cómputo con el pasivo del puente.",
               "Historia fila 35 (FCF al accionista, motor A y DCF simplificado) resta el principal de arrendamientos: es otra vía (motor A), fuera del alcance de la 4.13."]}
    res = os.path.join(E413, "resultados")
    os.makedirs(res, exist_ok=True)
    json.dump(out, open(os.path.join(res, "conciliacion_arrendamientos_viscofan.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    g = lambda x, n=3: (f"{x:,.{n}f}".replace(",", " ").replace(".", ",").replace(" ", ".")) if isinstance(x, (int, float)) else "—"  # noqa: E731
    md = ["# Viscofan · contraste selectivo y conciliación de inversión, amortización y arrendamientos 2021–2025 (encargo 4.13 §6 y §7)", "",
          "**Qué es.** Cada cifra se toma de una línea cuya etiqueta dice el concepto, en la columna que fija la cabecera de su tabla (el año), con el signo publicado y la unidad (miles de euros → millones). Las altas se leen de su frase. Solo lee: ninguna cifra cambia el expediente.", "",
          f"**Errores de lectura:** {len(errores)}. **Contrastes entre ediciones:** {sum(1 for c in contrastes if c.get('coincide'))} coinciden, {sum(1 for c in contrastes if not c.get('coincide'))} difieren.", "",
          "## 1. Cifras leídas", "", "| Concepto | Año | Publicado | Signo | Millones | Archivo · línea · pág. PDF | Columna (cabecera) |", "|---|---|---|---|---|---|---|"]
    for o in obs:
        if "error" in o:
            md.append(f"| {o['concepto']} | — | ERROR | — | — | {o['archivo']} | {o['error']} |")
            continue
        cab = f"{o['columna']} (línea {o['cabecera']['linea']})" if o.get("cabecera") else "frase"
        md.append(f"| {o['concepto']} | {o['anio']} | {o['valor_publicado']} | {o['signo_publicado']}{'' if o['signo_esperado_ok'] else ' (¡inesperado!)'} | {g(o['valor_mm'])} | {o['archivo']} · {o['linea']} · {o['pagina_pdf']} | {cab} |")
    md += ["", "## 2. Conciliación anual (millones de euros)", "", "| Año | Capex de caja | Altas DdU | D&A total | Amort. DdU | Pagos | Activo DdU ini → fin (otros) | Pasivo ini → fin (otros) |", "|---|---|---|---|---|---|---|---|"]
    for f in rec:
        act = f.get("activo") or {}
        pas = f.get("pasivo") or {}
        md.append(f"| {f['anio']} | {g(f['capex_caja'])} | {g(f['altas'])} | {g(f['da_total'])} | {g(f['amortizacion_derechos_de_uso'])} | {g(f['pagos'])} | "
                  f"{g(act.get('inicial'))} → {g(act.get('final'))} ({g(act.get('otros_residuo'))}) | {g(pas.get('inicial'))} → {g(pas.get('final'))} ({g(pas.get('otros_residuo'))}) |")
    md += ["", "«Otros» es el residuo de la conciliación (diferencias de cambio, bajas, modificaciones y reclasificaciones que el estado de flujos no separa). En el pasivo, los pagos incluyen la parte de intereses que el informe no separa.", "",
           "## 3. Bases de P-M1 según el perímetro (2021–2025)", "", "| Perímetro | Exceso (B60) | D_hist (B57) | F_hist (B62) | Amortización que se repone (B63) | Coherencia con el motor B |", "|---|---|---|---|---|---|"]
    for k, p in perimetros.items():
        md.append(f"| {k} | {g(p['exceso_B60'])} | {g(p['D_hist_B57'])} | {g(p['F_hist_B62'])} | {g(p['amortizacion_que_se_repone_B63'])} | {p['coherencia']} |")
    md += ["", "## 4. Dobles cómputos", ""] + [f"- {x}" for x in out["dobles_computos"]]
    open(os.path.join(res, "conciliacion_arrendamientos_viscofan.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
    print("\n".join(md[-20:]))
    return 1 if errores else 0


if __name__ == "__main__":
    sys.exit(main())
