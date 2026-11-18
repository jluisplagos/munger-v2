#!/usr/bin/env python3
"""Hoja resumen en lenguaje llano de un expediente CERRADO (reorientación §7; criterios K5 y K9 de la lectura del informe).

Uso:
  hoja_resumen.py EXPEDIENTE [--salida DIR] [--trabajo DIR] [--lock ARCHIVO] [--tasas 0.07,0.08,0.09,0.10,0.11]
  hoja_resumen.py EXPEDIENTE --comprobar        (¿la hoja que hay sigue leyendo la ficha y el material vigentes?)
  hoja_resumen.py EXPEDIENTE --verificar-origen (¿cada frase del texto llano sale, tal cual, de lo que escribió el personaje?)

Lee del expediente cerrado: ficha.json, informe.md, precio.json, resultados.json, fase_c.json, estado_pipeline.json, el libro
evaluado <E>_v63_evaluada.xlsx y, si existen, cierre_vigente.json, fase1_metadatos.json y fase1_fuentes.json. Escribe en el
expediente (o en --salida) dos archivos propios y nuevos: hoja_resumen.md (una página para leer) y hoja_resumen.json (la
trazabilidad: huellas de lo leído, origen de cada frase y la tabla de sensibilidad con sus cifras exactas).

Lo que NO hace:
  - no cambia ningún archivo que ya exista en el expediente (ni el material auditado ni las salidas oficiales) y no es una salida
    oficial: es material de estudio que se genera después del cierre;
  - no escribe ningún hecho ni cifra propios: el texto llano son frases del personaje (tesis Análisis!B101, tesis inversa B102 y
    `cambiaria_de_cubo` de fase_c.json) seleccionadas por una regla fija y limpiadas solo de referencias a celdas y páginas;
  - la sensibilidad a la tasa se calcula en COPIAS del libro evaluado en las que solo cambia Análisis!C56 (r), recalculadas con
    LibreOffice (recalc.sh) siempre bajo `flock` del cerrojo común, y leídas con leer_resultados.py y precio_de_si.py, como en el
    pipeline. Las copias se borran al terminar.

Códigos: 0 hecho (o hoja vigente con --comprobar) · 2 uso · 3 expediente no cerrado o incompleto · 4 hoja desactualizada o ausente
(--comprobar) / frase sin origen (--verificar-origen) · 5 la sensibilidad a la tasa heredada no reproduce el precio de Sí oficial ·
6 fallo del recálculo o de la lectura.
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

VERSION_HOJA = "1.0"
TASAS = (0.07, 0.08, 0.09, 0.10, 0.11)
CELDA_TASA = ("Análisis", "C56")
LOCK_DEFECTO = os.environ.get("HOJA_RESUMEN_LOCK", "/home/user/e_work/libreoffice.lock")
SALIDA_MD, SALIDA_JSON = "hoja_resumen.md", "hoja_resumen.json"
OBLIGATORIOS = ("ficha.json", "informe.md", "precio.json", "resultados.json", "fase_c.json", "estado_pipeline.json")
OPCIONALES = ("cierre_vigente.json", "fase1_metadatos.json", "fase1_fuentes.json", "fase1_v63.json")

ZONA_LLANA = {
    "bajo_malo": "bajo el MALO: por debajo del valor del escenario MALO",
    "cumple_regla_k": "cumple: en el precio de Sí o por debajo",
    "vigilar": "vigilar: entre el precio de Sí y el valor ponderado",
    "caro": "caro: por encima del valor ponderado",
}
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


class ErrorExpediente(Exception):
    pass


# ------------------------------------------------------------------------------------------------ utilidades
def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def cargar(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


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
    return len(re.findall(r"[\wÁÉÍÓÚÑáéíóúñ]+", t))


def obtener_campo(fase_c, campo):
    if campo in ("B101", "B102"):
        return (fase_c.get("celdas") or {}).get(campo)
    v = fase_c
    for k in campo.split("."):
        v = (v or {}).get(k) if isinstance(v, dict) else None
    return v


def seleccionar_parrafo(fase_c):
    """Regla fija (no hay juicio en la selección): 1) tesis, frase 1 (qué hace la empresa); 2) tesis, frase 2 (por qué);
    3) tesis, última frase (el veredicto); 4) tesis inversa, primera frase con al menos 6 palabras (el riesgo principal);
    5) tesis inversa, última frase; 6) «a No», frase 1 (lo que lo haría falso). Sin repetir frases; si quedan menos de 5, se
    completa con las frases siguientes de la tesis y de la tesis inversa, en orden, hasta 5 (máximo 8)."""
    t, ti, no = (frases(obtener_campo(fase_c, c)) for c in ("B101", "B102", "cambiaria_de_cubo.a_no"))
    elegidas = []

    def poner(campo, lista, idx):
        if 0 <= idx < len(lista) and not any(e["campo"] == campo and e["indice"] == idx for e in elegidas) and len(elegidas) < 8:
            elegidas.append({"campo": campo, "indice": idx, "original": lista[idx], "texto": limpiar(lista[idx])})

    poner("B101", t, 0)
    poner("B101", t, 1)
    poner("B101", t, len(t) - 1)
    k = next((i for i, f in enumerate(ti) if _n_palabras(limpiar(f)) >= 6), None)
    if k is not None:
        poner("B102", ti, k)
    poner("B102", ti, len(ti) - 1)
    poner("cambiaria_de_cubo.a_no", no, 0)
    extra = [("B101", t, i) for i in range(len(t))] + [("B102", ti, i) for i in range(len(ti))]
    for campo, lista, i in extra:
        if len(elegidas) >= 5:
            break
        poner(campo, lista, i)
    orden = {"B101": 0, "B102": 1, "cambiaria_de_cubo.a_no": 2}
    elegidas.sort(key=lambda e: (orden[e["campo"]], e["indice"]))
    return [e for e in elegidas if e["texto"]]


def texto_con_origen(fase_c, campo):
    """Un campo entero del personaje, frase a frase, limpiado igual que el párrafo (para «lo que lo haría falso»)."""
    return [{"campo": campo, "indice": i, "original": f, "texto": limpiar(f)} for i, f in enumerate(frases(obtener_campo(fase_c, campo)))]


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


# ------------------------------------------------------------------------------------------------ expediente cerrado
def libro_evaluado(exp):
    c = sorted(glob.glob(os.path.join(exp, "*_v63_evaluada.xlsx")))
    if len(c) != 1:
        raise ErrorExpediente(f"se esperaba un libro evaluado <E>_v63_evaluada.xlsx y hay {len(c)}")
    return c[0]


def leer_expediente(exp):
    """Comprueba que el expediente está cerrado y que lo que se lee es el material de ese cierre. Lanza ErrorExpediente si no."""
    falta = [f for f in OBLIGATORIOS if not os.path.isfile(os.path.join(exp, f))]
    if falta:
        raise ErrorExpediente("faltan archivos del cierre: " + ", ".join(falta))
    libro = libro_evaluado(exp)
    d = {f: cargar(os.path.join(exp, f)) for f in OBLIGATORIOS if f.endswith(".json")}
    for f in OPCIONALES:
        p = os.path.join(exp, f)
        d[f] = cargar(p) if os.path.isfile(p) else None
    ficha, st, precio = d["ficha.json"], d["estado_pipeline.json"], d["precio.json"]
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
    return d, libro, huellas


# ------------------------------------------------------------------------------------------------ sensibilidad a la tasa
def _correr(cmd, timeout=900):
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def sensibilidad(libro, k, tasas, trabajo=None, lock=LOCK_DEFECTO):
    """Para cada tasa: copia del libro evaluado con solo Análisis!C56 = r, recálculo forzado con LibreOffice bajo flock, lectura
    (leer_resultados.py --exigir-recalculo-forzado) y escalera (precio_de_si.calcular con la misma k). Las copias se borran."""
    base = tempfile.mkdtemp(prefix="hoja_tasa_", dir=trabajo)
    filas = []
    try:
        perfil = os.path.join(base, "perfil_lo")
        for r in tasas:
            d = os.path.join(base, f"r{round(r * 10000):05d}")
            os.makedirs(os.path.join(d, "in"))
            copia = os.path.join(d, "in", os.path.basename(libro))
            L = LibroV63(libro)
            L.escribir_celdas({f"{CELDA_TASA[0]}!{CELDA_TASA[1]}": r})
            L.guardar(copia)
            rc, out = _correr(["flock", lock, "bash", os.path.join(AQUI, "recalc.sh"), copia, os.path.join(d, "out"), perfil])
            rec = os.path.join(d, "out", os.path.basename(libro))
            if rc != 0 or not os.path.isfile(rec):
                raise RuntimeError(f"recálculo con r = {r}: {out[-300:]}")
            jres = os.path.join(d, "resultados.json")
            rc, out = _correr([sys.executable, os.path.join(AQUI, "leer_resultados.py"), rec, jres, "--exigir-recalculo-forzado"])
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
                          "estado_tecnico": (res.get("estados") or {}).get("estado_tecnico_B255")})
    finally:
        shutil.rmtree(base, ignore_errors=True)
    return filas


def reproduce_oficial(fila, precio):
    claves = ("precio_si", "ponderado", "zona", "V", "precio", "g_impl_actual")
    dif = {c: (fila.get(c), precio.get(c)) for c in claves if fila.get(c) != precio.get(c)}
    return not dif, dif


def firmeza(filas):
    z = {round(f["r"], 4): f.get("zona") for f in filas}
    tramo = [z.get(0.08), z.get(0.09), z.get(0.10)]
    if None in tramo:
        return None, "no se puede decir: falta la zona en alguna de las tasas del 8, 9 o 10 %"
    if len(set(tramo)) == 1:
        return True, f"firme: la zona no cambia entre el 8 y el 10 % ({ZONA_LLANA.get(tramo[0], tramo[0])})"
    return False, ("no firme: la zona cambia entre el 8 y el 10 % (" +
                   " · ".join(f"{p} %: {ZONA_LLANA.get(x, x)}" for p, x in zip((8, 9, 10), tramo)) + ")")


# ------------------------------------------------------------------------------------------------ composición
def aptitud(ficha):
    a = ficha.get("aptitud_de_uso")
    if not isinstance(a, dict):
        return ("experimental; no apto para dinero real",
                "la ficha no declara la aptitud de uso, es anterior a ese bloque: no se presume ninguna", None)
    if a.get("apto_para_dinero_real") is True:
        return ("la ficha declara apto para dinero real", "según la ficha, aptitud_de_uso; esta hoja no lo evalúa", a)
    return (f"{a.get('caracter') or 'experimental'}; no apto para dinero real",
            f"según la ficha, aptitud_de_uso de la entrega {a.get('version')}", a)


def fechas(d, ficha):
    """Fechas por separado, de fase1_metadatos.json o, si no está (expedientes anteriores), de fase1_v63.json; «no consta» si no hay."""
    f1 = d.get("fase1_v63.json") or {}
    meta = d.get("fase1_metadatos.json") or f1
    origen = "fase1_metadatos.json" if d.get("fase1_metadatos.json") else ("fase1_v63.json" if f1 else None)
    fu = d.get("fase1_fuentes.json") or {}
    anios = sorted(str(k) for k in fu if re.fullmatch(r"\d{4}", str(k))) if isinstance(fu, dict) else []
    plantilla_fu = "documentos de los ejercicios {a} a {b} ({n} ejercicios; fase1_fuentes.json)"
    if not anios:
        anios = sorted(str(a) for a in ((f1.get("historia") or {}).get("anios") or []) if re.fullmatch(r"\d{4}", str(a)))
        plantilla_fu = "años de la Historia de {a} a {b} ({n}; fase1_v63.json: este expediente no tiene fase1_fuentes.json)"
    base = (f"ejercicio {anios[-1]}" + (f" (cierre fiscal: {meta['cierre_fiscal']})" if meta.get("cierre_fiscal") else "")) if anios else "no consta"
    fuentes = plantilla_fu.format(a=anios[0], b=anios[-1], n=len(anios)) if anios else "no consta"
    pie = f" ({origen})" if origen else ""
    return [
        ("Análisis", fecha_larga(ficha.get("fecha"))),
        ("Datos base (último ejercicio de la Historia)", base),
        ("Precio", fecha_larga((meta.get("precio") or {}).get("fecha")) + pie),
        ("Acciones", fecha_larga((meta.get("acciones_diluidas") or {}).get("fecha")) + pie),
        ("Fuentes", fuentes),
    ]


def predicciones(fase_c, ficha):
    ce = fase_c.get("celdas") or {}
    out, avisos = [], []
    for i, fila in enumerate((38, 39, 40)):
        p = {"texto": ce.get(f"Palancas!A{fila}"), "fecha": fecha_iso(ce.get(f"Palancas!B{fila}")), "prob": ce.get(f"Palancas!C{fila}"),
             "celdas": f"Palancas!A{fila}:C{fila}"}
        out.append(p)
        fp = (ficha.get("predicciones") or [None] * 3)[i] if i < len(ficha.get("predicciones") or []) else None
        if not fp or fp.get("texto") != p["texto"] or fp.get("fecha") != p["fecha"] or fp.get("prob") != p["prob"]:
            avisos.append(f"la predicción {i + 1} de fase_c.json (Palancas A{fila}:C{fila}) no coincide con la de la ficha")
    return out, avisos


def componer(exp, d, libro, huellas, filas, tasa_heredada, reproduce, dif):
    ficha, fase_c, precio = d["ficha.json"], d["fase_c.json"], d["precio.json"]
    mon = ficha.get("moneda")
    dec = ficha.get("decision") or {}
    apt_corta, apt_nota, _ = aptitud(ficha)
    estado = str(ficha.get("estado_analisis") or "sin estado").replace("_", " ")
    accion = dec.get("accion") or f"sin acción (estado {estado})"
    psi = precio.get("precio_si")
    parrafo = seleccionar_parrafo(fase_c)
    falso = {c: texto_con_origen(fase_c, c) for c in ("cambiaria_de_cubo.a_no", "cambiaria_de_cubo.a_si", "cambiaria_de_cubo.a_demasiado_dificil",
                                                      "decision.condiciones_revision.a_la_baja", "decision.condiciones_revision.al_alza")}
    preds, avisos = predicciones(fase_c, ficha)
    tesis_libro = ((d["resultados.json"].get("celdas_juicio_analisis") or {}))
    for c in ("B101", "B102"):
        if tesis_libro.get(c) not in (None, obtener_campo(fase_c, c)):
            avisos.append(f"Análisis!{c} del libro evaluado no es el texto de fase_c.json")
    firme, firme_txt = firmeza(filas)
    L = []
    L.append(f"# {ficha.get('empresa')} ({ficha.get('ticker')}) · hoja resumen")
    L.append("")
    L.append(f"> Material de estudio en lenguaje llano, generado después del cierre a partir de las salidas oficiales. No es una salida "
             f"oficial ni la sustituye; si la ficha cambia, esta hoja se regenera (`hoja_resumen.py`). Ficha leída: `{huellas['ficha.json'][:16]}…`.")
    L.append("")
    L.append(f"**Veredicto del personaje** — {estado} · cubo **{ficha.get('cubo') or '—'}** · acción **{accion}** · precio de Sí "
             f"**{dinero(psi, mon)}** (precio actual {dinero(precio.get('precio'), mon)}, {ZONA_LLANA.get(precio.get('zona'), precio.get('zona') or '—')}) · "
             f"**{apt_corta}** — {apt_nota}.")
    L.append("")
    L.append("## En pocas palabras")
    L.append("")
    L.append(" ".join(f"{e['texto']} [{n}]" for n, e in enumerate(parrafo, 1)))
    L.append("")
    L.append("*Origen de cada frase* (fase_c.json, texto del personaje; solo se quitan las referencias a celdas y páginas, que están en el "
             "informe, §8 y §10): " + " · ".join(f"[{n}] {FUENTE_TEXTO[e['campo']]}, frase {e['indice'] + 1}" for n, e in enumerate(parrafo, 1)) + ".")
    L.append("")
    L.append("## Lo que lo haría falso")
    L.append("")
    L.append("*Texto del personaje* (fase_c.json: `cambiaria_de_cubo` y `decision.condiciones_revision`; sin referencias a corchetes de fuente):")
    L.append("")
    for campo, rot in (("cambiaria_de_cubo.a_no", "Pasaría a **No**"), ("cambiaria_de_cubo.a_si", "Pasaría a **Sí**"),
                       ("cambiaria_de_cubo.a_demasiado_dificil", "Pasaría a **Demasiado difícil**"),
                       ("decision.condiciones_revision.a_la_baja", "Revisión **a la baja**"), ("decision.condiciones_revision.al_alza", "Revisión **al alza**")):
        if falso[campo]:
            L.append(f"- {rot}: " + " ".join(e["texto"] for e in falso[campo]))
    L.append("")
    L.append("## Cuánto depende de la tasa")
    L.append("")
    L.append(f"Recalculado en copias del libro evaluado cambiando solo la tasa exigida (Análisis!C56). Precio actual: {dinero(precio.get('precio'), mon)}.")
    L.append("")
    L.append("| Tasa | Precio de Sí | Valor ponderado | Dónde queda el precio actual | Crecimiento que el precio da por hecho (años 1–5) |")
    L.append("|---|---|---|---|---|")
    for f in filas:
        rot = pct(f["r"], 0) + (" (heredada)" if abs(f["r"] - tasa_heredada) < 1e-12 else "")
        if f.get("sin_lectura") or f.get("sin_escalera"):
            L.append(f"| {rot} | sin lectura: {f.get('sin_lectura') or f.get('sin_escalera')} | — | — | — |")
            continue
        g = f.get("g_impl_actual")
        L.append(f"| {rot} | {dinero(f.get('precio_si'), mon)} | {dinero(f.get('ponderado'), mon)} | {ZONA_LLANA.get(f.get('zona'), f.get('zona'))} | "
                 f"{pct(g) if es_num(g) else g} |")
    L.append("")
    L.append(f"- **El {pct(tasa_heredada, 0)} es provisional**: es la tasa heredada; la tasa no está decidida.")
    L.append("- **La prueba del 10 % es información, no condición.**")
    L.append(f"- Conclusión **{firme_txt}**." if firme is not None else f"- {firme_txt}.")
    L.append(f"- Comprobación: a la tasa heredada la copia reproduce exactamente el precio de Sí oficial de precio.json: "
             f"**{'sí' if reproduce else 'NO — ' + json.dumps(dif, ensure_ascii=False)}**.")
    L.append("")
    L.append("## Predicciones fechadas")
    L.append("")
    L.append("Se comprueban en esta fecha con este dato:")
    L.append("")
    for n, p in enumerate(preds, 1):
        L.append(f"{n}. **{fecha_larga(p['fecha'])}** — {p['texto']} Probabilidad que le da el personaje: {pct(p['prob'], 0)}.")
    L.append("")
    L.append("## Fechas y versión")
    L.append("")
    for rot, v in fechas(d, ficha):
        L.append(f"- {rot}: {v}.")
    ver = ficha.get("versiones") or {}
    L.append(f"- Versión del personaje: {ver.get('personaje')} · plantilla {ver.get('plantilla')} · configuración {ver.get('config')} · hoja resumen {VERSION_HOJA}.")
    if avisos:
        L.append("")
        L.append("**Avisos:** " + " · ".join(avisos) + ".")
    L.append("")
    traza = {
        "version_hoja": VERSION_HOJA, "generada": dt.datetime.now().isoformat(timespec="seconds"),
        "expediente": os.path.abspath(exp), "entradas_sha256": huellas,
        "veredicto": {"estado_analisis": ficha.get("estado_analisis"), "cubo": ficha.get("cubo"), "accion": dec.get("accion"),
                      "precio_si": psi, "precio": precio.get("precio"), "zona": precio.get("zona"), "ponderado": precio.get("ponderado"),
                      "aptitud": apt_corta, "aptitud_nota": apt_nota},
        "parrafo": parrafo, "lo_que_lo_haria_falso": falso, "predicciones": preds,
        "sensibilidad": {"celda_tasa": "!".join(CELDA_TASA), "tasa_heredada": tasa_heredada, "k": precio.get("k"), "filas": filas,
                         "reproduce_oficial": reproduce, "diferencias": dif, "firme": firme, "firme_texto": firme_txt},
        "fechas": fechas(d, ficha), "versiones": ver, "avisos": avisos,
    }
    return "\n".join(L), traza


# ------------------------------------------------------------------------------------------------ órdenes
def comprobar(exp, salida):
    pj = os.path.join(salida, SALIDA_JSON)
    if not os.path.isfile(pj) or not os.path.isfile(os.path.join(salida, SALIDA_MD)):
        print(f"SIN HOJA: no hay {SALIDA_MD} y {SALIDA_JSON} en {salida}")
        return 4
    t = cargar(pj)
    cambios = []
    for f, h in (t.get("entradas_sha256") or {}).items():
        p = os.path.join(exp, f)
        if not os.path.isfile(p):
            cambios.append(f"{f} ya no está")
        elif sha256(p) != h:
            cambios.append(f"{f} cambió")
    if cambios:
        print("HOJA DESACTUALIZADA: " + "; ".join(cambios) + f". Regenerarla: hoja_resumen.py {exp}")
        return 4
    print(f"HOJA VIGENTE: lee la ficha {t['entradas_sha256']['ficha.json'][:16]}… y el material actual del expediente")
    return 0


def verificar_origen(exp, salida):
    t = cargar(os.path.join(salida, SALIDA_JSON))
    fase_c = cargar(os.path.join(exp, "fase_c.json"))
    todas = list(t.get("parrafo") or []) + [e for v in (t.get("lo_que_lo_haria_falso") or {}).values() for e in v]
    fallos = verificar_origen_frases(todas, fase_c)
    md = open(os.path.join(salida, SALIDA_MD), encoding="utf-8").read()
    for e in t.get("parrafo") or []:
        if e["texto"] not in md:
            fallos.append(f"frase del párrafo que no está en {SALIDA_MD}: {e['texto'][:60]!r}")
    print(("ORIGEN COMPROBADO: " if not fallos else "FRASES SIN ORIGEN: ") + (f"{len(todas)} frases" if not fallos else " | ".join(fallos)))
    return 0 if not fallos else 4


def generar(exp, salida, trabajo, lock, tasas):
    try:
        d, libro, huellas = leer_expediente(exp)
    except ErrorExpediente as e:
        print(f"EXPEDIENTE NO CERRADO O INCOMPLETO: {e}")
        return 3
    precio = d["precio.json"]
    previa = os.path.join(salida, SALIDA_JSON)
    if os.path.isfile(previa):
        try:
            ant = (cargar(previa).get("entradas_sha256") or {}).get("ficha.json")
        except (OSError, ValueError):
            ant = None
        if ant and ant != huellas["ficha.json"]:
            print(f"AVISO: la ficha cambió desde la hoja anterior ({ant[:16]}… → {huellas['ficha.json'][:16]}…): se regenera")
    r_her = LibroV63(libro).leer(*CELDA_TASA)
    if not es_num(r_her):
        print(f"EXPEDIENTE NO CERRADO O INCOMPLETO: Análisis!C56 del libro evaluado no es un número ({r_her!r})")
        return 3
    lista = sorted(set(list(tasas) + [r_her]))
    filas, reproduce, dif = [], False, {"motivo": "sin escalera oficial"}
    if "precio_si" in precio:
        try:
            filas = sensibilidad(libro, precio.get("k", PS.K_DEFECTO), lista, trabajo=trabajo, lock=lock)
        except (RuntimeError, subprocess.TimeoutExpired, OSError) as e:
            print(f"FALLO DEL RECÁLCULO: {e}")
            return 6
        fh = next(f for f in filas if f["r"] == r_her)
        reproduce, dif = reproduce_oficial(fh, precio)
    md, traza = componer(exp, d, libro, huellas, filas, r_her, reproduce, dif)
    os.makedirs(salida, exist_ok=True)
    for nombre, contenido in ((SALIDA_JSON, json.dumps(traza, ensure_ascii=False, indent=1)), (SALIDA_MD, md)):
        tmp = os.path.join(salida, f".{nombre}.tmp")
        with open(tmp, "w", encoding="utf-8") as f:
            f.write(contenido if contenido.endswith("\n") else contenido + "\n")
        os.replace(tmp, os.path.join(salida, nombre))
    fallos = verificar_origen_frases(traza["parrafo"] + [e for v in traza["lo_que_lo_haria_falso"].values() for e in v], d["fase_c.json"])
    print(f"OK: {os.path.join(salida, SALIDA_MD)} · {len(traza['parrafo'])} frases con origen · tasas "
          + ", ".join(pct(f['r'], 0) for f in filas) + f" · reproduce el oficial a {pct(r_her, 0)}: {'sí' if reproduce else 'NO'}"
          + f" · {traza['sensibilidad']['firme_texto']}")
    if fallos:
        print("FRASES SIN ORIGEN: " + " | ".join(fallos))
        return 4
    if "precio_si" in precio and not reproduce:
        print("LA SENSIBILIDAD NO REPRODUCE EL PRECIO DE SÍ OFICIAL: " + json.dumps(dif, ensure_ascii=False))
        return 5
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("expediente")
    ap.add_argument("--salida", help="carpeta donde escribir la hoja (por defecto, el expediente)")
    ap.add_argument("--trabajo", help="carpeta para las copias temporales (se borran)")
    ap.add_argument("--lock", default=LOCK_DEFECTO, help="cerrojo de LibreOffice para flock")
    ap.add_argument("--tasas", default=",".join(str(t) for t in TASAS))
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
    return generar(exp, salida, a.trabajo, a.lock, tasas)


if __name__ == "__main__":
    sys.exit(main())
