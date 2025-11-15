-- Script para eliminar y crear las tablas

CREATE DATABASE IF NOT EXISTS dned;
USE dned;

-- Eliminar las tablas si existen

DROP TABLE IF EXISTS user_workspace_associate;
DROP TABLE IF EXISTS user_unit_associate;
DROP TABLE IF EXISTS unit_school_associate;
DROP TABLE IF EXISTS school_headquarters_associate;
DROP TABLE IF EXISTS type_user_association;
DROP TABLE IF EXISTS email_sender_unit;
DROP TABLE IF EXISTS email_sender_school;
DROP TABLE IF EXISTS email_sender_headquarters;
DROP TABLE IF EXISTS token;
DROP TABLE IF EXISTS system_user;
DROP TABLE IF EXISTS user_workspace;
DROP TABLE IF EXISTS unit_unal;
DROP TABLE IF EXISTS school;
DROP TABLE IF EXISTS headquarters;
DROP TABLE IF EXISTS type_user;
DROP TABLE IF EXISTS email_sender;
DROP TABLE IF EXISTS user_unal;
DROP TABLE IF EXISTS period;

-- Ahora creamos nuevamente las tablas

-- Tabla: period
CREATE TABLE IF NOT EXISTS period (
    cod_period        VARCHAR(50)  PRIMARY KEY,
    initial_date      DATE         NOT NULL,
    final_date        DATE         NOT NULL,
    description       VARCHAR(255) NULL,
    CHECK (final_date >= initial_date)
) ENGINE=InnoDB;

-- Tabla: user_workspace
CREATE TABLE IF NOT EXISTS user_workspace (
    user_workspace_id VARCHAR(50) PRIMARY KEY,
    space             VARCHAR(100) NOT NULL,
    last_connection   DATETIME     NULL,
    active            BOOLEAN      NOT NULL DEFAULT TRUE
) ENGINE=InnoDB;

-- Tabla: user_unal
CREATE TABLE IF NOT EXISTS user_unal (
    email_unal  VARCHAR(100) PRIMARY KEY,
    document    VARCHAR(50)  NOT NULL,
    name        VARCHAR(100) NOT NULL,
    lastname    VARCHAR(100) NOT NULL,
    full_name   VARCHAR(200) NULL,
    gender      VARCHAR(10)  NULL,
    birth_date  DATE         NULL
) ENGINE=InnoDB;

-- Tabla: user_workspace_associate
CREATE TABLE IF NOT EXISTS user_workspace_associate (
    email_unal        VARCHAR(100) NOT NULL,
    user_workspace_id VARCHAR(50)  NOT NULL,
    cod_period        VARCHAR(50)  NOT NULL,
    PRIMARY KEY (email_unal, user_workspace_id, cod_period),
    CONSTRAINT fk_uws_user   FOREIGN KEY (email_unal)        REFERENCES user_unal(email_unal)             ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_uws_space  FOREIGN KEY (user_workspace_id) REFERENCES user_workspace(user_workspace_id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_uws_period FOREIGN KEY (cod_period)        REFERENCES period(cod_period)                ON DELETE RESTRICT ON UPDATE CASCADE,
    INDEX idx_uws_period (cod_period),
    INDEX idx_uws_space (user_workspace_id)
) ENGINE=InnoDB;

-- Tabla: unit_unal
CREATE TABLE IF NOT EXISTS unit_unal (
    cod_unit    VARCHAR(50)  PRIMARY KEY,
    email       VARCHAR(100) NULL,
    name        VARCHAR(100) NOT NULL,
    description TEXT         NULL,
    type_unit   VARCHAR(50)  NULL
) ENGINE=InnoDB;

-- Tabla: user_unit_associate
CREATE TABLE IF NOT EXISTS user_unit_associate (
    email_unal VARCHAR(100) NOT NULL,
    cod_unit   VARCHAR(50)  NOT NULL,
    cod_period VARCHAR(50)  NOT NULL,
    PRIMARY KEY (email_unal, cod_unit, cod_period),
    CONSTRAINT fk_uua_user   FOREIGN KEY (email_unal) REFERENCES user_unal(email_unal)   ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_uua_unit   FOREIGN KEY (cod_unit)   REFERENCES unit_unal(cod_unit)     ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_uua_period FOREIGN KEY (cod_period) REFERENCES period(cod_period)      ON DELETE RESTRICT ON UPDATE CASCADE,
    INDEX idx_uua_unit (cod_unit),
    INDEX idx_uua_period (cod_period)
) ENGINE=InnoDB;

-- Tabla: school
CREATE TABLE IF NOT EXISTS school (
    cod_school   VARCHAR(50)  PRIMARY KEY,
    email        VARCHAR(100) NULL,
    name         VARCHAR(100) NOT NULL,
    description  TEXT         NULL,
    type_facultad VARCHAR(50) NULL
) ENGINE=InnoDB;

-- Tabla: unit_school_associate
CREATE TABLE IF NOT EXISTS unit_school_associate (
    cod_unit   VARCHAR(50) NOT NULL,
    cod_school VARCHAR(50) NOT NULL,
    cod_period VARCHAR(50) NOT NULL,
    PRIMARY KEY (cod_unit, cod_school, cod_period),
    CONSTRAINT fk_usa_unit   FOREIGN KEY (cod_unit)   REFERENCES unit_unal(cod_unit)   ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_usa_school FOREIGN KEY (cod_school) REFERENCES school(cod_school)    ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_usa_period FOREIGN KEY (cod_period) REFERENCES period(cod_period)    ON DELETE RESTRICT ON UPDATE CASCADE,
    INDEX idx_usa_school (cod_school),
    INDEX idx_usa_period (cod_period)
) ENGINE=InnoDB;

-- Tabla: headquarters
CREATE TABLE IF NOT EXISTS headquarters (
    cod_headquarters VARCHAR(50)  PRIMARY KEY,
    email            VARCHAR(100) NULL,
    name             VARCHAR(100) NOT NULL,
    description      TEXT         NULL,
    type_facultad    VARCHAR(50)  NULL
) ENGINE=InnoDB;

-- Tabla: school_headquarters_associate
CREATE TABLE IF NOT EXISTS school_headquarters_associate (
    cod_school       VARCHAR(50) NOT NULL,
    cod_headquarters VARCHAR(50) NOT NULL,
    cod_period       VARCHAR(50) NOT NULL,
    PRIMARY KEY (cod_school, cod_headquarters, cod_period),
    CONSTRAINT fk_sha_school       FOREIGN KEY (cod_school)       REFERENCES school(cod_school)             ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_sha_headquarters FOREIGN KEY (cod_headquarters) REFERENCES headquarters(cod_headquarters) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_sha_period       FOREIGN KEY (cod_period)       REFERENCES period(cod_period)             ON DELETE RESTRICT ON UPDATE CASCADE,
    INDEX idx_sha_headquarters (cod_headquarters),
    INDEX idx_sha_period (cod_period)
) ENGINE=InnoDB;

-- Tabla: type_user
CREATE TABLE IF NOT EXISTS type_user (
    type_user_id VARCHAR(50) PRIMARY KEY,
    name         VARCHAR(100) NOT NULL,
    description  TEXT         NULL
) ENGINE=InnoDB;

-- Tabla: type_user_association
CREATE TABLE IF NOT EXISTS type_user_association (
    email_unal   VARCHAR(100) NOT NULL,
    type_user_id VARCHAR(50)  NOT NULL,
    cod_period   VARCHAR(50)  NOT NULL,
    PRIMARY KEY (email_unal, type_user_id, cod_period),
    CONSTRAINT fk_tua_user   FOREIGN KEY (email_unal)   REFERENCES user_unal(email_unal)     ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_tua_type   FOREIGN KEY (type_user_id) REFERENCES type_user(type_user_id)   ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_tua_period FOREIGN KEY (cod_period)   REFERENCES period(cod_period)        ON DELETE RESTRICT ON UPDATE CASCADE,
    INDEX idx_tua_type (type_user_id),
    INDEX idx_tua_period (cod_period)
) ENGINE=InnoDB;

-- Tabla central de correos emisores
CREATE TABLE IF NOT EXISTS email_sender (
    id    VARCHAR(50)  PRIMARY KEY,
    email VARCHAR(100) NOT NULL UNIQUE,
    name  VARCHAR(100) NULL
) ENGINE=InnoDB;

-- Asociación: email_sender con unidad
CREATE TABLE IF NOT EXISTS email_sender_unit (
    sender_id VARCHAR(50) NOT NULL,
    cod_unit  VARCHAR(50) NOT NULL,
    PRIMARY KEY (sender_id, cod_unit),
    CONSTRAINT fk_esu_sender FOREIGN KEY (sender_id) REFERENCES email_sender(id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_esu_unit   FOREIGN KEY (cod_unit)  REFERENCES unit_unal(cod_unit) ON DELETE CASCADE ON UPDATE CASCADE,
    INDEX idx_esu_unit (cod_unit)
) ENGINE=InnoDB;

-- Asociación: email_sender con escuela
CREATE TABLE IF NOT EXISTS email_sender_school (
    sender_id  VARCHAR(50) NOT NULL,
    cod_school VARCHAR(50) NOT NULL,
    PRIMARY KEY (sender_id, cod_school),
    CONSTRAINT fk_ess_sender FOREIGN KEY (sender_id)  REFERENCES email_sender(id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_ess_school FOREIGN KEY (cod_school) REFERENCES school(cod_school) ON DELETE CASCADE ON UPDATE CASCADE,
    INDEX idx_ess_school (cod_school)
) ENGINE=InnoDB;

-- Asociación: email_sender con sede
CREATE TABLE IF NOT EXISTS email_sender_headquarters (
    sender_id        VARCHAR(50) NOT NULL,
    cod_headquarters VARCHAR(50) NOT NULL,
    PRIMARY KEY (sender_id, cod_headquarters),
    CONSTRAINT fk_esh_sender       FOREIGN KEY (sender_id)        REFERENCES email_sender(id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_esh_headquarters FOREIGN KEY (cod_headquarters) REFERENCES headquarters(cod_headquarters) ON DELETE CASCADE ON UPDATE CASCADE,
    INDEX idx_esh_headquarters (cod_headquarters)
) ENGINE=InnoDB;

-- Auth tables
CREATE TABLE IF NOT EXISTS system_user (
    email           VARCHAR(100) PRIMARY KEY,
    created_at      DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    hashed_password VARCHAR(255) NOT NULL,
    state           BOOLEAN      NOT NULL DEFAULT TRUE,
    salt            VARCHAR(255) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS token (
    jwt_token VARCHAR(512) PRIMARY KEY,
    email     VARCHAR(100) NOT NULL,
    created_at DATETIME    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_token_user FOREIGN KEY (email) REFERENCES system_user(email) ON DELETE CASCADE ON UPDATE CASCADE,
    INDEX idx_token_email (email)
) ENGINE=InnoDB;
