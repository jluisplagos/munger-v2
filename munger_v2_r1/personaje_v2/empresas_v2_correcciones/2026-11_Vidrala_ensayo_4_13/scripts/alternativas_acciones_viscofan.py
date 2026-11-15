#!/usr/bin/env python3
"""Alternativas identificadas del número de acciones de Viscofan (encargo 4.13 §6). Sensibilidades de DEFINICIÓN con fechas mezcladas
(cuentas de 2025, precio del 3-nov-2026), no correcciones adoptadas ni valoraciones actualizadas; no se elige ninguna por su valor.

En COPIAS del libro evaluado (que no se toca), con LibreOffice y en secuencia, se escribe Análisis!C55 (acciones) y,
en la segunda lectura, también C41 (capitalización = 54,70 × N; cambia el peso del patrimonio en r_op). La primera fila reproduce el
caso activo (tiene que dar el precio de Sí de precio.json). Uso (desde munger_v2_r1/): python3 -I …/scripts/alternativas_acciones_viscofan.py
Escribe resultados/alternativas_acciones_viscofan.json y .md en la carpeta del ensayo 4.13.

(4.13, revisión interna R10) Por defecto, el libro evaluado VIGENTE del expediente 4.13 (viscofan/Viscofan, V6.4.1 con el perímetro NIIF 16);
`--libro-4-12` repite la lectura sobre el de la 4.12 (V6.4, «Caja»), que es la que se hizo primero (resultados/antecedentes_libro_4_12/).
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
VIS_412 = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_12", "viscofan", "experimental", "Viscofan")
VIS = VIS_412 if "--libro-4-12" in sys.argv else os.path.join(E413, "viscofan", "Viscofan")
ETIQUETA = "4.12 (V6.4, perímetro «Caja»)" if "--libro-4-12" in sys.argv else "4.13 vigente (V6.4.1, perímetro NIIF 16)"
PRECIO = 54.70
ALT = [("activa_reproduccion", 45.479209, "media ponderada «diluida» publicada de 2025 (nota 20.2; contradictoria: inferior a la básica)"),
       ("media_basica_2025", 45.656226, "media ponderada básica de 2025 (nota 20.1; denominador del BPA básico)"),
       ("circulacion_31dic2025", 45.993399, "acciones en circulación a 31-dic-2025: 46.500.000 − 506.601 propias (fecha de las cuentas)"),
       ("circulacion_30jun2026", 45.603643, "acciones en circulación a 30-jun-2026: 46.000.000 − 396.357 propias (CNMV, informe del primer semestre de 2026)")]
sys.path.insert(0, SCR)


def main():
    from v63_xml import LibroV63
    libro = os.path.join(VIS, "Viscofan_v63_evaluada.xlsx")
    pr0 = json.load(open(os.path.join(VIS, "precio.json"), encoding="utf-8"))
    tmp = tempfile.mkdtemp(prefix="acciones_viscofan_")
    perfil = os.path.join(tmp, ".lo_perfil")
    os.makedirs(os.path.join(tmp, "recalc"))
    filas = []
    for clave, n, concepto in ALT:
        for e_fijo in (True, False):
            if clave == "activa_reproduccion" and not e_fijo:
                continue
            nombre = f"{clave}_{'E_fijo' if e_fijo else 'E_recalculado'}"
            lb = LibroV63(libro)
            celdas = {"Análisis!C55": n} if e_fijo else {"Análisis!C55": n, "Análisis!C41": round(PRECIO * n, 6)}
            lb.escribir_celdas(celdas, {"Análisis": {"C55", "C41"}})
            lb.borrar_caches()
            copia = os.path.join(tmp, f"{nombre}.xlsx")
            lb.guardar(copia)
            r = subprocess.run(["bash", os.path.join(SCR, "recalc.sh"), copia, os.path.join(tmp, "recalc"), perfil], capture_output=True, text=True)
            if r.returncode != 0:
                print(f"recálculo {nombre}: {(r.stdout + r.stderr)[-300:]}")
                return 1
            rec = os.path.join(tmp, "recalc", f"{nombre}.xlsx")
            rj, pj = os.path.join(tmp, f"{nombre}.resultados.json"), os.path.join(tmp, f"{nombre}.precio.json")
            r = subprocess.run([sys.executable, os.path.join(SCR, "leer_resultados.py"), rec, rj, "--exigir-recalculo-forzado"], capture_output=True, text=True)
            if r.returncode != 0:
                print(f"lectura {nombre}: {(r.stdout + r.stderr)[-300:]}")
                return 1
            subprocess.run([sys.executable, os.path.join(SCR, "precio_de_si.py"), rj, pj, "--copia", "--k", "3"], capture_output=True, text=True)
            res, pr = json.load(open(rj, encoding="utf-8")), json.load(open(pj, encoding="utf-8"))
            filas.append({"caso": nombre, "N_mm": n, "concepto": concepto, "E_capitalizacion": celdas.get("Análisis!C41", 2487.7),
                          "ponderado": res["valores"].get("C83"), "precio_si": pr.get("precio_si"), "zona": pr.get("zona"),
                          "valida": (res.get("configuracion_v64") or {}).get("valida")})
    shutil.rmtree(tmp, ignore_errors=True)
    repro = filas[0]
    ok = abs((repro["precio_si"] or 0) - pr0["precio_si"]) <= 1e-9 and abs((repro["ponderado"] or 0) - pr0["ponderado"]) <= 1e-9
    out = {"libro": os.path.relpath(libro, PV), "libro_etiqueta": ETIQUETA, "naturaleza": "sensibilidades de definición con fechas mezcladas (cuentas de 2025, precio del 3-nov-2026); ninguna es una corrección adoptada ni una valoración actualizada",
           "precio": PRECIO, "reproduce_el_caso_activo": ok, "precio_si_activo": pr0["precio_si"], "casos": filas,
           "sensibilidad_externa": {"N": 45.993399, "precio_si_E_fijo": 38.84848, "precio_si_E_recalculado": 38.79687, "activo": 39.28770,
                                     "nota": "del libro de la 4.12 (V6.4, «Caja», fases A y B de entonces): comparables solo con la lectura --libro-4-12"}}
    res = os.path.join(E413, "resultados")
    json.dump(out, open(os.path.join(res, "alternativas_acciones_viscofan.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    g = lambda x, d=5: f"{x:.{d}f}".replace(".", ",") if isinstance(x, (int, float)) else "—"  # noqa: E731
    md = ["# Viscofan · alternativas del número de acciones (encargo 4.13 §6)", "",
          f"**Qué es.** Sensibilidades de definición sobre copias del libro evaluado {ETIQUETA} (`{os.path.relpath(libro, E413)}`), recalculadas con LibreOffice. Mezclan fechas (cuentas de 2025 y precio del 3-nov-2026). No son correcciones adoptadas ni valoraciones actualizadas, y no se elige ninguna por su valor. La conciliación de los conceptos está en `fuentes/CONCILIACION_ACCIONES_VISCOFAN_4_13.md`.", "",
          f"**Reproducción del caso activo:** {'sí' if ok else 'NO'} (precio de Sí {g(repro['precio_si'])} frente a {g(pr0['precio_si'])} de precio.json).", "",
          "| Caso | N (millones) | Concepto | E (capitalización) | Ponderado | Precio de Sí | Zona |", "|---|---|---|---|---|---|---|"]
    md += [f"| {f['caso']} | {g(f['N_mm'], 6)} | {f['concepto']} | {g(f['E_capitalizacion'], 3)} | {g(f['ponderado'], 3)} | {g(f['precio_si'])} | {f['zona']} |" for f in filas]
    md += ["", "**Contraste con la revisión externa** (N = 45,993399): precio de Sí 38,84848 con E y r_op fijos y unos 38,79687 recalculando E = 54,70 × N, frente a 39,28770 del caso activo de la 4.12. "
           + ("Las cifras de esta tabla con N = 45,993399 son las comparables (las dos lecturas: E fijo y E recalculado)." if "--libro-4-12" in sys.argv else
              "Son del libro de la 4.12; en este libro cambian el perímetro y las fases A y B, así que la comparable es la de `antecedentes_libro_4_12/`. Aquí se compara la diferencia relativa entre definiciones."), "",
           f"**Lectura (interpretación).** {'Ninguna alternativa cambia la zona' if len({f['zona'] for f in filas}) == 1 else 'Alguna alternativa cambia la zona'} ({', '.join(sorted({str(f['zona']) for f in filas}))}). "
           f"Entre la media diluida publicada y la circulación a 31-dic-2025 (E fijo), el precio de Sí cambia un {g(100 * (next(f['precio_si'] for f in filas if f['caso'] == 'circulacion_31dic2025_E_fijo') / repro['precio_si'] - 1), 2)} %. "
           "La elección es de definición, no de cálculo: decisión VISCOFAN-ACCIONES de la propuesta."]
    open(os.path.join(res, "alternativas_acciones_viscofan.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
    print("\n".join(md[4:]))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
