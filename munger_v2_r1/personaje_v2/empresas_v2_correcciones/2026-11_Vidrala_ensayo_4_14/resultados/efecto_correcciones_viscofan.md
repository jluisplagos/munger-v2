# Viscofan · efecto mecánico de las correcciones de entradas (rama 4.14)

**Qué es.** Copias del libro evaluado 4.13 congelado con las fases A, B y C fijas, en las que se escriben los datos corregidos en la rama (por grupo y todos juntos) y, aparte, las opciones de las decisiones pendientes; recalculadas con LibreOffice. Mide el efecto de los DATOS con todo lo demás fijo. **No es la valoración de la rama** (que rehace las fases con agentes reales) y **ninguna decisión se adopta**.

**Reproducción del caso activo:** sí (precio de Sí 40,16401 frente a 40,16401 de precio.json).

**Celdas de entradas que cambian en la rama:** 15.

| Caso | Celdas (antes → después) | Precio de Sí | Δ frente a la activa 4.13 | Δ frente a la rama (todas las correcciones) | Ponderado | Zona |
|---|---|---|---|---|---|---|
| activa 4.13 (reproducción) | — | 40,16401 | 0,00000 | — | 44,223 | caro |
| corrección · Historia fila 13 | H!G13 — → 0,000 | 40,16401 | 0,00000 | — | 44,223 | caro |
| corrección · Historia fila 14 | H!F14 -12,134 → -6,135; H!G14 19,349 → 25,178; H!J14 83,032 → 90,646; H!K14 15,452 → 8,862; H!L14 53,222 → 49,933 | 40,16845 | 0,00444 | — | 44,229 | caro |
| corrección · Historia fila 22 | H!D22 82,794 → 93,698 | 40,16401 | 0,00000 | — | 44,223 | caro |
| corrección · Historia fila 25 | H!F25 33,294 → 29,995; H!G25 37,871 → 28,204; H!H25 29,133 → 24,779; H!J25 25,916 → 17,266; H!K25 19,145 → 16,498; H!L25 20,989 → 14,878 | 40,29838 | 0,13437 | — | 44,358 | caro |
| corrección · Historia fila 26 | H!H26 0,000 → —; H!I26 0,000 → — | 40,16401 | 0,00000 | — | 44,223 | caro |
| TODAS las correcciones de la rama | H!D22 82,794 → 93,698; H!F14 -12,134 → -6,135; H!F25 33,294 → 29,995; H!G13 — → 0,000; H!G14 19,349 → 25,178; H!G25 37,871 → 28,204; H!H25 29,133 → 24,779; H!H26 0,000 → —; H!I26 0,000 → —; H!J14 83,032 → 90,646; H!J25 25,916 → 17,266; H!K14 15,452 → 8,862; H!K25 19,145 → 16,498; H!L14 53,222 → 49,933; H!L25 20,989 → 14,878 | 40,30282 | 0,13881 | — | 44,363 | caro |
| decisión (no adoptada) · D3/E5 · acciones en circulación a 31-dic-2025 (E fijo) · sobre la activa | A!C55 45,479 → 45,993 | 39,71499 | -0,44902 | — | 43,729 | caro |
| decisión (no adoptada) · D3/E5 · acciones en circulación a 31-dic-2025 (E fijo) · con todas las correcciones | A!C55 45,479 → 45,993 | 39,85225 | -0,31176 | -0,45057 | 43,867 | caro |
| decisión (no adoptada) · E1 · medias exactas C47–C50 (sin el redondeo del inversor) · sobre la activa | A!C47 77,500 → 77,533; A!C48 8,300 → 8,294; A!C49 5,500 → 5,547; A!C50 3,710 → 3,707 | 40,16401 | 0,00000 | — | 44,223 | caro |
| decisión (no adoptada) · E1 · medias exactas C47–C50 (sin el redondeo del inversor) · con todas las correcciones | A!C47 77,500 → 77,533; A!C48 8,300 → 8,294; A!C49 5,500 → 5,547; A!C50 3,710 → 3,707 | 40,30282 | 0,13881 | 0,00000 | 44,363 | caro |
