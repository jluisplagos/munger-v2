"""PDF mínimo de una página por texto (copia de pdf_minimo de test_verificacion_entradas_415.py del árbol congelado)."""


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
