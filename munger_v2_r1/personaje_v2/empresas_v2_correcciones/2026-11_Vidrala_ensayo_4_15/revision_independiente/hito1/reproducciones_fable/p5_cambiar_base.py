"""Sondas de cambiar_base.py (sin LibreOffice): persistencia de `analisis`, descartes, herencia y diagnóstico «construido_por_fase1_historia»."""
import copy, json, os, shutil, subprocess, sys, tempfile
V2 = os.environ.get("V2", "/tmp/rev_fable/trabajo_copia")          # árbol vigente (copia)
B14 = os.environ.get("B14", "/tmp/rev_fable/base/munger_v2_r1")     # árbol 4.14 (copia)
W = tempfile.mkdtemp(prefix="rev_fable_cb_")
def run(raiz, cambio):
    r = subprocess.run([sys.executable, "-B", os.path.join(raiz, "personaje_v2", "scripts", "cambiar_base.py"), "preparar", cambio], capture_output=True, text=True, cwd=raiz)
    return r.returncode, (r.stdout + r.stderr)
v = lambda x: x.get("valor") if isinstance(x, dict) else x
# --- A: CAMBIO 4.15 con el código vigente
d = json.load(open(os.path.join(V2, "personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_15/configuracion/cambio_elis_c48_4_15.json"), encoding="utf-8"))
dA = copy.deepcopy(d); dA["origen"] = os.path.join(V2, dA["origen"]); dA["destino"] = os.path.join(W, "A")
json.dump(dA, open(os.path.join(W, "cambioA.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
rc, out = run(V2, os.path.join(W, "cambioA.json")); print("A (código vigente, CAMBIO 4.15): rc", rc, out[-200:] if rc else "")
regA = json.load(open(os.path.join(W, "A", "resultados", "cambio_de_base.json"), encoding="utf-8"))
f1A = json.load(open(os.path.join(W, "A", "Elis", "fase1_v63.json"), encoding="utf-8")); mA = json.load(open(os.path.join(W, "A", "Elis", "fase1_metadatos.json"), encoding="utf-8"))
print("  sustituidas (construido_por_fase1_historia → valor):", {c: (x["construido_por_fase1_historia"], x["valor"]) for c, x in regA["sustituidas_en_fase1_v63"].items()})
print("  nota de fase1_v63.json:", [n for n in f1A["_notas"] if "cambio de base" in n][0][:420])
print("  fase1_metadatos.analisis:", {c: (v(x) if "calculo" not in x else "calculo") for c, x in (mA.get("analisis") or {}).items()})
# --- old: el mismo CAMBIO sin `calculo` (C48 como constante 108, como en la 4.14) con el código 4.14
cam414 = os.path.join(B14, "personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_14")
c414 = [os.path.join(r, f) for r, _, fs in os.walk(cam414) for f in fs if f.startswith("cambio_decisiones_elis") and f.endswith(".json")]
print("CAMBIO de la 4.14:", [os.path.relpath(x, B14) for x in c414])
d0 = json.load(open(c414[0], encoding="utf-8")); d0["origen"] = os.path.join(B14, d0["origen"]); d0["destino"] = os.path.join(W, "old")
json.dump(d0, open(os.path.join(W, "cambio_old.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
rc, out = run(B14, os.path.join(W, "cambio_old.json")); print("old (código 4.14, CAMBIO 4.14): rc", rc, out[-200:] if rc else "")
reg0 = json.load(open(os.path.join(W, "old", "resultados", "cambio_de_base.json"), encoding="utf-8"))
f10 = json.load(open(os.path.join(W, "old", "Elis", "fase1_v63.json"), encoding="utf-8")); m0 = json.load(open(os.path.join(W, "old", "Elis", "fase1_metadatos.json"), encoding="utf-8"))
print("  sustituidas (construido_por_fase1_historia → valor):", {c: (x["construido_por_fase1_historia"], x["valor"]) for c, x in reg0["sustituidas_en_fase1_v63"].items()})
print("  nota de fase1_v63.json:", [n for n in f10["_notas"] if "cambio de base" in n][0][:420])
print("  fase1_metadatos.analisis:", {c: v(x) for c, x in (m0.get("analisis") or {}).items()})
print("  analisis de fase1_v63.json — 4.14:", {c: v(x) for c, x in f10["analisis"].items()})
print("  analisis de fase1_v63.json — 4.15:", {c: v(x) for c, x in f1A["analisis"].items()})
# --- B: segundo cambio desde A que DESCARTA C42 y no declara nada más (código vigente)
dB = copy.deepcopy(d); dB["origen"] = os.path.join(W, "A", "Elis"); dB["destino"] = os.path.join(W, "B")
dB["analisis"] = {}; dB["analisis_que_se_descartan"] = {"C42": "(prueba) el múltiplo EV/EBITDA de la base anterior ya no vale"}; dB["evidencia"] = {}; dB["correcciones_fase1_partes"] = []
dB["conservar"] = [x for x in dB["conservar"] if x != "verificacion_entradas.json"] + ["fase1_metadatos.json"] if False else dB["conservar"]
json.dump(dB, open(os.path.join(W, "cambioB.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
rc, out = run(V2, os.path.join(W, "cambioB.json")); print("B (código vigente; origen = A; analisis = {}; descarta C42): rc", rc, out[-300:] if rc else "")
if rc == 0:
    f1B = json.load(open(os.path.join(W, "B", "Elis", "fase1_v63.json"), encoding="utf-8")); nr = json.load(open(os.path.join(W, "B", "antecedentes", "notas_retiradas.json"), encoding="utf-8"))
    print("  C42 en el fase1_v63.json nuevo:", f1B["analisis"].get("C42", "(no está)") if not isinstance(f1B["analisis"].get("C42"), dict) else v(f1B["analisis"]["C42"]),
          "| registrado como descartado:", [x for x in nr["retiradas"] if "descartadas" in str(x.get("de"))])
    print("  entradas heredadas sin declarar en el CAMBIO B:", {c: v(x) for c, x in f1B["analisis"].items()})
# --- B2: lo mismo con el flujo 4.14 (origen = old; código 4.14)
dB2 = copy.deepcopy(d0); dB2["origen"] = os.path.join(W, "old", "Elis"); dB2["destino"] = os.path.join(W, "B2")
dB2["analisis"] = {}; dB2["analisis_que_se_descartan"] = {"C42": "(prueba)"}; dB2["evidencia"] = {}; dB2["correcciones_fase1_partes"] = []
json.dump(dB2, open(os.path.join(W, "cambioB2.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
rc, out = run(B14, os.path.join(W, "cambioB2.json")); print("B2 (código 4.14; origen = old; analisis = {}; descarta C42): rc", rc, "|", out.strip()[-520:])
shutil.rmtree(W, ignore_errors=True)
