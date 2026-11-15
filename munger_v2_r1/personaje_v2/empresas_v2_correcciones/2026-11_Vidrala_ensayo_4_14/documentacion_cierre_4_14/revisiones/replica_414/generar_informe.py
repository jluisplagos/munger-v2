# -*- coding: utf-8 -*-
import json, sys
sys.dont_write_bytecode = True
D = '/home/claude/trabajo_4_14/agentes/replica_414/'
s = json.load(open(D + 'salida_replica.json'))
rc = json.load(open(D + 'salida_replica_recalc.json'))


def fmt(x):
    if isinstance(x, bool) or x is None:
        return str(x)
    if isinstance(x, float):
        return f'{x:.15g}'
    return str(x).replace('|', '/')


def tabla(filas, con_rel=True):
    out = ['| Magnitud | Expediente | Réplica | Diferencia (réplica − expediente) | Dif. relativa | Veredicto |', '|---|---|---|---|---|---|']
    for f in filas:
        d = f.get('diferencia'); r = f.get('dif_rel')
        out.append(f"| {f['magnitud']} | {fmt(f['expediente'])} | {fmt(f['replica'])} | {fmt(d) if d is not None else '—'} | "
                   f"{('%.2e' % r) if isinstance(r, float) else '—'} | **{f['veredicto']}** |")
    return '\n'.join(out)


L = []
A = L.append
A('# Réplica independiente de la escalera de precio · expedientes finales 4.14')
A('')
A('Revisión interna (agente de réplica, contexto limpio). Fecha: 14-nov-2026. Tolerancia: 1e-6 relativa; texto y booleanos, igualdad exacta.')
A('')
A('## Veredicto')
A('')
n_pasa = sum(1 for e in s['expedientes'].values() for f in e['tabla'] + e['intermedios'] if f['veredicto'] == 'PASA')
n_falla = sum(1 for e in s['expedientes'].values() for f in e['tabla'] + e['intermedios'] if f['veredicto'] == 'FALLA')
m_pasa = sum(1 for e in s['efecto_denominador'].values() for f in e['comparacion'] if f['veredicto'] == 'PASA')
m_falla = sum(1 for e in s['efecto_denominador'].values() for f in e['comparacion'] if f['veredicto'] == 'FALLA')
A(f'- **Escalera de los tres expedientes: reproducida.** Comparaciones con resultados.json, precio.json y caché del libro: {n_pasa} PASA, {n_falla} FALLA. '
  'La mayor diferencia relativa en V_MALO, V_NORMAL, V_BUENO, el ponderado y el precio de Sí es de unos 3,5e-15, es decir, error de redondeo en coma flotante.')
A(f'- **Efecto aislado del denominador (Viscofan y Elis): reproducido.** {m_pasa} PASA, {m_falla} FALLA frente a los ficheros de efecto, con todos sus casos (incluidos los de dilución).')
A('- La zona es «caro» en los tres expedientes, y en todas las variantes del denominador.')
A('- No he ajustado nada para que cuadre. Hubo un emparejamiento erróneo, mío, en la primera pasada (Elis, ver §5). Lo corregí cambiando con qué caso se compara, no el cálculo.')
A('')
A('## 1. Método')
A('')
A('- Código propio en `replica.py`. No importa ningún script del proyecto ni usa LibreOffice. Los libros se abren con openpyxl, sin guardar nada.')
A('- **Solo se leen constantes.** `Libro.inp()` lee del libro abierto con `data_only=False` y lanza una excepción si la celda pedida es una fórmula. Así ningún resultado intermedio del libro entra en el cálculo.')
A('- **Única lectura de caché usada para calcular:** el estado técnico del Motor (`B252` bloqueo, `B253` moneda comparable, `B254`, `B255` = «COMPLETO Y VÁLIDO»). Son 49 reglas (filas 201–249) que no he reimplementado. Solo deciden si hay lectura, no el valor.')
A('- Cadena reimplementada a partir de las fórmulas del libro:')
A('  - Historia: series 29–31 y anclas C43, C44, C48, C49, C52, C58 (f), C63, C64, C65, C66 y C70.')
A('  - Análisis: C52.')
A('  - Configuración V6.4: B5–B93, las 28 o 29 comprobaciones de §9 y la sección 11 NIIF 16 de la V6.4.1.')
A('  - Diagnóstico V6: C5, C9–C12, C15 (r operativa) y C16.')
A('  - Motor, filas 6–8: rama heredada y rama experimental (BU:DY), hasta BE…BK.')
A('  - Análisis C78 y C83.')
A('  - Tabla del DCF inverso: Motor 56–136, Análisis B108:B188, B191–B193 y C86.')
A('  - Escalera del Anexo C: P* en forma cerrada (C.3) contrastado con una bisección propia, precio de Sí = mín(P*, V_NORMAL), zona, G, L, crecimiento implícito, distancias y regla antigua C156.')
A('- Plantillas: el Motor de Vidrala es idéntico al de Viscofan. Su Configuración no tiene la sección 11 (B153 y B124 vacías). Elis (V6.3) no tiene la hoja Configuración V6.4 y su Motor solo tiene la rama heredada. Esto lo comprueba `difform.py`.')
A('- Supuestos activos que la réplica tuvo que reproducir:')
A('  - Viscofan: R1, SR1 con familia Θ (θ = 0,5), legado, perímetro NIIF 16 (Σ altas = 24,11) y t NOPAT = 22,12 %.')
A('  - Vidrala: R1, SR1 con familia Λ (λ = 1,15), cartera P0 explícita (filas 93), m0 manual (N2 = 18,547 %), «Media del ciclo» y t = 22,05 %.')
A('  - Elis: motor A con f = 0,04168 (Historia C58) y quiebra p = 5 % con recuperación 0.')
A('- Pruebas propias de la forma cerrada (`pruebas_anexo_C.py`): los 5 casos del Anexo C.5 y sus propiedades (G = 3L en P*, P* ≥ mín V, P* ≤ ponderado, independencia del orden, P* decrece con k). Todo PASA.')
A('- Comprobación adicional (`replica_sobre_recalc.py`): la réplica ejecutada sobre las copias `recalc/` da lo mismo (dif. rel. ≤ 3,4e-15). La copia `recalc/` difiere de la evaluada solo en la serialización de LibreOffice. Las constantes quedan con 15 cifras significativas (dif. rel. máxima 5,1e-15). El resto son textos de fórmula reescritos: «+(0.0)» pasa a «+(0)», «\'Análisis\'!» a «Análisis!» y «TRUE» a «TRUE()».')
A('')
for i, emp in enumerate(('Viscofan', 'Vidrala', 'Elis'), start=2):
    e = s['expedientes'][emp]
    A(f'## {i}. {emp} · motor {e["motor"]} · modo {e["modo_v64"] or "V6.3 (sin hoja de configuración)"}')
    A('')
    A(f'Libro: `{e["libro"]}`. Estado técnico (caché): {e["estado_cache"]}.')
    A('')
    A('### Escalera frente a resultados.json y precio.json')
    A('')
    A(tabla(e['tabla']))
    A('')
    A('### Pasos intermedios frente a la caché del libro (diagnóstico)')
    A('')
    A(tabla(e['intermedios']))
    A('')
    A('Réplica sobre la copia recalc/:')
    A('')
    A(tabla([dict(f, diferencia=(f['replica'] - f['expediente']) if isinstance(f['expediente'], float) else None) for f in rc[emp]]))
    A('')
A('## 5. Efecto aislado del denominador (Análisis C55)')
A('')
A('Los ficheros de efecto miden cada caso **sobre el libro anterior**: `viscofan/Viscofan/…_evaluada.xlsx` (rama 4.14) y `elis_motor_A/Elis/…_evaluada.xlsx`. '
  'Por eso apliqué a esos libros, con mi réplica, las celdas de cada caso y comparé el resultado. '
  'Además medí el efecto en el **libro final**: cambié solo C55 al valor anterior y dejé todo lo demás fijo.')
A('')
A('Entradas que cambian entre el libro anterior y el final (`diffinputs.py`):')
A('- Viscofan: C41, C47–C50 y C55.')
A('- Elis: C24, C31, C33, C34, C40, C41, C42, C46, C47, C50, C53, C54, C55 e Historia I25:L25.')
A('- Palancas, Configuración y Motor no cambian en ninguno de los dos.')
A('')
for emp in ('Viscofan', 'Elis'):
    x = s['efecto_denominador'][emp]
    ef = x['efecto_en_libro_final']
    A(f'### {emp}')
    A('')
    A(tabla(x['comparacion']))
    A('')
    A(f'Efecto en el libro final (C55 {ef["C55_nuevo"]} frente a {ef["C55_viejo"]}, todo lo demás fijo):')
    A('')
    A(f'- V (MALO, NORMAL, BUENO) con C55 nuevo: {[round(v, 10) for v in ef["V_C55_nuevo"]]}; con C55 anterior: {[round(v, 10) for v in ef["V_C55_viejo"]]}.')
    A(f'- Ponderado: {fmt(ef["pond_nuevo"])} frente a {fmt(ef["pond_viejo"])} (Δ = {fmt(ef["d_pond"])}).')
    A(f'- Precio de Sí: {fmt(ef["precio_si_nuevo"])} frente a {fmt(ef["precio_si_viejo"])} (Δ = {fmt(ef["d_precio_si"])}). Zona: {ef["zona_nuevo"]} / {ef["zona_viejo"]}.')
    A(f'- Cociente del precio de Sí = {fmt(ef["cociente_precio_si"])}; cociente de acciones (anterior ÷ nuevo) = {fmt(ef["cociente_acciones"])}.')
    A(f'- El mismo efecto medido sobre el libro anterior, según el fichero: Δ = {fmt(ef["d_precio_si_en_rama_segun_fichero"])}; mi réplica lo reproduce (tabla de arriba).')
    A('')
A('**Lectura.** El efecto del denominador es un reescalado exacto, por tres razones:')
A('- C55 solo entra en BK = BJ ÷ C55.')
A('- La r operativa del motor B usa la capitalización C41, no C55. En el motor A, la tasa es C56.')
A('- P*, el precio de Sí y el ponderado son homogéneos de grado 1 en V.')
A('')
A('Por eso el cociente del precio de Sí coincide con el de acciones hasta ~1e-15, y la zona no cambia.')
A('')
A('La pequeña diferencia entre la Δ medida en el libro anterior y la Δ medida en el libro final no es un error: el reescalado se aplica a un V distinto en cada libro.')
A('- Viscofan: −0,450571 frente a −0,449960. Cambia C41, y con ella la r operativa: 0,0826034 frente a 0,0826769.')
A('- Elis: +0,750200 frente a +0,749740. Cambian C46, C47 y C50, y con ellas f (Historia C58).')
A('')
A('**Lo que corregí durante la revisión.** En la primera pasada comparé «Elis final con el C55 anterior» con el caso «solo la capitalización» del fichero (6,556340), y salió FALLA (dif. rel. 6,1e-4). '
  'La causa estaba en mi emparejamiento, no en ninguno de los dos cálculos. El libro final de Elis también lleva las medias exactas de C46, C47 y C50, que en el motor A cambian f a través de C52 → C70 → C58. '
  'Así que lo que equivale a «final con el C55 anterior» es el caso «medias exactas» (6,552315). Contra ese caso cuadra con dif. rel. 4e-16. '
  'En Viscofan (motor B) esas celdas no intervienen, y la equivalencia con «solo la capitalización» sí es correcta.')
A('')
A('## 6. Lo que no he reproducido y por qué')
A('')
A('- **Estado técnico del Motor (B252–B255)** y las 49 reglas de las filas 201–249: lo leo de la caché. Solo condiciona que haya lectura; en los tres libros es «COMPLETO Y VÁLIDO», sin bloqueo y con moneda comparable. Sí compruebo por mi cuenta que Palancas C48 = Control maestro H4 = «EUR», que es lo que exige C15.')
A('- **Motor C**: no lo he implementado; ninguno de los tres expedientes lo usa.')
A('- **Aviso de la tasa de descuento** (Diagnóstico V6 C221, tornado), `coincide_C86` y la validez V6.4 que dan los ficheros de efecto (`valida_v64`): no los he reimplementado. No forman parte de la escalera.')
A('- **Comprobaciones de la Configuración V6.4 (§9)**: están implementadas según sus fórmulas, pero solo se han ejercitado en la rama válida (B90 = VERDADERO en Viscofan y Vidrala).')
A('- **Precio de Elis**: la escalera cuadra, pero precio.json avisa de que la tabla del DCF inverso no es utilizable (B191 = 0: «crecer destruye valor»). La réplica también da «no utilizable». '
  'El fichero de efecto advierte además que, con arrendamientos NIIF 16 en el motor A, el precio de Sí no es una conclusión utilizable. Eso es una cuestión de modelo y queda fuera de lo que una réplica aritmética puede validar.')
A('')
A('## 7. Archivos (todos en este directorio)')
A('')
A('- `replica.py`: motor de réplica (Historia, Configuración, Diagnóstico, Motor, tabla inversa y escalera).')
A('- `ejecutar.py`: ejecución y comparaciones; escribe `salida_replica.json` y `salida_consola.txt`.')
A('- `replica_sobre_recalc.py`: la misma réplica sobre las copias `recalc/`; escribe `salida_replica_recalc.json`.')
A('- `pruebas_anexo_C.py`: casos C.5 del Anexo C.')
A('- `difform.py`, `diffinputs.py`, `dump.py`: inspección de fórmulas y entradas, solo lectura.')
A('- `generar_informe.py`: genera este informe a partir de los JSON.')
A('')
A('Se ejecuta con `python3 -B ejecutar.py && python3 -B replica_sobre_recalc.py && python3 -B pruebas_anexo_C.py && python3 -B generar_informe.py`. No se ha modificado ningún archivo del proyecto: tras la ejecución, `find -newer` no devuelve nada en la raíz del ensayo.')
open(D + 'INFORME_REPLICA_4_14.md', 'w').write('\n'.join(L) + '\n')
print('ok', n_pasa, n_falla, m_pasa, m_falla)
