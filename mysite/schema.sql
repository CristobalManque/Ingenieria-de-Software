--DROP TABLE IF EXISTS producto;
--DROP TABLE IF EXISTS usuario;
DROP TABLE IF EXISTS OCcliente;
DROP TABLE IF EXISTS OCproveedor;

CREATE TABLE IF NOT EXISTS usuario(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nombre TEXT NOT NULL,
  direccion TEXT NOT NULL,
  telefono INTEGER NOT NULL,
  correo TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  tipo TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS producto(
  sku INTEGER PRIMARY KEY UNIQUE NOT NULL,
  nombre TEXT NOT NULL,
  fechaentrega TEXT NOT NULL,
  cantidad INTEGER NOT NULL,
  precioU INTEGER NOT NULL
);

CREATE TABLE OCcliente(
  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  producto VARCHAR(50) NOT NULL,
  fecha DATETIME NOT NULL,
  tmoneda VARCHAR(3) NOT NULL,
  moneda INTEGER,
  lugar TEXT NOT NULL,
  tpago TEXT NOT NULL
);

CREATE TABLE OCproveedor(
  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  cliente INTEGER NOT NULL,
  fecha DATETIME NOT NULL,
  tmoneda VARCHAR(3) NOT NULL,
  moneda INTEGER,
  lugar TEXT NOT NULL,
  tpago TEXT NOT NULL
);