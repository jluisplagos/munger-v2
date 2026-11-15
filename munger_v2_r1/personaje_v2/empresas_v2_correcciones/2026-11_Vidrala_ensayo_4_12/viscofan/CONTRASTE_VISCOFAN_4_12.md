# Viscofan · primer contraste entre empresas (encargo 4.12 §8)

**Qué es.** El resultado del contraste con Viscofan: las fuentes, la reproducción del expediente heredado, la configuración propia, el expediente experimental nuevo con agentes reales y lo que este contraste enseña sobre la generalización. Separa los **hechos comprobados** (con su archivo), las **interpretaciones** y lo que queda **pendiente**. No adopta nada.

**Fechas, por separado.**
- Base económica: cuentas consolidadas de 2025 (31-dic-2025).
- Fecha real de ejecución (fecha de análisis del expediente nuevo): 12-nov-2026; la del origen era el 4-nov-2026.
- Precio: 54,70 €, cierre del 3-nov-2026 (el del expediente heredado).
- Acciones: 45,479209 millones, media ponderada diluida de 2025.
- Tasa sin riesgo: 3,35 %, Bund a diez años del 4-nov-2026 (la del expediente heredado).
- Fuentes: publicaciones consultadas el 12-nov-2026; el informe anual de 2025 es un PDF creado el 25-mar-2026.

El expediente combina cuentas de 2025 con un precio de noviembre de 2026. **No es una valoración a cierre de 2025 ni un backtest**: no se comprueba qué habría pasado después de una fecha con la información de esa fecha.

## 1. Fuentes (hechos comprobados)

**Punto de partida.** El paquete conservaba los JSON de extracción y las referencias a AR_2016.txt–AR_2025.txt, pero ni los PDF ni los textos (`viscofan/fuentes/inventario_fuentes_viscofan.md`).

**Procedencia.** La consola no puede descargar de viscofan.com (el proxy responde 403). Las publicaciones son copias de las que la persona responsable dejó en una carpeta de su ordenador conectada a la sesión, en dos entregas (20:38 y 21:59 del 12-nov-2026). Cada una conserva el PDF, su SHA-256, el número de páginas, el texto con marcas de página y su identificación.

**Doce publicaciones conservadas, de dos clases:**
- **Misma paginación que la fuente que cita la fase 1** (2017, 2019, 2020, 2024 y 2025). Todas las cifras citadas están en la página citada (61/61, 64/64, 63/63, 65/65 y 66/66). Como no hay huella del original, se dice «misma paginación y cifras», no «mismo archivo».
- **Otra edición** (2016, 2018, 2021, 2022 y 2023; dos de 2021 y dos de 2023). Sirven para contrastar cifras por su contenido. **No se llaman «original recuperado».** No llevan el nombre AR_<año> de la fuente de la fase 1.

**Una edición de 2020 se sustituyó.** La de la primera entrega no tenía la paginación de la fase 1 (0 de 63 cifras en la página citada). Se sustituyó por la de la segunda entrega, que sí la tiene. Su huella queda registrada, pero no se conserva ni se usa.

**Contraste de la Historia** (`viscofan/fuentes/contraste_cifras_historia.md`). Las cifras impresas que la fase 1 sumó para cada celda se buscaron, por sus dígitos, en la publicación del ejercicio:
- 186 celdas contrastadas;
- 0 no encontradas y 0 sin publicación;
- 15 sin cifra (ceros con motivo o celdas vacías) y 9 solo con cifras cortas (no concluyentes).

Encontrar los dígitos no prueba que hablen de esa partida, y no encontrarlos en otra edición no prueba que la cifra antigua sea errónea. Es un contraste, no una verificación del original.

**Lo que falta.** Las ediciones exactas que cita la fase 1 para 2016, 2018 y 2021–2023 (sus cifras sí se contrastaron en otras ediciones). Y, para el modelo, un desglose del capex entre mantenimiento y crecimiento, que Viscofan no publica.

## 2. Reproducción del heredado (hecho comprobado)

`viscofan/resultados/reproduccion_heredado.md`. Con el código final, las mismas entradas y las mismas palancas del origen dan **exactamente** su resultado (|Δ| = 0), en la V6.3 y en el modo heredado de la V6.4:
- precio de Sí 43,050965031270174 €;
- ponderado 46,8821465263006 €;
- V = 35,39 / 47,56 / 63,33 €, con probabilidades 0,25 / 0,6 / 0,15;
- zona caro, motor B.

En ese control, «agente simulado» significa copiar sin cambios la salida del agente real del origen. Por tanto, cualquier diferencia posterior no viene del código.

## 3. Configuración propia (hechos y elecciones de ensayo, no adoptadas)

`viscofan/configuracion/analisis_configuracion_viscofan.md`: 61 de 61 cifras comprobadas en su página. **Nada se trasladó de Vidrala** (tipo, margen, cartera, λ ni proporción de mantenimiento).

- **N1 · tipo impositivo** (perímetro: actividades continuadas, consolidado; período 2021–2025, el de la regla heredada). La regla heredada (C52) da 19,83 %. El 10,1 % de 2025 se debe a activaciones de bases imponibles negativas en Estados Unidos (18,0 M€), una causa publicada y cuantificada. Sin ellas, la media es 22,12 %; además sin los ajustes de ejercicios anteriores, 22,66 %. El ensayo usa 22,12 %.
- **N2 · margen de partida.** Se deja vacío por elección explícita: la regla heredada («Último año») da 16,36 %, y el ciclo 2021–2025, 16,38 %. En 2025 no hay partidas no recurrentes materiales, y la empresa dice que los cambios de perímetro no tuvieron efecto material en el EBITDA.
- **N3 · circulante.** Con las líneas del balance, 48,28 % de las ventas en 2025 (48,04 % en 2024). La conciliación con las notas 9 y 14 da 46,79 % solo comercial.
- **Capex y amortización 2021–2025.** El capex fue 1,33 y 1,48 veces la amortización en 2021–2022, y 0,90–0,94 veces en 2023–2025. La amortización de la Historia incluye la de los derechos de uso (5,1–5,8 M€ al año), que se repone con arrendamientos y no con capex. Es el límite 13 del README de la V6.4. **Hecho medido sobre copias** (`resultados/sensibilidad_derechos_de_uso.md`, revisión interna R8): si el exceso histórico se calcula sobre la amortización que se repone con capex (67,864 en lugar de 40,813), con θ = 0,5 el precio de Sí baja de 39,29 a 38,58 € (−0,71 €) y sigue en «caro», por encima del extremo inferior del rango calculado (38,22 €). Con θ = 1 no hay cifra: saldría del dominio declarado de θ o exigiría editar una fórmula protegida de la plantilla, y no se hace. La medición es parcial: solo cambia el exceso (B60), no la base de reinversión de D_hist (B55) ni, por ella, f (revisión de lo afectado, RA2). **Interpretación:** con el exceso corregido, θ ≈ 0,60 equivale exactamente a θ = 1 con el de la plantilla (38,22 €, el extremo inferior del rango calculado), y un θ mayor queda fuera del dominio y por debajo de ese extremo; el revisor estima, de forma lineal y sin recalcular, unos 36,8 € con θ = 1. Es una lectura de sensibilidad, no una variante del expediente ni una corrección adoptada.
- **Adquisiciones.** 7,2 y 8,9 M€ en 2024–2025 (Brasil).
- **P-M1.** SR1 con la familia Θ. θ no se observa: se declara el rango 0–1 y θ = 0,5 solo como punto de cálculo, **sin central económica**. Con Λ, SRF solo estaría definida hasta λ = 1,1413 (límite 14).
- **Cartera.** Legado (sin P0): la ausencia de una cartera identificada no confirma ceros.
- **Combinaciones no definidas.** Se declaran y no se fuerzan: R0 con P-M1 se rechaza; SRF con Λ por encima de λ = 1,1413 no está definida; la inversión fija para crecer de R1 sería negativa si S2C × f > 2,07 (límite 15).
- **Protocolo del objetivo:** «objetivo_condicionado» (ensayo).

## 4. El expediente experimental con agentes reales (hechos comprobados)

`viscofan/experimental/Viscofan`, preparado con `scripts/preparar_viscofan_experimental.py`:
- carpeta nueva con las entradas de partida del origen, sin cambios salvo la fecha de análisis, que es la de ejecución real;
- las publicaciones recuperadas en `texto/`, con su nombre propio;
- la configuración propia y el aviso del ensayo;
- el extracto del origen, como antecedente para contrastar, no como entrada.

Cada código 10 se resolvió con un agente real. Las fases B y C recibieron como referencia de solo lectura las del expediente heredado, porque el encargo pide reutilizar «juicios y decisiones registradas». La fase A no las recibió: solo la herencia de la etapa 1 que lleva `datos_v63.md`, para que eligiera el motor por los hechos. Ninguna recibió nada de Vidrala. Las instrucciones exactas de cada relevo están en `resultados/relevos_agentes_4_12.md`.

| Relevo | Agente | Resultado |
|---|---|---|
| Extracción | Sonnet, esfuerzo medio | Reutiliza el extracto del origen y contrasta cada hecho en las publicaciones recuperadas. Con dos informes anuales añadidos (2021 y 2023, en español) contrasta 12 de los 13 hechos pendientes; queda uno, una previsión para 2024 que el informe de 2023 no recoge |
| Fase A | Opus, esfuerzo alto | **Motor B por los hechos** (C62 «No · financiación cambia mucho»): deuda de 116,8 a 304,1 M€ en 2021–2025, intereses de 0,9 a 8,9 M€ y reparto al accionista por encima de la caja generada. Sin límite del modelo; cubo provisional Vigilar. El agente lo declara ajustado (0,83 veces el EBITDA; el motor A sería calculable) |
| Fase B | Opus, esfuerzo alto | Gramática con código 0 y tres desviaciones G5 justificadas. **Cambia una sola palanca frente al heredado:** el margen objetivo del MALO, de 0,15 a 0,14, por la pendiente de −0,49 puntos al año de 2016–2025 (Historia, fila 29). Retira los apoyos posteriores a la base |
| Fase C (dos turnos, el mismo agente) | Opus, esfuerzo alto | «Esperar», cubo Vigilar. Ningún dato ausente material (22 revisados) y lista D10 vacía. El objetivo queda **condicionado** por PM1.estructura y PM1.parametro, con la acción sostenida en el ámbito calculado |
| Auditoría | Opus, esfuerzo medio, sin haber visto el trabajo | **APROBADO** 16/16 (solicitud SA-e8c8384c2e565c23, material 0dee970f14c042d4). Avisos que no impiden aprobar: el apoyo de B69, p(MALO) = 0,25, son años del 15,1–15,7 % y el MALO es del 14 % (con 0,2 el precio de Sí sube un 4,2 %, sin cambiar la zona); la línea de estado no usa la etiqueta literal «valor calculado condicional» |

**Resultado.** Concluido · auditoría interna APROBADO · cubo Vigilar · acción esperar · objetivo **condicionado y provisional** (lo condicionan PM1.estructura y PM1.parametro, por falta de un desglose del capex por destino):
- precio 54,70 €, zona caro;
- precio de Sí 39,29 € (39,2877008705048), ponderado 43,59 €;
- valores por escenario 30,69 / 44,85 / 60,00 €, con probabilidades 0,25 / 0,6 / 0,15;
- rango calculado del precio de Sí: 38,22–41,81 € en la activa y 12 escenarios (las 13 variantes), todos en «caro»; el precio está un 30,8 % por encima del mayor (la diferencia, dividida entre ese precio de Sí). No es un intervalo de confianza.
- el objetivo condicionado emitido (39,29 €) es el valor en θ = 0,5, que es un punto de cálculo y no una central: con θ = 0 el precio de Sí es 40,35 € y con θ = 1, 38,22 €. La fase C lee θ en la parte baja del rango (revisión interna R6).
- r: la heredada (9,0 %) está por debajo de la r mínima de la hoja (9,5 %, aviso A2) y es la palanca más influyente (A5). Ninguna variante la mueve. Con una r mayor el valor baja, así que «caro» no está en riesgo por ese lado (R9).

**Separación de los cambios** (`viscofan/resultados/separacion_cambios_viscofan.md`):

| Clase | Qué cambia frente al heredado | Efecto en el precio de Sí |
|---|---|---|
| Mecánica (código) | nada: la reproducción del heredado coincide (|Δ| = 0) | 0 |
| Datos | ninguna entrada económica de datos: de las 216, solo cambian las 14 celdas de «Configuración V6.4» y Palancas!B15 | 0 |
| Juicio | margen objetivo del MALO 0,15 → 0,14 (fase B) | −1,245 € (de 43,05 a 41,81 €) |
| Configuración | N1, R1 y P-M1 SR1 · Θ con θ = 0,5 | −2,518 € (de 41,81 a 39,29 €): N1 −1,45 €; R1 0,00 €; P-M1 −1,07 € (no aditivos) |

**Comparación homogénea y réplica** (`viscofan/experimental/resultados/`):
- Heredado con las mismas entradas y palancas: 41,81 €. Activa: 39,29 €.
- Estructuras compatibles: S −0,35 €, SR2 +0,36 €, SRF +1,61 €, H +1,07 € (igual que sin P-M1).
- θ en sus extremos: θ = 0 da +1,07 € (igual que sin P-M1) y θ = 1, −1,07 €.
- Convenciones: −0,09 € y +0,20 €.
- La réplica independiente de la 4.11 coincide en los 14 libros finales: diferencias ≤ 9,9e-14 €/acción en los valores y ≤ 4,8e-12 en la conciliación.

**Textos de evidencia heredados del origen (revisión interna R4).** En el libro, el período del precio («Cierre 6-oct-2026»), la transformación de la capitalización («53,60 × 45,6036 = 2.444,4», del semestral de 2026) y el criterio de las acciones («a 30-jun-2026 = 45,60») vienen del expediente de origen y no corresponden a los valores que entran en el modelo: 54,70 € del 3-nov-2026 y 45,479209 millones de acciones, la media diluida de 2025. Los valores sí salen de `fase1_metadatos.json`, con su fuente. La cadena de trazabilidad corregida lo avisa (cuatro avisos de fecha o valor incoherentes). Efecto acotado: con 45,60 millones de acciones, los valores por acción bajarían un 0,27 %. La auditoría nueva (SA-3ede622664324251, APROBADO) comprobó los cuatro avisos sobre el libro: los valores que entran en el modelo son coherentes y ninguna salida usa las cifras de esos textos. Los textos no se reescribieron: son del expediente de origen, y corregirlos exigiría repetir la fase 1. La fase C no evaluó estos avisos porque no se repitió.

**Cobertura del ámbito calculado.** En Viscofan, «PM1.familia» y «PM1.cartera» no tienen una variante aislada. No aparecen como «no cubiertas» porque la lista solo recoge las hipótesis que condicionan el objetivo, y la fase C les dio fundamento suficiente (es un juicio del agente; límite L15 del informe integrado).

## 5. Estructuras, dominios y lo que pasa en la hoja (hechos e interpretación)

- **R1 no mueve nada en Viscofan.** En los tres escenarios las ventas superan siempre el máximo conservado (el MALO crece un 1 % al año), así que la capacidad conservada nunca actúa. En Vidrala, en cambio, el MALO cae bajo el máximo y R1 resta 1,36 €.
- **H coincide con «sin P-M1».** La inversión para crecer de cada año supera el requisito (4,1 M€ al año con θ = 0,5), así que el crédito de H lo absorbe entero. En Vidrala, H daba +5,35 € frente a la activa.
- **El requisito es pequeño.** 4,1 M€ al año con θ = 0,5, frente a unos 19,5 M€ en Vidrala con λ = 1,15. Por eso P-M1 mueve el precio de Sí unos 1,1 € y no 6,6 €. El exceso histórico de capex sobre la amortización es pequeño (40,8 M€ en 2021–2025, con 2023–2025 por debajo de 1).
- **Dominios.** Ningún aviso activo con la configuración y las variantes calculadas. El factor f = 1,074 es una lectura sin umbral, y la fase C lo da por no material. Las combinaciones no definidas (SRF con Λ por encima de λ = 1,1413; R0 con P-M1) se declaran y no se fuerzan.
- **Discontinuidad en el año 11, como en Vidrala.** La rentabilidad marginal implícita de los años (10,5 %, 15,2 % y 21,1 %) queda por encima del ROIC del terminal (8 %, 11 % y 12 %). Con la convención activa, el requisito salta en el año 11 (+11,6 %, +47,3 % y +77,4 %), pero vale poco en euros.
- **El terminal pesa** el 48 %, el 59 % y el 62 % del valor en MALO, NORMAL y BUENO.

## 6. Qué se reutiliza, qué requiere interpretación propia y qué impide generalizar (interpretación)

**Se reutiliza correctamente** (comprobado en las dos empresas):
- **La mecánica.** Selección explícita, vigencia, variantes atadas a las entradas del libro, conciliación anual y terminal, réplica independiente (16 de 16 en Vidrala y 14 de 14 en Viscofan), cadena de trazabilidad, protocolo del objetivo y aptitud de uso. Funcionan sin cambios con una empresa de otra estructura: circulante del 48 % frente al 15 %, capex por debajo de la amortización en 2023–2025 y un tipo impositivo anómalo en 2025.
- **El recorrido.** Agentes reales en cada relevo; la fase A elige el motor por los hechos, y otro motor habría sido un límite legítimo; la auditoría de 16 puntos funciona sin cambiar su contrato.
- **La reproducción del heredado,** exacta en las dos empresas: un cambio de resultado nunca viene del código sin que se vea.
- **El protocolo de fuentes.** Inventario, huellas, edición identificada y contraste por página, sin llamar original a otra edición. Se aplicó con publicaciones de dos entregas.
- **El esquema de la configuración** (N1, N2, N3, P-M1, con trazabilidad, rangos y combinaciones no definidas), que admite un análisis propio por empresa.

**Requiere interpretación propia de la empresa** (no se puede trasladar):
- **N1.** En Viscofan, la anomalía del tipo de 2025 tiene una causa publicada y cuantificada (activaciones de bases negativas en EE. UU.). La regla que se usó en Vidrala no sirve aquí.
- **N2.** Vacío por elección explícita: el margen de 2025 coincide con el del ciclo y no hay partidas no recurrentes materiales.
- **N3.** El circulante es una magnitud propia. Su definición (balance frente a notas) mueve la razón 1,5 puntos.
- **P-M1.** La familia (Θ frente a Λ) y su rango dependen de las bases de cada empresa. Con las de Viscofan, Λ dejaría SRF sin definir por encima de λ = 1,1413, y el capex de 2023–2025 por debajo de la amortización no apoya un múltiplo de reposición fijo. θ no se observa y no tiene central.
- **La amortización de los derechos de uso.** Pesa distinto en cada empresa dentro de la D&A (límite 13).
- **La cartera.** La ausencia de una cartera identificada no confirma ceros (legado, sin P0).
- **El motor.** Para Viscofan es una decisión ajustada: con un apalancamiento algo menor, la fase A podría elegir el A, que la V6.4 no cubre.

**Límites que impiden generalizar** (interpretación):
- **Dos empresas, una configuración cada una.** Las dos son fabricantes industriales españoles del motor B, con fuentes parecidas. No dicen nada de financieras, de otros sectores ni del motor A o C.
- **Los efectos de los componentes no se trasladan.** R1 resta 1,36 € en Vidrala y 0 en Viscofan; H suma 5,35 € en Vidrala y queda igual que sin P-M1 en Viscofan. Una conclusión sobre un componente depende de las bases y de los escenarios de cada empresa.
- **Los dominios dependen de las bases.** SRF con Λ deja de estar definida a λ = 1,1413 en Viscofan y a ≈ 1,50 en Vidrala. Un umbral único no sería comparable.
- **La parte económica sigue sin validar en las dos.** En ninguna se observa el parámetro de reposición (λ o θ), ninguna publica el desglose del capex por destino, y nada se ha contrastado con lo que pasó después (no hay backtest).
- **Cada fase se ejecutó una vez.** No se ha medido cuánto variarían los juicios de los agentes en ejecuciones repetidas; en Viscofan la fase A declaró el motor ajustado y la fase C dudó de la probabilidad del MALO.
- **Fuentes.** Cinco ejercicios de Viscofan (2016, 2018 y 2021–2023) se contrastaron en otra edición, no en la que cita la fase 1.
