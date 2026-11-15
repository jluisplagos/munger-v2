#!/usr/bin/env python3
"""Baterías del resumen de la 4.7.1 en el árbol 4.8, separando la línea de huellas del código (entrega 4.8).

Uso (desde munger_v2_r1/): python3 -I personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_8/scripts/comparar_baterias_4_7_1.py

Por qué existe: `comprobar_entrega_4_7_1.py` da «NO COINCIDE» en su control de las tres baterías del resumen sobre el árbol 4.8,
porque la primera línea de cada salida conservada lleva las huellas del código y la 4.8 cambia `ficha.py`, `pipeline.py` y
`verificar_paquete.sh`. Este guion reutiliza, sin modificarlo, `ejecutar_baterias_4_7_1.py` (mismas copias temporales, mismas
sustituciones de código y misma firma) y comprueba por separado:
  - que el estado de cada prueba, el principio de las que fallan y la línea final coinciden con lo conservado en la 4.7.1;
  - qué huellas cambian y que son solo las de los archivos que la 4.8 declara cambiados.
Solo escribe en temporales. Código 0 si todo coincide.
"""
import importlib.util
import os
import sys

sys.dont_write_bytecode = True
AQUI = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RUNNER = os.path.join(os.path.dirname(AQUI), "2026-11_Vidrala_ensayo_4_7_1", "scripts", "ejecutar_baterias_4_7_1.py")
CAMBIAN_EN_4_8 = {"ficha.py", "pipeline.py", "verificar_paquete.sh"}

spec = importlib.util.spec_from_file_location("ejecutar_baterias_4_7_1", RUNNER)
eb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(eb)


def tabla(linea):
    return dict(x.rsplit(" ", 1) for x in linea[len("# código: "):].split(" · "))


todo = True
for destino, (prueba, sust) in eb.CASOS.items():
    txt, rc = eb.ejecutar(prueba, sust)
    f = eb.firma(txt)
    g = eb.firma(open(os.path.join(eb.AQUI, destino), encoding="utf-8").read())
    nuevas, viejas = tabla(f[0]), tabla(g[0])
    distintas = {k for k in nuevas if nuevas[k] != viejas.get(k)}
    iguales = f[1:] == g[1:]
    huellas_ok = distintas <= CAMBIAN_EN_4_8 and set(nuevas) == set(viejas)
    todo &= iguales and huellas_ok
    print(f"{destino}: código {rc} · {f[3][0] if f[3] else 'sin línea final'} · estados, fallos y línea final "
          f"{'IGUALES' if iguales else 'DISTINTOS'} a los conservados · huellas distintas: {', '.join(sorted(distintas)) or 'ninguna'}"
          f"{'' if huellas_ok else ' (FUERA DE LO DECLARADO)'}")
print("RESULTADO:", "las tres baterías coinciden con las conservadas salvo las huellas de los archivos que cambia la 4.8" if todo else "HAY DIFERENCIAS")
sys.exit(0 if todo else 1)
