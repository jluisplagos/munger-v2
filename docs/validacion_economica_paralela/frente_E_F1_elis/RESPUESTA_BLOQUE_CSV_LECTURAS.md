# Bloque CSV · cifras [LECTURA] al CSV verificado

Fecha: 16-nov-2026.

- **Encargo:** `ENCARGO_C20_CSV.md` de la revisión F1 v3 (`f5775dc`, repositorio auxiliar), segunda parte: pasar al CSV verificado las cifras [LECTURA] que el verificador acredite.
- **Base:** C20 `bf0d5c2`.
- **Esta entrega:** el commit que la contiene.

**Alcance.**
- Se añaden diez filas al CSV, sin tocar ninguna de las 752 anteriores.
- El verificador no cambia: es el de C20.
- La copia de investigación toma ocho de sus catorce lecturas de esas filas.
- **No se aplica N1**, no se adopta ninguna decisión (1a)–(5b) y Elis sigue en `pendiente_de_datos`.
- C48 = 108, C49 = 128,1, FCF base = 307,933 y E1/D3/E2/E6 no cambian.

## 1. Filas añadidas

Todas son del perímetro «consolidado IFRS, grupo Elis», en mm EUR y en modo `dos_columnas`. Las diez dan OK con el verificador de C20.

| Fila | Ejercicio | Documento, página | Rótulo | Literal | Edición | Lectura que sustituye |
|---|---|---|---|---|---|---|
| `FIN_ACTMEX_2025` | 2025 | URD 2025 p.313 | Accretion expense for the earnout pertaining to the acquisition in Mexico | 0.7 | vigente | `actualizacion_earnout_2025` |
| `FIN_ACTMEX_2024` | 2024 | URD 2025 p.313 | ídem | 5.6 | vigente | `actualizacion_earnout_2024` (antes leída en el DEU 2024) |
| `FIN_ACTMEX_FR_2023` | 2023 | DEU 2024 p.259 | Charge de désactualisation du complément de prix de l'acquisition réalisée au Mexique | 12,4 | vigente | `actualizacion_earnout_2023` |
| `FIN_ACTMEX_FR_2024` | 2024 | DEU 2024 p.259 | ídem | 5,6 | anterior | Segunda presentación de 2024 |
| `OOIE_EARN_U22_2021` | 2021 | URD 2022 p.285 | Earnout adjustments | (3.0) | vigente | `ajuste_earnout_2021` |
| `OOIE_EARN_U22_2022` | 2022 | URD 2022 p.285 | ídem | 2.1 | anterior | Antes de la reexpresión |
| `OOIE_EARN_U23_2022` | 2022 | URD 2023 p.302 | ídem | 2.4 | vigente | `ajuste_earnout_2022` |
| `ADQ_EARNDIF_FR_2023` | 2023 | DEU 2024 p.288 | Compléments de prix et paiements différés | (34,4) | vigente | `adq_earnouts_y_diferidos_2023` |
| `ADQ_EARNDIF_2024` | 2024 | URD 2025 p.342 | Earnouts and deferred consideration | (93.9) | vigente | `adq_earnouts_y_diferidos_2024` |
| `ADQ_EARNDIF_2025` | 2025 | URD 2025 p.341 | `re:^consideration\s{2,}` (rótulo partido en dos líneas) | (23.3) | vigente | `adq_earnouts_y_diferidos_2025` |

**Signos.**
- Los pagos de adquisiciones van con el signo impreso, como salida de caja.
- La copia de investigación los usa en positivo, con el signo de la lectura anterior, y lo declara en `VERIFICADAS`.

## 2. Lo que sigue en [LECTURA], y por qué

Siguen en [LECTURA] seis cifras: las columnas «Lavartex» y «otras adquisiciones» de la tabla de flujos por adquisición (nota 2.4), de 2023, 2024 y 2025.
- **Por qué:** son columnas por sociedad adquirida, no del grupo. El CSV del grupo no admite otro perímetro, y el contraste no calcula con ellas.
- **No intervienen en ningún cálculo:** la copia de investigación solo las lista.
- **Para pasarlas** haría falta otro perímetro declarado en el CSV y una regla del verificador para las columnas por sociedad. Ninguna de las dos cosas la pide el encargo.

## 3. Controles negativos

Se hicieron cuatro filas deliberadamente erróneas, solo en un CSV temporal del autor y no en el repositorio:

| Sonda | Resultado |
|---|---|
| Columna Lavartex de 2023 (31,4) declarada como total del grupo | PENDIENTE en ejercicio: «el token no está bajo ninguna columna reconocida». No queda OK |
| Columna «otras adquisiciones» de 2024 (10,7) declarada como total | PENDIENTE, por el mismo motivo |
| Cifra de 2024 (5.6) declarada como de 2025 | FALLO en ejercicio: «la columna es de 2024, no de 2025» |
| 2.1 del URD 2022, antes de la reexpresión, declarada vigente | FALLO en edición: la regla exige la publicación 2023 para 2022 |

**Límite.** Una columna por sociedad queda PENDIENTE, no FALLO. Basta para que el contraste no la use, porque solo calcula con filas sin FALLO, y una PENDIENTE usada se lista aparte. Pero no la rechaza.

## 4. Pruebas ejecutadas

Desde `scripts/`, sobre el árbol `munger_v2_r1` materializado. El libro es `elis_decisiones/Elis/Elis_v63_evaluada.xlsx`, SHA-256 `d2593777…92385`.

| Comando | Resultado | Salida |
|---|---|---|
| `verificar_cifras.py … --salida ../resultados/verificacion_cifras.json --exportar-paginas ../evidencias/paginas` | Código 2, por las 14 PENDIENTE de siempre. **762 filas: 748 OK, 14 PENDIENTE, 0 FALLO.** Las 752 anteriores no cambian; las 10 nuevas dan OK | `resultados/verificacion_cifras.json`; seis páginas nuevas en `evidencias/paginas/` |
| `contraste_f1.py …` | Código 0. **292 comprobaciones, 0 fallidas.** Salida idéntica byte a byte (`contraste_f1.json` y `.md`): el contraste no usa las filas nuevas | Sin cambios |
| `copia_investigacion_f1.py … --raiz …` | Código 0. **67 controles, 0 fallidos** (antes 58). Nuevos: 8 igualdades «lectura anterior = fila verificada» y la identidad de 2024 entre ediciones. Las cuatro sensibilidades de V3–V4 dan las mismas cifras, y siguen reproduciendo la revisión dirigida | `resultados/copia_investigacion_f1.{json,md,log}` |
| `test_verificar_cifras.py --raiz …` | Código 0. 143/143 y 13/13. Registro idéntico byte a byte | `resultados/test_verificar_cifras.log`, sin cambios |
| `test_contraste_residuos.py --libro …` | Código 0. 24/24 | Salida solo en consola, como hasta ahora |
| `cobertura_por_mutacion.py --libro …` | Código 0. **538 filas vigentes mutadas** (530 y las 8 vigentes nuevas). Las 8 nuevas quedan «no usada», que es la clase que declara el contraste («no declarada»: 119, antes 111). Ninguna diferencia con `cobertura_entradas`; las demás clases, sin cambio | `resultados/cobertura_por_mutacion.txt` |
| `sondas_metadatos.py --raiz … --autor .. --etiqueta CSV` | Código 0. **723/723** filas de tabla detectadas en unidad y 723/723 en perímetro, cada una en su dimensión. Sonda externa: 1/1 y 1/1 | `resultados/sondas_metadatos_CSV.json` |

**No se han repetido:**
- los controles sintéticos, que no leen el CSV;
- los scripts de los revisores n.º 1 a 9;
- LibreOffice.

## 5. Cambios en los textos

- **`copia_investigacion_f1.py`:**
  - nuevo diccionario `VERIFICADAS`, con las ocho lecturas y la fila y el signo de cada una;
  - las escenas de V3–V4 se rotulan «[cifras verificadas]»;
  - el JSON lleva, en cada lectura, su fila o el motivo por el que sigue en [LECTURA];
  - la reexpresión de 2022 queda registrada: 2,1 en el URD 2022 y 2,4 en el URD 2023, la vigente.
- **`README.md` y `INFORME_CONCILIACION_F1.md`:** recuentos del CSV y de la mutación.

## 6. Pendiente

- **Contraste externo** de este bloque, solo lo afectado. El revisor asignado está en el control común.
- **Las seis lecturas por sociedad**, solo si alguien decide declarar un perímetro por sociedad.
