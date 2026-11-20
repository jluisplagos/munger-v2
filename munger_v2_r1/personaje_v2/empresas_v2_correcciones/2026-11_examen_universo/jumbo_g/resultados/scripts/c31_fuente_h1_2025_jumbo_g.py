#!/usr/bin/env python3
"""jumbo_g · Análisis!C31 con su fuente: el informe semestral H1-2025 de Jumbo («Six months Financial Results for the Period from January 1st, 2025 to
June 30th, 2025», 66 páginas, sha256 0e69fd76…05f60; Release fuentes-examen-20261118 del auxiliar, asset 767753771, e57a_jumbo_h1financialresults2025_en.pdf),
conseguido por la persona responsable el 19-nov-2026 (REVISION_SELLADO.md, auxiliar coordinacion/cierre-v2: C31 era la única entrada material sin comprobar).
Solo el registro: no cambia valores del libro, fases ni la clase de la entrada. El apoyo del veredicto «No» (comparación semestral decidida por el inversor,
Control maestro!M34) se reescribe citando el H1-2025 con página del PDF y cita literal (espacios de maquetación de pdftotext -layout reducidos a uno; cada cita se
comprueba aquí en su página del texto conservado y del PDF). La entrada queda PENDIENTE de revisor, extractor «Claude orquestación», sin vínculo.
Uso: python3 -I c31_fuente_h1_2025_jumbo_g.py CARPETA_EMPRESA RASTRO.json"""
import copy, hashlib, json, os, re, subprocess, sys
C, RASTRO = sys.argv[1:3]
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "..", "..", "..", "..", "scripts"))
import verificacion_entradas as VE  # noqa: E402
HOY, EXT = "2026-11-20", "Claude orquestación"
h = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()  # noqa: E731
H125 = ("pdf/jumbo-h1-2025-financial-results.pdf", "texto/jumbo-h1-2025-financial-results.txt", "0e69fd76217b6dccb4fda1d17a71366c84d57e52c17723c3eb3763f1b6905f60")
H126 = ("pdf/jumbo-h1-2026-financial-results.pdf", "texto/jumbo-h1-2026-financial-results.txt", "84bba93c5f793480fbee53efc68b43922624a2d247e3e471341e44a2ac96b2cd")
for pdf, txt, sha in (H125, H126):
    assert h(os.path.join(C, pdf)) == sha, pdf
norm = lambda s: re.sub(r"\s+", " ", s).strip()  # noqa: E731


def pagina_txt(txt, n):
    t = open(os.path.join(C, txt), encoding="utf-8").read()
    m = re.search(rf"\[PDF PAGE {n}\]\n(.*?)(?=\[PDF PAGE {n + 1}\]\n|\Z)", t, re.S)
    return m.group(1)


def pagina_pdf(pdf, n):
    return subprocess.run(["pdftotext", "-layout", "-f", str(n), "-l", str(n), os.path.join(C, pdf), "-"], check=True, capture_output=True, text=True).stdout


def cita(fuente, n, literal):
    pdf, txt, _ = fuente
    for texto in (pagina_txt(txt, n), pagina_pdf(pdf, n)):
        assert literal in norm(texto), (txt, n, literal)
    return f"«{literal}»"


# ------------------------------------------------------------------------------------------------ citas comprobadas
c_inv8 = cita(H125, 8, "Inventories: Inventories of the Group amounted on 30.06.2025 to € 316,66 mil. compared to € 260,87 mil. as at 31.12.2024")
c_bal23 = cita(H125, 23, "Inventories 316.655.374 260.870.129 232.081.694 194.799.733")
c_cab23 = cita(H125, 23, "THE GROUP THE COMPANY Notes 30/06/2025 31/12/2024 30/06/2025 31/12/2024")
c_deu23 = cita(H125, 23, "90.278.641 77.667.057 receivables 4.11 76.960.832")
c_net50 = cita(H125, 50, "Net trade Receivables 15.390.263 9.792.479 16.862.909 10.498.705")
c_ant50 = cita(H125, 50, "Advances for inventory purchases 74.906.350 67.186.324 74.906.350 67.186.324")
c_tot50 = cita(H125, 50, "Total 90.278.641 76.960.832 91.751.287 77.667.057")
c_ven21 = cita(H125, 21, "Turnover 4.1 497.278.437 460.380.339 423.277.839 381.849.346")
d_inv25 = cita(H126, 25, "Inventories 325.764.610 310.497.568 232.471.805 229.846.997")
d_deu25 = cita(H126, 25, "receivables 4.11 86.024.991 75.235.066 101.436.376 84.079.821")
d_net52 = cita(H126, 52, "Net trade Receivables 15.072.374 8.168.039 30.483.759 17.012.795")
d_ven23 = cita(H126, 23, "Turnover 4.1 519.257.126 497.278.437 442.358.001 423.277.839")

inv, deu, net, ven = (325764610, 316655374), (86024991, 90278641), (15072374, 15390263), (519257126, 497278437)
pct = lambda a: f"{(a[0] / a[1] - 1) * 100:+.2f}".replace(".", ",").replace("-", "−") + " %"  # noqa: E731
assert pct(inv) == "+2,88 %" and pct(deu) == "−4,71 %" and pct(net) == "−2,07 %" and pct(ven) == "+4,42 %"

p = os.path.join(C, VE.REGISTRO)
antes_sha = h(p)
reg = json.load(open(p, encoding="utf-8"))
por = {e["celda"]: e for e in reg["entradas"]}
INST = VE.universo(C)
e = por["Análisis!C31"]
assert e["clase"] == "convencion" and e["valor_modelo"] == "No" == INST["celdas"]["Análisis!C31"]
antes = copy.deepcopy(e)

DOC125 = (f"informe semestral H1-2025 de Jumbo («Six months Financial Results for the Period from January 1st, 2025 to June 30th, 2025», {H125[1]}, PDF "
          f"{H125[0]}, sha256 {H125[2]}, FUENTES.tsv)")
DOC126 = f"informe semestral H1-2026 ({H126[1]}, sha256 {H126[2]})"
e["hipotesis"]["fundamento"] = (
    "Veredicto «No» a «¿Cobros o inventario crecen más rápido que ingresos?» con la comparación semestral (mismo punto estacional: 30-jun-2026 frente a 30-jun-2025), "
    "decidida por el inversor el 11-oct-2026 (Control maestro!M34). Grupo, euros; páginas del PDF (marcas [PDF PAGE n]); citas literales con los espacios de la "
    f"maquetación reducidos a uno. Nivel a 30-jun-2025, del {DOC125}: inventario PDF p. 23, estado de situación (columnas {c_cab23}): {c_bal23}; y p. 8: {c_inv8}. "
    f"Deudores comerciales a 30-jun-2025, p. 23 (la etiqueta «Trade debtors and other trade receivables» ocupa dos líneas y la cifra va desplazada): {c_deu23}; "
    f"desglose en la nota 4.11, p. 50: {c_net50}; {c_ant50}; {c_tot50} (los 90.278.641 son sobre todo anticipos a proveedores; clientes netos 15.390.263). "
    f"Ventas del 1S-2025, p. 21: {c_ven21}. Nivel a 30-jun-2026, del {DOC126}: p. 25: {d_inv25}; {d_deu25}; p. 52: {d_net52}; ventas del 1S-2026, p. 23: {d_ven23}. "
    f"Comparación: inventario 325.764.610 frente a 316.655.374 = {pct(inv)}; deudores comerciales 86.024.991 frente a 90.278.641 = {pct(deu)}; clientes netos "
    f"15.072.374 frente a 15.390.263 = {pct(net)}; ventas 519.257.126 frente a 497.278.437 = {pct(ven)}. Ni el inventario ni los cobros crecen más que las ventas → "
    "«No» (el libro redondea: +2,9 %, −4,7 %, −2,1 %, +4,42 %; Control maestro!M34). Sin factoring ni supplier finance encontrados (Control maestro!M34).")
e["hipotesis"]["alternativas"] = (
    "La comparación anual (31-dic-2025 frente a 31-dic-2024: inventario +19,0 % frente a ventas +7,2 %, AR2025 p. 24) daría BANDERA (Control maestro N34); "
    "el inversor eligió la semestral.")
e["hipotesis"]["limites"] = (
    "Depende del período de comparación elegido (decisión del inversor del 11-oct-2026). Los deudores comerciales totales son sobre todo anticipos a proveedores "
    "(74.906.350 − 17.972 a 30-jun-2025, p. 50); los clientes netos son una partida pequeña. La acumulación de inventario a 31-dic-2025 se vigila (Control maestro N34).")
e["hipotesis"]["procedencia"] = (
    f"Control maestro!L–N34 del libro (Jumbo_v63_evaluada.xlsx; L34 «H1-26 p.25, p.52; H1-25 p.23, p.50»); {H125[1]} [PDF PAGE 8, 21, 23, 50]; "
    f"{H126[1]} [PDF PAGE 23, 25, 52]")
e["incidencia"] = None
c0 = e.get("comprobacion") or {}
nota = ("apoyo reescrito con el informe semestral H1-2025, ya en el expediente (pdf/ y texto/, FUENTES.tsv; sha256 0e69fd76…05f60, Release fuentes-examen-20261118, "
        "asset 767753771): inventario 316.655.374 (PDF p. 23; p. 8 «€ 316,66 mil.»), deudores comerciales 90.278.641 (p. 23 y nota 4.11, p. 50; clientes netos "
        "15.390.263), ventas 497.278.437 (p. 21); con el H1-2026 (p. 23, 25, 52): +2,88 % / −4,71 % / −2,07 % frente a +4,42 % → «No». La clase y el valor no cambian; "
        "la incidencia anterior (sin fuente equivalente; aproximación 317,46) queda sustituida por la cifra publicada 316,66")
e["comprobacion"] = {
    "extractor": EXT, "revisor": None, "fecha": HOY, "resultado": "pendiente",
    "fuente_examinada": f"{H125[1]} [PDF PAGE 8, 21, 23, 50] y {H125[0]}; {H126[1]} [PDF PAGE 23, 25, 52]; Control maestro L–N34",
    "nota": f"[{EXT}, {HOY}, jumbo_g, tras REVISION_SELLADO.md] {nota} · Comprobación anterior: {c0.get('revisor')} {c0.get('fecha')} «{c0.get('resultado')}»: "
            f"{str(c0.get('nota'))[:400]}",
    "vinculo": None}
reg["nota_jumbo_g_c31_h1_2025"] = (f"{HOY}, {EXT}: Análisis!C31 con su fuente, el informe semestral H1-2025 (sha256 0e69fd76…05f60), añadido al expediente; apoyo con "
                                   "página y cita literal; pendiente de revisor. Rastro: resultados/registro_c31_h1_2025_jumbo_g.json")
json.dump(reg, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump({"fecha": HOY, "guion": "resultados/scripts/c31_fuente_h1_2025_jumbo_g.py",
           "fuente_nueva": {"archivo": H125[0], "texto": H125[1], "sha256": H125[2], "paginas": 66,
                            "release": "jluisplagos/munger-v2-evidencias-mistral · fuentes-examen-20261118 · asset 767753771 · e57a_jumbo_h1financialresults2025_en.pdf"},
           "registro_antes_sha256": antes_sha, "registro_despues_sha256": h(p),
           "cambios": [{"celda": "Análisis!C31", "motivo": nota, "antes": antes, "despues": copy.deepcopy(e)}]},
          open(RASTRO, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("cambiada Análisis!C31")
