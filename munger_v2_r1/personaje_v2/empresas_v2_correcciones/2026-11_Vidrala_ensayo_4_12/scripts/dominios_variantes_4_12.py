#!/usr/bin/env python3
"""Avisos de dominio de TODAS las variantes calculadas de los expedientes de la 4.12 (revisión interna R7). Solo lee.

El pipeline calcula los avisos de dominio (`dominios_v64.py`) sobre la variante «activa»; las demás variantes del rango no los llevan
en sus salidas. Este script los calcula, en lectura, sobre cada libro recalculado de `variantes_v64/recalc/` (con su `.resultados.json`)
y lista, por variante, los avisos activos y el factor f de la estructura. No cambia ningún expediente ni adopta umbrales.
Uso (desde munger_v2_r1/): python3 -I …/scripts/dominios_variantes_4_12.py
Escribe resultados/dominios_variantes_4_12.json y .md.
"""
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
EXP = os.path.dirname(AQUI)
PV = os.path.abspath(os.path.join(EXP, "..", ".."))
sys.path.insert(0, os.path.join(PV, "scripts"))
CASOS = {"Vidrala (cierre_condicionado)": os.path.join(EXP, "cierre_condicionado", "Vidrala"),
         "Viscofan (experimental)": os.path.join(EXP, "viscofan", "experimental", "Viscofan")}


def main():
    import dominios_v64 as DOM
    out = {}
    for nombre, c in CASOS.items():
        var = json.load(open(os.path.join(c, "configuracion_v64_variantes.json"), encoding="utf-8"))
        filas = []
        for v in var.get("variantes") or []:
            k = v.get("clave")
            libro = os.path.join(c, "variantes_v64", "recalc", f"{k}.xlsx")
            rj = os.path.join(c, "variantes_v64", f"{k}.resultados.json")
            if not (os.path.exists(libro) and os.path.exists(rj)):
                filas.append({"variante": k, "nota": "sin libro recalculado o sin resultados"})
                continue
            av = {a["id"]: a for a in DOM.avisos(libro, json.load(open(rj, encoding="utf-8")))}
            f = (av.get("factor_de_reestimacion") or {}).get("valores") or {}
            neg = av.get("inversion_fija_para_crecer_negativa") or {}
            nwc = (neg.get("valores") or {}).get("nwc_efectivo")
            # interpretación aplicada por una regla de este script (aviso activo sin NWC efectivo), no comprobada celda a celda (revisión de lo afectado, RA5)
            nota = ("interpretación, no comprobada celda a celda: negativos del MALO por la caída de las ventas con R0 (sin desglose del circulante: R0 libera capital al caer las ventas), "
                    "no por el dominio S2C·f > 1 ÷ NWC" if neg.get("activo") and not nwc else None)
            filas.append({"variante": k, "precio_si": v.get("precio_si"), "zona": v.get("zona"), "nota_aviso": nota,
                          "activos": [i for i, a in av.items() if a.get("activo") is True],
                          "f": f.get("f"), "estructura": f.get("estructura"), "f_fija": f.get("f_fija"),
                          "lambda_en_que_f_deja_de_estar_definida": f.get("lambda_en_que_f_deja_de_estar_definida")})
        out[nombre] = filas
    res = os.path.join(EXP, "resultados")
    json.dump(out, open(os.path.join(res, "dominios_variantes_4_12.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    g = lambda x, d=4: f"{x:.{d}f}" if isinstance(x, (int, float)) else "—"  # noqa: E731
    md = ["# Avisos de dominio de todas las variantes calculadas (revisión interna R7)", "",
          "**Qué es.** El pipeline calcula los avisos de dominio sobre la variante «activa». Aquí se calculan, en lectura, sobre cada libro recalculado de las variantes "
          "(`dominios_v64.py`, sin umbrales adoptados): avisos activos y factor de reestimación f de la estructura de cada variante. No cambia ningún expediente.",
          "Lectura: el extremo λ = 1,25 de Vidrala lleva f = 1,309 (la activa, 1,165); en Viscofan, θ = 1 lleva f = 1,160. En Vidrala, las dos variantes con R0 y sin P-M1 (solo_N1 y solo_N2, "
          "esta última el extremo superior del rango, 65,72 €) llevan activo el aviso de inversión fija para crecer negativa en el MALO. Los avisos son lecturas: no cambian ningún valor, "
          "y todas las variantes de las dos empresas siguen en «caro».", ""]
    for nombre, filas in out.items():
        md += [f"## {nombre}", "", "| Variante | Precio de Sí | Zona | Estructura | f | f_fija | Avisos activos | Nota |", "|---|---|---|---|---|---|---|---|"]
        for x in filas:
            if "nota" in x:
                md.append(f"| {x['variante']} | — | — | — | — | — | — | {x['nota']} |")
                continue
            md.append(f"| {x['variante']} | {g(x['precio_si'], 2)} | {x['zona']} | {x['estructura'] or '—'} | {g(x['f'])} | {g(x['f_fija'])} | {', '.join(x['activos']) or 'ninguno'} | {x.get('nota_aviso') or '—'} |")
        md.append("")
    open(os.path.join(res, "dominios_variantes_4_12.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
    print("\n".join(md))
    return 0


if __name__ == "__main__":
    sys.exit(main())
