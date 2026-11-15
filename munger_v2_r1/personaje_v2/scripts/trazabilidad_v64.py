#!/usr/bin/env python3
"""Cadena de trazabilidad de una valoración (encargo 4.12 §5): fuente → dato extraído → transformación o supuesto → entrada del modelo
→ cálculo → resultado → conclusión. Solo lee el expediente y escribe tres archivos:
  cadena_trazabilidad.json · cadena_trazabilidad.md · verificacion_trazabilidad.txt (PASS / AVISO; no hay FAIL: no decide nada).

Qué recoge:
  - una entrada por cada entrada económica (entradas_economicas.instantanea: las 58 materiales de la valoración y de la lectura del
    precio, con la Historia expandida, y en la V6.4 las de «Configuración V6.4» sin metadatos), con un IDENTIFICADOR por clase, que
    no se mezclan: D- dato publicado · C- cálculo derivado de datos publicados · V- convención · H- hipótesis (juicio);
  - su fuente y su tratamiento tal como los declara el libro (Control maestro: documento, página, período, unidad, ajuste o criterio,
    clasificación y Observación con la clase) o, en la configuración V6.4, su tabla de trazabilidad;
  - la magnitud (stock en una fecha, flujo de un ejercicio, precio, número de acciones, tasa o parámetro, metadato), el uso en el
    cálculo (motores y condición de la relación independiente) y el valor que entra en el modelo;
  - el resultado (vector de escenarios, ponderado, precio de Sí y zona) y la conclusión de la fase C con su objetivo, si existen;
  - las fechas separadas (ejecución, base, precio, acciones, revisión de fuentes).
Comprobaciones (AVISO, nunca recortes ni umbrales económicos adoptados): unidad declarada y coherente; signos de las magnitudes que
no pueden ser negativas; (4.12, revisión interna R4) en el precio, la capitalización y las acciones, fechas del período o de la
transformación distintas de la declarada y un resultado de la transformación («… = N») distinto del valor que entra en el modelo; un cero que depende de un dato pendiente de verificación (nunca «desconocido = cero») y celdas vacías;
fechas que faltan; un stock del circulante que no nombra el ejercicio base; ceros de la configuración sin fuente.
Uso: trazabilidad_v64.py CARPETA LIBRO_EVALUADO.xlsx
"""
import json
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import configuracion_economica as CE  # noqa: E402
import entradas_economicas as EE  # noqa: E402

# magnitud de cada entrada de la relación (por id)
MAGNITUD = {"precio": "precio en una fecha", "capitalizacion": "stock en una fecha", "acciones": "número de acciones en una fecha",
            "cfo_media": "flujo (media de ejercicios)", "capex_media": "flujo (media de ejercicios)", "int_fin_media": "flujo (media de ejercicios)",
            "leases_media": "flujo (media de ejercicios)", "sbc_media": "flujo (media de ejercicios)", "h_anios": "metadato (ejercicio)",
            "h_ventas": "flujo del ejercicio", "h_ebit": "flujo del ejercicio", "h_da": "flujo del ejercicio", "h_beneficio": "flujo del ejercicio",
            "h_tipo": "tasa del ejercicio", "h_capex": "flujo del ejercicio", "h_circulante": "flujo del ejercicio (aumento del circulante)",
            "h_intereses": "flujo del ejercicio", "h_patrimonio": "stock a cierre", "h_deuda": "stock a cierre", "h_arrend": "stock a cierre",
            "h_caja": "stock a cierre", "h_pensiones": "stock a cierre", "h_minoritarios": "stock a cierre", "moneda_cotizacion": "metadato",
            "moneda_modelo": "metadato", "ratio_adr": "metadato", "unidad": "metadato", "norma": "metadato",
            "h_adquisiciones": "flujo del ejercicio"}  # (4.12, revisión interna R1) solo V6.4: bases de P-M1
MAG_CONFIG = {"B4": "metadato (modo)", "B11": "tasa (parámetro)", "B16": "convención", "B21": "tasa (margen de partida)", "B28": "regla",
              "B29": "stock a la fecha del balance base", "B30": "stock a la fecha del balance base", "B31": "stock a la fecha del balance base",
              "B36": "estructura", "B37": "familia", "B38": "parámetro", "B39": "parámetro", "B40": "convención", "B41": "convención", "B42": "convención",
              "B43": "regla", "B44": "flujo anual (amortización de la cartera)", "B45": "stock a la fecha del balance base (valor neto)",
              "B46": "flujo del ejercicio", "B47": "flujo del ejercicio", "B48": "flujo del ejercicio", "B49": "flujo del ejercicio", "B50": "flujo del ejercicio",
              # (4.13 §7) V6.4.1: perímetro de la inversión y altas de derechos de uso (flujos de cada ejercicio H–L)
              "B146": "convención (perímetro)", **{f"B{i}": "flujo del ejercicio (altas de derechos de uso)" for i in range(147, 152)}}
# signo esperado de las series y datos que no pueden ser negativos (las demás, p. ej. patrimonio o aumento del circulante, sí pueden)
NO_NEGATIVAS = {"precio", "capitalizacion", "acciones", "h_ventas", "h_da", "h_capex", "h_deuda", "h_arrend", "h_caja", "h_minoritarios", "capex_media", "h_anios"}
CLASE_ID = {"dato publicado": "D", "derivado de datos publicados": "C", "convención": "V", "hipótesis": "H"}


MESES = {"ene": 1, "feb": 2, "mar": 3, "abr": 4, "may": 5, "jun": 6, "jul": 7, "ago": 8, "sep": 9, "oct": 10, "nov": 11, "dic": 12}


def _fechas_en(texto):
    """Fechas «AAAA-MM-DD» y «D-mmm-AAAA» (meses en español abreviados) de un texto, como «AAAA-MM-DD»."""
    out = set()
    for m in re.finditer(r"\b(\d{4})-(\d{2})-(\d{2})\b", texto):
        out.add(f"{m.group(1)}-{m.group(2)}-{m.group(3)}")
    for m in re.finditer(r"\b(\d{1,2})-(ene|feb|mar|abr|may|jun|jul|ago|sep|oct|nov|dic)[a-z]*\.?-(\d{4})\b", texto, re.I):
        out.add(f"{m.group(3)}-{MESES[m.group(2).lower()]:02d}-{int(m.group(1)):02d}")
    return out


def _num_es(t):
    """«2.444,4» → 2444.4 · «35.182.858» → 35182858 · «45,60» → 45.6 · «3169.97» → 3169.97."""
    t = t.strip().rstrip(".,")
    if "," in t:
        t = t.replace(".", "").replace(",", ".")
    elif re.fullmatch(r"\d{1,3}(\.\d{3})+", t):
        t = t.replace(".", "")
    try:
        return float(t)
    except ValueError:
        return None


def _resultados_en(texto):
    """Los resultados que escribe una transformación: los números que siguen a «=»."""
    return [x for x in (_num_es(m.group(1)) for m in re.finditer(r"=\s*([\d.,]*\d)", texto)) if x is not None]


def _coincide(x, v):
    return any(abs(x * f - v) <= 1e-3 * max(abs(v), 1e-12) for f in (1e-6, 1e-3, 1.0, 1e3, 1e6))


def _cargar(c, n):
    p = os.path.join(c, n)
    try:
        return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else None
    except (OSError, ValueError):
        return None


def control_maestro(libro):
    """{celda declarada (columna B): fila de evidencia} de Control maestro (filas con una celda en la columna B)."""
    from openpyxl import load_workbook
    wb = load_workbook(libro, read_only=True)
    ws = wb["Control maestro"]
    cab = ("etapa", "celda", "concepto", "naturaleza", "estado", "clasificacion", "periodo", "unidad", "tipo_fuente", "documento", "url", "pagina", "ajuste", "observaciones")
    out = {}
    unidad = ws["J4"].value
    for fila in ws.iter_rows(min_row=17, max_row=200, max_col=14, values_only=True):
        if isinstance(fila[1], str) and "!" in fila[1]:
            out[fila[1].strip()] = dict(zip(cab, fila))
    wb.close()
    return out, unidad


def _clase_obs(obs):
    m = re.search(r"\[Clase:\s*([^\]]+)\]", str(obs or ""))
    return m.group(1).strip() if m else None


def clasificar(e, ev):
    """Prefijo de identificador (D, C, V o H) de una entrada de la relación con su evidencia."""
    if e["tipo"] == "hipótesis":
        return "V" if _clase_obs((ev or {}).get("observaciones")) == "convención" else "H"
    txt = " ".join(str((ev or {}).get(k) or "") for k in ("tipo_fuente", "documento", "periodo", "ajuste")).lower()
    if "deriv" in txt or "÷" in txt or "media " in txt or e["id"].endswith("_media") or e["id"] == "h_tipo":
        return "C"
    return "D"


def construir(c, libro):
    inst = EE.instantanea(libro)
    cm, unidad = control_maestro(libro)
    conf = _cargar(c, "configuracion_economica.json") or {}
    res, precio, fc = _cargar(c, "resultados.json") or {}, _cargar(c, "precio.json") or {}, _cargar(c, "fase_c.json") or {}
    meta = _cargar(c, "fase1_metadatos.json") or {}
    da = _cargar(c, "datos_ausentes.json") or []
    pendientes = {str(x.get("dato") or "").replace("evidencia ", ""): x for x in da}
    avisos, entradas = [], []
    # (4.12, revisión interna R1) en un libro V6.4 también la fila 13 de la Historia, que entra en las bases de P-M1 (en un libro V6.3 no
    # está en la instantánea y se salta)
    rel = {e["celda"].replace("'", ""): e for e in EE.relacion_v64()}
    # entradas de la relación (agrupadas como las declara la relación: una serie de la Historia es una entrada)
    for celda_rel, e in rel.items():
        celdas = [f"{h}!{r}" for h, r in EE._expandir(e["celda"])]
        valores = [inst["celdas"].get(k) for k in celdas]
        if not any(k in inst["celdas"] for k in celdas):
            continue
        ev = cm.get(celda_rel) or cm.get(e["celda"])
        pref = clasificar(e, ev)
        item = {"id": f"{pref}-{e['id']}", "clase": {"D": "dato publicado", "C": "cálculo derivado de datos publicados", "V": "convención", "H": "hipótesis"}[pref],
                "fuente": {k: (ev or {}).get(k) for k in ("documento", "pagina", "url", "tipo_fuente")} if ev else None,
                "dato_extraido_y_periodo": {"periodo": (ev or {}).get("periodo"), "unidad": (ev or {}).get("unidad"), "periodo_que_usa_el_calculo": e.get("periodo")},
                "transformacion_o_supuesto": {"ajuste_o_criterio": (ev or {}).get("ajuste"), "clasificacion": (ev or {}).get("clasificacion"),
                                              "observacion": (ev or {}).get("observaciones"), "naturaleza": (ev or {}).get("naturaleza")},
                "entrada_del_modelo": {"celda": e["celda"], "valor": valores[0] if len(valores) == 1 else valores},
                "magnitud": MAGNITUD.get(e["id"], "tasa o parámetro" if e["tipo"] == "hipótesis" else "dato"),
                "calculo": {"motores": e.get("motores"), "condicion": e.get("cond")}}
        entradas.append(item)
        # comprobaciones
        num = [v for v in valores if isinstance(v, (int, float)) and not isinstance(v, bool)]
        if e["id"] in NO_NEGATIVAS and any(v < 0 for v in num):
            avisos.append(f"AVISO signo · {item['id']} ({e['celda']}): valores negativos en una magnitud que no puede serlo: {[v for v in num if v < 0]}")
        pend = pendientes.get(celda_rel) or pendientes.get(e["celda"])
        if any(v == 0 for v in num) and (pend or "pendiente de verificación" in str((ev or {}).get("observaciones") or "").lower() or (ev or {}).get("clasificacion") == "Dato no verificable"):
            item["ceros"] = "cero pendiente de verificación: dato ausente revisado en S-19 (no es «desconocido = cero»)" + (f" · {pend.get('que')}" if pend else "")
            avisos.append(f"AVISO cero pendiente · {item['id']} ({e['celda']}): {item['ceros']}")
        if e["tipo"] == "dato" and any(v is None for v in valores) and e["id"] not in ("ratio_adr",):
            vacias = [k for k, v in zip(celdas, valores) if v is None]
            item["vacias"] = vacias
            if len(vacias) == len(celdas):
                avisos.append(f"AVISO vacío · {item['id']} ({e['celda']}): sin valor (desconocido; no se convierte en cero)")
        u = str((ev or {}).get("unidad") or "")
        if unidad and u and u not in ("—", "%") and e["tipo"] == "dato" and str(unidad).lower() not in u.lower() and MAGNITUD.get(e["id"], "").startswith(("flujo", "stock")):
            avisos.append(f"AVISO unidad · {item['id']}: unidad declarada «{u}» y unidad del libro «{unidad}»")
    # configuración V6.4
    if conf.get("modo") == "Experimental":
        tz = conf.get("trazabilidad") or {}
        base = str(inst["celdas"].get("Historia!L5") or "")
        for k in CE.activos(conf):
            if k == "modo":
                continue
            t = tz.get(k) or {}
            pref = CLASE_ID.get(t.get("clase"), "H")
            refs = [r for r in CE.TRAZA_CELDAS[k] if r not in CE.CELDAS_METADATOS]
            vals = {r: inst["celdas"].get(f"{CE.HOJA}!{r}") for r in refs}
            item = {"id": f"{pref}-config-{k}", "clase": t.get("clase") or "hipótesis", "fuente": {"fuente_o_condicion": t.get("fuente_o_condicion")},
                    "dato_extraido_y_periodo": {"periodo": (conf.get("N1") or {}).get("periodo") if k.startswith("N1") else None,
                                                "perimetro": ((conf.get("N1") or {}).get("perimetro") if k.startswith("N1") else (conf.get("N2") or {}).get("perimetro") if k.startswith("N2") else None)},
                    "transformacion_o_supuesto": {"justificacion": t.get("justificacion"), "confianza": t.get("confianza"), "materialidad_declarada": t.get("materialidad")},
                    "entrada_del_modelo": {"celdas": {f"{CE.HOJA}!{r}": v for r, v in vals.items()}},
                    "magnitud": "; ".join(sorted({MAG_CONFIG.get(r, "parámetro") for r in refs})), "calculo": {"motores": "B", "condicion": "modo experimental"}}
            entradas.append(item)
            ceros = [r for r, v in vals.items() if v == 0]
            if ceros and k in ("N3.circulante",):
                avisos.append(f"AVISO cero · {item['id']}: {ceros} = 0 en el circulante comercial; un dato desconocido no se escribe como cero (fuente: {(conf.get('N3') or {}).get('fuente')})")
            if k == "N3.circulante" and base and base not in str((conf.get("N3") or {}).get("fuente") or ""):
                avisos.append(f"AVISO stock/flujo · {item['id']}: existencias, deudores y acreedores son stocks; se dividen por las ventas (flujo) del ejercicio base {base}, y la fuente no nombra ese ejercicio")
            if k == "PM1.cartera" and (conf.get("PM1") or {}).get("cartera") == CE.CARTERA[1] and any(v == 0 for v in (conf.get("PM1") or {}).get("cartera_historica") or []):
                item["ceros"] = "ceros explícitos de la cartera histórica; su motivo está en cartera_fuente: " + str((conf.get("PM1") or {}).get("cartera_fuente"))[:300]
    # fechas separadas
    dv = _cargar(c, "datos_v63.json") or {}
    an, pa = dv.get("analisis") or {}, dv.get("palancas") or {}
    fechas = {"ejecucion": meta.get("fecha_analisis") or an.get("D4"), "base_ultimo_ejercicio": inst["celdas"].get("Historia!L5"),
              "precio": ((meta.get("precio") or {}) if isinstance(meta.get("precio"), dict) else {}).get("fecha") or pa.get("C45"),
              "acciones": ((meta.get("acciones_diluidas") or {}) if isinstance(meta.get("acciones_diluidas"), dict) else {}).get("fecha") or pa.get("C46"),
              "revision_de_fuentes": ((dv.get("control_maestro") or {}).get("cabecera") or {}).get("L5_revision")}
    for k, v in fechas.items():
        if not v and k != "revision_de_fuentes":
            avisos.append(f"AVISO fecha · falta la fecha «{k}»")
    if not unidad:
        avisos.append("AVISO unidad · Control maestro J4 (unidad de todos los importes) vacío")
    # (4.12, revisión interna R4) precio, capitalización y acciones: las fechas que nombran el período o la transformación tienen que ser
    # la declarada (la del precio o la de las acciones), y el resultado que escribe la transformación («… = N») tiene que ser el valor
    # que entra en el modelo (en la misma escala o en miles o millones). Un texto de evidencia heredado que no se actualizó avisa.
    for item in entradas:
        idx = item["id"].split("-", 1)[-1]
        if idx not in ("precio", "capitalizacion", "acciones"):
            continue
        ref = fechas.get("acciones" if idx == "acciones" else "precio")
        per = (item.get("dato_extraido_y_periodo") or {}).get("periodo")
        aj = (item.get("transformacion_o_supuesto") or {}).get("ajuste_o_criterio")
        otras = sorted(f for f in _fechas_en(f"{per or ''} {aj or ''}") if ref and f != str(ref)[:10])
        if otras:
            avisos.append(f"AVISO fecha incoherente · {item['id']}: el período o la transformación nombran {', '.join(otras)} y la fecha declarada es {ref}")
        v = (item.get("entrada_del_modelo") or {}).get("valor")
        res_t = _resultados_en(str(aj or ""))
        if isinstance(v, (int, float)) and res_t and not any(_coincide(x, v) for x in res_t):
            avisos.append(f"AVISO valor incoherente · {item['id']}: la transformación escribe = {', '.join(f'{x:g}' for x in res_t)} y el valor que entra en el modelo es {v:g}")
    dec = fc.get("decision") or {}
    out = {"empresa": inst["celdas"].get("Análisis!B3") or os.path.basename(os.path.abspath(c)), "unidad": unidad, "fechas": fechas,
           "huella_entradas_economicas": inst["huella"], "n_celdas_economicas": inst["n"],
           "clases_de_identificador": {"D": "dato publicado", "C": "cálculo derivado de datos publicados", "V": "convención", "H": "hipótesis (juicio)"},
           "entradas": entradas,
           "resultado": EE.vector_escenarios(res, precio) | {"motor": res.get("motor")},
           "conclusion": {"estado_propuesto": fc.get("estado_analisis"), "accion": dec.get("accion"), "precio_objetivo": dec.get("precio_objetivo"),
                          "objetivo": ((fc.get("configuracion_v64") or {}).get("objetivo") or {}).get("tratamiento")},
           "avisos": avisos,
           "nota": "cadena fuente → dato → transformación o supuesto → entrada → cálculo → resultado → conclusión, tal como la declaran el libro y la configuración; "
                   "no la valida: los avisos señalan lo que hay que mirar, sin recortar entradas ni adoptar umbrales"}
    return out


def escribir(c, out):
    json.dump(out, open(os.path.join(c, "cadena_trazabilidad.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    md = [f"# Cadena de trazabilidad · {out['empresa']}", "",
          "fuente → dato extraído → transformación o supuesto → entrada del modelo → cálculo → resultado → conclusión (encargo 4.12 §5). "
          "Identificadores por clase: D- dato publicado · C- cálculo derivado · V- convención · H- hipótesis.", "",
          f"Unidad: {out['unidad']} · fechas: " + " · ".join(f"{k} {v}" for k, v in out["fechas"].items()) + f" · huella de las entradas económicas `{out['huella_entradas_economicas'][:16]}…` ({out['n_celdas_economicas']} celdas)", "",
          "| Id | Magnitud | Fuente | Período / unidad | Transformación o supuesto | Entrada del modelo | Cálculo |", "|---|---|---|---|---|---|---|"]
    corta = lambda x, n=90: (str(x) if len(str(x)) <= n else str(x)[:n] + "…") if x not in (None, "") else "—"  # noqa: E731
    for e in out["entradas"]:
        f = e.get("fuente") or {}
        p = e.get("dato_extraido_y_periodo") or {}
        t = e.get("transformacion_o_supuesto") or {}
        en = e.get("entrada_del_modelo") or {}
        md.append(f"| {e['id']} | {e['magnitud']} | {corta(f.get('documento') or f.get('fuente_o_condicion'))} {corta(f.get('pagina'), 40) if f.get('pagina') else ''} | "
                  f"{corta(p.get('periodo'), 40)} / {corta(p.get('unidad'), 20)} | {corta(t.get('ajuste_o_criterio') or t.get('justificacion') or t.get('observacion'))} | "
                  f"{corta(en.get('celda') or ', '.join(en.get('celdas') or {}), 30)} = {corta(en.get('valor') if 'valor' in en else list((en.get('celdas') or {}).values()), 60)} | "
                  f"motores {e['calculo'].get('motores')}; {corta(e['calculo'].get('condicion'), 50)} |".replace("\n", " "))
    r = out["resultado"]
    md += ["", f"**Resultado:** V MALO / NORMAL / BUENO {r.get('V')} · probabilidades {r.get('probabilidades')} · ponderado {r.get('ponderado')} · precio de Sí {r.get('precio_si')} · "
           f"precio {r.get('precio')} · zona {r.get('zona')} · motor {r.get('motor')}.",
           f"**Conclusión (fase C):** {out['conclusion']}.", "", "**Avisos:**"] + [f"- {a}" for a in out["avisos"] or ["ninguno"]]
    open(os.path.join(c, "cadena_trazabilidad.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
    lineas = [f"verificacion_trazabilidad · {out['empresa']} · {len(out['entradas'])} entradas · {len(out['avisos'])} avisos"]
    lineas += [a for a in out["avisos"]] or ["PASS · sin avisos"]
    lineas.append("PASS · cadena escrita (cadena_trazabilidad.json/.md): los avisos no deciden nada; los evalúan la fase C y la auditoría")
    open(os.path.join(c, "verificacion_trazabilidad.txt"), "w", encoding="utf-8").write("\n".join(lineas) + "\n")


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    out = construir(sys.argv[1], sys.argv[2])
    escribir(sys.argv[1], out)
    print(f"OK: cadena_trazabilidad.json/.md · {len(out['entradas'])} entradas · {len(out['avisos'])} avisos")
    return 0


if __name__ == "__main__":
    sys.exit(main())
