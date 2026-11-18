#!/usr/bin/env python3
"""Cierre del análisis (reparación del cierre, entrega 4.6). Reglas compartidas por pipeline.py, ficha.py e informe.py.

1. Material auditado (incidencia I1). La fase C solo PROPONE el estado. En el paso 11 el pipeline escribe el material provisional
   (`ficha_provisional.json`, `informe_provisional.md`); en el paso 13, antes de pedir la auditoría, fija la huella del material
   sometido a revisión (`material_auditoria.json`: SHA-256 de cada artefacto y un identificador). El auditor copia ese
   identificador en una línea `Material auditado: <id>`. El cierre oficial (paso 14, o `ficha.py` sin `--provisional` con
   `concluido`) exige: veredicto APROBADO según la regla estricta de H2 (pipeline.Pipeline.veredicto_auditoria, sin cambios),
   la línea de material igual al identificador fijado, y el material actual igual al fijado. Si cambia un artefacto, una
   aprobación anterior no vale para la versión nueva.
1b. Solicitud de auditoría (4.8.1, R-T1). La auditoría responde a una solicitud con identificador propio («Solicitud de auditoría:
   SA-…»), registrada por el paso 13 y ligada al material fijado. Un cierre aprobado como respuesta a una solicitud exige que
   auditoria.md sea esa respuesta (huella en estado_pipeline.json → auditoria_respuesta).
1c. Identidad de la respuesta aceptada (4.9, R-V1). Dos funciones separadas: A, detección de posibles reutilizaciones en el paso 13
   (huella_contenido, conservadora, sin orden); B, comprobación fiel de que auditoria.md es la respuesta aceptada (solicitud, material
   y huella_fiel con el contenido y el orden íntegros, salvo TRANSFORMACIONES_INOCUAS). La vigencia solo usa B.
2. Marca «con datos de etapa 1 incompletos» (I2): se activa solo por `entrada_v63.json → necesarios_para_listo_provisional`
   no vacío (nunca por el texto «NO LISTO» ni por los no bloqueantes) y conserva la lista exacta de causas.
3. Correspondencia D10 ↔ estado ↔ acción ↔ etiqueta de C104 (I3): tabla cerrada FUNDAMENTO_C104.
4. Alcance declarado del expediente (I4): `alcance_v2.json`, metadato explícito; sin él no hay aviso.
"""
import glob
import hashlib
import json
import os
import re
import unicodedata

MARCA_ETAPA1 = "con datos de etapa 1 incompletos"
LINEA_MATERIAL = re.compile(r"^[\s>*_-]*Material auditado[\s*_]*:[\s*_`]*([0-9a-f]{16})[\s*_`.]*$", re.I)
MATERIAL_FIJO = ["fase_a.json", "fase_a.md", "fase_b.json", "fase_b.md", "fase_c.json", "fase_c.md", "extracto_v63.md", "datos_ausentes.json",
                 "entrada_v63.json", "referencias_mecanicas.json", "resultados.json", "precio.json", "gramatica.json", "comprobacion_conjunta.json",
                 "ficha_provisional.json", "informe_provisional.md", "alcance_v2.json",
                 # (4.11) solo existen en expedientes con la plantilla V6.4 experimental: la configuración económica activa, la selección
                 # explícita de plantilla y referencia, y las variantes calculadas. Cambiar cualquiera retira la aprobación en la primera
                 # llamada (el material cambia), aunque el libro todavía no se haya recalculado. Los expedientes V6.3 no tienen estos
                 # archivos: su material (y su identificador) no cambia.
                 "configuracion_economica.json", "plantilla_activa.json", "configuracion_v64_variantes.json",
                 # (4.12 §5) cadena de trazabilidad del libro final (solo la escribe el pipeline en expedientes V6.4)
                 "cadena_trazabilidad.json"]


# ---------- 1. material auditado ----------
def _sha(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def material(carpeta, empresa=None):
    """{archivo: sha256} de los artefactos que se someten a la auditoría (los que existen) y su identificador."""
    e = empresa or os.path.basename(os.path.abspath(carpeta))
    nombres = MATERIAL_FIJO + [f"{e}_v63_evaluada.xlsx", f"{e}_v63_datos.xlsx"]
    huellas = {n: _sha(os.path.join(carpeta, n)) for n in nombres if os.path.isfile(os.path.join(carpeta, n))}
    ident = hashlib.sha256(json.dumps(sorted(huellas.items())).encode("utf-8")).hexdigest()[:16]
    return ident, huellas


def fijar_material(carpeta, empresa=None):
    ident, huellas = material(carpeta, empresa)
    json.dump({"id": ident, "archivos": huellas, "nota": "material sometido a la auditoría del paso 13; el auditor copia el id en «Material auditado: <id>»"},
              open(os.path.join(carpeta, "material_auditoria.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return ident


def material_fijado(carpeta):
    p = os.path.join(carpeta, "material_auditoria.json")
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else None


def id_en_auditoria(txt):
    """Identificador de la línea «Material auditado: <id>»; None si falta o hay más de una."""
    ids = [m.group(1).lower() for m in (LINEA_MATERIAL.match(l) for l in txt.replace("\\.", ".").splitlines()) if m]
    return ids[0] if len(ids) == 1 else None


# ---------- 1b. solicitud de auditoría (4.8.1, R-T1) ----------
# Hasta la 4.8, el paso 13 aceptaba como respuesta cualquier auditoria.md con una fecha de modificación posterior a la del último
# consumo: un informe antiguo con otra fecha (descompresión en otra zona horaria o con fechas renovadas) pasaba por una
# respuesta nueva. Desde la 4.8.1, cada petición de auditoría es una SOLICITUD con un identificador propio, persistente en
# estado_pipeline.json → solicitudes_auditoria y escrito en solicitud_auditoria.json y en el prompt. Una auditoría solo responde a
# la solicitud cuyo identificador nombra («Solicitud de auditoría: SA-…»); si aprueba, nunca una auditoría ya conocida (huella o contenido).
# Las fechas de los archivos no intervienen. La regla H2 (veredicto) y la vinculación al material no cambian.
SOLICITUD_AUDITORIA = "solicitud_auditoria.json"
LINEA_SOLICITUD = re.compile(r"^[\s>*_-]*Solicitud de auditor[ií]a[\s*_]*:[\s*_`]*(SA-[0-9a-f]{16})[\s*_`.]*$", re.I)


def nueva_solicitud(material_id, motivo, ahora):
    """Solicitud nueva: identificador imprevisible (no se deriva de ninguna auditoría existente) ligado al material fijado."""
    semilla = f"{material_id}|{ahora}|{os.urandom(16).hex()}"
    return {"id": "SA-" + hashlib.sha256(semilla.encode("utf-8")).hexdigest()[:16], "material": material_id, "creada": ahora,
            "motivo": motivo, "estado": "pendiente", "respuesta_sha256": None, "respondida": None, "veredicto": None}


def escribir_solicitud(carpeta, sol):
    json.dump({"id": sol["id"], "material": sol["material"], "creada": sol["creada"], "motivo": sol.get("motivo"),
               "nota": "solicitud de auditoría vigente del paso 13: el auditor copia el id en «Solicitud de auditoría: <id>» y el id de "
                       "material_auditoria.json en «Material auditado: <id>». Una auditoría anterior, aunque se copie o cambie de fecha, no "
                       "responde a esta solicitud."},
              open(os.path.join(carpeta, SOLICITUD_AUDITORIA), "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def _nfkc(txt):
    return unicodedata.normalize("NFKC", txt)


def id_solicitud_en_auditoria(txt):
    """Identificador de la línea «Solicitud de auditoría: SA-<16 hex>»; None si falta o hay más de una."""
    ids = ["SA-" + m.group(1)[3:].lower() for m in (LINEA_SOLICITUD.match(l) for l in _nfkc(txt).replace("\\.", ".").splitlines()) if m]
    return ids[0] if len(ids) == 1 else None


def sha_archivo(p):
    return _sha(p) if os.path.isfile(p) else None


def _sin_diacriticos(s):
    return "".join(c for c in unicodedata.normalize("NFKD", s) if unicodedata.category(c) != "Mn")


def huella_contenido(txt):
    """FUNCIÓN A (4.9, R-V1): DETECTOR conservador de posibles reutilizaciones, solo para el paso 13. NO acredita la identidad de
    una respuesta aprobada: para eso está huella_fiel (función B).
    Huella del contenido de una auditoría sin la línea de solicitud y sin formato: el MULTICONJUNTO de sus palabras (secuencias de
    letras y cifras), tras la forma Unicode NFKC, sin marcas diacríticas y con casefold. No cuentan los espacios, los saltos y cortes
    de línea, la puntuación, los separadores, las marcas de markdown, las tildes ni el orden; sí cuenta cuántas veces aparece cada
    palabra. Una auditoría ya usada a la que solo se añade la línea de una solicitud nueva o se cambia el formato tiene la misma.
    Por eso sirve para RECHAZAR una aprobación que podría ser reutilizada (falsos positivos aceptados: dos textos con las mismas
    palabras en otro orden se tratan como el mismo) y no sirve para ACEPTAR que un auditoria.md es la respuesta aceptada (dos textos
    con las mismas palabras en otro orden pueden decir lo contrario: «la evidencia respalda el crecimiento; la reposición queda
    pendiente» frente a «la evidencia respalda la reposición; el crecimiento queda pendiente»).
    (Auditoría interna de la 4.8.1, Y-a; control de vigencia, V-1; tercera revisión, W-1: el corte de las líneas no cuenta.)"""
    lineas = [l for l in _nfkc(txt).replace("\\.", ".").splitlines() if not LINEA_SOLICITUD.match(l)]
    palabras = re.findall(r"[^\W_]+", _sin_diacriticos("\n".join(lineas)).casefold())
    return hashlib.sha256("\n".join(sorted(palabras)).encode("utf-8")).hexdigest()


# ---------- 1c. identidad de la respuesta aceptada (4.9, R-V1) ----------
# FUNCIÓN B. Desde la 4.9, una aprobación registrada como respuesta a una solicitud solo sigue vigente si auditoria.md ES esa
# respuesta: se comprueban por separado (1) la solicitud (exactamente una línea «Solicitud de auditoría», la de la respuesta
# aceptada, que consta como respondida por ella y es del material fijado), (2) el material (motivo_auditoria_no_corresponde, sin
# cambios) y (3) la respuesta, con su contenido y su orden íntegros (huella_fiel). Solo se admiten las transformaciones de abajo;
# cualquier otra diferencia (palabras, orden, mayúsculas, espacios, líneas, puntuación, la propia línea de solicitud) retira la
# aprobación. No es un clasificador de significado: es una comparación fiel del texto.
TRANSFORMACIONES_INOCUAS = (
    "una marca BOM UTF-8 al principio del archivo",
    "los finales de línea CRLF (Windows) o CR, que se leen como LF",
    "los saltos de línea al final del archivo (ninguno, uno o varios)",
    "la forma de normalización Unicode NFC o NFD del mismo texto (canónicamente equivalentes: mismos caracteres visibles y mismo significado)",
)


def texto_fiel(datos):
    """Texto de una auditoría tras aplicar SOLO las TRANSFORMACIONES_INOCUAS; None si no es UTF-8 válido. `datos`: bytes o str."""
    if isinstance(datos, str):
        datos = datos.encode("utf-8")
    if datos.startswith(b"\xef\xbb\xbf"):
        datos = datos[3:]
    try:
        t = datos.decode("utf-8")
    except UnicodeDecodeError:
        return None
    t = t.replace("\r\n", "\n").replace("\r", "\n")
    return unicodedata.normalize("NFC", t).rstrip("\n")


def huella_fiel(datos):
    """SHA-256 de texto_fiel(datos): identidad de una respuesta salvo las transformaciones inocuas; None si no es UTF-8 válido."""
    t = texto_fiel(datos)
    return None if t is None else hashlib.sha256(t.encode("utf-8")).hexdigest()


def lineas_solicitud(txt):
    """Identificadores de todas las líneas «Solicitud de auditoría: SA-…» (en orden; vacía si no hay ninguna)."""
    return ["SA-" + m.group(1)[3:].lower() for m in (LINEA_SOLICITUD.match(l) for l in _nfkc(txt).replace("\\.", ".").splitlines()) if m]


def motivo_respuesta_no_aceptada(carpeta, datos, st, resp):
    """None si auditoria.md (bytes `datos`) es la respuesta aceptada `resp` (estado_pipeline.json → auditoria_respuesta); si no, el
    motivo. No calcula ni registra ninguna huella nueva: una respuesta de la 4.8.1, que no tiene huella fiel registrada, solo se
    acredita con sus bytes exactos (compatibilidad, encargo 4.9 §3.3)."""
    pref = f"auditoria.md no es la respuesta registrada a la solicitud {resp.get('solicitud')}: "
    txt = texto_fiel(datos)
    if txt is None:
        return pref + "no es texto UTF-8 válido"
    ids = lineas_solicitud(txt)
    if not ids:
        return pref + "no tiene ninguna línea «Solicitud de auditoría» (la respuesta aceptada nombraba su solicitud)"
    if len(ids) > 1:
        return pref + f"tiene {len(ids)} líneas «Solicitud de auditoría» ({', '.join(ids)}); la respuesta aceptada tiene exactamente una"
    if ids[0] != resp.get("solicitud"):
        return pref + f"nombra la solicitud {ids[0]}, no la de la respuesta aceptada"
    sol = next((s for s in (st or {}).get("solicitudes_auditoria") or [] if s.get("id") == resp.get("solicitud")), None)
    if not sol or sol.get("estado") != "respondida" or sol.get("respuesta_sha256") != resp.get("sha256"):
        return pref + "esa solicitud no consta en estado_pipeline.json como respondida por la respuesta aceptada"
    fij = (material_fijado(carpeta) or {}).get("id")
    if resp.get("material") != fij or sol.get("material") != fij:
        return pref + f"la respuesta aceptada es del material {resp.get('material')}, no del fijado {fij}"
    if resp.get("fiel"):
        if huella_fiel(datos) != resp["fiel"]:
            return pref + ("su contenido o su orden cambiaron después de aceptarla (solo se admiten: " + "; ".join(TRANSFORMACIONES_INOCUAS)
                           + "); la aprobación no vale para otro texto")
    elif hashlib.sha256(datos).hexdigest() != resp.get("sha256"):
        return pref + ("no es byte a byte la respuesta aceptada y, como cierre anterior a la 4.9, no tiene huella fiel registrada: la "
                       "correspondencia no puede acreditarse (no se calcula una huella nueva para atribuírsela); hace falta una auditoría nueva")
    return None


def leer_texto(ruta, limite=50_000_000):
    """Texto de un archivo para buscar auditorías: UTF-8 (con o sin BOM), UTF-16 con BOM o, si no, cp1252; None si parece binario
    (bytes NUL sin BOM UTF-16) o pasa de `limite`. (Tercera revisión de la 4.8.1, W-2.)"""
    try:
        if os.path.getsize(ruta) > limite:
            return None
        b = open(ruta, "rb").read()
    except OSError:
        return None
    if b[:2] in (b"\xff\xfe", b"\xfe\xff"):
        try:
            return b.decode("utf-16")
        except UnicodeDecodeError:
            return None
    if b"\x00" in b[:65536]:
        return None
    for cod in ("utf-8-sig", "cp1252"):
        try:
            return b.decode(cod)
        except UnicodeDecodeError:
            continue
    return None


class RegistroAuditoriasIlegible(Exception):
    """auditorias_conocidas.json existe y no se puede leer: no se acepta ninguna auditoría hasta restaurarlo (V-9)."""


AUDITORIAS_CONOCIDAS = "auditorias_conocidas.json"


def parece_auditoria(txt, veredicto=None):
    """¿Es un texto de auditoría? Una línea «Material auditado: <id>», o un APROBADO según H2 si se pasa el lector (veredicto)."""
    if any(LINEA_MATERIAL.match(l) for l in _nfkc(txt).replace("\\.", ".").splitlines()):
        return True
    return bool(veredicto) and veredicto(txt) == "APROBADO"


EXTENSIONES_NO_TEXTO = (".xlsx", ".xls", ".pdf", ".zip", ".png", ".jpg", ".jpeg", ".gif", ".ods", ".odt", ".docx", ".pptx", ".gz", ".7z")


def auditorias_del_expediente(carpeta, veredicto=None):
    """Huellas (bytes y contenido) de todas las auditorías que hay en el expediente, con cualquier nombre y en cualquier subcarpeta:
    todo archivo de texto (UTF-8, UTF-16 con BOM o cp1252; no binario; hasta 50 MB) que tenga una línea «Material auditado» o que H2
    califique APROBADO, y la huella que
    guarda cierre_vigente.json. (Auditoría interna de la 4.8.1, Y-b, y control de vigencia, V-2: la primera versión solo miraba
    auditoria*.md de la carpeta y de historial_cierres/.)"""
    shas, conts = set(), set()
    for raiz, dirs, fs in os.walk(carpeta):
        dirs[:] = [d for d in dirs if d not in ("__pycache__", ".lo_perfil")]
        for f in fs:
            r = os.path.join(raiz, f)
            if f.lower().endswith(EXTENSIONES_NO_TEXTO) or not os.path.isfile(r):
                continue
            txt = leer_texto(r)
            if txt is None:
                continue
            if parece_auditoria(txt, veredicto):
                shas.add(_sha(r))
                conts.add(huella_contenido(txt))
    cv = _j_tolerante(os.path.join(carpeta, CIERRE_VIGENTE)) or {}
    if cv.get("auditoria_sha256"):
        shas.add(cv["auditoria_sha256"])
    return shas, conts


def registro_auditorias(carpeta):
    """Registro persistente de auditorías ya conocidas o usadas (auditorias_conocidas.json). Vive fuera de estado_pipeline.json:
    --reiniciar no lo borra."""
    p = os.path.join(carpeta, AUDITORIAS_CONOCIDAS)
    if not os.path.exists(p):
        return set(), set()
    try:
        d = json.load(open(p, encoding="utf-8"))
        s, c = d.get("sha256") or [], d.get("contenido") or []
        if not (isinstance(s, list) and isinstance(c, list) and all(isinstance(x, str) for x in s + c)):
            raise ValueError("«sha256» y «contenido» tienen que ser listas de huellas")  # (tercera revisión, W-3)
        return set(s), set(c)
    except (ValueError, OSError, AttributeError) as e:
        raise RegistroAuditoriasIlegible(f"{AUDITORIAS_CONOCIDAS} no se puede leer ({e}): restaurarlo desde una copia; mientras tanto no se acepta ninguna auditoría") from e


def anotar_auditorias(carpeta, shas, conts, motivo):
    s0, c0 = registro_auditorias(carpeta)
    s1, c1 = s0 | set(x for x in shas if x), c0 | set(x for x in conts if x)
    if (s1, c1) != (s0, c0) or not os.path.exists(os.path.join(carpeta, AUDITORIAS_CONOCIDAS)):
        json.dump({"nota": "huellas de auditorías ya conocidas o usadas en este expediente (4.8.1, R-T1): ninguna puede acreditar una aprobación que responda a una solicitud "
                           "de auditoría nueva. Solo se añaden huellas; no se borra ninguna.", "ultimo_motivo": motivo,
                   "sha256": sorted(s1), "contenido": sorted(c1)}, open(os.path.join(carpeta, AUDITORIAS_CONOCIDAS), "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def motivo_auditoria_no_corresponde(carpeta, txt, empresa=None):
    """None si la auditoría nombra el material fijado y el material actual es ese; si no, el motivo."""
    fij = material_fijado(carpeta)
    if not fij:
        return "no hay material_auditoria.json: el material no se fijó antes de pedir la auditoría"
    ida = id_en_auditoria(txt)
    if ida is None:
        return "la auditoría no tiene exactamente una línea «Material auditado: <id>»"
    if ida != fij["id"]:
        return f"la auditoría corresponde al material {ida}, no al fijado {fij['id']}"
    actual, huellas = material(carpeta, empresa)
    if actual != fij["id"]:
        cambiados = sorted(set(k for k in set(huellas) | set(fij["archivos"]) if huellas.get(k) != fij["archivos"].get(k)))
        return f"el material cambió después de la auditoría ({', '.join(cambiados)}): la aprobación no vale para la versión nueva"
    return None


def leer_json_control(p):
    """(objeto, None) si el archivo existe y es JSON válido; (None, None) si no existe; (None, motivo) si existe y no se puede leer
    (4.9, Z-2 de la auditoría interna: un archivo de control ilegible es un motivo de retirada, no una excepción)."""
    if not os.path.exists(p):
        return None, None
    try:
        obj = json.load(open(p, encoding="utf-8"))
    except (ValueError, OSError) as e:
        return None, f"{os.path.basename(p)} no se puede leer ({type(e).__name__}: {str(e)[:80]})"
    if not isinstance(obj, dict):
        # (4.9, control de vigencia V-2) un JSON válido que no es un objeto tampoco es un archivo de control legible
        return None, f"{os.path.basename(p)} no se puede leer (es JSON válido, pero no un objeto: {type(obj).__name__})"
    return obj, None


def leer_ficha_control(p):
    """(segundo control de vigencia de la 4.9, W-1) Como leer_json_control, pero una ficha cuyo «cierre» no es un objeto (o nulo) también
    es ilegible: no se puede saber qué aprobación registra."""
    F, err = leer_json_control(p)
    if F is not None and F.get("cierre") is not None and not isinstance(F.get("cierre"), dict):
        return None, f"{os.path.basename(p)} no se puede leer («cierre» no es un objeto)"
    return F, err


def _motivo_estructura(st, cv, fij):
    """(4.9, control de vigencia V-1 y V-2) Tipos mínimos de los archivos de control que lee el cierre; None si son los esperados."""
    if st is not None:
        sols = st.get("solicitudes_auditoria")
        if sols is not None and not (isinstance(sols, list) and all(isinstance(s, dict) and isinstance(s.get("id"), str) for s in sols)):
            # (segundo control de vigencia, W-1) también una solicitud sin «id» de texto
            return "estado_pipeline.json no se puede leer (solicitudes_auditoria no es una lista de solicitudes con «id»)"
        for k, tipo in (("historial", list), ("cierres_archivados", list), ("paso", int)):
            if st.get(k) is not None and not isinstance(st.get(k), tipo):
                return f"estado_pipeline.json no se puede leer («{k}» no tiene el tipo esperado)"
        resp = st.get("auditoria_respuesta")
        if resp is not None and not isinstance(resp, dict):
            return "estado_pipeline.json no se puede leer (auditoria_respuesta no es un objeto)"
    if fij is not None and not (isinstance(fij.get("id"), str) and isinstance(fij.get("archivos"), dict)):
        return "material_auditoria.json no se puede leer (le faltan «id» o «archivos»)"
    return None


def motivo_rechazo_cierre(carpeta, veredicto, estado_pipeline=None, empresa=None):
    """None si se puede confirmar el cierre oficial; si no, el motivo (I1). veredicto = pipeline.Pipeline.veredicto_auditoria."""
    p = os.path.join(carpeta, "auditoria.md")
    if not os.path.exists(p):
        return "no hay auditoria.md"
    try:
        datos = open(p, "rb").read()
    except OSError as e:
        # (4.9, control de vigencia V-2) p. ej., auditoria.md es una carpeta
        return f"auditoria.md no se puede leer ({type(e).__name__}): la aprobación se retira hasta una auditoría nueva"
    # (4.10, encargo §3.2) lectura común ANTES de H2 y de los lectores de solicitud y material: solo las TRANSFORMACIONES_INOCUAS
    # (texto_fiel). Hasta la 4.9 aquí se decodificaba en UTF-8 sin quitar la marca BOM: una respuesta aceptada que empezaba por
    # «1. PASA» y a la que solo se añadía (o que ya traía) un BOM conservaba su huella fiel, pero H2 leía «﻿1. PASA», no
    # reconocía el punto 1 y daba REPETIR, y las cuatro vías retiraban una aprobación legítima. La regla H2
    # (Pipeline.veredicto_auditoria) no cambia; las huellas de bytes se siguen calculando sobre los bytes reales.
    txt = texto_fiel(datos)
    if txt is None:
        # (4.9, Z-2) antes, una excepción interrumpía todas las vías y la aprobación seguía publicada
        return "auditoria.md no es texto UTF-8 válido: no se puede acreditar como la respuesta aprobada; la aprobación se retira hasta una auditoría nueva"
    v = veredicto(txt)
    if v != "APROBADO":
        return f"la auditoría dice {v} (regla estricta de H2)"
    st = estado_pipeline
    if st is None:
        st, err = leer_json_control(os.path.join(carpeta, "estado_pipeline.json"))
        if err:
            return f"{err}: no consta qué respuesta de auditoría se aprobó; la aprobación se retira hasta restaurarlo y, si no se puede acreditar, hasta una auditoría nueva"
    cv, err_cv = leer_json_control(os.path.join(carpeta, CIERRE_VIGENTE))
    if err_cv:
        return f"{err_cv}: no consta qué salidas y qué auditoría se registraron al cerrar; la aprobación se retira"
    fij, err_f = leer_json_control(os.path.join(carpeta, "material_auditoria.json"))
    m = err_f and f"{err_f}: no consta qué material se aprobó; la aprobación se retira" or _motivo_estructura(st, cv, fij)
    if m:
        return m if err_f else m + ": la aprobación se retira"
    if st is not None and st.get("auditoria") != "APROBADO":
        return f"el pipeline no registró una auditoría APROBADO válida (auditoria = {st.get('auditoria')!r})"
    if st is not None and st.get("material_auditoria") != (material_fijado(carpeta) or {}).get("id"):
        return "el material aprobado registrado en el pipeline no es el fijado en material_auditoria.json"
    m = motivo_aprobacion_retirada(carpeta, st, cv)  # (4.13.1, H5) una aprobación ya retirada no se reactiva restaurando archivos
    if m:
        return m
    pend = [s for s in (st or {}).get("solicitudes_auditoria") or [] if s.get("estado") == "pendiente"]
    if pend:
        # (4.8.1, Y-h de la auditoría interna) con una auditoría nueva pedida, ninguna aprobación anterior cierra (tampoco ficha.py ni la vigencia)
        return f"hay una solicitud de auditoría pendiente ({pend[-1]['id']}): el cierre exige su respuesta, no una aprobación anterior"
    resp = (st or {}).get("auditoria_respuesta")
    if resp:
        # (4.8.1, R-T1) la aprobación registrada es la de una respuesta concreta a una solicitud: otro auditoria.md no la hereda.
        # (4.9, R-V1) Hasta la 4.9 bastaba con que coincidiera huella_contenido, que descarta la línea de solicitud y el orden de las
        # palabras: seguían vigentes una solicitud cambiada, eliminada o duplicada y un texto con las mismas palabras y otro
        # significado. Ahora se comprueban por separado la solicitud, el material y la respuesta íntegra (función B); huella_contenido
        # queda solo como detector del paso 13 (función A). Los finales de línea siguen sin anularla (Y-i), por TRANSFORMACIONES_INOCUAS.
        m = motivo_respuesta_no_aceptada(carpeta, datos, st, resp)
        if m:
            return m
    else:
        cv = cv or {}
        if cv.get("auditoria_fiel") and cv.get("solicitud"):
            # (4.9) estado del pipeline ausente: el cierre registrado en cierre_vigente.json lleva su respuesta (solicitud y huella fiel)
            datos = open(p, "rb").read()
            ids = lineas_solicitud(texto_fiel(datos) or "")
            if ids != [cv["solicitud"]] or huella_fiel(datos) != cv["auditoria_fiel"]:
                return (f"auditoria.md no es la respuesta registrada en cierre_vigente.json (solicitud {cv['solicitud']}): cambió la línea de "
                        "solicitud, el contenido o el orden (solo se admiten: " + "; ".join(TRANSFORMACIONES_INOCUAS) + ")")
        elif cv.get("auditoria_sha256") and cv["auditoria_sha256"] != sha_archivo(p):
            # (4.8.1, Y-g) cierre anterior a la 4.8.1: la auditoría que lo aprobó es la registrada en cierre_vigente.json (bytes exactos;
            # 4.9: sin huella fiel registrada no se acredita ninguna otra forma del archivo)
            return "auditoria.md no es la auditoría registrada en cierre_vigente.json al cerrar (cierre anterior a la 4.8.1)"
        elif not cv.get("auditoria_sha256"):
            # (4.9, Z-1 de la auditoría interna) ni estado_pipeline.json (auditoria_respuesta) ni cierre_vigente.json registran qué
            # auditoria.md se aprobó: antes se aceptaba cualquier APROBADO que nombrara el material y registrar_cierre le atribuía la
            # huella del archivo actual. No se atribuye una aprobación sin respaldo (encargo 4.9 §3.3): hace falta una auditoría nueva.
            return ("no consta la respuesta de auditoría aprobada (ni estado_pipeline.json → auditoria_respuesta ni cierre_vigente.json la registran): "
                    "no se atribuye la aprobación al auditoria.md actual; hace falta una auditoría nueva (paso 13)")
    return motivo_auditoria_no_corresponde(carpeta, txt, empresa) or motivo_acreditacion_libro(carpeta) or motivo_f1(carpeta, st)


# ---------- 1d. acreditación del libro final (4.10, P-N2) ----------
# Hasta la 4.10, verificacion_integridad.txt se generaba ANTES de incorporar las cachés (verificar_todo.sh) y acreditaba un archivo
# distinto del entregado (el libro evaluado sin cachés; la verificación posterior nombraba el temporal con_cache.tmp.xlsx). Desde la
# 4.10, verificar_todo.sh termina escribiendo, después de TODAS las escrituras del libro, un comprobante EXTERNO al libro
# (acreditacion_libro.json, de acreditar_libro.py) que distingue libro de entrada, libro evaluado verificado antes de las cachés y
# archivo final (su SHA-256, sus bytes y su propia verificación, verificacion_libro_final.txt). El libro no lleva su propio hash. Una
# modificación posterior del libro, o una ficha que registra otro libro, invalidan la correspondencia: el cierre no se confirma y la
# vigencia lo retira (no se actualiza un cierre antiguo para conservar su aprobación). Un expediente sin comprobante (anterior a la
# 4.10) queda con el límite declarado de P-N2: no se le atribuye un comprobante nuevo.
ACREDITACION_LIBRO = "acreditacion_libro.json"
MATERIAL_FIJO.extend([ACREDITACION_LIBRO, "verificacion_libro_final.txt"])
# (4.14, requisito de verificación completa de las entradas) el registro de verificación de las entradas forma parte del material: cambiar una
# entrada, una fuente o una transformación invalida la aprobación (los expedientes que no lo tienen conservan su identificador de material)
MATERIAL_FIJO.append("verificacion_entradas.json")
# (4.15, hito 2, I20) la declaración del modo de la entrada efectiva forma parte del material auditado: cambiarla retira la aprobación
# (solo existe en los expedientes que prepara cambiar_base.py desde la 4.15; los anteriores no cambian de material)
MATERIAL_FIJO.append("entrada_efectiva.json")
# (4.15, F1-IMPL; revisión H6) la declaración F1 del motor A y su evaluación forman parte del material auditado: cambiarlas después del cierre
# retira la aprobación (solo existen en los expedientes con F1; los demás conservan su identificador de material)
MATERIAL_FIJO.extend(["motor_a_f1.json", "motor_a_f1_resultado.json"])


def motivo_f1(carpeta, st=None):
    """(4.15, F1-IMPL; revisión H1) Con el motor A y F1 exigido, el cierre oficial de un estado que no sea pendiente_de_datos exige una
    evaluación F1 vigente (declaración y libro evaluado actuales) y utilizable: un bloqueo F1 nunca da una ficha oficial concluido,
    con decisión ni con objetivo. None si no hay objeción."""
    import motor_a_f1 as F1
    st = st if isinstance(st, dict) else {}
    v = F1.vigencia(carpeta, motor=st.get("motor"))
    if not v.get("exigido") or (v.get("vigente") and v.get("utilizable")):
        return None
    estado = st.get("estado_pendiente") or st.get("estado_analisis_fase_c") or st.get("estado_analisis")
    if estado == "pendiente_de_datos":
        return None
    return (f"motor A · F1: {v.get('motivo')}; sin una evaluación F1 vigente y utilizable no se confirma un cierre «{estado}» "
            "(ver motor_a_f1_resultado.md)")


def motivo_acreditacion_libro(carpeta):
    """None si no hay comprobante (expediente anterior a la 4.10) o si el libro final, la ficha oficial y la provisional corresponden
    a él; si no, el motivo."""
    ac, err = leer_json_control(os.path.join(carpeta, ACREDITACION_LIBRO))
    if err:
        return f"{err}: no se puede acreditar qué libro se verificó; la aprobación no vale"
    if ac is None:
        return None
    fin = ac.get("archivo_final") if isinstance(ac.get("archivo_final"), dict) else {}
    nombre, h = fin.get("archivo"), fin.get("sha256")
    if not (isinstance(nombre, str) and nombre == os.path.basename(nombre) and nombre.endswith("_v63_evaluada.xlsx") and isinstance(h, str)):
        # (revisión interna R-3) el comprobante tiene que nombrar el libro EVALUADO del expediente, no cualquier .xlsx
        return f"{ACREDITACION_LIBRO} no identifica el libro evaluado final (archivo «…_v63_evaluada.xlsx» y SHA-256): la aprobación no vale"
    if not str(fin.get("veredicto") or "").startswith("ÍNTEGRO"):
        # (revisión interna R-3) un comprobante cuya verificación final no es ÍNTEGRO no acredita nada, aunque la huella coincida
        return f"{ACREDITACION_LIBRO}: la verificación final del libro no es ÍNTEGRO ({fin.get('veredicto')!r}): la aprobación no vale"
    p = os.path.join(carpeta, nombre)
    if not os.path.isfile(p):
        return f"falta el libro acreditado {nombre}: la aprobación no vale"
    actual = _sha(p)
    if actual != h:
        return (f"{nombre} no es el libro acreditado en {ACREDITACION_LIBRO} (SHA-256 {actual[:12]}… frente a {h[:12]}…): el libro cambió después "
                "de su verificación final; la aprobación no vale para otro archivo")
    for fic in ("ficha.json", "ficha_provisional.json"):
        F = _j_tolerante(os.path.join(carpeta, fic))
        reg = ((F or {}).get("hashes") or {}).get("libro_evaluado") if isinstance(F, dict) else None
        if reg is not None and reg != h:
            return f"{fic} registra otro libro evaluado ({str(reg)[:12]}…) que el acreditado ({h[:12]}…): la correspondencia no se puede acreditar"
    return None


# ---------- 2. marca de datos de etapa 1 ----------
def marca_etapa1(entrada):
    """{"marca", "causas"} si faltan datos necesarios para LISTO · PROVISIONAL (y solo entonces); si no, None."""
    nec = (entrada or {}).get("necesarios_para_listo_provisional") or []
    if not nec:
        return None
    return {"marca": MARCA_ETAPA1, "causas": [dict(x) for x in nec],
            "nota": "Limitación visible; no sustituye la revisión de materialidad (S-19): un dato material mantiene pendiente_de_datos."}


# ---------- 3. correspondencia D10 ↔ C104 ----------
# (estado, acción) → resultado de fundamento_material admitido → etiqueta visible de C104 («fundamento <etiqueta>»).
# `no_procede` solo en los casos que D10 ya admite: conclusión no favorable concluida, o pendiente_de_datos por S-19.
FUNDAMENTO_C104 = {
    ("concluido", "comprar"): {"sin_limitacion": "lista vacía", "comprobacion_conjunta_superada": "comprobación conjunta superada"},
    ("concluido", "esperar"): {"no_procede": "no procede (conclusión no favorable)"},
    ("concluido", "descartar"): {"no_procede": "no procede (conclusión no favorable)"},
    ("concluido", "demasiado_dificil"): {"no_procede": "no procede (conclusión no favorable)"},
    ("pendiente_de_investigacion", None): {"pendiente_de_investigacion": "pendiente de investigación"},
    ("pendiente_de_datos", None): {"no_procede": "pendiente de datos"},
}
ETIQUETAS_C104 = sorted({e for d in FUNDAMENTO_C104.values() for e in d.values()}, key=len, reverse=True)


def etiqueta_fundamento(estado, accion, resultado):
    """(etiqueta, None) si la combinación es admitida; (None, motivo) si es contradictoria o desconocida."""
    fila = FUNDAMENTO_C104.get((estado, accion))
    if fila is None:
        return None, f"combinación estado {estado!r} · acción {accion!r} no admitida en el cierre"
    if resultado not in fila:
        return None, f"fundamento_material.resultado {resultado!r} no corresponde a estado {estado!r} · acción {accion!r} (admitidos: {', '.join(fila)})"
    return fila[resultado], None


def etiqueta_en_c104(c104):
    """La etiqueta que sigue a «fundamento » en C104 si es una de las conocidas; «?» si hay otra cosa; None si no hay."""
    m = re.search(r"·\s*fundamento\s+(.+?)\s*(?:·|$)", c104 or "")
    if not m:
        return None
    t = m.group(1).strip()
    for e in ETIQUETAS_C104:
        if t == e or t.startswith(e + " "):
            return e
    return "?"


def motivo_c104_fundamento(estado, accion, resultado, c104):
    esperada, motivo = etiqueta_fundamento(estado, accion, resultado)
    if motivo:
        return motivo
    vista = etiqueta_en_c104(c104)
    if vista is None:
        return f"C104 no lleva «fundamento {esperada}»"
    if vista == "?":
        return f"C104 lleva una etiqueta de fundamento desconocida (admitida aquí: «fundamento {esperada}»)"
    if vista != esperada:
        return f"C104 dice «fundamento {vista}» pero el JSON ({resultado}, {estado}, {accion}) exige «fundamento {esperada}»"
    return None


# ---------- 4. alcance declarado ----------
def alcance(carpeta):
    """Metadato explícito del expediente (alcance_v2.json). None si no existe; ValueError si está mal formado."""
    p = os.path.join(carpeta, "alcance_v2.json")
    if not os.path.exists(p):
        return None
    a = json.load(open(p, encoding="utf-8"))
    if a.get("tipo") not in ("ensayo_exploratorio",) or not str(a.get("aviso") or "").strip() or not str(a.get("fuente") or "").strip():
        raise ValueError("alcance_v2.json mal formado: hace falta tipo = ensayo_exploratorio, aviso y fuente no vacíos")
    return a


def linea_alcance(a):
    return f"> **Alcance del expediente ({a['tipo'].replace('_', ' ')}):** {a['aviso'].strip()}" if a else None


# ---------- 5. vigencia de las salidas oficiales (reparación 4.6.1) ----------
# Una salida oficial cerrada por una auditoría (ficha.json con «cierre», o con estado concluido) solo es VIGENTE si la aprobación
# sigue siendo válida para el material actual y la ficha (y el informe, si existe) son los registrados en cierre_vigente.json al
# cerrar. Si no, se ARCHIVA en historial_cierres/<n>_<material>/ con RETIRADA.json (qué aprobación era, de qué material, por qué
# se retira), la fila del resumen activo pasa a «SIN APROBACIÓN VIGENTE» y la fila anterior se conserva en resumen_v2_historial.csv,
# y el estado del pipeline deja de decir «concluido». La auditoría que la aprobó no se borra ni cambia: era la aprobación de otro
# material. Los estados tempranos sin auditoría (ficha sin «cierre» y estado ≠ concluido) no se tocan.
CIERRE_VIGENTE = "cierre_vigente.json"
SALIDAS_OFICIALES = ("ficha.json", "informe.md", CIERRE_VIGENTE)
# (hoja resumen, ronda 1 de su revisión crítica; decisión del coordinador) la hoja resumen en lenguaje llano (hoja_resumen.py) es material
# de estudio, no una salida oficial, pero resume un cierre concreto: cuando se retira la aprobación de ese cierre, o se relanza el pipeline,
# deja de valer y se archiva como NO VIGENTE junto al antecedente. Nunca se reactiva: una hoja nueva exige un cierre vigente nuevo.
HOJA_RESUMEN = ("hoja_resumen.md", "hoja_resumen.json")
NO_VIGENTE = "SIN APROBACIÓN VIGENTE"


def _j(p):
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else None


def _j_tolerante(p):
    """Como _j, pero un archivo ilegible devuelve None (4.9, Z-2: archivar y retirar no deben interrumpirse por un archivo de control
    ilegible; el motivo lo da motivo_rechazo_cierre)."""
    return leer_json_control(p)[0]


RESUMEN_V64 = "resumen_v2_v64_experimental.csv"
RESUMEN_V641 = "resumen_v2_v641_experimental.csv"
RESUMEN_V631 = "resumen_v2_v631_f1.csv"   # (4.15, F1-IMPL) V6.3.1 F1


def nombre_resumen(carpeta, cfg=None):
    """(4.11, revisión interna H2) Nombre del resumen junto al expediente: el que fije la configuración (resumen_csv_nombre); si no fija
    ninguno, el de la V6.4 experimental para un expediente que la tiene registrada en plantilla_activa.json (también en una llamada
    a mano sin MUNGER_CONFIG, O5) y resumen_v2.csv para los demás. Una fila V6.4 nunca comparte archivo con las filas V6.3."""
    nombre = os.path.basename((cfg or {}).get("resumen_csv_nombre") or "")
    if nombre:
        return nombre
    try:
        v = (json.load(open(os.path.join(carpeta, "plantilla_activa.json"), encoding="utf-8")) or {}).get("version")
    except (OSError, ValueError, AttributeError):
        v = None
    # (4.13 §7) la V6.4.1 tiene su propio resumen: sus filas no se mezclan con las de la V6.4 ni con las de la V6.3
    return (RESUMEN_V64 if v == "V6.4 experimental" else RESUMEN_V641 if v == "V6.4.1 experimental" else RESUMEN_V631 if v == "V6.3.1 F1"
            else "resumen_v2.csv")


def ruta_resumen(carpeta, cfg=None):
    return (cfg or {}).get("resumen_csv") or os.path.join(os.path.dirname(os.path.abspath(carpeta)), nombre_resumen(carpeta, cfg))


def ruta_historial(csv_path):
    """Historial de las filas retiradas de un resumen. resumen_v2_historial.csv junto al resumen (como hasta la 4.10.1), salvo para un
    resumen con nombre propio «resumen_v2_<x>.csv» (4.11, H2: el de la V6.4 experimental), cuyo historial es «resumen_v2_<x>_historial.csv»."""
    base = os.path.basename(csv_path)
    propio = base.startswith("resumen_v2_") and base.endswith(".csv") and not base.endswith("_historial.csv")
    return os.path.join(os.path.dirname(csv_path), base[:-4] + "_historial.csv" if propio else "resumen_v2_historial.csv")


def ficha_cerrada(F):
    """¿La ficha oficial dice que hubo un cierre con auditoría (o que está concluida)? Entonces exige vigencia."""
    return bool(F) and (bool(F.get("cierre")) or F.get("estado_analisis") == "concluido")


def cierre_registrado(carpeta):
    """(4.10, §3.3) ¿Hay un cierre registrado (cierre_vigente.json, legible o no)? Entonces la ficha oficial exige vigencia aunque
    haya perdido sus marcadores de cierre."""
    return os.path.lexists(os.path.join(carpeta, CIERRE_VIGENTE))


def aprobacion_sin_ficha_cerrada(carpeta, F, st=None):
    """(4.10, revisión interna R-1) ¿Hay una ficha oficial (ficha.json existe) que no está cerrada mientras el estado del pipeline
    registra una auditoría APROBADO en un estado de cierre? Es una aprobación sin salida cerrada que la respalde."""
    if not os.path.isfile(os.path.join(carpeta, "ficha.json")) or ficha_cerrada(F):
        return False
    if st is None:
        st = _j_tolerante(os.path.join(carpeta, "estado_pipeline.json"))
    if not (isinstance(st, dict) and st.get("auditoria") == "APROBADO"
            and st.get("estado_analisis") in ("concluido", "pendiente_de_investigacion", "pendiente_de_datos")):
        return False
    # Solo con una publicación VIVA registrada de un cierre (el rastro que deja un cierre publicado cuyos registros se borraron): en el
    # cierre legítimo del paso 14, entre la aprobación y la ficha cerrada, el estado ya dice APROBADO y puede quedar una ficha oficial
    # anterior sin cerrar, pero las publicaciones anteriores ya se retiraron al pedir la auditoría (Y-h)
    reg = _j_tolerante(os.path.join(carpeta, REGISTRO_RESUMEN)) or _j_tolerante(os.path.join(carpeta, RESPALDO_RESUMEN))
    pubs = (reg or {}).get("publicaciones") if isinstance(reg, dict) else None
    return isinstance(pubs, list) and any(isinstance(e, dict) and e.get("estado") == "publicada" for e in pubs)


def senal_publicacion(carpeta, st, F=None):
    """(4.13.1, H5; revisión interna D1-1, D1-4, D1-8) Señal de que la aprobación REGISTRADA en el estado (su solicitud y su respuesta
    aceptada) se publicó, o None. La señal es propia de esa aprobación, nunca el nombre de una empresa en un CSV (D1-1):
      - «registro»: una entrada «publicada» en el registro de publicaciones (o, si falta o es ilegible, en su respaldo), o una entrada con
        la identidad de esta aprobación en cualquier estado (las publicaciones desde la 4.13.1 la llevan; la sincronización no la borra);
      - «estado»: el propio estado del pipeline registra el FIN del paso 14 después de consumir la respuesta a esta solicitud (también en
        los cierres anteriores a la 4.13.1) o una publicación de esta aprobación (publicaciones_de_la_aprobacion).
    Un registro ilegible no es una señal (D1-4): no permite acreditar nada, así que no retira una aprobación del intervalo legítimo; la
    retirada pendiente que deja ese registro (código 5) ya impide cerrar y publicar hasta restaurarlo."""
    ident = identidad_aprobacion(st, None, carpeta)
    for p in (os.path.join(carpeta, REGISTRO_RESUMEN), os.path.join(carpeta, RESPALDO_RESUMEN)):
        reg, err = leer_json_control(p)
        pubs = reg.get("publicaciones") if isinstance(reg, dict) else None
        if err or not isinstance(pubs, list):
            continue
        for e in pubs:
            if not isinstance(e, dict):
                continue
            if e.get("estado") == "publicada":
                return f"el registro de publicaciones ({os.path.basename(p)}) conserva una publicación «publicada» en {os.path.basename(str(e.get('csv') or ''))}"
            if ident and (e.get("solicitud"), e.get("auditoria_fiel")) == tuple(ident):
                return f"el registro de publicaciones ({os.path.basename(p)}) registra una publicación de esta aprobación (solicitud {ident[0]})"
        break  # el primer registro legible manda (el respaldo solo sustituye a un registro ausente o ilegible)
    if ident and any(isinstance(x, dict) and (x.get("solicitud"), x.get("auditoria_fiel")) == tuple(ident) for x in st.get("publicaciones_de_la_aprobacion") or []):
        return f"estado_pipeline.json registra una publicación de esta aprobación (solicitud {ident[0]})"
    if ident and _fin_del_paso_14_tras(st, ident[0]):
        return f"estado_pipeline.json registra el FIN del paso 14 después de consumir la respuesta a la solicitud {ident[0]}"
    if ident and ident[0] == "legado-sha256" and any(isinstance(h, str) and FIN_CIERRE.search(h) for h in st.get("historial") or []):
        # (D1-5) cierre anterior a la 4.8.1 (sin solicitud): el estado registra el FIN del paso 14 con esa aprobación
        return "estado_pipeline.json registra el FIN del paso 14 de un cierre anterior a la 4.8.1 (sin solicitud de auditoría)"
    return None


FIN_CIERRE = re.compile(r"paso 14 · FIN · estado (concluido|pendiente_de_investigacion|pendiente_de_datos) · auditoría APROBADO")


def _fin_del_paso_14_tras(st, solicitud):
    """(revisión interna D2-3) solo un FIN del paso 14 que CIERRA (estado de cierre con auditoría APROBADO), no el de un no_entregable."""
    hist = [h for h in (st.get("historial") or []) if isinstance(h, str)]
    pos = [i for i, h in enumerate(hist) if f"respuesta a la solicitud {solicitud}" in h]
    return bool(pos) and any(FIN_CIERRE.search(h) for h in hist[pos[-1] + 1:])


def destinos_publicados_en_el_estado(st):
    """(4.13.1, H5) Destinos donde el estado del pipeline registra que el paso 14 publicó la fila («OK: fila de <empresa> en <ruta>»)
    después de consumir la respuesta aprobada: [(ruta, empresa)]. Se usa solo sin registro de publicaciones legible."""
    ident = identidad_aprobacion(st)
    hist = [h for h in (st.get("historial") or []) if isinstance(h, str)] if isinstance(st, dict) else []
    pos = [i for i, h in enumerate(hist) if ident and f"respuesta a la solicitud {ident[0]}" in h]
    if not ident and isinstance(st, dict) and not st.get("auditoria_respuesta"):
        pos = [-1]  # (D1-5) cierre anterior a la 4.8.1: todas las publicaciones que registra el historial
    out = []
    # (revisión interna D2-1, D2-4) primero el registro estructurado que deja resumen.py en el estado (destino completo, sin truncar)
    for x in (st.get("publicaciones_de_la_aprobacion") or []) if isinstance(st, dict) else []:
        if isinstance(x, dict) and ident and (x.get("solicitud"), x.get("auditoria_fiel")) == tuple(ident) and x.get("csv") and (x["csv"], x.get("empresa")) not in out:
            out.append((x["csv"], x.get("empresa")))
    for h in hist[pos[-1] + 1:] if pos else []:
        # la línea de la orden («$ python3 resumen.py <expediente> <destino> → 0 …», con el destino tal como se pasó) y la del resultado
        # («OK: fila de <empresa> en <ruta>»); el historial trunca las líneas largas, así que se usan las dos
        m = re.search(r"OK: fila de (.+?) en (\S+\.csv)", h)
        m2 = re.search(r"\$ \S*python3?\S* resumen\.py \S+ (.+?\.csv) → 0", h)
        emp = m.group(1) if m else (re.search(r"OK: fila de (.+?) en ", h).group(1) if re.search(r"OK: fila de (.+?) en ", h) else None)
        for ruta in ([m.group(2)] if m else []) + ([m2.group(1)] if m2 else []):
            if not any(os.path.basename(r) == os.path.basename(ruta) for r, _ in out):
                out.append((ruta, emp))
    return out


def aprobacion_publicada_sin_respaldo(carpeta, F=None, st=None):
    """(4.13.1, H5) Motivo si el estado del pipeline registra una auditoría APROBADO en un estado de cierre cuya publicación consta
    (senal_publicacion) y no queda ninguna salida que la respalde: ni ficha oficial cerrada (falte o exista sin cerrar) ni cierre registrado
    (cierre_vigente.json); None si no. Hasta la 4.13 solo se detectaba con una ficha oficial presente sin cerrar (aprobacion_sin_ficha_cerrada);
    sin ficha y sin registro del cierre, la aprobación interna seguía vigente (H5).
    Intervalo legítimo entre la aceptación de la auditoría (paso 13) y la publicación del paso 14: al pedir la auditoría, las publicaciones del
    cierre anterior se retiraron (Y-h: «retirada» o «retirada_pendiente»), la aprobación nueva es de otra solicitud y el paso 14 todavía no
    ha registrado su FIN: ninguna señal de publicación de ESTA aprobación. La distinción se hace con la solicitud, la respuesta y los rastros
    de publicación, nunca con fechas de archivos."""
    if ficha_cerrada(F) or cierre_registrado(carpeta):
        return None
    if st is None:
        st = _j_tolerante(os.path.join(carpeta, "estado_pipeline.json"))
    if not (isinstance(st, dict) and st.get("auditoria") == "APROBADO"
            and st.get("estado_analisis") in ("concluido", "pendiente_de_investigacion", "pendiente_de_datos")):
        return None
    return senal_publicacion(carpeta, st, F)


def _empresas_del_expediente(carpeta):
    """Nombre de la empresa en los archivos de entrada del expediente (nunca el nombre de la carpeta)."""
    nombres = set()
    for n in ("fase1_v63.json", "fase_a.json"):
        d = _j_tolerante(os.path.join(carpeta, n))
        if isinstance(d, dict) and isinstance(d.get("empresa"), str) and d["empresa"].strip():
            nombres.add(d["empresa"])
    return nombres


APROBACIONES_RETIRADAS = "aprobaciones_retiradas.json"


def identidad_aprobacion(st, cv=None, carpeta=None):
    """(4.13.1, H5) (solicitud, huella fiel) de la respuesta de auditoría que respalda la aprobación registrada; None si no consta."""
    resp = (st or {}).get("auditoria_respuesta") if isinstance(st, dict) else None
    if isinstance(resp, dict) and resp.get("solicitud") and resp.get("fiel"):
        return resp["solicitud"], resp["fiel"]
    if isinstance(cv, dict) and cv.get("solicitud") and cv.get("auditoria_fiel"):
        return cv["solicitud"], cv["auditoria_fiel"]
    if isinstance(cv, dict) and cv.get("auditoria_sha256") and not (isinstance(resp, dict) and resp):
        # (revisión interna D1-5) cierre anterior a la 4.8.1, sin solicitud ni huella fiel: lo identifica la huella de bytes de la auditoría
        # registrada en cierre_vigente.json (la misma que exige motivo_rechazo_cierre, Y-g)
        return "legado-sha256", cv["auditoria_sha256"]
    if carpeta and isinstance(st, dict) and st.get("auditoria") == "APROBADO" and not (isinstance(resp, dict) and resp):
        # (D1-5) cierre anterior a la 4.8.1 cuyo cierre_vigente.json falta: la auditoría aprobada es la de auditoria.md (sus bytes; la retirada
        # no la mueve ni la cambia), la misma huella que cierre_vigente.json registraría
        aud = os.path.join(carpeta, "auditoria.md")
        if os.path.isfile(aud):
            return "legado-sha256", _sha(aud)
    return None


def anotar_aprobacion_retirada(carpeta, ident, material_id, motivo, antecedente):
    """(4.13.1, H5) Registro que solo crece (aprobaciones_retiradas.json, fuera de las salidas oficiales y del estado del pipeline): una
    aprobación quitada del estado por una retirada no vuelve a acreditar ningún cierre, aunque se restauren archivos antiguos (también el
    estado). Hace falta una auditoría nueva (otra solicitud). Un registro ilegible no se sobrescribe: el cierre se rechaza (lado seguro)."""
    p = os.path.join(carpeta, APROBACIONES_RETIRADAS)
    d, err = leer_json_control(p)
    if err:
        return f"{APROBACIONES_RETIRADAS} no se puede leer ({err}): no se sobrescribe"
    d = d if isinstance(d, dict) else {}
    lista = d.get("retiradas") if isinstance(d.get("retiradas"), list) else []
    if not any(isinstance(e, dict) and (e.get("solicitud"), e.get("auditoria_fiel")) == tuple(ident) for e in lista):
        import datetime as _dt
        lista.append({"solicitud": ident[0], "auditoria_fiel": ident[1], "material_auditado": material_id,
                      "fecha": _dt.datetime.now().isoformat(timespec="seconds"), "motivo": str(motivo)[:300], "antecedente": antecedente})
    tmp = p + ".tmp"
    json.dump({"nota": "aprobaciones retiradas de este expediente (4.13.1, H5): ninguna vuelve a acreditar un cierre; solo se añaden entradas",
               "retiradas": lista}, open(tmp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    os.replace(tmp, p)
    return None


def motivo_aprobacion_retirada(carpeta, st, cv=None):
    """(4.13.1, H5) Motivo si la aprobación registrada (su solicitud y su respuesta) ya se retiró: consta en aprobaciones_retiradas.json o en
    el antecedente de una retirada (historial_cierres/*/RETIRADA.json). Dos señales independientes: no depende solo de una carpeta archivada."""
    ident = identidad_aprobacion(st, cv, carpeta)
    if not ident:
        return None
    d, err = leer_json_control(os.path.join(carpeta, APROBACIONES_RETIRADAS))
    # (revisión interna D1-6) un registro ilegible no retira por sí solo un cierre sano: se ignora esa fuente (no se sobrescribe) y deciden
    # las otras dos señales, que son independientes
    vistas = [e for e in ((d or {}).get("retiradas") or []) if isinstance(e, dict)] if not err else []
    # (D1-3) tercera señal: las entradas del registro de publicaciones (y del respaldo) que publicaron ESTA aprobación y que retiró una
    # RETIRADA DE LA APROBACIÓN (archivar_salidas las marca con retirada_de_la_aprobacion). (Revisión interna D2-2) una retirada de filas de
    # la sincronización, sin retirada de la aprobación, no cuenta: con el cierre vigente no es una retirada de esa aprobación
    for n in (REGISTRO_RESUMEN, RESPALDO_RESUMEN):
        reg = _j_tolerante(os.path.join(carpeta, n))
        for e in ((reg or {}).get("publicaciones") or []) if isinstance(reg, dict) else []:
            if isinstance(e, dict) and e.get("estado") in ("retirada", "retirada_pendiente") and e.get("solicitud") and e.get("retirada_de_la_aprobacion"):
                vistas.append({"solicitud": e.get("solicitud"), "auditoria_fiel": e.get("auditoria_fiel"), "fecha": e.get("fecha_retirada") or e.get("fecha"),
                               "antecedente": f"{n} ({os.path.basename(str(e.get('csv') or ''))})"})
    for r in sorted(glob.glob(os.path.join(carpeta, "historial_cierres", "*", "RETIRADA.json"))):
        x = _j_tolerante(r)
        a = (x or {}).get("aprobacion_retirada") if isinstance(x, dict) else None
        if isinstance(a, dict):
            vistas.append(dict(a, antecedente=os.path.relpath(os.path.dirname(r), carpeta)))
    for e in vistas:
        if (e.get("solicitud"), e.get("auditoria_fiel")) == tuple(ident):
            quien = (f"la aprobación del cierre anterior a la 4.8.1 (auditoría {ident[1][:12]}…)" if ident[0] == "legado-sha256"
                     else f"la aprobación de la solicitud {ident[0]}")
            return (f"{quien} ya se retiró ({e.get('fecha') or 'fecha no registrada'}; antecedente "
                    f"{e.get('antecedente') or '—'}): restaurar archivos antiguos no la reactiva; hace falta una auditoría nueva (paso 13)")
    return None


def instantanea_rastro(carpeta, destino):
    """(4.13.1, H5) Copia, antes de tocarlos, el estado del pipeline y el registro de publicaciones (y su respaldo) en
    <destino>/rastro_previo/: el rastro de la aprobación retirada no depende de que quede ninguna salida oficial que archivar."""
    import shutil
    d = os.path.join(destino, "rastro_previo")
    copiados = []
    for n in ("estado_pipeline.json", REGISTRO_RESUMEN, RESPALDO_RESUMEN):
        p = os.path.join(carpeta, n)
        if os.path.isfile(p):
            try:
                os.makedirs(d, exist_ok=True)
                shutil.copy2(p, os.path.join(d, n.lstrip(".")))
                copiados.append(n)
            except OSError:
                pass
    return copiados


def registrar_cierre(carpeta):
    """Lo llama ficha.py al escribir una ficha oficial cerrada con una aprobación válida."""
    F = _j(os.path.join(carpeta, "ficha.json")) or {}
    aud = os.path.join(carpeta, "auditoria.md")
    previo = _j_tolerante(os.path.join(carpeta, CIERRE_VIGENTE)) or {}
    reg = {"material_auditado": (F.get("cierre") or {}).get("material_auditado"), "estado_analisis": F.get("estado_analisis"),
           "ficha_sha256": _sha(os.path.join(carpeta, "ficha.json")), "informe_sha256": None,
           "auditoria_sha256": _sha(aud) if os.path.exists(aud) else None,
           "nota": "salidas oficiales vigentes de este material; si cambia el material o la aprobación, se archivan"}
    resp = (_j(os.path.join(carpeta, "estado_pipeline.json")) or {}).get("auditoria_respuesta") or {}
    if resp.get("fiel") and os.path.exists(aud) and huella_fiel(open(aud, "rb").read()) == resp["fiel"]:
        # (4.9, R-V1) la respuesta aceptada que respalda este cierre: solicitud y huella fiel registradas al aceptarla en el paso 13
        # (nunca se calculan aquí para una respuesta que no las tenía)
        reg.update(solicitud=resp.get("solicitud"), auditoria_fiel=resp["fiel"])
    elif not resp and previo.get("auditoria_fiel") and previo.get("solicitud") and os.path.exists(aud) and huella_fiel(open(aud, "rb").read()) == previo["auditoria_fiel"]:
        # (4.9, control de vigencia V-3) sin estado del pipeline, el cierre ya registrado en cierre_vigente.json conserva su respuesta:
        # la solicitud, la huella fiel y la huella de bytes de la respuesta aceptada (no la del archivo actual, que puede diferir
        # en una transformación inocua)
        reg.update(solicitud=previo["solicitud"], auditoria_fiel=previo["auditoria_fiel"], auditoria_sha256=previo.get("auditoria_sha256") or reg["auditoria_sha256"])
    json.dump(reg, open(os.path.join(carpeta, CIERRE_VIGENTE), "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def registrar_informe(carpeta):
    cv = _j(os.path.join(carpeta, CIERRE_VIGENTE))
    if cv is not None:
        cv["informe_sha256"] = _sha(os.path.join(carpeta, "informe.md"))
        json.dump(cv, open(os.path.join(carpeta, CIERRE_VIGENTE), "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def motivo_vigencia(carpeta, veredicto, empresa=None, comprobar_informe=True):
    """None si no hay salida oficial cerrada o si es vigente; si no, el motivo por el que no lo es.
    (4.13 §3) Guarda que no depende de interpretar bien un archivo alterado: si la comprobación misma falla por una estructura
    inesperada (AttributeError, TypeError, KeyError…), la aprobación no se puede acreditar y se retira (lado seguro), con el motivo."""
    try:
        return _motivo_vigencia(carpeta, veredicto, empresa, comprobar_informe)
    except (AttributeError, TypeError, KeyError, IndexError, ValueError) as e:
        return (f"la vigencia no se puede comprobar: un archivo de entrada o de control tiene una estructura inesperada ({type(e).__name__}: "
                f"{str(e)[:120]}); la aprobación no se puede acreditar y se retira (hace falta corregir el archivo y una auditoría nueva)")


def _motivo_vigencia(carpeta, veredicto, empresa=None, comprobar_informe=True):
    F, err_f = leer_ficha_control(os.path.join(carpeta, "ficha.json"))
    if err_f:
        # (4.9, control de vigencia V-1) una ficha oficial ilegible no puede acreditarse como la registrada: se retira (antes se
        # tomaba por «sin salida cerrada» y las vías se interrumpían después con la aprobación publicada)
        return f"{err_f}: la salida oficial no se puede acreditar como la registrada al cerrar; se retira"
    if not ficha_cerrada(F):
        if not cierre_registrado(carpeta):
            if aprobacion_sin_ficha_cerrada(carpeta, F):
                # (4.10, revisión interna R-1) además de los marcadores se borró cierre_vigente.json: no queda ningún cierre registrado,
                # pero el estado del pipeline sigue registrando una aprobación de una ficha que ya no está cerrada
                return ("la ficha oficial no está cerrada (sin «cierre» ni estado concluido) y no hay cierre registrado, pero estado_pipeline.json "
                        "registra una auditoría APROBADO: ninguna salida cerrada la respalda; la aprobación se retira (hace falta una auditoría nueva)")
            senal = aprobacion_publicada_sin_respaldo(carpeta, F)
            if senal:
                # (4.13.1, H5) sin ficha oficial cerrada (falta o está sin cerrar) ni cierre registrado, el estado sigue registrando una
                # aprobación cuya publicación consta: la aprobación publicada perdió su respaldo y se retira en la primera llamada.
                # (D1-8) el motivo dice qué señal de publicación se encontró
                return (("no hay ficha.json oficial" if not os.path.isfile(os.path.join(carpeta, "ficha.json")) else "la ficha oficial no está cerrada")
                        + f" ni cierre registrado ({CIERRE_VIGENTE}), pero estado_pipeline.json registra una auditoría APROBADO publicada ({senal}): "
                        "ninguna salida respalda la aprobación publicada; se retira (restaurar archivos antiguos no la reactiva: hace falta una auditoría nueva)")
            return None  # estado temprano legítimo, sin cierre previo registrado
        # (4.10, encargo §3.3; caso externo, heredado de la 4.8.1) la ficha oficial perdió sus marcadores de cierre («cierre» y
        # estado concluido; o es {} o falta), pero hay un cierre registrado: su correspondencia se comprueba con independencia de
        # los marcadores actuales. Hasta la 4.10 se tomaba por «sin salida cerrada» y las vías no retiraban nada: informe.py podía
        # dejar la fila concluido/APROBADO y resumen.py publicar pendiente_de_datos/APROBADO/esperar (o, con {}, una fila sin empresa)
        cv, err_cv = leer_json_control(os.path.join(carpeta, CIERRE_VIGENTE))
        if err_cv:
            return f"{err_cv}: no consta qué salida oficial se registró al cerrar; la aprobación se retira"
        p_f = os.path.join(carpeta, "ficha.json")
        if not os.path.isfile(p_f) or _sha(p_f) != (cv or {}).get("ficha_sha256"):
            return ("ficha.json no es la ficha registrada al cerrar: " + ("falta" if not os.path.isfile(p_f) else "perdió sus marcadores de cierre («cierre» o el estado concluido)")
                    + f" y {CIERRE_VIGENTE} registra otra; la aprobación se retira (restaurar o regenerar la ficha no la reactiva: hace falta una auditoría nueva)")
    m = motivo_rechazo_cierre(carpeta, veredicto, None, empresa)
    if m:
        return m
    cv = _j_tolerante(os.path.join(carpeta, CIERRE_VIGENTE))
    if not cv:
        return f"no hay {CIERRE_VIGENTE}: la ficha oficial no está ligada a ninguna aprobación registrada"
    fij = (material_fijado(carpeta) or {}).get("id")
    if cv.get("material_auditado") != fij or (F.get("cierre") or {}).get("material_auditado") != fij:
        return f"la ficha oficial pertenece a la aprobación del material {(F.get('cierre') or {}).get('material_auditado')}, no al material aprobado vigente {fij}"
    if _sha(os.path.join(carpeta, "ficha.json")) != cv.get("ficha_sha256"):
        return "ficha.json no es la ficha registrada al cerrar (cambió después del cierre)"
    inf = os.path.join(carpeta, "informe.md")
    if comprobar_informe and cv.get("informe_sha256") and os.path.exists(inf) and _sha(inf) != cv["informe_sha256"]:
        return "informe.md no es el informe registrado al cerrar (cambió después del cierre)"
    return None


def _retirar_fila(csv_path, empresa, material, motivo):
    import csv
    if not csv_path or not os.path.exists(csv_path):
        return False
    with open(csv_path, encoding="utf-8", newline="") as fh:
        rd = csv.DictReader(fh)
        cols, filas = rd.fieldnames, list(rd)
    mias = [r for r in filas if r.get("empresa") == empresa]
    if not mias or all((r.get("verificacion") or "").startswith(NO_VIGENTE) for r in mias):
        return False
    hist = ruta_historial(csv_path)
    hcols = list(cols) + ["retirada_motivo", "material_auditado"]
    nuevo = not os.path.exists(hist)
    with open(hist, "a", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=hcols)
        if nuevo:
            w.writeheader()
        for r in mias:
            if not (r.get("verificacion") or "").startswith(NO_VIGENTE):
                w.writerow(dict(r, retirada_motivo=motivo[:300], material_auditado=material or ""))
    activa = {k: "" for k in cols}
    activa.update({"empresa": empresa, "fecha": mias[-1].get("fecha", ""),
                   "verificacion": f"{NO_VIGENTE} · cierre anterior (APROBADO del material {material or 'sin registrar'}) archivado en {os.path.basename(hist)}"})
    filas = [r for r in filas if r.get("empresa") != empresa] + [activa]
    with open(csv_path, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for r in filas:
            w.writerow({k: r.get(k, "") for k in cols})
    return True


def archivar_hoja_resumen(carpeta, destino, motivo):
    """(hoja resumen, ronda 1) Mueve la hoja resumen del expediente (si la hay) a destino como hoja_resumen.NO_VIGENTE.md/.json y deja
    en destino HOJA_RESUMEN_NO_VIGENTE.json con la fecha y el motivo. No toca ninguna salida oficial ni el estado. Devuelve los nombres
    archivados (lista vacía si no había hoja)."""
    import datetime as _dt
    import shutil
    movidos = []
    for n in HOJA_RESUMEN:
        p = os.path.join(carpeta, n)
        if os.path.isfile(p):
            os.makedirs(destino, exist_ok=True)
            raiz, ext = os.path.splitext(n)
            shutil.move(p, os.path.join(destino, f"{raiz}.NO_VIGENTE{ext}"))
            movidos.append(f"{raiz}.NO_VIGENTE{ext}")
    if movidos:
        json.dump({"archivada": _dt.datetime.now().isoformat(timespec="seconds"), "motivo": motivo, "archivos": movidos,
                   "nota": "hoja resumen (material de estudio, no oficial) del cierre que dejó de valer: NO VIGENTE; no se reactiva"},
                  open(os.path.join(destino, "HOJA_RESUMEN_NO_VIGENTE.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return movidos


def archivar_salidas(carpeta, motivo, csv_path=None, st=None):
    """Archiva las salidas oficiales presentes como antecedente (conservando el historial), retira la fila activa del resumen y
    deja el estado del pipeline sin cierre. Devuelve la carpeta del archivo o None si no había nada que archivar."""
    import datetime as _dt
    import shutil
    presentes = [f for f in SALIDAS_OFICIALES if os.path.exists(os.path.join(carpeta, f))]
    F, err_ficha = leer_ficha_control(os.path.join(carpeta, "ficha.json"))
    F = F or {}
    # (4.13.1, H5) sin ninguna salida oficial que archivar, una aprobación publicada sin respaldo también se retira: se deja el antecedente
    # (RETIRADA.json y el rastro previo), se retiran las publicaciones y se invalida el estado. Antes se devolvía None sin tocar nada
    sin_respaldo = aprobacion_publicada_sin_respaldo(carpeta, None if err_ficha else F, st)
    if not presentes and not sin_respaldo:
        return None
    # (4.9, V-1) una ficha ilegible se trata como la salida cerrada que era; (4.10, §3.3) también la que perdió sus marcadores
    # mientras hay un cierre registrado: se retiran el estado y la aprobación del pipeline y todas las publicaciones registradas
    cerrada = (ficha_cerrada(F) or bool(err_ficha) or cierre_registrado(carpeta) or aprobacion_sin_ficha_cerrada(carpeta, F, st)
               or sin_respaldo)
    cv = _j_tolerante(os.path.join(carpeta, CIERRE_VIGENTE)) or {}
    mat = (F.get("cierre") or {}).get("material_auditado") or cv.get("material_auditado")
    if not mat and sin_respaldo:
        mat = (material_fijado(carpeta) or {}).get("id")  # (4.13.1, H5) el material que aprobó la auditoría registrada
    base = os.path.join(carpeta, "historial_cierres")
    os.makedirs(base, exist_ok=True)
    n = 1 + len([x for x in os.listdir(base) if os.path.isdir(os.path.join(base, x))])
    # (segundo control de vigencia, W-4; anterior a la 4.9) el identificador se limpia: un «../» no saca el archivo del expediente
    destino = os.path.join(base, f"{n:02d}_" + re.sub(r"[^0-9A-Za-z_-]", "_", str(mat or "sin_material")))
    os.makedirs(destino)
    # (4.13.1, H5) el rastro previo (estado y registro de publicaciones tal como estaban) se conserva ANTES de sincronizar publicaciones
    # y de tocar el estado, haya o no salidas oficiales que mover
    rastro = instantanea_rastro(carpeta, destino)
    for f in presentes:
        shutil.move(os.path.join(carpeta, f), os.path.join(destino, f))
    try:  # (hoja resumen, ronda 1) la hoja resumen de este cierre se archiva como NO VIGENTE con el antecedente
        hoja_archivada = archivar_hoja_resumen(carpeta, destino, motivo)
    except OSError:
        hoja_archivada = []
    copiada = False
    if os.path.isfile(os.path.join(carpeta, "auditoria.md")):  # (4.9, V-2) una carpeta con ese nombre no se copia
        try:
            shutil.copy2(os.path.join(carpeta, "auditoria.md"), os.path.join(destino, "auditoria_en_el_momento_de_la_retirada.md"))
            copiada = True
        except OSError:
            pass  # (segundo control de vigencia, W-3) sin permiso de lectura: la retirada sigue; RETIRADA.json lo dice
    actual, _ = material(carpeta)
    estado_previo = F.get("estado_analisis")
    if not estado_previo and sin_respaldo:  # (4.13.1, H5) sin ficha: el estado que presentaba la aprobación retirada
        _s0 = st if isinstance(st, dict) else _j_tolerante(os.path.join(carpeta, "estado_pipeline.json"))
        estado_previo = (_s0 or {}).get("estado_analisis") if isinstance(_s0, dict) else None
    reg = {"retirada": _dt.datetime.now().isoformat(timespec="seconds"), "motivo": motivo, "material_auditado_en_la_aprobacion": mat,
           "material_actual": actual, "estado_que_presentaba": estado_previo, "archivos": presentes, "rastro_previo": [os.path.join("rastro_previo", x.lstrip(".")) for x in rastro],
           **({"hoja_resumen_no_vigente": hoja_archivada} if hoja_archivada else {}),
           **({"sin_salidas_oficiales": "no quedaba ninguna salida oficial que archivar: la aprobación publicada había perdido su respaldo "
               "(sin ficha oficial cerrada ni cierre registrado); el rastro previo conserva el estado y el registro de publicaciones anteriores"}
              if not presentes else {}),
           "nota": (f"Aprobación histórica del material {mat}, distinto del actual {actual}: no acredita la versión actual. " if mat and mat != actual else
                    f"Salida oficial que ya no está respaldada por una aprobación válida del material actual ({motivo[:120]}): no acredita la versión actual. ")
                   + "La auditoría que la aprobó no se ha borrado ni cambiado" + (" (copia en este archivo)." if copiada else ("; no se pudo copiar (auditoria.md no se puede leer)." if os.path.exists(os.path.join(carpeta, "auditoria.md")) else "; en el momento de la retirada no había auditoria.md en el expediente."))}
    # (4.13.1, H5) la identidad de la aprobación que esta retirada quita (solicitud y huella fiel de la respuesta aceptada): restaurar archivos
    # antiguos, también el estado del pipeline, no la reactiva (motivo_aprobacion_retirada lo comprueba aquí y en aprobaciones_retiradas.json)
    _st0 = st if isinstance(st, dict) else _j_tolerante(os.path.join(carpeta, "estado_pipeline.json"))
    _st0 = _st0 if isinstance(_st0, dict) else None
    ident = identidad_aprobacion(_st0, cv, carpeta) if cerrada and ((_st0 or {}).get("auditoria") == "APROBADO" or _st0 is None) else None
    if ident:
        reg["aprobacion_retirada"] = {"solicitud": ident[0], "auditoria_fiel": ident[1], "fecha": reg["retirada"]}
    json.dump(reg, open(os.path.join(destino, "RETIRADA.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    if ident:
        try:
            anotar_aprobacion_retirada(carpeta, ident, mat, motivo, os.path.relpath(destino, carpeta))
        except OSError:
            pass  # el antecedente (RETIRADA.json) ya lleva la identidad: es la segunda señal
    fallo_retirada = None
    if F.get("empresa") or cerrada:
        # (4.7) en todos los destinos registrados y en el que se pase; un destino inaccesible queda como retirada pendiente
        # (4.10, §3.3) también si la ficha ya no dice su empresa (p. ej., {}): los destinos registrados llevan la suya
        # (4.13, revisión interna R2) protegida: un fallo inesperado no impide quitar la aprobación del estado (abajo); el registro queda
        # como estaba y retiradas_pendientes() lo sigue mostrando
        sin_registro = not any(os.path.lexists(os.path.join(carpeta, n)) for n in (REGISTRO_RESUMEN, RESPALDO_RESUMEN))
        try:
            retirar_publicaciones(carpeta, motivo, csv_path, F.get("empresa"), mat)
        except (AttributeError, TypeError, KeyError, IndexError, ValueError) as e:
            fallo_retirada = f"{type(e).__name__}: {str(e)[:160]}"
        if sin_respaldo and sin_registro:
            # (4.13.1, H5; revisión interna D1-1, D1-2, D1-10) sin registro ni respaldo: los destinos que el PROPIO estado del pipeline
            # registra como publicados por esta aprobación (paso 14) se retiran como destinos conocidos, con su empresa; nunca se busca una
            # fila por el nombre de la empresa en otros CSV (D1-1). Si la ruta registrada ya no existe (expediente trasladado), se usa la
            # misma ruta junto a la ubicación actual. retirar_publicaciones los registra y deja la retirada pendiente visible (código 5) si
            # un destino no se puede escribir (D1-2)
            # Solo destinos JUNTO A LA UBICACIÓN ACTUAL del expediente (la ruta registrada se traslada a la carpeta actual por su nombre) y el
            # destino que pasa la vía: una ruta absoluta del historial puede ser la del ORIGINAL de una copia (o de un expediente movido), y sin
            # registro no hay registro_id que lo distinga; no se toca ningún CSV fuera de la carpeta actual (protección de copias, 4.7, H-2)
            base = os.path.dirname(os.path.abspath(carpeta))
            vistos = set()
            for ruta, emp in destinos_publicados_en_el_estado(_st0):
                destino_csv = os.path.join(base, os.path.basename(ruta))
                if not emp:
                    # (D2-1) la línea truncada no dice la empresa: la de los archivos de entrada del expediente, si es una sola
                    nombres = _empresas_del_expediente(carpeta)
                    emp = next(iter(nombres)) if len(nombres) == 1 else None
                    if not emp:
                        continue
                if (destino_csv, emp) in vistos:
                    continue
                vistos.add((destino_csv, emp))
                try:
                    retirar_publicaciones(carpeta, motivo, destino_csv, emp, mat)
                except (AttributeError, TypeError, KeyError, IndexError, ValueError) as e:
                    fallo_retirada = f"{os.path.basename(ruta)}: {type(e).__name__}: {str(e)[:120]}"
            if csv_path and os.path.abspath(csv_path) not in {d for d, _ in vistos}:
                for emp in sorted({e for _, e in vistos}):  # (D1-10) el destino de la vía, con la empresa que registró el propio estado
                    try:
                        retirar_publicaciones(carpeta, motivo, csv_path, emp, mat)
                    except (AttributeError, TypeError, KeyError, IndexError, ValueError) as e:
                        fallo_retirada = f"{os.path.basename(csv_path)}: {type(e).__name__}: {str(e)[:120]}"
    if ident and cerrada:
        # (4.13.1, H5; revisión interna D2-2) las publicaciones que esta retirada de la aprobación retiró llevan su identidad y la marca
        # retirada_de_la_aprobacion: es la tercera señal de motivo_aprobacion_retirada (una retirada de filas de la sincronización no la lleva)
        try:
            reg_m = _leer_registro(carpeta)
            cambio = False
            for e in reg_m.get("publicaciones") or []:
                if not isinstance(e, dict) or e.get("estado") not in ("retirada", "retirada_pendiente"):
                    continue
                if e.get("solicitud") is None and e.get("material_auditado") == mat:
                    e.update(solicitud=ident[0], auditoria_fiel=ident[1])  # publicación anterior a la 4.13.1 de esta misma aprobación
                if (e.get("solicitud"), e.get("auditoria_fiel")) == tuple(ident) and not e.get("retirada_de_la_aprobacion"):
                    e["retirada_de_la_aprobacion"] = True
                    cambio = True
            if cambio:
                _guardar_registro(carpeta, reg_m)
        except (RegistroIlegible, OSError, AttributeError, TypeError, KeyError, ValueError):
            pass  # sin registro legible: deciden aprobaciones_retiradas.json y RETIRADA.json
    ep = os.path.join(carpeta, "estado_pipeline.json")
    propio = st is None
    if propio:
        st = _j_tolerante(ep)  # (4.9, Z-2) ilegible: no se toca; las salidas y las filas se retiran igual
        if st is not None and not isinstance(st, dict):
            st = None
    if st is not None:
        # (segundo control de vigencia, W-1; 4.13, revisión interna R2) los campos que se actualizan aquí con un tipo erróneo (o nulos)
        # ya no dejan el estado sin tocar (y con APROBADO): se reparan, conservando el valor anterior, y la aprobación se quita igual
        malos = {k: st.get(k) for k, tipo in (("historial", list), ("cierres_archivados", list), ("paso", int))
                 if k in st and (not isinstance(st.get(k), tipo) or isinstance(st.get(k), bool))}
        if malos:
            st.setdefault("campos_reparados_en_la_retirada", []).append({"valores_anteriores": malos, "fecha": reg["retirada"]})
            for k in malos:
                st[k] = 13 if k == "paso" else []
        if st.get("estado_analisis") in ("concluido", "pendiente_de_investigacion", "pendiente_de_datos") and cerrada:
            st["estado_analisis"] = None
            st["paso"] = min(st.get("paso", 13), 13)
        aud_reg = st.get("auditoria")
        if aud_reg == "APROBADO" and cerrada:
            st["auditoria"] = None  # la aprobación registrada era la del cierre archivado: no acredita el material actual
        st.setdefault("cierres_archivados", []).append({"carpeta": os.path.relpath(destino, carpeta), "material_auditado": mat, "auditoria_registrada": aud_reg, "motivo": motivo[:300]})
        st.setdefault("historial", []).append(f"{reg['retirada']} · " + (f"salidas oficiales archivadas en {os.path.relpath(destino, carpeta)}" if presentes else
                                              f"aprobación publicada sin respaldo retirada (sin salidas oficiales que archivar; antecedente en {os.path.relpath(destino, carpeta)})")
                                              + f": {motivo[:200]}"
                                              + (f" · la retirada de las publicaciones falló ({fallo_retirada}): queda pendiente" if fallo_retirada else ""))
        if propio:
            json.dump(st, open(ep, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return destino


def asegurar_vigencia(carpeta, veredicto, empresa=None, csv_path=None, st=None, comprobar_informe=True):
    """Si hay salidas oficiales cerradas que ya no son vigentes, las archiva. Devuelve (motivo, carpeta_archivo) o (None, None)."""
    m = motivo_vigencia(carpeta, veredicto, empresa, comprobar_informe)
    if not m:
        return None, None
    return m, archivar_salidas(carpeta, m, csv_path, st)


# ---------- 6. destinos del resumen (reparación 4.7) ----------
# Cada publicación de una fila de una ficha cerrada queda registrada en publicaciones_resumen.json, dentro del expediente y fuera de
# las salidas oficiales (no se archiva con ellas), con un respaldo (.publicaciones_resumen.respaldo.json): destino efectivo (ruta
# absoluta), empresa, expediente (ruta real) y material aprobado. Toda invalidación retira la aprobación en TODOS los destinos
# registrados (y en el que se pase), aunque la ficha, el informe y cierre_vigente.json ya estén archivados. No se buscan CSV fuera
# del registro (salvo la traslación de rutas de abajo, que solo mira la ruta equivalente de un destino ya registrado).
#   - Destino inaccesible (error de escritura o carpeta ausente): «retirada_pendiente» (código operativo 5), reintento en la llamada
#     siguiente. CSV ausente en una carpeta accesible: «sin_archivo», vigilado en cada sincronización.
#   - Identidad (auditorías internas de la 4.7, H-2, C-1, C-2): el registro lleva un registro_id. Una entrada cuyo expediente no es
#     este se interpreta así: si en esa ruta sigue existiendo un expediente con un registro del MISMO registro_id, este expediente es
#     una COPIA del original vivo: se registran como propios los destinos equivalentes (ruta trasladada) que existan y sean distintos
#     de los del original, la copia recibe un registro_id nuevo y las entradas del original pasan a «heredadas_del_original» (no se
#     tocan sus filas). Si no (ruta ausente, otro expediente u otro registro): este expediente es el original TRASLADADO o renombrado:
#     adopta las entradas y, para cada destino, usa la ruta trasladada si existe y, si no, la registrada.
#   - Salida humana para un destino que no volverá: la persona responsable puede poner en la entrada estado «descartada» con
#     «descartado_por» y «fecha_descarte» no vacíos (Claude no lo hace); esa entrada deja de bloquear. Un descarte incompleto
#     sigue como retirada pendiente.
#   - Traslado: solo se traslada un destino cuya carpeta registrada ya no está accesible (F-1).
#   - El resumen predeterminado del expediente es siempre un destino conocido (F-2).
#   - Registro ilegible: retirada pendiente (código 5), sin sobrescribirlo; aun así se retira el destino conocido de la llamada y,
#     si el respaldo es legible, los destinos del respaldo. Registro ausente: se usa el respaldo, con aviso.
#   - Escritura atómica (temporal y os.replace).
REGISTRO_RESUMEN = "publicaciones_resumen.json"
RESPALDO_RESUMEN = ".publicaciones_resumen.respaldo.json"
_VIVOS = ("publicada", "retirada_pendiente", "sin_archivo")
AVISOS_REGISTRO = []  # avisos ya impresos (salida de error) en este proceso


def _elemento_valido(e):
    """(4.13, revisión interna R2) Una entrada del registro es un objeto con `csv` de texto, `empresa` y `expediente` de texto o nulos y
    `estado` de texto. Cualquier otra cosa hace el registro ilegible (retirada pendiente visible), sin interpretarla."""
    return (isinstance(e, dict) and isinstance(e.get("csv"), str) and e.get("csv")
            and all(e.get(k) is None or isinstance(e.get(k), str) for k in ("empresa", "expediente", "material_auditado"))
            and isinstance(e.get("estado"), str))


class RegistroIlegible(Exception):
    def __init__(self, msg, respaldo=None):
        super().__init__(msg)
        self.respaldo = respaldo


def _ruta_exp(carpeta):
    return os.path.realpath(carpeta)


def _cargar(ruta):
    reg = json.load(open(ruta, encoding="utf-8"))
    if not isinstance(reg, dict) or not isinstance(reg.get("publicaciones"), list):
        raise ValueError("estructura no válida")
    malos = [i for i, e in enumerate(reg["publicaciones"]) if not _elemento_valido(e)]
    if malos:
        # (4.13, R2) se conservan las entradas válidas para retirar lo que se conoce; el registro sigue siendo ilegible
        err = ValueError(f"entradas mal formadas en publicaciones (posiciones {malos[:10]})")
        err.validas = [e for e in reg["publicaciones"] if _elemento_valido(e)]
        raise err
    return reg


def _leer_registro(carpeta):
    vacio = {"nota": "destinos del resumen en los que se publicó una fila de una ficha cerrada (reparación 4.7)", "publicaciones": []}
    principal, respaldo = os.path.join(carpeta, REGISTRO_RESUMEN), os.path.join(carpeta, RESPALDO_RESUMEN)
    rres = None
    validas = []
    if os.path.exists(respaldo):
        try:
            rres = _cargar(respaldo)
        except (ValueError, OSError) as e:
            rres = None
            validas += getattr(e, "validas", [])
    if os.path.exists(principal):
        try:
            return _cargar(principal)
        except (ValueError, OSError) as err:
            # (4.13, R2) para retirar lo que se conoce: el respaldo legible y, si no, las entradas válidas del principal y del respaldo
            conocidas = rres or {"publicaciones": validas + getattr(err, "validas", [])}
            raise RegistroIlegible(f"{REGISTRO_RESUMEN} ilegible ({type(err).__name__}: {err}); se conserva sin tocar: hay que restaurarlo"
                                   + (" (el respaldo es legible)" if rres else ""), conocidas) from err
    if os.path.exists(respaldo):
        if rres is None:
            raise RegistroIlegible(f"{REGISTRO_RESUMEN} no existe y {RESPALDO_RESUMEN} es ilegible: hay que restaurarlo")
        aviso = f"AVISO: {REGISTRO_RESUMEN} no existía en {carpeta}: se ha recuperado del respaldo"
        if aviso not in AVISOS_REGISTRO:
            AVISOS_REGISTRO.append(aviso)
            import sys as _sys
            print(aviso, file=_sys.stderr)
        rres.setdefault("avisos", []).append(f"{REGISTRO_RESUMEN} no existía: recuperado del respaldo")
        return rres
    return vacio


def _guardar_registro(carpeta, reg):
    reg.setdefault("registro_id", _nuevo_id())
    for nombre in (REGISTRO_RESUMEN, RESPALDO_RESUMEN):
        tmp = os.path.join(carpeta, nombre + ".tmp")
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(reg, fh, ensure_ascii=False, indent=1)
        os.replace(tmp, os.path.join(carpeta, nombre))


def _nuevo_id():
    import uuid
    return uuid.uuid4().hex


def _registro_id_en(ruta_exp):
    for nombre in (REGISTRO_RESUMEN, RESPALDO_RESUMEN):
        try:
            return _cargar(os.path.join(ruta_exp, nombre)).get("registro_id")
        except (ValueError, OSError):
            continue
    return "sin registro"


def _trasladar(csv, desde, hasta):
    return os.path.normpath(os.path.join(hasta, os.path.relpath(csv, desde)))


def _propias(reg, carpeta):
    """Entradas de este expediente, resolviendo copias y traslados (ver la cabecera de la sección). Modifica `reg`."""
    exp = _ruta_exp(carpeta)
    mi_id = reg.get("registro_id")
    out, heredadas = [], []
    for e in list(reg["publicaciones"]):
        r = e.get("expediente")
        if not r or os.path.realpath(r) == exp:
            out.append(e)
            continue
        if mi_id is not None and os.path.isdir(r) and _registro_id_en(r) == mi_id:  # (final, F-5a) sin registro_id no hay copia reconocible
            # copia del original vivo: solo los destinos equivalentes de la copia, distintos de los del original
            heredadas.append(e)
            reg["publicaciones"].remove(e)
            nuevo = _trasladar(e["csv"], r, exp)
            if nuevo != e["csv"] and os.path.exists(nuevo) and not any(x["csv"] == nuevo and x["empresa"] == e["empresa"] for x in reg["publicaciones"]):
                c = {k: v for k, v in e.items() if k not in ("trasladado_desde",)}
                c.update({"csv": nuevo, "expediente": exp, "heredada_de_la_copia": {"expediente": r, "csv": e["csv"]}})
                reg["publicaciones"].append(c)
                out.append(c)
        else:
            # original trasladado o renombrado
            nuevo = _trasladar(e["csv"], r, exp)
            e.setdefault("trasladado_desde", []).append({"expediente": r, "csv": e["csv"]})
            e["expediente"] = exp
            # (final, F-1) solo se traslada un destino cuya carpeta registrada ya no está accesible; si lo está, se conserva el registrado
            if nuevo != e["csv"] and not os.path.isdir(os.path.dirname(e["csv"])) and os.path.isdir(os.path.dirname(nuevo)):
                e["csv"] = nuevo
            out.append(e)
    if heredadas:
        reg.setdefault("heredadas_del_original", []).extend(heredadas)
        reg["copia_de"] = {"registro_id": mi_id, "expediente": heredadas[0].get("expediente")}
        reg["registro_id"] = _nuevo_id()
    return [e for e in out if not _descartada(e)]


def _viva(e):
    """Entrada que todavía puede presentar una aprobación: publicada, pendiente, sin archivo o con un descarte INCOMPLETO (F-3)."""
    return e.get("estado") in _VIVOS or (e.get("estado") == "descartada" and not _descartada(e))


def _descartada(e):
    return e.get("estado") == "descartada" and e.get("descartado_por") and e.get("fecha_descarte")


def registrar_publicacion(carpeta, csv_path, empresa, material_auditado):
    import datetime as _dt
    reg = _leer_registro(carpeta)
    ruta = os.path.abspath(csv_path)
    exp = _ruta_exp(carpeta)
    e = next((x for x in _propias(reg, carpeta) if x["csv"] == ruta and x["empresa"] == empresa), None)
    if e is None:
        e = {"csv": ruta, "empresa": empresa, "expediente": exp}
        reg["publicaciones"].append(e)
    e.update({"material_auditado": material_auditado, "estado": "publicada", "fecha": _dt.datetime.now().isoformat(timespec="seconds"), "error": None})
    # (4.13.1, H5; revisión interna D1-3) cada publicación lleva la identidad de la aprobación que la respalda (solicitud y huella fiel de
    # la respuesta aceptada): la sincronización cambia el estado de la entrada, no su identidad, y así una aprobación retirada no se reactiva
    # aunque se restaure el estado del pipeline
    ep = os.path.join(carpeta, "estado_pipeline.json")
    st = _j_tolerante(ep)
    ident = identidad_aprobacion(st if isinstance(st, dict) else None, _j_tolerante(os.path.join(carpeta, CIERRE_VIGENTE)), carpeta)
    if ident:
        e.update(solicitud=ident[0], auditoria_fiel=ident[1])
    _guardar_registro(carpeta, reg)
    if ident and isinstance(st, dict):
        pubs = st.setdefault("publicaciones_de_la_aprobacion", [])
        if isinstance(pubs, list) and not any(isinstance(x, dict) and (x.get("solicitud"), x.get("auditoria_fiel"), x.get("csv")) == (ident[0], ident[1], ruta) for x in pubs):
            pubs.append({"solicitud": ident[0], "auditoria_fiel": ident[1], "csv": ruta, "fecha": e["fecha"]})
            try:
                tmp = ep + ".tmp"
                json.dump(st, open(tmp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
                os.replace(tmp, ep)
            except OSError:
                pass  # la entrada del registro ya lleva la identidad


def _retirar_en(objetivos, motivo):
    pendientes = []
    for e in objetivos:
        try:
            if not os.path.isdir(os.path.dirname(e["csv"])):
                raise FileNotFoundError(f"la carpeta del destino no está accesible: {os.path.dirname(e['csv'])}")
            if not os.path.exists(e["csv"]):
                e["estado"], e["error"] = "sin_archivo", "el CSV no existe en una carpeta accesible: se vuelve a comprobar en cada sincronización"
                continue
            _retirar_fila(e["csv"], e["empresa"], e.get("material_auditado"), motivo)
            e["estado"], e["error"] = "retirada", None
            e["retirada_motivo"] = motivo[:300]
            e["fecha_retirada"] = __import__("datetime").datetime.now().isoformat(timespec="seconds")
        except OSError as err:
            e["estado"], e["error"] = "retirada_pendiente", f"{type(err).__name__}: {err}"
            pendientes.append(e["csv"])
    return pendientes


def retirar_publicaciones(carpeta, motivo, csv_extra=None, empresa_extra=None, material_extra=None, conservar_material=None):
    """Retira la aprobación en los destinos registrados (salvo los del material `conservar_material`, si es el vigente) y en
    `csv_extra`. Devuelve la lista de destinos con la retirada pendiente."""
    exp = _ruta_exp(carpeta)
    extra = {"csv": os.path.abspath(csv_extra), "empresa": empresa_extra, "expediente": exp, "material_auditado": material_extra, "estado": "publicada",
             "fecha": None, "error": None, "registrado_en_la_retirada": True} if csv_extra and empresa_extra else None
    try:
        reg = _leer_registro(carpeta)
    except RegistroIlegible as err:
        # (C-3) el registro no se toca, pero se retira lo que se conoce: el destino de la llamada y, si es legible, el respaldo
        objetivos = ([extra] if extra else []) + [e for e in ((err.respaldo or {}).get("publicaciones") or []) if _viva(e)
                                                     and os.path.realpath(e.get("expediente") or "") == exp and not (conservar_material and e.get("material_auditado") == conservar_material)]
        pend = _retirar_en(objetivos, motivo)
        return [f"{REGISTRO_RESUMEN}: {err}"] + pend
    propias = _propias(reg, carpeta)
    objetivos = [e for e in propias if _viva(e) and not (conservar_material and e.get("material_auditado") == conservar_material)]
    if extra:
        previa = next((e for e in propias if e["csv"] == extra["csv"] and e["empresa"] == empresa_extra), None)
        if previa is None:
            reg["publicaciones"].append(extra)
            objetivos.append(extra)
        elif previa not in objetivos:
            # (4.7.1, W-f de la auditoría interna) el destino de la llamada ya estaba registrado como retirado (o como el del material
            # vigente) y su fila aprobada ha reaparecido (p. ej., al restaurar una copia de seguridad): se vuelve a retirar
            objetivos.append(previa)
    pendientes = _retirar_en(objetivos, motivo)
    _guardar_registro(carpeta, reg)
    return pendientes


def sincronizar_resumenes(carpeta, veredicto, empresa=None):
    """Si no hay una salida oficial cerrada VIGENTE, retira la aprobación en todos los destinos registrados; si la hay, solo en los
    registrados para otro material. Devuelve los destinos con la retirada pendiente."""
    F = leer_ficha_control(os.path.join(carpeta, "ficha.json"))[0]  # (4.9, V-1, W-1) ilegible: no hay salida vigente; se retira
    vigente = ficha_cerrada(F) and motivo_vigencia(carpeta, veredicto, empresa) is None
    conservar = (F.get("cierre") or {}).get("material_auditado") if vigente else None
    motivo = "sin salida oficial vigente que respalde la aprobación publicada" if not vigente else "aprobación de un material distinto del vigente"
    # (final, F-2; vigencia, V-1 y V-2; 4.7.1, W-1 y W-a) el resumen predeterminado (junto a la ubicación ACTUAL del expediente) es
    # un destino conocido para una aprobación publicada allí sin registrar (anterior a la 4.7). Se DETECTA como en la 4.7: fila
    # APROBADO de la empresa con la fecha de una ficha cerrada que este expediente archivó (la fecha se lee también en los formatos
    # que deja una hoja de cálculo). El contenido publicado solo sirve para EXCLUIR la fila de la ficha oficial vigente, si la hay,
    # con los números comparados con tolerancia; si la exclusión falla, la fila se retira y resumen.py la vuelve a publicar (sentido
    # conservador). La empresa sale de la ficha, nunca del nombre de la carpeta que pasa el pipeline. Se calcula antes de leer el
    # registro, porque no depende de él (W-b: también con el registro ilegible).
    archivadas = _fichas_cerradas_archivadas(carpeta)
    emp = (F or {}).get("empresa") or (archivadas[0].get("empresa") if archivadas else None) or empresa
    pred = os.path.join(os.path.dirname(os.path.abspath(carpeta)), nombre_resumen(carpeta))  # (4.11, H2) el de la V6.4 en un expediente V6.4
    origen = _fila_aprobada(pred, emp, archivadas, salvo=F if vigente else None) if emp else None
    extra = (pred, emp, ((origen or {}).get("cierre") or {}).get("material_auditado")) if origen is not None else (None, None, None)
    try:
        reg = _leer_registro(carpeta)
    except RegistroIlegible:
        return retirar_publicaciones(carpeta, motivo, *extra, conservar_material=conservar)
    antes = json.dumps(reg, sort_keys=True)
    propias = _propias(reg, carpeta)
    if vigente and conservar:
        # (4.13.1, H5; revisión interna D1-3) las publicaciones anteriores a la 4.13.1 de un cierre VIGENTE reciben la identidad de su
        # aprobación (solicitud y huella fiel; o la huella de la auditoría en un cierre anterior a la 4.8.1), para que una retirada posterior
        # la conserve aunque se restaure el estado del pipeline
        ident = identidad_aprobacion(_j_tolerante(os.path.join(carpeta, "estado_pipeline.json")), _j_tolerante(os.path.join(carpeta, CIERRE_VIGENTE)), carpeta)
        for e in propias:
            if ident and e.get("estado") == "publicada" and e.get("material_auditado") == conservar and not e.get("solicitud"):
                e.update(solicitud=ident[0], auditoria_fiel=ident[1])
    if json.dumps(reg, sort_keys=True) != antes:
        _guardar_registro(carpeta, reg)  # copia o traslado resueltos: se fija el resultado
    if origen is None and not any(_viva(e) and not (conservar and e.get("material_auditado") == conservar) for e in propias):
        return []
    return retirar_publicaciones(carpeta, motivo, *extra, conservar_material=conservar)


def _num(v):
    """Número de una celda del resumen (o de la ficha), también con coma decimal; None si no es un número."""
    if isinstance(v, bool) or v is None:
        return None
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).strip()
    try:
        return float(s)
    except ValueError:
        pass
    import re as _re
    return float(s.replace(",", ".")) if _re.fullmatch(r"-?\d+,\d+", s) else None


def _fechas(v):
    """Fechas que puede representar un texto de fecha: ISO (la de la ficha) o los formatos habituales de una hoja de cálculo
    (día/mes y mes/día se admiten los dos, porque el texto no permite distinguirlos)."""
    import datetime as _dt
    s = str(v or "").strip().split("T")[0].split(" ")[0]
    out = set()
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%d/%m/%Y", "%m/%d/%Y", "%d/%m/%y", "%m/%d/%y", "%d.%m.%Y", "%d-%m-%Y"):
        try:
            out.add(_dt.datetime.strptime(s, fmt).date())
        except ValueError:
            pass
    return out


def _misma_fecha(v, fecha):
    a, b = _fechas(v), _fechas(fecha)
    if a and b:
        return bool(a & b)
    return bool(str(fecha or "").strip()) and str(v or "").strip() == str(fecha).strip()


def _igual(v, x):
    """Celda `v` del resumen frente al valor `x` de la ficha: números con tolerancia relativa de 1e-6; texto sin espacios de los extremos."""
    if x is None or (isinstance(x, str) and not x.strip()):
        return not str(v or "").strip()
    a, b = _num(v), _num(x)
    if a is not None and b is not None:
        import math
        return math.isclose(a, b, rel_tol=1e-6, abs_tol=1e-9)
    return str(v or "").strip() == str(x).strip()


def _fila_de(r, F):
    """La fila `r` de un resumen presenta lo que publicó la ficha `F` (mismas columnas que resumen.py toma de la ficha), con los
    números normalizados y la fecha en cualquiera de los formatos de _fechas (4.7.1, W-a)."""
    esc = (F or {}).get("escalera") or {}
    pares = {"estado_analisis": F.get("estado_analisis"), "precio": F.get("precio"), "moneda": F.get("moneda"),
             "precio_si": esc.get("precio_si"), "ponderado": esc.get("ponderado"), "zona": esc.get("zona"),
             "accion": (F.get("decision") or {}).get("accion"), "cubo_v2": F.get("cubo"), "motor": F.get("motor")}
    fecha_ok = _misma_fecha(r.get("fecha"), F.get("fecha")) if F.get("fecha") else not (r.get("fecha") or "").strip()
    return fecha_ok and all(_igual(r.get(k), x) for k, x in pares.items())


def _fila_aprobada(csv_path, empresa, de_fichas, salvo=None):
    """Ficha de `de_fichas` (cerradas y archivadas por este expediente) cuya aprobación sigue publicada en `csv_path`: fila APROBADO
    de la empresa con su fecha que no es la de la ficha `salvo` (la oficial vigente, si la hay). None si no hay ninguna."""
    import csv as _csv
    try:
        with open(csv_path, encoding="utf-8", newline="") as fh:
            for r in _csv.DictReader(fh):
                if (r.get("empresa") or "").strip() != empresa or (r.get("verificacion") or "").strip() != "APROBADO" or (salvo and _fila_de(r, salvo)):
                    continue
                A = next((A for A in de_fichas if _misma_fecha(r.get("fecha"), A.get("fecha"))), None)
                if A is not None:
                    return A
    except (OSError, ValueError):
        return None
    return None


def _fichas_cerradas_archivadas(carpeta):
    """Fichas cerradas archivadas en historial_cierres/, de la más reciente a la más antigua."""
    base = os.path.join(carpeta, "historial_cierres")
    out = []
    if os.path.isdir(base):
        for d in sorted(os.listdir(base), reverse=True):
            F = leer_ficha_control(os.path.join(base, d, "ficha.json"))[0]  # (4.9, V-1, W-1) una ficha archivada ilegible no interrumpe la retirada
            if F and ficha_cerrada(F):
                out.append(F)
    return out


def retiradas_pendientes(carpeta):
    try:
        reg = _leer_registro(carpeta)
    except RegistroIlegible as err:
        return [f"{REGISTRO_RESUMEN}: {err}"]
    return [e["csv"] for e in _propias(reg, carpeta) if e.get("estado") == "retirada_pendiente" or (e.get("estado") == "descartada" and not _descartada(e))]
