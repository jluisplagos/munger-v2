#!/usr/bin/env python3
"""s9 · I20: la ficha y el informe con el bloque nuevo, en copias temporales de expedientes reales (ficha.py e informe.py --provisional, como
la batería; sin pipeline ni LibreOffice).
A) V6.3 (Elis, motor A, copia de elis_decisiones): registro real (no apto con las reglas 4.15) → línea del informe;
B) V6.3 con un registro SINTÉTICO completo y apto que incluye 1 derivado, 1 entrada de juicio no material y 1 lectura externa no material:
   ¿qué dice el informe V6.3 de lo que no se contrastó? (en la V6.4 el párrafo de aptitud lo detalla: N1/N2/U1);
C) modo aplicado ≠ modo declarado y declaración ilegible: lo que muestran la ficha y el informe; ¿algo lo bloquea?
D) V6.4.1 (Viscofan, copia de viscofan_decisiones): las dos líneas (I20 y aptitud de uso);
E) esquema: fichas nuevas y fichas oficiales anteriores (4.14) contra el esquema nuevo; una ficha sin el bloque nuevo también valida;
F) verify_quotes_v2.py sobre los informes generados (como verificar_todo.sh)."""
import copy, hashlib, json, os, re, shutil, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import VE, PV, F

E414 = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_14")
TMP = tempfile.mkdtemp(prefix="rev_fable_s9_", dir=os.path.join(F, "tmp"))
IGN = shutil.ignore_patterns(".lo_perfil", "recalc", "variantes_v64", "prompts_generados", "historial_cierres", "antecedentes", "__pycache__")
ENV = dict(os.environ)


def salidas(d, env=None):
    r1 = subprocess.run([sys.executable, "-B", os.path.join(PV, "scripts", "ficha.py"), d, "--provisional"], capture_output=True, text=True, env=env or ENV)
    r2 = subprocess.run([sys.executable, "-B", os.path.join(PV, "scripts", "informe.py"), d, "--provisional"], capture_output=True, text=True, env=env or ENV)
    fi = json.load(open(os.path.join(d, "ficha_provisional.json"), encoding="utf-8")) if os.path.exists(os.path.join(d, "ficha_provisional.json")) else {}
    inf = open(os.path.join(d, "informe_provisional.md"), encoding="utf-8").read() if os.path.exists(os.path.join(d, "informe_provisional.md")) else ""
    rv = subprocess.run([sys.executable, "-B", os.path.join(PV, "scripts", "validar_esquema.py"), os.path.join(d, "ficha_provisional.json"), "ficha"], capture_output=True, text=True)
    return fi, inf, (r1.returncode, r2.returncode, rv.returncode, (r1.stdout + r1.stderr)[-200:].strip(), (r2.stdout + r2.stderr)[-200:].strip(), rv.stdout[-200:].strip())


def linea(inf, rotulo="Entradas financieras:"):
    m = re.search(r"> \*\*" + re.escape(rotulo) + r".*", inf)
    return m.group(0) if m else "(sin línea)"


def registro_sintetico(c):
    """El fixture de la batería, sobre la carpeta c: registro sintético completo y positivo (no verifica ningún dato real)."""
    f1p = os.path.join(c, "fase1_v63.json")
    f1 = json.load(open(f1p, encoding="utf-8"))
    for k, (vl, vf, m) in VE.entradas_no_reproducibles(c, VE.universo(c)).items():
        d = f1.setdefault("analisis", {}).get(k.split("!")[1])
        f1["analisis"][k.split("!")[1]] = dict(d, valor=vl) if isinstance(d, dict) else {"valor": vl, "fuente": "(fixture sintético) valor efectivo del libro"}
    json.dump(f1, open(f1p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    inst = VE.universo(c)
    anios = [inst["celdas"].get(f"Historia!{x}5") for x in "CDEFGHIJKL"]
    fs = os.path.join(c, "fuentes_sinteticas")
    os.makedirs(fs, exist_ok=True)
    paginas = []

    def fuente_para(k, v):
        n = len(paginas) + 1
        m = re.match(r"^Historia!([C-L])(\d+)$", k)
        periodo = f"ejercicio {int(anios['CDEFGHIJKL'.index(m.group(1))])}" if m else "31-dic-2025"
        if isinstance(v, (int, float)) and not isinstance(v, bool):
            if m and int(m.group(2)) == 5:
                vf, unidad, escala, cita = v, "año", 1.0, f"Ejercicio {int(v)}"
            else:
                vf, unidad, escala = round(v * 1000, 6), "miles de euros", 0.001
                if abs(vf * 0.001 - v) > 1e-12 * max(1.0, abs(v)) or (VE._decimales_exactos(vf) or 0) > 3:
                    vf, unidad, escala = v, "mm", 1.0  # (revisor) valores con más precisión que el milésimo de miles: se citan en mm, exactos
                cita = f"Partida sintética de {k}: {vf:.{max(3, VE._decimales_exactos(vf) or 0)}f}"
        else:
            vf, unidad, escala, cita = v, "texto", 1.0, f"Dato sintético de {k}: {v}"
        paginas.append(cita)
        return {"documento": "Fuente sintética de la prueba (no es un documento de la empresa)", "archivo": "fuentes_sinteticas/fuente.txt", "sha256": "__actual__",
                "version": "sintética 1", "pagina": str(n), "ubicacion": "tabla sintética", "concepto": f"concepto de {k}", "columna": periodo, "periodo": periodo,
                "unidad": unidad, "escala": escala, "signo": 1, "tratamiento": "ninguno", "perimetro": "consolidado", "reexpresado": "no aplica",
                "valor_fuente": vf, "cita": cita}

    comprobada = {"extractor": "extractor sintético", "revisor": "revisor sintético", "fecha": "2026-11-15", "resultado": "verificado",
                  "fuente_examinada": "fuentes_sinteticas/fuente.txt (página citada)", "nota": None}
    ents = []
    for k, v in inst["celdas"].items():
        t = inst["tipos"].get(k)
        e = {"celda": k, "id": inst["ids"].get(k), "ambito": inst["ambito"].get(k), "uso": "prueba", "material": True, "valor_modelo": v, "comprobacion": dict(comprobada), "incidencia": None}
        if t in ("hipótesis", "configuracion"):
            e.update(clase="hipotesis" if t == "hipótesis" else "convencion", hipotesis={"fundamento": "(prueba)", "alternativas": ["(prueba)"], "limites": ["(prueba)"]})
        elif v is None or v == "":
            e.update(clase="no_aplicable", justificacion="(prueba) celda vacía del libro: no aplica a este expediente")
        elif isinstance(v, (int, float)) and v == 0:
            e.update(clase="cero_comprobado", fuente=fuente_para(k, v))
        else:
            e.update(clase="dato_publicado", fuente=fuente_para(k, v))
        ents.append(e)
    reg = {"formato": VE.FORMATO, "empresa": os.path.basename(c), "nota": "REGISTRO SINTÉTICO DE PRUEBA (no verifica ningún dato real)", "perimetro_del_expediente": "consolidado",
           "huella_entradas_economicas": inst["huella"], "entradas": ents}
    return reg, paginas, comprobada


def escribir(c, reg, paginas):
    open(os.path.join(c, "fuentes_sinteticas", "fuente.txt"), "w", encoding="utf-8").write("".join(f"[PDF PAGE {i + 1}]\n{p}\n" for i, p in enumerate(paginas)))
    sha = hashlib.sha256(open(os.path.join(c, "fuentes_sinteticas", "fuente.txt"), "rb").read()).hexdigest()
    for e in reg["entradas"]:
        f = e.get("fuente") or {}
        if isinstance(f, dict) and f.get("archivo") == "fuentes_sinteticas/fuente.txt":
            f["sha256"] = sha
    hs = VE.huellas_registro(c, reg)
    for e in reg["entradas"]:
        cmp_ = e.setdefault("comprobacion", {})
        cmp_["vinculo"] = {"huella": hs[e["celda"]], "sellado_por": cmp_.get("revisor"), "fecha": cmp_.get("fecha")}
    json.dump(reg, open(os.path.join(c, VE.REGISTRO), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)


def ent(reg, k):
    return next(e for e in reg["entradas"] if e["celda"] == k)


print("== A · V6.3 (Elis, copia de elis_decisiones) con su registro real")
dA = os.path.join(TMP, "A", "Elis")
shutil.copytree(os.path.join(E414, "elis_decisiones", "Elis"), dA, ignore=IGN)
fi, inf, rcs = salidas(dA)
print("   códigos (ficha, informe, esquema):", rcs[:3], "| plantilla:", fi.get("versiones", {}).get("plantilla"), "| claves de aptitud:", [k for k in ("aptitud_de_uso", "verificacion_entradas") if k in fi])
print("   informe:", linea(inf)[:700])

print("\n== B · V6.3 con un registro sintético completo y apto, con 1 derivado, 1 de juicio no material revisada y 1 lectura externa no material")
dB = os.path.join(TMP, "B", "Elis")
shutil.copytree(os.path.join(E414, "elis_decisiones", "Elis"), dB, ignore=IGN)
reg, paginas, comprobada = registro_sintetico(dB)
escribir(dB, reg, paginas)
r = VE.comprobar(dB)
print("   control positivo:", r["apto_por_entradas"], r["resumen"][:200], (r["errores"] + r["discrepancias"] + r["pendientes"])[:2])
fi, inf, rcs = salidas(dB)
print("   informe (apto, sin nada que declarar):", linea(inf)[:400])
# 1 derivado: un dato de cálculo sin fuente, escrito con cifras admitidas a partir del año (U1)
anio_k = "Historia!F5"
k_der = next(e["celda"] for e in reg["entradas"] if e["clase"] == "dato_publicado" and e["ambito"] == "calculo" and re.match(r"^Historia![C-L](6|7|8)$", e["celda"]) and isinstance(e["valor_modelo"], float))
v_der, v_anio = ent(reg, k_der)["valor_modelo"], ent(reg, anio_k)["valor_modelo"]
from fractions import Fraction as Fr
dif = Fr(repr(float(v_anio))) - Fr(repr(float(v_der)))
ent_, dec = divmod(dif, 1)
digs = [f"{int(c)}*{10 ** (len(str(ent_)) - i - 1)}" for i, c in enumerate(str(ent_)) if c != "0"] + [f"{c}/{10 ** (i + 1)}" for i, c in enumerate(f"{float(dec):.3f}"[2:]) if c != "0"]
formula = f'o["{anio_k}"] - (' + " + ".join(digs) + ")"
ent(reg, k_der).update(clase="derivado", fuente={}, derivacion={"origenes": [anio_k], "formula": formula, "conciliacion": "(prueba) derivado del año", "unidad": "mm"})
# 1 entrada de juicio no material con el juicio de materialidad revisado, y 1 lectura externa no material
kj = [e["celda"] for e in reg["entradas"] if e["ambito"] == "juicio" and e["clase"] == "dato_publicado" and isinstance(e["valor_modelo"], (int, float))][:2]
for k in kj:
    ent(reg, k)["material"] = False
    ent(reg, k)["justificacion_materialidad"] = "(prueba) cifra de contexto que el juicio no usa para concluir nada"
f = ent(reg, kj[1])["fuente"]
for x in ("archivo", "sha256"):
    f.pop(x, None)
f.update(conservacion="externa", lectura_externa={"referencia": "https://ejemplo.invalid/serie", "fecha": "2026-11-15", "evidencia": "transcripción", "limitaciones": "sin bytes"})
ent(reg, kj[0])["comprobacion"]["resultado"] = "pendiente"  # no comprobada; solo la materialidad…
ent(reg, kj[0])["comprobacion"] = dict(comprobada)  # …se deja comprobada: no material pero comprobada
escribir(dB, reg, paginas)
r = VE.comprobar(dB)
print(f"   derivado {k_der} = {formula} (valor {v_der}); no materiales {kj}")
print("   comprobar:", r["apto_por_entradas"], "|", r["resumen"])
print("   errores/discrepancias/pendientes:", (r["errores"] + r["discrepancias"] + r["pendientes"])[:3])
fi, inf, rcs = salidas(dB)
ve = fi.get("verificacion_entradas") or {}
print("   ficha.verificacion_entradas.resumen (recuentos):", {k: (ve.get("resumen") or {}).get(k) for k in ("comprobadas_universo", "universo", "derivados_comprobados", "no_materiales", "no_materiales_sin_revisar", "lecturas_externas", "datos_como_hipotesis", "no_aplicables")})
print("   informe V6.3:", linea(inf)[:600])
print("   ¿el informe V6.3 menciona derivados, no materiales, lecturas externas o no aplicables?:", {p: (p in inf) for p in ("derivados comprobados", "no materiales", "lecturas externas", "no aplicables")})

print("\n== C · modo aplicado en el paso 2 ≠ modo declarado ahora; y declaración ilegible")
st_p = os.path.join(dB, "estado_pipeline.json")
st = json.load(open(st_p, encoding="utf-8"))
st["entrada_efectiva"] = {"modo": "estricta", "declarado_en": "entrada_efectiva.json"}
json.dump(st, open(st_p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump({"modo": "registrada", "motivo": "(prueba) se conserva el valor migrado", "fecha": "2026-11-15"}, open(os.path.join(dB, "entrada_efectiva.json"), "w", encoding="utf-8"))
fi, inf, rcs = salidas(dB)
print("   ficha.entrada_efectiva:", (fi.get("verificacion_entradas") or {}).get("entrada_efectiva"), "| apto_por_entradas:", (fi.get("verificacion_entradas") or {}).get("apto_por_entradas"), "| esquema:", rcs[2])
print("   informe:", linea(inf)[:520])
open(os.path.join(dB, "entrada_efectiva.json"), "w").write("{ilegible")
fi, inf, rcs = salidas(dB)
print("   ilegible → ficha.entrada_efectiva:", (fi.get("verificacion_entradas") or {}).get("entrada_efectiva"), "| apto_por_entradas:", (fi.get("verificacion_entradas") or {}).get("apto_por_entradas"), "| esquema:", rcs[2])
print("   informe:", linea(inf)[:520])
os.remove(os.path.join(dB, "entrada_efectiva.json"))
usos = subprocess.run(["grep", "-rn", "coinciden", os.path.join(PV, "scripts"), "--include=*.py", "--include=*.sh"], capture_output=True, text=True).stdout
print("   usos de «coinciden» en scripts/ (¿algún control lo consulta?):")
for l in usos.splitlines():
    print("      ", l.replace(os.path.join(PV, "scripts") + os.sep, "")[:170])

print("\n== D · V6.4.1 (Viscofan, copia de viscofan_decisiones)")
dD = os.path.join(TMP, "D", "Viscofan")
shutil.copytree(os.path.join(E414, "viscofan_decisiones", "Viscofan"), dD, ignore=IGN)
env64 = dict(os.environ, MUNGER_CONFIG=os.path.join(PV, "config_v2_v641_experimental.json"))
fi, inf, rcs = salidas(dD, env64)
print("   códigos (ficha, informe, esquema):", rcs[:3], rcs[3][:120], "| plantilla:", fi.get("versiones", {}).get("plantilla"))
print("   informe (I20):", linea(inf)[:420])
print("   informe (aptitud):", linea(inf, "Aptitud de uso")[:60], "…", (re.findall(r"Verificación de las entradas financieras:.{0,330}", inf) or [""])[0])
a1 = (fi.get("verificacion_entradas") or {}).get("apto_por_entradas")
a2 = ((fi.get("aptitud_de_uso") or {}).get("verificacion_entradas") or {}).get("apto_por_entradas")
print("   apto_por_entradas en los dos bloques de la ficha:", a1, a2, "| «apta por entradas» en el informe:", re.findall(r"apta por entradas: (sí|no)", inf))

print("\n== E · esquema nuevo con fichas oficiales anteriores (4.14) y con una ficha nueva sin el bloque")
for exp in ("elis_decisiones/Elis", "viscofan_decisiones/Viscofan", "vidrala_decisiones/Vidrala"):
    p = os.path.join(E414, exp, "ficha.json")
    rv = subprocess.run([sys.executable, "-B", os.path.join(PV, "scripts", "validar_esquema.py"), p, "ficha"], capture_output=True, text=True)
    print(f"   {exp}/ficha.json (4.14, sin el bloque): código {rv.returncode} {rv.stdout.strip()[:100]}")
fi2 = dict(fi)
fi2.pop("verificacion_entradas", None)
p2 = os.path.join(TMP, "ficha_sin_bloque.json")
json.dump(fi2, open(p2, "w", encoding="utf-8"), ensure_ascii=False)
rv = subprocess.run([sys.executable, "-B", os.path.join(PV, "scripts", "validar_esquema.py"), p2, "ficha"], capture_output=True, text=True)
print(f"   ficha nueva (4.15, hito 2) a la que se le quita el bloque verificacion_entradas: código {rv.returncode} {rv.stdout.strip()[:100]}  (0 = el esquema no lo exige)")
fi3 = copy.deepcopy(fi)
fi3["verificacion_entradas"]["apto_para_dinero_real"] = True
p3 = os.path.join(TMP, "ficha_dinero_real.json")
json.dump(fi3, open(p3, "w", encoding="utf-8"), ensure_ascii=False)
rv = subprocess.run([sys.executable, "-B", os.path.join(PV, "scripts", "validar_esquema.py"), p3, "ficha"], capture_output=True, text=True)
print(f"   ficha con verificacion_entradas.apto_para_dinero_real = true: código {rv.returncode} {rv.stdout.strip()[:140]}")
fi4 = copy.deepcopy(fi)
fi4["aptitud_de_uso"]["apto_para_dinero_real"] = True
p4 = os.path.join(TMP, "ficha_dinero_real2.json")
json.dump(fi4, open(p4, "w", encoding="utf-8"), ensure_ascii=False)
rv = subprocess.run([sys.executable, "-B", os.path.join(PV, "scripts", "validar_esquema.py"), p4, "ficha"], capture_output=True, text=True)
print(f"   ficha con aptitud_de_uso.apto_para_dinero_real = true (bloque de la 4.14): código {rv.returncode} {rv.stdout.strip()[:140]}")

print("\n== F · verify_quotes_v2.py sobre los informes provisionales generados (como verificar_todo.sh)")
cfgp = os.path.join(PV, "config_v2.json")
munger = subprocess.run([sys.executable, "-B", os.path.join(PV, "scripts", "config_v2.py"), "kit_v1.corpus_munger", cfgp], capture_output=True, text=True).stdout.strip()
damo = subprocess.run([sys.executable, "-B", os.path.join(PV, "scripts", "config_v2.py"), "corpus.damodaran", cfgp], capture_output=True, text=True).stdout.strip()
print("   corpus:", os.path.exists(munger), os.path.exists(damo))
for nombre, d in (("A (V6.3, registro real)", dA), ("B (V6.3, sintético)", dB), ("D (V6.4.1)", dD)):
    rq = subprocess.run([sys.executable, "-B", os.path.join(PV, "scripts", "verify_quotes_v2.py"), "--corpus", munger, "--corpus", damo, "--paginas-estrictas", os.path.join(d, "informe_provisional.md")], capture_output=True, text=True)
    print(f"   {nombre}: código {rq.returncode} · {(rq.stdout.strip().splitlines() or [''])[0][:120]} · {(rq.stdout.strip().splitlines() or [''])[-1][:120]}")
shutil.rmtree(TMP, ignore_errors=True)
