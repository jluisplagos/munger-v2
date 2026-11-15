#!/usr/bin/env python3
"""Batería de la integración económica experimental del motor B (V6.4; encargo 4.11 §8). Obligatoria en `verificar_paquete.sh completa`.

Uso (desde personaje_v2/): python3 -B pruebas/test_integracion_v64.py [grupo …]     grupos: A B C D E F G H (por defecto, todos)
  A · plantilla: reconstrucción determinista, verificador, V6.3 intacta, cambios declarados, alteración detectada.
  B · casos (LibreOffice, en secuencia): modo heredado = V6.3 celda a celda (libros 4.6.1 y 4.10.1); referencias completas de la 4.7.1 y
      de la 4.8.1; rechazos con motivo; cero válido; vuelta al heredado; conciliación anual y terminal; crédito, SRF, Rh = 0; R1 con
      caída, recuperación y nuevo máximo; DCF inverso y tornado con el modelo activo; réplica independiente (si está en el paquete).
  C · pipeline (agentes simulados): selección explícita; pasada V6.4 experimental; fase C sin evaluación V6.4; cambio de un parámetro
      después del cierre (retirada en la primera llamada y auditoría nueva); heredado V6.4 = V6.3 en el pipeline.
  D · cambio de base: preparación reproducible, sin sobrescribir, solo celdas declaradas, notas retiradas, concordancia y sin restos.
  E · (4.12 §3) vigencia antes del rechazo: siete alteraciones del material × cuatro primeras llamadas independientes, selección
      equivocada con material intacto, plantilla, referencia o verificador alterados con el mismo nombre, resumen no actualizable.
  F · (4.12 §4) materialidad y protocolos del objetivo: los dos protocolos y la falta de protocolo, contradicciones, dato ausente material
      (S-19), compra con una hipótesis experimental material sin fundamento fuera de las listas heredadas, cobertura de D10 y
      comprobación conjunta ausente o inválida, alternativas no numéricas evaluadas de forma explícita.
  G · (4.12 §5) coherencia del material final: variantes desactualizadas por cambios económicos (y reutilizadas ante cambios editoriales),
      instantánea de entradas, trazabilidad, dominios y fórmulas alteradas después del cierre.
  H · (4.13 §7) plantilla V6.4.1 experimental: integridad y reconstrucción, solo los cambios de fórmula declarados, validación del
      perímetro de la inversión, selección (V6.4 lo rechaza; V6.4.1 lo exige con requisito), huellas anteriores intactas, variantes y
      alternativas del perímetro, aplicación en un libro con las entradas de Viscofan, compatibilidad con la V6.4 y pasada del pipeline.
Escribe en temporales y en pruebas/_v64/ (que el manifiesto ignora como el resto de personaje_v2/pruebas/). Termina con la línea
«N/M pruebas de integración V6.4 PASAN» y código 0 solo si todas pasan.
"""
import copy
import csv
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

AQUI = os.path.dirname(os.path.abspath(__file__))
PV = os.path.dirname(AQUI)
RAIZ = os.path.dirname(PV)
V64 = os.path.join(RAIZ, "v6", "v64_experimental")
ENS = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_11")
PY = sys.executable
sys.path.insert(0, os.path.join(PV, "scripts"))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(ENS, "scripts"))
sys.path.append(os.path.join(V64, "scripts"))  # comparar_libros y trasladar_entradas (al final: no tapa los módulos de personaje_v2/scripts)
TMP = os.path.join(AQUI, "_v64")
RES = []


def paso(grupo, nombre, ok, detalle=""):
    RES.append({"grupo": grupo, "prueba": nombre, "ok": bool(ok), "detalle": str(detalle)[:600]})
    print(("PASA " if ok else "FALLA") + f" · {grupo} · {nombre}" + (f" · {str(detalle)[:300]}" if detalle else ""), flush=True)


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    return r.returncode, r.stdout + r.stderr


def recalc(libro, dir_rc, perfil):
    rc, out = run(["bash", os.path.join(PV, "scripts", "recalc.sh"), libro, dir_rc, perfil])
    return os.path.join(dir_rc, os.path.basename(libro)) if rc == 0 else None


# ======================================================================================= A · plantilla
def grupo_a():
    sys.path.insert(0, os.path.join(V64, "scripts"))
    import generar_referencia as GR  # (el de la V6.4: usa su inventario)
    plantilla = os.path.join(V64, "entregables", "Plantilla_V6.4_experimental.xlsx")
    ref64 = os.path.join(V64, "referencia", "referencia_V6.4_experimental.json")
    v63 = os.path.join(RAIZ, "v6", "entregables", "Plantilla_V6.3.xlsx")
    ref63 = os.path.join(RAIZ, "v6", "referencia", "referencia_V6.3.json")
    with tempfile.TemporaryDirectory() as t:
        nueva = os.path.join(t, "reconstruida.xlsx")
        rc, out = run([PY, "-I", os.path.join(V64, "scripts", "construir_v64_experimental.py"), v63, nueva])
        a, b = GR.capturar(plantilla), GR.capturar(nueva) if rc == 0 else {}
        paso("A", "reconstrucción desde la V6.3: mismas fórmulas, fijos, validaciones, formatos, nombres y partes que la entregada",
             rc == 0 and all(a[k] == b.get(k) for k in ("hojas", "formulas", "fijos", "validaciones", "formato_condicional", "nombres_definidos", "partes_paquete")),
             f"rc {rc} · SHA-256 {'idéntico' if rc == 0 and sha(nueva) == sha(plantilla) else 'distinto (no se exige)'}")
        # (4.12 §6) reconstrucción portable: contenido miembro a miembro, no la huella del archivo (que depende de la compresión del entorno)
        import comparar_zip as CZ
        ok_m, det_m = CZ.comparar(plantilla, nueva) if rc == 0 else (False, "sin reconstrucción")
        recomp = os.path.join(t, "recomprimida.xlsx")
        with zipfile.ZipFile(plantilla) as zin, zipfile.ZipFile(recomp, "w", zipfile.ZIP_DEFLATED, compresslevel=1) as zout:
            for i in zin.infolist():
                zout.writestr(i.filename, zin.read(i.filename), compress_type=zipfile.ZIP_DEFLATED, compresslevel=1)
        ok_r, det_r = CZ.comparar(plantilla, recomp)
        paso("A", "reconstrucción portable (4.12 §6): el mismo contenido miembro a miembro que la entregada; una recompresión cambia la huella del archivo y no el contenido",
             ok_m and ok_r and sha(recomp) != sha(plantilla), f"{det_m} · recompresión: {det_r}")
    rc, out = run([PY, "-I", os.path.join(V64, "scripts", "verificar_v64.py"), plantilla, ref64])
    paso("A", "verificar_v64.py: plantilla V6.4 ÍNTEGRA con su referencia", rc == 0 and "ÍNTEGRO" in out, out.strip().splitlines()[-1] if out.strip() else "")
    ref = json.load(open(ref64, encoding="utf-8"))
    paso("A", "la referencia V6.4 salió de la plantilla entregada (sha256_origen)", ref.get("sha256_origen") == sha(plantilla), ref.get("sha256_origen", "")[:16])
    rc, out = run(["sha256sum", "-c", os.path.join("referencia", "SHA256_entregables_V6.3.txt")], cwd=os.path.join(RAIZ, "v6"))
    rc2, out2 = run([PY, "-I", os.path.join(RAIZ, "v6", "scripts", "verificar_v63.py"), v63, ref63])
    paso("A", "V6.3 intacta: entregables con sus SHA-256 y plantilla ÍNTEGRA con su referencia", rc == 0 and rc2 == 0, (out.strip().splitlines() or [""])[-1] + " · " + (out2.strip().splitlines() or [""])[-1])
    r63 = json.load(open(ref63, encoding="utf-8"))
    cambiadas = {k for k in r63["formulas"] if k in ref["formulas"] and r63["formulas"][k] != ref["formulas"][k]}
    quitadas = {k for k in r63["formulas"] if k not in ref["formulas"]}
    motor = {f"Motor!{c}{r}" for r in range(6, 137) for c in ("AU", "AV", "AW", "AX", "AY", "AZ", "BA", "BB", "BC", "BD", "BF", "BL", "BP", "BQ", "BS", "BT")
             if f"Motor!AU{r}" in r63["formulas"]}
    esperadas = motor | {"Diagnóstico V6!C10", "Diagnóstico V6!C11", "Diagnóstico V6!C15", "Panel!A1"} | {f"Diagnóstico V6!{c}{r}" for c in "BCD" for r in (176, 177)}
    fijos = {k for k in r63["fijos"] if k in ref["fijos"] and r63["fijos"][k] != ref["fijos"][k]}
    paso("A", "cambios frente a la V6.3 = los declarados (16 columnas × 124 filas del Motor, 9 de Diagnóstico y Panel!A1; ninguna fórmula quitada)",
         cambiadas == esperadas and not quitadas and fijos == {"Análisis!A1", "Control maestro!A3", "Diagnóstico V6!E11", "Guía V6!A1"},
         f"cambiadas {len(cambiadas)} (esperadas {len(esperadas)}) · quitadas {len(quitadas)} · fijos {sorted(fijos)}")
    paso("A", "gráficos, controles, dibujos, validaciones y formatos de la V6.3 idénticos en la V6.4",
         ref["partes_paquete"] == r63["partes_paquete"] and all(r63["validaciones"][h] == ref["validaciones"][h] for h in r63["validaciones"])
         and all(r63["formato_condicional"][h] == ref["formato_condicional"].get(h) for h in r63["formato_condicional"]))
    with tempfile.TemporaryDirectory() as t:
        mal = os.path.join(t, "alterada.xlsx")
        zin = zipfile.ZipFile(plantilla)
        wbx = zin.read("xl/workbook.xml").decode()
        rels = zin.read("xl/_rels/workbook.xml.rels").decode()
        rid = re.search(r'<sheet[^>]*name="Motor"[^>]*r:id="(rId\d+)"', wbx).group(1)
        tgt = re.search(r'Id="%s"[^>]*Target="([^"]+)"|Target="([^"]+)"[^>]*Id="%s"' % (rid, rid), rels)
        parte = "xl/" + (tgt.group(1) or tgt.group(2)).lstrip("/").replace("xl/", "")
        with zipfile.ZipFile(mal, "w", zipfile.ZIP_DEFLATED) as zout:
            for i in zin.infolist():
                d = zin.read(i.filename)
                if i.filename == parte:
                    d = d.replace(b"-CO7+CY7,", b"-CO7+2*CY7,", 1)  # el crédito del año 1 de la fila NORMAL, duplicado
                    assert b"-CO7+2*CY7," in d, "no se encontró la fórmula de DI7 que se altera"
                zout.writestr(i, d)
        rc, out = run([PY, "-I", os.path.join(V64, "scripts", "verificar_v64.py"), mal, ref64])
        paso("A", "una alteración no autorizada de una fórmula nueva (Motor!DI7) se detecta y se nombra", rc == 1 and "DI7" in out, (out.strip().splitlines() or [""])[1] if out.strip() else "")
        import comparar_zip as CZ
        ok_a, det_a = CZ.comparar(plantilla, mal)
        paso("A", "la comparación miembro a miembro detecta la alteración (no confunde contenido con compresión)", not ok_a and parte in det_a, det_a)
    rc, out = run(["sha256sum", "-c", os.path.join("referencia", "SHA256_entregables_V6.4_experimental.txt")], cwd=V64)
    paso("A", "artefacto entregado (4.12 §6): plantilla y referencia V6.4 con su huella estricta (SHA-256 de todos los bytes)", rc == 0, (out.strip().splitlines() or [""])[-1])
    rc1, o1 = run([PY, "-I", os.path.join(V64, "scripts", "verificar_v64.py"), v63, ref64])
    rc2, o2 = run([PY, "-I", os.path.join(RAIZ, "v6", "scripts", "verificar_v63.py"), plantilla, ref63])
    paso("A", "versiones cruzadas: un libro V6.3 con la referencia V6.4, y uno V6.4 con la referencia V6.3, dan ALTERADO", rc1 == 1 and rc2 == 1)
    base_inv = os.path.join(RAIZ, "v6", "scripts", "inventario_entradas.py")
    import importlib.util
    spec = importlib.util.spec_from_file_location("inv64", os.path.join(V64, "scripts", "inventario_entradas.py"))
    inv64 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(inv64)
    spec = importlib.util.spec_from_file_location("inv63", base_inv)
    inv63 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(inv63)
    e64, e63 = inv64.conjunto_entradas(), inv63.conjunto_entradas()
    paso("A", "inventario V6.4 = V6.3 + entradas de «Configuración V6.4»; el de la V6.3 no cambia",
         all(e64[h] == e63[h] for h in e63) and set(e64) - set(e63) == {"Configuración V6.4"} and "B4" in e64["Configuración V6.4"])


# ======================================================================================= B · casos
def grupo_b():
    import casos_v64 as K
    from comparar_libros import comparar  # noqa: E402
    from openpyxl import load_workbook
    from precio_de_si import p_estrella
    d = os.path.join(TMP, "casos")
    shutil.rmtree(d, ignore_errors=True)
    rc, out = run([PY, "-I", os.path.join(ENS, "scripts", "generar_libros_casos.py"), d], cwd=RAIZ, timeout=3600)
    man = json.load(open(os.path.join(d, "manifiesto_casos.json"), encoding="utf-8")) if os.path.exists(os.path.join(d, "manifiesto_casos.json")) else {"casos": []}
    paso("B", f"libros de los casos generados y recalculados en secuencia ({len(man['casos'])})", rc == 0 and all(c["recalculo_ok"] for c in man["casos"]), out.strip().splitlines()[-1] if out.strip() else "")
    casos = {c["id"]: c for c in man["casos"]}
    wbs = {}

    def wb(i):
        if i not in wbs:
            wbs[i] = load_workbook(os.path.join(d, casos[i]["recalculado"]), data_only=True)
        return wbs[i]

    def valores(i):
        a = wb(i)["Análisis"]
        V = [a["B78"].value, a["C78"].value, a["D78"].value]
        if not all(isinstance(v, (int, float)) for v in V):
            return None
        p = [a["B69"].value, a["C69"].value, a["D69"].value]
        return {"V": V, "ponderado": a["C83"].value, "precio_si": min(p_estrella(V, p, 3), V[1])}
    # heredado = V6.3, celda a celda
    for base, caso in (("4.6.1", "her_461"), ("4.10.1", "her_4101")):
        src = os.path.join(RAIZ, K.BASES[base])
        cp = os.path.join(d, f"v63_{caso}.xlsx")
        shutil.copy(src, cp)
        rc_ = recalc(cp, os.path.join(d, "rc63"), os.path.join(d, "perfil_lo"))
        dif, n = comparar(rc_, os.path.join(d, casos[caso]["recalculado"]), 1e-12) if rc_ else ([("sin recálculo", None, None)], 0)
        paso("B", f"modo heredado sobre el libro {base}: todas las celdas de la V6.3 iguales (tolerancia 1e-12)", not dif, f"{n} celdas · {len(dif)} diferencias {dif[:3]}")
    dif, n = comparar(os.path.join(d, casos["her_461"]["recalculado"]), os.path.join(d, casos["her_461_explicito"]["recalculado"]), 0)
    paso("B", "«Heredado» escrito = celda vacía (B4)", not dif, f"{len(dif)} diferencias")
    # referencias
    grupos = {}
    for i, c in casos.items():
        r = c.get("referencia")
        if not r:
            continue
        v = valores(i)
        g = r["fuente"].split(" · ")[0]
        ok = v is not None and abs(v["ponderado"] - r["ponderado"]) <= r["tol"] and abs(v["precio_si"] - r["precio_si"]) <= r["tol"] and (
            r.get("V") is None or max(abs(x - y) for x, y in zip(v["V"], r["V"])) <= r.get("tol_V", r["tol"]))
        grupos.setdefault(g, []).append((i, ok, v and abs(v["ponderado"] - r["ponderado"])))
    for g, lst in sorted(grupos.items()):
        malos = [x for x in lst if not x[1]]
        paso("B", f"referencias de {g}: {len(lst)} casos reproducidos (V, ponderado y precio de Sí con sus valores completos)", not malos,
             f"máx. |Δ ponderado| {max((x[2] or 0) for x in lst):.1e}" + (f" · fallan {[x[0] for x in malos]}" if malos else ""))
    # rechazos
    malos = []
    for i, c in casos.items():
        if not i.startswith("rechazo_"):
            continue
        w = wb(i)
        if (valores(i) is not None or c["motivo_esperado"] not in str(w["Configuración V6.4"]["B8"].value) or w["Motor"]["B255"].value != "INCOMPLETO"
                or w["Motor"]["B252"].value is not True or "Configuración V6.4" not in str(w["Motor"]["B256"].value)):
            malos.append((i, str(w["Configuración V6.4"]["B8"].value)[:80]))
    paso("B", f"configuraciones incompletas o incompatibles ({sum(1 for i in casos if i.startswith('rechazo_'))}): no calculan, V35 INCOMPLETO (Motor B255), bloqueo del valor (B252) y motivo explícito (B256 y Configuración B8)", not malos, malos[:3])
    g0, g1, g2 = wb("N2_cero")["Configuración V6.4"], wb("N1_cero")["Configuración V6.4"], wb("T1_M1_R1")["Análisis"]
    paso("B", "cero válido frente a ausencia: N2 = 0 da m0 = 0 y N1 = 0 da t = 0 (no el respaldo), con valores distintos",
         g0["B25"].value == 0 and g1["B18"].value == 0 and valores("N2_cero")["ponderado"] != valores("T1_M1_R1")["ponderado"] != valores("N1_cero")["ponderado"])
    # vuelta al heredado: un caso experimental completo con B4 = Heredado
    vh = dict(casos["SR1_L1.15"]["config"])
    vh["Configuración V6.4!B4"] = "Heredado"
    sys.path.insert(0, os.path.join(V64, "scripts"))
    from trasladar_entradas import trasladar
    libro = os.path.join(d, "vuelta_heredado.xlsx")
    trasladar(os.path.join(RAIZ, K.BASES["4.6.1"]), os.path.join(V64, "entregables", "Plantilla_V6.4_experimental.xlsx"), libro, vh, False)
    rc_ = recalc(libro, os.path.join(d, "rc"), os.path.join(d, "perfil_lo"))
    dif, n = comparar(os.path.join(d, "rc63", "v63_her_461.xlsx"), rc_, 1e-12)
    w = load_workbook(rc_, data_only=True)
    paso("B", "retorno al modo heredado sin arrastrar parámetros (todas las opciones escritas): = V6.3 celda a celda, con el aviso B10",
         not dif and "ignora" in str(w["Configuración V6.4"]["B10"].value), f"{len(dif)} diferencias")
    # conciliación en todos los casos válidos
    malos = []
    for i in casos:
        if i.startswith("rechazo_") or valores(i) is None:
            continue
        k = wb(i)["Conciliación B"]
        if not all(str(k[f"B{b + 25}"].value).startswith("✓") for b in (5, 35, 65)):
            malos.append(i)
    paso("B", "identidad FCF = NOPAT + D&A − inversión fija bruta − Δcirculante, años 1–10 y terminal, y VP iguales al motor en MALO, NORMAL y BUENO de todos los casos válidos", not malos, malos[:5])

    def fila(i, b, off):
        k = wb(i)["Conciliación B"]
        return [k.cell(b + off, col).value for col in range(2, 13)]
    malos = []
    for i in casos:
        est = casos[i]["config"].get("Configuración V6.4!B36", "")
        if i.startswith("rechazo_") or valores(i) is None or not est:
            continue
        for b in (5, 35, 65):
            req, fija, cred = fila(i, b, 9), fila(i, b, 10), fila(i, b, 11)
            for q, f, c in zip(req, fija, cred):
                if not all(isinstance(x, (int, float)) for x in (q, f, c)):
                    continue
                if est.startswith("H"):
                    if not (-1e-12 <= c <= min(q, max(0.0, f)) + 1e-12):
                        malos.append((i, "crédito fuera de [0, min(req, max(0, fija))]"))
                elif abs(c) > 0:
                    malos.append((i, "crédito fuera de H"))
    paso("B", "crédito solo en H (también en el terminal) y acotado: 0 ≤ crédito ≤ min(requisito, max(0, fija para crecer))", not malos, malos[:3])
    malos = [b for b in (5, 35, 65) if fila("SRF_L1.15", b, 13) != fila("S_L1.15", b, 13)]
    paso("B", "SRF conserva el circulante: Δcirculante de SRF = el de S fila a fila (años y terminal)", not malos)
    ig = lambda x, y: max(abs(a - b) for a, b in zip(valores(x)["V"], valores(y)["V"])) < 1e-9  # noqa: E731
    paso("B", "Rh = 0: SRF = S (λ = 1) y θ = 0 en SR1 = sin requisito con P0", ig("SRF_L1.00", "S_L1.00") and ig("SR1_T0.00", "P0_solo") and ig("S_L1.00", "P0_solo"))
    k0 = wb("T1_M1_R0_sin_circulante")["Conciliación B"]
    paso("B", "R0 sin datos de circulante: mismo valor que R0 con ellos y la conciliación no separa el circulante (Δcirculante = 0)",
         ig("T1_M1_R0_sin_circulante", "T1_M1_R0") and all(x == 0 for b in (5, 35, 65) for x in fila("T1_M1_R0_sin_circulante", b, 13) if isinstance(x, (int, float)))
         and wb("T1_M1_R0_sin_circulante")["Configuración V6.4"]["B83"].value == 0 and str(k0["B30"].value).startswith("✓"))
    # R1: caída, recuperación por debajo del máximo y nuevo máximo (MALO del caso sintético)
    v, pico, dc, fi = fila("R1_nuevo_maximo", 5, 2)[:10], fila("R1_nuevo_maximo", 5, 3)[:10], fila("R1_nuevo_maximo", 5, 13)[:10], fila("R1_nuevo_maximo", 5, 10)[:10]
    v0 = wb("R1_nuevo_maximo")["Motor"]["C6"].value
    prev = [v0] + v[:-1]
    cae = [t for t in range(10) if v[t] < prev[t]]
    rec = [t for t in range(10) if prev[t] <= v[t] <= pico[t]]
    nuevo = [t for t in range(10) if v[t] > pico[t]]
    ok = cae and rec and nuevo and all(fi[t] == 0 and dc[t] < 0 for t in cae) and all(fi[t] == 0 and dc[t] >= 0 for t in rec) and all(fi[t] > 0 for t in nuevo)
    fi0 = fila("R0_nuevo_maximo", 5, 10)[:10]
    paso("B", "R1 con caída (solo libera circulante), recuperación por debajo del máximo (repone circulante, sin capacidad) y nuevo máximo (inversión completa); R0 desinvierte al caer",
         ok and all(fi0[t] < 0 for t in cae), f"años de caída {[t + 1 for t in cae]} · recuperación {[t + 1 for t in rec]} · nuevo máximo {[t + 1 for t in nuevo]}")
    k = wb("S_T0.50")["Conciliación B"]
    kv = wb("S_L1.15_anios_ventas")["Conciliación B"]
    paso("B", "salto del requisito entre el año 10 y el terminal visible (Θ plano con terminal ∝ ventas) y continuo con la convención proporcional",
         isinstance(k["B58"].value, (int, float)) and abs(k["B58"].value) > 1e-6 and isinstance(kv["B58"].value, (int, float)) and abs(kv["B58"].value - kv["D58"].value) < 1e-9,
         f"S_T0.50 {k['B58'].value} · años ∝ ventas {kv['B58'].value} vs g {kv['D58'].value}")
    m_e, m_h = wb("SR1_L1.15")["Motor"], wb("T1_M1_R1")["Motor"]
    a_e, a_h = wb("SR1_L1.15")["Análisis"], wb("T1_M1_R1")["Análisis"]
    paso("B", "el DCF inverso, el tornado y las sensibilidades usan el modelo activo (filas del Motor y C86 distintos con P-M1)",
         m_e["BK56"].value != m_h["BK56"].value and m_e["BK41"].value != m_h["BK41"].value and a_e["C86"].value != a_h["C86"].value)
    # (revisión interna H6) contraste numérico de las cuatro lecturas experimentales, recalculadas en Python desde las entradas de cada
    # fila del Motor y los parámetros efectivos de «Configuración V6.4» (B83:B89): BL (valor sin crecimiento; no incluye la cartera P0),
    # BP (reinversión del año 1), BQ (rentabilidad marginal efectiva) y Diagnóstico B176:D177 (con NOPAT, Δcirculante y fija del año 11)
    def num(x):
        return isinstance(x, (int, float)) and not isinstance(x, bool)

    def cerca(a, b):
        return num(a) and num(b) and abs(a - b) <= 1e-9 * max(1.0, abs(b))
    malos, n_filas, n_casos, n_p0 = [], 0, 0, 0
    for i in casos:
        if i.startswith("rechazo_") or valores(i) is None or wb(i)["Configuración V6.4"]["B76"].value is not True:
            continue
        w = wb(i)
        g, m, dgn = w["Configuración V6.4"], w["Motor"], w["Diagnóstico V6"]
        nwc, fs2c, froic, ffija, rsg = (g[f"B{k}"].value for k in (83, 84, 85, 86, 89))
        n_casos += 1
        n_p0 += 1 if any(num(g.cell(93, 1 + k).value) and g.cell(93, 1 + k).value > 0 for k in range(1, 11)) else 0
        for r in range(6, 137):
            if m[f"BS{r}"].value is not True or m[f"B{r}"].value != "B":
                continue
            n_filas += 1
            C_, D_, F_, G_, H_, I_, J_, K_, M_ = (m[f"{x}{r}"].value for x in "CDFGHIJKM")
            AA, AJ, AK, AU = (m[f"{x}{r}"].value for x in ("AA", "AJ", "AK", "AU"))
            nopat1 = AA * AK * (1 - K_)
            ns = AJ * (1 + H_) * F_ * (1 - K_)
            nd = AJ * H_ * nwc
            nf = (ns * H_ / (I_ * froic) - nd) * ffija
            esperado = {"BL": C_ * D_ * (1 - K_) / J_ - rsg / J_ + M_, "BQ": F_ * (1 - K_) / (nwc + (1 / (G_ * fs2c) - nwc) * ffija),
                        "DS": ns, "DT": nd, "DU": nf}
            if nopat1:
                esperado["BP"] = (nopat1 - AU) / nopat1
            for col, v in esperado.items():
                if not cerca(m[f"{col}{r}"].value, v):
                    malos.append((i, f"{col}{r}", m[f"{col}{r}"].value, v))
            if r in (6, 7, 8):
                cd = "BCD"[r - 6]
                if not cerca(dgn[f"{cd}176"].value, esperado["BQ"]):
                    malos.append((i, f"Diagnóstico {cd}176", dgn[f"{cd}176"].value, esperado["BQ"]))
                if nf + nd and not cerca(dgn[f"{cd}177"].value, ns * H_ / (nf + nd)):
                    malos.append((i, f"Diagnóstico {cd}177", dgn[f"{cd}177"].value, ns * H_ / (nf + nd)))
    paso("B", "lecturas experimentales con contraste numérico: BL (sin la cartera P0), BP, BQ y Diagnóstico B176:D177 = recalculadas desde las entradas de cada fila",
         not malos and n_casos >= 20 and n_p0 >= 5 and n_filas >= 100 * n_casos, f"{n_casos} casos ({n_p0} con P0) · {n_filas} filas · {len(malos)} diferencias {malos[:3]}")
    rep = os.path.join(ENS, "scripts", "replica_independiente_v64.py")
    if os.path.exists(rep):
        rc, out = run([PY, "-I", rep, d, "--json", os.path.join(d, "replica.json"), "--txt", os.path.join(d, "replica.txt")], cwd=RAIZ, timeout=3600)
        paso("B", "réplica independiente (contexto separado, sin leer las fórmulas del Excel) frente a todos los libros de los casos", rc == 0, (out.strip().splitlines() or [""])[-1])
    else:
        paso("B", "réplica independiente presente en el paquete", False, "falta scripts/replica_independiente_v64.py")


# ======================================================================================= C · pipeline
CFG64 = os.path.join(PV, "config_v2_v64_experimental.json")
PIPE = os.path.join(PV, "scripts", "pipeline.py")


def preparar_sintetico(c, conf=None):
    import agentes_sinteticos as AG  # noqa: F401
    shutil.rmtree(c, ignore_errors=True)
    os.makedirs(os.path.join(c, "etapa1"))
    nombre = os.path.basename(c)
    shutil.copy(os.path.join(AQUI, "sintetico", "_origen", "EmpresaX_v53_evaluada_sintetica.xlsx"), os.path.join(c, "etapa1", f"{nombre}_evaluada.xlsx"))
    open(os.path.join(c, "etapa1", "respuesta.md"), "w", encoding="utf-8").write("# respuesta v1 (sintética)\n\nCubo: VIGILAR. Precio de Sí v1: 15.\n")
    json.dump({"empresa": "Empresa X (inventada)", "cubo": "VIGILAR", "precio_de_si": 15}, open(os.path.join(c, "etapa1", "juicio.json"), "w", encoding="utf-8"))
    shutil.copy(os.path.join(PV, "esquema", "fase1_v63.ejemplo.json"), os.path.join(c, "fase1_v63.json"))
    if conf is not None:
        json.dump(conf, open(os.path.join(c, "configuracion_economica.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def conf_sintetica(modo="Experimental", lam=1.15, protocolo="objetivo_condicionado"):
    import configuracion_economica as CE
    t = {"clase": "hipótesis", "confianza": "baja", "fuente_o_condicion": "caso sintético", "justificacion": "prueba de la integración", "materialidad": "variantes"}
    if modo == "Heredado":
        return {"tipo": "configuracion_economica_motor_B", "version_formato": 1, "modo": "Heredado", "naturaleza": "prueba", "trazabilidad": {"modo": t}}
    return {"tipo": "configuracion_economica_motor_B", "version_formato": 1, "modo": "Experimental", "naturaleza": "configuración sintética de prueba; no es una adopción",
            **({"protocolo_objetivo": protocolo} if protocolo else {}),
            "N1": None, "N2": None, "N3": {"regla": CE.REGLAS[1], "existencias": 10.0, "deudores": 12.0, "acreedores": 8.0, "fuente": "sintético"},
            "PM1": {"estructura": CE.ESTRUCTURAS[2], "familia": CE.FAMILIAS[0], "lambda": lam, "lambda_rango": [1.10, 1.30], "theta": None, "convencion_anios": "Plana",
                    "convencion_terminal": "Proporcional a las ventas", "roic_terminal": CE.ROIC_T[0], "cartera": CE.CARTERA[0]},
            "trazabilidad": {k: dict(t) for k in CE.FILAS_TRAZA}}


def correr(c, cfg=CFG64, fase_c_v64=True, sin_v64_una_vez=False, max_vueltas=40, motor="B", parar_en_espera=False, opciones_v64=None, material_ausente=None,
           tras_fase_c=None):
    import agentes_sinteticos as AG
    import configuracion_economica as CE
    usado = {"sin_v64": False, "correccion_pedida": False}
    for _ in range(max_vueltas):
        r = subprocess.run([PY, PIPE, c] + (["--config", cfg] if cfg else []), capture_output=True, text=True)
        if r.returncode != 10 or parar_en_espera:
            return r.returncode, r.stdout + r.stderr, usado
        esp = open(os.path.join(c, "ESPERANDO.md"), encoding="utf-8").read()
        nombre = esp.split("**")[1]
        if "falta configuracion_v64" in esp:
            usado["correccion_pedida"] = True
        if nombre == "extraccion_v63":
            AG.extracto(c)
        elif nombre == "fase_a":
            AG.fase_a(c, motor=motor)
        elif nombre == "fase_b":
            AG.fase_b(c, justificar=True)
        elif nombre in ("fase_c_turno1", "fase_c_turno2"):
            ma = material_ausente
            if ma == "__primero__":  # el primer dato de datos_ausentes.json cuando la fase C lo revisa
                da_ = json.load(open(os.path.join(c, "datos_ausentes.json"), encoding="utf-8")) if os.path.exists(os.path.join(c, "datos_ausentes.json")) else []
                ma = (da_[0] if da_ else {}).get("dato")
            AG.fase_c(c, 1 if nombre.endswith("1") else 2, material_ausente=ma)
            if fase_c_v64 and not (sin_v64_una_vez and not usado["sin_v64"]):
                # (4.12 §4) evaluación V6.4 de un agente cuidadoso: materialidad separada, ámbito exacto y protocolo del objetivo
                AG.aplicar_v64(c, 1 if nombre.endswith("1") else 2, **(opciones_v64 or {}))
            elif sin_v64_una_vez and nombre.endswith("2"):
                usado["sin_v64"] = True
            if tras_fase_c:  # (4.13 §4) alteración posterior de la fase C (pruebas negativas de extremo a extremo)
                tras_fase_c(c, 1 if nombre.endswith("1") else 2, usado)
        elif nombre == "verificacion":
            AG.auditoria(c)
        else:
            raise RuntimeError(nombre)
    return None, "demasiadas vueltas", usado


def listado(c):
    return sorted((os.path.relpath(os.path.join(r, f), c), os.path.getmtime(os.path.join(r, f))) for r, ds, fs in os.walk(c) for f in fs)


def grupo_c():
    import configuracion_economica as CE
    import informe
    s1 = informe.distancias_con_denominador(90.10, 66.5206103)
    s2 = informe.distancias_con_denominador(50.0, 66.5206103)
    paso("C", "redacción de las distancias con el denominador identificado (cifras de prueba del encargo §7: 66,5206103 frente a 90,10)",
         "90.10 está un 35.45% por encima del precio de Sí 66.52" in s1 and "precio de Sí está un 26.17% por debajo del precio actual" in s1
         and "50.00 está un 24.84% por debajo del precio de Sí" in s2 and "precio de Sí está un 33.04% por encima del precio actual" in s2, s1)
    base = os.path.join(TMP, "pipeline")
    shutil.rmtree(base, ignore_errors=True)
    os.makedirs(base)
    # selección explícita
    c = os.path.join(base, "sel", "EmpresaXS")
    preparar_sintetico(c)
    antes = listado(c)
    rc, out, _ = correr(c)
    paso("C", "V6.4 sin configuracion_economica.json: se detiene con código 2 y no escribe nada", rc == 2 and listado(c) == antes and "exige configuracion_economica.json" in out, out.strip().splitlines()[-1][:160])
    conf_mal = conf_sintetica()
    conf_mal["PM1"]["lambda"] = 0.9
    json.dump(conf_mal, open(os.path.join(c, "configuracion_economica.json"), "w", encoding="utf-8"))
    antes = listado(c)
    rc, out, _ = correr(c)
    paso("C", "configuración económica no válida (λ < 1): código 2 sin escribir nada", rc == 2 and listado(c) == antes and "no es válida" in out)
    rc, out, _ = correr(c, cfg=None)
    paso("C", "configuración económica en un expediente ejecutado con la V6.3: código 2 (no se ignora en silencio)", rc == 2 and "exige la plantilla V6.4" in out)
    # (revisión interna H1) al revés: un expediente que ya empezó con la V6.3 (libros y estado, sin plantilla_activa.json) no se ejecuta con la V6.4
    c = os.path.join(base, "inv", "EmpresaXI")
    preparar_sintetico(c)
    rc0, _, _ = correr(c, cfg=None, parar_en_espera=True)
    json.dump(conf_sintetica(), open(os.path.join(c, "configuracion_economica.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    antes = listado(c)
    rc, out, _ = correr(c)
    paso("C", "un expediente que empezó con la V6.3 (libros y estado, sin plantilla_activa.json) ejecutado con la V6.4: código 2 sin escribir nada",
         rc0 == 10 and rc == 2 and listado(c) == antes and "se preparó con la V6.3" in out and not os.path.exists(os.path.join(c, "plantilla_activa.json")),
         out.strip().splitlines()[-1][:200])
    # (revisión interna H3) con la configuración experimental, la fase A elige el motor A: límite del modelo, no falta de datos
    c = os.path.join(base, "motorA", "EmpresaXA")
    preparar_sintetico(c, conf_sintetica())
    rc, out, _ = correr(c, motor="A")
    st_a = json.load(open(os.path.join(c, "estado_pipeline.json"), encoding="utf-8"))
    dg = json.load(open(os.path.join(c, "diagnostico.json"), encoding="utf-8")) if os.path.exists(os.path.join(c, "diagnostico.json")) else {}
    ent = open(os.path.join(c, "entrada_v63.md"), encoding="utf-8").read()
    paso("C", "V6.4 experimental y fase A con el motor A: termina en el límite del modelo (no en pendiente_de_datos) y entrada_v63.md separa datos y cobertura",
         st_a.get("estado_analisis") == "no_entregable" and (dg.get("causa") or {}).get("tipo") == "limite_del_modelo" and "solo cubre el motor B" in str(dg)
         and "Motor A: CALCULABLE" in ent and "NO cubierto por la configuración experimental" in ent,
         f"{st_a.get('estado_analisis')} · {(dg.get('causa') or {}).get('tipo')} · {str((dg.get('causa') or {}).get('detalle'))[:120]}")
    # pasada experimental completa
    c = os.path.join(base, "exp", "EmpresaXE")
    preparar_sintetico(c, conf_sintetica())
    rc, out, usado = correr(c, sin_v64_una_vez=True)
    st = json.load(open(os.path.join(c, "estado_pipeline.json"), encoding="utf-8"))
    paso("C", "pasada V6.4 experimental (motor B, agentes simulados): concluido · APROBADO", rc == 0 and st.get("estado_analisis") == "concluido" and st.get("auditoria") == "APROBADO",
         f"rc {rc} · {st.get('estado_analisis')} · {st.get('auditoria')}")
    paso("C", "la fase C sin evaluación V6.4 (configuracion_v64) recibe una corrección y no se cierra hasta darla", usado["correccion_pedida"] and usado["sin_v64"])
    pa = json.load(open(os.path.join(c, "plantilla_activa.json"), encoding="utf-8"))
    paso("C", "plantilla_activa.json registra la V6.4 con las huellas de plantilla, referencia y verificador",
         pa["version"] == "V6.4 experimental" and pa["archivo_sha256"] == sha(os.path.join(V64, "entregables", "Plantilla_V6.4_experimental.xlsx")))
    import pipeline as P
    import config_v2
    pp = P.Pipeline(c, config_v2.cargar(CFG64))
    paso("C", "las celdas de configuración de los libros de datos y evaluado son las de configuracion_economica.json", not pp.configuracion_en_libros_distinta(os.path.join(c, "configuracion_economica.json")))
    var = json.load(open(os.path.join(c, "configuracion_v64_variantes.json"), encoding="utf-8"))
    paso("C", "variantes calculadas (heredado, activa, componentes aislados, estructuras compatibles y extremos del rango de λ) ligadas al libro evaluado",
         var.get("aplica") and len(var["variantes"]) >= 10 and {"heredado", "activa", "parametro_minimo", "parametro_maximo"} <= {v["clave"] for v in var["variantes"]}
         and all(v.get("zona") for v in var["variantes"]) and var.get("variantes_sin_zona") == [] and var.get("configuracion_economica_sha256") == sha(os.path.join(c, "configuracion_economica.json")))
    pv = os.path.join(c, "configuracion_v64_variantes.json")
    bueno = open(pv, encoding="utf-8").read()
    m_ok = pp.variantes_corresponden()
    var_mal = json.loads(bueno)
    next(v for v in var_mal["variantes"] if v["clave"] == "activa")["ponderado"] += 1.0
    open(pv, "w", encoding="utf-8").write(json.dumps(var_mal, ensure_ascii=False))
    m_mal = pp.variantes_corresponden()
    open(pv, "w", encoding="utf-8").write(bueno)
    paso("C", "paso 12: la variante «activa» tiene que ser la valoración final (precio.json); unas variantes que no corresponden detienen el cierre",
         m_ok is None and m_mal is not None and "no es la valoración final" in m_mal, str(m_mal)[:160])
    f = json.load(open(os.path.join(c, "ficha.json"), encoding="utf-8"))
    inf = open(os.path.join(c, "informe.md"), encoding="utf-8").read()
    paso("C", "ficha e informe identifican plantilla, configuración efectiva y límites (sin presentarla como adoptada)",
         f["versiones"]["plantilla"] == "V6.4 experimental" and (f.get("configuracion_economica") or {}).get("modo") == "Experimental"
         and "## 14. Plantilla y configuración económica" in inf and "no adoptada" in inf and "denominador identificado" in inf)
    mat = json.load(open(os.path.join(c, "material_auditoria.json"), encoding="utf-8"))
    paso("C", "el material auditado vincula configuración económica, selección de plantilla y variantes",
         {"configuracion_economica.json", "plantilla_activa.json", "configuracion_v64_variantes.json"} <= set(mat["archivos"]))
    v_int = open(os.path.join(c, "verificacion_integridad.txt"), encoding="utf-8").read()
    paso("C", "verificación de integridad con el verificador y la referencia de la V6.4", "V6.4 experimental" in v_int and "ÍNTEGRO" in v_int)
    # una ejecución con la V6.3 sobre el expediente V6.4: código 2 sin escribir nada
    antes = listado(c)
    rc, out, _ = correr(c, cfg=None)
    paso("C", "un expediente V6.4 ejecutado con la configuración V6.3: código 2 sin escribir nada", rc == 2 and listado(c) == antes, out.strip().splitlines()[-1][:160])
    # cambio de un parámetro después del cierre, sin recalcular
    conf = json.load(open(os.path.join(c, "configuracion_economica.json"), encoding="utf-8"))
    pond0 = json.load(open(os.path.join(c, "precio.json"), encoding="utf-8"))["ponderado"]
    conf["PM1"]["lambda"] = 1.25
    json.dump(conf, open(os.path.join(c, "configuracion_economica.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    env64 = dict(os.environ, MUNGER_CONFIG=CFG64)  # como los llama el pipeline
    rc_i, out_i = run([PY, os.path.join(PV, "scripts", "informe.py"), c], env=env64)
    filas = open(os.path.join(os.path.dirname(c), "resumen_v2_v64_experimental.csv"), encoding="utf-8").read()
    paso("C", "cambiar λ después del cierre (sin recalcular): informe.py retira la aprobación en la primera llamada y la fila del resumen deja de estar APROBADO",
         rc_i in (3, 5) and "configuracion_economica.json" in out_i and os.path.isdir(os.path.join(c, "historial_cierres")) and "SIN APROBACIÓN VIGENTE" in filas, out_i.strip()[:200])
    rc_f, out_f = run([PY, os.path.join(PV, "scripts", "ficha.py"), c, "--estado", "concluido"], env=env64)
    paso("C", "ficha.py tampoco reaprueba con la configuración cambiada (sin auditoría nueva no hay ficha cerrada)", rc_f != 0 and not os.path.exists(os.path.join(c, "ficha.json")), out_f.strip()[-160:])
    rc, out, _ = correr(c)
    st = json.load(open(os.path.join(c, "estado_pipeline.json"), encoding="utf-8"))
    pond1 = json.load(open(os.path.join(c, "precio.json"), encoding="utf-8"))["ponderado"]
    lam_libro = json.load(open(os.path.join(c, "resultados.json"), encoding="utf-8"))["configuracion_v64"]["lambda"]
    reaplicada = any("configuración económica cambiada" in h for h in st["historial"])
    paso("C", "el pipeline reaplica la configuración, recalcula, pide variantes, fase C y auditoría nuevas y solo entonces vuelve a cerrar",
         rc == 0 and reaplicada and lam_libro == 1.25 and pond1 != pond0 and st.get("auditoria") == "APROBADO" and len(st.get("solicitudes_auditoria") or []) >= 2,
         f"ponderado {pond0} → {pond1} · λ en el libro {lam_libro} · solicitudes {len(st.get('solicitudes_auditoria') or [])}")
    # heredado V6.4 = V6.3 en el pipeline (mismo expediente sintético con motor B)
    c63 = os.path.join(base, "h63", "EmpresaXH")
    c64 = os.path.join(base, "h64", "EmpresaXH")
    preparar_sintetico(c63)
    preparar_sintetico(c64, conf_sintetica("Heredado"))
    rc1, _, _ = correr(c63, cfg=None, fase_c_v64=False)
    rc2, _, _ = correr(c64, fase_c_v64=False)
    r63 = json.load(open(os.path.join(c63, "resultados.json"), encoding="utf-8"))
    r64 = json.load(open(os.path.join(c64, "resultados.json"), encoding="utf-8"))
    p63, p64 = (json.load(open(os.path.join(x, "precio.json"), encoding="utf-8")) for x in (c63, c64))
    s63, s64 = (json.load(open(os.path.join(x, "estado_pipeline.json"), encoding="utf-8")) for x in (c63, c64))
    paso("C", "modo heredado de la V6.4 en el pipeline = V6.3: mismos valores, escalera, estados técnicos y estado final",
         rc1 == 0 and rc2 == 0 and r63["valores"] == r64["valores"] and p63["precio_si"] == p64["precio_si"] and p63["zona"] == p64["zona"]
         and r63["estados"] == r64["estados"] and s63.get("estado_analisis") == s64.get("estado_analisis") and "configuracion_v64" not in r63,
         f"ponderado {p63.get('ponderado')} / {p64.get('ponderado')} · {s63.get('estado_analisis')} / {s64.get('estado_analisis')}")
    # (revisión interna H2) las filas de los expedientes V6.4 van a su propio resumen junto al expediente; las V6.3, al resumen_v2.csv
    def filas_csv(p):
        return list(csv.DictReader(open(p, encoding="utf-8", newline=""))) if os.path.exists(p) else []
    ex = os.path.join(base, "exp")
    act = filas_csv(os.path.join(ex, "resumen_v2_v64_experimental.csv"))  # en exp/ solo está el expediente EmpresaXE
    hist = filas_csv(os.path.join(ex, "resumen_v2_v64_experimental_historial.csv"))
    import cierre_v2 as CIE
    paso("C", "las filas V6.4 (experimental y heredado) se publican en resumen_v2_v64_experimental.csv, con su historial de retiradas aparte, y nunca en el resumen_v2.csv de las filas V6.3 (tampoco a mano con config_v2.json)",
         len(act) == 1 and act[0].get("verificacion", "").startswith("APROBADO") and any((r.get("verificacion") or "").startswith("APROBADO") for r in hist)
         and not any(os.path.exists(os.path.join(ex, f)) for f in ("resumen_v2.csv", "resumen_v2_historial.csv"))
         and os.path.exists(os.path.join(base, "h64", "resumen_v2_v64_experimental.csv")) and not os.path.exists(os.path.join(base, "h64", "resumen_v2.csv"))
         and os.path.exists(os.path.join(base, "h63", "resumen_v2.csv")) and not os.path.exists(os.path.join(base, "h63", "resumen_v2_v64_experimental.csv"))
         and os.path.basename(CIE.ruta_resumen(c, config_v2.cargar(os.path.join(PV, "config_v2.json")))) == "resumen_v2_v64_experimental.csv"
         and os.path.basename(CIE.ruta_resumen(c63, config_v2.cargar(os.path.join(PV, "config_v2.json")))) == "resumen_v2.csv",
         f"fila activa {[r.get('verificacion', '')[:40] for r in act]} · historial {len(hist)} · {sorted(os.listdir(ex))}")


# ======================================================================================= D · cambio de base
def grupo_d():
    import cambiar_base as CB
    conf0 = json.load(open(os.path.join(ENS, "configuracion", "cambio_de_base_control_heredado.json"), encoding="utf-8"))
    base = os.path.join(TMP, "cambio_de_base")
    shutil.rmtree(base, ignore_errors=True)
    hechos = []
    # (4.15, segunda revisión independiente, N7) desde la 4.15 cambiar_base.py prepara los expedientes nuevos con la entrada efectiva
    # «estricta» por defecto. Este control heredado de la 4.11 tiene C50 de Vidrala sostenido solo por la etapa 1 (no reproducible, como
    # declara el hito 1 de la 4.15) y prueba la concordancia del cambio de base, no la entrada efectiva: declara el modo «registrada» con su
    # motivo. La parada del modo estricto con este mismo CAMBIO se prueba aparte, al final del grupo («tres»).
    MOTIVO_REG = ("(4.15) control heredado de la 4.11: C50 de Vidrala lo sostiene solo la etapa 1 (no reproducible, lo bloquea el comprobador "
                  "de entradas); este caso prueba la concordancia del cambio de base")
    for n in ("uno", "dos"):
        conf = copy.deepcopy(conf0)
        conf["entrada_efectiva"] = {"modo": "registrada", "motivo": MOTIVO_REG}
        conf["destino"] = os.path.join(base, n)
        p = os.path.join(base, f"cfg_{n}", "cambio_de_base.json")  # mismo nombre de archivo: la nota de fase1_v63.json lo cita
        os.makedirs(os.path.dirname(p), exist_ok=True)
        json.dump(conf, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        rc, out = run([PY, "-I", os.path.join(PV, "scripts", "cambiar_base.py"), "preparar", p], cwd=RAIZ, timeout=900)
        hechos.append((rc, conf, p, out))
    d1, d2 = (os.path.join(c["destino"], "Vidrala") for _, c, _, _ in hechos)
    activos = ["fase1_metadatos.json", "fase1_v63.json", "alcance_v2.json", "configuracion_economica.json", os.path.join("etapa1", "Vidrala_evaluada.xlsx")]
    iguales = all(rc == 0 for rc, *_ in hechos) and all(open(os.path.join(d1, a), "rb").read() == open(os.path.join(d2, a), "rb").read() for a in activos)
    paso("D", "preparar dos veces el cambio de base da las mismas entradas activas (metadatos, fase1_v63, etapa 1 de ensayo, alcance y configuración)", iguales,
         "; ".join(o.strip().splitlines()[-1][:80] for _, _, _, o in hechos if o.strip()))
    rc, out = run([PY, "-I", os.path.join(PV, "scripts", "cambiar_base.py"), "preparar", hechos[0][2]], cwd=RAIZ)
    paso("D", "no sobrescribe un expediente ya preparado", rc != 0 and "no se sobrescribe" in out)
    # (4.14, incidente del 14-nov-2026) un CAMBIO que no declara una entrada `analisis` del origen que construir no reproduce se detiene
    # (y no deja el destino a medias); descartarla de forma explícita, con su motivo, sí se admite y queda registrado
    # origen de prueba: copia del origen con una entrada `analisis` que construir no reproduce (como las reexpresadas del incidente)
    orig_p = os.path.join(base, "origen_con_C53", "Vidrala")
    shutil.copytree(os.path.join(RAIZ, conf0["origen"]), orig_p, ignore=shutil.ignore_patterns(".lo_perfil", "__pycache__"))
    f1o = json.load(open(os.path.join(orig_p, "fase1_v63.json"), encoding="utf-8"))
    f1o.setdefault("analisis", {})["C53"] = {"valor": 108.352, "fuente": "(prueba) entrada reexpresada de un cambio anterior", "pagina": None, "periodo": "2025", "unidad": "mm"}
    json.dump(f1o, open(os.path.join(orig_p, "fase1_v63.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for n, descarte in (("sin_declarar", None), ("descartada", {"C53": "(prueba) se descarta de forma explícita"})):
        conf = copy.deepcopy(conf0)
        conf["origen"] = orig_p
        conf["analisis"].pop("C53", None)
        conf["destino"] = os.path.join(base, n)
        if descarte:
            conf["analisis_que_se_descartan"] = descarte
        p = os.path.join(base, f"cfg_{n}", "cambio_de_base.json")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        json.dump(conf, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        hechos.append((*run([PY, "-I", os.path.join(PV, "scripts", "cambiar_base.py"), "preparar", p], cwd=RAIZ, timeout=900), n))
    (rc_s, out_s, _), (rc_d, out_d, _) = hechos[-2], hechos[-1]
    paso("D", "(4.14) un CAMBIO que perdería una entrada `analisis` del origen sin declararla se detiene y retira el destino; descartarla con su motivo se admite",
         rc_s != 0 and "PREPARACIÓN DETENIDA" in out_s and "Análisis!C53" in out_s and not os.path.exists(os.path.join(base, "sin_declarar", "Vidrala"))
         and rc_d == 0 and os.path.exists(os.path.join(base, "descartada", "Vidrala", "fase1_v63.json")), (out_s.strip().splitlines() or [""])[-1][:200])
    # (4.14, decisión E6 de Elis) corrección de EXTRACCIÓN en fase1_partes: con lo esperado se aplica antes de construir la Historia y
    # queda registrada (originales en antecedentes); si lo encontrado no es lo esperado, se detiene y retira el destino
    p25 = json.load(open(os.path.join(RAIZ, conf0["origen"], "fase1_partes", "AR_2025.json"), encoding="utf-8"))
    ent_a, ent_b = p25["partidas"]["ventas"]["actual"][0], p25["partidas"]["ventas"]["anterior"][0]
    f1_0 = json.load(open(os.path.join(d1, "fase1_v63.json"), encoding="utf-8"))["historia"]["partidas"]["ventas"]["valores"]
    for n, esperado in (("partes_mal", "no-es-lo-impreso"), ("partes_bien", ent_a["impreso"])):
        conf = copy.deepcopy(conf0)
        conf["destino"] = os.path.join(base, n)
        conf["correcciones_fase1_partes"] = [{"archivo": "AR_2025.json", "partida": "ventas", "lado": "actual", "indice": 0, "esperado": {"impreso": esperado},
                                              "nuevo": dict(ent_a, impreso=ent_b["impreso"]), "fuente": "(prueba) misma página", "motivo": "(prueba) corrección de extracción"}]
        p = os.path.join(base, f"cfg_{n}", "cambio_de_base.json")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        json.dump(conf, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        hechos.append((*run([PY, "-I", os.path.join(PV, "scripts", "cambiar_base.py"), "preparar", p], cwd=RAIZ, timeout=900), n))
    (rc_m, out_m, _), (rc_b, out_b, _) = hechos[-2], hechos[-1]
    ok_b = rc_b == 0
    if ok_b:
        f1_b = json.load(open(os.path.join(base, "partes_bien", "Vidrala", "fase1_v63.json"), encoding="utf-8"))["historia"]["partidas"]["ventas"]["valores"]
        reg_b = json.load(open(os.path.join(base, "partes_bien", "resultados", "cambio_de_base.json"), encoding="utf-8"))
        ok_b = (abs(f1_b[-1] - f1_0[-2]) < 1e-9 and f1_b[:-1] == f1_0[:-1] and len(reg_b.get("correcciones_fase1_partes") or []) == 1
                and os.path.exists(os.path.join(base, "partes_bien", "antecedentes", "fase1_partes_original", "AR_2025.json"))
                and json.load(open(os.path.join(RAIZ, conf0["origen"], "fase1_partes", "AR_2025.json"), encoding="utf-8")) == p25)
    paso("D", "(4.14) una corrección de extracción en fase1_partes con el valor esperado cambia solo esa celda de la Historia, se registra y deja el original en antecedentes "
              "(el origen no se toca); con un valor esperado distinto se detiene y retira el destino",
         ok_b and rc_m != 0 and "PREPARACIÓN DETENIDA" in out_m and not os.path.exists(os.path.join(base, "partes_mal", "Vidrala")),
         (out_m.strip().splitlines() or [""])[-1][:200])
    hechos = hechos[:2]
    reg = json.load(open(os.path.join(hechos[0][1]["destino"], "resultados", "cambio_de_base.json"), encoding="utf-8"))
    ant = json.load(open(os.path.join(hechos[0][1]["destino"], "antecedentes", "evidencia_anterior.json"), encoding="utf-8"))
    paso("D", "la copia de ensayo de la etapa 1 solo cambia las celdas declaradas y los textos anteriores quedan en antecedentes",
         set(reg["etapa1"]["miembros_cambiados"]) <= {"xl/worksheets/sheet1.xml", "xl/worksheets/sheet4.xml"} and "34,185" in str(ant) and "88,70" in str(ant))
    meta = json.load(open(os.path.join(d1, "fase1_metadatos.json"), encoding="utf-8"))
    f1 = json.load(open(os.path.join(d1, "fase1_v63.json"), encoding="utf-8"))
    pat = re.compile("Trading Economics|Bolsaman|35,206 M")
    paso("D", "las notas que reintroducían la tasa o las acciones anteriores se retiran (a antecedentes) y no quedan en metadatos ni en fase1_v63.json",
         not any(pat.search(str(n)) for n in meta.get("_notas", []) + f1.get("_notas", [])) and os.path.exists(os.path.join(hechos[0][1]["destino"], "antecedentes", "notas_retiradas.json")))
    paso("D", "fechas separadas: ejecución real, base 31-dic-2025, precio y acciones a 31-dic-2025", meta["fecha_analisis"] != "2025-12-31" and meta["precio"]["fecha"] == "2025-12-31"
         and meta["acciones_diluidas"]["fecha"] == "2025-12-31")
    # pasos 0–4 del pipeline (V6.4 heredado) y concordancia sin restos
    rc, out = run([PY, PIPE, d1, "--config", CFG64, "--hasta", "4"], timeout=900)
    ok_c = run([PY, "-I", os.path.join(PV, "scripts", "cambiar_base.py"), "comprobar", hechos[0][2]], cwd=RAIZ)
    paso("D", "tras los pasos 0–4 (V6.4 heredado), las entradas concuerdan y no queda ningún resto de la base anterior en la evidencia activa ni en las notas",
         ok_c[0] == 0 and "CONCUERDA Y SIN RESTOS" in ok_c[1], ok_c[1].strip().splitlines()[-1] if ok_c[1].strip() else "")
    # (4.15, N7) el mismo CAMBIO sin declarar el modo: «estricta» por defecto, y el paso 2 se detiene por C50 (código 7 de rellenar)
    conf3 = copy.deepcopy(conf0)
    conf3["destino"] = os.path.join(base, "tres")
    p3 = os.path.join(base, "cfg_tres", "cambio_de_base.json")
    os.makedirs(os.path.dirname(p3), exist_ok=True)
    json.dump(conf3, open(p3, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    rc3, out3 = run([PY, "-I", os.path.join(PV, "scripts", "cambiar_base.py"), "preparar", p3], cwd=RAIZ, timeout=900)
    d3 = os.path.join(base, "tres", "Vidrala")
    est3 = {}
    if rc3 == 0:
        run([PY, PIPE, d3, "--config", CFG64, "--hasta", "4"], timeout=900)
        try:
            est3 = json.load(open(os.path.join(d3, "estado_pipeline.json"), encoding="utf-8"))
        except (OSError, ValueError):
            est3 = {}
    hist3 = " ".join(est3.get("historial") or [])
    paso("D", "(4.15, N7) el mismo CAMBIO sin declarar el modo: entrada efectiva «estricta»; el paso 2 se detiene por C50 (rellenar --estricta → 7) sin escribir el libro de datos",
         rc3 == 0 and est3.get("paso") == 2 and (est3.get("entrada_efectiva") or {}).get("modo") == "estricta" and "--estricta → 7" in hist3 and "Análisis!C50" in hist3
         and not os.path.exists(os.path.join(d3, "Vidrala_v63_datos.xlsx")), (est3.get("estado_analisis"), est3.get("entrada_efectiva"), hist3[-200:]))
    neg = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_10_1", "Vidrala", "Vidrala_v63_evaluada.xlsx")
    sys.path.insert(0, os.path.join(PV, "scripts"))
    restos = []
    from openpyxl import load_workbook
    cm = load_workbook(neg, data_only=True)["Control maestro"]
    proh = [re.compile(x) for x in hechos[0][1]["textos_prohibidos"]]
    for r in range(17, 83):
        for col in "GHIJKLM":
            v = cm[f"{col}{r}"].value
            if isinstance(v, str) and any(p.search(v) for p in proh):
                restos.append(f"{col}{r}")
    paso("D", "control negativo: el libro de la 4.10.1 sí tiene esos restos (M41, M52, …), que la búsqueda encuentra", {"M41", "M52"} <= set(restos), ", ".join(restos[:8]))


# ======================================================================================= E · vigencia en la primera llamada (4.12 §3)
PIL411 = os.path.join(ENS, "piloto")
CFG63 = os.path.join(PV, "config_v2.json")


def huellas_dir(d):
    out = {}
    for r, ds, fs in os.walk(d):
        ds[:] = [x for x in ds if x not in ("__pycache__", ".lo_perfil")]
        for f in fs:
            p = os.path.join(r, f)
            if not os.path.islink(p):
                out[os.path.relpath(p, d)] = sha(p)
    return out


def copia_piloto(nombre):
    """Copia independiente del piloto cerrado de la 4.11 (sin variantes_v64/, prompts ni recálculos, que no son material) con el
    destino del resumen y el registro de publicaciones reubicados DENTRO de la copia: ninguna prueba toca publicaciones originales."""
    import cierre_v2 as CIE
    d = os.path.join(TMP, "vigencia", nombre)
    shutil.rmtree(d, ignore_errors=True)
    shutil.copytree(PIL411, os.path.join(d, "piloto"), ignore=shutil.ignore_patterns(".lo_perfil", "variantes_v64", "prompts_generados", "recalc", "__pycache__"))
    for r, ds, fs in os.walk(d):
        for x in ds + fs:
            os.chmod(os.path.join(r, x), 0o755 if os.path.isdir(os.path.join(r, x)) else 0o644)
    c = os.path.join(d, "piloto", "Vidrala")
    for n in (CIE.REGISTRO_RESUMEN, CIE.RESPALDO_RESUMEN):
        p = os.path.join(c, n)
        if os.path.exists(p):
            reg = json.load(open(p, encoding="utf-8"))
            for e in reg.get("publicaciones") or []:
                e["csv"] = os.path.join(d, "piloto", os.path.basename(e["csv"]))
                e["expediente"] = c
            json.dump(reg, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return c


def alterar(c, tipo):
    pc, pa, pv = (os.path.join(c, f) for f in ("configuracion_economica.json", "plantilla_activa.json", "configuracion_v64_variantes.json"))
    if tipo in ("valida_modificada", "invalida"):
        conf = json.load(open(pc, encoding="utf-8"))
        conf["PM1"]["lambda"] = 1.25 if tipo == "valida_modificada" else 0.9
        json.dump(conf, open(pc, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    elif tipo == "eliminada":
        os.remove(pc)
    elif tipo == "json_roto":
        open(pc, "w", encoding="utf-8").write('{"modo": "Experimental", "N1": ')
    elif tipo == "seleccion_alterada":
        reg = json.load(open(pa, encoding="utf-8"))
        reg["archivo_sha256"] = "0" * 64
        json.dump(reg, open(pa, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    elif tipo == "seleccion_borrada":
        os.remove(pa)
    elif tipo == "variantes_alteradas":
        var = json.load(open(pv, encoding="utf-8"))
        next(v for v in var["variantes"] if v["clave"] == "heredado")["ponderado"] += 1.0
        json.dump(var, open(pv, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def primera_llamada(c, via):
    env = {k: v for k, v in os.environ.items() if k != "MUNGER_CONFIG"}  # llamada a mano: sin la configuración del pipeline
    S = os.path.join(PV, "scripts")
    cmd = {"pipeline": [PY, "-B", os.path.join(S, "pipeline.py"), c, "--config", CFG64, "--hasta", "8"],
           "ficha": [PY, "-B", os.path.join(S, "ficha.py"), c],
           "informe": [PY, "-B", os.path.join(S, "informe.py"), c],
           "resumen": [PY, "-B", os.path.join(S, "resumen.py"), c, os.path.join(os.path.dirname(c), "resumen_v2.csv")]}[via]
    r = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=1800)
    return r.returncode, r.stdout + r.stderr


def retirada_comprobada(c):
    """(ok, detalle): la aprobación del material anterior ya no consta como vigente en ningún sitio y queda el antecedente explicado."""
    st = json.load(open(os.path.join(c, "estado_pipeline.json"), encoding="utf-8"))
    hc = os.path.join(c, "historial_cierres")
    ret = sorted(glob.glob(os.path.join(hc, "*", "RETIRADA.json")))
    mot = json.load(open(ret[-1], encoding="utf-8")).get("motivo") if ret else ""
    filas = list(csv.DictReader(open(os.path.join(os.path.dirname(c), "resumen_v2.csv"), encoding="utf-8", newline="")))
    reg = json.load(open(os.path.join(c, "publicaciones_resumen.json"), encoding="utf-8"))
    ok = (not os.path.exists(os.path.join(c, "ficha.json")) and not os.path.exists(os.path.join(c, "cierre_vigente.json")) and bool(mot)
          and st.get("auditoria") != "APROBADO" and st.get("estado_analisis") != "concluido"
          and filas and all((f.get("verificacion") or "").startswith("SIN APROBACIÓN VIGENTE") for f in filas)
          and all(e.get("estado") != "publicada" for e in reg.get("publicaciones") or []))
    return ok, f"auditoría {st.get('auditoria')} · estado {st.get('estado_analisis')} · antecedentes {len(ret)} · motivo «{str(mot)[:110]}» · fila «{(filas[-1].get('verificacion') or '')[:40] if filas else '—'}»"



def grupo_e_revision_413():
    """(4.13, revisión interna R1 y R2) JSON roto en CADA archivo .json del material con la primera llamada de ficha.py, ficha.json con un
    tipo anidado, y registro de publicaciones o estado con elementos mal formados junto con material cambiado (las cuatro vías)."""
    import cierre_v2 as CIE
    rotos = []
    for n in [m for m in CIE.MATERIAL_FIJO if m.endswith(".json")]:
        c = copia_piloto(f"r1_roto_{n.replace('.', '_')}")
        p = os.path.join(c, n)
        if not os.path.exists(p):
            continue
        t = open(p, encoding="utf-8").read()
        open(p, "w", encoding="utf-8").write(t[: max(1, len(t) // 2)])
        rc, out = primera_llamada(c, "ficha")
        ok, det = retirada_comprobada(c)
        rotos.append((n, ok and "Traceback" not in out, rc, det))
    malos = [x for x in rotos if not x[1]]
    paso("E", "(4.13, R1) JSON roto en cada archivo .json del material: la PRIMERA llamada de ficha.py retira la aprobación sin excepción",
         rotos and not malos, f"{len(rotos)} archivos · fallan {[(x[0], x[2], x[3][:80]) for x in malos][:4]}")
    c = copia_piloto("r1_ficha_hashes")
    pf = os.path.join(c, "ficha.json")
    f = json.load(open(pf, encoding="utf-8"))
    f["hashes"] = "x"
    json.dump(f, open(pf, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    rc, out = primera_llamada(c, "ficha")
    ok, det = retirada_comprobada(c)
    paso("E", "(4.13, R1) ficha.json con un campo anidado de otro tipo («hashes»: texto): ficha.py retira la aprobación sin excepción", ok and "Traceback" not in out, f"rc {rc} · {det}")
    # (4.13, revisión del cambio de la ronda general, H1–H3) combinaciones: un archivo ilegible del material junto con una ficha rota o
    # sin marcadores y sin cierre registrado, y un informe oficial cambiado a mano: la primera llamada de ficha.py retira la aprobación
    def _romper(c, n):
        p = os.path.join(c, n)
        t = open(p, encoding="utf-8").read()
        open(p, "w", encoding="utf-8").write(t[: max(1, len(t) // 2)])

    def _sin_marcadores(c):
        p = os.path.join(c, "ficha.json")
        f = json.load(open(p, encoding="utf-8"))
        f.pop("cierre", None)
        f["estado_analisis"] = "pendiente_de_datos"
        json.dump(f, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for nombre, alt in (("ficha rota, sin cierre_vigente.json y fase_b.json roto", lambda c: (_romper(c, "ficha.json"), os.remove(os.path.join(c, "cierre_vigente.json")), _romper(c, "fase_b.json"))),
                        ("ficha sin marcadores, sin cierre_vigente.json y fase_b.json roto", lambda c: (_sin_marcadores(c), os.remove(os.path.join(c, "cierre_vigente.json")), _romper(c, "fase_b.json"))),
                        ("informe.md cambiado a mano", lambda c: open(os.path.join(c, "informe.md"), "a", encoding="utf-8").write("\nlínea añadida a mano\n"))):
        c = copia_piloto("r1_comb_" + "".join(ch if ch.isalnum() else "_" for ch in nombre)[:40])
        alt(c)
        rc, out = primera_llamada(c, "ficha")
        ok, det = retirada_comprobada(c)
        paso("E", f"(4.13, revisión del cambio de la ronda) {nombre}: la primera llamada de ficha.py retira la aprobación sin excepción", ok and "Traceback" not in out, f"rc {rc} · {det}")
    for via in ("pipeline", "ficha", "informe", "resumen"):
        for caso in ("registro_null", "registro_sin_csv", "estado_campos_nulos"):
            c = copia_piloto(f"r2_{caso}_{via}")
            alterar(c, "valida_modificada")
            pr = os.path.join(c, CIE.REGISTRO_RESUMEN)
            if caso.startswith("registro"):
                reg = json.load(open(pr, encoding="utf-8"))
                reg["publicaciones"].append(None if caso == "registro_null" else {"estado": "publicada", "empresa": "Vidrala"})
                json.dump(reg, open(pr, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            else:
                pe = os.path.join(c, "estado_pipeline.json")
                st = json.load(open(pe, encoding="utf-8"))
                st.update(paso=None, historial=None, cierres_archivados=None)
                json.dump(st, open(pe, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            rc, out = primera_llamada(c, via)
            st = json.load(open(os.path.join(c, "estado_pipeline.json"), encoding="utf-8"))
            filas = list(csv.DictReader(open(os.path.join(os.path.dirname(c), "resumen_v2.csv"), encoding="utf-8", newline="")))
            sin_aprob = filas and all((x.get("verificacion") or "").startswith("SIN APROBACIÓN VIGENTE") for x in filas)
            ok = ("Traceback" not in out and st.get("auditoria") != "APROBADO" and st.get("estado_analisis") != "concluido" and sin_aprob
                  and (caso == "estado_campos_nulos" or rc == 5 or "RETIRADA PENDIENTE" in out))
            paso("E", f"(4.13, R2) material cambiado y {caso.replace('_', ' ')}: la primera llamada de {via} quita la aprobación del estado y de la fila, "
                      "sin excepción" + (" y con la retirada pendiente visible" if caso != "estado_campos_nulos" else ""),
                 ok, f"rc {rc} · estado {st.get('estado_analisis')}/{st.get('auditoria')} · fila {(filas[-1].get('verificacion') or '')[:30] if filas else '—'} · {out.strip()[-160:]}")

def grupo_e():
    import cierre_v2 as CIE
    import config_v2
    import pipeline as P
    import seleccion_plantilla as SEL
    orig = huellas_dir(PIL411)
    c0 = copia_piloto("control")
    paso("E", "la copia aislada del piloto cerrado de la 4.11 es vigente antes de alterarla (destinos y registro reubicados en la copia)",
         CIE.motivo_vigencia(c0, P.Pipeline.veredicto_auditoria, "Vidrala") is None)
    esperado_rc = {"pipeline": {"valida_modificada": (0,), "variantes_alteradas": (0,)}, "ficha": {}, "informe": {}, "resumen": {}}
    for tipo in ("valida_modificada", "invalida", "eliminada", "json_roto", "seleccion_alterada", "seleccion_borrada", "variantes_alteradas"):
        malos, det = [], []
        for via in ("pipeline", "ficha", "informe", "resumen"):
            c = copia_piloto(f"{tipo}_{via}")
            alterar(c, tipo)
            rc, out = primera_llamada(c, via)
            ok, d = retirada_comprobada(c)
            rc_ok = rc in esperado_rc[via].get(tipo, (2,) if via == "pipeline" else (3,))
            if not (ok and rc_ok):
                malos.append(f"{via}: rc {rc} · {d} · {out.strip().splitlines()[-1][:160] if out.strip() else ''}")
            det.append(f"{via} rc {rc}")
        paso("E", f"{tipo}: en la PRIMERA llamada de cada vía (pipeline, ficha, informe, resumen), cada una en su copia, la aprobación y su publicación "
             "se retiran antes de detener o rechazar, con el antecedente y el motivo", not malos, "; ".join(malos)[:500] or " · ".join(det))
    # (4.13 §3) tipos JSON erróneos (nulo, lista, escalar y estructuras anidadas): en la PRIMERA llamada de cada vía, cada una en su
    # copia, la aprobación se retira antes de detener o rechazar, sin excepciones (la 4.12 daba AttributeError antes de la vigencia en
    # nueve de estas llamadas y conservaba concluido/APROBADO, la ficha cerrada, el cierre registrado y la fila aprobada)
    def alterar_tipo(c, f, ruta, valor):
        pth = os.path.join(c, f)
        if ruta is None:
            json.dump(valor, open(pth, "w", encoding="utf-8"))
            return
        d = json.load(open(pth, encoding="utf-8"))
        x = d
        for k in ruta[:-1]:
            x = x[k]
        x[ruta[-1]] = valor
        json.dump(d, open(pth, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    TIPOS_413 = {"configuracion_economica nula": ("configuracion_economica.json", None, None), "configuracion_economica lista": ("configuracion_economica.json", None, []),
                 "configuracion_economica escalar": ("configuracion_economica.json", None, 3), "N1 lista": ("configuracion_economica.json", ["N1"], []),
                 "PM1 texto": ("configuracion_economica.json", ["PM1"], "x"), "trazabilidad anidada lista": ("configuracion_economica.json", ["trazabilidad", "modo"], []),
                 "plantilla_activa nula": ("plantilla_activa.json", None, None), "plantilla_activa lista": ("plantilla_activa.json", None, []),
                 "plantilla_activa escalar": ("plantilla_activa.json", None, "V6.4"), "plantilla_activa huella lista": ("plantilla_activa.json", ["archivo_sha256"], []),
                 "variantes nulas": ("configuracion_v64_variantes.json", None, None), "variantes objeto": ("configuracion_v64_variantes.json", ["variantes"], {}),
                 "material_auditoria lista": ("material_auditoria.json", None, []), "cierre_vigente lista": ("cierre_vigente.json", None, [])}
    for tipo, (f413, ruta, valor) in TIPOS_413.items():
        malos, det = [], []
        for via in ("pipeline", "ficha", "informe", "resumen"):
            c = copia_piloto(f"tipo_{re.sub(r'[^a-z0-9]', '_', tipo)}_{via}")
            alterar_tipo(c, f413, ruta, valor)
            rc, out = primera_llamada(c, via)
            ok, d = retirada_comprobada(c)
            rc_ok = rc in ((0, 2) if via == "pipeline" else (3,))
            if not (ok and rc_ok) or "Traceback" in out:
                malos.append(f"{via}: rc {rc} · {d} · {out.strip().splitlines()[-1][:160] if out.strip() else ''}")
            det.append(f"{via} rc {rc}")
        paso("E", f"(4.13) {tipo}: primera llamada de cada vía, cada una en su copia: sin excepciones, la aprobación y su publicación se retiran con el antecedente y el motivo",
             not malos, "; ".join(malos)[:500] or " · ".join(det))
    # (4.13 §3) estado del pipeline de otro tipo y registro de publicaciones de otra estructura: retirada o retirada pendiente visible
    malos = []
    for via in ("pipeline", "ficha", "informe", "resumen"):
        c = copia_piloto(f"estado_lista_{via}")
        alterar_tipo(c, "estado_pipeline.json", None, [])
        rc, out = primera_llamada(c, via)
        filas = list(csv.DictReader(open(os.path.join(os.path.dirname(c), "resumen_v2.csv"), encoding="utf-8", newline="")))
        if not (rc in ((6,) if via == "pipeline" else (3,)) and not os.path.exists(os.path.join(c, "ficha.json")) and not os.path.exists(os.path.join(c, "cierre_vigente.json"))
                and filas and all((r.get("verificacion") or "").startswith("SIN APROBACIÓN VIGENTE") for r in filas) and "Traceback" not in out):
            malos.append(f"{via}: rc {rc} · {out.strip().splitlines()[-1][:140] if out.strip() else ''}")
        c = copia_piloto(f"registro_lista_{via}")
        alterar_tipo(c, "publicaciones_resumen.json", None, [])
        rc, out = primera_llamada(c, via)
        if not (rc == 5 and "RETIRADA PENDIENTE" in out and "Traceback" not in out):
            malos.append(f"registro {via}: rc {rc} · {out.strip().splitlines()[-1][:140] if out.strip() else ''}")
    paso("E", "(4.13) estado_pipeline.json como lista: las cuatro vías retiran la aprobación; registro de publicaciones como lista: las cuatro vías se detienen con la retirada pendiente visible (código 5), informe.py incluido",
         not malos, "; ".join(malos)[:500])
    # material intacto y llamada con la plantilla equivocada: se rechaza sin escribir nada
    c = copia_piloto("intacto_v63")
    antes = huellas_dir(os.path.dirname(c))
    env = {k: v for k, v in os.environ.items() if k != "MUNGER_CONFIG"}
    r = subprocess.run([PY, "-B", os.path.join(PV, "scripts", "pipeline.py"), c, "--config", CFG63], capture_output=True, text=True, env=env, timeout=600)
    paso("E", "material intacto y llamada con la configuración V6.3: código 2, ningún archivo escrito y la aprobación sigue vigente",
         r.returncode == 2 and huellas_dir(os.path.dirname(c)) == antes and CIE.motivo_vigencia(c, P.Pipeline.veredicto_auditoria, "Vidrala") is None,
         (r.stdout + r.stderr).strip().splitlines()[-1][:200])
    # archivos de plantilla, referencia o verificador distintos de las huellas registradas: el nombre guardado no los acredita
    cfg64 = json.load(open(CFG64, encoding="utf-8"))
    malos = []
    for clave in ("archivo", "referencia", "verificador"):
        c = copia_piloto(f"archivos_{clave}")
        antes = huellas_dir(os.path.dirname(c))
        tmpd = os.path.join(TMP, "vigencia", f"cfg_{clave}")
        os.makedirs(tmpd, exist_ok=True)
        cf = copy.deepcopy(cfg64)
        for k in ("archivo", "referencia", "verificador", "scripts_v63", "add_sliders", "patch_base", "ejemplo_empresa_x", "docs"):
            cf["plantilla"][k] = os.path.normpath(os.path.join(PV, cf["plantilla"][k]))
        alt = os.path.join(tmpd, os.path.basename(cf["plantilla"][clave]))
        shutil.copy(cf["plantilla"][clave], alt)
        with open(alt, "ab") as fh:
            fh.write(b"\n")  # mismo nombre y misma «versión», otros bytes
        cf["plantilla"][clave] = alt
        cfp = os.path.join(tmpd, "config_v64_alterada.json")
        json.dump(cf, open(cfp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        r = subprocess.run([PY, "-B", os.path.join(PV, "scripts", "pipeline.py"), c, "--config", cfp], capture_output=True, text=True, env=env, timeout=600)
        out = (r.stdout + r.stderr).strip()
        if not (r.returncode == 2 and huellas_dir(os.path.dirname(c)) == antes and f"{clave}_sha256" in out):
            malos.append(f"{clave}: rc {r.returncode} · {out.splitlines()[-1][:160] if out else ''}")
    paso("E", "archivos de plantilla, referencia o verificador con otros bytes y el mismo nombre y versión: código 2 sin escribir nada (las huellas registradas no se acreditan con el identificador)",
         not malos, "; ".join(malos))
    # un generador llamado a mano sin MUNGER_CONFIG resuelve la selección registrada (y no la de la V6.3)
    cfg_r, m_r, nota = SEL.resolver(c0, config_v2.cargar(CFG63))
    paso("E", "una llamada a mano con config_v2.json sobre un expediente V6.4 resuelve la selección registrada (config_v2_v64_experimental.json) o no genera nada",
         m_r is None and SEL.es_v64(cfg_r) and "resuelta" in (nota or ""), nota)
    # un resumen que no se puede actualizar: la retirada queda pendiente y visible, sin seguir como aprobado
    c = copia_piloto("resumen_inaccesible")
    alterar(c, "invalida")
    rcsv = os.path.join(os.path.dirname(c), "resumen_v2.csv")
    os.remove(rcsv)
    os.makedirs(rcsv)  # el destino registrado existe, pero no se puede escribir como archivo
    rc, out = primera_llamada(c, "pipeline")
    st = json.load(open(os.path.join(c, "estado_pipeline.json"), encoding="utf-8"))
    reg = json.load(open(os.path.join(c, "publicaciones_resumen.json"), encoding="utf-8"))
    paso("E", "resumen que no se puede actualizar: la retirada queda pendiente y visible (código 5, registro «retirada_pendiente») y nada sigue como aprobado",
         rc == 5 and "RETIRADA PENDIENTE" in out and st.get("auditoria") != "APROBADO" and st.get("estado_analisis") != "concluido"
         and not os.path.exists(os.path.join(c, "ficha.json")) and any(e.get("estado") == "retirada_pendiente" for e in reg.get("publicaciones") or []),
         f"rc {rc} · {[e.get('estado') for e in reg.get('publicaciones') or []]} · {out.strip().splitlines()[-1][:160] if out.strip() else ''}")
    paso("E", "el piloto original y sus publicaciones no cambian con ninguna de estas pruebas", huellas_dir(PIL411) == orig)


# ======================================================================================= F · materialidad y protocolo del objetivo (4.12 §4)
def grupo_f():
    import configuracion_economica as CE
    import objetivo_v64 as OBJ
    import pipeline as P
    import config_v2
    import resumen as RS
    base = os.path.join(TMP, "objetivo")
    shutil.rmtree(base, ignore_errors=True)
    # configuración: protocolo opcional, validado, y solo en modo experimental
    cf = conf_sintetica()
    paso("F", "protocolo_objetivo: opcional (las configuraciones de la 4.11 siguen siendo válidas), uno de los dos si está y nunca en modo heredado",
         not CE.validar(conf_sintetica(protocolo=None)) and not CE.validar(cf) and CE.validar({**cf, "protocolo_objetivo": "otro"})
         and CE.validar({**conf_sintetica("Heredado"), "protocolo_objetivo": "objetivo_condicionado"}) and not CE.validar(conf_sintetica("Heredado")))
    # tabla del tratamiento (sin LibreOffice)
    fc0 = {"conclusion_provisional": "esperar", "limite_del_modelo": {"aplica": False}}
    caro, cumple = {"zona": "caro", "precio_si": 10.0}, {"zona": "cumple_regla_k", "precio_si": 10.0}
    t = lambda fc, pr, H, Pr, S, am=False: OBJ.tratamiento(fc, pr, H, Pr, S, am)[:2]  # noqa: E731
    casos = [t(fc0, caro, [], "bloqueo_del_objetivo", True) == ("objetivo_emitido", None),
             t(fc0, caro, ["x"], None, True) == ("objetivo_sin_protocolo", None),
             t(fc0, caro, ["x"], "bloqueo_del_objetivo", True) == ("objetivo_bloqueado", "protocolo_de_bloqueo"),
             t(fc0, caro, ["x"], "objetivo_condicionado", True) == ("objetivo_condicionado", None),
             t(fc0, caro, ["x"], "objetivo_condicionado", False) == ("objetivo_bloqueado", "accion_no_sostenida_en_el_ambito"),
             t(fc0, caro, ["x"], "objetivo_condicionado", True, True)[0] == "sin_objetivo",  # S-19 manda
             t({**fc0, "conclusion_provisional": "comprar"}, cumple, ["x"], "objetivo_condicionado", True)[0] == "sin_objetivo",
             t(fc0, cumple, ["x"], None, True)[0] == "sin_objetivo",  # esperar por una condición que no es de precio
             t({**fc0, "conclusion_provisional": "descartar"}, caro, ["x"], None, True)[0] == "sin_objetivo"]
    paso("F", "tratamiento del objetivo: emitido sin condicionantes; sin protocolo, bloqueo, condicionado y no sostenido; S-19, comprar, condición no de precio y descartar quedan fuera",
         all(casos), str(casos))
    # tres pasadas completas con agentes simulados: los dos protocolos y su ausencia
    exp = {}
    for nombre, prot in (("condicionado", "objetivo_condicionado"), ("bloqueo", "bloqueo_del_objetivo"), ("sin", None)):
        c = os.path.join(base, nombre, "EmpresaXO")
        preparar_sintetico(c, conf_sintetica(protocolo=prot))
        rc, out, _ = correr(c)
        exp[nombre] = (c, rc, out)
    c, rc, out = exp["condicionado"]
    st = json.load(open(os.path.join(c, "estado_pipeline.json"), encoding="utf-8"))
    f = json.load(open(os.path.join(c, "ficha.json"), encoding="utf-8"))
    ob = f.get("objetivo") or {}
    pr = json.load(open(os.path.join(c, "precio.json"), encoding="utf-8"))
    inf = open(os.path.join(c, "informe.md"), encoding="utf-8").read()
    fila = (list(csv.DictReader(open(os.path.join(os.path.dirname(c), "resumen_v2_v64_experimental.csv"), encoding="utf-8", newline=""))) or [{}])[0]
    paso("F", "presentación condicionada con la acción sostenida: concluido · APROBADO · esperar; la ficha distingue valor calculado, objetivo emitido, marca provisional, hipótesis, rango y ámbito",
         rc == 0 and st.get("estado_analisis") == "concluido" and st.get("auditoria") == "APROBADO" and f["decision"]["accion"] == "esperar"
         and ob.get("tratamiento") == "objetivo_condicionado" and ob.get("provisional") is True and ob.get("precio_objetivo_emitido") == f["decision"]["precio_objetivo"] == pr["precio_si"]
         and ob.get("valor_calculado_condicional") == pr["precio_si"] and "PM1.parametro" in [h["hipotesis"] for h in ob.get("hipotesis_que_lo_condicionan")]
         and (ob.get("rango_calculado") or {}).get("n_escenarios", 0) >= 10 and "no es un intervalo de confianza" in (ob.get("rango_calculado") or {}).get("naturaleza", ""),
         f"rc {rc} · {st.get('estado_analisis')} · {ob.get('tratamiento')} · {ob.get('precio_objetivo_emitido')}")
    paso("F", "informe (línea de estado y sección 14) y resumen V6.4 muestran el objetivo condicionado, su rango y sus límites sin llamarlo intervalo de confianza",
         "(condicionado, provisional: es el valor calculado condicional; lo condicionan" in inf and "en la activa y " in inf and "que no es un intervalo de confianza" in inf and "Objetivo y materialidad (protocolo experimental 4.12; no adoptado)" in inf
         and fila.get("protocolo_objetivo") == "objetivo_condicionado" and fila.get("estado_del_objetivo") == "emitido_condicionado" and fila.get("objetivo_provisional") == "True"
         and fila.get("rango_precio_si_min") not in ("", None), str({k: fila.get(k) for k in RS.COLS_V64}))
    apt = f.get("aptitud_de_uso") or {}
    paso("F", "aptitud de uso separada de la auditoría (4.12 §9): ficha, informe §1 y resumen V6.4 dicen «experimental» y que ni APROBADO ni «concluido» la acreditan",
         apt.get("caracter") == "experimental" and "dinero real" in str(apt.get("no_apto_para")) and "16 reglas" in str(apt.get("distinta_de_la_auditoria"))
         and "**Aptitud de uso (evaluación de la entrega" in inf and fila.get("aptitud_de_uso") == "experimental" and st.get("auditoria") == "APROBADO",
         json.dumps(apt, ensure_ascii=False)[:300])
    # (4.12, revisión interna R3) un subparámetro de P-M1 (la familia) que solo varían las variantes que quitan P-M1 entera no queda cubierto
    # por el ámbito; el parámetro, con sus extremos aislados, sí. No cambia el tratamiento del objetivo
    fc_r3 = copy.deepcopy(json.load(open(os.path.join(c, "fase_c.json"), encoding="utf-8")))
    for p_ in (fc_r3.get("configuracion_v64") or {}).get("parametros") or []:
        if p_.get("clave") == "PM1.familia":
            p_.update(material_para_objetivo=True, fundamento_suficiente=False, informacion_que_falta="familia no observada (sintético)")
            if isinstance(p_.get("juicio_objetivo"), dict):  # (4.14) con el contrato nuevo la materialidad para el objetivo es la del bloque
                p_["base_de_la_materialidad_objetivo"] = "juicio_economico"
                p_["juicio_objetivo"].update(material=True, base="juicio_economico", comparado_con=None,
                                             criterio={"origen": "juicio_propio_del_agente", "descripcion": "familia no observada (sintético)", "referencia": None})
    ev_r3 = OBJ.evaluar(c, fc=fc_r3)
    paso("F", "cobertura del ámbito: la familia de P-M1 sin ninguna variante aislada queda «no cubierta»; el parámetro, con sus extremos, cubierto; el tratamiento no cambia",
         ev_r3 is not None and "PM1.familia" in ev_r3["hipotesis_que_condicionan"] and "PM1.familia" in ev_r3["hipotesis_no_cubiertas"]
         and "PM1.parametro" not in ev_r3["hipotesis_no_cubiertas"] and ev_r3["tratamiento"] == "objetivo_condicionado",
         f"{(ev_r3 or {}).get('hipotesis_que_condicionan')} · no cubiertas {(ev_r3 or {}).get('hipotesis_no_cubiertas')}")
    c2, rc2, out2 = exp["bloqueo"]
    st2 = json.load(open(os.path.join(c2, "estado_pipeline.json"), encoding="utf-8"))
    f2 = json.load(open(os.path.join(c2, "ficha.json"), encoding="utf-8"))
    ob2 = f2.get("objetivo") or {}
    dg2 = json.load(open(os.path.join(c2, "diagnostico.json"), encoding="utf-8"))
    paso("F", "bloqueo del objetivo: pendiente_de_datos · Vigilar · sin acción ni objetivo emitido, con el valor calculado como condicional y un diagnóstico que dice qué falta",
         rc2 == 0 and st2.get("estado_analisis") == "pendiente_de_datos" and f2["cubo"] == "Vigilar" and (f2.get("decision") or {}).get("accion") is None
         and (f2.get("decision") or {}).get("precio_objetivo") is None and ob2.get("tratamiento") == "objetivo_bloqueado" and ob2.get("origen_del_bloqueo") == "protocolo_de_bloqueo"
         and ob2.get("precio_objetivo_emitido") is None and ob2.get("valor_calculado_condicional") == pr["precio_si"] and (dg2.get("causa") or {}).get("tipo") == "falta_de_datos"
         and "objetivo bloqueado" in str((dg2.get("causa") or {}).get("detalle")), f"rc {rc2} · {st2.get('estado_analisis')} · {(dg2.get('causa') or {}).get('detalle', '')[:120]}")
    c3, rc3, out3 = exp["sin"]
    st3 = json.load(open(os.path.join(c3, "estado_pipeline.json"), encoding="utf-8"))
    f3 = json.load(open(os.path.join(c3, "ficha.json"), encoding="utf-8"))
    ob3 = f3.get("objetivo") or {}
    dg3 = open(os.path.join(c3, "diagnostico.md"), encoding="utf-8").read()
    fila3 = (list(csv.DictReader(open(os.path.join(os.path.dirname(c3), "resumen_v2_v64_experimental.csv"), encoding="utf-8", newline=""))) or [{}])[0]
    paso("F", "sin protocolo y con condicionantes: ningún objetivo oficial (no_entregable · límite del modelo en el paso 10), con las dos lecturas explicadas y sin elegir ninguna",
         st3.get("estado_analisis") == "no_entregable" and f3.get("decision") is None and ob3.get("tratamiento") == "objetivo_sin_protocolo" and ob3.get("precio_objetivo_emitido") is None
         and set((ob3.get("lecturas_posibles") or {})) == {"bloqueo_del_objetivo", "objetivo_condicionado"} and "Con bloqueo_del_objetivo" in dg3 and "Con objetivo_condicionado" in dg3
         and fila3.get("precio_objetivo_emitido") == "" and fila3.get("estado_del_objetivo") == "no_emitido_falta_protocolo", f"{st3.get('estado_analisis')} · {ob3.get('tratamiento')}")
    # (4.12, auditoría del cierre de bloqueo de Vidrala, punto 10) la línea de estado de la sección 1 da el rango calculado y su ámbito
    # también con el objetivo bloqueado o sin protocolo, sin precio objetivo emitido y sin llamarlo intervalo de confianza
    l1 = {}
    for nombre in ("bloqueo", "sin"):
        txt = open(os.path.join(exp[nombre][0], "informe.md"), encoding="utf-8").read()
        l1[nombre] = next((x for x in txt.splitlines() if x.startswith("**Estado `")), "")
    paso("F", "informe §1 con el objetivo bloqueado o sin protocolo: valor calculado condicional no emitido, sin precio objetivo, y rango calculado con su ámbito sin llamarlo intervalo de confianza",
         "objetivo bloqueado" in l1["bloqueo"] and "ningún objetivo oficial" in l1["sin"]
         and all("valor calculado condicional, no emitido" in x and "rango calculado del precio de Sí" in x and "escenarios calculados, que no es un intervalo de confianza" in x
                 and "precio objetivo " not in x for x in l1.values()), " || ".join(x[:300] for x in l1.values()))
    # presentación condicionada sin acción sostenida (la fase C declara λ material para la acción)
    c4 = os.path.join(base, "no_sostenida", "EmpresaXO")
    preparar_sintetico(c4, conf_sintetica())
    rc4, out4, _ = correr(c4, opciones_v64={"material_accion": ("PM1.parametro",)})
    st4 = json.load(open(os.path.join(c4, "estado_pipeline.json"), encoding="utf-8"))
    ob4 = (json.load(open(os.path.join(c4, "ficha.json"), encoding="utf-8")).get("objetivo") or {})
    paso("F", "presentación condicionada sin acción sostenida en el ámbito: pendiente_de_investigacion, objetivo bloqueado (origen: acción no sostenida)",
         rc4 == 0 and st4.get("estado_analisis") == "pendiente_de_investigacion" and ob4.get("origen_del_bloqueo") == "accion_no_sostenida_en_el_ambito" and ob4.get("precio_objetivo_emitido") is None,
         f"rc {rc4} · {st4.get('estado_analisis')} · {ob4.get('tratamiento')} · {ob4.get('origen_del_bloqueo')}")
    # información material insuficiente: un dato ausente material (S-19) manda antes que cualquier protocolo
    c5 = os.path.join(base, "s19", "EmpresaXO")
    preparar_sintetico(c5, conf_sintetica())
    rc5, out5, _ = correr(c5, material_ausente="__primero__")
    da5 = json.load(open(os.path.join(c5, "datos_ausentes.json"), encoding="utf-8")) if os.path.exists(os.path.join(c5, "datos_ausentes.json")) else []
    dato5 = (da5[0] if da5 else {}).get("dato")
    st5 = json.load(open(os.path.join(c5, "estado_pipeline.json"), encoding="utf-8"))
    f5 = json.load(open(os.path.join(c5, "ficha.json"), encoding="utf-8")) if os.path.exists(os.path.join(c5, "ficha.json")) else {}
    ob5 = f5.get("objetivo") or {}
    paso("F", "información material insuficiente (dato ausente material, S-19) con el protocolo condicionado: pendiente_de_datos y el objetivo «sin objetivo» (S-19 manda antes que el protocolo)",
         bool(dato5) and rc5 == 0 and st5.get("estado_analisis") == "pendiente_de_datos" and ob5.get("tratamiento") == "sin_objetivo" and ob5.get("precio_objetivo_emitido") is None
         and dato5 in ((ob5.get("materialidad") or {}).get("datos_ausentes_materiales") or []), f"rc {rc5} · {st5.get('estado_analisis')} · {ob5.get('tratamiento')} · dato {dato5}")
    # contradicciones (sobre el material del expediente condicionado, sin LibreOffice)
    pp = P.Pipeline(c, config_v2.cargar(CFG64))
    fcb = json.load(open(os.path.join(c, "fase_c.json"), encoding="utf-8"))
    paso("F", "el material del expediente condicionado es coherente (control positivo de las contradicciones)", pp.coherencia_fase_c(copy.deepcopy(fcb)) is None)

    def mal(nombre, cambio, esperado):
        x = copy.deepcopy(fcb)
        cambio(x)
        m = pp.coherencia_fase_c(x)
        paso("F", f"contradicción detectada: {nombre}", bool(m) and esperado in m, str(m)[:200])
    par = lambda x, k: next(q for q in x["configuracion_v64"]["parametros"] if q["clave"] == k)  # noqa: E731
    mal("ámbito de un parámetro distinto del de las variantes calculadas", lambda x: par(x, "PM1.parametro").update(ambito=["heredado"]), "no es el de configuracion_v64_variantes.json")
    # (4.13 §5) con el contrato de cobertura, null es «no determinada» y tiene que ir con esa base (no se fuerza true o false)
    mal("material_para_accion = null con la base «calculada» (4.13: null ⇔ no determinada)", lambda x: par(x, "PM1.parametro").update(material_para_accion=None), "si y solo si")
    import objetivo_v64 as OBJ

    def revisar(x):  # discrepancias con la configuración recalculadas tras un cambio de la prueba (como haría un agente cuidadoso)
        for q in x["configuracion_v64"]["parametros"]:
            q["contradicciones_revisadas"] = [{"discrepancia": d, "resolucion": "revisada (sintético)"} for d in OBJ.discrepancias_con_la_configuracion(conf_c, q)]
    conf_c = json.load(open(os.path.join(c, "configuracion_economica.json"), encoding="utf-8"))
    paso("F", "(4.13 §5) control positivo: la familia (cubierta solo por variaciones conjuntas) declarada «no determinada» con null es coherente",
         next((q for q in fcb["configuracion_v64"]["parametros"] if q["clave"] == "PM1.familia"), {}).get("base_de_la_materialidad") == "no_determinada"
         and pp.coherencia_fase_c(copy.deepcopy(fcb)) is None)
    mal("(4.13 §5) materialidad «calculada» de la familia, cubierta solo por variaciones conjuntas (quitar P-M1 entera no la contrasta)",
        lambda x: par(x, "PM1.familia").update(material_para_accion=False, base_de_la_materialidad="calculada"), "materialidad «calculada» con cobertura variacion_conjunta")
    mal("(4.13 §5) cobertura distinta de la de las variantes calculadas", lambda x: par(x, "PM1.familia").update(cobertura="contraste_aislado"), "no es la de las variantes calculadas")
    mal("(4.13 §5) juicio económico sin inferencias", lambda x: par(x, "PM1.familia").update(material_para_accion=False, base_de_la_materialidad="juicio_economico", inferencias=[]),
        "declara sus inferencias")
    mal("(4.13 §5) parámetro sin evidencia citada", lambda x: par(x, "PM1.parametro").update(evidencia=[]), "evidencia")
    mal("(4.13 §5) hechos e inferencias sin separar (sin hechos)", lambda x: par(x, "PM1.parametro").update(hechos=[]), "hechos")

    def fundado(x):
        par(x, "PM1.parametro").update(fundamento_suficiente=True, informacion_que_falta=None, contradicciones_revisadas=[])
    mal("(4.13 §5) fundamento suficiente frente a una hipótesis de confianza baja en la configuración, sin revisar la discrepancia", fundado, "faltan por revisar")
    paso("F", "(4.13 §5) juicio económico con evidencia e inferencias para un parámetro sin contraste aislado: se acepta y se identifica como juicio",
         pp.coherencia_fase_c((lambda x: (par(x, "PM1.familia").update(material_para_accion=False, base_de_la_materialidad="juicio_economico",
                                                                         inferencias=["la otra familia no cambiaría la zona por … (sintético)"]), x)[1])(copy.deepcopy(fcb))) is None)
    if (json.loads(open(os.path.join(c, "configuracion_v64_variantes.json"), encoding="utf-8").read()).get("avisos_de_dominio_variantes") or {}):
        mal("(4.13 §5) un grupo de avisos de dominio de las variantes sin evaluar", lambda x: x["configuracion_v64"].update(avisos_de_dominio_variantes=[]), "falta evaluar el aviso")
    pv = os.path.join(c, "configuracion_v64_variantes.json")
    bueno = open(pv, encoding="utf-8").read()
    v_sin = json.loads(bueno)
    for q in v_sin["variantes"]:
        q["parametros_variados"] = [k for k in q.get("parametros_variados") or [] if k != "N3.circulante"]
    open(pv, "w", encoding="utf-8").write(json.dumps(v_sin, ensure_ascii=False))
    try:
        mal("material_para_accion = false «calculada» sin ninguna variante calculada que lo varíe (no determinada)",
            lambda x: par(x, "N3.circulante").update(material_para_accion=False, ambito=[], cobertura="sin_cobertura", base_de_la_materialidad="calculada"),
            "materialidad «calculada» con cobertura sin_cobertura")
    finally:
        open(pv, "w", encoding="utf-8").write(bueno)
    mal("material_para_conclusion que no es acción u objetivo (compatibilidad)", lambda x: par(x, "PM1.parametro").update(material_para_conclusion=False), "material_para_conclusion")
    mal("hipótesis sin fundamento suficiente sin la información que falta", lambda x: par(x, "PM1.parametro").update(informacion_que_falta=""), "informacion_que_falta")
    mal("objetivo emitido sin condiciones con hipótesis que lo condicionan", lambda x: x["configuracion_v64"]["objetivo"].update(tratamiento="objetivo_emitido"), "no corresponde")
    mal("falta una hipótesis D10 entre las que condicionan el objetivo", lambda x: x["configuracion_v64"]["objetivo"]["hipotesis_que_condicionan"].pop(), "hipotesis_que_condicionan")
    mal("protocolo distinto del declarado en la configuración", lambda x: x["configuracion_v64"]["objetivo"].update(protocolo="bloqueo_del_objetivo"), "protocolo")
    mal("acción sostenida afirmada con un condicionante material para la acción", lambda x: par(x, "PM1.parametro").update(material_para_accion=True, material_para_conclusion=True), "accion_sostenida_en_ambito")
    mal("ámbito del objetivo incompleto", lambda x: x["configuracion_v64"]["objetivo"]["ambito"].pop(), "TODO el ámbito")

    def bloqueo_sin_protocolo(x):
        x.update(estado_analisis="pendiente_de_datos", cubo_final="Vigilar")
        x["decision"].update(accion=None, precio_objetivo=None)
        x["configuracion_v64"]["objetivo"].update(tratamiento="objetivo_bloqueado", origen_del_bloqueo="protocolo_de_bloqueo")
    mal("pendiente_de_datos sin dato ausente material y sin el protocolo de bloqueo (S-19 se conserva)", bloqueo_sin_protocolo, "S-19")
    # «la zona no cambia» solo para las variantes calculadas; una variante que cambia la acción por la zona
    v = json.loads(bueno)
    pm = next(q for q in v["variantes"] if q["clave"] == "parametro_maximo")
    pm["zona"] = "cumple_regla_k"
    v["zonas_calculadas"], v["zona_igual_en_todas_las_calculadas"] = sorted({q["zona"] for q in v["variantes"]}), False
    open(pv, "w", encoding="utf-8").write(json.dumps(v, ensure_ascii=False))
    m_z = pp.coherencia_fase_c(copy.deepcopy(fcb))
    ev_z = OBJ.evaluar(c, copy.deepcopy(fcb))
    open(pv, "w", encoding="utf-8").write(bueno)
    paso("F", "una variante calculada que cambia la acción por la zona: «la zona no cambia» y la acción sostenida dejan de admitirse",
         bool(m_z) and ("no lo respalda" in m_z or "accion_sostenida" in m_z or "cambian la acción" in m_z) and ev_z["accion_sostenida_en_ambito"] is False
         and ev_z["tratamiento"] == "objetivo_bloqueado", str(m_z)[:200])
    # compra: D10 cubre también los parámetros experimentales sin fundamento suficiente (zona y variantes en «cumple la regla» en copias
    # temporales de precio.json y de las variantes, que se restauran)
    conf = json.load(open(os.path.join(c, "configuracion_economica.json"), encoding="utf-8"))
    pj = os.path.join(c, "precio.json")
    pr_bueno = open(pj, encoding="utf-8").read()
    cj = os.path.join(c, "comprobacion_conjunta.json")
    lam = CE.celda_principal("PM1.parametro", conf)

    def compra(fc_mod=None, ccj=None, completa=False):
        x = copy.deepcopy(fcb)
        x.update(estado_analisis="concluido", cubo_final="Sí", conclusion_provisional="comprar", cubo_provisional="Sí")
        x["decision"].update(accion="comprar", precio_objetivo=None, condicion=None)
        x["fundamento_material"].update(resultado="comprobacion_conjunta_superada")
        for h in x["fundamento_material"]["hipotesis_sin_fundamento"]:
            h["alternativas_defendibles"] = {"hay_base": True, "rango": [0, 1], "evidencia": "límites atados a hechos de la empresa (sintético)"}
        x["fundamento_material"]["comprobacion_conjunta"] = {"procede": True, "combinacion": {"Palancas!C15": 0.1}, "coherencia_economica": "sintética", "sobrevive": True}
        if fc_mod:
            fc_mod(x)
        pr2 = json.loads(pr_bueno)
        pr2["zona"] = "cumple_regla_k"
        open(pj, "w", encoding="utf-8").write(json.dumps(pr2, ensure_ascii=False))
        v2 = json.loads(bueno)
        for q in v2["variantes"]:
            q["zona"] = "cumple_regla_k"
        open(pv, "w", encoding="utf-8").write(json.dumps(v2, ensure_ascii=False))
        if ccj is not None:
            open(cj, "w", encoding="utf-8").write(json.dumps(ccj, ensure_ascii=False))
        try:
            ev = OBJ.evaluar(c, x)
            x["configuracion_v64"]["objetivo"].update(hipotesis_que_condicionan=ev["hipotesis_que_condicionan"], ambito=ev["ambito"], tratamiento=ev["tratamiento"],
                                                      origen_del_bloqueo=None, accion_sostenida_en_ambito=ev["accion_sostenida_en_ambito"])
            if completa:
                psi, malo, pond = pr2["precio_si"], pr2.get("precio_escenario_malo") or 0, pr2["ponderado"]
                x["celdas"]["C104"] = (f"Pendiente de decisión de cartera · conclusión del personaje: comprar al precio actual · zona cumple_regla_k · precio de Sí ≤ {psi:.2f} · "
                                       f"precio esc. MALO {malo:.2f} · ponderado {pond:.2f} · fundamento comprobación conjunta superada")
                return pp.coherencia_fase_c(x)
            return pp.coherencia_v64(x)
        finally:
            open(pj, "w", encoding="utf-8").write(pr_bueno)
            open(pv, "w", encoding="utf-8").write(bueno)
            if os.path.exists(cj):
                os.remove(cj)
    sobrevive = {"sobrevive": True, "escalera_bajo_combinacion": {"zona": "cumple_regla_k", "precio_si": 25.0, "ponderado": 26.0}, "combinacion": {"Palancas!C15": 0.1}}
    m1 = compra(ccj=sobrevive)
    paso("F", "compra favorable con una hipótesis experimental sin fundamento (λ) fuera de las listas heredadas de D10: no se puede aprobar",
         bool(m1) and "fuera de fundamento_material.hipotesis_sin_fundamento" in m1, str(m1)[:200])

    def con_lambda(x, en_comb=False, otra=None):
        x["fundamento_material"]["hipotesis_sin_fundamento"].append({"celda": lam, "hipotesis": "λ", "clase": "técnico", "porque_sin_fundamento": "sin desglose del capex",
                                                                     "alternativas_defendibles": {"hay_base": True, "rango": [1.10, 1.30], "evidencia": "extremos atados al capex y la amortización (sintético)"}})
        if en_comb:
            x["fundamento_material"]["comprobacion_conjunta"]["combinacion"][lam] = 1.30
        if otra:
            x["fundamento_material"]["comprobacion_conjunta"]["combinacion"][otra] = 0.5
    m2 = compra(lambda x: con_lambda(x), ccj=sobrevive)
    paso("F", "compra con λ en la lista D10 pero sin moverlo en la comprobación conjunta: no se puede aprobar", bool(m2) and "no mueve" in m2, str(m2)[:200])
    m3 = compra(lambda x: con_lambda(x, en_comb=True, otra="Configuración V6.4!B39"), ccj=sobrevive)
    paso("F", "una comprobación conjunta que mueve un parámetro inactivo (θ con la familia Λ) se rechaza", bool(m3) and "no están activos" in m3, str(m3)[:200])
    m4 = compra(lambda x: con_lambda(x, en_comb=True), ccj=None, completa=True)
    paso("F", "compra con la comprobación conjunta declarada pero ausente (sin comprobacion_conjunta.json): no se puede aprobar",
         bool(m4) and "sin comprobacion_conjunta.json" in m4, str(m4)[:200])
    sob_lam = dict(sobrevive, combinacion={"Palancas!C15": 0.1, lam: 1.30})
    m4b = compra(lambda x: con_lambda(x, en_comb=True), ccj=sob_lam, completa=True)
    paso("F", "control positivo: la compra con λ en D10, en la combinación y una comprobación conjunta superada pasa la coherencia", m4b is None, str(m4b)[:200])

    def estructura_sin_fundamento(x, alternativas=True):
        con_lambda(x, en_comb=True)
        par(x, "PM1.estructura").update(fundamento_suficiente=False, informacion_que_falta="destino del capex por tipo (sintético)")
        j_ = par(x, "PM1.estructura").get("juicio_objetivo")
        if isinstance(j_, dict) and j_.get("base") == "juicio_economico" and j_.get("material") is False and not j_.get("comparado_con"):
            # (4.14, V6) sin fundamento suficiente, «no material» por juicio exige declarar con qué se compara (lo prueba test_juicio_objetivo_414.py)
            j_["comparado_con"] = {"referencia": "otro_declarado", "valor_eur": 1.0, "fuente": "(sintético) comparación declarada para la prueba de cobertura de la estructura"}
        x["fundamento_material"]["hipotesis_sin_fundamento"].append({"celda": CE.celda_principal("PM1.estructura", conf), "hipotesis": "estructura S", "clase": "técnico",
                                                                     "porque_sin_fundamento": "sin hechos que elijan la estructura",
                                                                     "alternativas_defendibles": {"hay_base": True, "rango": ["H", "SR1", "SR2", "SRF", "sin requisito"], "evidencia": "estructuras compatibles calculadas (sintético)"}})
        if alternativas:
            x["fundamento_material"]["comprobacion_conjunta"]["alternativas_no_numericas"] = ["PM1.estructura"]
        revisar(x)
    m5 = compra(lambda x: estructura_sin_fundamento(x, alternativas=False), ccj=sob_lam)
    paso("F", "compra con una estructura (no numérica) sin fundamento suficiente y sin evaluar sus alternativas: no se puede aprobar",
         bool(m5) and "no evalúa sus alternativas" in m5, str(m5)[:200])
    falla_alt = dict(sob_lam, por_alternativa=[{"clave": "PM1.estructura", "alternativa": "H", "definida": True, "zona": "caro", "sobrevive": False}])
    m6 = compra(lambda x: estructura_sin_fundamento(x), ccj=falla_alt)
    paso("F", "compra con una alternativa de estructura que no sobrevive en la comprobación conjunta: no se puede aprobar", bool(m6) and "no están todas definidas y superadas" in m6, str(m6)[:200])
    ok_alt = dict(sob_lam, por_alternativa=[{"clave": "PM1.estructura", "alternativa": a, "definida": True, "zona": "cumple_regla_k", "sobrevive": True, "precio_si": 25.0, "ponderado": 26.0}
                                            for a in ("sin requisito adicional", "H", "SR1", "SR2", "SRF")])
    m6b = compra(lambda x: estructura_sin_fundamento(x), ccj=ok_alt)
    paso("F", "control positivo: con todas las alternativas de estructura definidas y superadas, la regla de cobertura no bloquea la compra", m6b is None, str(m6b)[:200])
    # comprobacion_conjunta.py real: rechaza un parámetro inactivo y recalcula cada alternativa de estructura definida
    libro = os.path.join(c, "EmpresaXO_v63_evaluada.xlsx")
    fcr = copy.deepcopy(fcb)
    fcr["fundamento_material"]["comprobacion_conjunta"] = {"procede": True, "combinacion": {lam: 1.30, "Configuración V6.4!B39": 0.5}, "coherencia_economica": "sintética", "sobrevive": None}
    fcp = os.path.join(c, "fase_c.json")
    fc_txt = open(fcp, encoding="utf-8").read()
    open(fcp, "w", encoding="utf-8").write(json.dumps(fcr, ensure_ascii=False))
    rc_i, out_i = run([PY, os.path.join(PV, "scripts", "comprobacion_conjunta.py"), c, libro, "--config", CFG64])
    fcr["fundamento_material"]["comprobacion_conjunta"] = {"procede": True, "combinacion": {lam: 1.30}, "coherencia_economica": "sintética", "sobrevive": None,
                                                           "alternativas_no_numericas": ["PM1.estructura"]}
    open(fcp, "w", encoding="utf-8").write(json.dumps(fcr, ensure_ascii=False))
    rc_a, out_a = run([PY, os.path.join(PV, "scripts", "comprobacion_conjunta.py"), c, libro, "--config", CFG64], timeout=1800)
    ccj_a = json.load(open(cj, encoding="utf-8")) if os.path.exists(cj) else {}
    open(fcp, "w", encoding="utf-8").write(fc_txt)
    if os.path.exists(cj):
        os.remove(cj)
    shutil.rmtree(os.path.join(c, "comprobacion_conjunta"), ignore_errors=True)
    alts = [a for a in ccj_a.get("por_alternativa") or [] if a.get("clave") == "PM1.estructura"]
    paso("F", "comprobacion_conjunta.py: código 3 si la combinación mueve un parámetro inactivo, y recálculo explícito de cada alternativa de estructura definida (una a una)",
         rc_i == 3 and "no están activos" in out_i and rc_a == 0 and len(alts) == 5 and all(a.get("definida") and a.get("zona") for a in alts)
         and ccj_a.get("sobrevive") == (ccj_a.get("sobrevive_combinacion_activa") and all(a["sobrevive"] for a in alts)),
         f"rc {rc_i}/{rc_a} · {[(a.get('alternativa'), a.get('zona')) for a in alts]} · {out_a.strip().splitlines()[-1][:160] if out_a.strip() else ''}")
    paso("F", "las pruebas de contradicción no dejan cambiado el material del expediente", open(fcp, encoding="utf-8").read() == fc_txt and open(pj, encoding="utf-8").read() == pr_bueno
         and open(pv, encoding="utf-8").read() == bueno and pp.coherencia_fase_c(copy.deepcopy(fcb)) is None)
    # compatibilidad: V6.3 y V6.4 heredado no cambian de ficha ni de columnas
    paso("F", "el protocolo no se aplica a la V6.3 ni al modo heredado de la V6.4 (sin campo objetivo; rige el Anexo B §B.6.7)",
         not OBJ.aplica(os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_10_1", "Vidrala"))
         and not OBJ.aplica(os.path.join(ENS, "control_heredado", "Vidrala")))
    d63 = os.path.join(base, "resumen63")
    os.makedirs(d63, exist_ok=True)
    json.dump({"empresa": "Empresa X (inventada)", "estado_analisis": "pendiente_de_datos"}, open(os.path.join(d63, "ficha.json"), "w", encoding="utf-8"))
    rc63, _ = run([PY, os.path.join(PV, "scripts", "resumen.py"), d63, os.path.join(base, "resumen_v2.csv")])
    cab63 = open(os.path.join(base, "resumen_v2.csv"), encoding="utf-8").readline().strip().split(",")
    vieja = os.path.join(base, "v64_vieja", "resumen_v2_v64_experimental.csv")
    os.makedirs(os.path.dirname(vieja), exist_ok=True)
    with open(vieja, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=RS.COLS)
        w.writeheader()
        w.writerow({"empresa": "Otra (4.11)", "estado_analisis": "concluido"})
    d64 = os.path.join(base, "v64_vieja", "EmpresaXO")
    # (4.13 §4) la ficha de partida es la del bloqueo (pendiente_de_datos, acción nula, objetivo bloqueado): hasta la 4.12 se usaba la del
    # condicionado con el estado cambiado a no_entregable, una ficha contradictoria (objetivo emitido en un análisis no concluido) que
    # resumen.py ya no publica
    shutil.copytree(exp["bloqueo"][0], d64, ignore=shutil.ignore_patterns("*.xlsx", "recalc", "variantes_v64", "prompts_generados", "historial_cierres"))
    fj = json.load(open(os.path.join(d64, "ficha.json"), encoding="utf-8"))
    fj.pop("cierre", None)  # sin cierre: la columna se prueba sin pasar por la vigencia (no es una fila aprobada)
    json.dump(fj, open(os.path.join(d64, "ficha.json"), "w", encoding="utf-8"), ensure_ascii=False)
    for f_ in ("cierre_vigente.json", "publicaciones_resumen.json", ".publicaciones_resumen.respaldo.json"):
        if os.path.exists(os.path.join(d64, f_)):
            os.remove(os.path.join(d64, f_))
    st64 = json.load(open(os.path.join(d64, "estado_pipeline.json"), encoding="utf-8"))
    st64["auditoria"] = None
    json.dump(st64, open(os.path.join(d64, "estado_pipeline.json"), "w", encoding="utf-8"), ensure_ascii=False)
    rc64, out64 = run([PY, os.path.join(PV, "scripts", "resumen.py"), d64, vieja], env=dict(os.environ, MUNGER_CONFIG=CFG64))
    filas = list(csv.DictReader(open(vieja, encoding="utf-8", newline="")))
    cab64 = open(vieja, encoding="utf-8").readline().strip().split(",")
    paso("F", "columnas: el resumen V6.3 no cambia; un resumen V6.4 de la 4.11 migra su cabecera (columnas nuevas al final) y conserva sus filas",
         rc63 == 0 and cab63 == RS.COLS and rc64 == 0 and cab64 == RS.COLS + RS.COLS_V64 and len(filas) == 2 and filas[0]["empresa"] == "Otra (4.11)" and filas[0]["protocolo_objetivo"] == ""
         and filas[1]["estado_del_objetivo"] == "bloqueado", f"rc {rc63}/{rc64} · {out64.strip()[-160:]}")


def grupo_f_413():
    """(4.13 §4) La acción final manda: el antecedente provisional no exime a la salida final de sus reglas."""
    import objetivo_v64 as OBJ
    import pipeline as P
    import config_v2
    base = os.path.join(TMP, "objetivo_413")
    shutil.rmtree(base, ignore_errors=True)
    # unidad: acción evaluada y contradicciones de la salida
    caro = {"zona": "caro", "precio_si": 10.0}
    fc_t = {"conclusion_provisional": "descartar", "decision": {"accion": "esperar", "precio_objetivo": 10.0}, "limite_del_modelo": {"aplica": False}}
    casos = {"la acción final manda sobre la provisional": OBJ.accion_evaluada(fc_t) == "esperar",
             "sin acción final, cuenta la provisional": OBJ.accion_evaluada({"conclusion_provisional": "esperar", "decision": {"accion": None}}) == "esperar",
             "descartar provisional + esperar final con objetivo y condicionantes, sin protocolo: sin protocolo (no se entrega)": OBJ.tratamiento(fc_t, caro, ["x"], None, True, False)[0] == "objetivo_sin_protocolo",
             "con bloqueo: bloqueado (no «sin objetivo»)": OBJ.tratamiento(fc_t, caro, ["x"], "bloqueo_del_objetivo", True, False)[0] == "objetivo_bloqueado",
             "transición legítima comprar → esperar con objetivo condicionado y acción sostenida": OBJ.tratamiento({**fc_t, "conclusion_provisional": "comprar"}, caro, ["x"], "objetivo_condicionado", True, False)[0] == "objetivo_condicionado"}
    bl = lambda eo, em, prov=False: {"estado_del_objetivo": eo, "precio_objetivo_emitido": em, "provisional": prov, "tratamiento": "t"}  # noqa: E731
    cs = OBJ.contradicciones_salida
    casos.update({
        "objetivo no emitido y decision.precio_objetivo conservado: contradicción": bool(cs("concluido", {"accion": "esperar", "precio_objetivo": 56.02}, bl("no_aplica", None))),
        "bloqueado con acción esperar: contradicción": bool(cs("concluido", {"accion": "esperar", "precio_objetivo": None}, bl("bloqueado", None))),
        "bloqueado con acción nula y pendiente_de_datos: coherente": not cs("pendiente_de_datos", {"accion": None, "precio_objetivo": None}, bl("bloqueado", None)),
        "compra sin objetivo de espera: coherente": not cs("concluido", {"accion": "comprar", "precio_objetivo": None}, bl("no_aplica", None)),
        "compra con precio objetivo: contradicción": bool(cs("concluido", {"accion": "comprar", "precio_objetivo": 10.0}, None)),
        "emitido condicionado igual con el redondeo declarado (56,024 ≈ 56,02): coherente": not cs("concluido", {"accion": "esperar", "precio_objetivo": 56.02}, bl("emitido_condicionado", 56.024, True)),
        "emitido 56,03 frente a 56,02: contradicción (antes pasaba con la tolerancia del 0,5 %)": bool(cs("concluido", {"accion": "esperar", "precio_objetivo": 56.02}, bl("emitido_condicionado", 56.03, True))),
        "sin objetivo según el tratamiento y precio objetivo en la decisión: contradicción": bool(cs("concluido", {"accion": "esperar", "precio_objetivo": 9.0}, None, {"tratamiento": "sin_objetivo", "estado_esperado": None, "motivo_mecanico": "x"}))})
    malos = [k for k, v in casos.items() if not v]
    paso("F", "(4.13 §4) la acción final manda en el tratamiento; contradicciones entre acción, estado, protocolo y los dos objetivos; transiciones legítimas, compras sin objetivo, bloqueos con acción nula y redondeo declarado",
         not malos, "; ".join(malos))
    # contraejemplo externo sobre COPIAS de la fase C real de cierre_condicionado/Vidrala (4.12): ni la coherencia ni la ficha lo aceptan
    E412 = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_12")
    cfg = config_v2.cargar(CFG64)
    malos, det = [], []
    for nombre, prot, concl in (("real", "igual", None), ("sin_protocolo_descartar", None, "descartar"), ("sin_protocolo_comprar", None, "comprar"),
                                ("bloqueo_descartar", "bloqueo_del_objetivo", "descartar"), ("bloqueo_comprar", "bloqueo_del_objetivo", "comprar")):
        d = os.path.join(base, "contraejemplo", nombre, "Vidrala")
        shutil.copytree(os.path.join(E412, "cierre_condicionado", "Vidrala"), d, ignore=shutil.ignore_patterns("variantes_v64", "historial_cierres", ".lo_perfil", "prompts_generados"))
        fc = json.load(open(os.path.join(d, "fase_c.json"), encoding="utf-8"))
        if prot != "igual":
            conf = json.load(open(os.path.join(d, "configuracion_economica.json"), encoding="utf-8"))
            conf.pop("protocolo_objetivo", None)
            if prot:
                conf["protocolo_objetivo"] = prot
            json.dump(conf, open(os.path.join(d, "configuracion_economica.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            fc["conclusion_provisional"] = concl
            # el bloque se actualiza con el propio evaluador, como en la prueba externa; la decisión final sigue concluido/esperar/56,02
            ev = OBJ.evaluar(d, fc)
            fc["configuracion_v64"]["objetivo"].update(protocolo=ev["protocolo"], hipotesis_que_condicionan=ev["hipotesis_que_condicionan"], ambito=ev["ambito"],
                                                     accion_sostenida_en_ambito=ev["accion_sostenida_en_ambito"], tratamiento=ev["tratamiento"], origen_del_bloqueo=ev["origen_del_bloqueo"])
            json.dump(fc, open(os.path.join(d, "fase_c.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        p = P.Pipeline(d, cfg, None)
        coh = p.coherencia_v64(fc)
        nsp = p.objetivo_sin_protocolo(fc)
        entregable_cerrado = coh is None and nsp is None
        r = subprocess.run([PY, "-B", os.path.join(PV, "scripts", "ficha.py"), d, "--provisional", "--config", CFG64], capture_output=True, text=True)
        det.append(f"{nombre}: coherencia {'acepta' if coh is None else 'rechaza'} · sin protocolo {'no' if nsp is None else 'sí'} · ficha provisional rc {r.returncode}")
        if nombre == "real":
            if not (entregable_cerrado and r.returncode == 0):
                malos.append(det[-1])
        elif entregable_cerrado:
            malos.append(det[-1] + " (llegaría a un cierre con el objetivo 56,02 y un bloque que no lo emite)")
        elif prot == "bloqueo_del_objetivo" and r.returncode != 3:
            malos.append(det[-1] + " (la ficha provisional no puede ser material aparentemente listo para la auditoría)")
    paso("F", "(4.13 §4) contraejemplo externo sobre copias de la fase C real de Vidrala (sin protocolo o con bloqueo, provisional descartar/comprar, final esperar 56,02): ninguno llega a un cierre ni a una ficha provisional; la fase C real sigue aceptada",
         not malos, "; ".join(malos)[:600] or " · ".join(det))
    # extremo a extremo con agentes SINTÉTICOS (no con casos financieros reales): la contradicción no cierra ni genera material de auditoría
    def contradecir(c, turno, usado):
        if turno != 2:
            return
        fc = json.load(open(os.path.join(c, "fase_c.json"), encoding="utf-8"))
        pr = json.load(open(os.path.join(c, "precio.json"), encoding="utf-8"))
        fc["conclusion_provisional"] = "descartar"
        fc["estado_analisis"], fc["cubo_final"] = "concluido", "Vigilar"
        fc["decision"] = dict(fc.get("decision") or {}, accion="esperar", precio_objetivo=pr.get("precio_si"))
        fc["configuracion_v64"]["objetivo"].update(tratamiento="sin_objetivo", origen_del_bloqueo=None)
        json.dump(fc, open(os.path.join(c, "fase_c.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        usado["contradicciones"] = usado.get("contradicciones", 0) + 1
    c = os.path.join(base, "e2e_bloqueo_contradictorio", "EmpresaXO")
    preparar_sintetico(c, conf_sintetica(protocolo="bloqueo_del_objetivo"))
    rc, out, usado = correr(c, tras_fase_c=contradecir)
    st = json.load(open(os.path.join(c, "estado_pipeline.json"), encoding="utf-8"))
    sin_material = not os.path.exists(os.path.join(c, "solicitud_auditoria.json")) and not os.path.exists(os.path.join(c, "material_auditoria.json"))
    paso("F", "(4.13 §4) extremo a extremo (sintético): una fase C con bloqueo que conserva esperar y el objetivo con el bloque «sin objetivo» no llega a un cierre ni a material de auditoría",
         st.get("estado_analisis") != "concluido" and st.get("auditoria") != "APROBADO" and not os.path.exists(os.path.join(c, "cierre_vigente.json")) and sin_material
         and usado.get("contradicciones", 0) >= 1,
         f"rc {rc} · estado {st.get('estado_analisis')} · auditoría {st.get('auditoria')} · contradicciones escritas {usado.get('contradicciones')} · material {'no' if sin_material else 'SÍ'} · {out.strip().splitlines()[-1][:150] if out.strip() else ''}")
    def contradecir_una_vez(c, turno, usado):
        if not usado.get("contradicciones"):
            contradecir(c, turno, usado)
    c = os.path.join(base, "e2e_bloqueo_corregido", "EmpresaXO")
    preparar_sintetico(c, conf_sintetica(protocolo="bloqueo_del_objetivo"))
    rc, out, usado = correr(c, tras_fase_c=contradecir_una_vez)
    st = json.load(open(os.path.join(c, "estado_pipeline.json"), encoding="utf-8"))
    f = json.load(open(os.path.join(c, "ficha.json"), encoding="utf-8")) if os.path.exists(os.path.join(c, "ficha.json")) else {}
    paso("F", "(4.13 §4) la misma contradicción corregida en la vuelta siguiente: el bloqueo legítimo se cierra (pendiente_de_datos · acción nula · objetivo bloqueado)",
         usado.get("contradicciones") == 1 and st.get("estado_analisis") == "pendiente_de_datos" and (f.get("decision") or {}).get("accion") is None
         and (f.get("objetivo") or {}).get("estado_del_objetivo") == "bloqueado",
         f"rc {rc} · estado {st.get('estado_analisis')} · {(f.get('objetivo') or {}).get('estado_del_objetivo')} · {out.strip().splitlines()[-1][:150] if out.strip() else ''}")



# ======================================================================================= G · coherencia, trazabilidad y límites (4.12 §5)

def grupo_f_revision_413():
    """(4.13, revisión interna R3 y R4) Terminación en no_entregable después de una fase C con objetivo; contrato de cobertura de la
    materialidad para el objetivo (null, base, «false calculada» con un contraste que mueve el precio de Sí)."""
    import objetivo_v64 as OBJ
    import pipeline as P
    import config_v2
    E413 = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_13")
    base = os.path.join(TMP, "revision_413")
    shutil.rmtree(base, ignore_errors=True)
    resultados = {}
    for nombre in ("vidrala_condicionado", "vidrala_bloqueo"):
        orig = os.path.join(E413, nombre, "Vidrala")
        c = os.path.join(base, nombre, "Vidrala")
        shutil.copytree(orig, c, ignore=shutil.ignore_patterns(".lo_perfil", "variantes_v64", "recalc", "prompts_generados", "historial_cierres", "__pycache__"))
        fc = json.load(open(os.path.join(c, "fase_c.json"), encoding="utf-8"))
        pr = json.load(open(os.path.join(c, "precio.json"), encoding="utf-8"))
        bl = OBJ.bloque_ficha(c, fc, pr, "no_entregable", {"accion": None, "precio_objetivo": None})
        cs = OBJ.contradicciones_salida("no_entregable", {"accion": None, "precio_objetivo": None}, bl)
        rc, out = run([PY, "-B", os.path.join(PV, "scripts", "ficha.py"), c, "--estado", "no_entregable", "--provisional"], env=dict(os.environ, MUNGER_CONFIG=CFG64))
        resultados[nombre] = (bl.get("estado_del_objetivo"), bl.get("precio_objetivo_emitido"), bl.get("provisional"), cs, rc)
    paso("F", "(4.13, R3) terminación en no_entregable después de una fase C con objetivo condicionado o bloqueado: el bloque dice «no emitido por el estado final», "
              "sin contradicción, y ficha.py escribe la ficha",
         all(v[0] == "no_emitido_estado_final" and v[1] is None and not v[2] and not v[3] and v[4] == 0 for v in resultados.values()), resultados)
    # R4 · contrato del objetivo sobre el expediente sintético condicionado de grupo_f (si existe) o uno nuevo
    c = os.path.join(base, "r4", "EmpresaXR")
    preparar_sintetico(c, conf_sintetica())
    rc, out, _ = correr(c)
    pp = P.Pipeline(c, config_v2.cargar(CFG64))
    fcb = json.load(open(os.path.join(c, "fase_c.json"), encoding="utf-8"))
    par = lambda x, k: next(q for q in x["configuracion_v64"]["parametros"] if q["clave"] == k)  # noqa: E731
    c414 = pp.st.get("contrato_juicio_objetivo") == getattr(OBJ, "FORMATO_JUICIO_OBJETIVO", None)
    paso("F", "(4.14) control positivo: el pipeline fija el contrato 4.14 y la fase C sintética con su juicio_objetivo es coherente",
         rc == 0 and c414 and pp.coherencia_fase_c(copy.deepcopy(fcb)) is None, f"rc {rc} · contrato {pp.st.get('contrato_juicio_objetivo')} · {pp.coherencia_fase_c(copy.deepcopy(fcb))}")
    # las reglas 4.13 del objetivo (_objetivo_413) siguen rigiendo las fases C cerradas con la 4.13 (los controles congelados): se prueban
    # sobre la misma fase C sin el bloque 4.14 y sin el contrato en el estado; el contrato 4.14 tiene su batería (test_juicio_objetivo_414.py)
    pp.st.pop("contrato_juicio_objetivo", None)
    for q in fcb["configuracion_v64"]["parametros"]:
        q.pop("juicio_objetivo", None)
    paso("F", "(4.13, R4) control positivo: la fase C sintética con la base de la materialidad para el objetivo es coherente", rc == 0 and pp.coherencia_fase_c(copy.deepcopy(fcb)) is None,
         f"rc {rc} · {pp.coherencia_fase_c(copy.deepcopy(fcb))}")

    def m(cambio):
        x = copy.deepcopy(fcb)
        cambio(x)
        return pp.coherencia_fase_c(x) or ""
    m1 = m(lambda x: par(x, "PM1.parametro").update(material_para_objetivo=False, material_para_conclusion=False, base_de_la_materialidad_objetivo="calculada"))
    m2 = m(lambda x: par(x, "PM1.parametro").update(material_para_objetivo=None, material_para_conclusion=par(x, "PM1.parametro").get("material_para_accion") is True))
    m3 = m(lambda x: par(x, "PM1.parametro").pop("base_de_la_materialidad_objetivo"))
    paso("F", "(4.13, R4) «no material para el objetivo» calculada con un contraste que mueve el precio de Sí: se rechaza (es un juicio); null sin «no_determinada» y la "
              "base ausente también", "mueven el precio de Sí al redondeo declarado" in m1 and "si y solo si" in m2 and "base_de_la_materialidad_objetivo" in m3, f"{m1[:120]} | {m2[:80]} | {m3[:80]}")
    x = copy.deepcopy(fcb)
    par(x, "PM1.parametro").update(material_para_objetivo=None, base_de_la_materialidad_objetivo="no_determinada", material_para_conclusion=bool(par(x, "PM1.parametro").get("material_para_accion")))
    conf = json.load(open(os.path.join(c, "configuracion_economica.json"), encoding="utf-8"))
    paso("F", "(4.13, R4) un parámetro sin fundamento suficiente con la materialidad para el objetivo no determinada condiciona el objetivo (no se convierte en «no material»)",
         "PM1.parametro" in OBJ.condicionantes(x, conf), OBJ.condicionantes(x, conf))

def grupo_g():
    import entradas_economicas as EE
    import dominios_v64 as DOM
    import objetivo_v64 as OBJ
    import pipeline as P
    import config_v2
    from v63_xml import LibroV63
    base = os.path.join(TMP, "coherencia")
    shutil.rmtree(base, ignore_errors=True)
    c = os.path.join(base, "exp", "EmpresaXG")
    preparar_sintetico(c, conf_sintetica())
    rc, out, _ = correr(c)
    st = json.load(open(os.path.join(c, "estado_pipeline.json"), encoding="utf-8"))
    paso("G", "expediente de partida: pasada V6.4 experimental con agentes simulados, concluido · APROBADO", rc == 0 and st.get("estado_analisis") == "concluido" and st.get("auditoria") == "APROBADO",
         f"rc {rc} · {st.get('estado_analisis')}")
    libro = os.path.join(c, "EmpresaXG_v63_evaluada.xlsx")
    # instantánea: un cambio editorial no cambia la huella; uno económico sí, y se nombra la celda
    tmpd = os.path.join(base, "libros")
    os.makedirs(tmpd, exist_ok=True)
    i0 = EE.instantanea(libro)
    ed, ec = os.path.join(tmpd, "editorial.xlsx"), os.path.join(tmpd, "economico.xlsx")
    lb = LibroV63(libro)
    lb.escribir_celdas({"Análisis!C104": "texto editorial distinto (prueba)", "Análisis!B101": "tesis reescrita (prueba)"}, {"Análisis": {"C104", "B101"}})
    lb.guardar(ed)
    lb = LibroV63(libro)
    lb.escribir_celdas({"Palancas!C15": 0.123}, {"Palancas": {"C15"}})
    lb.guardar(ec)
    ie, ic = EE.instantanea(ed), EE.instantanea(ec)
    paso("G", "instantánea de las entradas económicas: un cambio editorial (C104, B101) no cambia la huella; uno económico (Palancas!C15) sí y se nombra",
         ie["huella"] == i0["huella"] and ic["huella"] != i0["huella"] and EE.diferencias(i0, ic) == ["Palancas!C15"] and i0["n"] >= 200, f"{i0['n']} celdas · {EE.diferencias(i0, ic)}")
    pp = P.Pipeline(c, config_v2.cargar(CFG64))
    ok0 = pp.variantes_corresponden()
    bueno = open(libro, "rb").read()
    shutil.copy(ed, libro)
    m_ed = pp.variantes_corresponden()
    shutil.copy(ec, libro)
    m_ec = pp.variantes_corresponden()
    open(libro, "wb").write(bueno)
    paso("G", "variantes y libro final: el cambio editorial no obliga a repetir las valoraciones; el económico sí, con la celda nombrada",
         ok0 is None and m_ed is None and bool(m_ec) and "entradas económicas" in m_ec and "Palancas!C15" in m_ec, str(m_ec)[:200])
    pv = os.path.join(c, "configuracion_v64_variantes.json")
    vt = open(pv, encoding="utf-8").read()
    v = json.loads(vt)
    v["vector_escenarios_activa"]["V"][0] += 0.5
    open(pv, "w", encoding="utf-8").write(json.dumps(v, ensure_ascii=False))
    m_v = pp.variantes_corresponden()
    v = json.loads(vt)
    v.pop("formato")
    open(pv, "w", encoding="utf-8").write(json.dumps(v, ensure_ascii=False))
    m_f = pp.variantes_corresponden()
    open(pv, "w", encoding="utf-8").write(vt)
    pc = os.path.join(c, "configuracion_economica.json")
    ct = open(pc, encoding="utf-8").read()
    cf = json.loads(ct)
    cf["trazabilidad"]["PM1.parametro"]["justificacion"] = "texto de trazabilidad reescrito (prueba editorial)"
    open(pc, "w", encoding="utf-8").write(json.dumps(cf, ensure_ascii=False, indent=1))
    m_t = pp.variantes_corresponden()
    cf = json.loads(ct)
    cf["PM1"]["lambda"] = 1.2
    open(pc, "w", encoding="utf-8").write(json.dumps(cf, ensure_ascii=False, indent=1))
    m_l = pp.variantes_corresponden()
    open(pc, "w", encoding="utf-8").write(ct)
    paso("G", "correspondencia: el vector de escenarios de la activa y la configuración económica se contrastan (no bastan ponderado y precio de Sí); el formato anterior se rechaza; la trazabilidad no cuenta",
         bool(m_v) and "vector de escenarios" in m_v and bool(m_f) and "formato anterior" in m_f and m_t is None and bool(m_l) and "otra configuración económica" in m_l,
         f"{str(m_v)[:80]} · {str(m_l)[:80]}")
    # reutilización de las variantes en el paso 10 con un cambio editorial (sin recálculo)
    shutil.copy(ed, libro)
    antes = open(pv, "rb").read()
    r_ed = pp.variantes_v64(libro)
    reus = open(pv, "rb").read() == antes
    open(libro, "wb").write(bueno)
    paso("G", "paso 10: con un libro que solo cambió en lo editorial, las variantes se reutilizan (mismas entradas económicas, misma configuración y k)", r_ed is None and reus)
    # (4.12, revisión interna R1) la fila 13 de la Historia (adquisiciones netas) entra en las bases de P-M1: está en la instantánea V6.4
    # (relación «4.12+H13»); una instantánea guardada con la relación anterior se compara con la misma relación y su fila 13 con el libro
    # de la variante «activa»; sin ese libro, la fila 13 no se acredita
    act = os.path.join(c, "variantes_v64", "recalc", "activa.xlsx")
    vieja = {k: v for k, v in EE.instantanea(libro, version="4.12").items() if k != "version"}
    act_mod = os.path.join(tmpd, "activa_h13.xlsx")
    lb = LibroV63(act)
    lb.escribir_celdas({"Historia!J13": 7.5}, {"Historia": {"J13"}})
    lb.guardar(act_mod)
    ev_mod = os.path.join(tmpd, "evaluado_h13.xlsx")
    lb = LibroV63(libro)
    lb.escribir_celdas({"Historia!J13": 7.5}, {"Historia": {"J13"}})
    lb.guardar(ev_mod)
    d_ok, d_mod, d_sin = EE.comparar(vieja, libro, act)[0], EE.comparar(vieja, libro, act_mod)[0], EE.comparar(vieja, libro, None)[0]
    d_nueva = EE.diferencias(i0, EE.instantanea(ev_mod))
    paso("G", "la fila 13 de la Historia (bases de P-M1) entra en la instantánea V6.4; con una instantánea de la relación anterior se compara con el libro de la variante activa, y sin él no se acredita",
         i0.get("version") == EE.RELACION_ACTUAL and "Historia!J13" in i0["celdas"] and "Historia!J13" not in vieja["celdas"] and d_ok == [] and d_mod == ["Historia!J13"]
         and bool(d_sin) and "sin acreditar" in d_sin[0] and d_nueva == ["Historia!J13"], f"{i0.get('version')} · {d_mod} · {d_sin[:1]} · {d_nueva}")
    # avisos de dominio del piloto de la 4.11 (solo lectura): los valores declarados en su informe
    av = {a["id"]: a for a in DOM.avisos(os.path.join(PIL411, "Vidrala", "variantes_v64", "recalc", "activa.xlsx"),
                                         json.load(open(os.path.join(PIL411, "Vidrala", "variantes_v64", "activa.resultados.json"), encoding="utf-8")))}
    t_r1 = (av["terminal_r1_sin_maximo_conservado"]["valores"]["escenarios"] or [{}])[0]
    paso("G", "avisos de dominio con valores y motivo, sin umbral: en el piloto 4.11, terminal R1 sin el máximo (MALO, 16,39 M€ con ventas bajo el máximo), S2C inerte en el MALO y f = 1,165 con λ* ≈ 2,06",
         av["terminal_r1_sin_maximo_conservado"]["activo"] is True and t_r1.get("escenario") == "MALO" and abs(t_r1.get("inversion_fija_terminal", 0) - 16.39) < 0.01
         and av["s2c_inerte"]["activo"] is True and av["inversion_fija_para_crecer_negativa"]["activo"] is False and av["factor_de_reestimacion"]["activo"] is None
         and abs(av["factor_de_reestimacion"]["valores"]["lambda_en_que_f_deja_de_estar_definida"] - 2.06) < 0.01, json.dumps(t_r1, default=str)[:160])
    # (4.12) los valores de los avisos van al informe sin la sintaxis JSON: verificar_todo.sh pasa juntos informe.md e informe_provisional.md
    # a verify_quotes_v2 y, con comillas rectas, la última de un archivo se emparejaba con la primera del siguiente; la repetición desde el
    # paso 12 de un expediente cerrado con avisos activos fallaba por los informes anteriores (visto en el cierre). Se pasa el archivo dos veces
    import informe as INF
    corpus = [run([PY, os.path.join(PV, "scripts", "config_v2.py"), k, CFG64])[1].strip() for k in ("kit_v1.corpus_munger", "corpus.damodaran")]
    rq = {}
    for modo, rend in (("plano", INF.plano), ("json", lambda v: json.dumps(v, ensure_ascii=False, default=str))):
        mdq = os.path.join(tmpd, f"avisos_citas_{modo}.md")
        # texto del informe alrededor (verify_quotes_v2 solo comprueba un tramo con al menos dos marcadores ingleses: «the», «of», «a»…)
        prosa = "\n".join(f"Línea {k} del informe: la caja de cada año se lee en la Historia; véase the cost of capital, a modo de guía." for k in range(6))
        open(mdq, "w", encoding="utf-8").write(prosa + "\n" + "\n".join(f"- Aviso de dominio «{i}»: valores {rend(a.get('valores'))[:260]} · fase C: no material — "
                                                                       "lo digo en el diagnóstico y en las incoherencias" for i, a in av.items()) + "\n" + prosa + "\n")
        rq[modo] = run([PY, os.path.join(PV, "scripts", "verify_quotes_v2.py"), "--corpus", corpus[0], "--corpus", corpus[1], "--paginas-estrictas", mdq, mdq])
    paso("G", "los valores de los avisos de dominio se escriben en el informe sin comillas rectas: la verificación de citas pasa con ellos (y con la forma JSON anterior fallaba)",
         rq["plano"][0] == 0 and "NO ENCONTRADOS (0)" in rq["plano"][1] and rq["json"][0] != 0 and "NO ENCONTRADOS (0)" not in rq["json"][1] and '"' not in INF.plano(av["terminal_r1_sin_maximo_conservado"]["valores"]),
         f"plano {rq['plano'][0]} · json {rq['json'][0]} · {rq['plano'][1][-120:]}")
    # la fase C tiene que evaluar cada aviso activo; uno material condiciona el objetivo y no admite comprar
    fcb = json.load(open(os.path.join(c, "fase_c.json"), encoding="utf-8"))
    v = json.loads(vt)
    v["avisos_de_dominio"] = [dict(a, activo=True) if a["id"] == "terminal_r1_sin_maximo_conservado" else a for a in v["avisos_de_dominio"]]
    open(pv, "w", encoding="utf-8").write(json.dumps(v, ensure_ascii=False))
    try:
        m_sin = pp.coherencia_v64(copy.deepcopy(fcb))
        x = copy.deepcopy(fcb)
        x["configuracion_v64"]["avisos_de_dominio"].append({"id": "terminal_r1_sin_maximo_conservado", "material_para_conclusion": True, "consecuencia": "condiciona el objetivo (prueba)"})
        m_mat = pp.coherencia_v64(copy.deepcopy(x))
        ev = OBJ.evaluar(c, x)
        x["configuracion_v64"]["objetivo"]["hipotesis_que_condicionan"] = ev["hipotesis_que_condicionan"]
        m_ok = pp.coherencia_v64(copy.deepcopy(x))
        bl = OBJ.bloque_ficha(c, x, json.load(open(os.path.join(c, "precio.json"), encoding="utf-8")), "concluido", x["decision"])
        y = copy.deepcopy(x)
        y.update(estado_analisis="concluido", conclusion_provisional="comprar")
        y["decision"]["accion"] = "comprar"
        m_cmp = pp.coherencia_v64(y)
    finally:
        open(pv, "w", encoding="utf-8").write(vt)
    paso("G", "un aviso activo sin evaluar en la fase C se rechaza; si es material, condiciona el objetivo («limite:…», visible en la ficha) y no admite comprar",
         bool(m_sin) and "falta evaluar el aviso" in m_sin and bool(m_mat) and "hipotesis_que_condicionan" in m_mat and m_ok is None
         and "limite:terminal_r1_sin_maximo_conservado" in [h["hipotesis"] for h in bl["hipotesis_que_lo_condicionan"]]
         and "terminal_r1_sin_maximo_conservado" in bl["materialidad"]["limites_del_modelo_materiales"] and bool(m_cmp) and "límite del modelo material" in m_cmp,
         f"{str(m_sin)[:70]} · {str(m_cmp)[:70]}")
    # cadena de trazabilidad en el material auditado, con identificadores por clase y la cadena completa
    ct_j = json.load(open(os.path.join(c, "cadena_trazabilidad.json"), encoding="utf-8"))
    mat = json.load(open(os.path.join(c, "material_auditoria.json"), encoding="utf-8"))
    pref = {e["id"].split("-", 1)[0] for e in ct_j["entradas"]}
    campos = all({"fuente", "dato_extraido_y_periodo", "transformacion_o_supuesto", "entrada_del_modelo", "magnitud", "calculo"} <= set(e) for e in ct_j["entradas"])
    paso("G", "cadena de trazabilidad (fuente → dato → transformación → entrada → cálculo → resultado → conclusión) en el material auditado, con identificadores distintos por clase",
         "cadena_trazabilidad.json" in mat["archivos"] and pref <= {"D", "C", "V", "H"} and {"D", "H"} <= pref and campos and ct_j["resultado"].get("precio_si") is not None
         and ct_j["conclusion"].get("objetivo") == "objetivo_condicionado" and os.path.exists(os.path.join(c, "verificacion_trazabilidad.txt")), f"clases {sorted(pref)} · {len(ct_j['entradas'])} entradas")
    cp = copia_piloto("traz_piloto")
    import trazabilidad_v64 as TZ
    tz = TZ.construir(cp, os.path.join(cp, "Vidrala_v63_evaluada.xlsx"))
    ceros = [a for a in tz["avisos"] if a.startswith("AVISO cero pendiente")]
    paso("G", "un dato desconocido no se convierte en cero: los ceros pendientes de verificación del piloto 4.11 (C48, arrendamientos, minoritarios y, desde la revisión interna R1, adquisiciones de la Historia, que entran en P-M1) se señalan como tales",
         len(ceros) == 4 and any("int_fin_media" in a for a in ceros) and any("h_arrend" in a for a in ceros) and any("h_minoritarios" in a for a in ceros)
         and any("h_adquisiciones" in a for a in ceros), "; ".join(a[:60] for a in ceros))
    # (4.12, revisión interna R4) precio, capitalización y acciones: fechas y resultados de los textos de evidencia contrastados con el valor
    incoh_piloto = [a for a in tz["avisos"] if "incoherente" in a]
    cv_ = os.path.join(TMP, "vigencia", "traz_viscofan", "Viscofan")
    shutil.rmtree(os.path.dirname(cv_), ignore_errors=True)
    shutil.copytree(os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_12", "viscofan", "experimental", "Viscofan"), cv_,
                    ignore=shutil.ignore_patterns("variantes_v64", "recalc", "prompts_generados", "historial_cierres", ".lo_perfil", "texto"))
    tzv = TZ.construir(cv_, os.path.join(cv_, "Viscofan_v63_evaluada.xlsx"))
    incoh_v = [a for a in tzv["avisos"] if "incoherente" in a]
    paso("G", "cadena de trazabilidad: un texto de evidencia del precio, la capitalización o las acciones con otra fecha o con otro resultado que el valor avisa (Viscofan); el piloto 4.11, coherente, no",
         not incoh_piloto and any("fecha incoherente · D-precio" in a for a in incoh_v) and any("valor incoherente · D-capitalizacion" in a for a in incoh_v)
         and any("C-acciones" in a for a in incoh_v) and TZ._coincide(35182858, 35.182858) and TZ._resultados_en("53,60 × 45,6036 = 2.444,4") == [2444.4]
         and TZ._fechas_en("Cierre 6-oct-2026; 2026-11-03") == {"2026-10-06", "2026-11-03"}, "; ".join(a[:70] for a in incoh_v))
    # lecturas con bases parciales identificadas donde se usan
    gm = open(os.path.join(c, "gramatica.md"), encoding="utf-8").read()
    dm = open(os.path.join(c, "datos_v63.md"), encoding="utf-8").read()
    fi = json.load(open(os.path.join(c, "ficha.json"), encoding="utf-8"))
    env64 = dict(os.environ, MUNGER_CONFIG=CFG64)
    rcp, outp = run([PY, os.path.join(PV, "scripts", "ficha.py"), cp, "--provisional"], env=env64)
    fp = json.load(open(os.path.join(cp, "ficha_provisional.json"), encoding="utf-8"))
    lim = (fp.get("configuracion_economica") or {}).get("limites") or []
    paso("G", "G7 y referencias mecánicas (bases heredadas) y BL sin P0 se identifican en gramática, datos, ficha e informe; el piloto 4.11 regenerado en copia no inventa un objetivo 4.12",
         "bases heredadas" in gm and "Lecturas con bases parciales" in dm and any("G7" in x for x in fi["configuracion_economica"]["limites"])
         and rcp == 0 and any(x.startswith("BL ") for x in lim) and fp.get("objetivo") is None, f"rc {rcp} · {outp.strip()[-120:]}")
    # llamadas a mano: variantes y comprobación conjunta resuelven la selección o se detienen sin escribir
    pa = os.path.join(c, "plantilla_activa.json")
    pa_t = open(pa, encoding="utf-8").read()
    pa_j = json.loads(pa_t)
    pa_j["referencia_sha256"] = "0" * 64
    open(pa, "w", encoding="utf-8").write(json.dumps(pa_j))
    antes = listado(c)
    env0 = {k: v for k, v in os.environ.items() if k != "MUNGER_CONFIG"}
    r1, o1 = run([PY, os.path.join(PV, "scripts", "variantes_configuracion_v64.py"), c, libro], env=env0)
    r2, o2 = run([PY, os.path.join(PV, "scripts", "comprobacion_conjunta.py"), c, libro], env=env0)
    cambio = [x for x in listado(c) if x not in antes]
    open(pa, "w", encoding="utf-8").write(pa_t)
    paso("G", "llamadas a mano sin MUNGER_CONFIG a variantes y comprobación conjunta con una selección que no se acredita: código 2 y nada escrito",
         r1 == 2 and r2 == 2 and "SELECCIÓN DE PLANTILLA DETENIDA" in o1 and "SELECCIÓN DE PLANTILLA DETENIDA" in o2 and not [x for x in cambio if not x[0].endswith(".pyc")], f"{r1}/{r2} · {cambio[:3]}")
    # cambio del protocolo después del cierre: retirada, la fase C se repite con las mismas variantes y la auditoría es nueva
    c2 = os.path.join(base, "protocolo", "EmpresaXG")
    shutil.copytree(c, c2, ignore=shutil.ignore_patterns(".lo_perfil", "__pycache__"))
    for n in ("publicaciones_resumen.json", ".publicaciones_resumen.respaldo.json"):
        pr_ = os.path.join(c2, n)
        if os.path.exists(pr_):
            reg = json.load(open(pr_, encoding="utf-8"))
            for e in reg.get("publicaciones") or []:
                e["csv"] = os.path.join(os.path.dirname(c2), os.path.basename(e["csv"]))
                e["expediente"] = c2
            json.dump(reg, open(pr_, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    shutil.copy(os.path.join(os.path.dirname(c), "resumen_v2_v64_experimental.csv"), os.path.join(os.path.dirname(c2), "resumen_v2_v64_experimental.csv"))
    cf2 = json.load(open(os.path.join(c2, "configuracion_economica.json"), encoding="utf-8"))
    cf2["protocolo_objetivo"] = "bloqueo_del_objetivo"
    json.dump(cf2, open(os.path.join(c2, "configuracion_economica.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    var_antes = open(os.path.join(c2, "configuracion_v64_variantes.json"), "rb").read()
    rcp1, outp1, _ = correr(c2, parar_en_espera=True)
    esp = open(os.path.join(c2, "ESPERANDO.md"), encoding="utf-8").read() if os.path.exists(os.path.join(c2, "ESPERANDO.md")) else ""
    pr1 = os.path.join(c2, "prompts_generados", "10_fase_c_turno1.md")
    pr1_t = open(pr1, encoding="utf-8").read() if os.path.exists(pr1) else ""
    rcp2, outp2, _ = correr(c2)
    st2 = json.load(open(os.path.join(c2, "estado_pipeline.json"), encoding="utf-8"))
    ob2 = (json.load(open(os.path.join(c2, "ficha.json"), encoding="utf-8")).get("objetivo") or {})
    paso("G", "cambiar el protocolo después del cierre: retirada, fase C repetida con las mismas variantes (sin recalcularlas) y auditoría nueva; cierra con el bloqueo",
         rcp1 == 10 and "fase_c_turno1" in esp and rcp2 == 0 and st2.get("estado_analisis") == "pendiente_de_datos" and st2.get("auditoria") == "APROBADO"
         and ob2.get("tratamiento") == "objetivo_bloqueado" and open(os.path.join(c2, "configuracion_v64_variantes.json"), "rb").read() == var_antes
         and os.path.isdir(os.path.join(c2, "historial_cierres")), f"rc {rcp1}/{rcp2} · {st2.get('estado_analisis')} · {ob2.get('tratamiento')}")
    paso("G", "con el cambio de protocolo, el motivo («el protocolo del objetivo cambió … repetir la evaluación del objetivo») llega ya al prompt del turno 1 de la fase C y a ESPERANDO.md",
         "el protocolo del objetivo cambió" in pr1_t and "CORRECCIÓN pedida por el pipeline" in pr1_t and "el protocolo del objetivo cambió" in esp, esp[:300])
    # (4.12 §9) fórmula alterada en el libro evaluado de un expediente cerrado: la primera llamada retira la aprobación y la verificación
    # de integridad se repite antes de pedir una auditoría nueva (una auditoría no puede apoyarse en un verificacion_integridad.txt viejo)
    c3 = os.path.join(base, "formula", "EmpresaXG")
    shutil.copytree(c, c3, ignore=shutil.ignore_patterns(".lo_perfil", "__pycache__"))
    for n in ("publicaciones_resumen.json", ".publicaciones_resumen.respaldo.json"):
        pr_ = os.path.join(c3, n)
        if os.path.exists(pr_):
            reg = json.load(open(pr_, encoding="utf-8"))
            for e in reg.get("publicaciones") or []:
                e["csv"] = os.path.join(os.path.dirname(c3), os.path.basename(e["csv"]))
                e["expediente"] = c3
            json.dump(reg, open(pr_, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    shutil.copy(os.path.join(os.path.dirname(c), "resumen_v2_v64_experimental.csv"), os.path.join(os.path.dirname(c3), "resumen_v2_v64_experimental.csv"))
    lev = os.path.join(c3, "EmpresaXG_v63_evaluada.xlsx")
    zin = zipfile.ZipFile(lev)
    wbx, rels = zin.read("xl/workbook.xml").decode(), zin.read("xl/_rels/workbook.xml.rels").decode()
    rid = re.search(r'<sheet[^>]*name="Motor"[^>]*r:id="(rId\d+)"', wbx).group(1)
    tgt = re.search(r'Id="%s"[^>]*Target="([^"]+)"|Target="([^"]+)"[^>]*Id="%s"' % (rid, rid), rels)
    parte = "xl/" + (tgt.group(1) or tgt.group(2)).lstrip("/").replace("xl/", "")
    datos = {i.filename: zin.read(i.filename) for i in zin.infolist()}
    infos = zin.infolist()
    zin.close()
    alterada = datos[parte].replace(b"-CO7+CY7,", b"-CO7+2*CY7,", 1)
    with zipfile.ZipFile(lev, "w", zipfile.ZIP_DEFLATED) as zout:
        for i in infos:
            zout.writestr(i, alterada if i.filename == parte else datos[i.filename])
    rcf, outf, _ = correr(c3, parar_en_espera=True)
    st3 = json.load(open(os.path.join(c3, "estado_pipeline.json"), encoding="utf-8"))
    dg3 = json.load(open(os.path.join(c3, "diagnostico.json"), encoding="utf-8")) if os.path.exists(os.path.join(c3, "diagnostico.json")) else {}
    esp3 = open(os.path.join(c3, "ESPERANDO.md"), encoding="utf-8").read() if os.path.exists(os.path.join(c3, "ESPERANDO.md")) else ""
    paso("G", "fórmula alterada después del cierre: la primera llamada retira la aprobación y repite la verificación de integridad (no pide una auditoría con un verificado viejo)",
         os.path.isdir(os.path.join(c3, "historial_cierres")) and st3.get("auditoria") != "APROBADO" and "verificacion" not in esp3
         and st3.get("estado_analisis") == "no_entregable" and "verificar_todo" in str((dg3.get("causa") or {}).get("detalle")),
         f"rc {rcf} · {st3.get('estado_analisis')} · {str((dg3.get('causa') or {}).get('detalle'))[:140]} · espera: {esp3[:80]}")


# ======================================================================================= H · (4.13 §7) plantilla V6.4.1 y perímetro
V641 = os.path.join(RAIZ, "v6", "v641_experimental")
CFG641 = os.path.join(PV, "config_v2_v641_experimental.json")
E412 = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_12")
E413 = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_13")
ALTAS_VIS = [3.010, 1.633, 6.554, 6.419, 6.494]


def conf_perimetro(conf, perimetro=1, altas=ALTAS_VIS):
    import configuracion_economica as CE
    c = copy.deepcopy(conf)
    c["PM1"]["perimetro_inversion"] = CE.PERIMETROS[perimetro]
    if altas is not None:
        c["PM1"]["altas_derechos_uso"] = list(altas)
        c["PM1"]["altas_fuente"] = "altas de derechos de uso conciliadas (prueba)"
    c.setdefault("trazabilidad", {})["PM1.perimetro"] = {"clase": "convención", "confianza": "media", "fuente_o_condicion": "prueba",
                                                         "justificacion": "perímetro de la inversión", "materialidad": "variantes"}
    return c


def grupo_h():
    import configuracion_economica as CE
    import seleccion_plantilla as SEL
    import entradas_economicas as EE
    import variantes_configuracion_v64 as VAR
    import cierre_v2 as CIE
    import config_v2
    plantilla = os.path.join(V641, "entregables", "Plantilla_V6.4.1_experimental.xlsx")
    ref = os.path.join(V641, "referencia", "referencia_V6.4.1_experimental.json")
    # plantilla y referencia nuevas; la V6.4 conserva sus bytes
    rc, out = run([PY, "-I", os.path.join(V641, "scripts", "verificar_v64.py"), plantilla, ref])
    rc1, out1 = run(["sha256sum", "-c", os.path.join("referencia", "SHA256_entregables_V6.4.1_experimental.txt")], cwd=V641)
    rc2, out2 = run(["sha256sum", "-c", os.path.join("referencia", "SHA256_entregables_V6.4_experimental.txt")], cwd=V64)
    paso("H", "V6.4.1: plantilla ÍNTEGRA con su referencia nueva y huellas de sus entregables; la V6.4 conserva las suyas",
         rc == 0 and "ÍNTEGRO" in out and rc1 == 0 and rc2 == 0, (out.strip().splitlines() or [""])[-1][:120] + " · " + out2.strip().replace("\n", " ")[:120])
    sys.path.insert(0, os.path.join(V641, "scripts"))
    import importlib
    # los módulos de la plantilla tienen el mismo nombre en la V6.4 y en la V6.4.1: los de otros grupos (V6.4) no se reutilizan
    for m in ("generar_referencia", "inventario_entradas", "trasladar_entradas", "verificar_v64"):
        sys.modules.pop(m, None)
    GR = importlib.import_module("generar_referencia")
    with tempfile.TemporaryDirectory() as t:
        nueva = os.path.join(t, "reconstruida.xlsx")
        rc, out = run([PY, "-I", os.path.join(V641, "scripts", "construir_v641_experimental.py"),
                       os.path.join(V64, "entregables", "Plantilla_V6.4_experimental.xlsx"), nueva])
        a = GR.capturar(plantilla)
        b = GR.capturar(nueva) if rc == 0 else {}
        import comparar_zip as CZ
        ok_m, det_m = CZ.comparar(plantilla, nueva) if rc == 0 else (False, "sin reconstrucción")
        paso("H", "reconstrucción de la V6.4.1 desde la V6.4: mismas fórmulas, fijos, validaciones, formatos, nombres y partes, y el mismo contenido miembro a miembro",
             rc == 0 and ok_m and all(a[k] == b.get(k) for k in ("hojas", "formulas", "fijos", "validaciones", "formato_condicional", "nombres_definidos", "partes_paquete")),
             f"rc {rc} · {det_m} · {out.strip()[-160:]}")
    r = json.load(open(ref, encoding="utf-8"))
    r64 = json.load(open(os.path.join(V64, "referencia", "referencia_V6.4_experimental.json"), encoding="utf-8"))
    dif_f = sorted(k for k in set(r["formulas"]) | set(r64["formulas"]) if r["formulas"].get(k) != r64["formulas"].get(k))
    # (y Panel!A1, cuyo título dice la versión: una de las siete etiquetas de versión de la reconstrucción)
    esperadas = {k for k in dif_f if k == "Panel!A1" or re.match(r"Configuración V6\.4!(B55|B58|B9|B124|B143|[A-I]14[2-9]|[A-I]15[0-6])$", k)}
    paso("H", "las diferencias de fórmulas entre las referencias V6.4 y V6.4.1 son solo las declaradas (B55, B58, B9, B124, B143, filas 142–156 y el título de Panel con la versión) y las partes del paquete son las mismas",
         dif_f and set(dif_f) == esperadas and r["partes_paquete"] == r64["partes_paquete"], f"{len(dif_f)} · {[k for k in dif_f if k not in esperadas][:5]}")
    # configuración: validación del perímetro y compatibilidad con la plantilla
    base = conf_sintetica()
    niif = conf_perimetro(base)
    caja_con_altas = conf_perimetro(base, 0)
    malos = {"perímetro no reconocido": conf_perimetro(base, 1) | {}, "NIIF 16 sin altas": conf_perimetro(base, 1, None),
             "altas con cuatro años": conf_perimetro(base, 1, ALTAS_VIS[:4]), "altas negativas": conf_perimetro(base, 1, [1, 2, -1, 3, 4])}
    malos["perímetro no reconocido"]["PM1"]["perimetro_inversion"] = "Caja"
    sin_fuente = conf_perimetro(base)
    sin_fuente["PM1"]["altas_fuente"] = " "
    malos["altas sin fuente"] = sin_fuente
    tipo = conf_perimetro(base)
    tipo["PM1"]["altas_derechos_uso"] = "24,11"
    malos["altas de otro tipo (texto)"] = tipo
    sin_traza = conf_perimetro(base)
    del sin_traza["trazabilidad"]["PM1.perimetro"]
    malos["sin trazabilidad PM1.perimetro"] = sin_traza
    fallan = {k: CE.validar(v) for k, v in malos.items()}
    paso("H", "configuración V6.4.1: NIIF 16 con cinco altas y fuente es válida; «Caja» con altas declaradas también (no las suma); se rechazan perímetro no reconocido, NIIF 16 sin altas, altas incompletas, negativas, sin fuente, de otro tipo o sin trazabilidad",
         not CE.validar(niif) and not CE.validar(caja_con_altas) and all(fallan.values()) and "PM1.perimetro" in CE.activos(niif)
         and "PM1.perimetro" not in CE.activos(base), {k: (v[:1] or ["NO RECHAZA"])[0][:70] for k, v in fallan.items()})
    c64 = {"plantilla": {"version": "V6.4 experimental"}}
    c641 = {"plantilla": {"version": "V6.4.1 experimental"}}
    paso("H", "selección: la V6.4 rechaza una configuración con perímetro; la V6.4.1 con requisito adicional exige declararlo; las dos son de la familia V6.4",
         SEL.compatibilidad_perimetro(niif, c64) and SEL.compatibilidad_perimetro(base, c641) and not SEL.compatibilidad_perimetro(niif, c641)
         and not SEL.compatibilidad_perimetro(base, c64) and SEL.es_v64(c64) and SEL.es_v64(c641) and SEL.es_v641(c641) and not SEL.es_v641(c64)
         and not SEL.compatibilidad_perimetro(conf_sintetica("Heredado"), c641))
    # huellas: las configuraciones y variantes guardadas de la 4.12 conservan la suya; el perímetro la cambia
    guardadas = []
    for pv in glob.glob(os.path.join(E412, "**", "configuracion_v64_variantes.json"), recursive=True):
        v = json.load(open(pv, encoding="utf-8"))
        guardadas.append(v.get("configuracion_huella_economica") == EE.huella_configuracion(json.load(open(os.path.join(os.path.dirname(pv), "configuracion_economica.json"), encoding="utf-8"))))
    paso("H", "huella económica: las configuraciones guardadas de la 4.12 conservan su huella exacta; declarar el perímetro la cambia; «Caja» sin altas = sin perímetro en el libro",
         guardadas and all(guardadas) and EE.huella_configuracion(niif) != EE.huella_configuracion(base)
         and CE.celdas(base, v641=True)[f"{CE.HOJA}!B146"] is None and f"{CE.HOJA}!B146" not in CE.celdas(base), f"{sum(guardadas)}/{len(guardadas)}")
    claves = [v[0] for v in VAR.variantes(niif)]
    alt, mot = CE.alternativas(niif, "PM1.perimetro")
    alt_c, mot_c = CE.alternativas(conf_perimetro(base, 0, None), "PM1.perimetro")
    alt_e, _ = CE.alternativas(niif, "PM1.estructura")
    paso("H", "variantes y alternativas: el otro perímetro y sus extremos del rango; «Caja» sin altas no inventa la alternativa NIIF 16; las alternativas de estructura conservan el perímetro",
         {"perimetro_alternativo", "perimetro_alternativo_parametro_minimo", "perimetro_alternativo_parametro_maximo"} <= set(claves)
         and alt and alt[0][1]["PM1"]["perimetro_inversion"] == CE.PERIMETROS[0] and CE.parametros_variados(niif, alt[0][1]) == ["PM1.perimetro"]
         and not alt_c and "no declara" in str(mot_c) and len(alt_e) == 5, f"{claves} · {mot_c}")
    paso("H", "resumen propio: un expediente V6.4.1 publica en resumen_v2_v641_experimental.csv (ni en el de la V6.4 ni en el de la V6.3)",
         config_v2.cargar(CFG641).get("resumen_csv_nombre") == "resumen_v2_v641_experimental.csv" and CIE.RESUMEN_V641 == "resumen_v2_v641_experimental.csv")
    # (4.13 §5) cobertura por hipótesis y avisos de dominio de las variantes (unidad, sin LibreOffice)
    import objetivo_v64 as OBJ
    import dominios_v64 as DOM
    cvv = json.load(open(os.path.join(E412, "cierre_condicionado", "Vidrala", "configuracion_economica.json"), encoding="utf-8"))
    vs_v = VAR.variantes(cvv)
    var_u = {"formato": "4.13", "variantes": [{"clave": k, "zona": ("cumple_regla_k" if k == "estructura_SR2" else "caro"), "precio_si": 50.0 + i,
                                                "parametros_variados": CE.parametros_variados(cvv, cf)} for i, (k, _, cf) in enumerate(vs_v)]}
    cb = {k: OBJ.cobertura(var_u, k, cvv, None, "por_encima_del_precio_de_si") for k in CE.activos(cvv) if k != "modo"}
    paso("H", "(4.13 §5) cobertura: SR2 cubre el ROIC terminal como variación conjunta necesaria; R0 con P-M1 quitada cubre la regla como necesaria; la familia solo "
              "por variaciones conjuntas; contrastes aislados de N2, escudo, cartera, λ y convenciones; invariancia de la acción calculada aparte",
         cb["PM1.roic_terminal"]["tipo"] == "variacion_conjunta_necesaria" and cb["PM1.roic_terminal"]["conjuntas_necesarias"] == ["estructura_SR2"]
         and cb["N3.regla"]["tipo"] == "variacion_conjunta_necesaria" and "activa_R0_sin_PM1" in cb["N3.regla"]["conjuntas_necesarias"]
         and cb["PM1.familia"]["tipo"] == "variacion_conjunta" and cb["N1.tipo"]["tipo"] == "variacion_conjunta_necesaria"
         and all(cb[k]["tipo"] == "contraste_aislado" for k in ("N2.margen", "N1.escudo", "PM1.cartera", "PM1.parametro", "PM1.convencion_anios", "PM1.convencion_terminal"))
         and cb["PM1.estructura"]["accion_invariante_en_contrastes"] is False and cb["PM1.familia"]["accion_invariante_en_variantes_calculadas"] is True,
         {k: v["tipo"] for k, v in cb.items()})
    av = lambda **kw: [{"id": i, "activo": kw.get(i, False), "valores": {"f": kw.get("f")}} for i in DOM.IDS]  # noqa: E731
    por_v = {"activa": av(factor_de_reestimacion=None, f=1.16), "parametro_minimo": av(factor_de_reestimacion=None, f=1.31),
             "solo_N2": av(inversion_fija_para_crecer_negativa=True), "heredado": av()}
    filas_u = [{"clave": "activa", "zona": "caro", "precio_si": 55.0}, {"clave": "parametro_minimo", "zona": "caro", "precio_si": 51.3},
               {"clave": "solo_N2", "zona": "cumple_regla_k", "precio_si": 65.7}, {"clave": "heredado", "zona": "caro", "precio_si": 60.0}]
    g = DOM.agrupar(por_v, filas_u, OBJ.CLASE_ZONA)
    paso("H", "(4.13 §5) avisos de dominio de todas las variantes, agrupados: el aviso de un extremo del rango que no está en la activa se ve, con la conclusión a la que "
              "afecta (extremo superior e invariancia de la acción); el factor de reestimación lleva su rango de f; la fase C evalúa los dos grupos",
         g["inversion_fija_para_crecer_negativa"]["variantes"] == ["solo_N2"] and not g["inversion_fija_para_crecer_negativa"]["en_la_activa"]
         and any("extremo superior" in x for x in g["inversion_fija_para_crecer_negativa"]["afecta"]) and "acción" in g["inversion_fija_para_crecer_negativa"]["conclusiones"]
         and (g["factor_de_reestimacion"]["f_minimo"], g["factor_de_reestimacion"]["f_maximo"]) == (1.16, 1.31)
         and any("extremo inferior" in x for x in g["factor_de_reestimacion"]["afecta"])
         and sorted(DOM.grupos_a_evaluar(g)) == ["factor_de_reestimacion", "inversion_fija_para_crecer_negativa"], g)
    # (4.13, revisión interna R6, R12 y R17)
    import referencias_mecanicas as RM
    dvis = json.load(open(os.path.join(E413, "viscofan", "Viscofan", "datos_v63.json"), encoding="utf-8"))
    r_n = RM.calcular(dvis, config_v2.cargar(CFG641))["palancas"]["s2c"]
    dvis_caja = copy.deepcopy(dvis)
    dvis_caja["configuracion_v64"]["perimetro_efectivo"] = "Caja"
    r_c = RM.calcular(dvis_caja, config_v2.cargar(CFG641))["palancas"]["s2c"]
    paso("H", "(4.13, R6) con el perímetro NIIF 16 efectivo, la referencia mecánica del S2C se ancla en el S2C histórico del mismo perímetro (B155), no en C53 («Caja»)",
         "s2c_perimetro_niif16_B155" in r_n["anclas_usadas"] and "B155" in r_n["regla"] and "s2c_perimetro_niif16_B155" not in r_c["anclas_usadas"] and "Historia!C53" in r_c["regla"],
         f"NIIF 16 {r_n['MALO'], r_n['NORMAL'], r_n['BUENO']} · Caja {r_c['MALO'], r_c['NORMAL'], r_c['BUENO']}")
    inf = copy.deepcopy(base)
    inf["PM1"]["lambda"] = float("inf")
    nan = copy.deepcopy(base)
    nan["N3"]["existencias"] = float("nan")
    paso("H", "(4.13, R12) validar rechaza Infinity y NaN", bool(CE.validar(inf)) and bool(CE.validar(nan)), (CE.validar(inf)[:1], CE.validar(nan)[:1]))
    g_l = DOM.agrupar({"activa": [{"id": DOM.IDS[1], "activo": None, "valores": {"f": 1.1}}]}, [{"clave": "activa", "zona": "caro", "precio_si": 10.0}], OBJ.CLASE_ZONA)
    paso("H", "(4.13, R17) un grupo de avisos que en la activa es una lectura sin umbral sale «en la activa»", g_l[DOM.IDS[1]]["en_la_activa"] is True, g_l)
    # libro: aplicar la configuración en un libro V6.4.1 con las entradas de Viscofan (4.12) y leerla
    vis = os.path.join(E412, "viscofan", "experimental", "Viscofan")
    conf_v = json.load(open(os.path.join(vis, "configuracion_economica.json"), encoding="utf-8"))
    TR = importlib.import_module("trasladar_entradas")
    import leer_v63
    from openpyxl import load_workbook
    cfg641 = config_v2.cargar(CFG641)
    with tempfile.TemporaryDirectory() as t:
        libro = os.path.join(t, "Viscofan_v641.xlsx")
        TR.trasladar(os.path.join(vis, "Viscofan_v63_evaluada.xlsx"), plantilla, libro, None)
        lecturas = {}
        for nombre, cv in (("niif", conf_perimetro(conf_v)), ("caja", conf_perimetro(conf_v, 0)), ("sin_perimetro", conf_v)):
            pc = os.path.join(t, f"{nombre}.json")
            json.dump(cv, open(pc, "w", encoding="utf-8"), ensure_ascii=False)
            dst = os.path.join(t, f"{nombre}.xlsx")
            # aplicar sobre el libro con NIIF 16 ya escrito: una configuración sin perímetro tiene que vaciarlo (no se arrastra)
            src = os.path.join(t, "niif.xlsx") if nombre != "niif" else libro
            n, rc_v, linea = CE.aplicar(src, dst, pc, cfg641)
            rec = recalc(dst, os.path.join(t, "rc"), os.path.join(t, ".lo"))
            cvl = leer_v63.configuracion_v64(load_workbook(rec, data_only=True)) if rec else {}
            lecturas[nombre] = (rc_v, cvl.get("perimetro_efectivo"), cvl.get("altas_derechos_uso"), cvl.get("valida"), cvl.get("F_hist"), cvl.get("trazabilidad_completa"))
    ok = (lecturas["niif"][:4] == (0, "NIIF 16", lecturas["niif"][2], True) and abs((lecturas["niif"][2] or 0) - sum(ALTAS_VIS)) < 1e-9
          and lecturas["caja"][:4] == (0, "Caja", 0, True) and lecturas["sin_perimetro"][1] == "Caja" and lecturas["sin_perimetro"][2] == 0
          and abs((lecturas["niif"][4] or 0) - (lecturas["caja"][4] or 0) - sum(ALTAS_VIS)) < 1e-9 and lecturas["sin_perimetro"][4] == lecturas["caja"][4])
    paso("H", "configuracion_economica.aplicar en un libro V6.4.1 (entradas de Viscofan): NIIF 16 suma las altas a F_hist; «Caja» y una configuración sin perímetro vacían B146:B152 y dan la V6.4; libros ÍNTEGROS",
         ok, lecturas)
    # compatibilidad completa (LibreOffice): perímetro vacío = V6.4 celda a celda, heredado = heredado, NIIF 16 con θ = 0, 0,5 y 1 y réplica
    rc, out = run([PY, "-I", os.path.join(E413, "scripts", "compatibilidad_v641.py")], cwd=RAIZ)
    paso("H", "compatibilidad_v641.py: 0 celdas distintas con el perímetro vacío o «Caja» y en heredado; textos del resumen B9 que solo añaden el perímetro; réplica de las bases sin discrepancias",
         rc == 0, (out.strip().splitlines() or [""])[-1][:200])
    # pasada del pipeline con la V6.4.1 (agentes simulados), perímetro NIIF 16
    bp = os.path.join(TMP, "v641")
    shutil.rmtree(bp, ignore_errors=True)
    c = os.path.join(bp, "sel", "EmpresaXP")
    preparar_sintetico(c, base)
    antes = listado(c)
    rc_s, out_s, _ = correr(c, cfg=CFG641)
    paso("H", "pipeline con la V6.4.1 y requisito adicional sin perímetro declarado: código 2 sin escribir nada", rc_s == 2 and listado(c) == antes and "PM1.perimetro_inversion es obligatorio" in out_s,
         out_s.strip().splitlines()[-1][:200] if out_s.strip() else "")
    c = os.path.join(bp, "sel64", "EmpresaXQ")
    preparar_sintetico(c, niif)
    antes = listado(c)
    rc_s, out_s, _ = correr(c, cfg=CFG64)
    paso("H", "pipeline con la V6.4 y una configuración con perímetro: código 2 sin escribir nada (no se ignora)", rc_s == 2 and listado(c) == antes and "solo existe en la plantilla V6.4.1" in out_s,
         out_s.strip().splitlines()[-1][:200] if out_s.strip() else "")
    c = os.path.join(bp, "exp", "EmpresaXN")
    preparar_sintetico(c, conf_perimetro(base, 1, [0.5, 0.4, 0.6, 0.5, 0.7]))
    rc, out, _ = correr(c, cfg=CFG641)
    st = json.load(open(os.path.join(c, "estado_pipeline.json"), encoding="utf-8")) if os.path.exists(os.path.join(c, "estado_pipeline.json")) else {}
    pa = json.load(open(os.path.join(c, "plantilla_activa.json"), encoding="utf-8")) if os.path.exists(os.path.join(c, "plantilla_activa.json")) else {}
    f = json.load(open(os.path.join(c, "ficha.json"), encoding="utf-8")) if os.path.exists(os.path.join(c, "ficha.json")) else {}
    var = json.load(open(os.path.join(c, "configuracion_v64_variantes.json"), encoding="utf-8")) if os.path.exists(os.path.join(c, "configuracion_v64_variantes.json")) else {}
    inf = open(os.path.join(c, "informe.md"), encoding="utf-8").read() if os.path.exists(os.path.join(c, "informe.md")) else ""
    ef = ((f.get("configuracion_economica") or {}).get("efectivos_en_el_libro") or {})
    paso("H", "pasada V6.4.1 experimental con NIIF 16 (agentes simulados): concluido · APROBADO, plantilla_activa con las huellas de la V6.4.1, perímetro en la ficha y el informe, variante del otro perímetro calculada y resumen propio",
         rc == 0 and st.get("estado_analisis") == "concluido" and st.get("auditoria") == "APROBADO" and pa.get("version") == "V6.4.1 experimental"
         and pa.get("archivo_sha256") == sha(plantilla) and ef.get("perimetro_efectivo") == "NIIF 16" and abs((ef.get("altas_derechos_uso") or 0) - 2.7) < 1e-9
         and "perímetro de la inversión NIIF 16" in inf and "## 14. Plantilla y configuración económica (V6.4.1 experimental; no adoptada)" in inf
         and any(v.get("clave") == "perimetro_alternativo" and v.get("zona") for v in var.get("variantes") or [])
         and os.path.exists(os.path.join(bp, "exp", "resumen_v2_v641_experimental.csv")) and not os.path.exists(os.path.join(bp, "exp", "resumen_v2_v64_experimental.csv")),
         f"rc {rc} · {st.get('estado_analisis')} · {st.get('auditoria')} · {pa.get('version')} · {ef.get('perimetro_efectivo')} · {ef.get('altas_derechos_uso')} · {out.strip().splitlines()[-1][:120] if out.strip() else ''}")
    antes = listado(c)
    rc_s, out_s, _ = correr(c, cfg=CFG64)
    paso("H", "el expediente V6.4.1 ejecutado con la configuración V6.4: código 2 sin escribir nada", rc_s == 2 and listado(c) == antes, out_s.strip().splitlines()[-1][:160] if out_s.strip() else "")


def main():
    grupos = [g for g in sys.argv[1:] if g in "ABCDEFGH"] or list("ABCDEFGH")
    os.makedirs(TMP, exist_ok=True)
    for g in grupos:
        try:
            {"A": grupo_a, "B": grupo_b, "C": grupo_c, "D": grupo_d, "E": lambda: (grupo_e(), grupo_e_revision_413()), "F": lambda: (grupo_f(), grupo_f_413(), grupo_f_revision_413()), "G": grupo_g, "H": grupo_h}[g]()
        except Exception as e:  # una excepción es un fallo de la batería, no un PASA
            import traceback
            paso(g, "el grupo terminó sin excepciones", False, f"{type(e).__name__}: {e} · {traceback.format_exc().splitlines()[-3:]}")
    n_ok = sum(1 for r in RES if r["ok"])
    json.dump(RES, open(os.path.join(TMP, "resultados_integracion_v64.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{n_ok}/{len(RES)} pruebas de integración V6.4 PASAN")
    return 0 if n_ok == len(RES) else 1


if __name__ == "__main__":
    sys.exit(main())
