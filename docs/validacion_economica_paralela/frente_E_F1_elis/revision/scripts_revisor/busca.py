"""Busca un patrón (regex) en un texto paginado y muestra página PDF y línea.
Uso: python3 -I busca.py <txt> <regex> [max]
"""
import re
import sys

def main():
    txt, pat = sys.argv[1], re.compile(sys.argv[2], re.I)
    mx = int(sys.argv[3]) if len(sys.argv) > 3 else 80
    pages = open(txt, encoding="utf-8", errors="replace").read().split("\f")
    k = 0
    for n, page in enumerate(pages, 1):
        for line in page.splitlines():
            if pat.search(line):
                print(f"p{n}: {line.strip()[:230]}")
                k += 1
                if k >= mx:
                    return

if __name__ == "__main__":
    main()
