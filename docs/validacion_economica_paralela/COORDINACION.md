# Frentes paralelos — 15-nov-2026

Base congelada para el análisis económico: revision/4.15-hito1, commit 059f4f68dca7acf465b5f5b21de2dede84c885ff. Esta rama solo añade documentos de revisión: no cambia código, fórmulas, libros ni datos del producto.

## Estado observado

La captura más reciente muestra a Claude Code inspeccionando pruebas HTML, dentro de U2–U5/I20. R415-SIGNO aparece marcado como terminado por el autor; revisión independiente, regresión y empaquetado siguen pendientes. A las 16:57 UTC GitHub solo publicaba main y revision/4.15-hito1: los cambios de claude/hopeful-bardeen-qap6y0 no estaban disponibles. No se afirma conocer el estado del proceso vivo más allá de esa captura.

## Reparto

- T, tarea actual de Claude Code: controles de datos, modos/estados y salidas; I19/I20 y H-P1/X2 conforme al encargo, pruebas y punto de entrega con commit. Es el único frente que modifica código de producción en esta etapa.
- E, segunda tarea de Claude Code en una copia independiente: conciliación económica F1 de Elis, fuentes, definiciones, residuos y especificación propuesta. Solo documentos y cálculos de contraste separados; no modificar el producto ni adoptar criterios por su efecto en una valoración.
- Revisión externa, ChatGPT: contrastar fuentes, cálculos, incertidumbres y aceptación por expediente. El inicio documental y los criterios ya están guardados en esta carpeta. No se ha concluido la validación económica.

Antes de implementar una corrección F1, T y E deben compartir una especificación identificada por commit/huella y los supuestos pendientes. La implementación se hace sobre la versión técnica fijada de T; después se repite la réplica, se regeneran expedientes y se audita el material final. Dos procesos no deben escribir el mismo árbol ni usar el mismo perfil de LibreOffice simultáneamente.

## Resultados iniciales

F1_INICIO_CONCILIACION.md documenta fuentes primarias y celdas. La presencia de ROU149,5, intangibles adquiridos85,7 y pagos lease177,9 está comprobada; eso no prueba por sí solo un doble cómputo. C48=108 está conciliado y se preserva. La reinversión media que calibra C58 es−81,2; el puente hacia el FCF base aún debe cerrarse con impuestos y perímetros coherentes. No se valida ningún precio objetivo.

ACEPTACION_Y_ALCANCE.md distingue las decisiones E1/D3/E2/E6 ya autorizadas de supuestos pendientes, y propone pruebas por expediente y un contraste fuera de muestra. El registro de fuentes nuevas no equivale a disponer de sus bytes.

## Para ejecutar E

Abrir otra tarea de Claude Code sobre una copia aislada del repositorio. Leer y ejecutar PROMPT_FRENTE_ECONOMICO.md. Para disponer de binarios: materializar y verificar primero main con el ZIP original base-4.14 y después cambiar a esta rama. No aplicar tools/base_414.py sobre los textos ya modificados de la 4.15. La rama económica parte del hito1, no del trabajo aún no publicado del frente T.

La aceptación para apoyar una decisión de inversión se evalúa sobre un expediente concreto, un motor cuyo alcance esté validado y una versión auditada. Los tests y la conservación de bytes no acreditan por sí solos la economía del modelo ni la decisión de inversión. La rentabilidad y las pérdidas siguen siendo inciertas.

## Modelos y esfuerzo incorporados al encargo

Opus 5.5/Máx para la conciliación y el razonamiento económico; Opus 5.5/Alto para operaciones mecánicas; Fable 5.2/Máx para revisión independiente en contexto separado. El frente técnico conserva Opus 5.5/Alto. Aplicación mediante los controles realmente disponibles; no afirmar selección ni ejecución sin evidencia. El detalle y el procedimiento cuando se necesita ajuste manual están en PROMPT_FRENTE_ECONOMICO.md.
