# Inventario del expediente de la etapa 1 de Elis (14-nov-2026)

Sin repetir la etapa 1. Ni el Excel ni la respuesta acreditan ningún dato: son el punto de partida para localizar cada cifra en las fuentes oficiales.

## 1. Archivos recibidos (hechos)

| Archivo | SHA-256 | Procedencia |
|---|---|---|
| `Elis_evaluada.xlsx` | `b775e6b061b752cc531d72d82ba84a803fb0bfe3431c17b70bad7dbd5b43151b` | adjunto de la persona responsable (14-nov, 11:16) |
| `Elis_respuesta.md` | `999c42d452ec42aa861bc15e9e8e893980bb5b247417697d3be0a2871599c9fe` | ídem |
| 10 informes anuales 2016–2025 (Document de référence 2016; Registration Documents 2017–2018; Universal Registration Documents 2019–2025, el de 2024 en francés) | `elis_fuentes/HUELLAS_PDF.txt` | carpeta ELIS del ordenador de la persona responsable, copiada con sus bytes; texto con marcas de página en `elis_fuentes/texto/` (287 a 468 páginas cada uno) |

## 2. Integridad y versión (hechos)

- **Excel íntegro:** el ZIP no tiene errores de CRC y tiene 12 partes.
- **Plantilla V5.3:** las hojas Análisis, Guía Simply Wall St, Opciones y Control maestro tienen las mismas dimensiones que la etapa 1 de Viscofan (188 × 5, 71 × 3, 18 × 9 y 102 × 14).
- **Fecha de análisis:** 5-nov-2026. **Unidad:** mm EUR. **Norma:** IFRS.
- **Veredicto de la hoja:** «DESCARTAR · demasiado difícil», porque C13 = No. El juicio de la etapa 1 es «Vigilar». Esto no es una valoración del motor B, ni influye en la selección, que ya está fijada.

## 3. Datos y fechas (hechos; inventario completo en `elis_etapa1/inventario_control_maestro.txt`)

- **El Excel V5.3 no tiene Historia de 10 años.** La Historia 2016–2025 de la V6.3 se construye en la extracción de la etapa 1 hacia `fase1_v63.json` (como en Viscofan, 4.12).
  - Para Elis está por hacer, desde los 10 informes ya conservados, con el registro de verificación de las entradas.
  - Es una empresa nueva, así que no rige la regla de no rehacer diez años de extracción de los casos existentes.
- **Datos de la etapa 1 con período de 2026, que no es la base de 2025:**
  - C24: ROCE LTM a jun-26;
  - C31, C33, C34, C53 y C54: balance a 30-jun-2026 de la nota de prensa del primer semestre de 2026;
  - C40: caja libre LTM a jun-26;
  - C41 y C55: acciones pro forma tras la conversión de la OCEANE del 7-oct-2026;
  - C37: precio del 4-nov-2026;
  - C38: ficha de un tercero de jun-2026;
  - C57: Bund del 4-nov-2026;
  - C76: caja a 30-jun-2026;
  - C97: operaciones de directivos de nov-2025 a nov-2026.
- **Datos de 2025 o de varios años hasta 2025:** C26, C28, C32, C46–C50, C60, C88 y C96.

## 4. Tratamiento propuesto (sin adoptar)

**Base del 31-dic-2025** (último ejercicio auditado), como en Vidrala y Viscofan. Los datos de balance de 2026 se reexpresan al 31-dic-2025 con el URD 2025 mediante `cambiar_base.py`, que es el mecanismo general de la 4.11, con antecedentes y fechas separadas.
- El precio, que es posterior a la base, va con su fecha separada.
- Las acciones van a una fecha declarada. La conversión de la OCEANE de oct-2026 es un hecho posterior: se identifica y no se mezcla con la base.
- Lo que no se reexprese conserva su período declarado y se trata como contraste, no como entrada del motor.

**Distinción contable obligatoria** (regla fijada antes de evaluar): los activos textiles propios que Elis alquila a sus clientes, es decir el lino, que se capitaliza y amortiza (inmovilizado, capex de lino), no son los derechos de uso de los activos que Elis arrienda (NIIF 16).
- Cada entrada se etiqueta con su concepto.
- La inversión de P-M1 y el perímetro, «Caja» frente a «NIIF 16», se construyen sin mezclar los dos conceptos.

## 5. Documentación material que falta (para verificar las celdas con fechas de 2026)

| Dato | Período | Fuente necesaria | Descarga |
|---|---|---|---|
| Caja, deuda, capitales y circulante a 30-jun-2026; caja libre LTM | 1S 2026 | informe financiero semestral 2026 (EN y FR) | `descargar_fuentes_elis.bat` |
| Contraste del semestre y de las guías | 1S 2026 | comunicado y presentación de resultados del 1S 2026 | ídem |
| Contraste del ejercicio 2025 | FY2025 | comunicado de resultados anuales 2025 | ídem |
| Acciones tras la conversión de la OCEANE | oct-2026 | resultados de la conversión y ajuste del ratio | ídem (páginas web) |
| Acciones en circulación y derechos de voto al 30-sep-2026 | 30-sep-2026 | declaración mensual (L.233-8 II): se localiza en la lista de comunicados de Euronext que descarga el `.bat` | ídem, en dos pasos |
| Precio de cierre del 4-nov-2026 y Bund | 4-nov-2026 | dato de mercado con fecha: se declara la fuente | sin bytes oficiales; se declara |

El `.bat` está en la carpeta ELIS del ordenador de la persona responsable. Guarda los archivos en `ELIS\descargas_2026` con `HUELLAS.txt`, y desde ahí se copian a la sesión.
