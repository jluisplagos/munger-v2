#!/usr/bin/env python3
"""Correcciones de las entradas del expediente viscofan/Viscofan tras la revisión interna de la 4.13 (R5, R6 y R7). No toca ningún otro
expediente ni sobrescribe sin dejar el antecedente.

  - R5 · configuracion_economica.json: el texto de `naturaleza` (de la 4.12) decía que la base de Θ era el exceso «observado» de 40,813
    y que SRF solo estaba definida hasta λ = 1,1413. Las dos cifras son del perímetro «Caja». Con el perímetro NIIF 16 del expediente
    son 64,923 y 1,2011 (viscofan/resultados/dominios_perimetro.md). Se corrige el texto (cambio editorial: la huella económica no
    cambia).
  - R7 · fase1_v63.json y fase1_metadatos.json: el múltiplo EV/EBITDA (Análisis!C42 = 9,9) y su evidencia venían de la etapa 1, con la
    capitalización del 6-oct-2026 (2.444,4) y la deuda y el EBITDA del primer semestre de 2026. Se recalcula con la capitalización de
    las entradas (54,70 × 45,479209 = 2.487,7) y el balance y el EBITDA de 2025 (la base). El texto de periodos de la lista de
    comprobación (Control maestro D88, «precio 6-oct-26») se sustituye por el de las entradas. Los dos anteriores quedan en el registro
    de la fase 1 (`evidencias_sustituidas`).
  - R6 y C97 · fase A y fase B: se rehacen con agentes reales. La fase B se rehace porque la referencia mecánica del S2C se ancla ahora
    en el S2C histórico del perímetro NIIF 16. La fase A se rehace por el error de C97 que encontró la auditoría y porque cambian sus
    entradas (C42). Las salidas anteriores (extracción reutilizada aparte) se apartan a antecedentes/ejecucion_1_4_13/.
Uso (desde munger_v2_r1/): python3 -I …/scripts/corregir_viscofan_revision_4_13.py · Escribe viscofan/resultados/correccion_revision_4_13.json y .md.
"""
import datetime as dt
import hashlib
import json
import os
import shutil
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
E413 = os.path.dirname(AQUI)
PV = os.path.abspath(os.path.join(E413, "..", ".."))
C = os.path.join(E413, "viscofan", "Viscofan")
sys.path.insert(0, os.path.join(PV, "scripts"))


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def main():
    import entradas_economicas as EE
    from openpyxl import load_workbook
    reg = {"fecha": dt.datetime.now().isoformat(timespec="seconds"), "cambios": {}}
    # R5
    pc = os.path.join(C, "configuracion_economica.json")
    conf = json.load(open(pc, encoding="utf-8"))
    h0 = EE.huella_configuracion(conf)
    nat0 = conf["naturaleza"]
    a1 = "exceso de capex sobre D&A OBSERVADO en 2021–2025 (40,813)"
    b1 = ("exceso de la inversión sobre la D&A OBSERVADO en 2021–2025 (con el perímetro NIIF 16 del expediente, 64,923: capex + altas de derechos "
          "de uso − D&A; con «Caja» era 40,813)")
    a2 = "SRF solo estaría definida hasta λ = 1,1413"
    b2 = "SRF solo estaría definida hasta λ = 1,2011 con el perímetro NIIF 16 (1,1413 con «Caja»; viscofan/resultados/dominios_perimetro.md)"
    assert a1 in nat0 and a2 in nat0, "el texto de la naturaleza no es el esperado"
    conf["naturaleza"] = nat0.replace(a1, b1).replace(a2, b2)
    json.dump(conf, open(pc, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    assert EE.huella_configuracion(conf) == h0
    reg["cambios"]["configuracion_economica.json"] = {"naturaleza": [[a1, b1], [a2, b2]], "huella_economica": h0}
    # R7
    wb = load_workbook(os.path.join(C, "Viscofan_v63_datos.xlsx"), data_only=True, read_only=True)
    H = wb["Historia"]
    L = {r: H.cell(r, 12).value for r in (5, 7, 8, 22, 23, 24, 26)}
    assert L[5] == 2025
    cap = round(54.70 * 45.479209, 1)
    dfn = L[22] + L[23] - L[24]
    ev = cap + dfn + L[26]
    ebitda = L[7] + L[8]
    mult = round(ev / ebitda, 2)
    c42 = {"valor": mult, "fuente": (f"Cálculo: EV {ev:.1f} = capitalización {cap:.1f} (Análisis C41: 54,70 € del 3-nov-2026 × 45,479209 millones) + deuda financiera "
                                     f"{L[22]:.3f} + arrendamientos {L[23]:.3f} − caja {L[24]:.3f} (Historia L22–L24, 31-dic-2025) + minoritarios {L[26]:.3f} (L26); "
                                     f"÷ EBITDA 2025 {ebitda:.3f} = EBIT {L[7]:.3f} + D&A {L[8]:.3f} (Historia L7 y L8)"),
           "periodo": "precio del 3-nov-2026; balance a 31-dic-2025 y EBITDA de 2025 (la base): fechas separadas", "unidad": "x",
           "nota": ("(4.13) Sustituye al 9,9 de la etapa 1 (EV a 6-oct-2026 con capitalización 2.444,4, deuda a 30-jun-2026 y EBITDA de los doce meses "
                    "a jun-2026). Solo lectura de contraste: no entra en el motor B.")}
    d88 = ("Balance a 31-dic-2025 (base del modelo: Historia L22–L26); EBITDA y FCF de 2025; C26 agregado 2021–2025; C60 2020→2025; precio del "
           "3-nov-2026 (posterior a la base; fechas separadas); medias del FCF base (C46–C50) de 2023–2025. Evidencia heredada de la etapa 1 no "
           "actualizada, con su período declarado en su fila: C24, C31, C33, C34, C40, C53 y C54 (datos del primer semestre de 2026 o de los doce "
           "meses a jun-2026) y C38 (referencia externa del 28-sep-2026). Son celdas de contraste: no entran en el motor B.")
    e88 = ("Período de C46–C50 fijado por el inversor (23-oct-2026: 2023–2025). Queda por decidir si las celdas de contraste con datos de 2026 "
           "se rehacen sobre 2025.")
    for n in ("fase1_v63.json", "fase1_metadatos.json"):
        p = os.path.join(C, n)
        d = json.load(open(p, encoding="utf-8"))
        antes = {"analisis.C42": (d.get("analisis") or {}).get("C42"), "control_maestro_textos": d.get("control_maestro_textos")}
        d.setdefault("analisis", {})["C42"] = c42
        d.setdefault("control_maestro_textos", {}).update({"D88": d88, "E88": e88})
        json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        reg["cambios"][n] = {"antes": antes, "despues": {"analisis.C42": c42, "control_maestro_textos": {"D88": d88, "E88": e88}}}
    # fases A, B y C anteriores: antecedentes (no se borran)
    ant = os.path.join(E413, "viscofan", "antecedentes", "ejecucion_1_4_13")
    os.makedirs(ant, exist_ok=True)
    movidos = []
    for n in ("fase_a.json", "fase_a.md", "fase_b.json", "fase_b.md", "fase_c.json", "fase_c.md", "auditoria.md"):
        p = os.path.join(C, n)
        if os.path.exists(p):
            shutil.copy2(p, os.path.join(ant, n))
            movidos.append({n: sha(p)})
            os.remove(p)
    reg["apartados_a_antecedentes"] = movidos
    # la extracción se reutiliza otra vez: lee texto/ y no cita C42, la lista de períodos ni D4 (comprobado con grep en extracto_v63.md).
    # El pipeline solo consume una salida más nueva que la ya consumida: se retira su marca de consumo y queda registrado aquí
    pe = os.path.join(C, "estado_pipeline.json")
    st = json.load(open(pe, encoding="utf-8"))
    reg["extraccion_reutilizada"] = {"sha256": sha(os.path.join(C, "extracto_v63.md")), "marca_de_consumo_retirada": (st.get("consumidos") or {}).pop("extracto_v63.md", None)}
    json.dump(st, open(pe, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    reg["motivo_apartados"] = ("fase A: error de C97 (auditoría 1) y C42 cambiado en sus entradas; fase B: la referencia del S2C se ancla en el perímetro NIIF 16 "
                               "(revisión interna R6); fase C: depende de las dos. La extracción (reutilizada de la 4.12) se conserva: sus entradas no cambian")
    os.makedirs(os.path.join(E413, "viscofan", "resultados"), exist_ok=True)
    json.dump(reg, open(os.path.join(E413, "viscofan", "resultados", "correccion_revision_4_13.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    md = ["# Viscofan · correcciones de las entradas tras la revisión interna de la 4.13", "",
          f"- **R5 · configuración (editorial; huella económica `{h0[:16]}…` igual).** El exceso «observado» pasa a decir 64,923 con NIIF 16 (40,813 con «Caja»). La cota de SRF pasa a 1,2011 con NIIF 16 (1,1413 con «Caja»).",
          f"- **R7 · EV/EBITDA (C42).** Pasa de 9,9 (etapa 1: capitalización del 6-oct-2026 y datos del primer semestre de 2026) a **{mult}**: EV {ev:.1f} ÷ EBITDA 2025 {ebitda:.3f}, con la capitalización de las entradas y el balance de la base. Es una lectura de contraste: no entra en el motor B.",
          "- **R7 · lista de comprobación (D88 y E88).** El texto de períodos dice ahora las fechas de las entradas. Se declaran las celdas de contraste que conservan datos de 2026 de la etapa 1 (C24, C31, C33, C34, C38, C40, C53 y C54). La acción pendiente ya no pide fijar C46–C50, que el inversor fijó el 23-oct-2026.",
          "- **R7 · fecha de análisis (D4).** `rellenar_fase1_v63.py` escribe ahora también su período; antes quedaba el «7-oct-2026» de la etapa 1.",
          "- **Conciliación de acciones.** La N del modelo no viene de la etapa 1: la introdujo la fase 1 del pipeline V2 (`fuentes/CONCILIACION_ACCIONES_VISCOFAN_4_13.md`, antecedente bajo la tabla del §3).",
          f"- **Extracción reutilizada otra vez** (`extracto_v63.md`, `{reg['extraccion_reutilizada']['sha256'][:16]}…`): lee los informes y no cita ninguna de las celdas que cambian. Se retira su marca de consumo para que el pipeline la vuelva a consumir.",
          f"- **Fases A, B y C y auditoría anteriores, apartadas** a `antecedentes/ejecucion_1_4_13/` ({len(movidos)} archivos): se rehacen con agentes reales. {reg['motivo_apartados']}."]
    open(os.path.join(E413, "viscofan", "resultados", "correccion_revision_4_13.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main()
