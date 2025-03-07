import sys

from src.database import get_connection, get_active_connection
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
    cnxn = get_active_connection(cnxn)
    print("Ejecutando consultas analíticas predefinidas...\n")
    
    query_file = "practica1/database/queries.sql"
    
    try:
        with open(query_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as e:
        print("Error al leer el archivo de queries:", e)
        return

    # Separamos el archivo en bloques: título (comentario) y consulta
    queries = []
    current_title = None
    current_query = ""
    for line in lines:
        # Si la línea es un comentario que inicia con '--'
        if line.strip().startswith("--"):
            # Si ya habíamos acumulado una consulta, la guardamos junto a su título (comentario)
            if current_query.strip():
                queries.append((current_title, current_query.strip()))
                current_query = ""
            # Guardamos el título (comentario) (removiendo el '--')
            current_title = line.strip()[2:].strip()
        else:
            # Acumular las líneas de la consulta
            current_query += line

    # Agregar la última consulta si existe
    if current_query.strip():
        queries.append((current_title, current_query.strip()))
    
    cursor = cnxn.cursor()
    
    # Recorrer cada query, mostrar título y ejecutar la consulta
    for title, query in queries:
        print("\n" + title)
        print("-" * len(title))
        try:
            cursor.execute(query)
            
            # En el caso de queries que retornen resultados
            try:
                rows = cursor.fetchall()
                if rows:
                    # Muestra los resultados
                    for row in rows:
                        print(row)
                else:
                    print("La consulta se ejecutó correctamente, pero no devolvió resultados.")
            except Exception:
                # En queries que no retornan resultado (como las de DML o de ejecución dinámica)
                print("La consulta se ejecutó correctamente.\n")
        except Exception as e:
            print("Error en la consulta:", e)
    
    cnxn.commit()

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
