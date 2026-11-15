# Verificación de las entradas financieras · cobertura real (14-nov-2026, 12:00)

Comprobador `verificacion_entradas.py` de la instantánea i4 sobre los registros revisados. Extractores y revisores son agentes Claude con contextos separados (el revisor no ve el contexto del extractor). **No son revisiones humanas.** Ninguna celda se ha corregido todavía en los libros: esto mide el estado, no lo arregla.

## 1. Resumen

| | Viscofan | Vidrala |
|---|---|---|
| Universo (celdas de entradas económicas del libro) | 232 | 226 |
| **Verificadas por el revisor y vigentes** | **210** | **219** |
| Datos de origen auxiliares («aux:») | 102 | 119 |
| Discrepancias | 21 | 6 |
| Pendientes | 1 (C41, porque depende de C55) | 4 (C48, J14, K14, K13) |
| Errores del contrato / desactualizadas | 0 / 0 | 0 / 0 |
| **Apto por entradas** | **no** | **no** |

«Apto por entradas» es condición necesaria, no suficiente: aunque lo fuera, la entrega seguiría siendo experimental y no apta para dinero real.

## 2. Lo que puede mover el valor (motor B) · hechos de la fuente y estimaciones lineales sin recalcular el libro

| Empresa | Celda | Libro | Según la fuente | Efecto estimado | Qué hace falta |
|---|---|---|---|---|---|
| Viscofan | L25 pensiones 2025 | 20,989 | 14,878 (prestación definida, AR_2025 p. 87; la línea del balance suma 6,111 de otras retribuciones) | ≈ +0,13 €/acción | corrección del dato en la rama 4.14 |
| Viscofan | C55 acciones | 45,479209 (media ponderada diluida 2025, menor que la básica) | 45,993399 en circulación a 31-dic-2025 (46,5 M emitidas − 506.601 propias) | ≈ −0,49 €/acción | **decisión D3**, pendiente |
| Vidrala | K14 circulante 2024 | 84,994 | la fuente no publica el circulante limpio; ≈50 mm podrían ser la plusvalía de la venta de Italia (inferencia del revisor) | hasta ≈ −0,8 €/acción (cota grosera) | investigar la nota de la venta; decisión de tratamiento |
| Vidrala | K13 adquisiciones 2024 | −241,668 | alternativas −230,000 / −224,000 / −235,668 | hasta ≈ 0,25 €/acción | ídem |
| Vidrala | C48 intereses (y sus tres «aux») | 0 en financiación | no hay línea; el interés de arrendamientos (≈2,1–2,5 mil €) podría ir en pagos de deuda | ≈ −0,06 €/acción/año, solo motor A | reclasificar (derivado o ausente) |

## 3. Lo que no mueve el valor del motor B pero bloquea igual (se corrige o se reclasifica)

- **Viscofan:**
  - circulante F14, G14, J14–L14 (la fórmula suma la variación de provisiones de forma no homogénea; afecta al motor A y al S2C histórico 1,146 → ≈1,155);
  - pensiones de los demás años (mismo concepto);
  - deuda de 2017 (D22);
  - medias C47–C50 (redondeos del inversor);
  - G13 vacía frente a 0 publicado (efecto nulo).
  - Ceros inferidos (C23, D23, I26): el revisor confirma que no están impresos; tienen que reclasificarse (no aplicable o derivado por cuadre), no aceptarse aflojando el control.
- **Vidrala:**
  - C46 y C47 (redondeos, solo motor A);
  - F8 (D&A 2019 con el deterioro dentro; fuera de las ventanas de cálculo);
  - J14 (reexpresión por Italia: el revisor da dos parejas coherentes con J8, a 0,41 mm de diferencia).

## 4. Precios

- **Viscofan C37** (54,70 € del 3-nov-2026): **verificado** con el boletín oficial de la Bolsa de Madrid, p. 3, conservado con su SHA-256 (descargado por la persona responsable con `descargar_precio_viscofan.bat`).
- **Vidrala C37** (90,10 € a 31-dic-2025): **verificado** con el informe de gestión 2025, p. 97. No es el boletín de BME.
- **Elis** (24,18 € del 4-nov-2026): contrastado con el histórico oficial de Euronext, no ajustado, leído en el navegador integrado y conservado como texto y captura. Coincide con Twelve Data. Límite: es una lectura de la página, no un archivo descargado.

## 5. Mejoras del comprobador que salieron de esta ronda (i4)

- Un 0 publicado y una celda vacía ya no se dan por iguales.
- La cita tiene que contener el valor como cifra completa, no dentro de otra cifra.
- Se aceptan los ceros impresos como «-» (aislados o entre columnas), los miles separados por espacio y hasta seis decimales.
- 31/31 pruebas.

## 6. Siguiente

En las ramas 4.14 de los expedientes:
1. Corregir los datos con discrepancia confirmada y reclasificar los ceros inferidos.
2. Recalcular solo lo afectado y volver a pasar al revisor lo cambiado.
3. Lo que depende de una decisión (D3 acciones; tratamiento de K14/K13 de Vidrala) se calcula en sus dos versiones y se muestra por separado, sin adoptar nada.
