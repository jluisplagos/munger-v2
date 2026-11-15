"""Cuarta pasada · caso nuevo del grupo D de test_integracion_v64.py («el mismo CAMBIO sin declarar el modo: entrada efectiva
«estricta»; el paso 2 se detiene por C50 (rellenar --estricta → 7) sin escribir el libro de datos»), ejecutado SIN LibreOffice: las mismas
órdenes que la batería (cambiar_base.py preparar + pipeline.py --hasta 4), con `soffice` sustituido en el PATH por un sustituto que
termina con 1 (si el paso 2 no se detuviera, el paso 3 fallaría sin arrancar LibreOffice). Se evalúa la misma expresión que la batería.
También el caso de concordancia con el modo «registrada» declarado (solo la preparación y los pasos 1–2)."""
import copy, json, os, subprocess, sys, tempfile

PV = os.environ.get("PV", "/tmp/rev_fable4/congelado4/personaje_v2")
RAIZ = os.path.dirname(PV)
ENS = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_11")
CFG64 = os.path.join(PV, "config_v2_v64_experimental.json")
PIPE = os.path.join(PV, "scripts", "pipeline.py")
PY = sys.executable
STUB = os.path.join(os.environ.get("TMPDIR", "/tmp/rev_fable4/tmp"), "stub_bin")
os.makedirs(STUB, exist_ok=True)
for b in ("soffice", "libreoffice"):
    open(os.path.join(STUB, b), "w").write("#!/bin/sh\necho 'sustituto del revisor: LibreOffice no se ejecuta en esta sonda' >&2\nexit 1\n")
    os.chmod(os.path.join(STUB, b), 0o755)
ENV = dict(os.environ, PATH=STUB + os.pathsep + os.environ["PATH"], PYTHONDONTWRITEBYTECODE="1")
base = tempfile.mkdtemp(prefix="rev_fable_d_")
print("árbol:", PV)


def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, env=ENV, **kw)
    return r.returncode, r.stdout + r.stderr


conf0 = json.load(open(os.path.join(ENS, "configuracion", "cambio_de_base_control_heredado.json"), encoding="utf-8"))
print("CAMBIO del control heredado: «entrada_efectiva» =", conf0.get("entrada_efectiva", "(no la declara)"))
MOTIVO_REG = ("(4.15) control heredado de la 4.11: C50 de Vidrala lo sostiene solo la etapa 1 (no reproducible, lo bloquea el comprobador "
              "de entradas); este caso prueba la concordancia del cambio de base")
for nombre, ee in (("tres", None), ("uno", {"modo": "registrada", "motivo": MOTIVO_REG})):
    conf = copy.deepcopy(conf0)
    if ee:
        conf["entrada_efectiva"] = ee
    conf["destino"] = os.path.join(base, nombre)
    p = os.path.join(base, f"cfg_{nombre}", "cambio_de_base.json")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    json.dump(conf, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    rc, out = run([PY, "-I", os.path.join(PV, "scripts", "cambiar_base.py"), "preparar", p], cwd=RAIZ, timeout=900)
    d = os.path.join(base, nombre, "Vidrala")
    est = {}
    print(f"\n[{nombre} · entrada_efectiva del CAMBIO: {ee or '(sin declarar)'}] cambiar_base preparar → rc {rc}" + ("" if rc == 0 else " · " + out[-300:]))
    if rc == 0:
        print("   entrada_efectiva.json:", {k: v for k, v in json.load(open(os.path.join(d, "entrada_efectiva.json"), encoding="utf-8")).items() if k in ("modo", "motivo")},
              "| fase1_metadatos.json:", repr(json.load(open(os.path.join(d, "fase1_metadatos.json"), encoding="utf-8")).get("entrada_efectiva")))
        rcp, outp = run([PY, PIPE, d, "--config", CFG64, "--hasta", "2" if ee else "4"], timeout=900)
        try:
            est = json.load(open(os.path.join(d, "estado_pipeline.json"), encoding="utf-8"))
        except (OSError, ValueError):
            est = {}
        print(f"   pipeline --hasta {'2' if ee else '4'} → rc {rcp} · paso {est.get('paso')} · estado {est.get('estado_analisis')!r} · entrada_efectiva {est.get('entrada_efectiva')}")
    hist = " ".join(est.get("historial") or [])
    print("   historial (relleno):", [h.strip()[:260] for h in est.get("historial") or [] if "rellenar_fase1_v63.py" in h])
    print("   libro de datos escrito:", os.path.exists(os.path.join(d, "Vidrala_v63_datos.xlsx")), "| LibreOffice invocado (sustituto) en el historial:", "sustituto del revisor" in hist or "soffice" in hist)
    if not ee:
        ok = (rc == 0 and est.get("paso") == 2 and (est.get("entrada_efectiva") or {}).get("modo") == "estricta" and "--estricta → 7" in hist and "Análisis!C50" in hist
              and not os.path.exists(os.path.join(d, "Vidrala_v63_datos.xlsx")))
        print("   EXPRESIÓN DEL CASO NUEVO DE LA BATERÍA (grupo D):", "PASA" if ok else "FALLA")
import shutil
shutil.rmtree(base, ignore_errors=True)
