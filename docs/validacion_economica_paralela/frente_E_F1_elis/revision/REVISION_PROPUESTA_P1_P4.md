# Revisión económica dirigida a P1–P4 · propuesta de decisiones F1 · Elis

Fecha: 16-nov-2026. Material revisado: commit congelado `13f864f910bf0bb3e27007b23c13a8e957f1bfb7` de la rama `auditoria/economica-f1-frente-e`, carpeta `docs/validacion_economica_paralela/frente_E_F1_elis/`. Es la respuesta del autor a la revisión externa de su propuesta de decisiones, que está en la rama `auditoria/revision-propuesta-f1`, commit `1a071881c65a191056ca3c6b41a20a965825cf12`, y que he leído con `git show`, sin fusionarla. La propuesta anterior es la del commit `b83803c`.

Se publica en la rama `auditoria/economica-f1-frente-e-revision`, sobre el commit a3a1a2b.

Marcas: **[P]** publicado (leído en el PDF) · **[D]** derivado · **[I]** inferido · **[H]** hipótesis · **[Pol]** política.

Este documento no contiene valoraciones, precios, recomendaciones de inversión ni declaraciones de aptitud. No adopta ni registra ninguna decisión y no aprueba ni rechaza la propuesta en nombre de nadie. No modifica el material del autor, el producto, los libros ni los datos. Se conservan C48 = 108, C49 = 128,1, el FCF base 307,933 y E1/D3/E2/E6. No se ha enviado ninguna comunicación a terceros. Es una sola pasada.

---

## 0. Resultado en breve

| | Veredicto | Por qué |
|---|---|---|
| **P1** · inversión de transición | **Resuelto en parte** | La caja ya no puede desaparecer: se clasifica por finalidad, no se supone cero y sin importe u horizonte queda pendiente y bloquea. Pero con la clasificación «término explícito» y crecimiento la especificación la cobra dos veces, porque el ancla de S2C la lleva en su denominador (V2). Los cinco casos sintéticos de P1 son a crecimiento cero y no lo ven |
| **P2** · reposición y compras | **Resuelto en parte** | La tabla de correspondencia, el perímetro de R, la guarda V-F1c y el significado de «PPA constante» son correctos. La hipótesis (4b) está bien rotulada como hipótesis, pero su fundamento describe mal lo publicado: el «crecimiento orgánico» de Elis no excluye las compras pequeñas (V1, material). Las compras cobradas como término explícito tienen el mismo hueco del ancla (V2) |
| **P3** · normalización | **Resuelto** | El cálculo conjunto se reproduce con otra implementación (108 valores en los 12 escenarios). La regla fiscal de N1 es la publicada y, en un escenario sintético con impuestos, es la que da la caja. El 27,936 y el «≈ 18,6» están bien explicados. Dejar N2 pendiente está justificado. Quedan dos precisiones menores (V3 y V4) |
| **P4** · coherencia | **Resuelto en parte** | La severidad es la misma en el texto de aprobación y en E5; el 0,5 % no se adopta; el significado del ROIC y la condición son correctos con el tiempo del motor; la media de arrendamientos queda como referencia de ensayo con 16,778. Quedan: dos frases de E2 y E4 que contradicen a E5 (V10), un control del terminal que no se concilia con el que el libro ya tiene (V6), E3 frente a los términos explícitos (V7) y una sensibilidad de arrendamientos que es solo la de los pagos (V5) |

1. **Todo lo que declara el autor se reproduce** (§2). Manifiesto 356 de 356. `controles_sinteticos_f1.py`, `copia_investigacion_f1.py` y `contraste_f1.py` dan salidas idénticas byte a byte a las guardadas, con el libro `d2593777…92385` de la base 4.14 materializada (6.798 de 6.798).
2. **N1, recalculado por mi cuenta desde el CSV** (§5.1): −11,605 en el flujo sin crecimiento y −18,609 en el flujo del año 11 del escenario NORMAL; con el tipo fijo, −9,765 y −14,598. Coinciden los valores de T16. Mi script no importa código del autor y contrasta 89 celdas del libro.
3. **Hallazgo material (V1).** La propuesta apoya (4b) en que el crecimiento orgánico se mide «neto de los clientes perdidos» y concluye que «las bajas se repusieron sin compras». La definición publicada dice otra cosa: el crecimiento orgánico solo excluye el efecto de las adquisiciones «importantes» (más de 5,0 millones de ingresos anuales en Francia y de 3,0 en los demás países) [P: URD 2025, p. PDF 313; DEU 2024, p. 259; URD 2023, p. 267]. Las demás compras cuentan dentro del crecimiento orgánico. En 2023–25 su flujo neto fue 35,3 / 22,0 / 37,3, una media de 31,5, el 10,2 % del FCF base [P][D]. Lo publicado permite decir «sin compras importantes», no «sin compras». No demuestra que esas compras repongan clientes; quita parte del apoyo a la inferencia y da un importe publicado a la sensibilidad.
4. **Dos cosas que la respuesta da por no publicadas sí lo están (V3).**
   - La caja del earnout: la nota 2.4 separa «Earnouts and deferred consideration» dentro de la línea de adquisiciones del estado de flujos: 34,4 / 93,9 / 23,3, de los que 31,4 / 83,2 / 19,7 son de Lavartex, la compra de México de 2022 [P: DEU 2024 p. 288; URD 2025 p. 342 y p. 341]. La ubicación que el autor infiere [I] es correcta y es [P].
   - La actualización del earnout de 2025: 0,7 [P: URD 2025 p. 313]. Con 12,4 / 5,6 / 0,7, la línea fiscal publicada cuadra los tres años al tipo del 25,83 %: −15,834 / +0,801 / −0,232, frente a (15,8) / 0,8 / (0,2) [D].
5. **Un doble cargo que los controles no ven (V2).** Con la fórmula del ancla de E4, lo que se cobra como término explícito y no está en D_X sigue en el denominador del ancla. Con crecimiento del 5 %, el caso coherente P1b del autor pasa a cobrar de más 7 en el año 1 y 11,4 en el año 11; P2d, 9 y 14,7. Lo reproduzco con mi motor y con las funciones del propio autor (§8).
6. **Terminal (V6).** La condición ROIC = (1+g∞)·m_obj·(1−τ)·S2C es exacta con el tiempo del motor. Pero el libro ya tiene esa comprobación con otra fórmula, sin el factor (1+g∞), y con un umbral de aviso configurable: Convenciones V6.3 §3 y `Diagnóstico V6`, filas 176–179. La propuesta no la nombra.
7. **Las nueve decisiones** (§7). Ninguna pide elegir una cifra, con una salvedad: (4b) fija en cero las compras de reposición mientras falta el dato M6, y lo hace como hipótesis declarada, con la alternativa de bloquear. Ninguna se recomienda por su efecto en el valor.
8. **Objeciones: V1 (material), V2–V9 (menores) y V10–V11 (forma).** Ninguna cambia una cifra de la propuesta. V1 cambia el fundamento con que se pide aprobar (4b). Ninguna desbloquea ni bloquea por sí sola la valoración de Elis, que sigue en `pendiente_de_datos` por R.
9. **Lo que bloquea y no es un defecto** (§10): M1, M2, M6 con la finalidad de las compras pequeñas, N2, el perímetro de las palancas de Elis y las cuestiones de política de §10.

**Gravedad.** *Material*: cambia el fundamento o una cifra de la que depende el texto que se pide aprobar; conviene corregirla antes de decidir. *Menor*: hueco o imprecisión que no cambia el sentido de ninguna decisión; hay que corregirla antes de implementar. *Forma*: redacción, rótulos y referencias.

---

## 1. Encargo, configuración y límites de la independencia

**Encargo.** Mensaje recibido al crearse esta sesión, entregado como aviso automático y no tecleado por una persona en ella. Lo creó la sesión autora, que lo registra en su `revision/ESTADO.md` y en su `REGISTRO_CONFIGURACION.md` (commit `d5188bb`, posterior al congelado y que no reviso). Lo trato como un encargo de revisión: no doy por cierta ninguna descripción del autor sin comprobarla.

**Configuración.** Aquí no se escriben identificadores de modelo. Quien encarga puede leer la configuración de esta sesión en sus metadatos.

**Límites de la independencia:**
- Quien encarga fija el alcance y las preguntas.
- He leído la revisión externa y la respuesta del autor antes de calcular. Mis sondas parten de sus casos.
- Mi recálculo no importa código del autor y usa otra aritmética de redondeo, pero parte del mismo CSV de cifras verificadas. No he vuelto a verificar esas cifras contra los PDF: el verificador está fuera del alcance.
- Las cifras que he leído yo en los PDF llevan el rótulo [LECTURA] en mis salidas. Compruebo que su literal está en la página con dos extractores (`pdftotext` y `pypdf`) y he leído la cabecera de cada tabla para la columna y el ejercicio. No han pasado por el verificador del autor.
- Esta sesión es distinta de la autora y de las revisiones anteriores, pero es un agente de la misma clase y recibe el encargo por el mismo cauce. Un sesgo de lectura común a esa clase no se descarta.

---

## 2. Reproducción

Base 4.14 materializada desde el ZIP original de la Release `base-4.14` (1.130.912.246 bytes, SHA-256 `bb51942c…b93e`) con `tools/base_414.py`, en un worktree de `main` separado: 6.798 de 6.798, `complete: true`, ningún archivo versionado modificado (`resultados_revisor_p1_p4/materializacion_base_414.txt`). El material del autor, en un worktree del commit congelado. Python 3.13.18, `pdftotext` 24.02.0, openpyxl 3.1.5, pypdf 6.17.0. No he ejecutado LibreOffice.

Comando único: `scripts_revisor_p1_p4/reproducir.sh <frente del autor> <munger_v2_r1 materializado> <salida>` → `resultados_revisor_p1_p4/reproduccion.txt`.

| Cifra declarada | Resultado |
|---|---|
| Manifiesto: 356 archivos | 356 de 356 con `sha256sum -c` |
| Libro de Elis | SHA-256 `d2593777650f1d9d77bcc7b9eaa6f4c0c12a742fa4706bd20b35808f99c92385` |
| `controles_sinteticos_f1.py`: 22 casos, 8 coherentes y 14 incoherencias ilustradas; reproduce los 9 del revisor externo | Código 0. JSON y registro idénticos byte a byte |
| `copia_investigacion_f1.py`: 43 controles, ninguno fallido | Código 0. JSON e informe idénticos byte a byte |
| `contraste_f1.py`: 292 comprobaciones, 0 fallidas | Código 0. JSON e informe idénticos byte a byte; SHA-256 del JSON `147f4f49…3024`, el que registra la revisión externa |
| Las cinco fuentes PDF | Huellas iguales a las de `datos/fuentes.json` (`evidencia_pdf.txt`) |

---

## 3. P1 · Inversión de transición (clima)

**Qué pedía la revisión externa.** Que una categoría separada no dejara su caja fuera del modelo; correspondencia en la ventana, en los años proyectados y en el terminal, una sola vez; pendiente si no hay importe.

**Lo que resuelve la respuesta.**
- La decisión (5b) clasifica por finalidad documentada y ya no dice «fuera de R y del crecimiento».
- En la ventana, el gasto del plan está dentro del capex y, con él, del FCF base [P: «capex contained despite new workwear contracts and expenditure under the Climate plan», URD 2025 p. 122; comprobado].
- Sin importe u horizonte no se supone cero: E1 deja la fila vacía («desconocido, no cero») y V-F1i bloquea. Para Elis queda pendiente dentro de M1. **Esta parte de la pregunta está resuelta.**

**¿Se cobra una sola vez cada clasificación?** No en las tres. Motor y caja calculados por separado (`sondas_caja.py`, bloque S1; ventana con crecimiento, para que el ancla salga de sus datos):

| Clasificación (E2) | Ventana | Años 1–10 | Año 11 | Resultado |
|---|---|---|---|---|
| `en_R` (sostenimiento permanente) | Capex y FCF base | En la calibración de f, en proporción a las ventas | Igual | Una vez. El ancla de E4 la excluye sola, porque está en D_X (S1d y S1e: ancla 1). Matiz: f la hace crecer con las ventas; si el importe es fijo en euros, con crecimiento del 5 % cobra de más 0,35 en el año 1 y 5,0 en el año 11 (S1d) |
| `crecimiento` (amplía capacidad) | Capex y FCF base | ΔV/S2C, con el ancla | g∞/ROIC | Una vez, si de verdad crece con las ventas nuevas (S1f). Si no, desaparece a crecimiento cero: caso P1e del autor |
| `termino_explicito` (importe y horizonte) | Capex y FCF base | El término **y además ΔV/S2C** | El ancla la sigue cobrando cuando el plan ya ha terminado | **Dos veces con crecimiento** (S1a). A crecimiento cero, coherente (S1c) |

- **Por qué.** E4 define el ancla como ΔV ÷ Σ(capex − D_X + circulante + adquisiciones). Con `termino_explicito`, la transición no está en D_X y sí en el capex de la ventana: queda en el denominador como si fuera inversión de crecimiento. E4 solo saca del ancla las compras de reposición, porque «ya están en R».
- **Cuánto, en el ejemplo.** Ventana con ventas 100, ΔV 5 y capex 32 = 20 + 5 + 7. Ancla de E4: 5 ÷ 12. Con crecimiento del 5 %, motor − caja = −7 en el año 1, −8,5 en el año 5, −8,9 en el año 6 y −11,4 en el año 11. El plan era de cinco años: por el ancla se vuelve perpetuo, que es lo que el caso P1a del autor llama incoherencia cuando ocurre por R.
- **Con las funciones del autor** (`contraprueba_con_funciones_del_autor.py`): su caso P1b, coherente con S2C = 1, da las mismas diferencias con S2C = 5/12.
- **Por qué no lo vieron los controles.** Los cinco casos de P1 son a crecimiento cero y el ancla se escribe a mano. V-F1i nombra «en R y como término», no «como término y en el ancla».
- Objeción V2.

**¿Pendiente sin importe u horizonte, sin cero ni perpetuidad por el nombre?** Sí. Dos precisiones de forma (V10): V-F1i dice «transición material conocida» sin que haya importe con que medir si es material, y en Elis el plan se conoce y el importe no; y la tabla de correspondencia pone «solo si es permanente» en el terminal, que no describe la clasificación de crecimiento.

**Veredicto: resuelto en parte.** La omisión que señalaba la revisión externa está cerrada. Falta cerrar el doble cargo de una de las tres clasificaciones.

---

## 4. P2 · Reposición y compras

### 4.1 Tabla de correspondencia

He seguido cada fila con la mecánica del motor. En la ventana, NOPAT − f·ventas = FCF base + (capex − D_X) + circulante: el flujo sin crecimiento cobra D_X en lugar del capex, y el motor lo lleva al año base y a los siguientes en proporción a las ventas. Los años 1–10 añaden ΔV/S2C y el año 11, g∞/ROIC.

- **No encuentro ningún euro omitido en las filas de la tabla.** Arrendamientos, gasto comercial, capex propio necesario, compras de crecimiento, PPA y partidas recurrentes de la nota 4.6 están en un solo sitio.
- **Dos dobles cargos posibles que la especificación no cierra**, los dos con crecimiento y por el ancla: la transición con término explícito (§3) y las compras de reposición con término explícito (S2a: −9 en el año 1 y −14,7 en el año 11). Dentro de R no ocurre: con D_X = 29, la fórmula de E4 da 5 ÷ (25 − 29 + 9) = 1 (S2c). El caso P2d del autor es coherente porque escribe el ancla a mano «sin ellas»; E4 y V-F1j solo hablan de «en R y también en el ancla». V2.
- **La tabla no es toda la composición de f.** Impuestos e intereses están fuera de F1 (E8), y las cesiones y subvenciones (−10,0), las provisiones (−2,0) y el SBC están en el informe, §4.2. Las decisiones no los tocan. Conviene que la frase «ningún euro se omite» diga «de los costes que tocan estas decisiones» (V10).
- **Matiz, sin objeción.** Los gastos de transacción de las compras (1,5 / 5,2 / 2,4 [P: DEU 2024 p. 296; URD 2025 p. 350]) son caja, están en el EBIT y quedan en el margen como partida recurrente. Bajo (4b) son un coste de crecimiento que a crecimiento cero se seguiría cobrando. Es pequeño y de sentido prudente.

### 4.2 Perímetro de R y guarda V-F1c

- **Correctos.** Con D_X = R_propia + R_compras, f cobra las compras de reposición aunque estén fuera del capex y del FCF base, y el ancla de E4 las excluye (S2c). Comparar cada parte con su caja es lo coherente: R total puede superar el capex propio sin infrainversión.
- **Límite.** R_compras solo cabe en D_X con el perímetro `A3_estimado`. Con `A1_sin_ROU` o `A2_propio`, las compras de reposición tienen que ir como término explícito, que es el camino con el hueco de V2.
- **La cota de (3a) no es de R total (V8).** El capex propio, 867,2, acota R_propia más la transición. R, tal como la redefine el §3, incluye R_compras, que está fuera del capex. El intervalo 736,0–867,2 mide la materialidad solo bajo (4b). La media de las adquisiciones es 127,7 y la de capex más adquisiciones, 994,8 [D]. La propuesta dice que el intervalo «solo mide la materialidad», así que no cambia ninguna decisión, pero lo que está en juego si (4b) no se aprueba es más de 138.

### 4.3 La hipótesis (4b)

**Rótulo.** Bien: «hipótesis, no dato», con [P] para lo publicado y [H] para el futuro, y con la alternativa de exigir M6 y bloquear.

**Fundamento.** Tiene tres partes y una no se sostiene como está escrita.

| Afirmación de la propuesta | Lo que he comprobado |
|---|---|
| [P] Crecimiento orgánico positivo en 2021–25: 7,4 / 21,0 / 11,8 / 5,2 / 3,8 %; externo del 1,2 al 3,1 % en 2022–25 | Cierto [P: CSV]. El externo: 3,1 / 1,8 / 1,2 / 1,8 % |
| [P] Efecto volumen publicado en 2024 y 2025, sin cifra; en 2023, unos 9 puntos de precio | Cierto [P: URD 2025 p. 122; DEU 2024 p. 121; URD 2023 p. 261] |
| [I] «El crecimiento orgánico se mide sobre la cartera existente, neta de los clientes perdidos […]. Las bajas se repusieron sin compras» | **No es lo que dice la definición publicada.** V1 |

- **La definición [P].** «Organic growth […] is calculated excluding (i) the impacts of changes in the scope of consolidation of "major acquisitions" and "major disposals" in each of the periods under comparison, as well as (ii) the impact of exchange rate fluctuations. "Major acquisitions" […] are acquisitions […] of companies that generate, at the time of acquisition, annual revenue of more than €5.0 million in France and €3.0 million in other countries» (URD 2025, p. PDF 313). La misma definición, sin los umbrales, en DEU 2024 p. 259 («acquisitions importantes»), URD 2023 p. 267, URD 2022 p. 249 y URD 2021 p. 217. La p. 259 del DEU 2024 es una página que la respuesta cita para otra cifra.
- **Consecuencia [D].** El efecto de las compras que no son «importantes» no se excluye: está dentro del crecimiento orgánico publicado. El crecimiento externo publicado es solo el de las importantes.

**Cuánto pesan esas compras [P][D]** (`recalculo_independiente.txt`, sección I; `evidencia_pdf.txt`):

| | 2023 | 2024 | 2025 | Media |
|---|---|---|---|---|
| Adquisiciones netas del estado de flujos | 82,1 | 183,3 | 117,6 | 127,7 |
| · de ellas, earnouts y pagos aplazados | 34,4 | 93,9 | 23,3 | 50,5 |
| · · de ellos, Lavartex (México, comprada en 2022) | 31,4 | 83,2 | 19,7 | 44,8 |
| · flujo neto de las «otras adquisiciones» | 35,3 | 22,0 | 37,3 | **31,5** |
| Ingresos anuales de las «otras adquisiciones» del año | no sumados | 9,1 (9 compras) | 19,8 (16 compras) | |

Fuentes: DEU 2024 p. 288; URD 2025 p. 342, p. 341 y p. 339.

- 31,5 es el 10,2 % del FCF base; 127,7, el 41,5 %.
- 19,8 es el 0,43 % de las ventas de 2024 y 9,1, el 0,21 % de las de 2023. Son ingresos anuales; cuánto aportaron dentro de cada año al crecimiento orgánico no se publica.

**Qué significa y qué no.**
- El crecimiento orgánico nominal sigue siendo claramente positivo aunque se le quiten unas décimas: en eso el fundamento se mantiene.
- Lo que deja de estar acreditado es el paso siguiente. El efecto volumen de 2024–25 no tiene cifra, y la parte que procede de compras pequeñas tampoco. Lo publicado permite decir que las ventas se sostuvieron **sin compras importantes**. No permite decir que las bajas se repusieron **sin compras**.
- Tampoco demuestra lo contrario. Muchas de esas compras son de control de plagas y de salas limpias, que la empresa presenta como desarrollo: «These bolt-on acquisitions help to consolidate the Group's position in these various countries and/or to pursue the development of its pest control services» [P: URD 2025 p. 339]. «Consolidar la posición» puede ser ampliar o reponer.
- La condición de aplicación «se revisa si el crecimiento orgánico en volumen deja de ser positivo» no se puede observar con lo publicado: no hay cifra de volumen y la orgánica incluye esas compras.

**Sensibilidad.** «Cada millón anual de compras que fuera de reposición baja el flujo sostenible en un millón» es correcto, también en el año 11 (S2d). Pero es una pendiente sin importes. Los hay publicados: 31,5 de media para las compras que por definición están dentro del crecimiento orgánico, y 127,7 para todas, una referencia extrema contra la que sí hay evidencia. De los 383,0 de la ventana, 134,3 son pagos aplazados de una compra de 2022. Darlos no es elegir una cifra para R_compras: es decir cuánto hay en juego.

### 4.4 «PPA constante» y el 4,206

- **El significado es correcto.** f es una proporción de las ventas por construcción. Una partida que no es caja solo se anula en el flujo si el margen la lleva en la misma proporción que f devuelve. Recalculado: PPA media ÷ ventas medias, 1,8743 %; PPA de 2025 ÷ ventas de 2025, 1,7866 %; f devuelve 89,906 y m0 lleva 85,7; diferencia, **4,206** [D]. Está bien rotulado como convención [H].
- **Falta el sentido.** f devuelve más de lo que m0 lleva: el 4,206 **sube** el flujo sin crecimiento de A2. La propuesta se compromete a decir el sentido donde una opción mueve el valor.
- **Falta la otra mitad (V5).** La misma condición vale para la amortización ROU, que f también devuelve en A1 y A2: f devuelve 139,382 (2,9057 % de las ventas) y m0 lleva 149,5 (3,1167 %). Son **10,118** que **bajan** el flujo. El informe lo dice en §5.5; la propuesta y `perimetro_margen` de E2 solo hablan de la PPA. Los dos efectos de escala juntos, en A2: −5,913.

**Veredicto: resuelto en parte.** La correspondencia está hecha y es correcta en sus filas. El fundamento de (4b) hay que corregirlo antes de pedir que se apruebe «con su fundamento».

---

## 5. P3 · Normalización

### 5.1 Cálculo conjunto: recálculo propio

`recalculo_independiente.py` lee el CSV con el módulo estándar, reconstruye las partidas con mis identificadores, calcula el tipo de la fila 10 con dos modos de redondeo (deben coincidir), calibra f y reimplementa el motor A desde `Convenciones_financieras_V6_3.md`. No importa código del autor.

- **Base:** FCF base 307,933; C48 = 108; f de A0 = 0,041681455274; F₀ = 248,496395343; A1 y A2 como en T2 y T3. **89 comparaciones con celdas del libro coinciden:** Historia de 2021–25 (ventas, EBIT, D&A, tipo, capex, adquisiciones y circulante), C52, C53, C58, C70, C75, C76, las 15 palancas y los 33 flujos del Motor.
- **Escenarios:** los 12 de la copia de investigación. **108 valores coinciden** con `copia_investigacion_f1.json`: tipos de 2023–25, τ de 5 años, f, variación del flujo sin crecimiento y del año 11 en los tres escenarios. En todos, la variación es idéntica en A0, A1 y A2.

| N1 · ajustes de earnout 2023–25 | τ 2023 / 2024 / 2025 | τ de 5 años | m0 | f (A0) | Flujo sin crecimiento | Variación (f / m0 / τ) | Año 11 MALO / NORMAL / BUENO |
|---|---|---|---|---|---|---|---|
| Sin ajustes | 0,2963 / 0,2754 / 0,2560 | 0,28820 | 0,131338 | 0,041681455 | 248,496 | — | — |
| No deducibles (regla propuesta) | 0,2619 / 0,2806 / 0,2559 | 0,28234 | 0,131379 | 0,044900433 | 236,891 | **−11,605** (−15,441 / +0,144 / +3,692) | −15,433 / **−18,609** / −19,976 |
| Tipo fijo | sin cambios | 0,28820 | 0,131379 | 0,043746946 | 238,731 | −9,765 (−9,908 / +0,142 / 0) | −11,843 / −14,598 / −15,914 |

**El cálculo conjunto es correcto.** Una precisión de forma: lo que la propuesta llama «terminal NORMAL −18,609» es la variación del flujo del año 11, no la de un valor terminal (V10).

### 5.2 Regla fiscal de N1

- **Es la publicada [P].** La conciliación del impuesto tiene una línea propia: «Ajustements et désactualisation de compléments de prix non déductibles», 0,8 en 2024 y (15,8) en 2023 (DEU 2024 p. 337); «Adjustments and accretion of non-deductible earnouts», (0,2) en 2025 y 0,8 en 2024 (URD 2025 p. 392). Comprobadas en el PDF.
- **Cuadra los tres años [D].** −25,83 % × (ajuste + actualización): 2023, −25,83 % × (48,9 + 12,4) = −15,834; 2024, −25,83 % × (−8,7 + 5,6) = +0,801; 2025, −25,83 % × (0,2 + 0,7) = −0,232. Publicado: (15,8), 0,8 y (0,2). La respuesta lo deriva para 2023; con el 0,7 de 2025, que sí está publicado (§5.5), cuadran los tres.

**Es la regla que da la caja.** Escenario sintético con impuestos y con la caja conocida (`sondas_caja.py`, S3): un cargo de 9, no monetario y no deducible, en un año de la ventana; flujo sostenible, 52,5.

| Tipo de proyección | Sin normalizar | N1, no deducible | N1, tipo fijo | Deducir la partida entera |
|---|---|---|---|---|
| Media de la ventana | 54,639 | **52,5** | **52,5** | 45,639 |
| Media de cinco años, con los dos anteriores al tipo legal | 55,033 | **52,5** | 52,893 | 46,033 |
| Media de cinco años, con los dos anteriores al 31 % | 53,113 | 50,58 | 50,973 | 44,113 |

- Con tipos homogéneos, «no deducible» da exactamente la caja y «tipo fijo» no.
- Deducir la partida entera, que es lo que haría restar un diagnóstico como el 27,936, falla siempre.
- La tercera fila no es un defecto de N1: es la convención del τ de cinco años (E8.1), que desvía también la base sin normalizar.

**En Elis, parte del −11,605 es esa convención (V4).** El tipo de cada año de la ventana pesa un tercio en la calibración de f y un quinto en el τ de proyección. Si el τ de proyección fuera el de la ventana, N1 daría −9,141 con la regla publicada y −9,763 con el tipo fijo: la diferencia entre las dos reglas cambia de −1,840 a +0,622 (`recalculo_independiente.txt`, sección C). El efecto antes de impuestos es −13,966. Lo firme es que N1 baja el flujo sin crecimiento entre 9 y 12. El autor da las dos cifras y señala E8.1 como cuestión aparte; lo que falta es decir que los valores de T16 dependen de ella.

### 5.3 El 27,936 y el «≈ 18,6»

- **27,936 reproducido:** 13,675 − 4,032 + 18,293. Las tres razones de la respuesta son exactas:
  - toma las líneas del estado de flujos. Línea del estado de flujos menos línea de la nota 4.6, en las bajas: 3,1 / 5,8 / 2,6. En el earnout hay además otros no monetarios: −0,5 / −0,6 / −0,3;
  - quita la partida de f antes de impuestos: los ajustes de earnout de los tres años, después de impuestos y con el tipo fijo, mueven f en 9,908, no en 13,675;
  - lleva la plusvalía de 2025 a m0 y no la quita del NOPAT de 2025 que calibra f: al quitarla, f baja y el flujo sube 6,705.
- **«≈ 18,6» reproducido:** es la parte de f del ajuste de 2023 con el tipo recalculado, −18,648. El mismo ajuste baja el τ de cinco años, +4,334. Conjunto, −14,314. No se puede sumar al resto.
- **La explicación es correcta.**

### 5.4 N2

**Dejarla pendiente está justificado.**
- Que la plusvalía de 25,7 sea la de las indemnizaciones es una inferencia razonable: la mejora de otros ingresos operativos se explica por «a high level of insurance benefits in 2025» [P: URD 2025 p. 309] y es la única línea positiva grande de la nota. El autor la rotula [I].
- La caja no está identificada: cobros por bajas 15,3 frente a una plusvalía de 23,1 en el estado de flujos [P].
- Su fiscalidad no se publica. Las tres hipótesis dan de −10,305 a −11,598 en el flujo sin crecimiento y de +9,861 a +12,288 en el año 11 de NORMAL, reproducido.
- Una normalización simétrica tocaría el FCF base registrado (E6), y eso no corresponde a este encargo.

### 5.5 Dónde está la caja del earnout y el límite declarado de N1 (V3)

- **La caja está publicada.** La respuesta dice que el pago está fuera del FCF base por inferencia y que «la línea del pago no se ha identificado en las páginas examinadas». La nota 2.4 la da (§4.3, tabla): los earnouts y pagos aplazados son parte de «Acquisition of subsidiaries, net of cash acquired», en inversión. El de México se liquidó en 2024 y 2025: «settlement of the second installment and the balance of the Mexican earnout in 2024 and 2025» [P: URD 2025 p. 352].
  - La inferencia del autor es correcta y pasa a [P].
  - Importa porque el control V-F1l del propio autor exige la ubicación de la caja de cada ajuste. Con esto N1 la tiene.
  - Es coherente con «el coste de las compras se cobra como compras»: esos pagos están en el denominador del ancla con adquisiciones.
  - El motivo del ajuste también está publicado: la revaluación se debe a que las perspectivas de la sociedad comprada se revisaron al alza dos veces en 2023 [P: URD 2023 p. 302].
- **La actualización de 2025 está publicada.** La respuesta dice que «la de 2025 no se publica por separado». Es 0,7 [P: URD 2025 p. 313, tabla del resultado neto corriente]. Las de 2023 y 2024, 12,4 y 5,6 [P: DEU 2024 p. 259].
- **Tamaño del límite [LECTURA].** Si la regla fiscal de N1 alcanzara también a la actualización (fuera del BAI que da el tipo; el EBIT, como en N1): tipos 0,2544 / 0,2772 / 0,2556, τ de cinco años 0,28010; flujo sin crecimiento −12,396 y año 11 de NORMAL −20,270. Frente a N1: **−0,790 y −1,661**. Es pequeño. No propongo adoptarlo: las tres cifras no están en el CSV verificado.
- **2021 y 2022 (V4).** La regla dice «en la ventana de calibración», pero el τ de cinco años también promedia 2021 y 2022, que tuvieron ajustes de earnout: (3,0) y 2,4 (2,1 antes de la reexpresión) [P: URD 2022 p. 285; URD 2023 p. 302], con línea fiscal propia en 2022 (0,5; URD 2023 p. 345). Si se trataran igual, +0,416 en el flujo sin crecimiento y +0,466 en el año 11. Pequeño, pero el texto de la regla no dice qué se hace con esos dos años.

**Veredicto: resuelto.** La regla, la fiscalidad y el cálculo conjunto son correctos. Las precisiones de §5.5 refuerzan N1: no la cambian.

---

## 6. P4 · Coherencia

**Severidad.** La tabla de la propuesta y la columna de E5 coinciden control a control, de V-F1a a V-F1l: los mismos en BLOQUEA, V-F1c con justificación en AVISO, V-F1f y la comparación de V-F1k en INFORMA. El texto de (1a) remite a esa severidad. Quedan dos frases de la especificación que contradicen a E5 (V10):
- E4: «Si no coincide con `perimetro_reinversion`, se emite el **aviso** V-F1g». E5: V-F1g BLOQUEA (las negritas de estas dos citas son mías);
- E2, matriz, fila `A0_total`: «V-F1a si hay arrendamientos **materiales**». E5: BLOQUEA «con cualquier importe».

**Umbral del 0,5 %.** No se adopta: solo aparece para decir que no se adopta. V-F1a bloquea con cualquier importe. Es una elección prudente, y aprobar (1a) la aprueba, porque su texto remite a E5.

**Terminal.**
- **El significado del ROIC es correcto:** rendimiento de la inversión nueva, sobre el NOPAT del perímetro del margen y sobre el capital de crecimiento del perímetro del ancla; sin la ROU, porque el arrendamiento se paga en f, y sin la reposición, porque está en la calibración de f.
- **La condición es exacta con el tiempo del motor.** El motor cobra en el año t la inversión del aumento de ventas de ese mismo año. Igualando NOPAT₁₁·g∞/ROIC con (V₁₁ − V₁₀)/S2C sale ROIC = (1+g∞)·m_obj·(1−τ)·S2C. Comprobado en los tres escenarios (igualdad exacta) y en S4.
- **Las cifras de Elis, reproducidas:** 7,5486 / 10,8905 / 14,7743 %; diferencia de inversión del año 11, +4,450 / +10,284 / +28,964.
- **Pero el libro ya tiene esta comprobación, con otra fórmula (V6).** Convenciones V6.3 §3: «En el año 11 la rentabilidad del capital pasa de S2C·m_obj·(1−τ) a ROIC; el salto se muestra en Diagnóstico V6, bloque 10, y avisa si supera C179 (5 puntos)». En el libro de Elis, filas 176–179: 7,4739 / 10,6770 / 14,4140 % frente a 7 / 10 / 12 %; salto de 0,47 / 0,68 / 2,41 puntos; umbral del aviso, 5 puntos, «ajustable». Con la fórmula de la propuesta el salto es 0,55 / 0,89 / 2,77. La diferencia es el factor (1+g∞): con la fórmula del libro la inversión del año 11 es (1+g∞) veces ΔV/S2C. La propuesta presenta V-F1k como nuevo y no dice cuál de las dos fórmulas rige ni qué pasa con el umbral que ya existe.
- **«Debe justificarse» frente a INFORMA (V6).** Propuesta, §4: la diferencia «se informa (V-F1k) y debe justificarse». E4: «la palanca lo justifica». E5: INFORMA, sin consecuencia si no se justifica. Importa sobre todo en el sentido contrario al de Elis: un ROIC mayor que el que reproduce S2C cobra en el terminal menos inversión que los años 1–10.

**Arrendamientos (1b).**
- La media queda como referencia de ensayo y convención, no como peso futuro. Sensibilidad reproducida: 3,3589 % frente a 3,7087 %; 161,121763 frente a 177,9; **16,778237**. La precisión del autor sobre el redondeo del texto de la revisión externa es exacta.
- **Es la sensibilidad de los pagos solos (V5).** Vale entera en A0. En A1 y A2, que es lo que (1a) propone, f devuelve además la amortización ROU al peso medio: con el peso de 2025 en las dos cosas, −16,778 + 10,118 = **−6,660**. Ejemplo sintético: S5. No hace falta elegir otro punto: basta que el texto diga que 16,8 es la parte de los pagos.

**E3 frente a los términos explícitos (V7).** E3 dice «sin cambios en la estructura del flujo ni del terminal». Pero `tratamiento_transicion = termino_explicito` y `reposicion_con_importe` como término explícito añaden un término al flujo, y la especificación no da su fórmula en los años 1–10 ni en el año 11: solo está en el script sintético. E2 rechaza `EBIT_NIIF16_PPA_decreciente` precisamente porque exigiría «un término aparte».

**Veredicto: resuelto en parte.** Lo sustancial está hecho. No puede decirse «sincronizado» mientras E2 y E4 contradigan a E5 y el control del terminal duplique, con otra fórmula, uno que el libro ya tiene.

---

## 7. Las nueve decisiones

| ID | ¿Pide elegir una cifra donde falta evidencia? | ¿Se recomienda por su efecto en el valor? | Marcas | Texto que se pide aprobar |
|---|---|---|---|---|
| 1a | No | No. Dice el sentido (+139,4 frente a A0, reproducido) y el motivo es el doble cómputo | Bien | Claro. Lleva dentro (4a) y la severidad de todos los controles (V11) |
| 1b | No. La media es convención de ensayo y lo dice | No | Bien | Claro. «16,8» es solo la parte de los pagos (V5) |
| 2 | No. El inciso (v) es una convención para anular una partida que no es caja | No. Dice que da más flujo que A1 | «Reposición orgánica en la ventana [P][I]»: le alcanza V1 | Claro. El inciso (v) solo habla de la PPA (V5) |
| 3a | No. R sigue pendiente | No da cifra | «Reparto no publicado [P]» rotula como publicada una ausencia (V10) | Claro. El intervalo es de R_propia y transición (V8) |
| 3b | No. Admite una «estimación documentada»: con las exigencias de V-F1d no es elegir una cifra, pero es la vía por la que podría entrar una | — | Bien | No es un texto que se pueda aprobar: «Decido si…» no dice qué se aprueba (V11) |
| 4a | No | No. Dice que hoy el ROIC cobra más inversión que su S2C | Bien | Claro |
| 4b | **Es la única que fija una magnitud donde falta el dato: compras de reposición igual a cero, sin M6.** Lo hace como hipótesis declarada, con evidencia parcial y con la alternativa de bloquear | No se apoya en él. Dice que es la opción más favorable | [P] y [H], bien. El [I] no se sostiene como está escrito (V1) | Claro como hipótesis. Pide aprobarla «con su fundamento» y «su sensibilidad»: el fundamento hay que corregirlo y la sensibilidad no tiene importes (V1) |
| 5a | No | No. Baja el flujo | «Caja del earnout fuera del FCF base [I]» es [P] (V3) | Claro. No dice qué pasa con 2021–22 en el τ de cinco años (V4) |
| 5b | No | No da cifra | Bien | Claro. La especificación no garantiza «una sola vez» con término explícito y crecimiento (V2) |

- **Resultado del conjunto.** Es cierto que ninguna recomendación desbloquea una valoración: sin R no hay f, ni flujo de partida, ni ancla.
- **Dependencias.** Las nueve decisiones no son independientes. (2) y (5a) declaran que dependen de (4b). (1a) no declara que su política del §1 contiene la regla de (4a) ni que aprueba la severidad de los controles de (4b), (5a) y (5b). Aprobar (1a) y aplazar (4a) no es posible con el texto actual (V11).

---

## 8. Controles sintéticos

**¿Modelan la caja del escenario de forma independiente del motor?**
- **En el código, sí.** `Escenario.caja()` suma EBITDA, mantenimiento, pagos de arrendamiento, compras de reposición, transición e inversión de crecimiento. No usa f, ni el margen, ni la palanca S2C.
- **Comparten supuestos con el motor:** todos los costes crecen en proporción a las ventas, la inversión de crecimiento se paga el año en que crecen las ventas y no hay impuestos. Con esos supuestos el motor es exacto por construcción. Son ejemplos de definición, que es lo que se pedía.
- **El ancla se escribe a mano.** La ventana es estacionaria, sin ΔV, así que ningún caso calcula el ancla con la fórmula de E4. La correspondencia de la ventana al ancla no se prueba; por eso no se vio V2.
- **«Coincide con `motor_a`» vale con crecimiento y margen constantes.** `comprobar_motor` usa tres juegos con g de los años 1–5 igual a g∞ y m0 igual a m_obj. Con g = 5 % y g∞ = 2 %, el motor sintético y `motor_a` difieren en los años 6–10 y en el año 11 (diferencia máxima 9,1): `motor_a` baja el crecimiento y el sintético no. El caso P2h (5 % y g∞ = 0) no recorre la senda de `motor_a`. Para ilustrar definiciones es suficiente; la frase de T15 es más amplia que su prueba (V10).

**Casos que faltan para P1–P4 (V9):**

| Asunto | Estado | Lo que falta |
|---|---|---|
| Correspondencia de caja | Cubierta con el ancla dada | Un caso de extremo a extremo: ventana con crecimiento, ancla calculada con E4 y flujos. Mío: S1 y S2 |
| Crecimiento cero | Cubierto: P1a–e, P2a, P2b y P4c | Nada. Pero **P1 solo se prueba a crecimiento cero**: ningún caso de transición tiene crecimiento |
| Coste ya incluido en el EBIT | Cubierto: P2f y el caso del revisor externo | Nada |
| Compras de reposición | Cubiertas en R y en el ancla (P2a–c) y como término (P2d) | El término explícito con el ancla de E4 (S2a) |
| Terminal | Cubierto: P4a–d | Nada para la condición. Sí la conciliación con la fórmula de Convenciones §3 (S4) |
| Normalización | Sin caso sintético: T16 son valores de la copia de investigación | Un caso con impuestos y caja conocida. Mío: S3 |
| Guarda V-F1c | Un ejemplo en que la guarda nueva no salta | Casos en que debe saltar (T8 los pide a la implementación) |

Mis sondas: `sondas_caja.py`, 10 sondas de flujo y tres bloques de cálculo, cada una con su resultado esperado; `contraprueba_con_funciones_del_autor.py` repite las dos principales con `Escenario`, `motor_sintetico` y `caja_sintetica` del autor. Importes ficticios: no son datos de Elis.

---

## 9. Objeciones

### V1 · material · (4b) y (2) · el «crecimiento orgánico» publicado no excluye las compras pequeñas

- **Dónde.** Propuesta: tabla única, filas 2 y 4b (columna «Naturaleza»), y §2, «Compras de sociedades (4b)», tercer punto. Respuesta: §3, «Fundamento de la hipótesis (4b)». Informe: §6.3, «Evidencia parcial de la ventana».
- **Qué.** Se afirma que el crecimiento orgánico se mide neto de los clientes perdidos y que, al ser positivo, «las bajas se repusieron sin compras». La definición publicada solo excluye las adquisiciones «importantes». Las demás están dentro del crecimiento orgánico.
- **Evidencia.** URD 2025 p. PDF 313; DEU 2024 p. 259; URD 2023 p. 267. Flujo neto de las «otras adquisiciones»: 35,3 / 22,0 / 37,3 (DEU 2024 p. 288; URD 2025 p. 342 y p. 341). Ingresos anuales: 9,1 y 19,8 (URD 2025 p. 341 y p. 339). `python3 -I evidencia_pdf.py …` → `evidencia_pdf.txt`: 25 pasajes, 0 fallos, con dos extractores. Medias: `recalculo_independiente.txt`, sección I.
- **Corrección propuesta.**
  1. Corregir el fundamento con la definición publicada y sus umbrales.
  2. Rebajar la inferencia a lo que se sostiene: «sin compras importantes». Decir que no se publica qué parte del efecto volumen procede de compras pequeñas.
  3. Dar la sensibilidad con los importes publicados: 31,5 de media para las «otras adquisiciones» y 127,7 para todas, con la nota de que 134,3 de los 383,0 de la ventana son pagos aplazados de Lavartex.
  4. Precisar M6: finalidad de las compras pequeñas y crecimiento orgánico sin ellas.
  5. Decir que la condición «se revisa si el crecimiento orgánico en volumen deja de ser positivo» no es observable con lo publicado.
- **Lo que no propongo.** Ninguna cifra para R_compras. Aprobar o no (4b) como hipótesis sigue siendo de la persona responsable.

### V2 · menor · E4, V-F1i, V-F1j y T15 · lo que se cobra con un término explícito sigue en el denominador del ancla de S2C

- **Dónde.** Especificación: E4 (fórmula de C53 y la frase «si se documentan compras de reposición […] ya están en R»); E5, V-F1i y V-F1j; E9, T15. Propuesta: tabla de correspondencia, filas de la transición y de las compras de cartera.
- **Evidencia.** `python3 -I sondas_caja.py …` → `sondas_caja.txt`: S1a, motor − caja = −7 / −8,51 / −8,93 / −10,86 / −11,40 en los años 1, 5, 6, 10 y 11; S1b, coherente al sacarla del ancla; S1c, coherente a crecimiento cero; S2a, −9 … −14,66; S2b y S2c, coherentes. Con las funciones del autor: `contraprueba_con_funciones_del_autor.txt`, las mismas cifras.
- **Corrección propuesta.** Una regla en E4: lo que se cobra fuera de ΔV/S2C y no está en D_X sale del denominador del ancla. Añadir a V-F1i y a V-F1j la condición «cobrada como término y también en el ancla». Un caso en T15 con crecimiento y con el ancla calculada.

### V3 · menor · N1 · la caja del earnout y la actualización de 2025 están publicadas

- **Dónde.** Respuesta: §4, fila N1 de la tabla («[I]: la línea del pago no se ha identificado») y «Límite declarado de N1» («la de 2025 no se publica por separado»). Propuesta: §5.1, fila N1 y «Límite de N1»; tabla única, fila 5a; tabla de correspondencia, fila de N1, que dice «su caja está en las compras» sin marca.
- **Evidencia.** DEU 2024 p. 288; URD 2025 p. 341, p. 342 y p. 352; URD 2025 p. 313; DEU 2024 p. 259 (`evidencia_pdf.txt`). Conciliación de la línea fiscal y tamaño del límite: `recalculo_independiente.txt`, sección D.
- **Corrección propuesta.** Citar la nota 2.4 y pasar la ubicación de la caja a [P]. Corregir la frase sobre 2025. Si se quiere cerrar el límite, verificar 12,4 / 5,6 / 0,7 con el procedimiento del CSV y dar su efecto: −0,790 y −1,661 según mi lectura.

### V4 · menor · N1 y T16 · alcance de la regla en el τ de cinco años y dependencia de E8.1

- **Dónde.** Propuesta: texto de (5a) («en la ventana de calibración») y §5.1. Especificación: E3 y T16.
- **Evidencia.** `recalculo_independiente.txt`, sección C: −11,605 y −9,765 con el τ de cinco años; −9,141 y −9,763 con el de la ventana. Sección D: 2021–22, +0,416 y +0,466. `sondas_caja.txt`, S3. URD 2022 p. 285; URD 2023 p. 302 y p. 345.
- **Corrección propuesta.** Decir en la regla si alcanza a los ejercicios de 2021–22 que entran en el τ de cinco años. Decir en T16 y en la fila de (5a) que la cifra es la de la convención registrada del tipo, y dar el intervalo.

### V5 · menor · (1b) y (2)(v) · la sensibilidad de 16,8 es la de los pagos; falta la amortización ROU que devuelve f

- **Dónde.** Propuesta: tabla única, filas 1b y 2; §1, «Peso del arrendamiento»; §2, «PPA (2)»; §5.3. Especificación: E2, `EBIT_NIIF16_PPA_constante`; E8.5.
- **Evidencia.** `recalculo_independiente.txt`, secciones F y G: −16,778237; +10,118279; −6,659958; PPA +4,206; los dos efectos de escala en A2, −5,913. `sondas_caja.txt`, S5. El informe, §5.5, ya da el 10,1.
- **Corrección propuesta.** Dar en (1b) las dos partes y su suma. Extender el inciso (v) y `perimetro_margen` a la amortización ROU. Decir el sentido del 4,206.

### V6 · menor · terminal · dos fórmulas para la misma comprobación; «debe justificarse» frente a INFORMA

- **Dónde.** Propuesta: §4 y severidad de V-F1k. Especificación: E4, «Terminal», y E5, V-F1k. No se citan Convenciones V6.3 §3 ni `Diagnóstico V6`, bloque 10.
- **Evidencia.** `munger_v2_r1/v6/docs/Convenciones_financieras_V6_3.md`, §3. Libro de Elis, `Diagnóstico V6`, filas 176–179 (`recalculo_independiente.json`, `A_libro.diagnostico_bloque_10`). Sección H de `recalculo_independiente.txt`. `sondas_caja.txt`, S4.
- **Corrección propuesta.** Decir cuál de las dos fórmulas rige y por qué, y qué relación tiene V-F1k con el aviso y el umbral que ya existen. Decidir si la diferencia exige justificación (entonces, como V-F1c: aviso con justificación obligatoria) o solo se informa, y escribirlo igual en los tres sitios.

### V7 · menor · E3 · «sin cambios en la estructura del flujo» frente a los términos explícitos

- **Dónde.** Especificación: E3, último punto; E2, valores `termino_explicito` y `reposicion_con_importe`, y el motivo para no admitir `EBIT_NIIF16_PPA_decreciente`.
- **Evidencia.** Lectura. La fórmula del término solo está en `controles_sinteticos_f1.py` (`extra`, restado también en el año 11).
- **Corrección propuesta.** Escribir en E3 la fórmula del término en los años 1–10 y en el año 11, con su horizonte, o retirar la frase. Conciliarla con el motivo dado para la PPA decreciente.

### V8 · menor · (3a) · la cota 867,2 es de R_propia y transición

- **Dónde.** Propuesta: tabla única, fila 3a; §3, «Perímetro de R» y «Cota superior».
- **Evidencia.** `recalculo_independiente.txt`, sección I: capex propio medio 867,167; adquisiciones 127,667; suma 994,833.
- **Corrección propuesta.** Decir que la cota es de R_propia más transición y que el intervalo mide la materialidad bajo (4b).

### V9 · menor · controles sintéticos · anclas a mano, P1 sin crecimiento y N1 sin caso

- **Dónde.** `scripts/controles_sinteticos_f1.py`; especificación, T15.
- **Evidencia.** `contraprueba_con_funciones_del_autor.txt`: P1, 5 casos y 0 con crecimiento; motor sintético frente a `motor_a`. §8.
- **Corrección propuesta.** Los casos de la tabla de §8.

### V10 · forma · frases sin sincronizar y rótulos

- E4, «se emite el aviso V-F1g»; E2, matriz, «si hay arrendamientos materiales»: contradicen a E5.
- V-F1i, «transición material conocida»: «material» sin importe ni umbral.
- «Terminal NORMAL −18,609» es la variación del flujo del año 11 (propuesta, respuesta y T16).
- La respuesta da las líneas fiscales sin signo: «en 2024, 0,8, y en 2025, 0,2». Publicado: 0,8 y (0,2), de sentido contrario.
- «Reparto no publicado [P]»: una ausencia no es [P]; es el resultado de una búsqueda.
- T15 y la respuesta, «coincide con `motor_a`»: con crecimiento y margen constantes y sin impuestos.
- Tabla de correspondencia: «ningún euro se omite» se refiere a los costes que tocan las decisiones; la columna del terminal de la transición no recoge la clasificación de crecimiento; `en_R` hace crecer la transición con las ventas (S1d).

### V11 · forma · textos de aprobación

- (1a): su política del §1 contiene la regla de (4a) y la severidad de los controles de (4b), (5a) y (5b). Decir la dependencia o sacar esas frases.
- (3b): «Decido si…» no es un texto que se pueda aprobar. Dar las opciones: pedir el dato, buscar en fuentes públicas, encargar una estimación documentada o mantener el bloqueo.
- (4b): «con su fundamento» y «su sensibilidad», pendientes de V1.

---

## 10. Carencias de datos o de política que bloquean y no son defectos

No las puede resolver el autor. No propongo ninguna cifra para cerrarlas.

| Carencia | Clase | Qué impide |
|---|---|---|
| **M1.** Reparto del capex propio entre mantenimiento y crecimiento, por bloque y año; del plan climático, importe, horizonte y finalidad | Dato | R, f, el flujo de partida y el ancla de Elis; clasificar la transición. Es el bloqueo principal |
| **M2.** Tasa de bajas de clientes y desembolso por cliente nuevo | Dato | La parte de R_propia que repone clientes |
| **M6.** Finalidad de las compras. Con V1, en concreto: para qué son las compras pequeñas (31,5 al año de media) y cuánto fue el crecimiento orgánico sin ellas. Enlaza con M5, precio frente a volumen | Dato; o política, si se aprueba (4b) como hipótesis | Sustituir la hipótesis (4b) por un dato |
| **N2.** Fiscalidad de la plusvalía de 2025, dónde se cobró la indemnización y reposición de los activos | Dato | Normalizar N2 y dar un efecto conjunto de la normalización |
| **Perímetro de las palancas S2C y ROIC de Elis** | Juicio de la fase C, con R conocido | V-F1g y V-F1k; la compatibilidad del terminal |
| **Convención del tipo de proyección** (E8.1): cinco años frente a la ventana | Política, fuera de F1 | Nada por sí sola. Mueve la cifra de N1 entre −9,1 y −11,6 |
| **Umbral de V-F1a**, si se quiere uno; y qué se hace con el umbral del aviso del terminal que el libro ya tiene (`Diagnóstico V6!C179`, 5 puntos) | Política | Nada: sin umbral, V-F1a bloquea con cualquier importe |
| **Peso del arrendamiento en una valoración** | Hipótesis que se declara al valorar | Nada mientras sea referencia de ensayo |

**No es una carencia:** la actualización del earnout de 2023–25 y la caja del earnout están publicadas (V3). Falta verificarlas con el procedimiento del autor, no encontrarlas.

Se conserva `pendiente_de_datos` para Elis.

---

## 11. Límites: lo que no reproduje y lo que leí solo en parte

- **No reproducido:** `prueba_caja_no_nula.py`, que usa LibreOffice y el encargo excluye; `contraste_f1.py` consume su resultado conservado. Fuera del alcance y sin ejecutar: el verificador de cifras, sus tests, la mutación y las sondas de metadatos.
- **Sí reproducido:** todo lo demás que pedía el encargo, sin excepción (§2).
- **Leído entero:** la revisión externa y su encargo; la respuesta; la propuesta; la especificación de E0 a E10, salvo T14; los dos scripts nuevos; las Convenciones V6.3.
- **Leído en parte:**
  - del informe, §3 a §10 enteros y el diff de §4.2, §6.4 y §9; no he releído §0–§2, §12 ni §13;
  - de `contraste_f1.py`, las primeras 340 líneas (datos y motor); el resto lo he ejecutado, no leído;
  - T14, que es del verificador, por encima;
  - no he leído `fase_c.json`, `PUNTO_DE_RECUPERACION.md` ni `REGISTRO_CONFIGURACION.md`.
- **PDF:** 25 pasajes en páginas concretas, no una auditoría de las 752 cifras. De la lista de «otras adquisiciones» he sumado 2024 y 2025; la de 2023 no. La aportación de esas compras al crecimiento orgánico de cada año no se publica y no la estimo.
- **Cifras [LECTURA]:** 17, de nueve páginas. Están en `recalculo_independiente.json`, con documento, página y literal. No están en el CSV verificado.
- **Sondas:** las mías son de crecimiento y margen constantes, salvo S3, que no tiene crecimiento. Muestran definiciones, no datos de Elis.
- **No he calculado valores por acción** ni he comparado con ningún precio.
- **No he revisado** las observaciones U1–U6 de la revisión n.º 9 ni el commit `d5188bb`, posterior al congelado.

---

## 12. Archivos de esta revisión

Bajo `docs/validacion_economica_paralela/frente_E_F1_elis/revision/`:

| Archivo | Contenido |
|---|---|
| `REVISION_PROPUESTA_P1_P4.md` | Este informe |
| `scripts_revisor_p1_p4/reproducir.sh` | Reproducción completa: los tres scripts del autor y los cuatro del revisor |
| `scripts_revisor_p1_p4/recalculo_independiente.py` | Recálculo desde el CSV: base, 12 escenarios, convención del tipo, límite de N1, diagnóstico, arrendamientos, PPA, terminal y compras |
| `scripts_revisor_p1_p4/evidencia_pdf.py` | Huellas de los PDF, 25 pasajes con dos extractores y suma de las «otras adquisiciones» |
| `scripts_revisor_p1_p4/sondas_caja.py` | Sondas sintéticas propias, S1 a S5 |
| `scripts_revisor_p1_p4/contraprueba_con_funciones_del_autor.py` | Las dos sondas principales con las funciones del autor; motor sintético frente a `motor_a` |
| `resultados_revisor_p1_p4/` | Las salidas de esos scripts (`.json` y `.txt`), `reproduccion.txt` y `materializacion_base_414.txt` |

Comandos, desde `scripts_revisor_p1_p4/`, con `<frente>` = la carpeta del autor en un worktree de `13f864f` y `<base>` = `munger_v2_r1` materializado:

```bash
bash reproducir.sh <frente> <base> ../resultados_revisor_p1_p4
```

```bash
python3 -I recalculo_independiente.py --cifras <frente>/datos/cifras_fuente.csv --libro <base>/personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_14/elis_decisiones/Elis/Elis_v63_evaluada.xlsx --copia-autor <frente>/resultados/copia_investigacion_f1.json --salida ../resultados_revisor_p1_p4/recalculo_independiente.json --informe ../resultados_revisor_p1_p4/recalculo_independiente.txt
```

```bash
python3 -I evidencia_pdf.py --base <base> --fuentes <frente>/datos/fuentes.json --salida ../resultados_revisor_p1_p4/evidencia_pdf.json --informe ../resultados_revisor_p1_p4/evidencia_pdf.txt
```

```bash
python3 -I sondas_caja.py --salida ../resultados_revisor_p1_p4/sondas_caja.json --informe ../resultados_revisor_p1_p4/sondas_caja.txt
```

```bash
python3 -I contraprueba_con_funciones_del_autor.py --scripts-autor <frente>/scripts --controles-autor <frente>/resultados/controles_sinteticos_f1.json --salida ../resultados_revisor_p1_p4/contraprueba_con_funciones_del_autor.json --informe ../resultados_revisor_p1_p4/contraprueba_con_funciones_del_autor.txt
```

`recalculo_independiente.py` funciona sin `--libro` y sin `--copia-autor`: entonces solo comprueba los valores de referencia de E9 y de T16.
