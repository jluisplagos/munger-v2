#!/usr/bin/env python3
"""n8 · U7 (unidad monetaria no reconocida), H14 (signo −1 sin tratamiento) y U6 (modo de la entrada efectiva), segunda pasada.
A) _unidad_monetaria_no_reconocida sobre unidades plausibles: ¿cuáles pasan a «pendiente»? (las de los 7 registros reales, aparte);
B) registro sintético completo: un tipo de cambio como dato publicado («USD por EUR»), un precio por título, y el orden de H14;
C) H14: textos de tratamiento que equivalen a «ninguno» y no están en la lista;
D) U6: alcances con claves legítimas que se parecen a «entrada_efectiva», y declaraciones que siguen pasando en silencio.
Uso: python3 -I -B n8_u7_u6_h14.py"""
import json, os, sys, tempfile
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sondas"))
import fx5 as X
VE, K = X.VE, X.K
import pipeline as PL  # noqa: E402

print("== A · unidades: ¿«unidad monetaria no reconocida» (pendiente)?")
reales = ["EUR por acción", "euros por acción", "año", "año (ejercicio)", "millones de euros", "miles de euros", "texto", "acciones", "moneda", "norma"]
otras = ["mm", "m€", "€m", "k€", "eur", "euros", "MM€", "miles de €", "en miles de euros", "millones de EUR", "EUR millones", "millones de euros (reexpresado)", "M EUR", "EUR m",
         "USD por EUR", "EUR/USD", "USD/EUR", "tipo de cambio EUR/USD", "DKK por EUR", "céntimos de euro por acción", "EUR/acción", "€/acción", "€ por acción", "euros por título",
         "EUR per share", "DKK per aktie", "EUR por derecho", "EUR por ADR", "euros por bono", "EUR por tonelada", "€/MWh", "EUR por empleado", "miles de euros por empleado",
         "%", "% (en términos reales)", "tipos reales", "veces", "millones de acciones", "libras (peso)", "miles de toneladas", "francos suizos", "coronas danesas", "millones de DKK",
         "puntos básicos", "euro", "Euro", "número"]
for u in reales:
    print(f"   (real) {u!r:38} → {'PENDIENTE (U7)' if VE._unidad_monetaria_no_reconocida(u) else 'sin cambio'} · en UNIDADES: {VE._norm_txt(u) in VE.UNIDADES}")
for u in otras:
    nr = VE._unidad_monetaria_no_reconocida(u)
    print(f"          {u!r:38} → {'PENDIENTE (U7)' if nr else 'sin cambio':16} · en UNIDADES: {VE._norm_txt(u) in VE.UNIDADES}")

print("\n== B · registro sintético completo")
r0 = X.con()
print("   control positivo:", X.resumen(r0, K)[:60])
VF = X.ent(X.REG, K)["fuente"]["valor_fuente"]
VM = X.ent(X.REG, K)["valor_modelo"]


def caso(nombre, **cambio):
    r = X.con(lambda g: X.ent(g, K)["fuente"].update(cambio), resellar=True)
    print(f"   {nombre}\n      -> {'comprobada' if K in r['comprobadas'] else 'NO comprobada'} {'; '.join(x[:230] for x in X.con_k(r, K))}")


pg = X.nueva_pagina(f"Tipo de cambio de cierre: {VM:.3f} USD por EUR")
caso("B1 un tipo de cambio publicado, con su unidad «USD por EUR» y escala 1 (dato de origen de una conversión de divisa)", pagina=pg, cita=f"Tipo de cambio de cierre: {VM:.3f} USD por EUR", valor_fuente=VM, unidad="USD por EUR", escala=1.0)
caso("B2 el mismo dato con la unidad «tipo de cambio» (sin nombrar la moneda)", pagina=pg, cita=f"Tipo de cambio de cierre: {VM:.3f} USD por EUR", valor_fuente=VM, unidad="tipo de cambio", escala=1.0)
caso("B3 precio por título con la unidad «EUR por ADR»", pagina=pg, cita=f"Tipo de cambio de cierre: {VM:.3f} USD por EUR", valor_fuente=VM, unidad="EUR por ADR", escala=1.0)
pg2 = X.nueva_pagina(f"Partida sintética de {K}: {VF:.3f}")
caso("B4 H14 y su orden: signo −1 con «ninguno» y, además, la página publica la cifra en POSITIVO (se informa del tratamiento, no de la discrepancia con la página)",
     pagina=pg2, cita=f"Partida sintética de {K}: {VF:.3f}", valor_fuente=-VF, signo=-1, tratamiento="ninguno")
caso("B5 lo mismo con un tratamiento escrito: ahora sí se ve la discrepancia con la página", pagina=pg2, cita=f"Partida sintética de {K}: {VF:.3f}", valor_fuente=-VF, signo=-1,
     tratamiento="pago publicado entre paréntesis")

print("\n== C · H14: tratamientos que no explican el cambio de signo y no están en la lista (página «(849,697.000)», valor_fuente negativo, signo −1)")
pg3 = X.nueva_pagina(f"Partida sintética de {K}: ({VF:,.3f})")
for tr in ["ninguno", "Ninguno.", "ninguno (dato directo)", "none", "no aplica", "sin cambios", "n.a.", "N/A", "nada", "—", "–", ".", "x", "directo", "0", "ver nota", "pago publicado entre paréntesis"]:
    r = X.con(lambda g, tr=tr: X.ent(g, K)["fuente"].update(pagina=pg3, cita=f"Partida sintética de {K}: ({VF:,.3f})", valor_fuente=-VF, signo=-1, tratamiento=tr), resellar=True)
    print(f"   tratamiento {tr!r:36} → {'comprobada' if K in r['comprobadas'] else 'NO comprobada: ' + '; '.join(x[:90] for x in X.con_k(r, K))}")
kc = next(e["celda"] for e in X.REG["entradas"] if e["clase"] == "cero_comprobado")
r = X.con(lambda g: X.ent(g, kc)["fuente"].update(signo=-1), resellar=True)
print(f"   cero comprobado ({kc}) con signo −1 y tratamiento «ninguno» (−1 × 0 = 0: no hay cambio de signo que explicar) → "
      f"{'comprobada' if kc in r['comprobadas'] else 'NO comprobada: ' + '; '.join(x[:120] for x in X.con_k(r, kc))}")
r = X.con()
print("   control positivo al final:", X.resumen(r, K)[:60])

print("\n== D · U6: modo de la entrada efectiva con varios alcance_v2.json (sin entrada_efectiva.json)")
d = tempfile.mkdtemp(prefix="rev2_n8_")
BASE = {"tipo": "ensayo_exploratorio", "aviso": "x", "fuente": "x", "fecha": "2026-11-15"}
for nombre, extra in [("alcance real (tipo, aviso, fuente, fecha)", {}), ("+ «entrada_efectiva»: «estricta»", {"entrada_efectiva": "estricta"}),
                      ("+ «entrada_efectiva_motivo»", {"entrada_efectiva": "estricta", "entrada_efectiva_motivo": "x"}), ("+ «nota_entrada_efectiva»", {"nota_entrada_efectiva": "x"}),
                      ("+ «tasa_efectiva»", {"tasa_efectiva": 0.25}), ("+ «fecha_entrada_efectiva»", {"fecha_entrada_efectiva": "2026-01-01"}), ("+ «entrega_efectiva»", {"entrega_efectiva": "x"}),
                      ("+ «entrada_de_efectivo»", {"entrada_de_efectivo": 1}), ("+ «modo»: «estricta» (clave equivocada)", {"modo": "estricta"}),
                      ("+ «entrada_estricta»: true (clave equivocada)", {"entrada_estricta": True}), ("+ «efectiva»: «estricta»", {"efectiva": "estricta"}),
                      ("+ «modo_entrada_efectiva»: «estricta»", {"modo_entrada_efectiva": "estricta"}), ("+ «entrada_efectiva»: {«modo»: «estricta»} (objeto)", {"entrada_efectiva": {"modo": "estricta"}}),
                      ("+ «entrada_efectiva»: «estricta » (espacio final)", {"entrada_efectiva": "estricta "})]:
    json.dump(dict(BASE, **extra), open(os.path.join(d, "alcance_v2.json"), "w", encoding="utf-8"), ensure_ascii=False)
    try:
        res = PL.modo_entrada_efectiva(d)
    except ValueError as ex:
        res = f"ERROR: {str(ex)[:110]}"
    print(f"   {nombre:55} → {res}")
import shutil
shutil.rmtree(d, ignore_errors=True)
X.limpiar()
