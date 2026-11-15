# Informe integrado · encargo 4.12 · fiabilidad para decisiones con dinero real, cierre de la integración y contraste con Viscofan

**Para quién y cómo leerlo.** Para la persona responsable del proyecto. Distingue en cada apartado los **hechos comprobados** (con la evidencia que los sostiene), las **interpretaciones** y las **propuestas**. La jerga se explica la primera vez que aparece. La evaluación de aptitud de uso está en el apartado 9 y es independiente de la aprobación del pipeline: que un expediente esté «concluido» y «APROBADO» no significa que el sistema sea apto para decidir con dinero real.

## 1. En breve

**Qué se pedía** (encargo 4.12). Hacer fiables para un uso supervisado las piezas que la 4.11 dejó abiertas, cerrar de nuevo Vidrala con el código final, ensayar dos protocolos para el objetivo y contrastar el sistema con una segunda empresa, Viscofan. Y evaluar, por separado de las auditorías, para qué sirve hoy el sistema. El motor A queda fuera.

**Qué se hizo** (hechos comprobados):
- **Vigencia, materialidad y coherencia.** Vigencia de las aprobaciones antes de cualquier rechazo. Materialidad separada para la acción y para el objetivo, con dos protocolos experimentales. Variantes atadas a las entradas del libro, avisos de dominio con sus valores, cadena de trazabilidad y aptitud de uso en las salidas. La batería obligatoria de la V6.4 pasa de 58 a 127 pruebas.
- **Vidrala.**
  - El control con las palancas de la 4.11 reproduce el piloto exactamente.
  - El cierre nuevo con agentes reales termina en **concluido · APROBADO · Vigilar · esperar**: precio de Sí 56,02 € frente a 90,10 € (cierre del 31-dic-2025; análisis del 12-nov-2026), con el objetivo **condicionado y provisional** por las hipótesis de reposición (P-M1).
  - La copia con el protocolo de bloqueo termina, con el mismo material, en **pendiente_de_datos · APROBADO · sin acción ni objetivo**.
- **Viscofan.**
  - Doce publicaciones conservadas, con edición identificada, y el heredado reproducido exactamente.
  - Una configuración propia, sin nada de Vidrala.
  - El expediente nuevo con agentes reales termina en **concluido · APROBADO · Vigilar · esperar**: precio de Sí 39,29 € frente a 54,70 € (cierre del 3-nov-2026), con el objetivo condicionado por P-M1.
- **Variantes calculadas.** En las dos empresas, todas dan «caro».

**Qué permite** (evaluación del §9, interpretación). Un uso **supervisado y experimental**: analizar empresas del motor B con la persona responsable revisando cada relevo y leyendo los resultados como valores calculados condicionales. **No** permite apoyar decisiones con dinero real. La reposición que fija el nivel del precio de Sí no se observa en las cuentas, nada está adoptado, no hay ensayo en el tiempo y solo hay dos empresas del motor B. **El resultado sigue siendo experimental.**

## 2. Qué funciona (hechos comprobados)

Cada apartado dice qué se comprobó y dónde está la evidencia. Las cifras salen de las salidas registradas; no se ha copiado ninguna a mano de un expediente a otro.

### 2.1 Vigencia de las aprobaciones antes de cualquier rechazo (§3)

**Qué se pedía.** Que un cambio del material auditado retire la aprobación en la primera llamada de cualquier herramienta, también cuando esa llamada termina rechazando la selección de plantilla.

**Qué se hizo.**
- `pipeline.py`: si la selección no se acredita y el material auditado cambió, falta o no se puede leer, primero se retiran la aprobación y las publicaciones registradas y después se detiene (código 2, o 5 si una retirada queda pendiente). Con el material intacto, el rechazo no toca nada.
- `ficha.py`, `informe.py` y `resumen.py` llamados a mano sin `MUNGER_CONFIG` resuelven la selección registrada solo si las huellas coinciden; si no, terminan con código 2 sin escribir.

**Evidencia.**
- Grupo E de la batería: siete alteraciones del material por cuatro primeras llamadas independientes (pipeline, ficha, informe, resumen), sobre copias del piloto 4.11 con el registro de publicaciones reubicado; selección equivocada con el material intacto; plantilla, referencia o verificador alterados con el mismo nombre; resumen no actualizable (retirada pendiente visible).
- Reproducción del fallo de la 4.11: `resultados/reproduccion_vigencia_codigo_4_11.md` (el código 4.11 rechaza y conserva la aprobación) frente a `resultados/reproduccion_vigencia_4_12.md` (el código 4.12 la retira y la archiva).

**Diferencia intencionada con la 4.11.** Añadir `configuracion_economica.json` a un expediente V6.3 cerrado cambia su material y ahora retira su aprobación en la primera llamada. El rechazo H1 de la 4.11 se mantiene.

### 2.2 Materialidad y protocolos del objetivo (§4)

**Jerga.** El *precio de Sí* es el precio por debajo del cual el personaje compraría. El *valor calculado condicional* es lo que da el libro con hipótesis no adoptadas. El *precio objetivo emitido* es el que la salida presenta como objetivo. Un *protocolo* es la regla que decide qué hacer con el objetivo cuando lo condicionan hipótesis sin fundamento suficiente.

**Qué se hizo.**
- `configuracion_economica.json → protocolo_objetivo`, con dos alternativas de ensayo:
  - `objetivo_condicionado`: se presenta el objetivo como condicionado y provisional, con sus hipótesis y su rango, si la acción se sostiene en todo el ámbito calculado;
  - `bloqueo_del_objetivo`: no se emite objetivo y el expediente queda pendiente de datos.
- Ninguna de las dos está adoptada. Sin protocolo declarado, cuando hace falta, no se emite ningún objetivo oficial y el diagnóstico explica las dos lecturas.
- `objetivo_v64.py` (solo lee) separa: dato ausente material (S-19), hipótesis sin fundamento suficiente, materialidad para la acción, materialidad para el objetivo y ámbito. Calcula el tratamiento y la decisión que corresponde a partir de dos banderas que la fase C declara para cada parámetro: material para el objetivo y fundamento suficiente. La fase C no elige el tratamiento, pero esas banderas son juicios suyos que ninguna regla contrasta (revisión interna R5; §9.6, L15).
- Campo estructurado en la ficha (`objetivo`), línea de estado y sección 14 del informe, y columnas del resumen V6.4. No hay que buscar la palabra «provisional» en un párrafo.
- La comprobación conjunta (D10) rechaza mover parámetros inactivos y recalcula una a una las alternativas no numéricas definidas.

**Evidencia.** Grupo F (36 pruebas): los dos protocolos y su ausencia, diez contradicciones, un dato ausente material con prioridad sobre el protocolo, una compra con una hipótesis experimental material fuera de las listas heredadas, λ sin mover, θ inactivo, comprobación conjunta ausente o inválida, estructuras sin alternativas, compatibilidad V6.3 y columnas. Y dos expedientes reales sobre el mismo material económico de Vidrala (§2.5).

### 2.3 Coherencia de las variantes, dominios y trazabilidad (§5)

**Qué se hizo.**
- **Correspondencia de las variantes.** `entradas_economicas.py` toma una instantánea de las entradas económicas del libro de origen: las 58 materiales de la relación independiente de la V6.3, con la Historia expandida, y las de «Configuración V6.4» sin metadatos (216 celdas en Vidrala con la relación «4.12»). Desde la revisión interna (R1), la relación «4.12+H13» añade la fila 13 de la Historia (226 celdas en Vidrala). Las instantáneas guardadas con la relación anterior se comparan con el libro de la variante activa en esa fila. Las variantes, en formato «4.12», llevan esa instantánea, la huella económica de la configuración y el vector de escenarios de la activa. Un cambio editorial no repite las valoraciones; uno económico sí. Un cambio solo del protocolo repite la fase C con las mismas variantes.
- **Avisos de dominio con sus valores** (`dominios_v64.py`), sin umbrales adoptados: inversión fija para crecer negativa, factor de reestimación f (lectura sin umbral), terminal de R1 sin máximo conservado y S2C inerte. La fase C evalúa cada uno; uno material condiciona el objetivo y no admite comprar.
- **Cadena de trazabilidad** (`trazabilidad_v64.py`, paso 12 de los expedientes V6.4): fuente → dato extraído → transformación o supuesto → entrada → cálculo → resultado → conclusión. Lleva identificadores por clase (D- dato publicado, C- cálculo, V- convención, H- hipótesis), magnitud (stock, flujo, precio…), fechas separadas y avisos de unidad, signo, fecha, stock frente a flujo, vacíos y ceros pendientes de verificación. Un dato desconocido nunca se convierte en cero.
- **Lecturas con bases parciales identificadas** en las salidas donde se usan: G7 de la gramática y las referencias mecánicas usan las bases heredadas; el valor sin crecimiento (BL) no incluye la cartera P0.
- **Diferencias del piloto 4.11 con el código final**, sin editar el piloto: `resultados/diferencias_piloto_4_11_codigo_final.md`. Todas son de presentación o de registro: las cuatro de los campos que compara el script (la versión de la configuración, el nombre del resumen, la marca provisional de la línea de estado y los límites de R1), la aptitud de uso que añade la 4.12 y la redacción de la sección 14 («13, incluida la activa»), que el script no compara.

**Evidencia.** Grupo G (17 pruebas) y los tres expedientes reales.

### 2.4 Reconstrucción portable y fuente de rf (§6)

- **Reconstrucción.** `comparar_zip.py` compara el contenido miembro a miembro de una reconstrucción en otro entorno. Para el artefacto entregado se exige la huella estricta. No se promete identidad binaria entre entornos: la huella del archivo depende de la compresión. Grupo A (12 pruebas).
- **Fuente de rf (Bundesbank).** **No se consiguieron los bytes.** La consola no llega a bundesbank.de (el proxy responde 403), y la carpeta que la persona responsable conectó no tenía el PDF. La herramienta de lectura web devolvió el texto del documento de la URL del encargo, sin el archivo: fecha 11.11.2026; fila «2025 Dez.», diez años = 2,85 %, la cifra que cita `fase1_metadatos.json`. No se afirma disponer del ejemplar ni de su huella (6ace5ac7…, declarada por la revisión externa). Queda como limitación (§6 y §9).

### 2.5 Vidrala: cierre nuevo con el código final y agentes reales (§7)

**Qué se conserva.** Base económica de 2025, r = 0,09, P1, las probabilidades del ensayo y k = 3 experimental, sin descontar otra vez el dividendo. La configuración económica es la de demostración de la 4.11, no adoptada. No se adopta ningún parámetro nuevo.

**Control con las palancas de la 4.11** (`control_palancas_4_11/resultados/control_palancas.md`). **CONCUERDA** con el piloto: precio de Sí 57,74229205598012 €, ponderado 62,6151093424602 €, las 13 variantes iguales y 0 de 216 entradas económicas distintas. El código final, por tanto, no cambia la valoración del piloto.

**Recorrido real** (`cierre_condicionado/Vidrala`, protocolo `objetivo_condicionado`). Cada código 10 se resolvió con un agente real:
- extracción con Sonnet (esfuerzo medio);
- fases A, B y C con Opus (esfuerzo alto); la fase C, en dos turnos con el mismo agente;
- auditoría con Opus (esfuerzo medio), en un contexto que no vio el trabajo.

**Resultado** concluido · auditoría interna **APROBADO** (16/16; la vigente responde a la solicitud SA-2427fb9cd6e753fe sobre el material 5025f54d0c143062) · cubo Vigilar · acción esperar:
- precio 90,10 €, cierre del 31-dic-2025 (la fecha de análisis es el 12-nov-2026), zona caro;
- precio de Sí 56,02 € (56,01809018887024), ponderado 60,70 €;
- valores por escenario 44,32 / 60,21 / 78,52 €, con probabilidades 0,2 / 0,6 / 0,2;
- objetivo **condicionado y provisional**: lo condicionan PM1.estructura, PM1.familia y PM1.parametro, por falta de un desglose del capex por destino;
- rango calculado del precio de Sí: 51,29–65,72 € en la activa y 14 escenarios calculados (las 15 variantes), todos en «caro». No es un intervalo de confianza. La familia de P-M1 no queda cubierta por ese ámbito, porque ninguna variante calcula Θ (corrección de la revisión interna R3: antes las salidas decían «ninguna»).

**Separación de los cambios** (`resultados/separacion_cambios_vidrala.md`):

| Clase de cambio | Frente al piloto 4.11 | Efecto en el precio de Sí |
|---|---|---|
| Software | ninguno en la valoración (el control concuerda) | 0 |
| Configuración económica | ninguna celda; solo se declara el protocolo del objetivo, que no es una celda económica | 0 |
| Datos | ninguno (216 entradas iguales) | 0 |
| Juicio | la fase B baja el crecimiento de los años 1–5 (MALO −0,01 → −0,015; NORMAL 0,025 → 0,015; BUENO 0,045 → 0,035), sobre todo por sacar Toro del NORMAL y del MALO | −1,724 € (ponderado −1,918 €) |

**Comparación homogénea** (`cierre_condicionado/resultados/comparacion_homogenea.md`). Mismas entradas y palancas, copias del libro evaluado:
- heredado (V6.3 efectiva): precio de Sí 64,75 €;
- activa: 56,02 € (−8,73 €);
- de esa diferencia, P-M1 con su cartera explica −6,61 €; N1, N2 y R1 juntos, el resto;
- los efectos aislados no son aditivos.

**Réplica independiente** (la de la 4.11, sobre los 16 libros finales): 16 de 16 coinciden, con diferencias ≤ 6,4e-14 €/acción en los valores (`cierre_condicionado/resultados/replica_independiente.txt`).

**Dos protocolos sobre el mismo material** (`COMPARACION_PROTOCOLOS_4_12.md`). La copia `cierre_bloqueo/Vidrala` solo cambia el protocolo a `bloqueo_del_objetivo`. Su primera llamada retiró la aprobación heredada, y la copia tuvo su fase C y su auditoría propias; no se copió ninguna aprobación entre las dos. Resultado pendiente_de_datos · auditoría interna APROBADO (SA-8da4a78afc939a43, material f7a0ba07431707e3) · cubo Vigilar · sin acción ni precio objetivo: el mismo valor calculado condicional (56,02 €), que no se emite como objetivo.

**Revisión económica** (`REVISION_ECONOMICA_VIDRALA_4_12.md`), en resumen:
- **Reposición frente a crecimiento.** En los años, SR1 evita el doble cómputo que tendría S, porque quita del S2C histórico la parte de la reinversión atribuida a reposición; ese doble cómputo vale 0,50 €. En el terminal queda uno posible: si el ROIC de la fase B ya era neto de reposición, sobra hasta 1,06 € (SR2). La mayor incertidumbre estructural está entre H y las demás estructuras (5,35 €): las cuentas no separan reposición y crecimiento.
- **S2C de los años y ROIC del terminal.** La rentabilidad marginal implícita de los años (9,5 %, 14,7 % y 20,0 % en MALO, NORMAL y BUENO) queda por encima del ROIC del terminal (9 %, 9 % y 12 %): hay una discontinuidad en el año 11. Parte la crea SR1; el resto es una elección de la fase B.
- **Convención terminal.** Cambiarla mueve poco (−0,13 € y +0,40 €). Deja una incoherencia declarada: el requisito es plano en los años y salta en el año 11 (+20,1 % en el NORMAL y +40,4 % en el BUENO).
- **Capacidad conservada en el MALO.** Las ventas del MALO quedan siempre bajo el máximo conservado. El terminal prudente de R1 carga aun así 15,8 M€ de inversión fija para crecer: 2,54 €/acción del valor MALO, unos 0,51 € del ponderado.
- **Dependencia de hipótesis no adoptadas.** Las 15 variantes calculadas dan «caro» (precio de Sí de 51,29 a 65,72 €). El precio está un 37,1 % por encima del mayor precio de Sí calculado (la diferencia, dividida entre ese precio de Sí).
- **Qué se sostiene.** Con las fuentes disponibles se sostiene la acción («esperar» por precio) en todo el ámbito calculado. El nivel del precio de Sí, y con él cualquier objetivo, sigue siendo una valoración condicional: depende de la estructura y del parámetro de P-M1, que no se han observado. Lo resolvería un desglose del capex entre mantenimiento, reconstrucción de hornos y crecimiento.

### 2.6 Viscofan: primer contraste entre empresas (§8)

El detalle está en `viscofan/CONTRASTE_VISCOFAN_4_12.md`. En breve (hechos):

- **Fuentes.** El paquete no traía ni PDF ni textos. Se conservan doce publicaciones con su PDF, su huella, su identificación y su texto con marcas de página. Cinco tienen la paginación de la fase 1 (2017, 2019, 2020, 2024 y 2025); las demás son otras ediciones, que se usan para contrastar por el contenido y nunca se llaman «original recuperado». Se contrastaron 186 celdas de la Historia; ninguna quedó sin encontrar.
- **Heredado reproducido exactamente.** Precio de Sí 43,050965031270174 €, ponderado 46,8821465263006 €, en V6.3 y en V6.4 heredado.
- **Configuración propia, sin nada de Vidrala.** N1 22,12 %: sin las activaciones de bases negativas, con perímetro y período analizados. N2 vacío por elección explícita. R1 con un circulante del 48,28 %, conciliado. P-M1 SR1 · Θ con θ no observado: rango 0–1 y θ = 0,5 solo como punto de cálculo. Cartera legado. Las combinaciones no definidas se declaran.
- **Expediente nuevo con agentes reales** concluido · auditoría interna APROBADO (SA-e8c8384c2e565c23, material 0dee970f14c042d4) · cubo Vigilar · acción esperar:
  - la fase A eligió el motor B por los hechos;
  - la fase B cambió una sola palanca frente al heredado (margen del MALO, de 0,15 a 0,14);
  - la fase C concluye «esperar», con el objetivo condicionado por PM1.estructura y PM1.parametro;
  - precio de Sí 39,29 € frente a un precio de 54,70 €; las 13 variantes calculadas dan «caro» (38,22–41,81 €).
- **Separación de los cambios.** Mecánica 0; datos 0; juicio −1,245 €; configuración −2,518 €.
- **Réplica.** 14 de 14 coinciden.

## 3. Qué falló y cómo se trató

Todos los fallos de esta lista se detectaron antes de entregar. Ninguno se resolvió rebajando un criterio ni retocando una referencia.

| Qué falló | Cómo se detectó | Qué se hizo | Efecto en los resultados |
|---|---|---|---|
| Dos baterías V6.3 dieron resultados intermedios (auditorías 7/26, estados 26/28) | Ejecución durante el desarrollo | Se editó `pipeline.py` mientras corrían. Se repitieron con el código final: 55/55 y 28/28. Regla desde entonces: no se edita ningún script mientras corre una batería | Ninguno: no eran resultados del código final |
| La sección 0 de `datos_v63.md` decía, antes de la fase A, «configuración válida: False … revisa Análisis C62» con el motor A de la etapa 1 de Viscofan | Lectura del material antes de lanzar la fase A | `volcar_datos_v63.py` dice ahora que la validez depende del motor que elija la fase A y que otro motor es un límite legítimo. El expediente se preparó de nuevo antes de lanzar ningún agente | Ninguno: la fase A no llegó a ver el texto anterior |
| El primer recorrido de Viscofan se hizo con fuentes parciales | Llegó una segunda entrega de publicaciones (21:58) | Ese recorrido se archivó como antecedente, no como resultado (`viscofan/antecedentes_fuentes_parciales/`). El expediente se preparó de nuevo y la extracción y las fases se repitieron con agentes nuevos | El expediente entregado usa las doce publicaciones |
| Con `objetivo_bloqueado`, la línea de estado de la sección 1 no daba el rango calculado con su ámbito | La auditoría interna del cierre de bloqueo de Vidrala (aviso del punto 10, que el auditor no contó como fallo) | `informe.py` lo da ahora con cualquier tratamiento. La aprobación anterior no se consumió: se conserva en `cierre_bloqueo/resultados/auditoria_anterior_a_la_correccion/`. El material se regeneró (`--desde 13`) y hubo una auditoría nueva | Ninguno en cifras: cambia una línea del informe |
| La aptitud de uso no aparecía en las salidas de los expedientes; solo iba a estar en este informe | La orquestación, al preparar este informe (§9: «se reflejará de forma diferenciada en las salidas nuevas») | Bloque `aptitud_de_uso` en la ficha, en la sección 1 del informe y en el resumen V6.4, separado de la auditoría. Los dos expedientes de Vidrala se regeneraron desde el paso 13 y tuvieron auditorías nuevas. El de Viscofan lo lleva desde su paso 13 | Ninguno en cifras ni en estados |
| Con un cambio de protocolo, el motivo de repetir la fase C («el protocolo del objetivo cambió…») solo llegaba al agente en el turno 2 | El relevo real de `cierre_bloqueo/Vidrala` | `pipeline.py` lo pide ya en el turno 1 (prompt y ESPERANDO.md). En aquel relevo lo comunicó la orquestación. Prueba nueva en el grupo G | Ninguno: aquella fase C ya recibió el motivo |
| El control de entrega comprobaba que ningún archivo se llamara `AR_2020.pdf`, pero la segunda entrega sí trajo la edición de 2020 con la paginación de la fase 1 | Revisión del script tras la segunda entrega | La comprobación mira ahora lo que importa: ninguna **otra edición** lleva el nombre de la fuente de la fase 1 ni se llama «original recuperado», y la edición sustituida no está entre las publicaciones | — |
| La réplica independiente de la 4.11 no aceptaba los libros de la 4.12 tal cual | Primera ejecución de `replica_expedientes_4_12.py` | El envoltorio pasa a cada caso las celdas de su configuración (`CE.celdas`) y los ajustes de cada variante | 16 de 16 coinciden |
| **PDF del Bundesbank: sin bytes** | Descarga imposible desde la consola y la carpeta conectada no lo tenía | Limitación registrada (§2.4). Se continuó con lo demás | La fuente de rf de Vidrala no se conserva con su huella |
| La instantánea de entradas económicas y la cadena de trazabilidad no cubrían las adquisiciones de la Historia (fila 13), que en el modo experimental entran en las bases de P-M1 (D_hist, F_hist, f) | Revisión interna (R1) | Relación «4.12+H13»: la fila 13 entra en la instantánea y en la cadena. Las instantáneas guardadas con la relación anterior se comparan con el libro de la variante activa en esa fila; sin ese libro no se acreditan. Una prueba nueva y una actualizada en el grupo G | Ninguno en cifras: en los tres expedientes la fila 13 coincide con la de la activa |
| «Hipótesis no cubiertas por el ámbito calculado: ninguna» se cumplía casi siempre: un subparámetro de P-M1 contaba como cubierto aunque ningún escenario lo moviera solo | Revisión interna (R3) | Un subparámetro de P-M1 cuenta como cubierto solo si tiene un ámbito aislado o entra en la comprobación conjunta. Prueba nueva en el grupo F | En Vidrala aparece ahora «PM1.familia» como no cubierta; en Viscofan, ninguna. El tratamiento del objetivo no cambia |
| La cadena de trazabilidad de Viscofan daba «0 avisos» con textos de evidencia del precio, la capitalización y las acciones que contradicen el valor (fechas de octubre y de junio de 2026, 53,60 € y 45,60 millones de acciones) | Revisión interna (R4) | `trazabilidad_v64.py` contrasta las fechas y los resultados que citan esos textos con el valor y avisa («fecha incoherente», «valor incoherente»). Sin falsos avisos en Vidrala ni en el piloto de la 4.11. Prueba nueva en el grupo G | La cadena de Viscofan lleva ahora 4 avisos, que van a la auditoría. Los valores del libro no cambian (efecto de las acciones de junio estimado por el revisor en unos 0,1 € en el precio de Sí, no recalculado) |
| El informe decía que los dos expedientes usaban precios de noviembre de 2026; el de Vidrala usa el cierre del 31-dic-2025. «186 celdas contrastadas» aparecía sin su salvedad. La revisión económica de Vidrala daba una lista de hipótesis sin fundamento distinta de la del expediente | Revisión interna (R2, R14 y R5) | Textos corregidos: el precio de cada expediente con su fecha, la salvedad de las 186 celdas y la lista de la revisión económica igual que la del expediente, con la diferencia anotada en su apartado 7 | Ninguno en cifras |
| Los valores de los avisos de dominio se escribían en el informe con la sintaxis JSON. Al repetir desde el paso 12 los dos expedientes de Vidrala, la verificación de citas (`verify_quotes_v2`, que lee también el informe anterior) tomó sus comillas rectas por citas y los dos quedaron `no_entregable` en el paso 12 | Repetición desde el paso 12 tras las correcciones de la revisión (12-nov, 23:52) | `informe.py` escribe esos valores sin comillas rectas (`plano`). Los tres expedientes se repitieron desde el paso 11, que regenera el material provisional con el código corregido antes de la verificación. Prueba nueva en el grupo G, que comprueba también que la forma anterior fallaba. El defecto es de la 4.12: dos líneas heredadas del fundamento material (D10) escriben igual una lista y una combinación, pero no aparecen en estos expedientes (queda como límite) | Ninguno en cifras. Los cierres anteriores quedaron archivados por el pipeline en `historial_cierres/` |

## 4. Diferencias frente a la 4.11

**Código.**

| Archivo | Qué cambia |
|---|---|
| `personaje_v2/scripts/pipeline.py` | Vigencia antes del rechazo; paso 13 con `libros_verificados`; protocolo y coherencia del objetivo; variantes en formato «4.12» reutilizadas ante cambios editoriales; cambio de protocolo → fase C desde el paso 10, con el motivo ya en el turno 1; trazabilidad en el paso 12 |
| `objetivo_v64.py`, `entradas_economicas.py`, `dominios_v64.py`, `trazabilidad_v64.py`, `comparar_zip.py` | Nuevos (§2.2–§2.4) |
| `cierre_v2.py`, `seleccion_plantilla.py` | Vigencia y resolución de la selección en las llamadas a mano |
| `ficha.py`, `informe.py`, `resumen.py` | Objetivo estructurado, avisos de dominio, lecturas con bases parciales, rango con su ámbito en la línea de estado, aptitud de uso y valores de los avisos sin comillas rectas (solo V6.4 experimental) |
| `variantes_configuracion_v64.py`, `comprobacion_conjunta.py`, `configuracion_economica.py`, `comprobar_gramatica.py`, `volcar_datos_v63.py` | Parámetros variados por variante y ámbito; parámetros inactivos y alternativas no numéricas; protocolo; nota de G7; sección 0 antes de la fase A |
| `esquema/fase_c.esquema.json`, `esquema/ficha.esquema.json` | Materialidad separada, bloque `objetivo` y `aptitud_de_uso` |
| `prompts/fase_c_turno1.md`, `fase_c_turno2.md`, `verificacion.md` | Protocolo, materialidad y avisos dentro de los mismos 16 puntos de la auditoría |
| `pruebas/test_integracion_v64.py`, `pruebas/agentes_sinteticos.py` | Grupos E, F y G (de 58 a 127 pruebas) |
| `verificar_paquete.sh` | Mínimo de la batería V6.4: 127 |
| `ANEXO_D_salidas_y_formatos.md`, README de la V6.4 §9, `GUIA_RECORRIDO_SUPERVISADO.md` (nueva) | Formatos, límites 13–15 y recorrido supervisado |

**Lo que no cambia.** La plantilla V6.4 experimental y su referencia, la plantilla V6.3, `config_v2.json`, el kit, los originales (`personaje_v2/empresas_v2/`) y los expedientes de entregas anteriores, incluido el piloto 4.11, conservan sus bytes. Lo comprueba `scripts/comprobar_entrega_4_12.py`.

**Salidas.** Las de la V6.3 y del modo heredado de la V6.4 no cambian, salvo la vigencia, que es general. Las del piloto 4.11, regeneradas con el código final en una copia, tendrían diferencias de presentación o de registro (§2.3) y ninguna de valoración.

**Resultados de Vidrala.** Con las palancas de la 4.11, el código final reproduce el piloto exactamente (§2.5). El cierre nuevo cambia el precio de Sí de 57,74 € a 56,02 € por un solo cambio de juicio, separado y medido.

## 5. Expedientes ejecutados con el código final

| Expediente | Qué es | Agentes reales | Auditoría y cierre | Resultado |
|---|---|---|---|---|
| `cierre_condicionado/Vidrala` | Cierre nuevo de Vidrala, protocolo «objetivo_condicionado» | Extracción (Sonnet); fases A, B y C (Opus); tres auditorías (Opus): las dos primeras aprobaron materiales anteriores a correcciones del código y quedaron archivadas en `historial_cierres/`; la vigente, después de la revisión interna | SA-2dfc317a5da12a95 · material d6ddea627a0b290d · APROBADO | concluido · Vigilar · esperar · objetivo condicionado 56,02 € (provisional; no cubierta por el ámbito: PM1.familia) |
| `cierre_bloqueo/Vidrala` | Copia identificada con «bloqueo_del_objetivo» | Fase C (Opus); auditorías (Opus): una aprobación no consumida (se conserva), una detenida sin escribir, una aprobación archivada en `historial_cierres/` y la vigente, después de la revisión interna | SA-b485abe6363fd044 · material 6111eb9cf586324c · APROBADO | pendiente_de_datos · Vigilar · sin acción · objetivo bloqueado (valor calculado condicional 56,02 €) |
| `viscofan/experimental/Viscofan` | Expediente nuevo con configuración propia | Extracción (Sonnet); fases A, B y C (Opus); dos auditorías (Opus): la primera, archivada en `historial_cierres/`; la vigente, después de la revisión interna | SA-3ede622664324251 · material e0959b899e66d5b8 · APROBADO | concluido · Vigilar · esperar · objetivo condicionado 39,29 € (provisional) |

**Qué quiere decir «con el código final».**
- **Material.** Los tres materiales auditados (fichas e informes provisionales, cadena de trazabilidad, libros, variantes y fases) son los que produce el código final. Los tres expedientes se repitieron desde el paso 11 después de las correcciones de la revisión interna (13-nov, 00:04), tuvieron auditorías nuevas con agentes que no vieron el trabajo y se cerraron con ellas (00:12–00:13). Las cifras de valoración, los estados y las acciones son los mismos que en los cierres anteriores.
- **Lo que no se repitió.** Las variantes se calcularon antes de la corrección R1 y se reutilizan: su instantánea es de la relación «4.12» (216 entradas en Vidrala, sin la fila 13), y la fila 13 se comparó con la del libro de la variante activa en el paso 12, sin diferencias. La ficha y la sección 14 del informe dan esa huella anterior; la cadena de trazabilidad da la nueva (226 entradas en Vidrala). Lo anotó la auditoría del cierre condicionado. Un expediente nuevo calcula las variantes con la relación nueva.
- **Avisos de las auditorías nuevas** (dentro de puntos que pasan; ninguno es un fallo): en los tres, «PM1.familia» lleva `material_para_accion = false` sin un escenario que la aísle. Es un juicio del agente, pero también lo impone la regla: `pipeline.coherencia_v64` exige un booleano y no admite «sin calcular» (null) para un parámetro que el ámbito no calcula (revisión de lo afectado, RA4; límite L15); en el condicionado, la sección 7 cuenta «0 hipótesis sin fundamento suficiente» porque solo cuenta la lista de D10, que se usa para comprar, mientras el objetivo lo condicionan tres subparámetros de P-M1 sin fundamento suficiente (texto heredado que puede confundir); en la copia de bloqueo, la auditoría anotó que las adquisiciones entran en F_hist y no en D_hist, como dice la fase C; en el libro entran en las dos (B55 = Σ Historia!H31:L31, con L31 = L30 + N(L13), y B59 = Σ Historia!H13:L13), así que la frase de la fase C es correcta y el aviso de la auditoría no (revisión de lo afectado, RA3; la auditoría de Viscofan dice lo mismo en su aviso sobre la fila 13); en Viscofan, los cuatro avisos de la cadena son textos heredados que no se usan como dato.
- **Pasos 0–10 de Vidrala.** Se ejecutaron antes de dos correcciones que no tocan su material:
  - la redacción de la sección 0 antes de la fase A, que solo aplica cuando la configuración no es válida por el motor (en Vidrala lo es);
  - el motivo del cambio de protocolo en el turno 1 de la fase C, que en la copia de bloqueo suplió la orquestación.
- **Controles.** El control con las palancas de la 4.11 y la reproducción del heredado de Viscofan se ejecutaron con el código del desarrollo; los cambios posteriores no tocan la valoración. **No se repitieron con el código final.** Los cambios posteriores (fila 13 en la instantánea y en la cadena, avisos de la cadena, cobertura del ámbito, redacción del informe, aptitud de uso y valores de los avisos sin comillas) no entran en el cálculo. Evidencia: en los tres expedientes repetidos desde el paso 11, `precio.json`, `resultados.json`, `configuracion_economica.json`, `configuracion_v64_variantes.json` y `fase_c.json` quedaron idénticos byte a byte a los del cierre anterior.

## 6. Límites pendientes

Los límites relevantes para el uso, con su efecto, su evidencia, sus controles y lo que falta, están en la tabla del §9.6. Además siguen vigentes los límites técnicos de la plantilla, en el README de la V6.4: §8 (1–12, de la 4.11) y §9 (13–15, observados con Viscofan). Lo más importante:
- **Nada adoptado.** Ninguna configuración, estructura de reposición, protocolo ni umbral está adoptado; todas las decisiones siguen en la propuesta humana, sin firmar.
- **Reposición no observada.** La reposición por encima de la amortización (P-M1) no se puede observar con las cuentas publicadas de ninguna de las dos empresas: el nivel del precio de Sí es condicional.
- **Solo motor B.** La V6.4 experimental solo cubre el motor B. En los expedientes originales, cinco de las seis empresas (Aarsleff, Hermes, Nike, Rational y la Vidrala original) usaron el motor A.
- **Sin ensayo en el tiempo.** No hay contraste con decisiones en el tiempo.
- **Fuentes incompletas.** Falta el PDF del Bundesbank con sus bytes, y las ediciones exactas de cinco ejercicios de Viscofan.

## 7. Alcance real de las pruebas

**Ejecutadas con el código final**, primero sobre una copia limpia del árbol final y después sobre la descompresión del ZIP final (esta última, en el registro externo `munger_v2_r1_entrega4.12_validacion_supervisada_y_Viscofan.VERIFICACION.txt`, que va fuera del ZIP):
- **Ronda definitiva sobre la copia limpia (13-nov, 01:03–01:57).** `verificar_paquete.sh completa`: PASA en 22 min, con manifiesto, entorno, piloto 35, 114/114, 30/30, integración V6.4 **127/127**, trazabilidad 78/78, integridad 103/103, solicitudes 55/55, estados 28/28, resumen 45/45 y cierre 55/55.
- **Controles de las entregas.** Los 18 dan lo que dice `resultados/LEEME_CONTROLES_HISTORICOS_4_12.md` (la 4.12, 63 de 63). Sus salidas son las de referencia de `resultados/controles_historicos_en_arbol_4_12/`.
- **Manifiesto después.** Ningún archivo modificado, ausente ni de más.
- **Reinicio del contenedor.** Interrumpió los controles en el 13.º. Se repitieron los 18 sobre la misma copia, que seguía intacta frente al manifiesto; los doce que ya habían terminado dieron la misma salida.

**Ejecutadas durante el desarrollo** (`REGISTRO_PRUEBAS_4_12.md`):
- grupos de la batería después de cada corrección;
- las réplicas de los tres expedientes;
- la reproducción del fallo de vigencia;
- el control con las palancas de la 4.11;
- la reproducción del heredado de Viscofan;
- el contraste de la Historia de Viscofan;
- las diferencias del piloto 4.11.

**Solo conservadas (no se repitieron en esta entrega):**
- la reconstrucción externa de la V6.4 en otro entorno (se conserva su comparación);
- las fases con agentes reales y las auditorías de los expedientes de entregas anteriores, incluido el piloto 4.11, que no se reabre;
- la réplica de Fable de la 4.11 como implementación: se usa como herramienta, sin rehacerla.

**No probado:**
- el motor A o C con la V6.4 y las empresas financieras;
- el recálculo en Excel;
- ejecuciones repetidas de los agentes;
- un ensayo en el tiempo;
- las ediciones originales de cinco ejercicios de Viscofan y el PDF del Bundesbank.

## 8. Revisión interna

**Qué se hizo.** Una revisión con Fable, en un contexto separado que no vio el trabajo, del código, los expedientes y los documentos de la entrega (`revision_interna/ENCARGO_REVISION_INTERNA_4_12.md` y `REVISION_INTERNA_4_12.md`, 12-nov, 23:10–23:30). Motivo de usar Fable: es la comprobación de mayor consecuencia de la entrega (lo que se dice de la aptitud para decisiones con dinero real) y conviene que la haga un modelo distinto del que hizo el trabajo; el resto del procedimiento se hizo con Opus. Se avisó a la persona responsable antes de lanzarla.

**Resultado (hecho).** 0 bloqueantes, 5 importantes (R1–R5), 4 menores (R6–R9) y 5 observaciones (R10–R14). Ninguno cambia cifras de valoración, estados ni veredictos de los expedientes.

| Hallazgo | Respuesta |
|---|---|
| R1 · La instantánea y la cadena no cubrían la fila 13 de la Historia | Corregido en el código (§3). Prueba nueva (G) |
| R2 · Fechas de los precios mal descritas en este informe | Corregido en este informe: cada precio con su fecha |
| R3 · «Hipótesis no cubiertas: ninguna» casi vacía; errónea en Vidrala para P-M1 | Corregido en el código (§3). En Vidrala aparece «PM1.familia». Prueba nueva (F) |
| R4 · Textos de evidencia de Viscofan incoherentes con «0 avisos» | Corregido en el código (§3): la cadena de Viscofan lleva 4 avisos. Prueba nueva (G). Los textos heredados no se reescriben: son del expediente de origen |
| R5 · El tratamiento del objetivo depende de dos juicios del agente que nada contrasta | **No se corrige en el código**: contrastarlos exigiría un umbral o una regla de materialidad, que el encargo no permite adoptar. Se declara como límite (L15, §9.6), se corrige la frase de §2.2 y la lista de la revisión económica de Vidrala, y la propuesta humana lleva una decisión nueva (D412-FUNDAMENTO) |
| R6 · θ = 0,5 funciona como central en Viscofan aunque se declare «sin central» | Aclarado en el contraste de Viscofan: θ = 0,5 es el punto de cálculo de la activa, no una central adoptada |
| R7 · Avisos de dominio solo en la activa | Lectura de todas las variantes (`resultados/dominios_variantes_4_12.md`) y frase del README corregida. En Vidrala, las dos variantes con R0 y sin P-M1 (solo_N1 y solo_N2, esta última el extremo superior del rango, 65,72 €) llevan activo el aviso de inversión fija negativa en el MALO; la explicación de la tabla es una interpretación, no comprobada celda a celda (RA5). El pipeline sigue calculándolos solo en la activa (límite) |
| R8 · «Sesgo pequeño» sin calcular | Medido sobre copias en Viscofan: −0,71 € con θ = 0,5; sin cifra con θ = 1 (L13) |
| R9 · En Viscofan, la r usada está por debajo de la r mínima de la hoja | Recogido en el contraste de Viscofan y en las limitaciones |
| R10 · Baterías completas sin ejecutar sobre el código final | Se ejecutan en la verificación final sobre la copia limpia y la descompresión del ZIP (§7) |
| R11 · Avisos de las auditorías | Redacción del informe corregida (`informe.py`) |
| R12 · Restos del original en `cierre_bloqueo/Vidrala` | La propia revisión comprobó que no dan vigencia a nada. Se dejan como están: borrarlos sería editar la copia sin necesidad |
| R13 · ¿Recibió la fase A de Viscofan la fase A heredada? | No la recibió; lo dicen las instrucciones exactas de cada relevo (`resultados/relevos_agentes_4_12.md`) |
| R14 · «186 celdas contrastadas» sin su salvedad | Corregido (§9.3) |

**Después de las correcciones (hecho).** Los tres expedientes se repitieron desde el paso 11 con el código corregido y tuvieron auditorías nuevas (§5). Al repetirlos apareció un defecto más, de la 4.12, que la revisión no había visto (los valores de los avisos en JSON, §3); se corrigió con su prueba.

**Segunda revisión, de lo afectado (hecho).** Con Fable otra vez, en un contexto separado y con aviso previo a la persona responsable (13-nov, 00:15–00:27; `revision_interna/ENCARGO_REVISION_DE_LO_AFECTADO_4_12.md` y `REVISION_DE_LO_AFECTADO_4_12.md`). Motivo: comprobar con un modelo distinto que las correcciones resuelven los hallazgos sin abrir fallos nuevos. Resultado: 0 bloqueantes, 1 importante (RA1), 6 menores (RA2–RA7) y 5 observaciones (RA8–RA12). Confirma que las correcciones no cambian ninguna cifra, que cada auditoría responde a su solicitud y a su material, y que las pruebas nuevas fallarían con el código anterior. Estado de R1–R14 según esa revisión: resueltos R4, R6, R9, R11, R13 y R14; resueltos en parte R1, R2, R3, R7 y R8 (por RA1–RA6); R5 y R12, no corregidos y bien declarados; R10, pendiente de la verificación final.

| Hallazgo | Respuesta |
|---|---|
| RA1 · Importante · El control de la entrega comparaba la huella de la relación nueva con la guardada de la anterior y daba falso en los tres expedientes | Corregido: `comprobar_entrega_4_12.py` usa `EE.comparar` con el libro de la variante activa, como los pasos 10 y 12 del pipeline |
| RA2 · R8 medido solo en el exceso (B60); falta decir que con el exceso corregido θ > 0,60 queda por debajo del rango | Declarado en L13, en el contraste de Viscofan y en la lectura de sensibilidad: medición parcial (sin D_hist ni f) y equivalencia exacta θ ≈ 0,60 ↔ θ = 1 de la plantilla (38,22 €) |
| RA3 · El §5 repetía como hecho un aviso erróneo de dos auditorías (las adquisiciones entran en D_hist y en F_hist) | Corregido en el §5, con las celdas del libro |
| RA4 · La regla exige un booleano en `material_para_accion` aunque el ámbito no calcule el parámetro | Declarado en el §5 y en L15. No se cambia la regla: cambiaría el contrato de la fase C |
| RA5 · La respuesta a R7 no citaba el aviso activo en solo_N1 y solo_N2; la explicación de la tabla es una regla del script | Corregido en la respuesta a R7 y en la lectura de dominios, que marca esa explicación como interpretación |
| RA6 · La revisión económica y la propuesta daban 90,10 € sin la fecha | Corregido (cierre del 31-dic-2025; el de Viscofan, del 3-nov-2026). La comparación de protocolos no da el precio de mercado |
| RA7 · Cifras y horas anteriores en los documentos | Corregidas: grupos F (36) y G (17), la instantánea de 216 y 226 celdas, «una prueba nueva y una actualizada», la hora de G 17/17 y las diferencias del piloto (cuatro de los campos comparados, la aptitud de uso y la redacción de la sección 14) |
| RA8 · El aviso nuevo de la cadena (R4) tiene alcance limitado y su prueba depende del expediente real de Viscofan | Límite declarado: dos formatos de fecha, solo precio, capitalización y acciones, y tolerancia del 0,1 %; puede dar un falso aviso con un texto correcto de fechas mixtas |
| RA9 · `PM1.roic_terminal` nunca puede salir cubierto con la regla nueva | Límite declarado: un falso aviso del lado prudente; hoy no condiciona ningún objetivo |
| RA10 · La fila 13 entra en la cadena también en el modo heredado, donde no entra en el valor | Límite declarado; no afecta a ningún expediente de la entrega ni a la V6.3 |
| RA11 · Las instrucciones a las auditorías nuevas decían que la instantánea incluye la fila 13; en estos expedientes la guardada no la incluye | Reconocido: la instrucción fue imprecisa. La auditoría del condicionado lo detectó y lo comprobó con el libro; el §5 lo explica |
| RA12 · Detalles: «None» en el informe de Viscofan, la guía sin cambios, D412-FUNDAMENTO ausente del §9.5, redacción antigua en `lecturas_sin_protocolo` | El §9.5 nombra ya D412-FUNDAMENTO. `lecturas_sin_protocolo` dice ya «en la activa y N escenarios calculados» (no se usa en los tres expedientes, que tienen protocolo). La guía no cambió después de la primera revisión: lo que decía el encargo era impreciso. «None» en los valores de un aviso queda como detalle de presentación: corregirlo cambiaría el material auditado |

**Lo que no cubre ninguna revisión con Fable.** Las correcciones de RA1–RA12 se hicieron después de la segunda revisión y no se revisaron con Fable. RA1 lo comprueba el control de la entrega en la verificación final (§7). Las demás son de redacción, salvo dos líneas de código que no tocan los expedientes entregados (`lecturas_sin_protocolo` y el control de la entrega).

## 9. Evaluación expresa de aptitud de uso

**Qué es y qué no es.** Esta evaluación es de la entrega 4.12, separada de la aprobación del pipeline.
- Una auditoría APROBADO dice que un expediente cumple las 16 reglas de su contrato. Esta evaluación no cambia ese contrato ni ningún veredicto histórico.
- La evaluación se refleja de forma diferenciada en las salidas nuevas: `ficha.json → aptitud_de_uso`, un bloque en la sección 1 del informe y la columna `aptitud_de_uso` del resumen V6.4. Las tres dicen «experimental».
- **La confianza se refiere a lo examinado:**
  - versión 4.12;
  - motor B con la plantilla V6.4 experimental;
  - dos casos: Vidrala (base 2025, configuración de demostración) y Viscofan (base 2025, configuración propia);
  - uso supervisado;
  - el ámbito de las variantes calculadas.
- **No se atribuye una aptitud general al sistema** por haber completado dos empresas o por coincidir con una réplica.

**El resultado sigue siendo experimental.**

### 9.1 Integridad y funcionamiento técnico comprobados

**Hechos.**
- Batería V6.4 de 127 pruebas (grupos A–G) y baterías V6.3 con sus mínimos, en la verificación final sobre una copia limpia (§7).
- Vigencia de las aprobaciones en las primeras llamadas de las cuatro vías (grupo E y reproducción del fallo de la 4.11).
- Plantillas con su huella estricta y reconstrucción comparada miembro a miembro.
- Tres expedientes reales cerrados con agentes reales y auditorías APROBADO de agentes que no vieron el trabajo. Cada código 10 se resolvió; ningún expediente se entrega en espera.
- Conciliación anual y terminal correcta en cada escenario y variante.

**Lo que no cubre.**
- Las pruebas usan casos sintéticos y dos empresas.
- El recálculo se hace con LibreOffice en este entorno; no se ha probado el recálculo en Excel.
- La auditoría y la revisión interna las hacen modelos de la misma familia; la revisión externa de la 4.12 está pendiente.

### 9.2 Resultados financieros reproducidos

**Hechos.**
- Vidrala: el código final reproduce exactamente el piloto 4.11 con sus palancas. La réplica independiente coincide en los 16 libros finales del cierre.
- Viscofan: el código final reproduce exactamente el expediente heredado, en V6.3 y en V6.4 heredado. La réplica coincide en los 14 libros finales.

**Qué significa.** Reproducir quiere decir que la aritmética del modelo es la misma con las mismas entradas, y que otra implementación llega a las mismas cifras. **No** quiere decir que la valoración sea correcta, ni que las entradas y las hipótesis describan bien a la empresa.

### 9.3 Hipótesis y convenciones económicas: contrastadas o pendientes

**Contrastadas con fuentes** (hechos):
- las cifras de la Historia de Viscofan (186 celdas cuyas cifras se encontraron, por sus dígitos, en la publicación del ejercicio: es un contraste, no una verificación de la partida en el original);
- la causa de la anomalía del tipo de Viscofan en 2025;
- el circulante de Viscofan, conciliado con las notas;
- las series de capex, amortización y adquisiciones de las dos empresas;
- la separación de cambios de mecánica, configuración, datos y juicio en las dos.

**Pendientes, ninguna adoptada:**
- **La configuración de cada empresa:** N1, N2, N3, estructura y familia de P-M1, λ o θ, convenciones y cartera.
- **Los parámetros de ensayo:** r = 0,09 en Vidrala; en Viscofan, la r heredada (9,0 %) está por debajo de la r mínima de la hoja (9,5 %, aviso A2) y es la palanca más influyente (A5). También las probabilidades y k = 3 experimental.
- **La coherencia entre el S2C de los años y el ROIC del terminal** (Q-ROIC1).
- **El terminal de R1** cuando las ventas siguen bajo el máximo conservado.
- **El protocolo del objetivo y los umbrales de los dominios.**
- **El desglose del capex por destino:** no se publica en ninguna de las dos empresas. Sin él no se puede elegir la estructura de P-M1 ni observar λ o θ.
- **Contraste con resultados posteriores:** ninguna hipótesis se ha contrastado con lo que pasó después (no hay backtest).

### 9.4 Uso supervisado que permite la evidencia

**Permite** (interpretación):
- analizar empresas cuyo motor por los hechos es el B, con la V6.4 experimental como capa de sensibilidad y el modo heredado (V6.3) como control;
- que la persona responsable revise cada relevo con la guía `personaje_v2/GUIA_RECORRIDO_SUPERVISADO.md`;
- leer los resultados como valores calculados condicionales.

**Para qué sirve:**
- ver qué hipótesis mueven el precio de Sí y cuánto;
- saber si la zona se sostiene en todas las variantes calculadas (en las dos empresas, sí: «caro»);
- identificar qué información buscar, como el desglose del capex por destino;
- comparar configuraciones y protocolos sobre el mismo material.

**No permite:**
- emitir órdenes de compra o venta, ni fijar precios de compra o tamaños de posición a partir del objetivo;
- usarlo con empresas cuyo motor por los hechos sea el A o el C, ni con financieras;
- tomar «concluido» o APROBADO como garantía de que el resultado es correcto.

### 9.5 Condiciones pendientes antes de apoyar decisiones con dinero real

1. **Decisiones humanas** de la propuesta (sin firmar): el uso del sistema (D412-USO), el protocolo del objetivo, la regla del fundamento suficiente (D412-FUNDAMENTO), los dominios, el terminal de R1 y, por empresa, si se adopta alguna configuración.
2. **Validación económica de P-M1.** Un desglose del capex observable, o un método de estimación defendible y replicado, y una prueba de que la estructura elegida describe a cada empresa.
3. **Ensayo en el tiempo («point-in-time»).** Varias empresas y años, cada uno con la información disponible en su fecha, para medir la calidad de las decisiones. No se ha hecho. Los dos expedientes usan cuentas de 2025 con fecha de análisis del 12-nov-2026: Vidrala, con el precio de cierre de 2025 (90,10 €, diez meses y medio antes del análisis); Viscofan, con el del 3-nov-2026 (54,70 €).
4. **Más empresas, y el motor A.** Medir también la variación de los juicios de los agentes en ejecuciones repetidas, porque aquí cada fase se ejecutó una vez.
5. **Revisión externa de la 4.12,** independiente de los modelos que construyeron y auditaron.
6. **Fuentes completas.** El ejemplar del Bundesbank con sus bytes, y las ediciones exactas de Viscofan que cita la fase 1, o una nueva extracción sobre las ediciones conservadas.
7. **Procedimiento de uso.** Firma humana de cada decisión, control de la frescura del precio y de la tasa, y registro de los resultados frente a lo que pase después.

### 9.6 Limitaciones relevantes

| # | Limitación | Qué resultado o decisión puede afectar | Qué evidencia la identifica | Qué controles existen | Qué información o trabajo falta | Consecuencia para el uso |
|---|---|---|---|---|---|---|
| L1 | Reposición por encima de la amortización no observada (estructura, familia, λ/θ de P-M1) | El nivel del precio de Sí y cualquier objetivo: Vidrala 51,29–65,72 €, Viscofan 38,22–41,81 €. En Viscofan, el objetivo condicionado emitido (39,29 €) es el valor en θ = 0,5, un punto de cálculo y no una central (θ = 0: 40,35 €; θ = 1: 38,22 €) | Variantes calculadas, comparación homogénea y revisión económica de cada empresa | Variantes con zona; protocolo del objetivo; objetivo condicionado o bloqueado; ámbito explícito, con las hipótesis no cubiertas (en Vidrala, la familia) | Desglose del capex por destino; vida útil y coste de reposición | El objetivo es un valor condicional: no sirve como precio de compra |
| L2 | Configuración económica no adoptada (N1, N2, N3 y convenciones) | Precio de Sí y ponderado (Vidrala −8,73 € frente al heredado; Viscofan −2,52 €) | `comparacion_homogenea.md` de cada expediente | Modo heredado como control; componentes aislados | Decisiones VIDRALA-CONFIG y VISCOFAN-CONFIG | Los expedientes son ensayos |
| L3 | Discontinuidad entre el S2C de los años y el ROIC del terminal (Q-ROIC1) | El valor terminal, que pesa entre el 48 % y el 62 % en Viscofan | `datos_revision_economica.md` de cada expediente | Variante SR2; desviación G8 justificada en la fase C | Decisión sobre Q-ROIC1; contraste con el ROIC histórico | Sensibilidad de ±1 € en Vidrala y ±0,4 € en Viscofan con las variantes calculadas; mayor fuera de ellas |
| L4 | Terminal prudente de R1 con el MALO bajo el máximo conservado | El valor MALO de Vidrala (unos 2,5 €/acción) | Aviso de dominio y revisión económica §4 | Aviso visible y evaluado por la fase C | Especificación alternativa con su réplica (D411-TERMINAL-R1) | MALO conservador; no cambia la zona |
| L5 | r, probabilidades y k = 3 son de ensayo; en Viscofan, la r heredada (9,0 %) está por debajo de la r mínima de la hoja (9,5 %) y es la palanca más influyente | El valor, la zona y la acción | Aviso de alcance de cada expediente; avisos A2 y A5 de la ficha de Viscofan | Ninguna variante los mueve: quedan fuera del ámbito | Decisión humana y análisis de sensibilidad propio | «La zona no cambia» no cubre estos parámetros. Con una r mayor, el valor baja: «caro» no está en riesgo por ese lado |
| L6 | Datos de la etapa 1 incompletos en Vidrala (ceros pendientes de verificación, evidencias no verificables) | Flujos de intereses, arrendamientos y adquisiciones | Cadena de trazabilidad; `ficha.datos_etapa1_incompletos`; línea de estado | Un cero pendiente nunca se presenta como dato; S-19 | Confirmar esos ceros con las fuentes (N4) | Estado del libro «NO LISTO · evidencias incompletas» |
| L7 | Fuentes en otra edición (Viscofan 2016, 2018, 2021–2023) y PDF del Bundesbank sin bytes | Las citas de esas fuentes y la tasa sin riesgo de Vidrala | Inventario de fuentes; registro de avance §6 | Contraste por contenido; ninguna edición se llama original | Ediciones exactas; bytes y huella del PDF | Citas contrastadas, no verificadas en el original |
| L8 | Solo el motor B | Empresas cuyo motor por los hechos es A o C | Límite del modelo (H3 de la 4.11); fase A de Viscofan «ajustada» | Límite del modelo declarado, nunca forzado | Extender la integración al motor A | No se puede usar con esas empresas |
| L9 | Dos empresas, una configuración cada una y una ejecución por fase | La generalización y la estabilidad de los juicios | `viscofan/CONTRASTE_VISCOFAN_4_12.md` | Réplica numérica (no de juicio) | Más empresas y ejecuciones repetidas | La confianza se limita a estos casos |
| L10 | Sin ensayo en el tiempo; fechas distintas: Vidrala con el precio de cierre de 2025 y análisis de noviembre de 2026; Viscofan con cuentas de 2025 y precio de noviembre de 2026 | Saber si las decisiones habrían sido buenas; la vigencia del precio en la fecha de análisis | Fechas separadas en cada expediente | Aviso «no es un backtest»; aviso A3 de Viscofan (precio y acciones separados más de 90 días) | Ensayo con la información de cada fecha; precio de la fecha de análisis | No hay evidencia de calidad de decisión |
| L11 | Revisiones internas con modelos de la misma familia | Errores comunes no detectados | Registro de la revisión interna | Contexto separado; auditorías que no ven el trabajo | Revisión externa | — |
| L12 | Protocolo del objetivo no adoptado | El estado y la acción publicados (concluido o pendiente de datos) | `COMPARACION_PROTOCOLOS_4_12.md` | Cada expediente declara su protocolo; sin protocolo, ningún objetivo oficial | Decisión D412-PROTOCOLO | La presentación del objetivo depende de una elección abierta |
| L13 | Amortización de los derechos de uso dentro de la D&A (límite 13 del README) | Las bases de Λ y Θ | Análisis de la configuración de Viscofan | Límite declarado; medido en Viscofan sobre copias (`viscofan/resultados/sensibilidad_derechos_de_uso.md`): con θ = 0,5, contar solo la amortización que se repone con capex baja el precio de Sí de 39,29 a 38,58 € (−0,71 €, sigue en «caro» y por encima del extremo inferior del rango calculado, 38,22 €); con θ = 1 no hay cifra, porque el cálculo saldría del dominio declarado o exigiría editar una fórmula protegida de la plantilla. La medición es parcial: solo cambia el exceso (B60), no la base de reinversión de D_hist (B55) ni, por ella, f (revisión de lo afectado, RA2). Con el exceso corregido, θ ≈ 0,60 equivale exactamente a θ = 1 con el de la plantilla (38,22 €, el extremo inferior del rango); un θ mayor queda fuera del dominio y por debajo de ese extremo (estimación lineal del revisor para θ = 1: unos 36,8 €, sin recalcular) | Separarla en la plantilla, con definición, versión y réplica propias | Sesgo medido de −0,71 € con θ = 0,5 (parcial); con θ ≥ 0,60, por debajo del rango calculado |
| L14 | Dominios sin umbral (f, inversión fija negativa, terminal de R1, S2C inerte); el pipeline solo los calcula sobre la variante activa | Estructuras con parámetros extremos | `dominios_v64.py`; `resultados/dominios_variantes_4_12.md`, con todas las variantes (λ = 1,25 de Vidrala: f = 1,309) | Avisos con valores; la fase C los evalúa; uno material condiciona el objetivo y no admite comprar | Decisión D412-DOMINIOS; avisos de todas las variantes en las salidas | La persona tiene que leer los avisos, también los de las variantes |
| L15 | Las banderas por parámetro de la fase C (material para el objetivo, fundamento suficiente) son juicios que ninguna regla contrasta (revisión interna R5). La regla exige además un booleano en `material_para_accion` aunque el ámbito no calcule el parámetro (revisión de lo afectado, RA4) | Qué hipótesis condicionan el objetivo; con «comprar», qué entra en D10. La regla R1 sale con fundamento suficiente en Vidrala y sin él en Viscofan | `objetivo_v64.py`; `pipeline.coherencia_v64`; los `fase_c.json` | La auditoría revisa la coherencia con el ámbito y la acción, no el fundamento | Decisión D412-FUNDAMENTO (regla conservadora para comprar); evidencia con página para cada «fundamento suficiente» | La lista de condicionantes depende del juicio del agente: se lee como tal |
| L16 | Alcance de los controles nuevos de la 4.12 (revisión de lo afectado, RA8–RA10) | Los avisos que lee la auditoría: la cadena solo contrasta el precio, la capitalización y las acciones, con dos formatos de fecha y una tolerancia del 0,1 %; `PM1.roic_terminal` nunca sale cubierto por el ámbito porque solo varía ligado a la estructura; la fila 13 entra en la cadena también en el modo heredado, donde no entra en el valor | `trazabilidad_v64.py`; `objetivo_v64.cubiertas`; `REVISION_DE_LO_AFECTADO_4_12.md` | Pruebas de los grupos F y G; la del R4 depende del expediente real de Viscofan | Ampliar el contraste a más campos y formatos, con pruebas sintéticas propias | Un aviso puede faltar (campos no contrastados) o sobrar (fechas mixtas, roic terminal): se lee como ayuda a la auditoría, no como garantía |

## 10. Trabajo pendiente para un producto fiable para decisiones con dinero real

En orden de dependencia (propuesta, no adoptada):
1. **Decisiones humanas** de `propuestas/PROPUESTA_HUMANA_4_12.md`: uso, protocolo, dominios, terminal de R1 y configuración de cada empresa.
2. **Revisión externa de la 4.12.**
3. **Integración del motor A** (encargo propio; no se inicia en este).
4. **Más empresas del motor B y del A,** con ejecuciones repetidas de las fases de juicio para medir su variación.
5. **Ensayo en el tiempo** con la información de cada fecha (cuentas, precio y tasa), para medir la calidad de las decisiones.
6. **Evidencia para P-M1:** el desglose del capex por destino o un método de estimación replicado.
7. **Cambios de definición con su réplica:** la amortización de los derechos de uso, el terminal de R1 y Q-ROIC1.
8. **Procedimiento de uso:** firma humana de cada decisión, frescura de los datos de mercado y registro de resultados.

## 11. Siguiente paso para el motor A y más empresas

- **Motor A.** Especificar qué significan N1, N2, N3 y P-M1 cuando el valor sale del flujo de caja del accionista con el exceso de caja (C76). Después, ampliar la plantilla experimental con el modo heredado igual a la V6.3 también para el motor A, con su réplica independiente y su grupo de pruebas.
- **Primer ensayo del motor A.** Con una de las empresas originales que usan el motor A (Aarsleff, Hermes, Nike, Rational), siguiendo el mismo protocolo de fuentes, configuración propia y agentes reales que Viscofan.
- **Más empresas del motor B.** Seguirían el procedimiento de Viscofan, que ya está automatizado en sus scripts:
  - inventario de fuentes;
  - reproducción del heredado;
  - análisis propio de la configuración;
  - expediente nuevo;
  - separación de cambios;
  - comparación homogénea;
  - réplica.
