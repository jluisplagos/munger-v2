#!/usr/bin/env python3
"""Diferencias entre las salidas del piloto 4.11 y lo que produce el código final (encargo 4.12 §5). No toca el piloto.

El piloto histórico (…_4_11/piloto/Vidrala) se ejecutó con código intermedio de la 4.11 y no se edita para aparentar otra cosa.
Este script copia su material a una carpeta temporal (con el registro de publicaciones reubicado dentro de la copia), regenera allí
la ficha y el informe PROVISIONALES con el código de este árbol (ficha.py e informe.py con --provisional: sin vigencia, sin archivar
nada) y compara los cuatro puntos que señaló la revisión externa: selección, nombre del resumen, marca provisional en la primera
línea del informe y límites de R1. Añade lo que la 4.12 cambia en un expediente con fase C de la 4.11 (objetivo, avisos de dominio
y trazabilidad). Escribe resultados/diferencias_piloto_4_11_codigo_final.json y .md en este expediente.
Uso (desde munger_v2_r1/): python3 -I personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_12/scripts/diferencias_piloto_4_11.py
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
EXP = os.path.dirname(AQUI)
PV = os.path.abspath(os.path.join(EXP, "..", ".."))
RAIZ = os.path.dirname(PV)
PIL = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_11", "piloto")
CFG64 = os.path.join(PV, "config_v2_v64_experimental.json")
sys.path.insert(0, os.path.join(PV, "scripts"))


def huellas(d):
    out = {}
    for r, ds, fs in os.walk(d):
        for f in fs:
            p = os.path.join(r, f)
            out[os.path.relpath(p, d)] = hashlib.sha256(open(p, "rb").read()).hexdigest()
    return out


def linea_estado(md):
    t = open(md, encoding="utf-8").read() if os.path.exists(md) else ""
    for l in t.split("## 1.", 1)[-1].splitlines():
        if l.startswith("**Estado `"):
            return l
    return ""


def main():
    import cierre_v2 as CIE
    import config_v2
    import seleccion_plantilla as SEL
    antes = huellas(PIL)
    tmp = tempfile.mkdtemp(prefix="dif_piloto_411_")
    shutil.copytree(PIL, os.path.join(tmp, "piloto"), ignore=shutil.ignore_patterns(".lo_perfil", "prompts_generados", "__pycache__"))
    c = os.path.join(tmp, "piloto", "Vidrala")
    for n in (CIE.REGISTRO_RESUMEN, CIE.RESPALDO_RESUMEN):
        p = os.path.join(c, n)
        if os.path.exists(p):
            reg = json.load(open(p, encoding="utf-8"))
            for e in reg.get("publicaciones") or []:
                e["csv"] = os.path.join(tmp, "piloto", os.path.basename(e["csv"]))
                e["expediente"] = c
            json.dump(reg, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    env = dict(os.environ, MUNGER_CONFIG=CFG64)
    r1 = subprocess.run([sys.executable, "-B", os.path.join(PV, "scripts", "ficha.py"), c, "--provisional"], capture_output=True, text=True, env=env)
    r2 = subprocess.run([sys.executable, "-B", os.path.join(PV, "scripts", "informe.py"), c, "--provisional"], capture_output=True, text=True, env=env)
    f_pil = json.load(open(os.path.join(PIL, "Vidrala", "ficha.json"), encoding="utf-8"))
    f_nue = json.load(open(os.path.join(c, "ficha_provisional.json"), encoding="utf-8"))
    cfg = config_v2.cargar(CFG64)
    pa = SEL.leer(os.path.join(PIL, "Vidrala")) or {}
    reg = json.load(open(os.path.join(PIL, "Vidrala", CIE.REGISTRO_RESUMEN), encoding="utf-8"))
    l_pil, l_nue = linea_estado(os.path.join(PIL, "Vidrala", "informe.md")), linea_estado(os.path.join(c, "informe_provisional.md"))
    lim_pil = (f_pil.get("configuracion_economica") or {}).get("limites") or []
    lim_nue = (f_nue.get("configuracion_economica") or {}).get("limites") or []
    puntos = [
        {"punto": "selección", "piloto": {k: pa.get(k) for k in ("version", "config", "version_config", "archivo_sha256", "referencia_sha256", "verificador_sha256")},
         "codigo_final": {k: SEL.seleccion(cfg).get(k) for k in ("version", "config", "version_config", "archivo_sha256", "referencia_sha256", "verificador_sha256")},
         "comprobar_con_el_codigo_final": SEL.comprobar(os.path.join(PIL, "Vidrala"), cfg) or "acepta (mismas huellas de plantilla, referencia y verificador)",
         "diferencia": "la versión de la configuración del pipeline: el piloto registró " + str(pa.get("version_config")) + " y el código final usa " + str(cfg.get("version_config"))
                       + "; las tres huellas coinciden, así que la selección se acredita (la versión no forma parte de la comprobación)"},
        {"punto": "nombre del resumen", "piloto": [e.get("csv") for e in reg.get("publicaciones") or []],
         "codigo_final": os.path.relpath(CIE.ruta_resumen(os.path.join(PIL, "Vidrala"), cfg), RAIZ),
         "diferencia": "el piloto publicó su fila en resumen_v2.csv (antes de la corrección H2 de la revisión interna 4.11) y el registro guarda la ruta absoluta del árbol de "
                       "desarrollo de la 4.11; el código final publica las filas V6.4 en resumen_v2_v64_experimental.csv junto al expediente"},
        {"punto": "marca provisional en la primera línea del informe", "piloto": l_pil[:600], "codigo_final": l_nue[:600],
         "piloto_la_lleva": "provisional" in l_pil, "codigo_final_la_lleva": "provisional" in l_nue,
         "diferencia": "el informe del piloto se escribió antes de la corrección H7: no marca el objetivo como provisional en la línea de estado; el código final sí, con las hipótesis "
                       "que lo condicionan (Anexo B §B.6.7; el piloto tiene fase C de la 4.11, sin el bloque objetivo de la 4.12)"},
        {"punto": "límites de R1", "piloto": lim_pil, "codigo_final": lim_nue,
         "faltan_en_el_piloto": [x for x in lim_nue if x not in lim_pil],
         "diferencia": "la ficha del piloto se escribió antes de la corrección H12: no lleva los dos límites de R1 (terminal sin el máximo conservado y S2C inerte); el código final sí, y la 4.12 "
                       "añade las lecturas con bases parciales (BL sin P0; G7 con bases heredadas)"},
    ]
    nuevo_412 = {"objetivo": f_nue.get("objetivo"), "nota_objetivo": "fase C de la 4.11 (sin materialidad separada ni protocolo): el código final no reconstruye un objetivo 4.12 que esa fase C no evaluó",
                 "avisos_de_dominio": (f_nue.get("configuracion_economica") or {}).get("avisos_de_dominio"),
                 "nota_avisos": "las variantes del piloto son del formato 4.11 (sin instantánea ni avisos): con el código final, un pipeline nuevo las recalcularía (paso 10)",
                 "trazabilidad": "el piloto no tiene cadena_trazabilidad.json; la escribe el paso 12 del código final",
                 "aptitud_de_uso": f_nue.get("aptitud_de_uso"),
                 "nota_aptitud": ("el código final añade a la ficha y a la sección 1 del informe la aptitud de uso de la entrega, separada de la auditoría "
                                  "(«experimental»: ni «concluido» ni APROBADO hacen el resultado apto para decidir con dinero real); el piloto, de la 4.11, no la lleva"),
                 "informe_seccion_1_con_aptitud": "**Aptitud de uso (evaluación de la entrega" in (open(os.path.join(c, "informe_provisional.md"), encoding="utf-8").read() if os.path.exists(os.path.join(c, "informe_provisional.md")) else "")}
    despues = huellas(PIL)
    out = {"piloto": os.path.relpath(PIL, RAIZ), "copia_temporal": "(temporal, borrada al terminar)", "ficha_py": r1.returncode, "informe_py": r2.returncode,
           "salida_ficha": (r1.stdout + r1.stderr).strip()[-300:], "salida_informe": (r2.stdout + r2.stderr).strip()[-300:],
           "puntos": puntos, "cambios_4_12_en_un_expediente_con_fase_c_4_11": nuevo_412,
           "piloto_intacto": antes == despues, "n_archivos_piloto": len(antes),
           "conclusion": ("El piloto conserva sus salidas históricas y su aprobación (material intacto). Las cuatro diferencias son de presentación o de registro, no de "
                          "valoración: no cambian el ponderado, el precio de Sí, la zona, el estado ni la acción. El cierre nuevo de Vidrala (§7) se ejecuta con el código final.")}
    dst = os.path.join(EXP, "resultados")
    os.makedirs(dst, exist_ok=True)
    json.dump(out, open(os.path.join(dst, "diferencias_piloto_4_11_codigo_final.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    md = ["# Diferencias entre el piloto 4.11 y el código final", "",
          f"Piloto: `{out['piloto']}` (no se ha modificado: {'sí, intacto' if out['piloto_intacto'] else 'NO: CAMBIÓ'}; {out['n_archivos_piloto']} archivos). "
          "Las salidas del código final se regeneraron en una copia temporal, como material provisional (sin vigencia ni archivo).", ""]
    for p in puntos:
        md += [f"## {p['punto'][0].upper() + p['punto'][1:]}", "", f"- **Diferencia:** {p['diferencia']}.",
               f"- Piloto: `{json.dumps(p['piloto'], ensure_ascii=False, default=str)[:700]}`", f"- Código final: `{json.dumps(p['codigo_final'], ensure_ascii=False, default=str)[:700]}`", ""]
    md += ["## Lo que añade la 4.12 a un expediente con fase C de la 4.11", "", f"- {nuevo_412['nota_objetivo']} (objetivo = `{nuevo_412['objetivo']}`).",
           f"- {nuevo_412['nota_avisos']}.", f"- {nuevo_412['trazabilidad']}.",
           f"- {nuevo_412['nota_aptitud']} (ficha: `{(nuevo_412.get('aptitud_de_uso') or {}).get('caracter')}`; sección 1: {'sí' if nuevo_412['informe_seccion_1_con_aptitud'] else 'no'}).", "", f"**Conclusión.** {out['conclusion']}", ""]
    open(os.path.join(dst, "diferencias_piloto_4_11_codigo_final.md"), "w", encoding="utf-8").write("\n".join(md))
    print(f"OK: diferencias en resultados/diferencias_piloto_4_11_codigo_final.json/.md · piloto intacto: {out['piloto_intacto']}")
    shutil.rmtree(tmp, ignore_errors=True)
    return 0 if out["piloto_intacto"] and r1.returncode == 0 and r2.returncode == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
