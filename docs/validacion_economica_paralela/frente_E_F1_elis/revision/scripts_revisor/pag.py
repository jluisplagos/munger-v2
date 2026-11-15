"""Imprime páginas PDF (1-indexadas) de un texto generado con pdftotext -layout (páginas separadas por \\f).
Uso: python3 -I pag.py <txt> <pagina>[-<pagina>] [patron_grep]
"""
import re
import sys

def main():
    txt, rng = sys.argv[1], sys.argv[2]
    pat = re.compile(sys.argv[3], re.I) if len(sys.argv) > 3 else None
    pages = open(txt, encoding="utf-8", errors="replace").read().split("\f")
    a, _, b = rng.partition("-")
    a = int(a); b = int(b) if b else a
    for n in range(a, b + 1):
        page = pages[n - 1]
        print(f"===== {txt.split('/')[-1]} · página PDF {n} =====")
        for line in page.splitlines():
            if pat is None or pat.search(line):
                print(line.rstrip())

if __name__ == "__main__":
    main()
