#!/usr/bin/env python3
"""d3 · coste de _cita_cifra con muchas apariciones de la cita (quinta comprobación), 7a6583b (sin máximo) y 876bfc2 (máximo 200).
A) la cita repetida N veces en UNA línea (el caso de la prueba nueva, que usa N = 3.000) y en N líneas;
B) dónde se va el tiempo con 876bfc2: _apariciones_en_pagina (que sigue recogiendo TODAS las apariciones antes de contarlas; en una
   sola línea busca el principio y el final de la línea para cada una) frente al resto;
C) el caso de la segunda prueba nueva (150 apariciones en una línea de más de 100 kB), con y sin el recorte del contexto a 400 caracteres
   (la mutación n10c), para ver con qué margen la detecta el límite de 10 s de la prueba.
Los tiempos dependen de la carga de la máquina (se dice la carga al empezar).  Uso: python3 -I -B d3_coste_maximo.py"""
import os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun5 import VE, VP, ACT, ANT  # noqa: E402
print(f"VE = {ACT} · VP = {ANT} · carga de la máquina (1, 5, 15 min): {os.getloadavg()}")
CITA, VF = "Total: 849697.000", 849697.0


def t(f):
    t0 = time.perf_counter()
    r = f()
    return r, time.perf_counter() - t0


print("== A · la cita repetida N veces")
for sep, nombre in ((" ", "una línea"), ("\n", "N líneas")):
    for n in ((200, 201, 3000, 20000, 100000) if sep == " " else (200, 201, 3000, 20000, 100000, 400000)):
        pag = sep.join([CITA] * n)
        (rb, tb) = t(lambda: VE._cita_cifra(CITA, VF, pag))
        if n <= 20000:
            (ra, ta) = t(lambda: VP._cita_cifra(CITA, VF, pag))
            ant = f"7a6583b: {ra[0]:20} {ta:7.2f} s"
        else:
            ant = "7a6583b: (no se mide)             "
        (_, tap) = t(lambda: VE._apariciones_en_pagina(CITA, pag))
        print(f"   {nombre:10} N={n:7} ({len(pag) // 1000:6} kB) · {ant} · 876bfc2: {rb[0]:20} {tb:7.2f} s (de ellos, _apariciones_en_pagina: {tap:6.2f} s)")

print("\n== B · una sola línea muy larga con pocas apariciones al final (coste de buscar el principio de la línea)")
for kb, n in ((1000, 150), (5000, 150), (5000, 201), (5000, 5000)):
    pag = ("x" * 9 + " ") * (kb * 100) + " ".join([CITA] * n)
    (rb, tb) = t(lambda: VE._cita_cifra(CITA, VF, pag))
    print(f"   línea de {len(pag) // 1000:6} kB con {n:5} apariciones al final · 876bfc2: {rb[0]:20} {tb:7.2f} s")

print("\n== C · la segunda prueba nueva (150 apariciones en una línea de más de 100 kB), con el recorte a 400 caracteres y sin él")
pocas = " ".join([f"Partida {i}: {i}.5" for i in range(8000)] + [f"Total: {VF:.3f}"] * 150)
(r1, t1) = t(lambda: VE._cita_cifra(f"Total: {VF:.3f}", VF, pocas))
print(f"   876bfc2 tal cual: {r1[0]} en {t1:.2f} s (línea de {len(pocas)} caracteres)")
orig = VE._apariciones_en_pagina
import re  # noqa: E402


def sin_recorte(cita, pagina):
    """_apariciones_en_pagina de 876bfc2 sin la línea del recorte (la mutación n10c), copiada del código."""
    palabras = str(cita or "").split()
    if not palabras or pagina is None:
        return []
    t_ = re.sub("[   ]", " ", str(pagina))
    patron = r"\s+".join(re.escape(w) for w in palabras)
    patron = ((r"(?<![\d.,])" if re.match(r"\d", palabras[0]) else r"(?<![^\W\d_])" if re.match(r"[^\W\d_]", palabras[0]) else "") + patron
              + (r"(?!\d|[.,]\d)" if re.search(r"\d$", palabras[-1]) else r"(?![^\W\d_])" if re.search(r"[^\W\d_]$", palabras[-1]) else ""))
    out = []
    for m in re.finditer(patron, t_, re.I):
        ini = t_.rfind("\n", 0, m.start()) + 1
        fin = t_.find("\n", m.end())
        fin = len(t_) if fin < 0 else fin
        out.append((t_[ini:fin], m.start() - ini, m.end() - ini))
    return out


assert [x[1:] for x in orig("Total 5", "a\nTotal 5 x\n")] == [x[1:] for x in sin_recorte("Total 5", "a\nTotal 5 x\n")]
VE._apariciones_en_pagina = sin_recorte
try:
    (r2, t2) = t(lambda: VE._cita_cifra(f"Total: {VF:.3f}", VF, pocas))
finally:
    VE._apariciones_en_pagina = orig
print(f"   sin el recorte (mutación n10c): {r2[0]} en {t2:.2f} s → la prueba (menos de 10 s) {'la DETECTA' if t2 >= 10 else 'NO la detecta'} en esta máquina, con un margen de {t2 / 10:.1f} veces el límite")
