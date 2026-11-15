"""Cálculo de contraste independiente · F1 · Elis (frente E). Solo lectura; no modifica libros ni datos.

Parte de las cifras verificadas contra los PDF (datos/cifras_fuente.csv + resultados/verificacion_cifras.json) y
calcula con aritmética exacta (fracciones decimales), sin copiar las fórmulas del libro:
  A. Historia y Análisis C46–C52 reconstruidos desde la fuente y comparados con el libro (valores en caché).
  B. Conciliaciones anuales 2023–2025 (EBIT→CFO, D&A, capex, circulante, impuestos, arrendamientos, deuda) con residuos.
  C. FCF base por dos vías (CFO y free cash flow publicado − SBC) y f por dos vías: la definición de la plantilla
     y una descomposición económica componente a componente que debe sumar exactamente lo mismo.
  D. Motor A reimplementado desde Convenciones_financieras_V6_3.md (no desde las celdas) y contrastado con los
     flujos en caché del libro (solo flujos; no se calculan valores por acción).
  E. Puentes FCF base → flujo sin crecimiento del motor → flujo del año 1, y descomposición de la reinversión media.
  F. Arrendamientos: dónde está cada elemento en la calibración y en la proyección.
  G. Alternativas de perímetro de la reinversión necesaria (A0–A2 y cota B) con f, flujo de partida y anclas S2C.
     Son consecuencias calculadas de definiciones, NO propuestas adoptadas ni valoraciones.
Uso:
  python3 -I contraste_f1.py --cifras ../datos/cifras_fuente.csv --verificacion ../resultados/verificacion_cifras.json \
     [--libro <ruta>/Elis_v63_evaluada.xlsx] --salida ../resultados/contraste_f1.json --informe ../resultados/contraste_f1.md
Requiere openpyxl solo si se pasa --libro.
"""
import argparse
import csv
import hashlib
import json
import sys
from fractions import Fraction as Fr
from pathlib import Path

SHA_LIBRO = "d2593777650f1d9d77bcc7b9eaa6f4c0c12a742fa4706bd20b35808f99c92385"
VENTANA = (2023, 2024, 2025)
HORIZONTE = (2021, 2022, 2023, 2024, 2025)


def f6(x, n=6):
    return None if x is None else round(float(x), n)


# ---------------------------------------------------------------- datos de fuente
PERIMETRO_GRUPO = "consolidado IFRS, grupo Elis"


class Fuente:
    """Cifras verificadas. Solo entrega a los cálculos filas sin FALLO, de la edición vigente, del perímetro del grupo
    y con la unidad que pide cada cálculo; anota las que se usan con alguna dimensión PENDIENTE."""

    def __init__(self, ruta_csv, ruta_verif):
        verif = json.loads(Path(ruta_verif).read_text(encoding="utf-8"))
        if verif["resumen"]["fallos"]:
            sys.exit("la verificación de cifras tiene fallos: no se calcula sobre datos no verificados")
        # (revisión n.º 3, N3) la verificación debe ser la de este mismo CSV
        h = hashlib.sha256(Path(ruta_csv).read_bytes()).hexdigest()
        if (verif.get("huellas") or {}).get("datos") != h:
            sys.exit("la verificación no corresponde a este CSV (huella distinta): hay que volver a verificar")
        est = {r["id"]: r for r in verif["cifras"]}
        self.v, self.ref, self.meta = {}, {}, {}
        self.usadas, self.pendientes, self.contrapartes_pendientes = set(), {}, {}
        for r in csv.DictReader(Path(ruta_csv).open(encoding="utf-8"), delimiter=";"):
            if r["tipo"] != "tabla":
                continue
            e = est.get(r["id"])
            if e is None or e["estado"] == "FALLO":
                sys.exit(f"cifra sin verificar: {r['id']}")
            if e.get("literal") != r["literal"] or e.get("valor_publicado") != r["valor_publicado"]:
                sys.exit(f"{r['id']}: el literal o el valor del CSV no son los verificados")
            self.v[r["id"]] = Fr(r["valor_publicado"])
            self.ref[r["id"]] = f"{r['doc']} p.{r['pagina']} «{r['literal']}»"
            self.meta[r["id"]] = {"unidad": r["unidad"], "perimetro": r["perimetro"], "edicion": r["edicion"], "doc": r["doc"],
                                  "pagina": int(r["pagina"]), "decimales": e["decimales"], "estado": e["estado"],
                                  "motivo": e.get("motivo", "")}

    def __call__(self, i, unidad="mm EUR", contraparte=False):
        """contraparte=True: la cifra solo sirve de segunda presentación en una identidad. Si está PENDIENTE, se anota
        aparte y no hace pendientes los resultados: la identidad es, precisamente, una comprobación de esa cifra."""
        m = self.meta[i]
        if m["edicion"] != "vigente":
            sys.exit(f"{i}: un cálculo usa una cifra de edición «{m['edicion']}»; solo vale la edición vigente")
        if m["unidad"] != unidad:
            sys.exit(f"{i}: el cálculo pide {unidad} y la cifra está en {m['unidad']}")
        if m["perimetro"] != PERIMETRO_GRUPO:
            sys.exit(f"{i}: perímetro {m['perimetro']!r}, no el del grupo")
        self.usadas.add(i)
        if m["estado"] == "PENDIENTE":
            (self.contrapartes_pendientes if contraparte else self.pendientes)[i] = m["motivo"]
        return self.v[i]

    def pct(self, i):
        return self(i, "%")

    def epsilon(self, i):
        """Media unidad de la última cifra impresa: el error máximo de redondeo de la cifra publicada."""
        return Fr(5, 10 ** (self.meta[i]["decimales"] + 1))


class Q:
    """Cantidad lineal con su procedencia: valor exacto y coeficiente de cada cifra impresa que interviene."""
    __slots__ = ("v", "t")

    def __init__(self, v=0, t=None):
        self.v = Fr(v)
        self.t = {k: c for k, c in (t or {}).items() if c != 0}

    @staticmethod
    def de(x):
        return x if isinstance(x, Q) else Q(x)

    def __add__(self, o):
        o = Q.de(o)
        t = dict(self.t)
        for k, c in o.t.items():
            t[k] = t.get(k, 0) + c
        return Q(self.v + o.v, t)

    __radd__ = __add__

    def __neg__(self):
        return Q(-self.v, {k: -c for k, c in self.t.items()})

    def __sub__(self, o):
        return self + (-Q.de(o))

    def __rsub__(self, o):
        return Q.de(o) - self

    def __mul__(self, k):
        if isinstance(k, Q):
            raise TypeError("producto de dos cantidades: no es lineal")
        return Q(self.v * k, {i: c * k for i, c in self.t.items()})

    __rmul__ = __mul__

    def __truediv__(self, k):
        if isinstance(k, Q):
            raise TypeError("cociente de dos cantidades: no es lineal")
        return self * (Fr(1) / Fr(k))


class FuenteQ:
    """Misma interfaz que Fuente, pero devuelve cantidades con procedencia (para las tolerancias de redondeo)."""

    def __init__(self, F):
        self.F = F

    def __call__(self, i, unidad="mm EUR", contraparte=False):
        return Q(self.F(i, unidad, contraparte), {i: 1})

    def pct(self, i):
        return Q(self.F.pct(i), {i: 1})


def datos_anio(F, y):
    """Partidas de un ejercicio con la regla de la publicación más reciente (la de la Historia)."""
    d = {}
    if y in VENTANA:
        s = {2025: "_2025", 2024: "_2024", 2023: "_FR_2023"}[y]
        g = lambda b: b + s  # noqa: E731
        d["ventas"] = F(g("IS_VENTAS"))
        d["ebit_pub"] = F(g("IS_EBIT")) if y != 2024 else F("IS_EBIT_2024")
        d["fin"] = -F(g("IS_FIN"))            # gasto financiero neto (positivo)
        d["bai"] = F(g("IS_BAI"))
        d["imp"] = -F(g("IS_IMP"))            # gasto por impuesto (positivo)
        d["bn"] = F(g("IS_BN"))
        for k, b in [("cf_bn", "CF_BN"), ("cf_imp", "CF_IMP"), ("cf_fin", "CF_FIN"), ("sbc", "CF_SBC"), ("dap", "CF_DAP"),
                     ("cf_subv", "CF_SUBV"), ("plusv", "CF_PLUSV"), ("earn", "CF_EARN"), ("cf_antes", "CF_ANTES"),
                     ("cfo", "CF_CFO"), ("empl", "CF_EMPL"), ("desint", "CF_DESINT"), ("desmat", "CF_DESMAT"),
                     ("subvinv", "CF_SUBVINV"), ("ampl", "CF_AMPL"), ("autoc", "CF_AUTOC"), ("div", "CF_DIV"),
                     ("empr", "CF_EMPR"), ("reemb", "CF_REEMB"), ("ofin", "CF_OFIN")]:
            d[k] = F(g(b))
        d["wc_lineas"] = sum(F(g(b)) for b in ("CF_EXIS", "CF_CLI", "CF_OAC", "CF_PROV", "CF_PCON", "CF_OTRV"))
        d["imppag"] = -F(g("CF_IMPPAG"))
        d["capint"], d["capmat"] = -F(g("CF_CAPINT")), -F(g("CF_CAPMAT"))
        d["adq"] = -F(g("CF_ADQ"))
        d["leasepay"] = -F(g("CF_LEASE"))
        d["int"] = -F(g("CF_INT"))
        d["fcf_antes"], d["capnet"], d["bfr"] = F(g("FCF_ANTES")), -F(g("FCF_CAPNET")), -F(g("FCF_BFR"))
        d["fcf_apm"] = F(g("FCF_FCF"))
        d["sbcsoc"] = -F(g("FCF_SBCSOC"))
        d["lino"], d["oart"], d["otro"] = -F(g("CAPX_LINO")), -F(g("CAPX_OART")), -F(g("CAPX_OTRO"))
        d["ces"], d["subv_capex"], d["capnet_tabla"] = F(g("CAPX_CES")), F(g("CAPX_SUBV")), -F(g("CAPX_NETO"))
        for k, b in [("da_ebit", "DA_EBIT"), ("da_text", "DA_TEXT"), ("da_oart", "DA_OART"), ("da_otro", "DA_OTRO"),
                     ("da_rou", "DA_ROU"), ("da_deter", "DA_DETER"), ("da_ppa", "DA_PPA"), ("da_total", "DA_TOTAL")]:
            d[k] = -F(g(b))
        d["da_subv"] = F(g("DA_SUBV"))
        d["prov_cargo"] = -F(g("PROV_TOT"))   # dotación neta (positivo = cargo)
        d["ooie_earn"], d["ooie_plusv"] = F(g("OOIE_EARN")), F(g("OOIE_PLUSV"))
        d["int_ls_dev"] = -F(g("FIN_INTLS"))
        d["tax_corr"], d["tax_dif"], d["tax_real"], d["tax_cvae"] = F(g("TAX_CORR")), F(g("TAX_DIF")), F(g("TAX_REAL")), F(g("TAX_CVAE"))
        d["deu_bruta"], d["deu_caja"], d["deu_neta"], d["oceane"] = F(g("DEU_BRUTA")), F(g("DEU_CAJA")), F(g("DEU_NETA")), F(g("DEU_OCEANE"))
        # (revisión n.º 3, N2) líneas y totales de inversión y financiación; composición del crecimiento
        for k, b in [("cesfil", "CF_CESFIL"), ("prest", "CF_PREST"), ("divrec", "CF_DIVREC"), ("invtot", "CF_INVTOT"), ("fintot", "CF_FINTOT")]:
            d[k] = F(g(b), contraparte=True)
        d["crec_ext"], d["crec_fx"], d["crec_pub"] = (F.pct(f"CREC_EXT_{y}"), F.pct(f"CREC_FX_{y}"), F.pct(f"CREC_PUB_{y}"))
        if y != 2023:
            d["ooie_tot"], d["is_ooie"] = F(g("OOIE_TOT"), contraparte=True), F(g("IS_OOIE"), contraparte=True)
        # segundas presentaciones en otras páginas (contraste entre páginas de las entradas clave)
        d["fin_nota"], d["tax_bai"], d["is_ppa"] = -F(g("FIN_TOT")), F(g("TAX_BAI")), -F(g("IS_PPA"))
        d["ventas_seg"] = F({2025: "VENTAS_SEG_2025", 2024: "VENTAS_SEG_2024", 2023: "VENTAS_SEG_FR_2023"}[y])
        if y != 2023:                                   # el DEU 2024 no se usa para el puente de la deuda neta de 2023
            d["dn_adq"] = -F(f"DN_ADQ_{y}")
        d["sbc_ifrs2"] = -F(g("EBITA_SBC")) if y != 2023 else F("EBITA_SBC_FR_2023")
        d["crec_org"] = F.pct(f"CREC_ORG_{y}")
        d["taxdif_int"], d["taxdif_rou"], d["taxdif_ls"] = F(f"TAXDIF_INT_{y}"), F(f"TAXDIF_ROU_{y}"), F(f"TAXDIF_LS_{y}")
        # arrendamientos
        ly = str(y)
        d["ls_princ"] = -F(f"LS_PRINC_PAS_{ly}")
        d["ls_nuevo"], d["ls_reest"], d["ls_comb"] = F(f"LS_NUEVO_ROU_{ly}"), F(f"LS_REEST_ROU_{ly}"), F(f"LS_COMB_ROU_{ly}")
        d["ls_nuevo_pas"], d["ls_reest_pas"], d["ls_comb_pas"] = F(f"LS_NUEVO_PAS_{ly}"), F(f"LS_REEST_PAS_{ly}"), F(f"LS_COMB_PAS_{ly}")
        d["ls_amort"] = -F(f"LS_AMORT_ROU_{ly}")
        d["ls_fx_rou"], d["ls_fx_pas"] = F(f"LS_FX_ROU_{ly}"), F(f"LS_FX_PAS_{ly}")
        d["ls_otros_rou"], d["ls_otros_pas"] = F(f"LS_OTROS_ROU_{ly}"), F(f"LS_OTROS_PAS_{ly}")
        d["ls_deter"] = -F(f"LS_DETER_ROU_{ly}") if y != 2023 else Fr(0)
        if y == 2024:   # cierre de 2023 en el DEU 2024 frente a la apertura de 2024 en el URD 2025 (dos ediciones vigentes)
            d["rou_cierre_ed_ant"] = F("LS_SALDO_ROU_2023_FR", contraparte=True)
            d["pas_cierre_ed_ant"] = F("LS_SALDO_PAS_2023_FR", contraparte=True)
            d["rc_cierre_ed_ant"], d["rc_apertura"] = F("INT_RC_VNC_2023_FR", contraparte=True), F("INT_RC_VNC_2023", contraparte=True)
        if y == 2023:
            d["rou_ini"], d["pas_ini"] = F("LS_SALDO_ROU_2022"), F("LS_SALDO_PAS_2022")
            d["rou_fin"], d["pas_fin"] = F("LS_SALDO_ROU_2023_FR"), F("LS_SALDO_PAS_2023_FR")
        else:
            d["rou_ini"], d["pas_ini"] = F(f"LS_SALDO_ROU_{y-1}"), F(f"LS_SALDO_PAS_{y-1}")
            d["rou_fin"], d["pas_fin"] = F(f"LS_SALDO_ROU_{y}"), F(f"LS_SALDO_PAS_{y}")
    elif y == 2022:
        u = "_U23_2022"
        d["ventas"] = F("IS_VENTAS" + u)
        d["fin"], d["bai"], d["imp"] = -F("IS_FIN" + u), F("IS_BAI" + u), -F("IS_IMP" + u)
        d["ebit_pub"] = F("IS_EBIT" + u)
        d["cfo"], d["sbc"] = F("CF_CFO" + u), F("CF_SBC" + u)
        d["capint"], d["capmat"], d["adq"] = -F("CF_CAPINT" + u), -F("CF_CAPMAT" + u), -F("CF_ADQ" + u)
        d["wc_lineas"] = sum(F(b + u) for b in ("CF_EXIS", "CF_CLI", "CF_OAC", "CF_PROV", "CF_PCON", "CF_OTRV"))
        d["empl"] = F("CF_EMPL" + u)
        d["int_con_ls"], d["ls_princ"] = -F("CF_INTCONLS" + u), -F("CF_LSPRINC" + u)
        d["lino"], d["oart"], d["otro"] = -F("CAPX_LINO" + u), -F("CAPX_OART" + u), -F("CAPX_OTRO" + u)
        d["ces"], d["capnet_tabla"] = F("CAPX_CES" + u), -F("CAPX_NETO" + u)
        for k, b in [("da_text", "DA_TEXT"), ("da_oart", "DA_OART"), ("da_otro", "DA_OTRO"), ("da_rou", "DA_ROU"),
                     ("da_deter", "DA_DETER"), ("da_ppa", "DA_PPA"), ("da_total", "DA_TOTAL")]:
            d[k] = -F(b + u)
        d["da_subv"] = F("DA_SUBV" + u)
        d["int_ls_dev"] = -F("FIN_INTLS" + u)
        d["fcf_apm"] = F("FCF_FCF" + u)
        d["crec_org"] = F.pct("CREC_ORG_2022")
        # (revisión n.º 3, N2) segundas presentaciones para las identidades del horizonte
        d["ls_amort"], d["is_ppa"] = -F("LS_AMORT_ROU_2022", contraparte=True), -F("IS_PPA" + u, contraparte=True)
        d["bfr"] = -F("FCF_BFR" + u, contraparte=True)    # circulante del APM (URD 2023 p.268), segunda presentación
        # (C9) impuesto de la nota 9 (p.345) y flujo neto total de la nota 2.4 (p.294): segundas presentaciones
        d["tax_corr"], d["tax_dif"] = F("TAX_CORR" + u, contraparte=True), F("TAX_DIF" + u, contraparte=True)
        d["adq_nota"] = -F("CF_ADQ_NOTA" + u, contraparte=True)
        d["crec_ext"], d["crec_fx"], d["crec_pub"] = F.pct("CREC_EXT_2022"), F.pct("CREC_FX_2022"), F.pct("CREC_PUB_2022")
    elif y == 2021:
        u = "_U22_2021"
        d["ventas"] = F("IS_VENTAS" + u)
        d["fin"], d["bai"], d["imp"] = -F("IS_FIN" + u), F("IS_BAI" + u), -F("IS_IMP" + u)
        d["ebit_pub"] = F("IS_EBIT" + u)
        d["cfo"], d["sbc"], d["sbc_nota52"] = F("CF_CFO" + u), F("CF_SBC" + u), -F("SBC_N52" + u)
        d["capint"], d["capmat"], d["adq"] = -F("CF_CAPINT" + u), -F("CF_CAPMAT" + u), -F("CF_ADQ" + u)
        d["wc_lineas"] = sum(F(b + u) for b in ("CF_EXIS", "CF_CLI", "CF_OAC", "CF_PROV", "CF_PCON", "CF_OTRV"))
        d["empl"] = F("CF_EMPL" + u)
        d["int_con_ls"], d["ls_princ"] = -F("CF_INTCONLS" + u), -F("CF_LSPRINC" + u)
        d["lino"], d["oart"], d["otro"] = -F("CAPX_LINO" + u), -F("CAPX_OART" + u), -F("CAPX_OTRO" + u)
        d["ces"], d["capnet_tabla"] = F("CAPX_CES" + u), -F("CAPX_NETO" + u)
        for k, b in [("da_text", "DA_TEXT"), ("da_oart", "DA_OART"), ("da_otro", "DA_OTRO"), ("da_rou", "DA_ROU"),
                     ("da_deter", "DA_DETER"), ("da_ppa", "DA_PPA"), ("da_total", "DA_TOTAL")]:
            d[k] = -F(b + u)
        d["da_subv"] = F("DA_SUBV" + u)
        d["int_ls_dev"] = -F("FIN_INTLS" + u)
        d["fcf_apm"] = F("FCF_FCF" + u)
        d["crec_org"] = F.pct("CREC_ORG_2021")
        d["ls_amort"], d["is_ppa"] = -F("LS_AMORT_ROU_2021", contraparte=True), -F("IS_PPA" + u, contraparte=True)
        d["bfr"] = -F("FCF_BFR" + u, contraparte=True)    # circulante del APM (URD 2022 p.250), segunda presentación
        # (C9) impuesto de la nota 9 (p.326), flujo neto total de la nota 2.4 (p.277) y ventas de 2020 del informe
        # de gestión del URD 2021 (p.213) frente a las de su cuenta de resultados (p.226), que son S2020
        d["tax_corr"], d["tax_dif"] = F("TAX_CORR" + u, contraparte=True), F("TAX_DIF" + u, contraparte=True)
        d["adq_nota"] = -F("CF_ADQ_NOTA" + u, contraparte=True)
        d["ventas_2020"], d["ventas_2020_mr"] = F("IS_VENTAS_U21_2020"), F("IS_VENTAS_MR_U21_2020", contraparte=True)
    # derivadas comunes
    d["ebit_h"] = d["bai"] + d["fin"]                        # definición de la Historia (v2.2)
    if not isinstance(d["bai"], Q):                          # τ no es lineal: solo con valores exactos
        d["tau"] = Fr(round(d["imp"] / d["bai"], 4)).limit_denominator(10 ** 4)   # fila 10: 4 decimales
        d["tau_exacto"] = d["imp"] / d["bai"]
    d["capex"] = d["capint"] + d["capmat"]
    d["dwc"] = -(d["wc_lineas"] + d["empl"])                 # fila 14: + consume caja
    d["d_own"] = d["da_total"] - d["da_rou"] - d["da_ppa"]  # D&A propia (lino, otros artículos, resto, subv., deterioro)
    return d


# ---------------------------------------------------------------- libro (solo lectura de valores en caché)
def leer_libro(ruta):
    h = hashlib.sha256(Path(ruta).read_bytes()).hexdigest()
    if h != SHA_LIBRO:
        sys.exit(f"huella del libro distinta: {h}")
    import openpyxl
    wb = openpyxl.load_workbook(ruta, data_only=True, read_only=True)
    out = {"sha256": h}
    for hoja, rango in [("Historia", "A5:L81"), ("Análisis", "B46:D80"), ("Palancas", "B14:D23"), ("Motor", "A6:BT9"),
                        ("Diagnóstico V6", "C5:C14")]:
        ws = wb[hoja]
        for fila in ws[rango]:
            for c in fila:
                if c.value is not None:
                    out[f"{hoja}!{c.coordinate}"] = c.value
    return out


COL = {2016: "C", 2017: "D", 2018: "E", 2019: "F", 2020: "G", 2021: "H", 2022: "I", 2023: "J", 2024: "K", 2025: "L"}


# ---------------------------------------------------------------- motor A desde la convención
def motor_a(V0, m0, tau, f, g15, m_obj, s2c, g_inf, roic):
    """Convenciones V6.3: g_t (1–5 palanca; 6–10 lineal hasta g∞), m_t lineal a 5 años, flujo_t = V_t·[m_t(1−τ) − f] − ΔV/S2C."""
    V_prev, flujos, V = V0, [], []
    for t in range(1, 11):
        g_t = g15 if t <= 5 else g15 - (g15 - g_inf) * Fr(t - 5, 5)
        Vt = V_prev * (1 + g_t)
        mt = m0 + (m_obj - m0) * Fr(min(t, 5), 5)
        flujos.append(Vt * (mt * (1 - tau) - f) - (Vt - V_prev) / s2c)
        V.append(Vt)
        V_prev = Vt
    terminal = V[-1] * (1 + g_inf) * (m_obj * (1 - tau) * (1 - g_inf / roic) - f)
    sin_crec = V0 * (m0 * (1 - tau) - f)
    return {"flujos": flujos, "flujo_11": terminal, "flujo_sin_crecimiento": sin_crec, "V": V}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cifras", required=True, type=Path)
    ap.add_argument("--verificacion", required=True, type=Path)
    ap.add_argument("--libro", type=Path)
    ap.add_argument("--salida", required=True, type=Path)
    ap.add_argument("--informe", required=True, type=Path)
    ap.add_argument("--caja-no-nula", type=Path, help="resultados de prueba_caja_no_nula.py (copia del libro recalculada)")
    a = ap.parse_args()
    F = Fuente(a.cifras, a.verificacion)
    A = {y: datos_anio(F, y) for y in HORIZONTE}
    S2020 = F("IS_VENTAS_U21_2020")
    L = leer_libro(a.libro) if a.libro else None
    R = {"comprobaciones": [], "tablas": {}}
    md = []

    def check(nombre, calculado, referencia, tolerancia=Fr(0), nota="", clase="libro"):
        """clase: «libro» (frente al libro en caché), «fuente» (dos vías independientes o identidades de las cifras
        publicadas con tolerancia de redondeo) o «algebraica» (identidad que se cumple por construcción; documenta, no prueba datos)."""
        dif = calculado - referencia
        ok = abs(dif) <= tolerancia
        R["comprobaciones"].append({"nombre": nombre, "clase": clase, "calculado": f6(calculado), "referencia": f6(referencia),
                                    "diferencia": f6(dif, 9), "tolerancia": f6(tolerancia), "ok": ok, "nota": nota})
        return ok

    def avg(fn, anios=VENTANA):
        return sum(fn(A[y]) for y in anios) / len(anios)

    # ======================= B. conciliaciones anuales 2023–2025
    def residuos(d):
        ebit_cf = d["cf_bn"] + d["cf_imp"] + d["cf_fin"]
        return {
            "R1 EBIT publicado − (BAI + resultado financiero)": d["ebit_pub"] - d["ebit_h"],
            "R2 EBIT del EFE (BN+impuesto+financiero) − EBIT publicado": ebit_cf - d["ebit_pub"],
            "R3 caja antes de financieros e impuestos − suma de sus líneas": d["cf_antes"] - (ebit_cf + d["sbc"] + d["dap"] + d["cf_subv"] + d["plusv"] + d["earn"]),
            "R4 CFO − (caja antes − circulante − impuestos pagados)": d["cfo"] - (d["cf_antes"] - d["dwc"] - d["imppag"]),
            "R5 circulante APM − circulante de las líneas del EFE": d["bfr"] - d["dwc"],
            "R6 D&A en EBIT − suma de componentes": d["da_ebit"] - (d["da_text"] + d["da_oart"] + d["da_otro"] + d["da_rou"] - d["da_subv"]),
            "R7 D&A total − (D&A en EBIT + deterioro + PPA)": d["da_total"] - (d["da_ebit"] + d["da_deter"] + d["da_ppa"]),
            "R8 línea EFE amortizaciones y provisiones − (D&A total + subvención + provisiones)": d["dap"] - (d["da_total"] + d["da_subv"] + d["prov_cargo"]),
            "R9 capex bruto EFE − capex por tipo (lino + otros artículos + resto)": d["capex"] - (d["lino"] + d["oart"] + d["otro"]),
            "R10 capex neto APM − (capex bruto EFE − cesiones − subvenciones)": d["capnet"] - (d["capex"] - d["ces"] - d["subv_capex"]),
            "R11 FCF publicado − suma de sus componentes": d["fcf_apm"] - (d["fcf_antes"] - d["capnet"] - d["bfr"] - d["int"] - d["imppag"] - d["leasepay"]),
            "R12 FCF publicado − (CFO − capex neto − intereses − pagos de arrendamientos)": d["fcf_apm"] - (d["cfo"] - d["capnet"] - d["int"] - d["leasepay"]),
            "R13 interés implícito de caja (pagos − principal) − gasto devengado": (d["leasepay"] - d["ls_princ"]) - d["int_ls_dev"],
            "R14 pasivo por arrendamiento: final − (inicial + altas − principal + divisa + otros)": d["pas_fin"] - (d["pas_ini"] + d["ls_comb_pas"] + d["ls_nuevo_pas"] + d["ls_reest_pas"] - d["ls_princ"] + d["ls_fx_pas"] + d["ls_otros_pas"]),
            "R15 activo ROU: final − (inicial + altas − amortización − deterioro + divisa + otros)": d["rou_fin"] - (d["rou_ini"] + d["ls_comb"] + d["ls_nuevo"] + d["ls_reest"] - d["ls_amort"] - d["ls_deter"] + d["ls_fx_rou"] + d["ls_otros_rou"]),
            "R16 amortización ROU (nota 4.5) − amortización del movimiento de ROU": d["da_rou"] - d["ls_amort"],
            "R17 impuesto corriente + diferido − gasto por impuesto": d["tax_corr"] + d["tax_dif"] - d["imp"],
            "R18 SBC no monetario + cargas sociales − gasto IFRS 2 total": d["sbc"] + d["sbcsoc"] - d["sbc_ifrs2"],
            "R19 deuda bruta − caja − deuda neta": d["deu_bruta"] - d["deu_caja"] - d["deu_neta"],
            "R20 resultado financiero: cuenta de resultados − total de la nota de resultado financiero": d["fin"] - d["fin_nota"],
            "R21 resultado antes de impuestos: cuenta de resultados − conciliación del impuesto": d["bai"] - d["tax_bai"],
            "R22 amortización PPA: cuenta de resultados − nota de D&A": d["is_ppa"] - d["da_ppa"],
            "R23 ventas: cuenta de resultados − información por segmentos (total)": d["ventas"] - d["ventas_seg"],
            "R29 flujos de inversión: total − suma de sus líneas": d["invtot"] - (-d["capint"] + d["desint"] - d["capmat"] + d["desmat"] - d["adq"]
                                                                                  + d["cesfil"] + d["prest"] + d["divrec"] + d["subvinv"]),
            "R30 flujos de financiación: total − suma de sus líneas": d["fintot"] - (d["ampl"] + d["autoc"] + d["div"] + d["empr"] + d["reemb"]
                                                                                     - d["leasepay"] - d["int"] + d["ofin"]),
            "R31 capex neto: tabla de capex − tabla de free cash flow": d["capnet_tabla"] - d["capnet"],
            "R32 crecimiento publicado − (orgánico + externo + divisa)": d["crec_pub"] - (d["crec_org"] + d["crec_ext"] + d["crec_fx"]),
            "R33 resultado neto: cuenta de resultados − estado de flujos": d["bn"] - d["cf_bn"],
            "R37 impuesto: conciliación del tipo − cuenta de resultados": d["tax_real"] - d["imp"],
        } | ({"R38 otros ingresos y gastos operativos: nota − cuenta de resultados": d["ooie_tot"] - d["is_ooie"]} if "ooie_tot" in d else {}) | ({"R24 adquisiciones: EFE − puente de la deuda neta": d["adq"] - d["dn_adq"]} if "dn_adq" in d else {}) \
          | ({"R26 activo ROU: apertura de 2024 (URD 2025) − cierre de 2023 (DEU 2024)": d["rou_ini"] - d["rou_cierre_ed_ant"],
              "R27 pasivo por arrendamiento: apertura de 2024 (URD 2025) − cierre de 2023 (DEU 2024)": d["pas_ini"] - d["pas_cierre_ed_ant"],
              "R28 relaciones con clientes: apertura de 2024 (URD 2025) − cierre de 2023 (DEU 2024)": d["rc_apertura"] - d["rc_cierre_ed_ant"]}
             if "rou_cierre_ed_ant" in d else {})

    def residuos_horizonte(d):
        """(Revisión n.º 3, N2) Identidades de 2021 y 2022, años que solo entran en el ancla de S2C (C53)."""
        return {
            "R25 D&A total − suma de componentes (incluidos deterioro y PPA)": d["da_total"] - (d["da_text"] + d["da_oart"] + d["da_otro"] + d["da_rou"]
                                                                                              - d["da_subv"] + d["da_deter"] + d["da_ppa"]),
            "R16 amortización ROU (nota de D&A) − amortización del movimiento de ROU": d["da_rou"] - d["ls_amort"],
            "R22 amortización PPA: cuenta de resultados − nota de D&A": d["is_ppa"] - d["da_ppa"],
            "R34 capex bruto del EFE − capex por tipo (lino + otros artículos + resto)": d["capex"] - (d["lino"] + d["oart"] + d["otro"]),
            "R35 EBIT publicado − (BAI + resultado financiero)": d["ebit_pub"] - (d["bai"] + d["fin"]),
            "R36 FCF publicado − (CFO − capex neto − intereses con arrendamientos − principal)": d["fcf_apm"] - (d["cfo"] - d["capnet_tabla"]
                                                                                                             - d["int_con_ls"] - d["ls_princ"]),
            # circulante: las líneas del EFE (que entran en el ancla de S2C) frente al circulante del APM de otra página
            "R5 circulante APM − circulante de las líneas del EFE": d["bfr"] - d["dwc"],
            # (C9) entradas del ancla de S2C que solo se cotejaban con la Historia del libro
            "R17 impuesto corriente + diferido − gasto por impuesto": d["tax_corr"] + d["tax_dif"] - d["imp"],
            "R39 adquisiciones: EFE − flujo neto total de la nota de combinaciones de negocio": d["adq"] - d["adq_nota"],
        } | ({"R32 crecimiento publicado − (orgánico + externo + divisa)": d["crec_pub"] - (d["crec_org"] + d["crec_ext"] + d["crec_fx"])}
             if "crec_pub" in d else {}) \
          | ({"R40 ventas 2020 (base de S2C): cuenta de resultados − informe de gestión": d["ventas_2020"] - d["ventas_2020_mr"]}
             if "ventas_2020" in d else {})

    conc = {y: residuos(A[y]) for y in VENTANA}
    R["tablas"]["conciliaciones_residuos"] = {str(y): {k: f6(v, 3) for k, v in conc[y].items()} for y in VENTANA}
    # (O3; contraste externo sobre 6fb9294) Cada identidad se AFIRMA con su propia cota de redondeo: la suma, para cada
    # cifra impresa que interviene, de |coeficiente| × media unidad de su última cifra (0,05 en millones con un decimal).
    # Es el error máximo que puede producir el redondeo de las cifras publicadas; un residuo mayor es un dato erróneo o una
    # diferencia de concepto. No hay tolerancia global. La única excepción es una diferencia de concepto fijada en su
    # valor exacto: se exige |residuo − valor fijado| ≤ cota, así que un error nuevo en sus cifras la hace fallar.
    FQ = FuenteQ(F)
    AQ = {y: datos_anio(FQ, y) for y in HORIZONTE}
    concQ = {y: (residuos(AQ[y]) if y in VENTANA else residuos_horizonte(AQ[y])) for y in HORIZONTE}
    EXCEPCIONES = {
        (2025, "R13"): (Fr("0.4"), "diferencia de concepto 2025: interés implícito de caja 29,6 (pagos 177,9 del EFE p.327 "
                                   "− principal 148,3 de la nota 6.3 p.366) frente al gasto devengado 29,2 (nota 9 p.379); "
                                   "la fuente no publica el puente; en 2023 y 2024 la diferencia es 0,0"),
    }
    res_det, codigo_q = {}, {}
    for y in HORIZONTE:
        res_det[str(y)] = {}
        for k, q in concQ[y].items():
            cod = k.split(" ")[0]
            codigo_q[(y, cod)] = q
            assert y not in VENTANA or q.v == conc[y][k], k
            cota = sum(abs(c) * F.epsilon(i) for i, c in q.t.items())
            paginas = sorted({(F.meta[i]["doc"], F.meta[i]["pagina"]) for i in q.t})
            excep = (y, cod) in EXCEPCIONES
            esperado, nota = EXCEPCIONES.get((y, cod), (Fr(0), f"redondeo de {len(q.t)} cifras impresas"))
            ok = check(f"residuo {cod} {y} dentro de su cota de redondeo" + (" (diferencia de concepto fijada)" if excep else ""),
                       q.v, esperado, cota, nota, clase="fuente")
            res_det[str(y)][cod] = {"identidad": k, "residuo": f6(q.v, 3), "cota_de_redondeo": f6(cota, 3), "cifras": len(q.t),
                                    "paginas": [f"{dd} p.{pp}" for dd, pp in paginas],
                                    "contraste": "misma página" if len(paginas) == 1 else "entre páginas",
                                    "valor_fijado": f6(esperado, 3) if excep else None, "ok": ok}
    R["tablas"]["residuos_con_cota"] = res_det

    # ======================= A. FCF base por dos vías y Análisis C46–C52
    fcfb = {}
    for y in VENTANA:
        d = A[y]
        int_ls_caja = d["leasepay"] - d["ls_princ"]
        fcfb[y] = {"CFO": d["cfo"], "capex_neto": d["capnet"], "int_fin": d["int"], "int_arr_caja": int_ls_caja,
                   "principal_arr": d["ls_princ"], "sbc": d["sbc"],
                   "fcf_base_via_cfo": d["cfo"] - d["capnet"] - d["int"] - int_ls_caja - d["ls_princ"] - d["sbc"],
                   "fcf_base_via_apm": d["fcf_apm"] - d["sbc"]}
    C46, C47 = avg(lambda d: d["cfo"]), avg(lambda d: d["capnet"])
    C48 = avg(lambda d: d["int"]) + avg(lambda d: d["leasepay"] - d["ls_princ"])
    C49, C50 = avg(lambda d: d["ls_princ"]), avg(lambda d: d["sbc"])
    C52 = C46 - C47 - C48 - C49 - C50
    C52_apm = avg(lambda d: d["fcf_apm"] - d["sbc"])
    C48_devengo = avg(lambda d: d["int"]) + avg(lambda d: d["int_ls_dev"])
    R["tablas"]["fcf_base"] = {"por_anio": {str(y): {k: f6(v, 3) for k, v in fcfb[y].items()} for y in VENTANA},
                               "C46": f6(C46), "C47": f6(C47), "C48": f6(C48), "C48_int_fin": f6(avg(lambda d: d["int"])),
                               "C48_int_arr_caja": f6(avg(lambda d: d["leasepay"] - d["ls_princ"])), "C49": f6(C49), "C50": f6(C50),
                               "C52_via_cfo": f6(C52), "C52_via_fcf_publicado": f6(C52_apm),
                               "variante_no_adoptada_C48_con_interes_devengado": f6(C48_devengo),
                               "variante_no_adoptada_C48_sin_interes_arr": f6(avg(lambda d: d["int"]))}
    check("C52 vía CFO = vía FCF publicado − SBC", C52, C52_apm, clase="fuente")
    if L:
        for celda, val in [("Análisis!C46", C46), ("Análisis!C47", C47), ("Análisis!C48", C48), ("Análisis!C49", C49),
                           ("Análisis!C50", C50), ("Análisis!C52", C52)]:
            check(f"{celda} libro = fuente (exacto a 3 decimales registrados)", val, Fr(str(L[celda])), Fr(1, 1000))

    # ======================= A. Historia frente a la fuente
    hist = {}
    for y in HORIZONTE:
        d = A[y]
        filas = {6: d["ventas"], 7: d["ebit_h"], 8: d["da_total"], 10: d["tau"], 11: d["cfo"], 12: d["capex"], 13: d["adq"], 14: d["dwc"],
                 17: d["ls_princ"], 18: d.get("sbc_nota52", d["sbc"])}
        filas[15] = d["int"] if y in VENTANA else d["int_con_ls"]
        if y in VENTANA:
            filas[22], filas[23], filas[24] = d["deu_bruta"], d["pas_fin"], d["deu_caja"]
        hist[y] = filas
        if L:
            for fila, val in filas.items():
                celda = f"Historia!{COL[y]}{fila}"
                if celda in L:
                    check(f"{celda} ({y}) libro = fuente", val, Fr(str(L[celda])), Fr(0))
    if L:
        check("Historia!G6 (2020) libro = fuente", S2020, Fr(str(L["Historia!G6"])))

    # ======================= C. f: definición de la plantilla y descomposición económica
    S_avg = avg(lambda d: d["ventas"])
    nopat = {y: A[y]["ebit_h"] * (1 - A[y]["tau"]) for y in VENTANA}
    reinv = {y: A[y]["capex"] - A[y]["da_total"] + A[y]["dwc"] for y in VENTANA}
    NOPAT_avg, REINV_avg = sum(nopat.values()) / 3, sum(reinv.values()) / 3
    FS = NOPAT_avg - REINV_avg - C52
    f = FS / S_avg
    # El libro registra C46, C47 y C50 con 3 decimales (convención «redondeo: 3» del registro), no la media exacta.
    r3_ = lambda x: Fr(round(x, 3)).limit_denominator(1000)  # noqa: E731
    C52_libro = r3_(C46) - r3_(C47) - C48 - C49 - r3_(C50)
    FS_libro = NOPAT_avg - REINV_avg - C52_libro
    f_libro = FS_libro / S_avg
    R["tablas"]["redondeo_entradas"] = {"C46_exacto": f6(C46, 9), "C46_registrado": f6(r3_(C46), 3), "C47_exacto": f6(C47, 9),
                                        "C47_registrado": f6(r3_(C47), 3), "C50_exacto": f6(C50, 9), "C50_registrado": f6(r3_(C50), 3),
                                        "C52_exacto": f6(C52, 9), "C52_registrado": f6(C52_libro, 6), "f_exacta": f6(f, 15), "f_registrada": f6(f_libro, 15),
                                        "efecto_en_f": f6(f - f_libro, 15), "efecto_en_fugas_mm": f6(FS - FS_libro, 9)}
    comp = {}
    for y in VENTANA:
        d = A[y]
        ebit_cf = d["cf_bn"] + d["cf_imp"] + d["cf_fin"]
        r3 = d["cf_antes"] - (ebit_cf + d["sbc"] + d["dap"] + d["cf_subv"] + d["plusv"] + d["earn"])
        r4 = d["cfo"] - (d["cf_antes"] - d["dwc"] - d["imppag"])
        c = {
            "pagos_arrendamientos_principal": d["ls_princ"],
            "pagos_arrendamientos_interes_caja": d["leasepay"] - d["ls_princ"],
            "intereses_financieros_netos_pagados": d["int"],
            "impuesto: escudo del gasto financiero (−τ·financiero)": -d["tau"] * d["fin"],
            "impuesto: caja − devengo (pagado − gasto)": d["imppag"] - d["imp"],
            "impuesto: redondeo de τ a 4 decimales (gasto − τ·BAI)": d["imp"] - d["tau"] * d["bai"],
            "capex neto − bruto (cesiones, subvenciones)": d["capnet"] - d["capex"],
            "plusvalías por enajenación (no monetarias en EBIT)": -d["plusv"],
            "earnout y otros no monetarios": -d["earn"],
            "provisiones (D&A total − línea de amortizaciones y provisiones − subvención)": d["da_total"] - d["dap"] - d["cf_subv"],
            "EBIT de la Historia − EBIT del EFE": d["ebit_h"] - ebit_cf,
            "residuos de redondeo del EFE publicado (−R3 − R4)": -r3 - r4,
        }
        comp[y] = c
        fs_y = nopat[y] - reinv[y] - fcfb[y]["fcf_base_via_cfo"]
        check(f"descomposición económica de f·ventas {y} = definición de la plantilla", sum(c.values()), fs_y, clase="algebraica")
    comp_avg = {k: sum(comp[y][k] for y in VENTANA) / 3 for k in comp[2025]}
    check("descomposición media de f·ventas = C79", sum(comp_avg.values()), FS, clase="algebraica")
    R["tablas"]["f"] = {"ventas_medias": f6(S_avg), "nopat_medio": f6(NOPAT_avg), "reinversion_media": f6(REINV_avg),
                        "flujo_implicito": f6(NOPAT_avg - REINV_avg), "fcf_base": f6(C52), "fugas_mm": f6(FS), "f": f6(f, 12),
                        "componentes_por_anio": {str(y): {k: f6(v, 3) for k, v in comp[y].items()} for y in VENTANA},
                        "componentes_media": {k: f6(v, 3) for k, v in comp_avg.items()}}
    if L:
        for celda, val, tol in [("Historia!C74", S_avg, Fr(1, 10 ** 9)), ("Historia!C75", NOPAT_avg, Fr(1, 10 ** 9)),
                                ("Historia!C76", REINV_avg, Fr(1, 10 ** 9)), ("Historia!C70", C52_libro, Fr(1, 10 ** 9)),
                                ("Historia!C79", FS_libro, Fr(1, 10 ** 9)), ("Historia!C58", f_libro, Fr(1, 10 ** 12))]:
            check(f"{celda} libro = cálculo independiente", val, Fr(L[celda]), tol)

    # ======================= D. motor A desde la convención
    tau5 = sum(A[y]["tau"] for y in HORIZONTE) / 5
    V0, m0 = A[2025]["ventas"], A[2025]["ebit_h"] / A[2025]["ventas"]
    escenarios, tasas, caja = {}, {}, {}
    if L:
        check("Historia!C52 (τ 5 años) libro = fuente", tau5, Fr(str(L["Historia!C52"])), Fr(1, 10 ** 12))
        for fila, nombre, col in [(6, "MALO", "B"), (7, "NORMAL", "C"), (8, "BUENO", "D")]:
            p = {k: Fr(str(L[f"{hoja}!{col}{n}"])) for k, hoja, n in [("g15", "Palancas", 14), ("m_obj", "Palancas", 15),
                                                                          ("s2c", "Palancas", 16), ("roic", "Palancas", 18), ("g_inf", "Análisis", 68)]}
            mo = motor_a(V0, m0, tau5, f_libro, **p)
            escenarios[nombre] = (p, mo)
            cols = ["AU", "AV", "AW", "AX", "AY", "AZ", "BA", "BB", "BC", "BD"]
            for t, c in enumerate(cols):
                check(f"Motor!{c}{fila} flujo año {t+1} {nombre}: réplica = libro", mo["flujos"][t], Fr(L[f"Motor!{c}{fila}"]), Fr(1, 10 ** 9))
            check(f"Motor!BF{fila} flujo año 11 {nombre}: réplica = libro", mo["flujo_11"], Fr(L[f"Motor!BF{fila}"]), Fr(1, 10 ** 9))
            r_ = Fr(str(L[f"Motor!J{fila}"]))
            M_ = Fr(str(L[f"Motor!M{fila}"]))
            # (O15) Motor!BL = C·(D·(1−K) − L)/J + M: el exceso de caja M se resta ANTES de multiplicar por r
            check(f"(Motor!BL{fila} − Motor!M{fila})·r = flujo sin crecimiento {nombre}", mo["flujo_sin_crecimiento"],
                  (Fr(L[f"Motor!BL{fila}"]) - M_) * r_, Fr(1, 10 ** 8))
            check(f"Motor!M{fila} (exceso de caja del motor A) = Análisis!C76", M_, Fr(str(L["Análisis!C76"])))
            tasas[nombre], caja[nombre] = r_, M_
    F0 = V0 * (m0 * (1 - tau5) - f_libro)
    # (O15) Exceso de caja distinto de cero. Fórmula de Motor!BL (leída del libro): BL = C·(D·(1−K) − L)/J + M, con
    # M = Análisis!C76 en el motor A. La identidad corregida (BL − M)·r recupera F0 con cualquier M; la anterior,
    # BL·r − M, se desvía en M·(r − 1) y solo acierta con M = 0, que es el caso del libro.
    caja_no_nula = {}
    if tasas:
        r_n = tasas["NORMAL"]
        for X in (Fr(0), Fr(250), Fr(-80)):
            BL_X = F0 / r_n + X
            caja_no_nula[str(X)] = {"BL": f6(BL_X, 9), "(BL − M)·r": f6((BL_X - X) * r_n, 9), "BL·r − M (anterior)": f6(BL_X * r_n - X, 9)}
            check(f"exceso de caja {X}: (BL − M)·r = flujo sin crecimiento (fórmula de Motor!BL)", (BL_X - X) * r_n, F0, clase="algebraica")
            if X:
                check(f"exceso de caja {X}: la identidad anterior se desvía en M·(r − 1) (control negativo)", BL_X * r_n - X - F0,
                      X * (r_n - 1), clase="algebraica", nota="distinto de cero: la identidad anterior fallaría")
    if a.caja_no_nula:
        cn = json.loads(a.caja_no_nula.read_text(encoding="utf-8"))
        if cn.get("libro_sha256") != SHA_LIBRO:
            sys.exit("la prueba de caja no nula no se hizo sobre una copia del libro de referencia")
        for X, filas in cn["resultados"].items():
            for fila, nombre in [("6", "MALO"), ("7", "NORMAL"), ("8", "BUENO")]:
                v = filas[fila]
                check(f"copia recalculada, exceso de caja {X}: Motor!M{fila} = Análisis!C76", Fr(str(v["M"])), Fr(X),
                      Fr(1, 10 ** 9), nota="LibreOffice sobre copia temporal", clase="libro")
                check(f"copia recalculada, exceso de caja {X}: (Motor!BL{fila} − M)·r = flujo sin crecimiento {nombre}",
                      (Fr(str(v["BL"])) - Fr(str(v["M"]))) * Fr(str(v["J"])), F0, Fr(1, 10 ** 8),
                      nota="LibreOffice sobre copia temporal", clase="libro")
    R["tablas"]["exceso_de_caja_no_nulo"] = caja_no_nula

    # ======================= E. puentes
    EBIT_avg = avg(lambda d: d["ebit_h"])
    puente0 = {
        "FCF base (C52 registrado)": C52_libro,
        "+ nivel del EBIT 2025 frente a la media 2023–25, al τ de 5 años": (A[2025]["ebit_h"] - EBIT_avg) * (1 - tau5),
        "+ cambio de tipo: τ de 5 años frente a τ de cada año en la ventana": EBIT_avg * (1 - tau5) - NOPAT_avg,
        "− f aplicada a las ventas 2025 frente a las ventas medias": -f_libro * (V0 - S_avg),
        "+ reinversión histórica media que el motor no proyecta (C76)": REINV_avg,
    }
    puente0["= flujo sin crecimiento del motor (V0·[m0(1−τ) − f])"] = sum(puente0.values())
    check("puente FCF base → flujo sin crecimiento", puente0["= flujo sin crecimiento del motor (V0·[m0(1−τ) − f])"], F0, clase="algebraica")
    dR = {y: A[y]["da_rou"] for y in VENTANA}
    dP = {y: A[y]["da_ppa"] for y in VENTANA}
    reinv_desc = {
        "lino: compras − amortización": avg(lambda d: d["lino"] - d["da_text"]),
        "otros artículos en alquiler: compras − amortización": avg(lambda d: d["oart"] - d["da_oart"]),
        "resto de inmovilizado e intangibles: compras − amortización": avg(lambda d: d["otro"] - d["da_otro"]),
        "subvenciones imputadas (+) y deterioros (−)": avg(lambda d: d["da_subv"] - d["da_deter"]),
        "residuo de redondeo (capex EFE − por tipo; D&A total − componentes)": avg(lambda d: (d["capex"] - d["lino"] - d["oart"] - d["otro"]) - (d["da_total"] - d["da_text"] - d["da_oart"] - d["da_otro"] + d["da_subv"] - d["da_deter"] - d["da_rou"] - d["da_ppa"])),
        "circulante": avg(lambda d: d["dwc"]),
        "− amortización de derechos de uso NIIF 16": -sum(dR.values()) / 3,
        "− amortización de intangibles de combinaciones (PPA)": -sum(dP.values()) / 3,
    }
    check("descomposición de la reinversión media = C76", sum(reinv_desc.values()), REINV_avg, clase="algebraica")
    puente1 = {}
    for nombre, (p, mo) in escenarios.items():
        V1 = mo["V"][0]
        m1 = m0 + (p["m_obj"] - m0) / 5
        puente1[nombre] = {
            "flujo sin crecimiento": F0,
            "+ NOPAT adicional por ventas y margen del año 1": V1 * m1 * (1 - tau5) - V0 * m0 * (1 - tau5),
            "− f sobre el aumento de ventas": -f_libro * (V1 - V0),
            "− reinversión de crecimiento ΔV/S2C": -(V1 - V0) / p["s2c"],
        }
        puente1[nombre]["= flujo del año 1"] = sum(puente1[nombre].values())
        check(f"puente flujo sin crecimiento → año 1 {nombre}", puente1[nombre]["= flujo del año 1"], mo["flujos"][0], clase="algebraica")
    R["tablas"]["puentes"] = {"fcf_base_a_flujo_sin_crecimiento": {k: f6(v, 3) for k, v in puente0.items()},
                              "reinversion_media_descompuesta": {k: f6(v, 3) for k, v in reinv_desc.items()},
                              "flujo_sin_crecimiento_a_anio_1": {n: {k: f6(v, 3) for k, v in pp.items()} for n, pp in puente1.items()},
                              "palancas": {n: {k: f6(v, 6) for k, v in p.items()} for n, (p, _) in escenarios.items()},
                              "V0": f6(V0), "m0": f6(m0, 9), "tau_5_anios": f6(tau5, 6), "f_registrada": f6(f_libro, 12), "f_exacta": f6(f, 12)}

    # ======================= F. arrendamientos
    ls = {}
    for y in VENTANA:
        d = A[y]
        ls[str(y)] = {"pagos_totales_caja": d["leasepay"], "principal": d["ls_princ"], "interes_implicito_caja": d["leasepay"] - d["ls_princ"],
                      "interes_devengado_nota_8_2": d["int_ls_dev"], "diferencia_caja_devengo": d["leasepay"] - d["ls_princ"] - d["int_ls_dev"],
                      "amortizacion_ROU": d["da_rou"], "altas_no_monetarias_ROU (nuevas + reestimaciones + combinaciones)": d["ls_nuevo"] + d["ls_reest"] + d["ls_comb"],
                      "pasivo_final": d["pas_fin"], "variacion_pasivo": d["pas_fin"] - d["pas_ini"],
                      "amortizacion_ROU_sobre_ventas_%": 100 * d["da_rou"] / d["ventas"], "pagos_sobre_ventas_%": 100 * d["leasepay"] / d["ventas"]}
    R["tablas"]["arrendamientos"] = {y: {k: f6(v, 3) for k, v in t_.items()} for y, t_ in ls.items()}
    for y in (2021, 2022):
        d = A[y]
        R["tablas"]["arrendamientos"][str(y)] = {"principal": f6(d["ls_princ"], 3), "interes_devengado_nota_8_2": f6(d["int_ls_dev"], 3),
                                                 "intereses_pagados_incluidos_arrendamientos (presentación antigua)": f6(d["int_con_ls"], 3),
                                                 "amortizacion_ROU": f6(d["da_rou"], 3)}
    dR_avg, dP_avg = sum(dR.values()) / 3, sum(dP.values()) / 3
    P_avg = avg(lambda d: d["leasepay"])
    ubicacion = {
        "calibración: amortización ROU dentro del EBIT (NOPAT)": -dR_avg,
        "calibración: amortización ROU devuelta por la reinversión (− D&A total)": dR_avg,
        "calibración: pagos de arrendamiento dentro del FCF base (C48 + C49)": -P_avg,
        "calibración: coste neto de arrendamiento reconocido en la historia": -P_avg,
        "proyección (base 2025): amortización ROU dentro de m0": -A[2025]["da_rou"],
        "proyección (base 2025): pagos de arrendamiento dentro de f·V0": -P_avg / S_avg * V0,
        "proyección: devolución de la amortización ROU por la reinversión": Fr(0),
        "proyección (base 2025): coste de arrendamiento total cargado": -A[2025]["da_rou"] - P_avg / S_avg * V0,
    }
    R["tablas"]["arrendamientos_ubicacion"] = {k: f6(v, 3) for k, v in ubicacion.items()}
    # (O17) exceso exacto en la base 2025 = amortización ROU media escalada (antes de impuestos; el impuesto real ya está en f)
    R["tablas"]["arrendamientos_exceso_exacto_base_2025"] = f6(dR_avg / S_avg * V0, 3)
    # (O10) tendencia: pagos y amortización ROU crecen más deprisa que las ventas
    R["tablas"]["arrendamientos_tendencia"] = {
        "pagos_medios_escalados_a_2025 (f)": f6(P_avg / S_avg * V0, 3), "pagos_2025": f6(A[2025]["leasepay"], 3),
        "diferencia_pagos_2025_menos_escalados": f6(A[2025]["leasepay"] - P_avg / S_avg * V0, 3),
        "amortizacion_ROU_2025_en_m0": f6(A[2025]["da_rou"], 3), "amortizacion_ROU_media_escalada_devuelta_en_A1_A2": f6(dR_avg / S_avg * V0, 3),
        "ROU_2025_no_devuelta_en_A1_A2": f6(A[2025]["da_rou"] - dR_avg / S_avg * V0, 3)}

    # ======================= G. alternativas de perímetro (consecuencias, no propuestas adoptadas)
    defs = {
        "A0 V6.3 actual: reinversión necesaria = D&A total": lambda d: d["da_total"],
        "A1 sin derechos de uso: D&A total − ROU": lambda d: d["da_total"] - d["da_rou"],
        "A2 perímetro propio: D&A total − ROU − PPA": lambda d: d["d_own"],
        "B cota: toda la inversión propia es reposición (= capex bruto)": lambda d: d["capex"],
    }
    ventas = {y: A[y]["ventas"] for y in HORIZONTE}
    ventas[2020] = S2020
    alt = {}
    for nombre, DX in defs.items():
        reinv_x = avg(lambda d: d["capex"] - DX(d) + d["dwc"])
        fs_x = NOPAT_avg - reinv_x - C52_libro
        f_x = fs_x / S_avg
        F0_x = V0 * (m0 * (1 - tau5) - f_x)
        den_tot = sum(A[y]["capex"] - DX(A[y]) + A[y]["dwc"] + A[y]["adq"] for y in HORIZONTE)
        dS_org = {y: A[y]["crec_org"] / 100 * ventas[y - 1] for y in HORIZONTE}
        den_org_v = sum(A[y]["capex"] - DX(A[y]) + A[y]["dwc"] for y in VENTANA)
        den_org_h = sum(A[y]["capex"] - DX(A[y]) + A[y]["dwc"] for y in HORIZONTE)
        alt[nombre] = {
            "reinversion_necesaria_media_2023_25": f6(avg(DX), 3),
            "inversion_neta_de_crecimiento_media (capex − necesaria + circulante)": f6(reinv_x, 3),
            "fugas_f_por_ventas_mm": f6(fs_x, 3), "f": f6(f_x, 9),
            "flujo_sin_crecimiento_base_2025": f6(F0_x, 3), "diferencia_frente_a_A0": f6(F0_x - F0, 3),
            "reinversion_necesaria_implicita_en_proyeccion_base_2025": f6(avg(DX) / S_avg * V0, 3),
            "necesaria_menos_capex_medio_2023_25": f6(avg(DX) - avg(lambda d: d["capex"]), 3),
            "S2C_total_2021_25 (ΔV 2020→2025 ÷ Σ reinversión + adquisiciones)": f6((ventas[2025] - S2020) / den_tot, 4) if den_tot > 0 else None,
            "S2C_organico_2023_25 (Σ crecimiento orgánico ÷ Σ inversión neta propia)": f6(sum(dS_org[y] for y in VENTANA) / den_org_v, 4) if den_org_v > 0 else None,
            "S2C_organico_2021_25": f6(sum(dS_org.values()) / den_org_h, 4) if den_org_h > 0 else None,
        }
    # A1′: arrendamientos como deuda renovada (principal refinanciado con nuevos contratos): mantiene la D&A total en la
    # reinversión y quita el principal del FCF base. Cambia una entrada registrada (C49): solo como contraste.
    fs_a1p = NOPAT_avg - REINV_avg - (C52_libro + C49)
    f_a1p = fs_a1p / S_avg
    alt["A1′ arrendamientos como deuda renovada: D&A total y FCF base sin principal (cambia C49)"] = {
        "reinversion_necesaria_media_2023_25": f6(avg(lambda d: d["da_total"]), 3),
        "inversion_neta_de_crecimiento_media (capex − necesaria + circulante)": f6(REINV_avg, 3),
        "fugas_f_por_ventas_mm": f6(fs_a1p, 3), "f": f6(f_a1p, 9),
        "flujo_sin_crecimiento_base_2025": f6(V0 * (m0 * (1 - tau5) - f_a1p), 3),
        "diferencia_frente_a_A0": f6(V0 * (m0 * (1 - tau5) - f_a1p) - F0, 3),
        "reinversion_necesaria_implicita_en_proyeccion_base_2025": f6(avg(lambda d: d["da_total"]) / S_avg * V0, 3),
        "necesaria_menos_capex_medio_2023_25": f6(avg(lambda d: d["da_total"]) - avg(lambda d: d["capex"]), 3),
        "S2C_total_2021_25 (ΔV 2020→2025 ÷ Σ reinversión + adquisiciones)": None,
        "S2C_organico_2023_25 (Σ crecimiento orgánico ÷ Σ inversión neta propia)": None, "S2C_organico_2021_25": None}
    # Convención de financiación de f (fuera de F1): intereses proporcionales a las ventas sin endeudamiento nuevo.
    conv = {}
    for nombre, (p, mo) in escenarios.items():
        dV1 = mo["V"][0] - V0
        conv[nombre] = {"aumento_de_ventas_año_1": dV1,
                        "intereses_adicionales_en_f_año_1": avg(lambda d: d["int"]) / S_avg * dV1,
                        "endeudamiento_neto_omitido_si_deuda_neta/ventas_constante": A[2025]["deu_neta"] / V0 * dV1}
    R["tablas"]["convencion_financiacion"] = {n: {k: f6(v, 3) for k, v in c.items()} for n, c in conv.items()}
    if L:
        check("S2C total A0 = Historia!C53", Fr(alt["A0 V6.3 actual: reinversión necesaria = D&A total"]["S2C_total_2021_25 (ΔV 2020→2025 ÷ Σ reinversión + adquisiciones)"]).limit_denominator(10 ** 4),
              Fr(L["Historia!C53"]), Fr(1, 10 ** 4))
    R["tablas"]["alternativas"] = alt
    # (O4) Con la palanca S2C anclada en el C53 de cada perímetro, el exceso de los años 1–10 decrece con el crecimiento.
    s2c_ancla = {}
    for nombre, DX in defs.items():
        den = sum(A[y]["capex"] - DX(A[y]) + A[y]["dwc"] + A[y]["adq"] for y in HORIZONTE)
        s2c_ancla[nombre.split(" ")[0]] = (ventas[2025] - S2020) / den if den > 0 else None
    f_por = {nombre.split(" ")[0]: (NOPAT_avg - avg(lambda d, DX=DX: d["capex"] - DX(d) + d["dwc"]) - C52_libro) / S_avg for nombre, DX in defs.items()}
    o4 = {}
    if "NORMAL" in escenarios:
        pN = escenarios["NORMAL"][0]
        V1 = V0 * (1 + pN["g15"])
        m1 = m0 + (pN["m_obj"] - m0) / 5
        for k in ("A0", "A1", "A2"):
            o4[k] = {"S2C_ancla_C53": s2c_ancla[k], "f": f_por[k],
                     "flujo_sin_crecimiento": V0 * (m0 * (1 - tau5) - f_por[k]),
                     "flujo_año_1_NORMAL_con_S2C_ancla": V1 * (m1 * (1 - tau5) - f_por[k]) - (V1 - V0) / s2c_ancla[k]}
        for k in ("A1", "A2"):
            df_ = f_por["A0"] - f_por[k]
            dinv = 1 / s2c_ancla[k] - 1 / s2c_ancla["A0"]
            o4[k]["brecha_frente_a_A0_sin_crecimiento"] = o4[k]["flujo_sin_crecimiento"] - o4["A0"]["flujo_sin_crecimiento"]
            o4[k]["brecha_frente_a_A0_año_1"] = o4[k]["flujo_año_1_NORMAL_con_S2C_ancla"] - o4["A0"]["flujo_año_1_NORMAL_con_S2C_ancla"]
            o4[k]["aumento_de_ventas_que_anula_la_brecha"] = V0 * df_ / (dinv - df_)
    R["tablas"]["S2C_anclada_en_C53"] = {k: {kk: f6(vv, 4) for kk, vv in v.items()} for k, v in o4.items()}
    # (O9) Partidas puntuales de la ventana dentro del flujo sin crecimiento (comunes a todos los perímetros)
    earn_f = -comp_avg["earnout y otros no monetarios"] / S_avg * V0          # su presencia baja f → sube el flujo
    plusv_f = -comp_avg["plusvalías por enajenación (no monetarias en EBIT)"] / S_avg * V0
    plusv_m0 = A[2025]["ooie_plusv"] * (1 - tau5)
    R["tablas"]["partidas_puntuales_en_flujo_sin_crecimiento"] = {
        "earnout y otros no monetarios dentro de f": f6(earn_f, 3),
        "plusvalías netas de la ventana dentro de f": f6(plusv_f, 3),
        "resultado por bajas de inmovilizado 2025 (+25,7 en OOIE) dentro de m0, después de τ": f6(plusv_m0, 3),
        "efecto neto común a todos los perímetros": f6(earn_f + plusv_f + plusv_m0, 3)}
    # (O13) Prueba de implementación de A3_estimado con estimaciones SINTÉTICAS de la reinversión necesaria D_X.
    # No son datos de Elis ni estimaciones propuestas: solo comprueban que la fórmula se aplica bien.
    def f_y_F0(DX):
        f_x = (NOPAT_avg - avg(lambda d: d["capex"] - DX(d) + d["dwc"]) - C52_libro) / S_avg
        return f_x, V0 * (m0 * (1 - tau5) - f_x)
    fB_, F0B_ = f_y_F0(lambda d: d["capex"])
    fA2_, F0A2_ = f_y_F0(lambda d: d["d_own"])
    f3m, F03m = f_y_F0(lambda d: (d["capex"] + d["d_own"]) / 2)
    check("A3 sintético con D_X = capex propio: f de la cota B", fB_, f_por["B"], clase="algebraica")
    check("A3 sintético con D_X = D&A propia: f de A2", fA2_, f_por["A2"], clase="algebraica")
    check("A3 sintético con D_X = (capex + D&A propia)/2: f en el punto medio de A2 y B", f3m, (fB_ + fA2_) / 2, clase="algebraica")
    check("A3 sintético con D_X = (capex + D&A propia)/2: flujo sin crecimiento en el punto medio", F03m, (F0B_ + F0A2_) / 2, clase="algebraica")
    # (revisión n.º 3, N5) ancla C53 y flujos de los años 1–11 de cada caso sintético, para detectar una implementación que
    # aplique la D_X estimada a f pero no al ancla ni al terminal
    def c53_de(DX):
        den = sum(A[y]["capex"] - DX(A[y]) + A[y]["dwc"] + A[y]["adq"] for y in HORIZONTE)
        return (ventas[2025] - S2020) / den

    a3_ref = {}
    for nombre, DX, f_, F0_ in [("D_X = capex propio (reproduce B)", lambda d: d["capex"], fB_, F0B_),
                                ("D_X = D&A propia (reproduce A2)", lambda d: d["d_own"], fA2_, F0A2_),
                                ("D_X = (capex + D&A propia)/2 (sintético)", lambda d: (d["capex"] + d["d_own"]) / 2, f3m, F03m)]:
        flujos_ = {}
        for esc, (p, _) in escenarios.items():
            mo_x = motor_a(V0, m0, tau5, f_, **p)
            flujos_[esc] = {"anios_1_10": [f6(x, 12) for x in mo_x["flujos"]], "anio_11_terminal": f6(mo_x["flujo_11"], 12)}
        a3_ref[nombre] = {"f": f6(f_, 15), "flujo_sin_crecimiento": f6(F0_, 12), "S2C_C53": f6(c53_de(DX), 12),
                          "flujos_palancas_actuales": flujos_}
    check("A3 sintético, punto medio: C53 entre los de A2 y B", Fr(1) if c53_de(defs["A2 perímetro propio: D&A total − ROU − PPA"]) < c53_de(lambda d: (d["capex"] + d["d_own"]) / 2) < c53_de(lambda d: d["capex"]) else Fr(0),
          Fr(1), clase="algebraica")
    # (O13) Flujos de referencia de los años 1–11 con las palancas actuales para A1 y A2 (contraste de implementación)
    flujos_ref, desvio_11 = {}, {}
    for k in ("A1", "A2"):
        flujos_ref[k] = {}
        for nombre, (p, _) in escenarios.items():
            mo_k = motor_a(V0, m0, tau5, f_por[k], **p)
            flujos_ref[k][nombre] = [f6(x, 12) for x in mo_k["flujos"]] + [f6(mo_k["flujo_11"], 12)]
            # control negativo: una implementación que cambie f en los años 1–10 y no en el terminal no reproduce el año 11
            mo_0 = motor_a(V0, m0, tau5, f_por["A0"], **p)
            parcial_11 = mo_0["flujo_11"]
            check(f"{k} {nombre}: el año 11 de una implementación parcial (f de A0 en el terminal) difiere de la referencia",
                  mo_k["flujo_11"] - parcial_11, mo_k["V"][-1] * (1 + p["g_inf"]) * (f_por["A0"] - f_por[k]), clase="algebraica",
                  nota="diferencia distinta de cero: la referencia del año 11 detecta la implementación parcial")
            desvio_11.setdefault(k, {})[nombre] = f6(mo_k["flujo_11"] - parcial_11, 3)

    # ======================= materialidad
    mat = {
        "amortización ROU media 2023–25": dR_avg, "amortización ROU 2025": A[2025]["da_rou"],
        "amortización PPA media 2023–25": dP_avg, "amortización PPA 2025": A[2025]["da_ppa"],
        "capex bruto − D&A propia media 2023–25": avg(lambda d: d["capex"] - d["d_own"]),
        "capex bruto − D&A propia 2025": A[2025]["capex"] - A[2025]["d_own"],
        "D&A total − capex bruto media 2023–25": avg(lambda d: d["da_total"] - d["capex"]),
    }
    R["tablas"]["materialidad"] = {k: {"mm": f6(v, 3), "%_FCF_base": f6(100 * v / C52_libro, 2),
                                       "%_ventas_del_periodo": f6(100 * v / (V0 if k.endswith("2025") else S_avg), 3)} for k, v in mat.items()}

    # ======================= impuestos y financiación
    imp = {}
    for y in VENTANA:
        d = A[y]
        imp[str(y)] = {"tau_fila10": d["tau"], "EBIT_historia": d["ebit_h"], "impuesto_nocional_tau_EBIT": d["tau"] * d["ebit_h"],
                       "gasto_por_impuesto": d["imp"], "corriente": d["tax_corr"], "diferido": d["tax_dif"], "pagado": d["imppag"],
                       "escudo_gasto_financiero_tau_fin": d["tau"] * d["fin"], "CVAE_IRAP_incluido": d["tax_cvae"],
                       "pagado_menos_nocional": d["imppag"] - d["tau"] * d["ebit_h"],
                       "diferido_intangibles_(ingreso; PPA no deducible en caja)": d["taxdif_int"],
                       "diferido_ROU_+_pasivos_arrendamiento": d["taxdif_rou"] + d["taxdif_ls"],
                       "tau_por_PPA_(escudo nocional dentro del NOPAT)": d["tau"] * d["da_ppa"]}
        # (O7) ingreso por diferido de intangibles frente a la amortización de relaciones con clientes: base de la
        # inferencia «mayoritariamente no deducible» (la fila incluye también marcas y otros intangibles)
        am_rc = -F(f"INT_RC_AM_{y}")
        imp[str(y)]["amortizacion_relaciones_con_clientes"] = am_rc
        imp[str(y)]["diferido_intangibles_÷_amortizacion_relaciones_con_clientes"] = d["taxdif_int"] / am_rc
    imp["2025"]["anios_de_agotamiento_relaciones_con_clientes_(VNC ÷ amortización 2025)"] = F("INT_RC_VNC_2025") / -F("INT_RC_AM_2025")
    R["tablas"]["impuestos"] = {y: {k: f6(v, 4) for k, v in t_.items()} for y, t_ in imp.items()}
    fin_ = {}
    for y in VENTANA:
        d = A[y]
        fin_[str(y)] = {"FCF publicado": d["fcf_apm"], "FCF base del año (vía CFO)": fcfb[y]["fcf_base_via_cfo"], "adquisiciones": d["adq"],
                        "dividendos": -d["div"], "recompras netas de ampliaciones": -(d["autoc"] + d["ampl"]),
                        "emisión neta de deuda (EFE)": d["empr"] + d["reemb"], "deuda financiera neta final": d["deu_neta"],
                        "pasivo por arrendamientos final": d["pas_fin"], "OCEANE (componente de deuda)": d["oceane"]}
    R["tablas"]["financiacion"] = {y: {k: f6(v, 3) for k, v in t_.items()} for y, t_ in fin_.items()}
    R["tablas"]["financiacion_f"] = {"intereses_financieros_en_f_(%_ventas)": f6(100 * avg(lambda d: d["int"]) / S_avg, 4),
                                     "pagos_arrendamiento_en_f_(%_ventas)": f6(100 * P_avg / S_avg, 4),
                                     "deuda_financiera_neta_2025_sobre_ventas": f6(A[2025]["deu_neta"] / V0, 4)}
    hz = {}
    for y in HORIZONTE:
        d = A[y]
        hz[str(y)] = {"ventas": d["ventas"], "crecimiento_organico_%": d["crec_org"], "capex_bruto": d["capex"], "lino": d["lino"],
                      "otros_articulos": d["oart"], "resto": d["otro"], "D&A_total": d["da_total"], "D&A_ROU": d["da_rou"], "D&A_PPA": d["da_ppa"],
                      "D&A_propia": d["d_own"], "circulante": d["dwc"], "adquisiciones": d["adq"],
                      "fila30_capex−D&A+circulante": d["capex"] - d["da_total"] + d["dwc"],
                      "capex−D&A_propia+circulante": d["capex"] - d["d_own"] + d["dwc"],
                      "lino_compras−amortizacion": d["lino"] - d["da_text"]}
    R["tablas"]["horizonte_2021_2025"] = {y: {k: f6(v, 3) for k, v in t_.items()} for y, t_ in hz.items()}
    R["tablas"]["horizonte_2021_2025"]["ventas_2020"] = f6(S2020, 1)

    # ======================= demostración sintética (sin impuestos, sin crecimiento, estado estacionario)
    # EBITDA 100; capex propio = D&A propia = 20; derechos de uso: amortización 10, pagos 12 (principal 10 + interés 2);
    # PPA 5 sin reposición monetaria. FCF al accionista verdadero = 100 − 20 − 12 = 68.
    sint = {}
    for nombre, con_ppa in (("solo arrendamientos", False), ("arrendamientos y PPA", True)):
        ebitda, dO, dR, pagos, dP = Fr(100), Fr(20), Fr(10), Fr(12), Fr(5 if con_ppa else 0)
        ebit, capex, fcf_verdadero = ebitda - dO - dR - dP, dO, ebitda - dO - pagos
        fila = {"FCF verdadero": fcf_verdadero}
        for alt_n, DX in (("A0 (D&A total)", dO + dR + dP), ("A1 (sin ROU)", dO + dP), ("A2 (propia)", dO)):
            fS_ = ebit - (capex - DX) - fcf_verdadero          # calibración de f con la historia estacionaria
            fila[f"motor sin crecimiento · {alt_n}"] = ebit - fS_  # NOPAT − f·V (τ = 0)
        sint[nombre] = fila
        check(f"sintético {nombre}: A2 reproduce el FCF verdadero", fila["motor sin crecimiento · A2 (propia)"], fcf_verdadero, clase="algebraica")
        check(f"sintético {nombre}: A0 queda por debajo en ROU + PPA", fcf_verdadero - fila["motor sin crecimiento · A0 (D&A total)"], dR + dP, clase="algebraica")
    R["tablas"]["demostracion_sintetica"] = {n: {k: f6(v, 3) for k, v in fl.items()} for n, fl in sint.items()}

    # Valores de referencia para los criterios de prueba de la especificación (12 decimales; entradas registradas)
    ref = {"entradas": {"V0": f6(V0, 12), "m0": f6(m0, 15), "tau_5": f6(tau5, 12), "ventas_medias": f6(S_avg, 12),
                        "nopat_medio": f6(NOPAT_avg, 12), "C52_registrado": f6(C52_libro, 12)}, "perimetros": {}}
    for nombre, DX in defs.items():
        reinv_x = avg(lambda d: d["capex"] - DX(d) + d["dwc"])
        f_x = (NOPAT_avg - reinv_x - C52_libro) / S_avg
        den_tot = sum(A[y]["capex"] - DX(A[y]) + A[y]["dwc"] + A[y]["adq"] for y in HORIZONTE)
        ref["perimetros"][nombre.split(" ")[0]] = {"reinversion_media": f6(reinv_x, 12), "f": f6(f_x, 15),
                                                   "flujo_sin_crecimiento": f6(V0 * (m0 * (1 - tau5) - f_x), 12),
                                                   "S2C_C53": f6((ventas[2025] - S2020) / den_tot, 12) if den_tot > 0 else None}
    if L:
        for nombre, (p, mo) in escenarios.items():
            ref.setdefault("A0_flujos_libro", {})[nombre] = [f6(x, 12) for x in mo["flujos"]] + [f6(mo["flujo_11"], 12)]
    ref["A1_A2_flujos_palancas_actuales"] = flujos_ref
    ref["A1_A2_flujos_detalle"] = {k: {n: {"anios_1_10": v[:10], "anio_11_terminal": v[10]} for n, v in d_.items()} for k, d_ in flujos_ref.items()}
    ref["A3_estimado_sintetico"] = a3_ref
    ref["desvio_anio_11_implementacion_parcial"] = desvio_11
    R["referencia_especificacion"] = ref

    # Cobertura (revisión n.º 3, N2). Va al final, después de la última lectura de cifras, para que clasifique TODAS
    # las entradas usadas, también las de la sección de impuestos. Para CADA entrada, qué la comprueba además de su literal:
    # una identidad entre páginas distintas, una identidad dentro de la misma página, o la Historia del libro (otra
    # extracción de las mismas publicaciones). Las que no tienen nada de eso se listan.
    HIST_CLAVES = {6: ["ventas"], 7: ["bai", "fin"], 8: ["da_total"], 10: ["imp", "bai"], 11: ["cfo"], 12: ["capint", "capmat"],
                   13: ["adq"], 14: ["wc_lineas", "empl"], 17: ["ls_princ"]}
    usos = {}
    for y in HORIZONTE:
        for k, q in AQ[y].items():
            if isinstance(q, Q):
                for i in q.t:
                    usos.setdefault(i, set()).add(f"{k} {y}")
    por_libro = set()
    for y in HORIZONTE:
        claves = [c for v in HIST_CLAVES.values() for c in v] + (["int", "deu_bruta", "pas_fin", "deu_caja"] if y in VENTANA else ["int_con_ls"])
        claves.append("sbc_nota52" if "sbc_nota52" in AQ[y] else "sbc")
        for c in claves:
            if c in AQ[y] and isinstance(AQ[y][c], Q):
                por_libro |= set(AQ[y][c].t)
    if L:
        por_libro.add("IS_VENTAS_U21_2020")   # Historia!G6
    directos = {"IS_VENTAS_U21_2020": "ventas 2020, base del S2C (E9)",
                "INT_RC_VNC_2025": "años de agotamiento de las relaciones con clientes (impuestos, O7)"}
    directos.update({f"INT_RC_AM_{y}": f"amortización de relaciones con clientes {y} (impuestos, O7)" for y in VENTANA})
    cobertura = {}
    for i in sorted(F.usadas):
        entre = sorted(f"{c} {yy}" for (yy, c), q in codigo_q.items() if i in q.t and res_det[str(yy)][c]["contraste"] == "entre páginas")
        misma = sorted(f"{c} {yy}" for (yy, c), q in codigo_q.items() if i in q.t and res_det[str(yy)][c]["contraste"] == "misma página")
        estado = ("contrastada entre páginas" if entre else "solo identidad de la misma página" if misma
                  else "contrastada con la Historia del libro" if i in por_libro else "sin comprobación de segunda línea")
        cobertura[i] = {"fuente": F.ref[i], "usos": sorted(usos.get(i, [])) or [directos.get(i, "uso directo fuera de las tablas anuales")], "identidades_entre_paginas": entre,
                        "identidades_misma_pagina": misma, "historia_del_libro": i in por_libro, "estado": estado}
    # (Revisión n.º 4, P3) Una identidad de la misma página acredita la coherencia interna de su tabla, no su unidad ni su
    # perímetro: una tabla entera de otro perímetro o de otra unidad cuadra igual. La unidad y el perímetro solo los
    # acredita, de forma indirecta, una identidad entre páginas. Se marca, para cada entrada, si su página tiene alguna
    # entrada contrastada entre páginas, y se listan las páginas que no.
    pagina_de = {i: f"{F.meta[i]['doc']} p.{F.meta[i]['pagina']}" for i in cobertura}
    con_ancla = {pagina_de[i] for i, v in cobertura.items() if v["estado"] == "contrastada entre páginas"}
    for i, v in cobertura.items():
        v["pagina_con_identidad_entre_paginas"] = pagina_de[i] in con_ancla
    sin_ancla = {}
    for i in sorted(cobertura):
        if pagina_de[i] not in con_ancla:
            sin_ancla.setdefault(pagina_de[i], []).append(i)
    R["tablas"]["cobertura_entradas"] = {
        "resumen": {e: sum(1 for v in cobertura.values() if v["estado"] == e) for e in
                    ("contrastada entre páginas", "solo identidad de la misma página", "contrastada con la Historia del libro",
                     "sin comprobación de segunda línea")},
        "que_acredita_cada_clase": {
            "contrastada entre páginas": "el número y, de forma indirecta, su unidad y su perímetro: otra presentación de otro perímetro o de otra unidad rompería la identidad",
            "solo identidad de la misma página": "la coherencia interna de su tabla; no la unidad ni el perímetro de la tabla entera",
            "contrastada con la Historia del libro": "el número, salvo un error común a las dos transcripciones de la misma publicación",
            "sin comprobación de segunda línea": "nada más que su literal y las reglas automáticas del verificador"},
        "paginas_sin_identidad_entre_paginas": sin_ancla,
        "resumen_paginas": {"paginas_con_entradas": len(set(pagina_de.values())), "sin_identidad_entre_paginas": len(sin_ancla),
                            "entradas_en_ellas": sum(len(v) for v in sin_ancla.values()),
                            "misma_pagina_en_paginas_sin_ancla": sum(1 for i, v in cobertura.items()
                                                                     if v["estado"] == "solo identidad de la misma página" and not v["pagina_con_identidad_entre_paginas"])},
        "sin_comprobacion": {i: v["usos"] for i, v in cobertura.items() if v["estado"] == "sin comprobación de segunda línea"},
        "entradas": cobertura}
    ok = all(c["ok"] for c in R["comprobaciones"])
    por_clase = {}
    for c in R["comprobaciones"]:
        por_clase[c["clase"]] = por_clase.get(c["clase"], 0) + 1
    R["resumen"] = {"comprobaciones": len(R["comprobaciones"]), "fallidas": sum(not c["ok"] for c in R["comprobaciones"]),
                    "por_clase": por_clase, "libro_contrastado": bool(L), "libro_sha256": L["sha256"] if L else None,
                    "entradas_usadas": len(F.usadas), "entradas_usadas_pendientes": sorted(F.pendientes),
                    "contrapartes_de_identidad_pendientes": sorted(F.contrapartes_pendientes),
                    "copia_recalculada_con_caja_no_nula": bool(a.caja_no_nula)}
    assert set(cobertura) == F.usadas, "la cobertura no clasifica todas las entradas usadas"
    R["tablas"]["entradas_usadas_pendientes"] = F.pendientes
    R["tablas"]["contrapartes_de_identidad_pendientes"] = F.contrapartes_pendientes
    a.salida.parent.mkdir(parents=True, exist_ok=True)
    a.salida.write_text(json.dumps(R, ensure_ascii=False, indent=1), encoding="utf-8")

    # ----------------------------------------------------------------- informe legible
    def tabla(titulo, filas, cab):
        md.append(f"\n### {titulo}\n\n| " + " | ".join(cab) + " |\n|" + "---|" * len(cab))
        for fl in filas:
            md.append("| " + " | ".join("" if x is None else (f"{x:,.3f}".replace(",", " ") if isinstance(x, float) else str(x)) for x in fl) + " |")

    md.append("# Contraste independiente F1 · Elis · resultados calculados\n")
    md.append(f"Generado por `scripts/contraste_f1.py`. Comprobaciones: {R['resumen']['comprobaciones']} ({', '.join(f'{k}: {v}' for k, v in sorted(R['resumen']['por_clase'].items()))}), fallidas: {R['resumen']['fallidas']}. "
              f"Libro contrastado: {'sí, SHA-256 ' + L['sha256'] if L else 'no'}. Millones de euros salvo indicación.")
    tabla("Residuos de las conciliaciones anuales (0 = cuadra exactamente; ±0,1 = redondeo de la cifra impresa)",
          [[k] + [R["tablas"]["conciliaciones_residuos"][str(y)].get(k) for y in VENTANA] for k in conc[2025]], ["Identidad", "2023", "2024", "2025"])
    tabla("FCF base por año y media (C46–C52)", [[k] + [R["tablas"]["fcf_base"]["por_anio"][str(y)][k] for y in VENTANA] for k in fcfb[2025]],
          ["Concepto", "2023", "2024", "2025"])
    tabla("Composición económica de las fugas f·ventas (media 2023–25 y por año)",
          [[k, R["tablas"]["f"]["componentes_media"][k]] + [R["tablas"]["f"]["componentes_por_anio"][str(y)][k] for y in VENTANA] for k in comp_avg]
          + [["TOTAL = C79", f6(FS, 3)] + [f6(nopat[y] - reinv[y] - fcfb[y]["fcf_base_via_cfo"], 3) for y in VENTANA]],
          ["Componente", "Media", "2023", "2024", "2025"])
    tabla("Puente FCF base → flujo sin crecimiento del motor A (base 2025)", [[k, f6(v, 3)] for k, v in puente0.items()], ["Paso", "mm"])
    tabla("Descomposición de la reinversión media 2023–25 (C76)", [[k, f6(v, 3)] for k, v in reinv_desc.items()] + [["TOTAL = C76", f6(REINV_avg, 3)]], ["Bloque", "mm"])
    for n, pp in puente1.items():
        tabla(f"Puente flujo sin crecimiento → año 1 · {n}", [[k, f6(v, 3)] for k, v in pp.items()], ["Paso", "mm"])
    tabla("Arrendamientos por año", [[k] + [R["tablas"]["arrendamientos"][str(y)][k] for y in VENTANA] for k in ls["2025"]], ["Concepto", "2023", "2024", "2025"])
    tabla("Dónde queda el coste de arrendamiento", [[k, f6(v, 3)] for k, v in ubicacion.items()], ["Elemento", "mm"])
    claves_alt = list(next(iter(alt.values())).keys())
    tabla("Alternativas de perímetro de la reinversión necesaria (consecuencias calculadas; ninguna adoptada)",
          [[k] + [alt[n][k] for n in alt] for k in claves_alt], ["Magnitud"] + [n.split(":")[0] for n in alt])
    tabla("Palanca S2C anclada en el C53 de cada perímetro (escenario NORMAL; revisión O4)",
          [[k] + [R["tablas"]["S2C_anclada_en_C53"][x].get(k) for x in R["tablas"]["S2C_anclada_en_C53"]] for k in
           ["S2C_ancla_C53", "f", "flujo_sin_crecimiento", "flujo_año_1_NORMAL_con_S2C_ancla", "brecha_frente_a_A0_sin_crecimiento",
            "brecha_frente_a_A0_año_1", "aumento_de_ventas_que_anula_la_brecha"]], ["Magnitud"] + list(R["tablas"]["S2C_anclada_en_C53"]))
    tabla("Partidas puntuales dentro del flujo sin crecimiento (revisión O9)",
          [[k, v] for k, v in R["tablas"]["partidas_puntuales_en_flujo_sin_crecimiento"].items()], ["Partida", "mm"])
    tabla("Tendencia de los arrendamientos frente a la razón constante de f (revisión O10)",
          [[k, v] for k, v in R["tablas"]["arrendamientos_tendencia"].items()], ["Magnitud", "mm"])
    tabla("Materialidad (porcentaje sobre las ventas del mismo período: medias 2023–25 o 2025)",
          [[k, v["mm"], v["%_FCF_base"], v["%_ventas_del_periodo"]] for k, v in R["tablas"]["materialidad"].items()],
          ["Partida", "mm", "% FCF base (C52)", "% ventas del período"])
    tabla("Impuestos", [[k] + [R["tablas"]["impuestos"][str(y)].get(k) for y in VENTANA] for k in imp["2025"]], ["Concepto", "2023", "2024", "2025"])
    tabla("Demostración sintética (τ = 0, sin crecimiento): flujo del motor frente al FCF verdadero",
          [[k] + [R["tablas"]["demostracion_sintetica"][n][k] for n in sint] for k in next(iter(sint.values()))], ["Magnitud"] + list(sint))
    tabla("Financiación y accionista", [[k] + [R["tablas"]["financiacion"][str(y)][k] for y in VENTANA] for k in fin_["2025"]], ["Concepto", "2023", "2024", "2025"])
    tabla("Horizonte 2021–2025 (S2C)", [[k] + [R["tablas"]["horizonte_2021_2025"][str(y)][k] for y in HORIZONTE] for k in hz["2025"]],
          ["Concepto"] + [str(y) for y in HORIZONTE])
    md.append("\n### Comprobaciones\n")
    for c in R["comprobaciones"]:
        md.append(f"- {'OK' if c['ok'] else 'FALLO'} · [{c['clase']}] {c['nombre']}: {c['calculado']} frente a {c['referencia']} (dif. {c['diferencia']}; tol. {c['tolerancia']})")
    a.informe.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(json.dumps(R["resumen"], ensure_ascii=False))
    for c in R["comprobaciones"]:
        if not c["ok"]:
            print("FALLO", c["nombre"], c["calculado"], c["referencia"], c["diferencia"])
    if not ok:
        return 1
    return 2 if F.pendientes else 0


if __name__ == "__main__":
    sys.exit(main())
