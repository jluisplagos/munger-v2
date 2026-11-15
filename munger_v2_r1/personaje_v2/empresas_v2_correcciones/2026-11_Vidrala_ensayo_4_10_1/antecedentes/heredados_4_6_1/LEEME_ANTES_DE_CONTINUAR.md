# Expediente del ensayo de Vidrala regenerado con la vigencia de las salidas oficiales (entrega 4.6.1)

**Origen.** Es una copia del expediente aprobado de la 4.6, con su resumen (`../../2026-11_Vidrala_ensayo_4_6/`, que se conserva intacto). Los datos, el registro humano de P1, las fases y todos los números son los de la 4.6.

**Cómo se regeneró:**
1. Al relanzar el pipeline con el código 4.6.1, las salidas oficiales de la 4.6 se archivaron en `historial_cierres/01_74b94f8072dd58c1/` (con `RETIRADA.json`). No había una aprobación válida en el expediente, porque la auditoría 4.6 se conserva aparte como `auditoria_4_6_antecedente.md`, sin cambios.
2. La fila del resumen pasó a «SIN APROBACIÓN VIGENTE», y la anterior se conservó en `../resumen_v2_historial.csv`.
3. Una auditoría nueva e independiente aprobó el material `74b94f8072dd58c1`, idéntico al de la 4.6.
4. Solo entonces el paso 14 escribió `ficha.json`, `informe.md` y `cierre_vigente.json`, que liga ambas salidas a esa aprobación.

**Otros antecedentes conservados:**
- `auditoria_4_5_antecedente.md`;
- `auditoria_4_6_primera_material_305c3a5b.md`;
- `ficha.json.anterior` e `informe.md.anterior` (la 4.5).

**Alcance.** Son resultados **mecánicos de un ensayo exploratorio**. No son una comparación válida con el precio de noviembre de 2026 ni una recomendación. Ver `../INFORME_REPARACION_4_6_1.md`.
