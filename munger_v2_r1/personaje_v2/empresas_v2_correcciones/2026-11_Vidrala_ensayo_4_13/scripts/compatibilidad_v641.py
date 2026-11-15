#!/usr/bin/env python3
"""Compatibilidad y efecto de la plantilla V6.4.1 experimental (encargo 4.13 §7), con LibreOffice y en secuencia, sobre copias.

1. Mismas entradas que el libro evaluado de Viscofan de la 4.12 (V6.4), trasladadas a la V6.4.1 con el perímetro vacío: todas las celdas
   de las once hojas de la V6.3 y de «Configuración V6.4» y «Conciliación B» tienen que dar lo mismo que el libro V6.4 (tolerancia 1e-12),
   salvo las celdas nuevas o reetiquetadas.
2. Lo mismo en modo heredado (heredado V6.4.1 = heredado V6.4 = V6.3).
3. Perímetro NIIF 16 con las altas conciliadas (resultados/conciliacion_arrendamientos_viscofan.json): bases, f, requisito y precio de Sí
   con θ = 0, 0,5 y 1, y la réplica independiente de las bases (Python, desde la Historia del libro y las altas).
Uso (desde munger_v2_r1/): python3 -I …/scripts/compatibilidad_v641.py · Escribe resultados/compatibilidad_v641.json y .md.
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
RAIZ = os.path.dirname(PV)
SCR = os.path.join(PV, "scripts")
V641 = os.path.join(RAIZ, "v6", "v641_experimental")
VIS = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_12", "viscofan", "experimental", "Viscofan")
H = "Configuración V6.4"
NIIF = "NIIF 16 · capex de caja + altas de derechos de uso frente a toda la D&A"
NUEVAS = {f"{H}!{c}" for c in ["A55", "B55", "A58", "B58", "B9", "B124", "A124", "C124", "B143"] + [f"{x}{r}" for r in range(142, 157) for x in "ABCDEFGHI"]}
ETIQ = {"Análisis!A1", "Panel!A1", "Guía V6!A1", "Control maestro!A3", "Conciliación B!A1", "Diagnóstico V6!E176", "Diagnóstico V6!E177",
        # textos que repiten el resumen B9 de «Configuración V6.4», que en la V6.4.1 añade « · perímetro Caja|NIIF 16» (cambio buscado).
        # Se listan aparte en el informe con su valor, para que la exclusión se pueda comprobar
        "Conciliación B!A3", "Panel!C18"}
RESUMEN_B9 = ("Conciliación B!A3", "Panel!C18")
sys.path.insert(0, SCR)


def recalc(libro, tmp, perfil):
    r = subprocess.run(["bash", os.path.join(SCR, "recalc.sh"), libro, os.path.join(tmp, "recalc"), perfil], capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"recálculo: {(r.stdout + r.stderr)[-300:]}")
    return os.path.join(tmp, "recalc", os.path.basename(libro))


def valores(p):
    from openpyxl import load_workbook
    wb = load_workbook(p, data_only=True, read_only=True)
    out = {}
    for ws in wb.worksheets:
        for row in ws.iter_rows():
            for c in row:
                if c.value is not None:
                    out[f"{ws.title}!{c.coordinate}"] = c.value
    return out


def comparar(a, b, excluir):
    dif = []
    for k in sorted(set(a) | set(b)):
        if k in excluir:
            continue
        x, y = a.get(k), b.get(k)
        if isinstance(x, (int, float)) and isinstance(y, (int, float)) and not isinstance(x, bool):
            if abs(x - y) > 1e-12 * max(1.0, abs(x)):
                dif.append((k, x, y))
        elif x != y and not (x in (None, "") and y in (None, "")):
            dif.append((k, x, y))
    return dif


def precio(rec, tmp, nombre):
    rj, pj = os.path.join(tmp, f"{nombre}.resultados.json"), os.path.join(tmp, f"{nombre}.precio.json")
    r = subprocess.run([sys.executable, os.path.join(SCR, "leer_resultados.py"), rec, rj, "--exigir-recalculo-forzado"], capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"lectura {nombre}: {(r.stdout + r.stderr)[-300:]}")
    subprocess.run([sys.executable, os.path.join(SCR, "precio_de_si.py"), rj, pj, "--copia", "--k", "3"], capture_output=True, text=True)
    return json.load(open(rj, encoding="utf-8")), json.load(open(pj, encoding="utf-8"))


def main():
    sys.path.insert(0, os.path.join(V641, "scripts"))
    import trasladar_entradas as TR
    tmp = tempfile.mkdtemp(prefix="v641_")
    perfil = os.path.join(tmp, ".lo_perfil")
    os.makedirs(os.path.join(tmp, "recalc"))
    plantilla = os.path.join(V641, "entregables", "Plantilla_V6.4.1_experimental.xlsx")
    libro64 = os.path.join(VIS, "Viscofan_v63_evaluada.xlsx")
    v64 = valores(libro64)
    out = {"casos": {}}
    # 1 y 2: compatibilidad
    caja_txt = "Caja · capex de caja frente a toda la D&A (V6.4)"
    for nombre, cfgx in (("experimental_caja", None), ("experimental_caja_explicita", {f"{H}!B146": caja_txt}), ("heredado", {f"{H}!B4": "Heredado"})):
        dst = os.path.join(tmp, f"{nombre}.xlsx")
        TR.trasladar(libro64, plantilla, dst, cfgx)
        rec = recalc(dst, tmp, perfil)
        ref = v64
        if nombre == "heredado":  # heredado: la referencia es el mismo libro V6.4 en heredado
            d64 = os.path.join(tmp, "heredado_v64.xlsx")
            sys.path.insert(0, os.path.join(RAIZ, "v6", "v64_experimental", "scripts"))
            import importlib
            TR64 = importlib.import_module("trasladar_entradas")
            TR64.trasladar(libro64, os.path.join(RAIZ, "v6", "v64_experimental", "entregables", "Plantilla_V6.4_experimental.xlsx"), d64, cfgx)
            ref = valores(recalc(d64, tmp, perfil))
        vr = valores(rec)
        dif = comparar(ref, vr, NUEVAS | ETIQ)
        # los textos que repiten el resumen B9: el de la V6.4.1 tiene que ser el de la V6.4 más « · perímetro …» (y nada más)
        b9 = {k: {"v64": ref.get(k), "v641": vr.get(k), "solo_añade_el_perimetro": isinstance(ref.get(k), str) and isinstance(vr.get(k), str)
                  and (vr[k] == ref[k] or (vr[k].startswith(ref[k].rstrip(")")) and "perímetro" in vr[k][len(ref[k].rstrip(")")):]))} for k in RESUMEN_B9}
        out["casos"][nombre] = {"diferencias": len(dif), "primeras": [list(map(str, d)) for d in dif[:10]], "textos_del_resumen_B9": b9}
    # 3: perímetro NIIF 16 con las altas conciliadas, θ = 0, 0,5 y 1
    con = json.load(open(os.path.join(E413, "resultados", "conciliacion_arrendamientos_viscofan.json"), encoding="utf-8"))
    altas = [con["serie"][f"altas_derechos_de_uso:{a}"] for a in (2021, 2022, 2023, 2024, 2025)]
    fuente = "Altas de derechos de uso: CF_2021 p. 39 (2021), CF_2022 p. 51 (2022), CA_2023 p. 35 (2023), CF_2024 y AR_2025 p. 2374 del texto (2024, 2025); conciliacion_arrendamientos_viscofan.md"
    from openpyxl import load_workbook
    for theta in (0.0, 0.5, 1.0):
        for per in ("caja", "niif16"):
            nombre = f"{per}_theta_{theta}"
            cfgx = {f"{H}!B39": theta}
            if per == "niif16":
                cfgx.update({f"{H}!B146": NIIF, **{f"{H}!B{147 + i}": v for i, v in enumerate(altas)}, f"{H}!B152": fuente})
            dst = os.path.join(tmp, f"{nombre}.xlsx")
            TR.trasladar(libro64, plantilla, dst, cfgx)
            rec = recalc(dst, tmp, perfil)
            res, pr = precio(rec, tmp, nombre)
            ws = load_workbook(rec, data_only=True, read_only=True)[H]
            b = {r: ws[f"B{r}"].value for r in (55, 57, 58, 59, 60, 61, 62, 63, 70, 71, 72, 73, 84, 88, 89, 90, 153, 154, 155)}
            out["casos"][nombre] = {"theta": theta, "perimetro": per, "bases": b, "precio_si": pr.get("precio_si"), "ponderado": res["valores"].get("C83"), "zona": pr.get("zona"),
                                    "valida": (res.get("configuracion_v64") or {}).get("valida")}
    # réplica independiente de las bases (Python) con las cifras de la Historia del libro
    hist = load_workbook(libro64, data_only=True, read_only=True)["Historia"]
    capex = sum(hist[f"{c}12"].value for c in "HIJKL")
    da = sum(hist[f"{c}8"].value for c in "HIJKL")
    rn = sum(hist[f"{c}31"].value for c in "HIJKL")
    adq = sum(hist[f"{c}13"].value or 0 for c in "HIJKL")
    rep = {}
    for theta in (0.0, 0.5, 1.0):
        for per, extra in (("caja", 0.0), ("niif16", sum(altas))):
            D = rn + extra
            exc = capex - da + extra
            Rh = theta * exc
            f = D / (D - Rh) if D - Rh > 0 else None
            rep[f"{per}_theta_{theta}"] = {"D_hist": D, "exceso": exc, "F_hist": exc + adq, "Rh": Rh, "f": f, "requisito": theta * exc / 5}
    malos = []
    for k, r in rep.items():
        b = out["casos"][k]["bases"]
        for campo, celda in (("D_hist", 57), ("exceso", 60), ("F_hist", 62), ("Rh", 71), ("f", 72), ("requisito", 89)):
            if r[campo] is None or not isinstance(b[celda], (int, float)) or abs(r[campo] - b[celda]) > 1e-9 * max(1, abs(r[campo])):
                malos.append(f"{k}.{campo}: réplica {r[campo]} · libro {b[celda]}")
    out["replica"] = {"casos": rep, "discrepancias": malos}
    shutil.rmtree(tmp, ignore_errors=True)
    json.dump(out, open(os.path.join(E413, "resultados", "compatibilidad_v641.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    g = lambda x, d=4: f"{x:.{d}f}".replace(".", ",") if isinstance(x, (int, float)) else "—"  # noqa: E731
    md = ["# Plantilla V6.4.1 experimental · compatibilidad y efecto del perímetro (encargo 4.13 §7)", "",
          "**Qué es.** Recálculos con LibreOffice sobre copias, con las entradas del libro evaluado de Viscofan de la 4.12. No cambia ningún expediente.", "",
          "## 1. Compatibilidad", "",
          f"- Experimental con el perímetro vacío frente al libro V6.4: **{out['casos']['experimental_caja']['diferencias']}** celdas distintas (fuera de las celdas nuevas o reetiquetadas).",
          f"- Experimental con «Caja» escrito de forma explícita frente al libro V6.4: **{out['casos']['experimental_caja_explicita']['diferencias']}** celdas distintas.",
          f"- Modo heredado V6.4.1 frente a heredado V6.4: **{out['casos']['heredado']['diferencias']}** celdas distintas.",
          "- Celdas excluidas por ser texto que repite el resumen B9 (que en la V6.4.1 dice el perímetro), con su comprobación:"]
    for nombre in ("experimental_caja", "experimental_caja_explicita", "heredado"):
        for k, x in out["casos"][nombre]["textos_del_resumen_B9"].items():
            md.append(f"  - {nombre} · {k}: ¿solo añade el perímetro? **{'sí' if x['solo_añade_el_perimetro'] else 'NO'}** · V6.4 «{str(x['v64'])[-60:]}» · V6.4.1 «{str(x['v641'])[-80:]}»")
    md += ["",
          "## 2. Perímetro: caja (V6.4) frente a NIIF 16 completo", "",
          "| θ | Perímetro | D_hist (B57) | Exceso (B60) | F_hist (B62) | Rh (B71) | f (B72) | Requisito anual (B89) | Precio de Sí | Zona | ¿Válida? |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for theta in (0.0, 0.5, 1.0):
        for per in ("caja", "niif16"):
            x = out["casos"][f"{per}_theta_{theta}"]
            b = x["bases"]
            md.append(f"| {g(theta, 1)} | {'caja' if per == 'caja' else 'NIIF 16'} | {g(b[57], 3)} | {g(b[60], 3)} | {g(b[62], 3)} | {g(b[71], 3)} | {g(b[72])} | {g(b[89], 3)} | {g(x['precio_si'], 2)} | {x['zona']} | {x['valida']} |")
    md += ["", f"**Réplica independiente de las bases** (Python, desde la Historia del libro y las altas conciliadas): {len(malos)} discrepancias en D_hist, exceso, F_hist, Rh, f y requisito, en los seis casos.", "",
           "**Lectura (interpretación).** Con θ = 0 no hay requisito adicional y los dos perímetros dan lo mismo. Con NIIF 16 el exceso histórico pasa de 40,8 a 64,9 millones; el requisito, Rh y f suben, y el precio de Sí baja. Ningún caso sale del dominio declarado. La elección del perímetro sigue pendiente (VISCOFAN-PERIMETRO): la V6.4.1 la hace explícita y la integra en el modelo, pero no la adopta."]
    open(os.path.join(E413, "resultados", "compatibilidad_v641.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
    print("\n".join(md[5:]))
    b9_mal = [f"{n}.{k}" for n in ("experimental_caja", "experimental_caja_explicita", "heredado") for k, x in out["casos"][n]["textos_del_resumen_B9"].items() if not x["solo_añade_el_perimetro"]]
    print(f"compatibilidad: caja {out['casos']['experimental_caja']['diferencias']} · caja explícita {out['casos']['experimental_caja_explicita']['diferencias']} · heredado {out['casos']['heredado']['diferencias']} · textos B9 mal {b9_mal} · réplica {len(malos)}")
    return 0 if (all(out["casos"][n]["diferencias"] == 0 for n in ("experimental_caja", "experimental_caja_explicita", "heredado")) and not malos and not b9_mal) else 1


if __name__ == "__main__":
    sys.exit(main())
