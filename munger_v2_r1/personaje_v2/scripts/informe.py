#!/usr/bin/env python3
"""informe.md por empresa (Anexo D §D.8): trece secciones en orden fijo; las que no aplican al estado dicen «No aplica en estado …».

Uso: informe.py CARPETA [--provisional]   (lee ficha.json y los JSON de las fases; escribe informe.md)
Con --provisional lee ficha_provisional.json y escribe informe_provisional.md, material para la auditoría (reparación del cierre, 4.6).
Marca de la conclusión (4.6): «con datos de etapa 1 incompletos» con sus causas cuando la ficha la trae. Alcance (4.6): si la ficha
trae `alcance` (alcance_v2.json), su aviso se repite dentro de las secciones 1, 6 y 7, junto a la conclusión, el DCF inverso, la
escalera, el precio de Sí y la zona; sin `alcance` no se añade ningún aviso.
Sin preámbulos ni cierres. Todo hecho con su fuente; todo juicio como juicio. Ningún tamaño de posición.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cierre_v2 as CIE  # noqa: E402


def cargar(c, n):
    p = os.path.join(c, n)
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else None


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


def f(x, pct=False):
    if x is None:
        return "—"
    if isinstance(x, float):
        if pct:
            return f"{x:.1%}"
        if abs(x) < 1:  # tasas y ratios (g = 0,015, S2C…): sin redondear a dos decimales (0,015 no es 0,01)
            return (f"{x:.4f}".rstrip("0").rstrip(".")) or "0"
        return f"{x:,.2f}"
    if isinstance(x, (list, tuple)):
        # sin repr de Python: con apóstrofos dentro, repr() imprime "…" y verify_quotes_v2 lo leería como una cita (Aarsleff, 4-nov-2026)
        return "; ".join(f(i, pct) for i in x)
    return str(x)


def txt(v):
    """Texto sin repr de Python (listas y dicts): ver DECISIONES 4-nov-2026 (Aarsleff)."""
    if isinstance(v, (list, tuple)):
        return "; ".join(txt(i) for i in v)
    if isinstance(v, dict):
        return "; ".join(f"{k}: {txt(i)}" for k, i in v.items())
    return str(v)


def plano(x):
    """(4.12) Valores de un aviso de dominio escritos sin la sintaxis JSON. verificar_todo.sh pasa juntos informe.md e
    informe_provisional.md a verify_quotes_v2, que lee como cita el texto entre dos comillas rectas: con los valores en JSON, la última
    comilla de un archivo se emparejaba con la primera del siguiente y el texto del informe entre ellas pasaba por cita no encontrada.
    Al repetir desde el paso 12 un expediente con avisos de dominio activos, los informes anteriores hacían fallar la verificación."""
    if isinstance(x, dict):
        return "{" + "; ".join(f"{k} = {plano(v)}" for k, v in x.items()) + "}"
    if isinstance(x, (list, tuple)):
        return "[" + ", ".join(plano(v) for v in x) + "]"
    return str(x).replace('"', "")


def distancias_con_denominador(precio, precio_si):
    """(4.11 §7) Las dos lecturas de la distancia entre el precio y el precio de Sí, cada una con su denominador."""
    if not (isinstance(precio, (int, float)) and isinstance(precio_si, (int, float)) and precio > 0 and precio_si > 0):
        return "Distancia al precio de Sí: no calculable."
    if precio == precio_si:
        return f"Distancias (denominador identificado): el precio actual {precio:.2f} coincide con el precio de Sí."
    sobre_si = (precio - precio_si) / precio_si
    sobre_p = (precio_si - precio) / precio
    rel = "por encima" if sobre_si > 0 else "por debajo"
    rel2 = "por debajo" if sobre_p < 0 else "por encima"
    return (f"Distancias (denominador identificado): el precio actual {precio:.2f} está un {abs(sobre_si):.2%} {rel} del precio de Sí {precio_si:.2f} "
            f"(diferencia ÷ precio de Sí); el precio de Sí está un {abs(sobre_p):.2%} {rel2} del precio actual (diferencia ÷ precio actual).")


def main():
    c = sys.argv[1]
    prov = "--provisional" in sys.argv[2:]
    F, ilegible = leer_control(os.path.join(c, "ficha_provisional.json" if prov else "ficha.json"))
    F = F or {}
    if not prov and not os.path.exists(os.path.join(c, "ficha.json")):
        # (4.6.1) sin ficha oficial no hay informe oficial: no se publica el contenido de las fases bajo ninguna ficha
        import pipeline
        import config_v2
        import estructura_json as ESTR
        # (4.13.1, H5) antes de sincronizar: una aprobación publicada sin ficha ni cierre registrado se retira también del estado interno
        _av, _mal = ESTR.protegido(CIE.asegurar_vigencia, c, pipeline.Pipeline.veredicto_auditoria, None, CIE.ruta_resumen(c, config_v2.cargar()), contexto="vigencia")
        motivo, archivo = _av if _av else (_mal, None)
        pend = CIE.sincronizar_resumenes(c, pipeline.Pipeline.veredicto_auditoria) or CIE.retiradas_pendientes(c)  # (4.7)
        print("informe.py: no se publica el informe oficial: no hay ficha.json oficial (para el material de la auditoría, usa --provisional)"
              + (f" · aprobación retirada: {motivo}" if motivo else "") + (f" · antecedente en {os.path.relpath(archivo, c)}" if archivo else "")
              + (f" · RETIRADA PENDIENTE en {pend}" if pend else ""))
        return 5 if (pend or _mal) else 3
    # (4.9, V-1) una ficha oficial ilegible pasa por la vigencia (y se retira); (4.10, §3.3) también la que perdió sus marcadores de
    # cierre mientras hay un cierre registrado (cierre_vigente.json): su correspondencia no depende de los marcadores actuales
    # (4.10, revisión interna R-1) y la que no está cerrada mientras el estado del pipeline sigue registrando una aprobación
    pipe0 = leer_control(os.path.join(c, "estado_pipeline.json"))[0] or {}
    if not prov and (CIE.ficha_cerrada(F) or ilegible or os.path.lexists(os.path.join(c, "cierre_vigente.json")) or pipe0.get("auditoria") == "APROBADO"):
        # (4.6.1) un informe oficial de una ficha cerrada solo se publica si la aprobación es válida para el material actual y la ficha
        # es la registrada en ese cierre; si no, se rechaza y las salidas anteriores quedan como antecedente
        import pipeline  # regla estricta de H2, sin cambios
        motivo = CIE.motivo_vigencia(c, pipeline.Pipeline.veredicto_auditoria, comprobar_informe=False)
        if motivo:
            import config_v2
            archivo = CIE.archivar_salidas(c, "informe.py: " + motivo, CIE.ruta_resumen(c, config_v2.cargar()))
            pend = CIE.sincronizar_resumenes(c, pipeline.Pipeline.veredicto_auditoria) or CIE.retiradas_pendientes(c)  # (4.7) destinos registrados
            print(f"informe.py: no se publica el informe oficial: {motivo}." + (f" Salidas oficiales anteriores archivadas en {os.path.relpath(archivo, c)}." if archivo else "") + (f" RETIRADA PENDIENTE en {pend}." if pend else ""))
            return 5 if pend else 3
    if not prov:
        # (4.13 §3) como pipeline, ficha y resumen: con una retirada pendiente (destino no actualizable o registro de publicaciones
        # ilegible) no se publica un informe oficial que siga presentando la aprobación
        pend0 = CIE.retiradas_pendientes(c)
        if pend0:
            print(f"informe.py: RETIRADA PENDIENTE en {pend0}: no se publica el informe oficial hasta completarla (ver {CIE.REGISTRO_RESUMEN})")
            return 5
    # (4.12 §5) la selección del expediente se comprueba o se resuelve (en lectura) DESPUÉS de la vigencia: una llamada a mano sin
    # MUNGER_CONFIG no publica un informe aparentemente V6.4 con la configuración V6.3; con motivo no se escribe nada
    import config_v2
    import seleccion_plantilla as SEL
    # (4.13 §3) protegido: una estructura inesperada en la selección o la configuración es un motivo, no una excepción
    import estructura_json as ESTR
    _r, _m = ESTR.protegido(SEL.resolver, c, config_v2.cargar(), contexto="selección de plantilla")
    _cfg, m_sel, nota_sel = _r if _r else (config_v2.cargar(), _m, None)
    if m_sel:
        print(f"informe.py: SELECCIÓN DE PLANTILLA DETENIDA: {m_sel}: no se escribe ningún informe")
        return 2
    if nota_sel:
        print(f"informe.py: {nota_sel}")
    # (4.13 §4) la coherencia entre la acción final, el estado y los dos objetivos se exige también aquí: una ficha contradictoria
    # (escrita a mano o por una versión anterior) no se publica
    if isinstance(F.get("objetivo"), dict):
        import objetivo_v64 as OBJ
        contra = OBJ.contradicciones_salida(F.get("estado_analisis"), F.get("decision"), F.get("objetivo"))
        if contra:
            print("informe.py: CONTRADICCIÓN en la ficha: " + " | ".join(contra)[:600] + ". No se publica")
            return 3
    aviso = CIE.linea_alcance(F.get("alcance"))
    con_aviso = lambda cuerpo: f"{aviso}\n\n{cuerpo}" if aviso else cuerpo  # noqa: E731
    fa, fb, fc = cargar(c, "fase_a.json") or {}, cargar(c, "fase_b.json") or {}, cargar(c, "fase_c.json") or {}
    refs = cargar(c, "referencias_mecanicas.json") or {}
    precio = F.get("escalera") or {}
    estado = F.get("estado_analisis")
    na = lambda: f"No aplica en estado {estado}."  # noqa: E731
    S = []
    # 1
    dec = F.get("decision") or {}
    linea = f"**Estado `{estado}` · cubo {F.get('cubo') or F.get('cubo_cualitativo_fase_a') or '—'} · acción {dec.get('accion') or 'ninguna'}**"
    if precio and "precio_si" in precio:
        linea += f" · precio {f(precio.get('precio'))} {F.get('moneda') or ''} · zona {precio.get('zona')} · precio de Sí {f(precio.get('precio_si'))} · precio esc. MALO {f(precio.get('precio_escenario_malo'))} · ponderado {f(precio.get('ponderado'))}"
    ob = F.get("objetivo") if isinstance(F.get("objetivo"), dict) else None  # (4.12 §4) solo V6.4 experimental
    if ob is not None:
        # (4.12 §4) objetivo estructurado: se lee del campo de la ficha, no de un párrafo; el rango no es un intervalo de confianza
        rg = (ob.get("rango_calculado") or {})
        hc = [str(h.get("hipotesis")) for h in ob.get("hipotesis_que_lo_condicionan") or []]
        tr = ob.get("tratamiento")

        def _lista(xs, n=4):  # en la línea de estado, las primeras; la lista entera va en la sección 14
            return "; ".join(xs[:n]) + (f"; y {len(xs) - n} más (sección 14)" if len(xs) > n else "")

        def _rango():  # (4.12 §4 y verificación, punto 10) el rango calculado y su ámbito también en la línea de estado, con cualquier tratamiento
            return ((f"; rango calculado del precio de Sí {f(rg['precio_si'][0])}–{f(rg['precio_si'][1])} en la activa y {rg.get('n_escenarios')} escenarios calculados, que no es un intervalo de confianza" if rg.get("precio_si") else "")
                    + (f"; no cubiertas por ese ámbito: {_lista(ob.get('hipotesis_no_cubiertas_por_el_ambito'))}" if ob.get("hipotesis_no_cubiertas_por_el_ambito") else ""))
        if tr in ("objetivo_emitido", "objetivo_condicionado") and ob.get("precio_objetivo_emitido") is not None:
            linea += f" · precio objetivo {f(ob['precio_objetivo_emitido'])}"
            if tr == "objetivo_condicionado":
                linea += f" **(condicionado, provisional: es el valor calculado condicional; lo condiciona{'n' if len(hc) > 1 else ''} {_lista(hc)}" + _rango() + ")**"
        elif tr == "objetivo_bloqueado":
            # (4.12, auditoría del cierre de bloqueo de Vidrala, punto 10) con el objetivo bloqueado la línea de estado también da el rango y su ámbito
            linea += (f" · **objetivo bloqueado** ({'protocolo de bloqueo' if ob.get('origen_del_bloqueo') == 'protocolo_de_bloqueo' else 'la acción no se sostiene en el ámbito calculado'}"
                      f"; valor calculado condicional, no emitido: precio de Sí {f(ob.get('valor_calculado_condicional'))}; lo condiciona{'n' if len(hc) > 1 else ''} {_lista(hc)}" + _rango() + ")")
        elif tr == "objetivo_sin_protocolo":
            linea += (f" · **ningún objetivo oficial**: falta el protocolo del objetivo y el objetivo depende de {_lista(hc)} "
                      f"(valor calculado condicional, no emitido: precio de Sí {f(ob.get('valor_calculado_condicional'))}" + _rango() + ")")
        elif dec.get("precio_objetivo"):
            linea += f" · precio objetivo {f(dec['precio_objetivo'])}"
    elif dec.get("precio_objetivo"):
        linea += f" · precio objetivo {f(dec['precio_objetivo'])}"
        hs1 = (F.get("fundamento_material") or {}).get("hipotesis_sin_fundamento") or []
        if dec.get("accion") == "esperar" and hs1 and F.get("configuracion_economica") is not None:  # solo V6.4: las salidas V6.3 no cambian
            # (4.11, revisión interna H7; Anexo B §B.6.7) con «esperar» y alguna hipótesis sin base, el objetivo es provisional también
            # en la línea de estado, con las hipótesis que lo condicionan
            def _corta(x, n=120):  # por palabra, nunca a mitad de una cifra o de un paréntesis (como H14)
                return x if len(x) <= n else x[:max(x.rfind(" ", 0, n - 2), 1)] + " …"
            linea += " **(provisional: lo condiciona" + ("n" if len(hs1) > 1 else "") + " " + "; ".join(_corta(str(h.get("celda") or h.get("hipotesis") or "?")) for h in hs1) + ")**"
    if dec.get("condicion"):
        linea += f" · condición: {dec['condicion']}"
    m1 = F.get("datos_etapa1_incompletos") or {}
    if m1:
        linea += f" · **{m1.get('marca')}** (causas: {'; '.join(str(x.get('dato')) + (' — ' + str(x.get('que')) if x.get('que') else '') for x in m1.get('causas') or [])})"
    apt = F.get("aptitud_de_uso") if isinstance(F.get("aptitud_de_uso"), dict) else None
    vef = F.get("verificacion_entradas") if isinstance(F.get("verificacion_entradas"), dict) else None
    if vef is not None:
        # (4.15, hito 2, I20) en todas las plantillas (también V6.3): la aptitud por entradas y el modo de la entrada efectiva con su procedencia.
        # Sin comillas angulares: verify_quotes_v2.py lee «…» como citas textuales y las busca en el corpus
        _ee = vef.get("entrada_efectiva") or {}
        _ap, _de = _ee.get("aplicada_en_paso_2") or {}, _ee.get("declarada") or {}
        _rs = vef.get("resumen") or {}
        linea += (f"\n\n> **Entradas financieras:** apta por entradas: {'sí' if vef.get('apto_por_entradas') else 'no'}"
                  + (f" ({_rs.get('comprobadas_universo')} de {_rs.get('universo')} celdas del universo comprobadas)" if _rs.get("universo") is not None and _rs.get("comprobadas_universo") is not None else "")
                  # (4.15, hito 2, H8) también con el registro apto, lo que no se contrastó (resumen) y, si no lo es, el motivo completo
                  + (f"; {str(_rs.get('resumen')).replace('«', '').replace('»', '')}" if _rs.get("resumen") else "")
                  + (f"; motivo: {str(_rs.get('motivo')).replace('«', '').replace('»', '')}" if not vef.get("apto_por_entradas") and _rs.get("motivo") else "")
                  + (f"; {str(vef.get('motivo_modo')).replace('«', '').replace('»', '')}" if vef.get("motivo_modo") else "")
                  + f". Entrada efectiva: modo aplicado en el paso 2: {_ap.get('modo') or 'sin registro'}"
                  + (f" (declarado en {_ap.get('declarado_en')})" if _ap.get("declarado_en") else (" (sin declaración del modo)" if _ap.get("modo") else ""))
                  + (f"; declarado ahora: {_de.get('modo')} ({_de.get('declarado_en') or 'sin declaración'})" if not _de.get("error") else f"; declaración actual con error: {str(_de.get('error')).replace('«', '').replace('»', '')}")
                  + ("; **el modo aplicado no coincide con el declarado**" if _ee.get("coinciden") is False else "")
                  + ". Apta para dinero real: no.")
    f1b = F.get("motor_a_f1") if isinstance(F.get("motor_a_f1"), dict) else None
    if f1b is not None:
        # (4.15, F1-IMPL) motor A con el perímetro F1: si una guarda bloquea, el resultado del motor A no se usa para una conclusión
        _d = f1b.get("diferencias_frente_a_A0_flujo_sin_crecimiento") or {}
        # (F1 · US GAAP) con el motor B, F1 solo se exige con US GAAP (puente de deuda): entonces la línea habla del motor B; si no, como antes
        _mf = "B" if (F.get("motor") == "B" and (f1b.get("vigencia") or {}).get("exigido")) else "A"
        _cf, _uf = f1b.get("condicionada") or {}, f1b.get("us_gaap") or {}
        _dif = _uf.get("diferencia_coste_lineal_menos_pagos") or {}
        _df = _dif.get("coste_menos_pagos_medio")
        # (F1 · US GAAP, ronda 2) R1-8: la cota de la conclusión condicionada, en dos cifras; D-US2 bis: el valor de la hoja y cuánto cambiaría contando
        # los pagos; R1-15: K3b «según lo declarado» cuando no se contrastó con líneas; R1-9: con el motor B la línea habla solo del puente de deuda
        _cota = str((((_cf.get("cota") or {}).get("resumen") or {}).get("texto")) or "")
        _bis = (_uf.get("D_US2_bis") or {}).get("texto")
        _k3 = f1b.get("K3") or {}
        _k3b_nota = " (según lo declarado o la hipótesis: sin contraste independiente con las líneas del expediente)" if _k3.get("K3b_contrastado") is False else ""
        linea += (f"\n\n> **Motor {_mf} · F1:** {('utilizable para una conclusión' + (' CONDICIONADA' if _cf else '') + ' (condición necesaria, no suficiente)') if f1b.get('utilizable_para_conclusion') else f'el resultado del motor {_mf} no se usa para una conclusión'}"
                  + (f"; condicionada a la {str(_cf.get('texto')).replace('«', '').replace('»', '')}" if _cf else "")
                  + (f"; {_cota}" if _cota else "")
                  + (f"; {str(_bis).replace('«', '').replace('»', '')}" if _bis else
                     f"; US GAAP: se cuentan los pagos del arrendamiento operativo (coste lineal − pagos = {_df:+.3f} de media en la ventana)" if _df is not None else
                     "; US GAAP: se cuentan los pagos del arrendamiento operativo (el coste publicado no es comparable con los pagos: la diferencia no se calcula)" if _dif.get("comparable") is False else "")
                  + (f"; bloquean: {', '.join(sorted({str(g.get('id')) for g in f1b.get('bloquean') or []}))}" if f1b.get("bloquean") else "")
                  + (f"; evaluación no vigente: {str((f1b.get('vigencia') or {}).get('motivo')).replace('«', '').replace('»', '')}" if (f1b.get("vigencia") or {}).get("vigente") is False else "")
                  + ((f"; puente de deuda: alquiler contado {_k3.get('K3b_alquiler_contado')} (los perímetros de la reinversión son del motor A y no se evalúan)" if _k3 else "") if _mf == "B" else
                     (f"; K3: alquiler contado {_k3.get('K3b_alquiler_contado')}{_k3b_nota}, caja base por dos vías {'conforme' if _k3.get('K3a_caja_base_dos_vias') else 'sin explicar'}" if _k3 else "")
                     + f"; perímetro declarado: {f1b.get('perimetro_declarado') or 'sin declarar'}")
                  + (f"; flujo sin crecimiento frente a A0 (diagnóstico): " + ", ".join(f"{k} {v:+.1f}" for k, v in _d.items() if k != "A0_total" and v is not None) if _d else "")
                  + ". Detalle en motor_a_f1_resultado.md. Apta para dinero real: no.")
        _pf = [g for g in (f1b.get("avisos") or []) if str(g.get("id")).startswith(("V-F1g (valores)", "V-F1k (valores)"))]
        if _pf:
            # (P-FOSO, D3 de la revisión de la implantación) las palancas frente a las medidas del perímetro, con cifras (informan; solo con A1/A2)
            linea += "\n\n> **Perímetro F1 · palancas por valores (P-FOSO):** " + " · ".join(
                f"{g.get('id')}: {str(g.get('detalle')).replace('«', '').replace('»', '')}" for g in _pf) + "."
    if apt:
        # (4.12 §9) aptitud de uso, separada de la auditoría (solo V6.4 experimental): ni «concluido» ni APROBADO la acreditan
        dist = str(apt.get("distinta_de_la_auditoria") or "")
        linea += (f"\n\n> **Aptitud de uso (evaluación de la entrega {apt.get('version')}, separada de la auditoría): {apt.get('caracter')}.** "
                  f"Permite un {apt.get('uso_que_permite')}. No es apto para {apt.get('no_apto_para')}. {dist[:1].upper()}{dist[1:]}. Evaluación: {apt.get('evaluacion')}.")
        ve = apt.get("verificacion_entradas") if isinstance(apt.get("verificacion_entradas"), dict) else None
        if ve is not None:
            # (4.14) verificación completa de las entradas financieras: condición necesaria para presentar la conclusión como apta para dinero real
            # (4.15, revisión independiente, hallazgo 16) sin «comprobadas_universo» (ficha anterior) no se da un recuento: «comprobadas» incluye los auxiliares
            _n_u = ve.get("comprobadas_universo")
            linea += (f" **Verificación de las entradas financieras:** " + (f"{_n_u} de {ve.get('universo')} celdas del universo comprobadas " if _n_u is not None
                      else "ficha anterior a la corrección del recuento: sin recuento del universo ")
                      + (f"({ve.get('comprobadas_calculo')} de {ve.get('universo_calculo')} de cálculo y {ve.get('comprobadas_juicio')} de {ve.get('universo_juicio')} usadas por el juicio) "
                         if ve.get("universo_calculo") is not None else "")
                      + f"(+{ve.get('auxiliares')} datos de origen auxiliares) · {ve.get('materiales_no_comprobadas')} materiales sin comprobar · "
                      + (f"{ve.get('lecturas_externas')} lecturas externas sin bytes · " if ve.get("lecturas_externas") else "")
                      # (4.15, segunda revisión independiente, N1 y N2) lo que no se contrastó y por qué, también con el registro apto
                      + (f"{ve.get('no_materiales')} de juicio declaradas no materiales ({ve.get('no_materiales_sin_revisar') or 0} sin revisar) · " if ve.get("no_materiales") else "")
                      + (f"{ve.get('datos_como_hipotesis')} datos tratados como hipótesis o convención · " if ve.get("datos_como_hipotesis") else "")
                      + (f"{ve.get('no_aplicables')} no aplicables · " if ve.get("no_aplicables") else "")
                      # (4.15, hito 2, U1) los derivados, con el límite del control automático
                      + (f"{ve.get('derivados_comprobados')} derivados comprobados (significado económico: revisión independiente) · " if ve.get("derivados_comprobados") else "") + 
                      f"{ve.get('discrepancias')} discrepancias · {ve.get('desactualizadas')} desactualizadas · apta por entradas: "
                      f"{'sí' if ve.get('apto_por_entradas') else 'no'}. Apta para dinero real: no"
                      + (f" ({'; '.join(apt.get('motivos_no_apto') or [])})" if apt.get("motivos_no_apto") else "") + ".")
    if prov:
        linea = f"> **Material provisional para la auditoría:** el estado `{estado}` lo propone la fase C; la salida oficial (`informe.md`) solo se escribe tras una auditoría APROBADO del material vigente.\n\n{linea}"
    S.append(("1. Estado, cubo y conclusión", con_aviso(linea)))
    # 2
    cambios = F.get("cambios_vs_etapa1") or []
    if cambios:
        t = ["| Celda | Etapa 1 | Etapa 2 | Decisión | Motivo | Evidencia y razonamiento |", "|---|---|---|---|---|---|"]
        t += [f"| {x['celda']} | {f(x.get('antes'))} | {f(x.get('despues'))} | {x.get('decision')} | {x.get('motivo')} | {x.get('evidencia_y_razonamiento')} |" for x in cambios]
        comp = F.get("comparacion_etapa_1") or {}
        if comp:
            t.append(f"\nCubo v1 {comp.get('cubo_v1')} → v2 {comp.get('cubo_v2')} · precio de Sí v1 {f(comp.get('precio_de_si_v1'))} → v2 {f(comp.get('precio_de_si_v2'))}. {comp.get('por_que_difieren') or ''}")
        S.append(("2. Qué cambió respecto a la etapa 1 y por qué", "\n".join(t)))
    else:
        S.append(("2. Qué cambió respecto a la etapa 1 y por qué", "Sin herencia registrada (la fase A no se ejecutó o no hay etapa 1)."))
    # 3
    sp = F.get("seis_preguntas") or {}
    S.append(("3. Las seis preguntas", "\n".join(f"- **{k.replace('_', ' ')}**: {txt(v)}" for k, v in sp.items()) if sp else na()))
    # 4
    esc = F.get("escenarios") or {}
    t = []
    for e in ("MALO", "NORMAL", "BUENO"):
        x = esc.get(e) or {}
        h = x.get("historia") or {}
        t.append(f"**{e}** (p = {f(x.get('probabilidad'))}; valor por acción {f(x.get('valor_accion'))}): {x.get('frase') or ''}\n" + ("\n".join(f"  - {k}: {txt(v)}" for k, v in h.items()) if isinstance(h, dict) else str(h)))
    S.append(("4. Los tres escenarios contados", "\n".join(t) if fa else na()))
    # 5
    if fb:
        t = ["| Palanca | Escenario | Referencia mecánica | Decisión | Desviación | Clase | Por qué |", "|---|---|---|---|---|---|---|"]
        for pal in ("crecimiento_1_5", "margen_objetivo", "s2c", "g_perpetuo", "roic_lp", "probabilidades"):
            for e in ("MALO", "NORMAL", "BUENO"):
                x = ((fb.get("palancas") or {}).get(pal) or {}).get(e) or {}
                if x:
                    t.append(f"| {pal} | {e} | {f(x.get('referencia_mecanica'))}{(' (' + x['referencia_no_disponible_motivo'] + ')') if x.get('referencia_no_disponible_motivo') else ''} | {f(x.get('valor'))} | {f(x.get('desviacion'))} | {x.get('clase')} | {x.get('porque')} |")
        q = fb.get("quiebra") or {}
        t.append(f"\nQuiebra C22 = {f(q.get('C22'))} (disparadores: {', '.join(q.get('disparadores') or []) or 'ninguno'}): {q.get('porque') or ''} · Exceso de caja C76 = {f((fb.get('exceso_caja') or {}).get('C76'))} · Mercado C24 = {f((fb.get('mercado') or {}).get('C24'))}")
        t.append(f"Referencias mecánicas: versión {refs.get('version_referencias_mecanicas')} (convención del ejercicio; no son estimaciones de Damodaran).")
        S.append(("5. Tabla de palancas: referencia mecánica → decisión → desviación → clase → por qué", "\n".join(t)))
    else:
        S.append(("5. Tabla de palancas", na()))
    # 6
    sem = F.get("semaforos") or {}
    res = cargar(c, "resultados.json") or {}
    if res:
        t = ["Semáforos (Diagnóstico V6, bloque 3):"] + [f"- {v[0]}: {' · '.join(str(x) for x in v[1:] if x)}" for v in sem.values()]
        pt = F.get("peso_terminal") or [None] * 3
        t.append(f"- Peso del terminal (MALO/NORMAL/BUENO): {f(pt[0], True)} / {f(pt[1], True)} / {f(pt[2], True)}")
        sj = F.get("salto_anio_11") or [None] * 4
        t.append(f"- Salto del año 11 (MALO/NORMAL/BUENO): {f(sj[1])} / {f(sj[2])} / {f(sj[3])}" if isinstance(sj, list) and len(sj) >= 4 else "- Salto del año 11: —")
        t.append(f"- DCF inverso: el precio actual descuenta un crecimiento de ventas a cinco años de {f(precio.get('g_impl_actual'), True) if isinstance(precio.get('g_impl_actual'), float) else precio.get('g_impl_actual')} (NORMAL: {f((res.get('palancas') or {}).get('C14'), True)})")
        torn = res.get("tornado") or {}
        t.append(f"- Tornado (información, no criterio): palanca más influyente {torn.get('mas_influyente')}; efectos {torn.get('efectos')}")
        S.append(("6. Lo que dice la hoja", con_aviso("\n".join(t))))
    else:
        S.append(("6. Lo que dice la hoja", na()))
    # 7
    if precio and "precio_si" in precio:
        t = [f"Escalera (convención experimental, k = {precio.get('k')}): precio del escenario MALO {f(precio.get('precio_escenario_malo'))} (no es un suelo de valor) · precio de Sí {f(precio.get('precio_si'))} · ponderado {f(precio.get('ponderado'))}. Zona del precio actual {f(precio.get('precio'))}: **{precio.get('zona')}**. La zona dice si el precio cumple la regla de precio con mis valores; la conclusión depende además del fundamento material (D10) y de los bloqueos (D17). Regla antigua de la hoja (mín(MALO, 0,75 × ponderado)): {f(precio.get('C156_regla_antigua'))}."]
        if F.get("configuracion_economica") is not None:
            # (4.11 §7) distancias con el denominador identificado (la 4.10.1 llamó «por encima» a una distancia medida sobre el precio)
            t.append(distancias_con_denominador(precio.get("precio"), precio.get("precio_si")))
        if precio.get("aviso_tasa_descuento_mas_influyente") is True:
            t.append("El valor depende sobre todo de tu rentabilidad exigida (r heredada, S-3).")
        fm = F.get("fundamento_material") or {}
        if fm:
            hs = fm.get("hipotesis_sin_fundamento") or []
            t.append(f"\nFundamento material (D10): {len(hs)} hipótesis sin fundamento suficiente → resultado **{fm.get('resultado')}**.")
            # (4.13, auditoría de vidrala_bloqueo) la lista D10 son celdas del libro; los parámetros de la configuración experimental sin
            # fundamento suficiente se cuentan aparte (sección 14), y no son «cero» por estar vacía la lista D10
            p_sf = (((F.get("objetivo") or {}).get("materialidad") or {}).get("hipotesis_sin_fundamento_suficiente") or [])
            if p_sf:
                t.append(f"La lista D10 recoge celdas del libro. Aparte, {len(p_sf)} parámetros de la configuración experimental no tienen fundamento "
                         f"suficiente ({', '.join(p_sf)}): lo que hacen con el objetivo está en la sección 14.")
            for h in hs:
                ad = h.get("alternativas_defendibles") or {}
                t.append(f"- {h.get('celda')} · {h.get('hipotesis')} · clase {h.get('clase')} · {h.get('porque_sin_fundamento')} · alternativas: {'rango ' + json.dumps(ad.get('rango'), ensure_ascii=False) + ' · ' if ad.get('hay_base') else 'SIN BASE PARA ACOTAR · '}{ad.get('evidencia')}")
            cc = F.get("comprobacion_conjunta") or {}
            if cc:
                eb = cc.get("escalera_bajo_combinacion") or {}
                t.append(f"- Comprobación conjunta: combinación {json.dumps(cc.get('combinacion'), ensure_ascii=False)} · {cc.get('coherencia_economica')} · bajo la combinación el precio de Sí sería {f(eb.get('precio_si'))} y la zona {eb.get('zona_precio_actual')} → **{'superada' if cc.get('sobrevive') else 'no superada'}**; superarla no es una garantía de seguridad.")
        de = F.get("dos_errores") or {}
        if de:
            t.append(f"\nLos dos errores opuestos: más cerca de «{de.get('mas_cerca_de')}» porque {de.get('porque')}")
        S.append(("7. Escalera de precios (convención experimental), fundamento material y los dos errores opuestos", con_aviso("\n".join(t))))
    else:
        S.append(("7. Escalera de precios, fundamento material y los dos errores opuestos", (precio or {}).get("sin_lectura") and f"Sin lectura de precio: {precio['sin_lectura']}" or na()))
    # 8
    cel = fc.get("celdas") or {}
    S.append(("8. Tesis y tesis inversa", f"**Tesis:** {cel.get('B101')}\n\n**Tesis inversa:** {cel.get('B102')}" if cel.get("B101") else na()))
    # 9
    pr = F.get("predicciones")
    S.append(("9. Predicciones", "\n".join(f"- {p['texto']} · comprobar el {p['fecha']} · probabilidad dado el NORMAL {f(p['prob'])}" for p in pr) if pr and pr[0].get("texto") else na()))
    # 10
    cb = F.get("cambiaria_de_cubo") or {}
    S.append(("10. Qué me haría cambiar de cubo", "\n".join(f"- {k}: {txt(v)}" for k, v in cb.items()) if cb else na()))
    # 11
    ac = F.get("autocomprobacion") or []
    S.append(("11. Autocomprobación", "\n".join(f"- **{x.get('sesgo')}**: {x.get('hallazgo')} → {x.get('cambio')}" for x in ac) if ac else na()))
    # 12
    t = []
    for k in ("lo_que_no_se", "que_no_sabria_munger"):
        for x in (fa.get(k) or []):
            t.append(f"- {x}")
    rda = F.get("revision_datos_ausentes") or {}
    for x in (rda.get("revisados") or []):
        t.append(f"- Dato ausente {x.get('dato')} ({x.get('que_falta')}): afecta a {x.get('conclusion_afectada')} · {'MATERIAL' if x.get('material_para_conclusion_favorable') else 'no material'} · {x.get('porque')}")
    if F.get("que_lo_resolveria"):
        t.append(f"- Lo que haría falta para continuar: {F.get('incertidumbre_pendiente') or ''} → {F.get('que_lo_resolveria')}")
    S.append(("12. Qué no sé y qué pediría", "\n".join(t) if t else "Nada registrado."))
    # 13
    ci = F.get("citas") or {}
    S.append(("13. Citas usadas", f"Munger: {ci.get('munger')} citas con página · Damodaran: {ci.get('damodaran')} citas con página (verificadas por verify_quotes_v2.py en verificacion_citas.txt)."))
    ce = F.get("configuracion_economica")
    if ce is not None:
        # (4.11) solo en expedientes V6.4: base, versión, configuración efectiva y límites; nada se presenta como adoptado
        pl = ce.get("plantilla") or {}
        ef = ce.get("efectivos_en_el_libro") or {}
        vc = ce.get("variantes_calculadas") or {}
        ev = ce.get("evaluacion_fase_c") or {}
        t = [f"- Plantilla: **{pl.get('version')}** (`{pl.get('archivo')}`, SHA-256 `{str(pl.get('archivo_sha256'))[:16]}…`; referencia `{str(pl.get('referencia_sha256'))[:16]}…`; configuración del pipeline `{pl.get('config')}`).",
             f"- Configuración económica (`configuracion_economica.json`, SHA-256 `{str(ce.get('configuracion_sha256'))[:16]}…`): {ce.get('resumen')}. {ce.get('naturaleza') or ''}",
             f"- Efectivos en el libro: tipo NOPAT {f(ef.get('t_nopat'))} (Historia {f(ef.get('t_historia'))}; escudo {f(ef.get('t_escudo'))}) · m0 {f(ef.get('m0_aplicado'))} (heredado {f(ef.get('m0_heredado'))}) · {ef.get('regla')} · estructura {ef.get('codigo_estructura')} · factores S2C × {f(ef.get('f_s2c'))}, ROIC × {f(ef.get('f_roic'))}, inversión fija × {f(ef.get('f_fija'))} · trazabilidad {ef.get('trazabilidad_completa')}"
             # (4.13 §7) libros V6.4.1: perímetro de la inversión de las bases de P-M1
             + (f" · perímetro de la inversión {ef.get('perimetro_efectivo')} (altas de derechos de uso en las bases {f(ef.get('altas_derechos_uso'))}; S2C histórico de referencia {f(ef.get('s2c_referencia_perimetro'))})" if "perimetro_efectivo" in ef else "") + ".",
             f"- Conciliación año a año y terminal (hoja «Conciliación B»): {'; '.join(f'{k} {v}' for k, v in (ce.get('conciliacion') or {}).items())}.",
             f"- Variantes calculadas ({vc.get('n')}, incluida la activa): zonas {', '.join(vc.get('zonas') or [])}; «la zona no cambia» solo se afirma de esas variantes ({'misma zona en todas' if vc.get('zona_igual_en_todas') else 'hay zonas distintas'}).",
             f"- Evaluación de la fase C del mantenimiento: {txt((ev.get('mantenimiento') or {}).get('evaluacion'))}"]
        t += [f"- Límite: {x}" for x in ce.get("limites") or []]
        for a in ce.get("avisos_de_dominio") or []:
            # (4.12 §5) dominios declarados, con valores y motivo; sin umbrales adoptados
            evf = a.get("evaluacion_fase_c") or {}
            if a.get("activo") is False:
                continue
            t.append(f"- Aviso de dominio «{a.get('id')}» ({'activo' if a.get('activo') else 'lectura sin umbral'}): {a.get('motivo')} · valores {plano(a.get('valores'))[:260]}"
                     + (f" · fase C: {'MATERIAL' if evf.get('material_para_conclusion') else 'no material'} — {txt(evf.get('consecuencia'))}" if evf else ""))
        ee = ce.get("entradas_economicas") or {}
        if ee.get("huella"):
            t.append(f"- Correspondencia de las variantes: {ee.get('n')} entradas económicas (huella `{str(ee.get('huella'))[:16]}…`) y configuración económica `{str(ee.get('configuracion_huella_economica'))[:16]}…`; "
                     "un cambio editorial no repite las valoraciones, uno económico sí.")
        if ob is not None:
            # (4.12 §4) protocolo, objetivo y materialidad separada (ensayo; ningún protocolo está adoptado como regla general)
            rg = ob.get("rango_calculado") or {}
            ma = ob.get("materialidad") or {}
            t += ["", "**Objetivo y materialidad (protocolo experimental 4.12; no adoptado)**",
                  f"- Protocolo declarado: {ob.get('protocolo') or 'ninguno'} · tratamiento: {ob.get('tratamiento')} · estado del objetivo: {ob.get('estado_del_objetivo')}"
                  + (f" ({ob.get('origen_del_bloqueo')})" if ob.get("origen_del_bloqueo") else "") + ".",
                  f"- Valor calculado condicional (precio de Sí): {f(ob.get('valor_calculado_condicional'))} · precio objetivo emitido: {f(ob.get('precio_objetivo_emitido')) if ob.get('precio_objetivo_emitido') is not None else 'ninguno'} · marca provisional: {'sí' if ob.get('provisional') else 'no'}.",
                  f"- Acción provisional {ob.get('accion_provisional')}; ¿se sostiene en el ámbito calculado?: {'sí' if ob.get('accion_sostenida_en_ambito') else 'no'}"
                  + (f" ({'; '.join(ob.get('motivos_no_sostenida'))})" if ob.get("motivos_no_sostenida") else "") + ".",
                  f"- Rango calculado: precio de Sí {f(rg['precio_si'][0])}–{f(rg['precio_si'][1])}, ponderado {f(rg['ponderado'][0])}–{f(rg['ponderado'][1])}, en la activa y {rg.get('n_escenarios')} escenarios ({', '.join(rg.get('escenarios') or [])}). {rg.get('naturaleza')}."
                  if rg.get("precio_si") and rg.get("ponderado") else f"- Rango calculado: ninguno ({rg.get('naturaleza')}).",
                  "- Hipótesis que condicionan el objetivo: " + ("; ".join(f"{h.get('hipotesis')} (falta: {txt(h.get('informacion_que_falta'))})" for h in ob.get("hipotesis_que_lo_condicionan") or []) or "ninguna") + ".",
                  "- No cubiertas por el ámbito calculado: " + ("; ".join(ob.get("hipotesis_no_cubiertas_por_el_ambito") or []) or "ninguna") + ".",
                  f"- Materialidad separada: datos ausentes materiales {', '.join(ma.get('datos_ausentes_materiales') or []) or 'ninguno'} · sin fundamento suficiente {', '.join(ma.get('hipotesis_sin_fundamento_suficiente') or []) or 'ninguna'} · "
                  f"materiales para la acción {', '.join(ma.get('materiales_para_la_accion') or []) or 'ninguno'} (no determinada: {', '.join(ma.get('materialidad_para_la_accion_no_determinada') or []) or 'ninguno'}) · "
                  f"materiales para el objetivo {', '.join(ma.get('materiales_para_el_objetivo') or []) or 'ninguno'}.",
                  f"- Motivo: {txt(ob.get('motivo'))}"]
            cob = ob.get("cobertura") if isinstance(ob.get("cobertura"), dict) else None
            if cob:
                # (4.13 §5) cobertura por hipótesis: qué se contrastó y con qué base se afirma cada materialidad para la acción
                bases = cob.get("base_de_la_materialidad_para_la_accion") or {}
                t.append("- Cobertura por hipótesis (4.13; contraste aislado, variación conjunta necesaria, variación conjunta o sin cobertura · base de la "
                         "materialidad para la acción): " + "; ".join(
                             f"{k}: {(v or {}).get('tipo')} · {bases.get(k) or '—'}" + (" · acción invariante en las variantes calculadas" if (v or {}).get("accion_invariante_en_variantes_calculadas") else "")
                             for k, v in (cob.get("por_parametro") or {}).items()) + ".")
                for j in cob.get("juicios_economicos") or []:
                    t.append(f"- Juicio económico (no es una constatación calculada) sobre {j.get('clave')}: material para la acción = {j.get('material_para_accion')}; "
                             f"evidencia: {txt('; '.join(j.get('evidencia') or []))}; inferencias: {txt('; '.join(j.get('inferencias') or []))}.")
                for j in cob.get("juicios_economicos_objetivo") or []:
                    t.append(f"- Juicio económico sobre el objetivo (no es una constatación calculada) de {j.get('clave')}: material para el objetivo = {j.get('material_para_objetivo')}; "
                             # (4.13, auditoría de vidrala_condicionado) con su evidencia, como el juicio sobre la acción
                             f"evidencia: {txt('; '.join(j.get('evidencia') or [])) if j.get('evidencia') else '—'}; inferencias: {txt('; '.join(j.get('inferencias') or []))}.")
                for j in cob.get("juicios_objetivo") or []:
                    # (4.14, encargo de cierre §5) el juicio PROPIO sobre el objetivo, separado del de la acción
                    crit = j.get("criterio") or {}
                    cc = j.get("comparado_con") or {}
                    filas_c = "; ".join(f"{c.get('variante')} {c.get('delta_eur'):+.2f} €" + ("" if c.get("atribuible") else " (no atribuible)")
                                        for c in j.get("contraste") or [] if isinstance(c.get("delta_eur"), (int, float))) or "sin contraste (cambio no definido)"
                    t.append(f"- Juicio sobre el objetivo de {j.get('clave')} (contrato 4.14): hipótesis «{txt(j.get('hipotesis'))}»; contraste {filas_c}; cobertura {j.get('cobertura')}; "
                             f"base {j.get('base')} · material {j.get('material')}; "
                             + ({"juicio_propio_del_agente": f"criterio propio del agente, no adoptado: {txt(crit.get('descripcion'))}",
                                 "redondeo_declarado": "criterio: el redondeo declarado (dos decimales)", "politica_adoptada": f"política registrada {crit.get('referencia')}",
                                 "ninguno": "sin criterio declarado"}.get(crit.get("origen"), "criterio no declarado"))
                             + (f"; comparado con {cc.get('referencia')} ({cc.get('valor_eur')} €; {txt(cc.get('fuente'))})" if cc else "")
                             + f"; límites: {txt('; '.join(j.get('limites') or []))}; razonamiento: {txt('; '.join(j.get('razonamiento') or [])) or '—'}.")
                if cob.get("sin_fundamento_excluidas_por_juicio"):
                    t.append("- Hipótesis sin fundamento suficiente excluidas del objetivo por juicio económico (con la comparación declarada; la pertinencia la revisa la "
                             f"auditoría): {', '.join(cob['sin_fundamento_excluidas_por_juicio'])}.")
                nd_o = [k for k, b in (cob.get("base_de_la_materialidad_para_el_objetivo") or {}).items() if b == "no_determinada"]
                if nd_o:
                    t.append(f"- Materialidad para el objetivo no determinada: {', '.join(nd_o)} (si no tienen fundamento suficiente, condicionan el objetivo).")
                t.append("- La invariancia de la acción vale solo para las variantes calculadas: no es la materialidad de un parámetro que esas variantes no identifican; "
                         "«no determinada» no equivale a «no material».")
        gv = ce.get("avisos_de_dominio_variantes")
        if gv:
            t.append("- Avisos de dominio en las variantes calculadas (4.13, por grupo): " + "; ".join(
                # (4.13, R17 y auditoría de vidrala_condicionado) un grupo que solo es una lectura sin umbral no está «activo en ninguna»: se dice dónde se lee
                f"{k}: activo en {', '.join(g.get('variantes') or []) or 'ninguna variante'}"
                + (f"; lectura sin umbral en {', '.join(g.get('lecturas') or [])}" if g.get("lecturas") else "")
                + (" · en la activa" if g.get("en_la_activa") else "")
                + (f" (f {g.get('f_minimo')}–{g.get('f_maximo')})" if g.get("f_minimo") is not None else "")
                + f" · afecta a {', '.join(g.get('afecta') or []) or '—'} · fase C: " + ("MATERIAL" if (g.get("evaluacion_fase_c") or {}).get("material_para_conclusion") else "no material")
                + f" — {txt((g.get('evaluacion_fase_c') or {}).get('consecuencia'))}" for k, g in gv.items()) + ".")
            if ob.get("lecturas_posibles"):
                t += [f"- Lectura posible con {k}: {v}" for k, v in ob["lecturas_posibles"].items()]
        # (4.13 §7) el título dice la versión registrada (V6.4 o V6.4.1 experimental); los informes V6.4 conservan el de antes
        S.append((f"14. Plantilla y configuración económica ({pl.get('version') or 'V6.4 experimental'}; no adoptada)", con_aviso("\n".join(t))))
    md = [f"# {F.get('empresa')} ({F.get('ticker')}) · informe del personaje v2 · {F.get('fecha')}\n"]
    for titulo, cuerpo in S:
        md.append(f"## {titulo}\n\n{cuerpo}\n")
    salida = "informe_provisional.md" if prov else "informe.md"
    open(os.path.join(c, salida), "w", encoding="utf-8").write("\n".join(md))
    if not prov and CIE.ficha_cerrada(F):
        CIE.registrar_informe(c)
    print(f"OK: {salida} ({len(S)} secciones)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
