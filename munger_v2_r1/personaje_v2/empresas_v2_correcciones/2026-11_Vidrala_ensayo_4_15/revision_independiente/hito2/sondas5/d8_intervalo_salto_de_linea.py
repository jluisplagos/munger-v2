#!/usr/bin/env python3
"""d8 · Q3 (quinta comprobación): el intervalo de años y la fecha A TRAVÉS DE UN SALTO DE LÍNEA. En _signo_en_cita, las expresiones del
año anterior y de la fecha acaban en «$», que en Python casa también ANTES del salto de línea final: si la línea anterior acaba en un año
y la siguiente empieza por un guion pegado a otro «año» mayor («…1980⏎-2050»), el guion —que al principio de una línea es un signo
menos— se lee como el de un intervalo y la cifra, en positivo. Con 7a6583b el efecto era más amplio (dos enteros de la misma longitud).
A) a nivel de unidad (_cita_cifra con la página), 7a6583b → 876bfc2, con la cita que abarca las dos líneas;
B) en el registro completo (fixture de la batería): la entrada del año con la página en esa forma y el signo cambiado;
C) textos REALES: cuántas veces aparece la forma de riesgo («aaaa⏎-bbbb», 1900 ≤ a ≤ b ≤ 2100, la línea acaba en el año y la siguiente
   empieza por el guion) en los 73 textos conservados citados y en el texto SIN «-layout» de las páginas de PDF citadas (solo lee).
Uso: python3 -I -B d8_intervalo_salto_de_linea.py [sin_pdf]"""
import collections, glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun5 import VE, VP, PV, ACT, ANT  # noqa: E402
print(f"VE = {ACT} · VP = {ANT}")
print("comprobación del ancla: re.search(r'(\\d{4})$', '1980\\n') →", bool(re.search(r"(\d{4})$", "1980\n")), "· con \\Z →", bool(re.search(r"(\d{4})\Z", "1980\n")))

print("\n== A · unidad: la cita abarca las dos líneas")
for nombre, pag, cita, vf, real in (
        ("A1 dos negativos de cuatro cifras en líneas seguidas (texto sin columnas): «-1980⏎-2050», valor +2050", "Gastos financieros\n-1980\n-2050\n", "Gastos financieros -1980 -2050", 2050, "−"),
        ("A2 lo mismo con el valor publicado −2050", "Gastos financieros\n-1980\n-2050\n", "Gastos financieros -1980 -2050", -2050, "−"),
        ("A3 año al final de una línea y negativo al principio de la siguiente: «Ejercicio 2023⏎-2024», valor +2024", "Ejercicio 2023\n-2024\n", "Ejercicio 2023 -2024", 2024, "−"),
        ("A4 lo mismo con raya y con menos Unicode: «2023⏎−2024»", "Ejercicio 2023\n−2024\n", "Ejercicio 2023 −2024", 2024, "−"),
        ("A5 orden decreciente: «-2050⏎-1980», valor +1980 (no es un intervalo creciente)", "Gastos financieros\n-2050\n-1980\n", "Gastos financieros -2050 -1980", 1980, "−"),
        ("A6 enteros de dos cifras: «Nota 12⏎-45», valor +45 (con 7a6583b, intervalo)", "Nota 12\n-45\n", "Nota 12 -45", 45, "−"),
        ("A7 la línea anterior acaba en espacios: «2023   ⏎-2024» (el ancla ya no casa)", "Ejercicio 2023   \n-2024\n", "Ejercicio 2023 -2024", 2024, "−"),
        ("A8 la línea siguiente empieza con espacios: «2023⏎   -2024»", "Ejercicio 2023\n   -2024\n", "Ejercicio 2023 -2024", 2024, "−"),
        ("A9 fecha partida: «Notas 5-6⏎-2024», valor +2024", "Notas 5-6\n-2024\n", "Notas 5-6 -2024", 2024, "−"),
        ("A10 control: en la misma línea con un espacio «2023 -2024»", "Ejercicio 2023 -2024\n", "Ejercicio 2023 -2024", 2024, "−"),
        ("A11 control: intervalo de verdad en una línea «2023-2024»", "Ejercicio 2023-2024\n", "Ejercicio 2023-2024", 2024, "+")):
    a, b = VP._cita_cifra(cita, vf, pag), VE._cita_cifra(cita, vf, pag)
    mal = (b[0] == "ok") != ((vf > 0) == (real == "+"))
    print(f"   {nombre}\n      página={pag!r} cita={cita!r} vf={vf!r} (la página publica la cifra en {real})\n      7a6583b: {a[0]:20} 876bfc2: {b[0]:20}"
          + ("   <<< ACEPTA el signo contrario" if b[0] == "ok" and mal else "   <<< rechaza el signo publicado" if mal and b[0] == "signo_distinto" else ""))

print("\n== B · registro completo (fixture de la batería)")
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sondas"))
import fx5 as X  # noqa: E402
assert X.VE.__file__ == VE.__file__
KA = "Historia!F5"
anio = int(X.ent(X.REG, KA)["fuente"]["valor_fuente"])
print("   control positivo:", X.resumen(X.con())[:80])
for nombre, pagina, cita in ((f"la página publica «Ejercicio {anio - 1}⏎-{anio}» (−{anio} al principio de la línea) y la entrada dice +{anio}", f"Ejercicio {anio - 1}\n-{anio}", f"Ejercicio {anio - 1} -{anio}"),
                             (f"control: en la misma línea «Ejercicio {anio - 1} -{anio}»", f"Ejercicio {anio - 1} -{anio}", f"Ejercicio {anio - 1} -{anio}")):
    n = X.nueva_pagina(pagina)
    r = X.con(lambda g, n=n, cita=cita: X.ent(g, KA)["fuente"].update(cita=cita, pagina=n), resellar=True)
    print(f"   {nombre}\n      → " + ("COMPROBADA" if KA in r["comprobadas"] else "no comprobada · " + "; ".join(X.con_k(r, KA))[:170]) + f" · apto={r['apto_por_entradas']}")
print("   control positivo al final:", X.resumen(X.con())[:80])
X.limpiar()

print("\n== C · textos reales: la forma de riesgo «aaaa⏎-bbbb» (1900 ≤ a ≤ b ≤ 2100; la línea acaba en a y la siguiente empieza por el guion)")
E14 = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_14")
E412 = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_12")
E0 = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo")
EXPS = ["vidrala_decisiones_INVALIDO_perdio_analisis/Vidrala", "elis_decisiones/Elis", "viscofan/Viscofan", "elis_motor_A/Elis", "vidrala_decisiones/Vidrala", "vidrala/Vidrala", "viscofan_decisiones/Viscofan"]
GUI = "-‐‑‒–—−﹣－"
RX = re.compile(r"(?:^|[^\w.,])(\d{4})\n[" + re.escape(GUI) + r"](\d{4})(?!\d|[.,]\d)")
RX_AMPLIA = re.compile(r"(?:^|[^\w.,])(\d{1,4})\n[" + re.escape(GUI) + r"](\d{1,4})(?!\d|[.,]\d)")
RX_FECHA = re.compile(r"(?:^|[^\w.,])\d{1,2}-\d{1,2}\n[" + re.escape(GUI) + r"](\d{4})(?!\d|[.,]\d)")


def contar(t):
    riesgo = [m for m in RX.finditer(t) if 1900 <= int(m.group(1)) <= int(m.group(2)) <= 2100]
    amplia = [m for m in RX_AMPLIA.finditer(t) if len(m.group(1)) == len(m.group(2))]
    return riesgo, amplia, list(RX_FECHA.finditer(t))


textos, paginas_pdf = set(), set()
for exp in EXPS:
    c = os.path.join(E14, exp)
    reg, err = VE.cargar(c)
    for e in reg["entradas"]:
        f = e.get("fuente") if isinstance(e.get("fuente"), dict) else {}
        if f.get("archivo") and str(f["archivo"]).lower().endswith(".txt"):
            r = VE._ruta_fuente(c, f["archivo"])
            if r:
                textos.add(os.path.realpath(r))
tot = collections.Counter()
ej = []
for p in sorted(textos):
    t = open(p, encoding="utf-8", errors="replace").read()
    riesgo, amplia, fechas = contar(t)
    tot["forma de riesgo con la regla de 876bfc2 (años crecientes)"] += len(riesgo)
    tot["forma de riesgo con la regla de 7a6583b (enteros de la misma longitud)"] += len(amplia)
    tot["fecha partida «d-m⏎-aaaa»"] += len(fechas)
    ej += [(os.path.basename(p)[:40], t[max(0, m.start() - 30):m.end() + 10]) for m in riesgo[:3]]
print(f"   {len(textos)} textos conservados citados (con «-layout»): {dict(tot)}")
for x in ej[:6]:
    print("      ", repr(x))
if len(sys.argv) > 1 and sys.argv[1] == "sin_pdf":
    sys.exit(0)
CASOS = []
exp = os.path.join(E14, "elis_decisiones", "Elis")
CASOS.append(("Elis", exp, {os.path.basename(p)[:-4] + ".txt": p for p in glob.glob(os.path.join(exp, "fuentes_pdf", "*.pdf"))}))
exp = os.path.join(E14, "viscofan_decisiones", "Viscofan")
CASOS.append(("Viscofan", exp, {os.path.basename(p)[:-4] + ".txt": p for p in glob.glob(os.path.join(E412, "viscofan", "fuentes", "pdf", "*.pdf"))}))
exp = os.path.join(E14, "vidrala_decisiones", "Vidrala")
pv = {}
for p in glob.glob(os.path.join(E0, "fuentes", "cuentas_consolidadas_2016_2022", "*.pdf")):
    m = re.search(r"en-(\d{4})_consolidated", os.path.basename(p))
    if m:
        pv[f"CF_{m.group(1)}.txt"] = p
CASOS.append(("Vidrala", exp, pv))
for nombre, exp, pdfs in CASOS:
    reg = json.load(open(os.path.join(exp, VE.REGISTRO), encoding="utf-8"))
    pags = set()
    for e in reg["entradas"]:
        f = e.get("fuente") if isinstance(e.get("fuente"), dict) else None
        if f and str(f.get("archivo") or "").startswith("texto/") and pdfs.get(os.path.basename(f["archivo"])) and VE._numero_pagina(f.get("pagina")):
            pags.add((pdfs[os.path.basename(f["archivo"])], VE._numero_pagina(f.get("pagina"))))
    c = collections.Counter()
    ej = []
    for pdf, n in sorted(pags):
        t2 = VE._texto_pdf(pdf, n, layout=False)[1] or ""
        riesgo, amplia, fechas = contar(t2)
        c["páginas"] += 1
        c["forma de riesgo (876bfc2)"] += len(riesgo)
        c["forma de riesgo (7a6583b)"] += len(amplia)
        c["fecha partida"] += len(fechas)
        c["líneas que empiezan por un guion pegado a una cifra"] += len(re.findall(r"(?m)^[" + re.escape(GUI) + r"]\d", t2))
        ej += [(os.path.basename(pdf)[:36], n, t2[max(0, m.start() - 25):m.end() + 8]) for m in (riesgo + amplia)[:2]]
    print(f"   {nombre}: texto SIN «-layout» de las páginas de PDF citadas: {dict(c)}")
    for x in ej[:5]:
        print("      ", repr(x))
