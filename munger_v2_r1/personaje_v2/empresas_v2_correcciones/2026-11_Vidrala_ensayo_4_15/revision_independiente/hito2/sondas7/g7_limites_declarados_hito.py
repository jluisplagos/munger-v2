#!/usr/bin/env python3
"""g7 · séptima comprobación · lo que declara `HITO_2_4_15.md` §5 («Límites declarados») frente al código de la candidata, a nivel de unidad.
Para cada forma se da lo que el registro dice que pasa y lo que pasa: «pendiente» = signo_indeterminado o no_localizada; «discrepancia» =
ausente o signo_distinto; «aceptada» = ok. Se marca lo que no coincide. También los límites que las revisiones anotaron y el registro no nombra.
Uso: python3 -I -B g7_limites_declarados_hito.py"""
import json, os, re, shutil, sys, tempfile, types
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun7 import VE, VP, VQ, F, PV, ACT, ANT, PROP  # noqa: E402
print(f"VE = {ACT} · VP = {ANT} · VQ = {PROP}")
CLASE = {"ok": "aceptada", "signo_indeterminado": "pendiente", "no_localizada": "pendiente", "ausente": "discrepancia", "signo_distinto": "discrepancia"}
n_mal = 0


def caso(nombre, pag, cita, vf, declarado):
    global n_mal
    a, b, q = VP._cita_cifra(cita, vf, pag)[0], VE._cita_cifra(cita, vf, pag)[0], VQ._cita_cifra(cita, vf, pag)[0]
    marca = ""
    if declarado and CLASE[b] != declarado:
        n_mal += 1
        marca = f"   <<< el registro dice «{declarado}»"
    print(f"   {nombre:78} 8196522: {a:20} 45ff57c: {b:20} ({CLASE[b]}) propuesta: {q:20}{marca}")


print("\n== A · «quedan pendientes por prudencia formas legítimas como …» (HITO §5, Signo): cada forma con el valor que publica")
caso("«(149.5m)» con −149,5", "Resultado (149.5m)\n", "Resultado (149.5m)", -149.5, "pendiente")
caso("«(-x)»: «(-149,5)» con −149,5", "Resultado (-149,5)\n", "Resultado (-149,5)", -149.5, "pendiente")
caso("«31-dic-2024» con 2024", "Cierre 31-dic-2024\n", "Cierre 31-dic-2024", 2024, "pendiente")
caso("«2024-25» con 25", "Ejercicio 2024-25\n", "Ejercicio 2024-25", 25, "pendiente")
caso("«12-2024» con 2024", "Periodo 12-2024\n", "Periodo 12-2024", 2024, "pendiente")
caso("«7-7,5 %» con 7,5", "Rango 7-7,5 %\n", "Rango 7-7,5 %", 7.5, "pendiente")
caso("«2-3 %» con 3", "Rango 2-3 %\n", "Rango 2-3 %", 3, "pendiente")
caso("«100-150» con 150", "Entre 100-150 millones\n", "Entre 100-150 millones", 150, "pendiente")
caso("años decrecientes «2024-2023» con 2023", "Variación 2024-2023\n", "Variación 2024-2023", 2023, "pendiente")
caso("el día de una fecha ISO «2024-12-31» con 31", "Cierre 2024-12-31\n", "Cierre 2024-12-31", 31, "pendiente")
caso("«31-12-24» con 24", "Cierre 31-12-24\n", "Cierre 31-12-24", 24, "pendiente")
caso("un intervalo partido por un salto de línea: «Plan 2023⏎–2026» con +2026 (cita de las dos líneas)", "Plan 2023\n–2026\n", "Plan 2023 –2026", 2026, "pendiente")
caso("   … lo mismo citando solo «–2026»", "Plan 2023\n–2026\n", "–2026", 2026, "pendiente")
caso("«Q1'24» con 24 (cita completa)", "Ventas Q1'24 crecen\n", "Ventas Q1'24 crecen", 24, "pendiente")
caso("   … «Q1'24» citando desde la cifra «24 crecen»", "Ventas Q1'24 crecen\n", "24 crecen", 24, "pendiente")
caso("«. . . .130,8» citada desde la cifra «130,8»", "Total . . . .130,8\n", "130,8", 130.8, "pendiente")
caso("   … «. . . .130,8» con la cita completa", "Total . . . .130,8\n", "Total . . . .130,8", 130.8, "pendiente")
caso("«ejercicio .849,7» citada «849,7 millones»", "al cierre del ejercicio .849,7 millones\n", "849,7 millones", 849.7, "pendiente")
caso("   … «ejercicio .849,7» con la cita completa", "al cierre del ejercicio .849,7 millones\n", "al cierre del ejercicio .849,7 millones", 849.7, "pendiente")

print("\n== B · otros límites declarados del signo")
caso("H3: un guion separado por varios espacios, «Total -   849,7» con +849,7 («se lee como otra columna»)", "Total -   849,7\n", "Total -   849,7", 849.7, "aceptada")
caso("un carácter invisible entre el signo y la cifra «-<U+200B>849,7» con +849,7 («la hace leer en positivo»)", "Resultado -​849,7\n", "Resultado -​849,7", 849.7, "aceptada")
caso("el signo escrito con palabras «menos 149,5» con +149,5 («no se reconoce»)", "Resultado menos 149,5\n", "Resultado menos 149,5", 149.5, "aceptada")
caso("«$» en en_numero «da una discrepancia prudente tras una línea que acaba en cifra» (Q6, V7)", "Ventas 2023\n849,7 millones\n", "849,7 mill", 849.7, "discrepancia")

print("\n== C · U7 («real» con otro sentido deja la unidad pendiente; «dólares por euro» también) y U6/T6 (claves parecidas: error)")
for u in ("% real", "valor real", "real estate", "dólares por euro", "miles de euros", "%", "EUR/USD", "USD por EUR"):
    print(f"   unidad {u!r:22} _unidad_monetaria_no_reconocida = {VE._unidad_monetaria_no_reconocida(u)}")
SRC_PL = open(os.path.join(PV, "scripts", "pipeline.py"), encoding="utf-8").read()
PL = types.ModuleType("pl_g7"); PL.__file__ = os.path.join(PV, "scripts", "pipeline.py")
ruta = list(sys.path); exec(compile(SRC_PL, "pipeline.py", "exec"), PL.__dict__); sys.path[:] = ruta
tmp = tempfile.mkdtemp(prefix="g7_", dir=os.path.join(F, "tmp"))
try:
    for clave in ("entrega_efectiva", "entrada_de_efectivo", "tasa_efectiva", "entrada_efectiva"):
        json.dump({"tipo": "x", clave: "estricta"}, open(os.path.join(tmp, "alcance_v2.json"), "w"))
        try:
            r = "sin error: " + repr(PL.modo_entrada_efectiva(tmp))
        except (SystemExit, Exception) as ex:  # noqa: BLE001
            r = "ERROR (" + type(ex).__name__ + "): " + str(ex)[:110]
        print(f"   clave «{clave}»: {r}")
finally:
    shutil.rmtree(tmp, ignore_errors=True)

print("\n== D · límites que las revisiones anotaron y que `HITO_2_4_15.md` §5 NO nombra (todos en el sentido de aceptar)")
caso("5.ª y 6.ª (V6): un importe que parece un año, «Saldo 2023-2049» (publica −2049) con +2049", "Saldo 2023-2049\n", "Saldo 2023-2049", 2049, None)
caso("5.ª y 6.ª (V6): la regla de la fecha solo mira la forma, «Notas 5-6-1849» con +1849", "Notas 5-6-1849\n", "Notas 5-6-1849", 1849, None)
caso("6.ª (§2): moneda entre el guion y el salto de línea, «Saldo 2023-€⏎2024» con +2024", "Saldo 2023-€\n2024\n", "Saldo 2023-€ 2024", 2024, None)
caso("miles con espacio «1 849,7» citada «849,7» (declarado en el docstring de _cita_contiene)", "Total 1 849,7\n", "849,7", 849.7, None)
for nom, ap in (("U+02BC ʼ", "ʼ"), ("U+2032 ′", "′"), ("U+00B4 ´", "´"), ("U+0060 `", "`"), ("U+2018 ‘", "‘"), ("U+201B ‛", "‛"), ("U+FF07 ＇", "＇")):
    caso(f"6.ª (W3): signo parecido al apóstrofo {nom}: «1{ap}849,7» citada «849,7»", f"Total 1{ap}849,7\n", "849,7", 849.7, None)
print(f"\n   formas en las que lo declarado no coincide con lo que hace la candidata: {n_mal}")
