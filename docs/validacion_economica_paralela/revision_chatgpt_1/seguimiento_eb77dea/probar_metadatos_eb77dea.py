import csv,json,subprocess,sys,tempfile
from pathlib import Path
root=Path('/workspace/work/revision414_runtime/munger_v2_r1')
a=Path('/workspace/work/revision_f1_recibida/autor_eb77dea/docs/validacion_economica_paralela/frente_E_F1_elis')
base=list(csv.DictReader((a/'datos/cifras_fuente.csv').open(encoding='utf-8'),delimiter=';'))
rows=[]
with tempfile.TemporaryDirectory() as d:
 d=Path(d)
 for label,key,field,value in [('unidad_porcentaje','CREC_ORG_2025','unidad','mm EUR'),('perimetro_ventas','IS_VENTAS_2025','perimetro','segmento Francia')]:
  data=[dict(r) for r in base];row=next(r for r in data if r['id']==key);old=row[field];row[field]=value
  with (d/'c.csv').open('w',encoding='utf-8',newline='') as f:
   w=csv.DictWriter(f,fieldnames=list(data[0]),delimiter=';');w.writeheader();w.writerows(data)
  p=subprocess.run([sys.executable,'-I',str(a/'scripts/verificar_cifras.py'),'--raiz',str(root),'--datos',str(d/'c.csv'),'--fuentes',str(a/'datos/fuentes.json'),'--salida',str(d/'v.json')],capture_output=True,text=True)
  summary=json.loads((d/'v.json').read_text())['resumen'] if (d/'v.json').exists() else None
  rows.append({'case':label,'cell_id':key,'field':field,'original':old,'changed':value,'exit_code':p.returncode,'summary':summary})
Path('/workspace/work/revision_f1_recibida/resultados_chatgpt/metadatos_eb77dea.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
print(json.dumps(rows,ensure_ascii=False))
