#!/usr/bin/env python3
"""Prepara el expediente experimental NUEVO de Viscofan (encargo 4.12 §8). No toca el origen ni sobrescribe nada.

La base económica no cambia (cuentas de 2025), así que no se usa cambiar_base.py (que reconstruye fase1_v63.json desde los textos de la
fase 1, y esos textos no están en el paquete): se hace como dice la guía de la V6.4 para un expediente nuevo con la misma base —
carpeta nueva con solo las entradas de partida— y, además:
  - texto/: las publicaciones recuperadas, con su nombre propio (una edición distinta no lleva el nombre de la fuente de la fase 1);
  - fecha de análisis = fecha REAL de ejecución (en las copias de fase1_v63.json y fase1_metadatos.json; el resto de entradas, igual);
  - configuracion_economica.json: la configuración propia (viscofan/configuracion/configuracion_economica_viscofan_experimental.json);
  - alcance_v2.json con el aviso del ensayo;
  - antecedentes/: copia del extracto V6.3 del origen, para que la extracción lo reutilice y contraste (no es una entrada del pipeline).
Fechas separadas: base económica, ejecución, precio, acciones, tasa sin riesgo y consulta de las fuentes.
Uso (desde munger_v2_r1/): python3 -I …/scripts/preparar_viscofan_experimental.py
Escribe viscofan/experimental/Viscofan, viscofan/experimental/antecedentes y viscofan/experimental/resultados/preparacion.json/.md.
"""
import datetime as dt
import hashlib
import json
import os
import shutil
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
EXP = os.path.dirname(AQUI)
PV = os.path.abspath(os.path.join(EXP, "..", ".."))
RAIZ = os.path.dirname(PV)
ORIG = os.path.join(PV, "empresas_v2", "Viscofan")
ENS = os.path.join(EXP, "viscofan", "experimental")
DEST = os.path.join(ENS, "Viscofan")
FUENTES = os.path.join(EXP, "viscofan", "fuentes")
CONF = os.path.join(EXP, "viscofan", "configuracion", "configuracion_economica_viscofan_experimental.json")
ENTRADAS = ["etapa1", "fase1_v63.json", "fase1_metadatos.json", "fase1_fuentes.json", "fase1_partes", "fase1_listas.md"]
TEXTOS = ["AR_2025.txt", "CF_2024.txt", "CA_2023_es.txt", "CF_2022_compilacion.txt", "CF_2021.txt", "AR_2020.txt", "AR_2019.txt", "IA_2018_es.txt",
          "AR_2017.txt", "IA_2016_es.txt", "IA_2021_es.txt", "IA_2023_es.txt"]
sys.path.insert(0, os.path.join(PV, "scripts"))


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def huellas(base):
    out = {}
    for r, ds, fs in os.walk(base):
        for f in sorted(fs):
            p = os.path.join(r, f)
            out[os.path.relpath(p, base)] = sha(p)
    return out


def main():
    import configuracion_economica as CE
    if os.path.exists(DEST):
        print(f"ya existe {os.path.relpath(DEST, RAIZ)}: no se sobrescribe")
        return 1
    conf = json.load(open(CONF, encoding="utf-8"))
    faltas = CE.validar(conf)
    if faltas:
        print("configuración no válida: " + " | ".join(faltas))
        return 1
    hoy = dt.date.today().isoformat()
    os.makedirs(os.path.join(DEST, "texto"))
    copiadas = {}
    for n in ENTRADAS:
        o = os.path.join(ORIG, n)
        if os.path.isdir(o):
            shutil.copytree(o, os.path.join(DEST, n))
            copiadas[n] = huellas(o)
        else:
            shutil.copy2(o, os.path.join(DEST, n))
            copiadas[n] = sha(o)
    cambios = {}
    for n in ("fase1_v63.json", "fase1_metadatos.json"):
        p = os.path.join(DEST, n)
        d = json.load(open(p, encoding="utf-8"))
        cambios[n] = {"fecha_analisis": {"origen": d.get("fecha_analisis"), "expediente": hoy}}
        d["fecha_analisis"] = hoy
        json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    inv = json.load(open(os.path.join(FUENTES, "inventario_fuentes_viscofan.json"), encoding="utf-8"))
    por_texto = {os.path.basename(r["texto_con_marcas_de_pagina"]): r for r in inv["recuperadas"]}
    textos = []
    for t in TEXTOS:
        shutil.copy2(os.path.join(FUENTES, "texto", t), os.path.join(DEST, "texto", t))
        r = por_texto[t]
        textos.append({"texto": f"texto/{t}", "texto_sha256": sha(os.path.join(DEST, "texto", t)), "pdf": os.path.relpath(os.path.join(RAIZ, r["archivo"]), RAIZ), "pdf_sha256": r["sha256"],
                       "ejercicio": r["ejercicio"], "identificacion": r["identificacion"], "edicion_frente_a_la_fase_1": r.get("edicion")})
    json.dump(conf, open(os.path.join(DEST, "configuracion_economica.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    meta = json.load(open(os.path.join(ORIG, "fase1_metadatos.json"), encoding="utf-8"))
    alcance = {"tipo": "ensayo_exploratorio",
               "aviso": ("ENSAYO 4.12 · VISCOFAN CON LA PLANTILLA V6.4 EXPERIMENTAL (solo cubre el motor B; la fase A elige el motor) Y UNA CONFIGURACIÓN PROPIA NO ADOPTADA: "
                         "N1 sin las activaciones de bases imponibles negativas (22,12 %), N2 vacío por elección (regla heredada, margen de 2025), R1 (circulante 48,28 % de las ventas), "
                         "P-M1 SR1 · Θ con θ = 0,5 (punto medio del dominio, sin central económica) y extremos θ = 0 y θ = 1, cartera legado; protocolo experimental del objetivo "
                         "«objetivo_condicionado» (no adoptado); r heredada y k = 3 experimental. Cuentas de 2025 con el precio del 3-nov-2026: no es una valoración a cierre de 2025 "
                         "ni un backtest. Fecha de análisis = fecha real de ejecución."),
               "fuente": "2026-11_Vidrala_ensayo_4_12/viscofan/configuracion/configuracion_economica_viscofan_experimental.json; encargo 4.12 §8. Metadato de la orquestación.",
               "fecha": hoy}
    json.dump(alcance, open(os.path.join(DEST, "alcance_v2.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    ant = os.path.join(ENS, "antecedentes")
    os.makedirs(ant, exist_ok=True)
    shutil.copy2(os.path.join(ORIG, "extracto_v63.md"), os.path.join(ant, "extracto_v63_origen.md"))
    fechas = {"base_economica": "2025-12-31 (cuentas consolidadas de 2025)", "ejecucion": hoy,
              "precio": f"{meta['precio']['valor']} € del {meta['precio']['fecha']} ({meta['precio']['fuente']})",
              "acciones": f"{meta['acciones_diluidas']['valor']} millones, media ponderada diluida de 2025 ({meta['acciones_diluidas']['fecha']})",
              "tasa_sin_riesgo": f"{meta['tasa_sin_riesgo']['valor']} ({meta['tasa_sin_riesgo']['fuente']})",
              "fuentes": "publicaciones recuperadas el 2026-11-12 (copias de la carpeta de la persona responsable, en dos entregas: 20:38 y 21:59); el informe anual 2025 es un PDF creado el 25-mar-2026",
              "fecha_analisis_del_origen": cambios["fase1_v63.json"]["fecha_analisis"]["origen"]}
    reg = {"origen": os.path.relpath(ORIG, RAIZ), "destino": os.path.relpath(DEST, RAIZ), "entradas_copiadas_sin_cambios": copiadas, "campos_cambiados": cambios,
           "textos": textos, "configuracion": {"archivo": os.path.relpath(CONF, RAIZ), "sha256": sha(CONF), "resumen": CE.resumen(conf)},
           "alcance_sha256": sha(os.path.join(DEST, "alcance_v2.json")), "antecedentes": {"extracto_v63_origen.md": sha(os.path.join(ant, "extracto_v63_origen.md"))},
           "fechas": fechas,
           "no_se_copia": "libros V6.3, estado del pipeline, fases A–C, auditoría, ficha, informe y resumen del origen (el pipeline los genera de nuevo con agentes reales)"}
    os.makedirs(os.path.join(ENS, "resultados"), exist_ok=True)
    json.dump(reg, open(os.path.join(ENS, "resultados", "preparacion.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    md = ["# Viscofan · preparación del expediente experimental (encargo 4.12 §8)", "",
          f"- Origen `{reg['origen']}` (sin cambios) → `{reg['destino']}`. Entradas de partida copiadas: {', '.join(ENTRADAS)}.",
          f"- Único campo cambiado en las copias: `fecha_analisis` {cambios['fase1_v63.json']['fecha_analisis']['origen']} → {hoy} (fecha real de ejecución) en fase1_v63.json y fase1_metadatos.json.",
          f"- texto/: {len(textos)} publicaciones recuperadas con su nombre propio: " + "; ".join(f"`{x['texto']}` ({x['ejercicio']}, SHA-256 `{x['texto_sha256'][:12]}…`)" for x in textos) + ".",
          f"- Configuración: `{reg['configuracion']['archivo']}` (SHA-256 `{reg['configuracion']['sha256'][:16]}…`): {reg['configuracion']['resumen']}.",
          "- Antecedentes (no son entradas del pipeline): `antecedentes/extracto_v63_origen.md`, para que la extracción lo reutilice y contraste.",
          f"- No se copia: {reg['no_se_copia']}.", "", "**Fechas, por separado:**", ""] + [f"- {k.replace('_', ' ')}: {v}" for k, v in fechas.items()]
    open(os.path.join(ENS, "resultados", "preparacion.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
    print("\n".join(md))
    return 0


if __name__ == "__main__":
    sys.exit(main())
