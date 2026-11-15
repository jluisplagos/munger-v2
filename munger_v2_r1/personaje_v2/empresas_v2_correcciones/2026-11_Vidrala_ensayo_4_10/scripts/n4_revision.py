#!/usr/bin/env python3
"""Revisión de N4 (entrega 4.10, encargo §4.1 y §4.2). Solo lectura de la 4.9; escribe en ../n4/.

Uso: python3 -I n4_revision.py [--salida DIR]   (desde cualquier carpeta; por defecto escribe en ../n4/)

Parte de la matriz de la 4.9 (…_4_9/n4/matriz_n4.json, que no se modifica) y añade, para cada una de las 38 entradas:
  - «evidencia»: completa · parcial (clase 2 global con un componente sin acreditar) · depende_de_la_definicion · no_aplicable;
  - para «otros_activos_financieros», la DEFINICIÓN EXPLÍCITA con la que se clasifica y lo que excluye, y los derivados
    corrientes de cada año (líneas del cuadre del activo corriente que ya leyó la 4.9) como alternativa de la lectura amplia;
  - la situación de REGISTRO (campos humanos vacíos: la IA no confirma ceros) separada de la evidencia;
  - la dependencia: Historia C5:L26 para las 28 entradas con fila; ninguna para las 10 auxiliares mientras no entren en caja.
No hay una cuota objetivo de «respaldados»: los recuentos salen de la clasificación revisada.
"""
import argparse
import csv
import hashlib
import json
import os
import re

AQUI = os.path.dirname(os.path.abspath(__file__))
EXP = os.path.dirname(AQUI)
M49 = os.path.join(EXP, "..", "2026-11_Vidrala_ensayo_4_9", "n4", "matriz_n4.json")
OUT = os.path.join(EXP, "n4")

DEF_OAF = {
    "especificacion_vigente": "prompts/historia_anio.md: «activos financieros corrientes que no son caja (depósitos a plazo, inversiones financieras temporales)»; "
                              "prompts/metadatos_fase1.md: caja_incluye_otros_activos_financieros = true «solo si la empresa mantiene una parte material de su "
                              "liquidez en depósitos a plazo u otras inversiones financieras corrientes líquidas».",
    "lectura_estrecha_propuesta": {
        "incluye": ["depósitos a plazo y otros depósitos bancarios no clasificados como equivalentes de efectivo",
                    "inversiones financieras temporales líquidas (renta fija a corto, fondos monetarios, pagarés) no incluidas en «efectivo y equivalentes»"],
        "excluye": ["instrumentos financieros derivados (de cobertura o no): su valor razonable no es liquidez del accionista, revierte con la partida "
                    "cubierta y tiene contrapartida en pasivos derivados y en la reserva de coberturas",
                    "deudores comerciales y otras cuentas a cobrar (activos financieros del circulante operativo)",
                    "activos por impuestos y administraciones públicas", "otros activos corrientes operativos",
                    "activos financieros NO corrientes (p. ej., «Otros activos financieros» no corrientes)"],
        "razon_economica": "la partida es una ampliación posible de la CAJA (convención caja_incluye_otros_activos_financieros): solo tiene sentido para "
                           "activos que son liquidez disponible, no para coberturas ni para el circulante operativo",
    },
    "lectura_amplia_literal": "«activos financieros corrientes que no son caja»: incluiría los derivados corrientes (y, en sentido estricto de la NIIF 9, "
                              "también los deudores comerciales, lo que muestra que no es la intención de la especificación)",
    "convencion_de_la_referencia": "fase1_metadatos.json: caja_incluye_otros_activos_financieros = false: la partida no entra en la caja ni en la valoración",
}


def importes(linea):
    """Importes de una línea del cuadre: el primero es el del año; «-» es cero."""
    t = re.sub(r"^\D*?\s(\d{1,2})\s", " ", " " + linea + " ", count=1)  # quita la referencia de nota («8», «9»)
    nums = re.findall(r"(?<![\d.,])(-|\d{1,3}(?:[.,]\d{3})*)(?![\d.,])", t)
    out = []
    for n in nums:
        out.append(0.0 if n == "-" else float(n.replace(".", "").replace(",", "")) / 1000)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--salida", default=OUT)
    out = ap.parse_args().salida
    m = json.load(open(M49, encoding="utf-8"))
    filas = []
    for e in m["matriz"]:
        p, a, cl = e["partida"], e["anio"], e["clasificacion"]
        r = {"id": e["id"], "partida": p, "anio": a, "celda": e.get("celda"), "clase_4_9": cl, "valor_actual": e.get("valor_actual"),
             "dependencia": ("Historia C5:L26 (fila con dependencias en la valoración y los diagnósticos)" if e.get("celda") else
                             "ninguna mientras caja_incluye_otros_activos_financieros = false (partida auxiliar sin fila)"),
             "registro": {"decision": None, "fecha": None, "confirmado_por": None,
                          "nota": "campos humanos vacíos: la IA no confirma ceros; una firma no sustituye un dato que falta"}}
        if p == "intereses_financiacion" and a >= 2018:
            r.update(evidencia="parcial", componente_sin_acreditar="intereses de arrendamientos (NIIF 16 desde 2019; arrendamiento financiero NIC 17 en 2018): "
                     "la línea del estado de flujos en que se pagan no se publica (clase 3 en ese componente)",
                     componente_acreditado="intereses de deuda: pagados en explotación («Pagos de intereses»), así que no hay intereses de deuda en financiación")
        elif p == "otros_activos_financieros":
            lin = [l for l in e["comprobaciones"]["cuadre_activo_corriente"]["lineas"] if re.search(r"(?i)deriv", l)]
            der = importes(lin[0])[0] if lin else 0.0
            otras = [l for l in e["comprobaciones"]["cuadre_activo_corriente"]["lineas"] if re.search(r"(?i)deposit|invest|temporar|short-term financ|inversiones financ", l)]
            r.update(definicion_aplicada="lectura estrecha propuesta (ver «definicion»)", lineas_de_liquidez_no_caja=otras,
                     derivados_corrientes_mm=der, linea_derivados=lin[0] if lin else None,
                     valor_lectura_estrecha=0.0 if not otras else None, valor_lectura_amplia=der if not otras else None)
            if otras:
                r.update(evidencia="discrepante_o_insuficiente", motivo="hay una línea de liquidez no caja en el activo corriente")
            elif der == 0:
                r.update(evidencia="completa", motivo="cuadre completo sin depósitos ni inversiones temporales y sin derivados corrientes: cero con las dos lecturas")
            else:
                r.update(evidencia="depende_de_la_definicion",
                         motivo=f"cuadre completo sin depósitos ni inversiones temporales (cero con la lectura estrecha); con la lectura amplia, los derivados "
                                f"corrientes ({der:.3f} mm) no son cero")
        elif cl == 4:
            r.update(evidencia="no_aplicable", motivo=("no es un cero publicado: NIIF 16 no estaba en vigor" + (
                "; en 2018 depende además de la regla registrada que lleva el arrendamiento financiero NIC 17 a deuda («Arrendamientos = solo pasivos NIIF 16»), "
                "escrita en fase1_decisiones.json sin fecha ni firma (no se atribuye a una persona)" if a == 2018 else "")))
        elif cl == 2:
            r.update(evidencia="completa", motivo="cuadre completo y contrastes de la 4.9 sin reserva")
        else:
            r.update(evidencia="discrepante_o_insuficiente", motivo=f"clase {cl} en la 4.9")
        filas.append(r)
    os.makedirs(out, exist_ok=True)
    rec = {}
    for r in filas:
        rec.setdefault(r["evidencia"], {}).setdefault(r["partida"], []).append(r["anio"])
    resumen = {k: {"n": sum(len(v) for v in d.values()), "por_partida": d} for k, d in rec.items()}
    res = {"generado_por": "scripts/n4_revision.py (4.10)", "base_4_9": os.path.relpath(M49, EXP), "base_4_9_sha256": hashlib.sha256(open(M49, "rb").read()).hexdigest(),
           "definicion": {"otros_activos_financieros": DEF_OAF}, "recuento": resumen, "total": len(filas),
           "nota_dependencia": "las 28 entradas con fila alimentan Historia C5:L26; las 10 auxiliares (otros_activos_financieros) quedan fuera mientras no entren en caja",
           "matriz": filas}
    json.dump(res, open(os.path.join(out, "matriz_n4_4_10.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    with open(os.path.join(out, "matriz_n4_4_10.csv"), "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["id", "partida", "anio", "clase_4_9", "evidencia", "derivados_corrientes_mm", "motivo_o_componente", "registro_humano"])
        for r in filas:
            w.writerow([r["id"], r["partida"], r["anio"], r["clase_4_9"], r["evidencia"], r.get("derivados_corrientes_mm", ""),
                        r.get("motivo") or r.get("componente_sin_acreditar", ""), "vacío"])
    for k, v in sorted(resumen.items()):
        print(f"{k:28s} {v['n']:2d} · " + " · ".join(f"{p} {len(a)} ({min(a)}–{max(a)})" for p, a in v["por_partida"].items()))
    print(f"total {len(filas)}")


if __name__ == "__main__":
    main()
