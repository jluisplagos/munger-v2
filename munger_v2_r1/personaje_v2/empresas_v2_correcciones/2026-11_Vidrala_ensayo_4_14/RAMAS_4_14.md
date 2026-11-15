# Ramas 4.14 de Viscofan y Vidrala (creadas el 14-nov-2026, 12:45)

- **Origen:** copias de los expedientes cerrados de la 4.13 (`2026-11_Vidrala_ensayo_4_13/viscofan/Viscofan` y `…/vidrala_condicionado/Vidrala`). Esos expedientes siguen congelados como control (precios de Sí de referencia: Viscofan 40,1640071815 y Vidrala 56,0180901889) y no se tocan.
- **Añadido al copiar:**
  - el registro de verificación de las entradas revisado de forma independiente (`verificacion_entradas.json`);
  - en Viscofan, el boletín de la Bolsa de Madrid del 3-nov-2026 (`fuentes_mercado/`).
- **Qué se hará en las ramas:**
  - corregir en la extracción los datos con discrepancia confirmada (con su página);
  - regenerar la fase C con el contrato 4.14;
  - S5 en Viscofan;
  - pipeline con agentes reales y auditoría nueva;
  - registro de entradas actualizado y revisado de nuevo en lo que cambie.
  - Lo que depende de una decisión (D3, acciones; tratamiento de la venta de Italia en Vidrala) no se adopta: se calcula en sus versiones y se muestra por separado.
- **Estado a la copia:** las aprobaciones de la 4.13 siguen en la copia. Cualquier cambio del material las retira en la primera llamada (H5): es lo esperado en una rama.
