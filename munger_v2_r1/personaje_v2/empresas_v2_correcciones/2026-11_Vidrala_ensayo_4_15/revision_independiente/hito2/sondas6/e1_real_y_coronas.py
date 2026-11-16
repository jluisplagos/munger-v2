#!/usr/bin/env python3
"""e1 · sexta comprobación · V1 y V7 (unidades): la familia «corona» y los códigos DKK/SEK/NOK en _moneda_de, y «real» en MARCAS_MONEDA.
A) familia de la corona, par a par, frente a una tabla del revisor (independiente de _moneda_de);
B) «real» con OTRO sentido en el texto de una unidad («% real», «tipo real», «valor real», «real estate»…): 876bfc2 → 8196522;
C) unidades que estaban pendientes con 876bfc2 y dejan de estarlo con 8196522 (monotonía): ¿cuáles son?;
D) unidades REALES: todas las «unidad» de los registros verificacion_entradas.json del árbol y de los demás JSON de los expedientes:
   ¿alguna dice «real»?, ¿alguna cambia de estado entre los dos códigos?
Uso: python3 -I -B e1_real_y_coronas.py"""
import collections, glob, itertools, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun6 import VE, VP, VQ, ACT, ANT, PV  # noqa: E402
f = lambda M, u: M._unidad_monetaria_no_reconocida(u)  # noqa: E731
est = lambda x: "PENDIENTE" if x else "no pendiente"  # noqa: E731
print(f"VE = {ACT} · VP = {ANT} · VQ = 876bfc2 con las propuestas de la 5.ª")

print("\n== A · familia de la corona (tabla del revisor: un NOMBRE con cualquier forma de corona es la misma moneda; dos CÓDIGOS distintos, un tipo de cambio)")
COR = ["corona", "coronas", "dkk", "sek", "nok"]
COD = {"dkk", "sek", "nok"}
mal = []
c = collections.Counter()
for a, b in itertools.product(COR, repeat=2):
    cambio = a in COD and b in COD and a != b  # tabla del revisor
    for sep in ("/", " / ", " por ", " per "):
        for env in ("{}", "({})", "tipo de cambio {}", "tipo de cambio: {}", "exchange rate {}", " {} "):
            for may in (str, str.upper, str.capitalize):
                u = env.format(may(a) + sep + may(b))
                e = f(VE, u)
                c[("tipo de cambio" if cambio else "misma moneda", est(f(VP, u)), est(e))] += 1
                if e == cambio:
                    mal.append(u)
for k, v in sorted(c.items()):
    print(f"   {k[0]:15} · 876bfc2 {k[1]:13} → 8196522 {k[2]:13}: {v}")
print(f"   unidades en las que 8196522 no coincide con la tabla del revisor: {len(mal)} {mal[:6]}")
print("   casos sueltos:")
for u in ("coronas/DKK", "DKK/coronas", "corona/coronas", "coronas/coronas", "DKK/DKK", "SEK/SEK", "DKK/SEK", "SEK/NOK", "NOK/DKK", "coronas/SEK", "corona/NOK",
          "coronas danesas/DKK", "coronas suecas por corona danesa", "DKK por corona sueca", "coronas/euros", "EUR/DKK", "DKK/EUR", "coronas por euro", "miles de coronas", "millones de DKK",
          "DKK", "coronas", "DKK por acción", "DKK/SEK (miles)", "tipo de cambio DKK/SEK medio", "CZK/DKK", "corona checa/EUR", "ISK/EUR"):
    print(f"      {u!r:36} 876bfc2 {est(f(VP, u)):13} 8196522 {est(f(VE, u)):13} propuesta 5.ª {est(f(VQ, u))}")

print("\n== B · «real» con otro sentido en la unidad (ninguna es un importe en reales brasileños)")
OTRO = ["% real", "% (real)", "tipo real", "tipo de interés real", "tipo de interés real (%)", "valor real", "crecimiento real", "crecimiento real (%)", "PIB real", "tasa real",
        "variación real", "variación real %", "rentabilidad real", "en términos reales", "% en términos reales", "real terms", "real growth (%)", "real estate", "m² (real estate)",
        "tiempo real", "número real", "dato real", "cifra real", "unidades reales", "plantilla real", "horas reales", "real/nominal", "nominal/real", "veces (real)",
        "Real Decreto", "tipo de cambio real", "tipo de cambio real EUR/USD", "tipo de cambio efectivo real", "índice (base real)", "realizado", "realidad", "irreal", "real_2024", "real-2024",
        "años", "%", "veces", "acciones", "texto", "ratio", "puntos básicos", "x", "días", "toneladas"]
nuevos = []
for u in OTRO:
    a, b = f(VP, u), f(VE, u)
    if b and not a:
        nuevos.append(u)
    print(f"      {u!r:34} 876bfc2 {est(a):13} 8196522 {est(b):13}" + ("   <<< pendiente NUEVO (falso positivo de «real»)" if b and not a else "   (ya era pendiente: «reales»)" if a and b else ""))
print(f"   unidades con «real» en otro sentido que pasan a pendiente con 8196522: {len(nuevos)} de {len(OTRO)}")
print("   MARCAS_MONEDA: ", {w: bool(VE.MARCAS_MONEDA.search(w)) for w in ("real", "reales", "reale", "Real", "REAL", "realizado", "irreal", "real_2024", "real-2024", "real.", "(real)")})

print("\n== C · monotonía: unidades pendientes con 876bfc2 que DEJAN de estarlo con 8196522")
FORMAS = ["€", "eur", "euro", "euros", "$", "usd", "dólar", "dolar", "£", "gbp", "libra", "libras", "¥", "jpy", "chf", "franco", "francos", "dkk", "sek", "nok", "corona", "coronas", "brl", "real", "reales",
          "mm€", "meur", "keur", "k€"]
OTRAS = ["valor", "tipo", "nominal", "%", "acción", "miles", "millones", "año", "veces", "tipo de cambio", "exchange rate", "medio", "(cierre)", "constante", "bn", "mm", "por", "per", "/"]
dejan = collections.Counter()
ej = collections.defaultdict(list)
n = 0
import random
rnd = random.Random(6)
unidades = set()
for a, b in itertools.product(FORMAS, repeat=2):
    for sep in ("/", " / ", " por ", " per ", " ", " y ", "-"):
        for pre in ("", "tipo de cambio ", "exchange rate ", "miles de ", "millones de ", "importe en ", "valor "):
            for cal in ("", " medio", " (cierre)", " constante", " miles", " millones", " %", " por acción"):
                unidades.add(pre + a + sep + b + cal)
for _ in range(60000):
    unidades.add(" ".join(rnd.choice(FORMAS + OTRAS) for _i in range(rnd.randint(1, 5))))
for a in FORMAS + OTRAS:
    unidades.add(a)
for u in sorted(unidades):
    n += 1
    a, b = f(VP, u), f(VE, u)
    if a and not b:
        m = re.fullmatch(r"(?:(?:tipo de cambio|exchange rate)\b)?[\s:(]*(\S+?)\s*(?:por|per|/)\s*(\S+?)[\s)]*", u, re.I)
        clase = ("par simple «real ⟷ otra moneda» (ahora, tipo de cambio BRL)" if m and ("real" in (m.group(1).lower(), m.group(2).lower())) and m.group(1).lower() != m.group(2).lower() else "OTRA")
        dejan[clase] += 1
        if len(ej[clase]) < 8:
            ej[clase].append(u)
    c[("C", est(a), est(b))] += 1
print(f"   {n} unidades (pares con prefijos y calificativos, y combinaciones aleatorias de marcas y palabras): " + str({f"{k[1]} → {k[2]}": v for k, v in sorted(c.items()) if k[0] == "C"}))
for k, v in sorted(dejan.items()):
    print(f"   dejan de estar pendientes · {k}: {v}   ej.: {ej[k]}")
print(f"   de otra clase: {dejan.get('OTRA', 0)}")

print("\n== D · unidades reales del árbol")
E = os.path.join(PV, "empresas_v2_correcciones")
regs = sorted(glob.glob(os.path.join(E, "**", "verificacion_entradas.json"), recursive=True) + glob.glob(os.path.join(PV, "empresas_v2", "**", "verificacion_entradas.json"), recursive=True))
us = collections.Counter()
for p in regs:
    try:
        reg = json.load(open(p, encoding="utf-8"))
    except Exception as ex:  # noqa: BLE001
        print("   ilegible:", p, ex)
        continue
    for e in reg.get("entradas") or []:
        fu = e.get("fuente") if isinstance(e.get("fuente"), dict) else {}
        if "unidad" in fu:
            us[str(fu.get("unidad"))] += 1
        for d in (e.get("derivado") or {}).get("origenes") or [] if isinstance(e.get("derivado"), dict) else []:
            if isinstance(d, dict) and "unidad" in d:
                us["(origen) " + str(d.get("unidad"))] += 1
print(f"   {len(regs)} registros verificacion_entradas.json en el árbol (fuera de carpetas temporales); {sum(us.values())} unidades, {len(us)} distintas")
cambian = [(u, f(VP, u.replace('(origen) ', '')), f(VE, u.replace('(origen) ', ''))) for u in us if f(VP, u.replace('(origen) ', '')) != f(VE, u.replace('(origen) ', ''))]
con_real = [u for u in us if re.search(r"\breal(?:es)?\b", u, re.I)]
con_apos = [u for u in us if "'" in u or "’" in u]
print(f"   unidades reales cuyo estado U7 cambia entre 876bfc2 y 8196522: {len(cambian)} {cambian[:5]}")
print(f"   unidades reales que contienen la palabra «real(es)»: {len(con_real)} {con_real[:5]}")
print(f"   unidades reales pendientes por U7 con 8196522: {sorted(u for u in us if f(VE, u.replace('(origen) ', '')))}")
print("   todas las unidades reales distintas:", sorted(us.items(), key=lambda kv: -kv[1]))
# cualquier clave «unidad» de cualquier JSON de los expedientes (fichas, entradas, registros de otras versiones)
cu = collections.Counter()
nj = 0
for raiz in (E, os.path.join(PV, "empresas_v2")):
    for p in glob.glob(os.path.join(raiz, "**", "*.json"), recursive=True):
        try:
            if os.path.getsize(p) > 30_000_000:
                continue
            t = open(p, encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        nj += 1
        for m in re.finditer(r'"unidad[a-z_]*"\s*:\s*"((?:[^"\\]|\\.)*)"', t):
            cu[m.group(1)] += 1
real_j = {u: v for u, v in cu.items() if re.search(r"\breal(?:es)?\b", u, re.I)}
camb_j = {u: v for u, v in cu.items() if f(VP, u) != f(VE, u)}
print(f"   {nj} JSON de los expedientes: {sum(cu.values())} valores de claves «unidad…», {len(cu)} distintos; con la palabra «real(es)»: {real_j}; que cambian de estado U7: {camb_j}")
