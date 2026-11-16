"""Arnés de las sondas de la TERCERA pasada (Fable, hito 2 de la 4.15). «copia» = candidata f3d15e8 (árbol ligero: scripts, pruebas y
esquema copiados del árbol congelado; el resto, enlaces simbólicos al árbol congelado, que solo se lee); «prev» = candidata estable de la
segunda pasada (92b2362; scripts, pruebas y esquema sacados de git con «git archive»). Nunca LibreOffice (sustituto de soffice en el PATH).
VE = verificacion_entradas de la tercera candidata; VP = el de la anterior (cargado aparte en el mismo proceso)."""
import importlib.util, os, sys, tempfile
F = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PV = os.environ.get("PV") or os.path.join(F, "copia", "munger_v2_r1", "personaje_v2")
PVP = os.path.join(F, "prev", "munger_v2_r1", "personaje_v2")
CONGELADO = os.path.join(os.path.dirname(F), "munger_v2_r1")
sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
sys.path.insert(0, os.path.join(PV, "scripts"))
os.environ["PATH"] = os.path.join(F, "bin") + os.pathsep + os.environ.get("PATH", "")
os.environ.setdefault("TMPDIR", os.path.join(F, "tmp"))
tempfile.tempdir = os.environ["TMPDIR"]
import verificacion_entradas as VE  # noqa: E402


def cargar_prev(nombre="verificacion_entradas"):
    """Módulo `nombre` de la candidata anterior (92b2362), con otro nombre de módulo; sus importaciones internas (entradas_economicas…)
    se resuelven con los scripts de la tercera candidata, que no cambiaron (solo cambian verificacion_entradas, ficha y pipeline)."""
    p = os.path.join(PVP, "scripts", nombre + ".py")
    spec = importlib.util.spec_from_file_location(nombre + "_anterior", p)
    m = importlib.util.module_from_spec(spec)
    ruta = list(sys.path)
    spec.loader.exec_module(m)
    sys.path[:] = ruta  # el módulo anterior añade su carpeta a sys.path: se quita, para que lo demás se importe de la tercera candidata
    return m


VP = cargar_prev()
assert "textos_fuente" in open(VE.__file__, encoding="utf-8").read() and "textos_fuente" not in open(VP.__file__, encoding="utf-8").read()
ACT, ANT = os.environ.get("ETIQUETA_VE", "tercera (f3d15e8)"), "anterior (92b2362)"  # ETIQUETA_VE: para ejecutar con PV=<fable>/prop (propuestas del revisor)
