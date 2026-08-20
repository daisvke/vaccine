/*
STRING      => CHAR, VARCHAR, NCHAR, NVARCHAR, TEXT, NTEXT
INTEGER     => TINYINT, SMALLINT, INT, BIGINT
BOOLEAN     => BIT
UNSUPPORTED => DECIMAL, FLOAT
*/

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
        password VARCHAR(100),

        -- Boolean
        is_admin BIT,

        -- Integer types
        tiny_number TINYINT,
        small_number SMALLINT,
        medium_number INT,
        big_number BIGINT,

        -- String types
        fixed_text CHAR(10),
        short_text VARCHAR(100),
        unicode_fixed_text NCHAR(10),
        unicode_text NVARCHAR(100),
        long_text TEXT,
        unicode_long_text NTEXT,

        -- Unsupported
        decimal_value DECIMAL(10, 2),
        float_value FLOAT
    );
END
GO

IF NOT EXISTS (SELECT 1 FROM users)
BEGIN
    INSERT INTO users (
        username,
        password,
        is_admin,
        tiny_number,
        small_number,
        medium_number,
        big_number,
        fixed_text,
        short_text,
        unicode_fixed_text,
        unicode_text,
        long_text,
        unicode_long_text,
        decimal_value,
        float_value
    )
    VALUES
    (
        'admin',
        'test',
        1,
        10,
        100,
        100000,
        9000000000,
        'admin',
        'Administrator',
        N'admin',
        N'Administrator',
        'Administrator account',
        N'Administrator account',
        1234.56,
        1.5
    ),
    (
        'root',
        'rootpass',
        0,
        20,
        200,
        200000,
        8000000000,
        'root',
        'Root User',
        N'root',
        N'Root User',
        'Root account',
        N'Root account',
        42.50,
        3.14159
    );
END
GO
