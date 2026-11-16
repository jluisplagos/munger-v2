#!/usr/bin/env python3
"""r16 · N10 del relevo (tercera pasada), a nivel de UNIDAD, como n16 de la segunda pasada: Pipeline.solicitud_auditoria_vigente() llamada
directamente sobre una carpeta temporal con un estado_pipeline.json escrito por la sonda (NO se ejecuta pipeline.py ni ningún paso, ni
LibreOffice). Diferencia con n16: el estado lleva «material_refijado» en el relevo, como lo deja el paso 13 de la tercera candidata justo
después de volver a fijar el material (pipeline.py: _rels[-1]["material_refijado"] = st["material_auditoria"]).
1) flujo normal: el relevo llevó a fijar ESTE material → el motivo lo dice y el relevo queda ligado a la solicitud;
2) el material vuelve a ser el de la solicitud antigua y, más tarde, cambia por otra causa → la solicitud nueva no arrastra el relevo;
3) segunda llamada con el mismo material → no se duplica nada;  4) estado mal formado;
5) relevo ANTERIOR a esta candidata (ya con «solicitud», sin «material_refijado»): ¿qué «material_refijado» recibiría si el paso 13 vuelve
   a fijar material por otra causa? (se reproduce la línea del paso 13 sobre el estado; no se ejecuta el paso).
PV=<prev>/personaje_v2 para la candidata anterior.  Uso: python3 -I -B r16_relevo_unidad.py"""
import json, os, shutil, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comun3
from comun3 import PV
import pipeline as PL  # noqa: E402
print("código:", "tercera (f3d15e8)" if "material_refijado" in open(PL.__file__, encoding="utf-8").read() else "anterior (92b2362)", "·", PL.__file__.split("/fable/")[1])
CFG = json.load(open(os.path.join(PV, "config_v2.json"), encoding="utf-8"))
TMP = tempfile.mkdtemp(prefix="rev3_r16_")


def estado(nombre, material, solicitudes, relevos, **mas):
    d = os.path.join(TMP, nombre, "EmpresaX")
    os.makedirs(d)
    st = {"paso": 13, "estado_analisis": None, "intentos": {"fase_b": 0, "fase_c": 0, "auditoria": 0, "vueltas_c_a_b": 0, "vueltas_b_a_a": 0}, "historial": [], "motor": "B",
          "fase_b_escrita": True, "fase_c_escrita": True, "esperando": None, "inicio": "2026-11-15T10:00:00", "material_auditoria": material,
          "solicitudes_auditoria": solicitudes, "relevos_caducados": relevos}
    st.update(mas)
    json.dump(st, open(os.path.join(d, "estado_pipeline.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return d


def sol(i, material, est="pendiente"):
    return {"id": f"SA-{i:016x}", "material": material, "creada": "2026-11-15T10:00:00+00:00", "motivo": "auditoría del material fijado en el paso 13", "estado": est,
            "respuesta_sha256": None, "respondida": None, "veredicto": None}


def correr(d):
    try:
        P = PL.Pipeline(d, CFG)
        s = P.solicitud_auditoria_vigente()
        return s, json.load(open(os.path.join(d, "estado_pipeline.json"), encoding="utf-8")), None
    except Exception as ex:  # noqa: BLE001
        return None, None, f"{type(ex).__name__}: {str(ex)[:160]}"


A, B, C = "a" * 16, "b" * 16, "c" * 16
REL = {"material_fijado": A, "material_vigente": B, "archivos_cambiados": ["verificacion_entradas.json"], "detectado": "2026-11-15T11:00:00+00:00"}
print("\n== 1 · flujo normal: relevo → paso 12 → el paso 13 fija el material B y lo anota en el relevo → solicitud nueva")
d = estado("uno", B, [sol(1, A)], [dict(REL, material_refijado=B)])
s, st, err = correr(d)
print("   error:", err)
if s:
    print("   motivo:", s["motivo"][:230])
    print("   solicitudes:", [(x["id"][-4:], x["estado"]) for x in st["solicitudes_auditoria"]], "· relevo.solicitud == nueva:", st["relevos_caducados"][-1].get("solicitud") == s["id"])
    s2, st2, err2 = correr(d)
    print("   segunda llamada con el mismo material → misma solicitud:", s2 and s2["id"] == s["id"], "· solicitudes:", len(st2["solicitudes_auditoria"]), "· error:", err2)
    # más tarde el material cambia por otra causa (corrección): la solicitud siguiente no arrastra el relevo
    st2["material_auditoria"] = C
    json.dump(st2, open(os.path.join(d, "estado_pipeline.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    s3, st3, err3 = correr(d)
    print("   después, material C por otra causa → motivo:", (s3 or {}).get("motivo"), "· error:", err3)

print("\n== 2 · el material refijado es el de la solicitud antigua (el archivo se restauró); después cambia por otra causa")
d = estado("dos", A, [sol(1, A)], [dict(REL, material_refijado=A)])
s, st, err = correr(d)
print("   error:", err, "· se conserva la solicitud antigua:", s and s["id"] == sol(1, "")["id"], "· relevo.solicitud:", st and st["relevos_caducados"][-1].get("solicitud"))
if st:
    st["material_auditoria"] = C
    json.dump(st, open(os.path.join(d, "estado_pipeline.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    s2, st2, err2 = correr(d)
    print("   material C por otra causa → motivo:", (s2 or {}).get("motivo"), "→", "ARRASTRA el relevo" if "relevo caducado" in str((s2 or {}).get("motivo")) else "sin arrastre", "· error:", err2)

print("\n== 3 · relevo SIN «material_refijado» (estado escrito por la candidata anterior, o si el paso 13 no llegó a fijar el material)")
d = estado("tres", B, [sol(1, A)], [dict(REL)])
s, st, err = correr(d)
print("   error:", err, "· motivo:", (s or {}).get("motivo"), "· relevo.solicitud:", st and st["relevos_caducados"][-1].get("solicitud"))

print("\n== 4 · estado con relevos_caducados mal formado")
for nombre, rel in (("lista de textos", ["x"]), ("objeto en vez de lista", {"material_fijado": "a"}), ("texto", "x"), ("lista con un objeto sin claves", [{}]), ("número", 5), ("nulo", None),
                    ("lista con un relevo cuyo material_refijado no es texto", [dict(REL, material_refijado=[B])]), ("lista con archivos_cambiados que no es lista", [dict(REL, material_refijado=B, archivos_cambiados=7)]),
                    ("lista con archivos_cambiados de números", [dict(REL, material_refijado=B, archivos_cambiados=[1, 2])])):
    d = estado("cuatro_" + nombre.replace(" ", "_")[:40], B, [sol(1, A)], rel)
    s, st, err = correr(d)
    print(f"   relevos_caducados = {nombre:56} → " + (f"EXCEPCIÓN {err}" if err else f"solicitud nueva · motivo «{s['motivo'][:75]}…»"))

print("\n== 5 · relevo de un estado anterior a esta candidata: ya tiene «solicitud» y no tiene «material_refijado»")
st = {"relevos_caducados": [dict(REL, solicitud="SA-000000000000000f")], "material_auditoria": C}
_rels = st.get("relevos_caducados")  # las tres líneas del paso 13 (pipeline.py) tras fijar el material, copiadas tal cual
if isinstance(_rels, list) and _rels and isinstance(_rels[-1], dict) and not _rels[-1].get("material_refijado"):
    _rels[-1]["material_refijado"] = st["material_auditoria"]
print("   el paso 13 fija el material C por otra causa (no hay relevo nuevo) → el relevo antiguo queda:", {k: st["relevos_caducados"][-1].get(k) for k in ("material_fijado", "material_vigente", "solicitud", "material_refijado")})
print("   (ese relevo llevó en su día a fijar B y a la solicitud …000f; ahora dice que el material refijado fue C)")
shutil.rmtree(TMP, ignore_errors=True)
