CREATE TABLE IF NOT EXISTS usuarios (
	dni VARCHAR(8) PRIMARY KEY,
	nombre VARCHAR(255) NOT NULL,
	saldo FLOAT,
);

CREATE TABLE IF NOT EXISTS cuentas (
    numero_cuenta VARCHAR(20) PRIMARY KEY,
    dni_usuario VARCHAR(8) NOT NULL,
    saldo FLOAT,
    
    FOREIGN KEY (dni_usuario) REFERENCES usuarios(dni) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS tarjetas (
    numero_tarjeta VARCHAR(16) PRIMARY KEY,
    numero_cuenta VARCHAR(20) NOT NULL,
    pin_hash VARCHAR(255) NOT NULL,
    intentos_fallidos INT DEFAULT 0,
    bloqueada BOOLEAN DEFAULT FALSE,
    
    FOREIGN KEY (numero_cuenta) REFERENCES cuentas(numero_cuenta) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS cajeros (
    id_cajero VARCHAR(10) PRIMARY KEY,
    ubicacion VARCHAR(100) NOT NULL,
    efectivo_disponible FLOAT NOT NULL

CREATE TABLE IF NOT EXISTS transacciones (
    numero_transaccion VARCHAR(10) PRIMARY KEY,
    numero_cuenta VARCHAR(20) NOT NULL,
    id_cajero VARCHAR(10) NOT NULL,
    tipo_operacion VARCHAR(20) NOT NULL,
    monto FLOAT NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (numero_cuenta) REFERENCES cuentas(numero_cuenta) ON DELETE CASCADE,
    FOREIGN KEY (id_cajero) REFERENCES cajeros(id_cajero) ON DELETE RESTRICT
);