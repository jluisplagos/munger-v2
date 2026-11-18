# Pruebas V6.3.1 F1 · estructura

Fecha 2026-11-18 · plantilla `266d53bdd8af13d5…` · referencia `cd564e43f60239c8…`

**PASA: 21/21**

| Comprobación | Resultado | Detalle |
|---|---|---|
| la V6.3 no cambia (SHA-256 = origen de su referencia) | PASA | 8381a6cd7b1d798f |
| reconstrucción determinista: el guion desde la V6.3 da el mismo SHA-256 que el entregable | PASA | 266d53bdd8af13d5 / 266d53bdd8af13d5 |
| la referencia salió de este entregable | PASA |  |
| SHA256_entregables_V6.3.1_F1.txt coincide | PASA |  |
| fórmulas alteradas = fila 30, C53, C58, C76, Motor E205 y Panel A1 (y ninguna más) | PASA | de más [] · de menos [] |
| ninguna fórmula de la V6.3 quitada | PASA | [] |
| fórmulas nuevas = Historia C88:L88 (D_X) y C89 (perímetro efectivo) | PASA | [] |
| Historia C53: con A0 la fórmula de la V6.3 literal | PASA |  |
| Historia C58: con A0 la fórmula de la V6.3 literal | PASA |  |
| Historia C76: con A0 la fórmula de la V6.3 literal | PASA |  |
| fila 30: la de la V6.3 con D_X (fila 88) en lugar de la D&A (fila 8) | PASA |  |
| Motor E205: la de la V6.3 más tres causas al final (perímetro no reconocido, D_X vacía, D_X negativa) en lugar del último «» | PASA | IF(Historia!$C$89="no reconocido","INV/Perímetro F1 de la reinversión (Historia  |
| celdas fijas alteradas = tres etiquetas de versión | PASA | ['Análisis!A1', 'Control maestro!A3', 'Guía V6!A1'] |
| ninguna celda fija de la V6.3 quitada | PASA |  |
| celdas fijas nuevas solo en la sección nueva (Historia filas 84–90) | PASA | 13 celdas |
| mismas hojas, formato condicional, nombres definidos y partes del paquete | PASA | 13 partes |
| validaciones: solo dos nuevas en la Historia (lista del perímetro en C85; ≥ 0 en C86:L87) | PASA | [['C85', 'list', '', '"A0_total,A1_sin_ROU,A2_propio"', '', True], ['C86:L87', 'decimal', 'greaterThanOrEqual', '0', '', True]] |
| inventario de entradas: el de la V6.3 más Historia C85, C86:L87 y M85:S87 | PASA | ['C5:L26', 'C57', 'M5:S26', 'C85', 'C86:L87', 'M85:S87'] |
| verificar_v631.py: la plantilla es ÍNTEGRA frente a su referencia | PASA | VEREDICTO: ÍNTEGRO · 0 fallos · 0 avisos |
| verificar_v63.py (V6.3) rechaza la V6.3.1: una plantilla no pasa por la otra | PASA | VEREDICTO: ALTERADO · 30 fallos · 13 avisos |
| verificar_v631.py rechaza una mutación de D_X (C88 = C8) | PASA | VEREDICTO: ALTERADO · 1 fallos · 0 avisos |
