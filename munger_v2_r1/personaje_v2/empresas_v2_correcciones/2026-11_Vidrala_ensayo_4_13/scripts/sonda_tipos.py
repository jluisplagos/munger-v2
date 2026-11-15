"""Sonda 4.13 §3: tipos JSON erróneos en la primera llamada de cada vía, sobre copias aisladas del piloto 4.11."""
import json, os, sys
PV = sys.argv[1]
vias = sys.argv[3].split(",") if len(sys.argv) > 3 else ["pipeline", "ficha", "informe", "resumen"]
sys.path.insert(0, os.path.join(PV, "pruebas")); sys.path.insert(0, os.path.join(PV, "scripts"))
import test_integracion_v64 as T
os.makedirs(T.TMP, exist_ok=True)
def escribir(c, f, v):
    json.dump(v, open(os.path.join(c, f), "w", encoding="utf-8"))
def mod(c, caso):
    f, ruta, val = caso
    p = os.path.join(c, f)
    if ruta is None:
        escribir(c, f, val); return
    d = json.load(open(p, encoding="utf-8")); x = d
    for k in ruta[:-1]: x = x[k]
    x[ruta[-1]] = val
    escribir(c, f, d)
CASOS = {
 "ce_null": ("configuracion_economica.json", None, None), "ce_lista": ("configuracion_economica.json", None, []),
 "ce_escalar": ("configuracion_economica.json", None, 3), "ce_N1_lista": ("configuracion_economica.json", ["N1"], []),
 "ce_PM1_texto": ("configuracion_economica.json", ["PM1"], "x"), "ce_modo_lista": ("configuracion_economica.json", ["modo"], []),
 "pa_null": ("plantilla_activa.json", None, None), "pa_lista": ("plantilla_activa.json", None, []), "pa_escalar": ("plantilla_activa.json", None, "v"),
 "pa_sha_lista": ("plantilla_activa.json", ["archivo_sha256"], []),
 "var_null": ("configuracion_v64_variantes.json", None, None),
 "mat_lista": ("material_auditoria.json", None, []), "mat_null": ("material_auditoria.json", None, None), "mat_archivos_texto": ("material_auditoria.json", ["archivos"], "x"),
 "cv_lista": ("cierre_vigente.json", None, []), "cv_null": ("cierre_vigente.json", None, None),
 "sol_lista": ("solicitud_auditoria.json", None, []), "pub_lista": ("publicaciones_resumen.json", None, []),
 "pub_publicaciones_dict": ("publicaciones_resumen.json", ["publicaciones"], {}), "est_lista": ("estado_pipeline.json", None, []),
 "est_auditoria_respuesta_lista": ("estado_pipeline.json", ["auditoria_respuesta"], []),
 "ficha_cierre_lista": ("ficha.json", ["cierre"], []), "ficha_decision_texto": ("ficha.json", ["decision"], "x"), "var_variantes_dict": ("configuracion_v64_variantes.json", ["variantes"], {}),
}
sel = sys.argv[2].split(",") if len(sys.argv) > 2 and sys.argv[2] != "todos" else list(CASOS)
for k in sel:
    for via in vias:
        c = T.copia_piloto(f"sonda_{k}_{via}")
        mod(c, CASOS[k])
        rc, out = T.primera_llamada(c, via)
        try:
            ok, d = T.retirada_comprobada(c)
        except Exception as e:
            ok, d = False, f"comprobación: {type(e).__name__} {e}"
        tb = "Traceback" in out
        ult = out.strip().splitlines()[-1][:150] if out.strip() else ""
        print(f"{k:18s} {via:8s} rc={rc:<3} retirada={'sí' if ok else 'NO'} {'EXCEPCIÓN' if tb else ''} · {ult}")
