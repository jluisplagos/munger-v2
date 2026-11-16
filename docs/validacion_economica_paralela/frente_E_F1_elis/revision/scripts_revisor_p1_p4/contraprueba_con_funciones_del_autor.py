"""Contraprueba con las funciones del autor · revisión dirigida a P1–P4 · propuesta de decisiones F1.

Script de revisión. Carga, sin modificarlo, `controles_sinteticos_f1.py` del commit congelado y usa sus propias
funciones (`Escenario`, `motor_sintetico`, `caja_sintetica`, `motor_a`) para tres comprobaciones:

  1. Sus casos coherentes P1b (transición con término explícito) y P2d (compras de reposición con término explícito)
     pasan a cobrar de más si el motor recibe el ancla de S2C que da la fórmula de la especificación, E4, con una
     ventana que crece 5: 5 ÷ (5 + 7) y 5 ÷ (5 + 9). En sus casos el ancla se escribe a mano (1) y P1b va a
     crecimiento cero. Así el resultado no depende del motor del revisor.
  2. El motor sintético y `motor_a` solo coinciden con crecimiento y margen constantes: con una palanca g de los años
     1–5 distinta de g∞, `motor_a` baja el crecimiento en los años 6–10 y el sintético no.
  3. Recuento de casos por crecimiento, para ver cuántos casos de P1 se prueban con crecimiento. (Todos los casos
     del autor son sin impuestos: lo dice su cabecera, «sin impuestos, sin circulante ni intereses de deuda».)

Importes ficticios; no son datos de Elis.

Uso: python3 -I contraprueba_con_funciones_del_autor.py --scripts-autor <frente>/scripts \
        --controles-autor <frente>/resultados/controles_sinteticos_f1.json \
        --salida ../resultados_revisor_p1_p4/contraprueba_con_funciones_del_autor.json \
        --informe ../resultados_revisor_p1_p4/contraprueba_con_funciones_del_autor.txt
"""
import argparse
import importlib.util
import json
import sys
from fractions import Fraction as Fr
from pathlib import Path


def num(x):
    x = Fr(x)
    return int(x) if x.denominator == 1 else round(float(x), 6)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--scripts-autor", required=True, type=Path)
    ap.add_argument("--controles-autor", required=True, type=Path)
    ap.add_argument("--salida", required=True, type=Path)
    ap.add_argument("--informe", required=True, type=Path)
    a = ap.parse_args()
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location("controles_autor", a.scripts_autor / "controles_sinteticos_f1.py")
    M = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(M)
    V0, N = M.V0, M.N
    lineas, res = [], {}

    def p(s=""):
        lineas.append(s)

    def correr(esc, R, g, s2c, extra):
        m = esc.ebit_ventana() / V0
        f = esc.f(Fr(R))
        roic = (1 + g) * m * s2c if g else Fr(1)
        fl, term, _ = M.motor_sintetico(m, f, g, s2c, roic, g, extra)
        cj, cterm = M.caja_sintetica(esc, g, g)
        dif = [x - y for x, y in zip(fl, cj)] + [term - cterm]
        return {"f": num(f), "S2C_del_motor": num(s2c), "g": num(g),
                "motor_menos_caja": {"año_1": num(dif[0]), "año_5": num(dif[4]), "año_6": num(dif[5]), "año_10": num(dif[9]), "terminal": num(dif[10])},
                "coherente": all(d == 0 for d in dif)}

    base = dict(ebitda=100, d_propia=20, rou=10, pagos_arr=12, mant=20)
    g5 = Fr("0.05")
    temporal = lambda t: Fr(7) if t <= 5 else Fr(0)                  # noqa: E731
    cobro_t = lambda t, Vt: Fr(7) if t <= 5 else Fr(0)               # noqa: E731
    cobro_r = lambda t, Vt: Fr(9) * Vt / V0                          # noqa: E731

    p("1. CASOS COHERENTES DEL AUTOR CON EL ANCLA QUE DA LA FÓRMULA DE E4")
    esc1 = M.Escenario(**dict(base, trans_v=7), trans=temporal)
    esc2 = M.Escenario(**base, rep_adq=9)
    res["P1b"] = {
        "como lo ejecuta el autor (g = 0, S2C = 1)": correr(esc1, 20, Fr(0), Fr(1), cobro_t),
        "con g = 5 % y S2C = 1 (ancla sin la transición)": correr(esc1, 20, g5, Fr(1), cobro_t),
        "con g = 5 % y el ancla de E4 con D_X = R: 5 ÷ (5 + 7)": correr(esc1, 20, g5, Fr(5, 12), cobro_t)}
    res["P2d"] = {
        "como lo ejecuta el autor (g = 5 %, S2C = 1, escrita a mano)": correr(esc2, 20, g5, Fr(1), cobro_r),
        "con g = 5 % y el ancla de E4 con D_X = R_propia: 5 ÷ (5 + 9)": correr(esc2, 20, g5, Fr(5, 14), cobro_r)}
    for caso, filas in res.items():
        p(f"  {caso}")
        for nombre, v in filas.items():
            p(f"      {nombre}: coherente {v['coherente']}; motor − caja {v['motor_menos_caja']}")
    ok1 = (res["P1b"]["como lo ejecuta el autor (g = 0, S2C = 1)"]["coherente"]
           and res["P1b"]["con g = 5 % y S2C = 1 (ancla sin la transición)"]["coherente"]
           and not res["P1b"]["con g = 5 % y el ancla de E4 con D_X = R: 5 ÷ (5 + 7)"]["coherente"]
           and res["P2d"]["como lo ejecuta el autor (g = 5 %, S2C = 1, escrita a mano)"]["coherente"]
           and not res["P2d"]["con g = 5 % y el ancla de E4 con D_X = R_propia: 5 ÷ (5 + 9)"]["coherente"])

    p()
    p("2. MOTOR SINTÉTICO FRENTE A motor_a")
    m, f, s2c, roic = Fr("0.7"), Fr("0.02"), Fr(1), Fr("0.714")
    iguales, distintos = [], []
    for g15, gi in ((Fr("0.05"), Fr("0.05")), (Fr("0.05"), Fr("0.02"))):
        fl, term, _ = M.motor_sintetico(m, f, g15, s2c, roic, gi)
        ref = M.motor_a(V0, m, Fr(0), f, g15, m, s2c, gi, roic)
        d = [abs(x - y) for x, y in zip(fl, ref["flujos"])] + [abs(term - ref["flujo_11"])]
        fila = {"g_años_1_5": num(g15), "g_inf": num(gi), "diferencia_maxima": num(max(d)),
                "años_con_diferencia": [t + 1 for t in range(N) if d[t] != 0] + (["año 11"] if d[N] != 0 else [])}
        (iguales if max(d) == 0 else distintos).append(fila)
        p(f"  g 1–5 = {num(g15)}, g∞ = {num(gi)}: diferencia máxima {fila['diferencia_maxima']}; años con diferencia {fila['años_con_diferencia'] or 'ninguno'}")
    res["motor_sintetico_frente_a_motor_a"] = {"coinciden": iguales, "no_coinciden": distintos}
    ok2 = len(iguales) == 1 and len(distintos) == 1

    p()
    p("3. CASOS DEL AUTOR POR CUESTIÓN Y CRECIMIENTO")
    casos = json.loads(a.controles_autor.read_text(encoding="utf-8"))["casos"]
    cuenta = {}
    for c in casos:
        k = c["cuestion"]
        cuenta.setdefault(k, {"casos": 0, "con_crecimiento": 0})
        cuenta[k]["casos"] += 1
        cuenta[k]["con_crecimiento"] += 1 if (c["parametros"]["g_anios_1_10"] or c["parametros"]["g_terminal"]) else 0
    res["casos_del_autor"] = cuenta
    for k, v in cuenta.items():
        p(f"  {k}: {v['casos']} casos; con crecimiento {v['con_crecimiento']}")
    ok3 = cuenta["P1"]["con_crecimiento"] == 0
    res["resumen"] = {"1_el_ancla_de_E4_rompe_P1b_y_P2d": ok1, "2_el_motor_sintetico_solo_coincide_con_g_constante": ok2,
                      "3_ningun_caso_de_P1_tiene_crecimiento": ok3}
    p()
    p(f"RESUMEN: {res['resumen']}")
    a.salida.write_text(json.dumps(res, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    a.informe.write_text("\n".join(lineas) + "\n", encoding="utf-8")
    print("\n".join(lineas))
    return 0 if (ok1 and ok2 and ok3) else 1


if __name__ == "__main__":
    sys.exit(main())
