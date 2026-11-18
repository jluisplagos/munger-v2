#!/usr/bin/env python3
"""Prueba de extremo a extremo de la V6.3.1 F1 en el pipeline (F1-IMPL), con la empresa sintética y los agentes simulados de
test_pipeline_sintetico.py y las ayudas de prueba_pipeline_f1.py (LibreOffice: ejecutar con flock /home/user/e_work/libreoffice.lock).
Directorio temporal; no toca la batería sintética ni su línea de base, ni prueba_pipeline_f1.py.

Uso (desde cualquier carpeta): flock … python3 -B prueba_pipeline_v631.py [SALIDA.txt]
Casos (empresa sintética CON arrendamientos: principal en el FCF base, C49 > 0, D&A de derechos de uso = 30 % de la D&A, PPA 0; perímetro
A1_sin_ROU declarado en reinversión, palancas y ROIC):
  P6 · con config_v2_v631_f1.json: plantilla_activa.json V6.3.1; el paso 2 aplica la declaración al libro (C85 = A1_sin_ROU); F1 no
       bloquea (F1-LIBRO no salta: el libro calcula el perímetro y coincide con la capa), el gancho corre en los pasos 7 y 12 y el pipeline
       pasa de la fase B; la ficha lleva la versión V6.3.1 F1 y el bloque motor_a_f1 «utilizable».
  P7 · la misma declaración con config_v2.json (V6.3): el paso 7 termina en no_entregable · límite del modelo con F1-LIBRO (como antes).
  P8 · P6 con la declaración cambiada después (otra D&A de derechos de uso) y «--desde 7»: el libro ya no corresponde → F1-LIBRO bloquea.
"""
import json
import os
import shutil
import subprocess
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

CFG631 = os.path.join(PV, "config_v2_v631_f1.json")
CFG63 = os.path.join(PV, "config_v2.json")
RES = []


def paso(nombre, ok, detalle=""):
    RES.append((nombre, bool(ok)))
    print(("PASA " if ok else "FALLA") + " · " + nombre + (f" · {detalle}" if detalle else ""))


def declaracion(frac=0.3):
    f1 = json.load(open(os.path.join(PV, "esquema", "fase1_v63.ejemplo.json"), encoding="utf-8"))
    anios, da = f1["historia"]["anios"], f1["historia"]["partidas"]["da"]["valores"]
    d = PF.declaracion()
    for k in ("perimetro_reinversion", "perimetro_palancas_s2c", "perimetro_roic"):
        d[k]["valor"] = "A1_sin_ROU"
    import openpyxl
    a = openpyxl.load_workbook(os.path.join(PV, "pruebas", "sintetico", "_origen", "EmpresaX_v53_evaluada_sintetica.xlsx"), data_only=True)["Análisis"]
    n, pr = f1["anios_fcf_base"], f1["historia"]["partidas"]["arrendamientos_principal"]["valores"]
    d["conciliacion_fcf_base"].append({"componente": "C49", "importe": -(a["C49"].value - sum(pr[-n:]) / n),
                                       "partida": "C49 registrado con 2 decimales en la etapa 1 frente a la media de la Historia",
                                       "fuente": {"documento": "EmpresaX_v53_evaluada_sintetica.xlsx (Análisis) y fase1_v63.ejemplo.json (Historia)", "pagina": None}})
    d["series"]["da_rou"] = {str(y): {"valor_fuente": round(frac * v, 6), "signo": 1, "tratamiento": "ninguno", "documento": "informe anual sintético",
                                      "pagina": 1, "literal": repr(round(frac * v, 6)), "archivo": PF.FUENTE} for y, v in zip(anios, da)}
    return d


def correr(c, cfg):
    os.environ["MUNGER_CONFIG"] = cfg
    try:
        return TS.correr(c, TS.reaccion_normal())
    finally:
        os.environ.pop("MUNGER_CONFIG", None)


def leer(c, n):
    p = os.path.join(c, n)
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}


def bloquean(r):
    return [g["id"] + ": " + str(g["detalle"])[:120] for g in r.get("guardas") or [] if g.get("salta") and g.get("severidad") == "BLOQUEA"]


def main():
    salida = sys.argv[1] if len(sys.argv) > 1 else None
    base0, TS.BASE = TS.BASE, tempfile.mkdtemp(prefix="v631_pipe_")
    try:
        # P6
        c = PF.preparar("EmpresaX_V631", declaracion())
        rc, out = correr(c, CFG631)
        st, r, fi, pa = TS.estado(c), leer(c, "motor_a_f1_resultado.json"), leer(c, "ficha.json"), leer(c, "plantilla_activa.json")
        from openpyxl import load_workbook
        ev = os.path.join(c, "recalc", "EmpresaX_V631_v63_evaluada.xlsx")
        h = load_workbook(ev, data_only=True)["Historia"] if os.path.exists(ev) else None
        paso("P6 · V6.3.1: plantilla_activa.json registra la V6.3.1 F1 y el libro lleva el perímetro declarado (C85 = C89 = A1_sin_ROU, D_X = D&A − ROU)",
             pa.get("version") == "V6.3.1 F1" and h is not None and h["C85"].value == "A1_sin_ROU" and h["C89"].value == "A1_sin_ROU"
             and abs(h["L88"].value - (h["L8"].value - h["L86"].value)) < 1e-12, f"plantilla {pa.get('version')} · C89 {h['C89'].value if h else None!r}")
        g = [x for x in r.get("guardas") or [] if x["id"] == "F1-LIBRO"]
        paso("P6 · con arrendamientos y A1 declarado: F1-LIBRO no salta (libro = capa) y F1 no bloquea; gancho en los pasos 7 y 12; pasa de la fase B",
             g and not g[0]["salta"] and (r.get("libro_v631_f1") or {}).get("motivos") == [] and r.get("utilizable_para_conclusion") is True
             and os.path.exists(os.path.join(c, "fase_b.json")) and (st.get("motor_a_f1") or {}).get("paso") == 12,
             f"código {rc} · estado {st.get('estado_analisis')} · paso {st.get('paso')} · bloquean {bloquean(r)}")
        paso("P6 · estado final concluido; ficha con la plantilla V6.3.1 F1 y motor_a_f1 «utilizable» con el perímetro efectivo del libro",
             st.get("estado_analisis") == "concluido" and fi.get("estado_analisis") == "concluido" and (fi.get("versiones") or {}).get("plantilla") == "V6.3.1 F1"
             and (fi.get("motor_a_f1") or {}).get("utilizable_para_conclusion") is True
             and ((fi.get("motor_a_f1") or {}).get("libro_v631_f1") or {}).get("perimetro_efectivo") == "A1_sin_ROU" and "configuracion_economica" not in fi,
             f"estado {st.get('estado_analisis')} · ficha {fi.get('estado_analisis')}")
        paso("P6 · el resumen va a resumen_v2_v631_f1.csv (no a resumen_v2.csv)",
             not os.path.exists(os.path.join(TS.BASE, "resumen_v2.csv")) and (os.path.exists(os.path.join(TS.BASE, "resumen_v2_v631_f1.csv"))
                                                                              or st.get("estado_analisis") not in ("concluido",)),
             str(sorted(x for x in os.listdir(TS.BASE) if x.endswith(".csv"))))
        # P9 · R2-1 (revisión V6.3.1, V631-1) sobre copias del expediente cerrado: R21a (resultado F1 borrado), R21b (además, la declaración
        # cambiada) y R21c (el estado pierde el motor, como un expediente anterior a F1): ninguna llamada llega a concluido sin F1 vigente
        cerrado = os.path.join(TS.BASE, "_cerrado")
        shutil.copytree(c, cerrado)

        def copia(nombre):
            d_ = os.path.join(TS.BASE, nombre, "EmpresaX_V631")
            shutil.copytree(cerrado, d_)
            for n_ in ("motor_a_f1_resultado.json", "motor_a_f1_resultado.md"):
                if os.path.exists(os.path.join(d_, n_)):
                    os.remove(os.path.join(d_, n_))
            return d_

        def lanzar(d_, *args):
            os.environ["MUNGER_CONFIG"] = CFG631
            try:
                r_ = subprocess.run([TS.PY, TS.PIPE, d_, *args], capture_output=True, text=True)
            finally:
                os.environ.pop("MUNGER_CONFIG", None)
            rc_ = r_.returncode
            if rc_ == 10:
                rc_, _ = correr(d_, CFG631)
            return rc_, (r_.stdout + r_.stderr).strip()

        def oficial(d_):
            return (leer(d_, "ficha.json") or {}).get("estado_analisis"), str(((leer(d_, "ficha.json") or {}).get("decision") or {}).get("accion"))

        ca = copia("R21a")
        rca, outa = lanzar(ca, "--reiniciar", "--desde", "13")
        paso("P9 · R21a: resultado F1 borrado y «--reiniciar --desde 13» → llamada rechazada (código 2), aprobación retirada: ninguna ficha oficial concluido",
             rca == 2 and "no se combinan" in outa and oficial(ca)[0] != "concluido", f"código {rca} · ficha {oficial(ca)} · {outa[-160:]}")
        cb = copia("R21b")
        db = declaracion(0.40)
        PF.escribir_fuente(cb, db)
        json.dump(db, open(os.path.join(cb, "motor_a_f1.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        rcb, outb = lanzar(cb, "--reiniciar", "--desde", "13")
        rcb2, _ = lanzar(cb, "--desde", "13")
        stb, rb_ = TS.estado(cb), leer(cb, "motor_a_f1_resultado.json")
        gb = [x for x in rb_.get("guardas") or [] if x["id"] == "F1-LIBRO"]
        paso("P9 · R21b: además la declaración cambiada (30 % → 40 %): «--reiniciar --desde 13» rechazado; «--desde 13» → F1-LIBRO bloquea, sin concluido",
             rcb == 2 and gb and gb[0]["salta"] and stb.get("estado_analisis") in ("no_entregable", "pendiente_de_datos") and oficial(cb)[0] != "concluido",
             f"códigos {rcb}/{rcb2} · estado {stb.get('estado_analisis')} · paso {stb.get('paso')} · ficha {oficial(cb)}")
        cc = copia("R21c")
        stc = TS.estado(cc)
        stc.pop("motor", None)
        stc.pop("motor_a_f1", None)
        json.dump(stc, open(os.path.join(cc, "estado_pipeline.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        import motor_a_f1 as MF  # noqa: E402
        vc = MF.vigencia(cc)
        rcc, _ = lanzar(cc, "--desde", "13")
        stc2, rc_r = TS.estado(cc), leer(cc, "motor_a_f1_resultado.json")
        paso("P9 · R21c: el estado sin el motor (expediente anterior a F1) y sin resultado: vigencia() lee el motor de fase_a.json (A, no vigente) y "
             "«--desde 13» repone el motor, evalúa F1 de nuevo y solo concluye con una evaluación F1 vigente y utilizable",
             vc["motor"] == "A" and vc["vigente"] is False and stc2.get("motor") == "A" and (stc2.get("estado_analisis") != "concluido" or
                                                                                         (rc_r.get("utilizable_para_conclusion") is True and MF.vigencia(cc)["vigente"] is True)),
             f"vigencia {vc['motivo']} · código {rcc} · estado {stc2.get('estado_analisis')} · F1 {rc_r.get('utilizable_para_conclusion')}")
        # P8 · declaración cambiada después del paso 2: el libro ya no corresponde
        d = declaracion(0.31)
        PF.escribir_fuente(c, d)
        json.dump(d, open(os.path.join(c, "motor_a_f1.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        os.environ["MUNGER_CONFIG"] = CFG631
        try:
            r8 = subprocess.run([TS.PY, TS.PIPE, c, "--desde", "7"], capture_output=True, text=True)
        finally:
            os.environ.pop("MUNGER_CONFIG", None)
        rc8, _ = correr(c, CFG631)
        st8, r8r = TS.estado(c), leer(c, "motor_a_f1_resultado.json")
        g8 = [x for x in r8r.get("guardas") or [] if x["id"] == "F1-LIBRO"]
        paso("P8 · declaración cambiada (D&A ROU 30 % → 31 %) y «--desde 7»: el libro ya no corresponde; F1-LIBRO bloquea y no hay conclusión",
             g8 and g8[0]["salta"] and st8.get("estado_analisis") in ("no_entregable", "pendiente_de_datos") and r8r.get("utilizable_para_conclusion") is False,
             f"código {r8.returncode}/{rc8} · estado {st8.get('estado_analisis')} · paso {st8.get('paso')} · {str(g8[0]['detalle'] if g8 else None)[:160]}")
        # P7
        c = PF.preparar("EmpresaX_V63_A1", declaracion())
        rc, out = correr(c, CFG63)
        st, r = TS.estado(c), leer(c, "motor_a_f1_resultado.json")
        dg = leer(c, "diagnostico.json")
        paso("P7 · la misma declaración con la V6.3: el paso 7 termina en no_entregable · límite del modelo con F1-LIBRO; sin plantilla_activa.json",
             st.get("estado_analisis") == "no_entregable" and st.get("paso") == 7 and (dg.get("causa") or {}).get("tipo") == "limite_del_modelo"
             and "F1-LIBRO" in str((dg.get("causa") or {}).get("detalle")) and not os.path.exists(os.path.join(c, "plantilla_activa.json")),
             f"estado {st.get('estado_analisis')} · paso {st.get('paso')} · {bloquean(r)[:3]}")
    finally:
        shutil.rmtree(TS.BASE, ignore_errors=True)
        TS.BASE = base0
    n = sum(ok for _, ok in RES)
    linea = f"{n}/{len(RES)} pruebas de la V6.3.1 F1 en el pipeline PASAN"
    print(linea)
    if salida:
        open(salida, "w", encoding="utf-8").write("\n".join(f"{'PASA ' if ok else 'FALLA'} · {x}" for x, ok in RES) + "\n" + linea + "\n")
    return 0 if n == len(RES) else 1


if __name__ == "__main__":
    sys.exit(main())
