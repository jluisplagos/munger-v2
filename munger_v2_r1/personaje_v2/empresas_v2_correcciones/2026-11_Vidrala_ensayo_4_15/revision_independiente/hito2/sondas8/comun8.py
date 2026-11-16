"""Arnés de las sondas de la OCTAVA comprobación (Fable, hito 2 de la 4.15). Carga en un mismo proceso:
FN = fase1_historia de 0a0020b (esta candidata; copia ligera del árbol congelado rev8/munger_v2_r1, que solo se lee) ·
FO = fase1_historia de 45ff57c (candidata de la séptima; «git archive», árbol prev/).
Nunca LibreOffice (sustituto de soffice delante en el PATH). Solo lee los árboles."""
import hashlib, importlib.util, os, sys, tempfile
AQUI = os.path.dirname(os.path.abspath(__file__))
F = os.path.dirname(AQUI)
CONGELADO = os.path.join(os.path.dirname(F), "munger_v2_r1")
PV = os.path.join(F, "copia", "munger_v2_r1", "personaje_v2")
PVP = os.path.join(F, "prev", "munger_v2_r1", "personaje_v2")
sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
os.environ["PATH"] = os.path.join(F, "bin") + os.pathsep + os.environ.get("PATH", "")
os.environ.setdefault("TMPDIR", os.path.join(F, "tmp"))
os.makedirs(os.environ["TMPDIR"], exist_ok=True)
tempfile.tempdir = os.environ["TMPDIR"]


def cargar(p, nombre, ruta_scripts):
    """Carga un módulo por ruta con otro nombre; sus importaciones internas se resuelven en ruta_scripts."""
    spec = importlib.util.spec_from_file_location(nombre, p)
    m = importlib.util.module_from_spec(spec)
    antes = list(sys.path)
    sys.path.insert(0, ruta_scripts)
    try:
        spec.loader.exec_module(m)
    finally:
        sys.path[:] = antes
    return m


def huella(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


P_FN = os.path.join(PV, "scripts", "fase1_historia.py")
P_FO = os.path.join(PVP, "scripts", "fase1_historia.py")
FN = cargar(P_FN, "fase1_historia_0a0020b", os.path.join(PV, "scripts"))
FO = cargar(P_FO, "fase1_historia_45ff57c", os.path.join(PVP, "scripts"))
assert huella(P_FN) == huella(os.path.join(CONGELADO, "personaje_v2", "scripts", "fase1_historia.py")), "la copia no es el árbol congelado"
assert huella(P_FN).startswith("6f6f0b17") and huella(P_FO).startswith("b74494db"), (huella(P_FN), huella(P_FO))
ACT, ANT = "octava (0a0020b)", "anterior (45ff57c)"
