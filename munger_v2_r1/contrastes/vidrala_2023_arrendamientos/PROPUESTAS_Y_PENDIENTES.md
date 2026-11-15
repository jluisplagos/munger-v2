# Propuestas y pendientes · contraste 2023 y arrendamientos (entrega 4.2)

Son **propuestas**: no se ha aplicado ninguna. No se ha tocado `personaje_v2/empresas_v2/`, ni las extracciones, ni `fase1_decisiones.json`, ni los libros. La numeración sigue la del piloto (P1–P6 y PE1–PE7, en `contrastes/piloto_Vidrala_2025/`).

**Lo que sigue vigente del piloto:** P1 (circulante de 2024, 84,994, aplicación pendiente) y PE7 (revisión financiera de una `f` negativa).

## Propuestas

### P7 · Circulante de 2023 (decisión de la persona responsable, dentro de la revisión financiera)
- **Hecho.** 78,805 (vigente) incluye 11,061 de ajustes no monetarios de Italia trasladados a «Otros activos y pasivos…». 89,866 (informe de 2023) es la variación del circulante con un perímetro que incluye a Italia. No se publica la de las operaciones continuadas.
- **Opciones,** sin recomendación, porque es una decisión de perímetro:
  - **a)** mantener 78,805 y anotar que contiene la reclasificación;
  - **b)** fijar 89,866 con su fuente en un expediente nuevo (tipo B del contrato) y anotar que su perímetro es el consolidado con Italia;
  - **c)** revisar el perímetro de toda la columna 2023 (ventas, EBIT y D&A de continuadas frente a CFO, capex y circulante consolidados) antes de elegir.
- **Efecto aritmético** (réplicas del anexo): `f` se desplaza unas 0,0025 entre (a) y (b).

### P8 · Página de D&A en `AR_2024.json` (tipo A; sin cambio de valor)
Las líneas de D&A de 2024 y 2023 se citan en la p. 4 y están en la p. 7 del texto nuevo. Si en algún momento se rehace el expediente, una versión nueva de `AR_2024.json` debería citar la p. 7.

### P9 · Arrendamientos (decisión de la persona responsable)
Siguen vigentes las opciones de P3 (4,5, 6,8 o búsqueda de evidencia), ahora con más información:
- **Lo que queda descartado:** que los informes 2023–2025 o el ESEF 2025 publiquen el principal, el interés pagado o la línea de flujos. No lo hacen.
- **Para conseguir la evidencia,** habría que:
  - **c1)** preguntar a Relación con Inversores de Vidrala en qué línea del estado de flujos van los pagos de arrendamientos y si «Pagos de intereses» incluye los intereses de arrendamientos;
  - **c2)** revisar el ESEF 2024. Su valor esperado es bajo: el de 2025 no tiene etiquetas de arrendamientos.
- **Riesgo de duplicación** (informe, §2): no se puede descartar en ningún sentido. C49 = 4,5 tiene que seguir presentándose como hipótesis.

### P10 · Discrepancias de los documentos (solo notas; ninguna acción en el sistema)
- Informe inglés de 2024, p. 7: en la columna de 2023, provisiones, subvenciones y gastos financieros copian la columna de 2022. Prevalece la versión española.
- Nota 8, de 2022 a 2025: los pagos del pasivo se repiten como gasto de arrendamientos a corto plazo y de poco valor.
- Bristol: la cuota de 2024 es de 387 miles £ en el informe de 2024 y de 354 miles £ en el de 2025.
- Informe de 2023, p. 7: «112,5000» en la columna de 2022.

### P11 · Verificación automática del nuevo script (decisión de la persona responsable)
Añadir a `verificar_paquete.sh` un bloque que ejecute `contraste_2023_arrendamientos.py` y compare su salida, igual que se hizo con el piloto.
- **Por qué no se ha hecho:** este encargo prohíbe cambiar código, y aunque la herramienta de verificación no es código del sistema, se ha preferido no tocarla sin indicación.
- **Mientras tanto,** el script se ejecuta como indica el anexo, §1.

## Pendientes

| # | Pendiente | Qué haría falta |
|---|---|---|
| PE8 | Valor del circulante de 2023 con el perímetro coherente con la ventana | Decisión P7, dentro de PE7. El dato de continuadas no se publica |
| PE9 | Coherencia de perímetro de la columna 2023 de la Historia: ventas 1.427,473, EBIT 267,508 y D&A 87,21 de continuadas (D7 p. 4 y 7) frente a CFO, capex y circulante consolidados (Italia: +26.732 de explotación y −28.371 de inversión) | Revisión financiera (PE7). Este encargo no valida la ventana |
| PE10 | Principal, interés pagado y clasificación de los arrendamientos de 2023 a 2025 | P9-c1 o P9-c2 |
| PE11 | Ventas, EBIT y tipo de 2023: solo se ha comprobado que proceden del comparativo reexpresado (D7 p. 4); no se han contrastado línea a línea | Encargo específico, si la revisión financiera lo requiere |
| PE12 | Traducción inglesa de 2023 (D6) frente a la española (doc. 1809, 21,6 MB, no descargada completa) | Solo si se quiere contrastar la traducción; las cifras inglesas de 2023 cuadran internamente |
| PE13 | ESEF 2025 completo (ZIP de 36 MB y XHTML de 54 MB), no conservado | Descargarlo de su URL y comprobarlo con su huella si la persona responsable lo quiere en el paquete |
| PE1 y PE7 (del piloto) | Efecto en las valoraciones y revisión financiera de una `f` negativa | Siguen abiertos. Este encargo solo prepara evidencia |
