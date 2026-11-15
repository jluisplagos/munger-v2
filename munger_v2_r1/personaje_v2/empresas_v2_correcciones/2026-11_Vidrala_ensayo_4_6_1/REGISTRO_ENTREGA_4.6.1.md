# Registro de ejecución y cambios · entrega 4.6.1 (9-nov-2026)

## Encargo
«Munger v2 · reparación de la vigencia de las salidas oficiales». Pide que, cuando cambie el material aprobado, ninguna ruta conserve ni vuelva a publicar como vigente una salida oficial cerrada con la aprobación anterior. Autoriza cambios de código, pruebas, documentación y verificación; no autoriza cambios financieros.

## Ejecución
1. **Punto de partida:** paquete 4.6 verificado (SHA-256 `160b4656…92771b`, 1.208 archivos sin diferencias).
2. **Reproducción con el código 4.6:** `scripts/reproducir_vigencia.py` reprodujo el caso en sus tres rutas (`reproduccion/reproduccion_codigo_4_6.txt`).
3. **Reparación:** vigencia en `cierre_v2.py`, con su integración en `pipeline.py`, `ficha.py`, `informe.py` y `resumen.py`. Detalle en `INFORME_REPARACION_4_6_1.md`.
4. **Pruebas:**
   - `test_cierre_v2.py`: 55/55 con el código reparado; 43/55 con el 4.6, con las 12 negativas nuevas en FALLA;
   - reproducción con el código reparado: no se reproduce en ninguna de las tres rutas.
5. **Verificador:** la batería de cierre es obligatoria en `verificar_paquete.sh completa`. `comprobar_integracion_verificador.py` lo confirma con 13 de 13.
6. **Expediente regenerado:** copia del aprobado de la 4.6.
   - Al lanzar el pipeline, las salidas oficiales de la 4.6 se archivaron y la fila del resumen dejó de figurar como vigente.
   - Hubo una auditoría nueva e independiente: APROBADO del material `74b94f8072dd58c1`.
   - Tras ella, el cierre oficial se registró en `cierre_vigente.json`.
7. **Comparación y controles:** la comparación con la 4.6 da 32 de 32 (sin diferencias numéricas). Los controles del expediente (`comprobar_vigencia_ensayo.py`) dan 23 de 23.

## Qué no se ha hecho
- **Contenido financiero:** no se ha cambiado ningún dato, hipótesis, palanca, probabilidad, r ni número, y no se han vuelto a ejecutar las fases.
- **Reglas y registros:** no se ha tocado H1–H3, la regla estricta de H2 ni ningún registro humano.

## Modelos
Opus en todo, incluido un agente de auditoría de contexto separado. Fable no se usó.

## Verificación del paquete 4.6.1
Se verificó sobre una descompresión limpia del ZIP candidato, cuyo contenido es el mismo que el del final salvo este apartado. El ZIP final se volvió a verificar del mismo modo. Su huella está en el `.sha256` y en `PARTES.txt` de la entrega, y no aquí, porque escribirla cambiaría el propio paquete.

**`bash verificar_paquete.sh completa`:** código 0 y «RESULTADO GLOBAL: PASA».
- manifiesto: 1.354 archivos, 0 modificados, 0 ausentes y 0 de más;
- entorno: pasa;
- piloto: 35 comprobaciones, salida idéntica;
- 114/114 y 30/30, con los mismos nombres que la línea de base;
- batería de cierre: **55/55**, «RESULTADO cierre: PASA».

**Aparte** (código 0 y salida idéntica a la de referencia):
- 45 de la 4.2;
- 217 de la 4.3;
- 43 de la 4.3.1;
- 72 de la 4.4;
- 60 de la 4.5;
- 24 de la 4.6;
- 23 de la 4.6.1.

Tras las pruebas, los 1.354 archivos del manifiesto siguen intactos.

**Respecto a la 4.6:** cambian 14 archivos, ninguno desaparece y hay 146 nuevos, todos en `2026-11_Vidrala_ensayo_4_6_1/`. Los 14 son:
- **código y pruebas:** `cierre_v2.py`, `pipeline.py`, `ficha.py`, `informe.py`, `resumen.py` y `test_cierre_v2.py`;
- **documentación:** el prompt de verificación, el Anexo D y `DECISIONES.md`;
- **verificador:** `verificar_paquete.sh`;
- **archivos de paquete:** `VERSION`, `CONTINUIDAD.md`, `PROMPT_NUEVA_VENTANA.md` y `CAMBIOS_ARCHIVOS.txt`.
