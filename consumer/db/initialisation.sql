-- DROP DATABASE IF EXISTS coord_gps;
-- CREATE DATABASE coord_gps;
-- CREATE EXTENSION IF NOT EXISTS postgis;

\connect coord_gps ekip

DROP TABLE IF EXISTS "coord";
DROP TABLE IF EXISTS "user";

CREATE TABLE "user"(
    nom VARCHAR(20) PRIMARY KEY
);

CREATE TABLE coord (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(20)  NOT NULL,
    longitude FLOAT  NOT NULL,
    latitude FLOAT  NOT NULL,
    date1 TIMESTAMP  NOT NULL,
    CONSTRAINT fk_user FOREIGN KEY (nom) REFERENCES "user"(nom)
);

ALTER TABLE public.coord OWNER TO ekip;
INSERT INTO "user"(nom) VALUES 
('Alice'),
('Bob'),
('Charlie');

INSERT INTO coord (nom, longitude, latitude, date1) VALUES
('Alice', 2.2944, 48.8583, '2024-05-02 14:30:00'),
('Bob', -0.1276, 51.5074, '2024-05-03 10:15:00'),   
('Charlie', 13.4050, 52.5200, '2024-05-04 08:45:00');