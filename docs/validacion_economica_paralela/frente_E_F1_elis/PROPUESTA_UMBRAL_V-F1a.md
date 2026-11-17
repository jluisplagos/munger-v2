# Propuesta de umbral de materialidad para V-F1a · para decisión

**Fecha:** 17-nov-2026. **Estado:** propuesta para la persona responsable. **No adopta nada.**

- Responde a la petición registrada el 17-nov-2026: una propuesta de umbral para V-F1a, el control del doble cómputo del arrendamiento.
- Mientras no se decida otra cosa, **V-F1a sigue bloqueando con cualquier importe**, como aprobó (1a). El 0,5 % de la versión 1 no está adoptado; aquí se analiza como alternativa.
- Se conservan C48 = 108, C49 = 128,1, el FCF base 307,933, E1/D3/E2/E6 y Elis en `pendiente_de_datos`. No se fija R, θ, λ, k ni ninguna probabilidad.
- **El umbral no se ha elegido por su efecto en Elis:** con cualquiera de las opciones analizadas, el estado de Elis es el mismo (§7).

Marcas: **[P]** publicado o escrito en el producto · **[D]** derivado · **[I]** interpretación · **[H]** hipótesis · **[Pol]** política (una decisión, no un dato).

Cifras y casos: `resultados/umbral_v_f1a_frontera.{json,md}`, de `scripts/umbral_v_f1a_frontera.py`. Los casos usan importes ficticios, que no son datos de ninguna empresa. 30 casos con su estado esperado, 14 comprobaciones directas y 6 reglas erróneas detectadas, sin fallos.

---

## 1. Respuesta corta

- **Qué mide V-F1a.** Con el perímetro `A0_total` y arrendamientos, la proyección cobra el arrendamiento dos veces. El exceso es exacto: la amortización de los derechos de uso (D&A ROU), como proporción de las ventas [D].
- **Propuesta de umbral** [Pol]:
  - **medida:** e = D&A ROU media de la ventana ÷ FCF base registrado. Es la infravaloración relativa del flujo calibrado. No tiene unidades;
  - **valor: 0,1 % (uno por mil);**
  - **regla:** si e supera el 0,1 %, o si el FCF base no es positivo, BLOQUEA como hoy. Hasta el 0,1 %, AVISO con el exceso a la vista.
- **Lo que un umbral no hace:** no ahorra datos ni decisiones. Para medir e hace falta la misma fila de D&A ROU con la que el perímetro de (1a) corrige el error sin coste. Lo único que hace es tolerar un error conocido. Por eso la cifra es pequeña a propósito: solo lo claramente trivial.
- **«Sin umbral» sigue siendo coherente y es más simple.** La diferencia práctica entre las dos opciones es mínima. Un umbral de este tamaño no exime a ninguna empresa con arrendamientos corrientes [I]: para ellas la salida es el perímetro de (1a), no el umbral.
- **Cuándo adoptarlo.** Si hay un caso real con arrendamientos ínfimos que hoy quede bloqueado, este umbral lo resuelve. Si no lo hay, basta dejarlo sin umbral y tener esta propuesta preparada. No he medido e en los demás expedientes del motor A: sus cifras no están en el CSV verificado de este frente.
- **No propongo el 0,5 % de las ventas.** Su base no da una consecuencia uniforme: equivale al 2,5 % del FCF base en un negocio de margen ancho y al 25 % en uno de margen estrecho.
- **La cifra exacta es convencional.** Lo que la propuesta sostiene es la base y el orden de magnitud. No hay un dato del que salga un porcentaje.

---

## 2. Qué mide V-F1a exactamente

- **El doble cómputo** [D] (informe, §5): con `A0_total`, la proyección resta la D&A ROU dentro del margen y los pagos de arrendamiento completos dentro de f. El coste verdadero son los pagos.
- **Tamaño exacto** [D]. Por la fórmula de calibración (especificación, E3), la f de `A0_total` supera a la de `A1_sin_ROU` en

      ρ = f_A0 − f_A1 = Σ D&A ROU de la ventana ÷ Σ ventas de la ventana

  y el flujo de cada año lleva de menos ρ·V_t.
- **A la escala de la ventana**, el exceso es X = D&A ROU media. Es antes de impuestos: el impuesto real ya está dentro de f.
- **Alcance** [D]:
  - a crecimiento cero y en el año 11 el exceso es íntegro y no depende de ninguna palanca;
  - en los años 1–10, si la palanca S2C se ancla con el mismo perímetro de `A0_total`, el exceso disminuye con el crecimiento y se anula cerca del crecimiento histórico (informe, §5.3); por encima cambia de signo. **El error no es «siempre prudente».**
- **Ejemplo sintético** (caso T5 de la especificación): EBITDA 100; capex propio y D&A propia, 20; D&A ROU 10; pagos 12. Flujo verdadero 68; `A1_sin_ROU` da 68; `A0_total` da 58. El exceso es la D&A ROU.

---

## 3. Fundamento

### 3.1 Para qué sirve un umbral y para qué no

- **No ahorra el dato.** V-F1a no se puede evaluar sin la D&A ROU de cada año de la ventana, y V-F1b ya bloquea si esa fila está vacía con C49 positivo. Con esa misma fila se calcula el perímetro sin ROU.
- **No ahorra la decisión.** `perimetro_reinversion` se registra con fecha, persona y motivo, también si vale `A0_total`. Para los arrendamientos, la política ya está decidida: (1a).
- **Lo que sí hace:** permite conservar `A0_total` cuando el exceso es trivial. Evita declarar otro perímetro, pedir la D&A ROU de los años del ancla que están fuera de la ventana y volver a anclar S2C, margen y ROIC.
- **A cambio,** deja en el resultado un error de definición conocido, de tamaño exacto y corregible.

### 3.2 Qué origen puede tener una línea de materialidad en este sistema

- **El producto ya lo tiene escrito** [P]. El contrato del juicio sobre el objetivo (4.14; `personaje_v2/scripts/objetivo_v64.py`) admite cuatro orígenes para la línea entre material y no material: ninguno, el redondeo declarado, el juicio propio del agente y una política adoptada. Dice: «No hay umbral: un criterio propio del agente […] se representa como juicio suyo, nunca como política; una política solo cuenta si está registrada con decisión, fecha y firma humana». Ese contrato rige la capa experimental V6.4, no V-F1a; se cita como el criterio del producto sobre de dónde puede salir una línea de materialidad.
- **El umbral que la plantilla ya tiene para una incoherencia del modelo** [P] es el del salto del terminal (`Diagnóstico V6!C179`, 5 puntos, «ajustable»): avisa si se supera. Es un parámetro declarado, no una cifra demostrada.
- **La conciliación F1 no usa tolerancias globales** [D]: cada identidad se afirma con la cota de redondeo de sus cifras (informe, §2).
- **Consecuencia:** un porcentaje para V-F1a es una política [Pol]. Necesita una decisión registrada y no sale de ningún dato.

### 3.3 Qué debe cumplir la medida

1. **Estar ligada a la conclusión.** Lo que el motor valora es un flujo; el error debe medirse contra el flujo, no contra las ventas.
2. **Salir de entradas registradas,** sin palancas ni resultados del motor.
3. **No tener unidades:** el mismo resultado en millones o en miles y en cualquier moneda.
4. **Crecer con el exceso.**
5. **Tener el dominio definido:** qué pasa si el denominador es cero o negativo.
6. **Compararse de forma exacta.**

e = X ÷ FCF base las cumple:
- en la ventana, el flujo calibrado es el FCF base, y `A0_total` proyecta de menos exactamente X a esa escala. e es la infravaloración relativa del flujo calibrado [D];
- X y el FCF base son entradas registradas del mismo período;
- con un FCF base no positivo la medida no está definida, y entonces no hay exención.

ρ, la medida de la versión 1, cumple todas salvo la primera.

### 3.4 De qué tamaño

Es un error conocido, de signo y tamaño exactos, que se corrige sin coste. **Solo cabe tolerar lo claramente trivial.** No hay una cifra demostrable; estas referencias dan el orden de magnitud:

| Referencia | Orden | Naturaleza |
|---|---|---|
| Lo que la conciliación F1 ha tratado como no material sin pedir decisión: el residuo del interés de arrendamiento (informe, §5.4). El redondeo del registro (E7) es mucho menor | 0,04 % del FCF base | [D], práctica de este expediente |
| Lo que este expediente está llevando a decisión, partida a partida: el alcance de N1 (0,10 % con su opción B; 0,14 % con la A) y la actualización del earnout (0,26 %) | entre 0,10 % y 0,26 % del FCF base | [D], práctica de este expediente |
| La resolución de las fuentes: cota de redondeo de un FCF base de cientos de millones publicado con un decimal | del orden del 0,1 % (0,08 % en Elis) | [D] |
| Práctica de auditoría: importancia relativa global en torno al 5 % del resultado, y lo «claramente trivial», una pequeña fracción de ella | décimas de punto porcentual | Referencia externa citada como orden de magnitud. **No es una fuente de este expediente ni está en la base** |

- Un umbral bastante mayor que una o dos décimas de punto toleraría sin decisión errores mayores que los que aquí se deciden uno a uno.
- **Uno por mil** es la cifra redonda de ese orden. 0,05 % o 0,2 % serían igual de defendibles.
- Las referencias del expediente son cifras de Elis, porque el expediente es de Elis; el script las calcula en su bloque informativo. Sirven como medida de qué se ha tratado como decidible, no como efecto del umbral: a Elis el umbral no le cambia nada.

---

## 4. Propuesta

**Medida.**

    X = Σ D&A ROU de los ejercicios de la ventana ÷ n
    e = X ÷ FCF base registrado          (solo si el FCF base es positivo)

**Regla,** con el motor A, el perímetro `A0_total` y D&A ROU y C49 positivos:

| Situación | Estado | Efecto |
|---|---|---|
| FCF base nulo o negativo | **BLOQUEA** | La medida no está definida: no hay exención |
| e > 0,1 % | **BLOQUEA** | Como hoy: «coste de arrendamiento contado dos veces en la proyección» |
| 0 < e ≤ 0,1 % | **AVISO** | `A0_total` admisible. Se muestran X, e, ρ y la infravaloración del flujo sin crecimiento y del año 11. No acredita coherencia |

- **Frontera:** con e exactamente igual al umbral no bloquea. Es el criterio del umbral del terminal de la plantilla, que avisa «si supera» C179 y no en la igualdad.
- **Aritmética:** exacta y sin dividir. Se compara Σ D&A ROU con 0,001 · n · FCF base. Con esa forma, un FCF base nulo o negativo bloquea por sí solo.
- **Parámetro registrado:** el umbral se guarda con fecha, persona y motivo, como E1–E6. Por defecto, sin umbral.
- **Lo que no cambia:** V-F1b (fila vacía), V-F1e (invariantes) y V-F1m (solo uno de los dos importes es positivo). El perímetro de (1a) sigue siendo la regla y siempre se puede usar.

**Texto que se pediría aprobar:**

> «Apruebo un umbral de materialidad para V-F1a. Con el perímetro `A0_total` y D&A ROU y C49 positivos, se mide e = D&A ROU media de la ventana ÷ FCF base registrado. Si el FCF base es positivo y e no supera el 0,1 %, V-F1a pasa de BLOQUEA a AVISO y muestra el exceso, e y la infravaloración del flujo sin crecimiento y del año 11. Si e supera el 0,1 %, o el FCF base no es positivo, bloquea. La comparación es exacta. El umbral es un parámetro registrado. No cambian V-F1b, V-F1e ni V-F1m. Un aviso no acredita coherencia. Esta aprobación modifica el texto de (1a) solo en esto: `A0_total` se admite sin arrendamientos o, con aviso, por debajo del umbral.»

**Alternativa igual de fundada, que es lo vigente:**

> «Mantengo V-F1a sin umbral: con `A0_total` y D&A ROU y C49 positivos, bloquea con cualquier importe.»

---

## 5. Alternativas

| Alternativa | Regla | A favor | En contra |
|---|---|---|---|
| **Sin umbral** (vigente) | Bloquea con cualquier X positivo | La más simple. No tolera ningún error conocido. Es lo aprobado con (1a). La corrección no cuesta | Un arrendamiento ínfimo obliga a declarar otro perímetro |
| **Uno por mil del FCF base** (propuesta) | AVISO si e ≤ 0,1 % | Base ligada al flujo. Simple. Solo tolera lo trivial | La cifra es convencional. Añade un parámetro y una frontera |
| De resolución | AVISO si X ≤ B, la cota de redondeo del FCF base | No necesita una cifra de política: sale de la precisión de las fuentes, como las cotas de las identidades | Con pocas cifras significativas tolera mucho: 6,7 % del FCF base en el caso F26. Depende de cómo imprime cada empresa. Exige el literal de cada componente. Un error conocido no es ruido de redondeo |
| 1 % del FCF base | AVISO si e ≤ 1 % | Simple | Diez veces la propuesta. Tolera sin decisión más de lo que este expediente decide partida a partida |
| 5 % del FCF base | AVISO si e ≤ 5 % | Es el orden de la importancia relativa global en la práctica de auditoría (referencia externa) | Esa referencia es para errores no identificados. Aquí el error está identificado y medido |
| **0,5 % de las ventas** (versión 1) | BLOQUEA si ρ ≥ 0,5 % | ρ es exactamente el exceso de f. Simple | Consecuencia no uniforme (tabla siguiente). Exime con el FCF base negativo (caso F20). En la igualdad bloquea, al revés que el umbral de la plantilla |
| Contraste del precio de Sí | No material si el precio de Sí con `A0_total` y con `A1_sin_ROU` coincide a su redondeo declarado | Es el criterio «calculado» del contrato 4.14 y mide la conclusión misma | Para evaluarlo hay que calcular `A1_sin_ROU`, y entonces se usa ese. En la práctica equivale a no tener umbral |
| Medir con C49 en lugar de la D&A ROU | AVISO si C49 ÷ FCF base ≤ u | No pide la fila nueva | El principal pagado no acota la amortización: puede ser menor. Obligaría a tocar también V-F1b |

**El 0,5 % de las ventas, expresado sobre el flujo** [D]:

| FCF base ÷ ventas | 0,5 % de las ventas equivale a… del FCF base | Uno por mil del FCF base equivale a… de las ventas |
|---|---|---|
| 2 % | 25 % | 0,002 % |
| 5 % | 10 % | 0,005 % |
| 10 % | 5 % | 0,010 % |
| 20 % | 2,5 % | 0,020 % |
| 30 % | 1,7 % | 0,030 % |

- Los negocios con muchos arrendamientos y poco margen son justo aquellos en los que la versión 1 toleraría más.
- Dos casos lo muestran: con ρ = 0,4 % y un FCF base del 2 % de las ventas, la versión 1 solo avisa ante un 20 % del flujo (F17); con ρ = 0,6 % y un FCF base del 30 %, bloquea ante un 2 % (F18).

---

## 6. Cómo se mediría

| Elemento | Definición |
|---|---|
| Numerador | D&A ROU de cada ejercicio de la ventana de calibración (`Historia C57`), de la fila nueva de la especificación (E1): magnitud, con su fuente y su signo declarados |
| Denominador | FCF base registrado (`Análisis C52`), con su redondeo declarado (E7) |
| Unidad | Ninguna: e es un cociente. Se muestra en tanto por ciento del FCF base |
| Umbral | Un número registrado; en la propuesta, 0,001 |
| Aritmética | Racional exacta, sin redondeos intermedios y sin dividir: Σ D&A ROU ≤ umbral · n · FCF base |
| Orden de los controles | Dominio (motor A y `A0_total`) → invariantes (V-F1e) → fila vacía (V-F1b) → dominio de A0 (los dos a cero, admisible; solo uno positivo, V-F1m) → umbral |
| Qué se muestra en el aviso | X, e, ρ, el umbral, y ρ·V₀ y ρ·V₁₀·(1+g∞) por escenario |
| Cuándo | Al calibrar, antes de usar ningún resultado |

---

## 7. Casos de frontera

Importes ficticios. Estado con cada opción; los 30 casos completos, en `resultados/umbral_v_f1a_frontera.md`.

| Caso | Qué prueba | e | Sin umbral | **0,1 % FCF base** | Resolución | 1 % | 5 % | 0,5 % ventas |
|---|---|---|---|---|---|---|---|---|
| F01 | Sin arrendamientos | — | Admisible | Admisible | Admisible | Admisible | Admisible | Admisible |
| F02, F03 | Solo uno de los dos importes es positivo | — | V-F1m | V-F1m | V-F1m | V-F1m | V-F1m | V-F1m |
| F04 | Fila de D&A ROU vacía en un año | — | V-F1b | V-F1b | V-F1b | V-F1b | V-F1b | V-F1b |
| F05 | D&A ROU negativa | — | V-F1e | V-F1e | V-F1e | V-F1e | V-F1e | V-F1e |
| F06 | Arrendamientos grandes con `A1_sin_ROU` | — | No aplica | No aplica | No aplica | No aplica | No aplica | No aplica |
| **F07** | **Igualdad en el uno por mil** | 0,1000 % | BLOQUEA | **AVISO** | BLOQUEA | AVISO | AVISO | AVISO |
| **F08** | **Justo por encima** | 0,1111 % | BLOQUEA | **BLOQUEA** | BLOQUEA | AVISO | AVISO | AVISO |
| **F09** | **Justo por debajo** | 0,0889 % | BLOQUEA | **AVISO** | BLOQUEA | AVISO | AVISO | AVISO |
| F10 | Igualdad que la coma flotante no ve: 0,1 + 0,2 + 0,3 | 0,1000 % | BLOQUEA | AVISO | BLOQUEA | AVISO | AVISO | AVISO |
| F12 | Igualdad en la resolución | 0,2500 % | BLOQUEA | BLOQUEA | AVISO | AVISO | AVISO | AVISO |
| F16 | Igualdad en el 5 % y en el 0,5 % de las ventas a la vez | 5,0000 % | BLOQUEA | BLOQUEA | BLOQUEA | BLOQUEA | AVISO | BLOQUEA |
| F17 | Margen estrecho: ρ = 0,4 % | 20,0000 % | BLOQUEA | BLOQUEA | BLOQUEA | BLOQUEA | BLOQUEA | **AVISO** |
| F18 | Margen ancho: ρ = 0,6 % | 2,0000 % | BLOQUEA | BLOQUEA | BLOQUEA | BLOQUEA | AVISO | **BLOQUEA** |
| F19 | FCF base cero | no definida | BLOQUEA | BLOQUEA | AVISO | BLOQUEA | BLOQUEA | AVISO |
| F20 | FCF base negativo | no definida | BLOQUEA | BLOQUEA | BLOQUEA | BLOQUEA | BLOQUEA | **AVISO** |
| F21 | F07 en miles: mismo resultado | 0,1000 % | BLOQUEA | AVISO | BLOQUEA | AVISO | AVISO | AVISO |
| F22 | Importes en miles, impresos a centenas de millar | 0,2333 % | BLOQUEA | BLOQUEA | AVISO | AVISO | AVISO | AVISO |
| F23 | Los mismos importes, impresos al millar: cambia la resolución y no el porcentaje | 0,2333 % | BLOQUEA | BLOQUEA | **BLOQUEA** | AVISO | AVISO | AVISO |
| F25 | Un año de la ventana con D&A ROU cero | 0,0667 % | BLOQUEA | AVISO | AVISO | AVISO | AVISO | AVISO |
| F26 | Fuente con pocas cifras significativas | 6,6667 % | BLOQUEA | BLOQUEA | **AVISO** | BLOQUEA | BLOQUEA | BLOQUEA |
| F27 | Caso T5, arrendamiento material | 14,7059 % | BLOQUEA | BLOQUEA | BLOQUEA | BLOQUEA | BLOQUEA | BLOQUEA |
| F29 | Caso T5, arrendamiento ínfimo: `A0_total` da 79,89 en lugar de 79,94 | 0,0625 % | BLOQUEA | AVISO | BLOQUEA | AVISO | AVISO | AVISO |
| F30 | Motor B | — | No aplica | No aplica | No aplica | No aplica | No aplica | No aplica |

Comprobaciones directas:
- la cota de redondeo, también con una cifra que entra y sale (coeficiente neto cero);
- `(0.1 + 0.2 + 0.3) / 3 / 200 > 0.001` en coma flotante, y la igualdad exacta con fracciones;
- la identidad f_A0 − f_A1 = ρ y los flujos del caso T5;
- sin umbral, los cuatro casos de A0 dan el estado vigente (W3);
- con el FCF base nulo o negativo, el motivo mostrado es que la medida no está definida.

Una implementación debe dar esos mismos estados. El script aplica además seis reglas erróneas (frontera estricta en cada umbral, frontera de la versión 1 al revés, sin la guarda del FCF base, coeficientes sin compensar y dominio de A0 mal escrito) y comprueba que cada una hace fallar algún caso o alguna comprobación directa (`variantes_erroneas`).

**Elis, solo como información** (cifras verificadas; no es criterio): X = 132,5; FCF base = 307,933; e = 43,0 %; ρ = 2,91 %. Con `A0_total`, todas las opciones bloquean. Con el perímetro de (1a), V-F1a no se aplica.

---

## 8. Qué cambiaría en la especificación si se aprueba (no aplicado aquí)

- **E2,** fila `A0_total`: de «solo si D&A ROU = 0 y C49 = 0» a «o, con los dos positivos y e hasta el umbral, con aviso».
- **E5,** V-F1a: la condición, la severidad en dos tramos y el contenido del aviso.
- **E9,** T8: los casos de frontera del §7 con su estado esperado. T7 no cambia.
- **Los cuatro casos de A0** (W3): el de «los dos positivos» se divide en dos; los otros tres no cambian.
- **El texto de (1a),** aprobado el 17-nov-2026: la enmienda expresa del final del §4.

Si se mantiene sin umbral, no cambia nada.

---

## 9. Qué no valida

- **No valida `A0_total`.** Un aviso no es una prueba de coherencia: el resultado lleva un error conocido, pequeño y a la vista.
- **No mide el error de los años 1–10,** que depende de cómo esté anclada la palanca S2C y puede ir en los dos sentidos.
- **No cubre V-F1m ni V-F1b.** Un caso con un solo importe positivo, o con la fila vacía, sigue bloqueado por pequeño que sea. No propongo umbral para ellos: no afirman un doble cómputo, sino datos incompletos o en conflicto.
- **Un caso que E5 no nombra:** fila de D&A ROU vacía con C49 = 0. Por E1, vacío no es cero, así que `A0_total` no sería admisible. Lo anoto para el frente técnico; no lo resuelvo aquí.
- **No dice nada** de la PPA, de R, de las compras, de la transición ni de τ.
- **No es un umbral de materialidad del producto** ni sirve para otros controles.
- **No acredita los datos** con los que se mide.
- **No cambia nada en Elis** ni libera su valoración.
- **No dice a qué casos reales afectaría:** no he medido e en los demás expedientes del motor A.
- La cifra es una convención. Este documento no está revisado por un contexto distinto del autor.

---

## 10. Reproducción

Desde `scripts/`:

    python3 -I umbral_v_f1a_frontera.py --salida ../resultados/umbral_v_f1a_frontera.json \
        --informe ../resultados/umbral_v_f1a_frontera.md \
        --cifras ../datos/cifras_fuente.csv --verificacion ../resultados/verificacion_cifras.json \
        --n1 ../resultados/n1_alcance_y_actualizacion.json

Los tres últimos argumentos solo añaden el bloque informativo de Elis. Termina con 1 si algún caso no da su estado esperado o si alguna regla errónea no se detecta.
