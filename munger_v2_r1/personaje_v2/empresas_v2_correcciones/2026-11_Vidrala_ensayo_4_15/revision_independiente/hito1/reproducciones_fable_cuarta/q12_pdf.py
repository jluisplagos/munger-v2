"""Cuarta pasada (sonda q12 de la tercera; solo cambian el árbol y el arnés: regresión del 12 y de T4; las variantes nuevas están en r4_t4_tipo.py).
Texto original: Tercera pasada · hallazgo 12 (fuente .pdf: cabecera %PDF y la cita en esa página del PDF; valor de texto como palabra completa).
Parte A (sintética, arnés fx4): el control solo se aplica si el nombre del archivo termina en «.pdf»; página equivocada; PDF sin capa
de texto (escaneado); diferencias tipográficas entre el texto conservado y pdftotext.
Parte B (PDF reales del árbol, solo lectura): Elis y Viscofan 4.14 citando el PDF conservado con su texto extraído como «archivo_texto»:
¿cuántas entradas legítimas rechaza el control nuevo?  Uso: python3 -B q12_pdf.py [A|B|AB]"""
import copy, hashlib, json, os, shutil, sys, time

QUE = sys.argv[1] if len(sys.argv) > 1 else "AB"


def pdf_minimo(paginas):
    """Copia de pdf_minimo de test_verificacion_entradas_415.py (PDF mínimo, una página por texto)."""
    objs = []

    def esc(t):
        b = t.encode("cp1252", errors="replace")
        return b.replace(b"\\", b"\\\\").replace(b"(", b"\\(").replace(b")", b"\\)")
    n = len(paginas)
    kids = " ".join(f"{4 + 2 * i} 0 R" for i in range(n))
    objs.append(b"<< /Type /Catalog /Pages 2 0 R >>")
    objs.append(f"<< /Type /Pages /Kids [{kids}] /Count {n} >>".encode())
    objs.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>")
    for i, t in enumerate(paginas):
        lineas = str(t).split("\n")
        cont = b"BT /F1 9 Tf 40 800 Td 11 TL " + b" ".join(b"(" + esc(l) + b") Tj T*" for l in lineas) + b" ET" if str(t) else b""
        objs.append(f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 3 0 R >> >> /Contents {5 + 2 * i} 0 R >>".encode())
        objs.append(b"<< /Length " + str(len(cont)).encode() + b" >>\nstream\n" + cont + b"\nendstream")
    out = b"%PDF-1.4\n"
    offs = []
    for j, o in enumerate(objs, 1):
        offs.append(len(out))
        out += f"{j} 0 obj\n".encode() + o + b"\nendobj\n"
    xref = len(out)
    out += f"xref\n0 {len(objs) + 1}\n0000000000 65535 f \n".encode() + b"".join(f"{x:010d} 00000 n \n".encode() for x in offs)
    out += f"trailer\n<< /Size {len(objs) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode()
    return out


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


if "A" in QUE:
    import fx4 as fx
    from fx4 import VE, con, ent, resumen, K, REG, FS
    print("=== A · sintética")
    paginas = list(fx.paginas)
    sha_txt = sha(os.path.join(FS, "fuente.txt"))
    pag_k = int(ent(REG, K)["fuente"]["pagina"])
    print("K:", K, "página", pag_k, "| cita:", ent(REG, K)["fuente"]["cita"])

    def caso(nombre, r, k=K):
        print(f"[{nombre}] {resumen(r, k, 300)}")

    # A1 · bytes ajenos con otro nombre de archivo (el control de PDF se decide por la extensión del nombre)
    for nombre in ("ajeno.pdf", "ajeno.PDF", "ajeno.pdf.bak", "ajeno.bin", "ajeno.html", "ajeno_pdf", "informe_anual"):
        open(os.path.join(FS, nombre), "wb").write(b"bytes que no tienen nada que ver con el texto conservado\n")
        s = sha(os.path.join(FS, nombre))
        r = con(lambda g: ent(g, K)["fuente"].update(archivo=f"fuentes_sinteticas/{nombre}", sha256=s, archivo_texto="fuentes_sinteticas/fuente.txt", sha256_texto=sha_txt), resellar=True)
        caso(f"A1 · «fuente conservada» de bytes ajenos llamada {nombre!r} + archivo_texto sintético con su huella", r)
    # A2 · PDF verdadero con la cita en OTRA página (el texto conservado la sitúa en la página de K)
    otras = list(paginas)
    otras[pag_k - 1], otras[pag_k] = otras[pag_k], otras[pag_k - 1]
    open(os.path.join(FS, "otra_pagina.pdf"), "wb").write(pdf_minimo(otras))
    s = sha(os.path.join(FS, "otra_pagina.pdf"))
    r = con(lambda g: ent(g, K)["fuente"].update(archivo="fuentes_sinteticas/otra_pagina.pdf", sha256=s, archivo_texto="fuentes_sinteticas/fuente.txt", sha256_texto=sha_txt), resellar=True)
    caso("A2 · PDF verdadero con el MISMO texto, pero la cita está en la página siguiente del PDF", r)
    # A3 · PDF verdadero y fiel: aceptado
    open(os.path.join(FS, "fiel.pdf"), "wb").write(pdf_minimo(paginas))
    s_f = sha(os.path.join(FS, "fiel.pdf"))
    r = con(lambda g: ent(g, K)["fuente"].update(archivo="fuentes_sinteticas/fiel.pdf", sha256=s_f, archivo_texto="fuentes_sinteticas/fuente.txt", sha256_texto=sha_txt), resellar=True)
    caso("A3 · control positivo: PDF verdadero y fiel a su texto conservado", r)
    # A4 · PDF sin capa de texto en esa página (escaneado; el texto conservado vendría de un OCR)
    sin_texto = list(paginas)
    sin_texto[pag_k - 1] = ""
    open(os.path.join(FS, "escaneado.pdf"), "wb").write(pdf_minimo(sin_texto))
    s = sha(os.path.join(FS, "escaneado.pdf"))
    r = con(lambda g: ent(g, K)["fuente"].update(archivo="fuentes_sinteticas/escaneado.pdf", sha256=s, archivo_texto="fuentes_sinteticas/fuente.txt", sha256_texto=sha_txt), resellar=True)
    caso("A4 · PDF verdadero cuya página citada NO tiene capa de texto (escaneado; el texto conservado sería un OCR)", r)
    # A5 · el PDF verdadero solo contiene la CIFRA en esa página (otro concepto); la cita del registro es solo la cifra
    solo = list(paginas)
    vf = ent(REG, K)["fuente"]["valor_fuente"]
    solo[pag_k - 1] = f"Otro concepto distinto (no son las ventas): {vf:.3f}"
    open(os.path.join(FS, "solo_cifra.pdf"), "wb").write(pdf_minimo(solo))
    s = sha(os.path.join(FS, "solo_cifra.pdf"))
    txt2 = "".join(f"[PDF PAGE {i + 1}]\n{p}\n" for i, p in enumerate(paginas))
    r = con(lambda g: ent(g, K)["fuente"].update(archivo="fuentes_sinteticas/solo_cifra.pdf", sha256=s, archivo_texto="fuentes_sinteticas/fuente.txt", sha256_texto=sha_txt, cita=f"{vf:.3f}"), resellar=True)
    caso("A5 · la cita es solo la cifra; el texto conservado dice «Partida sintética de K», el PDF dice «Otro concepto distinto»", r)
    # A6 · comparación de textos: diferencias tipográficas habituales entre un texto conservado y pdftotext
    print("A6 · VE._cmp_txt (forma de comparación con el PDF):")
    for a, b in (("Beneficio 1 234,5", "Beneficio 1 234,5"), ("beneficio", "beneﬁcio"), ("Resultado -12,3", "Resultado −12,3"), ("Resultado -12,3", "Resultado –12,3"),
                 ("l'exercice", "l’exercice"), ("consolidated", "consoli­dated"), ("consolidated", "consoli-\ndated"), ("EBITDA 12,3", "EBITDA12,3"), ("œuvre", "oeuvre"), ("€", "EUR")):
        print(f"   {a!r} == {b!r}: {VE._cmp_txt(a) == VE._cmp_txt(b)}")
    print("A6 · VE._contiene_texto (valor de texto como palabra completa):")
    for hay, aguja in (("Divisa: NEURROS", "EUR"), ("Divisa: EUR (millones)", "eur"), ("Importes en EUR.", "EUR"), ("en millones de euros (EUR)", "EUR"), ("EUR/USD", "EUR"), ("EUR_miles", "EUR"),
                       ("NIIF-UE", "NIIF"), ("normas IFRS-EU", "IFRS"), ("IFRS16", "IFRS"), ("IFRS (IFRS-EU)", "IFRS (IFRS-EU)"), ("cifras en EUR'000", "EUR"), ("€", "€"), ("importes en € (miles)", "€"),
                       ("Mercado continuo", "continuo"), ("C++ y más", "C++")):
        print(f"   {aguja!r} en {hay!r}: {VE._contiene_texto(hay, aguja)}")
    fx.limpiar()

if "B" in QUE:
    PV = os.environ.get("PV", "/tmp/rev_fable4/congelado4/personaje_v2")
    sys.path.insert(0, os.path.join(PV, "scripts"))
    import verificacion_entradas as VE  # noqa: E402,F811
    E414 = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_14")
    E412 = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_12")
    print("\n=== B · PDF reales (solo lectura): la misma entrada citando el .txt (como hoy) y citando el PDF con «archivo_texto»")
    import tempfile
    for nombre, exp, dir_pdf in (("Elis", os.path.join(E414, "elis_decisiones", "Elis"), "fuentes_pdf"),
                                 ("Viscofan", os.path.join(E414, "viscofan_decisiones", "Viscofan"), os.path.join(E412, "viscofan", "fuentes", "pdf"))):
        t0 = time.time()
        carpeta = exp
        if os.path.isabs(dir_pdf):
            # Viscofan: los PDF no están en el expediente; copia temporal del expediente (sin libros pesados) con los PDF dentro
            tmp = tempfile.mkdtemp(prefix="rev_fable_pdf_")
            carpeta = os.path.join(tmp, "Viscofan")
            os.makedirs(carpeta)
            shutil.copytree(os.path.join(exp, "texto"), os.path.join(carpeta, "texto"))
            shutil.copytree(dir_pdf, os.path.join(carpeta, "fuentes_pdf"))
            shutil.copy(os.path.join(exp, VE.REGISTRO), carpeta)
            dir_pdf = "fuentes_pdf"
        reg = json.load(open(os.path.join(carpeta, VE.REGISTRO), encoding="utf-8"))
        shas, n_tot, n_sin_pdf, base_ok, pdf_ok, fallos, paginas_txt = {}, 0, 0, 0, 0, [], {}
        for e in reg["entradas"]:
            f = e.get("fuente") if isinstance(e.get("fuente"), dict) else None
            if e.get("clase") not in ("dato_publicado", "cero_comprobado") or not f or not str(f.get("archivo") or "").startswith("texto/"):
                continue
            n_tot += 1
            txt = f["archivo"]
            pdf = os.path.join(dir_pdf, os.path.basename(txt)[:-4] + ".pdf")
            if not os.path.isfile(os.path.join(carpeta, pdf)):
                n_sin_pdf += 1
                continue
            for p in (txt, pdf):
                if p not in shas:
                    shas[p] = sha(os.path.join(carpeta, p))
            vf = f.get("valor_fuente")
            r0 = VE.contraste_pagina(carpeta, e["celda"], f, VE._ruta_fuente(carpeta, txt), vf)
            f2 = dict(copy.deepcopy(f), archivo=pdf, sha256=shas[pdf], archivo_texto=txt, sha256_texto=shas[txt])
            r1 = VE.contraste_pagina(carpeta, e["celda"], f2, VE._ruta_fuente(carpeta, pdf), vf)
            base_ok += r0 is None
            pdf_ok += r1 is None
            if r0 is None and r1 is not None:
                fallos.append((e["celda"], pdf, f.get("pagina"), r1[0], str(f.get("cita"))[:110], r1[1][:150]))
        print(f"== {nombre}: {n_tot} entradas con fuente texto/…; sin PDF homónimo {n_sin_pdf}; pasan citando el .txt: {base_ok}; pasan citando el PDF + archivo_texto: {pdf_ok}; "
              f"rechazadas SOLO por el control del PDF: {len(fallos)}  ({time.time() - t0:.0f} s)")
        for x in fallos[:12]:
            print("   ", x)
        if carpeta != exp:
            shutil.rmtree(os.path.dirname(carpeta), ignore_errors=True)
