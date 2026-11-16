"""Arnés de las sondas NUEVAS de la quinta comprobación (Fable, hito 2 de la 4.15). VE = 876bfc2 (copia ligera del árbol congelado);
VP = 7a6583b (candidata de la cuarta comprobación, con «git archive»); V92 = 92b2362 (estable de la segunda pasada); VF3 = f3d15e8;
VPR = 7a6583b con las tres propuestas del revisor de la cuarta comprobación (no es código entregado). Nunca LibreOffice."""
import importlib.util, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
F = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(F, "sondas3"))
sys.path.insert(0, os.path.join(F, "sondas"))
from comun3 import VE, VP, ACT, ANT, PV, CONGELADO  # noqa: E402,F401


def cargar(p, nombre):
    spec = importlib.util.spec_from_file_location(nombre, p)
    m = importlib.util.module_from_spec(spec)
    ruta = list(sys.path)
    spec.loader.exec_module(m)
    sys.path[:] = ruta
    return m


V92 = cargar(os.path.join(F, "estable92", "scripts", "verificacion_entradas.py"), "verificacion_entradas_92b2362")
VF3 = cargar(os.path.join(F, "f3d", "scripts", "verificacion_entradas.py"), "verificacion_entradas_f3d15e8")
VPR = cargar(os.path.join(F, "prop4", "scripts", "verificacion_entradas.py"), "verificacion_entradas_propuesta4")
assert "tipo_cambio" not in open(V92.__file__, encoding="utf-8").read()
assert "_moneda_de" in open(VE.__file__, encoding="utf-8").read() and "_moneda_de" not in open(VP.__file__, encoding="utf-8").read()
assert "propuesta del revisor, Q1" in open(VPR.__file__, encoding="utf-8").read()
