#!/usr/bin/env python3
"""Avisos de DOMINIO de la V6.4 experimental (encargo 4.12 §5; revisión interna 4.11 H12 y H13). Solo lee.

Los cuatro dominios que la 4.11 declaró sin comprobar se hacen visibles con sus valores y su motivo. No se adopta ningún umbral
económico: un aviso «activo» es un hecho mecánico del libro (un signo, una comparación con el máximo conservado, una palanca que
no actúa); el factor de reestimación se muestra siempre, con su dominio, porque no tiene cota adoptada. Nada se recorta.
  - inversion_fija_para_crecer_negativa: algún año o el terminal con inversión fija para crecer < 0 (S2C·f > 1 ÷ NWC);
  - factor_de_reestimacion: con una estructura que reestima (SR1, SR2, SRF), f (y f_S2C, f_ROIC, f_fija) con D_hist, Rh, D_hist − Rh y,
    con Λ, el λ en que f deja de estar definida (lectura sin umbral: se muestra siempre en esas estructuras);
  - terminal_r1_sin_maximo_conservado: con R1, el terminal carga inversión fija para crecer aunque las ventas del año 10 sigan por
    debajo del máximo conservado;
  - s2c_inerte: con R1, un escenario cuyas ventas no superan el máximo conservado en ningún año 1–10: la palanca S2C no actúa.
La fase C evalúa cada aviso activo (y el factor) en `configuracion_v64.avisos_de_dominio` (material o no, con la consecuencia); un
aviso material condiciona el objetivo como «limite:<id>» (objetivo_v64) y nunca acompaña una compra.
Uso: dominios_v64.py LIBRO_RECALCULADO.xlsx RESULTADOS.json   (imprime los avisos)
"""
import json
import sys

ESC = (("MALO", 5), ("NORMAL", 35), ("BUENO", 65))
COLS = "BCDEFGHIJK"  # años 1–10; L = terminal
IDS = ("inversion_fija_para_crecer_negativa", "factor_de_reestimacion", "terminal_r1_sin_maximo_conservado", "s2c_inerte")


def _num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def filas_conciliacion(libro):
    """{escenario: {ventas[11], maximo[11], fija[11], s2c_efectivo}} de la hoja «Conciliación B» (copia recalculada)."""
    from openpyxl import load_workbook
    wb = load_workbook(libro, data_only=True, read_only=True)
    if "Conciliación B" not in wb.sheetnames:
        return None
    ws = wb["Conciliación B"]
    out = {}
    for nombre, b in ESC:
        fila = lambda d: [ws[f"{c}{b + d}"].value for c in COLS + "L"]  # noqa: E731
        out[nombre] = {"ventas": fila(2), "maximo": fila(3), "fija": fila(10), "s2c_efectivo": ws[f"B{b + 24}"].value}
    wb.close()
    return out


def avisos(libro, res):
    """Lista de avisos [{id, activo (True · False · None = lectura sin umbral), valores, motivo}] o [] si no es V6.4 experimental."""
    cv = (res or {}).get("configuracion_v64") or {}
    if not cv or str(cv.get("modo") or "") != "Experimental":
        return []
    filas = filas_conciliacion(libro) or {}
    pal = (res or {}).get("palancas") or {}
    s2c = {"MALO": pal.get("B16"), "NORMAL": pal.get("C16"), "BUENO": pal.get("D16")}
    r1 = str(cv.get("regla") or "").startswith("R1")
    out = []
    neg = [{"escenario": e, "anio": ("terminal" if i == 10 else i + 1), "valor": v} for e, d in filas.items() for i, v in enumerate(d["fija"]) if _num(v) and v < -1e-9]
    nwc = cv.get("nwc_efectivo")
    f_s2c = cv.get("f_s2c")
    out.append({"id": IDS[0], "activo": bool(neg), "valores": {"negativos": neg, "nwc_efectivo": nwc, "f_s2c": f_s2c,
                                                                "s2c_por_f": {e: (s * f_s2c if _num(s) and _num(f_s2c) else None) for e, s in s2c.items()},
                                                                "uno_entre_nwc": (1 / nwc if _num(nwc) and nwc else None)},
                "motivo": "la inversión fija para crecer sale negativa cuando S2C·f > 1 ÷ NWC: el modelo liberaría capital fijo al crecer (dominio declarado en la 4.11, H13)"})
    d_hist, rh, sumrep = cv.get("D_hist"), cv.get("Rh"), cv.get("amortizacion_que_se_repone")
    lam_lim = (1 + d_hist / sumrep) if (_num(d_hist) and _num(sumrep) and sumrep > 0 and str(cv.get("familia_texto") or "").startswith("Λ")) else None
    reestima = str(cv.get("codigo_estructura") or "").startswith(("SR1", "SR2", "SRF"))
    out.append({"id": IDS[1], "activo": None if reestima else False, "valores": {"f": cv.get("f"), "estructura": cv.get("codigo_estructura"), "f_s2c": f_s2c, "f_roic": cv.get("f_roic"), "f_fija": cv.get("f_fija"), "D_hist": d_hist, "Rh": rh,
                                                          "D_hist_menos_Rh": (d_hist - rh if _num(d_hist) and _num(rh) else None), "lambda": cv.get("lambda"),
                                                          "lambda_en_que_f_deja_de_estar_definida": lam_lim},
                "motivo": "f = D_hist ÷ (D_hist − Rh) no tiene cota superior adoptada: el S2C y el ROIC reestimados pierden sentido mucho antes de que f deje de estar "
                          "definida (4.11, H13). Se muestra siempre que la estructura reestima (SR1, SR2, SRF); no hay umbral"})
    sin_max, inertes = [], []
    if r1:
        for e, d in filas.items():
            v10, m10, ft = (d["ventas"][9], d["maximo"][9], d["fija"][10])
            if _num(v10) and _num(m10) and _num(ft) and v10 < m10 - 1e-9 and ft > 1e-9:
                sin_max.append({"escenario": e, "ventas_anio_10": v10, "maximo_conservado": m10, "inversion_fija_terminal": ft})
            vs, ms = d["ventas"][:10], d["maximo"][:10]
            if all(_num(v) and _num(m) for v, m in zip(vs, ms)) and not any(v > m + 1e-9 for v, m in zip(vs, ms)):
                inertes.append({"escenario": e, "s2c": s2c.get(e), "ventas_maximas_anios_1_10": max(vs), "maximo_conservado": ms[0]})
    out.append({"id": IDS[2], "activo": bool(sin_max) if r1 else False, "valores": {"regla": cv.get("regla"), "escenarios": sin_max},
                "motivo": "con R1, el terminal carga la inversión fija para crecer al ritmo g aunque las ventas del año 10 sigan por debajo del máximo conservado "
                          "(definición prudente de la 4.7.1/4.8.1; la regla del máximo no se aplica en el terminal)"})
    out.append({"id": IDS[3], "activo": bool(inertes) if r1 else False, "valores": {"regla": cv.get("regla"), "escenarios": inertes},
                "motivo": "con R1, en un escenario cuyas ventas no superan el máximo conservado en ningún año 1–10, la inversión fija para crecer es 0 y la palanca S2C "
                          "de ese escenario no actúa en esos años (4.11, H12)"})
    return out


def agrupar(por_variante, filas, clase_zona=None):
    """(4.13 §5; R7 y RA5 de la revisión 4.12) Avisos de dominio de TODAS las variantes calculadas, agrupados por aviso.
    por_variante: {clave de variante: lista de avisos()}; filas: las variantes (clave, zona, precio_si).
    Devuelve {id: {variantes (activo), lecturas (sin umbral), en_la_activa, afecta, conclusiones, valores_por_variante, f_por_variante}}.
    «afecta» dice de forma mecánica a qué parte del resultado toca: el valor de la activa, un extremo del rango calculado del precio de Sí
    (o su interior) y la invariancia de la acción (si alguna de esas variantes cambia de clase de zona frente a la activa)."""
    clase_zona = clase_zona or {}
    psi = {f["clave"]: f.get("precio_si") for f in filas if f.get("zona") and _num(f.get("precio_si"))}
    zon = {f["clave"]: f.get("zona") for f in filas}
    lo, hi = (min(psi.values()), max(psi.values())) if psi else (None, None)
    c0 = clase_zona.get(zon.get("activa"))
    out = {}
    for aid in IDS:
        act = [k for k, lst in por_variante.items() if any(a.get("id") == aid and a.get("activo") is True for a in lst or [])]
        lec = [k for k, lst in por_variante.items() if any(a.get("id") == aid and a.get("activo") is None for a in lst or [])]
        if not act and not lec:
            continue
        g = act or lec
        afecta = []
        if "activa" in g:
            afecta.append("valor de la activa (precio de Sí y ponderado)")
        ext = [k for k in g if k in psi and psi[k] in (lo, hi)]
        if any(psi.get(k) == lo for k in ext):
            afecta.append("extremo inferior del rango calculado del precio de Sí")
        if any(psi.get(k) == hi for k in ext):
            afecta.append("extremo superior del rango calculado del precio de Sí")
        if any(k in psi and k not in ext for k in g):
            afecta.append("interior del rango calculado")
        cambia = [k for k in g if c0 is not None and clase_zona.get(zon.get(k)) != c0]
        if cambia:
            afecta.append("invariancia de la acción (" + ", ".join(cambia) + " cambian la clase de zona)")
        vals = {k: next((a.get("valores") for a in por_variante[k] if a.get("id") == aid), None) for k in g}
        fs = {k: (v or {}).get("f") for k, v in vals.items()} if aid == IDS[1] else None
        # (4.13, revisión interna R17) en la activa también cuando allí es una lectura sin umbral
        out[aid] = {"variantes": act, "lecturas": lec, "en_la_activa": "activa" in act or "activa" in lec, "afecta": afecta,
                    "conclusiones": sorted({"objetivo (rango calculado)" for x in afecta if "rango" in x or "activa" in x} | ({"acción"} if cambia else set())),
                    "valores_por_variante": {k: (v if aid != IDS[1] else {kk: (v or {}).get(kk) for kk in ("f", "estructura", "D_hist", "Rh", "lambda")}) for k, v in vals.items()},
                    **({"f_minimo": min((x for x in fs.values() if _num(x)), default=None), "f_maximo": max((x for x in fs.values() if _num(x)), default=None)} if fs else {})}
    return out


def grupos_a_evaluar(grupos):
    """Ids de los grupos que la fase C evalúa en `avisos_de_dominio_variantes`: los activos en alguna variante distinta de la activa y la
    lectura del factor de reestimación cuando alguna variante lo tiene (su rango de f entre variantes no se muestra en la activa)."""
    out = []
    for aid, g in (grupos or {}).items():
        if [k for k in g.get("variantes") or [] if k != "activa"] or (aid == IDS[1] and [k for k in g.get("lecturas") or [] if k != "activa"]):
            out.append(aid)
    return out


def que_evaluar(lista):
    """Ids que la fase C tiene que evaluar: los activos y las lecturas sin umbral (activo None)."""
    return [a["id"] for a in lista or [] if a.get("activo") is not False]


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(2)
    print(json.dumps(avisos(sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8"))), ensure_ascii=False, indent=1, default=str))
