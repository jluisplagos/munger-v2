#!/usr/bin/env python3
"""Escribe las dos configuraciones de cambio de base del encargo 4.11 (§7 y §9) desde una base común, de forma reproducible:
  - configuracion/cambio_de_base_control_heredado.json → control_heredado/ (V6.4 en modo HEREDADO, para comparar con la 4.10.1);
  - configuracion/cambio_de_base_piloto.json            → piloto/ (V6.4 EXPERIMENTAL con una configuración de DEMOSTRACIÓN).
Las entradas de la base económica 2025 son las de la 4.10.1 (configuracion_ensayo_2025.json: precio, N, E, rf, datos reexpresados y
caso principal), con la evidencia ACTIVA corregida (M41/N41, M52/N52 y las demás filas con restos de la base anterior, §7) y sin las
notas que reintroducían la tasa o las acciones anteriores. Uso (desde munger_v2_r1/): python3 -I …/scripts/preparar_configuraciones_4_11.py [DIR_SALIDA] (por omisión, configuracion/)
"""
import copy
import json
import os

AQUI = os.path.dirname(os.path.abspath(__file__))
ENS = os.path.dirname(AQUI)
CORR = "personaje_v2/empresas_v2_correcciones"
C1 = json.load(open(os.path.join(ENS, "..", "2026-11_Vidrala_ensayo_4_10_1", "configuracion", "configuracion_ensayo_2025.json"), encoding="utf-8"))
E = C1["entradas"]
RX = C1["datos_heredados_reexpresados_a_2025"]["celdas"]
CP = C1["caso_principal_analisis"]

RF_FUENTE = ("Deutsche Bundesbank, Kapitalmarktstatistik «Tägliche Renditen der jeweils jüngsten Bundeswertpapiere» (fin de mes), fila «Dez. 3,47 . 3,24 2,85 2,63 2,44 2,12» "
             "del bloque de 2025: Bundesanleihe a 10 años, 2,85 % a fin de diciembre de 2025 (https://www.bundesbank.de/resource/blob/772218/f561ec1a8ae1e51f3cd4d15d81d454cf/"
             "472B63F073F071307366337C94F8C870/rendbund-data.pdf). Consultado el 12-nov-2026 (ejemplar con fecha 11.11.2026) con la herramienta web, que devuelve el contenido y no los "
             "bytes: el PDF no se conserva en el paquete (la consola no tiene red hacia bundesbank.de: proxy 403) y no se calcula aquí su huella; la revisión externa registró "
             "6ace5ac7785ecca9f8f3d56ce12f49fb2acbe4b9418dd84def46fc63c516a9dd para su ejemplar (dato de la revisión, no comprobado en esta sesión). Bund (sin riesgo del euro), no el bono "
             "español, que llevaría la prima país (sumada aparte).")

BASE = {
    "tipo": "cambio_de_base", "version_formato": 1, "empresa": "Vidrala",
    "origen": f"{CORR}/2026-11_Vidrala_ensayo_4_6_1/Vidrala",
    "base_economica": {"fecha": "2025-12-31", "descripcion": "Cierre del ejercicio 2025 de Vidrala (Historia 2016–2025), con las entradas del ensayo 4.10.1: precio de cierre de 2025, acciones en circulación y capitalización a 31-dic-2025, rf del Bund a fin de diciembre de 2025, con derecho al dividendo a cuenta. No se incorpora ninguna operación de 2026."},
    "fechas": {"ejecucion": "real", "precio": "2025-12-31", "acciones": "2025-12-31",
               "publicacion_fuentes": "cuentas anuales consolidadas 2025 formuladas el 24-feb-2026 (ES 2025, pág. PDF 17); Bundesbank, ejemplar de 11.11.2026 (valor de fin de diciembre de 2025)"},
    "conservar": ["etapa1", "texto", "fase1_partes", "fase1_decisiones.json", "fase1_fuentes.json"],
    "fuentes_adicionales": [{"pdf": C1["fuentes"]["es_2025"]["archivo"], "sha256": C1["fuentes"]["es_2025"]["sha256"], "texto": "texto/ES_2025_informacion_financiera_consolidada.txt"}],
    "metadatos": {
        "precio": {"valor": E["precio"]["valor"], "moneda_cotizacion": "EUR", "fecha": E["precio"]["fecha"], "fx": None, "fx_fecha": None, "fuente": E["precio"]["fuente"]},
        "acciones_diluidas": {"valor": E["N_millones"]["valor"], "fecha": E["N_millones"]["fecha"], "fuente": E["N_millones"]["fuente"], "pagina": E["N_millones"]["pagina"]},
        "capitalizacion": {"valor": E["E_capitalizacion"]["valor"], "fecha": E["E_capitalizacion"]["fecha"], "fuente": E["E_capitalizacion"]["fuente"]},
        "tasa_sin_riesgo": {"valor": E["tasa_sin_riesgo"]["valor"], "fuente": RF_FUENTE},
    },
    "nota_metadatos": ("(4.11, cambio de base) Metadatos ACTIVOS con base económica 31-dic-2025, escritos por cambiar_base.py: precio de cierre de 2025 (90,10 €, ES 2025 pág. PDF 97), "
                       "acciones en circulación a 31-dic-2025 (35.206.258 emitidas − 23.400 propias = 35,182858 millones; sin instrumentos dilutivos), E = 3.169,9755058 mm y rf del Bund a fin "
                       "de diciembre de 2025 (2,85 %, Bundesbank). fecha_analisis es la fecha real de ejecución. Las notas de la base anterior (precio, rentabilidad sin riesgo y "
                       "acciones) están en antecedentes/notas_retiradas.json y no se citan aquí."),
    "notas_que_se_retiran": ["Bolsaman", "Trading Economics", r"35,206 M", r"\(4\.10\.1\) Metadatos ACTIVOS", r"\(4\.10\.1\) Caso principal", r"\(4\.10\.1, preparación 2\)"],
    "analisis": {},
    "evidencia": {},
    "textos_prohibidos": [r"1S2026", r"IPP 1S", r"30/06/2026", r"25/09", r"23/06", r"22/07", r"88,70", r"34,185", r"3\.032", r"3\.029", r"35,206 −", r"liberada 2026",
                          r"Trading Economics", r"Bolsaman", r"\bLTM\b", r"G-16", r"2487_es-informes_financieros_semestrales"],
}
# caso principal de la 4.10.1 (precisión de referencia de C46/C47; supuesto heredado C48 = 0 y C49 = 4,5: P3 abierto)
for c, d in CP.items():
    BASE["analisis"][c] = {"valor": d["valor"], "fuente": d["fuente"], "pagina": None, "periodo": d.get("periodo"), "unidad": "mm", "naturaleza": "caso principal del ensayo (supuesto heredado si se dice)",
                           "perimetro": "consolidado", "fecha": "2023–2025", "derivacion": d["fuente"]}
# datos de Análisis reexpresados a 31-dic-2025 (4.10.1, preparación 2): se vacían en la copia de la etapa 1 y entran por la fase 1
for c, d in RX.items():
    BASE["analisis"][c] = {"valor": d["valor"], "fuente": d.get("fuente"), "pagina": d.get("pagina"), "periodo": d.get("periodo"), "unidad": "mm" if c in ("C53", "C54") else None,
                           "naturaleza": "dato reexpresado a 31-dic-2025" if not d.get("derivada") else "derivado de la Historia por rellenar_fase1_v63.py",
                           "perimetro": "consolidado", "fecha": "2025-12-31", "derivacion": d.get("fuente"), "derivada": bool(d.get("derivada")), "vaciar_en_etapa1": True,
                           "evidencia": {col: None for col in "EFGHIJKLMN"}}
    BASE["analisis"][c]["evidencia"]["M"] = ("Derivada por rellenar_fase1_v63.py de la Historia 2025 (deuda + arrendamientos − caja) ÷ EBITDA" if d.get("derivada")
                                             else "Reexpresado a 31-dic-2025 (fase1_v63.json); el valor de la etapa 1 (30-jun-2026) está en antecedentes/evidencia_anterior.json")
# filas que la 4.10.1 vació por su periodo (D4, C37, C57): las escribe de nuevo la fase 1
for celda, m in (("Análisis!D4", "Fecha REAL de ejecución del análisis (no es la fecha de la base económica, que es el 31-dic-2025)"),
                 ("Análisis!C37", "Precio de cierre de 2025 (90,10 €), ES 2025 pág. PDF 97; no contrastado con el boletín de BME"),
                 ("Análisis!C57", "Bund 10 años a fin de diciembre de 2025 (2,85 %), Bundesbank; el PDF no se conserva (ver fase1_metadatos.json)")):
    BASE["evidencia"][celda] = {col: None for col in "EFGHIJKLMN"} | {"M": m}
# evidencia ACTIVA corregida: filas con restos de la base anterior (4.10.1, concordancia_2025_evaluada y búsqueda ampliada)
BASE["evidencia"].update({
    "Análisis!B4": {"M": "Fabricante de envases de vidrio (Iberia, Reino Unido e Irlanda —Encirc— y Brasil —Vidroporto—). Italia vendida en 2024. Base 31-dic-2025: la compra de Cristalerías Toro (Chile, 2026) es posterior a la base y no se incorpora."},
    "Análisis!C28": {"N": "Base 31-dic-2025: CAGR 2020→2025 de las acciones medias ajustado por liberadas (criterio NIC 33), −0,6 %/año → Recompra. Las recompras de 2026 son posteriores a la base y no se incorporan. Diluidas = básicas todos los años (sin instrumentos dilutivos). Confianza alta en datos."},
    "Análisis!C32": {"N": "Base 31-dic-2025 (balance auditado de 2025): fondo de comercio 258,8 ÷ activo total 2.314,2 = 11,2 %. Sin deterioros del fondo de comercio 2018–2025; holgura del test no publicada. El dato del semestre de 2026 de la etapa 1 es posterior a la base (antecedentes). Confianza alta."},
    "Análisis!C38": {"N": "Dato de contexto de un tercero con fecha posterior a la base económica (Simply Wall St, 08-oct-2026): solo contraste; no entra en el cálculo ni en la conclusión. Precio objetivo medio de analistas aparte (secundario, no se usa)."},
    "Análisis!C40": {"J": "Estados de flujos consolidados 2023–2025 (CF_2023, CF_2024 y CF_2025): CFO, capex y principal de arrendamientos", "K": "Adjunto del usuario (cuentas anuales consolidadas)",
                     "L": "CF_2025, estado de flujos (pág. 7); CF_2024; CF_2023",
                     "M": "Decisión del inversor (23-oct-2026): FCF base con media 3 años 2023–25 (C46, C47, C49); C40 = FCF base → C40 = 161,2. Las demás opciones que listaba la etapa 1 (incluidos los doce meses a 30-jun-2026, posteriores a la base) están en antecedentes/evidencia_anterior.json.",
                     "N": "Base: FCF medio 2023–2025 = 161,2 (C46 335,4 − C47 169,7 − C49 4,5; supuesto heredado C49, P3 abierto). Los doce meses a 30-jun-2026 de la etapa 1 son posteriores a la base (antecedentes). La cifra de FCF de la guía de la empresa (APM, variación de deuda neta) no es comparable."},
    "Análisis!C41": {"L": "ES 2025 págs. PDF 97 (precio) y 67 (acciones)", "M": "90,10 € × 35,182858 millones de acciones en circulación (35.206.258 emitidas − 23.400 propias) = 3.169,9755058 mm (producto exacto, sin redondeo).",
                     "N": "Base 31-dic-2025. La compañía da 3.172 mm sobre las acciones emitidas. Sin ajustes por la ampliación liberada ni por la autocartera de 2026 (posteriores a la base). Confianza alta."},
    "Análisis!C46": {"J": "Estados de flujos consolidados 2023–2025 (CF_2023, CF_2024 y CF_2025)", "L": "EF2025 p.198; EF2024 p.197 (estados de flujos)",
                     "M": "Decisión del inversor (23-oct-2026): FCF base con media 3 años 2023–25 (C46, C47, C49) → C46 = 335,4 (CFO medio 2023–2025; fase1_historia.py construye 335,413; el caso principal conserva la precisión de referencia, como en la 4.10.1)."},
    "Análisis!C47": {"M": "Decisión del inversor (23-oct-2026): FCF base con media 3 años 2023–25 (C46, C47, C49); C40 = FCF base → C47 = 169.7. Las alternativas que listaba la etapa 1 (incluidos los doce meses a 30-jun-2026, posteriores a la base) están en antecedentes/evidencia_anterior.json."},
    "Análisis!C48": {"K": "Adjunto del usuario (cuentas anuales consolidadas)", "L": "EF2025 p.198 (estado de flujos)"},
    "Análisis!C50": {"G": "2019–2025", "J": "Memoria consolidada e Informe de remuneraciones EF2025"},
    "Análisis!C55": {"M": "Acciones en circulación = 35.206.258 emitidas − 23.400 propias = 35.182.858 (sin instrumentos dilutivos: diluidas = básicas).",
                     "N": "Base 31-dic-2025. No es la media anual ponderada (35,206 M, pág. PDF 82). La ampliación liberada de 2026 es posterior a la base y no se incorpora. Confianza alta."},
    "Análisis!C97": {"G": "hasta 31-dic-2025 (base económica)",
                     "M": "La evidencia de la etapa 1 (fuente secundaria con operaciones de 2026, posteriores a la base) está en antecedentes/evidencia_anterior.json; la fase A juzga C97 con las entradas hasta la base y lo documenta en N."},
    "Análisis!C76": {"G": "31-dic-2025 (no se informa con el motor B)", "K": "Adjunto del usuario (ES 2025, balance)", "L": "ES 2025 págs. PDF 9–10",
                     "M": "Con el motor B la celda no se informa: el puente ya suma la caja (108,352) y resta deuda, arrendamientos, pensiones y minoritarios a 31-dic-2025. El cálculo de la etapa 1 (caja y deuda a 30-jun-2026) está en antecedentes."},
})


def traza(clase, confianza, fuente, justificacion, materialidad):
    return {"clase": clase, "confianza": confianza, "fuente_o_condicion": fuente, "justificacion": justificacion, "materialidad": materialidad}


MAT = "la mide configuracion_v64_variantes.json (paso 10, variantes calculadas sobre copias del libro) y la evalúa la fase C"
CONF_EXP = {
    "tipo": "configuracion_economica_motor_B", "version_formato": 1, "plantilla_requerida": "V6.4 experimental", "modo": "Experimental",
    "naturaleza": ("Configuración de DEMOSTRACIÓN del encargo 4.11 (§9), elegida para comprobar el sistema y no por su valor: ejercita N1, N2, R1, el factor f del S2C (SR1), "
                   "la cartera P0 y las bases históricas. NO es una adopción: D-N1, D-N2, D-N3, D-N3b–e y P-M1 siguen sin firmar."),
    "N1": {"valor": 0.220541332769837, "fuente": "…_4_7_1/financiero/matriz.json (t_rec): media del tipo efectivo 2023–2025 de continuadas con todas las líneas de la conciliación",
           "periodo": "2023–2025", "perimetro": "continuadas", "clase": "derivado de datos publicados", "escudo": "Vinculado al tipo aplicado a NOPAT"},
    "N2": {"valor": 0.18546672136199518, "perimetro": "continuadas (2020–2022 sin el segmento Italia; 2023 reexpresado; 2024–2025 publicados)",
           "procedencia": "…_4_7_1/financiero/matriz.json (m_rec): media del ciclo 2020–2025 del margen EBIT de continuadas"},
    "N3": {"regla": "R1 · solo circulante; capacidad conservada", "existencias": 252.454, "deudores": 315.821, "acreedores": 352.841,
           "fuente": "CF_2025 (cuentas consolidadas 2025, inglés), balance a 31-dic-2025, págs. 2–3 (existencias, deudores y acreedores comerciales); igual que la 4.7.1"},
    "PM1": {"estructura": "SR1 · suma con S2C reestimado", "familia": "Λ · (λ − 1) × amortización que se repone", "lambda": 1.15, "theta": None,
            "convencion_anios": "Plana", "convencion_terminal": "Proporcional a las ventas", "roic_terminal": "ROIC de la fase B sin cambio",
            "cartera": "P0 · no se repone (explícito)", "cartera_anual": 4.492, "cartera_vnc": 21.858, "cartera_historica": [0, 0, 0, 4.921, 4.492],
            "cartera_fuente": "Nota de intangibles 2024–2025 (cartera de clientes de Vidroporto): amortización 4,921 (2024) y 4,492 (2025), valor neto 21,858 a 31-dic-2025 (…_4_8/scripts/analisis_pm1.py, ES 2025 págs. 52–53). 2021–2022 = 0 (no había cartera); 2023 = 0: dos meses de Vidroporto, no publicada por separado (supuesto)."},
    "trazabilidad": {
        "modo": traza("convención", "alta", "encargo 4.11 §9: expediente completo con N1–N3 y una estructura P-M1 explícita de demostración", "comprobar la integración con agentes reales; ninguna configuración se adopta", "sin efecto propio: el efecto es el de cada parámetro"),
        "N1.tipo": traza("derivado de datos publicados", "media", "propuesta T1 de la 4.7 (D-N1 sin firmar)", "el tipo de la Historia (C52, 20,0 %) incluye 2021–2022 con Italia y deducciones extraordinarias; T1 es la media 2023–2025 de continuadas", MAT + "; en la 4.7.1 (libro 4.6.1) T1 sola: ponderado 69,53 frente a 70,50"),
        "N1.escudo": traza("convención", "media", "configuración de compatibilidad de la V6.3 (el mismo tipo en NOPAT y en el escudo)", "no se separa el escudo sin una decisión (D-N6-τ de la 4.10)", MAT),
        "N2.margen": traza("derivado de datos publicados", "media", "propuesta M1 de la 4.7 (D-N2 sin firmar)", "C49 (16,9 %) mezcla perímetros (Italia hasta 2022, Brasil desde 2023); M1 es el ciclo 2020–2025 de continuadas. Es el margen de PARTIDA, no el objetivo del NORMAL", MAT),
        "N3.regla": traza("hipótesis", "media", "propuesta R1 de la 4.7.1 (D-N3 sin firmar)", "con ventas que caen no se recupera capital fijo: solo se libera circulante; la capacidad conservada sirve a la recuperación. Que la regla cuadre no demuestra la conservación", MAT + "; solo actúa en el MALO (ventas que caen)"),
        "N3.circulante": traza("dato publicado", "alta", "balance consolidado a 31-dic-2025 (CF_2025 págs. 2–3)", "circulante comercial = existencias + deudores − acreedores, sobre las ventas de 2025 (14,70 %)", MAT),
        "PM1.estructura": traza("hipótesis", "baja", "estructuras de la 4.8.1 (R-F1); ninguna elegida (D-N3b revisada sin firmar)", "SR1 se elige para la DEMOSTRACIÓN porque ejercita el factor f, D_hist con la cartera y P0; no es la de mayor valor (H) ni la de menor (S)", MAT + "; en la 4.8.1 (libro 4.6.1): SR1·Λ1,15 ponderado 62,47 frente a REF 69,24"),
        "PM1.familia": traza("hipótesis", "baja", "familia Λ de la 4.8.1", "Λ mide la reposición a coste corriente sobre la amortización que se repone; Θ necesitaría θ, no observado (Q-E1)", MAT),
        "PM1.parametro": traza("hipótesis", "baja", "λ central de la 4.8 tras la crítica independiente (1,15; rango 1,10–1,25)", "desfase de inflación de una vida útil de 8–16 años; no es una medición del mantenimiento", MAT),
        "PM1.convencion_anios": traza("convención", "media", "convención de la 4.8/4.8.1 (amortización de 2025 plana en los años 1–10)", "la del motor; la proporcional a ventas se calcula como variante", MAT),
        "PM1.convencion_terminal": traza("convención", "media", "convención de la 4.8.1 para Λ (amortización proporcional a las ventas en el terminal)", "continuidad con el crecimiento perpetuo; la alternativa «crece con g» se calcula como variante", MAT),
        "PM1.roic_terminal": traza("convención", "media", "definición de SR1 (encargo 4.11 §4): el ROIC del terminal no cambia", "si el ROIC_lp de la fase B ya es neto de reposición está sin decidir (Q-ROIC1): SR2 se calcula como variante", MAT),
        "PM1.cartera": traza("dato publicado", "media", "nota de intangibles 2024–2025; 2023 = 0 por supuesto", "la amortización de la cartera de clientes no se repone (P0, 4.8): se suma al FCF mientras dura (≈ 4,9 años)", MAT + "; en la 4.8 P0 sola: +0,49 de ponderado"),
    },
}
ALC_EXP = {"tipo": "ensayo_exploratorio", "aviso": ("ENSAYO 4.11 CON LA PLANTILLA V6.4 EXPERIMENTAL (motor B) Y BASE ECONÓMICA 31-dic-2025: configuración de DEMOSTRACIÓN no adoptada "
                                                   "(N1 = T1 22,05 %, N2 = M1 18,55 %, R1, P-M1 SR1 con λ = 1,15 y P0), elegida para comprobar el sistema y no por su valor; "
                                                   "k = 3 experimental; con derecho al dividendo a cuenta. Fecha de análisis = fecha real de ejecución. No es un backtest ni una "
                                                   "valoración adoptada; ninguna estructura, λ, tipo ni margen es una convención aprobada."),
           "fuente": "configuracion/cambio_de_base_piloto.json; encargo 4.11 §9. Metadato escrito por la orquestación, no por un agente de juicio.", "fecha": "2026-11-12"}
ALC_HER = {"tipo": "ensayo_exploratorio", "aviso": ("CONTROL HEREDADO 4.11: plantilla V6.4 en MODO HEREDADO con las entradas del ensayo 2025 (4.10.1) y la evidencia corregida por el "
                                                   "cambio de base; agentes simulados con las salidas de la 4.10.1 (no es un análisis nuevo): solo compara valores y estados mecánicos "
                                                   "con la 4.10.1."), "fuente": "configuracion/cambio_de_base_control_heredado.json; encargo 4.11 §9.", "fecha": "2026-11-12"}
CONF_HER = {"tipo": "configuracion_economica_motor_B", "version_formato": 1, "plantilla_requerida": "V6.4 experimental", "modo": "Heredado",
            "naturaleza": "control heredado: la V6.4 calcula como la V6.3 (R0, reposición = amortización como límite, tipo de la Historia y margen de Palancas C8)",
            "trazabilidad": {"modo": traza("convención", "alta", "encargo 4.11 §9: control heredado limpio", "comparar con la 4.10.1", "ninguna: reproduce el heredado")}}

import sys  # noqa: E402
SALIDA = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.join(ENS, "configuracion")  # otra carpeta: para comprobar la reproducción
for nombre, destino, conf_e, alc in (("cambio_de_base_control_heredado.json", f"{CORR}/2026-11_Vidrala_ensayo_4_11/control_heredado", CONF_HER, ALC_HER),
                                     ("cambio_de_base_piloto.json", f"{CORR}/2026-11_Vidrala_ensayo_4_11/piloto", CONF_EXP, ALC_EXP)):
    c = copy.deepcopy(BASE)
    c["destino"] = destino
    c["configuracion_economica"] = conf_e
    c["alcance"] = alc
    os.makedirs(SALIDA, exist_ok=True)
    json.dump(c, open(os.path.join(SALIDA, nombre), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"configuracion/{nombre}: {len(c['analisis'])} entradas de Análisis, {len(c['evidencia'])} evidencias reescritas, modo {conf_e['modo']}")
