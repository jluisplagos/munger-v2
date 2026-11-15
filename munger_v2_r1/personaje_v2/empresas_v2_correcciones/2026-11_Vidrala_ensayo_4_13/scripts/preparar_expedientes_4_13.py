#!/usr/bin/env python3
"""Prepara los expedientes que la 4.13 regenera (Hito 4; encargo 4.13 §9: «se reutilizarán fuentes y fases válidas; se reabrirán
únicamente las afectadas conforme a dependencias»). No toca los expedientes de la 4.12 ni sobrescribe nada.

1. vidrala_condicionado/Vidrala y vidrala_bloqueo/Vidrala. Son copias de los cierres de la 4.12, sin el perfil de LibreOffice:
   - El registro de publicaciones del resumen se reubica dentro de la carpeta nueva (la copia nunca toca el resumen de la 4.12).
   - En configuracion_economica.json solo cambian textos (cambio editorial; la huella económica no cambia):
     - la justificación de PM1.roic_terminal recoge la condición correcta de Q-ROIC1 (4.13 §8; CORRECCIONES_ECONOMICAS_VIDRALA_4_13.md);
     - la naturaleza lleva una nota de la 4.13.
   - Plantilla V6.4: Vidrala no tiene conciliadas las altas de derechos de uso (pendiente declarado), así que no se cambia de plantilla.
   - La aprobación copiada no vale. El material cambia y la primera llamada del pipeline la retira. Después, `--desde 10` recalcula las
     variantes (formato 4.13: contrastes aislados y avisos de dominio de todas las variantes) y pide una fase C y una auditoría nuevas
     con agentes reales. Las fases A y B no dependen de nada de lo que cambia y se conservan.
2. viscofan/Viscofan. Es un expediente NUEVO con la plantilla V6.4.1 experimental: un expediente solo se ejecuta con su plantilla.
   - Lleva las entradas de partida del expediente 4.12, con estos cambios en fase1_v63.json, fase1_metadatos.json y alcance_v2.json:
     - fecha de análisis = la de ejecución;
     - acciones y capitalización descritas con su concepto real y sus fechas (4.13 §6; la cifra NO cambia: decisión VISCOFAN-ACCIONES);
     - notas actualizadas con las operaciones de capital de 2026;
     - aviso de alcance con la V6.4.1 y el perímetro.
   - configuracion_economica.json: la del 4.12 con el perímetro de la inversión declarado de forma explícita. Es «NIIF 16», el punto de
     cálculo coherente con el motor B (resultados/conciliacion_arrendamientos_viscofan.md), con «Caja» como variante calculada. No se
     adopta: decisión VISCOFAN-PERIMETRO.
   - antecedentes/: extracto, fase A y fase B del expediente 4.12, para reutilizarlos si sus entradas solo difieren en lo editorial
     (comprobar_reutilizacion_viscofan.py lo comprueba antes de usarlos).
Uso (desde munger_v2_r1/): python3 -I …/scripts/preparar_expedientes_4_13.py
Escribe las carpetas y resultados/preparacion_expedientes_4_13.json y .md.
"""
import copy
import datetime as dt
import hashlib
import json
import os
import shutil
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
E413 = os.path.dirname(AQUI)
PV = os.path.abspath(os.path.join(E413, "..", ".."))
RAIZ = os.path.dirname(PV)
E412 = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_12")
sys.path.insert(0, os.path.join(PV, "scripts"))

ROIC_T_413 = ("(4.13 §8, condición de PRECISION_ROIC_4_9.md) Q-ROIC1 sigue sin decidir: si el ROIC de largo plazo de la fase B es neto de "
              "reposición (rendimiento de la inversión que excede el mantenimiento), la combinación coherente con la suma del requisito es la que NO "
              "reestima el ROIC del terminal (SR1); si se midió sobre una inversión total que ya incluye la reposición, la coherente es la que lo "
              "reestima (SR2, ROIC × f). SR2 se calcula como variante; ninguna se elige por su valor")


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def huellas(base):
    out = {}
    for r, ds, fs in os.walk(base):
        ds[:] = [d for d in ds if d not in (".lo_perfil", "__pycache__")]
        for f in sorted(fs):
            p = os.path.join(r, f)
            out[os.path.relpath(p, base)] = sha(p)
    return out


def copia_vidrala(origen, nombre):
    import cierre_v2 as CIE
    import entradas_economicas as EE
    ens = os.path.join(E413, nombre)
    dest = os.path.join(ens, "Vidrala")
    if os.path.exists(dest):
        raise SystemExit(f"ya existe {os.path.relpath(dest, RAIZ)}: no se sobrescribe")
    st = json.load(open(os.path.join(origen, "estado_pipeline.json"), encoding="utf-8"))
    if os.path.exists(os.path.join(origen, "ESPERANDO.md")) or st.get("paso") != 14:
        raise SystemExit(f"{origen} no está cerrado (paso {st.get('paso')})")
    h0 = huellas(origen)
    shutil.copytree(origen, dest, ignore=shutil.ignore_patterns(".lo_perfil", "__pycache__"))
    for n in (CIE.REGISTRO_RESUMEN, CIE.RESPALDO_RESUMEN):
        p = os.path.join(dest, n)
        if os.path.exists(p):
            reg = json.load(open(p, encoding="utf-8"))
            for e in reg.get("publicaciones") or []:
                e["csv"] = os.path.join(ens, os.path.basename(e["csv"]))
                e["expediente"] = dest
            json.dump(reg, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    pc = os.path.join(dest, "configuracion_economica.json")
    conf = json.load(open(pc, encoding="utf-8"))
    h_antes = EE.huella_configuracion(conf)
    ant_roic = conf["trazabilidad"]["PM1.roic_terminal"]["justificacion"]
    conf["trazabilidad"]["PM1.roic_terminal"]["justificacion"] = ROIC_T_413
    conf["naturaleza"] += (" (4.13) Copia regenerada con el código de la 4.13 (contrato de cobertura por hipótesis, avisos de dominio de todas las variantes) "
                           f"a partir de {os.path.relpath(origen, PV)}; misma configuración económica (huella sin cambios), plantilla V6.4 (las altas de derechos de "
                           "uso de Vidrala no están conciliadas: pendiente declarado).")
    json.dump(conf, open(pc, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    assert EE.huella_configuracion(conf) == h_antes, "el cambio tenía que ser editorial"
    pa = os.path.join(dest, "alcance_v2.json")
    al = json.load(open(pa, encoding="utf-8"))
    al["aviso"] = al["aviso"].replace("ENSAYO 4.12", "ENSAYO 4.13 (regeneración de la 4.12)")
    al["fecha"] = dt.date.today().isoformat()
    json.dump(al, open(pa, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return {"origen": os.path.relpath(origen, RAIZ), "destino": os.path.relpath(dest, RAIZ), "archivos_copiados": len(h0),
            "huella_economica_configuracion": {"antes": h_antes, "despues": EE.huella_configuracion(conf)},
            "cambios": {"configuracion_economica.json": {"trazabilidad.PM1.roic_terminal.justificacion": [ant_roic, ROIC_T_413], "naturaleza": "nota 4.13 añadida"},
                        "alcance_v2.json": {"aviso": "ENSAYO 4.12 → ENSAYO 4.13 (regeneración de la 4.12)", "fecha": al["fecha"]},
                        CIE.REGISTRO_RESUMEN: f"destino del resumen y expediente reubicados en {nombre}/"},
            "aprobacion": "la del origen viaja como antecedente y la retira la primera llamada del pipeline (material cambiado)"}


def viscofan():
    import configuracion_economica as CE
    ori = os.path.join(E412, "viscofan", "experimental", "Viscofan")
    ens = os.path.join(E413, "viscofan")
    dest = os.path.join(ens, "Viscofan")
    if os.path.exists(dest):
        raise SystemExit(f"ya existe {os.path.relpath(dest, RAIZ)}: no se sobrescribe")
    hoy = dt.date.today().isoformat()
    entradas = ["etapa1", "fase1_v63.json", "fase1_metadatos.json", "fase1_fuentes.json", "fase1_partes", "fase1_listas.md", "texto"]
    os.makedirs(dest)
    copiadas = {}
    for n in entradas:
        o = os.path.join(ori, n)
        if os.path.isdir(o):
            shutil.copytree(o, os.path.join(dest, n))
            copiadas[n] = huellas(o)
        else:
            shutil.copy2(o, os.path.join(dest, n))
            copiadas[n] = sha(o)
    cambios = {}
    acc_f = ("AR_2025, nota 20.2: media ponderada «diluida» de acciones en circulación de 2025, la publicada (45,479209 millones). Contradice su propia definición: "
             "queda por debajo de la básica (45,656226) con el mismo numerador, y su BPA (3,52) supera al básico (3,50); en 2024 sí la superaba. Otras cifras con su "
             "concepto y fecha: en circulación 45,993399 a 31-dic-2025 y 45,603643 a 30-jun-2026 (CNMV); no hay cifra al 3-nov-2026. La cifra no se sustituye "
             "(decisión VISCOFAN-ACCIONES, sin firmar): 2026-11_Vidrala_ensayo_4_13/fuentes/CONCILIACION_ACCIONES_VISCOFAN_4_13.md")
    cap_f = "Precio 54,70 EUR (cierre del 3-nov-2026) × 45,479209 millones (media ponderada «diluida» de 2025): fechas mezcladas, precio de 2026 y acciones medias de 2025"
    for n in ("fase1_v63.json", "fase1_metadatos.json"):
        p = os.path.join(dest, n)
        d = json.load(open(p, encoding="utf-8"))
        c = {"fecha_analisis": [d.get("fecha_analisis"), hoy]}
        d["fecha_analisis"] = hoy
        if isinstance(d.get("acciones_diluidas"), dict):
            c["acciones_diluidas.fuente"] = [d["acciones_diluidas"].get("fuente"), acc_f]
            d["acciones_diluidas"].update(fuente=acc_f, periodo="media ponderada del ejercicio 2025 (publicada como diluida)", unidad="millones de acciones",
                                          nota=("Sensibilidad de definición (no corrección): básica media 2025 45,656; en circulación 45,993 (31-dic-2025) y 45,604 "
                                                "(30-jun-2026); plan de incentivos 2025–2027 hasta 0,315 (objetivo) o 0,4725 (máximo) millones de acciones en 2028. "
                                                "Precio de Sí con cada una en resultados/alternativas_acciones_viscofan.md; todas en «caro»."))
        if isinstance(d.get("capitalizacion"), dict):
            c["capitalizacion.fuente"] = [d["capitalizacion"].get("fuente"), cap_f]
            d["capitalizacion"].update(fuente=cap_f, periodo="precio del 3-nov-2026 × acciones medias de 2025", unidad="millones de EUR",
                                       nota="Con las acciones en circulación a 30-jun-2026 (45,604) sería 2.494,5; a 31-dic-2025 (45,993), 2.515,8. Solo contraste.")
        if isinstance(d.get("_notas"), list):
            viejas = [x for x in d["_notas"] if str(x).startswith("Acciones diluidas")]
            d["_notas"] = [x for x in d["_notas"] if not str(x).startswith("Acciones diluidas")] + [
                "Acciones (4.13): media ponderada «diluida» publicada de 2025 (45,479 M), contradictoria con la básica (45,656 M). Capital: 46,5 M de acciones a "
                "31-dic-2025 con 506.601 propias; reducción de 500.000 acciones propias inscrita el 11-may-2026 (46,0 M; BORME-C-2026-1603); en junio de 2026, "
                "aumento liberado de 1.001.717 acciones con amortización simultánea del mismo número (BORME-C-2026-3155); autocartera de 396.357 a 30-jun-2026 (CNMV). "
                "Ninguna se aplica al modelo: elección pendiente VISCOFAN-ACCIONES."]
            c["_notas"] = {"sustituida": viejas}
        cambios[n] = c
        json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    con = json.load(open(os.path.join(E413, "resultados", "conciliacion_arrendamientos_viscofan.json"), encoding="utf-8"))
    altas = [con["serie"][f"altas_derechos_de_uso:{a}"] for a in (2021, 2022, 2023, 2024, 2025)]
    conf = copy.deepcopy(json.load(open(os.path.join(ori, "configuracion_economica.json"), encoding="utf-8")))
    conf["plantilla_requerida"] = "V6.4.1 experimental"
    conf["PM1"].update(perimetro_inversion=CE.PERIMETROS[1], altas_derechos_uso=altas,
                       altas_fuente=("Altas de derechos de uso 2021–2025 (notas de arrendamientos): CF_2021 p. 39, CF_2022_compilacion p. 51, CA_2023_es p. 35, "
                                     "CF_2024 y AR_2025; conciliación y réplica en 2026-11_Vidrala_ensayo_4_13/resultados/conciliacion_arrendamientos_viscofan.md"))
    conf["trazabilidad"]["PM1.perimetro"] = {
        "clase": "convención", "confianza": "media",
        "fuente_o_condicion": "plantilla V6.4.1 experimental (4.13 §7); altas de derechos de uso conciliadas 2021–2025 (24,110) frente a su amortización (27,051)",
        "justificacion": ("NIIF 16 completo: el motor B trata los arrendamientos como capital (Historia fila 32) y como deuda (puente), su NOPAT ya descuenta la "
                          "amortización de los derechos de uso y no resta sus pagos; la inversión que repone esos activos son las altas. Con «Caja» (la V6.4) la "
                          "D&A incluye la de los derechos de uso y el capex no incluye sus altas. Es el punto de cálculo, no una adopción: «Caja» se calcula como "
                          "variante (perimetro_alternativo) y la elección es VISCOFAN-PERIMETRO"),
        "materialidad": "la mide configuracion_v64_variantes.json (variante perimetro_alternativo y sus extremos de θ) y la evalúa la fase C"}
    conf["trazabilidad"]["PM1.familia"]["justificacion"] = (
        "Θ parte del exceso observado: con el perímetro NIIF 16, Σ (capex + altas de derechos de uso − D&A) 2021–2025 = 64,923 (40,813 con «Caja»); "
        "θ está acotado en [0, 1]; Λ necesitaría λ, no observado")
    conf["trazabilidad"]["PM1.parametro"]["justificacion"] = (
        "θ es la parte del exceso histórico que fue reposición; las cuentas no la separan. θ = 0 (todo fue crecimiento) y θ = 1 (todo fue reposición) se "
        "calculan como variantes, también con el perímetro «Caja»; con NIIF 16 la D&A de los derechos de uso se compara con sus altas (4.13 §7)")
    conf["trazabilidad"]["PM1.roic_terminal"]["justificacion"] = ROIC_T_413
    conf["naturaleza"] += (" (4.13) Expediente nuevo con la plantilla V6.4.1 experimental: el perímetro de la inversión de las bases de P-M1 se declara de forma "
                           "explícita, «NIIF 16» (capex + altas de derechos de uso frente a toda la D&A) como punto de cálculo coherente con el motor B, con «Caja» (la "
                           "V6.4) como variante calculada. No se adopta (VISCOFAN-PERIMETRO). N sigue en 45,479209 (VISCOFAN-ACCIONES).")
    f = CE.validar(conf)
    if f:
        raise SystemExit("configuración no válida: " + " | ".join(f))
    json.dump(conf, open(os.path.join(dest, "configuracion_economica.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    al = json.load(open(os.path.join(ori, "alcance_v2.json"), encoding="utf-8"))
    al["aviso"] = (al["aviso"].replace("ENSAYO 4.12 · VISCOFAN CON LA PLANTILLA V6.4 EXPERIMENTAL", "ENSAYO 4.13 · VISCOFAN CON LA PLANTILLA V6.4.1 EXPERIMENTAL")
                   .replace("cartera legado;", "cartera legado; perímetro de la inversión «NIIF 16» como punto de cálculo, con «Caja» como variante (no adoptado);")
                   + " Acciones: media ponderada «diluida» publicada de 2025, contradictoria con la básica (elección pendiente).")
    al["fecha"] = hoy
    al["fuente"] = "2026-11_Vidrala_ensayo_4_13/scripts/preparar_expedientes_4_13.py; encargo 4.13 §6 y §7. Metadato de la orquestación."
    json.dump(al, open(os.path.join(dest, "alcance_v2.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    ant = os.path.join(ens, "antecedentes")
    os.makedirs(ant)
    reus = {}
    for n in ("extracto_v63.md", "fase_a.json", "fase_a.md", "fase_b.json", "fase_b.md", "datos_v63.md", "entrada_v63.md", "datos_v63.json"):
        shutil.copy2(os.path.join(ori, n), os.path.join(ant, f"{n}.4_12"))
        reus[n] = sha(os.path.join(ori, n))
    return {"origen": os.path.relpath(ori, RAIZ), "destino": os.path.relpath(dest, RAIZ), "entradas_copiadas": copiadas, "campos_cambiados": cambios,
            "configuracion": {"sha256": sha(os.path.join(dest, "configuracion_economica.json")), "resumen": CE.resumen(conf), "altas_derechos_uso": altas},
            "alcance_sha256": sha(os.path.join(dest, "alcance_v2.json")), "antecedentes_para_reutilizar": reus,
            "no_se_copia": "libros, estado, fase C, auditoría, ficha, informe y resumen del 4.12 (el pipeline los genera de nuevo; la fase C y la auditoría, con agentes reales)"}


def main():
    if "--solo-viscofan" in sys.argv:
        # (rehacer solo Viscofan antes de ningún agente; los expedientes de Vidrala ya preparados no se tocan)
        p = os.path.join(E413, "resultados", "preparacion_expedientes_4_13.json")
        reg = json.load(open(p, encoding="utf-8"))
        reg["viscofan"] = viscofan()
        reg["viscofan_rehecho"] = dt.datetime.now().isoformat(timespec="seconds")
        json.dump(reg, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(json.dumps(reg["viscofan"]["campos_cambiados"], ensure_ascii=False)[:800])
        return 0
    reg = {"fecha": dt.datetime.now().isoformat(timespec="seconds"),
           "vidrala_condicionado": copia_vidrala(os.path.join(E412, "cierre_condicionado", "Vidrala"), "vidrala_condicionado"),
           "vidrala_bloqueo": copia_vidrala(os.path.join(E412, "cierre_bloqueo", "Vidrala"), "vidrala_bloqueo"),
           "viscofan": viscofan()}
    os.makedirs(os.path.join(E413, "resultados"), exist_ok=True)
    json.dump(reg, open(os.path.join(E413, "resultados", "preparacion_expedientes_4_13.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    md = ["# Preparación de los expedientes regenerados en la 4.13 (Hito 4)", ""]
    for k in ("vidrala_condicionado", "vidrala_bloqueo"):
        x = reg[k]
        md += [f"## {k}", f"- `{x['origen']}` → `{x['destino']}` ({x['archivos_copiados']} archivos, sin el perfil de LibreOffice).",
               f"- Cambio editorial en la configuración (huella económica igual: `{x['huella_economica_configuracion']['antes'][:16]}…`): justificación de PM1.roic_terminal con la condición de Q-ROIC1 de la 4.9 y nota 4.13.",
               "- Aprobación copiada: antecedente; la primera llamada la retira. Se sigue con `--desde 10` (variantes 4.13, fase C y auditoría nuevas).", ""]
    v = reg["viscofan"]
    md += ["## viscofan", f"- Expediente nuevo `{v['destino']}` (V6.4.1 experimental) con las entradas de partida de `{v['origen']}`.",
           "- Campos cambiados: " + "; ".join(f"{n}: {', '.join(c)}" for n, c in v["campos_cambiados"].items()) + ".",
           f"- Configuración: {v['configuracion']['resumen']} (altas {v['configuracion']['altas_derechos_uso']}).",
           f"- Antecedentes para reutilizar (solo si sus entradas no cambian en lo económico): {', '.join(v['antecedentes_para_reutilizar'])}.",
           f"- No se copia: {v['no_se_copia']}."]
    open(os.path.join(E413, "resultados", "preparacion_expedientes_4_13.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
    print("\n".join(md))
    return 0


if __name__ == "__main__":
    sys.exit(main())
