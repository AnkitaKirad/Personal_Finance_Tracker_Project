# Personal Finance Tracker Project

This project builds a complete data pipeline and warehouse to track and analyze personal financial transactions using the **Plaid API**. The goal is to apply modern data engineering and warehousing principles using a **medallion architecture** (Bronze → Silver → Gold) and implement **SCD Type 2** for dimension tracking.

---
## 🚀 Project Overview

- **Domain:** Personal Finance
- **Goal:** Build an end-to-end data warehouse to analyze and track financial transactions
- **Tools & Technologies:** Python, Pandas, SQL, PyODBC, Dotenv, Plaid data
- **Data Source:** JSON data exported from the **Plaid API**
- **Architecture:** Medallion Architecture (Bronze → Silver → Gold)
- **Database:** Microsoft SQL Server

---
## 🔧 Tech Stack
- **Python** – Data ingestion & transformation
- **SQL Server** – DWH backend & procedural logic
- **Pandas** – JSON flattening & preprocessing
- **T-SQL Stored Procedures** – Gold layer logic
- **ODBC** – Python-to-SQL connection
- **Version Control** – Git & GitHub

---
## 🏗️ Layers Explained

### 🥉 Bronze Layer
- Raw Plaid JSON files are collected and stored
- No transformations applied

### 🥈 Silver Layer
- Data is flattened, cleaned, and validated using Python
- CSVs generated for cleaned transactions and accounts
- Inserted into SQL Server staging tables

### 🥇 Gold Layer
- Star Schema designed with:
  - `fact_transactions`
  - `dim_account` (SCD Type 2)
  - `dim_date`
  - `dim_category`
- Stored Procedures handle loading with change detection & SCD logic
- Metadata logging for traceability

---
## 🧱 Schema Design
- ### Dimension Tables:
  - `dim_account`: All account-level metadata (type, holder, currency).
  - `dim_date`: Calendar table generated via recursive CTE.
  - `dim_category`: Extracted from transaction-level category array.
- ### Fact Table:
  - `fact_transactions`: Transaction fact table with FKs to dimensions and supporting attributes.
  
---
## 📊 Reporting Layer
- SQL views created for common analytics:
  - Total monthly spending
  - Top spending categories
  - Spending by merchant

---
## ✅ Key Features & Learnings

- 🔁 **SCD Type 2 Implementation** in `dim_account` for historical tracking
- 🏛️ **Star Schema** design to optimize analytics queries
- 📅 Dynamic `dim_date` generation using Recursive CTE
- 📦 **Stored Procedures** for Gold layer ETL logic
- 🔎 Robust data cleaning and validation in Python
- 📄 Metadata logging for traceability of pipeline runs

---

## 🧠 Highlights & Learning Outcomes

- ✅ Implemented full **ETL** pipeline using Python and SQL Server
- ✅ Applied **Medallion Architecture** in a real-world scenario
- ✅ Designed a robust **star schema**
- ✅ Implemented **SCD-1** logic using SQL Server Stored Procedures
- ✅ Built **reporting views** for insights without dashboard tools
- ✅ Learned how to handle data quality issues (NaNs, type mismatches, key violations)
- ✅ Strengthened SQL Server stored procedure & CTE knowledge

---

## 📁 Folder Structure

/plaid-dwh
│
├── /data
|   ├── /bronze
|   |     └── transactions_2025-07-20_13-50-30.json
|   ├── /Silver
|   |     ├──accounts_clean_2025-07-20_13-50-47.csv
|   |     └──transactions_clean_2025-07-20_13-50-47.csv
│   
├── /DBScripts
|   ├── DB_and_Schema_Creation_Scripts.sql
|   ├── Login_and_User_Creation.sql
|   ├── /silver
|   |     └── ddl_silver.sql
│   ├── /Gold
|   |     ├── ddl_gold.sql
│   |     ├── Load_dim_date_table.sql
│   |     ├── sp_load_dim_account_table.sql
│   |     ├── sp_load_dim_category_table.sql
│   |     └── sp_load_fact_transactions_table.sql
│   ├── /Reporting_Aggreated_Views
|   |     ├── Create_View__spent_by_category.sql
│   |     ├── Create_View__spent_on_per_merchant.sql
│   |     ├── Create_View_monthly_spent.sql
│   |     └── Create_View_monthly_spent_per_account.sql
│
├── /scripts
│   ├── extract.py
│   ├── transform.py
│   └── load.py
│
├── /docs
│   └── architecture.png
│
├── .env
├── Folder_Creation_Script.py
├── test_plaid.py
└── readme.md

---
## 🛠️ Setup & Execution

1. Configure `.env` for database credentials
2. Place raw JSONs in `data/bronze`
3. Run `silver_cleaner.py` to clean and load data to Silver layer
4. Execute Gold layer stored procedures (or run `gold_loader.py`)
5. Query reporting views from SQL Server

---
## 📌 Final Thoughts

This project simulates a **real-world finance data platform**, showcasing:
- Strong fundamentals in warehousing
- Data modeling best practices
- Hands-on pipeline building

---
## 🔗 Connect

If you liked this project or learned from it, feel free to connect with me or check out more of my work!
Linkedin: www.linkedin.com/in/ankitakirad
