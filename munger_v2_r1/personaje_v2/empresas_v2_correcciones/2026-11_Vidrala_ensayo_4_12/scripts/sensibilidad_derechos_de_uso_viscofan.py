#!/usr/bin/env python3
"""Sensibilidad del precio de Sí de Viscofan a la amortización de los derechos de uso dentro de la D&A (revisión interna R8; límite 13 del
README de la V6.4). Lectura de sensibilidad, no una variante del expediente ni una corrección adoptada.

La D&A de la Historia incluye la amortización de los derechos de uso (NIIF 16), que se repone con arrendamientos y no con capex. Con la
familia Θ, el exceso histórico de la plantilla (Configuración V6.4!B60 = Σ capex − D&A de 2021–2025 = 40,813) queda por debajo del exceso
sobre la amortización que sí se repone con capex: 40,813 + 27,051 (Σ de la amortización de derechos de uso 2021–2025, analisis_configuracion
_viscofan.md) = 67,864. Este script recalcula, en COPIAS del libro evaluado del expediente y con LibreOffice (en secuencia), el precio de
Sí con B60 = 67,864 para θ = 0,5 (punto de cálculo de la activa) y θ = 1 (extremo del rango), junto con las mismas copias sin cambiar B60.
No toca el expediente. Uso (desde munger_v2_r1/): python3 -I …/scripts/sensibilidad_derechos_de_uso_viscofan.py
Escribe viscofan/resultados/sensibilidad_derechos_de_uso.json y .md.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
EXP = os.path.dirname(AQUI)
PV = os.path.abspath(os.path.join(EXP, "..", ".."))
SCR = os.path.join(PV, "scripts")
VIS = os.path.join(EXP, "viscofan", "experimental", "Viscofan")
ROU = [5.123, 5.289, 5.293, 5.843, 5.503]  # amortización de derechos de uso 2021–2025 (analisis_configuracion_viscofan.md)
sys.path.insert(0, SCR)


def main():
    import configuracion_economica as CE
    from v63_xml import LibroV63
    libro = os.path.join(VIS, "Viscofan_v63_evaluada.xlsx")
    from openpyxl import load_workbook

    def leer(ruta, ref):  # valor en caché del libro recalculado
        return load_workbook(ruta, data_only=True, read_only=True)[CE.HOJA][ref].value
    b60 = leer(libro, "B60")
    b60_rou = round(b60 + sum(ROU), 6)
    tmp = tempfile.mkdtemp(prefix="rou_viscofan_")
    perfil = os.path.join(tmp, ".lo_perfil")
    os.makedirs(os.path.join(tmp, "recalc"))
    # B60 es una fórmula protegida: con la familia Θ, el requisito anual (θ × B60 ÷ 5) y Rh (θ × B60, que fija f en SR1) solo dependen del
    # producto θ × B60, así que contar el exceso sin los derechos de uso con θ equivale a θ' = θ × B60' ÷ B60 con el B60 de la plantilla
    # (exacto con SR1; F_hist, que también usa B60, solo entra en SRF). θ' = 1,66 queda fuera del dominio declarado [0, 1]: la plantilla puede rechazarlo
    k = b60_rou / b60
    casos = [("theta_0.5", 0.5, 0.5), ("theta_0.5_rou", 0.5, 0.5 * k), ("theta_1", 1.0, 1.0), ("theta_1_rou", 1.0, 1.0 * k)]
    filas = []
    for clave, theta_lectura, theta in casos:
        lb = LibroV63(libro)
        celdas = {f"{CE.HOJA}!B39": round(theta, 10)}
        lb.escribir_celdas(celdas, {CE.HOJA: {"B39"}})
        lb.borrar_caches()
        copia = os.path.join(tmp, f"{clave}.xlsx")
        lb.guardar(copia)
        r = subprocess.run(["bash", os.path.join(SCR, "recalc.sh"), copia, os.path.join(tmp, "recalc"), perfil], capture_output=True, text=True)
        if r.returncode != 0:
            print(f"recálculo {clave}: {(r.stdout + r.stderr)[-300:]}")
            return 1
        rec = os.path.join(tmp, "recalc", f"{clave}.xlsx")
        rj, pj = os.path.join(tmp, f"{clave}.resultados.json"), os.path.join(tmp, f"{clave}.precio.json")
        r = subprocess.run([sys.executable, os.path.join(SCR, "leer_resultados.py"), rec, rj, "--exigir-recalculo-forzado"], capture_output=True, text=True)
        if r.returncode != 0:
            print(f"lectura {clave}: {(r.stdout + r.stderr)[-300:]}")
            return 1
        subprocess.run([sys.executable, os.path.join(SCR, "precio_de_si.py"), rj, pj, "--copia", "--k", "3"], capture_output=True, text=True)
        res, pr = json.load(open(rj, encoding="utf-8")), json.load(open(pj, encoding="utf-8"))
        filas.append({"caso": clave, "theta": theta_lectura, "theta_escrito": round(theta, 6), "B60_equivalente": round(theta * b60 / theta_lectura, 6), "B60": leer(rec, "B60"), "requisito_anual_B88": leer(rec, "B88"), "f_B72": leer(rec, "B72"),
                      "V": [res["valores"].get(x) for x in ("B78", "C78", "D78")], "ponderado": res["valores"].get("C83"),
                      "precio_si": pr.get("precio_si"), "zona": pr.get("zona"), "valida": (res.get("configuracion_v64") or {}).get("valida")})
    shutil.rmtree(tmp, ignore_errors=True)
    d = {f["caso"]: f for f in filas}
    dif = lambda a, b: (a - b) if isinstance(a, (int, float)) and isinstance(b, (int, float)) else None  # noqa: E731
    efecto = {"theta_0.5": dif(d["theta_0.5_rou"]["precio_si"], d["theta_0.5"]["precio_si"]), "theta_1": dif(d["theta_1_rou"]["precio_si"], d["theta_1"]["precio_si"])}
    out = {"naturaleza": "lectura de sensibilidad sobre copias; no es una variante del expediente ni una corrección adoptada", "B60_plantilla": b60,
           "B60_sin_derechos_de_uso": b60_rou, "suma_amortizacion_derechos_de_uso_2021_2025": round(sum(ROU), 6), "casos": filas, "efecto_en_el_precio_si": efecto}
    res = os.path.join(EXP, "viscofan", "resultados")
    json.dump(out, open(os.path.join(res, "sensibilidad_derechos_de_uso.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    g = lambda x, n=4: f"{x:.{n}f}" if isinstance(x, (int, float)) else "—"  # noqa: E731
    md = ["# Viscofan · sensibilidad a la amortización de los derechos de uso (revisión interna R8; límite 13)", "",
          f"**Qué es.** Una lectura de sensibilidad sobre copias del libro evaluado, recalculadas con LibreOffice: el exceso histórico de la plantilla "
          f"(Configuración V6.4!B60 = {g(b60, 3)}) frente al exceso sobre la amortización que se repone con capex ({g(b60_rou, 3)}, sumando la amortización de los "
          f"derechos de uso de 2021–2025, {g(sum(ROU), 3)}). No es una variante del expediente ni una corrección adoptada.", "",
          "Método: con la familia Θ, el requisito anual (θ × B60 ÷ 5) y Rh (θ × B60, que fija f en SR1) solo dependen de θ × B60, así que el exceso sin los derechos de uso se calcula escribiendo θ' = θ × B60' ÷ B60 (B60 es una fórmula protegida). θ' > 1 queda fuera del dominio declarado.", "",
          "| Caso | θ de la lectura | θ escrito | B60 equivalente | Requisito anual (B88) | f (B72) | Ponderado | Precio de Sí | Zona | ¿Válida? |", "|---|---|---|---|---|---|---|---|---|---|"]
    md += [f"| {f['caso']} | {f['theta']} | {f['theta_escrito']} | {g(f['B60_equivalente'], 3)} | {g(f['requisito_anual_B88'], 3)} | {g(f['f_B72'])} | {g(f['ponderado'], 2)} | {g(f['precio_si'], 2)} | {f['zona']} | {f['valida']} |" for f in filas]
    fe = lambda x: f"{x:+.2f} €" if isinstance(x, (int, float)) else "sin valor (fuera del dominio)"  # noqa: E731
    md += ["", f"**Efecto en el precio de Sí** de contar solo la amortización que se repone con capex: θ = 0,5 → {fe(efecto['theta_0.5'])}; θ = 1 → {fe(efecto['theta_1'])}. "
           + ("En los casos calculados la zona no cambia (caro). " if all(f["zona"] == "caro" for f in filas if f["valida"]) else "")
           + (f"Con θ = 0,5 el precio de Sí ({d['theta_0.5_rou']['precio_si']:.2f} €) queda {'por encima' if d['theta_0.5_rou']['precio_si'] >= 38.2214 else 'por debajo'} del extremo inferior del rango calculado del expediente (38,22 €). "
              if isinstance(d["theta_0.5_rou"]["precio_si"], (int, float)) else "")
           + ("Con θ = 1 no hay cifra: el θ equivalente queda fuera del dominio declarado y la plantilla marca la configuración como no válida; "
              "para calcularlo habría que editar una fórmula protegida de la plantilla (B60), y no se hace. Queda como límite sin cifra. "
              if not d["theta_1_rou"]["valida"] else "")
           + f"La medición es parcial: solo cambia el exceso (B60), no la base de reinversión de D_hist (B55) ni, por ella, f (revisión de lo afectado, RA2). "
             f"Con el exceso corregido, θ = {b60 / b60_rou:.4f} equivale exactamente a θ = 1 con el de la plantilla ({d['theta_1']['precio_si']:.2f} €); un θ mayor queda fuera del dominio declarado."]
    open(os.path.join(res, "sensibilidad_derechos_de_uso.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
    print("\n".join(md))
    return 0


if __name__ == "__main__":
    sys.exit(main())
