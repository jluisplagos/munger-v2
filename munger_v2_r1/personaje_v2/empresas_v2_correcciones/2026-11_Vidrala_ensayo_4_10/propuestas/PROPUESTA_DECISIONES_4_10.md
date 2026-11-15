# Propuesta única de decisiones · entrega 4.10

**Para:** la persona responsable del proyecto.

**Qué es.** Todas las decisiones abiertas por la 4.10, agrupadas en un solo documento. Las cifras salen de `variantes/variantes_4_10.json` y de `INFORME_FINANCIERO_4_10.md`.

**Cómo leerla.**
- Cada decisión indica si es una **corrección factual** (un dato publicado sustituye a otro) o un **juicio o convención** (no hay un dato que la resuelva).
- La IA no rellena ninguna firma ni decisión: los campos humanos están en `decisiones_4_10.json`, vacíos.
- Las variantes y la copia exploratoria pueden usarse sin registrar las 38 confirmaciones de N4.

**Efectos.** Van en € por acción sobre el ponderado (P) y el precio de Sí (S) de la referencia: P 70,495154 y S 65,688087.

## A · Correcciones factuales

**A1 · D-N7, denominador: acciones en circulación a 31-dic-2025.**
- **Recomendación:** adoptar N = 35,182858.
- **Evidencia:** 35.206.258 emitidas menos 23.400 de autocartera (nota 14(k), ES 2025, pág. PDF 67). Lo confirma el dividendo a cuenta: 43.338.244,48 € ÷ 1,2318 €.
- **Alternativa:** 35,206, las emitidas, que hoy usa la referencia (la media ponderada anual es otro concepto).
- **Efecto:** +0,0463 en P si es solo el denominador; −0,0287 junto con A2.
- **Si no se adopta,** las acciones propias, que no tienen derechos, siguen en el denominador.

**A2 · D-N6, fecha de E.**
- **Recomendación:** E = precio de cierre de 2025 × N = 90,10 × 35,182858 = 3.169,976.
- **Evidencia:** Informe de gestión de 2025, pág. PDF 97 («cerró 2025 en 90,10 euros»).
- **Comprobación pendiente:** el dato procede del informe que la empresa deposita en la CNMV. No se ha contrastado con el boletín de BME; si se exige el boletín, la decisión queda condicionada.
- **Alternativa:** 87,90 × 35,206 = 3.094,6, que mezcla el precio de noviembre de 2026 con las acciones de 2025.
- **Efecto:** con N fija, −0,077 en P y −0,069 en S (r_op pasa de 0,086922 a 0,086992).
- **Si no se adopta,** la tasa operativa sigue dependiendo de un precio posterior a la fecha de valoración.

**A3 · D-N4-OAF, definición de «otros activos financieros».**
- **Recomendación:** fijar el texto de la lectura estrecha en `prompts/historia_anio.md`: depósitos a plazo e inversiones financieras temporales líquidas; excluye derivados, deudores, impuestos, otros activos operativos y activos no corrientes. Es una corrección de la especificación, no un cambio de criterio de caja.
- **Evidencia:** el propio texto entre paréntesis y la convención de `metadatos_fase1.md`; los derivados corrientes de cada año están en el informe financiero §1.
- **Alternativas:**
  - lectura amplia, que da derivados en 9 de 10 años y exigiría tratarlos en neto con los pasivos derivados;
  - una partida propia de derivados, fuera de la caja.
- **Efecto:** nulo mientras `caja_incluye_otros_activos_financieros = false`.
- **Si no se adopta,** 9 entradas siguen dependiendo de la definición.

**A4 · D-N4-reg revisada, registro de ceros.**
- **Recomendación:** si la persona responsable lo decide, registrar en `fase1_decisiones.json` (valor 0, fuente con página, fecha y persona) primero las **18 de evidencia completa**.
- Las **8 parciales** (intereses de 2018–2025), solo con la nota de que el componente de arrendamientos no está acreditado. La firma no lo sustituye.
- Las **9 dependientes de la definición**, después de A3.
- Las **3 no aplicables**, según D-N4-na.
- **Efecto:** ninguno en la valoración.
- **Si no se adopta,** siguen «Dato no verificable» en el libro y pendientes en el pipeline.

## B · Juicios y convenciones

**B1 · D-N8, base de derechos.**
- **Recomendación:** mantener la base con derecho a 31-dic-2025 (la referencia: la caja contiene el dividendo pagado el 13-feb-2026) y publicar siempre al lado el valor sin derecho, restando la obligación una sola vez.
- **Efecto del valor sin derecho:** −1,230983 en todos los valores con N = 35,206, o −1,231793 con A1.
- El complementario (16,490, propuesto) no se resta en ninguna de las dos.
- **Alternativa:** valorar sin derecho como base.
- **Si no se decide,** cada comparación con un precio tiene que decir si el precio lleva el derecho.

**B2 · D-N5, pensiones.**
- **Recomendación:** mantener 6,223 bruto (la provisión «Personal» completa) hasta tener el desglose de la obligación, los activos del plan y las otras obligaciones.
- **Alternativas:**
  - [Hipótesis] neto de un 25 % de impuesto: +0,0442;
  - solo el componente de prestación definida: no separable.
- No se pone 0.
- **Si no se adopta otra cosa,** sigue siendo la opción conservadora.

**B3 · D-P3, representación de C48 y C49** (con D-N4-C48 de la 4.9).
- **Recomendación:** mantener la situación A como referencia (C48 = 0, C49 = 4,5) y marcarla como condicionada a la línea de flujos de los intereses de arrendamientos (Q-N4a, no enviada).
- **Alternativa B:** C48 = 2,254 con C49 = 4,5, o C48 = 0 con C49 = 4,5 + 2,254 = 6,754, que son equivalentes. Con P = 4,510, P+I sería 6,764; la diferencia de 0,010 es el redondeo de C49.
- **Efecto:** nulo en la valoración del motor B. El FCF base baja 2,254 y `f` pasa de −0,0276 a −0,0261.
- **Nunca** C49 = P+I con los intereses dentro del CFO, ni C48 = 21,740.
- La discrepancia de la nota 8 sigue abierta.

**B4 · D-N6-τ, impuesto del escudo de la deuda.**
- **Recomendación:** mantener τ = 0,20032, la media de cinco años, que es la misma del motor.
- **Alternativa:** el tipo efectivo de 2025 (0,2433): +0,155 en P respecto a la referencia (+0,232 respecto a A2). No es representable sin cambiar la fórmula de r_op, porque la plantilla usa un solo τ.
- **Si no se adopta,** no cambia nada.

**B5 · D-N10, probabilidades.**
- **Recomendación:** conservar 0,2 / 0,6 / 0,2 como convención declarada, y pedir que la fase B de la próxima ejecución del personaje justifique el fundamento conjunto (ventas, energía y precio, margen, capital, mantenimiento y ejecución), no solo la frecuencia de márgenes.
- **Mostrar siempre** la sensibilidad de pesos y la historia adversa: el MALO adverso da P 68,56 y S 61,53; con 0,3 / 0,5 / 0,2, P 65,88 y S 57,66.
- **Sin cambio de pesos.**

**B6 · D-PN1, sentidos de «favorable»** (ver `ACLARACION_PN1_4_10.md`).
- **Recomendación:** no cambiar ningún criterio y usar dos términos distintos en la documentación: «conclusión con objetivo» (S-19: comprar, o esperar con precio objetivo) y «conclusión de compra» (D10: comprar).
- **Alternativa,** como cambio de criterio que se propone aparte: que D10 limite también «esperar con objetivo». Es más estricto y llevaría a `pendiente_de_investigacion` los cierres «esperar» con hipótesis sin fundamento.
- Igualar S-19 a D10 reduciría bloqueos y no se propone.

## C · Siguen igual (sin cambios en la 4.10)

- P-M1 abierta, con D-N3b, D-N3c, D-N3d y D-N3e, Q-ROIC1 y Q-E1 a Q-E7.
- D-RV1a a D-RV1c, D-AUT y Q-T1 a Q-T6.
- D-N4-na.

La especificación para integrar N1–N3 y P-M1 está en `ESPECIFICACION_INTEGRACION_4_10.md`.

**Siguiente hito propuesto.**
1. Que la persona responsable decida A1, A2 y B1.
2. Con eso, ejecutar de nuevo el personaje en el expediente exploratorio (pasos 5–14, con una auditoría nueva del material actual), si encarga actualizar la oportunidad.
