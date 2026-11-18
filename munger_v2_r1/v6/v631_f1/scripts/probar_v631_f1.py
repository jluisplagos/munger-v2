#!/usr/bin/env python3
"""Pruebas de la plantilla V6.3.1 F1 (F1-IMPL, recomendación (a) de la revisión).

Uso (desde cualquier carpeta):
  python3 -I probar_v631_f1.py estructura                 sin LibreOffice
  flock /home/user/e_work/libreoffice.lock python3 -I probar_v631_f1.py a0 DESTINO     con LibreOffice (DESTINO: carpeta nueva fuera del repo)

estructura: reconstrucción determinista (mismo SHA-256 que el entregable y que el origen de la referencia); la V6.3 sin cambios; la
  referencia de la V6.3.1 frente a la de la V6.3 difiere EXACTAMENTE en las celdas previstas (fórmulas de la fila 30, C53, C58, C76,
  Motor E205 y Panel A1; fórmulas nuevas C88:L89; tres etiquetas; la sección nueva A84:S90; dos validaciones; inventario + C85:L87 y
  M85:S87); con A0 las fórmulas de C53, C58 y C76 contienen literalmente las de la V6.3; el verificador de la V6.3.1 acepta la plantilla y
  rechaza una mutación, y el de la V6.3 la rechaza.
f1: (LibreOffice) el libro calcula el perímetro declarado y la capa motor_a_f1.py es su oráculo. Elis con A1_sin_ROU y A2_propio aplicados
  desde la declaración (f1_libro_v631.aplicar): f, C53 y los 33 flujos del Motor coinciden con los valores E9 del frente E (datos/elis_cifras_f1.json;
  10⁻¹² en f, 10⁻⁹ en C53 y flujos) y con la capa; F1-REPLICA y F1-LIBRO no saltan; F1-SERIES (H12) acepta sus series con las páginas
  del texto conservado en el expediente. Vacío no es cero (ROU o PPA vacía en la ventana → f
  vacía, Motor V05 INCOMPLETO y la capa en pendiente_de_datos, sin error); perímetro no reconocido → INV. La capa bloquea (F1-LIBRO) si el
  libro no corresponde: otro perímetro, otra serie, o un libro V6.3. Caso sintético NIIF 16 pesado (Empresa X con la D&A de derechos de uso
  = 75 % de la D&A, su principal en el FCF base y PPA = 15 %; ROU media ≥ 40 % del FCF base): libro = capa, e identidades f_A1 = f_A0 − ROU media ÷ ventas medias, f_A2 = f_A0 − (ROU + PPA) media ÷
  ventas medias y C53 = ΔV ÷ (Σ fila 31 en A0 + Σ ROU) con los valores del propio libro.
a0: con el perímetro vacío y con «A0_total» escrito, 0 celdas distintas (tolerancia 0, igualdad exacta) en las once hojas frente a la V6.3
  con las mismas entradas, recalculadas las dos por LibreOffice: libro de Elis (d2593777…, el que concilió el frente E) y los tres ejemplos
  de la V6.3 (Empresa X, ABB, Hermès). Excluidas solo las cuatro etiquetas de versión y la sección nueva (que no existe en la V6.3).
Escribe ../pruebas/resultado_<prueba>.json y .md. Código 0 si todo pasa.
"""
import datetime as dt
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
V631 = os.path.dirname(AQUI)
V6 = os.path.dirname(V631)
RAIZ = os.path.dirname(V6)
PV = os.path.join(RAIZ, "personaje_v2")
PLANTILLA_V63 = os.path.join(V6, "entregables", "Plantilla_V6.3.xlsx")
REF_V63 = os.path.join(V6, "referencia", "referencia_V6.3.json")
PLANTILLA = os.path.join(V631, "entregables", "Plantilla_V6.3.1_F1.xlsx")
REF = os.path.join(V631, "referencia", "referencia_V6.3.1_F1.json")
SHA_TXT = os.path.join(V631, "referencia", "SHA256_entregables_V6.3.1_F1.txt")
RECALC = os.path.join(PV, "scripts", "recalc.sh")
ELIS = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_14", "elis_decisiones", "Elis", "Elis_v63_evaluada.xlsx")
SHA_ELIS = "d2593777650f1d9d77bcc7b9eaa6f4c0c12a742fa4706bd20b35808f99c92385"
EJEMPLOS = [os.path.join(V6, "entregables", n) for n in ("Ejemplo_V6.3_EmpresaX.xlsx", "Ejemplo_ABB_V6.3.xlsx", "Ejemplo_migracion_Hermes_V6.3.xlsx")]
PY = sys.executable
COLS = "CDEFGHIJKL"
sys.path.insert(0, AQUI)

RES = []


def chk(nombre, ok, detalle=""):
    RES.append({"prueba": nombre, "ok": bool(ok), "detalle": detalle})
    print(("PASA " if ok else "FALLA") + f" · {nombre}" + (f" · {detalle}" if detalle else ""))


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def run(args, **kw):
    r = subprocess.run(args, capture_output=True, text=True, **kw)
    return r.returncode, (r.stdout + r.stderr).strip()


# ------------------------------------------------------------------------------------------------------------------ estructura
def estructura():
    ref63, ref = json.load(open(REF_V63)), json.load(open(REF))
    chk("la V6.3 no cambia (SHA-256 = origen de su referencia)", sha(PLANTILLA_V63) == ref63["sha256_origen"], sha(PLANTILLA_V63)[:16])
    with tempfile.TemporaryDirectory() as tmp:
        out = os.path.join(tmp, "Plantilla_V6.3.1_F1.xlsx")
        rc, txt = run([PY, "-I", os.path.join(AQUI, "construir_v631_f1.py"), PLANTILLA_V63, out])
        s_re = sha(out) if rc == 0 else None
    s_ent = sha(PLANTILLA)
    chk("reconstrucción determinista: el guion desde la V6.3 da el mismo SHA-256 que el entregable", rc == 0 and s_re == s_ent, f"{str(s_re)[:16]} / {s_ent[:16]}")
    chk("la referencia salió de este entregable", ref["sha256_origen"] == s_ent and ref["version"] == "V6.3.1 F1")
    lin = open(SHA_TXT, encoding="utf-8").read().split()
    chk("SHA256_entregables_V6.3.1_F1.txt coincide", s_ent in lin and "Plantilla_V6.3.1_F1.xlsx" in lin)
    # diferencias de la referencia, exactamente las previstas
    f63, f = ref63["formulas"], ref["formulas"]
    alteradas = {k for k in f63 if k in f and f63[k] != f[k]}
    quitadas = set(f63) - set(f)
    nuevas = set(f) - set(f63)
    prev_alt = {f"Historia!{c}30" for c in COLS} | {"Historia!C53", "Historia!C58", "Historia!C76", "Motor!E205", "Panel!A1"}
    prev_new = {f"Historia!{c}88" for c in COLS} | {"Historia!C89"}
    chk("fórmulas alteradas = fila 30, C53, C58, C76, Motor E205 y Panel A1 (y ninguna más)", alteradas == prev_alt,
        f"de más {sorted(alteradas - prev_alt)[:5]} · de menos {sorted(prev_alt - alteradas)[:5]}")
    chk("ninguna fórmula de la V6.3 quitada", not quitadas, str(sorted(quitadas)[:5]))
    chk("fórmulas nuevas = Historia C88:L88 (D_X) y C89 (perímetro efectivo)", nuevas == prev_new, str(sorted(nuevas ^ prev_new)[:5]))
    a0 = '=IF($C$89="A0_total",'
    for c in ("C53", "C58", "C76"):
        chk(f"Historia {c}: con A0 la fórmula de la V6.3 literal", f[f"Historia!{c}"].startswith(a0 + f63[f"Historia!{c}"][1:] + ","))
    chk("fila 30: la de la V6.3 con D_X (fila 88) en lugar de la D&A (fila 8)",
        all(f[f"Historia!{c}30"] == f63[f"Historia!{c}30"].replace(f"ISNUMBER({c}8)", f"ISNUMBER({c}88)").replace(f"{c}12-{c}8+", f"{c}12-{c}88+") for c in COLS))
    o, nw = f63["Motor!E205"], f["Motor!E205"]
    i = o.rfind('un hueco no vale cero",""') + len('un hueco no vale cero",')
    pre, suf = o[:i], o[i + 2:]
    medio = nw[len(pre):len(nw) - len(suf)] if nw.startswith(pre) and nw.endswith(suf) else ""
    chk("Motor E205: la de la V6.3 más tres causas al final (perímetro no reconocido, D_X vacía, D_X negativa) en lugar del último «»",
        medio.startswith('IF(Historia!$C$89="no reconocido","INV|') and medio.endswith('"")))') and medio.count("Historia!$C$89") == 3, medio[:80])
    x63, x = ref63["fijos"], ref["fijos"]
    alt_f = {k for k in x63 if k in x and x63[k] != x[k]}
    chk("celdas fijas alteradas = tres etiquetas de versión", alt_f == {"Análisis!A1", "Guía V6!A1", "Control maestro!A3"}, str(sorted(alt_f)))
    chk("ninguna celda fija de la V6.3 quitada", not (set(x63) - set(x)))
    nf = set(x) - set(x63)
    chk("celdas fijas nuevas solo en la sección nueva (Historia filas 84–90)",
        nf and all(k.startswith("Historia!") and 84 <= int("".join(ch for ch in k.split("!")[1] if ch.isdigit())) <= 90 for k in nf), f"{len(nf)} celdas")
    chk("mismas hojas, formato condicional, nombres definidos y partes del paquete",
        ref["hojas"] == ref63["hojas"] and ref["formato_condicional"] == ref63["formato_condicional"]
        and ref["nombres_definidos"] == ref63["nombres_definidos"] and ref["partes_paquete"] == ref63["partes_paquete"],
        f"{len(ref['partes_paquete'])} partes")
    v63, v = ref63["validaciones"], ref["validaciones"]
    dv_nuevas = [d for d in v["Historia"] if d not in v63["Historia"]]
    chk("validaciones: solo dos nuevas en la Historia (lista del perímetro en C85; ≥ 0 en C86:L87)",
        all(v[h] == v63[h] for h in v63 if h != "Historia") and all(d in v["Historia"] for d in v63["Historia"])
        and sorted(d[0] for d in dv_nuevas) == ["C85", "C86:L87"], str(dv_nuevas))
    e63, e = ref63["entradas"], ref["entradas"]
    chk("inventario de entradas: el de la V6.3 más Historia C85, C86:L87 y M85:S87",
        {h: r for h, r in e.items() if h != "Historia"} == {h: r for h, r in e63.items() if h != "Historia"}
        and e["Historia"] == e63["Historia"] + ["C85", "C86:L87", "M85:S87"], str(e["Historia"]))
    # verificadores
    ver = os.path.join(AQUI, "verificar_v631.py")
    rc, txt = run([PY, "-I", ver, PLANTILLA, REF])
    chk("verificar_v631.py: la plantilla es ÍNTEGRA frente a su referencia", rc == 0 and "ÍNTEGRO · 0 fallos" in txt, txt.splitlines()[-1])
    rc, txt = run([PY, "-I", os.path.join(V6, "scripts", "verificar_v63.py"), PLANTILLA, REF_V63])
    chk("verificar_v63.py (V6.3) rechaza la V6.3.1: una plantilla no pasa por la otra", rc == 1, (txt.splitlines() or [""])[1])
    with tempfile.TemporaryDirectory() as tmp:
        sys.path.insert(0, os.path.join(PV, "scripts"))
        from v63_xml import LibroV63
        from trasladar_entradas import escribir_formula
        lb = LibroV63(PLANTILLA)
        escribir_formula(lb, "Historia", "C88", "Historia!C8")   # D_X = D&A con cualquier perímetro: mutación del modelo
        m = os.path.join(tmp, "mut.xlsx")
        lb.guardar(m)
        rc, txt = run([PY, "-I", ver, m, REF])
        chk("verificar_v631.py rechaza una mutación de D_X (C88 = C8)", rc == 1 and "Historia!C88" in txt, (txt.splitlines() or [""])[1])


# ------------------------------------------------------------------------------------------------------------------ LibreOffice
def recalc(libro, dest):
    perfil = os.path.join(dest, "_perfil_lo")
    out = os.path.join(dest, "recalc")
    rc, txt = run(["bash", RECALC, libro, out, perfil])
    r = os.path.join(out, os.path.basename(libro))
    if rc != 0 or not os.path.exists(r):
        raise SystemExit(f"LibreOffice no recalculó {libro}: {txt[-300:]}")
    return r


def preparar(origen, plantilla, salida, otras=None):
    """Traslada las entradas y, para que el traslado sea fiel, vacía las celdas de entrada que el origen tiene vacías y la plantilla trae
    con un texto de ayuda (p. ej. Control maestro N52). Lo mismo con la V6.3 y con la V6.3.1."""
    import trasladar_entradas as T
    sys.path.insert(0, os.path.join(PV, "scripts"))
    from v63_xml import LibroV63
    src, pl = LibroV63(origen), LibroV63(plantilla)
    vaciar = {}
    for hoja, refs in T.INV.conjunto_entradas().items():
        if hoja not in src.hojas():
            continue
        vs, vp = src.todas_las_celdas(hoja), pl.todas_las_celdas(hoja)
        for r in refs:
            if vs.get(r) is None and vp.get(r) is not None and not (isinstance(vp[r], tuple) and vp[r][:1] == ("=",)):
                vaciar[f"{hoja}!{r}"] = None
    return T.trasladar(origen, plantilla, salida, {**vaciar, **(otras or {})})


def a0(dest):
    import comparar_libros as CL
    if os.path.exists(dest):
        raise SystemExit(f"{dest} ya existe: las pruebas escriben en una carpeta nueva")
    if os.path.commonpath([os.path.abspath(dest), RAIZ]) == RAIZ:
        raise SystemExit("DESTINO va fuera del repositorio")
    os.makedirs(dest)
    chk("libro de Elis: el que concilió el frente E (d2593777…), sin cambios", sha(ELIS) == SHA_ELIS)
    casos = [("Elis", ELIS)] + [(os.path.basename(p).replace(".xlsx", ""), p) for p in EJEMPLOS]
    detalle = {}
    for nombre, origen in casos:
        h0 = sha(origen)
        b63, b631, b631x = (os.path.join(dest, f"{nombre}_{s}.xlsx") for s in ("V6.3", "V6.3.1_vacio", "V6.3.1_A0"))
        n = preparar(origen, PLANTILLA_V63, b63)[0]
        preparar(origen, PLANTILLA, b631)
        preparar(origen, PLANTILLA, b631x, {"Historia!C85": "A0_total"})
        rc, txt = run([PY, "-I", os.path.join(AQUI, "verificar_v631.py"), b631x, REF])
        chk(f"{nombre}: el libro V6.3.1 con las entradas y «A0_total» es ÍNTEGRO frente a la referencia", rc == 0, txt.splitlines()[1])
        r63, r631, r631x = recalc(b63, dest), recalc(b631, dest), recalc(b631x, dest)
        d1, ncel = CL.comparar(r63, r631, tol=0)
        d2, _ = CL.comparar(r63, r631x, tol=0)
        chk(f"{nombre}: perímetro vacío · 0 celdas distintas frente a la V6.3 (igualdad exacta)", not d1, f"{ncel} celdas comparadas · {len(d1)} distintas {d1[:3]}")
        chk(f"{nombre}: «A0_total» escrito · 0 celdas distintas frente a la V6.3 (igualdad exacta)", not d2, f"{len(d2)} distintas {d2[:3]}")
        from openpyxl import load_workbook
        wb = load_workbook(r631x, data_only=True)
        hs = wb["Historia"]
        dx_ok = all((hs[f"{c}88"].value == hs[f"{c}8"].value) if isinstance(hs[f"{c}8"].value, (int, float)) else hs[f"{c}88"].value in (None, "")
                    for c in COLS)
        chk(f"{nombre}: con A0, D_X (fila 88) = D&A (fila 8) y perímetro efectivo A0_total", dx_ok and hs["C89"].value == "A0_total",
            f"C58 = {hs['C58'].value!r} · C53 = {hs['C53'].value!r} · Motor V05 = {wb['Motor']['D205'].value!r}")
        detalle[nombre] = {"origen": os.path.relpath(origen, RAIZ), "origen_sha256": h0, "celdas_de_entrada_trasladadas": n,
                           "celdas_comparadas": ncel, "distintas_vacio": len(d1), "distintas_A0_total": len(d2),
                           "C58": hs["C58"].value, "C53": hs["C53"].value, "C76": hs["C76"].value, "Motor_D205": wb["Motor"]["D205"].value}
        wb.close()
        chk(f"{nombre}: el origen no cambia", sha(origen) == h0)
    # el libro de Elis tal cual (recalculado) frente a la V6.3 con sus entradas: el traslado es fiel (informativo, tolerancia 1e-12)
    re_ = recalc(ELIS, os.path.join(dest, "elis_tal_cual"))
    d3, n3 = CL.comparar(re_, os.path.join(dest, "recalc", "Elis_V6.3.xlsx"), tol=1e-12)
    chk("Elis tal cual (recalculado) frente a la V6.3 con sus entradas trasladadas: 0 celdas distintas (1e-12; el traslado es fiel)", not d3,
        f"{n3} celdas · {len(d3)} distintas {d3[:3]}")
    shutil.rmtree(os.path.join(dest, "_perfil_lo"), ignore_errors=True)
    return detalle


def _escribir_libro(libro, salida, celdas):
    sys.path.insert(0, os.path.join(PV, "scripts"))
    from v63_xml import LibroV63
    lb = LibroV63(libro)
    lb.escribir_celdas({k: ({"valor": v, "tipo": "texto"} if isinstance(v, str) else v) for k, v in celdas.items()})
    lb.borrar_caches()
    lb.guardar(salida)


def _serie(vals, doc):
    return {str(y): {"valor_fuente": v, "signo": 1, "tratamiento": "ninguno", "documento": doc, "pagina": 1} for y, v in vals.items()}


def f1(dest):
    from fractions import Fraction as Fr
    from openpyxl import load_workbook
    sys.path.insert(0, os.path.join(PV, "scripts"))
    import motor_a_f1 as M
    import f1_libro_v631 as V631
    F1D = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_15", "f1_impl")
    sys.path.insert(0, os.path.join(F1D, "scripts"))
    import regresion_elis_f1 as RE
    if os.path.exists(dest):
        raise SystemExit(f"{dest} ya existe: las pruebas escriben en una carpeta nueva")
    if os.path.commonpath([os.path.abspath(dest), RAIZ]) == RAIZ:
        raise SystemExit("DESTINO va fuera del repositorio")
    os.makedirs(dest)
    cif = json.load(open(os.path.join(F1D, "datos", "elis_cifras_f1.json"), encoding="utf-8"))
    E9 = cif["referencia_E9"]
    REGP = {"fecha": "2026-11-18", "persona": "prueba V6.3.1 F1 (no es una decisión)", "motivo": "caso de prueba del libro"}
    chk("libro de Elis: d2593777…, sin cambios", sha(ELIS) == SHA_ELIS)
    base = os.path.join(dest, "Elis_V6.3.1_entradas.xlsx")
    preparar(ELIS, PLANTILLA, base)
    detalle = {}

    def libro(nombre, decl, origen=base, despues=None):
        dp = os.path.join(dest, f"{nombre}.motor_a_f1.json")
        json.dump(decl, open(dp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        b = os.path.join(dest, f"{nombre}.xlsx")
        V631.aplicar(origen, b, dp)
        if despues:
            _escribir_libro(b, b + ".tmp.xlsx", despues)
            os.replace(b + ".tmp.xlsx", b)
        return recalc(b, dest)

    ELIS_DIR = os.path.dirname(ELIS)
    TEXTOS = {"URD2022": "Elis - 2022 Universal Registration Document.txt", "URD2023": "Elis_Universal Registration Document_2023_EN.txt",
              "DEU2024FR": "Elis_Document d'enregistrement universel_2024_FR.txt", "URD2025": "Elis - 2025 Universal Registration Document.txt"}

    def evaluar(rec, decl):
        # (H12) las fuentes de las series se examinan en el expediente de Elis (solo lectura): texto/ con marcas «[PDF PAGE n]»
        return M.evaluar(M.leer_libro(rec), decl, carpeta=ELIS_DIR)

    def guarda(r, gid):
        return [g for g in r["guardas"] if g["id"] == gid]

    def salta(r, gid):
        return any(g["salta"] for g in guarda(r, gid))

    def decl_elis(per):
        d = RE.declaracion(cif, True, False)
        d["perimetro_reinversion"] = {"valor": per, "registro": REGP}
        for n_ in ("da_rou", "da_ppa"):
            for y_, e in d["series"][n_].items():
                e["fila"] = cif["series"][n_][y_]["etiqueta"]   # (V631-2) la fila de la página, para comprobar el ejercicio y la columna
        d["fuentes_series"] = {doc: {"archivo": os.path.join("texto", n_), "sha256": sha(os.path.join(ELIS_DIR, "texto", n_))} for doc, n_ in TEXTOS.items()}
        return d

    # ---------------------------------------------------------------- Elis A1 y A2 frente a E9 y a la capa
    recs = {}
    for per, k in (("A1_sin_ROU", "A1"), ("A2_propio", "A2")):
        d = decl_elis(per)
        rec = libro(f"Elis_{k}", d)
        recs[k] = rec
        wb = load_workbook(rec, data_only=True)
        h, mo = wb["Historia"], wb["Motor"]
        c58, c53 = h["C58"].value, h["C53"].value
        ref = E9["perimetros"][k]
        flujos = E9["A1_A2_flujos_palancas_actuales"][k]
        dev = max(abs(mo[f"{c}{fila}"].value - flujos[esc][t]) for esc, fila in (("MALO", 6), ("NORMAL", 7), ("BUENO", 8))
                  for t, c in enumerate(["AU", "AV", "AW", "AX", "AY", "AZ", "BA", "BB", "BC", "BD", "BF"]))
        chk(f"Elis {k}: perímetro efectivo {per} y Motor V05 OK", h["C89"].value == per and mo["D205"].value == "OK", f"V05 {mo['D205'].value!r}")
        chk(f"Elis {k} recalculado por LibreOffice: f = E9 (10⁻¹²)", abs(c58 - ref["f"]) <= 1e-12, f"{c58!r} frente a {ref['f']!r}")
        chk(f"Elis {k}: C53 (ancla de S2C) = E9 (10⁻⁹)", abs(c53 - ref["S2C_C53"]) <= 1e-9, f"{c53!r} frente a {ref['S2C_C53']!r}")
        chk(f"Elis {k}: los 33 flujos del Motor (años 1–10 y 11, tres escenarios) = E9 (10⁻⁹)", dev <= 1e-9, f"desviación máxima {dev:.2e}")
        if k == "A1":
            a11 = mo["BF7"].value - E9["A0_flujos_libro"]["NORMAL"][10]
            chk("Elis A1: el año 11 NORMAL se aparta del de A0 en 205,363 (control negativo: el terminal usa la f del perímetro)",
                abs(a11 - E9["desvio_anio_11_implementacion_parcial"]["A1"]["NORMAL"]) < 1e-3, f"{a11:.6f}")
        r = evaluar(rec, d)
        cd = r["calculo_perimetro_declarado"]
        chk(f"Elis {k}: la capa coincide con el libro (f 10⁻¹², ancla 10⁻⁹) y F1-REPLICA no salta (réplica con la D_X del libro)",
            abs(cd["f"] - c58) <= 1e-12 and abs(cd["ancla_s2c_E4"] - c53) <= 1e-9 and not salta(r, "F1-REPLICA")
            and per in str(r["replica_del_libro"].get("perimetro_replicado")), f"réplica {r['replica_del_libro'].get('perimetro_replicado')} · {r['replica_del_libro'].get('flujos_contrastados')} flujos")
        chk(f"Elis {k}: F1-LIBRO NO salta (libro V6.3.1 con el perímetro, las series, D_X, f, ancla y 33 flujos de la capa)",
            not salta(r, "F1-LIBRO") and r["libro_v631_f1"]["motivos"] == [] and r["libro_v631_f1"]["flujos_contrastados"] == 33,
            str(r["libro_v631_f1"]["motivos"])[:200])
        fs = [g for g in r["guardas"] if g["id"] == "F1-SERIES"]
        chk(f"Elis {k}: F1-SERIES sin problemas: las 10 cifras de D&A de derechos de uso y PPA completas, con su signo, en su fila y en la columna de su "
            "ejercicio, en el texto del expediente con su huella", fs and not fs[0]["salta"] and r["F1_SERIES"]["columna_comprobada"] == 10,
            str(fs[0]["detalle"] if fs else None)[:200])
        detalle[f"Elis_{k}"] = {"C58": c58, "C53": c53, "desviacion_max_flujos_E9": dev, "bloquean": sorted({g["id"] for g in r["guardas"] if g["salta"] and g["severidad"] == "BLOQUEA"}),
                                "estado_propuesto": r["estado_propuesto"]}
    # ---------------------------------------------------------------- V631-2 sobre el texto real: la cifra de otro ejercicio (E1)
    dE1 = decl_elis("A1_sin_ROU")
    dE1["series"]["da_rou"]["2025"].update({"literal": "(132.2)", "valor_fuente": -132.2})
    recE1 = libro("Elis_A1_E1", dE1)
    rE1 = evaluar(recE1, dE1)
    gE1 = guarda(rE1, "F1-SERIES")[0]
    chk("V631-2 · E1: la D&A ROU de 2025 declarada con la cifra de 2024 de la misma página: libro y capa coinciden, pero F1-SERIES la rechaza (columna de 2024)",
        not salta(rE1, "F1-LIBRO") and gE1["salta"] and gE1["efecto"] == "DATOS INVÁLIDOS" and "2024" in gE1["detalle"], gE1["detalle"][:160])
    # ---------------------------------------------------------------- V631-5 y V631-4: el ancla
    rec = libro("Elis_A1_circulante_2021", decl_elis("A1_sin_ROU"), despues={"Historia!H14": None})
    wb = load_workbook(rec, data_only=True)
    r = evaluar(rec, decl_elis("A1_sin_ROU"))
    chk("V631-5 · A1 con el circulante de 2021 vacío (fuera de la ventana, dentro de H–L): C53 vacía en el libro y en la capa; f = E9",
        wb["Historia"]["C53"].value is None and r["calculo_perimetro_declarado"]["ancla_s2c_E4"] is None
        and abs(wb["Historia"]["C58"].value - E9["perimetros"]["A1"]["f"]) <= 1e-12 and not salta(r, "F1-LIBRO"))
    rec = libro("Elis_A0_capex_2021", decl_elis("A0_total"), despues={"Historia!H12": None})
    wb = load_workbook(rec, data_only=True)
    r = evaluar(rec, decl_elis("A0_total"))
    chk("V631-4 · A0 con el capex de 2021 vacío: el libro calcula C53 como la V6.3 (≥ 3 años) y el oráculo no lo hace bloquear (la capa no lo calcula)",
        isinstance(wb["Historia"]["C53"].value, float) and r["calculo_perimetro_declarado"]["ancla_s2c_E4"] is None and r["libro_v631_f1"]["motivos"] == [],
        f"C53 {wb['Historia']['C53'].value!r}")
    # ---------------------------------------------------------------- vacío no es cero; perímetro no reconocido
    d = decl_elis("A1_sin_ROU")
    d2 = json.loads(json.dumps(d))
    del d2["series"]["da_rou"]["2024"]
    rec = libro("Elis_A1_sin_ROU_2024", d2)
    wb = load_workbook(rec, data_only=True)
    r = evaluar(rec, d2)
    chk("A1 con la D&A ROU de 2024 vacía (ventana): f y C53 vacías en el libro, Motor V05 INCOMPLETO, capa en pendiente_de_datos sin error ni F1-REPLICA",
        wb["Historia"]["C58"].value is None and wb["Historia"]["C53"].value is None and wb["Motor"]["D205"].value == "INCOMPLETO"
        and r["estado_propuesto"] == "pendiente_de_datos" and not salta(r, "F1-REPLICA"), f"{wb['Motor']['F205'].value!r}"[:160])
    d3 = json.loads(json.dumps(d))
    del d3["series"]["da_rou"]["2021"]
    rec = libro("Elis_A1_sin_ROU_2021", d3)
    wb = load_workbook(rec, data_only=True)
    r = evaluar(rec, d3)
    chk("A1 con la D&A ROU de 2021 vacía (fuera de la ventana, dentro del ancla H–L): f = E9, C53 vacía (cinco años) y la capa coincide",
        abs(wb["Historia"]["C58"].value - E9["perimetros"]["A1"]["f"]) <= 1e-12 and wb["Historia"]["C53"].value is None
        and r["calculo_perimetro_declarado"]["ancla_s2c_E4"] is None and not salta(r, "F1-LIBRO") and not salta(r, "F1-REPLICA"))
    d4 = decl_elis("A2_propio")
    del d4["series"]["da_ppa"]["2025"]
    rec = libro("Elis_A2_sin_PPA_2025", d4)
    wb = load_workbook(rec, data_only=True)
    chk("A2 con la PPA de 2025 vacía: f vacía y Motor V05 INCOMPLETO (vacío no es cero)", wb["Historia"]["C58"].value is None and wb["Motor"]["D205"].value == "INCOMPLETO")
    rec = libro("Elis_no_reconocido", decl_elis("A1_sin_ROU"), despues={"Historia!C85": "A3_estimado"})
    wb = load_workbook(rec, data_only=True)
    chk("C85 = «A3_estimado» (no está en el libro): perímetro efectivo «no reconocido», f vacía y Motor V05 DATOS INVÁLIDOS",
        wb["Historia"]["C89"].value == "no reconocido" and wb["Historia"]["C58"].value is None and wb["Motor"]["D205"].value == "DATOS INVÁLIDOS")
    rA3 = evaluar(rec, dict(decl_elis("A1_sin_ROU"), perimetro_reinversion={"valor": "A3_estimado", "registro": REGP}))
    chk("A3_estimado declarado (sin estimación): la capa termina en pendiente_de_datos (V-F1d) y F1-LIBRO bloquea (A3 no está en el libro)",
        rA3["estado_propuesto"] == "pendiente_de_datos" and salta(rA3, "V-F1d") and salta(rA3, "F1-LIBRO"))
    # ---------------------------------------------------------------- el oráculo bloquea si el libro no corresponde
    r = evaluar(recs["A1"], decl_elis("A2_propio"))
    chk("libro A1 con la declaración A2: F1-LIBRO bloquea (perímetro efectivo distinto)", salta(r, "F1-LIBRO") and any("perímetro efectivo" in x for x in r["libro_v631_f1"]["motivos"]))
    rec = libro("Elis_A1_serie_distinta", decl_elis("A1_sin_ROU"), despues={"Historia!K86": 131.0})
    r = evaluar(rec, decl_elis("A1_sin_ROU"))
    chk("libro A1 con una D&A ROU distinta de la declarada (2024): F1-LIBRO bloquea (serie, D_X, f y flujos)",
        salta(r, "F1-LIBRO") and any("D&A de derechos de uso 2024" in x for x in r["libro_v631_f1"]["motivos"]) and not salta(r, "F1-REPLICA"))
    r = evaluar(recalc(ELIS, os.path.join(dest, "v63")), decl_elis("A1_sin_ROU"))
    chk("libro V6.3 (Elis tal cual) con la declaración A1: F1-LIBRO bloquea como antes (límite declarado) y no hay bloque V6.3.1",
        salta(r, "F1-LIBRO") and "libro_v631_f1" not in r and "LÍMITE DECLARADO" in guarda(r, "F1-LIBRO")[0]["detalle"])
    rec = libro("Elis_A0", dict(decl_elis("A0_total")))
    r = evaluar(rec, decl_elis("A0_total"))
    chk("libro V6.3.1 con A0 y la declaración A0: F1-LIBRO no salta, la réplica es la de A0 y V-F1a sigue bloqueando (arrendamiento dos veces)",
        not salta(r, "F1-LIBRO") and r["replica_del_libro"]["perimetro_replicado"] == "A0" and not salta(r, "F1-REPLICA") and salta(r, "V-F1a"))
    # ---------------------------------------------------------------- sintético NIIF 16 pesado (Empresa X)
    ex = EJEMPLOS[0]
    wb = load_workbook(ex, data_only=True)
    h = wb["Historia"]
    anios = [h[f"{c}5"].value for c in COLS]
    da = {y: h[f"{c}8"].value for c, y in zip(COLS, anios)}
    rou = {y: round(0.75 * v, 6) for y, v in da.items()}
    ppa = {y: round(0.15 * v, 6) for y, v in da.items()}
    otras = {f"Historia!{c}17": rou[y] for c, y in zip(COLS, anios)}
    otras["Análisis!C49"] = round(sum(rou[y] for y in anios[-3:]) / 3, 6)
    sx = os.path.join(dest, "Sintetico_entradas.xlsx")
    preparar(ex, PLANTILLA, sx, otras)
    dsint = {"perimetro_reinversion": {"valor": "A0_total", "registro": REGP},
             "series": {"da_rou": _serie(rou, "informe sintético (inventado)"), "da_ppa": _serie(ppa, "informe sintético (inventado)")}}
    vals = {}
    for per in ("A0_total", "A1_sin_ROU", "A2_propio"):
        d = json.loads(json.dumps(dsint))
        d["perimetro_reinversion"]["valor"] = per
        rec = libro(f"Sintetico_{per}", d, origen=sx)
        w = load_workbook(rec, data_only=True)
        hh = w["Historia"]
        vals[per] = {"C58": hh["C58"].value, "C53": hh["C53"].value, "C74": hh["C74"].value, "C70": hh["C70"].value,
                     "S31": sum(hh[f"{c}31"].value for c in "HIJKL"), "dV": hh["L6"].value - hh["G6"].value, "V05": w["Motor"]["D205"].value}
        r = evaluar(rec, d)
        cd = r["calculo_perimetro_declarado"]
        chk(f"sintético NIIF 16 pesado · {per}: libro = capa (f, ancla) y F1-LIBRO y F1-REPLICA no saltan",
            vals[per]["V05"] == "OK" and abs(cd["f"] - vals[per]["C58"]) <= 1e-12 and abs(cd["ancla_s2c_E4"] - vals[per]["C53"]) <= 1e-9
            and not salta(r, "F1-LIBRO") and not salta(r, "F1-REPLICA"), f"f {vals[per]['C58']!r} · C53 {vals[per]['C53']!r} · {r['libro_v631_f1']['motivos'][:2]}")
    w3 = anios[-3:]
    m_rou = sum(rou[y] for y in w3) / 3
    m_ppa = sum(ppa[y] for y in w3) / 3
    a0v = vals["A0_total"]
    chk("sintético: NIIF 16 pesado (D&A ROU media ≥ 40 % del FCF base, con el principal dentro)", m_rou >= 0.4 * a0v["C70"], f"{m_rou:.3f} / {a0v['C70']:.3f}")
    chk("sintético: f_A1 = f_A0 − ROU media ÷ ventas medias (identidad, con los valores del libro)", abs(vals["A1_sin_ROU"]["C58"] - (a0v["C58"] - m_rou / a0v["C74"])) <= 1e-12,
        f"ROU media {m_rou:.3f} = {100 * m_rou / a0v['C70']:.0f} % del FCF base {a0v['C70']:.3f}")
    chk("sintético: f_A2 = f_A0 − (ROU + PPA) media ÷ ventas medias", abs(vals["A2_propio"]["C58"] - (a0v["C58"] - (m_rou + m_ppa) / a0v["C74"])) <= 1e-12)
    chk("sintético: C53_A1 = ΔV ÷ (Σ fila 31 en A0 + Σ ROU H–L) y C53_A2 con la PPA",
        abs(vals["A1_sin_ROU"]["C53"] - a0v["dV"] / (a0v["S31"] + sum(rou[y] for y in anios[-5:]))) <= 1e-9
        and abs(vals["A2_propio"]["C53"] - a0v["dV"] / (a0v["S31"] + sum(rou[y] + ppa[y] for y in anios[-5:]))) <= 1e-9)
    detalle["sintetico"] = vals
    shutil.rmtree(os.path.join(dest, "_perfil_lo"), ignore_errors=True)
    return detalle


def escribir(nombre, extra=None):
    ok = all(r["ok"] for r in RES)
    out = {"prueba": nombre, "fecha": dt.date.today().isoformat(), "plantilla_sha256": sha(PLANTILLA), "referencia_sha256": sha(REF),
           "resultado": "PASA" if ok else "FALLA", "total": len(RES), "pasan": sum(r["ok"] for r in RES), "comprobaciones": RES}
    if extra is not None:
        out["detalle"] = extra
    d = os.path.join(V631, "pruebas")
    os.makedirs(d, exist_ok=True)
    json.dump(out, open(os.path.join(d, f"resultado_{nombre}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    md = [f"# Pruebas V6.3.1 F1 · {nombre}", "", f"Fecha {out['fecha']} · plantilla `{out['plantilla_sha256'][:16]}…` · referencia `{out['referencia_sha256'][:16]}…`", "",
          f"**{out['resultado']}: {out['pasan']}/{out['total']}**", "", "| Comprobación | Resultado | Detalle |", "|---|---|---|"]
    md += [f"| {r['prueba']} | {'PASA' if r['ok'] else 'FALLA'} | {str(r['detalle']).replace('|', '/')[:300]} |" for r in RES]
    open(os.path.join(d, f"resultado_{nombre}.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
    print(f"{out['pasan']}/{out['total']} comprobaciones V6.3.1 F1 ({nombre}) {'PASAN' if ok else 'FALLAN'}")
    return 0 if ok else 1


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in ("estructura", "a0", "f1"):
        print(__doc__)
        sys.exit(2)
    if sys.argv[1] == "estructura":
        estructura()
        sys.exit(escribir("estructura"))
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)
    det = (a0 if sys.argv[1] == "a0" else f1)(sys.argv[2])
    sys.exit(escribir(sys.argv[1], det))
