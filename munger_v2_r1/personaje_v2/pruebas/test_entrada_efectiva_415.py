"""Batería de la entrada efectiva del FCF base (4.15; encargo correctivo §3: C48 de Elis). No ejecuta LibreOffice.

El defecto (I12): el libro de Elis conserva Análisis!C48 = 108 (intereses financieros netos + intereses de arrendamientos, tratamiento
del inversor) solo porque rellenar_fase1_v63.py no pisa un valor migrado de la etapa 1; fase1_v63.json, que es la entrada declarada,
reconstruye 82,933. Regenerado sin ese valor migrado, el precio de Sí sube +1,678 € sin que nadie lo decida.
Casos:
  C · fase1_historia.calcular_entrada: el cálculo declarado (Historia + componentes con fuente y página) da 108,0; errores explícitos.
  F · fase1_historia construir: una entrada de fase1_metadatos.json con `calculo` sale en fase1_v63.json con su valor y su fuente.
  R · rellenar_fase1_v63: la entrada migrada que contradice la declarada se conserva (regla v2.2) pero ya no en silencio: queda registrada
      y el comprobador de entradas la marca como no reproducible; --sobrescribir aplica la declarada; con la declarada correcta, nada
      registrado; sin valor migrado, se escribe la declarada.
  B · cambiar_base: las entradas `analisis` del CAMBIO quedan en las entradas declaradas del expediente (fase1_metadatos.json) y C48
      se reconstruye con su cálculo desde la copia de ensayo de la etapa 1 vaciada; (segunda revisión) herencia reconocida con motivo,
      descartes, celdas en dos listas y el modo de la entrada efectiva del expediente nuevo.
  P · (segunda revisión, N7) modo de la entrada efectiva que aplica el pipeline (falla en cerrado).
Uso: python3 -B test_entrada_efectiva_415.py [--json salida.json]
"""
import argparse, copy, json, os, shutil, subprocess, sys, tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
PV = os.path.dirname(AQUI)
RAIZ = os.path.dirname(PV)
sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
sys.path.insert(0, os.path.join(PV, "scripts"))
import fase1_historia as FH  # noqa: E402
from v63_xml import LibroV63  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--json")
ARGS = ap.parse_args()
E414 = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_14")
ELIS = os.path.join(E414, "elis_decisiones", "Elis")
CAMBIO = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_15", "configuracion", "cambio_elis_c48_4_15.json")
TMP = tempfile.mkdtemp(prefix="entrada_efectiva_415_")
RES = []


def paso(grupo, nombre, ok, detalle=""):
    RES.append({"grupo": grupo, "prueba": nombre, "resultado": "PASA" if ok else "FALLA", "detalle": str(detalle)[:400]})
    print(f"[{grupo}] {'PASA ' if ok else 'FALLA'} {nombre}" + (f" · {str(detalle)[:240]}" if detalle else ""))


def error(f):
    try:
        f()
        return None
    except ValueError as ex:
        return str(ex)


f1 = json.load(open(os.path.join(ELIS, "fase1_v63.json"), encoding="utf-8"))
H, anios = f1["historia"]["partidas"], f1["historia"]["anios"]
CALC = json.load(open(CAMBIO, encoding="utf-8"))["analisis"]["C48"]["calculo"]
# ------------------------------------------------------------------ C
r = FH.calcular_entrada("C48", {"calculo": CALC}, H, anios)
paso("C", "C48 de Elis desde la Historia y los pagos de arrendamientos con intereses declarados: 108,0 (= 82,933 + 25,067)",
     r["valor"] == 108.0 and "Cálculo declarado" in r["fuente"] and r["calculo"] == CALC, r["fuente"][:160])
paso("C", "con el valor 108 declarado además del cálculo: coincide", FH.calcular_entrada("C48", {"calculo": CALC, "valor": 108}, H, anios)["valor"] == 108.0)
e = error(lambda: FH.calcular_entrada("C48", {"calculo": CALC, "valor": 82.933}, H, anios))
paso("C", "un valor declarado distinto del calculado (82,933): error explícito", bool(e) and "no es el calculado" in e, e)
c2 = copy.deepcopy(CALC); c2["componentes"]["pagos_arrendamientos_con_intereses"]["2024"].pop("pagina")
e = error(lambda: FH.calcular_entrada("C48", {"calculo": c2}, H, anios))
paso("C", "un componente sin página: error (no se acepta una cifra sin su fuente)", bool(e) and "página" in e, e)
c3 = copy.deepcopy(CALC); c3["anios"] = [2024, 2025, 2026]
e = error(lambda: FH.calcular_entrada("C48", {"calculo": c3}, H, anios))
paso("C", "un año fuera de la Historia: error", bool(e) and "fuera de la Historia" in e, e)
c4 = copy.deepcopy(CALC); c4["operacion"] = "maximo"
paso("C", "una operación no admitida: error", bool(error(lambda: FH.calcular_entrada("C48", {"calculo": c4}, H, anios))))
c5 = copy.deepcopy(CALC); c5["terminos"][0]["signo"] = 2
paso("C", "un signo distinto de ±1: error", bool(error(lambda: FH.calcular_entrada("C48", {"calculo": c5}, H, anios))))
c6 = copy.deepcopy(CALC); c6["terminos"].append({"partida": "no_existe", "signo": 1})
paso("C", "una partida que no está en la Historia: error (no se rellena con cero)", bool(error(lambda: FH.calcular_entrada("C48", {"calculo": c6}, H, anios))))
c7 = copy.deepcopy(CALC); c7["redondeo"] = 0
c8 = copy.deepcopy(CALC); c8["anios"] = [2025, 2025, 2025]
c9 = copy.deepcopy(CALC); c9["anios"] = [2023, None, 2025]
paso("C", "(revisión independiente, h13) redondeo menor que 3, años repetidos o no enteros: error explícito (no TypeError)",
     all(error(lambda cc=cc: FH.calcular_entrada("C48", {"calculo": cc}, H, anios)) for cc in (c7, c8, c9)))
c10 = copy.deepcopy(CALC); c10["anios"] = [2016, 2017, 2018]
c10["terminos"] = [{"partida": "intereses_financiacion", "signo": 1}, {"partida": "arrendamientos_principal", "signo": -1}]
r10 = FH.calcular_entrada("C48", {"calculo": c10}, H, anios)
pend_h = (H.get("arrendamientos_principal") or {}).get("pendientes_verificacion") or []
paso("C", "(h7) un cálculo sobre años con ceros pendientes de verificación (H1) los hereda en «pendiente_verificacion»",
     (not pend_h) or (r10.get("pendiente_verificacion") == sorted(set(pend_h) & {2016, 2017, 2018})), (pend_h, r10.get("pendiente_verificacion")))
c11 = copy.deepcopy(CALC); c11["componentes"]["pagos_arrendamientos_con_intereses"]["2025"]["pagina"] = 99999
paso("C", "(h13) con la carpeta del expediente, un componente cuya página no existe en su texto: error", bool(error(lambda: FH.calcular_entrada("C48", {"calculo": c11}, H, anios, ELIS))))
paso("C", "(h13) con la carpeta del expediente, los componentes reales de C48 se contrastan con su página y su cita: 108,0", FH.calcular_entrada("C48", {"calculo": CALC}, H, anios, ELIS)["valor"] == 108.0)

# ------------------------------------------------------------------ F · construir
dF = os.path.join(TMP, "construir", "Elis")
os.makedirs(dF)
for n in ("fase1_metadatos.json", "fase1_partes", "fase1_fuentes.json", "texto", "etapa1"):
    o = os.path.join(ELIS, n)
    (shutil.copytree if os.path.isdir(o) else shutil.copy2)(o, os.path.join(dF, n))
r0 = subprocess.run([sys.executable, "-B", os.path.join(PV, "scripts", "fase1_historia.py"), "construir", dF], capture_output=True, text=True)
c48_antes = (json.load(open(os.path.join(dF, "fase1_v63.json"), encoding="utf-8"))["analisis"].get("C48") or {}).get("valor") if r0.returncode == 0 else None
paso("F", "construir con los metadatos de la 4.14 (sin C48 declarada): fase1_v63.json da 82,933, la media de los intereses netos (el defecto I12)",
     r0.returncode == 0 and c48_antes == 82.933, (r0.stdout + r0.stderr)[-200:] if r0.returncode else c48_antes)
m = json.load(open(os.path.join(dF, "fase1_metadatos.json"), encoding="utf-8"))
m.setdefault("analisis", {})["C48"] = {"calculo": copy.deepcopy(CALC), "periodo": "2023–2025", "unidad": "mm"}
json.dump(m, open(os.path.join(dF, "fase1_metadatos.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
r1 = subprocess.run([sys.executable, "-B", os.path.join(PV, "scripts", "fase1_historia.py"), "construir", dF], capture_output=True, text=True)
c48 = json.load(open(os.path.join(dF, "fase1_v63.json"), encoding="utf-8"))["analisis"].get("C48") if r1.returncode == 0 else {}
paso("F", "con C48 declarada con su cálculo en fase1_metadatos.json: fase1_v63.json da 108,0 con el cálculo y su fuente",
     r1.returncode == 0 and c48.get("valor") == 108.0 and c48.get("calculo") == CALC and "Cálculo declarado" in str(c48.get("fuente")), (r1.stdout + r1.stderr)[-200:] if r1.returncode else c48.get("valor"))
m["analisis"]["C48"]["calculo"]["componentes"]["pagos_arrendamientos_con_intereses"]["2025"]["valor"] = None
json.dump(m, open(os.path.join(dF, "fase1_metadatos.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
r2 = subprocess.run([sys.executable, "-B", os.path.join(PV, "scripts", "fase1_historia.py"), "construir", dF], capture_output=True, text=True)
paso("F", "un componente sin valor: construir falla con el motivo (no escribe una media incompleta)", r2.returncode != 0 and "C48" in (r2.stdout + r2.stderr), (r2.stdout + r2.stderr)[-200:])

# ------------------------------------------------------------------ R · rellenar
REL = os.path.join(PV, "scripts", "rellenar_fase1_v63.py")
CFG = os.path.join(PV, "config_v2.json")
base = os.path.join(ELIS, "Elis_v63_base.xlsx")


def rellenar(libro, f1p, salida, *extra):
    r = subprocess.run([sys.executable, "-B", REL, libro, f1p, salida, "--config", CFG, *extra], capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def leer(libro, ref):
    return LibroV63(libro).leer("Análisis", ref)


out = os.path.join(TMP, "r1.xlsx")
rc, txt = rellenar(base, os.path.join(ELIS, "fase1_v63.json"), out)
reg = json.load(open(out + ".fase1.registro.json", encoding="utf-8"))
dist = reg.get("entradas_migradas_distintas") or []
paso("R", "libro base de Elis (C48 = 108 migrado) con el fase1_v63.json de la 4.14 (82,933): se conserva 108 (regla v2.2), pero ya no en silencio: queda registrada como entrada migrada distinta y avisada",
     rc == 0 and leer(out, "C48") == 108 and [x["celda"] for x in dist] == ["Análisis!C48"] and dist[0]["fase1_v63"] == 82.933 and "NO reproducible" in txt + " ".join(reg.get("avisos") or []), (rc, dist))
sys.path.insert(0, os.path.join(PV, "scripts"))
import verificacion_entradas as VE  # noqa: E402
rc7, txt7 = rellenar(base, os.path.join(ELIS, "fase1_v63.json"), os.path.join(TMP, "r1e.xlsx"), "--estricta")
paso("R", "el mismo caso con --estricta (modo de los expedientes nuevos): código 7 y ningún libro escrito", rc7 == 7 and not os.path.exists(os.path.join(TMP, "r1e.xlsx")), txt7[-200:])
nr = VE.entradas_no_reproducibles(ELIS, VE.universo(ELIS))
r = VE.comprobar(ELIS)
paso("R", "el comprobador de entradas marca C48 de elis_decisiones (4.14) como no reproducible por la vía generativa (y solo C48)",
     list(nr) == ["Análisis!C48"] and nr["Análisis!C48"][:2] == (108, 82.933) and any(x.startswith("Análisis!C48:") for x in r["entradas_no_reproducibles"]), r["entradas_no_reproducibles"])
rc, txt = rellenar(base, os.path.join(ELIS, "fase1_v63.json"), out, "--sobrescribir")
paso("R", "con --sobrescribir se aplica la declarada de forma explícita (82,933)", rc == 0 and leer(out, "C48") == 82.933, (rc, leer(out, "C48") if os.path.exists(out) else None))
f1_ok = copy.deepcopy(f1)
f1_ok["analisis"]["C48"] = FH.calcular_entrada("C48", {"calculo": CALC}, H, anios)
p_ok = os.path.join(TMP, "fase1_ok.json")
json.dump(f1_ok, open(p_ok, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
out2 = os.path.join(TMP, "r2.xlsx")
rc, txt = rellenar(base, p_ok, out2)
reg2 = json.load(open(out2 + ".fase1.registro.json", encoding="utf-8"))
paso("R", "con la entrada efectiva declarada (108,0 con su cálculo): C48 = 108 y ninguna entrada migrada distinta", rc == 0 and leer(out2, "C48") == 108 and not reg2.get("entradas_migradas_distintas"), (rc, txt[-200:]))
vacio = os.path.join(TMP, "base_sin_migrados.xlsx")
lb = LibroV63(base)
lb.escribir_celdas({f"Análisis!{c}": None for c in ("C46", "C47", "C48", "C49", "C50")})
lb.guardar(vacio)
out3, out4 = os.path.join(TMP, "r3.xlsx"), os.path.join(TMP, "r4.xlsx")
rc3, _ = rellenar(vacio, os.path.join(ELIS, "fase1_v63.json"), out3)
rc4, _ = rellenar(vacio, p_ok, out4)
paso("R", "sin el valor migrado: con la declaración de la 4.14 sale 82,933 (el riesgo I12, ahora visible); con la entrada efectiva declarada sale 108",
     rc3 == 0 and leer(out3, "C48") == 82.933 and rc4 == 0 and leer(out4, "C48") == 108, (rc3, leer(out3, "C48") if rc3 == 0 else None, rc4, leer(out4, "C48") if rc4 == 0 else None))
for x, nom in (("viscofan_decisiones", "Viscofan"), ("vidrala_decisiones", "Vidrala")):
    e = os.path.join(E414, x, nom)
    cfg = os.path.join(PV, json.load(open(os.path.join(e, "plantilla_activa.json"), encoding="utf-8"))["config"])
    o = os.path.join(TMP, f"{nom}.xlsx")
    r = subprocess.run([sys.executable, "-B", REL, os.path.join(e, f"{nom}_v63_base.xlsx"), os.path.join(e, "fase1_v63.json"), o, "--config", cfg], capture_output=True, text=True)
    rg = json.load(open(o + ".fase1.registro.json", encoding="utf-8")) if os.path.exists(o + ".fase1.registro.json") else {}
    esperado = {"Viscofan": [], "Vidrala": ["Análisis!C50"]}[nom]  # (revisión independiente, hallazgo 4) Vidrala C50 = 0 lo sostiene solo la etapa 1
    md = [x["celda"] for x in rg.get("entradas_migradas_distintas") or []]
    paso("R", f"{nom} (expediente final de la 4.14): entradas del FCF base que solo sostiene la etapa 1 = {esperado or 'ninguna'} (registro de rellenar y comprobador de entradas)",
         r.returncode == 0 and md == esperado and sorted(VE.entradas_no_reproducibles(e, VE.universo(e))) == esperado, (md, (r.stdout + r.stderr)[-160:]))
    if esperado:
        r7 = subprocess.run([sys.executable, "-B", REL, os.path.join(e, f"{nom}_v63_base.xlsx"), os.path.join(e, "fase1_v63.json"), o + ".estricta.xlsx", "--config", cfg, "--estricta"],
                            capture_output=True, text=True)
        paso("R", f"{nom} con --estricta (modo de los expedientes nuevos): código 7 y ningún libro escrito", r7.returncode == 7 and not os.path.exists(o + ".estricta.xlsx"), (r7.stdout + r7.stderr)[-200:])

# ------------------------------------------------------------------ B · cambiar_base
d = json.load(open(CAMBIO, encoding="utf-8"))
d["destino"] = os.path.join(TMP, "cambio", "ensayo")
cp = os.path.join(TMP, "cambio.json")
json.dump(d, open(cp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
r = subprocess.run([sys.executable, "-B", os.path.join(PV, "scripts", "cambiar_base.py"), "preparar", cp], capture_output=True, text=True, cwd=RAIZ)
dest = os.path.join(TMP, "cambio", "ensayo", "Elis")
ok = r.returncode == 0 and os.path.isdir(dest)
meta = json.load(open(os.path.join(dest, "fase1_metadatos.json"), encoding="utf-8")) if ok else {}
f1n = json.load(open(os.path.join(dest, "fase1_v63.json"), encoding="utf-8")) if ok else {}
paso("B", "cambiar_base con el CAMBIO 4.15: las entradas `analisis` del CAMBIO quedan en fase1_metadatos.json (entradas declaradas), C48 con su cálculo",
     ok and (meta.get("analisis") or {}).get("C48", {}).get("calculo") == CALC and set(d["analisis"]) <= set(meta.get("analisis") or {}), (r.stdout + r.stderr)[-200:] if not ok else sorted(meta.get("analisis") or {}))
e1 = [f for f in os.listdir(os.path.join(dest, "etapa1")) if f.endswith(".xlsx")] if ok else []
paso("B", "fase1_v63.json del expediente nuevo: C48 = 108,0 calculado; la copia de ensayo de la etapa 1 tiene C48 vacía (la entrada no depende del valor migrado)",
     ok and (f1n.get("analisis") or {}).get("C48", {}).get("valor") == 108.0 and e1 and LibroV63(os.path.join(dest, "etapa1", e1[0])).leer("Análisis", "C48") in (None, ""),
     (f1n.get("analisis") or {}).get("C48", {}).get("valor") if ok else None)
dR = os.path.join(TMP, "reconstr", "Elis")
os.makedirs(dR)
for n in ("fase1_metadatos.json", "fase1_partes", "fase1_fuentes.json", "texto", "etapa1"):
    o = os.path.join(dest, n)
    if os.path.exists(o):
        (shutil.copytree if os.path.isdir(o) else shutil.copy2)(o, os.path.join(dR, n))
r = subprocess.run([sys.executable, "-B", os.path.join(PV, "scripts", "fase1_historia.py"), "construir", dR], capture_output=True, text=True)
f1r = json.load(open(os.path.join(dR, "fase1_v63.json"), encoding="utf-8")) if r.returncode == 0 else {}
v = lambda x: x.get("valor") if isinstance(x, dict) else x  # noqa: E731
dif = [c for c in set(f1n.get("analisis") or {}) | set(f1r.get("analisis") or {}) if v((f1n.get("analisis") or {}).get(c)) != v((f1r.get("analisis") or {}).get(c))]
paso("B", "en una carpeta limpia, construir con las entradas declaradas del expediente nuevo reproduce todas sus entradas de Análisis (sin el CAMBIO)",
     r.returncode == 0 and not dif and f1r["historia"] == f1n["historia"], dif or (r.stdout + r.stderr)[-200:])

# ------------------------------------------------------------------ B2 · segunda revisión independiente (N5, N7)
ee = json.load(open(os.path.join(dest, "entrada_efectiva.json"), encoding="utf-8")) if ok else {}
regc = json.load(open(os.path.join(TMP, "cambio", "ensayo", "resultados", "cambio_de_base.json"), encoding="utf-8")) if ok else {}
paso("B", "(N7) el expediente nuevo declara su entrada efectiva «estricta» (entrada_efectiva.json) y el registro del cambio lo dice",
     ee.get("modo") == "estricta" and (regc.get("entrada_efectiva") or {}).get("modo") == "estricta", ee)
mA = (meta.get("analisis") or {}) if ok else {}


def preparar2(nombre, **cambios):
    dd = dict(copy.deepcopy(d), origen=dest, destino=os.path.join(TMP, nombre, "ensayo"), analisis={}, evidencia={}, correcciones_fase1_partes=[])
    dd.update(cambios)
    pp = os.path.join(TMP, f"{nombre}.json")
    json.dump(dd, open(pp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    rr = subprocess.run([sys.executable, "-B", os.path.join(PV, "scripts", "cambiar_base.py"), "preparar", pp], capture_output=True, text=True, cwd=RAIZ)
    return rr.returncode, rr.stdout + rr.stderr, os.path.join(TMP, nombre, "ensayo")


rc, out, ens = preparar2("b_vacio", analisis_que_se_conservan={c: "" for c in mA})
paso("B", "(N5) reconocer entradas heredadas con un motivo vacío: rechazado antes de crear nada", rc != 0 and "sin motivo" in out and not os.path.exists(os.path.join(ens, "Elis")), out.strip()[-160:])
rc, out, ens = preparar2("b_doble", analisis_que_se_conservan={c: "(prueba) se conserva" for c in mA}, analisis_que_se_descartan={"C42": "(prueba) se descarta"})
paso("B", "(N5) una celda a la vez conservada y descartada: rechazado", rc != 0 and "a la vez" in out and not os.path.exists(os.path.join(ens, "Elis")), out.strip()[-160:])
rc, out, ens = preparar2("b_ajena", analisis_que_se_conservan=dict({c: "(prueba) se conserva" for c in mA}, Z99="(prueba) no se hereda"))
paso("B", "(N5) reconocer una entrada que el origen no declara: preparación detenida, destino retirado", rc != 0 and "Z99" in out and not os.path.exists(os.path.join(ens, "Elis")), out.strip()[-160:])
rc, out, ens = preparar2("b_sin", analisis_que_se_descartan={"C42": "(prueba) se descarta"})
paso("B", "(h8b) entradas heredadas sin declarar ni reconocer: preparación detenida, destino retirado", rc != 0 and "DETENIDA" in out and not os.path.exists(os.path.join(ens, "Elis")), out.strip()[-160:])
resto = {c: "(prueba) sigue valiendo para la base nueva" for c in mA if c != "C42"}
rc, out, ens = preparar2("b_ok", analisis_que_se_conservan=resto, analisis_que_se_descartan={"C42": "(prueba) el múltiplo de la base anterior ya no vale"},
                         entrada_efectiva={"modo": "registrada", "motivo": "(prueba) ensayo de la regla de la v2.2"})
regb = json.load(open(os.path.join(ens, "resultados", "cambio_de_base.json"), encoding="utf-8")) if rc == 0 else {}
f1b = json.load(open(os.path.join(ens, "Elis", "fase1_v63.json"), encoding="utf-8")) if rc == 0 else {}
paso("B", "(h8a; N5; N7) descarta C42 y reconoce el resto con su motivo: C42 fuera, las heredadas y los descartes constan en el registro del cambio, modo «registrada» con su motivo",
     rc == 0 and "C42" not in (f1b.get("analisis") or {}) and regb.get("analisis_heredadas_conservadas") == resto and "C42" in (regb.get("analisis_descartadas") or {})
     and json.load(open(os.path.join(ens, "Elis", "entrada_efectiva.json"), encoding="utf-8"))["modo"] == "registrada", out.strip()[-200:] if rc else sorted(regb.get("analisis_heredadas_conservadas") or {}))
rc, out, ens = preparar2("b_reg", analisis_que_se_conservan={c: "(prueba)" for c in mA}, entrada_efectiva={"modo": "registrada"})
paso("B", "(N7) modo «registrada» sin motivo: rechazado", rc != 0 and "sin motivo" in out, out.strip()[-160:])
# ------------------------------------------------------------------ P · modo de la entrada efectiva en el pipeline (N7)
import pipeline as PL  # noqa: E402
dP = os.path.join(TMP, "modo")
os.makedirs(dP)
m0 = PL.modo_entrada_efectiva(dP)
json.dump({"tipo": "ensayo_exploratorio", "aviso": "x", "fuente": "x", "entrada_efectiva": "estricta"}, open(os.path.join(dP, "alcance_v2.json"), "w"))
m1 = PL.modo_entrada_efectiva(dP)
json.dump({"modo": "estricta"}, open(os.path.join(dP, "entrada_efectiva.json"), "w"))
m2 = PL.modo_entrada_efectiva(dP)
open(os.path.join(dP, "entrada_efectiva.json"), "w").write("{ilegible")
e_il = error(lambda: PL.modo_entrada_efectiva(dP))
json.dump({"modo": "registrada"}, open(os.path.join(dP, "entrada_efectiva.json"), "w"))
e_rm = error(lambda: PL.modo_entrada_efectiva(dP))
json.dump({"modo": "otro"}, open(os.path.join(dP, "entrada_efectiva.json"), "w"))
e_ot = error(lambda: PL.modo_entrada_efectiva(dP))
paso("P", "(N7) modo de la entrada efectiva: sin declaración «registrada» (línea de base); alcance_v2.json o entrada_efectiva.json «estricta»; ilegible, otro modo o «registrada» sin motivo → error (el paso se detiene)",
     m0 == ("registrada", None) and m1 == ("estricta", "alcance_v2.json") and m2 == ("estricta", "entrada_efectiva.json") and bool(e_il) and bool(e_rm) and bool(e_ot), (m0, m1, m2, e_il, e_rm, e_ot))
src = open(os.path.join(PV, "scripts", "pipeline.py"), encoding="utf-8").read()
os.remove(os.path.join(dP, "entrada_efectiva.json"))
json.dump({"entrada_efectiva": "estricta"}, open(os.path.join(dP, "fase1_metadatos.json"), "w"))
e_falta = error(lambda: PL.modo_entrada_efectiva(dP))
json.dump({"modo": "registrada", "motivo": "(prueba)"}, open(os.path.join(dP, "entrada_efectiva.json"), "w"))
e_dist = error(lambda: PL.modo_entrada_efectiva(dP))
os.remove(os.path.join(dP, "entrada_efectiva.json")); os.remove(os.path.join(dP, "fase1_metadatos.json"))
json.dump({"modo": "estricta"}, open(os.path.join(dP, "Entrada_Efectiva.json"), "w"))
e_graf = error(lambda: PL.modo_entrada_efectiva(dP))
os.remove(os.path.join(dP, "Entrada_Efectiva.json"))
json.dump({"tipo": "ensayo_exploratorio", "aviso": "x", "fuente": "x", "entrada_efectiva": "Estricta"}, open(os.path.join(dP, "alcance_v2.json"), "w"))
e_alc = error(lambda: PL.modo_entrada_efectiva(dP))
paso("P", "(tercera revisión, T5) borrar entrada_efectiva.json que fase1_metadatos.json registra, contradecirlo, otra grafía o una errata en alcance_v2.json: error, no «registrada» en silencio",
     all((e_falta, e_dist, e_graf, e_alc)), (e_falta, e_dist, e_graf, e_alc))
paso("B", "(N7; T5) el expediente nuevo registra el modo también en fase1_metadatos.json", ok and meta.get("entrada_efectiva") == "estricta", meta.get("entrada_efectiva"))
sust = regc.get("sustituidas_en_fase1_v63") or {}
paso("B", "(N5; tercera revisión, T7) el diagnóstico de lo que daría la Historia dice None en las celdas que la Historia no construye (no repite el valor del CAMBIO)",
     any(x.get("construido_por_fase1_historia") is None for x in sust.values()) and not any(x.get("construido_por_fase1_historia") == x.get("valor") and x.get("construido_por_fase1_historia") is not None and c_ not in ("C46", "C47", "C48", "C49", "C50") for c_, x in sust.items()),
     {c_: (x.get("construido_por_fase1_historia"), x.get("valor")) for c_, x in list(sust.items())[:6]})
paso("P", "(N7) cableado en el código del pipeline (comprobación del texto, no del comportamiento; el comportamiento del paso 2 lo ejecutó la revisión independiente): pasa --estricta según ese modo y se detiene si el archivo es ilegible",
     "modo_entrada_efectiva(self.c)" in src and '(["--estricta"] if _estricta else [])' in src and 'f"entrada_efectiva.json: {ex}"' in src)
e = error(lambda: FH.calcular_entrada("C48", {"calculo": dict(copy.deepcopy(CALC), componentes={"pagos_arrendamientos_con_intereses": "no es un objeto"})}, H, anios))
e2 = error(lambda: FH.calcular_entrada("C48", {"calculo": dict(copy.deepcopy(CALC), componentes={"pagos_arrendamientos_con_intereses": {"2023": 5}})}, H, anios))
paso("C", "(segunda revisión, residuo del h13) un componente que no es un objeto: error explícito (no AttributeError)", bool(e) and bool(e2) and "no es un objeto" in e2, (e, e2))

n_ok = sum(x["resultado"] == "PASA" for x in RES)
print(f"{n_ok}/{len(RES)} pruebas de la entrada efectiva (4.15) PASAN")
print("RESULTADO entrada efectiva: " + ("PASA" if n_ok == len(RES) else "FALLA"))
if ARGS.json:
    json.dump(RES, open(ARGS.json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
shutil.rmtree(TMP, ignore_errors=True)
sys.exit(0 if n_ok == len(RES) else 1)
