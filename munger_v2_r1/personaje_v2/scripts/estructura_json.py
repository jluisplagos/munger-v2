#!/usr/bin/env python3
"""Validación estructural explícita de los JSON de entrada y de control (encargo 4.13 §3).

Hasta la 4.12, varias lecturas usaban `.get` sobre lo que devolvía `json.load` sin comprobar que fuera un objeto. Un archivo
alterado con JSON válido pero de otro tipo (null, [], 3, "x", o un campo anidado con otro tipo: N1 = []) producía AttributeError
ANTES de la comprobación de vigencia: la llamada terminaba con una excepción y el expediente conservaba concluido/APROBADO, la ficha
cerrada, el cierre registrado y la fila aprobada del resumen de un material que ya no era el auditado.

Este módulo da tres piezas que se usan antes de interpretar un archivo:
  - `comprobar(valor, plano)`: lista de faltas estructurales («N1: se esperaba objeto o nulo, es lista»), sin excepciones;
  - `leer_objeto(ruta, plano)`: (objeto o None, faltas): ausente, ilegible, JSON que no es un objeto o estructura incorrecta;
  - `protegido(fn, *args, contexto=…)`: segunda barrera: cualquier excepción de estructura (AttributeError, TypeError, KeyError,
    IndexError, ValueError) se convierte en un motivo explícito, nunca en una salida abrupta que deje una aprobación sin retirar.
Un plano es {"tipo": tipo o tupla de tipos, "campos": {clave: plano}, "elementos": plano, "valores": plano}; los tipos son
"objeto", "lista", "texto", "numero", "booleano" y "nulo". Los campos no declarados se aceptan (no se rechaza información extra).
"""
import json
import os

_TIPOS = {"objeto": dict, "lista": list, "texto": str, "booleano": bool}


def tipo_de(x):
    if x is None:
        return "nulo"
    if isinstance(x, bool):
        return "booleano"
    if isinstance(x, (int, float)):
        return "numero"
    if isinstance(x, str):
        return "texto"
    if isinstance(x, list):
        return "lista"
    if isinstance(x, dict):
        return "objeto"
    return type(x).__name__


def _es(x, t):
    if t == "nulo":
        return x is None
    if t == "numero":
        return isinstance(x, (int, float)) and not isinstance(x, bool)
    return isinstance(x, _TIPOS[t])


def comprobar(valor, plano, ruta=""):
    """Faltas estructurales de `valor` frente a `plano` (lista vacía si cumple). Nunca lanza excepciones."""
    tipos = plano.get("tipo") or ()
    tipos = (tipos,) if isinstance(tipos, str) else tuple(tipos)
    nombre = ruta or "raíz"
    if tipos and not any(_es(valor, t) for t in tipos):
        return [f"{nombre}: se esperaba {' o '.join(tipos)}, es {tipo_de(valor)}"]
    f = []
    if isinstance(valor, dict):
        for k, sub in (plano.get("campos") or {}).items():
            if k in valor:
                f += comprobar(valor[k], sub, f"{ruta}.{k}" if ruta else k)
        if plano.get("valores"):
            for k, v in valor.items():
                f += comprobar(v, plano["valores"], f"{ruta}.{k}" if ruta else str(k))
    if isinstance(valor, list) and plano.get("elementos"):
        for i, v in enumerate(valor):
            f += comprobar(v, plano["elementos"], f"{nombre}[{i}]")
    return f


def leer_objeto(ruta, plano=None):
    """(objeto, faltas). Sin archivo: (None, []); ilegible o de otra estructura: (None, [motivo…])."""
    if not os.path.lexists(ruta):
        return None, []
    try:
        v = json.load(open(ruta, encoding="utf-8"))
    except (OSError, ValueError) as e:
        return None, [f"{os.path.basename(ruta)} no se puede leer ({type(e).__name__}: {str(e)[:80]})"]
    f = comprobar(v, plano or {"tipo": "objeto"})
    if f:
        return None, [f"{os.path.basename(ruta)}: estructura incorrecta: " + "; ".join(f)[:400]]
    return v, []


def protegido(fn, *args, contexto="", **kw):
    """(resultado, motivo). Si `fn` lanza una excepción de estructura, (None, motivo) en lugar de interrumpir la llamada."""
    try:
        return fn(*args, **kw), None
    except (AttributeError, TypeError, KeyError, IndexError, ValueError) as e:
        return None, f"{contexto or getattr(fn, '__name__', 'lectura')}: estructura inesperada en un archivo de entrada o de control ({type(e).__name__}: {str(e)[:120]})"


# ---------- planos de los archivos afectados ----------
T, N, O, L, B, NU = "texto", "numero", "objeto", "lista", "booleano", "nulo"
_TRAZA = {"tipo": (O, NU), "campos": {k: {"tipo": (T, NU)} for k in ("clase", "confianza", "fuente_o_condicion", "justificacion", "materialidad")}}
PLANO_CONFIGURACION_ECONOMICA = {"tipo": O, "campos": {
    "tipo": {"tipo": (T, NU)}, "version_formato": {"tipo": (N, NU)}, "modo": {"tipo": (T, NU)}, "naturaleza": {"tipo": (T, NU)},
    "protocolo_objetivo": {"tipo": (T, NU)},
    "N1": {"tipo": (O, NU), "campos": {"valor": {"tipo": (N, NU)}, **{k: {"tipo": (T, NU)} for k in ("fuente", "periodo", "perimetro", "clase", "escudo")}}},
    "N2": {"tipo": (O, NU), "campos": {"valor": {"tipo": (N, NU)}, "perimetro": {"tipo": (T, NU)}, "procedencia": {"tipo": (T, NU)}}},
    "N3": {"tipo": (O, NU), "campos": {"regla": {"tipo": (T, NU)}, "fuente": {"tipo": (T, NU)},
                                       **{k: {"tipo": (N, NU)} for k in ("existencias", "deudores", "acreedores")}}},
    "PM1": {"tipo": (O, NU), "campos": {
        **{k: {"tipo": (T, NU)} for k in ("estructura", "familia", "convencion_anios", "convencion_terminal", "roic_terminal", "cartera", "cartera_fuente",
                                           "perimetro_inversion", "altas_fuente")},
        **{k: {"tipo": (N, NU)} for k in ("lambda", "theta", "cartera_anual", "cartera_vnc")},
        **{k: {"tipo": (L, NU), "elementos": {"tipo": N}} for k in ("lambda_rango", "theta_rango", "cartera_historica", "altas_derechos_uso")}}},
    "trazabilidad": {"tipo": (O, NU), "valores": _TRAZA}}}
PLANO_PLANTILLA_ACTIVA = {"tipo": O, "campos": {
    **{k: {"tipo": (T, NU)} for k in ("version", "config", "archivo", "referencia", "verificador", "nota",
                                       "archivo_sha256", "referencia_sha256", "verificador_sha256")},
    "version_config": {"tipo": (T, N, NU)}}}
PLANO_VARIANTES_V64 = {"tipo": O, "campos": {"variantes": {"tipo": (L, NU), "elementos": {"tipo": O}},
                                             "entradas_economicas": {"tipo": (O, NU)}, "rango": {"tipo": (O, NU)}}}
