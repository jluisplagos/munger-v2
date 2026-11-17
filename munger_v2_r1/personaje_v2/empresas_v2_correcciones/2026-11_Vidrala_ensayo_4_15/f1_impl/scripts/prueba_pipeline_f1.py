#!/usr/bin/env python3
"""Prueba de extremo a extremo del gancho F1 del pipeline (F1-IMPL, 4.15), con la empresa sintética y los agentes simulados de
test_pipeline_sintetico.py (LibreOffice: ejecutar con flock /home/user/e_work/libreoffice.lock). Directorio temporal; no toca la batería
sintética ni su línea de base.

Uso (desde personaje_v2/): flock … python3 -B empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_15/f1_impl/scripts/prueba_pipeline_f1.py SALIDA.txt
Casos:
  P1 · expediente de la 4.15 (entrada_efectiva.json) con motor A y SIN declaración F1: el paso 7 termina en pendiente_de_datos con el
       diagnóstico F1 (nunca un resultado silencioso).
  P2 · con una declaración F1 completa de una empresa sin arrendamientos ni PPA (C49 = 0, ROU = PPA = 0 declaradas, sin compras, sin
       transición, un solo perímetro A0): el gancho deja seguir; el pipeline llega a su estado final y la ficha lleva el bloque motor_a_f1
       «utilizable».
  P3 · la misma con US GAAP declarada: el paso 7 termina en no_entregable · límite del modelo (F1-NORMA).
  P4 · (revisión H2) sin entrada_efectiva.json ni declaración, con arrendamientos en el libro y sin la marca de la línea de base: se exige F1.
  P5 · (revisión H1) declaración cambiada después de un cierre concluido y relanzamiento con «--desde 13»: ninguna ficha oficial concluido.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

PV = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(PV, "pruebas"))
sys.dont_write_bytecode = True
import test_pipeline_sintetico as TS  # noqa: E402

RES = []
REG = {"fecha": "2026-11-17", "persona": "prueba sintética F1-IMPL", "motivo": "caso de prueba de extremo a extremo"}


def paso(nombre, ok, detalle=""):
    RES.append((nombre, bool(ok)))
    print(("PASA " if ok else "FALLA") + " · " + nombre + (f" · {detalle}" if detalle else ""))


def conciliacion_sintetica():
    """K3a: las entradas C46–C50 de la etapa 1 sintética (V5.3) están redondeadas a 2 decimales frente a las medias de la Historia de
    fase1_v63.json: cada diferencia se declara como partida, con su fuente (las dos tablas de la empresa inventada)."""
    import openpyxl
    a = openpyxl.load_workbook(os.path.join(PV, "pruebas", "sintetico", "_origen", "EmpresaX_v53_evaluada_sintetica.xlsx"), data_only=True)["Análisis"]
    f1 = json.load(open(os.path.join(PV, "esquema", "fase1_v63.ejemplo.json"), encoding="utf-8"))
    n, h = f1["anios_fcf_base"], f1["historia"]["partidas"]
    out = []
    for celda, partida, signo in (("C46", "cfo", 1), ("C47", "capex", -1), ("C48", "intereses_financiacion", -1), ("C50", "sbc", -1)):
        d = signo * (a[celda].value - sum(h[partida]["valores"][-n:]) / n)
        out.append({"componente": celda, "importe": d, "partida": f"{celda} registrado con 2 decimales en la etapa 1 frente a la media de la Historia",
                    "fuente": {"documento": "EmpresaX_v53_evaluada_sintetica.xlsx (Análisis) y fase1_v63.ejemplo.json (Historia)", "pagina": None}})
    return out


def declaracion(norma="NIIF"):
    cero = {str(y): {"valor_fuente": 0, "signo": 1, "tratamiento": "ninguno", "documento": "informe anual sintético", "pagina": 1} for y in range(2016, 2026)}
    return {"norma_contable": {"valor": norma, "registro": REG}, "perimetro_reinversion": {"valor": "A0_total", "registro": REG},
            "perimetro_margen": {"valor": "EBIT_NIIF16_PPA_constante", "registro": REG}, "perimetro_palancas_s2c": {"valor": "A0_total", "registro": REG},
            "perimetro_roic": {"valor": "A0_total", "registro": REG}, "clasificacion_compras": {"valor": "sin_compras", "registro": REG},
            "transicion": {"conocida": False, "tratamiento": None, "registro": REG}, "series": {"da_rou": cero, "da_ppa": dict(cero)},
            "conciliacion_fcf_base": conciliacion_sintetica()}


def preparar(nombre, decl=None, sin_arrendamientos=False, con_4_15=True, renombrar=False):
    c = TS.preparar(nombre, quitar_etapa1=(("C49",) if sin_arrendamientos else ()))  # sin el valor migrado de la etapa 1, manda fase1_v63.json
    if con_4_15:
        json.dump({"modo": "registrada", "motivo": "prueba F1-IMPL: el valor de la etapa 1 prevalece en la empresa sintética"},
                  open(os.path.join(c, "entrada_efectiva.json"), "w", encoding="utf-8"))
    if renombrar:  # sin la marca «(inventada)»: no es la línea de base sintética v2.2, así que no queda exenta
        p1 = os.path.join(c, "fase1_v63.json")
        f1 = json.load(open(p1, encoding="utf-8"))
        f1["empresa"] = "Empresa Y (prueba F1)"
        json.dump(f1, open(p1, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    if sin_arrendamientos:
        p = os.path.join(c, "fase1_v63.json")
        f1 = json.load(open(p, encoding="utf-8"))
        f1["analisis"]["C49"]["valor"] = 0
        pr = f1["historia"]["partidas"].get("arrendamientos_principal")
        if pr:
            pr["valores"] = [0] * 10
        pa = f1["historia"]["partidas"].get("arrendamientos")
        if pa:
            pa["valores"] = [0] * 10
        json.dump(f1, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    if decl is not None:
        json.dump(decl, open(os.path.join(c, "motor_a_f1.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return c


def main():
    salida = sys.argv[1] if len(sys.argv) > 1 else None
    base0, TS.BASE = TS.BASE, tempfile.mkdtemp(prefix="f1_pipe_")
    try:
        reac = TS.reaccion_normal()
        # P1
        c = preparar("EmpresaX")
        rc, out = TS.correr(c, reac)
        st = TS.estado(c)
        r = json.load(open(os.path.join(c, "motor_a_f1_resultado.json"), encoding="utf-8")) if os.path.exists(os.path.join(c, "motor_a_f1_resultado.json")) else {}
        dg = open(os.path.join(c, "diagnostico.md"), encoding="utf-8").read() if os.path.exists(os.path.join(c, "diagnostico.md")) else ""
        paso("P1 · 4.15 sin declaración F1: el paso 7 termina en pendiente_de_datos con el diagnóstico F1",
             st.get("estado_analisis") == "pendiente_de_datos" and st.get("paso") == 7 and r.get("bloquea") and "F1" in dg and not os.path.exists(os.path.join(c, "fase_b.json")),
             f"código {rc} · estado {st.get('estado_analisis')} · paso {st.get('paso')} · {str(r.get('rotulo'))[:160]}")
        fi = json.load(open(os.path.join(c, "ficha.json"), encoding="utf-8")) if os.path.exists(os.path.join(c, "ficha.json")) else {}
        paso("P1 · la ficha lleva el bloque motor_a_f1 con «no utilizable»", isinstance(fi.get("motor_a_f1"), dict) and fi["motor_a_f1"]["utilizable_para_conclusion"] is False)
        # P2
        c = preparar("EmpresaX_F1", declaracion(), sin_arrendamientos=True)
        rc, out = TS.correr(c, reac)
        st = TS.estado(c)
        r = json.load(open(os.path.join(c, "motor_a_f1_resultado.json"), encoding="utf-8")) if os.path.exists(os.path.join(c, "motor_a_f1_resultado.json")) else {}
        bl = [g["id"] + ": " + str(g["detalle"])[:100] for g in r.get("guardas") or [] if g.get("salta") and g.get("severidad") == "BLOQUEA"]
        paso("P2 · sin arrendamientos ni PPA y todo declarado: F1 no bloquea y el pipeline pasa de la fase B (gancho en los pasos 7 y 12)",
             r.get("utilizable_para_conclusion") is True and os.path.exists(os.path.join(c, "fase_b.json")) and (st.get("motor_a_f1") or {}).get("paso") == 12,
             f"código {rc} · estado {st.get('estado_analisis')} · paso {st.get('paso')} · bloquean {bl}")
        fi = json.load(open(os.path.join(c, "ficha.json"), encoding="utf-8")) if os.path.exists(os.path.join(c, "ficha.json")) else {}
        paso("P2 · el estado final no es un bloqueo F1 y la ficha lleva motor_a_f1 «utilizable»",
             st.get("estado_analisis") is not None and isinstance(fi.get("motor_a_f1"), dict) and fi["motor_a_f1"]["utilizable_para_conclusion"] is True,
             f"estado {st.get('estado_analisis')}")
        # P3
        c = preparar("EmpresaX_USGAAP", declaracion("US_GAAP"), sin_arrendamientos=True)
        rc, out = TS.correr(c, reac)
        st = TS.estado(c)
        dg = json.load(open(os.path.join(c, "diagnostico.json"), encoding="utf-8")) if os.path.exists(os.path.join(c, "diagnostico.json")) else {}
        paso("P3 · US GAAP: el paso 7 termina en no_entregable · límite del modelo con F1-NORMA (límite declarado)",
             st.get("estado_analisis") == "no_entregable" and st.get("paso") == 7 and (dg.get("causa") or {}).get("tipo") == "limite_del_modelo"
             and "F1-NORMA" in str((dg.get("causa") or {}).get("detalle")), f"estado {st.get('estado_analisis')} · {str((dg.get('causa') or {}).get('detalle'))[:200]}")
        # P4 · (revisión H2) sin entrada_efectiva.json ni motor_a_f1.json, con arrendamientos en el libro (C49 = 3,71) y sin la marca de la
        # línea de base: F1 se exige igual → el paso 7 termina en pendiente_de_datos (no hay A0 silencioso)
        c = preparar("EmpresaY", con_4_15=False, renombrar=True)
        rc, out = TS.correr(c, reac)
        st = TS.estado(c)
        paso("P4 · sin archivos de la 4.15 y con arrendamientos en el libro: F1 se exige y el paso 7 termina en pendiente_de_datos",
             st.get("estado_analisis") == "pendiente_de_datos" and st.get("paso") == 7 and os.path.exists(os.path.join(c, "motor_a_f1_resultado.json")),
             f"código {rc} · estado {st.get('estado_analisis')} · paso {st.get('paso')}")
        # P5 · (revisión H1) el expediente de P2 terminó en concluido con F1 utilizable; se cambia la declaración a una que bloquea y se relanza
        # con «--desde 13»: el paso 13 ve la evaluación no vigente, repite el 12 y el gancho termina; ninguna ficha oficial concluido/comprar
        c = os.path.join(TS.BASE, "EmpresaX_F1")
        d = declaracion()
        d["perimetro_reinversion"]["valor"] = "A2_propio"
        json.dump(d, open(os.path.join(c, "motor_a_f1.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        r = subprocess.run([TS.PY, TS.PIPE, c, "--desde", "13"], capture_output=True, text=True)
        rc, out = TS.correr(c, reac)
        st = TS.estado(c)
        fi = json.load(open(os.path.join(c, "ficha.json"), encoding="utf-8")) if os.path.exists(os.path.join(c, "ficha.json")) else {}
        dec = str(((fi.get("decision") or {}).get("accion") if isinstance(fi.get("decision"), dict) else fi.get("decision")) or "")
        paso("P5 · declaración cambiada tras el cierre y «--desde 13»: no hay ficha oficial concluido ni «comprar»; termina por F1",
             fi.get("estado_analisis") != "concluido" and "comprar" not in dec.lower() and st.get("estado_analisis") in ("no_entregable", "pendiente_de_datos"),
             f"código {r.returncode}/{rc} · estado {st.get('estado_analisis')} · paso {st.get('paso')} · ficha {fi.get('estado_analisis')} · decisión {dec[:60]}")
    finally:
        shutil.rmtree(TS.BASE, ignore_errors=True)
        TS.BASE = base0
    n = sum(ok for _, ok in RES)
    linea = f"{n}/{len(RES)} pruebas del gancho F1 del pipeline PASAN"
    print(linea)
    if salida:
        open(salida, "w", encoding="utf-8").write("\n".join(f"{'PASA ' if ok else 'FALLA'} · {x}" for x, ok in RES) + "\n" + linea + "\n")
    return 0 if n == len(RES) else 1


if __name__ == "__main__":
    sys.exit(main())
