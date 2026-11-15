from pathlib import Path
import json,sys,shutil,hashlib
script=Path('/workspace/work/revision414_runtime/munger_v2_r1/personaje_v2/pruebas/test_verificacion_entradas_414.py')
setup=script.read_text().split('\nr = con()\n')[0];ns={'__file__':str(script),'__name__':'probe_fixture'};sys.argv=[str(script)]
exec(compile(setup,str(script),'exec'),ns)
con,ent,reg=ns['con'],ns['ent'],ns['REG'];out=[]
r=con();assert r['apto_por_entradas'];out.append({'case':'control_positive','apto':r['apto_por_entradas']})
k=ns['k_dato'];r=con(lambda g:ent(g,k)['fuente'].update(pagina='999999'))
out.append({'case':'page_does_not_exist','cell':k,'apto':r['apto_por_entradas'],'errors':r['errores'],'discrepancies':r['discrepancias']})
r=con(lambda g:ent(g,k)['fuente'].update(archivo='fuentes_sinteticas/NO_EXISTE.txt',sha256=None))
out.append({'case':'declared_local_source_absent_and_no_hash','cell':k,'apto':r['apto_por_entradas'],'errors':r['errores'],'discrepancies':r['discrepancias']})
e=ent(reg,'Análisis!C55');f=e['fuente'];old=f['cita'];new='Partida sintética de Análisis!C55: '+str(round(f['valor_fuente']))
p=Path(ns['c'])/'fuentes_sinteticas/fuente.txt';p.write_text(p.read_text().replace(old,new));h=hashlib.sha256(p.read_bytes()).hexdigest()
def rounded(g):ent(g,'Análisis!C55')['fuente'].update(cita=new,sha256=h)
r=con(rounded);out.append({'case':'rounded_citation_accepted_as_exact_value','declared_value':f['valor_fuente'],'actual_quote':new,'apto':r['apto_por_entradas'],'errors':r['errores'],'discrepancies':r['discrepancias']})
Path('/workspace/work/revision414_sondas_entradas.json').write_text(json.dumps(out,ensure_ascii=False,indent=2));print(json.dumps(out,ensure_ascii=False,indent=2));shutil.rmtree(ns['TMP'])
