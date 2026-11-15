#!/usr/bin/env python3
"""Actualiza VERSION, CONTINUIDAD.md y PROMPT_NUEVA_VENTANA.md para la entrega 4.13, a partir de sus copias de la 4.12 en
…_4_13/reproduccion/ (de modo que se puede repetir sin acumular cambios). Uso (desde munger_v2_r1/):
    python3 -I -B …/scripts/actualizar_documentos_version_4_13.py N_BATERIA_V64 MINUTOS_RONDA
N_BATERIA_V64: número de pruebas de test_integracion_v64.py en la ronda general; MINUTOS_RONDA: duración de verificar_paquete.sh completa."""
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
EXP = os.path.dirname(AQUI)
RAIZ = os.path.abspath(os.path.join(EXP, "..", "..", ".."))
REP = os.path.join(EXP, "reproduccion")
ZIP = "munger_v2_r1_entrega4.13_fiabilidad_motor_B_y_conciliacion_economica.zip"
E = "personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_13"


def sustituir(t, a, b, n=1):
    assert t.count(a) == n, f"no encontrado {n} vez/veces: {a[:80]!r}"
    return t.replace(a, b)


def main():
    nb, mins = int(sys.argv[1]), sys.argv[2]
    # VERSION
    v = (f"munger_v2 · r1 · entrega 4.13 (fiabilidad del motor B y conciliación económica de los dos casos: guardas de estructura JSON antes de la vigencia en las "
         f"cuatro vías; coherencia de la acción final con el estado, el protocolo y los dos objetivos; contrato de cobertura por hipótesis (contraste aislado, "
         f"variación conjunta necesaria, juicio económico y «no determinada») y avisos de dominio de todas las variantes, agrupados; plantilla V6.4.1 experimental "
         f"con el perímetro de la inversión de P-M1, referencia nueva y compatibilidad exacta con la V6.4; acciones de Viscofan conciliadas (contradicción de la "
         f"nota 20 declarada, cuatro alternativas, todas «caro») y evidencia activa limpia; arrendamientos 2021–2025 conciliados, θ = 0, 0,5 y 1 con los dos "
         f"perímetros y réplica independiente; tres interpretaciones de Vidrala corregidas sin cambiar parámetros; tres expedientes regenerados con agentes reales "
         f"y auditorías APROBADO del material vigente: Vidrala condicionado concluido · esperar · objetivo condicionado 56,02 frente a 90,10 €, Vidrala bloqueo "
         f"pendiente_de_datos · sin acción, Viscofan (V6.4.1, NIIF 16) concluido · esperar · objetivo condicionado 40,16 frente a 54,70 €; batería obligatoria de "
         f"la V6.4 de {nb} pruebas; dos revisiones internas; aptitud: uso supervisado experimental, no apto para decisiones con dinero real; propuesta humana sin "
         f"firmar en tres grupos (13 decisiones); incluye la 4.12 y anteriores) · 2026-11-13 · base SHA-256 61c70800d0faa7c4a98888b7413820ec8041153e53484c32b0c549b26b6af87d")
    open(os.path.join(RAIZ, "VERSION"), "w", encoding="utf-8").write(v + "\n")
    # CONTINUIDAD
    c = open(os.path.join(REP, "CONTINUIDAD_4_12.md.txt"), encoding="utf-8").read()
    bloque = (
        f"- **Paquete:** `munger_v2_r1`, **entrega 4.13 (fiabilidad del motor B y conciliación económica de los dos casos)**, 13-nov-2026. Responde al encargo 4.13 "
        f"(`{E}/ENCARGO_4_13.md`), que resuelve las incidencias de la revisión externa de la 4.12 antes de ampliar al motor A. El identificador exacto está en `VERSION`. "
        f"Expediente: `{E}/` (empezar por `INFORME_INTEGRACION_4_13.md`, `REGISTRO_ENTREGA_4.13.md` y `propuestas/PROPUESTA_HUMANA_4_13.md`).\n"
        "  - **Fiabilidad técnica:** guardas de estructura JSON antes de la vigencia en pipeline, ficha, informe y resumen (`estructura_json.py`, `ESTR.protegido`, "
        "`motivo_vigencia` protegido; §3); la acción FINAL manda y una contradicción entre acción, estado, protocolo y los dos objetivos no llega a ningún cierre "
        "(`objetivo_v64.contradicciones_salida`; §4); contrato de cobertura por hipótesis con la base de cada materialidad (calculada, juicio económico o no "
        "determinada = null) para la acción y el objetivo, y avisos de dominio de todas las variantes, agrupados (formato 4.13; §5).\n"
        "  - **Plantilla V6.4.1 experimental** (`v6/v641_experimental/`): la V6.4 con el perímetro de la inversión de P-M1 («Caja» o «NIIF 16», con las altas de "
        "derechos de uso), referencia nueva y SHA-256; con el perímetro vacío o «Caja», 0 celdas distintas de la V6.4. Selección con "
        "`--config personaje_v2/config_v2_v641_experimental.json`. La V6.4 no cambia.\n"
        "  - **Viscofan** (`viscofan/Viscofan/`, V6.4.1, NIIF 16 como punto de cálculo, no adoptado): acciones conciliadas (`fuentes/CONCILIACION_ACCIONES_VISCOFAN_4_13.md`; "
        "N = 45,479209 con su concepto, contradicción declarada; VISCOFAN-ACCIONES pendiente), arrendamientos 2021–2025 conciliados, fases A, B y C nuevas con agentes "
        "reales: **concluido · APROBADO · Vigilar · esperar**, objetivo condicionado 40,16 frente a 54,70 € (18 variantes, todas «caro», 38,47–43,39).\n"
        "  - **Vidrala** (`vidrala_condicionado/`, `vidrala_bloqueo/`): fases C nuevas con el contrato de la 4.13; **concluido · APROBADO · esperar** (objetivo "
        "condicionado 56,02 frente a 90,10 €) y **pendiente_de_datos · APROBADO · sin acción** (objetivo bloqueado); tres interpretaciones de la 4.12 corregidas "
        "(`CORRECCIONES_ECONOMICAS_VIDRALA_4_13.md`).\n"
        f"  - **Pruebas:** batería obligatoria de la V6.4 de **{nb}** (grupos A–H); réplicas independientes 21 + 21 + 20. **Revisión interna** (Fable, contexto "
        "separado) en dos pasadas (`revision_interna/`); lo corregido después de la segunda lo comprueba el control de la entrega.\n"
        "  - **Aptitud de uso (informe §9):** uso supervisado y experimental de empresas del motor B; **no apto para decisiones con dinero real**. Nada adoptado: la "
        "propuesta humana (13 decisiones, en tres grupos) está sin firmar.\n"
        f"  - **Control:** `{E}/scripts/comprobar_entrega_4_13.py`. La versión 4.12 de este archivo está en `{E}/reproduccion/CONTINUIDAD_4_12.md.txt`.\n"
        "- **Entrega anterior 4.12 (validación supervisada, cierre de la integración y contraste con Viscofan)**, 12/13-nov-2026.")
    c = sustituir(c, "- **Paquete:** `munger_v2_r1`, **entrega 4.12 (validación supervisada, cierre de la integración y contraste con Viscofan)**, 12/13-nov-2026.", bloque)
    c = sustituir(c, "Tarda unos 25–40 minutos (23 en la copia limpia de la 4.12)", f"Tarda unos 25–45 minutos ({mins} en la copia limpia de la 4.13)")
    c = sustituir(c, "(`personaje_v2/pruebas/test_integracion_v64.py`, 4.11 y 4.12): **127/127** (plantilla, 117 casos con la réplica independiente, pipeline y cambio de base; desde la 4.12, vigencia, materialidad y protocolos del objetivo, y coherencia);",
                  f"(`personaje_v2/pruebas/test_integracion_v64.py`, 4.11, 4.12 y 4.13): **{nb}/{nb}** (plantilla, 117 casos con la réplica independiente, pipeline y cambio de base; desde la 4.12, vigencia, materialidad y protocolos del objetivo, y coherencia; desde la 4.13, guardas de estructura, salto del protocolo, cobertura y la V6.4.1);")
    c = sustituir(c, "**`personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_12/resultados/LEEME_CONTROLES_HISTORICOS_4_12.md`** (el de la 4.11 sigue describiendo el árbol 4.11).",
                  f"**`{E}/resultados/LEEME_CONTROLES_HISTORICOS_4_13.md`** (los de la 4.12 y la 4.11 siguen describiendo sus árboles).")
    c = sustituir(c, "El último es `python3 -I personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_11/scripts/comprobar_entrega_4_11.py`.",
                  f"El último es `python3 -I -B {E}/scripts/comprobar_entrega_4_13.py`.")
    fila412 = next(l for l in c.splitlines() if l.startswith("| **Entrega 4.12 (12/13-nov)**"))
    c = sustituir(c, fila412, fila412 + "\n| **Entrega 4.13 (13-nov)** | **Fiabilidad del motor B y conciliación económica:** guardas de estructura antes de la vigencia, acción final y objetivo coherentes, "
                  "contrato de cobertura y avisos de dominio de todas las variantes; V6.4.1 experimental con el perímetro de la inversión; acciones y arrendamientos de Viscofan "
                  "conciliados; interpretaciones de Vidrala corregidas; tres expedientes regenerados con agentes reales y auditorías APROBADO; dos revisiones internas; "
                  "aptitud: experimental; propuesta sin firmar en tres grupos |")
    fila_m = next(l for l in c.splitlines() if l.startswith("| `personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_12/` |"))
    c = sustituir(c, fila_m, f"| `{E}/` | Entrega 4.13: `INFORME_INTEGRACION_4_13.md`, `REGISTRO_ENTREGA_4.13.md`, `REGISTRO_PRUEBAS_4_13.md`, `REGISTRO_AVANCE_4_13.md`, "
                  "`CORRECCIONES_ECONOMICAS_VIDRALA_4_13.md`, `fuentes/`, `resultados/`, `revision_interna/`, `propuestas/`, `reproduccion/`, `scripts/` y los tres expedientes "
                  "(`vidrala_condicionado/`, `vidrala_bloqueo/`, `viscofan/`) |\n| `v6/v641_experimental/` | Plantilla V6.4.1 experimental del motor B (4.13): la V6.4 con el "
                  "perímetro de la inversión de P-M1; `entregables/`, `referencia/`, `scripts/` y `docs/README_V6.4.1_experimental.md` |\n" + fila_m)
    c = sustituir(c, "| `personaje_v2/GUIA_RECORRIDO_SUPERVISADO.md` | Guía breve del recorrido supervisado con agentes reales (4.12) |",
                  "| `personaje_v2/GUIA_RECORRIDO_SUPERVISADO.md` | Guía breve del recorrido supervisado con agentes reales (4.12; actualizada en la 4.13) |")
    lim = next(l for l in c.splitlines() if l.startswith("- **Entrega 4.12:** nada adoptado"))
    c = sustituir(c, lim, "- **Entrega 4.13:** nada adoptado (N y perímetro de Viscofan, configuraciones, estructura de reposición, protocolos, criterio de materialidad ni "
                  "umbrales de dominio); la materialidad para el objetivo es un juicio del agente (con el mismo material, dos agentes la trazan distinta); repetir las fases "
                  "A y B de Viscofan con agentes nuevos movió el precio de Sí +1,54 €, más que el perímetro, y el rango calculado no lo recoge; algunas celdas de contraste "
                  "de Viscofan conservan datos de 2026 de la etapa 1, declaradas; bytes de BORME y CNMV no conservados (informe §9.6 y revisiones internas).\n" + lim)
    p17 = next(l for l in c.splitlines() if l.startswith("9.17. **De la entrega 4.12**"))
    c = sustituir(c, p17, p17 + f"\n9.18. **De la entrega 4.13** (`{E}/propuestas/PROPUESTA_HUMANA_4_13.md` y `propuesta_humana_4_13.json`, sin firmar): política de salida "
                  "(D413-USO, D413-PROTOCOLO, D413-FUNDAMENTO, D413-DOMINIOS), elecciones por empresa (VISCOFAN-ACCIONES, VISCOFAN-PERIMETRO, VISCOFAN-CONFIG, "
                  "VIDRALA-CONFIG, VIDRALA-PERIMETRO) y ampliaciones (D413-MOTOR-A, D413-V641, D411-TERMINAL-R1, D412-V63). Sustituyen a las de la 4.12 del mismo "
                  "asunto. Información que falta: desglose del capex de los dos casos, acciones de Viscofan al 3-nov-2026, altas de derechos de uso de Vidrala.")
    c = sustituir(c, "integración V6.4 (127), trazabilidad (78)", f"integración V6.4 ({nb}), trazabilidad (78)")
    c = sustituir(c, "con el resultado que fija `personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_11/resultados/LEEME_BATERIAS_HISTORICAS.md`:",
                  f"con el resultado que fija `{E}/resultados/LEEME_CONTROLES_HISTORICOS_4_13.md`:")
    c = sustituir(c, "2. Adjuntar `munger_v2_r1_entrega4.12_validacion_supervisada_y_Viscofan.zip`", f"2. Adjuntar `{ZIP}`")
    open(os.path.join(RAIZ, "CONTINUIDAD.md"), "w", encoding="utf-8").write(c)
    # PROMPT_NUEVA_VENTANA
    p = open(os.path.join(REP, "PROMPT_NUEVA_VENTANA_4_12.md.txt"), encoding="utf-8").read()
    p = sustituir(p, "munger_v2_r1_entrega4.12_validacion_supervisada_y_Viscofan.zip", ZIP, 3)
    p = sustituir(p, "`munger_v2_r1_entrega4.12_validacion_supervisada_y_Viscofan.zip.sha256`", f"`{ZIP}.sha256`") if "`munger_v2_r1_entrega4.12_validacion_supervisada_y_Viscofan.zip.sha256`" in p else p
    l412 = next(l for l in p.splitlines() if l.startswith("- la validación supervisada de la integración"))
    p = sustituir(p, l412, l412 + "\n- la fiabilidad del motor B y la conciliación económica de los dos casos: guardas de estructura antes de la vigencia, acción final y objetivo "
                  "coherentes, contrato de cobertura y avisos de dominio de todas las variantes; plantilla V6.4.1 experimental con el perímetro de la inversión; acciones y "
                  "arrendamientos de Viscofan conciliados; interpretaciones de Vidrala corregidas; tres expedientes regenerados con agentes reales; batería obligatoria de "
                  f"la V6.4 de {nb} pruebas, dos revisiones internas, aptitud de uso (experimental) y propuesta humana sin firmar en tres grupos (entrega 4.13).")
    p = sustituir(p, "la batería de la integración V6.4 experimental (127/127, 4.11 y 4.12)", f"la batería de la integración V6.4 experimental ({nb}/{nb}, 4.11, 4.12 y 4.13)")
    p = sustituir(p, "los controles históricos y el de la 4.12, con los resultados y las salidas de referencia que fija `personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_12/resultados/LEEME_CONTROLES_HISTORICOS_4_12.md`",
                  f"los controles históricos y el de la 4.13, con los resultados y las salidas de referencia que fija `{E}/resultados/LEEME_CONTROLES_HISTORICOS_4_13.md`")
    p = sustituir(p, "terminando por `python3 -I personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_11/scripts/comprobar_entrega_4_11.py`",
                  f"terminando por `python3 -I -B {E}/scripts/comprobar_entrega_4_13.py`")
    open(os.path.join(RAIZ, "PROMPT_NUEVA_VENTANA.md"), "w", encoding="utf-8").write(p)
    print("VERSION, CONTINUIDAD.md y PROMPT_NUEVA_VENTANA.md actualizados para la 4.13")


if __name__ == "__main__":
    main()
