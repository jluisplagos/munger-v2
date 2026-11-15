"""Sonda H5 (encargo de cierre §4): piloto 4.11 cerrado y vigente, publicaciones y respaldo reubicados dentro de la copia,
sin ficha.json ni cierre_vigente.json, PM1.lambda = 1,25; primera llamada independiente por vía.

Uso: python3 -B sonda_h5.py PERSONAJE_V2 [vias] [variante]
variante: ambos (por defecto) | sin_ficha | sin_cierre | ninguno (control: solo el material cambiado)
Escribe una línea por vía con el estado interno, la fila pública, el registro y el rastro de la retirada.
"""
import csv, glob, json, os, sys
PV = os.path.abspath(sys.argv[1])
vias = sys.argv[2].split(",") if len(sys.argv) > 2 and sys.argv[2] != "todas" else ["pipeline", "ficha", "informe", "resumen"]
variante = sys.argv[3] if len(sys.argv) > 3 else "ambos"
sys.path.insert(0, os.path.join(PV, "pruebas")); sys.path.insert(0, os.path.join(PV, "scripts"))
import test_integracion_v64 as T
import cierre_v2 as CIE
os.makedirs(T.TMP, exist_ok=True)


def foto(c):
    st = json.load(open(os.path.join(c, "estado_pipeline.json"), encoding="utf-8"))
    filas = list(csv.DictReader(open(os.path.join(os.path.dirname(c), "resumen_v2.csv"), encoding="utf-8", newline="")))
    reg = json.load(open(os.path.join(c, CIE.REGISTRO_RESUMEN), encoding="utf-8"))
    ret = sorted(glob.glob(os.path.join(c, "historial_cierres", "*", "RETIRADA.json")))
    return {"auditoria": st.get("auditoria"), "estado": st.get("estado_analisis"),
            "fila": [(f.get("verificacion") or "")[:28] for f in filas],
            "registro": [e.get("estado") for e in reg.get("publicaciones") or []],
            "retiradas": len(ret), "ficha": os.path.exists(os.path.join(c, "ficha.json")),
            "cierre": os.path.exists(os.path.join(c, "cierre_vigente.json"))}


for via in vias:
    c = T.copia_piloto(f"h5_{variante}_{via}")
    if variante in ("ambos", "sin_ficha"):
        os.remove(os.path.join(c, "ficha.json"))
    if variante in ("ambos", "sin_cierre"):
        os.remove(os.path.join(c, "cierre_vigente.json"))
    antes = foto(c)
    T.alterar(c, "valida_modificada")
    rc, out = T.primera_llamada(c, via)
    d = foto(c)
    vigente = d["auditoria"] == "APROBADO" or d["estado"] == "concluido"
    ult = out.strip().splitlines()[-1][:120] if out.strip() else ""
    print(f"{variante:9s} {via:8s} rc={rc:<3} antes: {antes['auditoria']}/{antes['estado']} · después: {d['auditoria']}/{d['estado']} · "
          f"fila {d['fila']} · registro {d['registro']} · antecedentes {d['retiradas']} · "
          f"{'APROBACIÓN INTERNA VIGENTE' if vigente else 'sin aprobación interna'}{' · EXCEPCIÓN' if 'Traceback' in out else ''} · {ult}")
