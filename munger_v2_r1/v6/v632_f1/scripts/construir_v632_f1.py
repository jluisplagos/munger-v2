#!/usr/bin/env python3
"""Construye la plantilla V6.3.2 F1 del motor A a partir de la V6.3 (que no se modifica): la V6.3.1 F1 (perímetro F1 de la reinversión, el mismo
guion v6/v631_f1/scripts/construir_v631_f1.py, sin cambios) más la NORMALIZACIÓN DECLARADA DEL CIRCULANTE de la reinversión (19-nov-2026, decisión
V-CIRC (a) de la persona responsable sobre VINCI: «circulante a 0 también en la reinversión, con un mecanismo declarado: ni entradas ni salidas de
circulante», porque la caja base ya lo excluye).

Uso: python3 -I construir_v632_f1.py Plantilla_V6.3.xlsx Plantilla_V6.3.2_F1.xlsx

Qué cambia frente a la V6.3.1 F1 (y nada más):
  - Historia, sección nueva (filas 92–98): C93 regla (vacío = ninguna, o «circulante_a_cero»; lista de validación); C94:L94 años normalizados
    (1 o vacío; validación) y su procedencia en M93:S94; C95:L95 circulante excluido de la reinversión (= fila 14 en los años normalizados, 0 en los
    demás); C96:L96 circulante que usa la reinversión (fila 14 − fila 95; vacía con la fila 14 vacía); C97 normalización efectiva («ninguna»,
    «circulante_a_cero» o «no reconocida»: C93 con otro texto, o C94:L94 con algo distinto de 1, o marcas sin regla); A98 nota.
  - Fila 30 (y con ella la 31): capex − D_X + circulante de la fila 96. Sin normalización la fila 96 es la fila 14: el mismo valor.
  - C58 (f), C76 (conciliación) y C53 (ancla de S2C): con «ninguna», la fórmula de la V6.3.1 F1 literal (y con ella, con A0, la de la V6.3);
    con «circulante_a_cero», la rama de D_X de la V6.3.1 (la reinversión de la fila 30, ya normalizada) con cualquier perímetro: f exige normalizados
    TODOS los años de la ventana y el ancla, los cinco años H–L (con todo su denominador, E4: filas 12, 13, 14 y 88); con «no reconocida», vacías.
  - Motor E205 (validación V05 del motor A): al final, dos causas nuevas: normalización no reconocida (INV) y años de la ventana sin normalizar (INC).
  - Etiquetas de versión: Panel A1, Análisis A1, Guía V6 A1 y Control maestro A3 («V6.3.2 F1»).
La plantilla no decide nada: vacío = sin normalización = la V6.3.1 F1. La fila 14 (cifra publicada) y las demás series no cambian. La coherencia con la
caja base (Análisis C46 excluye el mismo circulante) la comprueba la capa motor_a_f1.py (F1-CIRC), no el libro.
Después, como la V6.3.1 F1: gráficos y dibujos de la plantilla de partida (patch_v62_base.restaurar_partes), deslizadores (add_sliders.py) y paquete
determinista (fechas fijas).
"""
import os
import re
import subprocess
import sys
import tempfile
import zipfile

from openpyxl import load_workbook
from openpyxl.worksheet.datavalidation import DataValidation

AQUI = os.path.dirname(os.path.abspath(__file__))
V6 = os.path.abspath(os.path.join(AQUI, "..", ".."))
sys.path.insert(0, os.path.join(V6, "scripts"))
sys.path.insert(0, os.path.join(V6, "v631_f1", "scripts"))
import patch_v62_base as base  # noqa: E402
import construir_v631_f1 as B631  # noqa: E402  (la transformación V6.3 → V6.3.1 F1, sin cambios)

VERSION = "V6.3.2 F1"
FECHA_FIJA = (2026, 11, 19, 0, 0, 0)
HI = "Historia"
COLS = "CDEFGHIJKL"
REGLA = "circulante_a_cero"                      # = motor_a_f1.REGLA_CIRCULANTE
F_TIT, F_REG, F_ANI, F_EXC, F_USA, F_EF, F_NOTA = 92, 93, 94, 95, 96, 97, 98
EF = f"$C${F_EF}"
VENTANA = B631.VENTANA                           # "COLUMN($C$6:$L$6)>12-$C$57"


def _args_si(expr):
    """Argumentos de primer nivel de «IF(a,b,c)» (sin el «=»), respetando paréntesis y comillas."""
    assert expr.startswith("IF(") and expr.endswith(")"), expr[:40]
    s, out, prof, cur, comillas = expr[3:-1], [], 0, [], False
    for ch in s:
        if ch == '"':
            comillas = not comillas
        if not comillas:
            if ch == "(":
                prof += 1
            elif ch == ")":
                prof -= 1
            elif ch == "," and prof == 0:
                out.append("".join(cur))
                cur = []
                continue
        cur.append(ch)
    out.append("".join(cur))
    assert prof == 0 and not comillas
    return out


def circulante(wb, f63):
    """Sección nueva y fórmulas que la usan. f63: las fórmulas de la V6.3 de C53, C58 y C76 (para comprobar lo que trae la V6.3.1)."""
    ws = wb[HI]
    for r in range(91, 99):
        for c in range(1, 20):
            assert ws.cell(r, c).value is None, f"Historia fila {r} no está libre"
    B631._estilo(ws[f"A{F_TIT}"], ws["A84"])
    ws[f"A{F_TIT}"] = ("  NORMALIZACIÓN DEL CIRCULANTE · motor A (V6.3.2 F1): circulante que la reinversión de f y del ancla de S2C excluye por una "
                       "decisión declarada")
    filas = ((F_REG, "Normalización del circulante de la reinversión (vacío = ninguna: la fila 14 tal cual)",
              "La declara la persona (motor_a_f1.json · normalizacion_circulante)"),
             (F_ANI, "Años normalizados: 1 = el circulante de ese año no entra en la reinversión", "De la declaración · vacío = no normalizado"),
             (F_EXC, "Circulante excluido de la reinversión (= fila 14 en los años normalizados)", "Calculado (no tocar)"),
             (F_USA, "Circulante que usa la reinversión (fila 14 − fila 95)", "Calculado (no tocar)"),
             (F_EF, "Normalización efectiva", "Calculada (no tocar)"))
    for r, a, b in filas:
        B631._estilo(ws[f"A{r}"], ws["A86"])
        B631._estilo(ws[f"B{r}"], ws["B86"])
        ws[f"A{r}"], ws[f"B{r}"] = a, b
        B631._estilo(ws[f"M{r}"], ws["M86"])
    B631._estilo(ws[f"C{F_REG}"], ws["C85"])
    ws[f"C{F_REG}"].number_format = "General"
    ws[f"D{F_REG}"] = (f"{REGLA}: ni entradas ni salidas de circulante en los años marcados en la fila {F_ANI} (la fila 14 sigue siendo la cifra "
                       "publicada; la caja base tiene que excluir el mismo circulante)")
    B631._estilo(ws[f"D{F_REG}"], ws["D85"])
    ws.merge_cells(f"D{F_REG}:L{F_REG}")
    for x in COLS:
        B631._estilo(ws[f"{x}{F_ANI}"], ws[f"{x}86"])
        ws[f"{x}{F_ANI}"].number_format = "General"
        B631._estilo(ws[f"{x}{F_EXC}"], ws[f"{x}88"])
        B631._estilo(ws[f"{x}{F_USA}"], ws[f"{x}88"])
        ws[f"{x}{F_EXC}"] = f'=IF(AND({EF}="{REGLA}",N({x}{F_ANI})=1),N({x}14),0)'
        ws[f"{x}{F_USA}"] = f'=IF(ISNUMBER({x}14),{x}14-{x}{F_EXC},"")'
    ws[f"C{F_EF}"] = (f'=IF(AND($C${F_REG}="",COUNTA($C${F_ANI}:$L${F_ANI})=0),"ninguna",IF(AND($C${F_REG}="{REGLA}",'
                      f'SUMPRODUCT(--($C${F_ANI}:$L${F_ANI}<>""),--($C${F_ANI}:$L${F_ANI}<>1))=0),"{REGLA}","no reconocida"))')
    B631._estilo(ws[f"C{F_EF}"], ws["C89"])
    ws[f"C{F_EF}"].number_format = "General"
    B631._estilo(ws[f"A{F_NOTA}"], ws["A90"])
    ws[f"A{F_NOTA}"] = ("Con la normalización vacía la hoja calcula exactamente como la V6.3.1 F1 (y, con A0_total, como la V6.3). Con «circulante_a_cero», "
                        "en los años marcados en la fila 94 el circulante no entra en la reinversión (fila 96 = 0): la fila 30 (y con ella la 31), f (C58), su "
                        "conciliación (C76) y el ancla de S2C (C53) usan la fila 96; la fila 14 sigue siendo la cifra publicada y la fila 95 enseña lo excluido. "
                        "f exige normalizados todos los años de la ventana y el ancla, los cinco años H–L (no se mezclan las dos reinversiones). Solo es "
                        "coherente si la caja base (Análisis C46) excluye el mismo circulante: lo comprueba la capa F1 (F1-CIRC), no la hoja.")
    ws.merge_cells(f"A{F_NOTA}:M{F_NOTA}")
    ws.row_dimensions[F_NOTA].height = 54
    # --- fila 30: capex − D_X + circulante de la fila 96
    for x in COLS:
        viejo = f'=IF(AND(ISNUMBER({x}12),ISNUMBER({x}88)),{x}12-{x}88+N({x}14),"")'
        assert ws[f"{x}30"].value == viejo, f"Historia {x}30 no es la de la V6.3.1 F1"
        ws[f"{x}30"] = f'=IF(AND(ISNUMBER({x}12),ISNUMBER({x}88)),{x}12-{x}88+N({x}{F_USA}),"")'
    # --- C58 (f): «ninguna» → la de la V6.3.1 literal; «circulante_a_cero» → su rama de D_X (fila 30 normalizada) con la ventana entera normalizada
    c58 = ws["C58"].value
    a = _args_si(c58[1:])
    assert len(a) == 3 and a[0] == '$C$89="A0_total"' and a[1] == f63["C58"][1:], "Historia C58 no es la de la V6.3.1 F1"
    assert f"SUMPRODUCT(--({VENTANA}),$C$30:$L$30)" in a[2]
    sin_marcar = f'SUMPRODUCT(--({VENTANA}),--($C${F_ANI}:$L${F_ANI}<>1))>0'
    ws["C58"] = f'=IF({EF}="ninguna",{c58[1:]},IF({EF}="{REGLA}",IF(NOT(ISNUMBER($C$57)),"",IF({sin_marcar},"",{a[2]})),""))'
    # --- C76 (reinversión neta media de la conciliación)
    c76 = ws["C76"].value
    a = _args_si(c76[1:])
    assert len(a) == 3 and a[0] == '$C$89="A0_total"' and a[1] == f63["C76"][1:], "Historia C76 no es la de la V6.3.1 F1"
    ws["C76"] = f'=IF({EF}="ninguna",{c76[1:]},IF({EF}="{REGLA}",{a[2]},""))'
    # --- C53 (ancla de S2C, E4): los cinco años H–L de todo el denominador y normalizados los cinco
    c53 = ws["C53"].value
    a = _args_si(c53[1:])
    assert len(a) == 3 and a[0] == '$C$89="A0_total"' and a[1] == f63["C53"][1:], "Historia C53 no es la de la V6.3.1 F1"
    ws["C53"] = (f'=IF({EF}="ninguna",{c53[1:]},IF({EF}="{REGLA}",IF(OR(COUNT($H$12:$L$12)<5,COUNT($H$13:$L$13)<5,COUNT($H$14:$L$14)<5,'
                 f'COUNT($H$88:$L$88)<5,SUMPRODUCT(--($H${F_ANI}:$L${F_ANI}=1))<5),"",{f63["C53"][1:]}),""))')
    # --- validaciones de las entradas nuevas
    dv = DataValidation(type="list", formula1=f'"{REGLA}"', allow_blank=True)
    dv.error, dv.errorTitle = f"Normalización del circulante: «{REGLA}» (vacío = ninguna).", "Normalización del circulante"
    dv.add(f"C{F_REG}")
    ws.add_data_validation(dv)
    dv2 = DataValidation(type="whole", operator="equal", formula1="1", allow_blank=True)
    dv2.error, dv2.errorTitle = "Año normalizado: 1 (el circulante de ese año no entra en la reinversión) o vacío.", "Año normalizado"
    dv2.add(f"C{F_ANI}:L{F_ANI}")
    ws.add_data_validation(dv2)


def motor_v05(wb):
    ws = wb["Motor"]
    v = ws["E205"].value
    fin = 'la PPA supera la D&A total (fila 8) en algún año de la ventana","")'
    assert v.count(fin) == 1, "Motor E205 no es la de la V6.3.1 F1"
    ef = f"Historia!$C${F_EF}"
    win = "COLUMN(Historia!$C$6:$L$6)>12-Historia!$C$57"
    nuevo = (fin[:-3]   # «…ventana",» sin el «"")» final: el último «""» de la V6.3.1 pasa a ser la cadena de causas nuevas
             + f'IF({ef}="no reconocida","INV|Normalización del circulante (Historia C{F_REG}:L{F_ANI}) no reconocida: C{F_REG} vacío o «{REGLA}» y en '
               f'C{F_ANI}:L{F_ANI} solo 1 o vacío (sin regla, ninguna marca)",'
             + f'IF(AND({ef}="{REGLA}",SUMPRODUCT(--({win}),--(Historia!$C${F_ANI}:$L${F_ANI}<>1))>0),"INC|Motor A · normalización del circulante: '
               f'faltan años de la ventana que calibra f en Historia C{F_ANI}:L{F_ANI} (la normalización cubre todos los años que usa la reinversión)","")))')
    ws["E205"] = v.replace(fin, nuevo)


def etiquetas(wb):
    cambios = {("Análisis", "A1"): ("— V6.3.1 F1 ·", f"— {VERSION} ·"), ("Guía V6", "A1"): ("GUÍA V6.3.1 F1 ·", f"GUÍA {VERSION} ·"),
               ("Panel", "A1"): ("DCF V6.3.1 F1 ·", f"DCF {VERSION} ·"),
               ("Control maestro", "A3"): ("Versión V6.3.1 F1 (18-nov-2026, F1-IMPL: perímetro F1 de la reinversión del motor A, Historia C85:L89; ",
                                           f"Versión {VERSION} (19-nov-2026, V-CIRC: normalización declarada del circulante de la reinversión, Historia "
                                           f"C{F_REG}:L{F_EF}; sobre la V6.3.1 F1 del 18-nov-2026, F1-IMPL: perímetro F1 de la reinversión del motor A, "
                                           "Historia C85:L89; ")}
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
                datos = re.sub(rb"(<dcterms:modified[^>]*>)[^<]*(</dcterms:modified>)", rb"\g<1>2026-11-19T00:00:00Z\g<2>", datos)
                datos = re.sub(rb"(<dcterms:created[^>]*>)[^<]*(</dcterms:created>)", rb"\g<1>2026-11-19T00:00:00Z\g<2>", datos)
            ni = zipfile.ZipInfo(info.filename, date_time=FECHA_FIJA)
            ni.compress_type = zipfile.ZIP_DEFLATED
            ni.external_attr = info.external_attr
            out.writestr(ni, datos)
    os.replace(tmp, path)


def main(src, dst):
    wb = load_workbook(src)
    f63 = {c: wb[HI][c].value for c in ("C53", "C58", "C76")}
    B631.historia(wb)        # V6.3 → V6.3.1 F1 (sin cambios)
    B631.motor_v05(wb)
    B631.etiquetas(wb)
    circulante(wb, f63)      # V6.3.1 F1 → V6.3.2 F1
    motor_v05(wb)
    n = etiquetas(wb)
    with tempfile.TemporaryDirectory() as tmp:
        mid = os.path.join(tmp, "v632.xlsx")
        wb.save(mid)
        restauradas = base.restaurar_partes(src, mid)
        subprocess.run([sys.executable, "-I", os.path.join(AQUI, "add_sliders.py"), mid, dst], check=True, capture_output=True)
    normalizar_paquete(dst)
    print(f"{VERSION}: la V6.3.1 F1 (perímetro F1, Historia C85:L89) y la normalización del circulante (Historia C{F_REG}:L{F_EF}); fila 30, C53, C58 y C76 "
          f"con el circulante de la fila {F_USA}, Motor E205; {n} etiquetas de versión; partes restauradas {len(restauradas)} → {dst}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)
    main(sys.argv[1], sys.argv[2])
