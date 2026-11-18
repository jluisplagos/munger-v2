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
    if len(sys.argv) < 2 or sys.argv[1] not in ("estructura", "a0"):
        print(__doc__)
        sys.exit(2)
    if sys.argv[1] == "estructura":
        estructura()
        sys.exit(escribir("estructura"))
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)
    det = a0(sys.argv[2])
    sys.exit(escribir("a0", det))
