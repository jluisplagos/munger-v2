#!/usr/bin/env python3
"""P-M1 · inversión de reposición de Vidrala frente a la amortización que usa el modelo (entrega 4.8, encargo §3).
Solo lectura del expediente de referencia, de los textos y PDF conservados y del código de la 4.7.1.

Uso: python3 -I analisis_pm1.py [--salida DIR]   (escribe ../financiero/pm1_* o DIR; código 1 si una evidencia no se reproduce o un control falla)

1. RÉPLICA. Se ejecuta SIN CAMBIOS el modelo auxiliar de la 4.7.1 (…_4_7_1/scripts/analisis_n1_n3.py) en una copia temporal, con
   sus mismas entradas, y se exige que sus salidas (matriz.csv, sensibilidades_n3.csv, n3_anio_a_anio.csv) sean idénticas byte a
   byte a las del paquete. Así la referencia T1·M1·R1 (ponderado 69,2447; precio de Sí 64,2622) y las sensibilidades de la 4.7.1
   se reproducen antes de introducir ninguna alternativa.
2. EVIDENCIA. Cada dato se vuelve a extraer de los textos conservados (CF_AAAA.txt del expediente de referencia, versión inglesa) y
   del PDF español conservado de 2025 (contrastes/piloto_Vidrala_2025/…/2308…pdf, que incluye el informe de gestión y el informe
   de sostenibilidad), con archivo, página, patrón y valor; si un dato no se reproduce, código 1. Las fuentes externas (CNMV y
   secundarias) están en ../fuentes/fuentes_externas_pm1.json: no se reproducen aquí porque sus PDF no están en el paquete.
3. CONCILIACIÓN por año (2016–2025) y por segmento (2018–2025): inversión, amortización, ratio, perímetro, bienes totalmente
   amortizados en uso y notas de definición.
4. ALTERNATIVAS (fundamentos fijados en ALTERNATIVAS antes de calcular valores), todas sobre T1·M1·R1 y con r = 0,09,
   probabilidades 0,2/0,6/0,2, k = 3, caja 108,352 y puente 160,784 sin cambios:
   REF  referencia de la 4.7.1 (mantenimiento = D&A).
   P0   corrección de la amortización de la cartera de clientes (no se repone).
   P1   reposición a coste corriente λ × D&A repuesta, con la regla del hueco (sin doble cómputo con ΔV ÷ S2C ni con g ÷ ROIC); λ
        central 1,15 y extremos 1,10 y 1,25; con P0.
   P1s  estructura alternativa de P1: S2C reestimado sin el exceso de reposición y reposición explícita en los diez años.
   P2   ola de reconstrucción 2026–2027 (información posterior a la base y secundaria), sobre P1 central, con escudo fiscal diferido.
   P3   P1 central con la capacidad no conservada en el MALO (la recuperación paga ΔV ÷ S2C completo).
   P4   combinación adversa: λ = 1,25, ola de reconstrucción y capacidad no conservada.
   P5   exceso estructural en nivel (media 2021–2025; P5x, el de 2025) con la regla del hueco.
   P6   suelo de inversión bruta en % de las ventas (media 2016–2025; previsión oficial de 2025, 12 %; nivel de 2025 perpetuo), con hueco.
   Correcciones tras la auditoría interna: el hueco de P3/P4 solo descuenta la inversión fija de R1 (Z-c); P5 mide el exceso frente a la
   amortización que se repone cuando aplica P0 (Z-d); P6i, fundamentado en la previsión oficial (Z-l); --salida para el control (Z-i).
   X41  la sensibilidad de la 4.7.1 «+41,8 % de D&A en todos los escenarios», con su doble cómputo cuantificado.
   P5 y P6, y λ central 1,15 (antes 1,10), se añadieron tras la crítica independiente con Fable (REGISTRO_ENTREGA_4.8.md, §4).
Ningún valor es una previsión, una cota ni una comparación con la cotización; son resultados mecánicos de un ensayo.
"""
import contextlib
import csv
import hashlib
import importlib.util
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

AQUI = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CORR = os.path.dirname(AQUI)
RAIZ_PAQ = os.path.abspath(os.path.join(CORR, "..", ".."))
REF = os.path.join(CORR, "2026-11_Vidrala_ensayo_4_6_1", "Vidrala")
TXT = os.path.join(REF, "texto")
M471 = os.path.join(CORR, "2026-11_Vidrala_ensayo_4_7_1")
PDF_ES = os.path.join(RAIZ_PAQ, "contrastes", "piloto_Vidrala_2025", "fuentes", "es_2308_descarga_2026-11-08", "2308_es-informacion_financiera_consolidada_2025.pdf")
PDF_ES_SHA = "29fd6a299d37270279195e8eb194820869a1bb2c513dd6a646963034698f14e7"
SAL = os.path.join(AQUI, "financiero")
if "--salida" in sys.argv:  # (Z-i) el control escribe en un temporal y compara con las salidas del paquete
    SAL = os.path.abspath(sys.argv[sys.argv.index("--salida") + 1])
os.makedirs(SAL, exist_ok=True)
LOG = []
FALLOS = []


def log(s=""):
    LOG.append(s)
    print(s)


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


# ------------------------------------------------------------------ 1. réplica de la 4.7.1, sin cambios, en una copia temporal
TMP = tempfile.mkdtemp(prefix="pm1_")
SALIDA_471 = None
try:
    corr_tmp = os.path.join(TMP, "corr")
    os.makedirs(os.path.join(corr_tmp, "x471", "scripts"))
    for d in ("2026-11_Vidrala_ensayo_4_6_1", "2026-11_Vidrala_ensayo_4_7"):
        os.symlink(os.path.join(CORR, d), os.path.join(corr_tmp, d))
    src = os.path.join(M471, "scripts", "analisis_n1_n3.py")
    shutil.copy(src, os.path.join(corr_tmp, "x471", "scripts", "analisis_n1_n3.py"))
    spec = importlib.util.spec_from_file_location("a471", os.path.join(corr_tmp, "x471", "scripts", "analisis_n1_n3.py"))
    A = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()):
        try:
            spec.loader.exec_module(A)
        except SystemExit as e:  # el guion de la 4.7.1 termina con sys.exit(0 si sus controles cumplen)
            SALIDA_471 = e.code
    iguales = {f: sha(os.path.join(corr_tmp, "x471", "financiero", f)) == sha(os.path.join(M471, "financiero", f))
               for f in ("matriz.csv", "sensibilidades_n3.csv", "n3_anio_a_anio.csv", "evidencia.json")}
    CONTROL_REPLICA = all(iguales.values()) and A.control and SALIDA_471 in (0, None)
finally:
    shutil.rmtree(TMP, ignore_errors=True)
CODIGO_471_SHA = sha(os.path.join(M471, "scripts", "analisis_n1_n3.py"))

T1, M1 = A.T_REC, A.M_REC
ESC, PROB, V0, ACC, PUENTE, DA25, NWC = A.ESC, A.PROB, A.V0, A.ACC, A.PUENTE, A.DA25, A.NWC_RATIO
R_OP = A.r_op(T1)
NOMBRES = ("MALO", "NORMAL", "BUENO")


# ------------------------------------------------------------------ 2. evidencia
EV = []


def _paginas_txt(f):
    t = open(os.path.join(TXT, f), encoding="utf-8").read()
    partes = re.split(r"\[PDF PAGE (\d+)\]", t)
    return {int(partes[i]): partes[i + 1] for i in range(1, len(partes), 2)}


_CACHE = {}


def paginas(fuente):
    if fuente not in _CACHE:
        if fuente == "ES_2025":
            if sha(PDF_ES) != PDF_ES_SHA:
                FALLOS.append("huella del PDF español de 2025 distinta de la conservada")
            out = subprocess.run(["pdftotext", "-layout", PDF_ES, "-"], capture_output=True, text=True).stdout
            _CACHE[fuente] = {i + 1: p for i, p in enumerate(out.split("\f"))}
        else:
            _CACHE[fuente] = _paginas_txt(fuente)
    return _CACHE[fuente]


def num(s):
    s = s.strip()
    neg = s.startswith("(") or s.startswith("-") or s.startswith("−")
    s = re.sub(r"[()\s−-]", "", s)
    return -float(s.replace(",", "").replace(".", "")) if neg else float(s.replace(",", "").replace(".", ""))


def ev(clave, fuente, pagina, patron, esperado, concepto, periodo, perimetro, unidad="miles de euros", grupo=1, texto=False, nota=""):
    """Busca `patron` (expresión regular sobre el texto de la página con los espacios normalizados) y compara el grupo `grupo` con
    `esperado` (número, o texto si texto=True). Registra la línea, la página y si se reproduce. Devuelve el valor esperado."""
    pags = paginas(fuente)
    cand = [pagina] if pagina else sorted(pags)
    for pg in cand:
        n = re.sub(r"\s+", " ", pags.get(pg, ""))
        m = re.search(patron, n)
        if m:
            visto = m.group(grupo)
            ok = (visto.strip() == esperado) if texto else abs(num(visto) - esperado) < 0.5
            EV.append({"clave": clave, "archivo": "PDF 2308 (español, 2025; conservado)" if fuente == "ES_2025" else fuente, "pagina_pdf": pg,
                       "extracto": n[max(0, m.start() - 40):m.end() + 40][:240], "concepto": concepto, "periodo": periodo, "perimetro": perimetro,
                       "unidad": unidad, "valor": visto.strip(), "esperado": esperado, "reproduce": ok, "nota": nota})
            if not ok:
                FALLOS.append(clave)
            return esperado
    EV.append({"clave": clave, "archivo": fuente, "pagina_pdf": pagina, "reproduce": False, "nota": "no encontrado"})
    FALLOS.append(clave)
    return esperado


ES = "ES_2025"
N = r"(\(?[\d.,]+\)?)"
# --- 2025: amortización por componentes (X-e directo en el PDF) y arrendamientos
ROU25 = ev("rou_dep_2025", ES, 58, r"Depreciación de derechos de uso " + N, 6760, "Depreciación de derechos de uso (cuenta de resultados)", "2025", "continuadas",
           nota="X-e: la cifra de 2025 es 6.760; la de 2024, 4.768 (misma línea)")
ROU24 = ev("rou_dep_2024", ES, 58, r"Depreciación de derechos de uso [\d.]+ " + N, 4768, "Depreciación de derechos de uso", "2024 (comparativo)", "continuadas")
ROU25_EN = ev("rou_dep_2025_en", "CF_2025.txt", None, r"Depreciation of right-of-use assets " + N, 6760, "Depreciation of right-of-use assets (versión inglesa)", "2025", "continuadas")
LEASE_ADD = ev("arrend_altas_2025", ES, 58, N + r" 1\.429 Gastos financieros devengados", 2404, "Altas de pasivos por arrendamiento", "2025", "continuadas")
LEASE_OTR = ev("arrend_otros_2025", ES, 58, r"Otros " + N + r" — Diferencias", 9596, "Otros movimientos del pasivo por arrendamiento (actualización de tarifas)", "2025", "continuadas")
LEASE_PAG = ev("arrend_pagos_2025", ES, 58, r"Pagos \(([\d.]+)\) \(6\.117\)", 8314, "Pagos por arrendamientos", "2025", "continuadas")
CL25 = ev("cartera_amort_2025", ES, 52, r"Altas \(677\) - \(2\.671\) \(73\) \(([\d.]+)\)", 4492, "Amortización de la cartera de clientes (Vidroporto)", "2025", "grupo")
INT25 = ev("intangibles_amort_2025", ES, 52, r"Altas \(677\) - \(2\.671\) \(73\) \([\d.]+\) \(([\d.]+)\)", 7913, "Amortización de activos intangibles (total)", "2025", "grupo")
CL_VNC = ev("cartera_vnc_2025", ES, 52, r"Saldos al 31 de 1\.501 52\.137 21\.773 327 ([\d.]+) 258\.793", 21858, "Valor neto contable de la cartera de clientes a 31-dic-2025", "31-dic-2025", "grupo")
CL24 = ev("cartera_amort_2024", ES, 53, r"Altas \(587\) - \(3\.009\) - \(([\d.]+)\)", 4921, "Amortización de la cartera de clientes", "2024", "grupo")
INT_ALTAS = ev("intangibles_altas_2025", ES, 52, r"Altas 433 37\.661 6\.830 249 - ([\d.]+)", 45173, "Altas de activos intangibles (incluye derechos de emisión)", "2025", "grupo")
EMIS_ALTAS = ev("derechos_emision_altas_2025", ES, 52, r"Altas 433 ([\d.]+) 6\.830", 37661, "Altas de derechos de emisión (asignación; no es inversión)", "2025", "grupo")
# --- 2025: inmovilizado material
PPE_ALTAS = ev("ppe_altas_2025", ES, 49, r"2\.088\.264 ([\d.]+) \(36\.070\)", 177848, "Altas de inmovilizado material", "2025", "grupo")
PPE_DOT = ev("ppe_dotacion_2025", ES, 49, r"\(959\.577\) \(([\d.]+)\)", 118275, "Dotación a la amortización del inmovilizado material", "2025", "grupo")
PPE_COSTE = ev("ppe_coste_2025", ES, 49, r"\(35\.814\) ([\d.]+)", 2194513, "Coste bruto del inmovilizado material a 31-dic-2025", "31-dic-2025", "grupo")
PPE_AA = ev("ppe_amort_acum_2025", ES, 49, r"17\.085 \(([\d.]+)\)", 1026815, "Amortización acumulada a 31-dic-2025", "31-dic-2025", "grupo")
PPE_DET = ev("ppe_deterioro_2025", ES, 49, r"\(2\.362\) - - - - \(([\d.]+)\)", 32569, "Deterioro acumulado a 31-dic-2025", "31-dic-2025", "grupo")
PPE_CURSO = ev("ppe_en_curso_2025", ES, 49, r"materiales en curso 2\.088\.264|195\.202 116\.817 \(2\.118\) - \(99\.982\) \(1\.381\) ([\d.]+)", 208538, "Inmovilizado en curso a 31-dic-2025", "31-dic-2025", "grupo")
PPE_TERR = ev("ppe_terrenos_construcciones_2025", ES, 49, r"\(7\.563\) ([\d.]+)", 405812, "Coste de terrenos y construcciones a 31-dic-2025", "31-dic-2025", "grupo")
ev("texto_renovacion_hornos_2025", ES, 50, r"(principalmente, en renovación de hornos)", "principalmente, en renovación de hornos", "Destino de las principales altas 2024–2025", "2024–2025", "España, Portugal y Reino Unido", "texto", texto=True)
COMP25 = ev("compromisos_2025", ES, 51, r"Instalaciones técnicas y maquinaria ([\d.]+) 9\.622", 66610, "Compromisos de compra de inmovilizado", "31-dic-2025", "grupo")
SUBV = ev("subvenciones_diferidas_2025", ES, 51, r"importe de ([\d.]+) miles de euros al 31 de diciembre de 2025", 23115, "Subvenciones de capital pendientes de imputar", "31-dic-2025", "grupo")
INV_SEG25 = ev("inversiones_total_2025", ES, 35, r"2\.314\.232 901\.354 ([\d.]+)", 185360, "Inversiones del ejercicio (altas de material e intangibles sin derechos de emisión)", "2025", "grupo")
REESTR = ev("reestructuracion_uk_2025", ES, 34, r"reestructuración por importe de ([\d.]+) miles", 13668, "Costes de reestructuración del segmento Reino Unido e Irlanda", "2025", "Reino Unido e Irlanda")
ev("texto_capacidad_2025", ES, 94, r"(adaptando nuestra capacidad industrial a la realidad del mercado)", "adaptando nuestra capacidad industrial a la realidad del mercado",
   "Informe de gestión: adaptación de capacidad mientras se ejecuta el plan inversor", "2025", "grupo", "texto", texto=True)
ev("texto_ventas_organicas_2025", ES, 88, r"Ventas 1\.465,2 1\.588,3 -7,8% (-5,4%)", "-5,4%", "Variación orgánica de las ventas (divisa constante y perímetro comparable)", "2025", "grupo", "texto", texto=True)
ev("texto_tres_hornos_2025", ES, 177, r"(asociados a 3 nuevos hornos)", "asociados a 3 nuevos hornos", "Sostenibilidad: reducción de emisiones por tres hornos nuevos", "2025", "grupo", "texto", texto=True)
ev("texto_paradas_hornos_2025", ES, 176, r"(paradas y arrancadas de hornos)", "paradas y arrancadas de hornos", "Sostenibilidad: paradas y arrancadas de hornos en 2025", "2025", "grupo", "texto", texto=True)
ev("texto_electrificacion", ES, 173, r"(actualmente entre un 10-15%, con nuevos hornos que incorporan una capacidad de electrificación del 25%)",
   "actualmente entre un 10-15%, con nuevos hornos que incorporan una capacidad de electrificación del 25%", "Electrificación de hornos (actual, nuevos, objetivo 40 % en 2030)", "2025", "grupo", "texto", texto=True)
ev("texto_vida_util_hornos", ES, 21, r"(Hornos, instalaciones y maquinaria de producción 8 - 16)", "Hornos, instalaciones y maquinaria de producción 8 - 16", "Vida útil contable de hornos", "2025", "grupo", "texto", texto=True)
# --- bienes totalmente amortizados en uso (coste), serie
TOT = {}
TOT[2016] = ev("totamort_2016", "CF_2017.txt", None, r"Euros \d+ million \(Euros (\d+) million at 31 December 2016\)", 182, "Coste de inmovilizado material totalmente amortizado en uso", "31-dic-2016", "publicado 2017", "millones de euros")
for y, f, pat, v in ((2017, "CF_2017.txt", r"in use amounts to Euros (\d+) million", 207), (2018, "CF_2018.txt", r"in use amounts to Euros (\d+) million", 362),
                     (2019, "CF_2019.txt", r"in use amounts to Euros (\d+) million", 408), (2020, "CF_2020.txt", r"in use amounts to Euros (\d+) million", 413),
                     (2021, "CF_2021.txt", r"in use amounts to Euros (\d+) million", 457), (2022, "CF_2022.txt", r"in use amounts to Euros (\d+) million", 500),
                     (2023, "CF_2023.txt", r"in use amounts to Euros (\d+) million", 543), (2024, "CF_2024.txt", r"with a cost of (\d+) million euros that is fully depreciated", 706),
                     (2025, "CF_2025.txt", r"cost of EUR (\d+) million that were fully depreciated", 627)):
    TOT[y] = ev(f"totamort_{y}", f, None, pat, v, "Coste de inmovilizado material totalmente amortizado en uso", f"31-dic-{y}", f"publicado {y}", "millones de euros")
# --- destino de las principales altas (texto), serie
for y, f, pat, txt in ((2017, "CF_2017.txt", r"(complete update of the production plant located in Italy)", "complete update of the production plant located in Italy"),
                       (2018, "CF_2018.txt", r"(United Kingdom \(Euros 33,733 thousand\))", "United Kingdom (Euros 33,733 thousand)"),
                       (2019, "CF_2019.txt", r"(Portugal \(Euros 20,250 thousand\) and the United Kingdom \(Euros 44,247 thousand\))", "Portugal (Euros 20,250 thousand) and the United Kingdom (Euros 44,247 thousand)"),
                       (2020, "CF_2020.txt", r"(United Kingdom \(Euros 77,801 thousand)", "United Kingdom (Euros 77,801 thousand"),
                       (2021, "CF_2021.txt", r"(United Kingdom \(Euros 32,597 thousand)", "United Kingdom (Euros 32,597 thousand"),
                       (2022, "CF_2022.txt", r"(Portugal \(Euros 94,557 thousand)", "Portugal (Euros 94,557 thousand"),
                       (2024, "CF_2024.txt", r"(primarily in the renewal of furnaces)", "primarily in the renewal of furnaces")):
    ev(f"texto_altas_{y}", f, None, pat, txt, "Destino declarado de las principales altas", str(y), f"publicado {y}", "texto", texto=True)
# --- inversiones del ejercicio y amortización por segmento (cuadros de segmentos, cifra del propio año salvo que se indique)
SEG = {}
SEG_PAT = {  # año: (archivo, {segmento: (patrón inversión, valor, patrón amortización, valor)})
    2018: ("CF_2019.txt", {"Reino Unido e Irlanda": (r"United 500,620 136,368 49,818 461,072 108,219 ([\d,]+) Kingdom", 35858, None, None)}),
    2019: ("CF_2019.txt", {"Iberia y resto": (r"Iberian 766,822 567,579 ([\d,]+)", 56371, r"Amortisation costs \(([\d,]+)\) \(8,991\)", 49311),
                            "Italia": (r"Italy 190,419 30,555 ([\d,]+)", 6003, r"Amortisation costs \([\d,]+\) \(([\d,]+)\) \(32,786\)", 8991),
                            "Reino Unido e Irlanda": (r"United 500,620 136,368 ([\d,]+)", 49818, r"Amortisation costs \([\d,]+\) \([\d,]+\) \(([\d,]+)\) \(91,088\)", 32786)}),
    2020: ("CF_2020.txt", {"Iberia y resto": (r"Other 835,574 556,599 ([\d,]+)", 79469, r"Amortisation costs \(([\d,]+)\) \(8,834\)", 44933),
                            "Italia": (r"Italy 185,061 32,173 ([\d,]+)", 4724, r"Amortisation costs \([\d,]+\) \(([\d,]+)\) \(30,377\)", 8834),
                            "Reino Unido e Irlanda": (r"Ireland 500,812 116,519 ([\d,]+)", 52178, r"Amortisation costs \([\d,]+\) \([\d,]+\) \(([\d,]+)\) \(84,144\)", 30377)}),
    2021: ("CF_2021.txt", {"Iberia y resto": (r"Other 928,243 537,574 ([\d,]+)", 73295, r"Amortisation costs \(([\d,]+)\) \(9,108\)", 41193),
                            "Italia": (r"Italy 227,922 43,637 ([\d,]+)", 7436, r"Amortisation costs \([\d,]+\) \(([\d,]+)\) \(35,983\)", 9108),
                            "Reino Unido e Irlanda": (r"Ireland 547,081 155,133 ([\d,]+)", 32597, r"Amortisation costs \([\d,]+\) \([\d,]+\) \(([\d,]+)\) \(86,284\)", 35983)}),
    2022: ("CF_2022.txt", {"Iberia y resto": (r"Other 1,213,988 723,448 ([\d,]+)", 90556, r"Amortisation costs \(([\d,]+)\) \(9,967\)", 39202),
                            "Italia": (r"Italy 217,841 42,786 ([\d,]+)", 14779, r"Amortisation costs \([\d,]+\) \(([\d,]+)\) \(36,291\)", 9967),
                            "Reino Unido e Irlanda": (r"Ireland 521,698 153,669 ([\d,]+)", 55878, r"Amortisation costs \([\d,]+\) \([\d,]+\) \(([\d,]+)\) \(85,460\)", 36291)}),
    2023: ("CF_2023.txt", {"Iberia y resto": (r"Other 1,181,098 717,688 ([\d,]+)", 109887, r"Amortisation costs \(([\d,]+)\) \(10,655\)", 43743),
                            "Italia": (r"Italy 229,277 52,430 ([\d,]+)", 4315, r"Amortisation costs \([\d,]+\) \(([\d,]+)\) \(42,552\)", 10655),
                            "Reino Unido e Irlanda": (r"Ireland 721,940 267,278 ([\d,]+)", 27619, r"Amortisation costs \([\d,]+\) \([\d,]+\) \(([\d,]+)\) \(915\)", 42552)}),
    2024: ("CF_2025.txt", {"Iberia y resto": (r"Vidrala Europe 1,170,721 511,827 [\d,]+ 1,144,646 525,930 ([\d,]+)", 118702, r"Amortisation costs \(([\d,]+)\) \(1,822\)", 51196),
                            "Reino Unido e Irlanda": (r"Ireland 703,158 264,548 [\d,]+ 726,109 262,134 ([\d,]+)", 40169, r"Amortisation costs \([\d,]+\) \(1,822\) \(([\d,]+)\)", 48920),
                            "Brasil": (r"Brazil 433,641 124,979 [\d,]+ 430,871 210,278 ([\d,]+)", 20505, r"Amortisation costs \([\d,]+\) \(1,822\) \([\d,]+\) \(([\d,]+)\)", 15782)}),
    2025: ("CF_2025.txt", {"Iberia y resto": (r"Vidrala Europe 1,170,721 511,827 ([\d,]+)", 116431, r"Amortisation costs \(([\d,]+)\) \(53,705\)", 57755),
                            "Reino Unido e Irlanda": (r"Ireland 703,158 264,548 ([\d,]+)", 46512, r"Amortisation costs \([\d,]+\) \(([\d,]+)\) \(21,488\)", 53705),
                            "Brasil": (r"Brazil 433,641 124,979 ([\d,]+)", 22417, r"Amortisation costs \([\d,]+\) \([\d,]+\) \(([\d,]+)\) \(132,948\)", 21488)}),
}
for y, (f, segs) in SEG_PAT.items():
    for s, (pi, vi, pa, va) in segs.items():
        inv = ev(f"seg_inv_{y}_{s}", f, None, pi, vi, f"Inversiones del ejercicio · {s}", str(y), s, nota="2018: comparativo reexpresado del informe 2019 (en el de 2018, 41,251)" if y == 2018 else "")
        da = ev(f"seg_da_{y}_{s}", f, None, pa, va, f"Amortización · {s}", str(y), s) if pa else None
        SEG[(y, s)] = (inv / 1000.0, None if da is None else da / 1000.0)
UK18_DA = ev("seg_da_2018_uk", "CF_2018.txt", None, r"United Kingdom & Ireland ([\d,]+) ([\d,]+) [\d,]+ [\d,]+ 86,817", 29899, "Amortización de inmovilizado material · Reino Unido e Irlanda", "2018", "Reino Unido e Irlanda")
UK18_DAi = ev("seg_da_2018_uk_int", "CF_2018.txt", None, r"United Kingdom & Ireland [\d,]+ ([\d,]+) [\d,]+ [\d,]+ 86,817", 439, "Amortización de intangibles · Reino Unido e Irlanda", "2018", "Reino Unido e Irlanda")
SEG[(2018, "Reino Unido e Irlanda")] = (SEG[(2018, "Reino Unido e Irlanda")][0], (UK18_DA + UK18_DAi) / 1000.0)
# --- definición de la amortización de 2019 en la Historia (hallazgo documental nuevo, sin corrección)
DA19_PUB = ev("da_2019_publicada", "CF_2019.txt", None, r"Amortisation and depreciation 6&7 ([\d,]+) 88,178", 91088, "Amortización 2019 (estado de flujos, informe 2019)", "2019", "publicado 2019 (con Italia)")
DET19 = ev("deterioro_2019", "CF_2020.txt", None, r"Impairment of non-current assets 6 1,415 ([\d,]+)", 6003, "Deterioro de inmovilizado 2019 (comparativo del informe 2020)", "2019", "publicado 2019 (con Italia)")

# ------------------------------------------------------------------ 3. conciliación por año y por segmento
CONC = []
for y in range(2016, 2026):
    capex, da = A.CAPEX_H[y], A.DA_H[y]
    nota = {2016: "sin Santos Barosa todo el año", 2017: "Santos Barosa desde 2017; actualización completa de Italia",
            2019: "D&A de la Historia = 91,088 + deterioro 6,003 (definición distinta de la del resto de años; ver hallazgo Y-1)",
            2020: "con Italia", 2021: "con Italia", 2022: "con Italia", 2023: "Brasil desde noviembre; Italia publicada en continuadas (CF_2023)",
            2024: "Italia vendida (2 meses); Brasil todo el año", 2025: "continuadas; apagón de abril; reestructuración en Reino Unido"}.get(y, "con Italia")
    CONC.append({"anio": y, "ventas": A.VENTAS[y], "capex_historia": capex, "da_historia": da, "capex_sobre_da": capex / da, "exceso": capex - da,
                 "totalmente_amortizado_en_uso_coste": TOT.get(y), "nota_perimetro": nota})
SEGFILAS = []
for (y, s), (inv, da) in sorted(SEG.items()):
    SEGFILAS.append({"anio": y, "segmento": s, "inversiones": inv, "amortizacion": da, "ratio": (inv / da) if da else None})
uk = [SEG[(y, "Reino Unido e Irlanda")] for y in range(2018, 2026)]
UK_CICLO = sum(i for i, _ in uk) / sum(d for _, d in uk)                         # 2018–2025, inversiones con 2018 reexpresado
UK_CICLO_PROPIO = (sum(i for i, _ in uk) - 35.858 + 41.251) / sum(d for _, d in uk)  # con la cifra de 2018 del propio informe 2018
ib = [SEG[(y, "Iberia y resto")] for y in range(2019, 2026)]
IB_RATIO = sum(i for i, _ in ib) / sum(d for _, d in ib)
DEPREC_ACTIVO = (PPE_COSTE - PPE_CURSO - TOT[2025] * 1000) / PPE_DOT  # años: coste aún en amortización (incluye terrenos) ÷ dotación


# ------------------------------------------------------------------ 4. alternativas
def lam(L, pi):
    """Cociente reposición ÷ amortización en estado estacionario con capacidad real constante, vida contable L e inflación de los
    bienes de equipo pi: la amortización lineal de coste histórico va por detrás del coste corriente de reponer."""
    return 1.0 / (sum((1 + pi) ** (-k) for k in range(L)) / L)


LAM_C, LAM_B, LAM_A = 1.15, 1.10, 1.25  # tras la crítica independiente (Fable): central 1,15 y rango 1,10–1,25 (§3 del informe)
LAM_BALANCE = {pi: 1 + pi * (PPE_COSTE - PPE_AA - PPE_DET) / PPE_DOT for pi in (0.02, 0.03)}  # 1 + π × valor neto ÷ dotación (incluye terrenos y obra en curso)
EXCESO_2025 = A.CAPEX_H[2025] - A.DA_H[2025]
EXCESO_MEDIO = sum(A.CAPEX_H[y] - A.DA_H[y] for y in range(2021, 2026)) / 5
# (4.8, Z-d de la auditoría interna) con P0 el exceso se mide frente a la amortización que se repone (sin la cartera de clientes:
# 4,921 en 2024 y 4,492 en 2025; la de 2023, dos meses de Vidroporto, no se publica por separado y se toma 0)
CART_Y = {2024: CL24 / 1000.0, 2025: CL25 / 1000.0}
EXCESO_MEDIO_PROPIO = sum(A.CAPEX_H[y] - (A.DA_H[y] - CART_Y.get(y, 0.0)) for y in range(2021, 2026)) / 5
EXCESO_2025_PROPIO = A.CAPEX_H[2025] - (A.DA_H[2025] - CART_Y[2025])
INV_VENTAS = {y: A.CAPEX_H[y] / A.VENTAS[y] for y in range(2016, 2026)}
INV_VENTAS_MEDIA = sum(INV_VENTAS.values()) / 10
CL = [min(CL25 / 1000.0, max(0.0, CL_VNC / 1000.0 - CL25 / 1000.0 * k)) for k in range(10)]  # amortización de la cartera que queda, años 1–10
ALTERNATIVAS = {
    "REF": "referencia 4.7.1 (T1·M1·R1; reposición = D&A en los tres escenarios y en el terminal)",
    "P0": "P0 · la amortización de la cartera de clientes de Vidroporto (4,492 en 2025; valor neto 21,858) no se repone: el modelo la cobra como inversión; se suma al FCF mientras dura (≈ 4,9 años). Dato publicado; efecto menor y favorable",
    "P1": f"P1 · reposición a coste corriente = λ × (D&A − cartera) con λ = {LAM_C:.2f} (indicios: desfase de inflación λ(12 años; 2 %) = {lam(12, 0.02):.3f} y λ(12; 3 %) = {lam(12, 0.03):.3f}; balance 1 + π × valor neto ÷ dotación = {LAM_BALANCE[0.02]:.3f} al 2 % y {LAM_BALANCE[0.03]:.3f} al 3 %; ciclo del Reino Unido 2018–2025 {UK_CICLO:.3f}–{UK_CICLO_PROPIO:.3f}, débil por perímetro; central elevado de 1,10 a 1,15 tras la crítica independiente). Regla del hueco: se añade solo max(0, (λ−1)·(D&A − cartera) − inversión fija neta del modelo), cada año y en el terminal (año 11, con D&A proporcional a las ventas), para no cobrar dos veces lo que ΔV ÷ S2C o g ÷ ROIC ya reinvierten. Sin escudo fiscal adicional (en estado estacionario el desfase no se recupera). Con P0",
    "P1b": f"P1 con λ = {LAM_B:.2f} (cerca del mínimo de los indicios: Reino Unido 1,095–1,113 y λ(12; 2 %) = 1,112; λ(10; 1 %) = {lam(10, 0.01):.3f} queda por debajo): extremo bajo explorado, no cota",
    "P1a": f"P1 con λ = {LAM_A:.2f} (λ(16; 3 %) = {lam(16, 0.03):.3f}; balance al 3 %): extremo alto explorado, no cota",
    "P1s": "P1s · estructura alternativa: S2C de la fase B multiplicado por el cociente entre el S2C marginal de la Historia sin el exceso de reposición en el denominador y el C53 (0,9159), y reposición explícita (λ−1)·(D&A − cartera) en los diez años de los tres escenarios; terminal con la regla del hueco. Con P0",
    "P2": "P2 · ola de reconstrucción 2026–2027 sobre P1: inversión bruta del año 1 = 180 (2026; la dirección habló de 170–189 en la conferencia de resultados: fuente secundaria y posterior a la base), año 2 a mitad de camino hacia la de P1; el exceso se amortiza en 12 años con escudo fiscal al tipo T1. Hipótesis condicionada",
    "P3": "P3 · P1 con la capacidad no conservada en el MALO (la recuperación paga ΔV ÷ S2C completo): Reino Unido adaptó su capacidad en 2025 con una reestructuración de 13,668. La regla del hueco solo descuenta la inversión fija de R1 (Z-c)",
    "P4": f"P4 · combinación adversa coherente: λ = {LAM_A:.3f}, ola de reconstrucción (P2) y capacidad no conservada en el MALO (P3)",
    "X41": "X41 · sensibilidad de la 4.7.1: +41,8 % de D&A en todos los escenarios y en el terminal, sin regla del hueco (para cuantificar su doble cómputo)",
    "P5": f"P5 · exceso estructural en nivel con la regla del hueco: el exceso medio 2021–2025 de la inversión sobre la amortización que se repone ({EXCESO_MEDIO_PROPIO:.1f} M€/año; {EXCESO_MEDIO:.1f} con la amortización total) se mantiene en los diez años (y en el terminal, proporcional a las ventas), descontando la inversión fija neta que el modelo ya paga. Supone que el exceso depende de reponer y conservar competitividad, no del crecimiento. Con P0",
    "P5x": f"P5 con el exceso de 2025 sobre la amortización que se repone ({EXCESO_2025_PROPIO:.1f} M€/año): el nivel de inversión de 2025 en el año 1 (después, el exceso constante con hueco). Con P0",
    "P5x0": f"P5 con el exceso de 2025 sobre la amortización total ({EXCESO_2025:.1f} M€/año) y sin P0: la parte de X41 que no es doble cómputo (solo para medirla)",
    "P6m": f"P6 · suelo de inversión bruta de caja = {INV_VENTAS_MEDIA:.1%} de las ventas (media 2016–2025 de la Historia), con la regla del hueco (se añade lo que falte sobre D&A − cartera + inversión fija neta; terminal con D&A proporcional a las ventas). Recoge la intensidad real de «conservar competitividad» (electrificación de hornos, descarbonización) que λ no mide. Con P0",
    "P6i": "P6 con un suelo del 12 % de las ventas: la previsión oficial de la inversión de 2025 («around 12% of sales», presentación del primer trimestre de 2025, O6). Con P0",
    "P6x": f"P6 con el nivel de 2025 perpetuo ({INV_VENTAS[2025]:.1%} de las ventas), sin retorno en margen: extremo alto explorado, no cota. Con P0",
}


def s2c_factor(lmb):
    """Cociente entre el S2C marginal de la Historia (C53: ΔV 2020–2025 ÷ reinversión total 2021–2025) recalculado sin el exceso de
    reposición estimado (λ−1)·(D&A − cartera) en el denominador y el C53 original."""
    dv = A.VENTAS[2025] - A.VENTAS[2020]
    den = sum(A.H.cell(31, 3 + (y - 2016)).value for y in range(2021, 2026))  # Historia!H31:L31, reinversión neta total
    cart = {2023: 0.0, 2024: CL24 / 1000.0, 2025: CL25 / 1000.0}
    exceso = sum((lmb - 1) * (A.DA_H[y] - cart.get(y, 0.0)) for y in range(2021, 2026))
    c53 = dv / den
    return (dv / (den - exceso)) / c53, c53, den


def modelo(clave, lmb=None, ola=False, sin_capacidad_malo=False, s2c_explicito=False, cartera=True, x_plano=None, nivel_hueco=None, suelo=None):
    """Valor por escenario con la alternativa. Devuelve dict con V, ponderado, precio de Sí, peso terminal y el año a año."""
    res = {"clave": clave, "V": [], "peso_terminal": [], "filas": [], "terminal": []}
    f_s2c = s2c_factor(lmb)[0] if s2c_explicito else 1.0
    for i, e in enumerate(ESC):
        g1, m5, s2c, g, roic = e
        regla = "circulante_sin_capacidad" if (sin_capacidad_malo and i == 0) else "circulante"
        e2 = (g1, m5, s2c * f_s2c, g, roic)
        V, fil = A.proyeccion(T1, M1, regla, e2)
        # (4.8, Z-c de la auditoría interna) la regla del hueco solo descuenta la inversión fija neta que paga crecimiento nominal de una
        # base conservada (la de R1), no la que reconstruye una capacidad que no se conservó
        _, fil_credito = A.proyeccion(T1, M1, "circulante", e2) if regla == "circulante_sin_capacidad" else (None, fil)
        pv, escudo_pend, filas = 0.0, [], []
        plan_prev = None
        for k, f in enumerate(fil):
            cl = CL[k] if cartera else 0.0
            if x_plano is not None:
                extra = x_plano * DA25
            elif nivel_hueco is not None:
                extra = max(0.0, nivel_hueco - fil_credito[k]["inversion_fija_neta"])
            elif suelo is not None:
                extra = max(0.0, suelo * f["ventas"] - (DA25 - cl + fil_credito[k]["inversion_fija_neta"]))
            elif lmb is None:
                extra = 0.0
            elif s2c_explicito:
                extra = (lmb - 1) * (DA25 - cl)
            else:
                extra = max(0.0, (lmb - 1) * (DA25 - cl) - fil_credito[k]["inversion_fija_neta"])
            bruta = DA25 + f["inversion_fija_neta"] + extra - cl  # inversión bruta de caja (sin la cartera, que no se repone)
            ola_k = 0.0
            if ola and k in (0, 1):
                plan = 180.0 if k == 0 else (180.0 + bruta) / 2
                ola_k = max(0.0, plan - bruta)
                escudo_pend.append((k, ola_k))
            escudo = sum(T1 * o / 12 for (s, o) in escudo_pend if s < k <= s + 12)
            fcf = f["fcf"] + cl - extra - ola_k + escudo
            pv += fcf / (1 + R_OP) ** f["anio"]
            filas.append({"alternativa": clave, "escenario": NOMBRES[i], "anio": f["anio"], "ventas": f["ventas"], "nopat": f["nopat"], "delta_circulante": f["delta_circulante"],
                          "inversion_fija_neta": f["inversion_fija_neta"], "cartera_no_repuesta": cl, "reposicion_adicional": extra, "ola": ola_k, "escudo_fiscal_ola": escudo,
                          "inversion_bruta_caja": bruta + ola_k, "fcf": fcf})
        # escudo fiscal de la ola que queda después del año 10 (en valor presente)
        pv += sum(T1 * o / 12 / (1 + R_OP) ** (k + 1) for (s, o) in escudo_pend for k in range(10, s + 13))  # años 11 en adelante
        n11 = V[10] * (1 + g) * m5 * (1 - T1)
        reinv11 = n11 * g / roic
        fija11 = reinv11 - V[10] * g * NWC
        da11 = DA25 * V[10] * (1 + g) / V0
        if x_plano is not None:
            extra11 = x_plano * DA25 * (1 + g)
        elif nivel_hueco is not None:
            extra11 = max(0.0, nivel_hueco * V[10] * (1 + g) / V0 - fija11)
        elif suelo is not None:
            extra11 = max(0.0, suelo * V[10] * (1 + g) - (da11 + fija11))
        elif lmb is None:
            extra11 = 0.0
        else:
            extra11 = max(0.0, (lmb - 1) * da11 - fija11)
        tv = (n11 - reinv11 - extra11) / (R_OP - g)
        pvt = tv / (1 + R_OP) ** 10
        v = (pv + pvt - PUENTE) / ACC
        res["V"].append(v)
        res["peso_terminal"].append(pvt / (pv + pvt))
        res["filas"] += filas
        res["terminal"].append({"escenario": NOMBRES[i], "nopat11": n11, "reinversion11": reinv11, "fija11": fija11, "da11": da11, "reposicion_adicional11": extra11, "fcf11": n11 - reinv11 - extra11})
    res["precio_si"], res["ponderado"] = A.escalera(res["V"], PROB)
    return res


R = {}
R["REF"] = modelo("REF", cartera=False)
R["P0"] = modelo("P0")
R["P1"] = modelo("P1", lmb=LAM_C)
R["P1_sin_P0"] = modelo("P1_sin_P0", lmb=LAM_C, cartera=False)
R["P1b"] = modelo("P1b", lmb=LAM_B)
R["P1a"] = modelo("P1a", lmb=LAM_A)
R["P1s"] = modelo("P1s", lmb=LAM_C, s2c_explicito=True)
R["P2"] = modelo("P2", lmb=LAM_C, ola=True)
R["P3"] = modelo("P3", lmb=LAM_C, sin_capacidad_malo=True)
R["P4"] = modelo("P4", lmb=LAM_A, ola=True, sin_capacidad_malo=True)
R["X41"] = modelo("X41", x_plano=A.X_2025, cartera=False)
R["P5"] = modelo("P5", nivel_hueco=EXCESO_MEDIO_PROPIO)
R["P5x"] = modelo("P5x", nivel_hueco=EXCESO_2025_PROPIO)
R["P5x0"] = modelo("P5x0", nivel_hueco=EXCESO_2025, cartera=False)  # solo para medir la parte no duplicada de X41
R["P6m"] = modelo("P6m", suelo=round(INV_VENTAS_MEDIA, 3))
R["P6i"] = modelo("P6i", suelo=0.12)
R["P6x"] = modelo("P6x", suelo=round(INV_VENTAS[2025], 3))
# controles de la réplica de valoración: REF = T1·M1·R1 de la 4.7.1; X41 = su sensibilidad «+41,8 % todos los escenarios»
m471 = {r["combinacion"]: r for r in csv.DictReader(open(os.path.join(M471, "financiero", "matriz.csv"), encoding="utf-8"))}["T1·M1·R1"]
s471 = [r for r in csv.DictReader(open(os.path.join(M471, "financiero", "sensibilidades_n3.csv"), encoding="utf-8"))
        if r["base"] == "T1·M1" and r["regla"] == "R1" and r["alcance"] == "todos los escenarios" and abs(float(r["x_sobre_DA"]) - A.X_2025) < 1e-5][0]
CONTROL_REF = all(abs(round(R["REF"]["V"][i], 4) - float(m471[k])) < 1e-9 for i, k in enumerate(("V_malo", "V_normal", "V_bueno"))) \
    and abs(round(R["REF"]["ponderado"], 4) - float(m471["ponderado"])) < 1e-9 and abs(round(R["REF"]["precio_si"], 4) - float(m471["precio_si"])) < 1e-9
CONTROL_X41 = abs(round(R["X41"]["ponderado"], 4) - float(s471["ponderado"])) < 1e-9 and abs(round(R["X41"]["precio_si"], 4) - float(s471["precio_si"])) < 1e-9
# identidades: FCF = NOPAT + D&A − inversión bruta − Δcirculante, con la inversión bruta de caja y la amortización no repuesta
IDENT = all(abs(f["fcf"] - (f["nopat"] + DA25 - (f["inversion_bruta_caja"]) - f["delta_circulante"] + f["escudo_fiscal_ola"])) < 1e-9 for a in R.values() for f in a["filas"])
# doble cómputo de X41: parte del adicional que ya pagaba la inversión fija neta del modelo (NORMAL y BUENO, años 1–10)
DOBLE = {NOMBRES[i]: sum(min(A.X_2025 * DA25, max(0.0, f["inversion_fija_neta"])) for f in R["REF"]["filas"] if f["escenario"] == NOMBRES[i]) for i in (1, 2)}
PARTE_DOBLE_X41 = 1 - (R["P5x0"]["ponderado"] - R["REF"]["ponderado"]) / (R["X41"]["ponderado"] - R["REF"]["ponderado"])
CLASE = {"REF": "referencia (supuesto de la plantilla, no acreditado)", "P0": "respaldado con alcance y límites (dato publicado; efecto menor)",
         "P1": "hipótesis condicionada (desfase de inflación; indicios de balance, de vida contable y del Reino Unido; no acreditada)", "P1_sin_P0": "descomposición de P1", "P1b": "sensibilidad (extremo bajo explorado)",
         "P1a": "sensibilidad (extremo alto explorado)", "P1s": "contraste de estructura de P1 (hipótesis condicionada)",
         "P2": "hipótesis condicionada (fuente secundaria y posterior a la base)", "P3": "hipótesis condicionada (capacidad)",
         "P4": "combinación adversa de λ alto, ola y capacidad (sensibilidad, no cota)", "X41": "sensibilidad de la 4.7.1; cerca de la mitad de su efecto es doble cómputo (la parte restante, en P5x0)",
         "P5": "hipótesis condicionada (nivel estructural; no acreditada)", "P5x": "sensibilidad (nivel de 2025 con hueco)", "P5x0": "medida auxiliar (doble cómputo de X41)", "P6m": "hipótesis condicionada (intensidad de inversión; no acreditada)",
         "P6i": "sensibilidad (intensidad de inversión: previsión de 2025)", "P6x": "sensibilidad (extremo alto explorado, no cota)"}

# ------------------------------------------------------------------ salidas
ok_ev = not FALLOS
log("P-M1 · REPOSICIÓN FRENTE A AMORTIZACIÓN · Vidrala · entrega 4.8 (resultados mecánicos de un ensayo; no comparables con el precio)")
log(f"réplica 4.7.1 ejecutada sin cambios (SHA-256 del código {CODIGO_471_SHA[:16]}…): salidas idénticas byte a byte {iguales} · control interno de la 4.7.1 {A.control}")
log(f"evidencia: {len(EV)} datos, {sum(e['reproduce'] for e in EV)} reproducen" + (f" · NO REPRODUCEN: {FALLOS}" if FALLOS else ""))
log(f"X-e (PDF español, p. 58; inglés, CF_2025): depreciación de derechos de uso 2025 = {ROU25:,.0f} · 2024 = {ROU24:,.0f} miles")
log(f"amortización 2025 = {DA25:.3f} = material {PPE_DOT / 1000:.3f} + intangibles {INT25 / 1000:.3f} (de ellos cartera {CL25 / 1000:.3f}) + derechos de uso {ROU25 / 1000:.3f} = {(PPE_DOT + INT25 + ROU25) / 1000:.3f}")
log(f"inversión de caja 2025 (Historia) {A.CAPEX_H[2025]:.3f} · altas del ejercicio {INV_SEG25 / 1000:.3f} · arrendamientos nuevos {(LEASE_ADD + LEASE_OTR) / 1000:.3f} (altas {LEASE_ADD / 1000:.3f} + otros {LEASE_OTR / 1000:.3f})")
fisica = (PPE_DOT + INT25 - CL25) / 1000
log(f"amortización de activos propios que se reponen (material + intangibles − cartera) {fisica:.3f}: inversión ÷ esa amortización = {A.CAPEX_H[2025] / fisica:.3f} (frente a {A.CAPEX_H[2025] / DA25:.3f} con la amortización total)")
log(f"bienes totalmente amortizados en uso (coste, M€): " + " · ".join(f"{y}: {v:.0f}" for y, v in sorted(TOT.items())) + f" · en 2025, {TOT[2025] * 1000 / PPE_COSTE:.1%} del coste bruto")
log(f"coste en amortización ÷ dotación 2025 ≈ {DEPREC_ACTIVO:.1f} años (vida contable media implícita; incluye terrenos)")
log("\nCONCILIACIÓN POR AÑO (Historia, filas 6, 8 y 12)")
for c in CONC:
    log(f"  {c['anio']}: ventas {c['ventas']:.1f} · inversión {c['capex_historia']:.1f} · D&A {c['da_historia']:.1f} · ratio {c['capex_sobre_da']:.2f} · totalmente amortizado {c['totalmente_amortizado_en_uso_coste'] or '—'} · {c['nota_perimetro']}")
log("\nPOR SEGMENTO (inversiones del ejercicio ÷ amortización)")
for s in SEGFILAS:
    log(f"  {s['anio']} · {s['segmento']}: {s['inversiones']:.3f} / " + (f"{s['amortizacion']:.3f} = {s['ratio']:.2f}" if s["amortizacion"] else "—"))
log(f"  Reino Unido e Irlanda, ciclo 2018–2025: {UK_CICLO:.3f} (con la cifra de 2018 del propio informe: {UK_CICLO_PROPIO:.3f}) · Iberia y resto 2019–2025: {IB_RATIO:.3f}")
log(f"\nλ: central {LAM_C:.2f}, bajo {LAM_B:.2f}, alto {LAM_A:.2f} · λ(12 años, 2 %) = {lam(12, 0.02):.3f} · λ(12, 3 %) = {lam(12, 0.03):.3f} · λ(10, 1 %) = {lam(10, 0.01):.3f} · λ(16, 3 %) = {lam(16, 0.03):.3f} · balance 1 + π·VNC/dotación: {LAM_BALANCE[0.02]:.3f} (2 %) · {LAM_BALANCE[0.03]:.3f} (3 %)")
log(f"exceso de la inversión sobre la amortización: 2025 {EXCESO_2025:.1f} (sobre la que se repone, {EXCESO_2025_PROPIO:.1f}) · media 2021–2025 {EXCESO_MEDIO:.1f} (sobre la que se repone, {EXCESO_MEDIO_PROPIO:.1f}) · inversión ÷ ventas: " + " · ".join(f"{y} {v:.1%}" for y, v in INV_VENTAS.items()) + f" · media {INV_VENTAS_MEDIA:.1%}")
log(f"· factor S2C de P1s {s2c_factor(LAM_C)[0]:.4f} (C53 recalculado {s2c_factor(LAM_C)[1]:.4f})")
log(f"\ncontrol REF = T1·M1·R1 de la 4.7.1: {CONTROL_REF} · control X41 = su sensibilidad «+41,8 % todos»: {CONTROL_X41} · identidad del FCF en todas las filas: {IDENT}")
log("\nALTERNATIVAS (T1·M1·R1 de base; r, probabilidades, k, caja, puente y acciones sin cambios)")
log(f"  {'clave':10s} {'V MALO':>7s} {'V NORMAL':>8s} {'V BUENO':>8s} {'ponderado':>9s} {'Δ':>6s} {'Sí':>6s} {'Δ':>6s}  peso terminal       clase")
for k, r in R.items():
    log(f"  {k:10s} {r['V'][0]:7.2f} {r['V'][1]:8.2f} {r['V'][2]:8.2f} {r['ponderado']:9.2f} {r['ponderado'] - R['REF']['ponderado']:+6.2f} {r['precio_si']:6.2f} {r['precio_si'] - R['REF']['precio_si']:+6.2f}  "
        + "/".join(f"{p:.3f}" for p in r["peso_terminal"]) + f"   {CLASE[k]}")
log(f"\nX41: parte de su efecto sobre el ponderado que es doble cómputo (comparada con P5x0, el mismo nivel con hueco y sin P0) ≈ {PARTE_DOBLE_X41:.0%}")
log(f"X41: inversión adicional que ya estaba pagada por la inversión fija neta del modelo, años 1–10: NORMAL {DOBLE['NORMAL']:.1f} · BUENO {DOBLE['BUENO']:.1f} (de {A.X_2025 * DA25 * 10:.1f} añadidos en cada escenario)")
for k in ("REF", "P1", "P2", "P4", "P5", "P6m", "P6x"):
    m = [f for f in R[k]["filas"] if f["escenario"] == "MALO"]
    log(f"  necesidades de caja {k} (MALO): FCF año 1 {m[0]['fcf']:.1f} · mínimo {min(f['fcf'] for f in m):.1f} · suma años 1–5 {sum(f['fcf'] for f in m[:5]):.1f} · inversión bruta de caja año 1 {m[0]['inversion_bruta_caja']:.1f}")
for k in ("P1", "P1a", "P5", "P6m"):
    log(f"  terminal {k}: " + " · ".join(f"{t['escenario']} fija11 {t['fija11']:.1f} → adicional {t['reposicion_adicional11']:.1f}" for t in R[k]["terminal"]))
for k in ("REF", "P1"):
    for i in (1, 2):
        fs = [f for f in R[k]["filas"] if f["escenario"] == NOMBRES[i]]
        log(f"  inversión bruta de caja ÷ ventas {k} {NOMBRES[i]}: año 1 {fs[0]['inversion_bruta_caja'] / fs[0]['ventas']:.1%} · año 10 {fs[-1]['inversion_bruta_caja'] / fs[-1]['ventas']:.1%} · cociente sobre D&A año 1 {fs[0]['inversion_bruta_caja'] / DA25:.2f}")

json.dump(EV, open(os.path.join(SAL, "pm1_evidencia.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
with open(os.path.join(SAL, "pm1_conciliacion_anual.csv"), "w", encoding="utf-8", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(CONC[0].keys()))
    w.writeheader()
    for c in CONC:
        w.writerow({k: (round(v, 6) if isinstance(v, float) else v) for k, v in c.items()})
with open(os.path.join(SAL, "pm1_segmentos.csv"), "w", encoding="utf-8", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=["anio", "segmento", "inversiones", "amortizacion", "ratio"])
    w.writeheader()
    for s in SEGFILAS:
        w.writerow({k: (round(v, 6) if isinstance(v, float) else v) for k, v in s.items()})
with open(os.path.join(SAL, "pm1_alternativas.csv"), "w", encoding="utf-8", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["clave", "V_malo", "V_normal", "V_bueno", "ponderado", "d_ponderado", "precio_si", "d_precio_si", "peso_terminal_malo", "peso_terminal_normal", "peso_terminal_bueno",
                "fcf1_malo", "fcf_min_malo", "inversion_bruta_caja_a1_malo", "clase", "fundamento"])
    for k, r in R.items():
        m = [f for f in r["filas"] if f["escenario"] == "MALO"]
        w.writerow([k, *[round(v, 4) for v in r["V"]], round(r["ponderado"], 4), round(r["ponderado"] - R["REF"]["ponderado"], 4), round(r["precio_si"], 4), round(r["precio_si"] - R["REF"]["precio_si"], 4),
                    *[round(p, 4) for p in r["peso_terminal"]], round(m[0]["fcf"], 3), round(min(f["fcf"] for f in m), 3), round(m[0]["inversion_bruta_caja"], 3), CLASE[k],
                    ALTERNATIVAS.get(k.replace("_sin_P0", ""), "P1 sin la corrección P0")])
with open(os.path.join(SAL, "pm1_anio_a_anio.csv"), "w", encoding="utf-8", newline="") as fh:
    campos = list(R["REF"]["filas"][0].keys())
    w = csv.DictWriter(fh, fieldnames=campos)
    w.writeheader()
    for r in R.values():
        for f in r["filas"]:
            w.writerow({k: (round(v, 5) if isinstance(v, float) else v) for k, v in f.items()})
    for r in R.values():
        for t in r["terminal"]:
            w.writerow({"alternativa": r["clave"], "escenario": t["escenario"], "anio": 11, "ventas": None, "nopat": round(t["nopat11"], 5), "delta_circulante": None,
                        "inversion_fija_neta": round(t["fija11"], 5), "cartera_no_repuesta": 0.0, "reposicion_adicional": round(t["reposicion_adicional11"], 5), "ola": 0.0,
                        "escudo_fiscal_ola": 0.0, "inversion_bruta_caja": None, "fcf": round(t["fcf11"], 5)})
json.dump({"constantes": {"T1": T1, "M1": M1, "r_op": R_OP, "DA25": DA25, "NWC_RATIO": NWC, "V0": V0, "acciones": ACC, "puente": PUENTE, "probabilidades": PROB,
                          "lambda": {"central": LAM_C, "bajo": LAM_B, "alto": LAM_A, "l12_pi2": lam(12, 0.02), "l12_pi3": lam(12, 0.03), "l10_pi1": lam(10, 0.01), "l16_pi3": lam(16, 0.03), "balance": LAM_BALANCE},
                          "exceso_2025": EXCESO_2025, "exceso_medio_2021_2025": EXCESO_MEDIO, "exceso_2025_propio": EXCESO_2025_PROPIO, "exceso_medio_propio": EXCESO_MEDIO_PROPIO, "inversion_sobre_ventas": INV_VENTAS, "inversion_sobre_ventas_media": INV_VENTAS_MEDIA, "uk_ciclo": [UK_CICLO, UK_CICLO_PROPIO], "iberia_2019_2025": IB_RATIO,
                          "cartera_por_anio": CL, "factor_s2c_P1s": s2c_factor(LAM_C)[0]},
           "alternativas": ALTERNATIVAS, "clases": CLASE,
           "resultados": {k: {"V": r["V"], "ponderado": r["ponderado"], "precio_si": r["precio_si"], "peso_terminal": r["peso_terminal"], "terminal": r["terminal"]} for k, r in R.items()},
           "controles": {"replica_471_identica": iguales, "control_471": A.control, "ref": CONTROL_REF, "x41": CONTROL_X41, "identidad_fcf": IDENT, "evidencia": ok_ev},
           "doble_computo_x41": DOBLE, "parte_doble_computo_x41": PARTE_DOBLE_X41}, open(os.path.join(SAL, "pm1_resultados.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
open(os.path.join(SAL, "pm1_salida.txt"), "w", encoding="utf-8").write("\n".join(LOG) + "\n")
TODO = CONTROL_REPLICA and CONTROL_REF and CONTROL_X41 and IDENT and ok_ev
log(f"\nRESULTADO: {'todos los controles cumplen' if TODO else 'ALGÚN CONTROL FALLA'}")
open(os.path.join(SAL, "pm1_salida.txt"), "a", encoding="utf-8").write(f"\nRESULTADO: {'todos los controles cumplen' if TODO else 'ALGÚN CONTROL FALLA'}\n")
sys.exit(0 if TODO else 1)
