"""Tercera pasada · (h17) prueba de la batería sobre la forma canónica de la huella, y residuo 13 (calcular_entrada).
h17: se reproduce la expresión de la prueba (test_verificacion_entradas_415.py, líneas 451–455) con el mismo fixture y se repite con
una MUTACIÓN de _canon que ya no canoniza los números (849697.0 ≠ 849697): si la prueba sigue pasando, no prueba esa mitad del rótulo.
13: componente que no es objeto (en la serie y en un año), periodo con años desordenados y texto de la fuente generada."""
import copy, json, os, re, sys, unicodedata
import fx4 as fx
from fx4 import VE, ent, REG, K

e0 = copy.deepcopy(ent(REG, K))
print("K:", K, "| valor_modelo:", repr(e0["valor_modelo"]), type(e0["valor_modelo"]).__name__, "| valor_fuente:", repr(e0["fuente"]["valor_fuente"]), type(e0["fuente"]["valor_fuente"]).__name__)
e1 = copy.deepcopy(e0); e1["valor_modelo"] = float(e1["valor_modelo"]); e1["fuente"]["valor_fuente"] = float(e1["fuente"]["valor_fuente"])
print("e1 es idéntica a e0 (float(x) no cambia nada):", e1 == e0 and repr(e1) == repr(e0))
e2 = copy.deepcopy(e1); e2["fuente"]["cita"] = e2["fuente"]["cita"] + " "; e2["fuente"]["concepto"] = "  " + e2["fuente"]["concepto"]
e3 = copy.deepcopy(e1); e3["fuente"]["cita"] = e3["fuente"]["cita"] + " (otra)"


def expresion():
    return VE.huella_fundamento(e0) == VE.huella_fundamento(e1) == VE.huella_fundamento(e2) and VE.huella_fundamento(e3) != VE.huella_fundamento(e0)


print("expresión de la prueba (h17) con el código del árbol:", expresion())
canon_original = VE._canon


def canon_sin_numeros(x):
    """MUTACIÓN: igual que _canon, pero sin convertir 849697.0 en 849697."""
    if isinstance(x, dict):
        return {str(k): canon_sin_numeros(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [canon_sin_numeros(v) for v in x]
    if isinstance(x, str):
        return re.sub(r"\s+", " ", unicodedata.normalize("NFC", x)).strip()
    return x


VE._canon = canon_sin_numeros
e_int = copy.deepcopy(e0); e_int["fuente"]["valor_fuente"] = int(e_int["fuente"]["valor_fuente"])
print("con la MUTACIÓN (los números ya no se canonizan): expresión de la prueba (h17):", expresion(),
      "| huella(849697.0) == huella(849697):", VE.huella_fundamento(e0) == VE.huella_fundamento(e_int))
VE._canon = canon_original
print("con el código del árbol: huella(valor_fuente 849697.0) == huella(valor_fuente 849697):", VE.huella_fundamento(e0) == VE.huella_fundamento(e_int), "(la propiedad se cumple; la prueba no la ejercita)")

print("\n=== residuo 13 · calcular_entrada")
import fase1_historia as FH  # noqa: E402
PV = fx.PV
ELIS = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_14", "elis_decisiones", "Elis")
CAMBIO = json.load(open(os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_15", "configuracion", "cambio_elis_c48_4_15.json"), encoding="utf-8"))
CALC = CAMBIO["analisis"]["C48"]["calculo"]
f1 = json.load(open(os.path.join(ELIS, "fase1_v63.json"), encoding="utf-8"))
H, anios = f1["historia"]["partidas"], f1["historia"]["anios"]  # como test_entrada_efectiva_415.py
print("firma:", FH.calcular_entrada.__code__.co_varnames[:FH.calcular_entrada.__code__.co_argcount], "| años del cálculo:", CALC.get("anios"), "| componentes:", {k: sorted(v) for k, v in (CALC.get("componentes") or {}).items()})


def probar(rotulo, calc):
    try:
        r = FH.calcular_entrada("C48", {"calculo": calc}, H, anios)
        print(f"[{rotulo}] valor {r.get('valor')!r} · periodo {r.get('periodo')!r} · fuente: {str(r.get('fuente'))[:110]}")
    except Exception as ex:  # noqa: BLE001
        print(f"[{rotulo}] {type(ex).__name__}: {str(ex)[:170]}")


probar("cálculo declarado del CAMBIO 4.15", copy.deepcopy(CALC))
nombre = next(iter(CALC["componentes"]))
a0 = sorted(CALC["componentes"][nombre])[0]
probar("la SERIE del componente no es un objeto", dict(copy.deepcopy(CALC), componentes={nombre: "no es un objeto"}))
probar("la serie del componente es una lista", dict(copy.deepcopy(CALC), componentes={nombre: [1, 2, 3]}))
c2 = copy.deepcopy(CALC); c2["componentes"][nombre][a0] = 5
probar(f"el componente del PRIMER año ({a0}) es un número, no un objeto", c2)
c3 = copy.deepcopy(CALC); c3["componentes"][nombre][a0] = "texto"
probar(f"el componente del primer año ({a0}) es un texto", c3)
c4 = copy.deepcopy(CALC); c4["componentes"][nombre][a0] = [1]
probar(f"el componente del primer año ({a0}) es una lista", c4)
c5 = copy.deepcopy(CALC); c5["componentes"] = "no es un objeto"
probar("«componentes» no es un objeto", c5)
c6 = copy.deepcopy(CALC); c6["anios"] = list(reversed(CALC["anios"]))
probar("años en orden inverso", c6)
c7 = copy.deepcopy(CALC); c7["anios"] = [CALC["anios"][1], CALC["anios"][2], CALC["anios"][0]]
probar("años desordenados", c7)
fx.limpiar()
