"""Cuarta pasada · T1/T2: los «decimales de round» quedan exentos del límite de constantes y la aritmética exacta calcula 10**n con
enteros de precisión arbitraria. Con un número de decimales enorme, `comprobar` (que «nunca lanza») no termina.
Se mide VE._eval_formula_exacta con n creciente y se ejecuta la CLI `comprobar` sobre el registro del arnés con un derivado
round(o["aux:kv"], n), en un proceso hijo con límite de memoria (4 GB) y de tiempo (60 s). No se deja ningún proceso vivo."""
import copy, os, resource, subprocess, sys, time
import fx4 as fx
from fx4 import VE, ent, K, REG

print("árbol:", fx.PV)
vK = fx.inst["celdas"][K]
print("\n=== A · VE._eval_formula_exacta('round(o[\"a\"], n)') y constantes admitidas")
for n in (4, 1000, 100000, 1000000, 3000000, 10000000):
    t = time.time()
    formula = f'round(o["a"], {n})'
    r = VE._eval_formula_exacta(formula, {"a": vK})
    print(f"   n = {n}: {float(r)!r} en {time.time() - t:.2f} s · constantes no admitidas: {VE._constantes_no_admitidas(formula)}")
for f in ('round(o["a"], -3)', 'round(o["a"], -15)', 'round(o["a"], 15)', 'round(o["a"], 999999999999)', 'round(o["a"], 2 + 2)', 'round(o["a"], o["b"])'):
    print(f"   {f}: constantes no admitidas = {VE._constantes_no_admitidas(f)}")

print("\n=== B · CLI `comprobar` con un derivado round(o[\"aux:kv\"], n) en el registro (proceso hijo: 4 GB y 60 s como máximo)")
CITA = f"Partida sintética aux:kv: {round(vK * 1000, 6):.3f}"
PAG = fx.nueva_pagina(CITA)
REG = fx.REG
BASE_F = copy.deepcopy(ent(REG, K)["fuente"])


def limites():
    resource.setrlimit(resource.RLIMIT_AS, (4 * 1024 ** 3, 4 * 1024 ** 3))


for n in (4, 3000000, 999999999999):
    reg = copy.deepcopy(REG)
    reg["entradas"].append({"celda": "aux:kv", "id": "aux:kv", "ambito": "auxiliar", "uso": "origen", "material": True, "clase": "dato_publicado", "valor_modelo": vK,
                            "comprobacion": dict(fx.COMPROBADA), "incidencia": None, "fuente": dict(copy.deepcopy(BASE_F), pagina=PAG, cita=CITA)})
    e = ent(reg, K); e["fuente"] = {}
    e.update(clase="derivado", derivacion={"origenes": ["aux:kv"], "formula": f'round(o["aux:kv"], {n})', "conciliacion": "x", "unidad": "mm"})
    fx.sellar_todo(reg)
    fx.escribir(reg)
    t = time.time()
    try:
        p = subprocess.run([sys.executable, "-B", os.path.join(fx.PV, "scripts", "verificacion_entradas.py"), "comprobar", fx.c], capture_output=True, text=True, timeout=60, preexec_fn=limites)
        print(f"   n = {n}: código {p.returncode} en {time.time() - t:.1f} s · {(p.stdout.strip().splitlines() or ['(sin salida)'])[0][:230]}")
        for l in p.stdout.splitlines()[1:3]:
            print("        " + l[:230])
    except subprocess.TimeoutExpired:
        print(f"   n = {n}: `comprobar` NO TERMINA en 60 s (proceso hijo cortado por el límite de tiempo de la sonda)")
fx.limpiar()
