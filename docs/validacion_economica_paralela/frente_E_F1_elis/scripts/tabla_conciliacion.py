"""Genera resultados/tabla_conciliacion.md desde datos/cifras_fuente.csv (cifras ya verificadas contra los PDF).

Cada celda muestra el literal impreso, con su signo, y la página PDF: así la tabla no depende de una transcripción a mano.
Convención: el literal es el publicado; la columna «Signo en el modelo» dice cómo lo usa la Historia/Análisis.
Uso: python3 -I tabla_conciliacion.py --cifras ../datos/cifras_fuente.csv --salida ../resultados/tabla_conciliacion.md
"""
import argparse
import csv
from pathlib import Path

# (bloque, concepto, signo en el modelo, {año: id})
FILAS = [
    ("EBIT → CFO", "Resultado operativo (EBIT publicado)", "+", {2023: "IS_EBIT_FR_2023", 2024: "IS_EBIT_2024", 2025: "IS_EBIT_2025"}),
    ("EBIT → CFO", "Resultado financiero neto", "gasto = −literal", {2023: "IS_FIN_FR_2023", 2024: "IS_FIN_2024", 2025: "IS_FIN_2025"}),
    ("EBIT → CFO", "Resultado antes de impuestos", "+", {2023: "IS_BAI_FR_2023", 2024: "IS_BAI_2024", 2025: "IS_BAI_2025"}),
    ("EBIT → CFO", "Gasto por impuesto (devengo)", "gasto = −literal", {2023: "IS_IMP_FR_2023", 2024: "IS_IMP_2024", 2025: "IS_IMP_2025"}),
    ("EBIT → CFO", "Pagos en acciones no monetarios (SBC, IFRS 2)", "+ (se resta en C50)", {2023: "CF_SBC_FR_2023", 2024: "CF_SBC_2024", 2025: "CF_SBC_2025"}),
    ("EBIT → CFO", "Amortizaciones y provisiones (línea del EFE)", "+", {2023: "CF_DAP_FR_2023", 2024: "CF_DAP_2024", 2025: "CF_DAP_2025"}),
    ("EBIT → CFO", "Subvenciones imputadas a resultados", "literal", {2023: "CF_SUBV_FR_2023", 2024: "CF_SUBV_2024", 2025: "CF_SUBV_2025"}),
    ("EBIT → CFO", "Resultados por enajenación de inmovilizado", "literal", {2023: "CF_PLUSV_FR_2023", 2024: "CF_PLUSV_2024", 2025: "CF_PLUSV_2025"}),
    ("EBIT → CFO", "Earnout y otros sin efecto en caja", "literal", {2023: "CF_EARN_FR_2023", 2024: "CF_EARN_2024", 2025: "CF_EARN_2025"}),
    ("EBIT → CFO", "Caja antes de costes financieros e impuestos", "+", {2023: "CF_ANTES_FR_2023", 2024: "CF_ANTES_2024", 2025: "CF_ANTES_2025"}),
    ("EBIT → CFO", "Variación del circulante (APM)", "consumo = −literal (fila 14)", {2023: "FCF_BFR_FR_2023", 2024: "FCF_BFR_2024", 2025: "FCF_BFR_2025"}),
    ("EBIT → CFO", "Impuestos pagados", "pago = −literal", {2023: "CF_IMPPAG_FR_2023", 2024: "CF_IMPPAG_2024", 2025: "CF_IMPPAG_2025"}),
    ("EBIT → CFO", "Caja de las operaciones (CFO)", "+ (fila 11; C46)", {2023: "CF_CFO_FR_2023", 2024: "CF_CFO_2024", 2025: "CF_CFO_2025"}),
    ("D&A", "Lino y textil propio en alquiler-mantenimiento", "−literal", {2023: "DA_TEXT_FR_2023", 2024: "DA_TEXT_2024", 2025: "DA_TEXT_2025"}),
    ("D&A", "Otros artículos propios en alquiler-mantenimiento", "−literal", {2023: "DA_OART_FR_2023", 2024: "DA_OART_2024", 2025: "DA_OART_2025"}),
    ("D&A", "Resto de inmovilizado material e intangible", "−literal", {2023: "DA_OTRO_FR_2023", 2024: "DA_OTRO_2024", 2025: "DA_OTRO_2025"}),
    ("D&A", "Derechos de uso NIIF 16 (ROU)", "−literal", {2023: "DA_ROU_FR_2023", 2024: "DA_ROU_2024", 2025: "DA_ROU_2025"}),
    ("D&A", "Subvenciones imputadas", "literal (resta)", {2023: "DA_SUBV_FR_2023", 2024: "DA_SUBV_2024", 2025: "DA_SUBV_2025"}),
    ("D&A", "Deterioros en otros ingresos y gastos operativos", "−literal", {2023: "DA_DETER_FR_2023", 2024: "DA_DETER_2024", 2025: "DA_DETER_2025"}),
    ("D&A", "Intangibles reconocidos en combinaciones (PPA)", "−literal", {2023: "DA_PPA_FR_2023", 2024: "DA_PPA_2024", 2025: "DA_PPA_2025"}),
    ("D&A", "D&A total neta de subvenciones (fila 8)", "−literal", {2023: "DA_TOTAL_FR_2023", 2024: "DA_TOTAL_2024", 2025: "DA_TOTAL_2025"}),
    ("D&A", "Provisiones: dotación neta total", "cargo = −literal", {2023: "PROV_TOT_FR_2023", 2024: "PROV_TOT_2024", 2025: "PROV_TOT_2025"}),
    ("Capex y adquisiciones", "Compras de intangibles (EFE)", "−literal", {2023: "CF_CAPINT_FR_2023", 2024: "CF_CAPINT_2024", 2025: "CF_CAPINT_2025"}),
    ("Capex y adquisiciones", "Compras de inmovilizado material (EFE)", "−literal", {2023: "CF_CAPMAT_FR_2023", 2024: "CF_CAPMAT_2024", 2025: "CF_CAPMAT_2025"}),
    ("Capex y adquisiciones", "de las que: compras de lino", "−literal", {2023: "CAPX_LINO_FR_2023", 2024: "CAPX_LINO_2024", 2025: "CAPX_LINO_2025"}),
    ("Capex y adquisiciones", "de las que: otros artículos en alquiler-mantenimiento", "−literal", {2023: "CAPX_OART_FR_2023", 2024: "CAPX_OART_2024", 2025: "CAPX_OART_2025"}),
    ("Capex y adquisiciones", "de las que: resto de inmovilizado e intangibles", "−literal", {2023: "CAPX_OTRO_FR_2023", 2024: "CAPX_OTRO_2024", 2025: "CAPX_OTRO_2025"}),
    ("Capex y adquisiciones", "Cesiones de activos", "literal", {2023: "CAPX_CES_FR_2023", 2024: "CAPX_CES_2024", 2025: "CAPX_CES_2025"}),
    ("Capex y adquisiciones", "Subvenciones de inversión cobradas", "literal", {2023: "CAPX_SUBV_FR_2023", 2024: "CAPX_SUBV_2024", 2025: "CAPX_SUBV_2025"}),
    ("Capex y adquisiciones", "Capex neto («Net capex», C47)", "−literal", {2023: "FCF_CAPNET_FR_2023", 2024: "FCF_CAPNET_2024", 2025: "FCF_CAPNET_2025"}),
    ("Capex y adquisiciones", "Adquisiciones de filiales netas de caja (fila 13)", "−literal", {2023: "CF_ADQ_FR_2023", 2024: "CF_ADQ_2024", 2025: "CF_ADQ_2025"}),
    ("Arrendamientos", "Pagos de arrendamientos incl. intereses (EFE, financiación)", "−literal", {2023: "CF_LEASE_FR_2023", 2024: "CF_LEASE_2024", 2025: "CF_LEASE_2025"}),
    ("Arrendamientos", "Principal pagado (nota de arrendamientos; fila 17; C49)", "−literal", {2023: "LS_PRINC_PAS_2023", 2024: "LS_PRINC_PAS_2024", 2025: "LS_PRINC_PAS_2025"}),
    ("Arrendamientos", "Gasto por intereses de arrendamientos (devengo, nota 8.2)", "−literal", {2023: "FIN_INTLS_FR_2023", 2024: "FIN_INTLS_2024", 2025: "FIN_INTLS_2025"}),
    ("Arrendamientos", "Nuevos derechos de uso (alta no monetaria)", "literal", {2023: "LS_NUEVO_ROU_2023", 2024: "LS_NUEVO_ROU_2024", 2025: "LS_NUEVO_ROU_2025"}),
    ("Arrendamientos", "Reestimaciones de derechos de uso (no monetario)", "literal", {2023: "LS_REEST_ROU_2023", 2024: "LS_REEST_ROU_2024", 2025: "LS_REEST_ROU_2025"}),
    ("Arrendamientos", "Altas por combinaciones de negocios (no monetario)", "literal", {2023: "LS_COMB_ROU_2023", 2024: "LS_COMB_ROU_2024", 2025: "LS_COMB_ROU_2025"}),
    ("Arrendamientos", "Pasivo por arrendamientos al cierre (fila 23)", "literal", {2023: "LS_SALDO_PAS_2023_FR", 2024: "LS_SALDO_PAS_2024", 2025: "LS_SALDO_PAS_2025"}),
    ("Financiación", "Intereses financieros netos pagados (sin arrendamientos; C48)", "−literal", {2023: "CF_INT_FR_2023", 2024: "CF_INT_2024", 2025: "CF_INT_2025"}),
    ("Financiación", "Deuda financiera bruta (fila 22)", "literal", {2023: "DEU_BRUTA_FR_2023", 2024: "DEU_BRUTA_2024", 2025: "DEU_BRUTA_2025"}),
    ("Financiación", "Caja y equivalentes (fila 24)", "literal", {2023: "DEU_CAJA_FR_2023", 2024: "DEU_CAJA_2024", 2025: "DEU_CAJA_2025"}),
    ("Financiación", "Deuda financiera neta", "literal", {2023: "DEU_NETA_FR_2023", 2024: "DEU_NETA_2024", 2025: "DEU_NETA_2025"}),
    ("Financiación", "OCEANE 2029 (componente de deuda)", "literal", {2023: "DEU_OCEANE_FR_2023", 2024: "DEU_OCEANE_2024", 2025: "DEU_OCEANE_2025"}),
    ("Financiación", "Dividendos pagados", "literal", {2023: "CF_DIV_FR_2023", 2024: "CF_DIV_2024", 2025: "CF_DIV_2025"}),
    ("Financiación", "Acciones propias", "literal", {2023: "CF_AUTOC_FR_2023", 2024: "CF_AUTOC_2024", 2025: "CF_AUTOC_2025"}),
    ("Financiación", "Free cash flow publicado (APM)", "literal", {2023: "FCF_FCF_FR_2023", 2024: "FCF_FCF_2024", 2025: "FCF_FCF_2025"}),
    ("SBC", "Cargas sociales de pagos en acciones (caja, en el APM)", "−literal", {2023: "FCF_SBCSOC_FR_2023", 2024: "FCF_SBCSOC_2024", 2025: "FCF_SBCSOC_2025"}),
    ("SBC", "Gasto IFRS 2 total en la conciliación del EBIT ajustado", "magnitud", {2023: "EBITA_SBC_FR_2023", 2024: "EBITA_SBC_2024", 2025: "EBITA_SBC_2025"}),
    ("Impuestos", "Impuesto corriente", "literal", {2023: "TAX_CORR_FR_2023", 2024: "TAX_CORR_2024", 2025: "TAX_CORR_2025"}),
    ("Impuestos", "Impuesto diferido", "literal", {2023: "TAX_DIF_FR_2023", 2024: "TAX_DIF_2024", 2025: "TAX_DIF_2025"}),
    ("Impuestos", "Diferido por intangibles en resultados (reversión de pasivo)", "literal", {2023: "TAXDIF_INT_2023", 2024: "TAXDIF_INT_2024", 2025: "TAXDIF_INT_2025"}),
    ("Impuestos", "Impuestos no basados en el resultado (CVAE, IRAP)", "literal", {2023: "TAX_CVAE_FR_2023", 2024: "TAX_CVAE_2024", 2025: "TAX_CVAE_2025"}),
    ("Intangibles adquiridos", "Relaciones con clientes: amortización", "−literal", {2023: "INT_RC_AM_2023", 2024: "INT_RC_AM_2024", 2025: "INT_RC_AM_2025"}),
    ("Intangibles adquiridos", "Relaciones con clientes: altas por combinaciones", "literal", {2023: "INT_RC_COMB_2023", 2024: "INT_RC_COMB_2024", 2025: "INT_RC_COMB_2025"}),
    ("Intangibles adquiridos", "Relaciones con clientes: valor neto al cierre", "literal", {2023: "INT_RC_VNC_2023", 2024: "INT_RC_VNC_2024", 2025: "INT_RC_VNC_2025"}),
    ("Crecimiento", "Crecimiento orgánico de ventas (%)", "literal", {2023: "CREC_ORG_2023", 2024: "CREC_ORG_2024", 2025: "CREC_ORG_2025"}),
    ("Crecimiento", "Ventas (fila 6)", "literal", {2023: "IS_VENTAS_FR_2023", 2024: "IS_VENTAS_2024", 2025: "IS_VENTAS_2025"}),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cifras", required=True, type=Path)
    ap.add_argument("--salida", required=True, type=Path)
    a = ap.parse_args()
    c = {r["id"]: r for r in csv.DictReader(a.cifras.open(encoding="utf-8"), delimiter=";")}
    doc = {"URD2025": "URD25", "DEU2024FR": "DEU24", "URD2023": "URD23", "URD2022": "URD22", "URD2021": "URD21"}
    out = ["# Tabla de conciliación 2023–2025 · cifras publicadas con fuente\n",
           "Generada por `scripts/tabla_conciliacion.py` desde `datos/cifras_fuente.csv`; cada cifra está verificada contra los bytes del PDF "
           "(`resultados/verificacion_cifras.json`). Literal impreso con su signo · documento y página PDF (no folio). Millones de euros, "
           "consolidado IFRS del grupo Elis, ejercicios naturales. 2023 = comparativo reexpresado del DEU 2024 (francés); 2024 = comparativo "
           "reexpresado del URD 2025; 2025 = URD 2025. Excepción: el diferido por intangibles de 2023 procede del URD 2023 (edición original).\n"]
    bloque = None
    for b, concepto, signo, ids in FILAS:
        if b != bloque:
            out.append(f"\n## {b}\n\n| Concepto | Signo en el modelo | 2023 | 2024 | 2025 |\n|---|---|---|---|---|")
            bloque = b
        celdas = []
        for y in (2023, 2024, 2025):
            r = c[ids[y]]
            celdas.append(f"{r['literal']} · {doc[r['doc']]} p.{r['pagina']}")
        out.append(f"| {concepto} | {signo} | " + " | ".join(celdas) + " |")
    a.salida.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"escrita {a.salida}")


if __name__ == "__main__":
    main()
