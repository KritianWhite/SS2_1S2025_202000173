import sys

from src.database import get_connection
from src.extract import extract_data
from src.transform import transform_and_clean_data
from src.load import load_to_sql_server, check_model_exists, fix_airport_data


def mostrar_menu():
    """
    Muestra el menú principal.
    """
    print("╔════════════════════════════════════════════════════╗")
    print("║          BIENVENIDO AL SISTEMA DE VUELOS           ║")
    print("╠════════════════════════════════════════════════════╣")
    print("║ [1] Borrar el modelo existente                     ║")
    print("║ [2] Crear nuevo modelo de datos                    ║")
    print("║ [3] Extraer información de los archivos fuentes    ║")
    print("║ [4] Procesar archivos de entrada específicos       ║")
    print("║ [5] Implementar consultas analíticas predefinidas  ║")
    print("║ [6] Salir                                          ║")
    print("╚════════════════════════════════════════════════════╝")

def borrar_modelo_existente(cnxn):

    try:
        with open("practica1/database/drop_model.sql", "r", encoding="utf-8") as f:
            sql_script = f.read()
        cursor = cnxn.cursor()
        # Ejecutar cada instrucción SQL separada por ";"
        for statement in sql_script.split(";"):
            if statement.strip():
                cursor.execute(statement)
        cnxn.commit()
        print("El modelo de datos ha sido eliminado exitosamente.")
    except Exception as e:
        print("Error al eliminar el modelo de datos:", e)

def crear_modelo_nuevo(cnxn):
    
    print("Creando modelo de datos...")
    try:
        with open("practica1/database/create_model.sql", "r", encoding="utf-8") as f:
            sql_script = f.read()
        cursor = cnxn.cursor()
        # Ejecutar cada instrucción SQL separada por ";"
        for statement in sql_script.split(";"):
            if statement.strip():
                cursor.execute(statement)
        cnxn.commit()
        print("\nEl modelo de datos ha sido creado exitosamente.")
    except Exception as e:
        print("Error al crear el modelo de datos:", e)


def extraer_informacion_archivos(cnxn):
    """
    Extrae los datos del archivo CSV por defecto, los almacena en memoria,
    los transforma y muestra una muestra de cada tabla resultante.
    """
    csv_path = "practica1/data/VuelosDataSet.csv"  # Archivo CSV por defecto
    # Extracción: guardar el DataFrame en memoria
    df_extraction = extract_data(csv_path)
    if df_extraction is None:
        print("Falló la extracción de datos.")
        return None
    
    # Transformación: limpiar y transformar los datos
    print("Iniciando transformación de datos...\n")
    tablas = transform_and_clean_data(df_extraction)
    
    if 'DIM_AIRPORT' in tablas:
        tablas['DIM_AIRPORT'] = fix_airport_data(tablas['DIM_AIRPORT'])
    
    print(tablas["DIM_PASSENGER"].head())
    print(tablas["DIM_DATE"].head())
    print(tablas["DIM_AIRPORT"].head())
    print(tablas["DIM_AIRLINE"])
    print(tablas["FACT_VUELO"].head())
    print("\nTransformación de datos completada.")
    
    # Cargar los datos en la base de datos
    print("\nCargando datos en la base de datos...")
    # Validar si el modelo de datos existe
    if not check_model_exists(cnxn):
        print("Antes debes de crear un nuevo modelo.")
        return

    # Si existe, proceder con la carga
    try:
        load_to_sql_server(tablas, cnxn)
    finally:
        cnxn.close()

def procesar_archivos_especificos():

    print("Procesando archivos de entrada específicos...")

def consultas_analiticas(cnxn):

    print("Ejecutando consultas analíticas predefinidas...")


def main():
    # 1. Intentar obtener la conexión a la base de datos
    cnxn = get_connection()
    if cnxn is None:
        print("ERROR: No se pudo establecer conexión con la base de datos.")
        return  # Si falla, salimos de la aplicación

    # 2. Bucle principal del menú
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            borrar_modelo_existente(cnxn)
        elif opcion == "2":
            crear_modelo_nuevo(cnxn)
        elif opcion == "3":
            extraer_informacion_archivos(cnxn)
        elif opcion == "4":
            procesar_archivos_especificos()
        elif opcion == "5":
            consultas_analiticas(cnxn)
        elif opcion == "6":
            print("Saliendo de la aplicación...")
            break
        else:
            print("Opción inválida. Intente de nuevo.")

    # 3. Cerrar la conexión antes de salir
    cnxn.close()

if __name__ == "__main__":
    main()
