#!/usr/bin/env python3
"""zoetis_t2 · fuentes del segundo tiempo tras `cambiar_base.py preparar` (encargo del coordinador, 19-nov-2026). Autor: Claude orquestación.
  1. Registro de entradas: preparar copia zoetis_t1d/Zoetis/verificacion_entradas.json del ÁRBOL DE TRABAJO (otros agentes trabajan en la rama);
     se fija la versión COMPROMETIDA (git show <commit>:…; el sellado definitivo de zoetis_t1d, 897db35) y se dejan las dos huellas en el rastro.
  2. PDF y HTML del T3 2026 (Release fuentes-examen-20261118, huellas de RELEASE_FUENTES_EXAMEN_SHA256SUMS) en pdf/; el comunicado HTML, sin páginas,
     pasa a texto/ como UNA página «[PDF PAGE 1]» con el mismo procedimiento que el del T2 (zoetis_t1c/resultados/scripts/html_a_texto.py, copiado
     sin cambios en la función de abajo); los dos PDF los extrajo cambiar_base.py (fuentes_adicionales).
  3. FUENTES.tsv: tres filas nuevas.
  4. fuentes_mercado/: el precio del 5-nov-2026 conservado por Mistral (rama mistral/examen-zoetis-t2, resultados_examen/zoetis_t2/fuentes_mercado/
     Zoetis_IR_XNYS_ZTS_historico_acciones_20261118.txt), byte a byte, con su huella comprobada contra el HUELLAS.txt de Mistral, bajo un nombre
     distinto del que ya hay (la transcripción del extractor heredada de zoetis_t1d, que se conserva). SOLO TRANSCRIPCIÓN: falta captura o CSV.
     El Treasury del 5-nov-2026 sale del CSV oficial ya conservado (asset 766892834); se comprueba la fila.
Uso: python3 -I fuentes_zoetis_t2.py CARPETA_ensayo(zoetis_t2) RAIZ_GIT COMMIT_T1D RASTRO.json"""
import hashlib, html.parser, json, os, re, shutil, subprocess, sys
ENS, GIT, COMMIT, RASTRO = sys.argv[1:5]
C = os.path.join(ENS, "Zoetis")
h = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()  # noqa: E731
rastro = {"fecha": "2026-11-19", "autor": "Claude orquestación", "guion": "resultados/scripts/fuentes_zoetis_t2.py", "pasos": []}
# 1) registro comprometido de zoetis_t1d
reg = os.path.join(C, "verificacion_entradas.json")
ruta_t1d = "munger_v2_r1/personaje_v2/empresas_v2_correcciones/2026-11_examen_universo/zoetis_t1d/Zoetis/verificacion_entradas.json"
comp = subprocess.run(["git", "-C", GIT, "show", f"{COMMIT}:{ruta_t1d}"], capture_output=True, check=True).stdout
antes = h(reg)
open(reg, "wb").write(comp)
rastro["pasos"].append({"paso": "registro de entradas de zoetis_t1d en su versión comprometida", "commit": COMMIT, "copiado_por_preparar_sha256": antes,
                        "comprometido_sha256": h(reg), "motivo": "preparar copia el árbol de trabajo; se fija la versión comprometida (sellado definitivo de zoetis_t1d, 897db35; igual en dfc0a2c) para no heredar cambios sin commit"})
# 2) PDF y HTML
REL = os.path.join(ENS, "fuentes_release")
SHA = {"zoetis-10q-2026-q3.pdf": "f797be282a86905e29ea3d41573fba5a645f2db674fc7c0f26fb93c0f71242bf",
       "zoetis-3q2026-financial-results.pdf": "bac00765798eb16967fc509b4f1b8c1011d05664249b70d22737f9bc6135e05d",
       "zoetis-3q2026-press-release.html": "fe2c88a8d6e3b4cf14b2edfb75eb63a39244d9d20109ae32a97493db77aaeb77"}
for n, s in SHA.items():
    assert h(os.path.join(REL, n)) == s, n
    dst = os.path.join(C, "pdf", n)
    assert not os.path.exists(dst), dst
    shutil.copy2(os.path.join(REL, n), dst)
    rastro["pasos"].append({"paso": f"pdf/{n}", "sha256": h(dst)})


class P(html.parser.HTMLParser):  # html_a_texto.py de zoetis_t1c, sin cambios
    def __init__(s):
        super().__init__(); s.out = []; s.skip = 0

    def handle_starttag(s, t, a):
        if t in ("script", "style", "noscript"):
            s.skip += 1
        if t in ("p", "div", "br", "tr", "li", "h1", "h2", "h3", "h4", "table"):
            s.out.append("\n")
        if t in ("td", "th"):
            s.out.append("\t")

    def handle_endtag(s, t):
        if t in ("script", "style", "noscript"):
            s.skip -= 1

    def handle_data(s, d):
        if not s.skip:
            s.out.append(d)


p = P()
p.feed(open(os.path.join(C, "pdf", "zoetis-3q2026-press-release.html"), encoding="utf-8", errors="replace").read())
t = "".join(p.out)
t = re.sub(r"[ \t\xa0]+", " ", t)
t = re.sub(r"\n\s*\n+", "\n\n", t).strip()
txt = os.path.join(C, "texto", "zoetis-3q2026-press-release.txt")
assert not os.path.exists(txt)
open(txt, "w", encoding="utf-8").write("[PDF PAGE 1]\n" + t + "\n\n")
assert "11/05/2026" in t and "Narrowed revenue to a range of $9.220 billion to $9.320 billion" in t
rastro["pasos"].append({"paso": "texto/zoetis-3q2026-press-release.txt (una página, procedimiento de html_a_texto.py)", "sha256": h(txt)})
for n in ("zoetis-10q-2026-q3.txt", "zoetis-3q2026-financial-results.txt"):
    rastro["pasos"].append({"paso": f"texto/{n} (cambiar_base.py, pdftotext -layout con marcas)", "sha256": h(os.path.join(C, "texto", n))})
# 3) FUENTES.tsv
ft = os.path.join(C, "FUENTES.tsv")
filas = open(ft, encoding="utf-8").read()
assert "zoetis-10q-2026-q3" not in filas
nuevas = [
    ["pdf/zoetis-10q-2026-q3.pdf", "zoetis-10q-2026-q3.pdf", SHA["zoetis-10q-2026-q3.pdf"], "53", "Q3 2026 (01.07.2026-30.09.2026; nueve meses 01.01-30.09.2026)", "2026-11-05",
     "Form 10-Q del tercer trimestre de 2026 (creado el 5-nov-2026 16:40 UTC; firmas del 5-nov-2026, PDF p. 50–51). SEGUNDO TIEMPO (zoetis_t2). Texto: texto/zoetis-10q-2026-q3.txt (pdftotext -layout con marcas, cambiar_base.py)."],
    ["pdf/zoetis-3q2026-financial-results.pdf", "zoetis-3q2026-financial-results.pdf", SHA["zoetis-3q2026-financial-results.pdf"], "23", "Q3 2026 (01.07.2026-30.09.2026) y guía 2026 actualizada", "2026-11-05",
     "Presentación de resultados del T3 2026 («November 5, 2026», PDF p. 1; creada el 4-nov-2026 15:13 UTC). SEGUNDO TIEMPO (zoetis_t2). Texto: texto/zoetis-3q2026-financial-results.txt (pdftotext -layout con marcas, cambiar_base.py)."],
    ["pdf/zoetis-3q2026-press-release.html", "zoetis-3q2026-press-release.html", SHA["zoetis-3q2026-press-release.html"], "1", "Q3 2026 (01.07.2026-30.09.2026) y guía 2026 actualizada", "2026-11-05",
     "Comunicado de resultados del T3 2026 (página HTML del emisor, «11/05/2026»), con la sección FULL YEAR 2026 FINANCIAL GUIDANCE (guía a 5-nov-2026, tipos de cambio del 20-oct-2026, frente a la del 6-ago-2026). SEGUNDO TIEMPO (zoetis_t2). Difiere en 1,8 kB de la copia de Mistral (página dinámica); se usa la de la Release (RELEASE_FUENTES_EXAMEN_VERIFICACION.md). Texto: texto/zoetis-3q2026-press-release.txt (una página, procedimiento de html_a_texto.py)."],
]
with open(ft, "a", encoding="utf-8") as f:
    if not filas.endswith("\n"):
        f.write("\n")
    for r in nuevas:
        f.write("\t".join(r) + "\n")
rastro["pasos"].append({"paso": "FUENTES.tsv (3 filas nuevas)", "sha256": h(ft)})
# 4) fuentes de mercado
FM = os.path.join(C, "fuentes_mercado")
src = os.path.join(REL, "Zoetis_IR_XNYS_ZTS_historico_acciones_20261118_mistral_examen_zoetis_t2.txt")
SHA_M = "1eee36e610e2d4980e85f416306c6878d2ba503f92f6859d8933a705556808de"
huellas_mistral = subprocess.run(["git", "-C", "/home/user/munger-v2-evidencias-mistral", "show",
                                  "origin/mistral/examen-zoetis-t2:resultados_examen/zoetis_t2/fuentes_mercado/HUELLAS.txt"], capture_output=True, check=True, text=True).stdout
assert h(src) == SHA_M and SHA_M in huellas_mistral
dst = os.path.join(FM, os.path.basename(src))
assert not os.path.exists(dst)
shutil.copy2(src, dst)
texto_p = open(dst, encoding="utf-8").read()
assert texto_p.startswith("[PDF PAGE 1]") and "November 05, 2026 | $82.11" in texto_p
heredado = open(os.path.join(FM, "Zoetis_IR_XNYS_ZTS_historico_acciones_20261118.txt"), encoding="utf-8").read()
assert "November 05, 2026 $82.11" in heredado
tt = open(os.path.join(FM, "US_Treasury_par_yield_2026_Release_766892834.txt"), encoding="utf-8").read()
fila_t = [l for l in tt.split("\n") if l.startswith("11/05/2026 |")]
assert len(fila_t) == 1 and fila_t[0].split(" | ")[12] == "4.84"
rastro["pasos"].append({"paso": f"fuentes_mercado/{os.path.basename(dst)}", "sha256": h(dst), "fila_usada": "November 05, 2026 | $82.11 (C37)",
                        "origen": "munger-v2-evidencias-mistral, rama mistral/examen-zoetis-t2 (d12c75c), resultados_examen/zoetis_t2/fuentes_mercado/Zoetis_IR_XNYS_ZTS_historico_acciones_20261118.txt",
                        "limitacion": "solo transcripción del extractor (web_fetch de investor.zoetis.com el 18-nov-2026); falta una captura o un CSV original de la página",
                        "contraste": "la transcripción del extractor heredada de zoetis_t1d (Zoetis_IR_XNYS_ZTS_historico_acciones_20261118.txt) da el mismo cierre: «November 05, 2026 $82.11»"})
rastro["pasos"].append({"paso": "Treasury del 5-nov-2026 (sin archivo nuevo)", "archivo": "fuentes_mercado/US_Treasury_par_yield_2026_Release_766892834.txt",
                        "sha256": h(os.path.join(FM, "US_Treasury_par_yield_2026_Release_766892834.txt")), "fila_usada": fila_t[0] + " (columna 13 «10 Yr» = 4.84; C57)"})
hu = os.path.join(FM, "HUELLAS.txt")
open(hu, "a", encoding="utf-8").write("\n".join([
    "", "--- Añadida en zoetis_t2 por Claude orquestación (19-nov-2026; resultados/fuentes_zoetis_t2.json): precio del 5-nov-2026 (segundo tiempo).", "",
    f"archivo: {os.path.basename(dst)}", f"  sha256: {h(dst)}",
    "  contenido: transcripción de la tabla «XNYS:ZTS historical stock data» de investor.zoetis.com hecha por el extractor Mistral (mistral-large-4-0) el "
    "18-nov-2026 (rama mistral/examen-zoetis-t2, la huella de su HUELLAS.txt); fila usada «November 05, 2026 | $82.11» (C37). SOLO TRANSCRIPCIÓN: falta "
    "una captura o un CSV original de la página. La transcripción heredada de zoetis_t1d (arriba) da el mismo cierre.",
    "  C57 (5-nov-2026): fila «" + fila_t[0] + "» del CSV oficial ya conservado (columna «10 Yr» = 4.84).", ""]))
rastro["huellas_txt_sha256"] = h(hu)
json.dump(rastro, open(RASTRO, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(rastro, ensure_ascii=False, indent=1))
