#!/usr/bin/env python3
"""Batería F1 · US GAAP (ASC 842): motor A con arrendamientos operativos y financieros por separado, puente de deuda y K3 (F1_USGAAP.md).

Uso (desde personaje_v2/): python3 -B pruebas/test_motor_a_f1_usgaap.py
Sin LibreOffice: libros sintéticos con valores; las anclas (Historia C52, C53, C58) se calculan aquí con las fórmulas de la plantilla, en
coma flotante e independientes de motor_a_f1. Empresa estable de referencia: ventas 1.000; resultado antes de alquileres y amortizaciones
100; capex propio = D&A propia = 20; alquiler operativo 12 (coste lineal = pago: 10 de amortización no monetaria del derecho de uso y 2 de
actualización del pasivo). EBIT 68, CFO 88, FCF base 68: la caja sin crecimiento es 68. Con financieros: derecho de uso 5, interés 1 y
principal 5 → EBIT 63, CFO 87, FCF base 62.
Grupos: N (norma como valor cerrado y mezcla), U1–U7 (operativos: tramos fuera, dentro de la fila 8, dentro de la fila 14), U2 y U4
(financieros y C49), U5 (desglose ausente), H (hipótesis D-US1 y su cota), D (D-US2: pagos frente a coste lineal), P (puente de deuda y
motor B), K3, S (fuentes de las series y citas), V631 (fila 86 del libro), G13 (crecimiento e impuestos), NIIF (no cambia), EX (exigencia,
vigencia y gancho del pipeline) y CLI.
Ronda 2 (revisión R1 y decisiones D-US2 bis y D-WM del 18-nov-2026): cada expediente sintético lleva el texto del estado de flujos (texto/) y
las líneas que la fase 1 sumó en las filas 8 y 14 (fase1_partes), con la VERDAD de dónde están los dos tramos separada de lo que se DECLARA.
Grupos nuevos: F (contraste de ubicaciones: contrastada, sin contrastar → condicionada, contradicha → bloquea), R3 (los tres caminos de la
revisión: «fuera» falsa, «fila_8» falsa y «los dos en la fila 14» falsa; matriz verdad × declaración; error a la baja), B (D-US2 bis: valor de
la hoja y cuánto cambiaría contando los pagos), W (D-WM: financieros no desglosados como deuda), R6 («no_publicada» frente a la página), R7
(coste no comparable), R13 (C49: redondeo y diferencia explicada), R14 (declaraciones mal formadas), R15 (K3b según lo declarado), R16
(amortización financiera fuera de la fila 8), R9 (motor B: ancla de S2C), R1 (motor B: norma sin determinar, falla en cerrado) y R11 (norma
de la fase 1 como lista cerrada).
"""
import atexit
import copy
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from fractions import Fraction as Fr

AQUI = os.path.dirname(os.path.abspath(__file__))
PV = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(PV, "scripts"))
sys.dont_write_bytecode = True
import motor_a_f1 as M  # noqa: E402
import f1_libro_v631 as V631  # noqa: E402

R = []


def paso(nombre, ok, detalle=""):
    R.append((nombre, bool(ok)))
    print(("PASA " if ok else "FALLA") + " · " + nombre + (f" · {detalle}" if detalle else ""))


COLS = "CDEFGHIJKL"
ANIOS = list(range(2016, 2026))
REG = {"fecha": "2026-11-18", "persona": "prueba sintética (no es una decisión)", "motivo": "caso de prueba US GAAP"}
DOC = "10-K sintético"
TXT = "10K_sint.txt"                       # el texto que «usó la fase 1» (texto/) y la fuente registrada de la declaración
FUENTE = os.path.join("texto", TXT)
# etiquetas del estado de flujos sintético
DA, DA_ROU = "Depreciation and amortization", "Depreciation and amortization, including amortization of operating lease right-of-use assets"
L_AM, L_ACT, L_PAS = "Non-cash lease expense", "Operating lease right-of-use assets", "Operating lease liabilities"
WC = ("Accounts receivable", "Accounts payable and accrued liabilities")
NIKE_ACT = ("(Increase) decrease in prepaid expenses, operating lease right-of-use assets and", "other current and non-current assets")
NIKE_PAS = ("Increase (decrease) in accounts payable, accrued liabilities, operating lease", "liabilities and other current and non-current liabilities")


def lista(x):
    return [float(x)] * 10 if isinstance(x, (int, float)) else [float(v) for v in x]


def libro(ebit=68.0, da=20.0, dwc=0.0, C70=68.0, C49=0.0, princ=0.0, tau=0.0, capex=20.0, adq=0.0, ventas=1000.0, l4="US GAAP", c48=0.0, int16=0.0,
          fila22=100.0, fila23=0.0, motor="A", n=3, palancas=True, r=0.09):
    """Libro sintético V6.3 (solo valores): las mismas fórmulas de la plantilla que usa test_motor_a_f1.py, más las filas 22 y 23 (puente)."""
    V, E, D, T, K, A, W, PR = (lista(x) for x in (ventas, ebit, da, tau, capex, adq, dwc, princ))
    L = {"sha256": "sintetico", "Diagnóstico V6!C5": motor, "Control maestro!L4": l4, "Diagnóstico V6!C179": 0.05, "Análisis!C56": r}
    for i, c in enumerate(COLS):
        for fila, serie_ in ((5, ANIOS), (6, V), (7, E), (8, D), (10, T), (12, K), (13, A), (14, W), (17, PR)):
            L[f"Historia!{c}{fila}"] = serie_[i]
        L[f"Historia!{c}22"], L[f"Historia!{c}23"] = fila22, fila23
    w = range(10 - n, 10)
    S = sum(V[i] for i in w) / n
    nop = sum(E[i] * (1 - T[i]) for i in w) / n
    rei = sum(K[i] - D[i] + W[i] for i in w) / n
    L.update({"Historia!C58": ((nop - rei) - C70) / S, "Historia!C57": n, "Historia!C70": C70, "Historia!C44": V[-1], "Historia!C48": E[-1] / V[-1],
              "Historia!C52": sum(T[5:]) / 5, "Historia!C64": fila22 + fila23})
    den = sum(K[i] - D[i] + W[i] + A[i] for i in range(5, 10))
    L["Historia!C53"] = (V[-1] - V[4]) / den if den > 0 else ""
    for i, c in enumerate(COLS):   # FCF base y su segunda vía (fila 35), coherentes por construcción
        L[f"Historia!{c}11"] = C70 + K[i] + c48 + C49
        L[f"Historia!{c}16"], L[f"Historia!{c}18"] = int16, 0.0
        L[f"Historia!{c}35"] = L[f"Historia!{c}11"] - K[i] - int16 - PR[i]
    L["Análisis!C46"] = sum(L[f"Historia!{COLS[i]}11"] for i in w) / n
    L["Análisis!C47"], L["Análisis!C48"], L["Análisis!C49"], L["Análisis!C50"], L["Análisis!C51"], L["Análisis!C52"] = sum(K[i] for i in w) / n, c48, C49, 0.0, "Sí", C70
    if palancas:
        for c, (g15, mo, s2c, gi, roic) in {"B": (0.02, 0.07, 1.0, 0.01, 0.08), "C": (0.03, 0.07, 1.2, 0.02, 0.10), "D": (0.04, 0.08, 1.5, 0.025, 0.12)}.items():
            L[f"Palancas!{c}14"], L[f"Palancas!{c}15"], L[f"Palancas!{c}16"], L[f"Palancas!{c}18"], L[f"Análisis!{c}68"] = g15, mo, s2c, roic, gi
    for c, s in zip("BCD", (0.0047, 0.0068, 0.0241)):
        L[f"Diagnóstico V6!{c}178"], L[f"Diagnóstico V6!{c}176"], L[f"Diagnóstico V6!{c}177"] = s, s + 0.1, 0.1
    return L


def libro_v631(base, per, rou8, ppa=0.0):
    """Libro V6.3.1 F1 sintético (paso 7, sin palancas): sección F1 de la Historia y f y ancla con D_X, como las fórmulas de la plantilla."""
    L = dict(base)
    L.update({"Historia!A84": "  PERÍMETRO F1 DE LA REINVERSIÓN · motor A (V6.3.1 F1)", "Historia!C85": per, "Historia!C89": per})
    dx = []
    for i, c in enumerate(COLS):
        L[f"Historia!{c}86"], L[f"Historia!{c}87"] = rou8, ppa
        dx.append(L[f"Historia!{c}8"] - (rou8 if per != "A0_total" else 0) - (ppa if per == "A2_propio" else 0))
        L[f"Historia!{c}88"] = dx[-1]
    k = lambda f: [L[f"Historia!{c}{f}"] for c in COLS]  # noqa: E731
    V, E, T, K, A, W = k(6), k(7), k(10), k(12), k(13), k(14)
    w = range(7, 10)
    L["Historia!C58"] = (sum(E[i] * (1 - T[i]) for i in w) / 3 - sum(K[i] - dx[i] + W[i] for i in w) / 3 - L["Historia!C70"]) / (sum(V[i] for i in w) / 3)
    den = sum(K[i] - dx[i] + W[i] + A[i] for i in range(5, 10))
    L["Historia!C53"] = (V[-1] - V[4]) / den if den > 0 else None
    return L


def serie(vals, signo=1, pagina=1):
    """Serie declarada: signo 1 = cifra publicada en positivo; −1 = publicada entre paréntesis (cargo o salida) y magnitud positiva en el modelo."""
    vals = vals if isinstance(vals, dict) else {y: vals for y in ANIOS}
    out = {}
    for y, v in vals.items():
        vf = -v if signo == -1 else v
        out[str(y)] = {"valor_fuente": vf, "signo": signo, "tratamiento": "publicado entre paréntesis" if signo == -1 else "ninguno", "documento": DOC, "pagina": pagina,
                       "literal": f"({abs(vf)})" if vf < 0 else f"{vf}"}
    return out


# citas por omisión: la existencia de cada clase, en las notas (página 1); la ubicación de cada tramo, con su línea del estado de flujos (página 2)
CITAS = {("op", True): "Operating lease cost", ("op", False): "The Company has no operating leases", ("fin", True): "Finance lease cost",
         ("fin", False): "The Company has no finance leases", ("am", "fila_8"): DA_ROU, ("am", "fila_14"): L_ACT, ("am", "fuera_de_las_filas_8_y_14"): L_AM,
         ("pas", "fila_14"): L_PAS, ("pas", "fuera_de_las_filas_8_y_14"): L_PAS}


def ev(clave, valor):
    return {"documento": DOC, "pagina": 1, "cita": CITAS[(clave, valor)]}


def ubic(clave, u, pagina_np=2):
    if u is None:
        return {}
    if u == "no_publicada":
        return {"ubicacion": u, "documento": DOC, "pagina": pagina_np}
    return {"ubicacion": u, "documento": DOC, "pagina": 2, "cita": CITAS[(clave, u)]}


def decl(per="A0_total", norma="US_GAAP", op=True, fin=False, ub_am="fuera_de_las_filas_8_y_14", ub_pas="fuera_de_las_filas_8_y_14", P=12, Lc=12, a8=None,
         ajuste=None, pasivo=0, rou_fin=None, fin_princ=None, ppa=0, us=True, pagina_np=2):
    d = {"norma_contable": {"valor": norma, "registro": REG}, "perimetro_reinversion": {"valor": per, "registro": REG},
         "perimetro_margen": {"valor": "EBIT_NIIF16_PPA_constante", "registro": REG}, "perimetro_palancas_s2c": {"valor": per, "registro": REG},
         "perimetro_roic": {"valor": per, "registro": REG}, "clasificacion_compras": {"valor": "sin_compras", "registro": REG},
         "transicion": {"conocida": False, "tratamiento": None, "registro": REG}, "series": {"da_ppa": serie(ppa)}}
    if us:
        d["arrendamientos_us_gaap"] = {"registro": REG, "operativos": None if op is None else dict(ev("op", op), existen=op),
                                       "financieros": None if fin is None else dict(ev("fin", fin), existen=fin)}
        if op:
            d["arrendamientos_us_gaap"]["operativos"].update({"amortizacion_rou": ubic("am", ub_am, pagina_np), "variacion_pasivo": ubic("pas", ub_pas, pagina_np)})
            for nombre, v in (("pagos_arr_operativo", P), ("coste_arr_operativo", Lc)):
                if v is not None:
                    d["series"][nombre] = serie(v)
            if pasivo is not None:
                d["series"]["pasivo_arr_operativo"] = serie({2025: pasivo})
    if a8 is not None:
        d["series"]["da_rou_operativo"] = serie(a8)
    if ajuste is not None:
        d["series"]["circulante_arr_operativo"] = serie(ajuste, signo=-1 if (isinstance(ajuste, (int, float)) and ajuste > 0) else 1)
    if rou_fin is not None:
        d["series"]["da_rou"] = serie(rou_fin)
    if fin_princ is not None:
        d["series"]["pagos_arr_financiero_principal"] = serie(fin_princ, signo=-1)
    return d


# (cierre de la ronda 2, R2-2) cifra impresa de las líneas PROPIAS del arrendamiento operativo cuando la fase 1 las sumó en la fila 14, coherente con la
# empresa de referencia: la variación del pasivo consume 10 de caja («(10)» en el estado de flujos → +10 en la fila 14) y la amortización del derecho de
# uso se suma («10» → −10 en la fila 14). Las demás líneas llevan cifras cualesquiera (n, n+1, n+2)
IMPORTES = {"Operating lease liabilities": "(10)", "Operating lease right-of-use assets": "10"}


def _renglones(x, n, imp=None):
    """Texto de una línea del estado de flujos: una etiqueta (o una etiqueta partida en dos renglones) y sus tres cifras (imp, la misma en las tres
    columnas, o n, n+1 y n+2); devuelve (texto, renglón con cifras)."""
    partes = [x] if isinstance(x, str) else list(x)
    ultimo = f"{partes[-1]}    {imp}    {imp}    {imp}" if imp else f"{partes[-1]}    {n}    {n + 1}    {n + 2}"
    return "\n".join(partes[:-1] + [ultimo]), ultimo


def _verdad_de(d):
    """La verdad por omisión es la declarada: (amortización, pasivo) con «fuera», «fila_8», «fila_14» o «no» (la empresa no publica la línea)."""
    b = d.get("arrendamientos_us_gaap") if isinstance(d.get("arrendamientos_us_gaap"), dict) else {}
    op = b.get("operativos") if isinstance(b.get("operativos"), dict) else {}
    if not op.get("existen"):
        return "no", "no"
    u = lambda k: (op.get(k) or {}).get("ubicacion") if isinstance(op.get(k), dict) else None  # noqa: E731
    return ({"fuera_de_las_filas_8_y_14": "fuera", "fila_8": "fila_8", "fila_14": "fila_14"}.get(u("amortizacion_rou"), "no"),
            {"fuera_de_las_filas_8_y_14": "fuera", "fila_14": "fila_14"}.get(u("variacion_pasivo"), "no"))


def expediente(d, verdad=None, carpeta=None, partes=True, texto=True, da=None, wc=None, fuera=None, notas=(), anios_partes=range(2021, 2026), conceptos=None,
               por_anio=None, fila23=(), despues_cfo=(), importes=None, unidad="millones"):
    """Carpeta de expediente sintética para una declaración:
      - texto/10K_sint.txt, registrado como fuente con su huella. Página 1: notas (las cifras de las series, las citas de existencia y `notas`); página 2:
        el estado de flujos, con las líneas que la fase 1 sumó en la fila 8 (`da`) y en la fila 14 (`wc`) y las que no sumó (`fuera`); página 3: otra página;
      - fase1_partes/AR_<año>.json (2021–2025: el lado «anterior» de cada informe da el año anterior, como en fase1_historia), con el renglón de las cifras
        de cada línea sumada (y `conceptos` para el concepto que «escribió el agente»).
    `verdad` = (amortización, pasivo) dice dónde están DE VERDAD los dos tramos (por omisión, donde dice la declaración): «fuera» (línea propia que la fase 1
    no sumó), «fila_8» (la D&A la nombra), «fila_14» (línea propia sumada en el circulante) o «no» (la empresa no publica la línea).
    partes=False: sin fase1_partes; texto=False: la fuente está en la raíz y no hay texto/ (la fase 1 no puede reconstruir etiquetas partidas).
    importes: {etiqueta: cifra impresa} de las líneas sumadas en las filas 8 y 14 (por omisión, IMPORTES para las de la fila 14); unidad: la del informe."""
    carpeta = carpeta or tempfile.mkdtemp(prefix="f1_us_")
    v_am, v_pas = verdad if verdad is not None else _verdad_de(d)
    l_da = list(da) if da is not None else [DA_ROU if v_am == "fila_8" else DA]
    l_wc = list(wc) if wc is not None else list(WC) + ([L_ACT] if v_am == "fila_14" else []) + ([L_PAS] if v_pas == "fila_14" else [])
    l_fuera = list(fuera) if fuera is not None else ([L_AM] if v_am == "fuera" else []) + ([L_PAS] if v_pas == "fuera" else [])
    conceptos = conceptos or {}
    n, filas, comp = [10], [], {"da": [], "circulante_lineas": [], "cfo": [], "arrendamientos": []}

    def poner(x, k=None):
        n[0] += 3
        etq = x if isinstance(x, str) else " ".join(x)
        imp = (importes or {}).get(etq, IMPORTES.get(etq) if (k == "circulante_lineas" and importes is None) else None) if k in ("da", "circulante_lineas") else None
        txt, ult = _renglones(x, n[0], imp)
        filas.append(txt)
        if k:
            comp[k].append({"concepto": conceptos.get(x, etq), "impreso": imp or str(n[0]), "pagina": 2, "linea": ult})

    filas.append("CONSOLIDATED STATEMENTS OF CASH FLOWS")
    poner("Net income")
    for x in l_da:
        poner(x, "da")
    for x in l_fuera:
        poner(x)
    filas.append("Changes in operating assets and liabilities:")
    for x in l_wc:
        poner(x, "circulante_lineas")
    poner("Net cash provided by operating activities", "cfo")
    poner("Principal payments on finance lease obligations")
    for x in despues_cfo:   # líneas de inversión o de financiación (después del total del flujo de explotación)
        poner(x)
    filas.append("Supplemental disclosure:")
    poner("Right-of-use assets obtained in exchange for new operating lease liabilities")
    for x in fila23:   # líneas del balance que la fase 1 sumó en la fila 23 (pasivo por arrendamientos): solo en fase1_partes
        comp["arrendamientos"].append({"concepto": x, "impreso": "50", "pagina": 3, "linea": f"{x}    50    48"})
    lits = sorted({str(e.get("literal")) for s_ in (d.get("series") or {}).values() if isinstance(s_, dict) for e in s_.values() if isinstance(e, dict)})
    b = d.get("arrendamientos_us_gaap") if isinstance(d.get("arrendamientos_us_gaap"), dict) else {}
    citas = [(b.get(k) or {}).get("cita") for k in ("operativos", "financieros") if isinstance(b.get(k), dict)]
    txt = ("[PDF PAGE 1]\nNotas sintéticas: " + " ".join(lits) + "\n" + "\n".join(sorted({c for c in citas if isinstance(c, str)} | set(notas))) + "\n"
           + "[PDF PAGE 2]\n" + "\n".join(filas) + "\n[PDF PAGE 3]\nCONSOLIDATED BALANCE SHEETS\n" + "\n".join(f"{x}    50    48" for x in fila23) + "\n[PDF PAGE 4]\n")
    arch = FUENTE if texto else TXT
    os.makedirs(os.path.dirname(os.path.join(carpeta, arch)) or carpeta, exist_ok=True)
    open(os.path.join(carpeta, arch), "w", encoding="utf-8").write(txt)
    d["fuentes_series"] = {DOC: {"archivo": arch, "sha256": hashlib.sha256(txt.encode("utf-8")).hexdigest()}}
    if partes:
        os.makedirs(os.path.join(carpeta, "fase1_partes"), exist_ok=True)
        for a in anios_partes:
            j = {"anio": a, "archivo": TXT, "unidad": unidad, "partidas": {k: {"actual": copy.deepcopy(v), "anterior": copy.deepcopy(v), "cero": None} for k, v in comp.items()}}
            if por_anio:
                j = por_anio(a, j)
            if j is not None:
                json.dump(j, open(os.path.join(carpeta, "fase1_partes", f"AR_{a}.json"), "w", encoding="utf-8"), ensure_ascii=False)
    return carpeta


def fuentes(d, carpeta=None):
    """Solo la fuente (sin fase1_partes): las ubicaciones declaradas no se pueden contrastar con las líneas de la fase 1."""
    return expediente(d, carpeta=carpeta, partes=False)


TMP = []
# las carpetas temporales se borran también si la batería se interrumpe (una excepción a medio camino no llega al «finally» del final)
atexit.register(lambda: [shutil.rmtree(t, ignore_errors=True) for t in TMP])


def ev_(L, d, con_fuentes=True, motor_libro=None, **k):
    """Evalúa con el expediente sintético escrito (fuente, texto del estado de flujos y fase1_partes; por omisión, la verdad es lo declarado)."""
    c = None
    if con_fuentes:
        c = expediente(d, **k)
        TMP.append(c)
    return M.evaluar(L, d, carpeta=c, motor_libro=motor_libro)


def g(r, gid):
    return [x for x in r["guardas"] if x["id"] == gid]


def salta(r, gid):
    return any(x["salta"] for x in g(r, gid))


def bloquea(r, gid):
    return any(x["salta"] and x["severidad"] == "BLOQUEA" for x in g(r, gid))


def bloquean(r):
    return sorted({x["id"] for x in r["guardas"] if x["salta"] and x["severidad"] == "BLOQUEA"})


def F0(r, p=None):
    return (r["diagnostico_por_perimetro"][p] if p else r["calculo_perimetro_declarado"])["flujo_sin_crecimiento"]


def cerca(a, b, tol=1e-9):
    return a is not None and abs(a - b) < tol


def cotas(r):
    """{texto: variación del flujo sin crecimiento en mm} de la cota de una conclusión condicionada."""
    return {k: v["variacion_maxima_del_flujo_sin_crecimiento_mm"] for k, v in ((r.get("condicionada") or {}).get("cota") or {}).items()
            if isinstance(v, dict) and "variacion_maxima_del_flujo_sin_crecimiento_mm" in v}


def estado_tramo(r, clave):
    return (((r.get("us_gaap") or {}).get("contraste_de_ubicaciones") or {}).get("tramos") or {}).get(clave, {}).get("estado")


# ================================================================== N · la norma es un valor cerrado (H13) y no se mezcla
LN = libro(l4="IFRS (adoptadas por la Unión Europea)")
dN = decl(norma="NIIF", us=False, ppa=0)
dN["series"]["da_rou"] = serie(0)
rN = ev_(LN, dN)
paso("N · NIIF con el libro «IFRS (adoptadas por la Unión Europea)» (variante histórica registrada): F1-NORMA no salta", not salta(rN, "F1-NORMA"))
for l4, txt in (("US GAAP (no IFRS)", "H13: «US GAAP (no IFRS)» ya no pasa como NIIF"), ("Otro", "«Otro»"), ("IFRS y US GAAP", "un texto con las dos normas"), ("", "L4 vacío")):
    paso(f"N · NIIF declarada y libro con {txt}: F1-NORMA bloquea", bloquea(ev_(libro(l4=l4), dN), "F1-NORMA"), g(ev_(libro(l4=l4), dN), "F1-NORMA")[0]["detalle"][:90])
paso("N · mezcla: NIIF declarada y libro «US GAAP» → F1-NORMA (DATOS INVÁLIDOS, «mezcla de normas»)",
     bloquea(ev_(libro(), dN), "F1-NORMA") and "mezcla de normas" in g(ev_(libro(), dN), "F1-NORMA")[0]["detalle"])
rmz = ev_(libro(l4="IFRS"), decl())
paso("N · mezcla: US_GAAP declarada y libro «IFRS» → F1-NORMA (DATOS INVÁLIDOS)", bloquea(rmz, "F1-NORMA") and g(rmz, "F1-NORMA")[0]["efecto"] == "DATOS INVÁLIDOS"
     and rmz["estado_propuesto"] == "pendiente_de_datos")
d_esp = decl()
d_esp["norma_contable"]["valor"] = "US GAAP"
paso("N · la declaración solo admite los identificadores NIIF y US_GAAP: «US GAAP» (con espacio) bloquea", bloquea(ev_(libro(), d_esp), "F1-NORMA"))
paso("N · libro «us gaap» (sin distinguir mayúsculas ni espacios de más) y «US GAAP» son el mismo valor de la lista", M.norma_del_libro({"Control maestro!L4": " us  gaap "}) == "US_GAAP"
     and M.norma_del_libro({"Control maestro!L4": "US GAAP"}) == "US_GAAP" and M.norma_del_libro({"Control maestro!L4": "US-GAAP"}) is None)
d_mix = copy.deepcopy(dN)
d_mix["arrendamientos_us_gaap"] = decl()["arrendamientos_us_gaap"]
paso("N · F1-US-MEZCLA: declaración NIIF con «arrendamientos_us_gaap» o con series de US GAAP → DATOS INVÁLIDOS", bloquea(ev_(LN, d_mix), "F1-US-MEZCLA")
     and bloquea(ev_(LN, dict(dN, series=dict(dN["series"], pagos_arr_operativo=serie(12)))), "F1-US-MEZCLA")
     and bloquea(ev_(LN, dict(dN, series=dict(dN["series"], caja_pagada_arr_financiero=serie(9)))), "F1-US-MEZCLA"))
r48 = ev_(libro(c48=3.0, C70=65.0), decl())
paso("N · F1-US-MEZCLA: US GAAP con intereses pagados «en financiación» (C48 = 3) → DATOS INVÁLIDOS (se restarían dos veces)", bloquea(r48, "F1-US-MEZCLA")
     and g(r48, "F1-US-MEZCLA")[0]["efecto"] == "DATOS INVÁLIDOS")
paso("N · con NIIF no aparece ninguna guarda F1-US-*, ni el bloque us_gaap, ni la huella de fase1_partes, aunque el expediente las tenga",
     not [x for x in rN["guardas"] if x["id"].startswith("F1-US")] and "us_gaap" not in rN and "fase1_partes_sha256" not in rN)

# ================================================================== U1 · solo operativos, los dos tramos fuera de las filas 8 y 14 (línea propia que la fase 1 no sumó)
L1 = libro()
r1 = ev_(L1, decl("A0_total"))
paso("U1 · solo operativos, tramos fuera de las filas: A0 da 68 = FCF base (el alquiler ya está una vez en el EBIT y en el CFO)", cerca(F0(r1), 68) and cerca(F0(r1, "A2_propio"), 68))
paso("U1 · las dos ubicaciones contrastadas con su línea (del estado de flujos y no sumada por la fase 1): ninguna guarda bloquea; utilizable sin hipótesis ni condición",
     r1["utilizable_para_conclusion"] and not bloquean(r1) and "condicionada" not in r1 and "CONDICIONADA" not in r1["rotulo"] and not salta(r1, "F1-US-FILAS")
     and estado_tramo(r1, "amortizacion_rou") == "contrastada" and estado_tramo(r1, "variacion_pasivo") == "contrastada", f"{bloquean(r1)} · {g(r1, 'F1-US-FILAS')[0]['detalle'][:140]}")
paso("U1 · K3b: alquiler contado una vez (operativos), contrastado con las líneas del expediente; K3 conforme", r1["K3"]["K3b_alquiler_contado"] == "una vez"
     and r1["K3"]["K3b_por_clase"] == {"operativos": "una vez"} and r1["K3"]["K3b_contrastado"] is True and r1["K3"]["conforme"] is True)
paso("U1 · F1-SERIES examina las series de US GAAP y las cuatro citas de clasificación en su página", not salta(r1, "F1-SERIES")
     and r1["F1_SERIES"]["citas_de_clasificacion_comprobadas"] == 4, g(r1, "F1-SERIES")[0]["detalle"][:120])
r1b = ev_(L1, decl("A2_propio"))
paso("U1 · con A2 declarado en un libro V6.3 solo bloquea F1-LIBRO (el libro calcula A0): límite declarado, como en NIIF", bloquean(r1b) == ["F1-LIBRO"] and cerca(F0(r1b), 68))
rsin = ev_(L1, decl("A0_total", op=False, P=None, Lc=None, pasivo=None))
paso("U1 · US GAAP sin arrendamientos de ninguna clase (declarado con su evidencia; ninguna línea sumada nombra un arrendamiento): A0 utilizable; K3b «ninguna vez (sin arrendamientos)»",
     rsin["utilizable_para_conclusion"] and rsin["K3"]["K3b_alquiler_contado"] == "ninguna vez (sin arrendamientos)" and rsin["K3"]["conforme"] is True, str(bloquean(rsin)))

# ================================================================== U2 · operativos + financieros (los financieros, como NIIF 16)
L2 = libro(ebit=63.0, da=25.0, C70=62.0, C49=5.0, princ=5.0)
d2 = decl("A2_propio", fin=True, rou_fin=5, fin_princ=5)
r2 = ev_(L2, d2)
paso("U2 · operativos + financieros: A2 da 62 = FCF base; A0 da 57 (la amortización del derecho de uso financiero contada dos veces)", cerca(F0(r2), 62)
     and cerca(F0(r2, "A0_total"), 57))
paso("U2 · con A2 solo bloquea F1-LIBRO; K3b una vez en las dos clases; F1-US-C49 no salta (C49 = principal financiero publicado)",
     bloquean(r2) == ["F1-LIBRO"] and r2["K3"]["K3b_por_clase"] == {"operativos": "una vez", "financieros": "una vez"} and not salta(r2, "F1-US-C49"), str(bloquean(r2)))
r2a = ev_(L2, decl("A0_total", fin=True, rou_fin=5, fin_princ=5))
paso("U2 · con A0 bloquea V-F1a (financieros) y K3b dice «financieros: dos veces»", bloquea(r2a, "V-F1a") and bloquea(r2a, "F1-K3b")
     and r2a["K3"]["K3b_por_clase"]["financieros"] == "dos veces" and r2a["K3"]["K3b_por_clase"]["operativos"] == "una vez", r2a["K3"]["K3b_alquiler_contado"])
r2s = ev_(libro(ebit=63.0, da=25.0, C70=67.0, C49=0.0), decl("A2_propio", fin=True, rou_fin=5, fin_princ=5))
paso("U9 · simétrica de los financieros: A2 con derecho de uso financiero y C49 = 0 → F1-M-SIM y F1-US-C49 (principal publicado omitido); K3b «financieros: ninguna vez»",
     bloquea(r2s, "F1-M-SIM") and bloquea(r2s, "F1-US-C49") and "se omitiría" in g(r2s, "F1-US-C49")[0]["detalle"] and r2s["K3"]["K3b_por_clase"]["financieros"] == "ninguna vez")
r2n = ev_(L2, decl("A2_propio", fin=True, rou_fin=5))
paso("U2 · financieros sin su principal publicado declarado → F1-US-C49 INCOMPLETO (no se puede descartar que C49 lleve pagos operativos; la salida si no se publica: D-WM)",
     bloquea(r2n, "F1-US-C49") and g(r2n, "F1-US-C49")[0]["efecto"] == "INCOMPLETO" and "D-WM" in g(r2n, "F1-US-C49")[0]["detalle"])
r2i = ev_(L2, decl("A2_propio", fin=False, rou_fin=5))
paso("U2 · «financieros.existen = false» con importes en da_rou → F1-US-DESGLOSE DATOS INVÁLIDOS (incoherencia)", bloquea(r2i, "F1-US-DESGLOSE")
     and g(r2i, "F1-US-DESGLOSE")[0]["efecto"] == "DATOS INVÁLIDOS")

# ================================================================== U3 · la D&A (fila 8) lleva la amortización del derecho de uso operativo (y su línea lo dice)
L3 = libro(da=30.0)
r3 = ev_(L3, decl("A0_total", ub_am="fila_8", a8=10))
paso("U3 · derecho de uso operativo dentro de la D&A con A0: F1-US-DA bloquea (MODELO NO APLICABLE); A0 daría 58 frente a la caja 68", bloquea(r3, "F1-US-DA")
     and g(r3, "F1-US-DA")[0]["efecto"] == "MODELO NO APLICABLE" and cerca(F0(r3, "A0_total"), 58))
paso("U3 · K3b «operativos: dos veces» (F1-K3b bloquea) y K3c también (reinversión media −10 con ventas estables)", bloquea(r3, "F1-K3b")
     and r3["K3"]["K3b_por_clase"] == {"operativos": "dos veces"} and bloquea(r3, "F1-K3c") and r3["K3"]["conforme"] is False)
paso("U3 · el puente K3 de A0 señala 10 de doble cómputo (clase doble_computo)",
     cerca(r3["diagnostico_por_perimetro"]["A0_total"]["K3"]["doble_computo_por_clase_a_la_escala_del_año_base"]["doble_computo"], 10))
r3b = ev_(L3, decl("A2_propio", ub_am="fila_8", a8=10))
paso("U3 · con A2 la excluye de D_X ((1a) b): 68; alquiler una vez; contrastada (la línea de la D&A sumada nombra el derecho de uso); solo bloquea F1-LIBRO en un libro V6.3",
     cerca(F0(r3b), 68) and bloquean(r3b) == ["F1-LIBRO"] and r3b["K3"]["K3b_alquiler_contado"] == "una vez" and estado_tramo(r3b, "amortizacion_rou") == "contrastada"
     and "condicionada" not in r3b, str(bloquean(r3b)))
r3c = ev_(L3, decl("A2_propio", ub_am="fila_8"))
paso("U3 · ubicación «fila_8» sin su serie da_rou_operativo: F1-US-DESGLOSE INCOMPLETO y el perímetro no es calculable (vacío ≠ 0)", bloquea(r3c, "F1-US-DESGLOSE")
     and bloquea(r3c, "F1-PERIMETRO") and r3c["calculo_perimetro_declarado"] is None and r3c["estado_propuesto"] == "pendiente_de_datos")
r3d = ev_(L3, decl("A2_propio", a8=10))
paso("U3 · importes en da_rou_operativo con la amortización declarada fuera de la fila 8 → incoherencia (DATOS INVÁLIDOS)", bloquea(r3d, "F1-US-DESGLOSE")
     and g(r3d, "F1-US-DESGLOSE")[0]["efecto"] == "DATOS INVÁLIDOS")
r9 = ev_(L3, decl("A2_propio", ub_am="fila_8", a8=10, P=0))
paso("U9 · simétrica de los operativos: amortización excluida de D_X sin pagos dentro del CFO (pagos declarados a cero) → F1-US-SIM (FUERA DEL DOMINIO); K3b «ninguna vez»",
     bloquea(r9, "F1-US-SIM") and g(r9, "F1-US-SIM")[0]["efecto"] == "FUERA DEL DOMINIO" and r9["K3"]["K3b_por_clase"]["operativos"] == "ninguna vez")

# ================================================================== U4 · C49 con pagos de arrendamientos operativos (ya están en el CFO)
L4 = libro(C70=56.0, C49=12.0, princ=12.0)
r4 = ev_(L4, decl("A0_total"))
paso("U4 · C49 = 12 sin arrendamientos financieros: F1-US-C49 bloquea (DATOS INVÁLIDOS: los pagos operativos se restarían dos veces); FCF base 56 frente a 68",
     bloquea(r4, "F1-US-C49") and g(r4, "F1-US-C49")[0]["efecto"] == "DATOS INVÁLIDOS" and "dos veces" in g(r4, "F1-US-C49")[0]["detalle"] and cerca(F0(r4), 56))
paso("U4 · K3a no lo ve (C49 y la fila 17 llevan el mismo error) pero K3b sí: «operativos: dos veces»", not salta(r4, "F1-K3a") and bloquea(r4, "F1-K3b")
     and r4["K3"]["K3b_por_clase"] == {"operativos": "dos veces"})
r4b = ev_(libro(ebit=63.0, da=25.0, C70=50.0, C49=17.0, princ=17.0), decl("A2_propio", fin=True, rou_fin=5, fin_princ=5))
paso("U4 · con financieros: C49 = 17 frente a 5 de principal financiero publicado → exceso de 12 (pagos operativos): bloquea; operativos dos veces, financieros una",
     bloquea(r4b, "F1-US-C49") and "12.0" in g(r4b, "F1-US-C49")[0]["detalle"] and r4b["K3"]["K3b_por_clase"] == {"operativos": "dos veces", "financieros": "una vez"})
r4c = ev_(libro(ebit=63.0, da=25.0, C70=62.0, C49=5.004, princ=5.004), decl("A2_propio", fin=True, rou_fin=5, fin_princ=5))
paso("U4 · tolerancia de redondeo: C49 = 5,004 frente a 5 de principal (≤ 0,005) no salta", not salta(r4c, "F1-US-C49"))

# ================================================================== U5 · desglose operativo/financiero ausente
r5 = ev_(L1, decl("A0_total", us=False))
paso("U5 · US GAAP sin «arrendamientos_us_gaap»: F1-US-DESGLOSE (INCOMPLETO) → pendiente_de_datos; ya no es un límite del modelo por F1-NORMA",
     bloquea(r5, "F1-US-DESGLOSE") and g(r5, "F1-US-DESGLOSE")[0]["efecto"] == "INCOMPLETO" and r5["estado_propuesto"] == "pendiente_de_datos" and not salta(r5, "F1-NORMA"))
paso("U5 · sin el desglose K3b no afirma nada («no evaluable») y K3 no es conforme", "no evaluable" in r5["K3"]["K3b_alquiler_contado"] and r5["K3"]["conforme"] is False)
for nombre, d_ in (("sin decir si hay financieros", decl(fin=None)), ("sin decir si hay operativos", decl(op=None)),
                   ("sin la ubicación de la variación del pasivo", decl(ub_pas=None)), ("sin la ubicación de la amortización", decl(ub_am=None)),
                   ("sin los pagos operativos", decl(P=None)), ("sin el coste lineal (D-US2: la diferencia tiene que quedar a la vista)", decl(Lc=None))):
    rr = ev_(L1, d_)
    paso(f"U5 · {nombre}: F1-US-DESGLOSE bloquea (INCOMPLETO)", bloquea(rr, "F1-US-DESGLOSE") and g(rr, "F1-US-DESGLOSE")[0]["efecto"] == "INCOMPLETO",
         g(rr, "F1-US-DESGLOSE")[0]["detalle"][:110])
r5p = ev_(L1, decl(pasivo=None))
paso("U5 · motor A sin el pasivo operativo del último ejercicio: no bloquea (el motor A no resta deuda); F1-US-PUENTE avisa de que el puente no se puede comprobar",
     r5p["utilizable_para_conclusion"] and g(r5p, "F1-US-PUENTE")[0]["severidad"] == "AVISO", g(r5p, "F1-US-PUENTE")[0]["detalle"][:110])
r5h = ev_(libro(dwc=10.0), decl("A0_total", ub_pas="fila_14", ajuste={y: 10 for y in ANIOS[-3:]}))
paso("U5 · el importe que se retira del circulante hace falta en la ventana de f y en los años H–L del ancla: declarado solo en la ventana → INCOMPLETO",
     bloquea(r5h, "F1-US-DESGLOSE") and "2021" in g(r5h, "F1-US-DESGLOSE")[0]["detalle"] and "2022" in g(r5h, "F1-US-DESGLOSE")[0]["detalle"])
d5r = decl()
d5r["arrendamientos_us_gaap"]["registro"] = {"fecha": "2026-11-18", "persona": "", "motivo": "x"}
paso("U5 · «arrendamientos_us_gaap» sin registro (fecha, persona, motivo) → bloquea: lo declara la persona, no el agente", bloquea(ev_(L1, d5r), "F1-US-DESGLOSE"))
d5u = decl()
d5u["arrendamientos_us_gaap"]["operativos"]["variacion_pasivo"]["ubicacion"] = "fila_8"
paso("U5 · ubicación no admitida (la variación del pasivo no puede estar en la fila 8) → DATOS INVÁLIDOS", g(ev_(L1, d5u), "F1-US-DESGLOSE")[0]["efecto"] == "DATOS INVÁLIDOS")
d5x = decl()
del d5x["arrendamientos_us_gaap"]["financieros"]["cita"]
paso("U5 · «financieros.existen = false» sin su evidencia (documento, página y cita) → INCOMPLETO: la ausencia también se documenta",
     bloquea(ev_(L1, d5x), "F1-US-DESGLOSE") and "financieros" in g(ev_(L1, d5x), "F1-US-DESGLOSE")[0]["detalle"])
d5e = decl()
del d5e["arrendamientos_us_gaap"]["operativos"]["amortizacion_rou"]["cita"]
paso("U5 · clasificación sin su cita literal → INCOMPLETO", bloquea(ev_(L1, d5e), "F1-US-DESGLOSE") and "cita" in g(ev_(L1, d5e), "F1-US-DESGLOSE")[0]["detalle"])

# ================================================================== U6 · un solo tramo dentro de la fila 14 (su importe se retira del circulante)
L6 = libro(dwc=10.0)
r6 = ev_(L6, decl("A0_total", ub_pas="fila_14", ajuste=10))
paso("U6 · variación del pasivo sola en la fila 14: el libro tal cual daría 78 (omite el alquiler); la capa la retira del circulante y da 68",
     cerca(L6["Historia!C58"], -0.01) and cerca(F0(r6), 68) and cerca(F0(r6, "A2_propio"), 68))
paso("U6 · ningún libro la retira: F1-LIBRO bloquea (límite declarado, con su salida) y es lo único que bloquea; la réplica del libro sigue conforme",
     bloquean(r6) == ["F1-LIBRO"] and "LÍMITE DECLARADO" in g(r6, "F1-LIBRO")[0]["detalle"] and "corrección registrada" in g(r6, "F1-LIBRO")[0]["detalle"]
     and not salta(r6, "F1-REPLICA") and r6["estado_propuesto"] == "no_entregable · limite_del_modelo", str(bloquean(r6)))
paso("U6 · K3b con el ajuste: una vez; el puente K3 muestra la partida retirada (−10) y cuadra; la línea del pasivo está entre las sumadas en la fila 14 (contrastada)",
     r6["K3"]["K3b_alquiler_contado"] == "una vez" and r6["calculo_perimetro_declarado"]["K3"]["identidad_cuadra"] and estado_tramo(r6, "variacion_pasivo") == "contrastada"
     and any("se retira del circulante" in ln["partida"] and cerca(ln["mm"], -10) for ln in r6["calculo_perimetro_declarado"]["K3"]["lineas"]))
r6b = ev_(L6, decl("A0_total", ub_pas="fila_14"))
paso("U6 · sin el importe declarado: F1-US-SIM (FUERA DEL DOMINIO: el alquiler se omitiría) y F1-US-DESGLOSE; K3b «operativos: ninguna vez»; no calculable",
     bloquea(r6b, "F1-US-SIM") and bloquea(r6b, "F1-US-DESGLOSE") and bloquea(r6b, "F1-K3b") and r6b["K3"]["K3b_por_clase"] == {"operativos": "ninguna vez"}
     and r6b["calculo_perimetro_declarado"] is None and r6b["estado_propuesto"] == "pendiente_de_datos")
r6c = ev_(L6, decl("A0_total", ub_pas="fila_14", ajuste=10), motor_libro="A")
L6p7 = libro(dwc=10.0, palancas=False)
r6p7 = ev_(L6p7, decl("A0_total", ub_pas="fila_14", ajuste=10))
paso("U6 · también en el paso 7 (sin palancas ni flujos en el libro) F1-LIBRO bloquea por el ajuste declarado", bloquea(r6p7, "F1-LIBRO") and bloquea(r6c, "F1-LIBRO"))
r6d = ev_(L1, decl("A0_total", ajuste=10))
paso("U6 · importes en circulante_arr_operativo sin ningún tramo declarado dentro de la fila 14 → incoherencia (DATOS INVÁLIDOS)",
     g(r6d, "F1-US-DESGLOSE")[0]["efecto"] == "DATOS INVÁLIDOS")
r6e = ev_(libro(dwc=-10.0), decl("A0_total", ub_am="fila_14", ajuste=-10))
paso("U6 · la amortización (baja del activo) sola en la fila 14 (−10): tal cual se contaría dos veces (58); retirada con su signo, 68",
     cerca(F0(r6e), 68) and bloquean(r6e) == ["F1-LIBRO"], str(bloquean(r6e)))
r6f = ev_(libro(dwc=-10.0), decl("A0_total", ub_am="fila_14"))
paso("U6 · …y sin su importe: F1-US-DA (dos veces) y K3b «operativos: dos veces»", bloquea(r6f, "F1-US-DA") and r6f["K3"]["K3b_por_clase"] == {"operativos": "dos veces"})

# ================================================================== B · los dos tramos dentro de la fila 14 · D-US2 bis: el valor de la hoja y cuánto cambiaría contando los pagos
OP_ = lambda d: d["arrendamientos_us_gaap"]["operativos"]  # noqa: E731
r7 = ev_(L1, decl("A0_total", ub_am="fila_14", ub_pas="fila_14"))
paso("B · los dos tramos dentro de la fila 14 con coste lineal = pagos: el expediente muestra las dos líneas (activo y pasivo); 68; utilizable sin condición; nada se retira",
     cerca(F0(r7), 68) and r7["utilizable_para_conclusion"] and "condicionada" not in r7 and r7["us_gaap"]["D_US2_bis"]["dos_lineas_comprobadas"] is True
     and r7["us_gaap"]["operativos"]["retirado_del_circulante_medio"] is None and r7["us_gaap"]["base_del_arrendamiento_operativo"].startswith("coste contable")
     and cerca(r7["us_gaap"]["D_US2_bis"]["contando_los_pagos"]["variacion_maxima_del_flujo_sin_crecimiento_mm"], 0), str(bloquean(r7)))
# coste lineal 12, pagos 13: EBIT 68, CFO 87, FCF base 67. Con los dos tramos netos en la fila 14, la fila 14 lleva pagos − coste = +1 y la hoja da 68 (cuenta el coste)
L7 = libro(dwc=1.0, C70=67.0)
r7b = ev_(L7, decl("A0_total", ub_am="fila_14", ub_pas="fila_14", P=13, Lc=12))
b7 = r7b["us_gaap"]["D_US2_bis"]
paso("B · D-US2 bis con pagos 13 ≠ coste 12: NO bloquea; se publica el valor de la hoja (68, cuenta el coste contable) y la capa no retira nada (F1-LIBRO no salta)",
     cerca(L7["Historia!C58"], 0.0) and cerca(F0(r7b), 68) and bloquean(r7b) == [] and r7b["utilizable_para_conclusion"] and not salta(r7b, "F1-LIBRO")
     and "coste contable" in b7["valor_publicado"] and cerca(b7["flujo_sin_crecimiento_de_la_hoja"], 68), str(bloquean(r7b)))
paso("B · …y al lado cuánto cambiaría contando los pagos: −1 mm (−1,47 % del flujo sin crecimiento: 67 = FCF base), con el registro de la decisión (18-nov-2026)",
     cerca(b7["contando_los_pagos"]["variacion_maxima_del_flujo_sin_crecimiento_mm"], -1.0) and cerca(b7["contando_los_pagos"]["variacion_maxima_del_flujo_sin_crecimiento_%"], -1.471, 1e-3)
     and b7["registro"]["fecha"] == "2026-11-18" and "112–114" in b7["registro"]["motivo"] and b7["neto_derivado_de_pagos_menos_coste_en"] == ANIOS, b7["texto"][:200])
vp7 = b7["contando_los_pagos"]["por_escenario (valor presente de los flujos a la r del libro, sin exceso de caja ni quiebra)"]
paso("B · …también en valor presente de los flujos por escenario (NORMAL: −0,001 × Σ ventas descontadas; réplica independiente más abajo, en H)",
     set(vp7) == {"MALO", "NORMAL", "BUENO"} and vp7["NORMAL"]["variacion_maxima_del_valor_presente_de_los_flujos_mm"] < 0 and "escenario NORMAL" in b7["texto"])
paso("B · queda a la vista en el rótulo y en F1-US-BASE (AVISO, no bloquea), con «D-US2 bis», «coste contable» y la cifra; no es una hipótesis (no se rotula condicionada)",
     "D-US2 bis" in r7b["rotulo"] and "coste contable" in r7b["rotulo"] and "-1.000 mm" in r7b["rotulo"] and g(r7b, "F1-US-BASE")[0]["severidad"] == "AVISO"
     and "CONDICIONADA" not in r7b["rotulo"] and "condicionada" not in r7b, r7b["rotulo"][:220])
r7m = ev_(libro(dwc=0.001, C70=67.999), decl("A0_total", ub_am="fila_14", ub_pas="fila_14", P=12.001, Lc=12))
paso("B · una milésima de diferencia (pagos 12,001 y coste 12) tampoco bloquea (antes: límite del modelo): 68; contando los pagos, −0,001",
     bloquean(r7m) == [] and cerca(F0(r7m), 68) and cerca(r7m["us_gaap"]["D_US2_bis"]["contando_los_pagos"]["variacion_maxima_del_flujo_sin_crecimiento_mm"], -0.001, 1e-9))
r7w = ev_(L7, decl("A0_total", ub_am="fila_14", ub_pas="fila_14", P={y: 13 for y in ANIOS[-3:]}, Lc={y: 12 for y in ANIOS[-3:]}))
paso("B · pagos y coste hacen falta solo en la ventana (no en los años del ancla): con los tres años de la ventana, utilizable", bloquean(r7w) == [] and cerca(F0(r7w), 68)
     and cerca(r7w["us_gaap"]["D_US2_bis"]["contando_los_pagos"]["variacion_maxima_del_flujo_sin_crecimiento_mm"], -1.0), str(bloquean(r7w)))
r7c = ev_(L7, decl("A0_total", ub_am="fila_14", ub_pas="fila_14", P=13, Lc=12, ajuste=1))
paso("B · con la línea neta publicada declarada («(1)»: +1 en la fila 14) manda el dato: misma cifra (−1 contando los pagos) sin derivar nada; el valor publicado sigue siendo el de la hoja",
     cerca(F0(r7c), 68) and bloquean(r7c) == [] and r7c["us_gaap"]["D_US2_bis"]["neto_derivado_de_pagos_menos_coste_en"] == []
     and cerca(r7c["us_gaap"]["D_US2_bis"]["contando_los_pagos"]["variacion_maxima_del_flujo_sin_crecimiento_mm"], -1.0), str(bloquean(r7c)))
r7s = ev_(L7, decl("A0_total", ub_am="fila_14", ub_pas="fila_14", P=13, Lc=12), partes=False)
paso("B · antes, el programa comprueba que el expediente muestra las dos líneas: sin fase1_partes no se puede comprobar → F1-US-FILAS INCOMPLETO (pendiente_de_datos), nunca el valor de la hoja",
     bloquean(r7s) == ["F1-US-FILAS"] and g(r7s, "F1-US-FILAS")[0]["efecto"] == "INCOMPLETO" and "D-US2 bis" in g(r7s, "F1-US-FILAS")[0]["detalle"]
     and r7s["estado_propuesto"] == "pendiente_de_datos" and "condicionada" not in r7s, g(r7s, "F1-US-FILAS")[0]["detalle"][:200])
# pagos 11 < coste 12 en la empresa estable (capex = D&A): el neto dentro de la fila 14 es −1 y la reinversión media de la hoja sale negativa. K3c lo señala como
# siempre (no es nuevo): bloquea sin justificación y avisa con ella. No es un bloqueo de D-US2 bis
L7n = libro(dwc=-1.0, C70=69.0)
d7n = decl("A0_total", ub_am="fila_14", ub_pas="fila_14", P=11, Lc=12)
r7n = ev_(L7n, d7n)
d7j = dict(copy.deepcopy(d7n), justificacion_reinversion_negativa="el circulante lleva −1 del arrendamiento operativo (coste 12, pagos 11); capex = D&A propia")
r7j = ev_(L7n, d7j)
paso("B · con pagos 11 < coste 12 y capex = D&A la reinversión media de la hoja es −1: K3c bloquea sin justificación (regla general, no de D-US2 bis) y con ella avisa: "
     "utilizable, valor de la hoja 68 y +1 contando los pagos", bloquean(r7n) == ["F1-K3c"] and bloquean(r7j) == [] and cerca(F0(r7j), 68)
     and cerca(r7j["us_gaap"]["D_US2_bis"]["contando_los_pagos"]["variacion_maxima_del_flujo_sin_crecimiento_mm"], 1.0), f"{bloquean(r7n)} · {bloquean(r7j)}")
# caso Nike: las dos líneas son mezcladas y están partidas en dos renglones; el agente abrevió el concepto y la «linea» de la fase 1 es el segundo renglón
C_NIKE = {NIKE_ACT: "Prepaid expenses, ROU assets and other assets", NIKE_PAS: "Accounts payable, accrued liabilities and other liabilities"}
WC_NIKE = ("Accounts receivable", "Inventories", NIKE_ACT, NIKE_PAS)


def d_nike(**k):
    d = decl("A0_total", ub_am="fila_14", ub_pas="fila_14", P=13, Lc=12, **k)
    OP_(d)["amortizacion_rou"]["cita"] = "prepaid expenses, operating lease right-of-use assets and other current and non-current assets"
    OP_(d)["variacion_pasivo"]["cita"] = "accounts payable, accrued liabilities, operating lease liabilities and other current and non-current liabilities"
    return d


rnk = ev_(L7, d_nike(), wc=WC_NIKE, conceptos=C_NIKE)
paso("B · caso Nike (líneas mezcladas y partidas en dos renglones; el renglón de las cifras del pasivo no nombra el arrendamiento): las dos líneas se reconocen por su "
     "etiqueta entera en la página → contrastadas; valor de la hoja 68 y −1 contando los pagos", bloquean(rnk) == [] and cerca(F0(rnk), 68)
     and estado_tramo(rnk, "amortizacion_rou") == "contrastada" and estado_tramo(rnk, "variacion_pasivo") == "contrastada"
     and cerca(rnk["us_gaap"]["D_US2_bis"]["contando_los_pagos"]["variacion_maxima_del_flujo_sin_crecimiento_mm"], -1.0), f"{bloquean(rnk)} · {g(rnk, 'F1-US-FILAS')[0]['detalle'][:200]}")
rnk2 = ev_(L7, d_nike(), wc=WC_NIKE, conceptos=C_NIKE, texto=False)
paso("B · caso Nike sin texto/ de la fase 1: la línea del pasivo se reconoce porque la cita, en la página citada, es la etiqueta entera de un renglón sumado (y la misma "
     "etiqueta está en los demás años)", bloquean(rnk2) == [] and estado_tramo(rnk2, "variacion_pasivo") == "contrastada", f"{bloquean(rnk2)} · {g(rnk2, 'F1-US-FILAS')[0]['detalle'][:200]}")
# camino (iii) de la revisión: solo la variación del pasivo está en la fila 14 (10 al año: la hoja daría 78 frente a 68) y se declaran «los dos dentro» con pagos = coste
L78 = libro(dwc=10.0)
d3a = decl("A0_total", ub_am="fila_14", ub_pas="fila_14")
OP_(d3a)["amortizacion_rou"]["cita"] = L_PAS                    # cita real: la línea del pasivo, que sí está en la fila 14
r3a = ev_(L78, d3a, verdad=("no", "fila_14"))
paso("R3 (iii) · «los dos en la fila 14» falsa, citando para la amortización la línea del pasivo → F1-US-FILAS INCOMPLETO: cada tramo se prueba con su línea; no utilizable",
     bloquea(r3a, "F1-US-FILAS") and "no la amortización" in g(r3a, "F1-US-FILAS")[0]["detalle"] and not r3a["utilizable_para_conclusion"], g(r3a, "F1-US-FILAS")[0]["detalle"][:200])
d3b = decl("A0_total", ub_am="fila_14", ub_pas="fila_14")
OP_(d3b)["amortizacion_rou"].update({"cita": "Operating lease right-of-use assets, net", "pagina": 1})   # cita real: la línea del balance, en las notas
r3b_ = ev_(L78, d3b, verdad=("no", "fila_14"), notas=("Operating lease right-of-use assets, net",))
paso("R3 (iii) · …o citando la línea del activo del balance (real, pero no está entre las sumadas en la fila 14) → no se puede comprobar la línea del activo: INCOMPLETO",
     bloquean(r3b_) == ["F1-US-FILAS"] and g(r3b_, "F1-US-FILAS")[0]["efecto"] == "INCOMPLETO" and "D-US2 bis" in g(r3b_, "F1-US-FILAS")[0]["detalle"]
     and estado_tramo(r3b_, "variacion_pasivo") == "contrastada", g(r3b_, "F1-US-FILAS")[0]["detalle"][:220])
d3c = decl("A0_total", ub_am="fila_14", ub_pas="fila_14")
OP_(d3c)["amortizacion_rou"]["cita"] = L_AM                     # cita real: la línea propia de la amortización, que la fase 1 NO sumó
r3c_ = ev_(L78, d3c, verdad=("fuera", "fila_14"))
paso("R3 (iii) · …o citando la línea propia de la amortización, que está en el estado de flujos y la fase 1 no sumó → DATOS INVÁLIDOS (la declaración contradice al expediente)",
     bloquea(r3c_, "F1-US-FILAS") and g(r3c_, "F1-US-FILAS")[0]["efecto"] == "DATOS INVÁLIDOS" and estado_tramo(r3c_, "amortizacion_rou") == "contradicha",
     g(r3c_, "F1-US-FILAS")[0]["detalle"][:220])

# ================================================================== D · D-US2 (se cuentan los pagos) con los tramos fuera de las filas
L7d = libro(C70=69.0)
r7d = ev_(L7d, decl("A0_total", P=11, Lc=12))
paso("D · tramos fuera de las filas con pagos 11 ≠ coste 12: se cuentan los pagos sin ajuste (69 = FCF base); utilizable; la diferencia (+1) a la vista, sin bloquear",
     cerca(F0(r7d), 69) and r7d["utilizable_para_conclusion"] and "+1.000" in g(r7d, "F1-US-BASE")[0]["detalle"]
     and g(r7d, "F1-US-BASE")[0]["severidad"] == "INFORMA" and r7d["us_gaap"]["base_del_arrendamiento_operativo"] == "pagos (D-US2)", g(r7d, "F1-US-BASE")[0]["detalle"][:160])

# ================================================================== H · hipótesis general declarada D-US1 (tramos que la empresa no publica)
rh = ev_(L1, decl("A0_total", ub_am="no_publicada", ub_pas="no_publicada"))
paso("H · D-US1: los dos tramos «no_publicada» → se suponen fuera de las filas 8 y 14; no bloquea: utilizable para una conclusión CONDICIONADA",
     rh["utilizable_para_conclusion"] and "CONDICIONADA" in rh["rotulo"] and rh["condicionada"]["hipotesis"] == "D-US1" and cerca(F0(rh), 68), rh["rotulo"][:140])
paso("H · la regla lleva su registro (18-nov-2026, persona responsable, DECISIONES_PARA_EL_USUARIO.md) y es una hipótesis, no un dato",
     rh["condicionada"]["registro"]["fecha"] == "2026-11-18" and "DECISIONES_PARA_EL_USUARIO.md" in rh["condicionada"]["registro"]["motivo"]
     and "no es un dato" in rh["condicionada"]["texto"] and rh["us_gaap"]["operativos"]["hipotesis_D_US1_en"] == ["amortizacion_rou", "variacion_pasivo"])
gh = g(rh, "F1-US-HIPOTESIS")[0]
ch = rh["condicionada"]["cota"]
k_pas = next(k for k in ch if k.startswith("si la variación del pasivo"))
k_am = next(k for k in ch if k.startswith("si la amortización"))
paso("H · F1-US-HIPOTESIS avisa (no bloquea) con la cota: si la variación del pasivo estuviera sola en la fila 14, el flujo bajaría como máximo en los pagos "
     "(−12; −17,6 %); si la amortización estuviera en la fila 8, subiría como máximo en el coste lineal (+12)",
     gh["salta"] and gh["severidad"] == "AVISO" and cerca(ch[k_pas]["variacion_maxima_del_flujo_sin_crecimiento_mm"], -12)
     and cerca(ch[k_am]["variacion_maxima_del_flujo_sin_crecimiento_mm"], 12) and cerca(ch[k_pas]["variacion_maxima_del_flujo_sin_crecimiento_%"], -17.647, 1e-3), gh["detalle"][:200])
vp = ch[k_pas]["por_escenario (valor presente de los flujos a la r del libro, sin exceso de caja ni quiebra)"]
# réplica independiente de la cota en valor presente (NORMAL): Δf = pagos ÷ ventas medias; ΔVP = −Δf·[Σ V_t/(1+r)^t + V_10(1+g)/((r−g)(1+r)^10)]
Vt, v = [], 1000.0
for t in range(1, 11):
    v *= 1 + (0.03 if t <= 5 else 0.03 - (0.03 - 0.02) * (t - 5) / 5)
    Vt.append(v)
kk = sum(Vt[t] / 1.09 ** (t + 1) for t in range(10)) + Vt[-1] * 1.02 / ((0.09 - 0.02) * 1.09 ** 10)
paso("H · la cota también en valor presente de los flujos, por escenario (NORMAL: −0,012 × Σ ventas descontadas; réplica independiente)",
     set(vp) == {"MALO", "NORMAL", "BUENO"} and cerca(vp["NORMAL"]["variacion_maxima_del_valor_presente_de_los_flujos_mm"], -0.012 * kk, 1e-3)
     and vp["NORMAL"]["variacion_maxima_%"] < 0, f"{vp['NORMAL']} · réplica {-0.012 * kk:.3f}")
rs_ = ch["resumen"]
paso("H · (R1-8) la cota resumida en dos cifras para el informe: % del flujo sin crecimiento (−17,6 % y +17,6 %) y % del valor presente en el escenario NORMAL; va en el rótulo",
     cerca(rs_["flujo_sin_crecimiento_%"][0], -17.647, 1e-3) and cerca(rs_["flujo_sin_crecimiento_%"][1], 17.647, 1e-3)
     and cerca(rs_["valor_presente_NORMAL_%"][0], vp["NORMAL"]["variacion_maxima_%"], 1e-9) and rs_["valor_presente_NORMAL_%"][1] > 0
     and "−" not in rs_["texto"] and "-17.6 %" in rs_["texto"] and "escenario NORMAL" in rs_["texto"] and rs_["texto"] in rh["rotulo"], rs_["texto"])
cb7 = M._resumen_cota({"a": {"variacion_maxima_del_flujo_sin_crecimiento_mm": -10.0, "variacion_maxima_del_flujo_sin_crecimiento_%": -14.7},
                       "b": {"variacion_maxima_del_flujo_sin_crecimiento_mm": -12.0, "variacion_maxima_del_flujo_sin_crecimiento_%": -17.6},
                       "c": {"variacion_maxima_del_flujo_sin_crecimiento_mm": 3.0, "variacion_maxima_del_flujo_sin_crecimiento_%": 4.4}})
paso("H · el resumen suma las variaciones del mismo signo (dos ubicaciones falsas a la vez se acumulan: −10 y −12 → −22) y no compensa las de signo contrario",
     cb7["flujo_sin_crecimiento_mm"] == [-22.0, 3.0] and cerca(cb7["flujo_sin_crecimiento_%"][0], -32.3) and cb7["valor_presente_NORMAL_%"] is None)
paso("H · F1-SERIES comprueba que la página citada es la del estado de flujos y no muestra una línea propia del arrendamiento operativo (2 páginas examinadas)",
     not salta(rh, "F1-SERIES") and rh["F1_SERIES"]["paginas_sin_linea_propia_del_arrendamiento_operativo"] == 2)
rh3 = ev_(L1, decl("A0_total", ub_am="no_publicada", ub_pas="no_publicada"), verdad=("fuera", "fuera"))
paso("H · donde la empresa publica la línea manda el dato: «no_publicada» y la página del estado de flujos muestra «Non-cash lease expense» → F1-SERIES DATOS INVÁLIDOS",
     bloquea(rh3, "F1-SERIES") and g(rh3, "F1-SERIES")[0]["efecto"] == "DATOS INVÁLIDOS" and "manda el dato" in g(rh3, "F1-SERIES")[0]["detalle"]
     and not rh3["utilizable_para_conclusion"], g(rh3, "F1-SERIES")[0]["detalle"][:160])
rh9 = ev_(L1, decl("A0_total", ub_am="no_publicada", ub_pas="no_publicada", pagina_np=9))
paso("H · «no_publicada» citando una página que no existe → F1-SERIES DATOS INVÁLIDOS", bloquea(rh9, "F1-SERIES") and g(rh9, "F1-SERIES")[0]["efecto"] == "DATOS INVÁLIDOS")
rh1p = ev_(L1, decl("A0_total", ub_am="no_publicada", ub_pas="no_publicada", pagina_np=1))
paso("H · «no_publicada» citando una página que no es la del estado de flujos (las notas, sin líneas de arrendamiento) → F1-SERIES INCOMPLETO: se examina el estado de flujos",
     bloquea(rh1p, "F1-SERIES") and g(rh1p, "F1-SERIES")[0]["efecto"] == "INCOMPLETO" and "no es la del estado de flujos" in g(rh1p, "F1-SERIES")[0]["detalle"],
     g(rh1p, "F1-SERIES")[0]["detalle"][:200])
dhs = decl("A0_total", ub_am="no_publicada", ub_pas="no_publicada")
del OP_(dhs)["variacion_pasivo"]["pagina"]
paso("H · «no_publicada» sin la página del estado de flujos examinada → F1-US-DESGLOSE INCOMPLETO", bloquea(ev_(L1, dhs), "F1-US-DESGLOSE"))
rh1 = ev_(L6, decl("A0_total", ub_am="no_publicada", ub_pas="fila_14", ajuste=10, pagina_np=2))
paso("H · un tramo publicado y otro no: el publicado se trata con su dato (pasivo en la fila 14: se retira; 68) y la hipótesis vale solo para el otro (cota solo al alza)",
     cerca(F0(rh1), 68) and rh1["condicionada"]["tramos"] == ["amortizacion_rou"] and not any(k.startswith("si la variación del pasivo") for k in rh1["condicionada"]["cota"])
     and any(k.startswith("si la amortización") for k in rh1["condicionada"]["cota"]) and estado_tramo(rh1, "variacion_pasivo") == "contrastada", str(bloquean(rh1)))
paso("H · sin hipótesis (tramos contrastados con su línea) F1-US-HIPOTESIS no salta y el rótulo no dice «condicionada»", not salta(r1, "F1-US-HIPOTESIS")
     and "condicionada" not in r1["rotulo"].lower())
paso("H · (R1-15) con la hipótesis, K3b dice «una vez» «según la hipótesis D-US1» y K3 no se presenta como conforme (no es una comprobación independiente)",
     rh["K3"]["K3b_alquiler_contado"] == "una vez" and rh["K3"]["K3b_contrastado"] is False and "hipótesis D-US1" in rh["K3"]["K3b_fundamento"]
     and rh["K3"]["conforme"] is None and "no es una comprobación independiente" in rh["K3"]["conforme_nota"], str(rh["K3"].get("conforme_nota")))

# ================================================================== P · puente de deuda (motor B) y motor A
LP = libro(fila22=100.0, fila23=50.0)
rp = ev_(LP, decl("A0_total", pasivo=50))
gp = g(rp, "F1-US-PUENTE")[0]
pu = rp["us_gaap"]["puente_de_deuda"]
paso("P · motor A con 50 de pasivo operativo en la fila 23: F1-US-PUENTE informa (el motor A no resta deuda) y no bloquea; deuda coherente de un puente = 100",
     gp["salta"] and gp["severidad"] == "INFORMA" and rp["utilizable_para_conclusion"] and cerca(pu["deuda_del_puente_coherente"], 100)
     and cerca(pu["deuda_del_puente_del_libro_C64"], 150), gp["detalle"][:130])
LB = libro(fila22=100.0, fila23=50.0, motor="B")
rb = ev_(LB, decl("A0_total", pasivo=50))
paso("P · motor B con US GAAP: F1 evalúa solo el puente; el pasivo operativo dentro de la fila 23 se restaría además del EBIT → F1-US-PUENTE BLOQUEA (límite declarado)",
     rb["aplica"] is True and "puente" in rb["alcance"] and bloquean(rb) == ["F1-US-PUENTE"] and rb["estado_propuesto"] == "no_entregable · limite_del_modelo"
     and "motor B" in rb["rotulo"] and "dos veces" in rb["K3"]["K3b_alquiler_contado"], rb["rotulo"][:120])
rb0 = ev_(libro(fila22=100.0, fila23=0.0, motor="B"), decl("A0_total", pasivo=0))
paso("P · motor B con la fila 23 sin pasivo operativo (0 declarado): utilizable; alquiler una vez", rb0["utilizable_para_conclusion"] and rb0["K3"]["K3b_alquiler_contado"] == "una vez"
     and "motor B utilizable" in rb0["rotulo"], str(bloquean(rb0)))
rbf = ev_(libro(fila22=100.0, fila23=30.0, motor="B"), decl("A0_total", fin=True, rou_fin=5, fin_princ=5, pasivo=0))
paso("P · motor B con 30 de pasivo por arrendamientos FINANCIEROS en la fila 23 y 0 operativo: no bloquea (los financieros sí son deuda del puente: 130)",
     rbf["utilizable_para_conclusion"] and cerca(rbf["us_gaap"]["puente_de_deuda"]["deuda_del_puente_coherente"], 130))
rbs = ev_(LB, decl("A0_total", us=False))
paso("P · motor B con US GAAP y sin declaración de arrendamientos → F1-US-DESGLOSE (pendiente_de_datos): nunca un puente silencioso",
     bloquea(rbs, "F1-US-DESGLOSE") and rbs["estado_propuesto"] == "pendiente_de_datos")
rbu = ev_(LB, decl("A0_total", ub_am=None, ub_pas=None, pasivo=50))
paso("P · motor B: no exige las ubicaciones de los tramos en el flujo (son del motor A); con el pasivo declarado, lo que bloquea es el puente",
     bloquean(rbu) == ["F1-US-PUENTE"], str(bloquean(rbu)))
rbx = ev_(LB, decl("A0_total", pasivo=60))
paso("P · pasivo operativo declarado (60) mayor que la fila 23 (50) → DATOS INVÁLIDOS", bloquea(rbx, "F1-US-PUENTE") and g(rbx, "F1-US-PUENTE")[0]["efecto"] == "DATOS INVÁLIDOS")
rbn = M.evaluar(libro(l4="IFRS", motor="B"), dN)
paso("P · motor B con NIIF: F1 sigue sin aplicar (T11 no cambia)", rbn["aplica"] is False and not rbn["bloquea"] and rbn["guardas"] == [])
rbm = ev_(libro(l4="US GAAP", motor="B"), dN)
paso("P · motor B, libro US GAAP y declaración NIIF → se evalúa (por el libro) y F1-NORMA bloquea por mezcla de normas", rbm["aplica"] is True and bloquea(rbm, "F1-NORMA"))
# (ronda 2) contraste del puente con las líneas que la fase 1 sumó en la fila 23 y lo que F1 no mira con el motor B (R1-9)
d_no = decl("A0_total", op=False, P=None, Lc=None, pasivo=None)
rg3 = ev_(LB, d_no, fila23=("Operating lease liabilities, non-current",))
paso("P · motor B, «operativos.existen = false» (falso) y la fase 1 sumó en la fila 23 una línea de pasivo por arrendamiento operativo → F1-US-PUENTE DATOS INVÁLIDOS",
     bloquea(rg3, "F1-US-PUENTE") and g(rg3, "F1-US-PUENTE")[0]["efecto"] == "DATOS INVÁLIDOS" and "contradice" in g(rg3, "F1-US-PUENTE")[0]["detalle"]
     and rg3["estado_propuesto"] == "pendiente_de_datos", g(rg3, "F1-US-PUENTE")[0]["detalle"][:200])
rg3b = ev_(LB, copy.deepcopy(d_no), partes=False)
paso("P · motor B, sin arrendamientos de ninguna clase declarados y 50 de pasivo por arrendamientos en la fila 23 → DATOS INVÁLIDOS (también sin fase1_partes)",
     bloquea(rg3b, "F1-US-PUENTE") and g(rg3b, "F1-US-PUENTE")[0]["efecto"] == "DATOS INVÁLIDOS", g(rg3b, "F1-US-PUENTE")[0]["detalle"][:160])
rpa = ev_(LP, decl("A0_total", pasivo=0), fila23=("Operating lease liabilities, non-current",))
paso("P · motor A, pasivo operativo declarado 0 y una línea de la fila 23 que lo nombra: avisa (el motor A no resta deuda) y no bloquea",
     g(rpa, "F1-US-PUENTE")[0]["severidad"] == "AVISO" and rpa["utilizable_para_conclusion"]
     and len(rpa["us_gaap"]["puente_de_deuda"]["lineas_de_arrendamiento_operativo_sumadas_en_la_fila_23"]) == 1)
ga = g(rb0, "F1-US-ANCLA")
paso("R9 · motor B con arrendamientos operativos: F1-US-ANCLA AVISA de lo que F1 no mira (el ancla de S2C, Historia C53, y el ROIC pueden arrastrar partidas del "
     "arrendamiento operativo); no bloquea", len(ga) == 1 and ga[0]["severidad"] == "AVISO" and "Historia C53" in ga[0]["detalle"] and "ROIC" in ga[0]["detalle"]
     and rb0["utilizable_para_conclusion"], ga[0]["detalle"][:200] if ga else "")
V13b = [1000 * 1.05 ** i for i in range(10)]
dao_b = [0.02 * v for v in V13b]
cap_b = [dao_b[i] + 0.5 * (V13b[i] - (V13b[i - 1] if i else V13b[0] / 1.05)) for i in range(10)]
Lg4 = libro(ventas=V13b, ebit=[0.10 * v for v in V13b], da=[dao_b[i] + 0.025 * V13b[i] for i in range(10)], tau=0.25, capex=cap_b, C70=50.0, motor="B", fila23=0.0)
rg4 = ev_(Lg4, decl("A0_total", pasivo=0), da=[DA_ROU])
paso("R9 · con la amortización operativa (2,5 % de las ventas) dentro de la D&A el ancla de S2C del libro queda vacía: el aviso lo dice y nombra la línea sumada en la fila 8",
     Lg4["Historia!C53"] == "" and "vacía" in g(rg4, "F1-US-ANCLA")[0]["detalle"] and "fila 8" in g(rg4, "F1-US-ANCLA")[0]["detalle"]
     and "right-of-use" in g(rg4, "F1-US-ANCLA")[0]["detalle"], g(rg4, "F1-US-ANCLA")[0]["detalle"][-230:])
paso("R9 · sin arrendamientos operativos declarados (y sin líneas que los nombren) no hay aviso del ancla", not g(ev_(libro(motor="B"), copy.deepcopy(d_no)), "F1-US-ANCLA"))

# ================================================================== S · fuentes de las series y citas de US GAAP (F1-SERIES)
dS = decl("A0_total")
dS["series"]["pagos_arr_operativo"]["2025"].update({"valor_fuente": -12, "signo": -1, "tratamiento": "publicado entre paréntesis"})   # literal «12» y valor −12
rS = ev_(L1, dS)
paso("S · serie de US GAAP con «valor_fuente» distinto de la cifra publicada con su signo → F1-SERIES DATOS INVÁLIDOS (R415-SIGNO)",
     bloquea(rS, "F1-SERIES") and g(rS, "F1-SERIES")[0]["efecto"] == "DATOS INVÁLIDOS" and "pagos_arr_operativo.2025" in g(rS, "F1-SERIES")[0]["detalle"])
dS2 = decl("A0_total")
cS = expediente(dS2)
TMP.append(cS)
OP_(dS2)["amortizacion_rou"]["cita"] = "Amortization of operating lease right-of-use assets"
rS2 = M.evaluar(L1, dS2, carpeta=cS)
paso("S · cita de una clasificación que no está en la página citada → F1-SERIES DATOS INVÁLIDOS", bloquea(rS2, "F1-SERIES") and "la cita no está" in g(rS2, "F1-SERIES")[0]["detalle"]
     and estado_tramo(rS2, "amortizacion_rou") == "sin_evidencia")
dS3 = decl("A0_total")
dS3["arrendamientos_us_gaap"]["financieros"]["cita"] = "no"
rS3 = ev_(L1, dS3)
paso("S · cita de menos de diez caracteres → F1-SERIES INCOMPLETO (no identifica una línea)", bloquea(rS3, "F1-SERIES") and g(rS3, "F1-SERIES")[0]["efecto"] == "INCOMPLETO")
rS4 = M.evaluar(L1, decl("A0_total"))
paso("S · sin la carpeta del expediente (fuentes no examinadas) → F1-SERIES bloquea (INCOMPLETO): un «utilizable» exige las fuentes", bloquea(rS4, "F1-SERIES")
     and rS4["estado_propuesto"] == "pendiente_de_datos")
dS5 = decl("A0_total", ub_pas="fila_14", ajuste=10)
dS5["series"]["circulante_arr_operativo"]["2024"].update({"valor_fuente": 10, "signo": 1, "tratamiento": "ninguno", "literal": "10"})
uS5 = M.leer_us(dS5, ANIOS)
paso("S · la partida del circulante lleva el signo de la fila 14: «(10)» publicado con signo −1 es +10 (consume caja) y admite importes negativos",
     uS5["ajuste"][2025] == Fr(10) and M.leer_serie({"series": {"circulante_arr_operativo": serie(-3)}}, "circulante_arr_operativo", ANIOS, con_signo=True)[0][2025] == Fr(-3)
     and M.leer_serie({"series": {"da_rou_operativo": serie(-3)}}, "da_rou_operativo", ANIOS)[0] == {})
dS6 = decl("A0_total")
cS6 = expediente(dS6)
TMP.append(cS6)
open(os.path.join(cS6, FUENTE), "a", encoding="utf-8").write("texto añadido después de declarar la huella\n")
rS6 = M.evaluar(L1, dS6, carpeta=cS6)
paso("S · si la fuente cambia después de declarar su huella, las citas de las ubicaciones no se dan por examinadas → F1-SERIES DATOS INVÁLIDOS",
     bloquea(rS6, "F1-SERIES") and g(rS6, "F1-SERIES")[0]["efecto"] == "DATOS INVÁLIDOS" and "sha256 distinto" in g(rS6, "F1-SERIES")[0]["detalle"])

# ================================================================== F · contraste de las ubicaciones con las líneas que la fase 1 sumó en las filas 8 y 14 (R1-3)
rF0 = ev_(L1, decl("A0_total"), partes=False)
cF0 = cotas(rF0)
paso("F · sin fase1_partes las ubicaciones declaradas no se pueden contrastar con una línea: F1-US-FILAS AVISA y la conclusión queda CONDICIONADA (antes: utilizable a secas)",
     rF0["utilizable_para_conclusion"] and bloquean(rF0) == [] and g(rF0, "F1-US-FILAS")[0]["severidad"] == "AVISO" and "CONDICIONADA" in rF0["rotulo"]
     and rF0["condicionada"]["hipotesis"] == "F1-US-FILAS" and estado_tramo(rF0, "variacion_pasivo") == "sin_contrastar", rF0["rotulo"][:200])
paso("F · …con la misma cota que la hipótesis D-US1: −12 si la variación del pasivo estuviera en la fila 14 y +12 si la amortización estuviera en la fila 8; "
     "no es una decisión de la persona (sin registro) y K3 no se presenta como conforme", sorted(round(v, 6) for v in cF0.values()) == [-12.0, 12.0]
     and all("sin contrastar con una línea" in k for k in cF0) and rF0["condicionada"]["registro"] is None and rF0["K3"]["conforme"] is None
     and "según lo declarado" in rF0["K3"]["K3b_fundamento"], str(cF0))
dF = decl("A0_total", ub_am="no_publicada", ub_pas="no_publicada")
rF2 = ev_(L1, dF, verdad=("no", "fila_14"))
paso("F · «no_publicada» cuando la fase 1 sumó «Operating lease liabilities» en la fila 14: F1-US-FILAS bloquea (DATOS INVÁLIDOS: manda el dato); no utilizable",
     bloquea(rF2, "F1-US-FILAS") and g(rF2, "F1-US-FILAS")[0]["efecto"] == "DATOS INVÁLIDOS" and "manda el dato" in g(rF2, "F1-US-FILAS")[0]["detalle"]
     and not rF2["utilizable_para_conclusion"] and estado_tramo(rF2, "variacion_pasivo") == "contradicha", g(rF2, "F1-US-FILAS")[0]["detalle"][:170])
rF3 = ev_(L1, decl("A0_total"), wc=WC + ("Prepaid expenses, ROU assets and other assets",))
paso("F · tramos declarados «fuera de las filas» con su línea, pero la fila 14 suma «Prepaid expenses, ROU assets and other assets» → F1-US-FILAS bloquea (la amortización)",
     bloquea(rF3, "F1-US-FILAS") and estado_tramo(rF3, "amortizacion_rou") == "contradicha" and estado_tramo(rF3, "variacion_pasivo") == "contrastada")
rF4 = ev_(L1, decl("A0_total"), da=[DA_ROU])
paso("F · la fila 8 suma una línea que nombra el derecho de uso y la amortización no está declarada dentro de la fila 8 → F1-US-FILAS bloquea", bloquea(rF4, "F1-US-FILAS")
     and "fila 8" in g(rF4, "F1-US-FILAS")[0]["detalle"])
paso("F · con la línea declarada dentro de la fila 14 (y su importe) no hay contradicción: F1-US-FILAS no salta", not salta(r6, "F1-US-FILAS") and bloquean(r6) == ["F1-LIBRO"])
paso("F · con NIIF no existe (nada cambia)", not g(rN, "F1-US-FILAS"))


def solo_anterior_2025(a, j):
    """La línea del pasivo solo está en el lado «anterior» de AR_2025 (el que da el valor de 2024)."""
    for lado in ("actual", "anterior"):
        if not (a == 2025 and lado == "anterior"):
            j["partidas"]["circulante_lineas"][lado] = [c for c in j["partidas"]["circulante_lineas"][lado] if "lease" not in c["concepto"].lower()]
    return j


rF6 = ev_(L6, decl("A0_total"), verdad=("fuera", "fila_14"), por_anio=solo_anterior_2025)
paso("F · (revisión B4) la línea solo en el lado «anterior» del informe siguiente, que es el que da el valor de la Historia: se ve → DATOS INVÁLIDOS",
     bloquea(rF6, "F1-US-FILAS") and g(rF6, "F1-US-FILAS")[0]["efecto"] == "DATOS INVÁLIDOS" and "anterior" in g(rF6, "F1-US-FILAS")[0]["detalle"], g(rF6, "F1-US-FILAS")[0]["detalle"][:200])
dP = decl("A0_total")
cP = expediente(dP, verdad=("fuera", "fila_14"), por_anio=solo_anterior_2025)
TMP.append(cP)
uP = M._partes_fase1(cP, list(range(2021, 2026)))
paso("F · las líneas de cada año se toman como las toma la fase 1 (fase1_historia): el lado «anterior» del informe siguiente y, en el último año, el lado «actual»; "
     "la línea que solo está en el «anterior» de AR_2025 es la de 2024", [any("pasivo" in c["lados"] for c in uP["usados"][a]["circulante_lineas"]) for a in range(2021, 2026)]
     == [False, False, False, True, False] and uP["usados"][2024]["circulante_lineas"][0]["origen"].startswith("AR_2025.json") and "anterior" in uP["usados"][2024]["circulante_lineas"][0]["origen"]
     and "actual" in uP["usados"][2025]["circulante_lineas"][0]["origen"] and not [k for k in uP["sin_examinar"] if k[1] != "arrendamientos"], str({a: uP["usados"][a]["circulante_lineas"][0]["origen"] for a in (2024, 2025)}))
rF7 = ev_(L6, decl("A0_total"), verdad=("fuera", "fila_14"), por_anio=lambda a, j: dict(j, anio=str(a)))
paso("F · (revisión B5) el «anio» de fase1_partes escrito como texto («2025») se lee igual → DATOS INVÁLIDOS", bloquea(rF7, "F1-US-FILAS")
     and g(rF7, "F1-US-FILAS")[0]["efecto"] == "DATOS INVÁLIDOS")
rF8 = ev_(L1, decl("A0_total"), anios_partes=range(2024, 2026))
paso("F · (revisión, punto 5) si faltan informes de años que usa el modelo (2021 y 2022), no dice «no contradicen»: quedan sin examinar → sin contrastar → CONDICIONADA",
     rF8["utilizable_para_conclusion"] and "CONDICIONADA" in rF8["rotulo"] and estado_tramo(rF8, "variacion_pasivo") == "sin_contrastar"
     and "2021" in rF8["us_gaap"]["contraste_de_ubicaciones"]["sin_contrastar"]["variacion_pasivo"], str(rF8["us_gaap"]["contraste_de_ubicaciones"]["sin_contrastar"])[:200])
dF9 = decl("A0_total")
cF9 = expediente(dF9)
TMP.append(cF9)
json.dump({"circulante_lineas": {"2024": {"valor_mm": 3.0, "fuente": "a mano", "fecha": "2026-11-18", "confirmado_por": "persona"}}}, open(os.path.join(cF9, "fase1_decisiones.json"), "w"))
rF9 = M.evaluar(L1, dF9, carpeta=cF9)
paso("F · un año con la fila 14 fijada a mano (fase1_decisiones.json) no es la suma de las líneas: queda sin examinar → sin contrastar → CONDICIONADA",
     "CONDICIONADA" in rF9["rotulo"] and estado_tramo(rF9, "variacion_pasivo") == "sin_contrastar" and "2024" in str(rF9["us_gaap"]["contraste_de_ubicaciones"]["fase1_partes"]["sin_examinar"]))
rF10 = ev_(L1, decl("A0_total"), texto=False)
paso("F · sin texto/ de la fase 1 las etiquetas partidas no se pueden reconstruir en los informes de los demás años: «fuera» no queda contrastada → CONDICIONADA",
     "CONDICIONADA" in rF10["rotulo"] and estado_tramo(rF10, "variacion_pasivo") == "sin_contrastar" and bloquean(rF10) == [], rF10["rotulo"][:160])
rF11 = ev_(L1, decl("A0_total"), anios_partes=range(2016, 2019))
paso("F · si la página citada es la del estado de flujos de un informe que no es de los años que usa el modelo, «fuera» no queda contrastada → CONDICIONADA",
     "CONDICIONADA" in rF11["rotulo"] and "años que usa el modelo" in rF11["us_gaap"]["contraste_de_ubicaciones"]["sin_contrastar"]["variacion_pasivo"])
# etiqueta partida en dos renglones con mayúsculas de título (el segundo renglón no empieza en minúscula): la línea sumada se reconoce igual
T_PAS = ("Increase (Decrease) in Accounts Payable, Accrued Liabilities, Operating Lease", "Liabilities and Other Liabilities")
dF12 = decl("A0_total")
OP_(dF12)["variacion_pasivo"]["cita"] = "Accrued Liabilities, Operating Lease Liabilities and Other Liabilities"
rF12 = ev_(L6, dF12, verdad=("fuera", "no"), wc=("Accounts Receivable", T_PAS), conceptos={T_PAS: "Accounts payable and other liabilities"})
paso("F · etiqueta partida con mayúsculas de título: la línea citada como «fuera» es una de las sumadas en la fila 14 → DATOS INVÁLIDOS (también sin texto/ de la fase 1)",
     bloquea(rF12, "F1-US-FILAS") and g(rF12, "F1-US-FILAS")[0]["efecto"] == "DATOS INVÁLIDOS"
     and bloquea(ev_(L6, copy.deepcopy(dF12), verdad=("fuera", "no"), wc=("Accounts Receivable", T_PAS), conceptos={T_PAS: "Accounts payable and other liabilities"}, texto=False), "F1-US-FILAS"),
     g(rF12, "F1-US-FILAS")[0]["detalle"][:200])
# etiqueta partida con renglones en blanco entre sus dos partes (texto a doble espacio): la línea citada se reconoce por los renglones de la página en que está la cita
B_PAS = ("Increase in accrued liabilities, operating lease", "", "", "liabilities and other")
dF14 = decl("A0_total")
OP_(dF14)["variacion_pasivo"]["cita"] = "accrued liabilities, operating lease liabilities and other"
rF14 = ev_(L6, dF14, verdad=("fuera", "no"), wc=("Accounts receivable", B_PAS), conceptos={B_PAS: "Accrued liabilities and other"})
paso("F · etiqueta partida con renglones en blanco en medio: la línea citada como «fuera» es una de las sumadas en la fila 14 → DATOS INVÁLIDOS",
     bloquea(rF14, "F1-US-FILAS") and g(rF14, "F1-US-FILAS")[0]["efecto"] == "DATOS INVÁLIDOS" and estado_tramo(rF14, "variacion_pasivo") == "contradicha",
     g(rF14, "F1-US-FILAS")[0]["detalle"][:200])
rF13 = ev_(L1, decl("A0_total"), por_anio=lambda a, j: {"anio": a, "archivo": TXT, "partidas": {}})
paso("F · una carpeta fase1_partes sin ninguna línea de explotación no permite contrastar nada: como si no la hubiera → sin contrastar → CONDICIONADA (no «sin contradicción»)",
     rF13["utilizable_para_conclusion"] and "CONDICIONADA" in rF13["rotulo"] and estado_tramo(rF13, "amortizacion_rou") == "sin_contrastar"
     and "sin fase1_partes" in rF13["us_gaap"]["contraste_de_ubicaciones"]["sin_contrastar"]["amortizacion_rou"])
paso("F · el resultado deja la huella de las líneas de la fase 1 con que se contrastó (fase1_partes) y, sin ellas, None", isinstance(r1["fase1_partes_sha256"], str)
     and len(r1["fase1_partes_sha256"]) == 64 and rF0["fase1_partes_sha256"] is None and r1["us_gaap"]["contraste_de_ubicaciones"]["fase1_partes"]["informes"] == list(range(2021, 2026)))

# ================================================================== R3 · los tres caminos de la revisión R1: ubicación FALSA con cita REAL (caja correcta 68)
# (i) «fuera» falsa: la variación del pasivo (10 al año) está de verdad dentro de la fila 14 (libro L6: la hoja da 78) y se declara «fuera de las filas» citando su línea
rB1 = ev_(L6, decl("A0_total"), verdad=("fuera", "fila_14"), partes=False)
paso("R3 (i) · «fuera» falsa sin fase1_partes (revisión B1): ya no es utilizable a secas: CONDICIONADA, con la cota a la vista (−12) que cubre el error (+10: 78 frente a 68)",
     rB1["utilizable_para_conclusion"] and cerca(F0(rB1), 78) and "CONDICIONADA" in rB1["rotulo"] and min(cotas(rB1).values()) <= -10 and "-12.000" in rB1["rotulo"],
     rB1["rotulo"][:260])
rB1v = ev_(libro_v631(libro(dwc=10.0, palancas=False), "A2_propio", 0.0), decl("A2_propio"), verdad=("fuera", "fila_14"), partes=False)
paso("R3 (i) · lo mismo en un libro V6.3.1 con A2 (revisión B1v): CONDICIONADA con su cota", rB1v["utilizable_para_conclusion"] and "CONDICIONADA" in rB1v["rotulo"]
     and cerca(F0(rB1v), 78) and min(cotas(rB1v).values()) <= -10)
rB6 = ev_(L6, decl("A0_total"), verdad=("fuera", "fila_14"))
paso("R3 (i) · con fase1_partes (revisión B6): la línea citada está entre las que la fase 1 sumó en la fila 14 → F1-US-FILAS DATOS INVÁLIDOS; no utilizable",
     bloquea(rB6, "F1-US-FILAS") and g(rB6, "F1-US-FILAS")[0]["efecto"] == "DATOS INVÁLIDOS" and "está entre las que la fase 1 sumó en la fila 14" in g(rB6, "F1-US-FILAS")[0]["detalle"]
     and rB6["estado_propuesto"] == "pendiente_de_datos", g(rB6, "F1-US-FILAS")[0]["detalle"][:200])
# (revisión B2) la línea de la fila 14 que lleva la variación del pasivo es «Accrued and other liabilities»: el estado de flujos no tiene línea propia del pasivo
WC_B2 = ("Accounts receivable", "Accrued and other liabilities")
rB2a = ev_(L6, decl("A0_total"), verdad=("fuera", "no"), wc=WC_B2)
paso("R3 (i) · (B2) sin línea propia en el estado de flujos, «fuera» no tiene qué citar: «Operating lease liabilities» solo está dentro de la línea de información "
     "complementaria (altas de derechos de uso) → F1-US-FILAS INCOMPLETO; no utilizable", bloquean(rB2a) == ["F1-US-FILAS"] and g(rB2a, "F1-US-FILAS")[0]["efecto"] == "INCOMPLETO"
     and "información complementaria" in g(rB2a, "F1-US-FILAS")[0]["detalle"] and not rB2a["utilizable_para_conclusion"], g(rB2a, "F1-US-FILAS")[0]["detalle"][:230])
dB2b = decl("A0_total")
OP_(dB2b)["variacion_pasivo"].update({"pagina": 3})   # cita real: la línea del balance (página 3)
rB2b = ev_(L6, dB2b, verdad=("fuera", "no"), wc=WC_B2, fila23=("Operating lease liabilities",))
paso("R3 (i) · (B2) citando la línea del balance (real): no es una línea del estado de flujos → F1-US-FILAS INCOMPLETO («fuera» se prueba con una línea del estado de flujos; "
     "si no la hay, «no_publicada»)", bloquean(rB2b) == ["F1-US-FILAS"] and g(rB2b, "F1-US-FILAS")[0]["efecto"] == "INCOMPLETO" and "no_publicada" in g(rB2b, "F1-US-FILAS")[0]["detalle"],
     g(rB2b, "F1-US-FILAS")[0]["detalle"][:220])
dB2c = decl("A0_total")
OP_(dB2c)["variacion_pasivo"]["cita"] = "Right-of-use assets obtained in exchange for new operating lease liabilities"   # cita real del estado de flujos: información complementaria
rB2c = ev_(L6, dB2c, verdad=("fuera", "no"), wc=WC_B2)
paso("R3 (i) · (B2) citando la línea de información complementaria del propio estado de flujos (altas de derechos de uso): no es una línea de la conciliación → INCOMPLETO",
     bloquean(rB2c) == ["F1-US-FILAS"] and "complementaria" in g(rB2c, "F1-US-FILAS")[0]["detalle"])
rB7 = ev_(L6, decl("A0_total", ub_pas="no_publicada"), verdad=("fuera", "no"), wc=WC_B2)
paso("R3 (i) · (B7) la declaración veraz de ese caso es «no_publicada»: hipótesis D-US1, CONDICIONADA, y la cota (−12) cubre el error (+10)",
     rB7["utilizable_para_conclusion"] and rB7["condicionada"]["hipotesis"] == "D-US1" and cerca(F0(rB7), 78) and min(cotas(rB7).values()) <= -10
     and estado_tramo(rB7, "amortizacion_rou") == "contrastada")
# (revisión B3) etiqueta real de Nike 2025: el concepto que escribió el agente no nombra el arrendamiento y la «linea» es el segundo renglón de la etiqueta
WC_B3 = ("Accounts receivable", "Inventories", NIKE_PAS)
C_B3 = {NIKE_PAS: "Accounts payable, accrued liabilities and other liabilities"}
dB3 = decl("A0_total")
OP_(dB3)["variacion_pasivo"]["cita"] = "accounts payable, accrued liabilities, operating lease liabilities and other current and non-current liabilities"
rB3 = ev_(L6, dB3, verdad=("fuera", "no"), wc=WC_B3, conceptos=C_B3)
paso("R3 (i) · (B3) con la etiqueta de Nike 2025 la línea sumada se reconoce por su etiqueta entera (el arrendamiento está en el primer renglón) → DATOS INVÁLIDOS",
     bloquea(rB3, "F1-US-FILAS") and g(rB3, "F1-US-FILAS")[0]["efecto"] == "DATOS INVÁLIDOS" and estado_tramo(rB3, "variacion_pasivo") == "contradicha",
     g(rB3, "F1-US-FILAS")[0]["detalle"][:260])
rB3n = ev_(L6, decl("A0_total", ub_pas="no_publicada"), verdad=("fuera", "no"), wc=WC_B3, conceptos=C_B3)
paso("R3 (i) · (B3) …y «no_publicada» tampoco pasa: la línea sumada nombra el pasivo por arrendamiento → manda el dato (F1-US-FILAS y F1-SERIES)",
     bloquea(rB3n, "F1-US-FILAS") and "manda el dato" in g(rB3n, "F1-US-FILAS")[0]["detalle"] and salta(rB3n, "F1-SERIES") and not rB3n["utilizable_para_conclusion"])
# (ii) «fila_8» falsa: la D&A (20) no lleva la amortización del derecho de uso operativo y se declara «fila_8» con da_rou_operativo = 10 (A2 la excluye de D_X: 78)
L1v = libro_v631(libro(palancas=False), "A2_propio", 10.0)
dC1 = decl("A2_propio", ub_am="fila_8", a8=10)
OP_(dC1)["amortizacion_rou"]["cita"] = DA                      # cita real y genérica: la línea de la D&A, que no nombra el arrendamiento
rC1 = ev_(L1v, dC1, verdad=("no", "fuera"))
paso("R3 (ii) · «fila_8» falsa con la cita genérica «Depreciation and amortization» (revisión C1): la cita no nombra el arrendamiento → F1-US-FILAS INCOMPLETO; no utilizable",
     bloquean(rC1) == ["F1-US-FILAS"] and g(rC1, "F1-US-FILAS")[0]["efecto"] == "INCOMPLETO" and "no nombra el arrendamiento" in g(rC1, "F1-US-FILAS")[0]["detalle"],
     g(rC1, "F1-US-FILAS")[0]["detalle"][:200])
NOTA_AM, NOTA_PAS = "Amortization of operating lease right-of-use assets was 10", "Operating lease liabilities were 50 at year end"
dC2 = decl("A2_propio", ub_am="fila_8", a8=10)
OP_(dC2)["amortizacion_rou"].update({"cita": NOTA_AM, "pagina": 1})   # cita real de una nota, que nombra el derecho de uso; ninguna línea sumada en la fila 8 lo nombra
rC2 = ev_(L1v, dC2, verdad=("no", "fuera"), notas=(NOTA_AM,))
cC2 = cotas(rC2)
paso("R3 (ii) · …con una cita real de una nota: el programa no puede contrastarla con una línea de la fila 8 → no bloquea, pero la conclusión queda CONDICIONADA, con su "
     "cota exacta (−10: el importe declarado) a la vista; cubre el error (78 frente a 68)", rC2["utilizable_para_conclusion"] and cerca(F0(rC2), 78) and "CONDICIONADA" in rC2["rotulo"]
     and estado_tramo(rC2, "amortizacion_rou") == "sin_contrastar" and [round(v, 6) for k, v in cC2.items() if "dentro de la fila 8" in k] == [-10.0]
     and "-10.000" in rC2["rotulo"], rC2["rotulo"][:300])
dC3 = decl("A2_propio", ub_am="fila_8", a8=10)
OP_(dC3)["amortizacion_rou"]["cita"] = L_AM                    # cita real: la línea propia de la amortización, que está en el estado de flujos y la fase 1 no sumó en la fila 8
rC3 = ev_(L1v, dC3, verdad=("fuera", "fuera"))
paso("R3 (ii) · …o citando la línea propia de la amortización del estado de flujos (no sumada en la fila 8) → DATOS INVÁLIDOS", bloquea(rC3, "F1-US-FILAS")
     and g(rC3, "F1-US-FILAS")[0]["efecto"] == "DATOS INVÁLIDOS" and estado_tramo(rC3, "amortizacion_rou") == "contradicha")
rC4 = ev_(libro_v631(libro(dwc=10.0, palancas=False), "A2_propio", 10.0), dict(copy.deepcopy(dC2)), verdad=("no", "fila_14"), notas=(NOTA_AM,), partes=False)
paso("R3 (i)+(ii) · las dos a la vez sin fase1_partes (88 frente a 68: +29,4 %): CONDICIONADA y el resumen de la cota suma las dos (−22 ≤ −20)",
     rC4["utilizable_para_conclusion"] and cerca(F0(rC4), 88) and rC4["condicionada"]["cota"]["resumen"]["flujo_sin_crecimiento_mm"][0] <= -20, rC4["condicionada"]["cota"]["resumen"]["texto"])

# matriz «dónde están de verdad los dos tramos» × «qué se declara» (la de la revisión), con la mejor cita real que tiene quien declara: la línea del estado de flujos
# donde el tramo está de verdad («linea») o una frase de una nota («nota»). Empresa de referencia en un libro V6.3.1 con A2; caja correcta 68
VERDADES = [(am, pas) for am in ("fuera", "fila_8", "fila_14") for pas in ("fuera", "fila_14")]
DECLS = [(am, pas) for am in ("fuera", "no_publicada", "fila_8", "fila_14") for pas in ("fuera", "no_publicada", "fila_14")]
UB = {"fuera": "fuera_de_las_filas_8_y_14", "no_publicada": "no_publicada", "fila_8": "fila_8", "fila_14": "fila_14"}


def caso_matriz(verdad, declarado, con_partes, estrategia):
    (v_am, v_pas), (d_am, d_pas) = verdad, declarado
    aj = None if (d_am == "fila_14") == (d_pas == "fila_14") else (-10 if d_am == "fila_14" else 10)
    d = decl("A2_propio", ub_am=UB[d_am], ub_pas=UB[d_pas], a8=(10 if d_am == "fila_8" else None), ajuste=aj)
    if estrategia == "linea":
        citas = {"amortizacion_rou": ({"fuera": L_AM, "fila_8": DA_ROU, "fila_14": L_ACT}[v_am], 2), "variacion_pasivo": (L_PAS, 2)}
    else:
        citas = {"amortizacion_rou": (NOTA_AM, 1), "variacion_pasivo": (NOTA_PAS, 1)}
    for k, (cita, pag) in citas.items():
        if OP_(d)[k].get("ubicacion") != "no_publicada":
            OP_(d)[k].update({"cita": cita, "pagina": pag})
    L = libro_v631(libro(da=20.0 + (10.0 if v_am == "fila_8" else 0.0), dwc=(-10.0 if v_am == "fila_14" else 0.0) + (10.0 if v_pas == "fila_14" else 0.0), palancas=False),
                   "A2_propio", 10.0 if d_am == "fila_8" else 0.0)
    r = ev_(L, d, verdad=verdad, partes=con_partes, notas=(NOTA_AM, NOTA_PAS))
    err = round(1000 * (0.068 - L["Historia!C58"]) - 68, 6)   # lo que publicaría el libro frente a la caja correcta
    veraz = declarado == verdad   # en esta matriz la empresa publica siempre la línea de cada tramo: «no_publicada» es falso («manda el dato»)
    cs = list(cotas(r).values())
    cubre = (err > 0 and sum(c for c in cs if c < 0) <= -err + 1e-9) or (err < 0 and sum(c for c in cs if c > 0) >= -err - 1e-9)
    return {"util": r["utilizable_para_conclusion"], "err": err, "cond": bool(r.get("condicionada")), "cubre": cubre, "veraz": veraz, "bl": bloquean(r)}


mz = {(cp, es): [(v, dd, caso_matriz(v, dd, cp, es)) for v in VERDADES for dd in DECLS] for cp in (False, True) for es in ("linea", "nota")}
for (cp, es), casos in mz.items():
    util = [c for c in casos if c[2]["util"]]
    mal = [c for c in util if c[2]["err"]]
    sin_cond = [c for c in mal if not c[2]["cond"]]
    fuera_cota = [c for c in mal if c[2]["cond"] and not c[2]["cubre"]]
    paso(f"R3 · matriz verdad × declaración ({'con' if cp else 'sin'} fase1_partes, cita de «{es}»; 72 pares): ningún utilizable con error en el flujo sin condición, y en "
         "todo condicionado con error la cota lo cubre", not sin_cond and not fuera_cota,
         f"utilizables {len(util)} · con error {len(mal)} · sin condición {len(sin_cond)} {[(c[0], c[1]) for c in sin_cond][:3]} · fuera de la cota {len(fuera_cota)} {[(c[0], c[1]) for c in fuera_cota][:3]}")
paso("R3 · matriz con fase1_partes y cita de la línea: ninguna declaración FALSA es utilizable (se contradice con las líneas sumadas o con las no sumadas)",
     not [c for c in mz[(True, "linea")] if c[2]["util"] and not c[2]["veraz"]], str([(c[0], c[1]) for c in mz[(True, "linea")] if c[2]["util"] and not c[2]["veraz"]][:4]))
ver_ = [c for c in mz[(True, "linea")] if c[2]["veraz"]]
paso("R3 · matriz con fase1_partes: una declaración VERAZ nunca termina en DATOS INVÁLIDOS por F1-US-FILAS ni por F1-SERIES (o es utilizable, o es el límite declarado "
     "F1-LIBRO de un tramo solo en la fila 14)", len(ver_) == 6 and all(c[2]["util"] or c[2]["bl"] == ["F1-LIBRO"] for c in ver_) and sum(c[2]["util"] for c in ver_) == 3
     and all(not c[2]["cond"] and not c[2]["err"] for c in ver_ if c[2]["util"]),
     f"veraces {len(ver_)} · utilizables {sum(c[2]['util'] for c in ver_)} · {[(c[0], c[1], c[2]['bl']) for c in ver_ if not c[2]['util'] and c[2]['bl'] != ['F1-LIBRO']][:3]}")

# errores a la baja (revisión): empresa que crece al 5 % con capex por encima de su D&A; la amortización del derecho de uso (2,5 % de las ventas) está de verdad en la fila 8
Vb = [1000 * 1.05 ** i for i in range(10)]
dao_ = [0.02 * v for v in Vb]
cap_ = [dao_[i] + 1.0 * (Vb[i] - (Vb[i - 1] if i else Vb[0] / 1.05)) for i in range(10)]
fcf_ = [0.10 * Vb[i] * 0.75 + dao_[i] - cap_[i] for i in range(10)]
Pb = {y: round(0.03 * Vb[i], 3) for i, y in enumerate(ANIOS)}
Amb = {y: round(0.025 * Vb[i], 3) for i, y in enumerate(ANIOS)}
caja_b = 0.075 * Vb[-1]
Lb = libro(ventas=Vb, ebit=[0.10 * v for v in Vb], da=[dao_[i] + Amb[y] for i, y in enumerate(ANIOS)], tau=0.25, capex=cap_, C70=sum(fcf_[-3:]) / 3)
rb1 = ev_(Lb, decl("A2_propio", P=Pb, Lc=Pb, ub_am="fila_8", a8=Amb))
rb2 = ev_(Lb, decl("A2_propio", P=Pb, Lc=Pb), verdad=("fila_8", "fuera"))
rb3 = ev_(Lb, decl("A2_propio", P=Pb, Lc=Pb, ub_am="no_publicada"), verdad=("no", "fuera"))   # la D&A la lleva y la empresa no lo dice en ninguna línea
err_b = F0(rb3) - caja_b
paso("R3 · error a la baja: con la verdad declarada («fila_8»), la caja sostenible (116,4); declarada «fuera» con la D&A que la nombra, bloquea (la cita no existe y la "
     "línea sumada la nombra)", cerca(F0(rb1), caja_b, 0.01) and bloquean(rb1) == ["F1-LIBRO"] and not rb2["utilizable_para_conclusion"] and bloquea(rb2, "F1-US-FILAS"),
     f"{F0(rb1):.3f} frente a {caja_b:.3f} · {bloquean(rb2)}")
paso("R3 · error a la baja: si la empresa no lo dice en ninguna línea («no_publicada»), el flujo sale un 33 % por debajo, pero CONDICIONADO y con una cota al alza que lo cubre",
     bloquean(rb3) == ["F1-LIBRO"] and bool(rb3.get("condicionada")) and err_b < -38 and max(cotas(rb3).values()) >= -err_b,
     f"flujo {F0(rb3):.3f} · error {err_b:+.3f} · cotas {[round(v, 3) for v in cotas(rb3).values()]}")

paso("R3 · matriz sin fase1_partes: nada se puede contrastar con una línea, así que ningún resultado utilizable lo es sin condición",
     all(c[2]["cond"] for es in ("linea", "nota") for c in mz[(False, es)] if c[2]["util"]) and sum(c[2]["util"] for c in mz[(False, "linea")]) > 0)

# ================================================================== W · D-WM: arrendamientos financieros que la empresa no desglosa → como deuda y activos propios
FIN_ = lambda d: d["arrendamientos_us_gaap"]["financieros"]  # noqa: E731


def d_wm(per="A0_total", caja={2023: 6.0, 2024: 9.0, 2025: 10.1}, gasto={2023: 5.8, 2024: 7.3, 2025: 9.6}, **k):
    """Caso Waste Management a escala: publica el gasto total (amortización + interés) y la caja pagada de sus arrendamientos financieros, sin separar el principal."""
    d = decl(per, fin=True, **k)
    FIN_(d)["desglose"] = "no_publicado"
    if caja is not None:
        d["series"]["caja_pagada_arr_financiero"] = serie(caja)
    if gasto is not None:
        d["series"]["gasto_arr_financiero"] = serie(gasto)
    return d


rw0 = ev_(L1, decl("A2_propio", fin=True, ub_am="no_publicada", ub_pas="no_publicada"))
paso("W · antes de D-WM (revisión F1): financieros sin amortización ni principal publicados por separado → F1-US-DESGLOSE y F1-US-C49 (pendiente_de_datos), y el mensaje "
     "da la salida", bloquea(rw0, "F1-US-DESGLOSE") and bloquea(rw0, "F1-US-C49") and "no_publicado" in g(rw0, "F1-US-DESGLOSE")[0]["detalle"])
rw = ev_(L1, d_wm(ub_am="no_publicada", ub_pas="no_publicada"))
wm = rw["us_gaap"]["D_WM"]
paso("W · D-WM: con «financieros.desglose»: «no_publicado» no se piden la amortización ni el principal; su amortización queda dentro de la propia (D_X no excluye nada) y "
     "C49 = 0: A0 da 68; utilizable", rw["utilizable_para_conclusion"] and bloquean(rw) == [] and cerca(F0(rw), 68) and rw["us_gaap"]["financieros"]["tratados_como_deuda_D_WM"] is True
     and M.leer_us(d_wm(), ANIOS)["rou8"] == {y: Fr(0) for y in ANIOS}, str(bloquean(rw)))
paso("W · es una hipótesis declarada: la conclusión es CONDICIONADA (D-US1 + D-WM), con el registro de la decisión (18-nov-2026, DECISIONES…:112–114)",
     rw["condicionada"]["hipotesis"] == "D-US1 + D-WM" and "CONDICIONADA" in rw["rotulo"] and "D-WM" in rw["rotulo"] and wm["registro"]["fecha"] == "2026-11-18"
     and "112–114" in wm["registro"]["motivo"] and any(c["id"] == "D-WM" and "no es un dato" in c["texto"] for c in rw["condicionada"]["condiciones"]), rw["rotulo"][:200])
de = wm["diferencia_estimada"]
cw = [v for k, v in cotas(rw).items() if "D-WM" in k]
paso("W · la diferencia estimada queda junto al resultado: caja pagada − gasto total = +0,8 mm al año (1,18 % de CFO − capex medio); tratados como arrendamientos el flujo "
     "sería 0,8 menor", cerca(de["caja_pagada_menos_gasto_total_medio_mm"], 0.8) and cerca(de["%_de_CFO_menos_capex_medio (Análisis C46 − C47)"], 100 * 0.8 / 68, 1e-3)
     and len(cw) == 1 and cerca(cw[0], -0.8) and "+0.800 mm" in rw["condicionada"]["texto"], f"{de['caja_pagada_menos_gasto_total_medio_mm']} · {cw}")
paso("W · K3b: los financieros «como deuda (D-WM)» y los operativos una vez; F1-US-C49 confirma que sus pagos no se restan de la caja base",
     rw["K3"]["K3b_por_clase"] == {"operativos": "una vez", "financieros": "como deuda (D-WM)"} and not salta(rw, "F1-US-C49") and "D-WM" in g(rw, "F1-US-C49")[0]["detalle"])
rw3 = ev_(libro(C70=63.0, C49=5.0, princ=5.0), d_wm())
paso("W · con D-WM y C49 = 5 (principal restado además de la amortización dentro de D_X: dos veces) → F1-US-C49 DATOS INVÁLIDOS y K3b lo dice",
     bloquea(rw3, "F1-US-C49") and g(rw3, "F1-US-C49")[0]["efecto"] == "DATOS INVÁLIDOS" and bloquea(rw3, "F1-K3b") and not salta(rw3, "F1-ROU-HISTORIA"))
rw4 = ev_(L1, d_wm(gasto=None))
paso("W · sin el gasto total publicado no se puede enseñar la diferencia estimada → F1-US-DESGLOSE INCOMPLETO", bloquea(rw4, "F1-US-DESGLOSE")
     and "gasto_arr_financiero" in g(rw4, "F1-US-DESGLOSE")[0]["detalle"] and g(rw4, "F1-US-DESGLOSE")[0]["efecto"] == "INCOMPLETO")
rw5 = ev_(L1, d_wm(rou_fin=5))
paso("W · «no_publicado» con importes en series.da_rou → DATOS INVÁLIDOS: si la empresa publica el desglose manda el dato", bloquea(rw5, "F1-US-DESGLOSE")
     and g(rw5, "F1-US-DESGLOSE")[0]["efecto"] == "DATOS INVÁLIDOS" and "manda el dato" in g(rw5, "F1-US-DESGLOSE")[0]["detalle"])
rw6 = ev_(L1, d_wm())
paso("W · con los operativos contrastados con su línea, la única condición es D-WM", rw6["condicionada"]["hipotesis"] == "D-WM" and rw6["condicionada"]["tramos"] == []
     and rw6["condicionada"]["registro"]["fecha"] == "2026-11-18" and "-0.800" in rw6["condicionada"]["cota"]["resumen"]["texto"], rw6["condicionada"]["cota"]["resumen"]["texto"])
dw7 = d_wm()
FIN_(dw7)["desglose"] = "a medias"
paso("W · «desglose» es un valor cerrado (publicado | no_publicado)", g(ev_(L1, dw7), "F1-US-DESGLOSE")[0]["efecto"] == "DATOS INVÁLIDOS")
dw9 = d_wm()
FIN_(dw9)["amortizacion_rou"] = {"ubicacion": "fuera_de_la_fila_8", "documento": DOC, "pagina": 1, "cita": "Finance lease cost"}
gw9 = g(ev_(L1, dw9), "F1-US-DESGLOSE")[0]
paso("W · «desglose»: «no_publicado» (D-WM) y la ubicación de la amortización de los financieros no se declaran a la vez: DATOS INVÁLIDOS (con D-WM esa amortización "
     "queda dentro de la propia)", gw9["salta"] and gw9["efecto"] == "DATOS INVÁLIDOS" and "no se declara dónde está esa amortización" in gw9["detalle"], gw9["detalle"][:200])
dw8 = decl("A0_total", fin=True, rou_fin=5, fin_princ=5)
dw8["series"]["caja_pagada_arr_financiero"] = serie(6)
paso("W · las series de D-WM con el desglose «publicado» no se ignoran en silencio → DATOS INVÁLIDOS", g(ev_(L2, dw8), "F1-US-DESGLOSE")[0]["efecto"] == "DATOS INVÁLIDOS")
paso("W · en el libro V6.3.1 la fila 86 no lleva nada de los financieros tratados como deuda (solo la amortización operativa que esté dentro de la fila 8)",
     all(V631.celdas(d_wm("A2_propio"), ANIOS)[f"Historia!{c}86"] == 0.0 for c in COLS)
     and all(V631.celdas(d_wm("A2_propio", ub_am="fila_8", a8=10), ANIOS)[f"Historia!{c}86"] == 10.0 for c in COLS))
rwb = ev_(libro(fila22=100.0, fila23=30.0, motor="B"), d_wm(pasivo=0))
paso("W · motor B con D-WM: los financieros son deuda del puente (130); no bloquea", rwb["utilizable_para_conclusion"]
     and cerca(rwb["us_gaap"]["puente_de_deuda"]["deuda_del_puente_coherente"], 130), str(bloquean(rwb)))

# ================================================================== R6 · «no_publicada» frente a la página del estado de flujos (revisión, grupo N)
dN1 = decl("A0_total", ub_am="no_publicada", ub_pas="no_publicada")
rN1 = ev_(L6, dN1, verdad=("no", "fila_14"))
paso("R6 · (N1, control) página con «Operating lease liabilities (…)» y los dos tramos «no_publicada» → F1-SERIES DATOS INVÁLIDOS («manda el dato»)",
     salta(rN1, "F1-SERIES") and "manda el dato" in g(rN1, "F1-SERIES")[0]["detalle"] and not rN1["utilizable_para_conclusion"])
dN2 = decl("A0_total", ub_am="no_publicada", ub_pas="no_publicada", pasivo=50)
dN2["series"]["pasivo_arr_operativo"]["2025"]["fila"] = "Operating lease liabilities"     # la etiqueta natural de la fila del balance
rN2 = ev_(dict(L6, **{f"Historia!{c}23": 50.0 for c in COLS}), dN2, verdad=("no", "fila_14"))
paso("R6 · (N2) la «fila» de una serie (la etiqueta del balance) ya no anula el contraste: sigue DATOS INVÁLIDOS (antes: utilizable, 78 frente a 68)",
     salta(rN2, "F1-SERIES") and "manda el dato" in g(rN2, "F1-SERIES")[0]["detalle"] and not rN2["utilizable_para_conclusion"])
dN3 = decl("A0_total", ub_am="no_publicada", ub_pas="no_publicada")
OP_(dN3)["cita"] = "Operating lease liabilities"     # cita de que existen: la línea del balance
rN3 = ev_(L6, dN3, verdad=("no", "fila_14"), notas=("Operating lease liabilities",))
paso("R6 · (N3) la cita de «operativos.existen» tampoco lo anula: sigue DATOS INVÁLIDOS", salta(rN3, "F1-SERIES") and "manda el dato" in g(rN3, "F1-SERIES")[0]["detalle"]
     and not rN3["utilizable_para_conclusion"])
ROTULOS = ("Operating lease liabilities", "Non-cash lease expense", "Noncash operating lease cost", "Operating lease right-of-use assets",
           "Reduction in the carrying amount of right-of-use assets", "Amortization of ROU assets", "Operating lease assets and liabilities, net",
           "Lease assets and liabilities, net", "Operating leases, net", "Operating lease asset amortization", "Amortization of operating and finance lease right-of-use assets",
           "Right-of-use assets", "Changes in operating lease right" + chr(0x2011) + "of" + chr(0x2011) + "use assets", "Other assets and liabilities, including operating leases")
no_vistos = []
for rot in ROTULOS:
    rr = ev_(L1, decl("A0_total", ub_am="no_publicada", ub_pas="no_publicada"), verdad=("no", "no"), fuera=[rot])
    if not (salta(rr, "F1-SERIES") and "manda el dato" in g(rr, "F1-SERIES")[0]["detalle"]):
        no_vistos.append(rot)
paso("R6 · (N4) los 14 rótulos habituales de un estado de flujos se ven en la página con el patrón amplio (antes, 10 no se veían), también la línea que mezcla "
     "operativos y financieros", not no_vistos, str(no_vistos))
dN5 = decl("A0_total", ub_am="no_publicada")
OP_(dN5)["variacion_pasivo"]["cita"] = "Operating leases, net"
rN5 = ev_(L1, dN5, verdad=("no", "no"), fuera=["Operating leases, net"])
paso("R6 · solo se excluye la línea del OTRO tramo cuando está declarada con su ubicación: «Operating leases, net» citada para el pasivo («fuera») no invalida la "
     "amortización «no_publicada»", not salta(rN5, "F1-SERIES") and rN5["utilizable_para_conclusion"] and rN5["condicionada"]["tramos"] == ["amortizacion_rou"], str(bloquean(rN5)))
rN6 = ev_(L1, decl("A0_total", ub_am="no_publicada", ub_pas="no_publicada"), verdad=("no", "no"))
paso("R6 · las líneas solo de financieros («Principal payments on finance lease obligations») y la información complementaria («…obtained in exchange for…») no son tramos "
     "del arrendamiento operativo: no invalidan «no_publicada»", not salta(rN6, "F1-SERIES") and rN6["F1_SERIES"]["paginas_sin_linea_propia_del_arrendamiento_operativo"] == 2)

FIN_SIN = "Payments on lease liabilities"   # el principal de los financieros, en financiación, con un rótulo que no dice «finance»
rN7 = ev_(L1, decl("A0_total", ub_am="no_publicada", ub_pas="no_publicada"), verdad=("no", "no"), despues_cfo=[FIN_SIN])
paso("R6 · una línea que nombra el pasivo por arrendamiento DESPUÉS del total del flujo de explotación (financiación: principal de los financieros) no es un tramo del "
     "operativo: no invalida «no_publicada»", not salta(rN7, "F1-SERIES") and rN7["utilizable_para_conclusion"] and rN7["F1_SERIES"]["paginas_sin_linea_propia_del_arrendamiento_operativo"] == 2,
     g(rN7, "F1-SERIES")[0]["detalle"][:160])
dN8 = decl("A0_total")
OP_(dN8)["variacion_pasivo"]["cita"] = FIN_SIN
rN8 = ev_(L6, dN8, verdad=("fuera", "no"), wc=("Accounts receivable", "Accrued and other liabilities"), despues_cfo=[FIN_SIN])
paso("R6 · …y tampoco sirve para probar «fuera»: citar esa línea de financiación (real, del estado de flujos y no sumada) → F1-US-FILAS INCOMPLETO",
     bloquean(rN8) == ["F1-US-FILAS"] and "después del total del flujo de explotación" in g(rN8, "F1-US-FILAS")[0]["detalle"], g(rN8, "F1-US-FILAS")[0]["detalle"][:260])

# ================================================================== R7 · el coste lineal declarado y los pagos, con el mismo perímetro
P_WM, L_WM = {2023: 7.7, 2024: 10.3, 2025: 21.4}, {2023: 18.9, 2024: 26.4, 2025: 42.7}   # caso Waste Management a escala: el gasto publicado lleva corto plazo y variable
dR7 = decl("A0_total", ub_am="no_publicada", ub_pas="no_publicada", P=P_WM, Lc=L_WM)
rR7a = ev_(L1, dR7)
paso("R7 · sin declarar nada, la diferencia se enseña y el resultado lleva la relación coste ÷ pagos (2,23) para que se vea si es de perímetro y no de calendario",
     cerca(rR7a["us_gaap"]["diferencia_coste_lineal_menos_pagos"]["coste_entre_pagos"], round((18.9 + 26.4 + 42.7) / (7.7 + 10.3 + 21.4), 4), 1e-4)
     and "perímetro" in rR7a["us_gaap"]["diferencia_coste_lineal_menos_pagos"]["nota"])
dR7b = copy.deepcopy(dR7)
OP_(dR7b).update({"coste_comparable_con_los_pagos": False, "coste_no_comparable_motivo": "el gasto publicado incluye corto plazo y variable; la empresa no lo separa"})
rR7 = ev_(L1, dR7b)
dfR7 = rR7["us_gaap"]["diferencia_coste_lineal_menos_pagos"]
paso("R7 · declarado «no comparable» (con su motivo): la diferencia coste − pagos NO se calcula ni se presenta como diferencia de calendario; no bloquea",
     rR7["utilizable_para_conclusion"] and dfR7["comparable"] is False and "coste_menos_pagos_medio" not in dfR7 and "no se calcula" in g(rR7, "F1-US-BASE")[0]["detalle"]
     and "corto plazo" in g(rR7, "F1-US-BASE")[0]["detalle"], g(rR7, "F1-US-BASE")[0]["detalle"][:200])
paso("R7 · …y la cota de D-US1 que usa el coste se rotula «cota holgada»", any("cota holgada" in k for k in cotas(rR7)) and not any("cota holgada" in k for k in cotas(rR7a)))
dR7c = copy.deepcopy(dR7b)
del OP_(dR7c)["coste_no_comparable_motivo"]
paso("R7 · «no comparable» sin su motivo → F1-US-DESGLOSE INCOMPLETO", bloquea(ev_(L1, dR7c), "F1-US-DESGLOSE"))
dR7d = decl("A0_total", ub_am="fila_14", ub_pas="fila_14", P=P_WM, Lc=L_WM)
OP_(dR7d).update({"coste_comparable_con_los_pagos": False, "coste_no_comparable_motivo": "incluye corto plazo y variable"})
rR7d = ev_(L1, dR7d)
paso("R7 · con D-US2 bis y el coste no comparable, cuánto cambiaría contando los pagos no se puede calcular: se dice así (no se inventa) y no bloquea",
     bloquean(rR7d) == [] and rR7d["us_gaap"]["D_US2_bis"]["contando_los_pagos"] is None and "NO se puede calcular" in rR7d["us_gaap"]["D_US2_bis"]["texto"])

# ================================================================== R13 · F1-US-C49: redondeo de la etapa 1 y diferencia explicada
PR6 = [5.0] * 7 + [5.0, 6.0, 6.0]                      # principal publicado 5/6/6: media 5,667
FP6 = {y: v for y, v in zip(ANIOS, PR6)}
rE6 = ev_(libro(ebit=63.0, da=25.0, C70=61.3, C49=5.7, princ=PR6), decl("A2_propio", fin=True, rou_fin=5, fin_princ=FP6))
paso("R13 · (revisión E6) principal 5/6/6 (media 5,667) y C49 = 5,7 (un decimal, como lo registra la etapa 1): es redondeo → F1-US-C49 no salta (antes: DATOS INVÁLIDOS)",
     not salta(rE6, "F1-US-C49") and "±0.05" in g(rE6, "F1-US-C49")[0]["detalle"], g(rE6, "F1-US-C49")[0]["detalle"])
rE6b = ev_(libro(ebit=63.0, da=25.0, C70=61.0, C49=6.0, princ=PR6), decl("A2_propio", fin=True, rou_fin=5, fin_princ=FP6))
paso("R13 · con C49 sin decimales (6) la tolerancia es media unidad", not salta(rE6b, "F1-US-C49"))
rE6c = ev_(libro(ebit=63.0, da=25.0, C70=61.2, C49=5.8, princ=PR6), decl("A2_propio", fin=True, rou_fin=5, fin_princ=FP6))
gE6c = g(rE6c, "F1-US-C49")[0]
paso("R13 · C49 = 5,8 (0,133 más que el principal: más que el redondeo) → bloquea, y el mensaje no afirma que sean pagos operativos («si son…»)",
     bloquea(rE6c, "F1-US-C49") and "no está explicada" in gE6c["detalle"] and "Si son pagos de arrendamientos operativos" in gE6c["detalle"], gE6c["detalle"][:230])
dE6d = decl("A2_propio", fin=True, rou_fin=5, fin_princ=FP6)
dE6d["conciliacion_fcf_base"] = [{"componente": "C49", "importe": -0.133333, "partida": "principal de un arrendamiento financiero pagado en enero y registrado en C49",
                                  "fuente": {"documento": DOC, "pagina": 1}}]
rE6d = ev_(libro(ebit=63.0, da=25.0, C70=61.2, C49=5.8, princ=PR6), dE6d)
paso("R13 · la misma diferencia explicada por una partida declarada con su fuente en conciliacion_fcf_base (componente C49, como K3a) → no bloquea: AVISA y pide comprobar "
     "que no son pagos operativos; K3b no cuenta un exceso", not bloquea(rE6d, "F1-US-C49") and g(rE6d, "F1-US-C49")[0]["severidad"] == "AVISO"
     and rE6d["K3"]["K3b_por_clase"]["operativos"] == "una vez" and not salta(rE6d, "F1-K3a"), g(rE6d, "F1-US-C49")[0]["detalle"][:200])
rE6e = ev_(libro(ebit=63.0, da=25.0, C70=67.0, C49=0.0), decl("A2_propio", fin=True, rou_fin=5, fin_princ={y: v for y, v in zip(ANIOS, [0] * 9 + [1])}))
paso("R13 · un cero en C49 no dice con cuántos decimales se escribió: principal 0/0/1 (media 0,333) y C49 = 0 → sigue bloqueando (se omitiría)",
     bloquea(rE6e, "F1-US-C49") and "se omitiría" in g(rE6e, "F1-US-C49")[0]["detalle"])

# ================================================================== R16 · financieros cuya amortización del derecho de uso no está dentro de la D&A (revisión E4)
L16 = libro(C70=67.0, C49=1.0, princ=1.0)
F16 = "Amortization of finance lease right-of-use assets"


def d16(per="A2_propio", pagina=1, **k):
    d = decl(per, fin=True, fin_princ=1, **k)
    FIN_(d)["amortizacion_rou"] = {"ubicacion": "fuera_de_la_fila_8", "documento": DOC, "pagina": pagina, "cita": F16}
    d["series"]["da_rou_financiero_fuera"] = serie(1)
    return d


r16v = ev_(L16, decl("A2_propio", fin=True, rou_fin=0, fin_princ=1))
paso("R16 · (control) da_rou = 0 con principal en la fila 17 y sin decir dónde está esa amortización: F1-ROU-HISTORIA sigue bloqueando, y el mensaje dice cómo se "
     "declara la verdad con US GAAP («fuera_de_la_fila_8» o D-WM)", bloquea(r16v, "F1-ROU-HISTORIA") and "fuera_de_la_fila_8" in g(r16v, "F1-ROU-HISTORIA")[0]["detalle"]
     and "D-WM" in g(r16v, "F1-ROU-HISTORIA")[0]["detalle"])
r16 = ev_(L16, d16(), notas=(F16,))
c16 = [v for k, v in cotas(r16).items() if "financieros" in k]
paso("R16 · declarar la verdad no bloquea: amortización del derecho de uso financiero «fuera_de_la_fila_8» (con su evidencia y su cifra publicada) → F1-ROU-HISTORIA no salta; "
     "A2 da 67 = FCF base; K3b una vez en las dos clases", not salta(r16, "F1-ROU-HISTORIA") and bloquean(r16) == ["F1-LIBRO"] and cerca(F0(r16), 67)
     and r16["K3"]["K3b_por_clase"] == {"operativos": "una vez", "financieros": "una vez"}, str(bloquean(r16)))
paso("R16 · como la cita es de una nota y ninguna línea lo contrasta, queda CONDICIONADA con su cota exacta (+1: si estuviera dentro de la D&A se contaría dos veces)",
     estado_tramo(r16, "amortizacion_rou_financiero") == "sin_contrastar" and c16 == [1.0] and "F1-US-FILAS" in r16["condicionada"]["hipotesis"], str(cotas(r16)))
r16l = ev_(L16, d16(pagina=2), fuera=[L_AM, L_PAS, F16])
paso("R16 · con su línea propia en el estado de flujos, no sumada en la fila 8 → contrastada: sin condición", estado_tramo(r16l, "amortizacion_rou_financiero") == "contrastada"
     and "condicionada" not in r16l and bloquean(r16l) == ["F1-LIBRO"], str(bloquean(r16l)))
r16c = ev_(L16, d16(), notas=(F16,), da=[DA, F16])
paso("R16 · si la fase 1 sumó en la fila 8 una línea de arrendamiento financiero, declararla fuera contradice al expediente → DATOS INVÁLIDOS", bloquea(r16c, "F1-US-FILAS")
     and g(r16c, "F1-US-FILAS")[0]["efecto"] == "DATOS INVÁLIDOS" and estado_tramo(r16c, "amortizacion_rou_financiero") == "contradicha")
r16a = ev_(L16, d16("A0_total"), notas=(F16,))
paso("R16 · con A0 tampoco bloquea V-F1m (C49 positivo y amortización a cero dentro de la fila 8 no es un conflicto si está declarada fuera): utilizable",
     not salta(r16a, "V-F1m") and r16a["utilizable_para_conclusion"] and cerca(F0(r16a), 67), str(bloquean(r16a)))
d16s = d16()
del d16s["series"]["da_rou_financiero_fuera"]
paso("R16 · «fuera_de_la_fila_8» sin la cifra publicada de esa amortización → F1-US-DESGLOSE INCOMPLETO (sin ella no hay cota)", bloquea(ev_(L16, d16s, notas=(F16,)), "F1-US-DESGLOSE"))

# ================================================================== R14 · declaraciones mal formadas: DATOS INVÁLIDOS, no una excepción
import random  # noqa: E402

for nombre, cambio in (("una serie de US GAAP que es un texto", lambda d: d["series"].update(pagos_arr_operativo="x")),
                       ("una serie que es una lista", lambda d: d["series"].update(da_rou_operativo=[1, 2])),
                       ("«series» que es una lista", lambda d: d.update(series=[1, 2])),
                       ("«clasificacion_compras» que es un texto", lambda d: d.update(clasificacion_compras="sin_compras")),
                       ("«transicion» que es un número", lambda d: d.update(transicion=3)),
                       ("«normalizacion.ajustes» que es un número", lambda d: d.update(normalizacion={"ajustes": 7})),
                       ("una ubicación que es una lista", lambda d: OP_(d)["amortizacion_rou"].update(ubicacion=["fila_8"]))):
    dm = decl("A0_total")
    cambio(dm)
    try:
        rm = M.evaluar(L1, dm)
        ok = (bloquea(rm, "F1-DECLARACION") or bloquea(rm, "F1-US-DESGLOSE")) and rm["estado_propuesto"] == "pendiente_de_datos"
        det = str(bloquean(rm))
    except Exception as ex:  # noqa: BLE001
        ok, det = False, f"{type(ex).__name__}: {ex}"
    paso(f"R14 · {nombre}: no hace fallar el programa; DATOS INVÁLIDOS (pendiente_de_datos)", ok, det)

RAROS = [None, "", 0, 1, -1, 1.5, True, False, [], {}, "fila_8", "fila_14", "no_publicada", "fuera_de_las_filas_8_y_14", "x", {"ubicacion": "fila_14"}, [1, 2], "2025", {"valor": 3}]
rnd = random.Random(842)


def mutar(x, prob):
    if isinstance(x, dict):
        out = {}
        for k_, v_ in x.items():
            r_ = rnd.random()
            if r_ < prob * 0.4:
                continue
            out[k_] = rnd.choice(RAROS) if r_ < prob else mutar(v_, prob)
        if rnd.random() < prob * 0.3:
            out[rnd.choice(["ubicacion", "existen", "pagina", "cita", "2025", "valor_fuente", "signo", "literal", "fila", "operativos", "registro", "desglose"])] = rnd.choice(RAROS)
        return out
    return x


exc, util_incompleto, n_util, N_FUZZ = {}, [], 0, 600
for i in range(N_FUZZ):
    base = decl(rnd.choice(["A0_total", "A2_propio", "A1_sin_ROU"]), fin=rnd.choice([True, False]), ub_am=rnd.choice(["fila_8", "fila_14", "fuera_de_las_filas_8_y_14", "no_publicada"]),
                ub_pas=rnd.choice(["fila_14", "fuera_de_las_filas_8_y_14", "no_publicada"]), a8=rnd.choice([None, 10]), ajuste=rnd.choice([None, 10, -10]),
                rou_fin=rnd.choice([None, 5]), fin_princ=rnd.choice([None, 5]), pasivo=rnd.choice([None, 0, 50]))
    if rnd.random() < 0.3:
        base = d_wm(rnd.choice(["A0_total", "A2_propio"]))
    dz = mutar(base, rnd.choice([0.03, 0.1, 0.25]))
    Lz = libro(da=rnd.choice([20.0, 25.0, 30.0]), dwc=rnd.choice([0.0, 10.0, -10.0]), C49=rnd.choice([0.0, 5.0]), princ=rnd.choice([0.0, 5.0]), fila23=rnd.choice([0.0, 50.0]),
               motor=rnd.choice(["A", "A", "B"]), l4=rnd.choice(["US GAAP", "US GAAP", "IFRS", "U.S. GAAP"]))
    cz_tmp = tempfile.mkdtemp(prefix="f1_us_")   # se crea aquí para poder borrarla aunque la fuente no se llegue a escribir (antes quedaba vacía en /tmp)
    try:
        cz = expediente(copy.deepcopy(dz) if not isinstance(dz.get("series"), dict) else dz, carpeta=cz_tmp, partes=rnd.random() < 0.7)
    except Exception:  # noqa: BLE001 — la declaración mutada no deja escribir la fuente: se evalúa sin carpeta
        cz = None
    try:
        rz = M.evaluar(Lz, dz, carpeta=cz)
        json.dumps(rz, default=str)
        if rz.get("utilizable_para_conclusion"):
            n_util += 1
            bz = dz.get("arrendamientos_us_gaap")
            if not (isinstance(bz, dict) and all(isinstance(bz.get(k_), dict) and isinstance(bz[k_].get("existen"), bool) for k_ in ("operativos", "financieros"))):
                util_incompleto.append(i)
    except M.ErrorDeclaracion:
        pass
    except Exception as ex:  # noqa: BLE001
        import traceback
        tb = traceback.extract_tb(ex.__traceback__)[-1]
        k_ = f"{type(ex).__name__} @ {os.path.basename(tb.filename)}:{tb.lineno} {tb.name}"
        exc[k_] = exc.get(k_, 0) + 1
    finally:
        shutil.rmtree(cz_tmp, ignore_errors=True)
paso(f"R14 · {N_FUZZ} declaraciones mal formadas al azar (semilla fija): ninguna excepción sin controlar (antes, AttributeError en una de cada nueve) y ningún «utilizable» "
     "con el desglose de arrendamientos incompleto", not exc and not util_incompleto, f"utilizables {n_util} · excepciones {exc} · utilizables incompletos {util_incompleto[:5]}")

# ================================================================== R1 · motor B: sin poder determinar la norma, falla en cerrado (como el motor A)
t415 = tempfile.mkdtemp(prefix="f1_us_415_")
tvie = tempfile.mkdtemp(prefix="f1_us_viejo_")
TMP += [t415, tvie]
json.dump({"modo": "registrada", "motivo": "expediente de la 4.15 (prueba)"}, open(os.path.join(t415, "entrada_efectiva.json"), "w"))
paso("R1 · exigido_puente: con el libro «US GAAP» se exige; con un libro NIIF reconocido, no (T11 no cambia), tampoco en un expediente de la 4.15",
     M.exigido_puente(t415, L=libro(motor="B")) and M.exigido_puente(tvie, L=libro(motor="B")) and not M.exigido_puente(t415, L=libro(l4="IFRS", motor="B"))
     and not M.exigido_puente(t415, L=libro(l4="IFRS (IFRS-EU)", motor="B")))
paso("R1 · (revisión G1) L4 fuera de la lista («U.S. GAAP», «Otro») o vacío en un expediente de la 4.15: no se puede descartar US GAAP → F1 se exige (antes: no se evaluaba nada)",
     all(M.exigido_puente(t415, L=libro(l4=x, motor="B")) for x in ("U.S. GAAP", "Otro", "", "US GAAP (no IFRS)")))
paso("R1 · (revisión G2) expediente de la 4.15 sin libro evaluado legible: se exige (falla en cerrado); en un expediente histórico (no 4.15) no cambia nada",
     M.exigido_puente(t415) and not M.exigido_puente(tvie) and not M.exigido_puente(tvie, L=libro(l4="U.S. GAAP", motor="B")) and M.norma_del_expediente(t415) == (None, False))
rG1 = M.evaluar(libro(fila22=100.0, fila23=50.0, motor="B", l4="U.S. GAAP"), {}, carpeta=t415)
paso("R1 · motor B, libro «U.S. GAAP» y sin declaración en un expediente de la 4.15: F1 aplica y F1-NORMA bloquea (pendiente_de_datos); nunca un puente silencioso",
     rG1["aplica"] is True and bloquea(rG1, "F1-NORMA") and rG1["estado_propuesto"] == "pendiente_de_datos" and "motor B" in rG1["rotulo"] and "sin determinar" in rG1["alcance"],
     rG1["rotulo"])
rG1v = M.evaluar(libro(fila22=100.0, fila23=50.0, motor="B", l4="U.S. GAAP"), {}, carpeta=tvie)
paso("R1 · el mismo libro en un expediente histórico (no de la 4.15): F1 sigue sin aplicar (los cierres anteriores no cambian)", rG1v["aplica"] is False and not rG1v["bloquea"])
rG1n = M.evaluar(libro(motor="B", l4=""), dN, carpeta=t415)
paso("R1 · motor B, declaración NIIF y libro sin norma (L4 vacío) en la 4.15 → F1-NORMA INCOMPLETO, sin pedir el desglose de US GAAP", bloquean(rG1n) == ["F1-NORMA"]
     and g(rG1n, "F1-NORMA")[0]["efecto"] == "INCOMPLETO" and not g(rG1n, "F1-US-DESGLOSE"))
rG1x = M.evaluar(libro(fila22=100.0, fila23=50.0, motor="B"), {}, carpeta=t415)
paso("R1 · (revisión XB3, en la capa) motor B, libro US GAAP y sin declaración F1: F1-NORMA y F1-US-DESGLOSE bloquean (pendiente_de_datos)",
     bloquea(rG1x, "F1-NORMA") and bloquea(rG1x, "F1-US-DESGLOSE") and rG1x["estado_propuesto"] == "pendiente_de_datos")

# ================================================================== R11 · la norma de la fase 1 es un valor de lista cerrada desde su origen
paso("R11 · norma_fase1_no_admitida: «IFRS», «US GAAP», las dos variantes históricas, «Otro» y el vacío se admiten",
     all(M.norma_fase1_no_admitida(x) is None for x in ("IFRS", "US GAAP", " us gaap ", "IFRS (IFRS-EU)", "IFRS (adoptadas por la Unión Europea)", "Otro", "", None)))
paso("R11 · …y las variantes verosímiles que antes llegaban al paso 7 se rechazan en origen, con el motivo («IFRS (EU)», «IFRS as adopted by the EU», «U.S. GAAP», «IAS/IFRS»)",
     all(isinstance(M.norma_fase1_no_admitida(x), str) and "lista cerrada" in M.norma_fase1_no_admitida(x) for x in ("IFRS (EU)", "IFRS as adopted by the EU", "U.S. GAAP", "IAS/IFRS", "NIIF-UE")))
prm = open(os.path.join(PV, "prompts", "metadatos_fase1.md"), encoding="utf-8").read()
paso("R11 · la instrucción de los metadatos de la fase 1 cierra el vocabulario («IFRS» o «US GAAP», exactamente)", 'EXACTAMENTE `"IFRS"`' in prm and '`"US GAAP"`' in prm
     and '("IFRS" / "US GAAP" / …)' not in prm)

# ================================================================== X · cierre de la ronda 2 (revisión R2): líneas ajenas al tramo, importes, financieros en la fila 8, notas y «Otro»
SEN_ACT, SEN_PAS, SEN_GEN = "Impairment of operating lease right-of-use assets", "Gain on termination of operating lease liabilities", "Loss on lease termination"
SEN_PARTIDA = ("Impairment of long-lived assets and operating lease", "right-of-use assets")
WC_SIN = list(WC) + ["Accrued and other liabilities"]
LX = libro_v631(libro(dwc=10.0, palancas=False), "A2_propio", 0.0)   # la variación del pasivo (10) va dentro de «Accrued and other liabilities»: el libro da 78; lo correcto, 68
LX0 = libro_v631(libro(palancas=False), "A2_propio", 0.0)


def d_np():
    return decl("A2_propio", ub_am="no_publicada", ub_pas="no_publicada")


def con_citas(am=None, pas=None, **k):
    d = decl("A2_propio", **k)
    for clave, cita in (("amortizacion_rou", am), ("variacion_pasivo", pas)):
        if cita:
            OP_(d)[clave]["cita"] = cita
    return d


def ajenas(r):
    return r["us_gaap"]["contraste_de_ubicaciones"]["lineas_ajenas_al_tramo"]


# ---- R2-1 · una línea que nombra el arrendamiento sin ser el tramo
rx1 = ev_(LX, d_np(), verdad=("no", "no"), wc=WC_SIN, fuera=[SEN_ACT])
paso("X · (R2-1, C1) declaración VERAZ «no_publicada» con una línea de deterioro del derecho de uso en el estado de flujos: ya no bloquea («manda el dato» no salta); "
     "utilizable y CONDICIONADA (D-US1), con la cota que cubre el error (+10 dentro de −12) y la línea ajena a la vista",
     rx1["utilizable_para_conclusion"] and bloquean(rx1) == [] and rx1["condicionada"]["hipotesis"] == "D-US1" and min(cotas(rx1).values()) <= -12 + 1e-9
     and any("Impairment" in x for x in ajenas(rx1)) and not salta(rx1, "F1-SERIES") and "no son un tramo" in g(rx1, "F1-US-FILAS")[0]["detalle"],
     f"{bloquean(rx1)} · {sorted(cotas(rx1).values())}")
rx1b = ev_(LX, d_np(), verdad=("no", "no"), wc=WC_SIN, fuera=[SEN_PARTIDA])
paso("X · (R2-1) lo mismo con la etiqueta partida en dos renglones (el deterioro está en el primero; el derecho de uso, en el de las cifras): la línea entera es ajena",
     rx1b["utilizable_para_conclusion"] and rx1b["condicionada"]["hipotesis"] == "D-US1" and len(ajenas(rx1b)) == 1 and "Impairment" in ajenas(rx1b)[0]
     and "right-of-use" in ajenas(rx1b)[0], str(bloquean(rx1b)))
rx1c = ev_(LX, d_np(), verdad=("no", "no"), wc=WC_SIN + [SEN_GEN])
paso("X · (R2-1) una línea ajena que la fase 1 SUMÓ en la fila 14 («Loss on lease termination») no contradice la declaración veraz «no_publicada» (antes: DATOS INVÁLIDOS)",
     rx1c["utilizable_para_conclusion"] and rx1c["condicionada"]["hipotesis"] == "D-US1" and not bloquea(rx1c, "F1-US-FILAS"), str(bloquean(rx1c)))
rx1d = ev_(LX, d_np(), verdad=("no", "no"), wc=WC_SIN, fuera=["Operating lease liabilities and other"])
paso("X · (R2-1) control: una línea que SÍ nombra el tramo sigue haciendo saltar «manda el dato» frente a «no_publicada»", bloquean(rx1d) == ["F1-SERIES"]
     and "manda el dato" in g(rx1d, "F1-SERIES")[0]["detalle"], str(bloquean(rx1d)))
rx2 = ev_(LX, con_citas(SEN_ACT, SEN_PAS), verdad=("no", "no"), wc=WC_SIN, fuera=[SEN_ACT, SEN_PAS])
gx2 = g(rx2, "F1-US-FILAS")[0]
paso("X · (R2-1, C3) los dos tramos «fuera» citando una línea de deterioro y otra de cancelación: no valen como línea del tramo → F1-US-FILAS INCOMPLETO, y el mensaje "
     "lleva a «no_publicada» (antes: utilizable sin condición, con 78)", bloquean(rx2) == ["F1-US-FILAS"] and gx2["efecto"] == "INCOMPLETO"
     and estado_tramo(rx2, "amortizacion_rou") == "insuficiente" and estado_tramo(rx2, "variacion_pasivo") == "insuficiente" and "junto a otra cosa" in gx2["detalle"]
     and "no_publicada" in gx2["detalle"] and rx2["K3"]["K3b_contrastado"] is False, gx2["detalle"][:200])
rx2g = ev_(LX, con_citas(SEN_GEN, SEN_GEN), verdad=("no", "no"), wc=WC_SIN, fuera=[SEN_GEN])
rx2m = ev_(LX, con_citas(SEN_ACT, ub_pas="no_publicada"), verdad=("no", "no"), wc=WC_SIN, fuera=[SEN_ACT])
paso("X · (R2-1, C4 y C2) lo mismo con una sola línea genérica («Loss on lease termination») para los dos, y con solo la amortización «fuera» citando el deterioro",
     bloquean(rx2g) == ["F1-US-FILAS"] and bloquean(rx2m) == ["F1-US-FILAS"] and estado_tramo(rx2m, "amortizacion_rou") == "insuficiente", f"{bloquean(rx2g)} · {bloquean(rx2m)}")
rx2d = ev_(LX, con_citas(L_ACT), verdad=("no", "no"), wc=WC_SIN, fuera=[SEN_ACT, SEN_PAS])
gx2d = g(rx2d, "F1-US-FILAS")[0]
paso("X · (R2-1) una cita que es un TROZO de una línea ajena («Operating lease liabilities» dentro de «Gain on termination of operating lease liabilities») tampoco vale",
     bloquean(rx2d) == ["F1-US-FILAS"] and gx2d["efecto"] == "INCOMPLETO" and "dentro de una línea que nombra el arrendamiento junto a otra cosa" in gx2d["detalle"]
     and estado_tramo(rx2d, "variacion_pasivo") == "insuficiente", gx2d["detalle"][:220])
rx2p = ev_(LX, con_citas("right-of-use assets", ub_pas="no_publicada"), verdad=("no", "no"), wc=WC_SIN, fuera=[SEN_PARTIDA])
paso("X · (R2-1) …ni la cita tomada del último renglón de una etiqueta partida cuyo primer renglón dice «Impairment»", bloquean(rx2p) == ["F1-US-FILAS"]
     and estado_tramo(rx2p, "amortizacion_rou") == "insuficiente", g(rx2p, "F1-US-FILAS")[0]["detalle"][:200])
rx2e = ev_(LX0, decl("A2_propio"), verdad=("fuera", "fuera"), fuera=[L_AM, L_PAS, SEN_GEN, SEN_ACT])
paso("X · (R2-1) control: con las líneas reales de los dos tramos (no sumadas) y además dos líneas ajenas, «fuera» citando las reales sigue CONTRASTADA y sin condición (68)",
     rx2e["utilizable_para_conclusion"] and rx2e.get("condicionada") is None and estado_tramo(rx2e, "amortizacion_rou") == "contrastada"
     and estado_tramo(rx2e, "variacion_pasivo") == "contrastada" and cerca(F0(rx2e), 68), str(bloquean(rx2e)))
rx2h = ev_(LX0, decl("A2_propio"), verdad=("fuera", "fuera"), wc=list(WC) + [SEN_PAS], fuera=[L_AM, L_PAS])
paso("X · (R2-1) control: la línea real del pasivo no está sumada y la fase 1 sí sumó en la fila 14 una línea AJENA que contiene las mismas palabras («Gain on "
     "termination of operating lease liabilities»): «fuera» sigue contrastada (la ajena no es «la línea citada» ni nombra el tramo)", rx2h["utilizable_para_conclusion"]
     and rx2h.get("condicionada") is None and estado_tramo(rx2h, "variacion_pasivo") == "contrastada" and estado_tramo(rx2h, "amortizacion_rou") == "contrastada",
     f"{bloquean(rx2h)} · {estado_tramo(rx2h, 'variacion_pasivo')}")
rx2f = ev_(libro_v631(libro(da=30.0, capex=30.0, palancas=False), "A2_propio", 0.0), con_citas(SEN_ACT), verdad=("no", "fuera"), fuera=[SEN_ACT, L_PAS])
paso("X · (R2-1, C5) el error a la baja también se cierra: amortización dentro de una D&A que no la nombra, declarada «fuera» con la línea de deterioro → bloquea",
     bloquean(rx2f) == ["F1-US-FILAS"], str(bloquean(rx2f)))
NO_TRAMO = ("Impairment of operating lease right-of-use assets", "Impairment of long-lived assets and operating lease right-of-use assets", "Loss on lease termination",
            "Gain on lease modification", "Gain on termination of operating lease liabilities", "Lease termination costs", "Lease incentives received",
            "Amortization of lease incentives", "Operating lease abandonment charges", "Lease exit costs", "Deterioro de derechos de uso",
            "Resultado por cancelación de arrendamientos", "Write-off of right-of-use assets", "Gain on sale and leaseback of leased assets")
SI_TRAMO = {"Operating lease liabilities": {"pasivo"}, "Operating lease right-of-use assets": {"activo"}, "Non-cash lease expense": {"activo"},
            "Amortization of operating lease right-of-use assets": {"activo"}, "Operating leases, net": {"activo", "pasivo"},
            "Reduction in the carrying amount of right-of-use assets": {"activo"}, "Variación de pasivos por arrendamiento": {"pasivo"}}
paso("X · (R2-1, C6) catorce rótulos habituales que nombran el arrendamiento junto a otra cosa: ninguno cuenta como tramo (_lados vacío); los de los tramos, como antes",
     all(M._ajena(M._nlin(t)) and not M._lados(M._nlin(t)) for t in NO_TRAMO) and all(M._lados(M._nlin(t)) == v and not M._ajena(M._nlin(t)) for t, v in SI_TRAMO.items()),
     str([t for t in NO_TRAMO if M._lados(M._nlin(t))] + [t for t, v in SI_TRAMO.items() if M._lados(M._nlin(t)) != v]))
paso("X · (R2-1) _lineas_logicas: una etiqueta partida es una sola línea; una cabecera con dos puntos no se une a la línea siguiente",
     [t for t, _ in M._lineas_logicas("Changes in operating assets and liabilities:\nImpairment of long-lived assets and operating lease\n   right-of-use assets   19   20\n"
                                      "Accounts receivable   (5)   (6)\n")]
     == ["changes in operating assets and liabilities:", "impairment of long-lived assets and operating lease right-of-use assets 19 20", "accounts receivable (5) (6)"])

# ---- R2-2 · el importe declarado dentro de una fila frente a la cifra impresa de su línea
rd1 = ev_(LX, decl("A2_propio", ub_pas="fila_14", ajuste=10), verdad=("fuera", "fila_14"))
paso("X · (R2-2, D1) VERAZ: la variación del pasivo es una línea propia sumada en la fila 14 (impreso «(10)» → +10 en la fila) y se declara con su importe 10: "
     "contrastada, también el importe; sigue el límite F1-LIBRO (nada más bloquea)", bloquean(rd1) == ["F1-LIBRO"] and estado_tramo(rd1, "variacion_pasivo") == "contrastada"
     and rd1["us_gaap"]["contraste_de_ubicaciones"]["importe_sin_contrastar"] == [], str(bloquean(rd1)))
rd2 = ev_(LX, decl("A2_propio", ub_pas="fila_14", ajuste=0), verdad=("fuera", "fila_14"))
gd2 = g(rd2, "F1-US-FILAS")[0]
paso("X · (R2-2, D2) la misma línea con importe declarado 0: DATOS INVÁLIDOS («el importe dentro de la fila es el de su línea»); antes, utilizable sin condición con 78",
     bloquean(rd2) == ["F1-US-FILAS"] and gd2["efecto"] == "DATOS INVÁLIDOS" and estado_tramo(rd2, "variacion_pasivo") == "contradicha"
     and "el importe dentro de la fila es el de su línea" in gd2["detalle"] and "'(10)'" in gd2["detalle"] and rd2["K3"]["K3b_contrastado"] is False, gd2["detalle"][:260])
rd3 = ev_(LX, decl("A2_propio", ub_pas="fila_14", ajuste={**{y: 10 for y in ANIOS[-5:]}, 2024: 9}), verdad=("fuera", "fila_14"))
paso("X · (R2-2) no solo el cero: un importe distinto del impreso en un solo año (9 en 2024) también es DATOS INVÁLIDOS, y el mensaje dice el año",
     bloquea(rd3, "F1-US-FILAS") and g(rd3, "F1-US-FILAS")[0]["efecto"] == "DATOS INVÁLIDOS" and "en 2024" in g(rd3, "F1-US-FILAS")[0]["detalle"])
LXa = libro_v631(libro(dwc=-10.0, palancas=False), "A2_propio", 0.0)
rd4 = ev_(LXa, decl("A2_propio", ub_am="fila_14", ajuste=-10), verdad=("fila_14", "fuera"))
rd4b = ev_(LXa, decl("A2_propio", ub_am="fila_14", ajuste=0), verdad=("fila_14", "fuera"))
paso("X · (R2-2) lo mismo con la amortización como línea propia de la fila 14 (impreso «10» → −10): con −10, contrastada (F1-LIBRO); con 0, DATOS INVÁLIDOS",
     bloquean(rd4) == ["F1-LIBRO"] and estado_tramo(rd4, "amortizacion_rou") == "contrastada" and bloquea(rd4b, "F1-US-FILAS")
     and g(rd4b, "F1-US-FILAS")[0]["efecto"] == "DATOS INVÁLIDOS" and estado_tramo(rd4b, "amortizacion_rou") == "contradicha", f"{bloquean(rd4)} · {bloquean(rd4b)}")
dmx = decl("A2_propio", ub_pas="fila_14", ajuste=0)
OP_(dmx)["variacion_pasivo"]["cita"] = "accrued liabilities, operating lease"
rmx = ev_(LX, dmx, verdad=("fuera", "no"), wc=list(WC) + [NIKE_PAS], fuera=[L_AM])
paso("X · (R2-2) el pasivo va dentro de una línea MEZCLADA de la fila 14 (la etiqueta de Nike) y se declara con importe 0: la ubicación está contrastada, pero el importe "
     "no se puede comparar con una cifra → CONDICIONADA, con los pagos como cota (−12 cubre el error de +10); K3b no dice «contrastado»",
     rmx["utilizable_para_conclusion"] and rmx["condicionada"]["hipotesis"] == "F1-US-FILAS" and estado_tramo(rmx, "variacion_pasivo") == "sin_contrastar"
     and rmx["us_gaap"]["contraste_de_ubicaciones"]["importe_sin_contrastar"] == ["variacion_pasivo"] and min(cotas(rmx).values()) <= -12 + 1e-9
     and rmx["K3"]["K3b_contrastado"] is False and any("los pagos menos el importe declarado" in k for k in cotas(rmx)), f"{bloquean(rmx)} · {cotas(rmx)}")
rd6 = ev_(LX, decl("A2_propio", ub_pas="fila_14", ajuste=0), verdad=("fuera", "fila_14"), partes=False)
paso("X · (R2-2, D2b) sin fase1_partes, «fila_14» con importe 0: condicionada como antes, pero ahora la cota cubre el error (−12; antes, 0)",
     rd6["utilizable_para_conclusion"] and rd6["condicionada"] and min(cotas(rd6).values()) <= -12 + 1e-9 and cerca(F0(rd6), 78), str(sorted(cotas(rd6).values())))
rd6a = ev_(LXa, decl("A2_propio", ub_am="fila_14", ajuste=0), verdad=("fila_14", "fuera"), partes=False)
paso("X · (R2-2) …y lo mismo al revés con la amortización (el error es a la baja, −10): la cota al alza es el coste lineal (+12); aquí además salta K3c (la "
     "reinversión media sale negativa), que es la regla general", rd6a["condicionada"] and max(cotas(rd6a).values()) >= 12 - 1e-9 and cerca(F0(rd6a), 58)
     and bloquean(rd6a) in ([], ["F1-K3c"]), f"{bloquean(rd6a)} · {sorted(cotas(rd6a).values())}")
rd7 = ev_(LX, decl("A2_propio", ub_pas="fila_14", ajuste=10), verdad=("fuera", "fila_14"), importes={L_PAS: "(10,000)"}, unidad="miles")
rd7b = ev_(LX, decl("A2_propio", ub_pas="fila_14", ajuste=10), verdad=("fuera", "fila_14"), importes={L_PAS: "(10,000)"})
paso("X · (R2-2) la cifra impresa se lleva a la escala del modelo con la unidad del informe (como la fase 1): «(10,000)» en miles es 10 (contrastada); en millones, no",
     bloquean(rd7) == ["F1-LIBRO"] and estado_tramo(rd7, "variacion_pasivo") == "contrastada" and bloquea(rd7b, "F1-US-FILAS")
     and estado_tramo(rd7b, "variacion_pasivo") == "contradicha", f"{bloquean(rd7)} · {bloquean(rd7b)}")
AM8 = "Amortization of operating lease right-of-use assets"
d8 = con_citas(AM8, ub_am="fila_8", a8=10)
r8 = ev_(libro_v631(libro(da=30.0, palancas=False), "A2_propio", 10.0), d8, verdad=("fila_8", "fuera"), da=[DA, AM8], importes={AM8: "10"})
d8b = con_citas(AM8, ub_am="fila_8", a8=15)
r8b = ev_(libro_v631(libro(da=30.0, palancas=False), "A2_propio", 15.0), d8b, verdad=("fila_8", "fuera"), da=[DA, AM8], importes={AM8: "10"})
paso("X · (R2-2) también en la fila 8 cuando la amortización es una línea PROPIA que la fase 1 sumó en la D&A: con su importe (10), contrastada y utilizable (68); "
     "con 15, DATOS INVÁLIDOS", r8["utilizable_para_conclusion"] and r8.get("condicionada") is None and cerca(F0(r8), 68) and bloquean(r8b) == ["F1-US-FILAS"]
     and g(r8b, "F1-US-FILAS")[0]["efecto"] == "DATOS INVÁLIDOS", f"{bloquean(r8)} · {bloquean(r8b)}")
r8c = ev_(libro_v631(libro(da=30.0, palancas=False), "A2_propio", 15.0), decl("A2_propio", ub_am="fila_8", a8=15), verdad=("fila_8", "fuera"))
paso("X · (R2-2, D3) LÍMITE declarado: con la amortización dentro de una D&A MEZCLADA (su línea la nombra pero su cifra es la de toda la D&A) un importe inflado (15 por "
     "10) no se puede comparar con una cifra impresa: sigue utilizable (73); es el mismo límite que NIIF con da_rou", r8c["utilizable_para_conclusion"]
     and estado_tramo(r8c, "amortizacion_rou") == "contrastada" and cerca(F0(r8c), 73), str(bloquean(r8c)))
# (cierre de la ronda 2, R2-2) la fila 8 puede llevar también la amortización de los financieros: una línea genérica del derecho de uso, o una que nombra
# los financieros, no tiene la cifra del tramo operativo y su importe no se compara (como el límite 11); una línea solo de los operativos, sí
LVf = libro_v631(libro(ebit=63.0, da=35.0, C70=62.0, C49=5.0, princ=5.0, palancas=False), "A2_propio", 15.0)
GEN8, OPFIN8 = "Amortization of right-of-use assets", "Amortization of operating and finance lease right-of-use assets"
rf8 = {etq: ev_(LVf, con_citas(etq, fin=True, rou_fin=5, fin_princ=5, ub_am="fila_8", a8=10), verdad=("fila_8", "fuera"), da=[DA, etq], importes={etq: "15"})
       for etq in (GEN8, OPFIN8)}
paso("X · (R2-2) declaración VERAZ con los financieros también dentro de la fila 8: la línea genérica «Amortization of right-of-use assets» (o la que nombra los "
     "operativos y los financieros) suma las dos amortizaciones (15 = 10 + 5); su cifra no es la del tramo operativo y el importe no se compara: utilizable (62), "
     "sin DATOS INVÁLIDOS; la línea que nombra los financieros cuenta como línea de su amortización (contrastada)",
     all(r["utilizable_para_conclusion"] and cerca(F0(r), 62) and estado_tramo(r, "amortizacion_rou") == "contrastada"
         and estado_tramo(r, "amortizacion_rou_financiero") == "contrastada" for r in rf8.values()),
     str({k[:24]: (bloquean(r), estado_tramo(r, "amortizacion_rou_financiero")) for k, r in rf8.items()}))
rf8b = ev_(libro_v631(libro(ebit=63.0, da=35.0, C70=62.0, C49=5.0, princ=5.0, palancas=False), "A2_propio", 20.0),
           con_citas(AM8, fin=True, rou_fin=5, fin_princ=5, ub_am="fila_8", a8=15), verdad=("fila_8", "fuera"), da=[DA, AM8], importes={AM8: "10"})
paso("X · (R2-2) control: con los financieros dentro de la fila 8, la línea que solo nombra los operativos sí se compara (15 declarado frente a 10 impreso → "
     "DATOS INVÁLIDOS)", bloquea(rf8b, "F1-US-FILAS") and g(rf8b, "F1-US-FILAS")[0]["efecto"] == "DATOS INVÁLIDOS", str(bloquean(rf8b)))
OPFIN14 = "Operating and finance lease liabilities"
rf14 = ev_(LX, con_citas(pas=OPFIN14, ub_pas="fila_14", ajuste=10), verdad=("fuera", "no"), wc=list(WC) + [OPFIN14], fuera=[L_AM], importes={OPFIN14: "(12)"})
paso("X · (R2-2) una línea de la fila 14 que nombra también los financieros («Operating and finance lease liabilities», impreso «(12)») no tiene la cifra del tramo "
     "operativo: el importe declarado (10) no se compara (no es DATOS INVÁLIDOS); la ubicación está contrastada y el importe no → condicionada; sigue el límite F1-LIBRO",
     bloquean(rf14) == ["F1-LIBRO"] and estado_tramo(rf14, "variacion_pasivo") == "sin_contrastar"
     and rf14["us_gaap"]["contraste_de_ubicaciones"]["importe_sin_contrastar"] == ["variacion_pasivo"], f"{bloquean(rf14)} · {estado_tramo(rf14, 'variacion_pasivo')}")
paso("X · (R2-2) _valor_en_la_fila sigue las reglas de la fase 1: «(28)» en la fila 14 es +28; «1,125» en miles en la fila 8 es 1,125; con signo −1 se invierte; lo "
     "que no es una cifra, o sin unidad válida, no se compara", M._valor_en_la_fila("circulante_lineas", {"impreso": "(28)"}, "millones") == 28
     and M._valor_en_la_fila("da", {"impreso": "1,125"}, "miles") == Fr(1125, 1000) and M._valor_en_la_fila("circulante_lineas", {"impreso": "(28)", "signo": -1}, "millones") == -28
     and M._valor_en_la_fila("da", {"impreso": "n/d"}, "millones") is None and M._valor_en_la_fila("da", {"impreso": "10"}, None) is None
     and M._valor_en_la_fila("da", {"impreso": "9,199,774"}, "unidades") == Fr(9199774, 10 ** 6))
paso("X · (R2-2) _linea_propia: solo las etiquetas que nombran únicamente el arrendamiento; las mezcladas (Nike, la D&A) y las que no lo nombran, no",
     all(M._linea_propia(t) for t in (L_PAS, L_ACT, L_AM, AM8, "Operating leases, net", "Change in operating lease assets and liabilities"))
     and not any(M._linea_propia(t) for t in (" ".join(NIKE_PAS), " ".join(NIKE_ACT), DA_ROU, DA, "Other assets and liabilities", "Accrued and other liabilities")))

# ---- R2-3 · financieros con la amortización del derecho de uso «dentro de la fila 8» por omisión
F_FIN = "Amortization of finance lease right-of-use assets"
LE = libro_v631(libro(ebit=68.0, da=20.0, C70=68.0, C49=5.0, princ=5.0, palancas=False), "A2_propio", 5.0)


def d_fin8():
    return decl("A2_propio", fin=True, rou_fin=5, fin_princ=5)


re1 = ev_(LE, d_fin8(), verdad=("fuera", "fuera"))
paso("X · (R2-3, E1) amortización del derecho de uso financiero dentro de la fila 8 por omisión y ninguna línea sumada la nombra: sigue utilizable (como NIIF 16), pero el "
     "tramo queda «por_omision», K3b dice «según lo declarado» y K3 no se presenta como conforme",
     re1["utilizable_para_conclusion"] and estado_tramo(re1, "amortizacion_rou_financiero") == "por_omision" and re1["K3"]["K3b_contrastado"] is False
     and "según lo declarado" in re1["K3"]["K3b_fundamento"] and re1["K3"]["conforme"] is None and estado_tramo(re1, "amortizacion_rou") == "contrastada",
     f"{bloquean(re1)} · {re1['K3']['K3b_fundamento'][:60]}")
re2 = ev_(LE, d_fin8(), verdad=("fuera", "fuera"), fuera=[L_AM, L_PAS, F_FIN])
ge2 = g(re2, "F1-US-FILAS")[0]
paso("X · (R2-3, E2) …y si el estado de flujos la muestra en una línea propia que la fase 1 NO sumó en la fila 8, manda el dato: DATOS INVÁLIDOS, y el mensaje dice "
     "cómo declararla («fuera_de_la_fila_8»); antes, utilizable sin condición con +5", bloquean(re2) == ["F1-US-FILAS"] and ge2["efecto"] == "DATOS INVÁLIDOS"
     and estado_tramo(re2, "amortizacion_rou_financiero") == "contradicha" and "fuera_de_la_fila_8" in ge2["detalle"] and "Amortization of finance lease" in ge2["detalle"],
     ge2["detalle"][:240])
re4 = ev_(libro_v631(libro(ebit=68.0, da=25.0, capex=20.0, C70=68.0, C49=5.0, princ=5.0, palancas=False), "A2_propio", 5.0), d_fin8(), verdad=("fuera", "fuera"),
          da=["Depreciation and amortization, including amortization of finance lease assets"])
paso("X · (R2-3, E4) control: si la línea de la D&A que la fase 1 sumó la nombra, queda contrastada y K3b dice «contrastado» (68)", re4["utilizable_para_conclusion"]
     and estado_tramo(re4, "amortizacion_rou_financiero") == "contrastada" and re4["K3"]["K3b_contrastado"] is True and cerca(F0(re4), 68), str(bloquean(re4)))
re5 = ev_(LE, d_fin8(), verdad=("fuera", "fuera"), partes=False)
re6 = ev_(LE, d_fin8(), verdad=("fuera", "fuera"), da=[DA, F_FIN])
paso("X · (R2-3) sin fase1_partes queda «por_omision» (no se ha contrastado); y si la línea propia SÍ está entre las sumadas en la fila 8, contrastada (no hay contradicción)",
     estado_tramo(re5, "amortizacion_rou_financiero") == "por_omision" and "sin fase1_partes" in re5["us_gaap"]["contraste_de_ubicaciones"]["tramos"]["amortizacion_rou_financiero"]["motivo"]
     and estado_tramo(re6, "amortizacion_rou_financiero") == "contrastada" and not bloquea(re6, "F1-US-FILAS"))
paso("X · (R2-3) con D-WM (como deuda) o con la amortización declarada fuera de la fila 8 no hay tramo «por omisión»: nada cambia",
     "amortizacion_rou_financiero" not in ev_(L1, d_wm())["us_gaap"]["contraste_de_ubicaciones"]["tramos"])

# ---- R2-4 · notas de texto dentro de «series» y valores vacíos
dN4 = copy.deepcopy(dN)
dN4["series"]["pagos_arrendamiento_sin_declarar"] = "vacío: el estado de flujos los publica en dos líneas (interés y principal), no en una"
rN4 = ev_(LN, dN4)
paso("X · (R2-4) una nota de texto dentro de «series», en una clave que no es una serie (la declaración real de Jumbo), ya no es DATOS INVÁLIDOS: se admite, queda a la "
     "vista (INFORMA) y el resultado es el de la declaración sin la nota", bloquean(rN4) == bloquean(rN) and rN4["utilizable_para_conclusion"] == rN["utilizable_para_conclusion"]
     and rN4.get("notas_en_series") == ["pagos_arrendamiento_sin_declarar"] and rN4["calculo_perimetro_declarado"] == rN["calculo_perimetro_declarado"]
     and [x["severidad"] for x in g(rN4, "F1-DECLARACION")] == ["INFORMA"] and "pagos_arrendamiento_sin_declarar" in g(rN4, "F1-DECLARACION")[0]["detalle"]
     and "notas_en_series" not in rN, str(bloquean(rN4)))
dN5 = copy.deepcopy(dN)
dN5["series"]["da_rou"] = "no la publica"
rN5 = ev_(LN, dN5)
paso("X · (R2-4) un texto en el lugar de una SERIE conocida sigue siendo DATOS INVÁLIDOS, y el mensaje dice exactamente dónde se escribe una nota",
     bloquea(rN5, "F1-DECLARACION") and "«nota»" in g(rN5, "F1-DECLARACION")[0]["detalle"] and "una clave que no sea el nombre de una serie" in g(rN5, "F1-DECLARACION")[0]["detalle"],
     g(rN5, "F1-DECLARACION")[0]["detalle"][:200])
dN6 = copy.deepcopy(dN)
dN6["series"]["otra_cosa"] = [1, 2]
paso("X · (R2-4) lo que no es un texto ni un objeto (una lista con contenido) en una clave desconocida de «series» tampoco se admite", bloquea(ev_(LN, dN6), "F1-DECLARACION"))


def con(d, **k):
    x = copy.deepcopy(d)
    x.update(k)
    return x


paso("X · (R2-4) vacío = sin declarar: «normalizacion» con [], \"\" o 0 se toma como vacía, como antes de la ronda 2 (la revisión contó 3 formas que pasaban de utilizable "
     "a bloqueada); con contenido y sin ser un objeto, DATOS INVÁLIDOS", all(bloquean(ev_(LN, con(dN, normalizacion=v))) == bloquean(rN) for v in ([], "", 0))
     and bloquea(ev_(LN, con(dN, normalizacion="x")), "F1-DECLARACION") and bloquea(ev_(LN, con(dN, normalizacion=[1])), "F1-DECLARACION"))
dU4 = decl("A2_propio", fin=True, rou_fin=5, fin_princ=5, ub_am="fila_8", a8=10)
dU4n = copy.deepcopy(dU4)
dU4n["series"]["nota_del_examen"] = "texto libre"
paso("X · (R2-4) la nota tampoco estorba al escribir el libro V6.3.1 (f1_libro_v631.celdas da las mismas celdas)", V631.celdas(dU4n, ANIOS) == V631.celdas(dU4, ANIOS))

# ---- «Otro» en Control maestro L4: límite del modelo, no falta de datos
LO = libro(l4="Otro")
rO1 = ev_(LO, dN)
paso("X · («Otro») libro con «Otro» en Control maestro L4 y una declaración completa: F1-NORMA es un LÍMITE DEL MODELO (F1 solo tiene reglas para NIIF y US GAAP), no un "
     "dato que falte → «no_entregable · limite_del_modelo» (antes: pendiente_de_datos)", bloquea(rO1, "F1-NORMA") and g(rO1, "F1-NORMA")[0]["efecto"] == "MODELO NO APLICABLE"
     and rO1["estado_propuesto"] == "no_entregable · limite_del_modelo" and "no un dato que falte" in g(rO1, "F1-NORMA")[0]["detalle"], rO1["estado_propuesto"])
rO2 = M.evaluar(LO, {})
paso("X · («Otro») …también sin declaración: faltan datos, pero ninguno arregla la norma; manda el límite del modelo", len(bloquean(rO2)) > 1
     and rO2["estado_propuesto"] == "no_entregable · limite_del_modelo", f"{bloquean(rO2)[:4]} · {rO2['estado_propuesto']}")
rO3 = M.evaluar(libro(l4="Otro", motor="B", fila23=50.0), {}, carpeta=t415)
paso("X · («Otro») con el motor B en un expediente de la 4.15 (se exige F1 porque no se puede descartar US GAAP): límite del modelo, ya no pendiente_de_datos",
     rO3["aplica"] is True and bloquean(rO3) == ["F1-NORMA"] and rO3["estado_propuesto"] == "no_entregable · limite_del_modelo", rO3["estado_propuesto"])
rO4 = ev_(libro(l4="U.S. GAAP"), dN)
paso("X · («Otro») control: un texto fuera de la lista («U.S. GAAP») sigue siendo un dato mal escrito → DATOS INVÁLIDOS, pendiente_de_datos",
     g(rO4, "F1-NORMA")[0]["efecto"] == "DATOS INVÁLIDOS" and rO4["estado_propuesto"] == "pendiente_de_datos")

# ---- R2-6 · F1-US-C49 «explicado»: el texto distingue el sentido de la diferencia
dE6f = decl("A2_propio", fin=True, rou_fin=5, fin_princ=FP6)
dE6f["conciliacion_fcf_base"] = [{"componente": "C49", "importe": 0.166667, "partida": "principal pagado en diciembre y registrado en otra partida de la caja base",
                                  "fuente": {"documento": DOC, "pagina": 1}}]
rE6f = ev_(libro(ebit=63.0, da=25.0, C70=61.5, C49=5.5, princ=PR6), dE6f)
paso("X · (R2-6) C49 por DEBAJO del principal publicado y la diferencia explicada: el aviso pide comprobar que el principal que falta está restado en esa partida (se "
     "omitiría), no que «no son pagos operativos»; por encima, sigue pidiendo lo segundo", g(rE6f, "F1-US-C49")[0]["severidad"] == "AVISO"
     and "se omitiría" in g(rE6f, "F1-US-C49")[0]["detalle"] and "pagos de arrendamientos operativos" not in g(rE6f, "F1-US-C49")[0]["detalle"]
     and "los contaría dos veces" in g(rE6d, "F1-US-C49")[0]["detalle"], g(rE6f, "F1-US-C49")[0]["detalle"][-170:])

# ================================================================== V631 · libro V6.3.1 F1: la fila 86 lleva financieros + operativos dentro de la fila 8
dV = decl("A2_propio", fin=True, rou_fin=5, fin_princ=5, ub_am="fila_8", a8=10)
cel = V631.celdas(dV, ANIOS)
paso("V631 · celdas: la fila 86 del libro lleva la suma (5 financieros + 10 operativos dentro de la fila 8 = 15) y su procedencia nombra las dos series",
     cel["Historia!C85"] == "A2_propio" and all(cel[f"Historia!{c}86"] == 15.0 for c in COLS) and "da_rou + series.da_rou_operativo" in cel["Historia!M86"])
dV0 = decl("A2_propio", fin=True, rou_fin=5, fin_princ=5)
paso("V631 · celdas: sin operativos dentro de la fila 8 la fila 86 es la de los financieros (5); con una ubicación sin declarar queda VACÍA (vacío ≠ 0)",
     all(V631.celdas(dV0, ANIOS)[f"Historia!{c}86"] == 5.0 for c in COLS)
     and all(V631.celdas(decl("A2_propio", fin=True, rou_fin=5, ub_am=None), ANIOS)[f"Historia!{c}86"] is None for c in COLS))
dNi = copy.deepcopy(dN)
dNi["perimetro_reinversion"]["valor"] = "A1_sin_ROU"
dNi["series"]["da_rou"] = serie(7)
dNi.pop("fuentes_series", None)
paso("V631 · celdas con NIIF: la fila 86 sigue siendo series.da_rou (sin cambio)", all(V631.celdas(dNi, ANIOS)[f"Historia!{c}86"] == 7.0 for c in COLS)
     and V631.celdas(dNi, ANIOS)["Historia!M86"].startswith("motor_a_f1.json · series.da_rou (documento"))
paso("V631 · celdas con la amortización financiera declarada fuera de la fila 8 (R16): la fila 86 no la lleva (0), y D_X del libro no excluye nada",
     all(V631.celdas(d16(), ANIOS)[f"Historia!{c}86"] == 0.0 for c in COLS))
# EBIT 63 (el coste lineal y la amortización financiera ya están dentro); fila 8 = 20 propia + 5 financiera + 10 operativa = 35; FCF base 62
LV = libro_v631(libro(ebit=63.0, da=35.0, C70=62.0, C49=5.0, princ=5.0, palancas=False), "A2_propio", 15.0)
rV = ev_(LV, dV)
paso("V631 · el libro V6.3.1 tal cual calcula el caso «operativos dentro de la fila 8 + financieros» con A2 (62 = FCF base): F1-LIBRO no salta y nada bloquea (utilizable)",
     not salta(rV, "F1-LIBRO") and rV["libro_v631_f1"]["motivos"] == [] and rV["utilizable_para_conclusion"] and not salta(rV, "F1-REPLICA") and cerca(F0(rV), 62)
     and "condicionada" not in rV, f"{bloquean(rV)} · {rV.get('libro_v631_f1')}")
LVm = dict(LV, **{"Historia!L86": 5.0})
paso("V631 · si la fila 86 del libro no es la suma declarada (solo los financieros en 2025) → F1-LIBRO bloquea (el oráculo compara la serie)",
     bloquea(ev_(LVm, dV), "F1-LIBRO"))
LVh = libro_v631(libro(palancas=False), "A2_propio", 0.0)
rVh = ev_(LVh, decl("A2_propio", ub_am="no_publicada", ub_pas="no_publicada"))
paso("V631 · caso habitual con D-US1 (tramos no publicados) y A2 en el libro V6.3.1 tal cual: calculable, utilizable y CONDICIONADO",
     rVh["utilizable_para_conclusion"] and "CONDICIONADA" in rVh["rotulo"] and not salta(rVh, "F1-LIBRO") and cerca(F0(rVh), 68), str(bloquean(rVh)))
LV6 = libro_v631(libro(dwc=10.0, palancas=False), "A2_propio", 0.0)
rV6 = ev_(LV6, decl("A2_propio", ub_pas="fila_14", ajuste=10))
paso("V631 · variación del pasivo en la fila 14: el libro V6.3.1 no retira nada del circulante → F1-LIBRO bloquea (f del libro ≠ capa) y es lo único que bloquea",
     bloquean(rV6) == ["F1-LIBRO"] and "retirada del circulante" in g(rV6, "F1-LIBRO")[0]["detalle"] and cerca(F0(rV6), 68) and not salta(rV6, "F1-REPLICA"), str(bloquean(rV6)))
LV7 = libro_v631(libro(dwc=1.0, C70=67.0, palancas=False), "A2_propio", 0.0)
rV7 = ev_(LV7, decl("A2_propio", ub_am="fila_14", ub_pas="fila_14", P=13, Lc=12))
paso("V631 · D-US2 bis en el libro V6.3.1 tal cual (caso Nike): el libro calcula lo declarado (F1-LIBRO no salta); 68 con el coste contable y −1 contando los pagos",
     bloquean(rV7) == [] and not salta(rV7, "F1-LIBRO") and cerca(F0(rV7), 68)
     and cerca(rV7["us_gaap"]["D_US2_bis"]["contando_los_pagos"]["variacion_maxima_del_flujo_sin_crecimiento_mm"], -1.0), str(bloquean(rV7)))

# ================================================================== G13 · con crecimiento e impuestos
V13 = [1000 * 1.05 ** i for i in range(10)]
dao = [0.02 * v for v in V13]
cap = [dao[i] + 0.5 * (V13[i] - (V13[i - 1] if i else V13[0] / 1.05)) for i in range(10)]
eb = [0.10 * v for v in V13]                                   # margen después del alquiler operativo (coste = pago = 3 % de las ventas)
fcf = [eb[i] * 0.75 + dao[i] - cap[i] for i in range(10)]      # CFO − capex: el pago ya está dentro del CFO
P13, A13, PR13 = ({y: 0.03 * V13[i] for i, y in enumerate(ANIOS)}, {y: 0.025 * V13[i] for i, y in enumerate(ANIOS)}, {y: 0.025 * V13[i] for i, y in enumerate(ANIOS)})
caja0 = 0.075 * V13[-1]
L13 = libro(ventas=V13, ebit=eb, da=dao, tau=0.25, capex=cap, C70=sum(fcf[-3:]) / 3)
r13 = ev_(L13, decl("A2_propio", P=P13, Lc=P13), con_fuentes=False)
paso("G13 · crecimiento 5 % y τ 25 %, tramos fuera: A2 da la caja sostenible a crecimiento cero (7,5 % de las ventas del año base); ancla S2C = 2,0",
     cerca(F0(r13), caja0, 1e-6) and cerca(r13["calculo_perimetro_declarado"]["ancla_s2c_E4"], 2.0), f"{F0(r13):.6f} frente a {caja0:.6f}")
L13a = libro(ventas=V13, ebit=eb, da=[dao[i] + A13[y] for i, y in enumerate(ANIOS)], tau=0.25, capex=cap, C70=sum(fcf[-3:]) / 3)
r13a = ev_(L13a, decl("A2_propio", P=P13, Lc=P13, ub_am="fila_8", a8=A13), con_fuentes=False)
paso("G13 · con la amortización operativa (2,5 % de las ventas) dentro de la fila 8: A2 da la misma caja; A0 la infravalora en esa amortización a la escala del año base",
     cerca(F0(r13a), caja0, 1e-6) and cerca(caja0 - F0(r13a, "A0_total"), sum(A13[y] for y in ANIOS[-3:]) / sum(V13[-3:]) * V13[-1], 1e-6)
     and cerca(r13a["calculo_perimetro_declarado"]["ancla_s2c_E4"], 2.0))
L13b = libro(ventas=V13, ebit=eb, da=dao, tau=0.25, capex=cap, dwc=[PR13[y] for y in ANIOS], C70=sum(fcf[-3:]) / 3)
r13b = ev_(L13b, decl("A2_propio", P=P13, Lc=P13, ub_pas="fila_14", ajuste=PR13), con_fuentes=False)
f_libro = L13b["Historia!C58"]
paso("G13 · con la variación del pasivo (2,5 % de las ventas) sola en la fila 14: retirada, A2 da la caja sostenible y el ancla 2,0; el libro tal cual la sobrevaloraría en ese importe",
     cerca(F0(r13b), caja0, 1e-6) and cerca(r13b["calculo_perimetro_declarado"]["ancla_s2c_E4"], 2.0)
     and cerca(V13[-1] * (0.075 - f_libro) - caja0, sum(PR13[y] for y in ANIOS[-3:]) / sum(V13[-3:]) * V13[-1], 1e-6))
L14 = libro(tau=0.25, C70=51.0)
r14 = ev_(L14, decl("A0_total"))
paso("G13 · estable con τ 25 %: EBIT 68, impuesto 17, FCF base 51 → A0 da 51; utilizable", cerca(F0(r14), 51) and r14["utilizable_para_conclusion"])

# ================================================================== NIIF · no cambia
paso("NIIF · sin arrendamientos ni PPA: A0 = la V6.3; utilizable; mismas guardas que antes (ninguna F1-US-*)", rN["utilizable_para_conclusion"] and cerca(F0(rN), 68)
     and rN["K3"]["K3b_alquiler_contado"] == "ninguna vez (sin arrendamientos)" and "K3b_por_clase" not in rN["K3"] and "K3b_fundamento" not in rN["K3"]
     and "conforme_nota" not in rN["K3"] and rN["K3"]["conforme"] is True)
LNi = libro(ebit=70.0, da=30.0, C70=68.0, C49=10.0, princ=10.0, c48=2.0, l4="IFRS")
dNa = copy.deepcopy(dN)
dNa["perimetro_reinversion"]["valor"] = "A1_sin_ROU"
dNa["perimetro_palancas_s2c"]["valor"] = dNa["perimetro_roic"]["valor"] = "A1_sin_ROU"
dNa["series"]["da_rou"] = serie(10)
dNa["conciliacion_fcf_base"] = [{"componente": "C48", "importe": -2, "partida": "interés de caja de los arrendamientos dentro de C48", "fuente": {"documento": DOC, "pagina": 1}}]
rNa = ev_(LNi, dNa)
paso("NIIF · caso T5 (derecho de uso 10, principal en C49): A1 = 68 y A0 = 58; solo bloquea F1-LIBRO; K3b «una vez»; la versión de la capa nombra US GAAP",
     cerca(F0(rNa, "A1_sin_ROU"), 68) and cerca(F0(rNa, "A0_total"), 58) and bloquean(rNa) == ["F1-LIBRO"] and rNa["K3"]["K3b_alquiler_contado"] == "una vez"
     and "US GAAP" in rNa["version"], str(bloquean(rNa)))
paso("NIIF · rou_fila8 con NIIF es series.da_rou; un resultado NIIF no lleva bloque us_gaap, condición ni hipótesis", M.rou_fila8(dNa, ANIOS) == {y: Fr(10) for y in ANIOS}
     and "us_gaap" not in rNa and "condicionada" not in rNa and "hipótesis" not in rNa["rotulo"])
paso("NIIF · el rótulo de un resultado utilizable es, letra por letra, el de antes", rN["rotulo"] == "motor A utilizable para una conclusión según F1 (condición necesaria, no "
     "suficiente; no apto para dinero real)")

# ================================================================== EX · exigencia, vigencia y gancho del pipeline
tmp = tempfile.mkdtemp(prefix="f1_us_ex_")
TMP.append(tmp)
paso("EX · con el motor A, un libro US GAAP exige F1 aunque no muestre arrendamientos (C49 = 0, filas 17 y 23 a cero); uno NIIF sin arrendamientos, no",
     M.exigido(tmp, L=libro()) and not M.exigido(tmp, L=libro(l4="IFRS")) and not M.arrendamientos_en_el_libro(libro()))
paso("EX · con el motor B, F1 se exige solo con US GAAP (por el libro o por la declaración): exigido_puente", M.exigido_puente(tmp, L=libro(motor="B"))
     and not M.exigido_puente(tmp, L=libro(l4="IFRS", motor="B")))


def escribir_xlsx(L, ruta):
    import openpyxl
    wb = openpyxl.Workbook()
    for h in ("Historia", "Análisis", "Palancas", "Motor", "Diagnóstico V6", "Control maestro"):
        wb.create_sheet(h)
    for k_, v_ in L.items():
        if "!" in k_:
            h, c = k_.split("!")
            wb[h][c] = v_
    wb.save(ruta)


def xlsx_textos_compartidos(ruta, l4):
    """Un .xlsx mínimo cuyo Control maestro L4 es un TEXTO COMPARTIDO (t="s" con su índice en sharedStrings.xml), como los libros que recalcula LibreOffice."""
    import zipfile
    ns = 'xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"'
    partes = {
        "[Content_Types].xml": '<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
                               '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/>'
                               '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
                               '<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
                               '<Override PartName="/xl/sharedStrings.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sharedStrings+xml"/></Types>',
        "_rels/.rels": '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                       '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>',
        "xl/workbook.xml": f'<?xml version="1.0" encoding="UTF-8"?><workbook {ns} xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
                           '<sheets><sheet name="Control maestro" sheetId="1" r:id="rId1"/></sheets></workbook>',
        "xl/_rels/workbook.xml.rels": '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                                      '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>'
                                      '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/sharedStrings" Target="sharedStrings.xml"/></Relationships>',
        "xl/worksheets/sheet1.xml": f'<?xml version="1.0" encoding="UTF-8"?><worksheet {ns}><sheetData><row r="4"><c r="K4" t="s"><v>0</v></c><c r="L4" t="s"><v>1</v></c></row></sheetData></worksheet>',
        "xl/sharedStrings.xml": f'<?xml version="1.0" encoding="UTF-8"?><sst {ns} count="2" uniqueCount="2"><si><t>Norma contable</t></si><si><t>{l4}</t></si></sst>'}
    with zipfile.ZipFile(ruta, "w") as z:
        for n_, x in partes.items():
            z.writestr(n_, x)


def cli(c, libro_, motor=None, origen=None):
    return subprocess.run([sys.executable, "-B", os.path.join(PV, "scripts", "motor_a_f1.py"), "evaluar", c, "--libro", libro_]
                          + (["--motor", motor] if motor else []) + (["--libro-origen", origen] if origen else []), capture_output=True, text=True)


try:
    import cierre_v2 as CIE
    from v63_xml import LibroV63
    c = os.path.join(tmp, "EmpresaUS")
    os.makedirs(os.path.join(c, "recalc"))
    pl_b, pl_b0 = os.path.join(tmp, "b.xlsx"), os.path.join(tmp, "b0.xlsx")
    escribir_xlsx(LB, pl_b)
    escribir_xlsx(libro(fila22=100.0, fila23=0.0, motor="B"), pl_b0)
    ev_libro = os.path.join(c, "EmpresaUS_v63_evaluada.xlsx")
    shutil.copy(pl_b, ev_libro)
    # (R1-1) en un libro con textos compartidos (los que recalcula LibreOffice) el lector ligero devuelve el ÍNDICE del texto, no el texto
    cs = os.path.join(tmp, "EmpresaLO")
    os.makedirs(os.path.join(cs, "recalc"))
    pl_s = os.path.join(cs, "recalc", "EmpresaLO_v63_evaluada.xlsx")
    xlsx_textos_compartidos(pl_s, "US GAAP")
    crudo = LibroV63(pl_s).leer("Control maestro", "L4")
    paso("R1 · (revisión R1-1) L4 de un libro con textos compartidos: LibroV63.leer devuelve el índice del texto («1», no «US GAAP»: así se perdía la norma); la norma del "
         "expediente se lee resolviendo el texto → US_GAAP, y F1 se exige con el motor B", crudo == "1" and M.norma_del_libro({"Control maestro!L4": crudo}) is None
         and M._l4_del_libro(pl_s) == "US GAAP" and M.norma_del_expediente(cs) == ("US_GAAP", True) and M.us_gaap_del_expediente(cs) and M.exigido_puente(cs, libro=pl_s)
         and M.vigencia(cs, motor="B")["exigido"] is True, f"LibroV63.leer → {crudo!r}")
    xlsx_textos_compartidos(pl_s, "IFRS")
    paso("R1 · …y con «IFRS» como texto compartido el motor B sigue sin exigir F1", M.norma_del_expediente(cs) == ("NIIF", True) and not M.exigido_puente(cs, libro=pl_s))
    open(pl_s, "wb").write(b"no es un xlsx")
    json.dump({"modo": "registrada", "motivo": "expediente de la 4.15 (prueba)"}, open(os.path.join(cs, "entrada_efectiva.json"), "w"))
    paso("R1 · un libro que no se puede leer no dice su norma: en un expediente de la 4.15 con el motor B, F1 se exige", M.norma_del_expediente(cs) == (None, False)
         and M.exigido_puente(cs) and M.vigencia(cs, motor="B")["exigido"] is True)
    st = {"motor": "B", "estado_pendiente": "concluido", "historial": [], "paso": 12}
    json.dump(st, open(os.path.join(c, "estado_pipeline.json"), "w"))
    v0 = M.vigencia(c, motor="B")
    paso("EX · vigencia con el motor B y libro US GAAP: F1 exigido; sin evaluación, un cierre «concluido» se rechaza", v0["exigido"] is True and v0["vigente"] is False
         and "sin evaluación F1" in str(CIE.motivo_f1(c, st)), str(v0.get("motivo")))
    dB = decl("A0_total", pasivo=50)
    fuentes(dB, c)
    json.dump(dB, open(os.path.join(c, "motor_a_f1.json"), "w", encoding="utf-8"))
    rc = cli(c, pl_b, "B", ev_libro)
    vb = M.vigencia(c, motor="B")
    paso("EX · CLI con el motor B y el pasivo operativo en la fila 23: código 4 (límite del modelo); vigente y no utilizable; el cierre «concluido» se rechaza",
         rc.returncode == 4 and vb["vigente"] is True and vb["utilizable"] is False and "concluido" in str(CIE.motivo_f1(c, st)), f"código {rc.returncode} · {rc.stdout.strip()[-100:]}")
    shutil.copy(pl_b0, ev_libro)
    dB0 = decl("A0_total", pasivo=0)
    fuentes(dB0, c)
    json.dump(dB0, open(os.path.join(c, "motor_a_f1.json"), "w", encoding="utf-8"))
    rc = cli(c, pl_b0, "B", ev_libro)
    paso("EX · con la fila 23 sin pasivo operativo: código 0; vigente y utilizable; el cierre no tiene objeción F1; sin el motor en el estado se toma del resultado (B)",
         rc.returncode == 0 and M.vigencia(c, motor="B")["utilizable"] is True and CIE.motivo_f1(c, st) is None and M.vigencia(c)["motor"] == "B",
         f"código {rc.returncode} · {rc.stdout.strip()[-100:]}")
    json.dump(dict(st, motor="B"), open(os.path.join(c, "estado_pipeline.json"), "w"))
    cn = os.path.join(tmp, "EmpresaNIIF")
    os.makedirs(cn)
    escribir_xlsx(libro(l4="IFRS", motor="B"), os.path.join(cn, "EmpresaNIIF_v63_evaluada.xlsx"))
    paso("EX · vigencia con el motor B y libro NIIF: no exigido («el motor no es el A»), como antes", M.vigencia(cn, motor="B")["exigido"] is False
         and M.vigencia(cn, motor="B")["motivo"] == "el motor no es el A" and CIE.motivo_f1(cn, {"motor": "B", "estado_pendiente": "concluido"}) is None)
    json.dump({"modo": "registrada", "motivo": "expediente de la 4.15 (prueba)"}, open(os.path.join(cn, "entrada_efectiva.json"), "w"))
    paso("EX · …también si ese expediente NIIF es de la 4.15 (el libro dice una norma reconocida)", M.vigencia(cn, motor="B")["exigido"] is False)
    # (R1-1) motor B en un expediente de la 4.15 cuyo libro no dice una norma de la lista: vigencia, cierre y gancho exigen F1
    cu = os.path.join(tmp, "EmpresaUSmal")
    os.makedirs(cu)
    pl_u = os.path.join(cu, "EmpresaUSmal_v63_evaluada.xlsx")
    escribir_xlsx(libro(fila22=100.0, fila23=50.0, motor="B", l4="U.S. GAAP"), pl_u)
    json.dump({"modo": "registrada", "motivo": "expediente de la 4.15 (prueba)"}, open(os.path.join(cu, "entrada_efectiva.json"), "w"))
    stu = {"motor": "B", "estado_pendiente": "concluido", "historial": [], "paso": 12}
    json.dump(stu, open(os.path.join(cu, "estado_pipeline.json"), "w"))
    vu = M.vigencia(cu, motor="B")
    paso("R1 · vigencia y cierre con el motor B y un libro «U.S. GAAP» en la 4.15: F1 exigido; sin evaluación no se confirma un cierre «concluido» (antes: «el motor no es el A»)",
         vu["exigido"] is True and vu["vigente"] is False and "motor B · F1" in str(CIE.motivo_f1(cu, stu)), str(CIE.motivo_f1(cu, stu))[:160])
    # el gancho del pipeline, ejecutado: Pipeline.motor_a_f1 con el motor B
    import pipeline as PL
    fin_ = []
    Pp = PL.Pipeline.__new__(PL.Pipeline)
    Pp.c, Pp.E, Pp.st = c, "EmpresaUS", {"motor": "B", "historial": [], "paso": 7}
    Pp.estado_path = os.path.join(tmp, "estado_pipeline_prueba.json")
    Pp.terminar = lambda estado, tipo, detalle, paso_, **k: fin_.append((estado, tipo, paso_, detalle))
    t0 = Pp.motor_a_f1(pl_b0, 7)
    paso("EX · gancho del pipeline con el motor B y US GAAP: evalúa el puente y deja seguir cuando es utilizable", t0 is False and not fin_
         and (Pp.st.get("motor_a_f1") or {}).get("bloquea") is False)
    shutil.copy(pl_b, ev_libro)
    fuentes(dB, c)
    json.dump(dB, open(os.path.join(c, "motor_a_f1.json"), "w", encoding="utf-8"))
    t4 = Pp.motor_a_f1(pl_b, 7)
    paso("EX · gancho con el motor B y pasivo operativo en la fila 23: termina en no_entregable · limite_del_modelo y el detalle nombra el motor B",
         t4 is True and fin_[-1][:2] == ("no_entregable", "limite_del_modelo") and "motor B · F1" in fin_[-1][3] and "F1-US-PUENTE" in fin_[-1][3], str(fin_[-1:])[:200])
    os.remove(os.path.join(c, "motor_a_f1.json"))
    n_fin = len(fin_)
    t5 = Pp.motor_a_f1(pl_b, 7)
    paso("R1 · (revisión XB3) gancho con el motor B, libro US GAAP (textos compartidos) y SIN declaración F1: se ejecuta y termina en pendiente_de_datos (antes: no se evaluaba)",
         t5 is True and len(fin_) == n_fin + 1 and fin_[-1][0] == "pendiente_de_datos" and "F1-NORMA" in fin_[-1][3], str(fin_[-1:])[:220])
    json.dump(dN, open(os.path.join(c, "motor_a_f1.json"), "w", encoding="utf-8"))
    t6 = Pp.motor_a_f1(pl_b, 7)
    paso("R1 · (revisión XB4) gancho con el motor B, libro US GAAP y una declaración que dice NIIF: se ejecuta y F1-NORMA bloquea por mezcla de normas",
         t6 is True and fin_[-1][0] == "pendiente_de_datos" and "mezcla de normas" in fin_[-1][3], str(fin_[-1:])[:220])
    Pp.c, Pp.E = cu, "EmpresaUSmal"
    t7 = Pp.motor_a_f1(pl_u, 7)
    paso("R1 · (revisión G1) gancho con el motor B y un libro «U.S. GAAP» en la 4.15: se ejecuta y F1-NORMA bloquea (pendiente_de_datos)",
         t7 is True and fin_[-1][0] == "pendiente_de_datos" and "F1-NORMA" in fin_[-1][3], str(fin_[-1:])[:200])
    Pp.c, Pp.E = cn, "EmpresaNIIF"
    paso("EX · gancho con el motor B y NIIF: no actúa (como antes)", Pp.motor_a_f1(os.path.join(cn, "EmpresaNIIF_v63_evaluada.xlsx"), 7) is False)
    # CLI con el motor A
    ca = os.path.join(tmp, "EmpresaUSA")
    os.makedirs(ca)
    pl_a, pl_a6, pl_a7 = os.path.join(tmp, "a.xlsx"), os.path.join(tmp, "a6.xlsx"), os.path.join(tmp, "a7.xlsx")
    escribir_xlsx(L1, pl_a)
    escribir_xlsx(L6, pl_a6)
    escribir_xlsx(L7, pl_a7)
    for nombre, d_, lib, esperado, kw in (("U1 utilizable", decl("A0_total"), pl_a, 0, {}), ("desglose ausente", decl("A0_total", us=False), pl_a, 3, {}),
                                          ("ajuste del circulante que ningún libro calcula", decl("A0_total", ub_pas="fila_14", ajuste=10), pl_a6, 4, {}),
                                          ("ubicación contradicha por las líneas de la fase 1", decl("A0_total"), pl_a6, 3, {"verdad": ("fuera", "fila_14")}),
                                          ("D-US2 bis (valor de la hoja)", decl("A0_total", ub_am="fila_14", ub_pas="fila_14", P=13, Lc=12), pl_a7, 0, {}),
                                          ("hipótesis D-US1", decl("A0_total", ub_am="no_publicada", ub_pas="no_publicada"), pl_a, 0, {})):
        shutil.rmtree(os.path.join(ca, "fase1_partes"), ignore_errors=True)
        expediente(d_, carpeta=ca, **kw)
        json.dump(d_, open(os.path.join(ca, "motor_a_f1.json"), "w", encoding="utf-8"))
        rc = cli(ca, lib, "A")
        md = open(os.path.join(ca, M.RESULTADO_MD), encoding="utf-8").read() if os.path.exists(os.path.join(ca, M.RESULTADO_MD)) else ""
        paso(f"CLI · motor A · {nombre}: código {esperado}; el informe .md lleva la sección de US GAAP", rc.returncode == esperado and "## US GAAP (ASC 842)" in md,
             f"código {rc.returncode} · {rc.stdout.strip()[-110:]}")
        if nombre.startswith("D-US2 bis"):
            paso("CLI · con D-US2 bis la salida dice que el valor es el de la hoja (coste contable) y cuánto cambiaría contando los pagos", "D-US2 bis" in rc.stdout
                 and "coste contable" in rc.stdout and "-1.000 mm" in rc.stdout, rc.stdout.strip()[-200:])
    paso("CLI · con la hipótesis D-US1 la salida dice CONDICIONADA y da la cota; el informe .md lleva la sección «Conclusión condicionada»", "CONDICIONADA" in rc.stdout
         and "cota:" in rc.stdout and "## Conclusión condicionada" in md and "**D-US1**" in md, rc.stdout.strip()[-160:])
finally:
    for t in TMP:
        shutil.rmtree(t, ignore_errors=True)

n_ok = sum(ok for _, ok in R)
print(f"\n{n_ok}/{len(R)} pruebas del motor A F1 con US GAAP PASAN")
sys.exit(0 if n_ok == len(R) else 1)
