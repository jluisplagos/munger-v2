# Mensaje de arranque para una ventana nueva

Este archivo se usa así:
1. Se abre una conversación nueva.
2. Se adjunta `munger_v2_r1_entrega4.14_cierre_verificacion_entradas.zip` (si se recibió en partes, reconstruido antes según `…zip.PARTES.txt`) y, de forma opcional, `munger_v2_r1_entrega4.14_cierre_verificacion_entradas.zip.sha256`.
3. Se pega como primer mensaje todo el texto que va debajo de la línea. También puede adjuntarse este archivo con una frase como «Seguir como primer mensaje el texto de PROMPT_NUEVA_VENTANA.md que va debajo de la línea».

---

# Continuación del proyecto Munger v2 · verificación inicial

Se adjunta `munger_v2_r1_entrega4.14_cierre_verificacion_entradas.zip`: el paquete completo del proyecto. Contiene, por orden:
- la reparación H1–H3 (entrega 3.1);
- el piloto de contraste de Vidrala 2025 (entrega 4.1);
- el contraste de los datos de 2023 y de los arrendamientos de Vidrala (entrega 4.2);
- la revisión financiera del piloto con el personaje (entrega 4.3) y su subsanación acotada (entrega 4.3.1);
- el expediente de ensayo corregido, detenido en el registro humano de P1 (entrega 4.4);
- su continuación tras ese registro, con el personaje ejecutado de nuevo y el contraste entre motores (entrega 4.5);
- la reparación del cierre y la presentación, con el ensayo regenerado (entrega 4.6), y la reparación de la vigencia de las salidas oficiales (entrega 4.6.1);
- la reparación del resumen configurado y la validación financiera N1–N3 de Vidrala, con sus propuestas sin aplicar (entrega 4.7), y la subsanación de su revisión independiente: W-1 y N3 (entrega 4.7.1);
- el contraste financiero de la reposición de Vidrala (P-M1) y la reparación de la coherencia de estados X-a y X-c (entrega 4.8), y la subsanación de su revisión independiente: solicitudes de auditoría identificables (R-T1) y coherencia de la reinversión (R-F1 y R-F2), con P-M1 todavía abierta (entrega 4.8.1);
- la integridad de la respuesta de auditoría vigente (R-V1) y la investigación documental de los 38 ceros pendientes de Vidrala (N4), sin ninguna confirmación de la IA (entrega 4.9);
- la consolidación financiera de Vidrala (N4 revisada, P3, N5–N8 y N10, con variantes aisladas y combinadas y una copia exploratoria) y las correcciones de trazabilidad (ZIP portable, BOM, ficha sin marcadores y libro final acreditado), con una propuesta única de decisiones sin firmar (entrega 4.10).
- la corrección de la preparación de la prueba de trazabilidad T-1 y el ensayo completo de Vidrala con base económica 2025, recorrido por el pipeline con agentes reales hasta el cierre con una auditoría interna nueva (concluido · Vigilar · esperar), con sus propuestas humanas sin firmar (entrega 4.10.1);
- la primera integración económica experimental del motor B: plantilla V6.4 experimental (modo heredado igual a la V6.3; modo experimental con N1, N2, N3 y P-M1 explícitos, conciliación anual y terminal y rechazos con motivo), conectada al pipeline con selección explícita; mecanismo general de cambio de base con limpieza de evidencias; batería obligatoria de 58 pruebas con réplica independiente; revisión interna sin bloqueantes, con sus correcciones; control heredado igual a la 4.10.1 y piloto de Vidrala con una configuración de demostración no adoptada y agentes reales; propuesta humana única sin firmar (entrega 4.11).

- la validación supervisada de la integración, con vigencia antes del rechazo, materialidad y dos protocolos experimentales del objetivo, variantes atadas a las entradas, dominios, trazabilidad y aptitud de uso en las salidas; Vidrala cerrada de nuevo con agentes reales (y su copia con el protocolo de bloqueo) y el primer contraste con otra empresa, Viscofan, con fuentes recuperadas, configuración propia y agentes reales; batería obligatoria de la V6.4 de 127 pruebas, revisión interna, evaluación de aptitud de uso (experimental) y propuesta humana única sin firmar (entrega 4.12).
- la fiabilidad del motor B y la conciliación económica de los dos casos: guardas de estructura antes de la vigencia, acción final y objetivo coherentes, contrato de cobertura y avisos de dominio de todas las variantes; plantilla V6.4.1 experimental con el perímetro de la inversión; acciones y arrendamientos de Viscofan conciliados; interpretaciones de Vidrala corregidas; tres expedientes regenerados con agentes reales; batería obligatoria de la V6.4 de 195 pruebas, dos revisiones internas, aptitud de uso (experimental) y propuesta humana sin firmar en tres grupos (entrega 4.13).
- el cierre con verificación completa de las entradas financieras: reparación 4.13.1 de la vigencia (H5), contrato del juicio sobre el objetivo, verificación de las entradas con revisor independiente como puerta del pipeline, cambio de base con guardián y correcciones de extracción; decisiones de la persona responsable aplicadas en expedientes nuevos con agentes reales (Viscofan y Vidrala concluidos · esperar; Elis, la tercera empresa, pendiente de datos y con el motor A no validado con NIIF 16), efectos separados, auditorías APROBADO, batería obligatoria de la V6.4 de 198 pruebas, matriz del alcance (no completado) y dictamen A–E (entrega 4.14).

La calidad del trabajo debe apoyarse en este expediente verificable y no en la memoria de conversaciones anteriores. La sesión anterior no está disponible.

## Primera tarea: comprobar el estado. No debe iniciarse ningún otro trabajo.
1. Descomprimir el ZIP en una carpeta nueva y vacía, separada de los adjuntos originales, que deben quedar intactos. Si se adjunta el archivo `.sha256`, comparar la huella del ZIP.
2. Leer entero `munger_v2_r1/CONTINUIDAD.md`. Es el punto de entrada y fija el estado, las decisiones vigentes, las limitaciones y los pendientes.
3. Desde `munger_v2_r1/`, ejecutar `bash verificar_paquete.sh completa`. Las pruebas que usan LibreOffice deben ejecutarse en secuencia, nunca dos a la vez. Antes, comprobar el espacio en disco (`CONTINUIDAD.md` §2, punto 5: conviene tener al menos 7 GB libres después de descomprimir).
4. Informar de forma breve:
   - la versión, según `VERSION`;
   - el resultado de cada bloque: manifiesto, entorno, contraste del piloto Vidrala 2025 (esperado 35 comprobaciones CUMPLEN y salida idéntica a la de referencia), `test_comprobadores.py` (esperado 114/114), `test_pipeline_sintetico.py` (esperado 30/30, con los mismos nombres que la línea de base) la batería de vigencia H5 (59/59, 4.13.1), la del juicio sobre el objetivo (27/27, 4.14), la de la verificación de las entradas (33/33, 4.14) y la de la integración V6.4 experimental (198/198, 4.11–4.14), de trazabilidad (78/78, 4.10.1), de integridad de la auditoría vigente (103/103), de solicitudes de auditoría (55/55), de coherencia de estados (28/28), del resumen (45/45) y de cierre (55/55);
   - aparte, sobre la misma descompresión y después de la verificación, el control de la 4.14 (`python3 -I -B personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_14/scripts/comprobar_entrega_4_14.py`; esperado: todas sus comprobaciones PASAN) y los controles históricos, hasta el de la 4.13, todos de una vez con `python3 -I -B personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_13/scripts/controles_historicos_4_13.py CARPETA_SALIDA`, con los resultados y las salidas de referencia que fija `personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_14/resultados/LEEME_CONTROLES_HISTORICOS_4_14.md` (cuáles son funcionales y cuáles están ligados, por diseño, a las huellas o al texto de su versión; el de la 4.13 da 83 de 89 en este árbol, y el LEEME explica por qué);
   - cualquier discrepancia entre `CONTINUIDAD.md` y lo que dicen los archivos o las pruebas.

   Si algo falla, se informa con precisión y no se corrige sin indicación.
5. Esperar la siguiente indicación de la persona responsable del proyecto. Las tareas posibles están en la sección 9 de `CONTINUIDAD.md`. Los relevos pendientes del paquete y cómo se resuelven están en su §2, punto 6.

## Reglas vigentes
- Toda la comunicación, en español claro y **en tercera persona**: la persona responsable del proyecto no recibe tratamientos de segunda persona. Hay que distinguir hechos comprobados, interpretaciones y propuestas, y explicar la jerga necesaria.
- **Opus** es el modelo principal. Fable puede usarse de forma selectiva cuando la dificultad, las consecuencias y el coste lo justifiquen, registrando el motivo y el resultado, y sin ejecutar todo el procedimiento con Fable. (Desde la 4.14) Se avisa a la persona responsable antes de cualquier uso de Fable.
- (4.14) **Verificación completa de las entradas financieras:** cada entrada se contrasta campo a campo con su fuente, la revisa un revisor distinto del extractor, y cero comprobado, dato ausente y no aplicable se distinguen. Una decisión con dinero real no se apoya en entradas sin verificar. Información financiera que falte: se busca completa en fuentes oficiales y, si hay que descargarla, se prepara un `.bat` para que la persona responsable la descargue (la IA no descarga sin permiso).
- (4.14) Limpiezas: se pueden eliminar sin preguntar temporales y copias de pruebas reproducibles, siempre que ninguna ejecución las use, se conserven el código exacto, las evidencias y los archivos únicos, y no se borren originales, fuentes ni entregables; las rutas eliminadas se registran.
- No se modifican los originales (`personaje_v2/empresas_v2/` ni los adjuntos): se trabaja sobre copias o en expedientes nuevos.
- No se cambian criterios financieros, probabilidades, rentabilidad exigida, escenarios ni conclusiones. No se rebaja ningún criterio para que algo pase. No se hace ninguna extracción masiva sin encargo expreso.
- Los encargos y prompts antiguos del paquete son documentación (sección 10 de `CONTINUIDAD.md`). No autorizan a construir, publicar, sincronizar repositorios ni ampliar el alcance.
- Un resultado que no se ha ejecutado no se presenta como ejecutado. Si un criterio no puede cumplirse, se declara el bloqueo sin darlo por terminado.
- Toda entrega nueva será un ZIP completo y versionado, con `VERSION`, registro, `CAMBIOS_ARCHIVOS.txt` y `MANIFIESTO_SHA256.txt` actualizados, y con las pruebas anteriores aprobadas. El ZIP se produce con `personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_10/scripts/empaquetar_zip.py` y se comprueba su extracción con Python y con `unzip`.
