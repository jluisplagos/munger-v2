#!/usr/bin/env python3
"""Verificación completa de las entradas financieras de un expediente (4.14; requisito de cierre «verificación completa de las entradas
financieras utilizadas»). No escribe nada salvo con `plantilla`.

Universo: TODAS las celdas de la instantánea de entradas económicas del libro (entradas_economicas.instantanea: las que alimentan la
valoración, sus referencias históricas, las sensibilidades y la lectura del precio), una entrada por celda —sin contar dos veces una misma
celda— más los datos de origen auxiliares de las entradas derivadas («aux:…», contados aparte). Un Excel evaluado anterior no acredita nada.

Registro: <expediente>/verificacion_entradas.json (forma parte del material auditado: cambiarlo retira la aprobación). Por entrada:
  celda · id · uso · material · clase ∈ {dato_publicado, derivado, cero_comprobado, dato_ausente, no_aplicable, hipotesis, convencion} ·
  valor_modelo (el del libro cuando se verificó) ·
  fuente {documento, archivo (ruta relativa al expediente o a personaje_v2/), sha256, version, pagina, ubicacion (tabla, nota o pasaje),
          concepto, columna, periodo, unidad, escala, signo, tratamiento, perimetro, reexpresado, valor_fuente, cita} (dato_publicado y cero) ·
  derivacion {origenes [celdas o aux:…], formula (expresión sobre `o["<origen>"]`), conciliacion} (derivado) ·
  hipotesis {fundamento, alternativas, limites} (hipótesis y convenciones: nunca como dato publicado; una firma no las demuestra) ·
  justificacion (dato_ausente y no_aplicable) ·
  comprobacion {extractor, revisor, fecha, resultado ∈ {verificado, discrepancia, pendiente}, fuente_examinada, nota} · incidencia.

Comprobaciones AUTOMÁTICAS (cobertura, conciliaciones y coherencia; NO demuestran la corrección semántica: eso es del revisor
independiente, que examina la fuente):
  - cobertura: toda celda del universo tiene su entrada; ninguna sobra; ninguna se repite;
  - vigencia: el valor del libro es el registrado; el sha256 del archivo de la fuente, si se conserva, es el registrado (una fuente, un dato o
    una transformación cambiados invalidan la comprobación y las que dependen de ella: reutilización solo si coinciden);
  - dato publicado: todos los campos; signo × escala × valor_fuente = valor_modelo; escala coherente con las unidades de la fuente y del
    modelo; período que contiene el año de la columna de la Historia; perímetro igual al declarado por el expediente; la cita literal está
    en la página citada del texto de la fuente (si se conserva) y contiene el valor de la fuente — encontrar los mismos dígitos en una página
    no acredita el contraste: la comprobación del revisor sigue siendo obligatoria;
  - derivado: orígenes con su entrada y comprobados; la fórmula reproduce el valor; conciliación declarada;
  - cero comprobado (cero con su fuente) ≠ dato ausente (sin dato, con justificación) ≠ no aplicable (justificación);
  - revisión: revisor distinto del extractor, resultado «verificado» y fuente examinada declarada.
`aptitud(carpeta)`: apto_por_entradas solo con cobertura completa y todas las entradas materiales comprobadas, vigentes y sin discrepancia.
Es condición necesaria, no suficiente, para presentar una conclusión como apta para dinero real.
(4.15, encargo correctivo tras la revisión externa de la 4.14)
  R1 · página: una fuente que exige contraste de página no está comprobada si la página no existe o no puede examinarse. «pagina» es la
       página del PDF (marcas «[PDF PAGE n]» del texto extraído); el folio impreso va aparte, en «folio». Página inexistente →
       discrepancia; página no inequívoca, o fuente sin texto con marcas de página («archivo_texto» para un PDF u HTML) → pendiente.
  R2 · conservación: «conservacion» = «local» (por defecto si hay «archivo») o «externa». Una fuente local tiene que existir y tener su
       sha256 registrado y vigente; si falta el archivo o la huella, la entrada queda pendiente: su contraste no es reproducible, y lo
       que declaren el extractor o el revisor no lo sustituye. Una lectura externa sin bytes exige «lectura_externa» {referencia, fecha,
       evidencia, limitaciones}; aunque esté completa no cuenta como comprobada: se lista aparte («lecturas_externas») y, si es material,
       impide la aptitud por entradas.
  R3 · cifras: la cita tiene que contener el valor de la fuente con formato numéricamente equivalente (separadores de miles y decimales,
       ceros finales); un número distinto que solo coincide al redondear no vale. Si la fuente publica menos precisión, el registro
       declara el valor publicado y la transformación (derivado), nunca una precisión inventada.
  I13 · vigencia del fundamento: cada comprobación lleva «vinculo» {huella, elementos, sellado_por, fecha}: la huella de su fundamento,
       evidencia y transformación (clase, valor, fuente, derivación, hipótesis, justificación y la fila de evidencia del Control maestro de
       la celda en el libro). Si cambia cualquiera de ellos, la comprobación queda desactualizada aunque el número coincida; sin vínculo
       (registros 4.14) queda pendiente. La huella incluye además quién, cuándo y con qué resultado se comprobó, las huellas de los orígenes
       de un derivado y la declaración de la entrada en fase1_v63.json (FCF base). `sellar` solo sella la revisión de hoy, de ese revisor y de
       entradas que pasan todos los controles; no impide escribir un vínculo a mano: detecta cambios, no acredita autoría (eso lo cubren el
       registro como material auditado y la auditoría).
  I8 · cobertura del juicio: además de las entradas de cálculo (instantánea de entradas_economicas, que sigue mandando en las variantes),
       el universo incluye las cifras financieras que se dan a las fases de juicio (datos de Análisis de datos_v63.md y filas de la Historia
       que no entran en el cálculo), con «ambito» = «juicio». Bloquean igual; su cambio no invalida las variantes (dependencias distintas).
  (4.15, segunda revisión independiente)
  N1 · una entrada de juicio no material (con «justificacion_materialidad») que no está comprobada solo deja de bloquear si un revisor
       independiente ha revisado y sellado ese juicio de materialidad (resultado «verificado», fuente examinada, vínculo vigente); se
       cuenta siempre, también cuando el registro es apto.
  N2 · un DATO del modelo que se obtiene como derivado de una hipótesis o convención (directa o indirectamente, p. ej. un auxiliar
       «convención») es un dato presentado como hipótesis: exige «justificacion_clase» y se lista; la fórmula de un derivado tiene que
       usar todos sus orígenes y solo ellos; «no aplicable» se cuenta aparte.
  N4 · el redondeo del libro a 3 decimales solo vale en un derivado que declara un importe («derivacion.unidad» monetaria); en
       cualquier otra magnitud el resultado es exacto o el redondeo se declara en la fórmula (round).
  12 · una fuente PDF tiene que ser un PDF y la cita tiene que estar en esa página del PDF (pdftotext), no solo en su texto conservado.
  (4.15, tercera y cuarta revisión: T1–T5) aritmética exacta (fracciones) en los derivados; una fórmula solo admite como literales enteros
       de 1 a 12, potencias de diez y los decimales de round, usa todos sus orígenes y cada uno influye; tipo de la fuente por su contenido.
       Límite declarado (U1): estas reglas descartan las formas triviales, NO acreditan que la fórmula derive el concepto: eso lo acredita
       solo la revisión independiente del significado económico de cada derivado (revisor distinto del extractor y vínculo sellado).
  (4.15, hito 2, tras la revisión externa del hito 1)
  R415-SIGNO · «valor_fuente» es la cifra PUBLICADA con su signo; «signo» y «escala» la transforman después hacia el modelo. La cita se
       contrasta con su signo (_cita_cifra): menos ASCII o Unicode, guion pegado, paréntesis contables («(130,8)» es −130,8) o sin marca;
       signo contrario → discrepancia; signo que no puede determinarse (guion a un espacio, dos marcas, dos signos a la vez) → pendiente;
       un guion separado por dos o más espacios en la página es otra columna (un cero). La transformación justificada (signo −1) sigue
       siendo válida. fase1_historia.calcular_entrada aplica la misma regla a los componentes de un cálculo declarado.
  U1 · los derivados comprobados se cuentan y se listan («derivados_comprobados», resumen, ficha e informe).
  U2 · un importe del libro es el resultado exacto o uno de sus redondeos a 3 decimales (|exacto − libro| ≤ 0,0005 con el libro a 3
       decimales como mucho: los dos sentidos de un empate); no es una tolerancia general.
  U3 · coste acotado: fórmula de 2000 caracteres y 400 nodos como mucho; round con los decimales como entero literal entre 0 y 12.
  U4 · sensibilidad local y estructural (_sensibilidad): se aceptan un origen −1, un producto por un cero, 0 / d, el argumento menor de
       un max y max(…, 0); siguen siendo errores o[x] * 0 + c, o[x] − o[x] + o[y] y una fórmula constante en el punto real.
  U5 · una fuente HTML se lee con html.parser (texto visible: sin comentarios, atributos, script, style, template, head ni elementos
       ocultos) y se decodifica por su BOM o su charset declarado; sin declaración y sin UTF-8 válido, pendiente.
Uso: verificacion_entradas.py comprobar <expediente> [--json] | plantilla <expediente> (escribe verificacion_entradas.plantilla.json)
     | sellar <expediente> --revisor NOMBRE --fecha AAAA-MM-DD(hoy) CELDA [CELDA …]
"""
import ast
import datetime as dt
import decimal
import fractions
import hashlib
import json
import os
import re
import sys
import unicodedata

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import entradas_economicas as EE  # noqa: E402

FORMATO = "4.15"
FORMATOS_ADMITIDOS = ("4.14", "4.15")
CONSERVACION = ("local", "externa")
CAMPOS_LECTURA_EXTERNA = ("referencia", "fecha", "evidencia", "limitaciones")
# (4.15, I8) datos de Análisis que datos_v63.md da a las fases de juicio (volcar_datos_v63.DATOS_ANALISIS) que no son de identificación ni
# fórmulas del libro; la batería comprueba que es un subconjunto de esa lista
DATOS_JUICIO_ANALISIS = ("C24", "C26", "C28", "C31", "C32", "C33", "C34", "C38", "C40", "C42", "C46", "C47", "C48", "C49", "C50", "C53", "C54",
                         "C55", "C57", "C60", "C88", "C96")
FILAS_HISTORIA_JUICIO = (6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26)  # leer_v63.FILAS_HISTORIA sin el año
# (4.15, revisión independiente, hallazgo 6) también lo que datos_v63.md da al juicio desde Palancas: el sector de Damodaran (C7, decide
# qué cuartiles ve el juicio), las fechas del precio y de las acciones (C45, C46) y el reparto geográfico (A28:B33, filas con dato), que
# fija la r mínima que la fase A compara con la r del inversor. Las cifras del extracto (extracto_v63.md) quedan fuera de este control:
# las cubre la verificación de citas de las fases.
DATOS_JUICIO_PALANCAS = ("C7", "C45", "C46")
FILAS_GEOGRAFIA = range(28, 34)
REGISTRO = "verificacion_entradas.json"
CLASES = ("dato_publicado", "derivado", "cero_comprobado", "dato_ausente", "no_aplicable", "hipotesis", "convencion")
CAMPOS_FUENTE = ("documento", "version", "pagina", "ubicacion", "concepto", "columna", "periodo", "unidad", "escala", "signo", "tratamiento",
                 "perimetro", "reexpresado", "valor_fuente", "cita")
RESULTADOS = ("verificado", "discrepancia", "pendiente")
# unidades → millones de la moneda (el modelo trabaja en «mm»: Control maestro!J4)
UNIDADES = {"mm": 1.0, "millones": 1.0, "millones de euros": 1.0, "millones de eur": 1.0, "m€": 1.0, "meur": 1.0, "€m": 1.0,
            "miles": 1e-3, "miles de euros": 1e-3, "miles de eur": 1e-3, "k€": 1e-3, "keur": 1e-3, "€000": 1e-3, "euros": 1e-6, "eur": 1e-6}
COL_ANIO = {c: i for i, c in enumerate("CDEFGHIJKL")}  # Historia C5:L5


def _sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest() if os.path.isfile(p) else None


def _num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and x == x and abs(x) != float("inf")


def _igual_exacto(a, b):
    """(4.15, hallazgo 5) Igualdad sin la tolerancia de importes: relativa 1e-9 (tasas, ratios, probabilidades, escalas y vigencia)."""
    if _num(a) and _num(b):
        return abs(a - b) <= 1e-9 * max(abs(a), abs(b)) + 1e-15
    return EE.iguales(a, b) if hasattr(EE, "iguales") else a == b


def _importe_libro_exacto(exacto, vm):
    """(4.15, hito 2, U2) Un IMPORTE del libro es el resultado EXACTO (fracción) o uno de sus redondeos a 3 decimales: el libro tiene como
    mucho 3 decimales y |exacto − libro| ≤ 0,0005. En un empate (x,xxx5 exacto) valen los dos vecinos, porque el generador (coma
    flotante), ROUND de la hoja y el redondeo de Python lo resuelven de forma distinta. No es una holgura: 0,2511 no es 0,25, 849,0 no es
    849,697 y 849,6976 no es 849,697 (con 3 decimales en el libro, la distancia máxima es media unidad del tercer decimal)."""
    if not (isinstance(exacto, fractions.Fraction) and _num(vm)):
        return False
    fv = fractions.Fraction(repr(float(vm)))
    if fv == exacto:
        return True
    return (fv * 1000).denominator == 1 and abs(exacto - fv) <= fractions.Fraction(1, 2000)


MARCAS_MONEDA = re.compile(r"(€|\$|£|¥|\beur\b|\beuros?\b|\busd\b|\bgbp\b|\bchf\b|\bdkk\b|\bsek\b|\bnok\b|\bbrl\b|\bjpy\b|\bd[oó]lar|\blibras?\b|"
                           r"\bcoronas?\b|\breal(?:es)?\b|\bfrancos?\b|\bmm€|\bmeur|\bkeur|\bk€)", re.I)  # (hito 2, V7) también «real»
POR_UNIDAD = re.compile(r"(por|per|/)\s*(acci[oó]n|share|t[ií]tulo|unidad|unit)", re.I)


def _moneda_de(marca):
    """(4.15, hito 2, Q1) La moneda de una marca de MARCAS_MONEDA, normalizada («€», «eur», «euros» → «eur»)."""
    m = _norm_txt(marca)
    # (hito 2, V1) también el franco, el real y las coronas: «corona» puede ser la danesa, la sueca o la noruega, así que con un código de
    # corona es la misma moneda («coronas/DKK» no es un tipo de cambio)
    for cod, formas in (("eur", ("€", "eur", "euro", "euros")), ("usd", ("$", "usd", "dólar", "dolar", "dólares", "dolares")),
                        ("gbp", ("£", "gbp", "libra", "libras")), ("jpy", ("¥", "jpy")), ("chf", ("chf", "franco", "francos")),
                        ("brl", ("brl", "real", "reales")), ("corona", ("corona", "coronas", "dkk", "sek", "nok"))):
        if m in formas or any(m.startswith(f) for f in formas if len(f) > 2):
            return cod
    return m


def _unidad_monetaria_no_reconocida(unidad):
    """(4.15, hito 2, U7) La unidad nombra una moneda pero no está en UNIDADES (y no es un importe por acción o por unidad, cuya escala es
    la del propio precio): su escala no puede contrastarse."""
    t = _norm_txt(unidad)
    # (hito 2, N9) un tipo de cambio («USD por EUR», «EUR/USD») es una razón entre monedas, no un importe: no se le aplica esta regla
    # (hito 2, T1) solo un par de monedas («USD por EUR», «EUR/USD», «tipo de cambio EUR/GBP») y sin ninguna palabra de escala: «miles de
    # euros a tipo de cambio constante» o «millones de euros/EUR million» son importes y siguen exigiendo una unidad reconocida
    m_ = MARCAS_MONEDA.pattern
    par = re.fullmatch(r"(?:(?:tipo de cambio|exchange rate)\b)?[\s:(]*(?P<a>" + m_ + r")\s*(?:por|per|/)\s*(?P<b>" + m_ + r")[\s)]*", t, re.I)
    _a, _b = (_moneda_de(par.group("a")), _moneda_de(par.group("b"))) if par is not None else (None, None)
    if {_a, _b} <= {"corona"} and par is not None and _norm_txt(par.group("a")) in ("dkk", "sek", "nok") and _norm_txt(par.group("b")) in ("dkk", "sek", "nok"):
        _a, _b = _norm_txt(par.group("a")), _norm_txt(par.group("b"))  # «DKK/SEK»: dos coronas distintas, un tipo de cambio
    tipo_cambio = (par is not None and _a != _b  # (hito 2, Q1) dos monedas DISTINTAS: «euros/EUR» no es un tipo de cambio
                   and re.search(r"miles|millones|millares|thousand|million|billion|\bmm\b|\bbn\b|mm€|meur|keur|k€|m€|€m|€000", t, re.I) is None)
    return bool(t) and t not in UNIDADES and MARCAS_MONEDA.search(t) is not None and POR_UNIDAD.search(t) is None and not tipo_cambio


def _canon(x):
    """(4.15, hallazgo 17) Forma canónica para la huella: números por su valor (849697.0 = 849697), textos en NFC sin espacios de más."""
    if isinstance(x, dict):
        return {str(k): _canon(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_canon(v) for v in x]
    if isinstance(x, float) and x == x and abs(x) != float("inf") and x.is_integer():
        return int(x)
    if isinstance(x, str):
        return re.sub(r"\s+", " ", unicodedata.normalize("NFC", x)).strip()
    return x


def libro_de(carpeta):
    e = os.path.basename(os.path.abspath(carpeta))
    for n in (f"{e}_v63_evaluada.xlsx", f"{e}_v63_datos.xlsx"):
        if os.path.isfile(os.path.join(carpeta, n)):
            return os.path.join(carpeta, n)
    return None


def universo_calculo(carpeta):
    """Entradas de cálculo: la instantánea de entradas_economicas (valoración, sensibilidades y lectura del precio)."""
    lb = libro_de(carpeta)
    return EE.instantanea(lb) if lb else None


def _es_formula(v):
    return isinstance(v, (list, tuple)) and len(v) >= 1 and v[0] == "="


def universo(carpeta):
    """(4.15, I8) Universo completo: las entradas de cálculo («ambito» = «calculo») y las cifras financieras que se dan a las fases de juicio
    y no entran en el cálculo («ambito» = «juicio»). «huella» sigue siendo la de las entradas de cálculo (variantes y vigencia)."""
    lb = libro_de(carpeta)
    if not lb:
        return None
    inst = EE.instantanea(lb)
    inst = dict(inst, celdas=dict(inst["celdas"]), tipos=dict(inst["tipos"]), ids=dict(inst["ids"]))
    inst["ambito"] = {k: "calculo" for k in inst["celdas"]}
    lec = EE._Lector(lb)
    hojas = set(lec.lb.hojas())
    extra = []
    if "Análisis" in hojas:
        extra += [("Análisis", r, f"juicio_{r}") for r in DATOS_JUICIO_ANALISIS]
    if "Historia" in hojas:
        extra += [("Historia", f"{c}{f}", f"juicio_h{f}") for f in FILAS_HISTORIA_JUICIO for c in "CDEFGHIJKL"]
    if "Palancas" in hojas:
        extra += [("Palancas", r, f"juicio_{r}") for r in DATOS_JUICIO_PALANCAS]
        for f in FILAS_GEOGRAFIA:
            if lec.leer("Palancas", f"A{f}") not in (None, "") or lec.leer("Palancas", f"B{f}") not in (None, ""):
                extra += [("Palancas", f"A{f}", f"juicio_geografia_{f}"), ("Palancas", f"B{f}", f"juicio_geografia_{f}")]
    for hoja, ref, ident in extra:
        k = f"{hoja}!{ref}"
        if k in inst["celdas"]:
            continue
        v = EE._norm(lec.leer(hoja, ref))
        if _es_formula(v) or lec.lb.tiene_formula(hoja, ref):
            continue  # transformación del libro sobre otras celdas: lo que se contrasta son sus orígenes
        inst["celdas"][k] = v
        inst["tipos"][k] = "dato"
        inst["ids"][k] = ident
        inst["ambito"][k] = "juicio"
    inst["n_calculo"] = sum(1 for a in inst["ambito"].values() if a == "calculo")
    inst["n_juicio"] = sum(1 for a in inst["ambito"].values() if a == "juicio")
    inst["n"] = len(inst["celdas"])
    return inst


def evidencia_libro(carpeta):
    """(4.15, I13) Fila de evidencia del Control maestro (filas 17–175: B = celda; C:N) de cada celda, tal como está en el libro."""
    lb = libro_de(carpeta)
    if not lb:
        return {}
    lec = EE._Lector(lb)
    if "Control maestro" not in set(lec.lb.hojas()):
        return {}
    out = {}
    for r in range(17, 176):
        b = lec.leer("Control maestro", f"B{r}")
        if not isinstance(b, str) or "!" not in b:
            continue
        fila = {c: EE._norm(lec.leer("Control maestro", f"{c}{r}")) for c in "CDEFGHIJKLMN"}
        fila = {c: (None if _es_formula(v) else v) for c, v in fila.items()}
        try:
            celdas = EE._expandir(b.replace("'", ""))
        except ValueError:
            continue
        for hoja, ref in celdas:
            out.setdefault(f"{hoja}!{ref}", {"fila": r, **fila})
    # (4.15, revisión independiente, hallazgo 14) las celdas de «Configuración V6.4» no tienen fila en el Control maestro: su evidencia son
    # las celdas de trazabilidad de su clave (fuente, período, perímetro…)
    CE = EE.CE
    if CE.HOJA in set(lec.lb.hojas()):
        for clave, refs in CE.TRAZA_CELDAS.items():
            meta = {m: EE._norm(lec.leer(CE.HOJA, m)) for m in refs if m in CE.CELDAS_METADATOS}
            for r_ in refs:
                if r_ not in CE.CELDAS_METADATOS:
                    out.setdefault(f"{CE.HOJA}!{r_}", {"clave": clave, "trazabilidad": meta})
    return out


CAMPOS_COMPROBACION_EN_HUELLA = ("extractor", "revisor", "fecha", "resultado", "fuente_examinada")


def huella_fundamento(e, evid=None, extra=None):
    """(4.15, I13) Huella del fundamento, la evidencia y la transformación de una entrada: lo que el revisor examinó. (Revisión independiente,
    hallazgos 3, 4, 9 y 17) Incluye también quién, cuándo y con qué resultado se comprobó (CAMPOS_COMPROBACION_EN_HUELLA), y en `extra` las
    huellas vigentes de los orígenes de un derivado y, en las entradas del FCF base, su declaración en fase1_v63.json. Forma canónica."""
    base = {c: e.get(c) for c in ("celda", "clase", "material", "valor_modelo", "fuente", "derivacion", "hipotesis", "justificacion",
                                  "justificacion_clase", "justificacion_materialidad")}
    c = e.get("comprobacion") if isinstance(e.get("comprobacion"), dict) else {}
    base["comprobacion"] = {k: c.get(k) for k in CAMPOS_COMPROBACION_EN_HUELLA}
    base["evidencia_libro"] = evid
    base["extra"] = extra
    t = json.dumps(_canon(base), ensure_ascii=False, sort_keys=True, default=str, separators=(",", ":"))
    return hashlib.sha256(t.encode("utf-8")).hexdigest()


def _f1_declaraciones(carpeta):
    """{celda de Análisis: declaración} de fase1_v63.json, o None si no hay fase1_v63.json legible como objeto."""
    try:
        f1 = json.load(open(os.path.join(carpeta, "fase1_v63.json"), encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if not isinstance(f1, dict):
        return None
    a = f1.get("analisis")
    return a if isinstance(a, dict) else {}


def huellas_registro(carpeta, reg=None, evid=None):
    """(4.15) {celda: huella vigente} de todas las entradas del registro, con los orígenes de los derivados (recursivo, con ciclos marcados)
    y la declaración de fase1_v63.json de las entradas del FCF base. Es lo que `comprobar` exige y lo que `sellar` escribe."""
    if reg is None:
        reg, _ = cargar(carpeta)
    evid = evidencia_libro(carpeta) if evid is None else evid
    por = {str(e.get("celda")): e for e in (reg or {}).get("entradas") or [] if isinstance(e, dict)}
    decl = _f1_declaraciones(carpeta)
    memo, en_curso = {}, set()

    def h(k):
        if k in memo:
            return memo[k]
        if k in en_curso:
            return "ciclo"
        en_curso.add(k)
        e = por.get(k) or {}
        extra = {}
        d = e.get("derivacion") if isinstance(e.get("derivacion"), dict) else {}
        if e.get("clase") == "derivado" and isinstance(d.get("origenes"), list):
            extra["origenes"] = {str(o): (h(str(o)) if str(o) in por else None) for o in d["origenes"]}
        if k in ENTRADAS_FCF_BASE:
            extra["declaracion_fase1_v63"] = None if decl is None else decl.get(k.split("!")[1])
        en_curso.discard(k)
        memo[k] = huella_fundamento(e, evid.get(k), extra or None)
        return memo[k]
    return {k: h(k) for k in por}


ELEMENTOS_VINCULO = ["clase", "material", "valor_modelo", "fuente (documento, archivo, sha256, página, cita, escala, signo…)", "derivacion (orígenes, fórmula, conciliación)",
                     "hipotesis (fundamento, alternativas, límites)", "justificacion (y la de la clase y la materialidad)", "fila de evidencia del Control maestro de la celda en el libro "
                     "(o la trazabilidad de su clave en «Configuración V6.4»)", "extractor, revisor, fecha, resultado y fuente examinada de la comprobación",
                     "huellas vigentes de los orígenes de un derivado", "declaración de la entrada en fase1_v63.json (FCF base)"]


def _anios(inst):
    return [inst["celdas"].get(f"Historia!{c}5") for c in "CDEFGHIJKL"]


def _ruta_fuente(carpeta, archivo):
    """Ruta de una fuente conservada. (4.15, hallazgo 11) Solo rutas relativas que quedan dentro del expediente o del paquete: una ruta
    absoluta o que sale de ellos no es una fuente conservada con el expediente."""
    if not archivo or os.path.isabs(str(archivo)):
        return None
    for base in (carpeta, os.path.dirname(AQUI), os.path.dirname(os.path.dirname(AQUI))):
        b = os.path.realpath(base)
        p = os.path.realpath(os.path.join(base, str(archivo)))
        if p.startswith(b + os.sep) and os.path.isfile(p):
            return p
    return None


def _numero_pagina(pagina):
    """(4.15, R1) Página del PDF como entero ≥ 1: un entero, «12» o «PDF 12»/«pdf p. 12». Cualquier otra forma («12-13», «p. 12 y 14»,
    «folio 76», vacío) no identifica una sola página del PDF → None."""
    if isinstance(pagina, bool):
        return None
    if isinstance(pagina, int):
        return pagina if pagina >= 1 else None
    if isinstance(pagina, float) and pagina.is_integer():
        return int(pagina) if pagina >= 1 else None
    m = re.fullmatch(r"\s*(?:pdf\s*(?:p(?:ág(?:ina)?|age)?\.?\s*)?)?(\d+)\s*", str(pagina or ""), re.I)
    return int(m.group(1)) if m and int(m.group(1)) >= 1 else None


def _pagina_examinable(ruta_txt, pagina):
    """(4.15, R1) («ok», texto) · («pendiente», motivo) si no se puede examinar · («discrepancia», motivo) si la página no existe."""
    n = _numero_pagina(pagina)
    if n is None:
        return "pendiente", f"la página declarada {pagina!r} no identifica una página del PDF (un entero; el folio impreso va en «folio»)"
    try:
        t = open(ruta_txt, encoding="utf-8", errors="replace").read()
    except OSError as ex:
        return "pendiente", f"el texto de la fuente no se puede leer ({type(ex).__name__}): la página no puede examinarse"
    partes = re.split(r"\[PDF PAGE (\d+)\]", t)
    numeros = [int(partes[i]) for i in range(1, len(partes) - 1, 2)]
    if not numeros:
        return "pendiente", "el texto de la fuente no tiene marcas «[PDF PAGE n]»: la página no puede examinarse"
    for i in range(1, len(partes) - 1, 2):
        if int(partes[i]) == n:
            return "ok", partes[i + 1]
    return "discrepancia", f"la página {n} no existe en el texto de la fuente (páginas {min(numeros)}–{max(numeros)}, {len(numeros)} marcas)"


def _norm_txt(s):
    # (14-nov, revisión del extractor de Viscofan) «str(s or "")» convertía el 0 en "": un 0 publicado y una celda vacía parecían iguales
    return re.sub(r"\s+", " ", "" if s is None else str(s)).strip().lower()


def _decimales_exactos(a):
    """(4.15, R3) Decimales con que se escribe el valor sin redondear, contados en su representación decimal más corta (repr), no con una
    tolerancia (hallazgo 10: 10000000,01 ya no se escribe «10.000.000»). None si necesita más de diez."""
    try:
        d = decimal.Decimal(repr(float(a))).normalize()
    except (decimal.InvalidOperation, ValueError):
        return None
    n = max(0, -d.as_tuple().exponent) if d.as_tuple().exponent < 0 else 0
    return n if n <= 10 else None


def _cifras(x):
    """Formas textuales de un número de la fuente (1.234,5 · 1,234.5 · 1234.5 · 1234,5 · 4 573,7), numéricamente EQUIVALENTES:
    (4.15, R3) solo con tantos decimales como tiene el valor o más (ceros finales: «54,7000» para 54,7); nunca menos, porque escribir
    149,5 como «150» o 45.479,209 como «45.479» es otro número obtenido redondeando."""
    if not _num(x):
        return []
    a = abs(x)
    d0 = _decimales_exactos(a)
    if d0 is None:
        return []
    out = set()
    for dec in range(d0, max(d0, 10) + 1):  # (14-nov) los boletines imprimen cuatro decimales («54,7000»); (4.15) hasta diez con ceros finales
        s = f"{a:,.{dec}f}"
        out |= {s, s.replace(",", "X").replace(".", ",").replace("X", "."), s.replace(",", ""), s.replace(",", "").replace(".", ","),
                s.replace(",", " ").replace(".", ","),  # miles con espacio y coma decimal («4 573,7», informes en francés)
                s.replace(",", " "), s.replace(",", "'")}  # (4.15, hallazgo 18) miles con espacio o apóstrofo y punto decimal
    return [o for o in out if o]


MENOS_UNICODE = "−"  # «−»: signo menos si va pegado a la cifra; aislado, como los guiones (una fuente real lo usa para imprimir un cero)
GUIONES = "-‐‑‒–—﹣－"  # guion ASCII y guiones tipográficos: signo menos si van pegados; aislados, un cero


MONEDA_RE = r"(?:[€$£¥]|\b(?:EUR|USD|GBP|CHF|JPY|DKK|SEK|NOK|BRL)\b)"


def _signo_en_cita(t, ini, fin):
    """(4.15, R415-SIGNO) Signo con que el texto t PUBLICA la cifra que ocupa t[ini:fin]: +1, −1 o None si no puede determinarse.
      −1: un guion o un menos («-», «−», «–», «—») PEGADO a la cifra y precedido de un espacio, el principio, un signo de puntuación o una
          moneda («$-149,5»); paréntesis contables «(149,5)», también con moneda («(€149,5)», «(EUR 149,5)», «(149,5 €)») o porcentaje
          («(3,2 %)»).
      +1: la cifra sin marca o con «+»; un guion pegado al año anterior de un intervalo de años crecientes y plausibles («2019-2020»,
          «FY2023-2024») o a una fecha («31-12-2024») no es un signo. Cualquier otro guion pegado entre cifras deja el signo indeterminado
          («2023-849», «2024-2023», «2-3 %», «100-150», el día de una fecha ISO, «31-12-24»): pendiente prudente, declarado (V6).
      None: un guion o un menos separado de la cifra por UN espacio (puede ser un cero de la columna anterior o un signo: «Interests - 13»;
          (hito 2, H4) también «−», que una fuente real usa para imprimir un cero), un guion pegado a una palabra, un paréntesis que no se
          cierra, dos marcas pegadas («-(149,5)») o un menos detrás de la cifra («149,5-»).
    Un guion separado por dos o más espacios es otra columna (el cero impreso como guion, la misma convención que el control del cero).
    Límite declarado (hito 2, H3): esa convención lee como positiva una cifra con un signo menos separado por varios espacios; en las
    fuentes reales la regla acierta. El texto tiene que ser el de la página (con sus espacios), no la cita: lo hace _cita_cifra.
    Otros límites declarados (revisiones del hito 2; ninguno afecta a un registro real): quedan pendientes, por prudencia, formas
    legítimas como «(149.5m)», «(-x)», «31-dic-2024», «2024-25», «12-2024» o «7-7,5 %» (T8, Q3) y diferencias tipográficas entre el texto
    conservado y el del documento (T4); un carácter invisible entre el signo y la cifra la hace leer en positivo; ISO-8859-9 y -11 se
    leen con su tabla ISO, no con la de windows; el signo escrito con palabras («menos 149,5») no se reconoce (Q6)."""
    antes, despues = t[:ini], t[fin:]
    antes = re.sub(MONEDA_RE + r"\s?$", "", antes, flags=re.I)
    despues = re.sub(r"^\s?(?:" + MONEDA_RE + r"|%)", "", despues, flags=re.I)
    marcas = re.escape(GUIONES + MENOS_UNICODE)
    m_par = re.search(r"\(\s*$", antes)
    if m_par:
        if re.search("[" + marcas + r"+]$", antes[:m_par.start()]):
            return None  # «-(149,5)»: dos marcas pegadas («- (149,5)», con el guion separado, es un cero de otra columna y la cifra negativa)
        return -1 if re.match(r"\s*\)", despues) else None
    if re.match(r"\s*\)", despues) and "(" not in antes:
        return None  # (hito 2, N10) «cifra)» sin «(» en la línea: el paréntesis puede haberse abierto en la línea anterior
    if re.match("[" + marcas + r"](?!\d)", despues):
        return None  # «149,5-»: menos detrás de la cifra (un guion seguido de otra cifra es un intervalo y no la afecta)
    m = re.search("[" + marcas + r"](\s*)$", antes)
    if m:
        previo = antes[:m.start()]
        # (hito 2, N5, T8 y Q3) solo un intervalo de años crecientes y plausibles («2019-2020», «FY2023-2024», con el prefijo como palabra) o
        # una fecha («31-12-2024»); cualquier otro guion pegado entre cifras («2023-849», «Saldo 2023-1849», «9-10») deja el signo indeterminado
        # (hito 2, V2) «\Z»: el año anterior está en la misma línea, pegado al guion (no antes de un salto de línea)
        m_prev = re.search(r"(?:^|[^\w.,])(\d{4})\Z", previo) or re.search(r"(?:^|[^\w.,])(?:FY|AF|EJ)(\d{4})\Z", previo, re.I)
        tok = t[ini:fin]
        anios = (m_prev is not None and re.fullmatch(r"\d{4}", tok) is not None and 1900 <= int(m_prev.group(1)) <= int(tok) <= 2100)
        fecha = re.search(r"(?:^|[^\w.,])\d{1,2}-\d{1,2}\Z", previo) is not None and re.fullmatch(r"\d{4}", tok) is not None  # «31-12-2024»
        if m.group(1) == "" and (fecha or anios):
            return 1
        if m.group(1) == "" and (previo == "" or re.search(r"[\s:;=/\[|€$£¥]$", previo)):
            return -1
        if len(m.group(1)) >= 2 and (previo == "" or re.search(r"\s$", previo)):
            return 1  # guion aislado de otra columna (un cero), separado de la cifra por dos o más espacios
        return None
    return 1


MAX_APARICIONES_CITA = 200  # (hito 2, Q4)


def _apariciones_en_pagina(cita, pagina):
    """(4.15, hito 2, H1) Cada aparición de la cita en la página: (línea o líneas completas de la página que la contienen, inicio y fin de
    la cita en ese texto). La cifra y su signo se leen en la LÍNEA de la página, no en la cita: una cita recortada a la cifra («849697.000»
    frente a «-849697.000» o «(849,697.000)») o cortada dentro de un número («849697» de «8496970», «0» de «0,49») no cambia lo publicado."""
    palabras = str(cita or "").split()
    if not palabras or pagina is None:
        return []
    t = re.sub(r"[   ]", " ", str(pagina))
    patron = r"\s+".join(re.escape(w) for w in palabras)
    # (hito 2, N10) la cita como fragmento completo: no empieza ni acaba dentro de una palabra o de una cifra de la página («Total 5» no
    # es una aparición dentro de «Subtotal 5,01»)
    # (hito 2, T2) el límite depende de con qué empieza y acaba la cita: si es una cifra, no va pegada a otra cifra ni a un separador con
    # cifra; si es una letra, no va pegada a otra letra («849.7» cuenta en «849.7m» y en «CHF7.3»; «Total 5» no cuenta en «Subtotal 5,01»)
    patron = ((r"(?<![\d.,])(?<!\d['’])" if re.match(r"\d", palabras[0]) else r"(?<![^\W\d_])" if re.match(r"[^\W\d_]", palabras[0]) else "") + patron  # (W4) apóstrofo
              + (r"(?!\d|[.,'’]\d)" if re.search(r"\d$", palabras[-1]) else r"(?![^\W\d_])" if re.search(r"[^\W\d_]$", palabras[-1]) else ""))
    out = []
    for m in re.finditer(patron, t, re.I):
        if len(out) > MAX_APARICIONES_CITA:  # (hito 2, V5) basta saber que pasa del máximo: el coste queda acotado
            break
        ini = t.rfind("\n", 0, m.start()) + 1
        fin = t.find("\n", m.end())
        fin = len(t) if fin < 0 else fin
        # (N10) coste acotado: el contexto que decide el signo y los límites de la cifra está cerca de la cita
        ini, fin = max(ini, m.start() - 400), min(fin, m.end() + 400)
        out.append((t[ini:fin], m.start() - ini, m.end() - ini))
    return out


def _lectura_cifra(t, vf, ventana=None):
    """(estado, detalle) de la cifra vf en el texto t; con `ventana` (ini, fin), solo las apariciones de la cifra completa (límites
    evaluados en t entero) que se solapan con la ventana."""
    t = re.sub(r"[   ]", " ", str(t or ""))
    def dentro(a, b):
        # (hito 2, N4) la cifra completa tiene que estar DENTRO de la cita, no solo tocarla (la cita «0» no acredita «849697.000»)
        return ventana is None or (a >= ventana[0] and b <= ventana[1])
    if vf == 0:
        for rx in (r"(?<![\w.,])[-–—−](?![\w.,]| ?[\d(])", r"(?<=[\d)] )[-–—−](?= [\d(])"):
            if any(dentro(m.start(), m.end()) for m in re.finditer(rx, t)):
                return "ok", "cero impreso como guion"  # aislado, o entre dos cifras de columnas contiguas («784.366 - 784.366»)
    signos = []
    for c in _cifras(vf):
        for m in re.finditer(r"(?<![\d.,])(?<!\d[’])" + re.escape(c) + r"(?!\d|[.,'’]\d)", t):  # (hito 2, V7 y W3) «1'849,7» ni «1’849,7» contienen 849,7
            if dentro(m.start(), m.end()):
                signos.append(_signo_en_cita(t, m.start(), m.end()))
    if not signos:
        return "ausente", "la cifra no aparece como cifra completa"
    if vf == 0:
        return "ok", "cero"
    s = 1 if vf > 0 else -1
    vistos = sorted({"positivo" if x == 1 else "negativo" if x == -1 else "indeterminado" for x in signos})
    if s in signos and -s not in signos:
        return "ok", "signo publicado igual al de valor_fuente"
    if -s in signos and s not in signos and None not in signos:
        return "signo_distinto", f"la página la publica en {'negativo' if s == 1 else 'positivo'} y valor_fuente es {'positivo' if s == 1 else 'negativo'}"
    return "signo_indeterminado", f"apariciones de la cifra: {', '.join(vistos)}"


def _cita_cifra(cita, vf, pagina=None):
    """(4.15, R415-SIGNO) Contraste de una cifra de la fuente CON SU SIGNO. «valor_fuente» es la cifra tal como se publica, antes de aplicar
    el «signo» y la «escala» que la llevan al modelo (un pago publicado «(130,8)» es valor_fuente −130,8; con signo −1 se transforma en la
    magnitud positiva del modelo, y esa transformación sigue siendo válida). Devuelve (estado, detalle):
      «ok»: alguna aparición de la cifra (formato equivalente, R3) tiene el signo de vf y ninguna tiene el contrario;
      «signo_distinto»: la cifra solo aparece con el signo contrario (discrepancia);
      «signo_indeterminado»: aparece con signos contrarios a la vez, solo con un signo que no puede determinarse, o la cita aparece varias
          veces en la página con lecturas distintas (pendiente: no lo resuelve una declaración del revisor);
      «no_localizada»: con `pagina`, la cita no se encuentra en la página con sus palabras (pendiente);
      «ausente»: la cifra no aparece como cifra completa (discrepancia).
    (hito 2, H1) Con `pagina` (el texto de la página citada) la cifra se lee en la LÍNEA de la página donde está cada aparición de la cita:
    sus límites de cifra completa y su signo son los de la página, no los de la cita. Sin `pagina` se lee en la propia cita (solo para
    comprobaciones de formato: el contraste documental siempre la pasa).
    Un cero no tiene signo: «0», «-0», «(0)» y el guion aislado que representa un cero valen para 0."""
    if not _num(vf):
        return "ausente", "valor no numérico"
    if pagina is None:
        return _lectura_cifra(cita, vf)
    apar = _apariciones_en_pagina(cita, pagina)
    if len(apar) > MAX_APARICIONES_CITA:
        # (hito 2, Q4 y N10) una cita que aparece cientos de veces no identifica un pasaje (y leerla en todas tiene un coste no acotado)
        return "signo_indeterminado", f"la cita aparece más de {MAX_APARICIONES_CITA} veces en la página: no identifica un pasaje; hay que citar un fragmento distintivo"  # (hito 2, W5)
    if not apar:
        palabras = str(cita or "").split()
        t_ = re.sub("[" + chr(0xa0) + chr(0x202f) + chr(0x2009) + "]", " ", str(pagina))
        sueltas = list(re.finditer(r"\s+".join(re.escape(w) for w in palabras), t_, re.I)) if palabras else []
        if sueltas:
            # (hito 2, N10, R3 y T2) la cita solo está como fragmento: si el corte cae dentro de un NÚMERO, la cifra citada no es la publicada
            # (discrepancia); si cae dentro de una palabra, se pide la cita completa (pendiente)
            def en_numero(m):
                # (hito 2, Q4) coste constante (solo los caracteres vecinos) y un punto o una coma solo cuentan si forman parte de un número
                antes2 = t_[max(0, m.start() - 2):m.start()]
                # (hito 2, V3 y V7) también un decimal sin cero delante («.5», «-.5», «(.5)») y los miles con apóstrofo («1'849,7»)
                return ((re.match(r"\d", palabras[0]) is not None and re.search(r"(?:\d|\d[.,'’]|(?:^|[^\w.,])[.,])\Z", antes2) is not None)
                        or (re.search(r"\d$", palabras[-1]) is not None and re.match(r"\d|[.,'’]\d", t_[m.end():m.end() + 2]) is not None))  # (W4)
            if any(en_numero(m) for m in sueltas):
                return "ausente", "la cita empieza o acaba dentro de una cifra de la página: no es una cifra completa de la página"
            return "no_localizada", "la cita empieza o acaba dentro de una palabra de la página: hay que citar el fragmento completo"
        return "no_localizada", "la cita no se encuentra en la página con sus palabras y sus espacios: la cifra no puede leerse en ella"
    lect = [_lectura_cifra(linea, vf, (a, b)) for linea, a, b in apar]
    estados = {e for e, _ in lect}
    if len(estados) == 1:
        return lect[0]
    return "signo_indeterminado", f"la cita aparece {len(apar)} veces en la página con lecturas distintas ({', '.join(sorted(estados))})"


def _cita_contiene(cita, vf):
    """El valor de la fuente aparece en la cita como cifra completa: no dentro de otra cifra (el «0» de «2019», el «12» de «2012»), y
    (4.15, R415-SIGNO) con el signo con que se publica: «-149,5» y «(149,5)» no contienen 149,5, ni «149,5» contiene −149,5; un signo que
    no puede determinarse tampoco vale (_cita_cifra da el motivo).
    Límite declarado: en el texto extraído las columnas van a veces separadas por un solo espacio, así que «4 573,7» no se distingue
    de dos cifras («4» y «573,7»); el control lo acepta y la pertinencia es del revisor independiente.
    Un cero puede estar impreso como «-», «–» o «—» aislado (pegado o a un solo espacio de una cifra es un signo menos; con dos o más, la columna siguiente)."""
    return _cita_cifra(cita, vf)[0] == "ok"


MAX_LONGITUD_FORMULA = 2000  # (4.15, hito 2, U3) coste acotado: una fórmula de un registro auditado no necesita más
MAX_NODOS_FORMULA = 400
DECIMALES_ROUND = range(0, 13)  # (4.15, hito 2, U3) round(x, n) con n literal entre 0 y 12


def _validar_formula(formula):
    """Restricciones sintácticas de una fórmula (sin evaluarla). Devuelve el árbol; ValueError si no se admite.
    (4.15, hito 2, U3) Coste acotado: como mucho MAX_LONGITUD_FORMULA caracteres y MAX_NODOS_FORMULA nodos; round con uno o dos argumentos y
    los decimales como entero LITERAL entre 0 y 12 (un número desmesurado de decimales dejaba `comprobar` sin terminar; uno negativo anulaba
    un origen); abs con un argumento; sum con una lista; min y max con al menos un argumento; sin argumentos con nombre."""
    if not isinstance(formula, str):
        raise ValueError("la fórmula no es un texto")
    if len(formula) > MAX_LONGITUD_FORMULA:
        raise ValueError(f"fórmula de {len(formula)} caracteres: el máximo es {MAX_LONGITUD_FORMULA}")
    arbol = ast.parse(formula, mode="eval")
    if sum(1 for _ in ast.walk(arbol)) > MAX_NODOS_FORMULA:
        raise ValueError(f"fórmula con más de {MAX_NODOS_FORMULA} nodos")
    permitidos = (ast.Expression, ast.BinOp, ast.UnaryOp, ast.Constant, ast.Subscript, ast.Name, ast.Load, ast.Add, ast.Sub, ast.Mult, ast.Div,
                  ast.USub, ast.UAdd, ast.Call, ast.List, ast.Tuple, ast.Index if hasattr(ast, "Index") else ast.Constant)
    for n in ast.walk(arbol):
        if not isinstance(n, permitidos):
            raise ValueError(f"elemento no permitido en la fórmula: {type(n).__name__}")
        if isinstance(n, ast.Name) and n.id not in ("o", "abs", "min", "max", "sum", "round"):
            raise ValueError(f"nombre no permitido: {n.id}")
        if isinstance(n, ast.Call):
            if not isinstance(n.func, ast.Name) or n.func.id == "o":
                raise ValueError("solo se admiten las funciones abs, min, max, sum y round")
            f, na = n.func.id, len(n.args)
            if f == "round":
                if na not in (1, 2):
                    raise ValueError("round admite uno o dos argumentos")
                if na == 2:
                    dec = n.args[1]
                    if not (isinstance(dec, ast.Constant) and isinstance(dec.value, int) and not isinstance(dec.value, bool) and dec.value in DECIMALES_ROUND):
                        raise ValueError("round(x, n): n tiene que ser un entero literal entre 0 y 12 (4.15, hito 2, U3)")
            elif f == "abs" and na != 1:
                raise ValueError("abs admite un solo argumento")
            elif f == "sum" and not (na == 1 and isinstance(n.args[0], (ast.List, ast.Tuple))):
                raise ValueError("sum admite una sola lista de términos")
            elif f in ("min", "max") and na < 1:
                raise ValueError(f"{f} sin argumentos")
    return arbol


def _claves_formula(formula):
    """(4.15, N2) Orígenes que usa una fórmula: las claves literales de o["…"]."""
    out = set()
    for n in ast.walk(ast.parse(formula, mode="eval")):
        if isinstance(n, ast.Subscript) and isinstance(n.value, ast.Name) and n.value.id == "o":
            sl = n.slice.value if hasattr(ast, "Index") and isinstance(n.slice, getattr(ast, "Index")) else n.slice
            if isinstance(sl, ast.Constant):
                out.add(str(sl.value))
            else:
                out.add(None)  # índice no literal: no se puede saber qué origen usa
    return out


def _frac(x):
    """Número exacto desde su representación decimal (849.697 es 849697/1000, no el binario más cercano)."""
    if isinstance(x, bool) or not isinstance(x, (int, float, fractions.Fraction)):
        raise ValueError(f"valor no numérico en la fórmula: {x!r}")
    if isinstance(x, (int, fractions.Fraction)):
        return fractions.Fraction(x)
    if x != x or abs(x) == float("inf"):
        raise ValueError("valor no finito en la fórmula")
    return fractions.Fraction(repr(x))


def _round_frac(x, n=0):
    """ROUND de la hoja de cálculo (mitad lejos de cero), exacto."""
    if not isinstance(n, int) and not (isinstance(n, fractions.Fraction) and n.denominator == 1):
        raise ValueError("round(…, n) exige un entero n")
    n = int(n)
    if n not in DECIMALES_ROUND:  # (4.15, hito 2, U3) también si se llama sin pasar por _validar_formula
        raise ValueError("round(x, n): n tiene que estar entre 0 y 12")
    q = fractions.Fraction(10) ** n
    y = abs(x) * q
    e = int(y)
    if y - e >= fractions.Fraction(1, 2):
        e += 1
    return (e if x >= 0 else -e) / q


def _eval_formula_exacta(formula, o, sin_redondeo=False):
    """(4.15, tercera revisión, T1) Evalúa la fórmula con aritmética decimal EXACTA (fractions), con las mismas operaciones que
    la evaluación anterior con coma flotante (_eval_formula, retirada en el hito 2 de la 4.15: ya no la llamaba nadie); round es el de la hoja (mitad lejos de cero). `sin_redondeo` hace de round la identidad (control de sensibilidad)."""
    arbol = _validar_formula(formula)  # mismas restricciones sintácticas (lanza ValueError)

    def ev(n):
        if isinstance(n, ast.Expression):
            return ev(n.body)
        if isinstance(n, ast.Constant):
            return _frac(n.value)
        if isinstance(n, ast.Subscript):
            sl = n.slice.value if hasattr(ast, "Index") and isinstance(n.slice, getattr(ast, "Index")) else n.slice
            return _frac(o[sl.value if isinstance(sl, ast.Constant) else ev(sl)])
        if isinstance(n, ast.UnaryOp):
            v = ev(n.operand)
            return -v if isinstance(n.op, ast.USub) else v
        if isinstance(n, ast.BinOp):
            a, b = ev(n.left), ev(n.right)
            return {ast.Add: lambda: a + b, ast.Sub: lambda: a - b, ast.Mult: lambda: a * b, ast.Div: lambda: a / b}[type(n.op)]()
        if isinstance(n, (ast.List, ast.Tuple)):
            return [ev(x) for x in n.elts]
        if isinstance(n, ast.Call):
            args = [ev(x) for x in n.args]
            f = n.func.id
            if f == "round":
                return args[0] if sin_redondeo else _round_frac(*args)
            if f == "abs":
                return abs(args[0])
            seq = args[0] if len(args) == 1 and isinstance(args[0], list) else args
            return {"min": min, "max": max, "sum": sum}[f](seq)
        raise ValueError(f"elemento no permitido en la fórmula: {type(n).__name__}")
    return ev(arbol)


def _sensibilidad(formula, vals, origenes, puntos=6, semilla=415):
    """(4.15, hito 2, U4; tercera revisión, T2) Dependencia de la fórmula (sin round) respecto de cada origen, en dos sentidos:
      - local: en los valores comprobados, el resultado cambia al perturbar el origen hacia arriba o hacia abajo (v ± δ·(1 + |v|), sin
        punto fijo: un origen −1 también se perturba);
      - estructural: en puntos genéricos (racionales pseudoaleatorios con una semilla FIJA, independiente de cómo se escriba la fórmula) y
        en puntos extremos de cada origen (±10⁹, que lo hacen dominante en un max o un min), el resultado cambia con el origen.
    Devuelve (inertes, locales): un origen es inerte si no influye ni local ni estructuralmente (o[x] * 0 + c, o[x] − o[x] + o[y]); y
    `locales` son los que influyen en el punto real: si no hay ninguno, el valor es una constante en ese punto (min(o[x], c) como límite).
    Así se aceptan un producto por un cero comprobado, 0 / d y el argumento menor de un max o mayor de un min, que antes eran errores.
    (hito 2, H6) La semilla ya no depende del texto de la fórmula: dos escrituras equivalentes dan el mismo veredicto."""
    import random as _random
    delta = fractions.Fraction(1, 10 ** 7)
    base = _eval_formula_exacta(formula, vals, sin_redondeo=True)
    locales = set()
    for o in origenes:
        v_o = _frac(vals[o])
        for sg in (1, -1):
            try:
                if _eval_formula_exacta(formula, dict(vals, **{o: v_o + sg * delta * (1 + abs(v_o))}), sin_redondeo=True) != base:
                    locales.add(o)
                    break
            except ZeroDivisionError:
                locales.add(o)
                break
    vivos = set(locales)
    rnd = _random.Random(semilla)
    gen_pts = [{o: fractions.Fraction(rnd.randint(-10 ** 6, 10 ** 6), rnd.randint(1, 10 ** 3)) for o in origenes} for _ in range(puntos)]
    for o in origenes:
        for g in (1, -1):
            pt = {x: fractions.Fraction(rnd.randint(-10 ** 3, 10 ** 3), rnd.randint(1, 10)) for x in origenes}
            pt[o] = fractions.Fraction(g * 10 ** 9)
            gen_pts.append(pt)
    for gen in gen_pts:
        try:
            b = _eval_formula_exacta(formula, gen, sin_redondeo=True)
        except ZeroDivisionError:
            continue
        for o in origenes:
            if o in vivos:
                continue
            for sg in (1, -1):
                try:
                    if _eval_formula_exacta(formula, dict(gen, **{o: gen[o] + sg * (1 + abs(gen[o])) / 1000}), sin_redondeo=True) != b:
                        vivos.add(o)
                        break
                except ZeroDivisionError:
                    vivos.add(o)
                    break
    return [o for o in dict.fromkeys(origenes) if o not in vivos], locales


def _suelo_cero(formula):
    """(4.15, hito 2, H6) La fórmula tiene un 0 literal como argumento de min o max (un suelo o un techo en cero)."""
    for n in ast.walk(ast.parse(formula, mode="eval")):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in ("min", "max"):
            if any(isinstance(x, ast.Constant) and isinstance(x.value, (int, float)) and not isinstance(x.value, bool) and x.value == 0 for x in n.args):
                return True
    return False


def _constantes_no_admitidas(formula):
    """(4.15, tercera revisión, T2) Una cifra de la fuente no se escribe en la fórmula: solo se admiten como literales los enteros de 1 a
    12 (p. ej. el divisor de una media), las potencias de diez (cambios de unidad) y el número de decimales de round."""
    arbol = _validar_formula(formula)  # (4.15, hito 2, U3) longitud, nodos y argumentos antes de cualquier análisis
    exentas = set()
    for n in ast.walk(arbol):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "round" and len(n.args) == 2:
            exentas.add(id(n.args[1]))
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in ("min", "max"):
            # (4.15, hito 2, U4) un 0 como límite de min o max («max(o[a] − o[b], 0)»: una partida que no puede ser negativa)
            for x in n.args:
                if isinstance(x, ast.Constant) and isinstance(x.value, (int, float)) and not isinstance(x.value, bool) and x.value == 0:
                    exentas.add(id(x))
    malas = []
    for n in ast.walk(arbol):
        if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)) and not isinstance(n.value, bool) and id(n) not in exentas:
            v = fractions.Fraction(repr(n.value)) if isinstance(n.value, float) else fractions.Fraction(n.value)
            pot10 = v > 0 and any(v == fractions.Fraction(10) ** k for k in range(-12, 13))
            if not ((v.denominator == 1 and 1 <= v <= 12) or pot10):
                malas.append(n.value)
    return malas


def _cmp_txt(s):
    """(4.15, hallazgo 12) Forma de comparación entre el texto conservado y el extraído del PDF: NFKC (ligaduras), sin espacios, minúsculas."""
    return re.sub(r"\s+", "", unicodedata.normalize("NFKC", "" if s is None else str(s))).lower()


_PDF_CACHE = {}


def _texto_pdf(ruta, n, layout=True):
    """(4.15, hallazgo 12) («ok», texto) de la página n del PDF con pdftotext (herramienta exigida por comprobar_entorno.sh);
    («discrepancia», motivo) si no es un PDF o la página no existe; («pendiente», motivo) si no se puede extraer."""
    clave = (ruta, n, layout, _sha(ruta))
    if clave in _PDF_CACHE:
        return _PDF_CACHE[clave]
    try:
        cab = open(ruta, "rb").read(1024)
    except OSError as ex:
        return "pendiente", f"el PDF no se puede leer ({type(ex).__name__})"
    if b"%PDF-" not in cab:
        r = ("discrepancia", "el archivo de la fuente no es un PDF (sin cabecera %PDF): el texto conservado no puede ser el de ese documento")
        _PDF_CACHE[clave] = r
        return r
    import shutil as _sh
    import subprocess as _sp
    if not _sh.which("pdftotext"):
        return "pendiente", "pdftotext no está disponible: no se puede comprobar que el texto conservado es el del PDF"
    try:
        info = _sp.run(["pdfinfo", ruta], capture_output=True, text=True, timeout=60) if _sh.which("pdfinfo") else None
        m = re.search(r"^Pages:\s+(\d+)", info.stdout, re.M) if info is not None else None
        if m and n > int(m.group(1)):
            r = ("discrepancia", f"la página {n} no existe en el PDF ({m.group(1)} páginas)")
            _PDF_CACHE[clave] = r
            return r
        p = _sp.run(["pdftotext", "-q"] + (["-layout"] if layout else []) + ["-f", str(n), "-l", str(n), "-enc", "UTF-8", ruta, "-"], capture_output=True, timeout=120)
    except (OSError, _sp.SubprocessError) as ex:
        return "pendiente", f"pdftotext no pudo extraer la página {n} ({type(ex).__name__})"
    if p.returncode != 0:
        r = ("discrepancia", f"pdftotext no puede extraer la página {n} del PDF (código {p.returncode}): página inexistente o PDF ilegible")
        _PDF_CACHE[clave] = r
        return r
    r = ("ok", p.stdout.decode("utf-8", errors="replace"))
    _PDF_CACHE[clave] = r
    return r


HTML_SIN_TEXTO_VISIBLE = {"script", "style", "template", "head", "title", "noscript", "iframe", "object", "svg", "math", "select", "option", "textarea"}
HTML_EN_LINEA = {"a", "abbr", "b", "bdi", "bdo", "cite", "code", "data", "dfn", "em", "font", "i", "kbd", "mark", "q", "s", "samp", "small", "span",
                 "strong", "sub", "sup", "time", "u", "var", "wbr", "nobr", "ins", "del", "label", "big", "tt"}
HTML_EN_CABECERA = {"html", "head", "title", "meta", "link", "style", "script", "base", "noscript", "template"}
HTML_VACIOS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}


def _cmp_txt_espacios(s):
    """(4.15, hito 2, U5) Como _cmp_txt, pero conserva la separación entre palabras (un espacio): «849 697.000» no es «849697.000».
    (H7) Sin guiones blandos ni espacios de ancho cero, que no se ven."""
    t = re.sub("[\u00ad\u200b\u200c\u200d\u2060\ufeff]", "", unicodedata.normalize("NFKC", "" if s is None else str(s)))
    return re.sub(r"\s+", " ", t).strip().lower()


CODECS_TEXTO_HTML = ("shift_jis", "euc_jp", "euc_kr", "iso2022_jp", "gb2312", "gbk", "gb18030", "big5", "big5hkscs", "cp437", "cp850", "cp852",
                     "cp858", "cp866", "cp874", "mac-roman", "mac-latin2", "mac-cyrillic")  # (hito 2, T3) sin EBCDIC (cp875…) ni iso-2022-kr


def _decodificar_html(crudo):
    """(4.15, hito 2, U5) (codificación, texto) de un HTML: BOM (UTF-8, UTF-16, UTF-32), charset declarado (<meta charset>, http-equiv o
    declaración XML) o UTF-8 estricto. (None, motivo) si no puede determinarse o no decodifica: no se adivina."""
    import codecs
    for bom, cod in ((codecs.BOM_UTF32_LE, "utf-32-le"), (codecs.BOM_UTF32_BE, "utf-32-be"), (codecs.BOM_UTF8, "utf-8"),
                     (codecs.BOM_UTF16_LE, "utf-16-le"), (codecs.BOM_UTF16_BE, "utf-16-be")):
        if crudo.startswith(bom):
            try:
                return cod, crudo[len(bom):].decode(cod)
            except UnicodeDecodeError:
                return None, f"el HTML empieza con el BOM de {cod} pero no se puede decodificar con esa codificación"
    cab = crudo[:8192].decode("ascii", errors="replace")
    m = (re.search(r"""<meta[^>]*?charset\s*=\s*["']?\s*([A-Za-z0-9_.:-]+)""", cab, re.I)
         or re.search(r"""<\?xml[^>]*encoding\s*=\s*["']([A-Za-z0-9_.:-]+)""", cab, re.I))
    if m:
        cod = m.group(1)
        try:
            nombre = codecs.lookup(cod).name
        except LookupError:
            return None, f"el HTML declara la codificación {cod!r}, que no se reconoce"
        if nombre in ("latin-1", "iso8859-1", "ascii"):
            cod = "cp1252"  # (hito 2, H7) como los navegadores (WHATWG): ISO-8859-1 y ASCII se leen como windows-1252
        elif nombre in ("utf-7",) or not (nombre.startswith(("utf-", "cp125", "iso8859-", "koi8")) or nombre in CODECS_TEXTO_HTML):  # (hito 2, T3) lista explícita
            return None, f"el HTML declara {cod!r}, que no es una codificación de texto admitida"
        try:
            return cod, crudo.decode(cod)
        except UnicodeDecodeError:
            return None, f"el HTML declara la codificación {cod!r} pero no se puede decodificar con ella"
    try:
        return "utf-8", crudo.decode("utf-8")
    except UnicodeDecodeError:
        return None, "el HTML no declara su codificación y no es UTF-8 válido: no puede determinarse (no se adivina)"


def _texto_html_visible(ruta):
    """(4.15, hito 2, U5) («ok», texto visible) de una fuente HTML, o («pendiente», motivo). Con html.parser, no con expresiones regulares:
    se descartan los comentarios, los atributos, script, style, template, head (title, meta), noscript y los elementos ocultos (atributo
    hidden, style con display:none o visibility:hidden, <details> y <dialog> cerrados salvo el <summary> visible), también sin cerrar (lo
    que sigue a un <script> sin cierre no es visible); aria-hidden no oculta a la vista. Los elementos de bloque y las celdas se separan con
    un espacio; los elementos en línea y las etiquetas con espacio de nombres no. Límite declarado: lo que ocultan las clases CSS o los
    scripts no se detecta (se acepta como visible)."""
    from html.parser import HTMLParser
    try:
        crudo = open(ruta, "rb").read()
    except OSError as ex:
        return "pendiente", f"la fuente HTML no se puede leer ({type(ex).__name__})"
    cod, texto = _decodificar_html(crudo)
    if cod is None:
        return "pendiente", texto

    class _P(HTMLParser):
        def __init__(self):
            super().__init__(convert_charrefs=True)
            self.pila, self.oculto, self.trozos = [], 0, []
            # (hito 2, T3) XHTML por la extensión, como abre el archivo un navegador (no por lo que diga el contenido)
            self.xhtml = str(ruta).lower().endswith((".xhtml", ".xht"))

        def _es_oculto(self, tag, attrs):
            # (hito 2, H7) aria-hidden no oculta el texto a la vista (solo a los lectores de pantalla): no se excluye; un <dialog> sin
            # «open» no se ve; un <details> sin «open» solo deja ver su <summary> (se trata en handle_starttag)
            a = {str(k).lower(): ("" if v is None else str(v)) for k, v in attrs}
            st = re.sub(r"\s+", "", a.get("style", "").lower())
            return (tag in HTML_SIN_TEXTO_VISIBLE or "hidden" in a or "display:none" in st or "visibility:hidden" in st
                    or (tag in ("dialog", "details") and "open" not in a) or (tag == "input" and a.get("type", "").lower() == "hidden"))

        def handle_starttag(self, tag, attrs):
            tag = tag.lower()
            en_linea = tag in HTML_EN_LINEA or ":" in tag  # (hito 2, H7) etiquetas con espacio de nombres (iXBRL «ix:nonFraction»): en línea
            if not en_linea:
                self.trozos.append(" ")
            if tag in HTML_VACIOS:
                return
            if any(t == "head" for t, _ in self.pila) and tag not in HTML_EN_CABECERA:
                # (hito 2, H7) </head> omitido: un elemento del cuerpo cierra la cabecera (como en un navegador)
                while self.pila and any(t == "head" for t, _ in self.pila):
                    t, oc = self.pila.pop()
                    self.oculto -= oc
            if tag == "summary" and not self._es_oculto(tag, attrs):  # (hito 2, N6) un <summary hidden> no se ve
                det = next((oc for t, oc in reversed(self.pila) if t == "details"), None)
                if det:  # el <summary> de un <details> cerrado se ve
                    self.pila.append((tag, -1))
                    self.oculto -= 1
                    return
            oc = 0 if ":" in tag else int(bool(self._es_oculto(tag, attrs)))
            self.pila.append((tag, oc))
            self.oculto += oc

        def handle_startendtag(self, tag, attrs):
            # (hito 2, H7) la barra de cierre no vale en un elemento HTML que no es vacío («<div hidden/>» oculta lo que sigue);
            # (N6) en XHTML sí cierra el elemento («<script …/>», «<div style="display:none"/>» no ocultan lo que sigue)
            if tag.lower() in HTML_VACIOS or self.xhtml:
                if tag.lower() not in HTML_EN_LINEA:
                    self.trozos.append(" ")
            else:
                self.handle_starttag(tag, attrs)

        def handle_endtag(self, tag):
            tag = tag.lower()
            if tag not in HTML_EN_LINEA and ":" not in tag:
                self.trozos.append(" ")
            if not any(t == tag for t, _ in self.pila):
                return
            while self.pila:
                t, oc = self.pila.pop()
                self.oculto -= oc
                if t == tag:
                    break

        def handle_data(self, data):
            if not self.oculto:
                self.trozos.append(data)

    p = _P()
    try:
        p.feed(texto)
        p.close()
    except Exception as ex:  # noqa: BLE001 — un HTML mal formado no detiene el control
        return "pendiente", f"la fuente HTML no se puede analizar ({type(ex).__name__})"
    return "ok", "".join(p.trozos)


def _tipo_fuente(ruta):
    """(4.15, tercera revisión, T4) Tipo de una fuente conservada por su CONTENIDO, no por su nombre: «pdf» (cabecera %PDF-, o extensión
    .pdf: si no tiene la cabecera, _texto_pdf lo rechaza), «html», «texto» (un .txt) u «otro»."""
    try:
        cab = open(ruta, "rb").read(2048)
    except OSError:
        cab = b""
    ext = str(ruta).lower()
    texto_o_html = ext.endswith((".htm", ".html", ".xhtml", ".txt")) or cab.lstrip()[:1] == b"<"
    if cab.lstrip().startswith(b"%PDF-") or ext.endswith(".pdf") or (b"%PDF-" in cab[:1024] and not texto_o_html):
        # (4.15, hito 2, U5 y H7) la cabecera puede ir tras bytes previos (como lo acepta pdftotext), salvo en un HTML o un texto que la mencionen
        return "pdf"
    c = cab.lstrip().lower()
    if ext.endswith((".htm", ".html", ".xhtml")) or c.startswith((b"<!doctype html", b"<html")):
        return "html"
    if ext.endswith(".txt"):
        return "texto"
    return "otro"


def _contiene_texto(hay, aguja):
    """(4.15, hallazgo 12) Un valor de texto aparece en la cita como palabra completa («EUR» no vale dentro de «NEURROS»)."""
    a, h = _norm_txt(aguja), _norm_txt(hay)
    return bool(a) and re.search(r"(?<!\w)" + re.escape(a) + r"(?!\w)", h) is not None


def cargar(carpeta):
    p = os.path.join(carpeta, REGISTRO)
    if not os.path.exists(p):
        return None, None
    try:
        d = json.load(open(p, encoding="utf-8"))
    except (OSError, ValueError) as e:
        return None, f"{REGISTRO} no se puede leer ({type(e).__name__})"
    if not isinstance(d, dict) or not isinstance(d.get("entradas"), list):
        return None, f"{REGISTRO} no tiene la estructura esperada (objeto con «entradas»)"
    if str(d.get("formato") or "") not in FORMATOS_ADMITIDOS:
        return None, f"{REGISTRO} tiene el formato {d.get('formato')!r}, que no es ninguno de {FORMATOS_ADMITIDOS}"
    return d, None


def perimetro_esperado(carpeta, reg):
    """El perímetro que declara el registro para el expediente (p. ej., «consolidado» o «consolidado · operaciones continuadas»)."""
    return str((reg or {}).get("perimetro_del_expediente") or "").strip() or None


ENTRADAS_FCF_BASE = tuple(f"Análisis!{c}" for c in ("C46", "C47", "C48", "C49", "C50"))


def entradas_no_reproducibles(carpeta, inst):
    """(4.15, C48 de Elis; revisión independiente, hallazgo 4) Entradas del FCF base con valor en el libro que la vía generativa no reproduce:
    fase1_v63.json declara otro valor, no la declara (o la declara sin número), o no hay fase1_v63.json legible (no se puede determinar).
    {celda: (valor del libro, valor declarado, motivo)}. Falla en cerrado."""
    decl = _f1_declaraciones(carpeta)
    out = {}
    for k in ENTRADAS_FCF_BASE:
        if k not in inst["celdas"]:
            continue
        vl = inst["celdas"].get(k)
        if vl is None or vl == "":
            continue
        if decl is None:
            out[k] = (vl, None, "no hay fase1_v63.json legible: no se puede determinar si la vía generativa reproduce la entrada efectiva")
            continue
        d = decl.get(k.split("!")[1])
        vf = d.get("valor") if isinstance(d, dict) else d
        if not _num(vf):
            out[k] = (vl, vf, "fase1_v63.json no declara esta entrada con un número: el libro la sostiene solo por el valor de la etapa 1")
        elif not _num(vl) or abs(vf - vl) > 1e-9 * max(1.0, abs(vf), abs(vl)):
            out[k] = (vl, vf, "fase1_v63.json (la vía generativa) declara otro valor: el libro lo sostiene solo por el valor migrado de la etapa 1")
    return out


def contraste_pagina(carpeta, k, f, ruta, vf):
    """(4.15, R1) Contraste de la cita en la página citada de una fuente local. None si pasa; si no, (categoría, motivo).
    El texto examinable es el propio archivo si es .txt con marcas «[PDF PAGE n]», o «archivo_texto» (con su «sha256_texto») si la
    fuente conservada es un PDF, un HTML u otro formato. Sin texto examinable, la página no puede examinarse: pendiente."""
    if str(ruta).lower().endswith(".txt") and _tipo_fuente(ruta) == "texto":
        ruta_txt = ruta
    else:
        ruta_txt = _ruta_fuente(carpeta, f.get("archivo_texto"))
        if not f.get("archivo_texto"):
            return "pendiente", f"la fuente {f.get('archivo')} no es un texto con marcas de página y no declara «archivo_texto»: la página citada no puede examinarse"
        if ruta_txt is None:
            return "pendiente", f"el texto de la fuente {f.get('archivo_texto')!r} no existe: la página citada no puede examinarse"
        if not f.get("sha256_texto"):
            return "pendiente", f"el texto de la fuente {f.get('archivo_texto')!r} no tiene «sha256_texto»: no se puede comprobar que es el examinado"
        if _sha(ruta_txt) != str(f["sha256_texto"]).strip().lower():
            return "desactualizada", f"el texto de la fuente {f.get('archivo_texto')} cambió (sha256_texto distinto del registrado)"
    estado, pag = _pagina_examinable(ruta_txt, f.get("pagina"))
    if estado != "ok":
        return estado, f"{pag} ({f.get('archivo_texto') or f.get('archivo')})"
    if not _norm_txt(f.get("cita")):
        return "pendiente", "la cita está vacía (tras normalizar los espacios): no hay pasaje que contrastar"
    if _norm_txt(f.get("cita")) not in _norm_txt(pag):
        return "discrepancia", f"la cita no está en la página {f.get('pagina')} de {f.get('archivo_texto') or f.get('archivo')}"
    tipo_f = _tipo_fuente(ruta)
    textos_fuente = []  # (hito 2, N3) el texto del propio documento (PDF u HTML) en el que también se lee la cifra con su signo
    if tipo_f == "html":
        # (4.15, tercera revisión, T4) una fuente HTML: la cita tiene que estar en su texto, no solo en el texto conservado
        # (4.15, hito 2, U5) en su texto VISIBLE (html.parser: sin comentarios, atributos, script, style, template, head ni elementos ocultos),
        # decodificado por su BOM o su charset declarado; las celdas y bloques se separan (una cifra no se forma con dos celdas contiguas)
        est_h, plano = _texto_html_visible(ruta)
        if est_h == "ok":
            textos_fuente.append(re.sub("[\u00ad\u200b\u200c\u200d\u2060\ufeff]", "", plano))  # (T4) sin caracteres invisibles
        if est_h != "ok":
            return est_h, f"{plano} ({f.get('archivo')})"
        if _cmp_txt_espacios(f.get("cita")) not in _cmp_txt_espacios(plano):
            return "discrepancia", f"la cita está en el texto conservado {f.get('archivo_texto')!r}, pero no en el texto visible de la fuente HTML {f.get('archivo')!r}"
    elif tipo_f == "otro" and not str(ruta).lower().endswith(".txt"):
        return "pendiente", (f"la fuente {f.get('archivo')!r} no es un PDF, un HTML ni un texto con marcas de página: no se puede comprobar que el texto "
                             "conservado es el de la fuente (tercera revisión, T4)")
    if tipo_f == "pdf":
        # (4.15, segunda revisión, hallazgo 12) el texto conservado tiene que ser el del PDF: la cita está en esa página del propio PDF
        # (con «-layout», como texto_con_marcas de cambiar_base.py, y sin él: el orden de las columnas puede cambiar entre los dos modos)
        est_pdf, txt_pdf = _texto_pdf(ruta, _numero_pagina(f.get("pagina")))
        if est_pdf != "ok":
            return est_pdf, f"{txt_pdf} ({f.get('archivo')})"
        if not txt_pdf.strip() and not _texto_pdf(ruta, _numero_pagina(f.get("pagina")), layout=False)[1].strip():
            return "pendiente", (f"la página {f.get('pagina')} del PDF {f.get('archivo')!r} no tiene capa de texto (pdftotext no extrae nada): el texto "
                                 "conservado (p. ej. un OCR) no se puede contrastar con el PDF; lo revisa el revisor independiente")
        txt_pdf2 = _texto_pdf(ruta, _numero_pagina(f.get("pagina")), layout=False)[1]
        textos_fuente += [txt_pdf, txt_pdf2]
        # (4.15, hito 2) límite declarado (cuarta revisión, U5 B6): una página cuya única capa de texto es un encabezado (escaneado con sello
        # digital) da «discrepancia»; distinguirla de una página corta legítima exigiría un umbral heurístico, que no se adopta
        if _cmp_txt(f.get("cita")) not in _cmp_txt(txt_pdf) and _cmp_txt(f.get("cita")) not in _cmp_txt(txt_pdf2):
            return "discrepancia", (f"la cita está en el texto conservado {f.get('archivo_texto')!r}, pero no en la página {f.get('pagina')} del PDF "
                                    f"{f.get('archivo')!r} (pdftotext): el texto conservado no es el de ese documento")
    if vf is not None and not _num(vf):
        # (4.15, hallazgo 12) un dato publicado de TEXTO: la cita tiene que contener el valor (o una equivalencia declarada en «equivalencia»)
        eq = [_norm_txt(x) for x in ([vf] + ([f.get("equivalencia")] if f.get("equivalencia") else [])) if _norm_txt(x)]
        if not any(_contiene_texto(f.get("cita"), x) for x in eq):
            return "discrepancia", f"la cita no contiene el valor de texto {vf!r} (ni una equivalencia declarada en «equivalencia»)"
        return None
    if vf is not None:
        # (4.15, R415-SIGNO) la cifra publicada se contrasta CON SU SIGNO; «signo» y «escala» son la transformación hacia el modelo
        est, det = _cita_cifra(f.get("cita"), vf, pag)
        if est == "ok" and _num(vf):
            # (hito 2, N3) en un PDF o un HTML, la cifra y su signo también se leen en el documento: si el texto conservado perdió el
            # paréntesis o el menos, la lectura del documento (donde la cita se localiza) manda
            lect = [_cita_cifra(f.get("cita"), vf, tf) for tf in textos_fuente]
            otras = [x for x in lect if x[0] != "no_localizada"]
            peor = next((x for x in otras if x[0] in ("signo_distinto", "ausente")), None) or next((x for x in otras if x[0] != "ok"), None)
            if peor:
                est, det = peor[0], peor[1] + " (en el documento de la fuente, no en el texto conservado)"
            elif lect and not otras:
                # (hito 2, T4) la cita está en el documento (contraste sin espacios) pero no con sus palabras: el signo no puede leerse en él
                est, det = "no_localizada", "la cita está en el documento de la fuente, pero no con sus palabras separadas igual: la cifra y su signo no pueden leerse en él"
        if est == "ausente":
            return "discrepancia", f"la cita no contiene el valor de la fuente {vf!r} como cifra completa de la página (formato equivalente, sin redondear)"
        if est == "signo_distinto":
            return "discrepancia", (f"la página no publica el valor de la fuente {vf!r} con su signo ({det}): «valor_fuente» es la cifra publicada "
                                    "con su signo; «signo» y «escala» la transforman después hacia el modelo (R415-SIGNO)")
        if est in ("signo_indeterminado", "no_localizada"):
            return "pendiente", (f"el signo con que la página publica {vf!r} no puede determinarse ({det}): hace falta una cita en la "
                                 "que la cifra publicada y su signo sean inequívocos; una declaración del revisor no lo sustituye (R415-SIGNO)")
    return None


def comprobar(carpeta, _presellar=frozenset()):
    """Informe de la verificación: cobertura, entradas comprobadas, pendientes, desactualizadas, discrepancias y errores del contrato, con la
    aptitud por entradas. Nunca lanza: un registro ausente o ilegible es «no verificado», y una entrada mal formada es un error del contrato.
    `_presellar` (solo para `sellar`): celdas cuyo vínculo se da por escrito para saber si pasan todos los demás controles."""
    inst = universo(carpeta)
    out = {"formato": FORMATO, "universo": (inst or {}).get("n"), "huella_entradas_economicas": (inst or {}).get("huella"), "registro": None,
           "por_clase": {}, "comprobadas": [], "pendientes": [], "desactualizadas": [], "discrepancias": [], "errores": [], "sin_entrada": [],
           "sobrantes": [], "repetidas": [], "auxiliares": 0, "materiales_no_comprobadas": [], "apto_por_entradas": False, "motivo": None,
           "lecturas_externas": [], "universo_calculo": (inst or {}).get("n_calculo"), "universo_juicio": (inst or {}).get("n_juicio"),
           "no_materiales": [], "datos_como_hipotesis": [], "entradas_no_reproducibles": [], "no_materiales_sin_revisar": [],
           "no_materiales_revisados": [], "no_aplicables": [], "claves_lecturas_externas": [], "resumen": None, "derivados_comprobados": []}
    if inst is None:
        out["motivo"] = "no hay libro del expediente: no se puede fijar el universo de entradas"
        out["resumen"] = out["motivo"]  # (T6) nunca None
        return out
    reg, err = cargar(carpeta)
    if reg is None:
        out["motivo"] = err or f"no hay {REGISTRO}: ninguna entrada financiera está verificada (un Excel evaluado anterior no acredita nada)"
        out["sin_entrada"] = sorted(inst["celdas"])
        out["pendientes"] = [f"{k}: sin entrada en el registro" for k in out["sin_entrada"]]
        out["materiales_no_comprobadas"] = [k for k in out["sin_entrada"] if inst["tipos"].get(k) != "hipótesis"]
        out.update(comprobadas_universo=0, comprobadas_calculo=0, comprobadas_juicio=0)  # (4.15, I9) «0 de N», nunca «None de N»
        out["resumen"] = out["motivo"]  # (T6) nunca None
        return out
    out["registro"] = REGISTRO
    out["formato_registro"] = reg.get("formato")
    evid = evidencia_libro(carpeta)
    try:
        huellas = huellas_registro(carpeta, reg, evid)
    except Exception:  # noqa: BLE001  (registro mal formado: ninguna huella vigente)
        huellas = {}
    en_curso = set()
    anios = _anios(inst)
    per_esp = perimetro_esperado(carpeta, reg)
    unidad_modelo = str(inst["celdas"].get("Control maestro!J4") or "mm").strip().lower()
    vistos, por_celda = set(), {}
    for e in reg["entradas"]:
        if not isinstance(e, dict):
            out["errores"].append("una entrada no es un objeto")
            continue
        k = str(e.get("celda") or "")
        if k in vistos:
            out["repetidas"].append(k)
            continue
        vistos.add(k)
        por_celda[k] = e
    for k in inst["celdas"]:
        if k not in por_celda:
            out["sin_entrada"].append(k)
    for k in por_celda:
        if not k.startswith("aux:") and k not in inst["celdas"]:
            out["sobrantes"].append(k)
    out["auxiliares"] = len([k for k in por_celda if k.startswith("aux:")])
    estado = {}  # celda → «comprobada» / «pendiente» / «desactualizada» / «discrepancia» / «error»

    def problema(k, cat, motivo):
        estado[k] = cat
        out[{"error": "errores", "pendiente": "pendientes", "desactualizada": "desactualizadas", "discrepancia": "discrepancias"}[cat]].append(f"{k}: {motivo}")

    def _depende_de_hipotesis(k, vistos_=None):
        vistos_ = set() if vistos_ is None else vistos_
        e = por_celda.get(k) or {}
        d = e.get("derivacion") if isinstance(e.get("derivacion"), dict) else {}
        for o in (d.get("origenes") or []) if e.get("clase") == "derivado" else []:
            o = str(o)
            if o in vistos_:
                continue
            vistos_.add(o)
            eo = por_celda.get(o) or {}
            if eo.get("clase") in ("hipotesis", "convencion") or _depende_de_hipotesis(o, vistos_):
                return True
        return False

    def revisar_una(k, e):
        en_curso.add(k)
        try:
            return _revisar_una(k, e)
        except Exception as ex:  # noqa: BLE001  (4.15, observación 21: nunca lanza)
            return problema(k, "error", f"entrada mal formada ({type(ex).__name__}: {str(ex)[:100]})")
        finally:
            en_curso.discard(k)

    def _revisar_una(k, e):
        clase = e.get("clase")
        if not isinstance(clase, str):
            return problema(k, "error", f"clase {clase!r} no es una de {CLASES}")
        out["por_clase"][clase] = out["por_clase"].get(clase, 0) + 1
        if clase not in CLASES:
            return problema(k, "error", f"clase {clase!r} no es una de {CLASES}")
        tipo_u = inst["tipos"].get(k)
        if tipo_u == "hipótesis" and clase not in ("hipotesis", "convencion"):
            return problema(k, "error", f"la celda es una hipótesis del modelo ({inst['ids'].get(k)}): no se presenta como {clase}")
        # (4.15, revisión independiente, hallazgo 1) una entrada de cálculo es material por definición (relación de entradas materiales);
        # una de juicio solo deja de serlo con su justificación, y se lista
        if e.get("material") is False:
            if not k.startswith("aux:") and inst["ambito"].get(k) == "calculo":
                return problema(k, "error", "una entrada de cálculo es material por definición: «material: false» no se admite")
            if not str(e.get("justificacion_materialidad") or "").strip():
                return problema(k, "error", "«material: false» sin «justificacion_materialidad»")
            out["no_materiales"].append(k)
        # (4.15, hallazgo 2) un DATO del modelo presentado como hipótesis o convención exige su justificación de clase y la revisión
        # independiente completa, y se lista aparte; «no aplicable» no se admite con un valor distinto de cero en el libro
        dato_como_hip = clase in ("hipotesis", "convencion") and tipo_u == "dato"
        if dato_como_hip:
            if not str(e.get("justificacion_clase") or "").strip():
                return problema(k, "error", f"la celda es un dato del modelo ({inst['ids'].get(k)}) presentado como {clase} sin «justificacion_clase»")
            out["datos_como_hipotesis"].append(k)
        if clase == "no_aplicable" and not k.startswith("aux:") and _num(inst["celdas"].get(k)) and inst["celdas"].get(k) != 0:
            return problema(k, "error", f"no aplicable con un valor en el libro ({inst['celdas'].get(k)!r}): es un dato que hay que contrastar")
        if clase == "no_aplicable" and not k.startswith("aux:"):
            out["no_aplicables"].append(k)  # (4.15, N2) se cuentan aparte, también con el registro apto
        if clase in ("hipotesis", "convencion"):
            h = e.get("hipotesis") or {}
            falta = [c for c in ("fundamento", "alternativas", "limites") if not h.get(c)]
            if falta:
                return problema(k, "error", f"{clase} sin {', '.join(falta)} (una hipótesis conserva su identificación, fundamento, alternativas y límites)")
            if e.get("fuente", {}) and (e.get("fuente") or {}).get("valor_fuente") is not None:
                return problema(k, "error", f"{clase} presentada con un valor de fuente: no es un dato publicado")
        if not k.startswith("aux:"):
            actual = inst["celdas"].get(k)
            if not _igual_exacto(actual, e.get("valor_modelo")):  # (4.15, hallazgo 5) vigencia exacta
                return problema(k, "desactualizada", f"el libro dice {actual!r} y el registro {e.get('valor_modelo')!r}: la comprobación no vale para el dato actual")
        if clase in ("dato_publicado", "cero_comprobado"):
            f = e.get("fuente") if isinstance(e.get("fuente"), dict) else {}
            conserv = str(f.get("conservacion") or ("local" if f.get("archivo") else "")).strip().lower()
            if conserv not in CONSERVACION:
                return problema(k, "pendiente", "la fuente no declara un archivo local conservado ni una lectura externa («conservacion»): no hay evidencia que examinar")
            falta = [c for c in CAMPOS_FUENTE if f.get(c) in (None, "")]
            if falta:
                return problema(k, "pendiente", f"faltan campos del contraste documental: {', '.join(falta)}")
            ruta = None
            if conserv == "local":
                # (4.15, R2) una fuente local tiene que existir con su huella: si falta, el contraste no es reproducible (las
                # declaraciones del extractor y del revisor no sustituyen la comprobación de la evidencia)
                ruta = _ruta_fuente(carpeta, f.get("archivo"))
                if ruta is None:
                    return problema(k, "pendiente", f"la fuente local {f.get('archivo')!r} no está en el expediente ni en el paquete: su contraste no es reproducible")
                if not f.get("sha256"):
                    return problema(k, "pendiente", f"la fuente local {f.get('archivo')!r} no tiene sha256 registrado: no se puede comprobar que es la que se examinó")
                if _sha(ruta) != str(f["sha256"]).strip().lower():
                    return problema(k, "desactualizada", f"la fuente {f.get('archivo')} cambió (sha256 distinto del registrado)")
            else:
                le = f.get("lectura_externa") if isinstance(f.get("lectura_externa"), dict) else {}
                falta_le = [c for c in CAMPOS_LECTURA_EXTERNA if not str(le.get(c) or "").strip()]
                if falta_le:
                    return problema(k, "pendiente", f"lectura externa sin {', '.join(falta_le)} (sin bytes conservados, la evidencia, la fecha y las limitaciones tienen que ser explícitas)")
            esc, sig, vf = f.get("escala"), f.get("signo"), f.get("valor_fuente")
            vm = e.get("valor_modelo") if k.startswith("aux:") else inst["celdas"].get(k)
            if vm is None and (_num(vf) or clase == "cero_comprobado"):
                return problema(k, "discrepancia", f"la celda está vacía en el libro y la fuente publica {vf!r}: vacío no es cero (dato ausente ≠ cero comprobado)")
            if not _num(vm):
                # dato publicado de texto (moneda, unidad, norma, mercado…): el valor de la fuente es el del modelo, sin escala ni signo
                if _norm_txt(vf) != _norm_txt(vm):
                    return problema(k, "discrepancia", f"el valor de la fuente {vf!r} no es el del modelo {vm!r}")
                if conserv == "local":
                    r_pag = contraste_pagina(carpeta, k, f, ruta, vf)  # (4.15, hallazgo 12) la cita de un dato de texto contiene su valor
                    if r_pag:
                        return problema(k, *r_pag)
                return revisar_comprobacion(k, e, externa=conserv == "externa")
            if not (_num(esc) and sig in (1, -1, "+1", "-1") and _num(vf)):
                return problema(k, "error", "escala, signo (+1/−1) o valor_fuente no numéricos")
            sig = int(sig)
            u = UNIDADES.get(_norm_txt(f.get("unidad")))
            um = UNIDADES.get(unidad_modelo, 1.0)
            if u is None and _unidad_monetaria_no_reconocida(f.get("unidad")):
                # (4.15, hito 2, U7) «miles de €», «en miles de euros», «MM€», «USD (millones)»…: una unidad monetaria que el vocabulario no
                # reconoce no puede quedar como «no monetaria» (solo con una potencia de diez); su escala no se puede comprobar
                return problema(k, "pendiente", f"unidad monetaria no reconocida «{f.get('unidad')}»: la escala {esc!r} no se puede contrastar con ella "
                                                "(se escribe con el vocabulario de UNIDADES; una conversión de divisa es un derivado con el tipo de cambio como origen)")
            if u is not None and _num(um) and um and not _igual_exacto(esc, u / um):
                return problema(k, "error", f"escala {esc!r} incoherente con las unidades (fuente «{f.get('unidad')}» → modelo «{unidad_modelo}» = {u / um!r})")
            if u is None and not any(_igual_exacto(esc, 10.0 ** k_) for k_ in range(-12, 13)):
                # (4.15, tercera revisión) con una unidad no monetaria (o no reconocida) la escala solo puede ser un cambio de unidad
                return problema(k, "error", f"escala {esc!r} con la unidad «{f.get('unidad')}»: fuera de las unidades monetarias reconocidas la escala tiene que ser una potencia de diez")
            importe = u is not None  # (4.15, hallazgo 5) la tolerancia del redondeo del libro solo vale para importes en unidades monetarias
            # (4.15, hito 2, U2) en un importe, signo × escala × valor_fuente se calcula EXACTO (fracciones) y se compara con el redondeo del libro
            if not (_importe_libro_exacto(sig * _frac(esc) * _frac(vf), vm) if importe else _igual_exacto(sig * esc * vf, vm)):
                return problema(k, "discrepancia", f"signo × escala × valor_fuente = {sig * esc * vf!r} ≠ valor del modelo {vm!r}")
            if sig == -1 and re.sub(r"[\s.,;:()¡!¿?«»\"']+", " ", _norm_txt(f.get("tratamiento"))).strip() in ("", "ninguno", "ninguna", "-", "—", "no", "n/a", "na", "sin tratamiento", "none"):
                # (4.15, hito 2, H14) un cambio de signo es una transformación: se declara su tratamiento (p. ej. «pago publicado entre paréntesis»)
                return problema(k, "error", "signo −1 con el tratamiento «ninguno»: el cambio de signo de la cifra publicada se declara en «tratamiento»")
            if clase == "cero_comprobado" and not _igual_exacto(vm, 0):
                return problema(k, "error", "cero comprobado con un valor distinto de cero")
            m = re.match(r"^Historia!([C-L])(\d+)$", k)
            if m and anios[COL_ANIO[m.group(1)]] is not None:
                anio = str(int(anios[COL_ANIO[m.group(1)]])) if _num(anios[COL_ANIO[m.group(1)]]) else str(anios[COL_ANIO[m.group(1)]])
                if anio not in str(f.get("periodo")) and anio not in str(f.get("columna")):
                    return problema(k, "error", f"la columna {m.group(1)} de la Historia es {anio}, pero el período declarado es «{f.get('periodo')}» (columna «{f.get('columna')}»)")
            if per_esp and _norm_txt(f.get("perimetro")) != _norm_txt(per_esp) and not str(f.get("perimetro_justificacion") or "").strip():
                return problema(k, "error", f"perímetro «{f.get('perimetro')}» distinto del del expediente «{per_esp}» sin justificación")
            if conserv == "local":
                r_pag = contraste_pagina(carpeta, k, f, ruta, vf)
                if r_pag:
                    return problema(k, *r_pag)
            return revisar_comprobacion(k, e, externa=conserv == "externa")
        elif clase == "derivado":
            d = e.get("derivacion") if isinstance(e.get("derivacion"), dict) else {}
            if not d.get("origenes") or not d.get("formula") or not str(d.get("conciliacion") or "").strip():
                return problema(k, "pendiente", "derivado sin orígenes, fórmula o conciliación")
            if not isinstance(d["origenes"], list) or not all(isinstance(o, str) and o for o in d["origenes"]) or not isinstance(d["formula"], str):
                return problema(k, "error", "«origenes» tiene que ser una lista de celdas o auxiliares y «formula» un texto (tercera revisión, T3)")
            try:
                ctes = _constantes_no_admitidas(d["formula"])
            except (SyntaxError, ValueError) as ex:
                return problema(k, "error", f"fórmula no evaluable ({type(ex).__name__}: {str(ex)[:80]})")
            if ctes:
                return problema(k, "error", f"la fórmula escribe cifras {ctes!r}: una cifra de la fuente entra como origen, con su clase y su revisión "
                                            "(solo se admiten enteros de 1 a 12, potencias de diez y los decimales de round)")
            try:
                usadas = _claves_formula(d["formula"])
            except (SyntaxError, ValueError) as ex:
                return problema(k, "error", f"fórmula no evaluable ({type(ex).__name__}: {str(ex)[:80]})")
            if usadas != {str(o) for o in d["origenes"]}:
                # (4.15, N2) una fórmula constante, o que no usa todos sus orígenes, no deriva el valor de ellos
                return problema(k, "error", f"la fórmula usa {sorted(map(str, usadas))} y los orígenes declarados son {sorted(map(str, d['origenes']))}: "
                                            "un derivado se calcula con todos sus orígenes y solo con ellos")
            vals = {}
            for o in d["origenes"]:
                if o not in por_celda:
                    return problema(k, "pendiente", f"el origen {o} no tiene entrada en el registro")
                if o in en_curso:
                    return problema(k, "error", f"derivación circular: {o} depende de {k}")
                if por_celda[o].get("clase") not in ("dato_publicado", "cero_comprobado", "derivado", "hipotesis", "convencion"):
                    # (4.15, tercera revisión, T2) un dato ausente o no aplicable no lleva un número del que derivar otro
                    return problema(k, "error", f"el origen {o} es de clase {por_celda[o].get('clase')!r}: un derivado solo se obtiene de datos publicados, ceros comprobados, "
                                                "otros derivados o hipótesis y convenciones declaradas")
                if o not in estado:
                    revisar_una(o, por_celda[o])
                if estado.get(o) != "comprobada":
                    return problema(k, "pendiente", f"el origen {o} no está comprobado ({estado.get(o)})")
                vals[o] = por_celda[o].get("valor_modelo") if o.startswith("aux:") else inst["celdas"].get(o)
            try:
                # (4.15, tercera revisión, T1) aritmética decimal exacta: 120,4 − 120,4 es 0 sin tolerancia, y la comparación es relativa al
                # resultado, no a los orígenes
                r_ex = _eval_formula_exacta(d["formula"], vals)
                r = float(r_ex)
                # (T2) cada origen tiene que influir en el resultado (sin round): o["x"] * 0 + c, o["x"] − o["x"] + c o min(o["x"], c) no derivan
                inertes, locales = _sensibilidad(d["formula"], vals, list(d["origenes"]))
            except Exception as ex:  # noqa: BLE001
                return problema(k, "error", f"fórmula no evaluable ({type(ex).__name__}: {str(ex)[:80]})")
            if inertes:
                return problema(k, "error", f"los orígenes {inertes} no influyen en el resultado de la fórmula: el valor no se deriva de ellos")
            if not locales and not (r_ex == 0 and _suelo_cero(d["formula"])):
                # (hito 2, H6) salvo el 0 de un suelo o techo declarado («max(o[a] − o[b], 0)» cuando actúa): es la regla de la fórmula
                return problema(k, "error", "con los valores comprobados, el resultado no depende de ningún origen (es una constante en ese punto: p. ej. "
                                            "min(o[x], c) como límite): el valor no se deriva de ellos (hito 2, U4)")
            vm = e.get("valor_modelo") if k.startswith("aux:") else inst["celdas"].get(k)
            importe = UNIDADES.get(_norm_txt(d.get("unidad"))) is not None  # (4.15, N4) el redondeo del libro, solo en importes
            if not (_importe_libro_exacto(r_ex, vm) if importe else _igual_exacto(r, vm)):  # (4.15, hito 2, U2) exacto, en los dos sentidos del empate
                return problema(k, "discrepancia", f"la fórmula da {r!r} y el modelo {vm!r} (" + ("ni exacto ni con el redondeo del libro a 3 decimales" if importe else
                                                    "no es exacto; el redondeo del libro a 3 decimales solo vale en un importe («derivacion.unidad»)")
                                + "; una transformación distinta se declara en la fórmula, p. ej. round(…, 4))")
            # (4.15, N2) un DATO que se obtiene de una hipótesis o convención (directa o indirectamente) es un dato presentado como hipótesis
            if not k.startswith("aux:") and tipo_u == "dato" and _depende_de_hipotesis(k):
                if not str(e.get("justificacion_clase") or "").strip():
                    return problema(k, "error", f"la celda es un dato del modelo ({inst['ids'].get(k)}) derivado de una hipótesis o convención sin «justificacion_clase»")
                out["datos_como_hipotesis"].append(k)
        elif clase in ("dato_ausente", "no_aplicable"):
            if not str(e.get("justificacion") or "").strip():
                return problema(k, "pendiente", f"{clase} sin justificación")
            if k.startswith("aux:") and _num(e.get("valor_modelo")) and e.get("valor_modelo") != 0:
                return problema(k, "error", f"un auxiliar {clase} con un número ({e.get('valor_modelo')!r}): sin dato no hay valor (tercera revisión, T2)")
            if clase == "dato_ausente" and _num(inst["celdas"].get(k)) and not k.startswith("aux:"):
                return problema(k, "error", "dato ausente con un valor en el libro: es un dato (o un cero) que hay que contrastar")
        return revisar_comprobacion(k, e)

    def revisar_comprobacion(k, e, externa=False):
        clase = e.get("clase")
        c = e.get("comprobacion") if isinstance(e.get("comprobacion"), dict) else {}
        es_hip = clase in ("hipotesis", "convencion") and inst["tipos"].get(k) != "dato"  # (hallazgo 2) un dato como hipótesis se revisa entero
        if es_hip and c.get("resultado") == "discrepancia":
            # (14-nov-2026, hallazgo del revisor RD) una hipótesis o convención no exige revisor, pero si un revisor registra una
            # discrepancia (p. ej. su fundamento ya no describe el dato vigente), cuenta: antes se ignoraba y el registro salía «apto»
            return problema(k, "discrepancia", f"el revisor registra una discrepancia en la {clase}: {str(c.get('nota') or e.get('incidencia') or '')[:120]}")
        if es_hip and c.get("resultado") == "pendiente":
            # (14-nov-2026, hallazgo de la orquestación) una hipótesis o convención cuyo registro queda explícitamente «pendiente»
            # (p. ej. texto sustituido a la espera de la confirmación del revisor) no está comprobada: antes contaba como comprobada
            return problema(k, "pendiente", f"la {clase} tiene la comprobación pendiente: {str(c.get('nota') or '')[:120]}")
        if not es_hip:
            if c.get("resultado") not in RESULTADOS:
                return problema(k, "pendiente", "sin resultado de la comprobación")
            if c.get("resultado") == "discrepancia":
                return problema(k, "discrepancia", f"el revisor registra una discrepancia: {str(c.get('nota') or e.get('incidencia') or '')[:120]}")
            if c.get("resultado") == "pendiente":
                return problema(k, "pendiente", "comprobación pendiente")
            if not str(c.get("extractor") or "").strip() or not str(c.get("revisor") or "").strip() or _norm_txt(c.get("extractor")) == _norm_txt(c.get("revisor")):
                return problema(k, "error", "la comprobación exige un revisor independiente del extractor (los dos declarados y distintos)")
            if not str(c.get("fuente_examinada") or "").strip():
                return problema(k, "error", "el revisor no declara qué fuente examinó (no basta con aceptar el registro del extractor)")
        # (4.15, I13) la comprobación vale para el fundamento, la evidencia y la transformación que se examinaron, no solo para el número
        v = c.get("vinculo") if isinstance(c.get("vinculo"), dict) else {}
        if k not in _presellar:
            if not v.get("huella"):
                return problema(k, "pendiente", "la comprobación no está vinculada a su fundamento, evidencia y transformación (registro anterior a la 4.15 o sin sellar): hay que revisarla de nuevo")
            if v.get("huella") != huellas.get(k):
                return problema(k, "desactualizada", "el fundamento, la evidencia, la transformación, sus orígenes o la propia comprobación cambiaron después de la revisión "
                                                     "(huella del vínculo distinta): la comprobación no vale aunque el número coincida")
            if _norm_txt(v.get("sellado_por")) != _norm_txt(c.get("revisor")) or str(v.get("fecha") or "") != str(c.get("fecha") or ""):
                return problema(k, "desactualizada", "el vínculo no lo selló el revisor registrado en la fecha de la comprobación")
        if externa:
            estado[k] = "externa"
            out["claves_lecturas_externas"].append(k)
            out["lecturas_externas"].append(f"{k}: lectura externa sin bytes conservados ({str(((e.get('fuente') or {}).get('lectura_externa') or {}).get('referencia'))[:100]}); no es un contraste reproducible")
            return
        estado[k] = "comprobada"
        if e.get("clase") == "derivado":
            # (4.15, hito 2, U1) los derivados se cuentan y se listan: el control descarta las fórmulas triviales, pero no acredita que la
            # fórmula derive el concepto; eso lo acredita solo la revisión independiente de su significado económico (revisor y vínculo)
            out["derivados_comprobados"].append(k)

    for k, e in por_celda.items():
        if k not in estado:
            revisar_una(k, e)
    # (4.15, C48 de Elis) una entrada del FCF base que la vía generativa no reproduce no se acredita, aunque su registro esté comprobado
    # (4.15, C48 de Elis; hallazgo 4) una entrada del FCF base que la vía generativa no reproduce no se acredita y BLOQUEA, sea cual sea el
    # estado o la materialidad de su registro
    for k, (vl, vf, por_que) in entradas_no_reproducibles(carpeta, inst).items():
        motivo = (f"el libro tiene {vl!r} y fase1_v63.json declara {vf!r}: {por_que}; no es reproducible desde las entradas declaradas: hay que "
                  f"declarar su cálculo (fase1_metadatos.json o CAMBIO.analisis)")
        out["entradas_no_reproducibles"].append(f"{k}: {motivo}")
        if estado.get(k) == "comprobada":
            estado[k] = "discrepancia"
            out["discrepancias"].append(f"{k}: {motivo}")
    # (4.15, segunda revisión, N1) una entrada de juicio no material que no está comprobada solo deja de bloquear si un revisor independiente
    # revisó y selló el juicio de materialidad (su justificación entra en la huella); si no, bloquea como cualquier entrada material
    for k in out["no_materiales"]:
        if estado.get(k) == "comprobada":
            continue
        e = por_celda.get(k) or {}
        c = e.get("comprobacion") if isinstance(e.get("comprobacion"), dict) else {}
        v = c.get("vinculo") if isinstance(c.get("vinculo"), dict) else {}
        just = re.sub(r"\W", "", str(e.get("justificacion_materialidad") or ""))
        falta = []
        if estado.get(k) not in ("pendiente", "externa"):
            falta.append(f"su estado es «{estado.get(k)}»")
        if len(just) < 20:
            falta.append("la justificación de la materialidad no explica nada (menos de 20 caracteres)")
        if c.get("resultado") != "verificado" or not str(c.get("fuente_examinada") or "").strip():
            falta.append("sin resultado «verificado» ni fuente examinada del revisor")
        if not str(c.get("extractor") or "").strip() or not str(c.get("revisor") or "").strip() or _norm_txt(c.get("extractor")) == _norm_txt(c.get("revisor")):
            falta.append("sin revisor independiente del extractor")
        if k not in _presellar and (v.get("huella") != huellas.get(k) or _norm_txt(v.get("sellado_por")) != _norm_txt(c.get("revisor"))
                                    or str(v.get("fecha") or "") != str(c.get("fecha") or "")):
            falta.append("sin vínculo vigente sellado por el revisor")
        if falta:
            out["no_materiales_sin_revisar"].append(f"{k}: declarada no material, pero {'; '.join(falta)}: bloquea como una entrada material")
        else:
            out["no_materiales_revisados"].append(k)
    out["comprobadas"] = sorted(k for k, v in estado.items() if v == "comprobada")
    # (14-nov-2026, aviso de la auditoría) «comprobadas» incluye los datos de origen auxiliares; la cobertura del universo se cuenta aparte
    out["comprobadas_universo"] = sum(1 for k in inst["celdas"] if estado.get(k) == "comprobada")
    out["comprobadas_calculo"] = sum(1 for k in inst["celdas"] if estado.get(k) == "comprobada" and inst["ambito"].get(k) == "calculo")
    out["comprobadas_juicio"] = sum(1 for k in inst["celdas"] if estado.get(k) == "comprobada" and inst["ambito"].get(k) == "juicio")
    for k in out["sin_entrada"]:
        out["pendientes"].append(f"{k}: sin entrada en el registro")
    # (4.15) toda celda MATERIAL del universo que no está comprobada bloquea, también una hipótesis o convención pendiente (sin vínculo,
    # con la comprobación explícitamente pendiente) y una lectura externa sin bytes; (14-nov-2026) ya bloqueaba la hipótesis pendiente
    mat_no = [k for k in inst["celdas"] if (por_celda.get(k) or {}).get("material", True) is not False and estado.get(k) != "comprobada"]
    out["materiales_no_comprobadas"] = mat_no
    bloqueos = (out["sin_entrada"] or out["sobrantes"] or out["repetidas"] or out["errores"] or out["desactualizadas"] or out["discrepancias"] or mat_no
                or out["entradas_no_reproducibles"] or out["no_materiales_sin_revisar"])
    out["apto_por_entradas"] = not bloqueos
    # (4.15, N1 y N2) el resumen se da siempre, también con el registro apto: lo que no se contrastó y por qué se ve en el informe
    out["resumen"] = (f"{out['comprobadas_universo']} de {inst['n']} celdas del universo comprobadas ({out['comprobadas_calculo']} de {inst['n_calculo']} de cálculo y "
                      f"{out['comprobadas_juicio']} de {inst['n_juicio']} de juicio); {len(out['no_materiales'])} entradas declaradas no materiales (de juicio o auxiliares) "
                      f"({len(out['no_materiales_revisados'])} con el juicio de materialidad revisado, {len(out['no_materiales_sin_revisar'])} sin revisar); "
                      f"{len(out['datos_como_hipotesis'])} datos tratados como hipótesis o convención; {len(out['no_aplicables'])} no aplicables; "
                      f"{len(out['lecturas_externas'])} lecturas externas sin bytes; {len(out['derivados_comprobados'])} derivados comprobados (su significado "
                      "económico lo acredita la revisión independiente, no el control automático)")
    if bloqueos:
        out["motivo"] = (f"{out['comprobadas_universo']} de {inst['n']} celdas del universo comprobadas ({out['comprobadas_calculo']} de {inst['n_calculo']} de cálculo y "
                         f"{out['comprobadas_juicio']} de {inst['n_juicio']} de juicio; +{out['auxiliares']} datos de origen auxiliares); "
                         f"{len(out['lecturas_externas'])} lecturas externas sin bytes; {len(out['entradas_no_reproducibles'])} entradas del FCF base no reproducibles; "
                         f"{len(out['datos_como_hipotesis'])} datos tratados como hipótesis o convención; {len(out['no_materiales'])} entradas de juicio no materiales "
                         f"({len(out['no_materiales_sin_revisar'])} sin el juicio de materialidad revisado); {len(out['no_aplicables'])} no aplicables; "
                         f"{len(mat_no)} entradas materiales sin comprobar; {len(out['desactualizadas'])} desactualizadas; {len(out['discrepancias'])} discrepancias; "
                         f"{len(out['errores'])} errores del contrato; {len(out['sin_entrada'])} sin entrada")
    return out


def aptitud(carpeta):
    """(apto_por_entradas, resumen) para la ficha y el informe."""
    r = comprobar(carpeta)
    return r["apto_por_entradas"], {"universo": r["universo"], "comprobadas": len(r["comprobadas"]), "comprobadas_universo": r.get("comprobadas_universo"), "auxiliares": r["auxiliares"],
                                    "universo_calculo": r.get("universo_calculo"), "universo_juicio": r.get("universo_juicio"),
                                    "comprobadas_calculo": r.get("comprobadas_calculo"), "comprobadas_juicio": r.get("comprobadas_juicio"),
                                    "lecturas_externas": len(r.get("lecturas_externas") or []), "formato_registro": r.get("formato_registro"),
                                    "entradas_no_reproducibles": len(r.get("entradas_no_reproducibles") or []), "datos_como_hipotesis": len(r.get("datos_como_hipotesis") or []),
                                    "no_materiales": len(r.get("no_materiales") or []), "no_materiales_sin_revisar": len(r.get("no_materiales_sin_revisar") or []),
                                    "no_aplicables": len(r.get("no_aplicables") or []), "resumen": r.get("resumen"),
                                    "derivados_comprobados": len(r.get("derivados_comprobados") or []),
                                    "pendientes": len(r["pendientes"]), "desactualizadas": len(r["desactualizadas"]), "discrepancias": len(r["discrepancias"]),
                                    "errores": len(r["errores"]), "materiales_no_comprobadas": len(r["materiales_no_comprobadas"]),
                                    "apto_por_entradas": r["apto_por_entradas"], "motivo": r["motivo"], "huella_entradas_economicas": r["huella_entradas_economicas"],
                                    "nota": ("condición necesaria, no suficiente, para presentar una conclusión como apta para dinero real; los controles automáticos "
                                             "comprueban cobertura, conciliaciones y coherencia, no la corrección semántica (revisión independiente de las fuentes)")}


def plantilla(carpeta):
    """Esqueleto del registro con una entrada por celda del universo (clase propuesta según el tipo de la instantánea) y valor_modelo del libro."""
    inst = universo(carpeta)
    ents = []
    for k, v in inst["celdas"].items():
        t = inst["tipos"].get(k)
        ents.append({"celda": k, "id": inst["ids"].get(k), "ambito": inst["ambito"].get(k), "uso": None, "material": True,
                     "clase": "hipotesis" if t == "hipótesis" else None, "valor_modelo": v, "fuente": {}, "derivacion": None, "hipotesis": None,
                     "justificacion": None, "comprobacion": {"extractor": None, "revisor": None, "fecha": None, "resultado": "pendiente", "fuente_examinada": None, "nota": None, "vinculo": None},
                     "incidencia": None})
    d = {"formato": FORMATO, "empresa": os.path.basename(os.path.abspath(carpeta)), "libro": os.path.basename(libro_de(carpeta)),
         "huella_entradas_economicas": inst["huella"], "perimetro_del_expediente": None, "entradas": ents}
    json.dump(d, open(os.path.join(carpeta, "verificacion_entradas.plantilla.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    return d


def sellar(carpeta, celdas, revisor, fecha):
    """(4.15, I13) El REVISOR vincula su comprobación al fundamento, la evidencia y la transformación que acaba de examinar, entrada por
    entrada. (Revisión independiente, hallazgos 3 y 15) Se niega:
      - si no se da la lista explícita de celdas;
      - si `fecha` no es la fecha del día (la del sistema): una comprobación fechada antes no se sella, hay que revisarla y fecharla de nuevo;
      - si la entrada no tiene ese revisor (distinto del extractor), el resultado «verificado», la fuente examinada y esa misma fecha;
      - si la entrada no pasa TODOS los controles automáticos (se evalúan como si el vínculo estuviera escrito).
    Registra `sellado_en` (marca de tiempo) y solo escribe el registro si sella alguna entrada. Límite declarado: un registro JSON no impide
    que alguien escriba el vínculo a mano; el vínculo detecta cambios, no acredita quién lo escribió. Eso lo cubre que el registro forma parte
    del material auditado (cierre_v2.MATERIAL_FIJO) y la auditoría independiente. Devuelve (selladas, rechazadas)."""
    if not celdas:
        raise SystemExit("sellar exige la lista explícita de celdas revisadas")
    hoy = dt.datetime.now().astimezone().date().isoformat()  # (4.15, N3) solo la fecha del sistema
    if str(fecha) != hoy:
        raise SystemExit(f"sellar solo sella la revisión de hoy ({hoy}); la fecha {fecha!r} no lo es: una comprobación anterior se revisa y se fecha de nuevo")
    reg, err = cargar(carpeta)
    if reg is None:
        raise SystemExit(err or f"no hay {REGISTRO}")
    por = {str(e.get("celda")): e for e in reg["entradas"] if isinstance(e, dict)}
    candidatas, mal = [], []
    for k in celdas:
        e = por.get(k)
        c = (e or {}).get("comprobacion") if isinstance((e or {}).get("comprobacion"), dict) else {}
        if e is None:
            mal.append(f"{k}: no tiene entrada"); continue
        if _norm_txt(c.get("revisor")) != _norm_txt(revisor) or not str(revisor).strip():
            mal.append(f"{k}: el revisor registrado es {c.get('revisor')!r}, no {revisor!r}"); continue
        if _norm_txt(c.get("extractor")) == _norm_txt(revisor):
            mal.append(f"{k}: el revisor es el extractor"); continue
        if c.get("resultado") != "verificado" or not str(c.get("fuente_examinada") or "").strip():
            mal.append(f"{k}: sin resultado «verificado» o sin fuente examinada"); continue
        if str(c.get("fecha") or "") != hoy:
            mal.append(f"{k}: la fecha de la comprobación ({c.get('fecha')}) no es la de esta revisión ({hoy})"); continue
        candidatas.append(k)
    r = comprobar(carpeta, _presellar=frozenset(candidatas)) if candidatas else {"comprobadas": [], "lecturas_externas": []}
    validas = set(r.get("comprobadas") or []) | set(r.get("claves_lecturas_externas") or []) | set(r.get("no_materiales_revisados") or [])  # (N8; N1)
    ok = []
    for k in candidatas:
        if k not in validas:
            cats = ("no_materiales_sin_revisar", "errores", "discrepancias", "desactualizadas", "pendientes")  # (T6) primero el motivo de la no material
            motivos = [x for cat in cats for x in r.get(cat) or [] if x.startswith(k + ": ")]
            mal.append(f"{k}: no pasa los controles automáticos ({(motivos or ['sin motivo registrado'])[0][:200]})")
        else:
            ok.append(k)
    if ok:
        huellas = huellas_registro(carpeta, reg)
        ahora = dt.datetime.now().astimezone().isoformat(timespec="seconds")
        for k in ok:
            por[k]["comprobacion"]["vinculo"] = {"huella": huellas[k], "elementos": ELEMENTOS_VINCULO, "sellado_por": revisor, "fecha": hoy, "sellado_en": ahora}
        # las huellas de los derivados que dependen de lo sellado no cambian por el sello (el vínculo no entra en la huella)
        reg["formato"] = FORMATO
        json.dump(reg, open(os.path.join(carpeta, REGISTRO), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    return ok, mal


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "sellar":
        import argparse
        ap = argparse.ArgumentParser()
        ap.add_argument("accion"); ap.add_argument("carpeta"); ap.add_argument("celdas", nargs="+")
        ap.add_argument("--revisor", required=True); ap.add_argument("--fecha", required=True)
        a = ap.parse_args()
        ok, mal = sellar(a.carpeta, a.celdas, a.revisor, a.fecha)
        print(f"selladas {len(ok)} · rechazadas {len(mal)}")
        for x in mal:
            print("  " + x)
        sys.exit(0 if not mal else 1)
    if len(sys.argv) < 3 or sys.argv[1] not in ("comprobar", "plantilla"):
        print(__doc__)
        sys.exit(2)
    if sys.argv[1] == "plantilla":
        d = plantilla(sys.argv[2])
        print(f"plantilla con {len(d['entradas'])} entradas")
        sys.exit(0)
    r = comprobar(sys.argv[2])
    if "--json" in sys.argv:
        print(json.dumps(r, ensure_ascii=False, indent=1, default=str))
    else:
        print(f"universo {r['universo']} · comprobadas del universo {r.get('comprobadas_universo')} · comprobadas en total {len(r['comprobadas'])} · pendientes {len(r['pendientes'])} · desactualizadas {len(r['desactualizadas'])} · "
              f"discrepancias {len(r['discrepancias'])} · errores {len(r['errores'])} · auxiliares {r['auxiliares']} · apto por entradas: {r['apto_por_entradas']}")
        for cat in ("errores", "discrepancias", "desactualizadas"):
            for x in r[cat][:10]:
                print(f"  {cat}: {x}")
        if r["motivo"]:
            print("  motivo: " + r["motivo"])
        print("  resumen: " + str(r.get("resumen")))
    sys.exit(0 if r["apto_por_entradas"] else 1)
