"""Umbral de materialidad de V-F1a · medida y casos de frontera · F1. Importes ficticios; no son datos de ninguna empresa.

Apoyo de PROPUESTA_UMBRAL_V-F1a.md. No adopta ningún umbral y no cambia la especificación: V-F1a sigue bloqueando con
cualquier importe mientras no se decida otra cosa. Calcula, con aritmética exacta (fracciones), el estado que daría cada
opción de umbral en casos de frontera escritos a mano, y lo compara con el estado esperado de cada caso.

Medidas (motor A, perímetro `A0_total`, ventana de n ejercicios):
  X   = amortización de los derechos de uso (D&A ROU) media de la ventana: el exceso que A0 carga de más, a la escala
        de la ventana, a crecimiento cero y en el año 11 (ρ·V, con ρ = f_A0 − f_A1 = Σ D&A ROU ÷ Σ ventas).
  B   = cota de redondeo del FCF base registrado: media de la ventana de Σ |coeficiente| × media unidad de la última
        cifra impresa de cada cifra publicada que lo compone (coeficientes netos: una cifra que entra y sale no cuenta).
  e   = X ÷ FCF base (solo si el FCF base es positivo).
  ρ   = X ÷ ventas medias.
Opciones:
  U0   sin umbral: bloquea con cualquier importe positivo (lo vigente).
  UP01 la propuesta: uno por mil del FCF base. AVISO si e ≤ 0,1 %; BLOQUEA si e > 0,1 % o si el FCF base no es positivo.
  UR   de resolución: AVISO si X ≤ B; BLOQUEA si X > B.
  UP1 y UP5  de política, más anchos: como UP01 con 1 % y 5 %.
  UV1  el de la versión 1, sobre las ventas: BLOQUEA si ρ ≥ 0,5 %; AVISO por debajo.
La comparación es exacta y sin dividir (X ≤ u·FCF base). En la frontera (e = u) no bloquea, como el aviso del terminal
del libro, que solo salta si |salto| supera C179.
Los demás controles no cambian con ninguna opción: V-F1b (fila vacía), V-F1e (invariantes) y V-F1m (solo uno positivo).

Uso:
  python3 -I umbral_v_f1a_frontera.py --salida ../resultados/umbral_v_f1a_frontera.json \
     --informe ../resultados/umbral_v_f1a_frontera.md [--cifras ../datos/cifras_fuente.csv \
     --verificacion ../resultados/verificacion_cifras.json]
Con --cifras y --verificacion añade, solo como información, las medidas de Elis con cifras verificadas.
Termina con 1 si algún caso no da su estado esperado.
"""
import argparse
import importlib.util
import json
import sys
from fractions import Fraction as Fr
from pathlib import Path

OPCIONES = {"U0": ("sin umbral (vigente)", None), "UP01": ("propuesta: e ≤ 0,1 % del FCF base", Fr(1, 1000)),
            "UR": ("resolución: X ≤ cota de redondeo del FCF base", None),
            "UP1": ("política: e ≤ 1 % del FCF base", Fr(1, 100)), "UP5": ("política: e ≤ 5 % del FCF base", Fr(5, 100)),
            "UV1": ("versión 1: ρ < 0,5 % de las ventas", Fr(5, 1000))}
BLQ, AVI, ADM, NAP = "V-F1a BLOQUEA", "V-F1a AVISO", "A0 admisible", "no aplica"
VB, VE, VM = "V-F1b BLOQUEA", "V-F1e BLOQUEA", "V-F1m BLOQUEA"


def fr(x):
    return None if x is None else Fr(str(x))


def cota_de_redondeo(componentes):
    """componentes: por año, lista de (identificador, coeficiente, decimales impresos). Los decimales pueden ser negativos
    (una cifra en miles impresa a centenas de millar: −2). Devuelve la media de la ventana de Σ |coef. neto| × media unidad."""
    total = Fr(0)
    for año in componentes:
        neto = {}
        for ident, coef, dec in año:
            c, d = neto.get(ident, (Fr(0), dec))
            neto[ident] = (c + coef, d)
        total += sum(abs(c) * Fr(5) / Fr(10) ** (d + 1) for c, d in neto.values())
    return total / len(componentes)


def evaluar(caso, opcion):
    """Estado de un caso con una opción de umbral. Orden de E5: dominio del control, invariantes, fila vacía, dominio de A0, umbral."""
    if caso.get("motor", "A") != "A" or caso.get("perimetro", "A0_total") != "A0_total":
        return NAP, "V-F1a solo se evalúa en el motor A con el perímetro A0_total"
    rou, c49 = [fr(x) for x in caso["rou"]], fr(caso["c49"])
    if c49 < 0 or any(x is not None and x < 0 for x in rou):
        return VE, "magnitud negativa: invariantes de E1"
    if any(x is None for x in rou):
        return (VB, "fila de D&A ROU vacía en algún año de la ventana: vacío no es cero") if c49 > 0 else \
               ("fuera de E5", "fila vacía con C49 = 0: E5 no nombra este caso (por E1, vacío no es cero)")
    X = sum(rou) / len(rou)
    if X == 0 and c49 == 0:
        return ADM, "sin arrendamientos"
    if X == 0 or c49 == 0:
        return VM, "solo uno de D&A ROU y C49 es positivo: fuera del dominio de A0; no se afirma doble cómputo"
    fcf, S = fr(caso["fcf"]), sum(fr(v) for v in caso["ventas"]) / len(caso["ventas"])
    if opcion == "U0":
        return BLQ, "sin umbral: bloquea con cualquier importe"
    if opcion == "UR":
        B = cota_de_redondeo(caso["componentes"])
        return (AVI, "X ≤ B: el exceso no supera la cota de redondeo del FCF base") if X <= B else (BLQ, "X > B")
    if opcion in ("UP01", "UP1", "UP5"):
        u = OPCIONES[opcion][1]
        if fcf <= 0:
            return BLQ, "FCF base no positivo: la medida no está definida y no hay exención"
        return (AVI, "e ≤ u") if X <= u * fcf else (BLQ, "e > u")       # sin dividir: comparación exacta
    if opcion == "UV1":
        return (BLQ, "ρ ≥ 0,5 % de las ventas") if X >= OPCIONES[opcion][1] * S else (AVI, "ρ < 0,5 % de las ventas")
    raise ValueError(opcion)


def comp(dec, n, extra=()):
    """Cinco cifras publicadas del FCF base por año (CFO, capex neto, intereses, pagos de arrendamiento, SBC), con `dec`
    decimales impresos; `extra` añade cifras con su coeficiente (para el caso de los coeficientes que se anulan)."""
    base = [("cfo", Fr(1), dec), ("capnet", Fr(-1), dec), ("int", Fr(-1), dec), ("leasepay", Fr(-1), dec), ("sbc", Fr(-1), dec)]
    return [base + list(extra) for _ in range(n)]


V3 = [1000, 1000, 1000]
PR = ("princ", Fr(1), 1), ("princ", Fr(-1), 1)      # el principal entra en C48 (+1, dentro de pagos − principal) y en C49 (−1)
# (id, descripción, caso, estado esperado por opción en el orden U0, UP01, UR, UP1, UP5, UV1)
CASOS = [
    ("F01", "sin arrendamientos (los dos a cero)", dict(rou=[0, 0, 0], c49=0, fcf=100, ventas=V3, componentes=comp(1, 3)), [ADM] * 6),
    ("F02", "solo C49 positivo", dict(rou=[0, 0, 0], c49="0.3", fcf=100, ventas=V3, componentes=comp(1, 3)), [VM] * 6),
    ("F03", "solo D&A ROU positiva", dict(rou=["0.3", "0.3", "0.3"], c49=0, fcf=100, ventas=V3, componentes=comp(1, 3)), [VM] * 6),
    ("F04", "fila de D&A ROU vacía en un año, con C49 positivo", dict(rou=["0.3", None, "0.3"], c49="0.3", fcf=100, ventas=V3, componentes=comp(1, 3)), [VB] * 6),
    ("F05", "D&A ROU negativa en un año", dict(rou=["0.3", "-0.1", "0.3"], c49="0.3", fcf=100, ventas=V3, componentes=comp(1, 3)), [VE] * 6),
    ("F06", "arrendamientos grandes con el perímetro A1_sin_ROU", dict(perimetro="A1_sin_ROU", rou=[50, 50, 50], c49=50, fcf=100, ventas=V3, componentes=comp(1, 3)), [NAP] * 6),
    ("F07", "frontera del uno por mil, igualdad: X = 0,3 y FCF base 300", dict(rou=["0.3", "0.3", "0.3"], c49="0.3", fcf=300, ventas=[3000] * 3, componentes=comp(1, 3)), [BLQ, AVI, BLQ, AVI, AVI, AVI]),
    ("F08", "justo por encima del uno por mil: e = 0,1111 %", dict(rou=["0.3", "0.3", "0.4"], c49="0.3", fcf=300, ventas=[3000] * 3, componentes=comp(1, 3)), [BLQ, BLQ, BLQ, AVI, AVI, AVI]),
    ("F09", "justo por debajo del uno por mil: e = 0,0889 %", dict(rou=["0.2", "0.3", "0.3"], c49="0.3", fcf=300, ventas=[3000] * 3, componentes=comp(1, 3)), [BLQ, AVI, BLQ, AVI, AVI, AVI]),
    ("F10", "uno por mil, igualdad exacta que la coma flotante no ve: 0,1 + 0,2 + 0,3 y FCF base 200", dict(rou=["0.1", "0.2", "0.3"], c49="0.2", fcf=200, ventas=[2000] * 3, componentes=comp(2, 3)), [BLQ, AVI, BLQ, AVI, AVI, AVI]),
    ("F11", "resolución, por debajo: X = 0,2333 < B = 0,25 (e = 0,2333 %)", dict(rou=["0.2", "0.2", "0.3"], c49="0.2", fcf=100, ventas=V3, componentes=comp(1, 3)), [BLQ, BLQ, AVI, AVI, AVI, AVI]),
    ("F12", "resolución, igualdad: X = B = 0,25 (ventana de dos años)", dict(rou=["0.2", "0.3"], c49="0.25", fcf=100, ventas=[1000, 1000], componentes=comp(1, 2)), [BLQ, BLQ, AVI, AVI, AVI, AVI]),
    ("F13", "resolución, justo por encima: X = 0,2667 > B = 0,25", dict(rou=["0.2", "0.3", "0.3"], c49="0.25", fcf=100, ventas=V3, componentes=comp(1, 3)), [BLQ, BLQ, BLQ, AVI, AVI, AVI]),
    ("F14", "frontera del 1 %, igualdad", dict(rou=[1, 1, 1], c49=1, fcf=100, ventas=V3, componentes=comp(1, 3)), [BLQ, BLQ, BLQ, AVI, AVI, AVI]),
    ("F15", "justo por encima del 1 %: e = 1,001 %", dict(rou=[1, 1, "1.003"], c49=1, fcf=100, ventas=V3, componentes=comp(1, 3)), [BLQ, BLQ, BLQ, BLQ, AVI, AVI]),
    ("F16", "frontera del 5 % del FCF base y del 0,5 % de las ventas a la vez (igualdad en las dos)", dict(rou=[5, 5, 5], c49=5, fcf=100, ventas=V3, componentes=comp(1, 3)), [BLQ, BLQ, BLQ, BLQ, AVI, BLQ]),
    ("F17", "margen estrecho: ρ = 0,4 % de las ventas y e = 20 % del FCF base", dict(rou=[4, 4, 4], c49=4, fcf=20, ventas=V3, componentes=comp(1, 3)), [BLQ, BLQ, BLQ, BLQ, BLQ, AVI]),
    ("F18", "margen ancho: ρ = 0,6 % de las ventas y e = 2 % del FCF base", dict(rou=[6, 6, 6], c49=6, fcf=300, ventas=V3, componentes=comp(1, 3)), [BLQ, BLQ, BLQ, BLQ, AVI, BLQ]),
    ("F19", "FCF base cero con arrendamiento al nivel del redondeo", dict(rou=["0.2", "0.2", "0.2"], c49="0.2", fcf=0, ventas=V3, componentes=comp(1, 3)), [BLQ, BLQ, AVI, BLQ, BLQ, AVI]),
    ("F20", "FCF base negativo con ρ = 0,2 % de las ventas", dict(rou=[2, 2, 2], c49=2, fcf=-50, ventas=V3, componentes=comp(1, 3)), [BLQ, BLQ, BLQ, BLQ, BLQ, AVI]),
    ("F21", "el caso F07 en miles, con la misma precisión impresa (centenas de millar): mismo resultado", dict(rou=[300, 300, 300], c49=300, fcf=300000, ventas=[3000000] * 3, componentes=comp(-2, 3)), [BLQ, AVI, BLQ, AVI, AVI, AVI]),
    ("F22", "el caso F11 en miles, con la misma precisión impresa: mismo resultado", dict(rou=[200, 200, 300], c49=200, fcf=100000, ventas=[1000000] * 3, componentes=comp(-2, 3)), [BLQ, BLQ, AVI, AVI, AVI, AVI]),
    ("F23", "los importes de F22 con el millar impreso: la resolución depende de la precisión de la fuente; el porcentaje, no", dict(rou=[200, 200, 300], c49=200, fcf=100000, ventas=[1000000] * 3, componentes=comp(0, 3)), [BLQ, BLQ, BLQ, AVI, AVI, AVI]),
    ("F24", "coeficientes que se anulan: el principal entra y sale y no cuenta en la cota (B = 0,25, no 0,35)", dict(rou=["0.3", "0.3", "0.3"], c49="0.3", fcf=100, ventas=V3, componentes=comp(1, 3, extra=PR)), [BLQ, BLQ, BLQ, AVI, AVI, AVI]),
    ("F25", "un año de la ventana con D&A ROU cero y media positiva (e = 0,0667 %)", dict(rou=[0, "0.3", "0.3"], c49="0.2", fcf=300, ventas=[3000] * 3, componentes=comp(1, 3)), [BLQ, AVI, AVI, AVI, AVI, AVI]),
    ("F26", "baja precisión de la fuente: FCF base 3,0 y D&A ROU 0,2 (dos unidades de la última cifra; e = 6,67 %)", dict(rou=["0.2", "0.2", "0.2"], c49="0.2", fcf=3, ventas=[30, 30, 30], componentes=comp(1, 3)), [BLQ, BLQ, AVI, BLQ, BLQ, BLQ]),
    ("F27", "caso T5 de la especificación (arrendamiento material): ROU 10, FCF verdadero 68", dict(rou=[10, 10, 10], c49=10, fcf=68, ventas=[400, 400, 400], componentes=comp(1, 3)), [BLQ] * 6),
    ("F28", "caso T5 con arrendamiento mínimo: ROU 0,2, FCF verdadero 79,76 (e = 0,2508 %)", dict(rou=["0.2", "0.2", "0.2"], c49="0.2", fcf="79.76", ventas=[400, 400, 400], componentes=comp(1, 3)), [BLQ, BLQ, AVI, AVI, AVI, AVI]),
    ("F29", "caso T5 con arrendamiento ínfimo: ROU 0,05, FCF verdadero 79,94 (e = 0,0625 %)", dict(rou=["0.05", "0.05", "0.05"], c49="0.05", fcf="79.94", ventas=[400, 400, 400], componentes=comp(2, 3)), [BLQ, AVI, BLQ, AVI, AVI, AVI]),
    ("F30", "motor B", dict(motor="B", rou=[50, 50, 50], c49=50, fcf=100, ventas=V3, componentes=comp(1, 3)), [NAP] * 6),
]


def t5(rou, pagos):
    """Caso sintético T5 de la especificación (τ = 0, sin crecimiento): EBITDA 100; capex propio = D&A propia = 20.
    Devuelve el flujo verdadero y los de A0 y A1, con f calibrada con la fórmula de E3."""
    ebitda, capex, da_propia, S = Fr(100), Fr(20), Fr(20), Fr(400)
    rou, pagos = fr(rou), fr(pagos)
    ebit = ebitda - da_propia - rou
    fcf = ebitda - capex - pagos                                    # los pagos de arrendamiento se cuentan una vez
    f = {k: (ebit - (capex - dx) - fcf) / S for k, dx in (("A0", da_propia + rou), ("A1", da_propia))}
    return {"FCF_verdadero": fcf, "flujo_A0": ebit - f["A0"] * S, "flujo_A1": ebit - f["A1"] * S, "f_A0_menos_f_A1": f["A0"] - f["A1"], "rho": rou / S}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--salida", required=True, type=Path)
    ap.add_argument("--informe", required=True, type=Path)
    ap.add_argument("--cifras", type=Path)
    ap.add_argument("--verificacion", type=Path)
    a = ap.parse_args()
    f6 = lambda x, n=6: None if x is None else round(float(x), n)   # noqa: E731
    errores, filas = [], []
    for ident, desc, caso, esperado in CASOS:
        est = {o: evaluar(caso, o) for o in OPCIONES}
        ok = [est[o][0] for o in OPCIONES] == esperado
        if not ok:
            errores.append(ident)
        rou = [fr(x) for x in caso["rou"]]
        medible = caso.get("motor", "A") == "A" and all(x is not None for x in rou)
        X = sum(rou) / len(rou) if medible else None
        fcf, S = fr(caso["fcf"]), sum(fr(v) for v in caso["ventas"]) / len(caso["ventas"])
        filas.append({"caso": ident, "descripcion": desc, "X_exceso_medio": f6(X), "B_cota_de_redondeo_del_FCF_base": f6(cota_de_redondeo(caso["componentes"])),
                      "e_sobre_el_FCF_base_pct": f6(100 * X / fcf, 4) if medible and fcf > 0 else None, "rho_sobre_las_ventas_pct": f6(100 * X / S, 4) if medible else None,
                      "estado": {o: est[o][0] for o in OPCIONES}, "motivo": {o: est[o][1] for o in OPCIONES}, "esperado": dict(zip(OPCIONES, esperado)), "ok": ok})
    # comprobaciones directas
    directas = []

    def directa(nombre, cond):
        directas.append({"comprobacion": nombre, "ok": bool(cond)})
        if not cond:
            errores.append(nombre)
    directa("cota con cinco cifras de un decimal = 0,25", cota_de_redondeo(comp(1, 3)) == Fr(1, 4))
    directa("cota con una cifra que entra y sale (coeficiente neto cero) = 0,25", cota_de_redondeo(comp(1, 3, extra=(("princ", Fr(1), 1), ("princ", Fr(-1), 1)))) == Fr(1, 4))
    directa("cota en miles con precisión de centenas de millar = 250", cota_de_redondeo(comp(-2, 3)) == Fr(250))
    directa("coma flotante: (0.1 + 0.2 + 0.3) / 3 / 200 > 0.001 (por eso la comparación es exacta)", (0.1 + 0.2 + 0.3) / 3 / 200 > 0.001)
    directa("exacto: (0,1 + 0,2 + 0,3) / 3 / 200 = 0,1 %", (Fr("0.1") + Fr("0.2") + Fr("0.3")) / 3 / 200 == Fr(1, 1000))
    a_mat, a_min, a_inf = t5(10, 12), t5("0.2", "0.24"), t5("0.05", "0.06")
    directa("T5: FCF verdadero 68, A1 = 68, A0 = 58; el exceso es la D&A ROU", (a_mat["FCF_verdadero"], a_mat["flujo_A1"], a_mat["flujo_A0"]) == (68, 68, 58))
    directa("T5: f_A0 − f_A1 = ρ = D&A ROU ÷ ventas", a_mat["f_A0_menos_f_A1"] == a_mat["rho"] and a_min["f_A0_menos_f_A1"] == a_min["rho"])
    directa("T5 con arrendamiento mínimo: FCF verdadero 79,76; A0 da 79,56 (0,2 de menos)", (a_min["FCF_verdadero"], a_min["flujo_A1"], a_min["flujo_A0"]) == (Fr("79.76"), Fr("79.76"), Fr("79.56")))
    directa("T5 con arrendamiento ínfimo: FCF verdadero 79,94; A0 da 79,89 (0,05 de menos, lo que el AVISO de la propuesta toleraría)",
            (a_inf["FCF_verdadero"], a_inf["flujo_A1"], a_inf["flujo_A0"]) == (Fr("79.94"), Fr("79.94"), Fr("79.89")))
    # con el FCF base nulo o negativo, la comparación sin dividir ya bloquea; la guarda da además el motivo correcto
    sin_fcf = dict(rou=["0.2"] * 3, c49="0.2", ventas=V3, componentes=comp(1, 3))
    directa("FCF base cero o negativo: el motivo mostrado es que la medida no está definida",
            all(evaluar(dict(sin_fcf, fcf=x), "UP01") == (BLQ, "FCF base no positivo: la medida no está definida y no hay exención") for x in (0, -50)))
    # sin umbral, los cuatro casos de A0 (W3) dan el estado vigente
    w3 = {(1, 1): BLQ, (0, 0): ADM, (1, 0): VM, (0, 1): VM}
    for (r, c), esp in w3.items():
        directa(f"vigente (sin umbral), D&A ROU {'positiva' if r else 'cero'} y C49 {'positivo' if c else 'cero'}: {esp}",
                evaluar(dict(rou=[r * Fr(1, 10)] * 3, c49=c * Fr(1, 10), fcf=100, ventas=V3, componentes=comp(1, 3)), "U0")[0] == esp)
    # el 0,5 % de las ventas expresado sobre el flujo, según el margen de FCF base sobre ventas
    equivalencia = [{"FCF_base_sobre_ventas_pct": m, "medio_punto_de_ventas_sobre_el_FCF_base_pct": f6(Fr(50) / m, 2),
                     "uno_por_mil_del_FCF_base_sobre_las_ventas_pct": f6(Fr(m) / 10, 3)} for m in (2, 5, 10, 20, 30)]

    elis = None
    if a.cifras and a.verificacion:
        spec = importlib.util.spec_from_file_location("contraste_f1", Path(__file__).with_name("contraste_f1.py"))
        C = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(C)
        F = C.Fuente(a.cifras, a.verificacion)
        A = {y: C.datos_anio(F, y) for y in C.VENTANA}
        av = lambda fn: sum(fn(A[y]) for y in C.VENTANA) / 3   # noqa: E731
        r3 = lambda x: Fr(round(x, 3)).limit_denominator(1000)   # noqa: E731
        C52 = r3(av(lambda d: d["cfo"])) - r3(av(lambda d: d["capnet"])) - av(lambda d: d["int"]) - av(lambda d: d["leasepay"]) - r3(av(lambda d: d["sbc"]))
        X = av(lambda d: d["da_rou"])
        ids = {2025: "_2025", 2024: "_2024", 2023: "_FR_2023"}
        B = sum(sum(F.epsilon(b + ids[y]) for b in ("CF_CFO", "FCF_CAPNET", "CF_INT", "CF_LEASE", "CF_SBC")) for y in C.VENTANA) / 3
        caso = dict(rou=[A[y]["da_rou"] for y in C.VENTANA], c49=av(lambda d: d["ls_princ"]), fcf=C52, ventas=[A[y]["ventas"] for y in C.VENTANA],
                    componentes=[[(b, Fr(1), F.meta[b + ids[y]]["decimales"]) for b in ("CF_CFO", "FCF_CAPNET", "CF_INT", "CF_LEASE", "CF_SBC")] for y in C.VENTANA])
        elis = {"nota": "solo información, con cifras verificadas; no es criterio para elegir ningún umbral. Por la decisión (1a), Elis no usa A0_total",
                "X_D&A_ROU_media_2023_25": f6(X, 3), "FCF_base_registrado": f6(C52, 3), "e_sobre_el_FCF_base_pct": f6(100 * X / C52, 2),
                "rho_sobre_las_ventas_pct": f6(100 * X / av(lambda d: d["ventas"]), 4), "B_cota_de_redondeo_del_FCF_base": f6(B, 3),
                "X_sobre_B": f6(X / B, 0), "estado_con_A0_total": {o: evaluar(caso, o)[0] for o in OPCIONES},
                "estado_con_el_perimetro_de_(1a)": evaluar(dict(caso, perimetro="A1_sin_ROU"), "U0")[0]}
        if C52 != Fr("307.933") or any(v != BLQ for v in elis["estado_con_A0_total"].values()):
            errores.append("Elis: FCF base distinto de 307,933 o algún umbral cambia su estado")

    res = {"naturaleza": "casos de frontera con importes ficticios; no adopta ningún umbral ni cambia la especificación",
           "opciones": {k: v[0] for k, v in OPCIONES.items()}, "casos": filas, "comprobaciones_directas": directas,
           "medio_punto_de_ventas_sobre_el_flujo": equivalencia, "elis_informativo": elis,
           "resumen": {"casos": len(filas), "casos_con_su_estado_esperado": sum(1 for x in filas if x["ok"]), "comprobaciones_directas": len(directas),
                       "directas_ok": sum(1 for x in directas if x["ok"]), "errores": errores}}
    a.salida.write_text(json.dumps(res, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = ["# Umbral de V-F1a · casos de frontera (importes ficticios)", "",
          "Generado por `scripts/umbral_v_f1a_frontera.py`. **No adopta ningún umbral.** X = D&A ROU media de la ventana; B = cota de redondeo "
          "del FCF base; e = X ÷ FCF base; ρ = X ÷ ventas medias.", "",
          f"Casos: {len(filas)}, con su estado esperado: {res['resumen']['casos_con_su_estado_esperado']}. Comprobaciones directas: "
          f"{res['resumen']['directas_ok']} de {len(directas)}.", "",
          "| Caso | Descripción | X | B | e (%) | ρ (%) | Sin umbral | Propuesta: 0,1 % FCF base | Resolución | 1 % FCF base | 5 % FCF base | 0,5 % ventas (v1) |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    corto = {BLQ: "BLOQUEA", AVI: "AVISO", ADM: "admisible", NAP: "no aplica", VB: "V-F1b", VE: "V-F1e", VM: "V-F1m"}
    for x in filas:
        md.append(f"| {x['caso']} | {x['descripcion']} | {x['X_exceso_medio']} | {x['B_cota_de_redondeo_del_FCF_base']} | {x['e_sobre_el_FCF_base_pct']} | "
                  f"{x['rho_sobre_las_ventas_pct']} | " + " | ".join(corto[x["estado"][o]] for o in OPCIONES) + " |")
    md += ["", "## El 0,5 % de las ventas, expresado sobre el flujo", "",
           "| FCF base ÷ ventas | 0,5 % de las ventas = … del FCF base | 0,1 % del FCF base = … de las ventas |", "|---|---|---|"] + \
          [f"| {x['FCF_base_sobre_ventas_pct']} % | {x['medio_punto_de_ventas_sobre_el_FCF_base_pct']} % | {x['uno_por_mil_del_FCF_base_sobre_las_ventas_pct']} % |"
           for x in equivalencia] + \
          ["", "## Comprobaciones directas", ""] + [f"- {'OK' if x['ok'] else 'FALLA'} · {x['comprobacion']}" for x in directas]
    if elis:
        md += ["", "## Elis (solo información; no es criterio)", ""] + [f"- {k}: {v}" for k, v in elis.items()]
    a.informe.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(json.dumps(res["resumen"], ensure_ascii=False))
    return 1 if errores else 0


if __name__ == "__main__":
    sys.exit(main())
