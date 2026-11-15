"""Copia a B los binarios release_asset de la base 4.14 (desde A), sin sobrescribir.
Uso: python3 -I copiar_binarios_a_b.py <baseline.json> <A/munger_v2_r1> <B/munger_v2_r1> <salida.json>
"""
import hashlib, json, os, shutil, sys

def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()

base, A, B, out = sys.argv[1:5]
d = json.load(open(base, encoding='utf-8'))
res = {'copiados': [], 'existentes_iguales': [], 'existentes_distintos': [],
       'origen_ausente_o_distinto': [], 'fallo_tras_copia': []}
assets = [f for f in d['files'] if f.get('storage') == 'release_asset']
for f in assets:
    rel = f['path']
    src = os.path.join(A, rel)
    dst = os.path.join(B, rel)
    if not os.path.isfile(src) or sha(src) != f['sha256']:
        res['origen_ausente_o_distinto'].append(rel)
        continue
    if os.path.lexists(dst):
        hd = sha(dst) if os.path.isfile(dst) else None
        if hd == f['sha256']:
            res['existentes_iguales'].append(rel)
        else:
            res['existentes_distintos'].append({'path': rel, 'sha256_B': hd, 'sha256_base414': f['sha256']})
        continue
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(src, dst)  # conserva bytes y marcas de tiempo
    if sha(dst) == f['sha256'] and os.path.getsize(dst) == f['size']:
        res['copiados'].append(rel)
    else:
        res['fallo_tras_copia'].append(rel)
res['recuento'] = {k: len(v) for k, v in res.items() if isinstance(v, list)}
res['recuento']['release_asset_en_baseline'] = len(assets)
json.dump(res, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(json.dumps(res['recuento'], ensure_ascii=False))
