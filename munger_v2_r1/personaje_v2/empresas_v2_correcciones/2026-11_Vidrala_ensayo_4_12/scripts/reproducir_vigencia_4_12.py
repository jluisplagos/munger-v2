#!/usr/bin/env python3
"""Reproducción del fallo de vigencia que encontró la revisión externa de la 4.11 (encargo 4.12 §3) y comprobación de la corrección.
Copia aislada del piloto cerrado de la 4.11 (…/2026-11_Vidrala_ensayo_4_11/piloto, que no se toca), con el destino del resumen y el
registro de publicaciones reubicados dentro de la copia; cambia SOLO configuracion_economica.json (PM1.lambda = 0.9, inválida) y
ejecuta por PRIMERA vez el pipeline con config_v2_v64_experimental.json, usando el código del árbol que se indique.
Uso (desde munger_v2_r1/): python3 -I …/2026-11_Vidrala_ensayo_4_12/scripts/reproducir_vigencia_4_12.py [--codigo RAIZ_DEL_ARBOL] [--salida NOMBRE]
  --codigo: árbol cuyo pipeline se ejecuta (por omisión, este). El piloto se copia siempre de este árbol.
Escribe …/2026-11_Vidrala_ensayo_4_12/resultados/<NOMBRE>.json y .md (por omisión, reproduccion_vigencia_4_12).
Código 0 si, con el código ejecutado, la aprobación del material anterior ya no consta como vigente después de la llamada."""
import argparse, csv, hashlib, json, os, shutil, subprocess, sys, tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
ENS = os.path.dirname(AQUI)
RAIZ = os.path.abspath(os.path.join(ENS, "..", "..", ".."))
PIL = os.path.join(RAIZ, "personaje_v2", "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_11", "piloto")


def huellas(d):
    out = {}
    for r, ds, fs in os.walk(d):
        for f in fs:
            p = os.path.join(r, f)
            out[os.path.relpath(p, d)] = hashlib.sha256(open(p, "rb").read()).hexdigest()
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--codigo", default=RAIZ)
    ap.add_argument("--salida", default="reproduccion_vigencia_4_12")
    a = ap.parse_args()
    codigo = os.path.abspath(a.codigo)
    t = tempfile.mkdtemp(prefix="vigencia_4_12_")
    dst = os.path.join(t, "piloto")
    shutil.copytree(PIL, dst, ignore=shutil.ignore_patterns(".lo_perfil", "variantes_v64", "prompts_generados", "recalc"))
    for r, ds, fs in os.walk(dst):
        for x in ds + fs:
            os.chmod(os.path.join(r, x), 0o755 if os.path.isdir(os.path.join(r, x)) else 0o644)
    c = os.path.join(dst, "Vidrala")
    for n in ("publicaciones_resumen.json", ".publicaciones_resumen.respaldo.json"):
        p = os.path.join(c, n)
        if os.path.exists(p):
            reg = json.load(open(p, encoding="utf-8"))
            for e in reg.get("publicaciones") or []:
                e["csv"] = os.path.join(dst, os.path.basename(e["csv"]))
                e["expediente"] = c
            json.dump(reg, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    pc = os.path.join(c, "configuracion_economica.json")
    conf = json.load(open(pc, encoding="utf-8"))
    conf["PM1"]["lambda"] = 0.9
    json.dump(conf, open(pc, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    antes = huellas(dst)
    env = {k: v for k, v in os.environ.items() if k != "MUNGER_CONFIG"}
    r = subprocess.run([sys.executable, "-B", os.path.join(codigo, "personaje_v2", "scripts", "pipeline.py"), c, "--config",
                        os.path.join(codigo, "personaje_v2", "config_v2_v64_experimental.json")], capture_output=True, text=True, env=env, timeout=1200)
    despues = huellas(dst)
    st = json.load(open(os.path.join(c, "estado_pipeline.json"), encoding="utf-8"))
    filas = list(csv.DictReader(open(os.path.join(dst, "resumen_v2.csv"), encoding="utf-8", newline="")))
    retirada = (st.get("auditoria") != "APROBADO" and st.get("estado_analisis") != "concluido" and not os.path.exists(os.path.join(c, "ficha.json"))
                and all((f.get("verificacion") or "").startswith("SIN APROBACIÓN VIGENTE") for f in filas))
    out = {"codigo": codigo, "piloto_copiado_de": os.path.relpath(PIL, RAIZ), "alteracion": "configuracion_economica.json: PM1.lambda = 0.9 (inválida)",
           "llamada": "pipeline.py COPIA --config config_v2_v64_experimental.json (primera llamada, sin MUNGER_CONFIG)",
           "codigo_de_salida": r.returncode, "salida": (r.stdout + r.stderr).strip().splitlines()[-4:],
           "estado_despues": {k: st.get(k) for k in ("paso", "estado_analisis", "auditoria")},
           "ficha_oficial_presente": os.path.exists(os.path.join(c, "ficha.json")), "antecedentes": sorted(os.listdir(os.path.join(c, "historial_cierres"))) if os.path.isdir(os.path.join(c, "historial_cierres")) else [],
           "filas_del_resumen": [f.get("verificacion", "")[:80] for f in filas],
           "archivos_cambiados": sorted(k for k in antes if despues.get(k) != antes[k]), "archivos_nuevos": sorted(k for k in despues if k not in antes),
           "aprobacion_del_material_anterior_retirada": retirada}
    json.dump(out, open(os.path.join(ENS, "resultados", a.salida + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    md = [f"# Reproducción del fallo de vigencia (encargo 4.12 §3) · código de `{codigo}`", "",
          f"- Copia aislada de `{out['piloto_copiado_de']}` (el original no se toca), con el resumen y el registro de publicaciones reubicados en la copia.",
          f"- Alteración: {out['alteracion']}. Llamada: {out['llamada']}.",
          f"- Código de salida: **{r.returncode}**.", "- Salida:", "```", *out["salida"], "```",
          f"- Después: estado {out['estado_despues']} · ficha oficial {'presente' if out['ficha_oficial_presente'] else 'archivada'} · antecedentes {out['antecedentes']}.",
          f"- Fila del resumen: {out['filas_del_resumen']}.",
          f"- Archivos cambiados: {len(out['archivos_cambiados'])} · nuevos: {len(out['archivos_nuevos'])}.", "",
          f"**Aprobación del material anterior retirada: {'sí' if retirada else 'NO (sigue constando como vigente)'}.**", ""]
    open(os.path.join(ENS, "resultados", a.salida + ".md"), "w", encoding="utf-8").write("\n".join(md))
    print("\n".join(md))
    shutil.rmtree(t, ignore_errors=True)
    return 0 if retirada else 1


if __name__ == "__main__":
    sys.exit(main())
