"""Arnés de las sondas de la SEGUNDA pasada (Fable). Importa los módulos de la copia propia del árbol congelado (estable) o, con
PV=<otra>/personaje_v2, de otra copia (p. ej. fable/cand: la candidata de la primera pasada, reconstruida aplicando el diff en inverso)."""
import os, sys
F = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PV = os.environ.get("PV") or os.path.join(F, "copia", "munger_v2_r1", "personaje_v2")
sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
sys.path.insert(0, os.path.join(PV, "scripts"))
os.environ["PATH"] = os.path.join(F, "bin") + os.pathsep + os.environ.get("PATH", "")  # soffice sustituto: nunca LibreOffice
os.environ.setdefault("TMPDIR", os.path.join(F, "tmp"))
import tempfile
tempfile.tempdir = os.environ["TMPDIR"]
import verificacion_entradas as VE  # noqa: E402
_rp = os.path.realpath(PV)
ETIQUETA = "estable" if os.path.realpath(os.path.join(F, "copia")) in _rp else ("candidata (1.ª pasada)" if os.path.realpath(os.path.join(F, "cand")) in _rp else PV)
__all__ = ["VE", "PV", "F", "ETIQUETA"]
