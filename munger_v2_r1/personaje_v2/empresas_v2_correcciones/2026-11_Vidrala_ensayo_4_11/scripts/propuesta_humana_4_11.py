#!/usr/bin/env python3
"""Escribe la propuesta humana única y agrupada de la 4.11 (encargo §10): propuestas/PROPUESTA_HUMANA_4_11.md y propuesta_humana_4_11.json.

Las cifras de efecto NO se copian a mano: se leen de las salidas calculadas (variantes del paso 10 del piloto, aislamiento de C46/C47 y
C49, fase C del piloto y salidas de la batería y la réplica). Ningún campo humano se rellena (decision, fecha y decidido_por = null).
Uso (desde munger_v2_r1/): python3 -I …/2026-11_Vidrala_ensayo_4_11/scripts/propuesta_humana_4_11.py
"""
import json
import os
import re

AQUI = os.path.dirname(os.path.abspath(__file__))
ENS = os.path.dirname(AQUI)
PIL = os.path.join(ENS, "piloto", "Vidrala")
OUT = os.path.join(ENS, "propuestas")


def j(p):
    return json.load(open(p, encoding="utf-8"))


def e(x, d=2):
    return f"{x:,.{d}f}".replace(",", " ").replace(".", ",").replace(" ", ".") if isinstance(x, (int, float)) else "—"


def es(x, d=2):
    """Diferencia con signo (+ / −)."""
    if not isinstance(x, (int, float)):
        return "—"
    return ("+" if x > 0 else "−" if x < 0 else "") + e(abs(x), d)


def main():
    var = {v["clave"]: v for v in j(os.path.join(PIL, "configuracion_v64_variantes.json"))["variantes"]}
    ais = {v["clave"]: v for v in j(os.path.join(ENS, "resultados", "aislamiento_entradas_4_11.json"))["variantes"] if "fallo" not in v}
    fc = j(os.path.join(PIL, "fase_c.json"))
    cv = fc.get("configuracion_v64") or {}
    mant = cv.get("mantenimiento") or {}
    par = {p["clave"]: p for p in cv.get("parametros") or []}
    st = j(os.path.join(PIL, "estado_pipeline.json"))
    pr = j(os.path.join(PIL, "precio.json"))
    rl = {v["clave"]: v for v in j(os.path.join(ENS, "resultados", "rango_lambda_4_11.json"))["variantes"]}
    ps_var = [x["precio_si"] for x in var.values()]

    def v(clave, campo="ponderado"):
        return var[clave][campo]

    def fila(clave):
        return f"ponderado {e(v(clave))} y precio de Sí {e(v(clave, 'precio_si'))} (zona {var[clave]['zona']})"

    her, act = "heredado", "activa"
    base = (f"Piloto 4.11 (base 31-dic-2025, palancas de su fase B; precio 90,10 €): heredado {fila(her)}; configuración de demostración "
            f"(T1 · M1 · R1 · SR1 · Λ 1,15 · P0) {fila(act)}. Variantes calculadas sobre copias del libro evaluado "
            "(piloto/Vidrala/configuracion_v64_variantes.md); la zona es «caro» en todas. El precio de Sí usa k = 3, que sigue siendo una "
            "convención experimental, y el ensayo no es un backtest: la fecha de análisis es la real y la base, el 31-dic-2025.")
    D = [
        {"id": "D411-PLANTILLA", "grupo": "diseño (plantilla y pipeline)", "relacion": "ESPECIFICACION_INTEGRACION_4_10.md; encargo 4.11",
         "pregunta": "¿Se usa la plantilla V6.4 experimental (motor B) en los ensayos supervisados con dos o tres empresas ya analizadas, con la V6.3 como plantilla por omisión y el modo heredado como control?",
         "recomendacion": ("Sí, como plantilla de ENSAYO, no como sustituta de la V6.3. El modo heredado reproduce la V6.3 celda a celda (0 diferencias en 120.168 celdas) y el "
                           "pipeline de la 4.10.1 (|Δ| = 0); la réplica independiente coincide en 117/117 casos; las configuraciones incompletas se rechazan con su motivo; "
                           "la conciliación anual y terminal es visible; la configuración forma parte del material auditado y su cambio retira la aprobación."),
         "alternativas": ["no usarla hasta adoptar las convenciones (N1–N3 y P-M1 no podrían ensayarse en otras empresas)",
                          "hacerla la plantilla por omisión (no recomendado: las convenciones siguen sin firmar)"],
         "evidencia": "REGISTRO_PRUEBAS_4_11.md (batería de 58, réplica 117/117, control heredado); resultados/seleccion_inversa_4_11.md; v6/v64_experimental/docs/README_V6.4_experimental.md",
         "efectos": ("ninguno en los expedientes V6.3: la selección es explícita y un expediente de una versión se detiene con código 2, sin escribir nada, en la otra, en los dos "
                     "sentidos (también una copia de un expediente V6.3 cerrado: resultados/seleccion_inversa_4_11.md); las filas V6.4 se publican en su propio resumen "
                     "(resumen_v2_v64_experimental.csv); si la fase A de otra empresa elige el motor A o el C, el expediente termina en el límite del modelo, sin forzar el motor"),
         "si_no_se_adopta": "la integración queda construida pero sin uso: el siguiente hito (dos o tres empresas) no puede ejecutarse con N1–N3 y P-M1"},
        {"id": "D411-N1", "grupo": "financiera (convención de Vidrala)", "relacion": "D-N1 (4.7); D-TAU-HOJA (4.10.1); D-N6-τ (4.10)",
         "pregunta": "¿Qué tipo impositivo aplica el motor B de Vidrala al NOPAT: el de la Historia (C52, 20,0 %, media de cinco años), T1 (22,05 %, media 2023–2025 de continuadas con toda la conciliación) u otro (T2, 24,3 %, el tipo efectivo de 2025)? ¿El escudo de la deuda en r_op usa el mismo tipo o el de la Historia?",
         "recomendacion": ("T1 con el escudo vinculado, como tipo normalizado del ensayo; T2 como sensibilidad. C52 mezcla 2021–2022 con Italia y deducciones "
                           "extraordinarias; T1 es la media de continuadas con toda la conciliación (4.7). Es una convención: no se ha medido un tipo «verdadero»."),
         "alternativas": ["C52 (20,0 %, heredado)", "T2 (24,3 %)", "T1 con el escudo al tipo de la Historia (separado)"],
         "evidencia": "…_4_7_1/financiero/matriz.json (t_rec); …_4_7/INFORME_FINANCIERO_N1_N3.md; fase C del piloto (configuracion_v64.parametros N1)",
         "efectos": f"solo N1 frente al heredado: {es(var['solo_N1']['delta_ponderado_frente_a_heredado'])} € de ponderado y {es(var['solo_N1']['delta_precio_si_frente_a_heredado'])} € de precio de Sí; con T2 (4.10.1, libro 4.10.1) el precio de Sí bajaba de 66,52 a 62,71 €",
         "si_no_se_adopta": f"se mantiene C52: el NOPAT usa un tipo que incluye un perímetro y deducciones que ya no están (en este piloto, el ponderado queda {e(-var['solo_N1']['delta_ponderado_frente_a_heredado'])} € más alto que con T1)"},
        {"id": "D411-N2", "grupo": "financiera (convención de Vidrala)", "relacion": "D-N2 (4.7); D-C8-MARGEN (4.10.1)",
         "pregunta": "¿Qué margen EBIT de partida (año 0) usa el motor B de Vidrala: la regla de Palancas C8 («Media del ciclo» = C49, 16,9 %, que mezcla Italia hasta 2022 y Brasil desde 2023) o M1 (18,55 %, media 2020–2025 de continuadas)?",
         "recomendacion": ("M1 como margen de partida mientras no llegue el dato por segmento del perímetro de 2025 (D-C8-MARGEN). Es el margen del año 0, no el objetivo del "
                           "NORMAL, que sigue siendo un juicio de la fase B."),
         "alternativas": ["Palancas C8 (heredado)", "el último año (2025)"],
         "evidencia": "…_4_7_1/financiero/matriz.json (m_rec); fase C del piloto (configuracion_v64.parametros N2)",
         "efectos": f"solo N2 frente al heredado: {es(var['solo_N2']['delta_ponderado_frente_a_heredado'])} € de ponderado y {es(var['solo_N2']['delta_precio_si_frente_a_heredado'])} € de precio de Sí",
         "si_no_se_adopta": f"el año 0 parte de una media con otro perímetro (con M1, el ponderado de este piloto cambiaría {es(var['solo_N2']['delta_ponderado_frente_a_heredado'])} €)"},
        {"id": "D411-N3", "grupo": "financiera (regla del modelo)", "relacion": "D-N3 (4.7.1); D-MALO-CAPITAL (4.10.1)",
         "pregunta": "¿Qué regla de reinversión con ventas que caen usa el motor B: R0 (simétrica: al caer las ventas se libera capital fijo) o R1 (solo se libera circulante; la capacidad se conserva y sirve a la recuperación)?",
         "recomendacion": ("R1 para Vidrala: en una empresa de hornos de vidrio la capacidad no se vende cuando cae la demanda. Límite declarado: el terminal no usa "
                           "la capacidad conservada (definición de la 4.7.1/4.8.1, prudente) y, en un escenario cuyas ventas no superan el máximo anterior en ningún "
                           "año, la palanca S2C no actúa (MALO del piloto)."),
         "alternativas": ["R0 (heredada)"],
         "evidencia": "…_4_7_1/INFORME_N3_SUBSANACION.md; batería B (caída, recuperación y nuevo máximo); fase C del piloto (configuracion_v64.parametros N3)",
         "efectos": f"solo R1 frente al heredado: {es(var['solo_R1']['delta_ponderado_frente_a_heredado'])} € de ponderado (solo cambia el MALO: {e(var[her]['V'][0])} → {e(var['solo_R1']['V'][0])})",
         "si_no_se_adopta": "con R0 el MALO libera capital fijo al caer las ventas (D-MALO-CAPITAL), lo que da más valor al escenario malo"},
        {"id": "D411-PM1-ESTRUCTURA", "grupo": "financiera (P-M1: estructura de la reposición)", "relacion": "D-N3b revisada y D-N3e (4.8.1); Q-ROIC1 (4.9); Q-E1–Q-E3",
         "pregunta": "¿Qué estructura relaciona la reposición por encima de la amortización con la inversión para crecer en Vidrala: sin requisito adicional, H (la inversión para crecer también repone), S (se suman sin reestimar), SR1 (suma con el S2C reestimado), SR2 (SR1 y ROIC del terminal × f) o SRF (suma con la inversión fija reestimada)?",
         "recomendacion": ("No adoptar todavía una estructura central: λ y θ no están medidos (faltan el desglose de la inversión y el calendario de hornos, Q-E1–Q-E3) "
                           "y la elección entre SR1 y SR2 depende de Q-ROIC1. Para los ensayos supervisados, usar una configuración declarada como ensayo "
                           f"y enseñar siempre el rango de las estructuras. Evaluación de la fase C del piloto, íntegra: «{mant.get('evaluacion', '—')}» "
                           f"(estructura más coherente según la fase C: {mant.get('estructura_mas_coherente') or 'ninguna con base suficiente'}). Nota de la revisión "
                           "interna (O8): el 33 % y λ ≈ 1,46 se miden sobre el exceso respecto de la amortización total (229,4); con la base que usa la hoja, el exceso "
                           "sobre la amortización que se repone (238,8), serían un 31 % y λ ≈ 1,48."),
         "alternativas": ["sin requisito adicional (reposición = amortización, límite declarado de la V6.3)", "H", "S", "SR1", "SR2", "SRF"],
         "evidencia": "…_4_8_1/INFORME_REINVERSION_4_8_1.md; piloto/Vidrala/fase_c.json (configuracion_v64.mantenimiento); configuracion_v64_variantes.md",
         "efectos": (f"con Λ = 1,15 y P0, frente a la activa sin P-M1 ({e(v('activa_sin_PM1'))}): H {e(v('estructura_H'))}, SRF {e(v('estructura_SRF'))}, "
                     f"SR2 {e(v('estructura_SR2'))}, SR1 {e(v(act))}, S {e(v('estructura_S'))} de ponderado; precios de Sí de {e(v('estructura_S', 'precio_si'))} a "
                     f"{e(v('estructura_H', 'precio_si'))}; zona caro en todas"),
         "si_no_se_adopta": f"el modelo sigue suponiendo reposición = amortización (sin requisito), que es la hipótesis que P-M1 cuestiona: según la estructura, el ponderado de este piloto estaría entre {e(v('activa_sin_PM1') - v('estructura_H'))} y {e(v('activa_sin_PM1') - v('estructura_S'))} € por encima"},
        {"id": "D411-PM1-PARAMETRO", "grupo": "financiera (P-M1: parámetro y convenciones)", "relacion": "D-N3b revisada (4.8.1)",
         "pregunta": "Si se usa una estructura con requisito: ¿λ (familia Λ) como un punto (1,15) o como un rango (1,10–1,25)? ¿Requisito plano o proporcional a las ventas en los años 1–10, y proporcional a las ventas o creciendo con g en el terminal? ¿ROIC del terminal sin cambio (salvo SR2)?",
         "recomendacion": ("λ como rango de sensibilidad (1,10–1,25), no como un punto; años planos y terminal proporcional a las ventas (continuidad con el crecimiento "
                           "perpetuo); ROIC sin cambio salvo en SR2. Son convenciones: λ es una hipótesis de inflación de reposición, no una medición."),
         "alternativas": ["λ = 1,15 como punto", "familia Θ (θ × exceso histórico; θ no observado)", "años proporcionales a las ventas", "terminal que crece con g"],
         "evidencia": "…_4_8/INFORME_PM1.md; …_4_8_1/financiero/rf_resultados.json; configuracion_v64_variantes.md",
         "efectos": (f"extremos del rango, recalculados en el libro (resultados/rango_lambda_4_11.md): λ = 1,10, ponderado {e(rl['parametro_minimo']['ponderado'])} y precio de Sí "
                     f"{e(rl['parametro_minimo']['precio_si'])} ({es(rl['parametro_minimo']['delta_precio_si_frente_a_activa'])} €); λ = 1,25, ponderado "
                     f"{e(rl['parametro_maximo']['ponderado'])} y precio de Sí {e(rl['parametro_maximo']['precio_si'])} ({es(rl['parametro_maximo']['delta_precio_si_frente_a_activa'])} €); "
                     f"zona {rl['parametro_minimo']['zona']} y {rl['parametro_maximo']['zona']}. Convención de los años alternativa: "
                     f"{es(var['convencion_anios_alternativa']['delta_ponderado_frente_a_activa'])} €; del terminal: "
                     f"{es(var['convencion_terminal_alternativa']['delta_ponderado_frente_a_activa'])} € de ponderado frente a la activa"),
         "si_no_se_adopta": "cada ensayo tendrá que declarar sus convenciones (la plantilla no tiene ninguna por omisión)"},
        {"id": "D411-PM1-CARTERA", "grupo": "financiera (P-M1: cartera de clientes)", "relacion": "D-N3c (4.8)",
         "pregunta": "¿La amortización de la cartera de clientes de Vidroporto (4,492 al año; valor neto 21,858) se trata como no repuesta (P0) o como el resto de la amortización (legado)?",
         "recomendacion": ("P0: la amortización de una relación con clientes adquirida no es una inversión de reposición; está documentada en la nota de intangibles y se agota en unos cinco años. "
                           "Nota de la revisión interna (O3): los ceros históricos de 2021–2023 son compatibles con la nota 7 de las cuentas de 2021 a 2024, que muestra una cartera "
                           "anterior (Santos Barosa, coste 13,237) totalmente amortizada a 31-dic-2020, y la de Vidroporto, que entra en el saldo reexpresado de 2023; el texto "
                           "de la fuente podría ser más preciso. Ningún cero se confirma aquí: eso corresponde a la persona responsable."),
         "alternativas": ["legado (se repone con la amortización)"],
         "evidencia": "…_4_8/scripts/analisis_pm1.py; ES 2025 págs. 52–53",
         "efectos": f"P0 sin requisito frente a la activa sin P-M1: {es(v('activa_solo_P0') - v('activa_sin_PM1'))} € de ponderado",
         "si_no_se_adopta": f"se trata como reposición una amortización que no se repone (en este piloto, {e(v('activa_solo_P0') - v('activa_sin_PM1'))} € de ponderado)"},
        {"id": "D411-TERMINAL-R1", "grupo": "regla del modelo (límite)", "relacion": "observación de la réplica independiente (replica/INFORME_REPLICA.md)",
         "pregunta": "¿Se mantiene el terminal prudente con R1 (carga la inversión fija para crecer al ritmo g aunque en el MALO las ventas sigan por debajo del máximo conservado) o se especifica un terminal que reconozca la capacidad sobrante?",
         "recomendacion": "Mantener el prudente (definición de la 4.7.1/4.8.1) y especificar la alternativa solo si en otra empresa el MALO depende materialmente de ello.",
         "alternativas": ["especificar y probar un terminal con capacidad sobrante (exige una regla nueva, réplica y pruebas)"],
         "evidencia": "réplica: 16,39 millones de inversión fija en el año 11 del MALO de H_L1.15 con las ventas por debajo del máximo",
         "efectos": "no calculado: no hay especificación alternativa (el efecto iría solo al MALO y sería a favor del valor)",
         "si_no_se_adopta": "sigue la regla prudente, declarada como límite"},
        {"id": "D411-P3", "grupo": "financiera (dato condicionado)", "relacion": "D-P3 (4.10); D-N4-C48 (4.9); Q-N4a",
         "pregunta": "¿C49 (arrendamientos · principal) sigue en 4,5 (supuesto heredado, situación A de P3) o pasa a 6,764 (pago total P+I de la nota 8 que construye fase1_historia.py)?",
         "recomendacion": "Mantener 4,5 marcado como condicionado hasta Q-N4a (como recomendó la 4.10); no tiene efecto en la valoración del motor B.",
         "alternativas": ["C49 = 6,764 (pago total)", "situación B de la 4.10 (C48 = 2,254 y C49 = 4,5)"],
         "evidencia": "resultados/aislamiento_entradas_4_11.md; …_4_10/INFORME_FINANCIERO_4_10.md",
         "efectos": f"en el piloto: {es(ais['C49_pago_total']['delta_ponderado'], 6)} € de ponderado y {es(ais['C49_pago_total']['delta_precio_si'], 6)} € de precio de Sí; FCF base (C52) {e(ais['control']['fcf_base_C52'], 3)} → {e(ais['C49_pago_total']['fcf_base_C52'], 3)}",
         "si_no_se_adopta": "sigue el supuesto heredado, declarado; el FCF base y f quedan con esa reserva"},
        {"id": "D411-C46C47", "grupo": "precisión de entrada", "relacion": "4.10.1 (variante de precisión, 0 €)",
         "pregunta": "En expedientes nuevos, ¿C46 y C47 toman los valores que construye fase1_historia.py (335,413 y 169,668) en lugar de la precisión de referencia (335,4 y 169,7)?",
         "recomendacion": "Sí en los expedientes nuevos: es precisión, no juicio. En este ensayo se conserva la de referencia para comparar con la 4.10.1.",
         "alternativas": ["conservar la precisión de referencia"],
         "evidencia": "resultados/aislamiento_entradas_4_11.md",
         "efectos": f"en el piloto: {es(ais['C46_C47_precisos']['delta_ponderado'], 6)} € de ponderado; FCF base (C52) {e(ais['control']['fcf_base_C52'], 3)} → {e(ais['C46_C47_precisos']['fcf_base_C52'], 3)}",
         "si_no_se_adopta": "ninguna consecuencia en el valor del motor B; una diferencia de redondeo en el FCF base"},
        {"id": "D411-RF-FUENTE", "grupo": "documental (fuente)", "relacion": "D-RF-FUENTE (4.10.1)",
         "pregunta": "¿Se incorpora al paquete el PDF del Bundesbank (rendbund-data.pdf, ejemplar de 11-nov-2026) que sostiene rf = 2,85 % de fin de diciembre de 2025, con su huella?",
         "recomendacion": ("Sí: que la persona responsable adjunte el PDF descargado (la revisión externa registró SHA-256 6ace5ac7785ecca9f8f3d56ce12f49fb2acbe4b9418dd84def46fc63c516a9dd) "
                           "para incorporarlo con su huella en la siguiente entrega. Desde esta consola no se puede descargar (proxy 403)."),
         "alternativas": ["mantener la cita documentada sin el PDF (límite declarado)"],
         "evidencia": "configuracion/cambio_de_base_piloto.json (metadatos.tasa_sin_riesgo.fuente)",
         "efectos": "ninguno en la valoración del motor B (4.10.1: C1 con rf 0,0329 y el ensayo con 0,0285 dan el mismo valor); trazabilidad de la fuente",
         "si_no_se_adopta": "la rf sigue apoyada en una lectura web sin bytes conservados"},
        {"id": "D411-MATERIALIDAD", "grupo": "regla del personaje (estado y conclusión)", "relacion": "revisión interna H4; tercer aviso de la auditoría del piloto; personaje §14 y §15; Anexo B §B.6.7; Anexo D §D.12",
         "pregunta": ("Cuando un parámetro experimental es material solo para el precio objetivo y no para la acción, ¿qué regla manda? (A) La de datos ausentes (S-19): si sin el "
                      "dato no se sostiene «esperar con precio objetivo», no se emite, el cubo queda en Vigilar sin acción y el estado es pendiente_de_datos. (B) La del fundamento "
                      "(B.6.7): concluido con «esperar» y el objetivo marcado provisional, con la hipótesis que lo condiciona."),
         "recomendacion": ("(B), con el rango del objetivo a la vista y con el campo separado en dos. Argumentos: la acción no depende de la configuración (en las "
                           f"{len(var)} variantes calculadas y en los dos extremos de λ la zona es «caro»: el precio, 90,10 €, supera el ponderado, que como máximo es "
                           f"{e(max(x['ponderado'] for x in var.values()))}); el objetivo sí depende (precio de Sí de {e(min(ps_var))} a {e(max(ps_var))} en las variantes, y de "
                           f"{e(rl['parametro_maximo']['precio_si'])} a {e(rl['parametro_minimo']['precio_si'])} en el rango de λ). Casi ninguna empresa publica el desglose entre "
                           "reposición y crecimiento: con (A), todo expediente con P-M1 activa acabaría en pendiente_de_datos y se perdería una conclusión cuya acción no depende del dato. "
                           "Para que la regla se pueda comprobar: separar material_para_conclusion en material_para_accion y material_para_objetivo, y que coherencia_v64 exija, con el "
                           "primero en true, la regla (A), y con solo el segundo, el objetivo provisional con el rango de las variantes calculadas."),
         "alternativas": ["(A) datos ausentes: pendiente_de_datos en cuanto el objetivo dependa de un parámetro sin medir",
                          "(B) con un umbral: provisional mientras el rango del objetivo en las variantes calculadas no supere un porcentaje que fije la persona responsable; por encima, (A)",
                          "dejarlo al criterio de la fase C, caso por caso, como en el piloto (no se puede comprobar mecánicamente)"],
         "evidencia": "piloto/Vidrala/fase_c.json (configuracion_v64.parametros y revision_datos_ausentes); piloto/Vidrala/auditoria.md (tercer aviso); revision_interna/REVISION_INTERNA_4_11.md (H4); resultados/rango_lambda_4_11.md",
         "efectos": (f"en el piloto: con (B), concluido · Vigilar · esperar, objetivo provisional {e(pr.get('precio_si'))} €; con (A), pendiente_de_datos, cubo Vigilar, sin acción ni "
                     "objetivo; en los dos casos, sin compra. En modo heredado el mismo dato ausente no mueve ninguna cifra (la V6.3 no tiene parámetro de reposición)"),
         "si_no_se_adopta": "cada fase C lo decide caso por caso y la auditoría no tiene una regla con la que comprobarlo: conviene decidirlo antes de probar otras empresas"},
        {"id": "D411-DOMINIOS", "grupo": "regla del modelo (avisos de dominio)", "relacion": "revisión interna H13; README de la V6.4 §8.9",
         "pregunta": ("¿Se añaden avisos (no rechazos) para los dominios que la plantilla no comprueba: f por encima de un umbral, inversión fija para crecer negativa "
                      "(1 ÷ (S2C·f) < NWC, en los años o en el terminal, también en SRF) y g ≤ 0 con R1 en un libro escrito a mano? ¿Con qué umbral para f?"),
         "recomendacion": ("Sí, como avisos en el libro o en el pipeline que lleguen a la fase C y a la auditoría; ninguno debe rechazar ni recortar, porque el encargo prohíbe "
                           "recortar dominios. Como punto de partida para el umbral, f > 1,5 (el S2C reestimado más de un 50 % por encima del histórico; en el piloto, f = 1,16); "
                           "el umbral es una convención que fija la persona responsable."),
         "alternativas": ["solo declararlos como límites (como ahora)", "rechazarlos (no recomendado: sería un recorte de dominio encubierto)"],
         "evidencia": "revision_interna/REVISION_INTERNA_4_11.md (H13); v6/v64_experimental/docs/README_V6.4_experimental.md §8",
         "efectos": "ninguno en las cifras entregadas: en el piloto y en los 117 casos no aparece ninguna de esas situaciones",
         "si_no_se_adopta": "en una empresa con poco activo fijo y mucho circulante, la inversión para crecer podría salir negativa sin que nada lo señale"},
    ]
    for d in D:
        d.update({"decision": None, "fecha": None, "decidido_por": None})
    out = {"tipo": "Propuesta humana única y agrupada de la entrega 4.11 (SIN FIRMAR)",
           "aviso": "Ningún campo humano está relleno. La IA recomienda y argumenta; no decide ni adopta ninguna configuración.",
           "contexto_del_piloto": base,
           "estado_del_piloto": {"estado_analisis": st.get("estado_analisis"), "auditoria": st.get("auditoria"), "ponderado": pr.get("ponderado"), "precio_si": pr.get("precio_si"), "zona": pr.get("zona")},
           "resueltas_por_ejecucion_en_la_4_11": {"D-REBASE": "mecanismo general implementado (personaje_v2/scripts/cambiar_base.py) y usado en el control y el piloto",
                                                   "D-EVIDENCIA-2026": "evidencia activa limpiada en los expedientes nuevos de la 4.11 (el libro cerrado de la 4.10.1 no se reescribe)",
                                                   "D-MALO-CAPITAL": "R1 ya es representable: la decisión pasa a D411-N3"},
           "siguen_pendientes_sin_repetir": ["D-N7", "D-N6", "D-N4-OAF", "D-N4-reg-4.10", "D-N8", "D-N5", "D-N6-tau (ver D411-N1)", "D-N10", "D-PN1",
                                             "D-FICHA-ETAPA1", "D-C97-RECUENTO", "D-TAU-HOJA (ver D411-N1)", "D-C8-MARGEN (ver D411-N2)", "Q-E1–Q-E7", "Q-ROIC1", "Q-N4a", "Q-T1–Q-T6"],
           "decisiones": D}
    os.makedirs(OUT, exist_ok=True)
    json.dump(out, open(os.path.join(OUT, "propuesta_humana_4_11.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    md = ["# Propuesta humana única de la entrega 4.11 (agrupada, sin firmar)", "",
          "**Qué es.** Las decisiones que la persona responsable del proyecto tendría que tomar para pasar de la integración experimental a una primera versión "
          "integrada supervisada. Cada una lleva una recomendación argumentada, las alternativas, la evidencia, los efectos calculados y lo que pasa si no se adopta. "
          "**Ningún campo humano está relleno** (`propuesta_humana_4_11.json`: `decision`, `fecha` y `decidido_por` = null): la IA recomienda; no decide.", "",
          f"**Contexto.** {base}", "",
          "**Ya resueltas por ejecución en la 4.11** (el encargo las autorizaba como trabajo técnico; no se vuelven a preguntar): "
          + "; ".join(f"{k}: {v}" for k, v in out["resueltas_por_ejecucion_en_la_4_11"].items()) + ".", "",
          "**Siguen pendientes, sin repetirlas aquí:** " + ", ".join(out["siguen_pendientes_sin_repetir"]) + ".", ""]
    def cap(x):
        # (revisión interna H14) una evidencia que empieza por una ruta (carpeta/archivo, …_4_8/…) conserva su minúscula
        return x if re.match(r"^[\w.…-]+/", x) else x[:1].upper() + x[1:]
    for d in D:
        md += [f"## {d['id']} · {d['grupo']}", "", f"**Pregunta.** {d['pregunta']}", "", f"**Recomendación (argumentada, no adoptada).** {d['recomendacion']}", "",
               "**Alternativas.** " + cap("; ".join(d["alternativas"])) + ".", "", f"**Evidencia.** {cap(d['evidencia'])}.", "", f"**Efectos calculados.** {cap(d['efectos'])}.", "",
               f"**Si no se adopta.** {cap(d['si_no_se_adopta'])}.", "", f"**Relación.** {cap(d['relacion'])}.", "", "Decisión: — · Fecha: — · Decidido por: —", ""]
    open(os.path.join(OUT, "PROPUESTA_HUMANA_4_11.md"), "w", encoding="utf-8").write("\n".join(md))
    print(f"propuesta: {len(D)} decisiones · {os.path.relpath(OUT, ENS)}/PROPUESTA_HUMANA_4_11.md y propuesta_humana_4_11.json")


if __name__ == "__main__":
    main()
