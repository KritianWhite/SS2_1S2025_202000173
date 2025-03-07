import pyodbc

def get_connection():
    """
    Retorna la conexión a la base de datos SQL Server.
    Retorna None si la conexión falla.
    """
    try:
        connection_string = (
            "DRIVER={ODBC Driver 18 for SQL Server};"
            "SERVER=DESKTOP-B3TTJH2\\SQLEXPRESS;" 
            "DATABASE=practica_semi2;" 
            "UID=sa;" 
            "PWD=Sseminario2025@;" 
            "Encrypt=no;" 
        )
        cnxn = pyodbc.connect(connection_string)
        return cnxn
    except Exception:
        return None
    
def get_active_connection(cnxn):
    try:
        cnxn.cursor()
        return cnxn  # La conexión está activa
    except pyodbc.ProgrammingError:
        # Reabrir la conexión
        return get_connection()
