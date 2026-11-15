# Registro de aplicación de P1 (entrega 4.5, 9-nov-2026)

## Recepción
- **Archivo recibido:** `PROPUESTA_fase1_decisiones_con_P1.json`, adjuntado por la persona responsable en la conversación del 9-nov-2026 (11:37, hora de Ámsterdam). Mensaje: «Se adjunta el archivo de decisiones revisado y cumplimentado por la persona responsable. La confirmación corresponde exclusivamente a P1: circulante de 2024 = +84,994 millones.»
- **Tamaño y huella:** 2.703 bytes · SHA-256 `b4e47afcb3ddbc6bda35bff9f20c8cfc6881c0b800bc731a34e4205b63c445a4`.
- **Conservado sin cambios como** `registro_P1/PROPUESTA_fase1_decisiones_con_P1_cumplimentada.json`.

## Validación (`scripts/validar_registro_P1.py`, 10 de 10; salida en `validacion_salida.txt`)
1. Conserva todas las decisiones anteriores (`_regla`, `deuda`, `arrendamientos`, `arrendamientos_principal`) sin cambios.
2. Solo añade `circulante_lineas`, con un único año (2024) y los campos `valor_mm`, `fuente`, `fecha` y `confirmado_por`.
3. `valor_mm` = 84.994 (millones; aumento del circulante con la convención de la Historia).
4. `fuente` idéntica a la propuesta de la 4.4.
5. `fecha` = «2026-11-09» y `confirmado_por` = «Jose Luis Pino Lagos»: cumplimentados, sin marcadores de posición ni nombres de agentes.

El validador se escribió y probó antes de recibir el archivo: rechaza la propuesta con los campos vacíos y un `confirmado_por` con nombre de agente.

## Incorporación
- Copiado **byte a byte** como `Vidrala/fase1_decisiones.json` del expediente de continuación (misma huella). Claude no reescribió ni reformateó su contenido.
- La copia de la 4.4 (`../2026-11_Vidrala_ensayo/Vidrala/fase1_decisiones.json`, sin P1) no se ha tocado.

## Alcance de la confirmación
Cubre **solo P1**. No cubre:
- los 38 ceros pendientes, que siguen pendientes;
- las demás decisiones heredadas;
- las hipótesis financieras del ensayo.

## Aplicación y efecto comprobado (`scripts/comprobar_continuacion.py`, §3–§4)
- **`construir`** registró «0 confirmados por decisión humana» porque ese contador se refiere a ceros. P1 entra como cifra fijada, con la fuente «decisión de Jose Luis Pino Lagos el 2026-11-09».
- **Historia K14:** −127,84 → **+84,994**. Es la única diferencia de valor de `fase1_v63.json` frente al original.
- **Celdas derivadas:** K30, K31, C53 (1,5492 → **0,915854**), C58 (0,019890 → **−0,027608**), C76, C77, C79 y C80. Todas son fórmulas de la fila 14.
