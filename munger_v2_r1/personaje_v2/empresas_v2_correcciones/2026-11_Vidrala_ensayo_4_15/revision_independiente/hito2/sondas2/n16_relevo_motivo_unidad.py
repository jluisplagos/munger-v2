#!/usr/bin/env python3
"""n16 · H9 del relevo (segunda pasada), a nivel de UNIDAD: Pipeline.solicitud_auditoria_vigente() llamada directamente sobre una carpeta
temporal con un estado_pipeline.json escrito por la sonda (NO se ejecuta pipeline.py ni ningún paso, ni LibreOffice: solo ese método, que
escribe estado_pipeline.json, solicitud_auditoria.json y auditorias_conocidas.json en la carpeta temporal).
1) relevo caducado normal: el motivo de la solicitud nueva y el vínculo relevo → solicitud;
2) el material vuelve a ser el de la solicitud antigua (p. ej. el archivo se restauró): ¿qué pasa con el relevo sin solicitud?
3) muchos archivos cambiados y nombres raros; 4) estado con relevos_caducados mal formado.
Uso: python3 -I -B n16_relevo_motivo_unidad.py"""
import json, os, shutil, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun2 import VE, PV, ETIQUETA
import pipeline as PL  # noqa: E402
import cierre_v2 as CIE  # noqa: E402
print("código:", ETIQUETA)
CFG = json.load(open(os.path.join(PV, "config_v2.json"), encoding="utf-8"))
TMP = tempfile.mkdtemp(prefix="rev2_n16_")


def estado(nombre, material, solicitudes, relevos, esperando=None, motivo_correccion=None):
    d = os.path.join(TMP, nombre, "EmpresaX")
    os.makedirs(d)
    st = {"paso": 13, "estado_analisis": None, "intentos": {"fase_b": 0, "fase_c": 0, "auditoria": 0, "vueltas_c_a_b": 0, "vueltas_b_a_a": 0}, "historial": [], "motor": "B",
          "fase_b_escrita": True, "fase_c_escrita": True, "esperando": esperando, "inicio": "2026-11-15T10:00:00", "material_auditoria": material,
          "solicitudes_auditoria": solicitudes, "relevos_caducados": relevos}
    if motivo_correccion:
        st["motivo_correccion"] = motivo_correccion
    json.dump(st, open(os.path.join(d, "estado_pipeline.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return d


def sol(i, material, est="pendiente"):
    return {"id": f"SA-{i:016x}", "material": material, "creada": "2026-11-15T10:00:00+00:00", "motivo": "auditoría del material fijado en el paso 13", "estado": est,
            "respuesta_sha256": None, "respondida": None, "veredicto": None}


def correr(d):
    try:
        P = PL.Pipeline(d, CFG)
        s = P.solicitud_auditoria_vigente()
        st = json.load(open(os.path.join(d, "estado_pipeline.json"), encoding="utf-8"))
        return s, st, None
    except Exception as ex:  # noqa: BLE001
        return None, None, f"{type(ex).__name__}: {str(ex)[:160]}"


REL = {"material_fijado": "aaaaaaaaaaaaaaaa", "material_vigente": "bbbbbbbbbbbbbbbb", "archivos_cambiados": ["verificacion_entradas.json"], "detectado": "2026-11-15T11:00:00+00:00"}
print("\n== 1 · relevo caducado normal (material nuevo, solicitud antigua pendiente)")
d = estado("uno", "bbbbbbbbbbbbbbbb", [sol(1, "aaaaaaaaaaaaaaaa")], [dict(REL)])
s, st, err = correr(d)
print("   error:", err)
if s:
    print("   solicitud nueva:", s["id"] != sol(1, "")["id"], "· material", s["material"], "\n   motivo:", s["motivo"])
    print("   solicitudes:", [(x["id"][-4:], x["estado"]) for x in st["solicitudes_auditoria"]], "· relevo.solicitud == nueva:", st["relevos_caducados"][-1].get("solicitud") == s["id"])
    print("   solicitud_auditoria.json:", json.load(open(os.path.join(d, "solicitud_auditoria.json"), encoding="utf-8"))["motivo"][:120])

print("\n== 2 · el material vuelve a ser el de la solicitud antigua (el archivo cambiado se restauró antes de volver a fijar el material)")
d = estado("dos", "aaaaaaaaaaaaaaaa", [sol(1, "aaaaaaaaaaaaaaaa")], [dict(REL)])
s, st, err = correr(d)
print("   error:", err)
if s:
    print("   se conserva la solicitud antigua:", s["id"] == sol(1, "")["id"], "· relevo con solicitud asociada:", st["relevos_caducados"][-1].get("solicitud"))
    # más tarde, por otro motivo (p. ej. una corrección de la fase C), el material cambia y se pide otra auditoría
    st["material_auditoria"] = "cccccccccccccccc"
    json.dump(st, open(os.path.join(d, "estado_pipeline.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    s2, st2, err2 = correr(d)
    print("   después, material nuevo por OTRO motivo → error:", err2)
    if s2:
        print("   motivo de la solicitud nueva:", s2["motivo"])
        print("   ->", "LA SOLICITUD NUEVA ARRASTRA EL TEXTO DE UN RELEVO ANTERIOR QUE NO ES SU CAUSA" if "relevo caducado" in s2["motivo"] else "sin arrastre")

print("\n== 3 · 60 archivos cambiados y nombres con caracteres raros")
rel3 = dict(REL, archivos_cambiados=[f"archivo_{i:02d}_«raro»\n{{x}}.json" for i in range(60)])
d = estado("tres", "bbbbbbbbbbbbbbbb", [sol(1, "aaaaaaaaaaaaaaaa")], [rel3])
s, st, err = correr(d)
print("   error:", err)
if s:
    print("   longitud del motivo:", len(s["motivo"]), "· empieza:", repr(s["motivo"][:150]))

print("\n== 4 · estado con relevos_caducados mal formado")
for nombre, rel in (("lista de textos", ["x"]), ("objeto en vez de lista", {"material_fijado": "a"}), ("texto", "x"), ("lista con un objeto sin claves", [{}]), ("número", 5)):
    d = estado("cuatro_" + nombre.replace(" ", "_"), "bbbbbbbbbbbbbbbb", [sol(1, "aaaaaaaaaaaaaaaa")], rel)
    s, st, err = correr(d)
    print(f"   relevos_caducados = {nombre:32} → " + (f"EXCEPCIÓN {err}" if err else f"solicitud nueva con motivo «{s['motivo'][:70]}…»"))
shutil.rmtree(TMP, ignore_errors=True)
