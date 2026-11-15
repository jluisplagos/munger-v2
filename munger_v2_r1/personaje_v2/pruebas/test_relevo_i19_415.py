#!/usr/bin/env python3
"""Batería del relevo caducado (4.15, hito 2, I19; obligatoria en «completa»).

Antes: con la auditoría pedida en el paso 13, si el material cambiaba (p. ej. verificacion_entradas.json escrito después de fijarlo), el
pipeline seguía esperando la solicitud antigua; una aprobación de esa solicitud se rechazaba y la corrección volvía a pedir el material
antiguo, hasta terminar en no_entregable (INCIDENCIAS_4_14.md, I19). Ahora el paso 13, mientras espera, compara el material fijado con el
vigente: si difieren, lo registra (estado_pipeline.json → relevos_caducados), repite la verificación (paso 12) y pide una auditoría del
material vigente (la solicitud antigua queda «sustituida»). Nada se aprueba con un material distinto.

Usa la empresa sintética y los agentes simulados de test_pipeline_sintetico.py (LibreOffice, en secuencia), en un directorio temporal.
La batería sintética no cambia: sus nombres están fijados por la línea de base v2.2.
Uso: python3 -B pruebas/test_relevo_i19_415.py
"""
import json
import os
import shutil
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
sys.dont_write_bytecode = True
import test_pipeline_sintetico as TS  # noqa: E402

RES = []


def paso(nombre, ok, detalle=""):
    RES.append((nombre, bool(ok)))
    print(("PASA " if ok else "FALLA") + " · " + nombre + (f" · {detalle}" if detalle else ""))


def t_relevo_caducado():
    """(4.15, hito 2, I19) Relevo caducado: con la auditoría pedida (paso 13, solicitud pendiente), verificacion_entradas.json se escribe
    después de fijar el material. Al relanzar el pipeline SIN «--desde», lo detecta, lo registra, repite la verificación (paso 12) y pide
    una auditoría del material vigente (la solicitud antigua queda «sustituida»). Una aprobación de la solicitud antigua no cierra nada;
    la del material vigente, sí. Trabaja en un directorio temporal."""
    import tempfile
    base0, TS.BASE = TS.BASE, tempfile.mkdtemp(prefix="relevo_i19_")
    try:
        c = TS.preparar("EmpresaX")
        reac = TS.reaccion_normal()
        rc = None
        for _ in range(30):
            r = subprocess.run([TS.PY, TS.PIPE, c], capture_output=True, text=True)
            rc = r.returncode
            if rc != 10:
                break
            nombre = open(os.path.join(c, "ESPERANDO.md"), encoding="utf-8").read().split("**")[1]
            if nombre == "verificacion":
                break
            reac(c, nombre)
        st = TS.estado(c)
        sol0 = [x for x in st.get("solicitudes_auditoria") or [] if x.get("estado") == "pendiente"]
        m0 = json.load(open(os.path.join(c, "material_auditoria.json"), encoding="utf-8"))["id"]
        paso("19 relevo: el pipeline espera la auditoría del material fijado con una solicitud pendiente", rc == 10 and len(sol0) == 1 and sol0[0]["material"] == m0, f"código {rc}")
        json.dump({"formato": "4.15", "entradas": [], "nota": "(prueba I19) registro escrito después de fijar el material"},
                  open(os.path.join(c, "verificacion_entradas.json"), "w", encoding="utf-8"), ensure_ascii=False)
        r = subprocess.run([TS.PY, TS.PIPE, c], capture_output=True, text=True)
        st = TS.estado(c)
        sols = st.get("solicitudes_auditoria") or []
        m1 = json.load(open(os.path.join(c, "material_auditoria.json"), encoding="utf-8"))["id"]
        rel = (st.get("relevos_caducados") or [{}])[-1]
        paso("19 relevo caducado sin «--desde»: se registra, se repite la verificación y se pide la auditoría del material vigente (la antigua, «sustituida»)",
             r.returncode == 10 and m1 != m0 and len(sols) == 2 and sols[0]["estado"] == "sustituida" and sols[1]["estado"] == "pendiente" and sols[1]["material"] == m1
             and rel.get("material_fijado") == m0 and rel.get("material_vigente") is not None and "verificacion_entradas.json" in (rel.get("archivos_cambiados") or [])
             and "relevo caducado" in (r.stdout + r.stderr) and st.get("paso") == 13 and st.get("esperando") == "13:auditoria.md",
             f"código {r.returncode} · material {m0} → {m1} · solicitudes {[(x['id'][:10], x['estado']) for x in sols]} · relevo {rel}")
        TS.AG.auditoria(c, "APROBADO", material=m0, solicitud=sols[0]["id"])  # responde a la solicitud ANTIGUA sobre el material antiguo
        r = subprocess.run([TS.PY, TS.PIPE, c], capture_output=True, text=True)
        st = TS.estado(c)
        paso("19 una aprobación de la solicitud antigua (material antiguo) no cierra nada", st.get("estado_analisis") is None and not os.path.exists(os.path.join(c, "cierre_vigente.json"))
             and not (os.path.exists(os.path.join(c, "ficha.json")) and (json.load(open(os.path.join(c, "ficha.json"), encoding="utf-8")).get("cierre"))), f"código {r.returncode} · estado {st.get('estado_analisis')}")
        rc, out = TS.correr(c, reac)
        st = TS.estado(c)
        paso("19 con la auditoría del material vigente, el análisis termina con su estado (relevo resuelto sin «--desde»)",
             rc == 0 and st.get("estado_analisis") in ("concluido", "pendiente_de_investigacion") and st.get("auditoria") == "APROBADO", f"código {rc} · estado {st.get('estado_analisis')} · auditoría {st.get('auditoria')}")
    finally:
        shutil.rmtree(TS.BASE, ignore_errors=True)
        TS.BASE = base0


if __name__ == "__main__":
    try:
        t_relevo_caducado()
    except Exception as e:  # noqa: BLE001
        import traceback
        traceback.print_exc()
        paso("excepción " + str(e)[:120], False)
    n = sum(ok for _, ok in RES)
    print(f"{n}/{len(RES)} pruebas del relevo caducado (4.15) PASAN")
    sys.exit(0 if n == len(RES) and n >= 4 else 1)
