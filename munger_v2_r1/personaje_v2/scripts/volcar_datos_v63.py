#!/usr/bin/env python3
"""Volcado de un libro V6.3 recalculado para los agentes del personaje v2 (encargo §3.2, §4.7 pasos 4 y 7).

Uso:
  volcar_datos_v63.py recalc/<E>_v63_datos.xlsx CARPETA_EMPRESA [--etapa1 DIR] [--referencias-mecanicas] [--config config_v2.json]

Escribe en CARPETA_EMPRESA:
  datos_v63.json   (máquina: anclas, series, cuartiles, análisis, diagnóstico, motor, evidencias, herencia)
  datos_v63.md     (agentes: datos con su evidencia, Historia, anclas, cuartiles, conciliación, estado técnico, HEREDADO)
  referencias_mecanicas.json y una sección en datos_v63.md, con --referencias-mecanicas (tras la fase A)
  datos_ausentes.json: añade los «no encontrado» de extracto_v63.md (sección 9) si existe, cuando afectan a una celda de juicio
"""
import argparse
import json
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import config_v2  # noqa: E402
import leer_v63 as L  # noqa: E402
import perimetro_f1 as PF  # noqa: E402
import referencias_mecanicas as RM  # noqa: E402

V53_JUICIO = ["C11", "C12", "C13", "C14", "C17", "C18", "C19", "C20", "C25", "C27", "C51", "C56", "C61", "C62", "B65", "C65", "D65",
              "B66", "C66", "D66", "B67", "C67", "D67", "B68", "C68", "D68", "B69", "C69", "D69", "C76", "C93", "C97", "C98", "B101", "B102", "C103", "C104"]
DATOS_ANALISIS = ["B3", "D3", "B4", "D4", "C24", "C26", "C28", "C31", "C32", "C33", "C34", "C37", "C38", "C40", "C41", "C42", "C46", "C47", "C48",
                  "C49", "C50", "C52", "C53", "C54", "C55", "C57", "C60", "C88", "C96"]
ETIQUETAS = {"B3": "Empresa", "D3": "Ticker", "B4": "Sector (texto libre)", "D4": "Fecha de análisis", "C24": "ROIC / ROCE (%)", "C26": "CFO ÷ beneficio neto",
             "C28": "Dilución (Recompra/Estable/Emite)", "C31": "¿Cobros o inventario crecen más rápido que ingresos?", "C32": "Goodwill ÷ activo total",
             "C33": "Deuda neta ÷ EBITDA (x)", "C34": "¿La caja cubre la deuda a corto?", "C37": "Precio actual", "C38": "Valor intrínseco de fuente externa",
             "C40": "FCF (mm) para FCF yield", "C41": "Capitalización (mm)", "C42": "EV/EBITDA (x)", "C46": "CFO medio (mm)", "C47": "Capex medio (mm)",
             "C48": "Intereses en financiación (mm, IFRS)", "C49": "Principal de arrendamientos (mm, IFRS 16)", "C50": "SBC (mm)", "C52": "FCF base (fórmula)",
             "C53": "Caja y equivalentes (mm)", "C54": "Deuda total (mm)", "C55": "Acciones diluidas (mm)", "C57": "Tasa sin riesgo", "C60": "CAGR acciones diluidas",
             "C88": "P/FCF histórico", "C96": "Fecha de la evidencia de gestión"}



def _sin_comilla_abierta(t):
    """Si el corte a 160 caracteres deja una « sin su » (cita truncada), se quita desde esa « (DECISIONES 3-nov-2026, Nike):
    verify_quotes_v2.py emparejaba la « abierta con la siguiente » de otro texto y daba decenas de citas «no encontradas»."""
    while t.count("«") > t.count("»"):
        t = t[:t.rindex("«")].rstrip()
    return t

def fmt(x):
    if x is None:
        return "—"
    if isinstance(x, float):
        return f"{x:.6g}"
    return str(x)


def leer_etapa1(dir_etapa1):
    """V5.3 evaluada + respuesta.md + juicio.json → bloque HEREDADO."""
    out = {"existe": False}
    if not dir_etapa1 or not os.path.isdir(dir_etapa1):
        return out
    xlsx = [f for f in os.listdir(dir_etapa1) if f.lower().endswith(".xlsx")]
    if xlsx:
        wb = L.abrir(os.path.join(dir_etapa1, xlsx[0]))
        ws = wb["Análisis"]
        celdas = {ref: L._v(ws[ref].value) for ref in V53_JUICIO}
        datos = {ref: L._v(ws[ref].value) for ref in DATOS_ANALISIS}
        obs = {}
        if "Control maestro" in wb.sheetnames:
            cm = wb["Control maestro"]
            for r in range(1, cm.max_row + 1):
                b = cm[f"B{r}"].value
                if isinstance(b, str) and b.startswith("Análisis!"):
                    obs[b.split("!")[1]] = {"E": L._v(cm[f"E{r}"].value), "F": L._v(cm[f"F{r}"].value), "N": L._v(cm[f"N{r}"].value), "fila": r}
        out.update({"existe": True, "libro": xlsx[0], "celdas": celdas, "datos": datos, "observaciones": obs})
    for nombre in ("respuesta.md", "juicio.json", "extracto.md"):
        p = os.path.join(dir_etapa1, nombre)
        if os.path.exists(p):
            out[nombre] = open(p, encoding="utf-8").read()
    return out


def seccion_md(t, herencia, refs=None, datos_ausentes=None):
    a, p, d, h, m, cm = t["analisis"], t["palancas"], t["diagnostico"], t["historia"], t["motor"], t["control_maestro"]
    filas_cm = {v["celda"]: v for v in cm["filas"].values()}
    md = []
    md.append(f"# DATOS V6.3 · {a.get('B3')} ({a.get('D3')}) · fecha de análisis {a.get('D4')}\n")
    md.append("Volcado automático (volcar_datos_v63.py). Todo lo de aquí es DATO de fase 1 o cálculo de la hoja, salvo el bloque HEREDADO, que son decisiones de la etapa 1 (hipótesis, no hechos: D3).\n")
    cv = t.get("configuracion_v64")
    if cv is not None:
        # (4.11) solo en libros V6.4 experimental: qué supuestos del motor B están activos y qué NO se hace en las fases
        md.append("## 0. Configuración V6.4 experimental del motor B (entrada de la orquestación; no la eligen ni la cambian las fases)\n")
        if cv.get("modo") == "Experimental" and not cv.get("valida") and refs is None and "solo es aplicable al motor B" in str(cv.get("motivo") or ""):
            # (4.12 §8) antes de la fase A el libro trae el motor de la etapa 1: la validez depende del motor que elija la fase A, y el
            # volcado no debe empujar hacia B (la fase A elige como si la configuración no existiera; otro motor es un límite legítimo)
            md.append(f"- Modo: **Experimental** · validez: **pendiente del motor que elija la fase A**. La configuración solo cubre el motor B y el libro trae "
                      f"todavía el motor de la etapa 1 ({d.get('motor') or '—'}).")
            md.append("- La fase A elige el motor por los criterios del personaje, como si esta configuración no existiera. Si elige otro motor, el expediente "
                      "termina en el límite del modelo experimental: es un resultado legítimo, no una falta de datos, y no se fuerza el motor B.")
        else:
            md.append(f"- Modo efectivo: **{cv.get('modo')}** · configuración válida: {cv.get('valida')} · motivo: {cv.get('motivo') or '—'}")
            md.append(f"- Resumen: {cv.get('resumen')}")
        if cv.get("modo") == "Experimental" and cv.get("valida"):
            md.append(f"- Tipos: Historia C52 {fmt(cv.get('t_historia'))} · aplicado a NOPAT {fmt(cv.get('t_nopat'))} · escudo de la deuda en r_op {fmt(cv.get('t_escudo'))}")
            md.append(f"- Margen de partida: heredado (Palancas C8) {fmt(cv.get('m0_heredado'))} · aplicado {fmt(cv.get('m0_aplicado'))} (el margen de partida NO es el margen objetivo del NORMAL)")
            md.append(f"- Reinversión: {cv.get('regla')} · circulante comercial ÷ ventas {fmt(cv.get('nwc_efectivo'))}")
            md.append(f"- P-M1: estructura {cv.get('codigo_estructura')} · familia {cv.get('familia_texto') or '—'} · λ {fmt(cv.get('lambda'))} · θ {fmt(cv.get('theta'))} · años {cv.get('convencion_anios') or '—'} · terminal {cv.get('convencion_terminal') or '—'} · ROIC {cv.get('roic_terminal') or '—'} · cartera {cv.get('cartera_texto')}")
            md.append(f"- Bases históricas H–L: D_hist {fmt(cv.get('D_hist'))} · F_hist {fmt(cv.get('F_hist'))} · exceso medio {fmt(cv.get('exceso_medio'))} · Rh {fmt(cv.get('Rh'))} · factores: S2C × {fmt(cv.get('f_s2c'))}, ROIC × {fmt(cv.get('f_roic'))}, inversión fija × {fmt(cv.get('f_fija'))}")
            if "perimetro_efectivo" in cv:  # (4.13 §7) libros V6.4.1
                md.append(f"- Perímetro de la inversión: {cv.get('perimetro_efectivo')} · altas de derechos de uso en las bases {fmt(cv.get('altas_derechos_uso'))} · S2C histórico de referencia con el perímetro {fmt(cv.get('s2c_referencia_perimetro'))}")
            md.append("- **Qué no se hace en las fases:** las palancas (S2C, ROIC, margen objetivo, g) se eligen con la misma base histórica que en la V6.3; la estructura ya aplica la reposición, el tipo y el margen de partida configurados. No se anticipan en las palancas (sería descontarlos dos veces) y no se presentan como convenciones adoptadas: son hipótesis de un ensayo.")
            # (4.12 §5) lecturas con bases parciales, identificadas donde se usan
            md.append("- **Lecturas con bases parciales (4.12):** " + (
                # (4.14, S4) con el perímetro NIIF 16 de la V6.4.1, las referencias del S2C se anclan en B155, no en una base heredada
                "la regla G7 de la gramática usa las bases heredadas (tipo de la Historia y S2C de la Historia, sin f); las referencias mecánicas del S2C se anclan en el S2C histórico del perímetro NIIF 16 (Configuración V6.4!B155), no en Historia!C53, y tampoco aplican f: no comprueban el modelo experimental."
                if str(cv.get("perimetro_efectivo") or "").upper().replace(" ", "") == "NIIF16" else
                "la regla G7 de la gramática y las referencias mecánicas usan las bases heredadas (tipo de la Historia y S2C sin f): no comprueban el modelo experimental.")
                      + (" El valor sin crecimiento (Diagnóstico B33:D33, Motor BL) y «cuánto pagas por crecer» no incluyen la cartera P0: son lecturas, no entran en el valor." if str(cv.get("cartera_texto") or "").startswith("P0") else ""))
        md.append("- Conciliación (hoja «Conciliación B»): " + "; ".join(f"{k} {v.get('comprobacion')}" for k, v in (cv.get("conciliacion") or {}).items()) + "\n")
    md.append("## 1. Estado técnico del libro\n")
    md.append(f"- Motor (Diagnóstico V6!C5): **{d['motor']}** · coherencia tipo/motor: {d['coherencia_tipo_motor']}")
    md.append(f"- Motor!B255 estado técnico: **{m['estado_tecnico_B255']}** · causa principal: {m['causa_tecnica_B256'] or '—'}")
    md.append(f"- Motor!B266 estado del libro: {m['estado_libro_B266']} · B253 comparable precio↔valor: {m['comparable_B253']} · B252 bloqueo del valor: {m['bloqueo_valor_B252']}")
    md.append(f"- Moneda del modelo (Control maestro!H4): {cm['cabecera']['H4_moneda']} · moneda de cotización (Palancas!C48): {p['C48']} · unidad: {cm['cabecera']['J4_unidad']} · norma contable: {cm['cabecera']['L4_norma']} · ratio ADR (D5): {cm['cabecera']['D5_ratio_adr']}")
    causas = [x for x in d["causas_activas"] if x]
    md.append("- Causas activas: " + ("; ".join(causas) if causas else "ninguna"))
    md.append("- Reglas del motor que no están en OK/N/A: " + ("; ".join(f"{r['id']} {r['resultado']} ({r['causa']})" for r in m["reglas"] if r["resultado"] not in ("OK", "N/A")) or "ninguna") + "\n")
    if t.get("perimetro_f1"):
        # (P-FOSO, D2 del dictamen del perímetro) solo con F1 declarado en A1_sin_ROU o A2_propio: sin él, el volcado no cambia
        md.extend(PF.seccion_md(t["perimetro_f1"], d.get("motor")))
    md.append("## 2. Datos de Análisis con su evidencia (Control maestro)\n")
    md.append("| Celda | Concepto | Valor | Clasificación (F) | Documento (J) | Página (L) | Observación (N) |\n|---|---|---|---|---|---|---|")
    for ref in DATOS_ANALISIS:
        f = filas_cm.get(f"Análisis!{ref}", {})
        md.append(f"| {ref} | {ETIQUETAS.get(ref, '')} | {fmt(a.get(ref))} | {fmt(f.get('F'))} | {fmt(f.get('J'))} | {fmt(f.get('L'))} | {fmt(f.get('N'))} |")
    md.append(f"\nFCF base (C52, fórmula): {fmt(a.get('C52'))} · Peso de la SBC (C59): {fmt(a.get('C59'))} · Precio (C37): {fmt(a.get('C37'))} {p['C48'] or ''} con fecha {p['C45']} · Acciones (C55): {fmt(a.get('C55'))} con fecha {p['C46']} · Capitalización (C41): {fmt(a.get('C41'))} · Causa de diferencia de capitalización (Palancas!C47): {p['C47']}\n")
    md.append("## 3. Historia (10 años; una celda vacía es DESCONOCIDO, nunca cero)\n")
    anios = h["partidas"]["anio"]
    md.append("| Partida | " + " | ".join(fmt(x) for x in anios) + " | Fuente (M) |\n|---|" + "---|" * 10 + "---|")
    for nombre in L.FILAS_HISTORIA.values():
        if nombre == "anio":
            continue
        md.append(f"| {nombre} | " + " | ".join(fmt(x) for x in h["partidas"][nombre]) + f" | {fmt(h['notas'].get(nombre))} |")
    md.append("\n### Series calculadas por la hoja\n")
    md.append("| Serie | " + " | ".join(fmt(x) for x in anios) + " |\n|---|" + "---|" * 10)
    for nombre, serie in h["series"].items():
        md.append(f"| {nombre} | " + " | ".join(fmt(x) for x in serie) + " |")
    md.append("\n### Anclas (Historia C43:C66)\n")
    md.append("| Ancla | Celda | Valor |\n|---|---|---|")
    for ref, nombre in L.ANCLAS.items():
        rot = " (todo el capital: con F1 en el perímetro declarado, solo frente al sector; ver 1 bis)" if (t.get("perimetro_f1") and ref in ("C54", "C55")) else ""
        md.append(f"| {nombre}{rot} | {ref} | {fmt(h['anclas'][nombre])} |")
    md.append("\n## 4. Sector y riesgo país que usa la hoja\n")
    md.append(f"- Sector de Damodaran (Palancas!C7): **{p['C7']}** · etapa (C5): {p['C5']} · caso especial (C6): {p['C6']} · base del margen (C8): {p['C8']} · I+D capitalizada (C9/C10): {p['C9']} / {p['C10']}")
    s = p["sector"]
    md.append(f"- Crecimiento de ventas del sector (3 años) Q1 / mediana / Q3: {fmt(s['crecimiento_q1'])} / {fmt(s['crecimiento_mediana'])} / {fmt(s['crecimiento_q3'])} · media propia (F14): {fmt(p['media_propia']['crecimiento'])}")
    md.append(f"- Margen operativo del sector Q1 / mediana / Q3: {fmt(s['margen_q1'])} / {fmt(s['margen_mediana'])} / {fmt(s['margen_q3'])} · media propia (F15): {fmt(p['media_propia']['margen'])}")
    md.append(f"- ROIC medio del sector (H18): {fmt(s['roic_media'])} · ROIC propio 5 años (F18): {fmt(p['media_propia']['roic'])}")
    md.append(f"- S2C MEDIO del sector (ventas ÷ capital; medida distinta de la palanca) Q1 / mediana / Q3: {fmt(s['s2c_medio_q1'])} / {fmt(s['s2c_medio_mediana'])} / {fmt(s['s2c_medio_q3'])} · propio (F19): {fmt(p['media_propia']['s2c_medio'])} · S2C MARGINAL propio (F16, la palanca): {fmt(p['media_propia']['s2c_marginal'])}")
    md.append(f"- Tasa sin riesgo (Análisis!C57): {fmt(a.get('C57'))} · r del inversor (C56, heredada): {fmt(a.get('C56'))} · r mínima (Diagnóstico!C17): {fmt(d['r_minima'])} · {d['r_vs_minima']} · r operativa del motor B (C15): {fmt(d['r_operativa'])}")
    geo = [g for g in p["geografia"] if g[0]]
    md.append("- Reparto geográfico (Palancas A28:B33): " + ("; ".join(f"{g[0]} {fmt(g[1])} (prima {fmt(g[2])})" for g in geo) if geo else "vacío") + "\n")
    md.append("## 5. Conciliación precio × acciones ≈ capitalización y f\n")
    md.append(f"- Parámetros de la hoja: tolerancia {fmt(d['parametros']['C91'])}, corte {fmt(d['parametros']['C92'])}, separación máxima de fechas {fmt(d['parametros']['C93'])} días")
    md.append(f"- Reglas V22, V26, V27, V28: " + "; ".join(f"{r['id']} {r['resultado']}" + (f" ({r['causa']})" if r['causa'] else "") for r in m["reglas"] if r["id"] in ("V22", "V26", "V27", "V28")))
    md.append(f"- f (fugas al accionista, Diagnóstico!C12 = Historia!C58): {fmt(d['f'])} · V0: {fmt(d['V0'])} · m0: {fmt(d['m0'])} · t: {fmt(d['t'])}\n")
    if herencia.get("existe"):
        md.append("## 6. HEREDADO de la etapa 1 (V5.3 decidida por el personaje v1) — hipótesis, no hechos (D3)\n")
        md.append(f"Libro: {herencia['libro']}. Cada celda con su Observación v1. El crecimiento del FCF (B67:D67) ya no se escribe en la V6.3 (fórmula): se muestra solo como contexto.\n")
        md.append("| Celda | Valor etapa 1 | Observación v1 (Control maestro N) |\n|---|---|---|")
        for ref in V53_JUICIO:
            o = herencia["observaciones"].get(ref, {})
            md.append(f"| {ref} | {fmt(herencia['celdas'].get(ref))} | {fmt(o.get('N'))} |")
        if herencia.get("juicio.json"):
            md.append("\n### juicio.json de la etapa 1\n```json\n" + herencia["juicio.json"].strip()[:20000] + "\n```")
        if herencia.get("respuesta.md"):
            md.append("\n### respuesta.md de la etapa 1 (cubo, precio de Sí v1, seis preguntas, qué le haría cambiar de cubo)\n\n" + herencia["respuesta.md"].strip()[:30000] + "\n")
    else:
        md.append("## 6. HEREDADO de la etapa 1\n\nNo se encontró carpeta etapa1/ (S-1): las 34 celdas heredadas se deciden sin herencia y se marcan así.\n")
    if refs:
        md.append("## 7. REFERENCIAS MECÁNICAS por palanca (convención del ejercicio, Anexo B §B.2; NO son estimaciones de Damodaran)\n")
        md.append(f"Versión de las reglas: {refs['version_referencias_mecanicas']} · motor {refs['motor']} · tasa del motor {fmt(refs['tasa_del_motor'])} · rf {fmt(refs['rf'])}. La fase B parte de aquí y se desvía con motivo; la clase «sin juicio propio» solo puede copiar una referencia disponible.\n")
        md.append("| Palanca | MALO_ref | NORMAL_ref | BUENO_ref | Regla / motivo de no disponibilidad | Anclas usadas | Criterio relacionado (no respalda la cifra) |\n|---|---|---|---|---|---|---|")
        for k, v in refs["palancas"].items():
            if "NORMAL" not in v:
                continue
            regla = v.get("referencia_no_disponible_motivo") or v.get("regla", "")
            md.append(f"| {k} | {fmt(v.get('MALO'))} | {fmt(v.get('NORMAL'))} | {fmt(v.get('BUENO'))} | {regla} | {json.dumps(v.get('anclas_usadas', {}), ensure_ascii=False)} | {v.get('criterio_relacionado', '')} |")
        q = refs["palancas"]["quiebra"]
        md.append(f"\n- Quiebra (C22/C23): referencia {fmt(q['C22'])} / {fmt(q['C23'])} · disparadores: {'; '.join(q['disparadores']) or 'ninguno'} · {q['regla']}")
        md.append(f"- Exceso de caja (C76): {fmt(refs['palancas']['exceso_caja']['C76'])} · Tamaño de mercado (C24): {refs['palancas']['mercado']['referencia_no_disponible_motivo']}")
        md.append("- Rentabilidad marginal implícita (S2C × margen × (1 − t)) y salto del año 11 con las referencias: " + json.dumps(refs["implicaciones_con_referencias"], ensure_ascii=False))
        notas = [f"{k}: {'; '.join(v.get('notas', []))}" for k, v in refs["palancas"].items() if v.get("notas")]
        if notas:
            md.append("- Notas del cálculo: " + " | ".join(notas))
        md.append("")
    if datos_ausentes is not None:
        md.append("## 8. DATOS AUSENTES no bloqueantes (entrada de la revisión de la fase C, S-19)\n")
        if datos_ausentes:
            md.append("| Dato | Nivel | De dónde debería venir | Nota |\n|---|---|---|---|")
            for x in datos_ausentes:
                md.append(f"| {x.get('dato')} | {x.get('nivel')} | {x.get('origen_esperado')} | {x.get('nota', '')} |")
        else:
            md.append("Ninguno.")
        md.append("")
    return "\n".join(md)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("recalc_xlsx")
    ap.add_argument("carpeta")
    ap.add_argument("--etapa1")
    ap.add_argument("--referencias-mecanicas", action="store_true")
    ap.add_argument("--config", default=None)  # (4.11) None → MUNGER_CONFIG (la del pipeline) o config_v2.json
    a = ap.parse_args()
    cfg = config_v2.cargar(a.config)
    wb = L.abrir(a.recalc_xlsx)
    t = L.todo(wb)
    etapa1 = a.etapa1 or os.path.join(a.carpeta, "etapa1")
    herencia = leer_etapa1(etapa1)
    t["herencia"] = {k: v for k, v in herencia.items() if k not in ("respuesta.md", "extracto.md", "juicio.json")}
    os.makedirs(a.carpeta, exist_ok=True)
    # (P-FOSO, 18-nov-2026; dictamen del perímetro, D2) con F1 declarado en A1_sin_ROU o A2_propio, las fases y las referencias reciben el
    # perímetro, los retornos del capital propio y la regla de la decisión; sin declaración (o con A0/A3) no se añade nada
    pf = PF.desde_datos(t, PF.leer_declaracion(a.carpeta), a.carpeta)
    if pf:
        import hashlib
        pf["anclas_capa_f1"] = PF.anclas_capa(a.carpeta, hashlib.sha256(open(a.recalc_xlsx, "rb").read()).hexdigest())
        t["perimetro_f1"] = pf
    refs = None
    if a.referencias_mecanicas:
        refs = RM.calcular(t, cfg)
        json.dump(refs, open(os.path.join(a.carpeta, "referencias_mecanicas.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    # datos ausentes: parte del pipeline (comprobar_entrada) + «no encontrado» del extracto
    da_path = os.path.join(a.carpeta, "datos_ausentes.json")
    datos_ausentes = json.load(open(da_path, encoding="utf-8")) if os.path.exists(da_path) else None
    ex_path = os.path.join(a.carpeta, "extracto_v63.md")
    if datos_ausentes is not None and os.path.exists(ex_path):
        txt = open(ex_path, encoding="utf-8").read()
        m = re.search(r"#+\s*9\.?\s*Lo que no encontré(.*)", txt, re.S | re.I)
        if m:
            ya = {x.get("dato") for x in datos_ausentes}
            for linea in m.group(1).strip().splitlines():
                linea = linea.strip(" -*·\t")
                if linea and len(linea) > 3 and linea[0] != "#" and ("extracto_v63: " + linea) not in ya:
                    datos_ausentes.append({"dato": "extracto_v63: " + _sin_comilla_abierta(linea[:160]), "nivel": "no bloqueante", "origen_esperado": "informes de la empresa (fase 1 / extracción)",
                                           "nota": "declarado «no encontrado» por el agente de extracción; la fase C decide si afecta a una celda de juicio"})
            json.dump(datos_ausentes, open(da_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(t, open(os.path.join(a.carpeta, "datos_v63.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    md = seccion_md(t, herencia, refs, datos_ausentes)
    open(os.path.join(a.carpeta, "datos_v63.md"), "w", encoding="utf-8").write(md)
    print(f"OK: datos_v63.md ({len(md.split())} palabras) y datos_v63.json en {a.carpeta}" + (" · referencias_mecanicas.json" if refs else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
