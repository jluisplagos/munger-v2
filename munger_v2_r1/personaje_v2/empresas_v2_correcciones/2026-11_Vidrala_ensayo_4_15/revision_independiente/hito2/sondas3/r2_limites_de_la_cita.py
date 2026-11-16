#!/usr/bin/env python3
"""r2 · N4 y N10 (tercera pasada): la cita como «fragmento completo» y la cifra dentro de la cita. ¿Rechazos falsos con citas reales
que empiezan o acaban en puntuación, paréntesis, símbolos, cifras con signo, o justo en la cifra cuando la página lleva algo pegado
(unidad, código de moneda, llamada de nota, numeración del epígrafe)? Cada caso: página, cita, valor_fuente y lo que el revisor espera:
«ok», «rechazo» (cualquier cosa distinta de ok) o un estado concreto. Se da el estado de la candidata anterior (92b2362) y el de la tercera.
A) la cita acaba o empieza justo en la cifra y la página lleva algo pegado que NO es parte del número (la cifra se publica entera);
B) la cita empieza o acaba dentro de una PALABRA (no de un número);  C) citas que empiezan o acaban en puntuación, paréntesis o símbolos;
D) controles: citas cortadas dentro de un NÚMERO (tienen que rechazarse);  E) qué mensaje recibe el extractor en el registro.
Uso: python3 -I -B r2_limites_de_la_cita.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun3 import VE, VP, ACT, ANT

n_mal = 0
regresiones = []


def fila(nombre, pag, cita, vf, espera):
    global n_mal
    en_pag = VE._norm_txt(cita) in VE._norm_txt(pag)
    e2 = VE._cita_cifra(cita, vf, pag)
    e1 = VP._cita_cifra(cita, vf, pag)
    real = "ok" if e2[0] == "ok" else "rechazo"
    bien = (real == espera) or (e2[0] == espera)
    marca = "" if bien else ("   <<< ACEPTA lo que no debería" if real == "ok" else "   <<< rechazo falso")
    if not bien and real != "ok" and e1[0] == "ok":
        marca += " (REGRESIÓN: la anterior daba «ok»)"
        regresiones.append((nombre, cita, vf, e2[0]))
    if not en_pag:
        marca += "   (la cita no está en la página)"
    print(f"   {nombre}\n      página={pag!r} cita={cita!r} vf={vf!r}\n      anterior: {e1[0]:20} tercera: {e2[0]} ({e2[1][:95]}){marca}")
    n_mal += not bien


print(f"VE = {ACT} · VP = {ANT}")
print("\n== A · la cifra se publica ENTERA; la cita acaba o empieza justo en la cifra y la página lleva algo pegado (se espera «ok»)")
A = [("A1 unidad pegada detrás: «849.7m»", "Revenue 849.7m\n", "Revenue 849.7", 849.7),
     ("A2 lo mismo, la cita es solo la cifra", "Revenue €849.7m\n", "849.7", 849.7),
     ("A3 «1.2bn»", "Net debt £1.2bn at year end\n", "Net debt £1.2", 1.2),
     ("A4 múltiplo «12,5x»", "Deuda neta / EBITDA 12,5x\n", "Deuda neta / EBITDA 12,5", 12.5),
     ("A5 puntos porcentuales «3,5pp»", "Margen +3,5pp\n", "Margen +3,5", 3.5),
     ("A6 «M€» pegado", "EBITDA 849,7M€\n", "EBITDA 849,7", 849.7),
     ("A7 «150MW»", "Potencia instalada 150MW\n", "Potencia instalada 150", 150),
     ("A8 código de moneda pegado delante: «EUR849,7»", "Importe EUR849,7 millones\n", "849,7 millones", 849.7),
     ("A9 «CHF849.7» y la cita es la cifra", "Total CHF849.7\n", "849.7", 849.7),
     ("A10 llamada de nota en superíndice Unicode: «849,7¹»", "Ventas 849,7¹\n", "Ventas 849,7", 849.7),
     ("A11 llamada de nota con letra: «849,7a»", "Ventas 849,7a\n", "Ventas 849,7", 849.7),
     ("A12 negativo con unidad pegada: «(130.8)m»", "Lease payments (130.8)m\n", "(130.8)", -130.8),
     ("A13 negativo con unidad pegada, cita recortada a la cifra", "Lease payments -130.8m\n", "130.8", -130.8),
     ("A14 control: unidad separada por un espacio", "Revenue 849.7 m\n", "Revenue 849.7", 849.7),
     ("A15 control: «849,7%»", "Margen 849,7%\n", "Margen 849,7", 849.7),
     ("A16 control: «849,7€»", "Importe 849,7€\n", "Importe 849,7", 849.7),
     ("A17 control: llamada de nota entre paréntesis «849,7(1)»", "Ventas 849,7(1)\n", "Ventas 849,7", 849.7),
     ("A18 control: «849,7*»", "Ventas 849,7*\n", "Ventas 849,7", 849.7),
     ("A19 control: la cita incluye la unidad pegada", "Revenue 849.7m\n", "Revenue 849.7m", 849.7)]
for a in A:
    fila(*a, "ok")

print("\n== B · la cita empieza o acaba dentro de una PALABRA o tras un punto pegado; la cifra se publica entera")
B = [("B1 numeración del epígrafe pegada: «2.3.Deuda financiera neta 849,7»", "2.3.Deuda financiera neta 849,7\n", "Deuda financiera neta 849,7", 849.7, "ok"),
     ("B2 frase anterior pegada: «…ejercicio.Total 849,7»", "al cierre del ejercicio.Total 849,7\n", "Total 849,7", 849.7, "ok"),
     ("B3 letra de apartado pegada: «a)Ventas 849,7» (control: «)» no es letra)", "a)Ventas 849,7\n", "Ventas 849,7", 849.7, "ok"),
     ("B4 «FY2024 849,7» y la cita empieza en el año", "FY2024 849,7\n", "2024 849,7", 849.7, "ok"),
     ("B5 coma pegada: «neto,consolidado 849,7»", "Resultado neto,consolidado 849,7\n", "consolidado 849,7", 849.7, "ok"),
     ("B6 la cita recorta el rótulo: «Subtotal 849,7» citado como «total 849,7» (otro concepto: pendiente o rechazo, pero la cifra SÍ está)", "Subtotal 849,7\n", "total 849,7", 849.7, "rechazo"),
     ("B7 la cita acaba dentro de una palabra posterior: «849,7 millones» citado «849,7 mill»", "Ventas 849,7 millones\n", "Ventas 849,7 mill", 849.7, "rechazo")]
for b in B:
    fila(*b)

print("\n== C · citas que empiezan o acaban en puntuación, paréntesis, símbolos o cifras con signo (se espera «ok»)")
C = [("C1 «(130,8)»", "Pagos (130,8)\n", "(130,8)", -130.8),
     ("C2 «130,8)»", "Pagos (130,8)\n", "130,8)", -130.8),
     ("C3 «(130,8»", "Pagos (130,8)\n", "(130,8", -130.8),
     ("C4 «-130,8» con el menos dentro de la cita", "Resultado -130,8\n", "-130,8", -130.8),
     ("C5 «−130,8» (menos Unicode)", "Resultado −130,8\n", "−130,8", -130.8),
     ("C6 «+130,8»", "Variación +130,8\n", "+130,8", 130.8),
     ("C7 «€130,8»", "Importe €130,8\n", "€130,8", 130.8),
     ("C8 «130,8 €.» con punto final", "Importe: 130,8 €.\n", "130,8 €.", 130.8),
     ("C9 «130,8;» seguido de más texto", "Ventas 130,8; costes 90,2\n", "Ventas 130,8;", 130.8),
     ("C10 cita que acaba en la cifra y la página sigue con punto final de frase", "El importe fue de 130,8. El resto\n", "fue de 130,8", 130.8),
     ("C11 cita que acaba en la cifra y la página sigue con coma de enumeración", "Ventas 130,8, costes 90,2\n", "Ventas 130,8", 130.8),
     ("C12 cita que acaba en un entero y la página sigue con punto final", "Plantilla: 1234. Otros\n", "Plantilla: 1234", 1234),
     ("C13 «(3,2 %)»", "Variación (3,2 %)\n", "(3,2 %)", -3.2),
     ("C14 «:130,8» dos puntos pegados", "Total:130,8\n", "130,8", 130.8),
     ("C15 «=130,8»", "Total=130,8\n", "130,8", 130.8),
     ("C16 cifra entre comillas «130,8»", "el importe «130,8» citado\n", "«130,8»", 130.8),
     ("C17 cifra tras barra «2024/130,8»", "2024/130,8\n", "130,8", 130.8),
     ("C18 cero como guion, la cita es el guion", "Dividendos        -        12,5\n", "Dividendos -", 0),
     ("C19 cero como guion entre paréntesis de nota: «- (1)»", "Dividendos        - (1)\n", "Dividendos -", 0),
     ("C20 año con apóstrofo: «'24» no; control «2024:»", "Ejercicio 2024: 130,8\n", "Ejercicio 2024", 2024),
     ("C21 cita que empieza por «%»: «% 3,2»", "Variación en % 3,2\n", "% 3,2", 3.2),
     ("C22 cifra seguida de «.» y salto de línea", "Total 130,8.\nOtros\n", "Total 130,8", 130.8),
     ("C23 cifra seguida de «…»", "Total 130,8…\n", "Total 130,8", 130.8),
     ("C24 cifra precedida de puntos conductores con espacio: «....... 130,8»", "Total ............ 130,8\n", "130,8", 130.8),
     ("C25 cifra tras puntos conductores PEGADOS: «.......130,8» (ya se rechazaba: el punto pegado se toma por separador)", "Total ............130,8\n", "130,8", "rechazo"),
     ("C26 fecha con puntos «31.12.2024» para 2024 (ya se rechazaba)", "Cierre a 31.12.2024\n", "31.12.2024", "rechazo")]
for c_ in C:
    nombre, pag, cita, vf = c_[:4]
    if vf == "rechazo":
        fila(nombre, pag, cita, 130.8 if "130,8" in cita else 2024, "rechazo")
    else:
        fila(nombre, pag, cita, vf, "ok")

print("\n== D · controles: cita cortada dentro de un NÚMERO (se espera «ausente»: discrepancia)")
D = [("D1 «849,697» de «849,697.000»", "Total 849,697.000\n", "Total 849,697", 849697),
     ("D2 «697.000» de «849,697.000»", "Total 849,697.000\n", "697.000", 697),
     ("D3 «849697» de «8496970»", "Total 8496970\n", "Total 849697", 849697),
     ("D4 «0» de «0,49»", "Ratio 0,49\n", "Ratio 0", 0),
     ("D5 «5» de «15»", "Nota 15\n", "5", 5)]
for d in D:
    fila(*d, "ausente")

print(f"\n{n_mal} casos distintos de lo esperado por el revisor · {len(regresiones)} rechazos falsos NUEVOS (la candidata anterior daba «ok»)")
for r in regresiones:
    print("   ", r)

# E) el registro completo: qué categoría y qué mensaje recibe la entrada
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sondas"))
import fx5 as X  # noqa: E402  (fixture de la batería; trabaja en una carpeta temporal)
print("\n== E · en el registro completo (fixture de la batería): categoría y mensaje")
print("   control positivo:", X.resumen(X.con())[:70])
for nombre, pag, cita, vf in (("E1 unidad pegada «849697.000m», cita hasta la cifra", "Partida sintética de Historia!F6: 849697.000m", "Partida sintética de Historia!F6: 849697.000", None),
                              ("E2 numeración pegada «2.3.Partida…», cita desde el rótulo", "2.3.Partida sintética de Historia!F6: 849697.000", "Partida sintética de Historia!F6: 849697.000", None),
                              ("E3 control: la misma línea con un espacio tras la numeración", "2.3. Partida sintética de Historia!F6: 849697.000", "Partida sintética de Historia!F6: 849697.000", None)):
    n = X.nueva_pagina(pag)
    r = X.con(lambda g: X.ent(g, X.K)["fuente"].update(pagina=n, cita=cita), resellar=True)
    print(f"   {nombre}\n      página={pag!r}\n      cita={cita!r}\n      -> " + ("comprobada" if X.K in r["comprobadas"] else "NO comprobada " + "; ".join(X.con_k(r, X.K))[:330]))
X.limpiar()
