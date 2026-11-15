"""Arnés común de las sondas de la revisión del hito 2 (Fable). Importa los módulos de la COPIA propia del árbol congelado.
PV (variable de entorno) permite apuntar a otra copia (p. ej. una con el código del hito 1)."""
import os, sys
F = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PV = os.environ.get("PV") or os.path.join(F, "copia", "munger_v2_r1", "personaje_v2")
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(PV, "scripts"))
os.environ["PATH"] = os.path.join(F, "bin") + os.pathsep + os.environ.get("PATH", "")  # soffice sustituto: nunca LibreOffice
os.environ.setdefault("TMPDIR", os.path.join(F, "tmp"))
import verificacion_entradas as VE  # noqa: E402
__all__ = ["VE", "PV", "F"]
