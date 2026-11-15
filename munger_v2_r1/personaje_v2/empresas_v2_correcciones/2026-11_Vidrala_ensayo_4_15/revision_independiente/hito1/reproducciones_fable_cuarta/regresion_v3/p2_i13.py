"""Sondas I13 (vínculo, sellar, huella) sobre el árbol CONGELADO (arnés fx4.py). Hallazgos 3, 9, 15, 17 y la orden `huella` retirada."""
import copy, datetime, hashlib, json, os, shutil, subprocess, sys, unicodedata
import fx4 as fx
from fx4 import VE, con, ent, con_k, resumen, K, REG, c, FS, nueva_pagina, PV

HOY = datetime.datetime.now().astimezone().date().isoformat()
CLI = [sys.executable, "-B", os.path.join(PV, "scripts", "verificacion_entradas.py")]


def caso(nombre, r, k=K):
    print(f"[{nombre}] {resumen(r, k)}")


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


r = con(); caso("control positivo", r)
print("fecha del sistema:", HOY)
k_hip = next(e["celda"] for e in REG["entradas"] if e["clase"] == "hipotesis")

print("\n=== D1 · hallazgo 3: sellar una revisión antigua (registro en formato 4.14, revisado «el 14-nov»; después cambian fundamento y evidencia)")
cs = os.path.join(fx.TMP, "sellar_retro", "Viscofan"); shutil.copytree(c, cs)
reg = copy.deepcopy(REG); reg["formato"] = "4.14"
for e in reg["entradas"]:
    e["comprobacion"].pop("vinculo", None); e["comprobacion"]["fecha"] = "2026-11-14"
ent(reg, k_hip)["hipotesis"]["fundamento"] = "(prueba) fundamento NUEVO, escrito después de la revisión del 14-nov"
ent(reg, K)["fuente"].update(documento="(prueba) OTRO documento", concepto="(prueba) otro concepto", tratamiento="(prueba) otra transformación")
fx.escribir(reg, cs)
r0 = VE.comprobar(cs); print("antes de sellar:", resumen(r0))
celdas = [e["celda"] for e in reg["entradas"]]
s0 = sha(os.path.join(cs, VE.REGISTRO))
p = subprocess.run(CLI + ["sellar", cs, "--revisor", "revisor sintético", "--fecha", "2026-11-14", *celdas], capture_output=True, text=True)
print(f"(a) CLI sellar --fecha 2026-11-14 ({len(celdas)} celdas): rc {p.returncode} | {(p.stdout + p.stderr).strip()[-230:]}")
p = subprocess.run(CLI + ["sellar", cs, "--revisor", "revisor sintético", "--fecha", HOY, *celdas], capture_output=True, text=True)
print(f"(b) CLI sellar --fecha {HOY} con las comprobaciones fechadas el 14-nov: rc {p.returncode} | {p.stdout.strip().splitlines()[:2]}")
print("    registro sin cambios tras (a) y (b):", sha(os.path.join(cs, VE.REGISTRO)) == s0, "| después:", resumen(VE.comprobar(cs)))
# (c) API con el parámetro `hoy`
try:
    ok, mal = VE.sellar(cs, celdas, "revisor sintético", "2026-11-14", hoy="2026-11-14")
    print(f"(c) API VE.sellar(..., fecha='2026-11-14', hoy='2026-11-14'): selladas {len(ok)} · rechazadas {len(mal)} | después: {resumen(VE.comprobar(cs))}")
    vk = ent(json.load(open(os.path.join(cs, VE.REGISTRO), encoding='utf-8')), K)["comprobacion"]["vinculo"]
    print("    vínculo de K:", {x: vk.get(x) for x in ("sellado_por", "fecha", "sellado_en")})
except SystemExit as ex:
    print("(c) API con hoy= : SystemExit:", str(ex)[:200])
except TypeError as ex:  # tercera pasada (N3): el parámetro ya no existe
    print("(c) API con hoy= : TypeError:", str(ex)[:200])
# (d) una orden que reescribe la fecha de las 321 comprobaciones a hoy y las sella en bloque con la CLI
fx.escribir(reg, cs)
reg_d = copy.deepcopy(reg)
for e in reg_d["entradas"]:
    e["comprobacion"]["fecha"] = HOY
fx.escribir(reg_d, cs)
p = subprocess.run(CLI + ["sellar", cs, "--revisor", "revisor sintético", "--fecha", HOY, *celdas], capture_output=True, text=True)
print(f"(d) fecha de las {len(celdas)} comprobaciones cambiada a hoy por un script + CLI sellar en una sola orden: rc {p.returncode} | {p.stdout.strip().splitlines()[:1]} | después: {resumen(VE.comprobar(cs))}")

print("\n=== D2 · vínculo escrito a mano (sin `sellar`)")
reg2 = copy.deepcopy(reg)
hs = VE.huellas_registro(cs, reg2)
for e in reg2["entradas"]:
    e["comprobacion"]["vinculo"] = {"huella": hs[e["celda"]]}
fx.escribir(reg2, cs)
print("(a) vínculo = {'huella': huellas_registro(...)} sin sellado_por ni fecha:", resumen(VE.comprobar(cs)))
for e in reg2["entradas"]:
    e["comprobacion"]["vinculo"].update(sellado_por=e["comprobacion"]["revisor"], fecha=e["comprobacion"]["fecha"])
fx.escribir(reg2, cs)
print("(b) ídem copiando sellado_por = revisor y fecha = fecha de la comprobación (14-nov), como hacen las baterías y el diagnóstico:", resumen(VE.comprobar(cs)))
p = subprocess.run(CLI + ["huella", c, K], capture_output=True, text=True)
print(f"(c) CLI `huella <expediente> {K}`: rc {p.returncode} | primera línea: {(p.stdout.strip().splitlines() or [''])[0][:120]!r} | ¿imprime una huella de 64 hex?: {any(len(x.strip()) == 64 and all(ch in '0123456789abcdef' for ch in x.strip()) for x in p.stdout.splitlines())}")

print("\n=== D3 · cambios posteriores al sello")
for nombre, cambio in [
    ("revisor cambiado", lambda g: ent(g, K)["comprobacion"].update(revisor="otro revisor cualquiera")),
    ("fecha de la comprobación cambiada", lambda g: ent(g, K)["comprobacion"].update(fecha="2019-01-01")),
    ("fuente examinada cambiada", lambda g: ent(g, K)["comprobacion"].update(fuente_examinada="ninguna en particular")),
    ("extractor cambiado", lambda g: ent(g, K)["comprobacion"].update(extractor="otro extractor")),
    ("nota de la comprobación cambiada", lambda g: ent(g, K)["comprobacion"].update(nota="cambiada")),
    ("incidencia, uso e id cambiados", lambda g: ent(g, K).update(incidencia="otra", uso="otro uso", id="otro_id")),
    ("ámbito declarado cambiado a «juicio»", lambda g: ent(g, K).update(ambito="juicio")),
    ("vinculo.sellado_por cambiado", lambda g: ent(g, K)["comprobacion"]["vinculo"].update(sellado_por="nadie")),
    ("vinculo.fecha cambiada", lambda g: ent(g, K)["comprobacion"]["vinculo"].update(fecha="1999-01-01")),
    ("revisor y vinculo.sellado_por cambiados a la vez (la huella incluye al revisor)", lambda g: (ent(g, K)["comprobacion"].update(revisor="otro"), ent(g, K)["comprobacion"]["vinculo"].update(sellado_por="otro"))),
    ("perimetro_del_expediente del registro cambiado (y el de la fuente de K con justificación)", lambda g: g.update(perimetro_del_expediente="otro perímetro")),
]:
    r = con(cambio); caso("después del sello: " + nombre, r)

print("\n=== D4 · hallazgo 9: derivado cuyo origen cambia de fundamento (con el `sellar` real)")
k_der = next(e["celda"] for e in REG["entradas"] if e["clase"] == "dato_publicado" and e["celda"].startswith("Historia!") and isinstance(e["valor_modelo"], (int, float)) and e["valor_modelo"] > 0 and e["celda"] != K)
vm = fx.inst["celdas"][k_der]
va = round(vm * 0.6, 3); vb = round(vm - va, 3)
p1 = nueva_pagina(f"Parte A de {k_der}: {round(va * 1000):d}"); p2 = nueva_pagina(f"Parte B de {k_der}: {round(vb * 1000):d}")
p1b = nueva_pagina(f"OTRA partida de OTRO documento (nada que ver): {round(va * 1000):d}")
def aux(nombre, pag, cita, v, **extra):
    f = dict(ent(REG, K)["fuente"], pagina=pag, cita=cita, valor_fuente=round(v * 1000), concepto=f"concepto de {nombre}", columna=ent(REG, k_der)["fuente"]["columna"], periodo=ent(REG, k_der)["fuente"]["periodo"]); f.update(extra)
    return {"celda": nombre, "id": nombre, "ambito": "auxiliar", "uso": "origen", "material": True, "clase": "dato_publicado", "valor_modelo": v, "comprobacion": dict(fx.COMPROBADA), "incidencia": None, "fuente": f}
def derivar(g):
    e = ent(g, k_der); e["fuente"] = {}
    e.update(clase="derivado", derivacion={"origenes": ["aux:a", "aux:b"], "formula": 'o["aux:a"] + o["aux:b"]', "conciliacion": "suma de las dos partes publicadas"})
    g["entradas"].append(aux("aux:a", p1, f"Parte A de {k_der}: {round(va * 1000):d}", va))
    g["entradas"].append(aux("aux:b", p2, f"Parte B de {k_der}: {round(vb * 1000):d}", vb))
cd = os.path.join(fx.TMP, "derivado", "Viscofan"); shutil.copytree(c, cd)
g = copy.deepcopy(REG); derivar(g)
for e in g["entradas"]:
    e["comprobacion"].pop("vinculo", None)
fx.escribir(g, cd)
ok, mal = VE.sellar(cd, [k_der], "revisor sintético", HOY); print("sellar SOLO el derivado con sus orígenes sin sellar:", ok, [x[:170] for x in mal])
ok, mal = VE.sellar(cd, [e["celda"] for e in g["entradas"]], "revisor sintético", HOY); print(f"sellar todo (derivado y orígenes en la misma orden): selladas {len(ok)} · rechazadas {len(mal)} |", resumen(VE.comprobar(cd), k_der))
g2 = json.load(open(os.path.join(cd, VE.REGISTRO), encoding="utf-8"))
ent(g2, "aux:a")["fuente"].update(pagina=p1b, cita=f"OTRA partida de OTRO documento (nada que ver): {round(va * 1000):d}", documento="OTRO documento", concepto="OTRO concepto", tratamiento="otra transformación")
fx.escribir(g2, cd)
r = VE.comprobar(cd); caso("el origen aux:a cambia de documento, concepto, página y cita (mismo número), sin nueva revisión", r, k_der); print("   aux:a:", con_k(r, "aux:a"))
ok, mal = VE.sellar(cd, [k_der], "revisor sintético", HOY); print("   sellar el derivado mientras su origen está desactualizado:", ok, [x[:200] for x in mal])
ok, mal = VE.sellar(cd, ["aux:a"], "revisor sintético", HOY); print("   se revisa y se sella de nuevo SOLO el origen:", ok, mal)
r = VE.comprobar(cd); caso("después de resellar solo el origen", r, k_der); print("   aux:a:", con_k(r, "aux:a") or "comprobada")
ok, mal = VE.sellar(cd, [k_der], "revisor sintético", HOY); r = VE.comprobar(cd); print("   se sella de nuevo el derivado:", ok, mal, "|", resumen(r, k_der))
# origen de segundo nivel
print("   — cadena de dos niveles: K2 = o[k_der]; cambia aux:a y se resellan aux:a y k_der, no K2")
k2 = next(e["celda"] for e in REG["entradas"] if e["clase"] == "dato_publicado" and e["celda"].startswith("Historia!") and isinstance(e["valor_modelo"], (int, float)) and e["valor_modelo"] > 0 and e["celda"] not in (K, k_der))
g3 = json.load(open(os.path.join(cd, VE.REGISTRO), encoding="utf-8"))
g3["entradas"].append(aux("aux:z", p2, f"Parte B de {k_der}: {round(vb * 1000):d}", vb))
e2 = ent(g3, k2); e2["fuente"] = {}
e2.update(clase="derivado", derivacion={"origenes": [k_der, "aux:z"], "formula": f'o["{k_der}"] - o["{k_der}"] + {fx.inst["celdas"][k2]!r} + 0 * o["aux:z"]', "conciliacion": "prueba de cadena"})
fx.escribir(g3, cd)
ok, mal = VE.sellar(cd, [k2, "aux:z"], "revisor sintético", HOY); print("   sellar K2 y aux:z:", ok, [x[:120] for x in mal], "|", resumen(VE.comprobar(cd), k2))
g4 = json.load(open(os.path.join(cd, VE.REGISTRO), encoding="utf-8"))
ent(g4, "aux:a")["fuente"].update(documento="TERCER documento")
fx.escribir(g4, cd)
ok, mal = VE.sellar(cd, ["aux:a", k_der], "revisor sintético", HOY); r = VE.comprobar(cd)
print("   tras cambiar aux:a y resellar aux:a y k_der:", ok, mal, "| K2:", con_k(r, k2) or "comprobada")

print("\n=== D5 · hallazgo 17: estabilidad de la huella")
e = copy.deepcopy(ent(REG, K)); h0 = VE.huella_fundamento(e, fx.EVID.get(K))
e2 = json.loads(json.dumps(e, ensure_ascii=True, sort_keys=False)); print("ida y vuelta por JSON y otro orden de claves:", VE.huella_fundamento(dict(reversed(list(e2.items()))), fx.EVID.get(K)) == h0)
e4 = copy.deepcopy(e); e4["fuente"]["valor_fuente"] = int(e4["fuente"]["valor_fuente"]); print(f"valor_fuente {e['fuente']['valor_fuente']!r} → {e4['fuente']['valor_fuente']!r}:", VE.huella_fundamento(e4, fx.EVID.get(K)) == h0)
e6 = copy.deepcopy(e); e6["fuente"]["documento"] = unicodedata.normalize("NFD", e6["fuente"]["documento"]); print("mismo texto en NFD en vez de NFC:", e6["fuente"]["documento"] != e["fuente"]["documento"], VE.huella_fundamento(e6, fx.EVID.get(K)) == h0)
e7 = copy.deepcopy(e); e7["fuente"]["cita"] = e7["fuente"]["cita"] + " "; print("un espacio final en la cita:", VE.huella_fundamento(e7, fx.EVID.get(K)) == h0)
e8 = copy.deepcopy(e); e8["fuente"]["pagina"] = int(e8["fuente"]["pagina"]); print("página '22' → 22:", VE.huella_fundamento(e8, fx.EVID.get(K)) == h0)
e9 = copy.deepcopy(e); e9["fuente"]["signo"] = "+1"; print("signo 1 → '+1':", VE.huella_fundamento(e9, fx.EVID.get(K)) == h0)
e10 = copy.deepcopy(e); e10["fuente"]["cita"] = e10["fuente"]["cita"].replace(" ", "  ", 1); print("dos espacios seguidos dentro de la cita:", VE.huella_fundamento(e10, fx.EVID.get(K)) == h0)
e11 = copy.deepcopy(e); e11["fuente"]["documento"] = e11["fuente"]["documento"].upper(); print("documento en MAYÚSCULAS (cambio real de texto):", VE.huella_fundamento(e11, fx.EVID.get(K)) == h0)
e12 = copy.deepcopy(e); e12["valor_modelo"] = True if e12["valor_modelo"] == 1 else e12["valor_modelo"]
print("colisiones de la forma canónica: _canon(1.0) == _canon(1):", VE._canon(1.0) == VE._canon(1), "| _canon(True) is True:", VE._canon(True) is True, "| _canon('a\\tb') =", repr(VE._canon("a\tb")), "| _canon(' 0.10 ') =", repr(VE._canon(" 0.10 ")))
r = con(lambda g: ent(g, K)["fuente"].update(valor_fuente=int(ent(g, K)["fuente"]["valor_fuente"]))); caso("registro reescrito con 849697 en vez de 849697.0 (mismo número), sin resellar", r)

print("\n=== D9 · hallazgo 15: un sellar rechazado no reescribe el registro")
cf = os.path.join(fx.TMP, "sellar_formato", "Viscofan"); shutil.copytree(c, cf)
reg = copy.deepcopy(REG); reg["formato"] = "4.14"
for e in reg["entradas"]:
    e["comprobacion"].pop("vinculo", None)
fx.escribir(reg, cf)
sha_a = sha(os.path.join(cf, VE.REGISTRO))
ok, mal = VE.sellar(cf, [K], "revisor que no es", HOY)
print("sellar rechazado (API):", ok, [x[:110] for x in mal[:1]], "| formato:", json.load(open(os.path.join(cf, VE.REGISTRO), encoding="utf-8"))["formato"], "| el archivo cambió:", sha_a != sha(os.path.join(cf, VE.REGISTRO)))
p = subprocess.run(CLI + ["sellar", cf, "--revisor", "revisor que no es", "--fecha", HOY, K], capture_output=True, text=True)
print("sellar rechazado (CLI): rc", p.returncode, "|", p.stdout.strip().splitlines()[:1], "| el archivo cambió:", sha_a != sha(os.path.join(cf, VE.REGISTRO)))
ok, mal = VE.sellar(cf, [K, "Historia!NOEXISTE"], "revisor sintético", HOY)
print("sellar con una celda válida y otra inexistente:", ok, [x[:60] for x in mal], "| formato ahora:", json.load(open(os.path.join(cf, VE.REGISTRO), encoding="utf-8"))["formato"], "| el archivo cambió:", sha_a != sha(os.path.join(cf, VE.REGISTRO)))

print("\n=== D10 · sellar y lecturas externas / auxiliares")
ce = os.path.join(fx.TMP, "sellar_externa", "Viscofan"); shutil.copytree(c, ce)
g = copy.deepcopy(REG)
LE = {"referencia": "https://ejemplo.invalid/serie", "fecha": "2026-11-15 10:00 CET", "evidencia": "transcripción", "limitaciones": "sin bytes conservados"}
ax = aux("aux:ext", "1", "x", 1.0); [ax["fuente"].pop(x, None) for x in ("archivo", "sha256")]; ax["fuente"].update(conservacion="externa", lectura_externa=dict(LE), valor_fuente=1000, cita="x 1000")
g["entradas"].append(ax)
f = ent(g, K)["fuente"]; [f.pop(x, None) for x in ("archivo", "sha256")]; f.update(conservacion="externa", lectura_externa=dict(LE))
for e in g["entradas"]:
    if e["celda"] in (K, "aux:ext"):
        e["comprobacion"].pop("vinculo", None)
fx.escribir(g, ce)
ok, mal = VE.sellar(ce, [K, "aux:ext"], "revisor sintético", HOY)
print("sellar una lectura externa de una celda del universo y otra de un auxiliar («aux:ext»):", ok, [x[:150] for x in mal])
fx.limpiar()
