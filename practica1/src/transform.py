import pandas as pd
from datetime import datetime

def transform_and_clean_data(df):
    """
    Transforma y limpia el dataset de vuelos generando las siguientes tablas:
      - DIM_PASSENGER
      - DIM_DATE
      - DIM_AIRPORT
      - DIM_AIRLINE
      - FACT_VUELO

    Parámetros:
      df (pd.DataFrame): DataFrame con los datos extraídos.

    Retorna:
      dict: Diccionario con cada DataFrame resultante limpio y transformado.
    """
    # ---- Limpieza General ----
    # Eliminar espacios en blanco en nombres de columnas
    df.columns = df.columns.str.strip()
    
    # Eliminar espacios en blanco en todas las columnas de tipo string
    text_columns = df.select_dtypes(include=['object']).columns
    for col in text_columns:
        df[col] = df[col].str.strip()
    
    # Convertir la columna 'Age' a numérico y eliminar filas con valores inválidos
    df['Age'] = pd.to_numeric(df['Age'], errors='coerce')
    df = df[df['Age'].notnull()]
    
    # Estandarizar valores de género (por ejemplo, 'male' -> 'Male', 'female' -> 'Female')
    df['Gender'] = df['Gender'].str.capitalize()
    
    # ---- DIM_PASSENGER ----
    # Crear mapeo de Passenger ID (alfanumérico) a un ID numérico secuencial
    unique_passengers = df['Passenger ID'].unique()
    passenger_map = {orig_id: idx+1 for idx, orig_id in enumerate(unique_passengers)}
    
    dim_passenger = pd.DataFrame({
        "PassengerID": df['Passenger ID'].map(passenger_map),
        "Género": df['Gender'],
        "Edad": df['Age'],
        "Nacionalidad": df['Nationality']
    }).drop_duplicates(subset=["PassengerID"]).reset_index(drop=True)
    
    # ---- DIM_DATE ----
    # Función para parsear fechas considerando varios formatos
    def parse_date(date_str):
        for fmt in ("%m/%d/%Y", "%m-%d-%Y", "%d/%m/%Y", "%d-%m-%Y"):
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        return None

    # Parsear la columna 'Departure Date'
    df['ParsedDate'] = df['Departure Date'].apply(parse_date)
    # Eliminar filas donde la fecha no pudo ser interpretada
    df = df[df['ParsedDate'].notnull()]
    
    # Estandarizar el formato de la fecha y extraer mes y año
    df['Fecha_formateada'] = df['ParsedDate'].dt.strftime("%Y-%m-%d")
    df['Mes'] = df['ParsedDate'].dt.month
    df['Año'] = df['ParsedDate'].dt.year

    # Crear la tabla DIM_DATE única
    dim_date = df[['Fecha_formateada', 'Mes', 'Año']].drop_duplicates().reset_index(drop=True)
    dim_date.insert(0, 'DateID', dim_date.index + 1)
    dim_date.rename(columns={'Fecha_formateada': 'Fecha'}, inplace=True)
    
    # ---- DIM_AIRPORT ----
    # Aeropuertos de origen (información más completa)
    orig_airports = df[['Airport Name', 'Airport Country Code', 'Country Name', 'Airport Continent']].copy()
    orig_airports.rename(columns={
        "Airport Name": "Nombre",
        "Airport Country Code": "Código",
        "Country Name": "País",
        "Airport Continent": "Continente"
    }, inplace=True)
    
    # Aeropuertos destino (solo se cuenta con el código)
    dest_airports = df[['Arrival Airport']].copy()
    dest_airports = dest_airports.rename(columns={'Arrival Airport': 'Código'})
    dest_airports['Nombre'] = None
    dest_airports['Ciudad'] = None
    dest_airports['País'] = None
    dest_airports['Continente'] = None
    
    # Combinar ambos y eliminar duplicados basados en el código
    dim_airport = pd.concat([orig_airports, dest_airports], ignore_index=True)
    dim_airport = dim_airport.drop_duplicates(subset=['Código']).reset_index(drop=True)
    dim_airport.insert(0, 'AirportID', dim_airport.index + 1)
    
    # ---- DIM_AIRLINE ----
    # No existe columna de aerolínea, se asigna valor por defecto
    dim_airline = pd.DataFrame({
        "AirlineID": [1],
        "Nombre": ["Desconocido"]
    })
    
    # ---- FACT_VUELO ----
    fact = df.copy()
    # Mapear PassengerID
    fact['PassengerID'] = fact['Passenger ID'].map(passenger_map)
    
    # Unir con DIM_DATE para obtener DateID
    fact = fact.merge(dim_date, left_on=['Fecha_formateada', 'Mes', 'Año'],
                      right_on=['Fecha', 'Mes', 'Año'], how='left')
    
    # Mapear OrigenAirportID usando "Airport Country Code"
    fact = fact.merge(dim_airport[['AirportID', 'Código']], 
                      left_on='Airport Country Code', right_on='Código', 
                      how='left', suffixes=('', '_origen'))
    fact.rename(columns={'AirportID': 'OrigenAirportID'}, inplace=True)
    
    # Mapear DestinoAirportID usando "Arrival Airport"
    fact = fact.merge(dim_airport[['AirportID', 'Código']], 
                      left_on='Arrival Airport', right_on='Código', 
                      how='left', suffixes=('', '_destino'))
    fact.rename(columns={'AirportID': 'DestinoAirportID'}, inplace=True)
    
    # Asignar AirlineID (valor por defecto)
    fact['AirlineID'] = 1
    # Generar FlightID secuencial
    fact['FlightID'] = range(1, len(fact) + 1)
    
    fact_vuelo = fact[['FlightID', 'PassengerID', 'DateID', 'OrigenAirportID', 
                         'DestinoAirportID', 'AirlineID', 'Flight Status']].copy()
    fact_vuelo.rename(columns={'Flight Status': 'EstadoVuelo'}, inplace=True)
    
    return {
        "DIM_PASSENGER": dim_passenger,
        "DIM_DATE": dim_date,
        "DIM_AIRPORT": dim_airport,
        "DIM_AIRLINE": dim_airline,
        "FACT_VUELO": fact_vuelo
    }
    
# Ejemplo de uso:
# tablas = transform_and_clean_data("practica1/data/VuelosDataSet.csv")
# print(tablas["DIM_PASSENGER"].head())
# print(tablas["DIM_DATE"].head())
# print(tablas["DIM_AIRPORT"].head())
# print(tablas["DIM_AIRLINE"])
# print(tablas["FACT_VUELO"].head())
