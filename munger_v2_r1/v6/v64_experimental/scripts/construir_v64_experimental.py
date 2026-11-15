#!/usr/bin/env python3
"""Construye la plantilla V6.4 EXPERIMENTAL del motor B a partir de la V6.3 (que no se modifica).

Uso: python3 -I construir_v64_experimental.py Plantilla_V6.3.xlsx Plantilla_V6.4_experimental.xlsx

Capa nueva (encargo 4.11, §3–§6):
  - hoja «Configuración V6.4»: modo (Heredado o Experimental), N1 (tipo normalizado y escudo de la deuda), N2 (margen de
    partida manual), N3 (R0 o R1 con el circulante comercial), P-M1 (estructura H, S, SR1, SR2 o SRF; familia Λ o Θ;
    convenciones de los años y del terminal; ROIC del terminal; cartera de clientes legado o P0), bases históricas,
    parámetros efectivos, validez con su motivo y tabla de trazabilidad;
  - hoja «Conciliación B»: MALO, NORMAL y BUENO, años 1–10 y terminal, con la identidad FCF = NOPAT + D&A − inversión
    fija bruta − Δcirculante comprobada fila a fila contra el flujo del motor;
  - Motor: columnas nuevas BU:DY en las 124 filas de valoración (Δcirculante, inversión fija para crecer, requisito de
    reposición, crédito, flujo experimental y terminal); las fórmulas de flujo, terminal, valor sin crecimiento,
    reinversión del año 1 y ROIC marginal pasan a IF(experimental, nueva, HEREDADA LITERAL); la validez (BS) y el motivo
    (BT) incorporan la validez de la configuración;
  - Diagnóstico V6: C10 (m0), C11 (t aplicado a NOPAT), C15 (escudo de la deuda en r_op) y B176:D177 (transición al
    terminal) con el mismo patrón;
  - etiquetas de versión y una línea de configuración en Panel!B18:C18.
En modo heredado (B4 vacío o «Heredado») ninguna opción nueva interviene: las fórmulas efectivas son las de la V6.3.
Después: gráficos canónicos de la V6.3 (patch_v62_base.restaurar_partes), deslizadores (add_sliders.py, siempre al final) y
paquete determinista (fechas fijas), como en construir_v63.py.
"""
import os
import re
import subprocess
import sys
import tempfile
import zipfile
from copy import copy

from openpyxl import load_workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter as COL
from openpyxl.worksheet.datavalidation import DataValidation

AQUI = os.path.dirname(os.path.abspath(__file__))
V6 = os.path.abspath(os.path.join(AQUI, "..", ".."))
sys.path.insert(0, os.path.join(V6, "scripts"))
import patch_v62_base as base  # noqa: E402  (solo restaurar_partes)

FECHA_FIJA = (2026, 11, 12, 0, 0, 0)
CFG = "Configuración V6.4"
CON = "Conciliación B"
Q = "'" + CFG + "'!"          # prefijo de referencia a la hoja de configuración
VERSION = "V6.4 experimental"

# ------------------------------------------------------------------ opciones (texto exacto de las listas)
MODOS = ("Heredado", "Experimental")
CLASES = ("dato publicado", "derivado de datos publicados", "convención", "hipótesis")
ESCUDO = ("Vinculado al tipo aplicado a NOPAT", "Tipo de la Historia (separado)")
REGLAS = ("R0 · simétrica (heredada)", "R1 · solo circulante; capacidad conservada")
ESTRUCTURAS = ("Sin requisito adicional", "H · hueco (crédito de la inversión para crecer)", "S · suma sin reestimar",
               "SR1 · suma con S2C reestimado", "SR2 · suma con S2C y ROIC reestimados", "SRF · suma con inversión fija reestimada")
FAMILIAS = ("Λ · (λ − 1) × amortización que se repone", "Θ · θ × exceso histórico medio")
CONV_ANIOS = ("Plana", "Proporcional a las ventas")
CONV_TERM = ("Proporcional a las ventas", "Crece con g")
ROIC_T = ("ROIC de la fase B sin cambio", "ROIC × f (SR2)")
CARTERA = ("Legado · se repone con la amortización", "P0 · no se repone (explícito)")
CONFIANZAS = ("alta", "media", "baja")


def lista(opciones):
    return '"' + ",".join(opciones) + '"'


def ex(celda, texto):
    return f'EXACT({celda},"{texto}")'


def uno_de(celda, opciones):
    return "OR(" + ",".join(ex(celda, o) for o in opciones) + ")"


def vacia(celda):
    return f'LEN(TRIM({celda}&""))=0'


# ------------------------------------------------------------------ celdas efectivas de la configuración (absolutas)
C = {k: Q + v for k, v in {
    "modo": "$B$5", "valida": "$B$90", "motivo": "$B$91", "exp": "$B$76", "r1": "$B$77", "pm1": "$B$78", "h": "$B$79",
    "lam": "$B$80", "anios_v": "$B$81", "term_v": "$B$82", "nwc": "$B$83", "fs2c": "$B$84", "froic": "$B$85", "ffija": "$B$86",
    "lm1": "$B$87", "nivel": "$B$88", "rsg": "$B$89", "da0": "$B$54", "t_nopat": "$B$18", "t_escudo": "$B$19", "m0_man": "$B$21",
    "requisito": "$B$67", "resumen": "$B$9"}.items()}
CL_FILA = 93   # cartera no repuesta, años 1–10 en B93:K93


def cl(k):
    return f"{Q}${COL(1 + k)}${CL_FILA}"


# ------------------------------------------------------------------ 1. hoja de configuración
def hoja_configuracion(wb):
    ws = wb.create_sheet(CFG)
    titulo = Font(name="Arial", bold=True, size=12)
    negrita = Font(name="Arial", bold=True)
    normal = Font(name="Arial")
    entrada = PatternFill("solid", fgColor="FFF2CC")
    calculo = PatternFill("solid", fgColor="E7E6E6")
    ws.column_dimensions["A"].width = 62
    ws.column_dimensions["B"].width = 34
    for c in "CDEFG":
        ws.column_dimensions[c].width = 26
    filas = {}

    def put(ref, val, font=normal, fill=None):
        ws[ref] = val
        ws[ref].font = font
        ws[ref].alignment = Alignment(wrap_text=True, vertical="top")
        if fill:
            ws[ref].fill = fill

    def etiqueta(r, txt, b=None, es_entrada=False, nota=None):
        put(f"A{r}", txt)
        if b is not None:
            put(f"B{r}", b, fill=calculo)
        elif es_entrada:
            ws[f"B{r}"].fill = entrada
        if nota:
            put(f"C{r}", nota)

    put("A1", f"  CONFIGURACIÓN {VERSION.upper()} · motor B · qué supuestos están activos", titulo)
    put("A2", "Plantilla experimental (encargo 4.11). Nada de lo que se escribe aquí es una convención adoptada: son hipótesis o propuestas de un "
              "ensayo. En modo heredado (B4 vacío o «Heredado») ninguna opción de esta hoja interviene y el libro calcula como la V6.3. "
              "Vacío, cero y error son distintos: una celda vacía usa el mecanismo heredado solo donde se dice; un texto o número fuera de "
              "su dominio invalida la configuración (no se recorta ni se sustituye).")
    ws.merge_cells("A2:G2")
    ws.row_dimensions[2].height = 60
    # --- modo
    put("A3", "  1 · MODO", negrita)
    etiqueta(4, "Modo del motor B («Heredado» o «Experimental»; vacío = Heredado)", es_entrada=True,
             nota="Experimental: solo con el motor B (Análisis C62 = «No · financiación cambia mucho»).")
    etiqueta(5, "Modo efectivo", f'=IF({vacia("$B$4")},"Heredado",IF({ex("$B$4", "Heredado")},"Heredado",IF({ex("$B$4", "Experimental")},"Experimental","ERROR")))')
    etiqueta(6, "Motor de la empresa (Diagnóstico V6 C5)", "='Diagnóstico V6'!$C$5")
    etiqueta(7, "¿Configuración válida?", "=$B$90")
    etiqueta(8, "Motivo (primera comprobación que no cumple)", "=$B$91")
    etiqueta(9, "Supuestos activos (resumen)", None)
    etiqueta(10, "Aviso", None)
    # --- N1
    etiqueta(11, "2 · N1 · tipo normalizado aplicado a NOPAT (decimal; opcional; vacío = Historia C52)", es_entrada=True)
    ws["A11"].font = negrita
    etiqueta(12, "  N1 · fuente", es_entrada=True)
    etiqueta(13, "  N1 · período", es_entrada=True)
    etiqueta(14, "  N1 · perímetro", es_entrada=True)
    etiqueta(15, "  N1 · clase", es_entrada=True, nota=" · ".join(CLASES))
    etiqueta(16, "  N1 · escudo de la deuda en r_op (obligatorio si hay tipo normalizado)", es_entrada=True, nota=" · ".join(ESCUDO))
    etiqueta(17, "Tipo de la Historia (Historia C52, media de 5 años)", "=Historia!$C$52")
    etiqueta(18, "Tipo aplicado a NOPAT (años 1–10 y terminal; Diagnóstico V6 C11)", f'=IF(AND($B$76,ISNUMBER($B$11)),$B$11,Historia!$C$52)')
    etiqueta(19, "Tipo del escudo de la deuda en r_op (Diagnóstico V6 C15)",
             f'=IF(AND($B$76,ISNUMBER($B$11),{ex("$B$16", ESCUDO[1])}),Historia!$C$52,$B$18)')
    put("C19", "La configuración de compatibilidad conserva el vínculo de la V6.3: el mismo tipo en NOPAT y en el escudo. Separarlos es una alternativa declarada.")
    # --- N2
    put("A20", "  3 · N2 · MARGEN EBIT DE PARTIDA (opcional; vacío = Palancas C8)", negrita)
    etiqueta(21, "N2 · margen EBIT de partida manual (decimal; vacío = regla de Palancas C8)", es_entrada=True)
    etiqueta(22, "  N2 · perímetro", es_entrada=True)
    etiqueta(23, "  N2 · procedencia (archivo, cálculo, período)", es_entrada=True)
    etiqueta(24, "Margen de partida heredado (Palancas C8: último año o media del ciclo)", '=IF(Palancas!$C8="Media del ciclo",Historia!$C$49,Historia!$C$48)')
    etiqueta(25, "Margen de partida aplicado (m0; Diagnóstico V6 C10)", "=IF(AND($B$76,ISNUMBER($B$21)),$B$21,$B$24)")
    put("A26", "El margen de partida (m0, año 0) no es el margen objetivo del NORMAL (Palancas C15, que se alcanza en el año 5): son conceptos distintos.")
    # --- N3
    put("A27", "  4 · N3 · REINVERSIÓN CON VENTAS QUE CAEN (obligatoria en modo experimental)", negrita)
    etiqueta(28, "N3 · regla", es_entrada=True, nota=" · ".join(REGLAS))
    etiqueta(29, "  circulante comercial · existencias del último año (mm)", es_entrada=True)
    etiqueta(30, "  circulante comercial · deudores comerciales y otros (mm)", es_entrada=True)
    etiqueta(31, "  circulante comercial · acreedores comerciales y otros (mm)", es_entrada=True)
    etiqueta(32, "  circulante comercial · fuente y fecha", es_entrada=True)
    etiqueta(33, "Circulante comercial ÷ ventas del último año (Historia C44)",
             '=IF(AND(ISNUMBER($B$29),ISNUMBER($B$30),ISNUMBER($B$31),ISNUMBER(Historia!$C$44)),IF(Historia!$C$44>0,($B$29+$B$30-$B$31)/Historia!$C$44,""),"")')
    etiqueta(34, "Regla efectiva", f'=IF($B$76,IF({ex("$B$28", REGLAS[1])},"R1","R0"),"R0 (heredada)")')
    put("C34", "R0: ΔV ÷ S2C en las dos direcciones (libera capital fijo al caer). R1: al caer solo se libera circulante; al recuperar por debajo del máximo conservado se repone circulante; por encima del máximo, ΔV ÷ S2C completo. Que la regla cuadre no demuestra que la capacidad se conserve.")
    # --- P-M1
    put("A35", "  5 · P-M1 · REPOSICIÓN Y CRECIMIENTO (obligatoria en modo experimental; ninguna estructura es central por defecto)", negrita)
    etiqueta(36, "P-M1 · estructura", es_entrada=True, nota=" · ".join(ESTRUCTURAS))
    etiqueta(37, "  familia del requisito adicional", es_entrada=True, nota=" · ".join(FAMILIAS))
    etiqueta(38, "  λ (reposición ÷ amortización que se repone; ≥ 1; hipótesis, no medición)", es_entrada=True)
    etiqueta(39, "  θ (fracción del exceso histórico que fue reposición; 0–1; hipótesis)", es_entrada=True)
    etiqueta(40, "  convención del requisito en los años 1–10", es_entrada=True, nota=" · ".join(CONV_ANIOS))
    etiqueta(41, "  convención del requisito en el terminal", es_entrada=True, nota=" · ".join(CONV_TERM))
    etiqueta(42, "  ROIC del terminal", es_entrada=True, nota=" · ".join(ROIC_T))
    etiqueta(43, "  amortización de la cartera de clientes", es_entrada=True, nota=" · ".join(CARTERA))
    etiqueta(44, "  P0 · amortización anual prevista de la cartera (mm)", es_entrada=True)
    etiqueta(45, "  P0 · valor neto contable de la cartera al cierre (mm)", es_entrada=True)
    for i, col in enumerate("HIJKL"):
        etiqueta(46 + i, f'="  P0 · amortización de la cartera del año "&IF(ISNUMBER(Historia!${col}$5),Historia!${col}$5,"(Historia {col})")&" (mm; 0 explícito si no la hubo)"', es_entrada=True)
    etiqueta(51, "  P0 · fuente de la cartera", es_entrada=True)
    put("C38", "Λ: requisito = (λ − 1) × amortización que se repone (sin la cartera con P0); Rh histórico con la misma definición.")
    put("C39", "Θ: requisito = θ × exceso histórico medio (H–L); Rh = θ × exceso histórico acumulado.")
    # --- bases históricas
    put("A53", "  6 · BASES HISTÓRICAS (Historia, columnas H–L: los cinco años del S2C marginal C53)", negrita)
    etiqueta(54, "Amortización del último año (D&A₀, Historia L8)", "=Historia!$L$8")
    etiqueta(55, "Σ reinversión neta total H–L (Historia H31:L31, denominador de C53)", "=SUM(Historia!$H$31:$L$31)")
    etiqueta(56, "Σ amortización de la cartera H–L (P0; 0 con legado)", "=IF($B$66,SUM($B$46:$B$50),0)")
    etiqueta(57, "D_hist · reinversión neta frente a la amortización que se repone", "=$B$55+$B$56")
    etiqueta(58, "Σ (capex − D&A) H–L", "=SUM(Historia!$H$12:$L$12)-SUM(Historia!$H$8:$L$8)")
    etiqueta(59, "Σ adquisiciones netas H–L (Historia H13:L13)", "=SUM(Historia!$H$13:$L$13)")
    etiqueta(60, "Exceso histórico acumulado sobre la amortización que se repone", "=$B$58+$B$56")
    etiqueta(61, "Exceso histórico medio (÷ 5)", "=$B$60/5")
    etiqueta(62, "F_hist · inversión fija neta histórica frente a la amortización que se repone, con adquisiciones", "=$B$60+$B$59")
    etiqueta(63, "Σ amortización que se repone H–L", "=SUM(Historia!$H$8:$L$8)-$B$56")
    put("C57", "D_hist no es la deuda del puente: es la reinversión histórica con la que se mide el S2C de referencia.")
    # --- derivados (sin depender de la validez)
    put("A65", "  7 · DERIVADOS DE LA CONFIGURACIÓN", negrita)
    etiqueta(66, "¿P0 explícito?", f"={ex('$B$43', CARTERA[1])}")
    etiqueta(67, "¿Requisito adicional? (estructura distinta de «Sin requisito adicional»)", f"=AND(ISTEXT($B$36),NOT({ex('$B$36', ESTRUCTURAS[0])}))")
    etiqueta(68, "¿Familia Λ?", f"={ex('$B$37', FAMILIAS[0])}")
    etiqueta(69, "Código de la estructura", '=IF($B$67,IFERROR(LEFT($B$36,FIND(" ",$B$36)-1),"?"),"—")')
    etiqueta(70, "Requisito a ventas constantes (nivel anual, M€)",
             "=IF($B$67,IF($B$68,IF(ISNUMBER($B$38),($B$38-1)*$B$54,0),IF(ISNUMBER($B$39),$B$39*$B$61,0)),0)")
    etiqueta(71, "Rh · parte de D_hist atribuida a reposición",
             "=IF($B$67,IF($B$68,IF(ISNUMBER($B$38),($B$38-1)*$B$63,0),IF(ISNUMBER($B$39),$B$39*$B$60,0)),0)")
    etiqueta(72, "f = D_hist ÷ (D_hist − Rh) (SR1, SR2)",
             '=IF(AND($B$67,OR($B$69="SR1",$B$69="SR2"),ISNUMBER($B$57)),IF(AND($B$57>0,$B$57-$B$71>0),$B$57/($B$57-$B$71),""),1)')
    etiqueta(73, "f_fija = 1 − Rh ÷ F_hist (SRF)",
             '=IF(AND($B$67,$B$69="SRF",ISNUMBER($B$62)),IF($B$62>0,1-$B$71/$B$62,""),1)')
    put("A75", "  8 · PARÁMETROS EFECTIVOS QUE LEE EL MOTOR (no tocar)", negrita)
    etiqueta(76, "EXPERIMENTAL ACTIVO Y VÁLIDO", '=AND($B$5="Experimental",$B$90)')
    etiqueta(77, "R1 activa", f"=AND($B$76,{ex('$B$28', REGLAS[1])})")
    etiqueta(78, "P-M1 activa (requisito adicional o P0)", "=AND($B$76,OR($B$67,$B$66))")
    etiqueta(79, "Estructura H (crédito)", '=AND($B$78,$B$69="H")')
    etiqueta(80, "Familia Λ activa", "=AND($B$78,$B$67,$B$68)")
    etiqueta(81, "Requisito proporcional a las ventas en los años 1–10", f"=AND($B$78,$B$67,{ex('$B$40', CONV_ANIOS[1])})")
    etiqueta(82, "Requisito proporcional a las ventas en el terminal", f"=AND($B$78,$B$67,{ex('$B$41', CONV_TERM[0])})")
    etiqueta(83, "Circulante comercial ÷ ventas efectivo (0 = sin desglose)", "=IF(AND($B$76,ISNUMBER($B$33)),$B$33,0)")
    etiqueta(84, "Factor del S2C de los años 1–10 (SR1, SR2)", '=IF(AND($B$78,OR($B$69="SR1",$B$69="SR2")),$B$72,1)')
    etiqueta(85, "Factor del ROIC del terminal (SR2)", '=IF(AND($B$78,$B$69="SR2"),$B$72,1)')
    etiqueta(86, "Factor de la inversión fija para crecer (SRF)", '=IF(AND($B$78,$B$69="SRF"),$B$73,1)')
    etiqueta(87, "λ − 1 efectivo", "=IF($B$80,$B$38-1,0)")
    etiqueta(88, "Nivel Θ efectivo (M€/año)", "=IF(AND($B$78,$B$67,NOT($B$68)),$B$39*$B$61,0)")
    etiqueta(89, "Requisito a ventas constantes efectivo (valor sin crecimiento)", "=IF(AND($B$78,$B$67),$B$70,0)")
    etiqueta(90, "Configuración válida (todas las comprobaciones de §9 cumplen)", "=COUNTIF($B$96:$B$124,TRUE)=0")
    etiqueta(91, "Motivo", '=IFERROR(INDEX($C$96:$C$124,MATCH(TRUE,$B$96:$B$124,0)),"")')
    put("A92", "Cartera de clientes no repuesta por año (P0; años 1–10)", negrita)
    put("A93", "Cartera no repuesta (M€)")
    for k in range(1, 11):
        put(f"{COL(1 + k)}92", k, negrita)
        put(f"{COL(1 + k)}{CL_FILA}", f"=IF(AND($B$78,$B$66),MIN($B$44,MAX(0,$B$45-$B$44*{k - 1})),0)", fill=calculo)
    # --- comprobaciones
    put("A95", "  9 · COMPROBACIONES (TRUE = no cumple; la primera da el motivo)", negrita)
    put("B95", "¿No cumple?", negrita)
    put("C95", "Motivo", negrita)
    E = '$B$5="Experimental"'
    est_ok = uno_de("$B$36", ESTRUCTURAS)
    reglas = [
        ('$B$5="ERROR"', "Modo no reconocido en B4: escribe «Heredado» o «Experimental» (vacío = Heredado)"),
        (f'AND({E},$B$6<>"B")', '="La configuración experimental V6.4 solo es aplicable al motor B; el motor elegido es «"&$B$6&"» (vuelve al modo Heredado o revisa Análisis C62)"'),
        (f"AND({E},NOT(OR({vacia('$B$11')},AND(ISNUMBER($B$11),$B$11>=0,$B$11<1))))", "N1: el tipo normalizado debe ser un número entre 0 y 1, o quedar vacío"),
        (f"AND({E},ISNUMBER($B$11),OR({vacia('$B$12')},{vacia('$B$13')},{vacia('$B$14')},NOT({uno_de('$B$15', CLASES)})))", "N1: faltan la fuente, el período, el perímetro o la clase del tipo normalizado"),
        (f"AND({E},ISNUMBER($B$11),NOT({uno_de('$B$16', ESCUDO)}))", "N1: elige el tratamiento del escudo de la deuda (vinculado al tipo aplicado o tipo de la Historia)"),
        (f"AND({E},NOT(OR({vacia('$B$21')},AND(ISNUMBER($B$21),$B$21>-1,$B$21<1))))", "N2: el margen de partida debe ser un número entre −1 y 1, o quedar vacío"),
        (f"AND({E},ISNUMBER($B$21),OR({vacia('$B$22')},{vacia('$B$23')}))", "N2: faltan el perímetro o la procedencia del margen de partida"),
        (f"AND({E},NOT({uno_de('$B$28', REGLAS)}))", "N3: elige la regla de reinversión (R0 o R1); en modo experimental no se toma ninguna por defecto"),
        (f"AND({E},{ex('$B$28', REGLAS[1])},NOT(ISNUMBER($B$33)))", "N3 · R1: faltan existencias, deudores o acreedores del último año (circulante comercial)"),
        (f"AND({E},ISNUMBER($B$33),OR($B$29<0,$B$30<0,$B$31<0))", "N3: los importes del circulante comercial no pueden ser negativos"),
        (f"AND({E},NOT({est_ok}))", "P-M1: elige la estructura (o «Sin requisito adicional»); en modo experimental no hay estructura por defecto"),
        (f"AND({E},NOT({uno_de('$B$43', CARTERA)}))", "P-M1: elige el tratamiento de la cartera de clientes (legado o P0 explícito)"),
        (f"AND({E},OR($B$67,$B$66),NOT({ex('$B$28', REGLAS[1])}))", "R0 + P-M1 no está especificado (las estructuras de reposición parten de R1): elige R1 o quita P-M1"),
        (f"AND({E},$B$67,NOT({uno_de('$B$37', FAMILIAS)}))", "P-M1: elige la familia del requisito adicional (Λ o Θ)"),
        (f"AND({E},$B$67,$B$68,NOT(AND(ISNUMBER($B$38),$B$38>=1)))", "P-M1 · Λ: λ debe ser un número ≥ 1"),
        (f"AND({E},$B$67,{ex('$B$37', FAMILIAS[1])},NOT(AND(ISNUMBER($B$39),$B$39>=0,$B$39<=1)))", "P-M1 · Θ: θ debe ser un número entre 0 y 1"),
        (f"AND({E},$B$67,NOT({uno_de('$B$40', CONV_ANIOS)}))", "P-M1: elige la convención del requisito en los años 1–10"),
        (f"AND({E},$B$67,NOT({uno_de('$B$41', CONV_TERM)}))", "P-M1: elige la convención del requisito en el terminal"),
        (f'AND({E},$B$67,NOT(OR(AND($B$69="SR2",{ex("$B$42", ROIC_T[1])}),AND($B$69<>"SR2",{ex("$B$42", ROIC_T[0])}))))',
         "P-M1: el ROIC del terminal debe ser «× f» en SR2 y «sin cambio» en las demás estructuras"),
        (f"AND({E},$B$66,NOT(AND(ISNUMBER($B$44),ISNUMBER($B$45),COUNT($B$46:$B$50)=5)))", "P0: faltan la amortización anual, el valor neto o la amortización histórica de la cartera (cinco años; 0 explícito si no la hubo)"),
        (f"AND({E},$B$66,COUNT($B$44:$B$50)=7,OR($B$44<0,$B$45<0,MIN($B$46:$B$50)<0))", "P0: los importes de la cartera no pueden ser negativos"),
        (f"AND({E},$B$66,ISNUMBER($B$44),ISNUMBER($B$45),$B$45>10*$B$44)", "P0: la cartera no se agota en diez años (valor neto > 10 × amortización anual): el terminal no la representa"),
        (f"AND({E},OR($B$67,$B$66),OR(COUNT(Historia!$H$31:$L$31)<5,COUNT(Historia!$H$12:$L$12)<5,COUNT(Historia!$H$8:$L$8)<5))", "P-M1: faltan bases históricas de los cinco años H–L (reinversión neta, capex o amortización)"),
        (f'AND({E},$B$67,OR($B$69="SR1",$B$69="SR2"),NOT(ISNUMBER($B$72)))', "P-M1 · SR1/SR2: D_hist ≤ 0 o D_hist − Rh ≤ 0: el factor f no está definido"),
        (f'AND({E},$B$67,$B$69="SRF",NOT(AND(ISNUMBER($B$73),$B$73>=0)))', "P-M1 · SRF: F_hist ≤ 0 o Rh > F_hist: el factor de la inversión fija queda fuera de [0, 1]"),
        (f"AND({E},$B$67,$B$70<0)", "P-M1: el requisito a ventas constantes es negativo (exceso histórico medio < 0): fuera del dominio declarado"),
        (f"AND({E},$B$67,$B$68,$B$66,ISNUMBER($B$44),$B$44>$B$54)", "P-M1 · Λ con P0: la amortización de la cartera supera la amortización total"),
        (f"AND({E},NOT(ISNUMBER(Historia!$L$8)))", "Modo experimental: falta la amortización del último año (Historia L8)"),
    ]
    for i, (cond, msg) in enumerate(reglas):
        r = 96 + i
        put(f"A{r}", f"Comprobación {i + 1}")
        put(f"B{r}", f"=IFERROR({cond},TRUE)", fill=calculo)
        put(f"C{r}", msg)
        ws.merge_cells(f"C{r}:G{r}")
    assert 96 + len(reglas) - 1 <= 124
    # resumen y aviso (después de definir todo)
    ws["B9"] = ('=IF($B$5="Heredado","Modo heredado: reinversión ΔV ÷ S2C simétrica; reposición = amortización (límite declarado de la V6.3); tipo de la Historia; margen de partida de Palancas C8",'
                'IF(NOT($B$90),"Configuración no válida: "&$B$91,'
                '"Experimental · t NOPAT "&FIXED(100*$B$18,2)&" % · escudo "&FIXED(100*$B$19,2)&" % · m0 "&FIXED(100*$B$25,2)&" %"&IF(ISNUMBER($B$21)," (manual)"," (Palancas C8)")'
                '&" · "&$B$34&IF($B$77," (circulante "&FIXED(100*$B$83,2)&" % de las ventas)","")'
                '&" · P-M1: "&IF($B$67,$B$69&" · "&IF($B$68,"Λ = "&FIXED($B$38,3),"θ = "&FIXED($B$39,3))&" · años "&$B$40&" · terminal "&$B$41&" · f "&FIXED($B$84,4)&" · f_fija "&FIXED($B$86,4),"sin requisito adicional")'
                '&IF($B$66," · P0 (cartera no repuesta)"," · cartera: legado")))')
    ws["B9"].fill = calculo
    ws["B10"] = ('=IF(AND($B$5="Heredado",COUNTA($B$11:$B$16,$B$21:$B$23,$B$28:$B$32,$B$36:$B$51)>0),'
                 '"Aviso: hay opciones experimentales escritas que el modo heredado ignora (no se arrastran)","")')
    ws["B10"].fill = calculo
    ws.merge_cells("B9:G9")
    ws.row_dimensions[9].height = 48
    # --- trazabilidad
    put("A127", "  10 · TRAZABILIDAD DE LOS PARÁMETROS (las escribe la orquestación desde la configuración económica del expediente)", negrita)
    for c, t in zip("ABCDEFG", ("Parámetro", "Valor efectivo", "Clase", "Confianza", "Fuente o condición", "Justificación", "Materialidad")):
        put(f"{c}128", t, negrita)
    traz = [
        ("N1 · tipo aplicado a NOPAT", "=$B$18"), ("N1 · tipo del escudo de la deuda", "=$B$19"), ("N2 · margen de partida (m0)", "=$B$25"),
        ("N3 · regla de reinversión", "=$B$34"), ("N3 · circulante comercial ÷ ventas", "=$B$83"),
        ("P-M1 · estructura", "=$B$69"), ("P-M1 · familia", '=IF($B$67,IF($B$68,"Λ","Θ"),"—")'), ("P-M1 · λ o θ", '=IF($B$80,$B$38,IF(AND($B$78,$B$67),$B$39,"—"))'),
        ("P-M1 · convención de los años", '=IF($B$67,$B$40,"—")'), ("P-M1 · convención del terminal", '=IF($B$67,$B$41,"—")'),
        ("P-M1 · ROIC del terminal", '=IF($B$67,$B$42,"—")'), ("P-M1 · cartera de clientes", '=IF($B$66,"P0","legado")'), ("Modo", "=$B$5"),
    ]
    activa = ["ISNUMBER($B$11)", "ISNUMBER($B$11)", "ISNUMBER($B$21)", "TRUE", ex("$B$28", REGLAS[1]),
              "TRUE", "$B$67", "$B$67", "$B$67", "$B$67", "$B$67", "TRUE", "TRUE"]
    put("H128", "¿Activo?", negrita)
    put("I128", "¿Falta traza?", negrita)
    for i, (p, f) in enumerate(traz):
        r = 129 + i
        put(f"A{r}", p)
        put(f"B{r}", f, fill=calculo)
        for c in "CDEFG":
            ws[f"{c}{r}"].fill = entrada
        put(f"H{r}", f'=AND($B$5="Experimental",{activa[i]})', fill=calculo)
        put(f"I{r}", f"=IF(AND($H{r},COUNTBLANK($C{r}:$G{r})>0),1,0)", fill=calculo)
    assert 129 + len(traz) - 1 == 141
    put("A143", "Trazabilidad de los parámetros ACTIVOS (clase, confianza, fuente o condición, justificación y materialidad)", negrita)
    put("B143", '=IF($B$5<>"Experimental","no aplica (modo heredado)",IF(SUM($I$129:$I$141)=0,"completa","INCOMPLETA: "&SUM($I$129:$I$141)&" parámetros activos sin traza completa (C:G)"))', fill=calculo)
    # validaciones de datos (listas)
    for ref, ops in (("B4", MODOS), ("B15", CLASES), ("B16", ESCUDO), ("B28", REGLAS), ("B36", ESTRUCTURAS), ("B37", FAMILIAS),
                     ("B40", CONV_ANIOS), ("B41", CONV_TERM), ("B42", ROIC_T), ("B43", CARTERA)):
        dv = DataValidation(type="list", formula1=lista(ops), allow_blank=True)
        dv.add(ref)
        ws.add_data_validation(dv)
    dv = DataValidation(type="list", formula1=lista(CLASES), allow_blank=True)
    dv.add("C129:C141")
    ws.add_data_validation(dv)
    dv = DataValidation(type="list", formula1=lista(CONFIANZAS), allow_blank=True)
    dv.add("D129:D141")
    ws.add_data_validation(dv)
    ws.freeze_panes = "B4"
    return ws, len(reglas)


# ------------------------------------------------------------------ 2. motor
NUEVAS = {"dc": 73, "fi": 83, "rq": 93, "cr": 103, "fx": 113}   # bloques de 10 columnas: BU, CE, CO, CY, DI
T = {"nopat": 123, "dc": 124, "fi": 125, "rq": 126, "cr": 127, "fx": 128, "flag": 129}   # DS … DY


def letra(c):
    return COL(c)


def L_t(t):
    return letra(26 + t)   # AA … AJ


def m_t(t):
    return letra(36 + t)   # AK … AT


def motor(wb):
    ws = wb["Motor"]
    filas = [r for r in range(1, ws.max_row + 1) if isinstance(ws.cell(r, 47).value, str) and ws.cell(r, 47).value.startswith("=")]
    assert len(filas) == 124, len(filas)
    # cabeceras
    nombres = {"dc": "Δcirc_t", "fi": "Fija crecer_t", "rq": "Requisito_t", "cr": "Crédito_t", "fx": "Flujo exp_t"}
    cab = ws["BT4"]
    for k, c0 in NUEVAS.items():
        for t in range(1, 11):
            ws.cell(3, c0 + t - 1, t)
            ws.cell(4, c0 + t - 1, f"{nombres[k]} {t}")
            ws.cell(4, c0 + t - 1)._style = copy(cab._style)
            ws.column_dimensions[letra(c0 + t - 1)].width = 12
    for k, txt in (("nopat", "NOPAT 11"), ("dc", "Δcirc 11"), ("fi", "Fija crecer 11"), ("rq", "Requisito 11"), ("cr", "Crédito 11"), ("fx", "Flujo exp 11"), ("flag", "Fila V6.4 (B)")):
        ws.cell(4, T[k], txt)
        ws.cell(4, T[k])._style = copy(cab._style)
        ws.column_dimensions[letra(T[k])].width = 12
    ws.cell(2, 73, "V6.4 EXPERIMENTAL · motor B · columnas BU:DY (se calculan con el motor B también en modo heredado, con R0 y sin P-M1, para la conciliación; "
                   "el flujo que usa la fila es el heredado salvo con «Configuración V6.4»!B76 = VERDADERO)")
    cambiadas = 0
    for r in filas:
        flag = f"$DY{r}"
        ws.cell(r, T["flag"], f'=AND($BS{r},$B{r}="B")')
        for t in range(1, 11):
            Lt, Lp = f"{L_t(t)}{r}", (f"$C{r}" if t == 1 else f"{L_t(t - 1)}{r}")
            pico = f"$C{r}" if t == 1 else f"MAX($C{r},$AA{r}:{L_t(t - 1)}{r})"
            dc = f"{letra(NUEVAS['dc'] + t - 1)}{r}"
            fi = f"{letra(NUEVAS['fi'] + t - 1)}{r}"
            rq = f"{letra(NUEVAS['rq'] + t - 1)}{r}"
            cr = f"{letra(NUEVAS['cr'] + t - 1)}{r}"
            fx = f"{letra(NUEVAS['fx'] + t - 1)}{r}"
            ws[dc] = f'=IF({flag},({Lt}-{Lp})*{C["nwc"]},"")'
            ws[fi] = (f'=IF({flag},IF({C["r1"]},MAX(0,{Lt}-{pico})*(1/($G{r}*{C["fs2c"]})-{C["nwc"]})*{C["ffija"]},'
                      f'({Lt}-{Lp})*(1/$G{r}-{C["nwc"]})),"")')
            ws[rq] = (f'=IF({flag},IF({C["pm1"]},IF({C["lam"]},{C["lm1"]}*({C["da0"]}*IF({C["anios_v"]},{Lt}/$C{r},1)-{cl(t)}),'
                      f'{C["nivel"]}*IF({C["anios_v"]},{Lt}/$C{r},1)),0),"")')
            ws[cr] = f'=IF({flag},IF({C["h"]},MIN({rq},MAX(0,{fi})),0),"")'
            ws[fx] = f'=IF({flag},{Lt}*{m_t(t)}{r}*(1-$K{r})+{cl(t)}-{fi}-{dc}-{rq}+{cr},"")'
            # flujo de la fila: IF(experimental, nuevo, heredado literal)
            au = ws.cell(r, 46 + t)
            viejo = au.value
            pre = f"=IF($BS{r},"
            assert viejo.startswith(pre) and viejo.endswith(',"")'), viejo
            inner = viejo[len(pre):-len(',"")')]
            au.value = f'=IF($BS{r},IF({C["exp"]},{fx},{inner}),"")'
            cambiadas += 1
        ns, nd, nf, nr, nc, nx = (f"{letra(T[k])}{r}" for k in ("nopat", "dc", "fi", "rq", "cr", "fx"))
        ws[ns] = f'=IF({flag},$AJ{r}*(1+$H{r})*$F{r}*(1-$K{r}),"")'
        ws[nd] = f'=IF({flag},$AJ{r}*$H{r}*{C["nwc"]},"")'
        ws[nf] = f'=IF({flag},({ns}*$H{r}/($I{r}*{C["froic"]})-{nd})*{C["ffija"]},"")'
        ws[nr] = (f'=IF({flag},IF(AND({C["pm1"]},{C["requisito"]}),IF({C["lam"]},{C["lm1"]}*{C["da0"]},{C["nivel"]})'
                  f'*IF({C["term_v"]},$AJ{r}*(1+$H{r})/$C{r},1+$H{r}),0),"")')
        ws[nc] = f'=IF({flag},IF({C["h"]},MIN({nr},MAX(0,{nf})),0),"")'
        ws[nx] = f'=IF({flag},{ns}-{nf}-{nd}-{nr}+{nc},"")'
        # terminal BF
        bf = ws[f"BF{r}"]
        pre = f"=IF($BS{r},"
        assert bf.value.startswith(pre) and bf.value.endswith(',"")')
        bf.value = f'=IF($BS{r},IF({C["exp"]},{nx},{bf.value[len(pre):-len(chr(44) + chr(34) * 2 + ")")]}),"")'
        # valor sin crecimiento BL
        bl = ws[f"BL{r}"]
        assert bl.value.startswith(pre) and bl.value.endswith(',"")')
        bl.value = (f'=IF($BS{r},IF({C["exp"]},$C{r}*$D{r}*(1-$K{r})/$J{r}-{C["rsg"]}/$J{r}+$M{r},'
                    f'{bl.value[len(pre):-len(chr(44) + chr(34) * 2 + ")")]}),"")')
        # reinversión del año 1 BP
        bp = ws[f"BP{r}"]
        pre_bp = f"=IF($BS{r},IFERROR("
        assert bp.value.startswith(pre_bp) and bp.value.endswith(',""),"")'), bp.value
        inner = bp.value[len(pre_bp):-len(',""),"")')]
        bp.value = f'=IF($BS{r},IFERROR(IF({C["exp"]},(AA{r}*AK{r}*(1-$K{r})-AU{r})/(AA{r}*AK{r}*(1-$K{r})),{inner}),""),"")'
        # ROIC marginal BQ
        bq = ws[f"BQ{r}"]
        esperado = f'=IF(AND($BS{r},$B{r}<>"C"),$F{r}*(1-$K{r})*$G{r},"")'
        assert bq.value == esperado, bq.value
        bq.value = (f'=IF(AND($BS{r},$B{r}<>"C"),IF({C["exp"]},$F{r}*(1-$K{r})/({C["nwc"]}+(1/($G{r}*{C["fs2c"]})-{C["nwc"]})*{C["ffija"]}),'
                    f'$F{r}*(1-$K{r})*$G{r}),"")')
        # validez BS y motivo BT
        bs = ws[f"BS{r}"]
        assert bs.value.startswith("=AND(") and bs.value.endswith(")")
        bs.value = bs.value[:-1] + f",{C['valida']})"
        bt = ws[f"BT{r}"]
        pre_bt = f'=IF($BS{r},"",'
        assert bt.value.startswith(pre_bt) and bt.value.endswith(")")
        bt.value = f'=IF($BS{r},"",IF(NOT({C["valida"]}),"Configuración V6.4: "&{C["motivo"]},{bt.value[len(pre_bt):-1]}))'
    return filas, cambiadas


# ------------------------------------------------------------------ 3. diagnóstico
def diagnostico(wb):
    ws = wb["Diagnóstico V6"]
    assert ws["C10"].value == '=IF(Palancas!$C8="Media del ciclo",Historia!$C$49,Historia!$C$48)'
    ws["C10"] = f'=IF(AND({C["exp"]},ISNUMBER({C["m0_man"]})),{C["m0_man"]},IF(Palancas!$C8="Media del ciclo",Historia!$C$49,Historia!$C$48))'
    assert ws["C11"].value == "=Historia!$C$52"
    ws["C11"] = f'=IF({C["exp"]},{C["t_nopat"]},Historia!$C$52)'
    v = ws["C15"].value
    assert v.count("(1-N($C11))") == 1
    ws["C15"] = v.replace("(1-N($C11))", f"(1-N(IF({C['exp']},{C['t_escudo']},$C11)))")
    ws["E10"] = "V6.4: en modo experimental, «Configuración V6.4» B21 si se informa (N2)."
    ws["E11"] = "Media de 5 años. V6.4: en modo experimental, el tipo normalizado de «Configuración V6.4» B11 si se informa (N1)."
    for col, fila in zip("BCD", (6, 7, 8)):
        v = ws[f"{col}176"].value
        ws[f"{col}176"] = f'=IF({C["exp"]},IF(ISNUMBER(Motor!BQ{fila}),Motor!BQ{fila},""),{v[1:]})'
        v = ws[f"{col}177"].value
        ws[f"{col}177"] = (f'=IF({C["exp"]},IFERROR(Motor!DS{fila}*Motor!H{fila}/(Motor!DU{fila}+Motor!DT{fila}),""),{v[1:]})')
    ws["E176"] = "V6.4 experimental: rentabilidad marginal efectiva del crecimiento (Motor BQ, con el circulante y los factores de la estructura)."
    ws["E177"] = "V6.4 experimental: ROIC efectivo del crecimiento terminal = NOPAT₁₁ × g ÷ (inversión fija para crecer + Δcirculante) del año 11."


# ------------------------------------------------------------------ 4. conciliación
ITEMS = ["Año", "Ventas", "Máximo de ventas conservado antes del año", "Margen EBIT", "NOPAT = ventas × margen × (1 − t)",
         "Amortización (D&A)", "Cartera de clientes no repuesta (P0)", "Reposición contable = D&A − cartera",
         "Requisito de reposición adicional", "Inversión fija para crecer", "Crédito: la misma inversión cumple las dos funciones (solo H)",
         "Reposición adicional pagada = requisito − crédito", "Δ circulante", "Inversión fija bruta = reposición contable + fija para crecer + adicional pagada",
         "Inversión total = inversión fija bruta + Δ circulante", "FCF por la identidad = NOPAT + D&A − inversión fija bruta − Δ circulante",
         "FCF que usa el motor (Motor AU:BD y BF)", "Diferencia (identidad − motor)", "Factor de descuento (terminal: ÷ (r − g) y 10 años)",
         "Valor presente", "Σ VP años 1–10 · motor · diferencia · VP terminal · motor · diferencia", "Peso del terminal (Motor BN)",
         "Salto año 10 → terminal: requisito · FCF · ventas (variación)", "S2C efectivo del crecimiento (años) · ROIC efectivo del crecimiento terminal",
         "Comprobación de la fila"]


def conciliacion(wb):
    ws = wb.create_sheet(CON)
    negrita = Font(name="Arial", bold=True)
    normal = Font(name="Arial")
    ws.column_dimensions["A"].width = 58
    for c in range(2, 14):
        ws.column_dimensions[COL(c)].width = 13
    ws["A1"] = "  CONCILIACIÓN DEL MOTOR B · años 1–10 y terminal · V6.4 experimental"
    ws["A1"].font = Font(name="Arial", bold=True, size=12)
    ws["A2"] = ("La identidad FCF = NOPAT + D&A − inversión fija bruta − Δcirculante es un control aritmético: no prueba que una misma inversión "
                "reponga y haga crecer, ni que λ o θ describan a la empresa. En modo heredado se muestra la regla de la V6.3 (R0, sin desglose "
                "del circulante y sin P-M1). Solo motor B.")
    ws["A2"].alignment = Alignment(wrap_text=True)
    ws.merge_cells("A2:M2")
    ws.row_dimensions[2].height = 45
    ws["A3"] = "=" + C["resumen"]
    ws.merge_cells("A3:M3")
    ws.row_dimensions[3].height = 45
    ws["A3"].alignment = Alignment(wrap_text=True)
    bloques = {}
    for n, (nombre, fm) in enumerate((("MALO", 6), ("NORMAL", 7), ("BUENO", 8))):
        b = 5 + n * 30
        bloques[nombre] = b
        ws[f"A{b}"] = f"{nombre} · Motor, fila {fm}"
        ws[f"A{b}"].font = negrita
        ws[f"B{b}"] = f'=IF(Motor!$DY${fm},"motor B calculable","no aplica: motor distinto de B o fila no calculable")'
        R = {it: b + 1 + i for i, it in enumerate(ITEMS)}
        for it, rr in R.items():
            ws[f"A{rr}"] = it
            ws[f"A{rr}"].font = normal
        ok = f"Motor!$DY${fm}"
        for t in range(1, 12):
            c = COL(1 + t)       # B … K años, L terminal
            term = t == 11
            prev = COL(t)        # columna anterior
            rv = R["Ventas"]
            ws[f"{c}{R['Año']}"] = t if not term else "Terminal (año 11)"
            ws[f"{c}{rv}"] = f'=IF({ok},Motor!{L_t(t)}{fm},"")' if not term else f'=IF({ok},Motor!$AJ{fm}*(1+Motor!$H{fm}),"")'
            rp = R["Máximo de ventas conservado antes del año"]
            ws[f"{c}{rp}"] = f'=IF({ok},Motor!$C{fm},"")' if t == 1 else f'=IF({ok},MAX({prev}{rp},{prev}{rv}),"")'
            rm = R["Margen EBIT"]
            ws[f"{c}{rm}"] = f'=IF({ok},Motor!{m_t(t)}{fm},"")' if not term else f'=IF({ok},Motor!$F{fm},"")'
            rn = R["NOPAT = ventas × margen × (1 − t)"]
            ws[f"{c}{rn}"] = f'=IF({ok},{c}{rv}*{c}{rm}*(1-Motor!$K{fm}),"")'
            rd = R["Amortización (D&A)"]
            ws[f"{c}{rd}"] = (f'=IF({ok},{C["da0"]}*IF({C["anios_v"]},{c}{rv}/Motor!$C{fm},1),"")' if not term
                              else f'=IF({ok},{C["da0"]}*{c}{rv}/Motor!$C{fm},"")')
            rc = R["Cartera de clientes no repuesta (P0)"]
            ws[f"{c}{rc}"] = f'=IF({ok},{cl(t)},"")' if not term else f'=IF({ok},0,"")'
            rrc = R["Reposición contable = D&A − cartera"]
            ws[f"{c}{rrc}"] = f'=IF({ok},{c}{rd}-{c}{rc},"")'
            col_m = (lambda k: f"Motor!{letra(NUEVAS[k] + t - 1)}{fm}") if not term else (lambda k: f"Motor!{letra(T[k])}{fm}")
            rq = R["Requisito de reposición adicional"]
            ws[f"{c}{rq}"] = f'=IF({ok},{col_m("rq")},"")'
            rf = R["Inversión fija para crecer"]
            ws[f"{c}{rf}"] = f'=IF({ok},{col_m("fi")},"")'
            rcr = R["Crédito: la misma inversión cumple las dos funciones (solo H)"]
            ws[f"{c}{rcr}"] = f'=IF({ok},{col_m("cr")},"")'
            rpa = R["Reposición adicional pagada = requisito − crédito"]
            ws[f"{c}{rpa}"] = f'=IF({ok},{c}{rq}-{c}{rcr},"")'
            rdc = R["Δ circulante"]
            ws[f"{c}{rdc}"] = f'=IF({ok},{col_m("dc")},"")'
            rb = R["Inversión fija bruta = reposición contable + fija para crecer + adicional pagada"]
            ws[f"{c}{rb}"] = f'=IF({ok},{c}{rrc}+{c}{rf}+{c}{rpa},"")'
            rt = R["Inversión total = inversión fija bruta + Δ circulante"]
            ws[f"{c}{rt}"] = f'=IF({ok},{c}{rb}+{c}{rdc},"")'
            ri = R["FCF por la identidad = NOPAT + D&A − inversión fija bruta − Δ circulante"]
            ws[f"{c}{ri}"] = f'=IF({ok},{c}{rn}+{c}{rd}-{c}{rb}-{c}{rdc},"")'
            rmo = R["FCF que usa el motor (Motor AU:BD y BF)"]
            ws[f"{c}{rmo}"] = f'=IF({ok},Motor!{letra(46 + t)}{fm},"")' if not term else f'=IF({ok},Motor!$BF{fm},"")'
            rdf = R["Diferencia (identidad − motor)"]
            ws[f"{c}{rdf}"] = f'=IF(AND(ISNUMBER({c}{ri}),ISNUMBER({c}{rmo})),{c}{ri}-{c}{rmo},"")'
            rfa = R["Factor de descuento (terminal: ÷ (r − g) y 10 años)"]
            ws[f"{c}{rfa}"] = (f'=IF({ok},1/(1+Motor!$J{fm})^{t},"")' if not term
                               else f'=IF({ok},1/((Motor!$J{fm}-Motor!$H{fm})*(1+Motor!$J{fm})^10),"")')
            rvp = R["Valor presente"]
            ws[f"{c}{rvp}"] = f'=IF(AND(ISNUMBER({c}{rmo}),ISNUMBER({c}{rfa})),{c}{rmo}*{c}{rfa},"")'
        rs = R["Σ VP años 1–10 · motor · diferencia · VP terminal · motor · diferencia"]
        rvp = R["Valor presente"]
        ws[f"B{rs}"] = f'=IF({ok},SUM(B{rvp}:K{rvp}),"")'
        ws[f"C{rs}"] = f'=IF({ok},Motor!$BE{fm},"")'
        ws[f"D{rs}"] = f'=IF(AND(ISNUMBER(B{rs}),ISNUMBER(C{rs})),B{rs}-C{rs},"")'
        ws[f"E{rs}"] = f'=IF({ok},L{rvp},"")'
        ws[f"F{rs}"] = f'=IF({ok},Motor!$BH{fm},"")'
        ws[f"G{rs}"] = f'=IF(AND(ISNUMBER(E{rs}),ISNUMBER(F{rs})),E{rs}-F{rs},"")'
        ws[f"B{R['Peso del terminal (Motor BN)']}"] = f'=IF({ok},Motor!$BN{fm},"")'
        rsa = R["Salto año 10 → terminal: requisito · FCF · ventas (variación)"]
        rq, rmo, rv = R["Requisito de reposición adicional"], R["FCF que usa el motor (Motor AU:BD y BF)"], R["Ventas"]
        ws[f"B{rsa}"] = f'=IF(AND(ISNUMBER(K{rq}),ISNUMBER(L{rq})),IF(K{rq}<>0,L{rq}/K{rq}-1,IF(L{rq}=0,0,"de 0 a "&FIXED(L{rq},3))),"")'
        ws[f"C{rsa}"] = f'=IF(AND(ISNUMBER(K{rmo}),ISNUMBER(L{rmo}),N(K{rmo})<>0),L{rmo}/K{rmo}-1,"")'
        ws[f"D{rsa}"] = f'=IF(AND(ISNUMBER(K{rv}),ISNUMBER(L{rv}),N(K{rv})<>0),L{rv}/K{rv}-1,"")'
        re_ = R["S2C efectivo del crecimiento (años) · ROIC efectivo del crecimiento terminal"]
        ws[f"B{re_}"] = f'=IF({ok},IFERROR(1/({C["nwc"]}+(1/(Motor!$G{fm}*{C["fs2c"]})-{C["nwc"]})*{C["ffija"]}),""),"")'
        rn, rf, rdc = R["NOPAT = ventas × margen × (1 − t)"], R["Inversión fija para crecer"], R["Δ circulante"]
        ws[f"C{re_}"] = f'=IF({ok},IFERROR(L{rn}*Motor!$H{fm}/(L{rf}+L{rdc}),""),"")'
        rk = R["Comprobación de la fila"]
        rdf = R["Diferencia (identidad − motor)"]
        ws[f"B{rk}"] = (f'=IF(NOT({ok}),"no aplica",IF(AND(MAX(ABS(MIN(B{rdf}:L{rdf})),ABS(MAX(B{rdf}:L{rdf})))<1E-9*MAX(1,ABS(MAX(B{rv}:L{rv}))),'
                        f'ABS(D{rs})<1E-9*MAX(1,ABS(C{rs})),ABS(G{rs})<1E-9*MAX(1,ABS(F{rs}))),"✓ cuadra: identidad anual y terminal y VP iguales al motor","✗ NO CUADRA: revisa la fila de diferencias"))')
        ws[f"B{rk}"].font = negrita
    ws.freeze_panes = "B5"
    return bloques


# ------------------------------------------------------------------ 5. etiquetas y Panel
def etiquetas(wb):
    a = wb["Análisis"]["A1"]
    assert "V6.3" in a.value
    a.value = a.value.replace("— V6.3 ·", f"— {VERSION} (sobre V6.3) ·")
    p = wb["Panel"]["A1"]
    p.value = p.value.replace("DCF V6.3", f"DCF {VERSION}")
    g = wb["Guía V6"]["A1"]
    g.value = g.value.replace("GUÍA V6.3", f"GUÍA V6.3 · plantilla {VERSION}")
    cm = wb["Control maestro"]["A3"]
    cm.value = (f"Versión {VERSION} (12-nov-2026, encargo 4.11): capa experimental del motor B (N1–N3 y P-M1) en «Configuración V6.4» y "
                f"«Conciliación B»; en modo heredado calcula como la V6.3. · " + cm.value)
    pn = wb["Panel"]
    pn["B18"] = "Configuración V6.4"
    pn["B18"]._style = copy(pn["B17"]._style)
    pn["C18"] = "=" + C["resumen"]
    pn["C18"]._style = copy(pn["C17"]._style)


def normalizar_paquete(path):
    z = zipfile.ZipFile(path)
    items = [(i, z.read(i.filename)) for i in z.infolist()]
    z.close()
    tmp = path + ".tmp"
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as out:
        for info, datos in items:
            if info.filename == "docProps/core.xml":
                datos = re.sub(rb"(<dcterms:modified[^>]*>)[^<]*(</dcterms:modified>)", rb"\g<1>2026-11-12T00:00:00Z\g<2>", datos)
                datos = re.sub(rb"(<dcterms:created[^>]*>)[^<]*(</dcterms:created>)", rb"\g<1>2026-11-12T00:00:00Z\g<2>", datos)
            ni = zipfile.ZipInfo(info.filename, date_time=FECHA_FIJA)
            ni.compress_type = zipfile.ZIP_DEFLATED
            ni.external_attr = info.external_attr
            out.writestr(ni, datos)
    os.replace(tmp, path)


def main(src, dst):
    wb = load_workbook(src)
    ws_cfg, n_reglas = hoja_configuracion(wb)
    filas, cambiadas = motor(wb)
    diagnostico(wb)
    bloques = conciliacion(wb)
    etiquetas(wb)
    with tempfile.TemporaryDirectory() as tmp:
        mid = os.path.join(tmp, "v64.xlsx")
        wb.save(mid)
        restauradas = base.restaurar_partes(src, mid)   # gráficos y dibujos canónicos de la V6.3
        subprocess.run([sys.executable, "-I", os.path.join(AQUI, "add_sliders.py"), mid, dst], check=True, capture_output=True)
    normalizar_paquete(dst)
    print(f"{VERSION}: {len(filas)} filas de valoración del motor · {cambiadas} flujos anuales envueltos · {n_reglas} comprobaciones de configuración · "
          f"conciliación {sorted(bloques.items())} · partes restauradas {len(restauradas)} → {dst}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)
    main(sys.argv[1], sys.argv[2])
