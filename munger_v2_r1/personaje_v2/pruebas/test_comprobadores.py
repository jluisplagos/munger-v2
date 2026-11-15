#!/usr/bin/env python3
"""Pruebas de los comprobadores reparados (contrato de reparación H1–H3, 8-nov-2026).

Uso: python3 pruebas/test_comprobadores.py [h2 …]     (sin argumentos: todas las partes disponibles)
Sale con 0 si todas las comprobaciones PASAN; 1 si alguna FALLA. Escribe pruebas/resultado_comprobadores.json.

H2 · pipeline.Pipeline.veredicto_auditoria
  - casos sintéticos 1–14 del contrato con su resultado esperado;
  - las auditorías reales de empresas_v2/*/auditoria.md: APROBADO y SHA-256 idéntico antes y después de leerlas;
  - documentación: ninguna regla antigua («FALLA en 1, 4, 11, 12 o 16» como única condición) vigente en los documentos.
"""
import glob
import hashlib
import json
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(RAIZ, "scripts"))
resultados = []


def paso(parte, nombre, ok, detalle=""):
    resultados.append({"parte": parte, "prueba": nombre, "ok": bool(ok), "detalle": detalle})
    print(("PASA " if ok else "FALLA") + f" · {parte} · {nombre}" + (f" · {detalle}" if detalle else ""))


# ------------------------------------------------------------------------------------------------------------------ H2
def h2():
    import pipeline
    V = pipeline.Pipeline.veredicto_auditoria
    P = {n: f"{n}. PASA · prueba {n}" for n in range(1, 17)}

    def aud(lineas, veredicto="APROBADO"):
        return "\n".join(lineas) + f"\nVeredicto: {veredicto}\n"

    todos = [P[n] for n in range(1, 17)]
    casos = [
        ("1 solo «Veredicto: APROBADO»", "Veredicto: APROBADO\n", "REPETIR"),
        ("2 «8. FALLA · hecho material inventado» + APROBADO", "8. FALLA · hecho material inventado\nVeredicto: APROBADO\n", "REPETIR"),
        ("3a FALLA en el punto 1 + APROBADO", "1. FALLA · verificar_v63.py no íntegro\nVeredicto: APROBADO\n", "REPETIR"),
        ("3b FALLA en el punto 11 + APROBADO", "11. FALLA · rango sin hecho propio\nVeredicto: APROBADO\n", "REPETIR"),
        ("3c FALLA en el punto 16 + APROBADO", "16. FALLA · faltan datos ausentes por revisar\nVeredicto: APROBADO\n", "REPETIR"),
        ("4 auditoría vacía", "", "REPETIR"),
        ("5 «APROBADO con reservas»", aud(todos, "APROBADO con reservas"), "REPETIR"),
        ("6 dos veredictos", aud(todos) + "Veredicto: REPETIR\n", "REPETIR"),
        ("7 16 puntos, FALLA en el 8, APROBADO", aud([P[n] if n != 8 else "8. FALLA · hecho material inventado" for n in range(1, 17)]), "REPETIR"),
        ("8 16 puntos, FALLA en los 11 no bloqueantes, APROBADO",
         aud([P[n] if n in (1, 4, 11, 12, 16) else f"{n}. FALLA · prueba {n}" for n in range(1, 17)]), "REPETIR"),
        ("9 16 puntos, todos PASA, APROBADO", aud(todos), "APROBADO"),
        ("10 16 puntos con el 5 duplicado", aud(todos + ["5. PASA · prueba 5 repetida"]), "REPETIR"),
        ("11 15 puntos (falta el 12)", aud([P[n] for n in range(1, 17) if n != 12]), "REPETIR"),
        ("12 16 puntos PASA, veredicto REPETIR", aud(todos, "REPETIR"), "REPETIR"),
        ("13 16 puntos PASA, el 7 con «Aviso: …»", aud([P[n] if n != 7 else "7. PASA · tesis con hechos. Aviso: una cifra sin página" for n in range(1, 17)]), "APROBADO"),
        ("14 16 puntos PASA, «FALLA» en el texto del 6", aud([P[n] if n != 6 else "6. PASA · ninguna cita FALLA en el corpus" for n in range(1, 17)]), "REPETIR"),
        # variantes de formato que el lector admite (marcas de markdown alrededor del número o del estado)
        ("15 16 puntos PASA en negrita («**1.** PASA», «2. **PASA**»), APROBADO",
         aud([f"**{n}.** PASA · prueba {n}" if n % 2 else f"{n}. **PASA** · prueba {n}" for n in range(1, 17)]), "APROBADO"),
        ("16 punto 17 adicional", aud(todos + ["17. PASA · punto que no existe"]), "REPETIR"),
        # cierre de H2 (revisión externa de la entrega 1): encabezados con estado o numeración inválidos
        ("17 encabezado «17. PENDIENTE · revisión pendiente»", aud(todos + ["17. PENDIENTE · revisión pendiente"]), "REPETIR"),
        ("18 encabezado «8. PENDIENTE · hecho material sin comprobar»", aud(todos + ["8. PENDIENTE · hecho material sin comprobar"]), "REPETIR"),
        ("19 encabezado «100. PASA · punto fuera del rango»", aud(todos + ["100. PASA · punto fuera del rango"]), "REPETIR"),
        ("20 encabezado «(17) PASA»", aud(todos + ["(17) PASA · otro"]), "REPETIR"),
        ("21 encabezado «8) PASA» (separador inválido)", aud(todos + ["8) PASA · otro"]), "REPETIR"),
        ("22 encabezado «**17.** PASA»", aud(todos + ["**17.** PASA · otro"]), "REPETIR"),
        ("23 encabezado «8 PENDIENTE»", aud(todos + ["8 PENDIENTE · otro"]), "REPETIR"),
        ("24 encabezado «8 – PENDIENTE»", aud(todos + ["8 – PENDIENTE · otro"]), "REPETIR"),
        ("25 encabezado «0. PASA»", aud(todos + ["0. PASA · otro"]), "REPETIR"),
        ("26 lista numerada tras «Veredicto: APROBADO»", aud(todos) + "1. Corregir B102\n", "REPETIR"),
        ("27 cifras legítimas de la evidencia en líneas de continuación",
         aud([P[n] if n != 7 else ("7. PASA · tesis inversa con hechos:\n   1.036 mm de circulante liberado (Historia fila 14)\n"
                                   "   2016: −238 · 2017: −66 · 2021: −410\n   14,6 accidentes por millón de horas\n   3.463 empleados\n"
                                   "   12:30 cierre de la junta\n   - 2016. Año de la caída de márgenes\n   -238 en 2016 y -66 en 2017")
              for n in range(1, 17)]), "APROBADO"),
    ]
    for nombre, txt, esperado in casos:
        obtenido = V(txt)
        paso("H2", f"caso {nombre}", obtenido == esperado, f"esperado {esperado} · obtenido {obtenido}")

    reales = sorted(glob.glob(os.path.join(RAIZ, "empresas_v2", "*", "auditoria.md")))
    paso("H2", "hay seis auditorías reales", len(reales) == 6, f"{len(reales)} encontradas")
    for f in reales:
        antes = hashlib.sha256(open(f, "rb").read()).hexdigest()
        v = V(open(f, encoding="utf-8").read())
        despues = hashlib.sha256(open(f, "rb").read()).hexdigest()
        paso("H2", f"auditoría real {os.path.relpath(f, RAIZ)}", v == "APROBADO" and antes == despues,
             f"veredicto {v} · SHA-256 {'idéntico' if antes == despues else 'CAMBIADO'} ({antes[:12]}…)")

    # documentación: la regla antigua no puede quedar vigente; solo se admite citada como sustituida o descartada
    antiguas = [r"Un FALLA en 1, 4, 11, 12 o 16 es REPETIR", r"Un FALLA en \(1\), \(4\), \(11\), \(12\) o \(16\) es REPETIR",
                r"sin FALLA en 1/4/11/12/16", r"dentro de un punto 1/4/11/12/16", r"ningún punto 1, 4, 11, 12 o 16",
                r"ningún FALLA en 1, 4, 11, 12 o 16", r"FALLA en 1, 4, 11, 12 o 16"]
    docs = [os.path.join(RAIZ, x) for x in ("prompts/verificacion.md", "ANEXO_D_salidas_y_formatos.md", "DECISIONES.md", "ESTADO.md",
                                             "README_v2.md", "PROMPT_CLAUDE_CODE.md", "ENCARGO_personaje_v2.md", "scripts/pipeline.py")]
    vigentes = []
    for d in docs:
        if not os.path.exists(d):
            continue
        for i, l in enumerate(open(d, encoding="utf-8").read().splitlines(), 1):
            for pat in antiguas:
                for m in re.finditer(pat, l):
                    contexto = l[max(0, m.start() - 160): m.end() + 40].lower()
                    if not re.search(r"sustitu|descartad", contexto):
                        vigentes.append(f"{os.path.relpath(d, RAIZ)}:{i}")
    paso("H2", "documentación: ninguna regla antigua vigente", not vigentes, ", ".join(sorted(set(vigentes))) or "ninguna")
    pr = open(os.path.join(RAIZ, "prompts", "verificacion.md"), encoding="utf-8").read()
    ax = open(os.path.join(RAIZ, "ANEXO_D_salidas_y_formatos.md"), encoding="utf-8").read()
    paso("H2", "prompt y Anexo D enuncian la regla nueva y el «Aviso:»",
         "Cualquier punto en FALLA obliga a escribir `Veredicto: REPETIR`" in pr and "«Aviso:»" in pr
         and "cualquier FALLA es REPETIR sin excepción" in ax and "«Aviso: …»" in ax)

    # el generador sintético produce auditorías que el lector entiende
    import tempfile
    sys.path.insert(0, AQUI)
    import agentes_sinteticos as AG
    with tempfile.TemporaryDirectory() as t:
        AG.auditoria(t, "APROBADO")
        a = V(open(os.path.join(t, "auditoria.md"), encoding="utf-8").read())
        AG.auditoria(t, "REPETIR")
        r = V(open(os.path.join(t, "auditoria.md"), encoding="utf-8").read())
    paso("H2", "generador sintético: APROBADO → APROBADO y REPETIR → REPETIR", a == "APROBADO" and r == "REPETIR", f"{a} / {r}")


# ------------------------------------------------------------------------------------------------------------------ H1
def _empresa_ar(c, pagina, partidas_extra, unidad="millones"):
    """Carpeta mínima con texto/AR.txt (una página) y fase1_partes/AR_2025.json."""
    import shutil
    import fase1_historia as F
    shutil.rmtree(c, ignore_errors=True)
    os.makedirs(os.path.join(c, "texto"))
    os.makedirs(os.path.join(c, "fase1_partes"))
    open(os.path.join(c, "texto", "AR.txt"), "w", encoding="utf-8").write("[PDF PAGE 1]\n" + pagina + "\n")
    p = {k: {} for k in F.PARTIDAS}
    p.update(partidas_extra)
    json.dump({"anio": 2025, "archivo": "AR.txt", "unidad": unidad, "partidas": p},
              open(os.path.join(c, "fase1_partes", "AR_2025.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def h1():
    import subprocess
    import tempfile
    import fase1_historia as F

    def comp(imp, lin, signo=None, concepto=None):
        x = {"concepto": concepto or lin.rsplit(" ", 1)[0], "impreso": imp, "pagina": 1, "linea": lin}
        if signo is not None:
            x["signo"] = signo
        return x

    casos = [
        ("1", "Revenue 123", {"capex": {"actual": [comp("123", "Capital expenditure 123")]}}, "RECHAZADO"),
        ("2", "Revenue 123", {"capex": {"actual": [comp("123", "Revenue 123")]}}, "ACEPTADO"),          # L1 concepto
        ("3", "Revenue 91234", {"capex": {"actual": [comp("123", "Capital expenditure 123")]}}, "RECHAZADO"),
        ("3b", "Capital expenditure 91234", {"capex": {"actual": [comp("123", "Capital expenditure 91234", concepto="Capital expenditure")]}}, "RECHAZADO"),
        ("4", "2025 2024\nCapital expenditure 150 123", {"capex": {"actual": [comp("123", "Capital expenditure 150 123", concepto="Capital expenditure")]}}, "ACEPTADO"),  # L2
        ("5", "Amounts in thousands of EUR\nCapital expenditure 123", {"capex": {"actual": [comp("123", "Capital expenditure 123")]}}, "ACEPTADO"),  # L3
        ("6", "Proceeds from sale of businesses 40", {"adquisiciones": {"actual": [comp("40", "Proceeds from sale of businesses 40", signo=-1)]}}, "ACEPTADO"),  # L4
        ("7", "Revenue 123", {"capex": {"cero": {"motivo": "no hay capex", "pagina": 1}}}, "RECHAZADO"),
        ("7b", "Revenue 123", {"sbc": {"cero": {"motivo": "no hay plan", "pagina": 1, "cita": "The Group has no share-based payment programmes"}}}, "RECHAZADO"),
        ("8", "Revenue 123", {"capex": {"actual": [comp("999", "Capital expenditure 999")]}}, "RECHAZADO"),
        ("9", "Capital expenditure 123", {"capex": {"actual": [dict(comp("123", "Capital expenditure 123"), pagina=7)]}}, "RECHAZADO"),
        ("10", "Capital expenditure 123", {"capex": {"actual": [comp("123", "Capital expenditure 123")]}}, "ACEPTADO"),
        ("11", "Revenue 123", {"capex": {"cero": {"motivo": "x", "pagina": 9}}}, "RECHAZADO"),
        ("12", "The Group has no share-based payment programmes.", {"sbc": {"cero": {"motivo": "no hay plan de pagos en acciones", "pagina": 1, "cita": "The Group has no share-based payment programmes"}}}, "PENDIENTE"),
        ("13", "The Group has no defined benefit pension obligations.", {"sbc": {"cero": {"motivo": "no hay plan de pagos en acciones", "pagina": 1, "cita": "The Group has no defined benefit pension obligations"}}}, "PENDIENTE"),
    ]
    with tempfile.TemporaryDirectory() as t:
        for n, pag, extra, esperado in casos:
            c = os.path.join(t, f"caso_{n}")
            _empresa_ar(c, pag, extra)
            pend = []
            e = F.comprobar_anio(c, 2025, pend)
            obtenido = "RECHAZADO" if e else ("PENDIENTE" if pend else "ACEPTADO")
            paso("H1", f"caso {n}", obtenido == esperado, f"esperado {esperado} · obtenido {obtenido}" + (f" · {e[0]}" if e else ""))
        # la orden comprobar-anio: PENDIENTE no es error (código 0) y se imprime; un rechazo da código 1
        for n, cod in (("12", 0), ("7", 1)):
            r = subprocess.run([sys.executable, "-B", os.path.join(RAIZ, "scripts", "fase1_historia.py"), "comprobar-anio", os.path.join(t, f"caso_{n}"), "2025"],
                               capture_output=True, text=True)
            ok = r.returncode == cod and (("PENDIENTE: cero de sbc 2025" in r.stdout) if n == "12" else True)
            paso("H1", f"orden comprobar-anio caso {n}: código {cod}" + (" y línea PENDIENTE" if n == "12" else ""), ok, f"código {r.returncode} · {r.stdout.strip().splitlines()[-1][:120] if r.stdout.strip() else ''}")
        # preparar no vuelve a pedir un año solo por tener ceros pendientes (comprobar_anio sin errores)
        paso("H1", "un cero pendiente no es un error para preparar (lista de errores vacía)", F.comprobar_anio(os.path.join(t, "caso_12"), 2025) == [])

    # inventario de ceros heredados y conservación de los expedientes originales
    import csv
    inv = os.path.join(RAIZ, "empresas_v2_correcciones", "ceros_heredados_H1.csv")
    filas = list(csv.DictReader(open(inv, encoding="utf-8"))) if os.path.exists(inv) else []
    reales = []
    for f in sorted(glob.glob(os.path.join(RAIZ, "empresas_v2", "*", "fase1_partes", "AR_*.json"))):
        d = json.load(open(f, encoding="utf-8"))
        reales += [(os.path.relpath(f, os.path.join(RAIZ, "empresas_v2")), k) for k, p in (d.get("partidas") or {}).items() if isinstance(p, dict) and p.get("cero")]
    paso("H1", "inventario de ceros heredados: 134 filas, las mismas que los AR_*.json",
         len(filas) == 134 and sorted((x["archivo_extraccion"], x["partida"]) for x in filas) == sorted(reales)
         and all(x["estado"] == "pendiente de verificación (heredado, sin cita)" for x in filas), f"{len(filas)} filas · {len(reales)} ceros en los AR")
    base = os.path.join(AQUI, "linea_base", "manifiesto_empresas_v2_base.sha256")
    distintos = []
    for l in open(base, encoding="utf-8"):
        h, p = l.rstrip("\n").split("  ", 1)
        q = os.path.join(RAIZ, p)
        if not os.path.exists(q) or hashlib.sha256(open(q, "rb").read()).hexdigest() != h:
            distintos.append(p)
    paso("H1", "expedientes originales de empresas_v2/ intactos (SHA-256 de la base)", not distintos, f"{len(distintos)} distintos" + (f": {distintos[:3]}" if distintos else ""))
    # ningún script escribe fase1_decisiones.json (solo una persona)
    escriben = []
    for f in glob.glob(os.path.join(RAIZ, "scripts", "*.py")) + glob.glob(os.path.join(RAIZ, "scripts", "*.sh")):
        texto = open(f, encoding="utf-8").read()
        # variables que guardan la ruta de fase1_decisiones.json (p. ej. dec_p): abrirlas en «w»/«a» también es escribir
        for var in set(re.findall(r"(\w+)\s*=\s*[^=\n]*fase1_decisiones", texto)):
            for i, l in enumerate(texto.splitlines(), 1):
                if re.search(r"open\(\s*" + re.escape(var) + r"""\s*,\s*["'][wa]b?["']""", l):
                    escriben.append(f"{os.path.basename(f)}:{i}")
        for i, l in enumerate(texto.splitlines(), 1):
            # escribir = abrir ese archivo en modo «w»/«a» o redirigir la salida de la shell hacia él
            if re.search(r"""open\(.*fase1_decisiones.*,\s*["'][wa]b?["']""", l) or re.search(r">>?\s*\S*fase1_decisiones", l) \
                    or re.search(r"""fase1_decisiones[^,)]*["']\s*\)\s*\.write_text""", l):
                escriben.append(f"{os.path.basename(f)}:{i}")
    paso("H1", "ningún script escribe fase1_decisiones.json", not escriben, ", ".join(escriben) or "ninguno")
    # tabla de dependencias de las celdas de Análisis (cierre de H1): un cero pendiente en la ventana hace pendiente la celda
    an = list(range(2016, 2026))
    def parts(**kw):
        return {k: {"valores": [1] * 10, "pendientes_verificacion": v} for k, v in kw.items()}
    esperados = [("C50", parts(sbc=[2024]), [2024]), ("C50", parts(sbc=[2021]), []), ("C33", parts(deuda=[2025]), [2025]), ("C33", parts(deuda=[2024]), []),
                 ("C24", parts(caja=[2021]), [2021]), ("C24", parts(caja=[2020]), []), ("C26", parts(beneficio_neto=[2023]), [2023]),
                 ("C28", parts(acciones_diluidas=[2020]), [2020]), ("C46", parts(sbc=[2025]), []), ("C24", parts(tipo_impositivo=[2025]), [2025])]
    malos = [(c, k, F.pendientes_celda(c, k, an, 3), e) for c, k, e in esperados if F.pendientes_celda(c, k, an, 3) != e]
    paso("H1", "tabla de dependencias: C24, C26, C28, C33 y C46–C50 heredan el pendiente solo dentro de su ventana", not malos, str(malos[:2]) if malos else "10 casos")
    pr = open(os.path.join(RAIZ, "prompts", "historia_anio.md"), encoding="utf-8").read()
    paso("H1", "prompt de extracción: cita obligatoria, pendiente y prohibición de escribir decisiones",
         '"cita": "..."' in pr and "pendiente de verificación" in pr and "No escribas nunca `fase1_decisiones.json`" in pr
         and "comprueba que cada `impreso` está en su `linea` y que la `linea` está en su página. Corrige hasta que pase." not in pr)


# ------------------------------------------------------------------------- H1 · recorrido completo (LibreOffice, ~1 min)
ANIOS = list(range(2016, 2026))
ETIQ = {"ventas": "Revenue", "ebit": "Operating profit", "da": "Depreciation and amortisation", "beneficio_neto": "Profit for the year",
        "impuestos": "Income tax expense", "bai": "Profit before tax", "cfo": "Cash flows from operating activities",
        "capex": "Purchase of property plant and equipment", "adquisiciones": "Acquisition of subsidiaries", "circulante_lineas": "Change in working capital",
        "intereses": "Finance costs", "intereses_financiacion": "Interest paid", "arrendamientos_principal": "Repayment of lease liabilities",
        "sbc": "Share-based payment expense", "id": "Research and development costs", "acciones_diluidas": "Diluted number of shares",
        "patrimonio": "Total equity", "deuda": "Borrowings", "arrendamientos": "Lease liabilities", "caja": "Cash and cash equivalents",
        "pensiones": "Pension obligations", "minoritarios": "Non-controlling interests"}
CITA_SBC = "The Group has no share-based payment programmes"
CITA_ADQ = "No business combinations took place during the year"


def _empresa_sintetica_fase1(c, con_ceros=True, metadatos_analisis=None):
    """Empresa X con informes en texto/ y extracciones AR_<año>.json construidas desde esquema/fase1_v63.ejemplo.json.
    Ceros con cita (PENDIENTES): sbc 2023–2025 (entran en la media de C50) y adquisiciones 2017 (fuera de toda media)."""
    import shutil
    import fase1_historia as F
    ej = json.load(open(os.path.join(RAIZ, "esquema", "fase1_v63.ejemplo.json"), encoding="utf-8"))
    hp = ej["historia"]["partidas"]
    for sub in ("texto", "fase1_partes"):   # solo estas subcarpetas: etapa1/ (la V5.3 de preparar) se conserva
        shutil.rmtree(os.path.join(c, sub), ignore_errors=True)
        os.makedirs(os.path.join(c, sub))
    for i, a in enumerate(ANIOS):
        val = {k: (hp[k]["valores"][i] if k in hp else None) for k in ETIQ}
        val["bai"] = hp["beneficio_neto"]["valores"][i] / 0.75
        val["impuestos"] = val["bai"] * 0.25
        val["circulante_lineas"] = -hp["circulante"]["valores"][i]   # el estado de flujos imprime el efecto en caja
        lineas, partidas = [], {k: {} for k in F.PARTIDAS}
        for k, et in ETIQ.items():
            if con_ceros and ((k == "sbc" and a >= 2023) or (k == "adquisiciones" and a == 2017)):
                continue
            imp = f"{val[k]:.2f}"
            lineas.append(f"{et} {imp}")
            partidas[k] = {"actual": [{"concepto": et, "impreso": imp, "pagina": 1, "linea": f"{et} {imp}"}], "anterior": None, "cero": None, "nota": None}
        if con_ceros and a >= 2023:
            lineas.append(CITA_SBC + ".")
            partidas["sbc"] = {"actual": None, "anterior": None, "cero": {"motivo": "no hay plan de pagos en acciones", "pagina": 1, "cita": CITA_SBC}, "nota": None}
        if con_ceros and a == 2017:
            lineas.append(CITA_ADQ + ".")
            partidas["adquisiciones"] = {"actual": None, "anterior": None, "cero": {"motivo": "no hubo adquisiciones", "pagina": 1, "cita": CITA_ADQ}, "nota": None}
        open(os.path.join(c, "texto", f"AR_{a}.txt"), "w", encoding="utf-8").write("[PDF PAGE 1]\nConsolidated statements (EUR million)\n" + "\n".join(lineas) + "\n")
        json.dump({"anio": a, "archivo": f"AR_{a}.txt", "fecha_cierre": f"{a}-12-31", "moneda": "EUR", "unidad": "millones", "reexpresion": None, "partidas": partidas},
                  open(os.path.join(c, "fase1_partes", f"AR_{a}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump({str(a): f"AR_{a}.txt" for a in ANIOS}, open(os.path.join(c, "fase1_fuentes.json"), "w", encoding="utf-8"))
    meta = {k: ej.get(k) for k in ("empresa", "ticker", "fecha_analisis", "sector_texto", "moneda_modelo", "norma_contable", "cierre_fiscal", "mercado",
                                   "ratio_adr", "sector_damodaran", "precio", "acciones_diluidas", "capitalizacion", "tasa_sin_riesgo", "geografia")}
    meta["anios_fcf_base"] = 3
    meta["analisis"] = {k: v for k, v in (ej.get("analisis") or {}).items() if k not in ("C46", "C47", "C48", "C49", "C50")}
    meta["analisis"].update(metadatos_analisis or {})
    json.dump(meta, open(os.path.join(c, "fase1_metadatos.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def _cm(libro):
    """{referencia de Control maestro (columna B): (F, N)} del libro."""
    import openpyxl
    ws = openpyxl.load_workbook(libro, read_only=True)["Control maestro"]
    out = {}
    for row in ws.iter_rows(min_row=17, max_row=175, min_col=2, max_col=14, values_only=True):
        if isinstance(row[0], str) and "!" in row[0]:
            out[row[0]] = (row[4], row[12])
    return out


def h1_recorrido():
    import shutil
    import subprocess
    sys.path.insert(0, AQUI)
    import test_pipeline_sintetico as TS
    FH = os.path.join(RAIZ, "scripts", "fase1_historia.py")
    nombre = "EmpresaX_cero_pendiente"
    c = TS.preparar(nombre, quitar_etapa1=("C46", "C47", "C48", "C49", "C50"))
    f1_ruta = os.path.join(c, "fase1_v63.json")
    os.remove(f1_ruta)
    _empresa_sintetica_fase1(c)
    # 1. extracción → construir
    r = subprocess.run([sys.executable, "-B", FH, "construir", c], capture_output=True, text=True)
    paso("H1 recorrido", "construir termina (código 0) con los ceros pendientes", r.returncode == 0, r.stdout.strip()[-200:])
    if r.returncode != 0:
        return
    f1 = json.load(open(f1_ruta, encoding="utf-8"))
    H = f1["historia"]["partidas"]
    rv = open(os.path.join(c, "historia_revision.md"), encoding="utf-8").read()
    paso("H1 recorrido", "fase1_v63.json: sbc pendiente en 2023–2025 y adquisiciones en 2017; valores 0 conservados",
         H["sbc"].get("pendientes_verificacion") == [2023, 2024, 2025] and H["adquisiciones"].get("pendientes_verificacion") == [2017]
         and H["sbc"]["valores"][-3:] == [0, 0, 0] and len(f1.get("pendientes_verificacion", [])) == 4,
         f"sbc {H['sbc'].get('pendientes_verificacion')} · adquisiciones {H['adquisiciones'].get('pendientes_verificacion')} · {len(f1.get('pendientes_verificacion', []))} pendientes")
    paso("H1 recorrido", "C50 (media 2023–2025 de sbc) hereda el estado pendiente; C46–C49 no",
         f1["analisis"]["C50"].get("pendiente_verificacion") == [2023, 2024, 2025]
         and not any(f1["analisis"][x].get("pendiente_verificacion") for x in ("C46", "C47", "C48", "C49")))
    paso("H1 recorrido", "historia_revision.md: sección «Ceros pendientes de verificación» con los 4; ya no existe «Ceros con evidencia»",
         "## Ceros pendientes de verificación (cita sin contrastar)" in rv and rv.count(CITA_SBC) == 3 and CITA_ADQ in rv and "## Ceros con evidencia" not in rv)
    f1_pendiente = json.load(open(f1_ruta, encoding="utf-8"))
    # 2. pipeline completo con agentes simulados: Excel y controles posteriores
    rc, out = TS.correr(c, TS.reaccion_normal())
    st = TS.estado(c)
    paso("H1 recorrido", "el pipeline llega al final (paso 14) con estado final", rc == 0 and st.get("estado_analisis") is not None and st.get("paso") == 14,
         f"código {rc} · paso {st.get('paso')} · estado {st.get('estado_analisis')}")
    if st.get("paso") != 14:
        return
    libro_datos = os.path.join(c, f"{nombre}_v63_datos.xlsx")
    cm = _cm(libro_datos)
    dep = {"Historia!C18:L18": "sbc", "Historia!C13:L13": "adquisiciones", "Análisis!C50": "C50"}
    estados = {k: (cm.get(k) or (None, None))[0] for k in dep}
    notas = {k: str((cm.get(k) or (None, ""))[1] or "") for k in dep}
    paso("H1 recorrido", "Excel: las filas con cero pendiente y C50 quedan «Dato no verificable» con la explicación en N",
         all(v == "Dato no verificable" for v in estados.values()) and all("PENDIENTE DE VERIFICACIÓN" in n for n in notas.values()), json.dumps(estados, ensure_ascii=False))
    verif = [k for k, (fv, _) in cm.items() if fv == "Rellenado y verificado" and k in dep]
    paso("H1 recorrido", "ninguna celda que dependa de un cero pendiente está «Rellenado y verificado»", not verif, ", ".join(verif) or "ninguna")
    otras = {k: cm.get(k, (None,))[0] for k in ("Historia!C6:L6", "Historia!C11:L11", "Análisis!C46", "Análisis!C47")}
    paso("H1 recorrido", "las celdas sin ceros pendientes siguen «Rellenado y verificado»", all(v == "Rellenado y verificado" for v in otras.values()), json.dumps(otras, ensure_ascii=False))
    ent = json.load(open(os.path.join(c, "entrada_v63.json"), encoding="utf-8"))
    listados = [x.get("dato") for x in ent.get("necesarios_para_listo_provisional", [])]
    da = [x.get("dato") for x in json.load(open(os.path.join(c, "datos_ausentes.json"), encoding="utf-8"))]
    paso("H1 recorrido", "comprobar_entrada los lista como evidencias pendientes y pasan a datos_ausentes.json (revisión S-19 de la fase C)",
         all(f"evidencia {k}" in listados and f"evidencia {k}" in da for k in dep), f"listados: {[x for x in listados if str(x).startswith('evidencia')]}")
    fc = json.load(open(os.path.join(c, "fase_c.json"), encoding="utf-8"))
    revisados = [x.get("dato") for x in ((fc.get("revision_datos_ausentes") or {}).get("revisados") or [])]
    paso("H1 recorrido", "la fase C revisó cada uno (no se aprueban en silencio)", all(f"evidencia {k}" in revisados for k in dep), f"{len(revisados)} revisados")
    res = json.load(open(os.path.join(c, "resultados.json"), encoding="utf-8"))
    est_libro = str((res.get("estados") or {}).get("estado_libro_B266") or "")
    fi = json.load(open(os.path.join(c, "ficha.json"), encoding="utf-8"))
    paso("H1 recorrido", "el libro no queda «LISTO»: estado NO LISTO · evidencias incompletas, también en la ficha",
         est_libro.startswith("NO LISTO · evidencias incompletas") and str(fi.get("estado_libro", "")).startswith("NO LISTO · evidencias incompletas"),
         f"resultados: {est_libro!r} · ficha: {fi.get('estado_libro')!r}")
    vt = open(os.path.join(c, "verificacion_estado_libro.txt"), encoding="utf-8").read() if os.path.exists(os.path.join(c, "verificacion_estado_libro.txt")) else ""
    vt_ok = any("verificar_todo.sh" in x and "RESULTADO verificar_todo.sh: PASS" in x for x in st.get("historial", []))
    paso("H1 recorrido", "verificar_todo.sh admite el estado «evidencias incompletas» con las tres evidencias listadas por la entrada",
         vt_ok and "evidencias incompletas" in vt and all(f"evidencia {k}" in vt for k in dep), vt.strip().splitlines()[0][-160:] if vt.strip() else "sin archivo")
    dv = open(os.path.join(c, "datos_v63.md"), encoding="utf-8").read()
    paso("H1 recorrido", "datos_v63.md (lo que leen los agentes) muestra «Dato no verificable» y el aviso del cero pendiente", "PENDIENTE DE VERIFICACIÓN" in dv)

    # 3. P2 · de pendiente a confirmado por decisión humana, con reconstrucción
    base = os.path.join(c, f"{nombre}_v63_base.xlsx")
    rel = os.path.join(RAIZ, "scripts", "rellenar_fase1_v63.py")
    dec_p = os.path.join(c, "fase1_decisiones.json")
    malas = [
        ("sin fecha ni persona", {"valor_mm": 0, "fuente": f"AR_2025.txt p. 1: «{CITA_SBC}»"}),
        ("confirmado_por un agente", {"valor_mm": 0, "fuente": f"AR_2025.txt p. 1: «{CITA_SBC}»", "fecha": "2026-11-08", "confirmado_por": "Claude (agente de extracción)"}),
        ("fuente sin página", {"valor_mm": 0, "fuente": "informe anual", "fecha": "2026-11-08", "confirmado_por": "Persona responsable del proyecto"}),
    ]
    for etiqueta, d in malas:
        json.dump({"sbc": {"2025": d}}, open(dec_p, "w", encoding="utf-8"), ensure_ascii=False)
        r = subprocess.run([sys.executable, "-B", FH, "construir", c], capture_output=True, text=True)
        paso("H1 confirmación", f"decisión inválida ({etiqueta}) → construir se detiene y no confirma", r.returncode == 1 and "decisiones inválidas" in r.stdout, r.stdout.strip()[-160:])
    buenas = {str(a): {"valor_mm": 0, "fuente": f"AR_{a}.txt p. 1: «{CITA_SBC}» (revisada la página completa: no hay plan ni gasto por pagos en acciones)",
                       "fecha": "2026-11-08", "confirmado_por": "Persona responsable del proyecto"} for a in (2023, 2024, 2025)}
    json.dump({"sbc": buenas}, open(dec_p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    r = subprocess.run([sys.executable, "-B", FH, "construir", c], capture_output=True, text=True)
    f1c = json.load(open(f1_ruta, encoding="utf-8"))
    Hc = f1c["historia"]["partidas"]
    mismos = all(Hc[k]["valores"] == f1_pendiente["historia"]["partidas"][k]["valores"] for k in Hc)
    paso("H1 confirmación", "construir con la decisión válida: sbc deja de estar pendiente, queda registrada (persona, fecha, fuente) y adquisiciones 2017 sigue pendiente",
         r.returncode == 0 and not Hc["sbc"].get("pendientes_verificacion") and Hc["adquisiciones"].get("pendientes_verificacion") == [2017]
         and len(f1c.get("ceros_confirmados", [])) == 3 and all(x["confirmado_por"] == "Persona responsable del proyecto" and x["fecha"] == "2026-11-08" for x in f1c["ceros_confirmados"])
         and "Persona responsable del proyecto el 2026-11-08" in Hc["sbc"]["fuente"], r.stdout.strip()[-160:])
    paso("H1 confirmación", "la reconstrucción no cambia ninguna cifra de la Historia", mismos)
    paso("H1 confirmación", "C50 deja de estar pendiente", not f1c["analisis"]["C50"].get("pendiente_verificacion") and f1c["analisis"]["C50"]["valor"] == f1_pendiente["analisis"]["C50"]["valor"])
    nuevo = os.path.join(c, f"{nombre}_v63_datos_confirmado.xlsx")
    r = subprocess.run([sys.executable, "-B", rel, base, f1_ruta, nuevo], capture_output=True, text=True)
    cm2 = _cm(nuevo)
    paso("H1 confirmación", "rellenar con la decisión: sbc y C50 pasan a «Rellenado y verificado»; adquisiciones sigue «Dato no verificable»",
         r.returncode == 0 and cm2.get("Historia!C18:L18", (None,))[0] == "Rellenado y verificado" and cm2.get("Análisis!C50", (None,))[0] == "Rellenado y verificado"
         and cm2.get("Historia!C13:L13", (None,))[0] == "Dato no verificable",
         f"código {r.returncode} · sbc {cm2.get('Historia!C18:L18', (None,))[0]} · C50 {cm2.get('Análisis!C50', (None,))[0]} · adquisiciones {cm2.get('Historia!C13:L13', (None,))[0]}")
    rv2 = open(os.path.join(c, "historia_revision.md"), encoding="utf-8").read()
    paso("H1 confirmación", "historia_revision.md lista los 3 ceros como confirmados por decisión humana, con la cita original",
         "## Ceros confirmados por decisión humana" in rv2 and rv2.count("Persona responsable del proyecto, 2026-11-08") == 3)


# ------------------------------------------------- H1 · reutilización de libros y metadatos (casos A, B y C de la revisión)
def _valores(libro):
    """Valores de datos: Historia C5:L26 y Análisis C24, C26, C28, C33, C46–C50."""
    import openpyxl
    wb = openpyxl.load_workbook(libro, read_only=True)
    out = {}
    for r, row in enumerate(wb["Historia"].iter_rows(min_row=5, max_row=26, min_col=3, max_col=12, values_only=True), 5):
        for j, v in enumerate(row):
            out[f"Historia!{'CDEFGHIJKL'[j]}{r}"] = v
    an = wb["Análisis"]
    for ref in ("C24", "C26", "C28", "C33", "C46", "C47", "C48", "C49", "C50"):
        out[f"Análisis!{ref}"] = an[ref].value
    return out


def _difs(a, b, salvo=()):
    def ig(x, y):
        if isinstance(x, (int, float)) and isinstance(y, (int, float)):
            return abs(x - y) <= 1e-9 * max(1.0, abs(x), abs(y))
        return x == y
    return sorted(k for k in set(a) | set(b) if k not in salvo and not ig(a.get(k), b.get(k)))


def h1_reutilizacion():
    import shutil
    import subprocess
    sys.path.insert(0, AQUI)
    import test_pipeline_sintetico as TS
    FH = os.path.join(RAIZ, "scripts", "fase1_historia.py")
    REL = os.path.join(RAIZ, "scripts", "rellenar_fase1_v63.py")
    nombre = "EmpresaX_reutilizacion"
    c = TS.preparar(nombre, quitar_etapa1=("C46", "C47", "C48", "C49", "C50"))
    f1p = os.path.join(c, "fase1_v63.json")

    def construir(con_ceros, meta_an=None, decisiones=None):
        _empresa_sintetica_fase1(c, con_ceros=con_ceros, metadatos_analisis=meta_an)
        dp = os.path.join(c, "fase1_decisiones.json")
        if os.path.exists(dp):
            os.remove(dp)
        if decisiones:
            json.dump(decisiones, open(dp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        r = subprocess.run([sys.executable, "-B", FH, "construir", c], capture_output=True, text=True)
        return r.returncode, json.load(open(f1p, encoding="utf-8")) if r.returncode == 0 else None, r.stdout

    def guardar_f1(f1, nombre_f):
        p = os.path.join(c, nombre_f)
        json.dump(f1, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        return p

    def rellenar(libro_in, f1_ruta, libro_out, sobrescribir=False):
        if os.path.exists(libro_out):
            os.remove(libro_out)
        r = subprocess.run([sys.executable, "-B", REL, libro_in, f1_ruta, libro_out] + (["--sobrescribir"] if sobrescribir else []), capture_output=True, text=True)
        return r.returncode, (r.stdout + r.stderr).strip()

    # Historia limpia (sin ceros) → libro base y libro de datos verificado, con el pipeline hasta el paso 2
    rc, f1_limpio, out = construir(False)
    p_limpio = guardar_f1(f1_limpio, "f1_limpio.json")
    shutil.copy(p_limpio, f1p)
    r = subprocess.run([sys.executable, "-B", os.path.join(RAIZ, "scripts", "pipeline.py"), c, "--hasta", "2"], capture_output=True, text=True)
    base, d_limpio = os.path.join(c, f"{nombre}_v63_base.xlsx"), os.path.join(c, f"{nombre}_v63_datos.xlsx")
    cm0 = _cm(d_limpio) if os.path.exists(d_limpio) else {}
    paso("H1 reutilización", "preparación: libro de datos con la Historia limpia (sbc y C50 «Rellenado y verificado»)",
         cm0.get("Historia!C18:L18", (None,))[0] == "Rellenado y verificado" and cm0.get("Análisis!C50", (None,))[0] == "Rellenado y verificado",
         f"pipeline --hasta 2 código {r.returncode}")
    v_limpio = _valores(d_limpio)
    rc, f1_pend, out = construir(True)
    p_pend = guardar_f1(f1_pend, "f1_pendiente.json")

    # Caso A · libro previamente rellenado (verificado) + Historia con ceros pendientes
    for sob in (False, True):
        d_a = os.path.join(c, f"A_{'sobrescribir' if sob else 'sin_sobrescribir'}.xlsx")
        rc, out = rellenar(d_limpio, p_pend, d_a, sob)
        cm = _cm(d_a) if rc == 0 else {}
        v = _valores(d_a) if rc == 0 else {}
        etiquetas = {k: cm.get(k, (None,))[0] for k in ("Historia!C18:L18", "Historia!C13:L13", "Análisis!C50")}
        ok_etq = all(x == "Dato no verificable" for x in etiquetas.values()) and all("[H1]" in str(cm.get(k, (None, ""))[1]) for k in etiquetas)
        if sob:
            ok_val = v.get("Análisis!C50") == f1_pend["analisis"]["C50"]["valor"]
            det_val = f"C50 = {v.get('Análisis!C50')} (Historia nueva {f1_pend['analisis']['C50']['valor']}, escrito por --sobrescribir)"
        else:
            ok_val = v.get("Análisis!C50") == v_limpio["Análisis!C50"] and "conserva" in str(cm.get("Análisis!C50", (None, ""))[1])
            det_val = f"C50 conservado = {v.get('Análisis!C50')} (la Historia nueva daría {f1_pend['analisis']['C50']['valor']}; la nota lo dice)"
        paso("H1 reutilización", f"caso A {'con' if sob else 'sin'} --sobrescribir: sbc, adquisiciones y C50 pasan a «Dato no verificable» [H1]; ninguna etiqueta verificada se conserva",
             rc == 0 and ok_etq, f"código {rc} · {json.dumps(etiquetas, ensure_ascii=False)}")
        paso("H1 reutilización", f"caso A {'con' if sob else 'sin'} --sobrescribir: el valor de C50 solo cambia si se pide --sobrescribir", rc == 0 and ok_val, det_val)
    d_a1 = os.path.join(c, "A_sin_sobrescribir.xlsx")

    # Caso A (etapa 1) · C50 trae un valor de la etapa 1 (fuente previa, no de esta Historia) y la Historia tiene ceros pendientes en su ventana
    c1 = TS.preparar("EmpresaX_reutilizacion_etapa1")
    os.remove(os.path.join(c1, "fase1_v63.json"))
    _empresa_sintetica_fase1(c1)
    subprocess.run([sys.executable, "-B", FH, "construir", c1], capture_output=True, text=True)
    r1 = subprocess.run([sys.executable, "-B", os.path.join(RAIZ, "scripts", "pipeline.py"), c1, "--hasta", "2"], capture_output=True, text=True)
    d1 = os.path.join(c1, "EmpresaX_reutilizacion_etapa1_v63_datos.xlsx")
    cm1 = _cm(d1) if os.path.exists(d1) else {}
    v1 = _valores(d1) if os.path.exists(d1) else {}
    import openpyxl
    v53 = openpyxl.load_workbook(os.path.join(c1, "etapa1", "EmpresaX_reutilizacion_etapa1_evaluada.xlsx"), read_only=True)["Análisis"]["C50"].value
    paso("H1 reutilización", "caso A (etapa 1): el C50 heredado de la etapa 1 conserva su valor pero queda «Dato no verificable» [H1] (la fuente previa no se da por válida)",
         cm1.get("Análisis!C50", (None,))[0] == "Dato no verificable" and "[H1]" in str(cm1.get("Análisis!C50", (None, ""))[1]) and v1.get("Análisis!C50") == v53,
         f"pipeline código {r1.returncode} · C50 = {v1.get('Análisis!C50')} (etapa 1: {v53}) · {cm1.get('Análisis!C50', (None,))[0]}")

    # Caso B · C50 ya presente en fase1_metadatos.json con la media de la misma Historia y ventana (no se elimina)
    c50_misma = {"valor": f1_limpio["analisis"]["C50"]["valor"], "fuente": "media 2023–2025 de SBC de los informes anuales (misma Historia)", "pagina": None,
                 "periodo": "2023–2025", "unidad": "mm"}
    rc, f1_b, out = construir(True, meta_an={"C50": c50_misma})
    e = (f1_b or {}).get("analisis", {}).get("C50", {})
    paso("H1 reutilización", "caso B: C50 de los metadatos (misma Historia y ventana) hereda el pendiente sin cambiar su valor",
         rc == 0 and e.get("pendiente_verificacion") == [2023, 2024, 2025] and e.get("valor") == c50_misma["valor"], f"código {rc} · {json.dumps({k: e.get(k) for k in ('valor', 'pendiente_verificacion')})}")
    p_b = guardar_f1(f1_b, "f1_B.json") if f1_b else None
    rc2, out2 = rellenar(base, p_b, os.path.join(c, "B.xlsx")) if p_b else (None, "")
    paso("H1 reutilización", "caso B: en el libro, C50 queda «Dato no verificable» [H1]", rc2 == 0 and _cm(os.path.join(c, "B.xlsx")).get("Análisis!C50", (None,))[0] == "Dato no verificable", f"código {rc2}")
    indep_ok = dict(c50_misma, fuente="Nota 12 del informe 2025, cuadro de pagos en acciones", independiente={
        "fuente": "AR_2025.txt p. 88, nota 12: «Share-based payment expense for the three years 2023–2025: 13.9»", "fecha": "2026-11-08",
        "confirmado_por": "Persona responsable del proyecto", "motivo": "cifra impresa en una nota distinta del estado de flujos"})
    rc, f1_b2, out = construir(True, meta_an={"C50": indep_ok})
    e2 = (f1_b2 or {}).get("analisis", {}).get("C50", {})
    paso("H1 reutilización", "caso B: una fuente independiente con respaldo explícito y trazable (fuente con página, fecha, persona) no hereda el pendiente",
         rc == 0 and not e2.get("pendiente_verificacion") and e2.get("independiente_confirmado") is True, f"código {rc} · {json.dumps({k: e2.get(k) for k in ('pendiente_verificacion', 'independiente_confirmado')})}")
    for etiqueta, mod in (("declarada sin respaldo", {"independiente": None}),
                          ("firmada por un agente", {"independiente": dict(indep_ok["independiente"], confirmado_por="agente de metadatos")}),
                          ("sin página", {"independiente": dict(indep_ok["independiente"], fuente="nota 12")})):
        x = dict(indep_ok, **mod)
        if x.get("independiente") is None:
            x.pop("independiente")
            x["fuente"] = "fuente independiente (declarada por el agente)"
        rc, f1_b3, out = construir(True, meta_an={"C50": x})
        e3 = (f1_b3 or {}).get("analisis", {}).get("C50", {})
        rv = open(os.path.join(c, "historia_revision.md"), encoding="utf-8").read()
        paso("H1 reutilización", f"caso B: fuente independiente {etiqueta} → sigue pendiente" + (" y queda anotada como no aceptada" if etiqueta != "declarada sin respaldo" else ""),
             rc == 0 and e3.get("pendiente_verificacion") == [2023, 2024, 2025] and (etiqueta == "declarada sin respaldo" or "Fuentes independientes no aceptadas" in rv), f"código {rc}")

    # Caso C · confirmación posterior sobre un libro previamente pendiente
    d_pend = os.path.join(c, "C_pendiente.xlsx")
    rellenar(base, p_pend, d_pend)
    buenas = {"sbc": {str(a): {"valor_mm": 0, "fuente": f"AR_{a}.txt p. 1: «{CITA_SBC}»", "fecha": "2026-11-08", "confirmado_por": "Persona responsable del proyecto"} for a in (2023, 2024, 2025)}}
    rc, f1_conf, out = construir(True, decisiones=buenas)
    p_conf = guardar_f1(f1_conf, "f1_confirmado.json")
    d_c1 = os.path.join(c, "C_confirmado.xlsx")
    rc, out = rellenar(d_pend, p_conf, d_c1)
    cm = _cm(d_c1) if rc == 0 else {}
    etq = {k: cm.get(k, (None,))[0] for k in ("Historia!C18:L18", "Análisis!C50", "Historia!C13:L13")}
    paso("H1 reutilización", "caso C: tras la confirmación, sbc y C50 pasan a «Rellenado y verificado» y adquisiciones 2017 sigue «Dato no verificable»",
         rc == 0 and etq == {"Historia!C18:L18": "Rellenado y verificado", "Análisis!C50": "Rellenado y verificado", "Historia!C13:L13": "Dato no verificable"}
         and "[H1]" not in str(cm.get("Historia!C18:L18", (None, ""))[1]) and "[H1]" not in str(cm.get("Análisis!C50", (None, ""))[1]), f"código {rc} · {json.dumps(etq, ensure_ascii=False)}")
    dif = _difs(_valores(d_pend), _valores(d_c1)) if rc == 0 else ["sin libro"]
    paso("H1 reutilización", "caso C: el cambio de estado no modifica ningún valor", not dif, ", ".join(dif[:5]) or "ningún valor cambia")
    otras = {k: (cm.get(k, (None,))[0], _cm(d_pend).get(k, (None,))[0]) for k in ("Historia!C6:L6", "Análisis!C46", "Análisis!C47")}
    paso("H1 reutilización", "caso C: solo cambian las evidencias afectadas (las demás conservan su estado)", all(a == b for a, b in otras.values()), json.dumps(otras, ensure_ascii=False))
    # reutilización no soportada: libro con C50 conservado de otra Historia y marcado pendiente → la confirmación no puede validarlo
    d_c2 = os.path.join(c, "C_no_soportado.xlsx")
    rc, out = rellenar(d_a1, p_conf, d_c2)
    paso("H1 reutilización", "caso C sin soporte: C50 pendiente con un valor distinto del de la Historia confirmada → rechazo expreso (código 5), sin escribir el libro y pidiendo regenerar",
         rc == 5 and not os.path.exists(d_c2) and "regener" in out.lower(), f"código {rc} · {out.splitlines()[-1][:160] if out else ''}")
    rc, out = rellenar(d_a1, p_conf, d_c2, sobrescribir=True)
    cm = _cm(d_c2) if rc == 0 else {}
    paso("H1 reutilización", "caso C sin soporte, regenerado con --sobrescribir: C50 toma el valor de la Historia confirmada y queda «Rellenado y verificado»",
         rc == 0 and cm.get("Análisis!C50", (None,))[0] == "Rellenado y verificado" and _valores(d_c2).get("Análisis!C50") == f1_conf["analisis"]["C50"]["valor"], f"código {rc}")


# ------------------------------------------------------------------------------- H3 · expediente corregido de Aarsleff
H3_DIR = os.path.join("empresas_v2_correcciones", "2026-11_H3")
H3_EXCEL_PERMITIDAS = {"Análisis!B102", "Control maestro!N30"}           # las dos celdas de texto con la frase
# diferencias técnicas inevitables de la regeneración (no son contenido): fecha de revisión que rellenar_fase1_v63.py escribe
# con la fecha del día en Control maestro!L5
H3_EXCEL_TECNICAS = {"Control maestro!L5"}
H3_ARCHIVOS_TECNICOS = {"estado_pipeline.json": "historial, marcas de tiempo, rutas absolutas y anotaciones «agente simulado»",
                        "auditoria.md": "auditoría nueva (paso 13) de un agente de verificación con contexto limpio",
                        "CORRECCION_H3.md": "registro de la corrección (nuevo)",
                        "diagnostico.md.anterior": "solo en el original: restos de intentos anteriores del pipeline (4-nov-2026)",
                        "diagnostico.json.anterior": "solo en el original: restos de intentos anteriores del pipeline (4-nov-2026)",
                        "Aarsleff_v63_base.xlsx.conciliacion.json": "solo cambian las rutas absolutas de «origen» y «plantilla» (comprobado)",
                        "Aarsleff_v63_datos.xlsx.fase1.registro.json": "n_celdas 444 → 445: rellenar_fase1_v63.py (H1) vacía también la columna J de las filas de Historia «No aplicable» (aquí Control maestro!J121, que ya estaba vacía); el libro no cambia (comprobado)"}
FRASE_VARIANTES = [re.compile(r"(?i)\b(cuatro|4|four)\s+(años|ejercicios|years)\b[^.;]{0,60}negativ"),
                   re.compile(r"(?i)negativ[^.;]{0,40}\b(cuatro|4)\s+(de|en)\s+(diez|10)\b")]


def _textos_excel(libro, data_only):
    import openpyxl
    wb = openpyxl.load_workbook(libro, data_only=data_only)
    return {f"{ws.title}!{c.coordinate}": c.value for ws in wb.worksheets for row in ws.iter_rows() for c in row if c.value is not None}


def _norm_tecnica(x, O, N):
    """Normaliza lo técnico de la regeneración: la carpeta absoluta del expediente (original en la máquina de origen, nuevo aquí),
    las huellas SHA-256 de los libros (16 o 64 cifras hexadecimales) y la fecha de revisión AAAA-MM-DD de Control maestro!L5."""
    s = str(x)
    for raiz in (O, N):
        s = s.replace(raiz, "<CARPETA>")
    # cualquier ruta absoluta a la carpeta del expediente (original o nuevo), esté donde esté el paquete
    s = re.sub(r"/[^\s'\"<>|]*?/(?:empresas_v2|empresas_v2_correcciones/2026-11_H3)/Aarsleff(?=/|\b)", "<CARPETA>", s)
    s = re.sub(r"\b[0-9a-f]{64}\b|\b[0-9a-f]{16}(?=…)", "<SHA256>", s)
    return s


def _solo_frase(viejo, nuevo):
    return isinstance(viejo, str) and isinstance(nuevo, str) and viejo != nuevo and \
        nuevo.replace("cinco años negativos", "cuatro años negativos").replace("Cinco años negativos", "Cuatro años negativos") == viejo


def _valor_ruta(obj, ruta):
    for parte in re.findall(r"\.([^.\[]+)|\[(\d+)\]", ruta):
        clave, idx = parte
        obj = obj[int(idx)] if idx else (obj.get(clave) if isinstance(obj, dict) else None)
    return obj


def h3():
    import difflib
    sys.path.insert(0, os.path.join(RAIZ, "scripts"))
    import pipeline
    O = os.path.join(RAIZ, "empresas_v2", "Aarsleff")
    N = os.path.join(RAIZ, H3_DIR, "Aarsleff")
    if not os.path.isdir(N):
        paso("H3", "existe el expediente nuevo", False, N)
        return
    informe = {"contenido": [], "tecnicas": [], "excel": {}, "json": {}, "texto": {}}

    def rel(p, base):
        return os.path.relpath(p, base)

    def lista(base):
        out = set()
        for r_, ds, fs in os.walk(base):
            ds[:] = [d for d in ds if d not in ("recalc", ".lo_perfil", "prompts_generados")]
            out |= {rel(os.path.join(r_, f), base) for f in fs}
        return out
    fo, fn = lista(O), lista(N)
    informe["tecnicas"].append("prompts_generados/, recalc/ y .lo_perfil/: prompts con rutas absolutas y copias de trabajo de LibreOffice (excluidos de la comparación; el original no incluía recalc/)")
    # 1. variantes de la afirmación incorrecta: ninguna en el expediente nuevo (textos y celdas del Excel)
    hallazgos = []
    for f in sorted(fn - {"CORRECCION_H3.md"}):   # el registro de la corrección cita la frase antigua a propósito
        p = os.path.join(N, f)
        if f.endswith(".xlsx"):
            for k, v in _textos_excel(p, False).items():
                if isinstance(v, str) and any(rx.search(v) for rx in FRASE_VARIANTES):
                    hallazgos.append(f"{f}:{k}")
        elif f.endswith((".md", ".json", ".txt", ".csv")):
            for i, l in enumerate(open(p, encoding="utf-8", errors="replace").read().splitlines(), 1):
                if any(rx.search(l) for rx in FRASE_VARIANTES):
                    hallazgos.append(f"{f}:{i}")
    paso("H3", "ninguna variante de «cuatro años negativos» en el expediente nuevo (textos y celdas)", not hallazgos, ", ".join(hallazgos[:5]) or "0 coincidencias")
    exclusiones = ["Cuatro de cinco años planos o negativos", "cuatro planos o negativos", "tres años negativos en once", "FCF negativo en FY20/21–21/22"]
    conservadas = {x: sum(open(os.path.join(N, f), encoding="utf-8", errors="replace").read().count(x) for f in fn if f.endswith((".md", ".json")))
                   for x in exclusiones}
    paso("H3", "las frases excluidas (otra serie u otra definición, heredadas) se conservan", all(v > 0 for v in conservadas.values()), json.dumps(conservadas, ensure_ascii=False))

    # 2. propagación: por archivo, «cinco» en el nuevo = «cuatro» en el original
    def cuenta(p, frase):
        if p.endswith(".xlsx"):
            return sum(str(v).count(frase) for v in _textos_excel(p, False).values() if isinstance(v, str))
        return open(p, encoding="utf-8", errors="replace").read().count(frase)
    prop, mal = {}, []
    for f in sorted(fo):
        if not f.endswith((".md", ".json", ".txt", ".csv", ".xlsx")):
            continue
        n4 = cuenta(os.path.join(O, f), "cuatro años negativos") + cuenta(os.path.join(O, f), "Cuatro años negativos")
        if n4:
            n5 = (cuenta(os.path.join(N, f), "cinco años negativos") + cuenta(os.path.join(N, f), "Cinco años negativos")) if f in fn else -1
            prop[f] = (n4, n5)
            if n5 != n4:
                mal.append(f)
    tot4, tot5 = sum(a for a, _ in prop.values()), sum(b for _, b in prop.values())
    paso("H3", "propagación completa: cada archivo tiene tantas «cinco años negativos» como «cuatro» tenía el original (27 en 13 archivos)",
         not mal and tot4 == 27 and len(prop) == 13 and tot5 == 27, f"{len(prop)} archivos · {tot4} → {tot5}" + (f" · distintos: {mal}" if mal else ""))

    # 3. controles
    st = json.load(open(os.path.join(N, "estado_pipeline.json"), encoding="utf-8"))
    hist = st.get("historial", [])
    ver = lambda s: any(s in x for x in hist)  # noqa: E731
    aud = pipeline.Pipeline.veredicto_auditoria(open(os.path.join(N, "auditoria.md"), encoding="utf-8").read()) if os.path.exists(os.path.join(N, "auditoria.md")) else "sin auditoría"
    paso("H3", "controles: verificar_todo.sh PASS, celdas PASS (64), esquema de la ficha VÁLIDO, citas PASS, integridad ÍNTEGRO",
         ver("RESULTADO verificar_todo.sh: PASS") and ver("PASS: 0 errores · 64 celdas correctas") and ver("VÁLIDO · ficha.json contra ficha.esquema.json")
         and "PASS" in open(os.path.join(N, "verificacion_citas.txt"), encoding="utf-8").read() and "ÍNTEGRO" in open(os.path.join(N, "verificacion_integridad.txt"), encoding="utf-8").read())
    paso("H3", "auditoría nueva leída con la regla de H2: APROBADO; pipeline terminado (paso 14, concluido)", aud == "APROBADO" and st.get("paso") == 14 and st.get("estado_analisis") == "concluido",
         f"auditoría {aud} · paso {st.get('paso')} · estado {st.get('estado_analisis')}")

    # 4. Excel: todas las hojas y celdas, fórmulas y valores guardados
    for libro in ("Aarsleff_v63_evaluada.xlsx", "Aarsleff_v63_datos.xlsx", "Aarsleff_v63_base.xlsx", "etapa1/Aarsleff_evaluada.xlsx"):
        po, pn = os.path.join(O, libro), os.path.join(N, libro)
        res = {}
        for modo, data_only in (("formulas", False), ("valores", True)):
            a_, b_ = _textos_excel(po, data_only), _textos_excel(pn, data_only)
            d = _difs(a_, b_)
            cont = [k for k in d if k not in H3_EXCEL_PERMITIDAS and k not in H3_EXCEL_TECNICAS]
            perm = [k for k in d if k in H3_EXCEL_PERMITIDAS]
            frase_ok = all(_solo_frase(a_.get(k), b_.get(k)) for k in perm)
            res[modo] = {"celdas": len(set(a_) | set(b_)), "diferencias": d, "contenido_no_permitido": cont, "permitidas_solo_frase": frase_ok}
        informe["excel"][libro] = res
        esperadas = H3_EXCEL_PERMITIDAS if libro == "Aarsleff_v63_evaluada.xlsx" else set()
        ok = all(not r["contenido_no_permitido"] and r["permitidas_solo_frase"] and set(x for x in r["diferencias"] if x not in H3_EXCEL_TECNICAS) == esperadas for r in res.values())
        paso("H3", f"Excel {libro}: fórmulas y valores idénticos salvo " + ("B102 y Control maestro!N30 (solo la frase)" if esperadas else "nada") + " y la fecha técnica Control maestro!L5",
             ok, " · ".join(f"{m}: {r['celdas']} celdas, dif {r['diferencias'][:4]}" for m, r in res.items()))

    # 5. JSON y textos: solo cambia la frase; el resto, técnico y declarado
    cont = []
    for f in sorted(fo | fn):
        if f.endswith(".xlsx") or os.path.basename(f) in H3_ARCHIVOS_TECNICOS or f.startswith("etapa1/") and f.endswith(".xlsx"):
            if os.path.basename(f) in H3_ARCHIVOS_TECNICOS:
                informe["tecnicas"].append(f"{f}: {H3_ARCHIVOS_TECNICOS[os.path.basename(f)]}")
            continue
        if f not in fo or f not in fn:
            cont.append(f"{f}: solo en {'el nuevo' if f in fn else 'el original'}")
            continue
        po, pn = os.path.join(O, f), os.path.join(N, f)
        if open(po, "rb").read() == open(pn, "rb").read():
            continue
        if f.endswith(".json"):
            jo, jn = json.load(open(po, encoding="utf-8")), json.load(open(pn, encoding="utf-8"))
            difs = []

            def walk(x, y, p=""):
                if isinstance(x, dict) and isinstance(y, dict):
                    for k in sorted(set(x) | set(y)):   # orden fijo: el informe tiene que ser reproducible
                        walk(x.get(k), y.get(k), f"{p}.{k}")
                elif isinstance(x, list) and isinstance(y, list) and len(x) == len(y):
                    for i, (u, v) in enumerate(zip(x, y)):
                        walk(u, v, f"{p}[{i}]")
                elif x != y and not (isinstance(x, (int, float)) and isinstance(y, (int, float)) and abs(x - y) <= 1e-9 * max(1, abs(x), abs(y))):
                    difs.append((p, _solo_frase(x, y), str(x)[:120], str(y)[:120]))
            walk(jo, jn)
            informe["json"][f] = [{"ruta": p, "solo_frase": s} for p, s, _, _ in difs]
            for p, s, xo, xn in difs:
                if s:
                    continue
                vo, vn = _valor_ruta(jo, p), _valor_ruta(jn, p)
                if _norm_tecnica(vo, O, N) == _norm_tecnica(vn, O, N) or p.endswith(".cabecera.L5_revision"):
                    informe["tecnicas"].append(f"{f}{p}: ruta absoluta, SHA-256 de un libro o fecha de revisión L5")
                else:
                    cont.append(f"{f}{p}: {xo!r} → {xn!r}")
        else:
            lo, ln = open(po, encoding="utf-8", errors="replace").read().splitlines(), open(pn, encoding="utf-8", errors="replace").read().splitlines()
            cambios = [(i, a_, b_) for i, (a_, b_) in enumerate(zip(lo, ln), 1) if a_ != b_]
            informe["texto"][f] = [{"linea": i, "solo_frase": _solo_frase(a_, b_)} for i, a_, b_ in cambios]
            if len(lo) != len(ln):
                cont.append(f"{f}: {len(lo)} → {len(ln)} líneas")
            for i, a_, b_ in cambios:
                if _solo_frase(a_, b_):
                    continue
                if _norm_tecnica(a_, O, N) == _norm_tecnica(b_, O, N):
                    informe["tecnicas"].append(f"{f}:{i}: ruta absoluta o SHA-256 de un libro")
                else:
                    cont.append(f"{f}:{i}: {a_[:100]!r} → {b_[:100]!r}")
    informe["contenido"] = sorted(cont)
    informe["tecnicas"] = sorted(informe["tecnicas"])
    paso("H3", "JSON y textos: toda diferencia es el cambio de la frase o técnica (ruta absoluta, SHA-256 de un libro, fecha L5, archivos declarados)", not cont,
         "; ".join(cont[:4]) or f"ninguna diferencia de contenido · {len(informe['tecnicas'])} técnicas registradas en comparacion_H3.json")

    # 6. conservación explícita
    conserv = {
        "fase1_v63.json idéntico": open(os.path.join(O, "fase1_v63.json"), "rb").read() == open(os.path.join(N, "fase1_v63.json"), "rb").read(),
        "precio.json idéntico": json.load(open(os.path.join(O, "precio.json"), encoding="utf-8")) == json.load(open(os.path.join(N, "precio.json"), encoding="utf-8")),
        "C25 = No (fase A y Excel)": json.load(open(os.path.join(N, "fase_a.json"), encoding="utf-8"))["celdas"]["C25"] == "No"
        and _textos_excel(os.path.join(N, "Aarsleff_v63_evaluada.xlsx"), False).get("Análisis!C25") == "No",
    }
    fo_, fn_ = json.load(open(os.path.join(O, "ficha.json"), encoding="utf-8")), json.load(open(os.path.join(N, "ficha.json"), encoding="utf-8"))
    for k in ("fecha", "cubo", "estado_analisis", "precio", "escalera", "decision", "predicciones", "motor"):
        conserv[f"ficha.{k} idéntico"] = fo_.get(k) == fn_.get(k)
    paso("H3", "conservados: fase1_v63.json, precio.json (precio de Sí, ponderado, MALO), fecha, cubo, acción, predicciones y C25 = No",
         all(conserv.values()), ", ".join(k for k, v in conserv.items() if not v) or f"{len(conserv)} comprobaciones")
    # 7. original intacto (manifiesto de la base)
    distintos = [l.split("  ", 1)[1].strip() for l in open(os.path.join(AQUI, "linea_base", "manifiesto_empresas_v2_base.sha256"), encoding="utf-8")
                 if l.startswith(tuple("0123456789abcdef")) and hashlib.sha256(open(os.path.join(RAIZ, l.split("  ", 1)[1].strip()), "rb").read()).hexdigest() != l.split("  ", 1)[0]]
    paso("H3", "el expediente original (y todo empresas_v2/) sigue idéntico a la base", not distintos, f"{len(distintos)} distintos")
    paso("H3", "CORRECCION_H3.md registra las cinco correcciones", os.path.exists(os.path.join(N, "CORRECCION_H3.md"))
         and open(os.path.join(N, "CORRECCION_H3.md"), encoding="utf-8").read().count("→") >= 5)
    # el informe regenerado va a pruebas/resultados_reparacion/ (el entregado en empresas_v2_correcciones/ no se reescribe) y tiene
    # que coincidir con el entregado
    os.makedirs(os.path.join(AQUI, "resultados_reparacion"), exist_ok=True)
    nuevo = json.loads(json.dumps(informe, ensure_ascii=False, default=str))
    json.dump(nuevo, open(os.path.join(AQUI, "resultados_reparacion", "comparacion_H3.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    entregado_p = os.path.join(RAIZ, H3_DIR, "comparacion_H3.json")
    entregado = json.load(open(entregado_p, encoding="utf-8")) if os.path.exists(entregado_p) else None
    paso("H3", "la comparación regenerada coincide con comparacion_H3.json entregado", entregado == nuevo,
         "idéntica" if entregado == nuevo else "distinta: ver pruebas/resultados_reparacion/comparacion_H3.json")


PARTES = {"h2": h2, "h1": h1, "h1_recorrido": h1_recorrido, "h1_reutilizacion": h1_reutilizacion, "h3": h3}

if __name__ == "__main__":
    pedidas = [p.lower() for p in sys.argv[1:]] or list(PARTES)
    for p in pedidas:
        if p not in PARTES:
            print(f"parte desconocida: {p} (disponibles: {', '.join(PARTES)})")
            sys.exit(2)
        PARTES[p]()
    ok = sum(r["ok"] for r in resultados)
    print(f"\n{ok}/{len(resultados)} comprobaciones PASAN")
    json.dump(resultados, open(os.path.join(AQUI, "resultado_comprobadores.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    sys.exit(0 if ok == len(resultados) else 1)
