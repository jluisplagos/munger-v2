# Expediente de ensayo de Vidrala · detenido antes de construir la Historia

Este expediente es una copia corregida para el ensayo de la ruta A con el motor B (entrega 4.4). El original, `personaje_v2/empresas_v2/Vidrala/`, no se ha tocado.

**No debe relanzarse el pipeline hasta que una persona haya registrado P1** en `fase1_decisiones.json`. La propuesta exacta está en `../PROPUESTA_REGISTRO_P1.md`.

Si se relanzara sin ese registro, `construir` generaría la Historia con el circulante de 2024 erróneo (−127,84), y el ensayo no incorporaría P1.

**Estado:**
- pasos 0 y 1 ejecutados: entorno y migración de la etapa 1, con un libro base idéntico al original;
- `estado_pipeline.json` en el paso 2;
- no hay `fase1_v63.json`.
