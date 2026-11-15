"""Batería de la verificación completa de las entradas financieras (4.14; requisito de cierre del 14-nov-2026).

Trabaja sobre una copia del expediente cerrado de Viscofan de la 4.13. Construye un registro SINTÉTICO completo (identificado como tal:
fuentes de texto sintéticas con marcas de página creadas en la copia; extractor y revisor ficticios) que sirve de control positivo, y
cada caso negativo cambia una sola cosa. No ejecuta el pipeline ni LibreOffice: llama a verificacion_entradas, a ficha.py e informe.py en
modo provisional y a la vigencia de cierre_v2.

Casos: P control positivo · C cobertura incompleta, sobrante y repetida · K columna equivocada (período de otra columna) · U unidades y
escala · S signo · R perímetro · D derivado con origen pendiente y con fórmula que no reproduce el valor · A reutilización desactualizada
(valor del libro cambiado; fuente conservada cambiada) · I revisión no independiente y sin fuente examinada · H hipótesis presentada como
dato · Z cero comprobado, dato ausente y no aplicable · T cita fuera de la página o sin el valor · G puerta: ficha e informe (apta por
entradas sí/no; nunca «apta para dinero real») · M el registro forma parte del material: cambiarlo retira la aprobación en la primera llamada.
Uso: python3 -B test_verificacion_entradas_414.py [--json salida.json]
"""
import argparse, copy, hashlib, json, os, shutil, subprocess, sys, tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
PV = os.path.dirname(AQUI)
sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
sys.path.insert(0, os.path.join(PV, "scripts"))
import verificacion_entradas as VE  # noqa: E402
import cierre_v2 as CIE  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--json")
ARGS = ap.parse_args()
E413 = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_13")
CFG = os.path.join(PV, "config_v2_v641_experimental.json")
TMP = tempfile.mkdtemp(prefix="verificacion_entradas_414_")
RES = []


def paso(grupo, nombre, ok, detalle=""):
    RES.append({"grupo": grupo, "prueba": nombre, "resultado": "PASA" if ok else "FALLA", "detalle": str(detalle)[:400]})
    print(f"[{grupo}] {'PASA ' if ok else 'FALLA'} {nombre}" + (f" · {str(detalle)[:240]}" if detalle else ""))


c = os.path.join(TMP, "viscofan", "Viscofan")
shutil.copytree(os.path.join(E413, "viscofan", "Viscofan"), c, ignore=shutil.ignore_patterns(".lo_perfil", "variantes_v64", "recalc", "prompts_generados", "__pycache__"))
inst = VE.universo(c)
anios = [inst["celdas"].get(f"Historia!{x}5") for x in "CDEFGHIJKL"]
os.makedirs(os.path.join(c, "fuentes_sinteticas"))
paginas = []


def fuente_para(k, v):
    """Página sintética con una cita que contiene el valor (en miles de euros para las cifras: escala 0,001 hacia «mm»)."""
    n = len(paginas) + 1
    m = __import__("re").match(r"^Historia!([C-L])(\d+)$", k)
    periodo = f"ejercicio {int(anios['CDEFGHIJKL'.index(m.group(1))])}" if m else "31-dic-2025"
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        if m and int(m.group(2)) == 5:
            vf, unidad, escala, cita = v, "año", 1.0, f"Ejercicio {int(v)}"
        else:
            vf, unidad, escala = round(v * 1000, 6), "miles de euros", 0.001
            cita = f"Partida sintética de {k}: {vf:.3f}"
    else:
        vf, unidad, escala, cita = v, "texto", 1.0, f"Dato sintético de {k}: {v}"
    paginas.append(cita)
    return {"documento": "Fuente sintética de la prueba (no es un documento de la empresa)", "archivo": "fuentes_sinteticas/fuente.txt", "sha256": None,
            "version": "sintética 1", "pagina": str(n), "ubicacion": "tabla sintética", "concepto": f"concepto de {k}", "columna": periodo, "periodo": periodo,
            "unidad": unidad, "escala": escala, "signo": 1, "tratamiento": "ninguno", "perimetro": "consolidado", "reexpresado": "no aplica",
            "valor_fuente": vf, "cita": cita}


COMPROBADA = {"extractor": "extractor sintético", "revisor": "revisor sintético", "fecha": "2026-11-14", "resultado": "verificado",
              "fuente_examinada": "fuentes_sinteticas/fuente.txt (página citada)", "nota": None}
ents = []
for k, v in inst["celdas"].items():
    t = inst["tipos"].get(k)
    e = {"celda": k, "id": inst["ids"].get(k), "uso": "prueba", "material": True, "valor_modelo": v, "comprobacion": dict(COMPROBADA), "incidencia": None}
    if t in ("hipótesis", "configuracion"):
        e.update(clase="hipotesis" if t == "hipótesis" else "convencion",
                 hipotesis={"fundamento": "(prueba)", "alternativas": ["(prueba)"], "limites": ["(prueba)"]})
    elif v is None or v == "":
        e.update(clase="no_aplicable", justificacion="(prueba) celda vacía del libro: no aplica a este expediente")
    elif isinstance(v, (int, float)) and v == 0:
        e.update(clase="cero_comprobado", fuente=fuente_para(k, v))
    else:
        e.update(clase="dato_publicado", fuente=fuente_para(k, v))
    ents.append(e)
# un derivado con orígenes auxiliares: el primer dato de la Historia como suma de dos partidas auxiliares
k_der = next(e["celda"] for e in ents if e["celda"].startswith("Historia!") and e["clase"] == "dato_publicado" and not e["celda"].endswith("5")
             and isinstance(e["valor_modelo"], (int, float)) and e["valor_modelo"] > 0)
vd = inst["celdas"][k_der]
for nombre, frac in (("aux:parte_1", 0.6), ("aux:parte_2", 0.4)):
    ents.append({"celda": nombre, "id": nombre, "uso": f"origen de {k_der}", "material": True, "clase": "dato_publicado", "valor_modelo": vd * frac,
                 "fuente": fuente_para(nombre, vd * frac) | {"periodo": "ejercicio 2016", "columna": "ejercicio 2016"}, "comprobacion": dict(COMPROBADA), "incidencia": None})
e_der = next(e for e in ents if e["celda"] == k_der)
e_der.update(clase="derivado", fuente={}, derivacion={"origenes": ["aux:parte_1", "aux:parte_2"], "formula": 'o["aux:parte_1"] + o["aux:parte_2"]',
                                                    "conciliacion": "(prueba) suma de las dos partidas"})
open(os.path.join(c, "fuentes_sinteticas", "fuente.txt"), "w", encoding="utf-8").write("".join(f"[PDF PAGE {i + 1}]\n{p}\n" for i, p in enumerate(paginas)))
REG = {"formato": VE.FORMATO, "empresa": "Viscofan", "nota": "REGISTRO SINTÉTICO DE PRUEBA (no verifica ningún dato real)", "perimetro_del_expediente": "consolidado",
       "huella_entradas_economicas": inst["huella"], "entradas": ents}


def con(cambio=None, escribir_fuente=None):
    reg = copy.deepcopy(REG)
    if cambio:
        cambio(reg)
    json.dump(reg, open(os.path.join(c, VE.REGISTRO), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    return VE.comprobar(c)


def ent(reg, k):
    return next(e for e in reg["entradas"] if e["celda"] == k)


k_dato = next(e["celda"] for e in ents if e["clase"] == "dato_publicado" and e["celda"].startswith("Historia!F") and not e["celda"].endswith("5"))
k_hip = next(e["celda"] for e in ents if e["clase"] == "hipotesis")

r = con()
paso("P", f"control positivo sintético: {len(r['comprobadas'])} comprobadas de {r['universo']} (+{r['auxiliares']} auxiliares), apta por entradas",
     r["apto_por_entradas"] and not r["errores"] and not r["discrepancias"] and len([x for x in r['comprobadas'] if not x.startswith('aux:')]) == r["universo"],
     (r["errores"] + r["discrepancias"] + r["pendientes"])[:3])
r = con(lambda g: g["entradas"].pop(3))
paso("C", "cobertura incompleta (una celda sin entrada): no apta, con la celda pendiente", not r["apto_por_entradas"] and len(r["sin_entrada"]) == 1, r["motivo"])
r = con(lambda g: g["entradas"].append(dict(ent(g, k_dato))))
paso("C", "entrada repetida: no apta (una misma celda no cuenta dos veces)", not r["apto_por_entradas"] and r["repetidas"] == [k_dato], r["repetidas"])
r = con(lambda g: g["entradas"].append(dict(ent(g, k_dato), celda="Historia!Z99")))
paso("C", "entrada de una celda que no es del universo: no apta", not r["apto_por_entradas"] and "Historia!Z99" in r["sobrantes"], r["sobrantes"])
r = con(lambda g: ent(g, k_dato)["fuente"].update(periodo="ejercicio 1999", columna="ejercicio 1999"))
paso("K", "columna equivocada (el período declarado no es el año de la columna de la Historia): error", any(k_dato in x and "columna" in x for x in r["errores"]), r["errores"][:1])
r = con(lambda g: ent(g, k_dato)["fuente"].update(escala=1.0))
paso("U", "unidades: escala 1 con la fuente en miles de euros y el modelo en mm: error", any(k_dato in x and "escala" in x for x in r["errores"]), r["errores"][:1])
r = con(lambda g: (ent(g, k_dato)["fuente"].update(unidad="millones de euros"), None))
paso("U", "unidades: la fuente declarada en millones con un valor en miles: incoherente (error o discrepancia)", not r["apto_por_entradas"], (r["errores"] + r["discrepancias"])[:1])
r = con(lambda g: ent(g, k_dato)["fuente"].update(signo=-1))
paso("S", "signo cambiado: discrepancia", any(k_dato in x for x in r["discrepancias"]), r["discrepancias"][:1])
r = con(lambda g: ent(g, k_dato)["fuente"].update(perimetro="segmento de envolturas"))
paso("R", "perímetro distinto del del expediente sin justificación: error", any(k_dato in x and "perímetro" in x for x in r["errores"]), r["errores"][:1])
r = con(lambda g: ent(g, k_dato)["fuente"].update(perimetro="segmento de envolturas", perimetro_justificacion="(prueba) la partida solo se publica por segmento"))
paso("R", "perímetro distinto con su justificación declarada: aceptado (la pertinencia es del revisor)", r["apto_por_entradas"], r["motivo"])
r = con(lambda g: ent(g, "aux:parte_2")["comprobacion"].update(resultado="pendiente"))
paso("D", "derivado con un origen pendiente: el derivado queda pendiente", any(x.startswith(k_der) and "origen" in x for x in r["pendientes"]), [x for x in r["pendientes"] if x.startswith(k_der)][:1])
r = con(lambda g: ent(g, k_der)["derivacion"].update(formula='o["aux:parte_1"]'))
paso("D", "derivado cuya fórmula no reproduce el valor: discrepancia", any(x.startswith(k_der) for x in r["discrepancias"]), r["discrepancias"][:1])
r = con(lambda g: ent(g, k_dato).update(valor_modelo=(ent(g, k_dato)["valor_modelo"] or 0) + 1))
paso("A", "reutilización desactualizada (el dato del libro ya no es el registrado): desactualizada", any(k_dato in x for x in r["desactualizadas"]), r["desactualizadas"][:1])
sha0 = hashlib.sha256(open(os.path.join(c, "fuentes_sinteticas", "fuente.txt"), "rb").read()).hexdigest()
r = con(lambda g: ent(g, k_dato)["fuente"].update(sha256=sha0))
ok1 = r["apto_por_entradas"]
open(os.path.join(c, "fuentes_sinteticas", "fuente.txt"), "a", encoding="utf-8").write("\n(cambio)\n")
r = con(lambda g: ent(g, k_dato)["fuente"].update(sha256=sha0))
paso("A", "fuente conservada con su huella: vale; si la fuente cambia, la comprobación queda desactualizada", ok1 and any(k_dato in x and "cambió" in x for x in r["desactualizadas"]), r["desactualizadas"][:1])
r = con(lambda g: ent(g, k_dato)["comprobacion"].update(revisor="extractor sintético"))
paso("I", "revisor igual al extractor: error (revisión independiente obligatoria)", any(k_dato in x and "independiente" in x for x in r["errores"]), r["errores"][:1])
r = con(lambda g: ent(g, k_dato)["comprobacion"].update(fuente_examinada=""))
paso("I", "revisor sin fuente examinada (aceptó el registro): error", any(k_dato in x and "fuente examinó" in x for x in r["errores"]), r["errores"][:1])
r = con(lambda g: ent(g, k_dato)["comprobacion"].update(resultado="discrepancia", nota="(prueba) la nota dice otra cifra"))
paso("I", "el revisor registra una discrepancia: no apta", any(k_dato in x for x in r["discrepancias"]), r["discrepancias"][:1])
r = con(lambda g: ent(g, k_hip).update(clase="dato_publicado", fuente=fuente_para(k_hip, ent(g, k_hip)["valor_modelo"])))
paso("H", "hipótesis presentada como dato publicado: error", any(k_hip in x and "hipótesis" in x for x in r["errores"]), r["errores"][:1])
r = con(lambda g: ent(g, k_hip).update(hipotesis={"fundamento": "(prueba)", "alternativas": [], "limites": ["x"]}))
paso("H", "hipótesis sin alternativas: error (conserva fundamento, alternativas y límites)", any(k_hip in x for x in r["errores"]), r["errores"][:1])
r = con(lambda g: ent(g, k_hip).setdefault("comprobacion", {}).update(resultado="discrepancia", revisor="revisor sintético", nota="(prueba) el fundamento ya no describe el dato vigente"))
paso("H", "(14-nov) una discrepancia registrada por el revisor en una hipótesis cuenta: no apta (antes se ignoraba)", any(k_hip in x for x in r["discrepancias"]) and not r["apto_por_entradas"], r["discrepancias"][:1])
r = con(lambda g: ent(g, k_hip).setdefault("comprobacion", {}).update(resultado="pendiente", revisor=None, nota="(prueba) texto sustituido, pendiente de confirmación del revisor"))
paso("H", "(14-nov) una hipótesis con la comprobación explícitamente pendiente: pendiente, no apta (antes contaba como comprobada)", any(k_hip in x for x in r["pendientes"]) and not r["apto_por_entradas"], r["pendientes"][:1])
r = con(lambda g: ent(g, k_dato).update(clase="dato_ausente", justificacion="(prueba)"))
paso("Z", "dato ausente con un valor en el libro: error (es un dato o un cero que hay que contrastar)", any(k_dato in x and "ausente" in x for x in r["errores"]), r["errores"][:1])
r = con(lambda g: ent(g, k_dato).update(clase="cero_comprobado"))
paso("Z", "cero comprobado con un valor distinto de cero: error", any(k_dato in x and "cero" in x for x in r["errores"]), r["errores"][:1])
k_na = next((e["celda"] for e in ents if e["clase"] == "no_aplicable"), None)
if k_na:
    r = con(lambda g: ent(g, k_na).update(justificacion=""))
    paso("Z", "no aplicable sin justificación: pendiente", any(k_na in x for x in r["pendientes"]), r["pendientes"][:1])
open(os.path.join(c, "fuentes_sinteticas", "fuente.txt"), "w", encoding="utf-8").write("".join(f"[PDF PAGE {i + 1}]\n{p}\n" for i, p in enumerate(paginas)))
r = con(lambda g: ent(g, k_dato)["fuente"].update(pagina="1" if ent(g, k_dato)["fuente"]["pagina"] != "1" else "2"))
paso("T", "cita que no está en la página citada: discrepancia", any(k_dato in x and "página" in x for x in r["discrepancias"]), r["discrepancias"][:1])
r = con(lambda g: ent(g, k_dato)["fuente"].update(valor_fuente=ent(g, k_dato)["fuente"]["valor_fuente"], cita=ent(g, k_dato)["fuente"]["cita"].split(":")[0]))
paso("T", "cita sin el valor de la fuente: discrepancia (los dígitos tienen que estar en el pasaje citado)", not r["apto_por_entradas"], (r["discrepancias"] + r["errores"])[:1])

# (14-nov, revisión del extractor de Viscofan) vacío ≠ cero y la cifra completa en la cita
def _pagina(texto):
    paginas.append(texto)
    open(os.path.join(c, "fuentes_sinteticas", "fuente.txt"), "w", encoding="utf-8").write("".join(f"[PDF PAGE {i + 1}]\n{p}\n" for i, p in enumerate(paginas)))
    return str(len(paginas))


k_vacia = next((e["celda"] for e in ents if inst["celdas"].get(e["celda"]) is None and e["celda"].startswith("Historia!") and e["clase"] in ("dato_ausente", "no_aplicable")), None)
if k_vacia:
    pv = _pagina(f"Partida sintética de {k_vacia}: 0")
    r = con(lambda g: ent(g, k_vacia).update(clase="cero_comprobado", valor_modelo=None, fuente=dict(ent(g, k_dato)["fuente"], valor_fuente=0, pagina=pv,
                                                                                                    cita=f"Partida sintética de {k_vacia}: 0", periodo=ent(g, k_dato)["fuente"]["periodo"])))
    paso("Z", "cero comprobado con la celda VACÍA en el libro: discrepancia (vacío no es cero; antes pasaba)", any(k_vacia in x and "vacía" in x for x in r["discrepancias"]), (r["discrepancias"] + r["errores"])[:1])
else:
    paso("Z", "cero comprobado con la celda vacía: hay una celda vacía en el universo para probarlo", False, "sin celda vacía")
vf0 = ent(REG, k_dato)["fuente"]["valor_fuente"]
pe = _pagina(f"Partida sintética de {k_dato}: 9{vf0:.3f}9")
r = con(lambda g: ent(g, k_dato)["fuente"].update(pagina=pe, cita=f"Partida sintética de {k_dato}: 9{vf0:.3f}9"))
paso("T", "el valor solo aparece DENTRO de otra cifra de la cita: discrepancia (antes pasaba por coincidencia de dígitos)", any(k_dato in x and "cifra completa" in x for x in r["discrepancias"]), r["discrepancias"][:1])
pf = _pagina(f"Partida sintética de {k_dato}: {vf0:,.3f}".replace(",", " ").replace(".", ","))
r = con(lambda g: ent(g, k_dato)["fuente"].update(pagina=pf, cita=f"Partida sintética de {k_dato}: {vf0:,.3f}".replace(",", " ").replace(".", ",")))
paso("T", "cifra con miles separados por espacio y coma decimal (francés): aceptada", r["apto_por_entradas"], (r["discrepancias"] + r["errores"])[:1])
assert VE._cita_contiene("Acquisitions  -   (12.3)", 0) and not VE._cita_contiene("Ejercicio 2019", 0) and not VE._cita_contiene("año 2012", 12) and VE._cita_contiene("4 573,7", 4573.7) and not VE._cita_contiene("Résultat - 12,3", 0) and not VE._cita_contiene("Résultat -12,3", 0) and VE._cita_contiene("Closing balance 1.662 784.366 - 784.366", 0) and VE._cita_contiene("Revenue 20.1 912.160 849.697", 849697) and VE._cita_contiene("Note 2017 2016", 2016) and VE._cita_contiene("VISCOFAN F 54,3000 02-11-26 55,3000 54,5000 54,7000 54,8454", 54.7)
paso("T", "cero impreso como «-» aceptado; el «0» de «2019» y el «12» de «2012» no cuentan; columnas a un espacio («912.160 849.697») sí", True)

# G · puerta en las salidas (llamadas a mano, modo provisional sobre la copia)
env = dict(os.environ, MUNGER_CONFIG=CFG)


def salidas():
    r1 = subprocess.run([sys.executable, "-B", os.path.join(PV, "scripts", "ficha.py"), c, "--provisional"], capture_output=True, text=True, env=env)
    r2 = subprocess.run([sys.executable, "-B", os.path.join(PV, "scripts", "informe.py"), c, "--provisional"], capture_output=True, text=True, env=env)
    F = json.load(open(os.path.join(c, "ficha_provisional.json"), encoding="utf-8")) if os.path.exists(os.path.join(c, "ficha_provisional.json")) else {}
    inf = open(os.path.join(c, "informe_provisional.md"), encoding="utf-8").read() if os.path.exists(os.path.join(c, "informe_provisional.md")) else ""
    return r1.returncode, r2.returncode, F.get("aptitud_de_uso") or {}, inf


os.remove(os.path.join(c, VE.REGISTRO))
rf, ri, apt, inf = salidas()
paso("G", "sin registro: la ficha y el informe dicen «apta por entradas: no» y nunca «apta para dinero real»",
     rf == 0 and ri == 0 and (apt.get("verificacion_entradas") or {}).get("apto_por_entradas") is False and apt.get("apto_para_dinero_real") is False
     and "apta por entradas: no" in inf and "Apta para dinero real: no" in inf, f"{rf}/{ri} · {apt.get('motivos_no_apto')}")
con()
rf, ri, apt, inf = salidas()
paso("G", "con el registro completo: apta por entradas, pero la conclusión sigue sin presentarse como apta para dinero real (condición necesaria, no suficiente)",
     rf == 0 and ri == 0 and (apt.get("verificacion_entradas") or {}).get("apto_por_entradas") is True and apt.get("apto_para_dinero_real") is False
     and "apta por entradas: sí" in inf and "Apta para dinero real: no" in inf, f"{rf}/{ri} · {apt.get('motivos_no_apto')}")

# M · el registro es material: cambiarlo invalida la aprobación
import pipeline as PL  # noqa: E402
cm = os.path.join(TMP, "viscofan_m", "Viscofan")  # copia nueva: G regeneró material provisional en la primera
shutil.copytree(os.path.join(E413, "viscofan", "Viscofan"), cm, ignore=shutil.ignore_patterns(".lo_perfil", "variantes_v64", "recalc", "prompts_generados", "__pycache__"))
vig0 = CIE.motivo_vigencia(cm, PL.Pipeline.veredicto_auditoria)
shutil.copytree(os.path.join(c, "fuentes_sinteticas"), os.path.join(cm, "fuentes_sinteticas"))
json.dump(REG, open(os.path.join(cm, VE.REGISTRO), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
vig1 = CIE.motivo_vigencia(cm, PL.Pipeline.veredicto_auditoria)
paso("M", "el registro forma parte del material auditado: añadirlo o cambiarlo después de la auditoría retira la aprobación", vig0 is None and vig1 is not None and "material" in vig1,
     f"antes: {vig0!r:.60} · después: {str(vig1)[:120]}")

n_ok = sum(x["resultado"] == "PASA" for x in RES)
print(f"{n_ok}/{len(RES)} pruebas de la verificación de las entradas (4.14) PASAN")
print("RESULTADO verificación de las entradas: " + ("PASA" if n_ok == len(RES) else "FALLA"))
if ARGS.json:
    json.dump(RES, open(ARGS.json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
shutil.rmtree(TMP, ignore_errors=True)
sys.exit(0 if n_ok == len(RES) else 1)
