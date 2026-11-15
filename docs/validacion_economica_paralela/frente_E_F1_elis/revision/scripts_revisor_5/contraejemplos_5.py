"""Revisión n.º 5 (frente E · F1 · Elis). Contraejemplos y controles sobre filas reales de los PDF. No modifica nada del autor.

Cada caso es una fila que existe en el PDF, declarada como se indica, y se ejecuta con verificar_cifras.py de cada versión
del autor (C8, C9 y C11) como proceso aparte: es la ejecución oficial, no una llamada a sus funciones.

  A. C9: el hueco de las columnas por país y su corrección.
  B. Columnas que no son las del ejercicio vigente y siguen pasando: «published», «reported» y «publié» de las tablas de
     reexpresión; balance de apertura; totales de una tabla de vencimientos.
  C. Filas legítimas que C9 deja PENDIENTE, y cifras de otro ejercicio que pasan de FALLO a PENDIENTE.
  D. P1: criterio de formato de recuento.
  E. P2: bloques y filas de otro perímetro que siguen pasando, y filas del grupo bajo un texto que nombra un país.

Para no contar posiciones a mano, la posición del token se calcula localizando el literal en la línea con el tokenizador
del propio verificador; el verificador oficial comprueba después que el token de esa posición es el literal.

Uso: python3 -I contraejemplos_5.py --raiz <munger_v2_r1> --version C8=<frente C8> --version C9=<frente C9> --version C11=<frente C11>
"""
import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from arnes import GRUPO, Modulo, estados, fila, motivo, oficial  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raiz", required=True)
    ap.add_argument("--version", action="append", required=True, help="NOMBRE=carpeta frente_E_F1_elis; la última es la revisada")
    a = ap.parse_args()
    versiones = [v.split("=", 1) for v in a.version]
    M = Modulo(versiones[-1][1], a.raiz, "verificador_revisado")
    casos, textos = [], []

    def caso(clave, titulo, doc, pagina, rx_linea, literal, anio, n_esimo=1, ocurrencia=1, **campos):
        """rx_linea localiza la línea (ocurrencia-ésima que casa); literal es el token (n_esimo-ésimo igual en la línea)."""
        lineas = M.texto(doc, pagina).splitlines()
        cand = [i for i, l in enumerate(lineas) if re.search(rx_linea, l)]
        if len(cand) < ocurrencia:
            raise SystemExit(f"{clave}: línea no encontrada en {doc} p.{pagina}: {rx_linea}")
        i = cand[ocurrencia - 1]
        idioma = M.fuentes[doc]["idioma"]
        toks = M.m.tokens_numericos(lineas[i], idioma)
        pos_tok = [k for k, t in enumerate(toks) if t == literal]
        if len(pos_tok) < n_esimo:
            raise SystemExit(f"{clave}: literal {literal!r} no encontrado en la línea: {toks}")
        pos = pos_tok[n_esimo - 1] - len(toks)
        iguales = [k for k, l in enumerate(lineas) if l == lineas[i]]
        E = M.fuentes[doc]["ejercicio"]
        c = dict(doc=doc, pagina=pagina, anio=anio, etiqueta="re:^" + re.escape(lineas[i]) + "$", ocurrencia=iguales.index(i) + 1, pos=pos,
                 literal=literal, valor_publicado=str(M.m.valor(literal, idioma)), unidad="%" if "%" in literal else "mm EUR",
                 edicion="vigente" if (anio == E - 1 or (anio == E and (E + 1) not in M.ejercicios)) else "anterior")
        c.update(campos)
        if c.get("control_anio") == "crecimiento":      # tabla de un solo ejercicio: la edición vigente es la del propio ejercicio
            c["edicion"] = "vigente" if anio == E else "anterior"
        idf = campos.pop("idf", None) or f"R5_{clave}"
        c.pop("idf", None)
        casos.append(fila(idf, **c))
        textos.append((clave, titulo, f"{doc} p.{pagina} l.{i + 1} · «{re.sub(r'  +', '  ', lineas[i].strip())[:105]}» · token «{literal}» · "
                                      f"declarado {anio}, {c['unidad']}, {c.get('perimetro', GRUPO)}, edición {c['edicion']}", idf))

    U21, U22, U23, D24, U25 = "URD2021", "URD2022", "URD2023", "DEU2024FR", "URD2025"
    ADQ = r"^\s*Acquisition of subsidiaries, net of cash acquired\s{2,}"

    # ------------------------------------------------------------------ A
    caso("A1", "Bélgica, contigua al total, en la tabla de flujos de adquisiciones de 2021 (el hueco descrito por el autor)", U22, 277, r"^\s*Net cash flow\s", "(19.0)", 2021)
    caso("A2", "control: columna del total de esa tabla", U22, 277, r"^\s*Net cash flow\s", "(86.8)", 2021)
    caso("A3", "Letonia, país que no está en la lista de países del verificador", U22, 277, r"^\s*Amount paid\s", "(2.6)", 2021)
    caso("A4", "Gran Bretaña, cabecera partida en dos líneas («Great» / «Britain»)", U22, 277, r"^\s*Amount paid\s", "(7.9)", 2021)
    caso("A5", "la misma tabla tal como se publicó en el URD 2021: Irlanda (13,5)", U21, 242, r"^\s*NET CASH FLOW\s", "(13.5)", 2021)
    caso("A6", "adquisiciones de 2020 por país (URD 2021 p.244): «Germany & Luxembourg»", U21, 244, r"^\s*NET CASH FLOW\s", "(19.2)", 2020)
    caso("A7", "control: total de las adquisiciones de 2020 (URD 2021 p.244)", U21, 244, r"^\s*NET CASH FLOW\s", "(87.6)", 2020)
    caso("A8", "sociedad adquirida (Lavartex), URD 2023 p.294: límite declarado por el autor", U23, 294, r"^\s*NET CASH FLOW\s", "(146.2)", 2022)
    caso("A9", "«Other acquisitions», URD 2023 p.294", U23, 294, r"^\s*NET CASH FLOW\s", "(39.1)", 2022)
    caso("A10", "tabla de 2022 con los países en las filas (URD 2022 p.275): México (146,2)", U22, 275, r"^\s*Mexico\s", "(146.2)", 2022)

    # ------------------------------------------------------------------ B
    caso("B1", "tabla de reexpresión del EFE: adquisiciones de 2021, columna «12/31/2021 published» (86,9)", U22, 271, ADQ, "(86.9)", 2021)
    caso("B2", "la misma línea, columna «12/31/2021 restated» (86,8): la cifra vigente", U22, 271, ADQ, "(86.8)", 2021)
    caso("B3", "la misma línea, columna del ajuste «IFRS 3» (0,1)", U22, 271, ADQ, "0.1", 2021)
    caso("B4", "informe de gestión, «2021 restated» (86,9): límite declarado por el autor", U22, 247, ADQ, "(86.9)", 2021)
    caso("B5", "resultado neto de 2021, columna «published» (114,6; reexpresado 114,4)", U22, 271, r"^\s*CONSOLIDATED NET INCOME \(LOSS\)\s", "114.6", 2021)
    caso("B6", "resultado neto de 2021, columna «restated» (114,4)", U22, 271, r"^\s*CONSOLIDATED NET INCOME \(LOSS\)\s", "114.4", 2021)
    caso("B7", "PPA de 2024, columna «2024 published» (84,9; la vigente es 85,0)", U25, 334, r"^\s*Amortization of intangible assets recognized in a business combination\s", "(84.9)", 2024)
    caso("B8", "PPA de 2024, columna «2024 restated» (85,0)", U25, 334, r"^\s*Amortization of intangible assets recognized in a business combination\s", "(85.0)", 2024)
    caso("B9", "adquisiciones de 2023, columna «2023 publié» (82,2; la vigente es 82,1)", D24, 283, r"^\s*Acquisition de filiales, sous déduction de la trésorerie acquise\s", "(82,2)", 2023)
    caso("B10", "adquisiciones de 2023, columna «2023 retraité» (82,1)", D24, 283, r"^\s*Acquisition de filiales, sous déduction de la trésorerie acquise\s", "(82,1)", 2023)
    caso("B11", "adquisiciones de 2022, columna «2022 reported» (221,6; la vigente es 221,7)", U23, 289, ADQ, "(221.6)", 2022)
    caso("B12", "adquisiciones de 2022, columna «2022 restated» (221,7)", U23, 289, ADQ, "(221.7)", 2022)
    caso("B13", "balance del URD 2021 (tres columnas): total de activos no corrientes de 2020 (7.010,1) declarado 2021", U21, 228, r"^\s*TOTAL NON-CURRENT ASSETS\s", "7,010.1", 2021)
    caso("B14", "balance del URD 2021: saldo de apertura «01/01/2020 Adjusted» (7.198,9) declarado 2020", U21, 228, r"^\s*TOTAL NON-CURRENT ASSETS\s", "7,198.9", 2020)
    caso("B15", "balance del URD 2021: la cifra correcta de 2021 (7.065,5) declarada 2021", U21, 228, r"^\s*TOTAL NON-CURRENT ASSETS\s", "7,065.5", 2021)
    caso("B16", "balance del URD 2021: la cifra correcta de 2020 (7.010,1) declarada 2020", U21, 228, r"^\s*TOTAL NON-CURRENT ASSETS\s", "7,010.1", 2020)
    caso("B19", "balance del URD 2021, fila con nota (cuatro tokens): saldo de apertura del fondo de comercio (3.795,6) declarado 2020", U21, 228, r"^\s*Goodwill\s", "3,795.6", 2020)
    caso("B17", "vencimientos de los pasivos por arrendamiento: total de flujos futuros sin descontar (856,9) declarado 2025", U25, 366, r"^\s*Lease liabilities\s", "856.9", 2025)
    caso("B18", "vencimientos: valor en libros del pasivo (703,2) declarado 2025", U25, 366, r"^\s*Lease liabilities\s", "703.2", 2025)

    # ------------------------------------------------------------------ C
    caso("C1", "cuenta de resultados del URD 2021: resultado antes de impuestos de 2020 (29,7)", U21, 226, r"^\s*Income \(loss\) before tax\s", "29.7", 2020)
    caso("C2", "el mismo token declarado 2021 (ejercicio equivocado)", U21, 226, r"^\s*Income \(loss\) before tax\s", "29.7", 2021)
    caso("C3", "cuenta de resultados del URD 2021: resultado neto de 2020 (2,7)", U21, 226, r"^\s*NET INCOME \(LOSS\)\s", "2.7", 2020)
    caso("C4", "control: ventas de 2020 (2.806,3), el número ancho de la misma columna", U21, 226, r"^\s*Revenue\s", "2,806.3", 2020)
    caso("C5", "EFE del URD 2021: pagos en acciones de 2020 (12,9)", U21, 229, r"^\s*Share-based payments\s", "12.9", 2020)
    caso("C6", "el mismo token declarado 2021 (ejercicio equivocado)", U21, 229, r"^\s*Share-based payments\s", "12.9", 2021)

    # ------------------------------------------------------------------ D
    caso("D1", "P1 (A1 del revisor n.º 4): efecto de la conversión, 23.355.764 acciones", U25, 395, r"^\s*Effect of conversion of convertible bonds\s", "23,355,764", 2025)
    caso("D2", "P1 (A2): acciones de emisión condicionada, 1.767.869", U25, 395, r"^\s*Effect of contingently issuable shares\s", "1,767,869", 2025)
    caso("D3", "P1 (A3, control): número medio ponderado de acciones", U25, 395, r"^\s*Weighted average number of shares\s", "233,954,020", 2025)
    caso("D4", "edición francesa: «Nombre moyen pondéré d'actions 235 896 652»", D24, 340, r"^\s*Nombre moyen pondéré d'actions\s", "235 896 652", 2024)
    caso("D5", "autocartera, 117.289 acciones («Treasury shares (a)»)", U21, 291, r"^\s*Treasury shares \(a\)\s", "117,289", 2021)
    caso("D6", "importe legítimo en millones sin decimales (sensibilidad del deterioro, 1.496): la unidad no debe quedar marcada", U22, 304, r"^\s*WACC\s+6\.4%", "1,496", 2022)

    # ------------------------------------------------------------------ E
    OBL = r"TOTAL VALUE OF DEFINED BENEFIT PLAN OBLIGATIONS \(1\)"
    caso("E1", "P2 (B1 del revisor n.º 4): obligaciones de Francia, 45,2 (el grupo: 414,4)", U25, 356, OBL, "45.2", 2025)
    caso("E2", "el mismo bloque «FRANCE – DETAILS»: tasa de descuento de Francia, 3,7 %", U25, 356, r"^\s*Discount rate\s", "3.7%", 2025)
    caso("E3", "bloque «IRELAND – DETAILS»: activos del plan de Irlanda, 24,2 (el grupo: 347,3)", U25, 357, r"^\s*FAIR VALUE OF PLAN ASSETS\s", "24.2", 2025)
    caso("E4", "bloque «UNITED KINGDOM – DETAILS»: activos del plan del Reino Unido, 243,5", U25, 358, r"^\s*FAIR VALUE OF PLAN ASSETS\s", "243.5", 2025)
    caso("E5", "URD 2023, bloque «FRANCE – DETAILS»: obligaciones de Francia de 2022, 40,1 (el mismo caso B1, otra edición)", U23, 308, r"^\s*Total value of defined benefit plan obligations \(1\)\s", "40.1", 2022)
    caso("E6", "URD 2022, bloque de Irlanda con el título en la página anterior: obligaciones, 29,6 (2021)", U22, 291, OBL, "29.6", 2021)
    caso("E7", "DEU 2024, «DÉTAIL POUR LE ROYAUME-UNI»: activos del plan, 257,3", D24, 304, r"^\s*JUSTE VALEUR DES ACTIFS DES RÉGIMES\s", "257,3", 2024)
    caso("E8", "tabla de crecimiento del URD 2021: ventas de «United Kingdom and Ireland» (364,2)", U21, 211, r"^\s*United Kingdom and Ireland\s", "364.2", 2021)
    caso("E9", "la misma fila: crecimiento orgánico del segmento (12,8 %) declarado crecimiento orgánico del grupo", U21, 211, r"^\s*United Kingdom and Ireland\s",
         "12.8%", 2021, idf="CREC_ORG_R5_UKI", control_anio="crecimiento")
    caso("E10", "control: crecimiento orgánico del grupo, fila TOTAL (7,4 %)", U21, 211, r"^\s*TOTAL\s", "7.4%", 2021, idf="CREC_ORG_R5_TOTAL", control_anio="crecimiento")
    caso("E11", "tabla de crecimiento del DEU 2024: «Royaume-Uni et Irlande», crecimiento orgánico (4,3 %)", D24, 253, r"^\s*Royaume-Uni et Irlande\s",
         "+ 4,3%", 2024, idf="CREC_ORG_R5_RUI", control_anio="crecimiento")
    caso("E12", "tabla de crecimiento del URD 2022: rótulo partido «and Ireland», crecimiento orgánico (28,8 %)", U22, 243, r"^\s*and Ireland\s", "28.8%", 2022,
         idf="CREC_ORG_R5_IRL", control_anio="crecimiento")
    caso("E13", "tabla de crecimiento del URD 2023: rótulo partido «Ireland», crecimiento orgánico (14,0 %)", U23, 261, r"^\s*Ireland\s+534", "14.0%", 2023,
         idf="CREC_ORG_R5_IRL23", control_anio="crecimiento")
    caso("E14", "control: URD 2025, «UK & Ireland», crecimiento orgánico (2,6 %)", U25, 307, r"^\s*UK & Ireland\s", "+2.6%", 2025, idf="CREC_ORG_R5_UKI25",
         control_anio="crecimiento")
    caso("E15", "fondo de comercio de la UGE Francia (1.442,9) declarado fondo de comercio del grupo", U25, 363, r"^\s*CGU France\s", "1,442.9", 2025)
    caso("E16", "tabla por países del DEU 2024: «République d'Irlande (Eire)» (109,3)", D24, 292, r"^\s*République d'Irlande \(Eire\)\s", "109,3", 2024)
    caso("E17", "control: fila «France» de esa tabla", D24, 292, r"^\s*France\s", M.m.tokens_numericos(next(l for l in M.texto(D24, 292).splitlines() if re.match(r"^\s*France\s", l)), "fr")[0], 2024)
    caso("E18", "fila del GRUPO bajo un texto que nombra un país: total de clientes y activos por contratos (824,1)", D24, 321, r"^\s*CLIENTS ET ACTIFS SUR CONTRATS\s", "824,1", 2024)
    caso("E19", "positivo del autor: total por países de la nota de pensiones (67,1), bajo «INFORMATION BY REGION»", U25, 356,
         r"^\s*LIABILITIES \(ASSETS\) RELATED TO DEFINED BENEFIT PLANS\s", "67.1", 2025)

    res = {nom: oficial(carpeta, a.raiz, casos)[1] for nom, carpeta in versiones}
    secciones = {"A": "A. C9: columnas por país (hueco y corrección)", "B": "B. Columnas que no son las del ejercicio vigente",
                 "C": "C. Filas legítimas que quedan PENDIENTE y ejercicio equivocado que pasa de FALLO a PENDIENTE",
                 "D": "D. P1: formato de recuento", "E": "E. P2: perímetro"}
    ultima = None
    for clave, titulo, donde, idf in textos:
        if clave[0] != ultima:
            ultima = clave[0]
            print(f"\n{secciones[ultima]}")
        print(f"\n{clave} {titulo}\n    {donde}")
        for nom, _ in versiones:
            r = res[nom][idf]
            e = estados(r)
            no_ok = [k for k in e if e[k] not in ("OK", "NO_APLICA")]
            print(f"    {nom:<4}{r['estado']}" + (" en las seis dimensiones" if not no_ok else " · " + " · ".join(f"{k} {e[k]}: {motivo(r, k)[:120]}" for k in no_ok)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
