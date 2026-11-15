#!/usr/bin/env python3
"""Comparación homogénea entre el modo heredado y el experimental (encargo 4.12 §7 y §8), con las MISMAS entradas y palancas.

Lee `configuracion_v64_variantes.json` de un expediente V6.4 experimental: todas sus variantes se calcularon sobre copias del MISMO
libro evaluado (mismas entradas, mismas palancas de las fases A y B), cambiando solo la configuración. Descompone la diferencia entre
el heredado (V6.3 efectiva) y la configuración activa por componente: N1, N2 y R1 aislados, la activa sin P-M1 y la activa; muestra
las estructuras compatibles, los extremos del rango del parámetro y las convenciones, con el ámbito de cada lectura. No calcula
nada nuevo ni atribuye a P-M1 lo que es de N1, N2 o R1: los efectos aislados no son aditivos y se dan como tales.
Uso (desde munger_v2_r1/): python3 -I …/scripts/comparacion_homogenea.py CARPETA_EMPRESA
Escribe CARPETA_EMPRESA/../resultados/comparacion_homogenea.json y .md.
"""
import json
import os
import sys


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    c = os.path.abspath(sys.argv[1])
    v = json.load(open(os.path.join(c, "configuracion_v64_variantes.json"), encoding="utf-8"))
    pr = json.load(open(os.path.join(c, "precio.json"), encoding="utf-8"))
    filas = {x["clave"]: x for x in v["variantes"]}
    her, act = filas["heredado"], filas["activa"]

    def fila(k, lectura):
        x = filas.get(k)
        if not x:
            return None
        return {"clave": k, "lectura": lectura, "configuracion": x.get("resumen_configuracion"), "parametros_variados_frente_a_la_activa": x.get("parametros_variados"),
                "V": x.get("V"), "ponderado": x.get("ponderado"), "precio_si": x.get("precio_si"), "zona": x.get("zona"),
                "delta_ponderado_frente_a_heredado": x.get("delta_ponderado_frente_a_heredado"), "delta_precio_si_frente_a_heredado": x.get("delta_precio_si_frente_a_heredado"),
                "delta_ponderado_frente_a_activa": x.get("delta_ponderado_frente_a_activa"), "delta_precio_si_frente_a_activa": x.get("delta_precio_si_frente_a_activa")}
    componentes = [f for f in (fila("heredado", "V6.3 efectiva (modo heredado) sobre el mismo libro"), fila("solo_N1", "solo N1 (tipo normalizado), lo demás heredado"),
                               fila("solo_N2", "solo N2 (margen de partida), lo demás heredado"), fila("solo_R1", "solo R1 (reinversión con capacidad conservada), lo demás heredado"),
                               fila("activa_sin_PM1", "la activa sin P-M1 (N1, N2 y R1 juntos)"), fila("activa_solo_P0", "la activa sin requisito adicional, con P0"),
                               fila("activa", "configuración activa del expediente")) if f]
    otras = [fila(k, x.get("descripcion")) for k, x in filas.items() if k not in {f["clave"] for f in componentes}]
    d_total = (act["ponderado"] - her["ponderado"], act["precio_si"] - her["precio_si"])
    pm1 = (act["ponderado"] - filas["activa_sin_PM1"]["ponderado"], act["precio_si"] - filas["activa_sin_PM1"]["precio_si"]) if "activa_sin_PM1" in filas else None
    out = {"expediente": c, "precio": pr.get("precio"), "zona_activa": pr.get("zona"), "mismas_entradas": (v.get("entradas_economicas") or {}).get("huella"),
           "heredado": {"ponderado": her["ponderado"], "precio_si": her["precio_si"], "zona": her["zona"]},
           "activa": {"ponderado": act["ponderado"], "precio_si": act["precio_si"], "zona": act["zona"]},
           "diferencia_total": {"ponderado": d_total[0], "precio_si": d_total[1]},
           "efecto_de_PM1_y_P0_sobre_la_activa_sin_PM1": {"ponderado": pm1[0], "precio_si": pm1[1]} if pm1 else None,
           "componentes": componentes, "otras_variantes": otras, "zonas_calculadas": v.get("zonas_calculadas"),
           "nota": ("Todas las variantes usan las mismas entradas y las mismas palancas (copias del libro evaluado; huella de las entradas económicas en `mismas_entradas`). "
                    "Los efectos aislados no son aditivos (interactúan); el rango de esta tabla no es un intervalo de confianza ni cubre hipótesis no exploradas.")}
    res = os.path.join(os.path.dirname(c), "resultados")
    os.makedirs(res, exist_ok=True)
    json.dump(out, open(os.path.join(res, "comparacion_homogenea.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    f2 = lambda x: f"{x:.2f}" if isinstance(x, (int, float)) else "—"  # noqa: E731
    md = ["# Comparación homogénea · heredado frente a experimental (mismas entradas y palancas)", "",
          f"Precio {pr.get('precio')} · zona activa {pr.get('zona')} · huella de las entradas económicas `{str(out['mismas_entradas'])[:16]}…`.", "",
          f"- **Heredado (V6.3 efectiva):** ponderado {f2(her['ponderado'])} · precio de Sí {f2(her['precio_si'])} · zona {her['zona']}.",
          f"- **Activa:** ponderado {f2(act['ponderado'])} · precio de Sí {f2(act['precio_si'])} · zona {act['zona']}.",
          f"- **Diferencia total (activa − heredado):** ponderado {f2(d_total[0])} · precio de Sí {f2(d_total[1])}."
          + (f" De ella, P-M1 (con la cartera) frente a la activa sin P-M1: ponderado {f2(pm1[0])} · precio de Sí {f2(pm1[1])}; el resto es de N1, N2 y R1 juntos." if pm1 else ""), "",
          "| Variante | Lectura | Ponderado | Precio de Sí | Zona | Δ pond. vs heredado | Δ Sí vs heredado | Δ Sí vs activa |", "|---|---|---|---|---|---|---|---|"]
    for f in componentes + otras:
        md.append(f"| {f['clave']} | {f['lectura']} | {f2(f['ponderado'])} | {f2(f['precio_si'])} | {f['zona']} | {f2(f['delta_ponderado_frente_a_heredado'])} | "
                  f"{f2(f['delta_precio_si_frente_a_heredado'])} | {f2(f['delta_precio_si_frente_a_activa'])} |")
    md += ["", out["nota"]]
    open(os.path.join(res, "comparacion_homogenea.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
    print(f"OK: heredado {f2(her['precio_si'])} → activa {f2(act['precio_si'])} (precio de Sí) · {len(componentes) + len(otras)} variantes → resultados/comparacion_homogenea.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
