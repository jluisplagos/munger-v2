# Registro de ejecución y cambios · entrega 4.2 (8-nov-2026)

## Encargo
«Munger v2 · contraste de datos de 2023 y arrendamientos de Vidrala». Tiene dos objetivos:
1. contrastar los datos de 2023 que alimentan las medias de `Análisis` y el circulante de la ventana;
2. buscar evidencia sobre el tratamiento de los arrendamientos de 2023 a 2025.

No incluye aplicar correcciones ni regenerar libros.

## Ejecución
1. **Comprobación inicial.** SHA-256 de la 4.1 (`85198c54…`): coincide. Se revisaron `VERSION`, `REGISTRO_IMPLEMENTACION_H1-H3.md`, `REGISTRO_PILOTO.md` y los documentos de la 4.1. El paquete de trabajo se construyó sobre una descompresión de la 4.1.
2. **Extracciones.** Se leyeron `AR_2023.json` y `AR_2024.json` para las partidas del encargo. Se detectó que la diferencia de 11,061 en el circulante de 2023 está entera en «Other current liabilities».
3. **Fuentes.**
   - Se listaron los documentos 2023 y 2024 del centro de resultados.
   - Se descargaron en el navegador integrado y se trasladaron por tramos: el inglés 2024, el inglés 2023 y el español 2024.
   - Se abrió el ESEF 2025 en el navegador.
   - El español 2023 y el ESEF 2024 quedaron identificados por URL y huella, sin usarse.
4. **Textos nuevos** con `pdf_a_texto.py`. Cotejo de las líneas citadas: 56 de 56 en 2023 y 49 de 51 en 2024 (2 de D&A con la página mal atribuida). `comprobar-anio` sobre una copia, que no cambió.
5. **Contraste.**
   - CFO y capex de 2023.
   - El circulante de 2023: reexpresión por Italia, con la traducción inglesa errónea y la española correcta.
   - Arrendamientos de 2022 a 2025: notas 8 y 16, conciliaciones NIC 7, ESEF y Bristol.
6. **Script reproducible** de 45 comprobaciones, su salida de referencia y los documentos de esta carpeta.
7. **Paquete 4.2:** `VERSION`, `CONTINUIDAD.md`, `PROMPT_NUEVA_VENTANA.md`, `CAMBIOS_ARCHIVOS.txt` y el manifiesto. Después, la verificación sobre una descompresión limpia (sección siguiente).

## Comprobado directamente en esta sesión
- Las huellas de D6, D7, D9 y del ZIP del ESEF y sus miembros, en el navegador y tras la reconstrucción.
- Todas las cifras y cuadres del informe y el anexo, mediante el script (45 comprobaciones).
- `comprobar-anio` 2023 y 2024 sobre una copia.
- La batería del piloto (35), sin diferencias.
- La verificación completa del paquete, sobre una descompresión limpia: manifiesto, entorno, piloto, 114/114 y 30/30. Los originales conservan el SHA-256 de la base.

## Antecedentes revisados externamente (no repetidos aquí)
- La revisión independiente del cierre documental de la 4.1, según indica la persona responsable.
- La huella del PDF español 2025 (`29fd6a29…`), obtenida también en la revisión externa, según la persona responsable.

## No comprobado
- La identidad byte a byte de los `CF_2023.txt` y `CF_2024.txt` originales.
- Ventas, EBIT y tipo de 2023, línea a línea.
- La traducción inglesa de 2023 frente a la española.
- El ESEF 2024.
- El ESEF 2025 completo (no conservado; ver `DOCUMENTOS_Y_FUENTES.md`).

## Modelos
- **Opus** en todo el procedimiento, con esfuerzo alto en las interpretaciones contables: reexpresión NIIF 5, NIIF 16 y NIC 7.
- **Fable no se usó.** Ninguna cuestión lo justificaba: la diferencia de 2023 se resolvió con aritmética y con la nota de Italia, y las preguntas de arrendamientos no avanzan con mejor razonamiento, sino con evidencia que los documentos no contienen.
- **No se usaron subagentes.**

## Cambios del paquete respecto a la 4.1
- **Nuevos:** `contrastes/vidrala_2023_arrendamientos/`, con los documentos, el script, la salida de referencia, las fuentes (D6, D7, D9 y el extracto del ESEF) y los textos nuevos.
- **Modificados:** `VERSION`, `CONTINUIDAD.md` y `PROMPT_NUEVA_VENTANA.md`.
- **Se regeneran:** `CAMBIOS_ARCHIVOS.txt` (respecto a la base) y `MANIFIESTO_SHA256.txt`.
- **Sin cambios:** `personaje_v2/` (originales, extracciones, decisiones, libros, código), `contrastes/piloto_Vidrala_2025/`, `v6/`, `kit_pipeline_munger/`, `documentacion_reparacion/` y `verificar_paquete.sh`.
