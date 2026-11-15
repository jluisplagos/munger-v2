"""Cuarta pasada (sonda q1 de la tercera; solo cambian el árbol y el arnés: regresión de N1/N3 y T6).
Texto original: Tercera pasada · N1 (una entrada de juicio no material y no comprobada solo deja de bloquear con el juicio de materialidad revisado y
sellado: resultado «verificado», fuente examinada, extractor ≠ revisor, justificación ≥ 20 caracteres alfanuméricos, vínculo vigente) y
recuentos en el resumen y en el informe. Arnés fx4.py (vínculo escrito a mano, como las baterías) + `sellar` real donde se dice."""
import copy, json, os, re, shutil, subprocess, sys
import fx4 as fx
from fx4 import VE, con, ent, con_k, resumen, K, REG, c

inst = fx.inst
KJ = next(e["celda"] for e in REG["entradas"] if e["ambito"] == "juicio" and e["clase"] == "dato_publicado" and isinstance(e["valor_modelo"], (int, float)))
JUST = "cifra de contexto del sector que ninguna fase usa para concluir (revisado)"
print("KJ:", KJ, inst["celdas"][KJ], "| entradas de juicio:", inst["n_juicio"])


def caso(nombre, r, k=KJ):
    print(f"[{nombre}] {resumen(r, k, 330)}")


def no_material(g, k=KJ, just=JUST, sin_fuente=True, **comprob):
    e = ent(g, k)
    e.update(material=False, justificacion_materialidad=just)
    if sin_fuente and isinstance(e.get("fuente"), dict) and e["fuente"]:
        e["fuente"].update(archivo="fuentes_sinteticas/NO_EXISTE.txt", sha256=None)
    e["comprobacion"].update(comprob)


print("\n=== A · requisitos del juicio de materialidad, uno a uno (fuente ausente; vínculo escrito a mano)")
r = con(lambda g: no_material(g), resellar=True); caso("A0 · positivo: justificación larga, revisor ≠ extractor, verificado, fuente examinada, vínculo vigente", r)
print("      resumen:", r["resumen"])
r = con(lambda g: no_material(g, fuente_examinada=None), resellar=True); caso("A1 · revisor SIN fuente examinada", r)
r = con(lambda g: no_material(g, fuente_examinada="   "), resellar=True); caso("A2 · fuente examinada de espacios", r)
r = con(lambda g: no_material(g, fuente_examinada="x"), resellar=True); caso("A3 · fuente examinada «x»", r)
r = con(lambda g: no_material(g, resultado="pendiente"), resellar=True); caso("A4 · resultado «pendiente»", r)
r = con(lambda g: no_material(g, resultado="discrepancia"), resellar=True); caso("A5 · resultado «discrepancia»", r)
r = con(lambda g: no_material(g, revisor="Extractor  Sintético"), resellar=True); caso("A6 · revisor = extractor (otra grafía)", r)
r = con(lambda g: no_material(g, extractor=None), resellar=True); caso("A7 · sin extractor", r)
for just in ("x" * 19, "x" * 20, "_" * 20, "1234567890 1234567890", "no material no material", "n/a n/a n/a n/a n/a n/a n/a", "· · · · · · · · · · · · · · · · · · · · · ·"):
    r = con(lambda g: no_material(g, just=just), resellar=True); caso(f"A8 · justificación {just!r}", r)
r = con(lambda g: no_material(g)); caso("A9 · justificación y material:false escritos DESPUÉS del sello (sin resellar)", r)
for mat in (0, "false", None, "no"):
    r = con(lambda g: (no_material(g), ent(g, KJ).update(material=mat)), resellar=True); caso(f"A10 · material = {mat!r} (no es el booleano false)", r)
r = con(lambda g: (no_material(g), ent(g, KJ).update(valor_modelo=inst["celdas"][KJ] + 1)), resellar=True); caso("A11 · no material revisada, pero con el valor del registro distinto del libro (estado desactualizada)", r)


def juicio_todas(g, just=JUST, **comprob):
    n = 0
    for e in g["entradas"]:
        if e.get("ambito") == "juicio" and inst["ambito"].get(e["celda"]) == "juicio":
            no_material(g, e["celda"], just, **comprob); n += 1
    return n


print("\n=== B · en bloque")
r = con(lambda g: juicio_todas(g), resellar=True)
print(f"[B1 · TODAS las entradas de juicio no materiales con la misma justificación larga y la comprobación completa del fixture (fuentes ausentes)] {resumen(r)}")
print("      resumen:", r["resumen"]); print("      motivo:", r["motivo"])
r = con(lambda g: juicio_todas(g, fuente_examinada=None), resellar=True)
print(f"[B2 · ídem sin fuente examinada] {resumen(r)}")
r = con(lambda g: juicio_todas(g, just="x"), resellar=True)
print(f"[B3 · ídem con justificación «x»] {resumen(r)}")

print("\n=== C · auxiliar no material y derivado que depende de él")
AUX = {"celda": "aux:nm", "id": "aux:nm", "ambito": "auxiliar", "uso": f"origen de {KJ}", "material": False, "justificacion_materialidad": JUST, "clase": "dato_publicado",
       "valor_modelo": inst["celdas"][KJ], "comprobacion": dict(fx.COMPROBADA), "incidencia": None,
       "fuente": dict(copy.deepcopy(ent(REG, KJ)["fuente"]), archivo="fuentes_sinteticas/NO_EXISTE.txt", sha256=None)}


def derivado_de_aux_nm(g, k):
    g["entradas"].append(copy.deepcopy(AUX))
    e = ent(g, k); e["fuente"] = {}
    e.update(clase="derivado", derivacion={"origenes": ["aux:nm"], "formula": 'o["aux:nm"]', "conciliacion": "x"})


r = con(lambda g: derivado_de_aux_nm(g, KJ), resellar=True); caso("C1 · derivado MATERIAL de juicio cuyo origen es un auxiliar no material revisado (sin fuente)", r)
print("      resumen:", r["resumen"])

print("\n=== D · `sellar` real (fecha del sistema)")
import datetime as dt
HOY = dt.datetime.now().astimezone().date().isoformat()
cs = os.path.join(fx.TMP, "sellar", "Viscofan")
shutil.copytree(c, cs)
reg = copy.deepcopy(REG)
no_material(reg, KJ, JUST)
KJ2 = next(e["celda"] for e in REG["entradas"] if e["ambito"] == "juicio" and e["clase"] == "dato_publicado" and isinstance(e["valor_modelo"], (int, float)) and e["celda"] != KJ)
no_material(reg, KJ2, "x")
fx.sellar_todo(reg, cs)
for k in (KJ, KJ2):
    ent(reg, k)["comprobacion"].pop("vinculo", None)
    ent(reg, k)["comprobacion"]["fecha"] = HOY
fx.escribir(reg, cs)
r0 = VE.comprobar(cs)
ok, mal = VE.sellar(cs, [KJ, KJ2], "revisor sintético", HOY)
r1 = VE.comprobar(cs)
print(f"antes de sellar: {resumen(r0)}")
print(f"sellar([{KJ} (justificación larga), {KJ2} (justificación «x»)]) → selladas {ok} · rechazadas {[m[:230] for m in mal]}")
print(f"después: {resumen(r1)}")
reg2 = json.load(open(os.path.join(cs, VE.REGISTRO), encoding="utf-8"))
ent(reg2, KJ)["justificacion_materialidad"] = JUST + " (cambiada después del sello)"
fx.escribir(reg2, cs)
r2 = VE.comprobar(cs)
print(f"tras cambiar la justificación de {KJ} después del sello: {'; '.join(x[:200] for x in r2['no_materiales_sin_revisar'] if x.startswith(KJ + ':'))}")
try:
    VE.sellar(cs, [KJ], "revisor sintético", HOY, hoy="2026-11-14")
    print("N3 · sellar(..., hoy=…) ACEPTADO")
except TypeError as ex:
    print("N3 · sellar(..., hoy=…) →", type(ex).__name__, str(ex)[:90])
try:
    VE.sellar(cs, [KJ], "revisor sintético", "2026-11-14")
    print("N3 · sellar con fecha de ayer ACEPTADO")
except SystemExit as ex:
    print("N3 · sellar con --fecha 2026-11-14 → SystemExit:", str(ex)[:120])

print("\n=== E · ficha e informe con el registro APTO y entradas no materiales, datos como hipótesis y no aplicables (¿se imprimen los recuentos?)")
CFG = os.path.join(fx.PV, "config_v2_v641_experimental.json")
env = dict(os.environ, MUNGER_CONFIG=CFG)


def informe_de(etiqueta):
    for s in ("ficha.py", "informe.py"):
        p = subprocess.run([sys.executable, "-B", os.path.join(fx.PV, "scripts", s), c, "--provisional"], capture_output=True, text=True, env=env)
        if p.returncode != 0:
            print(f"   {s} rc {p.returncode}: {(p.stdout + p.stderr)[-300:]}")
    inf = open(os.path.join(c, "informe_provisional.md"), encoding="utf-8").read() if os.path.exists(os.path.join(c, "informe_provisional.md")) else ""
    m = re.findall(r"\*\*Verificación de las entradas financieras:\*\*.{0,520}", inf)
    fic = json.load(open(os.path.join(c, "ficha_provisional.json"), encoding="utf-8")) if os.path.exists(os.path.join(c, "ficha_provisional.json")) else {}
    ve = ((fic.get("aptitud_de_uso") or {}).get("verificacion_entradas") or {})
    print(f"[{etiqueta}]")
    print("   informe:", (m[0] if m else "(sin línea)")[:520])
    print("   ficha.aptitud_de_uso.verificacion_entradas:", {k: ve.get(k) for k in ("apto_por_entradas", "no_materiales", "no_materiales_sin_revisar", "datos_como_hipotesis", "no_aplicables")})
    print("   ficha … resumen:", ve.get("resumen"))


def mezcla(g):
    n = 0
    for e in g["entradas"]:
        if e.get("ambito") == "juicio" and inst["ambito"].get(e["celda"]) == "juicio" and n < 5:
            no_material(g, e["celda"]); n += 1
    e = ent(g, K); e["fuente"] = {}
    e.update(clase="convencion", hipotesis={"fundamento": "x", "alternativas": ["x"], "limites": ["x"]}, justificacion_clase="x")


r = con(mezcla, resellar=True)
print(f"registro: {resumen(r)}")
informe_de("E1 · registro apto con 5 no materiales revisadas, 1 dato como convención y 3 no aplicables")
r = con()
informe_de("E2 · control: registro apto sin ninguna de esas categorías salvo los 3 no aplicables del fixture")
print("\n=== F · (T6) `resumen` sin registro y sin libro")
import tempfile
os.remove(os.path.join(c, VE.REGISTRO))
r = VE.comprobar(c)
print("   sin registro → resumen:", repr(r["resumen"])[:160], "| apto:", r["apto_por_entradas"])
vacia = tempfile.mkdtemp(prefix="rev_fable_vacia_")
r = VE.comprobar(vacia)
print("   carpeta sin libro → resumen:", repr(r["resumen"])[:160], "| apto:", r["apto_por_entradas"])
shutil.rmtree(vacia, ignore_errors=True)
fx.limpiar()
