# Registro · piloto Vidrala 2025 (entregas 4 y 4.1, 8-nov-2026)

## Encargo
«Munger v2 · contraste acotado del piloto Vidrala 2025»: cuatro cuestiones (CFO, capex, arrendamientos, adquisiciones y desinversiones) para la extracción `AR_2025.json`, seguidas hasta el dato efectivo. Sin extracción masiva, sin regenerar libros y sin tocar originales ni criterios.

## Secuencia
1. Se verificó la entrega 3.1 en una descompresión limpia: manifiesto, entorno, 114/114 y 30/30. Se identificó la diferencia con la versión prevista, la entrega 3 (informe, §0).
2. Se buscaron las fuentes:
   - **En el paquete:** no hay `texto/` ni `pdf/` de Vidrala.
   - **En el ordenador de la persona responsable:** se pidió acceso una sola vez a dos carpetas («VIDRALA SA» y «Personaje Munger»). El acceso no se concedió y no se volvió a pedir.
   - **En la web:** el entorno de trabajo no puede conectarse a vidrala.com. Las cuentas se descargaron con el navegador integrado de la aplicación de escritorio (anexo, §1). La herramienta de lectura web solo devolvía resúmenes, no texto literal, y no se usó como evidencia.
3. Se generó un texto nuevo con el conversor del proyecto y se cotejaron las 61 líneas de `AR_2025.json` (61/61). Después se ejecutó `comprobar-anio 2025` sobre una copia: solo dio los tres rechazos de ceros heredados.
4. Se contrastaron las cuatro cuestiones con el inglés y con el español, que prevalece. Cada dato se siguió por `AR_2025.json`, `fase1_decisiones.json`, `fase1_v63.json` y `historia_revision.md` hasta las celdas y fórmulas del libro evaluado. El libro se leyó en una copia, con los valores en caché.
5. Se escribió un script reproducible (35 comprobaciones) y se guardó su salida. El script se añadió a `verificar_paquete.sh` como bloque de solo lectura.
6. Se construyó el paquete de la entrega 4: la 3.1 sin cambios, más `contrastes/piloto_Vidrala_2025/`, y los archivos de continuidad e integridad actualizados. Después se verificó sobre una descompresión limpia.

## Modelos y esfuerzo
- **Opus** en todo el procedimiento, con esfuerzo alto en las interpretaciones contables (subtotales del CFO, NIIF 16 y conciliación NIC 7).
- **Fable no se usó.** Ninguna cuestión lo justificó: los cuadres son aritméticos y se demuestran con el documento; la única cuestión abierta (el principal de arrendamientos) no depende de razonar mejor, sino de evidencia que no está en el documento.
- **No se usaron subagentes.**

## Qué no se hizo y por qué
- **No se regeneró ningún libro ni se calculó el efecto en las valoraciones.** El encargo lo excluye (§7). Queda como PE1.
- **No se escribió `fase1_decisiones.json` ni se confirmaron ceros.** La decisión 7 lo reserva a una persona.
- **No se modificó ningún archivo de `personaje_v2/`.** Las comprobaciones se hicieron sobre copias.
- **Entrega 4:** el PDF español (13,5 MB) no se incluyó; quedó identificado por URL y SHA-256, y su extracto de dos páginas tiene huella propia. **Se incorpora en la 4.1** (ver más abajo).

## Cambios del paquete respecto a la entrega 3.1
- **Modificados (4):** `CONTINUIDAD.md`, `PROMPT_NUEVA_VENTANA.md`, `VERSION` y `verificar_paquete.sh`. Este último gana un bloque de solo lectura que ejecuta el contraste y compara su salida.
- **Nuevos (10):** los archivos de `contrastes/piloto_Vidrala_2025/`.
- **Se regeneran:** `CAMBIOS_ARCHIVOS.txt`, que sigue siendo respecto a la base, y `MANIFIESTO_SHA256.txt`.
- **Sin cambios:** `personaje_v2/`, `v6/`, `kit_pipeline_munger/` y `documentacion_reparacion/`.

## Entrega 4.1 · precisiones de cierre (8-nov-2026, 19:13)

**Indicación de la persona responsable.** Una revisión independiente respalda el hallazgo del circulante y los cuadres del piloto. Antes del cierre documental solo hay que hacer tres ajustes, sin cambios en extracciones, decisiones humanas, libros, escenarios ni código. H1–H3 permanece cerrado.

| Precisión | Qué se hizo |
|---|---|
| 1. Arrendamientos | Se sustituyeron «rango demostrable» y «caso extremo demostrable» (informe) y «opción conservadora» (correcciones) por una **sensibilidad condicionada**: cada valor (C49 = 4,5 y 6,8) lleva el supuesto del que depende y la advertencia de que no son límites ni validan el principal ni su clasificación. La falta de contraste de los datos de 2023 queda a la vista en el informe, el anexo y las correcciones. Los archivos tocados son el informe (tabla y §2, 4.3), el anexo (§3) y las correcciones (P3) |
| 2. Fuente española | El PDF completo (doc. 2308) se trasladó desde el navegador en 72 tramos y se reconstruyó. Su SHA-256 `29fd6a29…698f14e7` coincide con el del navegador y con el que obtuvo la revisión externa. Está en `fuentes/es_2308_descarga_2026-11-08/`. El extracto D4 se contrastó con él mediante pdftotext: mismas cifras (anexo, §2) |
| 3. Estado del hallazgo | El informe (tabla, §2 4.1 y §3), las correcciones (P1 y PE7, nueva) y `CONTINUIDAD.md` separan tres cosas: (a) la corrección documentalmente respaldada, 84,994; (b) su aplicación, pendiente; (c) la revisión financiera necesaria antes de llevar a conclusiones de valoración una `f` negativa. Se retiró «empuja al alza los tres escenarios», y el «≈70 mm» se presenta como magnitud aritmética de un término de la fórmula, no como efecto en la valoración |

**Lo que no cambia.** El script del piloto y su salida de referencia (35 comprobaciones), `personaje_v2/`, las extracciones, las decisiones, los libros y `verificar_paquete.sh`. Este último conserva en su comentario de cabecera la mención «entrega 4»: es inocua y no se toca para no cambiar código.

**Cambios del paquete respecto a la entrega 4:**
- **Modificados:** `VERSION`, `CONTINUIDAD.md`, `PROMPT_NUEVA_VENTANA.md` y, en `contrastes/piloto_Vidrala_2025/`, `INFORME_PILOTO_Vidrala_2025.md`, `DOCUMENTOS_Y_FUENTES.md`, `ANEXO_REPRODUCIBLE.md`, `CORRECCIONES_PROPUESTAS_Y_PENDIENTES.md` y este registro.
- **Nuevo:** el PDF español completo.
- **Se regeneran:** `CAMBIOS_ARCHIVOS.txt` y `MANIFIESTO_SHA256.txt`.

## Archivos de este expediente
| Archivo | Contenido |
|---|---|
| `INFORME_PILOTO_Vidrala_2025.md` | Informe principal: resultado de las cuatro cuestiones |
| `DOCUMENTOS_Y_FUENTES.md` | Documentos D1–D6 y fuentes ausentes F1–F4 |
| `ANEXO_REPRODUCIBLE.md` | Obtención de las fuentes, reproducción, cálculos y páginas |
| `CORRECCIONES_PROPUESTAS_Y_PENDIENTES.md` | P1–P6 y PE1–PE6 |
| `scripts/contraste_vidrala_2025.py` | Script de solo lectura |
| `resultados/contraste_salida.txt` | Salida de referencia del script |
| `fuentes/` | D1 (PDF en inglés), D2 (texto nuevo), D3 (PDF en español, desde la 4.1) y D4 (extracto español) |
