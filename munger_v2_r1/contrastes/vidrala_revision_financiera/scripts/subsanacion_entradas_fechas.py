#!/usr/bin/env python3
"""Munger v2 · entrega 4.3.1 · subsanación acotada: entradas del motor B, fechas y acciones (solo lectura).

Qué hace:
  1. Comprueba la huella de las fuentes que usa (texto EN25 del piloto, BORME conservado en esta entrega, libro,
     datos_v63.json del expediente).
  2. Comprueba cada cifra citada contra el texto de su página.
  3. Lee del libro (valores en caché) las entradas del motor B, el precio, la capitalización, las acciones y sus fechas,
     y la forma de descontar del motor.
  4. Lee de datos_v63.json (Control maestro heredado) las notas sobre 2026 y las clasifica como HEREDADAS NO CONTRASTADAS.
  5. Hace aritmética explícita sobre recuentos de acciones, fechas y saldos. No es una valoración: no calcula ningún
     valor por acción ni ningún precio de Sí, y no acredita hipótesis.

No escribe en el paquete, no crea __pycache__ (ejecutar con «python3 -I») y no modifica el script de 217 comprobaciones.
"""
import datetime as dt
import hashlib
import json
import os
import re
import sys

sys.dont_write_bytecode = True
import openpyxl  # noqa: E402

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
EXP = os.path.join(RAIZ, "personaje_v2", "empresas_v2", "Vidrala")
AQUI = os.path.join(RAIZ, "contrastes", "vidrala_revision_financiera")
F = {
    "EN25": (os.path.join(RAIZ, "contrastes", "piloto_Vidrala_2025", "fuentes", "texto_nuevo_CF_2025", "CF_2025_EXTRACCION_NUEVA.txt"),
             "ebfe0f35db7e30adf6ec381a610d30c4a56bc3ca59da24fe4c5af5b60aa6a4e4"),
    "BORME_PDF": (os.path.join(AQUI, "fuentes", "borme_2026_5696", "BORME-C-2026-5696.pdf"),
                  "59ec693b4aa943736d4433d74cdfe2d4b9bd8fea4a42f1f58ff28ab21db6394c"),
    "BORME": (os.path.join(AQUI, "fuentes", "borme_2026_5696", "BORME-C-2026-5696_texto.txt"),
              "4c90c93be02c836b3073677dc922f648f193060ed0d52f59e6cf3448cb7e1f81"),
    "LIBRO": (os.path.join(EXP, "Vidrala_v63_evaluada.xlsx"),
              "21c386711613fc4264ddff013a75ddaf2d0869378ee4a39e8ce07cd51f91da07"),
}
N_OK = N_TOTAL = 0


def comprobar(nombre, cond, detalle=""):
    global N_OK, N_TOTAL
    N_TOTAL += 1
    N_OK += bool(cond)
    print(f"  [{'CUMPLE' if cond else 'NO CUMPLE'}] {nombre}" + (f" · {detalle}" if detalle else ""))
    return bool(cond)


def sha(ruta):
    with open(ruta, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def paginas(ruta):
    t = open(ruta, encoding="utf-8").read()
    p = re.split(r"^\[PDF PAGE (\d+)\]\n", t, flags=re.M)
    return {int(p[i]): re.sub(r"\s+", " ", p[i + 1]) for i in range(1, len(p), 2)}


def esta(doc, pag, frase):
    return frase in TXT[doc][pag]


def pc(x, d=2):
    return mm(x * 100, d) + " %"


def mm(x, d=3):
    s = f"{x + 0.0:,.{d}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


print("SUBSANACIÓN 4.3.1 · ENTRADAS DEL MOTOR B, FECHAS Y ACCIONES · script de solo lectura")
print("=" * 100)
print("\n1. HUELLAS")
for k, (ruta, h) in F.items():
    comprobar(f"{k}: SHA-256 {h[:12]}…", os.path.exists(ruta) and sha(ruta) == h)
huella_datos = sha(os.path.join(EXP, "datos_v63.json"))
print(f"  datos_v63.json (Control maestro heredado, solo lectura): SHA-256 {huella_datos[:12]}…")
TXT = {"EN25": paginas(F["EN25"][0]), "BORME": paginas(F["BORME"][0])}

# ────────────────────────────────────────────────────────────────────────────────
print("\n2. HECHOS CITADOS · cuentas consolidadas 2025 (EN25)")
comprobar("p.60: acciones emitidas a 31-dic-2025 = 35,206,258", esta("EN25", 60, "At December 31 2025 35,206,258"))
comprobar("p.61: autocartera a 31-dic-2025 = 23,400 acciones", esta("EN25", 61, "Acquisition of own shares 23,400 330,000 Sale of own shares - (330,000) At December 31 23,400 -"))
comprobar("p.76: promedio ponderado de 2025 = 35,205,947 acciones; sin acciones potenciales dilutivas",
          esta("EN25", 76, "Weighted average number of ordinary shares outstanding at 31 December 35,205,947")
          and esta("EN25", 76, "The Company has no dilutive potential ordinary shares"))
comprobar("p.61: programa de recompra de 12 meses de hasta 350,000 acciones y 33 mm como máximo",
          esta("EN25", 61, "for the acquisition of up to 350,000 shares, with a maximum effective amount of EUR 33 million"))
comprobar("p.64: dividendo a cuenta de 2025 de 1,2318 €/acción (43,338 miles) aprobado el 19-dic-2025 y pagado el 13-feb-2026",
          esta("EN25", 64, "EUR 1.2318 per share, equivalent to a gross amount of EUR 43,338 thousand, which was paid on 13 February 2026"))
comprobar("p.65: dividendo complementario propuesto de 16.490.205,54 € (pendiente de la junta)", esta("EN25", 65, "Dividend 16,490,205.54"))
comprobar("p.78: Toro, valor de empresa ≈77 mm con deuda asumida y pago aplazado; ventas ≈70 mm y EBITDA ajustado ≈12 mm esperados en 2025",
          esta("EN25", 78, "total enterprise value of approximately EUR 77 million, which includes assumed debt and a portion of the price subject to deferred payment")
          and esta("EN25", 78, "equivalent to EUR 70 million and EUR 12 million, respectively"))
comprobar("p.78: cierre de Toro sujeto a un plan de ajuste y a la refinanciación con los acreedores actuales",
          esta("EN25", 78, "an organisational adjustment and adaptation plan, and the agreement of a refinancing arrangement with the current lenders"))
comprobar("p.78: borrasca Kristin en Portugal a comienzos de 2026, impacto preliminar de 10 a 15 mm antes de seguros y ayudas",
          esta("EN25", 78, "between EUR 10 million and EUR 15 million"))
comprobar("p.72: la provisión de personal recoge planes de prestación definida «y otras obligaciones con empleados»; plan británico de pensión y cobertura médica",
          esta("EN25", 72, "The personnel provision reflects defined benefit plans and other obligations with employees")
          and esta("EN25", 72, "post-retirement medical coverage"))
comprobar("p.71: provisión de personal a 31-dic-2025 = 6,223 (sin desglose de obligación y activos del plan en esa tabla)",
          esta("EN25", 71, "At 31 December 2025") and re.search(r"At 31 December 2025 46,366 6,223", TXT["EN25"][71]) is not None)
comprobar("p.3: la deuda del balance (préstamos) no incluye dividendos a pagar ni otros pasivos corrientes",
          esta("EN25", 3, "Loans and borrowings 16 66,833 92,688") and esta("EN25", 3, "Other current liabilities 13 26,440 30,848"))

print("\n3. HECHOS CITADOS · BORME núm. 208, 28-oct-2026, anuncio 5696 (conservado en esta entrega)")
B = " ".join(TXT["BORME"].values())
comprobar("Fecha de publicación: miércoles 28 de octubre de 2026", "Miércoles 28 de octubre de 2026" in B)
comprobar("Ejecuta el acuerdo sexto de la junta de 29-abr-2026: 1.760.312 acciones nuevas, liberadas, a 1,02 €",
          "Junta General Ordinaria de Accionistas de 29 de abril de 2026" in B and "(1.760.312)" in B and "€1.795.518,24" in B)
comprobar("Proporción: una acción nueva por cada veinte antiguas", "una (1) acción nueva por cada veinte (20) acciones antiguas" in B)
comprobar("Período de asignación: catorce días naturales desde el día siguiente a la publicación en el BORME y en la web de la sociedad",
          "catorce (14) días naturales a contar desde el día siguiente al de la publicación del anuncio de ampliación de capital en el Boletín Oficial del Registro Mercantil y la página web de la Sociedad" in B)
comprobar("Legitimados: titulares al final del día inmediatamente anterior al inicio del período de asignación",
          "al final del día inmediatamente anterior a la fecha de inicio del período de asignación gratuita" in B)
comprobar("El balance de base es el de 31-dic-2025", "ejercicio cerrado a 31 de diciembre de 2025" in B)
comprobar("1.760.312 × 20 = 35.206.240 acciones antiguas con derecho, frente a 35.206.258 emitidas a 31-dic-2025 (18 de diferencia por redondeo)",
          1760312 * 20 == 35206240 and 35206258 - 35206240 == 18)
print("  [Interpretación] Si la web publicó el mismo día, el período empieza el 29-oct-2026 y termina el 11-nov-2026: el 3-nov-2026 está dentro.")
print("  [Interpretación] En el mercado español la acción cotiza sin derecho desde el inicio del período; el BORME no fija esa fecha. Confirmarla exige el")
print("  calendario de la operación (hecho relevante o documento informativo de la CNMV/web, no conservados).")

# ────────────────────────────────────────────────────────────────────────────────
print("\n4. LIBRO (valores en caché, solo lectura)")
wv = openpyxl.load_workbook(F["LIBRO"][0], data_only=True)
wf = openpyxl.load_workbook(F["LIBRO"][0])
AN, H, P, M = wv["Análisis"], wv["Historia"], wv["Palancas"], wf["Motor"]
precio, cap, acc, r = AN["C37"].value, AN["C41"].value, AN["C55"].value, AN["C56"].value
f_precio, f_acc = P["C45"].value, P["C46"].value
comprobar(f"Análisis C37 (precio) = {precio}; C41 (capitalización) = {cap}; C55 (acciones) = {acc}; C56 (r) = {r}", (precio, cap, acc, r) == (87.9, 3094.6, 35.206, 0.09))
comprobar("C41 = C37 × C55 redondeado a un decimal", round(precio * acc, 1) == cap, mm(precio * acc, 4))
comprobar(f"Palancas C45 (fecha del precio) = {f_precio:%d-%m-%Y}; C46 (fecha de las acciones) = {f_acc:%d-%m-%Y}",
          f_precio == dt.datetime(2026, 11, 3) and f_acc == dt.datetime(2025, 12, 31))
comprobar("Palancas C47 (causa declarada de la diferencia de capitalización) = «Ninguna»", P["C47"].value == "Ninguna")
comprobar("Historia L20 (media diluida del año 2025) = C55 = 35,206", H["L20"].value == acc)
comprobar("Análisis D4 (fecha de análisis) = «2026-11-03», escrita como texto (aviso V31 del libro)", AN["D4"].value == "2026-11-03")
comprobar("Análisis C53 y C54 (contexto, 30-jun-2026) = 109,4 y 409,6; no entran en el motor B (convención 5)", (AN["C53"].value, AN["C54"].value) == (109.4, 409.6))
e = [M.cell(3, c).value for c in range(47, 57)]
comprobar("Motor: los flujos 1–10 se descuentan con exponentes enteros 1…10 (fila 3) y el terminal con ^10: valor referido al cierre del año base",
          e == list(range(1, 11)) and "^$AU$3:$BD$3" in M["BE7"].value and "^10" in M["BH7"].value)
D, L = H["C64"].value, H["L23"].value
comprobar("Historia C64 (deuda con arrendamientos, 31-dic-2025) = 262,913; C63 (i) y C52 (τ) del libro", D == 262.913, f"i {H['C63'].value:.6f} · τ {H['C52'].value:.5f}")

# ────────────────────────────────────────────────────────────────────────────────
print("\n5. CONTROL MAESTRO HEREDADO (datos_v63.json): notas sobre 2026, NO CONTRASTADAS en esta entrega")
dd = json.load(open(os.path.join(EXP, "datos_v63.json"), encoding="utf-8"))


def filas(o):
    if isinstance(o, dict):
        yield o
        for v in o.values():
            yield from filas(v)
    elif isinstance(o, list):
        for v in o:
            yield from filas(v)


CM = {}
for o in filas(dd):
    if isinstance(o, dict) and "celda" in o and "concepto" in o and "M" in o and o["celda"] not in CM:
        CM[o["celda"]] = o
c37, c41, c55, c34, c53, c54 = (CM[k] for k in ("Análisis!C37", "Análisis!C41", "Análisis!C55", "Análisis!C34", "Análisis!C53", "Análisis!C54"))
comprobar("C37: el campo «periodo» dice «Cierre 09/10/2026», pero la fuente es una cotización intradía de Bolsamanía del 03/11/2026 a las 10:13 (secundaria, un solo proveedor)",
          c37["periodo"] == "Cierre 09/10/2026" and "03/11/2026 10:13" in c37["J"] and "Sin otra fuente contrastada" in c37["J"])
comprobar("C37: la nota califica el precio de «con derecho» porque la liberada «no consta ejecutada a 09/10/2026»",
          "Precio \"con derecho\"" in c37["M"] and "no consta ejecutada a 09/10/2026" in c37["M"])
comprobar("C41: la nota del Control maestro calcula otra capitalización, 88,70 × 34,185 (netas de una autocartera ≈1,021 mm) = 3.032,2, distinta de la del libro",
          "88,70 × 34,185" in c41["M"] and "3.032,2" in c41["M"])
comprobar("C41: la autocartera de 2026 es una suma de informes semanales con un supuesto (sin compras 23/06–22/07)", "supuesto: sin compras 23/06–22/07" in c41["N"])
comprobar("C55: la nota anticipa ≈35,89 mm de acciones si se ejecuta la liberada con precio ex", "≈35,89 mm con precio ex" in c55["N"])
comprobar("C34 (fuente: informe semestral 1S2026, doc. 2487, no conservado): emisión 259,4; recompras 52,7; dividendos 43,3; Chile 23,6",
          all(x in c34["N"] for x in ("emisión 259,4", "recompras 52,7", "dividendos 43,3", "Chile 23,6")) and "2487" in c34["K"])
comprobar("C53: dividendo complementario ≈16,5 mm pagado el 15/07/2026 (heredado)", "≈16,5 mm pagado 15/07/2026" in c53["N"])
comprobar("C54: 30-jun-2026, pasivos financieros 409,6 con arrendamientos; sin NIIF 16, 361,7; deuda neta APM 252,3 (heredado)",
          "409,6" in c54["M"] and "361,7" in c54["N"] and "252,3" in c54["N"])

# ────────────────────────────────────────────────────────────────────────────────
print("\n6. ARITMÉTICA DE ACCIONES, FECHAS Y SALDOS (no es una valoración)")
emit25, auto25, nuevas = 35206258, 23400, 1760312
circ25 = (emit25 - auto25) / 1e6
total_post = (emit25 + nuevas) / 1e6
auto26_her = 1.021  # heredada, no contrastada (C41 y C55 del Control maestro)
neto_post_her = (emit25 / 1e6 - auto26_her) * 1.05
neto_post_sin = (emit25 - auto25) / 1e6 * 1.05
print(f"  Acciones del libro (C55): {acc} · emitidas 31-dic-2025 {mm(emit25 / 1e6, 6)} · en circulación 31-dic-2025 {mm(circ25, 6)} ({('+' if (circ25 / acc - 1) >= 0 else '') + pc(circ25 / acc - 1, 4)})")
print(f"  Tras la liberada: emitidas {mm(total_post, 6)} ({('+' if (total_post / acc - 1) >= 0 else '') + pc(total_post / acc - 1, 4)})")
print(f"  En circulación tras la liberada, con la autocartera de 31-dic-2025 (23.400): {mm(neto_post_sin, 6)} ({('+' if (neto_post_sin / acc - 1) >= 0 else '') + pc(neto_post_sin / acc - 1, 4)})")
print(f"  En circulación tras la liberada, con la autocartera heredada de 2026 (≈1,021 mm, no contrastada): {mm(neto_post_her, 6)} ({('+' if (neto_post_her / acc - 1) >= 0 else '') + pc(neto_post_her / acc - 1, 4)})")
comprobar("La autocartera heredada (≈1,021 mm) no cabe en el programa documentado de 350.000 acciones: exige otro programa no documentado aquí", auto26_her * 1e6 > 350000)
dias = (f_precio - f_acc).days
fac = (1 + r) ** (dias / 365) - 1
print(f"  Días entre la fecha de referencia del motor (31-dic-2025) y la del precio (3-nov-2026): {dias} → (1 + r)^({dias}/365) − 1 = {pc(fac, 4)} con r = {mm(r, 2)}")
print(f"  Parte transcurrida del año 1 del motor (2026) en la fecha del precio: {pc(dias / 365, 1)}")
div26 = 43.338 + 16.490
print(f"  Dividendos de 2026 que el comprador del 3-nov-2026 ya no recibe: 43,338 (hecho) + 16,490 (propuesto; pago heredado) = {mm(div26)} mm "
      f"= {mm(div26 / acc, 4)} €/acción sobre C55 = {pc(div26 / cap, 2)} de C41")
dn25 = D - H["L24"].value
dn26 = 409.6 - 109.4
print(f"  Deuda neta con arrendamientos: 31-dic-2025 {mm(dn25)} (documentada) · 30-jun-2026 {mm(dn26, 1)} (heredada) · variación {mm(dn26 - dn25, 1)} = {pc((dn26 - dn25) / cap, 2)} de C41")
print(f"  Toro: valor de empresa ≈77 mm (EN25 p.78) = {pc(77 / cap, 2)} de C41; ventas ≈70 mm = {pc(70 / H['L6'].value, 2)} de V0")
print(f"  Borrasca Kristin: 10–15 mm antes de seguros (EN25 p.78) = {pc(10 / cap, 2)}–{pc(15 / cap, 2)} de C41")


def r_op(E, Dd):
    return r * E / (E + Dd) + H["C63"].value * (1 - H["C52"].value) * Dd / (E + Dd)


base = r_op(cap, D)
print("  r_op de la convención 4 (aritmética; no es una valoración):")
for nom, E_, D_ in (("libro: E = 87,9 × 35,206 (3-nov-2026 × 31-dic-2025); D a 31-dic-2025", cap, D),
                    ("E con acciones en circulación tras la liberada y autocartera heredada", precio * neto_post_her, D),
                    ("E del libro; D con los pasivos financieros heredados a 30-jun-2026 (409,6)", cap, 409.6)):
    v = r_op(E_, D_)
    print(f"    {nom}: {mm(v, 6)} ({'+' if v >= base else '−'}{mm(abs(v - base) * 1e4, 1)} pb)")
comprobar("El libro mezcla fechas en E (precio de 3-nov-2026 por acciones de 31-dic-2025) y en D (31-dic-2025)", f_precio != f_acc)
comprobar("El libro no ha cambiado durante la ejecución", sha(F["LIBRO"][0]) == F["LIBRO"][1])
print(f"\nRESULTADO: {N_OK} de {N_TOTAL} comprobaciones cumplen.")
sys.exit(0 if N_OK == N_TOTAL else 1)
