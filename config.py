"""
Módulo de configuración con constantes y límites de validación
"""

# Límites  UG3.0
LIMITES_UG30 = {
    'disponibilidad_max': 170,
    'bruta_max': 195000,
    'total_carbon_max': 150
}

# Límites  UG3.2
LIMITES_UG32 = {
    'disponibilidad_max': 280,
    'bruta_max': 315000,
    'total_carbon_max': 200
}

LOGGING_CONFIG = {
    'filename': 'errores_validacion.log',
    'level': 'INFO',
    'format': '%(asctime)s - %(message)s',
    'datefmt': '%Y-%m-%d %H:%M:%S'
}

# valores validaciones
UNIDADES_VALIDAS = ["UG3.0", "UG3.2"]
TIPOS_EVENTO_VALIDOS = [-1, 0, 1]

# Rangos generales
RANGOS = {
    'periodo': (1, 24),
    'porcentaje_desviacion': (-100, 100),
    'alimentador_carbon': (0, 27),
    'suministro_caliza': (0, 60),
    'combustible_liquido': (0, 25000),
    'g_ln': (0, 164),
    'a_ln': (0, 188000)
}