# Diferencias entre el piloto 4.11 y el código final

Piloto: `personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_11/piloto` (no se ha modificado: sí, intacto; 247 archivos). Las salidas del código final se regeneraron en una copia temporal, como material provisional (sin vigencia ni archivo).

## Selección

- **Diferencia:** la versión de la configuración del pipeline: el piloto registró 0.2.2+v64exp.1 y el código final usa 0.2.2+v64exp.2; las tres huellas coinciden, así que la selección se acredita (la versión no forma parte de la comprobación).
- Piloto: `{"version": "V6.4 experimental", "config": "config_v2_v64_experimental.json", "version_config": "0.2.2+v64exp.1", "archivo_sha256": "04bab281d2a1a4b236e9714e069c9ade8a9c7d467f090b7ce435cce0040d9bef", "referencia_sha256": "8ee7ef7ed4d74962a005265e0e8056dfae7b29cb35dbdadf5a5b3ccadbec0281", "verificador_sha256": "944346fe1ed5e4fa632ac6f1f58912c0ad21821be29927e23b28bd08255dc150"}`
- Código final: `{"version": "V6.4 experimental", "config": "config_v2_v64_experimental.json", "version_config": "0.2.2+v64exp.2", "archivo_sha256": "04bab281d2a1a4b236e9714e069c9ade8a9c7d467f090b7ce435cce0040d9bef", "referencia_sha256": "8ee7ef7ed4d74962a005265e0e8056dfae7b29cb35dbdadf5a5b3ccadbec0281", "verificador_sha256": "944346fe1ed5e4fa632ac6f1f58912c0ad21821be29927e23b28bd08255dc150"}`

## Nombre del resumen

- **Diferencia:** el piloto publicó su fila en resumen_v2.csv (antes de la corrección H2 de la revisión interna 4.11) y el registro guarda la ruta absoluta del árbol de desarrollo de la 4.11; el código final publica las filas V6.4 en resumen_v2_v64_experimental.csv junto al expediente.
- Piloto: `["/home/claude/trabajo/munger_v2_r1/personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_11/piloto/resumen_v2.csv"]`
- Código final: `"personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_11/piloto/resumen_v2_v64_experimental.csv"`

## Marca provisional en la primera línea del informe

- **Diferencia:** el informe del piloto se escribió antes de la corrección H7: no marca el objetivo como provisional en la línea de estado; el código final sí, con las hipótesis que lo condicionan (Anexo B §B.6.7; el piloto tiene fase C de la 4.11, sin el bloque objetivo de la 4.12).
- Piloto: `"**Estado `concluido` · cubo Vigilar · acción esperar** · precio 90.10 EUR · zona caro · precio de Sí 57.74 · precio esc. MALO 45.56 · ponderado 62.62 · precio objetivo 57.74 · **con datos de etapa 1 incompletos** (causas: evidencia Historia!C23:L23 — Pasivo por arrendamientos: no verificable; evidencia Historia!C26:L26 — Minoritarios: no verificable; evidencia Análisis!C48 — Intereses pagados clasificados en financiación · IFRS: cero pendiente de verificación; evidencia Historia!C13:L13 — Adquisiciones netas (positivo): cero pendiente de verificación; evidencia Historia!C16:L16 — Intereses pag"`
- Código final: `"**Estado `concluido` · cubo Vigilar · acción esperar** · precio 90.10 EUR · zona caro · precio de Sí 57.74 · precio esc. MALO 45.56 · ponderado 62.62 · precio objetivo 57.74 **(provisional: lo condicionan Palancas!B16; Palancas!D16; B69:D69; Configuración V6.4 · P-M1 (PM1.estructura SR1 · PM1.familia Λ · PM1.parametro λ = 1,15))** · **con datos de etapa 1 incompletos** (causas: evidencia Historia!C23:L23 — Pasivo por arrendamientos: no verificable; evidencia Historia!C26:L26 — Minoritarios: no verificable; evidencia Análisis!C48 — Intereses pagados clasificados en financiación · IFRS: cero pen"`

## Límites de R1

- **Diferencia:** la ficha del piloto se escribió antes de la corrección H12: no lleva los dos límites de R1 (terminal sin el máximo conservado y S2C inerte); el código final sí, y la 4.12 añade las lecturas con bases parciales (BL sin P0; G7 con bases heredadas).
- Piloto: `["configuración de ensayo: ninguna estructura, λ, θ, tipo ni margen está adoptado (propuestas humanas sin firmar)", "P-M1 no queda resuelta por implementar sus alternativas; la identidad del FCF es aritmética, no prueba del mantenimiento real", "R0 + P-M1 sin especificar (se rechaza); motor B solamente"]`
- Código final: `["configuración de ensayo: ninguna estructura, λ, θ, tipo ni margen está adoptado (propuestas humanas sin firmar)", "P-M1 no queda resuelta por implementar sus alternativas; la identidad del FCF es aritmética, no prueba del mantenimiento real", "R0 + P-M1 sin especificar (se rechaza); motor B solamente", "R1: el terminal no aplica la regla del máximo conservado (carga la inversión fija para crecer al ritmo g aunque las ventas del MALO sigan por debajo del máximo; definición prudente)", "R1: en los años en que las ventas no superan el máximo conservado no hay inversión fija para crecer, y la palanca S2C de ese escenario no actúa en ellos", "BL (valor sin crecimiento; Diagnóstico B33:D33 y «cu`

## Lo que añade la 4.12 a un expediente con fase C de la 4.11

- fase C de la 4.11 (sin materialidad separada ni protocolo): el código final no reconstruye un objetivo 4.12 que esa fase C no evaluó (objetivo = `None`).
- las variantes del piloto son del formato 4.11 (sin instantánea ni avisos): con el código final, un pipeline nuevo las recalcularía (paso 10).
- el piloto no tiene cadena_trazabilidad.json; la escribe el paso 12 del código final.
- el código final añade a la ficha y a la sección 1 del informe la aptitud de uso de la entrega, separada de la auditoría («experimental»: ni «concluido» ni APROBADO hacen el resultado apto para decidir con dinero real); el piloto, de la 4.11, no la lleva (ficha: `experimental`; sección 1: sí).

**Conclusión.** El piloto conserva sus salidas históricas y su aprobación (material intacto). Las cuatro diferencias son de presentación o de registro, no de valoración: no cambian el ponderado, el precio de Sí, la zona, el estado ni la acción. El cierre nuevo de Vidrala (§7) se ejecuta con el código final.
