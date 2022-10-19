DROP TABLE IF EXISTS usuario;

CREATE TABLE usuario (
    id INTEGER PRIMARY KEY AUTOINCREMENT ,
    nombre TEXT NOT NULL ,
    direccion TEXT NOT NULL ,
    telefono INTEGER NOT NULL , 
    correo TEXT UNIQUE NOT NULL ,
    clave TEXT NOT NULL ,
    tipo TEXT NOT NULL 

);

