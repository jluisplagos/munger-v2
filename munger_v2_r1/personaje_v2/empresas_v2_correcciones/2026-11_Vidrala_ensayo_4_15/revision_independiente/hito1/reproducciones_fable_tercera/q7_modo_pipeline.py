"""Tercera pasada · N7 (modo de la entrada efectiva: entrada_efectiva.json «estricta» por defecto en los expedientes de cambiar_base;
pipeline.modo_entrada_efectiva falla en cerrado). Sin LibreOffice: se ejecutan SOLO los pasos 1 (migración) y 2 (relleno) del
Pipeline real sobre expedientes mínimos en una carpeta temporal; `soffice` se sustituye en el PATH por un sustituto que termina con 1.
1) modo_entrada_efectiva con variantes de declaración; 2) el paso 2 del pipeline con cada una (Elis 4.14: C48 migrado 108 frente a
82,933 declarado); 3) `cambiar_base preparar` con variantes de «entrada_efectiva» y de las listas de N5."""
import copy, json, os, shutil, subprocess, sys, tempfile

PV = os.environ.get("PV", "/tmp/rev_fable3/congelado3/personaje_v2")
V2 = os.path.dirname(PV)
STUB = os.path.join(os.environ.get("TMPDIR", "/tmp/rev_fable3/tmp"), "stub_bin")
os.makedirs(STUB, exist_ok=True)
for b in ("soffice", "libreoffice"):
    open(os.path.join(STUB, b), "w").write("#!/bin/sh\necho 'sustituto del revisor: LibreOffice no se ejecuta en esta sonda' >&2\nexit 1\n")
    os.chmod(os.path.join(STUB, b), 0o755)
os.environ["PATH"] = STUB + os.pathsep + os.environ["PATH"]
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(PV, "scripts"))
import pipeline as PL  # noqa: E402
import config_v2  # noqa: E402
from v63_xml import LibroV63  # noqa: E402

W = tempfile.mkdtemp(prefix="rev_fable_modo_")
ELIS = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_14", "elis_decisiones", "Elis")


def modo(d):
    try:
        return PL.modo_entrada_efectiva(d)
    except Exception as ex:  # noqa: BLE001
        return f"{type(ex).__name__}: {ex}"


print("=== 1 · pipeline.modo_entrada_efectiva")
VARIANTES = [
    ("sin ninguna declaración", None, None),
    ("entrada_efectiva.json {modo: estricta}", {"modo": "estricta"}, None),
    ("entrada_efectiva.json {modo: Estricta} (mayúscula)", {"modo": "Estricta"}, None),
    ("entrada_efectiva.json {modo: ESTRICTA}", {"modo": "ESTRICTA"}, None),
    ("entrada_efectiva.json {modo: 'estricta '} (espacio final)", {"modo": "estricta "}, None),
    ("entrada_efectiva.json {MODO: estricta} (clave en mayúsculas)", {"MODO": "estricta"}, None),
    ("entrada_efectiva.json {modo: registrada} sin motivo", {"modo": "registrada"}, None),
    ("entrada_efectiva.json {modo: registrada, motivo: '  '}", {"modo": "registrada", "motivo": "  "}, None),
    ("entrada_efectiva.json {modo: registrada, motivo: x}", {"modo": "registrada", "motivo": "x"}, None),
    ("entrada_efectiva.json = [] (lista)", [], None),
    ("entrada_efectiva.json ilegible", "{ilegible", None),
    ("entrada_efectiva.json vacío (0 bytes)", "", None),
    ("solo alcance_v2.json {entrada_efectiva: estricta}", None, {"entrada_efectiva": "estricta"}),
    ("solo alcance_v2.json {entrada_efectiva: Estricta} (mayúscula)", None, {"entrada_efectiva": "Estricta"}),
    ("solo alcance_v2.json {entrada_efectiva: estricto} (errata)", None, {"entrada_efectiva": "estricto"}),
    ("solo alcance_v2.json {entrada_efectiva: {modo: estricta}} (forma del archivo nuevo)", None, {"entrada_efectiva": {"modo": "estricta"}}),
    ("solo alcance_v2.json ilegible", None, "{ilegible"),
    ("entrada_efectiva.json {modo: registrada, motivo: x} + alcance {entrada_efectiva: estricta} (contradictorios)", {"modo": "registrada", "motivo": "x"}, {"entrada_efectiva": "estricta"}),
]


def declarar(d, ee, alc):
    for n, v in (("entrada_efectiva.json", ee), ("alcance_v2.json", alc)):
        p = os.path.join(d, n)
        if os.path.lexists(p):
            os.remove(p)
        if v is None:
            continue
        if isinstance(v, str):
            open(p, "w", encoding="utf-8").write(v)
        else:
            json.dump(v if n != "alcance_v2.json" else dict({"tipo": "ensayo_exploratorio", "aviso": "x", "fuente": "x"}, **v), open(p, "w", encoding="utf-8"), ensure_ascii=False)


dm = os.path.join(W, "modo"); os.makedirs(dm)
for rot, ee, alc in VARIANTES:
    declarar(dm, ee, alc)
    print(f"   {rot}: {modo(dm)}")
declarar(dm, None, None)
os.symlink(os.path.join(dm, "no_existe.json"), os.path.join(dm, "entrada_efectiva.json"))
print(f"   entrada_efectiva.json es un enlace simbólico roto: {modo(dm)}")
os.remove(os.path.join(dm, "entrada_efectiva.json")); os.makedirs(os.path.join(dm, "entrada_efectiva.json"))
print(f"   entrada_efectiva.json es una carpeta: {modo(dm)}")
os.rmdir(os.path.join(dm, "entrada_efectiva.json"))
json.dump({"modo": "estricta"}, open(os.path.join(dm, "Entrada_Efectiva.json"), "w"))
print(f"   el archivo se llama Entrada_Efectiva.json (mayúsculas en el nombre): {modo(dm)}")

print("\n=== 2 · pasos 1–2 del Pipeline real (sin LibreOffice) · Elis 4.14: C48 migrado 108 frente a 82,933 declarado en fase1_v63.json")
cfg = config_v2.cargar(os.path.join(PV, "config_v2.json"))
os.environ["MUNGER_CONFIG"] = cfg["_ruta_config"]


def expediente(nombre):
    d = os.path.join(W, nombre, "Elis")
    os.makedirs(d)
    for n in ("etapa1", "fase1_v63.json", "fase1_metadatos.json", "fase1_partes", "fase1_fuentes.json"):
        s = os.path.join(ELIS, n)
        (shutil.copytree if os.path.isdir(s) else shutil.copy)(s, os.path.join(d, n))
    return d


def pasos_1_2(d):
    p = PL.Pipeline(d, cfg)
    p.st["paso"] = 1
    try:
        p.correr(hasta=2)
    except Exception as ex:  # noqa: BLE001
        return f"EXCEPCIÓN {type(ex).__name__}: {str(ex)[:200]}"
    datos = os.path.join(d, "Elis_v63_datos.xlsx")
    reg = os.path.join(d, "Elis_v63_datos.xlsx.fase1.registro.json")
    mig = (json.load(open(reg, encoding="utf-8")).get("entradas_migradas_distintas") if os.path.exists(reg) else None)
    dg = json.load(open(os.path.join(d, "diagnostico.json"), encoding="utf-8")) if os.path.exists(os.path.join(d, "diagnostico.json")) else {}
    orden = [h.strip()[:150] for h in p.st["historial"] if "rellenar_fase1_v63.py" in h]
    return (f"estado {p.st.get('estado_analisis')!r} · paso {p.st.get('paso')} · libro de datos escrito: {os.path.exists(datos)}"
            + (f" · C48 = {LibroV63(datos).leer('Análisis', 'C48')!r}" if os.path.exists(datos) else "")
            + f" · entradas_migradas_distintas: {[(x['celda'].split('!')[1], x['libro'], x['fase1_v63']) for x in mig] if mig else mig}"
            + f"\n        orden registrada: {orden}\n        diagnóstico: {str((dg.get('causa') or {}).get('detalle'))[:230]}")


for rot, ee, alc in VARIANTES:
    d = expediente("p_" + str(VARIANTES.index((rot, ee, alc))))
    declarar(d, ee, alc)
    print(f"[{rot}] modo → {modo(d)}\n      {pasos_1_2(d)}")

print("\n=== 3 · cambiar_base preparar (CAMBIO 4.15 de Elis) con variantes de «entrada_efectiva» y de las listas")
CAMBIO = json.load(open(os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_15", "configuracion", "cambio_elis_c48_4_15.json"), encoding="utf-8"))


def preparar(nombre, **cambios):
    dd = dict(copy.deepcopy(CAMBIO), origen=os.path.join(V2, CAMBIO["origen"]), destino=os.path.join(W, nombre))
    dd.update(cambios)
    pth = os.path.join(W, f"{nombre}.json")
    json.dump(dd, open(pth, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    r = subprocess.run([sys.executable, "-B", os.path.join(PV, "scripts", "cambiar_base.py"), "preparar", pth], capture_output=True, text=True, cwd=V2)
    d = os.path.join(W, nombre, "Elis")
    ee = json.load(open(os.path.join(d, "entrada_efectiva.json"), encoding="utf-8")) if os.path.exists(os.path.join(d, "entrada_efectiva.json")) else None
    return r.returncode, (r.stdout + r.stderr).strip(), d, ee


rc, out, dA, ee = preparar("A")
print(f"[A · CAMBIO 4.15 de Elis sin «entrada_efectiva»] rc {rc} · entrada_efectiva.json: {ee}")
print("      línea del registro .md:", [l for l in out.splitlines() if "Entrada efectiva" in l][:1])
if rc == 0:
    print(f"      pasos 1–2 del Pipeline sobre el expediente nuevo: modo → {modo(dA)}\n      {pasos_1_2(dA)}")
    # el mismo expediente nuevo con la etapa 1 ORIGINAL (C48 = 108 migrado) y una declaración sin cálculo distinta: el modo estricto debe detenerlo
    dA2 = os.path.join(W, "A2", "Elis"); shutil.copytree(dA, dA2, ignore=shutil.ignore_patterns("Elis_v63_*", "estado_pipeline.json", "diagnostico*", "ficha*", "informe*", "*.csv"))
    f1 = json.load(open(os.path.join(dA2, "fase1_v63.json"), encoding="utf-8")); f1["analisis"]["C48"] = {"valor": 82.933, "fuente": "(sonda) media 2023–2025 de la Historia", "pagina": 1}
    json.dump(f1, open(os.path.join(dA2, "fase1_v63.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    xl = lambda d_: next(os.path.join(d_, "etapa1", f) for f in sorted(os.listdir(os.path.join(d_, "etapa1"))) if f.endswith(".xlsx"))  # noqa: E731
    shutil.copy(xl(ELIS), xl(dA2))
    print(f"      ídem con la etapa 1 original (108 migrado) y fase1_v63.json declarando 82,933: modo → {modo(dA2)}\n      {pasos_1_2(dA2)}")
    os.remove(os.path.join(dA2, "entrada_efectiva.json"))
    for n in os.listdir(dA2):
        if n.startswith(("Elis_v63_", "estado_pipeline", "diagnostico", "ficha", "informe")):
            os.remove(os.path.join(dA2, n))
    print(f"      ídem BORRANDO entrada_efectiva.json del expediente nuevo (queda el alcance_v2.json del CAMBIO): modo → {modo(dA2)}\n      {pasos_1_2(dA2)}")
for rot, ee_c in (("{modo: Estricta}", {"modo": "Estricta"}), ("'estricta' (texto, no objeto)", "estricta"), ("{} (objeto vacío)", {}), ("{modo: registrada}", {"modo": "registrada"}),
                  ("{modo: registrada, motivo: ' '}", {"modo": "registrada", "motivo": " "}), ("{modo: registrada, motivo: x}", {"modo": "registrada", "motivo": "x"}),
                  ("{modo: estricta, motivo: 7}", {"modo": "estricta", "motivo": 7})):
    rc, out, d, ee = preparar("ee_" + str(abs(hash(rot)) % 10000), entrada_efectiva=ee_c)
    print(f"[entrada_efectiva = {rot}] rc {rc} · {'entrada_efectiva.json: ' + str(ee) if rc == 0 else out[-170:]} · destino creado: {os.path.exists(d)}")
for rot, cambios in (("analisis_que_se_conservan = lista", {"analisis_que_se_conservan": ["C24"]}),
                     ("analisis_que_se_descartan con una celda que nadie declara (Z99)", {"analisis_que_se_descartan": dict(CAMBIO.get("analisis_que_se_descartan") or {}, Z99="(sonda) no existe")}),
                     ("motivo no textual (true) en analisis_que_se_descartan", {"analisis_que_se_descartan": dict(CAMBIO.get("analisis_que_se_descartan") or {}, C49=True)})):
    rc, out, d, ee = preparar("l_" + str(abs(hash(rot)) % 10000), **cambios)
    regc = json.load(open(os.path.join(os.path.dirname(d), "resultados", "cambio_de_base.json"), encoding="utf-8")) if rc == 0 else {}
    print(f"[{rot}] rc {rc} · {('analisis_descartadas del registro: ' + str(regc.get('analisis_descartadas'))[:200]) if rc == 0 else out[-200:]}")
shutil.rmtree(W, ignore_errors=True)
