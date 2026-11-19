#!/usr/bin/env python3
"""(V-CIRC) Diagnóstico de VINCI con la normalización declarada del circulante, sobre una COPIA del expediente de examen vinci/Vinci (que no se toca):
  1. la declaración F1 del expediente más `normalizacion_circulante` (decisión V-CIRC (a) de la persona responsable, 19-nov-2026: circulante a 0 en
     2021–2025, los años que usa la reinversión: la ventana de f, 2023–2025, y los cinco del ancla de S2C, 2021–2025), escrita solo en la copia;
  2. la capa F1 sobre el libro del expediente (V6.3.1 F1, recalc/Vinci_v63_datos.xlsx), sin y con la declaración;
  3. el libro V6.3.2 F1: las entradas del libro de datos del expediente trasladadas a la plantilla V6.3.2 F1 (la misma vía que las pruebas de la
     plantilla), la declaración aplicada con f1_libro_v631.aplicar (como el paso 2 del pipeline), recalculado con LibreOffice, verificado con
     verificar_v632.py frente a su referencia y evaluado por la capa (oráculo).
Es un diagnóstico (antes de la fase A: sin palancas, como la previsión del coordinador), no el paso 7 de un expediente.

Uso (desde munger_v2_r1/; LibreOffice: flock /home/user/e_work/libreoffice.lock):
  python3 -I …/f1_circulante/scripts/diagnostico_vinci_circulante.py EXPEDIENTE_VINCI DESTINO [--salida CARPETA_RESULTADOS]
DESTINO: carpeta nueva fuera del repositorio (se borra al final, salvo --conservar). Escribe diagnostico_vinci_circulante.json y .md en la carpeta de
resultados (por omisión, la de f1_circulante).
"""
import copy
import datetime as dt
import hashlib
import json
import os
import shutil
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", "..", "..", "..", ".."))   # munger_v2_r1
PV = os.path.join(RAIZ, "personaje_v2")
V632 = os.path.join(RAIZ, "v6", "v632_f1")
sys.path.insert(0, os.path.join(PV, "scripts"))
import motor_a_f1 as M  # noqa: E402
import f1_libro_v631 as F  # noqa: E402

REGISTRO = {"fecha": "2026-11-19", "persona": "persona responsable del proyecto (decisión registrada; no se firma aquí)", "motivo": M._REG_CIRC}
FUNDAMENTO = ("Decisión V-CIRC (a) de la persona responsable, 19-nov-2026 (munger-v2-evidencias-mistral, coordinacion/cierre_v2/DECISIONES_PARA_EL_USUARIO.md:"
              "134): «circulante a 0 también en la reinversión, con un mecanismo declarado (ni entradas ni salidas de circulante)». La caja base ya lo excluye: "
              "C46 = CFO − circulante por la decisión del inversor de la etapa 1 (Control maestro M43; conciliacion_fcf_base, componente C46, −2.090 = media "
              "2023–2025 de la fila 14). Años: los que usa la reinversión, la ventana de f (2023–2025) y los cinco del ancla de S2C (2021–2025).")


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def run(args):
    r = subprocess.run(args, capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr).strip()


def resumen(r):
    cd = r.get("calculo_perimetro_declarado") or {}
    return {"utilizable": r.get("utilizable_para_conclusion"), "estado_propuesto": r.get("estado_propuesto"),
            "bloquean": sorted({g["id"] for g in r["guardas"] if g["salta"] and g["severidad"] == "BLOQUEA"}),
            "avisos": sorted({g["id"] for g in r["guardas"] if g["salta"] and g["severidad"] in ("AVISO", "INFORMA")}),
            "f": cd.get("f"), "flujo_sin_crecimiento": cd.get("flujo_sin_crecimiento"), "reinversion_media": cd.get("reinversion_media"),
            "ancla_s2c_E4": cd.get("ancla_s2c_E4"), "tau_proyeccion": cd.get("tau_proyeccion"), "m0": cd.get("m0"),
            "K3c": next((g["detalle"] for g in r["guardas"] if g["id"] == "F1-K3c"), None),
            "F1-CIRC": next((g["detalle"] for g in r["guardas"] if g["id"] == "F1-CIRC"), None),
            "F1-LIBRO": next((g["detalle"] for g in r["guardas"] if g["id"] == "F1-LIBRO"), None),
            "K3_lineas": [(x["partida"], x["mm"], x["clase"]) for x in (cd.get("K3") or {}).get("lineas") or []],
            "diagnostico_por_perimetro": {k: {"f": v["f"], "flujo_sin_crecimiento": v["flujo_sin_crecimiento"], "ancla_s2c_E4": v["ancla_s2c_E4"]}
                                          for k, v in (r.get("diagnostico_por_perimetro") or {}).items()}}


def main():
    a = sys.argv[1:]
    if len(a) < 2:
        print(__doc__)
        return 2
    exp, dest = os.path.abspath(a[0]), os.path.abspath(a[1])
    salida = a[a.index("--salida") + 1] if "--salida" in a else os.path.join(os.path.dirname(AQUI), "resultados")
    if os.path.exists(dest):
        raise SystemExit(f"{dest} ya existe")
    if os.path.commonpath([dest, RAIZ]) == RAIZ:
        raise SystemExit("DESTINO va fuera del repositorio")
    os.makedirs(dest)
    try:
        c = os.path.join(dest, "Vinci")
        shutil.copytree(exp, c, ignore=shutil.ignore_patterns("pdf", ".lo_perfil", "__pycache__"))
        d0 = json.load(open(os.path.join(c, "motor_a_f1.json"), encoding="utf-8"))
        d1 = copy.deepcopy(d0)
        d1["normalizacion_circulante"] = {"regla": M.REGLA_CIRCULANTE, "anios": [2021, 2022, 2023, 2024, 2025], "fundamento": FUNDAMENTO, "registro": REGISTRO}
        json.dump(d1, open(os.path.join(c, "motor_a_f1.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)   # solo en la copia
        libro631 = os.path.join(c, "recalc", "Vinci_v63_datos.xlsx")
        L631 = M.leer_libro(libro631)
        r_sin = M.evaluar(L631, d0, carpeta=c)
        r_631 = M.evaluar(L631, d1, carpeta=c)
        # el libro V6.3.2 F1: entradas del libro de datos del expediente → plantilla V6.3.2 → declaración (como el paso 2) → LibreOffice
        sys.path.insert(0, os.path.join(V632, "scripts"))
        import trasladar_entradas as T   # el de la V6.3.2 (inventario con la normalización del circulante)
        plantilla = os.path.join(V632, "entregables", "Plantilla_V6.3.2_F1.xlsx")
        datos = os.path.join(c, "Vinci_v63_datos.xlsx")
        base = os.path.join(dest, "Vinci_V6.3.2_entradas.xlsx")
        n_ent, _ = T.trasladar(datos, plantilla, base)
        libro632 = os.path.join(dest, "Vinci_v63_datos.xlsx")
        cel = F.aplicar(base, libro632, os.path.join(c, "motor_a_f1.json"))
        rc_v, txt_v = run([sys.executable, "-I", os.path.join(V632, "scripts", "verificar_v632.py"), libro632, os.path.join(V632, "referencia", "referencia_V6.3.2_F1.json")])
        rc, txt = run(["bash", os.path.join(PV, "scripts", "recalc.sh"), libro632, os.path.join(dest, "recalc"), os.path.join(dest, "_perfil_lo")])
        rec = os.path.join(dest, "recalc", "Vinci_v63_datos.xlsx")
        if rc != 0 or not os.path.exists(rec):
            raise SystemExit(f"LibreOffice no recalculó el libro V6.3.2: {txt[-300:]}")
        L632 = M.leer_libro(rec)
        r_632 = M.evaluar(L632, d1, carpeta=c)
        from openpyxl import load_workbook
        wb = load_workbook(rec, data_only=True)
        h, mo = wb["Historia"], wb["Motor"]
        libro = {"C58_f": h["C58"].value, "C53_ancla": h["C53"].value, "C76_reinversion_media": h["C76"].value, "C70_FCF_base": h["C70"].value,
                 "C97_normalizacion_efectiva": h["C97"].value, "C93_regla": h["C93"].value,
                 "fila_14_circulante_publicado": {str(h[f"{x}5"].value): h[f"{x}14"].value for x in "CDEFGHIJKL"},
                 "fila_94_anios_normalizados": {str(h[f"{x}5"].value): h[f"{x}94"].value for x in "CDEFGHIJKL"},
                 "fila_95_excluido": {str(h[f"{x}5"].value): h[f"{x}95"].value for x in "CDEFGHIJKL"},
                 "fila_96_circulante_de_la_reinversion": {str(h[f"{x}5"].value): h[f"{x}96"].value for x in "CDEFGHIJKL"},
                 "fila_30_reinversion_neta_organica": {str(h[f"{x}5"].value): h[f"{x}30"].value for x in "CDEFGHIJKL"},
                 "Motor_V05": [mo["D205"].value, mo["F205"].value], "Palancas_F16_ancla_mostrada": wb["Palancas"]["F16"].value}
        wb.close()
        w0 = load_workbook(libro631, data_only=True)["Historia"]
        libro_631 = {"C58_f": w0["C58"].value, "C53_ancla": w0["C53"].value, "C76_reinversion_media": w0["C76"].value}
        cd = r_632.get("calculo_perimetro_declarado") or {}
        res = {"fecha": dt.date.today().isoformat(), "que_es": ("DIAGNÓSTICO sobre una copia de vinci/Vinci con la normalización del circulante declarada (decisión "
                                                                "V-CIRC (a)); antes de la fase A, sin palancas: no es el paso 7 ni una conclusión; no apto para dinero real"),
               "expediente_origen": os.path.relpath(exp, RAIZ) if os.path.commonpath([exp, RAIZ]) == RAIZ else exp,
               "libro_V6.3.1_sha256": sha(libro631), "declaracion_original_sha256": M.huella_declaracion(d0), "declaracion_con_la_normalizacion_sha256": M.huella_declaracion(d1),
               "normalizacion_declarada": d1["normalizacion_circulante"], "codigo": M.VERSION,
               "capa_libro_V6.3.1_sin_la_declaracion": resumen(r_sin), "capa_libro_V6.3.1_con_la_declaracion": resumen(r_631),
               "libro_V6.3.2": {"entradas_trasladadas": n_ent, "celdas_escritas_por_aplicar": {k: v for k, v in cel.items() if v is not None and k[9] != "M"},
                                "verificador_antes_de_recalcular": txt_v.splitlines()[:2], "verificador_codigo": rc_v, "valores_recalculados": libro,
                                "libro_V6.3.1_del_expediente": libro_631},
               "capa_libro_V6.3.2_con_la_declaracion": resumen(r_632),
               "oraculo": {"f_libro_menos_capa": (libro["C58_f"] - cd["f"]) if (libro["C58_f"] is not None and cd.get("f") is not None) else None,
                           "ancla_libro_menos_capa": (libro["C53_ancla"] - cd["ancla_s2c_E4"]) if (libro["C53_ancla"] is not None and cd.get("ancla_s2c_E4") is not None) else None,
                           "reinversion_libro_menos_capa": (libro["C76_reinversion_media"] - cd["reinversion_media"]) if cd.get("reinversion_media") is not None else None,
                           "F1_LIBRO": next((g["detalle"] for g in r_632["guardas"] if g["id"] == "F1-LIBRO"), None),
                           "F1_REPLICA": next((g["detalle"] for g in r_632["guardas"] if g["id"] == "F1-REPLICA"), None)},
               "normalizacion_circulante_del_resultado": r_632.get("normalizacion_circulante")}
        os.makedirs(salida, exist_ok=True)
        json.dump(res, open(os.path.join(salida, "diagnostico_vinci_circulante.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
        s0, s1, s2 = res["capa_libro_V6.3.1_sin_la_declaracion"], res["capa_libro_V6.3.1_con_la_declaracion"], res["capa_libro_V6.3.2_con_la_declaracion"]
        md = [f"# VINCI · normalización declarada del circulante (V-CIRC) · diagnóstico sobre una copia", "",
              f"{res['fecha']} · {res['que_es']}.", "", f"Libro del expediente (V6.3.1 F1) `{res['libro_V6.3.1_sha256'][:16]}…`; código de la capa: {M.VERSION}.", "",
              "| | f | reinversión media | flujo sin crecimiento | ancla S2C | bloquean |", "|---|---|---|---|---|---|"]
        for nom, s in (("libro V6.3.1, sin la declaración (estado actual)", s0), ("libro V6.3.1, con la declaración", s1), ("libro V6.3.2 F1, con la declaración", s2)):
            md.append(f"| {nom} | {s['f']} | {s['reinversion_media']} | {s['flujo_sin_crecimiento']} | {s['ancla_s2c_E4']} | {', '.join(s['bloquean']) or '—'} |")
        md += ["", f"- Libro V6.3.2 recalculado: C58 = {libro['C58_f']} · C53 = {libro['C53_ancla']} · C76 = {libro['C76_reinversion_media']} · C97 = {libro['C97_normalizacion_efectiva']}"
               f" · Motor V05 = {libro['Motor_V05'][0]} · Palancas F16 (ancla que ven las fases) = {libro['Palancas_F16_ancla_mostrada']}",
               f"- Libro − capa: f {res['oraculo']['f_libro_menos_capa']} · ancla {res['oraculo']['ancla_libro_menos_capa']} · reinversión {res['oraculo']['reinversion_libro_menos_capa']}",
               f"- F1-LIBRO: {res['oraculo']['F1_LIBRO']}", f"- F1-REPLICA: {res['oraculo']['F1_REPLICA']}",
               f"- F1-K3c (V6.3.2): {s2['K3c']}", f"- F1-CIRC (V6.3.2): {s2['F1-CIRC']}", f"- Avisos (V6.3.2): {', '.join(s2['avisos'])}",
               f"- Verificador del libro V6.3.2 con las entradas (antes de recalcular): {' · '.join(res['libro_V6.3.2']['verificador_antes_de_recalcular'])}",
               "", "## K3 · perímetro declarado (libro V6.3.2)", "", "| Partida | mm | Clase |", "|---|---|---|"]
        md += [f"| {p} | {x:.3f} | {k} |" for p, x, k in s2["K3_lineas"]]
        md += ["", "## Diagnóstico por perímetro (libro V6.3.2, con la normalización)", "", "| Perímetro | f | flujo sin crecimiento | ancla |", "|---|---|---|---|"]
        md += [f"| {k} | {v['f']} | {v['flujo_sin_crecimiento']} | {v['ancla_s2c_E4']} |" for k, v in s2["diagnostico_por_perimetro"].items()]
        open(os.path.join(salida, "diagnostico_vinci_circulante.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
        print("\n".join(md))
        return 0
    finally:
        if "--conservar" not in a:
            shutil.rmtree(dest, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
