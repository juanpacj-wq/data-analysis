"""
Programa principal para validación de archivos Excel
"""
import os
import logging
from config import LOGGING_CONFIG
from file_operations import cargar_hoja_excel, guardar_errores_consolidados, guardar_filas_con_multiples_errores, guardar_datos_limpios
from validation_engine import validar_dataframe

logging.basicConfig(
    filename=LOGGING_CONFIG['filename'],
    level=getattr(logging, LOGGING_CONFIG['level']),
    format=LOGGING_CONFIG['format'],
    datefmt=LOGGING_CONFIG['datefmt']
)

logger = logging.getLogger(__name__)


def validar_archivo_excel(ruta_archivo, nombre_hoja):
    """
    Valida los datos de una hoja específica de un archivo Excel
    
    Args:
        ruta_archivo (str): Ruta al archivo Excel
        nombre_hoja (str): Nombre de la hoja a validar
    
    Returns:
        tuple: (DataFrame errores, DataFrame múltiples errores, DataFrame original, dict celdas con errores)
    """
    # Cargar el archivo
    df = cargar_hoja_excel(ruta_archivo, nombre_hoja)
    if df is None:
        return None, None, None, None
    
    # Iniciar validación
    logger.info(f"Iniciando validación de la hoja '{nombre_hoja}' del archivo: {ruta_archivo}")
    
    # Validar el DataFrame
    return validar_dataframe(df, nombre_hoja)


def main():
    """
    Función principal que ejecuta la validación del archivo Excel
    """
    # Archivo Excel a procesar
    ruta_archivo = "DATA_BASE.xlsx"
    
    # Validar que el archivo exista
    if not os.path.exists(ruta_archivo):
        logger.error(f"El archivo {ruta_archivo} no existe.")
        print(f"El archivo {ruta_archivo} no existe.")
        return
    
    # Hojas a procesar
    hojas = ["G3.0", "G3.2"]
    
    # Diccionarios para almacenar resultados
    errores_por_hoja = {}
    multiples_errores_por_hoja = {}
    datos_originales = {}
    celdas_con_errores_por_hoja = {}
    
    # Procesar cada hoja
    for hoja in hojas:
        print(f"\n{'='*50}")
        print(f"Procesando hoja: {hoja}")
        print(f"{'='*50}")
        
        df_errores, df_multiples_errores, df_original, celdas_con_errores = validar_archivo_excel(
            ruta_archivo, hoja
        )
        
        # Almacenar resultados
        errores_por_hoja[hoja] = df_errores
        multiples_errores_por_hoja[hoja] = df_multiples_errores
        datos_originales[hoja] = df_original
        celdas_con_errores_por_hoja[hoja] = celdas_con_errores
    
    # Guardar resultados
    ruta_errores_consolidados = "errores_DATA_BASE_consolidado.xlsx"
    guardar_errores_consolidados(errores_por_hoja, ruta_errores_consolidados)
    
    ruta_filas_a_borrar = "Posibles_filas_a_borrar.xlsx"
    guardar_filas_con_multiples_errores(datos_originales, celdas_con_errores_por_hoja, ruta_filas_a_borrar)
    
    # Guardar archivo limpio sin filas con errores
    ruta_datos_limpios = "DATA_BASE_limpio.xlsx"
    guardar_datos_limpios(datos_originales, celdas_con_errores_por_hoja, ruta_datos_limpios)
    
    print("\nProceso de validación completado para todas las hojas.")
    logger.info("Proceso de validación completado para todas las hojas.")


if __name__ == "__main__":
    main()