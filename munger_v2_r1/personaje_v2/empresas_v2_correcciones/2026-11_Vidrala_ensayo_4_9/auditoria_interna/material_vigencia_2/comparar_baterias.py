import json, sys
a = json.load(open(sys.argv[1], encoding="utf-8")); b = json.load(open(sys.argv[2], encoding="utf-8"))
pa = [(p["grupo"], p["prueba"], p["pasa"]) for p in a["pruebas"]]
pb = [(p["grupo"], p["prueba"], p["pasa"]) for p in b["pruebas"]]
print("n", len(pa), len(pb), "pasan", sum(x[2] for x in pa), sum(x[2] for x in pb))
print("iguales prueba a prueba (grupo, nombre, resultado):", pa == pb)
for x, y in zip(pa, pb):
    if x != y: print("DIF", x, y)
# detalles
da = [p["detalle"] for p in a["pruebas"]]; db = [p["detalle"] for p in b["pruebas"]]
print("detalles distintos:", sum(1 for x, y in zip(da, db) if x != y))
