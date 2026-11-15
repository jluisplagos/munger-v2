#!/usr/bin/env python3
"""Copia identificada del cierre nuevo de Vidrala con el OTRO protocolo experimental del objetivo (encargo 4.12 §7: «se compararán los
dos protocolos de objetivo en copias claramente identificadas; no se copiará una aprobación entre ellas»).

Copia el expediente CERRADO `cierre_condicionado/Vidrala` (protocolo «objetivo_condicionado») a `cierre_bloqueo/Vidrala`, sin el perfil de
LibreOffice, y en la copia:
  - reubica el registro de publicaciones del resumen (destino y expediente) dentro de `cierre_bloqueo/`: la copia nunca toca el
    resumen del original;
  - cambia SOLO `protocolo_objetivo` → «bloqueo_del_objetivo» en configuracion_economica.json (y lo anota en `naturaleza`) y el aviso de
    alcance_v2.json. Las celdas económicas no cambian: las variantes siguen siendo las mismas.
La aprobación copiada NO vale: el material cambia, así que la primera llamada del pipeline la retira (vigencia antes de todo, §3), y
después repite la fase C con un agente nuevo y pide una auditoría nueva. Nada se copia como aprobado.
Uso (desde munger_v2_r1/): python3 -I …/scripts/preparar_cierre_bloqueo.py
Escribe cierre_bloqueo/Vidrala y cierre_bloqueo/resultados/preparacion_copia.json y .md.
"""
import hashlib
import json
import os
import shutil
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
EXP = os.path.dirname(AQUI)
PV = os.path.abspath(os.path.join(EXP, "..", ".."))
RAIZ = os.path.dirname(PV)
ORI = os.path.join(EXP, "cierre_condicionado", "Vidrala")
ENS = os.path.join(EXP, "cierre_bloqueo")
DEST = os.path.join(ENS, "Vidrala")
sys.path.insert(0, os.path.join(PV, "scripts"))


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def main():
    import cierre_v2 as CIE
    if os.path.exists(DEST):
        print(f"ya existe {os.path.relpath(DEST, RAIZ)}: no se sobrescribe")
        return 1
    st = json.load(open(os.path.join(ORI, "estado_pipeline.json"), encoding="utf-8"))
    if os.path.exists(os.path.join(ORI, "ESPERANDO.md")) or st.get("paso") != 14:
        print(f"el expediente de origen no está cerrado (paso {st.get('paso')}): primero se termina")
        return 1
    huellas_origen = {}
    for r, ds, fs in os.walk(ORI):
        ds[:] = [d for d in ds if d != ".lo_perfil"]
        for f in fs:
            p = os.path.join(r, f)
            huellas_origen[os.path.relpath(p, ORI)] = sha(p)
    shutil.copytree(ORI, DEST, ignore=shutil.ignore_patterns(".lo_perfil", "__pycache__"))
    for n in (CIE.REGISTRO_RESUMEN, CIE.RESPALDO_RESUMEN):
        p = os.path.join(DEST, n)
        if os.path.exists(p):
            reg = json.load(open(p, encoding="utf-8"))
            for e in reg.get("publicaciones") or []:
                e["csv"] = os.path.join(ENS, os.path.basename(e["csv"]))
                e["expediente"] = DEST
            json.dump(reg, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    pc = os.path.join(DEST, "configuracion_economica.json")
    conf = json.load(open(pc, encoding="utf-8"))
    antes = conf.get("protocolo_objetivo")
    conf["protocolo_objetivo"] = "bloqueo_del_objetivo"
    conf["naturaleza"] = conf["naturaleza"] + (" (4.12, copia para comparar protocolos) En ESTA copia el protocolo experimental del objetivo es «bloqueo_del_objetivo»; "
                                               "la configuración económica es la misma que la de cierre_condicionado. Ninguno de los dos protocolos está adoptado.")
    json.dump(conf, open(pc, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    pa = os.path.join(DEST, "alcance_v2.json")
    al = json.load(open(pa, encoding="utf-8"))
    al["aviso"] = al["aviso"].replace("protocolo experimental del objetivo «objetivo_condicionado» (no adoptado)",
                                      "protocolo experimental del objetivo «bloqueo_del_objetivo» (no adoptado; copia para comparar con «objetivo_condicionado»)")
    json.dump(al, open(pa, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    os.makedirs(os.path.join(ENS, "resultados"), exist_ok=True)
    reg = {"origen": os.path.relpath(ORI, RAIZ), "destino": os.path.relpath(DEST, RAIZ), "archivos_copiados": len(huellas_origen),
           "huellas_origen": huellas_origen, "cambios": {"configuracion_economica.json": {"protocolo_objetivo": [antes, "bloqueo_del_objetivo"], "naturaleza": "nota añadida"},
                                                       "alcance_v2.json": {"aviso": "protocolo de la copia"},
                                                       CIE.REGISTRO_RESUMEN: "destino del resumen y expediente reubicados en cierre_bloqueo/"},
           "aprobacion": "la del origen va en la copia como antecedente y la retira la primera llamada del pipeline (material cambiado); no se copia como vigente"}
    json.dump(reg, open(os.path.join(ENS, "resultados", "preparacion_copia.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    md = ["# Vidrala · copia con el protocolo «bloqueo_del_objetivo» (encargo 4.12 §7)", "",
          f"- Origen cerrado `{reg['origen']}` ({len(huellas_origen)} archivos, sin el perfil de LibreOffice) → `{reg['destino']}`.",
          f"- Único cambio económico-normativo: `protocolo_objetivo` {antes} → bloqueo_del_objetivo (con una nota en `naturaleza`) y el aviso de `alcance_v2.json`. Las celdas económicas no cambian.",
          "- Registro de publicaciones del resumen reubicado en `cierre_bloqueo/`: la copia no toca el resumen del original.",
          f"- {reg['aprobacion']}."]
    open(os.path.join(ENS, "resultados", "preparacion_copia.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
    print("\n".join(md))
    return 0


if __name__ == "__main__":
    sys.exit(main())
