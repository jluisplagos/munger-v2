"""Ejemplos sintéticos de conservación de caja para revisar la propuesta F1.

No ejecuta el producto, no estima costes de Elis y no adopta una política.
Son contraejemplos de definiciones incompletas, no fallos de implementación.
Uso: python3 -I sondas_economicas.py --salida comprobaciones_sinteticas.json
"""
import argparse
from fractions import Fraction as F
import json
from pathlib import Path


def calibrar(ebitda, da_propia, rou, ppa, capex, r, fcf_base, ventas=100):
    ebit = F(ebitda) - F(da_propia) - F(rou) - F(ppa)
    f = (ebit - (F(capex) - F(r)) - F(fcf_base)) / F(ventas)
    return ebit - f * F(ventas)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--salida', type=Path, required=True)
    args = ap.parse_args()
    rows = []

    def add(name, obtenido, esperado, situacion, comentario):
        rows.append({'caso': name, 'flujo_modelizado_sintetico': float(obtenido),
                     'flujo_caja_del_escenario': float(esperado),
                     'diferencia': float(obtenido - esperado),
                     'situacion': situacion, 'comentario': comentario})

    # Sin impuestos, circulante ni intereses externos; todos los importes ficticios.
    # EBITDA 100 ya es posterior a cualquier gasto comercial corriente.
    # Capex de mantenimiento propio 20; arrendamientos pagados 12; ROU 10.
    base = calibrar(100, 20, 10, 0, 20, 20, 68)
    add('arrendamiento_una_vez', base, F(68), 'coherente',
        'Con R propio 20, caja económica = 100 - 20 - 12 = 68.')
    old = calibrar(100, 20, 10, 0, 20, 30, 68)
    add('A0_doble_arrendamiento', old, F(68), 'incoherencia_ilustrada',
        'Usar D&A total como R vuelve a cobrar el ROU: resultado 58.')

    # Un desembolso obligatorio de transición de 7 no puede quedar fuera de todo.
    omitted = calibrar(100, 20, 10, 0, 27, 20, 61)
    add('transicion_excluida_de_R_y_sin_linea_de_caja', omitted, F(61),
        'incoherencia_ilustrada', 'Si capex 27 incluye 7 necesarios, caja = 61, no 68.')
    included = calibrar(100, 20, 10, 0, 27, 27, 61)
    add('transicion_incluida_en_R', included, F(61), 'coherente',
        'La misma salida no se añade también como término separado.')
    add('transicion_separada_con_cargo_explicito', omitted - 7, F(61), 'coherente',
        'La clasificación separada es posible si la caja sigue cobrándose una vez.')

    # Si una compra de cartera de 9 fuera necesaria para conservar ventas,
    # crecimiento cero no permite eliminarla. No se afirma que eso ocurra en Elis.
    add('adquisicion_de_reposicion_tratada_solo_como_crecimiento', base, F(59),
        'incoherencia_ilustrada', 'Con ventas constantes, ΔV/S2C = 0; falta cobrar 9.')
    restored = calibrar(100, 20, 10, 0, 20, 29, 68)
    add('adquisicion_de_reposicion_incluida_en_R', restored, F(59), 'coherente',
        'Aquí R=29 supera capex propio=20 sin infrainversión: incluye una compra de cartera de 9.')

    # EBITDA 100 ya lleva el gasto comercial; R es inversión adicional, no ese OPEX.
    duplicate = calibrar(100, 20, 10, 0, 20, 25, 68)
    add('gasto_comercial_ya_en_EBIT_y_cargado_otro_vez_en_R', duplicate, F(68),
        'incoherencia_ilustrada', 'Añadir otra vez el gasto comercial ficticio de 5 da 63, no 68.')

    ppa = calibrar(100, 20, 10, 5, 20, 20, 68)
    add('PPA_no_monetaria_con_costes_de_reposicion_ya_cubiertos', ppa, F(68), 'coherente',
        'Devolver PPA no implica que reponer clientes sea gratis; depende de dónde se pagó el coste.')
    assert all(x['diferencia'] == 0 for x in rows if x['situacion'] == 'coherente')
    assert all(x['diferencia'] != 0 for x in rows if x['situacion'] == 'incoherencia_ilustrada')

    # Sensibilidades aritméticas de datos históricos, no supuestos adoptados.
    sales = [F('4309.4'), F('4573.7'), F('4796.8')]
    mean_sales = sum(sales) / 3
    payments = [F('130.8'), F('150.8'), F('177.9')]
    scaled_payment = (sum(payments) / 3) / mean_sales * sales[-1]
    result = {'naturaleza': 'ilustraciones sintéticas de definiciones; no ejecución de Munger',
              'casos': rows,
              'sensibilidad_arrendamientos_historica': {
                  'pagos_2025': 177.9, 'media_pagos_escalada_a_ventas_2025': float(scaled_payment),
                  'diferencia': float(payments[-1] - scaled_payment),
                  'politica_adoptada': False},
              'ningun_coste_sintetico_es_dato_de_Elis': True}
    args.salida.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'casos': len(rows), 'coherentes': sum(x['situacion'] == 'coherente' for x in rows),
                      'incoherencias_ilustradas': sum(x['situacion'] != 'coherente' for x in rows),
                      'producto_ejecutado': False}, ensure_ascii=False))


if __name__ == '__main__':
    main()
