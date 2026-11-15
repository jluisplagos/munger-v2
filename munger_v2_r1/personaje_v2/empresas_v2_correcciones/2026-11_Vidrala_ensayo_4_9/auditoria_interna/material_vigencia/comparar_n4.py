# Compara la reproducción de n4_investigacion.py en tmp con n4/ y propuestas/ del expediente
import json, sys, hashlib
E = "/home/claude/vigencia_4_9/munger_v2_r1/personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_9"
T = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/vigencia_4_9/tmp/ejecuciones/n4"
h = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
for a, b in ((T + "/matriz_n4.csv", E + "/n4/matriz_n4.csv"), (T + "/recuento_n4.json", E + "/n4/recuento_n4.json"),
             (T + "/prop/propuestas_n4_sin_firmar.json", E + "/propuestas/propuestas_n4_sin_firmar.json"), (T + "/matriz_n4.json", E + "/n4/matriz_n4.json")):
    print(b.split("/")[-1], "bytes idénticos:", h(a) == h(b))
m, r = json.load(open(T + "/matriz_n4.json")), json.load(open(E + "/n4/matriz_n4.json"))
print("campo efectos:", m.get("efectos"), "|", r.get("efectos"))
dif = [k for k in set(m) | set(r) if m.get(k) != r.get(k)]
print("claves de primer nivel distintas:", dif)
def difs(x, y, ruta=""):
    if isinstance(x, dict) and isinstance(y, dict):
        for k in set(x) | set(y):
            yield from difs(x.get(k), y.get(k), ruta + "." + str(k))
    elif isinstance(x, list) and isinstance(y, list) and len(x) == len(y):
        for i, (a, b) in enumerate(zip(x, y)):
            yield from difs(a, b, ruta + f"[{i}]")
    elif x != y:
        yield ruta, str(x)[:80], str(y)[:80]
d = list(difs(m["matriz"], r["matriz"]))
print("diferencias dentro de la matriz:", len(d)); [print("  ", x) for x in d[:10]]
print("cobertura:", r["cobertura"])
