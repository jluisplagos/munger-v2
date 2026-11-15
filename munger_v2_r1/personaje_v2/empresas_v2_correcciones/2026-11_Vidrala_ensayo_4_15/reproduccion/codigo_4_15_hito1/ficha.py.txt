#!/usr/bin/env python3
"""ficha.json por empresa (Anexo D §D.7): lo necesario para la capa entre empresas y el futuro Damodaran independiente.

Uso: ficha.py CARPETA [--estado ESTADO] [--provisional] [--config config_v2.json]
Con --provisional escribe ficha_provisional.json: material para la auditoría con el estado PROPUESTO (paso 11; reparación del
cierre, 4.6). Sin él escribe la ficha oficial ficha.json; con --estado concluido solo si hay una auditoría APROBADO válida del
material vigente (cierre_v2.motivo_rechazo_cierre); si no, no escribe nada y termina con código 3.
Añade (4.6) `datos_etapa1_incompletos` (marca «con datos de etapa 1 incompletos» y sus causas, de entrada_v63.json →
necesarios_para_listo_provisional) y `alcance` (alcance_v2.json, metadato explícito del expediente; null si no existe).
Lee lo que haya en CARPETA (fase_a/b/c.json, resultados.json, precio.json, referencias_mecanicas.json, gramatica.json,
comprobacion_conjunta.json, entrada_v63.json, datos_v63.json, estado_pipeline.json, datos_ausentes.json, diagnostico.json).
Los campos que no existen en el estado van a null: nunca se inventan.
"""
import argparse
import datetime as dt
import hashlib
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import config_v2  # noqa: E402
import celdas_v2 as C  # noqa: E402
import cierre_v2 as CIE  # noqa: E402
import configuracion_economica as CE  # noqa: E402  (4.11)
import seleccion_plantilla as SEL  # noqa: E402  (4.11)

PAL_CLAVES = {"g15": "crecimiento_1_5", "m_obj": "margen_objetivo", "s2c": "s2c", "g_inf": "g_perpetuo", "roic_lp": "roic_lp"}
CELDA_PAL = {"crecimiento_1_5": "Palancas!{c}14", "margen_objetivo": "Palancas!{c}15", "s2c": "Palancas!{c}16", "g_perpetuo": "Análisis!{c}68", "roic_lp": "Palancas!{c}18"}
# (4.12 §9, evaluación expresa de aptitud de uso) en los expedientes V6.4 experimentales, la aptitud de uso va en un bloque propio,
# separado de la auditoría: la auditoría de 16 puntos comprueba las reglas del expediente y no evalúa la aptitud; este bloque no cambia
# su contrato ni ningún veredicto. Es la evaluación de la entrega (versión del código), no del expediente: se actualiza con cada entrega.
# Las salidas V6.3 y V6.4 heredadas no lo llevan.
APTITUD_V64 = {
    "caracter": "experimental",
    "version": "4.14",
    "uso_que_permite": ("análisis experimental bajo la supervisión de la persona responsable: recorrer el expediente, comparar escenarios, "
                        "configuraciones y protocolos, y preparar las preguntas y los datos que faltan"),
    "no_apto_para": ("apoyar decisiones con dinero real: las plantillas V6.4 y V6.4.1, su configuración económica, el perímetro de la inversión "
                     "y los protocolos del objetivo no están adoptados, y la entrega no acredita la aptitud para ese uso"),
    "distinta_de_la_auditoria": ("una auditoría APROBADO dice que el expediente cumple las 16 reglas del pipeline; ni ella ni el estado «concluido» "
                                 "hacen apto el resultado para decidir con dinero real"),
    "evaluacion": "informe integrado de la entrega 4.13 (2026-11_Vidrala_ensayo_4_13/INFORME_INTEGRACION_4_13.md, apartado de aptitud de uso)",
}


def aptitud_de_uso(c):
    """(4.14, requisito de verificación completa de las entradas) la aptitud de uso de la entrega más la verificación de las entradas del
    expediente: sin un registro vigente con cobertura completa y todas las entradas materiales comprobadas, ninguna salida presenta la
    conclusión como apta para dinero real. Es condición necesaria, no suficiente: la entrega sigue siendo experimental."""
    import verificacion_entradas as VE
    apto_e, resumen = VE.aptitud(c)
    a = dict(APTITUD_V64)
    a["version"] = "4.14"
    a["evaluacion"] = "informe integrado de la entrega 4.14 (apartado de aptitud de uso)"
    a["verificacion_entradas"] = resumen
    a["apto_para_dinero_real"] = False
    a["motivos_no_apto"] = ([] if apto_e else [f"verificación de las entradas financieras incompleta: {resumen.get('motivo')}"]) + [
        "la entrega es experimental: plantillas, configuración económica, perímetro y protocolos no adoptados"]
    return a


ILEGIBLES = []  # (4.13, revisión interna R1) archivos que existían y no se pudieron leer en esta llamada


def cargar(c, n):
    """Contenido JSON de un archivo del expediente; None si no existe. (4.13, R1) Un archivo que existe pero no se puede leer (JSON
    roto, sin permiso) no interrumpe la llamada: se anota en ILEGIBLES y la ficha no se escribe (la vigencia ya se comprobó antes)."""
    p = os.path.join(c, n)
    if not os.path.exists(p):
        return None
    try:
        return json.load(open(p, encoding="utf-8"))
    except (OSError, ValueError) as e:
        ILEGIBLES.append(f"{n} ({type(e).__name__})")
        return None


def _terminar_ilegibles(c, cfg, provisional):
    """(4.13, revisión del cambio de la ronda, H1, H2, H4 y H5) Hay archivos que no se pueden leer: no se escribe ninguna ficha. Fuera del
    modo provisional, antes de terminar, se aplica la vigencia COMPLETA (protegida) y se retira la aprobación publicada en todos los
    destinos. Código 5 si queda una retirada pendiente o la propia comprobación falló; 3 si no."""
    import estructura_json as ESTR
    ext = ""
    pend = mal = None
    if not provisional:
        import pipeline as _pl
        _av, mal = ESTR.protegido(CIE.asegurar_vigencia, c, _pl.Pipeline.veredicto_auditoria, None, CIE.ruta_resumen(c, cfg), contexto="vigencia")
        motivo, arch = _av if _av else (mal, None)
        pend, mp = ESTR.protegido(lambda: CIE.sincronizar_resumenes(c, _pl.Pipeline.veredicto_auditoria) or CIE.retiradas_pendientes(c), contexto="retirada")
        pend = pend or mp
        if motivo:
            ext = f" {'Aprobación retirada' if arch else 'Aprobación no acreditada'}: {motivo}." + (f" Salidas oficiales anteriores archivadas en {os.path.relpath(arch, c)}." if arch else "")
        if pend:
            ext += f" RETIRADA PENDIENTE: {pend}."
    print(f"ficha.py: no se escribe ninguna ficha: archivos del expediente que no se pueden leer: {', '.join(ILEGIBLES)}.{ext}")
    return 5 if (pend or mal) else 3


def leer_control(p):
    """(objeto, ilegible) de un archivo de control JSON: (None, False) si no existe; (None, True) si existe pero no es un objeto JSON
    legible (4.9, Z-2 y control de vigencia V-1/V-2: no interrumpe; la vigencia lo trata como motivo de retirada). Local a este
    script, sin depender de funciones nuevas de cierre_v2.py."""
    if not os.path.exists(p):
        return None, False
    try:
        o = json.load(open(p, encoding="utf-8"))
    except (ValueError, OSError):
        return None, True
    return (o, False) if isinstance(o, dict) else (None, True)


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest() if p and os.path.isfile(p) else None


TXT_S4_NIIF = 'G7 de la gramática usa las bases heredadas (tipo de la Historia y S2C de la Historia, sin f); las referencias mecánicas del S2C se anclan, con el perímetro NIIF 16 (V6.4.1), en el S2C histórico de ese perímetro (Configuración V6.4!B155), no en Historia!C53, y tampoco aplican f: no comprueban el modelo experimental'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("carpeta")
    ap.add_argument("--estado")
    ap.add_argument("--provisional", action="store_true")
    ap.add_argument("--config", default=None)  # (4.11) None → MUNGER_CONFIG (la del pipeline) o config_v2.json
    a = ap.parse_args()
    c = a.carpeta
    cfg = config_v2.cargar(a.config)
    # (4.12 §5) la selección del expediente se comprueba o se resuelve (en lectura): una llamada a mano sin MUNGER_CONFIG no produce
    # una ficha aparentemente V6.4 con la configuración V6.3. Con motivo no se escribe ninguna ficha; antes, fuera del modo
    # provisional, la vigencia retira una aprobación cuyo material cambió (4.12 §3: retirar primero, rechazar después)
    # (4.13 §3) protegido: una estructura inesperada en la selección o la configuración es un motivo, no una excepción
    import estructura_json as ESTR
    _r, _m = ESTR.protegido(SEL.resolver, c, cfg, contexto="selección de plantilla")
    cfg, m_sel, nota_sel = _r if _r else (cfg, _m, None)
    if nota_sel:
        print(f"ficha.py: {nota_sel}")
    if not a.provisional:
        # (4.13, revisión interna R1) vigencia ANTES de leer el material: una aprobación cuyo material cambió (también un JSON roto o de
        # otra estructura) se retira en la primera llamada, sin depender de poder interpretar ese material. Protegida: si la retirada
        # misma falla por una estructura inesperada, el motivo se dice y la llamada termina sin escribir ninguna ficha
        # (ronda general de la 4.13) aquí se comprueba la aprobación DEL MATERIAL (motivo_rechazo_cierre), no la identidad de la ficha
        # y del informe oficiales: esos son la salida que esta llamada regenera, y su cambio lo tratan, más abajo y como hasta la 4.12,
        # la sustitución W-d (código 0 con aviso, la ficha nueva no es vigente) y la ficha ilegible (V-1, W-2). Si no, las baterías de
        # trazabilidad (M) y de integridad (H) cambiarían de comportamiento sin que el material hubiera cambiado. Además se comprueba el
        # informe oficial: ficha.py no lo regenera, y registrar_cierre lo reescribiría como si fuera el registrado. Si un archivo no se
        # puede leer, la vigencia completa se aplica abajo, antes de terminar sin escribir (revisión del cambio de la ronda, H1–H3)
        import pipeline as _pl
        _csv0 = CIE.ruta_resumen(c, cfg)
        _F0, _errF0 = CIE.leer_ficha_control(os.path.join(c, "ficha.json"))
        _hay_cierre, _mh = ESTR.protegido(lambda: CIE.ficha_cerrada(_F0) or CIE.cierre_registrado(c), contexto="vigencia")
        # (4.13.1, H5) sin ficha oficial cerrada ni cierre registrado, una aprobación cuyo cierre consta como publicado no tiene respaldo:
        # se retira aquí, en la primera llamada, también con el material intacto (motivo_vigencia da el motivo)
        _sin_resp, _msr = (False, None) if (_hay_cierre or _mh) else ESTR.protegido(CIE.aprobacion_publicada_sin_respaldo, c, None if _errF0 else _F0, contexto="vigencia")
        _mh5 = None
        if _sin_resp:
            _mh5, _msr2 = ESTR.protegido(CIE.motivo_vigencia, c, _pl.Pipeline.veredicto_auditoria, contexto="vigencia")
            _msr = _msr or _msr2
        _mh = _mh or _msr  # un fallo de la comprobación misma: código 5
        if _hay_cierre or _mh or _mh5:
            _rm, _mrm = ESTR.protegido(CIE.motivo_rechazo_cierre, c, _pl.Pipeline.veredicto_auditoria, contexto="vigencia del material")

            def _informe_cambiado():
                cv = CIE._j_tolerante(os.path.join(c, CIE.CIERRE_VIGENTE)) or {}
                inf = os.path.join(c, "informe.md")
                if isinstance(cv, dict) and cv.get("informe_sha256") and os.path.exists(inf) and CIE._sha(inf) != cv["informe_sha256"]:
                    return "informe.md no es el informe registrado al cerrar (cambió después del cierre)"
                return None
            _ri, _mri = (None, None) if (_rm or _mrm) else ESTR.protegido(_informe_cambiado, contexto="vigencia del informe")
            _mv = _rm or _mrm or _mh or _ri or _mri or _mh5
            if _mv:
                _arch, _ma = ESTR.protegido(CIE.archivar_salidas, c, _mv, _csv0, contexto="retirada")
                _pend, _mp = ESTR.protegido(lambda: CIE.sincronizar_resumenes(c, _pl.Pipeline.veredicto_auditoria) or CIE.retiradas_pendientes(c), contexto="retirada")
                print(f"ficha.py: {'aprobación retirada' if _arch else 'aprobación no acreditada (nada que archivar)'} antes de leer el material: {_mv}."
                      + (f" Salidas oficiales anteriores archivadas en {os.path.relpath(_arch, c)}." if _arch else "")
                      + (f" RETIRADA PENDIENTE: {_ma or _mp or _pend}." if (_ma or _mp or _pend) else ""))
                if _ma or _mp or _pend or _mrm or _mh or _mri:
                    return 5
    fa, fb, fc = cargar(c, "fase_a.json"), cargar(c, "fase_b.json"), cargar(c, "fase_c.json")
    res, precio, refs, gram = cargar(c, "resultados.json"), cargar(c, "precio.json"), cargar(c, "referencias_mecanicas.json"), cargar(c, "gramatica.json")
    cc, entrada, datos, pipe, da, diag = cargar(c, "comprobacion_conjunta.json"), cargar(c, "entrada_v63.json"), cargar(c, "datos_v63.json"), leer_control(os.path.join(c, "estado_pipeline.json"))[0], cargar(c, "datos_ausentes.json"), cargar(c, "diagnostico.json")
    # (4.9, Z-2) un estado_pipeline.json ilegible no interrumpe ficha.py: motivo_rechazo_cierre lo da como motivo y la salida cerrada se retira
    f1 = cargar(c, "fase1_v63.json") or {}  # en los estados tempranos (pendiente_de_datos en los pasos 1-3) es la única fuente del nombre
    if ILEGIBLES:
        # (4.13, R1) una ficha no se construye con material que no se puede leer. (Revisión del cambio de la ronda, H1, H2 y H5) Antes de
        # terminar, fuera del modo provisional, la vigencia COMPLETA (también la ficha oficial y el registro del cierre): aquí no se
        # escribe ninguna ficha, así que la sustitución W-d no aplica; la combinación de un archivo ilegible con una ficha sin marcadores
        # o sin cierre registrado no puede dejar la aprobación vigente
        return _terminar_ilegibles(c, cfg, a.provisional)
    estado = a.estado or (pipe or {}).get("estado_analisis") or (fc or {}).get("estado_analisis") or "no_entregable"
    cierre = None
    if not a.provisional:
        import pipeline  # regla estricta de H2, sin cambios
        csv_res = CIE.ruta_resumen(c, cfg)
        vieja, vieja_ilegible = leer_control(os.path.join(c, "ficha.json"))
        if vieja_ilegible or (vieja and vieja.get("cierre") is not None and not isinstance(vieja.get("cierre"), dict)):
            # (4.9, control de vigencia V-1 y segundo control W-2) una ficha oficial que no se puede leer no se sustituye en silencio por
            # otra cerrada: se archiva como antecedente, se retira la aprobación publicada y el cierre exige una auditoría nueva (paso 13)
            motivo, archivo = CIE.asegurar_vigencia(c, pipeline.Pipeline.veredicto_auditoria, None, csv_res)
            pend = CIE.sincronizar_resumenes(c, pipeline.Pipeline.veredicto_auditoria) or CIE.retiradas_pendientes(c)
            print(f"ficha.py: no se escribe la ficha oficial: {motivo or 'ficha.json no se puede leer'}." + (f" Salidas oficiales anteriores archivadas en {os.path.relpath(archivo, c)}." if archivo else "")
                  + " Hace falta una auditoría nueva (paso 13)." + (f" RETIRADA PENDIENTE en {pend}." if pend else ""))
            return 5 if pend else 3
        if (os.path.lexists(os.path.join(c, "cierre_vigente.json")) or (vieja is not None and (pipe or {}).get("auditoria") == "APROBADO")) and not CIE.ficha_cerrada(vieja):
            # (4.10, encargo §3.3) la ficha oficial perdió sus marcadores de cierre («cierre» y el estado concluido; o es {} o falta)
            # mientras hay un cierre registrado: antes de escribir nada (y de que registrar_cierre actualice el registro en silencio)
            # se comprueba la correspondencia con el cierre registrado; si no corresponde, se archiva, se retira la aprobación en
            # todos los destinos registrados y no se escribe una ficha oficial nueva hasta una auditoría nueva (paso 13)
            motivo, archivo = CIE.asegurar_vigencia(c, pipeline.Pipeline.veredicto_auditoria, None, csv_res)
            if motivo:
                pend = CIE.sincronizar_resumenes(c, pipeline.Pipeline.veredicto_auditoria) or CIE.retiradas_pendientes(c)
                print(f"ficha.py: no se escribe la ficha oficial: {motivo}." + (f" Salidas oficiales anteriores archivadas en {os.path.relpath(archivo, c)}." if archivo else "")
                      + " Hace falta una auditoría nueva (paso 13)." + (f" RETIRADA PENDIENTE en {pend}." if pend else ""))
                return 5 if pend else 3
        motivo, _mex = ESTR.protegido(CIE.motivo_rechazo_cierre, c, pipeline.Pipeline.veredicto_auditoria, contexto="comprobación del cierre")
        motivo = motivo or _mex  # (4.13, R1) una estructura inesperada en ficha.json o en el cierre es un motivo de rechazo, no una excepción
        if estado == "concluido" and motivo:
            # (4.6.1) no basta con no escribir: una ficha oficial anterior que ya no es vigente se archiva (con informe y resumen)
            _, archivo = CIE.asegurar_vigencia(c, pipeline.Pipeline.veredicto_auditoria, None, csv_res)
            pend = CIE.sincronizar_resumenes(c, pipeline.Pipeline.veredicto_auditoria) or CIE.retiradas_pendientes(c)  # (4.7) todos los destinos registrados
            print(f"ficha.py: no se confirma «concluido» en la ficha oficial: {motivo}." + (f" Salidas oficiales anteriores archivadas en {os.path.relpath(archivo, c)}." if archivo else "") + " Para el material de la auditoría, usa --provisional." + (f" RETIRADA PENDIENTE en {pend}." if pend else ""))
            return 5 if pend else 3
        pend = CIE.sincronizar_resumenes(c, pipeline.Pipeline.veredicto_auditoria)
        if pend:
            print(f"ficha.py: RETIRADA PENDIENTE de aprobaciones publicadas en {pend}: no se escribe la ficha oficial hasta completarla")
            return 5
        # (4.8, X-c) «cierre» solo en un estado que la auditoría puede confirmar: nunca en no_entregable, aunque el pipeline esté
        # numéricamente en el paso 14 (fallo de implementación al cerrar, p. ej. una ficha que no cumple su esquema)
        # (4.8, Z-f de la auditoría interna) y solo si el estado es el que propuso el material auditado (ficha_provisional.json), cuando existe
        propuesto = ((cargar(c, "ficha_provisional.json") or {}).get("provisional") or {}).get("estado_propuesto")
        if not motivo and estado != "no_entregable" and (estado == "concluido" or (pipe or {}).get("paso") == 14) and (propuesto is None or estado == propuesto):
            cierre = {"auditoria": "APROBADO", "material_auditado": (CIE.material_fijado(c) or {}).get("id")}
        elif not motivo and estado == "concluido" and propuesto not in (None, "concluido"):
            print(f"ficha.py: no se confirma «concluido» en la ficha oficial: el material auditado proponía {propuesto!r}. Para el material de la auditoría, usa --provisional.")
            return 3
    if m_sel:
        print(f"ficha.py: SELECCIÓN DE PLANTILLA DETENIDA: {m_sel}: no se escribe ninguna ficha")
        return 2
    try:
        alc = CIE.alcance(c)
    except ValueError as e:
        print(f"ficha.py: {e}")
        return 1
    an = (datos or {}).get("analisis") or {}
    her = (datos or {}).get("herencia") or {}
    libros = {n: (os.path.join(c, f) if f else None) for n, f in (("entrada", next((f for f in os.listdir(c) if f.endswith("_v63_datos.xlsx")), "")), ("evaluado", next((f for f in os.listdir(c) if f.endswith("_v63_evaluada.xlsx")), "")))}
    # escenarios
    esc = {}
    for i, e in enumerate(("MALO", "NORMAL", "BUENO")):
        col = "BCD"[i]
        pal = {}
        for k, pk in PAL_CLAVES.items():
            ent = (((fb or {}).get("palancas") or {}).get(pk) or {}).get(e) or {}
            pal[k] = {kk: ent.get(kk) for kk in ("referencia_mecanica", "referencia_no_disponible_motivo", "valor", "desviacion", "clase", "confianza")} if ent else None
        esc[e] = {"historia": ((fa or {}).get("escenarios") or {}).get(e), "frase": ((fa or {}).get("celdas") or {}).get(f"{col}66"),
                  "probabilidad": ((res or {}).get("probabilidades") or [None] * 3)[i], "valor_accion": ((res or {}).get("valores") or {}).get(f"{col}78"), "palancas": pal}
    # cambios vs etapa 1 (34 heredadas)
    cambios = []
    for src in (fa, fb, fc):
        for k, v in ((src or {}).get("herencia") or {}).items():
            cambios.append({"celda": k, "antes": v.get("etapa1"), "despues": ((src or {}).get("celdas") or {}).get(k), "decision": v.get("decision"), "motivo": v.get("motivo"),
                            "evidencia_y_razonamiento": v.get("evidencia_y_razonamiento")})
    # C62 corregida por la fase C al declarar el límite del modelo (única corrección que llega al libro)
    for k, v in ((fc or {}).get("celdas_corregidas") or {}).items():
        if k in ("C62", "Análisis!C62") and v.get("despues") != v.get("antes"):
            for cmb in cambios:
                if cmb["celda"] in ("C62", "Análisis!C62"):
                    cmb.update({"despues": v.get("despues"), "decision": "cambia", "motivo": "razonamiento_corregido", "evidencia_y_razonamiento": f"corregida en la fase C (límite del modelo): {v.get('motivo')}"})
    # recuento de clases
    rec = {"fundamentada": 0, "convencion": 0, "tecnico": 0, "sin_juicio": 0}
    mapa = {"fundamentada": "fundamentada", "convención": "convencion", "técnico": "tecnico", "sin juicio propio": "sin_juicio"}
    for src in (fa, fb, fc):
        for o in ((src or {}).get("observaciones") or {}).values():
            for cl, k in mapa.items():
                if isinstance(o, str) and f"[Clase: {cl}]" in o:
                    rec[k] += 1
    fm = (fc or {}).get("fundamento_material") or {}
    decision = (fc or {}).get("decision")
    cubo_final = (fc or {}).get("cubo_final")
    if estado == "modelo_no_aplicable" and not decision:
        cubo_p = (fc or fa or {}).get("cubo_provisional")
        decision = {"accion": {"No": "descartar", "Demasiado difícil": "demasiado_dificil"}.get(cubo_p), "precio_objetivo": None, "condicion": None}
    if estado == "no_entregable":
        # lo que la fase C hubiera concluido no se entrega: la ficha no lleva cubo ni acción (D17)
        decision, cubo_final = None, None
    elif estado == "modelo_no_aplicable":
        # nunca comprar ni esperar, nunca cubo Sí (§8); el cubo es el cualitativo
        if decision and decision.get("accion") in ("comprar", "esperar"):
            decision = dict(decision, accion=None, precio_objetivo=None, condicion=None)
        if cubo_final == "Sí":
            cubo_final = None
    elif estado in ("pendiente_de_datos", "pendiente_de_investigacion"):
        decision = {"accion": None, "precio_objetivo": None, "condicion": None, "condiciones_revision": (decision or {}).get("condiciones_revision")} if decision else None
        cubo_final = cubo_final if cubo_final in ("Vigilar", "No", "Demasiado difícil") else None
    causa = None
    if estado != "concluido":
        causa = (diag or {}).get("causa") or {"tipo": {"pendiente_de_datos": "falta_de_datos", "pendiente_de_investigacion": "incertidumbre_no_acotada", "modelo_no_aplicable": "limite_del_modelo"}.get(estado, "fallo_de_implementacion"), "detalle": None}
    ficha = {
        "empresa": an.get("B3") or (fa or {}).get("empresa") or f1.get("empresa") or os.path.basename(os.path.abspath(c)), "ticker": an.get("D3") or f1.get("ticker"),
        "fecha": (fa or {}).get("fecha_analisis") or an.get("D4") or f1.get("fecha_analisis") or dt.date.today().isoformat(),
        "moneda": (((datos or {}).get("control_maestro") or {}).get("cabecera") or {}).get("H4_moneda") or f1.get("moneda_modelo"),
        "versiones": {"personaje": cfg.get("version_personaje"), "plantilla": (SEL.leer(c) or {}).get("version") or "V6.3", "gramatica": cfg.get("version_gramatica"), "referencias_mecanicas": cfg.get("version_referencias_mecanicas"), "config": cfg.get("version_config")},
        "hashes": {"libro_entrada": sha(libros["entrada"]), "libro_evaluado": sha(libros["evaluado"])},
        "estado_analisis": estado, "causa_si_no_concluido": causa,
        "etapa1": {"cubo": (her.get("celdas") or {}).get("C104"), "cubo_juicio": None, "precio_de_si": None, "fecha": None, "r": (her.get("celdas") or {}).get("C56")},
        "cubo": cubo_final, "cubo_cualitativo_fase_a": (fa or {}).get("cubo_provisional"),
        "decision": decision, "insumos_decision_cartera": (fc or {}).get("insumos_decision_cartera"),
        "motor": (res or {}).get("motor") or (fb or {}).get("motor"),
        "escenarios": esc, "valor_ponderado": ((res or {}).get("valores") or {}).get("C83"), "precio": ((res or {}).get("valores") or {}).get("C37"),
        "escalera": precio, "fundamento_material": fm or None, "comprobacion_conjunta": cc,
        "revision_datos_ausentes": (fc or {}).get("revision_datos_ausentes"),
        "estado_libro": ((res or {}).get("estados") or {}).get("estado_libro_B266"), "estado_evidencias": ((res or {}).get("estados") or {}).get("evidencias_B269"),
        "palanca_mas_influyente": {"nombre": ((res or {}).get("tornado") or {}).get("mas_influyente"), "nota": "información, no criterio (D10)"},
        "semaforos": (res or {}).get("semaforos"), "salto_anio_11": (((res or {}).get("salto_anio_11") or {}).get("filas") or [None] * 5)[4] if res else None,
        "peso_terminal": ((res or {}).get("por_escenario") or {}).get("peso_terminal"),
        "cambios_vs_etapa1": cambios, "n_cambios_vs_etapa1": len(cambios),
        "predicciones": [{"texto": ((fc or {}).get("celdas") or {}).get(f"Palancas!A{i}"), "fecha": ((fc or {}).get("celdas") or {}).get(f"Palancas!B{i}"), "prob": ((fc or {}).get("celdas") or {}).get(f"Palancas!C{i}"), "resultado": None} for i in (38, 39, 40)] if fc else None,
        "incertidumbre_pendiente": ((fc or {}).get("celdas") or {}).get("Diagnóstico V6!B222"), "que_lo_resolveria": ((fc or {}).get("celdas") or {}).get("Diagnóstico V6!B223") or fm.get("que_lo_resolveria"),
        "cambiaria_de_cubo": (fc or {}).get("cambiaria_de_cubo"), "autocomprobacion": (fc or {}).get("autocomprobacion"),
        "recuento_clases": rec, "desviaciones_justificadas": {"n": len(((fb or {}).get("desviaciones_justificadas") or []) + ((fc or {}).get("desviaciones_justificadas") or [])),
                                                             "lista": ((fb or {}).get("desviaciones_justificadas") or []) + ((fc or {}).get("desviaciones_justificadas") or [])},
        "avisos": [x for x in ((gram or {}).get("hallazgos") or []) if x.get("categoria") == "aviso"],
        "confianza_global": (fc or {}).get("confianza_global"),
        "que_falta": {"bloqueantes": (entrada or {}).get("bloqueantes"), "necesarios_para_listo_provisional": (entrada or {}).get("necesarios_para_listo_provisional"), "no_bloqueantes": (entrada or {}).get("no_bloqueantes"), "datos_ausentes": da},
        "citas": {"munger": None, "damodaran": None},
        "dos_errores": (fb or {}).get("dos_errores"), "seis_preguntas": (fa or {}).get("seis_preguntas"), "descalificadores": (fa or {}).get("descalificadores"), "foso": (fa or {}).get("foso"),
        "comparacion_etapa_1": (fc or {}).get("comparacion_etapa_1"),
        "datos_etapa1_incompletos": CIE.marca_etapa1(entrada),
        "alcance": alc,
    }
    pa = SEL.leer(c)
    if pa is not None:
        # (4.11) solo en expedientes V6.4: base, versión, configuración efectiva y límites (los expedientes V6.3 no cambian de ficha)
        conf_e = SEL.configuracion(c) or {}
        cv = (res or {}).get("configuracion_v64") or {}
        var = cargar(c, "configuracion_v64_variantes.json") or {}
        pc = os.path.join(c, SEL.CONF)
        ficha["configuracion_economica"] = {
            "plantilla": {k: pa.get(k) for k in ("version", "archivo", "archivo_sha256", "referencia", "referencia_sha256", "verificador", "verificador_sha256", "config")},
            "configuracion_sha256": sha(pc) if os.path.exists(pc) else None, "modo": conf_e.get("modo"), "resumen": CE.resumen(conf_e) if conf_e else None,
            "naturaleza": conf_e.get("naturaleza"),
            "efectivos_en_el_libro": {k: cv.get(k) for k in ("modo", "valida", "t_historia", "t_nopat", "t_escudo", "m0_heredado", "m0_aplicado", "regla", "nwc_efectivo",
                                                            "codigo_estructura", "lambda", "theta", "convencion_anios", "convencion_terminal", "roic_terminal", "cartera_texto",
                                                            "D_hist", "F_hist", "Rh", "f_s2c", "f_roic", "f_fija", "trazabilidad_completa")
                                     # (4.13 §7) solo libros V6.4.1: perímetro efectivo y altas de derechos de uso que entran en las bases
                                     + tuple(k for k in ("perimetro_efectivo", "altas_derechos_uso", "s2c_referencia_perimetro") if k in cv)} if cv else None,
            "conciliacion": {n: (x or {}).get("comprobacion") for n, x in (cv.get("conciliacion") or {}).items()} if cv else None,
            "variantes_calculadas": {"zonas": var.get("zonas_calculadas"), "zona_igual_en_todas": var.get("zona_igual_en_todas_las_calculadas"),
                                     "n": len([v for v in var.get("variantes") or [] if v.get("zona")]), "sin_calcular": [v.get("clave") for v in var.get("variantes") or [] if not v.get("zona")]} if var.get("aplica") else None,
            "evaluacion_fase_c": (fc or {}).get("configuracion_v64"),
            "limites": ["configuración de ensayo: ninguna estructura, λ, θ, tipo ni margen está adoptado (propuestas humanas sin firmar)",
                        "P-M1 no queda resuelta por implementar sus alternativas; la identidad del FCF es aritmética, no prueba del mantenimiento real",
                        "R0 + P-M1 sin especificar (se rechaza); motor B solamente"]
                       + (["R1: el terminal no aplica la regla del máximo conservado (carga la inversión fija para crecer al ritmo g aunque las ventas del MALO sigan por debajo del máximo; definición prudente)",
                           "R1: en los años en que las ventas no superan el máximo conservado no hay inversión fija para crecer, y la palanca S2C de ese escenario no actúa en ellos"]
                          if (cv.get("regla") == "R1" if cv else False) else [])
                       # (4.12 §5) lecturas con bases parciales, identificadas donde se usan: no son una comprobación completa del modelo experimental
                       + (["BL (valor sin crecimiento; Diagnóstico B33:D33 y «cuánto pagas por crecer») no incluye la cartera P0: es una lectura, no entra en el valor ni en el precio de Sí"]
                          if str((cv or {}).get("cartera_texto") or "").startswith("P0") else [])
                       # (4.14, S4 de la segunda revisión interna 4.13) con el perímetro NIIF 16 de la V6.4.1 el ancla de las referencias del S2C es
                       # B155, no una base heredada; G7 sigue con las bases de la Historia
                       + (([TXT_S4_NIIF] if str((cv or {}).get("perimetro_efectivo") or "").upper().replace(" ", "") == "NIIF16" else
                           ["G7 de la gramática y las referencias mecánicas usan las bases heredadas (tipo de la Historia y S2C sin f): no comprueban el modelo experimental"])
                          if conf_e.get("modo") == "Experimental" else []),
        }
        if var.get("formato") in ("4.12", "4.13"):
            # (4.12 §5) avisos de dominio con valores y motivo, y la evaluación de la fase C; huella de las entradas económicas de las variantes
            ev_av = {a.get("id"): a for a in ((fc or {}).get("configuracion_v64") or {}).get("avisos_de_dominio") or [] if isinstance(a, dict)}
            ficha["configuracion_economica"]["avisos_de_dominio"] = [dict(a, evaluacion_fase_c=ev_av.get(a.get("id"))) for a in var.get("avisos_de_dominio") or []]
            if var.get("formato") == "4.13":
                # (4.13 §5) avisos de las variantes calculadas, agrupados, con la evaluación de la fase C de cada grupo
                ev_gv = {a.get("id"): a for a in ((fc or {}).get("configuracion_v64") or {}).get("avisos_de_dominio_variantes") or [] if isinstance(a, dict)}
                ficha["configuracion_economica"]["avisos_de_dominio_variantes"] = {k: dict(g, evaluacion_fase_c=ev_gv.get(k))
                                                                                   for k, g in (var.get("avisos_de_dominio_variantes") or {}).items()}
            ficha["configuracion_economica"]["entradas_economicas"] = {"huella": (var.get("entradas_economicas") or {}).get("huella"),
                                                                        "n": (var.get("entradas_economicas") or {}).get("n"),
                                                                        "configuracion_huella_economica": var.get("configuracion_huella_economica"),
                                                                        "vector_escenarios_activa": var.get("vector_escenarios_activa")}
        if SEL.experimental(c):
            # (4.12 §4) objetivo estructurado y trazable (no hay que buscar «provisional» en un párrafo): protocolo, valor calculado
            # condicional, precio objetivo emitido, marca provisional, hipótesis que lo condicionan, rango calculado y su ámbito, y la
            # materialidad separada. decision.precio_objetivo sigue siendo el objetivo emitido (compatibilidad de los consumidores)
            import objetivo_v64 as OBJ
            ficha["objetivo"] = OBJ.bloque_ficha(c, fc or {}, precio or {}, estado, decision, var=var, conf=conf_e, ccj=cc)
            # (4.13 §4) una contradicción entre la acción final, el estado y los dos objetivos no llega a ninguna ficha (oficial ni
            # provisional: no se genera material aparentemente listo para la auditoría)
            # lo esperado por el tratamiento se exige cuando la ficha presenta el estado de la fase C (no a una ficha no_entregable
            # o forzada por el pipeline, que no lleva decisión); los cruces entre los dos objetivos y la acción, siempre
            ev_c = (OBJ.evaluar(c, fc or {}, precio or {}, var, conf_e, cc)
                    if ficha["objetivo"] is not None and estado == (fc or {}).get("estado_analisis") and estado != "no_entregable" else None)
            contra = OBJ.contradicciones_salida(estado, decision, ficha["objetivo"], ev_c) if ficha["objetivo"] is not None else []
            if contra:
                print("ficha.py: CONTRADICCIÓN en la decisión: " + " | ".join(contra)[:600] + ". No se escribe la ficha"
                      + ("" if a.provisional else " (la salida oficial anterior, si había, ya pasó la comprobación de vigencia)"))
                return 3
            ficha["aptitud_de_uso"] = aptitud_de_uso(c)  # (4.12 §9) separada de la auditoría; (4.14) con la verificación de las entradas
    if a.provisional:
        ficha["provisional"] = {"estado_propuesto": estado, "confirmado": False,
                                "nota": "material para la auditoría del paso 13; no es la salida oficial: el estado lo propone la fase C y solo se confirma tras una auditoría APROBADO del material vigente"}
    elif cierre:
        ficha["cierre"] = cierre
    # citas: contar referencias (Libro p. n) en los textos
    import re
    textos = json.dumps([fa, fb, fc], ensure_ascii=False)
    ficha["citas"] = {"munger": len(re.findall(r"\((?:PCA|TCI|DR|AIWTK|Poor Charlie's Almanack|Tao of Charlie Munger|Damn Right|All I Want To Know)[^)]*p\.?\s*\d+", textos)),
                      "damodaran": len(re.findall(r"\((?:NN|GV|MR|CV|PA|UD|FS|Numbers and Narrative|Growth and Value|Measuring Returns|Closure in Valuation|Probabilistic Approaches|Ups and Downs|Financial Service Firms)[^)]*p\.?\s*\d+", textos))}
    salida = "ficha_provisional.json" if a.provisional else "ficha.json"
    if ILEGIBLES:
        # (H4) un archivo leído después de la primera comprobación (ficha_provisional.json, variantes…) tampoco puede faltar en silencio
        return _terminar_ilegibles(c, cfg, a.provisional)
    sustituida = False
    if not a.provisional:
        vieja, vieja_ilegible = leer_control(os.path.join(c, "ficha.json"))
        nueva = json.loads(json.dumps(ficha, ensure_ascii=False, default=str))
        if (CIE.ficha_cerrada(vieja) and vieja != nueva) or vieja_ilegible:
            # (4.9, control de vigencia V-1) una ficha oficial ilegible tampoco se sobrescribe en silencio: queda como antecedente
            # (con --provisional no se llega aquí; sin él, una ficha ilegible ya se archivó arriba)
            # (4.6.1) una ficha oficial cerrada no se sobrescribe en silencio: queda como antecedente
            CIE.archivar_salidas(c, "sustituida por una ficha oficial nueva", csv_res)
            sustituida = True
    json.dump(ficha, open(os.path.join(c, salida), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    if not a.provisional and cierre:
        CIE.registrar_cierre(c)
    print(f"OK: {salida} · estado {'propuesto ' if a.provisional else ''}{estado} · cubo {ficha['cubo']} · acción {(decision or {}).get('accion')}")
    if sustituida and cierre:
        # (4.7.1, W-d de la auditoría interna) el código 0 solo dice que la ficha se escribió: la sustitución archivó la aprobación
        # registrada (4.6.1), así que la ficha nueva no es vigente hasta una auditoría nueva; informe.py y resumen.py la rechazarán
        print("ficha.py: AVISO: se ha sustituido una ficha cerrada y su aprobación queda archivada; la ficha nueva NO es vigente hasta "
              "una auditoría nueva del pipeline (informe.py y resumen.py la rechazarán)")
    if sustituida:
        # (4.7.1, W-1) tras sustituir una ficha cerrada, en la misma llamada: se retiran las filas que publicó la anterior (también la
        # del resumen predeterminado sin registrar); la de la ficha nueva la publica después resumen.py
        import pipeline
        pend = CIE.sincronizar_resumenes(c, pipeline.Pipeline.veredicto_auditoria) or CIE.retiradas_pendientes(c)
        if pend:
            print(f"ficha.py: RETIRADA PENDIENTE de la aprobación de la ficha sustituida en {pend}")
            return 5
    return 0


if __name__ == "__main__":
    sys.exit(main())
