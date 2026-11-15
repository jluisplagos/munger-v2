# Plantilla V6.4.1 experimental · compatibilidad y efecto del perímetro (encargo 4.13 §7)

**Qué es.** Recálculos con LibreOffice sobre copias, con las entradas del libro evaluado de Viscofan de la 4.12. No cambia ningún expediente.

## 1. Compatibilidad

- Experimental con el perímetro vacío frente al libro V6.4: **0** celdas distintas (fuera de las celdas nuevas o reetiquetadas).
- Experimental con «Caja» escrito de forma explícita frente al libro V6.4: **0** celdas distintas.
- Modo heredado V6.4.1 frente a heredado V6.4: **0** celdas distintas.
- Celdas excluidas por ser texto que repite el resumen B9 (que en la V6.4.1 dice el perímetro), con su comprobación:
  - experimental_caja · Conciliación B!A3: ¿solo añade el perímetro? **sí** · V6.4 «al a las ventas · f 1.0739 · f_fija 1.0000 · cartera: legado» · V6.4.1 «ional a las ventas · f 1.0739 · f_fija 1.0000 · cartera: legado · perímetro Caja»
  - experimental_caja · Panel!C18: ¿solo añade el perímetro? **sí** · V6.4 «al a las ventas · f 1.0739 · f_fija 1.0000 · cartera: legado» · V6.4.1 «ional a las ventas · f 1.0739 · f_fija 1.0000 · cartera: legado · perímetro Caja»
  - experimental_caja_explicita · Conciliación B!A3: ¿solo añade el perímetro? **sí** · V6.4 «al a las ventas · f 1.0739 · f_fija 1.0000 · cartera: legado» · V6.4.1 «ional a las ventas · f 1.0739 · f_fija 1.0000 · cartera: legado · perímetro Caja»
  - experimental_caja_explicita · Panel!C18: ¿solo añade el perímetro? **sí** · V6.4 «al a las ventas · f 1.0739 · f_fija 1.0000 · cartera: legado» · V6.4.1 «ional a las ventas · f 1.0739 · f_fija 1.0000 · cartera: legado · perímetro Caja»
  - heredado · Conciliación B!A3: ¿solo añade el perímetro? **sí** · V6.4 «V6.3); tipo de la Historia; margen de partida de Palancas C8» · V6.4.1 «ite declarado de la V6.3); tipo de la Historia; margen de partida de Palancas C8»
  - heredado · Panel!C18: ¿solo añade el perímetro? **sí** · V6.4 «V6.3); tipo de la Historia; margen de partida de Palancas C8» · V6.4.1 «ite declarado de la V6.3); tipo de la Historia; margen de partida de Palancas C8»

## 2. Perímetro: caja (V6.4) frente a NIIF 16 completo

| θ | Perímetro | D_hist (B57) | Exceso (B60) | F_hist (B62) | Rh (B71) | f (B72) | Requisito anual (B89) | Precio de Sí | Zona | ¿Válida? |
|---|---|---|---|---|---|---|---|---|---|---|
| 0,0 | caja | 296,489 | 40,813 | 56,974 | 0,000 | 1,0000 | 0,000 | 40,35 | caro | True |
| 0,0 | NIIF 16 | 320,599 | 64,923 | 81,084 | 0,000 | 1,0000 | 0,000 | 40,35 | caro | True |
| 0,5 | caja | 296,489 | 40,813 | 56,974 | 20,407 | 1,0739 | 4,081 | 39,29 | caro | True |
| 0,5 | NIIF 16 | 320,599 | 64,923 | 81,084 | 32,462 | 1,1127 | 6,492 | 38,62 | caro | True |
| 1,0 | caja | 296,489 | 40,813 | 56,974 | 40,813 | 1,1596 | 8,163 | 38,22 | caro | True |
| 1,0 | NIIF 16 | 320,599 | 64,923 | 81,084 | 64,923 | 1,2539 | 12,985 | 36,88 | caro | True |

**Réplica independiente de las bases** (Python, desde la Historia del libro y las altas conciliadas): 0 discrepancias en D_hist, exceso, F_hist, Rh, f y requisito, en los seis casos.

**Lectura (interpretación).** Con θ = 0 no hay requisito adicional y los dos perímetros dan lo mismo. Con NIIF 16 el exceso histórico pasa de 40,8 a 64,9 millones; el requisito, Rh y f suben, y el precio de Sí baja. Ningún caso sale del dominio declarado. La elección del perímetro sigue pendiente (VISCOFAN-PERIMETRO): la V6.4.1 la hace explícita y la integra en el modelo, pero no la adopta.
