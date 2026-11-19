# Pruebas V6.3.2 F1 · circ

Fecha 2026-11-19 · plantilla `046b64fc7b7898c8…` · referencia `2bed4bac64b00a2a…`

**PASA: 16/16**

| Comprobación | Resultado | Detalle |
|---|---|---|
| C1 · Vinci tipo, normalización 2021–2025: C97 «circulante_a_cero», fila 95 = fila 14 en 2021–2025 (0 antes), fila 96 = 0, Motor V05 OK | PASA | V05 'OK' · None |
| C1 · libro = capa: f (C58) a 10⁻¹², ancla (C53) a 10⁻⁹ y reinversión media (C76) a 10⁻⁹; f ≈ 1,574 % y ancla ≈ 2,3226 | PASA | C58 0.0157439542453269 · C53 2.3226451421801 · C76 575.666666666667 |
| C1 · los 33 flujos del Motor (años 1–10 y 11, tres escenarios con las palancas del ejemplo) = capa (10⁻⁹) | PASA | desviación máxima 6.91e-11 |
| C1 · F1-LIBRO, F1-REPLICA, F1-CIRC y F1-K3c no saltan; F1-LIBRO dice que el libro V6.3.2 calcula la normalización (33 flujos) | PASA | [] |
| C2 · sin la normalización: el libro V6.3.2 es la V6.3.1 F1 con las mismas entradas (0 celdas distintas, igualdad exacta) | PASA | 39950 celdas · [] |
| C2 · sin la normalización K3c BLOQUEA (reinversión −1.514,333) y el libro y la capa coinciden (F1-LIBRO no salta) | PASA | ['F1-K3c'] |
| C1/C2 · identidad con los valores del libro: f normalizada = f − media del circulante de la ventana ÷ ventas medias (10⁻¹²) | PASA | 0.0157439542453269 frente a 0.015743954245326833 |
| C1/C2 · identidad: C53 normalizada = ΔV ÷ (Σ fila 31 sin normalizar − Σ fila 14 de H–L) (10⁻⁹) | PASA |  |
| C3 · solo la ventana (2023–2025): f normalizada, C53 vacía en el libro y en la capa; F1-CIRC bloquea (INCOMPLETO) y F1-LIBRO no | PASA | ['F1-CIRC'] |
| C4 · sin 2024 (ventana): f y C53 vacías, Motor V05 INCOMPLETO con su causa; la capa en pendiente_de_datos (F1-CIRC) sin error ni F1-REPLICA | PASA | 'Motor A · normalización del circulante: faltan años de la ventana que calibra f en Historia C94:L94 (la normalización cubre todos los años que usa la reinversi |
| C5 · regla no reconocida: C97 «no reconocida», f y C53 vacías, Motor V05 DATOS INVÁLIDOS; la capa bloquea (F1-LIBRO) sin F1-REPLICA | PASA | ['F1-LIBRO'] |
| C5 · marca no reconocida: C97 «no reconocida», f y C53 vacías, Motor V05 DATOS INVÁLIDOS; la capa bloquea (F1-LIBRO) sin F1-REPLICA | PASA | ['F1-LIBRO'] |
| C6 · A0_total con la normalización: el libro usa la rama de D_X con la fila 30 normalizada; f y ancla = capa; réplica conforme | PASA | ['F1-2i', 'F1-K3b', 'F1-K3c', 'V-F1a'] |
| C7 · libro V6.3.1 con la normalización declarada: F1-LIBRO bloquea (límite declarado: la salida es la V6.3.2 F1) y la capa da las cifras normalizadas | PASA | ['F1-LIBRO'] |
| C8 · Elis (su caja base NO excluye el circulante) con la normalización: el libro la calcula (= capa) y la capa bloquea con F1-CIRC DATOS INVÁLIDOS | PASA | ['F1-CIRC', 'F1-REGISTRO', 'V-F1g', 'V-F1i', 'V-F1j', 'V-F1k'] |
| C1 · el libro con la normalización aplicada (antes de recalcular) es ÍNTEGRO frente a la referencia: C93:L94 son entradas | PASA | VEREDICTO: ÍNTEGRO · 0 fallos · 0 avisos |
