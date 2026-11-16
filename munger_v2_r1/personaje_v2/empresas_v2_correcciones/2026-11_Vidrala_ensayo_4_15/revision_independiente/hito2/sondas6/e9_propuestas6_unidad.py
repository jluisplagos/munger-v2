#!/usr/bin/env python3
"""e9 · sexta comprobación · las propuestas del revisor (propuestas6.py; NO es código entregado), a nivel de unidad.
A) prop6t (solo pruebas): el bloque de pruebas nuevas CON los casos propuestos, ejecutado contra la candidata (tiene que pasar entero),
   contra 876bfc2 y contra cada mutación de mutantes6.py: ¿cuáles detecta ahora?
B) prop6 (código): los casos del apóstrofo tipográfico (W3), de los límites de la cita (W4) y del mensaje (W5), candidata → propuesta;
C) prop6 frente a la candidata en un diferencial aleatorio: toda diferencia debe estar en una página con un apóstrofo (ASCII o «’») pegado
   a cifras o ser solo del mensaje del máximo; y en las citas REALES (1.645): ningún cambio.
Uso: python3 -I -B e9_propuestas6_unidad.py"""
import collections, os, random, re, sys, time, types
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun6 import VE, VP, F, PV, ACT, ANT, cargar  # noqa: E402
import mutantes6 as MU  # noqa: E402
V6 = cargar(os.path.join(F, "prop6", "munger_v2_r1", "personaje_v2", "scripts", "verificacion_entradas.py"), "verificacion_entradas_prop6")
assert "propuesta del revisor, W3" in open(V6.__file__, encoding="utf-8").read()
print(f"VE = {ACT} · VP = {ANT} · V6 = 8196522 con las propuestas W3, W4 y W5 del revisor")

print("\n== A · el bloque de pruebas nuevas con los casos propuestos (prop6t)")
T = open(os.path.join(F, "prop6t", "munger_v2_r1", "personaje_v2", "pruebas", "test_verificacion_entradas_415.py"), encoding="utf-8").read()
ini = T.index("# (hito 2, quinta comprobación, V1–V7 y pruebas de V4)")
fin = T.index("r = con()\npaso(\"RW\", \"el control positivo sigue apto después de los casos RW\"", ini)
BLOQUE = T[ini:fin]
SRC_VE = open(VE.__file__, encoding="utf-8").read()


def bloque(mod):
    res = []
    exec(compile(BLOQUE, "bloque_propuesto", "exec"), {"VE": mod, "paso": lambda b, n, ok, det=None: res.append((n, bool(ok), det)), "_time": time})
    return res


def mutante(nombre):
    s = SRC_VE
    for _a, viejo, nuevo in MU.M[nombre][3]:
        assert s.count(viejo) == 1, nombre
        s = s.replace(viejo, nuevo)
    m = types.ModuleType("mut_" + nombre)
    m.__file__ = VE.__file__
    ruta = list(sys.path)
    exec(compile(s, nombre + ".py", "exec"), m.__dict__)
    sys.path[:] = ruta
    return m


r = bloque(VE)
print(f"   candidata: {sum(ok for _n, ok, _d in r)} de {len(r)} pruebas del bloque PASAN" + "".join(f"\n      FALLA: {n[:90]} · {d}" for n, ok, d in r if not ok))
r = bloque(VP)
print(f"   876bfc2 (sin ninguna corrección): fallan {[n[:8] for n, ok, _d in r if not ok]}")
r = bloque(V6)
print(f"   propuesta de código (prop6): {sum(ok for _n, ok, _d in r)} de {len(r)} PASAN" + "".join(f"\n      FALLA: {n[:90]} · {d}" for n, ok, d in r if not ok))
for nombre, v in MU.M.items():
    if v[0] == "control" or any(a != MU.VEP for a, _x, _y in v[3]):
        continue
    r = bloque(mutante(nombre))
    fallan = [(n, d) for n, ok, d in r if not ok]
    print(f"   {nombre:34} {'DETECTADA' if fallan else '<<< NO detectada'}" + (f" por {[n[:8] for n, _d in fallan]} · {str(fallan[0][1])[:120]}" if fallan else ""))

print("\n== B · propuesta de código (W3, W4, W5): candidata → propuesta")
for nombre, pag, cita, vf in (("W3 «1’849,7» citada «849,7»", "Total 1’849,7\n", "849,7", 849.7), ("W3 «849’697» citada «Total 849»", "Total 849’697\n", "Total 849", 849),
                              ("W3 la cifra entera «1’849.7» = 1849,7 (sigue sin reconocerse: _cifras no genera «’»)", "Total 1’849.7\n", "Total 1’849.7", 1849.7),
                              ("V7 «1'849,7» citada «849,7»", "Total 1'849,7\n", "849,7", 849.7), ("V7 «849'697» citada «Total 849»", "Total 849'697\n", "Total 849", 849),
                              ("control «1'849.7» = 1849,7", "Total 1'849.7\n", "Total 1'849.7", 1849.7), ("control «849'697» = 849697", "Total 849'697\n", "Total 849'697", 849697),
                              ("W4 la cifra sola, que está además dentro de «1'849,7»", "Total 1'849,7\nOtros 849,7\n", "849,7", 849.7),
                              ("W4 «Total 849», que está además en «Total 849'697»", "Total 849'697\nTotal 849\n", "Total 849", 849),
                              ("W4 la cifra sola en positivo dos veces y dentro de «9'774» (valor −9)", "9'774\n 9 320\n", "9", -9),
                              ("W4 negativa de verdad y dentro de «1'849,7» (valor +849,7)", "Total 1'849,7\nOtros -849,7\n", "849,7", 849.7),
                              ("doble corte «1'849,7 millones» citada «849,7 mill»", "Total 1'849,7 millones\n", "849,7 mill", 849.7),
                              ("«Q1'24» con valor 24", "Ventas Q1'24 crecen\n", "Ventas Q1'24 crecen", 24), ("posesivo «SBF 120’s» con valor 120 (forma real de los textos de Elis)", "the SBF 120’s circular economy\n", "the SBF 120’s circular", 120),
                              ("«l’exercice 2023» con valor 2023", "l’exercice 2023\n", "l’exercice 2023", 2023), ("W5 mensaje con 400 apariciones", " ".join(["Total: 5.5"] * 400), "Total: 5.5", 5.5)):
    a, b = VE._cita_cifra(cita, vf, pag), V6._cita_cifra(cita, vf, pag)
    print(f"   {nombre:88} candidata: {a[0]:20} propuesta: {b[0]:20}" + (f" «{b[1][:60]}»" if "W5" in nombre else ""))

print("\n== C · propuesta de código frente a la candidata")
rnd = random.Random(96)
GUI = "-–−"


def numero(vals):
    r = rnd.random()
    if r < 0.3:
        a = rnd.randint(0, 2100)
        vals.append(a)
        return str(a)
    if r < 0.5:
        a, d = rnd.randint(0, 999), rnd.randint(0, 9)
        vals.extend([a + d / 10, a, d])
        return f"{a}{rnd.choice(',.')}{d}"
    m, c, d = rnd.randint(1, 9), rnd.randint(100, 999), rnd.randint(0, 9)
    sep = rnd.choice(["'", "'", "’", "’", ".", ",", " "])
    dec = rnd.choice(["", ",", "."])
    if dec == sep:
        dec = ""
    vals.extend([m * 1000 + c + (d / 10 if dec else 0), c + (d / 10 if dec else 0), c, m])
    return f"{m}{sep}{c}" + (f"{dec}{d}" if dec else "")


tr = collections.Counter()
ej = {}
sin = 0
for _ in range(120000):
    vals = []
    pag = "".join(numero(vals) if rnd.random() < 0.45 else rnd.choice([" ", " ", "  ", "\n", "Total ", "Saldo", "(", ")", "-", "–", "€", "%", ".", "'", "’", "Q1'", "l’", "120’s "]) for _i in range(rnd.randint(3, 10)))
    if not vals or not pag.strip():
        continue
    i = rnd.randrange(len(pag)); j = rnd.randint(i + 1, len(pag))
    if rnd.random() < 0.5:
        ps = [0] + [m.start() for m in re.finditer(r"(?<=\s)\S", pag)]; fs = [m.end() for m in re.finditer(r"\S(?=\s|$)", pag)]
        i = rnd.choice(ps); fs = [f for f in fs if f > i]; j = rnd.choice(fs) if fs else len(pag)
    cita = pag[i:j]
    if not cita.strip():
        continue
    vf = rnd.choice(vals) * rnd.choice([1, 1, -1])
    a, b = VE._cita_cifra(cita, vf, pag)[0], V6._cita_cifra(cita, vf, pag)[0]
    if a != b:
        tr[(a, b)] += 1
        ej.setdefault((a, b), (pag, cita, vf))
        if not re.search(r"\d['’]\d", pag):
            sin += 1
    else:
        tr["igual"] += 1
for k, v in sorted(tr.items(), key=lambda kv: -kv[1] if kv[0] != "igual" else 1):
    print(f"   {'igual' if k == 'igual' else k[0] + ' → ' + k[1]:44} {v:6}" + ("" if k == "igual" else f"   ej.: {ej[k]!r}"))
print(f"   diferencias en páginas SIN un apóstrofo (ASCII o «’») entre cifras: {sin}")
E14 = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_14")
c = collections.Counter()
for exp in ["vidrala_decisiones_INVALIDO_perdio_analisis/Vidrala", "elis_decisiones/Elis", "viscofan/Viscofan", "elis_motor_A/Elis", "vidrala_decisiones/Vidrala", "vidrala/Vidrala", "viscofan_decisiones/Viscofan"]:
    carpeta = os.path.join(E14, exp)
    reg, err = VE.cargar(carpeta)
    for e in reg["entradas"]:
        f = e.get("fuente") if isinstance(e.get("fuente"), dict) else {}
        if not VE._num(f.get("valor_fuente")) or not str(f.get("archivo") or "").lower().endswith(".txt"):
            continue
        ruta = VE._ruta_fuente(carpeta, f["archivo"])
        est, pag = VE._pagina_examinable(ruta, f.get("pagina")) if ruta else ("", None)
        if est != "ok":
            continue
        a, b = VE._cita_cifra(f.get("cita"), f["valor_fuente"], pag), V6._cita_cifra(f.get("cita"), f["valor_fuente"], pag)
        c["igual" if a == b else f"CAMBIA {a[0]} → {b[0]}"] += 1
print(f"   citas reales (estado y detalle) candidata → propuesta: {dict(c)}")
