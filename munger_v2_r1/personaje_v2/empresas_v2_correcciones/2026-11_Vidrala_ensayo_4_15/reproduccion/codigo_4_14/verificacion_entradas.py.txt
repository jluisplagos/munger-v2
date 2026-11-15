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
Uso: verificacion_entradas.py comprobar <expediente> [--json] | plantilla <expediente> (escribe verificacion_entradas.plantilla.json)
"""
import ast
import hashlib
import json
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import entradas_economicas as EE  # noqa: E402

FORMATO = "4.14"
REGISTRO = "verificacion_entradas.json"
CLASES = ("dato_publicado", "derivado", "cero_comprobado", "dato_ausente", "no_aplicable", "hipotesis", "convencion")
CAMPOS_FUENTE = ("documento", "version", "pagina", "ubicacion", "concepto", "columna", "periodo", "unidad", "escala", "signo", "tratamiento",
                 "perimetro", "reexpresado", "valor_fuente", "cita")
RESULTADOS = ("verificado", "discrepancia", "pendiente")
# unidades → millones de la moneda (el modelo trabaja en «mm»: Control maestro!J4)
UNIDADES = {"mm": 1.0, "millones": 1.0, "millones de euros": 1.0, "millones de eur": 1.0, "m€": 1.0, "meur": 1.0, "€m": 1.0,
            "miles": 1e-3, "miles de euros": 1e-3, "miles de eur": 1e-3, "k€": 1e-3, "keur": 1e-3, "€000": 1e-3, "euros": 1e-6, "eur": 1e-6}
TOL_ABS, TOL_REL = 0.0011, 1e-6  # 3 decimales en mm (redondeo declarado del libro)
COL_ANIO = {c: i for i, c in enumerate("CDEFGHIJKL")}  # Historia C5:L5


def _sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest() if os.path.isfile(p) else None


def _num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and x == x and abs(x) != float("inf")


def _igual(a, b):
    if _num(a) and _num(b):
        return abs(a - b) <= max(TOL_ABS, TOL_REL * max(abs(a), abs(b)))
    return EE.iguales(a, b) if hasattr(EE, "iguales") else a == b


def libro_de(carpeta):
    e = os.path.basename(os.path.abspath(carpeta))
    for n in (f"{e}_v63_evaluada.xlsx", f"{e}_v63_datos.xlsx"):
        if os.path.isfile(os.path.join(carpeta, n)):
            return os.path.join(carpeta, n)
    return None


def universo(carpeta):
    lb = libro_de(carpeta)
    return EE.instantanea(lb) if lb else None


def _anios(inst):
    return [inst["celdas"].get(f"Historia!{c}5") for c in "CDEFGHIJKL"]


def _ruta_fuente(carpeta, archivo):
    if not archivo:
        return None
    for base in (carpeta, os.path.dirname(AQUI), os.path.dirname(os.path.dirname(AQUI))):
        p = os.path.normpath(os.path.join(base, archivo))
        if os.path.isfile(p):
            return p
    return None


def _texto_pagina(ruta_txt, pagina):
    """Texto de la página `pagina` de un .txt con marcas «[PDF PAGE n]» (extract_pdf_text.py); None si no se puede."""
    try:
        t = open(ruta_txt, encoding="utf-8", errors="replace").read()
    except OSError:
        return None
    m = re.search(r"\d+", str(pagina or ""))
    if not m:
        return None
    n = int(m.group(0))
    partes = re.split(r"\[PDF PAGE (\d+)\]", t)
    for i in range(1, len(partes) - 1, 2):
        if int(partes[i]) == n:
            return partes[i + 1]
    return None


def _norm_txt(s):
    # (14-nov, revisión del extractor de Viscofan) «str(s or "")» convertía el 0 en "": un 0 publicado y una celda vacía parecían iguales
    return re.sub(r"\s+", " ", "" if s is None else str(s)).strip().lower()


def _cifras(x):
    """Formas textuales de un número de la fuente (1.234,5 · 1,234.5 · 1234.5 · 1234,5)."""
    if not _num(x):
        return []
    a = abs(x)
    out = set()
    for dec in range(0, 7):  # (14-nov) hasta seis decimales: los boletines de cotización imprimen cuatro («54,7000»)
        s = f"{a:,.{dec}f}"
        out |= {s, s.replace(",", "X").replace(".", ",").replace("X", "."), s.replace(",", ""), s.replace(",", "").replace(".", ","),
                s.replace(",", " ").replace(".", ",")}  # miles con espacio y coma decimal («4 573,7», informes en francés)
    return [o for o in out if o]


def _cita_contiene(cita, vf):
    """El valor de la fuente aparece en la cita como cifra completa: no dentro de otra cifra (el «0» de «2019», el «12» de «2012»).
    Límite declarado: en el texto extraído las columnas van a veces separadas por un solo espacio, así que «4 573,7» no se distingue
    de dos cifras («4» y «573,7»); el control lo acepta y la pertinencia es del revisor independiente.
    Un cero puede estar impreso como «-», «–» o «—» aislado (pegado o a un solo espacio de una cifra es un signo menos; con dos o más, la columna siguiente)."""
    t = re.sub(r"[\u00a0\u202f\u2009]", " ", str(cita or ""))
    if _num(vf) and vf == 0 and (re.search(r"(?<![\w.,])[-–—](?![\w.,]| ?[\d(])", t) or re.search(r"(?<=[\d)] )[-–—](?= [\d(])", t)):
        return True  # aislado, o entre dos cifras de columnas contiguas («784.366 - 784.366»)
    return any(re.search(r"(?<![\d.,])" + re.escape(c) + r"(?!\d|[.,]\d)", t) for c in _cifras(vf))


def _eval_formula(formula, o):
    """Evalúa una expresión aritmética sobre o["<origen>"] (solo números, + − × ÷, paréntesis, abs/min/max/sum)."""
    arbol = ast.parse(formula, mode="eval")
    permitidos = (ast.Expression, ast.BinOp, ast.UnaryOp, ast.Constant, ast.Subscript, ast.Name, ast.Load, ast.Add, ast.Sub, ast.Mult, ast.Div,
                  ast.USub, ast.UAdd, ast.Call, ast.List, ast.Tuple, ast.Index if hasattr(ast, "Index") else ast.Constant)
    for n in ast.walk(arbol):
        if not isinstance(n, permitidos):
            raise ValueError(f"elemento no permitido en la fórmula: {type(n).__name__}")
        if isinstance(n, ast.Name) and n.id not in ("o", "abs", "min", "max", "sum"):
            raise ValueError(f"nombre no permitido: {n.id}")
    return eval(compile(arbol, "<formula>", "eval"), {"__builtins__": {}}, {"o": o, "abs": abs, "min": min, "max": max, "sum": sum})


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
    return d, None


def perimetro_esperado(carpeta, reg):
    """El perímetro que declara el registro para el expediente (p. ej., «consolidado» o «consolidado · operaciones continuadas»)."""
    return str((reg or {}).get("perimetro_del_expediente") or "").strip() or None


def comprobar(carpeta):
    """Informe de la verificación: cobertura, entradas comprobadas, pendientes, desactualizadas, discrepancias y errores del contrato, con la
    aptitud por entradas. Nunca lanza: un registro ausente o ilegible es «no verificado»."""
    inst = universo(carpeta)
    out = {"formato": FORMATO, "universo": (inst or {}).get("n"), "huella_entradas_economicas": (inst or {}).get("huella"), "registro": None,
           "por_clase": {}, "comprobadas": [], "pendientes": [], "desactualizadas": [], "discrepancias": [], "errores": [], "sin_entrada": [],
           "sobrantes": [], "repetidas": [], "auxiliares": 0, "materiales_no_comprobadas": [], "apto_por_entradas": False, "motivo": None}
    if inst is None:
        out["motivo"] = "no hay libro del expediente: no se puede fijar el universo de entradas"
        return out
    reg, err = cargar(carpeta)
    if reg is None:
        out["motivo"] = err or f"no hay {REGISTRO}: ninguna entrada financiera está verificada (un Excel evaluado anterior no acredita nada)"
        out["sin_entrada"] = sorted(inst["celdas"])
        out["pendientes"] = [f"{k}: sin entrada en el registro" for k in out["sin_entrada"]]
        out["materiales_no_comprobadas"] = [k for k in out["sin_entrada"] if inst["tipos"].get(k) != "hipótesis"]
        return out
    out["registro"] = REGISTRO
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

    def revisar_una(k, e):
        clase = e.get("clase")
        out["por_clase"][clase] = out["por_clase"].get(clase, 0) + 1
        if clase not in CLASES:
            return problema(k, "error", f"clase {clase!r} no es una de {CLASES}")
        tipo_u = inst["tipos"].get(k)
        if tipo_u == "hipótesis" and clase not in ("hipotesis", "convencion"):
            return problema(k, "error", f"la celda es una hipótesis del modelo ({inst['ids'].get(k)}): no se presenta como {clase}")
        if clase in ("hipotesis", "convencion"):
            h = e.get("hipotesis") or {}
            falta = [c for c in ("fundamento", "alternativas", "limites") if not h.get(c)]
            if falta:
                return problema(k, "error", f"{clase} sin {', '.join(falta)} (una hipótesis conserva su identificación, fundamento, alternativas y límites)")
            if e.get("fuente", {}) and (e.get("fuente") or {}).get("valor_fuente") is not None:
                return problema(k, "error", f"{clase} presentada con un valor de fuente: no es un dato publicado")
        if not k.startswith("aux:"):
            actual = inst["celdas"].get(k)
            if not _igual(actual, e.get("valor_modelo")):
                return problema(k, "desactualizada", f"el libro dice {actual!r} y el registro {e.get('valor_modelo')!r}: la comprobación no vale para el dato actual")
        if clase in ("dato_publicado", "cero_comprobado"):
            f = e.get("fuente") if isinstance(e.get("fuente"), dict) else {}
            falta = [c for c in CAMPOS_FUENTE if f.get(c) in (None, "")]
            if falta:
                return problema(k, "pendiente", f"faltan campos del contraste documental: {', '.join(falta)}")
            ruta = _ruta_fuente(carpeta, f.get("archivo"))
            if f.get("sha256"):
                if ruta is None:
                    return problema(k, "pendiente", f"la fuente conservada {f.get('archivo')!r} no está en el expediente ni en el paquete")
                if _sha(ruta) != f["sha256"]:
                    return problema(k, "desactualizada", f"la fuente {f.get('archivo')} cambió (sha256 distinto del registrado)")
            esc, sig, vf = f.get("escala"), f.get("signo"), f.get("valor_fuente")
            vm = e.get("valor_modelo") if k.startswith("aux:") else inst["celdas"].get(k)
            if vm is None and (_num(vf) or clase == "cero_comprobado"):
                return problema(k, "discrepancia", f"la celda está vacía en el libro y la fuente publica {vf!r}: vacío no es cero (dato ausente ≠ cero comprobado)")
            if not _num(vm):
                # dato publicado de texto (moneda, unidad, norma, mercado…): el valor de la fuente es el del modelo, sin escala ni signo
                if _norm_txt(vf) != _norm_txt(vm):
                    return problema(k, "discrepancia", f"el valor de la fuente {vf!r} no es el del modelo {vm!r}")
                if ruta and ruta.endswith(".txt"):
                    pag = _texto_pagina(ruta, f.get("pagina"))
                    if pag is not None and _norm_txt(f.get("cita")) not in _norm_txt(pag):
                        return problema(k, "discrepancia", f"la cita no está en la página {f.get('pagina')} de {f.get('archivo')}")
                return revisar_comprobacion(k, e)
            if not (_num(esc) and sig in (1, -1, "+1", "-1") and _num(vf)):
                return problema(k, "error", "escala, signo (+1/−1) o valor_fuente no numéricos")
            sig = int(sig)
            u = UNIDADES.get(_norm_txt(f.get("unidad")))
            um = UNIDADES.get(unidad_modelo, 1.0)
            if u is not None and _num(um) and um and not _igual(esc, u / um):
                return problema(k, "error", f"escala {esc} incoherente con las unidades (fuente «{f.get('unidad')}» → modelo «{unidad_modelo}» = {u / um:g})")
            if not _igual(sig * esc * vf, vm):
                return problema(k, "discrepancia", f"signo × escala × valor_fuente = {sig * esc * vf:g} ≠ valor del modelo {vm!r}")
            if clase == "cero_comprobado" and not _igual(vm, 0):
                return problema(k, "error", "cero comprobado con un valor distinto de cero")
            m = re.match(r"^Historia!([C-L])(\d+)$", k)
            if m and anios[COL_ANIO[m.group(1)]] is not None:
                anio = str(int(anios[COL_ANIO[m.group(1)]])) if _num(anios[COL_ANIO[m.group(1)]]) else str(anios[COL_ANIO[m.group(1)]])
                if anio not in str(f.get("periodo")) and anio not in str(f.get("columna")):
                    return problema(k, "error", f"la columna {m.group(1)} de la Historia es {anio}, pero el período declarado es «{f.get('periodo')}» (columna «{f.get('columna')}»)")
            if per_esp and _norm_txt(f.get("perimetro")) != _norm_txt(per_esp) and not str(f.get("perimetro_justificacion") or "").strip():
                return problema(k, "error", f"perímetro «{f.get('perimetro')}» distinto del del expediente «{per_esp}» sin justificación")
            if ruta and ruta.endswith(".txt"):
                pag = _texto_pagina(ruta, f.get("pagina"))
                if pag is not None:
                    if _norm_txt(f.get("cita")) not in _norm_txt(pag):
                        return problema(k, "discrepancia", f"la cita no está en la página {f.get('pagina')} de {f.get('archivo')}")
                    if not _cita_contiene(f.get("cita"), vf):
                        return problema(k, "discrepancia", f"la cita no contiene el valor de la fuente {vf:g} como cifra completa")
        elif clase == "derivado":
            d = e.get("derivacion") if isinstance(e.get("derivacion"), dict) else {}
            if not d.get("origenes") or not d.get("formula") or not str(d.get("conciliacion") or "").strip():
                return problema(k, "pendiente", "derivado sin orígenes, fórmula o conciliación")
            vals = {}
            for o in d["origenes"]:
                if o not in por_celda:
                    return problema(k, "pendiente", f"el origen {o} no tiene entrada en el registro")
                if o not in estado:
                    revisar_una(o, por_celda[o])
                if estado.get(o) != "comprobada":
                    return problema(k, "pendiente", f"el origen {o} no está comprobado ({estado.get(o)})")
                vals[o] = por_celda[o].get("valor_modelo") if o.startswith("aux:") else inst["celdas"].get(o)
            try:
                r = _eval_formula(d["formula"], vals)
            except Exception as ex:  # noqa: BLE001
                return problema(k, "error", f"fórmula no evaluable ({type(ex).__name__}: {str(ex)[:80]})")
            vm = e.get("valor_modelo") if k.startswith("aux:") else inst["celdas"].get(k)
            if not _igual(r, vm):
                return problema(k, "discrepancia", f"la fórmula da {r:g} y el modelo {vm!r}")
        elif clase in ("dato_ausente", "no_aplicable"):
            if not str(e.get("justificacion") or "").strip():
                return problema(k, "pendiente", f"{clase} sin justificación")
            if clase == "dato_ausente" and _num(inst["celdas"].get(k)) and not k.startswith("aux:"):
                return problema(k, "error", "dato ausente con un valor en el libro: es un dato (o un cero) que hay que contrastar")
        return revisar_comprobacion(k, e)

    def revisar_comprobacion(k, e):
        clase = e.get("clase")
        c = e.get("comprobacion") if isinstance(e.get("comprobacion"), dict) else {}
        if clase in ("hipotesis", "convencion") and c.get("resultado") == "discrepancia":
            # (14-nov-2026, hallazgo del revisor RD) una hipótesis o convención no exige revisor, pero si un revisor registra una
            # discrepancia (p. ej. su fundamento ya no describe el dato vigente), cuenta: antes se ignoraba y el registro salía «apto»
            return problema(k, "discrepancia", f"el revisor registra una discrepancia en la {clase}: {str(c.get('nota') or e.get('incidencia') or '')[:120]}")
        if clase in ("hipotesis", "convencion") and c.get("resultado") == "pendiente":
            # (14-nov-2026, hallazgo de la orquestación) una hipótesis o convención cuyo registro queda explícitamente «pendiente»
            # (p. ej. texto sustituido a la espera de la confirmación del revisor) no está comprobada: antes contaba como comprobada
            return problema(k, "pendiente", f"la {clase} tiene la comprobación pendiente: {str(c.get('nota') or '')[:120]}")
        if clase not in ("hipotesis", "convencion"):
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
        estado[k] = "comprobada"

    for k, e in por_celda.items():
        if k not in estado:
            revisar_una(k, e)
    out["comprobadas"] = sorted(k for k, v in estado.items() if v == "comprobada")
    # (14-nov-2026, aviso de la auditoría) «comprobadas» incluye los datos de origen auxiliares; la cobertura del universo se cuenta aparte
    out["comprobadas_universo"] = sum(1 for k in inst["celdas"] if estado.get(k) == "comprobada")
    for k in out["sin_entrada"]:
        out["pendientes"].append(f"{k}: sin entrada en el registro")
    mat_no = [k for k in inst["celdas"] if (por_celda.get(k) or {}).get("material", True) is not False
              and (por_celda.get(k) or {}).get("clase") not in ("hipotesis", "convencion") and estado.get(k) != "comprobada"]
    # (14-nov-2026) una hipótesis o convención material con la comprobación explícitamente pendiente también bloquea
    mat_no += [k for k in inst["celdas"] if (por_celda.get(k) or {}).get("material", True) is not False
               and (por_celda.get(k) or {}).get("clase") in ("hipotesis", "convencion")
               and ((por_celda.get(k) or {}).get("comprobacion") or {}).get("resultado") == "pendiente"]
    out["materiales_no_comprobadas"] = mat_no
    bloqueos = out["sin_entrada"] or out["sobrantes"] or out["repetidas"] or out["errores"] or out["desactualizadas"] or out["discrepancias"] or mat_no
    out["apto_por_entradas"] = not bloqueos
    if bloqueos:
        out["motivo"] = (f"{out['comprobadas_universo']} de {inst['n']} celdas del universo comprobadas (+{out['auxiliares']} datos de origen auxiliares); "
                         f"{len(mat_no)} entradas materiales sin comprobar; {len(out['desactualizadas'])} desactualizadas; {len(out['discrepancias'])} discrepancias; "
                         f"{len(out['errores'])} errores del contrato; {len(out['sin_entrada'])} sin entrada")
    return out


def aptitud(carpeta):
    """(apto_por_entradas, resumen) para la ficha y el informe."""
    r = comprobar(carpeta)
    return r["apto_por_entradas"], {"universo": r["universo"], "comprobadas": len(r["comprobadas"]), "comprobadas_universo": r.get("comprobadas_universo"), "auxiliares": r["auxiliares"],
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
        ents.append({"celda": k, "id": inst["ids"].get(k), "uso": None, "material": True,
                     "clase": "hipotesis" if t == "hipótesis" else None, "valor_modelo": v, "fuente": {}, "derivacion": None, "hipotesis": None,
                     "justificacion": None, "comprobacion": {"extractor": None, "revisor": None, "fecha": None, "resultado": "pendiente", "fuente_examinada": None, "nota": None},
                     "incidencia": None})
    d = {"formato": FORMATO, "empresa": os.path.basename(os.path.abspath(carpeta)), "libro": os.path.basename(libro_de(carpeta)),
         "huella_entradas_economicas": inst["huella"], "perimetro_del_expediente": None, "entradas": ents}
    json.dump(d, open(os.path.join(carpeta, "verificacion_entradas.plantilla.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    return d


if __name__ == "__main__":
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
    sys.exit(0 if r["apto_por_entradas"] else 1)
