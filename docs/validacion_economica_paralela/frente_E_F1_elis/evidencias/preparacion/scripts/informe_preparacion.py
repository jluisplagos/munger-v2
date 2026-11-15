"""Compone /home/user/e_work/inventario/preparacion.json a partir de los registros generados."""
import hashlib, json, os, subprocess

W = '/home/user/e_work'
INV = os.path.join(W, 'inventario')
ENS = 'munger_v2_r1/personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_14'

def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()

def git(wt, *a):
    return subprocess.run(['git', '-C', wt, *a], capture_output=True, text=True).stdout.strip()

zipf = os.path.join(W, 'dl_base414', 'munger_v2_r1_entrega4.14_cierre_verificacion_entradas.zip')
verif = json.load(open(os.path.join(INV, 'VERIFICACION_BASE_COMPLETA_LOCAL_414.json'), encoding='utf-8'))
copia = json.load(open(os.path.join(INV, 'copia_binarios_A_a_B.json'), encoding='utf-8'))
pdfs = json.load(open(os.path.join(INV, 'inventario_pdf_elis.json'), encoding='utf-8'))
indice = json.load(open(os.path.join(W, 'textos_pdf', 'INDICE.json'), encoding='utf-8'))
logB = open(os.path.join(INV, 'log_verif_B_completo.txt'), encoding='utf-8').read().splitlines()

xl = {}
for wt in ('wt_main414', 'wt_hito415'):
    base = os.path.join(W, wt, ENS)
    d = {}
    for sub in ('elis_decisiones/Elis', 'elis_motor_A/Elis'):
        for root, _, files in os.walk(os.path.join(base, sub)):
            for fn in files:
                if fn.endswith('.xlsx'):
                    p = os.path.join(root, fn)
                    d[os.path.relpath(p, base)] = sha(p)
    xl[wt] = dict(sorted(d.items()))
ev = xl['wt_main414'].get('elis_decisiones/Elis/Elis_v63_evaluada.xlsx')
evB = xl['wt_hito415'].get('elis_decisiones/Elis/Elis_v63_evaluada.xlsx')
ESP_EV = 'd2593777650f1d9d77bcc7b9eaa6f4c0c12a742fa4706bd20b35808f99c92385'

out = {
 'fecha': subprocess.run(['date', '-Is'], capture_output=True, text=True).stdout.strip(),
 'raiz_trabajo': W,
 'repositorio': {'ruta': '/home/user/munger-v2', 'rama': git('/home/user/munger-v2', 'rev-parse', '--abbrev-ref', 'HEAD'),
                 'cambios_en_repositorio': 'ninguno (solo git worktree add --detach y git worktree list)'},
 'paso1_worktree_A': {'comando': 'git worktree add --detach /home/user/e_work/wt_main414 origin/main', 'codigo_salida': 0,
                      'HEAD': git(os.path.join(W, 'wt_main414'), 'rev-parse', 'HEAD'), 'estado': 'OK'},
 'paso2_descarga': {
   'comando_indicado': 'gh release download base-4.14 --repo jluisplagos/munger-v2 --pattern munger_v2_r1_entrega4.14_cierre_verificacion_entradas.zip --dir /home/user/e_work/dl_base414',
   'resultado_comando_indicado': '4 intentos, codigo 1 en todos: «non-200 OK status code: 403 Forbidden ... GitHub GraphQL is not available from Claude Code sessions; use the REST API». Logs: inventario/log_descarga_intento1..4.txt. Estado del proxy consultado (enabled, sin fallos de relay).',
   'alternativa_usada': 'API REST del mismo asset: gh api repos/jluisplagos/munger-v2/releases/tags/base-4.14 (asset id 750814858, size 1130912246, digest sha256:bb51942c...) y gh api -H "Accept: application/octet-stream" repos/jluisplagos/munger-v2/releases/assets/750814858 > dl_base414/<zip>',
   'codigo_salida_alternativa': 0, 'intentos_alternativa': 1,
   'bytes': os.path.getsize(zipf), 'bytes_esperados': 1130912246,
   'sha256': sha(zipf), 'sha256_esperado': 'bb51942cefb848e409a4828e3faeb70f94aa4d29af39cda6d90cd0a97cb7b93e',
   'estado': 'OK (por API REST; el comando gh release download falla por GraphQL bloqueado)'},
 'paso3_materializar_verificar_A': {
   'comandos': ['python3 -I tools/base_414.py materialize --source /home/user/e_work/dl_base414/munger_v2_r1_entrega4.14_cierre_verificacion_entradas.zip',
                'python3 -I tools/base_414.py verify --report /home/user/e_work/inventario/VERIFICACION_BASE_COMPLETA_LOCAL_414.json'],
   'codigos_salida': {'materialize': 0, 'verify': 0}, 'archivos_recuperados_materialize': 1008,
   'informe_verify': verif if len(json.dumps(verif)) < 4000 else {k: verif[k] for k in verif if not isinstance(verif[k], (list, dict))},
   'log': 'inventario/log_base414.txt',
   'manifiesto_A': {'sha256': sha(os.path.join(W, 'wt_main414', 'munger_v2_r1', 'MANIFIESTO_SHA256.txt')),
                    'esperado_baselines_4_14_json': json.load(open(os.path.join(W, 'wt_main414', 'baselines', '4.14.json')))['manifest_sha256'],
                    'nota': 'verify comprueba el manifiesto aparte (no suma en «verified»; aparecería en missing/changed si fallara).'},
   'archivos_versionados_modificados_en_A': int(git(os.path.join(W, 'wt_main414'), 'status', '--porcelain', '--untracked-files=no').count('\n') + (1 if git(os.path.join(W, 'wt_main414'), 'status', '--porcelain', '--untracked-files=no') else 0)),
   'estado': 'OK'},
 'paso4_worktree_B': {
   'comando': 'git worktree add --detach /home/user/e_work/wt_hito415 059f4f68dca7acf465b5f5b21de2dede84c885ff', 'codigo_salida': 0,
   'HEAD': git(os.path.join(W, 'wt_hito415'), 'rev-parse', 'HEAD'),
   'copia_binarios': {'script': 'scripts/copiar_binarios_a_b.py (shutil.copy2: bytes y marcas de tiempo; SHA-256 y tamaño comprobados tras copiar contra baselines/4.14.json)',
                      'recuento': copia['recuento'], 'existentes_distintos': copia['existentes_distintos'],
                      'detalle': 'inventario/copia_binarios_A_a_B.json'},
   'manifiesto_B': {'primera_linea': open(os.path.join(W, 'wt_hito415', 'munger_v2_r1', 'MANIFIESTO_SHA256.txt'), encoding='utf-8').readline().strip(),
                    'formato': 'línea 1 = cabecera (comentario); resto «huella  ruta» -> se usó tail -n +2 sin adaptación',
                    'comando': 'tail -n +2 MANIFIESTO_SHA256.txt | sha256sum -c --quiet (y una segunda pasada sin --quiet para contar OK)',
                    'codigo_salida': 0, 'entradas': len(logB),
                    'OK': sum(1 for l in logB if l.endswith(': OK')),
                    'FAILED': sum(1 for l in logB if l.endswith(': FAILED')),
                    'ausentes': sum(1 for l in logB if 'FAILED open or read' in l),
                    'presentes_fuera_del_manifiesto': open(os.path.join(INV, 'B_presentes_fuera_manifiesto.txt')).read().split('\n')[:-1],
                    'listas': ['inventario/B_rutas_manifiesto.txt', 'inventario/B_rutas_presentes.txt', 'inventario/B_presentes_fuera_manifiesto.txt', 'inventario/B_manifiesto_ausentes.txt'],
                    'tools_base_414_ejecutado_en_B': False},
   'archivos_versionados_modificados_en_B': 0,
   'estado': 'OK'},
 'paso5_huellas_xlsx_Elis': {
   'ruta_base': ENS, 'A': xl['wt_main414'], 'B': xl['wt_hito415'],
   'A_igual_B': xl['wt_main414'] == xl['wt_hito415'],
   'Elis_v63_evaluada_elis_decisiones': {'esperada': ESP_EV, 'A': ev, 'B': evB, 'coincide_A': ev == ESP_EV, 'coincide_B': evB == ESP_EV},
   'estado': 'OK'},
 'paso6_inventario_fuentes': {
   'detalle': pdfs['inventario'], 'nombres_listados_sin_archivo_o_sin_huella': pdfs['listados_sin_archivo'],
   'todos_coinciden_con_huella_registrada': all(all(v is True for v in e['coincide_huella_registrada'].values()) for e in pdfs['inventario']),
   'motor_A_homonimos_iguales': all(e['motor_A']['igual'] for e in pdfs['inventario'] if 'motor_A' in e),
   'B_PDF_iguales_a_A': True,
   'script': 'scripts/inventario_pdf_elis.py', 'estado': 'OK'},
 'paso7_texto_por_pagina': {
   'indice': 'textos_pdf/INDICE.json',
   'tratamiento_FF_final': 'pdftotext termina cada página con \\f; el segmento vacío tras el último \\f se descartó (ocurrió en los 14 documentos) y no cuenta como página.',
   'texto_completo_intermedio': 'textos_pdf/_completos/<slug>.txt (salida directa de pdftotext -layout)',
   'avisos_pdftotext': 'código 0 en los 14; algunos emiten «Syntax Warning» de fuentes (registrados en paso6 detalle.pdftotext_stderr, truncados).',
   'resumen': [{k: d[k] for k in ('slug', 'paginas_pdfinfo', 'paginas_extraidas', 'paginas_coinciden', 'paginas_vacias')} for d in indice['documentos']],
   'estado': 'OK'},
}
json.dump(out, open(os.path.join(INV, 'preparacion.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('ok')
