# Correcciones propuestas y pendientes · piloto Vidrala 2025

Todo lo que sigue son **propuestas**. No se ha aplicado ninguna:
- no se ha tocado `personaje_v2/empresas_v2/` ni ninguna extracción;
- no se ha escrito `fase1_decisiones.json`, que solo puede escribir una persona;
- no se ha regenerado ningún libro.

Cada propuesta indica quién tendría que decidirla.

## Correcciones propuestas

### P1 · Circulante de 2024 (prioridad alta: el dato vigente entra en el cálculo)

Estado, en tres partes separadas:
- **a) Corrección documentalmente respaldada:** 84,994 mm.
- **b) Aplicación:** pendiente. Es esta propuesta.
- **c) Revisión financiera:** necesaria antes de llevar a conclusiones de valoración la `f` negativa que resultaría (PE7).

- **Qué.** El aumento del circulante de 2024 (Historia K14) debe ser **84,994 mm** y no −127,840.
- **Por qué.** La versión española (D3, PDF p. 14) imprime «(106.417)». Con ese signo, las cinco líneas suman el subtotal impreso (84.994). El propio informe de 2024 (`AR_2024.json`) daba también 84,994.
- **Cómo, según el contrato (§1, tipo B, «cifra incorrecta»).** Una persona fija la cifra con su fuente en `fase1_decisiones.json` de un **expediente nuevo**, con la clave de la serie `circulante_lineas`. Por ejemplo, para que la persona lo revise y lo complete:

  ```json
  "circulante_lineas": {"2024": {"valor_mm": 84.994,
     "fuente": "CF_2025 versión española (doc. 2308) PDF p.14: «Otros activos y pasivos corrientes y no corrientes (106.417)», «Efectivo generado por las operaciones (84.994)»; coincide con AR_2024.json (CF_2024.txt p.7)",
     "fecha": "AAAA-MM-DD", "confirmado_por": "<persona>"}}
  ```

  En `fase1_historia.py`, `valor_mm` sustituye directamente el valor de la serie, que ya va con el signo de la plantilla: positivo = consume caja.
- **Después.** Ejecutar `construir` en ese expediente y comprobar que la Historia solo cambia en K14 (y en las filas 30, 31 y en C53, C58 y C76, que se calculan a partir de ella). **Antes de llevar el resultado a conclusiones,** hacer la revisión financiera de PE7. Después, recalcular el libro y revisar las fases A a C; la fase A citó «f = 0,020 está en rango» para elegir el motor A.
- **Alternativa de tipo A** (corregir el respaldo, no la cifra). Una versión nueva de `AR_2025.json` con `"signo": -1` en ese componente. Funciona, pero depende de que el lector acepte un paréntesis sin cerrar, así que se desaconseja.

### P2 · Detección del signo perdido (sistema; requiere un encargo, porque toca código de H1 y la limitación L4)

- **a)** Que `numero()` rechace los paréntesis desequilibrados («106,417)»), para que `comprobar-anio` lo señale.
- **b)** Que una diferencia grande entre el informe de un año y el comparativo del siguiente deje de ser un aviso en `historia_revision.md` y exija una decisión humana antes de `construir`, al menos cuando cambia el signo o supera un umbral.

No se implementa sin indicación.

### P3 · Arrendamientos (decisión de la persona responsable)

- **Historia fila 17.** Tiene el rótulo «principal» pero contiene el **pago total** (principal + intereses). No afecta al motor; solo a la fila 35, que es informativa. Hay dos opciones:
  - dejar constancia en la nota de la fila de que no es principal;
  - o, si se obtiene evidencia (P3-c), sustituirla por el principal.
- **`Análisis C49 = 4,5`.** Es una aproximación: pagos − gasto devengado, con la media de 2023 a 2025. Hay tres opciones:
  - **a)** mantenerla como **hipótesis declarada**, con la condición de que el interés pagado sea igual al devengado y esté dentro de «Interest paid» (explotación);
  - **b)** usar el pago total, 6,8. Supone que todo el pago, intereses incluidos, está fuera del CFO; con ese supuesto, el FCF base sería 158,9 y `f` 0,021430. Es una sensibilidad condicionada, no un límite;
  - **c)** buscar evidencia del interés pagado por arrendamientos y de su línea en el estado de flujos, por ejemplo en las etiquetas ESEF del paquete consolidado (doc. 2311 o 2305) o con una consulta a Vidrala.

  Lo que no procede es presentar 4,5 como «Rellenado y verificado» sin esa salvedad. Ni 4,5 ni 6,8 acotan el valor correcto ni validan el principal o su clasificación. Además, las dos medias incluyen datos de 2023 sin contrastar (pagos de 5,861 y devengado de 2,131; F2).

### P4 · Cero heredado de `intereses_financiacion` 2025 (revisión humana, paso 4 del contrato)

- **Evidencia para la persona que revise:** en D1 p. 7, «Interest paid (20,800) (32,100)» está en el bloque de explotación, y el bloque de financiación no tiene ninguna línea de intereses. El script lo comprueba.
- **Cita literal candidata, en la página 7:** «Interest paid (20,800) (32,100)».
- La IA **no** confirma el cero. Los otros dos ceros heredados de 2025 (`otros_activos_financieros` y `minoritarios`) están fuera de las cuatro cuestiones.

### P5 · Notas de los lectores (documentación; sin efecto en el cálculo)

- **CFO 2025 y 2024:** sustituir «el subtotal impreso no cuadra… erratas» por la explicación correcta: 224.195 y 240.195 son la suma de los ajustes, y el CFO cuadra.
- **Adquisiciones 2024:** quitar «Dudoso si 'Other effects of disposal' pertenece a la venta». El rótulo español, «Otros efectos enajenación», lo confirma.
- **Capex:** citar el rótulo español, que prevalece, en lugar del inglés erróneo.

### P6 · Participadas por puesta en equivalencia (criterio; decisión de la persona responsable)

La exclusión de los 6.000 de 2024 es coherente con la convención «negocios/dependientes». Si la persona responsable prefiere contar las compras de participadas como adquisición, el cambio es de criterio, no de dato, y solo afectaría al ancla S2C, no a la valoración.

## Pendientes

| # | Pendiente | Qué haría falta |
|---|---|---|
| PE1 | Efecto de P1 en los valores MALO, NORMAL y BUENO, en el precio de Sí y en el cubo | P1 decidida, PE7 hecha, expediente nuevo, `construir`, recálculo con LibreOffice y revisión de las fases A a C. No se hace sin encargo |
| PE7 | **Revisión financiera de una `f` negativa** antes de sacar conclusiones de valoración. Con el dato corregido, el FCF base (161,2) superaría al flujo operativo implícito de la ventana (119,96), y `f` = −0,0276 se proyectaría como porcentaje constante de las ventas | Juicio de la persona responsable sobre: el significado económico de esa diferencia; la ventana 2023–2025 y sus datos de 2023 sin contrastar (PE4, PE5); y si se mantiene el motor A |
| PE2 | Principal de arrendamientos (4.3) | P3-c o una decisión P3-a/b |
| PE3 | Identidad byte a byte del `CF_2025.txt` original (F1) | El archivo original, o su PDF, si está en el ordenador de la persona responsable |
| PE4 | Datos de 2023 que entran en las medias de `Análisis` (CFO, capex, pagos y devengado de arrendamientos) | El informe 2024 (F2) |
| PE5 | **Candidato para el siguiente contraste (interpretación):** `historia_revision.md` registra otras diferencias de circulante entre el informe y el comparativo siguiente (2022: 117,709 → 117,546; 2023: 89,866 → 78,805). La de 2023 entra en la ventana de `f`. No se ha investigado porque está fuera del alcance del piloto | Los informes 2023 y 2024 |
| PE6 | Discrepancias del propio documento: rótulos ingleses del capex; paréntesis omitido en 2024; la misma cifra de pagos de arrendamientos repetida como gasto a corto plazo en las dos versiones; «at 1 December» en el saldo inicial de caja; conciliación NIC 7 sin movimientos no monetarios | Ninguna acción en el sistema, más allá de las notas de P5. Solo podría aclararlas Vidrala |
