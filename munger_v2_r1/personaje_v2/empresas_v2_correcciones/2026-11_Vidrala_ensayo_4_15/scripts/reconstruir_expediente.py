#!/usr/bin/env python3
"""Reconstrucción de un expediente en una carpeta LIMPIA desde sus entradas declaradas (4.15; encargo correctivo §3, prueba obligatoria).

Entradas declaradas que se copian: etapa1/ (copia de ensayo del libro de la etapa 1), fase1_metadatos.json, fase1_partes/,
fase1_fuentes.json, fase1_decisiones.json, texto/, configuracion_economica.json, celdas_A/B/C.json (lo que escribieron las fases de
juicio), alcance_v2.json y entrada_efectiva.json (4.15, N7: con «estricta», el relleno se detiene con el código 7 como en el pipeline).
Nada más del expediente: ni sus libros, ni su fase1_v63.json (salvo --fase1 declarado), ni sus resultados.

Pasos, los del pipeline (2: fase 1; migración; relleno; configuración V6.4; escritura de A, B y C; recálculo; lectura y precio de Sí):
  --fase1 construir (por defecto): fase1_v63.json se reconstruye con `fase1_historia.py construir` desde fase1_partes y los metadatos;
  --fase1 declarado: se usa el fase1_v63.json del expediente como entrada declarada (semántica del pipeline cuando ya existe).
  --sin-migrados: antes del relleno se vacían en el libro base las entradas del FCF base (Análisis C46–C50) migradas de la etapa 1, para
  comprobar que la entrada efectiva sale de la vía generativa y no solo de la protección de un valor migrado.
Comparación con el expediente: fase1_v63.json (Historia y entradas de Análisis), libro de datos (valores y fórmulas), libro evaluado
(valores y fórmulas), valores recalculados de todas las celdas (tolerancia relativa 1e-9) y precio de Sí. Toda diferencia se lista: se
diagnostica, no se compensa.
Uso (desde munger_v2_r1/): python3 -I -B …/reconstruir_expediente.py EXPEDIENTE SALIDA.json [--fase1 construir|declarado] [--sin-migrados]
Además se informa de las entradas del FCF base que el libro conserva de la etapa 1 con un valor distinto del declarado en fase1_v63.json
(«entradas_migradas_distintas»): reproducen el número, pero no por la vía generativa.
Código: 0 si reproduce todo por la vía generativa; 1 si hay diferencias o entradas migradas distintas; 2 uso; 3 si un paso no termina.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
PV = os.path.abspath(os.path.join(AQUI, "..", "..", ".."))
SCR = os.path.join(PV, "scripts")
sys.path.insert(0, SCR)
import config_v2  # noqa: E402
from v63_xml import LibroV63  # noqa: E402

DECLARADAS = ["etapa1", "fase1_metadatos.json", "fase1_partes", "fase1_fuentes.json", "fase1_decisiones.json", "texto",
              "configuracion_economica.json", "celdas_A.json", "celdas_B.json", "celdas_C.json", "alcance_v2.json",
              "entrada_efectiva.json"]  # (4.15, N7) el modo de la entrada efectiva es una entrada declarada
FCF_BASE = [f"Análisis!{c}" for c in ("C46", "C47", "C48", "C49", "C50")]
TOL = 1e-9
# Tolerancias justificadas (se listan aparte, no se cuentan como diferencia): sellos de la fecha de ejecución, que no son entradas,
# transformaciones, fórmulas ni resultados
SELLOS_DE_EJECUCION = {"Control maestro!L5": "fecha de revisión que rellenar_fase1_v63.py escribe con la fecha del día"}


ENV = dict(os.environ)


def run(cmd, env=None):
    r = subprocess.run(cmd, capture_output=True, text=True, env=env or ENV)
    return r.returncode, (r.stdout + r.stderr)


def iguales(a, b):
    if isinstance(a, bool) or isinstance(b, bool):
        return a == b
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return abs(a - b) <= TOL * max(1.0, abs(a), abs(b))
    return a == b


def celdas_libro(ruta):
    """{Hoja!REF: ("f", fórmula) | ("v", valor)} de todas las celdas del libro (XML: fórmulas sin evaluar; valores tal como están)."""
    lb = LibroV63(ruta)
    out = {}
    for h in lb.hojas():
        for ref, v in lb.todas_las_celdas(h).items():
            out[f"{h}!{ref}"] = ("f", lb._celda(h, ref).find("{http://schemas.openxmlformats.org/spreadsheetml/2006/main}f").text) if lb.tiene_formula(h, ref) else ("v", v)
    return out


def valores_recalculados(ruta):
    import openpyxl
    wb = openpyxl.load_workbook(ruta, data_only=True, read_only=True)
    out = {}
    for ws in wb.worksheets:
        for fila in ws.iter_rows():
            for c in fila:
                if c.value is not None:
                    out[f"{ws.title}!{c.coordinate}"] = c.value
    return out


def _sellos(a, b, dif):
    return [{"celda": k, "motivo": SELLOS_DE_EJECUCION[k], "expediente": a.get(k), "reconstruido": b.get(k)} for k in dif if k in SELLOS_DE_EJECUCION]


def comparar(a, b, limite=60):
    dif = [k for k in sorted(set(a) | set(b)) if not (k in a and k in b and a[k][0] == b[k][0] and iguales(a[k][1], b[k][1]))]
    sellos = _sellos(a, b, dif)
    dif = [k for k in dif if k not in SELLOS_DE_EJECUCION]
    return {"n": len(dif), "ejemplos": [{"celda": k, "expediente": a.get(k), "reconstruido": b.get(k)} for k in dif[:limite]], "sellos_de_ejecucion": sellos}


def comparar_valores(a, b, limite=60):
    dif = [k for k in sorted(set(a) | set(b)) if not iguales(a.get(k), b.get(k))]
    sellos = _sellos(a, b, dif)
    dif = [k for k in dif if k not in SELLOS_DE_EJECUCION]
    return {"n": len(dif), "ejemplos": [{"celda": k, "expediente": a.get(k), "reconstruido": b.get(k)} for k in dif[:limite]], "sellos_de_ejecucion": sellos}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("expediente")
    ap.add_argument("salida")
    ap.add_argument("--fase1", choices=("construir", "declarado"), default="construir")
    ap.add_argument("--sin-migrados", action="store_true")
    a = ap.parse_args()
    exp = os.path.abspath(a.expediente)
    E = os.path.basename(exp)
    v64 = os.path.exists(os.path.join(exp, "configuracion_economica.json"))
    pa = os.path.join(exp, "plantilla_activa.json")
    nombre_cfg = (json.load(open(pa, encoding="utf-8")).get("config") if os.path.exists(pa) else None) or "config_v2.json"
    ruta_cfg = os.path.join(PV, nombre_cfg)  # la plantilla y la configuración con que se hizo el expediente (plantilla_activa.json)
    cfg = config_v2.cargar(ruta_cfg)
    ENV["MUNGER_CONFIG"] = ruta_cfg  # como el pipeline: todos los scripts usan la misma plantilla, referencia y verificador
    tmp = tempfile.mkdtemp(prefix=f"reconstruccion_{E}_")
    d = os.path.join(tmp, E)
    os.makedirs(d)
    perfil = os.path.join(tmp, ".lo_perfil")
    inf = {"expediente": os.path.relpath(exp, os.path.dirname(PV)), "modo_fase1": a.fase1, "sin_migrados": a.sin_migrados, "config": os.path.basename(ruta_cfg),
           "carpeta_limpia": "temporal (se elimina al terminar)", "entradas_declaradas": [], "pasos": [], "diferencias": {}}

    def fin(codigo):
        json.dump(inf, open(a.salida, "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
        shutil.rmtree(tmp, ignore_errors=True)
        print(json.dumps({k: inf.get(k) for k in ("expediente", "modo_fase1", "sin_migrados", "reproduce", "reproduce_por_via_generativa")}, ensure_ascii=False) if "reproduce" in inf else inf["pasos"][-1:])
        sys.exit(codigo)

    try:
        for n in DECLARADAS:
            o = os.path.join(exp, n)
            if os.path.isdir(o):
                shutil.copytree(o, os.path.join(d, n))
            elif os.path.isfile(o):
                shutil.copy2(o, os.path.join(d, n))
            else:
                continue
            inf["entradas_declaradas"].append(n)
        if a.fase1 == "declarado":
            shutil.copy2(os.path.join(exp, "fase1_v63.json"), os.path.join(d, "fase1_v63.json"))
            inf["entradas_declaradas"].append("fase1_v63.json")
        else:
            rc, out = run([sys.executable, "-B", os.path.join(SCR, "fase1_historia.py"), "construir", d])
            inf["pasos"].append({"paso": "fase1_historia construir", "rc": rc, "salida": out[-400:]})
            if rc != 0:
                return fin(3)
        f_e, f_r = json.load(open(os.path.join(exp, "fase1_v63.json"), encoding="utf-8")), json.load(open(os.path.join(d, "fase1_v63.json"), encoding="utf-8"))
        val = lambda x: x.get("valor") if isinstance(x, dict) else x  # noqa: E731
        an = sorted(set(f_e.get("analisis") or {}) | set(f_r.get("analisis") or {}))
        inf["diferencias"]["fase1_analisis"] = [{"celda": c, "expediente": val((f_e.get("analisis") or {}).get(c)), "reconstruido": val((f_r.get("analisis") or {}).get(c))}
                                                for c in an if not iguales(val((f_e.get("analisis") or {}).get(c)), val((f_r.get("analisis") or {}).get(c)))]
        pe, pr = (f_e.get("historia") or {}).get("partidas") or {}, (f_r.get("historia") or {}).get("partidas") or {}
        vv = lambda p: (p.get("valores") if isinstance(p, dict) else p) or []  # noqa: E731
        inf["diferencias"]["fase1_historia"] = [{"partida": k, "expediente": vv(pe.get(k)), "reconstruido": vv(pr.get(k))} for k in sorted(set(pe) | set(pr))
                                                if len(vv(pe.get(k))) != len(vv(pr.get(k))) or not all(iguales(x, y) for x, y in zip(vv(pe.get(k)), vv(pr.get(k))))]
        e1 = [f for f in os.listdir(os.path.join(d, "etapa1")) if f.endswith(".xlsx")][0]
        base, datos, ev = (os.path.join(d, f"{E}_v63_{x}.xlsx") for x in ("base", "datos", "evaluada"))
        rc, out = run([sys.executable, "-B", os.path.join(SCR, "migrar_v53_a_v63.py"), os.path.join(d, "etapa1", e1), cfg["plantilla"]["archivo"], base])
        inf["pasos"].append({"paso": "migración de la etapa 1", "rc": rc, "salida": out[-300:]})
        if rc != 0:
            return fin(3)
        if a.sin_migrados:
            lb = LibroV63(base)
            vaciadas = {k: lb.leer(*k.split("!")) for k in FCF_BASE}
            lb.escribir_celdas({k: None for k in FCF_BASE})
            lb.guardar(base)
            inf["pasos"].append({"paso": "entradas del FCF base migradas vaciadas en el libro base", "valores_migrados": vaciadas})
        import pipeline as _PL  # (4.15, N7) el mismo modo que aplica el pipeline (falla en cerrado)
        try:
            modo, origen_modo = _PL.modo_entrada_efectiva(d)
        except ValueError as ex:
            inf["pasos"].append({"paso": "modo de la entrada efectiva", "error": str(ex)})
            return fin(3)
        inf["modo_entrada_efectiva"] = {"modo": modo, "declarado_en": origen_modo}
        rc, out = run([sys.executable, "-B", os.path.join(SCR, "rellenar_fase1_v63.py"), base, os.path.join(d, "fase1_v63.json"), datos, "--config", ruta_cfg]
                      + (["--estricta"] if modo == "estricta" else []))
        inf["pasos"].append({"paso": "rellenar_fase1_v63", "rc": rc, "salida": out[-700:]})
        if rc != 0:
            return fin(3)
        try:
            inf["entradas_migradas_distintas"] = json.load(open(datos + ".fase1.registro.json", encoding="utf-8")).get("entradas_migradas_distintas") or []
        except (OSError, ValueError):
            inf["entradas_migradas_distintas"] = None
        if v64:
            rc, out = run([sys.executable, "-B", os.path.join(SCR, "configuracion_economica.py"), "aplicar", datos, datos + ".cfg.xlsx",
                           os.path.join(d, "configuracion_economica.json"), "--config", ruta_cfg])
            inf["pasos"].append({"paso": "configuración económica V6.4", "rc": rc, "salida": out[-300:]})
            if rc != 0:
                return fin(3)
            os.replace(datos + ".cfg.xlsx", datos)
        anterior = datos
        for fase in ("A", "B", "C"):
            cj = os.path.join(d, f"celdas_{fase}.json")
            if not os.path.exists(cj):
                inf["pasos"].append({"paso": f"escritura de la fase {fase}", "rc": None, "salida": "sin celdas declaradas"})
                continue
            rc, out = run([sys.executable, "-B", os.path.join(SCR, "escribir_v63.py"), anterior, ev + f".{fase}.xlsx", "--celdas", cj, "--verificar", cfg["plantilla"]["referencia"]])
            inf["pasos"].append({"paso": f"escritura de la fase {fase}", "rc": rc, "salida": out[-300:]})
            if rc != 0:
                return fin(3)
            anterior = ev + f".{fase}.xlsx"
        shutil.copy2(anterior, ev)
        inf["diferencias"]["libro_datos"] = comparar(celdas_libro(os.path.join(exp, f"{E}_v63_datos.xlsx")), celdas_libro(datos))
        inf["diferencias"]["libro_evaluado"] = comparar(celdas_libro(os.path.join(exp, f"{E}_v63_evaluada.xlsx")), celdas_libro(ev))
        rc, out = run(["bash", os.path.join(SCR, "recalc.sh"), ev, os.path.join(d, "recalc"), perfil])
        inf["pasos"].append({"paso": "recálculo (LibreOffice)", "rc": rc, "salida": out[-200:]})
        if rc != 0:
            return fin(3)
        rec = os.path.join(d, "recalc", os.path.basename(ev))
        rec_e = os.path.join(exp, "recalc", os.path.basename(ev))
        if os.path.exists(rec_e):
            inf["diferencias"]["valores_recalculados"] = comparar_valores(valores_recalculados(rec_e), valores_recalculados(rec))
        rj, pj = os.path.join(d, "resultados.json"), os.path.join(d, "precio.json")
        rc, out = run([sys.executable, "-B", os.path.join(SCR, "leer_resultados.py"), rec, rj, "--exigir-recalculo-forzado"])
        inf["pasos"].append({"paso": "lectura de resultados", "rc": rc, "salida": out[-200:]})
        if rc != 0:
            return fin(3)
        rc, out = run([sys.executable, "-B", os.path.join(SCR, "precio_de_si.py"), rj, pj, "--k", str(cfg.get("convenciones", {}).get("k_asimetria", 3))])
        p_e = json.load(open(os.path.join(exp, "precio.json"), encoding="utf-8")).get("precio_si")
        p_r = json.load(open(pj, encoding="utf-8")).get("precio_si") if os.path.exists(pj) else None
        inf["precio_si"] = {"expediente": p_e, "reconstruido": p_r, "diferencia": (p_r - p_e) if isinstance(p_r, (int, float)) and isinstance(p_e, (int, float)) else None}
        inf["entradas_fcf_base"] = {k: {"expediente": dict(celdas_libro(os.path.join(exp, f"{E}_v63_evaluada.xlsx"))).get(k), "reconstruido": celdas_libro(ev).get(k)} for k in FCF_BASE}
        dif = inf["diferencias"]
        # «reproduce»: mismos datos efectivos, transformaciones, fórmulas y resultados; «reproduce_por_via_generativa»: además, ninguna entrada
        # del FCF base la sostiene solo un valor migrado de la etapa 1 distinto de la que declara fase1_v63.json
        inf["reproduce"] = (not dif["fase1_analisis"] and not dif["fase1_historia"] and dif["libro_datos"]["n"] == 0 and dif["libro_evaluado"]["n"] == 0
                            and (dif.get("valores_recalculados") or {"n": 0})["n"] == 0 and inf["precio_si"]["diferencia"] is not None and abs(inf["precio_si"]["diferencia"]) <= TOL)
        inf["reproduce_por_via_generativa"] = bool(inf["reproduce"]) and inf.get("entradas_migradas_distintas") == []
        return fin(0 if inf["reproduce_por_via_generativa"] else 1)
    except Exception as ex:  # noqa: BLE001
        inf["pasos"].append({"paso": "excepción", "rc": None, "salida": f"{type(ex).__name__}: {ex}"[:600]})
        return fin(3)


if __name__ == "__main__":
    main()
