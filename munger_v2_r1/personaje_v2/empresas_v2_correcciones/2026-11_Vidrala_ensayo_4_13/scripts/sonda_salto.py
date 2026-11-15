"""Sonda 4.13 §4: contraejemplo externo del salto del protocolo, en copias de los expedientes reales de la 4.12."""
import copy, json, os, shutil, sys
PV = sys.argv[1]; OUT = sys.argv[2]
sys.path.insert(0, os.path.join(PV, "scripts"))
import config_v2, pipeline as P, objetivo_v64 as OBJ
E = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_12")
cfg = config_v2.cargar(os.path.join(PV, "config_v2_v64_experimental.json"))
def copia(rel, nombre):
    d = os.path.join(OUT, nombre); shutil.rmtree(d, ignore_errors=True)
    shutil.copytree(os.path.join(E, rel), d, ignore=shutil.ignore_patterns("variantes_v64", "historial_cierres", ".lo_perfil", "prompts_generados"))
    # las variantes recalculadas no hacen falta para la coherencia; configuracion_v64_variantes.json sí está
    return d
def coh(d, fc):
    p = P.Pipeline(d, cfg, None)
    return p.coherencia_v64(fc), p.coherencia_fase_c(fc) if hasattr(p, "coherencia_fase_c") else None
def actualizar_bloque(d, fc):
    ev = OBJ.evaluar(d, fc)
    ob = fc["configuracion_v64"]["objetivo"]
    ob.update(protocolo=ev["protocolo"], hipotesis_que_condicionan=ev["hipotesis_que_condicionan"], ambito=ev["ambito"],
              accion_sostenida_en_ambito=ev["accion_sostenida_en_ambito"], tratamiento=ev["tratamiento"], origen_del_bloqueo=ev["origen_del_bloqueo"])
    return ev
for nombre, rel, prot, concl in (("cond_real", "cierre_condicionado/Vidrala", "igual", None), ("bloq_real", "cierre_bloqueo/Vidrala", "igual", None),
                                  ("visc_real", "viscofan/experimental/Viscofan", "igual", None),
                                  ("cond_sin_protocolo_descartar", "cierre_condicionado/Vidrala", None, "descartar"),
                                  ("cond_sin_protocolo_comprar", "cierre_condicionado/Vidrala", None, "comprar"),
                                  ("cond_bloqueo_descartar", "cierre_condicionado/Vidrala", "bloqueo_del_objetivo", "descartar"),
                                  ("cond_bloqueo_comprar", "cierre_condicionado/Vidrala", "bloqueo_del_objetivo", "comprar")):
    d = copia(rel, nombre)
    fc = json.load(open(os.path.join(d, "fase_c.json"), encoding="utf-8"))
    if prot != "igual":
        conf = json.load(open(os.path.join(d, "configuracion_economica.json"), encoding="utf-8"))
        if prot is None: conf.pop("protocolo_objetivo", None)
        else: conf["protocolo_objetivo"] = prot
        json.dump(conf, open(os.path.join(d, "configuracion_economica.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    if concl:
        fc["conclusion_provisional"] = concl
        actualizar_bloque(d, fc)
    dec = fc.get("decision") or {}
    r = coh(d, fc)
    ev = OBJ.evaluar(d, fc)
    print(f"{nombre:30s} final {fc.get('estado_analisis')}/{dec.get('accion')}/{dec.get('precio_objetivo')} · tratamiento {ev['tratamiento']} · coherencia_v64: {(r[0] or 'ACEPTA')[:170]}")
