#!/usr/bin/env python3
"""Reproducción de T-1 (entrega 4.10.1). Uso: python3 -I reproducir_T1.py   (no usa LibreOffice; escribe solo en un temporal)

Construye, como el grupo L de test_trazabilidad_v2.py, el libro evaluado sin cachés + la copia con valores, ejecuta verificar_todo.sh
(cachés y comprobante) y compara la precondición «m0 = None» con:
  A) la preparación de la 4.10: las fichas copiadas de la referencia (registran 1020bb53…, el libro histórico);
  B) la preparación de la 4.10.1: fichas sintéticas con la identidad del libro recién acreditado.
Lo hace en este entorno y simulando OTRO entorno, en el que la reconstrucción del Excel da bytes distintos e inocuos (mismos miembros:
mismas fórmulas y valores; rezip_inocuo), que es lo que observó la revisión externa (73/74)."""
import hashlib, json, os, shutil, subprocess, sys, tempfile
sys.dont_write_bytecode = True  # (revisión interna 4.10.1) no deja __pycache__ en personaje_v2/scripts/ (tampoco los subprocesos: ENV)
ENV = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
AQUI = os.path.dirname(os.path.abspath(__file__))
PV = os.path.abspath(os.path.join(AQUI, "..", "..", ".."))
sys.path.insert(0, os.path.join(PV, "scripts")); sys.path.insert(0, os.path.join(PV, "pruebas"))
import cierre_v2 as CIE  # noqa: E402
EXP = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_6_1", "Vidrala")
TMP = tempfile.mkdtemp(prefix="repro_t1_")
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()  # noqa: E731
cfg = lambda k: subprocess.run([sys.executable, "-B", os.path.join(PV, "scripts", "config_v2.py"), k, os.path.join(PV, "config_v2.json")], capture_output=True, text=True).stdout.strip()  # noqa: E731


def rezip_inocuo(o, d):
    """Como en test_trazabilidad_v2.py: mismos miembros y contenido, otros bytes; si una forma coincidiera con el origen, la siguiente (H-3)."""
    import zipfile
    h0 = sha(o)
    for fecha, nivel in (((2001, 2, 3, 4, 5, 6), 1), ((2003, 4, 5, 6, 7, 8), 9), ((2005, 6, 7, 8, 9, 10), 5)):
        with zipfile.ZipFile(o) as zi, zipfile.ZipFile(d, "w", zipfile.ZIP_DEFLATED, compresslevel=nivel) as zo:
            for it in zi.infolist():
                zo.writestr(zipfile.ZipInfo(it.filename, date_time=fecha), zi.read(it.filename), compress_type=zipfile.ZIP_DEFLATED)
        if sha(d) != h0:
            return


def exigir(r, que):
    """(revisión interna 4.10.1) un paso técnico que falla no se presenta como reproducción."""
    if r.returncode != 0:
        print(f"NO REPRODUCE: {que} terminó con código {r.returncode}: {(r.stdout + r.stderr)[-300:]}")
        sys.exit(1)


def caso(nombre, otro_entorno):
    d = os.path.join(TMP, nombre, "Vidrala")
    shutil.copytree(EXP, d, ignore=shutil.ignore_patterns(".lo_perfil", "recalc"))
    ev = os.path.join(d, "Vidrala_v63_evaluada.xlsx")
    con = os.path.join(TMP, nombre + "_con_valores.xlsx"); shutil.copy2(ev, con)
    vac = os.path.join(TMP, nombre + "_celdas.json"); json.dump({}, open(vac, "w"))
    exigir(subprocess.run([sys.executable, "-B", os.path.join(PV, "scripts", "escribir_v63.py"), con, ev, "--celdas", vac, "--lista-blanca", "cualquiera", "--copia-de-prueba"], capture_output=True, text=True, env=ENV), "escribir_v63.py")
    os.makedirs(os.path.join(d, "recalc")); shutil.copy2(con, os.path.join(d, "recalc", "Vidrala_v63_evaluada.xlsx"))
    rv = subprocess.run(["bash", os.path.join(PV, "scripts", "verificar_todo.sh"), d, ev, os.path.join(d, "Vidrala_v63_datos.xlsx")], capture_output=True, text=True, env=ENV)
    # en esta copia sintética verificar_todo.sh da FAIL en comprobaciones ajenas a T-1 (como en el grupo L); lo que se exige es su paso de acreditación
    if "PASS · acreditar_libro.py" not in rv.stdout:
        print(f"NO REPRODUCE: verificar_todo.sh no acreditó el libro final: {(rv.stdout + rv.stderr)[-300:]}"); sys.exit(1)
    if otro_entorno:  # bytes distintos e inocuos del libro final, re-acreditado (lo que daría otro entorno)
        tmp = ev + ".orig"; shutil.copy2(ev, tmp); rezip_inocuo(tmp, ev); os.remove(tmp)
        exigir(subprocess.run([sys.executable, "-B", os.path.join(PV, "scripts", "acreditar_libro.py"), d, ev, os.path.join(d, "Vidrala_v63_datos.xlsx"), cfg("plantilla.referencia"), cfg("plantilla.verificador"), "incorporadas"], capture_output=True, text=True, env=ENV), "acreditar_libro.py")
    if not os.path.isfile(os.path.join(d, "acreditacion_libro.json")):
        print("NO REPRODUCE: falta el comprobante acreditacion_libro.json"); sys.exit(1)
    final = sha(ev)
    reg = (json.load(open(os.path.join(d, "ficha_provisional.json"), encoding="utf-8")).get("hashes") or {}).get("libro_evaluado")
    mA = CIE.motivo_acreditacion_libro(d)
    for fic in ("ficha.json", "ficha_provisional.json"):
        p = os.path.join(d, fic)
        if os.path.exists(p):
            F = json.load(open(p, encoding="utf-8")); F.setdefault("hashes", {})["libro_evaluado"] = final; json.dump(F, open(p, "w", encoding="utf-8"))
    mB = CIE.motivo_acreditacion_libro(d)
    print(f"{nombre}: libro final {final[:12]}… · ficha copiada registra {str(reg)[:12]}… · igual al histórico 1020bb53: {final.startswith('1020bb53')}")
    print(f"   A (preparación 4.10, fichas copiadas): m0 = {('None' if mA is None else repr(mA[:110]))} → la prueba antigua {'PASA' if mA is None else 'FALLA (como en la revisión externa)'}")
    print(f"   B (preparación 4.10.1, fichas sintéticas): m0 = {('None' if mB is None else repr(mB[:110]))} → precondición {'coherente' if mB is None else 'INCOHERENTE'}")
    return mA, mB


a = caso("este_entorno", False)
b = caso("otro_entorno_simulado", True)
shutil.rmtree(TMP, ignore_errors=True)
ok = a[1] is None and b[1] is None and b[0] is not None
print("RESULTADO:", "la preparación nueva es independiente de los bytes del Excel histórico; la antigua falla cuando difieren" if ok else "NO REPRODUCE")
sys.exit(0 if ok else 1)
