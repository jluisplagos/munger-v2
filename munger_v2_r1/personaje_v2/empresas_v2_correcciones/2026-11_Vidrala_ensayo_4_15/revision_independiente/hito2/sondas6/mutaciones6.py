#!/usr/bin/env python3
"""Mutaciones de la SEXTA comprobación (Fable, hito 2 de la 4.15, candidata 8196522), con la batería ENTERA. Usa el arnés de
mutaciones4.py (preparar y correr: un árbol ligero aparte por mutación, con scripts/, pruebas/ y esquema/ copiados de «copia» y el resto
enlaces; solo baterías permitidas, sin LibreOffice) y las definiciones de mutantes6.py.
Resultados en mut6/<nombre>/resultado.json (se guardan al terminar cada una; «pendientes» repite solo lo que falta).
Uso: python3 -I -B mutaciones6.py [-j N] NOMBRE [NOMBRE …] | todas | v | v4 | control | pendientes | lista"""
import concurrent.futures, json, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
F = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(F, "sondas4"))
sys.path.insert(0, AQUI)
import mutaciones4 as m4  # noqa: E402
import mutantes6 as MU  # noqa: E402
assert m4.F == F and m4.COPIA == os.path.join(F, "copia", "munger_v2_r1")
assert set(MU.M["c00_control"][4]) <= {"test_verificacion_entradas_415.py", "test_entrada_efectiva_415.py", "test_verificacion_entradas_414.py"}
assert all(set(v[4]) <= {m4.B415, m4.BEE, m4.B414} for v in MU.M.values())  # solo las baterías permitidas
m4.MUT = os.path.join(F, "mut6")
m4.M = MU.M
M = MU.M

if __name__ == "__main__":
    args = sys.argv[1:]
    j = 1
    if args[:1] == ["-j"]:
        j, args = int(args[1]), args[2:]
    mal = m4.comprobar_textos()
    if mal:
        print("TEXTOS QUE NO APARECEN EXACTAMENTE UNA VEZ:", mal)
        sys.exit(2)
    if not args or args == ["lista"]:
        for k, v in M.items():
            print(k, "·", v[0], "·", v[1], "·", v[2], "·", v[4])
        print(len(M), "mutaciones; textos comprobados")
        sys.exit(0)
    if args == ["todas"]:
        nombres = list(M)
    elif len(args) == 1 and args[0] in ("v", "v4", "control"):
        nombres = [k for k, v in M.items() if v[0] == args[0]]
    elif args == ["pendientes"]:
        nombres = [k for k in M if not os.path.exists(os.path.join(m4.MUT, k, "resultado.json"))]
    else:
        nombres = args
    with concurrent.futures.ThreadPoolExecutor(max_workers=j) as ex:
        for r in ex.map(m4.correr, nombres):
            print(json.dumps(r, ensure_ascii=False))
            sys.stdout.flush()
