/*
=============================================================
Create Database and Schemas
=============================================================
Script Purpose:
    This script creates a new database named 'DataWarehouse' after checking if it already exists. 
    If the database exists, it is dropped and recreated. Additionally, the script sets up three schemas 
    within the database: 'bronze', 'silver', and 'gold'.
	
WARNING:
    Running this script will drop the entire 'DataWarehouse' database if it exists. 
    All data in the database will be permanently deleted. Proceed with caution 
    and ensure you have proper backups before running this script.
*/

USE master;
GO

-- Drop and recreate the 'PersonalFinanceDW' database
IF EXISTS (SELECT 1 FROM sys.databases WHERE name = 'PersonalFinanceDW')
BEGIN
    ALTER DATABASE PersonalFinanceDW SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
    DROP DATABASE PersonalFinanceDW;
END;
GO

-- Create the 'PersonalFinanceDW' database
CREATE DATABASE PersonalFinanceDW;
GO

--Use the created database 'DataWarehouse'
Use PersonalFinanceDW;
GO

--Create the schema for Bronze Layer
Create Schema Bronze;
GO

--Create the schema for Silver Layer
Create Schema Silver;
GO

--Create the schema for Gold Layer
Create Schema Gold;
GO
