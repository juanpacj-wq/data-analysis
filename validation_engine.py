
"""
Módulo principal del motor de validación
"""
import pandas as pd
import logging
from collections import defaultdict
from validators import (
    validar_fecha, validar_entero_rango, validar_numero_rango,
    validar_unidad, validar_tipo_evento, obtener_limites
)
from config import RANGOS

logger = logging.getLogger(__name__)


def validar_fila(fila, fila_num, df_columns):
    """
    Valida una fila completa del DataFrame
    
    Args:
        fila: Serie de pandas con los datos de la fila
        fila_num: Número de fila en Excel (1-based)
        df_columns: Columnas del DataFrame
    
    Returns:
        list: Lista de errores encontrados
        list: Lista de columnas con errores
    """
    errores_fila = []
    columnas_con_error = []
    
    # límites según la unidad
    unidad = fila.get('Unidad', None)
    limites = obtener_limites(unidad)
    
    # validar Fecha
    if 'Fecha' in df_columns:
        valido, error = validar_fecha(fila['Fecha'], 'Fecha')
        if not valido:
            errores_fila.append(error)
            columnas_con_error.append('Fecha')
    
    # validar Periodo
    if 'Periodo' in df_columns:
        valido, error = validar_entero_rango(fila['Periodo'], RANGOS['periodo'][0], 
                                            RANGOS['periodo'][1], 'Periodo')
        if not valido:
            errores_fila.append(error)
            columnas_con_error.append('Periodo')
    
    # validar Unidad
    if 'Unidad' in df_columns:
        valido, error = validar_unidad(fila['Unidad'])
        if not valido:
            errores_fila.append(error)
            columnas_con_error.append('Unidad')
    
    # validar columnas numéricas con límites según unidad
    columnas_con_limite_disponibilidad = [
        'Disponibilidad declarada(MWh)',
        'Despacho programado(MWh)',
        'Despacho final(real)(MWh)',
        'Energía neta despachada (MWh)'
    ]
    
    for col in columnas_con_limite_disponibilidad:
        if col in df_columns and limites['disponibilidad_max'] is not None:
            valido, error = validar_numero_rango(fila[col], 0, limites['disponibilidad_max'], col)
            if not valido:
                errores_fila.append(error)
                columnas_con_error.append(col)
    
    # validar Energía desviada (puede ser negativa)
    if 'Energía desviada (MWh)' in df_columns and limites['disponibilidad_max'] is not None:
        valido, error = validar_numero_rango(fila['Energía desviada (MWh)'], 
                                           -limites['disponibilidad_max'], 
                                           limites['disponibilidad_max'], 
                                           'Energía desviada (MWh)')
        if not valido:
            errores_fila.append(error)
            columnas_con_error.append('Energía desviada (MWh)')
    
    # validar %Desviación
    if '%Desviación (%)' in df_columns:
        valido, error = validar_numero_rango(fila['%Desviación (%)'], 
                                           RANGOS['porcentaje_desviacion'][0], 
                                           RANGOS['porcentaje_desviacion'][1], 
                                           '%Desviación (%)', es_porcentaje=True)
        if not valido:
            errores_fila.append(error)
            columnas_con_error.append('%Desviación (%)')
    
    # validar columnas con límite bruta_max
    columnas_con_limite_bruta = [
        'Energía bruta generada (kWh)',
        'Energía consumida (kWh)',
        'Energía reactiva generada (kVAr)',
        'Energía reactiva consumida (kVAr)'
    ]
    
    for col in columnas_con_limite_bruta:
        if col in df_columns and limites['bruta_max'] is not None:
            valido, error = validar_numero_rango(fila[col], 0, limites['bruta_max'], col)
            if not valido:
                errores_fila.append(error)
                columnas_con_error.append(col)
    
    # validar alimentadores de carbón
    for i in range(1, 9):
        col_name = f'Alimentador {i} de carbón (Ton)'
        if col_name in df_columns:
            valido, error = validar_numero_rango(fila.get(col_name), 
                                               RANGOS['alimentador_carbon'][0], 
                                               RANGOS['alimentador_carbon'][1], 
                                               col_name)
            if not valido:
                errores_fila.append(error)
                columnas_con_error.append(col_name)
    
    # validar Total carbón
    if 'Total carbón Alimentado caldera (Ton)' in df_columns and limites['total_carbon_max'] is not None:
        valido, error = validar_numero_rango(fila['Total carbón Alimentado caldera (Ton)'], 
                                           0, limites['total_carbon_max'], 
                                           'Total carbón Alimentado caldera (Ton)')
        if not valido:
            errores_fila.append(error)
            columnas_con_error.append('Total carbón Alimentado caldera (Ton)')
    
    # validar Suministro caliza
    if 'Suministro caliza (Ton)' in df_columns:
        valido, error = validar_numero_rango(fila['Suministro caliza (Ton)'], 
                                           RANGOS['suministro_caliza'][0], 
                                           RANGOS['suministro_caliza'][1], 
                                           'Suministro caliza (Ton)')
        if not valido:
            errores_fila.append(error)
            columnas_con_error.append('Suministro caliza (Ton)')
    
    # validar Consumo combustible
    if 'Consumo combustible líquido FO (gal)' in df_columns:
        valido, error = validar_numero_rango(fila['Consumo combustible líquido FO (gal)'], 
                                           RANGOS['combustible_liquido'][0], 
                                           RANGOS['combustible_liquido'][1], 
                                           'Consumo combustible líquido FO (gal)')
        if not valido:
            errores_fila.append(error)
            columnas_con_error.append('Consumo combustible líquido FO (gal)')
    
    # validaciones específicas para UG3.0
    if unidad == "UG3.0":
        for col in ['G-LN764', 'G-LN765']:
            if col in df_columns:
                valido, error = validar_numero_rango(fila[col], 
                                                   RANGOS['g_ln'][0], 
                                                   RANGOS['g_ln'][1], col)
                if not valido:
                    errores_fila.append(error)
                    columnas_con_error.append(col)
        
        for col in ['A-LN764', 'A-LN765']:
            if col in df_columns:
                valido, error = validar_numero_rango(fila[col], 
                                                   RANGOS['a_ln'][0], 
                                                   RANGOS['a_ln'][1], col)
                if not valido:
                    errores_fila.append(error)
                    columnas_con_error.append(col)
    
    # validar Fecha Evento
    if 'Fecha Evento' in df_columns:
        valido, error = validar_fecha(fila['Fecha Evento'], 'Fecha Evento')
        if not valido:
            errores_fila.append(error)
            columnas_con_error.append('Fecha Evento')
    
    # validar Tipo de evento
    if 'Tipo de evento' in df_columns:
        valido, error = validar_tipo_evento(fila['Tipo de evento'])
        if not valido:
            errores_fila.append(error)
            columnas_con_error.append('Tipo de evento')
    
    return errores_fila, columnas_con_error


def validar_dataframe(df, nombre_hoja):
    """
    Valida un DataFrame completo
    
    Args:
        df: DataFrame a validar
        nombre_hoja: Nombre de la hoja para logging
    
    Returns:
        tuple: (DataFrame con errores, DataFrame con filas múltiples errores, 
                DataFrame original, diccionario de celdas con errores)
    """
    errores = []
    errores_por_fila = defaultdict(int)
    celdas_con_errores = defaultdict(list)
    
    for idx, fila in df.iterrows():
        fila_num = idx + 2  # +2 porque idx es 0-based y Excel ajá, los encabezados
        
        errores_fila, columnas_con_error = validar_fila(fila, fila_num, df.columns)
        
        # Procesar errores encontrados
        for error in errores_fila:
            errores.append({
                'Fila de error': fila_num,
                'Columna problema': error['columna'],
                'Valor original incorrecto': error['valor'],
                'Reglas de negocio': error['regla']
            })
            errores_por_fila[fila_num] += 1
            logger.warning(f"Error en fila {fila_num}, columna {error['columna']}: {error['valor']} - {error['regla']}")
        
        if columnas_con_error:
            celdas_con_errores[fila_num] = columnas_con_error
    
    df_errores = pd.DataFrame(errores)
    
    filas_multiples_errores = []
    for fila_num, cantidad in errores_por_fila.items():
        if cantidad > 1:
            errores_fila = [e for e in errores if e['Fila de error'] == fila_num]
            for error in errores_fila:
                filas_multiples_errores.append({
                    'Fila de error': error['Fila de error'],
                    'Columna problema': error['Columna problema'],
                    'Valor original incorrecto': error['Valor original incorrecto'],
                    'Reglas de negocio': error['Reglas de negocio'],
                    'Cantidad de errores en fila': cantidad
                })
    
    df_multiples_errores = pd.DataFrame(filas_multiples_errores)
    
    cantidad_errores = len(errores)
    if cantidad_errores > 0:
        logger.info(f"Se encontraron {cantidad_errores} errores en la hoja '{nombre_hoja}'.")
        print(f"Se encontraron {cantidad_errores} errores en la hoja '{nombre_hoja}'.")
    else:
        logger.info(f"No se encontraron errores en la hoja '{nombre_hoja}'.")
        print(f"No se encontraron errores en la hoja '{nombre_hoja}'.")
    
    return df_errores, df_multiples_errores, df, celdas_con_errores