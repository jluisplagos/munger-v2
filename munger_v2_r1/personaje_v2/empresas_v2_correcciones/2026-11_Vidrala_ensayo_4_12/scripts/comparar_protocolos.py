#!/usr/bin/env python3
"""Compara los dos protocolos experimentales del objetivo sobre el MISMO material económico de Vidrala (encargo 4.12 §7). Solo lee.

`cierre_condicionado/Vidrala` (protocolo «objetivo_condicionado») y `cierre_bloqueo/Vidrala` (copia con «bloqueo_del_objetivo»): comprueba
que el material económico es el mismo (celdas de la configuración, entradas económicas de las variantes, precio.json y variantes) y que
las aprobaciones son distintas (solicitud, material y auditoría), y pone lado a lado lo que publica cada uno: estado, cubo, acción,
objetivo (tratamiento, valor calculado condicional, precio objetivo emitido, provisional), hipótesis que lo condicionan, rango y la
fila del resumen V6.4. No interpreta: la lectura va en COMPARACION_PROTOCOLOS_4_12.md.
Uso (desde munger_v2_r1/): python3 -I …/scripts/comparar_protocolos.py
Escribe resultados/comparacion_protocolos.json y .md.
"""
import csv
import hashlib
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
EXP = os.path.dirname(AQUI)
PV = os.path.abspath(os.path.join(EXP, "..", ".."))
CASOS = {"objetivo_condicionado": os.path.join(EXP, "cierre_condicionado", "Vidrala"), "bloqueo_del_objetivo": os.path.join(EXP, "cierre_bloqueo", "Vidrala")}
sys.path.insert(0, os.path.join(PV, "scripts"))


def j(p):
    try:
        return json.load(open(p, encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest() if os.path.exists(p) else None


def fila_resumen(c):
    p = os.path.join(os.path.dirname(c), "resumen_v2_v64_experimental.csv")
    if not os.path.exists(p):
        return None
    filas = [r for r in csv.DictReader(open(p, encoding="utf-8")) if (r.get("empresa") or "").lower().startswith("vidrala")]
    return filas[-1] if filas else None


def main():
    import configuracion_economica as CE
    out = {"casos": {}}
    for prot, c in CASOS.items():
        st, fi, conf = j(os.path.join(c, "estado_pipeline.json")), j(os.path.join(c, "ficha.json")), j(os.path.join(c, "configuracion_economica.json"))
        ob, dec = fi.get("objetivo") or {}, fi.get("decision") or {}
        sol, mat = j(os.path.join(c, "solicitud_auditoria.json")), j(os.path.join(c, "material_auditoria.json"))
        out["casos"][prot] = {"expediente": os.path.relpath(c, EXP), "protocolo_declarado": conf.get("protocolo_objetivo"), "estado": st.get("estado_analisis"),
                              "auditoria": st.get("auditoria"), "cubo": fi.get("cubo"), "accion": dec.get("accion"), "precio_objetivo_decision": dec.get("precio_objetivo"),
                              "tratamiento": ob.get("tratamiento"), "estado_del_objetivo": ob.get("estado_del_objetivo"), "origen_del_bloqueo": ob.get("origen_del_bloqueo"),
                              "valor_calculado_condicional": ob.get("valor_calculado_condicional"), "precio_objetivo_emitido": ob.get("precio_objetivo_emitido"),
                              "provisional": ob.get("provisional"), "hipotesis_que_lo_condicionan": [h.get("hipotesis") for h in ob.get("hipotesis_que_lo_condicionan") or []],
                              "rango_precio_si": (ob.get("rango_calculado") or {}).get("precio_si"), "fila_resumen": fila_resumen(c),
                              "solicitud": sol.get("id") or sol.get("solicitud"), "material": mat.get("id") or mat.get("huella"), "auditoria_sha256": sha(os.path.join(c, "auditoria.md")),
                              "historial_cierres": sorted(os.listdir(os.path.join(c, "historial_cierres"))) if os.path.isdir(os.path.join(c, "historial_cierres")) else [],
                              "celdas_configuracion": CE.celdas(conf) if conf else None, "precio_json_sha256": sha(os.path.join(c, "precio.json")),
                              "variantes_huella_entradas": (j(os.path.join(c, "configuracion_v64_variantes.json")).get("entradas_economicas") or {}).get("huella")}
    a, b = out["casos"]["objetivo_condicionado"], out["casos"]["bloqueo_del_objetivo"]
    out["mismo_material_economico"] = {"celdas_de_la_configuracion": a["celdas_configuracion"] == b["celdas_configuracion"], "precio_json": a["precio_json_sha256"] == b["precio_json_sha256"],
                                      "entradas_de_las_variantes": a["variantes_huella_entradas"] == b["variantes_huella_entradas"]}
    out["aprobaciones_distintas"] = {"solicitud": a["solicitud"] != b["solicitud"], "auditoria": a["auditoria_sha256"] != b["auditoria_sha256"],
                                    "la_copia_retiro_la_aprobacion_heredada": bool(b["historial_cierres"])}
    for x in out["casos"].values():
        x.pop("celdas_configuracion", None)
    res = os.path.join(EXP, "resultados")
    json.dump(out, open(os.path.join(res, "comparacion_protocolos.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    campos = ["protocolo_declarado", "estado", "auditoria", "cubo", "accion", "precio_objetivo_decision", "tratamiento", "estado_del_objetivo", "origen_del_bloqueo",
              "valor_calculado_condicional", "precio_objetivo_emitido", "provisional", "hipotesis_que_lo_condicionan", "rango_precio_si", "solicitud", "historial_cierres"]
    md = ["# Vidrala · los dos protocolos del objetivo sobre el mismo material económico", "",
          "Mismo material económico: " + ", ".join(f"{k} {'sí' if v else 'NO'}" for k, v in out["mismo_material_economico"].items()) + ".",
          "Aprobaciones distintas: " + ", ".join(f"{k} {'sí' if v else 'NO'}" for k, v in out["aprobaciones_distintas"].items()) + ".", "",
          "| Campo | objetivo_condicionado | bloqueo_del_objetivo |", "|---|---|---|"]
    md += [f"| {k} | {a.get(k)} | {b.get(k)} |" for k in campos]
    md += ["", "Fila del resumen V6.4 (columnas del objetivo):", ""]
    for prot, x in out["casos"].items():
        fr = x.get("fila_resumen") or {}
        md.append(f"- {prot}: " + " · ".join(f"{k} = {fr.get(k)}" for k in ("estado", "cubo", "accion", "precio_objetivo", "protocolo_objetivo", "estado_del_objetivo",
                                                                          "valor_calculado_condicional", "precio_objetivo_emitido", "objetivo_provisional") if k in fr))
    open(os.path.join(res, "comparacion_protocolos.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
    print("\n".join(md[:4]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
