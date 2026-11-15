# Hallazgo de alcance: motor A (plantilla V6.3) con arrendamientos NIIF 16 materiales · Elis · 14-nov-2026

**Origen.** Fase C (turno 1) del expediente `…_4_14/elis_motor_A/Elis` (agente Claude real; no es una revisión humana). La fase B ya lo había señalado como sesgo a la baja.

## Hechos

Fuentes: URD 2025, PDF pp. 327, 350 y 366; DEU 2024, PDF p. 296; resultados.json del expediente.

**Libro (motor A):**
- Precio de Sí 6,56 €; ponderado 7,17 €; precio 24,18 €.
- Valor sin crecimiento: 10,66 €/acción.
- FCF base de partida: 248,6 mm, frente a 308 de C52.

**El ancla f del motor A cuenta dos veces el coste de los arrendamientos:**
- la amortización de los derechos de uso NIIF 16 dentro del margen: 149,5 mm (2025);
- el pago de los arrendamientos dentro de f: 177,9 mm.

**Además, f incluye 85,7 mm de amortización de intangibles de adquisiciones** que el capex no repone.

## Efecto (cálculo de una réplica del motor que reproduce la hoja al céntimo; solo cambia f)

| | Libro | Réplica sin el sesgo |
|---|---|---|
| Sesgo | — | entre 59 y unos 229 mm al año, a la baja |
| Precio de Sí | 6,56 € | entre 9,95 y 19,65 € |
| Ponderado | 7,17 € | entre 10,76 y 21,02 € |
| Frente al precio (24,18 €) | por debajo | siempre por debajo: «caro» se sostiene |

El punto exacto dentro de ese rango depende del reparto del capex entre reposición y crecimiento, que Elis no publica.

## Interpretación

**Es un límite del modelo en lo económico.** El nivel del libro (6,56 €) no es defendible como valor. La conclusión de zona sí lo es.

**No encaja en las categorías L1–L3:** la fase C deja `limite_del_modelo.aplica = false` y lo declara.

**Consecuencia para el alcance (dictamen, parte D):** el motor A de la V6.3 **no queda validado para empresas con arrendamientos NIIF 16 materiales**, ni con crecimiento por adquisiciones con intangibles amortizados.
- Vidrala y Viscofan van por el motor B y no se ven afectadas.
- Elis es el primer caso real del motor A en el alcance de esta entrega, y el resultado es este límite.

## Decisión para la persona responsable (no adoptada)

**F1 · ancla f del motor A con NIIF 16.** Opciones:
- (a) declarar el límite y no usar el motor A en esos casos (alcance);
- (b) corregir la definición de f en la plantilla para no contar dos veces los arrendamientos ni los intangibles comprados. Exigiría cambiar la plantilla, probarla, revisarla y regenerar los expedientes del motor A;
- (c) tratar el sesgo como juicio de la fase C, caso a caso.

**Propuesta:** (a) para esta entrega, con (b) como trabajo posterior identificado.

**Lo que no cambia:** las fórmulas de la plantilla V6.3 no se tocan en la 4.14 sin decisión.
