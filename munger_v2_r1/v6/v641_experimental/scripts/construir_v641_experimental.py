#!/usr/bin/env python3
"""Construye la plantilla V6.4.1 EXPERIMENTAL a partir de la V6.4 experimental (que no se modifica). Encargo 4.13 §7.

Uso: python3 -I construir_v641_experimental.py Plantilla_V6.4_experimental.xlsx Plantilla_V6.4.1_experimental.xlsx

Qué cambia frente a la V6.4 (y nada más):
  - «Configuración V6.4», sección 11 nueva (filas 145–156): PERÍMETRO DE LA INVERSIÓN de las bases de P-M1.
      B146 perímetro: vacío o «Caja · capex de caja frente a toda la D&A (V6.4)» = la V6.4; «NIIF 16 · capex de caja + altas de derechos
      de uso frente a toda la D&A»; B147:B151 altas de derechos de uso de los años H–L (mm); B152 fuente; B153 Σ altas que entran en
      las bases (0 con Caja o en modo heredado); B154 perímetro efectivo; B155 S2C histórico de referencia con el perímetro.
  - B55 (Σ reinversión neta total, D_hist) y B58 (Σ capex − D&A, de donde salen el exceso B60, F_hist B62, Rh, f, f_fija, el requisito
    anual y el terminal) suman B153. Con B146 vacío o «Caja», todas las celdas dan lo mismo que en la V6.4 (se comprueba).
  - Trazabilidad: fila 142 «P-M1 · perímetro de la inversión» (activa con requisito adicional); B143 la cuenta.
  - Comprobación 29 (fila 124): perímetro no reconocido, o NIIF 16 sin las cinco altas (≥ 0) o sin su fuente.
  - B9 (resumen) dice el perímetro; etiquetas de versión «V6.4.1 experimental».
Por qué NIIF 16 completo es la alternativa coherente con el motor B (y no «restar la amortización de los derechos de uso»): el motor B
trata los arrendamientos como capital (Historia fila 32) y como deuda (puente, Diagnóstico V6 C16), su NOPAT ya descuenta la amortización
de los derechos de uso y no resta sus pagos; la reposición de esos activos son las altas, financiadas con deuda. Excluir la amortización
de los derechos de uso solo sería coherente reexpresando el NOPAT, el capital y el puente (no se hace).
Después, como la V6.4: gráficos y dibujos de la plantilla de partida (patch_v62_base.restaurar_partes), deslizadores (add_sliders.py) y
paquete determinista.
"""
import os
import subprocess
import sys
import tempfile
from copy import copy

from openpyxl import load_workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.datavalidation import DataValidation

AQUI = os.path.dirname(os.path.abspath(__file__))
V6 = os.path.abspath(os.path.join(AQUI, "..", ".."))
sys.path.insert(0, os.path.join(V6, "scripts"))
sys.path.insert(0, os.path.join(V6, "v64_experimental", "scripts"))
import patch_v62_base as base  # noqa: E402
import construir_v64_experimental as V64  # noqa: E402  (normalizar_paquete, ex, uno_de, vacia, lista)

VERSION = "V6.4.1 experimental"
CFG = "Configuración V6.4"
PERIMETROS = ("Caja · capex de caja frente a toda la D&A (V6.4)", "NIIF 16 · capex de caja + altas de derechos de uso frente a toda la D&A")


def configuracion(wb):
    ws = wb[CFG]
    normal, negrita = Font(name="Arial"), Font(name="Arial", bold=True)
    entrada, calculo = PatternFill("solid", fgColor="FFF2CC"), PatternFill("solid", fgColor="E7E6E6")

    def put(ref, val, font=normal, fill=None):
        ws[ref] = val
        ws[ref].font = font
        ws[ref].alignment = Alignment(wrap_text=True, vertical="top")
        if fill:
            ws[ref].fill = fill
    # bases: la suma de las altas solo entra con el perímetro NIIF 16 (B153 = 0 con Caja o en modo heredado)
    assert ws["B55"].value == "=SUM(Historia!$H$31:$L$31)" and ws["B58"].value == "=SUM(Historia!$H$12:$L$12)-SUM(Historia!$H$8:$L$8)"
    put("A55", "Σ reinversión neta total H–L (Historia H31:L31, denominador de C53) + altas de derechos de uso con el perímetro NIIF 16 (B153)")
    ws["B55"] = "=SUM(Historia!$H$31:$L$31)+$B$153"
    put("A58", "Σ (capex − D&A) H–L + altas de derechos de uso con el perímetro NIIF 16 (B153)")
    ws["B58"] = "=SUM(Historia!$H$12:$L$12)-SUM(Historia!$H$8:$L$8)+$B$153"
    # sección 11
    put("A145", "  11 · PERÍMETRO DE LA INVERSIÓN DE LAS BASES DE P-M1 (V6.4.1 experimental, encargo 4.13 §7)", negrita)
    put("A146", "Perímetro de la inversión (vacío = «Caja», el de la V6.4)")
    ws["B146"].fill = entrada
    put("C146", " · ".join(PERIMETROS) + ". NIIF 16: los arrendamientos son capital y deuda en el motor B; sus altas son la inversión que los repone.")
    for i, col in enumerate("HIJKL"):
        put(f"A{147 + i}", f'="  altas de derechos de uso del año "&IF(ISNUMBER(Historia!${col}$5),Historia!${col}$5,"(Historia {col})")&" (mm; 0 explícito si no las hubo)"')
        ws[f"B{147 + i}"].fill = entrada
    put("A152", "  fuente de las altas (documento, nota y página de cada año)")
    ws["B152"].fill = entrada
    nif = V64.ex("$B$146", PERIMETROS[1])
    put("A153", "Σ altas de derechos de uso H–L que entran en las bases (0 con «Caja» o en modo heredado)")
    put("B153", f'=IF(AND($B$5="Experimental",{nif},COUNT($B$147:$B$151)=5),SUM($B$147:$B$151),0)', fill=calculo)
    put("A154", "Perímetro efectivo")
    put("B154", f'=IF(AND($B$5="Experimental",{nif}),"NIIF 16","Caja")', fill=calculo)
    put("A155", "S2C histórico de referencia con el perímetro (Δventas H–L ÷ D_hist); con «Caja» es Historia C53")
    put("B155", '=IF(AND(ISNUMBER(Historia!$L$6),ISNUMBER(Historia!$G$6),ISNUMBER($B$57)),IF($B$57>0,(Historia!$L$6-Historia!$G$6)/$B$57,""),"")', fill=calculo)
    put("A156", "Con «NIIF 16», D_hist, el exceso histórico (B60), F_hist (B62), Rh, f, f_fija, el requisito anual y el terminal incluyen las altas; "
                "la amortización que se repone (B63) ya incluía la de los derechos de uso. Las series publicadas de la Historia no cambian.")
    ws.merge_cells("A156:G156")
    # trazabilidad: fila 142
    assert ws["A142"].value is None and ws["A141"].value == "Modo"
    put("A142", "P-M1 · perímetro de la inversión")
    put("B142", "=$B$154", fill=calculo)
    for c in "CDEFG":
        ws[f"{c}142"].fill = entrada
    put("H142", '=AND($B$5="Experimental",$B$67)', fill=calculo)
    put("I142", "=IF(AND($H142,COUNTBLANK($C142:$G142)>0),1,0)", fill=calculo)
    assert "SUM($I$129:$I$141)" in ws["B143"].value
    ws["B143"] = ws["B143"].value.replace("SUM($I$129:$I$141)", "SUM($I$129:$I$142)")
    # comprobación 29
    assert ws["A124"].value is None and ws["B124"].value is None
    cond = (f'AND($B$5="Experimental",OR(AND(NOT({V64.vacia("$B$146")}),NOT({V64.uno_de("$B$146", PERIMETROS)})),'
            f'AND({nif},OR(COUNT($B$147:$B$151)<5,MIN($B$147:$B$151)<0,{V64.vacia("$B$152")}))))')
    put("A124", "Comprobación 29")
    put("B124", f"=IFERROR({cond},TRUE)", fill=calculo)
    put("C124", "Perímetro de la inversión: texto no reconocido, o «NIIF 16» sin las cinco altas de derechos de uso (≥ 0; 0 explícito) o sin su fuente")
    ws.merge_cells("C124:G124")
    # resumen B9: el perímetro
    assert ws["B9"].value.endswith('&IF($B$66," · P0 (cartera no repuesta)"," · cartera: legado")))')
    ws["B9"] = ws["B9"].value[:-len('&IF($B$66," · P0 (cartera no repuesta)"," · cartera: legado")))')] + \
        '&IF($B$66," · P0 (cartera no repuesta)"," · cartera: legado")&" · perímetro "&$B$154))'
    dv = DataValidation(type="list", formula1=V64.lista(PERIMETROS), allow_blank=True)
    dv.add("B146")
    ws.add_data_validation(dv)
    for dvx in ws.data_validations.dataValidation:  # clase y confianza también en la fila 142
        r = str(dvx.sqref)
        if r in ("C129:C141", "D129:D141"):
            dvx.sqref = dvx.sqref.__class__(r.replace("141", "142"))


def etiquetas(wb):
    n = 0
    for ws in wb.worksheets:
        for row in ws.iter_rows():
            for c in row:
                if isinstance(c.value, str) and "V6.4 experimental" in c.value:
                    c.value = c.value.replace("V6.4 experimental", VERSION)
                    n += 1
    cm = wb["Control maestro"]["A3"]
    cm.value = cm.value.replace(f"Versión {VERSION} (12-nov-2026, encargo 4.11)", f"Versión {VERSION} (13-nov-2026, encargo 4.13: perímetro de la inversión de P-M1; sobre la V6.4 del encargo 4.11)")
    return n


def main(src, dst):
    wb = load_workbook(src)
    configuracion(wb)
    n = etiquetas(wb)
    with tempfile.TemporaryDirectory() as tmp:
        mid = os.path.join(tmp, "v641.xlsx")
        wb.save(mid)
        restauradas = base.restaurar_partes(src, mid)
        subprocess.run([sys.executable, "-I", os.path.join(AQUI, "add_sliders.py"), mid, dst], check=True, capture_output=True)
    V64.normalizar_paquete(dst)
    print(f"{VERSION}: perímetro de la inversión (Configuración V6.4 B146:B155), B55 y B58 con B153, traza fila 142, comprobación 29; "
          f"{n} etiquetas de versión; partes restauradas {len(restauradas)} → {dst}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)
    main(sys.argv[1], sys.argv[2])
