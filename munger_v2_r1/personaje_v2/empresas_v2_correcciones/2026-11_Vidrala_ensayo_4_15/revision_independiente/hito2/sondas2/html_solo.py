"""Carga solo la parte HTML de verificacion_entradas.py (de HTML_SIN_TEXTO_VISIBLE a _contiene_texto) de la estable y de la candidata,
ejecutando ese trozo del código fuente: sirve con intérpretes que no tienen lxml (python3.11 y 3.12 de este entorno)."""
import os, re, types, unicodedata
F = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def cargar(arbol):
    p = os.path.join(F, arbol, "munger_v2_r1", "personaje_v2", "scripts", "verificacion_entradas.py")
    src = open(p, encoding="utf-8").read()
    ns = {"re": re, "unicodedata": unicodedata, "os": os}
    exec(compile(src[src.index("HTML_SIN_TEXTO_VISIBLE = "):src.index("def _contiene_texto(")], p + "[HTML]", "exec"), ns)
    return types.SimpleNamespace(**{k: v for k, v in ns.items() if k.startswith("_") and not k.startswith("__")})


VE, VC = cargar("copia"), cargar("cand")
