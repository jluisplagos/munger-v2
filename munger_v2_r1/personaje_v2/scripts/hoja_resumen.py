#!/usr/bin/env python3
"""Hoja resumen en lenguaje llano de un expediente CERRADO y VIGENTE (reorientación §7; criterios K5 y K9 de la lectura del informe).

Uso:
  hoja_resumen.py EXPEDIENTE [--salida DIR] [--trabajo DIR] [--lock ARCHIVO] [--espera-cerrojo S] [--cerrojo-ya-tomado]
                  [--tasas 0.07,0.08,0.09,0.10,0.11] [--antecedente]
  hoja_resumen.py EXPEDIENTE --comprobar        (¿la hoja que hay sigue siendo la del análisis oficial vigente?)
  hoja_resumen.py EXPEDIENTE --verificar-origen (¿cada frase del personaje sale, tal cual, de lo que escribió?)

Puerta (ronda 1 de la revisión crítica, hallazgos 1–4). La hoja no puede decir más que la ficha oficial:
  - solo se genera si el análisis oficial está VIGENTE con la misma comprobación que el cierre oficial (cierre_v2.motivo_vigencia:
    auditoría APROBADO de ese material, material sin cambios desde la auditoría, aprobación no retirada, F1 vigente y utilizable
    cuando se exige) y además hay un cierre registrado (cierre_vigente.json, ficha.cierre.auditoria = APROBADO) y el pipeline lo
    terminó. Con --antecedente se puede generar sobre un expediente que no es vigente, pero sale rotulada «NO VIGENTE · ANTECEDENTE»
    arriba y --comprobar nunca la da por vigente;
  - el veredicto sale de la ficha (estado, causa, decisión, objetivo, condición, fundamento, alcance), no de precio.json: sin
    conclusión oficial la hoja lo dice y no presenta el precio de Sí de la hoja de cálculo como precio de compra;
  - la aptitud se compone de aptitud_de_uso, verificacion_entradas y motor_a_f1 de la ficha; la hoja nunca dice «apto para dinero
    real» (no se acredita superando controles de software);
  - con cualquier código de error no se escribe hoja y la anterior, si la hay, se aparta como hoja_resumen.NO_VIGENTE.*;
  - la huella de hoja_resumen.md se guarda en hoja_resumen.json: una edición a mano se detecta.

Lee del expediente: ficha.json, informe.md, precio.json, resultados.json, fase_c.json, estado_pipeline.json, el libro evaluado
<E>_v63_evaluada.xlsx y, si existen, cierre_vigente.json, fase1_metadatos.json, fase1_fuentes.json y fase1_v63.json. Escribe en el
expediente (o en --salida) dos archivos propios: hoja_resumen.md (para leer) y hoja_resumen.json (trazabilidad: huellas de lo leído y
de la página, origen de cada frase y la tabla de sensibilidad con sus cifras exactas).

Lo que NO hace:
  - no cambia ningún archivo del expediente y no es una salida oficial: es material de estudio que se genera después del cierre;
  - no escribe ningún hecho ni cifra de la empresa propios: las frases son del personaje (tesis Análisis!B101, tesis inversa B102,
    `cambiaria_de_cubo` y `decision.condiciones_revision` de fase_c.json), limpiadas solo de referencias a celdas y páginas; los demás
    textos son fijos (iguales para todas las empresas) o campos de la ficha copiados;
  - la sensibilidad a la tasa se calcula en COPIAS del libro evaluado en las que solo cambia Análisis!C56 (r), recalculadas con
    LibreOffice (recalc.sh) bajo `flock -w` del cerrojo común en cada recálculo (no envolver este programa en flock del mismo cerrojo:
    se esperaría a sí mismo; si ya se tiene el cerrojo, usar --cerrojo-ya-tomado). Las copias se borran al terminar.

Códigos: 0 hecho (o hoja vigente con --comprobar) · 2 uso · 3 expediente no cerrado, no vigente, incompleto o mal formado ·
4 hoja desactualizada, no vigente, editada o ausente (--comprobar) / frase sin origen o contenido mínimo incumplido ·
5 la sensibilidad a la tasa del análisis no reproduce el precio de Sí de precio.json · 6 fallo del recálculo o de la lectura.
"""
import argparse
import datetime as dt
import glob
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import precio_de_si as PS  # noqa: E402
from v63_xml import LibroV63  # noqa: E402

VERSION_HOJA = "2.0"
TASAS = (0.07, 0.08, 0.09, 0.10, 0.11)
CELDA_TASA = ("Análisis", "C56")
_LOCK_COMUN = "/home/user/e_work/libreoffice.lock"
LOCK_DEFECTO = os.environ.get("HOJA_RESUMEN_LOCK") or (
    _LOCK_COMUN if os.path.isdir(os.path.dirname(_LOCK_COMUN)) else os.path.join(tempfile.gettempdir(), "munger_libreoffice.lock"))
ESPERA_CERROJO = 900
SALIDA_MD, SALIDA_JSON = "hoja_resumen.md", "hoja_resumen.json"
SUFIJO_NO_VIGENTE = ".NO_VIGENTE"
OBLIGATORIOS = ("ficha.json", "informe.md", "precio.json", "resultados.json", "fase_c.json", "estado_pipeline.json")
OPCIONALES = ("cierre_vigente.json", "fase1_metadatos.json", "fase1_fuentes.json", "fase1_v63.json")
DIAS_PRECIO_ANTIGUO = 90

# Textos fijos (iguales para todas las empresas): propuesta de redacción del §4 de la revisión crítica
ZONA_LLANA = {
    "bajo_malo": "por debajo de lo que valdría en su escenario malo (que no es un suelo: puede ir peor)",
    "cumple_regla_k": "en el precio de Sí o por debajo (cumple la regla de precio; no basta para comprar: ver la conclusión)",
    "vigilar": "por encima del precio de Sí y por debajo del valor medio: aún no compraría",
    "caro": "más caro que el valor medio de los tres escenarios",
}
ESTADO_LLANO = {
    "concluido": "concluido", "pendiente_de_datos": "pendiente de datos", "pendiente_de_investigacion": "pendiente de investigación",
    "no_entregable": "no entregable", "modelo_no_aplicable": "modelo no aplicable", "limite_del_modelo": "límite del modelo",
    "fallo_de_implementacion": "fallo de implementación",
}
CONCLUSION_LLANA = {
    "comprar": "Compraría al precio del análisis. Es la conclusión del personaje, no una recomendación.",
    "esperar": "No comprar ahora; esperar a mejor precio.",
    "descartar": "La descarta.",
}
OBJETIVO_LLANO = {
    "bloqueado": "bloqueado: la ficha no emite precio de compra",
    "emitido_condicionado": "emitido con condiciones (provisional)",
    "emitido": "emitido",
}
GLOSARIO = (
    ("Precio de Sí", r"precio de s[ií]", "el precio por acción al que el personaje compraría, o menos. Lo da la hoja de cálculo con una regla experimental."),
    ("Escenarios MALO, NORMAL y BUENO", r"\b(?:MALO|NORMAL|BUENO)\b|escenario", "tres historias posibles del negocio, cada una con un valor por acción."),
    ("Valor medio (valor ponderado)", r"ponderad|valor medio", "la media de los tres escenarios según la probabilidad que el personaje da a cada uno."),
    ("Tasa", r"\btasas?\b", "la rentabilidad anual mínima que el análisis le pide a la inversión. Cuanto más alta, menos vale la empresa en el cálculo."),
    ("Categoría (Sí, Vigilar, No, Demasiado difícil)", r"Vigilar|Demasiado difícil|categoría", "dónde coloca el personaje a la empresa: comprarla, seguirla esperando mejor precio, descartarla o dejarla por no saber valorarla."),
    ("ROIC", r"\bROIC\b", "lo que gana el negocio al año por cada euro invertido en él."),
    ("EBIT y margen EBIT", r"\bEBIT\b", "el beneficio de explotación; el margen EBIT es lo que queda de cada 100 € de ventas antes de intereses e impuestos."),
    ("EBITDA", r"\bEBITDA\b", "el beneficio de explotación antes de restar la amortización."),
    ("Capex", r"\bcapex\b", "lo que la empresa invierte en instalaciones y equipos."),
    ("Amortización", r"amortizaci", "el desgaste anual de instalaciones y equipos, que se resta como gasto."),
    ("Foso", r"\bfoso\b", "la ventaja que protege a la empresa de sus competidores."),
    ("Crecimiento orgánico", r"orgánic", "el de las ventas sin contar compras de empresas ni el efecto de las divisas."),
    ("Caja libre", r"caja libre|\bFCF\b", "el dinero que queda al año después de pagar la operación y las inversiones."),
    ("Deuda neta y apalancamiento", r"deuda neta|apalancamiento", "la deuda menos la caja; el apalancamiento la compara con el beneficio de explotación (en «veces»)."),
    ("mm", r"\bmm\b", "millones (de la moneda del análisis)."),
    ("Recompra", r"recompra", "la compra de sus propias acciones por la empresa."),
    ("Dividendo", r"dividendo", "el reparto de beneficios a los accionistas."),
    ("Motor A y motor B", r"\bmotor [AB]\b", "dos maneras de calcular el valor en la hoja de cálculo; el personaje elige una al principio del análisis."),
    ("F1", r"\bF1\b", "la revisión pendiente de cómo el motor A trata los arrendamientos; mientras no esté validada, el motor A no se da por bueno para concluir."),
    ("Tasa heredada", r"heredad", "la tasa que viene de la primera etapa del análisis; todavía no está decidida."),
)
MESES = ("enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre")
MONEDA = {"EUR": "€", "USD": "US$", "GBP": "£"}
FUENTE_TEXTO = {
    "B101": "tesis (Análisis!B101)",
    "B102": "tesis inversa (Análisis!B102)",
    "cambiaria_de_cubo.a_no": "«qué me haría cambiar de cubo»: a No",
    "cambiaria_de_cubo.a_si": "«qué me haría cambiar de cubo»: a Sí",
    "cambiaria_de_cubo.a_demasiado_dificil": "«qué me haría cambiar de cubo»: a Demasiado difícil",
    "decision.condiciones_revision.a_la_baja": "condición de revisión a la baja",
    "decision.condiciones_revision.al_alza": "condición de revisión al alza",
}
ROTULO_FALSO = (
    ("cambiaria_de_cubo.a_no", "Lo descartaría si…"),
    ("cambiaria_de_cubo.a_si", "Lo compraría si…"),
    ("cambiaria_de_cubo.a_demasiado_dificil", "Lo dejaría por demasiado difícil si…"),
    ("decision.condiciones_revision.a_la_baja", "Bajaría el precio de Sí si…"),
    ("decision.condiciones_revision.al_alza", "Subiría el precio de Sí si…"),
)


class ErrorExpediente(Exception):
    pass


# ------------------------------------------------------------------------------------------------ utilidades
def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def sha256_texto(t):
    return hashlib.sha256(t.encode("utf-8")).hexdigest()


def cargar(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def cargar_dict(path, nombre=None):
    """(hallazgo 13) Un JSON ilegible o con otra forma es un expediente mal formado (código 3), nunca una traza de Python."""
    try:
        d = cargar(path)
    except (OSError, ValueError) as e:
        raise ErrorExpediente(f"{nombre or os.path.basename(path)} no se puede leer como JSON ({type(e).__name__}: {str(e)[:120]})")
    if not isinstance(d, dict):
        raise ErrorExpediente(f"{nombre or os.path.basename(path)} no tiene la forma esperada (un objeto JSON; es {type(d).__name__})")
    return d


def es_num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def num_es(x, dec=2):
    """1312.5 → «1.312,50»."""
    s = f"{x:,.{dec}f}"
    return s.replace(",", "\x00").replace(".", ",").replace("\x00", ".")


def dinero(x, moneda):
    if not es_num(x):
        return "—"
    simb = MONEDA.get(moneda, moneda or "")
    return f"{num_es(x)} {simb}".strip()


def pct(x, dec=1):
    if not es_num(x):
        return str(x) if x not in (None, "") else "—"
    return f"{num_es(100 * x, dec)} %"


def tasa_txt(r):
    """(hallazgo 12) 0,09 → «9 %»; 0,085 → «8,5 %» (sin redondear una tasa no entera a la de al lado)."""
    if not es_num(r):
        return str(r)
    for dec in (0, 1, 2):
        if abs(round(100 * r, dec) - 100 * r) < 1e-9:
            return pct(r, dec)
    return pct(r, 2)


def fecha_larga(f):
    """'2028-04-30' (o serial de Excel) → «30 de abril de 2028»; lo que no es fecha se devuelve tal cual."""
    if es_num(f):
        f = (dt.date(1899, 12, 30) + dt.timedelta(days=int(f))).isoformat()
    if isinstance(f, str):
        m = re.match(r"^(\d{4})-(\d{2})-(\d{2})", f)
        if m:
            a, me, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
            return f"{d} de {MESES[me - 1]} de {a}"
    return str(f) if f not in (None, "") else "no consta"


def fecha_iso(f):
    if es_num(f):
        return (dt.date(1899, 12, 30) + dt.timedelta(days=int(f))).isoformat()
    return f


def a_fecha(f):
    f = fecha_iso(f)
    if isinstance(f, str):
        m = re.match(r"^(\d{4})-(\d{2})-(\d{2})", f)
        if m:
            try:
                return dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
            except ValueError:
                return None
    return None


def recortar(texto, n=360):
    """Recorta un campo de la ficha por el final de una frase (o de una palabra) y dice que sigue en la ficha."""
    t = re.sub(r"\s+", " ", str(texto or "")).strip()
    if len(t) <= n:
        return t
    corte = max(t.rfind(". ", 0, n), t.rfind("; ", 0, n))
    if corte < n // 3:
        corte = t.rfind(" ", 0, n)
    return t[:max(corte, 1)].rstrip(" ,;:") + " … (sigue en la ficha)"


# ------------------------------------------------------------------------------------------------ frases y limpieza
ABREVIATURAS = {"p", "pp", "ee", "uu", "sr", "sra", "núm", "aprox", "vs", "cf", "s.a", "art", "ed", "vol", "fig", "pág"}


def frases(texto):
    """Parte un texto del personaje en frases. No corta dentro de paréntesis, corchetes ni comillas, ni tras abreviaturas
    («p. 104», «EE. UU.», iniciales como «W. Kurtz»). Devuelve las frases tal cual (subcadenas exactas del texto)."""
    if not isinstance(texto, str):
        return []
    out, ini, prof, i, n = [], 0, 0, 0, len(texto)
    abre, cierra = "([«“", ")]»”"
    while i < n:
        ch = texto[i]
        if ch in abre:
            prof += 1
        elif ch in cierra:
            prof = max(0, prof - 1)
        elif ch in ".!?" and prof == 0 and i + 1 < n and texto[i + 1] == " ":
            j = i + 1
            while j < n and texto[j] == " ":
                j += 1
            sig = texto[j] if j < n else ""
            sig2 = texto[j + 1] if j + 1 < n else ""
            empieza = sig.isupper() or sig in "«¿¡“\"" or (sig.isdigit() and sig2 == ")")
            m = re.search(r"([\wÁÉÍÓÚÑáéíóúñ.]+)$", texto[ini:i])
            previa = m.group(1) if m else ""
            abrev = previa.lower().rstrip(".") in ABREVIATURAS or (len(previa) == 1 and previa.isupper())
            if empieza and not abrev:
                out.append(texto[ini:i + 1].strip())
                ini = j
                i = j
                continue
        i += 1
    resto = texto[ini:].strip()
    if resto:
        out.append(resto)
    return [f for f in out if f]


_HOJAS = r"(?:Historia|Palancas|Análisis|Diagnóstico V6|Motor|Control maestro|Panel|Sector|Riesgo país|Configuración V6\.4|Conciliación B)"
_CELDA = r"\$?[A-Z]{1,3}\$?\d{1,3}(?::\$?[A-Z]{1,3}\$?\d{1,3})?"
_REF = re.compile(
    r"^(?:"
    rf"(?:{_HOJAS}[!\s])?{_CELDA}"                                   # Historia C55 · Palancas!H18 · C37 · B78:D78
    rf"|(?:{_HOJAS}\s)?filas?\s+[\w–-]+"                            # Historia fila 29 · fila id
    rf"|{_HOJAS}|series? de la hoja"                                 # Historia · series de la hoja
    r"|(?:extracto\s+)?§\s?\d+"                                      # extracto §5
    r"|(?:extracto\s+)?[A-Z][A-Za-z]*[_ ]?\d{2,4}(?:,?\s*PDF)?\s+pp?\.\s?\d+(?:[–-]\d+)?"   # extracto AR25 p. 10 · AR_2025, PDF p. 17
    r")$")


# Las citas de Munger («…» (AIWTK p.36; HIM)) NO se quitan: sin ellas, la cita parecería del personaje.


def _es_referencia(parte):
    # (hallazgo 6) «Historia filas 29 y 33» es una sola referencia: la «y» une dos filas, no dos elementos
    parte = re.sub(r"(filas\s+[\w–-]+)\s+y\s+([\w–-]+)", r"\1–\2", parte)
    items = [x.strip() for x in re.split(r",\s*|\s+y\s+", parte.strip()) if x.strip()]
    return bool(items) and all(_REF.match(x) for x in items)


def _parentesis(m):
    """Dentro de un paréntesis, quita las partes (separadas por «; ») y, dentro de cada parte, los elementos (separados por «, »)
    que son solo referencias; si no queda nada, quita el paréntesis entero."""
    previo, contenido = m.group(1), m.group(2)
    quedan, cambia = [], False
    for parte in re.split(r";\s*", contenido):
        if _es_referencia(parte):
            cambia = True
            continue
        elems = re.split(r",\s+", parte)
        utiles = [e for e in elems if not _es_referencia(e)]
        if len(utiles) != len(elems):
            cambia = True
        quedan.append(", ".join(utiles))
    if not cambia:
        return m.group(0).replace("(", "\x01").replace(")", "\x02")  # se conserva (marcado para no volver a tratarlo)
    if not quedan:
        return ""
    return f"{previo}\x01{'; '.join(q.strip() for q in quedan)}\x02"


def limpiar(frase):
    """Quita de una frase del personaje SOLO lo que es referencia (corchetes de fuente, paréntesis o partes de paréntesis que son
    celdas, filas, hojas o páginas) y el ordinal inicial «1)». No añade ni cambia ninguna palabra ni cifra."""
    t = re.sub(r"\s*\[[^\[\]]*\]", "", frase)
    for _ in range(4):
        t2 = re.sub(r"(\s*)\(([^()\x01\x02]*)\)", _parentesis, t)
        if t2 == t:
            break
        t = t2
    t = t.replace("\x01", "(").replace("\x02", ")")
    t = re.sub(r"^\s*\d{1,2}\)\s*", "", t)
    t = re.sub(r"\s+([,.;:)])", r"\1", t)
    t = re.sub(r"\(\s+", "(", t)
    t = re.sub(r"[ \t]{2,}", " ", t)
    return t.strip()


def _cifras(t):
    return re.findall(r"\d+(?:[.,]\d+)*", t)


def _n_palabras(t):
    return len(re.findall(r"[\wÁÉÍÓÚÑáéíóúñ]+", t or ""))


def obtener_campo(fase_c, campo):
    if campo in ("B101", "B102"):
        return (fase_c.get("celdas") or {}).get(campo)
    v = fase_c
    for k in campo.split("."):
        v = (v or {}).get(k) if isinstance(v, dict) else None
    return v


def texto_con_origen(fase_c, campo):
    """Un campo entero del personaje, frase a frase, limpiado de referencias (cada frase con su campo e índice)."""
    return [{"campo": campo, "indice": i, "original": f, "texto": limpiar(f)} for i, f in enumerate(frases(obtener_campo(fase_c, campo)))]


def seleccionar_por_que(fase_c):
    """(hallazgo 5) La tesis y la tesis inversa ENTERAS, frase a frase: no se salta ninguna salvedad («Pero…», el precio, el riesgo
    concreto). No hay selección mecánica: se muestran todas las frases que escribió el personaje en esos dos campos."""
    return {"tesis": [e for e in texto_con_origen(fase_c, "B101") if e["texto"]],
            "tesis_inversa": [e for e in texto_con_origen(fase_c, "B102") if e["texto"]]}


def verificar_origen_frases(frases_hoja, fase_c):
    """Cada frase mostrada tiene campo e índice, su original es una frase exacta de ese campo de fase_c.json, la limpieza la
    reproduce y no trae ninguna cifra que no esté en el original. Devuelve la lista de fallos (vacía si todo cuadra)."""
    fallos = []
    for e in frases_hoja:
        campo, idx = e.get("campo"), e.get("indice")
        fuente = obtener_campo(fase_c, campo) if campo else None
        lista = frases(fuente)
        if not isinstance(fuente, str) or not isinstance(idx, int) or not (0 <= idx < len(lista)):
            fallos.append(f"sin origen: {e.get('texto', '')[:80]!r} (campo {campo!r}, frase {idx!r})")
            continue
        if lista[idx] != e.get("original") or e["original"] not in fuente:
            fallos.append(f"el original no es la frase {idx + 1} de {campo}: {e.get('texto', '')[:80]!r}")
        elif limpiar(e["original"]) != e.get("texto"):
            fallos.append(f"el texto no es la limpieza del original ({campo}, frase {idx + 1}): {e.get('texto', '')[:80]!r}")
        else:
            orig = set(_cifras(e["original"]))
            nuevas = [c for c in _cifras(e["texto"]) if c not in orig]
            if nuevas:
                fallos.append(f"cifras que no están en el original ({campo}, frase {idx + 1}): {nuevas}")
    return fallos


def contenido_minimo(por_que, falso, preds, ficha):
    """(hallazgo 5) Sin el contenido mínimo no hay hoja: tesis y tesis inversa con texto, «qué me haría pasar a No» con texto real
    (salvo que el cubo ya sea No) y tres predicciones con fecha y probabilidad. Devuelve la lista de faltas."""
    faltas = []
    for clave, rot in (("tesis", "la tesis (Análisis!B101)"), ("tesis_inversa", "la tesis inversa (Análisis!B102)")):
        if sum(_n_palabras(e["texto"]) for e in por_que.get(clave) or []) < 6:
            faltas.append(f"{rot} está vacía o no dice nada (menos de 6 palabras)")
    if ficha.get("cubo") != "No" and sum(_n_palabras(e["texto"]) for e in falso.get("cambiaria_de_cubo.a_no") or []) < 3:
        faltas.append("«qué me haría pasar a No» (cambiaria_de_cubo.a_no) está vacío o no dice nada")
    buenas = [p for p in preds if _n_palabras(str(p.get("texto") or "")) >= 3 and a_fecha(p.get("fecha")) and es_num(p.get("prob"))]
    if len(buenas) < 3:
        faltas.append(f"hacen falta tres predicciones con texto, fecha y probabilidad (hay {len(buenas)})")
    return faltas


# ------------------------------------------------------------------------------------------------ expediente cerrado y vigente
def libro_evaluado(exp):
    c = sorted(glob.glob(os.path.join(exp, "*_v63_evaluada.xlsx")))
    if len(c) != 1:
        raise ErrorExpediente(f"se esperaba un libro evaluado <E>_v63_evaluada.xlsx y hay {len(c)}")
    return c[0]


def empresa_del_libro(libro):
    return os.path.basename(libro)[:-len("_v63_evaluada.xlsx")]


def vigencia_oficial(exp, empresa, ficha):
    """(hallazgo 2) La MISMA puerta que el cierre oficial: cierre_v2.motivo_vigencia (auditoría APROBADO del material vigente, material
    sin cambios desde la auditoría, aprobación no retirada, F1 vigente y utilizable cuando se exige) y, además, un cierre registrado
    (cierre_vigente.json) con ficha.cierre.auditoria = APROBADO: motivo_vigencia da None también cuando no hay ninguna salida cerrada.
    Devuelve (motivo o None, vigencia F1)."""
    try:
        import cierre_v2 as CIE
        import pipeline as PIPE
        import motor_a_f1 as F1
    except Exception as e:  # noqa: BLE001 — sin la puerta oficial no hay hoja
        return f"no se puede cargar la comprobación oficial de vigencia ({type(e).__name__}: {str(e)[:120]})", {}
    try:
        f1 = F1.vigencia(exp)
    except Exception as e:  # noqa: BLE001
        f1 = {"exigido": True, "vigente": False, "utilizable": False, "motivo": f"la vigencia F1 no se puede comprobar ({type(e).__name__})"}
    try:
        m = CIE.motivo_vigencia(exp, PIPE.Pipeline.veredicto_auditoria, empresa)
    except Exception as e:  # noqa: BLE001 — lado seguro
        m = f"la vigencia oficial no se puede comprobar ({type(e).__name__}: {str(e)[:120]})"
    if m:
        return m, f1
    if not os.path.isfile(os.path.join(exp, CIE.CIERRE_VIGENTE)):
        return (f"no hay cierre registrado ({CIE.CIERRE_VIGENTE}): la ficha no está ligada a ninguna aprobación registrada; "
                "no hay análisis oficial vigente que resumir"), f1
    if (ficha.get("cierre") or {}).get("auditoria") != "APROBADO":
        return "la ficha no registra un cierre con auditoría APROBADO (ficha.cierre.auditoria)", f1
    if f1.get("exigido") and not (f1.get("vigente") and f1.get("utilizable")) and ficha.get("estado_analisis") != "pendiente_de_datos":
        # motivo_f1 ya lo comprueba dentro de motivo_vigencia; se repite aquí por si cambia el orden de las comprobaciones oficiales
        return f"motor A · F1: {f1.get('motivo')}; sin una evaluación F1 vigente y utilizable no hay conclusión del motor A", f1
    return None, f1


def leer_expediente(exp, antecedente=False):
    """Comprueba que el expediente está cerrado, que lo que se lee es el material de ese cierre y que el análisis oficial es vigente.
    Lanza ErrorExpediente si no. Con antecedente=True, un análisis no vigente se acepta pero queda marcado (d['_vigencia'])."""
    falta = [f for f in OBLIGATORIOS if not os.path.isfile(os.path.join(exp, f))]
    if falta:
        raise ErrorExpediente("faltan archivos del cierre (si se retiró la aprobación, la hoja anterior no vale): " + ", ".join(falta))
    libro = libro_evaluado(exp)
    d = {f: cargar_dict(os.path.join(exp, f)) for f in OBLIGATORIOS if f.endswith(".json")}
    for f in OPCIONALES:
        p = os.path.join(exp, f)
        d[f] = cargar_dict(p) if os.path.isfile(p) else None
    ficha, st, precio = d["ficha.json"], d["estado_pipeline.json"], d["precio.json"]
    for nombre, clave, tipo in (("ficha.json", "decision", dict), ("ficha.json", "escalera", dict), ("fase_c.json", "celdas", dict)):
        if d[nombre].get(clave) is not None and not isinstance(d[nombre].get(clave), tipo):
            raise ErrorExpediente(f"{nombre} → {clave} no tiene la forma esperada")
    motivos = []
    if not st.get("fin") or st.get("estado_analisis") in (None, ""):
        motivos.append("el pipeline no ha terminado (estado_pipeline.json sin «fin» o sin estado_analisis)")
    elif st.get("estado_analisis") != ficha.get("estado_analisis"):
        motivos.append(f"estado del pipeline {st.get('estado_analisis')!r} ≠ estado de la ficha {ficha.get('estado_analisis')!r}")
    if (ficha.get("provisional") or {}).get("confirmado") is False:
        motivos.append("ficha.json es provisional (provisional.confirmado = false)")
    huellas = {f: sha256(os.path.join(exp, f)) for f in OBLIGATORIOS}
    huellas[os.path.basename(libro)] = sha256(libro)
    for f in OPCIONALES:
        if d[f] is not None:
            huellas[f] = sha256(os.path.join(exp, f))
    cv = d["cierre_vigente.json"]
    if cv is not None:
        if cv.get("ficha_sha256") != huellas["ficha.json"]:
            motivos.append("ficha.json no es la del cierre vigente (cierre_vigente.json → ficha_sha256)")
        if cv.get("informe_sha256") not in (None, huellas["informe.md"]):
            motivos.append("informe.md no es el del cierre vigente (cierre_vigente.json → informe_sha256)")
    h_libro = (ficha.get("hashes") or {}).get("libro_evaluado")
    if h_libro != huellas[os.path.basename(libro)]:
        motivos.append(f"el libro evaluado no es el de la ficha (ficha.hashes.libro_evaluado {str(h_libro)[:12]}… ≠ {huellas[os.path.basename(libro)][:12]}…)")
    esc = ficha.get("escalera") or {}
    if es_num(esc.get("precio_si")) and esc.get("precio_si") != precio.get("precio_si"):
        motivos.append("la escalera de la ficha no es la de precio.json (precio_si distinto)")
    if motivos:
        raise ErrorExpediente("; ".join(motivos))
    m_vig, f1 = vigencia_oficial(exp, empresa_del_libro(libro), ficha)
    if m_vig and not antecedente:
        raise ErrorExpediente(f"el análisis oficial no está vigente: {m_vig}")
    d["_vigencia"] = {"vigente": m_vig is None, "motivo": m_vig}
    d["_f1"] = f1
    return d, libro, huellas


# ------------------------------------------------------------------------------------------------ sensibilidad a la tasa
def _correr(cmd, timeout=None):
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def sensibilidad(libro, k, tasas, trabajo=None, lock=LOCK_DEFECTO, espera=ESPERA_CERROJO, cerrojo_ya_tomado=False):
    """Para cada tasa: copia del libro evaluado con solo Análisis!C56 = r, recálculo forzado con LibreOffice bajo `flock -w` (salvo
    con cerrojo_ya_tomado), lectura (leer_resultados.py --exigir-recalculo-forzado) y escalera (precio_de_si.calcular con la misma k).
    Las copias se borran."""
    base = tempfile.mkdtemp(prefix="hoja_tasa_", dir=trabajo)
    filas = []
    try:
        perfil = os.path.join(base, "perfil_lo")
        for r in tasas:
            d = os.path.join(base, f"r{round(r * 100000):06d}")
            os.makedirs(os.path.join(d, "in"))
            copia = os.path.join(d, "in", os.path.basename(libro))
            L = LibroV63(libro)
            L.escribir_celdas({f"{CELDA_TASA[0]}!{CELDA_TASA[1]}": r})
            L.guardar(copia)
            cmd = ["bash", os.path.join(AQUI, "recalc.sh"), copia, os.path.join(d, "out"), perfil]
            if not cerrojo_ya_tomado:
                cmd = ["flock", "-w", str(int(espera)), lock] + cmd
            rc, out = _correr(cmd, timeout=int(espera) + 900)
            rec = os.path.join(d, "out", os.path.basename(libro))
            if rc != 0 or not os.path.isfile(rec):
                if not cerrojo_ya_tomado and rc == 1 and not out.strip():
                    raise RuntimeError(f"no se pudo tomar el cerrojo de LibreOffice ({lock}) en {int(espera)} s. Si este programa se lanzó "
                                       "dentro de «flock» del mismo cerrojo, se espera a sí mismo: lanzarlo sin flock (toma el cerrojo en cada "
                                       "recálculo) o con --cerrojo-ya-tomado")
                raise RuntimeError(f"recálculo con r = {r}: {out[-300:]}")
            jres = os.path.join(d, "resultados.json")
            rc, out = _correr([sys.executable, os.path.join(AQUI, "leer_resultados.py"), rec, jres, "--exigir-recalculo-forzado"], timeout=900)
            if rc != 0:
                raise RuntimeError(f"lectura con r = {r} (código {rc}): {out[-300:]}")
            res = cargar(jres)
            c56 = (res.get("valores") or {}).get("C56")
            if not es_num(c56) or abs(c56 - r) > 1e-12:
                raise RuntimeError(f"la copia recalculada no tiene r = {r} en Análisis!C56 (lee {c56!r})")
            esc, _ = PS.calcular(res, k=k)
            filas.append({"r": r, "C56_leida": c56, "precio": esc.get("precio"), "precio_si": esc.get("precio_si"),
                          "ponderado": esc.get("ponderado"), "zona": esc.get("zona"), "V": esc.get("V"),
                          "precio_escenario_malo": esc.get("precio_escenario_malo"), "g_impl_actual": esc.get("g_impl_actual"),
                          "C86_hoja": (res.get("valores") or {}).get("C86"), "sin_lectura": esc.get("sin_lectura"),
                          "sin_escalera": esc.get("sin_escalera"), "notas": esc.get("notas"),
                          "r_operativa_C15": res.get("r_operativa_C15"), "r_minima_C17": res.get("r_minima_C17"),
                          "r_vs_minima_C18": res.get("r_vs_minima_C18"),
                          "estado_tecnico": (res.get("estados") or {}).get("estado_tecnico_B255")})
    finally:
        shutil.rmtree(base, ignore_errors=True)
    return filas


def comprobar_recalculo(filas):
    """(hallazgo 10) Defensa ante un recálculo que no recalcula: con dos o más tasas, el precio de Sí y el valor medio tienen que bajar
    al subir la tasa y, si la hoja da la tasa con que descuenta (C15), tiene que cambiar con la tasa. Devuelve el motivo o None."""
    buenas = sorted((f for f in filas if es_num(f.get("precio_si")) and es_num(f.get("ponderado"))), key=lambda f: f["r"])
    for a, b in zip(buenas, buenas[1:]):
        if not (a["precio_si"] > b["precio_si"] and a["ponderado"] > b["ponderado"]):
            return (f"el precio de Sí o el valor medio no bajan al subir la tasa ({tasa_txt(a['r'])}: {a['precio_si']!r}, {a['ponderado']!r}; "
                    f"{tasa_txt(b['r'])}: {b['precio_si']!r}, {b['ponderado']!r}): el libro no parece recalculado")
    c15 = [f.get("r_operativa_C15") for f in buenas if es_num(f.get("r_operativa_C15"))]
    if len(c15) == len(buenas) and len(c15) > 1 and len(set(c15)) != len(c15):
        return "la tasa con que descuenta la hoja (Análisis!C15) no cambia con la tasa: el libro no parece recalculado"
    return None


def reproduce_oficial(fila, precio):
    claves = ("precio_si", "ponderado", "zona", "V", "precio", "g_impl_actual")
    dif = {c: (fila.get(c), precio.get(c)) for c in claves if fila.get(c) != precio.get(c)}
    return not dif, dif


def estabilidad(filas, tasa):
    """(hallazgo 12) ¿Dónde queda el precio del análisis con la tasa del análisis y un punto por encima y por debajo? Solo habla de la
    tasa: no dice que el análisis sea seguro (antes se llamaba «firme»)."""
    z = {round(f["r"], 6): f.get("zona") for f in filas}
    tramo_r = [round(tasa - 0.01, 6), round(tasa, 6), round(tasa + 0.01, 6)]
    tramo = [z.get(r) for r in tramo_r]
    rot = ", ".join(tasa_txt(r) for r in tramo_r[:2]) + " y " + tasa_txt(tramo_r[2])
    if None in tramo:
        return None, f"no se puede decir: falta alguna de las tasas {rot}"
    if len(set(tramo)) == 1:
        return True, (f"**Frente a la tasa, el resultado no cambia:** con el {rot} el precio del análisis queda en el mismo sitio "
                      f"({ZONA_LLANA.get(tramo[0], tramo[0])}). Esto solo habla de la tasa; no dice que el análisis sea seguro.")
    return False, (f"**Frente a la tasa, el resultado cambia:** con el {rot} el precio del análisis queda en sitios distintos ("
                   + "; ".join(f"{tasa_txt(r)}: {ZONA_LLANA.get(x, x)}" for r, x in zip(tramo_r, tramo))
                   + "). Esto solo habla de la tasa; no dice que el análisis sea seguro.")


# ------------------------------------------------------------------------------------------------ veredicto y aptitud (de la ficha)
def veredicto(ficha, precio, f1):
    """(hallazgo 1) El veredicto sale SOLO de la ficha. Devuelve un dict con: concluye (bool), conclusion (texto fijo por estado),
    causa, que_lo_resolveria, precio_compra (o None), lineas de precio y salvedades (campos de la ficha copiados)."""
    estado = ficha.get("estado_analisis")
    dec = ficha.get("decision") if isinstance(ficha.get("decision"), dict) else {}
    obj = ficha.get("objetivo") if isinstance(ficha.get("objetivo"), dict) else {}
    f1b = ficha.get("motor_a_f1") if isinstance(ficha.get("motor_a_f1"), dict) else None
    f1_inutil = (f1b is not None and f1b.get("utilizable_para_conclusion") is False) or (
        bool(f1.get("exigido")) and not (f1.get("vigente") and f1.get("utilizable")))
    accion, cubo = dec.get("accion"), ficha.get("cubo")
    concluye = estado == "concluido" and not f1_inutil
    if concluye:
        if cubo == "Demasiado difícil":
            texto = "No sabe valorarla y la deja."
        else:
            texto = CONCLUSION_LLANA.get(accion) or f"{accion or 'sin acción'}."
        texto += f" (Categoría del personaje: «{cubo or '—'}».)"
    elif estado == "concluido":
        texto = "**Sin conclusión:** el motor de cálculo A no se puede usar para concluir (F1)."
    elif estado == "pendiente_de_datos":
        texto = "**Sin conclusión: falta un dato.**"
    elif estado == "pendiente_de_investigacion":
        texto = "**Sin conclusión de compra:** una hipótesis no se puede acotar con lo que hay."
    else:
        texto = f"**Sin conclusión** (estado «{ESTADO_LLANO.get(estado, str(estado).replace('_', ' '))}»)."
    if not concluye and cubo:
        texto += f" Mientras tanto la deja en la categoría «{cubo}»."
    causa = ficha.get("causa_si_no_concluido") if isinstance(ficha.get("causa_si_no_concluido"), dict) else {}
    po = dec.get("precio_objetivo") if es_num(dec.get("precio_objetivo")) else None
    if obj:
        if obj.get("estado_del_objetivo") == "bloqueado" or obj.get("precio_objetivo_emitido") is None:
            po = None
        elif es_num(obj.get("precio_objetivo_emitido")):
            po = obj.get("precio_objetivo_emitido")
    if not concluye:
        po = None
    psi = precio.get("precio_si")
    mon = ficha.get("moneda")
    if po is not None:
        linea_precio = f"a {dinero(po, mon)} por acción o menos."
        if obj.get("provisional") or obj.get("estado_del_objetivo") == "emitido_condicionado":
            linea_precio += " **Es un precio provisional: el objetivo está condicionado** (ver «Salvedades de la ficha»)."
    else:
        linea_precio = "**la ficha no da precio de compra.**"
        if es_num(psi):
            if obj.get("estado_del_objetivo") == "bloqueado":
                por = "la ficha dice que el objetivo está bloqueado"
            elif not concluye and re.search(r"no es (?:una conclusión )?utilizable", " ".join(
                    str(x) for x in (causa.get("detalle"), (ficha.get("insumos_decision_cartera") or {}).get("fundamento")
                                     if isinstance(ficha.get("insumos_decision_cartera"), dict) else None) if x)):
                por = "la ficha dice que esa cifra no es utilizable para una conclusión"
            elif not concluye:
                por = "sin conclusión, esa cifra no es un precio de compra"
            else:
                por = "la ficha no la emite como objetivo"
            linea_precio += f" La hoja de cálculo arroja un precio de Sí de {dinero(psi, mon)}, pero {por}."
    salv = []
    if dec.get("condicion"):
        salv.append(("Condición", limpiar(str(dec["condicion"]))))
    if obj:
        e_obj = obj.get("estado_del_objetivo")
        txt = OBJETIVO_LLANO.get(e_obj, str(e_obj or "—").replace("_", " "))
        if obj.get("provisional") and "provisional" not in txt:
            txt += " (provisional)"
        hip = [str(h.get("hipotesis")) for h in obj.get("hipotesis_que_lo_condicionan") or [] if isinstance(h, dict) and h.get("hipotesis")]
        if hip:
            txt += "; lo condicionan " + ", ".join(hip)
        salv.append(("Objetivo de precio", txt))
    fund = (ficha.get("insumos_decision_cartera") or {}).get("fundamento") if isinstance(ficha.get("insumos_decision_cartera"), dict) else None
    if fund:
        salv.append(("Fundamento", limpiar(str(fund))))
    m1 = ficha.get("datos_etapa1_incompletos") if isinstance(ficha.get("datos_etapa1_incompletos"), dict) else {}
    if m1.get("marca"):
        salv.append(("Datos", f"{m1.get('marca')} ({len(m1.get('causas') or [])} causas; detalle en la ficha)"))
    alc = ficha.get("alcance") if isinstance(ficha.get("alcance"), dict) else {}
    if alc.get("aviso"):
        salv.append(("Alcance", str(alc["aviso"])))
    return {"concluye": concluye, "conclusion": texto, "estado": estado, "cubo": cubo, "accion": accion,
            "causa": limpiar(str(causa.get("detalle"))) if causa.get("detalle") else None,
            "que_lo_resolveria": limpiar(str(ficha.get("que_lo_resolveria"))) if ficha.get("que_lo_resolveria") and not concluye else None,
            "precio_compra": po, "linea_precio": linea_precio, "objetivo": obj or None, "salvedades": salv, "f1_inutil": f1_inutil}


def aptitud(ficha, f1):
    """(hallazgo 3) La aptitud se compone de los tres bloques de la ficha (aptitud_de_uso, verificacion_entradas, motor_a_f1) y de la
    vigencia F1 actual. Texto fijo: «Experimental: no vale para decidir con dinero real.» La hoja NUNCA dice «apto para dinero real»:
    no se acredita superando controles de software. Devuelve (lineas, datos)."""
    L = ["**¿Sirve para decidir con dinero real?** No. **Experimental: no vale para decidir con dinero real.**"]
    apt = ficha.get("aptitud_de_uso") if isinstance(ficha.get("aptitud_de_uso"), dict) else None
    vef = ficha.get("verificacion_entradas") if isinstance(ficha.get("verificacion_entradas"), dict) else None
    f1b = ficha.get("motor_a_f1") if isinstance(ficha.get("motor_a_f1"), dict) else None
    ve = vef if vef is not None else ((apt or {}).get("verificacion_entradas") if isinstance((apt or {}).get("verificacion_entradas"), dict) else None)
    datos = {"aptitud_de_uso": bool(apt), "verificacion_entradas": bool(ve), "motor_a_f1": bool(f1b), "apto_por_entradas": None}
    if ve is not None:
        rs = ve.get("resumen") if isinstance(ve.get("resumen"), dict) else ve
        apto_e = bool(ve.get("apto_por_entradas"))
        datos["apto_por_entradas"] = apto_e
        n_u, u = rs.get("comprobadas_universo"), rs.get("universo")
        cuenta = f"{n_u} de {u} datos comprobados" if n_u is not None and u is not None else None
        motivo = rs.get("motivo") if not apto_e else None
        L.append(f"- Datos de entrada verificados contra sus fuentes: **{'sí' if apto_e else 'no'}**"
                 + (f" ({cuenta})" if cuenta else "") + (f"; {recortar(motivo, 200)}" if motivo else "")
                 + (f"; {recortar(ve.get('motivo_modo'), 160)}" if ve.get("motivo_modo") else "") + ".")
    if f1b is not None:
        L.append(f"- Motor A · F1: {f1b.get('rotulo') or ('utilizable para una conclusión (condición necesaria, no suficiente)' if f1b.get('utilizable_para_conclusion') else 'el resultado del motor A no se usa para una conclusión')}"
                 + (f"; bloquean: {', '.join(sorted({str(g.get('id')) for g in f1b.get('bloquean') or [] if isinstance(g, dict)}))}" if f1b.get("bloquean") else "") + ".")
    if f1.get("exigido") and not (f1.get("vigente") and f1.get("utilizable")):
        L.append(f"- Motor A · F1 hoy: no vigente o no utilizable ({f1.get('motivo')}).")
    if apt is not None:
        L.append(f"- Evaluación de la entrega {apt.get('version') or '—'}: {apt.get('caracter') or 'experimental'}.")
    if ve is None and f1b is None and apt is None:
        L.append("- La ficha no dice nada sobre la aptitud; no se presume ninguna.")
    marcas = [b for b in (apt, ve, f1b) if isinstance(b, dict) and b.get("apto_para_dinero_real") is True]
    if marcas:
        L.append("- La ficha contiene una marca de aptitud para dinero real; esta hoja no la repite: la aptitud no se acredita superando "
                 "controles de software (haría falta una decisión humana registrada fuera de esta hoja).")
    return L, datos


def fechas(d, ficha):
    """Fechas por separado, de fase1_metadatos.json o, si no está (expedientes anteriores), de fase1_v63.json; «no consta» si no hay."""
    f1 = d.get("fase1_v63.json") or {}
    meta = d.get("fase1_metadatos.json") or f1
    origen = "fase1_metadatos.json" if d.get("fase1_metadatos.json") else ("fase1_v63.json" if f1 else None)
    fu = d.get("fase1_fuentes.json") or {}
    anios = sorted(str(k) for k in fu if re.fullmatch(r"\d{4}", str(k))) if isinstance(fu, dict) else []
    plantilla_fu = "documentos de los ejercicios {a} a {b} ({n} ejercicios)"
    if not anios:
        anios = sorted(str(a) for a in ((f1.get("historia") or {}).get("anios") or []) if re.fullmatch(r"\d{4}", str(a)))
        plantilla_fu = "años de la Historia de {a} a {b} ({n})"
    base = (f"ejercicio {anios[-1]}" + (f" (cierre fiscal: {meta['cierre_fiscal']})" if meta.get("cierre_fiscal") else "")) if anios else "no consta"
    fuentes = plantilla_fu.format(a=anios[0], b=anios[-1], n=len(anios)) if anios else "no consta"
    return [
        ("Análisis", fecha_larga(ficha.get("fecha"))),
        ("Datos base (último ejercicio de la Historia)", base),
        ("Precio usado en el análisis", fecha_larga(fecha_precio(d, ficha))),
        ("Acciones", fecha_larga((meta.get("acciones_diluidas") or {}).get("fecha"))),
        ("Fuentes", fuentes),
    ], origen


def fecha_precio(d, ficha):
    meta = d.get("fase1_metadatos.json") or d.get("fase1_v63.json") or {}
    f = (meta.get("precio") or {}).get("fecha") if isinstance(meta.get("precio"), dict) else None
    return f or ((ficha.get("insumos_decision_cartera") or {}).get("fecha_precio") if isinstance(ficha.get("insumos_decision_cartera"), dict) else None)


def predicciones(fase_c, ficha):
    ce = fase_c.get("celdas") or {}
    out, avisos = [], []
    fps = ficha.get("predicciones") if isinstance(ficha.get("predicciones"), list) else []
    for i, fila in enumerate((38, 39, 40)):
        p = {"texto": ce.get(f"Palancas!A{fila}"), "fecha": fecha_iso(ce.get(f"Palancas!B{fila}")), "prob": ce.get(f"Palancas!C{fila}"),
             "celdas": f"Palancas!A{fila}:C{fila}"}
        out.append(p)
        fp = fps[i] if i < len(fps) and isinstance(fps[i], dict) else None
        if not fp or fp.get("texto") != p["texto"] or fp.get("fecha") != p["fecha"] or fp.get("prob") != p["prob"]:
            avisos.append(f"la predicción {i + 1} de fase_c.json (Palancas A{fila}:C{fila}) no coincide con la de la ficha")
    return out, avisos


def glosario(texto):
    """(hallazgo 6) Glosario fijo: solo los términos que aparecen en la página."""
    return [(t, dfn) for t, patron, dfn in GLOSARIO if re.search(patron, texto, re.I if patron.islower() else 0)]


# ------------------------------------------------------------------------------------------------ composición
def componer(exp, d, libro, huellas, filas, tasa_heredada, reproduce, dif, hoy=None):
    ficha, fase_c, precio = d["ficha.json"], d["fase_c.json"], d["precio.json"]
    vig = d.get("_vigencia") or {"vigente": True, "motivo": None}
    f1 = d.get("_f1") or {}
    mon = ficha.get("moneda")
    hoy = hoy or dt.date.today()
    v = veredicto(ficha, precio, f1)
    apt_lineas, apt_datos = aptitud(ficha, f1)
    por_que = seleccionar_por_que(fase_c)
    falso = {c: texto_con_origen(fase_c, c) for c, _ in ROTULO_FALSO}
    preds, avisos = predicciones(fase_c, ficha)
    tesis_libro = d["resultados.json"].get("celdas_juicio_analisis") or {}
    for c in ("B101", "B102"):
        if tesis_libro.get(c) not in (None, obtener_campo(fase_c, c)):
            avisos.append(f"Análisis!{c} del libro evaluado no es el texto de fase_c.json")
    estable, estable_txt = estabilidad(filas, tasa_heredada) if filas else (None, "sin tabla de la tasa")
    f_precio = fecha_precio(d, ficha)
    fp, fa = a_fecha(f_precio), a_fecha(ficha.get("fecha"))
    dias_precio = (fa - fp).days if fp and fa else None
    zona = precio.get("zona")
    L = []
    L.append(f"# {ficha.get('empresa')} · resumen para estudiar")
    L.append("")
    if not vig["vigente"]:
        L.append(f"> **NO VIGENTE · ANTECEDENTE.** El sistema oficial no da por vigente este análisis: {vig['motivo']} Esta hoja solo sirve "
                 "para estudiar el antecedente; no describe ninguna conclusión vigente.")
        L.append("")
    L.append("> **Resumen para estudiar. No es una recomendación de compra ni un documento oficial.** Lo escribe un programa a partir del "
             "análisis de un analista simulado (el «personaje»). **Experimental: no vale para decidir con dinero real.** "
             f"Hecho el {fecha_larga(hoy.isoformat())}. Deja de valer si el análisis oficial cambia (ver «Para comprobar esta hoja», al final).")
    L.append("")
    L.append("## Qué concluye el análisis")
    L.append("")
    L.append(f"- **Qué concluye:** {v['conclusion']}")
    if v["causa"]:
        L.append(f"- **Motivo, según la ficha:** {recortar(v['causa'], 420)}")
    if v["que_lo_resolveria"]:
        L.append(f"- **Qué lo resolvería, según la ficha:** {recortar(v['que_lo_resolveria'], 260)}")
    L.append(f"- **A qué precio compraría:** {v['linea_precio']}")
    linea = f"- **Precio usado en el análisis:** {dinero(precio.get('precio'), mon)} ({fecha_larga(f_precio)})"
    if zona:
        linea += f": {ZONA_LLANA.get(zona, zona)}" + ("" if v["concluye"] else " (comparación con la hoja de cálculo; no es una conclusión)")
    linea += "."
    if dias_precio is not None and dias_precio > DIAS_PRECIO_ANTIGUO:
        linea += f" **Ojo:** es un precio de {dias_precio} días antes del análisis, no el de hoy."
    else:
        linea += " No es el precio de hoy."
    L.append(linea)
    L.append("")
    L.extend(apt_lineas)
    if v["salvedades"]:
        L.append("")
        L.append("**Salvedades de la ficha** (copiadas de la ficha oficial, recortadas):")
        L.append("")
        for rot, txt in v["salvedades"]:
            L.append(f"- {rot}: {recortar(txt, 220 if rot == 'Alcance' else 360)}")
    L.append("")
    L.append("## Por qué (con palabras del personaje)")
    L.append("")
    L.append(" ".join(e["texto"] for e in por_que["tesis"]))
    L.append("")
    L.append("**Lo que le preocupa** (su argumento en contra, entero):")
    L.append("")
    for e in por_que["tesis_inversa"]:
        L.append(f"- {e['texto']}")
    L.append("")
    L.append("## Lo que le haría cambiar de opinión")
    L.append("")
    for campo, rot in ROTULO_FALSO:
        if falso[campo]:
            L.append(f"- **{rot}** " + " ".join(e["texto"] for e in falso[campo]))
    L.append("")
    L.append("## Cuánto cambia el resultado si se le pide más o menos rentabilidad")
    L.append("")
    if not v["concluye"]:
        L.append("**Esto es una lectura de la hoja de cálculo, no una conclusión:** " + (
            "la ficha no da precio de compra." if v["precio_compra"] is None else "el análisis no concluye."))
        L.append("")
    L.append(f"La **tasa** es la rentabilidad anual mínima que el análisis le pide a la inversión. Cuanto más alta, menos vale la empresa "
             f"en el cálculo. El análisis usó el **{tasa_txt(tasa_heredada)}**: es una cifra heredada de la primera etapa y **todavía no "
             f"está decidida**. Por eso se repite el cálculo con otras tasas, cambiando solo esa cifra. Todo lo demás se deja igual, también "
             f"las hipótesis que el personaje fijó pensando en el {tasa_txt(tasa_heredada)} (por ejemplo, lo que rinde el capital a largo "
             "plazo): la tabla dice cuánto pesa la tasa con el mismo juicio, no qué habría decidido el personaje con otra tasa.")
    L.append("")
    hay_c15 = any(es_num(f.get("r_operativa_C15")) and abs(f["r_operativa_C15"] - f["r"]) > 1e-9 for f in filas)
    col_psi = "Precio de Sí (compraría a este precio o menos)" if v["concluye"] else "Precio de Sí de la hoja de cálculo (no es un precio de compra)"
    L.append(f"| Si se le pide un… | {col_psi} | Valor medio de sus tres escenarios | El precio del análisis ({dinero(precio.get('precio'), mon)}) queda… | Crecimiento anual de ventas que ese precio da por hecho (años 1–5) | Aviso de la hoja de cálculo |")
    L.append("|---|---|---|---|---|---|")
    hay_no_calc = False
    for f in filas:
        rot = tasa_txt(f["r"]) + (" (la del análisis)" if abs(f["r"] - tasa_heredada) < 1e-12 else "")
        if f.get("sin_lectura") or f.get("sin_escalera"):
            L.append(f"| {rot} | sin lectura: {f.get('sin_lectura') or f.get('sin_escalera')} | — | — | — | — |")
            continue
        g = f.get("g_impl_actual")
        if not es_num(g):
            hay_no_calc = True
        av = []
        if isinstance(f.get("r_vs_minima_C18"), str) and "REVISAR" in f["r_vs_minima_C18"]:
            av.append(f"la tasa queda por debajo de la mínima de la hoja ({tasa_txt(round(f['r_minima_C17'], 3)) if es_num(f.get('r_minima_C17')) else '—'})")
        if hay_c15 and es_num(f.get("r_operativa_C15")):
            av.append(f"descuenta al {pct(f['r_operativa_C15'])}")
        L.append(f"| {rot} | {dinero(f.get('precio_si'), mon)} | {dinero(f.get('ponderado'), mon)} | {ZONA_LLANA.get(f.get('zona'), f.get('zona'))} | "
                 f"{pct(g) if es_num(g) else 'no se puede calcular'} | {'; '.join(av) or '—'} |")
    L.append("")
    L.append(f"- **El {tasa_txt(tasa_heredada)} es provisional.**")
    if any(abs(f["r"] - 0.10) < 1e-12 for f in filas):
        L.append("- **La fila del 10 % es solo una prueba** para ver cuánto cambia el resultado. No es un requisito.")
    L.append(f"- {estable_txt}")
    fila_her = next((f for f in filas if abs(f["r"] - tasa_heredada) < 1e-12), {})
    a2 = next((a for a in ficha.get("avisos") or [] if isinstance(a, dict) and a.get("id") == "A2"), None)
    if a2 or (isinstance(fila_her.get("r_vs_minima_C18"), str) and "REVISAR" in fila_her["r_vs_minima_C18"]):
        m_min = fila_her.get("r_minima_C17")
        L.append(f"- **La hoja de cálculo avisa de que el {tasa_txt(tasa_heredada)} queda por debajo de su tasa mínima de referencia"
                 + (f" ({tasa_txt(round(m_min, 3))})" if es_num(m_min) else "") + ".**" + (" Aviso de la ficha: " + str(a2.get("detalle")) + "." if a2 else ""))
    if hay_c15:
        L.append("- En este cálculo la tasa con que se descuenta no es exactamente la de la primera columna: la hoja de cálculo la ajusta "
                 "(última columna).")
    if hay_no_calc:
        L.append("- «No se puede calcular»: la hoja de cálculo no da ese crecimiento para este caso (lo marca «no utilizable»).")
    L.append("- Dónde queda el precio frente a esos valores **no es la conclusión**: no mide el riesgo ni el fundamento.")
    L.append("- El escenario malo **no es un suelo** de valor ni la pérdida máxima posible.")
    L.append(f"- El precio de Sí sale de una **regla experimental** (k = {num_es(precio.get('k'), 0) if es_num(precio.get('k')) else '—'}): la "
             "ganancia esperada debe ser al menos el triple de la pérdida esperada.")
    L.append("")
    L.append("## Predicciones fechadas")
    L.append("")
    L.append("Se comprueban en esta fecha con este dato:")
    L.append("")
    for n, p in enumerate(preds, 1):
        L.append(f"{n}. **{fecha_larga(p['fecha'])}** — {p['texto']} Probabilidad que le da el personaje: {pct(p['prob'], 0)}.")
    L.append("")
    L.append("## Fechas")
    L.append("")
    lf, origen_f = fechas(d, ficha)
    for rot, val in lf:
        L.append(f"- {rot}: {val}.")
    L.append(f"- Hoja hecha el: {fecha_larga(hoy.isoformat())}.")
    cuerpo = "\n".join(L)
    gl = glosario(cuerpo)
    if gl:
        L.append("")
        L.append("## Palabras que pueden no ser conocidas")
        L.append("")
        for t, dfn in gl:
            L.append(f"- **{t}:** {dfn}")
    L.append("")
    L.append("## Para comprobar esta hoja")
    L.append("")
    L.append(f"- Vale solo mientras la ficha `{huellas['ficha.json'][:16]}…` siga siendo la oficial y vigente. Compruébalo con "
             f"`hoja_resumen.py {os.path.basename(exp)} --comprobar`.")
    L.append("- Las frases del personaje son las de la tesis (Análisis!B101), la tesis inversa (Análisis!B102), `cambiaria_de_cubo` y "
             "`decision.condiciones_revision` de fase_c.json, enteras; solo se quitan las referencias a celdas y páginas, que están en el "
             "informe (§8 y §10). El origen de cada frase está en hoja_resumen.json (`--verificar-origen`).")
    L.append(f"- Cálculo de la tabla: copias del libro evaluado cambiando solo Análisis!C56, recalculadas con LibreOffice. A la tasa del "
             f"análisis ({tasa_txt(tasa_heredada)}), el cálculo repetido da exactamente el precio de Sí de precio.json: "
             f"**{'sí' if reproduce else 'NO — ' + json.dumps(dif, ensure_ascii=False)}**.")
    ver = ficha.get("versiones") or {}
    L.append(f"- Versión del personaje: {ver.get('personaje')} · plantilla {ver.get('plantilla')} · configuración {ver.get('config')} · "
             f"hoja resumen {VERSION_HOJA}" + (f" · fechas de {origen_f}" if origen_f else "") + ".")
    if avisos:
        L.append(f"- **Avisos:** " + " · ".join(avisos) + ".")
    L.append("")
    md = "\n".join(L)
    traza = {
        "version_hoja": VERSION_HOJA, "generada": dt.datetime.now().isoformat(timespec="seconds"),
        "expediente": os.path.abspath(exp), "entradas_sha256": huellas,
        "vigencia": vig,
        "veredicto": {"estado_analisis": ficha.get("estado_analisis"), "concluye": v["concluye"], "cubo": ficha.get("cubo"),
                      "accion": v["accion"], "precio_compra": v["precio_compra"], "causa": v["causa"], "objetivo": v["objetivo"],
                      "precio_si_hoja_de_calculo": precio.get("precio_si"), "precio": precio.get("precio"), "fecha_precio": f_precio,
                      "dias_precio_antes_del_analisis": dias_precio, "zona": zona, "ponderado": precio.get("ponderado"),
                      "aptitud": apt_datos, "f1_inutil": v["f1_inutil"]},
        "por_que": por_que, "lo_que_lo_haria_falso": falso, "predicciones": preds,
        "sensibilidad": {"celda_tasa": "!".join(CELDA_TASA), "tasa_heredada": tasa_heredada, "k": precio.get("k"), "filas": filas,
                         "reproduce_oficial": reproduce, "diferencias": dif, "estable_frente_a_la_tasa": estable, "estable_texto": estable_txt},
        "fechas": lf, "versiones": ver, "avisos": avisos,
        "md_sha256": sha256_texto(md if md.endswith("\n") else md + "\n"),
    }
    return md, traza


def frases_de_la_traza(t):
    pq = t.get("por_que") or {}
    return ([e for k in ("tesis", "tesis_inversa") for e in pq.get(k) or []]
            + [e for v in (t.get("lo_que_lo_haria_falso") or {}).values() for e in v])


# ------------------------------------------------------------------------------------------------ órdenes
def apartar_hoja(salida, motivo):
    """(hallazgo 4) Con un código de error no queda ninguna hoja que --comprobar pueda dar por vigente: la anterior se aparta como
    hoja_resumen.NO_VIGENTE.md / .json (sustituye a una apartada antes). Devuelve los nombres apartados."""
    apartados = []
    for n in (SALIDA_MD, SALIDA_JSON):
        p = os.path.join(salida, n)
        if os.path.isfile(p):
            raiz, ext = os.path.splitext(n)
            os.replace(p, os.path.join(salida, raiz + SUFIJO_NO_VIGENTE + ext))
            apartados.append(raiz + SUFIJO_NO_VIGENTE + ext)
    if apartados:
        print(f"HOJA ANTERIOR APARTADA COMO NO VIGENTE ({', '.join(apartados)}): {motivo[:200]}")
    return apartados


def comprobar(exp, salida):
    """(hallazgos 2, 4 y 9) Repite la puerta completa (vigencia oficial incluida), las huellas de lo leído y la de la propia página."""
    pj, pm = os.path.join(salida, SALIDA_JSON), os.path.join(salida, SALIDA_MD)
    if not os.path.isfile(pj) or not os.path.isfile(pm):
        print(f"SIN HOJA: no hay {SALIDA_MD} y {SALIDA_JSON} en {salida}")
        return 4
    try:
        t = cargar_dict(pj)
    except ErrorExpediente as e:
        print(f"HOJA ILEGIBLE: {e}. Retirar la hoja.")
        return 4
    if t.get("md_sha256") != sha256(pm):
        print(f"HOJA EDITADA: {SALIDA_MD} no es la página que se generó (su huella no es la de {SALIDA_JSON}). Retirar la hoja y regenerarla.")
        return 4
    if not (t.get("vigencia") or {}).get("vigente"):
        print(f"HOJA NO VIGENTE (antecedente): {(t.get('vigencia') or {}).get('motivo')}")
        return 4
    if (t.get("sensibilidad") or {}).get("reproduce_oficial") is not True:
        print("HOJA NO VÁLIDA: a la tasa del análisis no reproducía el precio de Sí de precio.json. Retirar la hoja.")
        return 4
    try:
        _, _, huellas = leer_expediente(exp)
    except ErrorExpediente as e:
        print(f"HOJA NO VIGENTE: {e}. Retirar la hoja: ya no resume un análisis oficial vigente.")
        return 4
    ent = t.get("entradas_sha256") or {}
    cambios = []
    for f, h in ent.items():
        actual = huellas.get(f) or (sha256(os.path.join(exp, f)) if os.path.isfile(os.path.join(exp, f)) else None)
        if actual is None:
            cambios.append(f"{f} ya no está")
        elif actual != h:
            cambios.append(f"{f} cambió")
    cambios += [f"{f} apareció" for f in huellas if f not in ent]
    if cambios:
        print("HOJA DESACTUALIZADA: " + "; ".join(cambios) + f". Retirarla y, si el análisis oficial es vigente, regenerarla: hoja_resumen.py {exp}")
        return 4
    print(f"HOJA VIGENTE: lee la ficha {t['entradas_sha256']['ficha.json'][:16]}…, el análisis oficial es vigente y la página no se ha editado")
    return 0


def verificar_origen(exp, salida):
    try:
        t = cargar_dict(os.path.join(salida, SALIDA_JSON))
        fase_c = cargar_dict(os.path.join(exp, "fase_c.json"))
        md = open(os.path.join(salida, SALIDA_MD), encoding="utf-8").read()
    except (ErrorExpediente, OSError) as e:
        print(f"FRASES SIN ORIGEN: no se puede leer la hoja o fase_c.json ({e})")
        return 4
    todas = frases_de_la_traza(t)
    fallos = verificar_origen_frases(todas, fase_c)
    if t.get("md_sha256") != sha256_texto(md):
        fallos.append(f"{SALIDA_MD} se editó después de generarla (su huella no es la de {SALIDA_JSON})")
    for e in todas:
        if e.get("texto") and e["texto"] not in md:
            fallos.append(f"frase que no está en {SALIDA_MD}: {e['texto'][:60]!r}")
    if not todas:
        fallos.append("la hoja no registra ninguna frase del personaje")
    print(("ORIGEN COMPROBADO: " if not fallos else "FRASES SIN ORIGEN: ") + (f"{len(todas)} frases" if not fallos else " | ".join(fallos)))
    return 0 if not fallos else 4


def generar(exp, salida, trabajo, lock, tasas, antecedente=False, espera=ESPERA_CERROJO, cerrojo_ya_tomado=False):
    def falla(codigo, mensaje):
        print(mensaje)
        apartar_hoja(salida, mensaje)
        return codigo

    try:
        d, libro, huellas = leer_expediente(exp, antecedente=antecedente)
    except ErrorExpediente as e:
        return falla(3, f"EXPEDIENTE NO CERRADO, NO VIGENTE O INCOMPLETO: {e}")
    precio = d["precio.json"]
    previa = os.path.join(salida, SALIDA_JSON)
    if os.path.isfile(previa):
        try:
            ant = (cargar(previa).get("entradas_sha256") or {}).get("ficha.json")
        except (OSError, ValueError, AttributeError):
            ant = None
        if ant and ant != huellas["ficha.json"]:
            print(f"AVISO: la ficha cambió desde la hoja anterior ({ant[:16]}… → {huellas['ficha.json'][:16]}…): se regenera")
    try:
        r_her = LibroV63(libro).leer(*CELDA_TASA)
    except Exception as e:  # noqa: BLE001
        return falla(3, f"EXPEDIENTE NO CERRADO, NO VIGENTE O INCOMPLETO: el libro evaluado no se puede leer ({type(e).__name__})")
    if not es_num(r_her):
        return falla(3, f"EXPEDIENTE NO CERRADO, NO VIGENTE O INCOMPLETO: Análisis!C56 del libro evaluado no es un número ({r_her!r})")
    lista = sorted({round(x, 10) for x in list(tasas) + [r_her, r_her - 0.01, r_her + 0.01]})
    r_her = round(r_her, 10)
    filas, reproduce, dif = [], False, {"motivo": "sin escalera en precio.json"}
    if "precio_si" in precio:
        try:
            filas = sensibilidad(libro, precio.get("k", PS.K_DEFECTO), lista, trabajo=trabajo, lock=lock, espera=espera,
                                 cerrojo_ya_tomado=cerrojo_ya_tomado)
        except (RuntimeError, subprocess.TimeoutExpired, OSError, ValueError) as e:
            return falla(6, f"FALLO DEL RECÁLCULO: {e}")
        m_rec = comprobar_recalculo(filas)
        if m_rec:
            return falla(6, f"FALLO DEL RECÁLCULO: {m_rec}")
        fh = next(f for f in filas if abs(f["r"] - r_her) < 1e-12)
        reproduce, dif = reproduce_oficial(fh, precio)
    md, traza = componer(exp, d, libro, huellas, filas, r_her, reproduce, dif)
    fallos = verificar_origen_frases(frases_de_la_traza(traza), d["fase_c.json"])
    if fallos:
        return falla(4, "FRASES SIN ORIGEN (no se escribe hoja): " + " | ".join(fallos))
    faltas = contenido_minimo(traza["por_que"], traza["lo_que_lo_haria_falso"], traza["predicciones"], d["ficha.json"])
    if faltas:
        return falla(4, "CONTENIDO MÍNIMO INCUMPLIDO (no se escribe hoja): " + "; ".join(faltas))
    if not reproduce:
        return falla(5, "LA SENSIBILIDAD NO REPRODUCE EL PRECIO DE SÍ DE precio.json (no se escribe hoja): " + json.dumps(dif, ensure_ascii=False))
    os.makedirs(salida, exist_ok=True)
    md = md if md.endswith("\n") else md + "\n"
    for nombre, contenido in ((SALIDA_MD, md), (SALIDA_JSON, json.dumps(traza, ensure_ascii=False, indent=1) + "\n")):
        tmp = os.path.join(salida, f".{nombre}.tmp")
        with open(tmp, "w", encoding="utf-8") as f:
            f.write(contenido)
        os.replace(tmp, os.path.join(salida, nombre))
    print(f"OK: {os.path.join(salida, SALIDA_MD)} · {'VIGENTE' if traza['vigencia']['vigente'] else 'NO VIGENTE (antecedente)'} · "
          f"{'concluye' if traza['veredicto']['concluye'] else 'sin conclusión'} · {len(frases_de_la_traza(traza))} frases con origen · tasas "
          + ", ".join(tasa_txt(f['r']) for f in filas) + f" · reproduce precio.json a {tasa_txt(r_her)}: {'sí' if reproduce else 'NO'}")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("expediente")
    ap.add_argument("--salida", help="carpeta donde escribir la hoja (por defecto, el expediente)")
    ap.add_argument("--trabajo", help="carpeta para las copias temporales (se borran)")
    ap.add_argument("--lock", default=LOCK_DEFECTO, help="cerrojo de LibreOffice para flock (no lanzar este programa dentro de flock del mismo cerrojo)")
    ap.add_argument("--espera-cerrojo", type=int, default=ESPERA_CERROJO, help="segundos de espera por el cerrojo en cada recálculo")
    ap.add_argument("--cerrojo-ya-tomado", action="store_true", default=os.environ.get("HOJA_RESUMEN_CERROJO_YA_TOMADO") == "1",
                    help="el llamante ya tiene el cerrojo de LibreOffice (p. ej., verificar_paquete.sh bajo flock): no se toma otra vez "
                         "(también con HOJA_RESUMEN_CERROJO_YA_TOMADO=1)")
    ap.add_argument("--tasas", default=",".join(str(t) for t in TASAS))
    ap.add_argument("--antecedente", action="store_true",
                    help="permite generar la hoja de un análisis que el sistema oficial no da por vigente, rotulada «NO VIGENTE · ANTECEDENTE»")
    ap.add_argument("--comprobar", action="store_true")
    ap.add_argument("--verificar-origen", action="store_true")
    a = ap.parse_args(argv)
    exp = os.path.abspath(a.expediente)
    if not os.path.isdir(exp):
        print(f"no es una carpeta: {exp}")
        return 2
    salida = os.path.abspath(a.salida or exp)
    if a.comprobar:
        return comprobar(exp, salida)
    if a.verificar_origen:
        return verificar_origen(exp, salida)
    try:
        tasas = [float(x) for x in a.tasas.split(",") if x.strip()]
    except ValueError:
        print(f"--tasas no válidas: {a.tasas!r}")
        return 2
    if not tasas or any(not (0 < t < 1) for t in tasas):
        print(f"--tasas no válidas (entre 0 y 1): {a.tasas!r}")
        return 2
    return generar(exp, salida, a.trabajo, a.lock, tasas, antecedente=a.antecedente, espera=a.espera_cerrojo,
                   cerrojo_ya_tomado=a.cerrojo_ya_tomado)


if __name__ == "__main__":
    sys.exit(main())
