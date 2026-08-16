IF DB_ID('VaccineLab') IS NULL
BEGIN
    CREATE DATABASE VaccineLab;
END
GO

USE VaccineLab;
GO

IF OBJECT_ID('users', 'U') IS NULL
BEGIN
    CREATE TABLE users (
        id INT IDENTITY(1,1) PRIMARY KEY,
        username VARCHAR(50),
        password VARCHAR(100)
    );
END
GO

IF NOT EXISTS (SELECT 1 FROM users)
BEGIN
    INSERT INTO users (username, password)
    VALUES
        ('admin', 'test'),
        ('root', 'rootpass');
END
GO

IF OBJECT_ID('products', 'U') IS NULL
BEGIN
    CREATE TABLE products (
        id INT IDENTITY(1,1) PRIMARY KEY,
        name VARCHAR(50)
    );
END
GO

IF NOT EXISTS (SELECT 1 FROM products)
BEGIN
    INSERT INTO products (name)
    VALUES
        ('Laptop'),
        ('Mouse');
END
GO
