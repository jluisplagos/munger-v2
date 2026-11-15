#!/usr/bin/env python3
"""Comparación de los expedientes regenerados en la 4.13 con los de la 4.12 (encargo 4.13 §9: «se mantendrán separadas la reproducción
histórica y cualquier alternativa con entradas corregidas»). Solo lee.

Para cada par (Vidrala condicionado, Vidrala bloqueo, Viscofan), separa:
  - reproducción numérica: V, ponderado, precio de Sí y zona de la activa; para Viscofan, además, la variante «perímetro Caja» de la
    V6.4.1 frente a la activa de la 4.12 (debe coincidir exactamente: es la misma valoración con la V6.4.1);
  - cambio de configuración: solo el perímetro (Viscofan);
  - (revisión interna de la 4.13) en Viscofan las fases A y B se rehicieron con agentes reales: la reproducción histórica se hace con las
    variantes de la primera ejecución de la 4.13 (las palancas de la 4.12; `viscofan/antecedentes/ejecucion_1_4_13/`), y el cambio total
    de la activa se separa en el efecto de las palancas nuevas (con «Caja») y el del perímetro (con las palancas nuevas);
  - cambios de juicio de la fase C: estado, acción, tratamiento, hipótesis que condicionan el objetivo, estructura más coherente y, por
    parámetro, fundamento suficiente, materialidad para la acción y el objetivo y la base (4.13);
  - ámbito: número de variantes y rango del precio de Sí.
Uso (desde munger_v2_r1/): python3 -I …/scripts/comparar_4_12_4_13.py · Escribe resultados/comparacion_4_12_4_13.json y .md.
"""
import json
import os

AQUI = os.path.dirname(os.path.abspath(__file__))
E413 = os.path.dirname(AQUI)
PV = os.path.abspath(os.path.join(E413, "..", ".."))
E412 = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_12")
PARES = {"Vidrala · objetivo_condicionado": (os.path.join(E412, "cierre_condicionado", "Vidrala"), os.path.join(E413, "vidrala_condicionado", "Vidrala")),
         "Vidrala · bloqueo_del_objetivo": (os.path.join(E412, "cierre_bloqueo", "Vidrala"), os.path.join(E413, "vidrala_bloqueo", "Vidrala")),
         "Viscofan": (os.path.join(E412, "viscofan", "experimental", "Viscofan"), os.path.join(E413, "viscofan", "Viscofan"))}


def j(c, n):
    p = os.path.join(c, n)
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}


def resumen(c):
    st, pr, fc, f, var = j(c, "estado_pipeline.json"), j(c, "precio.json"), j(c, "fase_c.json"), j(c, "ficha.json"), j(c, "configuracion_v64_variantes.json")
    cv = fc.get("configuracion_v64") or {}
    ob = f.get("objetivo") or {}
    vs = [v for v in var.get("variantes") or [] if v.get("clave") != "activa" and v.get("zona")]
    ps = [v["precio_si"] for v in vs] + [pr.get("precio_si")]
    return {"estado": st.get("estado_analisis"), "auditoria": st.get("auditoria"), "accion": (f.get("decision") or {}).get("accion"),
            "precio_objetivo": (f.get("decision") or {}).get("precio_objetivo"), "tratamiento": ob.get("tratamiento"),
            "V": pr.get("V"), "ponderado": pr.get("ponderado"), "precio_si": pr.get("precio_si"), "zona": pr.get("zona"),
            "n_variantes": len(vs), "rango_precio_si": [min(ps), max(ps)], "formato_variantes": var.get("formato"),
            "condicionan": (cv.get("objetivo") or {}).get("hipotesis_que_condicionan"),
            "estructura_mas_coherente": (cv.get("mantenimiento") or {}).get("estructura_mas_coherente"),
            "parametros": {p["clave"]: {k: p.get(k) for k in ("fundamento_suficiente", "material_para_accion", "material_para_objetivo", "clase", "confianza",
                                                               "cobertura", "base_de_la_materialidad")} for p in cv.get("parametros") or []},
            "variantes": {v["clave"]: v for v in var.get("variantes") or []}}


def main():
    out = {}
    for nombre, (a, b) in PARES.items():
        x, y = resumen(a), resumen(b)
        cambios = {}
        for k in sorted(set(x["parametros"]) | set(y["parametros"])):
            pa, pb = x["parametros"].get(k) or {}, y["parametros"].get(k) or {}
            d = {c: [pa.get(c), pb.get(c)] for c in ("fundamento_suficiente", "material_para_accion", "material_para_objetivo", "clase", "confianza") if pa.get(c) != pb.get(c)}
            d["base_4_13"] = pb.get("base_de_la_materialidad")
            d["cobertura_4_13"] = pb.get("cobertura")
            cambios[k] = d
        rep = desc = None
        if "perimetro_alternativo" in y["variantes"]:
            ant = os.path.join(os.path.dirname(b), "antecedentes", "ejecucion_1_4_13", "configuracion_v64_variantes.json")
            v1 = {v["clave"]: v for v in (json.load(open(ant, encoding="utf-8")).get("variantes") or [])} if os.path.exists(ant) else {}
            pa = v1.get("perimetro_alternativo") or {}
            rep = {"fuente": os.path.relpath(ant, E413) if v1 else None, "precio_si_4_12": x["precio_si"], "precio_si_caja_4_13": pa.get("precio_si"),
                   "ponderado_4_12": x["ponderado"], "ponderado_caja_4_13": pa.get("ponderado"), "V_4_12": x["V"], "V_caja_4_13": pa.get("V"),
                   "identicos": bool(pa) and x["V"] == pa.get("V") and x["ponderado"] == pa.get("ponderado") and x["precio_si"] == pa.get("precio_si")}
            caja_nueva = y["variantes"]["perimetro_alternativo"]["precio_si"]
            desc = {"activa_4_12_caja_palancas_4_12": x["precio_si"], "caja_palancas_nuevas": caja_nueva, "activa_4_13_niif16_palancas_nuevas": y["precio_si"],
                    "efecto_palancas_nuevas": caja_nueva - x["precio_si"], "efecto_perimetro": y["precio_si"] - caja_nueva, "total": y["precio_si"] - x["precio_si"]}
        for r in (x, y):
            r.pop("variantes")
        out[nombre] = {"4.12": x, "4.13": y, "cambios_por_parametro": cambios, "reproduccion_con_caja": rep, "descomposicion": desc,
                       "misma_valoracion_activa": x["V"] == y["V"] and x["ponderado"] == y["ponderado"] and x["precio_si"] == y["precio_si"]}
    json.dump(out, open(os.path.join(E413, "resultados", "comparacion_4_12_4_13.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    g = lambda v, n=2: f"{v:.{n}f}".replace(".", ",") if isinstance(v, float) else ("—" if v is None else str(v))  # noqa: E731
    md = ["# Expedientes de la 4.13 frente a los de la 4.12", "",
          "**Qué es.** Comparación de solo lectura que separa la reproducción numérica, el cambio de configuración (solo el perímetro, en Viscofan) y los cambios de juicio de "
          "las fases C nuevas (agentes reales con el contrato de cobertura de la 4.13). Los expedientes de la 4.12 se conservan como control histórico.", ""]
    for nombre, r in out.items():
        x, y = r["4.12"], r["4.13"]
        md += [f"## {nombre}", "", "| | 4.12 | 4.13 |", "|---|---|---|"]
        for k, lab in (("estado", "Estado"), ("auditoria", "Auditoría"), ("accion", "Acción"), ("precio_objetivo", "Precio objetivo emitido"), ("tratamiento", "Tratamiento del objetivo"),
                       ("precio_si", "Precio de Sí (activa)"), ("ponderado", "Ponderado (activa)"), ("zona", "Zona"), ("n_variantes", "Variantes calculadas (sin la activa)"),
                       ("formato_variantes", "Formato de las variantes"), ("estructura_mas_coherente", "Estructura más coherente según la fase C")):
            md.append(f"| {lab} | {g(x[k], 3)} | {g(y[k], 3)} |")
        md.append(f"| Rango del precio de Sí | {g(x['rango_precio_si'][0])}–{g(x['rango_precio_si'][1])} | {g(y['rango_precio_si'][0])}–{g(y['rango_precio_si'][1])} |")
        md.append(f"| Hipótesis que condicionan el objetivo | {', '.join(x['condicionan'] or []) or '—'} | {', '.join(y['condicionan'] or []) or '—'} |")
        md += ["", f"- Misma valoración de la activa: **{'sí' if r['misma_valoracion_activa'] else 'no'}**."]
        if r["reproduccion_con_caja"]:
            rc = r["reproduccion_con_caja"]
            md.append(f"- Reproducción histórica (primera ejecución de la 4.13, con las palancas de la 4.12): la variante «perímetro Caja» de la V6.4.1 da "
                      f"{g(rc['precio_si_caja_4_13'], 10)} frente a {g(rc['precio_si_4_12'], 10)} de la 4.12 (V y ponderado {'idénticos' if rc['identicos'] else 'DISTINTOS'}).")
            d = r["descomposicion"]
            md.append(f"- Cambio de la activa, {g(d['total'], 4)} € de precio de Sí, separado: fases A y B nuevas (con «Caja») {g(d['efecto_palancas_nuevas'], 4)} € "
                      f"({g(d['activa_4_12_caja_palancas_4_12'], 4)} → {g(d['caja_palancas_nuevas'], 4)}); perímetro NIIF 16 (con las palancas nuevas) {g(d['efecto_perimetro'], 4)} € "
                      f"({g(d['caja_palancas_nuevas'], 4)} → {g(d['activa_4_13_niif16_palancas_nuevas'], 4)}).")
        md += ["", "Cambios de juicio por parámetro (4.12 → 4.13) y base de la materialidad para la acción en la 4.13:", ""]
        for k, d in r["cambios_por_parametro"].items():
            cam = "; ".join(f"{c} {v[0]} → {v[1]}" for c, v in d.items() if c not in ("base_4_13", "cobertura_4_13")) or "sin cambios en las banderas"
            md.append(f"- {k}: {cam} · cobertura {d['cobertura_4_13']} · base {d['base_4_13']}")
        md.append("")
    md += ["**Lectura (interpretación).** En Vidrala la valoración no cambia; cambian el ámbito (más contrastes aislados y avisos de dominio de todas las variantes) y los "
           "juicios de la fase C, que ya no eligen una estructura de mantenimiento. En Viscofan, con las palancas de la 4.12, la variante «Caja» reproduce exactamente la 4.12; "
           "la activa final cambia por dos causas separadas: las fases A y B rehechas tras la revisión interna (palancas del MALO, S2C anclado en el perímetro NIIF 16 y "
           "probabilidades) y el perímetro. Ningún cambio altera la zona ni la acción."]
    open(os.path.join(E413, "resultados", "comparacion_4_12_4_13.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main()
