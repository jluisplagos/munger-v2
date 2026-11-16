#!/usr/bin/env python3
"""c9b · T9 (cuarta comprobación), a nivel de unidad como r16: Pipeline.solicitud_auditoria_vigente() sobre un estado escrito por la sonda
(no se ejecuta ningún paso ni LibreOffice). ¿Qué motivo lleva la solicitud nueva cuando el relevo tiene «archivos_cambiados» mal formado
o ausente, y con la bandera «relevo_por_refijar» todavía en el estado?   Uso: python3 -I -B c9b_relevo_motivo.py"""
import json, os, shutil, sys, tempfile
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sondas3"))
import comun3  # noqa: F401
from comun3 import PV, ACT
import pipeline as PL  # noqa: E402
print("código:", ACT)
CFG = json.load(open(os.path.join(PV, "config_v2.json"), encoding="utf-8"))
TMP = tempfile.mkdtemp(prefix="rev4_c9b_")
A, B = "a" * 16, "b" * 16
REL = {"material_fijado": A, "material_vigente": B, "detectado": "2026-11-15T11:00:00+00:00", "material_refijado": B}
SOL = {"id": "SA-0000000000000001", "material": A, "creada": "2026-11-15T10:00:00+00:00", "motivo": "auditoría del material fijado en el paso 13", "estado": "pendiente",
       "respuesta_sha256": None, "respondida": None, "veredicto": None}
for nombre, extra, mas in (("lista de textos (normal)", {"archivos_cambiados": ["verificacion_entradas.json", "fase_c.json"]}, {}),
                           ("ausente", {}, {}), ("nulo", {"archivos_cambiados": None}, {}), ("número", {"archivos_cambiados": 7}, {}), ("lista con un objeto y un número", {"archivos_cambiados": [{"a": 1}, 2]}, {}),
                           ("texto", {"archivos_cambiados": "fase_c.json"}, {}), ("normal, con la bandera relevo_por_refijar aún en el estado", {"archivos_cambiados": ["fase_c.json"]}, {"relevo_por_refijar": True})):
    d = os.path.join(TMP, str(abs(hash(nombre))), "EmpresaX")
    os.makedirs(d)
    st = {"paso": 13, "estado_analisis": None, "intentos": {"fase_b": 0, "fase_c": 0, "auditoria": 0, "vueltas_c_a_b": 0, "vueltas_b_a_a": 0}, "historial": [], "motor": "B", "fase_b_escrita": True,
          "fase_c_escrita": True, "esperando": None, "inicio": "2026-11-15T10:00:00", "material_auditoria": B, "solicitudes_auditoria": [dict(SOL)], "relevos_caducados": [dict(REL, **extra)]}
    st.update(mas)
    json.dump(st, open(os.path.join(d, "estado_pipeline.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    try:
        s = PL.Pipeline(d, CFG).solicitud_auditoria_vigente()
        st2 = json.load(open(os.path.join(d, "estado_pipeline.json"), encoding="utf-8"))
        print(f"   archivos_cambiados = {nombre:58} → motivo: «{s['motivo'][:150]}» · bandera en el estado: {st2.get('relevo_por_refijar', '(no)')}")
    except Exception as ex:  # noqa: BLE001
        print(f"   archivos_cambiados = {nombre:58} → EXCEPCIÓN {type(ex).__name__}: {str(ex)[:120]}")
shutil.rmtree(TMP, ignore_errors=True)
