"""Pruebas del verificador de cifras (frente E): positivos reales y contraejemplos.

Cada caso fija el estado que debe dar verificar_cifras.py (OK, PENDIENTE o FALLO) y, en los contraejemplos, la
dimensión que debe detectarlo: literal, ejercicio, unidad, perimetro o edicion. En los mutantes «coherentes» se
cambian a la vez la posición, el literal, el valor, la página o la fuente, de modo que el literal sigue siendo
el impreso: solo la dimensión señalada puede rechazarlos, y el caso exige que las demás no fallen.

Cubre:
- los huecos de la revisión externa: página inexistente, fuente ausente o con otra huella, redondeo presentado
  como cifra exacta, signo publicado invertido (R415-SIGNO);
- los de la revisión independiente n.º 1 del frente E (O3, mutantes M1–M4): columna de otro ejercicio con su propio
  literal, bloque de movimientos o saldo de otro año, fuente sin huella declarada, y año, unidad y perímetro falsos;
- el contraste externo sobre 6fb9294: mutantes conjuntos de posición y literal, año, unidad, perímetro y edición.

Uso:  python3 -I test_verificar_cifras.py --raiz <ruta>/munger_v2_r1
"""
import argparse
import csv
import json
import subprocess
import sys
import tempfile
from pathlib import Path

AQUI = Path(__file__).resolve().parent
DATOS = AQUI.parent / "datos"
CODIGO = {"OK": 0, "PENDIENTE": 2, "FALLO": 1}


def ejecutar(raiz, filas, fuentes):
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        (d / "f.json").write_text(json.dumps(fuentes, ensure_ascii=False), encoding="utf-8")
        with (d / "c.csv").open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(filas[0].keys()), delimiter=";")
            w.writeheader()
            w.writerows(filas)
        r = subprocess.run([sys.executable, "-I", str(AQUI / "verificar_cifras.py"), "--raiz", str(raiz), "--datos", str(d / "c.csv"),
                            "--fuentes", str(d / "f.json"), "--salida", str(d / "s.json")], capture_output=True, text=True)
        if not (d / "s.json").is_file():
            return r.returncode, None
        return r.returncode, json.loads((d / "s.json").read_text(encoding="utf-8"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raiz", required=True, type=Path)
    a = ap.parse_args()
    fuentes = json.loads((DATOS / "fuentes.json").read_text(encoding="utf-8"))
    base = {r["id"]: r for r in csv.DictReader((DATOS / "cifras_fuente.csv").open(encoding="utf-8"), delimiter=";")}
    fila = lambda i: dict(base[i])  # noqa: E731
    lease, rou = fila("CF_LEASE_2025"), fila("DA_ROU_2025")
    casos = []

    def caso(nombre, filas, estado, fallan=None, fu=None, coherente=False, motivo=None):
        casos.append({"nombre": nombre, "filas": filas, "fuentes": fu or fuentes, "estado": estado,
                      "fallan": fallan or {}, "coherente": coherente, "motivo": motivo})

    # ---- positivos reales
    caso("positivo: pagos de arrendamiento y amortización ROU de 2025", [lease, rou], "OK")
    c = fila("DA_ROU_2025"); c.update(anio="2024", pos="-1", literal="(132.2)", valor_publicado="-132.2")
    caso("positivo: columna de 2024 declarada como 2024 (año, posición y literal coherentes)", [c], "OK")
    caso("positivo: total de la matriz por segmentos (lino plano 2025)", [fila("VENTAS_LINO_PLANO_2025")], "OK")
    caso("positivo: cifra de la edición anterior declarada «anterior»", [fila("DA_PPA_U23_2023")], "OK")
    caso("positivo: saldo de apertura de un bloque de movimientos", [fila("LS_SALDO_ROU_2023")], "OK")
    caso("positivo: porcentaje de crecimiento orgánico", [fila("CREC_ORG_2025")], "OK")
    caso("positivo: prosa del factor de riesgo (dos tercios del lino plano)", [fila("TXT_LINO_2TERCIOS_2025")], "OK")
    # ---- literal (revisión externa)
    c = dict(lease); c["literal"] = "177.9"; c["valor_publicado"] = "177.9"
    caso("signo invertido en el literal", [c], "FALLO", {"CF_LEASE_2025": {"literal"}})
    c = dict(lease); c["valor_publicado"] = "177.9"
    caso("signo invertido solo en el valor", [c], "FALLO", {"CF_LEASE_2025": {"literal"}})
    c = dict(rou); c["literal"] = "(150)"; c["valor_publicado"] = "-150"
    caso("redondeo 150 frente a 149,5", [c], "FALLO", {"DA_ROU_2025": {"literal"}})
    c = dict(rou); c["valor_publicado"] = "-150"
    caso("valor redondeado con literal correcto", [c], "FALLO", {"DA_ROU_2025": {"literal"}})
    c = dict(lease); c["pagina"] = "999999"
    caso("página inexistente", [c], "FALLO", {"CF_LEASE_2025": {"literal"}})
    c = dict(lease); c["pagina"] = "326"
    caso("página equivocada", [c], "FALLO", {"CF_LEASE_2025": {"literal"}})
    f2 = json.loads(json.dumps(fuentes)); f2["fuentes"]["URD2025"]["sha256"] = "0" * 64
    caso("fuente con huella distinta", [lease], "FALLO", {"CF_LEASE_2025": {"literal"}}, fu=f2)
    f3 = json.loads(json.dumps(fuentes)); f3["fuentes"]["URD2025"]["archivo"] += ".no_existe"
    caso("fuente ausente", [lease], "FALLO", {"CF_LEASE_2025": {"literal"}}, fu=f3)
    f4 = json.loads(json.dumps(fuentes)); del f4["fuentes"]["URD2025"]["sha256"]
    caso("fuente sin huella declarada: diagnóstico controlado", [lease], "FALLO", {"CF_LEASE_2025": {"literal"}}, fu=f4,
         motivo="no declara SHA-256")
    c = dict(lease); c["pos"] = "-1"
    caso("posición distinta con el mismo literal", [c], "FALLO", {"CF_LEASE_2025": {"literal"}})
    # ---- ejercicio (O3/M1 y contraste externo: posición y literal cambiados a la vez)
    c = dict(rou); c.update(pos="-1", literal="(132.2)", valor_publicado="-132.2")
    caso("M1: columna de 2024 con su literal declarada como 2025", [c], "FALLO", {"DA_ROU_2025": {"ejercicio"}}, coherente=True)
    c = dict(lease); c.update(pos="-1", literal="(150.8)", valor_publicado="-150.8")
    caso("pagos de arrendamiento de 2024 declarados como 2025", [c], "FALLO", {"CF_LEASE_2025": {"ejercicio"}}, coherente=True)
    c = fila("LS_NUEVO_ROU_2025"); c.update(ocurrencia="1", literal="145.7", valor_publicado="145.7")
    caso("bloque de movimientos de otro ejercicio", [c], "FALLO", {"LS_NUEVO_ROU_2025": {"ejercicio"}}, coherente=True)
    c = fila("LS_SALDO_PAS_2025"); c.update(etiqueta="AS AT 12/31/2024", literal="606.2", valor_publicado="606.2")
    caso("saldo de otra fecha", [c], "FALLO", {"LS_SALDO_PAS_2025": {"ejercicio"}}, coherente=True)
    c = dict(rou); c["anio"] = "2031"
    # un año falso rompe también la regla de edición: deben detectarlo las dos dimensiones
    caso("año alterado (2031)", [c], "FALLO", {"DA_ROU_2025": {"ejercicio", "edicion"}}, coherente=True)
    c = fila("VENTAS_LINO_PLANO_2025"); c["anio"] = "2024"
    caso("tabla de un solo ejercicio declarada de otro año", [c], "FALLO", {"VENTAS_LINO_PLANO_2025": {"ejercicio"}}, coherente=True)
    c = fila("TXT_VOLUMEN_2025"); c["anio"] = "2024"
    caso("prosa declarada de un ejercicio distinto del de la publicación", [c], "FALLO", {"TXT_VOLUMEN_2025": {"ejercicio"}}, coherente=True)
    c = dict(rou); c["control_anio"] = "manual"; c["nota"] = ""
    caso("control manual sin justificación", [c], "FALLO", {"DA_ROU_2025": {"ejercicio"}}, coherente=True)
    c = dict(rou); c["control_anio"] = "manual"; c["nota"] = "justificación de prueba"
    caso("control manual justificado: PENDIENTE, nunca OK", [c], "PENDIENTE")
    # ---- unidad
    c = dict(rou); c["unidad"] = "%"
    caso("unidad «%» para una cifra en millones", [c], "FALLO", {"DA_ROU_2025": {"unidad"}}, coherente=True)
    c = fila("CREC_ORG_2025"); c["unidad"] = "mm EUR"
    caso("unidad «mm EUR» para un porcentaje (sonda externa sobre eb77dea, campo separado)", [c], "FALLO", {"CREC_ORG_2025": {"unidad"}},
         coherente=True)
    c = dict(rou); c["unidad"] = "miles EUR"
    caso("unidad no reconocida", [c], "FALLO", {"DA_ROU_2025": {"unidad"}}, coherente=True)
    c = dict(rou)
    c.update(id="MILES_URD2025_P319", anio="2025", pagina="319", etiqueta="Aggregate invoice amount (incl. VAT)", ocurrencia="0",
             pos="0", literal="(5,285)", valor_publicado="-5285", control_anio="manual", nota="tabla sin años: caso de prueba")
    caso("tabla en miles de euros (sociedad matriz) declarada en millones", [c], "FALLO", {"MILES_URD2025_P319": {"unidad"}})
    # ---- perímetro
    c = fila("IS_VENTAS_2025"); c["perimetro"] = "segmento Francia"
    caso("perímetro «segmento Francia» en la cuenta de resultados consolidada (sonda externa sobre eb77dea, campo separado)", [c],
         "FALLO", {"IS_VENTAS_2025": {"perimetro"}}, coherente=True)
    c = fila("VENTAS_LINO_PLANO_2025"); c["perimetro"] = "segmento Francia"
    caso("columna «Total» de una matriz por segmentos declarada como segmento Francia", [c], "FALLO",
         {"VENTAS_LINO_PLANO_2025": {"perimetro"}}, coherente=True)
    c = fila("VENTAS_LINO_PLANO_2025"); c.update(pos="0", literal="598.4", valor_publicado="598.4", perimetro="segmento Francia")
    caso("positivo: columna de Francia de la matriz declarada como segmento Francia", [c], "OK")
    c = fila("VENTAS_LINO_PLANO_2025"); c.update(pos="0", literal="598.4", valor_publicado="598.4", perimetro="segmento Europa central")
    caso("columna de Francia de la matriz declarada como segmento Europa central", [c], "FALLO",
         {"VENTAS_LINO_PLANO_2025": {"perimetro"}}, coherente=True)
    c = fila("VENTAS_LINO_PLANO_2025"); c.update(pos="0", literal="598.4", valor_publicado="598.4")
    # lo detectan dos dimensiones: el perímetro (columna de un segmento) y la columna (no es la «Total»)
    caso("columna de un segmento (Francia) declarada como grupo", [c], "FALLO", {"VENTAS_LINO_PLANO_2025": {"perimetro", "columna"}}, coherente=True)
    c = dict(rou); c["perimetro"] = "grupo"
    caso("perímetro no reconocido", [c], "FALLO", {"DA_ROU_2025": {"perimetro"}}, coherente=True)
    # ---- edición (mutante conjunto: fuente, página, etiqueta, posición, literal y valor de la edición original)
    c = fila("DA_PPA_FR_2023"); o = base["DA_PPA_U23_2023"]
    c.update({k: o[k] for k in ("doc", "pagina", "etiqueta", "ocurrencia", "pos", "literal", "valor_publicado")})
    caso("edición original de 2023 (URD 2023) declarada vigente en lugar del DEU 2024", [c], "FALLO", {"DA_PPA_FR_2023": {"edicion"}}, coherente=True)
    c = fila("DA_PPA_FR_2023"); c["edicion"] = "anterior"
    caso("edición vigente declarada anterior", [c], "FALLO", {"DA_PPA_FR_2023": {"edicion"}}, coherente=True)
    c = fila("DA_PPA_U23_2023"); c["edicion"] = ""
    caso("edición sin declarar", [c], "FALLO", {"DA_PPA_U23_2023": {"edicion"}}, coherente=True)
    f5 = json.loads(json.dumps(fuentes)); f5["fuentes"]["URD2025"]["ejercicio"] = 2024
    caso("fuente con ejercicio declarado distinto del pie de página", [lease], "FALLO", {"CF_LEASE_2025": {"edicion"}}, fu=f5, coherente=True)
    f6 = json.loads(json.dumps(fuentes)); del f6["fuentes"]["URD2025"]["ejercicio"]
    caso("fuente sin ejercicio declarado", [lease], "FALLO", {"CF_LEASE_2025": {"edicion"}}, fu=f6, coherente=True)
    # ---- revisión n.º 3 (N1): columna alineada con la cabecera, modo de la lista cerrada, unidad, perímetro y concepto
    def nueva(rid, **c):
        f = {k: "" for k in lease}
        f.update(id=rid, tipo="tabla", ocurrencia="0", perimetro="consolidado IFRS, grupo Elis", edicion="vigente", unidad="mm EUR",
                 control_anio="dos_columnas", concepto="mutante del revisor", doc="URD2025")
        f.update(c)
        return f
    caso("positivo: total de 2025 en una tabla con tercera columna «Change» (revisión n.º 3, F2)",
         [nueva("MUT_EBITDA_2025_OK", anio="2025", pagina="308", etiqueta="re:^\\s*TOTAL\\s{2,}", pos="-3", literal="1,700.1", valor_publicado="1700.1")], "OK")
    caso("positivo: total de 2024 en esa misma tabla (F3)",
         [nueva("MUT_EBITDA_2024_OK", anio="2024", pagina="308", etiqueta="re:^\\s*TOTAL\\s{2,}", pos="-2", literal="1,609.8", valor_publicado="1609.8")], "OK")
    caso("F1: total de 2024 declarado de 2025 en la tabla con columna «Change»",
         [nueva("MUT_EBITDA_2025", anio="2025", pagina="308", etiqueta="re:^\\s*TOTAL\\s{2,}", pos="-2", literal="1,609.8", valor_publicado="1609.8")],
         "FALLO", {"MUT_EBITDA_2025": {"ejercicio"}}, coherente=True)
    c = dict(rou); c.update(pos="-1", literal="(132.2)", valor_publicado="-132.2", control_anio="crecimiento")
    caso("A1: M1 con el modo declarado «crecimiento»", [c], "FALLO", {"DA_ROU_2025": {"ejercicio"}})
    c = dict(rou); c.update(pos="-1", literal="(132.2)", valor_publicado="-132.2", control_anio="max_cabecera")
    caso("A2: M1 con el modo declarado «max_cabecera»", [c], "FALLO", {"DA_ROU_2025": {"ejercicio"}})
    c = fila("IS_EBIT_FR_2024"); c.update(edicion="vigente", control_anio="crecimiento")
    caso("A4: edición anterior declarada vigente con el modo «crecimiento»", [c], "FALLO", {"IS_EBIT_FR_2024": {"ejercicio"}})
    c = fila("OOIE_PLUSV_2025"); c.update(pos="-1", literal="(1.5)", valor_publicado="-1.5", control_anio="crecimiento")
    caso("H1: plusvalía de 2024 declarada de 2025 con el modo «crecimiento»", [c], "FALLO", {"OOIE_PLUSV_2025": {"ejercicio"}})
    caso("B1: número de acciones declarado en millones de euros",
         [nueva("MUT_ACCIONES", anio="2025", pagina="313", etiqueta="Number of shares, basic (C)", pos="-2", literal="234.0", valor_publicado="234.0")],
         "FALLO", {"MUT_ACCIONES": {"unidad"}}, coherente=True)
    caso("B2: beneficio por acción declarado en millones de euros",
         [nueva("MUT_BPA", anio="2025", pagina="313", etiqueta="re:basic, attributable to owners of the parent = A/C", pos="-2", literal="2.00",
                valor_publicado="2.00")], "FALLO", {"MUT_BPA": {"unidad"}})
    caso("C1: margen de EBITDA de Francia declarado del grupo",
         [nueva("MUT_MARGEN_FR", anio="2025", pagina="308", etiqueta="As a % of revenue", ocurrencia="1", pos="-2", literal="41.9%",
                valor_publicado="41.9", unidad="%")], "FALLO", {"MUT_MARGEN_FR": {"perimetro"}}, coherente=True)
    caso("positivo: margen de EBITDA del grupo (sublínea del TOTAL)",
         [nueva("MUT_MARGEN_GRUPO", anio="2025", pagina="308", etiqueta="As a % of revenue", ocurrencia="7", pos="-2", literal="35.4%",
                valor_publicado="35.4", unidad="%")], "OK")
    c = fila("TAXDIF_INT_2025"); c.update(pos="-5", literal="(0.9)", valor_publicado="-0.9")
    caso("D1: diferido de intangibles de la columna de combinaciones", [c], "FALLO", {"TAXDIF_INT_2025": {"columna"}}, coherente=True)
    c = fila("CREC_ORG_2025"); c.update(pos="-3", literal="+1.8%", valor_publicado="1.8")
    caso("D2: crecimiento externo declarado como orgánico", [c], "FALLO", {"CREC_ORG_2025": {"columna"}}, coherente=True)
    c = fila("LS_NUEVO_PAS_2025"); c.update(pos="-2", literal=fila("LS_NUEVO_ROU_2025")["literal"], valor_publicado=fila("LS_NUEVO_ROU_2025")["valor_publicado"])
    caso("columna del activo ROU declarada como pasivo por arrendamiento", [c], "FALLO", {"LS_NUEVO_PAS_2025": {"columna"}}, coherente=True)
    # ---- adenda de la revisión n.º 3 (contraejemplos de las heurísticas de perímetro y unidad; N9)
    caso("P1: ventas de Alemania (tabla por países) declaradas del grupo",
         [nueva("MUT_ALEMANIA", anio="2025", pagina="346", etiqueta="Germany", ocurrencia="1", pos="-2", literal="621.2", valor_publicado="621.2")],
         "FALLO", {"MUT_ALEMANIA": {"perimetro"}}, coherente=True)
    caso("P2a: ventas del segmento «Other» (tabla de crecimiento) declaradas del grupo",
         [nueva("MUT_OTHER", anio="2025", pagina="307", etiqueta="re:^Other\\s{2,}", pos="0", literal="35.6", valor_publicado="35.6")],
         "FALLO", {"MUT_OTHER": {"perimetro"}}, coherente=True)
    caso("P2b positivo: la misma cifra declarada «segmento Otros segmentos»",
         [nueva("MUT_OTHER_SEG", anio="2025", pagina="307", etiqueta="re:^Other\\s{2,}", pos="0", literal="35.6", valor_publicado="35.6",
                perimetro="segmento Otros segmentos")], "OK")
    caso("U1: número medio ponderado de acciones declarado en millones de euros",
         [nueva("MUT_ACC_MEDIAS", anio="2025", pagina="395", etiqueta="Weighted average number of shares", ocurrencia="1", pos="-2", literal="233,954,020",
                valor_publicado="233954020")], "FALLO", {"MUT_ACC_MEDIAS": {"unidad"}})
    caso("U2: número de acciones suscritas declarado en millones de euros",
         [nueva("MUT_ACC_SUSCR", anio="2025", pagina="362", etiqueta="Number of shares subscribed", ocurrencia="1", pos="-2", literal="889,250",
                valor_publicado="889250")], "FALLO", {"MUT_ACC_SUSCR": {"unidad"}})
    caso("X1 (N9): margen de Francia en una matriz con una celda vacía, declarado «segmento Europa central»",
         [nueva("VENTAS_SEG_MARGEN_X1", anio="2025", pagina="344", etiqueta="Adjusted EBITDA margin", pos="0", literal="41.9%",
                valor_publicado="41.9", unidad="%", control_anio="titulo", perimetro="segmento Europa central")],
         "FALLO", {"VENTAS_SEG_MARGEN_X1": {"perimetro"}}, coherente=True)
    caso("X2 positivo (N9): el mismo margen declarado «segmento Francia»",
         [nueva("VENTAS_SEG_MARGEN_X2", anio="2025", pagina="344", etiqueta="Adjusted EBITDA margin", pos="0", literal="41.9%",
                valor_publicado="41.9", unidad="%", control_anio="titulo", perimetro="segmento Francia")], "OK")
    # ---- combinado (M4 del revisor): año 2031 y unidad falsa en un porcentaje, perímetro falso en las ventas
    c1 = fila("CREC_ORG_2025"); c1.update(anio="2031", unidad="mm EUR")
    c2 = fila("IS_VENTAS_2025"); c2["perimetro"] = "segmento Francia"
    caso("M4: metadatos falsos en dos filas", [c1, c2], "FALLO",
         {"CREC_ORG_2025": {"ejercicio", "unidad", "edicion"}, "IS_VENTAS_2025": {"perimetro"}},
         coherente=True)
    # ---- C9 (tras C7): tabla de la nota 2.4 con la columna del total del ejercicio seguida de columnas por país
    # (URD 2022 p.277) o por sociedad adquirida (URD 2023 p.294). Sobre C7, la columna de Bélgica daba OK en todo.
    caso("positivo C9: total de los flujos netos de adquisiciones de 2021 (columna «12/31/2021», URD 2022 p.277)",
         [nueva("POS_ADQ_NOTA_2021", anio="2021", doc="URD2022", pagina="277", etiqueta="Net cash flow", pos="0", literal="(86.8)",
                valor_publicado="-86.8")], "OK")
    caso("C9: la columna de Bélgica, contigua al total, declarada del grupo",
         [nueva("MUT_ADQ_BELGICA", anio="2021", doc="URD2022", pagina="277", etiqueta="Net cash flow", pos="1", literal="(19.0)",
                valor_publicado="-19.0")], "FALLO", {"MUT_ADQ_BELGICA": {"perimetro"}})
    caso("C9: la columna de Suecia, la última, declarada del grupo",
         [nueva("MUT_ADQ_SUECIA", anio="2021", doc="URD2022", pagina="277", etiqueta="Net cash flow", pos="-1", literal="(1.4)",
                valor_publicado="-1.4")], "FALLO", {"MUT_ADQ_SUECIA": {"perimetro"}})
    caso("C9: la columna de una sociedad adquirida (Textilservice, URD 2023 p.294) declarada del grupo: PENDIENTE, nunca OK",
         [nueva("MUT_ADQ_TEXTIL", anio="2022", doc="URD2023", pagina="294", etiqueta="NET CASH FLOW", pos="1", literal="(25.7)",
                valor_publicado="-25.7")], "PENDIENTE")
    # ---- revisión n.º 4 (C10): P1, formato de recuento sin rótulo de la lista; P2, bloque de un país bajo su título
    caso("P1 (revisión n.º 4): «Effect of conversion of convertible bonds 23,355,764» (URD 2025 p.395) declarado en millones de euros: PENDIENTE, nunca OK",
         [nueva("MUT4_ACC_CONVERSION", anio="2025", pagina="395", etiqueta="re:^\\s*Effect of conversion of convertible bonds\\s{2,}", pos="-2",
                literal="23,355,764", valor_publicado="23355764")], "PENDIENTE")
    caso("P1: «Effect of contingently issuable shares 1,767,869» declarado en millones de euros: PENDIENTE",
         [nueva("MUT4_ACC_CONTINGENTES", anio="2025", pagina="395", etiqueta="re:^\\s*Effect of contingently issuable shares\\s{2,}", pos="-2",
                literal="1,767,869", valor_publicado="1767869")], "PENDIENTE")
    caso("P2 (revisión n.º 4): obligaciones de pensiones de Francia, 45,2, bajo el título «FRANCE – DETAILS» (URD 2025 p.356), declaradas del grupo: PENDIENTE",
         [nueva("MUT4_PENSIONES_FR", anio="2025", pagina="356", etiqueta="TOTAL VALUE OF DEFINED BENEFIT PLAN OBLIGATIONS (1)", ocurrencia="1", pos="-2",
                literal="45.2", valor_publicado="45.2")], "PENDIENTE")
    caso("positivo C10: pasivo neto por planes de prestación definida del grupo, 67,1, total de la tabla por países de esa página",
         [nueva("POS4_PENSIONES_GRUPO", anio="2025", pagina="356", etiqueta="LIABILITIES (ASSETS) RELATED TO DEFINED BENEFIT PLANS", pos="-2",
                literal="67.1", valor_publicado="67.1")], "OK")

    malos = 0
    for k in casos:
        cod, res = ejecutar(a.raiz, k["filas"], k["fuentes"])
        problemas = []
        if res is None:
            problemas.append("el verificador abortó sin informe")
        else:
            por_id = {r["id"]: r for r in res["cifras"]}
            estados = {r["estado"] for r in res["cifras"]}
            global_ = "FALLO" if "FALLO" in estados else ("PENDIENTE" if "PENDIENTE" in estados else "OK")
            if global_ != k["estado"]:
                problemas.append(f"estado {global_}, se esperaba {k['estado']}")
            if cod != CODIGO[k["estado"]]:
                problemas.append(f"código de salida {cod}, se esperaba {CODIGO[k['estado']]}")
            for i, dims in k["fallan"].items():
                r = por_id[i]
                for dim in dims:
                    if r["dimensiones"][dim]["estado"] != "FALLO":
                        problemas.append(f"{i}: la dimensión {dim} no lo detecta ({r['dimensiones'][dim]['estado']})")
                if k["coherente"]:
                    otras = [d for d, v in r["dimensiones"].items() if d not in dims and v["estado"] in ("FALLO", "NO_EVALUADO")]
                    if otras:
                        problemas.append(f"{i}: mutante no aislado; fallan también {otras}")
            if k["motivo"] and not any(k["motivo"] in (r.get("motivo") or "") for r in res["cifras"]):
                problemas.append(f"sin el motivo esperado «{k['motivo']}»")
        malos += bool(problemas)
        print("OK " if not problemas else "MAL", k["nombre"], "→", k["estado"] if not problemas else "; ".join(problemas))
    print(f"{len(casos) - malos}/{len(casos)} casos con el resultado esperado")
    return 1 if malos else 0


if __name__ == "__main__":
    sys.exit(main())
