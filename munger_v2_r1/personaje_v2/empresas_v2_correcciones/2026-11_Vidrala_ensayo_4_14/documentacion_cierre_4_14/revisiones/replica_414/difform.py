import openpyxl
R='/home/claude/trabajo_4_14/trabajo/munger_v2_r1/personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_14/'
P={'Viscofan':R+'viscofan_decisiones/Viscofan/Viscofan_v63_evaluada.xlsx','Vidrala':R+'vidrala_decisiones/Vidrala/Vidrala_v63_evaluada.xlsx','Elis':R+'elis_decisiones/Elis/Elis_v63_evaluada.xlsx'}
W={k:openpyxl.load_workbook(v) for k,v in P.items()}
for k,w in W.items(): print(k,[ws.title for ws in w])
regions=[('Motor','A6:DY8'),('Motor','A56:DY56'),('Diagnóstico V6','C5:C16'),('Historia','C43:C70'),('Historia','C28:L38'),('Análisis','B67:D90'),('Análisis','C52'),('Configuración V6.4','B1:K156')]
for sh,rg in regions:
    base=W['Viscofan']
    for k in ['Vidrala','Elis']:
        w=W[k]
        if sh not in w.sheetnames: print(k,'falta hoja',sh); continue
        n=0
        for row in base[sh][rg]:
            for c in row:
                a=c.value; b=w[sh][c.coordinate].value
                fa=isinstance(a,str) and a.startswith('='); fb=isinstance(b,str) and b.startswith('=')
                if (fa or fb) and a!=b:
                    n+=1
                    if n<=12: print(f'  {k} {sh}!{c.coordinate}: VISC={str(a)[:160]} | {k}={str(b)[:160]}')
        print(k,sh,rg,'difs de fórmula:',n)
