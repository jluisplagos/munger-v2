#!/usr/bin/env python3
"""Añade (o sustituye) la fila de una empresa en resumen_v2.csv (Anexo D §D.10).

Uso: resumen.py CARPETA resumen_v2.csv
"""
import csv
import json
import os
import sys

COLS = ["empresa", "fecha", "estado_analisis", "causa_si_no_concluido", "cubo_v1", "cubo_v2", "motor", "precio", "moneda", "precio_escenario_malo", "precio_si",
        "ponderado", "zona", "accion", "fundamento_material", "estado_libro", "palanca_mas_influyente", "n_desviaciones", "n_sin_juicio", "n_tecnico",
        "n_hipotesis_sin_fundamento", "comprobacion_conjunta", "n_datos_ausentes", "n_datos_ausentes_materiales", "intentos_B", "intentos_C", "verificacion",
        "coste_estimado", "tiempo_min"]
# (4.12 §4) columnas añadidas AL FINAL solo en los resúmenes con filas V6.4 experimentales (ficha.objetivo): las de la V6.3 no cambian.
# Un resumen V6.4 anterior migra su cabecera la primera vez que se escribe (sus filas quedan con estas columnas vacías).
COLS_V64 = ["protocolo_objetivo", "estado_del_objetivo", "valor_calculado_condicional", "precio_objetivo_emitido", "objetivo_provisional",
            "hipotesis_que_condicionan", "rango_precio_si_min", "rango_precio_si_max", "escenarios_calculados",
            "aptitud_de_uso"]  # (4.12 §9) aptitud de uso de la entrega, separada de la auditoría («experimental»)


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


def main():
    c, csv_path = sys.argv[1], os.path.abspath(sys.argv[2])
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import cierre_v2 as CIE
    if not os.path.exists(os.path.join(c, "ficha.json")):
        # (4.7, H-3 de la auditoría interna) sin ficha (p. ej., salidas archivadas): no se publica nada, pero se retiran las
        # aprobaciones registradas y se informa de las retiradas pendientes
        import pipeline as _p
        import estructura_json as ESTR
        # (4.13.1, H5) antes de sincronizar: una aprobación publicada sin ficha ni cierre registrado se retira también del estado interno
        _av, _mal = ESTR.protegido(CIE.asegurar_vigencia, c, _p.Pipeline.veredicto_auditoria, None, csv_path, contexto="vigencia")
        motivo_h5, archivo_h5 = _av if _av else (_mal, None)
        pend = CIE.sincronizar_resumenes(c, _p.Pipeline.veredicto_auditoria)
        arch = CIE._fichas_cerradas_archivadas(c)
        emp = arch[0].get("empresa") if arch else None
        origen = CIE._fila_aprobada(csv_path, emp, arch) if emp else None  # (final, F-2; V-2; 4.7.1, W-a) también en el destino recibido
        if origen is not None:
            pend = CIE.retirar_publicaciones(c, "resumen.py sin ficha oficial vigente", csv_path, emp, ((origen.get("cierre") or {}).get("material_auditado"))) or pend
        pend = pend or CIE.retiradas_pendientes(c)
        print("resumen.py: no hay ficha.json: no se escribe ninguna fila" + (f" · aprobación retirada: {motivo_h5}" if motivo_h5 else "")
              + (f" · antecedente en {os.path.relpath(archivo_h5, c)}" if archivo_h5 else "") + (f" · RETIRADA PENDIENTE en {pend}" if pend else ""))
        return 5 if (pend or _mal) else 3
    F, ilegible = leer_control(os.path.join(c, "ficha.json"))
    F = F or {}
    # (4.9, V-1) una ficha oficial ilegible pasa por la vigencia (y se retira); (4.10, §3.3) también la que perdió sus marcadores de
    # cierre mientras hay un cierre registrado (cierre_vigente.json): su correspondencia no depende de los marcadores actuales
    # (4.10, revisión interna R-1) y la que no está cerrada mientras el estado del pipeline sigue registrando una aprobación (sin
    # cierre_vigente.json): la vigencia se comprueba siempre que hay ficha oficial; para un estado temprano legítimo no hay motivo
    pipe0 = leer_control(os.path.join(c, "estado_pipeline.json"))[0] or {}
    if CIE.ficha_cerrada(F) or ilegible or os.path.lexists(os.path.join(c, "cierre_vigente.json")) or pipe0.get("auditoria") == "APROBADO":
        # (4.6.1) la fila activa de una ficha cerrada solo se escribe si su cierre es vigente para el material actual
        import pipeline  # regla estricta de H2, sin cambios
        motivo = CIE.motivo_vigencia(c, pipeline.Pipeline.veredicto_auditoria)
        if motivo:
            CIE.archivar_salidas(c, "resumen.py: " + motivo, csv_path)
            # (4.7.1, W-1) en la misma llamada: también el resumen predeterminado y los demás destinos conocidos
            pend = CIE.sincronizar_resumenes(c, pipeline.Pipeline.veredicto_auditoria) or CIE.retiradas_pendientes(c)
            print(f"resumen.py: no se escribe la fila como vigente: {motivo}" + (f" · RETIRADA PENDIENTE en {pend}" if pend else ""))
            return 5 if pend else 3
    # (4.12 §5) la selección del expediente se comprueba o se resuelve (en lectura) DESPUÉS de la vigencia; con motivo no se publica
    # ninguna fila
    import config_v2
    import seleccion_plantilla as SEL
    # (4.13 §3) protegido: una estructura inesperada en la selección o la configuración es un motivo, no una excepción
    import estructura_json as ESTR
    _r, _m = ESTR.protegido(SEL.resolver, c, config_v2.cargar(), contexto="selección de plantilla")
    _cfg, m_sel, nota_sel = _r if _r else (config_v2.cargar(), _m, None)
    if m_sel:
        print(f"resumen.py: SELECCIÓN DE PLANTILLA DETENIDA: {m_sel}: no se escribe ninguna fila")
        return 2
    if nota_sel:
        print(f"resumen.py: {nota_sel}")
    # (4.13 §4) la coherencia entre la acción final, el estado y los dos objetivos se exige también aquí: una ficha contradictoria
    # (escrita a mano o por una versión anterior) no se publica
    if isinstance(F.get("objetivo"), dict):
        import objetivo_v64 as OBJ
        contra = OBJ.contradicciones_salida(F.get("estado_analisis"), F.get("decision"), F.get("objetivo"))
        if contra:
            print("resumen.py: CONTRADICCIÓN en la ficha: " + " | ".join(contra)[:600] + ". No se publica")
            return 3
    # (4.7) antes de publicar, se retiran las aprobaciones registradas que ya no respalda una salida oficial vigente
    import pipeline as _p
    pend = CIE.sincronizar_resumenes(c, _p.Pipeline.veredicto_auditoria)
    if pend:
        print(f"resumen.py: RETIRADA PENDIENTE en {pend}: no se publica ninguna fila hasta completarla")
        return 5
    if not F.get("empresa"):
        # (4.10, §3.3) una ficha que no dice su empresa (p. ej., {}) no publica ninguna fila: antes podía aparecer una fila sin empresa
        # con la aprobación del pipeline
        print("resumen.py: la ficha oficial no dice su empresa: no se escribe ninguna fila")
        return 3
    pipe =leer_control(os.path.join(c, "estado_pipeline.json"))[0] or {}  # (4.9, Z-2) ilegible: sin interrumpir
    esc = F.get("escalera") or {}
    fm = F.get("fundamento_material") or {}
    rda = F.get("revision_datos_ausentes") or {}
    fila = {"empresa": F.get("empresa"), "fecha": F.get("fecha"), "estado_analisis": F.get("estado_analisis"),
            "causa_si_no_concluido": (F.get("causa_si_no_concluido") or {}).get("tipo"), "cubo_v1": (F.get("comparacion_etapa_1") or {}).get("cubo_v1"),
            "cubo_v2": F.get("cubo"), "motor": F.get("motor"), "precio": F.get("precio"), "moneda": F.get("moneda"),
            "precio_escenario_malo": esc.get("precio_escenario_malo"), "precio_si": esc.get("precio_si"), "ponderado": esc.get("ponderado"), "zona": esc.get("zona"),
            "accion": (F.get("decision") or {}).get("accion"), "fundamento_material": fm.get("resultado"), "estado_libro": F.get("estado_libro"),
            "palanca_mas_influyente": (F.get("palanca_mas_influyente") or {}).get("nombre"), "n_desviaciones": (F.get("desviaciones_justificadas") or {}).get("n"),
            "n_sin_juicio": (F.get("recuento_clases") or {}).get("sin_juicio"), "n_tecnico": (F.get("recuento_clases") or {}).get("tecnico"),
            "n_hipotesis_sin_fundamento": len(fm.get("hipotesis_sin_fundamento") or []) if fm else None,
            "comprobacion_conjunta": (F.get("comprobacion_conjunta") or {}).get("sobrevive") if F.get("comprobacion_conjunta") else None,
            "n_datos_ausentes": len(rda.get("revisados") or []) if rda else len(((F.get("que_falta") or {}).get("datos_ausentes") or [])),
            "n_datos_ausentes_materiales": sum(1 for x in (rda.get("revisados") or []) if x.get("material_para_conclusion_favorable")) if rda else None,
            "intentos_B": (pipe.get("intentos") or {}).get("fase_b"), "intentos_C": (pipe.get("intentos") or {}).get("fase_c"), "verificacion": (pipe.get("auditoria") if (CIE.ficha_cerrada(F) or pipe.get("auditoria") != "APROBADO") else None),
            "coste_estimado": pipe.get("coste_estimado"), "tiempo_min": pipe.get("tiempo_min")}
    ob = F.get("objetivo") if isinstance(F.get("objetivo"), dict) else None
    if ob is not None:
        rg = (ob.get("rango_calculado") or {}).get("precio_si") or [None, None]
        fila.update({"protocolo_objetivo": ob.get("protocolo"), "estado_del_objetivo": ob.get("estado_del_objetivo"),
                     "valor_calculado_condicional": ob.get("valor_calculado_condicional"), "precio_objetivo_emitido": ob.get("precio_objetivo_emitido"),
                     "objetivo_provisional": ob.get("provisional"), "hipotesis_que_condicionan": "; ".join(str(h.get("hipotesis")) for h in ob.get("hipotesis_que_lo_condicionan") or []),
                     "rango_precio_si_min": rg[0], "rango_precio_si_max": rg[1], "escenarios_calculados": (ob.get("rango_calculado") or {}).get("n_escenarios"),
                     "aptitud_de_uso": (F.get("aptitud_de_uso") or {}).get("caracter") if isinstance(F.get("aptitud_de_uso"), dict) else None})
    filas, cab = [], []
    if os.path.exists(csv_path):
        with open(csv_path, encoding="utf-8", newline="") as fh:
            rd = csv.DictReader(fh)
            filas = [r for r in rd if r.get("empresa") != fila["empresa"]]
            cab = rd.fieldnames or []
    cols = COLS + [k for k in COLS_V64 if ob is not None or k in cab]
    filas.append({k: ("" if v is None else v) for k, v in fila.items()})
    with open(csv_path, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for r in filas:
            w.writerow({k: r.get(k, "") for k in cols})
    if CIE.ficha_cerrada(F):
        CIE.registrar_publicacion(c, csv_path, fila["empresa"], (F.get("cierre") or {}).get("material_auditado"))  # (4.7) destino efectivo registrado
    print(f"OK: fila de {fila['empresa']} en {csv_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
