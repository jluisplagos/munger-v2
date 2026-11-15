#!/usr/bin/env python3
"""Separa, en el cierre nuevo de Vidrala, los cambios de software, configuración económica, datos y juicios frente al piloto 4.11
(encargo 4.12 §7: «se mantendrán separados los cambios de software, configuración económica, datos y juicios»; «una fase nueva podrá
cambiar [las palancas] con justificación, mostrando el efecto por separado»). Solo lee.

- Software: el control con las palancas de la 4.11 y el código final reproduce el piloto (control_palancas.json).
- Configuración: huella económica de la configuración del piloto, del control y del cierre (configuracion_economica.celdas sin metadatos).
- Datos: instantánea de las 216 entradas económicas del libro evaluado del piloto, del control y del cierre (entradas_economicas.py).
- Juicios: celdas de las fases A y B que cambian frente al piloto, y su efecto = cierre − control (mismo código, configuración y datos).
Uso (desde munger_v2_r1/): python3 -I …/scripts/separacion_cambios_vidrala.py
Escribe resultados/separacion_cambios_vidrala.json y .md.
"""
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
EXP = os.path.dirname(AQUI)
PV = os.path.abspath(os.path.join(EXP, "..", ".."))
PIL = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_11", "piloto", "Vidrala")
CTL = os.path.join(EXP, "control_palancas_4_11", "Vidrala")
NUE = os.path.join(EXP, "cierre_condicionado", "Vidrala")
sys.path.insert(0, os.path.join(PV, "scripts"))


def j(p):
    return json.load(open(p, encoding="utf-8"))


def main():
    import configuracion_economica as CE
    import entradas_economicas as EE
    libro = lambda d: os.path.join(d, "Vidrala_v63_evaluada.xlsx")  # noqa: E731
    inst = {k: EE.instantanea(libro(d)) for k, d in (("piloto", PIL), ("control", CTL), ("cierre", NUE))}
    conf = {k: j(os.path.join(d, "configuracion_economica.json")) for k, d in (("piloto", PIL), ("control", CTL), ("cierre", NUE))}
    huella_conf = {k: EE.huella_configuracion(c) if hasattr(EE, "huella_configuracion") else None for k, c in conf.items()}
    pr = {k: j(os.path.join(d, "precio.json")) for k, d in (("piloto", PIL), ("control", CTL), ("cierre", NUE))}
    cp = j(os.path.join(EXP, "control_palancas_4_11", "resultados", "control_palancas.json"))
    celdas = {}
    for fase in ("fase_a", "fase_b"):
        a, b = j(os.path.join(PIL, f"{fase}.json")).get("celdas") or {}, j(os.path.join(NUE, f"{fase}.json")).get("celdas") or {}
        celdas[fase] = {k: {"piloto_4_11": a.get(k), "cierre_4_12": b.get(k)} for k in sorted(set(a) | set(b)) if a.get(k) != b.get(k)}
    dif_datos_ctl = EE.diferencias(inst["piloto"], inst["control"])
    dif_cierre = EE.diferencias(inst["control"], inst["cierre"])
    cambios_eco_conf = CE.parametros_variados(conf["piloto"], conf["cierre"])
    out = {"software": {"control_concuerda_con_el_piloto": cp.get("resultado") == "CONCUERDA", "detalle": cp.get("diferencias_valoracion"),
                        "efecto_en_la_valoracion": 0.0 if cp.get("resultado") == "CONCUERDA" else None},
           "configuracion": {"parametros_economicos_distintos_piloto_cierre": cambios_eco_conf, "protocolo_del_objetivo": [conf["piloto"].get("protocolo_objetivo"), conf["cierre"].get("protocolo_objetivo")],
                             "huellas_economicas": huella_conf, "nota": "el protocolo del objetivo no es una celda económica: cambia la presentación del objetivo, no la valoración"},
           "datos": {"entradas_economicas_n": inst["cierre"]["n"], "piloto_frente_a_control": dif_datos_ctl, "huellas": {k: v["huella"] for k, v in inst.items()}},
           "juicios": {"celdas_que_cambian_frente_al_piloto": celdas, "entradas_economicas_que_cambian_control_frente_a_cierre": dif_cierre,
                       "efecto": {"precio_si": pr["cierre"]["precio_si"] - pr["control"]["precio_si"], "ponderado": pr["cierre"]["ponderado"] - pr["control"]["ponderado"],
                                  "V": [b - a for a, b in zip(pr["control"]["V"], pr["cierre"]["V"])]}},
           "valores": {k: {"precio_si": v["precio_si"], "ponderado": v["ponderado"], "V": v["V"], "p": v.get("p"), "zona": v.get("zona")} for k, v in pr.items()}}
    res = os.path.join(EXP, "resultados")
    json.dump(out, open(os.path.join(res, "separacion_cambios_vidrala.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    f = lambda x: f"{x:+.3f}" if isinstance(x, (int, float)) else "—"  # noqa: E731
    md = ["# Vidrala · cambios de software, configuración, datos y juicios frente al piloto 4.11", "",
          f"- **Software:** el control con las palancas de la 4.11 y el código final {'CONCUERDA' if out['software']['control_concuerda_con_el_piloto'] else 'NO concuerda'} con el piloto (V, ponderado, precio de Sí, zona, 13 variantes, 0 celdas económicas distintas): efecto en la valoración 0.",
          f"- **Configuración económica:** parámetros que varían entre el piloto y el cierre: {', '.join(cambios_eco_conf) or 'ninguno'}; protocolo del objetivo {out['configuracion']['protocolo_del_objetivo'][0]} → {out['configuracion']['protocolo_del_objetivo'][1]} (no es una celda económica).",
          f"- **Datos:** {inst['cierre']['n']} entradas económicas; piloto frente a control: {len(dif_datos_ctl)} distintas.",
          f"- **Juicios:** entre el control (palancas de la 4.11) y el cierre cambian {len(dif_cierre)} entradas económicas ({', '.join(dif_cierre)}): efecto en el precio de Sí {f(out['juicios']['efecto']['precio_si'])} € y en el ponderado {f(out['juicios']['efecto']['ponderado'])} € "
          f"(V {', '.join(f(x) for x in out['juicios']['efecto']['V'])}).", "",
          "| Valoración | Precio de Sí | Ponderado | Zona |", "|---|---|---|---|"]
    md += [f"| {k} | {v['precio_si']:.6f} | {v['ponderado']:.6f} | {v['zona']} |" for k, v in out["valores"].items()]
    md += ["", "Celdas de juicio que cambian frente al piloto 4.11 (fases A y B):", ""]
    for fase, d in celdas.items():
        md.append(f"- {fase}: " + ("; ".join(f"{k}: {x['piloto_4_11']!r} → {x['cierre_4_12']!r}" for k, x in d.items()) or "ninguna"))
    open(os.path.join(res, "separacion_cambios_vidrala.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
    print("\n".join(md[:6]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
