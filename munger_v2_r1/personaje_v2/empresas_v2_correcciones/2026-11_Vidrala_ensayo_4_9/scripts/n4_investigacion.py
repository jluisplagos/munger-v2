#!/usr/bin/env python3
"""Investigación N4 de los ceros pendientes de Vidrala (entrega 4.9, encargo §4). Solo lectura de la referencia.

Uso: python3 -I n4_investigacion.py [--salida DIR] [--propuestas DIR]   (desde cualquier carpeta; tarda unos segundos)

Referencia: personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_6_1/Vidrala/ (no se modifica).
Para cada cero pendiente de fase1_v63.json → pendientes_verificacion reconstruye la cadena
    celda del Excel → dato del JSON (fase1_v63.json, AR_<año>.json) → extracción (texto/CF_<año>.txt) → página del PDF
y comprueba concepto y columna, unidad y moneda, signo, período y comparativa, perímetro y dependencias. Contrasta la cita con la
partida (no basta con que la cita exista) mediante CUADRES COMPLETOS del bloque del estado financiero que contendría el dato:
  - minoritarios: patrimonio atribuido a la dominante + total pasivo = total patrimonio neto y pasivo (las dos columnas) y
    resultado del ejercicio = resultado atribuido a la dominante;
  - intereses_financiacion: bloque de financiación (suma de líneas = total impreso) sin ninguna línea de intereses, y la línea de
    intereses pagados dentro de explotación;
  - adquisiciones: bloque de inversión (suma = total) sin importe en la línea de adquisiciones del año;
  - arrendamientos_principal: bloque de financiación sin línea de arrendamientos; norma aplicable (NIC 17 / NIIF 16);
  - arrendamientos (pasivo): pasivos no corrientes y corrientes (sumas = subtotales) sin pasivo por arrendamientos; norma aplicable;
  - otros_activos_financieros: activo corriente (suma = subtotal) sin inversiones financieras corrientes.
En 2024 y 2025 repite los cuadres de minoritarios e intereses en la versión ESPAÑOLA (que prevalece) y en el ESEF 2025 oficial.
Clasificación (encargo §4.2): 1 cero publicado explícitamente · 2 cero derivado mediante una conciliación completa · 3 dato no
publicado o evidencia insuficiente · 4 concepto no aplicable o exención (no se convierte automáticamente en cero numérico) · 5 valor
discrepante que requiere una propuesta de corrección.
La IA no confirma ceros: la clasificación documental no es una confirmación humana ni cambia el estado del pipeline. Las
propuestas se escriben sin firmar (decision, fecha y confirmado_por vacíos) en propuestas/propuestas_n4_sin_firmar.json.
"""
import argparse
import csv
import glob
import hashlib
import itertools
import json
import os
import re
import subprocess
import tempfile
import zipfile

import openpyxl

AQUI = os.path.dirname(os.path.abspath(__file__))
EXPEDIENTE_49 = os.path.dirname(AQUI)
RAIZ = os.path.abspath(os.path.join(EXPEDIENTE_49, "..", "..", ".."))
CORR = os.path.join(RAIZ, "personaje_v2", "empresas_v2_correcciones")
EXP = os.path.join(CORR, "2026-11_Vidrala_ensayo_4_6_1", "Vidrala")
LIBRO = os.path.join(EXP, "Vidrala_v63_evaluada.xlsx")
CEROS_CSV = os.path.join(CORR, "ceros_heredados_H1.csv")
PDF_ES = {2025: os.path.join(RAIZ, "contrastes", "piloto_Vidrala_2025", "fuentes", "es_2308_descarga_2026-11-08", "2308_es-informacion_financiera_consolidada_2025.pdf"),
          2024: os.path.join(RAIZ, "contrastes", "vidrala_2023_arrendamientos", "fuentes", "es_2118_descarga_2026-11-08", "2118_es-informacion_financiera_consolidada_2024.pdf")}
ESEF = os.path.join(RAIZ, "contrastes", "vidrala_revision_financiera", "fuentes", "esef_2025_completo", "2311_en-2025_esef_consolidated_information.zip")
PDF_EN = {**{y: p for y, p in ((int(re.search(r"en-(\d{4})_", os.path.basename(p)).group(1)), p) for p in glob.glob(os.path.join(CORR, "2026-11_Vidrala_ensayo", "fuentes", "cuentas_consolidadas_2016_2022", "*.pdf")))},
          2023: os.path.join(RAIZ, "contrastes", "vidrala_2023_arrendamientos", "fuentes", "en_1831_descarga_2026-11-08", "1831_en-2023_consolidated_financial_information.pdf"),
          2024: os.path.join(RAIZ, "contrastes", "vidrala_2023_arrendamientos", "fuentes", "en_2145_descarga_2026-11-08", "2145_en-2024_consolidated_financial_information.pdf"),
          2025: os.path.join(RAIZ, "contrastes", "piloto_Vidrala_2025", "fuentes", "en_2355_descarga_2026-11-08", "2355_en-2025_consolidated_financial_information.pdf")}
FILA = {"adquisiciones": 13, "intereses_financiacion": 16, "arrendamientos_principal": 17, "arrendamientos": 23, "minoritarios": 26, "otros_activos_financieros": None}
ROTULO = {"adquisiciones": "Adquisiciones netas (positivo)", "intereses_financiacion": "Intereses pagados en financiación (IFRS)",
          "arrendamientos_principal": "Principal de arrendamientos (IFRS 16)", "arrendamientos": "Pasivo por arrendamientos",
          "minoritarios": "Minoritarios (intereses no dominantes)", "otros_activos_financieros": "Otros activos financieros corrientes (partida auxiliar de la caja)"}
TOL = 1.0  # miles de euros: las cifras impresas son enteras


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def col(anio):
    return "CDEFGHIJKL"[anio - 2016]


# ---------- lectura de textos ----------
def paginas_txt(anio):
    t = open(os.path.join(EXP, "texto", f"CF_{anio}.txt"), encoding="utf-8").read()
    p = re.split(r"\[PDF PAGE (\d+)\]", t)
    return {int(p[i]): p[i + 1] for i in range(1, len(p), 2)}


_PDF = {}


def paginas_pdf(ruta):
    if ruta not in _PDF:
        with tempfile.TemporaryDirectory() as d:
            out = os.path.join(d, "t.txt")
            subprocess.run(["pdftotext", "-layout", ruta, out], check=True, capture_output=True)
            _PDF[ruta] = {i: x for i, x in enumerate(open(out, encoding="utf-8").read().split("\f"), 1)}
    return _PDF[ruta]


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


TOKEN = re.compile(r"\(\s*\d[\d.,]*\s*\)|(?<![\w.,&])\d[\d.,]*(?![\w&])|(?<!\S)-(?!\S)")


def valor(tok):
    """Importe impreso → float (miles); '-' → 0.0; None si no se puede leer con seguridad (p. ej. «112,5000»)."""
    t = tok.strip()
    if t == "-":
        return 0.0
    neg = t.startswith("(")
    t = t.strip("()").strip()
    if re.fullmatch(r"\d{1,3}([.,]\d{3})+", t):
        v = float(re.sub(r"[.,]", "", t))
    elif re.fullmatch(r"\d+", t):
        v = float(t)
    else:
        return None
    return -v if neg else v


def importes(linea):
    return [valor(m.group(0)) for m in TOKEN.finditer(linea)]


def bloque(texto, inicio, total):
    """Líneas no vacías desde la que casa `inicio` hasta la que casa `total` (incluida)."""
    ls = [l.rstrip() for l in texto.splitlines() if l.strip()]
    i = next((k for k, l in enumerate(ls) if re.search(inicio, l)), None)
    if i is None:
        return None
    for k in range(i + 1, len(ls)):
        if re.search(total, ls[k]):
            return ls[i:k + 1]
    return None


def cuadre(lineas, total_re):
    """Cuadre completo de un bloque: suma de las líneas (actual y anterior) = total impreso. Resuelve las líneas con un solo importe
    probando las dos columnas (solo se acepta si una única asignación cuadra las dos). Devuelve un dict con el detalle."""
    lt = lineas[-1]
    tot = [x for x in importes(lt) if x is not None][-2:]
    cuerpo = lineas[1:-1]
    if len(tot) < 2:
        # el total impreso en una línea suelta justo antes del rótulo (maquetación del texto)
        k = max(i for i, l in enumerate(cuerpo) if len(importes(l)) >= 2 and not re.search(r"[A-Za-zÁÉÍÓÚáéíóúñ]", l)) if any(len(importes(l)) >= 2 and not re.search(r"[A-Za-zÁÉÍÓÚáéíóúñ]", l) for l in cuerpo) else None
        if k is None:
            return {"ok": False, "motivo": "total no localizado"}
        tot = importes(cuerpo[k])[-2:]
        cuerpo = cuerpo[:k] + cuerpo[k + 1:]
    pares, sueltas, ilegibles = [], [], []
    for l in cuerpo:
        xs = importes(l)
        if len(xs) >= 2:
            for x, colum in ((xs[-2], "actual"), (xs[-1], "anterior")):
                if x is None:
                    ilegibles.append({"linea": norm(l), "columna": colum})
        elif len(xs) == 1 and xs[0] is None:
            ilegibles.append({"linea": norm(l), "columna": "desconocida"})
        if len(xs) >= 2:
            pares.append((xs[-2], xs[-1], norm(l)))
        elif len(xs) == 1:
            sueltas.append((xs[0], norm(l)))
    sol = []
    for asign in itertools.product((0, 1), repeat=len(sueltas)):
        a = sum(p[0] or 0 for p in pares) + sum(s[0] for s, c in zip(sueltas, asign) if c == 0)
        b = sum(p[1] or 0 for p in pares) + sum(s[0] for s, c in zip(sueltas, asign) if c == 1)
        sol.append((abs(a - tot[0]) <= TOL, abs(b - tot[1]) <= TOL, asign, a, b))
    buenas = [s for s in sol if s[0] and s[1]]
    actual_ok = any(s[0] for s in sol)
    unica = len(buenas) == 1 or (not sueltas and buenas)
    asign = buenas[0][2] if buenas else ()
    return {"ok": bool(buenas) and unica, "actual_cuadra": actual_ok, "anterior_cuadra": any(s[1] for s in sol), "total": tot,
            "n_lineas": len(pares) + len(sueltas), "lineas_un_importe": [{"linea": c, "importe": v, "columna": ("actual" if a == 0 else "anterior")} for (v, c), a in zip(sueltas, asign)],
            "ilegibles": ilegibles, "lineas": [norm(l) for l in lineas]}


def fm(v):
    """Importes en miles con punto de millar: (1412878.0, 1309830.0) → «1.412.878 / 1.309.830»."""
    if v is None:
        return "—"
    if isinstance(v, (list, tuple)):
        return " / ".join(fm(x) for x in v)
    return f"{v:,.0f}".replace(",", ".") if isinstance(v, (int, float)) else str(v)


def cuadre_actual(cu):
    """El cuadre de la columna del propio año basta para el cero de ese año si la otra columna solo falla por una errata ilegible
    del texto (p. ej. «112,5000» en el comparativo 2022 del informe 2023), que se declara. Un importe ilegible en la columna del año (o
    en una línea de columna desconocida) nunca se tolera (auditoría interna de la 4.9, Z-4)."""
    il = cu.get("ilegibles") or []
    if il:
        return bool(cu.get("actual_cuadra") and not cu.get("lineas_un_importe") and all(i["columna"] == "anterior" for i in il))
    return bool(cu.get("ok"))


def ilegibles_txt(cu):
    return "; ".join(f"{i['linea']} (columna {i['columna']})" for i in cu.get("ilegibles") or [])


# Listas blancas de rótulos (auditoría interna de la 4.9, Z-4): clasificación por EXCLUSIÓN. Toda línea del bloque cuyo rótulo no está en
# la lista es una excepción (la entrada no puede quedar respaldada), aunque el bloque cuadre: un concepto con otro nombre (intereses
# rotulados «Finance costs paid», una adquisición rotulada «Business combinations», un depósito rotulado «Short-term investments»)
# no puede pasar por cero. Las listas contienen solo los rótulos que aparecen en los estados de Vidrala 2016–2025 (inglés y español).
BLANCA = {
    "financiacion": r"(proceeds from (loans and borrowings|other debts|issue of treasury shares and own equity instruments)|payments (of loans and borrowings|from other debts|to redeem own shares and other own equity instruments)|dividends paid"
                    r"|cobros procedentes de (las deudas con entidades de cr[eé]dito|otras deudas|la emisi[oó]n de acciones propias e instrumentos de patrimonio propio)|pagos procedentes (de las deudas con entidades de cr[eé]dito|de otras deudas|del rescate de acciones propias( y otros instrumentos de patrimonio propio)?)"
                    r"|dividendos pagados|subvenciones, donaciones y legados recibidos)",
    "inversion": r"(acquisition of (a subsidiary, net of the cash acquired|financial assets|intangible assets|property, plant and equipment)|(payments|proceeds) from sale of (property, plant and equipment|other intangible assets))",
    "activo_corriente": r"(inventories|trade and other receivables|current tax assets|derivative financial instruments|other current assets|cash and cash equivalents|existencias|deudores comerciales y otras cuentas a cobrar"
                        r"|activos por impuestos sobre las ganancias corrientes|instrumentos financieros derivados|otros activos corrientes|efectivo y otros medios l[ií]quidos equivalentes)",
    "pasivos_2016": r"(ingresos diferidos|pasivos financieros con entidades de cr[eé]dito|instrumentos financieros derivados|pasivos por impuestos diferidos|provisiones|otros pasivos no corrientes"
                    r"|acreedores comerciales y otras cuentas a pagar|pasivos por impuestos sobre las ganancias corrientes|otros pasivos corrientes)",
}
COLA = re.compile(r"(\s+(\(\s*\d[\d.,]*\s*\)?|\d[\d.,]*\)?|-|\d+(&|y)\d+))+\s*$")


def rotulos_no_reconocidos(lineas, clave):
    """Rótulos del cuerpo del bloque (sin la primera ni la última línea) que no están en la lista blanca. Una línea sin importes se
    une a la siguiente (rótulo partido); una línea solo con importes es maquetación."""
    out, pend = [], ""
    for l in (lineas or [])[1:-1]:
        t = norm(l)
        if not re.search(r"[A-Za-zÁÉÍÓÚáéíóúñ]", t):
            continue
        tiene_importe = bool(COLA.search(t)) and bool(importes(t))
        rot = norm(pend + " " + COLA.sub("", t)) if tiene_importe else ""
        if not tiene_importe:
            pend = norm(pend + " " + t)
            continue
        pend = ""
        if not re.fullmatch(BLANCA[clave], rot, flags=re.I):
            out.append(rot)
    if pend:
        out.append(pend)
    return out


def buscar_par(texto, rotulo):
    m = re.search(rotulo + r"\D*?(?P<a>\(?\d[\d.,]*\)?|-)\s+(?P<b>\(?\d[\d.,]*\)?|-)", norm(texto))
    return (valor(m.group("a")), valor(m.group("b"))) if m else None


def cita_en_pagina(texto, cita):
    return norm(cita) in norm(texto)


UNIDAD = re.compile(r"(?i)thousands of euros|miles de euros")
OTRA_UNIDAD = re.compile(r"(?i)millions of euros|millones de euros")
DESGLOSE = re.compile(r"(?i)\bof which\b|\bde los cuales\b|\bde las cuales\b")
NCI_PAGINA = re.compile(r"(?i)non-controlling|participaciones no dominantes|socios externos|minorit|outside (shareholders|interests)")


def unidad_cabecera(t, ini):
    """(Control de vigencia de la 4.9, V-4) La unidad se busca en la cabecera del estado (el texto anterior al bloque), no en toda la
    página: una mención suelta en una nota al pie no acredita la unidad; una cabecera en millones la contradice."""
    ls = t.splitlines()
    k = next((i for i, l in enumerate(ls) if re.search(ini, l)), None)
    cab = "\n".join(ls[:k] if k is not None else ls)
    return bool(UNIDAD.search(cab)) and not OTRA_UNIDAD.search(cab)


def excepciones_estructura(t, lineas, ini):
    """(Control de vigencia de la 4.9, V-4) Lo que la clasificación por exclusión no examina línea a línea y convierte en excepción:
    más de un bloque con el mismo inicio en la página (p. ej., actividades interrumpidas), un desglose «of which / de los cuales» en
    la página y, dentro del cuerpo del bloque, líneas solo con importes (sin rótulo) que no son el total impreso aparte."""
    out = []
    if ini and sum(1 for l in t.splitlines() if re.search(ini, l)) > 1:
        out.append("la página tiene más de un bloque que empieza igual")
    if DESGLOSE.search(t):
        out.append("la página tiene un desglose «of which / de los cuales»")
    if lineas:
        solo = [norm(l) for l in lineas[1:-1] if importes(l) and not re.search(r"[A-Za-zÁÉÍÓÚáéíóúñ]", l)]
        total_suelto = len([x for x in importes(lineas[-1]) if x is not None]) < 2
        if len(solo) > (1 if total_suelto else 0):
            out.append("líneas solo con importes, sin rótulo, dentro del bloque: " + "; ".join(solo))
    return out


# ---------- ESEF 2025 (versión española oficial) ----------
def esef_hechos():
    with zipfile.ZipFile(ESEF) as z:
        nombre = next(n for n in z.namelist() if n.endswith(".xhtml"))
        x = z.read(nombre).decode("utf-8")
    ctx = {i: b for i, b in re.findall(r'<xbrli:context id="([^"]+)">(.*?)</xbrli:context>', x, flags=re.S)}
    out = {}
    for a, v in re.findall(r"<ix:nonFraction([^>]*)>(.*?)</ix:nonFraction>", x, flags=re.S):
        n = re.search(r'name="([^"]+)"', a).group(1)
        b = ctx.get(re.search(r'contextRef="([^"]+)"', a).group(1), "")
        if "explicitMember" in b:
            continue
        f = (re.findall(r"<xbrli:(?:instant|endDate)>([^<]+)<", b) or ["?"])[-1][:4]
        t = re.sub(r"<[^>]+>", "", v).strip()
        val = 0.0 if t in ("-", "") else float(t.replace(".", "").replace(",", "."))
        out[(n, f)] = -val if re.search(r'sign="-"', a) else val
    return out


# ---------- comprobaciones por partida ----------
def ch_minoritarios(anio, P, pg, es=None):
    t = P.get(pg, "")
    eq = buscar_par(t, r"(?:Equity attributed to equity holders of the Parent|Patrimonio atribuido a tenedores de instrumentos de)")
    tl = buscar_par(t, r"(?:Total liabilities|Total pasivo)(?! y)")
    tel = buscar_par(t, r"(?:Total equity and liabilities|Total patrimonio neto y pasivo)")
    pyg = next((P[n] for n in sorted(P) if n > pg and re.search(r"(?i)(profit for the year from continuing|beneficio del ejercicio de\s+actividades continuadas|beneficio del ejercicio de actividades)", P[n])), "")
    pt = buscar_par(pyg, r"(?:Profit for the year|Beneficio del ejercicio)(?! (from|de|attrib|atrib|por))")
    pa = buscar_par(pyg, r"(?:Profit for the year attributable to equity holders of the Parent|Beneficio del ejercicio atribuible a tenedores de)")
    bal = bool(eq and tl and tel) and all(abs(eq[i] + tl[i] - tel[i]) <= TOL for i in (0, 1)) and not NCI_PAGINA.search(t)
    res = bool(pt and pa) and all(abs(pt[i] - pa[i]) <= TOL for i in (0, 1))
    menciones = []
    for n, x in P.items():
        for m in re.finditer(r"(?i)non-controlling|minority (interest|stake)|participaciones no dominantes|minoritari|socios externos", x):
            menciones.append({"pagina": n, "contexto": norm(x[max(0, m.start() - 160):m.end() + 120])})
    return {"cuadre_balance": bal, "cuadre_resultado": res, "patrimonio_atribuido": eq, "total_pasivo": tl, "total_pn_y_pasivo": tel,
            "resultado_ejercicio": pt, "resultado_atribuido": pa, "unidad": unidad_cabecera(t, r"(?i)equity attributed to equity holders|patrimonio atribuido a tenedores"),
            "excepciones_estructura": excepciones_estructura(t, None, None),
            "menciones_nci_en_notas": menciones[:12], "n_menciones_nci": len(menciones)}


INI_FIN = r"(?i)^\s*(cash flows from financing activities|flujos? de efectivo de actividades de financiaci)"
TOT_FIN = r"(?i)(net cash (from|used in|from/\(used in\)).*financing activities|efectivo neto (generado|utilizado).*financiaci)"
INI_INV = r"(?i)^\s*(cash flows from investing activities|flujos? de efectivo de actividades de inversi)"
TOT_INV = r"(?i)(net cash (used in|from|from/\(used in\)).*investing activities|efectivo neto (generado|utilizado).*inversi)"
INI_EXP = r"(?i)^\s*(cash flows from operating activities|flujos? de efectivo de actividades de explotaci)"
TOT_EXP = r"(?i)(net cash (from|used in|generated).*operating activities|efectivo neto (generado|utilizado).*explotaci)"
INTERES = re.compile(r"(?i)\binterest|\bintereses")
ARREND = re.compile(r"(?i)\blease|arrendamiento")


def ch_financiacion(anio, P, pg):
    t = P.get(pg, "")
    b = bloque(t, INI_FIN, TOT_FIN)
    e = bloque(t, INI_EXP, TOT_EXP)
    cu = cuadre(b, TOT_FIN) if b else {"ok": False, "motivo": "bloque de financiación no localizado"}
    lin_int_fin = [norm(l) for l in (b or []) if INTERES.search(l)]
    lin_arr_fin = [norm(l) for l in (b or []) if ARREND.search(l)]
    pagados = [(norm(l), importes(l)[-2:]) for l in (e or []) if re.search(r"(?i)interest paid|pagos de intereses", l)]
    return {"cuadre_financiacion": cu, "lineas_intereses_en_financiacion": lin_int_fin, "lineas_arrendamientos_en_financiacion": lin_arr_fin,
            "intereses_pagados_en_explotacion": pagados, "rotulos_no_reconocidos": rotulos_no_reconocidos(b, "financiacion"), "unidad": unidad_cabecera(t, INI_EXP),
            "excepciones_estructura": excepciones_estructura(t, b, INI_FIN)}


def ch_inversion(anio, P, pg):
    t = P.get(pg, "")
    b = bloque(t, INI_INV, TOT_INV)
    cu = cuadre(b, TOT_INV) if b else {"ok": False, "motivo": "bloque de inversión no localizado"}
    adq = [l for l in (cu.get("lineas_un_importe") or []) if re.search(r"(?i)acquisition of a subsidiar|adquisici[oó]n de (una )?sociedad", l["linea"])]
    adq_pares = [norm(l) for l in (b or []) if re.search(r"(?i)acquisition of a subsidiar|adquisici[oó]n de (una )?sociedad", l) and len(importes(l)) >= 2]
    return {"cuadre_inversion": cu, "linea_adquisiciones_un_importe": adq, "linea_adquisiciones_dos_importes": adq_pares,
            "rotulos_no_reconocidos": rotulos_no_reconocidos(b, "inversion"), "unidad": unidad_cabecera(t, INI_EXP),
            "excepciones_estructura": excepciones_estructura(t, b, INI_INV)}


def ch_activo_corriente(anio, P, pg):
    t = P.get(pg, "")
    b = bloque(t, r"(?i)^\s*(current assets|activos corrientes)", r"(?i)^\s*\(?\d[\d.,]*\)?\s+\(?\d[\d.,]*\)?\s*$")
    if b:
        b = b[:-1] + [b[-1]]
    cu = cuadre(b, "") if b else {"ok": False, "motivo": "activo corriente no localizado"}
    inversiones = [norm(l) for l in (b or []) if re.search(r"(?i)(financial investments|deposits|inversiones financieras|dep[oó]sitos|other (current )?financial assets|otros activos financieros)", l)]
    return {"cuadre_activo_corriente": cu, "lineas_inversiones_financieras_corrientes": inversiones,
            "rotulos_no_reconocidos": rotulos_no_reconocidos(b, "activo_corriente"), "unidad": unidad_cabecera(t, r"(?i)^\s*(non-current assets|activos no corrientes|current assets|activos corrientes)"),
            "excepciones_estructura": excepciones_estructura(t, b, r"(?i)^\s*(current assets|activos corrientes)")}


def ch_pasivos_2016(P, pg):
    t = P.get(pg, "")
    nc = bloque(t, r"(?i)^\s*pasivos no corrientes", r"^\s*\(?\d[\d.,]*\)?\s+\(?\d[\d.,]*\)?\s*$")
    co = bloque(t, r"(?i)^\s*pasivos corrientes", r"^\s*\(?\d[\d.,]*\)?\s+\(?\d[\d.,]*\)?\s*$")
    cnc, cco = (cuadre(nc, "") if nc else {"ok": False}), (cuadre(co, "") if co else {"ok": False})
    arr = [norm(l) for l in (nc or []) + (co or []) if ARREND.search(l)]
    notas = [{"pagina": n, "contexto": norm(x[max(0, m.start() - 120):m.end() + 220])} for n, x in sorted(P.items()) for m in [re.search(r"(?i)arrendamientos operativos|arrendamiento financiero|arrendamientos financieros", x)] if m]
    finan = [x for x in notas if re.search(r"(?i)arrendamientos? financieros?", x["contexto"])]
    return {"cuadre_no_corriente": cnc, "cuadre_corriente": cco, "lineas_arrendamiento_en_pasivo": arr, "notas_arrendamientos": notas[:6], "menciones_arrendamiento_financiero": finan,
            "rotulos_no_reconocidos": rotulos_no_reconocidos(nc, "pasivos_2016") + rotulos_no_reconocidos(co, "pasivos_2016"), "unidad": unidad_cabecera(t, r"(?i)^\s*pasivos no corrientes"),
            "excepciones_estructura": excepciones_estructura(t, nc, r"(?i)^\s*pasivos no corrientes") + excepciones_estructura(t, co, r"(?i)^\s*pasivos corrientes")}


def aplicar_condiciones_generales(e):
    """(Auditoría interna de la 4.9, Z-4) Condiciones generales de toda entrada respaldada (clase 2) o no aplicable (clase 4): la cita está
    en su página, la página declara la unidad, la comparativa del informe siguiente no la contradice y el bloque no tiene rótulos fuera de
    la lista blanca. Si alguna falla, la entrada pasa a la clase 3 con el motivo."""
    cm = e.get("comprobaciones") or {}
    fallos = [x for x, okx in (("la cita no está en su página", e.get("cita_en_su_pagina")), ("no se localiza el rótulo de unidad (miles de euros) en la página", cm.get("unidad")),
                               ("la comparativa del informe siguiente lo contradice", e.get("comparativa_coherente") is not False),
                               ("hay rótulos no reconocidos en el bloque: " + "; ".join(cm.get("rotulos_no_reconocidos") or []), not cm.get("rotulos_no_reconocidos")),
                               ("la estructura de la página no se puede examinar línea a línea: " + "; ".join(cm.get("excepciones_estructura") or []), not cm.get("excepciones_estructura"))) if not okx]
    e["condiciones_generales_no_cumplidas"] = fallos
    if fallos and e.get("clasificacion") in (2, 4):
        e["clasificacion"] = 3
        e["explicacion"] = "NO RESPALDADA: " + "; ".join(fallos) + ". " + e.get("explicacion", "")
        e["valor_propuesto"] = None
    return e


def texto_es_minoritarios(c, ve, anio):
    """(Control de vigencia de la 4.9, V-5) «Igual» solo si las cifras coinciden; si la versión española las reexpresa, se dice."""
    if not ve:
        return ""
    if ve.get("coincide_con_el_texto_ingles"):
        return " Igual en la versión española (prevalece)."
    i = 0 if ve.get("columna") == "del año" else 1
    tp, tt = (ve.get("total_pasivo") or [None, None])[i], (ve.get("total_pn_y_pasivo") or [None, None])[i]
    return (f" La versión española (prevalece; {ve.get('columna')}) también cuadra, pero con cifras reexpresadas: total pasivo {fm(tp)} y total patrimonio neto y pasivo "
            f"{fm(tt)}, frente a {fm(c['total_pasivo'][0])} y {fm(c['total_pn_y_pasivo'][0])} del texto inglés de {anio}; el patrimonio atribuido "
            + ("coincide" if (ve.get("patrimonio_atribuido") or [None, None])[i] == c["patrimonio_atribuido"][0] else "tampoco coincide")
            + ". La reexpresión no cambia el cero: en las dos versiones el balance cuadra sin participaciones no dominantes.")


def menciones_txt(c, contrastes):
    """Explicación de las menciones de intereses no dominantes del año, a partir de sus contextos (auditoría interna de la 4.9, Z-7)."""
    ms = c.get("menciones_nci_en_notas") or []
    if not ms:
        return " La memoria del texto no menciona intereses no dominantes."
    pol = [m for m in ms if re.search(r"(?i)goodwill|fondo de comercio", m["contexto"])]
    adq = [m for m in ms if m not in pol]
    nombres = sorted({n for m in adq for n in ("Vidroporto", "Envasados Eva", "Glassco") if n.lower() in m["contexto"].lower()})
    partes = []
    if pol:
        partes.append(f"{len(pol)} de política contable (definición del fondo de comercio)")
    if adq:
        partes.append(f"{len(adq)} sobre participaciones que el grupo adquiere en otras sociedades" + (f" ({', '.join(nombres)})" if nombres else ""))
    t = ((f" Las {len(ms)} menciones de intereses minoritarios o no dominantes de la memoria son " + " y ".join(partes)) if len(ms) > 1 else
         (" La única mención de intereses minoritarios o no dominantes de la memoria es " + ("de política contable (definición del fondo de comercio)" if pol else "sobre una participación que el grupo adquiere en otra sociedad" + (f" ({', '.join(nombres)})" if nombres else ""))))
    t += "; ninguna es un interés de terceros en el patrimonio de Vidrala (contextos en comprobaciones.menciones_nci_en_notas)." if len(ms) > 1 else "; no es un interés de terceros en el patrimonio de Vidrala (contexto en comprobaciones.menciones_nci_en_notas)."
    sd = contrastes.get("sociedades_dependientes")
    if sd:
        t += (f" La tabla de sociedades dependientes (p. {sd['pagina']}) da el 100 % en todas las consolidadas por integración global; los únicos porcentajes distintos "
              f"({', '.join(x + ' %' for x in sd['porcentajes_distintos_de_100'])}) son de sociedades por puesta en equivalencia.")
    return t


# ---------- investigación ----------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--salida", default=os.path.join(EXPEDIENTE_49, "n4"))
    ap.add_argument("--propuestas", default=os.path.join(EXPEDIENTE_49, "propuestas"))
    a = ap.parse_args()
    os.makedirs(a.salida, exist_ok=True)
    os.makedirs(a.propuestas, exist_ok=True)
    f1 = json.load(open(os.path.join(EXP, "fase1_v63.json"), encoding="utf-8"))
    pend = f1["pendientes_verificacion"]
    csv_v = [r for r in csv.DictReader(open(CEROS_CSV, encoding="utf-8")) if r["empresa"] == "Vidrala"]
    clave_csv = {(int(r["anio"]), r["partida"]) for r in csv_v}
    clave_pend = {(p["anio"], p["partida"]) for p in pend}
    reg = json.load(open(os.path.join(EXP, "Vidrala_v63_datos.xlsx.fase1.registro.json"), encoding="utf-8"))
    meta = json.load(open(os.path.join(EXP, "fase1_metadatos.json"), encoding="utf-8"))
    conv = meta.get("convenciones") or {}
    dec = json.load(open(os.path.join(EXP, "fase1_decisiones.json"), encoding="utf-8"))
    wb = openpyxl.load_workbook(LIBRO, data_only=True)
    H, A = wb["Historia"], wb["Análisis"]
    efe_p = os.path.join(a.salida, "efectos", "efectos_n4.json")
    efe = json.load(open(efe_p, encoding="utf-8")) if os.path.exists(efe_p) else None
    dpor = {v["variante"]: v["delta"] for v in (efe or {}).get("variantes", [])}
    esef = esef_hechos()
    recuento = {
        "pendientes_en_fase1_v63": len(pend), "ceros_heredados_csv_vidrala": len(csv_v),
        "en_csv_y_no_pendientes": sorted([list(k) for k in clave_csv - clave_pend]), "pendientes_no_en_csv": sorted([list(k) for k in clave_pend - clave_csv]),
        "por_partida": {k: sum(1 for p in pend if p["partida"] == k) for k in FILA},
        "con_fila_en_la_historia": sum(1 for p in pend if FILA[p["partida"]]), "auxiliares_sin_fila": sum(1 for p in pend if not FILA[p["partida"]]),
        "celdas_marcadas_dato_no_verificable_en_el_libro": reg.get("pendientes_verificacion"),
        "explicacion": ("El recuento real es 38 (fase1_v63.json → pendientes_verificacion), igual al del encargo. ceros_heredados_H1.csv tiene 39 entradas de Vidrala: "
                        "la 39.ª (adquisiciones, AR_2023.json, columna 2022) no se usa en la Historia porque la sustituye el comparativo del informe siguiente "
                        "(usado_en_historia = «no (lo sustituye el comparativo del informe siguiente)»). De las 38, 28 alimentan cinco filas de la Historia "
                        "(13, 16, 17, 23 y 26) y 10 son la partida auxiliar otros_activos_financieros, sin fila propia: solo contaría en la caja si "
                        f"fase1_metadatos.json lo declarara, y declara caja_incluye_otros_activos_financieros = {conv.get('caja_incluye_otros_activos_financieros')}. "
                        "Análisis!C48 no es un cero propio: es la media 2023–2025 de intereses_financiacion (fase1_historia.DEP_ANALISIS), y hereda su estado.")}
    matriz = []
    for p in sorted(pend, key=lambda x: (list(FILA).index(x["partida"]), x["anio"])):
        anio, part = p["anio"], p["partida"]
        ar = json.load(open(os.path.join(EXP, "fase1_partes", f"AR_{anio}.json"), encoding="utf-8"))
        cero = ar["partidas"][part]["cero"]
        P = paginas_txt(anio)
        pg = cero["pagina"]
        fila = FILA[part]
        celda = f"Historia!{col(anio)}{fila}" if fila else None
        valor_libro = H[f"{col(anio)}{fila}"].value if fila else None
        e = {"id": f"N4-{part}-{anio}", "partida": part, "concepto": ROTULO[part], "anio": anio, "celda": celda, "valor_actual": valor_libro if fila else 0.0,
             "estado_actual": "pendiente de verificación (H1): cita sin contrastar; en el libro «Dato no verificable» [H1]" if fila else "pendiente de verificación (H1); partida auxiliar sin celda propia",
             "fuente": {"json": f"fase1_partes/AR_{anio}.json → partidas.{part}.cero", "texto": f"texto/CF_{anio}.txt", "pagina_pdf": pg,
                        "pdf": os.path.relpath(PDF_EN.get(anio, ""), RAIZ) if PDF_EN.get(anio) else None, "pdf_sha256": sha(PDF_EN[anio]) if PDF_EN.get(anio) else None,
                        "idioma_del_texto": "español" if anio == 2016 else "inglés (traducción libre; «In the event of discrepancy, the Spanish-language version prevails»)"},
             "cita": cero["cita"], "motivo_extraccion": cero["motivo"], "cita_en_su_pagina": cita_en_pagina(P.get(pg, ""), cero["cita"])}
        if part == "minoritarios":
            c = ch_minoritarios(anio, P, pg)
            e["comprobaciones"] = c
            ok = c["cuadre_balance"] and c["cuadre_resultado"]
            contrastes = {}
            anio_es = anio if anio in PDF_ES else (anio + 1 if anio + 1 in PDF_ES else None)
            if anio_es:
                Pe = paginas_pdf(PDF_ES[anio_es])
                pge = next(n for n, x in Pe.items() if re.search(r"Total patrimonio neto y pasivo", x) and re.search(r"Patrimonio atribuido", x))
                ce = ch_minoritarios(anio_es, Pe, pge)
                contrastes["version_espanola"] = {"pdf": os.path.relpath(PDF_ES[anio_es], RAIZ), "pdf_sha256": sha(PDF_ES[anio_es]), "pagina": pge,
                                                  "columna": "del año" if anio_es == anio else f"comparativa {anio} del informe {anio_es} (las dos columnas cuadran)",
                                                  "cuadre_balance": ce["cuadre_balance"], "cuadre_resultado": ce["cuadre_resultado"],
                                                  "patrimonio_atribuido": ce["patrimonio_atribuido"], "total_pasivo": ce["total_pasivo"], "total_pn_y_pasivo": ce["total_pn_y_pasivo"],
                                                  "coincide_con_el_texto_ingles": (ce["patrimonio_atribuido"] == c["patrimonio_atribuido"] and ce["total_pn_y_pasivo"] == c["total_pn_y_pasivo"]) if anio_es == anio
                                                  else (ce["patrimonio_atribuido"][1] == c["patrimonio_atribuido"][0] and ce["total_pn_y_pasivo"][1] == c["total_pn_y_pasivo"][0])}
                ok = ok and ce["cuadre_balance"] and ce["cuadre_resultado"] and not ce["excepciones_estructura"]  # (W-5) también en la versión que prevalece
            if anio in (2024, 2025):
                pl, pla = esef.get(("ifrs-full:ProfitLoss", str(anio))), esef.get(("ifrs-full:ProfitLossAttributableToOwnersOfParent", str(anio)))
                contrastes["esef_2025"] = {"ProfitLoss": pl, "ProfitLossAttributableToOwnersOfParent": pla, "iguales": pl is not None and pl == pla,
                                           "hechos_de_intereses_no_dominantes": sorted({k[0] for k in esef if "oncontrolling" in k[0]}), "zip_sha256": sha(ESEF)}
                ok = ok and contrastes["esef_2025"]["iguales"] and not contrastes["esef_2025"]["hechos_de_intereses_no_dominantes"]
            dep_pag = next((n for n, x in P.items() if re.search(r"(?i)full consolidation method", x) and re.search(r"(?i)equity method", x) and "%" in x), None)
            if dep_pag:
                pct = re.findall(r"(\d{1,3})%", P[dep_pag])
                contrastes["sociedades_dependientes"] = {"pagina": dep_pag, "porcentajes_distintos_de_100": sorted(set(x for x in pct if x != "100")),
                                                         "texto": norm(P[dep_pag][P[dep_pag].find("The aforementioned"):][:260]) if "The aforementioned" in P[dep_pag] else None}
            e["contrastes"] = contrastes
            e["clasificacion"] = 2 if ok else 3
            e["explicacion"] = (f"Sin línea de participaciones no dominantes. Cuadre completo del balance {anio} (las dos columnas): patrimonio atribuido a la dominante "
                                f"{fm(c['patrimonio_atribuido'])} + total pasivo {fm(c['total_pasivo'])} = total patrimonio neto y pasivo {fm(c['total_pn_y_pasivo'])}; y de la cuenta de "
                                f"resultados: resultado del ejercicio {fm(c['resultado_ejercicio'])} = atribuido a la dominante {fm(c['resultado_atribuido'])}. Por tanto los intereses no "
                                "dominantes son 0 por diferencia, no por una cifra impresa." + texto_es_minoritarios(c, contrastes.get("version_espanola"), anio)
                                + (" En el ESEF 2025: ProfitLoss = ProfitLossAttributableToOwnersOfParent; ningún hecho de intereses no dominantes." if anio in (2024, 2025) else "")
                                + menciones_txt(c, contrastes))
            e["valor_propuesto"] = 0.0 if ok else None
        elif part in ("intereses_financiacion", "arrendamientos_principal"):
            c = ch_financiacion(anio, P, pg)
            e["comprobaciones"] = c
            cu = c["cuadre_financiacion"]
            ok = cuadre_actual(cu) and not c["lineas_intereses_en_financiacion"] and (part == "arrendamientos_principal" or bool(c["intereses_pagados_en_explotacion"])) and not c["rotulos_no_reconocidos"]
            if part == "arrendamientos_principal":
                ok = cu.get("ok") and not c["lineas_arrendamientos_en_financiacion"] and not c["rotulos_no_reconocidos"]
            contrastes = {}
            anio_es = anio if anio in PDF_ES else (anio + 1 if anio + 1 in PDF_ES else None)
            if anio_es and part == "intereses_financiacion":
                Pe = paginas_pdf(PDF_ES[anio_es])
                pge = next(n for n, x in Pe.items() if re.search(r"Flujos? de efectivo de actividades de financiaci", x) and re.search(r"Pagos de intereses", x))
                ce = ch_financiacion(anio_es, Pe, pge)
                cfe = ce["cuadre_financiacion"]
                ok_es = (cuadre_actual(cfe) if anio_es == anio else bool(cfe.get("anterior_cuadra"))) and not ce["lineas_intereses_en_financiacion"] and bool(ce["intereses_pagados_en_explotacion"]) and not ce["rotulos_no_reconocidos"] and not ce["excepciones_estructura"]
                contrastes["version_espanola"] = {"pdf": os.path.relpath(PDF_ES[anio_es], RAIZ), "pdf_sha256": sha(PDF_ES[anio_es]), "pagina": pge,
                                                  "columna": "del año" if anio_es == anio else f"comparativa {anio} del informe {anio_es}", "cuadre_financiacion": ok_es,
                                                  "total_financiacion": cfe.get("total"), "lineas_intereses_en_financiacion": ce["lineas_intereses_en_financiacion"],
                                                  "intereses_pagados_en_explotacion": ce["intereses_pagados_en_explotacion"], "rotulos_no_reconocidos": ce["rotulos_no_reconocidos"]}
                ok = ok and ok_es
            if anio in (2024, 2025) and part == "intereses_financiacion":
                contrastes["esef_2025"] = {"InterestPaidClassifiedAsOperatingActivities": esef.get(("ifrs-full:InterestPaidClassifiedAsOperatingActivities", str(anio))),
                                           "InterestPaidClassifiedAsFinancingActivities": esef.get(("ifrs-full:InterestPaidClassifiedAsFinancingActivities", str(anio))),
                                           "CashFlowsFromUsedInFinancingActivities": esef.get(("ifrs-full:CashFlowsFromUsedInFinancingActivities", str(anio))), "zip_sha256": sha(ESEF)}
                ok = ok and contrastes["esef_2025"]["InterestPaidClassifiedAsFinancingActivities"] is None and contrastes["esef_2025"]["InterestPaidClassifiedAsOperatingActivities"] is not None
            e["contrastes"] = contrastes
            pag = c["intereses_pagados_en_explotacion"]
            if part == "intereses_financiacion":
                e["clasificacion"] = 2 if ok else 3
                con_arr = anio >= 2018  # 2018: arrendamiento financiero (NIC 17, nota 15); 2019 en adelante: NIIF 16
                e["componentes"] = {"intereses_de_deudas": {"clasificacion": 2 if ok else 3, "explicacion": "en explotación («Interest paid» / «Pagos de intereses»); el bloque de financiación cuadra sin línea de intereses"},
                                    "intereses_de_arrendamientos": ({"clasificacion": 3, "explicacion": ("no consta en qué línea del estado de flujos están (contraste 4.2, INFORME_2023_Y_ARRENDAMIENTOS.md: «No consta»; "
                                                                                                         "el ESEF etiqueta el total de «Pagos de intereses» sin desglose). Por NIIF 16.50 b) seguirían la política de intereses (explotación), pero es una inferencia normativa, no un dato publicado")}
                                                                    if con_arr else {"clasificacion": "no procede", "explicacion": "sin arrendamientos en balance (2016: solo operativos, a gasto; 2017: ninguno)"})}
                e["reserva"] = ("componente de arrendamientos no acreditado (ligado a P3 y a Análisis!C49): no cambia el cero de los intereses de deudas; ver la hipótesis de C48 en la sección de efectos" if con_arr else None)
                e["explicacion"] = (f"Los intereses pagados de {anio} ({fm(pag[0][1][0]) if pag else '—'} miles) están en explotación, dentro del CFO. El bloque de financiación cuadra de forma completa "
                                    f"({cu.get('n_lineas')} líneas = total {fm(cu.get('total'))}) y no tiene ninguna línea de intereses: la parte en financiación es 0 por diferencia."
                                    + (f" La columna comparativa de este estado tiene una errata del texto ({ilegibles_txt(cu)}): el cuadre que acredita el cero es el de la columna {anio}." if cu.get("ilegibles") else "")
                                    + ((" Igual en la versión española (prevalece)" + ("" if anio in PDF_ES else f", en la columna comparativa {anio} del informe {anio + 1}")) + (" y en el ESEF 2025 (solo InterestPaidClassifiedAsOperatingActivities; ningún hecho de intereses en financiación)." if anio in (2024, 2025) else ".") if contrastes else ""))
                e["valor_propuesto"] = 0.0 if ok else None
            else:
                if anio == 2016:
                    pas = ch_pasivos_2016(P, 5)
                    notas = [x for x in [pas["notas_arrendamientos"]] if x]
                    # (auditoría interna de la 4.9, Z-4) la clase 4 depende de comprobaciones: norma por fecha, bloque cuadrado sin línea de arrendamientos
                    # y notas que solo describen arrendamientos operativos
                    e["clasificacion"] = 4 if (anio < 2019 and ok and pas["notas_arrendamientos"] and not pas["menciones_arrendamiento_financiero"]) else 3
                    e["explicacion"] = ("Ejercicio anterior a la NIIF 16 (en vigor desde 2019): el concepto «principal de arrendamientos NIIF 16» no existe. Los arrendamientos eran operativos (nota 3 f: "
                                        "«Las cuotas derivadas de los arrendamientos operativos … se reconocen como gasto»), así que su pago está dentro del CFO; no hay arrendamientos financieros. "
                                        f"El bloque de financiación cuadra sin línea de arrendamientos ({cu.get('n_lineas')} líneas = {fm(cu.get('total'))}). No es un cero publicado ni derivado: es un "
                                        "concepto no aplicable, cuya representación numérica en la plantilla (0, coherente con un CFO que ya descuenta las cuotas) es una decisión, no un hecho. "
                                        "Decisión registrada en fase1_decisiones.json, sin fecha ni firma en el archivo: arrendamientos_principal 2017 = 0 («antes de NIIF 16»).")
                    e["valor_propuesto"] = "no aplicable (representación numérica 0 a decidir)"
                    e["comprobaciones"]["notas_arrendamientos_2016"] = notas
                else:
                    ar18 = ar["partidas"].get("arrendamientos") or {}
                    fl = [x for x in ar18.get("actual") or [] if re.search(r"(?i)finance lease", x.get("concepto", "")) and x.get("impreso") == "40,916"]
                    regla = re.search(r"(?i)arrendamientos = solo pasivos NIIF 16.*arrendamientos financieros que no son NIIF 16.*van en deuda", dec.get("_regla") or "")
                    deuda18 = ((dec.get("deuda") or {}).get("2018") or {}).get("valor_mm")
                    e["clasificacion"] = 4 if (anio < 2019 and ok and fl and regla and deuda18 is not None and abs(deuda18 - 433.767) < 1e-6 and abs(H["E22"].value - deuda18) < 1e-6) else 3
                    e["condiciones_clase_4"] = {"anterior_a_niif16": anio < 2019, "financiacion_cuadra_sin_arrendamientos": bool(ok), "finance_lease_40916_en_AR_2018": bool(fl),
                                                "regla_registrada": bool(regla), "deuda_2018_registrada_433_767_igual_a_Historia_E22": deuda18 is not None and abs(H["E22"].value - deuda18) < 1e-6}
                    e["explicacion"] = ("Ejercicio anterior a la NIIF 16 (aplicada desde 2019 sin reexpresar): el concepto «principal de arrendamientos NIIF 16» no existe. Existía un arrendamiento "
                                        "financiero de NIC 17: la nota 15 de 2018 (p. 57) muestra un «Finance Lease» de 40.916 no corriente y «-» corriente, nacido en 2018. La regla registrada en "
                                        "fase1_decisiones.json (_regla: «Arrendamientos = solo pasivos NIIF 16. Los arrendamientos financieros que no son NIIF 16 (leasing de maquinaria de dic-2018 …) "
                                        "van en deuda») lo lleva a la deuda (decisión registrada deuda 2018 = 433,767, que incluye los 40.916) y deja arrendamientos 2018 = 0; por coherencia, "
                                        "cualquier pago de su principal corresponde a la deuda, no a la fila 17 (en el estado de flujos solo podría estar en «Payments of loans and borrowings», 121.155, que no lo separa). "
                                        f"El bloque de financiación cuadra sin línea de arrendamientos ({cu.get('n_lineas')} líneas = {fm(cu.get('total'))}). Decisión registrada (sin fecha ni firma): arrendamientos_principal 2017 = 0 "
                                        "(«antes de NIIF 16»). Concepto no aplicable bajo esa regla; su representación numérica (0, como en 2017) es una decisión, no un dato publicado.")
                    e["valor_propuesto"] = "no aplicable (representación numérica 0 a decidir, como la decisión registrada de 2017)"
        elif part == "adquisiciones":
            c = ch_inversion(anio, P, pg)
            e["comprobaciones"] = c
            cu = c["cuadre_inversion"]
            adq_actual = [l for l in c["linea_adquisiciones_un_importe"] if l["columna"] == "actual"] + c["linea_adquisiciones_dos_importes"]
            ok = cu.get("ok") and not adq_actual and not c["rotulos_no_reconocidos"]
            e["clasificacion"] = 2 if ok else 3
            e["explicacion"] = (f"El bloque de inversión de {anio} cuadra de forma completa en las dos columnas ({cu.get('n_lineas')} líneas = total {fm(cu.get('total'))}) sin importe de adquisiciones en {anio}"
                                + (": la única línea de adquisición del estado tiene un importe que solo cuadra en la columna comparativa (" + "; ".join(fm(l['importe']) for l in c['linea_adquisiciones_un_importe']) + ")" if c["linea_adquisiciones_un_importe"] else "; no hay línea de adquisiciones")
                                + ". Cero por diferencia. Aviso de la extracción: en el texto inglés los rótulos de este bloque están desplazados respecto de los importes (p. ej. «Proceeds from sale of property, plant and equipment» con el pago de inmovilizado); el cuadre no depende de los rótulos.")
            e["valor_propuesto"] = 0.0 if ok else None
        elif part == "arrendamientos":
            c = ch_pasivos_2016(P, pg)
            e["comprobaciones"] = c
            e["clasificacion"] = 4 if (anio < 2019 and c["cuadre_no_corriente"].get("ok") and c["cuadre_corriente"].get("ok") and not c["lineas_arrendamiento_en_pasivo"]
                                       and c["notas_arrendamientos"] and not c["menciones_arrendamiento_financiero"] and not c["rotulos_no_reconocidos"]) else 3
            e["explicacion"] = ("Ejercicio anterior a la NIIF 16: el «pasivo por arrendamientos (IFRS 16)» de la plantilla no existe. Los pasivos no corrientes y corrientes del balance 2016 cuadran con sus subtotales "
                                f"({fm(c['cuadre_no_corriente'].get('total'))} y {fm(c['cuadre_corriente'].get('total'))}) sin ninguna línea de arrendamiento, y la nota 3 f solo describe arrendamientos operativos "
                                "(a gasto). No hay arrendamientos financieros que estuvieran dentro de la deuda. Concepto no aplicable; su representación numérica (0) es una decisión, no un dato. "
                                "Decisiones registradas en fase1_decisiones.json, sin fecha ni firma en el archivo: arrendamientos 2017 = 0 y 2018 = 0 («antes de NIIF 16»), con la regla «Arrendamientos = solo pasivos NIIF 16».")
            e["valor_propuesto"] = "no aplicable (representación numérica 0 a decidir)"
        elif part == "otros_activos_financieros":
            c = ch_activo_corriente(anio, P, pg)
            e["comprobaciones"] = c
            cu = c["cuadre_activo_corriente"]
            ok = cu.get("ok") and not c["lineas_inversiones_financieras_corrientes"] and not c["rotulos_no_reconocidos"]
            anio_es = anio if anio in PDF_ES else (anio + 1 if anio + 1 in PDF_ES else None)
            if anio_es:
                # (control de vigencia de la 4.9, V-5) 2023 se contrasta con la columna comparativa del informe español de 2024
                Pe = paginas_pdf(PDF_ES[anio_es])
                pge = next(n for n, x in Pe.items() if re.search(r"(?m)^\s*Activos corrientes", x) and re.search(r"Efectivo y otros medios l", x))
                ce = ch_activo_corriente(anio_es, Pe, pge)
                cue = ce["cuadre_activo_corriente"]
                i = 0 if anio_es == anio else 1
                ok_es = bool(cue.get("ok")) and not ce["lineas_inversiones_financieras_corrientes"] and not ce["rotulos_no_reconocidos"] and not ce["excepciones_estructura"]
                e["contrastes"] = {"version_espanola": {"pdf": os.path.relpath(PDF_ES[anio_es], RAIZ), "pdf_sha256": sha(PDF_ES[anio_es]), "pagina": pge,
                                                        "columna": "del año" if anio_es == anio else f"comparativa {anio} del informe {anio_es}", "cuadre_activo_corriente": ok_es,
                                                        "total": cue.get("total"), "coincide_con_el_texto_ingles": bool(cue.get("total")) and bool(cu.get("total")) and cue["total"][i] == cu["total"][0],
                                                        "rotulos_no_reconocidos": ce["rotulos_no_reconocidos"]}}
                ok = ok and ok_es
            e["clasificacion"] = 2 if ok else 3
            e["explicacion"] = (f"El activo corriente de {anio} cuadra de forma completa ({cu.get('n_lineas')} líneas = subtotal {fm(cu.get('total'))}) y no tiene inversiones financieras corrientes ni depósitos: "
                                "solo existencias, deudores, impuestos, derivados, otros activos corrientes y efectivo. «Otros activos financieros» es una partida NO corriente. Cero por diferencia. "
                                "La partida no entra en el modelo: no tiene fila en la Historia y fase1_metadatos.json declara caja_incluye_otros_activos_financieros = false."
                                + ((" Igual en la versión española (prevalece)" + ("" if anio in PDF_ES else f", en la columna comparativa {anio} del informe {anio + 1}") + "."
                                    if e["contrastes"]["version_espanola"]["coincide_con_el_texto_ingles"] else (f" La versión española (prevalece; {e['contrastes']['version_espanola']['columna']}) también cuadra sin inversiones financieras corrientes, con el total reexpresado "
                                       f"({fm(e['contrastes']['version_espanola']['total'][0 if anio in PDF_ES else 1])} frente a {fm(cu['total'][0])} del texto inglés de {anio})."))
                                   if e.get("contrastes") else ""))
            e["valor_propuesto"] = 0.0 if ok else None
        # período, comparativa, signo, perímetro, unidad
        e["comprobacion_general"] = {
            "unidad_y_moneda": "miles de euros en el estado → mm en la Historia (÷ 1.000); moneda EUR" + ("" if (e.get("comprobaciones") or {}).get("unidad", True) else " · AVISO: rótulo de unidad no localizado en la página"),
            "signo": {"minoritarios": "saldo de patrimonio: 0 sin signo", "intereses_financiacion": "la plantilla resta C48 en positivo: un 0 no tiene signo", "arrendamientos_principal": "positivo en la plantilla; 0 sin signo",
                      "arrendamientos": "saldo; 0 sin signo", "adquisiciones": "positivo = compras netas; 0 sin signo", "otros_activos_financieros": "saldo; 0 sin signo"}[part],
            "periodo_y_comparativa": None, "perimetro": ("2024: Italia como discontinuada en el informe 2024 (columna 2023 reexpresada); no afecta a estas partidas" if anio in (2023, 2024) else "sin cambio de perímetro que afecte a la partida")}
        if anio < 2025 and part in ("minoritarios", "intereses_financiacion", "adquisiciones", "otros_activos_financieros"):
            Ps = paginas_txt(anio + 1)
            ar_sig = json.load(open(os.path.join(EXP, "fase1_partes", f"AR_{anio + 1}.json"), encoding="utf-8"))["partidas"][part]
            pg_s = (ar_sig.get("cero") or {}).get("pagina")
            if pg_s:
                if part == "minoritarios":
                    cs = ch_minoritarios(anio + 1, Ps, pg_s)
                    okc = cs["cuadre_balance"] and cs["cuadre_resultado"]
                elif part == "intereses_financiacion":
                    cs = ch_financiacion(anio + 1, Ps, pg_s)
                    okc = cs["cuadre_financiacion"].get("anterior_cuadra") and not cs["lineas_intereses_en_financiacion"]
                    if not okc and (cs["cuadre_financiacion"].get("ilegibles") or [{}])[0].get("columna") == "anterior" and not cs["lineas_intereses_en_financiacion"]:
                        okc = None  # errata del texto en la columna comparativa: no comprobable, sin contradicción
                elif part == "adquisiciones":
                    cs = ch_inversion(anio + 1, Ps, pg_s)
                    okc = cs["cuadre_inversion"].get("anterior_cuadra") and not [l for l in cs["linea_adquisiciones_un_importe"] if l["columna"] == "anterior"]
                else:
                    cs = ch_activo_corriente(anio + 1, Ps, pg_s)
                    okc = cs["cuadre_activo_corriente"].get("anterior_cuadra") and not cs["lineas_inversiones_financieras_corrientes"]
                e["comprobacion_general"]["periodo_y_comparativa"] = f"columna comparativa {anio} del informe {anio + 1} (p. {pg_s}): " + (
                    "coherente (cuadra igual)" if okc else ("no comprobable por una errata del texto (" + ilegibles_txt(cs["cuadre_financiacion"]) + "), sin línea de intereses: no la contradice" if okc is None else "NO coherente: revisar"))
                e["comparativa_coherente"] = okc if okc is None else bool(okc)
            else:
                e["comprobacion_general"]["periodo_y_comparativa"] = f"el informe {anio + 1} no registra un cero de la partida (la extracción de {anio + 1} tiene cifra o no la tiene)"
        else:
            e["comprobacion_general"]["periodo_y_comparativa"] = "último ejercicio (2025): sin informe siguiente; contraste con la versión española y el ESEF" if anio == 2025 else "partida sin comparativa útil (concepto no aplicable o NIC 17)"
        # dependencias y efecto
        dep = {"minoritarios": ("Historia!C65 (pensiones + minoritarios del último año) → Diagnóstico V6!C16 (puente del motor B = deuda + arrendamientos + pensiones + minoritarios − caja) → valor por acción de los tres escenarios (Análisis!B78:D78), ponderado (C83) y precio de Sí"
                                if anio == 2025 else "solo la regla de tipos de Historia C5:L26 (Motor!E234): ninguna fórmula usa el valor de años anteriores a 2025"),
               "intereses_financiacion": ("Análisis!C48 = media 2023–2025 (valor escrito por la fase 1, fase1_historia.DEP_ANALISIS) → C52 FCF base normalizado → f (Historia!C58/C80, Diagnóstico V6!C12), su control de rango (C50), precio ÷ FCF (Diagnóstico V6!B65/D65) y el disparador de quiebra de referencias_mecanicas.py; NO entra en la valoración del motor B"
                                          if anio >= 2023 else "solo la regla de tipos de Historia C5:L26: ninguna fórmula ni media de Análisis usa ese año"),
               "adquisiciones": "medias de la Historia (reinversión histórica) sin efecto numérico en las salidas medidas; regla de tipos",
               "arrendamientos_principal": "solo la regla de tipos (Análisis!C49 es la media 2023–2025, que no usa 2016 ni 2018)",
               "arrendamientos": "Historia!C64 solo usa el último año; regla de tipos; deuda media de C63 solo usa 2024–2025",
               "otros_activos_financieros": "ninguna: sin fila en la Historia y sin sumarse a la caja (convención declarada false)"}[part]
        e["dependencias"] = dep
        aplicar_condiciones_generales(e)
        dec_part = dec.get(part) if isinstance(dec.get(part), dict) else {}
        # (Z-5) las entradas de fase1_decisiones.json distintas de P1 no tienen fecha ni firma en el archivo: no se presentan como confirmaciones humanas
        e["registro_en_fase1_decisiones"] = {"decision_registrada_para_esta_entrada": str(anio) in dec_part,
                                             "decisiones_registradas_de_la_partida": {k: v for k, v in dec_part.items()},
                                             "con_fecha_y_firma": sorted(k for k, v in dec_part.items() if isinstance(v, dict) and v.get("fecha") and v.get("confirmado_por")),
                                             "regla_registrada": dec.get("_regla") if part in ("arrendamientos", "arrendamientos_principal") else None,
                                             "nota": "Salvo P1 (circulante 2024, con fecha y firma), las entradas de fase1_decisiones.json no tienen fecha ni confirmado_por en el archivo (sesión de construcción del 3-nov-2026; autoría no constatada)."}
        clave_efecto = {"minoritarios": "L26_mas_1" if anio == 2025 else "C26_K26_mas_1", "intereses_financiacion": "C48_mas_1" if anio >= 2023 else "fila16_mas_1",
                        "adquisiciones": "E13_I13_mas_1", "arrendamientos_principal": "C17_E17_mas_1", "arrendamientos": "C23_mas_1", "otros_activos_financieros": None}[part]
        d = dpor.get(clave_efecto) if clave_efecto else None
        e["efecto"] = {"variante_unitaria": clave_efecto, "delta_por_1_mm": d,
                       "efecto_del_valor_documentado": "nulo: el valor documentado coincide con el actual (0)" if e.get("valor_propuesto") == 0.0 else "sin valor documentado alternativo",
                       "material": bool(d and any(abs(v or 0) > 1e-9 for k, v in d.items() if k.startswith(("MALO", "NORMAL", "BUENO", "ponderado"))))}
        if part == "intereses_financiacion" and anio >= 2023:
            e["efecto"]["hipotesis_C48"] = {k: dpor.get(k) for k in ("H_C48_int_arrend", "H_C48_doble_computo")}
        e["carencia_o_decision"] = {
            2: "ninguna carencia documental; queda la confirmación humana (fase1_decisiones.json), que la IA no hace",
            3: "falta la evidencia indicada en la explicación; no hay valor que proponer",
            4: "decisión de la persona responsable: extender a este año la representación como 0 que ya tienen las decisiones registradas de 2017–2018 (sin fecha ni firma en el archivo; conviene confirmarlas si se quiere apoyar en ellas), coherente con la definición de la plantilla y con la regla «Arrendamientos = solo pasivos NIIF 16», o dejarlo vacío (= desconocido)"}[e["clasificacion"]]
        if e.get("reserva"):
            e["carencia_o_decision"] += "; reserva: " + e["reserva"]
        matriz.append(e)
    # resumen de cobertura (no es una confirmación ni un porcentaje de fiabilidad)
    cob = {"investigadas": len(matriz),
           "respaldadas_clase_1_o_2": sum(1 for e in matriz if e["clasificacion"] in (1, 2)),
           "de_ellas_con_reserva": sum(1 for e in matriz if e["clasificacion"] in (1, 2) and e.get("reserva")),
           "no_aplicables_clase_4": sum(1 for e in matriz if e["clasificacion"] == 4),
           "sin_evidencia_suficiente_clase_3": sum(1 for e in matriz if e["clasificacion"] == 3),
           "discrepantes_clase_5": sum(1 for e in matriz if e["clasificacion"] == 5),
           "por_clase": {str(k): sum(1 for e in matriz if e["clasificacion"] == k) for k in (1, 2, 3, 4, 5)},
           "aviso": "Cobertura documental de la IA. No es una confirmación humana (ningún cero cambia de estado en el pipeline) ni un porcentaje de fiabilidad para invertir."}
    salida = {"generado_por": "n4_investigacion.py (entrega 4.9)", "referencia": os.path.relpath(EXP, RAIZ), "libro_sha256": sha(LIBRO), "fase1_v63_sha256": sha(os.path.join(EXP, "fase1_v63.json")),
              "recuento": recuento, "cobertura": cob, "efectos": os.path.relpath(efe_p, RAIZ) if efe else None, "matriz": matriz}
    json.dump(salida, open(os.path.join(a.salida, "matriz_n4.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    with open(os.path.join(a.salida, "matriz_n4.csv"), "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["id", "partida", "anio", "celda", "valor_actual", "estado_actual", "pagina_pdf", "cita", "cita_en_su_pagina", "clasificacion", "reserva", "valor_propuesto",
                    "comparativa", "dependencias", "delta_ponderado_por_1_mm", "material", "explicacion", "carencia_o_decision"])
        for e in matriz:
            d = (e["efecto"].get("delta_por_1_mm") or {})
            w.writerow([e["id"], e["partida"], e["anio"], e["celda"] or "", e["valor_actual"], e["estado_actual"], e["fuente"]["pagina_pdf"], e["cita"], e["cita_en_su_pagina"], e["clasificacion"],
                        e.get("reserva") or "", e.get("valor_propuesto"), e["comprobacion_general"]["periodo_y_comparativa"], e["dependencias"], d.get("ponderado (Análisis!C83)"), e["efecto"]["material"],
                        e["explicacion"], e["carencia_o_decision"]])
    # expediente único de propuestas, agrupado por partida (sin una solicitud por cada celda dependiente), sin firmar
    grupos = []
    for part in FILA:
        es = [e for e in matriz if e["partida"] == part]
        for cl in sorted({e["clasificacion"] for e in es}):
            g = [e for e in es if e["clasificacion"] == cl]
            grupos.append({"grupo": f"{part} · clase {cl}", "partida": part, "anios": [e["anio"] for e in g], "celdas": [e["celda"] for e in g if e["celda"]],
                           "celdas_dependientes_sin_solicitud_propia": (["Análisis!C48 (media 2023–2025)"] if part == "intereses_financiacion" and any(e["anio"] >= 2023 for e in g) else [])
                                                                        + (["Historia!C65 → Diagnóstico V6!C16 (puente)"] if part == "minoritarios" and any(e["anio"] == 2025 for e in g) else []),
                           "clasificacion_documental": cl, "propuesta": {2: "registrar el cero con la fuente documental del cuadre (valor 0, sin cambio numérico)",
                                                                         3: "no confirmar: mantener pendiente hasta disponer de la evidencia que falta",
                                                                         4: "decidir la representación del concepto no aplicable (0 o vacío); no es una confirmación de un cero publicado"}[cl],
                           "valor_propuesto": g[0].get("valor_propuesto"), "fuentes": [f"AR_{e['anio']}.json · CF_{e['anio']}.txt p. {e['fuente']['pagina_pdf']}" for e in g],
                           "reserva": sorted({e["reserva"] for e in g if e.get("reserva")}) or None, "ids_matriz": [e["id"] for e in g],
                           "decision": None, "fecha": None, "confirmado_por": None,
                           "nota": "Campos decision, fecha y confirmado_por vacíos a propósito: solo los rellena la persona responsable, y solo en fase1_decisiones.json produce efecto (valor, fuente con página, fecha y persona). Esta propuesta no tiene efecto en el pipeline."})
    prop = {"tipo": "propuestas_n4_sin_firmar", "entrega": "4.9", "aviso": "Propuestas de la IA para revisión humana. La IA no confirma ceros ni escribe fase1_decisiones.json. Una clasificación documental favorable no equivale a una confirmación humana; P1 no autoriza otras confirmaciones.",
            "separacion": {"cobertura_documental": "matriz_n4.json → clasificacion", "registro_humano": "fase1_decisiones.json sin cambios (huella de la 4.8.1): conserva P1 (con fecha y firma) y la regla y las decisiones anteriores de deuda y arrendamientos (sin fecha ni firma en el archivo); ninguna de las 38 entradas está registrada", "estado_operativo": "el pipeline sigue tratando los 38 como pendientes («Dato no verificable»)"},
            "grupos": grupos}
    json.dump(prop, open(os.path.join(a.propuestas, "propuestas_n4_sin_firmar.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(recuento, open(os.path.join(a.salida, "recuento_n4.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps({"recuento": {k: recuento[k] for k in ("pendientes_en_fase1_v63", "ceros_heredados_csv_vidrala", "con_fila_en_la_historia", "auxiliares_sin_fila")}, "cobertura": cob}, ensure_ascii=False, indent=1))
    for e in matriz:
        print(f"{e['id']:36s} clase {e['clasificacion']} · cita en página {e['cita_en_su_pagina']} · comparativa {e.get('comparativa_coherente', '—')}" + (" · RESERVA" if e.get("reserva") else ""))


if __name__ == "__main__":
    main()
