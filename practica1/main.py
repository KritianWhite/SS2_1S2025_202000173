from src.database import get_connection

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

    print("Borrando el modelo existente...")


def crear_modelo_nuevo(cnxn):

    print("Creando nuevo modelo de datos...")

def extraer_informacion_archivos():
    
    print("Extrayendo información de los archivos fuentes...")

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
            extraer_informacion_archivos()
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
