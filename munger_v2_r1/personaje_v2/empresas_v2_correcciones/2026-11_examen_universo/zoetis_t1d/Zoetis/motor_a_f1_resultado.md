# Motor A · perímetro F1 · F1-IMPL 2 (4.15 · decisiones F1 del 17-nov-2026 · US GAAP, ASC 842: D-US1, D-US2, D-US2 bis y D-WM del 18-nov-2026 · cierre de la revisión R2 · margen de partida según Palancas C8, 19-nov-2026)

Libro `ffc88797eb8b7bb6…` · declaración `d85c2ea4820fa304…` · 2026-11-19

**motor B utilizable para una conclusión según F1 (condición necesaria, no suficiente; no apto para dinero real)**

Estado propuesto: — · apto para dinero real: no.

## Guardas

| Id | Salta | Severidad | Efecto | Decisión | Detalle |
|---|---|---|---|---|---|
| F1-NORMA | no | — | — | generalidad | US GAAP declarada; libro: US GAAP |
| F1-US-DESGLOSE | no | — | — | US GAAP · ASC 842 | arrendamientos operativos y financieros declarados por separado |
| F1-US-PUENTE | no | — | — | puente de deuda · US GAAP | la fila 23 no lleva pasivo por arrendamiento operativo: la deuda del puente es la del libro |
| F1-US-ANCLA | sí | AVISO | AVISO | motor B · ancla de S2C y ROIC (lo que F1 no evalúa) | con el motor B, F1 solo evalúa el puente de deuda: no examina en qué líneas del estado de flujos están la amortización del derecho de uso y la variación del pasivo del arrendamiento operativo. Si la D&A (fila 8) o el circulante (fila 14) las llevan, el ancla de S2C (Historia C53 = 0.808572) y el ROIC histórico del libro (filas 32–33), que son la referencia de la fase B, las arrastran. Ninguna línea sumada en las filas 8 y 14 de los cinco años del ancla nombra el arrendamiento |
| F1-SERIES-CERO | sí | AVISO | PENDIENTE | (1a) · F1-SERIES-ESCALA | CERO SIN CIFRA IMPRESA, PENDIENTE DE REVISOR (no comprobado: el programa solo ha visto que la frase está en la página; no bloquea F1-SERIES y la aptitud por entradas sigue en «no»): series.pasivo_arr_operativo.2025: motivo «Pasivo por arrendamiento OPERATIVO dentro de la fila 23 de la Historia en 2025 = 0: la fila 23 lleva solo el pasivo por arrendamientos financieros (1 + 6 = 7, PDF p. 89) por la corrección registrada de fase1_partes (resultados/correccion_fase1_partes.json); el pasivo operativo publicado (52 + 196 = »; cita (p. 89 de 'Zoetis · Form 10-K FY2025') «Supplemental information for our lease portfolio is as follows:» |
| F1-SERIES | no | — | — | (1a) · H12 · V631-2 | US GAAP · 2 clasificaciones con su cita en la página citada y 0 páginas examinadas sin línea propia (D-US1) · D&A de derechos de uso y PPA: cifra publicada con su signo, como cifra completa, en una página existente de una fuente del expediente con su huella; columna del ejercicio comprobada en 0 años, PENDIENTE en 1 (la aptitud por entradas sigue en «no») |

## Flujo sin crecimiento por perímetro (diagnóstico)

| Perímetro | f | Flujo sin crecimiento | Frente a A0 | Ancla S2C (E4) |
|---|---|---|---|---|

## US GAAP (ASC 842) · arrendamientos operativos y financieros por separado

```
{
 "decisiones": {
  "D-US1": {
   "regla": "si la empresa no publica en qué líneas del estado de flujos van los dos tramos del arrendamiento operativo (la amortización del derecho de uso y la variación del pasivo), se supone que van netos dentro del flujo de explotación, fuera de las filas 8 (D&A) y 14 (circulante) de la Historia: hipótesis declarada, no dato; la conclusión se presenta como condicionada, con su cota de sensibilidad. Donde la empresa publica las líneas, manda el dato",
   "registro": {
    "fecha": "2026-11-18",
    "persona": "persona responsable del proyecto (decisión registrada; no se firma aquí)",
    "motivo": "munger-v2-evidencias-mistral, coordinacion/cierre_v2/DECISIONES_PARA_EL_USUARIO.md:96–98"
   }
  },
  "D-US2": {
   "regla": "cuando el coste lineal del arrendamiento operativo y los pagos del año difieren, se cuentan los pagos y la diferencia queda a la vista, sin bloquear",
   "registro": {
    "fecha": "2026-11-18",
    "persona": "persona responsable del proyecto (decisión registrada; no se firma aquí)",
    "motivo": "munger-v2-evidencias-mistral, coordinacion/cierre_v2/DECISIONES_PARA_EL_USUARIO.md:96–98"
   }
  },
  "D-US2 bis": {
   "regla": "con el alquiler operativo mezclado en las líneas de otros activos y otros pasivos (los dos tramos dentro de la fila 14) no se bloquea: se publica el valor de la hoja, que cuenta el coste contable, y al lado cuánto cambiaría contando los pagos; antes, el programa comprueba que el expediente muestra las dos líneas (la del activo y la del pasivo)",
   "registro": {
    "fecha": "2026-11-18",
    "persona": "persona responsable del proyecto (decisión registrada; no se firma aquí)",
    "motivo": "munger-v2-evidencias-mistral, coordinacion/cierre_v2/DECISIONES_PARA_EL_USUARIO.md:112–114 (tras la revisión R1 de F1 con US GAAP)"
   }
  },
  "D-WM": {
   "regla": "los arrendamientos financieros que la empresa no desglosa se tratan como deuda y activos propios (hipótesis declarada): su amortización queda dentro de la propia y sus pagos no se restan de la caja base; la diferencia estimada (caja pagada − gasto total) se enseña junto al resultado",
   "registro": {
    "fecha": "2026-11-18",
    "persona": "persona responsable del proyecto (decisión registrada; no se firma aquí)",
    "motivo": "munger-v2-evidencias-mistral, coordinacion/cierre_v2/DECISIONES_PARA_EL_USUARIO.md:112–114 (tras la revisión R1 de F1 con US GAAP)"
   }
  }
 },
 "operativos": {
  "existen": true
 },
 "financieros": {
  "existen": true
 },
 "puente_de_deuda": {
  "ejercicio": 2025,
  "motor": "B",
  "deuda_financiera_fila_22": 9042.0,
  "pasivo_por_arrendamientos_fila_23": 7.0,
  "pasivo_operativo_dentro_de_la_fila_23": 0.0,
  "deuda_del_puente_del_libro_C64": 9049.0,
  "deuda_del_puente_coherente": 9049.0,
  "exceso_que_restaria_el_motor_B": 0.0,
  "lineas_de_arrendamiento_operativo_sumadas_en_la_fila_23": [],
  "regla": "deuda del puente = deuda financiera + pasivo por arrendamientos financieros; el pasivo por arrendamiento operativo no entra: su pago ya está entero en el EBIT (una sola vez)"
 }
}
```

## Parámetros sin valor adoptado

- alcance_n1_ejercicios_tau: sin valor (N1_ALCANCE_EJERCICIOS_TAU.md (propuesta, no adoptada))
- n1_actualizacion_financiera_earnout: sin valor (N1_ACTUALIZACION_EARNOUT_MEXICO.md (propuesta, no adoptada))
- umbral_v_f1a: sin valor (PROPUESTA_UMBRAL_V-F1a.md (propuesta, no adoptada))
