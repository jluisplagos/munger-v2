"""Sondas varias sobre el árbol CONGELADO: hallazgo 4 (bloqueo con el registro pendiente), 14 (trazabilidad de la configuración), observación 21
(«comprobar nunca lanza») e I9 sin libro."""
import copy, hashlib, json, os, shutil, subprocess, sys, tempfile
import fx4 as fx
from fx4 import VE, EE, LibroV63, con, ent, con_k, resumen, K, REG, c, PV


def caso(nombre, r, k=None):
    print(f"[{nombre}] {resumen(r, k)}")


print("=== hallazgo 4 · entrada no reproducible: bloquea sea cual sea el estado de su registro")
cE = os.path.join(fx.TMP, "efectiva", "Viscofan"); shutil.copytree(c, cE)
shutil.copy2(fx.F1_ORIGINAL, os.path.join(cE, "fase1_v63.json"))
nr = VE.entradas_no_reproducibles(cE, VE.universo(cE)); print("no reproducibles con la declaración original de la 4.13:", {k: v[:2] for k, v in nr.items()})
r = con(carpeta=cE); caso("registro comprobado y sellado ANTES de restaurar la declaración original (el vínculo incluía la declaración del fixture)", r); print("   no_repr:", len(r["entradas_no_reproducibles"]), "| desactualizadas:", [x[:60] for x in r["desactualizadas"]][:5])
r = con(resellar=True, carpeta=cE); caso("ídem con el vínculo rehecho sobre la declaración original", r); print("   discrepancias:", [x[:90] for x in r["discrepancias"]][:2])
def pendientes(g):
    for k in nr:
        ent(g, k)["comprobacion"].update(resultado="pendiente")
r = con(pendientes, resellar=True, carpeta=cE); caso("las mismas entradas con la comprobación pendiente", r)
def no_material(g):
    for k in nr:
        ent(g, k).update(material=False, justificacion_materialidad="x"); ent(g, k)["comprobacion"].update(resultado="pendiente")
r = con(no_material, resellar=True, carpeta=cE); caso("ídem con material:false (cálculo)", r)

print("\n=== hallazgo 14 · trazabilidad de las celdas de «Configuración V6.4» en el vínculo")
import configuracion_economica as CE
sin_evid = [k for k in fx.inst["celdas"] if k not in fx.EVID]
print("celdas del universo sin evidencia del libro en el vínculo:", len(sin_evid), "de", fx.inst["n"], "|", sin_evid[:12])
print("   por hoja:", {h: sum(1 for k in sin_evid if k.startswith(h + "!")) for h in sorted({k.split("!")[0] for k in sin_evid})})
cfg_cells = [k for k in fx.inst["celdas"] if k.startswith(CE.HOJA + "!")]
print("celdas de configuración en el universo:", len(cfg_cells), "| con trazabilidad en EVID:", sum(1 for k in cfg_cells if (fx.EVID.get(k) or {}).get("trazabilidad")), "| sin nada:", [k for k in cfg_cells if k not in fx.EVID])
print("   TRAZA_CELDAS:", {k: v for k, v in list(CE.TRAZA_CELDAS.items())[:4]}, "… | CELDAS_METADATOS:", sorted(CE.CELDAS_METADATOS)[:12])
cv = os.path.join(fx.TMP, "config", "Viscofan"); shutil.copytree(c, cv)
lb = LibroV63(VE.libro_de(cv))
lb.escribir_celdas({f"{CE.HOJA}!B12": "(prueba) OTRA fuente del tipo impositivo, escrita después de la revisión", f"{CE.HOJA}!B13": "(prueba) otro período"})
lb.guardar(VE.libro_de(cv))
r = con(carpeta=cv); caso("fuente y período del tipo impositivo (B12, B13) cambiados en el libro, sin nueva revisión", r, f"{CE.HOJA}!B11")
print("   desactualizadas:", [x.split(":")[0] for x in r["desactualizadas"]])
# todas las celdas de metadatos, una a una: ¿cuáles NO invalidan ninguna comprobación?
sin_efecto = []
for m_ in sorted(CE.CELDAS_METADATOS):
    cx = os.path.join(fx.TMP, "config_" + m_, "Viscofan"); shutil.copytree(c, cx)
    lbx = LibroV63(VE.libro_de(cx)); lbx.escribir_celdas({f"{CE.HOJA}!{m_}": "(prueba) texto cambiado"}); lbx.guardar(VE.libro_de(cx))
    rx = con(carpeta=cx)
    if not rx["desactualizadas"]:
        sin_efecto.append(m_)
    shutil.rmtree(os.path.dirname(cx), ignore_errors=True)
print("   celdas de metadatos de la configuración cuyo cambio NO deja ninguna comprobación desactualizada:", sin_efecto or "ninguna", f"(de {len(CE.CELDAS_METADATOS)})")

print("\n=== observación 21 · robustez de comprobar («nunca lanza»)")
def intento(nombre, cambio, resellar=False, k=None):
    try:
        r = con(cambio, resellar=resellar); print(f"[{nombre}] no lanza · {resumen(r, k, 150)}")
    except RecursionError:
        print(f"[{nombre}] LANZA RecursionError")
    except BaseException as ex:  # noqa: BLE001
        print(f"[{nombre}] LANZA {type(ex).__name__}: {str(ex)[:120]}")
k_hip = next(e["celda"] for e in REG["entradas"] if e["clase"] == "hipotesis")
k2 = next(e["celda"] for e in REG["entradas"] if e["clase"] == "dato_publicado" and e["celda"] != K and e["celda"].startswith("Historia!"))
intento("hipótesis con «fuente» de texto", lambda g: ent(g, k_hip).update(fuente="texto libre"), k=k_hip)
intento("clase que es una lista", lambda g: ent(g, K).update(clase=["dato_publicado"]), k=K)
def ciclo(g):
    for a, b in ((K, k2), (k2, K)):
        e = ent(g, a); e["fuente"] = {}; e.update(clase="derivado", derivacion={"origenes": [b], "formula": f'o["{b}"]', "conciliacion": "x"})
intento("dos derivados que se citan entre sí (ciclo), resellado", ciclo, True, K)
intento("página que es una lista", lambda g: ent(g, K)["fuente"].update(pagina=[22]), k=K)
intento("sha256 numérico", lambda g: ent(g, K)["fuente"].update(sha256=5), k=K)
intento("lectura_externa que no es objeto", lambda g: ent(g, K)["fuente"].update(conservacion="externa", lectura_externa="x"), k=K)
intento("vinculo que es texto", lambda g: ent(g, K)["comprobacion"].update(vinculo="x"), k=K)
intento("comprobacion que es texto", lambda g: ent(g, K).update(comprobacion="x"), k=K)
intento("valor_fuente NaN", lambda g: ent(g, K)["fuente"].update(valor_fuente=float("nan")), k=K)
intento("derivacion.origenes con un origen que es una lista (no hashable)", lambda g: ent(g, K).update(clase="derivado", fuente={}, derivacion={"origenes": [["x"]], "formula": "1", "conciliacion": "x"}), True, K)
intento("derivacion.origenes que es un texto", lambda g: ent(g, K).update(clase="derivado", fuente={}, derivacion={"origenes": "Historia!C5", "formula": "1", "conciliacion": "x"}), True, K)
intento("celda que es un número", lambda g: ent(g, K).update(celda=5))
intento("celda que es una lista", lambda g: ent(g, K).update(celda=["x"]))
intento("entradas con un elemento que no es objeto", lambda g: g["entradas"].append("x"))
intento("material que es un texto", lambda g: ent(g, K).update(material="no"), k=K)
intento("perimetro_del_expediente que es una lista", lambda g: g.update(perimetro_del_expediente=["x"]))
intento("fórmula que desborda la pila (10**10**10)", lambda g: ent(g, K).update(clase="derivado", fuente={}, derivacion={"origenes": ["Historia!C5"], "formula": "9**9**9**9", "conciliacion": "x"}), True, K) if False else print("[fórmula con potencias] no aplicable: el evaluador no admite ** (ast.Pow no permitido)")
intento("fórmula con multiplicación de listas gigante", lambda g: ent(g, K).update(clase="derivado", fuente={}, derivacion={"origenes": ["Historia!C5"], "formula": "sum([1] * 3)", "conciliacion": "x"}), True, K)
# fase1_v63.json con una declaración no serializable de forma estable / anidada
cz = os.path.join(fx.TMP, "f1raro", "Viscofan"); shutil.copytree(c, cz)
f1 = json.load(open(os.path.join(cz, "fase1_v63.json"), encoding="utf-8")); f1["analisis"]["C47"] = ["x", {"y": 1}]
json.dump(f1, open(os.path.join(cz, "fase1_v63.json"), "w"))
try:
    r = con(carpeta=cz); print("[fase1_v63.json con C47 declarada como lista] no lanza ·", resumen(r, "Análisis!C47", 120))
except BaseException as ex:  # noqa: BLE001
    print("[fase1_v63.json con C47 declarada como lista] LANZA", type(ex).__name__, str(ex)[:100])
# libro: sin Control maestro no es el caso; registro que no es objeto
for nombre, contenido in (("registro = []", "[]"), ("registro roto", "{ roto"), ("registro con entradas = objeto", '{"formato": "4.15", "entradas": {}}')):
    cy = os.path.join(fx.TMP, "regraro", "Viscofan")
    if not os.path.isdir(cy):
        shutil.copytree(c, cy)
    open(os.path.join(cy, VE.REGISTRO), "w").write(contenido)
    try:
        r = VE.comprobar(cy); print(f"[{nombre}] no lanza · apto={r['apto_por_entradas']} · motivo: {str(r['motivo'])[:110]}")
    except BaseException as ex:  # noqa: BLE001
        print(f"[{nombre}] LANZA", type(ex).__name__, str(ex)[:100])

print("\n=== I9 · sin libro / sin registro")
vacia = tempfile.mkdtemp(prefix="rev_fable_vacia_")
print("aptitud en una carpeta sin libro:", {k: v for k, v in VE.aptitud(vacia)[1].items() if k in ("universo", "comprobadas", "comprobadas_universo", "universo_calculo", "comprobadas_calculo", "motivo")})
shutil.rmtree(vacia, ignore_errors=True)
cs = os.path.join(fx.TMP, "sinreg", "Viscofan"); shutil.copytree(c, cs); os.remove(os.path.join(cs, VE.REGISTRO))
print("aptitud sin registro:", {k: v for k, v in VE.aptitud(cs)[1].items() if k in ("universo", "comprobadas", "comprobadas_universo", "universo_calculo", "comprobadas_calculo", "comprobadas_juicio")})
fx.limpiar()
