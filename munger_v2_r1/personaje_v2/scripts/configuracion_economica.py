#!/usr/bin/env python3
"""Configuración económica explícita del motor B para la plantilla V6.4 experimental (encargo 4.11 §3, §6 y §10).

Un expediente que se ejecuta con la plantilla V6.4 lleva `configuracion_economica.json`: el modo (Heredado o Experimental) y, en
modo experimental, N1, N2, N3 y P-M1 con su trazabilidad (clase, confianza, fuente o condición, justificación y materialidad).
La escribe la ORQUESTACIÓN (o una persona), nunca un agente de juicio, y NO es una adopción: es la configuración de un ensayo.
El pipeline la aplica al libro de datos en el paso 2 (después de la fase 1) y la incluye en el material auditado
(cierre_v2.MATERIAL_FIJO): cambiarla después del cierre retira la aprobación en la primera llamada, aunque el libro no se haya
recalculado.

(4.13 §7) La plantilla V6.4.1 experimental añade a P-M1 el perímetro de la inversión que repone el capital (B146:B152):
«Caja» (capex de caja frente a toda la D&A, lo de la V6.4) o «NIIF 16» (capex de caja + altas de derechos de uso). Es opcional en
el formato, solo existe en la V6.4.1 (seleccion_plantilla rechaza declararlo con la V6.4 y exige declararlo con la V6.4.1 cuando
hay requisito adicional) y no cambia la huella de una configuración que no lo declara (huella_configuracion omite sus celdas vacías).

Uso:
  configuracion_economica.py validar CONF.json            → código 0 si es válida; 1 con la lista de faltas
  configuracion_economica.py celdas CONF.json             → imprime el JSON {"Configuración V6.4!B4": …}
  configuracion_economica.py aplicar LIBRO_IN LIBRO_OUT CONF.json [--config config.json]
        escribe las celdas en una copia (LibroV63, lista blanca = entradas de «Configuración V6.4» del inventario de la plantilla
        activa), borra las cachés y verifica el libro con el verificador de la configuración (código 0 ÍNTEGRO; 1 si no)
  configuracion_economica.py resumen CONF.json            → una línea legible
El formato (versión 1) está en ESQUEMA_RESUMIDO, más abajo. Las validaciones replican las del libro y añaden la trazabilidad
completa de cada parámetro activo (el libro solo la muestra).
"""
import hashlib
import json
import os
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)

HOJA = "Configuración V6.4"
MODOS = ("Heredado", "Experimental")
CLASES = ("dato publicado", "derivado de datos publicados", "convención", "hipótesis")
CONFIANZAS = ("alta", "media", "baja")
ESCUDO = ("Vinculado al tipo aplicado a NOPAT", "Tipo de la Historia (separado)")
REGLAS = ("R0 · simétrica (heredada)", "R1 · solo circulante; capacidad conservada")
ESTRUCTURAS = ("Sin requisito adicional", "H · hueco (crédito de la inversión para crecer)", "S · suma sin reestimar",
               "SR1 · suma con S2C reestimado", "SR2 · suma con S2C y ROIC reestimados", "SRF · suma con inversión fija reestimada")
FAMILIAS = ("Λ · (λ − 1) × amortización que se repone", "Θ · θ × exceso histórico medio")
CONV_ANIOS = ("Plana", "Proporcional a las ventas")
CONV_TERM = ("Proporcional a las ventas", "Crece con g")
ROIC_T = ("ROIC de la fase B sin cambio", "ROIC × f (SR2)")
CARTERA = ("Legado · se repone con la amortización", "P0 · no se repone (explícito)")
# (4.13 §7) perímetro de la inversión (plantilla V6.4.1 experimental, «Configuración V6.4»!B146); el texto es el de la lista del libro
PERIMETROS = ("Caja · capex de caja frente a toda la D&A (V6.4)", "NIIF 16 · capex de caja + altas de derechos de uso frente a toda la D&A")
# filas de la tabla de trazabilidad del libro (C:G = clase, confianza, fuente o condición, justificación, materialidad)
FILAS_TRAZA = {"N1.tipo": 129, "N1.escudo": 130, "N2.margen": 131, "N3.regla": 132, "N3.circulante": 133, "PM1.estructura": 134,
               "PM1.familia": 135, "PM1.parametro": 136, "PM1.convencion_anios": 137, "PM1.convencion_terminal": 138,
               "PM1.roic_terminal": 139, "PM1.cartera": 140, "modo": 141, "PM1.perimetro": 142}
CAMPOS_TRAZA = ("clase", "confianza", "fuente_o_condicion", "justificacion", "materialidad")
# (4.12 §4) protocolo experimental del precio objetivo cuando lo condicionan hipótesis sin fundamento suficiente (objetivo_v64.py).
# Lo declara la orquestación en cada expediente experimental nuevo; es un ensayo, no una regla adoptada. Opcional para que las
# configuraciones de la 4.11 sigan siendo válidas: si falta cuando hace falta, no se emite un objetivo oficial (objetivo_v64).
PROTOCOLOS = ("bloqueo_del_objetivo", "objetivo_condicionado")
# (4.12 §4) celdas de entrada de «Configuración V6.4» de cada parámetro (sin las de trazabilidad, que son texto): sirven para saber
# qué parámetros varía cada variante calculada (ámbito de cada afirmación de materialidad) y qué celda nombra cada parámetro en D10
TRAZA_CELDAS = {"modo": ["B4"], "N1.tipo": ["B11", "B12", "B13", "B14", "B15"], "N1.escudo": ["B16"], "N2.margen": ["B21", "B22", "B23"],
                "N3.regla": ["B28"], "N3.circulante": ["B29", "B30", "B31", "B32"], "PM1.estructura": ["B36"], "PM1.familia": ["B37"],
                "PM1.parametro": ["B38", "B39"], "PM1.convencion_anios": ["B40"], "PM1.convencion_terminal": ["B41"], "PM1.roic_terminal": ["B42"],
                "PM1.cartera": [f"B{i}" for i in range(43, 52)],
                "PM1.perimetro": ["B146"] + [f"B{i}" for i in range(147, 152)] + ["B152"]}
# (4.13 §7) celdas que solo existen en la V6.4.1: vacías equivalen a la V6.4 («Caja»), así que la huella y la instantánea las omiten
# cuando están vacías (las configuraciones y los libros anteriores conservan su huella exacta)
SOLO_V641 = {"B146", "B147", "B148", "B149", "B150", "B151", "B152"}
# (4.12 §5) celdas de entrada que son metadatos de trazabilidad (fuente, período, perímetro, clase, procedencia): un cambio en ellas es
# editorial (no cambia ningún cálculo) y no entra en la huella de las entradas económicas
CELDAS_METADATOS = {"B12", "B13", "B14", "B15", "B22", "B23", "B32", "B51", "B152"}
# parámetros numéricos que la comprobación conjunta (D10) puede mover; los demás son alternativas no numéricas
NUMERICOS = {"N1.tipo": "B11", "N2.margen": "B21"}
ESQUEMA_RESUMIDO = {
    "tipo": "configuracion_economica_motor_B", "version_formato": 1, "plantilla_requerida": "V6.4 experimental o V6.4.1 experimental (esta, para el perímetro de la inversión)",
    "modo": "Heredado | Experimental", "naturaleza": "texto: ensayo, no adopción",
    "N1": "null | {valor, fuente, periodo, perimetro, clase, escudo}",
    "N2": "null | {valor, perimetro, procedencia}",
    "N3": "{regla, existencias, deudores, acreedores, fuente}",
    "PM1": "{estructura, familia, lambda, theta, [lambda_rango | theta_rango: [mín, máx], opcional: variantes de los extremos], convencion_anios, convencion_terminal, roic_terminal, cartera, cartera_anual, cartera_vnc, cartera_historica[5], cartera_fuente, [V6.4.1: perimetro_inversion, altas_derechos_uso[5], altas_fuente]}",
    "trazabilidad": "{clave de FILAS_TRAZA: {clase, confianza, fuente_o_condicion, justificacion, materialidad}}",
}


def _vacio(x):
    return x is None or (isinstance(x, str) and not x.strip())


def _num(x):
    # (4.13, revisión interna R12) solo números finitos: Infinity y NaN no son valores de ningún parámetro
    import math
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)


def activos(conf):
    """Claves de FILAS_TRAZA que están activas en esta configuración."""
    if not isinstance(conf, dict) or conf.get("modo") != "Experimental":
        return ["modo"]
    a = ["modo", "N3.regla", "PM1.estructura", "PM1.cartera"]
    if conf.get("N1"):
        a += ["N1.tipo", "N1.escudo"]
    if conf.get("N2"):
        a += ["N2.margen"]
    n3, pm = conf.get("N3") or {}, conf.get("PM1") or {}
    if n3.get("regla") == REGLAS[1]:
        a += ["N3.circulante"]
    if pm.get("estructura") not in (None, ESTRUCTURAS[0]):
        a += ["PM1.familia", "PM1.parametro", "PM1.convencion_anios", "PM1.convencion_terminal", "PM1.roic_terminal"]
        if declara_perimetro(conf):
            a += ["PM1.perimetro"]  # (4.13 §7) V6.4.1: la fila 142 del libro está activa con requisito adicional
    return a


def declara_perimetro(conf):
    """(4.13 §7) True si la configuración declara el perímetro de la inversión (campo de la V6.4.1)."""
    pm = conf.get("PM1") if isinstance(conf, dict) else None
    return isinstance(pm, dict) and any(pm.get(k) is not None for k in ("perimetro_inversion", "altas_derechos_uso", "altas_fuente"))


def es_niif16(conf):
    return declara_perimetro(conf) and conf["PM1"].get("perimetro_inversion") == PERIMETROS[1]


def validar(conf):
    # (4.13 §3) validación estructural explícita ANTES de cualquier .get: un JSON válido de otro tipo (null, [], 3, "x") o con un
    # campo anidado de otro tipo (N1 = [], PM1 = "x") devuelve faltas, nunca una excepción
    import estructura_json as ESTR
    fe = ESTR.comprobar(conf, ESTR.PLANO_CONFIGURACION_ECONOMICA)
    if fe:
        return ["estructura: " + x for x in fe]
    f = []
    if conf.get("tipo") != "configuracion_economica_motor_B" or conf.get("version_formato") != 1:
        f.append("tipo o version_formato desconocidos (se espera configuracion_economica_motor_B, versión 1)")
    if conf.get("modo") not in MODOS:
        f.append("modo: «Heredado» o «Experimental»")
        return f
    if conf.get("protocolo_objetivo") is not None and conf.get("protocolo_objetivo") not in PROTOCOLOS:
        f.append(f"protocolo_objetivo: uno de {PROTOCOLOS} (o ausente; 4.12 §4)")
    if _vacio(conf.get("naturaleza")):
        f.append("naturaleza: falta la declaración (ensayo o hipótesis, no adopción)")
    if conf["modo"] == "Heredado":
        for k in ("N1", "N2", "N3", "PM1", "protocolo_objetivo"):
            if conf.get(k):
                f.append(f"{k}: en modo heredado no se escriben opciones experimentales (se ignorarían); quítalas o usa el modo experimental"
                         + (" (4.12: el protocolo del objetivo es de la capa experimental; en modo heredado rige el Anexo B §B.6.7)" if k == "protocolo_objetivo" else ""))
        return f
    n1 = conf.get("N1")
    if n1 is not None:
        if not (_num(n1.get("valor")) and 0 <= n1["valor"] < 1):
            f.append("N1.valor: número en [0, 1)")
        for k in ("fuente", "periodo", "perimetro"):
            if _vacio(n1.get(k)):
                f.append(f"N1.{k}: obligatorio")
        if n1.get("clase") not in CLASES:
            f.append(f"N1.clase: una de {CLASES}")
        if n1.get("escudo") not in ESCUDO:
            f.append(f"N1.escudo: uno de {ESCUDO}")
    n2 = conf.get("N2")
    if n2 is not None:
        if not (_num(n2.get("valor")) and -1 < n2["valor"] < 1):
            f.append("N2.valor: número en (−1, 1)")
        for k in ("perimetro", "procedencia"):
            if _vacio(n2.get(k)):
                f.append(f"N2.{k}: obligatorio")
    n3 = conf.get("N3") or {}
    if n3.get("regla") not in REGLAS:
        f.append(f"N3.regla: una de {REGLAS} (obligatoria en modo experimental)")
    if n3.get("regla") == REGLAS[1]:
        for k in ("existencias", "deudores", "acreedores"):
            if not (_num(n3.get(k)) and n3[k] >= 0):
                f.append(f"N3.{k}: número ≥ 0 (R1)")
        if _vacio(n3.get("fuente")):
            f.append("N3.fuente: obligatoria con R1")
    pm = conf.get("PM1") or {}
    if pm.get("estructura") not in ESTRUCTURAS:
        f.append(f"PM1.estructura: una de {ESTRUCTURAS} (obligatoria; ninguna es central por defecto)")
    if pm.get("cartera") not in CARTERA:
        f.append(f"PM1.cartera: una de {CARTERA}")
    req = pm.get("estructura") in ESTRUCTURAS[1:]
    if (req or pm.get("cartera") == CARTERA[1]) and n3.get("regla") != REGLAS[1]:
        f.append("R0 + P-M1 no está especificado: las estructuras de reposición parten de R1")
    if req:
        if pm.get("familia") not in FAMILIAS:
            f.append(f"PM1.familia: una de {FAMILIAS}")
        if pm.get("familia") == FAMILIAS[0] and not (_num(pm.get("lambda")) and pm["lambda"] >= 1):
            f.append("PM1.lambda: número ≥ 1")
        if pm.get("familia") == FAMILIAS[1] and not (_num(pm.get("theta")) and 0 <= pm["theta"] <= 1):
            f.append("PM1.theta: número en [0, 1]")
        if pm.get("convencion_anios") not in CONV_ANIOS:
            f.append(f"PM1.convencion_anios: una de {CONV_ANIOS}")
        if pm.get("convencion_terminal") not in CONV_TERM:
            f.append(f"PM1.convencion_terminal: una de {CONV_TERM}")
        # (4.11, revisión interna H11) rango opcional del parámetro (hipótesis): [mínimo, máximo] con el valor activo dentro; con él,
        # variantes_configuracion_v64.py calcula los dos extremos (no entra en el libro)
        for k_r, k_p, lo, hi in (("lambda_rango", "lambda", 1.0, None), ("theta_rango", "theta", 0.0, 1.0)):
            rg = pm.get(k_r)
            if rg is None:
                continue
            if not (isinstance(rg, list) and len(rg) == 2 and all(_num(x) for x in rg) and rg[0] <= rg[1]
                    and rg[0] >= lo and (hi is None or rg[1] <= hi)):
                f.append(f"PM1.{k_r}: [mínimo, máximo] numéricos y ordenados dentro del dominio del parámetro")
            elif _num(pm.get(k_p)) and not (rg[0] <= pm[k_p] <= rg[1]):
                f.append(f"PM1.{k_r}: el valor activo de {k_p} tiene que estar dentro del rango")
        sr2 = pm.get("estructura", "").startswith("SR2")
        if pm.get("roic_terminal") != (ROIC_T[1] if sr2 else ROIC_T[0]):
            f.append("PM1.roic_terminal: «ROIC × f (SR2)» en SR2 y «ROIC de la fase B sin cambio» en las demás")
    if declara_perimetro(conf):
        # (4.13 §7) perímetro de la inversión (V6.4.1): replica la comprobación 29 del libro
        if pm.get("perimetro_inversion") not in PERIMETROS:
            f.append(f"PM1.perimetro_inversion: uno de {PERIMETROS}")
        # sin requisito adicional el perímetro no tiene efecto (en el libro, B55 y B58 solo alimentan celdas condicionadas por B67);
        # se admite para que las variantes y alternativas «sin requisito» conserven las mismas entradas
        alt = pm.get("altas_derechos_uso")
        # con «Caja» las altas pueden quedar declaradas (el libro no las suma: B153 = 0); así la variante de control NIIF 16 o Caja
        # se calcula con los mismos datos sin inventar ninguno. Si se declaran, se validan igual
        if pm.get("perimetro_inversion") == PERIMETROS[1] or alt is not None:
            if not (isinstance(alt, list) and len(alt) == 5 and all(_num(x) and x >= 0 for x in alt)):
                f.append("PM1.altas_derechos_uso: cinco números ≥ 0 de los años H–L (0 explícito); obligatorios con NIIF 16")
            if _vacio(pm.get("altas_fuente")):
                f.append("PM1.altas_fuente: obligatoria con las altas de derechos de uso")
    if pm.get("cartera") == CARTERA[1]:
        h = pm.get("cartera_historica")
        if not (_num(pm.get("cartera_anual")) and _num(pm.get("cartera_vnc")) and isinstance(h, list) and len(h) == 5 and all(_num(x) for x in h)):
            f.append("PM1 con P0: cartera_anual, cartera_vnc y cartera_historica (cinco números, 0 explícito) obligatorios")
        elif min([pm["cartera_anual"], pm["cartera_vnc"]] + h) < 0:
            f.append("PM1 con P0: importes de la cartera ≥ 0")
        elif pm["cartera_vnc"] > 10 * pm["cartera_anual"]:
            f.append("PM1 con P0: la cartera no se agota en diez años")
        if _vacio(pm.get("cartera_fuente")):
            f.append("PM1.cartera_fuente: obligatoria con P0")
    tz = conf.get("trazabilidad") or {}
    for k in activos(conf):
        t = tz.get(k) or {}
        falt = [c for c in CAMPOS_TRAZA if _vacio(t.get(c))]
        if falt:
            f.append(f"trazabilidad.{k}: faltan {', '.join(falt)}")
        if t.get("clase") not in (None, "") and t["clase"] not in CLASES:
            f.append(f"trazabilidad.{k}.clase: una de {CLASES}")
        if t.get("confianza") not in (None, "") and t["confianza"] not in CONFIANZAS:
            f.append(f"trazabilidad.{k}.confianza: una de {CONFIANZAS}")
    return f


def celdas(conf, v641=False):
    """{"Configuración V6.4!REF": valor} con TODAS las celdas de entrada de la hoja (las no usadas, vacías: no se arrastra nada).
    (4.13 §7) Con v641=True (el libro de destino es V6.4.1) también las del perímetro, vacías si la configuración no lo declara; con
    False solo si lo declara (un libro V6.4 no las admite y la huella de las configuraciones anteriores no cambia)."""
    H = HOJA + "!"
    c = {H + r: None for r in ["B4"] + [f"B{i}" for i in list(range(11, 17)) + list(range(21, 24)) + list(range(28, 33)) + list(range(36, 52))]
         + [f"{col}{i}" for i in range(129, 142) for col in "CDEFG"]}
    if v641 or declara_perimetro(conf):  # (4.13 §7) solo V6.4.1: las celdas no existen como entradas en la V6.4
        c.update({H + r: None for r in sorted(SOLO_V641)} | {H + f"{col}142": None for col in "CDEFG"})
    c[H + "B4"] = conf["modo"]
    if conf["modo"] == "Experimental":
        n1, n2, n3, pm = conf.get("N1"), conf.get("N2"), conf.get("N3") or {}, conf.get("PM1") or {}
        if n1:
            c.update({H + "B11": n1["valor"], H + "B12": n1["fuente"], H + "B13": n1["periodo"], H + "B14": n1["perimetro"], H + "B15": n1["clase"], H + "B16": n1["escudo"]})
        if n2:
            c.update({H + "B21": n2["valor"], H + "B22": n2["perimetro"], H + "B23": n2["procedencia"]})
        c[H + "B28"] = n3.get("regla")
        for k, r in (("existencias", "B29"), ("deudores", "B30"), ("acreedores", "B31"), ("fuente", "B32")):
            if n3.get(k) is not None:
                c[H + r] = n3[k]
        for k, r in (("estructura", "B36"), ("familia", "B37"), ("lambda", "B38"), ("theta", "B39"), ("convencion_anios", "B40"),
                     ("convencion_terminal", "B41"), ("roic_terminal", "B42"), ("cartera", "B43"), ("cartera_anual", "B44"),
                     ("cartera_vnc", "B45"), ("cartera_fuente", "B51")):
            if pm.get(k) is not None:
                c[H + r] = pm[k]
        for i, x in enumerate(pm.get("cartera_historica") or []):
            c[H + f"B{46 + i}"] = x
        if declara_perimetro(conf):
            c[H + "B146"] = pm.get("perimetro_inversion")
            for i, x in enumerate(pm.get("altas_derechos_uso") or []):
                c[H + f"B{147 + i}"] = x
            c[H + "B152"] = pm.get("altas_fuente")
    for k, t in (conf.get("trazabilidad") or {}).items():
        if k not in FILAS_TRAZA or (k == "PM1.perimetro" and not declara_perimetro(conf)):
            continue
        for col, campo in zip("CDEFG", CAMPOS_TRAZA):
            if not _vacio(t.get(campo)):
                c[H + f"{col}{FILAS_TRAZA[k]}"] = t[campo]
    return c


def resumen(conf):
    if conf.get("modo") != "Experimental":
        return "modo heredado (V6.3 efectiva)"
    n1, n2, n3, pm = conf.get("N1"), conf.get("N2"), conf.get("N3") or {}, conf.get("PM1") or {}
    p = [f"N1 {n1['valor']:.6g} ({'escudo vinculado' if n1['escudo'] == ESCUDO[0] else 'escudo al tipo de la Historia'})" if n1 else "N1 vacío (tipo de la Historia)",
         f"N2 {n2['valor']:.6g}" if n2 else "N2 vacío (Palancas C8)", (n3.get("regla") or "?").split(" ·")[0]]
    if pm.get("estructura") in ESTRUCTURAS[1:]:
        fam = "Λ" if pm.get("familia") == FAMILIAS[0] else "Θ"
        par = pm.get("lambda") if fam == "Λ" else pm.get("theta")
        p.append(f"P-M1 {pm['estructura'].split(' ·')[0]} · {fam} {par} · años {pm.get('convencion_anios')} · terminal {pm.get('convencion_terminal')}"
                 + (f" · perímetro {str(pm.get('perimetro_inversion')).split(' ·')[0]}" if declara_perimetro(conf) else ""))
    else:
        p.append("P-M1 sin requisito adicional")
    p.append("P0" if pm.get("cartera") == CARTERA[1] else "cartera legado")
    return "modo experimental · " + " · ".join(p)


# ------------------------------------------------------------------------------------------- (4.12 §4) ámbito y cobertura D10
def parametros_variados(conf_a, conf_b):
    """Claves de TRAZA_CELDAS cuyas celdas de entrada difieren entre dos configuraciones (las de trazabilidad no cuentan: son texto).
    Sirve para el ámbito de cada afirmación de materialidad: qué variantes calculadas varían cada parámetro."""
    ca, cb = celdas(conf_a), celdas(conf_b)
    return [k for k, refs in TRAZA_CELDAS.items() if any(ca.get(f"{HOJA}!{r}") != cb.get(f"{HOJA}!{r}") for r in refs)]


def celda_principal(clave, conf):
    """«Configuración V6.4!REF» con la que un parámetro activo se nombra en fundamento_material (D10): la del valor del parámetro."""
    if clave == "PM1.parametro":
        ref = "B39" if (conf.get("PM1") or {}).get("familia") == FAMILIAS[1] else "B38"
    else:
        ref = (TRAZA_CELDAS.get(clave) or [None])[0]
    return f"{HOJA}!{ref}" if ref else None


def numericos_activos(conf):
    """{clave: «Configuración V6.4!REF»} de los parámetros numéricos ACTIVOS que la comprobación conjunta puede mover: N1 (si hay N1),
    N2 (si hay N2) y el parámetro de la familia activa (λ o θ) si hay requisito adicional. Una combinación que mueve otra celda de la
    configuración mueve un parámetro inactivo (no cambiaría nada y aparentaría una comprobación)."""
    if conf.get("modo") != "Experimental":
        return {}
    out = {}
    if conf.get("N1"):
        out["N1.tipo"] = f"{HOJA}!B11"
    if conf.get("N2"):
        out["N2.margen"] = f"{HOJA}!B21"
    pm = conf.get("PM1") or {}
    if pm.get("estructura") in ESTRUCTURAS[1:]:
        out["PM1.parametro"] = celda_principal("PM1.parametro", conf)
    return out


def alternativas(conf, clave):
    """(4.12 §4 y §9) Alternativas NO numéricas definidas de un parámetro activo: [(etiqueta, configuración)]; [] con motivo si no
    hay ninguna definida sin inventar entradas. Las usa la comprobación conjunta para evaluar de forma explícita una hipótesis no
    numérica sin fundamento suficiente con una conclusión favorable. Devuelve (lista, motivo_si_vacía)."""
    import copy as _copy
    pm = conf.get("PM1") or {}
    n3 = conf.get("N3") or {}
    req = pm.get("estructura") in ESTRUCTURAS[1:]
    out = []
    if clave == "PM1.estructura" and not req:
        # sin requisito activo, las estructuras de reposición necesitan familia y parámetro que la configuración no declara
        return [], "sin requisito activo: las estructuras de reposición necesitan familia, parámetro y convenciones que la configuración no declara"
    if clave == "PM1.estructura":
        for e in ESTRUCTURAS:
            if e == pm.get("estructura"):
                continue
            if e == ESTRUCTURAS[0]:
                out.append(("sin requisito adicional", {**conf, "PM1": {**pm, "estructura": e}}))
            else:
                out.append((e.split(" ·")[0], {**conf, "PM1": {**pm, "estructura": e, "roic_terminal": ROIC_T[1] if e.startswith("SR2") else ROIC_T[0]}}))
    elif clave == "PM1.convencion_anios" and req:
        out.append((f"años «{CONV_ANIOS[1] if pm.get('convencion_anios') == CONV_ANIOS[0] else CONV_ANIOS[0]}»",
                    {**conf, "PM1": {**pm, "convencion_anios": CONV_ANIOS[1] if pm.get("convencion_anios") == CONV_ANIOS[0] else CONV_ANIOS[0]}}))
    elif clave == "PM1.convencion_terminal" and req:
        out.append((f"terminal «{CONV_TERM[1] if pm.get('convencion_terminal') == CONV_TERM[0] else CONV_TERM[0]}»",
                    {**conf, "PM1": {**pm, "convencion_terminal": CONV_TERM[1] if pm.get("convencion_terminal") == CONV_TERM[0] else CONV_TERM[0]}}))
    elif clave == "PM1.familia" and req:
        otra = FAMILIAS[1] if pm.get("familia") == FAMILIAS[0] else FAMILIAS[0]
        k_otra = "theta" if otra == FAMILIAS[1] else "lambda"
        if _num(pm.get(k_otra)):
            out.append((f"familia {otra.split(' ·')[0]} con {k_otra} = {pm[k_otra]}", {**conf, "PM1": {**pm, "familia": otra}}))
        else:
            return [], f"la otra familia ({otra.split(' ·')[0]}) no tiene {k_otra} declarado en la configuración: la combinación no está definida"
    elif clave == "PM1.cartera":
        if pm.get("cartera") == CARTERA[1]:
            out.append(("cartera legado", {**conf, "PM1": {**pm, "cartera": CARTERA[0]}}))
        else:
            return [], "P0 necesita los importes de la cartera (cartera_anual, cartera_vnc, cartera_historica) que la configuración no declara"
    elif clave == "N1.escudo" and conf.get("N1"):
        otro = ESCUDO[1] if conf["N1"].get("escudo") == ESCUDO[0] else ESCUDO[0]
        out.append((f"escudo «{otro}»", {**conf, "N1": {**conf["N1"], "escudo": otro}}))
    elif clave == "N3.regla":
        if req or pm.get("cartera") == CARTERA[1]:
            return [], "R0 + P-M1 no está especificado (la configuración lo rechaza): la alternativa R0 no está definida con P-M1 activo"
        if n3.get("regla") == REGLAS[1]:
            out.append(("R0 · simétrica", {**conf, "N3": {"regla": REGLAS[0]}}))
        else:
            return [], "R1 necesita existencias, deudores, acreedores y fuente que la configuración no declara"
    elif clave == "PM1.perimetro" and req and declara_perimetro(conf):
        otro = PERIMETROS[0] if pm.get("perimetro_inversion") == PERIMETROS[1] else PERIMETROS[1]
        if otro == PERIMETROS[1] and pm.get("altas_derechos_uso") is None:
            return [], "el perímetro NIIF 16 necesita las cinco altas de derechos de uso y su fuente, que la configuración no declara"
        out.append((f"perímetro {otro.split(' ·')[0]}", {**conf, "PM1": {**pm, "perimetro_inversion": otro}}))
    elif clave == "PM1.roic_terminal":
        return [], "el ROIC terminal va ligado a la estructura (SR2 ↔ ROIC × f): se evalúa con las alternativas de PM1.estructura"
    elif clave == "N3.circulante":
        return [], "el circulante comercial son datos del balance: se acota como dato publicado (rango), no como alternativa de estructura"
    elif clave in NUMERICOS or clave == "PM1.parametro":
        return [], "parámetro numérico: se mueve en la combinación de la comprobación conjunta, no como alternativa"
    else:
        return [], f"{clave}: sin alternativas definidas en esta configuración"
    malas = [f"{et}: {' | '.join(validar(c))[:200]}" for et, c in out if validar(c)]
    if malas:
        # una alternativa que la propia configuración no admite no se calcula ni se descarta en silencio
        return [], "alternativas no válidas con estas entradas: " + "; ".join(malas)
    return [(et, _copy.deepcopy(c)) for et, c in out], None


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def aplicar(libro_in, libro_out, conf_path, cfg):
    conf = json.load(open(conf_path, encoding="utf-8"))
    faltas = validar(conf)
    if faltas:
        raise SystemExit("configuración económica no válida: " + " | ".join(faltas))
    sys.path.insert(0, cfg["plantilla"]["scripts_v63"])
    import inventario_entradas  # noqa: E402  (el de la plantilla activa)
    from v63_xml import LibroV63  # noqa: E402
    permitidas = inventario_entradas.conjunto_entradas()
    if HOJA not in permitidas:
        raise SystemExit(f"la plantilla activa no tiene la hoja «{HOJA}» (configuración V6.3): la configuración económica exige la V6.4 experimental")
    libro = LibroV63(libro_in)
    if HOJA not in libro.hojas():
        raise SystemExit(f"el libro {os.path.basename(libro_in)} no tiene la hoja «{HOJA}»")
    escritas = libro.escribir_celdas(celdas(conf, v641="B146" in permitidas[HOJA]), {HOJA: permitidas[HOJA]})
    libro.borrar_caches()
    libro.guardar(libro_out)
    r = subprocess.run([sys.executable, cfg["plantilla"]["verificador"], libro_out, cfg["plantilla"]["referencia"]], capture_output=True, text=True)
    return len(escritas), r.returncode, (r.stdout.strip().splitlines() or [r.stderr])[-1]


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    orden = sys.argv[1]
    if orden == "validar":
        conf = json.load(open(sys.argv[2], encoding="utf-8"))
        f = validar(conf)
        print("VÁLIDA · " + resumen(conf) if not f else "NO VÁLIDA:\n- " + "\n- ".join(f))
        return 0 if not f else 1
    if orden == "celdas":
        print(json.dumps(celdas(json.load(open(sys.argv[2], encoding="utf-8"))), ensure_ascii=False, indent=1))
        return 0
    if orden == "resumen":
        print(resumen(json.load(open(sys.argv[2], encoding="utf-8"))))
        return 0
    if orden == "aplicar":
        import config_v2  # noqa: E402
        cfg = config_v2.cargar(sys.argv[sys.argv.index("--config") + 1] if "--config" in sys.argv else None)
        n, rc, linea = aplicar(sys.argv[2], sys.argv[3], sys.argv[4], cfg)
        print(f"OK: {n} celdas de «{HOJA}» escritas en {os.path.basename(sys.argv[3])} · {linea}")
        return 0 if rc == 0 else 1
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
