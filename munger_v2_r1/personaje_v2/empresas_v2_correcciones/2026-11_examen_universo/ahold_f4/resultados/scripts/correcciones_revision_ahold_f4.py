#!/usr/bin/env python3
"""ahold_f4 · correcciones pedidas por la revisión independiente antes de la fase A (munger-v2-evidencias-mistral,
coordinacion/cierre_v2/examen/revisiones/expedientes_f1/REVISION_AHOLD_F4.md @ 19c17a9; encargo del coordinador del 19-nov-2026).
Autor: «Claude orquestación». No toca la etapa 1 original (antecedentes/etapa1_original/): cambia la COPIA DE ENSAYO etapa1/Ahold_evaluada.xlsx,
fase1_metadatos.json (y reconstruye fase1_v63.json con fase1_historia.py construir) y el registro de entradas. Antes copia cada archivo a
antecedentes/revision_ahold_f4/ y guarda los textos anteriores en antecedentes/revision_ahold_f4/evidencia_anterior.json.
  3) Control maestro!M47 (fila CONTROL, decisión de la etapa 1 sustituida por P-O1 c), como se hizo con M43.
  4) C37/C41: el precio cita el histórico oficial de Euronext conservado en fuentes_mercado/ (cierre 36,05 el 13-nov-2026), no Trivano.
  5) C38 (Simply Wall St, «VERIFICAR A OJO», sin bytes): «Dato no verificable».
  6) menores: tabla de Damodaran de EE. UU. (limitación), cash pool nocional en los descubiertos de 2016–2017, guía de FCF rebajada el 4-nov
     en la N de C47, contexto del 2T de C28, C32 y C60 actualizado al 3T (valores sin cambio).
Los puntos 1) y 2) (relevo de extracción con la evidencia al 3T y tabla de vigencia) van en extracto_v63.md: relevo_extraccion_ahold_f4.py.
Uso (desde la carpeta del expediente ahold_f4/): python3 -I resultados/scripts/correcciones_revision_ahold_f4.py Ahold antecedentes resultados/registro_correcciones_revision_ahold_f4.json"""
import copy, hashlib, json, os, shutil, subprocess, sys
C, ANT, REG = sys.argv[1:4]
h = lambda x: hashlib.sha256(open(x, "rb").read()).hexdigest()  # noqa: E731
AQUI_SCRIPTS = os.path.abspath(os.path.join(C, *[".."] * 4, "scripts"))
sys.path.insert(0, AQUI_SCRIPTS)
from v63_xml import LibroV63  # noqa: E402
HOY, EXT = "2026-11-19", "Claude orquestación"
REV = "revisión independiente de ahold_f4 (REVISION_AHOLD_F4.md @ 19c17a9)"
DST = os.path.join(ANT, "revision_ahold_f4")
os.makedirs(DST)
ARCH = {"etapa1/Ahold_evaluada.xlsx": None, "fase1_metadatos.json": None, "fase1_v63.json": None, "verificacion_entradas.json": None}
for a in ARCH:
    shutil.copy2(os.path.join(C, a), os.path.join(DST, os.path.basename(a)))
    ARCH[a] = h(os.path.join(C, a))
anteriores, cambios = {}, []
EUR = "fuentes_mercado/Euronext_AD_NL0011794037_XAMS_historico_NO_AJUSTADO_2026-01-02_a_2026-11-17.txt"
FILA_EUR = "13/11/2026;35.52;36.15;35.43;36.05;36.05;2489661;5867;89623138;35.9981"
assert FILA_EUR in open(os.path.join(C, EUR), encoding="utf-8").read()
assert h(os.path.join(C, EUR)) == "ccea27a1535528822fb92e864e607b09aba1ac4b0257ccd3152afbe0e9b21142"
Q3 = "AD_q3-2026-interim-report.txt"
T3 = " ".join(open(os.path.join(C, "texto", Q3), encoding="utf-8").read().split())
for frase in ("free cash flow of around €2.1 billion (previously at least €2.3 billion)", "Closing carrying amount 8,491", "Total assets 49,856 49,089",
              "23,847,837 of the Company's own shares were repurchased at an average price of €35.41 per share", "Diluted 872 902 880 909"):
    assert frase in T3, frase
T17 = " ".join(open(os.path.join(C, "texto", "AD_annual-report-2017.txt"), encoding="utf-8").read().split())
assert "Bank overdrafts includes an amount of €1,367 million (January 1, 2017: €1,184 million) which relates to the overdraft position of a notional cash pooling" in T17
# ---------------- 3), 5) y 6): copia de ensayo de la etapa 1
e1 = os.path.join(C, "etapa1", "Ahold_evaluada.xlsx")
lb = LibroV63(e1)
filas = {}
for r in range(17, 176):
    b = lb.leer("Control maestro", f"B{r}")
    if isinstance(b, str):
        filas.setdefault(b, []).append(r)


def escribir(ref, texto, que):
    anteriores[f"Control maestro!{ref}"] = lb.leer("Control maestro", ref)
    lb.escribir("Control maestro", ref, texto, tipo="texto")
    cambios.append({"celda": f"Control maestro!{ref}", "de": que, "antes": anteriores[f"Control maestro!{ref}"], "despues": texto})


r47 = [r for r in filas.get("CONTROL", []) if "no se suman (sensibilidad)" in str(lb.leer("Control maestro", f"M{r}"))]
assert r47 == [47], r47
escribir("M47", ("Decisión sustituida por P-O1 (c) «regla espejo» de la persona responsable (18-nov-2026): los cobros que Ahold presenta en inversión SÍ se suman "
                 "(cobros de subarriendos en C49, dividendos de negocios conjuntos en C46, intereses cobrados en C48; ver C46, C48 y C49). En el CFO quedan los "
                 "arrendamientos a corto plazo, de bajo valor y variables (57 en 2025). Texto anterior de la etapa 1 en antecedentes/revision_ahold_f4/evidencia_anterior.json."),
         "3) M47, fila CONTROL: decisión de la etapa 1 sustituida por P-O1 (c)")
(r38,) = filas["Análisis!C38"]
escribir(f"F{r38}", "Dato no verificable", "5) C38: lectura externa sin bytes ni verificación")
escribir(f"N{r38}", ("(ahold_f4, 19-nov-2026) «Dato no verificable»: la etapa 1 pedía «VERIFICAR A OJO en la URL» y decía «si no se confirma → Dato no verificable»; la "
                     "lectura de Simply Wall St no tiene bytes en el expediente ni se ha verificado (" + REV + "). Contexto de la etapa 1: un 63 % por encima del precio "
                     "objetivo medio de analistas (37,55 €; 18 analistas; rango 22,63–44; secundaria). Confianza media."), "5) C38")
(r47c,) = filas["Análisis!C47"]
n47 = lb.leer("Control maestro", f"N{r47c}")
assert n47.endswith("Guía 2026: FCF de la empresa ≥ 2.300, capex ~2.700 (guía)."), n47
escribir(f"N{r47c}", n47 + (" (ahold_f4, 19-nov-2026) Guía rebajada el 4-nov-2026 en el informe del 3T: FCF de la empresa de unos 2.100 en 2026 (antes al menos 2.300), "
                            "base de 53 semanas [AD_q3-2026-interim-report.txt, PDF p. 2 y 5]. «LTM: circulante desfavorable del 1S26» es evidencia del 2T; con el 3T, FCF "
                            "de la empresa acumulado 747 frente a 1.104 en 2025, por el circulante (calendario y estacionalidad) [AD_q3-2026-interim-report.txt, PDF p. 10 y 24]."),
         "6) C47: guía de FCF del 4-nov")
(r28,) = filas["Análisis!C28"]
escribir(f"J{r28}", "Informes anuales 2020–25; Q3-26", "6) C28: contexto al 3T")
escribir(f"L{r28}", "Notas de BPA; Q3-26 PDF p. 12 y 21", "6) C28: contexto al 3T")
escribir(f"N{r28}", ("Entregas a empleados desde autocartera (2,1–3,4 M acciones/año) frente a 28,8–45,6 M recompradas. SBC ≈ 55 M€/año. (ahold_f4, 19-nov-2026) Con "
                     "el 3T: 23.847.837 acciones recompradas en 2026 hasta el 27-sep a 35,41 € de media, 865.173.863 en circulación a esa fecha (886.877.259 a "
                     "28-dic-2025) [AD_q3-2026-interim-report.txt, PDF p. 21]; media diluida de 39 semanas 880 M (909 M en 2025) [AD_q3-2026-interim-report.txt, PDF p. 12]. "
                     "El «1S26 (−3,2 % interanual)» de M es del 2T. Valor sin cambio. Confianza alta."), "6) C28: contexto al 3T")
(r32,) = filas["Análisis!C32"]
n32 = lb.leer("Control maestro", f"N{r32}")
assert n32.startswith("Q2-26 (sin auditar): 17,1%. ")
escribir(f"N{r32}", ("(ahold_f4, 19-nov-2026) Q3-26 (sin auditar): fondo de comercio 8.491 ÷ activo total 49.856 = 17,0 % [AD_q3-2026-interim-report.txt, PDF p. 14 y 18] "
                     "(con el 2T era 17,1 %); valor sin cambio (balance auditado de 2025). " + n32[len("Q2-26 (sin auditar): 17,1%. "):]), "6) C32: contexto al 3T")
(r60,) = filas["Análisis!C60"]
escribir(f"N{r60}", ("(ahold_f4, 19-nov-2026) Valor sin cambio (FY2022→FY2025 y FY2020→FY2025). Con el 3T: media diluida de 39 semanas 880 M frente a 909 M en 2025 "
                     "[AD_q3-2026-interim-report.txt, PDF p. 12]; el «−3,25 a −3,30 % con Q2-26 o 1S26 como punto final» de la etapa 1 era la lectura del 2T. Confianza alta."),
         "6) C60: contexto al 3T")
lb.marcar_modificada("Control maestro")
lb.guardar(e1)
# comprobación: solo cambian las celdas declaradas
import openpyxl  # noqa: E402
w_o, w_n = openpyxl.load_workbook(os.path.join(DST, "Ahold_evaluada.xlsx"), data_only=True), openpyxl.load_workbook(e1, data_only=True)
otras = [f"{hj}!{c.coordinate}" for hj in w_o.sheetnames for fila in w_o[hj].iter_rows() for c in fila
         if f"{hj}!{c.coordinate}" not in anteriores and w_n[hj][c.coordinate].value != c.value]
assert not otras, otras[:10]
# ---------------- 4) y 6): metadatos y reconstrucción de fase1_v63.json
mp = os.path.join(C, "fase1_metadatos.json")
meta = json.load(open(mp, encoding="utf-8"))
antes_meta = copy.deepcopy(meta)
pr = meta["precio"]
assert pr["valor"] == 36.05 and pr["fecha"] == "2026-11-13" and pr["fuente"].startswith("Trivano")
pr["fuente"] = ("Euronext Live, histórico oficial NO AJUSTADO de Ahold Delhaize (ISIN NL0011794037, Euronext Amsterdam), sesión del 13/11/2026: cierre 36,05 EUR "
                f"({EUR}, sha256 ccea27a1535528822fb92e864e607b09aba1ac4b0257ccd3152afbe0e9b21142, conservado en el expediente; HUELLAS.txt). Es la fecha del precio "
                "del expediente; la sesión más reciente del archivo es la del 17/11/2026 (35,14). Sin dividendo pendiente en esas fechas (último: ex-date 07/08/2026). "
                "El agente de metadatos lo había tomado de Trivano (36,05 EUR, +2,12 %), una fuente secundaria que ya no se usa.")
pr["pagina"] = f"{EUR}, fila del 13/11/2026"
pr["literal"] = FILA_EUR
cap = meta["capitalizacion"]
viejo = "36,05 € (precio de los metadatos de la fase 1, 13-nov-2026; pendiente de fuente oficial, sin cambio)"
assert cap["fuente"].startswith(viejo)
cap["fuente"] = ("36,05 € (cierre oficial de Euronext Amsterdam del 13-nov-2026, histórico no ajustado conservado en fuentes_mercado/)" + cap["fuente"][len(viejo):]
                 + " Z-ACC (19-nov-2026): con las 865.173.863 acciones a 27-sep-2026 (Q3-2026 PDF p. 21) sería 31.189,5 mm.")
n0 = meta["_notas"][0]
assert n0.startswith("Precio: no se obtuvo cotización")
meta["_notas"][0] = ("Precio (ahold_f4, 19-nov-2026): 36,05 € es el cierre oficial del 13-nov-2026 del histórico no ajustado de Euronext conservado en fuentes_mercado/ "
                     "(sustituye la cita de Trivano del agente de metadatos; " + REV + ").")
meta["_notas"] += [
    ("(ahold_f4, 19-nov-2026) Sector de Damodaran (Palancas!C7): «Retail (Grocery and Food)» sale de la tabla «Margins by industry» de empresas de EE. UU. "
     "(damodaran_margin.xls, hoja «Industry Averages», fila 83, datos de enero de 2026), la que la persona responsable subió a la Release fuentes-examen-20261118. "
     "Limitación: Ahold vende el 57 % en EE. UU. y el resto en Europa (Países Bajos, Bélgica y Europa central y oriental) e Indonesia; la tabla europea de Damodaran "
     "no está en el expediente, así que no se ha contrastado la clasificación ni sus cifras con ella."),
    ("(ahold_f4, 19-nov-2026) Deuda 2016–2017 (Historia C22 y D22, A-NIC17): los descubiertos bancarios (1.196 en 2016 y 1.368 en 2017) incluyen 1.184 y 1.367 de "
     "un cash pool nocional compensado por un importe igual en la caja [AD_annual-report-2017.txt, PDF p. 191; AD_annual-report-2018.txt, PDF p. 156]: inflan a la vez la "
     "deuda bruta y la caja de esos años; la deuda neta no cambia.")]
json.dump(meta, open(mp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
r = subprocess.run([sys.executable, "-B", os.path.join(AQUI_SCRIPTS, "fase1_historia.py"), "construir", C], capture_output=True, text=True)
assert r.returncode == 0, (r.stdout + r.stderr)[-800:]
f_o = json.load(open(os.path.join(DST, "fase1_v63.json"), encoding="utf-8"))
f_n = json.load(open(os.path.join(C, "fase1_v63.json"), encoding="utf-8"))
dif = sorted(k for k in set(f_o) | set(f_n) if f_o.get(k) != f_n.get(k))
assert set(dif) <= {"precio", "capitalizacion", "_notas"}, dif
# ---------------- registro de entradas
p = os.path.join(C, "verificacion_entradas.json")
d = json.load(open(p, encoding="utf-8"))
E = {e["celda"]: e for e in d["entradas"]}
reg = []


def pendiente(celda, nota, cambiar=None):
    e = E[celda]
    antes = copy.deepcopy(e)
    if cambiar:
        cambiar(e)
    c0 = e.get("comprobacion") or {}
    e["comprobacion"] = {"extractor": EXT, "revisor": None, "fecha": HOY, "resultado": "pendiente", "fuente_examinada": None,
                         "nota": f"[{EXT}, {HOY}, ahold_f4, {REV}] {nota} · Comprobación anterior: {c0.get('revisor')} {c0.get('fecha')} «{c0.get('resultado')}»: {str(c0.get('nota'))[:400]}",
                         "vinculo": None}
    reg.append({"celda": celda, "antes": antes, "despues": copy.deepcopy(e)})


pendiente("Análisis!C37", "la evidencia del Control maestro (J, L y M, escritas desde los metadatos) cita ya el histórico oficial de Euronext conservado (cierre 36,05 del 13-nov-2026), no Trivano; la fuente del registro no cambia")
pendiente("Análisis!C41", "la evidencia del Control maestro (J) cita ya el cierre oficial de Euronext del precio y la capitalización con las acciones a 27-sep-2026 (Z-ACC); valor y fórmula sin cambio")
pendiente("Análisis!C38", "Control maestro F = «Dato no verificable» (lectura externa sin bytes ni verificación); sigue siendo una lectura externa: no cuenta como comprobada")
pendiente("Análisis!C47", "N del Control maestro con la guía de FCF rebajada el 4-nov-2026 (Q3-26 PDF p. 2 y 5) y el contexto del 3T; valor y cálculo sin cambio")
for c, que in (("Análisis!C28", "J, L y N"), ("Análisis!C32", "N"), ("Análisis!C60", "N")):
    pendiente(c, f"contexto del 2T del Control maestro ({que}) actualizado al 3T; valor sin cambio")


def c7(e):
    e["fuente"]["tratamiento"] += ("; la tabla es la que subió la persona responsable (Release fuentes-examen-20261118). Limitación: Ahold vende el 57 % en EE. UU. y el resto en "
                                   "Europa e Indonesia; la tabla europea de Damodaran no está en el expediente y la clasificación no se ha contrastado con ella")


pendiente("Palancas!C7", "limitación de la tabla de EE. UU. declarada en el tratamiento", c7)
for celda, anio, cp, pag in (("Historia!C22", 2016, "1.184 de los 1.196", "AD_annual-report-2017.txt [PDF PAGE 191]"), ("Historia!D22", 2017, "1.367 de los 1.368", "AD_annual-report-2017.txt [PDF PAGE 191] y AD_annual-report-2018.txt [PDF PAGE 156]")):
    def nic(e, anio=anio, cp=cp, pag=pag):
        e["derivacion"]["conciliacion"] += (f" · Cash pool nocional: de los descubiertos de {anio}, {cp} son la posición deudora de un cash pool nocional compensado por un importe igual "
                                            f"en la caja ({pag}): inflan a la vez la deuda bruta y la caja; la deuda neta no cambia (" + REV + ").")
    pendiente(celda, "cash pool nocional de los descubiertos declarado en la conciliación", nic)
d["nota_de_la_orquestacion"] += (f" (ahold_f4, {HOY}, {REV}) {EXT} cambió {len(reg)} entradas más (resultados/registro_correcciones_revision_ahold_f4.json): C37, C41, C38, C47, "
                                 "C28, C32, C60 (evidencia del Control maestro), Palancas!C7 (limitación) y Historia C22/D22 (cash pool); pendientes de otro revisor.")
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
json.dump({"valores_y_textos_anteriores": anteriores, "metadatos_antes": {k: antes_meta[k] for k in ("precio", "capitalizacion", "_notas")}},
          open(os.path.join(DST, "evidencia_anterior.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
json.dump({"fecha": HOY, "guion": os.path.abspath(__file__), "revision": REV, "antes_sha256": ARCH,
           "despues_sha256": {a: h(os.path.join(C, a)) for a in ARCH}, "copia_de_los_anteriores": os.path.relpath(DST, os.path.dirname(C)),
           "control_maestro": cambios, "fase1_v63_claves_cambiadas": dif, "registro_entradas_cambiadas": [x["celda"] for x in reg], "registro_cambios": reg},
          open(REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
print("control maestro", len(cambios), "· fase1_v63", dif, "· registro", len(reg))
