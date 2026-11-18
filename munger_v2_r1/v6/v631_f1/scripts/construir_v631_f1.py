#!/usr/bin/env python3
"""Construye la plantilla V6.3.1 F1 del motor A a partir de la V6.3 (que no se modifica). F1-IMPL, recomendación (a) de la revisión.

Uso: python3 -I construir_v631_f1.py Plantilla_V6.3.xlsx Plantilla_V6.3.1_F1.xlsx

Qué es. La V6.3 con un solo cambio de modelo: la amortización que f, el ancla de S2C y, a través de f, el terminal tratan como
reposición (D_X) se calcula con el PERÍMETRO F1 de la reinversión que declara la persona (decisiones F1 del 17-nov-2026, E2–E4):
  A0_total   D_X = D&A total (fila 8)                     = la V6.3
  A1_sin_ROU D_X = D&A total − D&A de derechos de uso
  A2_propio  D_X = D&A total − D&A de derechos de uso − PPA
A3_estimado (R estimada), N1 y los términos explícitos (transición, compras) NO están en el libro: con ellos la capa F1
(personaje_v2/scripts/motor_a_f1.py) sigue bloqueando (F1-LIBRO). La plantilla no elige ningún perímetro: vacío = A0 = la V6.3.

Qué cambia frente a la V6.3 (y nada más):
  - Historia, sección nueva (filas 84–90): C85 perímetro (vacío, A0_total, A1_sin_ROU o A2_propio; lista de validación);
    C86:L86 D&A de derechos de uso y C87:L87 PPA por año (≥ 0; vacío = desconocido, no cero), con sus fuentes en M85:S87;
    C88:L88 D_X por año con el perímetro efectivo (vacío si falta una serie que el perímetro necesita); C89 perímetro efectivo
    («no reconocido» con un texto que no es de la lista: entonces D_X y f quedan vacías).
  - Fila 30 (reinversión neta orgánica, y con ella la fila 31): capex − D_X + circulante. Con A0, D_X es la fila 8: mismo valor.
  - C58 (f), C76 (conciliación) y C53 (ancla de S2C): con A0 la fórmula de la V6.3 literal; con A1/A2, la reinversión de la fila 30.
    Con A1/A2, f exige D_X en todos los años de la ventana (vacío ≠ 0) y el ancla, D_X en los cinco años H–L.
  - Motor E205 (validación V05 del motor A): con A1/A2 dice qué falta (INC) o qué es inválido (INV: perímetro no reconocido o
    D&A de derechos de uso + PPA mayor que la D&A total) en lugar de dejar f vacía sin explicación. Con A0 no añade nada.
  - Etiquetas de versión: Panel A1, Análisis A1, Guía V6 A1 y Control maestro A3 («V6.3.1 F1»).
Después, como la V6.4.1: gráficos y dibujos de la plantilla de partida (patch_v62_base.restaurar_partes), deslizadores (add_sliders.py)
y paquete determinista (fechas fijas).
"""
import os
import re
import subprocess
import sys
import tempfile
import zipfile
from copy import copy

from openpyxl import load_workbook
from openpyxl.styles import Alignment, Font
from openpyxl.worksheet.datavalidation import DataValidation

AQUI = os.path.dirname(os.path.abspath(__file__))
V6 = os.path.abspath(os.path.join(AQUI, "..", ".."))
sys.path.insert(0, os.path.join(V6, "scripts"))
import patch_v62_base as base  # noqa: E402

VERSION = "V6.3.1 F1"
FECHA_FIJA = (2026, 11, 18, 0, 0, 0)
HI = "Historia"
COLS = "CDEFGHIJKL"
PERIMETROS = ("A0_total", "A1_sin_ROU", "A2_propio")   # los mismos identificadores que motor_a_f1.PERIMETROS
F_SEL, F_ROU, F_PPA, F_DX, F_EF = 85, 86, 87, 88, 89
VENTANA = "COLUMN($C$6:$L$6)>12-$C$57"


def _estilo(dst, src):
    dst.font, dst.fill, dst.border = copy(src.font), copy(src.fill), copy(src.border)
    dst.number_format, dst.alignment, dst.protection = src.number_format, copy(src.alignment), copy(src.protection)


def historia(wb):
    ws = wb[HI]
    for r in range(84, 91):
        for c in range(1, 20):
            assert ws.cell(r, c).value is None, f"Historia fila {r} no está libre"
    # --- sección nueva
    _estilo(ws["A84"], ws["A41"])
    ws["A84"] = "  PERÍMETRO F1 DE LA REINVERSIÓN · motor A (V6.3.1 F1): qué amortización tratan f y el ancla de S2C como reposición"
    filas = ((F_SEL, "Perímetro de la reinversión (vacío = A0_total, el de la V6.3)", "Lo declara la persona (motor_a_f1.json)"),
             (F_ROU, "Amortización de derechos de uso (D&A ROU, NIIF 16), dentro de la fila 8", "Nota de derechos de uso · vacío = desconocido"),
             (F_PPA, "Amortización de intangibles de combinaciones (PPA), dentro de la fila 8", "Nota de intangibles · vacío = desconocido"),
             (F_DX, "D_X · amortización que f y el ancla tratan como reposición (perímetro efectivo)", "Calculada (no tocar)"),
             (F_EF, "Perímetro efectivo", "Calculado (no tocar)"))
    for r, a, b in filas:
        _estilo(ws[f"A{r}"], ws["A17"])
        _estilo(ws[f"B{r}"], ws["B17"])
        ws[f"A{r}"], ws[f"B{r}"] = a, b
        _estilo(ws[f"M{r}"], ws["M17"])
    _estilo(ws[f"C{F_SEL}"], ws["C17"])
    ws[f"C{F_SEL}"].number_format = "General"
    ws[f"D{F_SEL}"] = "A0_total · A1_sin_ROU (sin la D&A de derechos de uso) · A2_propio (sin la D&A de derechos de uso ni la PPA)"
    _estilo(ws[f"D{F_SEL}"], ws["A82"])
    ws.merge_cells(f"D{F_SEL}:L{F_SEL}")
    sel, ef = f"$C${F_SEL}", f"$C${F_EF}"
    ws[f"C{F_EF}"] = (f'=IF(OR({sel}="",{sel}="{PERIMETROS[0]}"),"{PERIMETROS[0]}",'
                      f'IF(OR({sel}="{PERIMETROS[1]}",{sel}="{PERIMETROS[2]}"),{sel},"no reconocido"))')
    _estilo(ws[f"C{F_EF}"], ws["C30"])
    ws[f"C{F_EF}"].number_format = "General"
    for x in COLS:
        _estilo(ws[f"{x}{F_ROU}"], ws[f"{x}17"])
        _estilo(ws[f"{x}{F_PPA}"], ws[f"{x}17"])
        _estilo(ws[f"{x}{F_DX}"], ws[f"{x}30"])
        ws[f"{x}{F_DX}"] = (f'=IF({ef}="{PERIMETROS[0]}",IF(ISNUMBER({x}8),{x}8,""),'
                            f'IF({ef}="{PERIMETROS[1]}",IF(AND(ISNUMBER({x}8),ISNUMBER({x}{F_ROU})),{x}8-{x}{F_ROU},""),'
                            f'IF({ef}="{PERIMETROS[2]}",IF(AND(ISNUMBER({x}8),ISNUMBER({x}{F_ROU}),ISNUMBER({x}{F_PPA})),{x}8-{x}{F_ROU}-{x}{F_PPA},""),"")))')
    _estilo(ws["A90"], ws["A82"])
    ws["A90"] = ("Con A0_total (o C85 vacío) la hoja calcula exactamente como la V6.3. Con A1_sin_ROU o A2_propio, la fila 30 (y con ella la 31), "
                 "f (C58), su conciliación (C76) y el ancla de S2C (C53) usan D_X en lugar de la D&A total; el terminal usa la misma f. "
                 "Las series publicadas (fila 8, FCF base, Análisis C46–C52) no cambian. Vacío no es cero: con A1/A2, una D&A de derechos de "
                 "uso o una PPA vacía en la ventana deja f vacía (Motor V05). R estimada (A3), N1 y los términos explícitos no están en el libro.")
    ws.merge_cells("A90:M90")
    ws.row_dimensions[90].height = 54
    # --- fila 30: capex − D_X + circulante
    for x in COLS:
        viejo = f'=IF(AND(ISNUMBER({x}12),ISNUMBER({x}8)),{x}12-{x}8+N({x}14),"")'
        assert ws[f"{x}30"].value == viejo, f"Historia {x}30 no es la de la V6.3"
        ws[f"{x}30"] = f'=IF(AND(ISNUMBER({x}12),ISNUMBER({x}{F_DX})),{x}12-{x}{F_DX}+N({x}14),"")'
    a0 = f'{ef}="{PERIMETROS[0]}"'
    reinv_v63 = f"SUMPRODUCT(--({VENTANA}),$C$12:$L$12-$C$8:$L$8+$C$14:$L$14)"
    reinv_dx = f"SUMPRODUCT(--({VENTANA}),$C$30:$L$30)"
    # --- C58 (f)
    f63 = ws["C58"].value
    assert f63.count(reinv_v63) == 1 and f63.startswith("=IF(OR(")
    chk8 = f'SUMPRODUCT(--({VENTANA}),--($C$8:$L$8=""))>0'
    assert f63.count(chk8) == 1
    f_dx = f63[1:].replace(reinv_v63, reinv_dx).replace(chk8, chk8 + f',SUMPRODUCT(--({VENTANA}),--($C${F_DX}:$L${F_DX}=""))>0')
    ws["C58"] = f"=IF({a0},{f63[1:]},{f_dx})"
    # --- C76 (reinversión neta media de la conciliación)
    c76 = ws["C76"].value
    assert c76 == f'=IF(NOT(ISNUMBER($C$58)),"",{reinv_v63}/$C$57)'
    ws["C76"] = f'=IF({a0},{c76[1:]},IF(NOT(ISNUMBER($C$58)),"",{reinv_dx}/$C$57))'
    # --- C53 (ancla de S2C, E4): con A1/A2 exige los cinco años H–L (vacío ≠ 0)
    c53 = ws["C53"].value
    assert c53 == '=IF(AND(ISNUMBER(L6),ISNUMBER(G6),COUNT(H31:L31)>=3),IF(SUM(H31:L31)>0,(L6-G6)/SUM(H31:L31),""),"")'
    ws["C53"] = f'=IF({a0},{c53[1:]},IF(COUNT($H$31:$L$31)<5,"",{c53[1:]}))'
    # --- validaciones de las entradas nuevas
    dv = DataValidation(type="list", formula1='"' + ",".join(PERIMETROS) + '"', allow_blank=True)
    dv.error, dv.errorTitle = "Perímetro F1: A0_total, A1_sin_ROU o A2_propio (vacío = A0_total).", "Perímetro F1"
    dv.add(f"C{F_SEL}")
    ws.add_data_validation(dv)
    dv2 = DataValidation(type="decimal", operator="greaterThanOrEqual", formula1="0", allow_blank=True)
    dv2.error, dv2.errorTitle = ("Amortización: magnitud no negativa (el cargo publicado entre paréntesis se escribe en positivo). Si es cero comprobado "
                                 "escribe 0; si no la conoces, deja la celda vacía."), "Importe no negativo"
    dv2.add(f"C{F_ROU}:L{F_PPA}")
    ws.add_data_validation(dv2)


def motor_v05(wb):
    ws = wb["Motor"]
    v = ws["E205"].value
    fin = 'IF(SUMPRODUCT(--(COLUMN(Historia!$C$6:$L$6)>12-Historia!$C$57),--(Historia!$C$14:$L$14=""))>0,"INC|Motor A: faltan aumento del circulante (fila 14) en algún año de la ventana que calibra f (Historia, últimos "&Historia!$C$57&" ejercicios); un hueco no vale cero",""'
    assert v.count(fin) == 1
    ef = f"Historia!$C${F_EF}"
    win = "COLUMN(Historia!$C$6:$L$6)>12-Historia!$C$57"
    nuevo = (fin[:-2]
             + f'IF({ef}="no reconocido","INV|Perímetro F1 de la reinversión (Historia C{F_SEL}) no reconocido: vacío, {PERIMETROS[0]}, {PERIMETROS[1]} o {PERIMETROS[2]}",'
             + f'IF(SUMPRODUCT(--({win}),--(Historia!$C${F_DX}:$L${F_DX}=""))>0,"INC|Motor A · perímetro "&{ef}&": falta la amortización de derechos de uso '
               f'(Historia fila {F_ROU}) o la PPA (fila {F_PPA}) en algún año de la ventana que calibra f; vacío no es cero",'
             + f'IF(SUMPRODUCT(--({win}),--(Historia!$C${F_DX}:$L${F_DX}<0))>0,"INV|Motor A · perímetro "&{ef}&": la amortización de derechos de uso más la PPA '
               f'supera la D&A total (fila 8) en algún año de la ventana","")))')
    ws["E205"] = v.replace(fin, nuevo)


def etiquetas(wb):
    cambios = {("Análisis", "A1"): ("— V6.3 ·", f"— {VERSION} ·"), ("Guía V6", "A1"): ("GUÍA V6.3 ·", f"GUÍA {VERSION} ·"),
               ("Panel", "A1"): ("DCF V6.3 ·", f"DCF {VERSION} ·"),
               ("Control maestro", "A3"): ("Versión V6.3 (30-oct-2026, cobertura completa de evidencias)",
                                           f"Versión {VERSION} (18-nov-2026, F1-IMPL: perímetro F1 de la reinversión del motor A, Historia C85:L89; "
                                           "sobre la V6.3 del 30-oct-2026, cobertura completa de evidencias)")}
    for (h, ref), (a, b) in cambios.items():
        v = wb[h][ref].value
        assert v.count(a) == 1, (h, ref)
        wb[h][ref].value = v.replace(a, b)
    return len(cambios)


def normalizar_paquete(path):
    z = zipfile.ZipFile(path)
    items = [(i, z.read(i.filename)) for i in z.infolist()]
    z.close()
    tmp = path + ".tmp"
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as out:
        for info, datos in items:
            if info.filename == "docProps/core.xml":
                datos = re.sub(rb"(<dcterms:modified[^>]*>)[^<]*(</dcterms:modified>)", rb"\g<1>2026-11-18T00:00:00Z\g<2>", datos)
                datos = re.sub(rb"(<dcterms:created[^>]*>)[^<]*(</dcterms:created>)", rb"\g<1>2026-11-18T00:00:00Z\g<2>", datos)
            ni = zipfile.ZipInfo(info.filename, date_time=FECHA_FIJA)
            ni.compress_type = zipfile.ZIP_DEFLATED
            ni.external_attr = info.external_attr
            out.writestr(ni, datos)
    os.replace(tmp, path)


def main(src, dst):
    wb = load_workbook(src)
    historia(wb)
    motor_v05(wb)
    n = etiquetas(wb)
    with tempfile.TemporaryDirectory() as tmp:
        mid = os.path.join(tmp, "v631.xlsx")
        wb.save(mid)
        restauradas = base.restaurar_partes(src, mid)
        subprocess.run([sys.executable, "-I", os.path.join(AQUI, "add_sliders.py"), mid, dst], check=True, capture_output=True)
    normalizar_paquete(dst)
    print(f"{VERSION}: perímetro F1 (Historia C85:L89), fila 30, C53, C58 y C76 con D_X, Motor E205; {n} etiquetas de versión; "
          f"partes restauradas {len(restauradas)} → {dst}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)
    main(sys.argv[1], sys.argv[2])
