#!/usr/bin/env python3
"""Recalcula a mano f = Historia!C58 para C52 alternativos, con las cachés del libro de referencia (sin LibreOffice):
f = (X − C70) / ventas medias, con C70 = Análisis!C52 y X despejado de la base (C79 = X − C70... ver fórmulas). Solo lectura."""
import openpyxl
L = "/home/claude/auditoria_4_9/munger_v2_r1/personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_6_1/Vidrala/Vidrala_v63_evaluada.xlsx"
wv = openpyxl.load_workbook(L, data_only=True)
f0, c52, ventas = wv["Diagnóstico V6"]["C12"].value, wv["Análisis"]["C52"].value, wv["Historia"]["C74"].value
X = f0 * ventas + c52
for nombre, fcf in (("base", c52), ("H_C48_int_arrend (C48 = 2,254)", c52 - 2.254), ("H_C48_doble_computo (C48 = 21,74)", c52 - 21.74)):
    f = (X - fcf) / ventas
    print(f"{nombre:36s} FCF {fcf:8.3f} · f {100*f:6.2f} % · control de rango: {'⚠ REVISAR' if (f < -0.02 or f > 0.05) else '✓ PASA'}")
