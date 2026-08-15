IF DB_ID('VaccineLab') IS NULL
    CREATE DATABASE VaccineLab;
GO

IF DB_ID('TestLab') IS NULL
    CREATE DATABASE TestLab;
GO

USE VaccineLab;
GO

CREATE TABLE users (
    id INT IDENTITY(1,1) PRIMARY KEY,
    username VARCHAR(50),
    password VARCHAR(100)
);
GO

INSERT INTO users (username, password)
VALUES
    ('admin', 'test'),
    ('root', 'rootpass');
GO

USE TestLab;
GO

CREATE TABLE products (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name VARCHAR(50)
);
GO

INSERT INTO products (name)
VALUES
    ('Laptop'),
    ('Mouse');
GO
