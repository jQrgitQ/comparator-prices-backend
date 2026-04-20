-- PostgreSQL

-- Tabla de roles
CREATE TABLE IF NOT EXISTS roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR UNIQUE NOT NULL
);

-- Insertar roles (si no existen)
INSERT INTO roles (name) VALUES ('user')
ON CONFLICT (name) DO NOTHING;

INSERT INTO roles (name) VALUES ('admin')
ON CONFLICT (name) DO NOTHING;

-- Tabla de usuarios
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    hashed_password VARCHAR NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    full_name VARCHAR,
    role_id INTEGER REFERENCES roles(id) DEFAULT 1
);

-- Insertar usuario admin (usuario: admin, password: admin)
-- Hash bcrypt de 'admin': $2b$12$fROC3WdG6qPzgCk4Cr2b9Oq5c5Ihzx1MAtArUZqIhGNBaDKp3vUiC
INSERT INTO users (email, hashed_password, is_active, full_name, role_id)
VALUES (
    'admin',
    '$2b$12$fROC3WdG6qPzgCk4Cr2b9Oq5c5Ihzx1MAtArUZqIhGNBaDKp3vUiC',
    TRUE,
    'Administrator',
    (SELECT id FROM roles WHERE name = 'admin')
);