#!/usr/bin/env python3
"""n11 · H1 (segunda pasada), en el registro completo (arnés fx5): (a) citas que solo TOCAN la cifra de la página (un carácter basta);
(b) una cita legítima que además aparece como subcadena de otra línea con otra cifra («Total 1,234.5» dentro de «Subtotal 1,234.56»):
¿rechazo falso?; (c) negativo partido en dos líneas con la cita en la segunda.
Uso: python3 -I -B n11_cita_toca_registro.py   (PV=<cand>/personaje_v2 para la candidata)"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sondas"))
import fx5 as X
VE, K = X.VE, X.K
print("código:", "estable" if hasattr(VE, "_apariciones_en_pagina") else "candidata (1.ª pasada)")
VF = X.ent(X.REG, K)["fuente"]["valor_fuente"]
print("control positivo:", X.resumen(X.con(), K)[:60])


def caso(nombre, pagina, cita, espera, vf=VF, signo=1, tratamiento="ninguno"):
    pg = X.nueva_pagina(pagina)
    r = X.con(lambda g: X.ent(g, K)["fuente"].update(pagina=pg, cita=cita, valor_fuente=vf, signo=signo, tratamiento=tratamiento), resellar=True)
    ok = K in r["comprobadas"]
    marca = "" if (ok and espera == "ok") or (not ok and espera == "rechazo") else ("   <<< COMPROBADA (el revisor esperaba un rechazo)" if ok else "   <<< rechazo falso")
    print(f"   {nombre}\n      página={pagina!r}\n      cita={cita!r} valor_fuente={vf}\n      -> {'comprobada' if ok else 'NO comprobada'} {'; '.join(x[:210] for x in X.con_k(r, K))}{marca}")


L = f"Partida sintética de {K}"
print("== (a) la cita toca la cifra, no la contiene")
caso("a1 la cita es «0»", f"{L}: {VF:.3f}", "0", "rechazo")
caso("a2 la cita es el rótulo y el primer dígito", f"{L}: {VF:.3f}", f"{L}: 8", "rechazo")
caso("a3 la cita es el final de la cifra «7.000»", f"{L}: {VF:.3f}", "7.000", "rechazo")
caso("a4 la cita lee otro número: «849» (la página publica 849697.000)", f"{L}: {VF:.3f}", f"{L}: 849", "rechazo")
caso("a5 control: la cita contiene la cifra entera", f"{L}: {VF:.3f}", f"{L}: {VF:.3f}", "ok")
print("== (b) la cita legítima aparece además como subcadena de otra línea")
caso("b1 «Total 849,697.000» y, en otra línea, «Subtotal 849,697.0001» (otra cifra)", f"Total {VF:,.3f}\nSubtotal {VF:,.3f}1", f"Total {VF:,.3f}", "ok")
caso("b2 «Total 849,697.000» y, en otra línea, «Subtotal 849,697.000» (la misma cifra)", f"Total {VF:,.3f}\nSubtotal {VF:,.3f}", f"Total {VF:,.3f}", "ok")
caso("b3 «Total 849,697.000» y, en otra línea, «Subtotal (849,697.000)»: la cita con su rótulo solo casa con la línea positiva", f"Total {VF:,.3f}\nSubtotal ({VF:,.3f})", f"Total {VF:,.3f}", "ok")
print("== (c) negativo partido en dos líneas")
caso("c1 «(» al final de una línea y «849,697.000)» en la siguiente; la cita es la segunda línea sin el paréntesis final", f"{L}: (\n{VF:,.3f})", f"{VF:,.3f}", "rechazo")
caso("c2 lo mismo con la cita de las dos líneas y valor_fuente negativo declarado", f"{L}: (\n{VF:,.3f})", f"{L}: ( {VF:,.3f})", "ok", vf=-VF, signo=-1, tratamiento="pago publicado entre paréntesis")
print("control positivo al final:", X.resumen(X.con(), K)[:60])
X.limpiar()
