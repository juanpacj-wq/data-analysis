# validators.py
"""
Módulo con todas las funciones de validación específicas
"""
import pandas as pd
from config import LIMITES_UG30, LIMITES_UG32, UNIDADES_VALIDAS, TIPOS_EVENTO_VALIDOS, RANGOS


def obtener_limites(unidad):
    """Obtiene los límites según la unidad"""
    if unidad == "UG3.0":
        return LIMITES_UG30
    elif unidad == "UG3.2":
        return LIMITES_UG32
    return {'disponibilidad_max': None, 'bruta_max': None, 'total_carbon_max': None}


def validar_fecha(valor, nombre_columna):
    """Valida si un valor es una fecha válida"""
    if pd.isna(valor):
        return True, None
    try:
        pd.to_datetime(valor)
        return True, None
    except:
        return False, {
            'columna': nombre_columna,
            'valor': str(valor),
            'regla': 'Formato de fecha válido (YYYY-MM-DD)' if nombre_columna == 'Fecha' else 'Formato de fecha y hora válido (YYYY-MM-DD HH:MM:SS)'
        }


def validar_entero_rango(valor, min_val, max_val, nombre_columna):
    """Valida si un valor es un entero dentro de un rango"""
    if pd.isna(valor):
        return True, None
    try:
        num = int(valor)
        if num < min_val or num > max_val:
            return False, {
                'columna': nombre_columna,
                'valor': str(valor),
                'regla': f'Entero del {min_val} al {max_val}'
            }
        return True, None
    except:
        return False, {
            'columna': nombre_columna,
            'valor': str(valor),
            'regla': f'Entero del {min_val} al {max_val}'
        }


def validar_numero_rango(valor, min_val, max_val, nombre_columna, es_porcentaje=False):
    """Valida si un valor es un número dentro de un rango"""
    if pd.isna(valor) or (isinstance(valor, str) and valor.strip() == ''):
        return True, None
    try:
        num = float(valor)
        if num < min_val or num > max_val:
            if es_porcentaje:
                return False, {
                    'columna': nombre_columna,
                    'valor': str(valor),
                    'regla': f'{min_val}% a {max_val}%'
                }
            else:
                return False, {
                    'columna': nombre_columna,
                    'valor': str(valor),
                    'regla': f'{min_val} - {max_val}'
                }
        return True, None
    except:
        if es_porcentaje:
            return False, {
                'columna': nombre_columna,
                'valor': str(valor),
                'regla': f'Número entre {min_val} y {max_val}'
            }
        else:
            return False, {
                'columna': nombre_columna,
                'valor': str(valor),
                'regla': f'Número entre {min_val} y {max_val}'
            }


def validar_unidad(valor):
    """Valida si la unidad es válida"""
    if pd.isna(valor):
        return True, None
    if valor not in UNIDADES_VALIDAS:
        return False, {
            'columna': 'Unidad',
            'valor': str(valor),
            'regla': ' o '.join(UNIDADES_VALIDAS)
        }
    return True, None


def validar_tipo_evento(valor):
    """Valida si el tipo de evento es válido"""
    if pd.isna(valor):
        return True, None
    try:
        tipo = int(valor)
        if tipo not in TIPOS_EVENTO_VALIDOS:
            return False, {
                'columna': 'Tipo de evento',
                'valor': str(valor),
                'regla': ', '.join(map(str, TIPOS_EVENTO_VALIDOS))
            }
        return True, None
    except:
        return False, {
            'columna': 'Tipo de evento',
            'valor': str(valor),
            'regla': ', '.join(map(str, TIPOS_EVENTO_VALIDOS))
        }