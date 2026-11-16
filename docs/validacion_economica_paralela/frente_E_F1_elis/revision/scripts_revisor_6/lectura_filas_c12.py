"""Revisión n.º 6 (frente E · F1 · Elis). Lectura independiente de las siete filas nuevas de C12, de las entradas que
contrastan con ellas y de las identidades R41, R8 de 2021–22, R24 de 2023 y R42. No modifica nada del autor.

Dos lecturas que no usan pdftotext ni las funciones del autor:
  - pdfminer (pdfplumber): palabras con su caja en puntos. La columna de cada número se identifica por las palabras de
    cabecera cuyo borde derecho coincide con el del número (las tablas de Elis alinean cabecera y cifra por la derecha);
  - PDFium (pypdfium2): texto de la página; el rótulo debe ir seguido de los mismos números en el mismo orden.

Para cada fila se imprime: pie de la página (publicación), cabecera de la página (estados consolidados o informe de
gestión), declaración de unidades de la tabla, cabecera de cada columna de la línea y el número de la posición declarada.
Después se calculan las identidades con fracciones exactas, y la cota y la sensibilidad de R42.

Uso: python3 -I lectura_filas_c12.py --raiz <munger_v2_r1> --autor <frente C13>
"""
import argparse
import csv
import json
import re
import sys
from fractions import Fraction as Fr
from pathlib import Path

import pypdfium2

sys.path.insert(0, str(Path(__file__).resolve().parent))
import geom  # noqa: E402

# id → patrón del rótulo en la fila geométrica (palabras unidas con un espacio)
FILAS_NUEVAS = ["BAI_NOTA9_U22_2021", "BAI_NOTA9_U23_2022", "CF_DAP_U22_2021", "PROV_TOT_U22_2021", "CF_DAP_U23_2022", "PROV_TOT_U23_2022",
                "DN_ADQ_FR_2023"]
CONTRAPARTES = ["IS_BAI_U22_2021", "IS_BAI_U23_2022", "DA_TOTAL_U22_2021", "DA_SUBV_U22_2021", "DA_TOTAL_U23_2022", "DA_SUBV_U23_2022",
                "CF_ADQ_FR_2023", "CREC_PUB_2021", "CREC_PUB_2022", "CREC_PUB_2023", "CREC_PUB_2024", "CREC_PUB_2025",
                "IS_VENTAS_U21_2020", "IS_VENTAS_U22_2021", "IS_VENTAS_U23_2022", "IS_VENTAS_FR_2023", "IS_VENTAS_2024", "IS_VENTAS_2025"]
ROTULO = {
    "BAI_NOTA9_U22_2021": r"^Income \(loss\) before tax\b", "BAI_NOTA9_U23_2022": r"^INCOME \(LOSS\) BEFORE TAX\b",
    "CF_DAP_U22_2021": r"^Depreciation, amortization and provisions\b", "CF_DAP_U23_2022": r"^Depreciation, amortization and provisions\b",
    "PROV_TOT_U22_2021": r"^TOTAL ADDITIONS TO OR REVERSALS OF PROVISIONS\b", "PROV_TOT_U23_2022": r"^TOTAL ADDITIONS TO OR REVERSALS OF PROVISIONS\b",
    "DN_ADQ_FR_2023": r"^Acquisitions de filiales, sous déduction de la trésorerie acquise",
    "IS_BAI_U22_2021": r"^Income \(loss\) before tax\b", "IS_BAI_U23_2022": r"^Income \(loss\) before tax\b",
    "DA_TOTAL_U22_2021": r"TO INCOME\)", "DA_TOTAL_U23_2022": r"TO INCOME\)",
    "DA_SUBV_U22_2021": r"^(?:› )?Portion of grants transferred to income", "DA_SUBV_U23_2022": r"^(?:› )?Portion of grants transferred to income",
    "CF_ADQ_FR_2023": r"^Acquisition de filiales, sous déduction de la trésorerie acquise",
    "IS_VENTAS_U21_2020": r"^Revenue\b", "IS_VENTAS_U22_2021": r"^Revenue\b", "IS_VENTAS_U23_2022": r"^Revenue\b",
    "IS_VENTAS_FR_2023": r"^Produits de l'activité ordinaire", "IS_VENTAS_2024": r"^Revenue\b", "IS_VENTAS_2025": r"^Revenue\b",
}
for _y in range(2021, 2026):
    ROTULO[f"CREC_PUB_{_y}"] = r"^TOTAL\b"


def valor(lit, fr):
    t = lit.replace(" ", " ").strip()
    neg = t.startswith("(") or t[:1] in "-–−"
    n = re.sub(r"[^\d.,]", "", t)
    n = n.replace(" ", "").replace(",", ".") if fr else n.replace(",", "")
    v = Fr(n)
    return -v if neg else v


def leer(pdf, fr, pagina, rx, literal, pos):
    """Lectura geométrica: fila cuyo texto casa con rx y contiene el literal; devuelve un dict con todo lo leído."""
    ws = geom.palabras(pdf, pagina)
    fs = geom.filas(ws)
    lit_n = re.sub(r"\s+", " ", literal.replace(" ", " ")).strip()
    cands = []
    for k, f in enumerate(fs):
        if not re.search(rx, f["txt"]):
            continue
        nums = geom.unir_numeros(f["ws"], fr)
        if any(re.sub(r"\s+", " ", t).replace("+ ", "+ ") == lit_n or re.sub(r"\s+", "", t) == re.sub(r"\s+", "", lit_n) for _, _, t in nums):
            cands.append((k, nums))
    if not cands:
        return {"error": "no se localiza la fila con pdfminer"}
    out = {"filas_que_casan": len(cands)}
    k, nums = cands[0]
    f = fs[k]
    out["linea"] = f["txt"]
    out["numeros"] = []
    j_un = None
    for x0, x1, t in nums:
        cab = geom.cabecera_del_token(fs, k, x0, x1)
        j_un = cab["j0"]
        out["numeros"].append({"texto": t, "x1": round(x1, 1), "cabecera_alineada_por_la_derecha": cab["alineadas"],
                               "cabecera_que_solapa": cab["solapan"]})
    out["unidades"] = fs[j_un]["txt"][:80] if j_un is not None else None
    idx = pos % len(nums) if -len(nums) <= pos < len(nums) else None
    out["token_de_la_posicion"] = nums[idx][2] if idx is not None else None
    out["columna_del_token"] = out["numeros"][idx]["cabecera_alineada_por_la_derecha"] if idx is not None else None
    # cabecera y pie de la página
    arriba = [f_["txt"] for f_ in fs if f_["c"] < 70]
    out["cabecera_de_pagina"] = " ‖ ".join(arriba)[:160]
    pie = [f_["txt"] for f_ in fs if re.search(r"Universal Registration Document|enregistrement universel", f_["txt"])]
    out["pie"] = pie[-1][:90] if pie else None
    # títulos por encima de la tabla: las tres filas no vacías anteriores a la cabecera
    j0 = j_un if j_un is not None else k
    tit = []
    j = j0 - 1
    while j >= 0 and len(tit) < 4:
        t_ = fs[j]["txt"]
        if not re.search(r"\d[.,]\d", t_) or len(t_) < 60:
            tit.append(t_[:100])
        j -= 1
    out["por_encima_de_la_tabla"] = tit
    return out


def leer_pdfium(pdf, pagina, rx_txt, literal):
    doc = pypdfium2.PdfDocument(str(pdf))
    tp = doc[pagina - 1].get_textpage()
    txt = tp.get_text_range().replace("\r\n", "\n").replace("\r", "\n").replace("’", "'").replace("￾", "").replace("\u0002", "")
    lineas = [l for l in txt.split("\n")]
    lit = re.sub(r"\s+", " ", literal.replace(" ", " ")).strip()
    for i, l in enumerate(lineas):
        l2 = re.sub(r"\s+", " ", l.replace(" ", " ")).strip()
        if re.search(rx_txt.replace("^", "").replace(r"\b", ""), l2) and (lit in l2 or lit.replace(" ", "") in l2.replace(" ", "")):
            return l2[:170]
    # el rótulo y los números pueden estar en líneas distintas: se devuelve la ventana
    for i, l in enumerate(lineas):
        if re.search(rx_txt.replace("^", "").replace(r"\b", ""), re.sub(r"\s+", " ", l)):
            ventana = " ⏎ ".join(re.sub(r"\s+", " ", x.replace(" ", " ")).strip() for x in lineas[i:i + 3])
            if lit in ventana or lit.replace(" ", "") in ventana.replace(" ", ""):
                return ventana[:200]
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raiz", required=True, type=Path)
    ap.add_argument("--autor", required=True, type=Path)
    a = ap.parse_args()
    fuentes = json.loads((a.autor / "datos" / "fuentes.json").read_text(encoding="utf-8"))["fuentes"]
    filas = {r["id"]: r for r in csv.DictReader((a.autor / "datos" / "cifras_fuente.csv").open(encoding="utf-8"), delimiter=";")}
    V = {}
    dif = 0
    for bloque, ids in (("SIETE FILAS NUEVAS DE C12", FILAS_NUEVAS), ("ENTRADAS QUE CONTRASTAN CON ELLAS Y ENTRADAS DE R42", CONTRAPARTES)):
        print(f"\n{'=' * 8} {bloque} {'=' * 8}")
        for i in ids:
            r = filas[i]
            fr = fuentes[r["doc"]]["idioma"] == "fr"
            pdf = a.raiz / fuentes[r["doc"]]["archivo"]
            g = leer(pdf, fr, int(r["pagina"]), ROTULO[i], r["literal"], int(r["pos"]))
            pf = leer_pdfium(pdf, int(r["pagina"]), ROTULO[i], r["literal"])
            print(f"\n{i} · {r['doc']} p.{r['pagina']} · declarado: ejercicio {r['anio']}, pos {r['pos']}, literal «{r['literal']}», {r['unidad']}, {r['perimetro']}, edición {r['edicion']}")
            if "error" in g:
                print("   pdfminer:", g["error"])
                dif += 1
                continue
            print(f"   pdfminer · línea: «{g['linea'][:120]}» (filas que casan: {g['filas_que_casan']})")
            for n in g["numeros"]:
                print(f"      número «{n['texto']}» (borde derecho {n['x1']}) · cabecera alineada: {n['cabecera_alineada_por_la_derecha']}"
                      + (f" · solapa: {n['cabecera_que_solapa']}" if n["cabecera_que_solapa"] else ""))
            print(f"   token de la posición declarada: «{g['token_de_la_posicion']}» · columna: {g['columna_del_token']}")
            print(f"   unidades de la tabla: {g['unidades']}")
            print(f"   por encima de la tabla: {g['por_encima_de_la_tabla']}")
            print(f"   cabecera de la página: {g['cabecera_de_pagina']}")
            print(f"   pie: {g['pie']}")
            print(f"   PDFium · {pf}")
            tok = g["token_de_la_posicion"] or ""
            igual = re.sub(r"\s+", "", tok) == re.sub(r"\s+", "", r["literal"].replace(" ", " "))
            anio_ok = any(str(r["anio"]) in c for c in (g["columna_del_token"] or [])) or r["control_anio"] == "crecimiento"
            if not igual or pf is None or not anio_ok:
                dif += 1
            print(f"   → literal de la posición = declarado: {'sí' if igual else 'NO'} · cabecera de la columna con el ejercicio {r['anio']}: "
                  f"{'sí' if anio_ok else 'NO'}{' (tabla de crecimiento: ejercicio por la cabecera de la tabla)' if r['control_anio'] == 'crecimiento' else ''}"
                  f" · PDFium lo confirma: {'sí' if pf else 'NO'}")
            V[i] = valor(r["literal"], fr)
    print(f"\nLecturas con alguna diferencia: {dif}")

    print(f"\n{'=' * 8} IDENTIDADES (fracciones exactas) {'=' * 8}")
    e = Fr(5, 100)

    def ident(nombre, residuo, n_cifras):
        cota = n_cifras * e
        print(f"   {nombre}: residuo {float(residuo):+.3f} · cota {float(cota):.2f} ({n_cifras} cifras de un decimal) · {'dentro' if abs(residuo) <= cota else 'FUERA'}")

    ident("R41 2021  BAI cuenta de resultados (URD22 p.258) − BAI nota 9 (p.326)", V["IS_BAI_U22_2021"] - V["BAI_NOTA9_U22_2021"], 2)
    ident("R41 2022  BAI cuenta de resultados (URD23 p.276) − BAI nota 9 (p.345)", V["IS_BAI_U23_2022"] - V["BAI_NOTA9_U23_2022"], 2)
    ident("R8 2021   línea EFE (URD22 p.261) − (D&A total + subvención + dotación neta) (p.284)",
          V["CF_DAP_U22_2021"] - (-V["DA_TOTAL_U22_2021"] + V["DA_SUBV_U22_2021"] - V["PROV_TOT_U22_2021"]), 4)
    ident("R8 2022   línea EFE (URD23 p.279) − (D&A total + subvención + dotación neta) (p.301)",
          V["CF_DAP_U23_2022"] - (-V["DA_TOTAL_U23_2022"] + V["DA_SUBV_U23_2022"] - V["PROV_TOT_U23_2022"]), 4)
    ident("R24 2023  adquisiciones EFE (DEU24 p.273) − puente de la deuda neta (p.260)", -V["CF_ADQ_FR_2023"] - (-V["DN_ADQ_FR_2023"]), 2)

    print(f"\n{'=' * 8} R42: crecimiento publicado − crecimiento de las ventas {'=' * 8}")
    ventas = {2020: V["IS_VENTAS_U21_2020"], 2021: V["IS_VENTAS_U22_2021"], 2022: V["IS_VENTAS_U23_2022"], 2023: V["IS_VENTAS_FR_2023"],
              2024: V["IS_VENTAS_2024"], 2025: V["IS_VENTAS_2025"]}
    print("   año · V / V₋₁ · crecimiento de las ventas · publicado · residuo · cota linealizada · cota exacta (peor caso) · diferencia")
    R = {}
    for y in range(2021, 2026):
        Vy, Vp, c = ventas[y], ventas[y - 1], V[f"CREC_PUB_{y}"]
        r = c - 100 * (Vy / Vp - 1)
        cota_lin = e + 100 * e / Vp + 100 * Vy * e / Vp ** 2
        # peor caso exacto: publicado ± 0,05; V ± 0,05; V₋₁ ∓ 0,05 (el cociente es monótono en cada variable)
        peor = max(abs((c + s * e) - 100 * ((Vy - s * e) / (Vp + s * e) - 1) - r) for s in (1, -1))
        R[y] = (r, cota_lin, Vy, Vp, c)
        print(f"   {y} · {float(Vy):.1f} / {float(Vp):.1f} · {float(100 * (Vy / Vp - 1)):.4f} % · {float(c):.1f} % · {float(r):+.4f} · "
              f"{float(cota_lin):.6f} · {float(peor):.6f} · {float(peor - cota_lin):.2e} · {'dentro' if abs(r) <= cota_lin else 'FUERA'}")
    print("\n   Umbral de detección de R42 (menor error que hace salir el residuo de su cota), por variable y signo del error:")
    print("   año · publicado (puntos): +/− · ventas del año (mm EUR): +/− · ventas del año anterior (mm EUR): +/−")
    for y, (r, cota, Vy, Vp, c) in R.items():
        up_c, dn_c = cota - r, cota + r                      # ∂r/∂c = 1
        sV = -100 / Vp                                       # ∂r/∂V < 0
        up_V, dn_V = (cota + r) / -sV, (cota - r) / -sV      # +ΔV baja r; −ΔV sube r
        sP = 100 * Vy / Vp ** 2                              # ∂r/∂V₋₁ > 0
        up_P, dn_P = (cota - r) / sP, (cota + r) / sP
        print(f"   {y} · +{float(up_c):.3f} / −{float(dn_c):.3f} · +{float(up_V):.2f} / −{float(dn_V):.2f} · +{float(up_P):.2f} / −{float(dn_P):.2f}"
              f"   (un +3,0 en V₋₁ mueve el residuo {float(3 * sP):+.4f} → {float(r + 3 * sP):+.4f}: {'detectado' if abs(r + 3 * sP) > cota else 'NO detectado'};"
              f" un +3,0 en V, {float(3 * sV):+.4f} → {float(r + 3 * sV):+.4f}: {'detectado' if abs(r + 3 * sV) > cota else 'NO detectado'})")
    print("\n   ¿Rompe R42 una fila de segmento? Crecimiento publicado de cada fila de segmento de las cinco tablas frente al crecimiento de las ventas del grupo:")
    for y in range(2021, 2026):
        r = filas[f"CREC_PUB_{y}"]
        fr = fuentes[r["doc"]]["idioma"] == "fr"
        fs = geom.filas(geom.palabras(a.raiz / fuentes[r["doc"]]["archivo"], int(r["pagina"])))
        k_tot = next(k for k, f in enumerate(fs) if re.match(r"^TOTAL\b", f["txt"]) and "%" in f["txt"])
        k_un = next(k for k in range(k_tot, -1, -1) if geom.UNIDAD.search(fs[k]["txt"]))
        pos = int(r["pos"])
        _, cota, Vy, Vp, c = R[y]
        g = 100 * (Vy / Vp - 1)
        segs = []
        for k in range(k_un + 1, k_tot):
            ns = geom.unir_numeros(fs[k]["ws"], fr)
            if len(ns) >= 4 and "%" in ns[pos][2]:
                etiqueta = " ".join(w["t"] for w in fs[k]["ws"] if w["x1"] < ns[0][0])
                if not etiqueta and k > 0:
                    etiqueta = fs[k - 1]["txt"] + " / " + (fs[k + 1]["txt"] if k + 1 < k_tot else "")
                segs.append((etiqueta[:34], valor(ns[pos][2].replace("%", ""), fr)))
        cerca = min(segs, key=lambda x: abs(x[1] - g))
        print(f"   {y} · {r['doc']} p.{r['pagina']} · {len(segs)} filas de segmento · crecimiento de las ventas del grupo {float(g):.3f} % · la más próxima: «{cerca[0]}» {float(cerca[1]):.1f} % "
              f"(distancia {float(abs(cerca[1] - g)):.3f}; cota {float(cota):.3f}) · filas que NO romperían R42: {sum(1 for s_ in segs if abs(s_[1] - g) <= cota)}")
    print("\n   Ventas de 2021 y de 2022: su única identidad entre páginas es R42 (dos años cada una). Intervalo de error que ninguna de las dos detecta:")
    for nombre, y_v, y_p in (("IS_VENTAS_U22_2021 (3.048,3)", 2021, 2022), ("IS_VENTAS_U23_2022 (3.820,9)", 2022, 2023)):
        r1, c1, Vy1, Vp1, _ = R[y_v]       # como V del año y_v
        r2, c2, Vy2, Vp2, _ = R[y_p]       # como V₋₁ del año y_p
        s1, s2 = -100 / Vp1, 100 * Vy2 / Vp2 ** 2
        # no detectado si |r1 + s1·d| ≤ c1 y |r2 + s2·d| ≤ c2
        lo = max((r1 - c1) / -s1, (-c2 - r2) / s2)
        hi = min((r1 + c1) / -s1, (c2 - r2) / s2)
        print(f"   {nombre}: errores entre {float(lo):+.2f} y {float(hi):+.2f} mm EUR no hacen fallar R42 de {y_v} ni de {y_p} "
              f"(anchura {float(hi - lo):.2f}; una identidad lineal de dos cifras detecta desde ±0,10)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
