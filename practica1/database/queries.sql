-- SELECT COUNT (*) de todas las tablas para ver que si realizo la carga en las tablas del modelo.
SELECT 'DIM_PASSENGER' AS Tabla, COUNT(*) AS TotalRegistros FROM DIM_PASSENGER
UNION ALL
SELECT 'DIM_DATE', COUNT(*) FROM DIM_DATE
UNION ALL
SELECT 'DIM_AIRPORT', COUNT(*) FROM DIM_AIRPORT
UNION ALL
SELECT 'DIM_AIRLINE', COUNT(*) FROM DIM_AIRLINE
UNION ALL
SELECT 'FACT_VUELO', COUNT(*) FROM FACT_VUELO;

-- Porcentaje de pasajeros por género. 
SELECT 
    Género,
    COUNT(*) AS TotalPasajeros,
    COUNT(*) * 100.0 / (SELECT COUNT(*) FROM DIM_PASSENGER) AS Porcentaje
FROM DIM_PASSENGER
GROUP BY Género;

-- Nacionalidades con su mes año de mayor fecha de salida.
DECLARE @colsPivot   NVARCHAR(MAX) = '';
DECLARE @colsSelect  NVARCHAR(MAX) = '';
DECLARE @colsTotal   NVARCHAR(MAX) = '';
DECLARE @query       NVARCHAR(MAX) = '';

SELECT 
    @colsPivot  = @colsPivot  + ',[' + CONCAT(RIGHT('0' + CAST(d.Mes AS VARCHAR(2)),2), '-', CAST(d.Año AS VARCHAR(4))) + ']',
    @colsSelect = @colsSelect + ',ISNULL([' + CONCAT(RIGHT('0' + CAST(d.Mes AS VARCHAR(2)),2), '-', CAST(d.Año AS VARCHAR(4))) + '], 0) AS [' + CONCAT(RIGHT('0' + CAST(d.Mes AS VARCHAR(2)),2), '-', CAST(d.Año AS VARCHAR(4))) + ']',
    @colsTotal  = @colsTotal  + ' + ISNULL([' + CONCAT(RIGHT('0' + CAST(d.Mes AS VARCHAR(2)),2), '-', CAST(d.Año AS VARCHAR(4))) + '],0)'
FROM DIM_DATE d
JOIN FACT_VUELO f ON d.DateID = f.DateID
GROUP BY d.Año, d.Mes
ORDER BY d.Año, d.Mes;

SET @colsPivot  = STUFF(@colsPivot, 1, 1, '');
SET @colsSelect = STUFF(@colsSelect, 1, 1, '');

SET @colsTotal  = STUFF(@colsTotal, 1, 3, '');

SET @query = N'
SELECT Nacionalidad, ' + @colsSelect + ', (' + @colsTotal + ') AS Total
FROM
(
    SELECT 
        p.Nacionalidad,
        CONCAT(RIGHT(''0'' + CAST(d.Mes AS VARCHAR(2)),2), ''-'', CAST(d.Año AS VARCHAR(4))) AS MesAño,
        1 AS Conteo
    FROM FACT_VUELO f
    INNER JOIN DIM_PASSENGER p ON f.PassengerID = p.PassengerID
    INNER JOIN DIM_DATE d ON f.DateID = d.DateID
) AS SourceTable
PIVOT
(
    SUM(Conteo)
    FOR MesAño IN (' + @colsPivot + ')
) AS pvt
ORDER BY Total DESC;
';

EXEC sp_executesql @query;

-- COUNT de vuelos por país.
SELECT 
    a.País,
    COUNT(*) AS TotalVuelos
FROM FACT_VUELO f
JOIN DIM_AIRPORT a ON f.OrigenAirportID = a.AirportID
GROUP BY a.País
ORDER BY TotalVuelos DESC;

-- Top 5 aeropuertos con mayor número de pasajeros. 
SELECT TOP 5 
    a.Nombre,
    a.País,
    (COALESCE(orig.TotalOrigen, 0) + COALESCE(dest.TotalDestino, 0)) AS TotalPasajeros
FROM DIM_AIRPORT a
LEFT JOIN (
    SELECT OrigenAirportID, COUNT(*) AS TotalOrigen
    FROM FACT_VUELO
    GROUP BY OrigenAirportID
) orig ON a.AirportID = orig.OrigenAirportID
LEFT JOIN (
    SELECT DestinoAirportID, COUNT(*) AS TotalDestino
    FROM FACT_VUELO
    GROUP BY DestinoAirportID
) dest ON a.AirportID = dest.DestinoAirportID
ORDER BY TotalPasajeros DESC;

-- COUNT divido por estado de vuelo.   
SELECT 
    EstadoVuelo,
    COUNT(*) AS TotalVuelos
FROM FACT_VUELO
GROUP BY EstadoVuelo
ORDER BY TotalVuelos DESC;

-- Top 5 de los países más visitados.  
SELECT TOP 5 
    a.País,
    COUNT(*) AS TotalVuelos
FROM FACT_VUELO f
JOIN DIM_AIRPORT a ON f.OrigenAirportID = a.AirportID
GROUP BY a.País
ORDER BY TotalVuelos DESC;

-- Top 5 de los continentes más visitados. 
SELECT TOP 5 
    a.Continente,
    COUNT(*) AS TotalVuelos
FROM FACT_VUELO f
JOIN DIM_AIRPORT a ON f.OrigenAirportID = a.AirportID
GROUP BY a.Continente
ORDER BY TotalVuelos DESC;

-- Top 5 de edades divido por género que más viajan.  
WITH CTE_AgeGender AS (
    SELECT 
        p.Género,
        p.Edad,
        COUNT(*) AS TotalVuelos,
        ROW_NUMBER() OVER (PARTITION BY p.Género ORDER BY COUNT(*) DESC) AS rn
    FROM FACT_VUELO f
    JOIN DIM_PASSENGER p ON f.PassengerID = p.PassengerID
    GROUP BY p.Género, p.Edad
)
SELECT Género, Edad, TotalVuelos
FROM CTE_AgeGender
WHERE rn <= 5
ORDER BY Género, TotalVuelos DESC;

-- COUNT de vuelos por MM-YYYY. 
SELECT 
    CONCAT(RIGHT('0' + CAST(d.Mes AS VARCHAR(2)),2), '-', CAST(d.Año AS VARCHAR(4))) AS [MM-YYYY],
    COUNT(*) AS TotalVuelos
FROM FACT_VUELO f
JOIN DIM_DATE d ON f.DateID = d.DateID
GROUP BY d.Mes, d.Año
ORDER BY d.Año, d.Mes;
