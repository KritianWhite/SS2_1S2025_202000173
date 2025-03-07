import pandas as pd
import numpy as np

def check_model_exists(cnxn):
    """
    Verificar si el modelo de datos existe. Se comprueba la existencia de la tabla DIM_PASSENGER.
    Retornar True si existe, False de lo contrario.
    """
    try:
        cursor = cnxn.cursor()
        cursor.execute("SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'DIM_PASSENGER'")
        result = cursor.fetchone()
        return result is not None
    except Exception as e:
        print("Error verificando la existencia del modelo de datos:", e)
        return False

def load_to_sql_server(transformed_data, connection):
    """
    Cargar los DataFrames transformados a SQL Server usando una conexión existente.
    Incluye validación y conversión de tipos de datos.
    
    Parámetros:
        transformed_data (dict): Diccionario con los DataFrames resultantes del proceso de transformación.
        connection: Conexión a SQL Server obtenida mediante pyodbc.
        
    Retorna:
        bool: True si la carga fue exitosa, False en caso contrario.
    """
    try:
        # Definir el orden de carga para respetar las restricciones de clave foránea
        load_order = [
            "DIM_PASSENGER",
            "DIM_DATE", 
            "DIM_AIRPORT", 
            "DIM_AIRLINE", 
            "FACT_VUELO"
        ]
        
        cursor = connection.cursor()
        
        # Para cada tabla, limpiar datos existentes e insertar nuevos
        for table_name in load_order:
            if table_name in transformed_data:
                df = transformed_data[table_name].copy()
                
                # Obtener información sobre las columnas de la tabla en SQL Server
                cursor.execute(f"SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}'")
                columns_info = {row.COLUMN_NAME: row.DATA_TYPE for row in cursor.fetchall()}
                
                # Verificar y limpiar tipos de datos
                for col in df.columns:
                    if col in columns_info:
                        # Reemplazar NaN por None para que SQL Server los interprete como NULL
                        df[col] = df[col].replace({np.nan: None})
                        
                        # Manejar valores nulos en columnas de texto
                        if columns_info[col] in ('varchar', 'nvarchar', 'char', 'nchar', 'text'):
                            df[col] = df[col].astype(object).where(pd.notnull(df[col]), None)
                            # Reemplazar cadenas vacías por None
                            df[col] = df[col].replace('', None)
                        
                        # Convertir explícitamente a float para columnas numéricas
                        elif columns_info[col] in ('float', 'real'):
                            # Convertir a float pero preservar None
                            def safe_float(x):
                                if x is None or pd.isna(x):
                                    return None
                                try:
                                    return float(x)
                                except (ValueError, TypeError):
                                    return None
                            
                            df[col] = df[col].apply(safe_float)
                        
                        # Convertir explícitamente a int para columnas enteras
                        elif columns_info[col] in ('int', 'bigint', 'smallint', 'tinyint'):
                            # Convertir a int pero preservar None
                            def safe_int(x):
                                if x is None or pd.isna(x):
                                    return None
                                try:
                                    return int(float(x))
                                except (ValueError, TypeError):
                                    return None
                            
                            df[col] = df[col].apply(safe_int)
                
                # Limpiar tabla existente
                cursor.execute(f"DELETE FROM {table_name}")
                connection.commit()
                
                # Preparar la inserción por lotes
                count = 0
                for _, row in df.iterrows():
                    try:
                        # Construir consulta de inserción dinámica basada en las columnas del DataFrame
                        columns = ', '.join(df.columns)
                        placeholders = ', '.join(['?' for _ in range(len(df.columns))])
                        
                        insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
                        
                        # Convertir los valores del DataFrame a una tupla para la inserción
                        values = tuple(row)
                        
                        cursor.execute(insert_query, values)
                        count += 1
                        
                        # Hacer commit cada 1000 registros para evitar transacciones muy grandes
                        if count % 1000 == 0:
                            connection.commit()
                            print(f"Cargados {count} registros en {table_name}...")
                    
                    except Exception as row_error:
                        print(f"Error al insertar fila en {table_name}: {str(row_error)}")
                        print(f"Valores problemáticos: {values}")
                        # No detenemos todo el proceso por un error en una fila
                        continue
                
                # Commit final para los registros restantes
                connection.commit()
                print(f"Tabla {table_name} cargada exitosamente con {count} registros.")
            else:
                print(f"Advertencia: Tabla {table_name} no encontrada en los datos transformados.")
        
        print("Proceso de carga completado exitosamente.")
        return True
        
    except Exception as e:
        # En caso de error, hacer rollback para mantener la integridad de la base de datos
        connection.rollback()
        print(f"Error durante la carga de datos: {str(e)}")
        return False
    finally:
        # No cerramos la conexión aquí porque fue proporcionada externamente
        if 'cursor' in locals() and cursor:
            cursor.close()


def fix_airport_data(df_airport):
    """
    Función específica para corregir problemas comunes en la tabla DIM_AIRPORT.
    
    Parámetros:
        df_airport (pandas.DataFrame): DataFrame de DIM_AIRPORT
        
    Retorna:
        pandas.DataFrame: DataFrame con datos corregidos
    """
    df = df_airport.copy()
    
    # Asegurarse de que los campos de texto no sean NaN
    text_columns = ['Código', 'Nombre', 'Ciudad', 'País', 'Continente']
    for col in text_columns:
        if col in df.columns:
            df[col] = df[col].fillna('')
    
    # Truncar el Código si excede la longitud máxima (normalmente 10 caracteres)
    if 'Código' in df.columns:
        df['Código'] = df['Código'].astype(str).str.slice(0, 10)
    
    return df
