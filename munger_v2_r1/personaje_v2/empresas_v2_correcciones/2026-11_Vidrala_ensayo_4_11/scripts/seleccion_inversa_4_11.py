#!/usr/bin/env python3
"""Ejecución 1 del §5 de la revisión interna (H1): selección inversa sobre una COPIA de un expediente V6.3 cerrado.
Copia el expediente cerrado de la 4.10.1 (…/2026-11_Vidrala_ensayo_4_10_1/Vidrala, que no se toca) a un temporal, le añade una
configuracion_economica.json válida (la del piloto 4.11) y lanza el pipeline con config_v2_v64_experimental.json. Registra el código de
salida, los archivos escritos o cambiados y el estado. Esperado tras la corrección de H1: código 2 y ningún archivo nuevo ni cambiado.
Escribe …/2026-11_Vidrala_ensayo_4_11/resultados/seleccion_inversa_4_11.json y .md.
Uso (desde munger_v2_r1/): python3 -I …/2026-11_Vidrala_ensayo_4_11/scripts/seleccion_inversa_4_11.py
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
ENS = os.path.dirname(AQUI)
RAIZ = os.path.abspath(os.path.join(ENS, "..", "..", ".."))
PV = os.path.join(RAIZ, "personaje_v2")
ORIGEN = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_10_1", "Vidrala")


def huellas(c):
    out = {}
    for r, ds, fs in os.walk(c):
        for f in fs:
            p = os.path.join(r, f)
            out[os.path.relpath(p, c)] = (hashlib.sha256(open(p, "rb").read()).hexdigest(), os.path.getmtime(p))
    return out


def main():
    tmp = tempfile.mkdtemp(prefix="seleccion_inversa_4_11_")
    c = os.path.join(tmp, "Vidrala")
    shutil.copytree(ORIGEN, c, symlinks=True)
    shutil.copy(os.path.join(ENS, "piloto", "Vidrala", "configuracion_economica.json"), os.path.join(c, "configuracion_economica.json"))
    st0 = json.load(open(os.path.join(c, "estado_pipeline.json"), encoding="utf-8"))
    antes = huellas(c)
    r = subprocess.run([sys.executable, os.path.join(PV, "scripts", "pipeline.py"), c, "--config", os.path.join(PV, "config_v2_v64_experimental.json")],
                       capture_output=True, text=True, timeout=600)
    despues = huellas(c)
    nuevos = sorted(set(despues) - set(antes))
    cambiados = sorted(k for k in set(antes) & set(despues) if antes[k] != despues[k])
    st1 = json.load(open(os.path.join(c, "estado_pipeline.json"), encoding="utf-8"))
    ok = r.returncode == 2 and not nuevos and not cambiados and "se preparó con la V6.3" in (r.stdout + r.stderr)
    out = {"origen": os.path.relpath(ORIGEN, RAIZ), "estado_del_origen": {k: st0.get(k) for k in ("paso", "estado_analisis", "auditoria")},
           "codigo_de_salida": r.returncode, "ultima_linea": (r.stdout + r.stderr).strip().splitlines()[-1] if (r.stdout + r.stderr).strip() else "",
           "archivos_nuevos": nuevos, "archivos_cambiados": cambiados, "estado_despues": {k: st1.get(k) for k in ("paso", "estado_analisis", "auditoria")},
           "plantilla_activa_escrita": os.path.exists(os.path.join(c, "plantilla_activa.json")), "resultado": "CONFORME" if ok else "NO CONFORME",
           "nota": "Copia en un temporal; el expediente de la 4.10.1 no se toca. La única entrada añadida a la copia es configuracion_economica.json (la del piloto)."}
    json.dump(out, open(os.path.join(ENS, "resultados", "seleccion_inversa_4_11.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    md = ["# Selección inversa sobre una copia de un expediente V6.3 cerrado (revisión interna H1, §5.1)", "",
          f"- Origen (no se toca): `{out['origen']}`, estado {out['estado_del_origen']}.",
          "- A la copia se le añade una `configuracion_economica.json` válida (la del piloto) y se lanza el pipeline con `config_v2_v64_experimental.json`.",
          f"- Código de salida: **{r.returncode}** (esperado tras la corrección: 2).",
          f"- Última línea: «{out['ultima_linea'][:400]}»",
          f"- Archivos nuevos: {len(nuevos)} {nuevos[:5]} · archivos cambiados: {len(cambiados)} {cambiados[:5]}.",
          f"- `plantilla_activa.json` escrito: {'sí' if out['plantilla_activa_escrita'] else 'no'} · estado después: {out['estado_despues']}.",
          "", f"**Resultado: {out['resultado']}.**", ""]
    open(os.path.join(ENS, "resultados", "seleccion_inversa_4_11.md"), "w", encoding="utf-8").write("\n".join(md))
    print("\n".join(md))
    shutil.rmtree(tmp, ignore_errors=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
