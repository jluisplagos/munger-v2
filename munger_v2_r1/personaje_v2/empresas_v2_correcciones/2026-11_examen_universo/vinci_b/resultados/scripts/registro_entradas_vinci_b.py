#!/usr/bin/env python3
"""Registro de entradas de vinci_b (examen; encargo del coordinador, 20-nov-2026). Parte del registro del extractor Mistral (rama
mistral/examen-vinci-entradas @ 737a8d8, resultados_examen/vinci/verificacion_entradas.json: 315 entradas + 162 auxiliares) y le aplica las
correcciones de la revisión independiente del registro (munger-v2-evidencias-mistral, coordinacion/cierre-v2,
coordinacion/cierre_v2/examen/vinci/revision_registro/REVISION.md y REVISION.tsv), adaptadas a los valores ACTUALES de vinci_b (plantilla
regenerada con `verificacion_entradas.py plantilla` sobre el libro de datos V6.3.2 F1):
  1. citas vacías de los 121 auxiliares: la línea literal que Mistral dejó en comprobacion.nota («línea: …») pasa a fuente.cita (se comprueba
     que está en su página);
  2. capa F1 Historia H86:L87 (estaban como dato_ausente con valor): H86:L86 y I87:L87 dato_publicado con las citas de motor_a_f1.json (nota 4.3);
     H87 = 0 «no_aplicable» (Cobra IS se compró el 31-dic-2021: no hay PPA que amortizar en 2021; la página no imprime un 0, así que no puede ser
     un cero_comprobado, que exige la cifra en la cita); justificación de F86/G86 corregida (la cifra sí se publica: URD 2020 PDF p. 319);
  3. C40 = 4.132 derivado con su cálculo declarado (2025); C26 = 2,31 derivado (Σ CFO 2021–25 ÷ Σ resultado neto consolidado, round 2);
  4. C57 = 0,0347 dato_publicado (Bundesbank WT1010, 2026-10-09; fuentes_mercado/);
  5. clases: C28, C31, C34, C60 y C88 convención (con el fundamento de la etapa 1 y justificacion_clase); C38 dato_publicado con lectura
     externa (Simply Wall St, sin bytes: no cuenta como comprobada);
  6. K22/L22: la cita con la raya «–» que imprime la página; Palancas!C48 y Control maestro!H4: equivalencia «€»;
  7. C37 con la exportación oficial de Euronext entregada por la persona y Palancas!C7 con damodaran_margin.xls (fuentes_mercado/, con huella);
  8. entradas nuevas de la normalización del circulante (V6.3.2 F1): Historia C93 y H94:L94 hipótesis declaradas (V-CIRC (a), V-ANCLA (a));
     C94:G94 no aplicables (años sin declarar, que no usa la reinversión);
  9. las 30 celdas de hipótesis del modelo (Mistral las dejó sin tocar, sin fundamento: error del contrato): las 11 que tienen valor (heredado de
     la etapa 1) llevan el fundamento de la etapa 1 que el libro guarda en Control maestro!N; las 19 vacías llevan un fundamento que dice
     expresamente que no hay hipótesis todavía (la escribe la fase). Ninguna se presenta como comprobada.
Extractor Mistral donde nada cambia; «Claude orquestación» en lo que cambia. Todas las comprobaciones quedan «pendiente», sin revisor ni vínculo
(no se usa `sellar`). No toca el libro, las fuentes ni las fases.
Uso: python3 registro_entradas_vinci_b.py CARPETA_EXPEDIENTE REGISTRO_MISTRAL.json PLANTILLA.json SALIDA_CAMBIOS.json"""
import copy
import hashlib
import json
import os
import re
import sys

C, ORIGEN, PLANT, SALIDA = sys.argv[1:5]
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "..", "..", "..", "..", "scripts"))
import verificacion_entradas as VE  # noqa: E402

EXT = "Claude orquestación"
MIS = "Mistral (mistral-large-4-0)"
HOY = "2026-11-20"
reg = json.load(open(ORIGEN, encoding="utf-8"))
reg_sha = hashlib.sha256(open(ORIGEN, "rb").read()).hexdigest()
plant = json.load(open(PLANT, encoding="utf-8"))
por = {e["celda"]: e for e in reg["entradas"]}
PL = {e["celda"]: e for e in plant["entradas"]}
INST = VE.universo(C)
EVID = VE.evidencia_libro(C)
CAMBIOS = []
assert set(PL) == set(INST["celdas"]) and len(PL) == 326


def sha(p):
    return hashlib.sha256(open(os.path.join(C, p), "rb").read()).hexdigest()


def pagina(archivo, n):
    t = open(os.path.join(C, archivo), encoding="utf-8").read()
    m = re.search(r"\[PDF PAGE %d\]" % n, t)
    fin = re.search(r"\[PDF PAGE \d+\]", t[m.end():])
    return t[m.end(): m.end() + fin.start()] if fin else t[m.end():]


def en_pagina(archivo, n, cita):
    return VE._norm_txt(cita) in VE._norm_txt(pagina(archivo, n))


def comp(fuente_examinada, nota):
    return {"extractor": EXT, "revisor": None, "fecha": HOY, "resultado": "pendiente", "fuente_examinada": fuente_examinada, "nota": nota, "vinculo": None}


DOCS = {}
for e in reg["entradas"]:
    f = e.get("fuente") or {}
    if str(f.get("archivo") or "").startswith("texto/") and f["archivo"] not in DOCS:
        DOCS[f["archivo"]] = {"documento": f["documento"], "version": f["version"], "sha256": f["sha256"]}
for a, d in DOCS.items():
    assert sha(a) == d["sha256"], f"huella distinta: {a}"


def nueva(celda, clase, valor, **kw):
    e = {"celda": celda, "id": PL[celda]["id"] if celda in PL else "aux", "ambito": PL[celda]["ambito"] if celda in PL else None, "uso": None, "material": True,
         "clase": clase, "valor_modelo": valor, "fuente": {}, "derivacion": None, "hipotesis": None, "justificacion": None, "comprobacion": None, "incidencia": None}
    e.update(kw)
    return e


def poner(e, motivo):
    k = e["celda"]
    if k in por:
        reg["entradas"][reg["entradas"].index(por[k])] = e
    else:
        reg["entradas"].append(e)
    por[k] = e
    CAMBIOS.append({"celda": k, "motivo": motivo})


def vm(k):
    return INST["celdas"][k]


COL = dict(zip(range(2016, 2026), "CDEFGHIJKL"))
decl = json.load(open(os.path.join(C, "motor_a_f1.json"), encoding="utf-8"))
f1 = json.load(open(os.path.join(C, "fase1_v63.json"), encoding="utf-8"))

# ------------------------------------------------------------------------------------------- 1. citas vacías de los auxiliares (121)
n_aux = 0
for k, e in list(por.items()):
    if not k.startswith("aux:") or (e.get("fuente") or {}).get("cita") is not None:
        continue
    nota = (e.get("comprobacion") or {}).get("nota") or ""
    m = re.search(r"línea: (.+)$", nota)
    assert m, k
    cita = m.group(1).strip()
    f = e["fuente"]
    assert en_pagina(f["archivo"], f["pagina"], cita), (k, cita)
    e2 = copy.deepcopy(e)
    e2["fuente"]["cita"] = cita
    e2["comprobacion"] = comp(e["comprobacion"].get("fuente_examinada"),
                              f"{nota} · (orquestación) cita = la línea literal que el extractor Mistral dejó en esta nota; Mistral extrajo el dato y no lo cambia "
                              "(revisión del registro, «121 aux tienen cita = null»)")
    poner(e2, "cita vacía → línea literal de la nota del extractor (revisión del registro)")
    n_aux += 1
assert n_aux == 121, n_aux

# ------------------------------------------------------------------------------------------- 2. K22/L22 (raya) y equivalencia «€»
for k in ("Historia!K22", "Historia!L22"):
    e = copy.deepcopy(por[k])
    vieja = e["fuente"]["cita"]
    assert vieja.startswith("I - Gross financial debt")
    e["fuente"]["cita"] = "I – Gross financial debt (29,972) (6,740) (36,712) (29,118) (6,152) (35,271)"
    assert en_pagina("texto/vinci-urd-2025.txt", 401, e["fuente"]["cita"])
    e["comprobacion"] = comp(por[k]["comprobacion"]["fuente_examinada"], "Cita con la raya «–» que imprime la página (antes guion «-»: comprobar daba discrepancia); valor sin cambio")
    poner(e, "cita: guion → raya «–» de la página (revisión del registro)")
for k in ("Palancas!C48", "Control maestro!H4"):
    e = copy.deepcopy(por[k])
    e["fuente"]["equivalencia"] = "€"
    e["comprobacion"] = comp(por[k]["comprobacion"]["fuente_examinada"], "«EUR» se imprime «€» («in € millions»): equivalencia «€» declarada (antes «€ (in € millions)», que la cita no contiene literal)")
    poner(e, "equivalencia «€» (revisión del registro)")

# ------------------------------------------------------------------------------------------- 3. capa F1, Historia F86:L87
J_F86 = ("Celda vacía en el libro: la declaración F1 (motor_a_f1.json → series.da_rou) solo cubre 2021–2025, los años que usa la capa F1 (ventana de f "
         "2023–2025 y los cinco del ancla). La cifra SÍ se publica: URD 2020 PDF p. 319 «In 2020, depreciation of property, plant and equipment included €582 "
         "million relating to right-of-use assets under leases (€548 million in 2019).» (y URD 2021 PDF p. 156: 582 en 2020); no se lleva al libro porque "
         "ningún cálculo F1 la usa. (vinci_b: corrige la justificación del extractor, que decía que no se desglosaba; revisión del registro, F86/G86.)")
assert en_pagina("texto/vinci-urd-2020.txt", 319, "In 2020, depreciation of property, plant and equipment included €582 million relating to right-of-use assets under leases (€548 million in 2019).")
for k in ("Historia!F86", "Historia!G86"):
    assert vm(k) is None
    e = copy.deepcopy(por[k])
    e["justificacion"] = J_F86
    e["comprobacion"] = comp("texto/vinci-urd-2020.txt [PDF PAGE 319]", "Clase sin cambio (celda vacía); justificación corregida: la cifra se publica pero la declaración F1 no la usa")
    poner(e, "justificación corregida (la cifra se publica: URD 2020 p. 319)")


def fuente_txt(archivo, pag, ubicacion, concepto, columna, periodo, valor_fuente, cita, reexpresado, tratamiento):
    d = DOCS[archivo]
    assert en_pagina(archivo, pag, cita), (archivo, pag, cita)
    return {"documento": d["documento"], "version": d["version"], "archivo": archivo, "sha256": d["sha256"], "pagina": pag, "folio": None,
            "ubicacion": ubicacion, "concepto": concepto, "columna": columna, "periodo": periodo, "unidad": "millones de euros", "escala": 1, "signo": 1,
            "tratamiento": tratamiento, "perimetro": "consolidado", "reexpresado": reexpresado, "valor_fuente": valor_fuente, "cita": cita}


CORRIENTE = {
    ("da_rou", 2021): ("texto/vinci-urd-2021.txt", 156, "In 2021, depreciation of property, plant and equipment included €605 million relating to right-of-use assets under leases"),
    ("da_rou", 2022): ("texto/vinci-urd-2022.txt", 168, "Depreciation of property, plant and equipment included €623 million in 2022 relating to right-of-use assets under leases"),
    ("da_rou", 2023): ("texto/vinci-urd-2023.txt", 171, "Depreciation of property, plant and equipment included €668 million in 2023 relating to right-of-use assets under leases"),
    ("da_rou", 2024): ("texto/vinci-urd-2024.txt", 350, "Depreciation of property, plant and equipment included €714 million in 2024 relating to right-of-use assets under leases"),
    ("da_ppa", 2023): ("texto/vinci-urd-2023.txt", 171, "In 2022 and 2023, amortisation of other intangible assets included €128 million relating to intangible assets identified when allocating"),
    ("da_ppa", 2024): ("texto/vinci-urd-2024.txt", 350, "Amortisation of other intangible assets included €108 million in 2024"),
}
ULT = {"da_rou": {2021: "URD2022", 2022: "URD2023", 2023: "URD2024", 2024: "URD2025", 2025: "URD2025"}}
for serie, fila, concepto in (("da_rou", 86, "amortización de los derechos de uso de arrendamientos (NIIF 16) incluida en la depreciación del inmovilizado material"),
                              ("da_ppa", 87, "amortización de los intangibles identificados en la asignación del precio de compra de Cobra IS (PPA)")):
    for y in range(2021, 2026):
        k = f"Historia!{COL[y]}{fila}"
        s = decl["series"][serie][str(y)]
        assert vm(k) == s["valor_fuente"], (k, vm(k), s["valor_fuente"])
        if s.get("cero_comprobado"):
            cz = s["cero_comprobado"]
            assert vm(k) == 0 and y == 2021 and serie == "da_ppa"
            poner(nueva(k, "no_aplicable", vm(k), justificacion=(
                f"Sin PPA de Cobra IS que amortizar en {y}: «{cz['cita']}» ({s['archivo']} [PDF PAGE {s['pagina']}]); la compra se cerró el último día del ejercicio y la "
                "nota 4.3 de 2021 (PDF p. 156) no menciona ninguna amortización de intangibles de combinaciones. La página no imprime un 0 de la partida: no es un "
                "cero_comprobado (exige la cifra en la cita), sino una partida que no aplica ese año (precedente zoetis_t1c). LÍMITE (motor_a_f1.json): es la única "
                "amortización de intangibles de combinaciones que VINCI publica por separado; la frase no prueba por sí sola la inexistencia de otras "
                "(F1-SERIES-CERO, pendiente de revisor)."),
                comprobacion=comp(f"{s['archivo']} [PDF PAGE {s['pagina']}]", "Cero por lectura de la declaración F1 (series.da_ppa.2021), pendiente de revisor. La revisión del "
                                                                              "registro proponía cero_comprobado; con esa clase la cita, que no contiene un 0, daría discrepancia")),
                  "dato_ausente con valor 0 → no_aplicable (revisión del registro, capa F1)")
            continue
        corriente = (s["documento"] == f"URD{y}")
        arch, pg, cita, rexp = s["archivo"], s["pagina"], s["cita"], ("no aplica (ejercicio corriente del informe)" if corriente else "comparativo del informe siguiente (cifra más reciente publicada)")
        if (serie, y) in CORRIENTE:
            # en el comparativo la cifra va entre paréntesis («(€605 million in 2021)») y su signo no puede determinarse (R415-SIGNO): se cita la misma
            # cifra en el informe del propio ejercicio, donde se imprime sin paréntesis; el comparativo (el que declara la capa F1) da la misma
            arch, pg, cita = CORRIENTE[(serie, y)]
            corriente = True
            rexp = (f"no aplica (ejercicio corriente del informe); el comparativo del informe siguiente ({s['archivo']}, PDF p. {s['pagina']}, la fuente que declara "
                    f"motor_a_f1.json) publica la misma cifra entre paréntesis: «{s['cita']}»")
        poner(nueva(k, "dato_publicado", vm(k), fuente=fuente_txt(
            arch, pg, s["cuadro"] if arch == s["archivo"] else f"nota 4.3 «Depreciation and amortisation», texto bajo el cuadro (prosa) del URD {y}", concepto,
            f"{y} ({'ejercicio corriente' if corriente else 'comparativo'} del URD {y if corriente else s['documento'][3:]}, prosa de la nota 4.3)",
            f"ejercicio {y}", s["valor_fuente"], cita, rexp,
            "cifra publicada en positivo en la prosa de la nota 4.3, en millones de euros; sin transformación"),
            comprobacion=comp(f"{s['archivo']} [PDF PAGE {s['pagina']}]", f"Serie F1 {serie} {y} de motor_a_f1.json ({s.get('nota', '')[:220]})")),
            "dato_ausente con valor → dato_publicado con la cita de motor_a_f1.json (revisión del registro, capa F1)")

# ------------------------------------------------------------------------------------------- 4. C40 y C26 (derivados)
c40 = f1["analisis"]["C40"]
assert vm("Análisis!C40") == 4132 and c40["valor"] == 4132.0
ORIG40 = ["Historia!L11", "Historia!L14", "aux:vinci-urd-2025_p370_div_2025", "Historia!L12", "aux:vinci-urd-2025_p358_cobros_2025", "aux:vinci-urd-2025_p358_ppp_2025",
          "Historia!L16", "Historia!L17", "aux:vinci-urd-2025_p359_sbc_ab_2025"]
assert all(o in por for o in ORIG40)
poner(nueva("Análisis!C40", "derivado", vm("Análisis!C40"), derivacion={
    "origenes": ORIG40,
    "formula": ('o["Historia!L11"] + o["Historia!L14"] + o["aux:vinci-urd-2025_p370_div_2025"] - o["Historia!L12"] + o["aux:vinci-urd-2025_p358_cobros_2025"] '
                '+ o["aux:vinci-urd-2025_p358_ppp_2025"] - o["Historia!L16"] - o["Historia!L17"] - o["aux:vinci-urd-2025_p359_sbc_ab_2025"]'),
    "conciliacion": ("FCF del accionista de 2025 con la definición de C46–C52 (cálculo declarado de fase1_v63.json; revisión del montaje): CFO 11.886 + fila 14 "
                     "(−2.496, sin la entrada de circulante, M43) + dividendos de sociedades no consolidadas 40 (P-O1 c) − capex D (3.873 − cobros 179 + PPP 311 = "
                     "4.005) − intereses de arrendamientos 110 − principal 761 − SBC abonada a patrimonio 422 = 4.132 = libro. La etapa 1 traía 7.228 (FCF de VINCI "
                     "de los doce meses a 30-jun-2026, con el circulante y sin los dividendos ni la SBC)."),
    "unidad": "millones de euros"},
    comprobacion=comp("orígenes del cálculo declarado (fase1_v63.json, analisis.C40.calculo)", "C40 sin resolver en el registro del extractor: el libro vigente guarda 4.132 "
                      "(la plantilla de Mistral, anterior a ee1ca6a, decía 7.228). Derivado del cálculo declarado (revisión del registro, C40)")),
    "clase null, 7.228 → derivado 4.132 con su cálculo (revisión del registro, C40)")
NI = ["aux:vinci-urd-2022_p159_net_income_consolidado_2021", "aux:vinci-urd-2023_p164_net_income_consolidado_2022", "aux:vinci-urd-2024_p334_net_income_consolidado_2023",
      "aux:vinci-urd-2025_p356_net_income_consolidado_2024", "aux:vinci-urd-2025_p356_net_income_consolidado_2025"]
CFO = [f"Historia!{COL[y]}11" for y in range(2021, 2026)]
assert sum(vm(x) for x in CFO) == 51333 and sum(por[x]["valor_modelo"] for x in NI) == 22263
poner(nueva("Análisis!C26", "derivado", vm("Análisis!C26"), derivacion={
    "origenes": CFO + NI,
    "formula": "round((" + " + ".join(f'o["{x}"]' for x in CFO) + ") / (" + " + ".join(f'o["{x}"]' for x in NI) + "), 2)",
    "conciliacion": ("Σ CFO 2021–2025 (7.806 + 9.387 + 10.540 + 11.714 + 11.886 = 51.333) ÷ Σ resultado neto CONSOLIDADO 2021–2025 (2.195 + 4.417 + 5.102 + 5.274 + "
                     "5.275 = 22.263) = 2,3057 → 2,31 (el redondeo a 2 decimales con que la etapa 1 escribe la celda; Control maestro M31: «mismo perímetro»). Con el "
                     "atribuible daría 2,41 (sensibilidad de la etapa 1, Control maestro N31)."),
    "unidad": "x"},
    comprobacion=comp("orígenes: Historia H11:L11 y resultado neto consolidado de las cuentas de resultados (URD 2022–2025)",
                      "Clase null en el registro del extractor (no lo reproducía con el atribuible); se reproduce con el consolidado (revisión del registro, C26)")),
    "clase null → derivado round(Σ CFO ÷ Σ resultado neto consolidado, 2) (revisión del registro, C26)")


# ------------------------------------------------------------------------------------------- 5. convenciones de la etapa 1 (C28, C31, C34, C60, C88)
def ev(k):
    return EVID.get(k) or {}


def conv_etapa1(k, justificacion_clase, alternativas, limites, motivo):
    e_ = ev(k)
    partes = [f"Control maestro!{c}{e_['fila']}: {e_[c]}" for c in "LMN" if e_.get(c) and e_.get(c) != "—"]
    poner(nueva(k, "convencion", vm(k), hipotesis={
        "identificacion": "V-" + k.split("!")[1],
        "fundamento": "Cálculo o clasificación de la etapa 1, tal como lo documenta el libro: " + " · ".join(partes),
        "alternativas": alternativas, "limites": limites,
        "procedencia": f"Control maestro!L–N{e_['fila']} del libro (Vinci_v63_datos.xlsx), heredado de la etapa 1 (Vinci_evaluada.xlsx)"},
        justificacion_clase=justificacion_clase,
        comprobacion=comp(f"Control maestro!L–N{e_['fila']} del libro", f"Clase null en el registro del extractor ({(por[k]['comprobacion'] or {}).get('nota', '')[:160]}) → convención "
                                                                       "con el fundamento de la etapa 1 (revisión del registro; precedente Jumbo)")), motivo)


conv_etapa1("Análisis!C28", "Etiqueta de texto (Dilución / Recompra / Estable) que la etapa 1 deriva de las acciones diluidas medias FY2022→FY2025 (570,51 → 567,06 M) con un "
            "umbral de ±0,5 %/año fijado por el inversor el 23-oct-2026; no es una cifra publicada.",
            "Sin el umbral: «Recompra» (−0,20 %/año en 3 años) o «Emite» (+0,14 %/año en 5 años, ⚠ REVISAR), según Control maestro M33.",
            "Depende de la ventana y del umbral (decisión del inversor); informativa, no es aviso.", "clase null → convención (revisión del registro)")
conv_etapa1("Análisis!C31", "Veredicto de texto (Sí/No) de la etapa 1 que compara el crecimiento de cobros e inventarios con el de los ingresos (junio frente a junio, perímetro "
            "igual) con la decisión del inversor del 23-oct-2026; no es una cifra publicada.",
            "Sin ajustar por Fletcher (en balance con un mes de ingresos): «Sí» por 0,17 pp (Control maestro M34).",
            "El desglose a 30-jun-2026 del semestral no pudo leerse en la etapa 1 (Control maestro N34); DSO 56 → 42 días como contraste.", "clase null → convención (revisión del registro)")
conv_etapa1("Análisis!C34", "Veredicto de texto (Sí/No) de la etapa 1: caja y equivalentes 14.998 ÷ deuda financiera a corto 7.604 = 1,97x a 30-jun-2026 (semestral); no es "
            "una cifra publicada.",
            "Prueba conservadora de la etapa 1 (con arrendamientos corrientes y reverse factoring, sin la caja de Concesiones): ≈ 1,49x → Sí (Control maestro N37).",
            "La caja de diciembre está inflada por la estacionalidad del circulante; la de junio es la del balance usado.", "clase null → convención (revisión del registro)")
conv_etapa1("Análisis!C60", "Tasa de crecimiento compuesto de las acciones diluidas medias FY2022→FY2025: (567,0603 ÷ 570,51)^(1/3) − 1 = −0,00202 → −0,002 (Historia L20 e "
            "I20); exige una raíz cúbica, que el contrato de fórmulas no admite; no es una cifra publicada.",
            "Con 5 años (FY2020→FY2025): +0,14 %/año (Control maestro M55).",
            "Cálculo a mano, no reproducible por la máquina; el revisor lo recalcula con Historia I20 y L20.", "clase null → convención con su cálculo (revisión del registro)")
conv_etapa1("Análisis!C88", "Mediana del P/FCF de fin de año 2019–2025 sin 2020 (capitalización a 31-dic ÷ FCF publicado por VINCI) calculada por la etapa 1; los precios de "
            "cierre de año no están conservados en el expediente y la mediana no cabe en el formato de fórmulas: no es una cifra publicada.",
            "Con el FCF sin circulante la etapa 1 da 13,4x de mediana (Control maestro N73).",
            "Sin precios de fin de año conservados: no reproducible con el expediente; solo contexto del múltiplo terminal («contexto, no juez»).",
            "clase null → convención (duda de la revisión del registro: convención con fundamento)")

# ------------------------------------------------------------------------------------------- 6. C38 (lectura externa)
e_ = ev("Análisis!C38")
poner(nueva("Análisis!C38", "dato_publicado", vm("Análisis!C38"), fuente={
    "documento": "Simply Wall St, ficha de valoración de VINCI (DG) «future cash flow value»", "version": "lectura externa de la etapa 1 (9-oct-2026); no se conservan bytes (página de terceros)",
    "conservacion": "externa",
    "lectura_externa": {"referencia": e_.get("K") or "https://www.simplywall.st", "fecha": "2026-10-09",
                        "evidencia": "el libro guarda 111,79 en Análisis!C38; Control maestro M39: «Solo contraste: \"future cash flow value\" 111,79 €» (etapa 1)",
                        "limitaciones": "fuente de terceros, no del emisor ni de la bolsa; sin bytes conservados no cuenta como comprobada (lectura externa listada aparte); la página no muestra la tasa ni el g"},
    "archivo": None, "sha256": None, "pagina": 1, "folio": None, "ubicacion": "ficha de valoración de la fuente externa", "concepto": "valor intrínseco de una fuente externa (solo contraste)",
    "columna": "—", "periodo": "2026-10-09 (lectura de la etapa 1)", "unidad": "EUR por acción", "escala": 1, "signo": 1, "tratamiento": "valor tal como figura en la fuente externa (etapa 1 heredada)",
    "perimetro": "no aplica: dato de fuente externa de mercado", "perimetro_justificacion": "dato de terceros, fuera del perímetro contable", "reexpresado": "no aplica",
    "valor_fuente": 111.79, "cita": "111.79"},
    incidencia="Lectura externa sin bytes: no cuenta como comprobada. Material (no se declara un juicio de materialidad en este registro).",
    comprobacion=comp("lectura externa (sin bytes)", "Duda de la revisión del registro: dato_publicado con lectura externa")),
    "clase null → dato_publicado con lectura externa (duda de la revisión del registro)")

# ------------------------------------------------------------------------------------------- 7. mercado: C37, C57, Palancas!C7
FM = "fuentes_mercado/"
EUR = FM + "VINCI_DG_FR0000125486_Euronext_historical_price_2024-11-20_a_2026-11-18.txt"
BUN = FM + "Bundesbank_WT1010_bund10y_diaria_hasta_2026-11-18.txt"
DAM = FM + "Damodaran_margin_industry_averages_2026-01.txt"
c37 = "2026-10-09 | 107.8 | 108.1 | 106.75 | 107.05 | 107.05 | 776381 | 5046 | 83208577 | 107.1749"
assert en_pagina(EUR, 1, c37) and en_pagina(BUN, 1, "2026-10-09 3.47") and en_pagina(DAM, 1, "fila 39: Engineering/Construction | 48")
e = copy.deepcopy(por["Análisis!C37"])
e["fuente"] = {
    "documento": "Euronext, exportación «Historical Data» de VINCI SA (ISIN FR0000125486, Euronext Paris), del 2024-11-20 al 2026-11-18",
    "version": ("XLS entregado por la persona responsable el 19-nov-2026 (VINCI_historical_price.xls; RELEASE_FUENTES_EXAMEN_VERIFICACION.md, anexo 3 bis), conservado byte a "
                "byte en fuentes_mercado/VINCI_DG_FR0000125486_Euronext_historical_price_2024-11-20_a_2026-11-18.xls, sha256 "
                "78eee9c5d6b1e0402ab9bf8979a5f2d19c09acf3d861bca9e9427ebe305afb9d; copia de texto con marca [PDF PAGE 1] (LibreOffice --convert-to csv bajo flock, celdas "
                "separadas por « | », ninguna cifra cambia), sha256 " + sha(EUR)),
    "archivo": EUR, "sha256": sha(EUR), "pagina": 1, "folio": None,
    "ubicacion": "tabla «Historical Data» (From 2024/11/20 to 2026/11/18; cabecera «Date | Open | High | Low | Last | Close | …»), fila 2026-10-09",
    "concepto": "precio de cierre (Close; Last coincide) de la sesión del 9-oct-2026", "columna": "Close (6.ª columna) de la fila 2026-10-09",
    "periodo": "cierre de la sesión del 9-oct-2026", "unidad": "EUR por acción", "escala": 1, "signo": 1,
    "tratamiento": ("cierre de la sesión del 9-oct-2026, sin transformación. En esa fecha hay dividendo a cuenta de 1,10 € pendiente de pago (fecha ex 13-oct-2026, según "
                    "la etapa 1): la acción cotizaba con derecho a él. Coincide con el histórico no ajustado de Euronext Live conservado por el extractor Mistral "
                    "(fuentes_mercado/Euronext_DG_FR0000125486_XPAR_historico_NO_AJUSTADO_2026-01-02_a_2026-11-19.txt, fila «09/10/2026;107.80;108.10;106.75;107.05;107.05…»)"),
    "perimetro": "no aplica: dato de mercado de la acción ordinaria DG (FR0000125486) en Euronext Paris",
    "perimetro_justificacion": "el precio de la acción es un dato de mercado, no del perímetro contable de la empresa", "reexpresado": "no aplica", "valor_fuente": 107.05, "cita": c37}
e["comprobacion"] = comp(f"{EUR} [PDF PAGE 1]", "Fuente principal: la exportación de Euronext de la persona (bytes originales, anexo 3 bis); el histórico de Mistral queda como contraste. Valor sin cambio")
poner(e, "fuente → exportación oficial de Euronext entregada por la persona (fuentes_mercado/, con huella)")
poner(nueva("Análisis!C57", "dato_publicado", vm("Análisis!C57"), fuente={
    "documento": "Deutsche Bundesbank, serie diaria BBSSY.D.REN.EUR.A630.000000WT1010.A «Daily yield of the current 10 year federal bond» (Bund a 10 años de referencia)",
    "version": ("CSV oficial subido por la persona responsable a la Release fuentes-examen-20261118 de jluisplagos/munger-v2-evidencias-mistral (asset 766892543, "
                "bund_10y_WT1010.csv; última actualización de la serie 2026-11-18 12:31:26), descarga cruda conservada byte a byte en "
                "fuentes_mercado/Bundesbank_WT1010_bund10y_diaria_hasta_2026-11-18.csv, sha256 fef9498ea765b89547cebb222ab8720e91c84113c8caca74a676e21e5e571967 (la huella "
                "publicada); conservada como texto con marca [PDF PAGE 1] y separador de espacio en las filas de datos, sha256 " + sha(BUN)),
    "archivo": BUN, "sha256": sha(BUN), "pagina": 1, "folio": None,
    "ubicacion": "tabla de la serie diaria (cabecera con la definición de la serie), fila del 2026-10-09", "concepto": "rendimiento del Bund a 10 años de referencia, en % diario",
    "columna": "2026-10-09 (fecha del precio, C37 y Palancas!C45)", "periodo": "2026-10-09", "unidad": "percent", "escala": 0.01, "signo": 1,
    "tratamiento": ("rendimiento diario publicado en %; escala 0,01 lo pasa a proporción (3,47 % = 0,0347). Misma fecha que el precio (9-oct-2026). Sustituye el 3,486 % "
                    "de la etapa 1 (Investing.com, sin bytes). Contraste, no elegidas: UMU 9–10 años de la Bundesbank 3,46 % y curva AAA del BCE 3,5112 % ese día "
                    "(fuentes_mercado/, Mistral)"),
    "perimetro": "no aplica: dato de mercado (bono soberano alemán de referencia en EUR)",
    "perimetro_justificacion": "la tasa sin riesgo es un dato de mercado del bono de referencia en EUR; el perímetro contable no se aplica", "reexpresado": "no aplica",
    "valor_fuente": 3.47, "cita": "2026-10-09 3.47"},
    comprobacion=comp(f"{BUN} [PDF PAGE 1]", "Clase null y 3,486 % sin fuente oficial en el registro del extractor → 0,0347 de la serie que fijó la persona (revisión del registro, C57)")),
    "clase null, 0,03486 → dato_publicado 0,0347 (Bundesbank WT1010; revisión del registro, C57)")
e = copy.deepcopy(por["Palancas!C7"])
e["fuente"] = {
    "documento": "Damodaran (NYU Stern), «Margins by industry» (margin.xls), hoja «Industry Averages», empresas de EE. UU., «Date updated» 2026-01-05",
    "version": ("XLS subido por la persona responsable a la Release fuentes-examen-20261118 de jluisplagos/munger-v2-evidencias-mistral (asset 766892761, damodaran_margin.xls), "
                "descarga cruda conservada byte a byte en fuentes_mercado/Damodaran_margin_2026-01.xls, sha256 25b04fce9740d9a471d50e176bf55aa6b7608cd0621b00072508a20e7c35ed7a "
                "(la huella publicada); hoja «Industry Averages» conservada como texto con marca [PDF PAGE 1], una línea por fila («fila n: celda | celda …», xlrd 2.0.1), sha256 " + sha(DAM)),
    "conservacion": "local", "archivo": DAM, "sha256": sha(DAM), "pagina": 1, "folio": None,
    "ubicacion": "hoja «Industry Averages», fila 39 (columna A «Industry Name»)", "concepto": "sector de Damodaran asignado a VINCI",
    "columna": "Industry Name (columna A), fila 39 de la hoja", "periodo": "clasificación de los datos de enero de 2026 («Date updated» 2026-01-05)", "unidad": "texto", "escala": 1, "signo": 1,
    "tratamiento": ("etiqueta de industria tal como figura en la tabla (48 empresas en esa fila; márgenes de la fila en la copia de texto). La tabla es de empresas de EE. UU. "
                    "La asignación de VINCI la confirma el indname global de Damodaran que entregó la persona (damodaran_indname.xls, 22 MB, no conservado en el "
                    "expediente): «Vinci SA (ENXTPA:DG) | ENXTPA:DG | Engineering/Construction | Industrials | 1600 | France» en las tres hojas. Alternativa no elegida "
                    "(metadatos): «Transportation» (autopistas y aeropuertos)."),
    "perimetro": "no aplica: clasificación sectorial externa", "perimetro_justificacion": "la clasificación sectorial es un dato externo al perímetro contable del grupo",
    "reexpresado": "no aplica", "valor_fuente": "Engineering/Construction", "cita": "fila 39: Engineering/Construction | 48"}
e["comprobacion"] = comp(f"{DAM} [PDF PAGE 1]", "Fuente HTML de Mistral sin «archivo_texto» (pendiente) → margin.xls de la persona con su copia de texto (revisión del registro, C7)")
poner(e, "fuente → damodaran_margin.xls de la persona (fuentes_mercado/, con huella)")

# ------------------------------------------------------------------------------------------- 8. normalización del circulante (V6.3.2 F1)
nc = decl["normalizacion_circulante"]
assert vm("Historia!C93") == "circulante_a_cero" and [vm(f"Historia!{COL[y]}94") for y in range(2016, 2026)] == [None] * 5 + [1] * 5
LIM_NC = ("Hipótesis declarada por decisión de la persona, no dato publicado; una firma no la demuestra y no se adopta para dinero real. Límite declarado (V-ANCLA (a)): el "
          "capital del balance (ROIC y S2C medios de todo el capital, Historia C54–C55, P-FOSO) sigue incluyendo el circulante negativo. Solo NIIF. F1-CIRC la exige "
          "demostrada por el cálculo declarado de C46 (la caja base excluye el mismo circulante) y bloquea si no.")
ALT_NC = ("Sin normalizar (fila 14 en la reinversión, como la V6.3.1 F1: f 4,4899 %, ancla S2C 5,9595; F1-K3c bloqueaba en vinci/Vinci) u opción (b) del diagnóstico "
          "(contar el circulante también en la caja base: misma f y mismo flujo sin crecimiento, otra caja base y otra ancla); años solo 2023–2025 (rechazado: mezcla dos "
          "definiciones en el ancla).")
poner(nueva("Historia!C93", "hipotesis", vm("Historia!C93"), hipotesis={
    "identificacion": "H-F1.normalizacion_circulante.regla (motor_a_f1.json → normalizacion_circulante)",
    "fundamento": ("Decisión registrada de la persona responsable (motor_a_f1.json → normalizacion_circulante.registro: " + json.dumps(nc["registro"], ensure_ascii=False)
                   + "). " + nc["fundamento"] + " El libro escribe C93 con f1_libro_v631.py aplicar (paso 2)."),
    "alternativas": ALT_NC, "limites": LIM_NC, "procedencia": "motor_a_f1.json → Historia!C93 del libro (f1_libro_v631.py aplicar)"},
    comprobacion=comp("motor_a_f1.json → normalizacion_circulante", "Configuración de la capa F1 (V6.3.2 F1): hipótesis declarada por la persona (V-CIRC (a), V-ANCLA (a))")),
    "entrada nueva de la normalización del circulante (plantilla V6.3.2 F1)")
for y in range(2016, 2026):
    k = f"Historia!{COL[y]}94"
    if y >= 2021:
        poner(nueva(k, "hipotesis", vm(k), hipotesis={
            "identificacion": f"H-F1.normalizacion_circulante.anios.{y}",
            "fundamento": (f"{y} está en la lista de años declarada (motor_a_f1.json → normalizacion_circulante.anios = {nc['anios']}): la usa la reinversión "
                           + ("(ventana de f 2023–2025 y ancla de S2C 2021–2025)" if y >= 2023 else "(ancla de S2C, 2021–2025)")
                           + f"; marca 1 = el circulante de {y} (fila 14) no entra en la reinversión (fila 96 = 0). Decisiones V-CIRC (a) y V-ANCLA (a) de la persona."),
            "alternativas": "Sin marca (vacío): el circulante del año entra en la reinversión; F1-CIRC bloquea si falta un año que use la reinversión (cobertura obligatoria).",
            "limites": LIM_NC, "procedencia": f"motor_a_f1.json → Historia!{COL[y]}94 del libro (f1_libro_v631.py aplicar)"},
            comprobacion=comp("motor_a_f1.json → normalizacion_circulante.anios", "Configuración de la capa F1 (V6.3.2 F1)")),
            "entrada nueva de la normalización del circulante (plantilla V6.3.2 F1)")
    else:
        poner(nueva(k, "no_aplicable", vm(k), justificacion=(
            f"{y} no está en la lista de años de la normalización declarada (motor_a_f1.json → normalizacion_circulante.anios = {nc['anios']}): no lo usa la reinversión "
            "(ventana de f 2023–2025 y los cinco años del ancla de S2C, 2021–2025). Celda vacía = año sin normalizar: la fila 14 de ese año no cambia y no entra en f "
            "ni en el ancla."),
            comprobacion=comp("motor_a_f1.json → normalizacion_circulante.anios", "Año sin declarar en la normalización (vacío = sin normalizar)")),
            "entrada nueva de la normalización del circulante (plantilla V6.3.2 F1)")

# ------------------------------------------------------------------------------------------- 9. las 30 celdas de hipótesis del modelo
HIP = [k for k, t in INST["tipos"].items() if t == "hipótesis"]
assert len(HIP) == 30
con_valor, vacias = [], []
for k in HIP:
    e0 = por[k]
    assert e0.get("clase") == "hipotesis" and not e0.get("hipotesis"), k
    v = vm(k)
    e_ = ev(k)
    n = e_.get("N")
    if v is None:
        assert not n, k
        vacias.append(k)
        poner(nueva(k, "hipotesis", None, hipotesis={
            "identificacion": "H-" + str(INST["ids"].get(k)),
            "fundamento": ("SIN HIPÓTESIS TODAVÍA (relevo de la fase A sin contestar): la celda está vacía en el libro y la escribe el personaje en sus fases. Este registro "
                           "no declara ningún fundamento para ella; la entrada solo existe para que la cobertura sea completa y quedará desactualizada en cuanto una fase "
                           "escriba la celda."),
            "alternativas": "Las que declare la fase que la escriba.",
            "limites": "Sin valor ni fundamento: no cuenta como comprobada y bloquea la aptitud por entradas hasta que la fase la escriba y se registre su fundamento.",
            "procedencia": f"Control maestro!fila {e_.get('fila')} del libro (Vinci_v63_datos.xlsx): vacía antes de la fase A"},
            comprobacion=comp(f"Control maestro!fila {e_.get('fila')} del libro (vacía)", "Celda de hipótesis vacía antes de la fase A: sin fundamento que registrar")),
            "hipótesis sin fundamento (error del contrato) → entrada que declara que aún no hay hipótesis (celda vacía antes de la fase A)")
        continue
    con_valor.append(k)
    m = re.match(r"\[Clase: ([^\]]+)\] \[Confianza: ([^\]]+)\]\s*(.*)$", n, re.S)
    assert m, (k, n[:80])
    clase_decl, confianza, resto = m.groups()
    clase = "convencion" if clase_decl.strip().lower().startswith("convenci") else "hipotesis"
    alt = re.search(r"Lo sustituiría:(.*)$", resto, re.S)
    poner(nueva(k, clase, v, hipotesis={
        "identificacion": ("V-" if clase == "convencion" else "H-") + str(INST["ids"].get(k)),
        "fundamento": f"[Clase: {clase_decl}] [Confianza: {confianza}]\nHeredado de la etapa 1 de la persona responsable (la fase A o B lo reescribe): {resto.strip()}",
        "alternativas": ("Lo sustituiría:" + alt.group(1).strip()) if alt else "La fase A puede corregirlo (otra ventana de años del FCF base).",
        "limites": (f"Confianza declarada: {confianza}. Es juicio de la etapa 1 de la persona responsable (clase declarada «{clase_decl}»), heredado en el libro, no un dato "
                    "publicado ni se demuestra con una firma; las cifras y páginas de apoyo no se contrastan en este registro. Si una fase lo reescribe, este fundamento "
                    "deja de describir la celda."),
        "procedencia": f"Control maestro!N{e_['fila']} del libro (Vinci_v63_datos.xlsx), heredado de la etapa 1 (Vinci_evaluada.xlsx)"},
        comprobacion=comp(f"Control maestro!N{e_['fila']} del libro", "Hipótesis del modelo con valor heredado de la etapa 1: se registra el fundamento que guarda el libro")),
        "hipótesis sin fundamento (error del contrato) → fundamento heredado de la etapa 1 (Control maestro N del libro)")
assert len(con_valor) == 11 and len(vacias) == 19

# ------------------------------------------------------------------------------------------- 10. vigencia de los valores del libro
for k, e in por.items():
    if k.startswith("aux:"):
        continue
    if not VE._igual_exacto(vm(k), e.get("valor_modelo")):
        raise SystemExit(f"valor desactualizado sin corregir: {k}: libro {vm(k)!r}, registro {e.get('valor_modelo')!r}")
assert set(k for k in por if not k.startswith("aux:")) == set(PL)

# ------------------------------------------------------------------------------------------- cabecera
reg["huella_entradas_economicas"] = plant["huella_entradas_economicas"]
reg["fuentes_mercado"] = {"archivo": "fuentes_mercado/", "huellas": "fuentes_mercado/HUELLAS.txt (resultados/fuentes_mercado_vinci_b.json)",
                          "contenido": dict(reg["fuentes_mercado"]["contenido"], **{
                              os.path.basename(EUR): {"que": "Exportación de Euronext «Historical Data» entregada por la persona (anexo 3 bis), copia de texto; fila usada: 2026-10-09, Close 107.05 (Análisis!C37). XLS original al lado (78eee9c5…).", "sha256": sha(EUR)},
                              os.path.basename(BUN): {"que": "Bundesbank WT1010 (Bund a 10 años), CSV oficial de la Release (asset 766892543), copia de texto; fila usada: 2026-10-09 3.47 (Análisis!C57). CSV original al lado (fef9498e…).", "sha256": sha(BUN)},
                              os.path.basename(DAM): {"que": "Damodaran margin.xls (enero 2026, asset 766892761), hoja «Industry Averages», copia de texto; fila 39 Engineering/Construction (Palancas!C7). XLS original al lado (25b04fce…).", "sha256": sha(DAM)}})}
reg["extractor_orquestacion"] = EXT
reg["fecha_orquestacion"] = HOY
reg["nota_de_la_orquestacion"] = (
    f"{HOY}, {EXT}: registro de vinci_b desde el del extractor Mistral (mistral/examen-vinci-entradas @ 737a8d8, sha256 {reg_sha}) con las correcciones de la revisión "
    "independiente del registro (coordinacion/cierre_v2/examen/vinci/revision_registro/REVISION.md y .tsv), adaptado a los valores actuales de vinci_b (plantilla regenerada "
    f"sobre el libro V6.3.2 F1: 326 entradas, 11 nuevas de la normalización del circulante). {len({c['celda'] for c in CAMBIOS})} entradas cambiadas o nuevas, con extractor "
    "«Claude orquestación»; las demás conservan a Mistral. Todas pendientes de revisor (sin sellar). Las 19 celdas de hipótesis vacías antes de la fase A llevan una entrada "
    "que dice que aún no hay hipótesis; las 11 con valor, el fundamento heredado de la etapa 1. Rastro: resultados/registro_entradas_vinci_b.json.")
salida_reg = os.path.join(C, VE.REGISTRO)
assert not os.path.exists(salida_reg)
open(salida_reg, "w", encoding="utf-8").write(json.dumps(reg, ensure_ascii=False, indent=1) + "\n")
json.dump({"fecha": HOY, "autor": EXT, "guion": "resultados/scripts/registro_entradas_vinci_b.py", "origen": "mistral/examen-vinci-entradas @ 737a8d8: resultados_examen/vinci/verificacion_entradas.json",
           "origen_sha256": reg_sha, "plantilla_huella_entradas": plant["huella_entradas_economicas"], "registro_sha256": hashlib.sha256(open(salida_reg, "rb").read()).hexdigest(),
           "cambiadas": len({c["celda"] for c in CAMBIOS}), "auxiliares_con_cita": n_aux, "hipotesis_con_valor": con_valor, "hipotesis_vacias": vacias, "cambios": CAMBIOS},
          open(SALIDA, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"{len({c['celda'] for c in CAMBIOS})} entradas cambiadas o nuevas → {salida_reg}")
