"""Arnés del revisor (Fable) para la revisión del HITO 2 de la 4.15. Es el fixture de test_verificacion_entradas_415.py (copia de Viscofan
4.13 con un registro SINTÉTICO completo y positivo, vínculos escritos por el arnés), tomado del arnés fx4.py de la cuarta pasada.
Trabaja en una carpeta temporal (TMPDIR) y lee el código de PV: por defecto la COPIA propia del árbol congelado (fable/copia/…);
con PV=<otra copia>/personaje_v2 se compara con otro código (p. ej. el del hito 1). Nunca escribe en PV ni lanza LibreOffice."""
import copy, hashlib, json, os, re, shutil, sys, tempfile
_F = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PV = os.environ.get("PV") or os.path.join(_F, "copia", "munger_v2_r1", "personaje_v2")
os.environ["PATH"] = os.path.join(_F, "bin") + os.pathsep + os.environ.get("PATH", "")  # soffice sustituto: nunca LibreOffice
os.environ.setdefault("TMPDIR", os.path.join(_F, "tmp"))
tempfile.tempdir = os.environ["TMPDIR"]
sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
sys.path.insert(0, os.path.join(PV, "scripts"))
import verificacion_entradas as VE  # noqa: E402
import entradas_economicas as EE  # noqa: E402
from v63_xml import LibroV63  # noqa: E402

E413 = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_13")
TMP = tempfile.mkdtemp(prefix="rev_fable_fx5_")  # respeta TMPDIR
IGN = shutil.ignore_patterns(".lo_perfil", "variantes_v64", "recalc", "prompts_generados", "__pycache__")
c = os.path.join(TMP, "viscofan", "Viscofan")
shutil.copytree(os.path.join(E413, "viscofan", "Viscofan"), c, ignore=IGN)
F1_ORIGINAL = os.path.join(E413, "viscofan", "Viscofan", "fase1_v63.json")
_f1p = os.path.join(c, "fase1_v63.json")
_f1 = json.load(open(_f1p, encoding="utf-8"))
for _k, (_vl, _vf, _m) in VE.entradas_no_reproducibles(c, VE.universo(c)).items():
    _d = _f1.setdefault("analisis", {}).get(_k.split("!")[1])
    _f1["analisis"][_k.split("!")[1]] = dict(_d, valor=_vl) if isinstance(_d, dict) else {"valor": _vl, "fuente": "(fixture sintético) valor efectivo del libro"}
json.dump(_f1, open(_f1p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
inst = VE.universo(c)
anios = [inst["celdas"].get(f"Historia!{x}5") for x in "CDEFGHIJKL"]
FS = os.path.join(c, "fuentes_sinteticas")
os.makedirs(FS)
paginas = []


def escribir_fuente():
    open(os.path.join(FS, "fuente.txt"), "w", encoding="utf-8").write("".join(f"[PDF PAGE {i + 1}]\n{p}\n" for i, p in enumerate(paginas)))


def fuente_para(k, v):
    n = len(paginas) + 1
    m = re.match(r"^Historia!([C-L])(\d+)$", k)
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
    return {"documento": "Fuente sintética de la prueba (no es un documento de la empresa)", "archivo": "fuentes_sinteticas/fuente.txt", "sha256": "__actual__",
            "version": "sintética 1", "pagina": str(n), "ubicacion": "tabla sintética", "concepto": f"concepto de {k}", "columna": periodo, "periodo": periodo,
            "unidad": unidad, "escala": escala, "signo": 1, "tratamiento": "ninguno", "perimetro": "consolidado", "reexpresado": "no aplica",
            "valor_fuente": vf, "cita": cita}


COMPROBADA = {"extractor": "extractor sintético", "revisor": "revisor sintético", "fecha": "2026-11-15", "resultado": "verificado",
              "fuente_examinada": "fuentes_sinteticas/fuente.txt (página citada)", "nota": None}
ents = []
for k, v in inst["celdas"].items():
    t = inst["tipos"].get(k)
    e = {"celda": k, "id": inst["ids"].get(k), "ambito": inst["ambito"].get(k), "uso": "prueba", "material": True, "valor_modelo": v,
         "comprobacion": dict(COMPROBADA), "incidencia": None}
    if t in ("hipótesis", "configuracion"):
        e.update(clase="hipotesis" if t == "hipótesis" else "convencion", hipotesis={"fundamento": "(prueba)", "alternativas": ["(prueba)"], "limites": ["(prueba)"]})
    elif v is None or v == "":
        e.update(clase="no_aplicable", justificacion="(prueba) celda vacía del libro: no aplica a este expediente")
    elif isinstance(v, (int, float)) and v == 0:
        e.update(clase="cero_comprobado", fuente=fuente_para(k, v))
    else:
        e.update(clase="dato_publicado", fuente=fuente_para(k, v))
    ents.append(e)
escribir_fuente()
EVID = VE.evidencia_libro(c)
REG = {"formato": VE.FORMATO, "empresa": "Viscofan", "nota": "REGISTRO SINTÉTICO DE PRUEBA (no verifica ningún dato real)", "perimetro_del_expediente": "consolidado",
       "huella_entradas_economicas": inst["huella"], "entradas": ents}


def sellar_todo(reg, carpeta=None):
    """Vínculo ESCRITO A MANO por el arnés (como en las baterías): huella vigente de huellas_registro, revisor y fecha de la comprobación."""
    carpeta = carpeta or c
    sha = hashlib.sha256(open(os.path.join(carpeta, "fuentes_sinteticas", "fuente.txt"), "rb").read()).hexdigest()
    for e in reg["entradas"]:
        f = e.get("fuente") or {}
        if isinstance(f, dict) and f.get("archivo") == "fuentes_sinteticas/fuente.txt" and f.get("sha256") == "__actual__":
            f["sha256"] = sha
    hs = VE.huellas_registro(carpeta, reg)
    for e in reg["entradas"]:
        cmp_ = e.setdefault("comprobacion", {})
        cmp_["vinculo"] = {"huella": hs[e["celda"]], "sellado_por": cmp_.get("revisor"), "fecha": cmp_.get("fecha")}
    return reg


def nueva_pagina(texto):
    paginas.append(texto)
    escribir_fuente()
    for e in REG["entradas"]:
        if (e.get("fuente") or {}).get("archivo") == "fuentes_sinteticas/fuente.txt":
            e["fuente"]["sha256"] = "__actual__"
    sellar_todo(REG)
    return str(len(paginas))


sellar_todo(REG)


def escribir(reg, carpeta=None):
    json.dump(reg, open(os.path.join(carpeta or c, VE.REGISTRO), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)


def con(cambio=None, resellar=False, carpeta=None):
    carpeta = carpeta or c
    reg = copy.deepcopy(REG)
    if cambio:
        cambio(reg)
    if resellar:
        sellar_todo(reg, carpeta)
    escribir(reg, carpeta)
    return VE.comprobar(carpeta)


def ent(reg, k):
    return next(e for e in reg["entradas"] if e["celda"] == k)


def con_k(r, k, cats=("errores", "discrepancias", "pendientes", "desactualizadas", "no_materiales_sin_revisar")):
    return [f"{cat}: {x}" for cat in cats for x in r.get(cat) or [] if x.startswith(k + ":")]


def resumen(r, k=None, ancho=260):
    s = (f"apto={r['apto_por_entradas']} comprobadas={r.get('comprobadas_universo')}/{r['universo']} pend={len(r['pendientes'])} desact={len(r['desactualizadas'])} "
         f"discr={len(r['discrepancias'])} err={len(r['errores'])} mat_no={len(r['materiales_no_comprobadas'])} ext={len(r.get('lecturas_externas') or [])} "
         f"no_mat={len(r.get('no_materiales') or [])} (sin_rev={len(r.get('no_materiales_sin_revisar') or [])}, rev={len(r.get('no_materiales_revisados') or [])}) "
         f"dato_hip={len(r.get('datos_como_hipotesis') or [])} no_aplic={len(r.get('no_aplicables') or [])} no_repr={len(r.get('entradas_no_reproducibles') or [])}")
    if k:
        s += " | " + "; ".join(x[:ancho] for x in con_k(r, k)) + (" | comprobada" if k in r["comprobadas"] else "")
    return s


K = "Historia!F6"


def limpiar():
    shutil.rmtree(TMP, ignore_errors=True)
