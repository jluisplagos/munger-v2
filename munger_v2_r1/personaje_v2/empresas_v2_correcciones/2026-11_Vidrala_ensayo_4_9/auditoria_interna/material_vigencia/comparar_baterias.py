# Compara prueba a prueba las salidas JSON de la batería con las de referencia del expediente
import json, sys
E = "/home/claude/vigencia_4_9/munger_v2_r1/personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_9"
T = "/home/claude/vigencia_4_9/tmp/ejecuciones"
def cargar(p):
    d = json.load(open(p, encoding="utf-8"))
    l = d.get("pruebas") if isinstance(d, dict) else d
    return d, [(x["grupo"], x["prueba"], x["pasa"]) if isinstance(x, dict) else tuple(x[:3]) for x in l]
for mio, ref in (("bateria_actual.json", E + "/resultados/test_integridad_auditoria_v2.json"),
                 ("bateria_481.json", E + "/reproduccion/test_integridad_con_codigo_4_8_1.json")):
    dm, a = cargar(T + "/" + mio); dr, b = cargar(ref)
    print(mio, "n =", len(a), "pasan", sum(1 for x in a if x[2] in (True, "PASA")), "| ref n =", len(b), "pasan", sum(1 for x in b if x[2] in (True, "PASA")),
          "| idénticas (grupo, prueba, resultado):", a == b)
    if a != b:
        for x, y in zip(a, b):
            if x != y: print("  DIF", x, "|", y)
    if mio == "bateria_481.json":
        h = [x for x in a if x[0].startswith("H")]
        print("  grupo H con 4.8.1:", len(h), "pruebas;", sum(1 for x in h if x[2] in (True, "PASA")), "pasan")
        for x in h: print("   ", x[2], x[1][:150])
