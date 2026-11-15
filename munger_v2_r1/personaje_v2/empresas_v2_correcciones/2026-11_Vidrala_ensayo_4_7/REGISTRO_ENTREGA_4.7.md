# Registro de ejecución y cambios · entrega 4.7 (9-nov-2026)

## Encargo
«Munger V2 — entrega 4.7: reparación del resumen y continuación financiera de Vidrala». Es una entrega consolidada con dos bloques separados:
- **Bloque A:** la invalidación de un expediente aprobado retira la aprobación en el resumen configurado y en cualquier destino registrado, por todas las vías.
- **Bloque B:** validación financiera material de N1 (tipo impositivo), N2 (margen de partida) y N3 (escenario MALO) sobre copias identificadas, con propuestas que no se aplican sin decisión humana.

Todo lo que sigue está ejecutado o declarado por Claude. Nada está comprobado externamente por ChatGPT.

## Modelos
Se usó Opus en todo, incluidos los agentes de auditoría con contexto separado: cuatro agentes para cinco revisiones. El segundo control de vigencia lo hizo el mismo agente que el primero, y así lo declara. Fable no se usó.

## Bloque A · reparación del resumen configurado
1. **Punto de partida:** paquete 4.6.1 verificado (ZIP `4bc68649…5a5b92`; 1.354 archivos sin diferencias; P1 `b4e47afc…c445a4`).
2. **Reproducción con el código 4.6.1**, sobre su árbol íntegro: el fallo se reproduce en las dos rutas (`reproduccion/reproduccion_resumen_codigo_4_6_1.txt`). Con el código 4.7: «NO SE REPRODUCE» (`reproduccion/reproduccion_resumen_codigo_4_7.txt`).
3. **Reparación:**
   - `cierre_v2.py`, sección 6: registro `publicaciones_resumen.json`, con respaldo, `registro_id`, copias y traslados, salida humana y escritura atómica;
   - integración en `pipeline.py`, `ficha.py`, `informe.py` y `resumen.py`;
   - código de salida 5, «retirada pendiente».
   - El detalle está en el Anexo D, «Destinos registrados del resumen», y en `CIERRE_TECNICO_BLOQUE_A.md`.
4. **Auditorías internas de Claude con contexto separado:** ninguna encontró hallazgos bloqueantes. Cada revisión trabajó sobre material fijado por huellas, y cada corrección posterior pasó por la siguiente revisión.

   | Auditoría | Material (SHA-256 del archivo de huellas) | Hallazgos importantes del bloque A | Corrección |
   |---|---|---|---|
   | primera | `MATERIAL_AUDITADO_4_7.txt` · `b849b5db…` | H-1 destino ausente; H-2 expediente trasladado; H-3 `resumen.py` sin ficha | cierre revisado (§3) |
   | control | `MATERIAL_CONTROL_4_7.txt` · `b75c2292…` | C-1 copia del árbol con el original vivo; C-2 traslado completo con código 5 permanente | cierre final (§4) |
   | final | `MATERIAL_FINAL_4_7.txt` · `fb044c67…` | F-1 regresión hacia un CSV ajeno; F-2 aprobación sin registrar en el predeterminado | cierre definitivo (§5) |
   | vigencia | `MATERIAL_VIGENCIA_4_7.txt` · `2d804f7f…` | V-1: F-2 no actuaba por el pipeline configurado (empresa tomada del nombre de la carpeta) | ajustes del §5 (22:15) |
   | vigencia 2 | `MATERIAL_VIGENCIA2_4_7.txt` · `2a8716b4…` | ninguno importante; W-1 menor, W-2 y W-3 observaciones | W-1 y W-2 quedan pendientes (abajo); W-3 es este empaquetado |

5. **Pruebas:** `test_resumen_v2.py` tiene 34 pruebas.

   | Código | Resultado |
   |---|---|
   | definitivo | **34/34** |
   | el que vio el primer control de vigencia | 33/34 |
   | el que vio la auditoría final | 30/34 |
   | el que vio la auditoría de control | 27/34 |
   | el que vio la primera auditoría | 19/34 |
   | 4.6.1 | 6/34 |

   `test_cierre_v2.py` da 55/55.
6. **Verificador:** el bloque «batería del resumen» es obligatorio en `verificar_paquete.sh completa`, con un mínimo de 34. Las integraciones de la 4.7 y de la 4.6.1 dan 13 de 13.
7. **Cierre técnico:** `CIERRE_TECNICO_BLOQUE_A.md` declara el orden real de los trabajos (§0).
   - El documento del primer cierre se escribió después de los libros de propuesta.
   - El bloque B se rehízo tras la primera auditoría.
   - Ninguna variante financiera usa el código del bloque A.
8. **Hallazgos que quedan abiertos tras el segundo control de vigencia** (no se corrigieron para no cambiar el material ya controlado):
   - **W-1 (menor):** `resumen.py`, invocado con una ficha cerrada no vigente hacia un destino distinto del predeterminado, no retira en esa llamada una aprobación sin registrar del predeterminado. La retira la siguiente sincronización por cualquier vía (pipeline, `informe.py`, `ficha.py`). El Anexo D, l. 207, lo afirma para «toda invalidación» y, en esta vía, solo es cierto a partir de la llamada siguiente.
     - Arreglo propuesto: sincronizar tras `archivar_salidas` en esa rama, como hace `informe.py`.
     - El auditor señala, por lectura y sin probarlo, que `ficha.py` (sustitución de una ficha cerrada) tampoco sincroniza tras archivar.
   - **W-2 (observación):** la consecuencia declarada para un registro sin `registro_id` (Anexo D, l. 211) vale para las vías directas. Por el pipeline de la copia con su configuración, su CSV configurado sí se retira.
9. **Límites declarados (Anexo D):**
   - CSV compartido entre dos expedientes de la misma empresa (H-7), y su extensión a una copia del expediente solo llevada a otro árbol (F-4);
   - registro y respaldo borrados a la vez;
   - punto de montaje vacío (C-10);
   - copia colocada en la ruta antigua antes de sincronizar (F-5b).
10. **Intactos:**
   - cifras, fuentes, fases, libros y P1 son idénticos a la 4.6.1;
   - los 1.342 archivos de la 4.6.1 que no son código del bloque A ni documentación conservan su huella;
   - el expediente de referencia de la 4.6.1 sigue vigente y sin registro.
11. **Error de Claude descubierto al verificar el empaquetado: el Anexo D estaba truncado.**
    - **Qué ocurrió:** al reescribir la sección «Destinos registrados del resumen» tras la primera auditoría, el script de edición buscaba el siguiente encabezado `###` y no lo encontró, porque lo que seguía era `## D.6b`. Por eso se perdieron las 56 líneas finales del Anexo D de la 4.6.1 (§D.6b y siguientes).
    - **Por qué no se vio antes:** ninguna de las cinco revisiones lo detectó. Lo detectó `test_comprobadores.py` dentro de `verificar_paquete.sh completa` sobre el primer ZIP candidato: dio 113/114, al fallar «prompt y Anexo D enuncian la regla nueva y el «Aviso:»», y el resultado global fue FALLA.
    - **Reparación:** se repuso el texto de la 4.6.1 completo, sin tocar la sección de la 4.7. La copia de referencia es `reproduccion/ANEXO_D_4_6_1.md`, con la huella del manifiesto de la 4.6.1. `test_comprobadores.py` vuelve a 114/114.
    - **Ajuste del comprobador:** `comprobar_entrega_4_7.py` se amplió, sin añadir controles, para reconocer esa restauración en el control de vigencia final. Sin el bloque repuesto, el Anexo D es exactamente el controlado (`97298b8e…`). La versión controlada del propio comprobador se conserva en `reproduccion/comprobar_entrega_4_7_controlado.py.txt` (`05c81f32…`).
    - **Alcance:** son los dos únicos archivos que cambian después del segundo control de vigencia, aparte de este registro, el manifiesto y la lista de cambios.
12. **Observación de procedimiento (C-9):** las ejecuciones con el código 4.6.1 dejaron cuatro `.pyc` en `__pycache__` del árbol de trabajo de la 4.6.1 (`/home/claude/entrega461/`, fuera de este paquete). Su manifiesto sigue intacto. Desde entonces se usa `PYTHONDONTWRITEBYTECODE=1`.

## Bloque B · N1–N3
Informe: `INFORME_FINANCIERO_N1_N3.md`. Scripts: `scripts/analisis_n1_n3.py` y `scripts/propuesta_excel.py`. Salidas: `financiero/`.
- **Evidencia:** 109 datos de los textos conservados, con archivo, página, concepto, columna publicada, período, perímetro, unidad y signo, todos reproducidos con su signo. Incluye las conciliaciones fiscales completas de 2021–2025 (31 líneas) y el segmento de Italia de 2018–2022.
- **Réplica:** reproduce el libro de referencia (53,6704 / 70,7722 / 86,4888; ponderado 70,4952; precio de Sí 65,6881; `r_op` 0,0869221) con una tolerancia de 0,005 €.
- **N1:**
  - el 20,0 % reconstruido es la media 2021–2025 del tipo efectivo;
  - propuesta T1 = 22,05 % (media 2023–2025 de continuadas, con toda la conciliación);
  - robustez: 21,6–21,9 %; sin 2024, 22,37 %;
  - T2 = 24,33 % queda como sensibilidad adversa;
  - la formulación anterior (23,30 %) se descartó por la primera auditoría y se conserva.
- **N2:**
  - la afirmación de fase_c.md, «no puede quedar por debajo» del 16,9 %, **no queda demostrada**;
  - el intervalo 16,9–19,9 % se describe solo como sensibilidad condicional;
  - propuesta M1 = 18,55 %;
  - efectos: perímetro +0,36 pp, ventana +1,33 pp, Brasil +0,56 pp.
- **N3:**
  - los ≈ 16 mm salen de la liberación simétrica ΔV ÷ S2C;
  - el FCF1 del MALO supera al del NORMAL porque el NORMAL reinvierte para crecer;
  - el circulante es el 14,70 % de las ventas y los compromisos de inmovilizado son de 66,6 mm;
  - propuesta R1: solo se libera el circulante y se conserva la capacidad. La regla de recuperación se revisó por coherencia y está declarada.
- **Matriz:** 27 combinaciones. La recomendada, T1·M1·R1, da 51,81 / 69,78 / 85,08, ponderado 69,24 (−1,25) y precio de Sí 64,26 (−1,43). Son resultados mecánicos, no una comparación válida con el precio de 87,9 ni una recomendación de compra o espera.
- **Libros de propuesta:**
  - M2 (Palancas!C8) y T1·M1 (Diagnóstico V6!C10/C11, sustitución declarada de fórmulas en la copia) coinciden con la réplica;
  - sus `precio.json` llevan el aviso de no comparabilidad;
  - R1 no es representable en la plantilla.
- **Decisiones humanas:** `financiero/decisiones_propuestas_N1_N3.json` está preparado y sin rellenar (D-N1, D-N2, D-N3).
- **Sin cambios:** N4, N9, N10, P-N1 y P-N2.

## Mejora frente a la 4.6.1

| Aspecto | 4.6.1 | 4.7 |
|---|---|---|
| Resumen configurado tras una invalidación directa | la aprobación sobrevivía | se retira en todos los destinos registrados y en el predeterminado, también con salidas archivadas, copias y traslados |
| Destino inaccesible | sin tratamiento | retirada pendiente, código 5, reintento; salida humana para un destino que no volverá |
| Baterías obligatorias en `completa` | cierre (55) | cierre (55) y resumen (34) |
| N1 tipo impositivo | 20,0 % sin examinar | conciliación completa; propuesta 22,05 % con robustez y sensibilidades |
| N2 margen de partida | 16,9 %; afirmación «no puede quedar por debajo» sin prueba | perímetros año a año; afirmación no demostrada; propuesta 18,55 % |
| N3 MALO | liberación de ≈ 16 mm sin examinar | reconstrucción año a año y realizabilidad; propuesta R1 en un modelo auxiliar |
| Comparación conjunta | no existía | 27 combinaciones reproducibles y dos libros de propuesta |
| Evidencia | — | 109 datos trazados con signo |

## Pendientes, por prioridad
1. **Decisiones de la persona responsable:** D-N1, D-N2 y D-N3 (archivo preparado).
2. **Si se aplican,** cómo llevarlas a la plantilla: entradas de tipo normalizado y margen de partida manual, y regla de reinversión asimétrica. Después, una nueva ejecución del personaje con auditoría.
3. **Datos que faltan:**
   - segmento de Italia 2016–2017;
   - Santos Barosa 2016;
   - pro forma de Brasil antes de 2023;
   - naturaleza de los «otros ajustes» y de las permanentes recurrentes.
4. **Hallazgos abiertos del bloque A:** W-1 (corrección de una llamada, propuesta) y W-2 (precisión del Anexo D).
5. **Límites declarados del bloque A**, por si la persona responsable quiere cerrarlos: una columna de material o expediente en el formato del resumen (H-7, F-4); el punto de montaje (C-10).
6. **Pendientes que siguen como estaban:** N4, N9, N10, P-N1 y P-N2.

## Verificación del paquete 4.7
Se verificó sobre una descompresión limpia del ZIP candidato, cuyo contenido es el mismo que el del final salvo este apartado, y el ZIP final se volvió a verificar del mismo modo. Sus huellas están en el `.sha256` y en `PARTES.txt` de la entrega, no aquí, porque escribirlas cambiaría el propio paquete.

**Primer candidato.** Dio FALLA por el Anexo D truncado (punto 11 del bloque A). Se reparó, se limpiaron los restos de una ejecución de `test_comprobadores.py` en el árbol de trabajo y se generó un candidato nuevo.

**`bash verificar_paquete.sh completa`:** código 0 y «RESULTADO GLOBAL: PASA», en unos 8 minutos.
- manifiesto: 1.412 archivos, 0 modificados, 0 ausentes y 0 de más;
- entorno: pasa;
- piloto: 35 comprobaciones, salida idéntica;
- 114/114 y 30/30, con los mismos nombres que la línea de base;
- batería del resumen: **34/34**, «RESULTADO resumen: PASA»;
- batería de cierre: **55/55**, «RESULTADO cierre: PASA».

**Aparte** (código 0 y salida idéntica a la de referencia):
- 45 de la 4.2;
- 217 de la 4.3;
- 43 de la 4.3.1;
- 72 de la 4.4;
- 60 de la 4.5;
- 24 de la 4.6;
- 23 de la 4.6.1;
- **49 de la 4.7**.

Tras las pruebas, las 1.412 entradas del manifiesto siguen intactas.

**Respecto a la 4.6.1:**
- **cambian 11 archivos:**
  - código: `cierre_v2.py`, `ficha.py`, `informe.py`, `pipeline.py` y `resumen.py`;
  - verificador: `verificar_paquete.sh`;
  - documentación: el Anexo D y `DECISIONES.md`;
  - paquete: `VERSION`, `CONTINUIDAD.md` y `PROMPT_NUEVA_VENTANA.md`;
- **se regeneran** `CAMBIOS_ARCHIVOS.txt` y el manifiesto;
- **ninguno desaparece;**
- **hay 58 nuevos:** `personaje_v2/pruebas/test_resumen_v2.py` y la carpeta `2026-11_Vidrala_ensayo_4_7/`;
- los originales y los expedientes de la 4.4 a la 4.6.1 son idénticos.
