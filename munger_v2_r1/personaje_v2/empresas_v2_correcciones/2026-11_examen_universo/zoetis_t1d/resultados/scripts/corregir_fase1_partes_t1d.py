#!/usr/bin/env python3
"""zoetis_t1d · corrección registrada de fase1_partes/AR_2018.json (minoritarios 2018), tras cambiar_base.py preparar.
Por qué: el sellado del registro de zoetis_t1c (REVISION_SELLADO.md, Historia!E26) comprobó que el 10-K 2018 (PDF p. 73) imprime «—» en la columna de 2018
de «Equity attributable to noncontrolling interests» (y 16 en 2017): es un cero PUBLICADO, no un dato ausente. La fase 1 dejó «actual» vacío («'—' en balance
(sin importe); no se declara cero»), así que la Historia guardaba E26 vacío. Se declara el «—» impreso como la cifra de 2018 (como el 2024 de AR_2024.json,
«impreso» «—»), con su línea literal y su página; fase1_historia.py lo convierte en 0. La corrección de cambiar_base.py (correcciones_fase1_partes) no sirve
porque exige una entrada existente que sustituir. No cambia ninguna otra partida. El original queda en antecedentes/fase1_partes_original/.
Uso: python3 -I corregir_fase1_partes_t1d.py CARPETA_EMPRESA CARPETA_ANTECEDENTES REGISTRO.json"""
import copy, hashlib, json, os, shutil, sys

C, ANT, REG = sys.argv[1:4]
h = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()  # noqa: E731
src = os.path.join(C, "fase1_partes", "AR_2018.json")
d = json.load(open(src, encoding="utf-8"))
m = d["partidas"]["minoritarios"]
ESPERADO_NOTA = "2018: '—' en balance (sin importe); no se declara cero."
if m.get("actual") is not None or m.get("cero") is not None or m.get("nota") != ESPERADO_NOTA:
    sys.exit(f"DETENIDO (nada escrito): AR_2018 · minoritarios no es el esperado: {json.dumps(m, ensure_ascii=False)[:300]}")
LINEA = "Equity attributable to noncontrolling interests — 16"
nuevo = copy.deepcopy(d)
nuevo["partidas"]["minoritarios"]["actual"] = [{"concepto": "Equity attributable to noncontrolling interests", "impreso": "—", "pagina": 73, "linea": LINEA}]
nuevo["partidas"]["minoritarios"]["nota"] = ("(zoetis_t1d, corrección registrada) 2018 = «—» impreso en el balance consolidado del 10-K 2018 (PDF p. 73; 2017 = 16): cero "
                                              "publicado, no dato ausente (sellado del registro de zoetis_t1c, Historia!E26). Nota anterior del lector: " + ESPERADO_NOTA)
sys.path.insert(0, os.path.abspath(os.path.join(C, *[".."] * 4, "scripts")))
import fase1_historia as FH  # noqa: E402
tmp = C.rstrip("/") + ".comprobacion_tmp"
if os.path.exists(tmp):
    sys.exit(f"existe {tmp}")
os.makedirs(os.path.join(tmp, "fase1_partes"))
os.symlink(os.path.abspath(os.path.join(C, "texto")), os.path.join(tmp, "texto"))
json.dump(nuevo, open(os.path.join(tmp, "fase1_partes", "AR_2018.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
err = FH.comprobar_anio(tmp, 2018)
shutil.rmtree(tmp)
if err:
    sys.exit("DETENIDO (nada escrito): la corrección no pasa comprobar_anio: " + json.dumps(err, ensure_ascii=False))
orig = os.path.join(ANT, "fase1_partes_original")
os.makedirs(orig, exist_ok=True)
o = os.path.join(orig, "AR_2018.json")
if os.path.exists(o):
    sys.exit(f"ya existe el original guardado {o}: no se sobrescribe")
shutil.copy2(src, o)
json.dump(nuevo, open(src, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump({"fecha": "2026-11-19", "autor": "Claude orquestación (agente de implementación, encargo del coordinador); sin firma humana", "guion": os.path.abspath(__file__),
           "archivo": "fase1_partes/AR_2018.json", "original": os.path.relpath(o, os.path.dirname(ANT)), "original_sha256": h(o), "nuevo_sha256": h(src),
           "cambio": {"partida": "minoritarios", "campo": "actual", "antes": None, "despues": nuevo["partidas"]["minoritarios"]["actual"],
                      "nota_antes": ESPERADO_NOTA, "nota_despues": nuevo["partidas"]["minoritarios"]["nota"]},
           "fuente": "texto/zoetis-10k-fy2018.txt [PDF PAGE 73], balance consolidado: «Equity attributable to noncontrolling interests — 16»",
           "motivo": "cero publicado («—») en vez de dato ausente (REVISION_SELLADO.md de zoetis_t1c, Historia!E26)"},
          open(REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("OK: AR_2018.json corregido; comprobar_anio sin errores")
