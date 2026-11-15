# Z-8: archivos citados (entre comillas invertidas) en la documentación de la 4.9 que no existen en el árbol
import os, re, glob
R = "/home/claude/vigencia_4_9/munger_v2_r1"
E = "personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_9"
docs = ["CONTINUIDAD.md", "VERSION", "PROMPT_NUEVA_VENTANA.md", "personaje_v2/DECISIONES.md", "personaje_v2/ANEXO_D_salidas_y_formatos.md"] + \
       [os.path.relpath(p, R) for p in glob.glob(f"{R}/{E}/*.md") + glob.glob(f"{R}/{E}/resultados/*.md") + glob.glob(f"{R}/{E}/n4/efectos/copias/LEEME.txt")]
todos = []
for dp, dn, fn in os.walk(R):
    for f in fn + dn:
        todos.append(os.path.relpath(os.path.join(dp, f), R))
EXT = (".md", ".py", ".json", ".txt", ".csv", ".sh", ".xlsx", ".pdf", ".zip", ".sha256")
falta = {}
for d in docs:
    txt = open(os.path.join(R, d), encoding="utf-8").read()
    if d == "personaje_v2/DECISIONES.md":
        txt = txt[txt.find("## 11-nov-2026"):]
    for m in re.finditer(r"`([^`\n]+)`", txt):
        t = m.group(1).strip()
        t = re.sub(r"\s.*$", "", t) if not t.startswith(("python3", "bash")) else (re.findall(r"\S+\.(?:py|sh)", t) or [""])[0]
        t = t.rstrip(".,;:)")
        if not t or not (("/" in t) or t.endswith(EXT)) or "*" in t or "<" in t or t.startswith(("http", "$", "~", "-")):
            continue
        if t.endswith(".zip") and "munger_v2_r1_entrega" in t or t in ("munger_v2_paquete.zip",):
            continue
        suf = t.replace("…", "").lstrip("/").lstrip("_")
        ok = any(os.path.exists(os.path.join(R, b, t)) for b in ("", E, "personaje_v2", os.path.dirname(d))) or \
             any(x.endswith(suf) for x in todos) or any(x.endswith(suf.rstrip("/")) for x in todos)
        if not ok:
            falta.setdefault(t, set()).add(d)
for t, ds in sorted(falta.items()):
    print(f"NO EXISTE: {t}  ← {', '.join(sorted(ds))}")
print("revisados:", len(docs), "documentos")
