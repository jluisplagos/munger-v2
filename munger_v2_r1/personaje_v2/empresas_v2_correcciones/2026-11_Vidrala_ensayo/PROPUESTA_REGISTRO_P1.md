# Registro humano que impide continuar: P1 en `fase1_decisiones.json`

**Es el único registro que falta para reanudar el ensayo.** Ninguna otra confirmación es necesaria para que el pipeline llegue a las fases. Prueba: la simulación de los pasos 0–4 en `resultados/simulacion_pasos_0_4.txt` y el script de comprobación, §6–7.

## Por qué hace falta un registro humano

**[Hecho] Qué dice el procedimiento vigente** (contrato de la reparación, §1; `fase1_historia.py`):
- una cifra incorrecta (tipo B) se fija «con fuente en `fase1_decisiones.json`»;
- ese archivo «lo escribe solo una persona; ningún agente ni script»;
- `construir` lo aplica.

**[Hecho] Qué es P1.**
- La lectura del comparativo de 2024 en el informe de 2025 perdió un paréntesis: «106,417)».
- Por eso el circulante de 2024 quedó en −127,840 en lugar de +84,994.
- La línea y el importe pasan las comprobaciones H1. Es un error de signo (limitación L4), no un rechazo de `comprobar-anio`.
- Una nueva extracción con signo cambiado no está prevista para un tipo B. Hacerla eludiría el registro humano.

**[Hecho] Qué no hace Claude:**
- no escribe `fase1_decisiones.json`;
- no firma;
- no pone fecha ni nombre;
- no aplica P1 por otra vía (editando `fase1_v63.json`, el libro o una extracción).

## Registro propuesto

**Archivo:** `Vidrala/fase1_decisiones.json` del expediente de ensayo. La persona responsable lo sustituye por el contenido de `PROPUESTA_fase1_decisiones_con_P1.json` después de revisarlo.

**Cambio respecto al archivo actual:** solo añade la clave `circulante_lineas`; el resto no varía. Los campos `fecha` y `confirmado_por` están vacíos y los rellena la persona.

```json
"circulante_lineas": {
 "2024": {
  "valor_mm": 84.994,
  "fuente": "CF_2024 español (doc. 2118) p.14: «Efectivo generado por las operaciones (84.994)», con «Otros activos y pasivos corrientes y no corrientes (106.417)»; comparativo de CF_2025.txt p.7: «Cash used in operating activities (84,994)», donde la línea «Other current liabilities» imprime «106,417)» sin paréntesis de apertura (P1 del piloto). Convención de la Historia: aumento del circulante = −(suma de las líneas de variación) = +84,994",
  "fecha": "",
  "confirmado_por": ""
 }
}
```

**Evidencia:**
- `contrastes/vidrala_2023_arrendamientos/textos_nuevos/CF_2024_ES_EXTRACCION_NUEVA.txt`, p.14, del PDF español 2118 conservado;
- `Vidrala/texto/CF_2025.txt`, p.7.

La comprobación del piloto (35) y la de la 4.3 (217) contienen el cuadre del estado de flujos.

**Convención de signo.** La Historia registra el aumento del circulante como consumo de caja: −(suma de las líneas). El subtotal impreso (84.994) entre paréntesis da +84,994.

## Qué ocurre después

1. Con el registro guardado, se ejecuta `python3 personaje_v2/scripts/pipeline.py personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo/Vidrala`.
2. El pipeline sigue desde el paso 2:
   - `preparar` no pide ningún año, porque todos pasan;
   - `construir` aplica P1;
   - después vienen el relleno, la comprobación de entrada y el volcado.
3. Se detiene en el paso 5 para pedir el agente de extracción. A partir de ahí vienen las fases A, B y C y la auditoría (ver `INFORME_DEL_ENSAYO.md`, §5).

**Resultado esperado, comprobado en la simulación:**
- la Historia difiere de la original solo en K14 = 84,994;
- C53 pasa de 1,549 a 0,916;
- C58 pasa de 0,0199 a −0,0276;
- 0 bloqueantes;
- los motores A, B y C son calculables;
- 6 evidencias quedan pendientes para «LISTO · PROVISIONAL»: los ceros pendientes y C48.
