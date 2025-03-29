@echo off
setlocal EnableDelayedExpansion

:: Configuración de conexión Supabase
set PGHOST=db.ykafauxqhwgpelazvsjj.supabase.co
set PGPORT=5432
set PGDATABASE=postgres
set PGUSER=postgres
set PGPASSWORD=password
set CSV_FILE=C:\Users\kriti\OneDrive\Documents\GitHub\SS2_1S2025_202000173\ProyectoF1\data\SGFood02.vent
set TABLE_NAME=Ventas_Temp

:: Configuración del archivo de log
set LOG_FILE=%~dp0upload_log_%date:~-4,4%%date:~-7,2%%date:~-10,2%_%time:~0,2%%time:~3,2%%time:~6,2%.log
set LOG_FILE=!LOG_FILE: =0!

:: Crear encabezado del log
echo ============================================ > %LOG_FILE%
echo Inicio de proceso: %date% %time% >> %LOG_FILE%
echo ============================================ >> %LOG_FILE%
echo. >> %LOG_FILE%
echo Configuración: >> %LOG_FILE%
echo Host: %PGHOST% >> %LOG_FILE%
echo Puerto: %PGPORT% >> %LOG_FILE%
echo Base de datos: %PGDATABASE% >> %LOG_FILE%
echo Usuario: %PGUSER% >> %LOG_FILE%
echo Archivo CSV: %CSV_FILE% >> %LOG_FILE%
echo Tabla destino: %TABLE_NAME% >> %LOG_FILE%
echo. >> %LOG_FILE%

:: Verificar si existe el archivo CSV
if not exist "%CSV_FILE%" (
    echo ERROR: El archivo CSV no existe: %CSV_FILE% >> %LOG_FILE%
    echo ERROR: El archivo CSV no existe: %CSV_FILE%
    goto :error
)

:: Comando para cargar CSV
echo Subiendo datos a PostgreSQL en Supabase... >> %LOG_FILE%
echo Iniciando carga: %time% >> %LOG_FILE%
echo Subiendo datos a PostgreSQL en Supabase...

:: Ejecutar comando y capturar salida
psql -h %PGHOST% -p %PGPORT% -d %PGDATABASE% -U %PGUSER% -c "\copy %TABLE_NAME% FROM '%CSV_FILE%' WITH (FORMAT csv, HEADER true, DELIMITER '|');" > %TEMP%\psql_output.txt 2>&1
set RESULT=%ERRORLEVEL%

:: Registrar la salida en el log
type %TEMP%\psql_output.txt >> %LOG_FILE%
echo. >> %LOG_FILE%

:: Verificar resultado
if %RESULT% EQU 0 (
    echo Datos subidos exitosamente: %time% >> %LOG_FILE%
    echo Datos subidos exitosamente.
) else (
    echo ERROR: La carga falló con código %RESULT%: %time% >> %LOG_FILE%
    echo ERROR: La carga falló. Revisa el log para más detalles: %LOG_FILE%
    goto :error
)

goto :end

:error
echo ============================================ >> %LOG_FILE%
echo Proceso terminado con errores: %date% %time% >> %LOG_FILE%
echo ============================================ >> %LOG_FILE%
exit /b 1

:end
echo ============================================ >> %LOG_FILE%
echo Proceso completado: %date% %time% >> %LOG_FILE%
echo ============================================ >> %LOG_FILE%
echo Log guardado en: %LOG_FILE%
endlocal
exit /b 0