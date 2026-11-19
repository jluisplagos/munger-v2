#!/usr/bin/env python3
"""zoetis_t2 · cifras del segundo tiempo de Zoetis (tercer trimestre de 2026, publicado el 5-nov-2026), comprobadas en el texto con marcas
[PDF PAGE n] antes de usarlas. Módulo común de generar_cambio_zoetis_t2.py, corregir_registro_zoetis_t2.py y extracto_zoetis_t2.py.
Cada componente es (archivo de texto, página del PDF, comienzo de la línea, posición del número en la línea, valor esperado): se busca en la
página la ÚNICA línea que empieza así y se comprueba que el número de esa posición es el esperado (se aborta si no). Extractor: Claude
orquestación (19-nov-2026). Mistral (rama mistral/examen-zoetis-t2) se usa solo como contraste, no como fuente.
LTM al 30-sep-2026 = 10-K 2025 (base anterior a la «Fiscal Year Alignment») − 9M-2025 + 9M-2026 (10-Q T3 2026). La nota 2 del 10-Q
(PDF p. 10–11) da el 9M-2025 «As previously reported» para ingresos, BAI, impuestos, beneficio neto y CFO, que se usan (misma base que el
10-K 2025); para intereses, D&A, capex y arrendamientos financieros solo publica el 9M-2025 reexpresado («recast»), que se usa: esas
cuatro mezclan bases (aproximación declarada, como en zoetis_t1d con el T2)."""
import hashlib, os, re
from fractions import Fraction as F

Q3 = "zoetis-10q-2026-q3.txt"
K25 = "zoetis-10k-fy2025.txt"
PR3 = "zoetis-3q2026-press-release.txt"
FR3 = "zoetis-3q2026-financial-results.txt"
NUM = re.compile(r"\(?\$?\s*[0-9][0-9,]*(?:\.[0-9]+)?\)?|—")


def paginas(ruta):
    t = open(ruta, encoding="utf-8").read()
    p = re.split(r"\[PDF PAGE (\d+)\]\n", t)
    return {int(p[i]): p[i + 1] for i in range(1, len(p), 2)}


def numeros(linea, prefijo):
    resto = linea.strip()[len(prefijo):]
    out = []
    for m in NUM.finditer(resto):
        s = m.group(0).replace("$", "").replace(" ", "")
        if s == "—":
            out.append(0)
            continue
        neg = s.startswith("(")
        s = s.strip("()").replace(",", "")
        if not s:
            continue
        v = F(s)
        out.append(-v if neg else v)
    return out


class Textos:
    def __init__(self, dir_texto):
        self.dir = dir_texto
        self.p = {}

    def sha(self, archivo):
        return hashlib.sha256(open(os.path.join(self.dir, archivo), "rb").read()).hexdigest()

    def pag(self, archivo, n):
        if archivo not in self.p:
            self.p[archivo] = paginas(os.path.join(self.dir, archivo))
        return self.p[archivo][n]

    def linea(self, archivo, n, prefijo, i, esperado):
        cand = [l for l in self.pag(archivo, n).split("\n") if l.strip().startswith(prefijo) and re.match(r"(\s|\$|$)", l.strip()[len(prefijo):])]
        if len(cand) > 1:  # la misma etiqueta en dos líneas de la página: vale solo si una y solo una lleva el valor en esa posición
            cand = [l for l in cand if len(numeros(l, prefijo)) > i and numeros(l, prefijo)[i] == F(str(esperado))]
        assert len(cand) == 1, (archivo, n, prefijo, cand)
        v = numeros(cand[0], prefijo)
        assert v[i] == F(str(esperado)), (archivo, n, prefijo, v, esperado)
        return cand[0].rstrip()

    def frase(self, archivo, n, frase):
        """Frase literal (con los espacios normalizados) en la página n."""
        assert " ".join(frase.split()) in " ".join(self.pag(archivo, n).split()), (archivo, n, frase)
        return frase


# componentes: clave → (archivo, página, prefijo de la línea, índice del número, valor, concepto, columna, periodo, reexpresado)
COMP = {
    # 10-Q T3 2026, cuenta de resultados (PDF p. 3): columnas 3M-2026, 3M-2025, 9M-2026, 9M-2025 (recast)
    "q3_p3_revenue_9m2026": (Q3, 3, "Revenue", 2, 7121, "Revenue", "nueve meses 2026", "1-ene a 30-sep-2026", "no aplica (período corriente)"),
    "q3_p3_revenue_9m2025_recast": (Q3, 3, "Revenue", 3, 7094, "Revenue", "nueve meses 2025 (2025(a), reexpresado)", "1-ene a 30-sep-2025", "reexpresado («recast», Fiscal Year Alignment)"),
    "q3_p3_interest_expense_9m2026": (Q3, 3, "Interest expense, net of capitalized interest", 2, 185, "Interest expense, net of capitalized interest", "nueve meses 2026", "1-ene a 30-sep-2026", "no aplica (período corriente)"),
    "q3_p3_interest_expense_9m2025": (Q3, 3, "Interest expense, net of capitalized interest", 3, 165, "Interest expense, net of capitalized interest", "nueve meses 2025 (2025(a), reexpresado; la nota 2 no da la cifra «as previously reported»)", "1-ene a 30-sep-2025", "reexpresado («recast»): mezcla bases con el 10-K 2025"),
    "q3_p3_bai_9m2026": (Q3, 3, "Income before provision for taxes on income", 2, 2353, "Income before provision for taxes on income", "nueve meses 2026", "1-ene a 30-sep-2026", "no aplica (período corriente)"),
    "q3_p3_taxes_9m2026": (Q3, 3, "Provision for taxes on income", 2, 470, "Provision for taxes on income", "nueve meses 2026", "1-ene a 30-sep-2026", "no aplica (período corriente)"),
    "q3_p3_net_income_9m2026": (Q3, 3, "Net income before allocation to noncontrolling interests", 2, 1883, "Net income before allocation to noncontrolling interests", "nueve meses 2026", "1-ene a 30-sep-2026", "no aplica (período corriente)"),
    # nota 2, «Fiscal Year Alignment» (PDF p. 10): 3M-2025 prev, ajuste, recast; 9M-2025 prev, ajuste, recast
    "q3_p10_revenue_9m2025_prev": (Q3, 10, "Revenue", 3, 7080, "Revenue (as previously reported)", "nueve meses 2025 «As previously reported»", "1-ene a 30-sep-2025", "base antigua («As previously reported»), la del 10-K 2025"),
    "q3_p10_bai_9m2025_prev": (Q3, 10, "Income before provision for taxes on income", 3, 2599, "Income before provision for taxes on income (as previously reported)", "nueve meses 2025 «As previously reported»", "1-ene a 30-sep-2025", "base antigua («As previously reported»), la del 10-K 2025"),
    "q3_p10_bai_9m2025_recast": (Q3, 10, "Income before provision for taxes on income", 5, 2571, "Income before provision for taxes on income (as recast)", "nueve meses 2025 «As recast»", "1-ene a 30-sep-2025", "reexpresado («As recast»)"),
    "q3_p10_taxes_9m2025_prev": (Q3, 10, "Provision for taxes on income", 3, 529, "Provision for taxes on income (as previously reported)", "nueve meses 2025 «As previously reported»", "1-ene a 30-sep-2025", "base antigua («As previously reported»), la del 10-K 2025"),
    "q3_p10_net_income_9m2025_prev": (Q3, 10, "Net income attributable to Zoetis Inc.", 3, 2070, "Net income attributable to Zoetis Inc. (as previously reported)", "nueve meses 2025 «As previously reported»", "1-ene a 30-sep-2025", "base antigua («As previously reported»), la del 10-K 2025"),
    # nota 2 (PDF p. 11): CFO 9M-2025 prev, ajuste, recast
    "q3_p11_cfo_9m2025_prev": (Q3, 11, "Net cash provided by operating activities", 0, 2011, "Net cash provided by operating activities (as previously reported)", "nueve meses 2025 «As previously reported»", "1-ene a 30-sep-2025", "base antigua («As previously reported»), la del 10-K 2025"),
    "q3_p11_cfo_9m2025_recast": (Q3, 11, "Net cash provided by operating activities", 2, 2056, "Net cash provided by operating activities (as recast)", "nueve meses 2025 «As recast»", "1-ene a 30-sep-2025", "reexpresado («As recast»)"),
    # estado de flujos (PDF p. 8): 9M-2026, 9M-2025 (recast)
    "q3_p8_cfo_9m2026": (Q3, 8, "Net cash provided by operating activities", 0, 1880, "Net cash provided by operating activities", "nueve meses 2026", "1-ene a 30-sep-2026", "no aplica (período corriente)"),
    "q3_p8_da_9m2026": (Q3, 8, "Depreciation and amortization expense", 0, 357, "Depreciation and amortization expense", "nueve meses 2026", "1-ene a 30-sep-2026", "no aplica (período corriente)"),
    "q3_p8_da_9m2025": (Q3, 8, "Depreciation and amortization expense", 1, 365, "Depreciation and amortization expense", "nueve meses 2025 (2025(a), reexpresado; la nota 2 no da la cifra «as previously reported»)", "1-ene a 30-sep-2025", "reexpresado («recast»): mezcla bases con el 10-K 2025"),
    "q3_p8_capex_9m2026": (Q3, 8, "Capital expenditures", 0, -334, "Capital expenditures", "nueve meses 2026", "1-ene a 30-sep-2026", "no aplica (período corriente)"),
    "q3_p8_capex_9m2025": (Q3, 8, "Capital expenditures", 1, -462, "Capital expenditures", "nueve meses 2025 (2025(a), reexpresado; la nota 2 no da la cifra «as previously reported»)", "1-ene a 30-sep-2025", "reexpresado («recast»): mezcla bases con el 10-K 2025"),
    "q3_p8_finance_leases_9m2026": (Q3, 8, "Financing cash flows - finance leases", 0, 1, "Financing cash flows - finance leases (principal de arrendamientos financieros pagado)", "nueve meses 2026", "1-ene a 30-sep-2026", "no aplica (período corriente)"),
    "q3_p8_finance_leases_9m2025": (Q3, 8, "Financing cash flows - finance leases", 1, 2, "Financing cash flows - finance leases (principal de arrendamientos financieros pagado)", "nueve meses 2025 (2025(a), reexpresado)", "1-ene a 30-sep-2025", "reexpresado («recast»)"),
    "q3_p8_ar_change_9m2026": (Q3, 8, "Accounts receivable", 0, -291, "Accounts receivable (variación en el estado de flujos)", "nueve meses 2026", "1-ene a 30-sep-2026", "no aplica (período corriente)"),
    "q3_p8_ar_change_9m2025": (Q3, 8, "Accounts receivable", 1, -190, "Accounts receivable (variación en el estado de flujos)", "nueve meses 2025 (reexpresado)", "1-ene a 30-sep-2025", "reexpresado («recast»)"),
    "q3_p8_inv_change_9m2026": (Q3, 8, "Inventories", 0, -143, "Inventories (variación en el estado de flujos)", "nueve meses 2026", "1-ene a 30-sep-2026", "no aplica (período corriente)"),
    "q3_p8_inv_change_9m2025": (Q3, 8, "Inventories", 1, -182, "Inventories (variación en el estado de flujos)", "nueve meses 2025 (reexpresado)", "1-ene a 30-sep-2025", "reexpresado («recast»)"),
    # balance (PDF p. 5): 30-sep-2026, 31-dic-2025 (recast)
    "q3_p5_cash_2026-09-30": (Q3, 5, "Cash and cash equivalents(b)", 0, 1333, "Cash and cash equivalents(b) (incluye 2 de caja restringida, nota (b))", "30 de septiembre de 2026", "saldo a 30-sep-2026", "no aplica (saldo interino)"),
    "q3_p5_cash_2025-12-31_recast": (Q3, 5, "Cash and cash equivalents(b)", 1, 2450, "Cash and cash equivalents(b)", "31 de diciembre de 2025 (2025(a), reexpresado)", "saldo a 31-dic-2025", "reexpresado («recast»; el 10-K 2025 imprime 2.312)"),
    "q3_p5_sti_2026-09-30": (Q3, 5, "Short-term investments", 0, 200, "Short-term investments", "30 de septiembre de 2026", "saldo a 30-sep-2026", "no aplica (saldo interino)"),
    "q3_p5_inventories_2026-09-30": (Q3, 5, "Inventories", 0, 2536, "Inventories", "30 de septiembre de 2026", "saldo a 30-sep-2026", "no aplica (saldo interino)"),
    "q3_p5_receivables_2026-09-30": (Q3, 5, "Accounts receivable, less allowance", 4, 1692, "Accounts receivable, less allowance for doubtful accounts", "30 de septiembre de 2026", "saldo a 30-sep-2026", "no aplica (saldo interino)"),
    "q3_p5_goodwill_2026-09-30": (Q3, 5, "Goodwill", 0, 2888, "Goodwill", "30 de septiembre de 2026", "saldo a 30-sep-2026", "no aplica (saldo interino)"),
    "q3_p5_total_assets_2026-09-30": (Q3, 5, "Total assets", 0, 15088, "Total assets", "30 de septiembre de 2026", "saldo a 30-sep-2026", "no aplica (saldo interino)"),
    "q3_p5_current_ltd_2026-09-30": (Q3, 5, "Current portion of long-term debt", 0, 750, "Current portion of long-term debt", "30 de septiembre de 2026", "saldo a 30-sep-2026", "no aplica (saldo interino)"),
    "q3_p5_long_term_debt_2026-09-30": (Q3, 5, "Long-term debt, net of discount and issuance costs", 0, 8299, "Long-term debt, net of discount and issuance costs", "30 de septiembre de 2026", "saldo a 30-sep-2026", "no aplica (saldo interino)"),
    "q3_p5_long_term_debt_2025-12-31_recast": (Q3, 5, "Long-term debt, net of discount and issuance costs", 1, 9042, "Long-term debt, net of discount and issuance costs", "31 de diciembre de 2025 (2025(a))", "saldo a 31-dic-2025", "reexpresado («recast»; coincide con el 10-K 2025)"),
    "q3_p5_total_equity_2026-09-30": (Q3, 5, "Total equity", 0, 3303, "Total equity", "30 de septiembre de 2026", "saldo a 30-sep-2026", "no aplica (saldo interino)"),
    "q3_p5_total_equity_2025-12-31_recast": (Q3, 5, "Total equity", 1, 3415, "Total equity", "31 de diciembre de 2025 (2025(a), reexpresado)", "saldo a 31-dic-2025", "reexpresado («recast»; el 10-K 2025 imprime 3.331)"),
}
# entradas auxiliares del registro de zoetis_t1d que se reutilizan (10-K 2025, selladas)
AUX_10K = {
    "bai_2025": ("aux:zoetis-10k-fy2025_p66_bai_2025", 3360),
    "interest_2025": ("aux:zoetis-10k-fy2025_p66_interest_expense_2025_ttm", 222),
    "taxes_2025": ("aux:zoetis-10k-fy2025_p66_provision_for_taxes_on_income_2025", 687),
    "da_2025": ("aux:zoetis-10k-fy2025_p70_depreciation_and_amortization_2025", 487),
    "cfo_2025": ("aux:zoetis-10k-fy2025_p70_cfo_10k2025_2025", 2904),
    "capex_2025": ("aux:zoetis-10k-fy2025_p70_capex_10k2025_2025", 621),
    "fl_2025": ("aux:zoetis-10k-fy2025_p89_principal_arrendamientos_financieros_2025", 2),
    "ar_change_2025": ("aux:zoetis-10k-fy2025_p70_accounts_receivable_2025", -236),
    "inv_change_2025": ("aux:zoetis-10k-fy2025_p70_inventories_2025", -199),
}
# 10-K 2025, líneas comprobadas aquí también (para la tabla de vigencia y el extracto)
K = {"revenue_2025": (K25, 66, "Revenue", 0, 9467), "net_income_2025": (K25, 66, "Net income before allocation to noncontrolling interests", 0, 2673)}


def aux_id(clave):
    assert clave.startswith("q3_")
    return "aux:zoetis-10q-2026-q3_" + clave[3:]


def calcular(tx):
    """Valores de los componentes (comprobados en el texto) y cifras derivadas exactas (Fraction)."""
    v = {}
    for k, (a, n, pref, i, val, *_r) in COMP.items():
        tx.linea(a, n, pref, i, val)
        v[k] = F(val)
    for k, (a, n, pref, i, val) in K.items():
        tx.linea(a, n, pref, i, val)
    k = {c: F(x[1]) for c, x in AUX_10K.items()}
    d = {}
    d["revenue_ltm"] = F(9467) - v["q3_p10_revenue_9m2025_prev"] + v["q3_p3_revenue_9m2026"]
    d["revenue_ltm_recast"] = F(9467) - v["q3_p3_revenue_9m2025_recast"] + v["q3_p3_revenue_9m2026"]
    d["bai_ltm"] = k["bai_2025"] - v["q3_p10_bai_9m2025_prev"] + v["q3_p3_bai_9m2026"]
    d["bai_ltm_recast"] = k["bai_2025"] - v["q3_p10_bai_9m2025_recast"] + v["q3_p3_bai_9m2026"]
    d["int_ltm"] = k["interest_2025"] - v["q3_p3_interest_expense_9m2025"] + v["q3_p3_interest_expense_9m2026"]
    d["da_ltm"] = k["da_2025"] - v["q3_p8_da_9m2025"] + v["q3_p8_da_9m2026"]
    d["tax_ltm"] = k["taxes_2025"] - v["q3_p10_taxes_9m2025_prev"] + v["q3_p3_taxes_9m2026"]
    d["ni_ltm"] = F(2673) - v["q3_p10_net_income_9m2025_prev"] + v["q3_p3_net_income_9m2026"]
    d["ebit_ltm"] = d["bai_ltm"] + d["int_ltm"]
    d["ebitda_ltm"] = d["ebit_ltm"] + d["da_ltm"]
    d["ebitda_ltm_recast"] = d["bai_ltm_recast"] + d["int_ltm"] + d["da_ltm"]
    d["cfo_ltm"] = k["cfo_2025"] - v["q3_p11_cfo_9m2025_prev"] + v["q3_p8_cfo_9m2026"]
    d["cfo_ltm_recast"] = k["cfo_2025"] - v["q3_p11_cfo_9m2025_recast"] + v["q3_p8_cfo_9m2026"]
    d["capex_ltm"] = k["capex_2025"] + v["q3_p8_capex_9m2025"] - v["q3_p8_capex_9m2026"]   # en positivo: 621 − 462 + 334
    d["fl_ltm"] = k["fl_2025"] - v["q3_p8_finance_leases_9m2025"] + v["q3_p8_finance_leases_9m2026"]
    d["fcf_ltm"] = d["cfo_ltm"] - d["capex_ltm"] - 0 - d["fl_ltm"]
    d["fcf_ltm_recast"] = d["cfo_ltm_recast"] - d["capex_ltm"] - d["fl_ltm"]
    d["deuda"] = v["q3_p5_current_ltd_2026-09-30"] + v["q3_p5_long_term_debt_2026-09-30"]
    d["caja"] = v["q3_p5_cash_2026-09-30"]
    d["deuda_neta"] = d["deuda"] - d["caja"]
    d["C33"] = d["deuda_neta"] / d["ebitda_ltm"]
    d["C33_recast"] = d["deuda_neta"] / d["ebitda_ltm_recast"]
    d["t_ltm"] = d["tax_ltm"] / d["bai_ltm"]
    d["nopat_ltm"] = d["ebit_ltm"] * (1 - d["t_ltm"])
    d["capital_sep"] = v["q3_p5_total_equity_2026-09-30"] + d["deuda"] - d["caja"]
    d["capital_dic"] = v["q3_p5_total_equity_2025-12-31_recast"] + v["q3_p5_long_term_debt_2025-12-31_recast"] - v["q3_p5_cash_2025-12-31_recast"]
    d["C24"] = d["nopat_ltm"] / d["capital_sep"]
    d["C24_medio"] = d["nopat_ltm"] / ((d["capital_sep"] + d["capital_dic"]) / 2)
    d["C24_sin_sti"] = d["nopat_ltm"] / (d["capital_sep"] - v["q3_p5_sti_2026-09-30"])
    d["C32"] = v["q3_p5_goodwill_2026-09-30"] / v["q3_p5_total_assets_2026-09-30"]
    d["inv_ltm_aumento"] = -(k["inv_change_2025"] - v["q3_p8_inv_change_9m2025"] + v["q3_p8_inv_change_9m2026"])   # 199 − 182 + 143
    d["ar_ltm_aumento"] = -(k["ar_change_2025"] - v["q3_p8_ar_change_9m2025"] + v["q3_p8_ar_change_9m2026"])      # 236 − 190 + 291
    assert (d["bai_ltm"], d["int_ltm"], d["da_ltm"], d["ebitda_ltm"], d["cfo_ltm"], d["capex_ltm"], d["fl_ltm"], d["fcf_ltm"]) == (3114, 242, 479, 3835, 2773, 493, 1, 2279)
    assert (d["deuda"], d["caja"], d["deuda_neta"], d["tax_ltm"], d["capital_sep"], d["capital_dic"]) == (9049, 1333, 7716, 628, 11019, 10007)
    return v, d
