#!/usr/bin/env python3
"""Preparación reproducible del ensayo de Vidrala con base económica 2025 (entrega 4.10.1, encargo §4 y §5).

Uso (desde munger_v2_r1/): python3 -I personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_10_1/scripts/preparar_ensayo_2025.py
Crea, a partir de una COPIA del expediente de la 4.6.1 (que no se modifica):
  - Vidrala/ (expediente activo) solo con las entradas de partida: etapa1/, texto/, fase1_partes/ (extracciones AR originales, con sus
    bytes), fase1_decisiones.json y fase1_fuentes.json (sin cambios), más el texto español de 2025 como fuente adicional;
  - antecedentes/heredados_4_6_1/ con TODO lo demás (extractos, fases, celdas, libros, resultados, precio.json, gramática, referencias,
    material y solicitudes de auditoría, auditorías, salidas oficiales, historial de cierres, registros de publicaciones, estado del
    pipeline, prompts y metadatos anteriores), con su inventario y huellas: el ensayo no hereda ningún cierre ni fase;
  - fase1_metadatos.json y fase1_v63.json ACTIVOS generados desde ../configuracion/configuracion_ensayo_2025.json (no se parchea el
    Excel): fase1_historia.py construir reconstruye fase1_v63.json con los metadatos nuevos y, después, se aplican las entradas del
    caso principal que la configuración declara (precisión de control de C46/C47 y supuesto heredado C48 = 0 / C49 = 4,5);
  - alcance_v2.json del ensayo. No escribe estado_pipeline.json: el pipeline lo crea propio al empezar.
Los destinos del resumen y el registro de publicaciones del ensayo quedan en esta carpeta del ensayo (aislados)."""
import hashlib
import json
import os
import shutil
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
ENS = os.path.dirname(AQUI)
PV = os.path.abspath(os.path.join(ENS, "..", ".."))
REF = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_6_1", "Vidrala")
ACT = os.path.join(ENS, "Vidrala")
ANT = os.path.join(ENS, "antecedentes", "heredados_4_6_1")
CONF = json.load(open(os.path.join(ENS, "configuracion", "configuracion_ensayo_2025.json"), encoding="utf-8"))
CONSERVAR = {"etapa1", "texto", "fase1_partes", "fase1_decisiones.json", "fase1_fuentes.json"}


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def texto_con_marcas(pdf, txt):
    """pdftotext -layout página a página, con las marcas «[PDF PAGE n]» que usan los textos del expediente y los prompts."""
    tmp = txt + ".tmp"
    subprocess.run(["pdftotext", "-layout", pdf, tmp], check=True)
    paginas = open(tmp, encoding="utf-8", errors="replace").read().split("\f")
    if paginas and not paginas[-1].strip():
        paginas = paginas[:-1]
    open(txt, "w", encoding="utf-8").write("".join(f"[PDF PAGE {i}]\n{p.rstrip()}\n\n" for i, p in enumerate(paginas, 1)))
    os.remove(tmp)


def main():
    if os.path.exists(ACT) or os.path.exists(ANT):
        print("ya existe el expediente activo o los antecedentes: no se rehace (borrar a mano para regenerar)")
        return 2
    os.makedirs(ANT)
    shutil.copytree(REF, ACT, ignore=shutil.ignore_patterns(".lo_perfil", "__pycache__"))
    inv = []
    for n in sorted(os.listdir(ACT)):
        if n in CONSERVAR:
            continue
        shutil.move(os.path.join(ACT, n), os.path.join(ANT, n))
    for r, ds, fs in os.walk(ANT):
        for f in fs:
            p = os.path.join(r, f)
            inv.append({"archivo": os.path.relpath(p, ANT), "sha256": sha(p)})
    json.dump({"origen": os.path.relpath(REF, PV), "nota": "Productos del expediente de la 4.6.1 que no corresponden a las entradas del ensayo 2025. "
               "Se conservan como antecedentes, sin cambios; ninguno está en una ruta activa del ensayo.", "archivos": inv},
              open(os.path.join(ENS, "antecedentes", "INVENTARIO_HEREDADOS_4_6_1.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    # fuente adicional: el texto de la versión española de 2025 (prioridad documental), con su procedencia
    es = CONF["fuentes"]["es_2025"]
    pdf = os.path.join(PV, "..", es["archivo"])
    txt = os.path.join(ACT, "texto", "ES_2025_informacion_financiera_consolidada.txt")
    texto_con_marcas(pdf, txt)
    # metadatos activos: los de la 4.6.1 con las entradas de la configuración (precio, acciones, capitalización, rf y fecha de ejecución)
    meta = json.load(open(os.path.join(ANT, "fase1_metadatos.json"), encoding="utf-8"))
    e = CONF["entradas"]
    meta["fecha_analisis"] = CONF["fechas"]["ejecucion"]
    meta["precio"] = {"valor": e["precio"]["valor"], "moneda_cotizacion": "EUR", "fecha": e["precio"]["fecha"], "fx": None, "fx_fecha": None, "fuente": e["precio"]["fuente"]}
    meta["acciones_diluidas"] = {"valor": e["N_millones"]["valor"], "fecha": e["N_millones"]["fecha"], "fuente": e["N_millones"]["fuente"], "pagina": e["N_millones"]["pagina"]}
    meta["capitalizacion"] = {"valor": e["E_capitalizacion"]["valor"], "fecha": e["E_capitalizacion"]["fecha"], "fuente": e["E_capitalizacion"]["fuente"]}
    meta["tasa_sin_riesgo"] = {"valor": e["tasa_sin_riesgo"]["valor"], "fuente": e["tasa_sin_riesgo"]["fuente"]}
    meta.setdefault("_notas", [])
    meta["_notas"] = [n for n in meta["_notas"] if "Bolsamanía" not in n] + [CONF["nota_metadatos"]]
    json.dump(meta, open(os.path.join(ACT, "fase1_metadatos.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    r = subprocess.run([sys.executable, "-B", os.path.join(PV, "scripts", "fase1_historia.py"), "construir", ACT], capture_output=True, text=True)
    print((r.stdout + r.stderr).strip()[-600:])
    if r.returncode != 0:
        return 1
    f1p = os.path.join(ACT, "fase1_v63.json")
    f1 = json.load(open(f1p, encoding="utf-8"))
    sustituidas = {}
    for celda, v in CONF["caso_principal_analisis"].items():
        antes = (f1.get("analisis", {}).get(celda) or {}).get("valor")
        f1.setdefault("analisis", {})[celda] = {"valor": v["valor"], "fuente": v["fuente"], "pagina": None, "periodo": v.get("periodo"), "unidad": "mm"}
        sustituidas[celda] = {"construido_por_fase1_historia": antes, "caso_principal": v["valor"]}
    f1.setdefault("_notas", []).append("(4.10.1) Caso principal del ensayo 2025: " + "; ".join(f"{c} {x['construido_por_fase1_historia']} → {x['caso_principal']}" for c, x in sustituidas.items())
                                       + " (configuracion_ensayo_2025.json → caso_principal_analisis). C49 = 4,5 es un supuesto heredado, no un principal acreditado (P3 abierto).")
    json.dump(f1, open(f1p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(CONF["alcance"], open(os.path.join(ACT, "alcance_v2.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump({"sustituidas_en_fase1_v63": sustituidas, "heredados_movidos": len(inv), "conservados": sorted(CONSERVAR),
               "fuente_adicional": os.path.relpath(txt, ENS), "fuente_adicional_sha256": sha(txt)},
              open(os.path.join(ENS, "resultados", "preparacion_salida.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"expediente activo preparado · {len(inv)} archivos heredados en antecedentes · sustituidas en fase1_v63.json: {sustituidas}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
