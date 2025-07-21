import math
import os
import json
import logging
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import pyodbc

# === Setup Logging ===
def setup_logger():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_dir = "logs/silver"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"silver_{timestamp}.log")

    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logging.getLogger().addHandler(console)
    logging.info("Silver Layer processing started.")
    return timestamp

# === Load Environment Variables ===
def load_db_credentials():
    load_dotenv()
    #print (os.getenv("SQL_USERNAME"))
    #print (os.getenv("SQL_PASSWORD"))
    return {
        "server": os.getenv("SQL_SERVER"),
        "database": os.getenv("SQL_DATABASE"),
        "username": os.getenv("SQL_USERNAME"),
        "password": os.getenv("SQL_PASSWORD")
    }

# === Extract and Flatten Counterparties ===
def extract_counterparty_info(counterparties):
    if isinstance(counterparties, list) and len(counterparties) > 0:
        cp = counterparties[0]
        return cp.get("name"), cp.get("type")
    return None, None

# === Flatten a Single Transaction Record ===
def flatten_transaction(tx):
    cp_name, cp_type = extract_counterparty_info(tx.get("counterparties", []))
    loc = tx.get("location", {})
    pmeta = tx.get("payment_meta", {})
    pfcat = tx.get("personal_finance_category", {})

    return {
        "transaction_id": tx.get("transaction_id"),
        "account_id": tx.get("account_id"),
        "name": tx.get("name"),
        "amount": tx.get("amount"),
        "date": tx.get("date"),
        "authorized_date": tx.get("authorized_date"),
        "merchant_name": tx.get("merchant_name"),
        "category": ', '.join(tx.get("category") if isinstance(tx.get("category"), list) else []),
        "category_id": tx.get("category_id"),
        "iso_currency_code": tx.get("iso_currency_code"),
        "payment_channel": tx.get("payment_channel"),
        "pending": tx.get("pending"),
        "counterparty_name": cp_name,
        "counterparty_type": cp_type,
        "location_city": loc.get("city"),
        "location_region": loc.get("region"),
        "location_country": loc.get("country"),
        "payment_meta_reference_number": pmeta.get("reference_number"),
        "payment_meta_payee": pmeta.get("payee"),
        "personal_finance_category_primary": pfcat.get("primary"),
        "personal_finance_category_detailed": pfcat.get("detailed"),
    }

# === To get account data ===
def get_account_details(accounts):
    acc_data = pd.json_normalize(accounts)
    acc_df = pd.DataFrame(acc_data)
   

    acc_df.columns = [col.replace(".", "_") for col in acc_df.columns]
    
    #print(acc_df.columns)
    return acc_df


# === Enforce Schema ===
def enforce_schema(df, expected_columns):
    for col in expected_columns:
        if col not in df.columns:
            df[col] = None
    return df[expected_columns]

# === Process and Save to Silver Layer ===
def process_json_to_silver(filepath, timestamp):
    with open(filepath, 'r') as f:
        raw_data = json.load(f)

    transactions = raw_data.get("transactions", [])
    accounts = raw_data.get("accounts", [])

    tx_data = [flatten_transaction(tx) for tx in transactions]
    tx_df = pd.DataFrame(tx_data)

    # Cleaning and transformations
    expected_tx_cols = [
        "transaction_id", "account_id", "name", "amount", "date", "authorized_date", "merchant_name",
        "category", "category_id", "iso_currency_code", "payment_channel", "pending",
        "counterparty_name", "counterparty_type", "location_city", "location_region", "location_country",
        "payment_meta_reference_number", "payment_meta_payee", "personal_finance_category_primary",
        "personal_finance_category_detailed"
    ]
    tx_df = enforce_schema(tx_df, expected_tx_cols)
    tx_df = tx_df[tx_df["amount"].apply(lambda x: isinstance(x, (int, float)) and x >= 0)]
    tx_df["date"] = pd.to_datetime(tx_df["date"], errors="coerce")
    tx_df["authorized_date"] = pd.to_datetime(tx_df["authorized_date"], errors="coerce")
    tx_df["merchant_name"] = tx_df["merchant_name"].astype(str).str.strip().str.lower()
    tx_df["category"] = tx_df["category"].astype(str).str.lower()
    tx_df["iso_currency_code"] = tx_df["iso_currency_code"].fillna("USD")
    tx_df["payment_channel"] = tx_df["payment_channel"].fillna("online")
    tx_df = tx_df[~tx_df["date"].isnull()]

    expected_accx_df_cols = ["account_id", "mask", "name", "official_name", "type", "subtype",
       "holder_category", "balances_available", "balances_current",
       "balances_limit", "balances_iso_currency_code",
       "balances_unofficial_currency_code"]
    

    acc_df = get_account_details(accounts)
    acc_df = enforce_schema(acc_df, expected_accx_df_cols)

    # Ensure numeric columns are coerced properly
    acc_df['balances_available'] = pd.to_numeric(acc_df['balances_available'], errors='coerce')
    acc_df['balances_current'] = pd.to_numeric(acc_df['balances_current'], errors='coerce')
    acc_df['balances_limit'] = pd.to_numeric(acc_df['balances_limit'], errors='coerce')
    float_cols = ['balances_available', 'balances_current', 'balances_limit']
    for col in float_cols:
        acc_df[col] = acc_df[col].apply(lambda x: None if pd.isna(x) else x)

    acc_df = acc_df.replace({pd.NA: None, pd.NaT: None, float('nan'): None, 'nan': None, 'NaN': None})
    acc_df = acc_df.where(pd.notnull(acc_df), None)
    tx_df = tx_df.where(pd.notnull(tx_df), None)

    for col in ['balances_available', 'balances_current', 'balances_limit']:
        acc_df[col] = acc_df[col].astype(float)

    silver_dir = "data/silver"
    os.makedirs(silver_dir, exist_ok=True)
    tx_csv = os.path.join(silver_dir, f"transactions_clean_{timestamp}.csv")
    acc_csv = os.path.join(silver_dir, f"accounts_clean_{timestamp}.csv")
    tx_df.to_csv(tx_csv, index=False)
    acc_df.to_csv(acc_csv, index=False)

    logging.info(f"Saved cleaned transactions to {tx_csv}")
    logging.info(f"Saved cleaned accounts to {acc_csv}")
    return tx_df, acc_df, tx_csv, acc_csv

# === Insert Data into SQL Server ===
def insert_into_sql(df, table_name, creds):
    conn_str = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={creds['server']};"
        f"DATABASE={creds['database']};"
        f"UID={creds['username']};"
        f"PWD={creds['password']}"
    )
    try:
        with pyodbc.connect(conn_str) as conn:
            cursor = conn.cursor()
            for index, row in df.iterrows():
                placeholders = ', '.join(['?'] * len(row))
                columns = ', '.join(row.index)
                sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

                # Force convert float NaN to None
                values = [
                    None if (isinstance(val, float) and math.isnan(val)) else val
                    for val in row.values
                ]
                cursor.execute(sql, *values)
            conn.commit()
        logging.info(f"Inserted data into SQL Server table: {table_name}")
    except Exception as e:
        logging.error(f"Failed to insert into {table_name}: {e}")
        print(sql)

# === Update Metadata Log ===
def update_metadata_log(filename, record_count, status, timestamp):
    metadata_file = "logs/silver/metadata_log.csv"
    os.makedirs(os.path.dirname(metadata_file), exist_ok=True)
    log_entry = {
        "filename": filename,
        "timestamp": timestamp,
        "records": record_count,
        "status": status
    }
    df = pd.DataFrame([log_entry])
    if os.path.exists(metadata_file):
        df.to_csv(metadata_file, mode='a', header=False, index=False)
    else:
        df.to_csv(metadata_file, index=False)
    logging.info(f"Metadata logged for {filename}")

# === Main ===
if __name__ == "__main__":
    try:
        ts = setup_logger()
        creds = load_db_credentials()

        bronze_dir = "data/bronze"
        files = sorted([f for f in os.listdir(bronze_dir) if f.endswith(".json")])
        latest_file = os.path.join(bronze_dir, files[-1]) if files else None

        if not latest_file:
            logging.warning("No JSON file found in bronze layer.")
            exit()

        logging.info(f"Processing file: {latest_file}")
        tx_df, acc_df, tx_csv, acc_csv = process_json_to_silver(latest_file, ts)

        insert_into_sql(tx_df, "Silver.stg_transactions", creds)
        insert_into_sql(acc_df, "Silver.stg_accounts", creds)

        update_metadata_log(latest_file, len(tx_df), "Success", ts)

        logging.info("Silver layer completed successfully!")

    except Exception as e:
        logging.error("Silver layer failed.", exc_info=True)
