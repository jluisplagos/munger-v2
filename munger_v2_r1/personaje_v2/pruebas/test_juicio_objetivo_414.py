"""Batería del contrato 4.14 del juicio propio sobre el OBJETIVO (encargo de cierre §5; S3 y S11 de la segunda revisión interna de la 4.13).

Trabaja sobre copias de los tres expedientes cerrados de la 4.13 (vidrala_condicionado, vidrala_bloqueo y viscofan) y llama a la coherencia de
la fase C del pipeline (Pipeline.coherencia_fase_c) sin ejecutar ningún paso, sin LibreOffice y sin agentes. Los bloques `juicio_objetivo` se
construyen en la prueba a partir de las fases C reales (con el contraste mecánico de objetivo_v64), y cada caso cambia una sola cosa.

Casos (diseño del frente B, `materialidad_objetivo_diseno.md` §4):
  L  legado: sin el contrato 4.14 en el estado, las fases C de la 4.13 siguen siendo coherentes (los cierres no se reabren; A15)
  P  control positivo: con el contrato y bloques completos, coherente; condicionantes iguales a los del objetivo declarado
  S3 «no material» por juicio de un parámetro sin fundamento cuyo contraste mueve el objetivo, sin comparación: rechazo (A4); con
     «no_determinada»: coherente y condiciona (control); con comparación declarada y coherente: aceptado (A5); con un valor falso: rechazo (A6)
  S11 criterio propio del agente marcado «calculada»: rechazo (A11); como juicio con su descripción: aceptado y visible como criterio propio
  V  contrato: contraste que no es el calculado (A9), atribuible cambiado, cobertura distinta, límites vacíos, política inventada (A10),
     bloque ausente con el contrato, campos 4.13 que no coinciden con el bloque, «calculada» sin contraste atribuible (A8)
  D10 una entrada D10 sigue condicionando aunque su parámetro se juzgue «no material» (A12)
  E  presentación: la ficha (bloque objetivo) y el informe §14 muestran el juicio sobre el objetivo y el criterio propio como no adoptado
Uso: python3 -B test_juicio_objetivo_414.py [--json salida.json]
"""
import argparse, copy, json, os, shutil, sys, tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
PV = os.path.dirname(AQUI)
sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
sys.path.insert(0, os.path.join(PV, "scripts"))
import objetivo_v64 as OBJ  # noqa: E402
import pipeline as P  # noqa: E402
import config_v2  # noqa: E402
import seleccion_plantilla as SEL  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--json")
ARGS = ap.parse_args()
E413 = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_13")
CFG = {"vidrala_condicionado": os.path.join(PV, "config_v2_v64_experimental.json"), "vidrala_bloqueo": os.path.join(PV, "config_v2_v64_experimental.json"),
       "viscofan": os.path.join(PV, "config_v2_v641_experimental.json")}
TMP = tempfile.mkdtemp(prefix="juicio_objetivo_414_")
RES = []


def paso(grupo, nombre, ok, detalle=""):
    RES.append({"grupo": grupo, "prueba": nombre, "resultado": "PASA" if ok else "FALLA", "detalle": str(detalle)[:400]})
    print(f"[{grupo}] {'PASA ' if ok else 'FALLA'} {nombre}" + (f" · {str(detalle)[:260]}" if detalle else ""))


def copia(nombre):
    orig = os.path.join(E413, nombre, "Viscofan" if nombre == "viscofan" else "Vidrala")
    c = os.path.join(TMP, nombre, os.path.basename(orig))
    shutil.copytree(orig, c, ignore=shutil.ignore_patterns(".lo_perfil", "variantes_v64", "recalc", "prompts_generados", "historial_cierres", "__pycache__"))
    return c


class Caso:
    def __init__(self, nombre):
        self.c = copia(nombre)
        os.environ["MUNGER_CONFIG"] = CFG[nombre]
        self.pp = P.Pipeline(self.c, config_v2.cargar(CFG[nombre]))
        self.fc = json.load(open(os.path.join(self.c, "fase_c.json"), encoding="utf-8"))
        self.var = json.load(open(os.path.join(self.c, "configuracion_v64_variantes.json"), encoding="utf-8"))
        self.conf = SEL.configuracion(self.c) or {}
        self.psi = json.load(open(os.path.join(self.c, "precio.json"), encoding="utf-8")).get("precio_si")

    def coh(self, fc, contrato=True):
        self.pp.st["contrato_juicio_objetivo"] = OBJ.FORMATO_JUICIO_OBJETIVO if contrato else None
        return self.pp.coherencia_fase_c(copy.deepcopy(fc))

    def par(self, fc, k):
        return next(q for q in fc["configuracion_v64"]["parametros"] if q["clave"] == k)

    def bloque(self, p):
        """Bloque 4.14 que corresponde a un parámetro de una fase C 4.13 (sin inventar fundamento: los textos nuevos son de prueba)."""
        k = p["clave"]
        cb = OBJ.cobertura(self.var, k, self.conf)
        base, mat = p.get("base_de_la_materialidad_objetivo"), p.get("material_para_objetivo")
        calc = OBJ.contraste_objetivo(self.var, cb, self.psi)
        mueve = any(c["atribuible"] and c["delta_eur"] is not None and round(c["delta_eur"], 2) != 0 for c in calc)
        crit = {"origen": "redondeo_declarado" if (base == "calculada" and mat is True and mueve) else "ninguno", "descripcion": None, "referencia": None}
        return {"hipotesis": f"(prueba) el valor activo de {k} sostiene el objetivo declarado", "contraste": calc, "cobertura": (cb or {}).get("tipo"),
                "limites": ["(prueba) alternativas no calculadas y extremos del dominio"], "base": base, "material": mat, "criterio": crit,
                "comparado_con": None, "razonamiento": list(p.get("inferencias") or []) or ["(prueba) razonamiento del objetivo"],
                "evidencia": list(p.get("evidencia") or []) or ["(prueba) configuracion_v64_variantes.md"]}

    def con_bloques(self, ajustar=None):
        """Fase C con un bloque por parámetro; los juicios que el contrato 4.14 rechazaría (S3 y S11) se pasan a «no_determinada» para el
        control positivo, y el objetivo declarado se actualiza con los condicionantes resultantes."""
        x = copy.deepcopy(self.fc)
        for p in x["configuracion_v64"]["parametros"]:
            p["juicio_objetivo"] = self.bloque(p)
            if OBJ.validar_juicio_objetivo(p["clave"], p, OBJ.cobertura(self.var, p["clave"], self.conf), self.var, self.psi):
                p["juicio_objetivo"].update(base="no_determinada", material=None, comparado_con=None,
                                            criterio={"origen": "ninguno", "descripcion": None, "referencia": None})
                p.update(material_para_objetivo=None, base_de_la_materialidad_objetivo="no_determinada",
                         material_para_conclusion=p.get("material_para_accion") is True)
        if ajustar:
            ajustar(x)
        ob = x["configuracion_v64"].get("objetivo") or {}
        ob["hipotesis_que_condicionan"] = OBJ.condicionantes(x, self.conf)
        return x


casos = {n: Caso(n) for n in ("vidrala_condicionado", "vidrala_bloqueo", "viscofan")}

# ---------- L · legado ----------
for n, k in casos.items():
    m = k.coh(k.fc, contrato=False)
    paso("L", f"{n}: sin el contrato 4.14 en el estado, la fase C cerrada de la 4.13 sigue siendo coherente (no se reabre)", m is None, m)

# ---------- P · control positivo ----------
pos = {}
for n, k in casos.items():
    x = k.con_bloques()
    pos[n] = x
    m = k.coh(x)
    paso("P", f"{n}: con el contrato 4.14 y bloques completos (los juicios S3/S11 como «no_determinada»), la fase C es coherente", m is None, m)

# ---------- S3 ----------
k = casos["viscofan"]
S3 = [p["clave"] for p in k.fc["configuracion_v64"]["parametros"] if p.get("fundamento_suficiente") is False and p.get("material_para_objetivo") is False
      and p.get("base_de_la_materialidad_objetivo") == "juicio_economico"]
paso("S3", "viscofan: los juicios S3 de la segunda revisión (sin fundamento, «no material» por juicio) son los esperados", set(S3) >= {"PM1.roic_terminal"}, S3)
k3 = "PM1.roic_terminal"
x = copy.deepcopy(pos["viscofan"])
p = k.par(x, k3)
p["juicio_objetivo"] = k.bloque(k.par(k.fc, k3))
p.update(material_para_objetivo=False, base_de_la_materialidad_objetivo="juicio_economico")
m = k.coh(x) or ""
paso("S3", f"viscofan {k3}: «no material» por juicio sin comparación declarada, con un contraste que mueve el precio de Sí: rechazo (A4)", "exige comparado_con" in m, m)
paso("S3", f"viscofan {k3}: como «no_determinada» condiciona el objetivo (control)", k3 in OBJ.condicionantes(pos["viscofan"], k.conf), OBJ.condicionantes(pos["viscofan"], k.conf))
amp = OBJ.amplitud_rango(k.var)
p["juicio_objetivo"]["comparado_con"] = {"referencia": "rango_calculado", "valor_eur": round(amp, 2), "fuente": "configuracion_v64_variantes.md (amplitud del rango calculado)"}
x["configuracion_v64"]["objetivo"]["hipotesis_que_condicionan"] = OBJ.condicionantes(x, k.conf)
m = k.coh(x)
paso("S3", f"viscofan {k3}: con la comparación declarada y coherente con el rango calculado, el contrato se cumple (la pertinencia es de la auditoría; A5)", m is None, m)
p["juicio_objetivo"]["comparado_con"]["valor_eur"] = round(amp, 2) + 1.0
m = k.coh(x) or ""
paso("S3", f"viscofan {k3}: con un valor de comparación que no es la amplitud del rango: rechazo (A6)", "amplitud del rango calculado" in m, m)
k = casos["vidrala_condicionado"]
x = copy.deepcopy(pos["vidrala_condicionado"])
p = k.par(x, k3)
p["juicio_objetivo"] = k.bloque(k.par(k.fc, k3))
p.update(material_para_objetivo=False, base_de_la_materialidad_objetivo="juicio_economico")
m = k.coh(x) or ""
paso("S3", f"vidrala_condicionado {k3}: el mismo rechazo (+1,06 € sin comparación declarada)", "exige comparado_con" in m, m)

# ---------- S11 ----------
k = casos["vidrala_bloqueo"]
x = copy.deepcopy(pos["vidrala_bloqueo"])
p = k.par(x, "N1.tipo")
orig = k.par(k.fc, "N1.tipo")
p["juicio_objetivo"] = k.bloque(orig)
p["juicio_objetivo"].update(base="calculada", material=True, criterio={"origen": "juicio_propio_del_agente", "descripcion": "mi criterio de 1,5 €", "referencia": None})
p.update(material_para_objetivo=True, base_de_la_materialidad_objetivo="calculada", material_para_conclusion=True)
m = k.coh(x) or ""
paso("S11", "vidrala_bloqueo N1.tipo: un criterio propio del agente (1,5 €) marcado «calculada»: rechazo (A11)", "criterio" in m and ("juicio_economico" in m or "S11" in m), m)
p["juicio_objetivo"]["base"] = "juicio_economico"
p["base_de_la_materialidad_objetivo"] = "juicio_economico"
x["configuracion_v64"]["objetivo"]["hipotesis_que_condicionan"] = OBJ.condicionantes(x, k.conf)
m = k.coh(x)
paso("S11", "vidrala_bloqueo N1.tipo: el mismo criterio como juicio económico con su descripción: el contrato se cumple", m is None, m)
p["juicio_objetivo"]["criterio"]["descripcion"] = ""
m = k.coh(x) or ""
paso("S11", "vidrala_bloqueo N1.tipo: un criterio propio sin descripción: rechazo", "descripcion" in m, m)
x_s11 = copy.deepcopy(x)
k.par(x_s11, "N1.tipo")["juicio_objetivo"]["criterio"]["descripcion"] = "mi criterio de 1,5 € (juicio mío, no un umbral adoptado)"

# ---------- V · contrato ----------
k = casos["viscofan"]


def variante_rechazada(etiqueta, cambio, texto):
    y = copy.deepcopy(pos["viscofan"])
    cambio(y)
    y["configuracion_v64"]["objetivo"]["hipotesis_que_condicionan"] = OBJ.condicionantes(y, k.conf)
    m = k.coh(y) or ""
    paso("V", f"viscofan: {etiqueta}: rechazo", texto in m, m)


def con_contraste(y, kk):
    return k.par(y, kk)["juicio_objetivo"]


kk = next(p["clave"] for p in k.fc["configuracion_v64"]["parametros"] if OBJ.contraste_objetivo(k.var, OBJ.cobertura(k.var, p["clave"], k.conf), k.psi))
variante_rechazada("Δ € declarado distinto del calculado (variantes recalculadas después del turno 1; A9)",
                   lambda y: con_contraste(y, kk)["contraste"][0].update(delta_eur=(con_contraste(y, kk)["contraste"][0]["delta_eur"] or 0) + 0.5), "no es el calculado")
variante_rechazada("una variante del contraste omitida", lambda y: con_contraste(y, kk)["contraste"].pop(), "exactamente las variantes calculadas")
variante_rechazada("«atribuible» cambiado por el agente", lambda y: con_contraste(y, kk)["contraste"][0].update(atribuible=not con_contraste(y, kk)["contraste"][0]["atribuible"]), "atribuible")
variante_rechazada("cobertura distinta de la mecánica", lambda y: con_contraste(y, kk).update(cobertura="sin_cobertura"), "no es la mecánica")
variante_rechazada("límites vacíos", lambda y: con_contraste(y, kk).update(limites=[]), "limites")
variante_rechazada("política inventada como criterio (A10)", lambda y: con_contraste(y, kk).update(criterio={"origen": "politica_adoptada", "descripcion": "x", "referencia": "D413-FUNDAMENTO"}),
                   "no está registrada")
variante_rechazada("bloque ausente con el contrato 4.14", lambda y: k.par(y, kk).pop("juicio_objetivo"), "obligatorio con el contrato")
variante_rechazada("campos 4.13 que no coinciden con el bloque", lambda y: k.par(y, kk).update(base_de_la_materialidad_objetivo="juicio_economico")
                   if con_contraste(y, kk)["base"] != "juicio_economico" else k.par(y, kk).update(base_de_la_materialidad_objetivo="calculada"), "tienen que coincidir")
sin_atrib = next((p["clave"] for p in k.fc["configuracion_v64"]["parametros"]
                  if not [c for c in OBJ.contraste_objetivo(k.var, OBJ.cobertura(k.var, p["clave"], k.conf), k.psi) if c["atribuible"]]), None)
if sin_atrib:
    variante_rechazada(f"«calculada» sin contraste atribuible ({sin_atrib}; hipótesis sin respaldo, A8)",
                       lambda y: (con_contraste(y, sin_atrib).update(base="calculada", material=False),
                                  k.par(y, sin_atrib).update(base_de_la_materialidad_objetivo="calculada", material_para_objetivo=False)), "exige un contraste aislado")

# ---------- D10 ----------
y = copy.deepcopy(pos["viscofan"])
celda_n3 = "Configuración V6.4!B21"
y.setdefault("fundamento_material", {}).setdefault("hipotesis_sin_fundamento", []).append({"celda": "PM1.cartera", "por_que": "(prueba) D10 de un parámetro juzgado no material"})
paso("D10", "una entrada D10 sigue condicionando el objetivo aunque su parámetro se juzgue «no material» (A12)", "PM1.cartera" in OBJ.condicionantes(y, k.conf), OBJ.condicionantes(y, k.conf))

# ---------- E · presentación ----------
k = casos["vidrala_bloqueo"]
fcp = os.path.join(k.c, "fase_c.json")
json.dump(x_s11, open(fcp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
pr = json.load(open(os.path.join(k.c, "precio.json"), encoding="utf-8"))
bl = OBJ.bloque_ficha(k.c, x_s11, pr, "pendiente_de_datos", {"accion": None, "precio_objetivo": None})
jo = ((bl or {}).get("cobertura") or {}).get("juicios_objetivo") or []
paso("E", "ficha (bloque objetivo): los juicios sobre el objetivo, con contraste, base y criterio, van aparte del juicio sobre la acción",
     len(jo) == len(x_s11["configuracion_v64"]["parametros"]) and any((j.get("criterio") or {}).get("origen") == "juicio_propio_del_agente" for j in jo), [j.get("clave") for j in jo])

import subprocess  # noqa: E402
env = dict(os.environ, MUNGER_CONFIG=CFG["vidrala_bloqueo"])
r1 = subprocess.run([sys.executable, "-B", os.path.join(PV, "scripts", "ficha.py"), k.c, "--provisional"], capture_output=True, text=True, env=env)
r2 = subprocess.run([sys.executable, "-B", os.path.join(PV, "scripts", "informe.py"), k.c, "--provisional"], capture_output=True, text=True, env=env)
inf = open(os.path.join(k.c, "informe_provisional.md"), encoding="utf-8").read() if os.path.exists(os.path.join(k.c, "informe_provisional.md")) else ""
paso("E", "informe §14 (provisional, sobre la copia): juicio sobre el objetivo de cada parámetro y el criterio propio del agente como «no adoptado»",
     r1.returncode == 0 and r2.returncode == 0 and "Juicio sobre el objetivo de N1.tipo (contrato 4.14)" in inf and "criterio propio del agente, no adoptado" in inf,
     f"ficha {r1.returncode} · informe {r2.returncode} · {(r1.stdout + r1.stderr + r2.stdout + r2.stderr).strip()[-200:]}")

n_ok = sum(r["resultado"] == "PASA" for r in RES)
print(f"{n_ok}/{len(RES)} pruebas del juicio sobre el objetivo (4.14) PASAN")
print("RESULTADO juicio sobre el objetivo: " + ("PASA" if n_ok == len(RES) else "FALLA"))
if ARGS.json:
    json.dump(RES, open(ARGS.json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
shutil.rmtree(TMP, ignore_errors=True)
sys.exit(0 if n_ok == len(RES) else 1)
