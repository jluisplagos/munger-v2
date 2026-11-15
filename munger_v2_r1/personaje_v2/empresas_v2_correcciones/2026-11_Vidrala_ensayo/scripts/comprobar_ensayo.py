#!/usr/bin/env python3
"""Munger v2 · entrega 4.4 · comprobaciones del expediente de ensayo de Vidrala (solo lectura sobre el paquete).

Comprueba, sin escribir en el paquete (las pruebas de construir se hacen en copias temporales que se borran):
  1. Huellas de las fuentes nuevas (cuentas consolidadas 2016–2022, OIR del dividendo 2275, OIR de la CNMV de la liberada) y de las
     de entregas anteriores que se reutilizan (cuentas 2023, 2024 y 2025).
  2. Que los diez textos de texto/ se reproducen byte a byte convirtiendo esos PDF con personaje_v2/scripts/pdf_a_texto.py.
  3. Que las versiones nuevas de fase1_partes/AR_*.json solo difieren de las originales en: 39 «cita» añadidas a ceros heredados
     y las dos páginas de D&A de AR_2024.json (4 → 7, P8).
  4. comprobar-anio de los diez años: OK, con 38 ceros PENDIENTES (sin confirmar; la IA no confirma ceros).
  5. Estado del expediente: sin fase1_v63.json (se generará con construir), fase1_decisiones.json idéntico al original (sin P1),
     libro base idéntico al original, pipeline detenido en el paso 2.
  6. construir en una copia temporal: Historia con los mismos valores que la original.
  7. construir en otra copia temporal con una decisión SIMULADA de P1 (sin persona, sin fecha, marcada como simulación): solo cambia
     el circulante de 2024 (−127,84 → 84,994). Es una prueba del mecanismo, no un registro humano ni un resultado del ensayo.
  8. Hechos del dividendo a cuenta y de la liberada de 2026 citados en RESOLUCION_DIVIDENDO_Y_ACCIONES.md.
  9. Integridad de los originales de empresas_v2/Vidrala/ frente al manifiesto del paquete.
Ejecutar con «python3 -I». Código 0 si todo cumple.
"""
import glob
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
import html

sys.dont_write_bytecode = True
AQUI = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PV2 = os.path.abspath(os.path.join(AQUI, "..", ".."))
RAIZ = os.path.dirname(PV2)
E = os.path.join(AQUI, "Vidrala")
O = os.path.join(PV2, "empresas_v2", "Vidrala")
SCR = os.path.join(PV2, "scripts")
F = os.path.join(AQUI, "fuentes")
N_OK = N_T = 0


def comprobar(nombre, cond, detalle=""):
    global N_OK, N_T
    N_T += 1
    N_OK += bool(cond)
    print(f"  [{'CUMPLE' if cond else 'NO CUMPLE'}] {nombre}" + (f" · {detalle}" if detalle else ""))


def sha(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def corre(args, cwd=None):
    r = subprocess.run([sys.executable, "-I"] + args, capture_output=True, text=True, cwd=cwd)
    return r.returncode, r.stdout + r.stderr


print("EXPEDIENTE DE ENSAYO DE VIDRALA · entrega 4.4 · comprobaciones de solo lectura")
print("=" * 100)
print("\n1. HUELLAS DE LAS FUENTES")
PDF = {
    2016: (os.path.join(F, "cuentas_consolidadas_2016_2022", "1279_en-2016_consolidated_financial_information.pdf"), "53849fe52385ae7e62a0806bb4ba0e8f06c9fe0a6778cd335bd58b0e70940b7b"),
    2017: (os.path.join(F, "cuentas_consolidadas_2016_2022", "1285_en-2017_consolidated_financial_information.pdf"), "da068c8b28642e59bfc498893b46b3a853a8a1c4707522d39fa4f4b5d4bac6ae"),
    2018: (os.path.join(F, "cuentas_consolidadas_2016_2022", "1291_en-2018_consolidated_financial_information.pdf"), "907687f9e3f05df84099fdf84638ba64ea643373d8bd1958cba1af5732308492"),
    2019: (os.path.join(F, "cuentas_consolidadas_2016_2022", "1297_en-2019_consolidated_financial_information.pdf"), "9c38b260482bb501673b0bb1a0382846405fb4d4ee636d668a4e5ed64814a6c3"),
    2020: (os.path.join(F, "cuentas_consolidadas_2016_2022", "1304_en-2020_consolidated_financial_information.pdf"), "35264bc723624779682c504b9e7057f85aaf11b68600a7b351a128c08188b10e"),
    2021: (os.path.join(F, "cuentas_consolidadas_2016_2022", "1413_en-2021_consolidated_financial_information.pdf"), "2b966a4188615e6dfce4ee1051c2314c5faec9c272f27ea4525763a5f3958494"),
    2022: (os.path.join(F, "cuentas_consolidadas_2016_2022", "1668_en-2022_consolidated_financial_information.pdf"), "180b3608c7e910a8010018bb40b33f0808ff1247170acef38c783d65aeb8382b"),
    2023: (glob.glob(os.path.join(RAIZ, "contrastes", "vidrala_2023_arrendamientos", "fuentes", "en_1831_*", "*.pdf"))[0], None),
    2024: (glob.glob(os.path.join(RAIZ, "contrastes", "vidrala_2023_arrendamientos", "fuentes", "en_2145_*", "*.pdf"))[0], None),
    2025: (glob.glob(os.path.join(RAIZ, "contrastes", "piloto_Vidrala_2025", "fuentes", "en_2355_*", "*.pdf"))[0], None),
}
for a, (p, h) in sorted(PDF.items()):
    if h:
        comprobar(f"{a}: {os.path.basename(p)} · SHA-256 {h[:12]}…", os.path.exists(p) and sha(p) == h)
    else:
        print(f"  {a}: {os.path.relpath(p, RAIZ)} (conservado en una entrega anterior) · SHA-256 {sha(p)[:12]}…")
OIR = os.path.join(F, "dividendo_2275", "2275_es-otra_informacion_relevante.pdf")
CNMV = os.path.join(F, "cnmv_liberada_2026", "CNMV_OIR_Vidrala_ampliacion_liberada_2026_5b51ba57.pdf")
comprobar("OIR del dividendo a cuenta (vidrala.com, doc. 2275) · SHA-256 cbaff23e…", sha(OIR) == "cbaff23e640718620fd43e7dfb18e9222a4c90fb34e1ce684abdc9c6dc83e25e")
comprobar("OIR de la liberada 2026 (CNMV, documento {5b51ba57…}) · SHA-256 3259cf30…", sha(CNMV) == "3259cf30e9bb9985648c4abbd9e37c32b9cc37409cd946eaf140a17a9a93c29d")

tmp = tempfile.mkdtemp(prefix="ensayo44_")
try:
    print("\n2. TEXTOS DE texto/ REPRODUCIBLES DESDE LOS PDF")
    os.makedirs(os.path.join(tmp, "conv", "pdf"))
    for a, (p, _) in PDF.items():
        shutil.copy(p, os.path.join(tmp, "conv", "pdf", f"CF_{a}.pdf"))
    rc, out = corre([os.path.join(SCR, "pdf_a_texto.py"), os.path.join(tmp, "conv")])
    comprobar("pdf_a_texto.py convierte los diez PDF sin avisos", rc == 0, f"código {rc}")
    for a in sorted(PDF):
        t1, t2 = os.path.join(tmp, "conv", "texto", f"CF_{a}.txt"), os.path.join(E, "texto", f"CF_{a}.txt")
        comprobar(f"texto/CF_{a}.txt idéntico a la conversión del PDF", os.path.exists(t2) and sha(t1) == sha(t2), sha(t2)[:12] + "…")
    for a, rel in ((2023, "contrastes/vidrala_2023_arrendamientos/textos_nuevos/CF_2023_EXTRACCION_NUEVA.txt"),
                   (2024, "contrastes/vidrala_2023_arrendamientos/textos_nuevos/CF_2024_EXTRACCION_NUEVA.txt"),
                   (2025, "contrastes/piloto_Vidrala_2025/fuentes/texto_nuevo_CF_2025/CF_2025_EXTRACCION_NUEVA.txt")):
        comprobar(f"CF_{a}.txt idéntico al texto nuevo de la entrega anterior ({os.path.basename(rel)})", sha(os.path.join(E, "texto", f"CF_{a}.txt")) == sha(os.path.join(RAIZ, rel)))

    print("\n3. VERSIONES NUEVAS DE fase1_partes/AR_*.json FRENTE A LAS ORIGINALES")

    def hojas(x, r=""):
        if isinstance(x, dict):
            for k, v in x.items():
                yield from hojas(v, f"{r}.{k}")
        elif isinstance(x, list):
            for i, v in enumerate(x):
                yield from hojas(v, f"{r}[{i}]")
        else:
            yield r, x
    citas, paginas, otras = 0, 0, []
    for f in sorted(glob.glob(os.path.join(O, "fase1_partes", "AR_*.json"))):
        a = dict(hojas(json.load(open(f, encoding="utf-8"))))
        b = dict(hojas(json.load(open(os.path.join(E, "fase1_partes", os.path.basename(f)), encoding="utf-8"))))
        for k in sorted(set(a) | set(b)):
            if a.get(k, "<ausente>") == b.get(k, "<ausente>"):
                continue
            if re.fullmatch(r"\.partidas\.\w+\.cero\.cita", k) and k not in a:
                citas += 1
            elif os.path.basename(f) == "AR_2024.json" and k in (".partidas.da.actual[0].pagina", ".partidas.da.anterior[0].pagina") and a[k] == 4 and b[k] == 7:
                paginas += 1
            else:
                otras.append(f"{os.path.basename(f)}{k}")
    comprobar("39 «cita» añadidas a ceros heredados (re-extracción solo de esas partidas)", citas == 39, str(citas))
    comprobar("2 páginas de D&A de AR_2024.json corregidas 4 → 7 (P8, tipo A, sin tocar importes)", paginas == 2, str(paginas))
    comprobar("Ninguna otra diferencia (importes, líneas, signos, notas)", not otras, "; ".join(otras[:5]))

    print("\n4. comprobar-anio DE LOS DIEZ AÑOS (expediente de ensayo)")
    pend = 0
    for a in sorted(PDF):
        rc, out = corre([os.path.join(SCR, "fase1_historia.py"), "comprobar-anio", E, str(a)])
        n = out.count("PENDIENTE:")
        pend += n
        comprobar(f"{a}: OK", rc == 0 and out.startswith("OK"), f"{n} ceros PENDIENTES")
    comprobar("38 ceros PENDIENTES de verificación en total (39 ceros con cita; el de adquisiciones de 2023 no se usa porque hay cifra)", pend == 38, str(pend))

    print("\n5. ESTADO DEL EXPEDIENTE DE ENSAYO")
    comprobar("No hay fase1_v63.json: el paso 2 del pipeline lo generará con construir", not os.path.exists(os.path.join(E, "fase1_v63.json")))
    comprobar("fase1_decisiones.json idéntico al original (registro humano; sin P1)", sha(os.path.join(E, "fase1_decisiones.json")) == sha(os.path.join(O, "fase1_decisiones.json")))
    for f in ("fase1_fuentes.json", "fase1_metadatos.json", "fase1_listas.md"):
        comprobar(f"{f} idéntico al original", sha(os.path.join(E, f)) == sha(os.path.join(O, f)))
    comprobar("etapa1/ idéntico al original", all(sha(p) == sha(os.path.join(O, "etapa1", os.path.relpath(p, os.path.join(E, "etapa1"))))
                                                   for p in glob.glob(os.path.join(E, "etapa1", "**", "*"), recursive=True) if os.path.isfile(p)))
    st = json.load(open(os.path.join(E, "estado_pipeline.json"), encoding="utf-8"))
    comprobar("Pipeline detenido en el paso 2 sin estado final (pasos 0 y 1 ejecutados)", st["paso"] == 2 and st["estado_analisis"] is None)
    import openpyxl
    wa = openpyxl.load_workbook(os.path.join(O, "Vidrala_v63_base.xlsx"))
    wb = openpyxl.load_workbook(os.path.join(E, "Vidrala_v63_base.xlsx"))
    dif = sum(1 for s in wa.sheetnames for row in wa[s].iter_rows() for c in row if c.value != wb[s][c.coordinate].value)
    comprobar("Libro base (migración de la etapa 1) idéntico celda a celda al original", dif == 0, f"{dif} diferencias")

    print("\n6. construir EN UNA COPIA TEMPORAL (sin P1)")

    def construir_copia(nombre, decision=None):
        d = os.path.join(tmp, nombre, "Vidrala")
        shutil.copytree(E, d)
        if decision:
            dec = json.load(open(os.path.join(d, "fase1_decisiones.json"), encoding="utf-8"))
            dec.update(decision)
            json.dump(dec, open(os.path.join(d, "fase1_decisiones.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        rc, out = corre([os.path.join(SCR, "fase1_historia.py"), "construir", d])
        return rc, out, (json.load(open(os.path.join(d, "fase1_v63.json"), encoding="utf-8")) if rc == 0 else None)

    orig = json.load(open(os.path.join(O, "fase1_v63.json"), encoding="utf-8"))
    rc, out, n1 = construir_copia("c1")
    comprobar("construir termina con código 0", rc == 0, out.strip().splitlines()[-1][:160] if out.strip() else "")
    vo = {k: v["valores"] for k, v in orig["historia"]["partidas"].items()}
    v1 = {k: v["valores"] for k, v in n1["historia"]["partidas"].items()} if n1 else {}
    comprobar("Historia: mismos años y mismos valores que la original en las 22 partidas", n1 and orig["historia"]["anios"] == n1["historia"]["anios"] and vo == v1)
    comprobar("Metadatos (precio, acciones, capitalización, fecha) iguales a los originales",
              n1 and all(orig[k] == n1[k] for k in ("precio", "acciones_diluidas", "capitalizacion", "fecha_analisis")))

    print("\n7. construir CON UNA DECISIÓN SIMULADA DE P1 (prueba del mecanismo; no es un registro humano)")
    sim = {"circulante_lineas": {"2024": {"valor_mm": 84.994, "fuente": "SIMULACIÓN DE PRUEBA EN COPIA TEMPORAL, no es una decisión humana: CF_2024 ES doc. 2118 p.14"}}}
    rc, out, n2 = construir_copia("c2", sim)
    v2 = {k: v["valores"] for k, v in n2["historia"]["partidas"].items()} if n2 else {}
    difs = [(k, i) for k in vo for i, (x, y) in enumerate(zip(vo[k], v2.get(k, []))) if x != y]
    comprobar("Con la decisión simulada solo cambia el circulante de 2024", difs == [("circulante", 8)], str(difs))
    comprobar("Circulante de 2024: −127,84 → 84,994", n2 and vo["circulante"][8] == -127.84 and v2["circulante"][8] == 84.994)

    prop = json.load(open(os.path.join(AQUI, "PROPUESTA_fase1_decisiones_con_P1.json"), encoding="utf-8"))
    actual = json.load(open(os.path.join(E, "fase1_decisiones.json"), encoding="utf-8"))
    extra = {k: v for k, v in prop.items() if k not in actual}
    comprobar("La propuesta de fase1_decisiones.json solo añade circulante_lineas 2024 = 84,994 (fecha y persona vacías, para la persona)",
              all(prop[k] == actual[k] for k in actual) and list(extra) == ["circulante_lineas"] and extra["circulante_lineas"]["2024"]["valor_mm"] == 84.994
              and extra["circulante_lineas"]["2024"]["fecha"] == "" and extra["circulante_lineas"]["2024"]["confirmado_por"] == "")

    print("\n8. DIVIDENDO A CUENTA Y LIBERADA DE 2026 (hechos citados)")
    oir = subprocess.run(["pdftotext", "-layout", OIR, "-"], capture_output=True, text=True).stdout
    o1 = re.sub(r"\s+", " ", oir)
    for frase in ("en su reunión celebrada el 17 de diciembre de 2025", "1,2318 euros brutos por acción", "Last trading date: 10 de febrero de 2026",
                  "Ex-date: 11 de febrero de 2026", "Record date: 12 de febrero de 2026", "Fecha de desembolso: 13 de febrero de 2026", "Llodio, 18 de diciembre de 2025"):
        comprobar(f"OIR 2275: «{frase}»", frase in o1)
    cn = re.sub(r"\s+", " ", subprocess.run(["pdftotext", "-layout", CNMV, "-"], capture_output=True, text=True).stdout)
    for frase in ("29 de octubre de 2026: Inicio del periodo de negociación de los derechos de asignación gratuita",
                  "11 de noviembre de 2026: Fin del periodo de negociación de los derechos de asignación gratuita",
                  "existen en circulación TREINTA Y CINCO MILLONES DOSCIENTAS SEIS MIL DOSCIENTAS CINCUENTA Y OCHO (35.206.258) acciones",
                  "(1.760.312) nuevas acciones", "Llodio, 20 de octubre de 2026",
                  "una vez finalice el período de asignación gratuita, formalice contablemente",
                  "desde la fecha de inscripción en los registros contables de Iberclear"):
        comprobar(f"OIR de la CNMV: «{frase[:90]}»", frase in cn)
    T = os.path.join(RAIZ, "contrastes", "piloto_Vidrala_2025", "fuentes", "texto_nuevo_CF_2025", "CF_2025_EXTRACCION_NUEVA.txt")
    t = open(T, encoding="utf-8").read()
    p = re.split(r"^\[PDF PAGE (\d+)\]\n", t, flags=re.M)
    P = {int(p[i]): re.sub(r"\s+", " ", p[i + 1]) for i in range(1, len(p), 2)}
    comprobar("EN25 p.70: «Dividends to shareholders (Note 15) 43,338 37,547» dentro de proveedores y otras cuentas a pagar", "Dividends to shareholders (Note 15) 43,338 37,547" in P[70])
    comprobar("EN25 p.67: «Dividends payables (Note 17) 37,547 (37,547) - 43,338 43,338» en la conciliación NIC 7", "Dividends payables (Note 17) 37,547 (37,547) - 43,338 43,338" in P[67])
    comprobar("EN25 p.64: el consejo del 19-dic-2025 aprobó el dividendo (el OIR dice 17-dic: discrepancia documental de fecha)", "On 19 December 2025, the Board of Directors" in P[64])
    comprobar("EN25 p.3: el dividendo a cuenta (43,338) reduce el patrimonio a 31-dic-2025", "Interim dividend distributed during the year (43,338) (37,547)" in P[3])
    z = zipfile.ZipFile(os.path.join(RAIZ, "contrastes", "vidrala_revision_financiera", "fuentes", "esef_2025_completo", "2311_en-2025_esef_consolidated_information.zip"))
    x = z.read([n for n in z.namelist() if n.endswith(".xhtml")][0]).decode("utf-8")
    tx = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", x)))
    comprobar("ESEF (español): «El Consejo de Administración de la Sociedad dominante de fecha 19 de diciembre de 2025»", "Consejo de Administración de la Sociedad dominante de fecha 19 de diciembre de 2025" in tx)
    acc = 43338244.48 / 1.2318
    comprobar("43.338.244,48 € ÷ 1,2318 €/acción ≈ 35.182.858 acciones = emitidas (35.206.258) − autocartera a 31-dic-2025 (23.400)", abs(acc - (35206258 - 23400)) < 1, f"{acc:,.1f}")

    print("\n9. ORIGINALES INTACTOS")
    man = {}
    for l in open(os.path.join(RAIZ, "MANIFIESTO_SHA256.txt"), encoding="utf-8"):
        if l.strip() and not l.startswith("#"):
            h, pth = l.rstrip("\n").split("  ", 1)
            man[pth] = h
    org = {k: v for k, v in man.items() if k.startswith("personaje_v2/empresas_v2/Vidrala/")}
    comprobar(f"Los {len(org)} archivos de empresas_v2/Vidrala/ conservan su huella del manifiesto", org and all(sha(os.path.join(RAIZ, k)) == v for k, v in org.items()))
finally:
    shutil.rmtree(tmp, ignore_errors=True)
print(f"\nRESULTADO: {N_OK} de {N_T} comprobaciones cumplen.")
sys.exit(0 if N_OK == N_T else 1)
