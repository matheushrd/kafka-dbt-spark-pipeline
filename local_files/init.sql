-- Criar o schema usuario
CREATE SCHEMA IF NOT EXISTS usuario;

-- Tabela usuario
CREATE TABLE IF NOT EXISTS usuario.usuario (
    id VARCHAR(255) PRIMARY KEY,
    nome VARCHAR(255),
    sobrenome VARCHAR(255),
    idade INT,
    telefone VARCHAR(255),
    email VARCHAR(255),
    created_at TIMESTAMP(6),
    updated_at TIMESTAMP(6)
);

-- Tabela endereco
CREATE TABLE IF NOT EXISTS usuario.endereco (
    id VARCHAR(255) PRIMARY KEY,
    usuario_id VARCHAR(255) REFERENCES usuario.usuario(id),
    rua_logradouro VARCHAR(255),
    numero INT,
    cidade VARCHAR(255),
    estado VARCHAR(255),
    pais VARCHAR(255),
    created_at TIMESTAMP(6),
    updated_at TIMESTAMP(6)
);

-- Criar o schema compras
CREATE SCHEMA IF NOT EXISTS compras;

-- Tabela compras
CREATE TABLE IF NOT EXISTS compras.compras (
    id VARCHAR(255) PRIMARY KEY,
    usuario_id VARCHAR(255) REFERENCES usuario.usuario(id),
    valor VARCHAR(255),
    metodo_pagamento VARCHAR(255),
    status_pedido VARCHAR(255),
    status_pagamento VARCHAR(255),
    expira_em TIMESTAMP,
    created_at TIMESTAMP(6),
    updated_at TIMESTAMP(6)
);

-- Tabela pagamento
CREATE TABLE IF NOT EXISTS compras.pagamento (
    id VARCHAR(255) PRIMARY KEY,
    compra_id VARCHAR(255) REFERENCES compras.compras(id),
    status VARCHAR(255) CHECK (status IN ('Pago', 'Rejeitado', 'Expirado'))
);

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- scripts/setup_replication.sql

-- Habilite a replicação lógica
ALTER SYSTEM SET wal_level = 'logical';
ALTER SYSTEM set max_wal_senders = 10;
ALTER SYSTEM set max_replication_slots = 10;

-- Reinicie o PostgreSQL para aplicar a configuração
SELECT pg_reload_conf();

-- Crie uma publicação para o esquema "usuario" e "compras"
CREATE PUBLICATION usuario_publication FOR TABLE usuario.usuario, usuario.endereco;
CREATE PUBLICATION compras_publication FOR TABLE compras.compras, compras.pagamento;

-- Crie um slot de replicação para os esquemas (substitua pelos seus valores)
SELECT * FROM pg_create_logical_replication_slot('usuario_slot', 'wal2json');
SELECT * FROM pg_create_logical_replication_slot('compras_slot', 'wal2json');

SELECT pg_reload_conf();

-- Insert 1
INSERT INTO usuario.usuario (id, nome, sobrenome, idade, telefone, email, created_at, updated_at) 
VALUES ('1', 'John', 'Doe', 30, '+123456789', 'john.doe@email.com', NOW(), NOW());

INSERT INTO usuario.usuario (id, nome, sobrenome, idade, telefone, email, created_at, updated_at) 
VALUES ('2', 'Jane', 'Smith', 25, '+987654321', 'jane.smith@email.com', NOW(), NOW());

INSERT INTO usuario.usuario (id, nome, sobrenome, idade, telefone, email, created_at, updated_at) 
VALUES ('3', 'Alice', 'Johnson', 22, '+1122334455', 'alice.johnson@email.com', NOW(), NOW());

INSERT INTO usuario.usuario (id, nome, sobrenome, idade, telefone, email, created_at, updated_at) 
VALUES ('4', 'Bob', 'Anderson', 35, '+9988776655', 'bob.anderson@email.com', NOW(), NOW());

INSERT INTO usuario.usuario (id, nome, sobrenome, idade, telefone, email, created_at, updated_at) 
VALUES ('5', 'Eva', 'Miller', 28, '+5544332211', 'eva.miller@email.com', NOW(), NOW());

INSERT INTO usuario.usuario (id, nome, sobrenome, idade, telefone, email, created_at, updated_at) 
VALUES ('6', 'Michael', 'Brown', 40, '+1122334455', 'michael.brown@email.com', NOW(), NOW());

INSERT INTO usuario.usuario (id, nome, sobrenome, idade, telefone, email, created_at, updated_at) 
VALUES ('7', 'Sophia', 'Taylor', 32, '+9988776655', 'sophia.taylor@email.com', NOW(), NOW());

INSERT INTO usuario.usuario (id, nome, sobrenome, idade, telefone, email, created_at, updated_at) 
VALUES ('8', 'William', 'Johnson', 27, '+5544332211', 'william.johnson@email.com', NOW(), NOW());

INSERT INTO usuario.usuario (id, nome, sobrenome, idade, telefone, email, created_at, updated_at) 
VALUES ('9', 'Olivia', 'Martinez', 33, '+123456789', 'olivia.martinez@email.com', NOW(), NOW());

INSERT INTO usuario.usuario (id, nome, sobrenome, idade, telefone, email, created_at, updated_at) 
VALUES ('10', 'Liam', 'Williams', 29, '+987654321', 'liam.williams@email.com', NOW(), NOW());
