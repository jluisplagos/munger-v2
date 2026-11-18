#!/usr/bin/env python3
"""Selección explícita de plantilla, referencia y configuración económica de un expediente (encargo 4.11 §3 y §6).

Regla: cada ejecución elige la plantilla con `--config` (config_v2.json = V6.3; config_v2_v64_experimental.json = V6.4
experimental; 4.13: config_v2_v641_experimental.json = V6.4.1 experimental, con el perímetro de la inversión). La V6.4 nunca se activa por defecto ni para expedientes antiguos.
  - Con la V6.4, el expediente tiene que traer `configuracion_economica.json` válida (configuracion_economica.validar). La
    primera ejecución escribe `plantilla_activa.json`: versión y SHA-256 de la plantilla, la referencia y el verificador, la
    configuración usada y la huella de la configuración económica. Va en el material auditado (cierre_v2.MATERIAL_FIJO).
  - Un expediente que ya tiene `plantilla_activa.json` solo se ejecuta con la MISMA plantilla, referencia y verificador. Con otra
    selección (por ejemplo, el config V6.3 sobre un expediente V6.4, o una V6.4 reconstruida con otras huellas), el pipeline se
    detiene con código 2 SIN escribir nada: para cambiar de plantilla se prepara un expediente nuevo.
  - Con la V6.3 y sin `plantilla_activa.json`, nada cambia respecto de la 4.10.1. Una configuración económica en un expediente
    V6.3 se rechaza (no se ignora en silencio).
Uso como módulo desde pipeline.py; desde la consola: seleccion_plantilla.py CARPETA [--config config.json] (comprueba sin escribir).
"""
import hashlib
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import configuracion_economica as CE  # noqa: E402
import estructura_json as ESTR  # noqa: E402

V64 = "V6.4 experimental"
# (4.13 §7) familia de plantillas con «Configuración V6.4»: la V6.4.1 añade el perímetro de la inversión (B146:B155) y cambia dos
# fórmulas (B55 y B58). Es una plantilla y una referencia nuevas, experimentales, que se seleccionan con su propio config
# (config_v2_v641_experimental.json); los expedientes V6.4 siguen con la V6.4 (plantilla_activa.json fija sus huellas)
V641 = "V6.4.1 experimental"
FAMILIA_V64 = (V64, V641)
# (4.15, F1-IMPL) V6.3.1 F1: la V6.3 del motor A con el perímetro F1 de la reinversión (Historia C85:L89). Familia V6.3 (sin configuración
# económica), pero con su propia referencia y selección registrada (plantilla_activa.json), como la V6.4.1; se elige con
# config_v2_v631_f1.json. Un expediente V6.3 no se ejecuta con ella ni uno V6.3.1 con la V6.3.
V631 = "V6.3.1 F1"
ARCHIVO = "plantilla_activa.json"
CONF = "configuracion_economica.json"


def _sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def version(cfg):
    return (cfg.get("plantilla") or {}).get("version") or "V6.3"


def es_v64(cfg):
    """True para toda plantilla con «Configuración V6.4» (V6.4 y V6.4.1 experimentales)."""
    return version(cfg) in FAMILIA_V64


def es_v641(cfg):
    return version(cfg) == V641


def es_v631(cfg):
    return version(cfg) == V631


def registra(cfg):
    """Plantillas que fijan su selección en plantilla_activa.json (todas salvo la V6.3)."""
    return es_v64(cfg) or es_v631(cfg)


def compatibilidad_perimetro(conf, cfg):
    """(4.13 §7) Motivo si la configuración económica y la plantilla no casan en el perímetro de la inversión; None si casan.
    - Con la V6.4 no existe el perímetro: declararlo se rechaza (no se ignora en silencio).
    - Con la V6.4.1 y requisito adicional, el perímetro se declara de forma explícita («Caja» o «NIIF 16»): ninguno es central por
      defecto y la fila 142 de la trazabilidad del libro está activa."""
    if not isinstance(conf, dict) or conf.get("modo") != "Experimental":
        return None
    pm = conf.get("PM1") if isinstance(conf.get("PM1"), dict) else {}
    if CE.declara_perimetro(conf) and not es_v641(cfg):
        return (f"la configuración económica declara PM1.perimetro_inversion, que solo existe en la plantilla {V641}; esta ejecución "
                f"selecciona {version(cfg)}: o se quita, o se prepara un expediente nuevo con config_v2_v641_experimental.json")
    if es_v641(cfg) and pm.get("estructura") in CE.ESTRUCTURAS[1:] and not CE.declara_perimetro(conf):
        return (f"con la plantilla {V641} y requisito adicional, PM1.perimetro_inversion es obligatorio ({' | '.join(CE.PERIMETROS)}) "
                f"con su trazabilidad (PM1.perimetro): ninguno se aplica por defecto")
    return None


def seleccion(cfg):
    pl = cfg["plantilla"]
    out = {"version": version(cfg), "config": os.path.basename(cfg.get("_ruta_config") or ""), "version_config": cfg.get("version_config")}
    for k in ("archivo", "referencia", "verificador"):
        p = pl.get(k)
        out[k] = os.path.basename(p) if p else None
        out[k + "_sha256"] = _sha(p) if p and os.path.isfile(p) else None
    return out


def comprobar(carpeta, cfg):
    """None si la ejecución puede seguir; si no, el motivo (el pipeline termina con código 2 sin escribir nada)."""
    sel = seleccion(cfg)
    faltan = [k for k in ("archivo", "referencia", "verificador") if not sel[k + "_sha256"]]
    if faltan:
        return f"la configuración {sel['config']} apunta a archivos que no existen: {', '.join('plantilla.' + k for k in faltan)}"
    pa = os.path.join(carpeta, ARCHIVO)
    if os.path.exists(pa):
        try:
            reg = json.load(open(pa, encoding="utf-8"))
        except (OSError, ValueError) as e:
            return f"{ARCHIVO} no se puede leer ({str(e)[:80]}): la selección de plantilla del expediente no se puede acreditar"
        fe = ESTR.comprobar(reg, ESTR.PLANO_PLANTILLA_ACTIVA)  # (4.13 §3) antes de cualquier .get
        if fe:
            return f"{ARCHIVO}: estructura incorrecta ({'; '.join(fe)[:200]}): la selección de plantilla del expediente no se puede acreditar"
        dif = [k for k in ("version", "archivo_sha256", "referencia_sha256", "verificador_sha256") if reg.get(k) != sel.get(k)]
        if dif:
            return (f"el expediente se preparó con {reg.get('version')} ({ARCHIVO}: {', '.join(f'{k} {str(reg.get(k))[:12]}' for k in dif)}) y esta ejecución "
                    f"selecciona {sel['version']} ({sel['config']}): un expediente solo se ejecuta con su plantilla; para cambiarla, prepara un expediente nuevo")
    elif not registra(cfg):
        if os.path.exists(os.path.join(carpeta, CONF)):
            return f"el expediente trae {CONF} pero la configuración {sel['config']} selecciona la V6.3: la configuración económica exige la plantilla {V64} o la {V641} (no se ignora)"
        return None
    else:
        if es_v631(cfg) and os.path.exists(os.path.join(carpeta, CONF)):
            return f"el expediente trae {CONF} pero la configuración {sel['config']} selecciona la {V631}: la configuración económica exige la plantilla {V64} o la {V641} (no se ignora)"
        # (4.11, revisión interna H1) con la V6.4 y SIN plantilla_activa.json: si la carpeta ya tiene libros V6.3 o pasos hechos, el
        # expediente se preparó con la V6.3 (que nunca escribe plantilla_activa.json): no se ejecuta con la V6.4 ni se le escribe nada
        previos = [f for f in sorted(os.listdir(carpeta)) if f.endswith(("_v63_base.xlsx", "_v63_datos.xlsx", "_v63_evaluada.xlsx"))]
        try:
            st0 = json.load(open(os.path.join(carpeta, "estado_pipeline.json"), encoding="utf-8")) or {}
            paso = st0.get("paso") if isinstance(st0, dict) else "ilegible"  # (4.13 §3)
        except (OSError, ValueError):
            paso = "ilegible" if os.path.exists(os.path.join(carpeta, "estado_pipeline.json")) else None
        if previos or (paso not in (None, 0)):
            return (f"el expediente ya tiene {', '.join(previos) or 'estado del pipeline'} (paso {paso}) y no tiene {ARCHIVO}: se preparó con la V6.3 (o es un "
                    f"expediente V6.4 cuya selección registrada se borró; 4.12: no se acredita con una selección nueva) y esta ejecución selecciona {version(cfg)} "
                    f"({sel['config']}); un expediente solo se ejecuta con su plantilla: para la V6.4, prepara un expediente nuevo "
                    f"(cambiar_base.py, o una carpeta con solo las entradas de partida)")
    if es_v64(cfg):
        pc = os.path.join(carpeta, CONF)
        if not os.path.exists(pc):
            return f"la plantilla {version(cfg)} exige {CONF} en el expediente (modo y parámetros explícitos; ver configuracion_economica.py)"
        try:
            conf = json.load(open(pc, encoding="utf-8"))
        except (OSError, ValueError) as e:
            return f"{CONF} no se puede leer: {str(e)[:120]}"
        f = CE.validar(conf)
        if f:
            return f"{CONF} no es válida: " + " | ".join(f)[:900]
        mp = compatibilidad_perimetro(conf, cfg)
        if mp:
            return f"{CONF}: {mp}"
    return None


def registrar(carpeta, cfg):
    """Escribe plantilla_activa.json en la primera ejecución con la V6.4, la V6.4.1 o la V6.3.1 F1 (no lo reescribe si ya existe: comprobar()
    exige que coincida)."""
    if not registra(cfg):
        return None
    pa = os.path.join(carpeta, ARCHIVO)
    if os.path.exists(pa):
        return pa
    reg = seleccion(cfg) | {"nota": "selección explícita de la plantilla de este expediente (encargo 4.11 §3); forma parte del material auditado. "
                                    "Un cambio de plantilla exige un expediente nuevo."}
    json.dump(reg, open(pa, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return pa


def resolver(carpeta, cfg):
    """(4.12 §5) Configuración con la que una llamada a un generador (ficha.py, informe.py, resumen.py; también a mano, sin
    MUNGER_CONFIG) trata el expediente. Devuelve (cfg_efectiva, motivo, nota): con motivo, el generador no escribe ninguna salida.
      - Expediente V6.4 (plantilla_activa.json): vale la configuración cargada si comprobar() la acepta. Si no (p. ej., una llamada a
        mano que cargó config_v2.json), se busca la registrada —su nombre está en plantilla_activa.json, en personaje_v2/— y se usa
        solo si comprobar() la acepta: sus archivos de plantilla, referencia y verificador tienen que tener las huellas registradas.
        El nombre o la versión guardados no bastan para acreditar archivos distintos (encargo 4.12 §3).
      - Expediente sin plantilla_activa.json (V6.3) con una configuración V6.4 cargada: se usa config_v2.json, si comprobar() la acepta.
      - plantilla_activa.json ilegible: motivo.
    Nunca escribe nada."""
    import config_v2  # noqa: E402
    pa = os.path.join(carpeta, ARCHIVO)
    if os.path.exists(pa) and leer(carpeta) is None:
        return cfg, f"{ARCHIVO} no se puede leer: la selección de plantilla del expediente no se puede acreditar", None
    reg = leer(carpeta)
    m = comprobar(carpeta, cfg)
    if not m:
        return cfg, None, None
    if reg:
        nombre = os.path.basename(str(reg.get("config") or ""))
        cand = os.path.join(AQUI, "..", nombre) if nombre else None
        if not cand or not os.path.isfile(cand) or os.path.abspath(cand) == os.path.abspath(cfg.get("_ruta_config") or ""):
            return cfg, f"la selección registrada ({reg.get('version')}, {nombre or 'sin configuración'}) no se puede resolver: {m}", None
        cfg2 = config_v2.cargar(cand)
        m2 = comprobar(carpeta, cfg2)
        if m2:
            return cfg, f"la selección registrada ({reg.get('version')}, {nombre}) no corresponde a los archivos actuales: {m2}", None
        return cfg2, None, f"selección del expediente resuelta: {nombre} ({reg.get('version')}; la configuración cargada era {os.path.basename(cfg.get('_ruta_config') or '')})"
    if registra(cfg):
        cfg2 = config_v2.cargar(config_v2.POR_DEFECTO)
        m2 = comprobar(carpeta, cfg2)
        if not m2:
            return cfg2, None, f"expediente sin plantilla_activa.json (V6.3): se usa config_v2.json, no la configuración {version(cfg)} cargada"
        return cfg, m2, None
    return cfg, m, None


def leer(carpeta):
    pa = os.path.join(carpeta, ARCHIVO)
    try:
        v = json.load(open(pa, encoding="utf-8")) if os.path.exists(pa) else None
    except (OSError, ValueError):
        return None
    # (4.13 §3) solo un objeto con la estructura de la selección; lo demás se trata como ilegible (resolver() da el motivo)
    return v if v is not None and not ESTR.comprobar(v, ESTR.PLANO_PLANTILLA_ACTIVA) else None


def configuracion(carpeta):
    pc = os.path.join(carpeta, CONF)
    try:
        v = json.load(open(pc, encoding="utf-8")) if os.path.exists(pc) else None
    except (OSError, ValueError):
        return None
    # (4.13 §3) solo una configuración con la estructura esperada; comprobar() ya dio el motivo de una que no la tiene
    return v if v is not None and not ESTR.comprobar(v, ESTR.PLANO_CONFIGURACION_ECONOMICA) else None


def experimental(carpeta):
    c = configuracion(carpeta)
    return bool(c) and c.get("modo") == "Experimental"


if __name__ == "__main__":
    import config_v2  # noqa: E402
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    cfg = config_v2.cargar(sys.argv[sys.argv.index("--config") + 1] if "--config" in sys.argv else None)
    m = comprobar(sys.argv[1], cfg)
    print("OK: " + json.dumps(seleccion(cfg), ensure_ascii=False) if not m else "DETENIDO: " + m)
    sys.exit(0 if not m else 2)
