"""Sondas varias: entrada no reproducible con material:false o sin fase1_v63.json, evidencia de la configuración V6.4, robustez de comprobar, I9 sin libro."""
import copy, hashlib, json, os, shutil, sys, tempfile
import fx
from fx import VE, EE, LibroV63, con, ent, con_k, resumen, K, REG, c, PV

def caso(nombre, r, k=None):
    print(f"[{nombre}] {resumen(r, k)}")

print("=== C48 · entrada no reproducible con el registro pendiente y material:false")
cE = os.path.join(fx.TMP, "efectiva", "Viscofan"); shutil.copytree(c, cE)
shutil.copy2(os.path.join(fx.E413, "viscofan", "Viscofan", "fase1_v63.json"), os.path.join(cE, "fase1_v63.json"))
nr = VE.entradas_no_reproducibles(cE, VE.universo(cE)); print("no reproducibles con la declaración original:", nr)
r = con(carpeta=cE); caso("registro comprobado", r); print("   entradas_no_reproducibles:", len(r["entradas_no_reproducibles"]))
def no_material(g):
    for k in nr:
        ent(g, k).update(material=False); ent(g, k)["comprobacion"].update(resultado="pendiente")
r = con(no_material, carpeta=cE); caso("las mismas entradas con material:false y la comprobación pendiente (sin revisor)", r); print("   entradas_no_reproducibles:", len(r["entradas_no_reproducibles"]), "| discrepancias:", r["discrepancias"][:1])
os.remove(os.path.join(cE, "fase1_v63.json")); r = con(carpeta=cE); caso("sin fase1_v63.json en la carpeta", r); print("   entradas_no_reproducibles:", r["entradas_no_reproducibles"])
open(os.path.join(cE, "fase1_v63.json"), "w").write("[]")
try:
    r = con(carpeta=cE); caso("fase1_v63.json = [] (JSON válido, no un objeto)", r)
except Exception as ex:
    print("[fase1_v63.json = [] (JSON válido, no un objeto)] comprobar LANZA", type(ex).__name__, str(ex)[:80])
os.remove(os.path.join(cE, "fase1_v63.json"))

print("\n=== I13 · evidencia del libro de las celdas de «Configuración V6.4» (trazabilidad) fuera del vínculo")
import configuracion_economica as CE
cv = os.path.join(fx.TMP, "config", "Viscofan"); shutil.copytree(c, cv)
lb = LibroV63(VE.libro_de(cv))
meta = sorted(CE.CELDAS_METADATOS)
print("   celdas de trazabilidad (metadatos) de la configuración:", {m: str(EE._Lector(VE.libro_de(cv)).leer(CE.HOJA, m))[:60] for m in meta[:5]})
lb.escribir_celdas({f"{CE.HOJA}!B12": "(prueba) OTRA fuente del tipo impositivo, escrita después de la revisión", f"{CE.HOJA}!B13": "(prueba) otro período"})
lb.guardar(VE.libro_de(cv))
r = con(carpeta=cv); caso("fuente y período del tipo impositivo de la configuración (B12, B13) cambiados en el libro, sin nueva revisión", r, f"{CE.HOJA}!B11")

print("\n=== Robustez de comprobar («nunca lanza»)")
def intento(nombre, cambio):
    try:
        r = con(cambio); print(f"[{nombre}] no lanza · {resumen(r)}")
    except RecursionError as ex:
        print(f"[{nombre}] LANZA RecursionError")
    except Exception as ex:
        print(f"[{nombre}] LANZA {type(ex).__name__}: {str(ex)[:90]}")
k_hip = next(e["celda"] for e in REG["entradas"] if e["clase"] == "hipotesis")
intento("hipótesis con «fuente» de texto", lambda g: ent(g, k_hip).update(fuente="texto libre"))
intento("clase que es una lista", lambda g: ent(g, K).update(clase=["dato_publicado"]))
k2 = next(e["celda"] for e in REG["entradas"] if e["clase"] == "dato_publicado" and e["celda"] != K and e["celda"].startswith("Historia!"))
def ciclo(g):
    for a, b in ((K, k2), (k2, K)):
        e = ent(g, a); e.pop("fuente", None); e.update(clase="derivado", derivacion={"origenes": [b], "formula": f'o["{b}"]', "conciliacion": "x"})
intento("dos derivados que se citan entre sí (ciclo)", ciclo)
intento("página que es una lista", lambda g: ent(g, K)["fuente"].update(pagina=[22]))
intento("sha256_texto numérico con archivo PDF", lambda g: ent(g, K)["fuente"].update(archivo="fuentes_sinteticas/fuente.txt", sha256_texto=5))
intento("lectura_externa que no es objeto", lambda g: ent(g, K)["fuente"].update(conservacion="externa", lectura_externa="x"))
intento("vinculo que es texto", lambda g: ent(g, K)["comprobacion"].update(vinculo="x"))
intento("valor_fuente NaN", lambda g: ent(g, K)["fuente"].update(valor_fuente=float("nan")))
print("\n=== I9 · sin libro")
vacia = tempfile.mkdtemp(prefix="rev_fable_vacia_")
print("aptitud en una carpeta sin libro:", {k: v for k, v in VE.aptitud(vacia)[1].items() if k in ("universo", "comprobadas", "comprobadas_universo", "universo_calculo", "comprobadas_calculo", "motivo")})
shutil.rmtree(vacia, ignore_errors=True)
fx.limpiar()
