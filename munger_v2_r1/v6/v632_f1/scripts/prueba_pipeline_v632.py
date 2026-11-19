#!/usr/bin/env python3
"""Prueba de extremo a extremo de la V6.3.2 F1 en el pipeline (V-CIRC, 19-nov-2026), con la empresa sintética y los agentes simulados de
test_pipeline_sintetico.py y las ayudas de prueba_pipeline_f1.py (LibreOffice: ejecutar con flock /home/user/e_work/libreoffice.lock).
Directorio temporal; no toca la batería sintética ni su línea de base, ni las pruebas de la V6.3.1.

Uso (desde cualquier carpeta): flock … python3 -B prueba_pipeline_v632.py [SALIDA.txt]
Empresa sintética SIN arrendamientos ni PPA (perímetro A0 declarado, como P2 de prueba_pipeline_f1.py), con circulante positivo (consume caja).
  Q1 · con config_v2_v632_f1.json, la caja base sin el circulante (C46 = CFO + circulante medio de la ventana, con su partida en
       conciliacion_fcf_base) y la normalización declarada 2021–2025: plantilla_activa.json V6.3.2; el paso 2 la aplica al libro (C93, C94:L94);
       C97 «circulante_a_cero»; F1 no bloquea en los pasos 7 y 12 (F1-LIBRO, F1-CIRC y F1-K3c no saltan) y el análisis llega a concluido; la
       ficha lleva la versión V6.3.2 F1 y el bloque de la normalización; el informe, la línea; datos_v63.md, la nota para las fases; el resumen va a
       resumen_v2_v632_f1.csv.
  Q2 · la misma empresa con la V6.3.2 y SIN normalización: C97 «ninguna», concluido; ni la ficha ni datos_v63.md hablan de normalización.
  Q3 · la declaración de Q1 con config_v2_v631_f1.json (V6.3.1): el paso 7 termina en no_entregable · límite del modelo con F1-LIBRO.
"""
import json
import os
import shutil
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", "..", ".."))
PV = os.path.join(RAIZ, "personaje_v2")
sys.path.insert(0, os.path.join(PV, "pruebas"))
sys.path.insert(0, os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_15", "f1_impl", "scripts"))
sys.path.insert(0, os.path.join(PV, "scripts"))
sys.dont_write_bytecode = True
import test_pipeline_sintetico as TS  # noqa: E402
import prueba_pipeline_f1 as PF  # noqa: E402

CFG632 = os.path.join(PV, "config_v2_v632_f1.json")
CFG631 = os.path.join(PV, "config_v2_v631_f1.json")
REG = {"fecha": "2026-11-19", "persona": "prueba sintética V-CIRC (no es una decisión)", "motivo": "caso de prueba de extremo a extremo"}
RES = []


def paso(nombre, ok, detalle=""):
    RES.append((nombre, bool(ok)))
    print(("PASA " if ok else "FALLA") + " · " + nombre + (f" · {detalle}" if detalle else ""))


def historia():
    f1 = json.load(open(os.path.join(PV, "esquema", "fase1_v63.ejemplo.json"), encoding="utf-8"))
    n, h = f1["anios_fcf_base"], f1["historia"]["partidas"]
    return f1, n, h


def declaracion(normalizar):
    d = PF.declaracion()
    if normalizar:
        f1, n, h = historia()
        cfo = sum(h["cfo"]["valores"][-n:]) / n
        wc = sum(h["circulante"]["valores"][-n:]) / n
        c46 = round(cfo + wc, 2)   # la etapa 1 registra con 2 decimales, como en la empresa sintética
        d["conciliacion_fcf_base"] = [e for e in d["conciliacion_fcf_base"] if e["componente"] != "C46"] + [
            {"componente": "C46", "importe": wc, "partida": "circulante de la ventana excluido del CFO en C46 (la caja base no lo cuenta)",
             "fuente": {"documento": "fase1_v63.ejemplo.json (Historia, fila 14)", "pagina": None}},
            {"componente": "C46", "importe": c46 - cfo - wc, "partida": "C46 registrado con 2 decimales en la etapa 1",
             "fuente": {"documento": "EmpresaX_v53_evaluada_sintetica.xlsx (Análisis) y fase1_v63.ejemplo.json (Historia)", "pagina": None}}]
        d["normalizacion_circulante"] = {"regla": "circulante_a_cero", "anios": [2021, 2022, 2023, 2024, 2025],
                                         "fundamento": "prueba: la caja base (C46) excluye el circulante; decisión V-CIRC (a): tampoco en la reinversión", "registro": REG}
    return d


def preparar(nombre, normalizar):
    c = PF.preparar(nombre, declaracion(normalizar), sin_arrendamientos=True)
    if normalizar:   # la caja base sin el circulante: C46 de la etapa 1 (manda en el modo registrado) y de fase1_v63.json
        f1, n, h = historia()
        cfo = sum(h["cfo"]["valores"][-n:]) / n
        wc = sum(h["circulante"]["valores"][-n:]) / n
        import openpyxl
        e1 = os.path.join(c, "etapa1", f"{nombre}_evaluada.xlsx")
        wb = openpyxl.load_workbook(e1)
        wb["Análisis"]["C46"] = round(cfo + wc, 2)
        wb.save(e1)
        p = os.path.join(c, "fase1_v63.json")
        f = json.load(open(p, encoding="utf-8"))
        f["analisis"]["C46"]["valor"] = cfo + wc
        json.dump(f, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return c


def correr(c, cfg):
    os.environ["MUNGER_CONFIG"] = cfg
    try:
        return TS.correr(c, TS.reaccion_normal())
    finally:
        os.environ.pop("MUNGER_CONFIG", None)


def leer(c, n):
    p = os.path.join(c, n)
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}


def texto(c, n):
    p = os.path.join(c, n)
    return open(p, encoding="utf-8").read() if os.path.exists(p) else ""


def bloquean(r):
    return [g["id"] + ": " + str(g["detalle"])[:120] for g in r.get("guardas") or [] if g.get("salta") and g.get("severidad") == "BLOQUEA"]


def salta(r, gid):
    return any(g.get("salta") for g in r.get("guardas") or [] if g.get("id") == gid)


def main():
    salida = sys.argv[1] if len(sys.argv) > 1 else None
    base0, TS.BASE = TS.BASE, tempfile.mkdtemp(prefix="v632_pipe_")
    try:
        from openpyxl import load_workbook
        # Q1
        c = preparar("EmpresaX_V632", True)
        rc, out = correr(c, CFG632)
        st, r, fi, pa = TS.estado(c), leer(c, "motor_a_f1_resultado.json"), leer(c, "ficha.json"), leer(c, "plantilla_activa.json")
        ev = os.path.join(c, "recalc", "EmpresaX_V632_v63_evaluada.xlsx")
        h = load_workbook(ev, data_only=True)["Historia"] if os.path.exists(ev) else None
        paso("Q1 · V6.3.2: plantilla_activa.json registra la V6.3.2 F1; el paso 2 escribió la normalización (C93, C94:L94 = 1 en 2021–2025) y C97 es «circulante_a_cero»",
             pa.get("version") == "V6.3.2 F1" and h is not None and h["C93"].value == "circulante_a_cero" and [h[f"{x}94"].value for x in "HIJKL"] == [1] * 5
             and h["G94"].value is None and h["C97"].value == "circulante_a_cero" and all(h[f"{x}96"].value == 0 for x in "HIJKL"),
             f"plantilla {pa.get('version')} · C97 {h['C97'].value if h else None!r}")
        nc = r.get("normalizacion_circulante") or {}
        paso("Q1 · F1 no bloquea (F1-LIBRO, F1-CIRC, F1-K3c y F1-REPLICA no saltan), la capa aplica la normalización y el gancho corre en los pasos 7 y 12",
             r.get("utilizable_para_conclusion") is True and not any(salta(r, x) for x in ("F1-LIBRO", "F1-CIRC", "F1-K3c", "F1-REPLICA")) and nc.get("aplicada") is True
             and (st.get("motor_a_f1") or {}).get("paso") == 12 and (r.get("libro_v631_f1") or {}).get("motivos") == [],
             f"código {rc} · estado {st.get('estado_analisis')} · paso {st.get('paso')} · bloquean {bloquean(r)}")
        paso("Q1 · estado final concluido; la ficha lleva la plantilla V6.3.2 F1 y, en motor_a_f1, la normalización aplicada (años y caja base)",
             st.get("estado_analisis") == "concluido" and fi.get("estado_analisis") == "concluido" and (fi.get("versiones") or {}).get("plantilla") == "V6.3.2 F1"
             and ((fi.get("motor_a_f1") or {}).get("normalizacion_circulante") or {}).get("aplicada") is True
             and ((fi.get("motor_a_f1") or {}).get("normalizacion_circulante") or {}).get("anios") == [2021, 2022, 2023, 2024, 2025] and "configuracion_economica" not in fi,
             f"estado {st.get('estado_analisis')} · ficha {fi.get('estado_analisis')}")
        paso("Q1 · el informe dice el circulante normalizado y datos_v63.md da a las fases la nota de la normalización con lo excluido por año",
             "circulante normalizado a cero en [2021, 2022, 2023, 2024, 2025]" in texto(c, "informe.md")
             and "Normalización declarada del circulante (libro V6.3.2 F1" in texto(c, "datos_v63.md"))
        paso("Q1 · el resumen va a resumen_v2_v632_f1.csv (ni al de la V6.3 ni al de la V6.3.1)",
             os.path.exists(os.path.join(TS.BASE, "resumen_v2_v632_f1.csv")) and not os.path.exists(os.path.join(TS.BASE, "resumen_v2.csv"))
             and not os.path.exists(os.path.join(TS.BASE, "resumen_v2_v631_f1.csv")), str(sorted(x for x in os.listdir(TS.BASE) if x.endswith(".csv"))))
        f_q1 = (r.get("calculo_perimetro_declarado") or {}).get("f")
        # Q2
        c2 = preparar("EmpresaX_V632_sin", False)
        rc2, _ = correr(c2, CFG632)
        st2, r2, fi2 = TS.estado(c2), leer(c2, "motor_a_f1_resultado.json"), leer(c2, "ficha.json")
        ev2 = os.path.join(c2, "recalc", "EmpresaX_V632_sin_v63_evaluada.xlsx")
        h2 = load_workbook(ev2, data_only=True)["Historia"] if os.path.exists(ev2) else None
        paso("Q2 · V6.3.2 sin normalización: C97 «ninguna», concluido, sin bloque de normalización en el resultado ni en la ficha ni nota en datos_v63.md",
             h2 is not None and h2["C97"].value == "ninguna" and st2.get("estado_analisis") == "concluido" and "normalizacion_circulante" not in r2
             and "normalizacion_circulante" not in (fi2.get("motor_a_f1") or {}) and "Normalización declarada del circulante" not in texto(c2, "datos_v63.md")
             and (fi2.get("versiones") or {}).get("plantilla") == "V6.3.2 F1", f"código {rc2} · estado {st2.get('estado_analisis')} · bloquean {bloquean(r2)}")
        f_q2 = (r2.get("calculo_perimetro_declarado") or {}).get("f")
        paso("Q1/Q2 · con el circulante fuera de la caja base Y de la reinversión, f es la misma que con el circulante en las dos (solo cambia el redondeo de C46)",
             f_q1 is not None and f_q2 is not None and abs(f_q1 - f_q2) < 1e-5, f"f Q1 {f_q1} · Q2 {f_q2}")
        # Q3
        c3 = preparar("EmpresaX_V631_norm", True)
        rc3, _ = correr(c3, CFG631)
        st3, r3 = TS.estado(c3), leer(c3, "motor_a_f1_resultado.json")
        dg = leer(c3, "diagnostico.json")
        g3 = [x for x in r3.get("guardas") or [] if x["id"] == "F1-LIBRO"]
        paso("Q3 · la declaración con la normalización y la V6.3.1: el paso 7 termina en no_entregable · límite del modelo con F1-LIBRO (la V6.3.1 no la calcula)",
             st3.get("estado_analisis") == "no_entregable" and st3.get("paso") == 7 and (dg.get("causa") or {}).get("tipo") == "limite_del_modelo"
             and g3 and g3[0]["salta"] and "V6.3.2 F1" in g3[0]["detalle"], f"estado {st3.get('estado_analisis')} · paso {st3.get('paso')} · {bloquean(r3)[:2]}")
    finally:
        shutil.rmtree(TS.BASE, ignore_errors=True)
        TS.BASE = base0
    n = sum(ok for _, ok in RES)
    linea = f"{n}/{len(RES)} pruebas de la V6.3.2 F1 en el pipeline PASAN"
    print(linea)
    if salida:
        open(salida, "w", encoding="utf-8").write("\n".join(f"{'PASA ' if ok else 'FALLA'} · {x}" for x, ok in RES) + "\n" + linea + "\n")
    return 0 if n == len(RES) else 1


if __name__ == "__main__":
    sys.exit(main())
