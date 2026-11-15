#!/usr/bin/env python3
"""¿Crea valor el crecimiento terminal de Vidrala en el motor B? (encargo 4.13 §8, «ROIC y tasa de descuento»). Solo copias.

La revisión económica de la 4.12 decía que, con un ROIC terminal del 9 % igual a la r personal del 9 %, «el crecimiento terminal no crea
valor». El motor B descuenta a r_op (Diagnóstico V6 C15 = 8,689151674 % en el expediente), no a la r personal, y P-M1 añade un requisito
de inversión que crece con las ventas en el terminal. La igualdad 9 % = 9 % no demuestra nada sobre el signo del efecto: aquí se calcula.

Sobre copias del libro evaluado de cierre_condicionado/Vidrala (4.12; no se modifica), con LibreOffice y en secuencia:
  - activa (SR1 · Λ 1,15 · P0) y la misma con g = 0 en los tres escenarios (Análisis B68:D68);
  - SR2 (ROIC terminal × f) y la misma con g = 0;
  - modo heredado (V6.3 efectiva) y el mismo con g = 0.
La diferencia entre cada par es el valor que aporta el crecimiento perpetuo con esa configuración (no es una propuesta de cambiar g).
Uso (desde munger_v2_r1/): python3 -I …/scripts/crecimiento_terminal_vidrala.py · Escribe resultados/crecimiento_terminal_vidrala.json y .md.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
E413 = os.path.dirname(AQUI)
PV = os.path.abspath(os.path.join(E413, "..", ".."))
SCR = os.path.join(PV, "scripts")
VID = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_12", "cierre_condicionado", "Vidrala")
sys.path.insert(0, SCR)
H = "Configuración V6.4"


def main():
    from v63_xml import LibroV63
    from openpyxl import load_workbook
    import configuracion_economica as CE
    libro = os.path.join(VID, "Vidrala_v63_evaluada.xlsx")
    tmp = tempfile.mkdtemp(prefix="gterm_")
    perfil = os.path.join(tmp, ".lo_perfil")
    os.makedirs(os.path.join(tmp, "recalc"))
    sr2 = CE.ESTRUCTURAS[4]
    casos = {
        "activa": {}, "activa_g0": {"Análisis!B68": 0, "Análisis!C68": 0, "Análisis!D68": 0},
        "SR2": {f"{H}!B36": sr2, f"{H}!B42": CE.ROIC_T[1]},
        "SR2_g0": {f"{H}!B36": sr2, f"{H}!B42": CE.ROIC_T[1], "Análisis!B68": 0, "Análisis!C68": 0, "Análisis!D68": 0},
        "heredado": {f"{H}!B4": "Heredado"}, "heredado_g0": {f"{H}!B4": "Heredado", "Análisis!B68": 0, "Análisis!C68": 0, "Análisis!D68": 0},
    }
    out = {"libro": os.path.relpath(libro, PV), "casos": {}}
    for nombre, celdas in casos.items():
        dst = os.path.join(tmp, f"{nombre}.xlsx")
        lb = LibroV63(libro)
        if celdas:
            lb.escribir_celdas(celdas)
        lb.borrar_caches()
        lb.guardar(dst)
        r = subprocess.run(["bash", os.path.join(SCR, "recalc.sh"), dst, os.path.join(tmp, "recalc"), perfil], capture_output=True, text=True)
        if r.returncode != 0:
            raise SystemExit(f"recálculo {nombre}: {(r.stdout + r.stderr)[-300:]}")
        rec = os.path.join(tmp, "recalc", os.path.basename(dst))
        rj, pj = os.path.join(tmp, f"{nombre}.res.json"), os.path.join(tmp, f"{nombre}.pre.json")
        r = subprocess.run([sys.executable, os.path.join(SCR, "leer_resultados.py"), rec, rj, "--exigir-recalculo-forzado"], capture_output=True, text=True)
        if r.returncode != 0:
            raise SystemExit(f"lectura {nombre}: {(r.stdout + r.stderr)[-300:]}")
        subprocess.run([sys.executable, os.path.join(SCR, "precio_de_si.py"), rj, pj, "--copia", "--k", "3"], capture_output=True, text=True)
        res, pr = json.load(open(rj, encoding="utf-8")), json.load(open(pj, encoding="utf-8"))
        wb = load_workbook(rec, data_only=True, read_only=True)
        d = wb["Diagnóstico V6"]
        out["casos"][nombre] = {"celdas": celdas, "V": [res["valores"].get(x) for x in ("B78", "C78", "D78")], "ponderado": res["valores"].get("C83"),
                                "precio_si": pr.get("precio_si"), "zona": pr.get("zona"), "r_op": d["C15"].value,
                                "valida": (res.get("configuracion_v64") or {}).get("valida")}
        wb.close()
    shutil.rmtree(tmp, ignore_errors=True)
    c = out["casos"]
    out["efecto_del_crecimiento_perpetuo"] = {k: {"ponderado": c[k]["ponderado"] - c[k + "_g0"]["ponderado"], "precio_si": c[k]["precio_si"] - c[k + "_g0"]["precio_si"],
                                                  "V": [a - b for a, b in zip(c[k]["V"], c[k + "_g0"]["V"])]} for k in ("activa", "SR2", "heredado")}
    json.dump(out, open(os.path.join(E413, "resultados", "crecimiento_terminal_vidrala.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    g = lambda x, n=2: f"{x:+.{n}f}".replace(".", ",") if isinstance(x, (int, float)) else "—"  # noqa: E731
    h = lambda x, n=2: f"{x:.{n}f}".replace(".", ",") if isinstance(x, (int, float)) else "—"  # noqa: E731
    md = ["# Vidrala · ¿crea valor el crecimiento terminal en el motor B? (encargo 4.13 §8)", "",
          f"**Qué es.** Recálculos con LibreOffice sobre copias de `{out['libro']}` (4.12; el expediente no cambia). r personal 9 %; el motor B descuenta a r_op = "
          f"{h(c['activa']['r_op'] * 100, 9)} % (Diagnóstico V6 C15, calculada con las entradas). g perpetuo de la fase B: 1 % / 2 % / 2,5 %. ROIC terminal de la fase B: 9 % / 9 % / 12 %.", "",
          "| Caso | V MALO | V NORMAL | V BUENO | Ponderado | Precio de Sí | Zona | r_op |", "|---|---|---|---|---|---|---|---|"]
    for k, x in c.items():
        md.append(f"| {k} | {' | '.join(h(v) for v in x['V'])} | {h(x['ponderado'])} | {h(x['precio_si'])} | {x['zona']} | {h((x['r_op'] or 0) * 100, 6)} % |")
    md += ["", "**Valor que aporta el crecimiento perpetuo** (caso − el mismo con g = 0; € por acción):", "",
           "| Configuración | Δ V MALO | Δ V NORMAL | Δ V BUENO | Δ ponderado | Δ precio de Sí |", "|---|---|---|---|---|---|"]
    for k, e in out["efecto_del_crecimiento_perpetuo"].items():
        md.append(f"| {k} | {' | '.join(g(v) for v in e['V'])} | {g(e['ponderado'])} | {g(e['precio_si'])} |")
    md += ["", "**Lectura (interpretación).** Un ROIC terminal igual a la r personal no hace neutral el crecimiento en el motor B: la perpetuidad se descuenta a r_op, y con "
               "P-M1 el terminal carga además un requisito que crece con las ventas. El signo y el tamaño del efecto son los de la tabla, por escenario; no se deducen de la "
               "igualdad 9 % = 9 % ni de la conclusión contraria («P-M1 introduce inversión adicional, luego el crecimiento destruye valor»). La r personal sigue en el 9 % y r_op se "
               "sigue calculando con las entradas; nada de esto cambia ninguna palanca."]
    open(os.path.join(E413, "resultados", "crecimiento_terminal_vidrala.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
    print("\n".join(md[-12:]))


if __name__ == "__main__":
    main()
