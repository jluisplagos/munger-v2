#!/usr/bin/env python3
"""Libros de PROPUESTA N1–N2 (entrega 4.7, bloque B). Copias identificadas; el libro de referencia no se toca.

Uso: python3 -I propuesta_excel.py   (escribe ../financiero/propuesta_excel/)

Dos copias del libro evaluado de la referencia 4.6.1 (Vidrala_v63_evaluada.xlsx):
  A. PROPUESTA_M2_ultimo_anio.xlsx: la única alternativa N1–N3 que la plantilla representa con una entrada propia:
     Palancas!C8 = «Último año» (lista Opciones!M3:M4) → Diagnóstico V6!C10 toma Historia!C48 (margen de 2025). Se escribe con
     escribir_v63.py --lista-blanca cualquiera --copia-de-prueba.
  B. PROPUESTA_T1_M1.xlsx: la combinación recomendada de N1 y N2. La plantilla no tiene entrada para un tipo normalizado ni para un
     margen de ciclo de otro perímetro: Historia!C52 (tipo) y Historia!C49 (margen) son fórmulas sobre los hechos publicados, y
     escribir_v63.py se niega con razón a escribir fórmulas. Primer intento (registrado): sustituir Historia!C52 y C49 por valores; la
     regla V39 del Motor lo bloquea («Alguna celda de salida (…; Historia C44, C48, C52, …) ha sido sobrescrita con un valor») y la
     hoja no da valor. En esta copia de propuesta, y solo en ella, se sustituyen en su lugar las dos celdas intermedias que consume
     el motor, Diagnóstico V6!C10 (margen de partida → Motor D6:D…) y Diagnóstico V6!C11 (tipo → Motor K…, r_op de Diagnóstico
     V6!C15), que la V39 no vigila: la protección de la plantilla se ELUDE de forma declarada, un nivel más abajo (auditoría interna,
     H-13). Historia, sus fórmulas y los hechos publicados quedan intactos. Consumidores que siguen leyendo Historia (no entran en el
     valor): Diagnóstico V6!B176:D176 (margen NORMAL tras impuestos, comparación de anclas), Motor E218 (comprobación de rango) y
     E236 (V39), que leen Historia!C52, y Palancas!F15 («media propia»), que lee Historia!C49 y sigue mostrando 16,86 %. El libro deja
     de ser una V6.3 íntegra: es una propuesta, no un entregable.
  N3 (R1 / R2) no es representable en la plantilla (la reinversión es ΔV ÷ S2C en las dos direcciones) y queda en el modelo
  auxiliar de analisis_n1_n3.py.
Cada copia se recalcula (recalc.sh, recálculo forzado), se lee con leer_resultados.py y precio_de_si.py (k = 3), se compara con la
réplica (tolerancia 0,005 €) y se compara celda a celda (fórmulas y valores) con la referencia.
"""
import json
import os
import shutil
import subprocess
import sys

sys.dont_write_bytecode = True
AQUI = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CORR = os.path.dirname(AQUI)
PV2 = os.path.dirname(CORR)
SCR = os.path.join(PV2, "scripts")
REF = os.path.join(CORR, "2026-11_Vidrala_ensayo_4_6_1", "Vidrala")
LIBRO = os.path.join(REF, "Vidrala_v63_evaluada.xlsx")
SAL = os.path.join(AQUI, "financiero", "propuesta_excel")
TOL = 0.005
sys.path.insert(0, SCR)
from v63_xml import NS, LibroV63  # noqa: E402

mat = json.load(open(os.path.join(AQUI, "financiero", "matriz.json"), encoding="utf-8"))
T1, M1 = mat["t_rec"], mat["m_rec"]
REPLICA = {f["combinacion"]: f for f in mat["matriz"]}
shutil.rmtree(SAL, ignore_errors=True)
os.makedirs(SAL)
perfil = os.path.join(os.environ.get("TMPDIR", "/tmp"), "lo_perfil_propuesta47")
LOG = []
AVISO_PRECIO = ("PROPUESTA de la entrega 4.7, no aplicada: valores, ponderado y precio de Sí mecánicos de un ensayo sobre una copia "
                "identificada. La zona, las distancias y g_impl frente a 87,9 (3-nov-2026) NO son una comparación válida con el precio "
                "ni una recomendación de compra o espera.")


def log(s=""):
    LOG.append(s)
    print(s)


def recalc_y_leer(libro, nombre):
    d = os.path.join(SAL, nombre)
    os.makedirs(d)
    subprocess.run(["bash", os.path.join(SCR, "recalc.sh"), libro, os.path.join(d, "recalc"), perfil], check=True, capture_output=True)
    rec = os.path.join(d, "recalc", os.path.basename(libro))
    r = subprocess.run([sys.executable, os.path.join(SCR, "leer_resultados.py"), rec, os.path.join(d, "resultados.json"), "--exigir-recalculo-forzado"], capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
    r = subprocess.run([sys.executable, os.path.join(SCR, "precio_de_si.py"), os.path.join(d, "resultados.json"), os.path.join(d, "precio.json"), "--k", "3"], capture_output=True, text=True)
    assert r.returncode in (0, 5), r.stdout + r.stderr
    pj = json.load(open(os.path.join(d, "precio.json"), encoding="utf-8"))
    # (auditoría interna, H-13) la lectura de precio_de_si.py trae zona y distancias frente al precio de la hoja: se marca el archivo
    pj = {"aviso": AVISO_PRECIO, **pj}
    json.dump(pj, open(os.path.join(d, "precio.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return json.load(open(os.path.join(d, "resultados.json"), encoding="utf-8")), pj, rec


def celdas(path):
    """{hoja!ref: (fórmula o None, valor en caché)} de todas las hojas, leído del XML."""
    import openpyxl
    wf = openpyxl.load_workbook(path)
    wv = openpyxl.load_workbook(path, data_only=True)
    out = {}
    for ws in wf.worksheets:
        vs = wv[ws.title]
        for row in ws.iter_rows():
            for c in row:
                if c.value is None:
                    continue
                f = c.value if isinstance(c.value, str) and c.value.startswith("=") else None
                out[f"{ws.title}!{c.coordinate}"] = (f, vs[c.coordinate].value if f else c.value)
    return out


def diferencias(ref_rec, prop_rec, ref_xml, prop_xml):
    a, b = celdas(ref_xml), celdas(prop_xml)
    f_dif = sorted(k for k in set(a) | set(b) if (a.get(k, (None, None))[0] != b.get(k, (None, None))[0]) or (a.get(k, (None, None))[0] is None and b.get(k, (None, None))[0] is None and a.get(k, (None, None))[1] != b.get(k, (None, None))[1]))
    av, bv = celdas(ref_rec), celdas(prop_rec)
    v_dif = []
    for k in sorted(set(av) | set(bv)):
        x, y = av.get(k, (None, None))[1], bv.get(k, (None, None))[1]
        if isinstance(x, (int, float)) and isinstance(y, (int, float)):
            if abs(x - y) > 1e-9 * max(1, abs(x)):
                v_dif.append((k, x, y))
        elif x != y:
            v_dif.append((k, x, y))
    return [(k, a.get(k, (None, None)), b.get(k, (None, None))) for k in f_dif], v_dif


def comparar(nombre, pr, comb):
    rp = REPLICA[comb]
    V = pr["V"]
    ok = all(abs(x - y) < TOL for x, y in zip(V, (rp["V_malo"], rp["V_normal"], rp["V_bueno"]))) and abs(pr["ponderado"] - rp["ponderado"]) < TOL and abs(pr["precio_si"] - rp["precio_si"]) < TOL
    log(f"  {nombre}: libro V {[round(x, 4) for x in V]} · ponderado {pr['ponderado']:.4f} · precio de Sí {pr['precio_si']:.4f}")
    log(f"  réplica {comb}: V {[round(rp[k], 4) for k in ('V_malo', 'V_normal', 'V_bueno')]} · ponderado {rp['ponderado']:.4f} · precio de Sí {rp['precio_si']:.4f} → {'COINCIDE' if ok else 'NO COINCIDE'} (tolerancia {TOL} €)")
    return ok


log("LIBROS DE PROPUESTA N1–N2 · entrega 4.7 (copias identificadas; resultados mecánicos, no comparables con el precio)")
ref_res = json.load(open(os.path.join(REF, "resultados.json"), encoding="utf-8"))
ref_rec = os.path.join(REF, "recalc", "Vidrala_v63_evaluada.xlsx")
oks = []

# A · M2 por la entrada de la plantilla
pa = os.path.join(SAL, "PROPUESTA_M2_ultimo_anio.xlsx")
cj = os.path.join(SAL, "celdas_M2.json")
json.dump({"Palancas!C8": "Último año"}, open(cj, "w", encoding="utf-8"), ensure_ascii=False)
r = subprocess.run([sys.executable, os.path.join(SCR, "escribir_v63.py"), LIBRO, pa, "--celdas", cj, "--lista-blanca", "cualquiera", "--copia-de-prueba", "--registro", os.path.join(SAL, "registro_escritura_M2.json")], capture_output=True, text=True)
assert r.returncode == 0, r.stdout + r.stderr
log("\nA. Palancas!C8 = «Último año» (entrada de la plantilla) · " + r.stdout.strip())
res_a, pr_a, rec_a = recalc_y_leer(pa, "M2")
log(f"  m0 leído {res_a['m0']:.6f} (Historia!C48) · t {res_a['t']:.6f} · r_op {res_a['r_operativa_C15']:.6f}")
oks.append(comparar("PROPUESTA_M2", pr_a, "T0·M2·R0"))
fd, vd = diferencias(ref_rec, rec_a, LIBRO, pa)
log(f"  celdas con fórmula o entrada distinta de la referencia: {len(fd)} → " + "; ".join(f"{k}: {x[0] or x[1]!r} → {y[0] or y[1]!r}" for k, x, y in fd))
log(f"  celdas con valor recalculado distinto: {len(vd)}")
oks.append(len(fd) == 1 and fd[0][0] == "Palancas!C8")

# B · T1 y M1 en las celdas intermedias que consume el motor (Historia queda intacta; ver la cabecera)
pb = os.path.join(SAL, "PROPUESTA_T1_M1.xlsx")
lib = LibroV63(LIBRO)
antes = {}
for ref, val in (("C11", T1), ("C10", M1)):
    c = lib._celda("Diagnóstico V6", ref)
    f = c.find(f"{{{NS}}}f")
    antes[ref] = f.text
    c.remove(f)  # solo en la copia de propuesta: el valor sustituye a la fórmula
    lib.escribir("Diagnóstico V6", ref, round(val, 6))
n_cache = lib.borrar_caches()
lib.marcar_modificada("Diagnóstico V6")
lib.guardar(pb)
log(f"\nB. Diagnóstico V6!C11 (tipo) = {round(T1, 6)} (antes ={antes['C11']}) · Diagnóstico V6!C10 (margen de partida) = {round(M1, 6)} (antes ={antes['C10']}) · {n_cache} cachés borradas")
log("  (primer intento, descartado: sustituir Historia!C52 y C49; la regla V39 del Motor bloquea el valor porque Historia!C52 es celda de salida protegida)")
res_b, pr_b, rec_b = recalc_y_leer(pb, "T1_M1")
log(f"  m0 leído {res_b['m0']:.6f} · t {res_b['t']:.6f} · r_op {res_b['r_operativa_C15']:.6f} (referencia {ref_res['r_operativa_C15']:.6f})")
oks.append(comparar("PROPUESTA_T1_M1", pr_b, "T1·M1·R0"))
fd, vd = diferencias(ref_rec, rec_b, LIBRO, pb)
log(f"  celdas con fórmula o entrada distinta de la referencia: {len(fd)} → " + "; ".join(f"{k}: {x[0] or x[1]!r} → {y[0] or y[1]!r}" for k, x, y in fd))
log(f"  celdas con valor recalculado distinto: {len(vd)} (las primeras 25:)")
for k, x, y in vd[:25]:
    log(f"    {k}: {x!r} → {y!r}")
oks.append(sorted(k for k, _, _ in fd) == ["Diagnóstico V6!C10", "Diagnóstico V6!C11"])
json.dump({"A": {"celdas": {"Palancas!C8": "Último año"}, "precio": pr_a}, "B": {"formulas_sustituidas": antes, "valores": {"Diagnóstico V6!C11": round(T1, 6), "Diagnóstico V6!C10": round(M1, 6)}, "precio": pr_b},
           "valores_distintos_B": [[k, str(x), str(y)] for k, x, y in vd]}, open(os.path.join(SAL, "comparacion.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
for d in ("M2", "T1_M1"):
    shutil.rmtree(os.path.join(SAL, d, "recalc"), ignore_errors=True)  # la copia recalculada solo sirve para leer valores
ok = all(oks)
log(f"\nRESULTADO: {'las dos propuestas reproducen la réplica y solo difieren de la referencia en las celdas declaradas' if ok else 'ERROR'} ({sum(oks)} de {len(oks)})")
open(os.path.join(SAL, "salida.txt"), "w", encoding="utf-8").write("\n".join(LOG) + "\n")
sys.exit(0 if ok else 1)
