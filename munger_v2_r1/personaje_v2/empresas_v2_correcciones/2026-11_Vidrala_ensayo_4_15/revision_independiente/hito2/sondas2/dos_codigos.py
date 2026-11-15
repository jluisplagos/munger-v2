"""Carga verificacion_entradas de la ESTABLE (VE) y de la CANDIDATA de la primera pasada (VC; fable/cand, reconstruida con el diff en inverso)
en el mismo proceso, para comparar una regla antes y después."""
import importlib.util, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun2 import VE, PV, F  # noqa: E402
_p = os.path.join(F, "cand", "munger_v2_r1", "personaje_v2", "scripts", "verificacion_entradas.py")
_spec = importlib.util.spec_from_file_location("verificacion_entradas_candidata", _p)
VC = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(VC)
assert VC.__file__ != VE.__file__ and hasattr(VC, "_pasaje_en_pagina") and hasattr(VE, "_apariciones_en_pagina")
