import pandas as pd

def extract_data(csv_path):
    """
    Lee el archivo CSV y devuelve un DataFrame con los datos extraídos.
    
    Parámetros:
        csv_path (str): Ruta al archivo CSV.
    
    Retorna:
        pd.DataFrame: DataFrame con los datos extraídos, o None si ocurre un error.
    """
    try:
        df = pd.read_csv(csv_path)
        print(f"Datos extraídos correctamente. Número de registros: {len(df)}")
        return df
    except Exception as e:
        print("Error extrayendo los datos del CSV:", e)
        return None
