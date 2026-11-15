# Registro de ejecución y cambios · entrega 4.6 (9-nov-2026)

## Encargo
«Munger v2 · reparación del cierre y la presentación del ensayo Vidrala». Repara cuatro incidencias:
- **I1:** `concluido` se publicaba antes de la auditoría.
- **I2:** faltaba la marca de datos de etapa 1 incompletos.
- **I3:** `no_procede` no correspondía al vocabulario de C104.
- **I4:** las comparaciones con el precio no llevaban aviso local.

Autoriza los cambios de código, documentación, formatos y pruebas estrictamente necesarios. No autoriza cambios financieros ni de criterio.

## Ejecución
1. **Punto de partida.** Paquete 4.5 verificado: SHA-256 `037c1cc5…cce997` y 1.069 archivos sin diferencias. Copia de trabajo nueva.
2. **Reproducción con el código 4.5.** `scripts/reproducir_incidencias.py` reprodujo las cuatro incidencias (`reproduccion/reproduccion_codigo_4_5.txt`).
3. **Reparación.** El detalle por incidencia está en `INFORME_REPARACION_4_6.md`.
4. **Pruebas:**
   - acceptance tests nuevos, `pruebas/test_cierre_v2.py`: 40/40 (`resultados/test_cierre_v2_salida.txt`);
   - `test_comprobadores.py`: 114/114;
   - `test_pipeline_sintetico.py`: 30/30;
   - reproducción con el código 4.6: ninguna incidencia se reproduce.
5. **Expediente regenerado** en `Vidrala/`, copia del de la 4.5:
   - la auditoría 4.5 se conserva como antecedente;
   - se añade `alcance_v2.json`;
   - C104 lleva la etiqueta armonizada;
   - se reanuda en el segundo turno de la fase C (`turno_c = 2`, `--desde 10`).
6. **Primera auditoría nueva:** APROBADO, con dos avisos sobre el material. Se corrigieron (código y una frase de `fase_c.md`) y se reanudó otra vez. El pipeline rechazó esa auditoría para el material nuevo, por id distinto.
7. **Segunda auditoría nueva:** APROBADO del material `74b94f8072dd58c1`. Después, el paso 14 escribió las salidas oficiales: concluido, Vigilar, auditoría APROBADO.
8. **Contraste y comparación.** El contraste entre motores y su descomposición se repitieron sobre el libro 4.6 con los scripts de la 4.5. La comparación numérica con la 4.5 dio 30/30. Los controles del expediente, `comprobar_cierre_ensayo.py`, dieron 24/24.

## Qué no se ha hecho
- **Criterios y fases:** no se ha cambiado ningún criterio, umbral, materialidad, palanca, probabilidad, r ni número. No se han vuelto a ejecutar las fases A y B. No se han modificado registros humanos.
- **Herramientas de verificación:** no se ha cambiado `verificar_paquete.sh` ni la regla estricta de H2.
- **Pendientes abiertos:** los normativos P-N1 a P-N3 quedan como pendientes (informe, §8).

## Modelos
- **Opus** en la orquestación y en las dos auditorías, cada una de contexto separado.
- **Fable no se usó.**

## Verificación del paquete 4.6
Se hizo sobre una descompresión limpia del ZIP candidato, que tiene el mismo contenido que el final salvo este apartado. El ZIP final se volvió a verificar del mismo modo. Su huella está en el `.sha256` y en `PARTES.txt` de la entrega, no aquí, porque escribirla cambiaría el propio paquete.

**`bash verificar_paquete.sh completa`:** código 0 y «RESULTADO GLOBAL: PASA».
- manifiesto: 1.208 archivos, 0 modificados, 0 ausentes y 0 de más;
- entorno: pasa;
- piloto: 35 comprobaciones, salida idéntica;
- 114/114 y 30/30, con los mismos nombres que la línea de base.

**Baterías aparte** (código 0 y salida idéntica a la de referencia):
- 45 de la 4.2;
- 217 de la 4.3;
- 43 de la 4.3.1;
- 72 de la 4.4;
- 60 de la 4.5;
- 24 del expediente 4.6.

**Pruebas de aceptación** `test_cierre_v2.py`: 40/40, con código 0.

**Integridad tras las pruebas:** los 1.208 archivos del manifiesto siguen intactos.

**Respecto a la 4.5:**
- cambian 16 archivos del paquete:
  - código: `pipeline.py`, `ficha.py`, `informe.py`, `verificar_todo.sh` y `agentes_sinteticos.py`;
  - prompts: `verificacion.md` y `fase_c_turno2.md`;
  - documentación: el personaje, los anexos A y D, el encargo y `DECISIONES.md`;
  - archivos de paquete: `VERSION`, `CONTINUIDAD.md`, `PROMPT_NUEVA_VENTANA.md` y `CAMBIOS_ARCHIVOS.txt`;
- no desaparece ninguno;
- hay 139 nuevos: `scripts/cierre_v2.py`, `pruebas/test_cierre_v2.py` y la carpeta `2026-11_Vidrala_ensayo_4_6/`.
