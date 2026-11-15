#!/usr/bin/env python3
"""Escribe la propuesta humana de la 4.13 (encargo §9, «Las decisiones pendientes se agruparán en…»): propuestas/PROPUESTA_HUMANA_4_13.md y .json.

Tres grupos: 1) política de salida; 2) elecciones económicas por empresa; 3) ampliaciones futuras. Cada decisión lleva recomendación,
alternativas, evidencia y efectos, y las firmas vacías (decision, fecha y decidido_por = null). No vuelve a pedir autorizaciones ya
concedidas (uso experimental supervisado, reparaciones técnicas). Los precios de Sí, rangos, estados y alternativas de acciones se leen
de las salidas de los expedientes finales de la 4.13 (fichas, precio.json, variantes y alternativas de acciones). Son LITERALES, con su
documento de origen en la evidencia de cada decisión: +1,75 y +1,06 € y el criterio de 1,5 € (fases C de Vidrala); 1,2011, 1,1413 y 1,50
(dominios); 24,110, 27,051, 64,923 y 40,813 (conciliación de arrendamientos); 22,12, 22,66 y 19,83 % (configuración de Viscofan); +1,57 €
(crecimiento terminal de Vidrala); −0,55 y +0,8 € (fase C de vidrala_bloqueo); «del orden de 1 €» (fase C de Vidrala, terminal de R1).
Uso (desde munger_v2_r1/): python3 -I …/2026-11_Vidrala_ensayo_4_13/scripts/propuesta_humana_4_13.py
"""
import json
import os

AQUI = os.path.dirname(os.path.abspath(__file__))
ENS = os.path.dirname(AQUI)
OUT = os.path.join(ENS, "propuestas")
COND = os.path.join(ENS, "vidrala_condicionado", "Vidrala")
BLOQ = os.path.join(ENS, "vidrala_bloqueo", "Vidrala")
VIS = os.path.join(ENS, "viscofan", "Viscofan")
GRUPOS = (("política de salida", "1. Política de salida"), ("elección económica por empresa", "2. Elecciones económicas por empresa"),
          ("ampliación futura", "3. Ampliaciones futuras"))


def j(p):
    try:
        return json.load(open(p, encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def e(x, d=2):
    return f"{x:,.{d}f}".replace(",", " ").replace(".", ",").replace(" ", ".") if isinstance(x, (int, float)) else "—"


def estado(c):
    st, fi = j(os.path.join(c, "estado_pipeline.json")), j(os.path.join(c, "ficha.json"))
    ob = fi.get("objetivo") or {}
    dec = fi.get("decision") or {}
    return {"estado": st.get("estado_analisis"), "auditoria": st.get("auditoria"), "cubo": fi.get("cubo"), "accion": dec.get("accion"),
            "tratamiento": ob.get("tratamiento"), "valor_calculado_condicional": ob.get("valor_calculado_condicional"),
            "precio_objetivo_emitido": ob.get("precio_objetivo_emitido"), "plantilla": (fi.get("plantilla") or {}).get("version")}


def cap(t):
    return t[:1].upper() + t[1:] if t else t


def variantes(c):
    return {x.get("clave"): x for x in (j(os.path.join(c, "configuracion_v64_variantes.json")).get("variantes") or []) if isinstance(x, dict)}


def rango(c):
    ps = [x.get("precio_si") for k, x in variantes(c).items() if k != "heredado" and isinstance(x.get("precio_si"), (int, float))]
    return (min(ps), max(ps), len(ps)) if ps else (None, None, 0)


def main():
    ec, eb, ev = estado(COND), estado(BLOQ), estado(VIS)
    pc, pv = j(os.path.join(COND, "precio.json")), j(os.path.join(VIS, "precio.json"))
    vc, vv = variantes(COND), variantes(VIS)
    rc, rv = rango(COND), rango(VIS)
    alt = {x["caso"]: x for x in (j(os.path.join(ENS, "resultados", "alternativas_acciones_viscofan.json")).get("casos") or [])}
    psi = lambda d, k: (d.get(k) or {}).get("precio_si")  # noqa: E731
    D = []
    # ---------------------------------------------------------------- 1. política de salida
    D.append({"id": "D413-USO", "grupo": "política de salida",
              "pregunta": "¿Qué uso permite esta entrega? El uso experimental supervisado ya está autorizado; la pregunta es si algo de la 4.13 cambia ese alcance.",
              "recomendacion": ("Mantener el uso SUPERVISADO y EXPERIMENTAL de la 4.12 para empresas de motor B, con la V6.4 o la V6.4.1 experimental como ensayo y el modo "
                                "heredado como control, y los resultados leídos como valores calculados condicionales. No a decisiones con dinero real: siguen abiertas las "
                                "condiciones de INFORME_INTEGRACION_4_13.md §9 (convenciones y estructuras sin adoptar, hipótesis no observadas, materialidad que depende del "
                                "juicio del agente, dos empresas y ningún contraste fuera de muestra)."),
              "alternativas": ["usar solo el modo heredado (V6.3 efectiva) y dejar la capa experimental para pruebas técnicas",
                               "apoyar decisiones con dinero real ya (no recomendado: ningún APROBADO ni porcentaje de avance lo acredita)"],
              "evidencia": "INFORME_INTEGRACION_4_13.md §9; REGISTRO_PRUEBAS_4_13.md; revision_interna/REVISION_INTERNA_4_13.md",
              "efectos": "ninguno en los expedientes: es el alcance del uso",
              "si_no_se_adopta": "rige el alcance de D412-USO, que esta propuesta no cambia", "sustituye_a": "D412-USO"})
    D.append({"id": "D413-PROTOCOLO", "grupo": "política de salida",
              "pregunta": ("Con «esperar» por precio y hipótesis experimentales sin fundamento suficiente que mueven el precio objetivo, ¿qué protocolo rige: "
                           "«objetivo_condicionado» o «bloqueo_del_objetivo»? Los dos siguen como ensayos no adoptados."),
              "recomendacion": ("Para el uso supervisado, «objetivo_condicionado»: conserva lo sostenido (la acción, que no cambia en ninguna variante calculada) y marca "
                                "el objetivo como condicional con sus hipótesis. Para dinero real ninguno basta: habría que fundamentar las hipótesis que condicionan "
                                "el objetivo. No se recomienda por emitir un precio: con el mismo material, los dos protocolos dan la misma acción calculada."),
              "alternativas": ["«bloqueo_del_objetivo» siempre (trata una hipótesis sin fundamento como un dato ausente)",
                               "«objetivo_condicionado» solo si todo el rango calculado del precio de Sí queda por debajo del precio"],
              "evidencia": "vidrala_condicionado/ y vidrala_bloqueo/ (mismo material económico; 4.12: COMPARACION_PROTOCOLOS_4_12.md)",
              "efectos": (f"Vidrala, mismo material: con «objetivo_condicionado», {ec['estado']} · {ec['accion']} · {ec['tratamiento']} (valor calculado condicional "
                          f"{e(ec['valor_calculado_condicional'])} €); con «bloqueo_del_objetivo», {eb['estado']} · {eb['accion'] or 'sin acción'} · {eb['tratamiento']} "
                          f"(el mismo valor, no emitido). Rango calculado del precio de Sí: {e(rc[0])}–{e(rc[1])} € en {rc[2]} variantes; precio {e(pc.get('precio'))} €"),
              "si_no_se_adopta": "cada expediente experimental declara su protocolo; sin él no se emite ningún objetivo oficial (objetivo_sin_protocolo)",
              "sustituye_a": "D412-PROTOCOLO"})
    D.append({"id": "D413-FUNDAMENTO", "grupo": "política de salida",
              "pregunta": ("¿Qué criterio decide que una hipótesis es material para el objetivo y si tiene fundamento suficiente? Hoy es el juicio económico de la fase C, "
                           "con su base declarada (calculada, juicio económico o no determinada) y sin umbral adoptado. Además sigue abierta la regla de D412-FUNDAMENTO "
                           "para «comprar»."),
              "recomendacion": ("Mantener el juicio declarado con su base y su evidencia, sin umbral, y adoptar dos reglas que no dependen de un número: (1) con «comprar», "
                                "todo parámetro activo de clase «hipótesis» cuenta como sin fundamento suficiente y va a D10; (2) una materialidad «no determinada» de un "
                                "parámetro sin fundamento condiciona el objetivo (ya es así en el código). Si se quiere un umbral, que lo fije la persona responsable, "
                                "relativo al precio de Sí, y que se pruebe en más empresas antes de usarlo."),
              "alternativas": ["umbral absoluto por empresa (por ejemplo, 1,5 € del precio de Sí, el criterio propio de un agente)",
                               "umbral relativo (por ejemplo, un porcentaje del precio de Sí) común a todas las empresas",
                               "dejarlo todo al juicio de la fase C, también con «comprar» (como ahora)"],
              "evidencia": ("vidrala_condicionado/Vidrala/fase_c.json y vidrala_bloqueo/Vidrala/fase_c.json (configuracion_v64.parametros); "
                            "REGISTRO_AVANCE_4_13.md (observación de materialidad); revision_interna/REVISION_INTERNA_4_13.md (R14); Anexo D §D.13"),
              "efectos": (f"Con el mismo material de Vidrala, dos agentes trazan líneas distintas: el de condicionado juzga no material N1 (+1,75 € de precio de Sí); "
                          f"el de bloqueo declara un criterio propio de 1,5 € y lo juzga material, aunque fundado. PM1.roic_terminal (+1,06 € en SR2) queda fuera de "
                          f"los condicionantes en los dos por juicio. Ninguno concluye «comprar», así que la regla (1) no cambia ningún expediente de la 4.13"),
              "si_no_se_adopta": "la materialidad para el objetivo sigue dependiendo del agente, con su base declarada y revisada por la auditoría",
              "sustituye_a": "D412-FUNDAMENTO"})
    D.append({"id": "D413-DOMINIOS", "grupo": "política de salida",
              "pregunta": ("¿Los avisos de dominio (factor f, inversión fija para crecer negativa, terminal de R1 sin máximo conservado, S2C inerte), ahora calculados en "
                           "todas las variantes y agrupados, siguen como avisos sin umbral?"),
              "recomendacion": ("Sí, con sus valores y la conclusión a la que afectan, mientras solo haya dos empresas. Las cotas dependen de las bases y del perímetro: "
                                "SRF deja de estar definida en λ = 1,2011 con el perímetro NIIF 16 de Viscofan (1,1413 con «Caja») y por encima de 1,50 en Vidrala."),
              "alternativas": ["umbral fijo para f (por ejemplo, 1,25) que bloquee «comprar»", "umbral por empresa en su configuración"],
              "evidencia": "personaje_v2/scripts/dominios_v64.py (agrupar); viscofan/resultados/dominios_perimetro.md; configuracion_v64_variantes.md de cada expediente",
              "efectos": ("ninguno en las conclusiones de la 4.13: en los tres expedientes la fase C da los grupos por no materiales para la acción; "
                          "inversion_fija_para_crecer_negativa forma el extremo superior del rango de Vidrala (variantes con N1, N2 o R0)"),
              "si_no_se_adopta": "se mantienen los avisos sin umbral", "sustituye_a": "D412-DOMINIOS"})
    # ---------------------------------------------------------------- 2. elecciones económicas por empresa
    D.append({"id": "VISCOFAN-ACCIONES", "grupo": "elección económica por empresa",
              "pregunta": ("Viscofan: ¿qué número de acciones divide el valor? El modelo usa 45,479209 millones, la media ponderada «diluida» publicada de 2025, que "
                           "contradice su propia definición (menor que la básica con el mismo numerador). La etapa 1 había usado 45,60 a 30-jun-2026 y descartado "
                           "la diluida por esa anomalía."),
              "recomendacion": ("Usar un número de acciones con derecho al valor en una fecha declarada, no un promedio de BPA: la circulación a 31-dic-2025 "
                                "(45,993399, la fecha de las cuentas) si se quiere coherencia con la base, o la de 30-jun-2026 (45,603643) si se prioriza la cercanía "
                                "al precio; más la dilución potencial del plan 2025–2027 si se decide contarla. No elegir por el valor: ninguna cambia la zona."),
              "alternativas": ["mantener la media «diluida» publicada (45,479209)", "media básica de 2025 (45,656226)",
                               "circulación a 31-dic-2025 (45,993399)", "circulación a 30-jun-2026 (45,603643)"],
              "evidencia": "fuentes/CONCILIACION_ACCIONES_VISCOFAN_4_13.md; resultados/alternativas_acciones_viscofan.md (libro vigente) y antecedentes_libro_4_12/",
              "efectos": (f"precio de Sí con E fijo: {e(psi(alt, 'activa_reproduccion_E_fijo'), 3)} € (activa), {e(psi(alt, 'media_basica_2025_E_fijo'), 3)} € (básica), "
                          f"{e(psi(alt, 'circulacion_31dic2025_E_fijo'), 3)} € (31-dic-2025), {e(psi(alt, 'circulacion_30jun2026_E_fijo'), 3)} € (30-jun-2026); "
                          f"todas «caro» con el precio de {e(pv.get('precio'))} €. Son sensibilidades de definición con fechas mezcladas, no valoraciones actualizadas"),
              "si_no_se_adopta": "el expediente sigue con 45,479209, descrito con su concepto real y su contradicción"})
    D.append({"id": "VISCOFAN-PERIMETRO", "grupo": "elección económica por empresa",
              "pregunta": ("Viscofan: ¿qué perímetro de la inversión usa P-M1? «NIIF 16» (capex + altas de derechos de uso frente a toda la D&A; el punto de cálculo "
                           "del expediente, plantilla V6.4.1 experimental) o «Caja» (capex de caja frente a toda la D&A; lo de la V6.4)."),
              "recomendacion": ("«NIIF 16», porque es el coherente con el motor B, que trata los arrendamientos como capital y como deuda: «Caja» compara un numerador "
                                "sin las altas de derechos de uso con una D&A que sí incluye su amortización. No adoptarlo hasta revisar la conciliación de los "
                                "arrendamientos 2021–2025 (altas 24,110; amortización de derechos de uso 27,051)."),
              "alternativas": ["«Caja» (como en la 4.12)", "solo activos propios (no coherente sin reexpresar NOPAT, capital y puente; no calculado como variante)"],
              "evidencia": ("resultados/conciliacion_arrendamientos_viscofan.md; resultados/compatibilidad_v641.md; viscofan/resultados/dominios_perimetro.md; "
                            "v6/v641_experimental/docs/README_V6.4.1_experimental.md"),
              "efectos": (f"precio de Sí de la activa (NIIF 16, θ = 0,5) {e(psi(vv, 'activa'), 3)} €; con «Caja» {e(psi(vv, 'perimetro_alternativo'), 3)} €; "
                          f"extremos de θ con «Caja» {e(psi(vv, 'perimetro_alternativo_parametro_minimo'), 3)} y {e(psi(vv, 'perimetro_alternativo_parametro_maximo'), 3)} €. "
                          f"Exceso observado 2021–2025: 64,923 (NIIF 16) frente a 40,813 («Caja»)"),
              "si_no_se_adopta": "el expediente sigue con NIIF 16 como punto de cálculo no adoptado y «Caja» como variante"})
    D.append({"id": "VISCOFAN-CONFIG", "grupo": "elección económica por empresa",
              "pregunta": ("Viscofan: ¿se adopta alguna de sus otras entradas propias? N1 22,12 % frente a C52 19,83 %; N2 vacío (regla heredada «Último año»); "
                           "R1 con un circulante del 48,28 % de las ventas; P-M1 SR1 · Θ con θ no observado (rango 0–1, punto de cálculo 0,5); cartera legado."),
              "recomendacion": ("Adoptar, si se quiere, solo N1 como dato derivado (causa publicada y cuantificada); θ y la estructura siguen siendo hipótesis sin "
                                "un desglose del capex entre mantenimiento y crecimiento."),
              "alternativas": ["N1 sin además los ajustes de ejercicios anteriores (22,66 %; la configuración usa 22,12 %)", "C52 heredado", "Λ en lugar de Θ (SRF solo definida hasta λ = 1,2011 con NIIF 16)"],
              "evidencia": "viscofan/Viscofan/configuracion_economica.json; viscofan/Viscofan/configuracion_v64_variantes.md; viscofan/Viscofan/fase_c.json",
              "efectos": (f"precio {e(pv.get('precio'))} € (cierre del 3-nov-2026); precio de Sí de la activa {e(pv.get('precio_si'))} € y de las variantes calculadas "
                          f"de {e(rv[0])} a {e(rv[1])} € ({rv[2]}); heredado {e(psi(vv, 'heredado'))} €. Estado: {ev['estado']} · {ev['accion'] or 'sin acción'} · {ev['tratamiento']}"),
              "si_no_se_adopta": "el expediente de Viscofan sigue siendo un ensayo con configuración no adoptada", "sustituye_a": "VISCOFAN-CONFIG (4.12)"})
    D.append({"id": "VIDRALA-CONFIG", "grupo": "elección económica por empresa",
              "pregunta": ("Vidrala: ¿qué configuración económica se adopta, si alguna? Siguen pendientes N1, N2, N3, la estructura de P-M1 (SR1, SR2, SRF, H, S o sin "
                           "requisito), λ, las convenciones y la cartera P0. La 4.13 corrigió las inferencias que apoyaban SR1 (Q-ROIC1, ROIC frente a r_op y la "
                           "inferencia contra H)."),
              "recomendacion": ("Ninguna adopción como valoración. Para la estructura: decidir primero qué ROIC mide el largo plazo (Q-ROIC1: neto de reposición → SR1; "
                                "sobre una inversión total que incluye la reposición → SR2) y la mezcla futura de fijo y circulante (SR1 frente a SRF). Las fases C "
                                "nuevas no nombran una estructura más coherente; descartan S, que carga otra vez el exceso que ya lleva el S2C histórico."),
              "alternativas": ["modo heredado (V6.3 efectiva)", "configuración de demostración, declarada como no adoptada", "otra combinación de las variantes calculadas"],
              "evidencia": ("CORRECCIONES_ECONOMICAS_VIDRALA_4_13.md; resultados/crecimiento_terminal_vidrala.md; vidrala_condicionado/Vidrala/fase_c.json "
                            "(configuracion_v64.mantenimiento); …_4_9/PRECISION_ROIC_4_9.md"),
              "efectos": (f"precio {e(pc.get('precio'))} €; precio de Sí de la activa {e(pc.get('precio_si'))} € y de las variantes calculadas de {e(rc[0])} a {e(rc[1])} € "
                          f"({rc[2]}); heredado {e(psi(vc, 'heredado'))} €; H {e(psi(vc, 'estructura_H'))}, SR2 {e(psi(vc, 'estructura_SR2'))}, SRF {e(psi(vc, 'estructura_SRF'))}, "
                          f"S {e(psi(vc, 'estructura_S'))} €. El crecimiento perpetuo con ROIC del 9 % y r_op 8,689 % aporta +1,57 € en la activa: no es neutral"),
              "si_no_se_adopta": "los expedientes de Vidrala siguen siendo ensayos con configuración no adoptada", "sustituye_a": "VIDRALA-CONFIG (4.12)"})
    D.append({"id": "VIDRALA-PERIMETRO", "grupo": "elección económica por empresa",
              "pregunta": ("Vidrala: ¿se concilia su perímetro de la inversión como el de Viscofan (altas de derechos de uso frente a su amortización) y se corrige el "
                           "perímetro del S2C histórico (entra Brasil y sale Italia)? Los expedientes usan la V6.4 sin perímetro declarado («Caja»)."),
              "recomendacion": ("Sí como trabajo técnico de la próxima entrega, sin adoptar nada: extraer las altas de derechos de uso de Vidrala 2021–2025 y "
                                "calcular las dos variantes, como se hizo con Viscofan. El efecto del S2C del mismo perímetro lo estima la fase C de vidrala_bloqueo "
                                "(≈ −0,55 € de precio de Sí) y el del margen (≈ +0,8 €); no se ha calculado en el libro."),
              "alternativas": ["dejar «Caja» en Vidrala (los arrendamientos pesan poco en su balance, sin cuantificar)", "corregir solo el S2C del mismo perímetro"],
              "evidencia": "vidrala_bloqueo/Vidrala/fase_c.json (estimación del S2C del mismo perímetro y del margen); vidrala_condicionado/Vidrala/fase_c.json (Palancas!C15, sin cifra)",
              "efectos": "no calculados: falta la extracción de las altas de derechos de uso de Vidrala",
              "si_no_se_adopta": "Vidrala sigue con el perímetro «Caja» implícito de la V6.4"})
    # ---------------------------------------------------------------- 3. ampliaciones futuras
    D.append({"id": "D413-MOTOR-A", "grupo": "ampliación futura",
              "pregunta": "¿Qué se exige antes de ampliar el sistema al motor A?",
              "recomendacion": ("Antes del motor A: decidir D413-FUNDAMENTO (criterio de materialidad) y las elecciones de acciones y de perímetro de Viscofan; "
                                "una tercera empresa de motor B con arrendamientos relevantes, preparada de cero con la V6.4.1; y una revisión externa de la 4.13. "
                                "El motor A no comparte P-M1 ni el perímetro: necesitará su propia capa experimental, plantilla, referencia y réplica."),
              "alternativas": ["empezar el motor A ya, con el motor B como está", "ampliar primero el motor B a más empresas y dejar el motor A para después"],
              "evidencia": "INFORME_INTEGRACION_4_13.md §10 y §11",
              "efectos": "ninguno en los expedientes", "si_no_se_adopta": "el sistema sigue limitado al motor B"})
    D.append({"id": "D413-V641", "grupo": "ampliación futura",
              "pregunta": "¿La plantilla V6.4.1 experimental (perímetro de la inversión) sustituye a la V6.4 en los expedientes nuevos de motor B?",
              "recomendacion": ("Sí para expedientes nuevos, como experimental: con el perímetro vacío o «Caja» da exactamente la V6.4 (0 celdas distintas), y obliga a "
                                "declarar el perímetro cuando hay requisito. Los expedientes V6.4 existentes no se reabren."),
              "alternativas": ["mantener las dos y elegir por expediente (como ahora)", "seguir solo con la V6.4"],
              "evidencia": "resultados/compatibilidad_v641.md; pruebas del grupo H; v6/v641_experimental/",
              "efectos": "ninguno en los expedientes existentes", "si_no_se_adopta": "se elige plantilla por expediente con la selección explícita"})
    D.append({"id": "D411-TERMINAL-R1", "grupo": "ampliación futura",
              "pregunta": ("¿Se mantiene el terminal prudente de R1 (carga la inversión para crecer al ritmo g aunque en el MALO las ventas sigan por debajo del máximo "
                           "conservado) o se especifica uno que reconozca la capacidad sobrante?"),
              "recomendacion": "Mantenerlo hasta tener una especificación con su réplica.",
              "alternativas": ["terminal que no invierta hasta recuperar el máximo (sin especificar)"],
              "evidencia": "…_4_12/REVISION_ECONOMICA_VIDRALA_4_12.md §4; README de la V6.4 §8 (1); grupo terminal_r1_sin_maximo_conservado de las variantes de Vidrala",
              "efectos": "solo en el escenario MALO (en Vidrala, del orden de 1 € del precio de Sí según su fase C)", "si_no_se_adopta": "sigue el terminal prudente"})
    D.append({"id": "D412-V63", "grupo": "ampliación futura",
              "pregunta": "¿Se extienden a los expedientes V6.3 la cadena de trazabilidad del paso 12 y el protocolo del objetivo?",
              "recomendacion": "La cadena de trazabilidad sí (es de solo lectura); el protocolo del objetivo no, mientras no se decida D413-PROTOCOLO.",
              "alternativas": ["las dos", "ninguna"], "evidencia": "Anexo D §D.13; personaje_v2/scripts/trazabilidad_v64.py",
              "efectos": "ninguno sobre los expedientes históricos (no se reabren)", "si_no_se_adopta": "los expedientes V6.3 siguen como en la 4.11"})
    for d in D:
        d.update({"decision": None, "fecha": None, "decidido_por": None})
    out = {"tipo": "propuesta_humana", "entrega": "4.13",
           "aviso": "Propuesta sin firmar. Ningún campo humano está relleno y nada de lo que aquí se recomienda está adoptado.",
           "estado_de_los_expedientes": {"Vidrala · objetivo_condicionado": ec, "Vidrala · bloqueo_del_objetivo": eb, "Viscofan (V6.4.1, NIIF 16)": ev},
           "no_se_vuelve_a_pedir": ["el uso experimental supervisado (autorizado)", "reparaciones técnicas, contrastes, reproducciones y regeneraciones de lo afectado"],
           "informacion_que_falta": ["desglose del capex de Vidrala y Viscofan entre mantenimiento, reconstrucción y crecimiento (condiciona P-M1 en los dos)",
                                     "número de acciones de Viscofan al 3-nov-2026 (no hay cifra oficial)",
                                     "altas de derechos de uso de Vidrala 2021–2025 (VIDRALA-PERIMETRO)",
                                     "bytes de los PDF de BORME y CNMV consultados para las acciones de Viscofan, y del PDF del Bundesbank de rf de Vidrala (no conservados)"],
           "decisiones": D}
    os.makedirs(OUT, exist_ok=True)
    json.dump(out, open(os.path.join(OUT, "propuesta_humana_4_13.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    md = ["# Propuesta humana de la entrega 4.13 (sin firmar)", "", out["aviso"], "",
          "**Estado de los expedientes que la sostienen.** " + " · ".join(f"{k}: {v['estado']}, {v['accion'] or 'sin acción'}, {v['tratamiento'] or '—'}, auditoría {v['auditoria'] or '—'}"
                                                                       for k, v in out["estado_de_los_expedientes"].items()), "",
          "**No se vuelve a pedir como aprobación:** " + "; ".join(out["no_se_vuelve_a_pedir"]) + ".", "",
          "**Información que falta (no son decisiones):** " + "; ".join(out["informacion_que_falta"]) + ".", ""]
    for grupo, titulo in GRUPOS:
        md += [f"## {titulo}", ""]
        for d in [x for x in D if x["grupo"] == grupo]:
            md += [f"### {d['id']}", "", f"**Pregunta.** {d['pregunta']}", "", f"**Recomendación (argumentada, no adoptada).** {d['recomendacion']}", "",
                   f"**Alternativas.** {'; '.join(d['alternativas'])}.", "", f"**Evidencia.** {d['evidencia']}.", "", f"**Efectos calculados.** {cap(d['efectos'])}.", "",
                   f"**Si no se adopta.** {cap(d['si_no_se_adopta'])}." + (f" Sustituye a: {d['sustituye_a']}." if d.get("sustituye_a") else ""), "",
                   "Decisión: — · Fecha: — · Decidido por: —", ""]
    open(os.path.join(OUT, "PROPUESTA_HUMANA_4_13.md"), "w", encoding="utf-8").write("\n".join(md))
    print(f"OK: {len(D)} decisiones (" + ", ".join(f"{sum(1 for d in D if d['grupo'] == g)} de {g}" for g, _ in GRUPOS) + ") → propuestas/PROPUESTA_HUMANA_4_13.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
