#!/usr/bin/env python3
"""g9 · séptima comprobación · (sustituye a e9 B y C de la sexta, con el mismo generador y la misma semilla)
A) los casos de e9 B (W3, W4, W5 y vecinos): 8196522 → 45ff57c, y frente a lo que proponía la sexta (prop6);
B) diferencial aleatorio de _cita_cifra (120.000 intentos, semilla 96, el generador de e9 C):
   B1) 45ff57c frente a la PROPUESTA de la sexta: si el autor la hubiera aplicado tal cual no habría ninguna diferencia;
   B2) 45ff57c frente a 8196522: ¿qué deja de aceptarse y qué pasa a aceptarse?
   cada diferencia se clasifica por el rasgo de la página (apóstrofo ASCII entre cifras, tipográfico entre cifras, ninguno);
C) las citas REALES con fuente de texto (estado y detalle) con los tres códigos y con la corrección propuesta (fix7).
Uso: python3 -I -B g9_diferencial_y_citas_reales.py"""
import collections, os, random, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun7 import VE, VP, VQ, F, PV, ACT, ANT, PROP, cargar  # noqa: E402
VF7 = cargar(os.path.join(F, "fix7", "munger_v2_r1", "personaje_v2", "scripts", "verificacion_entradas.py"), "verificacion_entradas_fix7") if os.path.isdir(os.path.join(F, "fix7")) else None
print(f"VE = {ACT} · VP = {ANT} · VQ = {PROP} · VF7 = 45ff57c con la corrección de :542 que propone el revisor" + ("" if VF7 else " (NO construido)"))

print("\n== A · casos de e9 B")
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
    a, b, q = VP._cita_cifra(cita, vf, pag), VE._cita_cifra(cita, vf, pag), VQ._cita_cifra(cita, vf, pag)
    print(f"   {nombre:88} 8196522: {a[0]:20} 45ff57c: {b[0]:20} propuesta: {q[0]:20}" + ("  <<< 45ff57c ≠ propuesta" if b[0] != q[0] else "") + (f" «{b[1][:60]}»" if "W5" in nombre else ""))

print("\n== B · diferencial aleatorio")
rnd = random.Random(96)


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


def rasgo(pag):
    a, t = re.search(r"\d'\d", pag) is not None, re.search(r"\d’\d", pag) is not None
    return "apóstrofo ASCII y tipográfico entre cifras" if a and t else "apóstrofo ASCII entre cifras" if a else "apóstrofo tipográfico entre cifras" if t else "SIN apóstrofo entre cifras"


comp = {"B1 · 45ff57c frente a la propuesta de la 6.ª": VQ, "B2 · 45ff57c frente a 8196522": VP}
if VF7:
    comp["B3 · la corrección propuesta (fix7) frente a la propuesta de la 6.ª"] = VQ
tr = {k: collections.Counter() for k in comp}
ej = {k: {} for k in comp}
n = 0
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
    n += 1
    b = VE._cita_cifra(cita, vf, pag)[0]
    est = {id(VQ): VQ._cita_cifra(cita, vf, pag)[0], id(VP): VP._cita_cifra(cita, vf, pag)[0]}
    for k, mod in comp.items():
        x = VF7._cita_cifra(cita, vf, pag)[0] if k.startswith("B3") else b
        o = est[id(mod)]
        if x != o:
            clave = (o, x, rasgo(pag))
            tr[k][clave] += 1
            ej[k].setdefault(clave, (pag, cita, vf))
        else:
            tr[k]["igual"] += 1
print(f"   {n} citas aleatorias")
for k in comp:
    otro = "propuesta" if "propuesta" in k.split("frente a")[1] else "8196522"
    este = "fix7" if k.startswith("B3") else "45ff57c"
    print(f"   -- {k}: iguales {tr[k]['igual']}, distintas {sum(v for kk, v in tr[k].items() if kk != 'igual')}")
    for kk, v in sorted(((kk, v) for kk, v in tr[k].items() if kk != "igual"), key=lambda kv: -kv[1]):
        sentido = "ACEPTA lo que el otro no" if kk[1] == "ok" else "deja de aceptar" if kk[0] == "ok" else "entre discrepancia y pendiente"
        print(f"      {otro} {kk[0]:20} → {este} {kk[1]:20} {v:6}  [{kk[2]}] ({sentido})   ej.: {ej[k][kk]!r}")
    acepta = sum(v for kk, v in tr[k].items() if kk != "igual" and kk[1] == "ok")
    sin = sum(v for kk, v in tr[k].items() if kk != "igual" and kk[2].startswith("SIN"))
    print(f"      → {este} da «ok» donde {otro} no: {acepta} · diferencias en páginas SIN apóstrofo entre cifras: {sin}")

print("\n== C · citas reales con fuente de texto")
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
            c["página no examinable"] += 1
            continue
        b = VE._cita_cifra(f.get("cita"), f["valor_fuente"], pag)
        c[f"45ff57c: {b[0]}"] += 1
        for nombre, mod in (("8196522", VP), ("propuesta 6.ª", VQ)) + ((("fix7", VF7),) if VF7 else ()):
            o = mod._cita_cifra(f.get("cita"), f["valor_fuente"], pag)
            c[f"{nombre}: " + ("igual (estado y detalle)" if o == b else f"CAMBIA {o[0]} → {b[0]}")] += 1
print(f"   {dict(c)}")
