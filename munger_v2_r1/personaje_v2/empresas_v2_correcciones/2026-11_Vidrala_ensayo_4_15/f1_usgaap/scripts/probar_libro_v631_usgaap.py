#!/usr/bin/env python3
"""F1 · US GAAP sobre el libro V6.3.1 F1 REAL, recalculado con LibreOffice: el libro tal cual (plantilla eaece01a…, sin tocar) calcula los
casos de US GAAP que no necesitan retirar nada del circulante, y la capa motor_a_f1.py es su oráculo.

Uso (desde cualquier carpeta): flock /home/user/e_work/libreoffice.lock python3 -I probar_libro_v631_usgaap.py DESTINO [SALIDA.json]
  DESTINO: carpeta nueva fuera del repositorio.
Base: el ejemplo «Empresa X» de la V6.3 (empresa inventada), con sus entradas trasladadas a la V6.3.1 y convertido en una empresa US GAAP:
Control maestro L4 = «US GAAP»; sin intereses ni principal de arrendamientos en financiación (C48 = C49 = 0, filas 16 y 17 a cero); C46,
C47 y C50 iguales a las medias de la Historia (para que K3a no dependa de redondeos). La fila 23 del ejemplo se declara pasivo operativo.
Casos:
  L1 · operativos con la amortización de su derecho de uso DENTRO de la fila 8 (30 % de la D&A) y PPA 10 %; perímetro A2: la fila 86 del
       libro lleva esa amortización; libro = capa (f a 10⁻¹², ancla a 10⁻⁹, 33 flujos); nada bloquea → utilizable.
  L2 · lo mismo con A0: F1-US-DA bloquea (alquiler dos veces) y la f del libro A0 es mayor en (amortización + PPA) ÷ ventas medias.
  L3 · operativos + financieros (derecho de uso financiero 20 % de la D&A con su principal en C49): la fila 86 lleva la suma (50 %).
  L4 · tramos no publicados (hipótesis D-US1) con A2: el libro tal cual lo calcula; conclusión condicionada.
  L5 · la variación del pasivo declarada dentro de la fila 14: el libro no la retira → F1-LIBRO bloquea; la réplica sigue conforme.
  L6 · motor B (Análisis C62 = «No · financiación cambia mucho»): el puente del libro resta la fila 23 entera (Diagnóstico V6 C16);
       F1-US-PUENTE bloquea por el pasivo operativo; con la fila 23 a cero y 0 declarado, no bloquea.
"""
import hashlib
import json
import os
import shutil
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
PV = os.path.abspath(os.path.join(AQUI, "..", "..", "..", ".."))
RAIZ = os.path.dirname(PV)
sys.path.insert(0, os.path.join(RAIZ, "v6", "v631_f1", "scripts"))
sys.path.insert(0, os.path.join(PV, "scripts"))
sys.dont_write_bytecode = True
import probar_v631_f1 as PB  # noqa: E402  (preparar, recalc, _escribir_libro; no ejecuta nada al importarse)
import motor_a_f1 as M  # noqa: E402
import f1_libro_v631 as V631  # noqa: E402

COLS = "CDEFGHIJKL"
DOC, FUENTE = "10-K sintético", "fuente_sintetica_us.txt"
REG = {"fecha": "2026-11-18", "persona": "prueba del libro V6.3.1 con US GAAP (no es una decisión)", "motivo": "caso de prueba"}
RES = []


def chk(nombre, ok, detalle=""):
    RES.append({"prueba": nombre, "ok": bool(ok), "detalle": detalle})
    print(("PASA " if ok else "FALLA") + f" · {nombre}" + (f" · {detalle}" if detalle else ""))


def serie(vals):
    return {str(y): {"valor_fuente": v, "signo": 1, "tratamiento": "ninguno", "documento": DOC, "pagina": 1, "literal": repr(v)} for y, v in vals.items()}


def main(dest, salida=None):
    from openpyxl import load_workbook
    if os.path.exists(dest):
        raise SystemExit(f"{dest} ya existe: las pruebas escriben en una carpeta nueva")
    if os.path.commonpath([os.path.abspath(dest), RAIZ]) == RAIZ:
        raise SystemExit("DESTINO va fuera del repositorio")
    os.makedirs(dest)
    chk("la plantilla V6.3.1 F1 es la entregada (eaece01a…): no se toca", PB.sha(PB.PLANTILLA).startswith("eaece01a7d6a1d86"), PB.sha(PB.PLANTILLA)[:16])
    ex = PB.EJEMPLOS[0]
    h = load_workbook(ex, data_only=True)["Historia"]
    anios = [int(h[f"{c}5"].value) for c in COLS]
    fila = lambda f: {y: h[f"{c}{f}"].value for c, y in zip(COLS, anios)}  # noqa: E731
    da, cfo, capex, sbc, f23 = fila(8), fila(11), fila(12), fila(18), fila(23)
    w3, w5 = anios[-3:], anios[-5:]
    m3 = lambda s: round(sum(s[y] for y in w3) / 3, 9)  # noqa: E731
    a8 = {y: round(0.30 * v, 6) for y, v in da.items()}
    ppa = {y: round(0.10 * v, 6) for y, v in da.items()}
    rfin = {y: round(0.20 * v, 6) for y, v in da.items()}
    us = {"Control maestro!L4": "US GAAP", "Análisis!C48": 0, "Análisis!C49": 0, "Análisis!C46": m3(cfo), "Análisis!C47": m3(capex), "Análisis!C50": m3(sbc)}
    us.update({f"Historia!{c}{f}": 0 for c in COLS for f in (16, 17)})
    base = os.path.join(dest, "EmpresaX_US_entradas.xlsx")
    PB.preparar(ex, PB.PLANTILLA, base, us)
    P, Lc = {y: round(0.02 * capex[y], 6) + 1 for y in w3}, {y: round(0.02 * capex[y], 6) + 1.1 for y in w3}

    def decl(per, ub_am="fila_8", ub_pas="fuera_de_las_filas_8_y_14", con_a8=True, fin=False, ajuste=None, pasivo=None):
        ev = {"documento": DOC, "pagina": 1}
        def ub(clave, u, cita):
            return {"ubicacion": u, "documento": DOC, "pagina": 2} if u == "no_publicada" else dict(ev, ubicacion=u, cita=cita)
        d = {"norma_contable": {"valor": "US_GAAP", "registro": REG}, "perimetro_reinversion": {"valor": per, "registro": REG},
             "perimetro_margen": {"valor": "EBIT_NIIF16_PPA_constante", "registro": REG}, "perimetro_palancas_s2c": {"valor": per, "registro": REG},
             "perimetro_roic": {"valor": per, "registro": REG},
             "clasificacion_compras": {"valor": "crecimiento_por_hipotesis", "registro": REG, "fundamento": "hipótesis declarada (prueba)"},
             "transicion": {"conocida": False, "tratamiento": None, "registro": REG},
             "arrendamientos_us_gaap": {"registro": REG,
                                        "operativos": dict(ev, cita="Operating lease cost", existen=True,
                                                           amortizacion_rou=ub("amortizacion_rou", ub_am, "Depreciation and amortization, including amortization of operating lease right-of-use assets"
                                                                               if ub_am == "fila_8" else "Non-cash lease expense"),
                                                           variacion_pasivo=ub("variacion_pasivo", ub_pas, "Operating lease liabilities" if ub_pas == "fila_14" else "Other operating activities, net")),
                                        "financieros": dict(ev, cita="Finance lease cost" if fin else "The Company has no finance leases", existen=fin)},
             "series": {"da_ppa": serie(ppa), "pagos_arr_operativo": serie(P), "coste_arr_operativo": serie(Lc),
                        "pasivo_arr_operativo": serie({anios[-1]: f23[anios[-1]] if pasivo is None else pasivo})}}
        if con_a8 and ub_am == "fila_8":
            d["series"]["da_rou_operativo"] = serie(a8)
        if fin:
            d["series"]["da_rou"] = serie(rfin)
            d["series"]["pagos_arr_financiero_principal"] = serie({y: rfin[y] for y in w3})
        if ajuste is not None:
            d["series"]["circulante_arr_operativo"] = serie({y: ajuste for y in w5})
        lits = sorted({str(e["literal"]) for s_ in d["series"].values() for e in s_.values()})
        txt = ("[PDF PAGE 1]\nNotas sintéticas: " + " ".join(lits) + "\nOperating lease cost\nFinance lease cost\nThe Company has no finance leases\n"
               "Depreciation and amortization, including amortization of operating lease right-of-use assets\nNon-cash lease expense\nOperating lease liabilities\n"
               "Other operating activities, net\n[PDF PAGE 2]\nCONSOLIDATED STATEMENTS OF CASH FLOWS\nNet income\nDepreciation and amortization\n"
               "Changes in working capital\nNet cash provided by operating activities\n[PDF PAGE 3]\n")
        d["_fuente"] = txt
        d["fuentes_series"] = {DOC: {"archivo": FUENTE, "sha256": hashlib.sha256(txt.encode("utf-8")).hexdigest()}}
        return d

    def libro(nombre, d, origen=base, despues=None):
        d = dict(d)
        txt = d.pop("_fuente")
        c = os.path.join(dest, nombre)
        os.makedirs(c)
        open(os.path.join(c, FUENTE), "w", encoding="utf-8").write(txt)
        dp = os.path.join(c, "motor_a_f1.json")
        json.dump(d, open(dp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        b = os.path.join(dest, f"{nombre}.xlsx")
        V631.aplicar(origen, b, dp)
        if despues:
            PB._escribir_libro(b, b + ".tmp.xlsx", despues)
            os.replace(b + ".tmp.xlsx", b)
        rec = PB.recalc(b, dest)
        return rec, d, c

    def bloquean(r):
        return sorted({g["id"] for g in r["guardas"] if g["salta"] and g["severidad"] == "BLOQUEA"})

    def salta(r, gid):
        return any(g["salta"] for g in r["guardas"] if g["id"] == gid)

    det = {}
    # ---------------------------------------------------------------- L1 · amortización operativa dentro de la fila 8, A2
    rec, d, c = libro("L1_A2", decl("A2_propio"))
    wb = load_workbook(rec, data_only=True)
    hh, mo = wb["Historia"], wb["Motor"]
    r = M.evaluar(M.leer_libro(rec), d, carpeta=c)
    cd = r["calculo_perimetro_declarado"]
    chk("L1 · el libro recalculado es US GAAP (L4) y lleva A2 con la amortización operativa en la fila 86 (30 % de la D&A) y la PPA en la 87; Motor V05 OK",
        wb["Control maestro"]["L4"].value == "US GAAP" and hh["C89"].value == "A2_propio" and mo["D205"].value == "OK"
        and all(abs(hh[f"{c_}86"].value - a8[y]) < 1e-9 and abs(hh[f"{c_}88"].value - (da[y] - a8[y] - ppa[y])) < 1e-9 for c_, y in zip(COLS, anios)),
        f"V05 {mo['D205'].value!r} · L86 {hh['L86'].value!r}")
    chk("L1 · libro = capa: f (10⁻¹²), ancla de S2C (10⁻⁹) y 33 flujos; F1-LIBRO, F1-REPLICA y F1-NORMA no saltan",
        abs(cd["f"] - hh["C58"].value) <= 1e-12 and abs(cd["ancla_s2c_E4"] - hh["C53"].value) <= 1e-9 and not salta(r, "F1-LIBRO") and not salta(r, "F1-REPLICA")
        and not salta(r, "F1-NORMA") and r["libro_v631_f1"]["flujos_contrastados"] == 33, f"f {hh['C58'].value!r} · C53 {hh['C53'].value!r} · {r['libro_v631_f1']['motivos'][:2]}")
    chk("L1 · nada bloquea: utilizable para una conclusión (sin hipótesis); K3 conforme, alquiler una vez", bloquean(r) == [] and r["utilizable_para_conclusion"]
        and r["K3"]["conforme"] is True and r["K3"]["K3b_alquiler_contado"] == "una vez" and "condicionada" not in r, str(bloquean(r)))
    det["L1"] = {"C58": hh["C58"].value, "C53": hh["C53"].value, "C74": hh["C74"].value, "bloquean": bloquean(r)}
    # ---------------------------------------------------------------- L2 · lo mismo con A0
    rec0, d0, c0 = libro("L2_A0", decl("A0_total"))
    h0 = load_workbook(rec0, data_only=True)["Historia"]
    r0 = M.evaluar(M.leer_libro(rec0), d0, carpeta=c0)
    m_a8, m_ppa = sum(a8[y] for y in w3) / 3, sum(ppa[y] for y in w3) / 3
    chk("L2 · con A0 el libro trata esa amortización como reposición: F1-US-DA bloquea (alquiler dos veces) y F1-2i por la PPA",
        "F1-US-DA" in bloquean(r0) and "F1-2i" in bloquean(r0) and r0["K3"]["K3b_por_clase"] == {"operativos": "dos veces"}, str(bloquean(r0)))
    chk("L2 · identidad con los valores del libro: f_A2 = f_A0 − (amortización operativa + PPA) media ÷ ventas medias",
        abs(hh["C58"].value - (h0["C58"].value - (m_a8 + m_ppa) / h0["C74"].value)) <= 1e-12, f"f_A0 {h0['C58'].value!r} · f_A2 {hh['C58'].value!r}")
    # ---------------------------------------------------------------- L3 · operativos + financieros
    fin_c49 = round(sum(rfin[y] for y in w3) / 3, 9)
    base_fin = os.path.join(dest, "EmpresaX_US_fin_entradas.xlsx")
    PB.preparar(ex, PB.PLANTILLA, base_fin, dict(us, **{"Análisis!C49": fin_c49}, **{f"Historia!{c_}17": rfin[y] for c_, y in zip(COLS, anios)}))
    rec3, d3, c3 = libro("L3_fin_A2", decl("A2_propio", fin=True), origen=base_fin)
    h3 = load_workbook(rec3, data_only=True)["Historia"]
    r3 = M.evaluar(M.leer_libro(rec3), d3, carpeta=c3)
    chk("L3 · operativos + financieros: la fila 86 lleva la suma (30 % + 20 % de la D&A); libro = capa; nada bloquea; una vez en cada clase",
        all(abs(h3[f"{c_}86"].value - (a8[y] + rfin[y])) < 1e-9 for c_, y in zip(COLS, anios)) and abs(r3["calculo_perimetro_declarado"]["f"] - h3["C58"].value) <= 1e-12
        and bloquean(r3) == [] and r3["K3"]["K3b_por_clase"] == {"operativos": "una vez", "financieros": "una vez"}, f"{bloquean(r3)} · {r3['K3'].get('K3b_por_clase')}")
    det["L3"] = {"C58": h3["C58"].value, "C53": h3["C53"].value, "bloquean": bloquean(r3)}
    # ---------------------------------------------------------------- L4 · hipótesis D-US1
    rec4, d4, c4 = libro("L4_DUS1_A2", decl("A2_propio", ub_am="no_publicada", ub_pas="no_publicada"))
    h4 = load_workbook(rec4, data_only=True)["Historia"]
    r4 = M.evaluar(M.leer_libro(rec4), d4, carpeta=c4)
    chk("L4 · tramos no publicados (hipótesis D-US1) con A2: el libro V6.3.1 tal cual lo calcula (fila 86 a cero, libro = capa); nada bloquea; conclusión CONDICIONADA con su cota",
        all(h4[f"{c_}86"].value == 0 for c_ in COLS) and abs(r4["calculo_perimetro_declarado"]["f"] - h4["C58"].value) <= 1e-12 and bloquean(r4) == []
        and "CONDICIONADA" in r4["rotulo"] and r4["condicionada"]["cota"] is not None and r4["libro_v631_f1"]["motivos"] == [], f"{bloquean(r4)} · {r4['rotulo'][:90]}")
    det["L4"] = {"C58": h4["C58"].value, "cota": r4["condicionada"]["cota"]}
    # ---------------------------------------------------------------- L5 · la variación del pasivo dentro de la fila 14
    rec5, d5, c5 = libro("L5_fila14_A2", decl("A2_propio", ub_am="fuera_de_las_filas_8_y_14", ub_pas="fila_14", ajuste=2.5),
                         despues={f"Historia!{c_}14": h[f"{c_}14"].value + 2.5 for c_ in "HIJKL"})
    h5 = load_workbook(rec5, data_only=True)["Historia"]
    r5 = M.evaluar(M.leer_libro(rec5), d5, carpeta=c5)
    s_w = h5["C74"].value
    chk("L5 · variación del pasivo dentro de la fila 14 (2,5 al año): el libro no la retira → F1-LIBRO es lo único que bloquea; la réplica del libro sigue conforme",
        bloquean(r5) == ["F1-LIBRO"] and not salta(r5, "F1-REPLICA") and "retirada del circulante" in next(g["detalle"] for g in r5["guardas"] if g["id"] == "F1-LIBRO"), str(bloquean(r5)))
    chk("L5 · la f de la capa es la del libro + 2,5 ÷ ventas medias (el libro sobrevaloraría el flujo en esa parte del alquiler)",
        abs(r5["calculo_perimetro_declarado"]["f"] - (h5["C58"].value + 2.5 / s_w)) <= 1e-12, f"capa {r5['calculo_perimetro_declarado']['f']!r} · libro {h5['C58'].value!r}")
    # ---------------------------------------------------------------- L6 · motor B: el puente
    recb, db, cb = libro("L6_motor_B", decl("A2_propio", ub_am="fuera_de_las_filas_8_y_14"), despues={"Análisis!C62": "No · financiación cambia mucho"})
    wbb = load_workbook(recb, data_only=True)
    hb, dgb = wbb["Historia"], wbb["Diagnóstico V6"]
    rb = M.evaluar(M.leer_libro(recb), db, carpeta=cb)
    c65_66 = dgb["C16"].value - hb["C64"].value
    chk("L6 · motor B en el libro real: el puente (Diagnóstico V6 C16) resta Historia C64 = fila 22 + fila 23, con el pasivo operativo dentro",
        dgb["C5"].value == "B" and abs(hb["C64"].value - (hb["L22"].value + hb["L23"].value)) < 1e-9 and hb["L23"].value > 0, f"C64 {hb['C64'].value!r} · C16 {dgb['C16'].value!r}")
    pu = rb["us_gaap"]["puente_de_deuda"]
    chk("L6 · F1 evalúa solo el puente con el motor B: F1-US-PUENTE bloquea (límite declarado); la deuda coherente es la fila 22 y el puente coherente sería C16 − fila 23",
        rb["aplica"] is True and bloquean(rb) == ["F1-US-PUENTE"] and abs(pu["deuda_del_puente_coherente"] - hb["L22"].value) < 1e-9
        and abs((pu["deuda_del_puente_coherente"] + c65_66) - (dgb["C16"].value - hb["L23"].value)) < 1e-9, f"{bloquean(rb)} · coherente {pu['deuda_del_puente_coherente']!r}")
    recb0, db0, cb0 = libro("L6_motor_B_sin_pasivo_operativo", decl("A2_propio", ub_am="fuera_de_las_filas_8_y_14", pasivo=0),
                            despues={"Análisis!C62": "No · financiación cambia mucho", **{f"Historia!{c_}23": 0 for c_ in COLS}})
    rb0 = M.evaluar(M.leer_libro(recb0), db0, carpeta=cb0)
    chk("L6 · con la fila 23 sin pasivo operativo (0 en el libro y 0 declarado) el motor B no bloquea por F1: utilizable", bloquean(rb0) == [] and rb0["utilizable_para_conclusion"],
        str(bloquean(rb0)))
    det["L6"] = {"puente": pu}
    shutil.rmtree(os.path.join(dest, "_perfil_lo"), ignore_errors=True)
    ok = all(x["ok"] for x in RES)
    linea = f"{sum(x['ok'] for x in RES)}/{len(RES)} comprobaciones de F1 · US GAAP sobre el libro V6.3.1 {'PASAN' if ok else 'FALLAN'}"
    print(linea)
    if salida:
        json.dump({"prueba": "libro V6.3.1 F1 con US GAAP (LibreOffice)", "plantilla_sha256": PB.sha(PB.PLANTILLA), "resultado": "PASA" if ok else "FALLA",
                   "total": len(RES), "pasan": sum(x["ok"] for x in RES), "comprobaciones": RES, "detalle": det, "linea": linea},
                  open(salida, "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    return 0 if ok else 1


if __name__ == "__main__":
    if len(sys.argv) not in (2, 3):
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1], sys.argv[2] if len(sys.argv) == 3 else None))
