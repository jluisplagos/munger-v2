#!/usr/bin/env python3
"""d6 · (quinta comprobación) las tres transiciones «discrepancia → pendiente» que introduce esta candidata, en el REGISTRO completo
(fixture de la batería) y su efecto en la aptitud. En el control, una discrepancia bloquea siempre; un pendiente no bloquea si la entrada
es de juicio, está declarada no material y un revisor independiente selló el juicio de materialidad (N1 de la segunda revisión del hito 1:
por diseño, esa entrada puede quedar sin contrastar). Se prueba cada caso con la entrada material (K, de cálculo) y con una de juicio
no material revisada (KJ).
  L · decimal sin cero delante: la página publica «.849697» (0,849697) y la cita empieza en la cifra («849697»)
  P · control: punto de fin de frase pegado («ejercicio.849697.000»): la cifra SÍ es la publicada
  I · guion pegado entre dos años DECRECIENTES («Variación 2024-<año>»): la entrada del año (Historia!F5, de cálculo) citada así
  M · más de 200 apariciones de la cita, todas en NEGATIVO, con valor_fuente positivo
PV=<prev>/personaje_v2 para la candidata anterior.  Uso: python3 -I -B d6_discrepancia_a_pendiente_registro.py"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sondas"))
import fx5 as X  # noqa: E402
VE = X.VE
print("código:", "quinta (876bfc2)" if "MAX_APARICIONES_CITA" in open(VE.__file__, encoding="utf-8").read() else "anterior (7a6583b, 4.ª comprobación)")
print("control positivo:", X.resumen(X.con())[:80])
K = X.K
KJ = next(e["celda"] for e in X.REG["entradas"] if e["ambito"] == "juicio" and e["clase"] == "dato_publicado" and isinstance(e["valor_modelo"], (int, float)))
JUST_M = "(prueba) cifra de contexto del sector que ninguna fase usa para concluir; revisado por el revisor independiente"
print(f"K = {K} (cálculo, material) · KJ = {KJ} (juicio)")
r0 = X.con(lambda g: X.ent(g, KJ).update(material=False, justificacion_materialidad=JUST_M), resellar=True)
print("control: KJ no material con el juicio de materialidad revisado y la cita buena:", X.resumen(r0)[:150])

CASOS = []
for k in (K, KJ):
    e = X.ent(X.REG, k)
    vf = e["fuente"]["valor_fuente"]
    ent_txt = f"{vf:.0f}" if float(vf).is_integer() else repr(vf)
    CASOS += [
        (k, "L decimal sin cero delante: página «… .<cifra>», cita desde la cifra", f"Partida sintética de {k}: .{ent_txt}", ent_txt, {}),
        (k, "L2 lo mismo entre paréntesis y con signo: «(-.<cifra>)»", f"Partida sintética de {k}: (-.{ent_txt})", ent_txt, {}),
        (k, "P control: punto de fin de frase pegado, la cifra es la publicada", f"al cierre del ejercicio.{ent_txt} miles", f"{ent_txt} miles", {}),
        (k, "M 201 apariciones de la cita, todas en negativo, con valor_fuente positivo", "\n".join([f"Total sintético: ({ent_txt})"] * 201), f"Total sintético: ({ent_txt})", {}),
        (k, "M0 control: 200 apariciones, todas en negativo", "\n".join([f"Total sintético: ({ent_txt})"] * 200), f"Total sintético: ({ent_txt})", {}),
    ]
KA = "Historia!F5"
anio = int(X.ent(X.REG, KA)["fuente"]["valor_fuente"])
CASOS += [(KA, f"I años decrecientes: «Variación {anio + 1}-{anio}», el año {anio}", f"Variación {anio + 1}-{anio}", f"Variación {anio + 1}-{anio}", {}),
          (KA, f"I0 control: años crecientes «Periodo {anio - 1}-{anio}»", f"Periodo {anio - 1}-{anio}", f"Periodo {anio - 1}-{anio}", {})]
for k, nombre, pagina, cita, extra in CASOS:
    n = X.nueva_pagina(pagina)
    for no_material in ((False,) if k in (K, KA) else (False, True)):
        def cambio(g, k=k, cita=cita, n=n, extra=extra, no_material=no_material):
            X.ent(g, k)["fuente"].update(cita=cita, pagina=n, **extra)
            if no_material:
                X.ent(g, k).update(material=False, justificacion_materialidad=JUST_M)
        r = X.con(cambio, resellar=True)
        cat = "comprobada" if k in r["comprobadas"] else next((c for c in ("errores", "discrepancias", "pendientes", "desactualizadas") if any(x.startswith(k + ":") for x in r[c])), "?")
        print(f"   {'K (cálculo, material)' if k == K else 'año (cálculo, material)' if k == KA else 'KJ (juicio, NO material revisada)' if no_material else 'KJ (juicio, material)':34} {nombre:74} → {cat:13} apto={r['apto_por_entradas']}"
              + (f"  · {X.con_k(r, k)[0][:140]}" if X.con_k(r, k) and cat == "errores" else ""))
print("control positivo al final:", X.resumen(X.con())[:80])
X.limpiar()
