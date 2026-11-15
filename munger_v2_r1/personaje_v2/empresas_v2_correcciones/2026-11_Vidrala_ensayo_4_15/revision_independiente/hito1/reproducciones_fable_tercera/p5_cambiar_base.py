"""Sondas de cambiar_base.py sobre el árbol CONGELADO (sin LibreOffice). Hallazgo 8: descartes, herencia reconocida y diagnóstico de la Historia."""
import copy, json, os, shutil, subprocess, sys, tempfile
V2 = os.environ.get("V2", "/tmp/rev_fable3/congelado3")
W = tempfile.mkdtemp(prefix="rev_fable_cb_")
def run(raiz, cambio):
    r = subprocess.run([sys.executable, "-B", os.path.join(raiz, "personaje_v2", "scripts", "cambiar_base.py"), "preparar", cambio], capture_output=True, text=True, cwd=raiz)
    return r.returncode, (r.stdout + r.stderr)
v = lambda x: x.get("valor") if isinstance(x, dict) else x
d = json.load(open(os.path.join(V2, "personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_15/configuracion/cambio_elis_c48_4_15.json"), encoding="utf-8"))
def preparar(nombre, dd):
    p = os.path.join(W, f"cambio{nombre}.json"); json.dump(dd, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return run(V2, p)
# --- A: CAMBIO 4.15 con el código congelado
dA = copy.deepcopy(d); dA["origen"] = os.path.join(V2, dA["origen"]); dA["destino"] = os.path.join(W, "A")
rc, out = preparar("A", dA); print("A (CAMBIO 4.15 de Elis): rc", rc, out[-300:] if rc else "")
regA = json.load(open(os.path.join(W, "A", "resultados", "cambio_de_base.json"), encoding="utf-8"))
f1A = json.load(open(os.path.join(W, "A", "Elis", "fase1_v63.json"), encoding="utf-8")); mA = json.load(open(os.path.join(W, "A", "Elis", "fase1_metadatos.json"), encoding="utf-8"))
print("  (8c) sustituidas (construido_por_fase1_historia → valor):", {c: (x["construido_por_fase1_historia"], x["valor"]) for c, x in regA["sustituidas_en_fase1_v63"].items()})
print("  nota de fase1_v63.json:", [n for n in f1A["_notas"] if "cambio de base" in n][0][:330])
print("  fase1_metadatos.analisis:", {c: (v(x) if "calculo" not in x else "calculo") for c, x in (mA.get("analisis") or {}).items()})
print("  analisis de fase1_v63.json:", {c: v(x) for c, x in f1A["analisis"].items()})
print("  archivos sobrantes del primer construir (diagnóstico) en el destino:", sorted(os.listdir(os.path.join(W, "A", "Elis")))[:40])
print("  claves del registro cambio_de_base.json:", sorted(regA))
base_B = lambda: dict(copy.deepcopy(d), origen=os.path.join(W, "A", "Elis"), analisis={}, evidencia={}, correcciones_fase1_partes=[])
# --- B: segundo cambio desde A que DESCARTA C42 y no declara ni reconoce nada más
dB = base_B(); dB["destino"] = os.path.join(W, "B"); dB["analisis_que_se_descartan"] = {"C42": "(prueba) el múltiplo EV/EBITDA de la base anterior ya no vale"}
rc, out = preparar("B", dB); print("\nB (origen = A; analisis = {}; descarta C42; no reconoce el resto): rc", rc, "|", out.strip()[-420:], "| destino retirado:", not os.path.exists(os.path.join(W, "B", "Elis")))
# --- B1: descarta C42 y reconoce el resto
resto = [c for c in mA["analisis"] if c != "C42"]
dB1 = base_B(); dB1["destino"] = os.path.join(W, "B1"); dB1["analisis_que_se_descartan"] = {"C42": "(prueba) ya no vale"}; dB1["analisis_que_se_conservan"] = {c: "(prueba) sigue valiendo para la base nueva" for c in resto}
rc, out = preparar("B1", dB1); print("\nB1 (descarta C42; reconoce las otras", len(resto), "en analisis_que_se_conservan): rc", rc, out[-300:] if rc else "")
if rc == 0:
    f1B = json.load(open(os.path.join(W, "B1", "Elis", "fase1_v63.json"), encoding="utf-8")); mB = json.load(open(os.path.join(W, "B1", "Elis", "fase1_metadatos.json"), encoding="utf-8"))
    nr = json.load(open(os.path.join(W, "B1", "antecedentes", "notas_retiradas.json"), encoding="utf-8")); regB = json.load(open(os.path.join(W, "B1", "resultados", "cambio_de_base.json"), encoding="utf-8"))
    print("  (8a) C42 en el fase1_v63.json nuevo:", f1B["analisis"].get("C42", "(no está)"), "| en fase1_metadatos.analisis:", "C42" in (mB.get("analisis") or {}), "| registrado como descartado:", [x for x in nr["retiradas"] if "descartadas" in str(x.get("de"))])
    print("  (8b) entradas conservadas en el expediente nuevo:", {c: v(x) for c, x in f1B["analisis"].items()})
    print("  ¿el registro cambio_de_base.json/.md lista las entradas heredadas y reconocidas?:", "conserv" in json.dumps(regB, ensure_ascii=False).lower(), "/", "conserv" in open(os.path.join(W, "B1", "resultados", "cambio_de_base.md"), encoding="utf-8").read().lower(),
          "| sustituidas:", regB["sustituidas_en_fase1_v63"])
# --- B2: reconoce con motivo vacío / reconoce una celda que el origen no tiene / declara y descarta la misma
dB2 = base_B(); dB2["destino"] = os.path.join(W, "B2"); dB2["analisis_que_se_descartan"] = {}; dB2["analisis_que_se_conservan"] = {c: "" for c in mA["analisis"]}
rc, out = preparar("B2", dB2); print("\nB2 (reconoce todas con motivo VACÍO): rc", rc, "|", out.strip()[-160:] if rc else "aceptado")
dB3 = base_B(); dB3["destino"] = os.path.join(W, "B3"); dB3["analisis_que_se_descartan"] = {"C42": "x"}; dB3["analisis_que_se_conservan"] = dict({c: "x" for c in mA["analisis"]}, Z99="no existe")
rc, out = preparar("B3", dB3)
print("B3 (C42 a la vez en descartan y en conservan; conserva además una celda Z99 que el origen no declara): rc", rc, "|", out.strip()[-200:] if rc else "aceptado",
      "| C42 en metadatos nuevos:", "C42" in (json.load(open(os.path.join(W, "B3", "Elis", "fase1_metadatos.json"), encoding="utf-8")).get("analisis") or {}) if rc == 0 else None)
dB4 = base_B(); dB4["destino"] = os.path.join(W, "B4"); dB4["analisis"] = {"C42": dict(d["analisis"]["C42"])}; dB4["analisis_que_se_descartan"] = {"C42": "x"}; dB4["analisis_que_se_conservan"] = {c: "x" for c in resto}
rc, out = preparar("B4", dB4)
if rc == 0:
    f4 = json.load(open(os.path.join(W, "B4", "Elis", "fase1_v63.json"), encoding="utf-8")); n4 = json.load(open(os.path.join(W, "B4", "antecedentes", "notas_retiradas.json"), encoding="utf-8"))
    print("B4 (C42 DECLARADA en analisis y a la vez DESCARTADA): rc 0 | C42 en fase1_v63.json:", v(f4["analisis"].get("C42")), "| notas_retiradas la da por descartada:", bool([x for x in n4["retiradas"] if "descartadas" in str(x.get("de"))]))
else:
    print("B4 (C42 declarada y descartada a la vez): rc", rc, "|", out.strip()[-200:])
# --- C: descarta una entrada del FCF base heredada con cálculo (C48): ¿qué queda?
dC = base_B(); dC["destino"] = os.path.join(W, "C"); dC["analisis_que_se_descartan"] = {"C48": "(prueba) se abandona el tratamiento del inversor"}; dC["analisis_que_se_conservan"] = {c: "x" for c in mA["analisis"] if c != "C48"}
rc, out = preparar("C", dC)
if rc == 0:
    fC = json.load(open(os.path.join(W, "C", "Elis", "fase1_v63.json"), encoding="utf-8"))
    print("\nC (descarta C48 con cálculo heredado): rc 0 | C48 en el fase1_v63.json nuevo:", v(fC["analisis"].get("C48")), "(lo que da la Historia)")
else:
    print("\nC (descarta C48): rc", rc, "|", out.strip()[-300:])
shutil.rmtree(W, ignore_errors=True)
