#!/usr/bin/env python3
"""Escribe la propuesta humana única y breve de la 4.12 (encargo §9, entregable 4): propuestas/PROPUESTA_HUMANA_4_12.md y .json.

Separa las decisiones necesarias para USAR el sistema de las ELECCIONES ECONÓMICAS de cada empresa. No vuelve a pedir como aprobación
tareas técnicas ya autorizadas (incorporar una fuente comprobada, contrastar, reproducir, corregir defectos). Las cifras de efecto se
leen de las salidas calculadas (fichas, variantes y comparaciones de los expedientes de la 4.12), no se copian a mano. Ningún campo
humano se rellena (decision, fecha y decidido_por = null).
Uso (desde munger_v2_r1/): python3 -I …/2026-11_Vidrala_ensayo_4_12/scripts/propuesta_humana_4_12.py
"""
import json
import os

AQUI = os.path.dirname(os.path.abspath(__file__))
ENS = os.path.dirname(AQUI)
OUT = os.path.join(ENS, "propuestas")
COND = os.path.join(ENS, "cierre_condicionado", "Vidrala")
BLOQ = os.path.join(ENS, "cierre_bloqueo", "Vidrala")
VIS = os.path.join(ENS, "viscofan", "experimental", "Viscofan")


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
            "precio_objetivo_emitido": ob.get("precio_objetivo_emitido")}


def cap(t):
    return t[:1].upper() + t[1:] if t else t


def variante(c, clave):
    v = j(os.path.join(c, "configuracion_v64_variantes.json"))
    return next((x for x in v.get("variantes") or [] if x.get("clave") == clave), {})


def main():
    ec, eb, ev = estado(COND), estado(BLOQ), estado(VIS)
    pc = j(os.path.join(COND, "precio.json"))
    vc = j(os.path.join(COND, "configuracion_v64_variantes.json"))
    psis = [x.get("precio_si") for x in vc.get("variantes") or [] if isinstance(x.get("precio_si"), (int, float))]
    pv = j(os.path.join(VIS, "precio.json"))
    vv = j(os.path.join(VIS, "configuracion_v64_variantes.json"))
    psis_v = [x.get("precio_si") for x in vv.get("variantes") or [] if isinstance(x.get("precio_si"), (int, float))]
    D = []
    D.append({"id": "D412-USO", "grupo": "uso del sistema",
              "pregunta": "¿Qué uso permite esta entrega: análisis experimental supervisado de empresas de motor B, sin apoyo a decisiones con dinero real?",
              "recomendacion": ("Sí a un uso SUPERVISADO y EXPERIMENTAL: expedientes de empresas cuyo motor por los hechos es el B, con la V6.4 en modo experimental "
                                "como ensayo y el modo heredado (V6.3 efectiva) como control, con la persona responsable revisando cada relevo (guía "
                                "personaje_v2/GUIA_RECORRIDO_SUPERVISADO.md) y los resultados leídos como valores calculados condicionales. No a decisiones con dinero "
                                "real mientras sigan abiertas las condiciones del informe (apartado 9): convenciones sin adoptar, hipótesis no observadas, una sola "
                                "configuración por empresa y dos empresas."),
              "alternativas": ["usar solo la V6.3 y dejar la V6.4 para pruebas técnicas", "apoyar decisiones con dinero real ya (no recomendado: ver apartado 9 del informe)"],
              "evidencia": "INFORME_INTEGRACION_4_12.md §9 (aptitud de uso y tabla de limitaciones); REGISTRO_PRUEBAS_4_12.md",
              "efectos": "ninguno en los expedientes: es el alcance del uso", "si_no_se_adopta": "la entrega queda como implementación verificada sin uso declarado",
              "sustituye_a": "D411-PLANTILLA"})
    D.append({"id": "D412-PROTOCOLO", "grupo": "uso del sistema",
              "pregunta": ("Cuando hipótesis experimentales sin fundamento suficiente condicionan el precio objetivo (con «esperar» por precio), ¿qué protocolo rige: "
                           "«objetivo_condicionado» (concluido · esperar, con el precio de Sí como valor calculado condicional y provisional) o «bloqueo_del_objetivo» "
                           "(pendiente_de_datos, sin acción ni objetivo)?"),
              "recomendacion": ("Para el uso supervisado, «objetivo_condicionado», porque conserva la información que sí está sostenida (la acción, cuando ninguna "
                                "variante calculada la cambia) y marca el objetivo como condicional con sus hipótesis. Para cualquier uso con dinero real, ninguno de "
                                "los dos basta por sí solo: haría falta fundamentar las hipótesis que condicionan el objetivo."),
              "alternativas": ["«bloqueo_del_objetivo» en todos los casos (más prudente; trata una hipótesis sin fundamento como un dato ausente)",
                               "«objetivo_condicionado» solo si el rango calculado del precio de Sí está por debajo del precio en todo el ámbito"],
              "evidencia": "COMPARACION_PROTOCOLOS_4_12.md; cierre_condicionado/ y cierre_bloqueo/ (mismo material económico, protocolos distintos)",
              "efectos": (f"Vidrala, mismo material: con «objetivo_condicionado» {ec['estado']} · {ec['accion']} · {ec['tratamiento']} (valor calculado condicional "
                          f"{e(ec['valor_calculado_condicional'])} €); con «bloqueo_del_objetivo» {eb['estado']} · {eb['accion'] or 'sin acción'} · {eb['tratamiento']} "
                          f"(el mismo valor calculado condicional, no emitido)"),
              "si_no_se_adopta": "cada expediente experimental tiene que declarar su protocolo; sin él no se emite ningún objetivo oficial (objetivo_sin_protocolo)",
              "sustituye_a": "D411-MATERIALIDAD"})
    D.append({"id": "D412-FUNDAMENTO", "grupo": "uso del sistema",
              "pregunta": ("Las banderas por parámetro de la fase C (material para el objetivo, fundamento suficiente) deciden qué hipótesis condicionan el objetivo y, con "
                           "«comprar», qué entra en D10, y ninguna regla las contrasta. ¿Se exige que, con «comprar», todo parámetro activo que la propia configuración "
                           "clasifica como «hipótesis» cuente como sin fundamento suficiente (y vaya a D10 y a la comprobación conjunta)?"),
              "recomendacion": ("Sí, para «comprar»: es una regla conservadora que impide que un juicio sin contraste deje una hipótesis no observada fuera de D10. Con "
                                "«esperar» no cambia nada en los expedientes de la 4.12. Para el objetivo, mantener el juicio de la fase C y revisar en la auditoría "
                                "que cada «fundamento suficiente» de un parámetro de clase «hipótesis» tenga evidencia con página."),
              "alternativas": ["dejarlo al juicio de la fase C (como ahora)", "aplicar la regla conservadora también al objetivo (cambiaría las hipótesis que lo condicionan)"],
              "evidencia": "revision_interna/REVISION_INTERNA_4_12.md (R5); INFORME_INTEGRACION_4_12.md §9.6 (L15); Anexo D §D.13",
              "efectos": ("ninguno en los expedientes de la 4.12 (ninguno concluye «comprar»). Diferencias de juicio observadas: la regla R1 sale con fundamento suficiente en "
                          "Vidrala y sin él en Viscofan, y la familia de P-M1 de Viscofan es «hipótesis» en la configuración y está fundamentada para la fase C"),
              "si_no_se_adopta": "una compra podría dejar fuera de D10 un parámetro no observado que la fase C dé por fundado"})
    D.append({"id": "D412-DOMINIOS", "grupo": "uso del sistema",
              "pregunta": "¿Los avisos de dominio (factor f, inversión fija para crecer negativa, terminal de R1 sin máximo conservado, S2C inerte) siguen como avisos sin umbral o se fijan umbrales que impidan una conclusión favorable?",
              "recomendacion": ("Siguen como avisos con sus valores, sin umbral, mientras solo haya dos empresas: con las bases de Viscofan la estructura SRF deja de "
                                "estar definida con λ por encima de 1,1413 y con las de Vidrala por encima de 1,50, así que un umbral fijo no sería comparable entre "
                                "empresas. Un aviso material ya condiciona el objetivo (limite:<id>) y no admite «comprar»."),
              "alternativas": ["umbral fijo para f (por ejemplo, 1,25) que bloquee «comprar»", "umbral por empresa fijado en su configuración"],
              "evidencia": "personaje_v2/scripts/dominios_v64.py; README de la V6.4 §8 (9) y §9 (13–15); viscofan/configuracion/analisis_configuracion_viscofan.md",
              "efectos": ("ninguno en los expedientes de la 4.12: en Vidrala, los avisos activos (terminal de R1 sin máximo conservado y S2C inerte en el MALO) y la lectura del factor f "
                          "no son materiales para la conclusión según su fase C; en Viscofan no hay ningún aviso activo y la fase C da el factor f por no material"),
              "si_no_se_adopta": "se mantienen los avisos sin umbral", "sustituye_a": "D411-DOMINIOS"})
    D.append({"id": "D411-TERMINAL-R1", "grupo": "uso del sistema",
              "pregunta": "¿Se mantiene el terminal prudente de R1 (carga la inversión para crecer al ritmo g aunque en el MALO las ventas sigan por debajo del máximo conservado) o se especifica uno que reconozca la capacidad sobrante?",
              "recomendacion": ("Mantenerlo hasta tener una especificación con su réplica: en Vidrala el efecto máximo es de unos 2,5 € del valor MALO (0,5 € del ponderado) y no cambia la zona; "
                                "en Viscofan no aplica, porque las ventas superan siempre el máximo conservado."),
              "alternativas": ["terminal que no invierta hasta recuperar el máximo (sin especificar)"],
              "evidencia": "REVISION_ECONOMICA_VIDRALA_4_12.md §4; README de la V6.4 §8 (1)", "efectos": "solo en el escenario MALO", "si_no_se_adopta": "sigue el terminal prudente"})
    D.append({"id": "D412-V63", "grupo": "uso del sistema",
              "pregunta": "¿Se extienden a los expedientes V6.3 la cadena de trazabilidad del paso 12 y el protocolo del objetivo?",
              "recomendacion": "La cadena de trazabilidad sí (es de solo lectura y ya se puede ejecutar a mano sobre un expediente V6.3); el protocolo del objetivo no, mientras no se decida D412-PROTOCOLO (en la V6.3 rige el Anexo B §B.6.7).",
              "alternativas": ["las dos", "ninguna"], "evidencia": "Anexo D §D.13; personaje_v2/scripts/trazabilidad_v64.py",
              "efectos": "ninguno sobre los expedientes históricos (no se reabren)", "si_no_se_adopta": "los expedientes V6.3 siguen como en la 4.11"})
    D.append({"id": "VIDRALA-CONFIG", "grupo": "elección económica",
              "pregunta": ("Vidrala: ¿qué configuración económica se adopta, si alguna? Sigue pendiente de la 4.11: N1 (T1 22,05 % o C52), N2 (M1 18,55 % o C8), "
                           "N3 (R1 o R0), la estructura de P-M1 (SR1, SR2, SRF, H, S o sin requisito), λ (punto o rango 1,10–1,25), las convenciones y la cartera P0, "
                           "además de P3 (C49) y C46/C47."),
              "recomendacion": ("Ninguna adopción todavía como valoración: la acción («esperar» por precio) no cambia en ninguna de las variantes calculadas, pero el nivel "
                                "del precio de Sí sí depende de ellas. Si se quiere un punto de partida para el uso supervisado, la configuración de demostración, "
                                "declarada como no adoptada."),
              "alternativas": ["modo heredado (V6.3 efectiva)", "configuración de demostración", "otra combinación de las variantes calculadas"],
              "evidencia": "cierre_condicionado/resultados/comparacion_homogenea.md; REVISION_ECONOMICA_VIDRALA_4_12.md; propuesta 4.11 (D411-N1 … D411-C46C47)",
              "efectos": (f"precio {e(pc.get('precio'))} € (cierre del 31-dic-2025); precio de Sí de la activa {e(pc.get('precio_si'))} € y de las variantes calculadas de {e(min(psis) if psis else None)} a "
                          f"{e(max(psis) if psis else None)} €; heredado {e(variante(COND, 'heredado').get('precio_si'))} €"),
              "si_no_se_adopta": "los expedientes de Vidrala siguen siendo ensayos con configuración no adoptada", "sustituye_a": "D411-N1, D411-N2, D411-N3, D411-PM1-ESTRUCTURA, D411-PM1-PARAMETRO, D411-PM1-CARTERA, D411-P3, D411-C46C47"})
    D.append({"id": "VISCOFAN-CONFIG", "grupo": "elección económica",
              "pregunta": ("Viscofan: ¿se adopta alguna de sus entradas propias? N1 22,12 % (sin las activaciones de bases imponibles negativas) frente a C52 19,83 %; "
                           "N2 vacío (regla heredada «Último año», 16,36 %); R1 con un circulante del 48,28 % de las ventas; P-M1 SR1 · Θ con θ no observado (rango 0–1, "
                           "punto de cálculo 0,5); cartera legado."),
              "recomendacion": ("Adoptar, si se quiere, solo N1 como dato derivado (la causa del 10,1 % de 2025 está publicada y cuantificada); θ y la estructura siguen "
                                "siendo hipótesis: no adoptarlas sin un desglose del capex entre mantenimiento y crecimiento."),
              "alternativas": ["N1 con además los ajustes de ejercicios anteriores (22,66 %)", "C52 heredado", "Λ en lugar de Θ (SRF solo definida hasta λ = 1,1413)"],
              "evidencia": "viscofan/configuracion/analisis_configuracion_viscofan.md; viscofan/experimental/Viscofan/configuracion_v64_variantes.md",
              "efectos": (f"precio {e(pv.get('precio'))} € (cierre del 3-nov-2026); precio de Sí de la activa {e(pv.get('precio_si'))} € y de las variantes calculadas de {e(min(psis_v) if psis_v else None)} a "
                          f"{e(max(psis_v) if psis_v else None)} €; heredado {e(variante(VIS, 'heredado').get('precio_si'))} €"),
              "si_no_se_adopta": "el expediente de Viscofan sigue siendo un ensayo con configuración no adoptada"})
    for d in D:
        d.update({"decision": None, "fecha": None, "decidido_por": None})
    out = {"tipo": "propuesta_humana", "entrega": "4.12",
           "aviso": "Propuesta única y breve, sin firmar. Ningún campo humano está relleno y nada de lo que aquí se recomienda está adoptado.",
           "estado_de_los_expedientes": {"Vidrala · objetivo_condicionado": ec, "Vidrala · bloqueo_del_objetivo": eb, "Viscofan": ev},
           "no_se_vuelve_a_pedir": ["incorporar el PDF del Bundesbank cuando se disponga de sus bytes (trabajo técnico autorizado)", "contrastes, reproducciones y correcciones técnicas"],
           "informacion_que_falta": ["bytes del PDF del Bundesbank (rendbund-data.pdf) para conservar la fuente de rf de Vidrala con su huella",
                                     "las ediciones exactas de Viscofan de 2016, 2018 y 2021–2023 que cita la fase 1 (sus cifras se contrastaron en otras ediciones)",
                                     "desglose del capex de Vidrala y Viscofan entre mantenimiento, reconstrucción y crecimiento"],
           "decisiones": D}
    os.makedirs(OUT, exist_ok=True)
    json.dump(out, open(os.path.join(OUT, "propuesta_humana_4_12.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    md = ["# Propuesta humana única de la entrega 4.12 (breve, sin firmar)", "", out["aviso"], "",
          "**Estado de los expedientes que la sostienen.** " + " · ".join(f"{k}: {v['estado']}, {v['accion'] or 'sin acción'}, {v['tratamiento'] or '—'}, auditoría {v['auditoria'] or '—'}"
                                                                       for k, v in out["estado_de_los_expedientes"].items()), "",
          "**No se vuelve a pedir como aprobación:** " + "; ".join(out["no_se_vuelve_a_pedir"]) + ".", "",
          "**Información que falta (no son decisiones):** " + "; ".join(out["informacion_que_falta"]) + ".", ""]
    for grupo, titulo in (("uso del sistema", "Decisiones necesarias para usar el sistema"), ("elección económica", "Elecciones económicas de cada empresa")):
        md += [f"## {titulo}", ""]
        for d in [x for x in D if x["grupo"] == grupo]:
            md += [f"### {d['id']}", "", f"**Pregunta.** {d['pregunta']}", "", f"**Recomendación (argumentada, no adoptada).** {d['recomendacion']}", "",
                   f"**Alternativas.** {'; '.join(d['alternativas'])}.", "", f"**Evidencia.** {d['evidencia']}.", "", f"**Efectos calculados.** {cap(d['efectos'])}.", "",
                   f"**Si no se adopta.** {cap(d['si_no_se_adopta'])}." + (f" Sustituye a: {d['sustituye_a']}." if d.get("sustituye_a") else ""), "",
                   "Decisión: — · Fecha: — · Decidido por: —", ""]
    open(os.path.join(OUT, "PROPUESTA_HUMANA_4_12.md"), "w", encoding="utf-8").write("\n".join(md))
    print(f"OK: {len(D)} decisiones ({sum(1 for d in D if d['grupo'] == 'uso del sistema')} de uso y {sum(1 for d in D if d['grupo'] == 'elección económica')} económicas) → propuestas/PROPUESTA_HUMANA_4_12.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
