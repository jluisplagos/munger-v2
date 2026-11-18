#!/usr/bin/env python3
"""Prueba de extremo a extremo de F1 · US GAAP en el pipeline, con la empresa sintética y los agentes simulados de
test_pipeline_sintetico.py (LibreOffice: ejecutar con flock /home/user/e_work/libreoffice.lock). Directorio temporal; no toca la batería
sintética ni su línea de base, ni las pruebas de F1-IMPL y de la V6.3.1.

Uso (desde cualquier carpeta): flock … python3 -B prueba_pipeline_usgaap.py [SALIDA.txt]
La empresa sintética se prepara como una empresa US GAAP: norma «US GAAP» en la fase 1 (Control maestro L4), sin intereses en financiación
(C48 = 0, fila 16 a cero), sin principal de arrendamientos en financiación (C49 = 0, fila 17 a cero) y con 50 de pasivo por arrendamiento
OPERATIVO en la fila 23. Declaración US_GAAP con arrendamientos operativos (pagos y coste lineal de la ventana) y sin financieros;
perímetro A2_propio en la reinversión, las palancas y el ROIC; plantilla V6.3.1 F1 (config_v2_v631_f1.json).
Casos:
  PU1 · tramos «no_publicada» (hipótesis D-US1): el libro V6.3.1 tal cual calcula lo declarado; F1 no bloquea en los pasos 7 y 12; el
        análisis llega a concluido; la ficha y el informe dicen que la conclusión es CONDICIONADA, con la cota en la línea del informe
        (R1-8), y muestran coste lineal − pagos (D-US2).
  PU2 · la variación del pasivo declarada dentro de la fila 14, con su importe: el paso 7 termina en no_entregable · límite del modelo
        (F1-LIBRO: ningún libro la retira del circulante).
  PU3 · sin «arrendamientos_us_gaap»: pendiente_de_datos en el paso 7, ya no un límite del modelo. Con A0 declarado lo dice la capa
        (F1-US-DESGLOSE); con A2, el propio libro: sin la clasificación la fila 86 queda vacía, f no se calcula y el libro lo declara
        incompleto (Motor V05) antes de llegar a la capa.
  PU4 · C49 con importe (pagos de arrendamientos en financiación) y sin financieros declarados: pendiente_de_datos (F1-US-C49).
Ronda 2 (revisión R1 y decisiones D-US2 bis y D-WM):
  PU5 · (R1-3, camino i) la variación del pasivo está dentro de la fila 14 (la fase 1 sumó su línea) y se declara «fuera» citando esa
        línea: con fase1_partes el paso 7 termina en pendiente_de_datos (F1-US-FILAS, DATOS INVÁLIDOS); antes llegaba a concluido.
  PU6 · (R1-3, camino ii) amortización declarada «fila_8» con una cita real de una nota y una D&A que no la nombra: no se puede contrastar
        con una línea → llega a concluido, pero CONDICIONADA, con su cota exacta en la ficha y en el informe; K3b «según lo declarado».
  PU7 · (D-US2 bis, caso Nike) los dos tramos dentro de la fila 14 en líneas mezcladas y partidas, pagos ≠ coste: no bloquea; concluido
        con el valor de la hoja (coste contable) y, al lado, cuánto cambiaría contando los pagos.
  PU8 · (R1-1, XB3) motor B, libro US GAAP recalculado por LibreOffice (textos compartidos) y SIN declaración F1: el gancho se ejecuta y
        el paso 7 termina en pendiente_de_datos; antes llegaba a concluido sin evaluar el puente.
  PU9 · (R1-1, XB4) motor B, libro US GAAP y declaración que dice NIIF: F1-NORMA (mezcla de normas), pendiente_de_datos.
  PU10 · (R1-9, XB2) motor B con el puente conforme: llega al final con F1 evaluado en el paso 12; la línea del informe habla del puente de
        deuda (no de «caja base por dos vías sin explicar» ni de «perímetro declarado: sin declarar») y la ficha lleva el aviso del ancla.
  PU11 · (R1-11) «norma_contable» fuera de la lista cerrada en fase1_v63.json («U.S. GAAP»): el paso 2 termina en pendiente_de_datos,
        antes de gastar la fase A.
Cierre de la ronda 2 (revisión R2):
  PU12 · (R2-1) el estado de flujos lleva una línea que nombra el arrendamiento sin ser un tramo («Loss on lease termination») y la
        variación del pasivo va dentro de «Accrued and other liabilities»: con la declaración VERAZ («no_publicada») llega a concluido
        CONDICIONADA con su cota (antes: pendiente_de_datos); con los dos tramos «fuera» citando esa línea, pendiente_de_datos en el
        paso 7 (antes: concluido sin condición y sobrevalorado).
  PU13 · (R2-2) «Operating lease liabilities» (2,5 al año) es una línea propia sumada en la fila 14 y se declara «fila_14» con importe 0:
        pendiente_de_datos en el paso 7 (F1-US-FILAS, DATOS INVÁLIDOS); antes, concluido sin condición.
  PU14 · («Otro») motor B con «Otro» como norma de la fase 1: el paso 7 termina en no_entregable · límite del modelo (antes:
        pendiente_de_datos).
"""
import hashlib
import json
import os
import shutil
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
PV = os.path.abspath(os.path.join(AQUI, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(PV, "pruebas"))
sys.path.insert(0, os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_15", "f1_impl", "scripts"))
sys.path.insert(0, os.path.join(PV, "scripts"))
sys.dont_write_bytecode = True
import test_pipeline_sintetico as TS  # noqa: E402
import prueba_pipeline_f1 as PF  # noqa: E402
import agentes_sinteticos as AG  # noqa: E402

CFG631 = os.path.join(PV, "config_v2_v631_f1.json")
DOC = "informe anual sintético"
REG = {"fecha": "2026-11-18", "persona": "prueba sintética F1 · US GAAP (no es una decisión)", "motivo": "caso de prueba de extremo a extremo"}
TXT = "10K_sint.txt"   # el texto del informe que «usó la fase 1» (texto/): la fuente registrada cuando el expediente lleva fase1_partes
DA, L_PAS, NOTA_AM = "Depreciation and amortization", "Operating lease liabilities", "Amortization of operating lease right-of-use assets"
WC = ("Accounts receivable", "Accounts payable and accrued liabilities")
NIKE_ACT = ("(Increase) decrease in prepaid expenses, operating lease right-of-use assets and", "other current and non-current assets")
NIKE_PAS = ("Increase (decrease) in accounts payable, accrued liabilities, operating lease", "liabilities and other current and non-current liabilities")
RES = []


def paso(nombre, ok, detalle=""):
    RES.append((nombre, bool(ok)))
    print(("PASA " if ok else "FALLA") + " · " + nombre + (f" · {detalle}" if detalle else ""), flush=True)


def serie(vals):
    return {str(y): {"valor_fuente": v, "signo": 1, "tratamiento": "ninguno", "documento": DOC, "pagina": 1, "literal": repr(v)} for y, v in vals.items()}


def declaracion(bloque=True, ub_pas="no_publicada", ajuste=None, financieros=False, per="A2_propio", P=None, Lc=None):
    d = PF.declaracion("US_GAAP")
    d["conciliacion_fcf_base"] = [p for p in d["conciliacion_fcf_base"] if p["componente"] != "C48"]   # con US GAAP C48 y la fila 16 van a cero
    for k in ("perimetro_reinversion", "perimetro_palancas_s2c", "perimetro_roic"):
        d[k]["valor"] = per
    del d["series"]["da_rou"]   # sin arrendamientos financieros (lo dice la clasificación, con su evidencia)
    for s_ in d["series"].values():
        for e in s_.values():
            e.pop("archivo", None)
    if bloque:
        ev = {"documento": DOC, "pagina": 1}
        np_ = {"ubicacion": "no_publicada", "documento": DOC, "pagina": 2}
        d["arrendamientos_us_gaap"] = {
            "registro": REG,
            "operativos": dict(ev, cita="Operating lease cost", existen=True, amortizacion_rou=dict(np_),
                               variacion_pasivo=dict(np_) if ub_pas == "no_publicada" else {"documento": DOC, "pagina": 2, "cita": L_PAS, "ubicacion": ub_pas}),
            "financieros": dict(ev, cita="The Company has no finance leases", existen=financieros)}
        d["series"].update({"pagos_arr_operativo": serie(P or {2023: 3.0, 2024: 3.2, 2025: 3.4}), "coste_arr_operativo": serie(Lc or {2023: 3.1, 2024: 3.3, 2025: 3.5}),
                            "pasivo_arr_operativo": serie({2025: 50})})
        if ajuste is not None:
            d["series"]["circulante_arr_operativo"] = serie({y: ajuste for y in range(2021, 2026)})
    return d


def escribir_fuente(c, d, da=(DA,), wc=WC, fuera=(), notas=(), partes=False, importes=None):
    """La fuente del expediente (texto/10K_sint.txt, registrada con su huella). Página 1: notas (las cifras de las series y las citas de existencia);
    página 2: el estado de flujos, con las líneas que la fase 1 sumó en la fila 8 (`da`) y en la fila 14 (`wc`) y las que no sumó (`fuera`).
    partes=True: además fase1_partes/AR_2021…2025.json con el renglón de las cifras de cada línea sumada (el pipeline no las usa: fase1_v63.json ya
    existe; las lee la capa F1 para contrastar las ubicaciones declaradas). importes: {etiqueta: cifra impresa} de las líneas que la llevan propia (la
    misma en las tres columnas); las demás llevan cifras cualesquiera."""
    lits = sorted({str(e.get("literal")) for s_ in (d.get("series") or {}).values() for e in s_.values() if isinstance(e, dict)})
    n, filas, comp = [10], ["CONSOLIDATED STATEMENTS OF CASH FLOWS"], {"da": [], "circulante_lineas": [], "cfo": []}

    def poner(x, k=None):
        n[0] += 3
        pp = [x] if isinstance(x, str) else list(x)
        imp = (importes or {}).get(" ".join(pp))
        ult = f"{pp[-1]}    {imp}    {imp}    {imp}" if imp else f"{pp[-1]}    {n[0]}    {n[0] + 1}    {n[0] + 2}"
        filas.extend(pp[:-1] + [ult])
        if k:
            comp[k].append({"concepto": pp[-1] if len(pp) > 1 else x, "impreso": imp or str(n[0]), "pagina": 2, "linea": ult})

    poner("Net income")
    for x in da:
        poner(x, "da")
    for x in fuera:
        poner(x)
    filas.append("Changes in operating assets and liabilities:")
    for x in wc:
        poner(x, "circulante_lineas")
    poner("Net cash provided by operating activities", "cfo")
    poner("Purchases of property and equipment")
    txt = ("[PDF PAGE 1]\nInforme anual sintético (US GAAP): " + " ".join(lits) + "\nOperating lease cost\nThe Company has no finance leases\n" + "\n".join(notas)
           + "\n[PDF PAGE 2]\n" + "\n".join(filas) + "\n[PDF PAGE 3]\n")
    os.makedirs(os.path.join(c, "texto"), exist_ok=True)
    open(os.path.join(c, "texto", TXT), "w", encoding="utf-8").write(txt)
    d["fuentes_series"] = {DOC: {"archivo": os.path.join("texto", TXT), "sha256": hashlib.sha256(txt.encode("utf-8")).hexdigest()}}
    if partes:
        os.makedirs(os.path.join(c, "fase1_partes"), exist_ok=True)
        for a in range(2021, 2026):
            json.dump({"anio": a, "archivo": TXT, "unidad": "millones", "partidas": {k: {"actual": v, "anterior": v, "cero": None} for k, v in comp.items()}},
                      open(os.path.join(c, "fase1_partes", f"AR_{a}.json"), "w", encoding="utf-8"), ensure_ascii=False)


def preparar(nombre, d, circulante_extra=0.0, con_c49=False, fila23=None, norma="US GAAP", sin_decl=False, **fuente):
    """La empresa sintética como empresa US GAAP (ver la cabecera)."""
    c = TS.preparar(nombre, quitar_etapa1=("C48",) if con_c49 else ("C48", "C49"))
    json.dump({"modo": "registrada", "motivo": "prueba F1 · US GAAP: el valor de la etapa 1 prevalece en la empresa sintética"},
              open(os.path.join(c, "entrada_efectiva.json"), "w", encoding="utf-8"))
    p = os.path.join(c, "fase1_v63.json")
    f1 = json.load(open(p, encoding="utf-8"))
    f1["norma_contable"] = norma
    f1["analisis"]["C48"]["valor"] = 0
    f1["historia"]["partidas"]["intereses_financiacion"]["valores"] = [0] * 10
    if not con_c49:
        f1["analisis"]["C49"]["valor"] = 0
        f1["historia"]["partidas"]["arrendamientos_principal"]["valores"] = [0] * 10
    if fila23 is not None:
        f1["historia"]["partidas"]["arrendamientos"]["valores"] = [fila23] * 10
    if circulante_extra:
        w = f1["historia"]["partidas"]["circulante"]["valores"]
        f1["historia"]["partidas"]["circulante"]["valores"] = w[:5] + [x + circulante_extra for x in w[5:]]
    json.dump(f1, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    if circulante_extra and "importes" not in fuente:
        # (R2-2) si la variación del pasivo es una línea propia de la fila 14, su cifra impresa es la que la fase 1 sumó: «(2.5)» → +2,5 en la fila
        fuente["importes"] = {L_PAS: f"({circulante_extra:g})"}
    escribir_fuente(c, d, **fuente)
    if not sin_decl:
        json.dump(d, open(os.path.join(c, "motor_a_f1.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return c


def reaccion_motor(motor):
    base = TS.reaccion_normal()

    def r(c, nombre):
        if nombre == "fase_a":
            AG.fase_a(c, motor=motor)
        else:
            base(c, nombre)
    return r


def correr(c, motor="A"):
    os.environ["MUNGER_CONFIG"] = CFG631
    try:
        return TS.correr(c, TS.reaccion_normal() if motor == "A" else reaccion_motor(motor))
    finally:
        os.environ.pop("MUNGER_CONFIG", None)


def leer(c, n):
    p = os.path.join(c, n)
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}


def bloquean(r):
    return sorted({g["id"] for g in r.get("guardas") or [] if g.get("salta") and g.get("severidad") == "BLOQUEA"})


def linea_f1(c):
    inf = open(os.path.join(c, "informe.md"), encoding="utf-8").read() if os.path.exists(os.path.join(c, "informe.md")) else ""
    return next((x for x in inf.splitlines() if "· F1:" in x), "")


def main():
    salida = sys.argv[1] if len(sys.argv) > 1 else None
    base0, TS.BASE = TS.BASE, tempfile.mkdtemp(prefix="usgaap_pipe_")
    try:
        # PU1 · hipótesis D-US1 con la V6.3.1 tal cual
        c = preparar("EmpresaX_US", declaracion())
        rc, out = correr(c)
        st, r, fi, pa = TS.estado(c), leer(c, "motor_a_f1_resultado.json"), leer(c, "ficha.json"), leer(c, "plantilla_activa.json")
        from openpyxl import load_workbook
        ev = os.path.join(c, "recalc", "EmpresaX_US_v63_evaluada.xlsx")
        wb = load_workbook(ev, data_only=True) if os.path.exists(ev) else None
        h = wb["Historia"] if wb else None
        paso("PU1 · el libro es US GAAP (Control maestro L4), V6.3.1 F1, con A2_propio aplicado; C48 y C49 a cero y 50 de pasivo operativo en la fila 23",
             wb is not None and wb["Control maestro"]["L4"].value == "US GAAP" and pa.get("version") == "V6.3.1 F1" and h["C89"].value == "A2_propio"
             and wb["Análisis"]["C48"].value == 0 and wb["Análisis"]["C49"].value == 0 and h["L23"].value == 50,
             f"L4 {wb['Control maestro']['L4'].value if wb else None!r} · C89 {h['C89'].value if h else None!r}")
        g_l = [x for x in r.get("guardas") or [] if x["id"] == "F1-LIBRO"]
        paso("PU1 · tramos no publicados (hipótesis D-US1): el libro V6.3.1 tal cual calcula lo declarado (F1-LIBRO no salta) y F1 no bloquea; gancho en los pasos 7 y 12",
             g_l and not g_l[0]["salta"] and (r.get("libro_v631_f1") or {}).get("motivos") == [] and r.get("utilizable_para_conclusion") is True
             and (st.get("motor_a_f1") or {}).get("paso") == 12 and os.path.exists(os.path.join(c, "fase_b.json")),
             f"código {rc} · estado {st.get('estado_analisis')} · paso {st.get('paso')} · bloquean {bloquean(r)}")
        k3 = r.get("K3") or {}
        paso("PU1 · K3: alquiler contado una vez «según la hipótesis D-US1» (no se presenta como conforme: no es una comprobación independiente); F1-SERIES sin problemas",
             k3.get("K3b_alquiler_contado") == "una vez" and k3.get("K3b_contrastado") is False and k3.get("conforme") is None
             and not any(x["id"] == "F1-SERIES" and x["salta"] for x in r.get("guardas") or []), json.dumps(k3, ensure_ascii=False)[:200])
        f1b = fi.get("motor_a_f1") or {}
        linea = linea_f1(c)
        paso("PU1 · estado final concluido; la ficha dice que la conclusión es CONDICIONADA (hipótesis D-US1, con su registro y su cota) y muestra coste lineal − pagos (D-US2)",
             st.get("estado_analisis") == "concluido" and fi.get("estado_analisis") == "concluido" and f1b.get("utilizable_para_conclusion") is True
             and (f1b.get("condicionada") or {}).get("hipotesis") == "D-US1" and ((f1b.get("condicionada") or {}).get("registro") or {}).get("fecha") == "2026-11-18"
             and (f1b.get("condicionada") or {}).get("cota") and abs(((f1b.get("us_gaap") or {}).get("diferencia_coste_lineal_menos_pagos") or {}).get("coste_menos_pagos_medio", 0) - 0.1) < 1e-9
             and any(a.get("id") == "F1-US-HIPOTESIS" for a in f1b.get("avisos") or []),
             f"estado {st.get('estado_analisis')} · ficha {fi.get('estado_analisis')} · {str(f1b.get('rotulo'))[:120]}")
        rs = (((f1b.get("condicionada") or {}).get("cota") or {}).get("resumen") or {})
        paso("PU1 · el informe lo dice en su línea F1: «CONDICIONADA», la hipótesis, «se cuentan los pagos» con la diferencia y (R1-8) la cota en dos cifras: % del flujo "
             "sin crecimiento y % del valor presente en el escenario NORMAL",
             "CONDICIONADA" in linea and "D-US1" in linea and "se cuentan los pagos" in linea and "+0.100" in linea and "cota: el flujo sin crecimiento podría cambiar entre" in linea
             and "escenario NORMAL" in linea and rs.get("valor_presente_NORMAL_%") and rs.get("texto") and rs["texto"] in linea, linea[:520])
        pu = ((r.get("us_gaap") or {}).get("puente_de_deuda") or {})
        paso("PU1 · puente: con el motor A, F1-US-PUENTE informa de los 50 de pasivo operativo en la fila 23 (deuda coherente de un puente = fila 22)",
             any(x["id"] == "F1-US-PUENTE" and x["salta"] and x["severidad"] == "INFORMA" for x in r.get("guardas") or [])
             and pu.get("deuda_del_puente_coherente") == pu.get("deuda_financiera_fila_22") and pu.get("pasivo_operativo_dentro_de_la_fila_23") == 50.0, json.dumps(pu, ensure_ascii=False)[:200])
        # PU2 · la variación del pasivo dentro de la fila 14
        c = preparar("EmpresaX_US14", declaracion(ub_pas="fila_14", ajuste=2.5), circulante_extra=2.5, wc=WC + (L_PAS,))
        rc, out = correr(c)
        st, r, dg = TS.estado(c), leer(c, "motor_a_f1_resultado.json"), leer(c, "diagnostico.json")
        paso("PU2 · variación del pasivo dentro de la fila 14 (2,5 al año, declarada): el paso 7 termina en no_entregable · límite del modelo con F1-LIBRO; sin fase B",
             st.get("estado_analisis") == "no_entregable" and st.get("paso") == 7 and (dg.get("causa") or {}).get("tipo") == "limite_del_modelo" and bloquean(r) == ["F1-LIBRO"]
             and "retirada del circulante" in str((dg.get("causa") or {}).get("detalle")) and not os.path.exists(os.path.join(c, "fase_b.json")),
             f"estado {st.get('estado_analisis')} · paso {st.get('paso')} · bloquean {bloquean(r)}")
        cd = r.get("calculo_perimetro_declarado") or {}
        lib = (r.get("replica_del_libro") or {})
        paso("PU2 · la capa retira la partida (su f es mayor que la del libro en 2,5 ÷ ventas medias) y la réplica del libro sigue conforme",
             lib.get("conforme") is True and cd.get("f") is not None and lib.get("C58") is not None and cd["f"] > lib["C58"], f"f capa {cd.get('f')} · f libro {lib.get('C58')}")
        # PU3 · sin el desglose
        c = preparar("EmpresaX_US_sin", declaracion(bloque=False, per="A0_total"))
        rc, out = correr(c)
        st, r = TS.estado(c), leer(c, "motor_a_f1_resultado.json")
        paso("PU3 · US GAAP con A0 y sin «arrendamientos_us_gaap»: el paso 7 termina en pendiente_de_datos con F1-US-DESGLOSE (ya no es un límite del modelo por F1-NORMA)",
             st.get("estado_analisis") == "pendiente_de_datos" and st.get("paso") == 7 and "F1-US-DESGLOSE" in bloquean(r) and "F1-NORMA" not in bloquean(r)
             and not os.path.exists(os.path.join(c, "fase_b.json")), f"estado {st.get('estado_analisis')} · paso {st.get('paso')} · bloquean {bloquean(r)}")
        c = preparar("EmpresaX_US_sin_A2", declaracion(bloque=False))
        rc, out = correr(c)
        st, dg = TS.estado(c), leer(c, "diagnostico.json")
        paso("PU3 · con A2 y sin el desglose la fila 86 del libro queda vacía (vacío ≠ 0), f no se calcula y el libro se declara incompleto: pendiente_de_datos en el "
             "paso 7, sin fase B (nunca un valor con la amortización supuesta a cero)",
             st.get("estado_analisis") == "pendiente_de_datos" and st.get("paso") == 7 and not os.path.exists(os.path.join(c, "fase_b.json")),
             f"estado {st.get('estado_analisis')} · paso {st.get('paso')} · {str((dg.get('causa') or {}).get('detalle'))[:220]}")
        # PU4 · C49 con importe y sin financieros
        c = preparar("EmpresaX_US_c49", declaracion(), con_c49=True)
        rc, out = correr(c)
        st, r = TS.estado(c), leer(c, "motor_a_f1_resultado.json")
        paso("PU4 · C49 con importe y sin arrendamientos financieros: pendiente_de_datos con F1-US-C49 (los pagos operativos ya están en el CFO)",
             st.get("estado_analisis") == "pendiente_de_datos" and st.get("paso") == 7 and "F1-US-C49" in bloquean(r),
             f"estado {st.get('estado_analisis')} · paso {st.get('paso')} · bloquean {bloquean(r)}")
        # PU5 · (R1-3, camino i) «fuera» falsa con cita real y fase1_partes
        c = preparar("EmpresaX_US_i", declaracion(ub_pas="fuera_de_las_filas_8_y_14"), circulante_extra=2.5, wc=WC + (L_PAS,), partes=True)
        rc, out = correr(c)
        st, r = TS.estado(c), leer(c, "motor_a_f1_resultado.json")
        g_f = [x for x in r.get("guardas") or [] if x["id"] == "F1-US-FILAS"]
        paso("PU5 · (R1-3 i) la variación del pasivo (2,5 al año) está dentro de la fila 14 y se declara «fuera» citando su línea: con fase1_partes el paso 7 termina en "
             "pendiente_de_datos (F1-US-FILAS, DATOS INVÁLIDOS); antes llegaba a concluido sin condición",
             st.get("estado_analisis") == "pendiente_de_datos" and st.get("paso") == 7 and bloquean(r) == ["F1-US-FILAS"] and g_f and g_f[0]["efecto"] == "DATOS INVÁLIDOS"
             and not os.path.exists(os.path.join(c, "fase_b.json")), f"estado {st.get('estado_analisis')} · paso {st.get('paso')} · {str(g_f[0]['detalle'])[:200] if g_f else bloquean(r)}")
        # PU6 · (R1-3, camino ii) «fila_8» con una cita real de una nota, sin línea que lo contraste
        d6 = declaracion()
        d6["arrendamientos_us_gaap"]["operativos"]["amortizacion_rou"] = {"ubicacion": "fila_8", "documento": DOC, "pagina": 1, "cita": NOTA_AM}
        d6["series"]["da_rou_operativo"] = serie({y: 3.0 for y in range(2016, 2026)})
        c = preparar("EmpresaX_US_ii", d6, notas=(NOTA_AM,), partes=True)
        rc, out = correr(c)
        st, r, fi = TS.estado(c), leer(c, "motor_a_f1_resultado.json"), leer(c, "ficha.json")
        f1b, linea = fi.get("motor_a_f1") or {}, linea_f1(c)
        ct = {k: v for k, v in (((r.get("condicionada") or {}).get("cota")) or {}).items() if isinstance(v, dict) and "dentro de la fila 8" in k}
        paso("PU6 · (R1-3 ii) amortización declarada «fila_8» (3,0 al año) con una cita real de una nota y una D&A que no la nombra: no se puede contrastar → llega a "
             "concluido, pero CONDICIONADA (antes: sin condición)", st.get("estado_analisis") == "concluido" and r.get("utilizable_para_conclusion") is True
             and "F1-US-FILAS" in str((r.get("condicionada") or {}).get("hipotesis")) and "CONDICIONADA" in str(r.get("rotulo")),
             f"estado {st.get('estado_analisis')} · paso {st.get('paso')} · bloquean {bloquean(r)} · {str(r.get('rotulo'))[:160]}")
        paso("PU6 · …con su cota exacta a la vista (el flujo bajaría en el importe declarado a la escala del año base) en la ficha y en la línea del informe; K3b «según lo "
             "declarado»", len(ct) == 1 and list(ct.values())[0]["variacion_maxima_del_flujo_sin_crecimiento_mm"] < -2.5
             and ((f1b.get("condicionada") or {}).get("cota") or {}).get("resumen") and "sin contrastar" in linea and "cota: el flujo sin crecimiento podría cambiar entre" in linea
             and "según lo declarado" in linea, linea[:420])
        # PU7 · D-US2 bis (caso Nike): los dos tramos dentro de la fila 14, en líneas mezcladas y partidas; pagos ≠ coste
        d7 = declaracion()
        op7 = d7["arrendamientos_us_gaap"]["operativos"]
        op7["amortizacion_rou"] = {"ubicacion": "fila_14", "documento": DOC, "pagina": 2, "cita": "prepaid expenses, operating lease right-of-use assets and other current and non-current assets"}
        op7["variacion_pasivo"] = {"ubicacion": "fila_14", "documento": DOC, "pagina": 2,
                                   "cita": "accounts payable, accrued liabilities, operating lease liabilities and other current and non-current liabilities"}
        c = preparar("EmpresaX_US_bis", d7, circulante_extra=-0.1, wc=("Accounts receivable", NIKE_ACT, NIKE_PAS), partes=True)
        rc, out = correr(c)
        st, r, fi = TS.estado(c), leer(c, "motor_a_f1_resultado.json"), leer(c, "ficha.json")
        f1b, linea = fi.get("motor_a_f1") or {}, linea_f1(c)
        bis = ((r.get("us_gaap") or {}).get("D_US2_bis") or {})
        paso("PU7 · (D-US2 bis, caso Nike) los dos tramos mezclados en líneas del circulante, pagos ≠ coste: NO bloquea; el expediente muestra las dos líneas; el libro "
             "V6.3.1 calcula lo declarado y el análisis llega a concluido", st.get("estado_analisis") == "concluido" and bloquean(r) == [] and bis.get("dos_lineas_comprobadas") is True
             and not any(x["id"] == "F1-LIBRO" and x["salta"] for x in r.get("guardas") or []), f"estado {st.get('estado_analisis')} · paso {st.get('paso')} · bloquean {bloquean(r)}")
        mm = ((bis.get("contando_los_pagos") or {}).get("variacion_maxima_del_flujo_sin_crecimiento_mm"))
        paso("PU7 · …se publica el valor de la hoja (coste contable) y, al lado, cuánto cambiaría contando los pagos (coste 3,3 y pagos 3,2 de media: +0,1 a la escala de "
             "las ventas medias), en el resultado, en la ficha y en la línea del informe", mm is not None and 0.05 < mm < 0.2 and "D-US2 bis" in str(r.get("rotulo"))
             and ((f1b.get("us_gaap") or {}).get("D_US2_bis") or {}).get("texto") and "D-US2 bis" in linea and "coste contable" in linea and "contando los pagos" in linea
             and "CONDICIONADA" not in linea, linea[:420])
        # PU8 · (R1-1, XB3) motor B, libro US GAAP y sin declaración F1
        c = preparar("EmpresaX_USB3", declaracion(), sin_decl=True)
        rc, out = correr(c, motor="B")
        st, r, fi = TS.estado(c), leer(c, "motor_a_f1_resultado.json"), leer(c, "ficha.json")
        rec = os.path.join(c, "recalc", "EmpresaX_USB3_v63_evaluada.xlsx")
        from v63_xml import LibroV63
        import motor_a_f1 as M
        crudo = LibroV63(rec).leer("Control maestro", "L4") if os.path.exists(rec) else None
        paso("PU8 · (R1-1) el libro que recalcula LibreOffice guarda «US GAAP» como texto compartido: el lector ligero devuelve su índice y la capa lo lee resuelto",
             crudo is not None and crudo != "US GAAP" and str(crudo).isdigit() and M._l4_del_libro(rec) == "US GAAP" and M.exigido_puente(c, libro=rec), f"LibroV63.leer → {crudo!r}")
        paso("PU8 · (R1-1, XB3) motor B con el libro US GAAP y SIN declaración F1: el gancho se ejecuta y el paso 7 termina en pendiente_de_datos (F1-NORMA y "
             "F1-US-DESGLOSE); antes llegaba a concluido sin evaluar el puente", st.get("motor") == "B" and st.get("estado_analisis") == "pendiente_de_datos" and st.get("paso") == 7
             and {"F1-NORMA", "F1-US-DESGLOSE"} <= set(bloquean(r)) and isinstance(fi.get("motor_a_f1"), dict) and fi["motor_a_f1"]["utilizable_para_conclusion"] is False
             and not os.path.exists(os.path.join(c, "fase_b.json")), f"estado {st.get('estado_analisis')} · paso {st.get('paso')} · motor {st.get('motor')} · bloquean {bloquean(r)}")
        # PU9 · (R1-1, XB4) motor B, libro US GAAP y declaración que dice NIIF
        d9 = declaracion()
        d9["norma_contable"]["valor"] = "NIIF"
        c = preparar("EmpresaX_USB4", d9)
        rc, out = correr(c, motor="B")
        st, r = TS.estado(c), leer(c, "motor_a_f1_resultado.json")
        paso("PU9 · (R1-1, XB4) motor B, libro US GAAP y declaración que dice NIIF: el gancho se ejecuta y el paso 7 termina en pendiente_de_datos con F1-NORMA (mezcla de normas)",
             st.get("estado_analisis") == "pendiente_de_datos" and st.get("paso") == 7 and "F1-NORMA" in bloquean(r)
             and any(x["id"] == "F1-NORMA" and "mezcla de normas" in str(x["detalle"]) for x in r.get("guardas") or []), f"estado {st.get('estado_analisis')} · paso {st.get('paso')} · bloquean {bloquean(r)}")
        # PU10 · (R1-9, XB2) motor B con el puente conforme
        d10 = declaracion()
        d10["series"]["pasivo_arr_operativo"] = serie({2025: 0})
        c = preparar("EmpresaX_USB2", d10, fila23=0)
        rc, out = correr(c, motor="B")
        st, r, fi = TS.estado(c), leer(c, "motor_a_f1_resultado.json"), leer(c, "ficha.json")
        f1b, linea = fi.get("motor_a_f1") or {}, linea_f1(c)
        paso("PU10 · (XB2) motor B con US GAAP, la fila 23 a cero y el pasivo operativo 0 declarado: F1 se evalúa en los pasos 7 y 12 y no bloquea; el pipeline llega al paso 14",
             st.get("motor") == "B" and st.get("paso") == 14 and (st.get("motor_a_f1") or {}).get("paso") == 12 and r.get("utilizable_para_conclusion") is True
             and "motor B utilizable" in str(r.get("rotulo")), f"estado {st.get('estado_analisis')} · paso {st.get('paso')} · bloquean {bloquean(r)}")
        paso("PU10 · (R1-9) la línea del informe habla del puente de deuda (ya no dice «caja base por dos vías sin explicar» ni «perímetro declarado: sin declarar») y la "
             "ficha lleva el aviso de lo que F1 no mira con el motor B (el ancla de S2C y el ROIC)", "Motor B · F1:" in linea and "puente de deuda: alquiler contado una vez" in linea
             and "sin explicar" not in linea and "sin declarar" not in linea and any(a.get("id") == "F1-US-ANCLA" for a in f1b.get("avisos") or []), linea[:330])
        # PU11 · (R1-11) la norma de la fase 1, fuera de la lista cerrada
        c = preparar("EmpresaX_US_norma", declaracion(), norma="U.S. GAAP")
        rc, out = correr(c)
        st, dg = TS.estado(c), leer(c, "diagnostico.json")
        paso("PU11 · (R1-11) «norma_contable» = «U.S. GAAP» en fase1_v63.json: el paso 2 termina en pendiente_de_datos con el motivo, antes de gastar la fase A (antes: paso 7)",
             st.get("estado_analisis") == "pendiente_de_datos" and st.get("paso") == 2 and "lista cerrada" in str((dg.get("causa") or {}).get("detalle"))
             and not os.path.exists(os.path.join(c, "fase_a.json")), f"estado {st.get('estado_analisis')} · paso {st.get('paso')} · {str((dg.get('causa') or {}).get('detalle'))[:160]}")
        # ---------------------------------------------------------------- cierre de la ronda 2 (revisión R2)
        SEN = "Loss on lease termination"
        fuera_ = "fuera_de_las_filas_8_y_14"
        # PU12 · (R2-1) línea que nombra el arrendamiento sin ser un tramo: declaración veraz y declaración falsa
        c = preparar("EmpresaX_US_r21h", declaracion(), circulante_extra=2.5, wc=WC + ("Accrued and other liabilities",), fuera=(SEN,), partes=True)
        rc, out = correr(c)
        st, r, linea = TS.estado(c), leer(c, "motor_a_f1_resultado.json"), linea_f1(c)
        aj = (((r.get("us_gaap") or {}).get("contraste_de_ubicaciones") or {}).get("lineas_ajenas_al_tramo") or [])
        paso("PU12 · (R2-1, Y4h) el estado de flujos lleva «Loss on lease termination» (no es un tramo) y la declaración es VERAZ («no_publicada» los dos): ya no se bloquea; "
             "llega a concluido CONDICIONADA (D-US1), con la cota en el informe y la línea ajena a la vista (antes: pendiente_de_datos en el paso 7)",
             st.get("estado_analisis") == "concluido" and bloquean(r) == [] and (r.get("condicionada") or {}).get("hipotesis") == "D-US1" and "CONDICIONADA" in linea
             and "cota: el flujo sin crecimiento podría cambiar entre" in linea and any(SEN in x for x in aj),
             f"estado {st.get('estado_analisis')} · paso {st.get('paso')} · bloquean {bloquean(r)} · ajenas {aj}")
        d12 = declaracion()
        for k_ in ("amortizacion_rou", "variacion_pasivo"):
            d12["arrendamientos_us_gaap"]["operativos"][k_] = {"ubicacion": fuera_, "documento": DOC, "pagina": 2, "cita": SEN}
        c = preparar("EmpresaX_US_r21", d12, circulante_extra=2.5, wc=WC + ("Accrued and other liabilities",), fuera=(SEN,), partes=True)
        rc, out = correr(c)
        st, r = TS.estado(c), leer(c, "motor_a_f1_resultado.json")
        g_f = [x for x in r.get("guardas") or [] if x["id"] == "F1-US-FILAS"]
        paso("PU12 · (R2-1, Y4) los dos tramos declarados «fuera» citando esa línea: no vale como línea del tramo → pendiente_de_datos en el paso 7 (F1-US-FILAS, "
             "INCOMPLETO), sin fase B (antes: concluido sin condición, con el valor sobrestimado)",
             st.get("estado_analisis") == "pendiente_de_datos" and st.get("paso") == 7 and bloquean(r) == ["F1-US-FILAS"] and g_f and g_f[0]["efecto"] == "INCOMPLETO"
             and "junto a otra cosa" in str(g_f[0]["detalle"]) and not os.path.exists(os.path.join(c, "fase_b.json")),
             f"estado {st.get('estado_analisis')} · paso {st.get('paso')} · {str(g_f[0]['detalle'])[:160] if g_f else bloquean(r)}")
        # PU13 · (R2-2) importe cero en un tramo cuya línea propia está sumada en la fila 14
        d13 = declaracion(ub_pas="fila_14", ajuste=0)
        d13["arrendamientos_us_gaap"]["operativos"]["amortizacion_rou"] = {"ubicacion": fuera_, "documento": DOC, "pagina": 2, "cita": "Non-cash lease expense"}
        c = preparar("EmpresaX_US_r22", d13, circulante_extra=2.5, wc=WC + (L_PAS,), fuera=("Non-cash lease expense",), partes=True)
        rc, out = correr(c)
        st, r = TS.estado(c), leer(c, "motor_a_f1_resultado.json")
        g_f = [x for x in r.get("guardas") or [] if x["id"] == "F1-US-FILAS"]
        paso("PU13 · (R2-2, Y5) «Operating lease liabilities» (2,5 al año) es una línea propia sumada en la fila 14 y se declara «fila_14» con importe 0: el importe dentro "
             "de la fila es el de su línea → pendiente_de_datos en el paso 7 (F1-US-FILAS, DATOS INVÁLIDOS), sin fase B (antes: concluido sin condición)",
             st.get("estado_analisis") == "pendiente_de_datos" and st.get("paso") == 7 and bloquean(r) == ["F1-US-FILAS"] and g_f and g_f[0]["efecto"] == "DATOS INVÁLIDOS"
             and "el importe dentro de la fila es el de su línea" in str(g_f[0]["detalle"]) and not os.path.exists(os.path.join(c, "fase_b.json")),
             f"estado {st.get('estado_analisis')} · paso {st.get('paso')} · {str(g_f[0]['detalle'])[:200] if g_f else bloquean(r)}")
        # PU14 · «Otro» como norma de la fase 1, con el motor B
        c = preparar("EmpresaX_US_otro", declaracion(), norma="Otro", sin_decl=True)
        rc, out = correr(c, motor="B")
        st, r, dg = TS.estado(c), leer(c, "motor_a_f1_resultado.json"), leer(c, "diagnostico.json")
        paso("PU14 · («Otro», Y9) motor B con «Otro» como norma de la fase 1 en un expediente de la 4.15: el paso 7 termina en no_entregable · límite del modelo (F1 no "
             "tiene regla para otras normas; ningún dato lo arregla); antes, pendiente_de_datos",
             st.get("motor") == "B" and st.get("estado_analisis") == "no_entregable" and st.get("paso") == 7 and (dg.get("causa") or {}).get("tipo") == "limite_del_modelo"
             and bloquean(r) == ["F1-NORMA"] and not os.path.exists(os.path.join(c, "fase_b.json")),
             f"estado {st.get('estado_analisis')} · paso {st.get('paso')} · causa {(dg.get('causa') or {}).get('tipo')} · bloquean {bloquean(r)}")
    finally:
        shutil.rmtree(TS.BASE, ignore_errors=True)
        TS.BASE = base0
    n = sum(ok for _, ok in RES)
    linea = f"{n}/{len(RES)} pruebas de F1 · US GAAP en el pipeline PASAN"
    print(linea)
    if salida:
        open(salida, "w", encoding="utf-8").write("\n".join(f"{'PASA ' if ok else 'FALLA'} · {x}" for x, ok in RES) + "\n" + linea + "\n")
    return 0 if n == len(RES) else 1


if __name__ == "__main__":
    sys.exit(main())
