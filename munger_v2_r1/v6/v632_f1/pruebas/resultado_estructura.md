# Pruebas V6.3.2 F1 · estructura

Fecha 2026-11-19 · plantilla `046b64fc7b7898c8…` · referencia `2bed4bac64b00a2a…`

**PASA: 26/26**

| Comprobación | Resultado | Detalle |
|---|---|---|
| la V6.3 no cambia (SHA-256 = origen de su referencia) | PASA | 8381a6cd7b1d798f |
| la V6.3.1 F1 no cambia (SHA-256 eaece01a… = origen de su referencia): los expedientes V6.3.1 siguen con sus huellas | PASA | eaece01a7d6a1d86 |
| reconstrucción determinista: el guion desde la V6.3 da el mismo SHA-256 que el entregable | PASA | 046b64fc7b7898c8 / 046b64fc7b7898c8 |
| la referencia salió de este entregable | PASA |  |
| SHA256_entregables_V6.3.2_F1.txt coincide | PASA |  |
| frente a la V6.3.1: fórmulas alteradas = fila 30, C53, C58, C76, Motor E205 y Panel A1 (y ninguna más) | PASA | de más [] · de menos [] |
| ninguna fórmula de la V6.3.1 quitada | PASA | [] |
| fórmulas nuevas = Historia C95:L95 (excluido), C96:L96 (circulante de la reinversión) y C97 (normalización efectiva) | PASA | [] |
| Historia C53: con «ninguna» la fórmula de la V6.3.1 F1 literal (y con ella, con A0, la de la V6.3) | PASA |  |
| Historia C58: con «ninguna» la fórmula de la V6.3.1 F1 literal (y con ella, con A0, la de la V6.3) | PASA |  |
| Historia C76: con «ninguna» la fórmula de la V6.3.1 F1 literal (y con ella, con A0, la de la V6.3) | PASA |  |
| fila 30: la de la V6.3.1 con el circulante de la fila 96 en lugar del de la fila 14 | PASA |  |
| C58 con «circulante_a_cero»: exige normalizados todos los años de la ventana (C94:L94 = 1) antes de la rama de D_X de la V6.3.1 | PASA |  |
| C53 con «circulante_a_cero»: los cinco años H–L de las filas 12, 13, 14 y 88 y normalizados los cinco (no se mezclan) | PASA |  |
| Motor E205: la de la V6.3.1 más dos causas al final (normalización no reconocida: INV; ventana sin normalizar: INC) en lugar del último «» | PASA | IF(Historia!$C$97="no reconocida","INV/Normalización del circulante (Historia C93:L94) no  |
| celdas fijas alteradas = tres etiquetas de versión | PASA | ['Análisis!A1', 'Control maestro!A3', 'Guía V6!A1'] |
| ninguna celda fija de la V6.3.1 quitada | PASA |  |
| celdas fijas nuevas solo en la sección nueva (Historia filas 92–98) | PASA | 13 celdas |
| mismas hojas, formato condicional, nombres definidos y partes del paquete que la V6.3.1 (y la V6.3) | PASA | 13 partes |
| validaciones: solo dos nuevas en la Historia (lista de la regla en C93; 1 o vacío en C94:L94) | PASA | [['C93', 'list', '', '"circulante_a_cero"', '', True], ['C94:L94', 'whole', 'equal', '1', '', True]] |
| inventario de entradas: el de la V6.3.1 F1 más Historia C93, C94:L94 y M93:S94 | PASA | ['C5:L26', 'C57', 'M5:S26', 'C85', 'C86:L87', 'M85:S87', 'C93', 'C94:L94', 'M93:S94'] |
| verificar_v632.py: la plantilla es ÍNTEGRA frente a su referencia | PASA | VEREDICTO: ÍNTEGRO · 0 fallos · 0 avisos |
| verificar_v631.py (V6.3.1) rechaza la V6.3.2: una plantilla no pasa por la otra | PASA | VEREDICTO: ALTERADO · 40 fallos · 13 avisos |
| verificar_v631.py sigue aceptando la V6.3.1 F1 | PASA |  |
| verificar_v632.py rechaza una mutación: el circulante de la reinversión sin normalizar (H96 = H14) | PASA | VEREDICTO: ALTERADO · 1 fallos · 0 avisos |
| verificar_v632.py rechaza una mutación: la normalización efectiva fija (C97 = «circulante_a_cero») | PASA | VEREDICTO: ALTERADO · 1 fallos · 0 avisos |
