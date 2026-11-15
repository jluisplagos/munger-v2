"""Cuarta pasada · T5 (el modo de la entrada efectiva queda también en fase1_metadatos.json: falta o contradicción → error; otra grafía →
error; errata en alcance_v2.json → error; modo en estado_pipeline.json). Sin LibreOffice: solo los pasos 1 (migración) y 2 (relleno) del
Pipeline real, con `soffice` sustituido en el PATH por un sustituto que termina con 1 (como q7).
1) pipeline.modo_entrada_efectiva con variantes de fase1_metadatos.json, del archivo y de su nombre.
2) paso 2 del Pipeline sobre el expediente nuevo de `cambiar_base preparar` (CAMBIO 4.15 de Elis), al que se repone la etapa 1 original
   (C48 = 108 migrado) y una declaración de 82,933 para crear el conflicto: intacto, sin el archivo, sin el archivo ni la clave, etc."""
import copy, json, os, shutil, subprocess, sys, tempfile

PV = os.environ.get("PV", "/tmp/rev_fable4/congelado4/personaje_v2")
V2 = os.path.dirname(PV)
STUB = os.path.join(os.environ.get("TMPDIR", "/tmp/rev_fable4/tmp"), "stub_bin")
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

W = tempfile.mkdtemp(prefix="rev_fable_modo4_")
ELIS = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_14", "elis_decisiones", "Elis")
print("árbol:", PV)


def modo(d):
    try:
        return PL.modo_entrada_efectiva(d)
    except Exception as ex:  # noqa: BLE001
        return f"{type(ex).__name__}: {ex}"


def poner(d, nombre, v):
    p = os.path.join(d, nombre)
    if os.path.lexists(p):
        os.remove(p)
    if v is None:
        return
    if isinstance(v, str):
        open(p, "w", encoding="utf-8").write(v)
    else:
        json.dump(v, open(p, "w", encoding="utf-8"), ensure_ascii=False)


print("\n=== 1 · pipeline.modo_entrada_efectiva (fase1_metadatos.json · entrada_efectiva.json · alcance_v2.json)")
ALC = {"tipo": "ensayo_exploratorio", "aviso": "x", "fuente": "x"}
E, R = {"modo": "estricta"}, {"modo": "registrada", "motivo": "x"}
VAR = [
    ("metadatos registra «estricta» y el archivo dice «estricta»", {"entrada_efectiva": "estricta"}, E, None),
    ("metadatos registra «estricta» y FALTA el archivo", {"entrada_efectiva": "estricta"}, None, None),
    ("metadatos registra «estricta» y el archivo dice «registrada» con motivo", {"entrada_efectiva": "estricta"}, R, None),
    ("metadatos registra «Estricta» (errata) y el archivo dice «estricta»", {"entrada_efectiva": "Estricta"}, E, None),
    ("metadatos registra «registrada» y el archivo dice «registrada» con motivo «x»", {"entrada_efectiva": "registrada"}, R, None),
    ("metadatos registra «» (vacío) y falta el archivo", {"entrada_efectiva": ""}, None, None),
    ("metadatos SIN la clave y falta el archivo (los dos rastros retirados)", {"empresa": "x"}, None, None),
    ("metadatos ILEGIBLE y falta el archivo", "{ilegible", None, None),
    ("metadatos es una lista y falta el archivo", [{"entrada_efectiva": "estricta"}], None, None),
    ("metadatos con la clave en otra grafía («Entrada_Efectiva») y falta el archivo", {"Entrada_Efectiva": "estricta"}, None, None),
    ("metadatos registra «estricta», falta el archivo y el alcance dice «estricta»", {"entrada_efectiva": "estricta"}, None, dict(ALC, entrada_efectiva="estricta")),
    ("sin metadatos; archivo «registrada» con motivo y alcance «estricta» (contradictorios)", None, R, dict(ALC, entrada_efectiva="estricta")),
    ("sin metadatos; alcance ILEGIBLE", None, None, "{ilegible"),
    ("sin metadatos; alcance con la clave en otra grafía («entrada_efectiba»)", None, None, dict(ALC, entrada_efectiba="estricta")),
    ("sin metadatos; alcance es una lista", None, None, [dict(ALC, entrada_efectiva="estricta")]),
]
dm = os.path.join(W, "modo"); os.makedirs(dm)
for rot, meta, ee, alc in VAR:
    poner(dm, "fase1_metadatos.json", meta); poner(dm, "entrada_efectiva.json", ee); poner(dm, "alcance_v2.json", alc)
    print(f"   {rot}: {modo(dm)}")
for n in ("fase1_metadatos.json", "entrada_efectiva.json", "alcance_v2.json"):
    poner(dm, n, None)
for otro in ("Entrada_Efectiva.json", "entrada_efectiva.JSON", "entrada-efectiva.json", "entrada_efectiva.json.bak", "entrada_efectiva .json", "entradaefectiva.json", "entrada_efectiva.json.txt"):
    poner(dm, otro, E)
    print(f"   sin metadatos; la declaración «estricta» está en un archivo llamado {otro!r}: {modo(dm)}")
    os.remove(os.path.join(dm, otro))

print("\n=== 2 · paso 2 del Pipeline real sobre el expediente nuevo de cambiar_base (estricto por defecto), con el conflicto de C48 repuesto")
cfg = config_v2.cargar(os.path.join(PV, "config_v2.json"))
os.environ["MUNGER_CONFIG"] = cfg["_ruta_config"]
CAMBIO = json.load(open(os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_15", "configuracion", "cambio_elis_c48_4_15.json"), encoding="utf-8"))
dd = dict(copy.deepcopy(CAMBIO), origen=os.path.join(V2, CAMBIO["origen"]), destino=os.path.join(W, "A"))
json.dump(dd, open(os.path.join(W, "A.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
r = subprocess.run([sys.executable, "-B", os.path.join(PV, "scripts", "cambiar_base.py"), "preparar", os.path.join(W, "A.json")], capture_output=True, text=True, cwd=V2)
dA = os.path.join(W, "A", "Elis")
print("cambiar_base preparar → rc", r.returncode)
meta = json.load(open(os.path.join(dA, "fase1_metadatos.json"), encoding="utf-8"))
print("   entrada_efectiva.json:", json.load(open(os.path.join(dA, "entrada_efectiva.json"), encoding="utf-8")))
print("   fase1_metadatos.json → «entrada_efectiva»:", repr(meta.get("entrada_efectiva")), "| alcance_v2.json → «entrada_efectiva»:",
      repr(json.load(open(os.path.join(dA, "alcance_v2.json"), encoding="utf-8")).get("entrada_efectiva", "(sin la clave)")))
xl = lambda d_: next(os.path.join(d_, "etapa1", f) for f in sorted(os.listdir(os.path.join(d_, "etapa1"))) if f.endswith(".xlsx"))  # noqa: E731


def expediente(nombre):
    d = os.path.join(W, nombre, "Elis")
    shutil.copytree(dA, d, ignore=shutil.ignore_patterns("Elis_v63_*", "estado_pipeline.json", "diagnostico*", "ficha*", "informe*", "*.csv"))
    f1 = json.load(open(os.path.join(d, "fase1_v63.json"), encoding="utf-8"))
    f1["analisis"]["C48"] = {"valor": 82.933, "fuente": "(sonda) media 2023–2025 de la Historia", "pagina": 1}
    json.dump(f1, open(os.path.join(d, "fase1_v63.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    shutil.copy(xl(ELIS), xl(d))
    return d


def pasos_1_2(d):
    p = PL.Pipeline(d, cfg)
    p.st["paso"] = 1
    try:
        p.correr(hasta=2)
    except Exception as ex:  # noqa: BLE001
        return f"EXCEPCIÓN {type(ex).__name__}: {str(ex)[:200]}"
    datos = os.path.join(d, "Elis_v63_datos.xlsx")
    est = json.load(open(os.path.join(d, "estado_pipeline.json"), encoding="utf-8")) if os.path.exists(os.path.join(d, "estado_pipeline.json")) else {}
    dg = json.load(open(os.path.join(d, "diagnostico.json"), encoding="utf-8")) if os.path.exists(os.path.join(d, "diagnostico.json")) else {}
    orden = [h.strip()[:120] for h in p.st["historial"] if "rellenar_fase1_v63.py" in h]
    return (f"estado {p.st.get('estado_analisis')!r} · paso {p.st.get('paso')} · libro de datos escrito: {os.path.exists(datos)}"
            + (f" · C48 = {LibroV63(datos).leer('Análisis', 'C48')!r}" if os.path.exists(datos) else "")
            + f"\n        estado_pipeline.json → «entrada_efectiva»: {est.get('entrada_efectiva', '(sin la clave)')}"
            + f"\n        orden registrada: {orden}\n        diagnóstico: {str((dg.get('causa') or {}).get('detalle'))[:200]}")


def sin_clave(d):
    m = json.load(open(os.path.join(d, "fase1_metadatos.json"), encoding="utf-8"))
    m.pop("entrada_efectiva", None)
    json.dump(m, open(os.path.join(d, "fase1_metadatos.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def con_clave(d, v):
    m = json.load(open(os.path.join(d, "fase1_metadatos.json"), encoding="utf-8"))
    m["entrada_efectiva"] = v
    json.dump(m, open(os.path.join(d, "fase1_metadatos.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)


CASOS = [
    ("intacto (control: estricto, se detiene con el código 7)", lambda d: None),
    ("se BORRA entrada_efectiva.json", lambda d: os.remove(os.path.join(d, "entrada_efectiva.json"))),
    ("se borra entrada_efectiva.json Y la clave «entrada_efectiva» de fase1_metadatos.json", lambda d: (os.remove(os.path.join(d, "entrada_efectiva.json")), sin_clave(d))),
    ("se borra entrada_efectiva.json y fase1_metadatos.json queda ILEGIBLE", lambda d: (os.remove(os.path.join(d, "entrada_efectiva.json")), open(os.path.join(d, "fase1_metadatos.json"), "w").write("{ilegible"))),
    ("se borra entrada_efectiva.json y se BORRA fase1_metadatos.json", lambda d: (os.remove(os.path.join(d, "entrada_efectiva.json")), os.remove(os.path.join(d, "fase1_metadatos.json")))),
    ("el archivo pasa a «registrada» con motivo «x» (metadatos sigue en «estricta»)", lambda d: poner(d, "entrada_efectiva.json", R)),
    ("el archivo Y los metadatos pasan a «registrada» (motivo «x»)", lambda d: (poner(d, "entrada_efectiva.json", R), con_clave(d, "registrada"))),
    ("el archivo se renombra a entrada_efectiva.json.bak", lambda d: os.rename(os.path.join(d, "entrada_efectiva.json"), os.path.join(d, "entrada_efectiva.json.bak"))),
]
for i, (rot, cambio) in enumerate(CASOS):
    d = expediente(f"c{i}")
    cambio(d)
    print(f"[{rot}] modo → {modo(d)}\n      {pasos_1_2(d)}")
shutil.rmtree(W, ignore_errors=True)
