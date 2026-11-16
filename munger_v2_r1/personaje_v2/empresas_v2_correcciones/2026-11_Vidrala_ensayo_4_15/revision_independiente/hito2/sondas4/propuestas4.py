#!/usr/bin/env python3
"""propuestas4 · NO es código entregado ni revisado: aplica sobre un árbol ligero aparte (fable/prop) las tres propuestas de código del
revisor en esta comprobación, para ver que son compatibles con lo que hay (baterías permitidas y registros reales):
  Q1 · la exención del tipo de cambio de U7 exige que las dos monedas del par sean DISTINTAS;
  Q3 · el prefijo FY/AF/EJ de un intervalo de años se ancla al principio de la palabra;
  Q4 · en_numero mira solo los dos caracteres anteriores (coste acotado; un punto tras una letra no es de un número).
Uso: python3 -I -B propuestas4.py   (crea fable/prop; después se ejecutan las baterías y las sondas con PV=<fable>/prop/…/personaje_v2)"""
import os, shutil, subprocess
F = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COPIA, PROP = os.path.join(F, "copia", "munger_v2_r1"), os.path.join(F, "prop", "munger_v2_r1")
if os.path.lexists(os.path.join(F, "prop")):
    shutil.rmtree(os.path.join(F, "prop"))
os.makedirs(os.path.join(PROP, "personaje_v2"))
for x in os.listdir(COPIA):
    if x != "personaje_v2":
        os.symlink(os.path.realpath(os.path.join(COPIA, x)), os.path.join(PROP, x))
for x in os.listdir(os.path.join(COPIA, "personaje_v2")):
    o, n = os.path.join(COPIA, "personaje_v2", x), os.path.join(PROP, "personaje_v2", x)
    if x in ("scripts", "pruebas", "esquema"):
        shutil.copytree(o, n, ignore=shutil.ignore_patterns("__pycache__"))
    else:
        os.symlink(os.path.realpath(o), n)
p = os.path.join(PROP, "personaje_v2", "scripts", "verificacion_entradas.py")
s = open(p, encoding="utf-8").read()
CAMBIOS = [
    # Q1
    (r'''    tipo_cambio = (re.fullmatch(r"(?:(?:tipo de cambio|exchange rate)\b)?[\s:(]*" + m_ + r"\s*(?:por|per|/)\s*" + m_ + r"[\s)]*", t, re.I) is not None
                   and re.search(''',
     r'''    m_tc = re.fullmatch(r"(?:(?:tipo de cambio|exchange rate)\b)?[\s:(]*" + m_ + r"\s*(?:por|per|/)\s*" + m_ + r"[\s)]*", t, re.I)
    # (propuesta del revisor, Q1) dos nombres de la MISMA moneda («euros/EUR», «EUR/€») no son un tipo de cambio: son un importe
    _c = {"€": "eur", "euro": "eur", "euros": "eur", "$": "usd", "dólar": "usd", "dolar": "usd", "£": "gbp", "libra": "gbp", "libras": "gbp", "¥": "jpy",
          "franco": "chf", "francos": "chf", "real": "brl", "reales": "brl"}
    _a, _b = (_c.get(m_tc.group(1), m_tc.group(1)), _c.get(m_tc.group(2), m_tc.group(2))) if m_tc else (None, None)
    _misma = _a == _b or (bool({_a, _b} & {"corona", "coronas"}) and {_a, _b} <= {"corona", "coronas", "dkk", "sek", "nok"})
    tipo_cambio = (m_tc is not None and not _misma
                   and re.search('''),
    # Q3
    (r'''or re.search(r"(?:FY|AF|EJ)(\d{4})$", previo, re.I)''', r'''or re.search(r"(?:^|[^\w.,])(?:FY|AF|EJ)(\d{4})$", previo, re.I)'''),
    # Q4
    (r'''                return ((re.match(r"\d", palabras[0]) is not None and re.search(r"[\d.,]$", t_[:m.start()]) is not None)''',
     r'''                return ((re.match(r"\d", palabras[0]) is not None and re.search(r"\d[.,]?$", t_[max(0, m.start() - 2):m.start()]) is not None)'''),
]
for viejo, nuevo in CAMBIOS:
    assert s.count(viejo) == 1, viejo[:60]
    s = s.replace(viejo, nuevo)
open(p, "w", encoding="utf-8").write(s)
d = subprocess.run(["diff", "-u", os.path.join(COPIA, "personaje_v2", "scripts", "verificacion_entradas.py"), p], capture_output=True, text=True).stdout
d = d.replace(COPIA, "copia/munger_v2_r1").replace(PROP, "prop/munger_v2_r1")
open(os.path.join(F, "salidas", "propuestas4_Q1_Q3_Q4.diff"), "w", encoding="utf-8").write(d)
print(f"prop creado · diff de {len(d.splitlines())} líneas en salidas/propuestas4_Q1_Q3_Q4.diff")
