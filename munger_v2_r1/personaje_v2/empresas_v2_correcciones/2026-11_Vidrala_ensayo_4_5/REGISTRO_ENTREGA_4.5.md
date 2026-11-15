# Registro de ejecución y cambios · entrega 4.5 (9-nov-2026)

## Encargo
«Munger v2 · reanudación del ensayo Vidrala tras el registro humano de P1».

**Pide:**
- validar el registro de P1 e incorporarlo sin modificarlo;
- reanudar el pipeline desde el paso 2, con los controles K14, C53 y C58;
- ejecutar de nuevo el personaje: extracción, fases A, B y C, y auditoría con contexto independiente. El motor B es la hipótesis principal y r = 0,09;
- conservar la resolución del dividendo;
- hacer un contraste controlado con el motor A y T3;
- comparar el resultado con el original;
- versionar el paquete como 4.5.

**Prohíbe:**
- confirmar ceros;
- cambiar hipótesis para obtener un Sí;
- actualizar en silencio el precio o los datos de 2026;
- presentar los resultados mecánicos como una comparación válida o una recomendación;
- alterar las 72 comprobaciones de la 4.4.

## Ejecución
1. **Primer mensaje sin el archivo de decisiones.** El primer mensaje del encargo llegó sin el archivo. Se identificó solo ese defecto y no se inventaron campos. Mientras tanto se prepararon:
   - la copia de continuación;
   - el validador `validar_registro_P1.py`, probado con tres casos.
2. **Registro recibido** (2.703 bytes, SHA-256 `b4e47afc…c445a4`):
   - validado con 10 de 10 requisitos;
   - conservado en `registro_P1/`;
   - copiado byte a byte como `Vidrala/fase1_decisiones.json`.
3. **Pipeline desde el paso 2** (`python3 -I personaje_v2/scripts/pipeline.py …/2026-11_Vidrala_ensayo_4_5/Vidrala`):
   - `construir` aplicó P1;
   - siguieron el relleno, la entrada (0 bloqueantes) y el volcado.

   Controles: K14 = 84,994; C53 = 0,915854; C58 = −0,027608. Solo cambiaron K14 y sus derivadas, todas explicadas.
4. **Pasos de agente.** Cada uno se ejecutó en un contexto separado, con el prompt generado por el pipeline y `ENTRADAS_AGENTES_4_5.md`:
   - extracción;
   - fase A, con el motor B justificado de nuevo;
   - fase B, con un S2C propio de 0,9 / 0,9 / 1,0;
   - fase C, en dos turnos, sin revisión de palancas;
   - auditoría, con veredicto APROBADO.

   Tras cada paso se relanzó el pipeline, que validó esquemas, citas, celdas, gramática y recálculo. Terminó en el paso 14: concluido, auditoría APROBADO, sin correcciones.
5. **Contraste de motores** en copias separadas (`contraste_motores.py`), con su descomposición (`descomponer_contraste.py`; la réplica reproduce la hoja al céntimo).
6. **Comparación con el original** (`comparar_con_original.py`) y controles (`comprobar_continuacion.py`, 60 de 60).
7. **Documentos:**
   - `INFORME_DEL_ENSAYO_4_5.md`;
   - `registro_P1/REGISTRO_APLICACION_P1.md`;
   - `REGISTRO_HIPOTESIS_ENSAYO_4_5.md` (copia del de la 4.4 con la fila de P1 actualizada);
   - `ENTRADAS_AGENTES_4_5.md`;
   - este registro.

## Qué no se ha hecho
- **Datos y supuestos:**
  - no se ha confirmado ningún cero;
  - no se ha cambiado ningún dato ni hipótesis para obtener un resultado;
  - no se han actualizado el precio, las acciones, la capitalización ni los datos de 2026;
  - no se han completado E1–E7.
- **Código:** no se ha modificado el código del sistema, `v6/` ni `verificar_paquete.sh`.
- **Sensibilidades no ejecutadas:**
  - la variante T3δ: δ = 0 se mantiene como hipótesis;
  - la alternativa del valor sin derecho al dividendo, que solo se cuantifica.
- **Observaciones de procedimiento de la auditoría:** quedan como propuesta, sin cambios de código.

## Modelos
- **Opus** en la orquestación y en los cinco agentes de contexto separado. El cuarto agente hizo los dos turnos de la fase C.
- **Diferencia declarada:** `config_v2.json` prevé Sonnet con esfuerzo medio para la extracción y esfuerzo medio para la verificación.
- **Fable no se usó.**

## Cambios del paquete respecto a la 4.4
- **Nuevo:** `personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_5/`, con:
  - el expediente `Vidrala/`, que incluye el libro evaluado, el recalculado, las fases, la auditoría, la ficha y el informe;
  - `registro_P1/`;
  - `contraste_motores/`;
  - `resultados/`;
  - `scripts/`;
  - los documentos.
- **Modificados:** `VERSION`, `CONTINUIDAD.md` y `PROMPT_NUEVA_VENTANA.md`.
- **Se regeneran:** `CAMBIOS_ARCHIVOS.txt` y `MANIFIESTO_SHA256.txt`.
- **Sin cambios:**
  - `personaje_v2/empresas_v2/` (originales);
  - el expediente de la 4.4, con sus 72 comprobaciones;
  - los contrastes anteriores;
  - el código;
  - `v6/`.
- **Limpieza:** se borraron las cachés que crean las ejecuciones (`__pycache__` y los perfiles `.lo_perfil` de LibreOffice). No forman parte del paquete.

## Verificación del paquete 4.5
Hecha sobre una descompresión limpia del ZIP candidato, con el mismo contenido que el final salvo este apartado. El ZIP final se volvió a verificar igual. Su huella está en el `.sha256` y en `PARTES.txt` de la entrega, no aquí, porque cambiaría el propio paquete.

**`bash verificar_paquete.sh completa`:** código 0 y «RESULTADO GLOBAL: PASA».
- manifiesto: 1.069 archivos, 0 modificados, 0 ausentes y 0 de más;
- entorno: pasa;
- piloto: 35 comprobaciones, salida idéntica;
- 114/114 y 30/30, con los mismos nombres que la línea de base.

**Aparte** (código 0 y salida idéntica a la de referencia en las cinco):
- 45 de la 4.2;
- 217 de la 4.3;
- 43 de la 4.3.1;
- 72 de la 4.4, sobre su expediente intacto;
- 60 de la 4.5.

**Después de las baterías:** los 1.069 archivos del manifiesto siguen intactos.

**Respecto a la 4.4:**
- cambian 4 archivos del paquete (`VERSION`, `CONTINUIDAD.md`, `PROMPT_NUEVA_VENTANA.md` y `CAMBIOS_ARCHIVOS.txt`);
- no desaparece ninguno;
- 131 son nuevos, todos en `2026-11_Vidrala_ensayo_4_5/`.
