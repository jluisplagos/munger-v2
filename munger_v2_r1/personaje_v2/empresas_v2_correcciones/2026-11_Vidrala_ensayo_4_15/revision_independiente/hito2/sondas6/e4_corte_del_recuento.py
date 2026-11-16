#!/usr/bin/env python3
"""e4 · sexta comprobación · V5: el corte del recuento de apariciones (_apariciones_en_pagina deja de recoger al pasar del máximo).
A) ¿cambia algún ESTADO? Para N apariciones (N alrededor del máximo y muy por encima), con mezclas (todas iguales, una negativa al
   principio, en medio o al final, la última sin la cifra…), se compara 876bfc2 con 8196522: estado y mensaje;
B) cuántas apariciones devuelve _apariciones_en_pagina (≤ máximo + 1) y qué dice el mensaje del pendiente;
C) el orden de las comprobaciones: fragmentos sueltos (dentro de un número o de una palabra) por encima del máximo;
D) coste: la entrada de la prueba nueva «(V5)» (100.000 apariciones en una línea) con y sin el corte, varias veces; y con 400.000;
E) otras vías de coste de _cita_cifra que el corte no toca (fragmentos sueltos, una línea enorme sin saltos).
Uso: python3 -I -B e4_corte_del_recuento.py"""
import os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun6 import VE, VP, ACT, ANT  # noqa: E402
MAX = VE.MAX_APARICIONES_CITA
print(f"VE = {ACT} · VP = {ANT} · MAX_APARICIONES_CITA = {MAX} (876bfc2: {VP.MAX_APARICIONES_CITA})")

print("\n== A · estados con N apariciones (876bfc2 → 8196522)")
dif_estado, dif_mensaje, n_casos = [], [], 0
for N in list(range(0, 8)) + list(range(MAX - 3, MAX + 6)) + [2 * MAX, 2 * MAX + 1, 1000, 5000]:
    for nombre, hacer in (("todas iguales (+)", lambda N: ["Total: 5.5"] * N),
                          ("la primera negativa", lambda N: ["Total: -5.5"] + ["Total: 5.5"] * (N - 1) if N else []),
                          ("la del medio negativa", lambda N: ["Total: 5.5"] * (N // 2) + ["Total: -5.5"] + ["Total: 5.5"] * (N - N // 2 - 1) if N else []),
                          ("la última negativa", lambda N: ["Total: 5.5"] * (N - 1) + ["Total: -5.5"] if N else []),
                          ("todas negativas", lambda N: ["Total: -5.5"] * N),
                          ("la última con otra cifra detrás", lambda N: ["Total: 5.5"] * (N - 1) + ["Total: 5.57"] if N else []),
                          ("una por línea", None)):
        for sep in (" ", "\n"):
            if hacer is None:
                pag = "\n".join(["Total: 5.5"] * N)
                if sep == " ":
                    continue
            else:
                pag = sep.join(hacer(N))
            for cita, vf in (("Total: 5.5", 5.5), ("Total: -5.5", -5.5), ("5.5", 5.5), ("Total:", 5.5)):
                a, b = VP._cita_cifra(cita, vf, pag), VE._cita_cifra(cita, vf, pag)
                n_casos += 1
                if a[0] != b[0]:
                    dif_estado.append((N, nombre, sep, cita, a, b))
                elif a[1] != b[1]:
                    dif_mensaje.append((N, nombre, cita, a[1], b[1]))
print(f"   {n_casos} casos · con ESTADO distinto: {len(dif_estado)} {dif_estado[:3]}")
print(f"   con el mismo estado y MENSAJE distinto: {len(dif_mensaje)}; N de esos casos: {sorted({x[0] for x in dif_mensaje})}")
for x in dif_mensaje[:3]:
    print(f"      N={x[0]} ({x[1]}; cita {x[2]!r}): 876bfc2 «{x[3][:60]}…» · 8196522 «{x[4][:60]}…»")

print("\n== B · apariciones devueltas y mensaje")
for N in (MAX - 1, MAX, MAX + 1, MAX + 2, 1000, 100000):
    pag = " ".join(["Total: 5.5"] * N)
    na, nb = len(VP._apariciones_en_pagina("Total: 5.5", pag)), len(VE._apariciones_en_pagina("Total: 5.5", pag))
    r = VE._cita_cifra("Total: 5.5", 5.5, pag)
    print(f"   N={N:6}: _apariciones_en_pagina devuelve {na:6} (876bfc2) y {nb:4} (8196522) · estado {r[0]:20} · mensaje: {r[1][:70]}")

print("\n== C · fragmentos sueltos por encima del máximo (la cita no es un fragmento completo)")
for nombre, pag, cita, vf in (("300 cortes dentro de un número («15.5» citada «5.5»)", " ".join(["Total: 15.5"] * 300), "5.5", 5.5),
                              ("300 cortes dentro de una palabra («Subtotal» citada «total: 5.5»)", " ".join(["Subtotal: 5.5x"] * 300), "total: 5.5", 5.5),
                              ("250 completas y 100 cortes dentro de un número", " ".join(["Total: 5.5"] * 250 + ["Total: 15.5"] * 100), "5.5", 5.5),
                              ("150 completas y 100 cortes dentro de un número", " ".join(["Total: 5.5"] * 150 + ["Total: 15.5"] * 100), "5.5", 5.5)):
    a, b = VP._cita_cifra(cita, vf, pag), VE._cita_cifra(cita, vf, pag)
    print(f"   {nombre:70} 876bfc2 {a[0]:20} 8196522 {b[0]:20}" + ("" if a[0] == b[0] else "   <<< CAMBIA"))

print("\n== D · coste con y sin el corte (segundos; la máquina tiene otra carga: orientativo)")
pag = " ".join(["Total: 5.5"] * 100000)
for i in range(3):
    t0 = time.time(); ra = VP._cita_cifra("Total: 5.5", 5.5, pag); ta = time.time() - t0
    t0 = time.time(); rb = VE._cita_cifra("Total: 5.5", 5.5, pag); tb = time.time() - t0
    print(f"   la entrada de la prueba «(V5)» (100.000 apariciones, {len(pag) / 1e6:.1f} MB), vez {i + 1}: sin el corte (876bfc2) {ta:6.2f} s → {ra[0]} · con el corte (8196522) {tb:6.3f} s → {rb[0]}"
          + (f"   ← la prueba exige < 5 s: {'pasaría también SIN el corte' if ta < 5 else 'fallaría sin el corte'}" if True else ""))
for N in (200000, 400000):
    pag = " ".join(["Total: 5.5"] * N)
    t0 = time.time(); VP._cita_cifra("Total: 5.5", 5.5, pag); ta = time.time() - t0
    t0 = time.time(); VE._cita_cifra("Total: 5.5", 5.5, pag); tb = time.time() - t0
    print(f"   {N} apariciones en una línea ({len(pag) / 1e6:.1f} MB): sin el corte {ta:6.2f} s · con el corte {tb:6.3f} s")

print("\n== E · otras vías que el corte no toca")
for nombre, pag, cita, vf in (("200.000 cortes dentro de una palabra en una línea", " ".join(["Subtotal: 5.5x"] * 200000), "total: 5.5", 5.5),
                              ("200.000 cortes dentro de un número en una línea", " ".join(["Total: 15.5"] * 200000), "5.5", 5.5),
                              ("200 apariciones completas en una línea de 4 MB (el contexto se recorta a 400 caracteres)", ("x" * 20000 + " Total: 5.5 ") * 200, "Total: 5.5", 5.5),
                              ("una aparición al final de una línea de 20 MB", "y" * 20_000_000 + " Total: 5.5", "Total: 5.5", 5.5)):
    t0 = time.time(); b = VE._cita_cifra(cita, vf, pag); tb = time.time() - t0
    t0 = time.time(); a = VP._cita_cifra(cita, vf, pag); ta = time.time() - t0
    print(f"   {nombre:90} 876bfc2 {a[0]:14} {ta:6.2f} s · 8196522 {b[0]:14} {tb:6.2f} s")
