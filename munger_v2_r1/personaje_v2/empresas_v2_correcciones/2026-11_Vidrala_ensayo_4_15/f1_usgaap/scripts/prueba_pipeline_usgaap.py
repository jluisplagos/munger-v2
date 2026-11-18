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
        análisis llega a concluido; la ficha y el informe dicen que la conclusión es CONDICIONADA y muestran coste lineal − pagos (D-US2).
  PU2 · la variación del pasivo declarada dentro de la fila 14, con su importe: el paso 7 termina en no_entregable · límite del modelo
        (F1-LIBRO: ningún libro la retira del circulante).
  PU3 · sin «arrendamientos_us_gaap»: pendiente_de_datos en el paso 7, ya no un límite del modelo. Con A0 declarado lo dice la capa
        (F1-US-DESGLOSE); con A2, el propio libro: sin la clasificación la fila 86 queda vacía, f no se calcula y el libro lo declara
        incompleto (Motor V05) antes de llegar a la capa.
  PU4 · C49 con importe (pagos de arrendamientos en financiación) y sin financieros declarados: pendiente_de_datos (F1-US-C49).
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

CFG631 = os.path.join(PV, "config_v2_v631_f1.json")
DOC = "informe anual sintético"
REG = {"fecha": "2026-11-18", "persona": "prueba sintética F1 · US GAAP (no es una decisión)", "motivo": "caso de prueba de extremo a extremo"}
PAG2 = ("CONSOLIDATED STATEMENTS OF CASH FLOWS\nNet income\nDepreciation and amortization\nStock-based compensation\nChanges in working capital\n"
        "Net cash provided by operating activities\nPurchases of property and equipment\n")
RES = []


def paso(nombre, ok, detalle=""):
    RES.append((nombre, bool(ok)))
    print(("PASA " if ok else "FALLA") + " · " + nombre + (f" · {detalle}" if detalle else ""))


def serie(vals):
    return {str(y): {"valor_fuente": v, "signo": 1, "tratamiento": "ninguno", "documento": DOC, "pagina": 1, "literal": repr(v), "archivo": PF.FUENTE} for y, v in vals.items()}


def declaracion(bloque=True, ub_pas="no_publicada", ajuste=None, financieros=False, per="A2_propio"):
    d = PF.declaracion("US_GAAP")
    d["conciliacion_fcf_base"] = [p for p in d["conciliacion_fcf_base"] if p["componente"] != "C48"]   # con US GAAP C48 y la fila 16 van a cero
    for k in ("perimetro_reinversion", "perimetro_palancas_s2c", "perimetro_roic"):
        d[k]["valor"] = per
    del d["series"]["da_rou"]   # sin arrendamientos financieros (lo dice la clasificación, con su evidencia)
    if bloque:
        ev = {"documento": DOC, "pagina": 1}
        np_ = {"ubicacion": "no_publicada", "documento": DOC, "pagina": 2}
        d["arrendamientos_us_gaap"] = {
            "registro": REG,
            "operativos": dict(ev, cita="Operating lease cost", existen=True, amortizacion_rou=dict(np_),
                               variacion_pasivo=dict(np_) if ub_pas == "no_publicada" else dict(ev, cita="Operating lease liabilities", ubicacion=ub_pas)),
            "financieros": dict(ev, cita="The Company has no finance leases", existen=financieros)}
        d["series"].update({"pagos_arr_operativo": serie({2023: 3.0, 2024: 3.2, 2025: 3.4}), "coste_arr_operativo": serie({2023: 3.1, 2024: 3.3, 2025: 3.5}),
                            "pasivo_arr_operativo": serie({2025: 50})})
        if ajuste is not None:
            d["series"]["circulante_arr_operativo"] = serie({y: ajuste for y in range(2021, 2026)})
    return d


def escribir_fuente(c, d):
    lits = sorted({str(e.get("literal")) for s_ in (d.get("series") or {}).values() for e in s_.values() if isinstance(e, dict)})
    txt = ("[PDF PAGE 1]\nInforme anual sintético (US GAAP): " + " ".join(lits) + "\nOperating lease cost\nOperating lease liabilities\n"
           "The Company has no finance leases\n[PDF PAGE 2]\n" + PAG2 + "[PDF PAGE 3]\n")
    open(os.path.join(c, PF.FUENTE), "w", encoding="utf-8").write(txt)
    d["fuentes_series"] = {DOC: {"archivo": PF.FUENTE, "sha256": hashlib.sha256(txt.encode("utf-8")).hexdigest()}}


def preparar(nombre, d, circulante_extra=0.0, con_c49=False):
    """La empresa sintética como empresa US GAAP (ver la cabecera)."""
    c = TS.preparar(nombre, quitar_etapa1=("C48",) if con_c49 else ("C48", "C49"))
    json.dump({"modo": "registrada", "motivo": "prueba F1 · US GAAP: el valor de la etapa 1 prevalece en la empresa sintética"},
              open(os.path.join(c, "entrada_efectiva.json"), "w", encoding="utf-8"))
    p = os.path.join(c, "fase1_v63.json")
    f1 = json.load(open(p, encoding="utf-8"))
    f1["norma_contable"] = "US GAAP"
    f1["analisis"]["C48"]["valor"] = 0
    f1["historia"]["partidas"]["intereses_financiacion"]["valores"] = [0] * 10
    if not con_c49:
        f1["analisis"]["C49"]["valor"] = 0
        f1["historia"]["partidas"]["arrendamientos_principal"]["valores"] = [0] * 10
    if circulante_extra:
        w = f1["historia"]["partidas"]["circulante"]["valores"]
        f1["historia"]["partidas"]["circulante"]["valores"] = w[:5] + [x + circulante_extra for x in w[5:]]
    json.dump(f1, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    escribir_fuente(c, d)
    json.dump(d, open(os.path.join(c, "motor_a_f1.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return c


def correr(c):
    os.environ["MUNGER_CONFIG"] = CFG631
    try:
        return TS.correr(c, TS.reaccion_normal())
    finally:
        os.environ.pop("MUNGER_CONFIG", None)


def leer(c, n):
    p = os.path.join(c, n)
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}


def bloquean(r):
    return sorted({g["id"] for g in r.get("guardas") or [] if g.get("salta") and g.get("severidad") == "BLOQUEA"})


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
        paso("PU1 · K3: alquiler contado una vez y K3 conforme; F1-SERIES sin problemas (series de US GAAP, citas y página examinada)",
             k3.get("K3b_alquiler_contado") == "una vez" and k3.get("conforme") is True and not any(x["id"] == "F1-SERIES" and x["salta"] for x in r.get("guardas") or []),
             json.dumps(k3, ensure_ascii=False)[:200])
        f1b = fi.get("motor_a_f1") or {}
        inf = open(os.path.join(c, "informe.md"), encoding="utf-8").read() if os.path.exists(os.path.join(c, "informe.md")) else ""
        linea = next((x for x in inf.splitlines() if "Motor A · F1:" in x), "")
        paso("PU1 · estado final concluido; la ficha dice que la conclusión es CONDICIONADA (hipótesis D-US1, con su registro y su cota) y muestra coste lineal − pagos (D-US2)",
             st.get("estado_analisis") == "concluido" and fi.get("estado_analisis") == "concluido" and f1b.get("utilizable_para_conclusion") is True
             and (f1b.get("condicionada") or {}).get("hipotesis") == "D-US1" and ((f1b.get("condicionada") or {}).get("registro") or {}).get("fecha") == "2026-11-18"
             and (f1b.get("condicionada") or {}).get("cota") and abs(((f1b.get("us_gaap") or {}).get("diferencia_coste_lineal_menos_pagos") or {}).get("coste_menos_pagos_medio", 0) - 0.1) < 1e-9
             and any(a.get("id") == "F1-US-HIPOTESIS" for a in f1b.get("avisos") or []),
             f"estado {st.get('estado_analisis')} · ficha {fi.get('estado_analisis')} · {str(f1b.get('rotulo'))[:120]}")
        paso("PU1 · el informe lo dice en su línea F1: «CONDICIONADA», la hipótesis y «se cuentan los pagos» con la diferencia",
             "CONDICIONADA" in linea and "D-US1" in linea and "se cuentan los pagos" in linea and "+0.100" in linea, linea[:260])
        pu = ((r.get("us_gaap") or {}).get("puente_de_deuda") or {})
        paso("PU1 · puente: con el motor A, F1-US-PUENTE informa de los 50 de pasivo operativo en la fila 23 (deuda coherente de un puente = fila 22)",
             any(x["id"] == "F1-US-PUENTE" and x["salta"] and x["severidad"] == "INFORMA" for x in r.get("guardas") or [])
             and pu.get("deuda_del_puente_coherente") == pu.get("deuda_financiera_fila_22") and pu.get("pasivo_operativo_dentro_de_la_fila_23") == 50.0, json.dumps(pu, ensure_ascii=False)[:200])
        # PU2 · la variación del pasivo dentro de la fila 14
        c = preparar("EmpresaX_US14", declaracion(ub_pas="fila_14", ajuste=2.5), circulante_extra=2.5)
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
