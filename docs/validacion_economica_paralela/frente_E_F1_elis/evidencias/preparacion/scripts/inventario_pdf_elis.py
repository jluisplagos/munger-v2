"""Inventario de PDF de Elis (A) y texto por página.
Uso: python3 -I inventario_pdf_elis.py <raiz_ensayo_A> <dir_textos> <salida_inventario.json>
"""
import hashlib, json, os, re, subprocess, sys

def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()

def leer_huellas(path):
    """Devuelve {nombre_base: huella}. Acepta «huella  ruta» y pares línea-nombre/línea-huella."""
    out = {}
    if not os.path.isfile(path):
        return out
    lines = [l.strip() for l in open(path, encoding='utf-8', errors='replace') if l.strip()]
    hexre = re.compile(r'^[0-9a-f]{64}$')
    i = 0
    while i < len(lines):
        l = lines[i]
        m = re.match(r'^([0-9a-f]{64})\s+\*?(.+)$', l)
        if m:
            out[os.path.basename(m.group(2))] = m.group(1)
            i += 1
            continue
        if i + 1 < len(lines) and hexre.match(lines[i + 1]):
            out[os.path.basename(l)] = lines[i + 1]
            i += 2
            continue
        out.setdefault(os.path.basename(l), None)  # nombre sin huella
        i += 1
    return out

SLUGS = {
    '4 - Document de reference 2016_0.pdf': 'URD2016',
    'Elis - 2017 Registration Document.pdf': 'URD2017',
    'Elis - 2018 Registration document.pdf': 'URD2018',
    'Elis - 2019 Universal Registration Document.pdf': 'URD2019',
    'Elis - 2020 Universal Registration Document.pdf': 'URD2020',
    'Elis_URD_2021_EN.pdf': 'URD2021',
    'Elis - 2022 Universal Registration Document.pdf': 'URD2022',
    'Elis_Universal Registration Document_2023_EN.pdf': 'URD2023',
    "Elis_Document d'enregistrement universel_2024_FR.pdf": 'DEU2024FR',
    'Elis - 2025 Universal Registration Document.pdf': 'URD2025',
    'Elis_Resultats_annuels_2025_communique.pdf': 'RA2025_communique',
    'Elis_2026_half-year_financial_report_EN.pdf': 'H1_2026_EN',
    'Elis_Rapport_financier_semestriel_2026_FR.pdf': 'H1_2026_FR',
    'Elis_H1_2026_results_presentation.pdf': 'H1_2026_pres',
}
ESPERADAS = {
    'Elis - 2025 Universal Registration Document.pdf': '04bfd08724e768804e7110093d3ec2cf017a7e7fe2983bacd75656d3a95cd62e',
    "Elis_Document d'enregistrement universel_2024_FR.pdf": '94e994f0de79cc588240f9866d263c4a5ae27fe3ccff83bc0b817eb91633c1e9',
}

raiz, dir_txt, salida = sys.argv[1:4]
dec = os.path.join(raiz, 'elis_decisiones', 'Elis')
motA = os.path.join(raiz, 'elis_motor_A', 'Elis', 'fuentes_pdf')
h_pdf = leer_huellas(os.path.join(dec, 'fuentes_pdf', 'HUELLAS_PDF.txt'))
h_2026 = {}
for fn in sorted(os.listdir(os.path.join(dec, 'fuentes_2026'))):
    if fn.startswith('HUELLAS') and fn.endswith('.txt'):
        h_2026[fn] = leer_huellas(os.path.join(dec, 'fuentes_2026', fn))
h_motA = leer_huellas(os.path.join(motA, 'HUELLAS_PDF.txt'))

items = []
for sub in ('fuentes_pdf', os.path.join('fuentes_2026', 'pdf')):
    d = os.path.join(dec, sub)
    for fn in sorted(os.listdir(d)):
        if fn.lower().endswith('.pdf'):
            items.append((sub, fn, os.path.join(d, fn)))

inv, indice = [], []
for sub, fn, p in items:
    e = {'carpeta': sub, 'archivo': fn,
         'ruta_relativa_ensayo': os.path.join('elis_decisiones', 'Elis', sub, fn),
         'bytes': os.path.getsize(p), 'sha256': sha(p)}
    info = subprocess.run(['pdfinfo', p], capture_output=True, text=True, cwd='/')
    m = re.search(r'^Pages:\s+(\d+)', info.stdout, re.M)
    e['paginas_pdfinfo'] = int(m.group(1)) if m else None
    e['pdfinfo_codigo'] = info.returncode
    if info.returncode != 0:
        e['pdfinfo_stderr'] = info.stderr.strip()[:500]
    # huellas registradas
    if sub == 'fuentes_pdf':
        reg = {'HUELLAS_PDF.txt': h_pdf.get(fn, 'NO_LISTADO')}
    else:
        reg = {k: v.get(fn, 'NO_LISTADO') for k, v in h_2026.items()}
    e['huellas_registradas'] = reg
    e['coincide_huella_registrada'] = {k: (v == e['sha256']) if v not in (None, 'NO_LISTADO') else v
                                       for k, v in reg.items()}
    if fn in ESPERADAS:
        e['huella_esperada_encargo'] = ESPERADAS[fn]
        e['coincide_huella_esperada_encargo'] = ESPERADAS[fn] == e['sha256']
    if sub == 'fuentes_pdf':
        pm = os.path.join(motA, fn)
        if os.path.isfile(pm):
            hm = sha(pm)
            e['motor_A'] = {'existe': True, 'sha256': hm, 'igual': hm == e['sha256'],
                            'huella_en_HUELLAS_PDF_motor_A': h_motA.get(fn, 'NO_LISTADO')}
        else:
            e['motor_A'] = {'existe': False}
    # texto por página
    slug = SLUGS.get(fn)
    e['slug'] = slug
    if slug:
        od = os.path.join(dir_txt, slug)
        os.makedirs(od, exist_ok=False)
        full = os.path.join(dir_txt, '_completos', slug + '.txt')
        os.makedirs(os.path.dirname(full), exist_ok=True)
        r = subprocess.run(['pdftotext', '-layout', p, full], capture_output=True, text=True, cwd='/')
        e['pdftotext_codigo'] = r.returncode
        if r.stderr.strip():
            e['pdftotext_stderr'] = r.stderr.strip()[:1000]
        txt = open(full, encoding='utf-8', errors='replace').read()
        partes = txt.split('\f')
        cola_vacia_descartada = False
        if len(partes) > 1 and partes[-1].strip() == '':
            partes = partes[:-1]
            cola_vacia_descartada = True
        vacias = []
        for i, t in enumerate(partes, 1):
            with open(os.path.join(od, 'p%04d.txt' % i), 'w', encoding='utf-8') as f:
                f.write(t)
            if t.strip() == '':
                vacias.append(i)
        e['paginas_extraidas'] = len(partes)
        e['segmento_final_vacio_tras_ultimo_FF_descartado'] = cola_vacia_descartada
        e['paginas_coinciden'] = len(partes) == e['paginas_pdfinfo']
        e['paginas_vacias'] = vacias
        indice.append({'slug': slug, 'ruta_original': e['ruta_relativa_ensayo'], 'sha256': e['sha256'],
                       'paginas_pdfinfo': e['paginas_pdfinfo'], 'paginas_extraidas': len(partes),
                       'paginas_coinciden': e['paginas_coinciden'],
                       'hay_paginas_vacias': bool(vacias), 'paginas_vacias': vacias})
    inv.append(e)

# huellas listadas sin archivo presente
pres_pdf = {fn for s, fn, _ in items if s == 'fuentes_pdf'}
pres_2026 = set(os.listdir(os.path.join(dec, 'fuentes_2026'))) | set(os.listdir(os.path.join(dec, 'fuentes_2026', 'pdf')))
listados_sin_archivo = {
    'HUELLAS_PDF.txt': sorted(k for k in h_pdf if k not in pres_pdf),
    **{k: sorted(n for n in v if n not in pres_2026) for k, v in h_2026.items()},
    'nombres_sin_huella': {k: sorted(n for n, h in v.items() if h is None) for k, v in {'HUELLAS_PDF.txt': h_pdf, **h_2026}.items()},
}
json.dump({'inventario': inv, 'listados_sin_archivo': listados_sin_archivo},
          open(salida, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.dump({'nota': 'Numeración = página PDF desde 1. Texto: pdftotext -layout, dividido por \\f. '
                   'Si tras el último \\f queda un segmento vacío (solo espacios), se descarta y no cuenta como página. '
                   'Ruta relativa a munger_v2_r1/personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_14/ '
                   'del worktree A (base 4.14, d69d4837). Página vacía = sin texto no blanco (posible imagen sin capa de texto).',
           'documentos': indice},
          open(os.path.join(dir_txt, 'INDICE.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for e in inv:
    print(e.get('slug'), e['bytes'], e['paginas_pdfinfo'], e.get('paginas_extraidas'),
          e['coincide_huella_registrada'], e.get('coincide_huella_esperada_encargo', ''),
          e.get('motor_A', {}).get('igual', ''), 'vacias=%d' % len(e.get('paginas_vacias', [])))
print(json.dumps(listados_sin_archivo, ensure_ascii=False))
