import sys, openpyxl
a=openpyxl.load_workbook(sys.argv[1]); b=openpyxl.load_workbook(sys.argv[2])
sheets=sys.argv[3].split(',') if len(sys.argv)>3 else a.sheetnames
for sh in sheets:
    if sh not in b.sheetnames: print('falta',sh); continue
    A=a[sh]; B=b[sh]
    mr=max(A.max_row,B.max_row); mc=max(A.max_column,B.max_column)
    n=0
    for r in range(1,mr+1):
        for c in range(1,mc+1):
            x=A.cell(r,c).value; y=B.cell(r,c).value
            if x!=y:
                fx=isinstance(x,str) and x.startswith('='); fy=isinstance(y,str) and y.startswith('=')
                n+=1
                if (isinstance(x,(int,float)) or isinstance(y,(int,float)) or fx or fy) and n<=40:
                    print(f'{sh}!{A.cell(r,c).coordinate}: {repr(x)[:90]} -> {repr(y)[:90]}')
    print(sh,'celdas distintas:',n)
