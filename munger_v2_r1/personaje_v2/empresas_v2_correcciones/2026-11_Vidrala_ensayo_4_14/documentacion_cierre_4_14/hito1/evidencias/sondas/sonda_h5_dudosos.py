"""Casos dudosos de H5: (1) sin ficha, sin cierre y sin registro de publicaciones ni respaldo; (2) restaurar archivos antiguos tras la retirada,
solo las salidas o también el estado del pipeline. Uso: python3 -B sonda_h5_dudosos.py PERSONAJE_V2"""
import csv, glob, json, os, shutil, sys
PV = os.path.abspath(sys.argv[1])
sys.path.insert(0, os.path.join(PV, "pruebas")); sys.path.insert(0, os.path.join(PV, "scripts"))
import test_integracion_v64 as T
import cierre_v2 as CIE
os.makedirs(T.TMP, exist_ok=True)


def foto(c):
    st = json.load(open(os.path.join(c, "estado_pipeline.json"), encoding="utf-8"))
    filas = list(csv.DictReader(open(os.path.join(os.path.dirname(c), "resumen_v2.csv"), encoding="utf-8", newline="")))
    p = os.path.join(c, CIE.REGISTRO_RESUMEN)
    reg = json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}
    return (f"{st.get('auditoria')}/{st.get('estado_analisis')} · fila {[(f.get('verificacion') or '')[:24] for f in filas]} · "
            f"registro {[e.get('estado') for e in reg.get('publicaciones') or []]} · antecedentes {len(glob.glob(os.path.join(c, 'historial_cierres', '*', 'RETIRADA.json')))}")


for via in ("pipeline", "ficha", "informe", "resumen"):
    c = T.copia_piloto(f"dud1_{via}")
    for n in ("ficha.json", "cierre_vigente.json", CIE.REGISTRO_RESUMEN, CIE.RESPALDO_RESUMEN):
        os.remove(os.path.join(c, n))
    rc, out = T.primera_llamada(c, via)
    print(f"(1) sin registro ni respaldo {via:8s} rc={rc} · {foto(c)} · {out.strip().splitlines()[-1][:100] if out.strip() else ''}")

for via in ("ficha", "informe", "resumen"):
    for con_estado in (False, True):
        c = T.copia_piloto(f"dud2_{via}_{int(con_estado)}")
        guard = os.path.join(os.path.dirname(c), "_guardados"); os.makedirs(guard)
        for n in ("ficha.json", "cierre_vigente.json", "informe.md", "estado_pipeline.json"):
            shutil.copy2(os.path.join(c, n), os.path.join(guard, n))
        os.remove(os.path.join(c, "ficha.json")); os.remove(os.path.join(c, "cierre_vigente.json"))
        rc1, _ = T.primera_llamada(c, via)
        tras = foto(c)
        for n in ("ficha.json", "cierre_vigente.json", "informe.md") + (("estado_pipeline.json",) if con_estado else ()):
            shutil.copy2(os.path.join(guard, n), os.path.join(c, n))
        rc2, out2 = T.primera_llamada(c, via)
        rc3, _ = T.primera_llamada(c, "resumen")
        print(f"(2) restaurar {'salidas+estado' if con_estado else 'salidas':15s} {via:8s} rc1={rc1} · tras retirar: {tras} · rc2={rc2} rc3={rc3} · tras restaurar: {foto(c)} · {out2.strip().splitlines()[-1][:90] if out2.strip() else ''}")
