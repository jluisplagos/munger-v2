"""Arnés de las sondas de la SÉPTIMA comprobación (Fable, hito 2 de la 4.15). Carga en un mismo proceso `verificacion_entradas` de:
VE = 45ff57c (esta candidata; copia ligera del árbol congelado rev7/munger_v2_r1, que solo se lee) ·
VP = 8196522 (candidata de la sexta comprobación, sacada con «git archive») ·
VQ = 8196522 con las propuestas W3, W4 y W5 del revisor de la sexta (prop6, reconstruido con el propuestas6.py entregado; NO es código entregado) ·
V876 = 876bfc2 (candidata de la quinta).
Nunca LibreOffice (sustituto de soffice delante en el PATH)."""
import importlib.util, os, sys, tempfile
AQUI = os.path.dirname(os.path.abspath(__file__))
F = os.path.dirname(AQUI)
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


def cargar(p, nombre):
    """Otro `verificacion_entradas` con otro nombre de módulo; sus importaciones internas se resuelven con los scripts de la candidata
    (entre 8196522 y 45ff57c solo cambia verificacion_entradas.py)."""
    spec = importlib.util.spec_from_file_location(nombre, p)
    m = importlib.util.module_from_spec(spec)
    ruta = list(sys.path)
    spec.loader.exec_module(m)
    sys.path[:] = ruta
    return m


VP = cargar(os.path.join(PVP, "scripts", "verificacion_entradas.py"), "verificacion_entradas_8196522")
VQ = cargar(os.path.join(F, "prop6", "munger_v2_r1", "personaje_v2", "scripts", "verificacion_entradas.py"), "verificacion_entradas_prop6")
V876 = cargar(os.path.join(F, "c876", "scripts", "verificacion_entradas.py"), "verificacion_entradas_876bfc2")
_s = {m: open(m.__file__, encoding="utf-8").read() for m in (VE, VP, VQ, V876)}
assert "(hito 2, W5)" in _s[VE] and "(hito 2, W5)" not in _s[VP]            # marcador de 45ff57c frente a 8196522
assert "propuesta del revisor, W3" in _s[VQ] and "(hito 2, V2)" in _s[VP]     # prop6 y 8196522
assert "(hito 2, V2)" not in _s[V876]                                         # 876bfc2
ACT, ANT, PROP = os.environ.get("ETIQUETA_VE", "séptima (45ff57c)"), "anterior (8196522)", "propuesta de la 6.ª (prop6)"
