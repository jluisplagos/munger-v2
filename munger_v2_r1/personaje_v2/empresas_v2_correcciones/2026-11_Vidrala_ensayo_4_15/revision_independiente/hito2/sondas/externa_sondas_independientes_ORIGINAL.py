"""Sondas externas. Fixture SINTÉTICO: no acredita cifras reales."""
import argparse, copy, hashlib, json, pathlib, shutil, sys
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--root',type=pathlib.Path,required=True)
parser.add_argument('--output',type=pathlib.Path,required=True)
args=parser.parse_args()
root=args.root.resolve()
test=root/'personaje_v2/pruebas/test_verificacion_entradas_415.py'
source=test.read_text();prefix=source.split('K = "Historia!F6"')[0]
ns={'__file__':str(test),'__name__':'fixture_externo'}
sys.argv=['sonda_externa']
exec(compile(prefix,str(test),'exec'),ns)
VE=ns['VE'];con=ns['con'];ent=ns['ent'];K='Historia!F6';rows=[]
def record(name,r):
 rows.append({'case':name,'apto_por_entradas':r['apto_por_entradas'],'errors':r['errores'][:2],'discrepancies':r['discrepancias'][:2],'pending':r['pendientes'][:2]})
try:
 record('control_positivo_sintetico',con())
 record('pagina_999999',con(lambda g:ent(g,K)['fuente'].update(pagina='999999')))
 record('fuente_local_ausente_sin_sha',con(lambda g:ent(g,K)['fuente'].update(archivo='fuentes_sinteticas/NO_EXISTE.txt',sha256=None)))
 direct=[{'citation':'Amortización: 150','value':149.5},{'citation':'Partida: 0','value':0.49},{'citation':'Acciones: 45479','value':45479.209},{'citation':'Importe: -149.5','value':149.5},{'citation':'Importe: 149.5','value':-149.5},{'citation':'Importe: (149.5)','value':149.5}]
 for item in direct:item['accepted']=bool(VE._cita_contiene(item['citation'],item['value']))
 # La página realmente conservada contiene ahora el signo negativo, con SHA y vínculo nuevos.
 original=copy.deepcopy(ns['REG']);f=ent(original,K)['fuente'];vf=f['valor_fuente'];index=int(f['pagina'])-1
 original_page=ns['paginas'][index]
 negative=original_page.replace(f'{abs(vf):.3f}',f'-{abs(vf):.3f}')
 if negative==original_page:raise RuntimeError('No se pudo construir el contraejemplo de signo')
 ns['paginas'][index]=negative;ns['escribir_fuente']()
 reg=copy.deepcopy(original)
 for e in reg['entradas']:
  if (e.get('fuente') or {}).get('archivo')=='fuentes_sinteticas/fuente.txt':e['fuente']['sha256']='__actual__'
 ent(reg,K)['fuente']['cita']=negative
 ns['sellar_todo'](reg)
 pathlib.Path(ns['c'],VE.REGISTRO).write_text(json.dumps(reg,ensure_ascii=False),encoding='utf-8')
 r=VE.comprobar(ns['c']);record('pagina_y_cita_negativas_con_valor_fuente_positivo',r)
 sign_case={'cell':K,'model_value':ent(reg,K)['valor_modelo'],'declared_source_value':vf,'declared_sign':ent(reg,K)['fuente']['signo'],'declared_treatment':ent(reg,K)['fuente']['tratamiento'],'actual_page_and_citation':negative,'apto_por_entradas':r['apto_por_entradas'],'checked_cell':K in r['comprobadas']}
 result={'fixture':'SINTÉTICO, no datos reales','cases':rows,'numeric_citation_probes':direct,'sign_case':sign_case}
 args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2))
 print(json.dumps(result,ensure_ascii=False,indent=2))
finally:
 shutil.rmtree(ns['TMP'])
