#!/usr/bin/env python3
"""s14 · R3 («cifra completa», «un número que solo coincide al redondear no vale») con la CITA CORTADA dentro de una cifra de la página.
El control comprueba que la cifra no está dentro de otra cifra DE LA CITA, pero la cita se busca en la página como subcadena: puede
empezar o acabar a mitad de un número publicado. Registro sintético completo (arnés fx5). Con PV=<copia del hito 1> se ve si ya ocurría."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fx5 as X
VE, K = X.VE, X.K
VF = X.ent(X.REG, K)["fuente"]["valor_fuente"]
print("código:", "hito 2" if hasattr(VE, "_cita_cifra") else "hito 1", "· control positivo:", X.resumen(X.con(), K)[:60])


def caso(nombre, pagina, cita, vf=VF, k=K, clase=None):
    pg = X.nueva_pagina(pagina)

    def cambio(g):
        X.ent(g, k)["fuente"].update(pagina=pg, cita=cita, valor_fuente=vf)
    r = X.con(cambio, resellar=True)
    res = "APTA y comprobada" if (r["apto_por_entradas"] and k in r["comprobadas"]) else "no apta"
    print(f"   {nombre}\n      la página publica: {pagina!r}\n      cita: {cita!r} · valor_fuente declarado: {vf!r}\n      -> {res}  {'; '.join(x[:140] for x in X.con_k(r, k))}")


caso("1 la página publica una cifra DIEZ veces mayor; la cita se corta antes del último dígito", f"Partida sintética de {K}: {int(VF)}0", f"Partida sintética de {K}: {int(VF)}")
caso("2 la página publica 1849697.000; la cita empieza en el segundo dígito", f"Partida sintética de {K}: 1{VF:.3f}", f"{VF:.3f}")
caso("3 la página publica 849697.499 (más precisión); la cita se corta en el punto decimal (truncar no es el valor publicado)", f"Partida sintética de {K}: {int(VF)}.499", f"Partida sintética de {K}: {int(VF)}")
caso("4 la página publica 849.697.123 (miles con punto); la cita se corta tras el segundo grupo", f"Partida sintética de {K}: 849.697.123", f"Partida sintética de {K}: 849.697")
KZ = next(e["celda"] for e in X.REG["entradas"] if e["clase"] == "cero_comprobado")
caso(f"5 cero comprobado ({KZ}): la página publica 0.49; la cita se corta tras el 0 (contraejemplo «0,49 no es 0» de la revisión externa de la 4.14)", "Partida: 0.49", "Partida: 0", vf=0, k=KZ)
caso(f"6 cero comprobado ({KZ}): la página publica 2019; la cita es «0» (el «0» de «2019»)", "Ejercicio 2019", "0", vf=0, k=KZ)
caso("7 control: las mismas citas completas se rechazan", f"Partida sintética de {K}: {int(VF)}0", f"Partida sintética de {K}: {int(VF)}0")
print("control positivo al final:", X.resumen(X.con(), K)[:60])
X.limpiar()
