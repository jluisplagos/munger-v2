#!/usr/bin/env python3
"""Control de la entrega 4.14 (encargo de cierre §11; solo lectura). Comprueba, sobre una descompresión del paquete:
  1. VERSION identifica la 4.14 y el registro de la reparación 4.13.1 se conserva.
  2. Los tres expedientes finales (Viscofan y Vidrala con sus decisiones, Elis con E6) están en el paso 14 con el estado esperado, su
     auditoría vigente es APROBADO y responde a la última solicitud y al material vigente (huellas de material_auditoria.json).
  3. Cada registro de verificación de las entradas es apto (verificacion_entradas.comprobar), con cobertura completa del universo.
  4. El precio de Sí de precio.json es el esperado (con 1e-9) y la acción de la ficha también.
  5. Los cálculos de efectos separados reproducen su expediente de partida y, en Elis, el caso «todo» reproduce el expediente nuevo.
  6. Los expedientes anteriores (controles 4.13, ramas 4.14 y elis_motor_A) existen y ninguno es posterior a su expediente de decisiones.
  7. Los documentos del cierre (decisiones, incidencias, matriz del alcance, hitos) están presentes.
No ejecuta el pipeline, no recalcula con LibreOffice y no escribe nada. Código 0 si todo pasa.
Uso (desde munger_v2_r1/): python3 -I -B personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_14/scripts/comprobar_entrega_4_14.py"""
import hashlib
import json
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
E414 = os.path.dirname(AQUI)
PV = os.path.abspath(os.path.join(E414, "..", ".."))
RAIZ = os.path.dirname(PV)
sys.path.insert(0, os.path.join(PV, "scripts"))

ESPERADO = {
    "viscofan_decisiones/Viscofan": {"estado": "concluido", "precio_si": 39.79819353512519, "accion": "esperar"},
    "vidrala_decisiones/Vidrala": {"estado": "concluido", "precio_si": 56.002005168244615, "accion": "esperar"},
    "elis_decisiones/Elis": {"estado": "pendiente_de_datos", "precio_si": 7.30205532309094, "accion": None},
}
ANTERIORES = {"viscofan_decisiones/Viscofan": "viscofan/Viscofan", "vidrala_decisiones/Vidrala": "vidrala/Vidrala",
              "elis_decisiones/Elis": "elis_motor_A/Elis"}
DOCS = ["documentacion_cierre_4_14/DECISIONES_ENTRADAS_4_14.md", "documentacion_cierre_4_14/INCIDENCIAS_4_14.md",
        "documentacion_cierre_4_14/MATRIZ_ALCANCE_4_14.md", "documentacion_cierre_4_14/HALLAZGO_MOTOR_A_NIIF16_4_14.md",
        "documentacion_cierre_4_14/HITO_2.md", "REGISTRO_ENTREGA_4.14.md"]
resultados = []


def ok(nombre, cond, detalle=""):
    resultados.append((bool(cond), nombre, detalle))


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def main():
    import verificacion_entradas as VE
    v = open(os.path.join(RAIZ, "VERSION"), encoding="utf-8").read()
    ok("VERSION identifica la entrega 4.14", "entrega 4.14" in v, v[:90])
    ok("se conserva el registro de la reparación 4.13.1", any("4_13_1" in f or "4.13.1" in f for _, _, fs in os.walk(os.path.join(E414, "documentacion_cierre_4_14")) for f in fs))
    for rel, esp in ESPERADO.items():
        d = os.path.join(E414, rel)
        st = json.load(open(os.path.join(d, "estado_pipeline.json"), encoding="utf-8"))
        ok(f"{rel}: paso 14 y estado {esp['estado']}", st.get("paso") == 14 and st.get("estado_analisis") == esp["estado"], f"{st.get('paso')} · {st.get('estado_analisis')}")
        txt = open(os.path.join(d, "auditoria.md"), encoding="utf-8-sig").read()
        mat = json.load(open(os.path.join(d, "material_auditoria.json"), encoding="utf-8"))
        sol = json.load(open(os.path.join(d, "solicitud_auditoria.json"), encoding="utf-8"))
        ver = re.findall(r"^Veredicto: (\S+)\s*$", txt, re.M)
        ok(f"{rel}: auditoría APROBADO, una sola línea de veredicto", ver == ["APROBADO"] and st.get("auditoria") == "APROBADO", str(ver))
        ok(f"{rel}: la auditoría responde a la solicitud y al material vigentes",
           f"Material auditado: {mat.get('id')}" in txt and f"Solicitud de auditoría: {sol.get('id')}" in txt, f"{mat.get('id')} · {sol.get('id')}")
        dif = [a for a, h in (mat.get("archivos") or {}).items() if not os.path.exists(os.path.join(d, a)) or sha(os.path.join(d, a)) != (h if isinstance(h, str) else (h or {}).get("sha256"))]
        ok(f"{rel}: el material auditado no ha cambiado ({len(mat.get('archivos') or {})} archivos)", not dif, ", ".join(dif[:5]))
        r = VE.comprobar(d)
        ok(f"{rel}: verificación de las entradas apta, universo completo", r["apto_por_entradas"] and r.get("comprobadas_universo") == r["universo"],
           f"{r.get('comprobadas_universo')} de {r['universo']} · pendientes {len(r['pendientes'])} · discrepancias {len(r['discrepancias'])}")
        pr = json.load(open(os.path.join(d, "precio.json"), encoding="utf-8"))
        fi = json.load(open(os.path.join(d, "ficha.json"), encoding="utf-8"))
        ok(f"{rel}: precio de Sí {esp['precio_si']:.5f}", abs((pr.get("precio_si") or 0) - esp["precio_si"]) <= 1e-9, str(pr.get("precio_si")))
        ok(f"{rel}: acción de la ficha {esp['accion']}", (fi.get("decision") or {}).get("accion") == esp["accion"], str((fi.get("decision") or {}).get("accion")))
        a = os.path.join(E414, ANTERIORES[rel])
        import datetime as dt
        t_nuevo = dt.datetime.fromisoformat(st["inicio"]).timestamp()  # inicio del pipeline del expediente nuevo (hora local)
        t_ant = max(os.path.getmtime(os.path.join(rr, f)) for rr, _, fs in os.walk(a) for f in fs) if os.path.isdir(a) else None
        ok(f"{rel}: se conserva el expediente anterior {ANTERIORES[rel]} (ningún archivo posterior al inicio del nuevo, {st['inicio']})",
           t_ant is not None and t_ant <= t_nuevo + 1, dt.datetime.fromtimestamp(t_ant).isoformat(timespec="seconds") if t_ant else "no existe")
    res = os.path.join(E414, "resultados")
    ev = json.load(open(os.path.join(res, "efecto_decisiones_viscofan.json"), encoding="utf-8"))
    ok("efectos de Viscofan (D3, E1): reproducen la rama", ev.get("reproduce") is True)
    ee = json.load(open(os.path.join(res, "efecto_decisiones_elis_E6.json"), encoding="utf-8"))
    ok("efectos de Elis (E6): reproducen el anterior y el caso «todo» reproduce el expediente nuevo",
       ee.get("reproduce_el_anterior") is True and isinstance(ee.get("todo_frente_al_expediente_nuevo"), (int, float)) and abs(ee["todo_frente_al_expediente_nuevo"]) <= 1e-9)
    ec = json.load(open(os.path.join(res, "efecto_correcciones_vidrala.json"), encoding="utf-8"))
    ok("efectos de Vidrala: reproducen el caso activo 4.13", ec.get("reproduce_el_caso_activo") is True)
    for p in DOCS:
        ok(f"documento presente: {p}", os.path.exists(os.path.join(E414, p)))
    for c, n, dt in resultados:
        print(f"{'PASA ' if c else 'FALLA'} · {n}" + (f" · {dt}" if dt else ""))
    n_ok = sum(1 for c, _, _ in resultados if c)
    print(f"{n_ok}/{len(resultados)} comprobaciones de la entrega 4.14 PASAN")
    return 0 if n_ok == len(resultados) else 1


if __name__ == "__main__":
    sys.exit(main())
