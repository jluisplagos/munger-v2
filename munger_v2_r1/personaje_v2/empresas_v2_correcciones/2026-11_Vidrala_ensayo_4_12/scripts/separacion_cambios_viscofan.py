#!/usr/bin/env python3
"""Separa, en el expediente experimental de Viscofan, los cambios de mecánica, configuración económica, datos y juicios frente al
expediente heredado (encargo 4.12 §8: «se explicarán cambios de datos, juicios y mecánica por separado»). Solo lee.

- Mecánica: la reproducción del heredado con el código final, en V6.3 y en V6.4 heredado, coincide con el origen (reproduccion_heredado.json).
- Datos: instantánea de las 216 entradas económicas (entradas_economicas.py) del libro evaluado de la reproducción en V6.4 heredado
  (mismas entradas y palancas que el origen) frente al del expediente nuevo, separando las celdas de «Configuración V6.4» (configuración),
  las de Palancas y Análisis que escriben las fases (juicio) y las demás (datos).
- Juicios: celdas de las fases A y B que cambian frente al origen, y su efecto = variante «heredado» del expediente nuevo (mismas
  palancas nuevas, modo heredado) − reproducción del heredado (palancas del origen, mismo código).
- Configuración: efecto = activa − variante «heredado» del expediente nuevo (mismas entradas y palancas), con los componentes aislados.
Uso (desde munger_v2_r1/): python3 -I …/scripts/separacion_cambios_viscofan.py
Escribe viscofan/resultados/separacion_cambios_viscofan.json y .md.
"""
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
EXP = os.path.dirname(AQUI)
PV = os.path.abspath(os.path.join(EXP, "..", ".."))
ORIG = os.path.join(PV, "empresas_v2", "Viscofan")
REP = os.path.join(EXP, "viscofan", "reproduccion_v64_heredado", "Viscofan")
NUE = os.path.join(EXP, "viscofan", "experimental", "Viscofan")
RES = os.path.join(EXP, "viscofan", "resultados")
sys.path.insert(0, os.path.join(PV, "scripts"))


def j(p):
    return json.load(open(p, encoding="utf-8"))


def clase(celda):
    if celda.startswith("Configuración V6.4!"):
        return "configuracion"
    hoja = celda.split("!")[0] if "!" in celda else ""
    if hoja in ("Palancas", "Análisis"):
        return "juicio"
    return "datos"


def main():
    import entradas_economicas as EE
    libro = lambda d: os.path.join(d, "Viscofan_v63_evaluada.xlsx")  # noqa: E731
    i_rep, i_nue = EE.instantanea(libro(REP)), EE.instantanea(libro(NUE))
    dif = EE.diferencias(i_rep, i_nue)
    por_clase = {}
    for c in dif:
        por_clase.setdefault(clase(c), []).append(c)
    rp = j(os.path.join(RES, "reproduccion_heredado.json"))
    pr_rep, pr_nue = j(os.path.join(REP, "precio.json")), j(os.path.join(NUE, "precio.json"))
    var = {v["clave"]: v for v in j(os.path.join(NUE, "configuracion_v64_variantes.json")).get("variantes") or []}
    her = var.get("heredado") or {}
    celdas = {}
    for fase in ("fase_a", "fase_b"):
        a, b = j(os.path.join(ORIG, f"{fase}.json")).get("celdas") or {}, j(os.path.join(NUE, f"{fase}.json")).get("celdas") or {}
        celdas[fase] = {k: {"heredado": a.get(k), "experimental_4_12": b.get(k)} for k in sorted(set(a) | set(b)) if a.get(k) != b.get(k)}
    fa_o, fa_n = j(os.path.join(ORIG, "fase_a.json")), j(os.path.join(NUE, "fase_a.json"))
    efecto_juicio = {"precio_si": her.get("precio_si") - pr_rep["precio_si"], "ponderado": her.get("ponderado") - pr_rep["ponderado"]}
    efecto_conf = {"precio_si": pr_nue["precio_si"] - her.get("precio_si"), "ponderado": pr_nue["ponderado"] - her.get("ponderado")}
    componentes = {k: {"precio_si": (var.get(k) or {}).get("precio_si"), "delta_precio_si_vs_heredado": ((var.get(k) or {}).get("precio_si") or 0) - her.get("precio_si")}
                   for k in ("solo_N1", "solo_R1", "activa_sin_PM1", "activa") if k in var}
    out = {"mecanica": {"reproduccion_del_heredado": rp.get("resultado"), "efecto_en_la_valoracion": 0.0 if rp.get("resultado") == "COINCIDE" else None},
           "motor": {"heredado": fa_o.get("celdas", {}).get("C62"), "experimental_4_12": fa_n.get("celdas", {}).get("C62"),
                     "nota": "los dos expedientes valoran con el motor B; la fase A nueva lo eligió por los hechos (C62)"},
           "entradas_economicas": {"n": i_nue["n"], "distintas": dif, "por_clase": por_clase,
                                   "huellas": {"reproduccion_heredado": i_rep["huella"], "experimental_4_12": i_nue["huella"]}},
           "juicios": {"celdas_que_cambian_frente_al_heredado": celdas, "efecto": efecto_juicio},
           "configuracion": {"efecto": efecto_conf, "componentes_aislados": componentes, "nota": "los efectos aislados no son aditivos"},
           "valores": {"heredado_origen": {k: pr_rep.get(k) for k in ("precio_si", "ponderado", "V", "p", "zona")},
                       "variante_heredado_4_12": {k: her.get(k) for k in ("precio_si", "ponderado", "V", "zona")},
                       "activa_4_12": {k: pr_nue.get(k) for k in ("precio_si", "ponderado", "V", "p", "zona")}}}
    json.dump(out, open(os.path.join(RES, "separacion_cambios_viscofan.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    f = lambda x: f"{x:+.3f}" if isinstance(x, (int, float)) else "—"  # noqa: E731
    md = ["# Viscofan · cambios de mecánica, configuración, datos y juicios frente al expediente heredado", "",
          "**Qué es.** La separación que pide el encargo 4.12 §8. Solo lee. «Heredado» es el expediente de origen (`personaje_v2/empresas_v2/Viscofan`, V6.3), "
          "reproducido con el código final; «experimental 4.12» es el expediente nuevo con agentes reales.", "",
          f"- **Mecánica:** la reproducción del heredado con el código final {'COINCIDE' if rp.get('resultado') == 'COINCIDE' else 'NO coincide'} con el origen en V6.3 y en V6.4 heredado "
          f"(|Δ| = 0): efecto en la valoración 0.",
          f"- **Motor:** heredado `{out['motor']['heredado']}` → 4.12 `{out['motor']['experimental_4_12']}`; los dos valoran con el motor B.",
          f"- **Entradas económicas** ({i_nue['n']}; reproducción del heredado frente al expediente nuevo): {len(dif)} distintas — "
          + "; ".join(f"{k}: {', '.join(v)}" for k, v in por_clase.items()) + ".",
          f"- **Juicios:** efecto en el precio de Sí {f(efecto_juicio['precio_si'])} € y en el ponderado {f(efecto_juicio['ponderado'])} € "
          "(variante «heredado» del expediente nuevo, con sus palancas, frente a la reproducción del heredado, con las del origen).",
          f"- **Configuración económica:** efecto en el precio de Sí {f(efecto_conf['precio_si'])} € y en el ponderado {f(efecto_conf['ponderado'])} € (activa frente a la variante «heredado»). "
          "Componentes aislados frente al heredado: " + "; ".join(f"{k} {f(v['delta_precio_si_vs_heredado'])} €" for k, v in componentes.items()) + " (no aditivos).", "",
          "| Valoración | Precio de Sí | Ponderado | V MALO / NORMAL / BUENO | Zona |", "|---|---|---|---|---|"]
    for k, v in out["valores"].items():
        md.append(f"| {k} | {v.get('precio_si'):.6f} | {v.get('ponderado'):.6f} | " + " / ".join(f"{x:.4f}" for x in v.get("V") or []) + f" | {v.get('zona')} |")
    md += ["", "Celdas de juicio que cambian frente al heredado (fases A y B; texto recortado):", ""]
    for fase, d in celdas.items():
        md.append(f"- {fase}: " + ("; ".join(f"{k}: {str(x['heredado'])[:90]!r} → {str(x['experimental_4_12'])[:90]!r}" for k, x in d.items()) or "ninguna"))
    open(os.path.join(RES, "separacion_cambios_viscofan.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
    print("\n".join(md[:9]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
