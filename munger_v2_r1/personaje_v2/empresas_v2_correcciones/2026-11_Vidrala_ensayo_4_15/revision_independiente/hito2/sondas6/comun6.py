"""Arnés de las sondas NUEVAS de la sexta comprobación (Fable, hito 2 de la 4.15). Carga en un mismo proceso:
VE = 8196522 (esta candidata; copia ligera del árbol congelado) · VP = 876bfc2 (candidata de la quinta comprobación, con «git archive») ·
VQ = 876bfc2 con las propuestas V1, V2 y V3 del revisor de la quinta comprobación (prop5; NO es código entregado) · V7A = 7a6583b · V92 = 92b2362.
Nunca LibreOffice (sustituto de soffice en el PATH, por comun3)."""
import os, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
F = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(F, "sondas5"))
from comun5 import VE, VP, VPR as VQ, V7A, V92, VF3, ACT, ANT, PV, CONGELADO, cargar  # noqa: E402,F401
