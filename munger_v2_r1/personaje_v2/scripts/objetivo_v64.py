#!/usr/bin/env python3
"""Materialidad y precio objetivo en la capa experimental V6.4 (encargo 4.12 §4). No escribe nada.

Solo se aplica a expedientes V6.4 en modo EXPERIMENTAL (plantilla_activa.json y configuracion_economica.json con modo
«Experimental»). En la V6.3 y en el modo heredado de la V6.4 rigen sin cambios las reglas vigentes (S-19, D10 y Anexo B §B.6.7).

Separa cinco cosas que la 4.11 mezclaba en `material_para_conclusion`:
  1. dato ausente material: S-19 (`revision_datos_ausentes`), que sigue mandando → pendiente_de_datos;
  2. hipótesis económica sin fundamento suficiente: los parámetros de la configuración con `fundamento_suficiente = false` y la
     lista D10 (`fundamento_material.hipotesis_sin_fundamento`). Una hipótesis incierta NO se convierte en un dato ausente;
  3. materialidad para la acción (`material_para_accion`: true · false · null = no determinada porque ninguna variante calculada
     varía el parámetro);
  4. materialidad para el objetivo (`material_para_objetivo`);
  5. ámbito: las variantes calculadas de configuracion_v64_variantes.json (y la comprobación conjunta, si se ejecutó) que respaldan
     cada afirmación. «La acción se sostiene» y el rango del precio de Sí solo valen para ese ámbito: no son un intervalo de
     confianza, no miden toda la incertidumbre económica y no cubren las hipótesis no exploradas.

Protocolo EXPERIMENTAL del objetivo (configuracion_economica.json → `protocolo_objetivo`; ensayo, no adopción). Solo actúa cuando
la conclusión provisional es «esperar» por precio (zona por encima del precio de Sí) y algo condiciona el objetivo:
  - `bloqueo_del_objetivo`: el objetivo no se emite; el expediente queda pendiente_de_datos (cubo Vigilar, acción null), la lectura
    S-19 del objetivo que depende de información material no disponible, con diagnóstico;
  - `objetivo_condicionado`: si la acción se sostiene en TODO el ámbito calculado, concluido · esperar con el objetivo emitido como
    condicionado (provisional), con las hipótesis que lo condicionan, el rango calculado y sus límites; si no se sostiene,
    pendiente_de_investigacion (la acción misma depende de hipótesis sin fundamento suficiente);
  - sin protocolo: no se emite ningún objetivo oficial; el pipeline termina en no_entregable · límite del modelo y el diagnóstico
    explica las dos lecturas.
La compra no se exime de nada: con «comprar», D10 cubre también los parámetros experimentales sin fundamento suficiente (pipeline,
coherencia_v64).

(4.13 §5) Contrato de cobertura por hipótesis (variantes con formato «4.13»). Para cada parámetro activo, `cobertura()` dice de forma
mecánica con qué se contrastó:
  - contraste_aislado: alguna variante calculada lo varía SOLO a él;
  - variacion_conjunta_necesaria: solo se puede variar junto con parámetros que la propia configuración liga a él (SR2 ↔ ROIC × f;
    N1 ↔ su escudo; R0 ↔ sin P-M1, porque R0 + P-M1 no está especificado). No queda «sin cobertura» por cambiar a la vez dos campos
    que no pueden cambiar por separado;
  - variacion_conjunta: solo lo varían variantes que cambian además otros parámetros no ligados (p. ej. «heredado» o «activa sin
    P-M1», que quitan P-M1 entera): no demuestran su efecto aislado;
  - sin_cobertura: ninguna variante calculada lo varía.
La fase C declara para cada parámetro la base de su materialidad para la acción: «calculada» (solo con contraste aislado o variación
conjunta necesaria), «juicio_economico» (con su evidencia: se presenta como juicio, no como constatación calculada) o «no_determinada»
(material_para_accion = null; no se convierte en false). La invariancia de la acción en las variantes calculadas se informa aparte
(`accion_invariante_en_variantes_calculadas`): no es la materialidad de un parámetro que esas variantes no identifican. No hay umbral
de fundamento suficiente: se exigen evidencia, hechos e inferencias separados y la revisión de las discrepancias con la clase y la
confianza que declara la configuración (`discrepancias_con_la_configuracion`).
"""
import json
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import configuracion_economica as CE  # noqa: E402
import seleccion_plantilla as SEL  # noqa: E402

PROTOCOLOS = CE.PROTOCOLOS
# lo que la zona de la escalera dice de la acción: por encima del precio de Sí no se compra por precio; por debajo, la regla se cumple
CLASE_ZONA = {"caro": "por_encima_del_precio_de_si", "vigilar": "por_encima_del_precio_de_si",
              "cumple_regla_k": "cumple_la_regla", "bajo_malo": "cumple_la_regla"}
TRATAMIENTOS = ("objetivo_emitido", "objetivo_condicionado", "objetivo_bloqueado", "objetivo_sin_protocolo", "sin_objetivo")
ORIGENES_BLOQUEO = ("protocolo_de_bloqueo", "accion_no_sostenida_en_el_ambito")
# (4.13, R3) además, «no_emitido_estado_final» cuando el estado de la salida no es el del tratamiento (bloque_ficha)
ESTADO_DEL_OBJETIVO = {"objetivo_emitido": "emitido", "objetivo_condicionado": "emitido_condicionado", "objetivo_bloqueado": "bloqueado",
                       "objetivo_sin_protocolo": "no_emitido_falta_protocolo", "sin_objetivo": "no_aplica"}
NATURALEZA_RANGO = ("rango de una tabla de sensibilidad: solo las variantes calculadas (y la comprobación conjunta, si se ejecutó); no es "
                    "un intervalo de confianza ni una medida completa de la incertidumbre económica, y no cubre las hipótesis no exploradas")
NOTA = "protocolo experimental del objetivo (encargo 4.12 §4): se ensaya en copias; no está adoptado como regla general"
# (4.13 §5) tipos de cobertura (de más a menos identificada) y bases de la materialidad para la acción
TIPOS_COBERTURA = ("contraste_aislado", "variacion_conjunta_necesaria", "variacion_conjunta", "sin_cobertura")
BASES_MATERIALIDAD = ("calculada", "juicio_economico", "no_determinada")
FORMATO_COBERTURA = "4.13"


def vinculados_necesarios(conf, clave):
    """(4.13 §5) Parámetros que la configuración obliga a cambiar junto con `clave` para que su alternativa esté definida."""
    act = set(CE.activos(conf or {}))
    pm = (conf or {}).get("PM1") or {}
    if clave == "PM1.estructura":
        return {"PM1.roic_terminal"}  # SR2 ↔ ROIC × f (validar lo exige)
    if clave == "PM1.roic_terminal":
        return {"PM1.estructura"}
    if clave == "N1.tipo":
        return {"N1.escudo"}  # sin N1 el escudo no existe
    if clave == "N3.regla":
        # R0 + P-M1 no está especificado (validar lo rechaza): R0 solo se calcula sin requisito adicional ni P0; R1 lleva su circulante
        ligados = {"N3.circulante"}
        if pm.get("estructura") in CE.ESTRUCTURAS[1:] or pm.get("cartera") == CE.CARTERA[1]:
            ligados |= {k for k in act if k.startswith("PM1.")}
        return ligados
    return set()


def cobertura(var, clave, conf=None, ccj=None, clase_activa=None):
    """(4.13 §5) {tipo, aisladas, conjuntas_necesarias, conjuntas, comprobacion_conjunta, accion_invariante_en_variantes_calculadas,
    accion_invariante_en_contrastes}. None si las variantes no traen parametros_variados (formato 4.11)."""
    vs = [v for v in (var or {}).get("variantes") or [] if v.get("clave") != "activa" and v.get("zona")]
    if vs and any("parametros_variados" not in v for v in (var or {}).get("variantes") or [] if v.get("clave") != "activa"):
        return None
    lig = vinculados_necesarios(conf, clave)
    ais, nec, con = [], [], []
    for v in vs:
        pv = set(v.get("parametros_variados") or [])
        if clave not in pv:
            continue
        if pv == {clave}:
            ais.append(v["clave"])
        elif pv <= {clave} | lig:
            nec.append(v["clave"])
        else:
            con.append(v["clave"])
    en_cc = False
    if ccj:
        comb = (ccj.get("combinacion") or {})
        en_cc = any(clave_de_celda(k, conf) == clave for k in comb) or any(a.get("clave") == clave and a.get("zona") for a in ccj.get("por_alternativa") or [])
    tipo = TIPOS_COBERTURA[0] if ais else TIPOS_COBERTURA[1] if nec else TIPOS_COBERTURA[2] if (con or en_cc) else TIPOS_COBERTURA[3]
    zonas = {v["clave"]: v.get("zona") for v in vs}

    def inv(claves):
        if not claves or clase_activa is None:
            return None
        return all(CLASE_ZONA.get(zonas.get(k)) == clase_activa for k in claves)
    return {"tipo": tipo, "aisladas": ais, "conjuntas_necesarias": nec, "conjuntas": con, "comprobacion_conjunta": en_cc,
            "vinculados_necesarios": sorted(lig),
            "accion_invariante_en_variantes_calculadas": inv(ais + nec + con), "accion_invariante_en_contrastes": inv(ais + nec)}


# ---------- (4.14, encargo de cierre §5; S3 y S11 de la segunda revisión interna 4.13) juicio propio sobre el OBJETIVO ----------
# Con el contrato 4.14 (lo fija el PIPELINE en estado_pipeline.json → contrato_juicio_objetivo al generar el prompt de la fase C, nunca un
# campo que escriba el agente), cada parámetro activo lleva `juicio_objetivo`, separado del juicio sobre la acción: hipótesis, contraste
# mecánico (referencia, alternativas y cambio en € y %), cobertura, límites, base, material, criterio (de dónde sale la línea entre
# material y no material), comparación declarada y razonamiento y evidencia propios. La validación comprueba el CONTRATO y su COHERENCIA,
# no la pertinencia económica (eso es de la auditoría): un campo de texto no vacío no acredita fundamento. No hay umbral: un criterio
# propio del agente (p. ej., 1,5 €) se representa como juicio suyo, nunca como política; una política solo cuenta si está registrada con
# decisión, fecha y firma humana. Diseño y parche de origen: frente B (agentes/B/materialidad_objetivo_diseno.md, juicio_objetivo_414.py).
FORMATO_JUICIO_OBJETIVO = "4.14"
ORIGENES_CRITERIO = ("ninguno", "redondeo_declarado", "juicio_propio_del_agente", "politica_adoptada")
COMPARADORES = ("rango_calculado", "resolucion_de_las_palancas", "otra_hipotesis_calculada", "otro_declarado")


def contraste_objetivo(var, cb, psi_activa):
    """Alternativas calculadas que contrastan un parámetro para el objetivo, con Δ € y Δ % del precio de Sí frente a la activa. Solo son
    atribuibles al parámetro los contrastes aislados y las variaciones conjuntas necesarias; las conjuntas se informan como no atribuibles."""
    vs = {v.get("clave"): v for v in (var or {}).get("variantes") or []}
    out = []
    for grupo, atrib in (("aisladas", True), ("conjuntas_necesarias", True), ("conjuntas", False)):
        for c in (cb or {}).get(grupo) or []:
            v = vs.get(c) or {}
            ps = v.get("precio_si")
            d = (ps - psi_activa) if _num(ps) and _num(psi_activa) else None
            out.append({"variante": c, "descripcion": v.get("descripcion") or v.get("configuracion"), "precio_si": ps, "delta_eur": d,
                        "delta_pct": (d / psi_activa) if d is not None and psi_activa else None, "atribuible": atrib})
    return out


def escribir_contraste_objetivo(carpeta):
    """(4.14) contraste_objetivo_v64.md (y .json): para cada parámetro activo, la cobertura mecánica y las alternativas calculadas con su
    precio de Sí y el cambio en € y % frente a la activa, que la fase C copia en juicio_objetivo.contraste. No es material auditado: se
    deriva de configuracion_v64_variantes.json y de precio.json, que sí lo son."""
    var = _cargar(carpeta, "configuracion_v64_variantes.json") or {}
    conf = SEL.configuracion(carpeta) or {}
    psi = (_cargar(carpeta, "precio.json") or {}).get("precio_si")
    filas, js = [], {}
    for k in CE.activos(conf):
        if k == "modo":
            continue
        cb = cobertura(var, k, conf)
        cs = contraste_objetivo(var, cb, psi)
        js[k] = {"cobertura": (cb or {}).get("tipo"), "contraste": cs}
        for c in cs or [None]:
            if c is None:
                filas.append(f"| {k} | {(cb or {}).get('tipo')} | — | — | — | — | — |")
            else:
                f = lambda x, n=2: f"{x:+.{n}f}" if _num(x) else "—"  # noqa: E731
                filas.append(f"| {k} | {(cb or {}).get('tipo')} | {c['variante']} | {format(c['precio_si'], '.4f') if _num(c['precio_si']) else '—'} | {f(c['delta_eur'])} | "
                             f"{f((c['delta_pct'] or 0) * 100, 2) + ' %' if _num(c['delta_pct']) else '—'} | {'sí' if c['atribuible'] else 'no (varía otros parámetros)'} |")
    json.dump({"formato": FORMATO_JUICIO_OBJETIVO, "precio_si_activa": psi, "por_parametro": js}, open(os.path.join(carpeta, "contraste_objetivo_v64.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    md = ["# Contraste mecánico para el juicio sobre el objetivo (contrato 4.14)", "",
          f"Precio de Sí de la activa: {psi}. Copia en `juicio_objetivo.contraste` exactamente estas filas de cada parámetro (variante, delta_eur y atribuible). "
          "Solo son atribuibles al parámetro los contrastes aislados y las variaciones conjuntas necesarias. Sin contraste, el cambio no está definido (no es 0).", "",
          "| Parámetro | Cobertura | Variante | Precio de Sí | Δ € | Δ % | Atribuible |", "|---|---|---|---|---|---|---|"] + filas
    open(os.path.join(carpeta, "contraste_objetivo_v64.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")


def amplitud_rango(var):
    vals = [v.get("precio_si") for v in (var or {}).get("variantes") or [] if _num(v.get("precio_si")) and v.get("zona")]
    return (max(vals) - min(vals)) if vals else None


def validar_juicio_objetivo(k, p, cb, var, psi_activa, politicas=None):
    """None si el bloque `juicio_objetivo` del parámetro `k` cumple el contrato 4.14; si no, el motivo. Reglas V1–V8 del diseño."""
    pref = f"configuracion_v64.parametros[{k}].juicio_objetivo"
    j = p.get("juicio_objetivo")
    if not isinstance(j, dict):
        return f"{pref}: obligatorio con el contrato {FORMATO_JUICIO_OBJETIVO} (juicio sobre el objetivo separado del de la acción; encargo de cierre §5)"
    base, mat = j.get("base"), j.get("material")
    if base not in BASES_MATERIALIDAD:
        return f"{pref}.base: una de {BASES_MATERIALIDAD}"
    if mat not in (True, False, None) or (base == "no_determinada") != (mat is None):
        return f"{pref}: material = null si y solo si base = «no_determinada» (lo no determinado no se convierte en false)"
    if p.get("material_para_objetivo", mat) != mat or p.get("base_de_la_materialidad_objetivo", base) != base:  # V1: los campos 4.13 se derivan
        return f"{pref}: material_para_objetivo y base_de_la_materialidad_objetivo tienen que coincidir con el bloque (se derivan de él)"
    if not str(j.get("hipotesis") or "").strip():
        return f"{pref}.hipotesis: obligatoria (qué afirmación sobre el objetivo se contrasta)"
    calc = contraste_objetivo(var, cb, psi_activa)  # V3: lo declarado tiene que ser lo calculado
    decl = {c.get("variante"): c for c in j.get("contraste") or [] if isinstance(c, dict)}
    if sorted(decl) != sorted(c["variante"] for c in calc):
        return f"{pref}.contraste: tiene que listar exactamente las variantes calculadas que varían {k}: {[c['variante'] for c in calc] or 'ninguna'}"
    for c in calc:
        d = decl[c["variante"]]
        if c["delta_eur"] is not None and (not _num(d.get("delta_eur")) or round(d["delta_eur"], 2) != round(c["delta_eur"], 2)):
            return f"{pref}.contraste[{c['variante']}].delta_eur {d.get('delta_eur')!r} no es el calculado {c['delta_eur']:.2f} (dos decimales; si las variantes se recalcularon, hay que volver a juzgar)"
        if d.get("atribuible") is not c["atribuible"]:
            return f"{pref}.contraste[{c['variante']}].atribuible = {c['atribuible']} (lo fija el tipo de cobertura, no el agente)"
    if j.get("cobertura") != (cb or {}).get("tipo"):
        return f"{pref}.cobertura {j.get('cobertura')!r} no es la mecánica: {(cb or {}).get('tipo')!r}"
    if not [x for x in j.get("limites") or [] if isinstance(x, str) and x.strip()]:
        return f"{pref}.limites: lista no vacía (qué no cubre el contraste: hipótesis no calculadas, dominio, familia, perímetro, interacciones…)"
    for campo in ("evidencia", "razonamiento"):
        if base != "no_determinada" and not (isinstance(j.get(campo), list) and [x for x in j[campo] if isinstance(x, str) and x.strip()]):
            return f"{pref}.{campo}: lista no vacía con base {base!r} (razonamiento y evidencia propios del objetivo)"
    crit = j.get("criterio") if isinstance(j.get("criterio"), dict) else None
    if not crit or crit.get("origen") not in ORIGENES_CRITERIO:
        return f"{pref}.criterio.origen: uno de {ORIGENES_CRITERIO} (de dónde sale la línea que separa material de no material)"
    atrib = [c for c in calc if c["atribuible"] and c["delta_eur"] is not None]
    mueve = [c for c in atrib if round(c["delta_eur"], 2) != 0]
    if base == "calculada":  # V4
        if (cb or {}).get("tipo") not in TIPOS_COBERTURA[:2] or not atrib:
            return f"{pref}: «calculada» exige un contraste aislado o una variación conjunta necesaria"
        if mat is False and mueve:
            return f"{pref}: «no material» calculada con contrastes que mueven el precio de Sí ({', '.join(c['variante'] for c in mueve)}): que no sea material es un juicio"
        if mat is True and crit.get("origen") not in ("redondeo_declarado", "politica_adoptada"):
            return (f"{pref}: «material» calculada con el criterio {crit.get('origen')!r}: solo con el redondeo declarado o una política adoptada; "
                    "con un criterio propio del agente la base es «juicio_economico» (S11)")
        if mat is True and crit.get("origen") == "redondeo_declarado" and not mueve:
            return f"{pref}: «material» por el redondeo declarado sin ningún contraste que mueva el precio de Sí"
    if crit.get("origen") == "politica_adoptada":  # V7: no se inventan adopciones
        pol = (politicas or {}).get(crit.get("referencia")) if isinstance(politicas, dict) else None
        if not isinstance(pol, dict) or not all(str(pol.get(c) or "").strip() for c in ("decision", "fecha", "decidido_por")):
            return f"{pref}.criterio: la política {crit.get('referencia')!r} no está registrada con decisión, fecha y firma humana"
    if crit.get("origen") == "juicio_propio_del_agente":  # V5 (S11)
        if base == "calculada":
            return f"{pref}: un criterio propio del agente es un juicio: base «juicio_economico», no «calculada» (S11)"
        if not str(crit.get("descripcion") or "").strip():
            return f"{pref}.criterio.descripcion: obligatoria con un criterio propio (se muestra como juicio del agente, no como política)"
    # V6 (S3): «no material» por juicio de un parámetro SIN fundamento suficiente cuyo contraste mueve el objetivo (o sin contraste atribuible)
    # exige declarar con qué se compara ese movimiento; sin comparación, la materialidad queda no determinada y condiciona el objetivo
    if base == "juicio_economico" and mat is False and p.get("fundamento_suficiente") is False and (mueve or not atrib):
        comp = j.get("comparado_con") if isinstance(j.get("comparado_con"), dict) else None
        if not comp or comp.get("referencia") not in COMPARADORES or not _num(comp.get("valor_eur")) or not str(comp.get("fuente") or "").strip():
            return (f"{pref}: «no material» por juicio de un parámetro sin fundamento suficiente "
                    + ("cuyo contraste mueve el precio de Sí " if mueve else "sin contraste atribuible ")
                    + f"exige comparado_con {{referencia ∈ {COMPARADORES}, valor_eur, fuente}}; sin esa comparación la base es «no_determinada» (y condiciona el objetivo)")
        if comp["referencia"] == "rango_calculado":
            amp = amplitud_rango(var)
            if amp is not None and round(comp["valor_eur"], 2) != round(amp, 2):
                return f"{pref}.comparado_con.valor_eur {comp['valor_eur']} no es la amplitud del rango calculado {amp:.2f}"
    return None


def discrepancias_con_la_configuracion(conf, p):
    """(4.13 §5; R5 de la revisión 4.12) Discrepancias entre la clase y la confianza que la configuración declara para un parámetro
    (trazabilidad) y el juicio de la fase C. No se resuelven con un umbral: la fase C tiene que revisarlas y decir cómo las resuelve."""
    t = (((conf or {}).get("trazabilidad") or {}).get(p.get("clave")) or {})
    out = []
    fs = p.get("fundamento_suficiente")
    if t.get("clase") == "hipótesis" and fs is True:
        out.append("hipotesis_en_la_configuracion_con_fundamento_suficiente")
    if t.get("confianza") == "baja" and fs is True:
        out.append("confianza_baja_en_la_configuracion_con_fundamento_suficiente")
    if t.get("clase") in ("dato publicado", "derivado de datos publicados") and fs is False:
        out.append("dato_en_la_configuracion_sin_fundamento_suficiente")
    if t.get("confianza") and p.get("confianza") and t.get("confianza") != p.get("confianza"):
        out.append("confianza_distinta")
    return out


def _cargar(c, n):
    p = os.path.join(c, n)
    try:
        return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else None
    except (OSError, ValueError):
        return None


def _num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def aplica(carpeta):
    return SEL.leer(carpeta) is not None and SEL.experimental(carpeta)


def _celdas_norm(celda):
    """Celdas sueltas de una referencia de D10 o de la combinación: «B69:D69» → {B69, C69, D69}; sin el prefijo «Análisis!»."""
    out = set()
    for parte in re.split(r"[;,\s]+", str(celda or "")):
        if not parte:
            continue
        hoja, ref = (parte.split("!", 1) if "!" in parte else ("Análisis", parte))
        pref = "" if hoja == "Análisis" else hoja + "!"
        m = re.fullmatch(r"([A-Z]{1,2})(\d{1,3}):([A-Z]{1,2})(\d{1,3})", ref)
        if m and m.group(2) == m.group(4) and len(m.group(1)) == 1 and len(m.group(3)) == 1:
            for col in range(ord(m.group(1)), ord(m.group(3)) + 1):
                out.add(f"{pref}{chr(col)}{m.group(2)}")
        else:
            out.add(pref + ref)
    return out


def clave_de_celda(celda, conf):
    """Clave de parámetro de la configuración si `celda` (de D10 o de la combinación) es su celda principal; si no, None."""
    if not conf or not str(celda or "").startswith(CE.HOJA + "!"):
        return None
    for k in CE.TRAZA_CELDAS:
        if CE.celda_principal(k, conf) == celda:
            return k
    return None


def condicionantes(fc, conf):
    """Hipótesis que condicionan el objetivo, en orden: los parámetros con material_para_objetivo = true y fundamento_suficiente =
    false, y toda la lista D10 (Anexo B §B.6.7: con esperar, cualquier hipótesis sin fundamento condiciona el objetivo). Una entrada
    D10 que es la celda principal de un parámetro se nombra con la clave del parámetro (sin duplicarla)."""
    cv = (fc or {}).get("configuracion_v64") or {}
    out = []
    for p in cv.get("parametros") or []:
        # (4.13, revisión interna R4) también la materialidad para el objetivo «no determinada» (null): sin fundamento suficiente y sin
        # saber si mueve el objetivo, lo condiciona (no se convierte en «no material»)
        # (4.14) con el bloque juicio_objetivo, su «material» manda (los campos 4.13 se derivan de él y la coherencia exige que coincidan)
        j = p.get("juicio_objetivo") if isinstance(p.get("juicio_objetivo"), dict) else None
        mpo, tiene = (j.get("material"), True) if j is not None and "material" in j else (p.get("material_para_objetivo"), "material_para_objetivo" in p)
        if mpo in (True, None) and tiene and p.get("fundamento_suficiente") is False and p.get("clave") not in out:
            out.append(p.get("clave"))
    for h in ((fc or {}).get("fundamento_material") or {}).get("hipotesis_sin_fundamento") or []:
        k = clave_de_celda(h.get("celda"), conf) or h.get("celda")
        if k not in out:
            out.append(k)
    # (4.12 §5) un aviso de dominio que la fase C declara material condiciona el objetivo como límite del modelo
    for a in (cv.get("avisos_de_dominio") or []) + (cv.get("avisos_de_dominio_variantes") or []):
        # (4.13 §5) también los avisos de las variantes calculadas que la fase C declara materiales
        if isinstance(a, dict) and a.get("material_para_conclusion") is True and f"limite:{a.get('id')}" not in out:
            out.append(f"limite:{a.get('id')}")
    return out


def escenarios(var, ccj, conf):
    """Escenarios calculados y válidos (con zona) del ámbito, sin la variante «activa» (es la referencia): las variantes de la
    configuración y, si se ejecutó, la comprobación conjunta y cada alternativa no numérica que recalculó."""
    out = []
    for v in (var or {}).get("variantes") or []:
        if v.get("clave") == "activa" or not v.get("zona"):
            continue
        out.append({"clave": v.get("clave"), "origen": "variante", "zona": v.get("zona"), "precio_si": v.get("precio_si"),
                    "ponderado": v.get("ponderado"), "varia": list(v.get("parametros_variados") or [])})
    if ccj and (ccj.get("escalera_bajo_combinacion") or {}).get("zona"):
        comb = ccj.get("combinacion") or {}
        varia = sorted({clave_de_celda(k, conf) or k for k in comb})
        eb = ccj["escalera_bajo_combinacion"]
        out.append({"clave": "comprobacion_conjunta", "origen": "comprobacion_conjunta", "zona": eb.get("zona"), "precio_si": eb.get("precio_si"),
                    "ponderado": eb.get("ponderado"), "varia": varia})
        for a in ccj.get("por_alternativa") or []:
            if a.get("zona"):
                out.append({"clave": f"comprobacion_conjunta · {a.get('clave')} = {a.get('alternativa')}", "origen": "comprobacion_conjunta_alternativa",
                            "zona": a.get("zona"), "precio_si": a.get("precio_si"), "ponderado": a.get("ponderado"), "varia": varia + [a.get("clave")]})
    return out


def ambito_parametro(var, clave):
    """Variantes calculadas (con zona, sin la activa) que varían el parámetro `clave`; None si las variantes no traen
    `parametros_variados` (formato 4.11: el ámbito no se puede determinar)."""
    vs = [v for v in (var or {}).get("variantes") or [] if v.get("clave") != "activa"]
    if vs and any("parametros_variados" not in v for v in vs):
        return None
    return [v.get("clave") for v in vs if v.get("zona") and clave in (v.get("parametros_variados") or [])]


def ambito_aislado(var, clave):
    """Variantes calculadas que varían SOLO ese parámetro (la estructura, con su ROIC terminal ligado): las demás del ámbito son
    variaciones conjuntas (p. ej. «heredado», que quita toda la configuración a la vez)."""
    propio = {clave} | ({"PM1.roic_terminal"} if clave == "PM1.estructura" else set())
    return [v.get("clave") for v in (var or {}).get("variantes") or [] if v.get("clave") != "activa" and v.get("zona")
            and clave in (v.get("parametros_variados") or []) and set(v.get("parametros_variados") or []) <= propio]


# (4.12, revisión interna R3) subparámetros de P-M1: «heredado», los componentes aislados de N1, N2 y R1 y «activa sin P-M1» quitan P-M1
# entera, así que los listan entre sus parámetros variados sin calcular ninguna alternativa suya (p. ej., la familia Θ con Λ activa)
SUBPARAMETROS_PM1 = ("PM1.familia", "PM1.parametro", "PM1.convencion_anios", "PM1.convencion_terminal", "PM1.roic_terminal", "PM1.cartera",
                     "PM1.perimetro")  # (4.13 §7) V6.4.1


def cubiertas(H, esc, fc, var=None):
    """Del conjunto H, las hipótesis cuya alternativa refleja al menos un escenario calculado (las demás, «no cubiertas»: el rango no
    las refleja). Un subparámetro de P-M1 solo queda cubierto por una variante que lo varía de forma AISLADA (con P-M1 activa) o por la
    comprobación conjunta; quitar P-M1 entera no calcula ninguna alternativa del subparámetro (revisión interna R3)."""
    varia_param = set()
    varia_celdas = set()
    varia_cc = set()
    for e in esc:
        for x in e.get("varia") or []:
            varia_param.add(x)
            varia_celdas |= _celdas_norm(x)
            if str(e.get("origen") or "").startswith("comprobacion_conjunta"):
                varia_cc.add(x)
    out = []
    conf = (var or {}).get("_conf")
    for h in H:
        if (var or {}).get("formato") == FORMATO_COBERTURA and h in CE.FILAS_TRAZA:
            # (4.13 §5) un parámetro queda cubierto por un contraste aislado, por una variación conjunta necesaria o por la comprobación
            # conjunta; quitar la configuración entera no lo cubre
            cb = cobertura(var, h, conf)
            if cb and (cb["tipo"] in TIPOS_COBERTURA[:2] or h in varia_cc):
                out.append(h)
            continue
        if h in SUBPARAMETROS_PM1 and var is not None:
            if ambito_aislado(var, h) or h in varia_cc:
                out.append(h)
            continue
        if h in varia_param or (_celdas_norm(h) & varia_celdas):
            out.append(h)
    return out


def accion_evaluada(fc):
    """(4.13 §4) La acción que se evalúa es la de la DECISIÓN FINAL. La conclusión provisional es un antecedente: solo cuenta cuando
    la acción final es nula (el protocolo o la falta de sostén en el ámbito la dejan sin acción) y no puede eximir a la salida final de
    sus reglas. Hasta la 4.12 se priorizaba la provisional: con «descartar» o «comprar» provisional y una decisión final «esperar» con
    precio objetivo, el bloque decía «sin objetivo» mientras decision.precio_objetivo seguía emitido."""
    fc = fc if isinstance(fc, dict) else {}
    dec = fc.get("decision") if isinstance(fc.get("decision"), dict) else {}
    return dec.get("accion") if dec.get("accion") is not None else fc.get("conclusion_provisional")


def tratamiento(fc, precio, H, P, S, alguno_material):
    """(tratamiento, origen_del_bloqueo, motivo) que corresponde mecánicamente (sobre la acción final, 4.13 §4)."""
    acc = accion_evaluada(fc)
    clase = CLASE_ZONA.get((precio or {}).get("zona"))
    psi = (precio or {}).get("precio_si")
    if ((fc or {}).get("limite_del_modelo") or {}).get("aplica") or acc in ("descartar", "demasiado_dificil"):
        return "sin_objetivo", None, "la conclusión no tiene precio objetivo (límite del modelo o conclusión cualitativa)"
    if alguno_material:
        return "sin_objetivo", None, "un dato ausente material (S-19) deja el expediente pendiente_de_datos antes que cualquier protocolo"
    if acc == "comprar":
        return "sin_objetivo", None, "la compra no lleva precio objetivo y no se exime de D10 (incluidos los parámetros experimentales)"
    if not _num(psi) or clase != "por_encima_del_precio_de_si":
        return "sin_objetivo", None, "sin precio objetivo de precio: esperar por una condición que no es de precio, o sin escalera"
    if not H:
        return "objetivo_emitido", None, "ninguna hipótesis sin fundamento suficiente condiciona el objetivo"
    if P is None:
        return "objetivo_sin_protocolo", None, "el objetivo depende de hipótesis sin fundamento suficiente y la configuración no declara protocolo_objetivo"
    if P == "bloqueo_del_objetivo":
        return "objetivo_bloqueado", "protocolo_de_bloqueo", "protocolo de bloqueo: el objetivo depende de información material no disponible"
    if S:
        return "objetivo_condicionado", None, "presentación condicionada: la acción se sostiene en todo el ámbito calculado"
    return "objetivo_bloqueado", "accion_no_sostenida_en_el_ambito", "presentación condicionada sin acción sostenida en el ámbito calculado: la acción depende de hipótesis sin fundamento suficiente"


ESPERADO = {("objetivo_emitido", None): ("concluido", "esperar", "precio_si", "Vigilar"),
            ("objetivo_condicionado", None): ("concluido", "esperar", "precio_si", "Vigilar"),
            ("objetivo_bloqueado", "protocolo_de_bloqueo"): ("pendiente_de_datos", None, None, "Vigilar"),
            ("objetivo_bloqueado", "accion_no_sostenida_en_el_ambito"): ("pendiente_de_investigacion", None, None, "Vigilar"),
            # sin protocolo, la fase C cierra su análisis como siempre (esperar con el precio de Sí); el pipeline no lo entrega
            ("objetivo_sin_protocolo", None): ("concluido", "esperar", "precio_si", "Vigilar")}


def evaluar(carpeta, fc=None, precio=None, var=None, conf=None, ccj=None):
    """Lo que se comprueba de forma mecánica para el objetivo de un expediente V6.4 experimental; None si no aplica."""
    if not aplica(carpeta):
        return None
    fc = fc if fc is not None else (_cargar(carpeta, "fase_c.json") or {})
    precio = precio if precio is not None else (_cargar(carpeta, "precio.json") or {})
    var = var if var is not None else (_cargar(carpeta, "configuracion_v64_variantes.json") or {})
    conf = conf if conf is not None else (SEL.configuracion(carpeta) or {})
    ccj = ccj if ccj is not None else _cargar(carpeta, "comprobacion_conjunta.json")
    cv = fc.get("configuracion_v64") or {}
    P = conf.get("protocolo_objetivo")
    alguno = bool((fc.get("revision_datos_ausentes") or {}).get("alguno_material"))
    esc = escenarios(var, ccj, conf)
    H = condicionantes(fc, conf)
    acc = accion_evaluada(fc)  # (4.13 §4) la acción final; la provisional solo si la final es nula
    acc_prov = fc.get("conclusion_provisional")
    acc_fin = (fc.get("decision") or {}).get("accion") if isinstance(fc.get("decision"), dict) else None
    clase0 = CLASE_ZONA.get(precio.get("zona"))
    # ¿se sostiene la acción en el ámbito calculado? (solo comprar y esperar por precio dependen de la zona)
    motivos = []
    if acc in ("comprar", "esperar") and not (acc == "esperar" and clase0 == "cumple_la_regla"):
        if not esc:
            motivos.append("no hay ningún escenario calculado en el ámbito")
        motivos += [f"{e['clave']} (zona {e['zona']})" for e in esc if CLASE_ZONA.get(e["zona"]) != clase0]
        motivos += [f"{p.get('clave')} (la fase C lo declara material para la acción)" for p in cv.get("parametros") or []
                    if p.get("clave") in H and p.get("material_para_accion") is True]
    S = not motivos
    T, origen, motivo = tratamiento(fc, precio, H, P, S, alguno)
    est_e, acc_e, po_e, cubo_e = ESPERADO.get((T, origen), (None, None, None, None))
    psi = precio.get("precio_si")
    vals = [x for x in [psi] + [e.get("precio_si") for e in esc] if _num(x)]
    ponds = [x for x in [precio.get("ponderado")] + [e.get("ponderado") for e in esc] if _num(x)]
    cub = cubiertas(H, esc, fc, dict(var or {}, _conf=conf))
    params = {p.get("clave"): p for p in cv.get("parametros") or []}
    info = []
    avisos_fc = {f"limite:{a.get('id')}": a for a in (cv.get("avisos_de_dominio_variantes") or []) + (cv.get("avisos_de_dominio") or []) if isinstance(a, dict)}
    for h in H:
        txt = (params.get(h) or {}).get("informacion_que_falta") or ((f"límite del modelo: {avisos_fc[h].get('consecuencia')}") if h in avisos_fc else None)
        if not txt:
            for d in (fc.get("fundamento_material") or {}).get("hipotesis_sin_fundamento") or []:
                if (clave_de_celda(d.get("celda"), conf) or d.get("celda")) == h:
                    ad = d.get("alternativas_defendibles") or {}
                    # sin base, la evidencia dice qué haría falta (prompt de la fase C); con base, el motivo de que siga sin fundamento
                    txt = (ad.get("evidencia") if not ad.get("hay_base") else None) or d.get("porque_sin_fundamento")
                    break
        info.append({"hipotesis": h, "informacion_que_falta": txt})
    return {
        "aplica": True, "protocolo": P, "accion_provisional": acc_prov, "accion_final": acc_fin, "accion_evaluada": acc,
        "transicion": (f"{acc_prov} → {acc_fin}" if acc_prov != acc_fin else None), "zona_activa": precio.get("zona"), "valor_calculado_condicional": psi if _num(psi) else None,
        "hipotesis_que_condicionan": H, "hipotesis_no_cubiertas": [h for h in H if h not in cub],
        "informacion_por_hipotesis": info,
        "ambito": [e["clave"] for e in esc], "zonas_en_ambito": {e["clave"]: e["zona"] for e in esc},
        "accion_sostenida_en_ambito": S, "motivos_no_sostenida": motivos,
        "rango_calculado": {"precio_si": [min(vals), max(vals)] if vals else None, "ponderado": [min(ponds), max(ponds)] if ponds else None,
                            "n_escenarios": len(esc), "escenarios": [e["clave"] for e in esc], "zonas": sorted({e["zona"] for e in esc}),
                            "naturaleza": NATURALEZA_RANGO},
        "tratamiento": T, "origen_del_bloqueo": origen, "motivo_mecanico": motivo,
        "estado_esperado": est_e, "accion_esperada": acc_e, "precio_objetivo_esperado": (psi if po_e == "precio_si" else None) if est_e else None,
        "cubo_esperado": cubo_e,
        "ambito_por_parametro": {k: ambito_parametro(var, k) for k in CE.activos(conf) if k != "modo"},
        # (4.13 §5) cobertura de cada parámetro activo (solo con variantes de formato 4.13) y discrepancias con la configuración
        "contrato_cobertura": (var or {}).get("formato") == FORMATO_COBERTURA,
        "cobertura_por_parametro": ({k: cobertura(var, k, conf, ccj, clase0) for k in CE.activos(conf) if k != "modo"}
                                    if (var or {}).get("formato") == FORMATO_COBERTURA else None),
        "discrepancias_por_parametro": {p.get("clave"): discrepancias_con_la_configuracion(conf, p) for p in cv.get("parametros") or [] if isinstance(p, dict)},
        "variantes_sin_parametros_variados": any(ambito_parametro(var, k) is None for k in CE.activos(conf) if k != "modo"),
    }


def mismo_importe(a, b):
    """(4.13 §4) Igualdad con el redondeo declarado de las salidas (dos decimales), no con una tolerancia relativa."""
    return _num(a) and _num(b) and round(float(a), 2) == round(float(b), 2)


def contradicciones_salida(estado, decision, bloque, ev=None):
    """(4.13 §4) Contradicciones entre la acción final, el estado, el protocolo, el objetivo estructurado y el objetivo de la
    decisión. Lista vacía si no hay ninguna. La usan la coherencia de la fase C (pipeline), ficha.py, informe.py y resumen.py: una
    contradicción no puede llegar a un cierre oficial ni a material aparentemente listo para la auditoría."""
    dec = decision if isinstance(decision, dict) else {}
    acc, po = dec.get("accion"), dec.get("precio_objetivo")
    f = []
    if po is not None and not _num(po):
        f.append(f"decision.precio_objetivo {po!r} no es un número")
    if _num(po) and acc != "esperar":
        f.append(f"decision.precio_objetivo {po} con la acción {acc!r}: solo «esperar» lleva precio objetivo (una compra no lleva objetivo de espera)")
    if _num(po) and estado != "concluido":
        f.append(f"decision.precio_objetivo {po} con el estado {estado!r}: un objetivo solo se emite en un análisis concluido")
    if isinstance(bloque, dict):
        eo, em = bloque.get("estado_del_objetivo"), bloque.get("precio_objetivo_emitido")
        if eo in ("emitido", "emitido_condicionado"):
            if not mismo_importe(po, em):
                f.append(f"objetivo {eo} {em} y decision.precio_objetivo {po}: tienen que coincidir (dos decimales)")
        elif _num(po):
            f.append(f"el objetivo estructurado dice {eo!r} ({bloque.get('tratamiento')}) y decision.precio_objetivo conserva {po}")
        if eo == "bloqueado" and (acc is not None or estado not in ("pendiente_de_datos", "pendiente_de_investigacion")):
            f.append(f"objetivo bloqueado con acción {acc!r} y estado {estado!r}: un objetivo bloqueado deja la acción nula y el análisis pendiente")
        if bloque.get("provisional") and eo != "emitido_condicionado":
            f.append("objetivo marcado provisional sin estar emitido como condicionado")
    if isinstance(ev, dict) and ev.get("estado_esperado"):
        if estado != ev["estado_esperado"] or acc != ev["accion_esperada"] or not ((po is None and ev["precio_objetivo_esperado"] is None) or mismo_importe(po, ev["precio_objetivo_esperado"])):
            f.append(f"con el tratamiento {ev['tratamiento']} (acción evaluada {ev.get('accion_evaluada')!r}) corresponden estado {ev['estado_esperado']}, acción "
                     f"{ev['accion_esperada']} y objetivo {ev['precio_objetivo_esperado']}; la salida tiene {estado}, {acc} y {po}")
    elif isinstance(ev, dict) and ev.get("tratamiento") == "sin_objetivo" and _num(po):
        f.append(f"sin objetivo ({ev.get('motivo_mecanico')}) y decision.precio_objetivo {po}")
    return f


def lecturas_sin_protocolo(ev):
    """Las dos lecturas posibles cuando falta el protocolo (se explican; ninguna se elige)."""
    r = ev.get("rango_calculado") or {}
    rg = r.get("precio_si")
    return {"bloqueo_del_objetivo": "pendiente_de_datos · cubo Vigilar · sin acción ni objetivo (el objetivo depende de información material no disponible)",
            "objetivo_condicionado": (f"concluido · esperar · objetivo {ev.get('valor_calculado_condicional'):.2f} condicionado a {', '.join(ev.get('hipotesis_que_condicionan') or [])}"
                                      + (f" · rango calculado del precio de Sí {rg[0]:.2f}–{rg[1]:.2f} en la activa y {r.get('n_escenarios')} escenarios calculados" if rg else "")
                                      if ev.get("accion_sostenida_en_ambito") and _num(ev.get("valor_calculado_condicional")) else
                                      "pendiente_de_investigacion · cubo Vigilar (la acción no se sostiene en el ámbito calculado)")}


def bloque_ficha(carpeta, fc, precio, estado, decision, var=None, conf=None, ccj=None):
    """ficha.json → `objetivo` (solo V6.4 experimental; None si no aplica). Estructurado y trazable: el lector no tiene que buscar la
    palabra «provisional» en un párrafo. `decision.precio_objetivo` sigue siendo el objetivo emitido (compatibilidad)."""
    if not isinstance(((fc or {}).get("configuracion_v64") or {}).get("objetivo"), dict):
        # sin fase C, o fase C anterior a la 4.12 (sin materialidad separada ni protocolo): no se reconstruye un objetivo que esa
        # fase C no evaluó; el informe usa entonces la marca de la regla vigente (Anexo B §B.6.7), como en la 4.11
        return None
    ev = evaluar(carpeta, fc, precio, var, conf, ccj)
    if ev is None:
        return None
    ob = ((fc or {}).get("configuracion_v64") or {}).get("objetivo") or {}
    cv = (fc or {}).get("configuracion_v64") or {}
    T = ev["tratamiento"]
    po = (decision or {}).get("precio_objetivo")
    emitido = po if (estado == "concluido" and T in ("objetivo_emitido", "objetivo_condicionado") and _num(po)) else None
    params = cv.get("parametros") or []
    rda = (fc or {}).get("revision_datos_ausentes") or {}
    eo = ESTADO_DEL_OBJETIVO[T]
    # (4.13, revisión interna R3) una salida cuyo estado no es el que produce el tratamiento de la fase C (p. ej., una terminación en
    # no_entregable después de la fase C) no emite ni bloquea ningún objetivo: lo dice, en lugar de arrastrar el de la fase C
    estado_final_distinto = eo in ("emitido", "emitido_condicionado", "bloqueado") and (estado == "no_entregable" or (ev.get("estado_esperado") and estado != ev["estado_esperado"]))
    if estado_final_distinto:
        eo, emitido = "no_emitido_estado_final", None
    out = {
        "protocolo": ev["protocolo"], "tratamiento": T, "estado_del_objetivo": eo,
        "origen_del_bloqueo": ev["origen_del_bloqueo"],
        "valor_calculado_condicional": ev["valor_calculado_condicional"],
        "precio_objetivo_emitido": emitido,
        "provisional": T == "objetivo_condicionado" and emitido is not None,
        "hipotesis_que_lo_condicionan": ev["informacion_por_hipotesis"],
        "hipotesis_no_cubiertas_por_el_ambito": ev["hipotesis_no_cubiertas"],
        "accion_provisional": ev["accion_provisional"], "accion_sostenida_en_ambito": ev["accion_sostenida_en_ambito"],
        "motivos_no_sostenida": ev["motivos_no_sostenida"],
        "rango_calculado": ev["rango_calculado"],
        "materialidad": {
            "datos_ausentes_materiales": [x.get("dato") for x in rda.get("revisados") or [] if x.get("material_para_conclusion_favorable")],
            "hipotesis_sin_fundamento_suficiente": [p.get("clave") for p in params if p.get("fundamento_suficiente") is False]
                                                   + [h.get("celda") for h in ((fc or {}).get("fundamento_material") or {}).get("hipotesis_sin_fundamento") or []],
            "materiales_para_la_accion": [p.get("clave") for p in params if p.get("material_para_accion") is True],
            "materialidad_para_la_accion_no_determinada": [p.get("clave") for p in params if p.get("material_para_accion") is None],
            "materiales_para_el_objetivo": [p.get("clave") for p in params if p.get("material_para_objetivo") is True],
            "materialidad_para_el_objetivo_no_determinada": [p.get("clave") for p in params if "material_para_objetivo" in p and p.get("material_para_objetivo") is None],
            "limites_del_modelo_materiales": [a.get("id") for a in cv.get("avisos_de_dominio") or [] if isinstance(a, dict) and a.get("material_para_conclusion") is True],
            "ambito_por_parametro": ev["ambito_por_parametro"],
            "ambito_aislado_por_parametro": {k: ambito_aislado(var if var is not None else (_cargar(carpeta, "configuracion_v64_variantes.json") or {}), k)
                                             for k in (ev["ambito_por_parametro"] or {})},
        },
        # (4.13 §5) cobertura por hipótesis, base de cada materialidad (calculada, juicio económico o no determinada) e invariancia de
        # la acción en las variantes calculadas, que no es la materialidad de un parámetro no identificado
        "cobertura": ({"por_parametro": ev["cobertura_por_parametro"],
                       "base_de_la_materialidad_para_la_accion": {p.get("clave"): p.get("base_de_la_materialidad") for p in params},
                       "base_de_la_materialidad_para_el_objetivo": {p.get("clave"): p.get("base_de_la_materialidad_objetivo") for p in params},
                       "juicios_economicos_objetivo": [{"clave": p.get("clave"), "material_para_objetivo": p.get("material_para_objetivo"), "evidencia": p.get("evidencia"),
                                                        "inferencias": p.get("inferencias")} for p in params if p.get("base_de_la_materialidad_objetivo") == "juicio_economico"],
                       "juicios_economicos": [{"clave": p.get("clave"), "material_para_accion": p.get("material_para_accion"), "evidencia": p.get("evidencia"),
                                               "inferencias": p.get("inferencias")} for p in params if p.get("base_de_la_materialidad") == "juicio_economico"],
                       # (4.14, encargo de cierre §5) el juicio propio sobre el objetivo, si la fase C se generó con ese contrato
                       "juicios_objetivo": ([dict({k2: (p.get("juicio_objetivo") or {}).get(k2) for k2 in ("hipotesis", "contraste", "cobertura", "limites", "base",
                                                                                                          "material", "criterio", "comparado_con", "razonamiento", "evidencia")},
                                                  clave=p.get("clave"), fundamento_suficiente=p.get("fundamento_suficiente"))
                                             for p in params if isinstance(p.get("juicio_objetivo"), dict)] or None),
                       "sin_fundamento_excluidas_por_juicio": ([p.get("clave") for p in params if isinstance(p.get("juicio_objetivo"), dict)
                                                                and p.get("fundamento_suficiente") is False and p["juicio_objetivo"].get("material") is False
                                                                and p["juicio_objetivo"].get("base") == "juicio_economico"] or None),
                       "discrepancias_revisadas": {p.get("clave"): p.get("contradicciones_revisadas") for p in params if p.get("contradicciones_revisadas")},
                       "nota": ("contraste_aislado y variacion_conjunta_necesaria permiten una materialidad calculada; variacion_conjunta y sin_cobertura, "
                                "solo un juicio económico con evidencia o «no determinada». La invariancia de la acción vale solo para las variantes calculadas.")}
                      if ev.get("contrato_cobertura") else None),
        "motivo": ((f"el estado final {estado!r} no es el que corresponde al tratamiento de la fase C ({ev.get('estado_esperado')}): no se emite ni se bloquea "
                    "ningún objetivo en esta salida. " if estado_final_distinto else "") + (ob.get("motivo") or ev["motivo_mecanico"])),
        "nota": NOTA,
    }
    if T == "objetivo_sin_protocolo":
        out["lecturas_posibles"] = lecturas_sin_protocolo(ev)
    return out


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    print(json.dumps(evaluar(sys.argv[1]), ensure_ascii=False, indent=1, default=str))
