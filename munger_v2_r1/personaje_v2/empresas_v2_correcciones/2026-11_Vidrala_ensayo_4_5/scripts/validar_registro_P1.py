#!/usr/bin/env python3
"""Valida, sin modificarlo, el archivo de decisiones con el registro humano de P1 (entrega 4.5, §2 del encargo).

Uso: python3 -I validar_registro_P1.py <archivo_recibido.json>

Requisitos (todos obligatorios):
  1. Conserva las decisiones anteriores: todas las claves de fase1_decisiones.json de la entrega 4.4 con el mismo contenido.
  2. Añade únicamente circulante_lineas → 2024 (ninguna otra clave ni otro año).
  3. valor_mm = 84.994 (millones; aumento del circulante con la convención de la Historia).
  4. fuente idéntica a la de la propuesta (PROPUESTA_fase1_decisiones_con_P1.json).
  5. fecha y confirmado_por cumplimentados, sin marcadores de posición ni nombres de agentes; fecha con un año reconocible.
El script no rellena ni corrige nada: informa del defecto concreto.
"""
import hashlib, json, os, re, sys
sys.dont_write_bytecode = True
AQUI = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
E44 = os.path.join(AQUI, "..", "2026-11_Vidrala_ensayo")
ANT = os.path.join(E44, "Vidrala", "fase1_decisiones.json")
PROP = os.path.join(E44, "PROPUESTA_fase1_decisiones_con_P1.json")
AGENTES = ("claude", "chatgpt", "gpt", "openai", "anthropic", "opus", "sonnet", "haiku", "fable", "mythos", "agente", "asistente", "ia", "ai", "llm", "bot", "modelo")
MARCADORES = ("", "-", "--", "?", "n/a", "na", "tbd", "todo", "pendiente", "xxx", "xx", "x", "fecha", "nombre", "persona", "dd/mm/aaaa", "aaaa-mm-dd", "yyyy-mm-dd")
N_OK = N_T = 0


def comprobar(nombre, cond, detalle=""):
    global N_OK, N_T
    N_T += 1; N_OK += bool(cond)
    print(f"  [{'CUMPLE' if cond else 'NO CUMPLE'}] {nombre}" + (f" · {detalle}" if detalle else ""))


def humano(v):
    if not isinstance(v, str):
        return False, f"no es texto ({type(v).__name__})"
    s = v.strip()
    if s.lower() in MARCADORES or re.fullmatch(r"[<\[{(].*[>\]})]", s) or re.search(r"(?i)rellenar|completar|placeholder|ejemplo", s):
        return False, f"marcador de posición: «{v}»"
    pal = set(re.findall(r"[a-záéíóúñü]+", s.lower()))
    ag = sorted(pal & set(AGENTES))
    if ag:
        return False, f"contiene nombre de agente: {ag}"
    return True, f"«{s}»"


if len(sys.argv) != 2:
    sys.exit(__doc__)
ruta = sys.argv[1]
raw = open(ruta, "rb").read()
print(f"REGISTRO HUMANO DE P1 · validación de {os.path.basename(ruta)}")
print(f"  bytes {len(raw)} · SHA-256 {hashlib.sha256(raw).hexdigest()}")
try:
    d = json.loads(raw.decode("utf-8"))
    comprobar("JSON válido en UTF-8", True)
except Exception as e:
    comprobar("JSON válido en UTF-8", False, str(e)[:120]); print(f"\nRESULTADO: {N_OK} de {N_T}."); sys.exit(1)
ant = json.load(open(ANT, encoding="utf-8"))
prop = json.load(open(PROP, encoding="utf-8"))
comprobar("1. Conserva todas las decisiones anteriores sin cambios", all(k in d and d[k] == ant[k] for k in ant),
          ", ".join(k for k in ant if d.get(k) != ant[k]))
extra = [k for k in d if k not in ant]
comprobar("2. Solo añade la clave circulante_lineas", extra == ["circulante_lineas"], str(extra))
cl = d.get("circulante_lineas", {})
comprobar("2. circulante_lineas contiene solo el año 2024", isinstance(cl, dict) and list(cl) == ["2024"], str(list(cl) if isinstance(cl, dict) else cl))
r = cl.get("2024", {}) if isinstance(cl, dict) else {}
comprobar("2. La entrada 2024 tiene exactamente valor_mm, fuente, fecha y confirmado_por", isinstance(r, dict) and set(r) == {"valor_mm", "fuente", "fecha", "confirmado_por"}, str(sorted(r) if isinstance(r, dict) else r))
comprobar("3. valor_mm = 84.994", isinstance(r.get("valor_mm"), (int, float)) and not isinstance(r.get("valor_mm"), bool) and r.get("valor_mm") == 84.994, repr(r.get("valor_mm")))
comprobar("4. fuente idéntica a la propuesta", r.get("fuente") == prop["circulante_lineas"]["2024"]["fuente"])
ok, det = humano(r.get("fecha"))
comprobar("5. fecha cumplimentada por la persona (sin marcador ni agente)", ok, det)
comprobar("5. fecha con un año reconocible (20xx)", isinstance(r.get("fecha"), str) and re.search(r"\b20\d\d\b", r["fecha"]) is not None, repr(r.get("fecha")))
ok, det = humano(r.get("confirmado_por"))
comprobar("5. confirmado_por cumplimentado por la persona (sin marcador ni agente)", ok, det)
print(f"\nRESULTADO: {N_OK} de {N_T} requisitos cumplen.")
sys.exit(0 if N_OK == N_T else 1)
