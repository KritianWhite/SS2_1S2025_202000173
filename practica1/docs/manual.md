# PRACTICA 1 | SEMINARIO DE SISTEMAS 2
## Christian Alessander Blanco González
## 202000173


# DESCRIPCIÓN BASE DE DATOS
## Create_model.sql
Este script SQL crea la estructura de una base de datos orientada a un modelo dimensional. Se definen cuatro tablas de dimensión y una tabla de hechos:

- DIM_PASSENGER: Almacena información de los pasajeros (ID, género, edad y nacionalidad).
- DIM_DATE: Registra detalles de fechas (ID, fecha, mes y año).
- DIM_AIRPORT: Contiene información sobre aeropuertos (ID, código, nombre, ciudad, país y continente).
- DIM_AIRLINE: Guarda el nombre de las aerolíneas (ID y nombre).

La tabla FACT_VUELO es la tabla de hechos que relaciona los datos de las dimensiones mediante claves foráneas, vinculando un vuelo con un pasajero, una fecha, un aeropuerto de origen y destino, y una aerolínea, además de almacenar el estado del vuelo.

## Drop_model.sql
Este script elimina la estructura de la base de datos en el orden correcto para evitar problemas de integridad referencial. Primero se borra la tabla de hechos (FACT_VUELO) y luego se eliminan las tablas de dimensiones (DIM_AIRLINE, DIM_AIRPORT, DIM_DATE y DIM_PASSENGER) utilizando la cláusula IF EXISTS para evitar errores en caso de que alguna tabla no exista.

## Queries.sql
Contiene múltiples consultas que extraen y agregan información del modelo dimensional. A continuación, se presenta un resumen breve de cada bloque de consulta:

1. **Conteo de registros en las tablas:**  
   La primera consulta utiliza UNION ALL para mostrar el número total de registros en cada tabla (dimensiones y hechos). Esto permite verificar que la carga de datos se haya realizado correctamente.

2. **Porcentaje de pasajeros por género:**  
   Agrupa los datos de la tabla de pasajeros por género, contando cuántos hay de cada uno y calculando el porcentaje que representa respecto al total de pasajeros.

3. **Nacionalidades con su mes-año de mayor fecha de salida (Pivot Dinámico):**  
   Se construye una consulta dinámica que pivota la información de fechas. Para cada nacionalidad, se muestra el conteo de vuelos agrupados por una columna dinámica que combina mes y año. La consulta utiliza variables para construir la lista de columnas del pivot y luego ejecuta la consulta dinámica para obtener una tabla que muestra, por cada nacionalidad, el total de vuelos por mes-año, junto con un total acumulado.

4. **Conteo de vuelos por país:**  
   Se agrupan los vuelos según el país de origen de los aeropuertos, mostrando cuántos vuelos se han realizado desde cada país y ordenándolos de mayor a menor.

5. **Top 5 aeropuertos con mayor número de pasajeros:**  
   Se calcula el total de pasajeros para cada aeropuerto sumando los vuelos de origen y destino. La consulta muestra los cinco aeropuertos con mayor cantidad de pasajeros, incluyendo el nombre y el país del aeropuerto.

6. **Conteo de vuelos por estado de vuelo:**  
   Se agrupa la tabla de hechos según el estado de cada vuelo, proporcionando un conteo de vuelos por cada estado (por ejemplo, "en tiempo", "retrasado", etc.) y ordenando el resultado de mayor a menor.

7. **Top 5 de los países más visitados:**  
   Se cuentan los vuelos agrupados por el país de origen de los aeropuertos y se seleccionan los cinco países con mayor número de vuelos, lo que indica los destinos más populares.

8. **Top 5 de los continentes más visitados:**  
   Similar a la consulta anterior, pero agrupando por continente en lugar de por país para identificar cuáles son los continentes que reciben mayor cantidad de vuelos.

9. **Top 5 de edades divididas por género que más viajan:**  
   Utilizando una CTE (Common Table Expression), la consulta agrupa los datos de pasajeros por género y edad, contando cuántos vuelos han tomado. Se asigna un número de fila para cada grupo y se seleccionan los cinco primeros para cada género, mostrando así las edades con mayor volumen de vuelos.

10. **Conteo de vuelos por mes-año (MM-YYYY):**  
    Agrupa los vuelos en función de una columna que combina mes y año, derivada de la tabla de fechas, y cuenta el total de vuelos para cada período, ordenando los resultados cronológicamente.

# DESCRIPCIÓN ETL
## extract.py
Tiene una función que se encarga de leer el archivo CSV y extraer sus datos en un DataFrame de Pandas.

- **Función extract_data:**  
  - Entrada: Recibe como parámetro la ruta del archivo CSV (csv_path).  
  - Proceso:  
    - Utiliza pd.read_csv para leer el archivo y cargar sus datos en un DataFrame.  
    - Imprime un mensaje con la cantidad de registros extraídos, lo que ayuda a confirmar que la lectura fue exitosa.  
  - Manejo de errores:  
    - Si ocurre algún error durante la lectura (por ejemplo, si la ruta es incorrecta o el archivo está dañado), se captura la excepción y se imprime un mensaje de error.  
  - Salida: Devuelve el DataFrame con los datos extraídos. Si ocurre algún error, retorna None.

## transform.py
Se encarga de transformar y limpiar el dataset de vuelos para generar las tablas del modelo dimensional.

1. **Limpieza general:**  
   - Elimina espacios en blanco en los nombres de columnas y en los valores de columnas tipo texto.  
   - Convierte la columna de edad a formato numérico y elimina filas con valores inválidos.  
   - Estandariza los valores de la columna de género (por ejemplo, "male" se transforma en "Male").

2. **Creación de la tabla DIM_PASSENGER:**  
   - Genera un mapeo que asigna a cada pasajero un identificador numérico secuencial a partir de su "Passenger ID" original.  
   - Crea la tabla con los campos: PassengerID, Género, Edad y Nacionalidad, eliminando duplicados.

3. **Creación de la tabla DIM_DATE:**  
   - Define una función para parsear la fecha de salida considerando distintos formatos.  
   - Aplica la función a la columna "Departure Date" y elimina las filas donde la fecha no pudo ser interpretada.  
   - Estandariza el formato de la fecha y extrae el mes y el año para construir la tabla, asignándole un identificador único (DateID).

4. **Creación de la tabla DIM_AIRPORT:**  
   - Separa la información de aeropuertos de origen (con datos completos) y destino (solo con el código).  
   - Combina ambas fuentes y elimina duplicados basándose en el código del aeropuerto, asignando un identificador único (AirportID).

5. **Creación de la tabla DIM_AIRLINE:**  
   - Dado que no existe una columna específica de aerolínea en el dataset, se crea una tabla con un valor por defecto ("Desconocido").

6. **Creación de la tabla FACT_VUELO:**  
   - Mapea los identificadores de pasajero y une la información de fecha (para obtener DateID) y aeropuertos (para obtener Origen y Destino AirportID) mediante joins.  
   - Asigna un AirlineID por defecto y genera un FlightID secuencial para cada registro.  
   - Finalmente, selecciona y renombra las columnas pertinentes para formar la tabla de hechos.

## load.py
Encargado de cargar los datos transformados en una base de datos SQL Server y de realizar algunas validaciones y correcciones previas.

1. **Verificación de la existencia del modelo:**  
   - La función check_model_exists consulta en el INFORMATION_SCHEMA.TABLES para determinar si la tabla DIM_PASSENGER ya existe. Esto ayuda a confirmar si el modelo dimensional ha sido creado previamente.

2. **Carga de datos a SQL Server (load_to_sql_server):**  
   - Orden de carga: Define el orden de inserción de las tablas para respetar las relaciones de claves foráneas (dimensiones primero y luego la tabla de hechos).  
   - Validación y conversión de tipos: Para cada tabla, se obtienen los metadatos de columnas y se realizan conversiones necesarias (por ejemplo, reemplazo de valores NaN por None, conversión de tipos numéricos y manejo de valores nulos en campos de texto).  
   - Inserción por lotes: Se limpia la tabla existente en SQL Server (mediante DELETE) y se insertan los nuevos registros en lotes, haciendo commits cada 1000 filas para evitar transacciones muy grandes.  
   - Manejo de errores: Se captura cualquier error en la inserción de filas individuales sin detener el proceso completo y se utiliza rollback en caso de errores críticos.

3. **Corrección de datos en la tabla DIM_AIRPORT (`ix_airport_data):**  
   - Esta función específica asegura de que los campos de texto no tengan valores nulos, rellenándolos con cadenas vacías, y trunca el código del aeropuerto si excede la longitud máxima permitida (normalmente 10 caracteres).

# PRINCIPAL
## main.py
Orquesta el flujo principal de la aplicación, integrando los procesos de extracción, transformación y carga, además de ejecutar consultas analíticas.

1. **Menú Principal:**  
   La función mostrar_menu despliega un menú con las opciones disponibles para el usuario, permitiendo elegir entre borrar el modelo existente, crear uno nuevo, extraer y procesar archivos, ejecutar consultas analíticas o salir de la aplicación.

2. **Borrado y Creación del Modelo de Datos:**  
   - borrar_modelo_existente: Lee y ejecuta el script SQL (drop_model.sql) para eliminar las tablas del modelo de datos, respetando el orden adecuado para evitar conflictos con claves foráneas.  
   - crear_modelo_nuevo: Lee y ejecuta el script SQL (create_model.sql) que crea la estructura del modelo dimensional.

3. **Extracción, Transformación y Carga (ETL):**  
   - extraer_informacion_archivos:  
     - Extrae los datos desde un archivo CSV utilizando la función extract_data.  
     - Aplica la función transform_and_clean_data para limpiar y transformar los datos, generando las tablas del modelo dimensional.  
     - Realiza ajustes adicionales en la tabla DIM_AIRPORT mediante fix_airport_data.  
     - Finalmente, valida la existencia del modelo en la base de datos y, si está creado, carga los datos transformados con la función load_to_sql_server.

4. **Procesamiento de Archivos Específicos:**  
   - La función procesar_archivos_especificos es un espacio reservado para implementar futuros procesos de archivos particulares.

5. **Consultas Analíticas Predefinidas:**  
   - consultas_analiticas:  
     - Lee el archivo queries.sql, separa cada consulta junto con su título (comentario) y las ejecuta en la base de datos.  
     - Imprime los resultados o notifica si la consulta se ejecutó sin devolver datos.

6. **Función Principal (main):**  
   - Establece la conexión a la base de datos utilizando get_connection.  
   - Ejecuta un bucle que muestra el menú y procesa la opción seleccionada por el usuario.  
   - Al final, se cierra la conexión a la base de datos.

## database.py
Se encarga de establecer y gestionar la conexión con la base de datos SQL Server.

1. **Función get_connection:**  
   - Construye una cadena de conexión utilizando parámetros como el driver ODBC, el servidor, la base de datos, usuario y contraseña.  
   - Intenta establecer la conexión con SQL Server mediante pyodbc.connect.  
   - Retorna la conexión establecida o None si ocurre algún error durante el proceso.

2. **Función get_active_connection:**  
   - Verifica si la conexión pasada como parámetro está activa intentando obtener un cursor.  
   - Si la conexión no es válida (por ejemplo, ya fue cerrada o está inactiva), intenta reabrirla llamando a get_connection.  
   - Retorna la conexión activa, ya sea la original o una nueva en caso de haber sido necesario.
