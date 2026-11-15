import sys, openpyxl
p=sys.argv[1]; sh=sys.argv[2]; rng=sys.argv[3]
wb=openpyxl.load_workbook(p,data_only=False,read_only=False)
wv=openpyxl.load_workbook(p,data_only=True,read_only=False)
ws=wb[sh]; wv_=wv[sh]
for row in ws[rng]:
    for c in row:
        if c.value is not None:
            v=wv_[c.coordinate].value
            print(f"{c.coordinate}\t{repr(c.value)[:300]}\t=> {repr(v)[:80]}")
