#!/usr/bin/env python3
"""Escribe los datos de fase 1 (fase1_v63.json) en un libro V6.3 migrado (pipeline paso 2; encargo §3.4 y §11 pieza 2).

Uso: rellenar_fase1_v63.py <E>_v63_base.xlsx fase1_v63.json <E>_v63_datos.xlsx [--config config_v2.json] [--sobrescribir]

Esquema de fase1_v63.json: esquema/fase1_v63.esquema.md (ejemplo en esquema/fase1_v63.ejemplo.json). Por celda: valor,
fuente, pagina, periodo, unidad. Escribe:
  Historia C5:L26 (el año más reciente en L) + notas M; C57 (años de la media del FCF base)
  Palancas C7 (sector), A28:B33 (geografía), C45 (fecha del precio), C46 (fecha de las acciones), C48 (moneda de cotización)
  Control maestro H4, J4, L4, N4, B5, D5, J5, L5, N5
  Análisis B3, D3, D4, C37 (precio en moneda del modelo), C41 (capitalización), C55 (acciones), C57 (rf) y las celdas de datos que vengan
  Deriva de Historia si vienen vacías: C24 (ROIC medio 5a), C26 (CFO/beneficio medio), C28 (dilución), C33 (deuda neta/EBITDA)
  C51 = «Sí» y C56 = r por defecto si vienen vacías (convención documentada; la fase A las confirma)
  Filas de datos de Control maestro: F = «Rellenado y verificado» + J documento + L página + G periodo + H unidad; sin fuente → «Dato no verificable»
  Reparación H1 (8-nov-2026): una fila de Historia con un cero PENDIENTE de verificación (historia.partidas.<p>.pendientes_verificacion)
  y toda celda de Análisis que dependa de él (C46–C50 con `pendiente_verificacion`; las derivadas C24, C26, C28, C33 si usan un año
  pendiente; la reclasificación IFRS de C48/C49) quedan «Dato no verificable» con la explicación en N, nunca «Rellenado y verificado».
Sin --sobrescribir, una celda de datos ya presente (migrada de la etapa 1) no se pisa, salvo precio, capitalización y acciones (siempre frescos).
Reutilización de un libro ya rellenado (cierre de H1, 8-nov-2026): las filas de Historia se reclasifican siempre con la Historia
actual; las celdas de Análisis que dependen de la Historia (fase1_historia.DEP_ANALISIS) se revisan aunque ya tengan valor: con un
cero pendiente en su ventana pasan a «Dato no verificable» conservando su valor (salvo --sobrescribir); una celda antes pendiente
solo vuelve a «Rellenado y verificado» si su valor coincide con el de la Historia actual. Lo que no puede resolverse con seguridad
(valor distinto del de la Historia actual en una celda que procedía de la Historia o estaba pendiente) se RECHAZA: no se escribe el
libro y hay que regenerar desde el libro base o repetir con --sobrescribir.
Borra las cachés de las fórmulas (recálculo forzado, §1.4). Código 0 ok · 1 verificación fallida · 2 uso · 3 esquema inválido ·
5 reutilización del libro no soportada (regenerar).
"""
import argparse
import datetime as dt
import json
import os
import re
import statistics
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import config_v2  # noqa: E402
import fase1_historia as FH  # noqa: E402  (DEP_ANALISIS, pendientes_celda, defecto_independiente: reparación H1)
from v63_xml import LibroV63  # noqa: E402

FILAS = {"anio": 5, "ventas": 6, "ebit": 7, "da": 8, "beneficio_neto": 9, "tipo_impositivo": 10, "cfo": 11, "capex": 12, "adquisiciones": 13,
         "circulante": 14, "intereses": 15, "intereses_financiacion": 16, "arrendamientos_principal": 17, "sbc": 18, "id": 19,
         "acciones_diluidas": 20, "patrimonio": 21, "deuda": 22, "arrendamientos": 23, "caja": 24, "pensiones": 25, "minoritarios": 26}
COLS = "CDEFGHIJKL"
DATOS_ANALISIS_PERMITIDOS = {"C24", "C26", "C28", "C31", "C32", "C33", "C34", "C38", "C40", "C42", "C46", "C47", "C48", "C49", "C50", "C53", "C54", "C57", "C60", "C88", "C96", "B4"}
F_OK, F_NOVERIF = "Rellenado y verificado", "Dato no verificable"
# (4.13 §6) celdas que se escriben SIEMPRE frescas desde la fase 1: precio, capitalización, acciones y tasa sin riesgo. Su evidencia de
# Control maestro (G:N) se sustituye entera: hasta la 4.12, las columnas que la fase 1 no traía (periodo, literal de M, notas de N,
# enlace de K…) seguían con el texto del libro base, de otra fecha o de otra cifra (Viscofan: «Cierre 6-oct-2026» con el precio del
# 3-nov-2026; «53,60 × 45,6036» con la capitalización 54,70 × 45,479209). El texto anterior queda como antecedente en el registro.
FRESCAS = ("Análisis!C37", "Análisis!C41", "Análisis!C55", "Análisis!C57",
           # (4.13, revisión interna R7) el múltiplo EV/EBITDA depende del precio y de N: si la fase 1 lo trae, sustituye al de la etapa 1
           # con toda su evidencia (si no lo trae, se conserva el heredado, como hasta ahora)
           "Análisis!C42")
COLS_EVIDENCIA = "GHIJKLMN"


def num(x):
    return x if isinstance(x, (int, float)) and not isinstance(x, bool) else None


def filas_cm(libro):
    """{'Análisis!C37': fila} leyendo la columna B de Control maestro en el XML."""
    out = {}
    for r in range(17, 176):
        v = libro.leer("Control maestro", f"B{r}")
        if isinstance(v, str) and "!" in v:
            out[v] = r
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("libro_base")
    ap.add_argument("fase1_json")
    ap.add_argument("salida")
    ap.add_argument("--config", default=None)  # (4.11) None → MUNGER_CONFIG (la del pipeline) o config_v2.json
    ap.add_argument("--sobrescribir", action="store_true")
    ap.add_argument("--sin-verificar", action="store_true")
    a = ap.parse_args()
    cfg = config_v2.cargar(a.config)
    f1 = json.load(open(a.fase1_json, encoding="utf-8"))
    for k in ("empresa", "ticker", "moneda_modelo", "historia", "precio", "acciones_diluidas", "capitalizacion", "sector_damodaran"):
        if k not in f1:
            print(f"ERROR esquema: falta '{k}' en fase1_v63.json")
            return 3
    libro = LibroV63(a.libro_base)
    cm = filas_cm(libro)
    celdas, registro = {}, {"escritas": [], "derivadas": [], "no_pisadas": [], "convenciones": [], "avisos": []}

    tratadas, rechazos = set(), []   # H1: celdas dependientes de la Historia ya revisadas · reutilizaciones no soportadas
    H1_RESUELTO = "H1 resuelto: la Historia actual no tiene ceros pendientes en la ventana de esta celda (antes figuraba como pendiente)."

    def cm_prev(fila):
        return tuple(libro.leer("Control maestro", f"{c}{fila}") for c in "FJN")

    def es_h1(n_):
        return "[H1]" in str(n_ or "")

    def de_historia(j_):
        return str(j_ or "").startswith(("Derivado de Historia", "Historia de fase1_v63.json"))

    def iguales(x, y):
        if num(x) is not None and num(y) is not None:
            return abs(x - y) <= 1e-9 * max(1.0, abs(x), abs(y))
        return x == y

    def marcar_pendiente(fila, clave, pendiente, documento, periodo=None, unidad=None, conservado=None, nuevo=None):
        # H1: depende de un cero sin verificar → «Dato no verificable», con documento y motivo a la vista
        texto = str(pendiente)
        if conservado is not None:
            texto += f" · Valor conservado del libro: {conservado}"
            if nuevo is not None and not iguales(conservado, nuevo):
                texto += f"; con la Historia actual sería {nuevo} (se aplica solo con --sobrescribir o regenerando desde el libro base)"
            texto += "."
        celdas[f"Control maestro!F{fila}"] = F_NOVERIF
        celdas[f"Control maestro!J{fila}"] = str(documento or "fase1_v63.json")
        celdas[f"Control maestro!N{fila}"] = texto
        celdas[f"Control maestro!E{fila}"] = "Listo para auditoría"
        if periodo:
            celdas[f"Control maestro!G{fila}"] = str(periodo)
        if unidad:
            celdas[f"Control maestro!H{fila}"] = str(unidad)
        registro["avisos"].append(f"{clave}: depende de un cero pendiente de verificación → «Dato no verificable»" + (" (valor del libro conservado)" if conservado is not None else ""))
        registro.setdefault("pendientes_verificacion", []).append(clave)

    def etiquetar(fila, clave, derivada, fuente, pagina, periodo, unidad, nota, n_prev=None):
        if derivada:
            celdas[f"Control maestro!F{fila}"] = F_OK
            celdas[f"Control maestro!J{fila}"] = derivada
            celdas[f"Control maestro!I{fila}"] = "cálculo derivado de Historia"
        elif fuente:
            celdas[f"Control maestro!F{fila}"] = F_OK
            celdas[f"Control maestro!J{fila}"] = str(fuente)
            if pagina not in (None, ""):
                celdas[f"Control maestro!L{fila}"] = str(pagina)
        else:
            celdas[f"Control maestro!F{fila}"] = F_NOVERIF
            registro["avisos"].append(f"{clave} sin fuente: «Dato no verificable»")
        if periodo:
            celdas[f"Control maestro!G{fila}"] = str(periodo)
        if unidad:
            celdas[f"Control maestro!H{fila}"] = str(unidad)
        if nota:
            celdas[f"Control maestro!N{fila}"] = str(nota)
        elif es_h1(n_prev):
            celdas[f"Control maestro!N{fila}"] = H1_RESUELTO
        celdas[f"Control maestro!E{fila}"] = "Listo para auditoría"

    def poner(clave, valor, tipo=None, fuente=None, pagina=None, periodo=None, unidad=None, nota=None, forzar=False, derivada=None, pendiente=None, dep=False):
        actual = libro.leer(*clave.split("!", 1))
        fila = cm.get(clave)
        if dep:
            tratadas.add(clave)
        n_prev = cm_prev(fila)[2] if fila else None
        if actual not in (None, "") and not (a.sobrescribir or forzar):
            if dep and fila:
                f_prev, j_prev, n_prev = cm_prev(fila)
                if pendiente:   # el valor del libro se conserva; cambia solo su estado, y la nota lo dice
                    marcar_pendiente(fila, clave, pendiente, derivada or fuente, periodo, unidad, conservado=actual, nuevo=valor)
                    return True
                if es_h1(n_prev):
                    if iguales(actual, valor):   # confirmación posterior: misma cifra, ya sin pendiente
                        etiquetar(fila, clave, derivada, fuente, pagina, periodo, unidad, nota, n_prev)
                        registro.setdefault("evidencias_actualizadas", []).append({"celda": clave, "valor": actual, "de": F_NOVERIF, "a": celdas[f"Control maestro!F{fila}"]})
                        return True
                    rechazos.append(f"{clave}: figuraba pendiente de verificación con el valor {actual}, y la Historia actual da {valor}")
                    return False
                if de_historia(j_prev) and not iguales(actual, valor):
                    rechazos.append(f"{clave}: el valor {actual} procede de otra Historia (Control maestro J: «{str(j_prev)[:80]}»); la actual da {valor}")
                    return False
            registro["no_pisadas"].append({"celda": clave, "actual": actual, "nuevo": valor})
            return False
        celdas[clave] = {"valor": valor, "tipo": tipo} if tipo else valor
        registro["escritas"].append(clave)
        if clave in FRESCAS and fila:
            antes = {c: libro.leer("Control maestro", f"{c}{fila}") for c in COLS_EVIDENCIA}
            if any(v not in (None, "") for v in antes.values()):
                registro.setdefault("evidencias_sustituidas", []).append({"celda": clave, "fila_control_maestro": fila,
                                                                         "antes": {c: v for c, v in antes.items() if v not in (None, "")}})
            for c in COLS_EVIDENCIA:
                celdas[f"Control maestro!{c}{fila}"] = None
        if derivada:
            registro["derivadas"].append({"celda": clave, "valor": valor, "como": derivada})
        if fila and pendiente:
            marcar_pendiente(fila, clave, pendiente, derivada or fuente, periodo, unidad)
            return True
        if fila:
            etiquetar(fila, clave, derivada, fuente, pagina, periodo, unidad, nota, n_prev)
        return True

    # ---- identificación y metadatos ----
    poner("Análisis!B3", f1["empresa"], fuente="fase1_v63.json (identificación)", forzar=True)
    poner("Análisis!D3", f1["ticker"], fuente="fase1_v63.json (identificación)", forzar=True)
    if f1.get("fecha_analisis"):
        # (4.13, revisión interna R7) con su período: la etapa 1 dejaba en G la fecha de su propia preparación (p. ej. «7-oct-2026»)
        poner("Análisis!D4", str(f1["fecha_analisis"])[:10], fuente="fase1_v63.json (fecha de análisis)", periodo=str(f1["fecha_analisis"])[:10], forzar=True)  # D4 tiene formato general en la plantilla: texto ISO, como en los ejemplos
    if f1.get("sector_texto"):
        poner("Análisis!B4", f1["sector_texto"])
    celdas["Control maestro!H4"] = f1["moneda_modelo"]
    celdas["Control maestro!J4"] = f1.get("unidad", "mm")
    if f1.get("norma_contable"):
        celdas["Control maestro!L4"] = f1["norma_contable"]
    if f1.get("cierre_fiscal"):
        celdas["Control maestro!N4"] = f1["cierre_fiscal"]
    if f1.get("mercado"):
        celdas["Control maestro!B5"] = f1["mercado"]
    ratio = f1.get("ratio_adr")
    celdas["Control maestro!D5"] = num(ratio) if num(ratio) is not None else None
    if ratio not in (None, "") and num(ratio) is None:
        registro["avisos"].append(f"ratio_adr {ratio!r} no numérico: D5 se deja vacía")
    celdas["Control maestro!L5"] = dt.date.today().isoformat()
    celdas["Control maestro!N5"] = "fase 1 v2 (rellenar_fase1_v63.py)"
    # ---- Historia ----
    h = f1["historia"]
    anios = h.get("anios") or []
    if not 1 <= len(anios) <= 10:
        print("ERROR esquema: historia.anios tiene que tener entre 1 y 10 años")
        return 3
    desplaz = 10 - len(anios)
    for i, y in enumerate(anios):
        celdas[f"Historia!{COLS[desplaz + i]}5"] = int(y)
    partidas = h.get("partidas", {})
    for nombre, fila in FILAS.items():
        if nombre == "anio" or nombre not in partidas:
            continue
        p = partidas[nombre]
        vals = p.get("valores") if isinstance(p, dict) else p
        if vals is None:
            continue
        if len(vals) != len(anios):
            print(f"ERROR esquema: historia.partidas.{nombre}.valores tiene {len(vals)} valores y hay {len(anios)} años")
            return 3
        for i, v in enumerate(vals):
            celdas[f"Historia!{COLS[desplaz + i]}{fila}"] = num(v) if v is not None else None
        if isinstance(p, dict):
            nota = " · ".join(str(x) for x in (p.get("fuente"), p.get("pagina") and f"p. {p['pagina']}", p.get("nota")) if x)
            if nota:
                celdas[f"Historia!M{fila}"] = nota
    if f1.get("anios_fcf_base"):
        celdas["Historia!C57"] = int(f1["anios_fcf_base"])
    # ---- precio, acciones, capitalización, rf ----
    pr = f1["precio"]
    poner("Análisis!C37", num(pr["valor"]), fuente=pr.get("fuente"), pagina=pr.get("pagina"), forzar=True,
          periodo=pr.get("periodo") or (f"cierre del {pr['fecha']}" if pr.get("fecha") else None),  # (4.13 §6) periodo de la propia fase 1
          unidad=pr.get("unidad") or (f"{pr.get('moneda_cotizacion') or f1['moneda_modelo']}/acción"),
          nota=(f"fecha {pr.get('fecha')} · moneda de cotización {pr.get('moneda_cotizacion')}" + (f" · convertido a {f1['moneda_modelo']} con fx {pr.get('fx')} de {pr.get('fx_fecha')}" if pr.get("fx") else "")
                + (f" · {pr['nota']}" if pr.get("nota") else "")))
    if pr.get("literal"):
        celdas[f"Control maestro!M{cm['Análisis!C37']}"] = str(pr["literal"]) if cm.get("Análisis!C37") else None
    if pr.get("fecha"):
        celdas["Palancas!C45"] = {"valor": pr["fecha"], "tipo": "fecha"}
    celdas["Palancas!C48"] = pr.get("moneda_cotizacion") or f1["moneda_modelo"]
    if pr.get("moneda_cotizacion") and pr["moneda_cotizacion"] != f1["moneda_modelo"] and not pr.get("fx"):
        registro["avisos"].append("la moneda de cotización difiere de la del modelo y no hay fx: la hoja no leerá el precio (Motor!B253)")
    if pr.get("fx"):
        celdas["Control maestro!J5"] = f"{pr['moneda_cotizacion']}→{f1['moneda_modelo']} {pr['fx']} ({pr.get('fx_fecha')})"
    ac = f1["acciones_diluidas"]
    poner("Análisis!C55", num(ac["valor"]), fuente=ac.get("fuente"), pagina=ac.get("pagina"), periodo=ac.get("periodo") or ac.get("fecha"), unidad=ac.get("unidad") or f1.get("unidad", "mm"),
          nota=ac.get("nota"), forzar=True)
    if ac.get("literal") and cm.get("Análisis!C55"):
        celdas[f"Control maestro!M{cm['Análisis!C55']}"] = str(ac["literal"])
    if ac.get("fecha"):
        celdas["Palancas!C46"] = {"valor": ac["fecha"], "tipo": "fecha"}
    cap = f1["capitalizacion"]
    poner("Análisis!C41", num(cap["valor"]), fuente=cap.get("fuente"), pagina=cap.get("pagina"), periodo=cap.get("periodo") or cap.get("fecha"), unidad=cap.get("unidad") or f1.get("unidad", "mm"),
          nota=cap.get("nota"), forzar=True)
    if cap.get("literal") and cm.get("Análisis!C41"):
        celdas[f"Control maestro!M{cm['Análisis!C41']}"] = str(cap["literal"])
    if f1.get("tasa_sin_riesgo") is not None:
        t = f1["tasa_sin_riesgo"]
        poner("Análisis!C57", num(t["valor"]) if isinstance(t, dict) else num(t), fuente=(t.get("fuente") if isinstance(t, dict) else None), forzar=True)
    # ---- sector y geografía ----
    celdas["Palancas!C7"] = f1["sector_damodaran"]
    for i in range(6):
        celdas[f"Palancas!A{28 + i}"] = None
        celdas[f"Palancas!B{28 + i}"] = None
    for i, g in enumerate((f1.get("geografia") or [])[:6]):
        celdas[f"Palancas!A{28 + i}"] = g["pais"]
        celdas[f"Palancas!B{28 + i}"] = num(g["pct"])
    # ---- celdas de datos de Análisis que vengan ----
    def nota_pend(que, anios_p):
        return (f"[H1] Depende de un cero PENDIENTE DE VERIFICACIÓN ({que}; {', '.join(map(str, anios_p))}): la cita del informe no se ha"
                " contrastado con la partida. El valor se conserva; solo una decisión humana registrada en fase1_decisiones.json lo confirma.")

    n_fcf = int(f1.get("anios_fcf_base") or 3)

    def pend_celda(ref, entrada=None):
        """Años pendientes (H1) de una celda de Análisis que depende de la Historia, venga de donde venga su valor. Solo un respaldo
        independiente explícito y válido en la entrada de fase1_v63.json (`independiente`) la libra; declararlo no basta."""
        if ref not in FH.DEP_ANALISIS:
            return []
        if isinstance(entrada, dict) and entrada.get("independiente") is not None and FH.defecto_independiente(entrada["independiente"]) is None:
            return []
        pv = set(FH.pendientes_celda(ref, partidas, anios, n_fcf))
        if isinstance(entrada, dict):
            pv |= set(entrada.get("pendiente_verificacion") or [])
        return sorted(pv)

    for ref, d in (f1.get("analisis") or {}).items():
        if ref not in DATOS_ANALISIS_PERMITIDOS:
            registro["avisos"].append(f"Análisis!{ref} no es una celda de datos admitida: ignorada")
            continue
        v = d.get("valor") if isinstance(d, dict) else d
        pv = pend_celda(ref, d)
        poner(f"Análisis!{ref}", v, fuente=(d.get("fuente") if isinstance(d, dict) else None), pagina=(d.get("pagina") if isinstance(d, dict) else None),
              periodo=(d.get("periodo") if isinstance(d, dict) else None), unidad=(d.get("unidad") if isinstance(d, dict) else None),
              nota=(d.get("nota") if isinstance(d, dict) else None), forzar=f"Análisis!{ref}" in FRESCAS,  # (4.13, R7)
              pendiente=(nota_pend(f"Análisis!{ref} depende de la Historia", pv) if pv else None), dep=ref in FH.DEP_ANALISIS)
    # (4.13, revisión interna R7) textos de la lista de comprobación del Control maestro (C86:E102) que la etapa 1 dejó con fechas o
    # cifras que ya no son las de las entradas: la fase 1 puede sustituirlos de forma explícita; el anterior queda en el registro
    for ref, texto in (f1.get("control_maestro_textos") or {}).items():
        m_ref = re.match(r"^([CDE])(\d+)$", str(ref))
        # (4.14, S5 de la segunda revisión interna 4.13) también F5, «Periodo usado en medias DCF» de la cabecera, que la migración de la etapa 1
        # trae como texto («Pendiente de inversor: …») aunque el período ya esté fijado: es un texto declarativo, no una entrada del motor
        if not (str(ref) == "F5" or (m_ref and 86 <= int(m_ref.group(2)) <= 102)) or not isinstance(texto, str):
            registro["avisos"].append(f"control_maestro_textos: {ref!r} no es una celda de la lista de comprobación (C86:E102) ni la cabecera del período (F5): ignorada")
            continue
        registro.setdefault("evidencias_sustituidas", []).append({"celda": f"Control maestro!{ref}", "antes": {"texto": libro.leer("Control maestro", ref)}})
        celdas[f"Control maestro!{ref}"] = texto
    # ---- derivadas de Historia si vienen vacías ----
    def serie(nombre):
        p = partidas.get(nombre)
        vals = (p.get("valores") if isinstance(p, dict) else p) or []
        return [num(v) for v in vals]
    ventas, ebit, da, ben, tipo, cfo, patr, deuda, arr, caja = (serie(k) for k in ("ventas", "ebit", "da", "beneficio_neto", "tipo_impositivo", "cfo", "patrimonio", "deuda", "arrendamientos", "caja"))
    n = len(anios)

    def vacia(ref):
        """Se (re)calcula si está vacía, con --sobrescribir o si su valor actual procede de la Historia o estaba pendiente (H1)."""
        if libro.leer("Análisis", ref) in (None, "") or a.sobrescribir:
            return True
        fila = cm.get(f"Análisis!{ref}")
        if fila:
            _, j_, n_ = cm_prev(fila)
            return de_historia(j_) or es_h1(n_)
        return False
    if vacia("C24") and "C24" not in (f1.get("analisis") or {}):
        roics = []
        for i in range(n):
            r_i = None
            if ebit[i] is not None and patr[i] is not None and deuda[i] is not None:
                ci = patr[i] + deuda[i] + (arr[i] or 0) - (caja[i] or 0)
                if ci > 0:
                    r_i = ebit[i] * (1 - (tipo[i] or 0)) / ci
            roics.append(r_i)
        ult = [x for x in roics[-5:] if x is not None]
        if len(ult) == 5:
            pv = pend_celda("C24")
            poner("Análisis!C24", round(statistics.mean(ult), 4), derivada="Derivado de Historia filas 7, 10, 21–24 (ROIC medio de los 5 últimos ejercicios, misma fórmula que Historia!C33/C55)",
                  pendiente=(nota_pend("ROIC medio 5 años", pv) if pv else None), dep=True)
    if vacia("C26") and "C26" not in (f1.get("analisis") or {}):
        k = int(f1.get("anios_fcf_base") or 3)
        pares = [(cfo[i], ben[i]) for i in range(n - k, n) if i >= 0 and cfo[i] is not None and ben[i] not in (None, 0)]
        if len(pares) == k and all(b > 0 for _, b in pares):
            pv = pend_celda("C26")
            poner("Análisis!C26", round(statistics.mean(c / b for c, b in pares), 3), derivada=f"Derivado de Historia filas 11 y 9 (CFO ÷ beneficio neto, media de los {k} últimos ejercicios)",
                  pendiente=(nota_pend("CFO ÷ beneficio", pv) if pv else None), dep=True)
    if vacia("C28") and "C28" not in (f1.get("analisis") or {}):
        acc = serie("acciones_diluidas")
        for k in (5, 3):
            if n > k and acc[-1] is not None and acc[-1 - k] not in (None, 0) and acc[-1 - k] > 0:
                cagr = (acc[-1] / acc[-1 - k]) ** (1 / k) - 1
                cat = "Recompra" if cagr <= -0.005 else ("Emite" if cagr >= 0.005 else "Estable")
                pv = pend_celda("C28")
                poner("Análisis!C28", cat, derivada=f"Derivado de Historia fila 20 (CAGR {k} años de acciones diluidas = {cagr:.2%}; convención: ≤ −0,5 % Recompra, ≥ +0,5 % Emite)",
                      pendiente=(nota_pend("acciones diluidas", pv) if pv else None), dep=True)
                break
    if vacia("C33") and "C33" not in (f1.get("analisis") or {}):
        if deuda[-1] is not None and ebit[-1] is not None and da[-1] is not None and caja[-1] is not None:
            ebitda = ebit[-1] + da[-1]
            if ebitda > 0:
                pv = pend_celda("C33")
                poner("Análisis!C33", round((deuda[-1] + (arr[-1] or 0) - caja[-1]) / ebitda, 2), derivada="Derivado de Historia filas 22–24 y 7–8 ((deuda + arrendamientos − caja) ÷ EBITDA del último año)",
                      pendiente=(nota_pend("deuda neta ÷ EBITDA", pv) if pv else None), dep=True)
    # ---- convenciones previas a la fase A ----
    if libro.leer("Análisis", "C51") in (None, ""):
        celdas["Análisis!C51"] = "Sí"
        if cm.get("Análisis!C51"):
            r_ = cm["Análisis!C51"]
            celdas[f"Control maestro!E{r_}"], celdas[f"Control maestro!F{r_}"] = "Listo para auditoría", "Estimación declarada"
            celdas[f"Control maestro!N{r_}"] = "[Clase: convención] [Confianza: media] Hereda: vacía en la etapa 1. Rellenada por convención antes de la fase A (rellenar_fase1_v63.py): restar la SBC siempre (v1). La fase A la confirma."
        registro["convenciones"].append("C51 = Sí")
    if num(libro.leer("Análisis", "C56")) is None:
        r_def = cfg.get("convenciones", {}).get("r_por_defecto", 0.09)
        celdas["Análisis!C56"] = r_def
        if cm.get("Análisis!C56"):
            r_ = cm["Análisis!C56"]
            celdas[f"Control maestro!E{r_}"], celdas[f"Control maestro!F{r_}"] = "Listo para auditoría", "Estimación declarada"
            celdas[f"Control maestro!N{r_}"] = f"[Clase: convención] [Confianza: media] Hereda: vacía en la etapa 1. r = {r_def} por defecto de config_v2.json (S-3), escrita antes de la fase A. Munger no la cambia; informa si r < r mínima."
        registro["convenciones"].append(f"C56 = {r_def}")
    # ---- clasificación de las filas de DATOS de Control maestro (control de evidencias, encargo §7.1) ----
    nombre_por_fila = {v: k for k, v in FILAS.items()}
    metadatos = {"Palancas!C48": "moneda de cotización", "'Control maestro'!H4": "moneda del modelo", "'Control maestro'!J4": "unidad", "'Control maestro'!L4": "norma contable",
                 "'Control maestro'!D5": "ratio ADR", "'Control maestro'!N4": "cierre fiscal", "Palancas!C45": "fecha del precio", "Palancas!C46": "fecha de las acciones", "Palancas!C7": "sector de Damodaran"}
    for r in range(17, 176):
        b = libro.leer("Control maestro", f"B{r}")
        if not isinstance(b, str) or "!" not in b:
            continue
        nat = str(libro.leer("Control maestro", f"D{r}") or "")
        f_actual = celdas.get(f"Control maestro!F{r}", libro.leer("Control maestro", f"F{r}"))
        j_actual = celdas.get(f"Control maestro!J{r}", libro.leer("Control maestro", f"J{r}"))
        es_fila_historia = b.startswith("Historia!C") and ":L" in b
        if f_actual not in (None, "") and not es_fila_historia:   # H1: las filas de Historia se reclasifican siempre
            continue
        if es_fila_historia:
            n_hist_prev = libro.leer("Control maestro", f"N{r}")
            fila_h = int(b.split("!C")[1].split(":")[0])
            nombre = nombre_por_fila.get(fila_h)
            pp = partidas.get(nombre) if nombre else None
            tiene_datos = any(celdas.get(f"Historia!{COLS[desplaz + i]}{fila_h}") is not None for i in range(len(anios))) or fila_h == 5
            if not tiene_datos:
                celdas[f"Control maestro!F{r}"] = "No aplicable"
                celdas[f"Control maestro!N{r}"] = "Sin datos en Historia para esta partida (vacío = desconocido): el motor que la exija lo dirá."
                celdas[f"Control maestro!J{r}"] = None
                continue
            fuente = (pp.get("fuente") if isinstance(pp, dict) else None) or (h.get("fuente_general") or "fase1_v63.json (años de la Historia; fuente en cada partida)" if fila_h == 5 else None)
            pv = (pp.get("pendientes_verificacion") or []) if isinstance(pp, dict) else []
            if pv:
                # H1: la fila contiene un cero sin verificar → nunca «Rellenado y verificado»
                celdas[f"Control maestro!F{r}"] = F_NOVERIF
                celdas[f"Control maestro!J{r}"] = str(fuente or "fase1_v63.json")[:2000]
                celdas[f"Control maestro!N{r}"] = nota_pend(f"Historia, {nombre}", pv)
                registro["avisos"].append(f"{b}: cero pendiente de verificación en {pv} → «Dato no verificable»")
                registro.setdefault("pendientes_verificacion", []).append(b)
            elif fuente:
                celdas[f"Control maestro!F{r}"] = F_OK
                celdas[f"Control maestro!J{r}"] = str(fuente)
                if isinstance(pp, dict) and pp.get("pagina") not in (None, ""):
                    celdas[f"Control maestro!L{r}"] = str(pp["pagina"])
                if es_h1(n_hist_prev):
                    conf = [str(x["anio"]) for x in (f1.get("ceros_confirmados") or []) if x.get("partida") in (nombre, {"circulante": "circulante_lineas"}.get(nombre))]
                    celdas[f"Control maestro!N{r}"] = H1_RESUELTO + (f" Ceros confirmados por decisión humana (fase1_decisiones.json): {', '.join(conf)}." if conf else "")
                    registro.setdefault("evidencias_actualizadas", []).append({"celda": b, "de": F_NOVERIF, "a": F_OK})
            else:
                celdas[f"Control maestro!F{r}"] = F_NOVERIF
                registro["avisos"].append(f"{b} sin fuente en fase1_v63.json: «Dato no verificable»")
                if es_h1(n_hist_prev):
                    celdas[f"Control maestro!N{r}"] = "Sin fuente en fase1_v63.json (H1 resuelto: ya no hay ceros pendientes en esta fila)."
            celdas[f"Control maestro!E{r}"] = "Listo para auditoría"
            celdas[f"Control maestro!G{r}"] = f"{anios[0]}–{anios[-1]}"
            celdas[f"Control maestro!H{r}"] = f1.get("unidad", "mm") + " " + f1["moneda_modelo"]
        elif b == "Historia!C57":
            celdas[f"Control maestro!E{r}"], celdas[f"Control maestro!F{r}"] = "Listo para auditoría", "Estimación declarada"
            celdas[f"Control maestro!N{r}"] = f"[Clase: convención] [Confianza: alta] Años de la media del FCF base = {f1.get('anios_fcf_base', 3)}: los mismos años que C46–C50 (fase1_v63.json / etapa 1). La fase A puede corregirlo."
        elif b in metadatos:
            celdas[f"Control maestro!E{r}"], celdas[f"Control maestro!F{r}"] = "Listo para auditoría", F_OK
            celdas[f"Control maestro!J{r}"] = "fase1_v63.json (metadatos)"
        elif nat.startswith("Dato objetivo"):
            hoja_ref = b.replace("'", "")
            if j_actual not in (None, "") or celdas.get(f"Control maestro!L{r}") or libro.leer("Control maestro", f"L{r}") not in (None, "") or libro.leer("Control maestro", f"M{r}") not in (None, ""):
                celdas[f"Control maestro!F{r}"] = F_OK
                if j_actual in (None, ""):
                    celdas[f"Control maestro!J{r}"] = "evidencia de la etapa 1 (Control maestro L/M)"
            else:
                hoja, ref = hoja_ref.split("!")
                if ":" in ref:  # rangos (p. ej. Palancas!A28:B28, reparto geográfico): se mira la primera celda
                    ref = ref.split(":")[0]
                valor = libro.leer(hoja, ref) if hoja in libro.partes else None
                if valor in (None, "") and celdas.get(f"{hoja}!{ref}") in (None, ""):
                    continue  # celda vacía: la comprobación de entrada dirá si bloquea
                # reparto geográfico con documento en fase1_v63.json (geografia[i].fuente/pagina, o geografia_fuente común)
                geo = f1.get("geografia") or []
                if hoja == "Palancas" and ref[:1] == "A" and ref[1:].isdigit() and 0 <= int(ref[1:]) - 28 < len(geo):
                    gi = geo[int(ref[1:]) - 28]
                    gf = gi.get("fuente") or (f1.get("geografia_fuente") or {}).get("fuente")
                    gp = gi.get("pagina") or (f1.get("geografia_fuente") or {}).get("pagina")
                    if gf:
                        celdas[f"Control maestro!F{r}"] = F_OK
                        celdas[f"Control maestro!J{r}"] = str(gf)
                        if gp not in (None, ""):
                            celdas[f"Control maestro!L{r}"] = str(gp)
                        if gi.get("nota"):
                            celdas[f"Control maestro!N{r}"] = str(gi["nota"])
                        celdas[f"Control maestro!E{r}"] = "Listo para auditoría"
                        continue
                celdas[f"Control maestro!F{r}"] = F_NOVERIF
                registro["avisos"].append(f"{b} con valor pero sin documento (ni en la etapa 1 ni en fase1_v63.json): «Dato no verificable»")
            celdas[f"Control maestro!E{r}"] = "Listo para auditoría"
    # ---- «No aplicable» heredado en C48/C49 con norma IFRS (visto con Vidrala, 3-nov-2026) ----
    # En IFRS las dos celdas aplican siempre: si la etapa 1 las dejó como «No aplicable» con un valor numérico, el valor es un
    # dato (0 cuando los intereses van en explotación) y su evidencia está en la Historia de fase1_v63.json.
    ifrs_tratadas = set()
    if str(f1.get("norma_contable", "")).upper().startswith("IFRS"):
        for ref, partida in (("Análisis!C48", "intereses_financiacion"), ("Análisis!C49", "arrendamientos_principal")):
            fila = cm.get(ref)
            if not fila:
                continue
            f_act = celdas.get(f"Control maestro!F{fila}", libro.leer("Control maestro", f"F{fila}"))
            # H1: una celda que una pasada anterior dejó pendiente desde «No aplicable» se trata como «No aplicable»
            if f"Control maestro!F{fila}" not in celdas and f_act == F_NOVERIF and es_h1(libro.leer("Control maestro", f"N{fila}")):
                f_act = "No aplicable"
            if f_act == "No aplicable":
                ifrs_tratadas.add(ref)
            v = celdas.get(ref, libro.leer(*ref.split("!", 1)))
            v = v.get("valor") if isinstance(v, dict) else v
            hp = (f1.get("historia") or {}).get("partidas", {}).get(partida) or {}
            if f_act == "No aplicable" and num(v) is not None and pend_celda(ref.split("!")[1]):
                # H1: la evidencia de la Historia contiene un cero sin verificar: no se reclasifica como verificado
                celdas[f"Control maestro!F{fila}"] = F_NOVERIF
                celdas[f"Control maestro!E{fila}"] = "Listo para auditoría"
                celdas[f"Control maestro!N{fila}"] = nota_pend(f"Historia, {partida}", pend_celda(ref.split("!")[1]))
                registro["avisos"].append(f"{ref}: «No aplicable» heredado con la Historia de {partida} pendiente de verificación → «Dato no verificable»")
                registro.setdefault("pendientes_verificacion", []).append(ref)
            elif f_act == "No aplicable" and num(v) is not None and hp.get("fuente"):
                celdas[f"Control maestro!F{fila}"] = F_OK
                celdas[f"Control maestro!E{fila}"] = "Listo para auditoría"
                j_prev = libro.leer("Control maestro", f"J{fila}")
                celdas[f"Control maestro!J{fila}"] = (f"{j_prev} · " if j_prev and "fase1_v63.json, Historia" not in str(j_prev) else "") + f"fase1_v63.json, Historia ({partida}): {str(hp['fuente'])[:300]}"
                if es_h1(libro.leer("Control maestro", f"N{fila}")):
                    celdas[f"Control maestro!N{fila}"] = H1_RESUELTO
                registro["convenciones"].append(f"{ref}: «No aplicable» heredado reclasificado como dato verificado (IFRS: la celda aplica; valor {v} documentado en la Historia)")
    # ---- H1: celdas dependientes de la Historia que nadie ha tratado en esta pasada (valor de la etapa 1 u otra fuente) ----
    for ref in FH.DEP_ANALISIS:
        clave = f"Análisis!{ref}"
        fila = cm.get(clave)
        if clave in tratadas or clave in ifrs_tratadas or not fila or f"Control maestro!F{fila}" in celdas:
            continue
        actual = libro.leer("Análisis", ref)
        if actual in (None, ""):
            continue
        f_prev, j_prev, n_prev = cm_prev(fila)
        pv = pend_celda(ref)
        if pv:
            marcar_pendiente(fila, clave, nota_pend(f"{clave} depende de la Historia", pv), j_prev or "valor previo del libro", conservado=actual)
        elif es_h1(n_prev):
            rechazos.append(f"{clave}: figuraba pendiente de verificación y la Historia actual ya no lo está, pero su valor ({actual}) no procede de esta pasada: su evidencia anterior no puede restaurarse")
    # ---- H1: reutilización no soportada → no se escribe nada ----
    if rechazos:
        registro["rechazos_reutilizacion"] = rechazos
        json.dump(registro, open(a.salida + ".fase1.registro.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
        print("RECHAZADO (código 5): reutilización del libro no soportada; no se ha escrito el libro de salida. Hay que regenerar desde el"
              " libro base (<E>_v63_base.xlsx) o repetir con --sobrescribir.")
        for x in rechazos:
            print(f"- {x}")
        return 5
    # ---- escribir ----
    sys.path.insert(0, cfg["plantilla"]["scripts_v63"])
    import inventario_entradas  # noqa
    permitidas = inventario_entradas.conjunto_entradas()
    libro.escribir_celdas(celdas, permitidas)
    libro.borrar_caches()
    libro.guardar(a.salida)
    registro["n_celdas"] = len(celdas)
    json.dump(registro, open(a.salida + ".fase1.registro.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    print(f"OK: {len(celdas)} celdas escritas en {a.salida} · derivadas: {len(registro['derivadas'])} · convenciones: {registro['convenciones']} · avisos: {len(registro['avisos'])}")
    if not a.sin_verificar:
        r = subprocess.run([sys.executable, cfg["plantilla"]["verificador"], a.salida, cfg["plantilla"]["referencia"]], capture_output=True, text=True)
        print((r.stdout.strip().splitlines() or [r.stderr])[-1])
        return 0 if r.returncode == 0 else 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
