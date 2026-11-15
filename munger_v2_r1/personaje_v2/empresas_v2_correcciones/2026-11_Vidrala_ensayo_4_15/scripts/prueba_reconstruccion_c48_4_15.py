#!/usr/bin/env python3
"""Prueba obligatoria de reproducibilidad de C48 de Elis (encargo correctivo 4.15, §3), en carpetas limpias y con LibreOffice en secuencia.

Casos (reconstruir_expediente.py en cada uno; el expediente de la 4.14 no se toca):
  1. elis_decisiones (4.14), entradas declaradas tal como están (su fase1_v63.json): reproduce el número (108) solo por el valor migrado de
     la etapa 1; la vía generativa declara 82,933 y ahora queda registrado como entrada migrada distinta (antes, en silencio).
  2. elis_decisiones (4.14) sin los valores migrados del FCF base: C48 = 82,933 y el precio de Sí cambia (la sensibilidad de la revisión
     externa: 7,3020553231 → 8,9801824507, +1,6781271276): es la discrepancia de reconstrucción, ahora visible.
  3. CAMBIO 4.15 (configuracion/cambio_elis_c48_4_15.json: el de E6 más C48 declarada con su cálculo) preparado con cambiar_base.py en un
     destino temporal y ENSAMBLADO con las celdas de las fases A, B y C y los libros de elis_decisiones (que son la referencia): con
     `construir` desde las entradas declaradas, C48 = 108 y el mismo precio de Sí; las diferencias que queden se clasifican.
  4. Igual que 3, sin los valores migrados del FCF base: C48 sigue en 108 (sale de la vía generativa, no de la protección del migrado).
  5–6. Contraste de la herramienta: viscofan_decisiones y vidrala_decisiones (4.14) con sus entradas declaradas.
  7–8. Viscofan y Vidrala (4.14) sin los valores migrados del FCF base (Vidrala C50 = 0 lo sostiene solo la etapa 1).
Clasificación de las diferencias (no se compensa ninguna): «fecha de ejecución» (Análisis!D4 y sus ecos en Control maestro F4 y G20: la
fecha real de la preparación, declarada como tal por cambiar_base.py), «evidencia documental» (columnas C:N del Control maestro de las
filas de evidencia y su inventario J179:J236: el texto de la fuente de una celda) y «datos, fórmulas o resultados» (todo lo demás).
Uso (desde munger_v2_r1/): python3 -I -B …/prueba_reconstruccion_c48_4_15.py CARPETA_RESULTADOS"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
X = os.path.dirname(AQUI)
PV = os.path.abspath(os.path.join(X, "..", ".."))
RAIZ = os.path.dirname(PV)
E414 = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_14")
REC = os.path.join(AQUI, "reconstruir_expediente.py")
FECHA = {"Análisis!D4", "Control maestro!F4", "Control maestro!G20"}


def clase(celda):
    if celda in FECHA:
        return "fecha de ejecución"
    m = re.match(r"^Control maestro!([C-N])(\d+)$", celda)
    if m and (17 <= int(m.group(2)) <= 175 or 179 <= int(m.group(2)) <= 236):
        return "evidencia documental"
    return "datos, fórmulas o resultados"


def reconstruir(exp, nombre, res, *extra):
    salida = os.path.join(res, f"{nombre}.json")
    r = subprocess.run([sys.executable, "-I", "-B", REC, exp, salida, *extra], capture_output=True, text=True, cwd=RAIZ)
    d = json.load(open(salida, encoding="utf-8"))
    d["codigo_de_salida"] = r.returncode
    cl = {}
    for k in ("libro_datos", "libro_evaluado", "valores_recalculados"):
        for x in (d.get("diferencias", {}).get(k) or {}).get("ejemplos", []):
            cl.setdefault(clase(x["celda"]), set()).add(x["celda"])
    d["clasificacion"] = {k: sorted(v) for k, v in cl.items()}
    json.dump(d, open(salida, "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    return d


def main():
    res = os.path.abspath(sys.argv[1])
    os.makedirs(res, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix="c48_4_15_")
    filas = []
    try:
        el = os.path.join(E414, "elis_decisiones", "Elis")
        filas.append(("1 · Elis 4.14, entradas declaradas", reconstruir(el, "1_elis_4_14_declarado", res, "--fase1", "declarado")))
        filas.append(("2 · Elis 4.14, sin valores migrados del FCF base", reconstruir(el, "2_elis_4_14_sin_migrados", res, "--fase1", "declarado", "--sin-migrados")))
        cambio = json.load(open(os.path.join(X, "configuracion", "cambio_elis_c48_4_15.json"), encoding="utf-8"))
        cambio["destino"] = os.path.join(tmp, "preparado")
        cp = os.path.join(tmp, "cambio.json")
        json.dump(cambio, open(cp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        r = subprocess.run([sys.executable, "-I", "-B", os.path.join(PV, "scripts", "cambiar_base.py"), "preparar", cp], capture_output=True, text=True, cwd=RAIZ)
        if r.returncode != 0:
            raise SystemExit("cambiar_base preparar falló: " + (r.stdout + r.stderr)[-500:])
        ens = os.path.join(tmp, "ensamblado", "Elis")
        shutil.copytree(os.path.join(tmp, "preparado", "Elis"), ens)
        for f in ("celdas_A.json", "celdas_B.json", "celdas_C.json", "Elis_v63_datos.xlsx", "Elis_v63_evaluada.xlsx", "precio.json"):
            shutil.copy2(os.path.join(el, f), os.path.join(ens, f))
        shutil.copytree(os.path.join(el, "recalc"), os.path.join(ens, "recalc"))
        filas.append(("3 · CAMBIO 4.15 (C48 con su cálculo), construir", reconstruir(ens, "3_elis_4_15_construir", res, "--fase1", "construir")))
        filas.append(("4 · CAMBIO 4.15, construir, sin valores migrados", reconstruir(ens, "4_elis_4_15_construir_sin_migrados", res, "--fase1", "construir", "--sin-migrados")))
        filas.append(("5 · Viscofan 4.14, entradas declaradas (contraste)", reconstruir(os.path.join(E414, "viscofan_decisiones", "Viscofan"), "5_viscofan_4_14_declarado", res, "--fase1", "declarado")))
        filas.append(("6 · Vidrala 4.14, entradas declaradas (contraste)", reconstruir(os.path.join(E414, "vidrala_decisiones", "Vidrala"), "6_vidrala_4_14_declarado", res, "--fase1", "declarado")))
        # (revisión independiente del hito 1, hallazgo 19f) también sin los valores migrados del FCF base en los otros dos expedientes
        filas.append(("7 · Viscofan 4.14, sin valores migrados del FCF base", reconstruir(os.path.join(E414, "viscofan_decisiones", "Viscofan"), "7_viscofan_4_14_sin_migrados", res, "--fase1", "declarado", "--sin-migrados")))
        filas.append(("8 · Vidrala 4.14, sin valores migrados del FCF base", reconstruir(os.path.join(E414, "vidrala_decisiones", "Vidrala"), "8_vidrala_4_14_sin_migrados", res, "--fase1", "declarado", "--sin-migrados")))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    g = lambda x: f"{x:.10f}".replace(".", ",") if isinstance(x, (int, float)) else "—"  # noqa: E731
    md = ["# Reproducibilidad de C48 de Elis · reconstrucción en carpetas limpias (4.15)", "",
          "Generado por `scripts/prueba_reconstruccion_c48_4_15.py`. Cada caso reconstruye el expediente desde sus entradas declaradas con "
          "`scripts/reconstruir_expediente.py` (LibreOffice en secuencia) y lo compara con el expediente de referencia. La fecha de revisión del "
          "Control maestro (L5) es un sello de ejecución y se lista aparte.", "",
          "| Caso | Termina | C48 (referencia → reconstruido) | Precio de Sí (referencia → reconstruido) | Diferencia | Diferencias de datos, fórmulas o resultados | Otras diferencias | Entradas migradas distintas (la vía generativa no las reproduce) |",
          "|---|---|---|---|---|---|---|---|"]
    for nombre, d in filas:
        ult = d["pasos"][-1]
        termina = "completo" if "precio_si" in d else f"se detiene en «{ult['paso']}» (código {ult['rc']})"
        c48 = d.get("entradas_fcf_base", {}).get("Análisis!C48") or {}
        ps = d.get("precio_si") or {}
        cl = d.get("clasificacion") or {}
        otras = "; ".join(f"{k}: {', '.join(v)}" for k, v in cl.items() if k != "datos, fórmulas o resultados") or "ninguna"
        lista = cl.get("datos, fórmulas o resultados", [])
        n_dat = (d.get("diferencias", {}).get("valores_recalculados") or {}).get("n", 0)
        entradas = sorted({x["celda"] for k in ("libro_datos",) for x in (d.get("diferencias", {}).get(k) or {}).get("ejemplos", [])
                           if x["celda"].startswith("Análisis!") and clase(x["celda"]) == "datos, fórmulas o resultados"})
        datos = ((f"entradas distintas: {', '.join(entradas) or 'ninguna'}; " if entradas else "") + f"{n_dat} celdas recalculadas distintas (primeras: {', '.join(lista[:3])})") if lista else "ninguna"
        md.append(f"| {nombre} | {termina} | {(c48.get('expediente') or [None, '—'])[1]} → {(c48.get('reconstruido') or [None, '—'])[1]} | {g(ps.get('expediente'))} → {g(ps.get('reconstruido'))} | "
                  f"{g(ps.get('diferencia'))} | {datos} | {otras} | "
                  + (", ".join(f"{x['celda']} (libro {x['libro']} · fase1_v63 {x['fase1_v63']})" for x in d.get("entradas_migradas_distintas") or []) or "ninguna") + " |")
    md += ["", "Detalle de cada caso en su JSON (pasos, salidas, diferencias de fase1_v63.json, libros y valores recalculados)."]
    open(os.path.join(res, "RECONSTRUCCION_C48_4_15.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main()
