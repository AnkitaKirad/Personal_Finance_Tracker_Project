# Personal Finance Tracker Project

This project builds a complete data pipeline and warehouse to track and analyze personal financial transactions using the **Plaid API**. The goal is to apply modern data engineering and warehousing principles using a **medallion architecture** (Bronze → Silver → Gold) and implement **SCD Type 2** for dimension tracking.

---

## 🚀 Project Overview

- **Domain:** Personal Finance
- **Goal:** Build an end-to-end data warehouse to analyze and track financial transactions
- **Data Source:** JSON data exported from the **Plaid API**
- **Architecture:** Medallion Architecture (Bronze → Silver → Gold)
- **Database:** Microsoft SQL Server
- **Tools & Technologies:** Python, Pandas, SQL, PyODBC, Dotenv, Plaid data

---

## 📂 Architecture Diagram

> *(Attach or link the visual diagram here)*  
> Diagram should show: Bronze → Silver → Gold → Views → Reporting

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

## 🧠 Learning Outcomes

- End-to-end ETL implementation
- Warehouse design principles
- Writing production-grade Python ETL scripts
- Implementing SCD Type 2 manually
- Creating reusable stored procedures
- Working with financial APIs & semi-structured data

---

## 📁 Folder Structure

