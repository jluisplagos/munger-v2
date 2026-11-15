# Reproducibilidad de C48 de Elis · reconstrucción en carpetas limpias (4.15)

Generado por `scripts/prueba_reconstruccion_c48_4_15.py`. Cada caso reconstruye el expediente desde sus entradas declaradas con `scripts/reconstruir_expediente.py` (LibreOffice en secuencia) y lo compara con el expediente de referencia. La fecha de revisión del Control maestro (L5) es un sello de ejecución y se lista aparte.

| Caso | Termina | C48 (referencia → reconstruido) | Precio de Sí (referencia → reconstruido) | Diferencia | Diferencias de datos, fórmulas o resultados | Otras diferencias | Entradas migradas distintas (la vía generativa no las reproduce) |
|---|---|---|---|---|---|---|---|
| 1 · Elis 4.14, entradas declaradas | completo | 108 → 108 | 7,3020553231 → 7,3020553231 | 0,0000000000 | ninguna | ninguna | Análisis!C48 (libro 108 · fase1_v63 82.933) |
| 2 · Elis 4.14, sin valores migrados del FCF base | completo | 108 → 82.933 | 7,3020553231 → 8,9801824507 | 1,6781271276 | entradas distintas: Análisis!C48; 2942 celdas recalculadas distintas (primeras: Análisis!B108, Análisis!B109, Análisis!B110) | evidencia documental: Control maestro!G45, Control maestro!G46, Control maestro!H45, Control maestro!H46, Control maestro!J45, Control maestro!J46 | ninguna |
| 3 · CAMBIO 4.15 (C48 con su cálculo), construir | completo | 108 → 108 | 7,3020553231 → 7,3020553231 | 0,0000000000 | ninguna | fecha de ejecución: Análisis!D4, Control maestro!F4, Control maestro!G20; evidencia documental: Control maestro!G45, Control maestro!H45, Control maestro!J184, Control maestro!J45 | ninguna |
| 4 · CAMBIO 4.15, construir, sin valores migrados | completo | 108 → 108 | 7,3020553231 → 7,3020553231 | 0,0000000000 | ninguna | fecha de ejecución: Análisis!D4, Control maestro!F4, Control maestro!G20; evidencia documental: Control maestro!G45, Control maestro!G46, Control maestro!H45, Control maestro!H46, Control maestro!J184, Control maestro!J185, Control maestro!J45, Control maestro!J46 | ninguna |
| 5 · Viscofan 4.14, entradas declaradas (contraste) | completo | 8.294 → 8.294 | 39,7981935351 → 39,7981935351 | 0,0000000000 | ninguna | ninguna | ninguna |
| 6 · Vidrala 4.14, entradas declaradas (contraste) | completo | — → — | 56,0020051682 → 56,0020051682 | 0,0000000000 | ninguna | ninguna | Análisis!C50 (libro 0 · fase1_v63 None) |
| 7 · Viscofan 4.14, sin valores migrados del FCF base | completo | 8.294 → 8.294 | 39,7981935351 → 39,7981935351 | 0,0000000000 | ninguna | evidencia documental: Control maestro!G43, Control maestro!H43, Control maestro!J182, Control maestro!J43 | ninguna |
| 8 · Vidrala 4.14, sin valores migrados del FCF base | completo | — → — | 56,0020051682 → 56,0020051682 | 0,0000000000 | entradas distintas: Análisis!C50; 6 celdas recalculadas distintas (primeras: Análisis!C50, Análisis!D50, Análisis!D51) | evidencia documental: Control maestro!G46, Control maestro!J185, Control maestro!J46 | ninguna |

Detalle de cada caso en su JSON (pasos, salidas, diferencias de fase1_v63.json, libros y valores recalculados).
