/*
===============================================================================
DDL Script: Create Gold Tables
===============================================================================
Script Purpose:
    This script creates tables in the 'Gold' schema, dropping existing tables 
    if they already exist.
	  Run this script to re-define the DDL structure of 'Gold' Tables
	  Table Name:
		1. Gold.dim_account
		2. Gold.dim_date
		3. Gold.dim_category
		4. Gold.fact_transactions
===============================================================================
*/

CREATE TABLE Gold.dim_account (
    account_sk INT IDENTITY(1,1) PRIMARY KEY,		--Surrogate key
	account_id				VARCHAR(100),
	mask					VARCHAR(10),
	name					VARCHAR(255),
	official_name			VARCHAR(255),
	type					VARCHAR(50),
	subtype					VARCHAR(50),
	holder_category			VARCHAR(100),
	currency_code			VARCHAR(10),
	is_active				BIT,
	start_date				DATE,
	end_date				DATE,
	current_flag			BIT,
	UNIQUE(account_id, start_date) 
);

CREATE TABLE Gold.dim_date (
	date_sk			INT PRIMARY KEY,		--Surrogate key
	date			DATE,
	day				INT,
	month			INT,
	month_name		VARCHAR(15),
	year			INT,
	quarter			INT,
	day_of_week		VARCHAR(10)
);

CREATE TABLE Gold.dim_category (
	category_sk			INT IDENTITY(1,1) PRIMARY KEY,	--Surrogate key
	primary_category	VARCHAR(100),
	detailed_category	VARCHAR(150),
	UNIQUE(primary_category, detailed_category)
);


CREATE TABLE Gold.fact_transactions (
	transaction_sk			INT IDENTITY(1,1) PRIMARY KEY,		--Surrogate key
	transaction_id						VARCHAR(100),
	account_sk							INT,					--FK to dim_account
	date_sk								INT,					--FK to dim_date
	merchant_name						VARCHAR(255),
	amount								DECIMAL(18,2),
	currency_code						VARCHAR(10),
	payment_channel						VARCHAR(50),
	category_sk							INT,					--FK to dim_category
	pending_flag						BIT,					--	1 = pending, 0 = posted
	created_at							DATETIME DEFAULT getdate()--Load timestamp
	FOREIGN KEY (account_sk) REFERENCES Gold.dim_account(account_sk)  ON DELETE NO ACTION ON UPDATE CASCADE,
	FOREIGN KEY (date_sk) REFERENCES Gold.dim_date(date_sk)  ON DELETE NO ACTION ON UPDATE CASCADE,
	FOREIGN KEY (category_sk) REFERENCES Gold.dim_category(category_sk)  ON DELETE NO ACTION ON UPDATE CASCADE,
	UNIQUE(transaction_id)
);
GO