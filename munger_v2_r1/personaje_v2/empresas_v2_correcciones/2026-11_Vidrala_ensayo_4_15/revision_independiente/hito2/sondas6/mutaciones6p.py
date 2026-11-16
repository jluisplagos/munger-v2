#!/usr/bin/env python3
"""Mutaciones de la sexta comprobación SOBRE EL ÁRBOL CON LAS PRUEBAS PROPUESTAS (fable/prop6t: el código de 8196522 y los casos de prueba
que propone el revisor en W1). Sirve para confirmar con la batería ENTERA que las mutaciones que hoy sobreviven se detectarían con esos
casos. Mismo arnés (mutaciones4.py) y mismas definiciones (mutantes6.py); resultados en mut6p/<nombre>/resultado.json. No es código entregado.
Uso: python3 -I -B mutaciones6p.py [-j N] NOMBRE [NOMBRE …]"""
import concurrent.futures, json, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
F = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(F, "sondas4"))
sys.path.insert(0, AQUI)
import mutaciones4 as m4  # noqa: E402
import mutantes6 as MU  # noqa: E402
m4.COPIA = os.path.join(F, "prop6t", "munger_v2_r1")
m4.MUT = os.path.join(F, "mut6p")
m4.M = MU.M
assert all(set(v[4]) <= {m4.B415, m4.BEE, m4.B414} for v in MU.M.values())  # solo las baterías permitidas

if __name__ == "__main__":
    args = sys.argv[1:]
    j = 1
    if args[:1] == ["-j"]:
        j, args = int(args[1]), args[2:]
    mal = m4.comprobar_textos()
    if mal:
        print("TEXTOS QUE NO APARECEN EXACTAMENTE UNA VEZ:", mal)
        sys.exit(2)
    with concurrent.futures.ThreadPoolExecutor(max_workers=j) as ex:
        for r in ex.map(m4.correr, args):
            print(json.dumps(r, ensure_ascii=False))
            sys.stdout.flush()
