#!/usr/bin/env python3
"""Propuestas del revisor para V1, V2 y V3 (quinta comprobación), aplicadas JUNTAS sobre una copia ligera del código de 876bfc2
(fable/prop5: scripts/, pruebas/ y esquema/ copiados de «copia»; el resto, enlaces). NO es código entregado ni revisado: sirve para
comprobar que lo que se propone es compatible con las baterías y con los registros reales. Nunca toca el árbol congelado.
  V1 · _moneda_de normaliza también el franco (CHF) y el real (BRL), y «corona(s)» se toma por la misma moneda que DKK, SEK o NOK;
  V2 · el año anterior y la fecha del intervalo se anclan con «\\Z» (no casan antes de un salto de línea: un guion al principio de una
       línea no es el de un intervalo);
  V3 · en_numero: un punto o una coma al principio de una «palabra» (tras un espacio, un signo, un paréntesis o una moneda) es el de un
       decimal sin cero delante («.5», «-.5», «(.5)», «$.85»): el corte cae dentro de un número (discrepancia), no de una palabra.
Uso: python3 -I -B propuestas5.py   (escribe fable/prop5 y el diff en salidas/propuestas5_V1_V2_V3.diff)"""
import os, shutil, subprocess, sys
F = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COPIA = os.path.join(F, "copia", "munger_v2_r1")
PROP = os.path.join(F, "prop5", "munger_v2_r1")
if os.path.lexists(os.path.join(F, "prop5")):
    shutil.rmtree(os.path.join(F, "prop5"))
os.makedirs(os.path.join(PROP, "personaje_v2"))
for x in os.listdir(COPIA):
    if x != "personaje_v2":
        os.symlink(os.path.realpath(os.path.join(COPIA, x)), os.path.join(PROP, x))
for x in os.listdir(os.path.join(COPIA, "personaje_v2")):
    o, n = os.path.join(COPIA, "personaje_v2", x), os.path.join(PROP, "personaje_v2", x)
    if x in ("scripts", "pruebas", "esquema"):
        shutil.copytree(o, n, ignore=shutil.ignore_patterns("__pycache__"), symlinks=True)
    else:
        os.symlink(os.path.realpath(o), n)
p = os.path.join(PROP, "personaje_v2", "scripts", "verificacion_entradas.py")
s = open(p, encoding="utf-8").read()
CAMBIOS = [
    # V1
    ("""                        ("gbp", ("£", "gbp", "libra", "libras")), ("jpy", ("¥", "jpy"))):""",
     """                        ("gbp", ("£", "gbp", "libra", "libras")), ("jpy", ("¥", "jpy")), ("chf", ("chf", "franco", "francos")), ("brl", ("brl", "reales")),
                        ("corona", ("corona", "coronas"))):  # (propuesta del revisor, V1)"""),
    ("""    tipo_cambio = (par is not None and _moneda_de(par.group("a")) != _moneda_de(par.group("b"))  # (hito 2, Q1) dos monedas DISTINTAS: «euros/EUR» no es un tipo de cambio""",
     """    _ab = {_moneda_de(par.group("a")), _moneda_de(par.group("b"))} if par is not None else set()
    # (propuesta del revisor, V1) «coronas/DKK»: el nombre y un código de corona pueden ser la misma moneda
    tipo_cambio = (par is not None and len(_ab) == 2 and not ("corona" in _ab and _ab <= {"corona", "dkk", "sek", "nok"})  # (hito 2, Q1) dos monedas DISTINTAS: «euros/EUR» no es un tipo de cambio"""),
    # V2
    (r"""        m_prev = re.search(r"(?:^|[^\w.,])(\d{4})$", previo) or re.search(r"(?:^|[^\w.,])(?:FY|AF|EJ)(\d{4})$", previo, re.I)""",
     r"""        m_prev = re.search(r"(?:^|[^\w.,])(\d{4})\Z", previo) or re.search(r"(?:^|[^\w.,])(?:FY|AF|EJ)(\d{4})\Z", previo, re.I)  # (propuesta del revisor, V2) \Z: no antes de un salto de línea"""),
    (r"""        fecha = re.search(r"(?:^|[^\w.,])\d{1,2}-\d{1,2}$", previo) is not None and re.fullmatch(r"\d{4}", tok) is not None  # «31-12-2024»""",
     r"""        fecha = re.search(r"(?:^|[^\w.,])\d{1,2}-\d{1,2}\Z", previo) is not None and re.fullmatch(r"\d{4}", tok) is not None  # «31-12-2024»"""),
    # V3
    (r"""                return ((re.match(r"\d", palabras[0]) is not None and re.search(r"(?:\d|\d[.,])$", antes2) is not None)""",
     r"""                # (propuesta del revisor, V3) también un punto o una coma al principio de una «palabra»: decimal sin cero delante («.5», «-.5», «(.5)»)
                return ((re.match(r"\d", palabras[0]) is not None and re.search(r"(?:\d|\d[.,]|(?:^|[^\w.,])[.,])\Z", antes2) is not None)"""),
]
for viejo, nuevo in CAMBIOS:
    assert s.count(viejo) == 1, viejo[:80]
    s = s.replace(viejo, nuevo)
open(p, "w", encoding="utf-8").write(s)
d = subprocess.run(["diff", "-u", os.path.join("copia", "munger_v2_r1", "personaje_v2", "scripts", "verificacion_entradas.py"),
                    os.path.join("prop5", "munger_v2_r1", "personaje_v2", "scripts", "verificacion_entradas.py")], cwd=F, capture_output=True, text=True).stdout
open(os.path.join(F, "salidas", "propuestas5_V1_V2_V3.diff"), "w", encoding="utf-8").write(d)
print(d)
print(f"{len(d.splitlines())} líneas de diff · prop5 escrito")
