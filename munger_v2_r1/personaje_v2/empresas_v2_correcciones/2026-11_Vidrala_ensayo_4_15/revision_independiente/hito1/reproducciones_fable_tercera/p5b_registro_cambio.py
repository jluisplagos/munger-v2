import copy, json, os, shutil, subprocess, sys, tempfile
V2 = "/tmp/rev_fable3/congelado3"
W = tempfile.mkdtemp(prefix="rev_fable_cb2_")
def run(cambio):
    r = subprocess.run([sys.executable, "-B", os.path.join(V2, "personaje_v2", "scripts", "cambiar_base.py"), "preparar", cambio], capture_output=True, text=True, cwd=V2)
    return r.returncode, (r.stdout + r.stderr)
d = json.load(open(os.path.join(V2, "personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_15/configuracion/cambio_elis_c48_4_15.json"), encoding="utf-8"))
dA = copy.deepcopy(d); dA["origen"] = os.path.join(V2, dA["origen"]); dA["destino"] = os.path.join(W, "A")
p = os.path.join(W, "A.json"); json.dump(dA, open(p, "w"), ensure_ascii=False); print("A rc", run(p)[0])
mA = json.load(open(os.path.join(W, "A", "Elis", "fase1_metadatos.json"), encoding="utf-8"))
dB = dict(copy.deepcopy(d), origen=os.path.join(W, "A", "Elis"), destino=os.path.join(W, "B1"), analisis={}, evidencia={}, correcciones_fase1_partes=[],
          analisis_que_se_descartan={"C42": "MOTIVO_DESCARTE"}, analisis_que_se_conservan={c: "MOTIVO_CONSERVA_" + c for c in mA["analisis"] if c != "C42"})
p = os.path.join(W, "B1.json"); json.dump(dB, open(p, "w"), ensure_ascii=False); rc, out = run(p); print("B1 rc", rc)
reg = open(os.path.join(W, "B1", "resultados", "cambio_de_base.json"), encoding="utf-8").read(); md = open(os.path.join(W, "B1", "resultados", "cambio_de_base.md"), encoding="utf-8").read()
print("registro .json menciona MOTIVO_CONSERVA / analisis_que_se_conservan / C24:", "MOTIVO_CONSERVA" in reg, "analisis_que_se_conservan" in reg, '"C24"' in reg)
print("registro .md menciona MOTIVO_CONSERVA / C24:", "MOTIVO_CONSERVA" in md, "C24" in md)
print("md:\n" + md[:1500])
f1 = json.load(open(os.path.join(W, "B1", "Elis", "fase1_v63.json"), encoding="utf-8"))
print("nota de fase1_v63.json del cambio B1:", [n for n in f1["_notas"] if "cambio de base" in n][-1][:300])
shutil.rmtree(W, ignore_errors=True)
