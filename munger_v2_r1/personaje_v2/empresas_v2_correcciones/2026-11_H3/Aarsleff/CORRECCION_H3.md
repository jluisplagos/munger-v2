# Corrección H3 · Aarsleff · 8-nov-2026

Expediente nuevo y regenerado. El original, `empresas_v2/Aarsleff/`, no se ha tocado.

**Motivo.** El diagnóstico H3 comprobó que la Historia, fila 35 (FCF al accionista), tiene **cinco** años negativos: 2016, 2017, 2021, 2022 y 2023. Los textos de las fases A y C decían «cuatro». Ninguna fórmula lee esa fila, así que el error era solo de texto.

## Las cinco correcciones (salidas de agente registradas, sustitución literal sin reformatear)

| Archivo | Ruta | Antes → después |
|---|---|---|
| `fase_a.json` | `seis_preguntas.que_caja_espero` | «con cuatro años negativos» → «con cinco años negativos» |
| `fase_a.json` | `herencia.C25.evidencia_y_razonamiento` | «cuatro años negativos de diez» → «cinco años negativos de diez» |
| `fase_a.json` | `observaciones.C25` | «cuatro años negativos de diez» → «cinco años negativos de diez» |
| `fase_a.md` | líneas 49 y 99 | «Cuatro años negativos de diez» → «Cinco años negativos de diez» · «con cuatro años negativos» → «con cinco años negativos» |
| `fase_c.json` | `celdas.B102` | «con cuatro años negativos» → «con cinco años negativos» |

`celdas.C25` sigue siendo «No». Ninguna otra ruta de `fase_a.json` ni de `fase_c.json` cambia. Se comprobó comparando las rutas JSON del original con las del nuevo.

## Cómo se regeneró
1. Se copiaron sin cambios: `etapa1/`, `fase1_v63.json`, `fase1_partes/`, `fase1_fuentes.json`, `fase1_metadatos.json`, `fase1_listas.md`, `historia_revision.md`, `fase_b.md` y `fase_c.md`. Se copió `fase_a.md` con las dos correcciones.
2. En `../agentes_registrados/` quedaron las salidas originales de los agentes:
   - `extracto_v63.md` y `fase_b.json`, sin cambios;
   - `fase_a.json`, corregido;
   - el `fase_c.json` corregido, copiado como `fase_c.turno1.json` y como `fase_c.turno2.json`;
   - ningún `auditoria.md`.
3. Se ejecutó `python3 scripts/pipeline.py empresas_v2_correcciones/2026-11_H3/Aarsleff --agentes-simulados empresas_v2_correcciones/2026-11_H3/agentes_registrados`. El pipeline llegó al paso 13 sin pedir otro agente y allí se detuvo para pedir la auditoría.
4. Auditoría nueva: la hizo el agente de verificación previsto en el sistema (Opus, esfuerzo medio, sin contexto previo), con el prompt que había generado el pipeline. Resultado: 16 puntos en PASA y «Veredicto: APROBADO».
5. Se relanzó el pipeline, que leyó la auditoría con la regla de H2 y terminó: paso 14, estado `concluido`, auditoría APROBADO.
6. Se borraron `recalc/` y `.lo_perfil/`, que son copias de trabajo de LibreOffice que el expediente original tampoco incluía.

## Resultado
La comparación completa con el original, con su clasificación de diferencias técnicas y de contenido, está en `../comparacion_H3.json` y en la prueba `pruebas/test_comprobadores.py h3`.

- **Excel:** idénticas todas las celdas de los cuatro libros, tanto fórmulas como valores, salvo `Análisis!B102` y `Control maestro!N30`, donde cambia solo la frase. Hay además una diferencia técnica: `Control maestro!L5`, la fecha de revisión que escribe el relleno.
- **Sin cambios:** precio de Sí 450,57; ponderado 502,36; escenario MALO 346,99; zona caro; cubo Vigilar; acción esperar; fecha de análisis; predicciones; C25 = No.
