#!/usr/bin/env python3
"""n3 · (a) ¿Cuántas entradas reales dependen de que la cita solo TOQUE la cifra de la página (solapamiento) en vez de CONTENERLA?
Se sustituye, solo en memoria, la regla «se solapa con la ventana» de _lectura_cifra por «queda dentro de la ventana» y se repite el
inventario de signo de los 7 registros reales. (b) Lo mismo con «solo las apariciones limpias de la cita» (las que no empiezan ni acaban
dentro de una palabra o de una cifra de la página) cuando hay alguna. (c) Coste: una página de una sola línea larga con muchas apariciones de
la cita. Solo lee.  Uso: python3 -I -B n3_cita_toca_y_reales.py"""
import collections, json, os, re, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun2 import VE, PV

E14 = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_14")
EXPS = ["vidrala_decisiones_INVALIDO_perdio_analisis/Vidrala", "elis_decisiones/Elis", "viscofan/Viscofan", "elis_motor_A/Elis", "vidrala_decisiones/Vidrala",
        "vidrala/Vidrala", "viscofan_decisiones/Viscofan"]


def lectura_contenida(t, vf, ventana=None):
    """Copia de VE._lectura_cifra con una sola diferencia: la cifra (o el guion del cero) tiene que quedar DENTRO de la ventana."""
    t = re.sub(r"[\xa0  ]", " ", str(t or ""))

    def dentro(a, b):
        return ventana is None or (a >= ventana[0] and b <= ventana[1])
    if vf == 0:
        for rx in (r"(?<![\w.,])[-–—−](?![\w.,]| ?[\d(])", r"(?<=[\d)] )[-–—−](?= [\d(])"):
            if any(dentro(m.start(), m.end()) for m in re.finditer(rx, t)):
                return "ok", "cero impreso como guion"
    signos = []
    for c in VE._cifras(vf):
        for m in re.finditer(r"(?<![\d.,])" + re.escape(c) + r"(?!\d|[.,]\d)", t):
            if dentro(m.start(), m.end()):
                signos.append(VE._signo_en_cita(t, m.start(), m.end()))
    if not signos:
        return "ausente", "la cifra no aparece como cifra completa dentro de la cita"
    if vf == 0:
        return "ok", "cero"
    s = 1 if vf > 0 else -1
    if s in signos and -s not in signos:
        return "ok", ""
    if -s in signos and s not in signos and None not in signos:
        return "signo_distinto", ""
    return "signo_indeterminado", ""


def entradas():
    for exp in EXPS:
        c = os.path.join(E14, exp)
        reg, err = VE.cargar(c)
        for e in reg["entradas"]:
            f = e.get("fuente") if isinstance(e.get("fuente"), dict) else {}
            vf = f.get("valor_fuente")
            if not VE._num(vf) or e.get("clase") not in ("dato_publicado", "cero_comprobado"):
                continue
            ruta = VE._ruta_fuente(c, f.get("archivo")) if f.get("archivo") else None
            if not (ruta and str(ruta).lower().endswith(".txt")):
                continue
            est, txt = VE._pagina_examinable(ruta, f.get("pagina"))
            if est == "ok":
                yield exp, e.get("celda"), f.get("cita"), vf, txt


print("== (a) y (b) · inventario de los 7 registros reales con tres reglas")
cuenta = collections.Counter()
detalle = []
n_multi = n_sucias = 0
orig = VE._lectura_cifra
for exp, celda, cita, vf, pag in entradas():
    base = VE._cita_cifra(cita, vf, pag)[0]
    VE._lectura_cifra = lectura_contenida
    try:
        cont = VE._cita_cifra(cita, vf, pag)[0]
    finally:
        VE._lectura_cifra = orig
    apar = VE._apariciones_en_pagina(cita, pag)
    limpias = []
    for linea, a, b in apar:
        antes, desp = linea[:a], linea[b:]
        sucia_ini = bool(re.search(r"[\w.,]$", antes)) and bool(re.match(r"[\w]", linea[a:a + 1]))
        sucia_fin = bool(re.match(r"\d|[.,]\d|\w", desp)) and bool(re.search(r"\w$", linea[a:b]))
        if not (sucia_ini or sucia_fin):
            limpias.append((linea, a, b))
    n_multi += len(apar) > 1
    n_sucias += len(limpias) < len(apar)
    cuenta[("estable", base)] += 1
    cuenta[("cifra dentro de la cita", cont)] += 1
    if base != cont:
        detalle.append((exp, celda, vf, cita, base, cont))
for k in sorted(cuenta):
    print(f"   {k[0]:28} {k[1]:20} {cuenta[k]}")
print(f"   entradas con la cita más de una vez en la página: {n_multi} · con alguna aparición «sucia» (dentro de una palabra o cifra): {n_sucias}")
print(f"   entradas cuyo estado cambia si se exige que la cifra quede DENTRO de la cita: {len(detalle)}")
for d in detalle[:10]:
    print("      ", d)

print("\n== (c) · coste con una página de una sola línea larga")
for n_rep, cita, vf in [(2000, "2024", 2024), (5000, "0", 0), (2000, "-", 0)]:
    pag = " ".join(f"Partida {i} {cita} 1{i % 97}.5" for i in range(n_rep))
    t0 = time.time()
    r = VE._cita_cifra(cita, vf, pag)
    print(f"   línea única de {len(pag) // 1000} kB con {n_rep} apariciones de la cita {cita!r}: {r[0]} en {time.time() - t0:.1f} s")
pag = "\n".join(f"Partida {i}        -        1{i % 97}.5        2024" for i in range(400))
t0 = time.time()
r = VE._cita_cifra("-", 0, pag)
print(f"   página normal de 400 líneas con 400 guiones (cita «-»): {r[0]} en {time.time() - t0:.2f} s")
