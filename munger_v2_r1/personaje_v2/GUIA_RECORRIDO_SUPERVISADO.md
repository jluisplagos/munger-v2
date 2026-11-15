# Guía breve del recorrido supervisado · plantillas V6.4 y V6.4.1 experimentales (motor B) · entregas 4.13 y 4.14

**Para qué sirve.** Explica cómo se recorre un expediente con agentes reales bajo la supervisión de la persona responsable, qué se mira en cada relevo y cómo se lee el resultado. Un recorrido así produce un **análisis experimental**: no es una decisión de inversión, no aprueba ningún parámetro y no sustituye a la evaluación de aptitud del informe de la entrega (`…/2026-11_Vidrala_ensayo_4_13/INFORME_INTEGRACION_4_13.md`, apartado de aptitud de uso).

**Vocabulario mínimo.**
- *Expediente*: la carpeta de una empresa con sus entradas, sus libros y las salidas de cada fase.
- *Relevo* (código 10): el pipeline se detiene y espera a que un agente escriba un archivo; se lanza el agente y se vuelve a ejecutar el pipeline.
- *Configuración económica*: `configuracion_economica.json`, que fija N1 (tipo impositivo normalizado), N2 (margen de partida), N3 (regla de reinversión) y P-M1 (estructura de la reposición). La escribe la orquestación, nunca un agente de juicio, y **no es una adopción**.
- *Material auditado*: los archivos que la auditoría aprueba; si cambian después, la aprobación se retira.
- *Valor calculado condicional*: lo que da el libro con hipótesis no adoptadas. *Precio objetivo emitido*: solo lo hay cuando nada material lo condiciona (ver §5).

## 1. Antes de empezar

1. Comprobar el paquete en una descompresión limpia: `bash verificar_paquete.sh completa` (≈ 25–45 min, 36 en la prueba de traspaso de la 4.14; tiene que dar PASA). Espacio en disco: CONTINUIDAD §2, punto 5.
2. Una sola tarea con LibreOffice a la vez: el pipeline, las baterías y los controles que recalculan van siempre en secuencia. `comprobar_entorno.sh`, que el pipeline ejecuta al empezar, también llama a LibreOffice. Las lecturas sin recálculo pueden ir en paralelo.
3. No se modifica nada de `personaje_v2/empresas_v2/` ni de los expedientes de entregas anteriores: se trabaja en un expediente nuevo.

## 2. Preparar el expediente

- **Base económica nueva** (por ejemplo, pasar de 2024 a 2025): `python3 -I personaje_v2/scripts/cambiar_base.py preparar CAMBIO.json`. Separa las fechas (ejecución real, base, precio, acciones, publicación de las fuentes), reconstruye `fase1_v63.json` desde los textos de la fase 1 y deja los productos del origen en `antecedentes/`. Necesita esos textos.
- **Misma base, sin los textos de la fase 1** (caso de Viscofan en la 4.12): carpeta nueva con las entradas de partida (`etapa1/`, `fase1_v63.json`, `fase1_metadatos.json`, `fase1_fuentes.json`, `fase1_partes/`), los textos recuperados en `texto/` con su nombre propio (una edición distinta no lleva el nombre de la fuente de la fase 1), la fecha de análisis igual a la fecha real de ejecución y `alcance_v2.json` con el aviso del ensayo. Modelo: `…_4_12/scripts/preparar_viscofan_experimental.py`; en la 4.13, `…_4_13/scripts/preparar_expedientes_4_13.py`.
- **Cifras frescas y su evidencia** (precio, capitalización, acciones, rf y, si se recalcula, EV/EBITDA): `fase1_v63.json` trae la cifra con su fuente, período, unidad y nota, y `rellenar_fase1_v63.py` sustituye entera su evidencia en el Control maestro (la anterior queda en el registro de la fase 1, `evidencias_sustituidas`). La lista de períodos de la comprobación (Control maestro C86:E102) se sustituye con `control_maestro_textos`. Una cifra de contraste que conserve datos de otra fecha se declara, no se borra.
- **Configuración económica** (la orquestación):
  - con un análisis propio de la empresa y sus fuentes con página (modelo: `…_4_12/scripts/analisis_configuracion_viscofan.py`); nada se traslada de otra empresa;
  - trazabilidad completa de cada parámetro activo: clase, confianza, fuente o condición, justificación y materialidad;
  - un parámetro no observado (λ, θ) va como rango (`lambda_rango` o `theta_rango`) y su valor activo se declara como punto de cálculo, sin central económica adoptada;
  - una entrada vacía (N1 o N2) conserva la regla heredada solo si la elección se explica;
  - con la V6.4.1, el perímetro de la inversión de P-M1 (`PM1.perimetro_inversion`: «Caja» o «NIIF 16», con `altas_derechos_uso` y `altas_fuente` de cinco años si es NIIF 16) es obligatorio cuando hay requisito; el otro perímetro se calcula como variante y ninguno está adoptado;
  - se declara el protocolo experimental del objetivo (`protocolo_objetivo`: `objetivo_condicionado` o `bloqueo_del_objetivo`); ninguno está adoptado;
  - se valida: `python3 -B personaje_v2/scripts/configuracion_economica.py validar configuracion_economica.json`.

## 3. Recorrer el pipeline

`python3 personaje_v2/scripts/pipeline.py CARPETA --config personaje_v2/config_v2_v64_experimental.json` (V6.4) o `--config personaje_v2/config_v2_v641_experimental.json` (V6.4.1, con el perímetro). La selección de la plantilla es siempre explícita: la V6.4 rechaza una configuración con perímetro y la V6.4.1 exige declararlo si hay requisito. `…_4_13/scripts/paso_pipeline.py CARPETA [--config …]` hace una pasada y guarda la salida completa en `resultados/pipeline_NN_*.txt`.

| Código | Qué significa | Qué se hace |
|---|---|---|
| 0 | terminado (concluido, pendiente o no entregable, con su diagnóstico) | leer la ficha, el informe y `diagnostico.md` |
| 10 | espera a un agente (`ESPERANDO.md`, `prompts_generados/`) | lanzar el agente y volver a ejecutar |
| 2 | parada sin escribir: selección, configuración o material incoherentes | corregir la causa; no forzar |
| 3 | límite del modelo (motor fuera de la cobertura, financiera, otro método) | es un resultado legítimo; se documenta |
| 5 | retirada de una aprobación pendiente de registrar | volver a ejecutar cuando el resumen sea escribible |
| 6 | estado del pipeline o registro de auditorías ilegible | restaurar desde una copia o relanzar con `--reiniciar`; nunca se sigue como aprobado |

**Cada relevo** se resuelve con un agente real:
- el prompt generado (`prompts_generados/NN_<fase>.md`), con el modelo y el esfuerzo de `config_v2_v64_experimental.json → modelos` (extracción: Sonnet, esfuerzo medio; fases A, B y C: Opus, esfuerzo alto; verificación: Opus, esfuerzo medio);
- reglas de la ejecución: escribe solo su salida; notas en una carpeta temporal; sin internet ni memoria; base económica declarada; no ejecuta el pipeline ni LibreOffice; no abre Excel;
- la fase C tiene dos turnos con **el mismo agente** (se continúa la conversación);
- nunca se copia la salida de otro expediente en un expediente real (los agentes «simulados» solo valen para pruebas técnicas y controles).

Orden habitual: extracción → fase A → fase B → recálculo y variantes (paso 10) → fase C turno 1 → turno 2 → verificación y auditoría → cierre. Puede haber vueltas (gramática, correcciones de formato, de la fase C a la B).

## 4. Qué mira la persona responsable en cada relevo

- **Fase A.** El motor sale de los hechos, como si la configuración no existiera. Si la fase A elige un motor que la V6.4 no cubre (A o C), el expediente termina en el límite del modelo experimental: es un resultado válido, no un fallo.
- **Fase B.** `gramatica.md`: errores corregidos y desviaciones justificadas con hechos. Las palancas no descuentan otra vez lo que ya hace la configuración.
- **Paso 10.** `configuracion_v64_variantes.md` (formato 4.13): variantes **calculadas** sobre copias del libro (heredado, componentes aislados, contrastes aislados de cada parámetro, estructuras compatibles, convenciones, extremos del parámetro y, con la V6.4.1, el otro perímetro), con la zona de cada una, la **cobertura** de cada parámetro (contraste aislado, variación conjunta necesaria, variación conjunta o sin cobertura) y los **avisos de dominio de todas las variantes, agrupados**, con la conclusión a la que afecta cada grupo. Una variante sin zona impide afirmar «la misma zona en todas».
- **Fase C.** `configuracion_v64`: para cada parámetro activo, si es material para la acción y para el objetivo, con la **base** de cada materialidad (calculada, juicio económico con su evidencia, o no determinada = null; «no determinada» no es «no material»), los hechos separados de las inferencias, las discrepancias con la configuración revisadas, y si tiene fundamento suficiente. No hay umbral adoptado de materialidad: la línea que traza el agente es un juicio y se lee como tal (dos agentes pueden trazarla distinta con el mismo material); la comprobación conjunta (D10) con la combinación de los numéricos activos y las alternativas no numéricas definidas; el bloque `objetivo` (su tratamiento lo comprueba `objetivo_v64.py`, no lo elige el agente).
- **Paso 12.** `verificar_todo.sh`, la correspondencia de las variantes con `precio.json` y con las entradas económicas del libro final, y la cadena de trazabilidad (`cadena_trazabilidad.md`: fuente → dato → transformación → entrada → cálculo → resultado → conclusión, con avisos de ceros pendientes, vacíos, signos, unidades, stock/flujo y fechas).
- **Auditoría.** Los 16 puntos del contrato histórico, sobre el material fijado. APROBADO solo vale para ese material. Si una auditoría encuentra un defecto del código que escribe el material provisional (ficha, informe), se corrige el código y se relanza `pipeline.py … --desde 13`: el material se regenera y se fija de nuevo, y hace falta una auditoría nueva; la aprobación del material anterior no se usa para cerrar (en la 4.13 se guardó en `antecedentes/auditoria_material_<id>/`). Cada auditoría es un agente nuevo.

## 5. Cómo se lee el resultado

- **Estado, acción y cubo** (ficha e informe, línea 1).
- **Aptitud de uso** (`ficha.json → aptitud_de_uso`; informe §1, debajo de la línea de estado; columna del resumen V6.4): es la evaluación de la entrega, separada de la auditoría. Mientras diga «experimental», ni el estado «concluido» ni una auditoría APROBADO hacen el resultado apto para decidir con dinero real.
- **Objetivo** (`ficha.json → objetivo`; informe §1 y §14):
  - `objetivo_emitido`: nada material lo condiciona;
  - `objetivo_condicionado`: hay hipótesis sin fundamento que lo condicionan, pero la acción se sostiene en todo el ámbito calculado: el precio de Sí se da como **valor calculado condicional, provisional**, con la lista de hipótesis;
  - `objetivo_bloqueado`: con el protocolo de bloqueo, o porque la acción no se sostiene en el ámbito: no hay precio objetivo;
  - `objetivo_sin_protocolo`: hacía falta un protocolo y no se declaró: no se emite un objetivo oficial;
  - `sin_objetivo`: comprar, descartar, demasiado difícil, dato ausente material (S-19) o esperar por algo que no es el precio.
- **Rango calculado**: es la dispersión de las variantes calculadas, **no un intervalo de confianza** ni cubre las hipótesis no exploradas.
- **Avisos de dominio** y **lecturas con bases parciales** (G7, BL): se leen con sus valores; no hay umbrales adoptados.
- **Acción final y objetivo**: la acción FINAL manda; una contradicción entre la acción final, el estado, el protocolo y los dos objetivos (el estructurado y el de la decisión) no llega a ninguna ficha ni a material listo para auditoría.
- **Fechas**: base económica, ejecución, precio, acciones y fuentes van por separado; un expediente con cuentas de un año y precio posterior no es una valoración al cierre de ese año ni un backtest.

## 6. Cambios después del cierre

Cualquier cambio del material auditado (configuración, selección, libros, variantes, fórmulas, protocolo), también un archivo del material o un campo de control del que depende la vigencia con una estructura JSON incorrecta (nulo, lista, escalar o campo anidado de otro tipo), retira la aprobación en la **primera** llamada de cualquier herramienta, antes de rechazar nada, y el pipeline repite lo afectado (por ejemplo, un cambio solo del protocolo repite la fase C sin recalcular las variantes; un cambio económico las recalcula). Las salidas cerradas no se editan a mano.

## 7. Qué no se hace

- Rellenar campos humanos, firmar decisiones o dar por adoptados un parámetro, un cero pendiente, una estructura de reposición o un protocolo.
- Modificar los originales, las plantillas, las referencias o los expedientes históricos.
- Usar agentes simulados en un expediente financiero real.
- Rebajar un criterio para que algo pase, o retocar una referencia para ocultar un fallo.
- Leer el resultado como una orden de compra o de venta.

## 8. Novedades de la 4.14 (flujo habitual con la verificación de las entradas)

1. **Entrada.** Hay tres vías: desde Excel (la V5.3 del v1 y la V6.3 con datos), desde PDF (`scripts/pdf_a_texto.py` y `scripts/fase1_historia.py construir`) o desde instrucciones (`prompts/historia_anio.md` y `prompts/metadatos_fase1.md`).
   - *Ejemplos de entrada y salida:* Viscofan y Vidrala (Excel) y Elis (PDF e instrucciones), en `empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_14/`.
   - Cada expediente lleva en su carpeta la entrada (`etapa1/`, `fase1_*`, `texto/`) y la salida (`ficha.json`, `informe.md`, `auditoria.md` y los libros).
2. **Registro de las entradas.** `python3 -B scripts/verificacion_entradas.py plantilla CARPETA` crea el registro. Para no tocar el expediente, hágase en una copia.
   - **El extractor** rellena cada entrada: fuente con archivo, página, cita que contenga la cifra, escala y signo; o una derivación con orígenes y fórmula; o una hipótesis con fundamento, alternativas y límites; o un cero comprobado, un dato ausente o no aplicable, cada uno con su justificación.
   - **Un revisor distinto** rellena `comprobacion` en cada entrada: revisor, resultado, fuente examinada y nota.
   - `python3 -B scripts/verificacion_entradas.py comprobar CARPETA` dice si el registro es apto. El pipeline lo vuelve a comprobar en el paso 12.
   - Un registro no apto no impide recorrer el pipeline, y ninguna salida se presenta como apta para dinero real. Con la V6.4 y la V6.4.1, la ficha y el informe dicen «apta por entradas: no». Con la V6.3 (motor A) no lo dicen: el resultado está en `estado_pipeline.json → verificacion_entradas` y en el registro del pipeline (INCIDENCIAS I20).
3. **Cambio de base o corrección de datos de un expediente cerrado.**
   - Se escribe un `CAMBIO.json`, con los ejemplos de `…_4_14/configuracion/cambio_decisiones_*.json`, y se ejecuta `python3 -I scripts/cambiar_base.py preparar CAMBIO.json`. Nunca sobrescribe: crea un expediente nuevo y el origen no se toca.
   - Una corrección de la Historia va en `correcciones_fase1_partes`, con el valor impreso que se espera encontrar.
   - Si el CAMBIO perdería una entrada `analisis` del origen, la preparación se detiene.
   - Después se actualiza el registro de las entradas que cambian. Primero escribe el extractor y después revisa el revisor; también se actualizan los fundamentos de las hipótesis que reescriban las fases.
4. **Regla de rama para los agentes.** Cada agente parte de la salida del expediente anterior (`../antecedentes/heredados/`) y cambia solo lo que se invalida, con una sección «Cambios frente al expediente anterior».
5. **Configuración por motor.**
   - Motor B: `--config config_v2_v64_experimental.json` (V6.4) o `config_v2_v641_experimental.json` (V6.4.1, con perímetro).
   - Motor A: `--config config_v2.json` (V6.3).
   - Con la V6.4, la elección del motor A por la fase A termina en «límite del modelo» (Elis, `elis/`).
6. **Efectos separados.** Se miden con copias del libro evaluado del expediente anterior, con sus fases fijas. Ejemplos: `…_4_14/scripts/efecto_decisiones_*.py`. El caso «todo» tiene que reproducir el expediente nuevo.
7. **Interrupciones y recuperación.**
   - Si el pipeline se corta, se vuelve a ejecutar con el mismo comando: retoma en el paso guardado en `estado_pipeline.json`, y un agente que no terminó se vuelve a lanzar con el mismo `prompts_generados/NN_*.md`.
   - `--desde N` repite desde el paso N cuando cambia una entrada de ese paso, por ejemplo `--desde 12` para el registro de las entradas.
   - Si el material cambia después de una auditoría, la aprobación se retira sola: el pipeline emite una solicitud nueva, y una auditoría anterior no responde a ella.
   - **Relevo caducado.** Si, mientras el paso 13 espera, cambia o aparece un archivo del material (`cierre_v2.MATERIAL_FIJO`), la solicitud pendiente ya no se puede aprobar: el pipeline no vuelve a fijar el material mientras espera (INCIDENCIAS I19). Se usa `--desde 12`, que emite una solicitud nueva.
   - **Relevo de un expediente anterior o sustituido:** en una copia hermana a la misma profundidad, nunca en su sitio. Se relanza primero con el mismo comando para regenerar los prompts con las rutas actuales (CONTINUIDAD §2, punto 6).
   - Una retirada o una publicación pendiente se resuelve con el mismo pipeline; ver `scripts/cierre_v2.py` y `documentacion_cierre_4_14/hito1/REGISTRO_REPARACION_4_13_1.md`.
