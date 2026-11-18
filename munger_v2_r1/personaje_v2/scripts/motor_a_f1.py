#!/usr/bin/env python3
"""Motor A con el perímetro F1 (decisiones del 17-nov-2026) · guardas V-F1a…m · comprobación K3 (F1-IMPL, 4.15).

Qué es. La capa del motor A (V6.3) que aplica las decisiones económicas F1 registradas el 17-nov-2026 por la persona responsable
(DECISIONES_PARA_EL_USUARIO.md, F1 (1a)–(5b) y E8.1). Usa las MISMAS ecuaciones que el libro V6.3 (Convenciones V6.3 §1–§3 y §10) y las
mismas entradas (Historia, Análisis, Palancas y Diagnóstico V6 del libro recalculado), más una declaración del expediente
(`motor_a_f1.json`) con lo que el libro no tiene: la norma contable, los perímetros, la amortización de derechos de uso y de intangibles
de combinaciones por año, la clasificación de las compras, la inversión de transición, la reinversión estimada y los ajustes N1.
  - Reproduce el libro en el perímetro A0 (f = Historia C58, ancla = C53, flujos = Motor AU:BD y BF): si no lo reproduce, bloquea
    (F1-REPLICA). Es la comprobación de que la capa y el libro son el mismo motor.
  - Calcula f, el ancla de S2C (E4), los flujos de los años 1–10 y del año 11 (E3) y el flujo sin crecimiento con el perímetro
    declarado y, como diagnóstico, con A0, A1 y A2.
  - Evalúa las guardas V-F1a…V-F1m con la severidad de E5 y las guardas de implantación F1-* (límites declarados).
  - K3: el flujo sin crecimiento frente al FCF base (la «caja libre base normalizada», Análisis C52 → Historia C70), partida a partida;
    señala la amortización no monetaria que la proyección cobra además de su caja (doble cómputo).
Qué NO es. No cambia el libro, la plantilla V6.3, sus fuentes ni sus entradas registradas (C46–C52, C48 = 108, C49, C70). El libro V6.3
sigue calculando A0: con otro perímetro (o con N1), su valor no corresponde a la declaración y la conclusión del motor A queda
bloqueada (F1-LIBRO, límite declarado); los flujos F1 se muestran como diagnóstico rotulado. No adopta ningún valor sin decidir
(PARAMETROS_SIN_VALOR) ni declara aptitud para dinero real.
US GAAP (ASC 842; 18-nov-2026, F1_USGAAP.md). La norma es un valor cerrado (NIIF o US_GAAP) y los arrendamientos OPERATIVOS y FINANCIEROS
se tratan por separado. Financieros: como NIIF 16 (da_rou y C49). Operativos: su coste va entero en el EBIT y su pago en el CFO, así que
ya cuentan una vez en el FCF base; la reinversión que calibra f no lleva ninguna partida suya (D-US2: se cuentan los pagos): la
amortización de su derecho de uso que esté dentro de la fila 8 sale de D_X y lo que esté dentro de la fila 14 se retira del circulante.
Si la empresa no publica en qué líneas del flujo van esos dos tramos, se aplica la hipótesis general declarada D-US1 (fuera de las filas 8
y 14) y la conclusión queda condicionada, con su cota. Con el motor B y US GAAP solo se evalúa el puente de deuda (F1-US-PUENTE).

Uso:
  motor_a_f1.py evaluar CARPETA [--libro LIBRO_RECALCULADO] [--declaracion motor_a_f1.json] [--salida DIR]
      escribe DIR/motor_a_f1_resultado.json y .md (DIR = CARPETA por defecto).
      Código: 0 utilizable para una conclusión · 3 bloquea con falta de datos o de decisión (pendiente_de_datos) ·
              4 bloquea por el modelo (límite del modelo) · 5 bloquea por un fallo de implementación (réplica o K3) · 2 uso o archivo ilegible.
  motor_a_f1.py plantilla  → imprime una declaración vacía (todo sin declarar)
"""
import argparse
import datetime as dt
import hashlib
import json
import os
import re
import sys
from fractions import Fraction as Fr

# los módulos hermanos (f1_libro_v631, verificacion_entradas) se importan dentro de las funciones: con «python3 -I» la carpeta del guion no
# está en sys.path (la regresión de Elis lo llama así) y el import fallaba desde la V6.3.1
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

VERSION = "F1-IMPL 2 (4.15 · decisiones F1 del 17-nov-2026 · US GAAP, ASC 842: D-US1, D-US2, D-US2 bis y D-WM del 18-nov-2026 · cierre de la revisión R2)"
DECLARACION = "motor_a_f1.json"
RESULTADO = "motor_a_f1_resultado.json"
RESULTADO_MD = "motor_a_f1_resultado.md"

PERIMETROS = ("A0_total", "A1_sin_ROU", "A2_propio", "A3_estimado")
MARGENES = ("EBIT_NIIF16_PPA_constante", "EBIT_NIIF16_PPA_decreciente", "EBIT_NIIF16_sin_PPA", "margen_despues_de_arrendamientos")
COMPRAS = ("pendiente", "crecimiento_por_hipotesis", "reposicion_con_importe", "sin_compras")
TRANSICION = ("pendiente", "en_R", "termino_explicito", "crecimiento")
NORMAS = ("NIIF", "US_GAAP")
# (F1 · US GAAP; revisión F1-IMPL, H13) La norma es un VALOR CERRADO. En la declaración: NIIF o US_GAAP. En el libro (Control maestro L4,
# cuya lista de validación es «IFRS, US GAAP, Otro»): una lista cerrada de valores EXACTOS (sin distinguir mayúsculas ni espacios de más), los
# de la lista y las dos variantes con que se escribieron los libros NIIF anteriores. No se busca «ifrs» dentro de un texto: «US GAAP (no
# IFRS)» no es ningún valor de la lista y bloquea.
NORMA_DEL_LIBRO = {"ifrs": "NIIF", "niif": "NIIF", "ifrs (ifrs-eu)": "NIIF", "ifrs (adoptadas por la unión europea)": "NIIF", "us gaap": "US_GAAP"}
# (F1 · US GAAP, ASC 842) series propias de US GAAP (mismo formato que da_rou) y ubicaciones admitidas de los dos tramos no monetarios del
# arrendamiento operativo en el estado de flujos (fila 8 = D&A; fila 14 = variación del circulante)
SERIES_US = ("pagos_arr_operativo", "coste_arr_operativo", "da_rou_operativo", "circulante_arr_operativo", "pasivo_arr_operativo",
             "pagos_arr_financiero_principal", "caja_pagada_arr_financiero", "gasto_arr_financiero", "da_rou_financiero_fuera")
SERIES_US_CON_SIGNO = ("circulante_arr_operativo",)   # lleva el signo de la fila 14 (+ consume caja): puede ser negativa
UBICACIONES = {"amortizacion_rou": ("fila_8", "fila_14", "fuera_de_las_filas_8_y_14", "no_publicada"),
               "variacion_pasivo": ("fila_14", "fuera_de_las_filas_8_y_14", "no_publicada")}
# (ronda 2, R1-16) amortización del derecho de uso de los arrendamientos FINANCIEROS: por omisión dentro de la fila 8 (como NIIF 16, con su serie
# da_rou); «fuera_de_la_fila_8» se declara con su evidencia y con la serie da_rou_financiero_fuera (la cifra publicada)
UBICACIONES_FIN = ("fila_8", "fuera_de_la_fila_8")
# (ronda 2, D-WM) desglose de los arrendamientos financieros: «publicado» (amortización y principal por separado: como NIIF 16) o «no_publicado»
# (la empresa no los separa: se tratan como deuda y activos propios, hipótesis declarada)
DESGLOSES_FIN = ("publicado", "no_publicado")
TOL_E7 = Fr(5, 10 ** 4)        # redondeo a 3 decimales de E7 (K3a)
TOL_US_C49 = Fr(5, 1000)       # C49 frente al principal financiero publicado: medio céntimo de la unidad del modelo (redondeo a 2 decimales de la etapa 1)
CITA_MINIMA = 10               # caracteres mínimos de la cita literal de una clasificación (una cita más corta no identifica una línea)
# Decisiones de la persona responsable del 18-nov-2026 sobre US GAAP (reglas generales, iguales para todas las empresas; no se declaran por
# expediente). D-US1 es una HIPÓTESIS declarada, no un dato: donde la empresa publica las líneas, manda el dato.
_REG_US = {"fecha": "2026-11-18", "persona": "persona responsable del proyecto (decisión registrada; no se firma aquí)",
           "motivo": "munger-v2-evidencias-mistral, coordinacion/cierre_v2/DECISIONES_PARA_EL_USUARIO.md:96–98"}
# (ronda 2) decisiones de la persona responsable del 18-nov-2026 (tarde), tras la revisión R1 de F1 con US GAAP
_REG_US2 = {"fecha": "2026-11-18", "persona": "persona responsable del proyecto (decisión registrada; no se firma aquí)",
            "motivo": "munger-v2-evidencias-mistral, coordinacion/cierre_v2/DECISIONES_PARA_EL_USUARIO.md:112–114 (tras la revisión R1 de F1 con US GAAP)"}
DECISIONES_US = {
    "D-US1": {"regla": ("si la empresa no publica en qué líneas del estado de flujos van los dos tramos del arrendamiento operativo (la amortización "
                        "del derecho de uso y la variación del pasivo), se supone que van netos dentro del flujo de explotación, fuera de las filas 8 "
                        "(D&A) y 14 (circulante) de la Historia: hipótesis declarada, no dato; la conclusión se presenta como condicionada, con su "
                        "cota de sensibilidad. Donde la empresa publica las líneas, manda el dato"), "registro": dict(_REG_US)},
    "D-US2": {"regla": ("cuando el coste lineal del arrendamiento operativo y los pagos del año difieren, se cuentan los pagos y la diferencia "
                        "queda a la vista, sin bloquear"), "registro": dict(_REG_US)},
    "D-US2 bis": {"regla": ("con el alquiler operativo mezclado en las líneas de otros activos y otros pasivos (los dos tramos dentro de la fila 14) no se "
                            "bloquea: se publica el valor de la hoja, que cuenta el coste contable, y al lado cuánto cambiaría contando los pagos; antes, "
                            "el programa comprueba que el expediente muestra las dos líneas (la del activo y la del pasivo)"), "registro": dict(_REG_US2)},
    "D-WM": {"regla": ("los arrendamientos financieros que la empresa no desglosa se tratan como deuda y activos propios (hipótesis declarada): su "
                       "amortización queda dentro de la propia y sus pagos no se restan de la caja base; la diferencia estimada (caja pagada − gasto "
                       "total) se enseña junto al resultado"), "registro": dict(_REG_US2)}}
# líneas que nombran un arrendamiento o un derecho de uso: en las que la fase 1 sumó en la fila 8 (da) o en la fila 14 (circulante_lineas), en la
# página del estado de flujos y en las citas de las ubicaciones (ronda 2, R1-6: un solo patrón, el amplio)
_LINEA_ARR = re.compile(r"\bleas(?:e|es|ed|ing)\b|right[- ]of[- ]use|\brou\b|arrendamiento|derechos? de uso", re.I)
# información complementaria del estado de flujos (altas sin caja, caja pagada): no es una línea de la conciliación del flujo de explotación
_LINEA_SUPL = re.compile(r"exchang|obtain|supplement|cash paid|non-?cash (?:investing|financing)|a cambio de|informaci[oó]n complementaria", re.I)
# (ronda 2, R1-3) qué tramo enseña una línea: el pasivo (variación del pasivo) o el activo o el gasto (amortización del derecho de uso). Los
# términos van pegados a «lease» o a «right-of-use»: «accrued expenses» o «other assets» en una línea mezclada no cuentan
_T_PASIVO = re.compile(r"leas(?:e|es|ing)\s+(?:assets?\s+and\s+)?(?:liabilit|obligation)|(?:liabilit\w*|obligations?)\s+(?:under|for|on|of)\s+(?:\w+\s+){0,3}leas|"
                       r"pasivos?\s+(?:por|de)\s+arrendamiento", re.I)
_T_ACTIVO = re.compile(r"right[- ]of[- ]use|\brou\b|leas(?:e|es|ing)\s+(?:assets?|expenses?|costs?|amortization)|non-?cash\s+(?:operating\s+)?leas|"
                       r"amortization\s+of\s+(?:\w+\s+){0,4}leas|derechos?\s+de\s+uso|activos?\s+por\s+arrendamiento|gastos?\s+por\s+arrendamiento", re.I)
# (cierre de la ronda 2, R2-1) líneas que nombran un arrendamiento JUNTO A OTRA COSA —deterioro, baja, cancelación, modificación, abandono, costes de
# salida, incentivos, venta con arrendamiento posterior, resultados—: no son la amortización del derecho de uso ni la variación del pasivo. No hacen
# saltar «manda el dato» frente a «no_publicada», no valen como cita de una ubicación y no cuentan entre las líneas sumadas que nombran un tramo
_LINEA_AJENA = re.compile(r"impair|write[- ]?(?:offs?|downs?)|written[- ](?:off|down)|terminat|modif|remeasur|abandon|\bexit\b|incentiv|lease[- ]?backs?\b|"
                          r"\bgains?\b|\bloss(?:es)?\b|deterioro|saneamiento|\bbajas?\b|cancelaci|rescisi|terminaci|modificaci|abandono|costes?\s+de\s+salida|"
                          r"incentivo|arrendamiento\s+posterior|ganancia|p[eé]rdida|plusval|minusval", re.I)
# (R2-2) palabras de una línea PROPIA de un tramo: si la etiqueta entera solo lleva estas, su cifra impresa es la del arrendamiento; con cualquier otra
# («accounts payable, accrued liabilities, operating lease liabilities and other…», «depreciation and amortization, including…») es una línea mezclada
_PALABRAS_PROPIAS = frozenset("""operating finance financing lease leases leasing leased right of use rou asset assets liability liabilities obligation obligations
non noncash cash expense expenses cost costs amortization amortisation reduction reductions in the carrying amount amounts change changes increase decrease net and
for on under to from a total current noncurrent long term short portion payments payment principal accretion interest
arrendamiento arrendamientos operativo operativos financiero financieros derecho derechos de uso activo activos pasivo pasivos por variación variacion cambio
cambios aumento disminución disminucion amortización amortizacion gasto gastos coste costes neto neta y en del los las el la no monetario monetarios corriente
corrientes pagos pago principal""".split())
_ES_FIN = re.compile(r"financ|capital\s+leas", re.I)
_ES_OP = re.compile(r"operating|operativ", re.I)
_NOMBRE_TRAMO = {"amortizacion_rou": "la amortización del derecho de uso", "variacion_pasivo": "la variación del pasivo",
                 "amortizacion_rou_financiero": "la amortización del derecho de uso de los arrendamientos financieros"}
_LADO_TRAMO = {"amortizacion_rou": "activo", "variacion_pasivo": "pasivo"}
_UB_TXT = {"fila_8": "dentro de la fila 8", "fila_14": "dentro de la fila 14", "fuera_de_las_filas_8_y_14": "fuera de las filas 8 y 14",
           "fuera_de_la_fila_8": "fuera de la fila 8", "no_publicada": "no publicada (hipótesis D-US1)"}
# E8.1, decidido el 17-nov-2026: se mantiene el τ registrado de cinco años (Historia C52)
CONVENCION_TAU = "cinco_anios"
# Decisiones aplazadas (propuestas de 9cad78d sin adoptar): NO tienen valor. Si un cálculo las necesita, se calculan las variantes y la
# conclusión queda bloqueada (F1-PARAM). No se declaran por expediente: son decisiones de producto.
PARAMETROS_SIN_VALOR = {
    "alcance_n1_ejercicios_tau": {"valor": None, "opciones": ["solo_ventana", "tambien_ejercicios_tau_fuera_de_la_ventana"],
                                  "documento": "N1_ALCANCE_EJERCICIOS_TAU.md (propuesta, no adoptada)"},
    "n1_actualizacion_financiera_earnout": {"valor": None, "opciones": ["excluida", "incluida_fuera_del_BAI"],
                                            "documento": "N1_ACTUALIZACION_EARNOUT_MEXICO.md (propuesta, no adoptada)"},
    "umbral_v_f1a": {"valor": None, "opciones": ["sin umbral (V-F1a bloquea con cualquier importe)", "una medida y un valor"],
                     "documento": "PROPUESTA_UMBRAL_V-F1a.md (propuesta, no adoptada)"},
}
# reglas de normalización aprobadas: solo N1 (5a), sin efecto en el gasto por impuesto; N2 pendiente; nada por su etiqueta
REGLAS_NORMALIZACION = {"N1": "no_deducible"}
TOL_LIBRO = Fr(1, 10 ** 9)
COLS = "CDEFGHIJKL"
CLAVES_DECL = {"formato", "nota", "norma_contable", "perimetro_reinversion", "perimetro_margen", "perimetro_palancas_s2c", "perimetro_roic",
               "clasificacion_compras", "transicion", "reinversion_estimada", "series", "normalizacion", "umbral_v_f1a", "parametros",
               "conciliacion_fcf_base", "justificacion_reinversion_negativa", "fuentes_series", "arrendamientos_us_gaap"}
SERIES = ("da_rou", "da_ppa", "pagos_arrendamiento")
SIN_TRATAMIENTO = ("", "ninguno", "ninguna", "-", "—", "no", "n/a", "na", "sin tratamiento", "none")


class ErrorDeclaracion(Exception):
    pass


# ----------------------------------------------------------------------------------------------------------- utilidades numéricas
def Q(x):
    """Número exacto desde el valor del libro o de la declaración (los float se toman por su representación decimal, como el contraste F1)."""
    if x is None or isinstance(x, bool):
        return None
    if isinstance(x, Fr):
        return x
    if isinstance(x, int):
        return Fr(x)
    if isinstance(x, float):
        return Fr(repr(x))
    if isinstance(x, str):
        s = x.strip().replace(",", ".")
        try:
            return Fr(s)
        except (ValueError, ZeroDivisionError):
            return None
    return None


def fl(x, n=12):
    return None if x is None else round(float(x), n)


def media(xs):
    xs = list(xs)
    return sum(xs, Fr(0)) / len(xs)


def r4(x):
    """Convención de la fila 10 de la Historia: tipo = gasto ÷ BAI con 4 decimales."""
    return Fr(round(x, 4)).limit_denominator(10 ** 4)


# ----------------------------------------------------------------------------------------------------------- lectura del libro
def leer_libro(ruta):
    """Valores (caché) del libro V6.3 recalculado: lo que el motor A usa y lo que la réplica contrasta. Solo lectura."""
    import openpyxl
    wb = openpyxl.load_workbook(ruta, data_only=True, read_only=True)
    v = {"sha256": hashlib.sha256(open(ruta, "rb").read()).hexdigest(), "ruta": os.path.abspath(ruta)}
    rangos = [("Historia", "A5:L81"), ("Historia", "A84:L89"), ("Análisis", "B44:D80"), ("Palancas", "B14:D23"), ("Motor", "A6:BT9"),
              ("Diagnóstico V6", "B5:D16"), ("Diagnóstico V6", "B174:D179"), ("Control maestro", "H4:L4")]
    for hoja, rango in rangos:
        if hoja not in wb.sheetnames:
            continue
        for fila in wb[hoja][rango]:
            for c in fila:
                if c.value is not None:
                    v[f"{hoja}!{c.coordinate}"] = c.value
    wb.close()
    return v


def _hist(L, fila):
    return [L.get(f"Historia!{c}{fila}") for c in COLS]


# ----------------------------------------------------------------------------------------------------------- declaración
def plantilla_declaracion():
    reg = {"fecha": None, "persona": None, "motivo": None}
    return {
        "formato": "motor_a_f1 v1",
        "nota": "Declaración F1 del expediente. La rellena la persona responsable (o quien ella designe), nunca el agente. Vacío = sin declarar.",
        "norma_contable": {"valor": None, "registro": dict(reg)},
        "perimetro_reinversion": {"valor": None, "registro": dict(reg)},
        "perimetro_margen": {"valor": None, "registro": dict(reg)},
        "perimetro_palancas_s2c": {"valor": None, "registro": dict(reg)},
        "perimetro_roic": {"valor": None, "registro": dict(reg)},
        "clasificacion_compras": {"valor": None, "registro": dict(reg), "importes": None, "proporcion_ventas": None,
                                  "ancla_s2c_excluye_terminos": None, "fundamento": None},
        "transicion": {"conocida": None, "tratamiento": None, "registro": dict(reg), "importes": None, "horizonte": None,
                       "naturaleza": None, "finalidad_documentada": None, "ancla_s2c_excluye_terminos": None},
        "reinversion_estimada": None,
        "arrendamientos_us_gaap": None,   # solo con US_GAAP: {registro, operativos: {existen, documento, pagina, cita, amortizacion_rou, variacion_pasivo}, financieros: {…}}
        "series": {s: {} for s in SERIES},
        "normalizacion": {"ajustes": [], "bai": {}, "gasto_impuesto": {}, "margen_objetivo_sin_ajustes": None,
                          "deducir_diagnostico_partidas_puntuales": False},
        "umbral_v_f1a": None,
    }


def _registro_ok(reg):
    return isinstance(reg, dict) and all(str(reg.get(k) or "").strip() for k in ("fecha", "persona", "motivo"))


def _valor(decl, clave):
    d = decl.get(clave)
    if isinstance(d, dict):
        return d.get("valor"), d.get("registro")
    return None, None


def _declaracion_bien_formada(decl):
    """(ronda 2, R1-14) Copia de la declaración en la que las claves que tienen que ser un objeto (o una lista) lo son; lo que no lo es se sustituye por un
    valor vacío y se anota (DATOS INVÁLIDOS en F1-DECLARACION), en lugar de hacer fallar el programa. Devuelve (declaración, problemas, notas).
    (cierre de la ronda 2, R2-4) Vacío = sin declarar: un valor vacío que no es un objeto ([], "" o 0) se toma como vacío, como antes de la ronda 2; solo
    lo que tiene contenido y no es un objeto es DATOS INVÁLIDOS. Dentro de «series», un TEXTO en una clave que no es el nombre de una serie es una nota:
    se admite, no entra en el cálculo y queda a la vista (notas). Los demás sitios de una nota: «nota» en el primer nivel y «nota» dentro del año de una serie."""
    d, mal, notas = dict(decl), [], []
    objetos = ("norma_contable", "perimetro_reinversion", "perimetro_margen", "perimetro_palancas_s2c", "perimetro_roic", "clasificacion_compras", "transicion",
               "series", "normalizacion", "fuentes_series")
    for k in objetos:
        if d.get(k) is not None and not isinstance(d[k], dict):
            if d[k]:   # con contenido y sin ser un objeto; vacío ([], "", 0) = sin declarar
                mal.append(f"«{k}» no es un objeto ({type(d[k]).__name__})")
            d[k] = {}
    if isinstance(d.get("series"), dict):
        s = dict(d["series"])
        for k, v in list(s.items()):
            if v is None or isinstance(v, dict):
                continue
            if isinstance(v, str) and v.strip() and k not in SERIES and k not in SERIES_US:
                notas.append(k)   # una nota de texto, no una serie: admitida y a la vista
                del s[k]
            elif not v:
                s[k] = {}
            else:
                mal.append(f"series.{k} no es un objeto por año ({type(v).__name__}); una nota de texto se escribe en «nota» (primer nivel de la declaración), en "
                           "«nota» dentro del año de una serie o, dentro de «series», como texto en una clave que no sea el nombre de una serie")
                s[k] = {}
        d["series"] = s
    if isinstance(d.get("normalizacion"), dict):
        n = dict(d["normalizacion"])
        for k in ("bai", "gasto_impuesto"):
            if n.get(k) is not None and not isinstance(n[k], dict):
                if n[k]:
                    mal.append(f"normalizacion.{k} no es un objeto por año")
                n[k] = {}
            elif isinstance(n.get(k), dict) and any(not str(a).lstrip("-").isdigit() for a in n[k]):
                mal.append(f"normalizacion.{k}: clave de año no válida")
                n[k] = {a: v for a, v in n[k].items() if str(a).lstrip("-").isdigit()}
        if n.get("ajustes") is not None and not isinstance(n["ajustes"], list):
            if n["ajustes"]:
                mal.append("normalizacion.ajustes no es una lista")
            n["ajustes"] = []
        d["normalizacion"] = n
    for k in ("clasificacion_compras", "transicion"):
        if isinstance(d.get(k), dict):
            c = dict(d[k])
            for kk in ("importes", "importes_historicos"):
                if c.get(kk) is not None and not isinstance(c[kk], dict):
                    if c[kk]:
                        mal.append(f"{k}.{kk} no es un objeto por año")
                    c[kk] = None
                elif isinstance(c.get(kk), dict) and any(not str(a).lstrip("-").isdigit() for a in c[kk]):
                    mal.append(f"{k}.{kk}: clave de año no válida")
                    c[kk] = {a: v for a, v in c[kk].items() if str(a).lstrip("-").isdigit()}
            d[k] = c
    re_ = d.get("reinversion_estimada")
    if re_ is not None and not isinstance(re_, dict):
        if re_:
            mal.append("«reinversion_estimada» no es un objeto")
        d["reinversion_estimada"] = None
    elif isinstance(re_, dict) and (re_.get("por_anio") is not None) and (not isinstance(re_["por_anio"], dict) or any(v is not None and not isinstance(v, dict) for v in re_["por_anio"].values())):
        mal.append("reinversion_estimada.por_anio no es un objeto por año de objetos")
        d["reinversion_estimada"] = dict(re_, por_anio={k: v for k, v in re_["por_anio"].items() if isinstance(v, dict)} if isinstance(re_["por_anio"], dict) else {})
    return d, mal, notas


def leer_serie(decl, nombre, anios, con_signo=False):
    """{año: magnitud} de una serie declarada y sus problemas. Cada año: {valor_fuente, signo, tratamiento, documento, pagina}; la magnitud
    del modelo es signo × valor_fuente (R415-SIGNO: la cifra publicada con su signo; un cambio de signo declara su tratamiento). Vacío =
    desconocido (no cero); 0 solo con valor_fuente 0 declarado. con_signo: la magnitud puede ser negativa (solo la partida del arrendamiento
    operativo dentro de la fila 14, que lleva el signo de esa fila)."""
    s = ((decl.get("series") or {}).get(nombre)) or {}
    out, problemas = {}, []
    if not isinstance(s, dict):
        return {}, [f"series.{nombre} no es un objeto por año"]
    for k, e in s.items():
        try:
            y = int(k)
        except (TypeError, ValueError):
            problemas.append(f"series.{nombre}: clave de año no válida {k!r}")
            continue
        if y not in anios:
            problemas.append(f"series.{nombre}: el año {y} no está en la Historia del libro (fila 5)")
            continue
        if not isinstance(e, dict):
            problemas.append(f"series.{nombre}.{y}: se declara {{valor_fuente, signo, tratamiento, documento, pagina}}")
            continue
        vf, sg = Q(e.get("valor_fuente")), e.get("signo")
        if vf is None:
            problemas.append(f"series.{nombre}.{y}: valor_fuente no numérico")
            continue
        if sg not in (1, -1):
            problemas.append(f"series.{nombre}.{y}: signo sin declarar (1 o −1)")
            continue
        if "escala" in e and _escala_serie(e) is None:   # (F1-SERIES-ESCALA) la escala de la cifra impresa: solo los tres valores
            problemas.append(f"series.{nombre}.{y}: escala {e.get('escala')!r} no válida (se declara «unidades», «miles» o «millones»)")
            continue
        trat = re.sub(r"[\s.,;:()¡!¿?«»\"']+", " ", str(e.get("tratamiento") or "").lower()).strip()
        if sg == -1 and trat in SIN_TRATAMIENTO:
            problemas.append(f"series.{nombre}.{y}: signo −1 con el tratamiento «ninguno»: el cambio de signo se declara en «tratamiento»")
            continue
        if not str(e.get("documento") or "").strip() or e.get("pagina") in (None, ""):
            problemas.append(f"series.{nombre}.{y}: sin documento o página de la fuente")
            continue
        m = sg * vf
        if m < 0 and not con_signo:
            problemas.append(f"series.{nombre}.{y}: magnitud negativa ({float(m)}): una amortización o un pago no es negativo en el modelo")
            continue
        out[y] = m
    return out, problemas


# ----------------------------------------------------------------------------------------------------------- norma contable · US GAAP (ASC 842)
def norma_del_libro(L):
    """Norma que declara el libro (Control maestro L4) por la lista cerrada NORMA_DEL_LIBRO: «NIIF», «US_GAAP» o None (vacío o no reconocido)."""
    t = re.sub(r"\s+", " ", str(L.get("Control maestro!L4") or "")).strip()
    return NORMA_DEL_LIBRO.get(t.casefold()) if t else None


def norma_fase1_no_admitida(valor):
    """(ronda 2, R1-11) La norma contable que la fase 1 escribe en Control maestro L4 es un valor de vocabulario cerrado desde su origen (el campo
    «norma_contable» de fase1_v63.json): «IFRS» o «US GAAP» (las dos variantes históricas de los libros NIIF y «Otro», el tercer valor de la lista
    de la plantilla, también se admiten). Devuelve el motivo si el valor no es de la lista, o None si lo es o no se declara (vacío: no se escribe)."""
    t = re.sub(r"\s+", " ", "" if valor is None else str(valor)).strip()
    if not t or t.casefold() in NORMA_DEL_LIBRO or t.casefold() == "otro":
        return None
    return (f"«norma_contable» = {valor!r} en fase1_v63.json no es un valor de la lista cerrada: se escribe exactamente «IFRS» o «US GAAP» (la capa F1 no busca la "
            "norma dentro de un texto; «IFRS (EU)», «IFRS as adopted by the EU» o «U.S. GAAP» no son valores de la lista)")


def _evidencia_ok(d, con_cita=True):
    return (isinstance(d, dict) and bool(str(d.get("documento") or "").strip()) and d.get("pagina") not in (None, "")
            and (not con_cita or bool(str(d.get("cita") or "").strip())))


def leer_us(decl, anios):
    """(F1 · US GAAP, ASC 842) Lo que la declaración dice de los arrendamientos con US GAAP, con los OPERATIVOS y los FINANCIEROS por separado:
      - arrendamientos_us_gaap: registro; por clase, «existen» (true/false) con documento, página y cita; de los operativos, dónde están en
        el estado de flujos sus dos tramos no monetarios («amortizacion_rou» y «variacion_pasivo»: ubicacion, documento, página y cita) y si
        el coste lineal declarado tiene el mismo perímetro que los pagos («coste_comparable_con_los_pagos», ronda 2, R1-7); de los
        financieros, si la empresa publica su desglose («desglose»: «publicado» | «no_publicado», D-WM) y dónde está la amortización de su
        derecho de uso («amortizacion_rou.ubicacion»: «fila_8», por omisión, o «fuera_de_la_fila_8», R1-16);
      - las series SERIES_US y da_rou (con US GAAP, la amortización del derecho de uso de los FINANCIEROS dentro de la fila 8).
    Devuelve: op / fin (True, False o None = sin declarar), ub_decl (ubicación DECLARADA de cada tramo) y ub_am / ub_pas (ubicación efectiva;
    con «no_publicada» la de la hipótesis D-US1, fuera de las filas 8 y 14, y el tramo queda anotado en hipotesis_D_US1), rou_fin, a8
    (amortización del derecho de uso operativo dentro de la fila 8), rou8 = rou_fin + a8 (lo que A1/A2 excluyen de D_X), tramos_en_fila_14,
    retira_de_14 (un solo tramo dentro de la fila 14: su importe se retira del circulante), ajuste (lo que se retira por año), dos_en_14 y
    neto_14 (D-US2 bis: los dos tramos dentro; no se retira nada y el neto solo sirve para enseñar cuánto cambiaría contando los pagos),
    fin_como_deuda (D-WM) y fin_am_ub, y las faltas, incoherencias y evidencias que examinan las guardas. Vacío ≠ 0: una ubicación sin declarar
    deja a8 y rou8 sin valor."""
    b = decl.get("arrendamientos_us_gaap")
    faltas, incoh, evid, ausencias, hip = [], [], [], [], []
    U = {"bloque": isinstance(b, dict)}
    if not U["bloque"]:
        faltas.append("falta «arrendamientos_us_gaap»: si hay arrendamientos operativos y financieros (cada clase con su evidencia) y su registro")
    b = b if isinstance(b, dict) else {}
    U["registro_ok"] = _registro_ok(b.get("registro"))
    if U["bloque"] and not U["registro_ok"]:
        faltas.append("arrendamientos_us_gaap sin registro (fecha, persona, motivo): lo declara la persona, no el agente")
    op_d = b.get("operativos") if isinstance(b.get("operativos"), dict) else {}
    fin_d = b.get("financieros") if isinstance(b.get("financieros"), dict) else {}

    def existe(d, nombre):
        if not isinstance(d.get("existen"), bool):
            if U["bloque"]:
                faltas.append(f"arrendamientos_us_gaap.{nombre}.existen sin declarar (true o false): sin el desglose entre operativos y financieros no hay regla")
            return None
        if not _evidencia_ok(d):
            faltas.append(f"arrendamientos_us_gaap.{nombre}: sin documento, página y cita literal de que existen o de que no existen")
        else:
            evid.append((f"arrendamientos_us_gaap.{nombre}", d))
        return d["existen"]

    U["op"], U["fin"] = existe(op_d, "operativos"), existe(fin_d, "financieros")
    U["ub_decl"] = {"amortizacion_rou": None, "variacion_pasivo": None}
    U["ev"] = {"amortizacion_rou": {}, "variacion_pasivo": {}, "amortizacion_rou_financiero": {}}

    def ubicacion(clave):
        d = op_d.get(clave) if isinstance(op_d.get(clave), dict) else {}
        et = f"arrendamientos_us_gaap.operativos.{clave}"
        u = d.get("ubicacion")
        U["ev"][clave] = d
        if u is None:
            faltas.append(f"{et}.ubicacion sin declarar ({' | '.join(UBICACIONES[clave])})")
            return None
        if not isinstance(u, str) or u not in UBICACIONES[clave]:
            incoh.append(f"{et}.ubicacion {u!r} no admitida ({' | '.join(UBICACIONES[clave])})")
            return None
        U["ub_decl"][clave] = u
        if u == "no_publicada":
            # D-US1: la empresa no publica la línea → hipótesis general declarada (fuera de las filas 8 y 14). Se cita la página examinada
            if not _evidencia_ok(d, con_cita=False):
                faltas.append(f"{et}: «no_publicada» sin el documento y la página del estado de flujos que se examinó")
            else:
                ausencias.append((et, d))
            hip.append(clave)
            return "fuera_de_las_filas_8_y_14"
        if not _evidencia_ok(d):
            faltas.append(f"{et}: sin documento, página y cita literal de la línea que lo muestra")
        else:
            evid.append((et, d))
        return u

    U["ub_am"] = ubicacion("amortizacion_rou") if U["op"] else None
    U["ub_pas"] = ubicacion("variacion_pasivo") if U["op"] else None
    U["hipotesis_D_US1"] = hip
    # (ronda 2, R1-7) el coste lineal que se declara es el «operating lease cost» de los contratos capitalizados, el mismo perímetro que los pagos (sin
    # corto plazo ni variable). Si la empresa no lo separa, se declara que no es comparable, con su motivo, y la diferencia con los pagos no se calcula
    cc = op_d.get("coste_comparable_con_los_pagos")
    U["coste_comparable"], U["coste_no_comparable_motivo"] = True, None
    if cc is False:
        U["coste_comparable"] = False
        U["coste_no_comparable_motivo"] = str(op_d.get("coste_no_comparable_motivo") or "").strip() or None
        if U["op"] and not U["coste_no_comparable_motivo"]:
            faltas.append("arrendamientos_us_gaap.operativos.coste_comparable_con_los_pagos = false sin «coste_no_comparable_motivo» (qué lleva el coste publicado "
                          "que no está en los pagos)")
    elif cc is not None and cc is not True:
        incoh.append(f"arrendamientos_us_gaap.operativos.coste_comparable_con_los_pagos {cc!r} no es true ni false")
    # financieros: desglose publicado (como NIIF 16) o no publicado (D-WM: como deuda y activos propios), y dónde está la amortización de su derecho de uso
    U["fin_como_deuda"], U["fin_am_ub"] = False, "fila_8"
    dg, fa = fin_d.get("desglose"), fin_d.get("amortizacion_rou")
    if U["fin"] is True and dg is not None:
        if not isinstance(dg, str) or dg not in DESGLOSES_FIN:
            incoh.append(f"arrendamientos_us_gaap.financieros.desglose {dg!r} no admitido ({' | '.join(DESGLOSES_FIN)})")
        elif dg == "no_publicado":
            U["fin_como_deuda"] = True
    if U["fin"] is True and fa is not None:
        et = "arrendamientos_us_gaap.financieros.amortizacion_rou"
        if not isinstance(fa, dict) or not isinstance(fa.get("ubicacion"), str) or fa.get("ubicacion") not in UBICACIONES_FIN:
            incoh.append(f"{et}: se declara {{ubicacion ({' | '.join(UBICACIONES_FIN)}), documento, pagina, cita}}")
        elif U["fin_como_deuda"]:
            incoh.append(f"{et}: con el desglose «no_publicado» (D-WM) no se declara dónde está esa amortización (queda dentro de la propia)")
        elif fa["ubicacion"] == "fuera_de_la_fila_8":
            U["fin_am_ub"], U["ev"]["amortizacion_rou_financiero"] = "fuera_de_la_fila_8", fa
            if not _evidencia_ok(fa):
                faltas.append(f"{et}: «fuera_de_la_fila_8» sin documento, página y cita literal")
            else:
                evid.append((et, fa))
    S, probl = {}, []
    for s in SERIES_US:
        S[s], p = leer_serie(decl, s, anios, con_signo=(s in SERIES_US_CON_SIGNO))
        probl += p
    rou_decl, _ = leer_serie(decl, "da_rou", anios)   # sus problemas ya los recoge la lectura general de SERIES
    cero = {y: Fr(0) for y in anios}

    def hay(*series):
        return any(v != 0 for s_ in series for v in s_.values())

    # financieros: como NIIF 16 (amortización del derecho de uso dentro de la fila 8 y principal en C49), salvo declaración expresa
    if U["fin"] is False:
        if hay(rou_decl, S["pagos_arr_financiero_principal"], S["caja_pagada_arr_financiero"], S["gasto_arr_financiero"], S["da_rou_financiero_fuera"]):
            incoh.append("financieros.existen = false y hay importes en series.da_rou o en series.pagos_arr_financiero_principal (o en caja_pagada_arr_financiero, "
                         "gasto_arr_financiero o da_rou_financiero_fuera)")
        U["rou_fin"] = dict(cero)
    elif U["fin_como_deuda"]:
        # D-WM: su amortización queda dentro de la propia (nada se excluye de D_X) y sus pagos no se restan de la caja base
        if hay(rou_decl, S["pagos_arr_financiero_principal"], S["da_rou_financiero_fuera"]):
            incoh.append("financieros.desglose = «no_publicado» (D-WM) y hay importes en series.da_rou, pagos_arr_financiero_principal o da_rou_financiero_fuera: "
                         "si la empresa publica el desglose manda el dato (desglose «publicado»)")
        U["rou_fin"] = dict(cero)
    elif U["fin_am_ub"] == "fuera_de_la_fila_8":
        if hay(rou_decl):
            incoh.append("financieros.amortizacion_rou.ubicacion = «fuera_de_la_fila_8» y hay importes en series.da_rou (la que está DENTRO de la fila 8)")
        U["rou_fin"] = dict(cero)
    else:
        U["rou_fin"] = dict(rou_decl)
        if hay(S["da_rou_financiero_fuera"]):
            incoh.append("series.da_rou_financiero_fuera con importes, y la amortización del derecho de uso financiero no está declarada fuera de la fila 8")
    if U["fin"] is True and not U["fin_como_deuda"] and hay(S["caja_pagada_arr_financiero"], S["gasto_arr_financiero"]):
        incoh.append("series.caja_pagada_arr_financiero o gasto_arr_financiero con importes, y el desglose de los financieros no está declarado «no_publicado» (D-WM)")
    # operativos: amortización del derecho de uso dentro de la fila 8 (si lo está, A1/A2 la excluyen de D_X)
    conocida = U["op"] is False or (U["op"] is True and U["ub_am"] is not None)
    if U["op"] is True and U["ub_am"] == "fila_8":
        U["a8"] = dict(S["da_rou_operativo"])
    else:
        if hay(S["da_rou_operativo"]):
            incoh.append("series.da_rou_operativo con importes, y la amortización del derecho de uso operativo no está declarada dentro de la fila 8")
        U["a8"] = dict(cero) if conocida else {}
    U["rou8"] = {y: U["rou_fin"][y] + U["a8"][y] for y in anios if y in U["rou_fin"] and y in U["a8"]}
    # operativos dentro de la fila 14. Un solo tramo dentro: su importe se retira del circulante que usa la reinversión (D-US2: se cuentan los pagos,
    # una vez). Los dos dentro (D-US2 bis, ronda 2): no se retira nada; se publica el valor de la hoja, que cuenta el coste contable, y el neto que
    # llevan (la línea neta publicada o, si no la hay, pagos − coste lineal) solo sirve para enseñar cuánto cambiaría contando los pagos
    en14 = [k for k, u in (("amortizacion_rou", U["ub_am"]), ("variacion_pasivo", U["ub_pas"])) if u == "fila_14"] if U["op"] is True else []
    aj, neto, derivado = {}, {}, []
    if len(en14) == 1:
        aj = dict(S["circulante_arr_operativo"])
    elif len(en14) == 2:
        for y in anios:
            if y in S["circulante_arr_operativo"]:
                neto[y] = S["circulante_arr_operativo"][y]
            elif U["coste_comparable"] and y in S["pagos_arr_operativo"] and y in S["coste_arr_operativo"]:
                neto[y] = S["pagos_arr_operativo"][y] - S["coste_arr_operativo"][y]   # identidad de ASC 842: los dos tramos netos = pagos − coste lineal
                derivado.append(y)
    elif hay(S["circulante_arr_operativo"]):
        incoh.append("series.circulante_arr_operativo con importes, y ningún tramo del arrendamiento operativo está declarado dentro de la fila 14")
    if U["op"] is False and hay(S["pagos_arr_operativo"], S["coste_arr_operativo"], S["pasivo_arr_operativo"]):
        incoh.append("operativos.existen = false y hay importes en sus series")
    U.update({"tramos_en_fila_14": en14, "retira_de_14": len(en14) == 1, "dos_en_14": len(en14) == 2, "ajuste": aj, "neto_14": neto,
              "neto_14_derivado": derivado, "S": S, "problemas_series": probl, "faltas": faltas, "incoherencias": incoh, "evidencias": evid,
              "ausencias": ausencias})
    return U


def rou_fila8(decl, anios):
    """Amortización de derechos de uso dentro de la fila 8 que A1 y A2 excluyen de D_X (la que el libro V6.3.1 lleva en la fila 86): con NIIF,
    series.da_rou; con US GAAP, la de los financieros más la de los operativos que esté declarada dentro de la fila 8."""
    if _valor(decl, "norma_contable")[0] == "US_GAAP":
        return leer_us(decl, anios)["rou8"]
    return leer_serie(decl, "da_rou", anios)[0]


def _guarda_norma(G, L, decl):
    """F1-NORMA: la norma es un valor cerrado en la declaración (NORMAS) y en el libro (NORMA_DEL_LIBRO), y los dos dicen lo mismo."""
    norma, reg_norma = _valor(decl, "norma_contable")
    l4 = re.sub(r"\s+", " ", str(L.get("Control maestro!L4") or "")).strip()
    nl = norma_del_libro(L)
    if l4.casefold() == "otro":
        # (cierre de la ronda 2, interpretación 5) «Otro» es un valor de la lista de la plantilla, pero F1 no tiene regla para otras normas: es un límite del
        # modelo, no un dato que falte (ningún dato lo arregla sin cambiar la norma). Manda sobre lo que falte en la declaración (clase «norma»)
        G.add("F1-NORMA", True, "BLOQUEA", "MODELO NO APLICABLE", "el libro declara «Otro» como norma contable (Control maestro L4): F1 solo tiene reglas para "
              "NIIF y US GAAP; con otra norma el resultado del motor no se usa para una conclusión (límite del modelo, no un dato que falte)", "generalidad", clase="norma")
    elif norma is None:
        G.add("F1-NORMA", True, "BLOQUEA", "INCOMPLETO", "norma contable sin declarar en la declaración F1 (entrada obligatoria)", "generalidad")
    elif norma not in NORMAS:
        G.add("F1-NORMA", True, "BLOQUEA", "MODELO NO APLICABLE", f"norma contable {norma!r} no soportada por F1 (valor cerrado: {' o '.join(NORMAS)})", "generalidad")
    elif not l4:
        G.add("F1-NORMA", True, "BLOQUEA", "INCOMPLETO", "el libro no declara la norma contable (Control maestro L4)", "generalidad")
    elif nl is None:
        G.add("F1-NORMA", True, "BLOQUEA", "DATOS INVÁLIDOS", f"el libro dice {l4!r} en Control maestro L4, que no es un valor reconocido de la norma (lista cerrada de "
              "valores exactos: IFRS, NIIF, IFRS (IFRS-EU), IFRS (adoptadas por la Unión Europea), US GAAP); no se busca la norma dentro de un texto", "generalidad")
    elif nl != norma:
        G.add("F1-NORMA", True, "BLOQUEA", "DATOS INVÁLIDOS", f"mezcla de normas: la declaración F1 dice {norma} y el libro dice {l4!r} (Control maestro L4)", "generalidad")
    else:
        G.add("F1-NORMA", False, None, None, f"{'NIIF' if norma == 'NIIF' else 'US GAAP'} declarada; libro: {l4}", "generalidad")
    if norma is not None and not _registro_ok(reg_norma):
        G.add("F1-REGISTRO", True, "BLOQUEA", "INCOMPLETO", "norma_contable sin registro (fecha, persona, motivo)", "E2 (registro de cada declaración)")
    return norma


# ----------------------------------------------------------------------------------------------------------- motor A (Convenciones V6.3)
def motor(V0, m0, tau, f, g15, m_obj, s2c, g_inf, roic, X=None, X11=Fr(0)):
    """flujo_t = V_t·[m_t(1−τ) − f] − ΔV_t/S2C − X_t (t = 1…10); año 11 = V₁₀(1+g∞)[m_obj(1−τ)(1 − g∞/ROIC) − f] − X₁₁ (E3).
    Sin términos explícitos es exactamente el motor A del libro (Convenciones §1–§3)."""
    X = X or {}
    V_prev, flujos, V = V0, [], []
    for t in range(1, 11):
        g_t = g15 if t <= 5 else g15 - (g15 - g_inf) * Fr(t - 5, 5)
        Vt = V_prev * (1 + g_t)
        mt = m0 + (m_obj - m0) * Fr(min(t, 5), 5)
        xt = X(t, Vt) if callable(X) else X.get(t, Fr(0))
        flujos.append(Vt * (mt * (1 - tau) - f) - (Vt - V_prev) / s2c - xt)
        V.append(Vt)
        V_prev = Vt
    x11 = X11(V[-1] * (1 + g_inf)) if callable(X11) else X11
    terminal = V[-1] * (1 + g_inf) * (m_obj * (1 - tau) * (1 - g_inf / roic) - f) - x11
    return {"flujos": flujos, "flujo_11": terminal, "V": V}


# ----------------------------------------------------------------------------------------------------------- evaluación
class Guardas:
    def __init__(self):
        self.lista = []

    def add(self, gid, salta, severidad, efecto, detalle, decision, clase=None):
        """clase (solo si bloquea): «datos» (falta de datos o de decisión → pendiente_de_datos), «modelo» (límite del modelo),
        «implementacion» (fallo de la réplica o de K3), «norma» (norma contable para la que F1 no tiene regla: límite del modelo aunque falten datos)."""
        if clase is None:
            clase = {"INCOMPLETO": "datos", "DATOS INVÁLIDOS": "datos", "FUERA DEL DOMINIO": "datos"}.get(efecto, "modelo")
        self.lista.append({"id": gid, "salta": bool(salta), "severidad": severidad if salta else None, "efecto": efecto if salta else None,
                           "detalle": detalle, "decision": decision, "clase": clase if (salta and severidad == "BLOQUEA") else None})

    def bloquean(self):
        return [g for g in self.lista if g["salta"] and g["severidad"] == "BLOQUEA"]


def evaluar(L, decl, motor_libro=None, carpeta=None):
    """Evaluación F1 completa. L: valores del libro (leer_libro). decl: declaración (dict). Devuelve el resultado (dict, serializable)."""
    G = Guardas()
    if not isinstance(decl, dict):
        raise ErrorDeclaracion("la declaración no es un objeto JSON")
    desconocidas = sorted(set(decl) - CLAVES_DECL)
    res = {"version": VERSION, "fecha": dt.date.today().isoformat(), "libro_sha256": L.get("sha256"),
           "declaracion_sha256": huella_declaracion(decl),
           "apto_para_dinero_real": False, "parametros_sin_valor_adoptado": PARAMETROS_SIN_VALOR, "convencion_tau": CONVENCION_TAU}
    motor_ = motor_libro or L.get("Diagnóstico V6!C5")
    res["motor_del_libro"] = motor_
    # (ronda 2, R1-14) una clave que tiene que ser un objeto o una lista y no lo es no hace fallar el programa: DATOS INVÁLIDOS (la huella de la
    # declaración ya está tomada sobre el original)
    decl, mal_formadas, notas_series = _declaracion_bien_formada(decl)
    if notas_series:
        # (cierre de la ronda 2, R2-4) un texto dentro de «series» en una clave que no es una serie es una nota: no se ignora en silencio ni bloquea
        res["notas_en_series"] = list(notas_series)
        G.add("F1-DECLARACION", True, "INFORMA", "INFORMA", "notas de texto dentro de «series» (no son series: no entran en el cálculo y quedan a la vista): "
              + ", ".join(notas_series)[:300], "—")
    if motor_ == "B":
        nd, nl = _valor(decl, "norma_contable")[0], norma_del_libro(L)
        # (F1 · US GAAP) con el motor B y US GAAP se evalúa solo el puente de deuda (el pasivo por arrendamiento operativo no es deuda del puente).
        # (ronda 2, R1-1) También si el libro no dice una norma de la lista cerrada (vacío, «U.S. GAAP», «Otro»…) en un expediente de la 4.15: no
        # se puede descartar US GAAP y F1-NORMA bloquea (falla en cerrado, como el motor A)
        if nd == "US_GAAP" or nl == "US_GAAP" or (nl is None and (carpeta is None or _expediente_415(carpeta))):
            if mal_formadas:
                G.add("F1-DECLARACION", True, "BLOQUEA", "DATOS INVÁLIDOS", "declaración mal formada: " + "; ".join(mal_formadas)[:600], "—")
            return _evaluar_puente_motor_b(L, decl, res, G, desconocidas, carpeta)
    if motor_ != "A":
        res.update({"aplica": False, "motivo": f"el libro usa el motor {motor_!r}: F1 solo afecta al motor A (T11)", "guardas": [],
                    "bloquea": False, "utilizable_para_conclusion": None})
        return res
    res["aplica"] = True
    if desconocidas:
        G.add("F1-DECLARACION", True, "BLOQUEA", "DATOS INVÁLIDOS",
              f"claves no reconocidas en la declaración: {', '.join(desconocidas)} (no se ignoran en silencio; las entradas registradas "
              "del FCF base, C46–C52, no se declaran aquí)", "—")
    if mal_formadas:
        G.add("F1-DECLARACION", True, "BLOQUEA", "DATOS INVÁLIDOS", "declaración mal formada: " + "; ".join(mal_formadas)[:600], "—")

    # ---------------------------------------------------------------- entradas del libro
    anios_raw = _hist(L, 5)
    if not all(isinstance(a, (int, float)) for a in anios_raw):
        raise ErrorDeclaracion("Historia C5:L5 no tiene los diez años")
    anios = [int(a) for a in anios_raw]
    col = dict(zip(anios, COLS))
    H = {n: dict(zip(anios, [Q(x) for x in _hist(L, fila)])) for n, fila in
         (("V", 6), ("EBIT", 7), ("DA", 8), ("tau", 10), ("capex", 12), ("adq", 13), ("dwc", 14), ("princ", 17))}
    n = L.get("Historia!C57")
    n = int(n) if isinstance(n, (int, float)) and int(n) == n else None
    C70, C58, C52, C53 = (Q(L.get(f"Historia!{c}")) for c in ("C70", "C58", "C52", "C53"))
    C49 = Q(L.get("Análisis!C49"))
    V0, m0_libro = Q(L.get("Historia!C44")), Q(L.get("Historia!C48"))
    if n is None or C70 is None or (C58 is None and not _f_vacia_v631(L)) or V0 is None:
        raise ErrorDeclaracion("el libro no tiene f calculada (Historia C57, C58, C70 o C44 vacías): el motor A no es calculable")
    ventana = anios[-n:]
    horiz = anios[-5:]
    ant = anios[-6]
    for y in ventana:
        for k in ("V", "EBIT", "DA", "tau", "capex", "dwc"):
            if H[k][y] is None:
                raise ErrorDeclaracion(f"Historia {k} {y} vacía dentro de la ventana de f")
    res["entradas_registradas"] = {"Historia!C70 (FCF base que calibra f)": fl(C70), "Análisis!C48": fl(Q(L.get("Análisis!C48"))),
                                   "Análisis!C49 (principal de arrendamientos)": fl(C49), "Análisis!C52": fl(Q(L.get("Análisis!C52"))),
                                   "Historia!C58 (f del libro, A0)": fl(C58, 15), "Historia!C52 (τ de 5 años)": fl(C52, 6),
                                   "Historia!C53 (S2C, A0)": fl(C53), "V0": fl(V0), "m0 del libro": fl(m0_libro, 15),
                                   "ventana": ventana, "horizonte_ancla": horiz,
                                   "nota": "entradas registradas del FCF base: no cambian con F1 (E0.3, T10); la capa F1 no las escribe"}

    # ---------------------------------------------------------------- norma contable (entrada declarada)
    norma = _guarda_norma(G, L, decl)
    us = norma == "US_GAAP"   # (F1 · US GAAP) arrendamientos operativos y financieros por separado (leer_us); con NIIF nada cambia

    # ---------------------------------------------------------------- series declaradas
    S, probl_series = {}, []
    for s in SERIES:
        S[s], p = leer_serie(decl, s, anios)
        probl_series += p
    rou, ppa, pagos = S["da_rou"], S["da_ppa"], S["pagos_arrendamiento"]
    # rou8: la amortización de derechos de uso DENTRO de la fila 8, la que A1 y A2 excluyen de D_X. Con NIIF es la serie da_rou (el mismo objeto).
    # (F1 · US GAAP) rou pasa a ser la de los arrendamientos FINANCIEROS (la que se relaciona con C49: V-F1a, V-F1b, V-F1m y F1-M-SIM) y rou8 le
    # suma la de los operativos que esté declarada dentro de la fila 8
    rou8, U, us_f = rou, None, None
    _ser = decl.get("series") if isinstance(decl.get("series"), dict) else {}
    if us:
        U = leer_us(decl, anios)
        probl_series += U["problemas_series"]
        rou, rou8 = U["rou_fin"], U["rou8"]
    elif norma == "NIIF" and (decl.get("arrendamientos_us_gaap") is not None or any(_ser.get(s) for s in SERIES_US)):
        G.add("F1-US-MEZCLA", True, "BLOQUEA", "DATOS INVÁLIDOS", "mezcla de normas: la declaración dice NIIF y lleva «arrendamientos_us_gaap» o series propias "
              f"de US GAAP ({', '.join(SERIES_US)}): no se ignoran en silencio", "generalidad · US GAAP")
    # V-F1e: invariantes de E1 y signos
    inv = []
    for y in anios:
        da = H["DA"][y]
        if da is None:
            continue
        if y in rou8 and rou8[y] > da:
            inv.append(f"{y}: D&A ROU {float(rou8[y])} > D&A total {float(da)}")
        if y in ppa and ppa[y] > da:
            inv.append(f"{y}: PPA {float(ppa[y])} > D&A total {float(da)}")
        if y in rou8 and y in ppa and rou8[y] + ppa[y] > da:
            inv.append(f"{y}: D&A ROU + PPA {float(rou8[y] + ppa[y])} > D&A total {float(da)}")
    G.add("V-F1e", bool(inv or probl_series), "BLOQUEA", "DATOS INVÁLIDOS",
          "; ".join(probl_series + inv) if (inv or probl_series) else "invariantes de E1 y signos declarados: conformes", "(1a)")

    # ---------------------------------------------------------------- perímetros declarados
    per, reg_per = _valor(decl, "perimetro_reinversion")
    pmar, reg_mar = _valor(decl, "perimetro_margen")
    ppal, reg_pal = _valor(decl, "perimetro_palancas_s2c")
    proi, reg_roi = _valor(decl, "perimetro_roic")
    for nombre, val, reg in (("perimetro_reinversion", per, reg_per), ("perimetro_margen", pmar, reg_mar),
                             ("perimetro_palancas_s2c", ppal, reg_pal), ("perimetro_roic", proi, reg_roi)):
        if val is not None and not _registro_ok(reg):
            G.add("F1-REGISTRO", True, "BLOQUEA", "INCOMPLETO", f"{nombre} sin registro (fecha, persona, motivo): es una decisión, no la rellena el agente",
                  "E2 (registro de cada declaración)")
    if per is None:
        G.add("F1-PERIMETRO", True, "BLOQUEA", "INCOMPLETO", "perimetro_reinversion sin declarar", "(1a)")
    elif per not in PERIMETROS:
        G.add("F1-PERIMETRO", True, "BLOQUEA", "DATOS INVÁLIDOS", f"perimetro_reinversion {per!r} no admitido ({', '.join(PERIMETROS)})", "(1a)")
        per = None

    sum_rou_w = sum((rou[y] for y in ventana if y in rou), Fr(0))
    rou_vacio_w = [y for y in ventana if y not in rou]
    ppa_vacio_w = [y for y in ventana if y not in ppa]
    c49_pos = C49 is not None and C49 > 0
    rou_pos = sum_rou_w > 0
    # V-F1b: C49 > 0 y D&A ROU vacía en algún año de la ventana (vacío ≠ 0)
    vf1b = c49_pos and bool(rou_vacio_w)
    G.add("V-F1b", vf1b, "BLOQUEA", "INCOMPLETO",
          (f"C49 = {float(C49)} > 0 y D&A ROU vacía en {rou_vacio_w}: vacío no es cero" if vf1b else "D&A ROU declarada en la ventana o C49 = 0"), "(1a)")
    # A0: los cuatro casos de W3 (V-F1a, admisible, V-F1m) y, además, D&A ROU desconocida con C49 = 0 (vacío ≠ 0: A0 no se admite)
    if per == "A0_total":
        umbral_decl = decl.get("umbral_v_f1a")
        if rou_vacio_w and not c49_pos:
            G.add("V-F1b", True, "BLOQUEA", "INCOMPLETO",
                  f"perímetro A0 con C49 = 0 y D&A ROU vacía en {rou_vacio_w}: A0 solo se admite con la D&A ROU comprobada a cero (vacío ≠ 0)", "(1a)")
        G.add("V-F1a", rou_pos and c49_pos, "BLOQUEA", "MODELO NO APLICABLE",
              ("coste de arrendamiento contado dos veces en la proyección: D&A ROU de la ventana "
               f"{float(sum_rou_w)} > 0 y C49 = {float(C49)} > 0, con perímetro A0 (sin umbral adoptado: bloquea con cualquier importe)")
              if (rou_pos and c49_pos) else "no salta (la ausencia de V-F1a no admite A0 por sí sola)", "(1a)")
        # (ronda 2, R1-16) con US GAAP, C49 positivo y la amortización del derecho de uso financiero a cero no es un conflicto si está declarada fuera
        # de la fila 8 (con su evidencia): D_X no la lleva
        dom = (rou_pos != c49_pos) and not rou_vacio_w and not (us and U["fin"] is True and U["fin_am_ub"] == "fuera_de_la_fila_8" and c49_pos and not rou_pos)
        G.add("V-F1m", dom, "BLOQUEA", "FUERA DEL DOMINIO",
              (f"solo uno de D&A ROU ({float(sum_rou_w)}) y C49 ({float(C49) if C49 is not None else None}) es positivo: entradas incompletas o en "
               "conflicto que hay que aclarar; no se afirma doble cómputo") if dom else "no salta", "(1a)")
        if umbral_decl is not None:
            G.add("F1-PARAM", True, "BLOQUEA", "INCOMPLETO",
                  f"umbral de V-F1a declarado ({umbral_decl!r}) sin decisión adoptada: no se aplica; V-F1a bloquea con cualquier importe", "umbral V-F1a (sin decidir)")
    else:
        G.add("V-F1a", False, None, None, "no aplica: el perímetro no es A0", "(1a)")
        G.add("V-F1m", False, None, None, "no aplica: el perímetro no es A0", "(1a)")
    # (revisión F1-IMPL, H4) guarda simétrica de V-F1m: excluir la ROU de D_X solo es coherente si los pagos están dentro del FCF base.
    # Con A1/A2/A3, D&A ROU > 0 y C49 cero o vacío, el alquiler se omitiría en la proyección: fuera del dominio (adición a E5, para la persona)
    sim = per in ("A1_sin_ROU", "A2_propio", "A3_estimado") and rou_pos and not c49_pos
    G.add("F1-M-SIM", sim, "BLOQUEA", "FUERA DEL DOMINIO",
          (f"perímetro {per} con D&A ROU {float(sum_rou_w)} > 0 y C49 = {None if C49 is None else float(C49)} (cero o vacío): f devolvería la ROU sin "
           "que los pagos estén en el FCF base; el alquiler no se contaría ninguna vez") if sim else "no salta", "(1a) · simétrica de V-F1m")
    # (H11) C49 vacío no es cero; una ROU declarada a cero con principal (fila 17) o pasivo (fila 23) positivos en la Historia es un conflicto
    if C49 is None:
        G.add("F1-C49", True, "BLOQUEA", "INCOMPLETO", "Análisis C49 (principal de arrendamientos del FCF base) vacío: vacío no es cero", "(1a)")
    fila17 = [y for y in ventana if (H["princ"][y] or 0) > 0]
    fila23 = [y for y in ventana if (Q(L.get(f"Historia!{col[y]}23")) or 0) > 0]
    if us:
        # (F1 · US GAAP) la fila 17 es el principal de los financieros y la fila 23 puede llevar el pasivo de los operativos: hay conflicto si la
        # fila 17 es positiva sin derecho de uso financiero, o si la fila 23 es positiva sin arrendamientos de ninguna clase
        fila23 = fila23 if (U["op"] is False and U["fin"] is False) else []
        # (ronda 2, R1-16 y D-WM) tampoco hay conflicto con la fila 17 si la amortización del derecho de uso financiero está declarada fuera de la
        # fila 8 (declarar la verdad no bloquea) o si los financieros se tratan como deuda (su amortización queda dentro de la propia)
        if U["fin"] is True and (U["fin_como_deuda"] or U["fin_am_ub"] == "fuera_de_la_fila_8"):
            fila17 = []
    rou_cero_conflicto = bool(rou) and not rou_vacio_w and sum_rou_w == 0 and (fila17 or fila23)
    G.add("F1-ROU-HISTORIA", rou_cero_conflicto, "BLOQUEA", "DATOS INVÁLIDOS",
          (f"D&A ROU declarada a cero en la ventana y la Historia muestra arrendamientos (principal fila 17 en {fila17}; pasivo fila 23 en {fila23})"
           # (ronda 2, R1-16) con US GAAP la amortización del derecho de uso financiero puede no estar dentro de la D&A: se declara así, no con un cero
           + ("; con US GAAP, si la amortización del derecho de uso de los arrendamientos financieros no está dentro de la D&A (fila 8), no se declara da_rou a cero: "
              "se declara «financieros.amortizacion_rou.ubicacion»: «fuera_de_la_fila_8», con su evidencia y su cifra publicada (series.da_rou_financiero_fuera); y si "
              "la empresa no desglosa sus arrendamientos financieros, «financieros.desglose»: «no_publicado» (D-WM)" if us else ""))
          if rou_cero_conflicto else "sin conflicto entre la ROU declarada y las filas 17 y 23 de la Historia", "(1a)")
    if us:
        us_f = _guardas_us(G, L, U, decl, anios, ventana, horiz, per, C49, col)
        _contraste_us(G, decl, carpeta, U, sorted(set(ventana) | set(horiz)), rou_pos)

    # (2)(i): la PPA no es un desembolso de reposición. A0 y A1 la tratan como reposición (D_X la contiene)
    sum_ppa_w = sum((ppa[y] for y in ventana if y in ppa), Fr(0))
    if per in ("A0_total", "A1_sin_ROU"):
        if ppa_vacio_w:
            G.add("F1-2i", True, "BLOQUEA", "INCOMPLETO",
                  f"perímetro {per} con la PPA vacía en {ppa_vacio_w}: no se puede comprobar la política (2)(i) (vacío ≠ 0)", "(2)(i)")
        else:
            G.add("F1-2i", sum_ppa_w > 0, "BLOQUEA", "MODELO NO APLICABLE",
                  (f"perímetro {per} con PPA {float(sum_ppa_w)} > 0 en la ventana: trata la amortización PPA como reposición, contra la política "
                   "(2)(i) aprobada; la combinación no está cubierta por las decisiones (no se resuelve aquí)") if sum_ppa_w > 0 else "PPA = 0 en la ventana", "(2)(i)")
    else:
        G.add("F1-2i", False, None, None, "el perímetro no trata la PPA como reposición", "(2)(i)")

    # ---------------------------------------------------------------- normalización N1 (5a) · V-F1l · parámetros sin valor
    norm = decl.get("normalizacion") or {}
    ajustes = norm.get("ajustes") or []
    vf1l, aj_ok, param_pend = [], {}, []
    if norm.get("deducir_diagnostico_partidas_puntuales"):
        vf1l.append("se pide deducir el diagnóstico de partidas puntuales (27,936 en Elis) como si fuera un ajuste: es un diagnóstico, no una regla")
    bai_d, imp_d = {}, {}
    for nombre, dst in (("bai", bai_d), ("gasto_impuesto", imp_d)):
        for k, e in (norm.get(nombre) or {}).items():
            vv = Q(e.get("valor")) if isinstance(e, dict) else Q(e)
            if vv is None or not isinstance(e, dict) or not str(e.get("documento") or "").strip():
                vf1l.append(f"normalizacion.{nombre}.{k}: valor o fuente sin declarar")
                continue
            dst[int(k)] = vv
    for i, a in enumerate(ajustes):
        if not isinstance(a, dict):
            vf1l.append(f"ajuste {i}: no es un objeto")
            continue
        regla = a.get("regla")
        y = a.get("anio")
        imp = Q(a.get("importe"))
        falta = [k for k in ("partida", "fuente", "regla_fiscal", "ubicacion_caja") if not a.get(k)]
        if a.get("tipo") == "diagnostico":
            vf1l.append(f"ajuste {i}: un diagnóstico no es un ajuste")
            continue
        if a.get("tipo") == "actualizacion_financiera_earnout":
            continue   # no es un ajuste del EBIT: opción de N1 sin decidir (variante, abajo)
        if regla not in REGLAS_NORMALIZACION:
            vf1l.append(f"ajuste {i} ({a.get('partida')}): regla {regla!r} no aprobada (solo N1; N2 pendiente; ninguna partida se normaliza por su etiqueta)")
            continue
        if falta or imp is None or not isinstance(y, int):
            vf1l.append(f"ajuste {i} ({a.get('partida')}): faltan {', '.join(falta) or 'importe o año'}")
            continue
        if a.get("regla_fiscal") != REGLAS_NORMALIZACION[regla]:
            vf1l.append(f"ajuste {i}: la regla fiscal de N1 es «sin efecto en el gasto por impuesto» (no_deducible), no {a.get('regla_fiscal')!r}")
            continue
        if y not in anios:
            vf1l.append(f"ajuste {i}: el año {y} no está en la Historia")
            continue
        if y not in bai_d or y not in imp_d:
            vf1l.append(f"ajuste {i}: N1 recalcula el tipo de {y} (gasto ÷ BAI, 4 decimales): faltan el BAI o el gasto por impuesto declarados de {y}")
            continue
        aj_ok.setdefault(y, []).append(imp)
    tau_anios = anios[-5:]
    fuera = sorted(y for y in aj_ok if y not in ventana)
    act = [a for a in ajustes if isinstance(a, dict) and a.get("tipo") == "actualizacion_financiera_earnout"]
    act_ok = {}
    for a in act:
        y, imp = a.get("anio"), Q(a.get("importe"))
        if isinstance(y, int) and imp is not None and a.get("fuente") and y in bai_d and y in imp_d:
            act_ok.setdefault(y, []).append(imp)
        else:
            vf1l.append(f"actualización financiera del earnout ({y}): importe, fuente, BAI o gasto por impuesto sin declarar")
    if aj_ok:
        if not norm.get("margen_objetivo_sin_ajustes"):
            vf1l.append("N1 exige el margen objetivo declarado sin esos ajustes (condición de 5a): sin declarar")
        # (revisión, H9) el alcance de N1 a los ejercicios del τ fuera de la ventana no está decidido: no se elige por omisión
        param_pend.append(f"alcance de N1 a los ejercicios del τ fuera de la ventana sin decisión adoptada (declarados fuera de la ventana: {fuera or 'ninguno'}); "
                          "no se elige por omisión" + ("; se calculan las variantes" if fuera else ""))
        if act or norm.get("actualizacion_financiera_earnout_declarada") is not False:
            param_pend.append("actualización financiera del earnout (N1 alcanza o no el BAI que da el tipo): sin decisión adoptada; "
                              "o se declara expresamente que no existe (actualizacion_financiera_earnout_declarada: false)")
    G.add("V-F1l", bool(vf1l), "BLOQUEA", "INCOMPLETO", "; ".join(vf1l) if vf1l else
          ("ajustes N1 con fuente, regla fiscal y caja" if aj_ok else "sin ajustes de normalización (el diagnóstico se muestra como diagnóstico)"), "(5a)")
    if param_pend:
        G.add("F1-PARAM", True, "BLOQUEA", "INCOMPLETO", " · ".join(param_pend), "(5a) opciones sin decidir")

    def tasas_y_ebit(con_fuera, con_act=False):
        tau, ebit = {}, {}
        for y in anios:
            ebit[y] = H["EBIT"][y]
            tau[y] = H["tau"][y]
            ajs = aj_ok.get(y) if (y in ventana or con_fuera) else None
            dB = -sum(act_ok.get(y, []), Fr(0)) if (con_act and (y in ventana or con_fuera)) else Fr(0)
            if ajs or dB:
                dE = -sum(ajs or [], Fr(0))       # sacar la partida del EBIT y del BAI de su año
                if y in ventana:
                    ebit[y] = H["EBIT"][y] + dE
                tau[y] = r4(imp_d[y] / (bai_d[y] + dE + dB))   # gasto sin cambios (no deducible)
        return tau, ebit

    # ---------------------------------------------------------------- compras (4b) · transición (5b) · reinversión estimada (3a)
    cc = decl.get("clasificacion_compras") or {}
    ccv, reg_cc = cc.get("valor"), cc.get("registro")
    tr = decl.get("transicion") or {}
    re_ = decl.get("reinversion_estimada")
    adq_w = [H["adq"][y] for y in ventana]
    adq_h = [H["adq"][y] for y in horiz]
    # V-F1j
    vj, vj_efecto = [], "INCOMPLETO"
    if ccv is None or ccv == "pendiente":
        vj.append("clasificación de las compras de sociedades " + ("pendiente (opción A de 4b, hasta M6)" if ccv == "pendiente" else "sin declarar"))
    elif ccv not in COMPRAS:
        vj.append(f"clasificacion_compras {ccv!r} no admitida")
        vj_efecto = "DATOS INVÁLIDOS"
    else:
        if not _registro_ok(reg_cc):
            G.add("F1-REGISTRO", True, "BLOQUEA", "INCOMPLETO", "clasificacion_compras sin registro (fecha, persona, motivo)", "(4b)")
        if ccv == "sin_compras" and any(a is None or a != 0 for a in adq_w + adq_h):
            vj.append("«sin_compras» con adquisiciones distintas de cero (o vacías) en la Historia (fila 13)")
            vj_efecto = "DATOS INVÁLIDOS"
        if ccv == "crecimiento_por_hipotesis" and not str(cc.get("fundamento") or "").strip():
            vj.append("hipótesis «las compras son crecimiento» sin su fundamento declarado")
        if ccv == "reposicion_con_importe":
            if per == "A3_estimado":
                if not (isinstance(re_, dict) and all(isinstance((re_.get("por_anio") or {}).get(str(y)), dict)
                                                       and Q((re_["por_anio"][str(y)]).get("R_compras")) is not None for y in ventana)):
                    vj.append("compras de reposición con A3: R_compras por año de la ventana sin declarar")
            elif Q(cc.get("proporcion_ventas")) is None and not isinstance(cc.get("importes"), dict):
                vj.append("compras de reposición fuera de D_X: término explícito sin importe por año ni proporción de las ventas")
            else:
                vj += _terminos_incompletos("compras de reposición", cc, horiz, con_proporcion=True)   # (revisión F1-IMPL, H10)
            if per != "A3_estimado" and cc.get("ancla_s2c_excluye_terminos") is not True:
                vj.append("compras de reposición cobradas como término explícito y también en el denominador del ancla de S2C (o sin declarar que el ancla las excluye)")
                vj_efecto = "MODELO NO APLICABLE"
            if per == "A3_estimado" and Q(cc.get("proporcion_ventas")) is not None:
                vj.append("compras de reposición en R (A3) y además como término explícito: se cobrarían dos veces")
                vj_efecto = "MODELO NO APLICABLE"
    G.add("V-F1j", bool(vj), "BLOQUEA", vj_efecto, "; ".join(vj) if vj else f"compras: {ccv}", "(4b)")
    # V-F1i
    vi, vi_efecto = [], "INCOMPLETO"
    trt = tr.get("tratamiento")
    conocida = tr.get("conocida")
    H_tr = tr.get("horizonte")
    if conocida is None:
        vi.append("sin declarar si hay una inversión de transición conocida (publicada o documentada)")
    elif conocida:
        if trt is None or trt == "pendiente":
            vi.append("transición conocida con su tratamiento " + ("pendiente" if trt == "pendiente" else "sin declarar") + " (sin importe ni horizonte la conclusión queda pendiente; nunca cero por defecto)")
        elif trt not in TRANSICION:
            vi.append(f"tratamiento de la transición {trt!r} no admitido")
            vi_efecto = "DATOS INVÁLIDOS"
        else:
            if not _registro_ok(tr.get("registro")):
                G.add("F1-REGISTRO", True, "BLOQUEA", "INCOMPLETO", "tratamiento de la transición sin registro (fecha, persona, motivo)", "(5b)")
            if not str(tr.get("finalidad_documentada") or "").strip():
                vi.append("la clasificación es por finalidad documentada: falta la finalidad y su fuente")
            if trt == "termino_explicito":
                imps = tr.get("importes")
                if not isinstance(imps, dict) or not isinstance(H_tr, int) or H_tr < 1:
                    vi.append("término explícito sin importe por año o sin horizonte")
                elif H_tr > 10:
                    vi.append(f"horizonte H = {H_tr} > 10: lo pendiente después del año 10 se descontaría fuera de Gordon (W1, E3), y no está implementado")
                    vi_efecto = "MODELO NO APLICABLE"
                elif any(Q(imps.get(str(t))) is None for t in range(1, H_tr + 1)):
                    vi.append("término explícito sin importe en algún año 1…H")
                vi += _terminos_incompletos("transición", tr, horiz, anios_futuros=0)   # (H10) importes históricos del ancla (X^v)
                if tr.get("naturaleza") == "permanente":
                    vi.append("una transición permanente no va como término temporal: en R (proporcional a las ventas) o declarada proporcional")
                    vi_efecto = "MODELO NO APLICABLE"
                if tr.get("ancla_s2c_excluye_terminos") is not True:
                    vi.append("transición cobrada como término y también en el denominador del ancla de S2C (o sin declarar que el ancla la excluye)")
                    vi_efecto = "MODELO NO APLICABLE"
                if isinstance(re_, dict) and any(Q((v or {}).get("transicion")) not in (None, 0) for v in (re_.get("por_anio") or {}).values()):
                    vi.append("transición en R y además como término explícito: dos veces")
                    vi_efecto = "MODELO NO APLICABLE"
            if trt == "en_R":
                if tr.get("naturaleza") != "permanente":
                    vi.append("en R solo cabe un sostenimiento permanente y proporcional a las ventas (una temporal en R se cobra de más después del plan)")
                    vi_efecto = "MODELO NO APLICABLE"
                if per != "A3_estimado":
                    vi.append("transición en R con un perímetro de D&A (A1/A2): la D&A no la contiene de forma comprobable; exige A3_estimado con su importe dentro de R")
    elif conocida is False and not _registro_ok(tr.get("registro")):   # (revisión F1-IMPL, H11) «no hay transición conocida» es una declaración
        G.add("F1-REGISTRO", True, "BLOQUEA", "INCOMPLETO", "«sin transición conocida» sin registro (fecha, persona, motivo)", "(5b)")
    if conocida is False and trt not in (None, "pendiente"):
        vi.append("se declara que no hay transición conocida y a la vez un tratamiento")
        vi_efecto = "DATOS INVÁLIDOS"
    G.add("V-F1i", bool(vi), "BLOQUEA", vi_efecto, "; ".join(vi) if vi else
          ("sin transición conocida" if conocida is False else f"transición: {trt}"), "(5b)")
    # V-F1d y V-F1c (A3)
    R_por = {}
    if per == "A3_estimado":
        vd = []
        if not isinstance(re_, dict):
            vd.append("A3_estimado sin estimación de la reinversión necesaria (R sigue en pendiente_de_datos: 3a, 3b (iv))")
        else:
            for k in ("fuente", "metodo", "rango", "responsable", "reposicion_clientes", "transicion"):
                if not str(re_.get(k) or "").strip():
                    vd.append(f"falta {k}")
            if re_.get("incluye_gasto_comercial") is not False:
                vd.append("sin declarar que R no incluye el gasto comercial corriente (está en el margen: 2 (ii); caso P2f)")
            pa = re_.get("por_anio") or {}
            for y in horiz:
                e = pa.get(str(y))
                if not isinstance(e, dict) or Q(e.get("R_propia")) is None:
                    if y in ventana:
                        vd.append(f"R_propia de {y} sin declarar")
                    continue
                R_por[y] = {k: Q(e.get(k)) or Fr(0) for k in ("R_propia", "R_compras", "transicion")}
        G.add("V-F1d", bool(vd), "BLOQUEA", "INCOMPLETO", "; ".join(vd) if vd else "estimación documentada (no es un dato publicado)", "(3a)")
        if not vd:
            rp = media(R_por[y]["R_propia"] + R_por[y]["transicion"] for y in ventana)
            rc = media(R_por[y]["R_compras"] for y in ventana)
            cp = media(H["capex"][y] for y in ventana)
            cm = media((H["adq"][y] or Fr(0)) for y in ventana)
            salta = rp > cp or rc > cm
            just = str((re_ or {}).get("justificacion_infrainversion") or "").strip()
            G.add("V-F1c", salta, "AVISO" if just else "BLOQUEA", "INCOMPLETO",
                  (f"R_propia (+ transición) media {float(rp):.3f} frente a capex propio {float(cp):.3f}; R_compras {float(rc):.3f} frente a compras "
                   f"{float(cm):.3f}" + (f" · justificación: {just}" if just else " · sin justificación: la entrada pasa a «hipótesis pendiente»"))
                  if salta else "cada parte de R por debajo de su caja (no se compara R total con el capex propio)", "(3a)")
        else:
            G.add("V-F1c", False, None, None, "no evaluable sin estimación (V-F1d)", "(3a)")
    else:
        G.add("V-F1d", False, None, None, "no aplica: el perímetro no es A3_estimado", "(3a)")
        G.add("V-F1c", False, None, None, "no aplica: el perímetro no es A3_estimado", "(3a)")

    # ---------------------------------------------------------------- V-F1h (margen) · V-F1g (palancas S2C) · V-F1k (ROIC, perímetro)
    vh = []
    if pmar is None:
        vh.append("perimetro_margen sin declarar")
    elif pmar not in MARGENES:
        vh.append(f"perimetro_margen {pmar!r} no admitido")
    elif pmar == "margen_despues_de_arrendamientos":
        vh.append("margen después de arrendamientos: no admisible por ahora (A1′ deja el interés de arrendamiento en f: N4)")
    elif pmar == "EBIT_NIIF16_PPA_decreciente" and per in ("A2_propio", "A3_estimado"):
        vh.append("PPA decreciente con una f que devuelve la PPA: no admisible por ahora (exige f variable o un término no monetario)")
    elif per in ("A1_sin_ROU", "A2_propio", "A0_total") and pmar != "EBIT_NIIF16_PPA_constante":
        vh.append(f"{per} exige EBIT_NIIF16_PPA_constante (2 (v): la PPA y la ROU como proporción constante de las ventas, la misma que devuelve f)")
    elif per == "A3_estimado" and pmar not in ("EBIT_NIIF16_PPA_constante", "EBIT_NIIF16_sin_PPA"):
        vh.append(f"A3_estimado con {pmar}: combinación no especificada")
    G.add("V-F1h", bool(vh), "BLOQUEA", "MODELO NO APLICABLE", "; ".join(vh) if vh else f"margen {pmar} coherente con {per}", "(2)")
    G.add("V-F1g", ppal is None or ppal != per, "BLOQUEA", "MODELO NO APLICABLE",
          ("perímetro de las palancas S2C sin declarar" if ppal is None else f"palancas S2C ancladas en {ppal!r} ≠ perímetro de la reinversión {per!r}")
          if (ppal is None or ppal != per) else f"perímetro declarado de las palancas S2C = perímetro de la reinversión ({per}): compara etiquetas de la "
          "declaración, no cifras" + ("; los valores, en «V-F1g (valores)» (P-FOSO, D3)" if per == "A2_propio" else ""), "(4a)")
    G.add("V-F1k", proi is None or proi != ppal, "BLOQUEA", "MODELO NO APLICABLE",
          ("perímetro del ROIC del terminal sin declarar" if proi is None else f"ROIC del terminal en {proi!r} ≠ palancas S2C {ppal!r}")
          if (proi is None or proi != ppal) else f"perímetro declarado del ROIC del terminal = el de las palancas S2C ({ppal}): compara etiquetas de la "
          "declaración, no cifras" + ("; los valores, en «V-F1k (valores)» (P-FOSO, D3)" if per == "A2_propio" else ""), "(4a)")

    # ---------------------------------------------------------------- cálculo por perímetro (diagnóstico A0, A1, A2 y el declarado)
    def DX_de(p, y):
        da = H["DA"][y]
        if da is None:
            return None
        if p == "A0_total":
            return da
        if p == "A1_sin_ROU":
            return da - rou8[y] if y in rou8 else None
        if p == "A2_propio":
            return da - rou8[y] - ppa[y] if (y in rou8 and y in ppa) else None
        if p == "A3_estimado":
            e = R_por.get(y)
            return (e["R_propia"] + e["R_compras"] + e["transicion"]) if e else None
        if p == "B_cota_capex":
            return H["capex"][y]
        if p == "LIBRO_DX":  # (V6.3.1 F1) D_X que calcula el propio libro (Historia fila 88): solo para la réplica
            return Q(L.get(f"Historia!{col[y]}88"))
        return None

    def X_terminos(p):
        """Términos explícitos de caja de E3 (fuera de D_X): transición «termino_explicito» y compras de reposición fuera de D_X."""
        imps_tr = {}
        if tr.get("conocida") and trt == "termino_explicito" and isinstance(tr.get("importes"), dict) and isinstance(H_tr, int) and H_tr <= 10:
            imps_tr = {t: Q(tr["importes"].get(str(t))) or Fr(0) for t in range(1, H_tr + 1)}
        a_prop = Q(cc.get("proporcion_ventas")) if (ccv == "reposicion_con_importe" and p != "A3_estimado") else None
        imps_cc = {int(k): Q(v) for k, v in (cc.get("importes") or {}).items()} if (ccv == "reposicion_con_importe" and p != "A3_estimado"
                                                                                     and isinstance(cc.get("importes"), dict)) else {}

        def X(t, Vt):
            return imps_tr.get(t, Fr(0)) + (a_prop * Vt if a_prop is not None else imps_cc.get(t, Fr(0)) or Fr(0))
        # (H10) con importes por año, el año 11 cobra su importe declarado (antes, 0 a perpetuidad); un importe ausente lo bloquea V-F1j
        X11 = (lambda V11: a_prop * V11) if a_prop is not None else (imps_cc.get(11) or Fr(0))
        return X, X11, bool(imps_tr or a_prop is not None or imps_cc)

    pal = {}
    for esc, c in (("MALO", "B"), ("NORMAL", "C"), ("BUENO", "D")):
        vals = {k: Q(L.get(ref)) for k, ref in (("g15", f"Palancas!{c}14"), ("m_obj", f"Palancas!{c}15"), ("s2c", f"Palancas!{c}16"),
                                                ("roic", f"Palancas!{c}18"), ("g_inf", f"Análisis!{c}68"))}
        if all(v is not None for v in vals.values()) and vals["s2c"] != 0 and vals["roic"] != 0:
            pal[esc] = vals
    res["palancas"] = {k: {kk: fl(vv) for kk, vv in v.items()} for k, v in pal.items()} or None

    def WC_de(y, con_ajuste=True):
        """Circulante que usa la reinversión: la fila 14 y, con US GAAP, sin la partida del arrendamiento operativo que esté dentro de ella (None si
        hay que retirarla y su importe no está declarado: vacío ≠ 0). con_ajuste=False: la fila 14 tal cual, que es lo que calcula el libro."""
        w = H["dwc"][y]
        if w is None or not us or not con_ajuste or not U["retira_de_14"]:
            return w
        return w - U["ajuste"][y] if y in U["ajuste"] else None

    def calcular(p, con_fuera=False, aplicar_n1=True, con_act=False, con_ajuste=True):
        if any(DX_de(p, y) is None or WC_de(y, con_ajuste) is None for y in ventana):
            return None
        tau, ebit = tasas_y_ebit(con_fuera, con_act) if aplicar_n1 else ({y: H["tau"][y] for y in anios}, {y: H["EBIT"][y] for y in anios})
        S_ = media(H["V"][y] for y in ventana)
        nopat = media(ebit[y] * (1 - tau[y]) for y in ventana)
        reinv = media(H["capex"][y] - DX_de(p, y) + WC_de(y, con_ajuste) for y in ventana)
        f = (nopat - reinv - C70) / S_
        if any(tau[y] is None for y in tau_anios):
            return None
        tau5 = media(tau[y] for y in tau_anios) if CONVENCION_TAU == "cinco_anios" else media(tau[y] for y in ventana)
        m0 = ebit[anios[-1]] / V0
        F0 = V0 * (m0 * (1 - tau5) - f)
        X, X11, hay_x = X_terminos(p)
        # ancla de S2C (E4): (V_L − V_G) ÷ Σ_H..L (capex − D_X + ΔWC + adquisiciones − X^v); X^v = términos explícitos de la ventana del ancla
        ancla = None
        # (revisión V6.3.1, V631-5 y E4) los cinco años H–L de TODO el denominador: capex, D_X, circulante y adquisiciones (vacío ≠ 0)
        if all(DX_de(p, y) is not None and H["capex"][y] is not None and H["dwc"][y] is not None and H["adq"][y] is not None
               and WC_de(y, con_ajuste) is not None for y in horiz) and H["V"][ant] is not None:
            xv = Fr(0)
            if hay_x and ccv == "reposicion_con_importe" and p != "A3_estimado":
                if Q(cc.get("proporcion_ventas")) is not None:
                    xv += sum(Q(cc.get("proporcion_ventas")) * H["V"][y] for y in horiz)
                else:   # (H10) con importes por año, X^v son los importes históricos declarados de H–L (obligatorios: V-F1j)
                    xv += sum((Q(((cc.get("importes_historicos") or {}).get(str(y)))) or Fr(0)) for y in horiz)
            xv += sum((Q(((tr.get("importes_historicos") or {}).get(str(y)))) or Fr(0)) for y in horiz) if trt == "termino_explicito" else Fr(0)
            den = sum(H["capex"][y] - DX_de(p, y) + (WC_de(y, con_ajuste) or Fr(0)) + (H["adq"][y] or Fr(0)) for y in horiz) - xv
            ancla = (H["V"][anios[-1]] - H["V"][ant]) / den if den > 0 else None
        esc = {}
        for nombre, pv in pal.items():
            mo = motor(V0, m0, tau5, f, X=X, X11=X11, **pv)
            esc[nombre] = {"anios_1_10": [fl(x) for x in mo["flujos"]], "anio_11": fl(mo["flujo_11"]), "_mo": mo}
        # K3: puente FCF base → flujo sin crecimiento, partida a partida
        Eb = media(ebit[y] for y in ventana)
        da_own = {y: H["DA"][y] - rou8.get(y, Fr(0)) - ppa.get(y, Fr(0)) for y in ventana}
        lineas = [("FCF base que calibra f (Historia C70, entrada registrada)", C70, "caja"),
                  ("+ nivel del EBIT del año base frente a la media de la ventana, al τ de proyección", (ebit[anios[-1]] - Eb) * (1 - tau5), "explicada"),
                  ("+ τ de proyección frente al τ de cada año de la ventana", Eb * (1 - tau5) - nopat, "explicada"),
                  ("− f aplicada a las ventas del año base en lugar de las medias", -f * (V0 - S_), "explicada")]
        if p in ("A3_estimado", "B_cota_capex"):
            lineas.append(("+ reinversión de la ventana que la proyección sin crecimiento no repite (capex − D_X + circulante; D_X = "
                           + ("R estimada)" if p == "A3_estimado" else "capex propio: cota)"), reinv, "explicada"))
        else:
            k3_rou = media(rou8.get(y, Fr(0)) for y in ventana) if (p == "A0_total" and all(y in rou8 for y in ventana)) else Fr(0)
            k3_ppa = media(ppa.get(y, Fr(0)) for y in ventana) if (p in ("A0_total", "A1_sin_ROU") and all(y in ppa for y in ventana)) else Fr(0)
            conocido = all(y in rou8 and y in ppa for y in ventana)
            if conocido:
                lineas.append(("+ inversión neta propia y circulante de la ventana (capex − D&A propia + circulante)",
                               media(H["capex"][y] - da_own[y] + H["dwc"][y] for y in ventana), "explicada"))
                lineas.append(("− amortización ROU que D_X devuelve como reposición, con los pagos de arrendamiento ya dentro del FCF base",
                               -k3_rou, "doble_computo" if (k3_rou > 0 and (c49_pos or (us and us_f["pagos_op_pos"]))) else ("fuera_de_dominio" if k3_rou > 0 else "explicada")))
                lineas.append(("− amortización PPA que D_X devuelve como reposición (no es caja: política (2)(i))",
                               -k3_ppa, "reposicion_no_monetaria" if k3_ppa > 0 else "explicada"))
                if us and con_ajuste and U["retira_de_14"]:
                    lineas.append(("− partida del arrendamiento operativo dentro de la fila 14, que se retira del circulante (US GAAP: su pago ya está en el FCF base)",
                                   -media(U["ajuste"][y] for y in ventana), "explicada"))
            else:
                lineas.append(("+ reinversión de la ventana que la proyección sin crecimiento no repite (capex − D_X + circulante; D&A ROU o PPA sin declarar)",
                               reinv, "sin_desglose"))
        suma = sum((x for _, x, _ in lineas), Fr(0))
        k3 = {"lineas": [{"partida": a, "mm": fl(x, 6), "clase": c} for a, x, c in lineas], "flujo_sin_crecimiento": fl(F0, 9),
              "suma_de_partidas": fl(suma, 9), "identidad_cuadra": abs(suma - F0) <= TOL_LIBRO * max(1, abs(F0)),
              "doble_computo_mm_en_la_ventana": fl(-sum((x for _, x, c in lineas if c in ("doble_computo", "reposicion_no_monetaria")), Fr(0)), 6),
              "doble_computo_mm_a_la_escala_del_año_base": fl(-sum((x for _, x, c in lineas if c in ("doble_computo", "reposicion_no_monetaria")), Fr(0)) * V0 / S_, 6),
              "doble_computo_por_clase_a_la_escala_del_año_base": {c: fl(-sum((x for _, x, cc in lineas if cc == c), Fr(0)) * V0 / S_, 6)
                                                                  for c in ("doble_computo", "reposicion_no_monetaria")},
              "partidas_sin_explicar": [a for a, _, c in lineas if c in ("doble_computo", "fuera_de_dominio", "reposicion_no_monetaria", "sin_desglose")]}
        return {"f": f, "F0": F0, "tau5": tau5, "m0": m0, "nopat": nopat, "reinv": reinv, "S": S_, "ancla": ancla, "esc": esc, "k3": k3,
                "tau_ventana": {y: tau[y] for y in ventana}}

    diag = {}
    for p in ("A0_total", "A1_sin_ROU", "A2_propio", "B_cota_capex"):
        r = calcular(p, aplicar_n1=False)
        if r:
            diag[p] = r
    # réplica del libro (F1-REPLICA): A0 sin normalizar reproduce Historia C58, C53 y los flujos del Motor
    rep = []
    r0 = diag.get("A0_total")
    if us and U["retira_de_14"]:
        r0 = calcular("A0_total", aplicar_n1=False, con_ajuste=False)   # (F1 · US GAAP) la réplica es la del libro, que no retira nada del circulante
    r0, p_rep = _replica_v631(L, r0, lambda p, **k: calcular(p, **dict(k, con_ajuste=False)), anios, col, rep)
    if r0 is None and C58 is None and p_rep != "A0":
        res["replica_del_libro"] = {"perimetro_replicado": p_rep, "conforme": not rep, "nota": "f vacía en el libro y en la réplica (D_X incompleta en la ventana)"}
    elif r0 is None:
        rep.append(f"{p_rep} no calculable con la Historia del libro")
    else:
        if C58 is None or abs(r0["f"] - C58) > Fr(1, 10 ** 12):
            rep.append(f"f {p_rep} {float(r0['f'])} ≠ Historia C58 {None if C58 is None else float(C58)}")
        if C52 is not None and abs(r0["tau5"] - C52) > Fr(1, 10 ** 12):
            rep.append(f"τ de 5 años {float(r0['tau5'])} ≠ Historia C52 {float(C52)}")
        if m0_libro is not None and abs(r0["m0"] - m0_libro) > Fr(1, 10 ** 12):
            rep.append(f"m0 {float(r0['m0'])} ≠ Historia C48 {float(m0_libro)}")
        if C53 is not None and r0["ancla"] is not None and abs(r0["ancla"] - C53) > Fr(1, 10 ** 9):
            rep.append(f"ancla {p_rep} {float(r0['ancla'])} ≠ Historia C53 {float(C53)}")
        n_flujos = 0
        for nombre, fila in (("MALO", 6), ("NORMAL", 7), ("BUENO", 8)):
            if nombre not in r0["esc"]:
                continue
            mo = r0["esc"][nombre]["_mo"]
            for t, c in enumerate(["AU", "AV", "AW", "AX", "AY", "AZ", "BA", "BB", "BC", "BD"]):
                lv = Q(L.get(f"Motor!{c}{fila}"))
                if lv is not None:
                    n_flujos += 1
                    if abs(mo["flujos"][t] - lv) > TOL_LIBRO:
                        rep.append(f"Motor!{c}{fila} {float(lv)} ≠ réplica {float(mo['flujos'][t])}")
            lv = Q(L.get(f"Motor!BF{fila}"))
            if lv is not None:
                n_flujos += 1
                if abs(mo["flujo_11"] - lv) > TOL_LIBRO:
                    rep.append(f"Motor!BF{fila} {float(lv)} ≠ réplica {float(mo['flujo_11'])}")
        res["replica_del_libro"] = {"f": fl(r0["f"], 15), "C58": fl(C58, 15), "ancla": fl(r0["ancla"]), "C53": fl(C53),
                                    "flujos_contrastados": n_flujos, "conforme": not rep, "perimetro_replicado": p_rep}
    G.add("F1-REPLICA", bool(rep), "BLOQUEA", "DATOS INVÁLIDOS", "; ".join(rep) if rep else
          "la réplica A0 reproduce el libro (f, τ, m0, ancla y flujos): la capa F1 y el libro son el mismo motor", "T1/T7", clase="implementacion")

    # perímetro declarado: con N1 (variante «solo ventana» y, si hay ajustes fuera de la ventana, la otra)
    decl_r = calcular(per) if per else None
    variantes = {}
    if per and aj_ok and (fuera or act_ok):
        variantes["N1 solo en la ventana, sin la actualización financiera"] = decl_r
        if fuera:
            variantes["N1 también en los ejercicios del τ fuera de la ventana"] = calcular(per, con_fuera=True)
        if act_ok:
            variantes["N1 con la actualización financiera fuera del BAI que da el tipo"] = calcular(per, con_act=True)
        if fuera and act_ok:
            variantes["N1 en los ejercicios del τ y con la actualización financiera"] = calcular(per, con_fuera=True, con_act=True)
        sin_n1 = calcular(per, aplicar_n1=False)
        if sin_n1:
            res["efecto_N1_frente_a_sin_normalizar"] = {k: (fl(v["F0"] - sin_n1["F0"], 6) if v else None) for k, v in variantes.items()}
    if per and decl_r is None:
        G.add("F1-PERIMETRO", True, "BLOQUEA", "INCOMPLETO", f"el perímetro {per} no es calculable: faltan series (D&A ROU, PPA o R) en la ventana"
              + (" o, con US GAAP, la ubicación de la amortización del derecho de uso operativo o el importe que se retira del circulante" if us else ""), "(1a)")
    # K3 (revisión F1-IMPL, H5): el puente es una identidad y se conserva como presentación (E6); las tres comprobaciones que siguen las
    # pueden hacer fallar los datos
    k3 = {"identidad": None, "K3a_caja_base_dos_vias": None, "K3b_alquiler_contado": None, "K3c_reposicion_frente_a_su_caja": None}
    if decl_r and not decl_r["k3"]["identidad_cuadra"]:
        G.add("F1-K3", True, "BLOQUEA", "DATOS INVÁLIDOS", f"el puente no cuadra: suma {decl_r['k3']['suma_de_partidas']} ≠ flujo {decl_r['k3']['flujo_sin_crecimiento']}",
              "K3", clase="implementacion")
    k3["identidad"] = decl_r["k3"]["identidad_cuadra"] if decl_r else None
    # K3a · caja base por dos vías: Historia C70 frente a la media de la fila 35 (CFO − capex − intereses en financiación − principal − SBC).
    # La diferencia se descompone en sus componentes (C46 − CFO, C47 − capex, C48 − fila 16, C49 − fila 17, C50 − fila 18 y C70 − C52); cada
    # componente distinto de cero (más que el redondeo a 3 decimales de E7) tiene que estar explicado por una partida declarada con su fuente.
    TOL_E7 = Fr(5, 10 ** 4)
    f35 = [Q(L.get(f"Historia!{col[y]}35")) for y in ventana]
    filas = {k: [Q(L.get(f"Historia!{col[y]}{fi}")) for y in ventana] for k, fi in (("cfo", 11), ("capex", 12), ("int16", 16), ("princ", 17), ("sbc", 18))}
    an = {c: Q(L.get(f"Análisis!{c}")) for c in ("C46", "C47", "C48", "C49", "C50", "C52")}
    resta_sbc = str(L.get("Análisis!C51") or "").strip() == "Sí"
    k3a_mot = []
    if any(x is None for x in f35):
        k3a_mot.append("fila 35 de la Historia vacía en la ventana: la caja base no se puede contrastar por la segunda vía")
    else:
        dif = C70 - media(f35)
        comp = {}
        if all(v is not None for v in an.values()) and all(x is not None for v in filas.values() for x in v):
            m = {k: media(v) for k, v in filas.items()}
            comp = {"C46": an["C46"] - m["cfo"], "C47": -(an["C47"] - m["capex"]), "C48": -(an["C48"] - m["int16"]), "C49": -(an["C49"] - m["princ"]),
                    "C50": -((an["C50"] if resta_sbc else Fr(0)) - m["sbc"]), "C70": C70 - an["C52"]}
        decl_c = decl.get("conciliacion_fcf_base") or []
        expl = {}
        for e in decl_c if isinstance(decl_c, list) else []:
            if not isinstance(e, dict) or Q(e.get("importe")) is None or not str(e.get("partida") or "").strip() or not e.get("fuente") or e.get("componente") not in comp:
                k3a_mot.append(f"partida de conciliación incompleta o con un componente no reconocido: {e!r}"[:200])
                continue
            expl[e["componente"]] = expl.get(e["componente"], Fr(0)) + Q(e["importe"])
        for c, d in comp.items():
            if abs(d - expl.get(c, Fr(0))) > TOL_E7:
                k3a_mot.append(f"componente {c}: {float(d):+.6f} en la caja base frente a la fila 35, explicado {float(expl.get(c, Fr(0))):+.6f}")
        if not comp:
            k3a_mot.append("faltan Análisis C46–C52 o las filas 11, 12, 16, 17 o 18 de la ventana: no se puede descomponer la diferencia")
        elif abs(dif - sum(comp.values(), Fr(0))) > 3 * TOL_E7:
            k3a_mot.append(f"la diferencia total {float(dif):+.6f} no es la suma de sus componentes {float(sum(comp.values(), Fr(0))):+.6f}: "
                           "la fila 35 no es CFO − capex − intereses − principal − SBC de las filas de la Historia")
        if abs(dif - sum(expl.values(), Fr(0))) > 3 * TOL_E7:
            k3a_mot.append(f"diferencia total sin explicar: {float(dif - sum(expl.values(), Fr(0))):+.6f}")
        res["K3a_caja_base"] = {"C70": fl(C70, 6), "media_fila_35": fl(media(f35), 6), "diferencia": fl(dif, 6),
                                "componentes": {c: fl(d, 6) for c, d in comp.items()}, "explicado": {c: fl(v, 6) for c, v in expl.items()},
                                "residuo": fl(dif - sum(expl.values(), Fr(0)), 6)}
    k3["K3a_caja_base_dos_vias"] = not k3a_mot
    G.add("F1-K3a", bool(k3a_mot), "BLOQUEA", "DATOS INVÁLIDOS",
          ("caja base por dos vías: " + "; ".join(k3a_mot)) if k3a_mot else "caja base por dos vías: cada diferencia entre C70 y la fila 35 está explicada por una partida declarada", "K3")
    # K3b · cuántas veces cuenta la proyección el coste de arrendamiento: amortización ROU en el margen + pagos en el FCF base − ROU que f devuelve
    if per and us:
        _k3b_us(G, k3, U, us_f, per, rou_pos, c49_pos)
    elif per:
        devuelve = per in ("A1_sin_ROU", "A2_propio", "A3_estimado")
        veces = (1 if rou_pos else 0) + (1 if c49_pos else 0) - (1 if (rou_pos and devuelve) else 0)
        esperado = 1 if (rou_pos or c49_pos) else 0
        k3["K3b_alquiler_contado"] = {0: "ninguna vez", 1: "una vez", 2: "dos veces"}.get(veces, str(veces)) + ("" if (rou_pos or c49_pos) else " (sin arrendamientos)")
        G.add("F1-K3b", veces != esperado, "BLOQUEA", "MODELO NO APLICABLE",
              f"alquiler contado {k3['K3b_alquiler_contado']} en la proyección con el perímetro {per} (debe contarse una vez)" if veces != esperado
              else f"alquiler contado {k3['K3b_alquiler_contado']}", "K3")
    # K3c · reposición frente a su caja: con ventas que no bajan en la ventana, una reinversión media negativa (capex − D_X + circulante) dice
    # que D_X devuelve más amortización de la que el capex pudo reponer; sin justificación declarada, bloquea
    if decl_r:
        neg = decl_r["reinv"] < 0 and H["V"][ventana[-1]] >= H["V"][ventana[0]]
        just = str(decl.get("justificacion_reinversion_negativa") or "").strip()
        k3["K3c_reposicion_frente_a_su_caja"] = not neg or bool(just)
        G.add("F1-K3c", neg, "AVISO" if just else "BLOQUEA", "INCOMPLETO",
              (f"reinversión media de la ventana {float(decl_r['reinv']):.3f} < 0 con ventas que no bajan: D_X devuelve más amortización de la que el capex repuso"
               + (f" · justificación: {just}" if just else " · sin justificación")) if neg else
              f"reinversión media {float(decl_r['reinv']):.3f} ≥ 0 (o ventas a la baja)", "K3")
    k3["conforme"] = None if k3["identidad"] is None and k3["K3a_caja_base_dos_vias"] else all(v not in (False,) for v in (k3["identidad"], k3["K3a_caja_base_dos_vias"], k3["K3c_reposicion_frente_a_su_caja"])) \
        and k3["K3b_alquiler_contado"] in (None, "una vez", "ninguna vez (sin arrendamientos)")
    if us and k3["conforme"] is True and k3.get("K3b_contrastado") is False:
        # (ronda 2, R1-15) K3b repite la clasificación declarada: sin contraste con las líneas del expediente no se presenta como conforme
        k3["conforme"], k3["conforme_nota"] = None, "K3b no es una comprobación independiente: " + k3["K3b_fundamento"]
    res["K3"] = k3
    # F1-LIBRO: el libro V6.3 calcula A0 sin normalizar
    hay_terminos = bool(per) and X_terminos(per)[2]
    # (F1 · US GAAP) ningún libro retira del circulante la partida del arrendamiento operativo: si el ajuste declarado no es cero, el libro no calcula lo declarado
    hay_ajuste = bool(us and U["retira_de_14"] and any(U["ajuste"].get(y) for y in set(ventana) | set(horiz)))
    txt_ajuste = (", partida del arrendamiento operativo retirada del circulante (US GAAP; LÍMITE DECLARADO: ningún libro la retira; la salida es corregir la "
                  "fila 14 con una corrección registrada de las entradas en un expediente nuevo, o una plantilla con ese ajuste)") if hay_ajuste else ""
    dif_motor = []
    if decl_r:
        for nombre, fila in (("MALO", 6), ("NORMAL", 7), ("BUENO", 8)):
            if nombre not in decl_r["esc"]:
                continue
            mo = decl_r["esc"][nombre]["_mo"]
            for t, c in enumerate(["AU", "AV", "AW", "AX", "AY", "AZ", "BA", "BB", "BC", "BD", "BF"]):
                lv = Q(L.get(f"Motor!{c}{fila}"))
                v = mo["flujos"][t] if t < 10 else mo["flujo_11"]
                if lv is not None and abs(v - lv) > TOL_LIBRO * max(1, abs(lv)):
                    dif_motor.append(f"Motor!{c}{fila}")
    v631 = _libro_v631(L, per, rou8, ppa, anios, col, DX_de, decl_r, dif_motor)
    if v631 is not None:  # (V6.3.1 F1) el libro calcula el perímetro F1: la capa es el oráculo
        res["libro_v631_f1"] = v631
        if per and (v631["motivos"] or aj_ok or hay_terminos or hay_ajuste):
            G.add("F1-LIBRO", True, "BLOQUEA", "MODELO NO APLICABLE",
                  f"el libro V6.3.1 F1 no calcula lo declarado ({per}" + (", N1" if aj_ok else "") + (", términos explícitos" if hay_terminos else "") + txt_ajuste
                  + "; N1 y los términos explícitos no están en el libro): " + "; ".join(v631["motivos"])[:900]
                  + ": la conclusión del motor A no se toma del libro; los flujos F1 son un diagnóstico", "(1a) · implantación")
        else:
            G.add("F1-LIBRO", False, None, None, f"el libro V6.3.1 F1 calcula el perímetro declarado ({per}): f, ancla, D_X, series y "
                  f"{v631['flujos_contrastados']} flujos del Motor coinciden con la capa", "(1a) · implantación")
    elif per and (per != "A0_total" or aj_ok or hay_terminos or dif_motor or hay_ajuste):
        G.add("F1-LIBRO", True, "BLOQUEA", "MODELO NO APLICABLE",
              f"LÍMITE DECLARADO · el libro V6.3 calcula el perímetro A0 sin normalizar y sin términos explícitos; con {per}" + (" y N1" if aj_ok else "")
              + (" y términos explícitos de caja (transición o compras)" if hay_terminos else "") + txt_ajuste
              + (f"; flujos del perímetro declarado distintos de los del Motor en {len(dif_motor)} celdas" if dif_motor else "")
              + ": su valor no corresponde a la declaración; la conclusión del motor A no se toma del libro; los flujos F1 son un diagnóstico", "(1a) · implantación")
    else:
        G.add("F1-LIBRO", False, None, None, "el perímetro declarado es el que calcula el libro", "(1a) · implantación")

    # V-F1k numérico (bloque 10 del libro, con el umbral vigente C179) e igualdad exacta (INFORMA)
    c179 = Q(L.get("Diagnóstico V6!C179"))
    bloque10 = {}
    for nombre, c in (("MALO", "B"), ("NORMAL", "C"), ("BUENO", "D")):
        s178 = Q(L.get(f"Diagnóstico V6!{c}178"))
        if s178 is None or c179 is None or nombre not in pal:
            continue
        pv = pal[nombre]
        tau_ = (decl_r or r0 or {}).get("tau5") or C52
        exacta = (1 + pv["g_inf"]) * pv["m_obj"] * (1 - tau_) * pv["s2c"] - pv["roic"]
        bloque10[nombre] = {"fila_176": fl(Q(L.get(f"Diagnóstico V6!{c}176")), 9), "fila_177": fl(Q(L.get(f"Diagnóstico V6!{c}177")), 9),
                            "fila_178_salto": fl(s178, 9), "C179": fl(c179, 9), "supera_umbral": abs(s178) > c179,
                            "salto_igualdad_exacta": fl(exacta, 9)}
    if bloque10:
        sup = [k for k, v in bloque10.items() if v["supera_umbral"]]
        G.add("V-F1k (salto del terminal)", bool(sup), "AVISO", "AVISO",
              (f"|salto| > C179 en {sup}: G8 (vigente) exige justificación en la tesis u Observación de B18:D18" if sup
               else "|salto| ≤ C179 en los tres escenarios: informa (no acredita coherencia)"), "(4a)")
    res["bloque_10_del_libro"] = bloque10 or None
    import perimetro_f1 as PF   # (P-FOSO, D3) V-F1g/V-F1k por valores, donde las palancas existen (paso 12; en el paso 7, «aún sin palancas»)
    res["perimetro_f1_valores"] = PF.guardas_valores(G, L, decl, per, pal, decl_r, diag, carpeta)

    # V-F1f (INFORMA): efectos de escala de la PPA y de la ROU, agotamiento de la PPA
    info_f = {}
    yL = anios[-1]
    S_w = media(H["V"][y] for y in ventana)
    if all(y in ppa for y in ventana) and yL in ppa:
        info_f["PPA: media ÷ ventas medias (lo que devuelve f en A2)"] = fl(media(ppa[y] for y in ventana) / S_w, 6)
        info_f["PPA: año base ÷ ventas del año base (lo que lleva m0)"] = fl(ppa[yL] / V0, 6)
        info_f["efecto de escala de la PPA en el flujo sin crecimiento de A2 (mm)"] = fl(media(ppa[y] for y in ventana) / S_w * V0 - ppa[yL], 3)
    if all(y in rou8 for y in ventana) and yL in rou8:
        info_f["ROU: media ÷ ventas medias (lo que devuelve f en A1 y A2)"] = fl(media(rou8[y] for y in ventana) / S_w, 6)
        info_f["ROU: año base ÷ ventas del año base (lo que lleva m0)"] = fl(rou8[yL] / V0, 6)
        info_f["efecto de escala de la ROU en el flujo sin crecimiento de A1 y A2 (mm)"] = fl(media(rou8[y] for y in ventana) / S_w * V0 - rou8[yL], 3)
    vnc = Q(((decl.get("series") or {}).get("vnc_intangibles_adquiridos") or {}).get("valor")) if isinstance((decl.get("series") or {}).get("vnc_intangibles_adquiridos"), dict) else None
    if vnc is not None and yL in ppa and ppa[yL] > 0:
        info_f["años de agotamiento de la PPA al ritmo del año base (valor neto ÷ PPA)"] = fl(vnc / ppa[yL], 2)
    sum_rou8_w = sum((rou8[y] for y in ventana if y in rou8), Fr(0))   # con NIIF, igual que sum_rou_w
    G.add("V-F1f", per in ("A1_sin_ROU", "A2_propio") and (sum_rou8_w > 0 or (per == "A2_propio" and sum_ppa_w > 0)), "INFORMA", "INFORMA",
          json.dumps(info_f, ensure_ascii=False) if info_f else "sin series para los efectos de escala", "(2)")

    # (1b) sensibilidad al peso de 2025 de los pagos y de la amortización ROU (la media de la ventana es la convención declarada)
    sens = None
    if all(y in pagos for y in ventana) and yL in pagos:
        w_m, w_L = media(pagos[y] for y in ventana) / S_w, pagos[yL] / V0
        sp = -V0 * (w_L - w_m)
        sr = (rou[yL] - media(rou[y] for y in ventana) / S_w * V0) if (all(y in rou for y in ventana) and yL in rou) else None
        sens = {"convencion": "media de la ventana (referencia de ensayo y convención declarada; no es una estimación del peso futuro)",
                "pagos_media_%_ventas": fl(100 * w_m, 4), "pagos_año_base_%_ventas": fl(100 * w_L, 4),
                "sensibilidad_pagos_mm (A0, A1 y A2)": fl(sp, 3),
                "sensibilidad_amortizacion_ROU_que_devuelve_f_mm (A1 y A2)": fl(sr, 3) if sr is not None else None,
                "total_A1_A2_mm": fl(sp + sr, 3) if sr is not None else None}
    res["sensibilidad_peso_arrendamiento_1b"] = sens

    # (3a) materialidad de R: D&A propia y capex propio de la ventana (no son R; R sigue pendiente)
    if all(y in rou8 and y in ppa for y in ventana):
        res["materialidad_R_3a"] = {"D&A propia media (referencia inferior; no es cota)": fl(media(H["DA"][y] - rou8[y] - ppa[y] for y in ventana), 3),
                                    "capex propio medio (cota superior de R_propia + transición)": fl(media(H["capex"][y] for y in ventana), 3),
                                    "nota": "solo mide la materialidad de R_propia más la transición; no fija R (3a)"}
    # materialidad de V-F1a (para un umbral futuro; sin umbral adoptado)
    if r0 and all(y in rou8 for y in ventana):
        rou_m = media(rou8[y] for y in ventana)
        res["materialidad_V_F1a"] = {"D&A ROU media de la ventana (mm)": fl(rou_m, 3), "÷ ventas medias": fl(rou_m / S_w, 6),
                                     "÷ FCF base": fl(rou_m / C70, 6), "exceso en el flujo sin crecimiento del año base (mm)": fl(rou_m / S_w * V0, 3),
                                     "umbral": "ninguno adoptado: V-F1a bloquea con cualquier importe"}

    def salida(r):
        if r is None:
            return None
        return {"f": fl(r["f"], 15), "flujo_sin_crecimiento": fl(r["F0"], 9), "tau_proyeccion": fl(r["tau5"], 9), "m0": fl(r["m0"], 12),
                "nopat_medio": fl(r["nopat"], 9), "reinversion_media": fl(r["reinv"], 9), "ancla_s2c_E4": fl(r["ancla"]),
                "tau_ventana": {str(k): fl(v, 6) for k, v in r["tau_ventana"].items()},
                "escenarios": {k: {"anios_1_10": v["anios_1_10"], "anio_11": v["anio_11"]} for k, v in r["esc"].items()}, "K3": r["k3"]}
    res["perimetro_declarado"] = per
    res["calculo_perimetro_declarado"] = salida(decl_r)
    if variantes:
        res["variantes_parametros_sin_valor"] = {k: salida(v) for k, v in variantes.items()}
    res["diagnostico_por_perimetro"] = {k: salida(v) for k, v in diag.items()}
    if "A0_total" in diag:
        res["diferencias_frente_a_A0_flujo_sin_crecimiento"] = {k: fl(v["F0"] - diag["A0_total"]["F0"], 6) for k, v in diag.items()}
    if us:
        _informes_us(G, res, L, U, us_f, anios, ventana, col, V0, S_w, decl_r, pal, motor_)
        res["fase1_partes_sha256"] = (U.get("partes") or {}).get("sha256")   # las líneas de la fase 1 con que se contrastaron las ubicaciones (None: sin fase1_partes)
    _guarda_fuentes_series(G, decl, carpeta, anios, res, us=U)   # (revisión F1-IMPL, H12; V631-2) al final: BLOQUEA si nada más bloquea
    return _cerrar(res, G, "A")


def _cerrar(res, G, motor):
    """Estado propuesto y rótulo a partir de las guardas. Una conclusión que se apoya en una hipótesis declarada (D-US1, D-WM) o en una ubicación
    declarada que no se ha podido contrastar con una línea se rotula CONDICIONADA; con D-US2 bis el rótulo dice que el valor es el de la hoja."""
    res["guardas"] = G.lista
    bl = G.bloquean()
    res["bloquea"] = bool(bl)
    res["utilizable_para_conclusion"] = not bl
    clases = {g["clase"] for g in bl}
    res["estado_propuesto"] = (None if not bl else "no_entregable · fallo_de_implementacion" if "implementacion" in clases
                               else "no_entregable · limite_del_modelo" if "norma" in clases   # «Otro»: ningún dato lo arregla
                               else "pendiente_de_datos" if "datos" in clases else "no_entregable · limite_del_modelo")
    cond = res.get("condicionada")
    bis = ((res.get("us_gaap") or {}).get("D_US2_bis") or {}).get("texto")
    res["rotulo"] = (f"DIAGNÓSTICO F1 · el resultado del motor {motor} no se usa para una conclusión: " + ", ".join(sorted({g["id"] for g in bl}))) if bl else \
        ((f"motor {motor} utilizable para una conclusión según F1" if not cond else
          f"motor {motor} utilizable para una conclusión CONDICIONADA según F1 · {cond['texto']}" + (f" · {cond['cota']['resumen']['texto']}" if (cond.get("cota") or {}).get("resumen") else ""))
         + (f" · {bis}" if bis else "") + " (condición necesaria, no suficiente; no apto para dinero real)")
    return res


# ----------------------------------------------------------------------------------------------------------- US GAAP (ASC 842)
def _unidad_de_redondeo(x, maximo=6):
    """Unidad del último decimal con que está escrito un valor del libro (5,7 → 0,1; 6 → 1; 5,67 → 0,01)."""
    for n in range(maximo + 1):
        if (x * 10 ** n).denominator == 1:
            return Fr(1, 10 ** n)
    return Fr(1, 10 ** maximo)


def _conciliacion_explicada(decl):
    """{componente: importe explicado} de las partidas completas de «conciliacion_fcf_base» (las mismas que admite K3a: importe, partida y fuente)."""
    out = {}
    lst = decl.get("conciliacion_fcf_base")
    for e in lst if isinstance(lst, list) else []:
        if (isinstance(e, dict) and Q(e.get("importe")) is not None and str(e.get("partida") or "").strip() and e.get("fuente")
                and isinstance(e.get("componente"), str)):
            out[e["componente"]] = out.get(e["componente"], Fr(0)) + Q(e["importe"])
    return out


def _guardas_us(G, L, U, decl, anios, ventana, horiz, per, C49, col):
    """(F1 · US GAAP) Guardas de los arrendamientos con ASC 842, con los operativos y los financieros por separado (F1_USGAAP.md §3 y §5).
    El alquiler operativo ya cuenta una vez en el FCF base (coste entero en el EBIT, pago en el CFO) y la reinversión que calibra f no lleva
    ninguna partida suya (D-US2: se cuentan los pagos). Se contaría de más si su amortización quedara dentro de D_X o sola dentro del
    circulante, o si C49 llevara sus pagos; se omitiría si la variación de su pasivo quedara sola dentro del circulante. Con los dos tramos
    dentro del circulante (D-US2 bis) no se retira nada: se publica el valor de la hoja. Devuelve las marcas que usan K3b, el puente K3 y los
    informes."""
    S = U["S"]
    P, Lc, finp = S["pagos_arr_operativo"], S["coste_arr_operativo"], S["pagos_arr_financiero_principal"]
    dec = "US GAAP · ASC 842"
    faltas, incoh = list(U["faltas"]), list(U["incoherencias"])
    op, fin, en14 = U["op"], U["fin"], U["tramos_en_fila_14"]
    # F1-US-MEZCLA: partidas propias de NIIF en un libro US GAAP
    c48 = Q(L.get("Análisis!C48"))
    f16 = [y for y in ventana if (Q(L.get(f"Historia!{col[y]}16")) or 0) > 0]
    mez = ([f"Análisis C48 = {float(c48)}"] if (c48 is not None and c48 > TOL_E7) else []) + ([f"Historia fila 16 positiva en {f16}"] if f16 else [])
    G.add("F1-US-MEZCLA", bool(mez), "BLOQUEA", "DATOS INVÁLIDOS",
          ("mezcla de normas: intereses pagados «en financiación» (" + "; ".join(mez) + ") con US GAAP, donde los intereses pagados van siempre en el flujo "
           "de explotación (ASC 230): el FCF base los restaría dos veces") if mez else "sin partidas propias de NIIF en un libro US GAAP (C48 y fila 16 a cero)", dec)
    # series exigidas (vacío ≠ 0)
    pagos_op_pos = sum((P[y] for y in ventana if y in P), Fr(0)) > 0
    if op is True:
        p_w, l_w = [y for y in ventana if y not in P], [y for y in ventana if y not in Lc]
        if p_w:
            faltas.append(f"series.pagos_arr_operativo sin declarar en {p_w} (caja pagada por arrendamientos operativos dentro del flujo de explotación)")
        elif not pagos_op_pos:
            incoh.append("operativos.existen = true y series.pagos_arr_operativo suma cero en la ventana")
        if l_w:
            faltas.append(f"series.coste_arr_operativo sin declarar en {l_w} (coste lineal de los contratos capitalizados, el mismo perímetro que los pagos; D-US2: su "
                          "diferencia con los pagos queda a la vista; si la empresa no lo separa del corto plazo y del variable, se declara igualmente y se marca "
                          "«coste_comparable_con_los_pagos»: false)")
        if U["ub_am"] == "fila_8":
            a_w = [y for y in ventana if y not in U["a8"]]
            if a_w:
                faltas.append(f"series.da_rou_operativo sin declarar en {a_w} (amortización del derecho de uso operativo dentro de la fila 8)")
        if U["retira_de_14"]:
            # la ventana de f y los cinco años H–L del ancla de S2C usan el circulante: el importe que se retira hace falta en todos (0 explícito si no lo hubo)
            j_w = [y for y in sorted(set(ventana) | set(horiz)) if y not in U["ajuste"]]
            if j_w:
                faltas.append(f"series.circulante_arr_operativo sin declarar en {j_w} (importe del tramo del arrendamiento operativo que está dentro de la fila 14, "
                              "con el signo de esa fila, en la ventana de f y en los años H–L del ancla)")
    if fin is True and U["fin_como_deuda"]:
        # D-WM: no se piden ni la amortización ni el principal; sí lo publicado que permite enseñar la diferencia estimada (caja pagada − gasto total)
        for s_, txt in (("caja_pagada_arr_financiero", "caja pagada por los arrendamientos financieros"), ("gasto_arr_financiero", "gasto total de los arrendamientos financieros")):
            x_w = [y for y in ventana if y not in S[s_]]
            if x_w:
                faltas.append(f"series.{s_} sin declarar en {x_w} ({txt}, tal como se publica: D-WM enseña la diferencia estimada junto al resultado)")
    elif fin is True and U["fin_am_ub"] == "fuera_de_la_fila_8":
        x_w = [y for y in ventana if y not in S["da_rou_financiero_fuera"]]
        if x_w:
            faltas.append(f"series.da_rou_financiero_fuera sin declarar en {x_w} (amortización publicada del derecho de uso de los arrendamientos financieros, que se "
                          "declara fuera de la fila 8)")
    elif fin is True:
        r_w = [y for y in ventana if y not in U["rou_fin"]]
        if r_w:
            faltas.append(f"series.da_rou sin declarar en {r_w} (amortización del derecho de uso de los arrendamientos financieros dentro de la fila 8; si la empresa "
                          "no publica el desglose de sus arrendamientos financieros, «financieros.desglose»: «no_publicado» (D-WM); si esa amortización no está dentro "
                          "de la fila 8, «financieros.amortizacion_rou.ubicacion»: «fuera_de_la_fila_8»)")
    G.add("F1-US-DESGLOSE", bool(faltas or incoh), "BLOQUEA", "DATOS INVÁLIDOS" if incoh else "INCOMPLETO",
          ("; ".join(incoh + faltas))[:1500] if (faltas or incoh) else
          "arrendamientos operativos y financieros declarados por separado, con sus series" + (" · hipótesis D-US1 en " + ", ".join(U["hipotesis_D_US1"]) if U["hipotesis_D_US1"] else "")
          + (" · financieros tratados como deuda (D-WM)" if U["fin_como_deuda"] else ""), dec)
    # F1-US-C49: con US GAAP, C49 solo lleva el principal de los arrendamientos financieros (los pagos de los operativos están en el CFO)
    fin_m = Fr(0) if (fin is False or U["fin_como_deuda"]) else (media(finp[y] for y in ventana) if (fin is True and all(y in finp for y in ventana)) else None)
    exceso_c49 = defecto_c49 = False
    if C49 is None:
        G.add("F1-US-C49", False, None, None, "C49 vacío: lo señala F1-C49", dec)
    elif fin is None:
        G.add("F1-US-C49", False, None, None, "no evaluable: falta declarar si hay arrendamientos financieros (F1-US-DESGLOSE)", dec)
    elif fin_m is None:
        G.add("F1-US-C49", True, "BLOQUEA", "INCOMPLETO", f"series.pagos_arr_financiero_principal sin declarar en {[y for y in ventana if y not in finp]}: sin el "
              "principal publicado de los arrendamientos financieros no se puede comprobar que C49 no lleva pagos de los operativos (si la empresa no publica el "
              "principal por separado: «financieros.desglose»: «no_publicado», D-WM)", dec)
    elif U["fin_como_deuda"]:
        exceso_c49 = C49 > TOL_US_C49
        G.add("F1-US-C49", exceso_c49, "BLOQUEA", "DATOS INVÁLIDOS",
              (f"C49 = {float(C49)} con los arrendamientos financieros tratados como deuda (D-WM): sus pagos no se restan de la caja base (su amortización queda "
               "dentro de la propia; restar además el principal contaría el arrendamiento dos veces)") if exceso_c49 else
              "C49 = 0: los pagos de los arrendamientos financieros, tratados como deuda (D-WM), no se restan de la caja base", dec)
    else:
        # (ronda 2, R1-13) tolerancia: media unidad del último decimal con que la etapa 1 registró C49 (un cero no dice con cuántos decimales se escribió);
        # y se admite la diferencia explicada por una partida declarada con su fuente en «conciliacion_fcf_base» (componente C49), como hace K3a
        tol = TOL_US_C49 if C49 == 0 else max(TOL_US_C49, _unidad_de_redondeo(C49) / 2)
        dif = C49 - fin_m
        expl = _conciliacion_explicada(decl).get("C49", Fr(0))
        resto = dif + expl
        exceso_c49, defecto_c49 = resto > tol, resto < -tol
        explicado = abs(dif) > tol and not (exceso_c49 or defecto_c49)
        G.add("F1-US-C49", exceso_c49 or defecto_c49 or explicado, "AVISO" if explicado else "BLOQUEA", "AVISO" if explicado else "DATOS INVÁLIDOS",
              (f"C49 = {float(C49)} supera en {float(dif)} el principal publicado de los arrendamientos financieros ({float(fin_m)} de media en la ventana"
               + ("; no hay financieros" if fin is False else "") + f"), más que el redondeo de C49 (±{float(tol)})"
               + (f" y que lo explicado en conciliacion_fcf_base ({float(expl):+})" if expl else "") + ": la diferencia no está explicada. Si son pagos de arrendamientos "
               "operativos, con US GAAP ya están en el CFO y restarlos además en C49 los cuenta dos veces") if exceso_c49 else
              (f"C49 = {float(C49)} no alcanza el principal publicado de los arrendamientos financieros ({float(fin_m)} de media en la ventana): la diferencia "
               f"({float(-dif)}), mayor que el redondeo de C49 (±{float(tol)})" + (f" y que lo explicado en conciliacion_fcf_base ({float(expl):+})" if expl else "")
               + ", se pagó en financiación y no está en el FCF base: se omitiría") if defecto_c49 else
              (f"C49 = {float(C49)} difiere en {float(dif):+} del principal publicado de los arrendamientos financieros ({float(fin_m)} de media en la ventana); la "
               f"diferencia está explicada por una partida declarada en conciliacion_fcf_base ({float(expl):+}, componente C49): "
               + ("compruébese que no son pagos de arrendamientos operativos (ya están en el CFO: restarlos además en C49 los contaría dos veces)" if dif > 0 else
                  "compruébese que el principal que C49 no lleva está restado de la caja base en esa partida (si no, se omitiría)")) if explicado else
              f"C49 = {float(C49)} es el principal publicado de los arrendamientos financieros ({float(fin_m)} de media en la ventana; redondeo de C49 ±{float(tol)})", dec)
    # F1-US-DA (dos veces) y F1-US-SIM (ninguna): la amortización del derecho de uso operativo o la variación de su pasivo dentro de la reinversión
    a8_pos = sum((U["a8"].get(y, Fr(0)) for y in ventana), Fr(0)) > 0
    sin_ajuste = U["retira_de_14"] and any(y not in U["ajuste"] for y in ventana)
    am14_solo_sin = sin_ajuste and en14 == ["amortizacion_rou"]
    pas14_solo_sin = sin_ajuste and en14 == ["variacion_pasivo"]
    da1 = per == "A0_total" and a8_pos
    G.add("F1-US-DA", da1 or am14_solo_sin, "BLOQUEA", "MODELO NO APLICABLE",
          ("alquiler operativo contado dos veces: " + "; ".join(
              (["la amortización de su derecho de uso está dentro de la D&A (fila 8) y el perímetro A0 la trata como reposición, con el pago ya dentro del "
                "FCF base (CFO): hace falta un perímetro que la excluya (A1 o A2)"] if da1 else [])
              + (["la amortización de su derecho de uso está sola dentro del circulante (fila 14) y su importe no está declarado para retirarla"] if am14_solo_sin else [])))
          if (da1 or am14_solo_sin) else "la amortización del derecho de uso operativo no queda dentro de la reinversión", dec)
    s1 = per in ("A1_sin_ROU", "A2_propio", "A3_estimado") and a8_pos and not pagos_op_pos
    G.add("F1-US-SIM", s1 or pas14_solo_sin, "BLOQUEA", "FUERA DEL DOMINIO",
          ("alquiler operativo omitido: " + "; ".join(
              (["la variación de su pasivo está sola dentro del circulante (fila 14) y su importe no está declarado para retirarla: la proyección trataría "
                "como inversión que no se repite la parte del pago que reduce el pasivo"] if pas14_solo_sin else [])
              + ([f"el perímetro {per} excluye de D_X la amortización de su derecho de uso sin pagos declarados dentro del CFO"] if s1 else [])))
          if (s1 or pas14_solo_sin) else "la variación del pasivo operativo no queda sola dentro de la reinversión", "simétrica · " + dec)
    return {"pagos_op_pos": pagos_op_pos, "a8_pos": a8_pos, "exceso_c49": exceso_c49, "defecto_c49": defecto_c49, "fin_m": fin_m,
            "am14_solo_sin": am14_solo_sin, "pas14_solo_sin": pas14_solo_sin}


_GUIONES = re.compile("[%s-%s%s]" % (chr(0x2010), chr(0x2015), chr(0x2212)))   # guiones tipográficos (U+2010 a U+2015) y signo menos (U+2212)


def _nlin(s):
    """Texto normalizado para comparar líneas y citas: minúsculas, un solo espacio y un solo tipo de guion."""
    t = "" if s is None else str(s)
    t = _GUIONES.sub("-", t).replace(chr(0xA0), " ").replace(chr(0x2019), "'")
    return re.sub(r"\s+", " ", t).strip().lower()


def _sin_cifras(t):
    """Etiqueta de un renglón sin sus cifras (para reconocer la misma línea en el informe de otro ejercicio)."""
    t = _TOK.sub(" ", t)
    t = re.sub(r"(?<!\w)[-$%€£]+(?!\w)", " ", t)
    return re.sub(r"\s+", " ", t).strip(" .:·")


def _lados(t):
    """Tramos del arrendamiento que nombra un texto: conjunto de «pasivo» (la variación del pasivo) y «activo» (la amortización del derecho de uso).
    Vacío si no nombra un arrendamiento ni un derecho de uso; los dos si lo nombra sin precisar (línea genérica o neta: «Operating leases, net»)."""
    if not _LINEA_ARR.search(t) or _LINEA_AJENA.search(t):   # (R2-1) una línea ajena al tramo (deterioro, cancelación…) no nombra ninguno
        return set()
    s = ({"pasivo"} if _T_PASIVO.search(t) else set()) | ({"activo"} if _T_ACTIVO.search(t) else set())
    return s or {"pasivo", "activo"}


def _ajena(t):
    """(cierre de la ronda 2, R2-1) True si el texto nombra un arrendamiento o un derecho de uso junto a un término de otra cosa (deterioro, baja, cancelación,
    modificación, abandono, incentivos, resultado…): la línea no es un tramo del arrendamiento operativo."""
    return bool(_LINEA_ARR.search(t) and _LINEA_AJENA.search(t))


def _linea_propia(etiqueta):
    """(cierre de la ronda 2, R2-2) True si la etiqueta entera de una línea (sin sus cifras) solo nombra el arrendamiento: todas sus palabras son del
    vocabulario de un tramo (_PALABRAS_PROPIAS). Solo entonces su cifra impresa es el importe del arrendamiento dentro de la fila."""
    palabras = re.findall(r"[^\W\d_]+", _sin_cifras(_nlin(etiqueta)))
    return bool(palabras) and all(p in _PALABRAS_PROPIAS for p in palabras) and bool(_LINEA_ARR.search(_nlin(etiqueta)))


def _lineas_logicas(pagina):
    """Líneas de una página con la etiqueta ENTERA: cada renglón con cifras, precedido de los renglones anteriores de su etiqueta cuando está partida (hasta
    tres renglones sin cifras que no terminan en «:»); los renglones sin cifras que no preceden a uno con cifras van solos (cabeceras). Devuelve
    [(texto normalizado, texto tal como está)]. Sirve para que un término que está en el primer renglón de una etiqueta partida («Impairment of long-lived
    assets and operating lease» / «right-of-use assets 19 20») cuente para toda la línea."""
    out, pend = [], []
    for raw in str(pagina).splitlines():
        t = _nlin(raw)
        if not t:
            continue
        if _TOK.search(t):
            out.extend(pend[:-3])
            out.append((" ".join([x[0] for x in pend[-3:]] + [t]), " ".join([x[1] for x in pend[-3:]] + [raw.strip()])))
            pend = []
        elif t.endswith(":"):
            out.extend(pend)
            out.append((t, raw.strip()))
            pend = []
        else:
            pend.append((t, raw.strip()))
    out.extend(pend)
    return out


def _solapa(a, b, minimo=12):
    """True si dos textos normalizados son la misma línea o partes de ella: uno contiene al otro, o el final de uno es el comienzo del otro (una
    etiqueta partida en dos renglones)."""
    if not a or not b:
        return False
    if a in b or b in a:
        return True
    for x, y in ((a, b), (b, a)):
        for k in range(min(len(x), len(y)), minimo - 1, -1):
            if x.endswith(y[:k]):
                return True
    return False


def _componentes_parte(x):
    """Componentes de un lado de una partida de fase1_partes (la misma regla que fase1_historia.componentes)."""
    if isinstance(x, dict):
        if isinstance(x.get("componentes"), list):
            return [c for c in x["componentes"] if isinstance(c, dict)]
        return [x] if "impreso" in x else []
    return [c for c in x if isinstance(c, dict)] if isinstance(x, list) else []


def _paginas_texto(ruta):
    """{n: texto} de un texto con marcas «[PDF PAGE n]»; None si no se puede leer."""
    try:
        t = open(ruta, encoding="utf-8", errors="replace").read()
    except OSError:
        return None
    partes = re.split(r"\[PDF PAGE (\d+)\]", t)
    return {int(partes[i]): partes[i + 1] for i in range(1, len(partes) - 1, 2)}


def _etiqueta_completa(pagina, linea):
    """Etiqueta ENTERA de un renglón del estado de flujos (ronda 2, R1-3): el renglón con las cifras, precedido de los renglones anteriores de la misma
    etiqueta cuando está partida en dos o tres (renglones sin cifras que no terminan en «:»). La fase 1 guarda solo el renglón con las cifras: en
    «…accrued liabilities, operating lease» / «liabilities and other liabilities (426) 397» el arrendamiento está en el primero. None si el renglón no
    es una línea de la página (no se puede reconstruir)."""
    ln = _nlin(linea)
    if not ln or pagina is None:
        return None
    filas = str(pagina).splitlines()
    for i, raw in enumerate(filas):
        if ln not in _nlin(raw):
            continue
        partes, j, n, blancos = [_nlin(raw)], i - 1, 0, 0
        while j >= 0 and n < 3:
            ant = _nlin(filas[j])
            if not ant:
                blancos += 1
                if blancos > 1:
                    break
                j -= 1
                continue
            if _TOK.search(ant) or ant.endswith(":"):
                break
            partes.insert(0, ant)
            j, n, blancos = j - 1, n + 1, 0
        return " ".join(partes)
    return None


def _valor_en_la_fila(k, c, unidad):
    """(cierre de la ronda 2, R2-2) Lo que un componente de fase1_partes aporta a su fila de la Historia, en la escala del modelo (millones), con las reglas
    de fase1_historia.construir: en la fila 8 («da»), impreso × signo × escala; en la fila 14 («circulante_lineas»), lo mismo con el signo cambiado
    (+ consume caja). None si no se puede calcular (cifra no numérica, signo o unidad no válidos): entonces el importe no se compara."""
    try:
        import fase1_historia as FH
        sg = c.get("signo", 1)
        if isinstance(sg, bool) or sg not in (1, -1):
            return None
        v = Q(float(FH.numero(c["impreso"]))) * sg * Q(float(FH.ESCALA[unidad]))
    except Exception:  # noqa: BLE001 — una partida que la fase 1 no habría aceptado: no se compara
        return None
    return -v if k == "circulante_lineas" else v


def _partes_fase1(carpeta, anios_req):
    """(ronda 2, R1-3) Las líneas que la fase 1 sumó en la fila 8 (partida «da»), en la fila 14 («circulante_lineas») y en la fila 23 («arrendamientos»)
    en los años que usa el modelo, tomadas como las toma fase1_historia.construir: para el año a, el lado «anterior» del informe a+1 si tiene
    componentes y, si no, el lado «actual» del informe a (el año es el del campo «anio», entero o texto, o el del nombre del archivo). Un valor fijado
    a mano en fase1_decisiones.json, un informe ausente o una partida sin componentes quedan SIN EXAMINAR (no «sin contradicción»). De cada línea se
    reconstruye la etiqueta entera con su página de texto/ cuando está. None si el expediente no tiene fase1_partes."""
    d = os.path.join(carpeta, "fase1_partes") if carpeta else None
    if not d or not os.path.isdir(d):
        return None
    AR, ileg, huellas = {}, [], []
    for n in sorted(os.listdir(d)):
        if not n.endswith(".json"):
            continue
        ruta = os.path.join(d, n)
        j = _json(ruta)
        huellas.append(f"{n}:{_sha(ruta) if os.path.isfile(ruta) else ''}")
        p = j.get("partidas") if isinstance(j, dict) and isinstance(j.get("partidas"), dict) else None
        a = None
        if p is not None:
            try:
                a = int(j.get("anio"))
            except (TypeError, ValueError):
                m = re.search(r"(?<!\d)((?:19|20)\d\d)(?!\d)", n)
                a = int(m.group(1)) if m else None
        if p is None or a is None:
            ileg.append(n)
            continue
        AR[a] = dict(j, _nombre=n)
    dec = _json(os.path.join(carpeta, "fase1_decisiones.json"))
    dec = dec if isinstance(dec, dict) else {}
    paginas, cache = {}, {}

    def pagina(arch, n):
        if arch not in paginas:
            ruta = _fuente_del_expediente(carpeta, os.path.join("texto", str(arch))) if isinstance(arch, str) and arch else None
            paginas[arch] = _paginas_texto(ruta) if ruta else None
        pg = paginas[arch]
        return pg.get(n) if (pg and isinstance(n, int)) else None

    def comps(a, k, lado):
        if (a, k, lado) in cache:
            return cache[(a, k, lado)]
        j, out = AR.get(a), None
        if j is not None:
            p, out = j["partidas"].get(k), []
            for c in _componentes_parte(p.get(lado) if isinstance(p, dict) else None):
                lin = _nlin(c.get("linea"))
                arch = j.get("archivo") if isinstance(j.get("archivo"), str) else None
                pg = pagina(arch, c.get("pagina"))
                comp = _etiqueta_completa(pg, lin)
                texto = f"{_nlin(c.get('concepto'))} · {comp or lin}"
                # (cierre de la ronda 2) «ajena»: nombra el arrendamiento junto a otra cosa (R2-1; sus «lados» quedan vacíos); «propia»: la etiqueta entera
                # solo nombra el arrendamiento, así que su cifra impresa es el importe del tramo dentro de la fila («valor», R2-2); «pag»: su página
                out.append({"k": k, "informe": a, "lado": lado, "origen": f"{j['_nombre']}, lado «{lado}»", "nlin": lin, "etiqueta": _sin_cifras(lin),
                            "completa": comp is not None, "texto": texto, "ver": _sin_cifras(comp) if comp else texto, "lados": _lados(texto),
                            "generica": bool(_LINEA_ARR.search(texto)) and not _T_PASIVO.search(texto) and not _T_ACTIVO.search(texto),
                            "solo_fin": bool(_ES_FIN.search(texto)) and not _ES_OP.search(texto), "es_op": bool(_ES_OP.search(texto)),
                            "ajena": _ajena(texto), "propia": comp is not None and _linea_propia(comp), "con_fin": bool(_ES_FIN.search(texto)),
                            "impreso": c.get("impreso"), "valor": _valor_en_la_fila(k, c, j.get("unidad")), "pag": pg})
        cache[(a, k, lado)] = out
        return out

    usados, sin_ex = {}, {}
    for a in anios_req:
        usados[a] = {}
        for k in ("da", "circulante_lineas", "arrendamientos"):
            dk = dec.get(k) if isinstance(dec.get(k), dict) else {}
            sig, pro = comps(a + 1, k, "anterior"), comps(a, k, "actual")
            pk = AR[a]["partidas"].get(k) if a in AR else None
            if str(a) in dk:
                usados[a][k], sin_ex[(a, k)] = None, "valor fijado a mano en fase1_decisiones.json (no es la suma de las líneas)"
            elif sig:
                usados[a][k] = sig
            elif pro:
                usados[a][k] = pro
            elif isinstance(pk, dict) and pk.get("cero"):
                usados[a][k] = []   # cero declarado con su motivo: ninguna línea sumada
            else:
                usados[a][k] = None
                sin_ex[(a, k)] = "sin informe de ese ejercicio en fase1_partes" if (sig is None and pro is None) else "partida sin líneas en fase1_partes"
    todos = [c for a in sorted(AR) for k in ("da", "circulante_lineas", "cfo") for lado in ("actual", "anterior") for c in (comps(a, k, lado) or [])]
    return {"usados": usados, "sin_examinar": sin_ex, "todos": todos, "ilegibles": ileg, "informes": sorted(AR),
            "sha256": hashlib.sha256("\n".join(huellas).encode("utf-8")).hexdigest()}


def _lector_paginas(decl, carpeta):
    """Lector de las páginas de las fuentes registradas en «fuentes_series», con las mismas exigencias que F1-SERIES (documento registrado, archivo dentro
    de la carpeta del expediente con su huella vigente y texto con marcas de página). Se repite aquí, sin tocar la validación de las series de
    _guarda_fuentes_series. Devuelve pagina(documento, página) → («ok», texto) | («incompleto» o «invalido», motivo)."""
    import verificacion_entradas as VE
    fs = decl.get("fuentes_series") if isinstance(decl.get("fuentes_series"), dict) else {}
    textos = {}

    def texto(doc):
        if doc in textos:
            return textos[doc]
        f = fs.get(doc) if isinstance(fs.get(doc), dict) else None
        if f is None:
            out = ("incompleto", f"documento {doc!r} sin fuente registrada en «fuentes_series» (archivo y sha256)")
        elif carpeta is None:
            out = ("incompleto", "fuente no examinada (la evaluación no recibió la carpeta del expediente)")
        else:
            ruta = _fuente_del_expediente(carpeta, f.get("archivo"))
            if ruta is None:
                fuera = _fuera_del_expediente(carpeta, f.get("archivo"))
                out = ("invalido" if fuera else "incompleto",
                       f"la fuente {f.get('archivo')!r} de {doc!r} " + ("está fuera de la carpeta del expediente" if fuera else "no existe en el expediente"))
            elif not str(f.get("sha256") or "").strip():
                out = ("incompleto", f"la fuente {f.get('archivo')!r} de {doc!r} sin «sha256»")
            elif VE._sha(ruta) != str(f["sha256"]).strip().lower():
                out = ("invalido", f"la fuente {f.get('archivo')!r} de {doc!r} cambió (sha256 distinto del declarado)")
            else:
                rt, out = ruta, None
                if not ruta.lower().endswith(".txt"):
                    rt = _fuente_del_expediente(carpeta, f.get("archivo_texto"))
                    if rt is None or not str(f.get("sha256_texto") or "").strip():
                        out = ("incompleto", f"{doc!r}: la fuente no es un texto con marcas de página y su «archivo_texto» (con «sha256_texto») no está en el expediente")
                    elif VE._sha(rt) != str(f["sha256_texto"]).strip().lower():
                        out = ("invalido", f"{doc!r}: el texto de la fuente cambió (sha256_texto distinto del declarado)")
                if out is None:
                    out = ("ok", rt)
        textos[doc] = out
        return out

    def pagina(doc, n):
        est_t, rt = texto(str(doc or ""))
        if est_t != "ok":
            return est_t, rt
        est, pag = VE._pagina_examinable(rt, n)
        if est != "ok":
            return ("invalido" if est == "discrepancia" else "incompleto"), pag
        return "ok", pag
    return pagina


def _lineas_con_cita(pagina, cn):
    """Líneas de la página (un renglón, o dos o tres renglones seguidos de una etiqueta partida) en las que está la cita. Sirve para saber DE QUÉ línea es
    una cita: «operating lease liabilities» también está dentro de «Right-of-use assets obtained in exchange for new operating lease liabilities».
    (cierre de la ronda 2, R2-1) Primero, las líneas con la etiqueta ENTERA (_lineas_logicas) que contienen la cita: así una cita tomada del último
    renglón de «Impairment of long-lived assets and operating lease» / «right-of-use assets» se reconoce como de una línea ajena al tramo."""
    out = [t for t, _ in _lineas_logicas(pagina) if cn in t]
    if out:
        return out
    filas = [x for x in (_nlin(r) for r in str(pagina).splitlines()) if x]
    for i in range(len(filas)):
        for n in (1, 2, 3):
            t = " ".join(filas[i:i + n])
            if cn in t:
                if n == 1 or cn not in " ".join(filas[i + 1:i + n]):   # la cita empieza en el renglón i
                    out.append(t)
                break
    return out


def _contraste_us(G, decl, carpeta, U, anios_req, rou_fin_pos, solo_existencia=False):
    """(F1 · US GAAP; ronda 2, R1-3 y R1-6) F1-US-FILAS: quien afirma una ubicación tiene que enseñar la línea, y lo que el programa no puede contrastar
    con una línea no da una conclusión sin condición. Contrasta lo declarado con (a) las páginas citadas de las fuentes registradas y (b) las líneas
    que la fase 1 sumó de verdad en la fila 8 («da») y en la fila 14 («circulante_lineas») en los años que usa el modelo (_partes_fase1):
      - «fila_8» o «fila_14»: la cita nombra el arrendamiento y su tramo (la línea del pasivo para la variación del pasivo; la del activo o del gasto
        para la amortización; o una línea que nombre los dos), y una línea sumada en esa fila lo nombra en cada año del modelo → CONTRASTADA. Si la
        línea citada es del estado de flujos y la fase 1 no la sumó ahí → DATOS INVÁLIDOS. Si no se puede comprobar → SIN CONTRASTAR;
      - «fuera_de_las_filas_8_y_14»: la cita es una línea del estado de flujos que nombra el tramo y que la fase 1 NO sumó; si está entre las sumadas
        → DATOS INVÁLIDOS; si la página no es la del estado de flujos → INCOMPLETO (sin esa línea, la ubicación es «no_publicada»);
      - «no_publicada» (D-US1): la página examinada es la del estado de flujos y no muestra una línea de ese tramo (patrón amplio; solo se excluye la
        línea del OTRO tramo cuando está declarada con su ubicación, la información complementaria y las líneas solo de financieros);
      - en todos los casos: una línea sumada que nombra un tramo declarado en otro sitio contradice la declaración → DATOS INVÁLIDOS;
      - los dos tramos «fila_14» (D-US2 bis): hacen falta las dos líneas contrastadas; si no, INCOMPLETO (no se publica el valor de la hoja).
    (cierre de la ronda 2, revisión R2)
      - R2-1 · una línea que nombra el arrendamiento junto a otra cosa (deterioro, cancelación, modificación, incentivos, resultado…: _LINEA_AJENA) no es
        un tramo: no hace saltar «manda el dato» frente a «no_publicada», no vale como cita de una ubicación (INCOMPLETO) y no cuenta entre las sumadas;
      - R2-2 · el importe declarado dentro de una fila se compara con la cifra impresa de la línea PROPIA que la fase 1 sumó ahí (otro importe, también
        un 0 → DATOS INVÁLIDOS); con una línea mezclada dentro de la fila 14 el importe no se puede comparar → SIN CONTRASTAR (condicionada, con cota);
      - R2-3 · la amortización del derecho de uso FINANCIERO dentro de la fila 8 por omisión: si el estado de flujos la muestra en una línea propia que
        la fase 1 no sumó en la fila 8 → DATOS INVÁLIDOS; si ninguna línea sumada la nombra, queda «por_omision» (K3b no dice «contrastado»).
    Los tramos SIN CONTRASTAR dejan la conclusión CONDICIONADA, con su cota (_informes_us). Los problemas de las citas y de sus páginas se pasan a
    F1-SERIES. solo_existencia (motor B): solo las citas de existencia de cada clase; las ubicaciones son del motor A."""
    dec = "US GAAP · ubicaciones frente a las líneas del expediente (D-US1: manda el dato)"
    C = {"invalidas": [], "incompletas": [], "citas_ok": 0, "aus_ok": 0, "tramos": {}, "sin_contrastar": {}, "fase1_partes": None, "lineas_ajenas": [],
         "importe_sin_contrastar": []}
    U["contraste"] = C
    pagina = _lector_paginas(decl, carpeta)
    P = _partes_fase1(carpeta, anios_req)
    U["partes"] = P
    if P is not None:
        C["fase1_partes"] = {"informes": P["informes"], "sin_examinar": [f"{a} · {k}: {m}" for (a, k), m in sorted(P["sin_examinar"].items()) if k != "arrendamientos"],
                             "ilegibles": P["ilegibles"], "sha256": P["sha256"]}
        if not P["todos"]:
            P = None   # una carpeta fase1_partes sin ninguna línea de explotación legible no permite contrastar nada: como si no la hubiera

    def pag_de(et, e):
        est, pag = pagina(e.get("documento"), e.get("pagina"))
        if est != "ok":
            (C["invalidas"] if est == "invalido" else C["incompletas"]).append(f"{et}: {pag}")
            return None
        return pag

    def en_la_pagina(pag):
        """Líneas de explotación de la fase 1 (da, circulante y CFO, de cualquier informe) que están en la página: con dos o más, es la página del estado de flujos."""
        pn = _nlin(pag)
        return [c for c in P["todos"] if c["nlin"] and c["nlin"] in pn]

    def es_estado(pag):
        return len({c["nlin"] for c in en_la_pagina(pag)}) >= 2

    def explotacion(pag):
        """La página hasta el total del flujo de explotación (el renglón que la fase 1 tomó como CFO), incluido: las líneas que nombran un arrendamiento
        después de él son de inversión o de financiación (principal de los financieros) o información complementaria, no tramos del operativo."""
        if P is None:
            return pag
        cfo = {c["nlin"] for c in P["todos"] if c["k"] == "cfo" and c["nlin"]}
        filas = str(pag).splitlines()
        for i, raw in enumerate(filas):
            t = _nlin(raw)
            if t and any(x in t for x in cfo):
                return "\n".join(filas[:i + 1])
        return pag

    pag_ok = {}
    for et, e in U["evidencias"]:   # existencia de cada clase y tramos con ubicación declarada: la cita literal está en su página
        pag = pag_de(et, e)
        if pag is None:
            continue
        cita = _nlin(e.get("cita"))
        if len(cita) < CITA_MINIMA:
            C["incompletas"].append(f"{et}: la cita tiene menos de {CITA_MINIMA} caracteres: no identifica una línea")
        elif cita not in _nlin(pag):
            C["invalidas"].append(f"{et}: la cita no está en la página {e.get('pagina')} de {str(e.get('documento'))!r}")
        else:
            C["citas_ok"] += 1
            pag_ok[et] = pag
    if solo_existencia:
        return C
    for et, e in U["ausencias"]:    # D-US1: la página examinada es la del estado de flujos y no muestra una línea de ese tramo
        clave = et.rsplit(".", 1)[-1]
        pag = pag_de(et, e)
        if pag is None:
            continue
        otras = [_nlin(U["ev"][k].get("cita")) for k in _LADO_TRAMO if k != clave and U["ub_decl"].get(k) not in (None, "no_publicada")]
        lineas = []
        for t, raw in _lineas_logicas(explotacion(pag)):   # con la etiqueta entera: lo que hace ajena una línea puede estar en su primer renglón
            if not _LINEA_ARR.search(t) or _LINEA_SUPL.search(t) or (_ES_FIN.search(t) and not _ES_OP.search(t)):
                continue
            if _ajena(t):   # (R2-1) deterioro, cancelación, modificación…: no es un tramo; queda a la vista y no hace saltar «manda el dato»
                if raw not in C["lineas_ajenas"]:
                    C["lineas_ajenas"].append(raw)
                continue
            if _LADO_TRAMO[clave] not in _lados(t) or any(_solapa(o, t) for o in otras):
                continue
            lineas.append(raw)
        if P is not None and not es_estado(pag):
            C["incompletas"].append(f"{et}: «no_publicada», pero la página {e.get('pagina')} de {str(e.get('documento'))!r} no es la del estado de flujos que usó la "
                                    "fase 1 (no lleva sus líneas de explotación): se examina la página del estado de flujos")
        elif lineas:
            C["invalidas"].append(f"{et}: «no_publicada», pero la página {e.get('pagina')} de {str(e.get('documento'))!r} muestra una línea del arrendamiento "
                                  f"operativo ({lineas[0][:90]!r}): donde la empresa publica la línea manda el dato (D-US1); declara su ubicación")
        else:
            C["aus_ok"] += 1

    contradice, insuf = [], []
    fila = {"da": "8", "circulante_lineas": "14"}

    def usados(a, k):
        return None if P is None else P["usados"].get(a, {}).get(k)

    def completo(a, k):
        us_ = usados(a, k)
        return us_ is not None and all(c["completa"] for c in us_)

    def marcar(clave, estado, motivo=None):
        C["tramos"].setdefault(clave, {})
        C["tramos"][clave].update({"estado": estado, "motivo": motivo})
        if estado == "sin_contrastar":
            C["sin_contrastar"][clave] = motivo
        else:
            C["sin_contrastar"].pop(clave, None)

    def enlazadas(pag, cn, ks):
        """Líneas sumadas (de las filas ks) que son la línea citada: su etiqueta entera en la página citada contiene la cita, o los renglones de la página
        en que está la cita (uno, o dos o tres seguidos de una etiqueta partida) incluyen su renglón de las cifras."""
        de_la_cita = _lineas_con_cita(pag, cn)
        return [c for c in en_la_pagina(pag) if c["k"] in ks and not c["ajena"]   # (R2-1) una línea ajena al tramo no es «la línea citada»
                and (cn in (_etiqueta_completa(pag, c["nlin"]) or c["nlin"]) or any(c["nlin"] in t for t in de_la_cita))]

    def importe_frente_a_la_linea(clave, k_decl, etqs, lado):
        """(cierre de la ronda 2, R2-2) El importe declarado dentro de la fila frente a la cifra impresa de la línea sumada que nombra el tramo. Si la línea
        es PROPIA (su etiqueta entera solo nombra el arrendamiento), lo que hay dentro de la fila es exactamente lo que esa línea aporta: otro importe →
        DATOS INVÁLIDOS (también un 0, se declare como se declare). Si es una línea mezclada con otras partidas, o su cifra no se puede leer, el importe
        no se puede comparar: con un tramo solo dentro de la fila 14 queda SIN CONTRASTAR (conclusión condicionada, con el pago o el coste como cota); en
        la fila 8 es el límite general de la D&A (el importe lleva su propia cifra publicada: F1-SERIES). Tampoco se compara la cifra de una línea que
        nombra los financieros, ni, en la fila 8, la de una línea genérica del derecho de uso si la amortización de los financieros puede estar dentro."""
        if k_decl == "circulante_lineas" and not U["retira_de_14"]:
            return   # los dos tramos dentro de la fila 14 (D-US2 bis): no se retira nada
        decl_ = U["ajuste"] if k_decl == "circulante_lineas" else U["a8"]
        mal, sin_cifra = [], []

        def comparable(c):
            """La cifra impresa de la línea es la del tramo operativo: línea propia con cifra legible que no nombra los financieros y, en la fila 8, que
            nombra los operativos o no puede llevar la amortización de los financieros (dentro de la fila 8 por omisión o como activos propios, D-WM)."""
            return (c["propia"] and c["valor"] is not None and not c["con_fin"]
                    and (k_decl != "da" or c["es_op"] or not fin_en_8))

        for a in anios_req:
            ls_ = [c for c in (usados(a, k_decl) or []) if c["etiqueta"] in etqs or (lado in c["lados"] and not c["solo_fin"])]
            if not ls_ or a not in decl_:
                continue   # el año sin línea o sin importe declarado lo señalan el contraste de la ubicación y F1-US-DESGLOSE
            if all(comparable(c) for c in ls_):
                v = sum((c["valor"] for c in ls_), Fr(0))
                if abs(decl_[a] - v) > TOL_LIBRO * max(1, abs(v)):
                    mal.append((a, decl_[a], v, ls_[0]))
            else:
                sin_cifra.append(a)
        if mal:
            a, x, v, c = mal[0]
            contradice.append(f"{_NOMBRE_TRAMO[clave]} está declarada dentro de la fila {fila[k_decl]} con un importe de {float(x)} en {a}"
                              + (f" (y otro distinto del impreso en {[m[0] for m in mal[1:]]})" if len(mal) > 1 else "")
                              + f", pero la línea propia que la fase 1 sumó en esa fila ({c['origen']}: «{c['ver'][:110]}», impreso {str(c['impreso'])[:24]!r}) le "
                              f"aporta {float(v)}: el importe dentro de la fila es el de su línea")
            marcar(clave, "contradicha", "el importe declarado no es el de la línea propia sumada en esa fila")
        elif sin_cifra and k_decl == "circulante_lineas":
            marcar(clave, "sin_contrastar", f"la ubicación está contrastada, pero el importe no: en {sin_cifra} la línea sumada en la fila 14 que nombra ese tramo "
                   "es una línea mezclada con otras partidas (o su cifra no se puede leer) y el importe declarado no se puede comparar con una cifra impresa")
            C["importe_sin_contrastar"].append(clave)

    def del_modelo(pag):
        """La página citada es la del estado de flujos de un informe de los años que usa el modelo (o del siguiente, cuyo comparativo da el último de ellos)."""
        return bool({c["informe"] for c in en_la_pagina(pag)} & (set(anios_req) | {a + 1 for a in anios_req}))

    # (R2-2) la fila 8 puede llevar también la amortización del derecho de uso de los financieros (dentro por omisión, o con D-WM como activos propios):
    # una línea genérica de la D&A («Amortization of right-of-use assets») puede sumar las dos, y su cifra impresa no es la del tramo operativo
    fin_en_8 = U["fin"] is not False and (U["fin_como_deuda"] or U["fin_am_ub"] == "fila_8")

    if U["op"] is True:
        for clave in ("amortizacion_rou", "variacion_pasivo"):
            ub, e = U["ub_decl"][clave], U["ev"][clave]
            et = f"arrendamientos_us_gaap.operativos.{clave}"
            lado, nom = _LADO_TRAMO[clave], _NOMBRE_TRAMO[clave]
            C["tramos"][clave] = {"ubicacion_declarada": ub, "estado": None, "motivo": None}
            if ub is None:
                marcar(clave, "sin_declarar")
                continue
            if ub == "no_publicada":
                marcar(clave, "hipotesis_D_US1", "la empresa no publica la línea: hipótesis general declarada (no es un dato)")
                continue
            if et not in pag_ok:
                marcar(clave, "sin_evidencia", "la cita no se ha podido examinar en su página (F1-SERIES o F1-US-DESGLOSE)")
                continue
            cn, pag = _nlin(e.get("cita")), pag_ok[et]
            if _ajena(cn):   # (R2-1)
                insuf.append(f"{et}: la cita {str(e.get('cita'))[:80]!r} nombra el arrendamiento junto a otra cosa (deterioro, baja, cancelación, modificación, "
                             f"abandono, incentivos, resultado…): no es la línea de {nom} y no prueba su ubicación; si la empresa no publica la línea del tramo, la "
                             "ubicación es «no_publicada» (hipótesis D-US1)")
                marcar(clave, "insuficiente", "la cita es una línea ajena al tramo")
                continue
            ls = _lados(cn)
            if not ls or _LINEA_SUPL.search(cn):
                insuf.append(f"{et}: la cita {str(e.get('cita'))[:80]!r} no nombra el arrendamiento ni el derecho de uso (o es información complementaria del estado de "
                             "flujos): quien afirma una ubicación enseña la línea; si la empresa no publica la línea, la ubicación es «no_publicada» (hipótesis D-US1)")
                marcar(clave, "insuficiente", "la cita no nombra el arrendamiento")
                continue
            if lado not in ls:
                insuf.append(f"{et}: la cita {str(e.get('cita'))[:80]!r} nombra {'el pasivo' if lado == 'activo' else 'el activo o el gasto'} del arrendamiento, no {nom}: "
                             "cada tramo se prueba con su línea (o con una línea que nombre los dos)")
                marcar(clave, "insuficiente", "la cita nombra el otro tramo")
                continue
            # la cita tiene que ser de una línea de la conciliación: no vale si en su página solo está dentro de líneas de información complementaria
            # (altas de derechos de uso, caja pagada) o de arrendamientos financieros
            de_la_cita = [t for t in _lineas_con_cita(explotacion(pag), cn) if not _LINEA_SUPL.search(t) and not (_ES_FIN.search(t) and not _ES_OP.search(t))]
            if de_la_cita and all(_ajena(t) for t in de_la_cita):   # (R2-1) la cita es un trozo de una línea ajena al tramo
                insuf.append(f"{et}: la cita {str(e.get('cita'))[:80]!r} solo está, en la página {e.get('pagina')}, dentro de una línea que nombra el arrendamiento "
                             f"junto a otra cosa («{de_la_cita[0][:110]}»: deterioro, baja, cancelación, modificación, abandono, incentivos, resultado…): no enseña "
                             f"la línea de {nom}; si la empresa no publica la línea del tramo, la ubicación es «no_publicada» (hipótesis D-US1)")
                marcar(clave, "insuficiente", "la cita es de una línea ajena al tramo")
                continue
            if not de_la_cita:
                insuf.append(f"{et}: la cita {str(e.get('cita'))[:80]!r} solo está, en la página {e.get('pagina')}, dentro de líneas de información complementaria o de "
                             "arrendamientos financieros, o después del total del flujo de explotación (inversión o financiación): no enseña la línea de "
                             f"{nom}; si la empresa no publica la línea, la ubicación es «no_publicada» (hipótesis D-US1)")
                marcar(clave, "insuficiente", "la cita no es de una línea de la conciliación del flujo de explotación")
                continue
            if P is None:
                marcar(clave, "sin_contrastar", "sin fase1_partes en el expediente: la ubicación declarada no se ha contrastado con las líneas que la fase 1 sumó en las filas 8 y 14")
                continue
            enl = enlazadas(pag, cn, ("da", "circulante_lineas"))
            if ub == "fuera_de_las_filas_8_y_14":
                if enl:
                    contradice.append(f"{nom} está declarada fuera de las filas 8 y 14, pero la línea citada está entre las que la fase 1 sumó en la fila "
                                      f"{fila[enl[0]['k']]} ({enl[0]['origen']}: «{enl[0]['ver'][:130]}»)")
                    marcar(clave, "contradicha", "la línea citada está entre las sumadas")
                    continue
                if not es_estado(pag):
                    insuf.append(f"{et}: «fuera de las filas» se prueba con una línea del estado de flujos que nombre el arrendamiento y que la fase 1 no sumó en las "
                                 f"filas 8 y 14; la página citada ({e.get('pagina')} de {str(e.get('documento'))!r}) no es la del estado de flujos que usó la fase 1 (no "
                                 "lleva sus líneas de explotación). Si no hay tal línea, la ubicación es «no_publicada» (hipótesis D-US1)")
                    marcar(clave, "insuficiente", "la cita no es una línea del estado de flujos")
                    continue
                req = ("circulante_lineas",) if clave == "variacion_pasivo" else ("da", "circulante_lineas")
                falta = [f"{a} (fila {fila[k]})" for a in anios_req for k in req if not completo(a, k)]
                if not del_modelo(pag):
                    marcar(clave, "sin_contrastar", "la página citada no es la del estado de flujos de un informe de los años que usa el modelo")
                elif falta:
                    marcar(clave, "sin_contrastar", "la línea citada no está entre las sumadas en el informe citado, pero no se han podido examinar enteras las líneas "
                           f"sumadas en {', '.join(falta[:6])}")
                else:
                    marcar(clave, "contrastada", "la línea citada es del estado de flujos y la fase 1 no la sumó en las filas 8 y 14; ninguna línea sumada en los "
                           "años del modelo nombra ese tramo")
                continue
            k_decl = {"fila_8": "da", "fila_14": "circulante_lineas"}[ub]
            otros = [c for c in enl if c["k"] != k_decl]
            if otros:
                contradice.append(f"{nom} está declarada dentro de la fila {fila[k_decl]}, pero la línea citada está entre las que la fase 1 sumó en la fila "
                                  f"{fila[otros[0]['k']]} ({otros[0]['origen']})")
                marcar(clave, "contradicha", "la línea citada está sumada en la otra fila")
                continue
            etqs = {c["etiqueta"] for c in enl if len(c["etiqueta"]) >= 6}
            con, sin, sin_ex = [], [], []
            for a in anios_req:
                us_ = usados(a, k_decl)
                if us_ is None:
                    sin_ex.append(a)
                elif any(c["etiqueta"] in etqs or (lado in c["lados"] and not c["solo_fin"]) for c in us_):
                    con.append(a)
                else:
                    sin.append(a)
            if es_estado(pag) and not enl and not con:
                contradice.append(f"{nom} está declarada dentro de la fila {fila[k_decl]}, pero la línea citada, que está en la página del estado de flujos, no es "
                                  "ninguna de las que la fase 1 sumó en esa fila, y ninguna línea sumada en los años del modelo nombra ese tramo")
                marcar(clave, "contradicha", "la línea citada no está entre las sumadas en esa fila")
            elif not sin and not sin_ex:
                marcar(clave, "contrastada", f"una línea sumada en la fila {fila[k_decl]} nombra ese tramo en {con}")
                importe_frente_a_la_linea(clave, k_decl, etqs, lado)
            else:
                marcar(clave, "sin_contrastar", "; ".join(([f"ninguna línea sumada en la fila {fila[k_decl]} nombra ese tramo en {sin}"] if sin else [])
                                                          + ([f"sin líneas examinadas en {sin_ex}"] if sin_ex else [])))
    # (R1-16) financieros: la amortización de su derecho de uso declarada FUERA de la fila 8
    fin_fuera = U["fin"] is True and not U["fin_como_deuda"] and U["fin_am_ub"] == "fuera_de_la_fila_8"
    if fin_fuera:
        clave, et = "amortizacion_rou_financiero", "arrendamientos_us_gaap.financieros.amortizacion_rou"
        C["tramos"][clave] = {"ubicacion_declarada": "fuera_de_la_fila_8", "estado": None, "motivo": None}
        if et not in pag_ok:
            marcar(clave, "sin_evidencia", "la cita no se ha podido examinar en su página (F1-SERIES o F1-US-DESGLOSE)")
        else:
            cn, pag = _nlin(U["ev"][clave].get("cita")), pag_ok[et]
            if not _LINEA_ARR.search(cn) or _LINEA_SUPL.search(cn):
                insuf.append(f"{et}: la cita no nombra el arrendamiento ni el derecho de uso: quien afirma una ubicación enseña la línea")
                marcar(clave, "insuficiente", "la cita no nombra el arrendamiento")
            elif P is None:
                marcar(clave, "sin_contrastar", "sin fase1_partes en el expediente: no se ha contrastado con las líneas que la fase 1 sumó en la fila 8")
            else:
                enl = enlazadas(pag, cn, ("da",))
                falta = [a for a in anios_req if not completo(a, "da")]
                if enl:
                    contradice.append(f"{_NOMBRE_TRAMO[clave]} está declarada fuera de la fila 8, pero la línea citada está entre las que la fase 1 sumó en la fila 8 "
                                      f"({enl[0]['origen']})")
                    marcar(clave, "contradicha", "la línea citada está entre las sumadas en la fila 8")
                elif es_estado(pag) and not falta:
                    marcar(clave, "contrastada", "la línea citada es del estado de flujos y la fase 1 no la sumó en la fila 8")
                else:
                    marcar(clave, "sin_contrastar", "la cita no es una línea del estado de flujos que usó la fase 1" if not es_estado(pag)
                           else f"no se han podido examinar enteras las líneas sumadas en la fila 8 en {falta}")
    # (cierre de la ronda 2, R2-3) financieros con la amortización de su derecho de uso DENTRO de la fila 8 (por omisión, como NIIF 16): manda el dato si el
    # estado de flujos la muestra en una línea propia que la fase 1 no sumó en la fila 8; y solo cuenta como contrastada si una línea sumada la nombra
    fin8 = U["fin"] is True and not U["fin_como_deuda"] and U["fin_am_ub"] == "fila_8" and rou_fin_pos
    if fin8:
        clave = "amortizacion_rou_financiero"
        C["tramos"][clave] = {"ubicacion_declarada": "fila_8", "estado": None, "motivo": None}
        if P is None:
            marcar(clave, "por_omision", "dentro de la fila 8 por omisión (como NIIF 16); sin fase1_partes no se ha contrastado con las líneas sumadas en la fila 8")
        else:
            pags, a_la_vista = [], []
            for pg in [c["pag"] for c in P["todos"] if c["pag"] is not None] + list(pag_ok.values()):
                if not any(pg is x for x in pags) and es_estado(pg) and del_modelo(pg):
                    pags.append(pg)
            for pg in pags:
                sumadas = [c["nlin"] for c in en_la_pagina(pg) if c["k"] == "da"]
                for t, raw in _lineas_logicas(explotacion(pg)):
                    if (_LINEA_ARR.search(t) and not _LINEA_SUPL.search(t) and not _ajena(t) and _ES_FIN.search(t) and not _ES_OP.search(t) and "activo" in _lados(t)
                            and not any(s in t for s in sumadas) and raw not in a_la_vista):
                        a_la_vista.append(raw)
            sin_l = [a for a in anios_req if not any("activo" in c["lados"] and (c["con_fin"] or not c["es_op"]) for c in (usados(a, "da") or []))]
            if a_la_vista:
                contradice.append(f"{_NOMBRE_TRAMO[clave]} está declarada dentro de la fila 8 (series.da_rou; es la ubicación por omisión), pero el estado de flujos la "
                                  f"muestra en una línea propia que la fase 1 no sumó en la fila 8 («{a_la_vista[0][:120]}»): se declara «fuera_de_la_fila_8» con esa "
                                  "línea (financieros.amortizacion_rou) y su cifra en series.da_rou_financiero_fuera")
                marcar(clave, "contradicha", "el estado de flujos la muestra en una línea propia que la fase 1 no sumó en la fila 8")
            elif not sin_l:
                marcar(clave, "contrastada", "una línea sumada en la fila 8 nombra la amortización de arrendamientos financieros o de derechos de uso en los años del modelo")
            else:
                marcar(clave, "por_omision", f"dentro de la fila 8 por omisión (como NIIF 16): ninguna línea sumada en la fila 8 la nombra en {sin_l}; no se ha contrastado "
                       "con una línea (el importe es el declarado en series.da_rou)")
    # líneas sumadas en los años del modelo que nombran un tramo declarado en otro sitio: la declaración contradice al expediente
    if P is not None and U["op"] is not None:
        en8 = U["op"] is True and U["ub_decl"]["amortizacion_rou"] == "fila_8"
        fuera14 = [k for k in _LADO_TRAMO if U["ub_decl"].get(k) != "fila_14"]
        vistas = set()
        for a in anios_req:
            for c in usados(a, "circulante_lineas") or []:
                if not c["lados"] or c["solo_fin"] or ("14", c["etiqueta"]) in vistas:
                    continue
                if U["op"] is False:
                    mal = ["operativos.existen = false"]
                elif c["generica"]:
                    mal = ["ningún tramo del arrendamiento operativo está declarado dentro de la fila 14"] if len(fuera14) == 2 else []
                else:
                    mal_k = [k for k in fuera14 if _LADO_TRAMO[k] in c["lados"]]
                    mal = [f"{_NOMBRE_TRAMO[k]} está declarada {_UB_TXT.get(U['ub_decl'].get(k), 'sin ubicación')}" for k in mal_k]
                    for k in mal_k:
                        marcar(k, "contradicha", "una línea sumada en la fila 14 nombra ese tramo")
                if mal:
                    vistas.add(("14", c["etiqueta"]))
                    contradice.append(f"la fila 14 del expediente suma una línea que nombra el arrendamiento ({c['origen']}: «{c['ver'][:130]}») y " + " y ".join(mal))
            for c in usados(a, "da") or []:
                if not c["lados"] or ("8", c["etiqueta"]) in vistas:
                    continue
                if c["solo_fin"]:
                    mal = (["financieros.existen = false"] if U["fin"] is False else
                           [f"{_NOMBRE_TRAMO['amortizacion_rou_financiero']} está declarada fuera de la fila 8"] if fin_fuera else [])
                    if mal and fin_fuera:
                        marcar("amortizacion_rou_financiero", "contradicha", "una línea sumada en la fila 8 nombra un arrendamiento financiero")
                elif en8 or (fin8 and not c["es_op"]):
                    mal = []
                elif U["op"] is False:
                    mal = ["operativos.existen = false" + ("" if U["fin"] else " y no hay amortización de derecho de uso financiero declarada dentro de la fila 8")]
                else:
                    mal = [f"{_NOMBRE_TRAMO['amortizacion_rou']} del arrendamiento operativo está declarada {_UB_TXT.get(U['ub_decl'].get('amortizacion_rou'), 'sin ubicación')}"
                           + ("" if fin8 else " (y no hay amortización de derecho de uso financiero declarada dentro de la fila 8)")]
                    marcar("amortizacion_rou", "contradicha", "una línea sumada en la fila 8 nombra el derecho de uso o el arrendamiento")
                if mal:
                    vistas.add(("8", c["etiqueta"]))
                    contradice.append(f"la fila 8 del expediente suma una línea que nombra un arrendamiento o un derecho de uso ({c['origen']}: «{c['ver'][:130]}») y "
                                      + " y ".join(mal))
    # D-US2 bis: con los dos tramos dentro de la fila 14 solo se publica el valor de la hoja si el expediente muestra las dos líneas
    U["dos_lineas_comprobadas"] = None
    if U["op"] is True and U["dos_en_14"]:
        mal14 = [k for k in _LADO_TRAMO if C["tramos"].get(k, {}).get("estado") != "contrastada"]
        U["dos_lineas_comprobadas"] = not mal14
        pend = [k for k in mal14 if C["tramos"].get(k, {}).get("estado") in ("sin_contrastar", "sin_evidencia")]
        if pend:
            insuf.append("D-US2 bis: con los dos tramos dentro de la fila 14 se publica el valor de la hoja solo si el expediente muestra las dos líneas (la del "
                         "activo y la del pasivo) entre las sumadas en la fila 14; no se ha podido comprobar: "
                         + "; ".join(f"{_NOMBRE_TRAMO[k]}: {C['tramos'][k]['motivo']}" for k in pend))
            for k in pend:
                C["sin_contrastar"].pop(k, None)   # no queda condicionada: bloquea
    C["contradicciones"], C["insuficientes"] = contradice, insuf
    est = {k: v.get("estado") for k, v in C["tramos"].items()}
    C["fundamento"] = ("hipótesis" if "hipotesis_D_US1" in est.values() else "") + (" y " if ("hipotesis_D_US1" in est.values() and C["sin_contrastar"]) else "") \
        + ("declarado" if C["sin_contrastar"] else "")
    if not C["fundamento"]:
        # sin tramos que contrastar (no hay operativos): «contrastado» solo si las líneas de las filas 8 y 14 se examinaron enteras en los años del modelo
        C["fundamento"] = "contrastado" if (est and all(v == "contrastada" for v in est.values())) or \
            (not est and P is not None and all(completo(a, k) for a in anios_req for k in ("da", "circulante_lineas"))) else "declarado"
    resumen = "; ".join(f"{_NOMBRE_TRAMO[k]}: {_UB_TXT.get(v.get('ubicacion_declarada'), v.get('ubicacion_declarada'))} · {str(v.get('estado')).replace('_', ' ')}"
                        for k, v in C["tramos"].items())
    ajenas = (" · líneas de la página examinada que nombran el arrendamiento junto a otra cosa y no son un tramo (no cuentan; R2-1): "
              + "; ".join(f"«{x[:100]}»" for x in C["lineas_ajenas"][:3])) if C["lineas_ajenas"] else ""
    if contradice or insuf:
        G.add("F1-US-FILAS", True, "BLOQUEA", "DATOS INVÁLIDOS" if contradice else "INCOMPLETO",
              ((("la declaración contradice al expediente: " + "; ".join(contradice[:4]) + ": donde hay línea manda el dato (D-US1)") if contradice else "")
               + (" · " if (contradice and insuf) else "") + "; ".join(insuf[:3]))[:1800], dec)
    elif C["sin_contrastar"]:
        G.add("F1-US-FILAS", True, "AVISO", "AVISO", "ubicaciones declaradas SIN CONTRASTAR con una línea del expediente: "
              + "; ".join(f"{_NOMBRE_TRAMO[k]} ({_UB_TXT.get(C['tramos'][k]['ubicacion_declarada'])}): {m}" for k, m in C["sin_contrastar"].items())
              + ". La conclusión queda CONDICIONADA, con su cota (F1-US-HIPOTESIS)" + ajenas, dec)
    elif P is None:
        G.add("F1-US-FILAS", True, "INFORMA", "INFORMA", "sin fase1_partes en el expediente: no se ha podido contrastar lo declarado con las líneas que la fase 1 sumó "
              "en las filas 8 y 14" + (f" ({resumen})" if resumen else "") + ajenas, dec)
    else:
        G.add("F1-US-FILAS", False, None, None, (f"{resumen} · " if resumen else "") + "lo declarado no contradice las líneas que la fase 1 sumó en las filas 8 y 14 en los "
              f"años que usa el modelo ({anios_req[0]}–{anios_req[-1]}; informes {P['informes'][0] if P['informes'] else '—'}–{P['informes'][-1] if P['informes'] else '—'})"
              + (f"; sin examinar: {'; '.join(C['fase1_partes']['sin_examinar'][:4])}" if C["fase1_partes"]["sin_examinar"] else "")
              + (f"; no se pudieron leer: {', '.join(P['ilegibles'][:3])}" if P["ilegibles"] else "") + ajenas, dec)
    return C


def _k3b_us(G, k3, U, f, per, rou_pos, c49_pos):
    """(F1 · US GAAP) K3b por clase. Operativos: 1 (coste en el EBIT y pago en el CFO) + 1 si C49 lleva sus pagos + 1 si la amortización de
    su derecho de uso queda en D_X o sola en el circulante − 1 si la variación de su pasivo queda sola en el circulante. Financieros: como
    NIIF 16 (amortización en el margen + principal en C49 − la que f devuelve); tratados como deuda (D-WM) no se cuentan aquí. Cada clase que
    exista tiene que dar exactamente uno. (ronda 2, R1-15) K3b repite la clasificación declarada: no es una comprobación independiente; lleva su
    fundamento (contrastado con las líneas del expediente, según lo declarado o según la hipótesis D-US1) y solo cuenta como conforme si las
    ubicaciones se contrastaron con líneas."""
    nombre = {0: "ninguna vez", 1: "una vez", 2: "dos veces", 3: "tres veces"}
    fund = (U.get("contraste") or {}).get("fundamento") or "declarado"
    k3["K3b_contrastado"] = fund == "contrastado"
    k3["K3b_fundamento"] = {"contrastado": "contrastado con las líneas que la fase 1 sumó en las filas 8 y 14",
                            "declarado": "según lo declarado: las ubicaciones no se han contrastado con una línea del expediente (no es una comprobación independiente)",
                            "hipótesis": "según la hipótesis D-US1 (no es un dato ni una comprobación independiente)",
                            "hipótesis y declarado": "según la hipótesis D-US1 y lo declarado sin contrastar (no es una comprobación independiente)"}[fund]
    if U["op"] is None or U["fin"] is None:
        k3["K3b_alquiler_contado"], k3["K3b_por_clase"] = "no evaluable (falta declarar si hay arrendamientos operativos y financieros)", None
        G.add("F1-K3b", False, None, None, "no evaluable sin el desglose de US GAAP (lo bloquea F1-US-DESGLOSE)", "K3")
        return
    devuelve = per in ("A1_sin_ROU", "A2_propio", "A3_estimado")
    clases, mal = {}, []
    if U["op"]:
        v = ((1 if f["pagos_op_pos"] else 0) + (1 if f["exceso_c49"] else 0) + (1 if (f["a8_pos"] and not devuelve) else 0)
             + (1 if f["am14_solo_sin"] else 0) - (1 if f["pas14_solo_sin"] else 0))
        clases["operativos"] = nombre.get(v, f"{v} veces")
        if v != 1:
            mal.append(f"operativos {clases['operativos']}")
    if U["fin"] and U["fin_como_deuda"]:
        clases["financieros"] = "como deuda (D-WM)"
        if f["exceso_c49"]:
            mal.append("financieros tratados como deuda (D-WM) con sus pagos restados en C49")
    elif U["fin"]:
        v = (1 if rou_pos else 0) + (1 if c49_pos else 0) - (1 if (rou_pos and devuelve) else 0) + (1 if (f["exceso_c49"] and not U["op"]) else 0)
        esperado = 1 if (rou_pos or c49_pos or (f["fin_m"] is not None and f["fin_m"] > TOL_US_C49)) else 0
        clases["financieros"] = nombre.get(v, f"{v} veces") + ("" if esperado else " (sin importes)")
        if v != esperado:
            mal.append(f"financieros {clases['financieros']}")
    elif f["exceso_c49"] and not U["op"]:
        mal.append("C49 positivo sin arrendamientos de ninguna clase")
    k3["K3b_por_clase"] = clases or None
    k3["K3b_alquiler_contado"] = ("; ".join(f"{k}: {v}" for k, v in clases.items()) if mal else ("una vez" if clases else "ninguna vez (sin arrendamientos)"))
    G.add("F1-K3b", bool(mal), "BLOQUEA", "MODELO NO APLICABLE",
          (f"alquiler mal contado en la proyección con el perímetro {per} ({'; '.join(mal)}): cada clase debe contarse una vez") if mal
          else f"alquiler contado {k3['K3b_alquiler_contado']}" + (f" ({', '.join(clases)})" if clases else "") + f" · {k3['K3b_fundamento']}", "K3")


def _guarda_puente_us(G, L, U, anios, motor):
    """(F1 · US GAAP) Puente de deuda. El motor B proyecta el EBIT, que con US GAAP ya lleva entero el alquiler operativo: su pasivo no es
    deuda del puente (se contaría dos veces). Deuda coherente = deuda financiera (fila 22) + pasivo por arrendamientos financieros (fila 23
    sin el pasivo operativo). El libro resta Historia C64 = fila 22 + fila 23: si la fila 23 lleva pasivo operativo, con el motor B bloquea
    (límite declarado: ningún libro lo excluye) y con el motor A informa (el motor A no resta deuda). (ronda 2) Lo declarado se contrasta con las
    líneas que la fase 1 sumó en la fila 23 del último ejercicio (partida «arrendamientos» de fase1_partes): si una nombra un arrendamiento
    operativo y se declara que la fila 23 no lleva ninguno, con el motor B bloquea (DATOS INVÁLIDOS) y con el motor A avisa."""
    yL, dec = anios[-1], "puente de deuda · US GAAP"
    l22, l23, c64 = Q(L.get("Historia!L22")), Q(L.get("Historia!L23")), Q(L.get("Historia!C64"))
    op23 = Fr(0) if U["op"] is False else (U["S"]["pasivo_arr_operativo"].get(yL) if U["op"] is True else None)
    coh = (l22 + l23 - op23) if None not in (l22, l23, op23) else None
    P = U.get("partes")
    lin23 = [c for c in ((P["usados"].get(yL, {}).get("arrendamientos") or []) if P else []) if c["lados"] and c["es_op"]]
    p = {"ejercicio": yL, "motor": motor, "deuda_financiera_fila_22": fl(l22, 6), "pasivo_por_arrendamientos_fila_23": fl(l23, 6),
         "pasivo_operativo_dentro_de_la_fila_23": fl(op23, 6), "deuda_del_puente_del_libro_C64": fl(c64, 6), "deuda_del_puente_coherente": fl(coh, 6),
         "exceso_que_restaria_el_motor_B": fl(op23, 6),
         "lineas_de_arrendamiento_operativo_sumadas_en_la_fila_23": [f"{c['origen']}: «{c['ver'][:130]}»" for c in lin23] if P else None,
         "regla": "deuda del puente = deuda financiera + pasivo por arrendamientos financieros; el pasivo por arrendamiento operativo no entra: su pago ya está "
                  "entero en el EBIT (una sola vez)"}
    if op23 is not None and op23 <= TOL_E7 and lin23:
        G.add("F1-US-PUENTE", True, "BLOQUEA" if motor == "B" else "AVISO", "DATOS INVÁLIDOS" if motor == "B" else "AVISO",
              f"la declaración contradice al expediente: se declara que la fila 23 no lleva pasivo por arrendamiento operativo en {yL} y la fase 1 sumó en ella una línea "
              f"que lo nombra ({lin23[0]['origen']}: «{lin23[0]['ver'][:130]}»)" + ("" if motor == "B" else " (no afecta al motor A, que no resta deuda)"), dec)
    elif motor == "B" and U["op"] is False and U["fin"] is False and l23 is not None and l23 > TOL_E7:
        G.add("F1-US-PUENTE", True, "BLOQUEA", "DATOS INVÁLIDOS",
              f"la fila 23 del libro lleva {float(l23)} de pasivo por arrendamientos en {yL} y se declara que no hay arrendamientos de ninguna clase", dec)
    elif op23 is None and motor != "B" and U["op"] is True:
        # el motor A no resta deuda: el dato del puente no bloquea su conclusión, pero sin él no se puede decir qué lleva la fila 23
        G.add("F1-US-PUENTE", True, "AVISO", "AVISO", f"sin series.pasivo_arr_operativo de {yL} no se puede comprobar si la fila 23 lleva pasivo por arrendamiento operativo "
              "(no afecta al motor A, que no resta deuda; con el motor B bloquearía: el puente lo restaría además del EBIT)", dec)
    elif op23 is None:
        G.add("F1-US-PUENTE", False, None, None, "no evaluable: falta declarar si hay arrendamientos operativos o su pasivo del último ejercicio (lo bloquea F1-US-DESGLOSE)", dec)
    elif l23 is not None and op23 > l23 + TOL_E7:
        G.add("F1-US-PUENTE", True, "BLOQUEA", "DATOS INVÁLIDOS",
              f"el pasivo por arrendamiento operativo declarado dentro de la fila 23 ({float(op23)}) supera la fila 23 del libro ({float(l23)}) en {yL}", dec)
    elif op23 > TOL_E7 and motor == "B":
        G.add("F1-US-PUENTE", True, "BLOQUEA", "MODELO NO APLICABLE",
              f"LÍMITE DECLARADO · el puente del motor B (Historia C64 = fila 22 + fila 23 = {None if c64 is None else float(c64)}) resta {float(op23)} de pasivo por "
              f"arrendamiento operativo, cuyo pago ya está entero en el EBIT que proyecta el motor B: el alquiler se contaría dos veces. Deuda coherente del puente: "
              f"{None if coh is None else float(coh)}. Ningún libro lo excluye: la salida es que la fila 23 lleve solo el pasivo por arrendamientos financieros "
              "(corrección registrada de las entradas en un expediente nuevo)", dec, clase="modelo")
    elif op23 > TOL_E7:
        G.add("F1-US-PUENTE", True, "INFORMA", "INFORMA",
              f"la fila 23 lleva {float(op23)} de pasivo por arrendamiento operativo. El motor A no resta deuda, así que no afecta a su valor; sí entra en el capital "
              f"invertido y en el ROIC histórico del libro (filas 32–33) y en Historia C64. Deuda coherente de un puente (motor B): {None if coh is None else float(coh)}", dec)
    else:
        G.add("F1-US-PUENTE", False, None, None, "la fila 23 no lleva pasivo por arrendamiento operativo: la deuda del puente es la del libro"
              + ("" if P else " (según lo declarado: sin fase1_partes no se ha contrastado con las líneas de la fila 23)"), dec)
    return p


def _resumen_cota(entradas):
    """(ronda 2, R1-8) La cota en dos cifras para el informe: cuánto podría cambiar el flujo sin crecimiento (mm y %) y el valor presente de los flujos en
    el escenario NORMAL (%). Cada entrada es la variación si UNA de las hipótesis o ubicaciones no fuera cierta; como son independientes, el extremo
    inferior suma las negativas y el superior, las positivas."""
    k_vp = "por_escenario (valor presente de los flujos a la r del libro, sin exceso de caja ni quiebra)"

    def rango(xs):
        xs = [x for x in xs if x is not None]
        return [round(sum(x for x in xs if x < 0), 6), round(sum(x for x in xs if x > 0), 6)] if xs else None

    mm = rango([e.get("variacion_maxima_del_flujo_sin_crecimiento_mm") for e in entradas.values()])
    pf = rango([e.get("variacion_maxima_del_flujo_sin_crecimiento_%") for e in entradas.values()])
    vn = rango([((e.get(k_vp) or {}).get("NORMAL") or {}).get("variacion_maxima_%") for e in entradas.values()])
    if not mm:
        return {"flujo_sin_crecimiento_mm": None, "flujo_sin_crecimiento_%": None, "valor_presente_NORMAL_%": None, "texto": "cota: no calculable (faltan series)"}
    txt = (f"cota: el flujo sin crecimiento podría cambiar entre {mm[0]:+.3f} y {mm[1]:+.3f} mm" + (f" ({pf[0]:+.1f} % y {pf[1]:+.1f} %)" if pf else "")
           + (f"; el valor presente de los flujos en el escenario NORMAL, entre {vn[0]:+.1f} % y {vn[1]:+.1f} %" if vn else ""))
    return {"flujo_sin_crecimiento_mm": mm, "flujo_sin_crecimiento_%": pf, "valor_presente_NORMAL_%": vn, "texto": txt}


def _informes_us(G, res, L, U, f, anios, ventana, col, V0, S_w, decl_r, pal, motor):
    """(F1 · US GAAP) Lo que queda a la vista junto al resultado:
      - D-US2: se cuentan los pagos; la diferencia con el coste lineal (si el coste declarado tiene el mismo perímetro que los pagos: R1-7);
      - D-US2 bis: con los dos tramos dentro de la fila 14 se publica el valor de la hoja (coste contable) y cuánto cambiaría contando los pagos;
      - la CONDICIÓN de la conclusión y su cota: la hipótesis D-US1 (tramos que la empresa no publica), las ubicaciones declaradas que no se han podido
        contrastar con una línea (R1-3) y la hipótesis D-WM (financieros no desglosados, como deuda), con cuánto cambiaría el resultado si no fueran
        ciertas (flujo sin crecimiento y valor presente por escenario) y su resumen para el informe (R1-8);
      - el puente de deuda."""
    S = U["S"]
    P, Lc = S["pagos_arr_operativo"], S["coste_arr_operativo"]
    yL, esc = anios[-1], V0 / S_w
    C = U.get("contraste") or {}
    F0 = decl_r["F0"] if decl_r else None
    r_ = Q(L.get("Análisis!C56"))
    k_vp = "por_escenario (valor presente de los flujos a la r del libro, sin exceso de caja ni quiebra)"
    p_m = media(P[y] for y in ventana) if (U["op"] is True and all(y in P for y in ventana)) else None
    l_m = media(Lc[y] for y in ventana) if (U["op"] is True and all(y in Lc for y in ventana)) else None
    completo = p_m is not None and l_m is not None
    comparable = U["coste_comparable"]

    def efecto(df):
        """Lo que cambiaría el resultado si f cambiara en df: flujo sin crecimiento (mm y %) y valor presente de los flujos por escenario."""
        e = {"variacion_maxima_de_f": fl(df, 9), "variacion_maxima_del_flujo_sin_crecimiento_mm": fl(-df * V0, 6),
             "variacion_maxima_del_flujo_sin_crecimiento_%": fl(-100 * df * V0 / F0, 3) if F0 else None}
        if decl_r and r_ is not None:
            vp = {}
            for n_, v_ in decl_r["esc"].items():
                mo, g_ = v_["_mo"], pal[n_]["g_inf"]
                if r_ <= g_:
                    continue
                k_ = sum(mo["V"][t] / (1 + r_) ** (t + 1) for t in range(10)) + mo["V"][-1] * (1 + g_) / ((r_ - g_) * (1 + r_) ** 10)
                base = sum(mo["flujos"][t] / (1 + r_) ** (t + 1) for t in range(10)) + mo["flujo_11"] / ((r_ - g_) * (1 + r_) ** 10)
                vp[n_] = {"variacion_maxima_del_valor_presente_de_los_flujos_mm": fl(-df * k_, 3),
                          "variacion_maxima_%": fl(-100 * df * k_ / base, 2) if base > 0 else None}
            e[k_vp] = vp or None
        return e

    # ---- D-US2 (y R1-7): pagos frente al coste lineal
    dif = None
    if completo and comparable:
        dif = {"coste_lineal_medio_de_la_ventana": fl(l_m, 6), "pagos_medios_de_la_ventana": fl(p_m, 6), "coste_menos_pagos_medio": fl(l_m - p_m, 6),
               "coste_menos_pagos_a_la_escala_del_año_base": fl((l_m - p_m) * esc, 6),
               "coste_menos_pagos_del_año_base": fl(Lc[yL] - P[yL], 6) if (yL in Lc and yL in P) else None,
               "coste_entre_pagos": fl(l_m / p_m, 4) if p_m else None,
               "nota": "D-US2: se cuentan los pagos. Si se contara el coste lineal, el flujo sin crecimiento cambiaría en −(coste − pagos) a la escala del año base. "
                       "El coste declarado es el de los contratos capitalizados (sin corto plazo ni variable): si la diferencia no es de calendario sino de "
                       "perímetro, se declara «coste_comparable_con_los_pagos»: false"}
    elif completo:
        dif = {"comparable": False, "coste_publicado_medio_de_la_ventana": fl(l_m, 6), "pagos_medios_de_la_ventana": fl(p_m, 6),
               "coste_entre_pagos": fl(l_m / p_m, 4) if p_m else None, "motivo": U["coste_no_comparable_motivo"],
               "nota": "el coste publicado no tiene el mismo perímetro que los pagos (declarado): la diferencia coste − pagos no se calcula"}
    # ---- D-US2 bis: los dos tramos dentro de la fila 14 → valor de la hoja (coste contable) y cuánto cambiaría contando los pagos
    bis = None
    if U["op"] is True and U["dos_en_14"]:
        neto = U["neto_14"]
        bis = {"regla": DECISIONES_US["D-US2 bis"]["regla"], "registro": DECISIONES_US["D-US2 bis"]["registro"],
               "valor_publicado": "el de la hoja, que cuenta el coste contable del arrendamiento operativo (no los pagos)",
               "flujo_sin_crecimiento_de_la_hoja": fl(F0, 6), "dos_lineas_comprobadas": U.get("dos_lineas_comprobadas"), "contando_los_pagos": None}
        if all(y in neto for y in ventana):
            n_m = media(neto[y] for y in ventana)   # lo que llevan dentro de la fila 14 los dos tramos netos: pagos − coste
            ef = efecto(n_m / S_w)                    # contar los pagos sería retirarlo del circulante: f + neto ÷ ventas medias
            bis.update({"neto_dentro_de_la_fila_14_medio_de_la_ventana (pagos − coste)": fl(n_m, 6), "neto_derivado_de_pagos_menos_coste_en": list(U["neto_14_derivado"]),
                        "contando_los_pagos": ef})
            mm, pc = ef["variacion_maxima_del_flujo_sin_crecimiento_mm"], ef["variacion_maxima_del_flujo_sin_crecimiento_%"]
            vn = ((ef.get(k_vp) or {}).get("NORMAL") or {}).get("variacion_maxima_%")
            bis["texto"] = ("D-US2 bis: el alquiler operativo va mezclado en las líneas del circulante; se publica el valor de la hoja, que cuenta el coste contable; "
                            f"contando los pagos, el flujo sin crecimiento cambiaría en {mm:+.3f} mm" + (f" ({pc:+.2f} %)" if pc is not None else "")
                            + (f" y el valor presente de los flujos en el escenario NORMAL en {vn:+.2f} %" if vn is not None else ""))
        else:
            bis["texto"] = ("D-US2 bis: el alquiler operativo va mezclado en las líneas del circulante; se publica el valor de la hoja, que cuenta el coste contable; cuánto "
                            "cambiaría contando los pagos NO se puede calcular (" + ("el coste publicado no es comparable con los pagos y no hay línea neta declarada"
                                                                                     if not comparable else "faltan pagos o coste lineal en la ventana") + ")")
    txt_dif = ((f"; coste lineal medio {float(l_m):.3f}, pagos medios {float(p_m):.3f}: coste − pagos = {float(l_m - p_m):+.3f} de media en la ventana "
                f"({float((l_m - p_m) * esc):+.3f} a la escala del año base)") if (completo and comparable) else
               (f"; el coste publicado ({float(l_m):.3f} de media) no tiene el mismo perímetro que los pagos ({float(p_m):.3f}): la diferencia no se calcula "
                f"({U['coste_no_comparable_motivo']})") if completo else "; coste lineal o pagos sin declarar: la diferencia no se puede mostrar")
    if bis:
        G.add("F1-US-BASE", True, "AVISO", "AVISO", bis["texto"] + txt_dif + f" · registro de la regla: {_REG_US2['fecha']}, {_REG_US2['motivo']}", "D-US2 bis")
    else:
        G.add("F1-US-BASE", U["op"] is True, "INFORMA", "INFORMA",
              ("arrendamientos operativos: la proyección cuenta los PAGOS (D-US2)" + txt_dif) if U["op"] is True else "sin arrendamientos operativos declarados", "D-US2")
    # ---- condiciones de la conclusión y su cota
    conds, entradas = [], {}
    hip = U["hipotesis_D_US1"] if U["op"] is True else []
    holgada = "" if comparable else " (cota holgada: el coste publicado lleva partidas que no están en los pagos)"
    if hip:
        if "variacion_pasivo" in hip and p_m is not None:
            entradas["si la variación del pasivo estuviera sola dentro de la fila 14 (el alquiler se omitiría): como máximo, los pagos"] = efecto(p_m / S_w)
        if "amortizacion_rou" in hip and l_m is not None:
            entradas["si la amortización del derecho de uso estuviera dentro de la fila 8, o sola dentro de la fila 14 (se contaría dos veces): como máximo, "
                     "el coste lineal" + holgada] = efecto(-l_m / S_w)
        conds.append({"id": "D-US1", "tipo": "hipótesis general declarada", "tramos": list(hip),
                      "texto": ("hipótesis D-US1 (no es un dato): la empresa no publica en qué líneas del flujo van "
                                + " ni ".join(_NOMBRE_TRAMO[k] for k in hip) + " del arrendamiento operativo; se supone" + ("n" if len(hip) > 1 else "")
                                + " dentro del flujo de explotación, fuera de las filas 8 y 14"),
                      "regla": DECISIONES_US["D-US1"]["regla"], "registro": DECISIONES_US["D-US1"]["registro"]})
    sc = dict(C.get("sin_contrastar") or {})
    if sc:
        for clave in sc:
            ub = (C["tramos"].get(clave) or {}).get("ubicacion_declarada")
            a8_m = media(U["a8"][y] for y in ventana) if all(y in U["a8"] for y in ventana) else None
            aj_m = media(U["ajuste"][y] for y in ventana) if (U["retira_de_14"] and all(y in U["ajuste"] for y in ventana)) else None
            ff = S["da_rou_financiero_fuera"]
            af_m = media(ff[y] for y in ventana) if all(y in ff for y in ventana) else None
            if clave == "variacion_pasivo" and ub == "fuera_de_las_filas_8_y_14" and p_m is not None:
                entradas["si la variación del pasivo, declarada fuera de las filas 8 y 14 y sin contrastar con una línea, estuviera sola dentro de la fila 14 (el "
                         "alquiler se omitiría): como máximo, los pagos"] = efecto(p_m / S_w)
            elif clave == "amortizacion_rou" and ub == "fuera_de_las_filas_8_y_14" and l_m is not None:
                entradas["si la amortización del derecho de uso, declarada fuera de las filas 8 y 14 y sin contrastar con una línea, estuviera dentro de la fila 8, o "
                         "sola dentro de la fila 14 (se contaría dos veces): como máximo, el coste lineal" + holgada] = efecto(-l_m / S_w)
            elif clave == "amortizacion_rou" and ub == "fila_8" and a8_m is not None:
                entradas["si la amortización del derecho de uso, declarada dentro de la fila 8 y sin contrastar con una línea, no estuviera dentro de la D&A (D_X "
                         "la habría excluido sin llevarla): el importe declarado"] = efecto(a8_m / S_w)
            elif ub == "fila_14" and aj_m is not None:
                if clave in (C.get("importe_sin_contrastar") or []):
                    entradas[f"si {_NOMBRE_TRAMO[clave]} dentro de la fila 14 fuera menor que el importe declarado, que no se ha podido comparar con una cifra "
                             "impresa (se habría retirado de más): como máximo, el importe declarado"] = efecto(-aj_m / S_w)
                else:
                    entradas[f"si {_NOMBRE_TRAMO[clave]}, declarada dentro de la fila 14 y sin contrastar con una línea, no estuviera dentro del circulante (se "
                             "habría retirado sin estar): el importe declarado"] = efecto(-aj_m / S_w)
                # (cierre de la ronda 2, R2-2) el importe tampoco está contrastado con una cifra impresa: si lo que hay dentro de la fila fuera más que lo
                # declarado (un 0, por ejemplo), la parte sin retirar seguiría dentro de la reinversión. Como máximo, los pagos (pasivo) o el coste lineal
                if clave == "variacion_pasivo" and p_m is not None and p_m > aj_m:
                    entradas["si la variación del pasivo dentro de la fila 14 fuera mayor que el importe declarado (la parte sin retirar omitiría el alquiler): "
                             "como máximo, los pagos menos el importe declarado"] = efecto((p_m - aj_m) / S_w)
                elif clave == "amortizacion_rou" and l_m is not None and l_m > -aj_m:
                    entradas["si la amortización del derecho de uso dentro de la fila 14 fuera mayor que el importe declarado (la parte sin retirar se contaría dos "
                             "veces): como máximo, el coste lineal menos el importe declarado" + holgada] = efecto(-(l_m + aj_m) / S_w)
            elif clave == "amortizacion_rou_financiero" and af_m is not None:
                entradas["si la amortización del derecho de uso de los arrendamientos financieros, declarada fuera de la fila 8 y sin contrastar con una línea, "
                         "estuviera dentro de la D&A (se contaría dos veces): el importe publicado"] = efecto(-af_m / S_w)
        conds.append({"id": "F1-US-FILAS", "tipo": "ubicación declarada sin contrastar con una línea del expediente", "tramos": list(sc),
                      "texto": ("ubicación declarada sin contrastar con una línea (no es un dato comprobado): "
                                + "; ".join(f"{_NOMBRE_TRAMO[k]}, {_UB_TXT.get((C['tramos'].get(k) or {}).get('ubicacion_declarada'))}" for k in sc)),
                      "regla": "lo que el programa no puede contrastar con una línea del expediente no da una conclusión sin condición (revisión R1 de F1 con US GAAP, R1-3)",
                      "registro": None, "motivos": sc})
    wm = None
    if U["fin"] is True and U["fin_como_deuda"]:
        cp, gt = S["caja_pagada_arr_financiero"], S["gasto_arr_financiero"]
        wm = {"regla": DECISIONES_US["D-WM"]["regla"], "registro": DECISIONES_US["D-WM"]["registro"], "diferencia_estimada": None}
        if all(y in cp and y in gt for y in ventana):
            d_m = media(cp[y] - gt[y] for y in ventana)
            base = (Q(L.get("Análisis!C46")) - Q(L.get("Análisis!C47"))) if None not in (Q(L.get("Análisis!C46")), Q(L.get("Análisis!C47"))) else None
            ef = efecto(d_m / S_w)   # tratados como arrendamientos (principal en la caja base, amortización fuera de D_X) el flujo sería menor en principal − amortización
            entradas["si los arrendamientos financieros no desglosados se trataran como arrendamientos y no como deuda (D-WM): diferencia estimada = caja pagada − "
                     "gasto total"] = ef
            wm["diferencia_estimada"] = {"caja_pagada_media_de_la_ventana": fl(media(cp[y] for y in ventana), 6),
                                         "gasto_total_medio_de_la_ventana": fl(media(gt[y] for y in ventana), 6),
                                         "caja_pagada_menos_gasto_total_medio_mm": fl(d_m, 6), "a_la_escala_del_año_base_mm": fl(d_m * esc, 6),
                                         "%_de_CFO_menos_capex_medio (Análisis C46 − C47)": fl(100 * d_m / base, 3) if base else None, "efecto": ef,
                                         "nota": "estimación: el flujo sin crecimiento queda por encima del que saldría tratándolos como arrendamientos en (principal − "
                                                 "amortización) = caja pagada − gasto total si las dos cifras llevan el mismo interés; si la caja pagada fuera solo el "
                                                 "principal, la diferencia sería mayor en el interés"}
        conds.append({"id": "D-WM", "tipo": "hipótesis declarada", "tramos": ["financieros"],
                      "texto": ("hipótesis D-WM (no es un dato): la empresa no desglosa sus arrendamientos financieros; se tratan como deuda y activos propios (su "
                                "amortización queda dentro de la propia y sus pagos no se restan de la caja base)"
                                + (f"; diferencia estimada, caja pagada − gasto total: {float(d_m):+.3f} mm al año" if wm["diferencia_estimada"] else "")),
                      "regla": DECISIONES_US["D-WM"]["regla"], "registro": DECISIONES_US["D-WM"]["registro"]})
    cota = None
    if conds:
        cota = {"flujo_sin_crecimiento_con_la_hipotesis": fl(F0, 6), "tramos_con_hipotesis": list(hip)}
        cota.update(entradas)
        cota["nota"] = ("cotas, no estimaciones (salvo la de D-WM): la parte del pago que reduce el pasivo es menor que el pago y la amortización del derecho de uso es "
                        "menor que el coste lineal; si los dos tramos estuvieran netos dentro de la fila 14, la variación sería solo −(pagos − coste lineal)")
        cota["resumen"] = _resumen_cota(entradas)
        reg = next((c["registro"] for c in conds if c.get("registro")), None)
        res["condicionada"] = {"hipotesis": " + ".join(c["id"] for c in conds), "tramos": list(hip), "texto": " · ".join(c["texto"] for c in conds),
                               "regla": conds[0]["regla"], "registro": reg, "condiciones": conds, "cota": cota}
    G.add("F1-US-HIPOTESIS", bool(conds), "AVISO", "AVISO",
          (res["condicionada"]["texto"] + ". CONCLUSIÓN CONDICIONADA. Cota: "
           + "; ".join(f"{k}: flujo sin crecimiento {v['variacion_maxima_del_flujo_sin_crecimiento_mm']:+.3f} mm"
                       + (f" ({v['variacion_maxima_del_flujo_sin_crecimiento_%']:+.1f} %)" if v.get("variacion_maxima_del_flujo_sin_crecimiento_%") is not None else "")
                       for k, v in entradas.items())
           + " · registro de las reglas: " + "; ".join(f"{c['id']}: {c['registro']['fecha']}, {c['registro']['motivo']}" for c in conds if c.get("registro"))) if conds
          else "sin hipótesis ni ubicaciones sin contrastar: los tramos del arrendamiento operativo están contrastados con su línea (o no hay operativos)", "D-US1 · D-WM · R1-3")
    puente = _guarda_puente_us(G, L, U, anios, motor)
    aj = U["ajuste"]
    res["us_gaap"] = {
        "decisiones": DECISIONES_US,
        "base_del_arrendamiento_operativo": "coste contable: el valor de la hoja (D-US2 bis)" if bis else "pagos (D-US2)",
        "operativos": {"existen": U["op"], "ubicacion_de_la_amortizacion_del_derecho_de_uso": U["ub_am"], "ubicacion_de_la_variacion_del_pasivo": U["ub_pas"],
                       "hipotesis_D_US1_en": list(U["hipotesis_D_US1"]), "pagos_medios_de_la_ventana": fl(p_m, 6), "coste_lineal_medio_de_la_ventana": fl(l_m, 6),
                       "coste_comparable_con_los_pagos": comparable,
                       "amortizacion_dentro_de_la_fila_8_media": fl(media(U["a8"][y] for y in ventana), 6) if all(y in U["a8"] for y in ventana) else None,
                       "tramos_dentro_de_la_fila_14": list(U["tramos_en_fila_14"]),
                       "retirado_del_circulante_medio": fl(media(aj[y] for y in ventana), 6) if (U["retira_de_14"] and all(y in aj for y in ventana)) else None},
        "financieros": {"existen": U["fin"], "tratados_como_deuda_D_WM": U["fin_como_deuda"], "ubicacion_de_la_amortizacion_del_derecho_de_uso": None if U["fin_como_deuda"] else U["fin_am_ub"],
                        "principal_publicado_medio_de_la_ventana": fl(f["fin_m"], 6),
                        "amortizacion_dentro_de_la_fila_8_media": fl(media(U["rou_fin"][y] for y in ventana), 6) if all(y in U["rou_fin"] for y in ventana) else None},
        "diferencia_coste_lineal_menos_pagos": dif, "D_US2_bis": bis, "D_WM": wm, "cota_D_US1": cota,
        "contraste_de_ubicaciones": {"tramos": C.get("tramos"), "fundamento": C.get("fundamento"), "fase1_partes": C.get("fase1_partes"),
                                     "sin_contrastar": C.get("sin_contrastar"), "importe_sin_contrastar": C.get("importe_sin_contrastar") or [],
                                     "lineas_ajenas_al_tramo": C.get("lineas_ajenas") or []},
        "puente_de_deuda": puente}


def _evaluar_puente_motor_b(L, decl, res, G, desconocidas, carpeta):
    """(F1 · US GAAP) Con el motor B, F1 solo evalúa el puente de deuda: norma (valor cerrado), existencia de arrendamientos por clase y pasivo
    por arrendamiento operativo dentro de la fila 23 (F1-US-PUENTE). Los perímetros de la reinversión son del motor A y no se evalúan.
    (ronda 2, R1-1) También se llega aquí con la norma SIN DETERMINAR en un expediente de la 4.15 (libro sin norma o con un valor fuera de la lista
    cerrada): no se puede descartar US GAAP y F1-NORMA bloquea. (R1-9) Lo que F1 no mira con el motor B se avisa: el ancla de S2C y el ROIC."""
    res.update({"aplica": True, "alcance": "puente de deuda del motor B con US GAAP (F1-US-PUENTE): los perímetros de la reinversión son del motor A y no se evalúan"})
    if desconocidas:
        G.add("F1-DECLARACION", True, "BLOQUEA", "DATOS INVÁLIDOS", f"claves no reconocidas en la declaración: {', '.join(desconocidas)} (no se ignoran en silencio)", "—")
    anios_raw = _hist(L, 5)
    if not all(isinstance(a, (int, float)) for a in anios_raw):
        raise ErrorDeclaracion("Historia C5:L5 no tiene los diez años")
    anios = [int(a) for a in anios_raw]
    norma = _guarda_norma(G, L, decl)
    if norma != "US_GAAP" and norma_del_libro(L) != "US_GAAP":
        res["alcance"] = ("norma contable sin determinar con el motor B (F1-NORMA): no se puede descartar US GAAP, donde el pasivo por arrendamiento operativo no es "
                          "deuda del puente; sin la norma no hay conclusión")
        res["K3"] = {"K3b_alquiler_contado": "no evaluable (norma contable sin determinar)"}
        return _cerrar(res, G, "B")
    U = leer_us(decl, anios)
    yL, pasv = anios[-1], U["S"]["pasivo_arr_operativo"]
    # del desglose, lo que usa el puente: registro, existencia por clase y el pasivo operativo (las ubicaciones de los tramos y las series de la
    # reinversión son del motor A)
    faltas = [x for x in U["faltas"] if ".amortizacion_rou" not in x and ".variacion_pasivo" not in x and "coste_comparable" not in x]
    if U["op"] is True and yL not in pasv:
        faltas.append(f"series.pasivo_arr_operativo sin declarar en {yL} (pasivo por arrendamiento operativo dentro de la fila 23)")
    incoh = [x for x in U["incoherencias"] if "pasivo_arr_operativo" in x or "existen" in x]
    G.add("F1-US-DESGLOSE", bool(faltas or incoh), "BLOQUEA", "DATOS INVÁLIDOS" if incoh else "INCOMPLETO",
          ("; ".join(incoh + faltas))[:1500] if (faltas or incoh) else "arrendamientos operativos y financieros declarados por separado", "US GAAP · ASC 842")
    U["evidencias"] = [e for e in U["evidencias"] if ".amortizacion_rou" not in e[0] and ".variacion_pasivo" not in e[0]]
    U["ausencias"] = []
    _contraste_us(G, decl, carpeta, U, anios[-5:], False, solo_existencia=True)
    puente = _guarda_puente_us(G, L, U, anios, "B")
    if U["op"] is not False:
        # (R1-9) lo que F1 no mira con el motor B: el ancla de S2C y el ROIC histórico pueden arrastrar partidas del arrendamiento operativo
        P = U.get("partes")
        lin = sorted({f"fila {'8' if k == 'da' else '14'}: «{c['ver'][:130]}»" for a in anios[-5:] for k in ("da", "circulante_lineas")
                      for c in (((P or {}).get("usados") or {}).get(a, {}).get(k) or []) if c["lados"] and not c["solo_fin"]})
        c53 = Q(L.get("Historia!C53"))
        G.add("F1-US-ANCLA", True, "AVISO", "AVISO",
              "con el motor B, F1 solo evalúa el puente de deuda: no examina en qué líneas del estado de flujos están la amortización del derecho de uso y la "
              "variación del pasivo del arrendamiento operativo. Si la D&A (fila 8) o el circulante (fila 14) las llevan, el ancla de S2C (Historia C53 = "
              f"{'vacía' if c53 is None else round(float(c53), 6)}) y el ROIC histórico del libro (filas 32–33), que son la referencia de la fase B, las arrastran"
              + (f". Líneas sumadas que nombran el arrendamiento en los cinco años del ancla: {'; '.join(lin[:4])}" if lin else
                 ". Ninguna línea sumada en las filas 8 y 14 de los cinco años del ancla nombra el arrendamiento" if P else ". Sin fase1_partes no se han examinado las líneas"),
              "motor B · ancla de S2C y ROIC (lo que F1 no evalúa)")
    doble = any(g["id"] == "F1-US-PUENTE" and g["salta"] and g["severidad"] == "BLOQUEA" and g["efecto"] == "MODELO NO APLICABLE" for g in G.lista)
    res["K3"] = {"K3b_alquiler_contado": ("operativos: dos veces (en el EBIT y en la deuda del puente)" if doble else
                                          "no evaluable" if (U["op"] is None or (U["op"] and yL not in pasv)) else "una vez" if U["op"] else "ninguna vez (sin arrendamientos operativos)"),
                 "K3b_fundamento": "según lo declarado (el pasivo por arrendamiento operativo dentro de la fila 23)" + (
                     "" if not U.get("partes") else ", contrastado con las líneas que la fase 1 sumó en la fila 23")}
    res["us_gaap"] = {"decisiones": DECISIONES_US, "operativos": {"existen": U["op"]}, "financieros": {"existen": U["fin"]}, "puente_de_deuda": puente}
    _guarda_fuentes_series(G, decl, carpeta, anios, res, us=U, series=("pasivo_arr_operativo",))
    return _cerrar(res, G, "B")


def _terminos_incompletos(nombre, d, horiz, con_proporcion=False, anios_futuros=11):
    """(revisión F1-IMPL, H10) Términos explícitos: vacío no es cero. Con importes por año, los de los años 1–10 y el del 11 (o la proporción de
    las ventas, que vale para todos); si el ancla de S2C los excluye, los importes históricos de los cinco años H–L (X^v). Devuelve problemas."""
    out = []
    prop = Q(d.get("proporcion_ventas")) if con_proporcion else None
    if con_proporcion and d.get("proporcion_ventas") is not None and (prop is None or prop < 0):
        out.append(f"{nombre}: proporción de las ventas no numérica o negativa ({d.get('proporcion_ventas')!r})")
    if prop is None and anios_futuros:
        imps = d.get("importes") if isinstance(d.get("importes"), dict) else {}
        falta = [t for t in range(1, anios_futuros + 1) if Q(imps.get(str(t))) is None]
        if falta:
            out.append(f"{nombre}: importes ausentes o no numéricos en los años {falta} (1–10 y 11 obligatorios; vacío no es cero)")
    if d.get("ancla_s2c_excluye_terminos") is True and prop is None:
        hist = d.get("importes_historicos") if isinstance(d.get("importes_historicos"), dict) else {}
        falta = [y for y in horiz if Q(hist.get(str(y))) is None]
        if falta:
            out.append(f"{nombre}: el ancla de S2C los excluye, pero faltan los importes históricos de {falta} (X^v de E4; 0 explícito si no los hubo)")
    return out


def _literal_valores(lit):
    """(H12) Valores con signo que admite una cifra publicada tal como se lee («(149,5)», «-12.3», «1.234,5», «—» = 0)."""
    t = str(lit or "").strip().replace("\u00a0", "").replace(" ", "")
    if t in ("-", "—", "–"):
        return {Fr(0)}
    neg = (t.startswith("(") and t.endswith(")")) or t[:1] in ("-", "−", "–")
    t = t.strip("()").lstrip("-−–")
    if not t or not re.fullmatch(r"[\d.,]+", t):
        return set()
    cands = set()
    for dec in (",", "."):
        mil = "." if dec == "," else ","
        if t.count(dec) > 1:
            continue
        ent = t.split(dec)[0]
        if mil in ent and not re.fullmatch(r"\d{1,3}(" + re.escape(mil) + r"\d{3})+", ent):
            continue
        if dec in t and mil in t.split(dec)[1]:
            continue
        try:
            cands.add(Fr(t.replace(mil, "").replace(dec, ".")))
        except ValueError:
            pass
    return {-x if neg else x for x in cands}


_TOK = re.compile(r"(?<![\w.,/])\(?[-−–]?\d[\d.,]*\)?(?![\w.,/])")
_ANIO = re.compile(r"(?<!\d)((?:19|20)\d\d)(?!\d)")


def _sin_esp(x):
    return re.sub(r"\s+", "", str(x or ""))


def _norm_fila(x):
    return re.sub(r"\s+", " ", str(x or "")).strip().lower()


def _cifra_en_columna(pagina, fila, anio, literal, tol=4):
    """(revisión V6.3.1, V631-2) Localiza la cifra en la página: («ok», detalle) si está, como cifra completa (no como parte de otra), en la
    única línea de la página que contiene la fila declarada y en la columna cuyo encabezado de ejercicio (alineado por posición en el texto
    con marcas de página, «pdftotext -layout») es el año declarado; («invalida», …) si la fila no la contiene o está en la columna de otro
    ejercicio; («pendiente», …) si la fila no se identifica en una sola línea o no hay encabezado alineado (la columna no se puede comprobar)."""
    lineas = [x.expandtabs(8) for x in str(pagina).splitlines()]
    cand = [i for i, x in enumerate(lineas) if _norm_fila(fila) and _norm_fila(fila) in _norm_fila(x)]
    if len(cand) != 1:
        return "pendiente", f"la fila {fila!r} está en {len(cand)} líneas de la página (hace falta una)"
    i = cand[0]
    toks = [m for m in _TOK.finditer(lineas[i]) if _sin_esp(m.group(0)) == _sin_esp(literal)]
    if not toks:
        return "invalida", f"la fila {fila!r} no contiene la cifra {literal!r} como cifra completa"
    anios_col = set()
    for m in toks:
        r = m.end() - (1 if m.group(0).endswith(")") else 0)
        for k in range(i - 1, max(-1, i - 80), -1):
            al = [y.group(1) for y in _ANIO.finditer(lineas[k]) if abs(y.end() - r) <= tol]
            if al:
                anios_col.add(al[0])
                break
    if not anios_col:
        return "pendiente", f"sin encabezado de ejercicio alineado con {literal!r} en la fila {fila!r}"
    if anios_col == {str(anio)}:
        return "ok", f"{literal} en la columna {anio} de la fila {fila!r}"
    return "invalida", f"la cifra {literal!r} de la fila {fila!r} está en la columna de {sorted(anios_col)}, no en la de {anio}"


# (F1-SERIES-ESCALA) Escala de la cifra impresa y ceros sin cifra en las series F1. El modelo trabaja en millones (la misma tabla que
# fase1_historia.ESCALA): «valor_fuente» es la cifra con su signo publicado en la escala del modelo y «escala» dice en qué escala está
# impresa la cifra de «literal»; sin «escala», la del modelo (el comportamiento anterior). La comparación sigue siendo exacta.
ESCALAS_SERIE = {"unidades": Fr(1, 10 ** 6), "miles": Fr(1, 10 ** 3), "millones": Fr(1)}
CEROS_IMPRESOS = ("—", "–", "-", "nil")   # un cero publicado sin dígitos, en la fila y la columna de su ejercicio
CITA_CERO_PALABRAS = 8                    # una cita más corta es un fragmento (un encabezado, una etiqueta): no prueba una inexistencia


def _escala_serie(e):
    """Factor de la escala declarada en un elemento de serie hacia la del modelo (millones); None si «escala» no es uno de los tres valores."""
    x = e.get("escala", "millones")
    return ESCALAS_SERIE.get(x) if isinstance(x, str) else None


def _clase_cero(e):
    """«comprobado» (cero sin cifra impresa, probado por una frase: «cero_comprobado» {motivo, cita}), «impreso» (cero publicado como «—»,
    «–», «-» o «nil» en «literal») o None (una cifra con dígitos: el camino de siempre)."""
    if "cero_comprobado" in e:
        return "comprobado"
    lit = e.get("literal")
    return "impreso" if isinstance(lit, str) and lit.strip() in CEROS_IMPRESOS else None


# (revisión de f1/series-escala, hallazgo B) marcas de escala de una página (lista cerrada, en minúsculas y con los espacios reducidos).
# Solo encabezados, no importes de la prosa: «EUR 15 million» no es una marca (hay una cifra en medio).
_MON = r"(?:eur|euros?|usd|us\$|gbp|chf|sek|dkk|nok)"
MARCAS_ESCALA = {
    "millones": [r"\bin millions?\b", r"\bmillions? of (?:u\.?s\.? )?(?:euros?|eur|dollars|usd|pounds|francs)\b", r"\(\s*millions?\s*\)", r"\b" + _MON + r"\s?(?:m|mn|million|millions)\b",
                 r"[€$£]\s?(?:m|mn|million|millions)\b", r"(?<!\w)(?:m€|meur|mio\.? ?(?:eur|€))(?!\w)", r"\ben millones\b", r"\(\s*millones de\b"],
    "miles": [r"\bin thousands?\b", r"\bthousands? of (?:u\.?s\.? )?(?:euros?|eur|dollars|usd|pounds|francs)\b", r"\(\s*'?000\s*\)", r"[€$£]\s?'?000\b", r"\b" + _MON + r"\s?'?000\b",
              r"\b" + _MON + r"\s?(?:k|thousand|thousands)\b", r"[€$£]\s?(?:k|thousand|thousands)\b", r"(?<!\w)(?:k€|keur|teur|t€)(?!\w)",
              r"\ben miles\b", r"\(\s*miles de\b"],
    "unidades": [r"\b(?:amounts|figures|expressed)\s+in\s+(?:euros?|eur|u\.?s\.? dollars|dollars|usd)\b(?!\s?\(?\s?(?:m\b|mn\b|millions?|thousands?|'?000|k\b))",
                 r"\(\s*(?:in\s+)?(?:euros?|eur|€|usd|\$)\s*\)", r"\b(?:importes |cifras )?(?:expresad[oa]s )?en euros\b(?! ?(?:miles|millones))"],
}


def _escala_de_pagina(pagina):
    """Escalas que declara la página por sus encabezados («(in millions)», «(amounts in Euro)», «in thousands of euros», «€000»…)."""
    t = re.sub(r"\s+", " ", str(pagina)).lower()
    return {esc for esc, pats in MARCAS_ESCALA.items() if any(re.search(p, t) for p in pats)}


def _escala_de_tabla(pagina, literal, fila=None):
    """(ronda 2, límite 1) Escalas que declara el bloque de la tabla de la cifra, no toda la página: desde la línea de la cifra (la que
    contiene también la «fila», si la hay; la primera, si hay varias) hacia arriba hasta dos líneas en blanco seguidas o el principio de
    la página. Lo que va debajo de la fila (otra tabla, otra nota) no cuenta. Si el encabezado de la tabla quedó en la página anterior
    (página de continuación), el bloque no tiene marca y la escala queda PENDIENTE."""
    lineas = str(pagina).splitlines()
    cifra = [i for i, ln in enumerate(lineas) if any(_sin_esp(m.group(0)) == _sin_esp(literal) for m in _TOK.finditer(ln))]
    con_fila = [i for i in cifra if fila and _norm_fila(fila) and _norm_fila(fila) in _norm_fila(lineas[i])]
    i = (con_fila or cifra or [len(lineas) - 1])[0]
    j = i
    while j > 1 and not (lineas[j - 1].strip() == "" and lineas[j - 2].strip() == ""):
        j -= 1
    if j == 1 and lineas[0].strip():
        j = 0
    return _escala_de_pagina("\n".join(lineas[j:i + 1]))


def _aviso_cero_comprobado(G, et, e):
    """(revisión de f1/series-escala, punto 3) Un cero comprobado por una frase no bloquea F1-SERIES, pero tampoco está comprobado: queda
    como aviso propio, F1-SERIES-CERO (PENDIENTE de revisor), con su motivo y su cita, en la guarda, en motor_a_f1_resultado.md (tabla de
    guardas) y en los avisos del bloque motor_a_f1 de la ficha. Un aviso por evaluación; cada año se añade a su detalle."""
    cc = e.get("cero_comprobado") or {}
    linea = (f"{et}: motivo «{str(cc.get('motivo')).strip()[:300]}»; cita (p. {e.get('pagina')} de {e.get('documento')!r}) "
             f"«{str(cc.get('cita')).strip()[:200]}»")
    g = next((x for x in G.lista if x["id"] == "F1-SERIES-CERO"), None)
    if g is None:
        G.add("F1-SERIES-CERO", True, "AVISO", "PENDIENTE",
              "CERO SIN CIFRA IMPRESA, PENDIENTE DE REVISOR (no comprobado: el programa solo ha visto que la frase está en la página; no "
              "bloquea F1-SERIES y la aptitud por entradas sigue en «no»): " + linea, "(1a) · F1-SERIES-ESCALA")
    else:
        g["detalle"] += " · " + linea


def _cero_en_pagina(pagina, e, anio):
    """(F1-SERIES-ESCALA; revisión de f1/usgaap, R1-2) Comprueba un cero en la página citada. Devuelve («ok» | «pendiente» | «invalida» |
    «incompleta», detalle):
      - cero impreso: la marca de «literal», aislada (no pegada a una cifra ni a una palabra), en la única línea de la página que contiene
        la «fila» declarada, después de su etiqueta, y en la columna del ejercicio (alineada con su encabezado, como _cifra_en_columna). Sin
        «fila» → incompleta (un guion suelto en una página no prueba nada); fila sin la marca, o la marca solo en columnas de otros
        ejercicios → invalida; sin encabezado alineado → pendiente (no bloquea F1; la aptitud por entradas sigue en «no»);
      - cero comprobado: «motivo» y «cita» literal (espacios y mayúsculas aparte) en la página, de al menos CITA_CERO_PALABRAS palabras y
        sin importes. El programa comprueba que la frase está en la página, no que pruebe la inexistencia: queda siempre «pendiente» (la
        confirma un revisor; no bloquea F1 y la aptitud por entradas sigue en «no»)."""
    import verificacion_entradas as VE
    if _clase_cero(e) == "comprobado":
        cc = e.get("cero_comprobado")
        if not isinstance(cc, dict):
            return "invalida", "«cero_comprobado» se declara {motivo, cita}"
        if not str(cc.get("motivo") or "").strip() or not str(cc.get("cita") or "").strip():
            return "incompleta", "«cero_comprobado» sin «motivo» o sin «cita» literal que pruebe la inexistencia"
        cita = VE._norm_txt(cc["cita"])
        if len(cita.split()) < CITA_CERO_PALABRAS:
            return "invalida", f"la cita del cero tiene menos de {CITA_CERO_PALABRAS} palabras: un fragmento no prueba la inexistencia"
        importes = [s for s in (m.group(0).rstrip(".,") for m in _TOK.finditer(cita)) if not re.fullmatch(r"\(?(?:19|20)\d\d\)?", s)
                    and (re.search(r"\d[.,]\d", s) or (s.startswith("(") and s.endswith(")"))) and any(v != 0 for v in _literal_valores(s))]
        if importes:
            return "invalida", (f"la cita del cero contiene importes ({', '.join(importes[:3])}): una cifra no prueba una inexistencia "
                                f"(un cero impreso se declara en «literal»)")
        if cita not in VE._norm_txt(pagina):
            return "invalida", f"la cita del cero no está en la página {e.get('pagina')}"
        return "pendiente", ("cero comprobado por una frase de la página: el programa comprueba la cita, no que pruebe la inexistencia; "
                             "la confirma un revisor (la aptitud por entradas sigue en «no»)")
    lit, fila = e["literal"].strip(), str(e.get("fila") or "").strip()
    if not fila:
        return "incompleta", f"cero impreso {lit!r} sin «fila»: una marca sin dígitos solo prueba un cero en su fila y su columna"
    lineas = [x.expandtabs(8) for x in str(pagina).splitlines()]
    cand = [i for i, x in enumerate(lineas) if _norm_fila(fila) in _norm_fila(x)]
    if len(cand) != 1:
        return "incompleta", f"la fila {fila!r} está en {len(cand)} líneas de la página (hace falta una): el cero impreso {lit!r} no se puede situar"
    i = cand[0]
    m = re.search(r"\s+".join(map(re.escape, fila.split())), lineas[i], re.I)
    # (revisión de f1/series-escala, hallazgo A) una marca es una celda: se descarta si a su derecha quedan letras (es parte de la etiqueta:
    # «Finance lease - principal», «Financing cash flows – finance leases») o si la sigue, con un espacio como mucho, una cifra o un
    # paréntesis (es el signo de un negativo: «- 7»). Otra marca «nil» a la derecha no cuenta como letras.
    marcas = [mk for mk in re.compile(r"(?<!\S)" + re.escape(lit) + r"(?!\S)").finditer(lineas[i], m.end() if m else 0)
              if not re.search(r"[^\W\d_]", re.sub(r"(?<!\S)nil(?!\S)", "", lineas[i][mk.end():], flags=re.I))
              and not re.match(r" ?[\d(]", lineas[i][mk.end():])]
    if not marcas:
        return "invalida", f"la fila {fila!r} no contiene el cero impreso {lit!r} como marca aislada después de su etiqueta"
    alineados = []
    for mk in marcas:
        al = None
        for k in range(i - 1, max(-1, i - 80), -1):
            ys = [y.group(1) for y in _ANIO.finditer(lineas[k]) if abs(y.end() - mk.end()) <= 4]
            if ys:
                al = ys[0]
                break
        alineados.append(al)
    if str(anio) in alineados:
        return "ok", f"cero impreso {lit} en la columna {anio} de la fila {fila!r}"
    if None in alineados:
        return "pendiente", f"sin encabezado de ejercicio alineado con el cero impreso {lit!r} en la fila {fila!r}"
    return "invalida", f"el cero impreso {lit!r} de la fila {fila!r} está en la columna de {sorted(set(alineados))}, no en la de {anio}"


def _fuente_del_expediente(carpeta, archivo):
    """Ruta real de un archivo DENTRO de la carpeta del expediente (no del paquete ni de otro expediente); None si no lo está o no existe."""
    if not carpeta or not archivo or os.path.isabs(str(archivo)):
        return None
    b = os.path.realpath(carpeta)
    p = os.path.realpath(os.path.join(carpeta, str(archivo)))
    return p if p.startswith(b + os.sep) and os.path.isfile(p) else None


def _fuera_del_expediente(carpeta, archivo):
    """True si «archivo» es absoluto o sale de la carpeta del expediente (p. ej. «../otro/texto.txt»)."""
    if not archivo:
        return False
    if os.path.isabs(str(archivo)):
        return True
    b = os.path.realpath(carpeta)
    return not os.path.realpath(os.path.join(carpeta, str(archivo))).startswith(b + os.sep)


def _guarda_fuentes_series(G, decl, carpeta, anios, res=None, us=None, series=None):
    """(revisión F1-IMPL, H12; revisión V6.3.1, V631-2) Las series que entran en D_X (D&A de derechos de uso y PPA). Por año se exige:
      - «literal»: la cifra tal como se publica, con su signo; «valor_fuente» tiene que ser esa cifra (R415-SIGNO, T9);
      - «documento» registrado en «fuentes_series» con su «archivo» (dentro de la carpeta del expediente) y su «sha256» vigente; un PDF, con
        «archivo_texto» y «sha256_texto»; «archivo» en la entrada, si lo hay, el mismo (la fuente queda ligada al documento);
      - la página citada existe y contiene la cifra como cifra completa (no como parte de otra: «149.5» no vale en «(1149.57)»);
      - (F1-SERIES-ESCALA) «escala» opcional de la cifra impresa («unidades», «miles» o «millones»; sin ella, la del modelo, en millones):
        «valor_fuente» (en la escala del modelo) tiene que ser exactamente la cifra de «literal» convertida (Jumbo publica en euros:
        «(9.199.774)» con escala «unidades» es −9,199774); otro valor de «escala» → DATOS INVÁLIDOS. Un cero publicado sin dígitos
        («—», «–», «-», «nil» en «literal», «valor_fuente» 0) se busca como marca aislada en su «fila» y en la columna del ejercicio; un cero
        sin cifra impresa se declara «cero_comprobado» {motivo, cita}, sin «literal» y con «valor_fuente» 0: la cita literal tiene que estar
        en la página citada (al menos 8 palabras, sin importes) y queda PENDIENTE de revisor, como una columna (_cero_en_pagina), con su
        aviso propio F1-SERIES-CERO. (Ronda 2) La escala declarada se contrasta con los encabezados de la página (_escala_de_pagina): otra
        escala → DATOS INVÁLIDOS; sin encabezado reconocible → PENDIENTE;
      - «fila» (la etiqueta de la fila en la página): la cifra está en esa fila y en la columna del ejercicio del año. Si la fila o la columna
        no se pueden identificar, la columna queda PENDIENTE (no bloquea F1; la aptitud por entradas sigue en «no» porque las filas 85–87 del
        libro entran en el universo de verificacion_entradas.py y exigen su comprobación por un revisor).
    Vacío o no examinable → INCOMPLETO; cifra, signo, página, columna o huella distintos, o fuente fuera del expediente → DATOS INVÁLIDOS.
    No acredita la entrada (sin revisor ni sello). BLOQUEA si nada más bloquea; si otra guarda ya bloquea, AVISA (no cambia el estado).
    (F1 · US GAAP) us = leer_us(…): se examinan además las series propias de US GAAP (SERIES_US) y las clasificaciones: cada cita literal
    tiene que estar en la página citada de una fuente registrada con su huella; un tramo «no_publicada» (hipótesis D-US1) cita la página del
    estado de flujos examinada, que tiene que existir y no mostrar una línea propia del arrendamiento operativo (si la muestra, manda el dato)."""
    import verificacion_entradas as VE
    inval, incomp, col_pend, col_ok = [], [], [], 0
    fs = decl.get("fuentes_series") if isinstance(decl.get("fuentes_series"), dict) else {}
    textos = {}

    def texto(doc):
        if doc in textos:
            return textos[doc]
        f = fs.get(doc) if isinstance(fs.get(doc), dict) else None
        out = None
        if f is None:
            out = ("incompleto", f"documento {doc!r} sin fuente registrada en «fuentes_series» (archivo y sha256)")
        elif carpeta is None:
            out = ("incompleto", "fuente no examinada (la evaluación no recibió la carpeta del expediente)")
        else:
            ruta = _fuente_del_expediente(carpeta, f.get("archivo"))
            if ruta is None:
                fuera = _fuera_del_expediente(carpeta, f.get("archivo"))
                out = ("invalido" if fuera else "incompleto",
                       f"la fuente {f.get('archivo')!r} de {doc!r} " + ("está fuera de la carpeta del expediente" if fuera else "no existe en el expediente"))
            elif not str(f.get("sha256") or "").strip():
                out = ("incompleto", f"la fuente {f.get('archivo')!r} de {doc!r} sin «sha256»")
            elif VE._sha(ruta) != str(f["sha256"]).strip().lower():
                out = ("invalido", f"la fuente {f.get('archivo')!r} de {doc!r} cambió (sha256 distinto del declarado)")
            else:
                rt = ruta
                if not ruta.lower().endswith(".txt"):
                    rt = _fuente_del_expediente(carpeta, f.get("archivo_texto"))
                    if rt is None or not str(f.get("sha256_texto") or "").strip():
                        out = ("incompleto", f"{doc!r}: la fuente no es un texto con marcas de página y su «archivo_texto» (con «sha256_texto») no está en el expediente")
                    elif VE._sha(rt) != str(f["sha256_texto"]).strip().lower():
                        out = ("invalido", f"{doc!r}: el texto de la fuente cambió (sha256_texto distinto del declarado)")
                if out is None:
                    out = ("ok", rt)
        textos[doc] = out
        return out

    for nombre in (series if series is not None else ("da_rou", "da_ppa") + (SERIES_US if us is not None else ())):
        s = ((decl.get("series") or {}).get(nombre)) or {}
        if not isinstance(s, dict):
            continue
        for k, e in sorted(s.items()):
            if not isinstance(e, dict):
                continue
            et = f"series.{nombre}.{k}"
            cero = _clase_cero(e)   # (F1-SERIES-ESCALA) None: cifra con dígitos · «impreso»: «—», «–», «-», «nil» · «comprobado»: sin cifra
            vals = {Fr(0)} if cero else _literal_valores(e.get("literal"))
            vf = Q(e.get("valor_fuente"))
            esc = _escala_serie(e)
            if esc is None:
                inval.append(f"{et}: escala {e.get('escala')!r} no válida (se declara «unidades», «miles» o «millones»)")
                continue
            if cero == "comprobado" and e.get("literal") not in (None, ""):
                inval.append(f"{et}: «cero_comprobado» con «literal» {e.get('literal')!r}: un cero sin cifra impresa no lleva cifra")
                continue
            if e.get("literal") in (None, "") and cero is None:
                incomp.append(f"{et}: sin «literal» (la cifra tal como se publica, con su signo)")
                continue
            if not vals:
                inval.append(f"{et}: «literal» {e.get('literal')!r} no es una cifra")
                continue
            if vf not in {v * esc for v in vals}:
                inval.append(f"{et}: «valor_fuente» {e.get('valor_fuente')!r} no es la cifra publicada {e.get('literal')!r} con su signo"
                             + (f" en la escala del modelo (impresa en {e['escala']})" if "escala" in e else "")
                             + (" (un cero tiene «valor_fuente» 0)" if cero else "") + " (R415-SIGNO, T9)")
            doc = str(e.get("documento") or "")
            f = fs.get(doc) if isinstance(fs.get(doc), dict) else {}
            if e.get("archivo") and f and os.path.normpath(str(e["archivo"])) != os.path.normpath(str(f.get("archivo"))):
                inval.append(f"{et}: «archivo» {e.get('archivo')!r} no es la fuente registrada de {doc!r} ({f.get('archivo')!r})")
                continue
            est_t, rt = texto(doc)
            if est_t != "ok":
                (inval if est_t == "invalido" else incomp).append(f"{et}: {rt}")
                continue
            est, pag = VE._pagina_examinable(rt, e.get("pagina"))
            if est == "discrepancia":
                inval.append(f"{et}: {pag}")
                continue
            if est != "ok":
                incomp.append(f"{et}: {pag}")
                continue
            if cero:   # (F1-SERIES-ESCALA) un cero sin dígitos: su marca en la fila y la columna, o la frase que prueba la inexistencia
                est_c, det = _cero_en_pagina(pag, e, k)
                {"invalida": inval, "incompleta": incomp, "pendiente": col_pend}.get(est_c, []).append(f"{et}: {det}")
                if est_c == "ok":
                    col_ok += 1
                elif est_c == "pendiente" and cero == "comprobado":   # (revisión, punto 3) visible como aviso propio: no está comprobado
                    _aviso_cero_comprobado(G, et, e)
                continue
            if not any(_sin_esp(m.group(0)) == _sin_esp(e["literal"]) for ln in pag.splitlines() for m in _TOK.finditer(ln)):
                inval.append(f"{et}: la cifra {e['literal']!r} no está, como cifra completa, en la página {e.get('pagina')} de {doc!r}")
                continue
            if "escala" in e:   # (revisión de f1/series-escala, hallazgo B; ronda 2, límite 1) la escala, contra el bloque de su tabla
                hay = _escala_de_tabla(pag, e["literal"], e.get("fila"))
                if hay and e["escala"] not in hay:
                    inval.append(f"{et}: escala declarada «{e['escala']}», pero la tabla de la cifra (página {e.get('pagina')} de {doc!r}) "
                                 f"declara {sorted(hay)}")
                    continue
                if hay != {e["escala"]}:
                    col_pend.append(f"{et}: escala «{e['escala']}» declarada y NO comprobada: la tabla de la cifra (página {e.get('pagina')}) "
                                    + ("declara varias escalas " + str(sorted(hay)) if hay else "no tiene encabezado de escala reconocible"))
                    # (ronda 2, detalle menor) con la escala pendiente el año no cuenta como columna comprobada; la columna se sigue
                    # examinando (una cifra de otro ejercicio sigue siendo DATOS INVÁLIDOS)
                    try:
                        anio_e = int(k)
                    except ValueError:
                        inval.append(f"{et}: año no válido")
                        continue
                    if not str(e.get("fila") or "").strip():
                        col_pend.append(f"{et}: sin «fila» (etiqueta de la fila): columna y ejercicio sin comprobar")
                        continue
                    est_e, det_e = _cifra_en_columna(pag, e["fila"], anio_e, e["literal"])
                    if est_e == "invalida":
                        inval.append(f"{et}: {det_e}")
                    elif est_e == "pendiente":
                        col_pend.append(f"{et}: {det_e}")
                    continue
            try:
                anio = int(k)
            except ValueError:
                inval.append(f"{et}: año no válido")
                continue
            if not str(e.get("fila") or "").strip():
                col_pend.append(f"{et}: sin «fila» (etiqueta de la fila): columna y ejercicio sin comprobar")
                continue
            est_c, det = _cifra_en_columna(pag, e["fila"], anio, e["literal"])
            if est_c == "invalida":
                inval.append(f"{et}: {det}")
            elif est_c == "pendiente":
                col_pend.append(f"{et}: {det}")
            else:
                col_ok += 1
    citas_ok = aus_ok = 0
    if us is not None:
        # (ronda 2) las citas de las clasificaciones y las páginas de los tramos «no_publicada» las examina el contraste de ubicaciones (_contraste_us),
        # con las mismas exigencias de fuente; sus problemas se suman aquí
        ct = us.get("contraste") or {}
        inval += ct.get("invalidas") or []
        incomp += ct.get("incompletas") or []
        citas_ok, aus_ok = ct.get("citas_ok") or 0, ct.get("aus_ok") or 0
    probl = inval + incomp
    otras = bool(G.bloquean())
    if res is not None:
        res["F1_SERIES"] = {"invalidas": inval, "incompletas": incomp, "columna_comprobada": col_ok, "columna_pendiente": col_pend,
                            "nota": "condición mínima, no la verificación de entradas: las filas 85–87 del libro V6.3.1 entran en su universo"}
        if us is not None:
            res["F1_SERIES"].update({"citas_de_clasificacion_comprobadas": citas_ok, "paginas_sin_linea_propia_del_arrendamiento_operativo": aus_ok,
                                     "nota_us_gaap": "las series y clasificaciones propias de US GAAP no están en el libro: quedan fuera del universo de verificacion_entradas.py"})
    G.add("F1-SERIES", bool(probl), "AVISO" if otras else "BLOQUEA", "DATOS INVÁLIDOS" if inval else "INCOMPLETO",
          ("; ".join(probl)[:1500] + (" (además de las guardas que ya bloquean)" if otras else "")) if probl else
          ((f"US GAAP · {citas_ok} clasificaciones con su cita en la página citada y {aus_ok} páginas examinadas sin línea propia (D-US1) · " if us is not None else "") +
           f"D&A de derechos de uso y PPA: cifra publicada con su signo, como cifra completa, en una página existente de una fuente del expediente "
           f"con su huella; columna del ejercicio comprobada en {col_ok} años" + (f", PENDIENTE en {len(col_pend)} (la aptitud por entradas sigue en «no»)"
                                                                                  if col_pend else "")), "(1a) · H12 · V631-2")


def _f_vacia_v631(L):
    """(V6.3.1 F1) En un libro V6.3.1 con un perímetro F1 distinto de A0, f vacía (D_X incompleta en la ventana) no es un libro ilegible: es
    un dato que falta (la capa lo dice con V-F1b o F1-PERIMETRO)."""
    import f1_libro_v631 as V631
    return V631.perimetro_del_libro(L) not in (None, "A0_total")


def _replica_v631(L, r0, calcular, anios, col, rep):
    """(V6.3.1 F1) La réplica (F1-REPLICA) contrasta el perímetro que calcula el libro: A0 en un libro V6.3 (o V6.3.1 con A0); en un libro
    V6.3.1 con A1/A2, las ecuaciones con la D_X del propio libro (fila 88), y D_X con las filas 8, 86 y 87 del libro."""
    import f1_libro_v631 as V631
    p = V631.perimetro_del_libro(L)
    if p in (None, "A0_total"):
        return r0, "A0"
    rep.extend(V631.replica_dx(L, anios, col))
    return calcular("LIBRO_DX", aplicar_n1=False), f"D_X del libro ({p})"


def _libro_v631(L, per, rou, ppa, anios, col, DX_de, decl_r, dif_motor):
    """(V6.3.1 F1) None si el libro no es V6.3.1 F1; si lo es, {perimetro_efectivo, motivos, flujos_contrastados}: motivos vacío = el libro
    calcula el perímetro declarado (comparación numérica con la capa, que queda como oráculo)."""
    import f1_libro_v631 as V631
    p = V631.perimetro_del_libro(L)
    if p is None:
        return None
    n = sum(1 for k in L if k.startswith("Motor!") and k[6:8] in ("AU", "AV", "AW", "AX", "AY", "AZ", "BA", "BB", "BC", "BD", "BF")
            and k[8:] in ("6", "7", "8") and Q(L[k]) is not None)
    mot = V631.corresponde(L, per, rou, ppa, anios, col, (lambda y: DX_de(per, y)) if per else (lambda y: None), decl_r, dif_motor)
    esperado = 11 * len(decl_r["esc"]) if decl_r else 0   # sin palancas todavía (paso 7) no hay flujos en el libro ni en la capa
    if decl_r and n != esperado:
        mot.append(f"{n} flujos del Motor en el libro y {esperado} en la capa (11 por escenario con palancas)")
    return {"perimetro_efectivo": p, "motivos": mot, "flujos_contrastados": n}


def informe_md(r):
    md = [f"# Motor A · perímetro F1 · {r.get('version')}", "",
          f"Libro `{str(r.get('libro_sha256'))[:16]}…` · declaración `{str(r.get('declaracion_sha256'))[:16]}…` · {r.get('fecha')}", "",
          f"**{r.get('rotulo') or r.get('motivo')}**", ""]
    if not r.get("aplica"):
        return "\n".join(md) + "\n"
    md += [f"Estado propuesto: {r.get('estado_propuesto') or '—'} · apto para dinero real: no.", ""]
    if r.get("condicionada"):   # (F1 · US GAAP) hipótesis declaradas y ubicaciones sin contrastar, con su cota
        cd_ = r["condicionada"]
        md += ["## Conclusión condicionada", ""] + [f"- **{c.get('id')}** ({c.get('tipo')}): {c.get('texto')}" for c in cd_.get("condiciones") or []]
        md += ["", str(((cd_.get("cota") or {}).get("resumen") or {}).get("texto") or "cota: ver el bloque de US GAAP"), ""]
    md += ["## Guardas", "",
           "| Id | Salta | Severidad | Efecto | Decisión | Detalle |", "|---|---|---|---|---|---|"]
    for g in r["guardas"]:
        md.append(f"| {g['id']} | {'sí' if g['salta'] else 'no'} | {g['severidad'] or '—'} | {g['efecto'] or '—'} | {g['decision']} | {str(g['detalle']).replace('|', '/')} |")
    md += ["", "## Flujo sin crecimiento por perímetro (diagnóstico)", "", "| Perímetro | f | Flujo sin crecimiento | Frente a A0 | Ancla S2C (E4) |", "|---|---|---|---|---|"]
    dif = r.get("diferencias_frente_a_A0_flujo_sin_crecimiento") or {}
    for k, v in (r.get("diagnostico_por_perimetro") or {}).items():
        md.append(f"| {k} | {v['f']:.9f} | {v['flujo_sin_crecimiento']:.3f} | {dif.get(k, 0):+.3f} | {v['ancla_s2c_E4'] if v['ancla_s2c_E4'] is None else round(v['ancla_s2c_E4'], 6)} |")
    cd = r.get("calculo_perimetro_declarado")
    if cd:
        md += ["", f"## K3 · perímetro declarado ({r.get('perimetro_declarado')})", "", "| Partida | mm | Clase |", "|---|---|---|"]
        for ln in cd["K3"]["lineas"]:
            md.append(f"| {ln['partida']} | {ln['mm']:.3f} | {ln['clase']} |")
        md.append(f"| **= flujo sin crecimiento** | **{cd['K3']['flujo_sin_crecimiento']:.3f}** | {'cuadra' if cd['K3']['identidad_cuadra'] else 'NO CUADRA'} |")
    k3a = ((r.get("diagnostico_por_perimetro") or {}).get("A0_total") or {}).get("K3")
    if k3a:
        md += ["", "## K3 · perímetro A0 (lo que calcula el libro)", "", "| Partida | mm | Clase |", "|---|---|---|"]
        for ln in k3a["lineas"]:
            md.append(f"| {ln['partida']} | {ln['mm']:.3f} | {ln['clase']} |")
        md.append(f"| **= flujo sin crecimiento** | **{k3a['flujo_sin_crecimiento']:.3f}** | {'cuadra' if k3a['identidad_cuadra'] else 'NO CUADRA'} |")
        md.append(f"\nDoble cómputo señalado por K3 en A0: {k3a['doble_computo_mm_en_la_ventana']:.3f} mm de media en la ventana; "
                  f"{k3a['doble_computo_mm_a_la_escala_del_año_base']:.3f} a la escala del año base.")
    if r.get("us_gaap"):
        md += ["", "## US GAAP (ASC 842) · arrendamientos operativos y financieros por separado", "", "```", json.dumps(r["us_gaap"], ensure_ascii=False, indent=1), "```"]
    if r.get("sensibilidad_peso_arrendamiento_1b"):
        md += ["", "## (1b) Sensibilidad al peso del año base", "", "```", json.dumps(r["sensibilidad_peso_arrendamiento_1b"], ensure_ascii=False, indent=1), "```"]
    md += ["", "## Parámetros sin valor adoptado", ""] + [f"- {k}: sin valor ({v['documento']})" for k, v in PARAMETROS_SIN_VALOR.items()]
    return "\n".join(md) + "\n"


def huella_declaracion(decl):
    return hashlib.sha256(json.dumps(decl, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()


EXENCIONES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "esquema", "motor_a_f1_exenciones.json")


def _sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def _json(p):
    try:
        return json.load(open(p, encoding="utf-8"))
    except (OSError, ValueError):
        return None


def exencion(carpeta):
    """(revisión F1-IMPL, H2) Exenciones EXPLÍCITAS de la exigencia F1, registradas (no por la ausencia de un archivo):
    - la línea de base sintética v2.2: fase1_v63.json de una empresa marcada «(inventada)», sin entrada_efectiva.json ni motor_a_f1.json;
    - los cierres históricos anteriores a F1-IMPL, por la huella SHA-256 de su cierre_vigente.json en esquema/motor_a_f1_exenciones.json
      (un cierre nuevo tiene otra huella y no queda exento). Devuelve el motivo o None."""
    f1 = _json(os.path.join(carpeta, "fase1_v63.json")) or {}
    if (isinstance(f1, dict) and "(inventada)" in str(f1.get("empresa") or "")
            and not any(os.path.lexists(os.path.join(carpeta, n)) for n in (DECLARACION, "entrada_efectiva.json"))):
        return "línea de base sintética v2.2 (empresa inventada; sin declaración F1 ni entrada efectiva de la 4.15)"
    cv = os.path.join(carpeta, "cierre_vigente.json")
    if os.path.isfile(cv):
        reg = _json(EXENCIONES) or {}
        h = _sha(cv)
        for e in reg.get("cierres_historicos") or []:
            if e.get("cierre_vigente_sha256") == h:
                return f"cierre histórico registrado anterior a F1-IMPL ({e.get('expediente')}): antecedente; su valor A0 no queda validado por F1"
    return None


def libro_del_expediente(carpeta):
    e = os.path.basename(os.path.abspath(carpeta))
    for p in (os.path.join(carpeta, "recalc", f"{e}_v63_evaluada.xlsx"), os.path.join(carpeta, f"{e}_v63_evaluada.xlsx")):
        if os.path.isfile(p):
            return p
    return None


def arrendamientos_en_el_libro(L):
    """El propio libro muestra arrendamientos: Análisis C49 positivo o vacío (vacío ≠ 0), o principal (fila 17) o pasivo (fila 23)
    positivos en algún año. La PPA no tiene fila en la Historia V6.3: no se puede ver en el libro (límite declarado)."""
    c49 = Q(L.get("Análisis!C49"))
    if c49 is None or c49 > 0:
        return True
    return any((Q(L.get(f"Historia!{c}{fi}")) or 0) > 0 for c in COLS for fi in (17, 23))


def _expediente_415(carpeta):
    """El expediente es de la 4.15: declara F1 (motor_a_f1.json), tiene entrada_efectiva.json, declara el modo en alcance_v2.json o en fase1_metadatos.json, o
    el paso 2 lo registró en estado_pipeline.json."""
    if any(os.path.lexists(os.path.join(carpeta, n)) for n in (DECLARACION, "entrada_efectiva.json")):
        return True
    for n in ("alcance_v2.json", "fase1_metadatos.json"):
        d = _json(os.path.join(carpeta, n))
        if isinstance(d, dict) and "entrada_efectiva" in d:
            return True
    st = _json(os.path.join(carpeta, "estado_pipeline.json"))
    return isinstance(st, dict) and isinstance(st.get("entrada_efectiva"), dict)


def exigido(carpeta, libro=None, L=None):
    """(revisión F1-IMPL, H2) Con el motor A, F1 se exige salvo exención explícita (exencion): si el expediente la declara
    (motor_a_f1.json), si es de la 4.15 (entrada_efectiva.json, el modo en alcance_v2.json o fase1_metadatos.json, o registrado en
    estado_pipeline.json), o si el propio libro muestra arrendamientos. Sin libro legible, se exige (falla en cerrado)."""
    if exencion(carpeta):
        return False
    if _expediente_415(carpeta):
        return True
    if L is None:
        libro = libro or libro_del_expediente(carpeta)
        if not libro:
            return True
        try:
            L = leer_libro(libro)
        except Exception:  # noqa: BLE001 — sin libro legible no se sabe que no haya arrendamientos
            return True
    # (F1 · US GAAP) un libro US GAAP no muestra los arrendamientos operativos (C49 y la fila 17 van a cero): con el motor A, F1 se exige siempre
    return arrendamientos_en_el_libro(L) or norma_del_libro(L) == "US_GAAP"


def _l4_del_libro(ruta):
    """Texto de Control maestro L4 de un .xlsx. (ronda 2, R1-1) Se lee con openpyxl, que resuelve los textos compartidos: v63_xml.LibroV63.leer devuelve el
    valor tal como está en el XML y, en los libros que recalcula LibreOffice, eso es el ÍNDICE del texto compartido («1149»), no «US GAAP»."""
    import openpyxl
    wb = openpyxl.load_workbook(ruta, data_only=True, read_only=True)
    try:
        return wb["Control maestro"]["L4"].value if "Control maestro" in wb.sheetnames else None
    finally:
        wb.close()


def norma_del_expediente(carpeta, libro=None, L=None):
    """(norma, legible): la norma del libro del expediente por la lista cerrada («NIIF», «US_GAAP» o None si L4 está vacío o fuera de la lista) y si el
    libro se pudo leer (False: no hay libro evaluado o no se puede abrir)."""
    if L is None:
        libro = libro or libro_del_expediente(carpeta)
        if not libro:
            return None, False
        try:
            L = {"Control maestro!L4": _l4_del_libro(libro)}
        except Exception:  # noqa: BLE001 — un libro que no se puede leer no dice su norma
            return None, False
    return norma_del_libro(L), True


def us_gaap_del_expediente(carpeta, libro=None, L=None):
    """(F1 · US GAAP) True si la declaración F1 dice US_GAAP o el libro del expediente dice «US GAAP» (Control maestro L4, lista cerrada)."""
    d = _json(os.path.join(carpeta, DECLARACION))
    if isinstance(d, dict) and _valor(d, "norma_contable")[0] == "US_GAAP":
        return True
    return norma_del_expediente(carpeta, libro=libro, L=L)[0] == "US_GAAP"


def exigido_puente(carpeta, libro=None, L=None):
    """(F1 · US GAAP) Con el motor B, F1 se exige solo para el puente de deuda (F1-US-PUENTE: el pasivo por arrendamiento operativo no es deuda del
    puente), salvo exención explícita (exencion): si la declaración o el libro dicen US GAAP. (ronda 2, R1-1) Y si la norma del libro NO SE PUEDE
    DETERMINAR (sin libro legible, L4 vacío o con un valor fuera de la lista cerrada, como «U.S. GAAP») en un expediente de la 4.15: falla en
    cerrado, como el motor A (F1-NORMA dirá qué falta). Con un libro NIIF reconocido no se exige (T11)."""
    if exencion(carpeta):
        return False
    d = _json(os.path.join(carpeta, DECLARACION))
    if isinstance(d, dict) and _valor(d, "norma_contable")[0] == "US_GAAP":
        return True
    n, _ = norma_del_expediente(carpeta, libro=libro, L=L)
    if n is not None:
        return n == "US_GAAP"
    return _expediente_415(carpeta)


def vigencia(carpeta, motor=None):
    """(revisión F1-IMPL, H1 y H6) Estado F1 del expediente para el cierre, la ficha y el informe: exigido, exento, vigente (el resultado
    corresponde a la declaración y al libro evaluado actuales) y utilizable. Con el motor A y F1 exigido, sin un resultado vigente y
    utilizable no hay conclusión del motor A."""
    st = _json(os.path.join(carpeta, "estado_pipeline.json")) or {}
    r = _json(os.path.join(carpeta, RESULTADO))
    motor = motor or (st.get("motor") if isinstance(st, dict) else None) or (
        (r.get("motor_del_libro") if r.get("motor_del_libro") in ("A", "B", "C") else ("A" if r.get("aplica") else r.get("motor_del_libro"))) if isinstance(r, dict) else None)
    if motor is None:
        # (revisión V6.3.1, V631-1; R2-1) sin el motor en el estado ni en el resultado, el de la fase A (fase_a.json, C62)
        fa = _json(os.path.join(carpeta, "fase_a.json"))
        c62 = ((fa.get("celdas") or {}) if isinstance(fa, dict) else {}).get("C62")
        motor = {"Sí": "A", "No · financiación cambia mucho": "B", "No · banco o aseguradora": "C"}.get(c62)
    out = {"motor": motor, "exento": exencion(carpeta)}
    if motor is None and not out["exento"] and exigido(carpeta):
        # motor desconocido no es «no es el A»: con F1 exigido, sin saber el motor no hay conclusión acreditada
        return dict(out, exigido=True, vigente=False, utilizable=False, motivo="motor desconocido (ni el estado del pipeline, ni el resultado F1, "
                    "ni fase_a.json lo dicen): F1 no se puede dar por no aplicable")
    puente_b = motor == "B" and exigido_puente(carpeta)   # (F1 · US GAAP) con el motor B, solo el puente de deuda (ronda 2, R1-1: la regla del gancho)
    if motor != "A" and not puente_b:
        return dict(out, exigido=False, vigente=None, utilizable=None, motivo="el motor no es el A")
    if out["exento"]:
        return dict(out, exigido=False, vigente=None, utilizable=None, motivo=out["exento"])
    if not puente_b and not exigido(carpeta):
        return dict(out, exigido=False, vigente=None, utilizable=None, motivo="el libro no muestra arrendamientos y el expediente no es de la 4.15")
    if not isinstance(r, dict):
        return dict(out, exigido=True, vigente=False, utilizable=False, motivo="sin evaluación F1 (motor_a_f1_resultado.json)")
    dp = os.path.join(carpeta, DECLARACION)
    d = _json(dp) if os.path.exists(dp) else {}
    if d is None or huella_declaracion(d) != r.get("declaracion_sha256"):
        return dict(out, exigido=True, vigente=False, utilizable=False, motivo="la declaración F1 cambió (o no se puede leer) después de la evaluación")
    e = os.path.basename(os.path.abspath(carpeta))
    pl = os.path.join(carpeta, f"{e}_v63_evaluada.xlsx")
    if not r.get("libro_origen_sha256") or not os.path.isfile(pl) or _sha(pl) != r.get("libro_origen_sha256"):
        return dict(out, exigido=True, vigente=False, utilizable=False, motivo="el libro evaluado no es el que se evaluó con F1 (o no consta su huella)")
    ok = bool(r.get("utilizable_para_conclusion"))
    return dict(out, exigido=True, vigente=True, utilizable=ok, motivo=None if ok else str(r.get("rotulo")))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="orden", required=True)
    e = sub.add_parser("evaluar")
    e.add_argument("carpeta")
    e.add_argument("--libro")
    e.add_argument("--declaracion")
    e.add_argument("--salida")
    e.add_argument("--motor", help="motor elegido por la fase A (el pipeline lo pasa; si no, el de Diagnóstico V6!C5)")
    e.add_argument("--libro-origen", help="libro evaluado del expediente (su huella queda en el resultado para la vigencia)")
    sub.add_parser("plantilla")
    a = ap.parse_args(argv)
    if a.orden == "plantilla":
        print(json.dumps(plantilla_declaracion(), ensure_ascii=False, indent=1))
        return 0
    c = a.carpeta
    libro = a.libro
    if not libro:
        cand = sorted(x for x in os.listdir(os.path.join(c, "recalc")) if x.endswith("_v63_evaluada.xlsx")) if os.path.isdir(os.path.join(c, "recalc")) else []
        if not cand:
            print("ERROR: no hay recalc/<E>_v63_evaluada.xlsx: indica --libro (un libro recalculado)")
            return 2
        libro = os.path.join(c, "recalc", cand[0])
    pd_ = a.declaracion or os.path.join(c, DECLARACION)
    salida = a.salida or c
    try:
        decl = json.load(open(pd_, encoding="utf-8")) if os.path.exists(pd_) else {}
    except (OSError, ValueError) as ex:
        print(f"ERROR: {pd_} no se puede leer ({type(ex).__name__}): no se evalúa nada (falla en cerrado)")
        return 2
    try:
        L = leer_libro(libro)
        r = evaluar(L, decl, motor_libro=a.motor, carpeta=c)
    except ErrorDeclaracion as ex:
        print(f"ERROR: {ex}")
        return 2
    if not os.path.exists(pd_):
        r["declaracion"] = "ausente: todo sin declarar"
    r["declaracion_ruta"] = os.path.abspath(pd_)
    if a.libro_origen:
        r["libro_origen_sha256"] = _sha(a.libro_origen)
    os.makedirs(salida, exist_ok=True)
    json.dump(r, open(os.path.join(salida, RESULTADO), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    open(os.path.join(salida, RESULTADO_MD), "w", encoding="utf-8").write(informe_md(r))
    print(r.get("rotulo") or r.get("motivo"))
    if not r.get("aplica") or not r.get("bloquea"):
        return 0
    ep = r.get("estado_propuesto") or ""
    return 5 if "implementacion" in ep else 3 if ep == "pendiente_de_datos" else 4


if __name__ == "__main__":
    sys.exit(main())
