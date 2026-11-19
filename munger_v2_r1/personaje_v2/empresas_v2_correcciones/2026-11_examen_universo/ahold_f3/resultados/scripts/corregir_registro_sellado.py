#!/usr/bin/env python3
"""ahold_f3 · correcciones de cita y clase del registro de entradas (verificacion_entradas.json) que pide el sellado
(munger-v2-evidencias-mistral, coordinacion/cierre_v2/examen/ahold/revision_registro/REVISION_SELLADO.md, 787ad6f/909d279). Solo el registro: el libro,
las fases y el pipeline no se tocan. Extractor «Claude orquestación»; cada entrada corregida queda PENDIENTE de otro revisor (sin vínculo). Las demás
conservan su sello si `comprobar` mantiene su vínculo. Historia!C22 y D22 NO se tocan (lo decide la persona responsable).
Uso: python3 -I corregir_registro_sellado.py CARPETA_EMPRESA CARPETA_ANTECEDENTES REGISTRO_CAMBIOS.json"""
import copy, hashlib, json, os, re, shutil, sys
C, ANT, REG = sys.argv[1:4]
p = os.path.join(C, "verificacion_entradas.json")
h = lambda x: hashlib.sha256(open(x, "rb").read()).hexdigest()  # noqa: E731
bk = os.path.join(ANT, "verificacion_entradas_antes_de_correccion_sellado.json")
assert not os.path.exists(bk)
shutil.copy2(p, bk)
d = json.load(open(p, encoding="utf-8"))
E = {e["celda"]: e for e in d["entradas"]}
HOY = "2026-11-19"
cambios = []


def pendiente(e, nota):
    antes = copy.deepcopy(e)
    c0 = e.get("comprobacion") or {}
    e["comprobacion"] = {"extractor": "Claude orquestación", "revisor": None, "fecha": HOY, "resultado": "pendiente", "fuente_examinada": None,
                         "nota": f"[Claude orquestación, {HOY}] {nota} · Comprobación anterior: {c0.get('revisor')} {c0.get('fecha')} «{c0.get('resultado')}»: {str(c0.get('nota'))[:400]}", "vinculo": None}
    cambios.append({"celda": e["celda"], "antes": antes, "despues": e})


def plantilla(archivo):
    for x in d["entradas"]:
        f = x.get("fuente") or {}
        if f.get("archivo") == archivo and f.get("sha256"):
            return {k: f[k] for k in ("documento", "version", "archivo", "sha256")}
    raise SystemExit(f"sin plantilla de fuente para {archivo}")


def linea(archivo, pg, s):
    t = open(os.path.join(C, archivo), encoding="utf-8").read()
    m = re.split(r"\[PDF PAGE (\d+)\]\n", t)
    ls = [x.strip() for x in {int(m[i]): m[i + 1] for i in range(1, len(m), 2)}[pg].splitlines() if x.strip().startswith(s)] or [x.strip() for x in {int(m[i]): m[i + 1] for i in range(1, len(m), 2)}[pg].splitlines() if s in x]
    assert ls, (archivo, pg, s)
    return ls[0]


# 1) folios y periodo
for c, e in E.items():
    f = e.get("fuente") or {}
    fx = {("texto/AD_annual-report-2019.txt", 125, 110): 124, ("texto/AD_annual-report-2018.txt", 160, 281): 160, ("texto/AD_annual-report-2017.txt", 147, 54): 147,
          ("texto/AD_q2-2026-interim-report.txt", 15, 30): 15}.get((f.get("archivo"), f.get("pagina"), f.get("folio")))
    if fx is None or c == "Historia!D23":   # D23 cambia de clase abajo
        continue
    f["folio"] = fx
    msg = f"folio corregido al impreso ({fx})"
    if c == "aux:Q2-2026_p15_cfo_hy2026":
        f["periodo"] = "1S 2026 (semestre cerrado el 28-jun-2026)"; msg += "; periodo: el semestre cerrado el 28-jun-2026, no «12 meses»"
    if c == "aux:Q2-2026_p15_cfo_hy2025":
        f["periodo"] = "1S 2025 (semestre comparativo, cerrado el 29-jun-2025)"; msg += "; periodo del semestre comparativo"
    pendiente(e, msg + " (REVISION_SELLADO.md de Ahold)")
# 2) C23 y D23: NIC 17 → no_aplicable
for c, anio in (("Historia!C23", 2016), ("Historia!D23", 2017)):
    e = E[c]; assert e["valor_modelo"] == 0
    e["clase"] = "no_aplicable"; e["fuente"] = {}
    e["justificacion"] = (f"El libro guarda 0 por ausencia de la partida: el ejercicio {anio} está en NIC 17, sin pasivo por arrendamientos NIIF 16, y la información anterior al "
                          "30-dic-2018 no se reexpresó («Financial information prior to December 30, 2018, has not been restated for the impact of the implementation of IFRS 16 Leases», "
                          "texto/AD_annual-report-2025.txt [PDF PAGE 65], nota 1). Los arrendamientos financieros NIC 17 están en la fila 22 (deuda), cuya definición decide la persona "
                          "responsable (REVISION_SELLADO.md, C22/D22). La cita anterior («Finance lease liabilities (517) …», asignación del precio de compra de Delhaize) no probaba el cero.")
    pendiente(e, "cero con cita que no lo probaba → no_aplicable (NIC 17; AR2025 PDF p. 65, nota 1)")
# 3) minoritarios
for c, arch, pg, per in (("Historia!G26", "texto/AD_annual-report-2021.txt", 180, "ejercicio 2020 (columna comparativa del informe 2021)"),
                         ("Historia!H26", "texto/AD_annual-report-2022.txt", 190, "ejercicio 2021 (columna comparativa del informe 2022)"),
                         ("Historia!K26", "texto/AD_annual-report-2025.txt", 212, "ejercicio 2024 (columna comparativa del informe 2025)")):
    e = E[c]; assert e["clase"] == "cero_comprobado" and e["valor_modelo"] == 0
    f = e["fuente"]; f.update(plantilla(arch))
    f.update({"pagina": pg, "folio": None, "cita": linea(arch, pg, "Non-controlling interests"), "ubicacion": "cuenta de resultados consolidada (resultado atribuido)",
              "concepto": "resultado atribuido a minoritarios: «—» en los dos ejercicios (sin minoritarios)", "periodo": per, "valor_fuente": 0,
              "reexpresado": "columna comparativa del informe siguiente"})
    pendiente(e, "cita: «Non-controlling interests — —» de la cuenta de resultados del informe siguiente (antes, una fila de otro año del estado de cambios en el patrimonio)")
DER = {"Historia!D26": (2017, ("texto/AD_annual-report-2018.txt", 43, "Group equity", 15170), ("texto/AD_annual-report-2018.txt", 91, "Equity attributable to common shareholders", 15170)),
       "Historia!E26": (2018, ("texto/AD_annual-report-2019.txt", 40, "Group equity", 14205), ("texto/AD_annual-report-2019.txt", 123, "Equity attributable to common shareholders", 14205)),
       "Historia!F26": (2019, ("texto/AD_annual-report-2020.txt", 67, "Group equity", 14083), ("texto/AD_annual-report-2020.txt", 147, "Equity attributable to common shareholders", 14083))}
nuevas = []
for c, (anio, ge, ea) in DER.items():
    e = E[c]; assert e["valor_modelo"] == 0
    orig = []
    for (arch, pg, s, v), clave in ((ge, "group_equity"), (ea, "equity_attributable_to_common_shareholders")):
        a = {"celda": f"aux:{os.path.basename(arch)[:-4]}_p{pg}_{clave}_{anio}", "id": "aux", "ambito": None, "uso": None, "material": True, "clase": "dato_publicado",
             "valor_modelo": v, "fuente": dict(plantilla(arch), pagina=pg, folio=None, ubicacion="balance o resumen de la posición financiera consolidada", concepto=s,
                                                columna=f"{anio} (columna comparativa del informe siguiente)", periodo=f"cierre del ejercicio {anio}", unidad="millones de euros",
                                                escala=1, signo=1, tratamiento="cifra publicada, sin transformación", perimetro="consolidado",
                                                reexpresado="columna comparativa del informe siguiente", valor_fuente=v, cita=linea(arch, pg, s)),
             "derivacion": None, "hipotesis": None, "justificacion": None,
             "comprobacion": {"extractor": "Claude orquestación", "revisor": None, "fecha": HOY, "resultado": "pendiente", "fuente_examinada": None,
                              "nota": f"[Claude orquestación, {HOY}] origen nuevo de {c} (minoritarios = Group equity − patrimonio atribuible)", "vinculo": None}, "incidencia": None}
        assert a["celda"] not in E, a["celda"]
        nuevas.append(a); orig.append(a["celda"]); cambios.append({"celda": a["celda"], "antes": None, "despues": a})
    e["clase"] = "derivado"; e["fuente"] = {}
    e["derivacion"] = {"origenes": orig, "formula": f'o["{orig[0]}"] - o["{orig[1]}"]',
                       "conciliacion": f"minoritarios {anio} = Group equity {ge[3]:,} − patrimonio atribuible a los accionistas {ea[3]:,} = 0 (sin línea de minoritarios en el balance)".replace(",", "."),
                       "unidad": "millones de euros"}
    pendiente(e, "cero con cita que no lo probaba → derivado 0 = Group equity − patrimonio atribuible (REVISION_SELLADO.md)")
d["entradas"] += nuevas
# 4) fila 19 (I+D)
for col in "CDEFGHIJKL":
    e = E[f"Historia!{col}19"]; assert e["clase"] == "dato_ausente"
    e["justificacion"] = ("La fila 19 del libro es «I+D (gasto del año)» (partida «id» de fase1_v63.json) y queda vacía: los informes anuales 2016–2025 de Ahold Delhaize no cifran un gasto de "
                          "investigación y desarrollo (distribución alimentaria); no hay dato publicado que contrastar. Vacío no es cero.")
    pendiente(e, "justificación corregida: la fila es I+D, no deterioros")
# 5) etiquetas de juicio → convención
for c, fila in (("Análisis!C28", 33), ("Análisis!C31", 36 - 2), ("Análisis!C34", 39 - 2)):
    e = E[c]; prev = e.get("justificacion")
    e["clase"] = "convencion"
    e["hipotesis"] = {"identificacion": f"V-{c.split('!')[1]}", "fundamento": f"Etiqueta de juicio de la etapa 1 tal como la documenta el libro (Control maestro, fila de {c}); apoyo: {prev}",
                      "alternativas": "la etiqueta depende del umbral o de la lectura de la regla que documenta la etapa 1 (ver datos_v63.md)", "limites": "etiqueta informativa; no es una cifra publicada",
                      "procedencia": "Control maestro del libro (Ahold_v63_evaluada.xlsx) y datos_v63.md"}
    e["justificacion"] = None
    e["justificacion_clase"] = f"Etiqueta de texto con valor en el libro («{e['valor_modelo']}»): convención de la etapa 1, no un dato publicado ni un dato ausente (REVISION_SELLADO.md; precedente jumbo_e C28)."
    pendiente(e, "clase dato_ausente → convención con su fundamento (etiqueta con valor)")
e = E["Palancas!A30"]
e["clase"] = "convencion"; e["justificacion"] = None
e["hipotesis"] = {"identificacion": "V-A30", "fundamento": ("El informe 2025 (nota 6, texto/AD_annual-report-2025.txt [PDF PAGE 224]) solo separa The Netherlands, The United States y Rest of world (19.371 mm EUR); "
                                                          "la etiqueta «Región · Western Europe» para Rest of world es una asignación de la etapa 1, no un dato publicado. Rest of world incluye Bélgica y Luxemburgo, "
                                                          "Chequia, Rumanía (Profi), Grecia y Serbia; el informe no publica qué parte es de cada país."),
                  "alternativas": "repartir Rest of world entre Europa occidental y Europa central y oriental si se publicara el desglose; con otra región cambia la prima de riesgo país y la r mínima de la fase A",
                  "limites": "la afirmación anterior de que Bélgica es «la mayor parte» no tiene fuente y se retira", "procedencia": "Palancas!A30 del libro"}
e["justificacion_clase"] = "Etiqueta asignada (convención de la etapa 1), no un no_aplicable con valor (REVISION_SELLADO.md)."
pendiente(e, "clase no_aplicable → convención; se retira la afirmación sin fuente sobre Bélgica")
# 6) C24 con la definición LTM del libro
e = E["Análisis!C24"]
oi26, oi25 = "aux:Q2-2026_p11_operating_income_hy2026", "aux:Q2-2026_p11_operating_income_hy2025"
assert oi26 in E and oi25 in E
e["derivacion"] = {"origenes": ["Historia!L7", oi26, oi25, "Historia!L21", "Historia!L22", "Historia!L23"],
                   "formula": f'round((o["Historia!L7"] + o["{oi26}"] - o["{oi25}"]) / (o["Historia!L21"] + o["Historia!L22"] + o["Historia!L23"]), 3)',
                   "conciliacion": ("ROCE antes de impuestos IFRS con fondo de comercio, LTM a 28-jun-2026 (definición de Control maestro fila 29): resultado operativo LTM = 3.542 + 1.760 − 1.741 = 3.561 "
                                    "(Q2-2026 PDF p. 11) ÷ capital empleado al último cierre auditado (patrimonio 14.195 + deuda 6.429 + arrendamientos 11.974 = 32.598, Historia 2025) = 0,10924 → 0,109 = libro. "
                                    "La etapa 1 no documenta la fecha del denominador: con el balance del 28-jun-2026 (14.445 + 19.261) saldría 0,106; queda para el revisor."),
                   "unidad": None}
pendiente(e, "fórmula con el resultado operativo LTM (definición del libro) en lugar del EBIT de 2025; el denominador es el capital empleado al cierre de 2025 (fecha no documentada por la etapa 1)")
d["nota_del_extractor"] = str(d.get("nota_del_extractor") or "") + f" ({HOY}) Claude orquestación corrigió {len(cambios)} entradas de cita o clase que pedía el sellado (resultados/registro_cambios_sellado_ahold_f3.json); quedan pendientes de otro revisor. C22/D22 sin tocar."
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
json.dump({"fecha": HOY, "guion": os.path.abspath(__file__), "registro_antes_sha256": h(bk), "registro_despues_sha256": h(p), "entradas": [x["celda"] for x in cambios], "cambios": cambios},
          open(REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
print("corregidas", len(cambios))
