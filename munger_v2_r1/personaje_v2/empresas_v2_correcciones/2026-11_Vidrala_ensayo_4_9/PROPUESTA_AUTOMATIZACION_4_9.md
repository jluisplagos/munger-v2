# Propuesta: verificación automática de ceros y excepciones humanas (entrega 4.9, encargo §5)

> **[Propuesta] No está activada.**
> - El contrato de confirmaciones vigente no cambia:
>   - la IA no confirma ceros;
>   - la IA no rellena `decision`, `fecha` ni `confirmado_por`;
>   - una clasificación documental favorable no es una confirmación humana;
>   - P1 no autoriza otras confirmaciones.
> - Activar esta política exige una decisión expresa de la persona responsable, un encargo y una entrega con sus pruebas.

## 1. Por qué

Los 38 ceros pendientes de Vidrala se investigaron en la 4.9 con comprobaciones reproducibles (`scripts/n4_investigacion.py`):
- localizar la cita en su página;
- cuadrar el bloque completo del estado financiero;
- contrastar con la versión española y con el ESEF;
- rastrear las dependencias;
- medir el efecto por recálculo.

Resultado:
- 35 entradas quedan respaldadas por un cuadre completo, 8 de ellas con una reserva;
- 3 son conceptos no aplicables. Para años vecinos hay decisiones escritas en `fase1_decisiones.json`, pero sin fecha ni firma: no constan como confirmaciones humanas.

Hoy las 38 esperan igual una decisión humana, una a una. La propuesta es reservar esa decisión a las excepciones y que la persona responsable revise de una vez, agrupadas, las verificaciones automáticas.

## 2. Condiciones para una verificación automática

Un cero solo podría quedar **verificado automáticamente** si se cumplen todas estas condiciones, y cada una deja traza:
1. **Cita en su página.** La línea citada está en la página declarada del texto conservado, y ese texto se regenera desde el PDF oficial con su huella.
2. **Cuadre completo de ambas columnas.** El bloque del estado que contendría el dato cuadra en sus dos columnas:
   - la suma de las líneas es igual al total impreso;
   - no hay ninguna línea ilegible en la columna del año;
   - no hay ninguna línea del concepto con importe en esa columna;
   - una línea con un solo importe solo se acepta si una única asignación de columnas cuadra las dos.
3. **Comparativa coherente.** La columna comparativa del informe siguiente cuadra igual. Si no existe (último año), hacen falta la versión española y, si la hay, la taxonomía oficial (ESEF).
4. **Prioridad documental aplicada.** Si hay versión española, se comprueba en ella y se exige que coincida. Una contradicción entre versiones oficiales nunca se resuelve automáticamente: pasa a excepción.
5. **Norma aplicable.** El concepto existe en ese ejercicio. Si no existe (NIIF 16 antes de 2019), no es un cero verificado sino un **no aplicable**: véase el punto 3.
6. **Sin componentes sin acreditar.** Si una parte del concepto no está publicada (los intereses de arrendamientos dentro de los intereses pagados), la entrada no se verifica automáticamente: queda «respaldada con reserva» y es una excepción.
7. **Clasificación por exclusión.** Cada línea del bloque tiene un rótulo de una lista blanca para esa partida. Una línea con un rótulo desconocido no se interpreta: es una excepción. La detección por rótulos buscados no basta, porque un rótulo alternativo («Finance costs paid», «Business combinations», «Short-term investments») la esquiva (auditoría interna de la 4.9, Z-4).

La investigación de la 4.9 ya aplica las condiciones 1, 2 (con la tolerancia a erratas solo en la columna comparativa), 3, la unidad (buscada en la cabecera del estado) y la 7, más las excepciones de estructura del control de vigencia (líneas sin rótulo, segundo bloque, desgloses «of which») (`n4_investigacion.aplicar_condiciones_generales`). Las clases 4 dependen de la norma por fecha y de la ausencia de la línea. Eso no la convierte en una verificación automática: no está activada y nada se registra.

## 3. Cero, ausencia de dato y no aplicabilidad

La propuesta usa tres estados, que no se convierten unos en otros:

| Estado | Qué significa | Representación en la Historia |
|---|---|---|
| **Cero verificado** | Clase 1 (publicado) o 2 (cuadre completo), con todas las condiciones del §2 | `0` |
| **No aplicable** | El concepto no existe en ese ejercicio o hay una exención (clase 4) | Lo decide la persona responsable una vez, como **regla**: `0` si la definición de la plantilla lo admite, o vacío. Nunca se infiere un 0. Ya existe una regla así para los arrendamientos («solo pasivos NIIF 16»), con decisiones de 2017–2018 escritas en `fase1_decisiones.json`, aunque sin fecha ni firma |
| **Ausencia o evidencia insuficiente** | Clase 3, o un valor discrepante (clase 5) | Vacío (= desconocido) o pendiente; nunca `0` |

## 4. Trazabilidad y estado propio

**Estado nuevo.** Se propone un estado distinto de los dos actuales («pendiente de verificación» y «confirmado por una persona»): `verificado_automaticamente`.

**Registro.** Cada verificación quedaría en un archivo propio, separado de `fase1_decisiones.json`, con:
- la versión y la huella del verificador;
- las huellas del PDF, del texto y del ESEF;
- la página;
- el bloque y sus totales;
- las comprobaciones superadas;
- la fecha.

El pipeline tendría que distinguir los tres estados:
- en el libro, por ejemplo con la etiqueta «Dato verificado (automático)»;
- en `datos_ausentes.json`;
- en la ficha.

Así un lector distingue lo que comprobó una máquina de lo que confirmó una persona.

**Caducidad.** Una verificación automática caduca si cambia:
- el texto, el PDF o la extracción;
- la versión del verificador.

## 5. Pruebas contra falsos positivos

Ninguna activación sin una batería que demuestre que el verificador **rechaza**, como mínimo:
- una línea del concepto dentro del bloque (intereses en financiación);
- un bloque que no cuadra (falta o sobra una línea);
- un importe ilegible en la columna del año;
- un interés no dominante en el balance;
- un resultado atribuido distinto del total;
- una adquisición con importe en la columna del año;
- un depósito corriente;
- una cita que no está en su página;
- rótulos alternativos que esconderían el concepto;
- estructuras de página que la lectura línea a línea no ve (líneas sin rótulo, un segundo bloque, un desglose fuera del bloque, la unidad en una nota al pie).

La 4.9 ya incluye estas pruebas, a pequeña escala, en `scripts/test_n4_comprobaciones.py` (19 pruebas, con los 14 rótulos alternativos de la auditoría interna y los 6 engaños estructurales del control de vigencia). Una activación exigiría además:
- **los once engaños del segundo control de vigencia que hoy pasan** (W-5 de `AUDITORIA_INTERNA_4_9_vigencia_2.md`: «thereof», «including», espacios no separables y homoglifos, otra cabecera de bloque, «€ millions», rótulos partidos, otros nombres de los minoritarios), convertidos en pruebas y rechazados;
- **mutaciones del verificador**, todas detectadas;
- **una muestra con resultados conocidos de otra empresa**, para no sobreajustar a Vidrala;
- **la comprobación de que un cambio en el PDF o en el texto invalida la verificación.**

## 6. Cuándo hace falta una persona

Siguen siendo excepciones que exigen intervención humana:
- **Contradicción entre versiones oficiales** (español frente a inglés, PDF frente a ESEF) o una errata en la columna del año.
- **Concepto no aplicable**, salvo que ya exista una regla humana para ese caso.
- **Componente no publicado** (reserva): por ejemplo, los intereses de arrendamientos, que dependen de P3 y de C49.
- **Clases 3 y 5**: evidencia insuficiente o valor discrepante.
- **Efecto material en la valoración** por encima de un umbral que fije la persona responsable. Por ejemplo, L26: −0,0284 € por acción por cada millón.
- **Juicio de perímetro**: discontinuadas, reexpresiones o cambios de consolidación.
- **Cualquier cambio de criterio** de la plantilla.

## 7. Cómo presentar las decisiones pendientes

Un único expediente por empresa, como `propuestas/propuestas_n4_sin_firmar.json`:
- **Agrupado por partida y clase**, no por celda. Por ejemplo, «minoritarios 2016–2025, clase 2» es un solo grupo de diez años.
- **Celdas dependientes listadas dentro del grupo**, sin solicitud propia: C48 dentro de `intereses_financiacion`, el puente dentro de `minoritarios`.
- **Tres bloques separados:**
  1. las verificaciones automáticas, para una revisión en bloque que la persona responsable puede aceptar o rechazar de una vez;
  2. las excepciones, con la evidencia y la pregunta concreta;
  3. las reglas de no aplicabilidad, una vez y no por año.
- **Columnas separadas**:
  - cobertura documental;
  - situación del registro humano;
  - estado que reconoce el pipeline.

## 8. Qué haría falta para activarla

1. Una decisión expresa de la persona responsable sobre esta política y sobre el estado `verificado_automaticamente`.
2. Un encargo de código:
   - el verificador como pieza del sistema, no del expediente;
   - el estado nuevo en `fase1_historia.py`, en `rellenar_fase1_v63.py` y en el libro;
   - las pruebas del §5.
3. Una reejecución con auditoría nueva del expediente que lo use.

Hasta entonces, las 38 entradas siguen pendientes en el pipeline, aunque la matriz de la 4.9 documente su cobertura.
