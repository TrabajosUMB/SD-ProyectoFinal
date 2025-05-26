-- Crear la base de datos
CREATE DATABASE JobRadarDB;
GO

USE JobRadarDB;
GO

-- Crear tablas necesarias para Django
CREATE TABLE [auth_user] (
    [id] [int] IDENTITY(1,1) NOT NULL PRIMARY KEY,
    [password] [nvarchar](128) NOT NULL,
    [last_login] [datetime2](7) NULL,
    [is_superuser] [bit] NOT NULL,
    [username] [nvarchar](150) NOT NULL UNIQUE,
    [first_name] [nvarchar](150) NOT NULL,
    [last_name] [nvarchar](150) NOT NULL,
    [email] [nvarchar](254) NOT NULL,
    [is_staff] [bit] NOT NULL,
    [is_active] [bit] NOT NULL,
    [date_joined] [datetime2](7) NOT NULL
);

-- Crear tabla para perfiles de usuario
CREATE TABLE [user_profile] (
    [id] [int] IDENTITY(1,1) NOT NULL PRIMARY KEY,
    [user_id] [int] NOT NULL UNIQUE,
    [professional_title] [nvarchar](200) NULL,
    [experience_years] [int] NOT NULL DEFAULT 0,
    [skills] [nvarchar](max) NULL,
    CONSTRAINT [FK_UserProfile_User] FOREIGN KEY([user_id]) REFERENCES [auth_user] ([id])
);

-- Crear tabla para ofertas de trabajo
CREATE TABLE [job_offer] (
    [id] [int] IDENTITY(1,1) NOT NULL PRIMARY KEY,
    [title] [nvarchar](200) NOT NULL,
    [company] [nvarchar](200) NOT NULL,
    [location] [nvarchar](200) NOT NULL,
    [salary_min] [decimal](10, 2) NOT NULL,
    [salary_max] [decimal](10, 2) NOT NULL,
    [description] [nvarchar](max) NOT NULL,
    [skills_required] [nvarchar](max) NOT NULL,
    [url] [nvarchar](500) NOT NULL,
    [modality] [nvarchar](50) NOT NULL,
    [contract_type] [nvarchar](50) NOT NULL,
    [education_level] [nvarchar](50) NOT NULL,
    [experience_years] [int] NOT NULL,
    [is_active] [bit] NOT NULL DEFAULT 1,
    [created_at] [datetime2](7) NOT NULL DEFAULT GETDATE()
);

-- Crear índices
CREATE INDEX [IX_JobOffer_Title] ON [job_offer] ([title]);
CREATE INDEX [IX_JobOffer_Company] ON [job_offer] ([company]);
CREATE INDEX [IX_JobOffer_Location] ON [job_offer] ([location]);
GO
