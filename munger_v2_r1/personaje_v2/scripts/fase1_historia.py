#!/usr/bin/env python3
"""Pieza 7 · construye fase1_v63.json a partir de los informes anuales (texto/*.txt con marcas [PDF PAGE n]).

Procedimiento (generalización de lo hecho a mano con Rational, 3-nov-2026; DECISIONES.md):
  1. `preparar CARPETA`  elige un informe por ejercicio (los 10 más recientes con estados financieros), y escribe un prompt por
     año (prompts_generados/01_historia_<año>.md, agente Sonnet, en paralelo) y otro de metadatos (01_metadatos.md: precio,
     acciones, rf, sector, geografía; necesita web). Código 10 si falta alguna salida (lista en ESPERANDO_FASE1.md), 0 si están.
  2. Cada agente escribe fase1_partes/AR_<año>.json y comprueba su archivo con `comprobar-anio CARPETA AÑO`.
  3. `construir CARPETA` comprueba otra vez cada número en su página, consolida (regla: para cada año, la cifra MÁS RECIENTE
     publicada: el comparativo del informe siguiente si existe, que recoge reexpresiones y reclasificaciones; si no, la del propio
     informe), escribe historia_revision.md (todas las diferencias, ceros con evidencia, desconocidos, convenciones) y
     fase1_v63.json. Código 0 ok · 1 faltan datos esenciales o hay salidas inválidas (detalle en historia_revision.md) · 2 uso.

Convenciones (declaradas en las notas de cada partida y en historia_revision.md):
  - unidades a millones (mm) según `unidad` del informe; acciones a millones;
  - magnitudes de coste en positivo (capex, D&A, intereses, arrendamientos, I+D, SBC, impuestos); EBIT, beneficio y CFO con su signo;
  - adquisiciones = −(suma de lo impreso en el estado de flujos: pagos negativos, cobros positivos);
  - circulante (aumento = consume caja) = −(suma de las líneas de variación del circulante del estado de flujos);
  - tipo impositivo = impuestos ÷ resultado antes de impuestos (vacío si este ≤ 0);
  - caja = efectivo y equivalentes; + otros activos financieros corrientes SOLO si fase1_metadatos.json lo declara
    (convenciones.caja_incluye_otros_activos_financieros = true, con motivo);
  - un `cero` del agente (con motivo, página y `cita` literal de esa página) es 0 PENDIENTE de verificación (reparación H1,
    8-nov-2026): la cita prueba que el texto existe, no que hable de la partida; el 0 se conserva, se lista en historia_revision.md
    y las celdas del libro que dependen de él quedan «Dato no verificable». Un `cero` sin cita, o con una cita que no está en la
    página, es un error. Un null sin `cero` es desconocido (celda vacía), nunca 0;
  - fase1_decisiones.json (opcional, lo escribe solo una persona; ningún agente ni script) fija a mano una cifra con su fuente:
    {"partida": {"año": {"valor_mm": x, "fuente": "..."}}}. Para confirmar un cero pendiente la decisión tiene que llevar además
    `fecha` (AAAA-MM-DD) y `confirmado_por` (una persona), y la fuente tiene que citar página; si no, `construir` se detiene.

Redondeo (examen, jumbo_f, Historia!I17; rama producto/redondeo-exacto): cada importe de la Historia se calcula EXACTO (fracciones)
desde la cifra impresa, con su signo y su escala, y se redondea una sola vez a 4 decimales con ROUND de la hoja (mitad lejos de
cero). Antes se dividía en coma flotante y round() redondeaba el binario: 7.035.150 € daba 7,0351 en vez de 7,0352. Efectos al
reconstruir una Historia con el código nuevo (revisión independiente, C1; los expedientes ya construidos no cambian solos):
  - empates exactos en el 5.º decimal: jumbo y jumbo_b–f, I17 (2022) 7,0351 → 7,0352 y L14 (circulante 2025, suma de las líneas
    61,15855) 61,1585 → 61,1586;
  - el cero negativo desaparece (adquisiciones en cero de Vidrala, Viscofan y Jumbo): -0.0 → 0.0 en fase1_v63.json y «-0.000» →
    «0.000» en historia_revision.md; v63_xml escribe «0» en vez de «-0» en el libro, así que su huella cambia aunque el valor no;
  - `valor_sin_redondear` de calcular_entrada es el float de la suma exacta, no la suma float: cambia el último dígito binario
    (jumbo_b C46: 307.1729666666667 → 307.17296666666664, también en el texto de su `fuente`; el valor 307,173 no cambia);
  - la tabla de historia_revision.md muestra los valores nuevos (L14 = 61,159), todavía con el formato de Python (presentación);
  - las medias C46–C50 redondean dos veces, a propósito y como la hoja: la media exacta de los valores ya redondeados a 4 decimales
    de la Historia, redondeada a 3. La regla «una sola vez» vale para cada importe de la Historia y para calcular_entrada.
No cambia ninguna otra regla: tolerancia de los comparativos, umbral del EBIT, decisiones humanas (valor_mm tal cual), ceros
pendientes, regla de acciones ni numero() (que sigue dando float a motor_a_f1.py).
"""
import glob
import json
import os
import re
import sys
from fractions import Fraction

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.normpath(os.path.join(AQUI, ".."))
PARTIDAS = ["ventas", "ebit", "da", "beneficio_neto", "impuestos", "bai", "cfo", "capex", "adquisiciones", "circulante_lineas", "intereses",
            "intereses_financiacion", "arrendamientos_principal", "sbc", "id", "acciones_diluidas", "patrimonio", "deuda", "arrendamientos",
            "caja", "otros_activos_financieros", "pensiones", "minoritarios"]
CON_SIGNO = {"ebit", "ebit_derivado", "beneficio_neto", "bai", "cfo", "patrimonio"}
# v2.2 (Nike, 3-nov-2026): EBIT con una sola definición en los diez años. `ebit_derivado` = BAI − resultado financiero; si está
# los diez años se usa para todos, si no, el subtotal impreso; nunca se mezclan definiciones sin dejarlo en historia_revision.md
OPCIONALES = ["ebit_derivado"]
ESENCIALES = ["ventas", "ebit", "beneficio_neto", "cfo", "capex", "patrimonio", "caja", "acciones_diluidas"]
ESCALA = {"unidades": 1e-6, "miles": 1e-3, "millones": 1.0}
# (redondeo exacto) la misma escala, exacta: los importes de la Historia se calculan con fracciones desde la cifra impresa
ESCALA_EXACTA = {"unidades": Fraction(1, 10 ** 6), "miles": Fraction(1, 10 ** 3), "millones": Fraction(1)}
# (4.14, tercera empresa) también los informes en francés (Elis: Document de référence 2016 y Document d'enregistrement universel 2024)
CLAVE_ESTADOS = re.compile(r"balance sheet|statement of financial position|cash flow statement|statement of cash flows|estado de flujos|balance consolidado|estado de situaci"
                           r"|[ée]tat de la situation financi[èe]re|tableau des flux de tr[ée]sorerie|bilan consolid[ée]", re.I)


def paginas(ruta):
    t = open(ruta, encoding="utf-8", errors="replace").read()
    return {int(m.group(1)): m.group(2) for m in re.finditer(r"\[PDF PAGE (\d+)\]\n(.*?)(?=\[PDF PAGE \d+\]|\Z)", t, re.S)}


def norm(s):
    return re.sub(r"\s+", " ", str(s).replace("−", "-").replace("–", "-").replace("—", "-")).strip()


def _cifra_impresa(s):
    """(negativo, cifra decimal en texto sin separadores) de una cifra impresa; None si es un guion o está vacía (cero)."""
    s = norm(s)
    if s in ("-", "", "—"):
        return None
    neg = s.startswith("(") or s.startswith("-")
    d = s.strip("()-+ ")
    if re.fullmatch(r"\d{1,3}( \d{3})+([.,]\d{1,2})?", d):  # (14-nov) miles con espacio: «4 573,7» (informes en francés)
        d = d.replace(" ", "")
    if not re.fullmatch(r"\d{1,3}([.,]\d{3})*([.,]\d{1,2})?|\d+([.,]\d{1,2})?", d):
        raise ValueError(f"no numérico: {s!r}")
    m = re.fullmatch(r"(.*?)([.,])(\d{1,2})", d)
    if m and not re.fullmatch(r"\d{1,3}([.,]\d{3})+", d):  # decimales reales (p. ej. 11.37)
        return neg, re.sub(r"[.,]", "", m.group(1)) + "." + m.group(3)
    return neg, re.sub(r"[.,]", "", d)


def numero(s):
    """'1,125,977' · '(12.345)' · '-8,580' · '3.463' · '–' → float. Separadores de miles con coma o punto; sin decimales en los estados."""
    c = _cifra_impresa(s)
    if c is None:
        return 0.0
    v = float(c[1])
    return -v if c[0] else v


def numero_exacto(s):
    """(redondeo exacto) La misma lectura que numero(), pero exacta: la cifra impresa como fracción, sin pasar por coma flotante."""
    c = _cifra_impresa(s)
    if c is None:
        return Fraction(0)
    v = Fraction(c[1])
    return -v if c[0] else v


def exacto(x):
    """(redondeo exacto) Fracción exacta de un número: un float se toma por su representación decimal (repr), como el contraste de las
    entradas (verificacion_entradas). Un texto no es un número aquí (la cifra impresa se lee con numero_exacto).
    Límite (revisión independiente): sirve para un float que es una cifra decimal escrita (un valor de la Historia ya redondeado, un
    número de JSON), no para el resultado de aritmética float, que ya arrastra el error binario (redondear(2.0004999999999997, 3)
    da 2.0). Por eso a redondear solo llegan fracciones exactas o cifras así, nunca una suma o un cociente en float."""
    if isinstance(x, Fraction):
        return x
    if isinstance(x, bool) or not isinstance(x, (int, float)):
        raise TypeError(f"no es un número: {x!r}")
    if isinstance(x, float):
        if x != x or x in (float("inf"), float("-inf")):
            raise ValueError(f"no es un número finito: {x!r}")
        return Fraction(repr(x))
    return Fraction(x)


def redondear(x, n):
    """(redondeo exacto) ROUND de la hoja de cálculo (LibreOffice/Excel): n decimales, mitad lejos de cero, calculado EXACTO sobre la
    fracción (no sobre un float ya dividido, que convertía 7,03515 en 7,0351499… y lo redondeaba a 7,0351). Devuelve float."""
    fx = exacto(x)
    q = Fraction(10) ** n
    y = abs(fx) * q
    e = int(y)
    if y - e >= Fraction(1, 2):
        e += 1
    return float(Fraction(e if fx >= 0 else -e) / q)


def componentes(x):
    if x is None:
        return []
    if isinstance(x, dict):
        if isinstance(x.get("componentes"), list):
            return x["componentes"]
        return [x] if "impreso" in x else []
    return [c for c in x if isinstance(c, dict)]


def importe_completo(imp, texto):
    """Reparación H1 (R-b): el importe aparece como número completo, no como trozo de otro («6.0» no vale dentro de «196.0»,
    ni «7» dentro de «7,608»). imp y texto ya normalizados con norm(). (4.15 hito 2, séptima comprobación, X5) el apóstrofo de miles,
    ASCII o tipográfico, también es parte del número: «849,7» no vale dentro de «1'849,7» ni «849» dentro de «849’697»."""
    return re.search(r"(?<![\d.,])(?<!\d['’])" + re.escape(imp) + r"(?![\d.,'’]*\d)", texto) is not None


# Confirmación de un cero pendiente: solo por decisión humana registrada en fase1_decisiones.json (reparación H1, P2).
CAMPOS_CONFIRMACION = ("valor_mm", "fuente", "fecha", "confirmado_por")
NO_HUMANO = re.compile(r"\b(claude|ia|ai|agente|agent|sonnet|opus|haiku|fable|mythos|gpt|llm|modelo|bot|script|pipeline|autom[aá]tic\w*)\b", re.I)


def defecto_confirmacion(d):
    """None si la decisión confirma válidamente un cero pendiente; si no, el motivo. Exige valor, fuente con página,
    fecha ISO y una persona en confirmado_por (nunca un agente, un modelo o un script)."""
    if not isinstance(d, dict):
        return "no es un objeto"
    falt = [c for c in CAMPOS_CONFIRMACION if d.get(c) in (None, "")]
    if falt:
        return "faltan " + ", ".join(falt)
    if not isinstance(d["valor_mm"], (int, float)) or isinstance(d["valor_mm"], bool):
        return "valor_mm no numérico"
    if not re.search(r"\bp(?:\.|ág\.?|ágina|agina)\s*\d+", str(d["fuente"]), re.I):
        return "la fuente no cita página («p. N»)"
    if not re.fullmatch(r"20\d\d-[01]\d-[0-3]\d", str(d["fecha"])):
        return "fecha no ISO (AAAA-MM-DD)"
    if NO_HUMANO.search(str(d["confirmado_por"])):
        return f"confirmado_por {d['confirmado_por']!r} no es una persona (la IA no confirma ceros)"
    return None


# Celdas de datos de Análisis que dependen de la Historia (reparación H1, cierre): partidas de la Historia (claves de
# historia.partidas) y ventana de años («fcf» = los anios_fcf_base últimos; n = los n últimos). Un cero pendiente en esa
# ventana hace pendiente la celda, venga de donde venga su valor, salvo respaldo independiente explícito y válido.
DEP_ANALISIS = {"C46": (("cfo",), "fcf"), "C47": (("capex",), "fcf"), "C48": (("intereses_financiacion",), "fcf"),
                "C49": (("arrendamientos_principal",), "fcf"), "C50": (("sbc",), "fcf"),
                "C24": (("ebit", "tipo_impositivo", "patrimonio", "deuda", "arrendamientos", "caja"), 5),
                "C26": (("cfo", "beneficio_neto"), "fcf"), "C28": (("acciones_diluidas",), 6),
                "C33": (("deuda", "arrendamientos", "caja", "ebit", "da"), 1)}


def pendientes_celda(celda, partidas, anios, n_fcf):
    """Años con cero pendiente de verificación (historia.partidas.<p>.pendientes_verificacion) en la ventana de la celda."""
    nombres, vent = DEP_ANALISIS[celda]
    n = int(n_fcf or 3) if vent == "fcf" else int(vent)
    ventana = set(anios[-n:]) if anios else set()
    out = set()
    for nm in nombres:
        p = partidas.get(nm)
        out |= {y for y in ((p.get("pendientes_verificacion") or []) if isinstance(p, dict) else []) if y in ventana}
    return sorted(out)


def defecto_independiente(ind):
    """None si `independiente` es un respaldo explícito y trazable de una fuente independiente de la Historia: fuente con
    página, fecha ISO, una persona en confirmado_por (nunca un agente, modelo o script) y motivo. Si no, el motivo del rechazo."""
    if not isinstance(ind, dict):
        return "no es un objeto con fuente, fecha, confirmado_por y motivo"
    falt = [c for c in ("fuente", "fecha", "confirmado_por", "motivo") if ind.get(c) in (None, "")]
    if falt:
        return "faltan " + ", ".join(falt)
    if not re.search(r"\bp(?:\.|ág\.?|ágina|agina)\s*\d+", str(ind["fuente"]), re.I):
        return "la fuente no cita página («p. N»)"
    if not re.fullmatch(r"20\d\d-[01]\d-[0-3]\d", str(ind["fecha"])):
        return "fecha no ISO (AAAA-MM-DD)"
    if NO_HUMANO.search(str(ind["confirmado_por"])):
        return f"confirmado_por {ind['confirmado_por']!r} no es una persona"
    return None


# ---------------------------------------------------------------- comprobar
def incoherencias_acciones(anios, valores, acciones_meta=None, factor=10.0):
    """(examen, Ahold; revisión independiente del parche de la unidad, hallazgo 1) La serie de acciones diluidas (millones) no puede
    saltar más de `factor` veces entre dos años con dato, ni el último año alejarse más de `factor` veces de las acciones de los
    metadatos (Análisis!C55): es la huella de una unidad mal inferida (miles por millones o al revés), que antes pasaba en silencio.
    Devuelve la lista de incoherencias (vacía si la serie es coherente). No juzga recompras ni ampliaciones reales: un salto real de
    más de diez veces en un año también se detiene y hay que explicarlo declarando la unidad y revisando la serie."""
    out = []
    pares = [(a, v) for a, v in zip(anios, valores) if isinstance(v, (int, float)) and not isinstance(v, bool) and v > 0]
    for (a0, v0), (a1, v1) in zip(pares, pares[1:]):
        if max(v0, v1) / min(v0, v1) > factor:
            out.append(f"acciones_diluidas: salto de {v0:g} ({a0}) a {v1:g} ({a1}) millones, más de {factor:g} veces (¿unidad mal inferida? declare «unidad» en la partida de cada año)")
    try:
        m = float((acciones_meta or {}).get("valor")) if isinstance(acciones_meta, dict) else None
    except (TypeError, ValueError):
        m = None
    if m and m > 0 and pares:
        a1, v1 = pares[-1]
        if max(m, v1) / min(m, v1) > factor:
            out.append(f"acciones_diluidas: {v1:g} millones en {a1} frente a {m:g} millones en los metadatos (Análisis!C55): más de {factor:g} veces (¿unidad mal inferida?)")
    return out


def defecto_acciones_meta(ac):
    """(examen, zoetis_t1c, Análisis!C55; rama producto/minoritarios-acciones) Las acciones de los metadatos son un número de acciones,
    no un importe: el redondeo del libro a 3 decimales en mm no vale para ellas (verificacion_entradas, N4). Si los metadatos traen la
    cifra impresa («impreso», con «unidad»: unidades por omisión, miles o millones), «valor» tiene que ser EXACTAMENTE esa cifra en
    millones, con todos sus decimales (424.927.535 acciones → 424.927535, no 424,928). Lista de defectos; vacía si no hay o si los
    metadatos no traen «impreso» (metadatos anteriores a esta regla: sin cambio, la precisión no se comprueba)."""
    if not isinstance(ac, dict) or ac.get("impreso") is None:
        return []
    imp, uni = ac.get("impreso"), ac.get("unidad", "unidades")
    if not isinstance(imp, str):
        return [f"acciones_diluidas de los metadatos: «impreso» {imp!r} tiene que ser la cifra tal como se imprime (texto)"]
    if uni not in ESCALA_EXACTA:
        return [f"acciones_diluidas de los metadatos: unidad {uni!r} no es una de {list(ESCALA_EXACTA)}"]
    try:
        n = numero_exacto(imp)
    except ValueError as e:
        return [f"acciones_diluidas de los metadatos: {e}"]
    exacta = n * ESCALA_EXACTA[uni]
    if exacta <= 0:
        return [f"acciones_diluidas de los metadatos: «impreso» {imp!r} no es un número positivo de acciones"]
    v = ac.get("valor")
    try:
        ok = exacto(v) == exacta
    except (TypeError, ValueError):
        ok = False
    if not ok:
        return [f"acciones_diluidas de los metadatos (Análisis!C55): valor {v!r} no es la cifra impresa «{imp}» ({uni}) en millones = "
                f"{float(exacta)!r}, con todos sus decimales (un número de acciones no se redondea)"]
    return []


def comprobar_anio(carpeta, anio, pendientes=None):
    """Errores de AR_<año>.json (lista vacía = sin errores). Reparación H1 (8-nov-2026):
      R-a  la `linea` normalizada tiene que estar en su página (sin vía alternativa);
      R-b  el `impreso` tiene que figurar como importe completo en la línea y en la página;
      R-c  un `cero` necesita `motivo`, página existente y `cita` literal (≤ 200 caracteres) que esté en esa página; sin cita,
           o con una cita que no está, es un error. Con la cita presente el cero queda PENDIENTE de verificación (la cita prueba
           que el texto existe, no que hable de esa partida): si se pasa la lista `pendientes`, se añade a ella un registro por
           cero; nunca cuenta como comprobado."""
    ruta = os.path.join(carpeta, "fase1_partes", f"AR_{anio}.json")
    if not os.path.exists(ruta):
        return [f"falta {ruta}"]
    try:
        d = json.load(open(ruta, encoding="utf-8"))
    except json.JSONDecodeError as e:
        return [f"AR_{anio}.json no es JSON: {e}"]
    err = []
    arch = d.get("archivo")
    if not arch or not os.path.exists(os.path.join(carpeta, "texto", arch)):
        return [f"AR_{anio}: «archivo» ausente o inexistente en texto/: {arch!r}"]
    P = {k: norm(v) for k, v in paginas(os.path.join(carpeta, "texto", arch)).items()}
    if d.get("unidad") not in ESCALA:
        err.append(f"unidad {d.get('unidad')!r} no es una de {list(ESCALA)}")
    falt = [k for k in PARTIDAS if k not in (d.get("partidas") or {})]
    if falt:
        err.append("faltan claves: " + ", ".join(falt))
    for k, p in (d.get("partidas") or {}).items():
        if not isinstance(p, dict):
            err.append(f"{k}: no es un objeto")
            continue
        for cual in ("actual", "anterior"):
            for c in componentes(p.get(cual)):
                imp, pg, lin = c.get("impreso"), c.get("pagina"), c.get("linea")
                if c.get("signo", 1) not in (1, -1):
                    err.append(f"{k} {cual}: signo {c.get('signo')!r} no es 1 ni -1")
                try:
                    numero(imp)
                except Exception as e:
                    err.append(f"{k} {cual}: {e}")
                    continue
                if not isinstance(pg, int) or pg not in P:
                    err.append(f"{k} {cual}: página {pg!r} inexistente")
                    continue
                if not lin or not importe_completo(norm(imp), norm(lin)):
                    err.append(f"{k} {cual}: «{imp}» no está en su línea como importe completo")
                elif norm(lin) not in P[pg]:
                    err.append(f"{k} {cual}: la línea «{norm(lin)[:80]}» no está en la página {pg}")
                elif not importe_completo(norm(imp), P[pg]):
                    err.append(f"{k} {cual}: «{imp}» no está en la página {pg} como importe completo")
        if k == "acciones_diluidas" and p.get("unidad") is not None and not (isinstance(p.get("unidad"), str) and p["unidad"] in ESCALA):
            err.append(f"acciones_diluidas: unidad {p.get('unidad')!r} no es una de {list(ESCALA)} (unidades, miles o millones de acciones)")
        cz = p.get("cero")
        if cz is not None:
            if not isinstance(cz, dict) or not cz.get("motivo") or cz.get("pagina") not in P:
                err.append(f"{k}: «cero» sin motivo o con página inexistente")
            elif not isinstance(cz.get("cita"), str) or not norm(cz["cita"]):
                err.append(f"{k}: «cero» sin «cita» literal de la página {cz.get('pagina')}")
            elif len(norm(cz["cita"])) > 200:
                err.append(f"{k}: la «cita» del cero pasa de 200 caracteres")
            elif norm(cz["cita"]) not in P[cz["pagina"]]:
                err.append(f"{k}: la «cita» del cero no está en la página {cz['pagina']}")
            elif pendientes is not None and not componentes(p.get("actual")):
                pendientes.append({"partida": k, "anio": int(d.get("anio") or anio), "archivo": arch, "pagina": cz["pagina"],
                                   "cita": norm(cz["cita"]), "motivo": cz["motivo"]})
    return err


# ---------------------------------------------------------------- preparar
def elegir_fuentes(carpeta):
    fijo = os.path.join(carpeta, "fase1_fuentes.json")
    if os.path.exists(fijo):
        return {int(k): v for k, v in json.load(open(fijo, encoding="utf-8")).items()}
    por_anio = {}
    for ruta in sorted(glob.glob(os.path.join(carpeta, "texto", "*.txt"))):
        nombre = os.path.basename(ruta)
        anios = re.findall(r"(?<!\d)(20\d\d)(?!\d)", nombre)
        if not anios:
            continue
        txt = open(ruta, encoding="utf-8", errors="replace").read()
        puntos = len(CLAVE_ESTADOS.findall(txt))
        if puntos == 0:
            continue
        a = int(anios[-1])
        if a not in por_anio or puntos > por_anio[a][1]:
            por_anio[a] = (nombre, puntos)
    ult = sorted(por_anio)[-10:]
    out = {a: por_anio[a][0] for a in ult}
    json.dump({str(a): f for a, f in out.items()}, open(fijo, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return out


def listas_plantilla(carpeta):
    """Vuelca los nombres válidos de sector (hoja Sector) y de país/región (hoja Riesgo país) para el agente de metadatos."""
    sys.path.insert(0, AQUI)
    import config_v2
    import openpyxl
    cfg = config_v2.cargar()
    wb = openpyxl.load_workbook(cfg["plantilla"]["archivo"], read_only=True)
    sect = [r[0] for r in wb["Sector"].iter_rows(min_row=1, values_only=True) if r and isinstance(r[0], str) and r[0].strip()]
    paises = [r[0] for r in wb["Riesgo país"].iter_rows(min_row=6, values_only=True) if r and isinstance(r[0], str) and r[0].strip()]
    with open(os.path.join(carpeta, "fase1_listas.md"), "w", encoding="utf-8") as f:
        f.write("# Nombres válidos de la Plantilla V6.3\n\n## Sector de Damodaran (hoja Sector, columna A)\n" + "\n".join(f"- {s}" for s in sect)
                + "\n\n## País o región (hoja Riesgo país, columna A)\n" + "\n".join(f"- {p}" for p in paises) + "\n")


def preparar(carpeta, empresa):
    fuentes = elegir_fuentes(carpeta)
    if len(fuentes) < 3:
        print(f"solo {len(fuentes)} informes con estados financieros en texto/ (hacen falta los de 10 años; mínimo 3)")
        return 1
    os.makedirs(os.path.join(carpeta, "fase1_partes"), exist_ok=True)
    os.makedirs(os.path.join(carpeta, "prompts_generados"), exist_ok=True)
    plantilla = open(os.path.join(RAIZ, "prompts", "historia_anio.md"), encoding="utf-8").read()
    pendientes = []
    for a, arch in sorted(fuentes.items()):
        if os.path.exists(os.path.join(carpeta, "fase1_partes", f"AR_{a}.json")) and not comprobar_anio(carpeta, a):
            continue
        txt = (plantilla.replace("{CARPETA}", carpeta).replace("{EMPRESA}", empresa).replace("{ANIO}", str(a))
               .replace("{ARCHIVO}", arch).replace("{RAIZ}", RAIZ))
        errs = comprobar_anio(carpeta, a) if os.path.exists(os.path.join(carpeta, "fase1_partes", f"AR_{a}.json")) else []
        if errs:
            txt += "\n\n## CORRECCIÓN\nTu salida anterior no pasa la comprobación:\n" + "\n".join(f"- {e}" for e in errs[:40]) + "\n"
        p = os.path.join(carpeta, "prompts_generados", f"01_historia_{a}.md")
        open(p, "w", encoding="utf-8").write(txt)
        pendientes.append((f"historia {a}", p, f"fase1_partes/AR_{a}.json"))
    if not os.path.exists(os.path.join(carpeta, "fase1_metadatos.json")):
        listas_plantilla(carpeta)
        txt = open(os.path.join(RAIZ, "prompts", "metadatos_fase1.md"), encoding="utf-8").read()
        txt = txt.replace("{CARPETA}", carpeta).replace("{EMPRESA}", empresa).replace("{ANIOS}", ", ".join(str(a) for a in sorted(fuentes)))
        p = os.path.join(carpeta, "prompts_generados", "01_metadatos.md")
        open(p, "w", encoding="utf-8").write(txt)
        pendientes.append(("metadatos", p, "fase1_metadatos.json"))
    if pendientes:
        with open(os.path.join(carpeta, "ESPERANDO_FASE1.md"), "w", encoding="utf-8") as f:
            f.write(f"# ESPERANDO · fase 1 (Historia de 10 años y metadatos) · {empresa}\n\nLanza estos agentes EN PARALELO, cada uno con su prompt como instrucción "
                    "(historia: Sonnet, esfuerzo medio; metadatos: Sonnet, esfuerzo medio, con búsqueda web). Cuando todos hayan escrito su salida, vuelve a lanzar pipeline.py.\n\n")
            for n, p, s in pendientes:
                f.write(f"- **{n}** · prompt `{os.path.relpath(p, carpeta)}` → escribe `{s}`\n")
        print(f"ESPERANDO fase 1: {len(pendientes)} agentes ({', '.join(n for n, _, _ in pendientes)})")
        return 10
    if os.path.exists(os.path.join(carpeta, "ESPERANDO_FASE1.md")):
        os.remove(os.path.join(carpeta, "ESPERANDO_FASE1.md"))
    return 0


# ---------------------------------------------------------------- construir
OPERACIONES_CALCULO = ("media", "suma")


def _cifra_publicada_componente(nombre, anio, cmp, v):
    """(4.15, hito 2, R415-SIGNO) (cifra publicada, transformación) de un componente de un cálculo declarado. Sin «valor_fuente», la cifra
    publicada es «valor» y no hay transformación (None). Con «valor_fuente», exige «signo» ±1 y «tratamiento», y valor = signo ×
    valor_fuente exactamente (en su representación decimal: ni redondeo ni escala; un cambio de escala no es una conversión de signo)."""
    claves = ("valor_fuente", "signo", "tratamiento")
    if not any(k in cmp for k in claves):
        return v, None
    vf, sg, tr = cmp.get("valor_fuente"), cmp.get("signo"), cmp.get("tratamiento")
    if not isinstance(vf, (int, float)) or isinstance(vf, bool) or vf != vf or vf in (float("inf"), float("-inf")):
        raise ValueError(f"el componente {nombre} de {anio}: «valor_fuente» {vf!r} no es la cifra publicada (un número)")
    if sg not in (1, -1) or isinstance(sg, bool):
        raise ValueError(f"el componente {nombre} de {anio}: «signo» {sg!r} no es ±1")
    if not str(tr or "").strip():
        raise ValueError(f"el componente {nombre} de {anio}: la transformación de la cifra publicada {vf!r} no declara «tratamiento»")
    from fractions import Fraction
    if Fraction(repr(float(v))) != sg * Fraction(repr(float(vf))):
        raise ValueError(f"el componente {nombre} de {anio}: valor {v!r} ≠ signo × valor_fuente = {sg * vf!r} (la transformación declarada no lo reproduce)")
    return vf, (sg, str(tr).strip())


def calcular_entrada(celda, d, H, anios, carpeta=None):
    """(4.15) Valor de una entrada de Análisis desde su `calculo` declarado:
    {"operacion": "media"|"suma", "anios": [AAAA, …], "terminos": [{"partida": <fila de la Historia>, "signo": ±1} | {"componente": <nombre>, "signo": ±1}],
     "componentes": {<nombre>: {"AAAA": {"valor": x, "fuente": "texto/…", "pagina": n, "cita": "…"
                                          [, "valor_fuente": y, "signo": ±1, "tratamiento": "…"]}}}, "decision": "…", "redondeo": 3}
    Cada año suma sus términos; la operación agrega los años. Un año sin dato, un componente sin fuente o un «valor» declarado que no
    coincide con el calculado es un error (no se rellena ni se redondea en silencio).
    (Revisión independiente de la 4.15, hallazgos 7 y 13) Los años tienen que ser enteros distintos; el redondeo, un entero ≥ 3 (el del libro
    por defecto), y se dice en la fuente; con `carpeta`, cada componente se contrasta con su fuente: la cita tiene que estar en la página PDF
    citada del texto conservado y contener el valor (verificacion_entradas). La entrada hereda los ceros pendientes de verificación (H1) de
    las partidas y años que usa (`pendiente_verificacion`). Cualquier defecto es un ValueError.
    (4.15, hito 2, R415-SIGNO) La cita se contrasta con la cifra PUBLICADA y su signo. Si el componente usa otra cifra que la publicada (p.
    ej. la magnitud positiva de un pago publicado «(130,8)»), lo declara: «valor_fuente» (la cifra publicada, con su signo), «signo» (±1)
    y «tratamiento» (por qué), con valor = signo × valor_fuente exactamente; la transformación declarada sigue siendo válida. Sin esa
    declaración, «valor» es la cifra publicada: una magnitud positiva frente a un pago publicado entre paréntesis es un error."""
    cal = d["calculo"]
    if not isinstance(cal, dict):
        raise ValueError("el cálculo no es un objeto")
    op = cal.get("operacion")
    if op not in OPERACIONES_CALCULO:
        raise ValueError(f"operación {op!r} no admitida ({OPERACIONES_CALCULO})")
    sel = cal.get("anios") or []
    if not isinstance(sel, list) or not sel or any(not isinstance(a, int) or isinstance(a, bool) for a in sel):
        raise ValueError(f"años {sel!r}: tienen que ser una lista de años enteros")
    if len(set(sel)) != len(sel):
        raise ValueError(f"años repetidos {sel}")
    if any(a not in anios for a in sel):
        raise ValueError(f"años {sel} fuera de la Historia {anios}")
    red = cal.get("redondeo", 3)
    if not isinstance(red, int) or isinstance(red, bool) or red < 3:
        raise ValueError(f"redondeo {red!r}: tiene que ser un entero ≥ 3 (el libro trabaja con 3 decimales en mm)")
    terms = cal.get("terminos") or []
    if not isinstance(terms, list) or not terms:
        raise ValueError("sin términos")
    comps = cal.get("componentes") or {}
    if not isinstance(comps, dict):
        raise ValueError("los componentes no son un objeto")
    VE = None
    if carpeta is not None:
        import verificacion_entradas as VE  # noqa: N811
    por_anio, fuentes, pend = [], [], set()
    for a in sel:
        i = anios.index(a)
        tot = Fraction(0)  # (redondeo exacto) suma exacta de las cifras declaradas (repr decimal), redondeada una vez con ROUND de la hoja
        for t in terms:
            if not isinstance(t, dict):
                raise ValueError(f"término no válido: {t!r}")
            sg = t.get("signo", 1)
            if sg not in (1, -1) or isinstance(sg, bool):
                raise ValueError(f"signo {sg!r} no es ±1")
            if t.get("partida"):
                p = H.get(t["partida"])
                vals = (p.get("valores") if isinstance(p, dict) else p) if p is not None else None
                v = vals[i] if vals and i < len(vals) else None
                if not isinstance(v, (int, float)) or isinstance(v, bool):
                    raise ValueError(f"la Historia no tiene {t['partida']} de {a}")
                if isinstance(p, dict) and a in (p.get("pendientes_verificacion") or []):
                    pend.add(a)
                fuentes.append(f"{a} {t['partida']} (Historia) {v}")
            elif t.get("componente"):
                serie = comps.get(t["componente"])
                if serie is not None and not isinstance(serie, dict):
                    raise ValueError(f"el componente {t['componente']!r} no es un objeto {{año: {{valor, fuente, página, cita}}}}")
                cmp = (serie or {}).get(str(a)) or {}
                if not isinstance(cmp, dict):  # (4.15, segunda revisión, residuo del hallazgo 13) nunca un AttributeError
                    raise ValueError(f"el componente {t['componente']} de {a} no es un objeto {{valor, fuente, página, cita}}")
                v = cmp.get("valor")
                if not isinstance(v, (int, float)) or isinstance(v, bool) or not str(cmp.get("fuente") or "").strip() or cmp.get("pagina") in (None, ""):
                    raise ValueError(f"el componente {t['componente']} de {a} no tiene valor, fuente y página")
                publicado, transf = _cifra_publicada_componente(t["componente"], a, cmp, v)
                if VE is not None:
                    ruta = VE._ruta_fuente(carpeta, cmp["fuente"])
                    if ruta is None or not ruta.lower().endswith(".txt"):
                        raise ValueError(f"el componente {t['componente']} de {a}: su fuente {cmp['fuente']!r} no es un texto conservado en el expediente")
                    estado, pag = VE._pagina_examinable(ruta, cmp["pagina"])
                    if estado != "ok":
                        raise ValueError(f"el componente {t['componente']} de {a}: {pag}")
                    if not VE._norm_txt(cmp.get("cita")) or VE._norm_txt(cmp.get("cita")) not in VE._norm_txt(pag):
                        raise ValueError(f"el componente {t['componente']} de {a}: la cita no está en la página {cmp['pagina']}")
                    est_c, det_c = VE._cita_cifra(cmp.get("cita"), publicado, pag)
                    if est_c != "ok":
                        pista = (" Si el cálculo usa otra cifra que la publicada (p. ej. la magnitud de un pago publicado entre paréntesis), declara "
                                 "«valor_fuente» (la cifra publicada con su signo), «signo» y «tratamiento»." if est_c == "signo_distinto" and transf is None else "")
                        raise ValueError(f"el componente {t['componente']} de {a}: la cita no contiene la cifra publicada {publicado!r} con su signo "
                                         f"({est_c}: {det_c}).{pista}")
                fuentes.append(f"{a} {t['componente']} {v}" + (f" (= {transf[0]:+d} × {publicado!r} publicado: {transf[1]})" if transf else "")
                               + f" ({cmp['fuente']} p.{cmp['pagina']})")
            else:
                raise ValueError(f"término sin partida ni componente: {t}")
            tot += sg * exacto(v)
        por_anio.append(tot)
    bruto_exacto = sum(por_anio, Fraction(0)) / len(por_anio) if op == "media" else sum(por_anio, Fraction(0))
    val = redondear(bruto_exacto, red)
    bruto = float(bruto_exacto)
    if d.get("valor") is not None and not (isinstance(d["valor"], (int, float)) and not isinstance(d["valor"], bool) and abs(d["valor"] - val) <= 1e-9 * max(1.0, abs(val))):
        raise ValueError(f"el valor declarado {d['valor']!r} no es el calculado {val!r}")
    desc = " ".join(("+" if t.get("signo", 1) == 1 else "−") + " " + (t.get("partida") or t.get("componente")) for t in terms).lstrip("+ ")
    out = {k: v for k, v in d.items() if k != "calculo"}
    out.update(valor=val, calculo=cal, periodo=d.get("periodo") or f"{min(sel)}–{max(sel)}", unidad=d.get("unidad") or "mm", valor_sin_redondear=bruto,
               fuente=(f"Cálculo declarado ({op} {sel[0]}–{sel[-1]} de: {desc}; redondeo a {red} decimales; sin redondear {bruto!r}): " + "; ".join(fuentes))  # (4.15, hito 2, H10) sin recortar: se perdían la fuente y la página del último año
               + (f". {cal['decision']}" if cal.get("decision") else ""))
    if pend:
        out["pendiente_verificacion"] = sorted(set(out.get("pendiente_verificacion") or []) | pend)
        out["nota"] = ((out.get("nota") or "") + f" Cálculo con ceros pendientes de verificación en {', '.join(map(str, sorted(pend)))} (H1).").strip()
    return out


def construir(carpeta):
    fuentes = elegir_fuentes(carpeta)
    anios = sorted(fuentes)
    rev, problemas = [], []
    pend_ar = []  # ceros con cita presente: PENDIENTES de verificación (reparación H1)
    for a in anios:
        for e in comprobar_anio(carpeta, a, pend_ar):
            problemas.append(f"AR_{a}: {e}")
    pend_ar_idx = {(x["partida"], x["anio"]): x for x in pend_ar}
    meta_p = os.path.join(carpeta, "fase1_metadatos.json")
    if not os.path.exists(meta_p):
        problemas.append("falta fase1_metadatos.json")
    if problemas:
        open(os.path.join(carpeta, "historia_revision.md"), "w", encoding="utf-8").write("# Revisión de la Historia · SALIDAS INVÁLIDAS\n\n" + "\n".join(f"- {p}" for p in problemas) + "\n")
        print("\n".join(problemas[:30]))
        return 1
    meta = json.load(open(meta_p, encoding="utf-8"))
    dec_p = os.path.join(carpeta, "fase1_decisiones.json")
    dec = json.load(open(dec_p, encoding="utf-8")) if os.path.exists(dec_p) else {}
    AR = {a: json.load(open(os.path.join(carpeta, "fase1_partes", f"AR_{a}.json"), encoding="utf-8")) for a in anios}

    def leer(a, k, cual):
        """(valor_mm, fuente, cero_motivo) del informe a, columna cual; valor None si no hay. (redondeo exacto) valor_mm es una fracción
        exacta: la cifra impresa (texto) por su signo y su escala, sin coma flotante; se redondea una sola vez, al escribir la serie."""
        d = AR[a]
        p = (d["partidas"] or {}).get(k) or {}
        esc = ESCALA_EXACTA[d["unidad"]]
        comps = componentes(p.get(cual))
        if comps:
            if k == "circulante_lineas":
                v = -sum((numero_exacto(c["impreso"]) * c.get("signo", 1) for c in comps), Fraction(0))
            else:
                v = sum((numero_exacto(c["impreso"]) * c.get("signo", 1) for c in comps), Fraction(0))
            if k == "acciones_diluidas":
                # (examen, Ahold) la unidad declarada por el extractor manda: con más de 1.000 millones de acciones («1,031» en
                # millones) la regla por tamaño las tomaba como miles y las dividía por mil. Sin declaración, la regla de siempre.
                if isinstance(p.get("unidad"), str) and p["unidad"] in ESCALA_EXACTA:
                    v = v * ESCALA_EXACTA[p["unidad"]]
                else:
                    v = v / 10 ** 6 if abs(v) > 10 ** 5 else (v / 10 ** 3 if abs(v) > 10 ** 3 else v)
            else:
                v = v * esc
            pags = sorted({c["pagina"] for c in comps})
            return v, f"{d['archivo']} p.{','.join(map(str, pags))}", None
        cz = p.get("cero")
        if cz and cual == "actual":
            return Fraction(0), f"{d['archivo']} p.{cz['pagina']} (cero: {cz['motivo']})", cz["motivo"]
        return None, None, None

    def ajustar(k, v):
        if v is None:
            return None
        if k in CON_SIGNO or k == "circulante_lineas":
            return v
        if k == "adquisiciones":
            return -v
        return abs(v)

    serie, fuente, notas_k = {}, {}, {}
    pend_usados, confirmados, dec_invalidas = {}, [], []
    for k in PARTIDAS + OPCIONALES:
        serie[k], fuente[k] = [], []
        for a in anios:
            v, f, cz = leer(a, k, "actual")
            usado = "propio"
            if a + 1 in AR:
                v2, f2, _ = leer(a + 1, k, "anterior")
                if v2 is not None:
                    if v is not None and abs(abs(float(v2)) - abs(float(v))) > max(0.0005 * max(abs(float(v)), 1), 0.0005):
                        rev.append(f"- **{k} {a}**: informe {a} = {redondear(ajustar(k, v), 3)} · comparativo del informe {a + 1} = {redondear(ajustar(k, v2), 3)} → se usa el más reciente ({f2}). Reexpresión, reclasificación o definición distinta: revisar si la diferencia es grande. Informe {a + 1}: «{(AR[a + 1].get('reexpresion') or 'sin nota de reexpresión')[:200]}»")
                    v, f, usado, cz = v2, f2 + " (comparativo del informe siguiente)", "siguiente", None
            # H1: el valor usado es un cero del propio informe con cita sin contrastar → PENDIENTE, salvo decisión humana válida
            pendiente = bool(cz) and (k, a) in pend_ar_idx
            d_k = dec.get(k) if isinstance(dec.get(k), dict) else {}
            if pendiente and str(a) in d_k:
                defecto = defecto_confirmacion(d_k[str(a)])
                if defecto:
                    dec_invalidas.append(f"{k} {a}: la decisión no confirma el cero pendiente ({defecto})")
                else:
                    pendiente = False
                    dd = d_k[str(a)]
                    confirmados.append({"partida": k, "anio": a, "valor_mm": dd["valor_mm"], "fuente": dd["fuente"], "fecha": dd["fecha"],
                                        "confirmado_por": dd["confirmado_por"], "cita_original": pend_ar_idx[(k, a)]["cita"]})
            if str(a) in d_k:
                dd = d_k[str(a)]
                v, f = dd["valor_mm"], dd["fuente"] + " (fase1_decisiones.json)"
                if dd.get("confirmado_por") and dd.get("fecha"):
                    f += f" · decisión de {dd['confirmado_por']} el {dd['fecha']}"
                rev.append(f"- **{k} {a}**: fijado a mano en fase1_decisiones.json = {v} ({f})")
                serie[k].append(v)
            else:
                serie[k].append(None if v is None else redondear(ajustar(k, v), 4))  # (redondeo exacto) ROUND de la hoja sobre la cifra exacta
            if pendiente:
                pend_usados.setdefault(k, []).append(a)
                f = (f or "") + " (CERO PENDIENTE DE VERIFICACIÓN: cita sin contrastar)"
            fuente[k].append(f or "desconocido")
    # EBIT homogéneo (v2.2)
    ebit_metodo = "impreso"
    if all(v is not None for v in serie["ebit_derivado"]):
        difs = [(a, i, d) for a, i, d in zip(anios, serie["ebit"], serie["ebit_derivado"]) if i is not None and abs(i - d) > max(0.005 * abs(d), 0.001)]
        for a, i, d in difs:
            rev.append(f"- **ebit {a}**: subtotal impreso = {redondear(i, 3)} · derivado (BAI − resultado financiero) = {redondear(d, 3)} → se usa el derivado los diez años (misma definición)")
        serie["ebit"], fuente["ebit"], ebit_metodo = serie["ebit_derivado"], fuente["ebit_derivado"], "derivado"
    elif any(v is not None for v in serie["ebit_derivado"]) or any(v is None for v in serie["ebit"]):
        rev.append("- **AVISO EBIT**: no hay EBIT derivado los diez años; se usa el subtotal impreso donde existe. Revisar que la definición sea la misma todos los años.")
    # tipo impositivo
    tipo = []
    for i in range(len(anios)):
        t, b = serie["impuestos"][i], serie["bai"][i]
        tipo.append(redondear(exacto(t) / exacto(b), 4) if t is not None and b not in (None, 0) and b > 0 else None)
    caja = list(serie["caja"])
    conv = (meta.get("convenciones") or {})
    if conv.get("caja_incluye_otros_activos_financieros"):
        caja = [None if c is None else redondear(exacto(c) + exacto(o or 0), 4) for c, o in zip(serie["caja"], serie["otros_activos_financieros"])]
    H = {}

    origen = {"circulante": "circulante_lineas"}

    def aviso_pend(anios_p):
        return (f" CERO PENDIENTE DE VERIFICACIÓN en {', '.join(map(str, anios_p))}: el informe no imprime cifra y la cita que lo"
                " respalda no se ha contrastado con la partida (reparación H1). El 0 se conserva; solo una decisión humana registrada en"
                " fase1_decisiones.json (valor, fuente con página, fecha y persona) lo confirma.") if anios_p else ""

    def poner(clave, vals, fu, nota, pend=None):
        # notas de los lectores (lo que vieron: reexpresiones, partidas extraordinarias, ambigüedades), las más recientes primero
        k = origen.get(clave, clave)
        lect = [f"{a}: {AR[a]['partidas'].get(k, {}).get('nota')}" for a in sorted(anios, reverse=True) if isinstance(AR[a]["partidas"].get(k), dict) and AR[a]["partidas"][k].get("nota")]
        if k in dec and dec[k].get("_nota"):
            lect.insert(0, dec[k]["_nota"])
        extra = (" Notas de los lectores: " + " | ".join(lect))[:700] if lect else ""
        anios_p = sorted(set(pend if pend is not None else pend_usados.get(k, [])))
        H[clave] = {"valores": vals, "fuente": "; ".join(f"{a} {s}" for a, s in zip(anios, fu)), "pagina": None, "nota": nota + aviso_pend(anios_p) + extra}
        if anios_p:
            H[clave]["pendientes_verificacion"] = anios_p
    base = "Construido por fase1_historia.py: cifra más reciente publicada de cada año (comparativo del informe siguiente cuando existe)."
    for k in ["ventas", "ebit", "da", "beneficio_neto"]:
        poner(k, serie[k], fuente[k], base + (" EBIT = resultado antes de impuestos − resultado financiero, la misma definición los diez años (v2.2)." if k == "ebit" and ebit_metodo == "derivado" else ""))
    pend_tipo = sorted(set(pend_usados.get("impuestos", [])) | set(pend_usados.get("bai", [])))
    H["tipo_impositivo"] = {"valores": tipo, "fuente": "impuestos ÷ resultado antes de impuestos; " + "; ".join(f"{a} {x} / {y}" for a, x, y in zip(anios, fuente["impuestos"], fuente["bai"])), "pagina": None, "nota": "Vacío si el resultado antes de impuestos es ≤ 0." + aviso_pend(pend_tipo)}
    if pend_tipo:
        H["tipo_impositivo"]["pendientes_verificacion"] = pend_tipo
    for k in ["cfo", "capex", "adquisiciones"]:
        poner(k, serie[k], fuente[k], base + (" Adquisiciones = −(pagos y cobros por negocios del estado de flujos)." if k == "adquisiciones" else ""))
    poner("circulante", serie["circulante_lineas"], fuente["circulante_lineas"], base + " Aumento del circulante = −(suma de las líneas de variación del circulante del estado de flujos): convención del ejercicio.")
    for k in ["intereses", "intereses_financiacion", "arrendamientos_principal", "sbc", "id", "acciones_diluidas", "patrimonio", "deuda", "arrendamientos"]:
        poner(k, serie[k], fuente[k], base)
    pend_caja = sorted(set(pend_usados.get("caja", [])) | (set(pend_usados.get("otros_activos_financieros", [])) if conv.get("caja_incluye_otros_activos_financieros") else set()))
    poner("caja", caja, fuente["caja"], pend=pend_caja, nota=base + (f" Incluye otros activos financieros corrientes: {conv.get('motivo_caja', '')} Solo efectivo (mm): " + ", ".join(f"{a} {c}" for a, c in zip(anios, serie['caja'])) if conv.get("caja_incluye_otros_activos_financieros") else " Solo efectivo y equivalentes (definición de la plantilla)."))
    for k in ["pensiones", "minoritarios"]:
        poner(k, serie[k], fuente[k], base)
    # esenciales
    falt = [f"{k} {a}" for k in ESENCIALES for a, v in zip(anios, serie[k]) if v is None and a >= anios[-3]]
    f1 = {k: meta.get(k) for k in ("empresa", "ticker", "fecha_analisis", "sector_texto", "moneda_modelo", "norma_contable", "cierre_fiscal", "mercado", "ratio_adr", "sector_damodaran", "precio", "acciones_diluidas", "capitalizacion", "tasa_sin_riesgo", "geografia", "geografia_fuente")}
    f1["unidad"] = "mm"
    if isinstance(meta.get("control_maestro_textos"), dict) and meta["control_maestro_textos"]:
        # (4.15, X2/H-P1) textos declarativos del Control maestro (cabecera F5 y lista de comprobación C86:E102) que sustituyen los de la
        # etapa 1 cuando ya no describen el expediente; rellenar_fase1_v63.py los escribe y guarda el anterior en su registro
        f1["control_maestro_textos"] = dict(meta["control_maestro_textos"])
    f1["anios_fcf_base"] = meta.get("anios_fcf_base", 3)
    f1["historia"] = {"anios": anios, "partidas": H}
    f1["analisis"] = meta.get("analisis") or {}
    # (4.15, C48 de Elis) entradas de Análisis declaradas con su CÁLCULO explícito sobre la Historia y componentes con fuente: la entrada
    # efectiva justificada se reconstruye desde las entradas declaradas (no depende de que la celda conserve un valor migrado)
    errores_calculo = []
    for celda, d in list(f1["analisis"].items()):
        if isinstance(d, dict) and isinstance(d.get("calculo"), dict):
            try:
                f1["analisis"][celda] = calcular_entrada(celda, d, H, anios, carpeta)
            except (ValueError, TypeError) as ex:
                errores_calculo.append(f"Análisis!{celda}: {ex}")
    if errores_calculo:
        raise SystemExit("fase1_metadatos.json · cálculo de entradas de Análisis no reproducible: " + "; ".join(errores_calculo))
    # v2.2 (Nike): los datos base del DCF (Análisis C46–C50) salen de la Historia si la etapa 1 no los trae: media de los
    # últimos anios_fcf_base ejercicios. rellenar_fase1_v63.py solo los escribe en celdas vacías (no pisa la etapa 1).
    # (redondeo exacto) doble redondeo intencionado, como la hoja: la media exacta de los valores de la Historia (ya a 4 decimales) a 3.
    n_fcf = int(meta.get("anios_fcf_base", 3) or 3)
    for celda, k in (("C46", "cfo"), ("C47", "capex"), ("C48", "intereses_financiacion"), ("C49", "arrendamientos_principal"), ("C50", "sbc")):
        ult = serie[k][-n_fcf:]
        if celda not in f1["analisis"] and len(ult) == n_fcf and all(v is not None for v in ult):
            f1["analisis"][celda] = {"valor": redondear(sum(map(exacto, ult), Fraction(0)) / n_fcf, 3), "fuente": f"Historia de fase1_v63.json, media {anios[-n_fcf]}–{anios[-1]} de {k}: " + "; ".join(fuente[k][-n_fcf:])[:400], "pagina": None, "periodo": f"{anios[-n_fcf]}–{anios[-1]}", "unidad": "mm"}
    # H1 (cierre): el pendiente se propaga a TODA celda de datos de Análisis que dependa de la Historia en su ventana, también si ya
    # venía en fase1_metadatos.json (caso B: una media de la misma Historia). Una fuente independiente solo se libra con un
    # respaldo explícito y trazable (`independiente`: fuente con página, fecha, persona, motivo); declararla no basta.
    indep_rechazadas = []
    for celda in DEP_ANALISIS:
        e = f1["analisis"].get(celda)
        if not isinstance(e, dict):
            if e is not None:
                f1["analisis"][celda] = e = {"valor": e}
            else:
                continue
        pend_c = pendientes_celda(celda, H, anios, n_fcf)
        if not pend_c:
            continue
        if "independiente" in e:
            defecto = defecto_independiente(e["independiente"])
            if defecto is None:
                e["independiente_confirmado"] = True
                e["nota"] = ((e.get("nota") or "") + f" Fuente independiente de la Historia, respaldada por {e['independiente']['confirmado_por']} el {e['independiente']['fecha']}: {e['independiente']['fuente']} ({e['independiente']['motivo']}). La Historia tiene ceros pendientes en {', '.join(map(str, pend_c))}, que no afectan a esta cifra.").strip()
                continue
            indep_rechazadas.append(f"{celda}: respaldo independiente no aceptado ({defecto})")
        e["pendiente_verificacion"] = sorted(set(pend_c) | set(e.get("pendiente_verificacion") or []))  # (4.15) sin perder los del cálculo
        e["nota"] = ((e.get("nota") or "") + f" Depende de la Historia con ceros pendientes en {', '.join(map(str, pend_c))}." + aviso_pend(pend_c)).strip()
    if not f1.get("capitalizacion") and f1.get("precio") and f1.get("acciones_diluidas"):
        f1["capitalizacion"] = {"valor": redondear(exacto(f1["precio"]["valor"]) * exacto(f1["acciones_diluidas"]["valor"]), 1), "fecha": f1["precio"].get("fecha"), "fuente": "precio × acciones diluidas"}
    f1["_notas"] = ["Historia construida por scripts/fase1_historia.py (pieza 7); revisión completa en historia_revision.md."] + list(meta.get("_notas") or [])
    f1["pendientes_verificacion"] = [dict(pend_ar_idx[(k, a)]) for k in sorted(pend_usados) for a in pend_usados[k]]
    if confirmados:
        f1["ceros_confirmados"] = confirmados
    if f1["pendientes_verificacion"]:
        f1["_notas"].append(f"{len(f1['pendientes_verificacion'])} ceros pendientes de verificación (cita sin contrastar, reparación H1): ver historia_revision.md.")
    faltan_meta = [k for k in ("empresa", "ticker", "moneda_modelo", "precio", "acciones_diluidas", "sector_damodaran") if not f1.get(k)]
    inc_acc = incoherencias_acciones(anios, serie["acciones_diluidas"], meta.get("acciones_diluidas")) + defecto_acciones_meta(meta.get("acciones_diluidas"))
    # revisión
    with open(os.path.join(carpeta, "historia_revision.md"), "w", encoding="utf-8") as f:
        f.write(f"# Revisión de la Historia · {f1.get('empresa')}\n\nInformes usados: " + ", ".join(f"{a} {fuentes[a]}" for a in anios) + "\n\n")
        f.write("## Tabla (mm)\n\n| Partida | " + " | ".join(map(str, anios)) + " |\n|---|" + "---|" * len(anios) + "\n")
        for k, d in H.items():
            f.write(f"| {k} | " + " | ".join("—" if v is None else f"{v:,.3f}" for v in d["valores"]) + " |\n")
        f.write("\n## Diferencias entre el informe de cada año y el comparativo del siguiente (se usa la más reciente)\n\n" + ("\n".join(rev) or "- ninguna") + "\n")
        ceros = [f"- {x['partida']} {x['anio']}: {x['archivo']} p.{x['pagina']} · motivo: {x['motivo']} · cita: «{x['cita']}»" for x in f1["pendientes_verificacion"]]
        conf = [f"- {x['partida']} {x['anio']} = {x['valor_mm']}: {x['fuente']} · {x['confirmado_por']}, {x['fecha']} (cita original: «{x['cita_original']}»)" for x in confirmados]
        desc = [f"- {k} {a}" for k in PARTIDAS for a, v in zip(anios, serie[k]) if v is None]
        f.write("\n## Ceros pendientes de verificación (cita sin contrastar)\n\nEl informe no imprime cifra; la cita existe en la página, pero nadie ha comprobado que hable de esa partida. El 0 se conserva y las celdas que dependen de él se marcan «Dato no verificable» en el libro. Solo una decisión humana registrada en fase1_decisiones.json (valor, fuente con página, fecha, persona) lo confirma.\n\n" + ("\n".join(ceros) or "- ninguno")
                + "\n\n## Ceros confirmados por decisión humana (fase1_decisiones.json)\n\n" + ("\n".join(conf) or "- ninguno")
                + "\n\n## Desconocidos (celda vacía, nunca 0)\n\n" + ("\n".join(desc) or "- ninguno") + "\n")
        celdas_pend = [f"- Análisis!{x}: {', '.join(map(str, e['pendiente_verificacion']))}" for x, e in f1["analisis"].items() if isinstance(e, dict) and e.get("pendiente_verificacion")]
        f.write("\n## Celdas de Análisis que heredan el pendiente\n\n" + ("\n".join(celdas_pend) or "- ninguna") + "\n")
        if indep_rechazadas:
            f.write("\n## Fuentes independientes no aceptadas (la celda sigue pendiente)\n\n" + "\n".join(f"- {x}" for x in indep_rechazadas) + "\n")
        if dec_invalidas:
            f.write("\n## DECISIONES INVÁLIDAS (bloquea)\n\n" + "\n".join(f"- {x}" for x in dec_invalidas) + "\n")
        f.write("\n## Convenciones\n\n" + json.dumps(conv, ensure_ascii=False) + "\n")
        if falt or faltan_meta or inc_acc:
            f.write("\n## BLOQUEA\n\n" + "\n".join([f"- falta {x}" for x in falt + faltan_meta] + [f"- {x}" for x in inc_acc]) + "\n")
    if dec_invalidas:
        print("decisiones inválidas en fase1_decisiones.json: " + "; ".join(dec_invalidas))
        return 1
    if falt or faltan_meta:
        print("faltan datos esenciales: " + ", ".join(falt + faltan_meta))
        return 1
    if inc_acc:
        print("acciones diluidas incoherentes: " + "; ".join(inc_acc))
        return 1
    json.dump(f1, open(os.path.join(carpeta, "fase1_v63.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"fase1_v63.json escrito ({len(anios)} años, {len(rev)} diferencias con el comparativo, {len(f1['pendientes_verificacion'])} ceros pendientes de verificación, {len(confirmados)} confirmados por decisión humana; ver historia_revision.md)")
    return 0


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    cmd, carpeta = sys.argv[1], os.path.abspath(sys.argv[2])
    if cmd == "comprobar-anio":
        pend = []
        errs = comprobar_anio(carpeta, int(sys.argv[3]), pend)
        print("OK" if not errs else "\n".join(errs))
        for x in pend:
            print(f"PENDIENTE: cero de {x['partida']} {x['anio']} (p. {x['pagina']}, cita «{x['cita'][:80]}»): la cita existe pero no está contrastada con la partida; no cuenta como comprobado")
        return 0 if not errs else 1
    if cmd == "preparar":
        return preparar(carpeta, sys.argv[3] if len(sys.argv) > 3 else os.path.basename(carpeta))
    if cmd == "construir":
        return construir(carpeta)
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
