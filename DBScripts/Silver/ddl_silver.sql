/*
===============================================================================
DDL Script: Create Silver Tables
===============================================================================
Script Purpose:
    This script creates tables in the 'Silver' schema, dropping existing tables 
    if they already exist.
	  Run this script to re-define the DDL structure of 'Silver' Tables
	  Table Name:
		1. Silver.stg_accounts
		2. Silver.stg_transactions
===============================================================================
*/

IF OBJECT_ID('Silver.stg_accounts', 'U') IS NOT NULL
    DROP TABLE Silver.stg_accounts;
GO

CREATE TABLE Silver.stg_accounts (
    account_id							VARCHAR(100) PRIMARY KEY,
	mask								VARCHAR(10),
    name								NVARCHAR(255),
    official_name						NVARCHAR(255),
    type								VARCHAR(50),
    subtype								VARCHAR(50),
	holder_category						VARCHAR(100),
    balances_available					DECIMAL(18, 2),
    balances_current					DECIMAL(18, 2),
    balances_limit						DECIMAL(18, 2),
    balances_iso_currency_code			VARCHAR(10),
    balances_unofficial_currency_code	VARCHAR(10)
);
GO

IF OBJECT_ID('Silver.stg_transactions', 'U') IS NOT NULL
    DROP TABLE Silver.stg_transactions;
GO

CREATE TABLE Silver.stg_transactions (
    transaction_id VARCHAR(100) PRIMARY KEY,
    account_id VARCHAR(100),
    name NVARCHAR(255),
    amount DECIMAL(18, 2),
    date DATE,
    authorized_date DATE,
    merchant_name NVARCHAR(255),
    category NVARCHAR(255),
    category_id VARCHAR(100),
    iso_currency_code VARCHAR(10),
    payment_channel VARCHAR(50),
    pending BIT,
    counterparty_name NVARCHAR(255),
    counterparty_type VARCHAR(100),
    location_city NVARCHAR(100),
    location_region NVARCHAR(100),
    location_country VARCHAR(50),
    payment_meta_reference_number VARCHAR(100),
    payment_meta_payee NVARCHAR(255),
    personal_finance_category_primary VARCHAR(100),
    personal_finance_category_detailed VARCHAR(100)
);
GO