#!/usr/bin/env python3
"""vinci_b · correcciones del registro tras el sellado (munger-v2-evidencias-mistral, coordinacion/cierre_v2/examen/vinci_b/revision_registro/REVISION_SELLADO.md
@ 53e69a5; producto c489b19), por encargo del coordinador (20-nov-2026). Solo el registro: no cambia valores del libro ni fases; no se relanza el pipeline.
Cada entrada tocada queda PENDIENTE de revisor, extractor «Claude orquestación», sin vínculo; no se usa `sellar`.
 1) Historia!C86, D86, E86: se quita la afirmación falsa de que en 2019-2020 la nota 4.3 no desglosa la amortización de derechos de uso (URD 2020 PDF p. 319
    publica 548 y 582); la celda vacía antes de la NIIF 16 sigue siendo correcta.
 2) Palancas!A29: los límites anotan que «Europe excluding France» (28.511, URD 2025 PDF p. 369) incluye Central and Eastern Europe (3.297, 4,4 % de las ventas)
    bajo la etiqueta «Región · Western Europe» (como la aproximación Z-R de Zoetis).
 3) acciones de cinco consejeros (URD 2025 PDF p. 148: Lombard, Aguilar, Assouad, Bertocco Trindade, Zingoni): cada cita pasa a la fila literal de esa persona
    (antes citaban la de Grégoire Sainte Marie o Messemer); los valores no cambian.
 4) Análisis!C96 no se toca: se sellará cuando se resuelvan sus orígenes.
Uso: python3 -I corregir_registro_tras_sellado_vinci_b.py CARPETA_EMPRESA RASTRO.json"""
import copy, hashlib, json, os, re, sys
C, RASTRO = sys.argv[1:3]
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "..", "..", "..", "..", "scripts"))
import verificacion_entradas as VE  # noqa: E402
HOY, EXT = "2026-11-20", "Claude orquestación"
h = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()  # noqa: E731
p = os.path.join(C, VE.REGISTRO)
antes_sha = h(p)
reg = json.load(open(p, encoding="utf-8"))
por = {e["celda"]: e for e in reg["entradas"]}
cambios = []


def pagina(archivo, n):
    t = open(os.path.join(C, archivo), encoding="utf-8").read()
    m = re.search(r"\[PDF PAGE %d\]" % n, t)
    fin = re.search(r"\[PDF PAGE \d+\]", t[m.end():])
    return t[m.end(): m.end() + fin.start()] if fin else t[m.end():]


def linea(archivo, n, contiene):
    ls = [l for l in pagina(archivo, n).split("\n") if contiene in l]
    if len(ls) != 1:
        raise SystemExit(f"{archivo} p.{n}: {len(ls)} líneas con {contiene!r}")
    return ls[0].strip()


def pendiente(e, nota, fuente_examinada=None):
    antes = copy.deepcopy(e)
    c0 = e.get("comprobacion") or {}
    e["comprobacion"] = {"extractor": EXT, "revisor": None, "fecha": HOY, "resultado": "pendiente", "fuente_examinada": fuente_examinada,
                         "nota": f"[{EXT}, {HOY}, vinci_b, tras REVISION_SELLADO.md @ 53e69a5] {nota} · Comprobación anterior: {c0.get('revisor')} {c0.get('fecha')} «{c0.get('resultado')}»: {str(c0.get('nota'))[:300]}",
                         "vinculo": None}
    cambios.append({"celda": e["celda"], "motivo": nota, "antes": antes, "despues": copy.deepcopy(e)})


# 1) C86, D86, E86
for k, anio in (("Historia!C86", 2016), ("Historia!D86", 2017), ("Historia!E86", 2018)):
    e = por[k]
    assert e["clase"] == "dato_ausente" and e.get("valor_modelo") is None, k
    e["justificacion"] = (f"Celda vacía en el libro. {anio} es anterior a la NIIF 16 (aplicada por VINCI desde 2019): no hay derechos de uso cuya amortización deba "
                          "separarse, así que no hay dato publicado que pueble la celda. (La amortización de derechos de uso sí se publica desde 2019: URD 2020 PDF p. 319, "
                          "548 en 2019 y 582 en 2020; ver Historia!F86 y G86, también vacías porque la declaración F1 solo cubre 2021–2025.)")
    pendiente(e, "justificación corregida: se quita que la nota 4.3 no desglosaba la amortización de derechos de uso en 2019-2020 (URD 2020 p. 319 publica 548 y 582)",
              "texto/vinci-urd-2020.txt [PDF PAGE 319]")

# 2) Palancas!A29
e = por["Palancas!A29"]
URD25 = "texto/vinci-urd-2025.txt"
for s in ("Europe excluding France", "Central and Eastern Europe", "Total revenue"):
    assert s in pagina(URD25, 369), s
e["hipotesis"]["limites"] = (e["hipotesis"]["limites"] + " Aproximación en Europa (como la decisión Z-R de Zoetis: se deja la agrupación y se anota la diferencia): la fila "
                             "«Europe excluding France» (28.511, URD 2025 PDF p. 369) que el libro etiqueta «Región · Western Europe» incluye «Central and Eastern Europe» (3.297, "
                             "un 4,4 % de las ventas de 74.599) y «Rest of Europe» (5.732); la etiqueta atribuye a Europa occidental ventas que no son solo suyas y fija con "
                             "ellas la prima de esa región en la r mínima. El peso de la fila (B29) es correcto.")
pendiente(e, "límites: anotada la inclusión de Central and Eastern Europe (3.297, 4,4 %) en «Europe excluding France» etiquetada «Western Europe»",
          f"{URD25} [PDF PAGE 369]")

# 3) acciones de cinco consejeros
for slug, nombre in (("marie_christine_lombard", "Marie-Christine Lombard"), ("carlos_f_aguilar", "Carlos F. Aguilar"), ("yannick_assouad", "Yannick Assouad"),
                     ("karla_bertocco_trindade", "Karla Bertocco Trindade"), ("maria_victoria_zingoni", "María Victoria Zingoni")):
    k = f"aux:vinci-urd-2025_p148_board_shares_{slug}_2025"
    e = por[k]
    cita = linea(URD25, 148, nombre)
    vf = e["fuente"]["valor_fuente"]
    assert VE._cita_cifra(cita, vf, pagina(URD25, 148))[0] == "ok", (k, cita)
    antes = e["fuente"]["cita"]
    e["fuente"]["cita"] = cita
    pendiente(e, f"cita sustituida por la fila literal de {nombre} (antes citaba «{antes[:40]}…»); valor sin cambios", f"{URD25} [PDF PAGE 148]")

reg["nota_vinci_b_tras_sellado"] = (f"{HOY}, {EXT}: tras REVISION_SELLADO.md @ 53e69a5 — justificación de C86:E86, límites de Palancas!A29 y citas de cinco consejeros "
                                    "(p. 148). Rastro: resultados/registro_tras_sellado_vinci_b.json")
json.dump(reg, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump({"fecha": HOY, "guion": "resultados/scripts/corregir_registro_tras_sellado_vinci_b.py", "revision": "REVISION_SELLADO.md @ 53e69a5 (auxiliar); producto c489b19",
           "registro_antes_sha256": antes_sha, "registro_despues_sha256": h(p), "cambios": cambios}, open(RASTRO, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("cambiadas", len(cambios))
