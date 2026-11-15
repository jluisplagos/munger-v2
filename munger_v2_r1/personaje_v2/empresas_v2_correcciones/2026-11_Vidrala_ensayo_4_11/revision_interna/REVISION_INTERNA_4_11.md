# Revisión interna de la entrega 4.11 · primera integración económica experimental del motor B

**Revisión interna (Claude, contexto separado; no es la revisión externa).**

- **Quién revisa.** Un agente de Claude que no participó en el trabajo y que solo ha leído el material. No es la revisión externa (ChatGPT) ni la sustituye.
- **Encargo.** `revision_interna/ENCARGO_REVISION_INTERNA_4_11.md`: fórmulas, concatenación del flujo, fuentes y límites económicos, más el piloto.
- **Fecha.** 12-nov-2026. Las huellas de abajo se tomaron a las 13:13 (hora del sistema).
- **Alcance de lo escrito.** Este informe es el único archivo que el revisor ha escrito en el paquete. Los temporales están en `/tmp/claude-0/-home-claude/d8a381ee-40a6-50ca-8023-33d75d699d51/scratchpad/revision_interna/`.

## Veredicto en breve

**Sin bloqueantes.** El material puede entregarse como implementación experimental no adoptada.

| Gravedad | Número | Cuáles |
|---|---|---|
| Bloqueante | 0 | — |
| Importante | 4 | H1, H2, H3, H4 |
| Menor | 10 | H5 a H14 |
| Observación | 8 | O1 a O8 |

Ningún hallazgo cambia una cifra entregada. Los cuatro importantes son de flujo y de reglas:

- **H1:** una garantía documentada que no se cumple en un sentido;
- **H2:** una salida que no dice con qué modelo se calculó;
- **H3:** un juicio de la fase A que el sistema condiciona sin declararlo;
- **H4:** dos reglas escritas del personaje que dan estados distintos para el piloto, sin que nada decida entre ellas.

Los cuatro pesan sobre todo en el siguiente uso previsto, con dos o tres empresas más.

## Huellas SHA-256 de lo revisado

| Qué | Archivo | SHA-256 |
|---|---|---|
| Plantilla | `v6/v64_experimental/entregables/Plantilla_V6.4_experimental.xlsx` | `04bab281d2a1a4b236e9714e069c9ade8a9c7d467f090b7ce435cce0040d9bef` |
| Referencia | `v6/v64_experimental/referencia/referencia_V6.4_experimental.json` | `8ee7ef7ed4d74962a005265e0e8056dfae7b29cb35dbdadf5a5b3ccadbec0281` |
| Constructor | `v6/v64_experimental/scripts/construir_v64_experimental.py` | `55cf02f447ef174df4e9b22575c09bdaa17ba5f528c82663e4953e523a51ff17` |
| Pipeline | `personaje_v2/scripts/pipeline.py` | `56e30946ef68fc50b959bcdf825bdffdf1627677afe3bb2c543278fc82204370` |
| Configuración del piloto (cambio de base) | `configuracion/cambio_de_base_piloto.json` | `4a4e75193e012273c09739a573ff3fdf16448733253d8c33bdbdf44f26571aae` |
| Configuración del piloto (económica) | `piloto/Vidrala/configuracion_economica.json` | `a50f097c437770bc734aa22125c494e884f47a6af422c5f1bc8730be46c15be6` |
| Estado del piloto | `piloto/Vidrala/estado_pipeline.json` | `dec3868573d975da244b838863956058db2211ac0f315eeb9a532b88e1d1c6ee` |
| Libro evaluado del piloto | `piloto/Vidrala/Vidrala_v63_evaluada.xlsx` | `cd88f96d6017a591fb552748d6d8bc17aa6a4d716ad8d4a86429cad77da5b18d` |
| Ficha del piloto | `piloto/Vidrala/ficha.json` | `7f8eff40ee4755c29de75f1e38e6efce6d261443204103e65826591a40c53add` |
| Informe del piloto | `piloto/Vidrala/informe.md` | `3d8fc0982988e2cf78c81f9b2acfea688f358584aa37736528994b98c9e60859` |
| Auditoría del piloto | `piloto/Vidrala/auditoria.md` | `138a9026222f7f48b5e47686c3bb021a7a967fc948289cce2c849df3b977d046` |
| Documentación de la plantilla | `v6/v64_experimental/docs/README_V6.4_experimental.md` | `09cc9b366a8323d55208885bdedfe3e6fda69d8ad56991be510a9c0076ab3385` |
| Informe de integración | `INFORME_INTEGRACION_4_11.md` | `394ad86d991b62bfcb2a8b73582aa1b121a1d661ae22b2021c95bf3171c89209` |
| Propuesta humana | `propuestas/PROPUESTA_HUMANA_4_11.md` | `6a0acd6584f7224c9e0bf40165e66503cdc17be94bfd4210c583f8758e585858` |
| Registro de pruebas | `REGISTRO_PRUEBAS_4_11.md` | `9c2a7452c8342d4beac805712efd89897a7ed9702757690476bc0fdf7f8c5321` |

Las rutas sin prefijo son relativas a `personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_11/`.

**El árbol cambió durante la revisión.** El código, la plantilla y el expediente del piloto no cambiaron: el piloto está quieto desde las 12:43:29. Sí se reescribieron documentos mientras se revisaba: el informe de integración, la propuesta, su guion y los registros llevan hora 13:06:25, y a las 13:06:42 aparecieron los registros `concordancia_Vidrala_v63_datos.*` del piloto y del control. Los números de línea de este informe corresponden a las versiones de la tabla, que a las 13:35 seguían sin cambios.

## 1. Qué se revisó y qué no

### 1.1 Método

- **Solo lectura.** No se ejecutaron LibreOffice, `recalc.sh`, `pipeline.py`, `verificar_paquete.sh` ni la batería. Lo que necesita una ejecución se pide en el §5.
- **Lectura de valores.** Los libros recalculados se leyeron con openpyxl. Los valores son los que dejó LibreOffice; no se comprobó el comportamiento en Excel.
- **Réplica propia.** El revisor escribió en Python el modelo del motor B experimental y lo comparó con los valores de los libros. No es una réplica a ciegas: se escribió después de leer el constructor, la especificación y los análisis fuente. Compara los tres escenarios y el ponderado, no las filas de sensibilidades.
- **Reconstrucción.** El constructor se ejecutó sobre la V6.3 con salida al scratchpad, sin tocar el árbol.

### 1.2 Jerga usada

- **Motor B:** la valoración «operativo con deuda» de la plantilla. Descuenta el flujo de caja libre (FCF) a una tasa operativa (r_op) y resta la deuda neta.
- **Modo heredado y modo experimental:** en heredado la V6.4 calcula como la V6.3. En experimental aplica las piezas nuevas, si la configuración es válida.
- **N1, N2, N3:** tipo impositivo normalizado, margen de partida escrito a mano y regla de reinversión cuando las ventas caen. En N3, R0 es la regla simétrica de la V6.3 y R1 libera solo circulante y conserva la capacidad.
- **P-M1:** el tratamiento de la reposición por encima de la amortización. Tiene estructuras (H, S, SR1, SR2, SRF), dos familias de requisito (Λ, con el parámetro λ, y Θ, con θ) y un tratamiento de la cartera de clientes adquirida (P0: su amortización no se repone).
- **f y f_fija:** factores que reestiman las ventas por euro invertido (S2C) o la inversión fija, para descontar la parte de la inversión histórica que fue reposición. D_hist es la reinversión histórica, Rh la parte atribuida a reposición y F_hist la inversión fija neta histórica.
- **NWC:** circulante comercial dividido por las ventas.
- **Terminal:** el año 11, que representa todos los años posteriores al décimo.
- **Ponderado y precio de Sí:** el valor medio de los tres escenarios con sus probabilidades, y el precio que cumple la regla de asimetría con k = 3 (una convención experimental).
- **Zona:** la posición del precio de mercado frente a esos valores; «caro» es la más alta.
- **Variantes:** recálculos mecánicos del libro del piloto con otra configuración, hechos por el pipeline en el paso 10.
- **Material auditado y vigencia:** la lista de archivos cuya huella respalda una aprobación, y la regla que retira la aprobación si alguno cambia.
- **Código 2:** la salida con la que el pipeline se niega a empezar, sin escribir nada.

### 1.3 Revisado y conforme (hechos comprobados)

**Plantilla y fórmulas.**

- Frente a la V6.3 hay 1.994 fórmulas cambiadas (1.984 del Motor, 9 de Diagnóstico y Panel!A1), 7.870 nuevas y ninguna quitada; en total, 18.834. Los 4 textos fijos cambiados son los declarados.
- En las 124 filas de valoración del Motor, las 16 columnas envueltas (AU:BD, BF, BL, BP, BQ, BS, BT) conservan la fórmula heredada literal en su rama heredada. Las columnas BU:DY siguen el mismo patrón en las 124 filas, sin excepciones.
- La reconstrucción con el constructor da el mismo SHA-256 `04bab281…`.
- Coinciden con la especificación de la réplica, con el README §5 y con los análisis fuente (`analisis_n1_n3.py`, `analisis_pm1.py`, `analisis_reinversion_4_8_1.py`):
  - R1 con el máximo conservado (constructor, líneas 378 y 385–386);
  - f y f_fija (líneas 211–214) y los parámetros efectivos, que solo actúan con B76 o B78 verdaderos (líneas 216–229);
  - el crédito de H en los años y en el terminal (líneas 389 y 405);
  - la cartera P0 (línea 236);
  - las convenciones de años y terminal (líneas 387–388 y 403–404);
  - el terminal (líneas 400–406), con el ROIC multiplicado por f solo en SR2;
  - Diagnóstico C10, C11 y C15 (líneas 443–449).
- Hoja «Configuración V6.4»: 28 comprobaciones (B96:B123) en el orden y con los motivos del README §4. Vacío, cero y error se tratan de forma distinta: un 0 en N1 o N2 se usa, un texto se rechaza y un error cuenta como «no cumple» (`=IFERROR(condición,TRUE)`, línea 277). Un modo mal escrito no cae al heredado en silencio: invalida las filas.
- Las 124 filas leen la misma bandera (B76), así que el DCF inverso, el tornado y las sensibilidades de un libro usan todos el modelo activo o todos el heredado.

**Réplica propia frente a los libros recalculados.**

- Piloto: MALO 45,5602, NORMAL 61,9264, BUENO 81,7362, ponderado 62,6151 y precio de Sí 57,7423, con diferencias del orden de 1e-14.
- Las 13 variantes del piloto: diferencia máxima 5,7e-14.
- Los 117 casos de la batería: 94 calculan y coinciden (diferencia máxima 4,7e-13) y 23 se rechazan, cada uno con su motivo y con el estado INCOMPLETO en Motor!B255.

**Flujo.**

- Las 96 celdas de configuración del libro de datos y del evaluado son las de `configuracion_economica.json`.
- Las 23 huellas de `material_auditoria.json` coinciden con los archivos. La auditoría responde a la solicitud SA-a843decaaf51d16e sobre el material `6dd711561fd92f12`.
- La variante «activa» coincide con `precio.json` (diferencia 0).
- Las fases no pueden escribir la hoja de configuración: no está en su lista de celdas permitidas.
- `coherencia_v64` (`pipeline.py`, líneas 1130–1155) exige una evaluación por parámetro activo, el mantenimiento con `adoptada = false` y que «la zona no cambia» esté respaldado por las variantes. La fase C del piloto evalúa los 12 parámetros activos y afirma la zona solo de las 13 variantes calculadas.
- El material auditado incluye la configuración, la selección de plantilla y las variantes (`cierre_v2.py`, líneas 31–38).
- Control heredado: mismas cifras que la 4.10.1, con diferencia 0.

**Cambio de base.**

- 128 celdas de evidencia en 23 filas, 7 datos vaciados, 10 entradas sustituidas y 3 notas retiradas.
- El expediente de origen está intacto: su huella es la de la 4.6.1.
- La copia de la etapa 1 tiene la misma huella (`0276426f…`) en el control y en el piloto.
- El revisor reprodujo en lectura la comprobación `comprobar` sobre el libro de datos y el evaluado del piloto: «CONCUERDA Y SIN RESTOS» en los dos, dentro del rango que esa comprobación examina (ver H9).

**Fuentes del piloto.**

| Entrada | Valor | Fuente comprobada |
|---|---|---|
| N1 | 0,220541 | `t_rec` de `…_4_7_1/financiero/matriz.json`, exacto |
| N2 | 0,185467 | `m_rec` del mismo archivo, exacto |
| N3: existencias y deudores | 252,454 y 315,821 | `texto/CF_2025.txt`, pág. 2 |
| N3: acreedores | 352,841 | `texto/CF_2025.txt`, pág. 3 |
| NWC | 0,147038 | (252,454 + 315,821 − 352,841) ÷ 1.465,16 |
| Cartera P0 | 4,492 (2025), 4,921 (2024), valor neto 21,858 | ES 2025, págs. PDF 52–53; `analisis_pm1.py` |
| Precio | 90,10 | ES 2025, pág. PDF 97 |
| Acciones | 35.182.858 | 35.206.258 emitidas − 23.400 propias; ES 2025, pág. PDF 67 |
| E | 3.169,9755058 | 90,10 × 35,182858 |
| rf | 2,85 % | Bundesbank; sin PDF en el paquete (límite declarado) |

**Cifras de los documentos.** Las tablas y distancias del informe de integración §2–§4 y los «efectos calculados» de la propuesta se rehicieron a partir de los archivos y coinciden: componentes aislados, estructuras, convenciones, 56,04 % y 35,91 %, −10,3 %, 0,33–7,79 € y la fe de erratas (35,45 % y 26,17 %).

### 1.4 No revisado o no ejecutado

- La batería, el pipeline, el recálculo y `verificar_paquete.sh`. Los flujos de H1 y H3 se analizaron leyendo el código; de H1 se simuló solo la función `comprobar`.
- Las filas de sensibilidades, tornado y DCF inverso se revisaron por estructura de fórmulas, no por valor. Las cubre numéricamente la réplica independiente del paquete, que no se volvió a ejecutar.
- El comportamiento en Excel.
- Los motores A, C y D.
- El texto original del encargo 4.11: se usó su resumen en el README §5.
- El extracto del piloto frente a los PDF, y la calidad del juicio de las fases A y B, salvo su coherencia con la configuración.
- `VERSION`, `CONTINUIDAD.md`, el registro de la entrega y el LEEME de controles históricos, que quedan fuera por encargo.
- `scripts/comprobar_entrega_4_11.py`, que apareció a las 13:06:25, durante la revisión.

## 2. Hallazgos

**Escala.**

- **Bloqueante:** impide entregar el material como implementación experimental no adoptada. Por ejemplo, una cifra entregada errónea, el modo heredado distinto de la V6.3, una configuración inválida que calcula o una aprobación que sobrevive a un cambio.
- **Importante:** no altera cifras, pero incumple una garantía documentada o un criterio expreso del encargo, o condiciona el siguiente uso.
- **Menor:** errata, laguna de presentación o de control con efecto acotado.
- **Observación:** se deja constancia; no pide cambio.

### Importantes

#### H1 · La selección de plantilla no se detiene cuando un expediente V6.3 se ejecuta con la V6.4

**Hecho comprobado.**

- `seleccion_plantilla.py`, función `comprobar` (líneas 52–83): la plantilla del expediente solo se compara si existe `plantilla_activa.json` (línea 59). Un expediente V6.3 nunca tiene ese archivo, porque `registrar` (líneas 86–96) solo lo escribe con la V6.4. Con la configuración V6.4 y sin ese archivo, la función solo pide que `configuracion_economica.json` exista y sea válida (líneas 72–82) y deja seguir.
- Simulación del revisor, solo de esa función, sobre una carpeta de prueba del scratchpad que imita un expediente V6.3 cerrado (un archivo vacío con nombre de libro de datos y un estado en el paso 14; la función solo mira qué archivos hay):
  - con una configuración económica válida y `config_v2_v64_experimental.json`, devuelve «puede seguir»;
  - sin configuración económica, se detiene;
  - con configuración económica y `config_v2.json` (V6.3), se detiene.
- `pipeline.py`, `main`: después de `comprobar` (líneas 1300–1303) se escribe `plantilla_activa.json` (línea 1317), se pasa la vigencia (línea 1320) y `reaplicar_configuracion` (línea 1346) intenta aplicar la configuración a libros que no tienen la hoja. `configuracion_economica.py` (líneas 234–235) falla con «el libro … no tiene la hoja» y el análisis termina en `no_entregable · fallo_de_implementacion` (líneas 1347–1350).
- `cierre_v2.py` (líneas 31–38): `configuracion_economica.json` y `plantilla_activa.json` son material auditado. Su aparición cambia el material de un expediente V6.3 cerrado.
- Tres documentos afirman lo contrario:
  - README §7, líneas 194–197: se detiene con código 2, sin escribir nada, si «el expediente se preparó con otra plantilla»;
  - Anexo D §D.12, línea 343: «Un expediente V6.4 que se ejecuta con la configuración V6.3 (o al revés) se detiene con código 2 sin escribir nada»;
  - propuesta, D411-PLANTILLA, línea 21: «un expediente de una versión se detiene con código 2 en la otra».
- La batería prueba cuatro cruces (`test_integracion_v64.py`, líneas 356, 362, 364 y 396), entre ellos el de un expediente V6.4 ejecutado con la V6.3. El inverso no está.

**Interpretación.** Leído el código, no ejecutado: el fallo hace ruido y no produce cifras, pero no es «sin escribir nada». Escribe `plantilla_activa.json` en un expediente V6.3. Si ese expediente tenía un cierre vigente, la vigencia lo archivaría, porque el material cambia. Después tampoco arrancaría con la V6.3, que se detendría con código 2 hasta que alguien borrase a mano los dos archivos. Importa por el siguiente paso: el informe de integración §6.4 (línea 248) propone preparar las otras empresas «con una copia del original si no cambia» la base. Una copia de un expediente V6.3 lleva sus libros y su estado: es este caso.

**Propuesta.**

1. En `comprobar`, con la V6.4 y sin `plantilla_activa.json`, detener con código 2 si la carpeta ya tiene libros `*_v63_datos.xlsx` o `*_v63_evaluada.xlsx`, o un `estado_pipeline.json` con pasos hechos.
2. Añadir el cruce al grupo C de la batería.
3. Precisar en el informe §6.4 cómo se prepara un expediente V6.4 cuando la base no cambia: qué se copia y qué no.
4. Mientras no se corrija, ajustar las tres frases citadas o declarar el límite.

#### H2 · El resumen no dice con qué modelo se calculó la fila

**Hecho comprobado.**

- `resumen.py`, líneas 11–14: la lista de columnas no tiene plantilla, modo de configuración, marca de objetivo provisional ni fecha del precio.
- `piloto/resumen_v2.csv`: la fila del piloto es `"Vidrala, S.A.",2026-11-12,concluido,…,B,90.1,EUR,45.56…,57.74229205598012,62.6151093424602,caro,esperar,…,APROBADO`. No se distingue de una fila V6.3. Lleva la fecha de análisis (12-nov-2026) junto a un precio que es del 31-dic-2025.
- `cierre_v2.py`, líneas 572–573: si la configuración no trae `resumen_csv`, el destino es `resumen_v2.csv` en la carpeta que contiene el expediente. Ni `config_v2.json` ni `config_v2_v64_experimental.json` lo traen.
- `resumen.py`, línea 95: al publicar, se sustituye la fila que hubiera de la misma empresa.
- El encargo de esta revisión pide que «la ficha, el informe y el resumen» reflejen el modelo activo. La ficha y el informe lo hacen; el resumen, no. Ningún documento lo declara como límite.

**Interpretación.** En el piloto no hay daño: el destino está aislado porque el expediente cuelga de `piloto/`. Ese aislamiento sale de la disposición de carpetas y no de una regla. Un expediente V6.4 creado junto a los V6.3 publicaría en el resumen común una fila experimental, no adoptada y con objetivo provisional, y sustituiría la fila V6.3 de esa empresa sin ninguna marca.

**Propuesta.** Elegir una de dos vías.

- **Mínima:** dar a `config_v2_v64_experimental.json` un `resumen_csv` propio, para que una fila experimental nunca comparta archivo con las V6.3, y decirlo en el Anexo D §D.12.
- **Completa:** añadir al final columnas para la plantilla, el modo, la marca de provisional y la fecha del precio, vacías en las filas V6.3. Antes hay que mirar si la batería del resumen y los controles históricos dependen de la lista de columnas.

#### H3 · Con la configuración experimental, el sistema presenta a la fase A los motores A y C como «no calculables» y, si los elige, da una causa equivocada

**Hecho comprobado.**

- `piloto/Vidrala/entrada_v63.md`, líneas 7 y 9: «Motor A: NO calculable · … La configuración experimental V6.4 solo es aplicable al motor B». Lo mismo para el C.
- Ese archivo se escribe por primera vez en el paso 3 (`pipeline.py`, línea 571), antes de que la fase A elija el motor, y simula siempre los tres motores (`comprobar_entrada_v63.py`, líneas 179–183). El que hay ahora en la carpeta es el que el paso 7 reescribe después de la fase A; la sección de motores sale de la misma simulación.
- `prompts/fase_a.md`, líneas 8 y 16: describe «Motores calculables» como «qué motores tienen los datos de Historia que exigen» y añade: «Si eliges uno no calculable, el pipeline se detendrá en `pendiente_de_datos` y te lo dirá: elige con eso delante». El prompt no tiene ninguna indicación para la V6.4.
- `pipeline.py`, líneas 627–631: si la fase A elige un motor no calculable, el análisis termina en `pendiente_de_datos · falta_de_datos`, con «datos de Historia que exige el motor» como lo que hace falta.
- No hay prueba de este recorrido en la batería: el grupo C usa siempre el motor B.
- En el piloto, la fase A eligió B y lo dejó escrito en `fase_a.json`: «La configuración V6.4 del ensayo no es la razón: lo elegiría igual en la V6.3». Vidrala usa el motor B desde el ensayo 4.5.

**Interpretación.** El resultado del piloto no cambia. La laguna es del flujo: la configuración la escribe la orquestación antes de la fase A, y lo que la fase A lee le dice que solo B es calculable y que elija con eso delante. El informe de integración §6.2 dice que el motor B «no se puede forzar»; tal como está, el sistema empuja hacia él. Si la fase A eligiera A o C, la causa registrada sería una falta de datos que no existe. La causa real es un límite del modelo. Según el propio informe, cinco de las seis empresas analizadas usaron el motor A.

**Propuesta.**

1. En `entrada_v63.md`, separar «no calculable por datos» de «no cubierto por la configuración experimental».
2. En `pipeline.py` 627–631, cuando el motivo sea la configuración, terminar con la causa `limite_del_modelo` y decir qué hacer: modo heredado o V6.3.
3. Añadir al prompt de la fase A un párrafo para la V6.4: el motor se elige por los criterios del personaje, como si la configuración no existiera.
4. Añadir una prueba con agentes simulados.
5. Declarar el límite en el README §8.6 y en el informe §4.

Como alternativa de diseño, que decide la persona responsable: fijar la configuración experimental solo después de que una fase A en modo heredado haya elegido el motor B.

#### H4 · Dos reglas escritas del personaje dan estados distintos para el piloto, y nada decide entre ellas

Es el tercer aviso de la auditoría del piloto. El revisor lo examinó con criterio propio y concluye que es más que un aviso de presentación.

**Hecho comprobado.**

- **Lo que hizo la fase C** (`fase_c.json`):
  - En `configuracion_v64.parametros`, PM1.estructura, PM1.familia y PM1.parametro llevan `material_para_conclusion = true`. En `observaciones` precisa: «Solo P-M1 … es material para el objetivo; ninguna parte de la configuración lo es para la acción esperar».
  - En `revision_datos_ausentes`, el dato «Capex previsto 2026 y siguientes, total o por destino» afecta a «mantenimiento P-M1 (λ) y precio objetivo» y lleva `material_para_conclusion_favorable = false`. Motivo: «La acción esperar no depende de él …; deja provisional el objetivo». `alguno_material = false`.
  - Estado `concluido`, acción `esperar`, precio objetivo 57,74 marcado provisional.
- **Regla A, datos ausentes** (personaje §15, línea 235; prompt de la fase C, línea 22): un dato ausente es material si sin él no se puede sostener «la conclusión favorable (`comprar`, o `esperar` con precio objetivo)». En ese caso «no la emito: cierro con cubo `Vigilar`, sin acción, y el pipeline pone `pendiente_de_datos`». El orden de la línea 233 pone esta regla antes que la del fundamento.
- **Regla B, hipótesis sin base** (personaje §14, línea 225; Anexo B §B.6.7, línea 165): «con `esperar` y alguna hipótesis sin base, el precio objetivo se marca provisional con la hipótesis que lo condiciona».
- **Prompt de la fase C para la V6.4** (línea 29): «Si un parámetro es material para la conclusión, aplica las reglas de siempre (fundamento material, datos ausentes, estados): no fuerces `concluido`, `comprar` ni un precio objetivo».
- **Lo que comprueba el pipeline:**
  - con `esperar`, el precio objetivo tiene que ser el precio de Sí (`pipeline.py`, líneas 1238–1243): no existe un `esperar` sin objetivo;
  - si algún dato ausente se marca material, el estado tiene que ser `pendiente_de_datos` (líneas 1178–1184);
  - de `material_para_conclusion` solo se comprueba que sea un booleano (líneas 1143–1145); no tiene consecuencia mecánica.
- El Anexo D §D.12 (línea 350) no dice si «conclusión» es la acción o el objetivo.
- No hay umbral numérico de materialidad en el personaje, los anexos ni los prompts. El «10 %» del aviso describe el −10,3 % medido.
- La auditoría lo dejó así: «la fase C lo deja como objetivo provisional (B.6.7) y no como dato material S-19, con motivo escrito: es su criterio, no lo cambio, y conviene que lo mire la revisión externa».
- El informe de integración §3 describe el tratamiento (línea 190: «Por eso el objetivo es provisional y no se fuerza otra conclusión»), pero su lista de avisos de la auditoría (líneas 194–200) no recoge este.

**Interpretación.**

- La fase C aplicó la regla B y lo razonó. La letra de la regla A también encaja: la conclusión del piloto es exactamente «`esperar` con precio objetivo», y la propia fase C dice que el objetivo depende de P-M1 y que el dato ausente es parte de lo que lo resolvería.
- Las dos lecturas coinciden en lo principal: no hay compra y el cubo es Vigilar. Difieren en el estado (`concluido` frente a `pendiente_de_datos`) y en si se publica una acción y un precio objetivo.
- La dependencia la crea la configuración de demostración. En modo heredado el mismo dato ausente no mueve ninguna cifra, porque la V6.3 no tiene parámetro de reposición.
- Lo que hace importante el hallazgo es el siguiente uso. Casi ninguna empresa publica el desglose de su inversión entre reposición y crecimiento. Con cualquier estructura P-M1 activa, el objetivo dependerá de λ o de θ. Con la lectura A, todos esos expedientes terminarían en `pendiente_de_datos`. Con la B, todos concluirían con un objetivo provisional. Conviene decidirlo antes de probar otras empresas.
- El revisor no cambia el estado ni la conclusión del piloto. Considera defendible la opción de la fase C y fundado el aviso de la auditoría.

**Propuesta.**

1. Llevar la cuestión a la propuesta humana como una decisión más: qué regla manda cuando un parámetro experimental es material solo para el precio objetivo.
2. Definir en el Anexo D §D.12 a qué se refiere `material_para_conclusion`: a la acción, al objetivo o a los dos por separado.
3. Hacer que `coherencia_v64` aplique la regla que se elija.
4. Añadir este aviso a la lista del informe de integración §3 y, mientras no se decida, declararlo en el §4.

### Menores

#### H5 · El recuento «Fórmulas nuevas: 7.844» está desfasado

**Hecho.** README línea 64 e informe de integración línea 33 dicen 7.844. La plantilla final tiene 18.834 fórmulas (lo dice el propio README, línea 40) y la V6.3, 10.964: son 7.870 nuevas. Reparto: Motor 7.068, «Conciliación B» 670, «Configuración V6.4» 131 y Panel!C18. La cifra 7.844 era la de la plantilla anterior al ajuste de trazabilidad (18.808 fórmulas).

**Propuesta.** Corregir las dos líneas. Panel!C18 es una fórmula nueva que el README §3 no nombra.

#### H6 · El «valor sin crecimiento» experimental no recoge la cartera P0, y cuatro lecturas experimentales no tienen contraste numérico

**Hecho.**

- Constructor, líneas 415–416: en experimental, BL = NOPAT₀ ÷ r_op − B89 ÷ r_op + puente. B89 es el requisito a ventas constantes (línea 229). Coincide con el README, línea 164.
- Con P0 activa, los flujos de los años suman la amortización de la cartera y rebajan el requisito mientras dura (línea 390). BL no lo recoge.
- Estimación del revisor para el piloto: el valor actual de esa partida es 19,8 M€, unos 0,56 €/acción. BL da 58,19; con la cartera daría unos 58,75.
- La cifra llega al texto del piloto: «casi el valor sin crecimiento (58,19)» (`ficha.json`, `cambios_vs_etapa1[30]`).
- Las ramas experimentales de BL, BP, BQ y Diagnóstico B176:D177 no las contrasta nadie por valor. `replica/INFORME_REPLICA.md`, línea 154, deja fuera «Panel, Diagnóstico y demás hojas». La batería solo las inventaría como fórmulas cambiadas (línea 85).

**Interpretación.** BL no entra en el valor, en el ponderado ni en el precio de Sí. Es una cifra de lectura. La diferencia es de un 1 % y no cambia el sentido de la frase.

**Propuesta.** Declarar en el README §5 que BL no incluye la cartera, o incluirla. Añadir a la batería un contraste numérico de estas cuatro lecturas.

#### H7 · El §1 del informe da el precio objetivo sin «provisional», y la ficha no lleva la marca en un campo propio

Es el primer aviso de la auditoría.

**Hecho.**

- `informe.py`, líneas 114–115: la línea de estado añade «· precio objetivo 57.74» sin más.
- `ficha.json`, `decision`: `{"accion": "esperar", "precio_objetivo": 57.74, "condicion": null, …}`. La palabra «provisional» está en `insumos_decision_cartera.fundamento` y en textos de las fases, no en un campo que un programa pueda leer.
- La regla (Anexo B §B.6.7, línea 165) pide marcar el objetivo como provisional «en C104, la ficha y el informe».

**Interpretación.** El revisor coincide con la auditoría. El informe lo dice en los §2, §8, §10 y §12, pero la línea de estado del §1 es la que más se lee y la que se copia.

**Propuesta.** Un campo en `ficha.decision` con la marca y la hipótesis que condiciona el objetivo, que `informe.py` lleve al §1 y que pueda usar el resumen (H2).

#### H8 · `ficha.etapa1.cubo` copia el texto de C104 de la etapa 1

Es el segundo aviso de la auditoría.

**Hecho.** `ficha.py`, línea 180. En el piloto: `"cubo": "0% · Vigilar · precio de Sí ≈ 48 € (estimado)"`, con `precio_de_si` y `fecha` a `null`.

**Interpretación.** De acuerdo con la auditoría. Es D-FICHA-ETAPA1, abierta desde la 4.10.1 y declarada. No es nueva ni la causa la 4.11.

**Propuesta.** Ninguna nueva. Sigue pendiente de decisión humana.

#### H9 · Quedan tres textos de la base anterior en el Control maestro, fuera del rango que examina la comprobación

**Hecho.**

- `cambiar_base.py`, líneas 254–261: `comprobar` busca restos en las filas 17–82 y 107–175 del Control maestro.
- En el libro de datos y en el evaluado del piloto, y en el de datos del control:
  - F5: «Pendiente de inversor: 3a (2023–25) / 5a (2021–25) / LTM 30/06/2026»;
  - D88: «FY vs LTM: métricas actuales a LTM 30/06/2026; …»;
  - D100: «Intereses pagados en explotación 2019–2025 y 1S2026 (IPP G-16, línea 1421)».
- F5 pasa a `datos_v63.json`. No llega a los textos que leen las fases ni a la ficha o el informe.
- Los registros de concordancia, creados a las 13:06:42, cubren el libro de datos. Del evaluado no hay registro; la reproducción en lectura del revisor da el mismo resultado.

**Interpretación.** «CONCUERDA Y SIN RESTOS» es cierto dentro del rango examinado. No afecta a ningún valor. Las filas 84–102 son un bloque de auditoría heredado de la etapa 1 que describe la base anterior.

**Propuesta.** Ampliar el rango de `comprobar` a la cabecera y al bloque 84–102, o decir en el informe §1 qué filas quedan fuera. Guardar también la concordancia del libro evaluado.

#### H10 · Las variantes no quedan atadas al libro entregado ni se vuelven a contrastar

**Hecho.**

- `configuracion_v64_variantes.json` del piloto: `libro_origen_sha256` empieza por `502543e8`. El libro entregado es `cd88f96d…`. Las variantes se calculan en el paso 10, antes de que la fase C escriba sus celdas.
- `pipeline.py`, líneas 1112–1128: las variantes se recalculan si la huella del libro cambia, pero la función no se vuelve a llamar después de la fase C. El paso 12 no comprueba que la variante «activa» siga siendo `precio.json`.
- La batería (línea 381) titula la prueba «ligadas al libro evaluado» y comprueba solo que existen.
- `variantes_configuracion_v64.py`, líneas 132–135: una variante sin zona queda fuera de `zonas_calculadas` sin aviso. `ficha.py`, línea 221, cuenta todas las variantes, calculen o no.

**Interpretación.** En el piloto no hay efecto: la «activa» coincide con `precio.json` y las 13 calculan. El riesgo es latente: si la fase C corrigiera una celda que entra en el valor, las variantes quedarían viejas sin que nada lo detecte.

**Propuesta.** Comprobar en el paso 12 que la variante «activa» coincide con `precio.json`. Hacer que una variante que no calcula impida afirmar «misma zona en todas» y que la ficha cuente solo las calculadas.

#### H11 · El parámetro que la fase C declara material no tiene variante calculada

**Hecho.**

- Las 13 variantes mantienen λ = 1,15. No hay ninguna de λ ni de la familia Θ.
- `fase_c.json`, `PM1.parametro`: «Sin variante calculada. Réplica (estimación, sin afirmar zona): λ 1,10 → precio de Sí 60,12; … λ 1,25 → 53,00».
- La propuesta, D411-PM1-PARAMETRO (línea 105), recomienda «λ como rango de sensibilidad (1,10–1,25)». Sus «efectos calculados» (línea 111) solo dan las convenciones.
- El rango está en la propia configuración: `trazabilidad.PM1.parametro` dice «1,15; rango 1,10–1,25».
- La réplica del revisor da 60,1154 con λ = 1,10 y 52,9960 con λ = 1,25. Coincide con la estimación de la fase C.

**Interpretación.** La fase C lo trata bien: no afirma zona. Pero la persona responsable tiene que decidir entre un punto y un rango sin que el efecto del rango haya pasado por el libro.

**Propuesta.** Añadir a `variantes_configuracion_v64.py` los extremos del rango del parámetro cuando la configuración lo declare. Para esta entrega, pedir el recálculo de los dos extremos (§5).

#### H12 · Los límites que imprimen la ficha y el informe del piloto no incluyen dos que están activos en él

**Hecho.**

- `ficha.py`, líneas 223–225: tres límites fijos, iguales para todo expediente. El informe del piloto los copia en el §14.
- No está el terminal con R1 (README §8.1). En el MALO del piloto está activo: las ventas del año 11 (1.421,3) quedan por debajo del máximo (1.465,16) y el terminal carga 16,39 M€ de inversión fija para crecer.
- Estimación del revisor: unos 0,67 €/acción en el MALO y 0,13 €/acción de ponderado. Es el valor actual de esa carga en los cuatro años en que las ventas seguirían por debajo del máximo.
- Tampoco está que, con R1, la palanca S2C del MALO no actúa. En el piloto la inversión fija para crecer es 0 en los diez años del MALO, porque las ventas nunca superan las de 2025. Lo detecta la fase C y lo recoge la auditoría como aviso. No está en el README §8 ni en el informe de integración §4.
- La propuesta no dice que k = 3 es experimental ni que el ensayo no es un backtest. Las dos cosas sí están en el informe del piloto y en el de integración.

**Propuesta.** Que los límites de la ficha dependan de la configuración activa: con R1, el del terminal y el de la palanca inerte. Añadir a la propuesta una frase de contexto con k = 3 experimental y «no es un backtest». Añadir la palanca inerte al README §8 y al informe §4.

#### H13 · Hay dominios que ni se comprueban ni se declaran

**Hecho.**

- **f sin cota superior.** La comprobación 24 (constructor, línea 268) solo rechaza si D_hist − Rh ≤ 0. Con los datos del piloto, f es 1,16 con λ = 1,15; 1,89 con λ = 1,5; y 17,8 con λ = 2,0. La configuración deja de estar definida en λ ≈ 2,06. Todas esas λ se aceptan, porque solo se exige λ ≥ 1. En la réplica del revisor el valor no se dispara: baja de forma lineal con λ. Lo que pierde sentido es el S2C reestimado.
- **Inversión fija para crecer negativa.** La fórmula de los años multiplica por (1 ÷ (S2C·f) − NWC) (línea 385). Nada comprueba que ese término sea ≥ 0. Es negativo cuando S2C·f supera 1 ÷ NWC. En el piloto haría falta f > 7,6, es decir, λ ≈ 1,9. En una empresa con poco activo fijo y mucho circulante puede ocurrir con f = 1: por ejemplo, con S2C = 4 y NWC = 0,30.
- **Inversión fija terminal negativa.** El README §8.2 lo declara solo para el crédito de H. La misma condición afecta a SRF, donde f_fija reduciría una liberación en lugar de una inversión.
- **g ≤ 0 con R1.** La regla V15 del libro admite un crecimiento perpetuo entre −10 % y 10 %. El terminal no aplica el máximo conservado en ningún sentido. El pipeline lo acota a g ≥ 0 con la lista de la gramática (`comprobar_gramatica.py`, línea 30).
- En el piloto y en los 117 casos no aparece ninguna de estas situaciones.

**Interpretación.** No afecta a ninguna cifra entregada. Importará al probar otras empresas, sobre todo las de poco activo fijo.

**Propuesta.** Añadir avisos, no rechazos, para f por encima de un umbral y para inversión fija para crecer negativa. Declarar los cuatro dominios en el README §8.

#### H14 · La propuesta humana tiene un texto cortado y tres rutas con la mayúscula cambiada

**Hecho.**

- Propuesta, línea 87: «…con ventas orgánicas a la baja); S c (estructura más coherente según la fase C: SR1)». El guion `scripts/propuesta_humana_4_11.py`, línea 91, corta la evaluación de la fase C a 600 caracteres.
- Propuesta, líneas 163, 181 y 199: «Resultados/aislamiento_entradas_4_11.md» y «Configuracion/cambio_de_base_piloto.json». Las carpetas son `resultados/` y `configuracion/`. El guion, líneas 167–168, pone en mayúscula la primera letra de la evidencia.

**Propuesta.** Cortar por frase o no cortar, y no cambiar la mayúscula cuando la evidencia empieza por una ruta.

### Observaciones

- **O1 · «Conciliación B».** La identidad del FCF es aritmética: las partidas salen de las mismas columnas del motor. Está declarado en la ficha y en el informe. La amortización del terminal se muestra siempre proporcional a las ventas (constructor, líneas 518–519), con independencia de la convención elegida; se cancela en la identidad y solo afecta a la presentación.
- **O2 · Comprobación conjunta.** `comprobacion_conjunta.py`, líneas 27, 56 y 89: admite mover N1, N2, λ y θ aunque el parámetro no esté activo. Mover uno inactivo dejaría la copia sin efecto o inválida. Es conservador. En el piloto no procede.
- **O3 · Cartera P0.**
  - El texto de `cartera_fuente` dice «2021–2022 = 0 (no había cartera)» y «2023 = 0 … (supuesto)». La nota 7 de `texto/CF_2021.txt` a `CF_2024.txt` muestra una cartera anterior, la de Santos Barosa (coste 13.237), totalmente amortizada a 31-dic-2020 y sin dotación en 2021, 2022 ni 2023; la de Vidroporto entra en el saldo reexpresado de 2023 sin amortización acumulada. Los datos son compatibles con los tres ceros y permitirían un texto más preciso. El revisor lo señala y no confirma ningún cero: eso corresponde a la persona responsable.
  - P0 supone que la amortización sigue al nivel de 2025 hasta agotar el valor neto (4,9 años) y que el margen proyectado ya la lleva restada.
- **O4 · Controles mecánicos con la base histórica.** La regla G7 de la gramática (`comprobar_gramatica.py`, líneas 143 y 269) y las referencias mecánicas (`referencias_mecanicas.py`, líneas 101 y 185–188) usan el tipo de la Historia y el S2C sin f también en modo experimental. Es un diseño declarado en `prompts/fase_b.md`, línea 33. En ese modo, la rentabilidad marginal que vigila G7 no es la que calcula el motor. Sin efecto en el piloto.
- **O5 · Ejecución a mano.** `ficha.py`, `informe.py` y `resumen.py` no comprueban la selección de plantilla. Ejecutados a mano sobre un expediente V6.4, sin `--config` ni la variable `MUNGER_CONFIG`, cargarían `config_v2.json`. Leído en el código, no ejecutado.
- **O6 · Salto del requisito en el año 11.** Con la convención activa del piloto (años planos, terminal proporcional a las ventas) el requisito pasa de 19,94 a 25,66 en el NORMAL (+28,7 %) y a 29,96 en el BUENO (+50,2 %). Con la combinación inversa, el requisito cae en el terminal: −16 % y −25 % en el caso `S_T0.50_terminal_g_anios_ventas`. Las dos combinaciones mixtas se aceptan. El efecto de cambiar cada convención está calculado en las variantes.
- **O7 · Registros de pruebas.**
  - `REGISTRO_PRUEBAS_4_11.md`, línea 15: del grupo C constan 15 de 17 pruebas en el desarrollo; las 17 quedan para la copia limpia. A fecha de esta revisión no consta una pasada completa de las 53.
  - `replica/INFORME_REPLICA.md` describe la pasada de 107 casos. La de 117 está en `replica_salida_plantilla_final.txt`.
- **O8 · Detalles de texto.**
  - «λ = 1,15 es ~33 % del exceso histórico» y «todo reposición daría λ ≈ 1,46» (informe de integración, línea 185) usan el exceso sobre la amortización total: 229,4. La hoja usa el exceso sobre la amortización que se repone: 238,8. Con esa base serían un 31 % y λ ≈ 1,48.
  - Diagnóstico B177 queda vacío con g = 0.
  - Las fuentes de N1 y N2 llevan la ruta abreviada «…_4_7_1/…».

## 3. Los tres avisos de la auditoría del piloto, con criterio propio

**Aviso 1 · El §1 del informe da 57,74 sin «provisional».** De acuerdo. Es H7. La regla pide la marca en el informe, y el informe la tiene, pero no en la línea que resume el estado. Es de presentación y se corrige en `informe.py`. Si se regenera el informe del piloto, conviene comprobar antes que la vigencia lo admite sin retirar la aprobación.

**Aviso 2 · `ficha.etapa1` copia el texto de C104.** De acuerdo. Es H8: un asunto abierto y declarado desde la 4.10.1, que la 4.11 no agrava.

**Aviso 3 · El objetivo depende en más de un 10 % de P-M1 y la fase C lo trata como objetivo provisional, no como dato material.** Es H4, y el revisor le da más peso que la auditoría. Resumen del criterio:

- La auditoría tiene razón en que no es evidente: hay dos reglas escritas y la letra de las dos encaja con el caso.
- La opción de la fase C es defendible y está razonada. El revisor no la cambia.
- **La acción no depende de la configuración.** En las 13 variantes calculadas el precio (90,10) supera el ponderado, que como máximo es 71,77, y la zona es «caro».
- **El objetivo sí depende, y el rango es ancho.** En las variantes calculadas el precio de Sí va de 57,03 a 67,00. La réplica del revisor da además:

  | Supuesto | Precio de Sí (réplica) |
  |---|---|
  | λ = 1,10 | 60,12 |
  | λ = 1,25 | 53,00 |
  | θ = 1 (todo el exceso histórico es reposición) | 48,20 |
  | λ = 1,46 (el extremo «todo reposición» que nombra la fase C) | 43,10 |

  Estas cuatro cifras no han pasado por LibreOffice y de ellas no se afirma zona. En la réplica, el precio sigue por encima del ponderado en las cuatro.
- **Lo que falta** es decidir qué regla manda (H4) y enseñar el rango junto al objetivo provisional (H7 y H11). La palabra «provisional» sola no dice que el objetivo puede ir de unos 66 € (V6.3 efectiva) a menos de 50 €.

**Los demás avisos de la auditoría** (C12, C98 y la carga de capex sin ventas del MALO) son de juicio del personaje y no se reexaminan aquí. El tercero tiene una causa mecánica que sí se recoge: con R1 la palanca S2C del MALO no actúa (H12).

## 4. Límites económicos: dónde se declara cada uno

| Límite | README §8 | Informe del piloto | Propuesta humana | Informe de integración |
|---|---|---|---|---|
| El terminal con R1 no aplica el máximo conservado | Sí (§8.1) | **No**, y está activo en su MALO (H12) | Sí (D411-N3 y D411-TERMINAL-R1) | Sí (§4.3) |
| Crédito terminal de H | Sí (§8.2) | No aplica: la activa es SR1 | No | Sí (§4.4) |
| λ y θ son hipótesis, no mediciones | No en §8 (el §1 dice que nada está aprobado) | Sí (§14) | Sí (líneas 87 y 105) | Sí (§4.2) |
| Dominios de f y f_fija | Solo como comprobaciones 24–25 (§4); **no en §8** | No | No | No (H13) |
| P-M1 no resuelta | Sí, en sustancia (§1) | Sí (§14) | Sí, en sustancia (línea 87) | Sí (§4.2) |
| La configuración de demostración no está adoptada | Sí | Sí | Sí | Sí |
| P3 (C48/C49) y C46/C47 | No aplica: es del expediente | Sí | Sí (D411-P3 y D411-C46C47) | Sí (§4.5) |
| k = 3 experimental | No | Sí (alcance) | **No** (H12) | Sí (§4.7) |
| El ensayo no es un backtest | No aplica | Sí (alcance) | **No** (H12) | Sí (§4.7) |

**Límites no declarados que encontró el revisor.**

1. La regla que decide el estado cuando un parámetro experimental es material solo para el objetivo no está fijada (H4).
2. El motor lo condiciona la configuración antes de la fase A (H3).
3. El resumen no identifica el modelo (H2).
4. Con R1, la palanca S2C no actúa en un escenario cuyas ventas no superan el máximo anterior (H12).
5. f no tiene cota superior, y la inversión fija para crecer puede salir negativa (H13).
6. El terminal con R1 y g ≤ 0 (H13).
7. El «valor sin crecimiento» experimental no incluye la cartera P0 (H6).
8. Las variantes no cubren el parámetro material (H11).
9. La comprobación de restos del cambio de base no examina toda la hoja (H9).

## 5. Ejecuciones y recálculos que se piden

El revisor no los ejecutó. Las cifras «esperadas» salen de su réplica o de la lectura del código.

1. **Selección inversa (H1).** Sobre una copia de un expediente V6.3 cerrado, añadir una `configuracion_economica.json` válida y lanzar el pipeline con `config_v2_v64_experimental.json`. Registrar el código de salida, los archivos escritos y el estado. Esperado hoy: no hay código 2, se escribe `plantilla_activa.json`, se archiva el cierre de la copia y el estado es `no_entregable`. Esperado tras la corrección: código 2 y ningún archivo nuevo.
2. **Fase A que elige A con la configuración experimental (H3).** Con agentes simulados. Registrar el estado, la causa y el texto de lo que hace falta.
3. **Extremos del parámetro (H11).** Recalcular el libro del piloto con λ = 1,10 y λ = 1,25. Esperado: precio de Sí 60,1154 y 52,9960, zona «caro». Si se quiere citar el extremo «todo reposición», recalcular también θ = 1 (esperado 48,20) o λ = 1,46 (esperado 43,10).
4. **Batería completa (O7).** Las 53 pruebas en una sola pasada sobre la copia limpia, con la salida guardada. Ya está prevista.
5. **Concordancia del libro evaluado del piloto (H9).** Ejecutar `cambiar_base.py comprobar` sobre `Vidrala_v63_evaluada.xlsx` y guardar la salida.

## 6. Veredicto

**Sin bloqueantes.**

**¿Puede entregarse como implementación experimental no adoptada?** Sí. Lo sostienen los hechos del §1.3: las fórmulas coinciden con sus definiciones, la réplica propia reproduce el piloto, sus 13 variantes y los 117 casos, el control heredado da lo mismo que la 4.10.1, las configuraciones inválidas no calculan, la configuración forma parte del material auditado, las fuentes del piloto coinciden con sus documentos y nada se presenta como adoptado.

**Recomendación de orden.**

- **Antes de entregar, por su bajo coste:**
  - corregir H5 y H14;
  - ajustar las frases que afirman más de lo comprobado (H1: Anexo D línea 343 y propuesta línea 21);
  - añadir al informe de integración el aviso de la auditoría que falta en su lista (H4);
  - declarar H1 a H4 como límites en el informe de integración §4 si no se corrigen ahora.
- **Antes de probar otras empresas:** decidir H4, corregir H1, H2 y H3, y ejecutar las comprobaciones 1 y 2 del §5. H13 también pesa ahí.
- **Para la decisión humana sobre P-M1:** el recálculo 3 del §5 y el rango junto al objetivo provisional (H7 y H11).

Esta revisión no cambia ningún criterio financiero, probabilidad, rentabilidad exigida, escenario ni conclusión, no rellena ningún campo humano y no confirma ningún cero.
