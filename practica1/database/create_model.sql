CREATE TABLE DIM_PASSENGER (
  PassengerID int PRIMARY KEY,
  Género varchar(50),
  Edad int,
  Nacionalidad varchar(50)
);

CREATE TABLE DIM_DATE (
  DateID int PRIMARY KEY,
  Fecha date,
  Mes int,
  Año int
);

CREATE TABLE DIM_AIRPORT (
  AirportID int PRIMARY KEY,
  Código varchar(10),
  Nombre varchar(100),
  Ciudad varchar(50),
  País varchar(50),
  Continente varchar(50)
);

CREATE TABLE DIM_AIRLINE (
  AirlineID int PRIMARY KEY,
  Nombre varchar(100)
);

CREATE TABLE FACT_VUELO (
  FlightID int PRIMARY KEY,
  PassengerID int FOREIGN KEY REFERENCES DIM_PASSENGER(PassengerID),
  DateID int FOREIGN KEY REFERENCES DIM_DATE(DateID),
  OrigenAirportID int FOREIGN KEY REFERENCES DIM_AIRPORT(AirportID),
  DestinoAirportID int FOREIGN KEY REFERENCES DIM_AIRPORT(AirportID),
  AirlineID int FOREIGN KEY REFERENCES DIM_AIRLINE(AirlineID),
  EstadoVuelo varchar(50)
);
